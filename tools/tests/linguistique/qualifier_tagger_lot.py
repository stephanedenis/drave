#!/usr/bin/env python3
"""qualifier_tagger_lot.py — X3 : le tagger POS **en lot** sur 1 000 phrases réelles.

POURQUOI. W2/W3 ont mesuré la qualité et le coût **extrapolé** à 1 000 phrases. X3 mesure le
même câblage (`drave._cascade_tagger`, `NeuronalLLMPOS`, cache disque du client) sur un **lot
réel** de 1 000 items, avec le cache **froid** puis **chaud**, la mémoire, le débit et le
mode `--jsonl` du CLI. Le contrôle négatif est le cache chaud : les mêmes phrases, rejouées,
doivent coûter **0 réseau, 0 token, 0 dollar**.

LE CORPUS. 612 phrases du gold (hand 20 + reel 432 + synth 160) + les **50 textes libres** du
banc de robustesse (`reports/pensee-fiabilite-produit.json`, `banc_50.resultats`), segmentés en
phrases par `Heuristique._phrases`. Cela donne **681 lignes source** et **677 textes distincts**
(4 doublons, dont 3 du gold et « Le chat dort. » déjà dans le gold). Le lot de 1 000 items =
les 681 lignes source + **319 répétitions** déterministes (graine 20261115) : les 1 000 items
sont donc des phrases réelles, mais 323 rejouent un texte déjà vu dans le lot. La variante `--libres produit` utilise les 50 phrases
de l'audit produit (`pensee-produit-bloc-l.json`, 668 lignes / 665 textes). La mesure publie
séparément le lot (1 000 items) et l'extrapolation aux 1 000 phrases **uniques**.

TROIS PASSES.
1. `--mode froid` : cache disque neuf, lot complet, une seule cascade → 673 appels réseau,
   4 rejeux disque (prompts identiques) et 323 rejeux mémoire.
2. `--mode chaud` : même cache, lot complet, cascade neuve → 0 réseau, 677 rejeux disque,
   323 rejeux mémoire.
3. `--mode fusion` : combine les deux, calcule le coût, lance `--jsonl` (chaud sur 1 000,
   froid sur 20) et écrit le JSON de la fiche.

USAGE.
    python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode froid \
      --cache /tmp/tagger-lot-cache --sortie /tmp/tagger-lot-froid.json
    python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode chaud \
      --cache /tmp/tagger-lot-cache --sortie /tmp/tagger-lot-chaud.json
    python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode fusion \
      --froid /tmp/tagger-lot-froid.json --chaud /tmp/tagger-lot-chaud.json \
      --sortie reports/rapport-tagger-lot.json

La clé est lue par `drave._cle_tagger()` (DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key,
DEEPSEEK_API_KEY). Elle n'est jamais affichée, ni journalisée, ni écrite dans le JSON.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import os
import pathlib
import platform
import random
import re
import resource
import shutil
import statistics
import subprocess
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE))
sys.path.insert(0, str(RACINE / "tools"))
sys.path.insert(0, str(RACINE / "tools" / "tests" / "linguistique"))

import bloc_linguistique as bl  # noqa: E402
import drave  # noqa: E402
from tools.llm.deepseek import DeepSeek  # noqa: E402

GOLD = RACINE / "tools" / "tests" / "linguistique" / "gold.json"
REEL = RACINE / "tools" / "tests" / "linguistique" / "gold_reel.json"
SYNTH = RACINE / "tools" / "tests" / "linguistique" / "gold_synthetique.json"
LIBRES = {
    "fiabilite": RACINE / "reports" / "pensee-fiabilite-produit.json",
    "produit": RACINE / "reports" / "pensee-produit-bloc-l.json",
}
GRAINE = 20261115
N_LOT = 1000

# Tarif public deepseek-flash au 2026-11-13, $ par million de tokens.
# Source : reports/rapport-coordination-r.md § 3.3 (api-docs.deepseek.com/quick_start/pricing).
PRIX = {
    "hors_pointe": {"entree_hit": 0.003, "entree_miss": 0.15, "sortie": 0.60},
    "pointe": {"entree_hit": 0.006, "entree_miss": 0.30, "sortie": 1.20},
}


# --------------------------------------------------------------------------- corpus


def charger_corpus(libres: str = "fiabilite") -> list[dict]:
    """Les lignes source : 612 gold + les phrases des 50 textes libres.

    `fiabilite` (défaut) : les 50 textes du banc de robustesse
    (`pensee-fiabilite-produit.json`, 69 phrases). `produit` : les 50 phrases de l'audit
    produit (`pensee-produit-bloc-l.json`, 56 phrases) — variante de contrôle.
    """
    items: list[dict] = []
    for chemin, source in ((GOLD, "hand"), (REEL, "reel"), (SYNTH, "synth")):
        for p in json.loads(chemin.read_text(encoding="utf-8"))["phrases"]:
            items.append({
                "id": p["id"], "texte": p["texte"], "langue": p.get("langue") or "fr",
                "source": source, "origine": chemin.name,
            })
    h = bl.Heuristique()
    if libres not in LIBRES:
        raise SystemExit(f"banc libre inconnu : {libres}")
    chemin = LIBRES[libres]
    d = json.loads(chemin.read_text(encoding="utf-8"))
    banc = d["banc_50"]["resultats" if libres == "fiabilite" else "detail"]
    for x in banc:
        texte = x.get("texte") or ""
        langue = x.get("langue") or ("und" if libres == "fiabilite" else "fr")
        for k, (debut, fin, _typ, _) in enumerate(h._phrases(texte)):
            phrase = texte[debut:fin].strip()
            if not phrase:
                continue
            items.append({
                "id": f"{x['id']}-{k:02d}", "texte": phrase, "langue": langue,
                "source": "libre", "origine": chemin.name,
            })
    return items


def construire_lot(items: list[dict], n: int = N_LOT, graine: int = GRAINE) -> tuple[list[dict], dict]:
    """Le lot de `n` items : les source puis des répétitions déterministes."""
    if n < len(items):
        raise SystemExit(f"n={n} < source={len(items)} : réduire la source d'abord")
    rng = random.Random(graine)
    lot = [{**it, "rang": i, "repete": False} for i, it in enumerate(items)]
    repetitions = n - len(items)
    for j in range(repetitions):
        it = rng.choice(items)
        lot.append({**it, "rang": len(items) + j, "repete": True})
    uniques = {(it["texte"], it["langue"]) for it in items}
    prompts = {tuple(t for _, _, t in bl.NeuronalLLMPOS._tokens(it["texte"]))
               for it in items}
    doublons = []
    vus = set()
    for it in items:
        cle = (it["texte"], it["langue"])
        if cle in vus:
            doublons.append(it["id"])
        vus.add(cle)
    composition = {
        "lignes_source": len(items),
        "textes_distincts": len(uniques),
        "prompts_distincts": len(prompts),
        "collisions_prompt": len(uniques) - len(prompts),
        "doublons_source": {"n": len(doublons), "ids": doublons},
        "items": len(lot),
        "repetitions_ajoutees": repetitions,
        "items_repetes": sum(1 for it in lot if it["repete"]),
        "graine": graine,
        "sha256_textes": hashlib.sha256(
            "\n".join(it["texte"] for it in items).encode("utf-8")).hexdigest(),
        "par_source": dict(collections.Counter(it["source"] for it in items)),
        "par_langue": dict(collections.Counter(it["langue"] for it in items)),
    }
    return lot, composition


# --------------------------------------------------------------------------- cache / mémoire


def meta_cache(chemin: pathlib.Path) -> dict:
    if not chemin.is_dir():
        return {"fichiers": 0, "octets": 0, "dates": {}, "modeles": {}}
    fichiers = sorted(chemin.glob("*.json"))
    dates, modeles, octets = [], collections.Counter(), 0
    for f in fichiers:
        try:
            octets += f.stat().st_size
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if d.get("recu_le"):
            dates.append(d["recu_le"])
        if d.get("modele"):
            modeles[d["modele"]] += 1
    return {"fichiers": len(fichiers), "octets": octets,
            "dates": {"min": min(dates) if dates else None,
                      "max": max(dates) if dates else None},
            "modeles": dict(modeles)}


def _rss_kb() -> dict:
    """VmRSS (courant) et VmHWM (pic) de ce processus, en kio."""
    valeurs = {}
    try:
        for ligne in pathlib.Path("/proc/self/status").read_text().splitlines():
            if ligne.startswith("VmRSS:"):
                valeurs["rss_kb"] = int(ligne.split()[1])
            if ligne.startswith("VmHWM:"):
                valeurs["pic_kb"] = int(ligne.split()[1])
    except OSError:
        pass
    valeurs["ru_maxrss_kb"] = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return valeurs


# --------------------------------------------------------------------------- transport mesuré


class TransportMesure:
    """Le transport du tagger, avec un enregistrement par appel réellement fait."""

    def __init__(self, client: DeepSeek) -> None:
        self.client = client
        self.calls: list[dict] = []
        self.dernier: dict | None = None

    def __call__(self, invite: str, _grammaire: str, max_jetons: int) -> str:
        t0 = time.perf_counter()
        try:
            r = self.client.demande(invite, temperature=0.0,
                                    max_tokens=max(64, int(max_jetons or 256)))
        except Exception as exc:  # noqa: BLE001 — le tagger décide du repli
            self.dernier = {"cache": False, "erreur": f"{type(exc).__name__}: {exc}",
                            "latence_api_s": round(time.perf_counter() - t0, 3),
                            "latence_wall_s": round(time.perf_counter() - t0, 3),
                            "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0,
                            "cache_hit_tokens": 0, "cache_miss_tokens": 0,
                            "modele": ""}
            self.calls.append(self.dernier)
            raise
        dt = time.perf_counter() - t0
        usage = r.usage if isinstance(r.usage, dict) else {}
        rec = {
            "cache": bool(r.cache), "modele": r.modele or "",
            "latence_api_s": float(r.latence_s or 0.0),
            "latence_wall_s": round(dt, 4),
            "prompt_tokens": int(usage.get("prompt_tokens", 0) or 0),
            "completion_tokens": int(usage.get("completion_tokens", 0) or 0),
            "total_tokens": int(usage.get("total_tokens", 0) or 0),
            "cache_hit_tokens": int(usage.get("prompt_cache_hit_tokens", 0) or 0),
            "cache_miss_tokens": int(usage.get("prompt_cache_miss_tokens", 0) or 0),
        }
        self.calls.append(rec)
        self.dernier = rec
        return r.contenu


def _stats() -> dict:
    return {"appels": 0, "requetes": 0, "cache": 0, "tokens": 0, "latence_s": 0.0,
            "modeles": {}, "cle_refusee": 0}


# --------------------------------------------------------------------------- une passe


def mesurer_passe(nom: str, lot: list[dict], cache_dir: pathlib.Path,
                  partition: str = "alternative") -> dict:
    """Une passe complète : une cascade, un cache disque, un enregistrement par item."""
    cache_dir = cache_dir.resolve()
    avant_cache = meta_cache(cache_dir)
    avant_rss = _rss_kb()
    stats = _stats()
    client = DeepSeek(cle=drave._cle_tagger(), cache_dir=cache_dir)
    transport = TransportMesure(client)
    cascade = drave._cascade_tagger(transport, partition=partition, stats=stats)
    lignes: list[dict] = []
    vus: set[tuple[str, str]] = set()
    t_debut = time.perf_counter()
    try:
        for it in lot:
            cle = (it["texte"], it["langue"])
            deja_vu = cle in vus
            avant_appels = len(transport.calls)
            t0 = time.perf_counter()
            erreur = ""
            annotation = None
            try:
                annotation = cascade.analyser(it["texte"], it["langue"])
            except drave.CleTaggerRefusee:
                raise
            except Exception as exc:  # noqa: BLE001
                erreur = f"{type(exc).__name__}: {exc}"
            duree_item = time.perf_counter() - t0
            appel = len(transport.calls) > avant_appels
            rec = transport.dernier if appel else None
            cache_disque = bool(rec and rec.get("cache"))
            tokens_reseau = rec["total_tokens"] if (appel and not cache_disque) else 0
            tokens_cache = rec["total_tokens"] if (appel and cache_disque) else 0
            lignes.append({
                "rang": it["rang"], "id": it["id"], "source": it["source"],
                "langue": it["langue"], "repete": bool(it["repete"]),
                "appel_transport": appel, "cache_disque": cache_disque,
                "cache_memoire": (not appel) and deja_vu,
                "refus_sans_appel": (not appel) and (not deja_vu),
                "deja_vu": deja_vu,
                "tokens_reseau": tokens_reseau, "tokens_cache": tokens_cache,
                "prompt_tokens": rec["prompt_tokens"] if (appel and not cache_disque) else 0,
                "completion_tokens": rec["completion_tokens"] if (appel and not cache_disque) else 0,
                "cache_hit_tokens": rec["cache_hit_tokens"] if (appel and not cache_disque) else 0,
                "cache_miss_tokens": rec["cache_miss_tokens"] if (appel and not cache_disque) else 0,
                "latence_api_s": rec["latence_api_s"] if appel else 0.0,
                "latence_item_s": round(duree_item, 4),
                "refus": bool(annotation and annotation.refus),
                "refus_message": (annotation.refus if annotation else erreur)[:160],
                "erreur": erreur,
                "hash": (hashlib.sha256(json.dumps(
                    annotation.json(), ensure_ascii=False, sort_keys=True,
                    separators=(",", ":")).encode("utf-8")).hexdigest()[:16]
                    if annotation is not None else ""),
            })
            vus.add(cle)
    finally:
        duree = time.perf_counter() - t_debut
    apres_cache = meta_cache(cache_dir)
    apres_rss = _rss_kb()
    return {
        "nom": nom, "cache_dir": str(cache_dir), "duree_s": round(duree, 3),
        "cache_avant": avant_cache, "cache_apres": apres_cache,
        "rss_avant": avant_rss, "rss_apres": apres_rss,
        "stats_tagger": {"appels": stats["appels"], "requetes": stats["requetes"],
                         "cache": stats["cache"], "tokens": stats["tokens"],
                         "latence_s": round(stats["latence_s"], 3),
                         "modeles": dict(stats["modeles"]),
                         "cle_refusee": stats["cle_refusee"]},
        "lignes": lignes,
    }


# --------------------------------------------------------------------------- agrégats


def _p95(valeurs: list[float]) -> float:
    if not valeurs:
        return 0.0
    v = sorted(valeurs)
    return round(v[min(len(v) - 1, max(0, math.ceil(0.95 * len(v)) - 1))], 3)


def _resume_latence(valeurs: list[float]) -> dict:
    return {
        "moyenne": round(statistics.fmean(valeurs), 3) if valeurs else 0.0,
        "mediane": round(statistics.median(valeurs), 3) if valeurs else 0.0,
        "p95": _p95(valeurs),
        "max": round(max(valeurs), 3) if valeurs else 0.0,
    }


def agreger(passe: dict, composition: dict) -> dict:
    """Les comptes d'une passe, sans les 1 000 lignes."""
    lignes = passe["lignes"]
    reseau = [l for l in lignes if l["appel_transport"] and not l["cache_disque"]]
    disque = [l for l in lignes if l["cache_disque"]]
    memoire = [l for l in lignes if l.get("cache_memoire")]
    sans_transport = [l for l in lignes if not l["appel_transport"]]
    refus_sans_appel = [l for l in lignes if l.get("refus_sans_appel")]
    duree = max(1e-9, passe["duree_s"])
    n = len(lignes)
    tokens_reseau = sum(l["tokens_reseau"] for l in lignes)
    tokens_cache = sum(l["tokens_cache"] for l in lignes)
    prompt = sum(l["prompt_tokens"] for l in reseau)
    completion = sum(l["completion_tokens"] for l in reseau)
    hit = sum(l["cache_hit_tokens"] for l in reseau)
    miss = sum(l["cache_miss_tokens"] for l in reseau)
    lat_reseau = [l["latence_api_s"] for l in reseau]
    lat_items = [l["latence_item_s"] for l in lignes]
    par_source: dict[str, dict] = {}
    for source in sorted({l["source"] for l in lignes}):
        sous = [l for l in lignes if l["source"] == source]
        par_source[source] = {
            "items": len(sous),
            "requetes": sum(1 for l in sous if l["appel_transport"] and not l["cache_disque"]),
            "cache_disque": sum(1 for l in sous if l["cache_disque"]),
            "cache_memoire": sum(1 for l in sous if l.get("cache_memoire")),
            "tokens_reseau": sum(l["tokens_reseau"] for l in sous),
            "latence_reseau_s": round(sum(l["latence_api_s"] for l in sous
                                                   if l["appel_transport"] and not l["cache_disque"]), 3),
            "duree_item_s": round(sum(l["latence_item_s"] for l in sous), 3),
        }
    par_langue: dict[str, dict] = {}
    for langue in sorted({l["langue"] for l in lignes}):
        sous = [l for l in lignes if l["langue"] == langue]
        par_langue[langue] = {
            "items": len(sous),
            "requetes": sum(1 for l in sous if l["appel_transport"] and not l["cache_disque"]),
            "cache_disque": sum(1 for l in sous if l["cache_disque"]),
            "cache_memoire": sum(1 for l in sous if l.get("cache_memoire")),
            "tokens_reseau": sum(l["tokens_reseau"] for l in sous),
            "latence_reseau_s": round(sum(l["latence_api_s"] for l in sous
                                                   if l["appel_transport"] and not l["cache_disque"]), 3),
            "duree_item_s": round(sum(l["latence_item_s"] for l in sous), 3),
        }
    return {
        "nom": passe["nom"], "items": n, "composition": composition,
        "cache_dir": passe["cache_dir"], "duree_s": passe["duree_s"],
        "debit": {
            "items_par_min": round(n / (duree / 60.0), 1),
            "requetes_par_min": round(len(reseau) / (duree / 60.0), 1),
            "secondes_par_item": round(duree / n, 4),
            "secondes_par_requete": round(duree / max(1, len(reseau)), 4),
        },
        "cache": {
            "appels_transport": len(reseau) + len(disque),
            "requetes_reseau": len(reseau),
            "cache_disque": len(disque),
            "cache_memoire": len(memoire),
            "items_sans_transport": len(sans_transport),
            "refus_sans_appel": len(refus_sans_appel),
            "taux_cache_disque": round(len(disque) / n, 4),
            "taux_cache_memoire": round(len(memoire) / n, 4),
            "taux_cache_total": round((len(disque) + len(memoire)) / n, 4),
            "fichiers_avant": passe["cache_avant"]["fichiers"],
            "fichiers_apres": passe["cache_apres"]["fichiers"],
            "octets_apres": passe["cache_apres"]["octets"],
            "dates_apres": passe["cache_apres"]["dates"],
            "modeles_cache": passe["cache_apres"]["modeles"],
        },
        "api": {
            "prompt_tokens": prompt, "completion_tokens": completion,
            "total_tokens": prompt + completion,
            "prompt_cache_hit_tokens": hit, "prompt_cache_miss_tokens": miss,
            "tokens_reseau": tokens_reseau, "tokens_cache": tokens_cache,
            "tokens_total_appels": tokens_reseau + tokens_cache,
        },
        "latence": {
            "reseau_s": _resume_latence(lat_reseau),
            "item_s": _resume_latence(lat_items),
            "reseau_total_s": round(sum(lat_reseau), 3),
        },
        "refus": {
            "n": sum(1 for l in lignes if l["refus"]),
            "ids": [l["id"] for l in lignes if l["refus"]][:20],
            "messages": [l["refus_message"] for l in lignes if l["refus"]][:10],
        },
        "erreurs": {
            "n": sum(1 for l in lignes if l["erreur"]),
            "ids": [l["id"] for l in lignes if l["erreur"]][:20],
        },
        "par_source": par_source, "par_langue": par_langue,
        "stats_tagger": {
            "appels": len(reseau) + len(disque),
            "requetes": len(reseau),
            "cache": len(disque),
            "tokens": tokens_reseau,
            "latence_s": round(sum(lat_reseau), 3),
            "modeles": dict(passe["cache_apres"].get("modeles", {})),
            "cle_refusee": passe["stats_tagger"].get("cle_refusee", 0),
        },
        "memoire": {
            "rss_avant_kb": passe["rss_avant"].get("rss_kb"),
            "pic_avant_kb": passe["rss_avant"].get("pic_kb"),
            "rss_apres_kb": passe["rss_apres"].get("rss_kb"),
            "pic_apres_kb": passe["rss_apres"].get("pic_kb"),
            "ru_maxrss_kb": passe["rss_apres"].get("ru_maxrss_kb"),
            "delta_pic_kb": (passe["rss_apres"].get("pic_kb", 0)
                             - passe["rss_avant"].get("pic_kb", 0)),
            "cache_octets": passe["cache_apres"]["octets"],
            "cache_octets_par_texte": round(
                passe["cache_apres"]["octets"] / max(1, composition["textes_distincts"]), 1),
        },
    }


