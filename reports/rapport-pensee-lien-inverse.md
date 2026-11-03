# B13 — la forme inversée : `_sujet` réparé, `_verbe` reste aveugle, les 10 paires restent 5/10

> **Ligne de roadmap** : **L/B13** · **Date** : 2026-11-03 · **Verdict** : ⚠️ **la réparation de
> `_sujet` est réelle mais insuffisante** — sur les formes inversées (« Ne mange-t-il pas ? »),
> `_sujet` rend maintenant `il` (le 3ᵉ segment du token `mange-t-il`), mais **`_verbe` rend `None`**
> parce que `mange-t-il` est étiqueté **NOUN**, pas VERB. Résultat : les 10 paires restent **5/10**
> (r418–r422 5/5, r408–r412 0/5). La limite n'est plus le sujet, c'est **le verbe**.

## 1. Le diagnostic

| question | `_sujet` avant | `_sujet` après | `_verbe` |
|---|---|---|---|
| r408 « Ne viens-tu pas demain ? » | None | **viens-tu** | None |
| r409 « Ne mange-t-il pas ? » | None | **il** | None |
| r410 « Ne dort-elle pas ? » | None | **dort-elle** | None |
| r411 « Ne partent-ils pas ? » | None | **partent-ils** | None |
| r412 « Ne lis-tu pas ? » | None | **lis-tu** | None |

Trois formes sur cinq donnent encore **le mot entier** (`viens-tu`, `dort-elle`, `partent-ils`) au
lieu du pronom seul : la coupe ne marche que quand le mot a **trois** segments (`mange-t-il`).

## 2. Les résultats

| lecture | justes | taux |
|---|---:|---:|
| 10 paires (après réparation `_sujet`) | **5/10** | 0,50 |
| 10 paires (avant) | 5/10 | 0,50 |
| r418–r422 (non inversées) | 5/5 | 1,00 |
| r408–r412 (inversées) | 0/5 | 0,00 |

- r409 part sur **r389** « Le bateau tangue ; il avance. » (sujet `il`, plus proche que r424).
- r410–r412 restent `None` : aucun antécédent ne partage le sujet (mal coupé) ni le verbe.

## 3. Le contrôle négatif

- r418–r422 font **5/5** avant comme après : la réparation de `_sujet` ne casse rien.
- r408–r412 font **0/5** avant comme après : la réparation ne suffit pas — c'est le **verbe** qui
  manque, pas le sujet.

## 4. Ce qui pourrait rendre ce résultat faux

- L'heuristique découpe `mange-t-il` en **un** token ; un vrai segmenteur en ferait trois.
- 10 paires d'un même bloc.
- Le repli sujet-seul peut choisir une phrase sans le bon verbe (r409 → r389).

## 5. La suite

1. **Réparer `_verbe`** pour la forme inversée (chercher le verbe dans le premier segment du token
   `mange-t-il`, ou dans l'étiquette `GV`).
2. Ajouter le critère **assertion ↔ question** (acte) avant le repli.
3. **Parité DRVM/native** (cadenas 3, porte 27, labyrinthe 2) — déjà mesurée.

## 6. Fichiers

- [`pensee-lien-inverse.json`](pensee-lien-inverse.json) — la mesure et le diagnostic.
- [`tools/tests/linguistique/miroir.py`](../tools/tests/linguistique/miroir.py) — `_sujet`, `_verbe`.
