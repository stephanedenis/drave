# B13 — la confirmation (run 2) : refus 0, le niveau gagne encore

> **Ligne de roadmap** : **B13** (moteur de pensée, règles 6 et 11) · **Date** : 2026-11-04 ·
> **Verdict** : ✅ **145/145 portes** : la passe API est **rejouée** sur le gold 432 après le
> correctif d'élision. **Aucun refus** (`aucun_refus: True`), le `r353` passe, et le **niveau
> gagne encore** : POS **0,9389** (+0,008), syntagmes **0,8241**, tête **0,8797**, acte 0,9954.
> Le réel confirme le réel.
>
> **Dispositif** : [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py),
> [`pensee-quatre-modes-432-run2.json`](pensee-quatre-modes-432-run2.json),
> [`autotest.py`](../tools/pensee/autotest.py).

## 1. Run 1 contre run 2

| mode | POS (run 1) | **POS (run 2)** | syntagmes | tête | acte |
|---|---:|---:|---:|---:|---:|
| heuristique | 0,7394 | **0,7444** | 0,2520 | 0,4511 | 0,9954 |
| neuronal | 0,9309 | **0,9389** | 0,8241 | 0,8797 | 0,0000 |
| parallèle | 0,9280 | 0,9326 | 0,8029 | 0,8571 | 0,9954 |
| cascade | 0,9280 | 0,9326 | 0,8029 | 0,8571 | 0,9954 |
| **parallele_niveau** | 0,9309 | **0,9389** | **0,8241** | **0,8797** | 0,9954 |
| **cascade_niveau** | 0,9309 | **0,9389** | **0,8241** | **0,8797** | 0,9954 |

**Ce que ça dit** :

- **Le refus `r353` est tombé** : `refus 0`, `aucun_refus: True` — l'élision séparée aligne la
  tokenisation du bloc sur celle du modèle (la cause était bien là).
- **Le niveau gagne encore** (0,9389) et le gain est **stable** (run 1 : 0,9309) : ce n'est pas
  un accident d'une passe.
- **La pragmatique reste à l'heuristique** (0,9954) : le neuronal seul la perd (acte 0,0) ;
  c'est la **raison d'être de la fusion par niveau**.
- **Le coût est stable** : 858 appels, 254 454 tokens, 807,6 s de latence.

## 2. Ce que ce banc ne dit pas

- **Deux passes** (température 0) : la variance du modèle n'est pas mesurée au-delà.
- **Le seuil `parallele`** (0,9326 < 0,9299) : il échoue encore — le seuil est peut-être à
  réviser, ou le mode `parallele` (confiance) est intrinsèquement sous le niveau.
- **Le gold 432** : les seuils sont ceux du banc.
- **Le défaut `PRIORITE_NIVEAU`** n'est pas encore basculé : les portes utilisent le mock.

## 3. Ce qui pourrait rendre cette fiche fausse

- **une seule graine d'API** (température 0) ;
- **le gold** : 432 phrases ;
- **le `r353`** : un cas, mais la cause (l'élision) est générale ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le défaut `PRIORITE_NIVEAU`** : les deux passes convergent ; il peut devenir le défaut des
   portes **quand la clé est présente** (sinon la confiance).
2. **Le seuil du `parallele`** : le réviser ou le documenter.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py) — les six modes.
- [`pensee-quatre-modes-432-run2.json`](pensee-quatre-modes-432-run2.json) — la passe 2 (brute).
- [`autotest.py`](../tools/pensee/autotest.py) — T142, 145/145.