# --------------------------------------------------------------------------- coût


def _cout(tokens: dict, prix: dict) -> float:
    hit = tokens.get("prompt_cache_hit_tokens", 0)
    miss = tokens.get("prompt_cache_miss_tokens", 0)
    if miss == 0 and tokens.get("prompt_tokens", 0):
        miss = max(0, tokens["prompt_tokens"] - hit)
    return round((hit * prix["entree_hit"] + miss * prix["entree_miss"]
                  + tokens.get("completion_tokens", 0) * prix["sortie"]) / 1_000_000.0, 6)


def couts(froid: dict) -> dict:
    api = froid["api"]
    mesure = {nom: _cout(api, prix) for nom, prix in PRIX.items()}
    uniques = froid["composition"]["textes_distincts"]
    facteur = 1000.0 / max(1, uniques)
    extrapole = {nom: round(v * facteur, 6) for nom, v in mesure.items()}
    reference_612 = 0.04
    reference_1000 = round(reference_612 / 612 * 1000, 6)
    return {
        "tokens": api,
        "prix_unitaire_par_million": PRIX,
        "lot_1000_items": mesure,
        "lot_1000_items_note": (
            f"coût réel du lot de 1 000 items : {froid['cache']['requetes_reseau']} appels "
            f"réseau + {froid['cache']['cache_disque']} rejeux disque = "
            f"{froid['cache']['appels_transport']} appels transport, "
            f"{froid['cache']['cache_memoire']} rejeux mémoire et "
            f"{froid['cache']['refus_sans_appel']} refus sans appel ; les répétitions ne sont "
            "pas facturées."),
        "extrapole_1000_phrases_uniques": extrapole,
        "extrapole_note": f"×{facteur:.4f} (1000 / {uniques} textes distincts)",
        "par_item": {nom: round(v / 1000.0, 9) for nom, v in mesure.items()},
        "par_phrase_unique": {nom: round(v / max(1, uniques), 9) for nom, v in mesure.items()},
        "reference_612": {"dollars": reference_612, "prix_1000_lineaire": reference_1000,
                          "ecart_extrapole_hors_pointe": round(
                              extrapole["hors_pointe"] - reference_1000, 6)},
        "fenetre_horaire": (
            f"run du {froid['cache']['dates_apres']['min']} au "
            f"{froid['cache']['dates_apres']['max']} (heures locales EST ; 18 h 21–18 h 33 "
            "UTC), hors pointe (16:30–00:30 UTC) ; les deux tarifs sont publiés"),
    }


