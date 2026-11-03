# B13 — la contrainte thématique : cinq contraintes de forme, toujours 5/10

> **Ligne de roadmap** : **L/B13** · **Date** : 2026-11-03 · **Verdict** : ⚠️ **la contrainte
> thématique (adverbe hors négation) ne restaure pas les paires : 5/10**. Après le sujet normalisé,
> le verbe, l'acte, la phrase simple et le GV unique, le lien de surface **plafonne**. r408 tombe à
> `None`, r409 → r306 « Il ne vient pas. », r410 → r308, r411 → r013 « Ils ont acheté une maison. ».

## 1. La contrainte ajoutée

`_adverbes(a)` : adverbes **hors négation** (le complément thématique). La question et l'antécédent
doivent partager le même ensemble (`demain` rapproche r408 de r423, pas r306).

## 2. Les résultats (inchangés)

| lecture | justes | taux |
|---|---:|---:|
| 10 paires (thématique) | **5/10** | 0,50 |
| r418–r422 (non inversées) | 5/5 | 1,00 |
| r408–r412 (inversées) | 0/5 | 0,00 |

## 3. Le constat final

**Cinq contraintes de forme** — sujet normalisé, verbe, acte (question→assertion), phrase simple,
GV unique, adverbe thématique — **n'ont pas suffi**. Les 5 paires correctes ne sont pas
identifiables par la surface, parce que d'autres phrases partagent sujet, verbe et adverbe.

Le lien de surface **plafonne à 5/10** sur ce gold. Ce n'est pas un bug du banc : c'est la limite de
l'approche « forme + proximité ».

## 4. Le contrôle négatif

- r418–r422 : 5/5 — les contraintes ne cassent rien.
- r408–r412 : 0/5 — chaque contrainte a amélioré le **diagnostic** (r344, r390, r354, r222 écartés)
  sans améliorer le **taux**.

## 5. La suite

1. **Apprendre** le lien sur les 5 paires (positif) et les distracteurs (négatif).
2. Contrainte de **similarité de contenu** (vecteurs) entre question et antécédent.
3. Ou **documenter** que le lien de surface plafonne à 5/10 et passer à la parité DRVM/native.

## 6. Fichiers

- [`pensee-lien-thematique.json`](pensee-lien-thematique.json) — la mesure et le constat final.
- [`tools/tests/linguistique/miroir.py`](../tools/tests/linguistique/miroir.py) — `_adverbes`,
  `trouver_precedente`.
