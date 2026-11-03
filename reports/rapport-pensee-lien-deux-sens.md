# B13 — contre-fiche : le « plafond 5/10 » était un artefact — 5/5 en arrière, 4/5 en avant (9/10)

> **Ligne de roadmap** : **L/B13** · **Date** : 2026-11-03 · **Verdict** : ⚠️ **correction d'une
> mesure antérieure** — le « plafond 5/10 » est faux. Les 10 paires se répartissent en **5 paires
> arrière** (assertion **avant** la question : r418–r422 → r423–r427) et **5 paires avant**
> (assertion **après** la question : r408–r412 → r423–r427). Le lien arrière ne peut pas trouver
> les secondes **par construction** ; leur 0/5 n'est pas une limite, c'est une erreur de banc.

## 1. L'erreur

Ma fiche `rapport-pensee-lien-thematique.md` concluait « le lien de surface plafonne à 5/10 ».
C'était faux : j'avais étendu le banc à 10 paires, mais **5 d'entre elles ont l'assertion après la
question** (positions 417–421 contre 407–411) alors que `trouver_precedente` ne regarde que
**derrière**. Le 0/5 était donc mécanique.

## 2. Les deux sens

| lien | paires | justes | taux |
|---|---:|---:|---:|
| **arrière** (assertion avant) | 5 | **5** | **1,00** |
| **avant** (assertion après) | 5 | **4** | **0,80** |
| **total** | 10 | **9** | **0,90** |

- Le lien **arrière** est celui du banc d'origine (`fidelite_lien_auto`) : **5/5**.
- Le lien **avant** (`trouver_suivante`, nouveau, miroir du précédent) : **4/5**.
- Le **contextuel** reste 5/5.

## 3. L'échec unique

La seule paire manquée est **r412 → r427** : « Ne lis-tu pas ? » (fr) → « **You come tomorrow.** »
(en). C'est une paire **croisée fr/en du gold** : le sujet `tu` ne peut pas égaler `You`, ni le verbe
`lis` égaler `come`. Ce n'est pas une limite du lien, c'est un **défaut du gold**.

## 4. Le contrôle négatif

- Le lien arrière sur les paires avant : **0/5** par construction (l'assertion est après).
- Le lien avant sur les paires arrière : **0/5** par construction.
- Le contextuel : 5/5 — la difficulté est bien le **sens** du lien, pas la réponse.

## 5. Ce qui pourrait rendre ce résultat faux

- 10 paires seulement, dont une croisée : la statistique est fragile.
- Le lien avant n'a été mesuré que sur 5 paires.
- Le gold réel est écrit par le même auteur que le banc.

## 6. La suite

1. **Corriger le gold** : la paire r412→r427 est croisée ; soit la remplacer, soit la sortir du banc.
2. Étendre les paires avant/arrière (10, 20) pour stabiliser.
3. Le « plafond » est levé : **9/10** au total.

## 7. Fichiers

- [`pensee-lien-deux-sens.json`](pensee-lien-deux-sens.json) — les mesures des deux sens.
- [`tools/tests/linguistique/miroir.py`](../tools/tests/linguistique/miroir.py) — `trouver_suivante`,
  `fidelite_lien_avant`.
