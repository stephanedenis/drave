# N4 — la grammaticalité du « 100 M » : moins de GV, plus de ciment, un banc piégé par la boucle

> **Ligne de roadmap** : **N4** (l'usage du natif) · **Date** : 2026-11-18 · **Modèle mesuré** :
> `work/n2ac/mix1024-100m.pt` (**73,37 M** paramètres réels, 3 000 pas, PPL val **4,014**) ·
> **Référence** : `work/n2ac/mix1024-60k.pt` (**34,30 M**, 30 000 pas, PPL **2,404**) ·
> **Verdict** : en greedy, à 128 octets (protocole du 34 M), le 100 M **perd les GV** (1,45
> contre 6,90) et **monte le ciment** (0,661 contre 0,335) ; à 64 octets (contrôle de longueur),
> le même écart tient (1,10 contre 3,35 ; 0,693 contre 0,427). Mais **42 %** des GV du 34 M sont le seul token
> « a » et **46 %** des mots du 100 M sont « de » : GV et ciment mesurent surtout la **classe du
> token de boucle**. Le 100 M est **plus répétitif et moins divers** ; il n'est pas démontré
> « moins grammatical ». Le fichier fait **73,37 M** et **3 000 pas** (10× moins que le 34 M) :
> la comparaison d'échelle est confondue avec l'entraînement.

## 1. Le dispositif

Le banc existant a deux étages, et il faut les distinguer :

1. [`tools/banc_generation.py`](../tools/banc_generation.py) génère **20 prompts fixes**, trois
   réglages (greedy ; top-40/0,8 ; top-20/0,5), avec le vocabulaire de référence de 50 000 formes.
2. [`tools/banc_grammaticalite.py`](../tools/banc_grammaticalite.py) passe ces générations dans
   `bloc_linguistique.Heuristique` et agrège GV, GN, mots, ciment (part des DET/PREP/CONJ/PRON/
   AUX/PONCT), attachements et `sans_verbe` (la part des textes sans GV).

**Aucune modification de code n'a été nécessaire.** `banc_grammaticalite.py` ne charge pas de
modèle : il lit un JSON de générations. C'est `banc_generation.py` qui charge le modèle, et il a
déjà `--device`. La consigne « ajouter `--device` » ne s'appliquait donc pas ici ; on a utilisé
`--device cuda:0` à l'étage de génération. Le GPU 0 était libre au lancement (1 MiB, 0 %) ; un
autre entraînement l'a occupé ensuite, mais la mesure était finie.

**Deux longueurs, parce que la question de la longueur est réelle.** Le protocole du 34 M est à
**128 octets** ; c'est la comparaison historique. Le 100 M a aussi été mesuré à **64 octets**,
longueur du banc apparié du 100 M, pour voir si l'écart tient. Les deux sont donnés séparément.

Les commandes exactes :

```bash
# 1. génération du 100 M, 20 prompts, 128 octets, GPU
/home/stephane/gpu-env/bin/python tools/banc_generation.py \
    --modele work/n2ac/mix1024-100m.pt --n 128 --device cuda:0 \
    --sortie /tmp/banc-generation-100m-128o.json

# 2. contrôle 34 M aléatoire à 128 octets (le contrôle du protocole de référence)
#    -> reports/banc-generation-aleatoire.json (déjà publié)

# 3. grammaticalité, 100 M à 128 octets, contrôle 34 M à 128 octets
/home/stephane/gpu-env/bin/python tools/banc_grammaticalite.py \
    --entree /tmp/banc-generation-100m-128o.json \
    --controle reports/banc-generation-aleatoire.json \
    --sortie /tmp/banc-grammaticalite-100m-128o-controle34.json

# 4. grammaticalité, 100 M à 64 octets, contrôle 34 M à 64 octets (apparié)
/home/stephane/gpu-env/bin/python tools/banc_grammaticalite.py \
    --entree reports/banc-generation-100m.json \
    --controle reports/banc-generation-alea-64o.json \
    --sortie /tmp/banc-grammaticalite-100m-64o.json

# 5. contrôle scale-matched : 100 M aléatoire à 128 octets, graine 1234
/home/stephane/gpu-env/bin/python tools/banc_generation.py \
    --modele work/n2ac/mix1024-100m.pt --aleatoire --n 128 \
    --sortie /tmp/banc-generation-alea-100m-128o.json

/home/stephane/gpu-env/bin/python tools/banc_grammaticalite.py \
    --entree /tmp/banc-generation-100m-128o.json \
    --controle /tmp/banc-generation-alea-100m-128o.json \
    --sortie /tmp/banc-grammaticalite-100m-controle-100m.json
```

Le JSON [`banc-grammaticalite-100m.json`](banc-grammaticalite-100m.json) fusionne ces passes en
trois clés : `n128` (100 M + contrôle 34 M à 128 octets), `n64` (100 M + contrôle 34 M à
64 octets) et `controle_100m_n128` (le contrôle scale-matched 100 M à 128 octets).

**Référence 34 M.** Le JSON `reports/banc-grammaticalite.json` (34 M, 128 octets, contrôle 34 M
aléatoire) a été reproduit à l'identique :

```bash
/home/stephane/gpu-env/bin/python tools/banc_grammaticalite.py \
    --entree reports/banc-generation.json \
    --controle reports/banc-generation-aleatoire.json \
    --sortie /tmp/banc-grammaticalite-34m-128o.json
diff /tmp/banc-grammaticalite-34m-128o.json reports/banc-grammaticalite.json  # identique
```

Le 34 M à 64 octets a été mesuré de la même façon :

```bash
/home/stephane/gpu-env/bin/python tools/banc_grammaticalite.py \
    --entree reports/banc-generation-34m-64o.json \
    --controle reports/banc-generation-alea-64o.json \
    --sortie /tmp/banc-grammaticalite-34m-64o.json
```

**Appariement.** Mêmes 20 prompts, mêmes trois réglages, même vocabulaire de 50 000 formes, même
analyseur. Le greedy est déterministe : on a vérifié que les 20 préfixes 64 octets du 100 M sont
identiques dans la génération 128 octets (20/20), et que les 20 préfixes 64 octets du 34 M (GPU)
sont identiques à la référence 128 octets (CPU) (20/20). L'échantillonnage, lui, n'est pas
graine-fixé dans `banc_generation.py` : les lignes top-40 et top-20 sont **un tirage**.

## 2. À 128 octets : le protocole du 34 M

| modèle | réglage | GV | GN | mots | ciment | attaches | sans GV | GV/100 mots |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **34 M** | greedy | **6,90** | 2,85 | 44,8 | **0,335** | 0,737 | 0,15 | **15,4** |
| **34 M** | top-40/0,8 | 6,35 | 3,15 | 35,2 | 0,377 | 0,887 | 0,00 | 18,0 |
| **34 M** | top-20/0,5 | 5,85 | 3,15 | 38,5 | 0,310 | 0,789 | 0,00 | 15,2 |
| **100 M** | greedy | **1,45** | 1,55 | 35,2 | **0,661** | 0,905 | **0,40** | **4,1** |
| **100 M** | top-40/0,8 | 4,00 | 1,85 | 27,7 | 0,375 | 0,771 | 0,00 | 14,4 |
| **100 M** | top-20/0,5 | 2,65 | 1,90 | 32,0 | 0,461 | 0,871 | 0,00 | 8,3 |

**Lecture immédiate.** En greedy, le 100 M perd **5,45 GV** par texte (6,90 → 1,45), **1,30 GN**
et **9,6 mots** ; 8 textes sur 20 n'ont **aucun GV** contre 3 sur 20 pour le 34 M. Son ciment
**double** (0,335 → 0,661). En top-40, la chute de GV est plus faible (−2,35) et le ciment est
identique (0,375 contre 0,377) ; en top-20, la chute est de −3,20 et le ciment monte de +0,151.
Le 100 M n'est donc pas uniformément « moins structuré » : c'est le **greedy** qui s'effondre,
et le top-40 qui résiste le mieux.

**Normalisation.** Les longueurs diffèrent (35,2 mots pour le 100 M greedy contre 44,8 pour le
34 M), et un GV se compte par texte. La colonne GV/100 mots retire cet effet : 15,4 → 4,1 en
greedy, 18,0 → 14,4 en top-40, 15,2 → 8,3 en top-20. La conclusion tient.

## 3. À 64 octets : le contrôle de longueur

| modèle | réglage | GV | GN | mots | ciment | GV/100 | ratio GV/100 au hasard |
|---|---|---:|---:|---:|---:|---:|---:|
| **34 M** | greedy | 3,35 | 2,25 | 24,6 | 0,427 | 13,6 | **4,3×** |
| **34 M** | top-40 | 3,10 | 2,40 | 15,8 | 0,343 | 19,6 | **4,7×** |
| **34 M** | top-20 | 3,40 | 2,30 | 20,3 | 0,342 | 16,7 | **4,0×** |
| **100 M** | greedy | 1,10 | 1,30 | 19,9 | 0,693 | 5,5 | **1,8×** |
| **100 M** | top-40 | 2,15 | 1,95 | 15,1 | 0,375 | 14,2 | **3,4×** |
| **100 M** | top-20 | 1,60 | 1,80 | 17,4 | 0,471 | 9,2 | **2,2×** |
| contrôle 34 M aléatoire | greedy | 1,50 | 1,75 | 47,5 | 0,790 | 3,2 | 1,0 |
| contrôle 34 M aléatoire | top-40 | 2,05 | 2,10 | 48,6 | 0,795 | 4,2 | 1,0 |
| contrôle 34 M aléatoire | top-20 | 2,15 | 2,00 | 51,6 | 0,819 | 4,2 | 1,0 |

*Le hasard est le 34 M aléatoire (seul contrôle n=64 disponible) ; le 100 M aléatoire n'a été
mesuré qu'à 128 octets.*

**L'écart tient.** À 64 octets, le 34 M garde **3,35 GV** (13,6 GV/100) et le 100 M tombe à
**1,10** (5,5 GV/100) ; le ciment passe de 0,427 à 0,693. La chute 6,90 → 1,45 n'est donc pas
un artefact de longueur : à longueur divisée par deux, les deux modèles perdent des GV, mais le
rapport 34 M / 100 M reste de **2,5×** en GV/100 (contre 3,8× à 128 octets).

**Longueur, modèle ou analyseur ?** Les trois, et c'est le point méthodologique :

- **La longueur** explique la baisse des valeurs absolues (6,90 → 3,35 pour le 34 M ; 1,45 →
  1,10 pour le 100 M), pas la direction de l'écart. Le GV/100 ne rend pas les deux modèles
  comparables pour autant, parce que le prompt est inclus dans le texte analysé : à 64 octets,
  le prompt pèse une plus grande part, ce qui remonte le ciment des deux côtés (34 M 0,335 →
  0,427 ; 100 M 0,661 → 0,693).
- **Le modèle** : le 100 M produit moins de mots par texte (19,9 contre 24,6 à 64 octets) et
  les concentre sur un token, « de ». Le 34 M boucle sur des tokens courts, dont « a », qui
  porte l'essentiel de ses GV. La classe du token de boucle change le compte de GV (voir §5).
- **L'analyseur** : il construit un GV autour de « a » (pourtant étiqueté `PREP`) et un GP
  autour de « de ». Il **amplifie** la différence de classe du token de boucle.

**Conséquence.** La baisse 6,9 → 1,45 n'est **pas** attribuable à une seule cause. Elle est
réelle sur les métriques du banc, mais elle ne mesure pas proprement « la grammaire » : elle
mesure la rencontre d'un token de boucle, d'un analyseur et d'une longueur.

## 4. Les contrôles

| contrôle | n | réglage | GV | mots | ciment | GV/100 |
|---|---:|---|---:|---:|---:|---:|
| 34 M aléatoire | 128 | greedy | 2,30 | 62,5 | 0,791 | 3,7 |
| 34 M aléatoire | 128 | top-40 | 3,35 | 87,8 | 0,801 | 3,8 |
| 34 M aléatoire | 128 | top-20 | 4,00 | 89,6 | 0,796 | 4,5 |
| **100 M aléatoire** | 128 | greedy | **4,75** | 90,4 | 0,763 | **5,3** |
| **100 M aléatoire** | 128 | top-40 | **5,25** | 105,1 | 0,816 | **5,0** |
| **100 M aléatoire** | 128 | top-20 | **3,85** | 87,4 | 0,795 | **4,4** |
| 34 M aléatoire | 64 | greedy | 1,50 | 47,5 | 0,790 | 3,2 |
| 34 M aléatoire | 64 | top-40 | 2,05 | 48,6 | 0,795 | 4,2 |
| 34 M aléatoire | 64 | top-20 | 2,15 | 51,6 | 0,819 | 4,2 |

**Ratios natif / hasard (GV/100) :**

| longueur | modèle | greedy | top-40 | top-20 |
|---|---|---:|---:|---:|
| 128 octets | 34 M | **4,2×** | **4,7×** | **3,4×** |
| 128 octets | 100 M | **0,8×** | 2,9× | 1,9× |
| 64 octets | 34 M | **4,3×** | **4,7×** | **4,0×** |
| 64 octets | 100 M | **1,8×** | 3,4× | 2,2× |

*Lecture des contrôles : à 128 octets, chaque modèle est comparé à son propre aléatoire (34 M
pour le 34 M, 100 M pour le 100 M) ; à 64 octets, les deux sont comparés au 34 M aléatoire,
seul contrôle n=64 disponible. Sources : `reports/banc-grammaticalite.json` (34 M, 128),
`controle_100m_n128` (100 M, 128), `n64.aleatoire` (34 M, 64).*

**Ce que le contrôle dit.** Le 34 M est **3,4 à 4,7× au-dessus de son bruit**, stable d'une
longueur à l'autre. Le 100 M greedy est **au plancher** (0,8× de son propre hasard à 128 octets ;
1,8× du hasard 34 M à 64 octets : selon la longueur et le contrôle, il passe juste sous ou juste
au-dessus du hasard). En top-40 et top-20, il
garde un signal (1,9–3,4×), mais plus faible que le 34 M. Le 100 M n'est donc pas du bruit pur
en échantillonnage ; en greedy, il n'est pas distinguable du hasard par ce banc.

