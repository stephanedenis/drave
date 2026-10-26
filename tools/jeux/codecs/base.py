#!/usr/bin/env python3
"""base.py — le contrat d'un codec de jeu : surface ⇄ RSN.

Un codec est la **couche linguistique** d'un jeu. Il expose deux opérations et
une mesure :

- `lit(surface, niveau)` : de la surface vers une `Lecture` (les quatre couches
  + la RSN + les candidats) ;
- `rend(rsn, format)` : de la RSN vers une surface (la restitution) ;
- `detecte(surface)` : la confiance que cette surface parle de ce jeu.

Les niveaux sont **cumulatifs** : 0 ne lit que la forme canonique exacte, 1
ajoute la normalisation, 2 le lexique, 3 la grammaire des phrases, 4 la
sémantique (légalité, désambiguïsation, canonicalisation). L'ablation de
`mesure.py` vérifie que la couverture ne baisse pas quand on monte.
"""
from __future__ import annotations

import re

from dataclasses import dataclass, field
from typing import Any, Iterable

from ..grammaire import Jeton, jetons, naturel
from ..lexique import langue_probable
from ..lexique_multilingue import MULTI
from ..rsn import Annotation, RSN

NIVEAUX = {
    0: "surface (forme canonique exacte)",
    1: "normalisation (casse, espaces, ponctuation)",
    2: "lexique (synonymes, FR/EN)",
    3: "grammaire (phrases, ordre libre)",
    4: "sémantique (légalité, désambiguïsation, canonicalisation)",
}


@dataclass(frozen=True)
class Arbre:
    """L'arbre syntaxique, volontairement générique.

    Chaque codec nomme son genre (`coup_echecs`, `etat_go`, `carte`…) et ses
    champs. Un champ absent vaut `None` : c'est ainsi que la grammaire dit
    « la surface ne le précise pas » sans inventer.
    """

    genre: str
    champs: tuple[tuple[str, Any], ...] = ()

    def champ(self, nom: str, defaut: Any = None) -> Any:
        for k, v in self.champs:
            if k == nom:
                return v
        return defaut

    def avec(self, **nouveaux) -> "Arbre":
        d = dict(self.champs)
        d.update(nouveaux)
        return Arbre(self.genre, tuple(sorted(d.items())))

    def vers_dict(self) -> dict:
        return {"genre": self.genre, **{k: v for k, v in self.champs}}


@dataclass
class Lecture:
    """Le résultat d'une lecture : toutes les couches restent visibles.

    `rsn` est la seule chose que l'étage 2 consomme. Les autres champs servent à
    mesurer, annoter et diagnostiquer — jamais à décider d'un coup.
    """

    jeu: str
    surface: str
    niveau: int
    normalise: str
    unites: list[Jeton] = field(default_factory=list)
    arbre: Arbre | None = None
    rsn: RSN | None = None
    candidats: list[RSN] = field(default_factory=list)
    erreurs: list[str] = field(default_factory=list)
    format: str = "inconnu"
    langue: str = "inconnue"
    confiance: float = 0.0
    ambiguites: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return self.rsn is not None and not self.erreurs

    def vers_dict(self) -> dict:
        return {
            "jeu": self.jeu, "surface": self.surface, "niveau": self.niveau,
            "format": self.format, "langue": self.langue,
            "confiance": round(self.confiance, 4),
            "ambiguites": list(self.ambiguites),
            "arbre": self.arbre.vers_dict() if self.arbre else None,
            "rsn": self.rsn.vers_dict() if self.rsn else None,
            "erreurs": list(self.erreurs),
            "candidats": [c.resume() for c in self.candidats],
        }


