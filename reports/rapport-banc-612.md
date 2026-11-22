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