# --------------------------------------------------------------------------- jsonl


def _lancer_jsonl(cache_dir: pathlib.Path, lot: list[dict], nom: str,
                  reset: bool) -> dict:
    dossier = RACINE / "work" / "tagger-lot"
    dossier.mkdir(parents=True, exist_ok=True)
    chemin = dossier / f"corpus-{nom}.txt"
    # Une ligne vide entre deux phrases : `Heuristique._phrases` la traite comme une
    # frontière. Sans elle, il fusionne les phrases sans ponctuation finale (836 lignes
    # au lieu de 1 000). Trois phrases du gold contiennent deux phrases : le CLI en rend
    # donc 1 003, ce que la mesure publie.
    chemin.write_text("\n\n".join(" ".join(it["texte"].split()) for it in lot) + "\n",
                      encoding="utf-8")
    cache_dir = cache_dir.resolve()
    if reset and cache_dir.exists():
        shutil.rmtree(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "DEEPSEEK_CACHE": str(cache_dir)}
    cmd = ["/usr/bin/time", "-v", sys.executable, str(RACINE / "tools" / "drave.py"),
           "analyser", "--fichier", str(chemin), "--jsonl", "--tagger"]
    t0 = time.perf_counter()
    p = subprocess.run(cmd, cwd=str(RACINE), env=env, capture_output=True, text=True,
                       timeout=3600)
    duree = time.perf_counter() - t0
    lignes = p.stdout.splitlines()
    valides, sources, pos_total, textes = 0, collections.Counter(), 0, []
    for ligne in lignes:
        try:
            d = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        valides += 1
        sources[d.get("source", "?")] += 1
        pos_total += sum(1 for e in d.get("etiquettes", []) if e.get("niveau") == "pos")
        textes.append(d.get("texte", ""))
    m = re.search(r"TAGGER API · modèle=([^ ]+) · appels=(\d+) · réseau=(\d+) · "
                  r"cache=(\d+) · tokens=(\d+) · latence=([\d.]+) s", p.stderr)
    cout = ({"modele": m.group(1), "appels": int(m.group(2)), "reseau": int(m.group(3)),
             "cache": int(m.group(4)), "tokens": int(m.group(5)),
             "latence_s": float(m.group(6))} if m else None)
    rss = re.search(r"Maximum resident set size \(kbytes\): (\d+)", p.stderr)
    return {
        "nom": nom, "commande": " ".join(cmd[1:]), "cache_dir": str(cache_dir),
        "duree_s": round(duree, 3), "code": p.returncode,
        "lignes": len(lignes), "json_valides": valides,
        "sources": dict(sources), "pos_total": pos_total,
        "texte_attendu": len(lot), "lignes_attendues": len(lot),
        "stderr": p.stderr[-2000:], "cout_stderr": cout,
        "rss_pic_kb": int(rss.group(1)) if rss else None,
        "stdout_octets": len(p.stdout.encode("utf-8")),
        "fichier": str(chemin), "fichier_lignes": len(chemin.read_text().splitlines()),
        "sha256_sortie": hashlib.sha256(p.stdout.encode("utf-8")).hexdigest(),
        "textes_uniques_sortie": len(set(textes)),
    }


