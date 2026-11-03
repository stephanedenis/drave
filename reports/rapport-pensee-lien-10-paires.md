# B13 — les 10 paires : 5/10, la forme inversée est la limite (r408–r412)

> **Ligne de roadmap** : **L/B13** · **Date** : 2026-11-03 · **Verdict** : ⚠️ **les 10 paires donnent
> 5/10** — le lien réparé (paire sujet+verbe) marche sur les **formes non inversées** (r418–r422 :
> **5/5**) et échoue sur les **formes inversées** (r408–r412 : **0/5**). Deux causes distinctes :
> `_sujet` ne trouve pas le pronom inversé (« mange-**t-il** ») et r408 choisit r304 « Viens-tu
> demain ? » (même verbe, plus proche) au lieu de r423. **Le critère paire ne suffit pas : il faut
> la forme.**

## 1. Les 10 paires

| question | attendu | trouvé | juste |
|---|---|---|---|
| r408 « Ne viens-tu pas demain ? » | r423 | **r304** « Viens-tu demain ? » | ❌ |
| r409 « Ne mange-t-il pas ? » | r424 | — (None) | ❌ |
| r410 « Ne dort-elle pas ? » | r425 | — (None) | ❌ |
| r411 « Ne partent-ils pas ? » | r426 | — (None) | ❌ |
| r412 « Ne lis-tu pas ? » | r427 | — (None) | ❌ |
| r418 « Tu ne viens pas demain ? » | r423 | r423 | ✅ |
| r419 « Il ne mange pas ? » | r424 | r424 | ✅ |
| r420 « Elle ne dort pas ? » | r425 | r425 | ✅ |
| r421 « Ils ne partent pas ? » | r426 | r426 | ✅ |
| r422 « You don't come tomorrow? » | r427 | r427 | ✅ |

## 2. Les deux causes

1. **Le sujet inversé** : `_sujet` cherche un `PRON` en niveau POS ; dans « Ne mange-t-il pas ? », le
   pronom est **après** le verbe (`t-il`), et l'heuristique ne le reconnaît pas → `None`.
2. **La proximité reste** : r408 trouve « Viens-tu demain ? » (r304) qui partage sujet et verbe —
   c'est une **question**, pas l'assertion attendue (r423). Le critère de paire ne distingue pas
   **assertion** et **question**.

## 3. Le contrôle négatif

- **r418–r422 (non inversées) : 5/5** — le lien réparé marche quand la forme est simple.
- **r408–r412 (inversées) : 0/5** — la limite est la **forme**, pas la proximité.
- Avant réparation, r418–r422 faisaient 2/5 : la réparation a bien servi.

## 4. Ce qui pourrait rendre ce résultat faux

- 10 paires seulement, choisies dans un même bloc du gold.
- Le juge est une égalité d'ids.
- `_sujet` est une heuristique : une vraie analyse morphosyntaxique changerait la donne.

## 5. La suite

1. **Réparer `_sujet`** pour la forme inversée (`t-il`, `elle`, `ils`) puis re-mesurer les 10.
2. Ajouter le critère **assertion ↔ question** (acte) avant la proximité.
3. **Parité DRVM/native** (cadenas 3, porte 27, labyrinthe 2) — déjà mesurée.

## 6. Fichiers

- [`pensee-lien-repare-10.json`](pensee-lien-repare-10.json) — la mesure et les limites.
- [`tools/tests/linguistique/miroir.py`](../tools/tests/linguistique/miroir.py) — `_sujet`, `_verbe`,
  `trouver_precedente`.
