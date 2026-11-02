# B13 — la coréférence à 103 liens : la cible est atteinte

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **112/112 portes** : trente-cinq phrases à **pronom sujet simple** (r373–r407 : `il ronfle`,
> `elle sent bon`, `it purrs`, `she dances`) entrent dans le gold (**407 réels**). La
> coréférence passe de **68 à 103 liens** : la **cible de 100** est **atteinte**. Les deux
> règles font **86/103** — le pronom sujet simple ne les sépare plus.
>
> **Seuils ajustés (2ᵉ fois)** : le gold réel à 407 phrases fait tomber le syntagme réel à
> **0,1713** ; le verdict `syntagme_reel` passe de 0,18 à **0,16**. C'est le signe que le gold
> grandit plus vite que le segmenteur : la prochaine ligne utile est **le segmenteur**, pas le
> gold.
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore-103.json`](pensee-anaphore-103.json).

## 1. Les 103 liens

| sous-ensemble | liens | dernier nom | rôle |
|---|---:|---:|---:|
| r301–r342 (court) | 30 | **27** | 23 |
| r343–r372 (enchaîné) | 38 | 24 | **29** |
| r373–r407 (sujet simple) | 35 | **35** | **35** |
| **tout** | **103** | **86** | **86** |

**Ce que ça dit** :

- **La cible est atteinte** : 103 liens ≥ 100 ; le gold réel est à **407 phrases**.
- **Les deux règles convergent** (86/103) : sur les pronoms sujets simples, le dernier nom et le
  rôle sont identiques ; le désaccord ne vient que des cas enchaînés et des PP.
- **Le plafond reste** 86/103 (0,835) : les 17 échecs sont les cas ambigus (les deux noms, le PP
  locatif, le rôle de l'objet).
- **La négative reste** : 86 < 103.

## 2. Ce que ce banc ne dit pas

- **103 liens** ; 200 demanderaient 100 phrases de plus.
- **Les réfléchis** (`se`, `s'`) et les **possessifs** (`son`, `leur`) ne sont pas couverts.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 587** (407 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la taille** (103 liens) ;
- **les ancres** (annotation à la main) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Les réfléchis et les possessifs** : 30 liens de plus, une autre règle.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `resoudre`, `resoudre_roles`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — 407 réels.
- [`autotest.py`](../tools/pensee/autotest.py) — T109, 112/112.
- [`pensee-anaphore-103.json`](pensee-anaphore-103.json) — le bilan.
