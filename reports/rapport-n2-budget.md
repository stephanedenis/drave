# N2 — le budget paie, les quatre sources coûtent, et la validation n'est pas tenue à l'écart

> **Ligne de roadmap** : N2 (la distillation) · **Date** : 2026-10-31 · **Verdict** : le budget
> complet (20 000 pas, 41 Mo) fait baisser la PPL de **2,9355 à 2,8527** sous le protocole de N2.19 ;
> le corpus à quatre sources la fait **monter** à **3,7591** ; et **32,8 % des fenêtres du protocole
> de validation sont verbatim dans l'entraînement** — sur les fenêtres propres, le meilleur élève
> est à **2,9795**, pas à 2,8527.

## La question

La hiérarchie est écartée deux fois (N2.h1, N2.h2 : 2,9935 contre 2,9927). La roadmap désigne
ensuite **le curriculum et les données** : le dispositif reconstruit plus tôt dans la journée n'avait vu que
**20,48 Mo d'un seul corpus en 5 000 pas**, la moitié du budget de N2 (41 Mo, 20 000 pas, quatre
sources). Ce dispositif est mesuré ici à budget plein, avec trois graines, et comparé à trois
témoins : la base supervisée, la distillation courte de la campagne précédente, et le corpus
à quatre sources.

## Le dispositif — reconstruit, archivé, rejoué

Tout vient de la campagne du 31/10 conservée sur deux disques
(`/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/`, 1,4 Go, manifeste vérifié) :

| pièce | valeur | provenance |
|---|---|---|
| professeur | 23,57 M · 20 000 pas · **0,9195 bit/octet** (PPL 1,892) | `artefacts/route-teacher-20k` |
| élève de base | `drave-n0` 11 469 192 · 20 000 pas supervisés · **3,2161** | `artefacts/drave-n0-base-20k.pt` |
| distillation courte | 5 000 pas · 20,48 Mo · **2,9355** (3 graines) | `artefacts/temoin-g{1,2,3}.pt` |

Le script [`tools/distiller_budget.py`](../tools/distiller_budget.py) ajoute ce qui manquait :
un **plan de stages** (`seq:pas:lr`), le corpus **multi-sources reconstruit à l'identique** depuis
le manifeste [`native-corpus-multi.json`](native-corpus-multi.json) (quotas + ordre de van der
Corput), et un décalage de fenêtres par graine `(graine − 1) × 10 000 019` — sans lui, deux graines
rendent le même nombre (défaut corrigé dans la campagne précédente).

Plan des bras, **budget strictement égal** (20 000 pas × 16 × 128 = **41 Mo vus**), lr 1e-4 sur
10 000 pas puis 3e-5 sur 10 000 — le schéma de la chaîne historique, trois graines :

| bras | données | ce qu'il isole |
|---|---|---|
| **A** | `corpus_fr_train` (français seul) | le budget, à données constantes |
| **B** | manifeste 4 sources : fr 3,8 %, UDHR 3,6 %, **en 82,5 %**, litt. 10,1 % | la diversité, telle que le manifeste la définit |
| **B′** | 4 sources à **quotas égaux** (25 % chacune) | la part de l'anglais dans l'effet de B |
| **C** | A puis 10 000 pas à **seq 129**, lr 5e-6, lot 15 | le curriculum de longueur (N2.33) |

## Ce qui est mesuré

| bras | graines | protocole 8×16×128 | fenêtres propres | fenêtres contaminées | 8×15×129 |
|---|---:|---:|---:|---:|---:|
| **base** — base supervisée 20 000 pas | 1 | 3,2161 | 3,2450 | 3,0756 | 3,2653 |
| **T5k** — 5 000 pas, français (campagne du 31/10) | 3 | 2,9355 ±0,0039 | 3,0534 ±0,0076 | 2,7041 ±0,0036 | 2,9623 ±0,0009 |
| **A** — 20 000 pas, français seul | 3 | 2,8527 ±0,0031 | 2,9795 ±0,0071 | 2,5862 ±0,0016 | 2,8743 ±0,0017 |
| **B** — 20 000 pas, manifeste 4 sources (82,5 % anglais) | 3 | 3,7591 ±0,0075 | 3,8573 ±0,0161 | 3,4554 ±0,0109 | 3,8218 ±0,0092 |
| **Bp** — 20 000 pas, 4 sources à quotas égaux (25 %) | 3 | 3,4350 ±0,0022 | 3,5634 ±0,0039 | 3,1177 ±0,0052 | 3,4848 ±0,0041 |
| **C** — curriculum 129 sur A (10 000 pas) | 3 | 2,8471 ±0,0037 | 2,9783 ±0,0047 | 2,5746 ±0,0028 | 2,8327 ±0,0076 |

Les fenêtres **propres** sont 128 fenêtres tirées en ordre de van der Corput dont les 129
octets n'apparaissent **pas** dans `corpus_fr_train.txt` ; les **contaminées** sont les
128 premières qui y apparaissent. Même calcul de perte, même modèle, même jeu source.

**Contrôle de grille.** Sur quatre grilles de fenêtres (compteurs 0, 1 000 003, 2 000 009,
3 000 029), A reste **sous** le témoin de 5 000 pas : −0,083 à −0,118. La PPL absolue de A, elle,
varie de 2,75 à 2,94 selon la grille : le jeu de validation n'est pas homogène, et c'est la
comparaison **appariée** qui porte le résultat, pas le chiffre absolu.

