# B13 — le lien automatique réparé : 5/5 après le réordonnancement

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **136/136 portes** : le **lien automatique** passe de **0/5 à 5/5** après deux corrections :
> les **assertions précèdent** les questions (`r423`–`r427` avant `r418`–`r422`), et le **sujet**
> a un repli `PRON/NOUN` (les phrases courtes n'ont pas de GN — le générateur S ne sort qu'un GV).
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-lien-auto-fixe.json`](pensee-lien-auto-fixe.json).

## 1. Les deux corrections

| correction | effet |
|---|---|
| **réordonner** le gold (assertions avant questions) | le lien peut trouver une phrase **antérieure** |
| **repli `PRON/NOUN`** pour le sujet | les phrases courtes n'ont pas de GN |

| mesure | avant | **après** |
|---|---:|---:|
| lien automatique | 0/5 | **5/5** |
| contexte (index) | 5/5 | 5/5 |

**Ce que ça dit** :

- **Le lien automatique fonctionne** sur ces 5 paires : la phrase qui partage le sujet (`Tu`/`You`)
  est retrouvée sans index codé en dur.
- **Le repli `PRON/NOUN` est révélateur** : le générateur S ne produit pas de GN pour
  `Tu ne viens pas demain ?` — une lacune du segmenteur, pas du lien.
- **Le contexte devient utilisable** : le 5/5 du round 135 était un artefact d'index ; le 5/5
  d'aujourd'hui est un **lien** mesuré.
- **La frontière tient** : le lien trouve la phrase, il ne comprend pas le sens.

## 2. Ce que ce banc ne dit pas

- **5 paires** : un échantillon.
- **Le sujet** est un mot de surface (le pronom) ; un vrai lien demanderait la coréférence (la
  ligne anaphore, 103 liens).
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 607** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **le réordonnancement** a changé les index : les fiches qui citent r418–r427 restent valides
  (les ids sont stables) ;
- **le repli** sur le premier PRON/NOUN est naïf ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La coréférence comme lien** : réutiliser les 103 liens de la ligne anaphore pour trouver la
   phrase de l'antécédent, pas seulement le mot.
2. **Le neuronal réel** : toujours bloqué.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `_sujet` (repli), `trouver_precedente`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — l'ordre corrigé.
- [`autotest.py`](../tools/pensee/autotest.py) — T133, 136/136.
- [`pensee-lien-auto-fixe.json`](pensee-lien-auto-fixe.json) — le lien réparé.
