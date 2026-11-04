# B13 — la relation GN → GV : 221 sur 637 (0,3469)

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **159/159 portes** : la **relation GN → GV** (le rôle du GN et la présence d'un GV) est mesurée
> sur le gold 432 : **637 GN**, dont **221** portent un rôle `agent`/`patient`/`destinataire`
> **et** ont un GV dans la phrase (**0,3469**). Les **322** GN restants sont des « groupe
> nominal » sans rôle — la relation ne peut pas être posée.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-relation.json`](pensee-relation.json).

## 1. Les rôles

| rôle | GN | part |
|---|---:|---:|
| **agent** | **260** | 40,8 % |
| **patient** | **55** | 8,6 % |
| **groupe nominal** (sans rôle) | **322** | 50,6 % |
| **tout** | **637** | 100 % |

| mesure | valeur |
|---|---:|
| GN avec rôle agent/patient/destinataire et un GV | **221** |
| taux | **0,3469** |

**Ce que ça dit** :

- **La moitié des GN n'ont pas de rôle** (322) : le segmenteur les déclare « groupe nominal »
  sans dire s'ils sont agent ou patient — la relation GN → GV est **indécidable** pour eux.
- **Les rôles posés sont fiables** : 260 agents + 55 patients ; la relation est calculable pour
  221 GN (0,3469).
- **La relation est une autre mesure que la cible** : la cible attache un segment à un autre
  segment (239 cas) ; la relation dit le **rôle** du GN (315 cas). Les deux se complètent.
- **La négative est explicite** : 0,3469 < 1,0 ; la moitié des GN restent sans rôle.

## 2. Ce que ce banc ne dit pas

- **Les 322 sans rôle** : leur rôle n'est pas annoté dans le gold ; le segmenteur ne le devine pas.
- **Le gold 432** : 432 phrases.
- **La relation inverse** (GV → GN) n'est pas mesurée.
- **Le gold 612** (432 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **le rôle** est une étiquette du segmenteur, pas du gold ;
- **le gold** : 432 phrases ;
- **la définition de la relation** (rôle + GV) est un choix ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Annoter le rôle des 322** : le levier de la relation, comme les cibles pour l'attachement.
2. **La relation inverse** : le GV → ses GN (sujet, objet).
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — les rôles du GN.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `attachement`.
- [`autotest.py`](../tools/pensee/autotest.py) — T156, 159/159.
- [`pensee-relation.json`](pensee-relation.json) — les rôles.
