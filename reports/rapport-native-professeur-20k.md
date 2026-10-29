# N2.15 — professeur 20 000 pas : 0,904 bit/octet, PPL 1.871

> **Objet.** Pousser le professeur byte-level à 20 000 pas pour fournir une cible plus proche de
> 2,5 au student.

## Résultat

| mesure | 5 000 pas | 10 000 pas | **20 000 pas** |
|---|---:|---:|---:|
| bits/octet | 1,2359 | 1,0729 | **0,9036** |
| **PPL** | 2,355 | 2,104 | **1.871** |
| durée | 422 s | 1 800 s | **1 669 s** |

- Même architecture 23,76 M, même corpus, VDC.
- Sortie : `/tmp/route-teacher-20k`.

## Lecture

- Le professeur descend à **1.871** de PPL, **sous 2,0**.
- Il est maintenant **nettement plus fort** que le student 11,47 M (**2,876**).
- La porte **2,5** est **accessible au professeur**, pas au student.

## Verdict

**N2.15 — professeur 20k : atteint**, PPL **1.871**.

## Limites

- **Même corpus** ; pas de test externe.
- **20 000 pas** ; peut encore progresser.
- **Non versionné**.

## Fichiers

- Code : [`tools/entrainer_moteur.py`](../tools/entrainer_moteur.py).
- JSON : [`native-professeur-20k.json`](native-professeur-20k.json).
