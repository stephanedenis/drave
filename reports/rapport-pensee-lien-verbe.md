# B13 — `_verbe` réparé pour l'inversion : les paires restent 5/10, le repli sujet-seul trompe

> **Ligne de roadmap** : **L/B13** · **Date** : 2026-11-03 · **Verdict** : ⚠️ **`_verbe` réparé mais
> les 10 paires restent 5/10** — « mange-t-il » donne maintenant le verbe `mange`, et pourtant
> r409 choisit **r344 « Le chat mange ; il dort. »** (sujet `il` + verbe `mange`, mais ce n'est pas
> la paire), r408 choisit r304, r410–r412 restent `None`. Le **repli sujet-seul** est devenu le
> problème : il retient une phrase qui a le sujet sans être la bonne assertion.

## 1. La réparation

Dans `_verbe` : si le token contient des tirets (« mange-t-il »), le verbe est le **premier
segment**. `_sujet` (déjà réparé au round précédent) prend le **dernier** segment.

| question | `_verbe` avant | `_verbe` après |
|---|---|---|
| « Ne mange-t-il pas ? » | None | **mange** |
| « Ne viens-tu pas demain ? » | None | **viens** |
| « Ne dort-elle pas ? » | None | **dort** |

## 2. Les résultats (inchangés)

| lecture | justes | taux |
|---|---:|---:|
| 10 paires | **5/10** | 0,50 |
| r418–r422 (non inversées) | 5/5 | 1,00 |
| r408–r412 (inversées) | 0/5 | 0,00 |

| question | trouvé | pourquoi faux |
|---|---|---|
| r408 | r304 « Viens-tu demain ? » | même sujet+verbe, mais c'est une **question**, pas l'assertion r423 |
| r409 | **r344** « Le chat mange ; il dort. » | sujet `il` + verbe `mange` — mais pas la paire |
| r410–r412 | None | aucun antécédent avec sujet **et** verbe concaténés |

## 3. Le contrôle négatif

- r418–r422 : **5/5** — les formes non inversées marchent toujours.
- r408–r412 : **0/5** — la réparation du verbe **ne change pas** le résultat : le problème est
  ailleurs (l'acte, la paire, le repli).

## 4. Conclusion

Réparer les pièces (`_sujet`, `_verbe`) ne suffit pas : **le repli sujet-seul** choisit une phrase
qui a le sujet mais pas la paire, et **rien ne distingue une assertion d'une question**. Le critère
suivant doit être l'**acte** (assertion ↔ question) avant la proximité.

## 5. La suite

1. Ajouter le critère **acte** (assertion ↔ question) dans `trouver_precedente`.
2. Re-mesurer les 10 paires.
3. **Parité DRVM/native** (cadenas 3, porte 27, labyrinthe 2).

## 6. Fichiers

- [`pensee-lien-verbe.json`](pensee-lien-verbe.json) — la mesure et le constat.
- [`tools/tests/linguistique/miroir.py`](../tools/tests/linguistique/miroir.py) — `_verbe`.
