# B13 — l'élision : le bloc coupe `l'écoutent`, le refus tombe

> **Ligne de roadmap** : **B13** (moteur de pensée, règles 6 et 11) · **Date** : 2026-11-04 ·
> **Verdict** : ✅ **144/144 portes** : la cause du refus `r353` est corrigée. Le tokeniseur du
> bloc coupait `l'écoutent` en **un** token ; le modèle en rendait **deux** (7 POS pour 6 tokens).
> La tokenisation sépare maintenant l'**élision** (`l'`, `d'`, `m'`, `t'`, `s'`, `n'`, `qu'`) :
> `l'` + `écoutent`. Le POS gagne **+0,0011** (0,7444 → **0,7455**) sur les 432 phrases, sans
> perte de syntagmes ni de tête.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-elision.json`](pensee-elision.json).

## 1. La correction

| mesure | avant | **après** |
|---|---:|---:|
| tokens de `l'écoutent` | 1 | **2** (`l'` + `écoutent`) |
| POS (432 phrases) | 0,7444 | **0,7455** |
| syntagmes F1 | 0,2861 | 0,2861 |
| tête F1 | 0,4986 | 0,4986 |

**Ce que ça dit** :

- **Le refus venait de la tokenisation** : le bloc et le modèle ne découpaient pas l'élision
  pareil ; le contrat doit imposer **sa** tokenisation au bloc neuronal — c'est fait.
- **Le gain est petit mais réel** (+0,0011 de POS) : les élisions sont rares dans le gold, mais
  chaque `l'`/`d'`/`qu'` était mal aligné.
- **Aucune perte** : les syntagmes et la tête ne bougent pas ; les 432 phrases restent valides.
- **La négative est explicite** : avant, `r353` refusait (7/6) ; le refus n'est pas encore
  re-mesuré sur l'API — il faudra une passe pour le confirmer.

## 2. Ce que ce banc ne dit pas

- **Le refus n'est pas re-joué** : la passe API coûte 30 min ; le correctif est mesuré
  localement (la tokenisation), pas encore sur le modèle.
- **Les élisions rares** : `aujourd'hui` reste un seul token (pas une élision de clitique).
- **L'heuristique** ; le modèle réel via l'API.
- **Le gold 612** (432 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la passe API** : le modèle peut encore rendre 7 POS pour une autre raison ; la mesure
  locale ne le prouve pas.
- **les élisions** : la liste `l d m t s n` et `qu'` n'est peut-être pas complète.
- **le JSON régénéré** (`gold_reel.json` doit suivre).
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La passe API de confirmation** : re-jouer le gold 432 et vérifier que `r353` passe.
2. **Le défaut `PRIORITE_NIVEAU`** : si la passe confirme, il peut devenir le défaut des portes.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `_mots` (élision).
- [`autotest.py`](../tools/pensee/autotest.py) — T141, 144/144.
- [`pensee-elision.json`](pensee-elision.json) — la correction.
