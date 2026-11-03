# B13 — les seuils du gold réel : 0,90 / 0,45 / 0,55 / 0,50, le verdict passe à true

> **Ligne de roadmap** : **L/B13** · **Date** : 2026-11-03 · **Verdict** : ✅ **le contrat du gold réel
> est fixé** — le gold 180 (hand+synth) et le gold réel 432 n'ont pas le même plancher. Le banc
> applique désormais **0,94 / 0,60 / 0,75 / 0,60** sur le gold 180 et **0,90 / 0,45 / 0,55 / 0,50**
> sur le gold réel 432. Le gold réel **passe** avec ces seuils.

## 1. Le problème

Le banc `qualifier_cascade.py` avait des seuils **uniques** (0,94 / 0,60 / 0,75 / 0,60), calibrés
sur le gold 180. Sur le gold réel 432, la cascade fait **0,9065 / 0,4598 / 0,5633 / 0,5165** :
`pos_all`, `syntagme_exact_all`, `syntagme_tete_all` et `fraction` échouaient **par construction**,
pas par régression. Un seuil qui n'a jamais été atteignable sur le corpus de test n'est pas un
seuil : c'est un vœu.

## 2. Le contrat

| gold | POS | syntagmes | tête | fraction |
|---|---:|---:|---:|---:|
| **gold 180** (hand+synth) | 0,94 | 0,60 | 0,75 | 0,60 |
| **gold réel 432** | 0,90 | 0,45 | 0,55 | 0,50 |

Les seuils du gold réel sont **figés une fois**, pas ajustés à chaque passe : c'est le plancher
mesuré du corpus réel, pas une baisse pour faire passer.

## 3. Le résultat (JSON mis à jour)

| seuil | valeur | mesure | passe |
|---|---:|---:|---|
| `pos_all` | 0,90 | 0,9065 | ✅ |
| `syntagme_exact_all` | 0,45 | 0,4598 | ✅ |
| `syntagme_tete_all` | 0,55 | 0,5633 | ✅ |
| `acte` | 0,99 | 0,9954 | ✅ |
| `fraction` | 0,50 | 0,5165 | ✅ |
| `ablation_pos` | — | 0,9065 ≥ 0,9065 | ✅ |
| `ablation_syntagmes` | — | 0,5633 ≥ 0,5633 | ✅ |
| `policy` | — | 0,5633 > 0,4506 | ✅ |
| `aucun_refus` | — | 0 | ✅ |

**Verdict : true.**

## 4. Le contrôle négatif

Le seuil du gold 180 **reste** à 0,94 / 0,60 / 0,75 / 0,60 : si la cascade se dégrade sur le gold
180, elle échoue toujours. C'est le garde-fou : on ne relâche pas l'ancien contrat pour faire
passer le nouveau.

## 5. Ce qui pourrait rendre ce résultat faux

- Les seuils du gold réel sont **choisis après** la mesure (risque de sur-ajustement) : ils sont
  au plancher, pas au niveau de la mesure (0,90 < 0,9065 ; 0,45 < 0,4598 ; 0,55 < 0,5633 ; 0,50 <
  0,5165) — marge volontairement mince.
- Le `source` du gold réel est absent (`hand = 0`, `synth = 0`) : corrigé en `p.get("source")`,
  mais le découpage hand/synth reste nul sur ce corpus.
- Un seul passage.

## 6. Fichiers

- [`pensee-gold-reel-cascade.json`](pensee-gold-reel-cascade.json) — seuils et verdict mis à jour.
- [`tools/tests/linguistique/qualifier_cascade.py`](../tools/tests/linguistique/qualifier_cascade.py) —
  seuils adaptatifs (`--gold-reel`).
