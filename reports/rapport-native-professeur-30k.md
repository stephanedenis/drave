# N2.20 — professeur 30 000 pas : 0,794 bit/octet, PPL 1.734

> **Objet.** Pousser le professeur byte-level à 30 000 pas pour fournir une cible plus proche de
> 2,5 au student.

## Résultat

| mesure | 10 000 | 20 000 | **30 000** |
|---|---:|---:|---:|
| bits/octet | 1,0729 | 0,9036 | **0,7940** |
| **PPL** | 2,104 | 1,869 | **1.734** |
| durée | 1 800 s | 1 669 s | **2 407 s** |

- Même architecture 23,76 M, même corpus, VDC.
- Sortie : `/tmp/route-teacher-30k`.

## Lecture

- Le professeur descend à **1.734** de PPL.
- Il est **très au-dessus** du student 11,47 M (**2,708**).
- La cible **2,5** est **facile** pour le professeur, **difficile** pour le student.

## Verdict

**N2.20 — professeur 30k : atteint**, PPL **1.734**.

## Limites

- **Même corpus**, pas de test externe.
- **Non versionné**.

## Fichiers

- Code : [`tools/entrainer_moteur.py`](../tools/entrainer_moteur.py).
- JSON : [`native-professeur-30k.json`](native-professeur-30k.json).