**Le ciment du hasard.** Les contrôles ont un ciment **plus élevé** que les modèles
(0,76–0,82 contre 0,31–0,69). Le ciment n'est pas un score de grammaticalité : le texte
aléatoire, décodé en fragments, produit beaucoup de tokens courts qui ressemblent à des classes
fermées. Les modèles sont **sous** ce plancher, et le 100 M s'en approche parce qu'il boucle sur
« de ». Il faut lire le ciment avec la **diversité** des classes fermées, pas seul.

## 5. Ce que le banc compte vraiment : la classe du token de boucle

C'est la découverte de cette mesure, et elle change la lecture du tableau §2.

**Côté 34 M.** Le total des GV sur les 20 textes greedy est de **138**. Le GV le plus fréquent est
**« a » seul : 58 occurrences (42 %)**, puis « de » (6), « d » (5), « A » (3), « A Ba » (3),
« a a » (3), « est » (2), « a da » (2), « a e e » (2). Les GV du 34 M sont donc massivement des
**runs de « a »**, le plus souvent le verbe avoir sans accent, que l'analyseur étiquette `PREP`
mais autour duquel il construit quand même un GV (rôle `prédicat`). Le texte « La science » en
donne 39 GV, dont une trentaine de « a » ou « a a a… ».

**Côté 100 M.** Le total des GV greedy est de **29**. Le plus fréquent est « est » (3), puis
« ss » (3), « mise » (2), « est un pays », « landes », « es », « se mise », « était », « jouent »,
« a décidé late »… Les GV sont **plus rares mais plus variés**. Et le token de boucle est
« de » : **304 des 661 mots générés (46 %)**, soit **65 % des classes fermées** ; « lande »
suit avec 86 occurrences (13 %). Le texte n'est pas une phrase, c'est une chaîne de « de ».

