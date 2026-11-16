#!/usr/bin/env python3
"""banc_performance.py — le banc reproductible de `drave analyser`.

Ce que le banc mesure, et comment :

1. **le texte réel de 10 000 mots** — un préfixe exact du corpus (10 000 tokens `mot` ou
   `nombre`, coupés au 10 000e token, pas au caractère), analysé par le CLI (`--json`) et
   par la fonction (`Heuristique.analyser`) dans un sous-processus neuf ;
2. **100 phrases courtes** — 100 phrases réelles de 3 à 12 mots, mesurées en 100 appels
   séparés (le coût fixe du CLI), en 100 appels dans un même processus (le coût fixe de la
   fonction), et en un seul appel `--jsonl` (le lot) ;
3. **`--tagger`** — le même lot de 100 phrases, puis éventuellement les 10 000 mots, avec
   un cache DeepSeek **froid** (`DEEPSEEK_CACHE` dans un répertoire temporaire) : le coût
   réseau, les tokens et les appels sont lus dans la ligne `TAGGER API` du CLI ;
4. **le contrôle négatif de linéarité** — un bloc de phrases entières répété 1, 2, 4, 8,
   16, 32 et 40 fois : le temps doit croître linéairement avec la taille, pas
   quadratiquement. Le banc ajuste `t = a + b·n` et `t = a + b·n + c·n²`, calcule la pente
   log-log et les rapports de doublement. Un **contrôle de l'instrument** (une boucle
   volontairement linéaire et une boucle volontairement quadratique) vérifie que la pente
   log-log distingue bien 1 de 2.

Le banc est **hors ligne par défaut** : `--avec-tagger` est nécessaire pour le réseau.
Tout est en bibliothèque standard. Le JSON de sortie est stable (pas d'horodatage dans les
mesures, seulement `date` et l'environnement) et contient les mesures brutes, les
ajustements et le verdict.

    python3 tools/banc_performance.py --rapide
    python3 tools/banc_performance.py --avec-tagger --tagger-complet

La fiche est `reports/rapport-performance.md` ; le JSON, `reports/performance.json`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import pathlib
import platform
import resource
import shutil
import statistics
import subprocess
import sys
import tempfile
import time

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "tools"))

import bloc_linguistique as bl  # noqa: E402  (après l'installation du chemin)

TAILLES = (250, 500, 1000, 2000, 4000, 8000, 10000)
SOURCE = "data/corpus_fr_litterature.txt"
MOTS = 10000
PHRASES_COURTES = 100
REPETITIONS = 3
TIME_BIN = shutil.which("time") or "/usr/bin/time"


# --------------------------------------------------------------------------- outils


def _sha256(texte: str) -> str:
    return hashlib.sha256(texte.encode("utf-8", "replace")).hexdigest()


def _mots(texte: str) -> list[tuple[int, int, str, str]]:
    return [m for m in bl.Heuristique._mots(texte) if m[3] in ("mot", "nombre")]


def _compter_mots(texte: str) -> int:
    return len(_mots(texte))


def _prefixe_mots(texte: str, n: int) -> tuple[str, int]:
    """Le préfixe qui contient exactement `n` tokens mot/nombre (ou tout le texte)."""
    mots = _mots(texte)
    if not mots:
        return texte, 0
    n = max(1, min(int(n), len(mots)))
    return texte[:mots[n - 1][1]], n


def _bloc_phrases(texte: str, cible: int = 250) -> tuple[str, int, int]:
    """Un bloc de phrases entières, le plus proche possible de `cible` mots."""
    phrases = bl.Heuristique._phrases(texte)
    bloc = ""
    debut = fin = 0
    for d, f, _typ, _ in phrases:
        morceau = texte[d:f].strip()
        if not morceau:
            continue
        n = _compter_mots(morceau)
        if bloc and _compter_mots(bloc) + n > cible:
            break
        if not bloc:
            debut = d
        bloc = (bloc + "\n\n" + morceau).strip()
        fin = f
    return bloc, debut, fin


def _phrases_courtes(texte: str, n: int = 100) -> list[str]:
    """`n` phrases réelles de 3 à 12 mots, une seule phrase par entrée.

    On garde l'ordre du texte. Si le texte n'en fournit pas assez, on complète avec les
    phrases les plus courtes (toujours dans l'ordre du texte) — le critère est consigné.
    """
    candidates: list[tuple[int, int, str]] = []
    for i, (d, f, _typ, _) in enumerate(bl.Heuristique._phrases(texte)):
        texte_phrase = " ".join(texte[d:f].split())
        if not texte_phrase:
            continue
        mots = _compter_mots(texte_phrase)
        if 3 <= mots <= 12 and len(bl.Heuristique._phrases(texte_phrase)) == 1:
            candidates.append((i, mots, texte_phrase))
    if len(candidates) >= n:
        return [x[2] for x in candidates[:n]]
    # repli : les phrases les plus courtes, puis l'ordre du texte
    toutes = []
    for i, (d, f, _typ, _) in enumerate(bl.Heuristique._phrases(texte)):
        texte_phrase = " ".join(texte[d:f].split())
        if texte_phrase and len(bl.Heuristique._phrases(texte_phrase)) == 1:
            toutes.append((i, _compter_mots(texte_phrase), texte_phrase))
    toutes.sort(key=lambda x: (x[1], x[0]))
    return [x[2] for x in toutes[:n]]


def _ols(xs: list[float], ys: list[float]) -> dict:
    """Moindres carrés `y = a + b·x` : pente, ordonnée, R², RMSE."""
    n = len(xs)
    if n < 2:
        return {"a": 0.0, "b": 0.0, "r2": 0.0, "rmse": 0.0, "n": n}
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx if sxx else 0.0
    a = my - b * mx
    ss_tot = sum((y - my) ** 2 for y in ys)
    ss_res = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    return {"a": a, "b": b,
            "r2": (1.0 - ss_res / ss_tot) if ss_tot else 0.0,
            "rmse": math.sqrt(ss_res / n), "n": n}


def _resoudre_3x3(m: list[list[float]], v: list[float]) -> list[float] | None:
    """Gauss-Jordan pour le système normal du polynôme de degré 2."""
    a = [row[:] + [v[i]] for i, row in enumerate(m)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) < 1e-18:
            return None
        a[col], a[pivot] = a[pivot], a[col]
        p = a[col][col]
        a[col] = [x / p for x in a[col]]
        for r in range(3):
            if r == col:
                continue
            f = a[r][col]
            if f:
                a[r] = [x - f * y for x, y in zip(a[r], a[col])]
    return [a[i][3] for i in range(3)]


def _quadratique(xs: list[float], ys: list[float]) -> dict:
    """Moindres carrés `y = a + b·x + c·x²`."""
    n = len(xs)
    if n < 3:
        return {"a": 0.0, "b": 0.0, "c": 0.0, "r2": 0.0, "rmse": 0.0, "n": n}
    s = [sum(x ** k for x in xs) for k in range(5)]
    t = [sum(y * x ** k for x, y in zip(xs, ys)) for k in range(3)]
    m = [[s[0], s[1], s[2]], [s[1], s[2], s[3]], [s[2], s[3], s[4]]]
    coef = _resoudre_3x3(m, t)
    if coef is None:
        return {"a": 0.0, "b": 0.0, "c": 0.0, "r2": 0.0, "rmse": 0.0, "n": n}
    a, b, c = coef
    my = sum(ys) / n
    ss_tot = sum((y - my) ** 2 for y in ys)
    ss_res = sum((y - (a + b * x + c * x * x)) ** 2 for x, y in zip(xs, ys))
    return {"a": a, "b": b, "c": c,
            "r2": (1.0 - ss_res / ss_tot) if ss_tot else 0.0,
            "rmse": math.sqrt(ss_res / n), "n": n}


def _loglog(xs: list[float], ys: list[float]) -> dict:
    """La pente α de `log t = α·log n + β` — α = 1 linéaire, α = 2 quadratique."""
    paires = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    if len(paires) < 2:
        return {"alpha": 0.0, "beta": 0.0, "r2": 0.0, "n": len(paires)}
    lx = [math.log(x) for x, _ in paires]
    ly = [math.log(y) for _, y in paires]
    fit = _ols(lx, ly)
    return {"alpha": fit["b"], "beta": fit["a"], "r2": fit["r2"],
            "rmse": fit["rmse"], "n": fit["n"]}


def _mediane(valeurs: list[float]) -> float:
    return statistics.median(valeurs) if valeurs else 0.0


def _p95(valeurs: list[float]) -> float:
    if not valeurs:
        return 0.0
    v = sorted(valeurs)
    return v[min(len(v) - 1, int(round(0.95 * (len(v) - 1))))]


def _resume(valeurs: list[float]) -> dict:
    return {"n": len(valeurs), "mediane": _mediane(valeurs),
            "moyenne": statistics.mean(valeurs) if valeurs else 0.0,
            "min": min(valeurs) if valeurs else 0.0,
            "max": max(valeurs) if valeurs else 0.0,
            "p95": _p95(valeurs)}


# --------------------------------------------------------------------------- exécution


def _run(cmd: list[str], *, env: dict | None = None, timeout: float = 7200.0,
         entree: bytes | None = None) -> dict:
    """Un sous-processus, son temps mural, son pic RSS (GNU time), sa sortie.

    `/usr/bin/time -f %M` mesure le **pic RSS du seul enfant** ; `resource` ne donnerait que
    le maximum de tous les enfants déjà lancés. Si GNU time manque, `rss_kb` vaut `None`
    et le champ `outil_memoire` le dit.
    """
    env = dict(os.environ if env is None else env)
    env.setdefault("PYTHONHASHSEED", "0")
    rss_path = None
    cmd_time = cmd
    outil = "resource"
    if TIME_BIN and pathlib.Path(TIME_BIN).is_file():
        fd, rss_path = tempfile.mkstemp(prefix="banc-rss-", suffix=".txt")
        os.close(fd)
        cmd_time = [TIME_BIN, "-f", "%M", "-o", rss_path, "--"] + cmd
        outil = f"{TIME_BIN} -f %M"
    t0 = time.perf_counter()
    try:
        p = subprocess.run(cmd_time, capture_output=True, env=env, timeout=timeout,
                           input=entree, cwd=str(RACINE))
        duree = time.perf_counter() - t0
        rss_kb = None
        if rss_path:
            try:
                rss_kb = int(pathlib.Path(rss_path).read_text(encoding="utf-8").strip())
            except (OSError, ValueError):
                rss_kb = None
        if rss_kb is None:
            rss_kb = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        return {"code": p.returncode, "duree_s": duree, "rss_kb": rss_kb,
                "stdout": p.stdout, "stderr": p.stderr.decode("utf-8", "replace"),
                "outil_memoire": outil, "commande": cmd}
    finally:
        if rss_path:
            try:
                os.unlink(rss_path)
            except OSError:
                pass


def _run_analyse(texte_path: pathlib.Path, repetitions: int) -> dict:
    """La fonction `Heuristique.analyser` seule, dans un sous-processus neuf."""
    resultats = []
    for _ in range(max(1, repetitions)):
        sortie = texte_path.with_suffix(".annotation.json")
        r = _run([sys.executable, str(pathlib.Path(__file__).resolve()),
                  "--interne", "--fichier", str(texte_path), "--sortie-json", str(sortie)])
        if r["code"] != 0:
            raise RuntimeError(f"interne : code {r['code']} — {r['stderr'][:300]}")
        d = json.loads(r["stdout"].decode("utf-8"))
        d["rss_processus_kb"] = r["rss_kb"]
        d["duree_processus_s"] = r["duree_s"]
        resultats.append(d)
        try:
            sortie.unlink()
        except OSError:
            pass
    return {
        "repetitions": len(resultats),
        "duree_analyse_s": _resume([x["duree_analyse_s"] for x in resultats]),
        "duree_json_s": _resume([x["duree_json_s"] for x in resultats]),
        "duree_totale_s": _resume([x["duree_totale_s"] for x in resultats]),
        "rss_kb": _resume([x["rss_kb"] for x in resultats]),
        "json_octets": resultats[0]["json_octets"],
        "etiquettes": resultats[0]["etiquettes"],
        "syntagmes": resultats[0]["syntagmes"],
        "unites_semantiques": resultats[0]["unites_semantiques"],
        "phrases": resultats[0]["phrases"],
        "mots": resultats[0]["mots"],
        "brut": resultats,
    }


def _run_cli(texte_path: pathlib.Path, repetitions: int, jsonl: bool = False,
             avec_tagger: bool = False, env: dict | None = None,
             timeout: float = 7200.0) -> dict:
    """Le CLI `drave.py analyser` sur un fichier, `--json` ou `--jsonl`."""
    resultats = []
    for _ in range(max(1, repetitions)):
        cmd = [sys.executable, str(RACINE / "tools" / "drave.py"), "analyser",
               "--fichier", str(texte_path)]
        cmd += ["--jsonl"] if jsonl else ["--json"]
        if avec_tagger:
            cmd.append("--tagger")
        r = _run(cmd, env=env, timeout=timeout)
        r["octets_stdout"] = len(r["stdout"])
        if jsonl:
            lignes = [ln for ln in r["stdout"].decode("utf-8", "replace").splitlines() if ln.strip()]
            r["lignes"] = len(lignes)
            annotations = []
            for ln in lignes:
                try:
                    annotations.append(json.loads(ln))
                except json.JSONDecodeError:
                    pass
            r["etiquettes"] = sum(len(a.get("etiquettes", [])) for a in annotations)
            r["refus"] = sum(1 for a in annotations if a.get("refus"))
            r["texte_octets"] = len(r["stdout"])  # compatibilité de nom
            r.pop("stdout", None)
        else:
            try:
                annotation = json.loads(r["stdout"].decode("utf-8"))
                r["etiquettes"] = len(annotation.get("etiquettes", []))
                r["unites_semantiques"] = len(annotation.get("unites_semantiques", []))
                r["refus"] = annotation.get("refus", "")
                r["schema"] = annotation.get("schema")
                r["version"] = annotation.get("version")
            except (json.JSONDecodeError, UnicodeDecodeError):
                r["etiquettes"] = None
            r.pop("stdout", None)
        resultats.append(r)
    premier = resultats[0]
    return {
        "repetitions": len(resultats),
        "duree_s": _resume([x["duree_s"] for x in resultats]),
        "rss_kb": _resume([x["rss_kb"] for x in resultats]),
        "octets": premier["octets_stdout"],
        "code": premier["code"],
        "stderr": premier["stderr"],
        "etiquettes": premier.get("etiquettes"),
        "unites_semantiques": premier.get("unites_semantiques"),
        "refus": premier.get("refus"),
        "lignes": premier.get("lignes"),
        "schema": premier.get("schema"),
        "version": premier.get("version"),
        "brut": resultats,
    }


def _run_100_cli(phrases: list[str]) -> dict:
    """100 appels CLI séparés — le coût fixe du produit, démarrage compris."""
    durees, rss, octets, codes = [], [], [], []
    for phrase in phrases:
        r = _run([sys.executable, str(RACINE / "tools" / "drave.py"), "analyser",
                  phrase, "--json"])
        durees.append(r["duree_s"])
        rss.append(r["rss_kb"])
        octets.append(len(r["stdout"]))
        codes.append(r["code"])
        del r["stdout"]
    return {
        "appels": len(phrases),
        "codes": sorted(set(codes)),
        "duree_totale_s": sum(durees),
        "duree_par_appel_s": _resume(durees),
        "rss_kb": _resume(rss),
        "octets_par_appel": _resume(octets),
        "octets_total": sum(octets),
        "durees_s": durees,
        "mots": sum(_compter_mots(p) for p in phrases),
    }


def _run_100_fonction(phrases: list[str], repetitions: int = 3) -> dict:
    """100 appels `Heuristique.analyser` dans un processus, sans le démarrage du CLI."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as f:
        json.dump(phrases, f, ensure_ascii=False)
        chemin = pathlib.Path(f.name)
    try:
        totaux, par_appel, rss, octets = [], [], [], []
        for _ in range(max(1, repetitions)):
            r = _run([sys.executable, str(pathlib.Path(__file__).resolve()),
                      "--interne-phrases", "--fichier", str(chemin)])
            if r["code"] != 0:
                raise RuntimeError(f"interne-phrases : code {r['code']} — {r['stderr'][:300]}")
            d = json.loads(r["stdout"].decode("utf-8"))
            totaux.append(d["duree_totale_s"])
            par_appel.extend(d["durees_s"])
            rss.append(d["rss_kb"])
            octets.extend(d["octets"])
        mots = [_compter_mots(p) for p in phrases]
        # le coût fixe : l'ordonnée à l'origine de t = a + b·mots
        fit = _ols([float(m) for m in mots for _ in range(max(1, repetitions))],
                   par_appel) if len(par_appel) == len(mots) * max(1, repetitions) else None
        return {
            "appels": len(par_appel),
            "duree_totale_s": _resume(totaux),
            "duree_par_appel_s": _resume(par_appel),
            "durees_s": par_appel,
            "rss_kb": _resume(rss),
            "octets_par_appel": _resume(octets),
            "octets_total": sum(octets),
            "mots": sum(mots),
            "cout_fixe_s": fit["a"] if fit else None,
            "cout_par_mot_s": fit["b"] if fit else None,
            "ajustement_par_mot": fit,
        }
    finally:
        try:
            chemin.unlink()
        except OSError:
            pass


# --------------------------------------------------------------------------- helpers


def _helper_analyse(texte_path: pathlib.Path, sortie: pathlib.Path) -> int:
    texte = texte_path.read_text(encoding="utf-8", errors="replace")
    h = bl.Heuristique()
    h.analyser("Le chat dort.")  # compile les expressions régulières, hors mesure
    t0 = time.perf_counter()
    annotation = h.analyser(texte)
    duree_analyse = time.perf_counter() - t0
    t1 = time.perf_counter()
    contenu = json.dumps(annotation.json(), ensure_ascii=False, indent=1) + "\n"
    duree_json = time.perf_counter() - t1
    sortie.write_text(contenu, encoding="utf-8")
    print(json.dumps({
        "duree_analyse_s": duree_analyse,
        "duree_json_s": duree_json,
        "duree_totale_s": duree_analyse + duree_json,
        "rss_kb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "json_octets": len(contenu.encode("utf-8")),
        "etiquettes": len(annotation.etiquettes),
        "syntagmes": sum(1 for e in annotation.etiquettes if e.niveau == "syntagme"),
        "unites_semantiques": len(annotation.unites_semantiques),
        "phrases": sum(1 for e in annotation.etiquettes
                       if e.niveau == "phrase" and e.type == "type"),
        "mots": _compter_mots(texte),
    }, ensure_ascii=False))
    return 0


def _helper_phrases(chemin: pathlib.Path) -> int:
    phrases = json.loads(chemin.read_text(encoding="utf-8"))
    h = bl.Heuristique()
    h.analyser("Le chat dort.")  # compile les expressions régulières, hors mesure
    durees, octets = [], []
    for phrase in phrases:
        t0 = time.perf_counter()
        annotation = h.analyser(phrase)
        durees.append(time.perf_counter() - t0)
        octets.append(len(json.dumps(annotation.json(), ensure_ascii=False,
                                     indent=1).encode("utf-8")))
    print(json.dumps({
        "durees_s": durees,
        "octets": octets,
        "duree_totale_s": sum(durees),
        "rss_kb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "mots": [_compter_mots(p) for p in phrases],
    }, ensure_ascii=False))
    return 0


# --------------------------------------------------------------------------- tagger


def _lire_stats_tagger(stderr: str) -> dict:
    """La dernière ligne `TAGGER API` du CLI : appels, réseau, cache, tokens, latence."""
    motif = ("appels=", "réseau=", "cache=", "tokens=", "latence=")
    for ligne in reversed(stderr.splitlines()):
        if all(m in ligne for m in motif):
            def _val(cle: str, apres: str) -> str:
                i = ligne.find(cle)
                return ligne[i + len(cle):].split(apres, 1)[0].strip()
            try:
                return {
                    "modele": ligne.split("modèle=", 1)[1].split(" ", 1)[0] if "modèle=" in ligne else "",
                    "appels": int(_val("appels=", " ")),
                    "reseau": int(_val("réseau=", " ")),
                    "cache": int(_val("cache=", " ")),
                    "tokens": int(_val("tokens=", " ")),
                    "latence_s": float(_val("latence=", " s")),
                }
            except (ValueError, IndexError):
                return {}
    return {}


def _extrapoler_10k(tagger: dict, corpus: dict) -> None:
    """Estimation du tagger sur le texte complet, à partir du lot mesuré.

    Le tagger fait **un appel par phrase**. On extrapole le nombre d'appels, le temps et
    les tokens depuis le lot mesuré ; les tokens sont corrigés du rapport de longueur
    moyenne des phrases (le lot de 100 phrases courtes est plus court que le texte).
    C'est une **estimation**, pas une mesure : le champ `mesure` le dit.
    """
    t = (tagger or {}).get("cent_courtes") or {}
    stats = t.get("stats") or {}
    phrases_mesurees = max(1, int(t.get("phrases") or 0))
    if not t or not stats or not corpus.get("phrases"):
        return
    phrases_10k = int(corpus["phrases"])
    mots_10k = int(corpus["mots"])
    mots_lot = int(corpus.get("phrases_courtes", {}).get("mots") or 0)
    phrases_lot = max(1, phrases_mesurees)
    longueur_10k = mots_10k / max(1, phrases_10k)
    longueur_lot = mots_lot / phrases_lot
    ratio_longueur = longueur_10k / longueur_lot if longueur_lot else 1.0
    ratio = phrases_10k / phrases_mesurees
    t["extrapolation_10k"] = {
        "mesure": False,
        "phrases": phrases_10k,
        "phrases_mesurees": phrases_mesurees,
        "appels_estimes": int(round(stats.get("appels", 0) * ratio)),
        "requetes_estimees": int(round(stats.get("reseau", 0) * ratio)),
        "tokens_estimes": int(round(stats.get("tokens", 0) * ratio * ratio_longueur)),
        "duree_estimee_s": t.get("duree_s", 0.0) * ratio,
        "reseau_estime_s": stats.get("latence_s", 0.0) * ratio,
        "rapport_longueur": ratio_longueur,
    }


def _run_tagger(texte_path: pathlib.Path, timeout: float = 7200.0) -> dict:
    """`--tagger --jsonl` avec un cache **froid** : le coût réseau réel."""
    cache = tempfile.mkdtemp(prefix="banc-deepseek-")
    env = dict(os.environ)
    env["DEEPSEEK_CACHE"] = cache
    try:
        r = _run([sys.executable, str(RACINE / "tools" / "drave.py"), "analyser",
                  "--fichier", str(texte_path), "--jsonl", "--tagger"],
                 env=env, timeout=timeout)
        lignes = [ln for ln in r["stdout"].decode("utf-8", "replace").splitlines() if ln.strip()]
        annotations = []
        for ln in lignes:
            try:
                annotations.append(json.loads(ln))
            except json.JSONDecodeError:
                pass
        stats = _lire_stats_tagger(r["stderr"])
        return {
            "code": r["code"],
            "duree_s": r["duree_s"],
            "rss_kb": r["rss_kb"],
            "octets_jsonl": len(r["stdout"]),
            "lignes": len(lignes),
            "phrases": len(annotations),
            "etiquettes": sum(len(a.get("etiquettes", [])) for a in annotations),
            "refus": sum(1 for a in annotations if a.get("refus")),
            "stats": stats,
            "stderr": r["stderr"],
            "disponible": r["code"] == 0 and bool(stats),
            "cache_froid": True,
        }
    finally:
        shutil.rmtree(cache, ignore_errors=True)


# --------------------------------------------------------------------------- contrôle


def _boucle_lineaire(n: int) -> int:
    x = 0
    for i in range(n * 200):
        x += i
    return x


def _boucle_quadratique(n: int) -> int:
    x = 0
    for i in range(n):
        for j in range(n):
            x += 1
    return x


def _controle_instrument(tailles: list[int], repetitions: int = 2) -> dict:
    """Le contrôle de l'instrument : la pente log-log retrouve 1 et 2."""
    resultat = {}
    for nom, fonction, reps in (("lineaire", _boucle_lineaire, repetitions),
                                ("quadratique", _boucle_quadratique, max(1, repetitions))):
        mesures = []
        for n in tailles:
            ds = []
            for _ in range(reps):
                t0 = time.perf_counter()
                fonction(n)
                ds.append(time.perf_counter() - t0)
            mesures.append({"n": n, "duree_s": _mediane(ds), "repetitions": reps})
        xs = [m["n"] for m in mesures]
        ys = [m["duree_s"] for m in mesures]
        resultat[nom] = {
            "mesures": mesures,
            "loglog": _loglog(xs, ys),
            "lineaire": _ols([float(x) for x in xs], ys),
            "quadratique": _quadratique([float(x) for x in xs], ys),
        }
        resultat[nom]["pente_attendue"] = 1.0 if nom == "lineaire" else 2.0
    return resultat


def _ajustements(mesures: list[dict]) -> dict:
    """Linéaire, quadratique, log-log et rapports de doublement sur les points mesurés."""
    xs = [float(m["mots"]) for m in mesures]
    ys = [float(m["duree_s"]) for m in mesures]
    points = sorted(zip(xs, ys))
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    doubles = []
    for i in range(1, len(points)):
        n0, t0 = points[i - 1]
        n1, t1 = points[i]
        if n0 > 0 and t0 > 0 and 1.9 <= (n1 / n0) <= 2.1:
            doubles.append({"de": n0, "a": n1, "rapport": t1 / t0,
                            "attendu_lineaire": 2.0, "attendu_quadratique": 4.0})
    return {
        "lineaire": _ols(xs, ys),
        "quadratique": _quadratique(xs, ys),
        "loglog": _loglog(xs, ys),
        "doublements": doubles,
    }


def _profil(chemin: pathlib.Path, sortie: pathlib.Path) -> int:
    """cProfile sur `Heuristique.analyser` : les fonctions qui portent le temps."""
    import cProfile
    import pstats

    if not chemin.is_absolute():
        chemin = RACINE / chemin
    texte = chemin.read_text(encoding="utf-8", errors="replace")
    h = bl.Heuristique()
    h.analyser("Le chat dort.")
    pr = cProfile.Profile()
    t0 = time.perf_counter()
    pr.enable()
    annotation = h.analyser(texte)
    pr.disable()
    duree = time.perf_counter() - t0
    stats = pstats.Stats(pr)
    stats.sort_stats("cumulative")
    fonctions = []
    for (fichier, ligne, nom), (cc, nc, tt, ct, _callers) in stats.stats.items():
        fonctions.append({"fonction": nom, "fichier": pathlib.Path(fichier).name,
                          "ligne": ligne, "appels": nc,
                          "temps_propre_s": round(tt, 3),
                          "temps_cumule_s": round(ct, 3)})
    fonctions.sort(key=lambda x: x["temps_cumule_s"], reverse=True)
    rapport = {
        "schema": "drave.performance.profil",
        "version": 1,
        "date": time.strftime("%Y-%m-%d"),
        "fichier": str(chemin.relative_to(RACINE)) if chemin.is_relative_to(RACINE) else str(chemin),
        "mots": _compter_mots(texte),
        "duree_s": duree,
        "etiquettes": len(annotation.etiquettes),
        "syntagmes": sum(1 for e in annotation.etiquettes if e.niveau == "syntagme"),
        "top": fonctions[:20],
    }
    sortie = pathlib.Path(sortie)
    if not sortie.is_absolute():
        sortie = RACINE / sortie
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for f in fonctions[:12]:
        print(f"{f['temps_cumule_s']:8.3f} s  {f['appels']:>8}  {f['fichier']}:{f['ligne']}  "
              f"{f['fonction']}")
    print(f"profil → {sortie}  ({duree:.1f} s, {rapport['mots']} mots, "
          f"{rapport['syntagmes']} syntagmes)")
    return 0


# --------------------------------------------------------------------------- environnement


def _environnement() -> dict:
    def _cpu() -> str:
        try:
            for ligne in pathlib.Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines():
                if ligne.startswith("model name"):
                    return ligne.split(":", 1)[1].strip()
        except OSError:
            pass
        return platform.processor() or "inconnu"

    try:
        mem_kb = int(pathlib.Path("/proc/meminfo").read_text(encoding="utf-8")
                     .split("MemTotal:", 1)[1].split()[0])
    except (OSError, IndexError, ValueError):
        mem_kb = None
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(RACINE),
                                capture_output=True, text=True, timeout=10).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        commit = ""
    return {
        "python": sys.version.split()[0],
        "implementation": platform.python_implementation(),
        "machine": platform.machine(),
        "systeme": platform.platform(),
        "cpu": _cpu(),
        "nproc": os.cpu_count(),
        "ram_kb": mem_kb,
        "git_commit": commit,
        "outil_memoire": f"{TIME_BIN} -f %M" if TIME_BIN else "resource",
        "pyhashseed": "0",
        "date": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }


