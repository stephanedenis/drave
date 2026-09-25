# Qtrinet — « mode listes » : exécuter sans GPU

Objectif : **pas** de compresser le modèle, mais l'exécuter avec des opérations
purement structurelles (compter, décaler, additionner) — donc **sans multiplieur,
sans cœur tensoriel, sans GPU**.

Mesures sur **qwen2 Q8_0** (494.0 M poids, densité 99.2 %).

## Deux façons d'exprimer la valeur

| Mode | Principe | Décodeur |
|---|---|---|
| **unaire** | la valeur est la longueur de la suite de zéros (≤ 127) | un compteur |
| **décalage-addition** | valeur positionnelle, une addition par bit à 1 | un décalage + un compteur |

## 1. Coût par poids

| Mode | additions/poids | bits de flux/poids |
|---|---|---|
| multiplieur (référence GPU) | 0.99 | 8,00 |
| **décalage-addition (popcount)** | **3.10** | 8,00 |
| **unaire (suites de zéros)** | **42.45** | **42.45** |

➡️ L'unaire coûte **13.7× plus** d'opérations *et* de flux, pour le
même résultat exact.

## 2. Projection sur 7 G poids

| Support | 8 bits positionnel | unaire |
|---|---|---|
| 1 carte FPGA (9,66 Go/s) | 1.4 tok/s | 0.26 tok/s |
| 4 cartes FPGA | 5.5 tok/s | 1.04 tok/s |
| CPU (28,7 Go/s) | 4.1 tok/s | 0.77 tok/s |

## Verdict

1. **Oui, un modèle 8 bits peut s'exécuter en mode listes sans GPU** — et c'est
   même la bonne réponse à la contrainte « aucun DSP » du cahier des charges.
   Mais **pas sous forme unaire**.
2. **L'unaires est disqualifié par la mesure** : `E[|v|] = 42,79` pour un Q8_0,
   soit **13.7× plus d'opérations et de flux** que le décalage-addition.
   Des suites de 127 zéros, c'est 127 cycles par poids : le débit s'effondre.
3. **Le décalage-addition donne le même résultat pour 3,13 additions par poids**
   (mesuré : `E[popcount] = 3,13`). Chaque poids de 8 bits se décompose en bits,
   chaque bit à 1 déclenche une addition décalée. **Aucun multiplieur.**
4. **Le stockage ne change pas** : le modèle reste en 8 bits (ou 4, ou ternaire).
   C'est l'*exécution* qui est structurelle, pas le format. On ne paie rien en
   taille, on paie 3,13× en opérations — largement abordable sur un FPGA où 95 %
   des ALM dorment.
5. **Conséquence majeure** : la contrainte « pas de DSP » **n'exige pas** des poids
   ternaires. Le décalage-addition fonctionne pour n'importe quelle largeur
   entière. On peut donc exécuter un modèle 8 bits ou 4 bits existant, sans
   réentraînement et sans GPU.

> ⚠️ Projections sur la partie GEMM seule, à débit mémoire mesuré. Les 3,13
> additions par poids supposent un accumulateur par destination et un séquenceur
> de décalages — à valider en RTL.


---
*Généré par `run_list_mode.py` — Qtrinet.*
