# R1.2 — La fenêtre 2 048 et le point d'équilibre : à octets constants, 1 024 gagne ; à pas constants, plus de données gagnent

> **Ligne de roadmap** : R1 (la fenêtre native) · **Date** : 2026-11-03 · **Verdict** : à
> **octets constants** (20,5 Mo vus sur `data/wiki_fr`), la fenêtre entraînée paie jusqu'à
> **1 024** — à 2 000 octets, 3,2459 (fenêtre 256) → 2,9728 (512) → **2,9449** (1 024) — et
> **2 048 ne la bat pas** (2,9630) : à budget d'octets fixé, doubler encore la fenêtre divise les
> **pas** par deux (1 250 contre 2 500) et le gain s'annule. À **pas constants** (20 000), la même
> recette à fenêtre **1 024** voit **8× plus d'octets** et **écrase** tout : **2,9955** à 128
> octets, **2,6256** à 1 000, **2,5429** à 4 000 — à **0,13** et **0,04** de 2,5 en domaine
> (`val_fr`, pas le corpus propre : ce n'est pas la porte, c'en est le voisinage). La fenêtre et
> le compute ne s'opposent pas : la fenêtre **rend chaque octet plus utile**, et c'est le produit
> des deux qui compte.

## La question

La fiche [`rapport-n2-fenetre`](rapport-n2-fenetre.md) a mesuré la loi à trois points (256, 512,
1 024) à octets constants et conclu que 1 024 gagnait là où la fenêtre sert. Deux questions
restaient : **est-ce que ça continue** (2 048), et **qu'est-ce que ça donne quand on paie le
compute** (la même recette à 20 000 pas).

## Le dispositif

| run | seq = fenêtre | pas | octets vus | init |
|---|---:|---:|---:|---|
| fenêtre 256 | 128 | 20 000 | 20,5 Mo | `base-wiki-45m` |
| fenêtre 512 | 512 | 5 000 | 20,5 Mo | `base-wiki-45m` |
| fenêtre 1 024 | 1 024 | 2 500 | 20,5 Mo | `base-wiki-45m` |
| **fenêtre 2 048** | 2 048 | 1 250 | 20,5 Mo | `base-wiki-45m` |
| **fenêtre 1 024, 20 k pas** | 1 024 | 20 000 | 164 Mo | `base-wiki-45m` (puis suite) |

RoPE, 34,3 M (`384/512`), lot 8, lr 3e-4, graine 1, canal, corpus `data/wiki_fr/propre` (186 Mo).
Mètre `eval_production.py` : les deux validations appariées, canal fourni, longueurs jusqu'à
4 000 octets. Contrôles : même texte (contexte 256 → 2 000), permutation, miroir de copie.

## 1. À octets constants : le gain s'arrête à 1 024

Validation française, PPL par longueur :

| fenêtre | 128 | 512 | 1 000 | 2 000 | 4 000 |
|---|---:|---:|---:|---:|---:|
| 256 (20 000 pas) | 3,3696 | 3,2892 | 3,2545 | 3,2459 | 3,2305 |
| 512 (5 000 pas) | **3,3399** | **3,0990** | 3,0107 | 2,9728 | 2,9447 |
| **1 024 (2 500 pas)** | 3,3878 | 3,1098 | **2,9950** | **2,9449** | **2,9108** |
| 2 048 (1 250 pas) | 3,4179 | 3,1450 | 3,0202 | 2,9630 | 2,9265 |

- **la fenêtre 1 024 est la meilleure à partir de 1 000 octets** et jusqu'à 4 000 ;
- **2 048 ne la bat pas** — à 4 000 octets, 2,9265 contre **2,9108**, et il a coûté la moitié
  des pas ;
- à 128 octets, l'ordre est **512 > 256 > 1 024 > 2 048** : plus la fenêtre est longue, plus le
  **démarrage à froid** coûte, et à octets constants il n'est pas rattrapé.

**Le point d'équilibre est donc 1 024 octets** à ce budget : au-delà, la fenêtre n'achète plus
rien — c'est le nombre de pas qui manque.

