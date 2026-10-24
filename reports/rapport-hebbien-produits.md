# A6.1 — les produits hebbiens n'ajoutent presque rien : +0,0045 de R²

> Mesure du 24/10/2026, Qwen2.5-0.5B Q4_0, **couche 6**, **504 positions**, trace DRVF v2,
> `tools/hebbien_produits.py`. Le test est celui que le rapport du capteur
> ([`rapport-capteur-hebbien.md`](rapport-capteur-hebbien.md) § 4) proposait : les produits `x_i·x_j`
> capturent-ils un espace de caractéristiques **neuf** que la trace linéaire n'a pas ?

## Le protocole

- On tient à l'écart **1/8 des neurones** (112 sur 896) et on prédit leur activation à partir des 7/8 restants.
- **(a)** régression linéaire (ridge) sur les 784 autres neurones ; **(b)** la même + **256 produits** `x_i·x_j`
  tirés au hasard.
- Coupe 80 % / 20 % par position ; R² moyen sur les neurones tenus.

## Les résultats

| régression | R² |
|---|---:|
| **linéaire seule** | **0,9214** |
| linéaire + 256 produits | 0,9259 |
| **gain des produits** | **+0,0045** |

## Ce que ça dit

- **La trace linéaire explique déjà 92 %** de l'activation des neurones tenus à l'écart : à cette couche, les
  activations sont **fortement corrélées** entre neurones — un neurone est presque une combinaison des autres.
- **Les produits n'ajoutent que +0,0045** : la piste du § 4 n'est **pas soutenue ici**. C'est le **deuxième
  négatif** de l'A6.1, après « la création de nœuds par Hebb n'ajoute rien sur 69 % des poids » — et il est
  cohérent : là où la structure linéaire explique 92 %, il reste peu à gagner.

## Ce que ça ne dit pas

- **Une seule couche** (la 6) et **un seul modèle** (0,5 B) : les couches où la trace linéaire explique moins
  (les premières, plus creuses) sont les seules où les produits pourraient payer — c'est là qu'il faudrait refaire
  le test.
- **256 produits** sur les 307 000 couples possibles : le tirage au hasard n'est pas la sélection par la trace
  hebbienne (les couples les plus **corrélés**) — la piste exacte du rapport demande le classement par `H[o][(i,j)]`.
- Le R² mesure la **reconstruction**, pas l'**utilité** : le rapport le dit déjà (§ 5) — sans une perplexité qui
  tranche, un nœud qui reconstruit n'est pas un nœud qui sert.
