# N4.6 — SFT minimal : 24/24 vus, 0/4 tenus

> **Objet.** Tester si `drave-n0` peut apprendre un **format instruction** sur 24 paires, et
> généraliser à quatre paires tenues à l'écart.

## Dispositif

- Modèle : `/tmp/drave-n0-prof20k-5.pt`, PPL validation **2,708**.
- 24 paires `Q: … / R: …` (capitales, arithmétique, vocabulaire, faits).
- **500 pas**, lot 4, lr 1e-4, perte uniquement sur la réponse.
- Génération greedy de 16 octets après `Q: …\nR:`.

## Résultat

| ensemble | exactitude |
|---|---:|
| **paires vues** (24) | **24/24** |
| **paires tenues** (4) | **0/4** |

- Perte d'entraînement : **0,0000** dès 300 pas.
- Détails : [`native-sft-eval.json`](native-sft-eval.json).

## Lecture

- Le modèle **mémorise parfaitement** les 24 réponses : c'est un **format**, pas un alignement.
- Sur les quatre paires **jamais vues**, **0/4** : aucune généralisation.
- Le SFT de 500 pas **surapprend** ; il faudrait des milliers de paires et une régularisation.
- **Ce n'est pas un assistant** : c'est un perroquet de 24 phrases.

## Verdict

**N4.6 — mémorisation : atteinte** ; **alignement minimal : non**. Le format est appris, le sens
n'est pas transféré.

## Limites

- **24 paires**, un seul format.
- **4 tenues** seulement.
- **Pas de température**, greedy.
- **Pas de données externes**.

## Fichiers

- Code : [`tools/sft_natif.py`](../tools/sft_natif.py), [`tools/evaluer_sft.py`](../tools/evaluer_sft.py).
- Données : `data/instructions_fr.jsonl` (non versionné).
- JSON : [`native-sft-eval.json`](native-sft-eval.json).
