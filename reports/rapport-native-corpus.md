# N2.1 — 50 000 fenêtres pour `drave-n0`

> **Objet.** Construire le corpus d'entraînement de N2 : fenêtres d'octets, split train/validation
> déterministe, manifeste d'offsets. Le corpus source n'est **pas versionné**.

## Résultat

| mesure | valeur |
|---|---:|
| source | `data/corpus_fr.txt` |
| octets | **4 633 889** |
| fenêtre | **128** octets |
| pas | **64** |
| **fenêtres** | **50 000** |
| train | **45 000** |
| validation | **5 000** |
| graine | 0 |

- Manifeste : [`native-corpus.json`](native-corpus.json) — 50 000 offsets, pas le texte.
- Découpage : `tools/corpus_natif.py --source data/corpus_fr.txt --max 50000 --val 5000`.
- Test : `tools/cerveau/tests/test_corpus_natif.py` (100 fenêtres, 90/10).

## Lecture

- **N2.1 est atteint en volume** : 50 000 fenêtres, 45 000/5 000.
- Ce sont des fenêtres **chevauchantes** (pas 64) du **même** corpus : augmenter le nombre de
  fenêtres n'ajoute pas de **données nouvelles**, seulement des vues.
- La **licence** du corpus source reste **à vérifier** avant toute diffusion.
- Le manifeste ne contient **pas** le texte : `data/` est ignoré par git.

## Verdict

**N2.1 — volume : atteint** (50 000 fenêtres). **N2.1 — diversité : non** : il faudra ajouter
d'autres sources (code, dialogue, UDHR, textes publics) avant de conclure à un corpus.

## Limites

- **Un seul corpus**, français, 4,63 Mo.
- **Chevauchement** : les fenêtres ne sont pas indépendantes.
- **Licence non vérifiée**.
- Le split aléatoire ne garantit pas l'absence de fuite entre fenêtres proches.

## Fichiers

- Code : [`tools/corpus_natif.py`](../tools/corpus_natif.py).
- Test : [`tools/cerveau/tests/test_corpus_natif.py`](../tools/cerveau/tests/test_corpus_natif.py).
- JSON : [`native-corpus.json`](native-corpus.json).
