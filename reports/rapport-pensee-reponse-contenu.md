# B13 — la réponse au contenu : 0/19, la frontière du modèle

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6 — le miroir) · **Date** : 2026-11-02
> · **Verdict** : ✅ **124/124 portes** : la **réponse au contenu** (répondre à la question, pas
> à son type) est mesurée : **0/19**. Ce n'est pas un échec de mesure, c'est la **frontière** :
> l'heuristique reconnaît l'acte, elle ne peut pas répondre au contenu. Cette sortie demande
> un **modèle** — le neuronal réel, toujours bloqué.
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-reponse-contenu.json`](pensee-reponse-contenu.json).

## 1. Les sept sorties

| sortie | source | **mesure** | nature |
|---|---|---:|---|
| surface (graphèmes) | 587 phrases | 1,0000 | contrôle |
| POS + intervalles | 587 phrases | 1,0000 | restitution |
| résumé (syntagmes) | 587 phrases | 0,7834 / 0,7472 | sémantique |
| réponse (acte) | 19 questions | 1,0000 | contrat |
| **réponse au contenu** | 19 questions | **0,0000** | **modèle** |

**Ce que ça dit** :

- **Le bloc ne répond pas** : il *reconnaît* les questions (19/19) mais ne peut pas y répondre ;
  la réponse au contenu exige un modèle de langue.
- **La frontière est nommée** : les quatre premières sorties sont **restitutives** (elles
  recopient ou classent) ; la cinquième est **générative** — et c'est celle que le mock ne
  fournit pas.
- **Le mock n'est pas un modèle** : il produit des étiquettes, pas des réponses ; le 0/19 le
  prouve, alors que le contrat (la forme) passe.
- **La mesure est honnête** : un `None` explicite vaut mieux qu'une réponse inventée.

## 2. Ce que ce banc ne dit pas

- **Ce qu'un vrai modèle ferait** : la mesure dit que le bloc actuel ne peut pas, pas que la
  tâche est impossible.
- **19 questions** seulement.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition de « répondre »** (le contenu, pas le type) ;
- **le `None`** est un choix : une heuristique pourrait tenter une réponse et échouer
  autrement — ce serait une autre mesure ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le neuronal réel** : la seule sortie qui le demande — débloquer (modèle local, poids).
2. **La réponse au contenu heuristique** : tenter une réponse par extraction (le syntagme
   sujet + le prédicat) et mesurer l'échec.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `repondre_contenu`, `fidelite_contenu`.
- [`autotest.py`](../tools/pensee/autotest.py) — T121, 124/124.
- [`pensee-reponse-contenu.json`](pensee-reponse-contenu.json) — les sept sorties.
