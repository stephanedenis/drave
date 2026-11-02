# B13 — l'hybride : 24/30, aucune règle simple n'atteint 30/30

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **101/101 portes** : l'**hybride** (sujet par le rôle `agent`, objet par le dernier nom) est
> mesuré. Il fait **24/30** : mieux que le rôle seul (23/30), moins bien que le dernier nom seul
> (**27/30**). **Aucune règle simple n'atteint 30/30** : le gold demande le **sens du verbe**.
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore-hybride.json`](pensee-anaphore-hybride.json).

## 1. Les trois règles

| sous-ensemble | dernier nom | rôle | **hybride** |
|---|---:|---:|---:|
| r301–r336 (court) | **20/20** | 14/20 | 15/20 |
| r337–r342 (long) | 7/10 | **9/10** | **9/10** |
| **tout** | **27/30** | 23/30 | 24/30 |

**Ce que ça dit** :

- **Le dernier nom reste le meilleur** (27/30) : sur ce gold, la proximité bat le rôle.
- **L'hybride rattrape une partie du rôle** (+1 sur le total, +1 sur le court) sans perdre le
  long (9/10).
- **Aucune règle simple n'atteint 30/30** : les trois échecs restants (r321/r322/r337) exigent
  le **sens du verbe** (`voir` vs `parler`) ou une annotation sémantique.
- **La négative est explicite** : 24/30 < 27/30.

## 2. Ce que ce banc ne dit pas

- **30 liens** ; 100 donneraient une courbe.
- **Le sens du verbe** n'est pas modélisé ; c'est la limite des trois règles.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 522** (342 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la taille** (30 liens) ;
- **les rôles et les ancres** (annotation à la main) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le sens du verbe** : une table de rôles sémantiques (`voir` objet, `parler` destinataire).
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `resoudre_hybride`, `mesurer_hybride`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `coref` sur 32 phrases.
- [`autotest.py`](../tools/pensee/autotest.py) — T98, 101/101.
- [`pensee-anaphore-hybride.json`](pensee-anaphore-hybride.json) — le bilan.
