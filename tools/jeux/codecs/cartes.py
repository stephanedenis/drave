#!/usr/bin/env python3
"""codecs.cartes — la surface des cartes : « as de cœur », « A♥ », une donne.

Le jeu de cartes est le témoin de l'**information imparfaite** : la RSN porte
les quatre mains (parce que l'étage 2 en a besoin pour la mesure et la
simulation), mais une **action** ne porte qu'une carte — le joueur est celui qui
a le trait. Les surfaces reconnues sont le nom court (`A♥`, `AS`, `10H`), le nom
français (`as de cœur`), le nom anglais (`ace of hearts`), la liste de cartes
d'une main, et la **donne** canonique (`whist atout=H … | N:… | E:…`).

Le codec ne distribue pas : une donne se crée par `regles.cartes.Position.depart`
(graine reproductible). Il lit et rend des états, il ne les invente pas.
"""
from __future__ import annotations

import re

from ..grammaire import naturel
from ..lexique import LEX
from ..lexique_multilingue import MULTI
from ..rsn import Annotation, RSN
from ..regles import cartes as C
from .base import Arbre, Codec, Lecture

_RANGS_TXT = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
              "10": 10, "t": 10, "j": 11, "q": 12, "k": 13, "a": 14}
_COULEURS_TXT = {"c": 0, "d": 1, "h": 2, "s": 3,
                 "\u2663": 0, "\u2666": 1, "\u2665": 2, "\u2660": 3}
_RE_COURT = re.compile(r"(?<![A-Za-z0-9])(10|[2-9TJQKA])[-]?([cdhsCDHS\u2663\u2666\u2665\u2660])(?![A-Za-z0-9])")
_MOTS_RANG = {
    "as": 14, "ace": 14, "roi": 13, "king": 13, "dame": 12, "reine": 12,
    "queen": 12, "valet": 11, "jack": 11, "dix": 10, "ten": 10,
    "neuf": 9, "nine": 9, "huit": 8, "eight": 8, "sept": 7, "seven": 7,
    "six": 6, "cinq": 5, "five": 5, "quatre": 4, "four": 4,
    "trois": 3, "three": 3, "deux": 2, "two": 2,
}
_MOTS_COULEUR = {
    "trefle": 0, "trefles": 0, "club": 0, "clubs": 0,
    "carreau": 1, "carreaux": 1, "diamond": 1, "diamonds": 1,
    "coeur": 2, "coeurs": 2, "heart": 2, "hearts": 2,
    "pique": 3, "piques": 3, "spade": 3, "spades": 3,
}
_RE_LONGUE = re.compile(
    r"\b(" + "|".join(sorted(_MOTS_RANG, key=len, reverse=True)) + r")\b"
    r"(?:\s+(?:de|du|of|des))?\s+"
    r"\b(" + "|".join(sorted(_MOTS_COULEUR, key=len, reverse=True)) + r")\b")
_RE_JOUEUR = re.compile(r"\b([nesw]|nord|est|sud|ouest|north|east|south|west)\b", re.I)
_JOUEURS = {"n": 0, "nord": 0, "north": 0, "e": 1, "est": 1, "east": 1,
            "s": 2, "sud": 2, "south": 2, "w": 3, "ouest": 3, "west": 3}


def _carte(r: int, c: int) -> int:
    return C.carte_id(r, c)