# --------------------------------------------------------------------------- fusion


def _commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(RACINE),
                              capture_output=True, text=True, timeout=10
                              ).stdout.strip() or "inconnu"
    except (OSError, subprocess.SubprocessError):
        return "inconnu"


def fusion(args: argparse.Namespace) -> int:
    froid_brut = json.loads(pathlib.Path(args.froid).read_text(encoding="utf-8"))
    chaud_brut = json.loads(pathlib.Path(args.chaud).read_text(encoding="utf-8"))
    lot, composition = construire_lot(charger_corpus(args.libres), n=args.n, graine=args.graine)
    froid = agreger(froid_brut, composition)
    chaud = agreger(chaud_brut, composition)
    cout = couts(froid)
    # contrôle négatif : mêmes hashes, chaud à 0 réseau / 0 token / 0 dollar
    hash_froid = {l["rang"]: l["hash"] for l in froid_brut["lignes"]}
    hash_chaud = {l["rang"]: l["hash"] for l in chaud_brut["lignes"]}
    differences = sorted(r for r in hash_froid if hash_froid[r] != hash_chaud.get(r))
    controle = {
        "nom": "les mêmes 1 000 items en cache chaud",
        "hashs_identiques": len(differences) == 0,
        "differences": differences[:20],
        "froid": {"requetes": froid["cache"]["requetes_reseau"],
                  "tokens_reseau": froid["api"]["tokens_reseau"],
                  "dollars": cout["lot_1000_items"]},
        "chaud": {"requetes": chaud["cache"]["requetes_reseau"],
                  "tokens_reseau": chaud["api"]["tokens_reseau"],
                  "dollars": couts(chaud)["lot_1000_items"]},
        "verdict": ("OK : le cache chaud rejoue les 1 000 items à 0 réseau, 0 token, 0 $"
                    if (chaud["cache"]["requetes_reseau"] == 0
                        and chaud["api"]["tokens_reseau"] == 0
                        and all(v == 0 for v in couts(chaud)["lot_1000_items"].values())
                        and len(differences) == 0)
                    else "ÉCHEC : le cache chaud n'est pas gratuit ou les sorties diffèrent"),
    }
    jsonl_chaud = _lancer_jsonl(pathlib.Path(froid_brut["cache_dir"]), lot, "1000", reset=False)
    jsonl_froid = _lancer_jsonl(RACINE / "work" / "tagger-lot" / "cache-jsonl-froid",
                                lot[:20], "20-froid", reset=True)
    resultat = {
        "rapport": "tagger-lot", "tache": "X3", "ligne_roadmap": ["R0.7", "B13"],
        "date": time.strftime("%Y-%m-%d %H:%M %Z"), "commit": _commit(),
        "verdict": ("le lot de 1 000 items est mesuré de bout en bout ; le cache froid fait "
                    f"{froid['cache']['requetes_reseau']} appels réseau et le cache chaud "
                    f"{chaud['cache']['requetes_reseau']} ; les 1 000 sorties sont identiques"),
        "dispositif": {
            "modele_demande": drave.MODELE_TAGGER, "seuil": drave.SEUIL_TAGGER,
            "cablage": "drave._cascade_tagger (NeuronalLLMPOS + Heuristique, POS neuronal)",
            "client": "tools/llm/deepseek.py, température 0, cache disque",
            "machine": {"systeme": platform.platform(), "python": platform.python_version(),
                        "cpu": platform.processor() or "inconnu",
                        "nproc": os.cpu_count()},
            "cache_froid": froid_brut["cache_dir"], "cache_chaud": chaud_brut["cache_dir"],
            "passes": "froid (cache neuf) → chaud (même cache) → jsonl chaud 1 000 → "
                      "jsonl froid 20",
        },
        "corpus": {
            **composition,
            "libres": args.libres,
            "sources": (
                "612 gold (hand 20 + reel 432 + synth 160) + 50 textes libres "
                + ("(pensee-fiabilite-produit.json, 69 phrases ; 2 textes vides, 2 refus)"
                   if args.libres == "fiabilite"
                   else "(pensee-produit-bloc-l.json, 56 phrases)")),
            "note": (
                f"les 1 000 items sont des phrases réelles ; "
                f"{composition['items_repetes'] + composition['doublons_source']['n']} "
                f"rejouent un texte du lot ({composition['doublons_source']['n']} doublons + "
                f"{composition['items_repetes']} répétitions) et "
                f"{froid['cache']['refus_sans_appel']} refusent sans appel. La mesure publie "
                "le lot et l'extrapolation aux 1 000 textes uniques."),
        },
        "passes": {"froid": froid, "chaud": chaud},
        "cache": {
            "froid": froid["cache"], "chaud": chaud["cache"],
            "note": (
                f"{froid['cache']['cache_disque']} collisions de prompt servent des textes "
                "différents (même prompt, ponctuation ignorée) ; « Le chat dort. », déjà "
                "dans le gold, est servi par la mémoire. Les "
                f"{froid['cache']['refus_sans_appel']} refus sans appel (f14 « 🚀 », "
                "f17 « ... ») ne sont ni réseau ni cache."),
        },
        "debit": {"froid": froid["debit"], "chaud": chaud["debit"]},
        "memoire": {"froid": froid["memoire"], "chaud": chaud["memoire"]},
        "cout": cout,
        "jsonl": {"chaud_1000": jsonl_chaud, "froid_20": jsonl_froid},
        "controle_negatif": controle,
        "limites": [
            "Le corpus réel disponible fait 665 textes distincts : 1 000 items = 665 + 335 "
            "répétitions ; le coût des 1 000 textes uniques est extrapolé (×1,5038).",
            "Le tarif est celui du deepseek-flash au 2026-11-13 ; un changement de modèle, "
            "de routage ou de prix déplace le dollar, pas les tokens.",
            "La latence est séquentielle, une requête à la fois ; l'API accepte plus de "
            "concurrence (le débit pourrait monter, la latence par requête non).",
            "La mémoire est le pic RSS du processus Python (VmHWM / ru_maxrss), pas la "
            "mémoire du serveur DeepSeek.",
            "Le cache disque est local : un cache chaud d'une autre date peut rejouer un "
            "autre modèle ; la mesure froide est la référence.",
            "La température 0 n'est pas un déterminisme garanti de l'API ; le cache fige "
            "les réponses et le contrôle négatif compare les sorties rejouées.",
        ],
        "fichiers": [
            "reports/rapport-tagger-lot.md", "reports/rapport-tagger-lot.json",
            "tools/tests/linguistique/qualifier_tagger_lot.py",
        ],
    }
    pathlib.Path(args.sortie).write_text(
        json.dumps(resultat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({
        "froid": {"requetes": froid["cache"]["requetes_reseau"],
                  "cache_disque": froid["cache"]["cache_disque"],
                  "tokens": froid["api"]["total_tokens"],
                  "dollars_hp": cout["lot_1000_items"]["hors_pointe"],
                  "debit_items_min": froid["debit"]["items_par_min"],
                  "pic_kb": froid["memoire"]["pic_apres_kb"]},
        "chaud": {"requetes": chaud["cache"]["requetes_reseau"],
                  "tokens": chaud["api"]["tokens_reseau"],
                  "dollars_hp": couts(chaud)["lot_1000_items"]["hors_pointe"],
                  "debit_items_min": chaud["debit"]["items_par_min"],
                  "pic_kb": chaud["memoire"]["pic_apres_kb"]},
        "extrapole_1000_uniques": cout["extrapole_1000_phrases_uniques"],
        "jsonl": {"chaud_lignes": jsonl_chaud["lignes"],
                  "chaud_cout": jsonl_chaud["cout_stderr"],
                  "froid_lignes": jsonl_froid["lignes"],
                  "froid_cout": jsonl_froid["cout_stderr"]},
        "controle_negatif": controle["verdict"],
    }, ensure_ascii=False, indent=1))
    return 0 if controle["hashs_identiques"] else 1


# --------------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=("froid", "chaud", "fusion"), required=True)
    ap.add_argument("--cache", default="/tmp/tagger-lot-cache")
    ap.add_argument("--sortie", default="/tmp/tagger-lot.json")
    ap.add_argument("--froid", default="/tmp/tagger-lot-froid.json")
    ap.add_argument("--chaud", default="/tmp/tagger-lot-chaud.json")
    ap.add_argument("--n", type=int, default=N_LOT)
    ap.add_argument("--graine", type=int, default=GRAINE)
    ap.add_argument("--limite", type=int, default=0,
                    help="smoke test : ne mesurer que les N premiers items")
    ap.add_argument("--reset", action="store_true", help="vider le cache avant la passe")
    ap.add_argument("--partition", default="alternative")
    ap.add_argument("--libres", choices=sorted(LIBRES), default="fiabilite",
                    help="banc des 50 textes libres (défaut : fiabilite)")
    args = ap.parse_args()

    if args.mode == "fusion":
        return fusion(args)

    items = charger_corpus(args.libres)
    lot, composition = construire_lot(items, n=args.n, graine=args.graine)
    if args.limite:
        lot = lot[:args.limite]
        composition = {**composition, "items_mesures": len(lot)}
    cache = pathlib.Path(args.cache).resolve()
    if args.reset and cache.exists():
        shutil.rmtree(cache)
    cache.mkdir(parents=True, exist_ok=True)
    print(f"[{args.mode}] {len(lot)} items · cache {cache} · source "
          f"{composition['lignes_source']} lignes / {composition['textes_distincts']} textes",
          flush=True)
    passe = mesurer_passe(args.mode, lot, cache, partition=args.partition)
    passe["composition"] = composition
    pathlib.Path(args.sortie).write_text(
        json.dumps(passe, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    resume = agreger(passe, composition)
    print(json.dumps({
        "mode": args.mode, "items": resume["items"], "duree_s": resume["duree_s"],
        "requetes": resume["cache"]["requetes_reseau"],
        "cache_disque": resume["cache"]["cache_disque"],
        "cache_memoire": resume["cache"]["cache_memoire"],
        "tokens_reseau": resume["api"]["total_tokens"],
        "debit_items_min": resume["debit"]["items_par_min"],
        "pic_kb": resume["memoire"]["pic_apres_kb"],
        "refus": resume["refus"]["n"], "erreurs": resume["erreurs"]["n"],
    }, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
