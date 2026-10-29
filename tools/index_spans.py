#!/usr/bin/env python3
"""index_spans.py — R05 : le balayage classique (requête → spans), sans encodeur.

POURQUOI CE FICHIER. Le balayage humain trouve « 3 663 » ou « 12 septembre 2025 » sans lire le
document : il cherche une **forme** — un nombre, une date — pas une phrase. Le contrôleur de
R0.2, lui, classe des **passages** ; il ne sait pas qu'un nombre est une réponse possible.

Cet index fait le chemin **classique** que la fiche R05 demande avant toute tête : il extrait
les **spans** (nombres avec unité, dates) des régions de R0.1, il les offset dans le flux, et il
les classe par le BM25 du **passage** qui les porte. La tête ne s'ajoutera que si ce chemin ne
suffit pas — et R0.4 a montré qu'elle ne paie pas.

Ce qui est vérifié, et comment :
  - **les offsets** : `flux[start:start+octets]` doit rendre exactement le span ;
  - **le rappel@10** : sur les questions dont la valeur est un nombre ou une date, le span gold
    est-il dans les dix premiers ?
  - **le rejeu** : deux indexations du même document donnent les mêmes spans, aux mêmes offsets.

Usage :
  python3 tools/index_spans.py --document docs/implantation/format-flux.md --requete "3 663"
  python3 tools/index_spans.py --mesure --json reports/r05-balayage.json
  python3 tools/index_spans.py --autotest
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document  # noqa: E402
import lecteur_controleur as lc  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
# Un nombre, avec ses séparateurs (3 663, 1,5, 49,87 %) et son unité éventuelle ; une date ISO
# ou française. Les deux formes que le balayage humain cherche sans lire.
RE_NOMBRE = re.compile(r"\d[\d\s.,]*\d|\d")
RE_DATE = re.compile(r"\d{4}-\d{2}-\d{2}|\d{1,2}\s+(?:janvier|février|mars|avril|mai|juin|"
                     r"juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}", re.I)
# Les nombres en MOTS : « combien d'invariants ? » attend « six », pas un chiffre. Le lexique est
# fermé (les cardinaux et ordinaux courants) — un span de type « nombre-mot ».
MOTS_NOMBRES = (
    "un|une|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|"
    "seize|vingt|trente|quarante|cinquante|soixante|cent|mille|million|milliard|"
    "premier|première|second|seconde|deuxième|troisième|quatrième|cinquième|sixième|septième|"
    "huitième|neuvième|dixième|onzième|douzième|treizième|quatorzième|quinzième|seizième|"
    "vingtième|trentième|quarantième|cinquantième|soixantième|centième|millième|"
    "quatre-vingt|quatre-vingts|quatre-vingtième|quatre-vingt-dix|soixante-dix|"
    "dix-sept|dix-huit|dix-neuf|deux-cents|trois-cents"
)
RE_NOMBRE_MOT = re.compile(rf"\b(?:{MOTS_NOMBRES})\b", re.I)
UNITES = ("octets", "o", "Go", "Mo", "Ko", "Gio", "Mio", "ms", "s", "ns", "µs", "%", "jetons",
          "t/s", "tok/s", "couches", "paramètres", "M", "B", "G")


def spans_du_document(manifeste: dict) -> list[dict]:
    """Les spans d'un document, offsetés dans le flux, avec leur passage porteur."""
    passages = lc.passages(manifeste)
    out = []
    for passage in passages:
        texte = passage["texte"]
        # Les nombres en MOTS (« six », « cinq ») ont été essayés : +2 questions au pilote,
        # −5 sur les deux bancs (le bruit des spans l'emporte). Mesuré, rejeté — voir la fiche.
        for motif, type_ in ((RE_DATE, "date"), (RE_NOMBRE, "nombre")):
            for m in motif.finditer(texte):
                span = m.group(0).strip()
                if not span:
                    continue
                # l'unité qui suit fait partie du span : « 3 663 octets », « 24,05 % »
                fin = m.end()
                reste = texte[fin:fin + 12]
                unite = next((u for u in UNITES if reste.lstrip(" ").startswith(u)), None)
                if unite:
                    span = texte[m.start():fin + len(reste) - len(reste.lstrip(" ")) + len(unite)]
                debut = passage["start"] + len(texte[:m.start()].encode("utf-8"))
                out.append({"texte": span, "type": type_, "start": debut,
                            "octets": len(span.encode("utf-8")),
                            "passage": passage["indice"], "region": passage["region"],
                            "pos": m.start(), "fenetre": texte[max(0, m.start() - 50):m.end() + 50]})
    return out


class IndexSpans:
    """L'index : les passages (BM25) et les spans qu'ils portent."""

    def __init__(self, manifeste: dict):
        self.passages = lc.passages(manifeste)
        self.index = lc.Index(self.passages)
        self.spans = spans_du_document(manifeste)
        self.par_passage: dict[int, list[int]] = {}
        for i, span in enumerate(self.spans):
            self.par_passage.setdefault(span["passage"], []).append(i)

    def chercher(self, requete: str, k: int = 10) -> list[dict]:
        """Le classement : le BM25 du passage porteur, puis ses spans dans l'ordre.

        La fenêtre (le texte autour du nombre) a été essayée comme second terme : elle
        RÉORDONNE les spans d'une même phrase et fait tomber le top-1 de 0,932 à 0,691 sur le
        banc lexical — la couverture de la fenêtre récompense les mots de la question, pas la
        valeur. Mesuré, rejeté (voir la fiche R05, § « ce qui a été essayé »)."""
        scores = self.index.scores(requete)
        ordre = sorted(range(len(self.passages)), key=lambda i: -scores[i])
        sortie: list[dict] = []
        for i in ordre:
            for j in self.par_passage.get(i, []):
                span = dict(self.spans[j])
                span.pop("fenetre", None)
                span["score"] = round(scores[i], 3)
                sortie.append(span)
            if len(sortie) >= k:
                break
        return sortie[:k]

    def exact(self, valeur: str, k: int | None = None) -> list[dict]:
        """La recherche exacte d'une valeur : le balayage d'un terme connu."""
        cible = normalise(valeur)
        out = [s for s in self.spans if normalise(s["texte"]).startswith(cible)]
        return out[:k] if k else out


