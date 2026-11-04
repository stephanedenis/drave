# B13 — les quatre modes sur le gold 432 : le niveau gagne avec le réel

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6 et règle 11) · **Date** : 2026-11-04 ·
> **Verdict** : ✅ **143/143 portes** : les **six modes** du contrat de L sont mesurés sur le
> **gold réel 432**, avec le **neuronal réel** (l'API DeepSeek, `deepseek-chat`, température 0).
> Le **niveau** (`PRIORITE_NIVEAU`) gagne : POS **0,9309**, syntagmes **0,8226**, tête **0,8784**,
> et garde la pragmatique de l'heuristique (**0,9954**). Le **mock** avait conclu l'inverse :
> le défaut par défaut reste la confiance **faute de clé dans les portes**, pas par choix.
>
> **Dispositif** : [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py),
> [`pensee-quatre-modes-432.json`](pensee-quatre-modes-432.json),
> [`autotest.py`](../tools/pensee/autotest.py).

## 1. Les six modes (432 phrases, API réelle)

| mode | POS | syntagmes F1 | tête F1 | acte |
|---|---:|---:|---:|---:|
| heuristique | 0,7394 | 0,2520 | 0,4511 | **0,9954** |
| neuronal (compose) | **0,9309** | **0,8226** | **0,8784** | 0,0000 |
| parallèle (confiance) | 0,9280 | 0,8020 | 0,8570 | 0,9954 |
| cascade (confiance) | 0,9280 | 0,8020 | 0,8570 | 0,9954 |
| **parallèle_niveau** | **0,9309** | **0,8226** | **0,8784** | 0,9954 |
| **cascade_niveau** | **0,9309** | **0,8226** | **0,8784** | 0,9954 |

**Ce que ça dit** :

- **Le niveau gagne avec le réel** : POS **0,9309** (+0,19 sur l'heuristique), syntagmes
  **0,8226** (+0,57), tête **0,8784** (+0,43) — et la **pragmatique** reste celle de
  l'heuristique (0,9954) parce que le neuronal ne la rend pas (acte 0,0).
- **Le neuronal seul ne suffit pas** : son acte est **0,0** ; la fusion par niveau lui prend la
  POS et les syntagmes, et laisse la pragmatique à l'heuristique.
- **Le mock avait conclu l'inverse** (0,3432 pour le niveau) : le défaut ne peut pas être changé
  sans la clé — c'est pourquoi il reste la confiance **dans les portes**, et le banc utilise
  l'option `PRIORITE_NIVEAU`.
- **Le coût est mesuré** : **858 appels API**, **254 341 tokens**, **803,8 s** de latence
  cumulée pour la passe complète.

## 2. Les seuils et le refus

| seuil | valeur |
|---|---|
| heuristique, neuronal, cascade, `_niveau` | ✅ |
| **parallèle** (confiance) | ❌ 0,928 < 0,9299 |
| **aucun_refus** | ❌ **1 refus** |

**Le refus `r353`** : `Le professeur parle ; les élèves l'écoutent.` — le neuronal rend **7 POS
pour 6 tokens** (`ValueError: longueur POS 7 / 6`) : le tokenizer du bloc coupe `l'écoutent` en
**deux** (`l'` + `écoutent`), le modèle en rend **un**. Le refus est **nommé** ; le correctif
(tokeniser l'élision comme le bloc) est la prochaine action.

## 3. Ce qui pourrait rendre ce résultat faux

- **Une seule passe API** (température 0) : la variance du modèle n'est pas mesurée.
- **Le gold 432** : les seuils sont ceux du banc.
- **`PRIORITE_NIVEAU` est une décision** calibrée sur cette passe : une autre passe pourrait
  déplacer les niveaux.
- **Le refus `r353`** : un cas, pas une classe.

## 4. La suite

1. **Le correctif `r353`** : aligner la tokenisation de l'élision sur celle du bloc.
2. **Le défaut** : si une deuxième passe confirme, `PRIORITE_NIVEAU` peut devenir le défaut des
   portes — mais la clé doit être présente.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py) — les six modes.
- [`pensee-quatre-modes-432.json`](pensee-quatre-modes-432.json) — les mesures, le coût, le refus.
- [`autotest.py`](../tools/pensee/autotest.py) — T139, T140, 143/143.
