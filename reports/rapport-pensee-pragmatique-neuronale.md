# B13 — la pragmatique neuronale : 1,0 / 1,0 / 0,98 / 0,98 sur 130 phrases

> **Ligne de roadmap** : **B13** (moteur de pensée, règles 6 et 11) · **Date** : 2026-11-04 ·
> **Verdict** : ✅ **151/151 portes** : la **pragmatique neuronale** est branchée sur le composite
> (`NeuronalLLMPragmatique` → `NeuronalLLMCompose`) et mesurée sur les **130 premières phrases**
> du gold 432 : **acte 1,0**, **négation 1,0**, **modalité 0,9846**, **double sens 0,9769**. La
> sortie que le composite ne rendait pas (acte 0,0) est maintenant **la meilleure**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-pragmatique-130.json`](pensee-pragmatique-130.json).

## 1. Les 130 phrases

| mesure | valeur |
|---|---:|
| POS | 0,9677 |
| syntagmes F1 | 0,8795 |
| tête F1 | 0,9202 |
| **acte** | **1,0000** |
| **négation** | **1,0000** |
| **modalité** | 0,9846 |
| **double sens** | 0,9769 |

**Ce que ça dit** :

- **Le composite rend enfin la pragmatique** : le tagger dédié (grammaire GBNF à quatre champs)
  donne l'acte à 1,0 — l'heuristique faisait 0,9954, le composite nu faisait 0,0.
- **La négation est parfaite** (1,0) : les négations explicites du gold sont toutes trouvées.
- **La modalité et le double sens** sont à 0,98 : deux cas perdus sur 130, à regarder.
- **La POS monte aussi** (0,9677 contre 0,9389 sur 432) : les 130 premières phrases sont plus
  faciles (le début du gold), pas un effet du pragma.
- **La négative est explicite** : 2 erreurs sur 130, pas zéro.

## 2. Ce que ce banc ne dit pas

- **130 phrases** : un échantillon du gold 432 ; la passe complète est en cours
  (`pensee-quatre-modes-432-pragma.json`).
- **Le coût** : 3 taggers par phrase (POS, chunks, pragma) — 390 appels pour 130 phrases.
- **Le tagger pragma** utilise la grammaire GBNF : le JSON est contraint, pas vérifié après coup.
- **Le gold 612** (432 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **l'échantillon** : les 130 premières phrases sont plus simples que les 302 suivantes ;
- **la modalité** : 0,9846 peut baisser sur le gold complet ;
- **le double sens** : la règle de l'heuristique (les mots doubles) pourrait diverger ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La passe complète** : le pragma sur les 432 (en cours).
2. **Les 2 erreurs** : les nommer (la modalité et le double sens).
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `NeuronalLLMCompose(pragma=...)`.
- [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py) — le pragma branché.
- [`autotest.py`](../tools/pensee/autotest.py) — T148, 151/151.
- [`pensee-pragmatique-130.json`](pensee-pragmatique-130.json) — les 130 phrases.
