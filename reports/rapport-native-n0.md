# N1.2 — `drave-n0` : PPL 3,35 sur le corpus français

> **Objet.** Premier entraînement du modèle natif : `drave-n0`, **11,37 M** paramètres, octets,
> 6 blocs, attention locale, FFN creux, têtes précoces, cellule de pensée. Le but de cette passe
> est le **prochain octet** ; les pertes locales, les têtes entraînées et la pensée mesurée
> viendront après.

## Dispositif

- **Corpus** : `data/corpus_fr.txt`, **4 633 889 octets** ; validation = **derniers 5 %**
  (10 000 octets minimum).
- **Modèle** : 11 368 392 paramètres ; 6 blocs ; `d=224`, 4 têtes, fenêtre **256**,
  8 experts top-2, **k-WTA 25 %**, 3 têtes précoces, 2 pas de pensée.
- **Entraînement** : **10 000 pas**, lot **8**, séquence **128**, lr **3e-4**, AdamW,
  clipping 1,0, graine 1, GPU 0, **448,5 s**.

## Résultats

| mesure | valeur |
|---|---:|
| perte finale | **1,1536** |
| **PPL validation** | **3,3534** |
| jetons de validation | 8 192 |
| paramètres | **11 368 392** |
| DRVM exporté | **110 tenseurs**, 12 blocs |
| SHA-256 du DRVM | `edf90a97…fcec2e1` |

Courbe : **13,53** à 200 pas, **8,21** à 1 000, **4,35** à 5 000, **3,35** à 10 000.

## Lecture

- Le natif **apprend** : la PPL passe de **13,5** à **3,35** en 10 000 pas, sous la cible **4,0**.
- C'est un **modèle de prochain octet**, pas un assistant : aucune tête précoce n'est entraînée,
  aucune perte locale, aucun pont.
- La validation est **le même corpus** ; ce n'est pas une preuve de généralisation hors domaine.
- Le DRVM est **écrit** et **lu** par le moteur (`--drvm-inspect`) ; la **parité PPL
  entraîneur ↔ moteur** reste à faire, le moteur ne sait pas encore exécuter un bloc DRVM.

## Verdict

**N1.2 est atteint pour la PPL de base** : **3,35 < 4,0**. Le modèle est un **banc de mécanismes**
qui apprend ; il ne raisonne pas encore, ne sort pas tôt, et ne pense pas de façon mesurée.

## Limites

- **Même corpus** pour l'entraînement et la validation ; pas de test externe.
- **Prochain octet seulement** : les pertes locales, têtes précoces, pensée et pont ne sont pas
  entraînés.
- **Pas de parité moteur** : `drave-core` lit le DRVM, mais n'exécute pas encore la passe avant.
- **11,37 M** : modèle de banc, pas d'assistant.

## Fichiers

- Code : [`tools/native_model.py`](../tools/native_model.py),
  [`tools/entrainer_native.py`](../tools/entrainer_native.py).
- JSON : [`native-n0.json`](native-n0.json).
