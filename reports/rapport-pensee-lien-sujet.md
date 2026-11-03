# B13 — le sujet inversé normalisé : les paires restent 5/10, le lien choisit hors paire

> **Ligne de roadmap** : **L/B13** · **Date** : 2026-11-03 · **Verdict** : ⚠️ **la normalisation du
> sujet inversé marche, mais le taux ne bouge pas** : 5/10. `_sujet` rend maintenant `tu`, `il`,
> `elle`, `ils`, `tu` pour `viens-tu`, `mange-t-il`, `dort-elle`, `partent-ils`, `lis-tu` ; et
> pourtant le lien choisit des phrases **au bon sujet et au bon verbe mais hors paire** : r408 →
> **r222** « Si tu viens, nous partirons. », r409 → **r344** « Le chat mange ; il dort. », r410 →
> **r227** « Pendant qu'il dort, elle lit. », r411 → **r354** « Marie et Paul dansent ; ils
> s'amusent. », r412 → **r270** « Quand tu veux, nous partons. ».

## 1. La réparation

`_sujet` : le sujet inversé est le **dernier** segment du token, quel que soit le nombre de
segments (`viens-tu` → `tu`, `mange-t-il` → `il`). `_verbe` prend le **premier** segment.

| question | `_sujet` | `_verbe` |
|---|---|---|
| r408 « Ne viens-tu pas demain ? » | **tu** | viens |
| r409 « Ne mange-t-il pas ? » | **il** | mange |
| r410 « Ne dort-elle pas ? » | **elle** | dort |
| r411 « Ne partent-ils pas ? » | **ils** | partent |
| r412 « Ne lis-tu pas ? » | **tu** | lis |

## 2. Les résultats (inchangés)

| lecture | justes | taux |
|---|---:|---:|
| 10 paires | **5/10** | 0,50 |
| r418–r422 (non inversées) | 5/5 | 1,00 |
| r408–r412 (inversées) | 0/5 | 0,00 |

## 3. Le nouveau diagnostic

Les 5 inversées trouvent maintenant des phrases qui **matchent sujet + verbe** — mais ce ne sont
pas **la paire** : r222 « Si tu viens… » a le sujet `tu` et le verbe `viens`, et elle est **plus
proche** que r423. Le lien prend le premier candidat qui matche, sans contrainte de **paire
thématique** (même énoncé, assertion ↔ question).

## 4. Le contrôle négatif

- r418–r422 : 5/5 — la normalisation ne casse rien.
- r408–r412 : 0/5 — la normalisation a marché (les sujets sont bons) mais le **choix** reste faux.

## 5. Ce qui pourrait rendre ce résultat faux

- Le lien n'a **aucune notion de paire thématique** : il matche sujet+verbe et prend le plus proche.
- 10 paires d'un même bloc.
- La coupe sur le dernier segment est aveugle (`lis-tu` → `tu`, correct ici).

## 6. La suite

1. **Contrainte de paire thématique** : l'antécédent doit partager plus que sujet+verbe (le
   complément, l'adverbe de temps, la structure).
2. Ou **apprendre** le lien sur les 5 paires correctes.
3. **Parité DRVM/native** (cadenas 3, porte 27, labyrinthe 2).

## 7. Fichiers

- [`pensee-lien-sujet.json`](pensee-lien-sujet.json) — la mesure et le diagnostic.
- [`tools/tests/linguistique/miroir.py`](../tools/tests/linguistique/miroir.py) — `_sujet`.
