#!/usr/bin/env python3
"""or_roles_second.py — J4, les **seconds cadres** : un second annotateur (l'API) sur l'or de rôles.

POURQUOI. L'or de rôles (`reports/or-roles-base-v1.json`, 46 textes) a été codé par « base » — un
seul annotateur, donc pas un or humain indépendant (l'état de S le dit : « 12 des 28 mappings
contredisent la source anglaise »). J4 demande **un second cadre** : un second annotateur qui
relève les mêmes cadres sémantiques, pour mesurer l'**accord inter-annotateurs** — si deux
annotateurs indépendants retrouvent les mêmes rôles, l'or tient ; sinon, il mesure le désaccord.

Le second annotateur est l'API (`deepseek-chat`), avec le même schéma : 7 rôles (agent, prédicat,
lieu, temps, destinataire, possession, complément), chaque rôle une liste d'expressions **copiées
du texte**. La comparaison se fait par **expression** (les chaînes, normalisées), pas par offset —
le modèle ne compte pas les caractères.

Usage :
  source ~/.bashrc && python3 tools/or_roles_second.py --json reports/or-roles-second.json
  python3 tools/or_roles_second.py --sans-api   # le témoin : aucun second cadre
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import unicodedata
import urllib.request

RACINE = pathlib.Path(__file__).resolve().parent.parent
OR = RACINE / "reports" / "or-roles-base-v1.json"
MODELE = "deepseek-chat"
URL = "https://api.deepseek.com/chat/completions"
ROLES = ("agent", "predicat", "lieu", "temps", "destinataire", "possession", "complement")


def norme(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]+", " ", s).strip()


def prompt(texte: str) -> str:
    return (
        "Pour ce texte français, donne les **cadres sémantiques** : pour chaque cadre, le prédicat "
        "et les rôles. Les 7 rôles sont : agent, predicat, lieu, temps, destinataire, possession, "
        "complement. Chaque rôle est la **liste des expressions du texte** (copiées exactement, "
        "sans rien inventer). Réponds en JSON strict : "
        '{"cadres": [{"principal": true, "roles": {"agent": ["..."], "predicat": ["..."], '
        '"lieu": [], "temps": [], "destinataire": [], "possession": [], "complement": []}}]}\n\n'
        f"Texte : {texte}"
    )


def appeler(texte: str, delai: int = 60) -> dict:
    clé = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("DSH_API_KEY")
    if not clé:
        return {"erreur": "pas de DEEPSEEK_API_KEY"}
    corps = json.dumps({
        "model": MODELE,
        "messages": [{"role": "user", "content": prompt(texte)}],
        "temperature": 0, "response_format": {"type": "json_object"},
    }).encode("utf-8")
    req = urllib.request.Request(URL, data=corps, headers={
        "Content-Type": "application/json", "Authorization": f"Bearer {clé}"})
    try:
        with urllib.request.urlopen(req, timeout=delai) as r:
            d = json.loads(r.read().decode("utf-8"))
        return json.loads(d["choices"][0]["message"]["content"])
    except Exception as e:  # noqa: BLE001
        return {"erreur": f"{type(e).__name__}: {e}"}


def roles_du_gold(cadres: list[dict]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {r: set() for r in ROLES}
    for c in cadres:
        for r, exps in (c.get("roles") or {}).items():
            if r in out:
                for e in exps:
                    out[r].add(norme(e.get("texte", "")))
    return out


def roles_de_lapi(cadres: list[dict]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {r: set() for r in ROLES}
    for c in cadres:
        for r, exps in (c.get("roles") or {}).items():
            if r in out and isinstance(exps, list):
                for e in exps:
                    out[r].add(norme(e if isinstance(e, str) else str(e)))
    return out


def f1(pred: set[str], gold: set[str]) -> float:
    if not pred and not gold:
        return 1.0
    if not pred or not gold:
        return 0.0
    inter = len(pred & gold)
    if not inter:
        return 0.0
    p, r = inter / len(pred), inter / len(gold)
    return 2 * p * r / (p + r)


def mesurer(sans_api: bool = False) -> dict:
    or_ = json.loads(OR.read_text(encoding="utf-8"))
    textes = or_["textes"]
    resultats = []
    for t in textes:
        cadres = t["cadres"]
        if isinstance(cadres, str):
            cadres = json.loads(cadres)
        gold = roles_du_gold(cadres)
        if sans_api:
            resultats.append({"id": t["id"], "texte": t["texte"], "sans_api": True})
            continue
        r = appeler(t["texte"])
        if "erreur" in r:
            resultats.append({"id": t["id"], "erreur": r["erreur"]})
            continue
        pred = roles_de_lapi(r.get("cadres", []))
        par_role = {role: f1(pred[role], gold[role]) for role in ROLES}
        resultats.append({"id": t["id"], "texte": t["texte"],
                          "f1_roles": par_role, "f1_moyen": sum(par_role.values()) / len(ROLES),
                          "pred": {k: sorted(v) for k, v in pred.items() if v},
                          "gold": {k: sorted(v) for k, v in gold.items() if v}})
    ok = [x for x in resultats if "f1_moyen" in x]
    return {"textes": len(textes), "annotés": len(ok),
            "f1_moyen": round(sum(x["f1_moyen"] for x in ok) / len(ok), 4) if ok else None,
            "detail": resultats}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="")
    ap.add_argument("--sans-api", action="store_true")
    a = ap.parse_args()
    r = mesurer(a.sans_api)
    print(json.dumps({k: r[k] for k in ("textes", "annotés", "f1_moyen")}, ensure_ascii=False))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
