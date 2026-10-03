# Sprint 17 — `proj+mlp` : entrées-sorties ou calcul ? (et le fil qui manque)

- **Début** : 23:15 · **Fin prévue** : 01:15
- **Objectif** : le poste dominant de V4.1 (3 530 ms/token à ctx 32) est la lecture
  et le calcul des experts. Décider par la mesure s'il est borné par le disque ou
  par le calcul, et prendre le gain le moins cher (le fil manquant).
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. `proj+mlp` est borné par le CALCUL, pas par le disque (mesuré)

Deux passes identiques à la suite (`ctx 8`, 4 jetons, 8 bits) : la seconde trouve
dans `buff/cache` les ~12 Go d'experts que la première vient de lire. Si le poste
était borné par les entrées-sorties, la seconde serait plus rapide.

| passe | durée | poste `proj+mlp` |
|---|---|---|
| 1 (cache de pages froid) | 17,5 s | 4 357,29 ms/token |
| 2 (experts en cache) | 17,4 s | 4 416,31 ms/token |

**Identiques à 0,1 s près.** Le poste dominant de V4.1 n'est donc pas la lecture
des 330 Go d'experts : c'est la **déquantification** de ces experts
(`Source::Dequant`, la grille Q2_K — « le chemin le plus cher du moteur » d'après
son propre commentaire), qui matérialise ~10,4 G de valeurs f32 par jeton.

Cela **contredit la conclusion de P9** (« le goulot est la LECTURE ») — pour un
autre modèle et une autre mesure (trois tranches contre huit grappes, sur
V4-Flash). Les deux peuvent être vraies : ce qui change ici, c'est que le disque
est rapide et le chemin de déquantification lent.

### 2. Le gain le moins cher : le fil qui manquait

La déquantification des experts est découpée **par lignes** entre `threads_iq`
fils, et ce nombre était **borné à 8** — sur une machine qui en a 20.

| mesure | avant (8 fils) | après (20 fils) |
|---|---|---|
| poste `proj+mlp`, ctx 8 | 4 357,29 ms/token | **3 142,48** (×1,39) |
| passe, ctx 8 | 17,5 s | **13,6 s** (×1,29) |
| poste `proj+mlp`, ctx 32 | 3 530,27 ms/token | **2 431,58** (×1,45) |
| passe, ctx 32 (31 jetons) | 145,1 s | **109,8 s** (×1,32) |
| perplexité (ctx 8 / ctx 32) | 1 743 713,6243 / 115 521,8693 | **identiques** |
| vides, 2 544 tenseurs | — | **0 différent** |

Le découpage par lignes garantit l'égalité au bit près (aucune réassociation) :
elle est vérifiée, pas supposée.

**Cumulé depuis le début de la nuit** (blocs 15 et 17), la passe ctx 32 de V4.1
passe de **313,1 s à 109,8 s (×2,85)**, sans qu'un seul chiffre change.

### 3. Ce que la mesure dit du levier suivant

Le chemin de déquantification matérialise les poids en f32 puis les multiplie :
avec 20 fils il tourne à ~4,3 G de poids par seconde. Le levier qui reste est de
**vectoriser la déquantification seule** (conversion codebook → f32), sans toucher
au produit scalaire : la conversion est une fonction pure, valeur par valeur,
donc **SIMD y est bit-exact par construction** — contrairement au SIMD du produit
scalaire, qui réassocie la somme et changerait la référence de non-régression.
C'est le chantier du bloc 18.

## Rétrospective — garder / changer / doute

**Garder.**

- **Le contrôle « même mesure, cache chaud »** : deux passes identiques à la suite
  ont tranché entre disque et calcul en 35 secondes, sans instrumenter une ligne.
  C'est le genre de contrôle à garder sous la main pour tout poste de lecture.
- **Chercher le fil manquant** : un `clamp(1, 8)` sur une machine à 20 cœurs, sur
  le chemin le plus cher du moteur, valait ×1,32 sur la passe — et le découpage
  par lignes le rendait gratuit en exactitude.

**Changer.**

- **Une conclusion de performance n'est pas transitive.** P9 avait mesuré « le
  goulot est la LECTURE » sur V4-Flash avec trois tranches contre huit grappes ;
  je l'avais reprise pour V4.1 sans la re-mesurer. Elle est **fausse ici** (deux
  passes identiques, cache chaud ou froid). Toute conclusion de performance doit
  être re-mesurée sur le modèle et le chemin où on l'applique.
- **Le budget de fils doit être justifié par une mesure, pas par un `clamp`.**
  Le `clamp(1, 8)` n'avait aucune note ; il coûtait 32 % de la passe.

**Doute.**

- Le contrôle « cache chaud » est fait à **ctx 8, 4 jetons** (12 Go d'experts, qui
  tiennent dans les 95 Go de `buff/cache`). À 1 024 jetons, le flux d'experts
  (330 Go) dépasse le cache et le disque redevient peut-être la borne. Le contrôle
  refait à **ctx 64 (63 jetons, ~330 Go lus)** répond en partie : voir les deux
  passes ci-dessous.

