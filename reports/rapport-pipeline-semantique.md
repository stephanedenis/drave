# B13 — chaîne sémantique M1 → M5 → M6 → M8

> **Objet.** Vérifier que les briques corrigées se **parlent** sur un seul flux. Ce n'est pas un
> nouveau module et ce n'est pas une preuve sémantique : chaque score reste celui de son module.

## Mesures

| étage | mesure | résultat |
|---|---|---:|
| **M1** | code exact sur 528 surfaces réelles | **528/528** |
| **M5** contexte | `source`, ordre 1, split 80/20 par partie, 160 parties test | **18,70 %** (majoritaire 6,49 %) ; surprise **2,423** vs **3,539** |
| **M5** sans contexte | même split | **12,60 %** ; surprise **3,112** |
| **M6** | conjonction 88 essais | **94,32 %** (base 75 %) |
| **M6** | tâche sens/langue 792 essais | **94,95 %** (base 50 %), commutation 0 |
| **M8** | prototypes sur les 528 épisodes (non tenus à l'écart) | champs **96,14 %**, exact **57,95 %**, 7 prototypes |
| **M9** | M1 sans contexte | **70,83 %** |

## Lecture

- **M1** porte la chaîne : sans lui, rien.
- **M5** avec le plateau gagne **+6,1 pts** d'exact et **−1,12 nat** de surprise sur `source` ;
  c'est le gain de contexte déjà mesuré par A6, retrouvé dans le pipeline.
- **M6** est un **sélecteur** ; la commutation reste nulle.
- **M8** est mesuré **sur les épisodes stockés** : 57,95 % d'exact ne dit rien de la généralisation ;
  la mesure honnête reste le leave-one-code-out à **0** (A7).

## Limites

- **M2** n'est pas dans la chaîne : il demande un entraînement GPU séparé.
- **M8** est évalué sur les mêmes épisodes que la consolidation ; c'est une **borne haute**.
- Le pipeline est **Python**, pas le moteur Rust ; il ne prouve pas la sémantique, il prouve
  l'**intégration**.

## Fichiers

- Code : [`tools/cerveau/pipeline_semantique.py`](../tools/cerveau/pipeline_semantique.py).
- Test : [`tools/cerveau/tests/test_pipeline_semantique.py`](../tools/cerveau/tests/test_pipeline_semantique.py).
- JSON : [`pipeline-semantique.json`](pipeline-semantique.json).
