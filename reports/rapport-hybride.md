# Rapport — hybride codec + mémoire, et le contexte

> **Objet.** Mesurer le bloc **déterministe** qui lit les surfaces de jeux : le codec classique avec le
> **contexte** (position, trait), puis la **mémoire de traduction** par paire. Le natif n'est pas utilisé ici :
> il est mesuré à part (55,7 % de code exact après normalisation).

## 1. Lecture avec contexte

| condition | coups lus | couverture |
|---|---:|---:|
| codec **sans** contexte | 374 / 528 | **70,8 %** |
| codec **avec** contexte | **528 / 528** | **100 %** |

Le **contexte** (position RSN ou état de départ) est décisif : sans lui, le codec ne peut pas lever les
ambiguïtés (symbole du morpion, chemin des dames, pièce des échecs). Avec lui, la lecture est **exacte** sur
tout le corpus B5/B7.

## 2. Mémoire de traduction

Pour chaque item, on cherche la surface de la **même paire** dans une autre langue.

| mesure | valeur |
|---|---:|
| items avec une cible mémoire | **470 / 528** |
| cibles qui sont une autre surface | **428 / 470** |
| nature | mémoire parallèle, **pas un modèle** |

La mémoire est **exacte par construction** ; elle ne prouve **aucune généralisation** à une paire absente.
C'est un bloc de **haute fiabilité sur le corpus**, pas un traducteur de surfaces inconnues.

## 3. Comparaison des blocs

| bloc | lecture | code exact | généralisation |
|---|---:|---:|---|
| codec + contexte | 528 / 528 | **100 %** | corpus B5/B7 |
| mémoire de traduction | 470 cibles | 100 % (mémoire) | non |
| natif normalisé | 528 test | **55,7 %** | surfaces réelles jamais vues |
| décodeur libre B10 | — | chrF 14,0 / 5,4 | négatif |

## 4. Lecture

- Le **codec avec contexte** est le **meilleur bloc linguistique** du corpus : 100 % de lecture, déterministe.
- Le **natif normalisé** est le seul bloc qui **généralise** à des surfaces réelles inconnues (55,7 %), mais il
  reste loin du codec et son invariance est **37,0 %**.
- La **mémoire** donne une traduction exacte sur les paires connues, mais ce n'est pas un modèle.
- La **restitution de surface** reste partielle (33/79 formats) : le format cible doit être explicite.

## 5. Contrôles

- **Sans contexte** : 70,8 % ; le gain du contexte est mesuré, pas supposé.
- **Mémoire vs modèle** : la mémoire est étiquetée comme telle ; aucune généralisation revendiquée.
- **Natif** : test sur surfaces réelles jamais vues, split par paire.
- **Déterminisme** du codec et du natif : 1,000.

## 6. Fichiers

- Code : [`hybride.py`](../tools/semantique/hybride.py), [`normalisation.py`](../tools/semantique/normalisation.py).
- Mesures : [`hybride-mesures.json`](hybride-mesures.json).
- Fiche B11 : [`rapport-universaux.md`](rapport-universaux.md).
