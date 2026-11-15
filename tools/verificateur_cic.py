#!/usr/bin/env python3
"""verificateur_cic.py — vérificateur INDÉPENDANT du corpus d'or CIC-lite.

Le corpus d'or CIC (`nipada/falsification/corpus_dor_cic_v1.json`, Panini/Research)
est un artefact portable : 3 définitions, 21 constantes et 42 entrées (36 attendues
« accepte », 6 attendues « rejette »). Chaque entrée porte une preuve et un type
sérialisés en **de Bruijn** (octets canoniques) et une empreinte
`sha256(preuve || type)`.

La doctrine du corpus est explicite : *toute implémentation doit reproduire
exactement ces verdicts à partir de cet artefact seul*. Ce module est cette
implémentation côté Drave. Il n'importe rien de Panini : il relit le JSON, décode
le format, recalcule les empreintes et rejoue les 42 jugements avec un noyau
CIC-lite réécrit ici.

Ce que le vérificateur contrôle
-------------------------------
1. **Intégrité du fichier** : sha256 du corpus (la copie de Drave est
   byte-identique à l'original Panini).
2. **Sérialisation canonique** : chaque terme (défs, constantes, preuves, types)
   se décode puis se ré-encode exactement sur les mêmes octets.
3. **Type de de Bruijn** (B3) : chaque type est **clos** (aucun indice hors
   portée) et bien formé (`[] ⊢ type : sort n`) ; chaque preuve est close elle
   aussi. Un type valide n'est pas supposé : il est vérifié avant de servir de
   contrat à la preuve.
4. **Empreinte** : `sha256(octets(preuve) || octets(type))` égale l'empreinte
   déclarée, **et** une seconde implémentation de SHA-256 (FIPS 180-4, écrite
   ici sans `hashlib`) rejoue les 42 empreintes, le sha256 du fichier et les 24
   termes de l'environnement. Les deux chemins doivent concorder.
5. **Verdicts** : le noyau rend `True` pour les 36 « accepte » et `False` pour les
   6 « rejette » → 42/42 attendus.
6. **Contrôles négatifs** : altérer un octet d'une preuve acceptée doit la faire
   rejeter (36/36) ; altérer un octet d'un type doit le rendre invalide ou faire
   rejeter la preuve (42/42) ; le contrôle est exhaustif sur la plus petite
   preuve (`eq(2,2)`, 4 octets = 1 020 mutations).
7. **Non-trivialité** : un noyau qui accepte tout et un noyau qui rejette tout
   doivent échouer (respectivement 6 et 36 désaccords) — sinon le banc ne mesure
   rien.

Usage
-----
    python3 tools/verificateur_cic.py                 # résumé humain
    python3 tools/verificateur_cic.py --json          # mesure machine
    python3 tools/verificateur_cic.py --verbeux       # une ligne par entrée
    python3 tools/verificateur_cic.py --corpus CHEMIN --sha256 EMPREINTE
    python3 tools/verificateur_cic.py --sans-controles  # rejeu seul (rapide)

Sortie : code 0 si tout passe, 1 si un contrôle échoue, 2 si l'artefact est
illisible. Le module ne fait aucune écriture : il lit et imprime.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
import time
from typing import Any, Optional

RACINE = pathlib.Path(__file__).resolve().parents[1]
CORPUS_DEFAUT = RACINE / "tools" / "tests" / "cic" / "corpus_dor_cic_v1.json"

# sha256 du corpus source Panini/Research (nipada/falsification/corpus_dor_cic_v1.json),
# vérifié le 2026-11-14 ; la copie de Drave est byte-identique.
SHA256_CORPUS = "3018f6f4349641534be3a73309a1b25ff4bc71a3975e7105f2c15b61da18aaec"
COMMIT_SOURCE = "2130310db46ca9d59883500adc607bd86f534678"

# ---------------------------------------------------------------------------
# Format portable — étiquettes de termes et sérialisation canonique
# ---------------------------------------------------------------------------

TAGS = {
    "var": 0x00, "sort": 0x01, "pi": 0x02, "lam": 0x03, "app": 0x04,
    "nat": 0x05, "zero": 0x06, "suc": 0x07, "natrec": 0x08, "id": 0x09,
    "refl": 0x0A, "j": 0x0B, "sigma": 0x0C, "pair": 0x0D, "fst": 0x0E,
    "snd": 0x0F, "def": 0x10, "const": 0x11,
    "unit": 0x12, "tt": 0x13, "empty": 0x14, "abort": 0x15,
    "natind": 0x16, "bool": 0x17, "true": 0x18, "false": 0x19, "boolrec": 0x1A,
    "list": 0x1B, "nil": 0x1C, "cons": 0x1D, "listrec": 0x1E,
    "expr": 0x1F, "evar": 0x20, "ezero": 0x21, "eone": 0x22, "eadd": 0x23,
    "emul": 0x24, "erec": 0x25, "boolind": 0x26,
}
TAGS_INV = {v: k for k, v in TAGS.items()}

ATOMES = frozenset({
    "nat", "zero", "unit", "tt", "empty", "bool", "true", "false",
    "nil", "expr", "ezero", "eone",
})
UNAIRES = frozenset({"suc", "refl", "fst", "snd", "list", "evar"})
BINAIRES = frozenset({
    "pi", "lam", "app", "sigma", "pair", "abort", "cons", "eadd", "emul",
})
LIEURS = frozenset({"pi", "lam", "sigma"})
QUATRE = frozenset({"natrec", "natind", "boolrec", "boolind"})
ARITES = {"id": 3, "j": 6, "listrec": 5, "erec": 7}


class DecodeError(ValueError):
    """Le flux d'octets n'est pas un terme CIC-lite canonique."""


def _varint(n: int) -> bytes:
    if not isinstance(n, int) or n < 0:
        raise DecodeError(f"varint négatif ou non entier : {n!r}")
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def _read_varint(buf: bytes, i: int) -> tuple[int, int]:
    val = 0
    shift = 0
    start = i
    while True:
        if i >= len(buf):
            raise DecodeError("varint tronqué")
        b = buf[i]
        i += 1
        val |= (b & 0x7F) << shift
        if not (b & 0x80):
            # Refus d'un encodage non canonique (zéro de tête inutile).
            if i - start > 1 and b == 0:
                raise DecodeError("varint non canonique")
            return val, i
        shift += 7
        if shift > 63:
            raise DecodeError("varint trop long")


def serialize(t: tuple) -> bytes:
    """Encodage canonique d'un terme (de Bruijn) — inverse exact de `deserialize`."""
    if not isinstance(t, tuple) or not t:
        raise DecodeError(f"terme mal formé : {t!r}")
    tag = t[0]
    if tag not in TAGS:
        raise DecodeError(f"étiquette inconnue : {tag!r}")
    code = TAGS[tag]
    out = bytearray([code])
    if tag in ("var", "sort"):
        out += _varint(t[1])
    elif tag in ATOMES:
        pass
    elif tag in UNAIRES:
        out += serialize(t[1])
    elif tag in BINAIRES:
        out += serialize(t[1]) + serialize(t[2])
    elif tag in ARITES:
        if len(t) != ARITES[tag] + 1:
            raise DecodeError(f"{tag} attend {ARITES[tag]} enfants")
        for x in t[1:]:
            out += serialize(x)
    elif tag in QUATRE:
        if len(t) != 5:
            raise DecodeError(f"{tag} attend 4 enfants")
        for x in t[1:]:
            out += serialize(x)
    elif tag in ("def", "const"):
        nom = t[1].encode("utf-8")
        out += _varint(len(nom)) + nom
    else:  # pragma: no cover - toute étiquette est couverte ci-dessus
        raise DecodeError(f"étiquette non sérialisable : {tag!r}")
    return bytes(out)


