# N2.9 — student 21,63 M sur 20 000 pas : 3,381, toujours derrière 11,47 M

> **Objet.** Donner au student de 21,63 M un **vrai budget** (20 000 pas) pour voir si la capacité
> finit par payer, après le résultat confondu de N2.5 (5 000 pas) et le budget égal de N2.5b.

## Dispositif

- Professeur : `/tmp/route-teacher`, **23,76 M**, PPL **2,355**.
- Student : **21 634 536** paramètres, initialisation aléatoire, **20 000 pas**, lot 8, lr 1e-4,
  T=2, alpha 0,7, têtes précoces, VDC.
- **1 276 s** GPU.

## Résultats

| mesure | 11,47 M | 21,63 M |
|---|---:|---:|
| 5 000 pas | **3,295** (checkpoint) | **4,294** |
| **20 000 pas** | **3,123** | **3,381** |
| précision principale | 67,96 % | **66,80 %** |
| tête 3 | 68,01 % | **65,43 %** |
| gap au professeur | +0,768 | **+1,026** |

## Lecture

- **Plus gros, toujours moins bon** : **3,381** contre **3,123**, soit **+8,3 %**.
- Le 21,63 M **progresse** de 4,294 à 3,381 en 15 000 pas de plus, mais **ne rattrape pas** le
  11,47 M.
- La tête 1 reste faible (**34,7 %**) : les premières couches du gros modèle ne sont pas assez
  entraînées.
- **La capacité seule ne suffit pas** à ce budget : l'initialisation, le lot et le nombre de pas
  dominent.

## Verdict

**N2.9 — négatif** : à 20 000 pas, le student **21,63 M** est **pire** que le **11,47 M**. La porte
**PPL < 2,5** reste **non atteinte**.

## Limites

- **20 000 pas** ; le 21,63 M n'est peut-être pas convergé.
- **Lot 8** ; le 11,47 M a été distillé avec lot 16 pour N2.8.
- **Une seule graine** pour ce point.
- **Même corpus**, pas de test externe.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-21m-20k.json`](native-21m-20k.json).
