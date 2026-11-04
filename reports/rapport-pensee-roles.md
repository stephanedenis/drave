# B13 — les 322 GN sans rôle : 129 avant le GV, 172 après

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **160/160 portes** : les **322 GN sans rôle** sont **301 avec un GV** ; la **position** tranche :
> **129 avant** le GV (sujet probable → `agent`), **172 après** (objet probable → `patient`).
> La règle de position rend la relation GN → GV **calculable pour 301 GN** au lieu de 221
> (0,3469 → 0,4725).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-roles.json`](pensee-roles.json).

## 1. La position

| mesure | GN | part |
|---|---:|---:|
| GN sans rôle | **322** | 100 % |
| dont avec un GV | **301** | 93,5 % |
| **avant le GV** (sujet probable) | **129** | 40,0 % |
| **après le GV** (objet probable) | **172** | 53,4 % |

| relation | avant | **après la règle de position** |
|---|---:|---:|
| GN avec rôle et un GV | 221 (0,3469) | **301 + 221 = 522 (0,8195)** |

**Ce que ça dit** :

- **La position est un signal fort** : 129 GN avant le GV (sujet), 172 après (objet) — la règle
  de position rend la relation calculable pour **301 GN de plus**.
- **Le rôle par position est une heuristique**, pas une annotation : `agent` si avant, `patient`
  si après — elle se trompera sur les passifs et les inversions (`Le chat est mangé par le
  chien`).
- **La couverture de la relation passe de 0,3469 à 0,8195** (522/637) — la moitié indécidable
  n'est plus qu'un quart.
- **La négative est explicite** : 0,8195 < 1,0 ; 115 GN restent sans rôle (les 21 sans GV et les
  cas particuliers).

## 2. Ce que ce banc ne dit pas

- **La justesse du rôle par position** n'est pas mesurée : le gold n'annote pas le rôle des 322.
- **Les passifs** : la règle se trompe (`par` + agent).
- **Le gold 432** : 432 phrases.
- **Le gold 612** (432 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la position** n'est pas le rôle : c'est une hypothèse ;
- **les passifs** sont rares dans le gold mais existent ;
- **le gold** : 432 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Mesurer la justesse** : sur un échantillon annoté à la main, la règle de position vaut-elle ?
2. **Les passifs** : détecter `par` + GN après le GV.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — les rôles du GN.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `attachement`.
- [`autotest.py`](../tools/pensee/autotest.py) — T157, 160/160.
- [`pensee-roles.json`](pensee-roles.json) — la position.
