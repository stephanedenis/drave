# B13 — la réponse contextuelle : 5/5, la phrase précédente tranche

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **134/134 portes** : la **réponse contextuelle** — la phrase précédente tranche l'accord —
> retrouve les **5/5** questions pièges : si la précédente est une assertion affirmative
> (`Tu viens demain.`), la question négative (`Tu ne viens pas demain ?`) **constate** et la
> réponse est `non` ; si elle nie, la question demande l'accord (`si`).
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-contexte.json`](pensee-contexte.json).

## 1. Les 5 paires

| question (piège) | précédente | réponse | **contextuelle** |
|---|---|---|---|
| r418 `Tu ne viens pas demain ?` | r423 `Tu viens demain.` | `non` | **non** ✅ |
| r419 `Il ne mange pas ?` | r424 `Il mange.` | `non` | **non** ✅ |
| r420 `Elle ne dort pas ?` | r425 `Elle dort.` | `non` | **non** ✅ |
| r421 `Ils ne partent pas ?` | r426 `Ils partent.` | `non` | **non** ✅ |
| r422 `You don't come tomorrow?` | r427 `You come tomorrow.` | `no` | **no** ✅ |

**Ce que ça dit** :

- **Le contexte suffit pour ces 5 cas** : la polarité de la phrase précédente (affirmative) dit
  que la question **constate**, donc `non` ; la règle du `si` seule (sans contexte) se trompait.
- **La règle est encore de surface** : elle lit la négation de la précédente, pas le sens ; une
  question rhétorique (`Tu ne viens pas ?` après une affirmation) attendrait `si` — le contexte
  ne fait que déplacer le problème.
- **5/5 vs 0/5** : c'est le **contrôle négatif** du round — sans contexte, 0/5 ; avec, 5/5.
- **La frontière n'est pas franchie** : le contexte est un signal, pas une compréhension.

## 2. Ce que ce banc ne dit pas

- **Les paires** sont construites (assertion + question) : le gold ne les lie pas par un champ ;
- **5 paires** : un échantillon ;
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 607** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **le lien question/précédente** est codé en dur (r418↔r423, …) ; un autre ordre changerait tout ;
- **la règle** (affirmative → constat) n'est pas générale ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le lien automatique** : trouver la phrase précédente par le thème (le sujet partagé), pas par
   l'index.
2. **Le neuronal réel** : toujours bloqué ; c'est lui qui trancherait le sens.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir (les portes sont gelées).

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `repondre_contextuel`, `fidelite_contextuelle`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — les 5 assertions (r423–r427).
- [`autotest.py`](../tools/pensee/autotest.py) — T131, 134/134.
- [`pensee-contexte.json`](pensee-contexte.json) — les 5 paires.
