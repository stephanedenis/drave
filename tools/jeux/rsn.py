#!/usr/bin/env python3
"""rsn.py — la représentation sémantique neutre d'un jeu (RSN-jeu).

POURQUOI CE MODULE. L'étage 1 de Drave transforme une **surface** (du texte, une
notation, un diagramme) en **sens** ; l'étage 2 raisonne sur ce sens. Pour les
jeux symboliques, le sens est un **état** (la position, le trait, les droits) et
une **action** (un coup, une carte jouée, une passe). Ce module définit le
**contrat** entre les deux étages :

    surface ──(couches linguistiques)──► RSN-jeu ──(pensée)──► décision

Caractéristiques du contrat, et chacune est mesurée par `mesure.py` :

1. **canonique** : deux surfaces qui disent la même chose donnent le MÊME corps
   (donc la même empreinte), même si la langue, la notation ou la confiance
   changent ;
2. **séparable** : l'annotation (langue, confiance, ambiguïtés, surface) n'entre
   PAS dans l'empreinte — le bruit est porté, pas confondu avec le sens ;
3. **compact** : un encodage binaire (`RSNB`) est disponible en plus du JSON
   canonique, pour mesurer le coût du contrat ;
4. **réversible** : tout corps encodé se décode à l'identique (test de
   round-trip), et tout état se rend en surface par le codec du jeu ;
5. **typé** : le corps est un arbre de `null` / `bool` / `int` / `str` / liste /
   dictionnaire. Aucun flottant : les valeurs décimales (komi) sont en dixièmes,
   pour que l'empreinte ne dépende pas d'un arrondi de machine.

Vocabulaire : les éléments du corps sont des **unités de sens** (une case, un
trait, une carte), jamais des « jetons » — le jeton est l'unité technique du
tokeniseur, pas celle de la RSN.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, replace
from typing import Any, Iterable, Mapping

VERSION = 1
JEUX = ("morpion", "echecs", "dames", "go", "cartes")
NATURES = ("etat", "coup", "partie", "main", "resultat", "requete")

# Un corps est un arbre JSON **restreint** : pas de flottants, pas de tuples
# (ils seraient sérialisés en listes et l'aller-retour changerait le type).
TypesCorps = (type(None), bool, int, str, list, dict)


class ErreurRSN(ValueError):
    """Le corps viole le contrat (type interdit, clé non textuelle, etc.)."""


def _verifie(corps: Any, chemin: str = "corps") -> None:
    """Vérifie récursivement le contrat de type, en nommant le chemin fautif."""
    if isinstance(corps, bool) or corps is None or isinstance(corps, int) or isinstance(corps, str):
        return
    if isinstance(corps, float):
        raise ErreurRSN(f"{chemin} : flottant interdit (un dixième entier, p. ex. komi=65)")
    if isinstance(corps, (list, tuple)):
        for i, v in enumerate(corps):
            _verifie(v, f"{chemin}[{i}]")
        return
    if isinstance(corps, Mapping):
        for k, v in corps.items():
            if not isinstance(k, str):
                raise ErreurRSN(f"{chemin} : clé non textuelle {k!r}")
            _verifie(v, f"{chemin}.{k}")
        return
    raise ErreurRSN(f"{chemin} : type interdit {type(corps).__name__}")


def canonise(corps: Any) -> Any:
    """Normalise un corps : tuples → listes, dictionnaires triés, pas de flottant.

    Les dictionnaires sont reconstruits dans l'ordre trié des clés ; c'est ce qui
    rend le JSON et l'encodage binaire **déterministes** (deux corps sémantiquement
    égaux donnent exactement les mêmes octets, quel que soit l'ordre d'insertion).
    """
    if corps is None or isinstance(corps, (bool, int, str)):
        return corps
    if isinstance(corps, float):
        raise ErreurRSN("flottant interdit dans un corps canonique")
    if isinstance(corps, (list, tuple)):
        return [canonise(v) for v in corps]
    if isinstance(corps, Mapping):
        return {str(k): canonise(corps[k]) for k in sorted(corps, key=str)}
    raise ErreurRSN(f"type interdit {type(corps).__name__}")


@dataclass(frozen=True)
class Annotation:
    """Le bruit de la surface, gardé À CÔTÉ du sens (jamais dans l'empreinte).

    - `langue` : « fr », « en », ou « notation » pour une notation formelle ;
    - `format` : « san », « uci », « fen », « gtp », « donne »…
    - `confiance` : 0..1, la confiance de la lecture de surface ;
    - `ambiguites` : ce que la surface ne tranche pas (« R » = roi ou tour ?) ;
    - `surface` : le texte d'origine, pour le miroir et le diagnostic ;
    - `niveau` : la couche linguistique qui a produit la lecture (0..4).
    """

    langue: str = "inconnue"
    format: str = "inconnu"
    confiance: float = 1.0
    ambiguites: tuple[str, ...] = ()
    surface: str = ""
    niveau: int = 4

    def avec(self, **champs) -> "Annotation":
        return replace(self, **champs)

    def vers_dict(self) -> dict:
        return {
            "langue": self.langue,
            "format": self.format,
            "confiance": round(float(self.confiance), 4),
            "ambiguites": list(self.ambiguites),
            "surface": self.surface,
            "niveau": int(self.niveau),
        }


@dataclass(frozen=True)
class RSN:
    """Une unité de sens d'un jeu : jeu + nature + corps canonique + annotation."""

    jeu: str
    nature: str
    corps: dict = field(default_factory=dict)
    annotation: Annotation = field(default_factory=Annotation)

    def __post_init__(self) -> None:
        if self.jeu not in JEUX:
            raise ErreurRSN(f"jeu inconnu : {self.jeu!r} (connus : {', '.join(JEUX)})")
        if self.nature not in NATURES:
            raise ErreurRSN(f"nature inconnue : {self.nature!r} (connues : {', '.join(NATURES)})")
        _verifie(self.corps)
        object.__setattr__(self, "corps", canonise(self.corps))

    # ---- le contrat -----------------------------------------------------
    def canonique(self) -> dict:
        """Le sens seul : version, jeu, nature, corps trié. Pas d'annotation."""
        return {"version": VERSION, "jeu": self.jeu, "nature": self.nature, "corps": self.corps}

    def octets_json(self) -> bytes:
        """JSON canonique : séparateurs fixes, clés triées, UTF-8."""
        return json.dumps(self.canonique(), ensure_ascii=False, sort_keys=True,
                          separators=(",", ":")).encode("utf-8")

    def texte_json(self) -> str:
        return self.octets_json().decode("utf-8")

    def empreinte(self) -> str:
        """SHA-256 du sens seul — deux surfaces équivalentes la partagent."""
        return hashlib.sha256(self.octets_json()).hexdigest()

    def empreinte_courte(self, n: int = 12) -> str:
        return self.empreinte()[:n]

    def meme_sens(self, autre: "RSN") -> bool:
        return self.jeu == autre.jeu and self.nature == autre.nature and self.empreinte() == autre.empreinte()

    def avec(self, *, corps: Mapping | None = None, annotation: Annotation | None = None) -> "RSN":
        return RSN(self.jeu, self.nature, dict(self.corps) if corps is None else dict(corps),
                   self.annotation if annotation is None else annotation)

    def avec_annotation(self, **champs) -> "RSN":
        return self.avec(annotation=self.annotation.avec(**champs))

    # ---- l'encodage compact (RSNB) --------------------------------------
    def octets_binaire(self) -> bytes:
        return encode_binaire(self)

    def octets_binaire_avec_annotation(self) -> bytes:
        return encode_binaire(self, avec_annotation=True)

    # ---- lisibilité ------------------------------------------------------
    def resume(self) -> str:
        return f"{self.jeu}/{self.nature}/{self.empreinte_courte(8)}"

    def vers_dict(self) -> dict:
        return {"jeu": self.jeu, "nature": self.nature, "corps": self.corps,
                "annotation": self.annotation.vers_dict(), "empreinte": self.empreinte()}

    @classmethod
    def depuis_dict(cls, d: Mapping) -> "RSN":
        ann = d.get("annotation") or {}
        return cls(str(d["jeu"]), str(d["nature"]), dict(d["corps"]),
                   Annotation(langue=str(ann.get("langue", "inconnue")),
                              format=str(ann.get("format", "inconnu")),
                              confiance=float(ann.get("confiance", 1.0)),
                              ambiguites=tuple(ann.get("ambiguites", ())),
                              surface=str(ann.get("surface", "")),
                              niveau=int(ann.get("niveau", 4))))


# ---------------------------------------------------------------------------
# RSNB — un encodage binaire compact, générique et réversible.
#
# Ce n'est pas un format de transport (le moteur a DRVF pour ça) : c'est la
# mesure du **coût du contrat sémantique**. Les entiers sont en zigzag-varint,
# les longueurs en varint, les dictionnaires dans l'ordre trié des clés. Le
# décodage ne devine rien : chaque octet est un tag.
# ---------------------------------------------------------------------------
_MAGIE = b"RSNB"
_T_NUL, _T_FAUX, _T_VRAI, _T_ENT, _T_TXT, _T_LISTE, _T_DICT = range(7)


def _varint(n: int) -> bytes:
    if n < 0:
        raise ErreurRSN("varint négatif")
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def _lit_varint(buf: bytes, i: int) -> tuple[int, int]:
    n = 0
    dec = 0
    while True:
        if i >= len(buf):
            raise ErreurRSN("RSNB tronqué (varint)")
        b = buf[i]
        i += 1
        n |= (b & 0x7F) << dec
        if not b & 0x80:
            return n, i
        dec += 7
        if dec > 63:
            raise ErreurRSN("varint trop long")


def _zigzag(n: int) -> int:
    return (n << 1) if n >= 0 else ((-n << 1) - 1)


def _dezigzag(n: int) -> int:
    return (n >> 1) if not n & 1 else -((n + 1) >> 1)


def _encode_valeur(v: Any, out: bytearray) -> None:
    if v is None:
        out.append(_T_NUL)
    elif v is False:
        out.append(_T_FAUX)
    elif v is True:
        out.append(_T_VRAI)
    elif isinstance(v, int):
        out.append(_T_ENT)
        out += _varint(_zigzag(v))
    elif isinstance(v, str):
        b = v.encode("utf-8")
        out.append(_T_TXT)
        out += _varint(len(b))
        out += b
    elif isinstance(v, (list, tuple)):
        out.append(_T_LISTE)
        out += _varint(len(v))
        for x in v:
            _encode_valeur(x, out)
    elif isinstance(v, Mapping):
        out.append(_T_DICT)
        out += _varint(len(v))
        for k in sorted(v, key=str):
            if not isinstance(k, str):
                raise ErreurRSN("clé non textuelle dans RSNB")
            _encode_valeur(k, out)
            _encode_valeur(v[k], out)
    else:
        raise ErreurRSN(f"type interdit dans RSNB : {type(v).__name__}")


def _decode_valeur(buf: bytes, i: int) -> tuple[Any, int]:
    if i >= len(buf):
        raise ErreurRSN("RSNB tronqué (tag)")
    tag = buf[i]
    i += 1
    if tag == _T_NUL:
        return None, i
    if tag == _T_FAUX:
        return False, i
    if tag == _T_VRAI:
        return True, i
    if tag == _T_ENT:
        n, i = _lit_varint(buf, i)
        return _dezigzag(n), i
    if tag == _T_TXT:
        n, i = _lit_varint(buf, i)
        if i + n > len(buf):
            raise ErreurRSN("RSNB tronqué (texte)")
        return buf[i:i + n].decode("utf-8"), i + n
    if tag == _T_LISTE:
        n, i = _lit_varint(buf, i)
        out = []
        for _ in range(n):
            v, i = _decode_valeur(buf, i)
            out.append(v)
        return out, i
    if tag == _T_DICT:
        n, i = _lit_varint(buf, i)
        out = {}
        for _ in range(n):
            k, i = _decode_valeur(buf, i)
            if not isinstance(k, str):
                raise ErreurRSN("RSNB : clé non textuelle")
            v, i = _decode_valeur(buf, i)
            out[k] = v
        return out, i
    raise ErreurRSN(f"RSNB : tag inconnu {tag}")


def encode_binaire(rsn: RSN, avec_annotation: bool = False) -> bytes:
    if rsn.jeu not in JEUX:
        raise ErreurRSN(f"jeu inconnu : {rsn.jeu}")
    if rsn.nature not in NATURES:
        raise ErreurRSN(f"nature inconnue : {rsn.nature}")
    out = bytearray(_MAGIE)
    out.append(VERSION)
    out.append(JEUX.index(rsn.jeu))
    out.append(NATURES.index(rsn.nature))
    _encode_valeur(rsn.corps, out)
    if avec_annotation:
        ann = rsn.annotation.vers_dict()
        ann["confiance"] = int(round(float(ann.get("confiance", 1.0)) * 1000))
        _encode_valeur(ann, out)
    else:
        out.append(0)  # marqueur « pas d'annotation »
    return bytes(out)


def decode_binaire(buf: bytes) -> RSN:
    if not buf.startswith(_MAGIE):
        raise ErreurRSN("RSNB : magie absente")
    if len(buf) < 5:
        raise ErreurRSN("RSNB : en-tête tronqué")
    version = buf[4]
    if version != VERSION:
        raise ErreurRSN(f"RSNB : version {version} inconnue (attendue {VERSION})")
    if len(buf) < 6:
        raise ErreurRSN("RSNB : en-tête tronqué")
    jeu = JEUX[buf[5]] if buf[5] < len(JEUX) else None
    if jeu is None:
        raise ErreurRSN(f"RSNB : jeu inconnu {buf[5]}")
    if len(buf) < 7:
        raise ErreurRSN("RSNB : en-tête tronqué")
    nature = NATURES[buf[6]] if buf[6] < len(NATURES) else None
    if nature is None:
        raise ErreurRSN(f"RSNB : nature inconnue {buf[6]}")
    corps, i = _decode_valeur(buf, 7)
    if not isinstance(corps, dict):
        raise ErreurRSN("RSNB : le corps doit être un dictionnaire")
    ann = Annotation()
    if i < len(buf):
        marque = buf[i]
        if marque == 0:
            i += 1
        else:
            d, i = _decode_valeur(buf, i)
            if isinstance(d, dict):
                ann = Annotation(langue=str(d.get("langue", "inconnue")),
                                 format=str(d.get("format", "inconnu")),
                                 confiance=float(d.get("confiance", 1000)) / 1000.0,
                                 ambiguites=tuple(d.get("ambiguites", ())),
                                 surface=str(d.get("surface", "")),
                                 niveau=int(d.get("niveau", 4)))
    if i != len(buf):
        raise ErreurRSN("RSNB : octets en trop après le corps")
    return RSN(jeu, nature, corps, ann)


# ---------------------------------------------------------------------------
# Diagnostic : où deux RSN diffèrent-elles ? (pour les tests et la fiche)
# ---------------------------------------------------------------------------
def differences(a: Any, b: Any, chemin: str = "corps") -> list[tuple[str, Any, Any]]:
    """Les chemins où deux corps diffèrent, avec les deux valeurs."""
    if type(a) is not type(b):
        return [(chemin or "corps", a, b)]
    if isinstance(a, Mapping):
        out = []
        for k in sorted(set(a) | set(b), key=str):
            if k not in a:
                out.append((f"{chemin}.{k}", "<absent>", b[k]))
            elif k not in b:
                out.append((f"{chemin}.{k}", a[k], "<absent>"))
            else:
                out += differences(a[k], b[k], f"{chemin}.{k}")
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [(f"{chemin}.longueur", len(a), len(b))]
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out += differences(x, y, f"{chemin}[{i}]")
        return out
    if a != b:
        return [(chemin or "corps", a, b)]
    return []


def meme_corps(a: RSN, b: RSN, ignore: Iterable[str] = ()) -> tuple[bool, list[tuple[str, Any, Any]]]:
    """Compare deux RSN en ignorant éventuellement des champs de premier niveau."""
    ca, cb = dict(a.corps), dict(b.corps)
    for k in ignore:
        ca.pop(k, None)
        cb.pop(k, None)
    d = differences(ca, cb)
    return (not d and a.jeu == b.jeu and a.nature == b.nature, d)