**Conséquence.** GV et ciment sont **anti-corrélés par la classe du token de boucle** : une
boucle sur un verbe (« a ») gonfle les GV et baisse le ciment ; une boucle sur une préposition
(« de ») fait l'inverse. Le banc ne mesure donc pas proprement la syntaxe ; il mesure aussi
**quelle classe de mot le modèle répète**. Un test de sensibilité avec l'étiquetage du même
analyseur le confirme : 20 des 29 GV du 100 M contiennent un token `VERB`/`AUX`, contre 16 des
138 du 34 M — mais l'analyseur étiquetant « a » `PREP`, ce test est indicatif, pas décisif.

**Ce qui reste robuste.** Indépendamment de la classe du token, le 100 M est **plus répétitif et
moins divers** :

| modèle | réglage | mot dominant | part | types générés | GV | ciment |
|---|---|---|---:|---:|---:|---:|
| 34 M | greedy | « 1 » | 18,4 % | 149 | 6,90 | 0,335 |
| 34 M | top-40 | « 1 » | 3,2 % | 345 | 6,35 | 0,377 |
| 34 M | top-20 | « 20 » | 7,5 % | 261 | 5,85 | 0,310 |
| **100 M** | greedy | « de » | **46,0 %** | **74** | 1,45 | 0,661 |
| **100 M** | top-40 | « de » | 9,5 % | 289 | 4,00 | 0,375 |
| **100 M** | top-20 | « de » | 24,4 % | 248 | 2,65 | 0,461 |

