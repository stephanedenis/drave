# Rapport — La nuit des optimisations V4.1 : ×3,54 sur la passe, et pas un chiffre changé

03/10 (blocs 15 à 19), `/home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf`
(365,71 Go, 40 couches, 384 experts dont 6 par jeton), 16 à 20 fils selon la mesure.

**Verdict en une ligne : trois leviers — un matvec parallèle par lignes, un
plafond de fils qui n'avait aucune raison d'être, et deux noyaux AVX2 de
déquantification — font passer la passe ctx 32 de 313,1 s à 88,5 s, et 5 670
teneurs comparés disent que pas un bit n'a bougé.**

## 1. Les trois leviers, mesurés séparément

| levier | mesure | gain |
|---|---|---|
| **matvec f32 parallèle par LIGNES** (bloc 15) | attention 12 369,91 → 1 324,48 ms/token à ctx 8 | **×9,34** sur le poste, ×3 sur la passe |
| **`threads_iq` déborné** (8 → 20 fils, bloc 17) | `proj+mlp` ctx 32 : 3 530,27 → 2 431,58 ms/token | ×1,45 |
| **noyau AVX2 de déquantification Q2_K** (bloc 18) | `proj+mlp` ctx 32 : 2 431,58 → 1 833,91 ms/token | ×1,33 |
| noyau AVX2 IQ1_M (V4-Flash, bloc 18) | `proj+mlp` : 2 054,97 → 1 916,57 ms/token | ×1,07 |

Bilan sur la passe complète :

| passe | avant la nuit | après |
|---|---|---|
| V4.1 ctx 8 (4 jetons) | 66-68 s | **10,7 s** |
| V4.1 ctx 32 (31 jetons) | 313,1 s | **88,5 s** (×3,54) |
| V4.1 ctx 64 (63 jetons) | — | 185,7 s |
| V4.1 ctx 1 024 (1 023 jetons) | hors de portée (≈ 3,5 h) | **3 635 s (60,6 min)** |
| V4.1 découpé, 2 nœuds | 51,3 s (réf. locale 68,0) | **16,4 s** (réf. locale 25,6) |
| V4-Flash ctx 32 (4 jetons notés) | — | 12,8 s de calcul, PPL **8430,4966** |

## 2. Ce qui garantit qu'aucun chiffre n'a changé

| preuve | résultat |
|---|---|
| vides V4.1, ctx 8 (2 544 tenseurs) — après chaque levier | **0 différent** |
| vides V4-Flash, ctx 32 (3 126 tenseurs) — noyau IQ1_M | **0 différent** |
| perplexité V4.1 : ctx 8, 32, 64, 1 024 | 1 743 713,6243 · 115 521,8693 · 44 774,3783 · 1 287 700,8239, **identiques** avant/après |
| logits, 32 jetons à ctx 32 contre ctx 1 024 (4 007 682 valeurs) | **0,000e+00** |
| découpage à deux nœuds | écart **0,00e0**, 82 016 octets dans les deux sens |
| porte `tools/portes.sh rapide` | toutes vertes, **V4-Flash 8430,4966** |

La répartition des preuves compte : le matvec parallèle et le débornage des fils
sont **bit-exacts par construction** (découpage par lignes : chaque ligne garde
son ordre de sommation) ; les noyaux AVX2 aussi (conversion pure, valeur par
valeur, sans FMA).

## 3. Deux idées REFUSÉES par la mesure (et pourquoi c'est le résultat)

| idée | ce que la mesure a dit |
|---|---|
| **cache RAM des experts** (justifié par une trace : 50 % des lectures dans 394 experts, 31,9 % de réutilisation entre jetons consécutifs) | **plus lent** : passe ctx 32 = 145,1 s sans, 151,2 s à 4 Go (+4 %), 175,5 s à 32 Go (+21 %). Le noyau fait déjà ce travail (`buff/cache`, ~95 Go) : la copie ajoute un second exemplaire et du `memcpy` sans retirer les lectures NVMe. Drapeau éteint, verdict dans son annonce |
| **SIMD du produit scalaire** | écarté : huit accumulateurs partiels réassocient la somme, donc changent des bits, donc la référence de non-régression. Le noyau de *déquantification*, lui, est gratuit en exactitude — d'où le choix fait |

## 4. Ce que la nuit a appris sur la méthode

1. **Une conclusion de performance n'est pas transitive.** P9 avait mesuré « le
   goulot est la LECTURE » sur V4-Flash, avec un autre protocole. Ici, deux passes
   identiques à la suite (la seconde trouvant 12 Go d'experts dans le cache de
   pages) donnent le **même temps à 0,1 s près** : le poste est borné par le
   CALCUL. Re-mesurer sur le modèle et le chemin où on applique la conclusion.
2. **Un chiffre de réutilisation n'est pas une prédiction de gain.** La trace
   disait tout ce qu'il fallait pour croire au cache ; elle ne disait rien de la
   hiérarchie mémoire existante.
3. **Le plafond d'un noyau se mesure avant de l'écrire.** La déquantification
   pesait 25 % de la passe et 45 % du poste d'experts (ablation, bloc 17) : le
   noyau Q2_K pouvait donc rendre au mieux ~×1,3 sur le poste — c'est exactement
   ce qu'il a rendu (×1,33). Pour IQ1_M, le plafond était bas (la lecture du
   codebook domine) et le noyau n'a rendu que ×1,07.
4. **Un diagnostic documenté sans interrupteur est du code mort.** Le profil de
   perplexité par profondeur était décrit, codé, commenté — et aucun drapeau ne
   l'activait depuis des semaines (une relecture l'avait même écrit dans
   `docs/vision.md`). Branché au bloc 19.

## 5. Reproduire

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
cargo build --release --manifest-path drave-core/Cargo.toml
M=/home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf

# la passe de référence (ctx 8, 4 jetons) : 10,7 s, PPL 1 743 713,6243
./drave-core/target/release/drave "$M" --ppl /tmp/v41_last4.ids --ctx 8 --limit 4 \
    --abits 8 --threads 16

# ctx 32 : 88,5 s, PPL 115 521,8693
./drave-core/target/release/drave "$M" --ppl /tmp/v41_texte.txt.ids --ctx 32 --limit 32 \
    --abits 8 --threads 16 --ppl-profil

# l'égalité au bit près : mêmes vides avant/après (DRAVE_DUMP_COUCHES), comparés en numpy
# les portes : toutes vertes, V4-Flash 8430,4966
tools/portes.sh rapide
```

`/tmp/v41_last4.ids` = `270,15301,6605,223` · `/tmp/v41_texte.txt.ids` = le même
texte (73 jetons) · `/tmp/v41_1024.ids` = 1 024 jetons du même wikitext.

## 6. Ce qui reste, nommé

- **Le produit scalaire** (dont le SIMD réassocierait) et les **lectures
  compressées** : non mesurés séparément, et c'est ce qui reste dans le poste
  d'experts après le noyau.
- **Les autres formats de grille** (Q3_K, IQ2_XXS, IQ1_S…) n'ont pas de noyau.
- **Le réglage des fils est un réglage de machine** : le balayage donne 16 comme
  optimum ici (11,4 s contre 13,1 s à 20 fils), et le code ne le code pas en dur.
