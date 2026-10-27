# Rapport — base d'universaux typés

> **Objet.** Tester la direction « base fixe d'universaux + paramètres fixes en sortie » sur les coups des
> jeux, et comparer deux blocs : le **parseur natif typé** et le **codec classique**.
> Code : [`tools/semantique/universaux.py`](../tools/semantique/universaux.py),
> [`typed_corpus.py`](../tools/semantique/typed_corpus.py),
> [`entrainer_type.py`](../tools/semantique/entrainer_type.py). Données : B5 (112 items) et B7 (449 surfaces),
> filtrés sur les **coups**.

## 1. Le corpus et le code

| élément | valeur |
|---|---:|
| coups B5 | 79 |
| coups B7 | 449 |
| items après dédoublonnage | 528 |
| train / validation | 377 / 151 |
| paires train / validation | 25 / 6 |
| champs typés | 15 |
| classes (vocabulaire fixe) | 502 |

Le code est un **one-hot concaténé** sur 15 champs : `jeu`, `action`, `de`, `vers`, `promotion`, `roque`,
`case`, `symbole`, `carte`, `taille`, `point`, `passe`, `chemin_0`, `chemin_1`, `chemin_2`. Le découpage est
**par paire** : aucune surface d'un même sens n'est des deux côtés.

## 2. Le parseur natif typé

`route` 31,63 M, pooling moyen, 15 têtes linéaires, lot 32, lr base 2e-4, lr têtes 1e-3.

### 2.1 Réel seul : surapprentissage

Découpage par paire, 377 train / 151 validation, 200 pas.

| mesure | valeur |
|---|---:|
| exactitude **train** (code complet) | **48,3 %** |
| exactitude **validation** (code complet) | **0,0 %** |
| base gelée, validation | **0,0 %** |
| majoritaire (validation) | **0,0 %** |
| déterminisme (même entrée) | **1,000** |
| invariance par paire (validation) | **0,000** |

**Lecture** : le modèle **surapprend** les surfaces d'entraînement et ne généralise pas à des coups nouveaux.
La base gelée ne fait pas mieux : ce n'est pas seulement un problème de capacité, c'est un problème de
**données/compositionnalité**. Le code typé est déterministe, mais le parseur ne le remplit pas.

### 2.2 Synthétique : la distillation débloque