## 2. À pas constants : la fenêtre rend chaque octet plus utile

Même recette (RoPE, 1 024), mais **20 000 pas** — donc **8× plus d'octets** que le run à
2 500 pas :

| run | octets | 128 | 512 | 1 000 | 2 000 | 4 000 |
|---|---:|---:|---:|---:|---:|---:|
| fenêtre 256, 20 000 pas | 20,5 Mo | 3,3696 | 3,2892 | 3,2545 | 3,2459 | 3,2305 |
| **fenêtre 1 024, 20 000 pas** | **164 Mo** | **2,9955** | **2,7201** | **2,6256** | **2,5757** | **2,5429** |
| fenêtre 2 048, 15 000 pas | 246 Mo | 3,0065 | 2,7227 | **2,6118** | **2,5514** | **2,5114** |

Ce n'est pas une comparaison de fenêtre (les octets diffèrent) : c'est la **recette** à 1 024 qui
monte en régime. La comparaison honnête est **à corpus et recette égaux** — le run de R1.1
(20 000 pas, fenêtre 256, **20,5 Mo**) contre celui-ci (20 000 pas, fenêtre 1 024, **164 Mo**) :

| | 128 | 512 | 1 000 | 2 000 | 4 000 |
|---|---:|---:|---:|---:|---:|
| R1.1 (fenêtre 256, 20,5 Mo) | 3,3696 | 3,2892 | 3,2545 | 3,2459 | 3,2305 |
| **fenêtre 1 024, 164 Mo** | **2,9955** | **2,7201** | **2,6256** | **2,5757** | **2,5429** |
| écart | −0,374 | −0,569 | −0,629 | −0,670 | −0,688 |

**La fenêtre ne s'oppose pas au compute, elle le multiplie** : à pas constants, elle fait
−0,37 en domaine et **−0,63 à 1 000 octets**, et l'écart **croît avec la longueur**. Sur le même
corpus, la porte 2,5 n'est plus qu'à **0,13** en domaine à 1 000 octets (2,6256), là où la
recette à fenêtre 256 était à **0,75** (3,2545).

**Le point d'équilibre se déplace avec le budget** : à 246 Mo vus (15 000 pas à 2 048), la
fenêtre 2 048 reprend la tête au long — **2,5114** à 4 000 octets, le meilleur chiffre de la nuit
sur `val_fr`, contre 2,5429 pour 1 024 — mais elle reste derrière à 128 octets (3,0065 contre
2,9955). « 1 024 est le point d'équilibre » vaut donc **à 20,5 Mo de budget** : plus on paie
d'octets, plus la fenêtre large devient rentable.

Réserve de corpus : ce modèle n'a vu que `wiki_fr`, dont la validation `val_fr` est le domaine ;
les modèles du mélange (production) paient la largeur en domaine (`mix-200k` : 3,1591). Le
chiffre 2,9955 n'est donc **pas** comparable directement à 3,1591 — c'est la comparaison
R1.1 → 1 024 (même corpus) qui porte.

## 3. Le contrôle « même texte » : la fenêtre reste la borne

Le modèle à 1 024 (20 k pas) : 2,9197 → 2,8125 → **2,7847** → 2,7837 au contexte 256/512/1 024/
2 000 — il gagne jusqu'à **1 024** et s'arrête (**1 024 = 2 000**). Le modèle à 2 048 n'a pas été
contrôlé de la même façon faute de temps de banc ; c'est une limite nommée.

## 3 bis. La fenêtre paie à toutes les capacités testées

La note de passage N2 → R1 demandait de refaire R1.1/R1.2 « au moins à 21,65 M et 34,3 M ». Les
deux bras RoPE ont été entraînés **depuis une initialisation aléatoire identique**, à **octets
constants** (33 Mo), fenêtre 512 (8 000 pas) contre fenêtre 128 (32 000 pas) :

| capacité | fenêtre 512 : 128 / 512 / 1 024 | fenêtre 128 : 128 / 512 / 1 024 |
|---|---|---|
| **11,47 M** | 3,6452 / **3,4493** / **3,3628** | **3,5979** / 6,1680 / 7,2446 |
| **21,65 M** | 3,5312 / **3,3145** / **3,2104** | **3,4494** / 6,1580 / 7,6361 |