# --------------------------------------------------------------------------- rapport markdown


def _fmt(x, nd=2):
    if x is None:
        return "—"
    if isinstance(x, float):
        return f"{x:.{nd}f}"
    return str(x)


def _markdown(rapport: dict) -> str:
    env = rapport["environnement"]
    corpus = rapport["corpus"]
    m10 = rapport["mesures"]["reel_10000"]
    mc = rapport["mesures"]["cent_courtes"]
    tag = rapport["mesures"].get("tagger", {})
    echelle = rapport["echelle"]
    lignes = [
        "# T4 — la performance de `drave analyser`",
        "",
        f"> **Ligne de roadmap** : B13 (produit) · **Tâche** : T4 (exploitable, 4/5) · "
        f"**Date** : {rapport['date']} · **Verdict** : "
        f"{rapport['verdict']['resume']}",
        "",
        "## 1. Le dispositif",
        "",
        f"- **Corpus** : `{corpus['source']}` — préfixe exact de "
        f"**{corpus['mots']:,} mots** "
        f"({corpus['caracteres']:,} caractères, {corpus['phrases']} phrases), "
        f"sha256 `{corpus['prefixe_sha256'][:16]}…`.",
        f"- **Machine** : {env['cpu']} · {env['nproc']} processeurs · "
        f"{env['ram_kb'] // (1024 * 1024) if env['ram_kb'] else '?'} Go · Python {env['python']}.",
        f"- **Mesure** : {TIME_BIN} -f %M pour le pic RSS ; "
        f"{rapport['parametres']['repetitions']} répétitions pour les mesures froides ; "
        f"médiane et intervalle.",
        "",
        "## 2. Les 10 000 mots",
        "",
        "| mesure | valeur |",
        "|---|---:|",
        f"| temps mural du CLI (`--json`) | **{_fmt(m10['cli']['duree_s']['mediane'], 3)} s** "
        f"({_fmt(m10['cli']['duree_s']['min'], 3)}–{_fmt(m10['cli']['duree_s']['max'], 3)}) |",
        f"| temps de la fonction seule | **{_fmt(m10['fonction']['duree_analyse_s']['mediane'], 3)} s** |",
        f"| sérialisation JSON | **{_fmt(m10['fonction']['duree_json_s']['mediane'], 3)} s** |",
        f"| débit (fonction) | **{_fmt(corpus['mots'] / m10['fonction']['duree_analyse_s']['mediane'], 0)} mots/s** |",
        f"| débit (CLI) | **{_fmt(corpus['mots'] / m10['cli']['duree_s']['mediane'], 0)} mots/s** |",
        f"| pic RSS | **{_fmt(m10['fonction']['rss_kb']['mediane'] / 1024, 1)} Mio** "
        f"(CLI {_fmt(m10['cli']['rss_kb']['mediane'] / 1024, 1)} Mio) |",
        f"| taille du JSON | **{m10['cli']['octets']:,} octets** ({_fmt(m10['cli']['octets'] / 1e6, 1)} Mo) |",
        f"| étiquettes | **{m10['cli']['etiquettes']:,}** |",
        f"| syntagmes | **{m10['fonction']['syntagmes']:,}** |",
        f"| JSONL compact (10 000 mots) | **{m10['jsonl']['octets']:,} octets** "
        f"({_fmt(m10['jsonl']['duree_s']['mediane'], 2)} s) |",
        "",
        "## 3. Les 100 phrases courtes",
        "",
        "| mesure | valeur |",
        "|---|---:|",
        f"| 100 appels CLI séparés | **{_fmt(mc['appels_cli']['duree_par_appel_s']['mediane'] * 1000, 1)} ms/appel** "
        f"({_fmt(mc['appels_cli']['duree_totale_s'], 2)} s pour 100) |",
        f"| 100 appels fonction | **{_fmt(mc['appels_fonction']['duree_par_appel_s']['mediane'] * 1000, 2)} ms/appel** "
        f"({_fmt(mc['appels_fonction']['duree_totale_s']['mediane'], 3)} s) |",
        f"| coût fixe (ordonnée) | **{_fmt((mc['appels_fonction']['cout_fixe_s'] or 0) * 1000, 2)} ms** "
        f"· pente **{_fmt((mc['appels_fonction']['cout_par_mot_s'] or 0) * 1000, 2)} ms/mot** |",
        f"| un appel `--jsonl` pour les 100 | **{_fmt(mc['lot_cli']['duree_s']['mediane'], 3)} s** "
        f"(soit {_fmt(mc['lot_cli']['duree_s']['mediane'] / 100 * 1000, 2)} ms/phrase) |",
        f"| JSON par phrase (moyenne) | **{_fmt(mc['appels_fonction']['octets_par_appel']['moyenne'], 0)} octets** |",
        f"| accélération du lot vs 100 CLI | **×{_fmt(mc['appels_cli']['duree_totale_s'] / max(1e-9, mc['lot_cli']['duree_s']['mediane']), 1)}** |",
        "",
        "## 4. `--tagger` — le coût réseau",
        "",
    ]
    if tag.get("cent_courtes"):
        t = tag["cent_courtes"]
        st = t.get("stats", {})
        tokens = st.get("tokens", 0)
        lignes += [
            "| mesure | valeur |",
            "|---|---:|",
            f"| 100 phrases (`--jsonl`) | **{_fmt(t['duree_s'], 1)} s** |",
            f"| appels / requêtes réseau | **{st.get('appels', '—')} / {st.get('reseau', '—')}** |",
            f"| tokens | **{tokens:,}** |",
            f"| latence réseau cumulée | **{_fmt(st.get('latence_s'), 1)} s** |",
            f"| temps par phrase | **{_fmt(t['duree_s'] / max(1, t['phrases']), 2)} s** |",
            f"| pic RSS | **{_fmt(t['rss_kb'] / 1024, 1)} Mio** |",
            "",
        ]
        if tag.get("dix_mille"):
            t10 = tag["dix_mille"]
            st10 = t10.get("stats", {})
            lignes += [
                "Sur les 10 000 mots (`--jsonl`, une requête par phrase) :",
                "",
                "| mesure | valeur |",
                "|---|---:|",
                f"| durée | **{_fmt(t10['duree_s'], 1)} s** |",
                f"| appels / requêtes | **{st10.get('appels', '—')} / {st10.get('reseau', '—')}** |",
                f"| tokens | **{st10.get('tokens', 0):,}** |",
                f"| latence réseau | **{_fmt(st10.get('latence_s'), 1)} s** |",
                f"| phrases / étiquettes | **{t10.get('phrases', '—')} / {t10.get('etiquettes', '—'):,}** |",
                f"| JSONL | **{t10.get('octets_jsonl', 0):,} octets** |",
                "",
            ]
    else:
        lignes += ["Le tagger n'a pas été mesuré (option `--avec-tagger` absente ou clé indisponible).", ""]
    lignes += [
        "## 5. Le contrôle négatif de linéarité",
        "",
        "Le bloc de phrases entières est répété ; chaque point a la même distribution de "
        "texte, seule la taille change.",
        "",
        "| mots | temps (s) | mots/s | rapport au précédent |",
        "|---:|---:|---:|---:|",
    ]
    for m in echelle["bloc_repete"]["mesures"]:
        lignes.append(f"| {m['mots']} | {_fmt(m['duree_s'], 3)} | "
                      f"{_fmt(m['mots'] / m['duree_s'], 0)} | {_fmt(m.get('rapport'), 2)} |")
    a = echelle["bloc_repete"]["ajustements"]
    lignes += [
        "",
        f"- pente log-log **α = {_fmt(a['loglog']['alpha'], 2)}** "
        f"(R² {_fmt(a['loglog']['r2'], 3)}) — 1 = linéaire, 2 = quadratique ;",
        f"- linéaire : R² {_fmt(a['lineaire']['r2'], 3)}, RMSE {_fmt(a['lineaire']['rmse'], 3)} s ;",
        f"- quadratique : R² {_fmt(a['quadratique']['r2'], 3)}, "
        f"c = {a['quadratique']['c']:.3e} s/mot², RMSE {_fmt(a['quadratique']['rmse'], 3)} s ;",
        f"- contrôle de l'instrument : boucle linéaire α = "
        f"**{_fmt(echelle['instrument']['lineaire']['loglog']['alpha'], 2)}**, "
        f"boucle quadratique α = **{_fmt(echelle['instrument']['quadratique']['loglog']['alpha'], 2)}**.",
        "",
        f"**Verdict** : {'✅ le contrôle passe' if rapport['verdict']['controle_lineaire'] else '❌ le contrôle **échoue**'} — "
        f"α = {_fmt(a['loglog']['alpha'], 2)} sur le bloc répété, "
        f"le terme quadratique ajoute {a['quadratique']['r2'] - a['lineaire']['r2']:+.3f} de R².",
        "",
        "## 6. Ce qui pourrait rendre ces chiffres faux",
        "",
        "- **Un seul texte** : le préfixe de 10 000 mots est un texte littéraire français "
        "(Alice) ; un texte technique, juridique ou multilingue peut changer la densité de "
        "syntagmes, donc le temps.",
        "- **Le bloc répété n'est pas le texte réel** : il mesure la croissance à densité "
        "constante. Le texte réel de 10 000 mots a une densité de syntagmes plus faible ; "
        "c'est pourquoi il est plus rapide que le bloc répété de même taille.",
        "- **Le cache réseau** : le tagger est mesuré avec `DEEPSEEK_CACHE` dans un "
        "répertoire temporaire froid ; un cache chaud divise le temps et les tokens par "
        "presque le nombre d'appels.",
        "- **La machine** : 40 cœurs partagés, pas d'épinglage CPU ; les mesures répétées "
        "donnent la dispersion, pas une garantie temps réel.",
        "- **Le JSON** : la taille est celle du JSON **indenté** du CLI (`indent=1`) ; le "
        "JSONL du tagger est compact, donc plus petit à contenu égal.",
        "",
        "## 7. Reproduire",
        "",
        "```bash",
        "python3 tools/banc_performance.py --avec-tagger --tagger-complet",
        "python3 tools/banc_performance.py --rapide          # sans réseau",
        "```",
        "",
        f"JSON brut : [`reports/performance.json`](performance.json).",
        "",
    ]
    return "\n".join(lignes)