def _toutes_les_cartes(texte: str) -> list[tuple[int, int]]:
    """Toutes les cartes d'une surface, avec leur position (pour l'ordre)."""
    t = texte
    trouvees: list[tuple[int, int]] = []
    # noms longs d'abord (ils contiennent parfois une lettre de rang)
    for m in _RE_LONGUE.finditer(naturel(t)):
        r = _MOTS_RANG[m.group(1)]
        c = _MOTS_COULEUR[m.group(2)]
        trouvees.append((m.start(), _carte(r, c)))
    # noms courts
    for m in _RE_COURT.finditer(t):
        r = _RANGS_TXT[m.group(1).lower()]
        c = _COULEURS_TXT[m.group(2).lower()]
        pos = m.start()
        # évite de compter deux fois un nom long déjà trouvé
        if any(abs(pos - p) <= 2 for p, _ in trouvees):
            continue
        trouvees.append((pos, _carte(r, c)))
    # Le multilingue ne sert que s'il n'y a AUCUNE carte déjà lue : sur une
    # liste, l'appariement rang/enseigne par proximité fabriquerait des cartes
    # croisées. Les listes restent FR/EN (ou en notation) ; une carte isolée
    # dans n'importe laquelle des 53 langues est couverte.
    if not trouvees:
        for pos, carte in _cartes_multilingues(t):
            if carte not in [c for _, c in trouvees]:
                trouvees.append((pos, carte))
    trouvees.sort()
    return trouvees


def _cartes_multilingues(texte: str) -> list[tuple[int, int]]:
    """Les cartes d'une surface multilingue (rang + enseigne), par proximité.

    Les libellés Wikidata sont des **lemmes** : « tuз » (as), « черви » (cœurs).
    On apparie chaque rang avec l'enseigne la plus proche ; les rangs 2-10 sont
    acceptés en chiffres, ce qui rend les basses cartes couvertes dès qu'une
    enseigne est connue.
    """
    rangs = [(m.position, m.valeur) for m in MULTI.cherche("cartes.rang", texte)]
    for m in re.finditer(r"(?<!\d)(10|[2-9])(?!\d)", texte):
        rangs.append((m.start(), m.group(1)))
    couleurs = [(m.position, m.valeur) for m in MULTI.cherche("cartes.couleur", texte)]
    if not rangs or not couleurs:
        return []
    rangs.sort()
    couleurs.sort()
    sortie: list[tuple[int, int]] = []
    libres = list(couleurs)
    for pos, r in rangs:
        if not libres:
            break
        c = min(libres, key=lambda x: abs(x[0] - pos))
        libres.remove(c)
        try:
            sortie.append((min(pos, c[0]), C.carte_id(int(r), "CDHS".index(c[1]))))
        except (ValueError, IndexError):
            continue
    return sortie


def _carte_unique(texte: str) -> int | None:
    cs = _toutes_les_cartes(texte)
    return cs[0][1] if len(cs) == 1 else None


def _lit_joueur(s: str) -> int:
    s = s.strip().lower()
    if s in _JOUEURS:
        return _JOUEURS[s]
    if s.isdigit() and 0 <= int(s) < 4:
        return int(s)
    raise C.ErreurCartes(f"joueur inconnu : {s!r}")


def _est_etat(texte: str) -> bool:
    t = texte.strip()
    return bool(re.search(r"(?:^|\|)\s*[NESWnesw]\s*:", t)
                or re.search(r"\bwhist\b", t, re.I)
                or re.search(r"\batout\s*=", t, re.I)
                or re.search(r"\bdonne\b", t, re.I))


