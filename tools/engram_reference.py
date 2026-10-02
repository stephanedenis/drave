#!/usr/bin/env python3
"""Référence **Python** de l'adressage de l'engram de DeepSeek-V4.1.

Transcription de `vllm/models/deepseek_v4_1/common/engram.py` **via** son portage
1:1 en C++ (`mudler/vllm.cpp`, `deepseek_v4_1_engram.cpp`) : les noms de
fonctions et les commentaires citent les lignes de l'original.

Ce que ce script calcule : pour chaque jeton d'une séquence, la **rangée** à
lire dans chacune des deux tables d'engram (couches 1 et 14), pour chacune des
`n_hash_cols = (max_ngram - 1) × n_heads = 24` colonnes de hachage. C'est la
« liste d'adresses » du plan (P8).

Ce qu'il ne calcule pas : la lecture des rangées (e4m3 × e8m0) ni l'injection.
Ils viendront après, contre la même référence.

Les trois détails qui portent tout le comportement — et qu'aucune
reconnaissance de forme ne devinerait :

1. le repli se fait par **OU exclusif** (`^=`), pas par somme ;
2. `blocked` est **collant** : dès qu'un n-gramme est cassé (début de séquence,
   jeton mort), tous les reculs plus profonds sont remplacés par le pad ;
3. le modulo se fait **par colonne** — premier et offset propres à chaque
   (couche, groupe de recul, tête).

Usage :
    python3 tools/engram_reference.py            # auto-test (invariants)
    python3 tools/engram_reference.py --json F   # écrit les adresses d'une
                                                 # séquence d'essai
"""
import json
import struct
import sys

# `kEngramDeadId` : le portage C++ le définit à côté du pad ; un jeton mort
# (masqué) n'est pas un jeton ordinaire, c'est un trou.
K_ENGRAM_DEAD_ID = -1


def is_prime(n):
    """`engram.py:63-85` — Miller-Rabin déterministe pour n < 2^32.

    Le portage C++ **reproduit un défaut d'origine** et le documente : avec les
    témoins (2, 7, 61), `_is_prime(61)` est **faux** (61 est multiple du
    témoin), et 61 est la seule valeur sous 2000 où l'algorithme se trompe.
    On le reproduit ici pour la même raison que lui : un portage qui diverge
    silencieusement de son oracle sur une entrée ne prouve rien sur les autres.
    """
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 7, 61):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def find_next_prime(start, seen):
    """`engram.py:88-93` — le premier suivant NON DÉJÀ VU (`seen` est partagé
    entre toutes les couches et tous les groupes : deux colonnes ne partagent
    jamais un premier, les intervalles de seaux restent disjoints)."""
    c = start + 1
    while True:
        if is_prime(c) and c not in seen:
            return c
        c += 1


def layout_depuis_metadonnees(vocab_size, layer_ids, max_ngram_size, n_heads,
                              compressed_vocab_size, pad_token_id):
    """`engram.py:178-210` — les 48 premiers et les offsets, recalculés.

    Le redémarrage de `current` à `vocab_size - 1` à chaque groupe est **inerte**
    (la recherche avance et saute les déjà-vus) mais on le garde : c'est ce
    qu'écrit l'original, et un portage qui « simplifie » ce qui ne change rien
    finit par simplifier ce qui change quelque chose.
    """
    n_hash_cols = (max_ngram_size - 1) * n_heads
    seen, primes = [], []
    for _ in layer_ids:
        for _groupe in range(max_ngram_size - 1):
            current = vocab_size - 1
            for _tete in range(n_heads):
                current = find_next_prime(current, seen)
                seen.append(current)
                primes.append(current)
    offsets = []
    for _ in layer_ids:
        courant = 0
        for col in range(n_hash_cols):
            offsets.append(courant)
            courant += primes[len(offsets) - 1]
    return primes, offsets


