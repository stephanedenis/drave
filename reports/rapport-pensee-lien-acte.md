# B13 — le critère acte : les 10 paires restent 5/10, la normalisation du sujet inversé manque

> **Ligne de roadmap** : **L/B13** · **Date** : 2026-11-03 · **Verdict** : ⚠️ **le critère acte est
> posé (question → assertion) mais le taux ne bouge pas** : 5/10. r408 bascule de r304 à `None`
> (« viens-tu » ≠ « Tu »), r409 garde r344, r410–r412 restent `None`. La limite est désormais la
> **normalisation morphologique du sujet inversé**, pas la logique du lien.

## 1. Le critère ajouté

`trouver_precedente` : quand la question est de type **question**, l'antécédent doit être une
**assertion** (jamais une autre question). C'est ce qui écarte r304 « Viens-tu demain ? » pour r408.

## 2. Le diagnostic

| question | sujet trouvé | sujet attendu | acte |
|---|---|---|---|
| r408 « Ne viens-tu pas demain ? » | **viens-tu** | Tu | question |
| r409 « Ne mange-t-il pas ? » | **il** | Il | question |
| r410 « Ne dort-elle pas ? » | **dort-elle** | Elle | question |
| r411 « Ne partent-ils pas ? » | **partent-ils** | Ils | question |
| r412 « Ne lis-tu pas ? » | **lis-tu** | You | question |

Quatre sujets sur cinq ne sont **pas normalisés** : `_sujet` rend le **mot entier** au lieu du
pronom. Seul r409 (« mange-t-il » → `il`) est coupé correctement.

## 3. Les résultats

| lecture | justes | taux |
|---|---:|---:|
| 10 paires (critère acte) | **5/10** | 0,50 |
| r418–r422 (non inversées) | 5/5 | 1,00 |
| r408–r412 (inversées) | 0/5 | 0,00 |

## 4. Le contrôle négatif

- r418–r422 : 5/5 — le critère acte ne casse rien.
- r408 : passe de r304 à `None` — le critère **écarte** la mauvaise question, mais ne trouve pas la
  bonne assertion, faute de sujet normalisé.
- r409 : garde r344 — le sujet `il` et le verbe `mange` matchent, mais ce n'est pas la paire.

## 5. Ce qui pourrait rendre ce résultat faux

- La coupe du token inversé ne marche qu'à 3 segments (`mange-t-il`) ; `viens-tu` n'en a que 2.
- 10 paires d'un même bloc.
- Le repli sujet-seul peut encore choisir une phrase sans la bonne paire.

## 6. La suite

1. **Normaliser le sujet** : (`viens-tu` → `tu`, `dort-elle` → `elle`) — coupe sur le **dernier**
   segment quel que soit le nombre de segments, avec table de pronoms.
2. Re-mesurer les 10 paires.
3. **Parité DRVM/native** (cadenas 3, porte 27, labyrinthe 2).

## 7. Fichiers

- [`pensee-lien-acte.json`](pensee-lien-acte.json) — la mesure et le diagnostic.
- [`tools/tests/linguistique/miroir.py`](../tools/tests/linguistique/miroir.py) — `_acte`,
  `trouver_precedente`.
