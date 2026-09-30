# Drave — harnais de test : qualité et débit variable

Modèle : **qwen2 Q8_0** · corpus : WikiText-2 test (4080 tokens évalués).

## 1. Qualité — perplexité

**PPL = 24.77** sur 4080 tokens.

Référence : un Qwen2.5-0.5B correct tourne autour de 15-25 sur WikiText-2 ;
cette valeur valide l'implémentation numpy (aucune bibliothèque ML).

## 2. Événements par couche

| Couche | Activations nulles (MLP) | Nulles (après SiLU) | Événements MLP | Événements attention |
|---|---|---|---|---|
| 0 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 1 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 2 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 3 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 4 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 5 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 6 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 7 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 8 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 9 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 10 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 11 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 12 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 13 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 14 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 15 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 16 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 17 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 18 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 19 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 20 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 21 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 22 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
| 23 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |

## 3. Débit variable

| Statistique | Événements/token |
|---|---|
| Moyenne | 354.88 M |
| Médiane (p50) | 354.88 M |
| p95 | 354.88 M |
| p99 | 354.88 M |
| Maximum | 354.88 M |
| Écart-type / moyenne | 0.0 % |

## Verdict

1. **La perplexité est le test de qualité standard le moins cher** : quelques
   centaines de kilo-octets de texte, aucun jeu de données à installer, et une
   comparaison directe avec la littérature. C'est le premier test à faire passer.
2. **Le débit variable dépend de la parcimonie des ACTIVATIONS**, pas seulement
   des poids. Or un transformer standard produit **très peu de zéros exacts** :
   SiLU et softmax sont lisses, aucune activation ne tombe exactement à zéro.
   La cascade a donc un nombre d'événements **quasi constant** — la variance
   vient des poids, pas des données.
3. **Conséquence** : si l'on veut un débit réellement variable (et les gains qui
   vont avec), il faut **imposer la parcimonie des activations** — par un seuil
   (ReLU, top-k) ou par une architecture qui la produit naturellement. C'est là
   que les modèles « impensables » en architecture dense deviennent intéressants.

> ⚠️ Mesure faite sur une seule fenêtre de tokens pour les statistiques
> d'événements (coût numpy), et sur l'ensemble du corpus pour la perplexité.


---
*Généré par `run_harness.py` — Drave.*
