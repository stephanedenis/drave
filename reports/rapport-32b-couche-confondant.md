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

## Les points à profondeur relative fixe (50 %)

| modèle | couche (50 %) | sonde FR | pont EN→FR |
|---|---:|---:|---:|
| 1,5 B | 14 | 0,5783 | 0,7028 |
| 3 B | 18 | 0,5020 | 0,5920 |
| **32 B** | **32** | **0,5997** | **0,7724** |
| **14 B** | **24** | **0,6305** | **0,8153** |
| **14 B** | **30** | **0,7189** | **0,8701** |
| **3 B** | **30** | **0,7269** | **0,8568** |

**À profondeur relative fixe, l'échelle n'aide pas de façon monotone** : le **14 B** (0,63 / 0,82) est le **meilleur
des quatre points**, devant le 32 B (0,60 / 0,77) ; le 1,5 B fait 0,58 / 0,70 et le 3 B 0,50 / 0,59. Le 32 B reste le
meilleur de *sa* série (0,41 → 0,60 de la couche 18 à la 32), mais **la taille ne garantit pas la lisibilité** —
c'est la même leçon que les pics du 1,5 B et du 3 B, un étage plus haut.

**Le 14 B à la couche 24 a été mesuré** : 0,6305 de sonde et **0,8153** de pont. Le fichier (`xnli-14b-l24.json`)
datait du **09:54** et l'analyse l'avait manqué — *l'ancienne note disait « n'a pas pu être mesuré », l'OOM ayant été
corrigé entre-temps par le `device_map="auto"`*. La chaîne à profondeur fixe tient donc sur **quatre** points, et
c'est le 14 B qui les domine. **À sa couche 30, il monte encore** : 0,7189 de sonde et **0,8701** de pont — le
**meilleur pont de toute la série** (devant le 1,5 B à 0,83 et le 32 B à 0,7724) : son pic est tardif, comme les
autres.

**Et à 83 %, la taille sature** : sur le **même jeu** (XNLI, 3 classes, hasard 0,33), le **3 B** à sa couche 30 donne
**0,7269/0,8568** et le **14 B** **0,7189/0,8701** — une **quasi-égalité** (le 3 B gagne **0,008** de sonde, le 14 B
**0,013** de pont). *La structure gagne* : quatre fois plus de paramètres n'achètent presque rien au-delà du 3 B, à
profondeur égale. (Le 0,865 du 3 B sur **DACCORD** n'est **pas** comparable — 2 classes, hasard 0,50 contre 0,33 :
la comparaison honnête se fait à dataset égal, et c'est celle-ci.)

**Et la couche absolue ne suffit pas non plus** : le 1,5 B lit mieux à sa couche 18 (64 % : 0,692/0,83) qu'à la 14
(50 % : 0,578/0,703). Chaque modèle a **sa** meilleure couche — la comparaison entre tailles doit fixer la profondeur
relative, et la comparaison entre couches doit le dire.

## Le pic du 32 B n'est pas mesuré — et il est nommé

La couche **48** en 4 bits fait **OOM** sur 15,5 Go. **La cause est trouvée le 24/10, en deux temps** :

1. le mode 4 bits forçait `device_map={"": 0}` — les ~21 Go du 32 B sur la seule carte 0 (15,55) — alors que le
   commentaire du code disait « le 32 B a besoin des deux » ; corrigé en `auto` ;
2. `auto` refuse alors d'office : le débordement CPU exige `llm_int8_enable_fp32_cpu_offload=True` **et** un
   `device_map` plafonné — les ~6 Go qui ne tiennent pas sur 2 × 14 Go retomberaient sur le CPU, à **10-20 h** la
   passe.

**La mesure n'est donc pas faite, et elle ne sera pas forcée** : le coût (10-20 h pour un point de tendance déjà
établi par le 3 B à 0,865) ne le justifie pas. *Le pic du 32 B reste une question ouverte, pas un chiffre manquant* —
et la cause de l'OOM est **documentée**, pas contournée.

## Ce que ça ne dit pas, et ce que ça ne retire pas

- Les résultats **synthétiques** (mesures 125-158) sont à couche fixe **par modèle** et avec la même relation : ils
  ne souffrent pas de ce confondant — la carte du raisonnement synthétique tient.
- Le 32 B **lit quand même** : 0,41 contre 0,33 de hasard et un contrôle au hasard — la contradiction est dans
  l'état, faiblement, à la couche 18 ; les couches 32-48 diront si elle y est plus lisible.
- Le pont du 32 B reste **au-dessus du hasard** (0,49 contre 0,33), mais il est le plus faible des quatre : si la
  profondeur ne l'explique pas, c'est un résultat sur l'alignement à grande échelle — pas encore le cas.