Le 100 M a **deux fois moins de types** en greedy (74 contre 149) et un mot dominant qui pèse
**46 %** contre **18 %**. C'est un diagnostic de **dégénérescence**, pas de grammaticalité.

## 6. Le lexique ne voit pas la chute

| modèle | réglage | mots valides | distinct-2 | répétition |
|---|---|---:|---:|---:|
| 34 M | greedy | 0,870 | 0,726 | 15 |
| 100 M | greedy | **0,878** | 0,652 | **6** |
| 34 M | top-40 | 0,490 | 1,000 | 1 |
| 100 M | top-40 | **0,551** | 1,000 | 1 |
| 34 M | top-20 | **0,735** | 0,981 | 1 |
| 100 M | top-20 | 0,673 | 0,960 | 2 |

Le banc lexical dit que le 100 M est **comparable ou meilleur** en greedy et top-40 (et qu'il
répète moins : 6 contre 15), tandis que le banc de grammaticalité dit qu'il a **près de cinq fois
moins de GV** (6,90 / 1,45 = 4,76). Les deux axes ne mesurent pas la même chose : en greedy, les
mots valides sont saturés dès 34 M, la structure non. C'est exactement la raison d'être du
second banc — mais la §5 interdit de lire la différence de GV comme une pure perte de syntaxe.

