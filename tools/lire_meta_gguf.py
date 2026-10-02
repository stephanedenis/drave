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
