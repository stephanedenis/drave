#!/usr/bin/env python3
"""corpus_propre.py — un corpus sans répétition, et un split qui ne fuit pas.

POURQUOI. N2.d a mesuré que **32,8 %** des fenêtres du protocole de validation
apparaissent **verbatim** dans l'entraînement : le corpus empile des passages qui se
recopient (127 blocs contigus, jusqu'à 1,8 Ko). Toute PPL mesurée sur ce jeu est donc
une PPL de mémoire, pas de généralisation — et 2,7078 comme 2,6998 sont mesurées dessus.

CE QUE FAIT L'OUTIL.

1. **Déduplication par shingles.** On roule un hachage de Rabin-Karp sur des fenêtres de
   `--fenetre` octets (96 par défaut). La première occurrence d'un shingle est gardée ;
   toute position couverte par un shingle déjà vu est retirée. Conséquence : après
   nettoyage, **aucune fenêtre de 128 octets ne se répète** dans le texte — donc aucune
   fenêtre de validation ne peut apparaître dans l'entraînement.
2. **Split par chunks contigus.** Le texte nettoyé est découpé en chunks de `--chunk`
   octets ; un chunk sur `--val` va en validation, le suivant en test, le reste en
   entraînement. Les fenêtres d'évaluation sont tirées **dans** leur fichier : elles ne
   traversent jamais une frontière.
3. **Vérification.** On recompte, sur le fichier produit, combien de fenêtres de
   validation apparaissent verbatim dans l'entraînement — le chiffre doit être **zéro**.
   On mesure aussi la queue de distribution : la plus longue répétition résiduelle.

Le manifeste (`reports/corpus-propre.json`) porte les tailles, les sha256, les taux et
la licence à vérifier.

Usage :
  python3 tools/corpus_propre.py --source data/corpus_fr.txt \
      --sortie data/corpus_propre --manifeste reports/corpus-propre.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

BASE, MOD = 257, (1 << 61) - 1


def hachages(data: bytes, fenetre: int) -> list[int]:
    """Hachage roulant de toutes les fenêtres de `fenetre` octets (Rabin-Karp)."""
    n = len(data)
    if n < fenetre:
        return []
    puissance = pow(BASE, fenetre - 1, MOD)
    h = 0
    for i in range(fenetre):
        h = (h * BASE + data[i]) % MOD
    out = [h]
    for i in range(fenetre, n):
        h = (h - data[i - fenetre] * puissance) % MOD
        h = (h * BASE + data[i]) % MOD
        out.append(h)
    return out


def couverture(hs: list[int], fenetre: int) -> list[bool]:
    """Vrai pour chaque position couverte par un shingle déjà vu plus tôt."""
    n = len(hs) + fenetre - 1
    premier: dict[int, int] = {}
    marque = [False] * len(hs)
    for i, h in enumerate(hs):
        j = premier.get(h)
        if j is None:
            premier[h] = i
        elif i - j >= fenetre:  # vraie répétition, pas le recouvrement de la fenêtre
            marque[i] = True
    # dilater : une fenêtre marquée couvre ses `fenetre` octets
    couvert = [False] * n
    portee = 0
    for i in range(n):
        if i < len(marque) and marque[i]:
            portee = fenetre
        if portee > 0:
            couvert[i] = True
            portee -= 1
    return couvert


def deduit(data: bytes, fenetre: int, min_run: int = 64) -> tuple[bytes, dict]:
    hs = hachages(data, fenetre)
    couvert = couverture(hs, fenetre)
    # garder les runs non couverts d'au moins min_run octets
    morceaux, stats = [], {"retires": 0, "runs": 0, "plus_long_run": 0}
    i, n = 0, len(data)
    while i < n:
        if not couvert[i]:
            j = i
            while j < n and not couvert[j]:
                j += 1
            if j - i >= min_run:
                morceaux.append(data[i:j])
                stats["runs"] += 1
                stats["plus_long_run"] = max(stats["plus_long_run"], j - i)
            else:
                stats["retires"] += j - i
            i = j
        else:
            j = i
            while j < n and couvert[j]:
                j += 1
            stats["retires"] += j - i
            i = j
    return b"\n".join(morceaux), stats


def decoupe(texte: bytes, chunk: int) -> list[bytes]:
    return [texte[i:i + chunk] for i in range(0, len(texte), chunk)]


def split(chunks: list[bytes], val_un_sur: int, test_un_sur: int):
    train, val, test = [], [], []
    for i, c in enumerate(chunks):
        if i % val_un_sur == val_un_sur - 1:
            val.append(c)
        elif i % test_un_sur == test_un_sur - 2:  # décalé : sinon val et test se recouvrent
            test.append(c)
        else:
            train.append(c)
    return b"".join(train), b"".join(val), b"".join(test)


def taux_contamination(train: bytes, val: bytes, fenetre: int = 128, pas: int = 64,
                       maxi: int | None = None) -> dict:
    n = len(val) - fenetre - 1
    positions = list(range(0, max(0, n), pas))
    if maxi:
        positions = positions[:maxi]
    touchees = sum(1 for j in positions if val[j:j + fenetre + 1] in train)
    return {"fenetres": len(positions), "contaminees": touchees,
            "taux": round(touchees / max(1, len(positions)), 4)}


def plus_longue_repetition(train: bytes, val: bytes, essais: int = 40, graine: int = 0) -> int:
    """Plus longue extension d'une fenêtre de validation retrouvée dans l'entraînement."""
    import random
    rng = random.Random(graine)
    n = len(val) - 129
    if n <= 0:
        return 0
    pire = 0
    for _ in range(essais):
        j = rng.randrange(0, n)
        w = val[j:j + 129]
        p = train.find(w)
        if p < 0:
            continue
        g = 0
        while j - g > 0 and p - g > 0 and val[j - g - 1] == train[p - g - 1]:
            g += 1
        d = 0
        while (j + 129 + d < len(val) and p + 129 + d < len(train)
               and val[j + 129 + d] == train[p + 129 + d]):
            d += 1
        pire = max(pire, g + 129 + d)
    return pire


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="data/corpus_fr.txt")
    ap.add_argument("--sortie", default="data/corpus_propre")
    ap.add_argument("--manifeste", default="reports/corpus-propre.json")
    ap.add_argument("--fenetre", type=int, default=96)
    ap.add_argument("--chunk", type=int, default=8192)
    ap.add_argument("--val", type=int, default=20)
    ap.add_argument("--test", type=int, default=20)
    ap.add_argument("--verif-max", type=int, default=None,
                    help="borne le nombre de fenêtres vérifiées (gros corpus)")
    a = ap.parse_args()

    source = pathlib.Path(a.source)
    data = source.read_bytes()
    propre, stats = deduit(data, a.fenetre)
    chunks = decoupe(propre, a.chunk)
    train, val, test = split(chunks, a.val, a.test)
    val_chunks = [i for i in range(len(chunks)) if i % a.val == a.val - 1]
    test_chunks = [i for i in range(len(chunks)) if i % a.test == a.test - 2]
    sortie = pathlib.Path(a.sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    for nom, contenu in (("train", train), ("val", val), ("test", test)):
        (sortie / f"{nom}.txt").write_bytes(contenu)

    contam = taux_contamination(train, val, maxi=a.verif_max)
    contam_test = taux_contamination(train, test, maxi=a.verif_max)
    plus_long = plus_longue_repetition(train, val)
    manifeste = {
        "source": str(source),
        "source_octets": len(data),
        "source_sha256": hashlib.sha256(data).hexdigest(),
        "methode": {
            "deduplication": "shingles de Rabin-Karp (base 257, mod 2^61−1), première "
                             "occurrence gardée, runs gardés ≥ 64 octets, joints par \\n",
            "fenetre_shingle": a.fenetre,
            "chunk_octets": a.chunk,
            "split": f"un chunk sur {a.val} en validation, le suivant sur {a.test} en test",
        },
        "propre_octets": len(propre),
        "deduplication": {**stats, "retires_pct": round(100 * stats["retires"] / len(data), 2)},
        "train_octets": len(train), "val_octets": len(val), "test_octets": len(test),
        "chunks": {"train": len(chunks) - len(val_chunks) - len(test_chunks),
                   "val": len(val_chunks), "test": len(test_chunks)},
        "sha256": {nom: hashlib.sha256(c).hexdigest()
                   for nom, c in (("train", train), ("val", val), ("test", test))},
        "contamination": {"validation": contam, "test": contam_test},
        "plus_longue_repetition_val_train": plus_long,
        "licence": "corpus local, licence à vérifier — ne pas diffuser",
        "note": "les corpus de data/ ne sont pas versionnés ; ce manifeste porte leur empreinte",
    }
    pathlib.Path(a.manifeste).write_text(json.dumps(manifeste, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({k: manifeste[k] for k in
                      ("source_octets", "propre_octets", "train_octets", "val_octets",
                       "test_octets", "deduplication", "contamination")},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
