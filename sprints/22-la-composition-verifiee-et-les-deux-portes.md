# Sprint 22 — La composition vérifiée, et les deux portes de P6 auditées

- **Début** : 03:35 · **Fin** : 04:30 (55 min)
- **Objectif** : le bloc 21 a éliminé dix hypothèses et laissé V4.1 cassé, avec un
  plan précis : vérifier non plus chaque *pièce* contre une transcription, mais la
  **composition** (chemin des experts en numpy, puis le cœur de l'attention avec
  les blocs compressés). Puis, si tout est juste, auditer les deux portes de P6
  (Drave et correction) — la règle du dépôt est qu'aucune phase ne passe sans
  elles, et elles n'avaient jamais été *exécutées* depuis leur écriture.
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. La composition de V4.1 est vérifiée, pièce par pièce, en numpy

Quatre vérifications, toutes contre une transcription écrite à la main (numpy
`float64`), chacune sur des données **réelles du fichier Q2** :

| pièce | dump du moteur | référence | écart |
|---|---|---|---|
| chemin des experts | `moe_down` (vide neuf) | `Σ_e w_e · W_d[e]·act(W_g[e]·hn, W_u[e]·hn)` | **3,9e-05 / 5,2e-05** relatif |
| entrée normée du MoE | `ffn_hn` (vide neuf) | `rmsnorm(hc_mel_ffn, ffn_norm, 1e-20)` | 1e-07 à 1e-06 |
| projections, normes, rotations | `q_rope`, `kv_rope` | transcription | **1e-06** |
| cœur de l'attention | `attn_brut`, `attn_out` | scores + puits + somme + dé-rotation + `wo_a`/`wo_b` groupés | **8,5e-07 / 5,7e-06** |
| couche compressée + règle de visibilité | blocs, `n_visible = (pos+1)/ratio`, publication à `(b+1)·ratio − 1` | transcription | **7,1e-07** |

Deux vides neufs ont été ajoutés au moteur pour rendre cela vérifiable (`ffn_hn`,
`moe_down`) — un dump qui n'existe pas est une pièce qu'on ne peut pas vérifier.
**Conclusion : il n'y a plus aucune pièce de V4.1 qui ne soit pas vérifiée.** Ce
qui reste hors d'atteinte est nommé dans le plan (P7) : la composition sur
40 couches, qui n'a pas d'oracle, et le fichier Q2 lui-même.

### 2. Le chemin des experts : une faute de MON script, à nouveau

L'écart initial sur `q_rope` (3,6 relatif) n'était pas dans le moteur : mon script
prélevait la tranche de rotation dans `q` au lieu de `qn`. En appliquant la
rotation au **`q_norm` du moteur lui-même**, l'écart tombe à **1,0e-06**. Même
schéma que le groupe `wo_b` du bloc 21 : quand une vérification accuse le moteur,
la première hypothèse doit être l'instrument.

### 3. Porte Drave de P6 : deux points sur quatre ne tenaient pas — puis tiennent

Exécuter la porte a suffi à la faire échouer :

1. **Le flux n'était pas lisible par l'outil d'analyse.** `tools/analyse_flux.py`
   lisait la version 1 du format DRVF (indice u32 + i16) ; le moteur écrit la 2
   (indices par écarts) et la 3 (échelle f16 par bloc de 32 canaux, valeurs i8).
   L'outil plantait sur une trace du moteur. Corrigé : lecteur v1/v2/v3 avec
   échelles par bloc, et la porte est **branchée** dans `tools/portes.sh` (7ter) —
   elle produit une trace avec le petit modèle et la relit, à chaque passage.
2. **Le rejeu n'était pas « identique »** : « 672 listes manquantes » venait de ma
   trace partielle (`--trace-couches 0,20`), pas du moteur. Trace complète →
   **688 listes servies, 0 manquante**. L'écart de perplexité, lui, ne tombe pas à
   zéro (4,5e-06) parce que la trace porte des activations déjà quantifiées que le
   rejeu requantifie. **Définition écrite et vérifiée par la porte** : aucune liste
   manquante **et** écart ≤ 1e-5 (mesuré : 4,5e-06 sur V4-Flash, 1,6e-06 sur Qwen).

