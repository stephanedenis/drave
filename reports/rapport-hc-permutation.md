# Hyper-connexions de V4-Flash : les 16 connexions sont une PERMUTATION

> Mesuré le 03/10 (bloc 27) en fermant la **porte Drave de P1**, qui n'avait
> aucun instrument : les 24 poids d'un raccord (`pre`, `post`, `comb`) étaient
> calculés à chaque jeton puis **jetés**. Le moteur les écrit maintenant
> (`DRAVE_DUMP_COUCHES`, noms `hc_attn` et `hc_ffn`), et `tools/analyse_hc.py`
> les relit, vérifie la promesse du Sinkhorn et dit la structure.

## 1. La porte

V4-Flash, 4 positions, 9 couches (0, 1, 2, 5, 10, 20, 30, 40, 42) :

| contrôle | mesure |
|---|---|
| Sinkhorn, axe **sources** (ce que `norm_src` garantit) : \|Σsrc − 1\| | **1,14e-06** ✅ |
| Sinkhorn, axe destinations (résidu de la dernière `norm_dst`, non jugé) | 6,33e-02 |
| connexions significatives (≥ 0,05) | **51/144 (35 %)** |
| stabilité entre positions consécutives (corrélation du `comb`) | 0,9212 (min 0,6730) |
| variabilité par entrée (coefficient de variation) | 0,839 |

L'ordre des normalisations est celui de la référence (softmax sur les
destinations, `+eps`, puis `iters − 1` paires `norm_dst`/`norm_src`) : **le
dernier axe normalisé est celui des sources**, et c'est le seul dont la somme
vaut 1. L'autre axe garde un résidu (6 %) — le mesurer vaut mieux que de
supposer les deux.

> ⚠️ Piège d'instrument, noté parce qu'il a mordu : le moteur écrit
> `comb[d + s·hc]`, donc dans le fichier plat **la destination varie le plus
> vite**. Après un `reshape(4,4)`, la ligne est la source et la colonne la
> destination — l'inverse de l'intuition. L'outil a d'abord accusé le moteur
> (« l'axe garanti ne somme pas à 1 : 8,16e-02 ») alors que l'axe garanti était
> juste à 1,13e-06. Le test sur données synthétiques **et** la lecture de
> `sinkhorn` ont tranché.

## 2. La structure : 4 connexions dominantes, et c'est une permutation

Sur les 43 couches, position 0 :

| mesure | résultat |
|---|---|
| masse portée par les **4 plus grandes** entrées (total = 4,0) | **≈ 3,97 / 4,0 (99 %)** |
| entrées ≥ 0,20 | **4 sur 16** dans 39 couches sur 43 |
| les 4 dominantes forment-elles une **permutation** ? | **43 / 43 couches** |
| masse diagonale moyenne | **3,746 / 4 (94 %)** · min 1,025 (couche 34) |

Autrement dit : le raccord ne **mélange** pas les quatre copies, il les
**ré-achemine**. La plupart des couches gardent l'identité (masse diagonale
3,9-4,0), mais **neuf couches permutent** :

| couche | permutation (destination ← source) | masse diagonale |
|---|---|---|
| 2 | [2, 1, 0, 3] (0↔2) | 2,016 |
| 5 | [0, 3, 2, 1] (1↔3) | 2,011 |
| 27, 28 | [0, 1, 3, 2] (2↔3) | 2,002 · 1,953 |
| 29 | [0, 2, 1, 3] (1↔2) | 2,018 |
| 33 | [0, 3, 2, 1] (1↔3) | 1,989 |
| 34 | [0, 3, 1, 2] (presque un 4-cycle) | **1,025** |
| 40 | [1, 0, 2, 3] (0↔1) | 2,002 |
| 42 | [0, 2, 1, 3] (1↔2) | 2,919 |

Les couches 0, 1 et 42 sont les plus « mélangeantes » (5 à 7 entrées
significatives) : le premier et le dernier raccord brassent plus que le corps du
réseau.

## 3. Ce que ça change, et ce que ça ne dit pas encore

- **Le plan demandait** : « combien des 16 poids sont significatifs, et sont-ils
  stables d'un jeton à l'autre ? » Réponse mesurée : **4 le sont** (12
  négligeables, 99 % de la masse), et ils forment une **permutation** ; la
  structure est **stable à 0,92** entre positions consécutives sans être figée.
- **Conséquence exploitable** : un raccord pourrait se calculer comme une
  **permutation apprise** (4 coefficients) au lieu de 16, ce qui simplifie le
  flux (`comb` passe de 16 à 4 valeurs par raccord, soit 24 → 12 par couche) —
  **à condition** que la mesure tienne sur d'autres positions et sur V4.1. C'est
  une hypothèse, pas encore une simplification.
- **Ce que ça ne dit pas** : la mesure porte sur **position 0** pour les 43
  couches et sur 4 positions pour 9 couches ; la variance entre positions
  (CV 0,84) montre que le `comb` bouge. Une vérification sur 32 positions et
  sur V4.1 est la suite naturelle, et elle est peu coûteuse (un vidage + l'outil).