## Le contrôle négatif

- **permutation** : mêmes octets de validation, ordre détruit — la PPL s'effondre (1086,7460),
  le modèle exploite bien l'ordre et pas les fréquences d'octets ;
- **la base** (aucune distillation) et **la distillation courte** (5 000 pas) encadrent le budget ;
- **B′ contre B** : même budget, même professeur, seule la part de l'anglais change ;
- **C contre A** : comparaison appariée graine par graine, même fenêtres.

## La validation n'est pas tenue à l'écart

C'est le résultat qui change la lecture de la porte. `corpus_fr_val.txt` est la **queue** de
`corpus_fr.txt`, `corpus_fr_train.txt` sa **tête** : les positions sont disjointes (`train + val`
reconstitue exactement les 4 633 889 octets), mais le **contenu se répète** — le corpus empile des
documents qui se recopient.

- **30,7 %** d'un échantillon de 300 fenêtres de validation apparaissent **verbatim** dans
  l'entraînement ; **32,8 %** des 128 fenêtres du protocole (42 sur 128) ;
- **23,5 %** d'un échantillon de 200 fenêtres d'entraînement apparaissent **plus d'une fois** dans
  l'entraînement lui-même ;
- conséquence mesurée sur A : **2,5862** sur les fenêtres contaminées contre **2,9795** sur les
  fenêtres propres — l'écart est de **0,39 de PPL** ;
- la **base** (20 000 pas supervisés, aucune distillation) ne montre que **0,17** d'écart ;
  la distillation courte **0,35**, A **0,39** : la mémoire des répétitions **se construit avec le
  budget**.

Le protocole de N2.19 et de N2.33 échantillonne **depuis le compteur 0** : un tiers de ses fenêtres
sont mémorisables. **2,7078 et 2,6998 sont donc mesurés sur le même jeu contaminé** : la porte
< 2,5 n'a jamais été une mesure de généralisation. La colonne « propres » est la seule qui la donne,
et c'est une **borne basse** : une fenêtre propre peut être à un octet d'une fenêtre vue.

## Ce que ça change pour N2

1. **Le budget paie, mais peu** : **−0,0828** de PPL pour 20 000 pas de plus (2,8527 contre
   2,9355), du même ordre que la chaîne historique (≈ −0,09 par 20 000 pas à lr 3e-5, N2.23).
   La porte < 2,5 n'est pas approchée : il manque **0,3527** sur le protocole, et
   **0,4795** sur les fenêtres propres. À ce rendement — qui décroît — il faudrait de
   l'ordre de **90 000 pas de plus** pour espérer 2,5 ; la chaîne historique en a enchaîné plus de
   100 000 pour arriver à 2,70.
2. **Les données, telles que le manifeste les définit, coûtent** : B perd 0,9064 sur le
   protocole. Le manifeste est à 82,5 % anglais alors que le professeur est **français** : les
   cibles anglaises qu'il donne sont faibles, et le français se dilue. B′ (quotas égaux, 25 % par
   source) coûte encore **+0,58** : l'anglais explique une partie de la perte, pas toute ; dans les
   deux cas, la diversité **n'aide pas la porte française**.
3. **Le curriculum 129** : gagne **0,0416** sur le protocole 129 (comparaison appariée) et
   **0,0056** sur le protocole 128 — réel, mais marginal : il ne déplace pas la porte.
4. **Le prochain levier de N2 n'est pas un levier d'entraînement, c'est le corpus** : reconstruire
   un train/val **au niveau du document** (aucun document des deux côtés), dédupliquer, puis
   remesurer la porte sur des fenêtres propres. Tant que ce n'est pas fait, toute PPL < 2,5 sur ce
   jeu peut venir de la mémoire.

## Ce qui pourrait le rendre faux

- **Le professeur de B est français** : B et B′ mesurent « un corpus majoritairement anglais distillé
  par un professeur français », pas la diversité en général. Le confondant est nommé, pas levé.
- **Le plan de taux d'apprentissage est un choix** (10 000 pas à 1e-4, 10 000 à 3e-5), copié de la
  chaîne historique ; un autre plan peut donner un autre rendement.
- **La détection de duplication est verbatim** : une fenêtre recomposée à partir de deux fenêtres
  vues, ou à un octet près, passe pour propre. La PPL « propres » est donc une **borne basse**, pas
  une mesure exacte.
- **128 fenêtres propres** (16 384 octets) : l'intervalle de confiance sur la PPL reste de l'ordre de
  quelques centièmes ; les écarts de 0,08 sont à la limite, ceux de 0,9 ne le sont pas.
- **Une seule architecture** (11,47 M) : la capacité n'est pas testée ici.

## Fichiers

- Code : [`tools/distiller_budget.py`](../tools/distiller_budget.py) (entraînement) ·
  [`tools/eval_n2_budget.py`](../tools/eval_n2_budget.py) (évaluation et contamination) ·
  agrégat [`n2-budget.json`](n2-budget.json).
- Points de contrôle : **12 `.pt` (542 Mo) archivés sur deux disques** —
  `/home/stephane/Data13TB/stephane/backups/n2/2026-10-31/n2d/` et
  `/home/stephane/IA/artefacts/n2/2026-10-31/n2d/` ; `work/n2d/` reste la copie de travail.
