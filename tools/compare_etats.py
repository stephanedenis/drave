#!/usr/bin/env python3
"""Compare les états intermédiaires de Drave à ceux de llama.cpp, tenseur par tenseur.

Deux formats en entrée :

* **Drave** — `DRAVE_DUMP_COUCHES=<préfixe>` écrit des f32 bruts :
  `<préfixe>-<nom>-<couche>-<position>.bin`, sans en-tête.
* **llama.cpp** — `REF_DUMP=<préfixe> ./tools/ref_logits …` écrit
  `<préfixe>-<nom>-<couche>.bin` avec un en-tête `REFD`, `ndim`, `ne[4]`, puis
  les f32 dans l'ordre ggml (une colonne par position).

La comparaison porte sur les **vecteurs entiers**, pas sur huit valeurs : c'est
ce qui distingue « ça a l'air proche » de « c'est le même calcul ».

Usage :
    python3 tools/compare_etats.py <préfixe_drave> <préfixe_ref> <nom> <couche> <positions>

Exemple :
    python3 tools/compare_etats.py /tmp/v4flash /tmp/ref_v4flash l_last 0 0,1,2,3
"""
import struct
import sys


def lire_drave(chemin):
    with open(chemin, "rb") as f:
        b = f.read()
    return list(struct.unpack(f"<{len(b) // 4}f", b))


def lire_ref(chemin):
    with open(chemin, "rb") as f:
        b = f.read()
    if b[:4] != b"REFD":
        raise SystemExit(f"{chemin} : magie REFD absente")
    ndim = struct.unpack("<i", b[4:8])[0]
    ne = struct.unpack("<4i", b[8:24])[0:ndim]
    n = 1
    for d in ne:
        n *= d
    vals = struct.unpack(f"<{n}f", b[24:24 + 4 * n])
    return ne, list(vals)


def main():
    if len(sys.argv) != 6:
        raise SystemExit(__doc__)
    pd, pr, nom, couche, positions = sys.argv[1:6]
    ne, ref = lire_ref(f"{pr}-{nom}-{couche}.bin")
    n_embd = ne[0]
    # Deux dispositions selon le tenseur : `l_last` est [embd, hc, position],
    # `hc_attn_pre` est [embd, position] (le mélange est déjà fait). Confondre
    # les deux compare des copies à des jetons — et « longueurs différentes »
    # est alors le seul avertissement.
    par_position = (ne[1] * (ne[2] if len(ne) > 2 else 1)) == 1 or ne[1] == 1 \
        or (len(ne) > 2 and ne[2] == 1)
    hc = 1 if par_position else ne[1]
    print(f"# {nom}-{couche} : référence ne={ne} → {n_embd} valeurs × "
          f"{'1 par position' if par_position else str(hc) + ' copies'}")
    for p in (int(x) for x in positions.split(",")):
        d = lire_drave(f"{pd}-{nom}-{couche}-{p}.bin")
        # llama.cpp : ne0 = embd (rapide), puis les copies, puis la position.
        base = p * n_embd * hc
        r = ref[base:base + n_embd * hc]
        if len(d) != len(r):
            print(f"  pos {p} : LONGUEURS DIFFÉRENTES — Drave {len(d)}, référence {len(r)}")
            continue
        ecarts = [abs(a - b) for a, b in zip(d, r)]
        mx = max(ecarts)
        imax = ecarts.index(mx)
        dyn = max(abs(x) for x in r) or 1.0
        # corrélation : le seul chiffre qui distingue « décalé » de « faux »
        md = sum(d) / len(d)
        mr = sum(r) / len(r)
        num = sum((a - md) * (b - mr) for a, b in zip(d, r))
        den = (sum((a - md) ** 2 for a in d) * sum((b - mr) ** 2 for b in r)) ** 0.5
        corr = num / den if den > 0 else float("nan")
        verdict = "✅" if mx <= 1e-4 * dyn else ("~" if corr > 0.999 else "❌")
        print(f"  pos {p} : écart max {mx:.3e} (indice {imax}, dynamique {dyn:.3e}) · "
              f"corrélation {corr:.6f} {verdict}")


if __name__ == "__main__":
    main()