def deserialize(buf: bytes, i: int = 0) -> tuple[tuple, int]:
    """Décode un terme à partir de `i` ; rend (terme, indice suivant)."""
    if i >= len(buf):
        raise DecodeError("flux vide ou tronqué")
    code = buf[i]
    i += 1
    tag = TAGS_INV.get(code)
    if tag is None:
        raise DecodeError(f"octet d'étiquette inconnu : 0x{code:02x}")
    if tag == "var":
        v, i = _read_varint(buf, i)
        return ("var", v), i
    if tag == "sort":
        v, i = _read_varint(buf, i)
        return ("sort", v), i
    if tag in ATOMES:
        return (tag,), i
    if tag in UNAIRES:
        a, i = deserialize(buf, i)
        return (tag, a), i
    if tag in BINAIRES:
        a, i = deserialize(buf, i)
        b, i = deserialize(buf, i)
        return (tag, a, b), i
    if tag in ARITES:
        xs = []
        for _ in range(ARITES[tag]):
            x, i = deserialize(buf, i)
            xs.append(x)
        return (tag, *xs), i
    if tag in QUATRE:
        xs = []
        for _ in range(4):
            x, i = deserialize(buf, i)
            xs.append(x)
        return (tag, *xs), i
    if tag in ("def", "const"):
        ln, i = _read_varint(buf, i)
        if i + ln > len(buf):
            raise DecodeError(f"nom {tag} tronqué")
        nom = buf[i:i + ln].decode("utf-8")
        return (tag, nom), i + ln
    raise DecodeError(f"étiquette non décodable : {tag!r}")  # pragma: no cover


def decode_exact(hexa: str) -> tuple:
    """Décode un terme et exige que TOUS les octets soient consommés."""
    try:
        buf = bytes.fromhex(hexa)
    except ValueError as exc:
        raise DecodeError(f"hexadécimal invalide : {exc}") from exc
    t, i = deserialize(buf, 0)
    if i != len(buf):
        raise DecodeError(f"{len(buf) - i} octet(s) après la fin du terme")
    return t


def empreinte(preuve_hex: str, type_hex: str) -> str:
    """Empreinte du corpus : sha256(preuve || type), octets binaires."""
    return hashlib.sha256(bytes.fromhex(preuve_hex) + bytes.fromhex(type_hex)).hexdigest()


# ---------------------------------------------------------------------------
# Seconde implémentation de SHA-256 (FIPS 180-4), sans hashlib
# ---------------------------------------------------------------------------

