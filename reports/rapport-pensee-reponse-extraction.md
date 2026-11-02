# B13 — la réponse par extraction : 19/19, mais ce n'est pas une réponse

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **125/125 portes** : l'**extraction** (le premier GN de la phrase, à défaut le GV) trouve une
> réponse pour **19/19** questions. Mais c'est une **fausse victoire** : l'extraction rend le
> sujet, pas la réponse. Le 19/19 mesure que l'heuristique **trouve un GN**, pas qu'elle répond.
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-reponse-extraction.json`](pensee-reponse-extraction.json).

## 1. Les sorties

| sortie | source | **mesure** | nature |
|---|---|---:|---|
| surface | 587 phrases | 1,0000 | contrôle |
| POS + spans | 587 phrases | 1,0000 | restitution |
| résumé | 587 phrases | 0,7834 / 0,7472 | sémantique |
| réponse (acte) | 19 questions | 1,0000 | contrat |
| réponse au contenu | 19 questions | 0,0000 | modèle |
| **extraction (GN)** | **19 questions** | **1,0000** | **fausse victoire** |

**Ce que ça dit** :

- **L'extraction trouve toujours un GN** (19/19) : il y a toujours un syntagme nominal dans une
  question ; ce n'est pas la réponse, c'est le **sujet**.
- **La mesure est trompeuse** : 19/19 dirait « parfait » ; la fiche dit « le 19/19 mesure la
  présence d'un GN, pas la correction ». C'est le **contrôle négatif** du round.
- **La frontière du modèle tient** : l'extraction ne remplace pas la réponse au contenu (0/19).
- **Deux 1,0 qui ne veulent pas dire la même chose** : celui de l'acte est un contrat, celui de
  l'extraction est un artefact.

## 2. Ce que ce banc ne dit pas

- **La correction des réponses** (le contenu juste) n'est pas mesurée : aucune réponse n'est
  jugée, seulement extraite.
- **19 questions** ; le réel donne les mêmes ordres.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition de l'extraction** (le premier GN, pas la réponse) ;
- **le 19/19** est un plafond de forme, pas de sens ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le jugement des réponses** : un juge (humain ou modèle) pour mesurer la correction — la
   seule mesure qui compte.
2. **Le neuronal réel** : toujours bloqué ; c'est lui qui répondrait.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `repondre_extraction`, `fidelite_extraction`.
- [`autotest.py`](../tools/pensee/autotest.py) — T122, 125/125.
- [`pensee-reponse-extraction.json`](pensee-reponse-extraction.json) — les sorties.