### 4. Le balayage des fils, et la borne qui revient avec le contexte

**Balayage** (ctx 8, 4 jetons, 8 bits), la question laissée en doute :

| `--threads` | 8 | 12 | **16** | 20 | 24 |
|---|---|---|---|---|---|
| durée de la passe | 14,1 s | 13,3 s | **11,4 s** | 13,1 s | 16,1 s |

**16 fils est l'optimum** sur cette machine (20 cœurs physiques, 40 logiques) ;
au-delà, la sur-souscription coûte. Toutes les mesures publiées de cette nuit sont
à 20 fils : elles sous-estiment donc légèrement le gain possible (11,4 s contre
13,1 s à ctx 8, soit encore 13 %). Le `clamp` du code reste le nombre de fils
demandé (il ne code pas 16 en dur) : c'est un réglage de machine, et la mesure
est publiée pour qui veut le poser.

**Contexte long** (ctx 64, 63 jetons, ~330 Go d'experts lus — bien au-delà des
95 Go de `buff/cache`), deux passes identiques à la suite :

| passe | durée | poste `proj+mlp` | perplexité |
|---|---|---|---|
| 1 | 194,1 s | 1 961,16 ms/token | 44 774,3783 |
| 2 | 185,7 s | 1 890,06 ms/token | 44 774,3783 |

**+4,3 % pour la seconde**, alors qu'elle relit 330 Go que le cache de pages ne
peut pas tenir : le disque n'est pas la borne non plus à ce contexte. Le poste
dominant est le calcul de déquantification, à toute échelle mesurée — et la
perplexité identique au chiffre près est une quatrième preuve d'égalité (après
ctx 8, ctx 32 et les vides).

### 5. La part exacte de la déquantification, mesurée par ablation

Pour ne pas vectoriser ce qui ne pèse pas, deux builds temporaires (jamais
commités, aucun chiffre de perplexité n'en est publié) à ctx 8, 4 jetons, 16 fils :

| variante | durée de la passe | poste `proj+mlp` |
|---|---|---|
| complète (référence) | **11,3 s** | ~2 900 ms/token |
| déquantification remplacée par un remplissage, **produit gardé** | **8,6 s** | 1 592,50 |
| produit remplacé par un `black_box`, **déquantification gardée** | 14,2 s | 3 468,76 |

La **déquantification** (la conversion codebook → f32, plus les lectures
compressées qu'elle porte) vaut donc **~25 % de la passe et ~45 % du poste
d'experts**. Le second essai ne dit rien : `black_box` coûte plus cher que le
produit qu'il remplace — une ablation ne vaut que si ce qu'on met à la place est
moins cher que ce qu'on retire, et ça se vérifie.

## Planning du bloc 18 — vectoriser la DÉQUANTIFICATION seule (bit-exact par construction)

La conversion d'un super-bloc de grille (codebook + signes → f32) est une fonction
**pure, valeur par valeur** : la vectoriser ne réassocie aucune somme, donc ne
change pas un bit — contrairement au SIMD du produit scalaire, qui réassocierait
et ferait tomber la référence de non-régression (V4-Flash 8430,4966).

1. ~~Mesurer la part exacte de la conversion~~ — **fait au bloc 17** : ~25 % de la
   passe, ~45 % du poste d'experts (ablation, ci-dessus). C'est assez pour
   justifier le noyau, et c'est la borne du gain attendu.
2. **Vectoriser `dequant_grille_dans`** pour le format de V4.1 (Q2_K, type 10) avec
   AVX2, en gardant l'ordre valeur par valeur — même s'il n'y a pas de somme, la
   conversion doit rester identique (arrondis, clamps).
3. **Prouver** : 2 544 vides identiques au bit près, perplexités ctx 8 et ctx 32
   inchangées, porte V4-Flash 8430,4966 inchangée, puis publier le gain.

## Portes

- `tools/portes.sh rapide` : **toutes vertes** — 63 tests, Qwen 19,3885, clusters
  799,8557, **V4-Flash 8430,4966**, engram, cinq modes de flux.
- V4.1 : perplexités et vides inchangés (mesuré ci-dessus).
- **Découpage à deux nœuds, refait avec le binaire final** (16 fils des deux
  côtés) : `écart 0,00e0`, 82 016 octets à l'aller comme au retour, référence
  locale **25,6 s** (elle en coûtait 68,0 en début de nuit) et deux nœuds
  **16,4 s**. Le découpage reste donc exact après avoir changé la décomposition
  parallèle de deux chemins — c'est ce qu'il fallait vérifier, pas supposer.

## Ce qui reste, nommé

- **Le balayage des fils** (8/12/16/20) n'a pas été fait : seul 8 → 20 est mesuré.
- **Le SIMD du produit scalaire** reste écarté : il change des bits, donc la
  référence de non-régression — décision inchangée depuis le bloc 15.
- **Le cache RAM d'experts** (bloc 16) reste éteint et documenté.