# --------------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", default=SOURCE)
    ap.add_argument("--mots", type=int, default=MOTS)
    ap.add_argument("--phrases-courtes", type=int, default=PHRASES_COURTES)
    ap.add_argument("--repetitions", type=int, default=REPETITIONS)
    ap.add_argument("--tailles", default=",".join(str(x) for x in TAILLES))
    ap.add_argument("--bloc-repetitions", default="1,2,4,8,16,32,40")
    ap.add_argument("--sortie", default="reports/performance.json")
    ap.add_argument("--rapport", default="")
    ap.add_argument("--avec-tagger", action="store_true")
    ap.add_argument("--tagger-complet", action="store_true",
                    help="mesure aussi les 10 000 mots avec --tagger (coûteux)")
    ap.add_argument("--tagger-seulement", action="store_true",
                    help="ne refait que la partie --tagger et met à jour le JSON existant")
    ap.add_argument("--profil", default="",
                    help="profile un fichier avec cProfile et écrit les fonctions dominantes")
    ap.add_argument("--rapide", action="store_true",
                    help="petit passage hors ligne : 3 tailles, 1 répétition, sans tagger")
    ap.add_argument("--interne", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--interne-phrases", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--fichier", default="", help=argparse.SUPPRESS)
    ap.add_argument("--sortie-json", default="", help=argparse.SUPPRESS)
    args = ap.parse_args()

    # --- le mode profil : la cause, pas seulement le chiffre
    if args.profil:
        # ne jamais écraser le JSON de performance par un profil
        sortie_profil = args.sortie
        if sortie_profil == "reports/performance.json":
            sortie_profil = "reports/performance-profil.json"
        return _profil(pathlib.Path(args.profil), pathlib.Path(sortie_profil))

    # --- les deux modes helpers, appelés par le banc lui-même
    if args.interne:
        return _helper_analyse(pathlib.Path(args.fichier), pathlib.Path(args.sortie_json))
    if args.interne_phrases:
        return _helper_phrases(pathlib.Path(args.fichier))

    if args.rapide:
        args.repetitions = 1
        args.tailles = "250,1000,10000"
        args.avec_tagger = False
        args.tagger_complet = False
    tailles = [int(x) for x in args.tailles.split(",") if x.strip()]

    if args.tagger_seulement:
        sortie = pathlib.Path(args.sortie)
        if not sortie.is_absolute():
            sortie = RACINE / sortie
        if not sortie.is_file():
            print(f"banc : JSON introuvable pour --tagger-seulement : {sortie}", file=sys.stderr)
            return 2
        rapport = json.loads(sortie.read_text(encoding="utf-8"))
        work = RACINE / "work" / "banc-performance"
        lot = work / "phrases-courtes-lot.txt"
        complet = work / f"corpus-{rapport['corpus']['mots']}.txt"
        tagger = {"disponible": False, "raison": "--avec-tagger absent"}
        print("banc : tagger sur 100 phrases courtes (réseau froid)…", file=sys.stderr)
        t100 = _run_tagger(lot, timeout=7200.0)
        tagger["cent_courtes"] = t100
        if args.tagger_complet:
            print("banc : tagger sur le texte complet (réseau froid, long)…", file=sys.stderr)
            tagger["dix_mille"] = _run_tagger(complet, timeout=10800.0)
        tagger["disponible"] = bool(t100.get("disponible"))
        tagger["raison"] = ("mesuré (cache froid)" if tagger["disponible"]
                            else (t100.get("stderr", "")[:300]
                                  or "clé absente ou réseau indisponible"))
        _extrapoler_10k(tagger, rapport.get("corpus", {}))
        rapport["mesures"]["tagger"] = tagger
        rapport["commande"] = " ".join(sys.argv)
        rapport["parametres"]["avec_tagger"] = True
        rapport["parametres"]["tagger_complet"] = bool(args.tagger_complet)
        rapport["parametres"]["tagger_seulement"] = True
        rapport["date"] = time.strftime("%Y-%m-%d")
        # écriture intermédiaire : même si le run complet est interrompu, le lot de 100
        # phrases est déjà publié.
        sortie.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n",
                          encoding="utf-8")
        print(f"banc : JSON intermédiaire → {sortie}", file=sys.stderr)
        if args.rapport:
            chemin_rapport = pathlib.Path(args.rapport)
            if not chemin_rapport.is_absolute():
                chemin_rapport = RACINE / chemin_rapport
            chemin_rapport.parent.mkdir(parents=True, exist_ok=True)
            chemin_rapport.write_text(_markdown(rapport) + "\n", encoding="utf-8")
            print(f"banc : rapport → {chemin_rapport}", file=sys.stderr)
        print(json.dumps({"tagger_disponible": tagger["disponible"],
                          "cent_courtes_s": t100.get("duree_s"),
                          "cent_courtes_appels": t100.get("stats", {}).get("appels"),
                          "sortie": str(sortie)}, ensure_ascii=False, indent=1))
        return 0

    source = pathlib.Path(args.source)
    if not source.is_absolute():
        source = RACINE / source
    if not source.is_file():
        print(f"banc : source introuvable : {source}", file=sys.stderr)
        return 2
    texte_source = source.read_text(encoding="utf-8", errors="replace")
    texte, mots_reels = _prefixe_mots(texte_source, args.mots)
    if mots_reels != args.mots:
        print(f"banc : source trop courte : {mots_reels} mots au lieu de {args.mots}",
              file=sys.stderr)
    phrases = bl.Heuristique._phrases(texte)

    work = RACINE / "work" / "banc-performance"
    work.mkdir(parents=True, exist_ok=True)
    texte_path = work / f"corpus-{mots_reels}.txt"
    texte_path.write_text(texte, encoding="utf-8")

    courtes = _phrases_courtes(texte, args.phrases_courtes)
    if len(courtes) < args.phrases_courtes:
        print(f"banc : seulement {len(courtes)} phrases courtes", file=sys.stderr)
    courtes_path = work / "phrases-courtes.txt"
    courtes_path.write_text("\n".join(courtes) + "\n", encoding="utf-8")
    lot_path = work / "phrases-courtes-lot.txt"
    lot_path.write_text("\n\n".join(courtes) + "\n", encoding="utf-8")

    bloc, bloc_debut, bloc_fin = _bloc_phrases(texte, 250)
    bloc_path = work / "bloc-controle.txt"
    bloc_path.write_text(bloc, encoding="utf-8")
    bloc_mots = _compter_mots(bloc)

    print(f"banc : {mots_reels} mots, {len(phrases)} phrases, "
          f"{len(courtes)} phrases courtes, bloc {bloc_mots} mots", file=sys.stderr)

    # --- 10 000 mots
    print("banc : 10 000 mots (fonction + CLI)…", file=sys.stderr)
    m10_fonction = _run_analyse(texte_path, args.repetitions)
    m10_cli = _run_cli(texte_path, args.repetitions, jsonl=False)
    m10_jsonl = _run_cli(texte_path, 1, jsonl=True)

    # --- 100 phrases courtes
    print("banc : 100 phrases courtes (fonction + CLI)…", file=sys.stderr)
    mc_fonction = _run_100_fonction(courtes, repetitions=max(1, args.repetitions))
    mc_cli = _run_100_cli(courtes)
    mc_lot = _run_cli(lot_path, 1, jsonl=True)

    # --- tagger
    tagger: dict = {"disponible": False, "raison": "--avec-tagger absent"}
    if args.avec_tagger:
        print("banc : tagger sur 100 phrases courtes (réseau froid)…", file=sys.stderr)
        t100 = _run_tagger(lot_path, timeout=7200.0)
        tagger["cent_courtes"] = t100
        if args.tagger_complet:
            print("banc : tagger sur 10 000 mots (réseau froid, long)…", file=sys.stderr)
            t10 = _run_tagger(texte_path, timeout=10800.0)
            tagger["dix_mille"] = t10
        tagger["disponible"] = bool(tagger.get("cent_courtes", {}).get("disponible"))
        tagger["raison"] = ("mesuré (cache froid)" if tagger["disponible"]
                            else (tagger.get("cent_courtes", {}).get("stderr", "")[:300]
                                  or "clé absente ou réseau indisponible"))
        _extrapoler_10k(tagger, {
            "phrases": len(phrases), "mots": mots_reels,
            "phrases_courtes": {"n": len(courtes),
                                "mots": sum(_compter_mots(p) for p in courtes)},
        })

    # --- échelle : préfixes réels et bloc répété
    print("banc : échelle (préfixes réels)…", file=sys.stderr)
    mesures_prefixes = []
    for n in tailles:
        sous, n_reel = _prefixe_mots(texte, n)
        chemin = work / f"prefixe-{n_reel}.txt"
        chemin.write_text(sous, encoding="utf-8")
        r = _run_analyse(chemin, args.repetitions)
        mesures_prefixes.append({
            "mots": n_reel,
            "duree_s": r["duree_analyse_s"]["mediane"],
            "duree_min_s": r["duree_analyse_s"]["min"],
            "duree_max_s": r["duree_analyse_s"]["max"],
            "rss_kb": r["rss_kb"]["mediane"],
            "json_octets": r["json_octets"],
            "etiquettes": r["etiquettes"],
            "syntagmes": r["syntagmes"],
        })

    print("banc : échelle (bloc répété)…", file=sys.stderr)
    mesures_bloc = []
    for k in [int(x) for x in args.bloc_repetitions.split(",") if x.strip()]:
        texte_bloc = "\n\n".join([bloc] * k)
        n = _compter_mots(texte_bloc)
        chemin = work / f"bloc-x{k}.txt"
        chemin.write_text(texte_bloc, encoding="utf-8")
        r = _run_analyse(chemin, args.repetitions)
        # le nombre de syntagmes est la variable explicative réelle
        mesures_bloc.append({
            "mots": n,
            "duree_s": r["duree_analyse_s"]["mediane"],
            "duree_min_s": r["duree_analyse_s"]["min"],
            "duree_max_s": r["duree_analyse_s"]["max"],
            "rss_kb": r["rss_kb"]["mediane"],
            "json_octets": r["json_octets"],
            "etiquettes": r["etiquettes"],
            "syntagmes": r["syntagmes"],
        })
    for i, m in enumerate(mesures_bloc):
        m["rapport"] = (m["duree_s"] / mesures_bloc[i - 1]["duree_s"]
                        if i and mesures_bloc[i - 1]["duree_s"] else None)

    print("banc : contrôle de l'instrument…", file=sys.stderr)
    instrument = _controle_instrument(tailles, repetitions=2)

    a_bloc = _ajustements(mesures_bloc)
    a_prefixes = _ajustements(mesures_prefixes)
    # le modèle en nombre de syntagmes : t = a + b·k + c·k²
    synt = [float(m["syntagmes"]) for m in mesures_bloc if m.get("syntagmes")]
    temps = [float(m["duree_s"]) for m in mesures_bloc if m.get("syntagmes")]
    ajust_synt = {"lineaire": _ols(synt, temps), "quadratique": _quadratique(synt, temps),
                  "loglog": _loglog(synt, temps)}
    alpha_bloc = a_bloc["loglog"]["alpha"]
    # le contrôle passe si α est dans [0,85 ; 1,15] et si le terme quadratique n'explique
    # pas mieux que le linéaire (R² quadratique - R² linéaire < 0,02).
    lineaire_ok = 0.85 <= alpha_bloc <= 1.15
    quadratique_ok = (a_bloc["quadratique"]["r2"] - a_bloc["lineaire"]["r2"]) < 0.02
    controle_ok = bool(lineaire_ok and quadratique_ok)
    verdict = {
        "resume": ("10 000 mots exploitables ; contrôle de linéarité "
                   + ("**passe**" if controle_ok else "**échoue**")),
        "dix_mille_exploitable": m10_fonction["duree_analyse_s"]["mediane"] < 30.0,
        "debit_mots_s": mots_reels / m10_fonction["duree_analyse_s"]["mediane"],
        "controle_lineaire": controle_ok,
        "alpha_bloc_repete": alpha_bloc,
        "alpha_prefixes_reels": a_prefixes["loglog"]["alpha"],
        "raison": (f"α = {alpha_bloc:.2f} sur le bloc répété (1 = linéaire, 2 = quadratique) ; "
                   f"le terme quadratique ajoute "
                   f"{a_bloc['quadratique']['r2'] - a_bloc['lineaire']['r2']:+.3f} de R²."),
        "prochaine_action": ("profiler et borner `_groupes_partition` (O(k²) sur les syntagmes) "
                             "et `_cible_proche` (tri de tous les GV par segment) ; mesurer "
                             "k = syntagmes, pas seulement les mots."),
    }

    rapport = {
        "schema": "drave.performance",
        "version": 1,
        "date": time.strftime("%Y-%m-%d"),
        "tache": "T4 (exploitable, 4/5)",
        "commande": " ".join(sys.argv),
        "parametres": {
            "source": str(source.relative_to(RACINE)) if source.is_relative_to(RACINE) else str(source),
            "mots": mots_reels,
            "phrases_courtes": len(courtes),
            "repetitions": args.repetitions,
            "tailles": tailles,
            "avec_tagger": args.avec_tagger,
            "tagger_complet": args.tagger_complet,
        },
        "environnement": _environnement(),
        "corpus": {
            "source": str(source.relative_to(RACINE)) if source.is_relative_to(RACINE) else str(source),
            "source_sha256": _sha256(texte_source),
            "prefixe_sha256": _sha256(texte),
            "mots": mots_reels,
            "caracteres": len(texte),
            "phrases": len(phrases),
            "bloc_controle": {"mots": bloc_mots, "debut": bloc_debut, "fin": bloc_fin,
                              "sha256": _sha256(bloc)},
            "phrases_courtes": {
                "n": len(courtes),
                "mots": sum(_compter_mots(p) for p in courtes),
                "median_mots": statistics.median([_compter_mots(p) for p in courtes])
                if courtes else 0,
                "exemples": courtes[:5],
            },
        },
        "mesures": {
            "reel_10000": {"fonction": m10_fonction, "cli": m10_cli, "jsonl": m10_jsonl},
            "cent_courtes": {"appels_fonction": mc_fonction, "appels_cli": mc_cli,
                             "lot_cli": mc_lot},
            "tagger": tagger,
        },
        "echelle": {
            "prefixes_reels": {"mesures": mesures_prefixes, "ajustements": a_prefixes},
            "bloc_repete": {"mesures": mesures_bloc, "ajustements": a_bloc,
                            "ajustements_syntagmes": ajust_synt},
            "instrument": instrument,
        },
        "verdict": verdict,
    }

    sortie = pathlib.Path(args.sortie)
    if not sortie.is_absolute():
        sortie = RACINE / sortie
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"banc : JSON → {sortie}", file=sys.stderr)

    if args.rapport:
        chemin_rapport = pathlib.Path(args.rapport)
        if not chemin_rapport.is_absolute():
            chemin_rapport = RACINE / chemin_rapport
        chemin_rapport.parent.mkdir(parents=True, exist_ok=True)
        chemin_rapport.write_text(_markdown(rapport) + "\n", encoding="utf-8")
        print(f"banc : rapport → {chemin_rapport}", file=sys.stderr)

    print(json.dumps({
        "dix_mille_s": m10_fonction["duree_analyse_s"]["mediane"],
        "debit_mots_s": verdict["debit_mots_s"],
        "rss_mio": m10_fonction["rss_kb"]["mediane"] / 1024,
        "json_octets": m10_cli["octets"],
        "cent_ms": mc_fonction["duree_par_appel_s"]["mediane"] * 1000,
        "alpha_bloc": alpha_bloc,
        "controle_lineaire": controle_ok,
        "tagger_disponible": tagger.get("disponible", False),
        "sortie": str(sortie),
    }, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
