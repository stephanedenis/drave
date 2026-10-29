# N2.10 — professeur français 10 000 pas : 1,073 bit/octet, PPL 2.104

> **Objet.** Améliorer le professeur byte-level de 23,76 M pour donner au student une cible plus
> forte que la PPL 2,355 de N2.2.

## Dispositif

- Qwen3-MoE byte-level, **23,76 M**, **10 000 pas**, lot 16, séquence 128.
- Corpus : `data/corpus_fr_train.txt` ; validation : derniers 5 %.
- VDC pour les fenêtres ; sortie `/tmp/route-teacher-10k`.

## Résultat

| mesure | N2.2 (5 000 pas) | N2.10 (10 000 pas) |
|---|---:|---:|
| validation bits/octet | 1,2359 | **1,0729** |
| **PPL** | 2,355 | **2.104** |
| gain | — | **−10,6 %** |

## Lecture

- Le professeur **s'améliore** de **2,355** à **2.104** avec 5 000 pas de plus.
- Il reste **23,76 M** : c'est la cible de distillation, pas le student.
- La PPL **2.104** rend la porte **2,5** théoriquement accessible, mais le student 11,47 M est
  encore à **3,05**.

## Verdict

**N2.10 est atteint** : professeur **2.104**, meilleur que 2,355.

## Limites

- **Même corpus** ; pas de test externe.
- **10 000 pas** ; le professeur peut encore progresser.
- **Non versionné** : `/tmp/route-teacher-10k`.

## Fichiers

- Code : [`tools/entrainer_moteur.py`](../tools/entrainer_moteur.py).
- JSON : [`native-professeur-10k.json`](native-professeur-10k.json).
