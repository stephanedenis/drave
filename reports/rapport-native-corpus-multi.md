# N2.6 — corpus diversifié : 49 999 fenêtres, quatre sources

> **Objet.** Répondre au reproche de N2.1 : un seul corpus, français. On construit un manifeste
> multi-sources sans concaténer les fichiers.

## Résultat

| mesure | valeur |
|---|---:|
| sources | **4** |
| fenêtres | **49 999** |
| train / validation | **44 999 / 5 000** |
| fenêtre / pas | 128 / 64 |
| `corpus_fr.txt` | 4,63 Mo, 72 403 fenêtres possibles |
| `udhr_train.txt` | 4,38 Mo, 68 433 |
| `corpus_en.txt` | 100,28 Mo, 1 566 813 |
| `corpus_mixte_litt.txt` | 12,23 Mo, 191 143 |

- Manifeste : [`native-corpus-multi.json`](native-corpus-multi.json).
- Répartition **équilibrée par quotas** entre sources, puis tirage déterministe (graine 0).

## Lecture

- La **diversité** est là : français, anglais, UDHR multilingue, littérature mixte.
- Les **49 999** fenêtres sont un plafond de quotas, pas 50 000 exactement (arrondi).
- Les **licences** ne sont **pas** vérifiées : le manifeste le dit.
- **Aucun entraînement** n'utilise encore ce corpus : c'est N2.7.

## Verdict

**N2.6 — diversité : atteint** (4 sources, 49 999 fenêtres). La **qualité** et les **licences** restent à
vérifier ; la **distillation** sur ce corpus n'est pas faite.

## Limites

- Quotas **équilibrés** : l'anglais, 100 Mo, est sous-représenté par rapport à son volume.
- **Fenêtres chevauchantes**.
- **Licences non vérifiées**.
- **Pas de test** de contamination entre train et validation.

## Fichiers

- Code : [`tools/corpus_natif.py`](../tools/corpus_natif.py).
- JSON : [`native-corpus-multi.json`](native-corpus-multi.json).
