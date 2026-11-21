#!/usr/bin/env python3
"""or_roles_adjudication.py — J4, étape 2 : l'**adjudication** des désaccords de cadres.

POURQUOI. Le second annotateur (`tools/or_roles_second.py`) a mesuré un accord de F1 0,7085 avec
l'or de rôles — et l'analyse a montré que certains désaccords sont des **erreurs de l'or**
(or-f47 : « c » comme agent de « C'est ») ou des différences de périmètre (or-f50). Un or qui
contient des erreurs ne peut pas servir de référence : il faut un **troisième passage** qui tranche
les désaccords, texte par texte, en voyant les deux annotations.

CE QUE LE SCRIPT FAIT. Il prend les textes les plus faibles du second passage, envoie à l'API le
texte + les deux annotations (A = l'or, B = le second) + le schéma des 7 rôles, et demande une
**adjudication** : pour chaque rôle, quelles expressions sont justes (A, B, les deux, aucune) et
quelle est la bonne annotation. Il rend un JSON et un petit bilan.

Usage (fenêtre remisée) :
  source ~/.bashrc && python3 tools/or_roles_adjudication.py --n 10 --json reports/or-roles-adjudication.json
  python3 tools/or_roles_adjudication.py --sans-api   # le témoin
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import urllib.request

RACINE = pathlib.Path(__file__).resolve().parent.parent
OR = RACINE / "reports" / "or-roles-base-v1.json"
SECOND = RACINE / "reports" / "or-roles-second.json"
MODELE = "deepseek-chat"
URL = "https://api.deepseek.com/chat/completions"
ROLES = ("agent", "predicat", "lieu", "temps", "destinataire", "possession", "complement")


def prompt(texte: str, a: dict, b: dict) -> str:
    return (
        "Tu es l'adjudicateur d'une annotation de **cadres sémantiques** en français. Deux "
        "annotateurs ont produit les cadres ci-dessous pour le même texte ; ils ne sont pas "
        "d'accord. Tranche : pour chaque rôle (agent, predicat, lieu, temps, destinataire, "
        "possession, complement), dis quelles expressions sont justes — celles de A, celles de B, "
        "les deux, ou aucune — et rends l'annotation **corrigée** (les expressions du texte, "
        "copiées exactement). Réponds en JSON strict : "
        '{"cadres": [{"principal": true, "roles": {"agent": ["..."], "predicat": ["..."], '
        '"lieu": [], "temps": [], "destinataire": [], "possession": [], "complement": []}}], '
        '"verdicts": [{"role": "agent", "A": ["..."], "B": ["..."], "choix": "A|B|deux|aucune"}]}\n\n'
        f"Texte : {texte}\n\nA (or) : {json.dumps(a, ensure_ascii=False)}\n\n"
        f"B (second) : {json.dumps(b, ensure_ascii=False)}"
    )


def appeler(texte: str, a: dict, b: dict, delai: int = 90) -> dict:
    clé = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("DSH_API_KEY")
    if not clé:
        return {"erreur": "pas de DEEPSEEK_API_KEY"}
    corps = json.dumps({
        "model": MODELE,
        "messages": [{"role": "user", "content": prompt(texte, a, b)}],
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


def choisir(n: int) -> list[dict]:
    second = json.loads(SECOND.read_text(encoding="utf-8"))
    or_ = json.loads(OR.read_text(encoding="utf-8"))
    par_id = {t["id"]: t for t in or_["textes"]}
    ok = [x for x in second["detail"] if "f1_moyen" in x]
    faibles = sorted(ok, key=lambda x: x["f1_moyen"])[:n]
    sortie = []
    for x in faibles:
        t = par_id[x["id"]]
        cadres = t["cadres"]
        if isinstance(cadres, str):
            cadres = json.loads(cadres)
        sortie.append({"id": x["id"], "texte": x["texte"], "f1": x["f1_moyen"],
                       "a": cadres, "b": x.get("pred", {})})
    return sortie


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--json", default="")
    ap.add_argument("--sans-api", action="store_true")
    a = ap.parse_args()
    textes = choisir(a.n)
    if a.sans_api:
        print(json.dumps({"textes": len(textes), "adjudiqués": 0}, ensure_ascii=False))
        return
    resultats = []
    for t in textes:
        r = appeler(t["texte"], t["a"], t["b"])
        resultats.append({"id": t["id"], "f1": t["f1"],
                          "adjudication": r.get("cadres"), "verdicts": r.get("verdicts"),
                          "erreur": r.get("erreur")})
        print(f"  {t['id']} (F1 {t['f1']:.2f}) : "
              f"{'ok' if r.get('cadres') else r.get('erreur', 'vide')}")
    ok = [x for x in resultats if x.get("adjudication")]
    print(json.dumps({"textes": len(textes), "adjudiqués": len(ok)}, ensure_ascii=False))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps({"detail": resultats}, ensure_ascii=False,
                                                   indent=1) + "\n")


if __name__ == "__main__":
    main()
