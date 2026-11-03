# B13 — la parité DRVM/native : 114/114 poids, 5/5 prompts, rejouable mais checkpoint volatil

> **Ligne de roadmap** : **L/B13** · **Date** : 2026-11-03 · **Verdict** : ✅ **la parité est
> mesurée et documentée** — 114/114 tenseurs identiques octet-à-octet (poids) et 5/5 prompts avec
> un écart maximal de 0,00006 (logits). Les deux bancs sont **rejouables en CPU**, mais leur
> checkpoint vit dans `/tmp` et a été **nettoyé** : il faut le régénérer avant tout rejeu.

## 1. Les deux parités

| mesure | valeur | fiche |
|---|---:|---|
| tenseurs du checkpoint | 114 | [`rapport-drvm-parite.md`](rapport-drvm-parite.md) |
| identiques octet-à-octet | **114 / 114** | idem |
| prompts comparés | 5 | [`rapport-native-parite.md`](rapport-native-parite.md) |
| top-1 / top-5 | **5/5 / 5/5** | idem |
| écart max | **0,00006** | idem |

- **Poids** : le DRVM est un **conteneur fidèle** du checkpoint (aucun octet changé).
- **Logits** : le Rust natif et Python donnent le **même top-1/top-5** sur cinq prompts ; l'écart
  est compatible avec l'ordre des additions f32.

## 2. La rejouabilité (mesurée ce soir)

- `tools/verifier_parite_native.py` s'exécute avec `PYTHONPATH=.` et `~/gpu-env/bin/python`
  (torch présent).
- Il échoue **uniquement** sur `FileNotFoundError: /tmp/drave-n0-pont.pt` — le checkpoint a été
  nettoyé.
- Pour rejouer : régénérer le checkpoint (`tools/entrainer_native.py`) et le DRVM
  (`tools/applique_pont.py`), **CPU**, ~11,5 M paramètres, **aucun GPU de N2**.

## 3. Le contrôle négatif

- Les poids sont comparés **octet-à-octet** : aucune perte, aucun arrondi.
- Les logits sont comparés sur des prompts **fixes** (pas de tirage aléatoire).
- **Aucune mesure GPU** : N2 est resté intact, la parité est CPU.

## 4. Ce qui pourrait rendre ce résultat faux

- Le checkpoint en `/tmp` est **volatile** : la fiche décrit un état qui n'est plus sur disque.
- 5 prompts fixes : la parité n'est **pas** une garantie de perplexité.
- `drave-core` lit le DRVM mais **n'exécute pas** encore la passe avant d'un bloc DRVM : c'est la
  parité des **poids** et des **logits**, pas de la passe avant complète.

## 5. La suite

1. **Régénérer** le checkpoint + DRVM en CPU et rejouer les deux bancs (fait reproductible).
2. **Exécuter** la passe avant DRVM dans `drave-core` (la parité manquante).
3. Gold réel 432 (déjà fait) et le lien (plafond 5/10, documenté).

## 6. Fichiers

- [`pensee-parite-drvm-native.json`](pensee-parite-drvm-native.json) — l'état et la rejouabilité.
- [`tools/verifier_parite_native.py`](../tools/verifier_parite_native.py) — le banc.
- [`reports/rapport-drvm-parite.md`](rapport-drvm-parite.md),
  [`reports/rapport-native-parite.md`](rapport-native-parite.md) — les fiches d'origine.
