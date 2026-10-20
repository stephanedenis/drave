#!/usr/bin/env python3
"""analyse_litteraire.py — OÙ LE LITTÉRAIRE SE PERD : noms propres, omissions, expansions.

POURQUOI ✓✓. La mesure 64 a donné **47,7-49,8** de chrF au littéraire, le domaine le plus dur ✓✗, mais un chrF
moyen ne dit **pas ce qui manque** : est-ce le style, le sens, les noms, la longueur ? Ici, on reprend les sorties
**déjà produites** (200 paires 1:1 du *Tour du monde*) et on les décompose ✓✓ :

  · **les noms propres** — le français porte « Fogg », « Passepartout », « Aouda »… ; la sortie anglaise les
    conserve-t-elle ? ✓✓ On mesure le **rappel des ancres** (occurrence par occurrence), avec un **contrôle
    négatif** : le même dictionnaire appliqué à la sortie d'une **autre** paire ✓✓ ;
  · **les omissions** — une sortie **deux fois plus courte** que la référence a perdu du contenu ✗✓ ;
  · **les expansions** — une sortie **deux fois plus longue** a ajouté du contenu ✗✓ ;
  · **le chrF par sous-groupe** — avec ou sans nom propre ✓ : *si les paires avec noms sont les plus mauvaises, le
    problème est la fidélité des entités ; sinon, c'est le style* ✓✓.

CE QUE CE N'EST PAS ✗ : une analyse sémantique (on ne vérifie pas que le sens est juste, seulement que les noms
sont là et que la longueur tient) ; et le dictionnaire d'ancres est celui de l'aligneur
(`tools/aligneur_litteraire.py`), donc il couvre les noms **connus** du livre, pas les descriptions ✓.
"""
from __future__ import annotations
import argparse, importlib.util, json, pathlib, random, re, unicodedata

RACINE = pathlib.Path(__file__).resolve().parent.parent


def charge_ancres():
    spec = importlib.util.spec_from_file_location("aligneur", RACINE / "tools/aligneur_litteraire.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ANCRES


def nz(t: str) -> str:
    return " ".join(unicodedata.normalize("NFC", t).lower().split())


def trouve(formes, texte, majuscule=False) -> int:
    """Occurrences d'un groupe de formes, frontières de mot ✓ (accent/casse insensibles ; majuscule exigée si
    l'ancre est ambiguë : « fix » contre « fixe », « young » contre « young man ») ✓."""
    n = 0
    for f in formes:
        for m in re.finditer(r"(?<!\w)" + re.escape(f) + r"(?!\w)", texte, re.I):
            if majuscule and not texte[m.start()].isupper():
                continue
            n += 1
    return n


def compte_groupe(formes, texte, majuscule) -> int:
    """Une occurrence de « Phileas Fogg » ne doit pas compter deux fois (forme longue et forme courte) ✓."""
    return max((trouve([f], texte, majuscule) for f in formes), default=0)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="data/alignement/verne_fr_en.json")
    ap.add_argument("--resultats", default="reports/traduction-litteraire-3b.json,reports/traduction-litteraire-7b.json")
    ap.add_argument("--sortie", default="reports/analyse-litteraire.json")
    a = ap.parse_args()
    data = json.loads(pathlib.Path(a.corpus).read_text())
    pp = [p for p in data["paires"] if p.get("n_fr") == 1 and p.get("n_en") == 1]
    ancres = charge_ancres()                       # (nom, formes_fr, formes_en, majuscule_exigee) ✓
    sorties = []
    for patron in a.resultats.split(","):
        for f in sorted(RACINE.glob(patron.strip())):
            d = json.loads(f.read_text())[0]
            sorties.append((f.stem, d))
    res = []
    for nom_modele, d in sorties:
        rng = random.Random(0)
        noms_tot = noms_gardes = 0
        paires_nom = paires_nom_ok = 0
        court = long = 0
        chrf_nom, chrf_sans = [], []
        for x in d["details"]:
            i = x["article"]
            if i >= len(pp):
                continue
            src, ref, out = pp[i]["fr"], pp[i]["en"], x["sortie"]
            groupes = []
            for nom, fr, en, maj in ancres:
                n_src = compte_groupe(fr, src, maj)
                if n_src:
                    groupes.append((n_src, compte_groupe(en, out, maj)))
            if groupes:
                chrf_nom.append(x["chrf"]); paires_nom += 1
                if all(g >= n for n, g in groupes):
                    paires_nom_ok += 1
                for n, g in groupes:
                    noms_tot += n; noms_gardes += min(n, g)
            else:
                chrf_sans.append(x["chrf"])
            ratio = len(out) / max(1, len(ref))
            court += ratio < 0.5
            long += ratio > 2.0
        n = len(d["details"])
        # contrôle négatif : les noms de la source apparaissent-ils dans la sortie d'une AUTRE paire ? ✓✓
        noms_controle = tirages = 0
        for x in d["details"][:100]:
            i = x["article"]
            if i >= len(pp):
                continue
            src = pp[i]["fr"]
            autres = [y for y in d["details"] if y["article"] != i]
            if not autres:
                continue
            autre = rng.choice(autres)["sortie"]
            for nom, fr, en, maj in ancres:
                n_src = compte_groupe(fr, src, maj)
                if n_src:
                    noms_controle += min(n_src, compte_groupe(en, autre, maj))
                    tirages += n_src
        r = {"modele": nom_modele, "n": n,
             "rappel_noms": round(noms_gardes / max(1, noms_tot), 3),
             "occurrences_noms": noms_tot,
             "paires_avec_nom": paires_nom,
             "paires_noms_tous_gardes": round(paires_nom_ok / max(1, paires_nom), 3),
             "controle_rappel_noms": round(noms_controle / max(1, tirages), 3),
             "omissions_ratio_lt_0.5": round(court / n, 3),
             "expansions_ratio_gt_2": round(long / n, 3),
             "chrf_avec_nom": round(sum(chrf_nom) / max(1, len(chrf_nom)), 1),
             "chrf_sans_nom": round(sum(chrf_sans) / max(1, len(chrf_sans)), 1),
             "n_avec_nom": len(chrf_nom), "n_sans_nom": len(chrf_sans)}
        res.append(r)
        print(f"  {nom_modele} : rappel noms {r['rappel_noms']:.1%} (contrôle {r['controle_rappel_noms']:.1%}) "
              f"· paires 100 % {r['paires_noms_tous_gardes']:.1%} · omissions {r['omissions_ratio_lt_0.5']:.1%} "
              f"· expansions {r['expansions_ratio_gt_2']:.1%} · chrF avec nom {r['chrf_avec_nom']} "
              f"sans nom {r['chrf_sans_nom']}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