class Codec:
    """La base : un codec déclare son jeu, ses formats et ses motifs."""

    jeu: str = "?"
    formats: tuple[str, ...] = ("canonique",)

    # ---- à implémenter par chaque codec --------------------------------
    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
            langue: str | None = None) -> Lecture:
        raise NotImplementedError

    def rend(self, rsn: RSN, format: str = "canonique", langue: str = "fr",
             contexte: RSN | None = None) -> str:
        raise NotImplementedError

    def detecte(self, texte: str) -> float:
        return 0.0

    # ---- aides communes ------------------------------------------------
    def sans_nom_jeu(self, texte: str) -> str:
        """Retire un nom de jeu en tête (« шахматы конь g1 f3 » → « конь g1 f3 »).

        Les libellés viennent du lexique multilingue ; le retrait est fait sur la
        forme normalisée du libellé, avec des séparateurs souples (tiret, espace,
        apostrophe). On ne retire que si le reste n'est pas vide.
        """
        ms = MULTI.cherche("jeu.nom", texte)
        if not ms:
            return texte
        m = max(ms, key=lambda x: len(x.forme))
        motif = r"[\W_]+".join(re.escape(p) for p in m.forme.split())
        nouveau = re.sub(motif, " ", texte, count=1, flags=re.I)
        return nouveau if nouveau.strip() else texte

    def lecture(self, texte: str, niveau: int, langue: str | None = None,
                format: str = "inconnu") -> Lecture:
        lang = langue or langue_probable(texte)[0]
        if lang in ("inconnue", "notation"):
            ml = MULTI.detecte_langue(texte)
            if ml:
                lang = ml
        return Lecture(self.jeu, texte, niveau, naturel(texte), jetons(texte),
                       format=format, langue=lang)

    def annotation(self, lecture: Lecture, rsn: RSN | None = None,
                   confiance: float | None = None, ambiguites: Iterable[str] = ()) -> Annotation:
        return Annotation(langue=lecture.langue, format=lecture.format,
                          confiance=lecture.confiance if confiance is None else confiance,
                          ambiguites=tuple(dict.fromkeys((*lecture.ambiguites, *ambiguites))),
                          surface=lecture.surface, niveau=lecture.niveau)

    def echoue(self, lecture: Lecture, message: str) -> Lecture:
        lecture.erreurs.append(message)
        lecture.confiance = 0.0
        return lecture

    def reussi(self, lecture: Lecture, rsn: RSN, format: str | None = None,
               confiance: float = 1.0, ambiguites: Iterable[str] = ()) -> Lecture:
        lecture.format = format or lecture.format
        lecture.confiance = confiance
        lecture.ambiguites = tuple(dict.fromkeys((*lecture.ambiguites, *ambiguites)))
        rsn = rsn.avec_annotation(langue=lecture.langue, format=lecture.format,
                                  confiance=confiance,
                                  ambiguites=lecture.ambiguites,
                                  surface=lecture.surface, niveau=lecture.niveau)
        lecture.rsn = rsn
        return lecture


# ---------------------------------------------------------------------------
# Le registre : un codec par jeu, importé à la demande (pas de cycle).
# ---------------------------------------------------------------------------
_CACHE: dict[str, Codec] = {}
_NOMS = ("morpion", "echecs", "dames", "go", "cartes")


def codec(jeu: str) -> Codec:
    if jeu not in _NOMS:
        raise KeyError(f"jeu inconnu : {jeu!r} (connus : {', '.join(_NOMS)})")
    if jeu not in _CACHE:
        module = __import__(f"{__package__}.{jeu}", fromlist=["CODEC"])
        _CACHE[jeu] = module.CODEC
    return _CACHE[jeu]


def tous_les_codecs() -> dict[str, Codec]:
    return {j: codec(j) for j in _NOMS}


def lit(texte: str, jeu: str | None = None, niveau: int = 4,
        contexte: RSN | None = None, langue: str | None = None) -> Lecture:
    """Lit une surface ; si `jeu` est absent, choisit le codec le plus confiant.

    La détection est **explicite** : on garde le jeu candidat et la confiance
    dans la `Lecture`. Un texte ambigu (une case `e4` seule) n'est pas deviné au
    hasard : il est lu par le jeu demandé, ou refusé avec les candidats nommés.
    """
    if jeu is not None:
        return codec(jeu).lit(texte, niveau=niveau, contexte=contexte, langue=langue)
    scores = {j: c.detecte(texte) for j, c in tous_les_codecs().items()}
    meilleur = max(scores, key=lambda j: scores[j])
    if scores[meilleur] <= 0.0:
        # Dernier recours : le codec qui arrive à lire sans erreur, le plus confiant.
        lectures = []
        for j, c in tous_les_codecs().items():
            l = c.lit(texte, niveau=niveau, contexte=contexte, langue=langue)
            if l.ok:
                lectures.append((l.confiance, j, l))
        if not lectures:
            return Lecture("?", texte, niveau, naturel(texte), jetons(texte),
                           erreurs=[f"aucun codec ne lit {texte!r}"])
        return max(lectures, key=lambda x: x[0])[2]
    return codec(meilleur).lit(texte, niveau=niveau, contexte=contexte, langue=langue)


def rend(rsn: RSN, format: str = "canonique", langue: str = "fr",
         contexte: RSN | None = None) -> str:
    return codec(rsn.jeu).rend(rsn, format=format, langue=langue, contexte=contexte)


def detecte_jeu(texte: str) -> tuple[str, float]:
    # Les codecs d'abord (notation, vocabulaire), puis les noms de jeux
    # multilingues. Le nom d'un jeu ne doit pas écraser une notation plus
    # spécifique : « dame de cœur » nomme une carte, pas les dames.
    scores = {j: c.detecte(texte) for j, c in tous_les_codecs().items()}
    jeu = MULTI.jeu(texte)
    if jeu is not None:
        scores[jeu[0]] = max(scores.get(jeu[0], 0.0), jeu[1])
    j = max(scores, key=lambda k: scores[k])
    return j, scores[j]
