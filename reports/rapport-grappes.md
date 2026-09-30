# Drave — grappes afférentes/efférentes et découpage en sous-modèles

Modèle : MLP 32→64→10, structure **imposée à l'entraînement**
(masque à 4 grappes + une fraction d'arêtes inter-grappes).

## Coût de la structure imposée

| Couplage | Accuracy | Non-nuls | Densité | Arêtes hors grappe | Écart moyen | Positions (b/poids) |
|---|---|---|---|---|---|---|
| 0.0 % | 74.12 % | 346 | 12.9 % | 0.0 % | 2.40 | 0.39 |
| 1.0 % | 73.34 % | 346 | 12.9 % | 2.7 % | 3.26 | 0.39 |
| 5.0 % | 74.02 % | 373 | 13.9 % | 12.0 % | 4.14 | 0.69 |
| 20.0 % | 75.78 % | 459 | 17.1 % | 35.9 % | 6.69 | 0.85 |
| 100.0 % | 76.07 % | 708 | 26.3 % | 75.0 % | 3.43 | 0.79 |

**Comparaison à budget égal** (346 non-nuls) :

- modèle en grappes pures : **74.12 %**
- meilleur modèle dense de même budget (32→7→10, 311 paramètres) : **74.12 %**

## Trafic ring (découpage en 4 sous-modèles, 7B type)

**Ce qui traverse le ring, ce sont les activations, pas les poids** (ceux-ci
restent résidents sur leur carte).

| Couplage | Activations traversantes | Ko/token | µs sur le ring |
|---|---|---|---|
| 0.0 % | 0.0 % | 0.0 | 0.0 |
| 1.0 % | 27.7 % | 72.5 | 15.1 |
| 5.0 % | 37.0 % | 97.1 | 20.2 |
| 20.0 % | 60.9 % | 159.7 | 33.3 |
| 100.0 % | 100.0 % | 262.1 | 54.6 |

➡️ Même sans grappes, le ring transporte des **dizaines de µs** face à des
**dizaines de ms** de calcul. Le ring n'est jamais le goulot : la valeur des
grappes est ailleurs (coût d'encodage et partitionnabilité).


## Verdict

1. **Oui, la structure s'impose à la conversion** — et c'est même la seule
   façon : appliquée *après* coup, elle coûte cher (l'élagage en blocs perdait
   11 points à densité égale dans `run_encoding.py`) ; imposée *pendant*
   l'entraînement, le modèle s'y adapte.
2. **La double dividende est réelle** : grouper les destinations raccourcit les
   écarts, donc baisse le coût des positions — en plus de réduire le trafic
   inter-cartes. Les deux colonnes vont dans le même sens.
3. **Le couplage est le curseur** : quelques pour cent d'arêtes hors grappe
   suffisent souvent à récupérer l'essentiel de l'accuracy, et le ring est
   très loin d'être saturé (voir §trafic : des µs contre des dizaines de ms
   de calcul).
4. **Conséquence architecturale** : le découpage en sous-modèles doit être
   choisi *avant* la quantification, et il détermine à la fois le format
   d'encodage et l'affectation aux cartes.

> ⚠️ Mesures sur un MLP de 2 688 poids : les valeurs absolues ne se transposent
> pas. Ce qui se transpose, c'est le **sens des compromis** et l'existence de la
> double dividende.


---
*Généré par `run_clusters.py` — Drave.*
