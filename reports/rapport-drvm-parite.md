# N0.3b — DRVM ↔ checkpoint : 114/114 tenseurs identiques

> **Objet.** Vérifier que le DRVM exporté par `tools/native_model.py` restitue **exactement** les
> tenseurs du checkpoint PyTorch, avant de demander au moteur d'exécuter la passe avant.

## Résultat

| mesure | valeur |
|---|---:|
| tenseurs du checkpoint | **114** |
| tenseurs DRVM | **114** |
| **identiques octet-à-octet** | **114 / 114** |
| mauvais | **aucun** |

- Checkpoint : `/tmp/drave-n0-pont.pt` (11 469 192 paramètres).
- DRVM : `/tmp/drave-n0-pont.drvm`, **114 tenseurs** (pont compris).
- Chaque tenseur est comparé à `t.detach().cpu().contiguous().numpy().tobytes()`.

## Lecture

- L'export **ne perd aucun tenseur** et **ne change aucun octet** : le DRVM est un **conteneur
  fidèle** du checkpoint.
- C'est la **parité des poids**, pas la **parité de perplexité** : `drave-core` lit le DRVM
  (`--drvm-inspect`) mais n'exécute pas encore la passe avant d'un bloc DRVM.
- Le pont ajoute **4 tenseurs** (poids, biais, et deux pour la pensée) : 114 au lieu de 110.

## Verdict

**N0.3b — poids : atteint**. La **parité PPL** reste la porte suivante : elle demande que le moteur
calcule la passe avant DRVM, pas seulement qu'il lise le manifeste.

## Limites

- **Un seul modèle** (`drave-n0`, 11,47 M).
- **Aucun** test de PPL moteur.
- Le DRVM est comparé au checkpoint, pas à un GGUF équivalent.

## Fichiers

- Code : [`tools/drvm.py`](../tools/drvm.py), [`tools/native_model.py`](../tools/native_model.py).
- JSON : [`drvm-parite.json`](drvm-parite.json).
