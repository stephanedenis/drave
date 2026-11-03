# B13 — un seul GV : les juxtapositions tombent, les paires restent 5/10

> **Ligne de roadmap** : **L/B13** · **Date** : 2026-11-03 · **Verdict** : ⚠️ **la contrainte
> « un seul GV » (pas de `;`) écarte bien r344/r390/r354, mais le taux reste 5/10** — le lien prend
> maintenant **n'importe quelle phrase simple** au bon sujet+verbe : r409 → **r306** « Il ne vient
> pas. », r410 → **r308** « Marie lit. Elle aime les livres. », r411 → **r190** « Ils arrivent
> demain. ». La limite n'est plus la forme : c'est l'**absence de paire thématique**.

## 1. La contrainte ajoutée

`_simple(a)` renvoie **False** si le texte contient `;` (juxtaposition = deux propositions).
C'est ce qui écarte r344 « Le chat mange ; il dort. », r390 « La cloche sonne ; elle appelle. »,
r354 « Marie et Paul dansent ; ils s'amusent. ».

## 2. Les résultats

| lecture | justes | taux |
|---|---:|---:|
| 10 paires (un seul GV) | **5/10** | 0,50 |
| r418–r422 (non inversées) | 5/5 | 1,00 |
| r408–r412 (inversées) | 0/5 | 0,00 |

| question | trouvé | pourquoi |
|---|---|---|
| r408 | — | aucun candidat simple |
| r409 | **r306** « Il ne vient pas. » | sujet+verbe ok, mais pas la paire |
| r410 | **r308** « Marie lit. Elle aime les livres. » | sujet `elle` + verbe `lit`… autre énoncé |
| r411 | **r190** « Ils arrivent demain. » | sujet+verbe ok, mais pas la paire |
| r412 | — | aucun candidat |

## 3. Le contrôle négatif

- r418–r422 : 5/5 — les contraintes ne cassent rien.
- Les juxtapositions sont bien écartées : la contrainte **fonctionne**.
- Mais **toute** phrase simple au bon sujet+verbe est acceptée : la surface ne suffit pas.

## 4. Conclusion

Chaque contrainte de forme (sujet normalisé, verbe, acte, phrase simple, un seul GV) améliore le
**diagnostic** sans améliorer le **taux** : les 5 paires correctes ne sont pas identifiables par la
seule surface, parce que d'autres phrases partagent sujet+verbe. Il faut soit une contrainte
**thématique** (le complément, l'adverbe de temps), soit **apprendre** le lien sur les 5 paires.

## 5. La suite

1. **Contrainte thématique** : partager aussi le complément ou l'adverbe de temps.
2. Ou **apprendre** le lien (5 exemples positifs).
3. **Parité DRVM/native** (cadenas 3, porte 27, labyrinthe 2).

## 6. Fichiers

- [`pensee-lien-gv.json`](pensee-lien-gv.json) — la mesure et le constat.
- [`tools/tests/linguistique/miroir.py`](../tools/tests/linguistique/miroir.py) — `_simple`.
