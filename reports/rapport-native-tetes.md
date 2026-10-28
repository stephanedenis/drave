# N1.4 — les têtes précoces de `drave-n0` : 55,2 / 60,9 / 62,1 %

> **Objet.** Entraîner les **trois têtes précoces** de `drave-n0` avec le modèle, et mesurer
> leur précision top-1 par rapport à la tête principale. C'est le **réflexe** : décider avant la
> fin du graphe.

## Dispositif

- `drave-n0` : **11 368 392** paramètres, 6 blocs, octets, fenêtre 256, 8 experts top-2,
  k-WTA 25 %, **3 têtes précoces** après les blocs 2, 4, 6.
- **Corpus** : `data/corpus_fr.txt`, **4,63 Mo** ; validation = derniers **5 %**.
- **10 000 pas**, lot 8, séquence 128, lr 3e-4, AdamW, graine 1 ; les pertes des trois têtes
  s'ajoutent à la perte principale.
- **475,7 s** GPU 0.

## Résultats

| tête | position | précision top-1 |
|---|---|---:|
| principale | après le bloc 6 | **62,55 %** |
| précoce 1 | après le bloc 2 | **55,15 %** |
| précoce 2 | après le bloc 4 | **60,94 %** |
| précoce 3 | après le bloc 6 | **62,13 %** |
| **témoin uniforme** | — | **0,39 %** (1/256) |

- **PPL validation** : **3,3634** (contre 3,3534 sans pertes précoces : +0,30 %).
- **DRVM** : 110 tenseurs, 44 Mo, lu par `--drvm-inspect`.

## Lecture

- Les têtes **apprennent** : **55,2 %** après 2 blocs, **60,9 %** après 4, **62,1 %** après 6.
- La **tête 3** est à **0,4 point** de la principale : le réflexe tardif est presque gratuit.
- La **tête 1** coûte **7,4 points** : sortir après deux blocs est possible, mais ce n'est pas gratuit.
- Le **témoin uniforme** est à **0,39 %** : les têtes ne sont pas des classifieurs au hasard.
- La PPL **ne se dégrade pas** (3,363 contre 3,353) : les pertes précoces n'ont pas cassé le modèle.

## Verdict

**N1.4 est atteint** : les têtes précoces sont **entraînées** et **mesurées** ; le réflexe après
4 et 6 blocs est proche de la sortie complète. Il reste à mesurer le **coût** (temps, octets) et
à décider du **seuil** d'acceptation du réflexe.

## Limites

- **Même corpus** pour l'entraînement et la validation ; pas de test externe.
- **Top-1 seulement** ; pas de calibration, pas de seuil d'abstention.
- **Pas de mesure de temps** : le gain du réflexe n'est pas encore chiffré.
- **Pas de contrôle par tête aléatoire entraînée** : le témoin est uniforme.

## Fichiers

- Code : [`tools/native_model.py`](../tools/native_model.py),
  [`tools/entrainer_native.py`](../tools/entrainer_native.py).
- JSON : [`native-tetes.json`](native-tetes.json).
