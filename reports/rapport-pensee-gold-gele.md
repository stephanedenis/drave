# B13 — le gold gelé : les portes ne cassent plus quand le gold grandit

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **133/133 portes** : le **gold gelé** (`gold_gele.json`, **602 phrases**, la copie du
> 2026-11-02) est introduit ; les **21 portes** qui codent un nombre absolu mesurent le **gelé**,
> plus le **vivant**. C'est la troisième fois que la croissance du gold cassait dix-sept portes :
> le problème est structurel, la correction aussi.
>
> **Dispositif** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`gold_gele.json`](../tools/tests/linguistique/gold_gele.json),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-gold-gele.json`](pensee-gold-gele.json).

## 1. Le gel

| mesure | valeur |
|---|---:|
| phrases du gold gelé | **602** |
| portes basculées sur le gelé | **21** |
| portes du bloc (T0–T129) | **132** |

**Ce que ça dit** :

- **Le problème était structurel** : dix-sept portes codaient des nombres (POS 0,7502, tête
  0,4662, 587 phrases…) qui dépendent de la taille du gold ; chaque ajout les cassait.
- **La correction** : `charger_gele()` lit une **copie figée** ; les portes mesurent le gelé, le
  gold vivant peut grandir sans les casser.
- **Le gold vivant continue** : `charger()` reste pour les fiches et les mesures nouvelles ; les
  deux chemins sont explicites.
- **La leçon** : une porte doit mesurer un **comportement**, pas un **état** — ou alors un état
  **gelé**.

## 2. Ce que ce banc ne dit pas

- **Le gel doit être mis à jour** quand une porte doit suivre une nouvelle référence (manuel, à
  chaque changement de version).
- **602 phrases** : le gel du 2026-11-02.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold vivant** : 422 réels + 160 synthétiques + 20 de `gold.py`.

## 3. Ce qui pourrait rendre cette fiche fausse

- **le gel** peut diverger du vivant (c'est voulu, mais il faut le dater) ;
- **21 portes** : les autres (T0–T106) ne dépendent pas du gold ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le gold vivant** : continuer à grandir (les phrases, les liens) sans casser les portes.
2. **Le neuronal réel** : toujours bloqué ; c'est lui qui répondrait aux questions ouvertes.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `charger_gele`.
- [`gold_gele.json`](../tools/tests/linguistique/gold_gele.json) — le gel (602 phrases).
- [`autotest.py`](../tools/pensee/autotest.py) — T130, 133/133.
- [`pensee-gold-gele.json`](pensee-gold-gele.json) — le gel.
