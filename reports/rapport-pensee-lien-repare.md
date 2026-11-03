# B13 — le lien réparé : la paire (sujet + verbe) avant la proximité, auto 2/5 → 5/5

> **Ligne de roadmap** : **L/B13** · **Date** : 2026-11-03 · **Verdict** : ✅ **le lien automatique
> passe de 2/5 à 5/5** sans toucher à la réponse contextuelle (5/5). Le critère de **paire** —
> même sujet **et** même verbe — passe avant la proximité ; la proximité ne sert plus que de
> **repli** quand aucun verbe ne concorde. Les distracteurs r428–r432, qui partagent le sujet mais
> pas le verbe, ne sont plus choisis.

## 1. La réparation

Dans `trouver_precedente` (`miroir.py`) :

1. on calcule le **sujet** et le **verbe** de la question ;
2. on parcourt les précédentes de la plus récente à la plus ancienne ;
3. on retient la première qui a **le même sujet ET le même verbe** (la **paire**) ;
4. à défaut, on garde en **repli** la plus récente qui a le même sujet.

## 2. Les résultats

| lecture | avant | après |
|---|---:|---:|
| **lien automatique** | 2/5 (0,40) | **5/5 (1,00)** |
| réponse contextuelle | 5/5 | 5/5 |

| question | attendu | avant | après |
|---|---|---|---|
| r418 | r423 | r423 ✅ | r423 ✅ |
| r419 | r424 | r428 ❌ | **r424 ✅** |
| r420 | r425 | r430 ❌ | **r425 ✅** |
| r421 | r426 | r431 ❌ | **r426 ✅** |
| r422 | r427 | r427 ✅ | r427 ✅ |

## 3. Le contrôle négatif

- **Avec** les distracteurs : avant 2/5, après 5/5 — c'est bien le critère de paire qui répare.
- **Sans** distracteurs : 5/5 avant comme après — le banc n'était pas le problème, le lien oui.
- Le **repli** (sujet seul) reste en place : si aucun verbe ne concorde, on ne renvoie pas `None`.

## 4. Ce qui pourrait rendre ce résultat faux

- Le verbe est le **premier VERB** de surface : une phrase à deux verbes pourrait mal apparier.
- 5 paires seulement ; les distracteurs sont **construits** pour ce piège.
- Le juge est une égalité d'ids (pas de paraphrase).

## 5. La suite

1. Étendre les paires (10, 20) et vérifier que le critère ne casse rien.
2. **Parité DRVM/native** (cadenas 3, porte 27, labyrinthe 2) — déjà mesurée.
3. Le **gold réel** reste le corpus de référence (432 phrases).

## 6. Fichiers

- [`pensee-lien-repare.json`](pensee-lien-repare.json) — la mesure et le détail.
- [`tools/tests/linguistique/miroir.py`](../tools/tests/linguistique/miroir.py) — `_verbe`,
  `trouver_precedente`.
