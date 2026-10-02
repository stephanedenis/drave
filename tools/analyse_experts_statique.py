#!/usr/bin/env python3
"""Analyse STATIQUE des experts d'un MoE : que portent les poids eux-mêmes.

Les traces de routage disent quels experts sont *appelés*. Ce script regarde ce
qu'ils *sont* : deux experts aux poids presque identiques sont redondants, et
l'un des deux peut disparaître — c'est une économie d'empreinte qu'aucune trace
ne peut révéler.

    python3 tools/analyse_experts_statique.py <modele.gguf> --couches 0,12,24,36

Trois mesures, et ce que chacune cherche :

* **similarité entre experts** (intra-couche) — des experts jumeaux ? Si deux
  experts d'une même couche font la même chose, n'en stocker qu'un divise leur
  empreinte par deux ;
* **profil de SOURCES** — la norme de chaque colonne d'entrée. Deux experts qui
  écoutent les mêmes dimensions d'entrée ont la même source ;
* **profil de DESTINATIONS** — la norme de chaque ligne de sortie. Deux experts
  qui écrivent dans les mêmes dimensions ont la même destination.

Un couple d'experts dont les sources ET les destinations se recouvrent est un
candidat direct à la fusion — et donc à un cluster « d'experts jumeaux » qu'on
peut isoler et réduire.

Ne lit que la tête des tenseurs : sur un modèle de 18 Go, l'analyse complète de
quelques couches coûte quelques mégaoctets de lecture.
"""
import argparse
import struct
import sys

import numpy as np


class Lecteur:
    """Lecteur GGUF minimal : en-tête, descripteurs, et octets d'un tenseur."""

    def __init__(self, chemin):
        self.f = open(chemin, "rb")
        self.meta, self.tenseurs, self.debut = self._entete()

    def _u32(self):
        return struct.unpack("<I", self.f.read(4))[0]

    def _u64(self):
        return struct.unpack("<Q", self.f.read(8))[0]

    def _str(self):
        n = self._u64()
        return self.f.read(n).decode("utf-8", "replace")

    def _val(self, t):
        if t == 0: return struct.unpack("<B", self.f.read(1))[0]
        if t == 1: return struct.unpack("<b", self.f.read(1))[0]
        if t == 2: return struct.unpack("<H", self.f.read(2))[0]
        if t == 3: return struct.unpack("<h", self.f.read(2))[0]
        if t == 4: return self._u32()
        if t == 5: return struct.unpack("<i", self.f.read(4))[0]
        if t == 6: return struct.unpack("<f", self.f.read(4))[0]
        if t == 7: return struct.unpack("<B", self.f.read(1))[0] != 0
        if t == 8: return self._str()
        if t == 9:
            et = self._u32(); n = self._u64()
            return [self._val(et) for _ in range(n)]
        if t == 10: return self._u64()
        if t == 11: return struct.unpack("<q", self.f.read(8))[0]
        if t == 12: return struct.unpack("<d", self.f.read(8))[0]
        raise ValueError(f"type de métadonnée {t}")

    def _entete(self):
        f = self.f
        assert f.read(4) == b"GGUF", "ce n'est pas un GGUF"
        f.read(4)                      # version
        nt, nk = self._u64(), self._u64()
        meta = {}
        for _ in range(nk):
            k = self._str(); t = self._u32(); meta[k] = self._val(t)
        tenseurs = {}
        for _ in range(nt):
            nom = self._str()
            nd = self._u32()
            dims = [self._u64() for _ in range(nd)][::-1]      # ggml stocke à l'envers
            ttype = self._u32()
            offset = self._u64()
            tenseurs[nom] = (dims, ttype, offset)
        align = meta.get("general.alignment", 32)
        debut = (f.tell() + align - 1) // align * align
        return meta, tenseurs, debut

    def octets(self, nom, nb):
        """Les `nb` premiers octets des données d'un tenseur."""
        dims, _, offset = self.tenseurs[nom]
        self.f.seek(self.debut + offset)
        return self.f.read(nb), dims


def f16(b):
    return np.frombuffer(b, dtype=np.float16).astype(np.float32)


