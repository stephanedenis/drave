# N2 — Distillation native (50 000 séquences)

> **Statut** : en cours · **Priorité** : P1 · **Programme** : N · **Dépend de** : N1
> **Ligne de roadmap** : N2 · **Fiche de résultat attendue** : rapport-n2-distillation.md (à créer dans `reports/`)
> **Résumé** : Faire tenir le natif sans professeur, sur 50 000 séquences, avec la porte < 2,5 de PPL.
> **Glossaire** : [distillation](../../theorie/glossaire/entrees/distillation.md) · [professeur / élève](../../theorie/glossaire/entrees/professeur-eleve.md) · [perplexité](../../theorie/glossaire/entrees/perplexite.md) · [BPE](../../theorie/glossaire/entrees/bpe.md).

## Le besoin

Le student plafonne à 2,708 et la porte < 2,5 n'est pas atteinte. Les 130–256 de contexte sont négatifs ; il faut décider si le levier est la donnée, la capacité ou la hiérarchie.

**Le levier retenu le 2026-10-29 est la hiérarchie** (l'état de section), et c'est **N2 qui la porte** : R11 en mesurera la fenêtre. Les longueurs brutes ne sont plus essayées — cinq négatifs suffisent.

## L'état

Le budget est mesuré (N2.d) : 2,9355 → 2,8527, mais **sur un jeu contaminé à 32,8 %**. N2.h a
refait le mètre : corpus dédupliqué (−22,2 % de texte), split par chunks, **0 % de fuite** ; la
chaîne propre vaut **3,09** en domaine et **16,7** sur de la littérature jamais vue — le modèle de
N2 est un **spécialiste du dépôt**. La diversité française (moitié dépôt, moitié littérature)
ramène la littérature à **3,86** pour **+0,17** en domaine.

## La porte

PPL < 2,5 sur le **corpus propre**, tenu à l'écart par construction, avec le contrôle par
permutation et le même budget de calcul. L'élève honnête est à **3,09** : la porte est à **0,59**.

## Contrôles négatifs

- jeu tenu à l'écart ; contrôle par permutation
- même budget de calcul entre tailles
- les négatifs 130–256 sont rejoués dans le même tableau

## Prochaine action

**Le corpus est le levier, pas le budget.** Sur le mètre propre, la diversité française
divise la PPL hors dépôt par 4,3 (16,7 → 3,86) pour +0,17 en domaine, et le verrou de longueur
tombe avec des positions aléatoires. Prochaine action : **plus de texte français unique** (le
corpus propre fait 3,2 Mo d'entraînement) et la **capacité** sur ce mètre ; puis la longueur.

## Voir aussi

- [Programme N](../roadmap.md#programme-n--le-natif-drvm-drave-n0-distillation)
- [Programme R, R1](../roadmap.md#r1--la-fenêtre-native)
