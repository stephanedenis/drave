#!/usr/bin/env python3
"""qualifier_neuronal.py — qualifie un tagger neuronal local sur le gold (180 phrases, 804 tokens).

Le tagger est `bloc_linguistique.NeuronalLLMPOS` : un modèle GGUF servi par `llama-server`, une
grammaire GBNF qui impose une classe par token, et les spans de la tokenisation du bloc. On
mesure trois lectures — **heuristique**, **neuronal seul**, **cascade** — et trois contrôles
négatifs (majoritaire, uniforme, permutation). Les seuils sont **pré-enregistrés** avant la
passe ; le JSON sort dans `reports/` et la fiche dans `reports/rapport-pensee-gold-neuronal.md`.

    python3 tools/tests/linguistique/qualifier_neuronal.py --demarrer --sortie reports/pensee-gold-neuronal.json

Le serveur est lancé sur CPU (`-ngl 0`) : les GPU de N2 restent intacts.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import pathlib
import random
import re
import statistics
import subprocess
import sys
import time
import urllib.request
from collections import Counter

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl  # noqa: E402

GOLD = pathlib.Path(__file__).with_name("gold.json")
SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")
FERME = {"DET", "PREP", "PRON", "CONJ", "AUX", "ADV", "NUM"}
CLASSES = ("DET", "NOUN", "VERB", "ADJ", "ADV", "PREP", "PRON", "AUX", "CONJ", "NUM", "INTJ", "PUNCT")


def charger() -> list[dict]:
    hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
    synth = json.loads(SYNTH.read_text(encoding="utf-8"))["phrases"]
    for p in hand:
        p["source"] = "hand"
    for p in synth:
        p["source"] = "synth"
    return hand + synth


def _pos(a: bl.Annotation) -> dict[tuple[int, int], str]:
    return {(e.debut, e.fin): e.type for e in a.etiquettes if e.niveau == "pos"}


def _score(annotations: dict[str, bl.Annotation], phrases: list[dict]) -> dict:
    ok = n = 0
    ok_ferme = n_ferme = ok_ouvert = n_ouvert = 0
    conf: dict[tuple[str, str], int] = {}
    par_classe: dict[str, dict[str, int]] = {}
    for p in phrases:
        pos = _pos(annotations[p["id"]])
        for m in p["mots"]:
            pred = pos.get((m["debut"], m["fin"]), "?")
            n += 1
            juste = pred == m["pos"]
            ok += int(juste)
            if m["pos"] in FERME:
                n_ferme += 1
                ok_ferme += int(juste)
            else:
                n_ouvert += 1
                ok_ouvert += int(juste)
            if not juste:
                conf[(m["pos"], pred)] = conf.get((m["pos"], pred), 0) + 1
            c = par_classe.setdefault(m["pos"], {"support": 0, "justes": 0})
            c["support"] += 1
            c["justes"] += int(juste)
    return {
        "tokens": n,
        "exactitude": round(ok / max(1, n), 4),
        "ferme": round(ok_ferme / max(1, n_ferme), 4),
        "ouvert": round(ok_ouvert / max(1, n_ouvert), 4),
        "classes": {k: {"support": v["support"], "justes": v["justes"],
                        "exactitude": round(v["justes"] / max(1, v["support"]), 4)}
                    for k, v in sorted(par_classe.items())},
        "confusions": [{"or": a, "predit": b, "n": c}
                       for (a, b), c in sorted(conf.items(), key=lambda kv: -kv[1])[:12]],
    }


def _sources(annotations: dict[str, bl.Annotation], phrases: list[dict]) -> dict:
    hand = [p for p in phrases if p["source"] == "hand"]
    synth = [p for p in phrases if p["source"] == "synth"]
    return {"all": _score(annotations, phrases), "hand": _score(annotations, hand),
            "synth": _score(annotations, synth)}


def _controles(phrases: list[dict]) -> dict:
    rng = random.Random(0)
    n = sum(len(p["mots"]) for p in phrases)
    majoritaire = sum(1 for p in phrases for m in p["mots"] if m["pos"] == "NOUN") / max(1, n)
    uniforme = 1.0 / len(CLASSES)
    return {
        "majoritaire": {"description": "toujours NOUN", "exactitude": round(majoritaire, 4)},
        "uniforme": {"description": "tirage uniforme sur les 12 classes", "exactitude": round(uniforme, 4)},
        "permutation": {"description": "les POS prédits sont permutés entre tokens (graine 0)",
                        "exactitude": None},
        "hasard": {"graine": 0, "tokens": n},
    }


def _permutation(annotations: dict[str, bl.Annotation], phrases: list[dict]) -> float:
    """Contrôle du **métrique** : on garde les POS prédits, on les permute, on re-mesure."""
    predits: list[str] = []
    gold: list[str] = []
    for p in phrases:
        pos = _pos(annotations[p["id"]])
        for m in p["mots"]:
            predits.append(pos.get((m["debut"], m["fin"]), "?"))
            gold.append(m["pos"])
    random.Random(0).shuffle(predits)
    return round(sum(a == b for a, b in zip(predits, gold)) / max(1, len(gold)), 4)


def _sha256(chemin: pathlib.Path) -> str:
    h = hashlib.sha256()
    with chemin.open("rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def _version() -> str:
    """`llama-server --version` écrit sur stderr ; on lit les deux flux."""
    for commande in (["llama-server", "--version"], ["llama-cli", "--version"]):
        r = subprocess.run(commande, capture_output=True, text=True)
        for ligne in (r.stdout + "\n" + r.stderr).splitlines():
            if ligne.strip():
                return ligne.strip()
    return "inconnue"


def _fichiers(modele: pathlib.Path) -> list[dict]:
    """Les shards du modèle : le premier ne suffit pas, llama.cpp charge les deux."""
    m = re.match(r"(.+)-\d{5}-of-(\d{5})\.gguf$", modele.name)
    if not m:
        return [{"nom": str(modele), "octets": modele.stat().st_size,
                 "sha256": _sha256(modele)}]
    prefixe, total = m.group(1), int(m.group(2))
    shards = sorted(modele.parent.glob(f"{prefixe}-*-of-{total:05d}.gguf"))
    return [{"nom": str(s), "octets": s.stat().st_size, "sha256": _sha256(s)} for s in shards]


def _sante(endpoint: str, timeout: float = 2.0) -> bool:
    try:
        with urllib.request.urlopen(endpoint.rstrip("/") + "/health", timeout=timeout) as r:
            return json.loads(r.read().decode()).get("status") == "ok"
    except Exception:
        return False


def demarrer_serveur(modele: pathlib.Path, port: int, log: pathlib.Path) -> subprocess.Popen:
    commande = ["llama-server", "-m", str(modele), "--host", "127.0.0.1", "--port", str(port),
                "-ngl", "0", "-c", "1024", "--no-webui"]
    print("serveur :", " ".join(commande))
    journal = log.open("w", encoding="utf-8")
    proc = subprocess.Popen(commande, stdout=journal, stderr=subprocess.STDOUT)
    for _ in range(120):
        if proc.poll() is not None:
            raise RuntimeError(f"le serveur est mort — voir {log}")
        if _sante(f"http://127.0.0.1:{port}"):
            return proc
        time.sleep(0.5)
    proc.terminate()
    raise RuntimeError(f"le serveur n'a pas répondu en 60 s — voir {log}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--modele", default=str(RACINE / "models/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf"))
    ap.add_argument("--endpoint", default="")
    ap.add_argument("--port", type=int, default=18082)
    ap.add_argument("--demarrer", action="store_true", help="lance llama-server sur CPU")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--confiance", type=float, default=0.6)
    ap.add_argument("--limite", type=int, default=0, help="ne mesurer que les N premières phrases (dev)")
    ap.add_argument("--sortie", default=str(RACINE / "reports/pensee-gold-neuronal.json"))
    args = ap.parse_args()

    phrases = charger()
    if args.limite:
        phrases = phrases[:args.limite]
    modele = pathlib.Path(args.modele)
    if not modele.exists():
        raise SystemExit(f"modèle absent : {modele}")
    endpoint = args.endpoint or f"http://127.0.0.1:{args.port}"
    proc = None
    if not _sante(endpoint):
        if not args.demarrer:
            raise SystemExit(f"serveur absent sur {endpoint} — relancer avec --demarrer")
        log = pathlib.Path("/tmp/qualifier-neuronal-serveur.log")
        proc = demarrer_serveur(modele, args.port, log)
    else:
        print(f"serveur existant utilisé : {endpoint}")

    tagger = bl.NeuronalLLMPOS(modele, endpoint=endpoint, confiance=args.confiance)
    t0 = time.perf_counter()
    annotations: dict[str, bl.Annotation] = {}
    latences: list[float] = []
    refus: list[str] = []
    try:
        with cf.ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
            def _un(p):
                a = tagger.analyser(p["texte"], p["langue"])
                return p["id"], a
            for pid, a in ex.map(_un, phrases):
                annotations[pid] = a
                latences.append(float(a.cout.get("duree_s", 0.0)))
                if a.refus:
                    refus.append(f"{pid}: {a.refus}")

        h = bl.Heuristique()
        h_annotations = {p["id"]: h.analyser(p["texte"], p["langue"]) for p in phrases}
        cascade = bl.Cascade(bl.Heuristique(), tagger, seuil=args.confiance)
        c_annotations = {p["id"]: cascade.analyser(p["texte"], p["langue"]) for p in phrases}
        duree = time.perf_counter() - t0

        mesures = {
            "heuristique": _sources(h_annotations, phrases),
            "neuronal": _sources(annotations, phrases),
            "cascade": _sources(c_annotations, phrases),
        }
        mesures["cascade"]["appels_neuronal"] = cascade.appels_neuronal
        mesures["cascade"]["seuil"] = args.confiance
        mesures["neuronal"]["appels_http"] = tagger.appels
        mesures["neuronal"]["refus"] = len(refus)
        mesures["neuronal"]["refus_detail"] = refus[:10]
        mesures["neuronal"]["latence_s"] = {
            "moyenne": round(statistics.fmean(latences), 3) if latences else 0.0,
            "mediane": round(statistics.median(latences), 3) if latences else 0.0,
            "p95": round(sorted(latences)[int(0.95 * (len(latences) - 1))], 3) if latences else 0.0,
        }
        controles = _controles(phrases)
        controles["permutation"]["exactitude"] = _permutation(annotations, phrases)

        seuils = {
            "neuronal_all": mesures["neuronal"]["all"]["exactitude"] >= 0.80,
            "cascade_all": mesures["cascade"]["all"]["exactitude"] >= 0.90,
            "cascade_synth": mesures["cascade"]["synth"]["exactitude"] >= 0.90,
            "cascade_hand_sans_regression": (mesures["cascade"]["hand"]["exactitude"]
                                             >= mesures["heuristique"]["hand"]["exactitude"]),
            "aucun_refus": len(refus) == 0,
            "controles_sous_0_40": max(v["exactitude"] for v in controles.values()
                                        if v.get("exactitude") is not None) < 0.40,
        }
        resultat = {
            "date": time.strftime("%Y-%m-%d %H:%M %Z"),
            "modele": {
                "nom": modele.name,
                "fichiers": _fichiers(modele),
                "quantisation": "Q4_K_M",
                "runtime": _version(),
                "gpu": 0,
            },
            "gold": {"phrases": len(phrases), "tokens": sum(len(p["mots"]) for p in phrases),
                     "hand": sum(1 for p in phrases if p["source"] == "hand"),
                     "synth": sum(1 for p in phrases if p["source"] == "synth")},
            "tagger": {"classe": "NeuronalLLMPOS", "confiance": args.confiance,
                       "tokenisation": "Heuristique._mots (mot/nombre)",
                       "contrainte": "grammaire GBNF, une classe par token"},
            "mesures": mesures,
            "controles": controles,
            "seuils": seuils,
            "verdict": all(seuils.values()),
            "duree_totale_s": round(duree, 1),
            "limites": [
                "POS seulement : le tagger ne rend ni syntagmes ni pragmatique.",
                "20 phrases réelles (hand) ont servi au choix du modèle et du prompt ; les 160 "
                "synthétiques sont le jeu de test.",
                "Le seuil 0,6 de la cascade vient du seuil ouvert de l'heuristique (0,55), pas "
                "d'un balayage sur le gold.",
                "CPU seulement (les GPU de N2 sont réservés) ; pas de mesure GPU.",
                "Le gold utilise la même tokenisation que le bloc (vérifié : 180/180).",
            ],
        }
    finally:
        if proc is not None:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()

    sortie = pathlib.Path(args.sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": resultat["verdict"], "seuils": seuils,
                      "heuristique": mesures["heuristique"]["all"]["exactitude"],
                      "neuronal": mesures["neuronal"]["all"]["exactitude"],
                      "cascade": mesures["cascade"]["all"]["exactitude"],
                      "cascade_synth": mesures["cascade"]["synth"]["exactitude"],
                      "cascade_hand": mesures["cascade"]["hand"]["exactitude"],
                      "refus": len(refus), "appels": tagger.appels,
                      "latence": mesures["neuronal"]["latence_s"]}, ensure_ascii=False, indent=1))
    print(f"écrit : {sortie}")
    return 0 if resultat["verdict"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
