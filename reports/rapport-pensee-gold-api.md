# Le gold neuronal sur l'API DeepSeek — mêmes verdicts, trente-cinq fois plus vite

> **Question** : le professeur **en ligne** (`deepseek-chat`) reproduit-il les verdicts du
> Qwen2.5-7B local sur les problèmes de B13, et à quel coût de latence ?

## Dispositif

- Les mesureurs B13 [`qualifier_politique_drvm.py`](../tools/tests/qualifier_politique_drvm.py) et
  [`qualifier_porte_minute_drvm.py`](../tools/tests/qualifier_porte_minute_drvm.py), avec
  `PolitiqueLLM` de [`operateurs.py`](../tools/pensee/operateurs.py) branché sur
  `https://api.deepseek.com` ;
- `--modele deepseek-chat`, `--endpoint https://api.deepseek.com`, **sans** `--demarrer` : aucun
  serveur local, aucun GPU (la règle 11 d'`AGENTS.md`) ;
- clé dans `~/.config/drave/deepseek.key` (`0600`), lue par `DEEPSEEK_KEY_FILE` ;
- cache `data/deepseek/cache`, température 0, `max_tokens` 8, 96 appels par mesure ;
- sorties séparées : [`pensee-politique-llm-api.json`](pensee-politique-llm-api.json),
  [`pensee-porte-minute-api.json`](pensee-porte-minute-api.json).

## Résultats

| mesure | 7B local (02/11) | API `deepseek-chat` (03/11) |
|---|---|---|
| porte-minute `llm_porte` | True, 26 nœuds, 7 appels, 6,404 s, score 1,0 | True, 24 nœuds, 6 appels, **5,544 s**, score 1,0 |
| porte-minute `llm_labyrinthe` | False, 200 nœuds, 95 appels, 101,615 s, score 0,25 | False, 200 nœuds, 78 appels, **2,869 s**, score 0,25 |
| politique (3 problèmes) | 0 erreur | **0 erreur**, 2,61 s |

**Le verdict est identique** : la porte-minute **discrimine** la règle (1,0) et le labyrinthe sans la
porte reste à 0,25 ; le professeur en ligne **ne fait pas mieux** que le 7B sur le labyrinthe (200
nœuds, but non atteint) — c'est le résultat attendu : la difficulté est dans la **recherche**, pas
dans le modèle.

## Contrôles négatifs

- **sans la porte** (`llm_labyrinthe`, prompt labyrinthe) : 0,25 — la mesure ne crédite pas une règle
  qu'elle n'a pas reçue ;
- **aveugle** et **hasard** restent les contrôles de la porte (inchangés) ;
- **0 erreur** sur 96 appels : une panne d'API laisserait des `erreurs > 0` ; le cas
  `deepseek-flash` l'a montré (96/96 réponses vides, score 0,25 par défaut).

## Ce qui pourrait rendre ce résultat faux

- **le changement de professeur** : les chiffres ne sont comparables qu'entre passes **API** ; le 7B
  et `deepseek-chat` ne sont pas le même modèle ;
- **la latence** dépend du réseau et de la charge de l'API — 2,9 s contre 101,6 s ici n'est pas un
  invariant ;
- **`deepseek-flash`** est un modèle à **raisonnement** : avec `max_tokens: 8` il consomme tout dans
  le raisonnement et rend un contenu **vide** ; garder `deepseek-chat` (ou augmenter `max_tokens`) ;
- **le cache** (914 entrées) : une réponse cachée peut masquer une régression de modèle — le purger
  avant une passe de référence ;
- **la clé** : sans `DEEPSEEK_KEY_FILE`, la mesure échoue proprement (0 appel, pas de faux résultat).

## Reproduire

    export DEEPSEEK_KEY_FILE=~/.config/drave/deepseek.key
    python3 tools/tests/qualifier_politique_drvm.py --endpoint https://api.deepseek.com \
        --modele deepseek-chat --sortie reports/pensee-politique-llm-api.json
    python3 tools/tests/qualifier_porte_minute_drvm.py --endpoint https://api.deepseek.com \
        --modele deepseek-chat --sortie reports/pensee-porte-minute-api.json

## Ligne de roadmap

**B13** — le professeur de référence devient `deepseek-chat` (API en ligne) ; les GPU restent
exclusivement à Drave. La fiche ne remplace pas les mesures du 7B : elle les **complète** et fixe le
professeur des passes suivantes.
