#!/usr/bin/env python3
"""decoupe_langues.py — découper un panel de langues par ÉCRITURE, déduite du texte.

Un découpage « à la main » n'est ni reproductible ni vérifiable. Ici l'écriture est
déduite des POINTS DE CODE du texte lui-même : on compte les caractères par bloc
Unicode et on garde le bloc dominant. On peut alors tenir à l'écart un panel
STRATIFIÉ — chaque écriture représentée — au lieu d'un panel qui serait, comme
précédemment, uniquement non latin.

Usage : decoupe_langues.py <dossier de .txt> [--test 20] [--val 40] [--graine 5]
"""
import glob, json, os, sys, unicodedata
from collections import Counter, defaultdict


BLOCS = [
    (0x0041, 0x024F, "latin"), (0x0370, 0x03FF, "grec"), (0x0400, 0x04FF, "cyrillique"),
    (0x0530, 0x058F, "armenien"), (0x0590, 0x05FF, "hebreu"), (0x0600, 0x06FF, "arabe"),
    (0x0900, 0x097F, "devanagari"), (0x0980, 0x09FF, "bengali"), (0x0A00, 0x0A7F, "gurmukhi"),
    (0x0B80, 0x0BFF, "tamoul"), (0x0C00, 0x0C7F, "telougou"), (0x0D00, 0x0D7F, "malayalam"),
    (0x0E00, 0x0E7F, "thai"), (0x0E80, 0x0EFF, "lao"), (0x1000, 0x109F, "birman"),
    (0x10A0, 0x10FF, "georgien"), (0x1200, 0x137F, "ethiopien"), (0x1780, 0x17FF, "khmer"),
    (0x3040, 0x30FF, "japonais"), (0x4E00, 0x9FFF, "cjk"), (0xAC00, 0xD7AF, "coreen"),
    (0x0F00, 0x0FFF, "tibetain"), (0x1800, 0x18AF, "mongol"), (0x10300, 0x1032F, "etrusque"),
]


def bloc(texte):
    c = Counter()
    for ch in texte:
        p = ord(ch)
        if p < 0x41:
            continue
        for lo, hi, nom in BLOCS:
            if lo <= p <= hi:
                c[nom] += 1
                break
    return c.most_common(1)[0][0] if c else "inconnu"


def main():
    d = sys.argv[1]
    n_test = int(sys.argv[sys.argv.index("--test")+1]) if "--test" in sys.argv else 20
    n_val = int(sys.argv[sys.argv.index("--val")+1]) if "--val" in sys.argv else 40
    graine = int(sys.argv[sys.argv.index("--graine")+1]) if "--graine" in sys.argv else 5
    par_ecriture = defaultdict(list)
    for f in sorted(glob.glob(os.path.join(d, "*.txt"))):
        L = os.path.basename(f)[:-4]
        t = open(f, encoding="utf-8", errors="replace").read()
        par_ecriture[bloc(t)].append(L)
    print(f"# {sum(len(v) for v in par_ecriture.values())} langues · "
          f"{len(par_ecriture)} écritures")
    for e, ls in sorted(par_ecriture.items(), key=lambda x: -len(x[1])):
        print(f"    {e:<12} {len(ls):>4}  {' '.join(ls[:8])}{' …' if len(ls) > 8 else ''}")
    import random
    rng = random.Random(graine)
    test, val = [], []
    for e, ls in sorted(par_ecriture.items()):
        ls = sorted(ls); rng.shuffle(ls)
        # un panel STRATIFIÉ : chaque écriture fournit sa part
        k = max(1, round(n_test*len(ls)/sum(len(v) for v in par_ecriture.values())))
        test += ls[:k]
        val += ls[k:k+max(1, round(n_val*len(ls)/sum(len(v) for v in par_ecriture.values())))]
    reste = [L for ls in par_ecriture.values() for L in ls if L not in set(test) | set(val)]
    print(f"\n# TEST {len(test)} · VALIDATION {len(val)} · APPRENTISSAGE {len(reste)}")
    print(f"# écritures du TEST : "
          f"{ {e: sum(1 for L in test if L in par_ecriture[e]) for e in par_ecriture} }")
    json.dump({"test": sorted(test), "validation": sorted(val), "train": sorted(reste)},
              open("/tmp/decoupe392.json", "w"), indent=1)
    print("# /tmp/decoupe392.json écrit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