Les surfaces **réelles** ne sont **jamais** vues à l'entraînement. On génère 10 556 surfaces synthétiques
multilingues (coups légaux d'échecs et de dames, 81 points de go, 52 cartes, cases de morpion, 71 langues),
labels RSN exacts, puis on teste sur les **528 surfaces réelles** B5/B7.

| mesure | valeur |
|---|---:|
| exactitude **train synthétique** | **92,3 %** |
| exactitude **test réel** (code complet) | **45,1 %** |
| `jeu` | **83,1 %** |
| `action` | **82,4 %** |
| `de` / `vers` | **90,0 % / 89,4 %** |
| `carte` | **67,8 %** |
| `case` / `symbole` | **88,3 % / 86,9 %** |
| **invariance par paire** (même sens, langues différentes) | **7,4 %** |
| déterminisme | **1,000** |
| restitution (15 formats testés) | **40,0 %** |

### 2.3 Normalisation lexicale : le levier

Les mots du lexique (jeux, pièces, rangs, enseignes, passe) sont remplacés par des **concepts canoniques**
(`[jeu.morpion]`, `[echecs.piece.N]`, `[cartes.rang.13]`) avant le parseur ; les coordonnées et les nombres
restent. L'enseigne de carte tranche l'ambiguïté « roi » (pièce d'échecs ou rang).

Entraînement synthétique normalisé (10 556), test sur les **528 surfaces réelles normalisées**, aucune surface
réelle à l'entraînement.

| mesure | baseline synthétique | **normalisé** |
|---|---:|---:|
| code exact | 45,1 % | **55,7 %** |
| `jeu` | 83,1 % | **91,3 %** |
| `action` | 82,4 % | **91,3 %** |
| `de` / `vers` | 90,0 / 89,4 % | **95,1 / 87,9 %** |
| `carte` | 67,8 % | **69,5 %** |
| **invariance par paire** | 7,4 % | **37,0 %** |
| déterminisme | 1,000 | **1,000** |
| restitution (formats testés) | 40,0 % | 33,3 % |

**Lecture** : la normalisation est le **bon levier** — l'invariance passe de **7,4 % à 37,0 %** et le code
exact de **45,1 % à 55,7 %**. Mais le codec reste à **100 %** : il reste des ambiguïtés de surface (symbole du
morpion, chemin des dames, cartes), et le natif n'a pas encore la cohérence totale.

### 2.4 Cohérence inter-langues : deux négatifs

Deux régularisations ont été testées sur le même entraînement synthétique, avec le même test réel.

| variante | code exact | invariance par paire | lecture |
|---|---:|---:|---|
| baseline synthétique | **45,1 %** | **7,4 %** | référence |
| consistance softmax (poids 1,0) | 38,3 % | 0,0 % | la contrainte écrase le code, sans cohérence |
| adversaire de langue (poids 0,5) | 39,6 % | 0,0 % | l'adversaire retire de l'information utile |

La **consistance** et l'**adversaire** ne règlent pas le problème : ils **dégradent** le code exact et ne
rendent pas les langues cohérentes. Le baseline synthétique reste le meilleur parseur natif.

**Lecture** : la distillation synthétique **fonctionne** — le parseur natif passe de 0 % à **45,1 %** de code
exact sur des surfaces réelles qu'il n'a jamais vues, avec **83 %** de jeu et **90 %** de source/cible. Mais
il reste **loin du codec** (100 % de lecture exacte), et l'**invariance par paire est faible (7,4 %)** : les
prédictions dépendent encore de la langue. Le codec reste le bloc fiable ; le natif est un **élève** qui doit
être rendu cohérent entre langues.

## 3. Le codec classique

Le codec B5/B7 est le **bloc linguistique exact** déjà présent dans le dépôt.

| mesure | B5 | B7 |
|---|---:|---:|
| coups lus | 79 / 79 | 449 / 449 |
| RSN exacte après lecture | **100 %** | **100 %** |
| restitution exacte (formats canoniques) | **33 / 79** | non mesurée (`multilingue`) |

**Lecture** : la **lecture sémantique** est exacte sur tout le corpus ; la **restitution de surface** n'est
exacte que sur 33/79 formats canoniques — le format de sortie doit être choisi, ce n'est pas un décodeur
universel. La traduction **sémantique** (surface → RSN → RSN cible) est donc exacte par construction ; la
traduction **de surface** demande encore un rendu par langue.

## 4. Contrôles

- **Découpage par paire** : aucune paire de validation n'apparaît à l'entraînement.
- **Majoritaire** : 0 % de code complet exact ; le score n'est pas porté par une classe fréquente.
- **Base gelée** : 0 % ; le résultat négatif n'est pas dû à un entraînement trop fort de la base.
- **Train vs validation** : 48,3 % contre 0 % : le contrôle d'apprentissage est explicite, c'est un
  **surapprentissage**, pas une mesure de généralisation.
- **Déterminisme** : 1,000 ; le code est stable.
- **Codec** : lecture exacte 100 % sur les deux corpus.

## 5. Ce que le résultat établit

1. La **base typée** est un **contrat** clair : 15 champs, 502 classes, sortie déterministe.
2. Le **codec classique** est aujourd'hui le **meilleur bloc linguistique** pour ce corpus : lecture
   sémantique exacte à 100 %.
3. Le **parseur natif typé** n'est **pas** au niveau : il surapprend et ne généralise pas. Il faut soit
   **plus de données synthétiques/compositionnelles**, soit de la **régularisation**, soit **distiller le
   codec** dans le natif.
4. La **restitution** est partielle (33/79) ; le format cible doit être explicite.

## 6. Ce qui pourrait rendre ce résultat faux

- Un corpus de validation plus grand, ou un découpage par **langue** plutôt que par paire.
- Un parseur natif avec **données synthétiques** et **classes équilibrées**.
- Un codec avec un **format canonique** imposé : la restitution 33/79 peut monter.
- Une taxonomie plus fine (rôles, aspect) : le code actuel est un **sous-ensemble** jeu.

## 7. Fichiers

- Code : [`universaux.py`](../tools/semantique/universaux.py), [`typed_corpus.py`](../tools/semantique/typed_corpus.py),
  [`entrainer_type.py`](../tools/semantique/entrainer_type.py), tests.
- Mesures : [`universaux-mesures.json`](universaux-mesures.json).
- Note de fond : [`docs/semantique-universaux.md`](../docs/semantique-universaux.md).