def dequant_q4k(bloc):
    """Q4_K : 144 octets pour 256 poids (d, dmin, 12 o de scales, 128 o de quants)."""
    d = float(f16(bloc[0:2])[0]); dmin = float(f16(bloc[2:4])[0])
    sc = np.frombuffer(bloc[4:16], dtype=np.uint8)
    qs = np.frombuffer(bloc[16:144], dtype=np.uint8)
    out = np.empty(256, dtype=np.float32)
    for g in range(4):
        for moitie in (0, 1):
            j = 2 * g + moitie
            if j < 4:
                s = sc[j] & 63; m = sc[j + 4] & 63
            else:
                s = (sc[j + 4] & 0x0F) | ((sc[j - 4] >> 6) << 4)
                m = (sc[j + 4] >> 4) | ((sc[j] >> 6) << 4)
            q = qs[g * 32:(g + 1) * 32]
            lo = (q & 0x0F).astype(np.float32) if moitie == 0 else (q >> 4).astype(np.float32)
            out[g * 64 + moitie * 32: g * 64 + moitie * 32 + 32] = d * s * lo - dmin * m
    return out


def dequant_q6k(bloc):
    """Q6_K : 210 octets pour 256 poids (ql 128, qh 64, scales 16, d 2)."""
    ql = np.frombuffer(bloc[0:128], dtype=np.uint8)
    qh = np.frombuffer(bloc[128:192], dtype=np.uint8)
    sc = np.frombuffer(bloc[192:208], dtype=np.int8).astype(np.float32)
    d = float(f16(bloc[208:210])[0])
    out = np.empty(256, dtype=np.float32)
    for l in range(32):
        is_ = l // 16
        q1 = ((ql[l] & 0x0F) | ((qh[l] & 3) << 4)).astype(np.int16) - 32
        q2 = ((ql[l + 32] & 0x0F) | (((qh[l] >> 2) & 3) << 4)).astype(np.int16) - 32
        q3 = ((ql[l] >> 4) | (((qh[l] >> 4) & 3) << 4)).astype(np.int16) - 32
        q4 = ((ql[l + 32] >> 4) | (((qh[l] >> 6) & 3) << 4)).astype(np.int16) - 32
        out[l] = d * sc[is_ + 0] * q1
        out[l + 32] = d * sc[is_ + 2] * q2
        out[l + 64] = d * sc[is_ + 4] * q3
        out[l + 96] = d * sc[is_ + 6] * q4
    return out


