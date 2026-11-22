# Le banc du modèle natif sur le gold gelé (602 phrases)

> **Ce que ce document est.** La génération du 100 M (checkpoint 3 000 pas, le meilleur) sur les
> **602 phrases du gold gelé** — l'amorce est le début de la phrase réelle, la sortie est mesurée
> contre le lexique du gold. L'outil : [`tools/banc_612.py`](../tools/banc_612.py) ; le JSON :
> [`banc-612.json`](banc-612.json) ; le banc de style (20 prompts) :
> [`rapport-banc-generation.md`](rapport-banc-generation.md).

## 1. La mesure

| mesure | valeur | ce que ça dit |
|---|---:|---|
| phrases | **602** | tout le gold gelé |
| **mots valides** | **0,755** (6 087 mots) | 3 mots sur 4 existent dans le lexique du gold |
| **répétition** (2-grammes) | **3** | pas de boucle |
| **sorties non-UTF-8** | **0** | aucune dérive d'encodage |
| le débit | **127,5 octets/s** | GPU (le 100 M) |
| la durée | **75,5 s** | 602 phrases × 16 octets |
| le lexique | 769 mots | le vocabulaire du gold |

## 2. Le contrôle : les 20 prompts du banc de style

| banc | amorce | mots valides | répétition |
|---|---|---:|---:|
| le banc de style | 20 prompts écrits à la main | **0,882** | 6 |
| **le banc 612** | le début des 602 phrases du gold | **0,755** | **3** |

**La lecture honnête** : la génération sur de **vraies phrases** est **moins bonne** que sur les
prompts du banc de style (0,755 contre 0,882) — les prompts du banc sont plus courts et plus
« faciles », et le gold contient des phrases longues, ponctuées, avec des mots rares. La répétition
est **meilleure** (3 contre 6).

## 3. Ce que ça ne dit pas

- **La qualité** : « mots valides » ne dit pas que la phrase **a du sens** — le modèle peut aligner
  des mots réels sans composer. C'est le défaut connu du natif (le diagnostic du 16/11).
- **La comparaison au 34 M** : le même banc n'a pas été lancé sur le 34 M (le checkpoint existe,
  il faudrait 2 min sur CPU).
- **Le gold est petit** : 602 phrases, 769 mots de lexique — un banc de **débit** et de **dérive**,
  pas de qualité linguistique.

## 4. Le prochain pas

Le **même banc sur le 34 M** (le contrôle) et sur le **30 k** (le témoin du sur-apprentissage) :
la comparaison des trois checkpoints sur **le même corpus** donnera la vraie courbe.
## 5. Le deuxième témoin : le 30 k sur le même banc

| checkpoint | mots valides | répétition | **non-UTF-8** | octets/s |
|---|---:|---:|---:|---:|
| 3 000 pas | 0,755 | 3 | **0** | 127,5 |
| **30 000 pas** | **0,763** | 3 | **29** | 116,3 |

**Le résultat surprenant** : sur les **602 phrases réelles**, le 30 k fait **légèrement mieux**
(0,763 contre 0,755) — alors que sur les 20 prompts du banc de style, il fait **beaucoup moins bien**
(0,501 contre 0,882).

**L'explication la plus probable** : le banc de style mesure la **créativité** (des prompts courts,
le modèle doit inventer) ; le banc 612 mesure la **continuité** (l'amorce est une vraie phrase, le
modèle prolonge). Le sur-apprenti **prolonge** mieux une phrase connue, mais **invente** moins bien.
Ce n'est pas une contradiction : c'est **deux mesures différentes**.

**Le signal d'alerte** : les **29 sorties non-UTF-8** du 30 k (contre 0 pour le 3 k) — le
sur-apprentissage produit des séquences d'octets invalides. C'est un défaut **mesuré**, pas une
impression.

**La conclusion** : le **3 k reste la référence** (0 dérive, meilleure créativité) ; le **30 k est
le témoin** (meilleure continuité, dérive d'encodage). Les deux mesures sont nécessaires — un banc
unique mentirait.
## 6. Le troisième témoin : le 34 M sur le même banc

| checkpoint | paramètres | mots valides | répétition | non-UTF-8 | octets/s |
|---|---:|---:|---:|---:|---:|
| 34 M (30 k pas, `n0-rope`) | 34,3 M | **0,666** | 3 | 3 | 107,4 |
| **100 M (3 000 pas)** | 96,7 M | **0,755** | 3 | **0** | 127,5 |
| 100 M (30 000 pas) | 96,7 M | 0,763 | 3 | 29 | 116,3 |

**Le classement** : le 100 M **bat le 34 M de 9 points** (0,755 contre 0,666) sur les phrases
réelles — et le 100 M n'a vu que **0,24 jeton/paramètre** contre **7,2** pour le 34 M. C'est la
**confirmation** de la thèse du 16/11 : **l'échelle paie par jeton vu**.

**Le détail qui nuance** : le 34 M est **stable** (3 non-UTF-8 seulement), le 100 M à 3 000 pas est
**parfaitement propre** (0), et le 100 M à 30 000 pas **dérive** (29). Le sur-apprentissage n'est
pas la taille : c'est le **ratio données/paramètres**.

**Le protocole est reproductible** : le même outil (`tools/banc_612.py`), les mêmes 602 phrases,
le même lexique (769 mots), sur les trois checkpoints.
