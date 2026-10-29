# N4.8 — consignes courtes : 0/40 sur des mots tenus

> **Objet.** Sortir du SFT à 24 paires : 2 000 consignes procédurales (majuscules, minuscules,
> répétition, doublement) sur **50 mots**, et 40 consignes sur **10 mots tenus à l'écart**.

## Dispositif

- Modèle : `/tmp/drave-n0-prof20k-5.pt`, PPL **2,708**, converti en SFT.
- 2 000 paires d'entraînement, **800 pas**, lr 2e-4, perte sur la réponse.
- 40 paires de validation sur des **mots jamais vus**.
- Génération greedy de 32 octets.

## Résultat

| ensemble | exactitude |
|---|---:|
| entraînement (2 000) | **mémorisé** (perte 0) |
| **mots tenus (40)** | **0/40** |

## Lecture

- Le modèle **n'apprend pas la règle** « majuscules », « minuscules », « répète » : il apprend les
  **40 mots** et leurs transformations.
- Sur un mot nouveau, **0/40**.
- Ce n'est pas un problème de format : le format `Q: … / R:` est appris.
- C'est un problème de **généralisation symbolique** : le natif ne factorise pas la consigne et le mot.

## Verdict

**N4.8 — négatif** : consignes courtes, **0/40** sur mots tenus. Le SFT mémorise, il ne généralise
pas.

## Limites

- **40** paires tenues, **10** mots.
- **800 pas**, un seul lr.
- **Pas de curriculum** mot → règle.
- **Pas de test** avec des consignes composées.

## Fichiers

- Code : [`tools/jeu_consignes.py`](../tools/jeu_consignes.py), [`tools/evaluer_consignes.py`](../tools/evaluer_consignes.py).
- JSON : [`native-consignes.json`](native-consignes.json).
