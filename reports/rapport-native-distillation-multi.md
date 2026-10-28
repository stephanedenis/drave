# N2.7 — distillation multi-sources : 9,517, au niveau du professeur

> **Objet.** Distiller `drave-n0` sur le corpus multi-sources (fr, UDHR, en, littérature) avec un
> professeur **multi**, tous deux échantillonnés par van der Corput.

## Dispositif

- Professeur : Qwen3-MoE byte-level **23,76 M**, **5 000 pas**, validation **3,2587 bit/octet**, PPL **9.571**.
- Student : `drave-n0` **11 469 192** paramètres, initialisé depuis `/tmp/drave-n0-pont.pt`.
- **5 000 pas**, lot 16, séquence 128, lr 2e-4, T=2, alpha 0,7, têtes précoces.
- Corpus : `data/corpus_multi_train.txt` (115,4 Mo) ; validation 6,08 Mo.
- **341 s** GPU.

## Résultats

| mesure | professeur | student |
|---|---:|---:|
| PPL validation | **9.571** | **9.517** |
| bits/octet | **3,2587** | — |
| précision principale | — | **36,34 %** |
| têtes précoces | — | **30,10 / 34,08 / 36,83 %** |
| paramètres | 23,76 M | **11,47 M** |

- **Écart student − professeur** : **-0.055** de PPL (**-0.6 %**).
- Le student **égale** le professeur avec **deux fois moins** de paramètres.

## Lecture

- Sur le corpus **multi**, le student **rattrape** le professeur : **9,517** contre **9,571**.
- Mais les deux sont **bien plus mauvais** que sur le français seul (**3,3**) : le corpus est plus
  difficile, et la PPL n'est **pas comparable** entre corpus.
- La **précision** tombe à **36,3 %** : le multi-sources est un autre problème.
- La porte N2 (**< 2,5**) reste **non atteinte** ; elle était définie sur le français.

## Verdict

**N2.7 — atteint comme distillation** : le student égale le professeur sur le multi. **N2 — porte < 2,5
non atteinte** : le corpus multi n'est pas le français, et la cible doit être **redéfinie par corpus**.

## Limites

- **Un seul teacher multi**, 5 000 pas.
- **PPL non comparable** au français.
- **Pas de test externe**.
- **Têtes** mesurées mais pas utilisées pour sortir tôt.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-distillation-multi.json`](native-distillation-multi.json).