## 7. Le modèle mesuré n'est pas un « 100 M » entraîné

C'est la limite la plus lourde, et elle était invisible dans le nom du fichier :

| | 34 M (`mix1024-60k.pt`) | « 100 M » (`mix1024-100m.pt`) |
|---|---:|---:|
| paramètres réels | 34 301 224 | **73 366 568** |
| pas d'entraînement | 30 000 | **3 000** |
| PPL validation | **2,404** | **4,014** |
| perte finale | 1,025 | 1,467 |
| durée | 13 331 s | 880 s |
| `d_model` / `expert_hidden` | 384 / 512 | 640 / 640 |
| fenêtre | 1 024 | 256 |

Le fichier fait **73,37 M** paramètres, pas 100 M : l'échelle réelle est **×2,14**, pas ×3. Et il
n'a que **3 000 pas**, soit **10× moins** que le 34 M, avec une PPL de validation **1,6 point
plus mauvaise**. Ce n'est pas un test d'échelle : c'est un **checkpoint précoce** comparé à un
modèle 10× plus entraîné. La conclusion « l'échelle n'achète pas la grammaire » n'est **pas**
démontrée par ces chiffres ; la seule conclusion autorisée est : « ce checkpoint de 73 M à
3 000 pas est plus répétitif et moins divers que le 34 M à 30 000 pas ».

## 8. Ce qui pourrait le rendre faux

- **Prompts et longueur** : 20 prompts fixes, 128 ou 64 octets, un seul jeu. Les prompts
  contiennent parfois un verbe (« Il était une fois », « Les enfants jouent ») ; ils sont communs
  aux deux modèles, donc l'appariement tient, mais les valeurs absolues ne sont pas une
  estimation de population. Le prompt est **inclus** dans le texte analysé ; à 64 octets, il
  pèse plus.
- **Un tirage** : le greedy est déterministe (vérifié 20/20 sur les préfixes 64 → 128), mais
  top-40 et top-20 ne sont pas graine-fixés. Une autre graine peut déplacer les GV de plusieurs
  unités. Le contrôle aléatoire est lui aussi un tirage unique.
