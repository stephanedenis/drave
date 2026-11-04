# B13 — le défaut de la fusion : la confiance, pas le niveau

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 (repris le
> 04-11) · **Verdict** : ✅ **141/141 portes** : le **défaut de `priorite_par_niveau`** a été
> essayé (`PRIORITE_NIVEAU`) puis **rejeté** : avec le **mock**, la fusion par niveau fait tomber
> la POS de **0,7424 à 0,3432** (−0,40) et les syntagmes de 0,3165 à 0,1378. Le défaut reste la
> **confiance**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-defaut-niveau.json`](pensee-defaut-niveau.json).

## 1. Les deux défauts

| mode | POS | syntagmes F1 | tête F1 |
|---|---:|---:|---:|
| **confiance (défaut)** | **0,7424** | **0,3165** | **0,4764** |
| niveau (`PRIORITE_NIVEAU`) | 0,3432 | 0,1378 | 0,4553 |

**Ce que ça dit** :

- **Le niveau est calibré pour le neuronal réel**, pas pour le mock : `PRIORITE_NIVEAU` donne la
  POS au neuronal ; le mock la rend mal (0,34), la confiance la garde à l'heuristique (0,74).
- **Le défaut doit rester la confiance** : la fusion par niveau est une **option** du banc, pas
  le comportement par défaut — c'est ce que la mesure du mock impose.
- **Le réel tranchera** : sur l'API DeepSeek, le niveau gagnait (0,9331/0,8069/0,8704) ; sans la
  clé, on ne peut pas le vérifier — le défaut sûr est la confiance.
- **La négative est explicite** : −0,40 de POS, −0,18 de syntagmes.

## 2. Ce que ce banc ne dit pas

- **Le mock n'est pas le neuronal réel** : le rejet vaut pour le mock ; l'API pourrait renverser
  la conclusion (la fiche « quatre modes » le dit).
- **432 phrases** ; le réel donne les mêmes ordres.
- **Le neuronal réel** : la clé DeepSeek est absente de cet environnement, la mesure n'est pas
  reproductible ici.
- **Le gold 612** (432 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **le mock** : sa POS est mauvaise, ce qui pénalise le niveau par construction ;
- **le seuil** de la cascade (0,6) n'entre pas dans cette comparaison ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La clé DeepSeek** : la seule façon de trancher le défaut (niveau vs confiance) sur le réel.
2. **Le refus `r353`** : non reproductible sans l'API ; il reste ouvert.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `PRIORITE_NIVEAU`, `_fusion`.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `evaluer_bloc`.
- [`autotest.py`](../tools/pensee/autotest.py) — T138, 141/141.
- [`pensee-defaut-niveau.json`](pensee-defaut-niveau.json) — les deux modes.
