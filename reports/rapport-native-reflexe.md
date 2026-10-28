# N1.7 — le réflexe de `drave-n0` : 24 % plus rapide

> **Objet.** Mesurer le **gain de temps** du réflexe : sortir après **4 blocs** au lieu de 6, avec la
> tête précoce 2 (60,9 % de précision) contre la tête principale (62,6 %).

## Résultat

| mesure | valeur |
|---|---:|
| passe complète (6 blocs) | **7,871 ms** |
| réflexe (4 blocs) | **5,978 ms** |
| **gain** | **24,05 %** |
| précision principale | **62,55 %** |
| précision du réflexe | **60,94 %** |
| coût en précision | **−1,61 point** |

- GPU 0, séquence **128**, lot 1, **50 répétitions** après 10 échauffements, `torch.cuda.synchronize`.
- Modèle : 11,47 M, pont, pensée contractante, 3 têtes.

## Lecture

- Le réflexe **économise un quart du temps** (24,05 %) pour **1,61 point** de précision.
- C'est un **compromis** : le gain est réel, le coût est mesurable, et les deux sont nommés.
- La mesure est **GPU** ; le gain CPU pourrait différer.

## Verdict

**N1.7 est positif** : le réflexe après **4 blocs** donne **24 %** de temps pour **1,6 point** de
précision. Le seuil d'acceptation reste à décider par usage.

## Limites

- **Lot 1**, séquence 128 ; pas de batch.
- **50 répétitions**, une graine ; pas d'intervalle.
- Le **temps** inclut la tête précoce, pas le transport.
- Un seul modèle.

## Fichiers

- Code : [`tools/native_model.py`](../tools/native_model.py) (`forward_jusqua`).
- JSON : [`native-reflexe.json`](native-reflexe.json).