# ---------------------------------------------------------------------------
class CodecCartes(Codec):
    jeu = "cartes"
    formats = ("donne", "mains", "carte", "francais", "anglais", "liste")

    # ------------------------------------------------------------------
    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
            langue: str | None = None) -> Lecture:
        lec = self.lecture(texte, niveau, langue)
        if not texte or not texte.strip():
            return self.echoue(lec, "surface vide")

        # 1. donne / état
        if _est_etat(texte):
            try:
                pos = self._lit_donne(texte, niveau)
            except Exception as e:
                return self.echoue(lec, f"donne invalide : {e}")
            lec.format = "donne"
            lec.arbre = Arbre("etat_cartes", (("mains", tuple(tuple(m) for m in pos.mains)),
                                              ("atout", pos.atout)))
            return self.reussi(lec, C.rsn_depuis_position(pos), "donne", 1.0)

        # 2. une carte = une action
        cartes = _toutes_les_cartes(texte)
        if len(cartes) == 1:
            carte = cartes[0][1]
            # niveau 0 : forme courte exacte (A♥, AS, 10H) ; le nom long est niveau 2
            if niveau < 2 and _RE_LONGUE.search(naturel(texte)) and not _RE_COURT.fullmatch(texte.strip()):
                return self.echoue(lec, "nom long : niveau 2")
            if contexte is not None and niveau >= 4:
                try:
                    pos = C.position_depuis_rsn(contexte)
                    if not pos.coup_legal(carte):
                        return self.echoue(lec, f"coup illégal : {C.nom_court(carte)}")
                except Exception as e:
                    return self.echoue(lec, f"position de contexte invalide : {e}")
            lec.format = "carte"
            lec.arbre = Arbre("coup_cartes", (("carte", carte),))
            return self.reussi(lec, C.action_depuis_carte(carte), "carte", 0.95,
                               [] if contexte is not None or niveau < 4 else ["position requise pour valider"])

        # 3. plusieurs cartes = une main (ou une donne partielle)
        if len(cartes) >= 2:
            if niveau < 1:
                return self.echoue(lec, "liste de cartes : niveau 1")
            if niveau < 2 and _RE_LONGUE.search(naturel(texte)):
                return self.echoue(lec, "noms longs : niveau 2")
            cs = sorted({c for _, c in cartes})
            if len(cs) != len({c for _, c in cartes}):
                return self.echoue(lec, "carte en double dans la main")
            lec.format = "liste"
            lec.arbre = Arbre("main_cartes", (("cartes", tuple(cs)),))
            return self.reussi(lec, RSN("cartes", "main", {"cartes": cs}), "liste", 0.9)

        return self.echoue(lec, "aucune lecture de cartes")

    # ------------------------------------------------------------------
    def _lit_donne(self, texte: str, niveau: int) -> C.Position:
        t = re.sub(r"\s+", " ", texte.strip())
        # en-tête et segments
        segments = [s.strip() for s in re.split(r"[|]", t) if s.strip()]
        entete = segments[0] if segments else t
        atout = -1
        m = re.search(r"atout\s*[=:]\s*([cdhs\u2663\u2666\u2665\u2660]|trefle|coeur|carreau|pique|club|heart|diamond|spade|-)",
                      entete, re.I)
        if m and m.group(1) != "-":
            v = m.group(1).lower()
            atout = _COULEURS_TXT.get(v)
            if atout is None:
                atout = _MOTS_COULEUR.get(v, -1)
        donneur = 0
        m = re.search(r"donneur\s*[=:]\s*([nesw0-3]|nord|est|sud|ouest)", entete, re.I)
        if m:
            donneur = _lit_joueur(m.group(1))
        entameur = 0
        m = re.search(r"entame(?:ur)?\s*[=:]\s*([nesw0-3]|nord|est|sud|ouest)", entete, re.I)
        if m:
            entameur = _lit_joueur(m.group(1))
        plis = [0, 0]
        m = re.search(r"plis\s*[=:]\s*(\d+)\s*[,;-]\s*(\d+)", entete, re.I)
        if m:
            plis = [int(m.group(1)), int(m.group(2))]
        tour = None
        m = re.search(r"tour\s*[=:]\s*([nesw0-3]|nord|est|sud|ouest)", entete, re.I)
        if m:
            tour = _lit_joueur(m.group(1))

        mains: list[list[int]] = [[], [], [], []]
        pli: list[list[int]] = []
        for seg in segments[1:] + ([entete] if len(segments) == 1 else []):
            mh = re.match(r"([NESWnesw])\s*[=:]\s*(.*)", seg)
            if mh and not re.match(r"(?:atout|donneur|entame|tour|plis)\b", seg, re.I):
                j = _lit_joueur(mh.group(1))
                mains[j] = [c for _, c in _toutes_les_cartes(mh.group(2))]
                continue
            mp = re.match(r"pli\s*[=:]?\s*(.*)", seg, re.I)
            if mp:
                reste = mp.group(1)
                for m2 in re.finditer(r"([NESW])\s*:\s*([^\s,;]+)", reste, re.I):
                    j = _lit_joueur(m2.group(1))
                    cs = _toutes_les_cartes(m2.group(2))
                    if cs:
                        pli.append([j, cs[0][1]])
        # un tour explicite, sinon déduit
        if tour is None:
            tour = (entameur + len(pli)) % 4
        pos = C.Position(mains, atout, donneur, entameur, tour, pli, plis)
        if niveau >= 4:
            if pos.terminal():
                return pos
            if len(pli) > 0 and len(pli) != (tour - entameur) % 4:
                # le nombre de cartes du pli doit correspondre au tour
                pass
            if not pos.mains[pos.tour] and not pos.terminal():
                raise C.ErreurCartes("le joueur au trait n'a pas de carte")
        return pos

    # ------------------------------------------------------------------
    def rend(self, rsn: RSN, format: str = "canonique", langue: str = "fr",
             contexte: RSN | None = None) -> str:
        if rsn.jeu != "cartes":
            raise ValueError("ce n'est pas une RSN de cartes")
        if rsn.nature == "etat":
            pos = C.position_depuis_rsn(rsn, valide=False)
            if format in ("donne", "canonique"):
                atout = C.COULEURS[pos.atout] if pos.atout >= 0 else "-"
                entete = (f"whist atout={atout} donneur={C.NOMS_JOUEURS[pos.donneur]} "
                          f"entame={C.NOMS_JOUEURS[pos.entameur]} tour={C.NOMS_JOUEURS[pos.tour]} "
                          f"plis={pos.plis[0]},{pos.plis[1]}")
                mains = " | ".join(
                    f"{C.NOMS_JOUEURS[j]}: " + " ".join(C.nom_court(c) for c in pos.mains[j])
                    for j in range(4))
                pli = ""
                if pos.pli:
                    pli = " | pli=" + " ".join(f"{C.NOMS_JOUEURS[j]}:{C.nom_court(c)}"
                                                for j, c in pos.pli)
                return entete + " | " + mains + pli
            if format == "mains":
                return "\n".join(
                    f"{C.NOMS_JOUEURS[j]}: " + " ".join(C.nom_carte(c, langue) for c in pos.mains[j])
                    for j in range(4))
            if format == "diagramme":
                return "\n".join(
                    f"{C.NOMS_JOUEURS[j]}: " + " ".join(C.nom_court(c) for c in pos.mains[j])
                    for j in range(4))
            raise ValueError(f"format d'état inconnu : {format}")
        if rsn.nature == "coup":
            carte = int(rsn.corps["carte"])
            if format in ("carte", "canonique"):
                return C.nom_court(carte)
            if format == "francais":
                return C.nom_carte(carte, "fr")
            if format == "anglais":
                return C.nom_carte(carte, "en")
            raise ValueError(f"format de coup inconnu : {format}")
        if rsn.nature == "main":
            cs = [int(c) for c in rsn.corps["cartes"]]
            if format in ("liste", "canonique"):
                return " ".join(C.nom_court(c) for c in cs)
            if format == "francais":
                return ", ".join(C.nom_carte(c, "fr") for c in cs)
            if format == "anglais":
                return ", ".join(C.nom_carte(c, "en") for c in cs)
            raise ValueError(f"format de main inconnu : {format}")
        if rsn.nature == "partie":
            _, coups = C.partie_depuis_rsn(rsn)
            return " ".join(C.nom_court(c) for c in coups)
        raise ValueError(f"nature inconnue : {rsn.nature}")

    # ------------------------------------------------------------------
    def detecte(self, texte: str) -> float:
        t = texte.lower()
        if "whist" in t or "cartes" in t or "cards" in t:
            return 0.9
        if _est_etat(texte):
            return 0.95
        cs = _toutes_les_cartes(texte)
        if cs:
            if any(c in "\u2660\u2665\u2666\u2663" for c in texte):
                return 0.7
            if _RE_LONGUE.search(naturel(texte)):
                return 0.95
            if len(cs) >= 2:
                return 0.9
            return 0.35
        return 0.0


CODEC = CodecCartes()
