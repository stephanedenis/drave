# Bilan B11 — ce qui tient, ce qui ne tient pas

> **Point de fin du round 12.** L'objectif complet n'est **pas** atteint : le codec classique tient la
> lecture et la **restitution du code** (aller-retour RSN), mais la **surface originale** n'est rendue
> qu'à **33/79**, le **natif** ne lit qu'à **59,8 %** et le **raisonnement n'est pas branché**. Ce bilan
> sépare les résultats des espoirs.

## 1. Les trois étages

| étage | état | mesure | verdict |
|---|---|---|---|
| **(1) sémantique partagée** | encodeur UDHR 10 langues, `z` 128, NVLink | rappel **0,426** vs **0,167** ; mélangé **0,172** ; sonde **0,100** | ✅ **premier palier** |
| **(2) sens → texte** | codec canonique (restitution du code) | **79/79 + 449/449**, aller-retour **100 %** ; surface **33/79** | ✅ **code** |
| | natif normalisé + contexte | **59,8 %** de code exact, invariance **40,7 %** | ⚠️ **partiel** |
| **(3) raisonnement** | sur code typé | non branché | ⏳ **non fait** |

## 2. Ce qui tient

- **Encodeur** : 0,426 contre 0,167 de hasard, contrôle mélangé 0,172, sonde de langue 0,100. Le `z` est
  discriminant et neutre en langue sur ce corpus.
- **Codec + contexte** : **528/528** coups lus, RSN exacte, sans réseau.
- **Restitution du code (aller-retour RSN)** : **79/79** et **449/449**, aller-retour RSN exact **100 %**,
  sans décodeur neuronal ; la **surface originale** reste à **33/79**.
- **Natif synthétique** : 45,1 % sans normalisation, **55,7 %** avec normalisation, **59,8 %** avec le
  contexte suffixé ; l'invariance passe de **7,4 %** à **40,7 %**.
- **Mémoire de traduction** : 470 cibles, dont 428 autres surfaces ; explicitement **pas un modèle**.

## 3. Ce qui ne tient pas

- **Natif** : 59,8 % de code exact, **40,7 %** d'invariance ; `carte` **69,3 %** ; les ambiguïtés de surface
  (symbole du morpion, chemin des dames) ne sont pas levées.
- **Surface originale** : **33/79** seulement ; le format canonique doit être choisi.
- **Décodeur libre B10** : chrF **14,0 / 5,4** contre un plancher **38,8** (référence tronquée ;
  **12,7 / 5,3** contre **39,6** en référence complète) ; négatif.
- **Traduction de surface** en langue cible : non mesurée ; la traduction **sémantique** est exacte.
- **Raisonnement** : **non branché**. Le brancher sur un code à 59,8 % mesurerait le parseur, pas la pensée.

## 4. Contrôles négatifs nommés

| contrôle | résultat |
|---|---|
| natif réel seul | 48,3 % train / **0 %** validation |
| base gelée | **0 %** |
| majoritaire | **0 %** |
| consistance softmax | 38,3 % / invariance 0 |
| adversaire de langue | 39,6 % / invariance 0 |
| contexte préfixé | **0,4 % / 88,9 %** (collapse) |
| contexte séparé | 59,1 % / 40,7 % (aucun gain) |
| décodeur libre | chrF 14,0 / 5,4 (sous le plancher) |
| mémoire de traduction | **pas un modèle** |

## 5. Lecture

Le **meilleur modèle linguistique** pour ce corpus est un **hybride** :

1. **codec classique** pour la lecture et la **restitution du code** (100 %) ; la **surface** reste à 33/79 ;
2. **natif normalisé** pour les surfaces inconnues (59,8 %), en secours ;
3. **mémoire** pour les paires connues, explicitement étiquetée comme mémoire.

Le **natif seul** n'est pas une couche sémantique fiable ; le **codec seul** ne généralise pas. L'objectif
« reconstruire le modèle natif » reste **ouvert**.

## 6. Prochaine action

- **Cartes** : `carte` 69,3 % ; compléter les formes de rangs/enseignes.
- **Désambiguïsation** : contexte séparé ou règles ; le codec le fait déjà.
- **Traduction de surface** : rendu par langue à partir de la RSN.
- **Raisonnement** : seulement après un code natif fiable, ou sur le codec avec la mention « classique ».

## 7. Commits

`325c1dec`, `1968af92`, `0584fd74`, `bb94843f`, `c0f1e845`, `38c3d880`, `532ddd07`, `386e59d5`.