def hachage(token_map, primes, offsets, multipliers, token_ids, positions,
            layer_ids, max_ngram_size, n_heads, pad_token_id,
            dead_mask=None, chunk_start=None):
    """`engram.py:248-380` — la liste d'adresses, pour UNE séquence.

    `token_ids[i]` est le jeton à `positions[i]` (le cas d'un préremplissage
    complet : tout est « dans le lot », donc le palier 1 de la référence suffit).
    Rend, pour chaque jeton, `n_layers × n_hash_cols` indices de rangée.
    """
    n_layers = len(layer_ids)
    n_hash_cols = (max_ngram_size - 1) * n_heads
    if dead_mask is None:
        dead_mask = [0] * len(token_ids)
    pad_id = token_map[pad_token_id]
    sortie = []
    for token in range(len(token_ids)):
        position = positions[token]
        debut_lot = positions[0] if chunk_start is None else chunk_start
        rolling = [0] * n_layers
        bloc = [0] * (n_layers * n_hash_cols)
        blocked = False
        for shift in range(max_ngram_size):
            lookback = position - shift
            source = pad_id
            if lookback >= debut_lot:
                i = token - shift
                if i >= 0:
                    source = (K_ENGRAM_DEAD_ID if dead_mask[i]
                              else token_map[token_ids[i]])
            # COLLANT : une fois cassé, tous les reculs plus profonds le sont.
            blocked = blocked or lookback < 0 or source == K_ENGRAM_DEAD_ID
            value = pad_id if blocked else source
            for layer in range(n_layers):
                rolling[layer] ^= value * multipliers[layer * max_ngram_size + shift]
                if shift == 0:
                    continue
                for head in range(n_heads):
                    col = (shift - 1) * n_heads + head
                    idx = layer * n_hash_cols + col
                    bloc[layer * n_hash_cols + col] = (
                        rolling[layer] % primes[idx] + offsets[idx])
        sortie.append(bloc)
    return sortie


def _auto_test():
    """Les invariants que la référence affirme, vérifiés ici."""
    # 1. Le défaut reproduit : 61 n'est pas premier pour cet algorithme.
    assert is_prime(61) is False, "le défaut d'origine (61) doit être reproduit"
    assert is_prime(59) is True and is_prime(60) is False
    # 2. Le layout se recalcule et les 48 premiers sont distincts.
    primes, offsets = layout_depuis_metadonnees(16_000_000, [1, 14], 4, 8, 99_092, 2)
    assert len(primes) == 48, len(primes)
    assert len(set(primes)) == 48, "deux colonnes partagent un premier"
    assert primes == sorted(primes), "les premiers doivent croître globalement"
    assert offsets[0] == 0
    # 3. Le hachage : un jeton seul ne remplit que la colonne shift=1..3, et
    #    deux séquences identiques donnent les mêmes adresses.
    tok = [5, 6, 7, 8]
    tokmap = list(range(99_092))          # identité : dense, comme celle du fichier
    mult = [3, 5, 7, 11, 13, 17, 19, 23]
    a = hachage(tokmap, primes, offsets, mult, tok, [0, 1, 2, 3], [1, 14], 4, 8, 2)
    b = hachage(tokmap, primes, offsets, mult, tok, [0, 1, 2, 3], [1, 14], 4, 8, 2)
    assert a == b, "le hachage doit être déterministe"
    assert len(a) == 4 and len(a[0]) == 48
    # 4. Toutes les adresses tombent dans les bornes de leur colonne.
    for jeton in a:
        for couche in range(2):
            for col in range(24):
                idx = couche * 24 + col
                v = jeton[idx]
                assert offsets[idx] <= v < offsets[idx] + primes[idx], (idx, v)
    print("auto-test : ok — 48 premiers distincts, adresses bornées, "
          "hachage déterministe, défaut d'origine reproduit")


if __name__ == "__main__":
    if "--json" in sys.argv:
        f = sys.argv[sys.argv.index("--json") + 1]
        # Séquence d'essai : les identifiants sont choisis < len(token_map).
        ids = [((i * 7919) % 99_000) for i in range(10_000)]
        mult = [((i * 2654435761) | 1) % (2**31) for i in range(8)]
        primes, offsets = layout_depuis_metadonnees(16_000_000, [1, 14], 4, 8, 99_092, 2)
        # La table de correspondance d'essai est l'identité (dense sur [0, 99 092)).
        tokmap = list(range(99_092))
        adr = hachage(ids, primes, offsets, mult, ids, list(range(10_000)),
                      [1, 14], 4, 8, 2)
        with open(f, "w") as g:
            json.dump({"ids": ids, "multipliers": mult, "primes": primes,
                       "offsets": offsets, "adresses": adr}, g)
        print(f"{len(adr)} jetons × 48 adresses écrits dans {f}")
    else:
        _auto_test()
