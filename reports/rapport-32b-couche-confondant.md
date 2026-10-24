# Le 32 B : le pont à 0,49 — et le confondant de la couche relative

> Mesures du 24/10/2026, XNLI (2 490 paires FR/EN, 747 en test), la **couche 18** (le défaut des outils), la sonde
> linéaire, le contrôle par étiquettes mélangées. Le 32 B est chargé en **nf4** (le fp16 ne tient pas sur 2 × 16 Go) ;
> les autres en fp16.

## Les résultats

| modèle | couches | profondeur de la couche 18 | **sonde FR** | **pont EN→FR** | contrôle |
|---|---:|---:|---:|---:|---:|
| 1,5 B | 28 | **64 %** | 0,6921 | 0,8300 | 0,325 |
| 3 B | 36 | 50 % | 0,5020 | 0,5920 | 0,327 |
| 14 B | 48 | 37 % | 0,4810 | 0,6270 | 0,318 |
| **32 B (nf4)** | 64 | **28 %** | **0,4096** | **0,4900** | 0,333 |
| hasard | — | — | 0,333 | — | — |

À première vue : la sonde et le pont **décroissent avec la taille**, et le 32 B est le plus bas (0,41 / 0,49).

## Le confondant, avant la conclusion

**La couche 18 n'est pas la même couche d'un modèle à l'autre.** Sa profondeur relative tombe de **64 %** (1,5 B) à
**28 %** (32 B) : au 1,5 B c'est une couche tardive — là où les sondes lisent traditionnellement le mieux —, au 32 B
c'est une couche précoce. La comparaison « à couche 18 fixe » mesure donc **deux choses à la fois** : la taille et la
profondeur relative.

Conséquences, écrites avant toute conclusion :

- **la décroissance n'est pas attribuable à la taille** par ce protocole : elle peut être l'effet de la couche ;
- **le résultat du 1,5 B (« il bat les gros ») est du même ordre** : il est lu à 64 % de profondeur, les autres à
  50 %, 37 % et 28 % — la comparaison est confondue ;
- le 32 B ajoute un second confondant : le **nf4** (les autres sont en fp16) — la quantification peut coûter une part
  des 0,41 (la mesure ne l'isole pas).

## Ce qu'il faut mesurer pour trancher

**À profondeur relative fixe** — la moitié du réseau : la couche **14** (1,5 B), **18** (3 B), **24** (14 B),
**32** (32 B). L'extraction du 32 B prend ~2-3 h par couche (le 4 bits) : elle est en file. En attendant, la seule
conclusion honnête est celle-ci :

> *Le protocole « couche 18 » ne compare pas des couches comparables ; la carte du raisonnement naturel, du 1,5 B au
> 32 B, n'est pas encore tracée.*

## Premier point à profondeur relative fixe — et il complique la règle

Le 1,5 B à la couche **14** (50 % de sa profondeur) :

| couche | profondeur | sonde FR | pont EN→FR |
|---|---:|---:|---:|
| 14 | 50 % | **0,5783** | **0,7028** |
| 18 | 64 % | 0,6921 | 0,8300 |

**La couche relative ne suffit pas** : à 50 % de profondeur, le 1,5 B lit *moins* bien qu'à 64 %. Chaque modèle a
donc **sa** meilleure couche, et la comparaison honnête doit fixer la profondeur relative **et** rapporter que la
couche choisie n'est pas la meilleure de chaque modèle. Le 32 B à la couche 32 (50 %) tourne ; le 14 B à la
couche 24 suivra.

## Ce que ça ne dit pas, et ce que ça ne retire pas

- Les résultats **synthétiques** (mesures 125-158) sont à couche fixe **par modèle** et avec la même relation : ils
  ne souffrent pas de ce confondant — la carte du raisonnement synthétique tient.
- Le 32 B **lit quand même** : 0,41 contre 0,33 de hasard et un contrôle au hasard — la contradiction est dans
  l'état, faiblement, à la couche 18 ; les couches 32-48 diront si elle y est plus lisible.
- Le pont du 32 B reste **au-dessus du hasard** (0,49 contre 0,33), mais il est le plus faible des quatre : si la
  profondeur ne l'explique pas, c'est un résultat sur l'alignement à grande échelle — pas encore le cas.
