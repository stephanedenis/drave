# R11 — Contexte hiérarchique et état de section

> **Statut** : spécifiée · **Priorité** : P1 · **Programme** : R · **Dépend de** : R01, N1, N2
> **Ligne de roadmap** : R1.1 · **Fiche de résultat attendue** : rapport-r11-contexte-hierarchique.md (à créer dans `reports/`)
> **Résumé** : Lire par sections avec un état de section, sans exiger que l'attention voie toute la page.
> **Glossaire** : [perplexité](../../theorie/glossaire/entrees/perplexite.md) · [test de l'aiguille](../../theorie/glossaire/entrees/test-de-l-aiguille.md) · [graphe de document](../../theorie/glossaire/entrees/graphe-de-document.md).

## Le besoin

Le natif surapprend 129 octets et échoue à 130–256. Avant d'allonger le contexte brut, il faut une hiérarchie : span → paragraphe → section → document, avec un état qui résume chaque section.

**Ordre arrêté le 2026-10-29** : c'est **N2** qui porte la hiérarchie (l'état de section, 3 graines) ; R11 mesure la fenêtre qui en résulte et n'ouvre donc qu'après N2. La mesure reste ici : PPL à 1 000 octets, aiguille native, stabilité.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | des octets, des frontières de section (R01) et un état courant |
| **sortie** | un état de section et un état de document, utilisables par le décodeur |
| **coût** | coût linéaire en octets, mémoire d'état bornée |
| **trace** | l'état de section est sauvé et rejouable |

## Ce qui est mesuré

- PPL à 1 000 octets contre 129
- aiguille native à 4 000 octets
- taille de l'état et stabilité sur plusieurs sections

## Portes

1. PPL à 1 000 octets dans un facteur 1,5 de celle à 129
2. aiguille native ≥ 15/18 à 4 000 octets
3. l'état ne s'effondre pas sur 10 sections

## Contrôles négatifs

- contexte plat sans état ; état constant ; sections mélangées
- même budget de calcul à 129 octets

## Ce qui pourrait le rendre faux

- l'état de section contient la réponse gold
- l'évaluation est faite sur la longueur d'entraînement
- une seule graine

## Étapes

1. définir l'état de section et la frontière
2. entraîner sur des sections de longueur croissante
3. mesurer PPL, aiguille, stabilité ; écrire la fiche

## Documents à écrire

- `contexte-hierarchique.md` (état, frontières, entraînement, porte, dans `docs/implantation/`)
- mettre à jour R1.1

## Voir aussi

- [Programme R](../roadmap.md#r1--la-fenêtre-native)
- [Analyse, § 5.2](../../theorie/lecture-rapide.md#52-la-fenêtre-et-la-hiérarchie-l2)