Le motif est **le même à toutes les tailles** : à 128 octets la fenêtre courte gagne de 0,05 à
0,08 ; dès 512 elle perd **2,7** (11,47 M) et **2,8** (21,65 M). La fenêtre n'est donc **pas un
luxe de gros modèle** : elle est la condition pour que la longueur existe, du plus petit au plus
grand. Les niveaux absolus ne se comparent pas d'une taille à l'autre (les bras 34,3 M partent
d'un modèle déjà entraîné, ceux-ci de zéro) ; c'est le **contraste fenêtre** qui est mesuré ici.

## 4. Le miroir de copie reste muet

Sur tous les modèles de la nuit, la justesse de copie à distance est **0,0078** au mieux (le
hasard de 1/128), y compris à fenêtre 1 024 et sur la production affinée. **La fenêtre plus large
ne crée pas de circuit de copie** : la PPL baisse, la restitution ne vient pas avec. C'est la
limite dure de R1 — et la raison pour laquelle la porte « aiguille native ≥ 15/18 à 4 000 octets »
n'est pas atteinte.

## Ce que ça change

- **La recette de production recommandée** devient : mélange 1 Go, RoPE, **fenêtre 1 024**,
  autant de pas qu'on peut payer — pas 128. La fenêtre 512 reste le compromis à bas budget, et
  2 048 n'a pas d'intérêt à budget d'octets fixé.
- **La porte < 2,5 change de prix** : sur le corpus propre de ce banc, elle est passée de 0,75
  au-dessus (fenêtre 256) à **0,13 au-dessus** (fenêtre 1 024) pour le même nombre de pas — le
  prochain run doit être un run **long à fenêtre 1 024**, pas un run de pas à fenêtre 128.
- **Le point d'équilibre 1 024** est une mesure à un budget (20,5 Mo) ; à budget plus grand, il
  se déplacera peut-être vers 2 048.

## Ce qui pourrait le rendre faux

- **Un lancement par point**, et les pas d'optimisation ne sont pas contrôlés à octets constants
  (20 000 / 5 000 / 2 500 / 1 250) : c'est précisément ce que le § 2 mesure, mais chaque point de
  la loi reste unique.
- **Le point 2 048 n'a que 1 250 pas** : il est pénalisé par construction ; à 2 500 pas il
  battrait peut-être 1 024. La conclusion « 1 024 est le point d'équilibre » vaut **à 20,5 Mo de
  budget**, pas dans l'absolu.
- **Le run à 1 024 / 20 000 pas** part du même point que les autres : il mesure la recette, pas
  l'effet isolé de la fenêtre (les octets ont été multipliés par 8).
- **La validation interne et les validations d'évaluation** ne sont pas le même texte ; les
  écarts inférieurs à 0,05 ne sont pas interprétables.
**Le coût d'inférence ne quadruple pas.** Mesuré à batch 8 (`work/n2ac/cout_fenetre.py`),
le débit passe de **22 306** octets/s (fenêtre 256) à **22 730** (512), **21 156** (1 024) et
**19 405** (2 048) : l'attention quadruple à chaque doublement, mais le FFN **domine** à 34,3 M,
donc le débit ne perd que **13 %** de 256 à 2 048. La fenêtre est presque gratuite à cette
taille — elle ne le resterait pas à plus grande échelle.

## Fichiers

- Modèles : `work/n2ac/rope2048-1.25k.pt`, `work/n2ac/rope1024-20k.pt` ; comparés à
  `work/n2ac/rope-20k.pt` et `work/n2ac/rope512-5k.pt` (fiche `n2-fenetre`).
- Bancs : `work/n2ac/eval_production.py`, `eval_longueurs.py`, `eval_fenetre.py`,
  `chaine_2048_wiki.sh`, `chaine_1024.sh`.
- Mesures : `reports/n2-r12-2048.json` ; fiches amont
  [`n2-fenetre`](rapport-n2-fenetre.md), [`n2-r11`](rapport-n2-r11.md).
