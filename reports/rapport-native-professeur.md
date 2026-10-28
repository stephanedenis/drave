# N2.2 — le professeur local : 23,76 M, 1,236 bit/octet

> **Objet.** Entraîner un professeur **octet** exécutable par le moteur, pour distiller `drave-n0`
> sans tokenizer intermédiaire. Le professeur est un Qwen3-MoE byte-level.

## Résultat

| mesure | valeur |
|---|---:|
| famille | Qwen3-MoE byte-level |
| paramètres | **23,76 M** |
| pas | 5 000 |
| lot / séquence | 16 / 128 |
| validation | **1,2359 bit/octet** |
| **PPL validation** | **2.355** |
| durée | 422 s GPU |

- Corpus : `data/corpus_fr_train.txt`, 4,40 Mo ; validation = derniers 5 %.
- Sortie : `/tmp/route-teacher` (non versionnée).
- Log : `/tmp/route-teacher.log`.

## Lecture

- Le professeur est **meilleur** que `drave-n0` : **2,355** contre **3,465** de PPL.
- Il est **deux fois plus gros** (23,76 M contre 11,47 M) et lit **1,84 M** poids par jeton et par couche.
- Il parle **256 octets**, donc la distillation vers le student ne demande **aucun tokenizer**.

## Verdict

**N2.2 est atteint** : un professeur local byte-level est entraîné et mesuré. Il est plus fort que le
student, ce qui rend N2.3 utile.

## Limites

- **Même corpus** pour l'entraînement et la validation ; pas de test externe.
- **5 000 pas** seulement ; le professeur peut encore progresser.
- **Non versionné** : `/tmp/route-teacher` disparaîtra au redémarrage.

## Fichiers

- Code : [`tools/entrainer_moteur.py`](../tools/entrainer_moteur.py).
- JSON : [`native-professeur.json`](native-professeur.json).
