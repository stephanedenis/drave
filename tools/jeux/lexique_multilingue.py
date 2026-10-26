#!/usr/bin/env python3
"""lexique_multilingue.py — les libellés des jeux, en 53 langues.

Le fichier `lexique_multilingue.json` (construit par
`construire_lexique_multilingue.py`) porte les libellés **normalisés** de
35 concepts : noms des cinq jeux, pièces des échecs, rangs et enseignes des
cartes, couleurs, notions de maîtres. Ce module les charge et les rend
cherchables par **domaine** :

    MULTI.cherche("echecs.piece", "король g1 f3")
    MULTI.cherche("cartes.couleur", "ملك القلوب")

La recherche est **multi-formes** : n-grammes de 1 à 4 unités pour les langues à
espaces, et sous-chaîne pour les écritures qui n'en mettent pas (CJK, thaï). Le
libellé est comparé sous sa forme normalisée (`normalise_forme`), la même que
celle du constructeur : NFKC, casse pliée, diacritiques optionnels retirés,
parenthèses de désambiguïsation ôtées.

Ce module ne **devine** pas la langue d'un texte : il compte les libellés
reconnus et rend la langue la plus probable (`detecte_langue`). C'est une
mesure, pas une certitude ; la fiche donne le taux.
"""
from __future__ import annotations

import json
import pathlib
from collections import Counter, defaultdict
from dataclasses import dataclass

from .lexique import normalise_forme

FICHIER = pathlib.Path(__file__).resolve().parent / "lexique_multilingue.json"


@dataclass(frozen=True)
class CorrespondanceML:
    concept: str
    domaine: str
    valeur: str
    langue: str
    forme: str
    position: int


def _domaine_valeur(concept: str) -> tuple[str, str]:
    """Le concept Wikidata → (domaine du codec, valeur sémantique)."""
    p = concept.split(".")
    if concept.startswith("echecs.piece."):
        return "echecs.piece", p[-1]
    if concept.startswith("cartes.rang."):
        return "cartes.rang", p[-1]
    if concept.startswith("cartes.couleur."):
        return "cartes.couleur", p[-1]
    if concept.startswith("echecs."):
        return "echecs.terme", p[-1]
    if concept.startswith("cartes."):
        return "cartes.terme", p[-1]
    if concept == "go.passe":
        return "go.passe", "passe"
    if concept.startswith("go."):
        return "go.terme", p[-1]
    if concept.startswith("jeu."):
        return "jeu.nom", p[-1]
    if concept == "commun.blanc":
        return "commun.couleur", "w"
    if concept == "commun.noir":
        return "commun.couleur", "b"
    if concept.startswith("maitre."):
        return "maitre.concept", p[-1]
    return p[0], p[-1]


