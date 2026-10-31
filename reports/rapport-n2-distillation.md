# N2 — la hiérarchie ne paie pas non plus sur le dispositif de distillation

> **Ligne de roadmap** : N2 (la hiérarchie) · **Date** : 2026-10-31 · **Verdict** : ❌ **négatif** —
> à budget strictement égal, l'état de section transporté entre segments ne bat pas le modèle nu :
> **2,9935 contre 2,9927** (protocole segmenté, trois graines). L'écart, **+0,029 %**, est du même
> ordre que la dispersion entre graines.

## La question

N2 plafonne à **2,6998** et le contexte s'arrête à 129 octets. Le levier retenu par la roadmap est
la **hiérarchie** — un état de section qui résume les octets lus et se transporte d'un segment au
suivant. Une première ablation, sur le petit corpus (`rapport-n2-hierarchie.md`), avait rendu un
négatif net : état **3,9759** contre témoin **3,9617**, et surtout **confondu avec un état
étranger** (3,9764). Il fallait refaire la mesure sur le **vrai dispositif de N2** : professeur
byte-level, distillation, 11,5 M d'élève.

## Le dispositif — reconstruit, parce que tout avait disparu

Le professeur, l'élève, le corpus distillé et les points de contrôle vivaient dans `/tmp`, effacés
au démarrage de la machine (07 h 09). La campagne a donc d'abord **reconstruit** la chaîne :

| pièce | valeur | référence historique |
|---|---|---|
| professeur | 23,57 M · 20 000 pas · **0,9195 bit/octet** (PPL 1,892) | 23,76 M · **0,9036 bit/octet** (PPL 1,869) |
| élève de base | 20 000 pas · PPL **3,2064** (standard) | « pont » 3,295 |
| distillation | 5 000 pas × 8 × 4 × 128 = **20,48 Mo vus**, lr 1e-4, T=2, α=0,7 | 20 000 pas × 16 × 128 = 41 Mo |

Trois bras, **mêmes octets, mêmes fenêtres, mêmes pas** : **témoin** (modèle nu), **hiérarchie**
(`GRUCell(224)` sur la moyenne du segment, injecté avant les blocs), **contrôle** (même
architecture, état roulé = celui d'un autre document du lot). Trois graines ; BPTT tronquée à un
segment ; état remis à zéro à chaque pas, les échantillons étant des documents indépendants.

Banc : [`tools/distiller_section.py`](../tools/distiller_section.py) · évaluation
[`tools/eval_n2.py`](../tools/eval_n2.py) · données [`n2-distillation.json`](n2-distillation.json).

## Ce qui est mesuré

PPL sur **256 fenêtres** de `corpus_fr_val`, trois protocoles (moyenne ± étendue sur trois graines) :

| bras | standard 128 | segmenté 4×128 | segmenté, sans état |
|---|---:|---:|---:|
| **témoin** | **2,9639** ±0,0019 | **2,9927** ±0,0039 | 2,9927 ±0,0039 |
| **hiérarchie** | 2,9646 ±0,0039 | **2,9935** ±0,0077 | 2,9953 ±0,0039 |
| **contrôle** | 2,9638 ±0,0137 | 2,9952 ±0,0055 | 2,9965 ±0,0046 |

- **hiérarchie − témoin** : **+0,0007** (standard, +0,024 %) · **+0,0009** (segmenté, +0,029 %) ;
- **contrôle − témoin** : −0,0001 (standard) · **+0,0025** (segmenté) ;
- **hiérarchie − contrôle** : +0,0008 (standard) · **−0,0016** (segmenté).

La distillation, elle, paie : l'élève passe de **3,2064 à 2,9639** (standard), soit **−0,24**, très
au-dessus du bruit. C'est le seul effet solide du tableau.

## Le contrôle négatif, et ce qu'il dit

Deux lectures, et il faut les tenir ensemble :

1. **contre le modèle nu, l'état ne gagne rien** (+0,029 %, dans la dispersion des graines) ;
2. **contre son propre contrôle sans état, l'état transporte un peu d'information** : 2,9935 avec
   état contre 2,9953 sans (−0,0017), et il bat l'état **étranger** de 0,0016 sur le protocole
   segmenté.

Autrement dit : l'état n'est pas du bruit, mais **il coûte exactement ce qu'il rapporte**. La
machinerie (GRU, injection, 350 k paramètres de plus) annule le signal qu'elle transporte. C'est la
même conclusion que N2.h1, avec des chiffres dix fois plus serrés.

## Ce qui pourrait le rendre faux

- **Le budget est court** : 20,48 Mo vus, la moitié de la distillation de N2 (41 Mo), et **sans le
  curriculum 129**. L'état de section pourrait payer plus loin — mais c'est précisément au-delà de
  129 octets que N2 avait échoué.
- **La BPTT est tronquée à un segment** : l'état ne reçoit aucun gradient du segment suivant.
- **Les graines ne variaient d'abord rien** : modèle chargé, aucun dropout, fenêtres déterministes.
  Le premier `temoin g2` rendait *exactement* 2,972744888777891, le même nombre que `temoin g1` ;
  les graines 2 et 3 ont été refaites avec un décalage de fenêtres de `(graine−1) × 10 000 019`.
- **Les PPL ne sont pas comparables à 2,6998** : fenêtres d'évaluation, jeu de validation et budget
  diffèrent. Cette fiche ne dit rien de la porte **< 2,5** ; elle dit que ce levier ne la rapproche
  pas.

## Ce que ça change pour N2

Le levier « état de section » est **testé deux fois, négatif deux fois** — sur le petit corpus et
sur le dispositif de distillation. Il ne doit plus être la prochaine action de N2. Restent, dans
l'ordre du graphe : **le curriculum et les données** (41 Mo, 4 sources, 20 000 pas), **la
capacité** (le 21,63 M à budget égal donnait −8,1 %), et **la fenêtre brute**, que R11 doit
trancher. La porte **< 2,5** n'est pas atteinte et n'a pas été approchée ici.