# Toutes les constantes sont celles de la publication FIPS 180-4. Cette
# implémentation est volontairement indépendante de `hashlib` : elle rejoue les
# 42 empreintes du corpus et le sha256 du fichier, et le vérificateur compare
# les deux chemins. Une divergence est un échec, pas un avertissement.
_K256 = (
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5,
    0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
    0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC,
    0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7,
    0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13,
    0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3,
    0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5,
    0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208,
    0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2,
)
_H256 = (
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
)
_M32 = 0xFFFFFFFF
_VECTEURS_SHA256 = (
    (b"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    (b"abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
    (b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
     "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"),
    (bytes(range(256)),
     "40aff2e9d2d8922e47afd4648e6967497158785fbd1da870e7110266bf944880"),
)


def _rotr32(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & _M32


def sha256_pur(message: bytes) -> str:
    """SHA-256 (FIPS 180-4) réécrit ici, **sans hashlib** — la seconde implémentation.

    Rend l'empreinte hexadécimale (64 caractères minuscules). Le rembourrage est
    celui de la norme : `0x80`, des zéros jusqu'à 56 octets modulo 64, puis la
    longueur du message en bits sur 8 octets big-endian.
    """
    if not isinstance(message, (bytes, bytearray)):
        raise TypeError(f"sha256_pur attend des octets, pas {type(message).__name__}")
    data = bytearray(message)
    longueur_bits = len(data) * 8
    data.append(0x80)
    while len(data) % 64 != 56:
        data.append(0)
    data += longueur_bits.to_bytes(8, "big", signed=False)

    h = list(_H256)
    for debut in range(0, len(data), 64):
        w = [int.from_bytes(data[debut + 4 * i:debut + 4 * i + 4], "big")
             for i in range(16)]
        for i in range(16, 64):
            x, y = w[i - 15], w[i - 2]
            s0 = _rotr32(x, 7) ^ _rotr32(x, 18) ^ (x >> 3)
            s1 = _rotr32(y, 17) ^ _rotr32(y, 19) ^ (y >> 10)
            w.append((w[i - 16] + s0 + w[i - 7] + s1) & _M32)

        a, b, c, d, e, f, g, hh = h
        for i in range(64):
            s1 = _rotr32(e, 6) ^ _rotr32(e, 11) ^ _rotr32(e, 25)
            ch = (e & f) ^ ((~e & _M32) & g)
            t1 = (hh + s1 + ch + _K256[i] + w[i]) & _M32
            s0 = _rotr32(a, 2) ^ _rotr32(a, 13) ^ _rotr32(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            t2 = (s0 + maj) & _M32
            hh, g, f, e, d, c, b, a = g, f, e, (d + t1) & _M32, c, b, a, (t1 + t2) & _M32
        h = [(x + y) & _M32 for x, y in zip(h, (a, b, c, d, e, f, g, hh))]
    return "".join(f"{x:08x}" for x in h)


def empreinte_pure(preuve_hex: str, type_hex: str) -> str:
    """Même formule que `empreinte`, calculée par la seconde implémentation."""
    return sha256_pur(bytes.fromhex(preuve_hex) + bytes.fromhex(type_hex))


def autotest_sha256_pur() -> dict:
    """Vecteurs FIPS + comparaison à `hashlib` sur des longueurs de rembourrage."""
    ecarts = []
    for message, attendu in _VECTEURS_SHA256:
        obtenu = sha256_pur(message)
        if obtenu != attendu:
            ecarts.append({"message": message.hex(), "attendu": attendu, "obtenu": obtenu})
    for n in (1, 55, 56, 57, 63, 64, 65, 119, 120, 127, 128, 129):
        message = bytes((i * 37 + 11) & 0xFF for i in range(n))
        if sha256_pur(message) != hashlib.sha256(message).hexdigest():
            ecarts.append({"longueur": n, "raison": "divergence avec hashlib"})
    return {
        "implementation": "FIPS 180-4 réécrite dans ce module, sans hashlib",
        "vecteurs": len(_VECTEURS_SHA256) + 12,
        "ecarts": ecarts,
        "verdict": "pass" if not ecarts else "fail",
    }


# ---------------------------------------------------------------------------
# Portée des indices de de Bruijn — contrôle syntaxique indépendant du noyau
# ---------------------------------------------------------------------------

def indices_hors_portee(t: tuple, profondeur: int = 0) -> list[int]:
    """Rend les indices de variables qui dépassent le nombre de lieurs ouverts.

    Un terme clos (``[] ⊢ t``) ne doit contenir aucun `var i` avec `i >=
    profondeur`. Le contrôle est purement structurel : il ne dépend ni du
    noyau, ni de la conversion, ni de l'environnement.
    """
    tag = t[0]
    if tag == "var":
        return [t[1]] if t[1] >= profondeur else []
    if tag in LIEURS:
        return (indices_hors_portee(t[1], profondeur)
                + indices_hors_portee(t[2], profondeur + 1))
    if tag in ATOMES or tag in ("sort", "def", "const"):
        return []
    hors: list[int] = []
    for x in t[1:]:
        if isinstance(x, tuple):
            hors += indices_hors_portee(x, profondeur)
    return hors


def est_clos(t: tuple) -> bool:
    """Vrai si tous les indices de de Bruijn sont sous un lieur."""
    return not indices_hors_portee(t)


# ---------------------------------------------------------------------------
# Noyau CIC-lite — termes de de Bruijn, typage bidirectionnel, conversion
# ---------------------------------------------------------------------------

def shift(t: tuple, d: int, c: int = 0) -> tuple:
    """Décale de `d` les variables libres >= `c`."""
    tag = t[0]
    if tag == "var":
        i = t[1]
        return ("var", i + d) if i >= c else t
    if tag in ATOMES or tag in ("sort", "def", "const"):
        return t
    if tag in LIEURS:
        return (tag, shift(t[1], d, c), shift(t[2], d, c + 1))
    if tag in ("suc", "refl", "fst", "snd", "list", "evar"):
        return (tag, shift(t[1], d, c))
    if tag in BINAIRES:
        return (tag, shift(t[1], d, c), shift(t[2], d, c))
    if tag in ARITES or tag in QUATRE:
        return (tag, *(shift(x, d, c) for x in t[1:]))
    raise DecodeError(f"shift : étiquette inconnue {tag!r}")


def subst(t: tuple, s: tuple, x: int = 0) -> tuple:
    """Substitution `t[x := s]` (les variables > x sont décrémentées de 1)."""
    tag = t[0]
    if tag == "var":
        i = t[1]
        if i == x:
            return s
        return ("var", i - 1) if i > x else t
    if tag in ATOMES or tag in ("sort", "def", "const"):
        return t
    if tag in LIEURS:
        # Le domaine est au niveau x ; le corps au niveau x+1, et `s` y est décalé.
        return (tag, subst(t[1], s, x), subst(t[2], shift(s, 1, 0), x + 1))
    if tag in ("suc", "refl", "fst", "snd", "list", "evar"):
        return (tag, subst(t[1], s, x))
    if tag in BINAIRES:
        return (tag, subst(t[1], s, x), subst(t[2], s, x))
    if tag in ARITES or tag in QUATRE:
        return (tag, *(subst(u, s, x) for u in t[1:]))
    raise DecodeError(f"subst : étiquette inconnue {tag!r}")


def subst_many(t: tuple, args: list[tuple], x: int = 0) -> tuple:
    """Substitution SIMULTANÉE `t[x+i := args[i]]` (i < len(args)).

    Les arguments sont décalés à chaque passage sous un lieur ; les variables
    >= x+len(args) sont décrémentées de len(args). C'est la forme correcte pour
    réduire un récurseur appliqué à plusieurs arguments : substituer l'un après
    l'autre modifierait les arguments déjà insérés.
    """
    n = len(args)

    def rec(u: tuple, depth: int, remplacements: list[tuple]) -> tuple:
        tag = u[0]
        if tag == "var":
            i = u[1]
            base = x + depth
            if base <= i < base + n:
                return remplacements[i - base]
            return ("var", i - n) if i >= base + n else u
        if tag in ATOMES or tag in ("sort", "def", "const"):
            return u
        if tag in LIEURS:
            dedans = [shift(a, 1, 0) for a in remplacements]
            return (tag, rec(u[1], depth, remplacements), rec(u[2], depth + 1, dedans))
        if tag in ("suc", "refl", "fst", "snd", "list", "evar"):
            return (tag, rec(u[1], depth, remplacements))
        if tag in BINAIRES:
            return (tag, rec(u[1], depth, remplacements), rec(u[2], depth, remplacements))
        if tag in ARITES or tag in QUATRE:
            return (tag, *(rec(z, depth, remplacements) for z in u[1:]))
        raise DecodeError(f"subst_many : étiquette inconnue {tag!r}")

    return rec(t, 0, list(args))


def apply_multi(s: tuple, args: list[tuple]) -> tuple:
    """Applique `s` à `args` ; si c'est une chaîne de λ, substitue en une passe."""
    body = s
    for _ in args:
        if body[0] == "lam":
            body = body[2]
        else:
            r = s
            for a in args:
                r = ("app", r, a)
            return r
    # `body` a été débarrassé de n lambdas : var 0 = dernier argument.
    return subst_many(body, list(reversed(args)), 0)


class Kernel:
    """Noyau CIC-lite : `check(contexte, terme, type) -> bool`, pur et déterministe.

    Le fragment couvert est celui du format portable (`TAGS`) : univers
    hiérarchiques, Π, λ, application, ℕ + récurseur, Id + refl + J, Σ + paires +
    projections, définitions transparentes (δ), constantes, unité, vide,
    Bool/Liste/Expr et leurs récurseurs. Pas de W, ∃ ni de types inductifs
    définis par l'utilisateur — ce ne sont pas des étiquettes du format.
    """

    def __init__(self, defs: dict[str, tuple], consts: dict[str, tuple]):
        self.defs = dict(defs)
        self.consts = dict(consts)
        self._eval_cache: dict[int, tuple[tuple, tuple]] = {}
        self._nf_cache: dict[int, tuple[tuple, tuple]] = {}
        self._infer_cache: dict[tuple[int, int], tuple[Any, Any, Any]] = {}
        self._check_cache: dict[tuple[int, int, int], tuple[Any, Any, Any, bool]] = {}

    # -- conversion -------------------------------------------------------
    def eval(self, t: tuple) -> tuple:
        """Forme de tête faible (β, ι, δ, η de Σ)."""
        key = id(t)
        hit = self._eval_cache.get(key)
        if hit is not None and hit[0] is t:
            return hit[1]
        r = self._eval(t)
        self._eval_cache[key] = (t, r)
        return r

    def _eval(self, t: tuple) -> tuple:
        tag = t[0]
        if tag == "app":
            f = self.eval(t[1])
            if f[0] == "lam":
                return self.eval(subst(f[2], t[2]))
            return ("app", f, t[2])
        if tag == "fst":
            p = self.eval(t[1])
            if p[0] == "pair":
                return self.eval(p[1])
            return ("fst", p)
        if tag == "snd":
            p = self.eval(t[1])
            if p[0] == "pair":
                return self.eval(p[2])
            return ("snd", p)
        if tag == "natrec":
            A, z, s, n = t[1], t[2], t[3], self.eval(t[4])
            if n[0] == "zero":
                return self.eval(z)
            if n[0] == "suc":
                return self.eval(apply_multi(self.eval(s), [n[1], ("natrec", A, z, s, n[1])]))
            return ("natrec", A, z, s, n)
        if tag == "j":
            A, a, P, base, b, p = t[1], t[2], t[3], t[4], t[5], self.eval(t[6])
            if p[0] == "refl":
                return self.eval(base)
            return ("j", A, a, P, base, b, p)
        if tag == "natind":
            P, base, step, n = t[1], t[2], t[3], self.eval(t[4])
            if n[0] == "zero":
                return self.eval(base)
            if n[0] == "suc":
                return self.eval(apply_multi(self.eval(step),
                                             [n[1], ("natind", P, base, step, n[1])]))
            return ("natind", P, base, step, n)
        if tag == "boolrec":
            A, tt, ff, b = t[1], t[2], t[3], self.eval(t[4])
            if b[0] == "true":
                return self.eval(tt)
            if b[0] == "false":
                return self.eval(ff)
            return ("boolrec", A, tt, ff, b)
        if tag == "boolind":
            P, pt, pf, b = t[1], t[2], t[3], self.eval(t[4])
            if b[0] == "true":
                return self.eval(pt)
            if b[0] == "false":
                return self.eval(pf)
            return ("boolind", P, pt, pf, b)
        if tag == "listrec":
            A, P, z, s, l = t[1], t[2], t[3], t[4], self.eval(t[5])
            if l[0] == "nil":
                return self.eval(z)
            if l[0] == "cons":
                return self.eval(apply_multi(self.eval(s),
                                             [l[1], l[2], ("listrec", A, P, z, s, l[2])]))
            return ("listrec", A, P, z, s, l)
        if tag == "erec":
            P, v, z, o, a, m, e = t[1], t[2], t[3], t[4], t[5], t[6], self.eval(t[7])
            if e[0] == "evar":
                return self.eval(("app", v, e[1]))
            if e[0] == "ezero":
                return self.eval(z)
            if e[0] == "eone":
                return self.eval(o)
            if e[0] == "eadd":
                return self.eval(apply_multi(self.eval(a),
                                             [e[1], e[2],
                                              ("erec", P, v, z, o, a, m, e[1]),
                                              ("erec", P, v, z, o, a, m, e[2])]))
            if e[0] == "emul":
                return self.eval(apply_multi(self.eval(m),
                                             [e[1], e[2],
                                              ("erec", P, v, z, o, a, m, e[1]),
                                              ("erec", P, v, z, o, a, m, e[2])]))
            return ("erec", P, v, z, o, a, m, e)
        if tag == "pair":
            a, b = t[1], t[2]
            if a[0] == "fst" and b[0] == "snd" and a[1] == b[1]:
                return self.eval(a[1])       # η de Σ
            return t
        if tag == "def":
            if t[1] not in self.defs:
                return t
            return self.eval(self.defs[t[1]])  # δ
        return t

    def nf(self, t: tuple) -> tuple:
        """Forme normale complète (whnf puis normalisation des sous-termes)."""
        key = id(t)
        hit = self._nf_cache.get(key)
        if hit is not None and hit[0] is t:
            return hit[1]
        r = self._nf(t)
        self._nf_cache[key] = (t, r)
        return r

    def _nf(self, t: tuple) -> tuple:
        t = self.eval(t)
        tag = t[0]
        if tag in LIEURS:
            return (tag, self.nf(t[1]), self.nf(t[2]))
        if tag == "app":
            f = self.nf(t[1])
            a = self.nf(t[2])
            if f[0] == "lam":
                return self.nf(("app", f, a))
            return ("app", f, a)
        if tag in ("suc", "refl", "fst", "snd", "list", "evar"):
            return (tag, self.nf(t[1]))
        if tag in ("pair", "cons", "eadd", "emul", "abort"):
            a, b = self.nf(t[1]), self.nf(t[2])
            if tag == "pair" and a[0] == "fst" and b[0] == "snd" and a[1] == b[1]:
                return self.nf(a[1])
            return (tag, a, b)
        if tag == "id":
            return (tag, self.nf(t[1]), self.nf(t[2]), self.nf(t[3]))
        if tag in QUATRE:
            return (tag, *(self.nf(x) for x in t[1:]))
        if tag in ("j", "listrec", "erec"):
            return (tag, *(self.nf(x) for x in t[1:]))
        return t

    def conv(self, a: tuple, b: tuple) -> bool:
        """Égalité définitionnelle : formes normales structurellement égales."""
        return self.nf(a) == self.nf(b)

    # -- typage -----------------------------------------------------------
    def niveau(self, ctx: tuple, t: tuple) -> Optional[int]:
        ty = self.infer(ctx, t)
        if ty is None:
            return None
        ty = self.eval(ty)
        return ty[1] if ty[0] == "sort" else None

    def type_bien_forme(self, A: tuple) -> Optional[tuple]:
        """Vérifie que `A` est un **type clos** : `[] ⊢ A : s` avec `s` un sort.

        Rend le sort (`("sort", n)`) ou `None`. C'est la vérification du *type*
        de de Bruijn, distincte de la vérification de la *preuve* : un terme
        bien encodé n'est pas forcément un type, et un type ouvert n'a pas de
        sens dans le contexte vide.
        """
        if indices_hors_portee(A):
            return None
        ty = self.infer((), A)
        if ty is None:
            return None
        ty = self.eval(ty)
        return ty if ty[0] == "sort" else None

    def infer(self, ctx: tuple, t: tuple) -> Optional[tuple]:
        key = (id(ctx), id(t))
        hit = self._infer_cache.get(key)
        if hit is not None and hit[0] is ctx and hit[1] is t:
            return hit[2]
        r = self._infer(ctx, t)
        self._infer_cache[key] = (ctx, t, r)
        return r

    def _infer(self, ctx: tuple, t: tuple) -> Optional[tuple]:
        tag = t[0]
        if tag == "var":
            i = t[1]
            if i >= len(ctx):
                return None
            # Le type stocké vit dans le contexte de sa liaison ; on le décale.
            return shift(ctx[len(ctx) - 1 - i], i + 1, 0)
        if tag == "sort":
            return ("sort", t[1] + 1)
        if tag == "pi":
            A, B = t[1], t[2]
            l1 = self.niveau(ctx, A)
            l2 = self.niveau(ctx + (A,), B)
            if l1 is None or l2 is None:
                return None
            return ("sort", max(l1, l2))
        if tag == "lam":
            A, body = t[1], t[2]
            if self.niveau(ctx, A) is None:
                return None
            B = self.infer(ctx + (A,), body)
            if B is None:
                return None
            return ("pi", A, B)
        if tag == "app":
            f_ty = self.infer(ctx, t[1])
            if f_ty is None:
                return None
            f_ty = self.eval(f_ty)
            if f_ty[0] != "pi":
                return None
            A, B = f_ty[1], f_ty[2]
            if not self.check(ctx, t[2], A):
                return None
            return subst(B, t[2])
        if tag == "nat":
            return ("sort", 0)
        if tag == "zero":
            return ("nat",)
        if tag == "suc":
            if not self.check(ctx, t[1], ("nat",)):
                return None
            return ("nat",)
        if tag == "natrec":
            A, z, s, n = t[1], t[2], t[3], t[4]
            if self.niveau(ctx, A) is None:
                return None
            if not self.check(ctx, z, A):
                return None
            s_ty = ("pi", ("nat",), ("pi", shift(A, 1, 0), shift(A, 2, 0)))
            if not self.check(ctx, s, s_ty):
                return None
            if not self.check(ctx, n, ("nat",)):
                return None
            return A
        if tag == "id":
            A, a, b = t[1], t[2], t[3]
            l = self.niveau(ctx, A)
            if l is None:
                return None
            if not self.check(ctx, a, A):
                return None
            if not self.check(ctx, b, A):
                return None
            return ("sort", l)
        if tag == "refl":
            a = t[1]
            A = self.infer(ctx, a)
            if A is None:
                return None
            return ("id", A, a, a)
        if tag == "j":
            A, a, P, base, b, p = t[1], t[2], t[3], t[4], t[5], t[6]
            if self.niveau(ctx, A) is None:
                return None
            if not self.check(ctx, a, A):
                return None
            P_ty = ("pi", A,
                    ("pi", ("id", shift(A, 1), shift(a, 1), ("var", 0)),
                     ("sort", 0)))
            if not self.check(ctx, P, P_ty):
                return None
            base_ty = ("app", ("app", P, a), ("refl", a))
            if not self.check(ctx, base, base_ty):
                return None
            if not self.check(ctx, b, A):
                return None
            if not self.check(ctx, p, ("id", A, a, b)):
                return None
            return ("app", ("app", P, b), p)
        if tag == "sigma":
            A, B = t[1], t[2]
            l1 = self.niveau(ctx, A)
            l2 = self.niveau(ctx + (A,), B)
            if l1 is None or l2 is None:
                return None
            return ("sort", max(l1, l2))
        if tag == "pair":
            return None
        if tag == "fst":
            p_ty = self.infer(ctx, t[1])
            if p_ty is None:
                return None
            p_ty = self.eval(p_ty)
            if p_ty[0] != "sigma":
                return None
            return p_ty[1]
        if tag == "snd":
            p_ty = self.infer(ctx, t[1])
            if p_ty is None:
                return None
            p_ty = self.eval(p_ty)
            if p_ty[0] != "sigma":
                return None
            return subst(p_ty[2], ("fst", t[1]))
        if tag == "def":
            if t[1] not in self.defs:
                return None
            return self.infer(ctx, self.defs[t[1]])
        if tag == "const":
            return self.consts.get(t[1])
        if tag == "unit":
            return ("sort", 0)
        if tag == "tt":
            return ("unit",)
        if tag == "empty":
            return ("sort", 0)
        if tag == "abort":
            A, p = t[1], t[2]
            if self.niveau(ctx, A) is None:
                return None
            if not self.check(ctx, p, ("empty",)):
                return None
            return A
        if tag == "natind":
            P, base, step, n = t[1], t[2], t[3], t[4]
            if not self.check(ctx, P, ("pi", ("nat",), ("sort", 0))):
                return None
            if not self.check(ctx, base, ("app", P, ("zero",))):
                return None
            step_ty = ("pi", ("nat",),
                       ("pi", ("app", shift(P, 1, 0), ("var", 0)),
                        ("app", shift(P, 2, 0), ("suc", ("var", 1)))))
            if not self.check(ctx, step, step_ty):
                return None
            if not self.check(ctx, n, ("nat",)):
                return None
            return ("app", P, n)
        if tag == "bool":
            return ("sort", 0)
        if tag == "true":
            return ("bool",)
        if tag == "false":
            return ("bool",)
        if tag == "boolrec":
            A, tt, ff, b = t[1], t[2], t[3], t[4]
            if self.niveau(ctx, A) is None:
                return None
            if not self.check(ctx, tt, A):
                return None
            if not self.check(ctx, ff, A):
                return None
            if not self.check(ctx, b, ("bool",)):
                return None
            return A
        if tag == "boolind":
            P, pt, pf, b = t[1], t[2], t[3], t[4]
            if not self.check(ctx, P, ("pi", ("bool",), ("sort", 0))):
                return None
            if not self.check(ctx, pt, ("app", P, ("true",))):
                return None
            if not self.check(ctx, pf, ("app", P, ("false",))):
                return None
            if not self.check(ctx, b, ("bool",)):
                return None
            return ("app", P, b)
        if tag == "list":
            l = self.niveau(ctx, t[1])
            if l is None:
                return None
            return ("sort", l)
        if tag == "nil":
            return None
        if tag == "cons":
            return None
        if tag == "listrec":
            A, P, z, s, l = t[1], t[2], t[3], t[4], t[5]
            LA = ("list", A)
            if self.niveau(ctx, A) is None:
                return None
            if not self.check(ctx, P, ("pi", LA, ("sort", 0))):
                return None
            if not self.check(ctx, z, ("app", P, ("nil",))):
                return None
            s_ty = ("pi", A,
                    ("pi", shift(LA, 1, 0),
                     ("pi", ("app", shift(P, 2, 0), ("var", 0)),
                      ("app", shift(P, 3, 0), ("cons", ("var", 2), ("var", 1))))))
            if not self.check(ctx, s, s_ty):
                return None
            if not self.check(ctx, l, LA):
                return None
            return ("app", P, l)
        if tag == "expr":
            return ("sort", 0)
        if tag == "evar":
            if not self.check(ctx, t[1], ("nat",)):
                return None
            return ("expr",)
        if tag in ("ezero", "eone"):
            return ("expr",)
        if tag in ("eadd", "emul"):
            if not self.check(ctx, t[1], ("expr",)):
                return None
            if not self.check(ctx, t[2], ("expr",)):
                return None
            return ("expr",)
        if tag == "erec":
            P, v, z, o, a, m, e = t[1], t[2], t[3], t[4], t[5], t[6], t[7]
            EX = ("expr",)
            if not self.check(ctx, P, ("pi", EX, ("sort", 0))):
                return None
            if not self.check(ctx, v, ("pi", ("nat",),
                                       ("app", shift(P, 1, 0), ("evar", ("var", 0))))):
                return None
            if not self.check(ctx, z, ("app", P, ("ezero",))):
                return None
            if not self.check(ctx, o, ("app", P, ("eone",))):
                return None
            a_ty = ("pi", EX, ("pi", EX,
                    ("pi", ("app", shift(P, 2, 0), ("var", 1)),
                     ("pi", ("app", shift(P, 3, 0), ("var", 1)),
                      ("app", shift(P, 4, 0), ("eadd", ("var", 3), ("var", 2)))))))
            if not self.check(ctx, a, a_ty):
                return None
            m_ty = ("pi", EX, ("pi", EX,
                    ("pi", ("app", shift(P, 2, 0), ("var", 1)),
                     ("pi", ("app", shift(P, 3, 0), ("var", 1)),
                      ("app", shift(P, 4, 0), ("emul", ("var", 3), ("var", 2)))))))
            if not self.check(ctx, m, m_ty):
                return None
            if not self.check(ctx, e, EX):
                return None
            return ("app", P, e)
        return None

    def check(self, ctx: tuple, t: tuple, A: tuple) -> bool:
        key = (id(ctx), id(t), id(A))
        hit = self._check_cache.get(key)
        if hit is not None and hit[0] is ctx and hit[1] is t and hit[2] is A:
            return hit[3]
        r = self._check(ctx, t, A)
        self._check_cache[key] = (ctx, t, A, r)
        return r

    def _check(self, ctx: tuple, t: tuple, A: tuple) -> bool:
        tag = t[0]
        if tag == "lam":
            A = self.eval(A)
            if A[0] != "pi":
                return False
            if self.niveau(ctx, t[1]) is None:
                return False
            if not self.conv(t[1], A[1]):
                return False
            return self.check(ctx + (t[1],), t[2], A[2])
        if tag == "pair":
            A = self.eval(A)
            if A[0] != "sigma":
                return False
            if not self.check(ctx, t[1], A[1]):
                return False
            return self.check(ctx, t[2], subst(A[2], t[1]))
        if tag == "refl":
            A = self.eval(A)
            if A[0] != "id":
                return False
            a = t[1]
            if not self.conv(a, A[2]):
                return False
            if not self.conv(a, A[3]):
                return False
            return self.check(ctx, a, A[1])
        if tag == "nil":
            A = self.eval(A)
            return A[0] == "list"
        if tag == "cons":
            A = self.eval(A)
            if A[0] != "list":
                return False
            if not self.check(ctx, t[1], A[1]):
                return False
            return self.check(ctx, t[2], A)
        B = self.infer(ctx, t)
        if B is None:
            return False
        return self.conv(B, A)

    def verify(self, t: tuple, A: tuple) -> bool:
        """Jugement sur terme clos : `[] ⊢ t : A`."""
        return self.check((), t, A)


# ---------------------------------------------------------------------------
# Lecture de l'artefact et rejeu
# ---------------------------------------------------------------------------

def charger_corpus(chemin: pathlib.Path) -> tuple[dict, dict, bytes, str]:
    brut = chemin.read_bytes()
    sha = hashlib.sha256(brut).hexdigest()
    try:
        d = json.loads(brut)
    except json.JSONDecodeError as exc:
        raise DecodeError(f"JSON illisible : {exc}") from exc
    for cle in ("doctrine", "defs", "consts", "entrees"):
        if cle not in d:
            raise DecodeError(f"clé absente : {cle}")
    if not isinstance(d["defs"], dict) or not isinstance(d["consts"], dict):
        raise DecodeError("defs/consts doivent être des objets")
    if not isinstance(d["entrees"], list):
        raise DecodeError("entrees doit être une liste")
    return d["defs"], d["consts"], brut, sha


def construire_environnement(defs_hex: dict, consts_hex: dict) -> tuple[dict, dict, dict]:
    """Décode défs et constantes ; rend aussi un bilan de sérialisation canonique."""
    defs, consts = {}, {}
    bilan = {"defs": 0, "consts": 0, "echecs": []}
    for nom, hexa in defs_hex.items():
        t = decode_exact(hexa)
        if serialize(t).hex() != hexa:
            bilan["echecs"].append(f"def:{nom}")
        defs[nom] = t
        bilan["defs"] += 1
    for nom, hexa in consts_hex.items():
        t = decode_exact(hexa)
        if serialize(t).hex() != hexa:
            bilan["echecs"].append(f"const:{nom}")
        consts[nom] = t
        bilan["consts"] += 1
    return defs, consts, bilan


def rejouer(corpus: dict, defs: dict, consts: dict) -> dict:
    """Rejoue toutes les entrées ; rend le bilan détaillé."""
    noyau = Kernel(defs, consts)
    resultats = []
    for e in corpus["entrees"]:
        nom = e.get("nom", "?")
        attendu = e.get("verdict")
        if attendu not in ("accepte", "rejette"):
            raise DecodeError(f"verdict inconnu pour {nom!r} : {attendu!r}")
        preuve_hex, type_hex = e.get("preuve_hex"), e.get("type_hex")
        if not isinstance(preuve_hex, str) or not isinstance(type_hex, str):
            raise DecodeError(f"preuve/type absents pour {nom!r}")
        t0 = time.perf_counter()
        try:
            preuve = decode_exact(preuve_hex)
            typ = decode_exact(type_hex)
            decode_ok = True
        except DecodeError as exc:
            preuve = typ = None
            decode_ok = False
            detail_decode = str(exc)

        # Vérification du TYPE de de Bruijn : le type doit être clos, puis
        # `[] ⊢ type : sort n`. Ce n'est pas la même chose que vérifier la
        # preuve contre ce type : un type ouvert ou mal typé ne doit jamais
        # servir de contrat.
        preuve_close = type_clos = type_bien_forme = False
        niveau_type = None
        if decode_ok:
            preuve_close = est_clos(preuve)
            hors_type = indices_hors_portee(typ)
            type_clos = not hors_type
            if type_clos:
                sort_type = noyau.type_bien_forme(typ)
                if sort_type is not None:
                    type_bien_forme = True
                    niveau_type = sort_type[1]

        obtenu = (noyau.verify(preuve, typ)
                  if decode_ok and type_bien_forme else False)
        duree = time.perf_counter() - t0
        attendu_bool = attendu == "accepte"
        try:
            empreinte_ok = empreinte(preuve_hex, type_hex) == e.get("empreinte")
        except ValueError:
            empreinte_ok = False
        try:
            empreinte_pure_ok = empreinte_pure(preuve_hex, type_hex) == e.get("empreinte")
        except ValueError:
            empreinte_pure_ok = False
        serial_ok = False
        if decode_ok:
            serial_ok = (serialize(preuve).hex() == preuve_hex
                         and serialize(typ).hex() == type_hex)
        resultats.append({
            "nom": nom,
            "attendu": attendu,
            "obtenu": "accepte" if obtenu else "rejette",
            "accord": decode_ok and (obtenu == attendu_bool),
            "empreinte_ok": empreinte_ok,
            "empreinte_pure_ok": empreinte_pure_ok,
            "preuve_close": preuve_close,
            "type_clos": type_clos,
            "type_bien_forme": type_bien_forme,
            "niveau_type": niveau_type,
            "serialisation_canonique": serial_ok,
            "octets_preuve": len(preuve_hex) // 2,
            "octets_type": len(type_hex) // 2,
            "duree_s": round(duree, 6),
        })
        if not decode_ok:
            resultats[-1]["erreur_decodage"] = detail_decode
    n = len(resultats)
    accord = sum(1 for r in resultats if r["accord"])
    niveaux = sorted({r["niveau_type"] for r in resultats if r["niveau_type"] is not None})
    return {
        "verdicts": n,
        "attendus_acceptes": sum(1 for r in resultats if r["attendu"] == "accepte"),
        "attendus_rejetes": sum(1 for r in resultats if r["attendu"] == "rejette"),
        "accord": accord,
        "desaccord": n - accord,
        "taux_accord": round(accord / n, 6) if n else 0.0,
        "empreintes_valides": sum(1 for r in resultats if r["empreinte_ok"]),
        "empreintes_pures_valides": sum(1 for r in resultats if r["empreinte_pure_ok"]),
        "empreintes_concordantes": sum(
            1 for r in resultats if r["empreinte_ok"] and r["empreinte_pure_ok"]),
        "serialisations_canoniques": sum(1 for r in resultats if r["serialisation_canonique"]),
        "preuves_closes": sum(1 for r in resultats if r["preuve_close"]),
        "types_clos": sum(1 for r in resultats if r["type_clos"]),
        "types_bien_formes": sum(1 for r in resultats if r["type_bien_forme"]),
        "niveaux_types": niveaux,
        "entrees": resultats,
    }


def _muter_octet(hexa: str, indice: int = -1, delta: int = 1) -> str:
    b = bytearray(bytes.fromhex(hexa))
    if not b:
        raise ValueError("preuve vide")
    i = indice % len(b)
    b[i] = (b[i] + delta) % 256
    return b.hex()


def controle_octet_altere(corpus: dict, defs: dict, consts: dict) -> dict:
    """Altère le dernier octet de chaque preuve acceptée et exige un rejet.

    On vérifie aussi que l'empreinte recalculée change : l'altération est
    détectable par le sha256 même si, par accident, le terme restait typable.
    """
    noyau = Kernel(defs, consts)
    mutations = acceptes = empreintes_changees = empreintes_pures_changees = 0
    details = []
    for e in corpus["entrees"]:
        if e.get("verdict") != "accepte":
            continue
        mut = _muter_octet(e["preuve_hex"], -1, 1)
        mutations += 1
        try:
            t = decode_exact(mut)
            typ = decode_exact(e["type_hex"])
            r = noyau.type_bien_forme(typ) is not None and noyau.verify(t, typ)
        except DecodeError:
            r = False
        if r:
            acceptes += 1
            details.append(e["nom"])
        if empreinte(mut, e["type_hex"]) != e.get("empreinte"):
            empreintes_changees += 1
        if empreinte_pure(mut, e["type_hex"]) != e.get("empreinte"):
            empreintes_pures_changees += 1
    return {
        "methode": "dernier octet de la preuve +1 (mod 256), sur chaque preuve acceptée",
        "mutations": mutations,
        "acceptes_apres_mutation": acceptes,
        "rejetes_apres_mutation": mutations - acceptes,
        "empreintes_changees": empreintes_changees,
        "empreintes_pures_changees": empreintes_pures_changees,
        "noms_encore_acceptes": details,
        "verdict": ("pass" if acceptes == 0 and empreintes_changees == mutations
                    and empreintes_pures_changees == mutations else "fail"),
    }


def controle_type_altere(corpus: dict, defs: dict, consts: dict) -> dict:
    """Altère le dernier octet de chaque TYPE et exige un rejet.

    Le contrôle vérifie les deux verrous ajoutés en B3 : (a) le type muté
    n'est plus clos ou n'est plus un type bien formé, (b) la preuve n'est plus
    acceptée contre lui — même si elle l'était encore, l'empreinte a changé
    sous les deux implémentations de SHA-256.
    """
    noyau = Kernel(defs, consts)
    mutations = acceptes = types_invalides = 0
    empreintes_changees = empreintes_pures_changees = 0
    details = []
    for e in corpus["entrees"]:
        mut = _muter_octet(e["type_hex"], -1, 1)
        mutations += 1
        try:
            typ = decode_exact(mut)
            preuve = decode_exact(e["preuve_hex"])
            valide = noyau.type_bien_forme(typ) is not None
            if not valide:
                types_invalides += 1
            r = valide and noyau.verify(preuve, typ)
        except DecodeError:
            types_invalides += 1
            r = False
        if r:
            acceptes += 1
            details.append(e["nom"])
        if empreinte(e["preuve_hex"], mut) != e.get("empreinte"):
            empreintes_changees += 1
        if empreinte_pure(e["preuve_hex"], mut) != e.get("empreinte"):
            empreintes_pures_changees += 1
    return {
        "methode": "dernier octet du type +1 (mod 256), sur les 42 entrées",
        "mutations": mutations,
        "types_devenus_invalides": types_invalides,
        "acceptes_apres_mutation": acceptes,
        "rejetes_apres_mutation": mutations - acceptes,
        "empreintes_changees": empreintes_changees,
        "empreintes_pures_changees": empreintes_pures_changees,
        "noms_encore_acceptes": details,
        "verdict": ("pass" if acceptes == 0 and empreintes_changees == mutations
                    and empreintes_pures_changees == mutations else "fail"),
    }


def controle_exhaustif_petite_preuve(corpus: dict, defs: dict, consts: dict) -> dict:
    """Énumère TOUTES les mutations d'un octet de la plus petite preuve acceptée."""
    noyau = Kernel(defs, consts)
    candidates = [e for e in corpus["entrees"] if e.get("verdict") == "accepte"]
    if not candidates:
        return {"verdict": "fail", "raison": "aucune preuve acceptée"}
    e = min(candidates, key=lambda x: len(x["preuve_hex"]))
    original = bytes.fromhex(e["preuve_hex"])
    typ = decode_exact(e["type_hex"])
    total = acceptes = 0
    exemples = []
    for i in range(len(original)):
        for v in range(256):
            if v == original[i]:
                continue
            total += 1
            b = bytearray(original)
            b[i] = v
            try:
                r = noyau.verify(decode_exact(b.hex()), typ)
            except DecodeError:
                r = False
            if r:
                acceptes += 1
                if len(exemples) < 10:
                    exemples.append({"octet": i, "valeur": v, "hex": b.hex()})
    return {
        "preuve": e["nom"],
        "octets": len(original),
        "mutations": total,
        "acceptes_apres_mutation": acceptes,
        "rejetes_apres_mutation": total - acceptes,
        "exemples_acceptes": exemples,
        "verdict": "pass" if acceptes == 0 else "fail",
    }


def controle_non_trivialite(corpus: dict, defs: dict, consts: dict) -> dict:
    """Un noyau qui accepte tout / rejette tout doit échouer sur ce corpus."""
    attendus = [e["verdict"] == "accepte" for e in corpus["entrees"]]
    n = len(attendus)
    tout_oui = sum(1 for a in attendus if a)
    tout_non = sum(1 for a in attendus if not a)
    return {
        "accepte_tout": {
            "accord": tout_oui,
            "desaccord": n - tout_oui,
            "verdict": "pass" if tout_oui < n else "fail",
        },
        "rejette_tout": {
            "accord": tout_non,
            "desaccord": n - tout_non,
            "verdict": "pass" if tout_non < n else "fail",
        },
    }


def verifier_sha256_independant(brut: bytes, corpus: dict, defs: dict, consts: dict,
                                sha_attendu: Optional[str] = None) -> dict:
    """Rejoue le sha256 par la seconde implémentation et compare à `hashlib`.

    Trois familles de messages : le fichier du corpus, les 42 couples
    `preuve || type` (l'empreinte déclarée), et les 24 termes de
    l'environnement (3 définitions + 21 constantes, sérialisés). Aucun de ces
    calculs ne passe par `hashlib` côté seconde implémentation.
    """
    autotest = autotest_sha256_pur()
    sha_hl = hashlib.sha256(brut).hexdigest()
    sha_pur = sha256_pur(brut)
    corpus_ok = sha_pur == sha_hl
    if sha_attendu is not None:
        corpus_ok = corpus_ok and sha_pur == sha_attendu

    entrees_ok = entrees_declarees = 0
    preuves_seules_ok = types_seuls_ok = 0
    ecarts_entrees = []
    for e in corpus["entrees"]:
        try:
            p = bytes.fromhex(e["preuve_hex"])
            t = bytes.fromhex(e["type_hex"])
        except (KeyError, ValueError, TypeError):
            ecarts_entrees.append({"nom": e.get("nom"), "raison": "hex invalide"})
            continue
        couple = p + t
        pur = sha256_pur(couple)
        hl = hashlib.sha256(couple).hexdigest()
        if pur == hl:
            entrees_ok += 1
        else:
            ecarts_entrees.append({"nom": e.get("nom"), "raison": "sha pur ≠ hashlib"})
        if pur == e.get("empreinte"):
            entrees_declarees += 1
        else:
            ecarts_entrees.append({"nom": e.get("nom"), "raison": "sha pur ≠ empreinte déclarée"})
        preuves_seules_ok += int(sha256_pur(p) == hashlib.sha256(p).hexdigest())
        types_seuls_ok += int(sha256_pur(t) == hashlib.sha256(t).hexdigest())

    environnement_concordants = 0
    environnement = list(defs.items()) + list(consts.items())
    ecarts_environnement = []
    for nom, terme in environnement:
        octets = serialize(terme)
        if sha256_pur(octets) == hashlib.sha256(octets).hexdigest():
            environnement_concordants += 1
        else:
            ecarts_environnement.append(nom)

    verdict = "pass" if (
        autotest["verdict"] == "pass"
        and corpus_ok
        and entrees_ok == len(corpus["entrees"])
        and entrees_declarees == len(corpus["entrees"])
        and preuves_seules_ok == len(corpus["entrees"])
        and types_seuls_ok == len(corpus["entrees"])
        and environnement_concordants == len(environnement)
    ) else "fail"
    return {
        "implementation": "SHA-256 FIPS 180-4 réécrite dans verificateur_cic.py (sans hashlib)",
        "autotest": autotest,
        "corpus": {
            "sha256_hashlib": sha_hl,
            "sha256_pur": sha_pur,
            "sha256_attendu": sha_attendu,
            "concordant": corpus_ok,
        },
        "entrees": {
            "total": len(corpus["entrees"]),
            "concordantes_hashlib": entrees_ok,
            "empreintes_declarees_ok": entrees_declarees,
            "preuves_seules_concordantes": preuves_seules_ok,
            "types_seuls_concordants": types_seuls_ok,
            "ecarts": ecarts_entrees,
        },
        "environnement": {
            "total": len(environnement),
            "concordants_hashlib": environnement_concordants,
            "ecarts": ecarts_environnement,
        },
        "verdict": verdict,
    }


# ---------------------------------------------------------------------------
# CLI et mesure
# ---------------------------------------------------------------------------

def _tags_presents(t: tuple, acc: set[str]) -> None:
    acc.add(t[0])
    for x in t[1:]:
        if isinstance(x, tuple):
            _tags_presents(x, acc)


def _chemin_affiche(chemin: pathlib.Path) -> str:
    try:
        return str(chemin.resolve().relative_to(RACINE))
    except ValueError:
        return str(chemin)


def mesurer(chemin: pathlib.Path, sha_attendu: Optional[str] = None,
            controles: bool = True) -> dict:
    t0 = time.perf_counter()
    defs_hex, consts_hex, brut, sha = charger_corpus(chemin)
    artefact = json.loads(brut)
    defs, consts, bilan_serial = construire_environnement(defs_hex, consts_hex)
    entrees = artefact["entrees"]
    exercees: set[str] = set()
    decodage_entrees_ok = True
    for t in list(defs.values()) + list(consts.values()):
        _tags_presents(t, exercees)
    for e in entrees:
        for cle in ("preuve_hex", "type_hex"):
            try:
                _tags_presents(decode_exact(e[cle]), exercees)
            except (DecodeError, KeyError, TypeError):
                decodage_entrees_ok = False
    rejeu = rejouer({"entrees": entrees}, defs, consts)
    sha_independant = verifier_sha256_independant(
        brut, {"entrees": entrees}, defs, consts, sha_attendu)
    controles_negatifs = {}
    if controles:
        controles_negatifs = {
            "octet_altere": controle_octet_altere({"entrees": entrees}, defs, consts),
            "type_altere": controle_type_altere({"entrees": entrees}, defs, consts),
            "octet_altere_exhaustif": controle_exhaustif_petite_preuve(
                {"entrees": entrees}, defs, consts),
            "non_trivialite": controle_non_trivialite({"entrees": entrees}, defs, consts),
        }
        negatifs_ok = (
            controles_negatifs["octet_altere"]["verdict"] == "pass"
            and controles_negatifs["type_altere"]["verdict"] == "pass"
            and controles_negatifs["octet_altere_exhaustif"]["verdict"] == "pass"
            and all(v["verdict"] == "pass"
                    for v in controles_negatifs["non_trivialite"].values())
        )
    else:
        controles_negatifs = {"desactive": True}
        negatifs_ok = True
    duree = time.perf_counter() - t0

    sha_ok = (sha_attendu is None) or (sha == sha_attendu)
    serial_ok = not bilan_serial["echecs"]
    serial_entrees_ok = rejeu["serialisations_canoniques"] == rejeu["verdicts"]
    empreintes_ok = rejeu["empreintes_valides"] == rejeu["verdicts"]
    empreintes_pures_ok = rejeu["empreintes_pures_valides"] == rejeu["verdicts"]
    types_bien_formes_ok = (rejeu["types_bien_formes"] == rejeu["verdicts"]
                            and rejeu["types_clos"] == rejeu["verdicts"])
    preuves_closes_ok = rejeu["preuves_closes"] == rejeu["verdicts"]
    sha_independant_ok = sha_independant["verdict"] == "pass"
    rejeu_ok = rejeu["desaccord"] == 0 and rejeu["verdicts"] == 42
    global_ok = bool(sha_ok and serial_ok and serial_entrees_ok and decodage_entrees_ok
                     and empreintes_ok and empreintes_pures_ok
                     and types_bien_formes_ok and preuves_closes_ok
                     and sha_independant_ok and rejeu_ok and negatifs_ok)

    return {
        "tache": "B3",
        "titre": "Corpus d'or CIC v2 : type de Bruijn vérifié + sha256 rejoué par une seconde implémentation",
        "date": time.strftime("%Y-%m-%d"),
        "ligne": "L / R0.7 (le bloc langue) — chantier Panini",
        "outil": "tools/verificateur_cic.py",
        "outil_sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
        "python": sys.version.split()[0],
        "corpus": {
            "chemin": _chemin_affiche(chemin),
            "doctrine": artefact.get("doctrine"),
            "sha256": sha,
            "sha256_attendu": sha_attendu,
            "sha256_ok": sha_ok,
            "octets": len(brut),
            "source_panini": "Panini/research/nipada/falsification/corpus_dor_cic_v1.json",
            "commit_source": COMMIT_SOURCE,
            "copie_drave_byte_identique": sha == SHA256_CORPUS,
        },
        "environnement": {
            "defs": bilan_serial["defs"],
            "consts": bilan_serial["consts"],
            "serialisation_canonique": serial_ok,
            "echecs_serialisation": bilan_serial["echecs"],
        },
        "noyau": {
            "fragment": "CIC-lite portable (de Bruijn) : Π, λ, app, ℕ, Id/J, Σ, "
                        "définitions δ, constantes, unité, vide, Bool, Liste, Expr",
            "etiquettes": sorted(TAGS),
            "etiquettes_exercees": sorted(exercees),
            "etiquettes_non_exercees": sorted(set(TAGS) - exercees),
            "couverture_etiquettes": f"{len(exercees)}/{len(TAGS)}",
            "independant_de_panini": True,
        },
        "type_de_bruijn": {
            "definition": "un type valide est clos (aucun indice hors portée) et "
                          "[] ⊢ type : sort n ; la preuve est close elle aussi",
            "types_totaux": rejeu["verdicts"],
            "types_clos": rejeu["types_clos"],
            "types_bien_formes": rejeu["types_bien_formes"],
            "preuves_closes": rejeu["preuves_closes"],
            "niveaux_observes": rejeu["niveaux_types"],
            "verdict": "pass" if (types_bien_formes_ok and preuves_closes_ok) else "fail",
        },
        "sha256_independant": sha_independant,
        "resultat": rejeu,
        "integrite": {
            "sha256_corpus": sha_ok,
            "serialisation_environnement": serial_ok,
            "serialisation_entrees": serial_entrees_ok,
            "decodage_entrees": decodage_entrees_ok,
            "empreintes": empreintes_ok,
            "empreintes_pures": empreintes_pures_ok,
            "type_de_bruijn": types_bien_formes_ok,
            "preuves_closes": preuves_closes_ok,
            "sha256_seconde_implementation": sha_independant_ok,
            "verdicts": rejeu_ok,
        },
        "controles_negatifs": controles_negatifs,
        "duree_s": round(duree, 3),
        "verdict": "pass" if global_ok else "fail",
    }


def _resume_humain(m: dict) -> str:
    r = m["resultat"]
    lignes = [
        f"Corpus : {m['corpus']['chemin']}",
        f"sha256 : {m['corpus']['sha256']}"
        f"{' (attendu)' if m['corpus']['sha256_ok'] else ' — ❌ diffère de l’attendu'}",
        f"Environnement : {m['environnement']['defs']} defs, "
        f"{m['environnement']['consts']} consts, "
        f"sérialisation canonique {'✅' if m['environnement']['serialisation_canonique'] else '❌'}",
        f"Verdicts : {r['accord']}/{r['verdicts']} d’accord "
        f"({r['attendus_acceptes']} acceptés, {r['attendus_rejetes']} rejetés) "
        f"— désaccords {r['desaccord']}",
        f"Empreintes : {r['empreintes_valides']}/{r['verdicts']} valides "
        f"(hashlib) · {r['empreintes_pures_valides']}/{r['verdicts']} par la seconde implémentation",
        f"Type de Bruijn : {r['types_bien_formes']}/{r['verdicts']} types clos et bien formés "
        f"({r['preuves_closes']}/{r['verdicts']} preuves closes)",
        f"sha256 indépendant : {m['sha256_independant']['verdict']} "
        f"(corpus {'ok' if m['sha256_independant']['corpus']['concordant'] else 'KO'}, "
        f"{m['sha256_independant']['entrees']['concordantes_hashlib']}/"
        f"{m['sha256_independant']['entrees']['total']} couples, "
        f"{m['sha256_independant']['environnement']['concordants_hashlib']}/"
        f"{m['sha256_independant']['environnement']['total']} termes)",
        "Contrôles négatifs :",
    ]
    if "octet_altere" in m["controles_negatifs"]:
        a = m["controles_negatifs"]["octet_altere"]
        t = m["controles_negatifs"]["type_altere"]
        e = m["controles_negatifs"]["octet_altere_exhaustif"]
        n = m["controles_negatifs"]["non_trivialite"]
        lignes += [
            f"  octet altéré (36 preuves acceptées) : {a['rejetes_apres_mutation']}/"
            f"{a['mutations']} rejetés, {a['acceptes_apres_mutation']} accepté(s) — {a['verdict']}",
            f"  type altéré (42 entrées) : {t['rejetes_apres_mutation']}/{t['mutations']} "
            f"rejetés, {t['types_devenus_invalides']} type(s) invalide(s) — {t['verdict']}",
            f"  exhaustif {e['preuve']} : {e['rejetes_apres_mutation']}/{e['mutations']} "
            f"rejetés, {e['acceptes_apres_mutation']} accepté(s) — {e['verdict']}",
            f"  non-trivialité : accepte-tout {n['accepte_tout']['accord']}/{r['verdicts']}, "
            f"rejette-tout {n['rejette_tout']['accord']}/{r['verdicts']}",
        ]
    else:
        lignes.append("  désactivés")
    lignes.append(f"Durée : {m['duree_s']} s — VERDICT {m['verdict'].upper()}")
    return "\n".join(lignes)


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--corpus", type=pathlib.Path, default=CORPUS_DEFAUT,
                   help=f"corpus JSON (défaut : {CORPUS_DEFAUT})")
    p.add_argument("--sha256", dest="sha_attendu", default=SHA256_CORPUS,
                   help="sha256 attendu du corpus (défaut : celui de la copie Drave)")
    p.add_argument("--json", action="store_true", help="sortie machine")
    p.add_argument("--verbeux", action="store_true", help="une ligne par entrée")
    p.add_argument("--sans-controles", action="store_true",
                   help="ne pas exécuter les contrôles négatifs (rejeu seul)")
    args = p.parse_args(argv)

    try:
        sha_attendu = args.sha_attendu or None
        m = mesurer(args.corpus, sha_attendu, controles=not args.sans_controles)
    except (DecodeError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"❌ artefact illisible : {exc}", file=sys.stderr)
        return 2

    if args.verbeux and not args.json:
        for e in m["resultat"]["entrees"]:
            marque = "✅" if e["accord"] else "❌"
            print(f"  {marque} {e['nom']:<24} attendu={e['attendu']:<8} "
                  f"obtenu={e['obtenu']:<8} empreinte={'ok' if e['empreinte_ok'] else 'KO'}")
    if args.json:
        print(json.dumps(m, indent=1, ensure_ascii=False))
    else:
        print(_resume_humain(m))
    return 0 if m["verdict"] == "pass" else 1


if __name__ == "__main__":
    sys.setrecursionlimit(20000)
    raise SystemExit(main())
