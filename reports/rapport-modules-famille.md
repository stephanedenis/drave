# C3.2b — un module de restitution par famille : l'indo-européen recopie à 100 %

> Mesure du 24/10/2026, Qwen2.5-0.5B, la famille **indo-européenne** (98 langues, 3 688 articles UDHR),
> `tools/lora_recopie.py --famille`.

## Le protocole

- **Le corpus** : `data/udhr/familles/indo-european.jsonl` (les articles de la famille), encodé par le tokenizer.
- **Le LoRA** : rang 8, **200 pas**, lr 1e-3, sur la recopie (l'invite « Recopie exactement… » → la cible = le texte).
- **La mesure** : le **taux de recopie** (le plus long préfixe exact), avant et après ; le **contrôle** (la même
  invite avec une cible différente) ; **3 textes d'évaluation jamais vus** à l'entraînement.

## Les résultats

| | la recopie | le contrôle |
|---|---:|---:|
| avant | 0,0 % | 0,0 % |
| **après** | **100,0 %** | **0,0 %** |

**La copie est acquise et le perroquet est évité.** Le module par famille recopie **exactement** le texte de sa
famille, et le contrôle (une cible différente) reste à **0 %** — ce n'est pas de la génération qui singe, c'est de la
restitution.

## Ce que ça dit, et ce que ça ne dit pas

- **Ça dit** : un module par famille **apprend la recopie exacte** de sa famille (100 %), sans le perroquet (0 %).
  C'est la première brique de C3.2 — le module qui remplace le module unique.
- **Ça ne dit pas** : que la **restitution à dix langues** est sauvée (c'est C3.2c) ; le corpus d'évaluation est de
  **3 textes** (le taux a une granularité grossière) ; le modèle est le **0,5 B** et **200 pas** seulement.
- **La réserve** : 100 % sur 3 textes n'est pas 100 % sur 3 000. Le chiffre qui compte sera celui de C3.2c : la
  **courbe** du module par famille contre la courbe de référence (30 % → 4,4 % → 0,4 % → 0,6 %).

## La suite

**C3.2c** : la même mesure avec **plus de textes**, sur les **9 familles** de 9 langues ou plus, et la comparaison à
la courbe — le module par famille **casse-t-il la chute entre 1 et 10 langues** ?