### 4. Porte de correction de P6 : mesurée, et l'instrument était le mauvais

Comparaison à llama.cpp, protocoles alignés (mêmes identifiants, même ctx, un seul
batch), 5 identifiants et 4 prédictions : corrélations **0,9876 à 0,9984**, rangs
du vrai jeton voisins, top-1 identique sur 3 positions sur 4. **Mais** la
perplexité, sur cette fenêtre, donnait 6 719,61 (llama.cpp) contre 8 430,4966
(nous) : **25 %**. Une fenêtre froide de quatre jetons amplifie chaotiquement un
écart de logits de 1 %.

Ce que ça corrige dans ce que le dépôt affirme : le chiffre de `portes.sh`
(8430,4966) est une **référence de non-régression interne**, pas une mesure
d'accord avec llama.cpp. C'était écrit nulle part avant ce bloc.

## Portes

- **64 tests** ✓ · Qwen 19,3885 ✓ · clusters 799,8557 ✓ · V4-Flash **8430,4966** ✓
- `tools/portes.sh` sections 7ter (flux lisible), 7quater (rejeu ≤ 1e-5),
  8 (découpage) : branchées et vertes.
- Aucune optimisation de ce bloc ne change une sortie : les changements sont un
  lecteur d'outil, un bornage d'option et des dumps.

## Rétrospective — garder / changer / doute

**Garder.** Les drapeaux d'ablation qui **s'annoncent** (`DRAVE_SANS_*`) : ils ont
éliminé dix hypothèses en 55 minutes là où la lecture de code n'avait rien donné
en une nuit. Et la règle « la première hypothèse est l'instrument » : elle a
encore payé deux fois dans ce bloc (la rotation du Q, les 672 listes manquantes).

**Changer.** Une porte qu'on n'exécute pas pourrit. Les deux portes de P6 étaient
*écrites* au bloc 22 précédent et jamais lancées ; exécutées, deux points sur
quatre étaient faux — dont un outil d'analyse incapable de lire le format de son
propre moteur. La leçon n'est pas « mieux écrire les portes », c'est **les
brancher dans `portes.sh` le jour où on les écrit**. C'est fait pour ces deux-là.

**Changer (2).** J'ai publié « perplexité identique » comme si c'était un critère
alors que deux quantifications différentes ne peuvent pas donner le même nombre.
Un critère qu'on n'a jamais mesuré n'est pas un critère : c'est une intention.

**Doute.** Le point 4 ci-dessus reposait sur **quatre** positions, dont trois avec
une corrélation ≥ 0,9979 — et c'était de la chance : sur 63 positions, la
corrélation **minimale** est 0,955. Une fenêtre courte ne teste pas la fidélité du
moteur, elle teste la stabilité du chaos. Tout chiffre d'accord publié sur une
fenêtre courte doit être marqué comme tel.

**Doute (2).** La porte Drave de P6 est maintenant *définie* (listes manquantes,
seuil 1e-5) mais elle n'est tenue que sur le **petit modèle** : la tenir sur
V4-Flash coûte une passe complète. La définition est écrite, l'exécution reste à
la demande — c'est un écart entre ce que la porte *dit* et ce que la porte
*vérifie à chaque passage*, et il est nommé ici plutôt que masqué.

## Planning du bloc 23 — serrer la porte de correction, et jusqu'au contexte long

1. **Serrer la porte** : 64 positions au lieu de 4, corrélation par position,
   top-1, rang du vrai jeton, et l'écart de perplexité — puis **écrire la
   définition** (seuils) dans le plan, en remplacement de « même perplexité ».
2. **Porter la comparaison au contexte long** : le plan l'annonce depuis P6
   (« à terme, la même comparaison sur une couche compressée à contexte long »).
   1 024 jetons sur V4-Flash, llama.cpp contre le moteur, mêmes identifiants,
   comparaison position par position — c'est la seule mesure qui exerce la règle
   de visibilité des blocs compressés sur une longue fenêtre.
3. Écrire le résultat dans le plan (P6), et la porte dans `portes.sh` si elle est
   assez rapide pour être exécutée à chaque passage.