class Multilingue:
    def __init__(self, chemin: pathlib.Path | str = FICHIER) -> None:
        self.chemin = pathlib.Path(chemin)
        self.donnees = json.loads(self.chemin.read_text(encoding="utf-8"))
        self._construire()

    @classmethod
    def depuis_donnees(cls, donnees: dict) -> "Multilingue":
        obj = cls.__new__(cls)
        obj.chemin = None
        obj.donnees = donnees
        obj._construire()
        return obj

    def _construire(self) -> None:
        self.langues: list[str] = list(self.donnees["langues"])
        self.concepts: dict = self.donnees["concepts"]
        # domaine → {forme: [(concept, valeur, langue)]}
        self.index: dict[str, dict[str, list[tuple[str, str, str]]]] = defaultdict(dict)
        for concept, c in self.concepts.items():
            domaine, valeur = _domaine_valeur(concept)
            for langue, formes in c.get("labels", {}).items():
                for f in formes:
                    f = normalise_forme(f)
                    if not f:
                        continue
                    variantes = {f}
                    # l'article arabe (ال) et l'article hébreu (ה) sont des
                    # préfixes : le libellé Wikidata les porte souvent, la
                    # surface peut les omettre (ou l'inverse).
                    if langue == "ar":
                        variantes.add(f[2:] if f.startswith("ال") else "ال" + f)
                    if langue == "he":
                        variantes.add(f[1:] if f.startswith("ה") else "ה" + f)
                    for v in variantes:
                        self.index[domaine].setdefault(v, [])
                        if (concept, langue) not in [(x[0], x[2]) for x in self.index[domaine][v]]:
                            self.index[domaine][v].append((concept, valeur, langue))
        # les formes longues d'abord, pour que « jeu de cartes » batte « cartes »
        self._formes_triees = {
            d: sorted(table, key=len, reverse=True) for d, table in self.index.items()
        }
        # un index unique pour la détection de langue : une seule passe par texte
        self._detection: dict[str, set[str]] = {}
        for domaine in ("jeu.nom", "echecs.piece", "cartes.rang", "cartes.couleur",
                        "go.passe", "commun.couleur"):
            for forme, entrées in self.index.get(domaine, {}).items():
                for _, _, langue in entrées:
                    self._detection.setdefault(forme, set()).add(langue)

    # ------------------------------------------------------------------
    def cherche(self, domaine: str, texte: str, max_ngram: int = 4) -> list[CorrespondanceML]:
        """Toutes les occurrences des libellés du domaine dans le texte."""
        t = normalise_forme(texte)
        if not t:
            return []
        toks = t.split()
        out: list[CorrespondanceML] = []
        vus: set[tuple[str, str, int, str]] = set()

        def ajoute(concept, valeur, langue, forme, pos):
            cle = (concept, langue, pos, forme)
            if cle in vus:
                return
            vus.add(cle)
            out.append(CorrespondanceML(concept, domaine, valeur, langue, forme, pos))

        for n in range(1, max_ngram + 1):
            for i in range(len(toks) - n + 1):
                forme = " ".join(toks[i:i + n])
                for concept, valeur, langue in self.index.get(domaine, {}).get(forme, []):
                    ajoute(concept, valeur, langue, forme, i)
        # écritures sans espaces : le libellé peut être une sous-chaîne du texte
        for forme in self._formes_triees.get(domaine, []):
            if " " in forme or len(forme) < 2 or not any(ord(c) > 127 for c in forme):
                continue
            pos = t.find(forme)
            if pos >= 0:
                for concept, valeur, langue in self.index[domaine][forme]:
                    ajoute(concept, valeur, langue, forme, pos)
        return sorted(out, key=lambda m: (m.position, -len(m.forme)))

    # ------------------------------------------------------------------
    def detecte_langue(self, texte: str) -> str | None:
        """La langue la plus probable, par comptage de libellés reconnus.

        On ne parcourt pas les huit domaines : un index unique (forme → langues)
        est consulté en une passe. C'est ce qui garde la lecture rapide alors que
        le lexique a 1 433 couples.
        """
        t = normalise_forme(texte)
        if not t:
            return None
        toks = t.split()
        compteur: Counter[str] = Counter()
        for n in range(1, 5):
            for i in range(len(toks) - n + 1):
                forme = " ".join(toks[i:i + n])
                for langue in self._detection.get(forme, ()):
                    compteur[langue] += 1
        for forme, langues in self._detection.items():
            if " " not in forme and len(forme) >= 2 and any(ord(c) > 127 for c in forme) \
                    and forme in t:
                for langue in langues:
                    compteur[langue] += 1
        if not compteur:
            return None
        (langue, n), = compteur.most_common(1)
        return langue if n >= 1 else None

    def jeu(self, texte: str) -> tuple[str, float] | None:
        """Le jeu nommé dans le texte, s'il l'est."""
        ms = self.cherche("jeu.nom", texte)
        if not ms:
            return None
        # le libellé le plus long est le plus spécifique
        m = max(ms, key=lambda x: (len(x.forme), -x.position))
        jeu = "cartes" if m.valeur == "whist" else m.valeur
        return jeu, 0.9

    # ------------------------------------------------------------------
    def formes(self, concept: str, langue: str) -> list[str]:
        return list(self.concepts.get(concept, {}).get("labels", {}).get(langue, []))

    def langues_du_concept(self, concept: str) -> list[str]:
        return sorted(self.concepts.get(concept, {}).get("labels", {}))

    def concepts_de_langue(self, langue: str) -> list[str]:
        return sorted(c for c, v in self.concepts.items() if langue in v.get("labels", {}))

    def permute(self, decalage: int = 1) -> "Multilingue":
        """Une copie où les libellés sont **décalés** entre concepts du même domaine.

        C'est le contrôle négatif : les mêmes formes, mais associées au mauvais
        sens. La couverture doit s'effondrer ; si elle ne bouge pas, c'est que la
        mesure ne lit pas le sens.
        """
        import copy
        data = copy.deepcopy(self.donnees)
        groupes: dict[str, list[str]] = defaultdict(list)
        for concept in data["concepts"]:
            domaine, _ = _domaine_valeur(concept)
            groupes[domaine].append(concept)
        for concepts in groupes.values():
            labels = [data["concepts"][c].get("labels", {}) for c in concepts]
            for i, c in enumerate(concepts):
                data["concepts"][c]["labels"] = labels[(i + decalage) % len(labels)]
        return Multilingue.depuis_donnees(data)

    def couverture(self) -> dict:
        """La matrice langues × concepts, et les langues « fortes »."""
        par_langue = {l: 0 for l in self.langues}
        par_concept = {}
        for c, v in self.concepts.items():
            n = len(v.get("labels", {}))
            par_concept[c] = n
            for l in v.get("labels", {}):
                if l in par_langue:
                    par_langue[l] += 1
        # une langue « forte » a de quoi dire une pièce d'échecs (N et P) et
        # au moins un rang de carte + une enseigne.
        fortes = []
        for l in self.langues:
            a = bool(self.formes("echecs.piece.N", l)) and bool(self.formes("echecs.piece.P", l))
            b = (bool(self.formes("cartes.rang.14", l)) or bool(self.formes("cartes.rang.13", l))) \
                and any(bool(self.formes(f"cartes.couleur.{s}", l)) for s in "CDHS")
            if a and b:
                fortes.append(l)
        return {
            "langues": len(self.langues),
            "concepts": len(self.concepts),
            "couples": sum(par_concept.values()),
            "par_concept": par_concept,
            "par_langue": par_langue,
            "moyenne_concepts_par_langue": round(sum(par_langue.values()) / len(self.langues), 2),
            "langues_fortes": fortes,
            "n_langues_fortes": len(fortes),
        }


MULTI = Multilingue()