def normalise(t: str) -> str:
    return re.sub(r"[\s.,]", "", str(t).lower())


def autotest() -> int:
    chemin = RACINE / "docs/implantation/format-flux.md"
    manifeste = graphe_document.manifeste(chemin)
    flux = b"".join(r["texte"].encode("utf-8") for r in manifeste["regions"])
    a = IndexSpans(manifeste)
    b = IndexSpans(manifeste)
    ok = total = 0

    total += 1
    if a.spans and all(flux[s["start"]:s["start"] + s["octets"]] == s["texte"].encode("utf-8")
                       for s in a.spans):
        print(f"✅ offsets exacts : {len(a.spans)} spans, tous dans le flux"); ok += 1
    else:
        print("❌ offsets faux")

    total += 1
    if [(s["texte"], s["start"]) for s in a.spans] == [(s["texte"], s["start"]) for s in b.spans]:
        print("✅ rejeu : deux indexations identiques"); ok += 1
    else:
        print("❌ rejeu : deux indexations diffèrent")

    total += 1
    trouves = a.exact("3 663")
    if trouves and any("3 663" in s["texte"] for s in trouves):
        print(f"✅ recherche exacte : « 3 663 » trouvé à l'offset {trouves[0]['start']}"); ok += 1
    else:
        print("❌ recherche exacte : « 3 663 » introuvable")

    total += 1
    top = a.chercher("Combien d'octets coûte le mode dense par flux ?", 10)
    if top and any("3 663" in s["texte"] for s in top):
        print("✅ balayage : la valeur est dans les dix premiers spans"); ok += 1
    else:
        print("❌ balayage : la valeur n'est pas dans les dix premiers spans")

    total += 1
    if not a.exact("zorglub 42"):
        print("✅ contrôle négatif : un terme absent ne rend rien"); ok += 1
    else:
        print("❌ contrôle négatif : un terme absent rend un span")

    total += 1
    # contrôle croisé : un index ne trouve que SON document. « drave » n'est pas dans
    # format-flux.md, et la valeur d'un autre document ne doit pas y apparaître.
    if not a.exact("drave") and not a.exact("billots"):
        print("✅ contrôle croisé : un terme d'un autre document ne rend rien"); ok += 1
    else:
        print("❌ contrôle croisé : l'index a trouvé un terme d'un autre document")

    print(f"\n{ok}/{total} contrôles verts")
    return 0 if ok == total else 1


def mesure(json_path: pathlib.Path | None = None) -> int:
    """Le rappel@10 sur les deux bancs, et le temps par requête."""
    resultats = {}
    for nom, chemin_banc in (("lexical", "tools/tests/documents/bench-complet.json"),
                             ("paraphrase", "tools/tests/documents/bench-durci.json")):
        banc = json.loads((RACINE / chemin_banc).read_text(encoding="utf-8"))
        total = trouves = 0
        durees = []
        for document in banc["documents"]:
            index = IndexSpans(graphe_document.manifeste(RACINE / document["chemin"]))
            for q in document["questions"]:
                if not re.search(r"\d", str(q["valeur"])):
                    continue  # le rappel des nombres et des dates seulement
                debut = time.time()
                top = index.chercher(q["question"], 10)
                durees.append(time.time() - debut)
                total += 1
                if any(normalise(q["valeur"]) in normalise(s["texte"]) for s in top):
                    trouves += 1
        resultats[nom] = {"n": total, "trouves": trouves,
                          "rappel10": round(trouves / total, 3) if total else 0,
                          "ms_moyen": round(1000 * sum(durees) / len(durees), 2) if durees else 0}
        print(f"  {nom:11s} n={total:3d} · rappel@10 {resultats[nom]['rappel10']:.3f} "
              f"· {resultats[nom]['ms_moyen']:.1f} ms/requête")
    if json_path:
        json_path.write_text(json.dumps({"date": "2026-10-29", "ligne": "R0.4/R05",
                                         "resultats": resultats}, ensure_ascii=False, indent=1),
                             encoding="utf-8")
        print(f"  résultats : {json_path}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="R05 — l'index de spans (balayage).")
    ap.add_argument("--document", type=pathlib.Path)
    ap.add_argument("--requete")
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--exact", help="recherche exacte d'une valeur")
    ap.add_argument("--mesure", action="store_true")
    ap.add_argument("--json", type=pathlib.Path)
    ap.add_argument("--autotest", action="store_true")
    args = ap.parse_args()
    if args.autotest:
        return autotest()
    if args.mesure:
        return mesure(args.json)
    if not args.document:
        ap.error("--document est requis")
    index = IndexSpans(graphe_document.manifeste(args.document))
    if args.exact:
        for s in index.exact(args.exact, args.k):
            print(f"{s['type']:6s} {s['start']:6d} {s['texte']!r}")
        return 0
    if not args.requete:
        ap.error("--requete ou --exact est requis")
    for s in index.chercher(args.requete, args.k):
        print(f"{s['score']:6.2f} {s['type']:6s} {s['start']:6d} {s['texte']!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