def lignes(octets, n_lignes, n_cols, ttype):
    """Déquantifie les `n_lignes` premières lignes d'un tenseur quantifié."""
    if ttype == 12:                       # Q4_K
        par_ligne = n_cols // 256 * 144
        return np.stack([np.concatenate([
            dequant_q4k(octets[l * par_ligne + b * 144: l * par_ligne + (b + 1) * 144])
            for b in range(n_cols // 256)]) for l in range(n_lignes)])
    if ttype == 14:                       # Q6_K
        par_ligne = n_cols // 256 * 210
        return np.stack([np.concatenate([
            dequant_q6k(octets[l * par_ligne + b * 210: l * par_ligne + (b + 1) * 210])
            for b in range(n_cols // 256)]) for l in range(n_lignes)])
    if ttype == 8:                        # Q8_0
        par_ligne = n_cols // 32 * 34
        out = []
        for l in range(n_lignes):
            bl = octets[l * par_ligne:(l + 1) * par_ligne]
            ligne = np.concatenate([f16(bl[b * 34:b * 34 + 2]) *
                                    np.frombuffer(bl[b * 34 + 2:(b + 1) * 34],
                                                  dtype=np.int8).astype(np.float32)
                                    for b in range(n_cols // 32)])
            out.append(ligne)
        return np.stack(out)
    if ttype == 0:                        # F32
        return np.frombuffer(octets[:n_lignes * n_cols * 4],
                             dtype=np.float32).reshape(n_lignes, n_cols)
    if ttype == 1:                        # F16
        return f16(octets[:n_lignes * n_cols * 2]).reshape(n_lignes, n_cols)
    raise ValueError(f"type {ttype} non géré par ce script")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("modele")
    ap.add_argument("--couches", default="0,12,24,36,47")
    ap.add_argument("--lignes", type=int, default=16,
                    help="lignes de sortie lues par expert (16 par défaut)")
    ap.add_argument("--seuil", type=float, default=0.90,
                    help="similarité au-delà de laquelle deux experts sont jumeaux")
    args = ap.parse_args()

    g = Lecteur(args.modele)
    arch = g.meta.get("general.architecture", "?")
    n_exp = g.meta.get(f"{arch}.expert_count", 0)
    print(f"{arch} · {n_exp} experts par couche · lecture de {args.lignes} lignes par expert")
    print()

    for l in (int(x) for x in args.couches.split(",")):
        noms = {s: f"blk.{l}.{s}" for s in ("ffn_gate_exps.weight", "ffn_up_exps.weight",
                                            "ffn_down_exps.weight")}
        presents = {s: n for s, n in noms.items() if n in g.tenseurs}
        if not presents:
            print(f"couche {l} : aucun tenseur d'experts")
            continue
        print(f"=== COUCHE {l} ===")
        for s, nom in presents.items():
            dims, ttype, _ = g.tenseurs[nom]
            n_exp_t, n_out, n_cols = dims[0], dims[1], dims[2]
            bloc = {12: 144, 14: 210, 8: 34, 0: 4, 1: 2}[ttype]
            par_ligne = (n_cols // 256 * bloc if ttype in (12, 14)
                         else n_cols // 32 * bloc if ttype == 8 else n_cols * bloc)
            besoin = args.lignes * par_ligne
            octets, _ = g.octets(nom, besoin * n_exp_t)
            X = np.stack([lignes(octets[e * besoin:(e + 1) * besoin],
                                 args.lignes, n_cols, ttype) for e in range(n_exp_t)])
            # Similarité entre experts, sur les lignes lues (aplaties).
            A = X.reshape(n_exp_t, -1)
            A = A - A.mean(axis=1, keepdims=True)
            norme = np.linalg.norm(A, axis=1, keepdims=True)
            norme[norme == 0] = 1
            An = A / norme
            S = An @ An.T
            np.fill_diagonal(S, -1)
            paires = [(S[i, j], i, j) for i in range(n_exp_t) for j in range(i + 1, n_exp_t)]
            paires.sort(reverse=True)
            jumelles = [p for p in paires if p[0] >= args.seuil]
            print(f"  {s.split('.')[0][4:]:5s} [{n_exp_t}, {n_out}, {n_cols}] : "
                  f"similarité max {paires[0][0]:.3f} (experts {paires[0][1]}/{paires[0][2]}) · "
                  f"médiane {np.median([p[0] for p in paires]):.3f} · "
                  f"{len(jumelles)} paires ≥ {args.seuil}")
            # SOURCES : quelles dimensions d'ENTRÉE portent le poids, en moyenne
            # sur les experts. DESTINATIONS : quelles dimensions de SORTIE.
            # On regarde des profils, pas des valeurs.
            src = np.abs(X).mean(axis=(0, 1))          # un nombre par colonne
            dst = np.abs(X).mean(axis=(0, 2))          # un nombre par ligne lue
            def concentre(v, nom):
                a = v + 1e-12
                cum = np.cumsum(np.sort(a)[::-1]) / a.sum()
                n80 = int(np.searchsorted(cum, 0.80)) + 1
                print(f"         {nom:12s} : {n80}/{len(v)} portent 80 % "
                      f"({100*n80/len(v):4.1f} %) · max/min {a.max()/max(a.min(),1e-9):8.1f}")
            concentre(src, "sources")
            concentre(dst, "destinations")
        print()

    print("Lecture : une similarité proche de 1 entre deux experts d'une même couche")
    print("signifie qu'ils calculent la même chose — l'un des deux est dupliqué.")
    print("Les paires au-dessus du seuil sont les « experts jumeaux » à isoler dans")
    print("un cluster qu'on peut réduire.")


if __name__ == "__main__":
    main()
