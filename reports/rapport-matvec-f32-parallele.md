# Rapport — Le produit matrice-vecteur f32 de V4.1 : ×9,34 sur l'attention, sans changer un bit

02/10 (bloc 15), pas complet V4.1 sur `/home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf`
(365,71 Go, 40 couches), 20 fils, 4 jetons, ctx 8, 8 bits d'activation.

**Verdict en une ligne : les 12,4 s par jeton du poste « attention » étaient un
produit matrice-vecteur **mono-fil** sur une machine à vingt cœurs ; le découper
par **lignes** donne ×9,34 sur le poste et ×3 sur la passe, avec une perplexité et
des vides **identiques au bit près**.**

## 1. Ce que le profil disait, et ce qu'il cachait

```
postes (ms/token) : projets-attn 0.00 | rope 0.00 | attention 12369.91 | proj+mlp 9383.19 | total 21753
dont attention : scores 0.00 | softmax 0.00 | somme pondérée + écriture KV 12369.91
```

Les deux sous-compteurs à zéro sont ceux de l'AUTRE chemin d'attention (le MLA de
V3, `prof[4]`/`prof[5]`) : sur V4.1, la totalité d'`attn_v4` — projections q/kv,
compresseur, indexeur, scores, softmax, somme pondérée — tombait dans `prof[2]`,
sous une étiquette qui ne décrit que sa dernière partie. Le poste n'était donc pas
« la somme pondérée » : c'était tout.

Contrôle par isolement, sans instrumenter une ligne : `--moe-topk 1` (MoE réduit
~6×) laisse le poste à **7 283,42 ms/token** — il ne bouge pas d'un ordre, il est
bien dans `attn_v4`, et il perd 5 s du seul fait de la contention de cœurs avec le
MoE.

## 2. La cause : `matvec_f32`, onze fois par couche, sur un fil

```rust
fn matvec_f32(w: &[f32], x: &[f32], n_in: usize, n_out: usize, y: &mut [f32]) {
    for o in 0..n_out {
        let ligne = &w[o * n_in..(o + 1) * n_in];
        let mut acc = 0f32;
        for i in 0..n_in { acc += ligne[i] * x[i]; }
        y[o] = acc;
    }
}
```

Appelée par `attn_v4` (q_a, q_b, kv, `comp_kv`, `comp_gate`, indexeur, sortie
groupée), par le `wkv` de l'engram ([25 600, 6 144] = 157 M de produits par
couche et par jeton) et par `forward_mla`. Ordre de grandeur pour V4.1 :
**~41 M de produits par couche et par jeton**, soit 1,65 G par jeton — pour un
seul fil, à ~0,13 GFLOP/s effectif.

## 3. Le correctif : parallèle par LIGNES

`matvec_f32_fils(w, x, n_in, n_out, y, n_fils)` découpe les **lignes de sortie**
en tranches contiguës (même schéma que le noyau d'experts) : chaque ligne est
sommée par un seul fil, dans le même ordre. Aucune réassociation n'est
introduite, donc **le résultat est identique au bit près** — c'est la seule forme
d'accélération qui ne change pas le calcul, et elle n'a rien à annoncer.

Deux garde-fous repris du noyau d'experts, tous deux nés d'un bug réel du dépôt :
la tranche du fil s'indexe par `o - o0` (l'index global levait « len is 256 but
the index is 256 » dès le deuxième fil), et un seuil (`n_out × n_in < 65 536`)
évite de payer un `spawn` (~30 µs) pour un petit produit.

## 4. Mesures

| mesure | avant | après |
|---|---|---|
| poste `attention` | 12 369,91 ms/token | **1 324,48 ms/token** (×9,34) |
| poste `proj+mlp` | 9 383,19 | 5 945,70 (×1,58 — contention de cœurs en moins) |
| total | 21 753,10 ms/token | **7 270,18 ms/token** (×2,99) |
| durée de la passe (4 jetons, ctx 8) | 66-68 s | **22,2 s** |
| perplexité | 1 743 713,6243 | **1 743 713,6243** |
| vides, 2 544 tenseurs | — | **0 différent** |

La comparaison de vides porte sur tout ce que la passe écrit (q, kv, attention,
compresseur, indexeur, hyper-connexions, engram, MoE par les états de couche) :
l'égalité au bit près est donc établie là où le moindre changement de sommation se
verrait.

## 5. Le gain de bout en bout à contexte plus long

Même commande que l'A/B de l'engram du bloc 14 (31 jetons, ctx 32, 8 bits) :

| mesure | avant | après |
|---|---|---|
| durée de la passe | 313,1 s | **152,9 s (×2,05)** |
| perplexité (31 jetons) | 115 521,8693 | **115 521,8693** |

Le gain de bout en bout est donc **×2,05** à ctx 32, contre ×3 à ctx 8 : quand le
contexte grandit, le débit mémoire — et non plus les cœurs inoccupés — borne le
poste. C'est le chiffre à citer, pas le ×9,34 du poste isolé.

## 6. Ce qui reste sur la table

Le poste lit ~6,6 Go de poids par jeton en 1,32 s, soit **≈ 5 Go/s** — loin des
40-60 Go/s que la DDR4 de la machine peut rendre. Le levier suivant est le SIMD
(AVX2, comme `dot8_avx`), **et il coûte** : huit accumulateurs partiels changent
l'ordre de la sommation, donc des bits, donc la référence de non-régression
(V4-Flash 8430,4966 et tous les chiffres du chemin f32 seraient à re-mesurer).
Décision : ne pas le faire tant que le poste dominant est `proj+mlp`
(5 946 ms/token, des lectures d'experts sur NVMe — P9 a déjà mesuré que le goulot
est la LECTURE).

## 7. Reproduire

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
cargo build --release --manifest-path drave-core/Cargo.toml
M=/home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf
# la passe, son profil et sa perplexité (~25 s)
./drave-core/target/release/drave "$M" --ppl /tmp/v41_last4.ids --ctx 8 --limit 4 \
    --abits 8 --threads 20
# l'égalité au bit près : mêmes vides avant/après, comparés en numpy
DRAVE_DUMP_COUCHES=/tmp/apres/l ./drave-core/target/release/drave "$M" --ppl \
    /tmp/v41_last4.ids --ctx 8 --limit 4 --abits 8 --threads 20
# (les vides « avant » viennent de la même commande avec le binaire précédent)
```
