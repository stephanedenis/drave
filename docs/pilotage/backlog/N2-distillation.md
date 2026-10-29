# N2 — Distillation native (50 000 séquences)

> **Statut** : en cours · **Priorité** : P1 · **Programme** : N · **Dépend de** : N1
> **Ligne de roadmap** : N2 · **Fiche de résultat attendue** : rapport-n2-distillation.md (à créer dans `reports/`)
> **Résumé** : Faire tenir le natif sans professeur, sur 50 000 séquences, avec la porte < 2,5 de PPL.
> **Glossaire** : [distillation](../../theorie/glossaire/entrees/distillation.md) · [professeur / élève](../../theorie/glossaire/entrees/professeur-eleve.md) · [perplexité](../../theorie/glossaire/entrees/perplexite.md) · [BPE](../../theorie/glossaire/entrees/bpe.md).

## Le besoin

Le student plafonne à 2,708 et la porte < 2,5 n'est pas atteinte. Les 130–256 de contexte sont négatifs ; il faut décider si le levier est la donnée, la capacité ou la hiérarchie.

**Le levier retenu le 2026-10-29 est la hiérarchie** (l'état de section), et c'est **N2 qui la porte** : R11 en mesurera la fenêtre. Les longueurs brutes ne sont plus essayées — cinq négatifs suffisent.

## L'état

49 999 fenêtres, 4 sources ; professeur 30k 1,734 (0,794 bit/octet) ; student 3,123 à 20 000 pas ; meilleur 2,6998 ; plateau 2,708. Le 21,63 M à budget égal donne −8,1 %, mais à 20 000 pas il est pire (3,381 contre 3,123).

## La porte

PPL < 2,5 sur le jeu tenu à l'écart, avec le contrôle par permutation et le même budget de calcul.

## Contrôles négatifs

- jeu tenu à l'écart ; contrôle par permutation
- même budget de calcul entre tailles
- les négatifs 130–256 sont rejoués dans le même tableau

## Prochaine action

Lancer la série **hiérarchie** (état de section, longueurs croissantes) avec 3 graines et le même budget ; garder la porte < 2,5 comme mesure de la distillation, et passer la main à R11 pour la fenêtre. Ne pas allonger le contexte **brut**.

## Voir aussi

- [Programme N](../roadmap.md#programme-n--le-natif-drvm-drave-n0-distillation)
- [Programme R, R1](../roadmap.md#r1--la-fenêtre-native)
