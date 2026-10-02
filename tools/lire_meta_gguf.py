#!/usr/bin/env python3
"""Lit les métadonnées d'un GGUF (en-tête seul) et imprime les clés demandées.

Pourquoi un outil séparé : le moteur expose `--tensors` (inventaire) et
`--config` (résumé), mais ni l'un ni l'autre ne montre une **liste** de
métadonnées — et certaines décisions d'architecture tiennent à une liste
(`compress_ratios` : quelles couches sont compressées, et à quel ratio).

Usage :
    python3 tools/lire_meta_gguf.py <fichier.gguf> [motif ...]

Sans motif, imprime toutes les clés et leurs valeurs (tronquées).
"""
import struct
import sys

TYPES = {0: "u8", 1: "i8", 2: "u16", 3: "i16", 4: "u32", 5: "i32",
         6: "f32", 7: "bool", 8: "str", 9: "array", 10: "u64", 11: "i64", 12: "f64"}
FIXES = {0: ("<B", 1), 1: ("<b", 1), 2: ("<H", 2), 3: ("<h", 2), 4: ("<I", 4),
         5: ("<i", 4), 6: ("<f", 4), 7: ("<?", 1), 10: ("<Q", 8), 11: ("<q", 8),
         12: ("<d", 8)}


class Lecteur:
    def __init__(self, chemin):
        self.f = open(chemin, "rb")

    def octets(self, n):
        b = self.f.read(n)
        if len(b) != n:
            raise EOFError("fin de fichier")
        return b

    def scalaire(self, t):
        fmt, taille = FIXES[t]
        return struct.unpack(fmt, self.octets(taille))[0]

    def chaine(self):
        n = struct.unpack("<Q", self.octets(8))[0]
        return self.octets(n).decode("utf-8", "replace")

    def valeur(self, t):
        if t == 8:
            return self.chaine()
        if t == 9:
            et = struct.unpack("<I", self.octets(4))[0]
            n = struct.unpack("<Q", self.octets(8))[0]
            vals = [self.valeur(et) for _ in range(n)]
            return vals
        return self.scalaire(t)


def lire(chemin, motifs):
    r = Lecteur(chemin)
    if r.octets(4) != b"GGUF":
        raise SystemExit("ce n'est pas un GGUF")
    version = struct.unpack("<I", r.octets(4))[0]
    n_tensors, n_kv = struct.unpack("<QQ", r.octets(16))
    print(f"# {chemin}\n# version {version} · {n_tensors} tenseurs · {n_kv} paires clé/valeur")
    for _ in range(n_kv):
        cle = r.chaine()
        t = struct.unpack("<I", r.octets(4))[0]
        v = r.valeur(t)
        if motifs and not any(m in cle for m in motifs):
            continue
        if isinstance(v, list) and len(v) > 64:
            v = v[:64] + [f"… (+{len(v) - 64})"]
        print(f"{cle} = {v}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    lire(sys.argv[1], sys.argv[2:])


def lire_tenseur_f32(chemin, motif, index):
    """Lit un tenseur F32 par nom (recherche par sous-chaîne) et le renvoie en
    liste de f32. Sert à sortir une NORME ou une ÉCHELLE du GGUF pour recalculer
    une étape hors du moteur — ce qui a permis de localiser l'écart CSA."""
    r = Lecteur(chemin)
    if r.octets(4) != b"GGUF":
        raise SystemExit("ce n'est pas un GGUF")
    version = struct.unpack("<I", r.octets(4))[0]
    n_tensors, n_kv = struct.unpack("<QQ", r.octets(16))
    alignement = 32
    for _ in range(n_kv):
        cle = r.chaine()
        t = struct.unpack("<I", r.octets(4))[0]
        v = r.valeur(t)
        if cle == "general.alignment":
            alignement = int(v)
    infos = []
    for _ in range(n_tensors):
        nom = r.chaine()
        nd = struct.unpack("<I", r.octets(4))[0]
        dims = [struct.unpack("<Q", r.octets(8))[0] for _ in range(nd)]
        ttype = struct.unpack("<I", r.octets(4))[0]
        off = struct.unpack("<Q", r.octets(8))[0]
        infos.append((nom, dims, ttype, off))
    # La section de données commence après l'en-tête, ALIGNÉE : lire un tenseur
    # sans ce décalage donne des valeurs absurdes (−5,8e26 pour une norme), ce
    # qui est heureusement très visible.
    fin_entete = r.f.tell()
    donnees = (fin_entete + alignement - 1) // alignement * alignement
    cible = [i for i in infos if motif in i[0]]
    if not cible:
        raise SystemExit(f"aucun tenseur ne contient « {motif} »")
    nom, dims, ttype, off = cible[0]
    n = 1
    for d in dims:
        n *= d
    base = donnees + off
    if ttype != 0:   # F32
        raise SystemExit(f"{nom} : type {ttype}, pas F32 (ce lecteur ne fait que F32)")
    r.f.seek(base)
    return nom, dims, list(struct.unpack(f"<{n}f", r.octets(4 * n)))