- **L'analyseur est heuristique**, pas un parseur : les GV/GN sont des segments de surface,
  l'analyseur attache presque tout (0,56–0,91), et il étiquette « a » `PREP` tout en construisant
  un GV. Un vrai parseur donnerait d'autres chiffres.
- **Le ciment est piégé par la boucle** : 65 % des classes fermées du 100 M greedy sont « de ».
  Un ciment haut peut signifier « boucle sur une préposition », pas « glu grammaticale ».
- **Les contrôles ne sont pas tous appariés au même modèle** : à 128 octets, le contrôle
  `n128` est le **34 M aléatoire** (le contrôle du protocole de référence) ; le contrôle
  scale-matched **100 M aléatoire** est dans `controle_100m_n128`. À 64 octets, seul le
  **34 M aléatoire** existe ; un 100 M aléatoire à 64 octets n'a pas été généré.
- **Asymétrie CPU/GPU** : le 100 M natif a été généré sur GPU, le 100 M aléatoire sur CPU
  (`--aleatoire` ignore `--device` dans l'état actuel du script). L'échantillonnage n'étant pas
  graine-fixé, l'asymétrie est tolérable, mais elle existe.
- **Byte-level, sans BPE** : les chiffres sont propres à ce tokenizer.

## 9. Ce que ça change

1. **Ne pas inscrire le 100 M comme résultat d'échelle.** Le checkpoint disponible est précoce
   (3 000 pas, PPL 4,01) et plus dégénéré ; il ne teste pas l'effet de la taille.
2. **La prochaine action est l'entraînement à parité**, pas le 300 M : amener le 73 M à un budget
   comparable (**13 000 pas pour r1**, **30 000 pas pour la parité stricte** avec le 34 M, ou
   PPL ≤ 2,40), puis rejouer **les mêmes commandes**. Tant que ce n'est pas fait, la ligne N4
   reste « 34 M mesuré, 100 M précoce ».
3. **Le banc de grammaticalité doit devenir un banc à deux axes** : GV/ciment **plus** un
   diagnostic de boucle (part du mot dominant, types générés, part des GV d'un seul token). Sans
   cela, il classe les modèles selon leur token de boucle.
4. **Le ciment seul n'est pas un critère de qualité** : il est plus haut dans le hasard que dans
   les deux modèles. Il ne doit pas être présenté comme un score de grammaticalité.

**Pour le checkpoint r1 (13 000 pas).** Le protocole est prêt : générer à `--n 128 --device
cuda:0`, passer `banc_grammaticalite.py` avec le contrôle 34 M à 128 octets **et** le contrôle
100 M aléatoire à 128 octets, puis comparer, dans cet ordre : (1) la part de « de » (46 % au
checkpoint 3 000 pas) et le nombre de types (74) ; (2) le GV/100 (4,1) et son ratio au hasard
(0,8×) ; (3) le ciment (0,661), en le lisant avec la diversité des classes fermées ; (4) la
répétition (6) et les mots valides (0,878). Si la part de « de » reste haute et que le GV/100 ne
monte pas vers 10–15 à 13 000 pas, le budget seul ne suffira probablement pas ; si elle baisse et
que le GV/100 monte, le checkpoint 3 000 pas était surtout sous-entraîné.

## 10. Voir aussi

- [le banc de génération](../tools/banc_generation.py) · [le banc de grammaticalité](../tools/banc_grammaticalite.py)
- [la fiche du 34 M](rapport-banc-generation.md) · [la fiche du 100 M (64 octets)](rapport-banc-generation-100m.md)
- les données : [100 M grammaticalité](banc-grammaticalite-100m.json) · [34 M grammaticalité](banc-grammaticalite.json) · [34 M génération à 128 octets](banc-generation.json) · [contrôle 34 M à 128 octets](banc-generation-aleatoire.json) · [100 M génération à 64 octets](banc-generation-100m.json) · [contrôle 34 M à 64 octets](banc-generation-alea-64o.json) · [34 M génération à 64 octets](banc-generation-34m-64o.json)
- [le plan natif](../docs/pilotage/natif-plan.md)
