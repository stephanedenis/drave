# Rapport — restitution canonique et aller-retour RSN

> **Objet.** Mesurer la **restitution déterministe** : une RSN correcte est rendue en surface
> canonique, puis relue ; la RSN relue doit être **identique**. C'est le bloc classique, sans décodeur
> neuronal.

## 1. Résultats

Formats canoniques : `cellule` (morpion), `san` (échecs), `numerique` (dames), `gtp` (go), `carte` (cartes).

| corpus | coups | rendus | aller-retour RSN exact | erreurs |
|---|---:|---:|---:|---:|
| **B5** | 79 | **79** | **79** | 0 |
| **B7** | 449 | **449** | **449** | 0 |

**100 %** de rendu et **100 %** d'aller-retour sur les deux corpus. La surface canonique est **relue** en la
même RSN : le contrat est stable, déterministe, reproductible.

## 2. Ce que cela ne dit pas

- La **surface originale** n'est pas toujours reproduite : **33/79** formats B5 seulement. Le format de
  sortie doit être **choisi** (canonique), pas deviné.
- Le rendu est **par jeu** et **par format** ; ce n'est pas un traducteur de langues naturelles.
- La **traduction sémantique** (surface → RSN → RSN cible) est exacte par construction ; la **traduction de
  surface** en langue cible reste à faire.

## 3. Comparaison

| bloc | sens → texte | code exact | généralisation |
|---|---|---:|---|
| **codec canonique** | **79/79, 449/449** | **100 %** | corpus B5/B7 |
| codec formats originaux | 33/79 B5 | — | corpus |
| natif normalisé + contexte | — | 59,8 % | surfaces inconnues |
| décodeur libre B10 | chrF 14,0 / 5,4 | — | négatif |

## 4. Lecture

Le **meilleur bloc de restitution** est le **codec canonique** : 100 % de rendu et d'aller-retour, sans
réseau, sans échantillonnage, sans variabilité. Le natif reste nécessaire pour **lire des surfaces
inconnues** (59,8 %), pas pour **rendre** une RSN déjà lue.

C'est l'hybride demandé : **neuronal pour la surface inconnue**, **classique pour le contrat sémantique**.

## 5. Contrôles

- **Aller-retour** : la RSN relue est comparée à la RSN de départ, pas à la surface.
- **Formats canoniques** déclarés par jeu ; aucune devinette.
- **Corpus B5/B7** : 528 coups, aucun rejet.
- **Déterminisme** : le codec n'échantillonne pas.

## 6. Fichiers

- Code : [`restitution.py`](../tools/semantique/restitution.py).
- Mesures : [`restitution-mesures.json`](restitution-mesures.json).
- Fiche B11 : [`rapport-universaux.md`](rapport-universaux.md).
