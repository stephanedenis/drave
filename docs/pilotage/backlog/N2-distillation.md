# N2 — Distillation native (50 000 séquences)

> **Statut** : en cours · **Priorité** : P1 · **Programme** : N · **Dépend de** : N1
> **Ligne de roadmap** : N2 · **Fiches de résultat** : `rapport-n2-200k`, `rapport-n2-r11`, `rapport-n2-fenetre`, `rapport-n2-production-fenetre`
> **Résumé** : Faire tenir le natif sans professeur, sur 50 000 séquences, avec la porte < 2,5 de PPL.
> **Glossaire** : [distillation](../../theorie/glossaire/entrees/distillation.md) · [professeur / élève](../../theorie/glossaire/entrees/professeur-eleve.md) · [perplexité](../../theorie/glossaire/entrees/perplexite.md) · [BPE](../../theorie/glossaire/entrees/bpe.md).

## Le besoin

Le student plafonne à 2,708 et la porte < 2,5 n'est pas atteinte. Les 130–256 de contexte sont négatifs ; il faut décider si le levier est la donnée, la capacité ou la hiérarchie.

La **hiérarchie** (l'état de section) a été **écartée** : R11 ne la retient pas. Le levier mesuré le **03/11** est la **fenêtre entraînée** (RoPE) — 1 024 est la recette de production.

## L'état

Le budget est mesuré (N2.d) : 2,9355 → 2,8527, mais **sur un jeu contaminé à 32,8 %**. N2.h a
refait le mètre : corpus dédupliqué (−22,2 % de texte), split par chunks, **0 % de fuite** ; la
chaîne propre vaut **3,09** en domaine et **16,7** sur de la littérature jamais vue — le modèle de
N2 est un **spécialiste du dépôt**. La diversité française (moitié dépôt, moitié littérature)
ramène la littérature à **3,86** pour **+0,17** en domaine.

Depuis, deux mesures : le run de **200 000 pas** (1,02 Go) donne **3,1591 / 5,6056 / 7,2770 /
8,0018** (val_fr / littérature / anglais / wikitext2) ; la **fenêtre entraînée 1 024** donne
**2,4759 / 2,4373** au **grand corpus** — **sous 2,5** — et **2,7856** sur le **corpus propre**.
512 paie hors domaine, **2 048 ne paie pas** ; le compute ne remplace pas la fenêtre.

## La porte

PPL < 2,5 sur le **corpus propre**, tenu à l'écart par construction, avec le contrôle par
permutation et le même budget de calcul. L'élève honnête est passé de **3,09** à **2,7856** sur le
corpus propre (**0,29** de la porte) et **2,4759 / 2,4373** au grand corpus — **sous 2,5**.

## Contrôles négatifs

- jeu tenu à l'écart ; contrôle par permutation
- même budget de calcul entre tailles
- les négatifs 130–256 sont rejoués dans le même tableau

## Prochaine action

**La fenêtre est la recette ; il reste la porte propre.** Prochaine action : la **porte propre**
(0,29 manquant à 2,7856) — données ou capacité — puis **R1.2 à 1 024** entraînée et **N4**. Les
200 k pas seuls ne suffisent pas (3,16) ; la longueur reste le levier de la largeur (positions
aléatoires : 256 octets de 14,11 à 3,25).

## Voir aussi

- [Programme N](../roadmap.md#programme-n--le-natif-drvm-drave-n0-distillation)
- [Programme R, R1](../roadmap.md#r1--la-fenêtre-native)
