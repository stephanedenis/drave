# N2.ae — 200 000 pas sur le mélange 1 Go : −0,33 en domaine, −1,06 en largeur, et la porte 2,5 à un million de pas

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : à recette constante (34,3 M,
> canal, positions aléatoires), passer de **60 000** à **200 000 pas** sur le mélange de **1,02 Go**
> fait baisser la PPL partout — **3,1591** en validation française (contre 3,4902, **−0,33**),
> **3,0035** sur le grand corpus (−0,35), **5,6056** en littérature (−0,42), **7,2770** en anglais
> (−1,06), **8,0018** sur wikitext2 (−1,05) — **sans perdre le français**. La porte **< 2,5 n'est
> pas atteinte** : la PPL de domaine est à **3,16**, et la loi de puissance mesurée sur la
> trajectoire (exposant **0,099** sur 20 k–200 k, **0,089** sur 40 k–200 k) place 2,5 à **1,3–2,7
> millions de pas**, soit **21 à 44 h** de GPU à cette vitesse. Deux effets secondaires nets : le
> gain **décroît avec la longueur** et **s'inverse à 512 octets** (+0,14), et la **largeur** est ce
> qui progresse le plus. C'est l'argument direct de R1.2 : le compute ne remplace pas une fenêtre
> entraînée.

## La question

N2.aa avait montré qu'à 40 Mo vus, un corpus 5,6× plus grand ne fait pas apprendre plus — il fait
apprendre **autre chose** ; la bonne question était donc « **plus de pas ?** ». `en-cours` la
formulait ainsi : **les 200 000 pas sur le mélange 1 Go font-ils passer sous 2,5 sans perdre le
français ?** N2.ac (60 000 pas) valait 3,49 en domaine et 6,03 en littérature : la porte était à
0,99.

## Le dispositif

- **Corpus** : `data/wiki_mix/propre/train.txt` — **1 017 487 092 octets** (1,02 Go), concaténation
  de `data/wiki_fr/propre` (186 Mo) et `data/wiki_big/propre` (831 Mo) ; canal concaténé ; le
  découpage interne réserve les 5 % finaux à la validation d'entraînement.
- **Recette** : **identique à N2.ac** — 34,3 M (`384/512`), `--seq 128 --lot 8 --lr 3e-4
  --graine 1 --positions-aleatoires 384 --canal` — à un seul paramètre près : **200 000 pas** au
  lieu de 60 000 (×3,33). GPU 0, **11 410 s** (3 h 10), ~57 ms/pas.
- **Mètre** : `work/n2ac/eval_200k.py`, protocole N2.ac — canal fourni, fenêtres Van der Corput
  dans des chunks de 8 192, 8 lots × 16 fenêtres. Le témoin 60 k (`work/n2w/mix-60k.pt`), repassé
  dans le même mètre, **redonne N2.ac à l'identique** (3,4902 / 3,4615 / 3,5169 / 6,0283 / 8,3352
  / 9,0525) : le banc n'a pas bougé entre les deux fiches.
- **Contrôles** : contrôle **par permutation** des octets de validation (ordre détruit, octets et
  canal ensemble) ; deux validations appariées (fr et grand corpus) ; une mesure de **transfert**
  sur le corpus propre du dépôt (jamais vu).

## Ce qui est mesuré

| mesure | 60 000 pas (N2.ac) | **200 000 pas** | écart |
|---|---:|---:|---:|
| validation française (L128) | 3,4902 | **3,1591** | −0,3311 |
| validation française (L256) | 3,4615 | 3,2047 | −0,2568 |
| validation française (L512) | 3,5169 | 3,6577 | **+0,1408** |
| validation du grand corpus (L128) | 3,3565 | **3,0035** | −0,3530 |
| validation du grand corpus (L512) | 3,3685 | 3,4878 | **+0,1193** |
| littérature (jamais vue) | 6,0283 | **5,6056** | −0,4227 |
| anglais (jamais vu) | 8,3352 | **7,2770** | −1,0582 |
| wikitext2 (jamais vu) | 9,0525 | **8,0018** | −1,0507 |
| corpus propre du dépôt (transfert) | 9,2731 | 9,1262 | −0,1469 |
| **permutation (contrôle négatif)** | 215,56 | **181,91** | — |

Précision top-1 (tête principale) : **0,6416 → 0,6741** (+3,3 points) ; têtes précoces :
0,5764 / 0,6221 / 0,6379 → **0,6091 / 0,6619 / 0,6716**.

### La trajectoire et sa loi

Validation interne (2 lots, 8 192 octets — bruit ±0,05), tous les 10 000 pas :

| pas | 10 k | 30 k | 50 k | 100 k | 150 k | 200 k |
|---|---:|---:|---:|---:|---:|---:|
| PPL | 4,646 | 3,781 | 3,525 | 3,292 | 3,152 | **3,103** |

La mesure finale sur 8 lots (32 768 octets) vaut **2,9801**. Ajustée en loi de puissance
`PPL = a · pas^(−b)` : **b = 0,0987** sur 20 k–200 k (**a = 10,30**), **b = 0,0894** sur 40 k–200 k
(**a = 9,23**). L'exposant **décroît** quand on retire la phase rapide — la loi n'est pas stable,
et c'est une information : le rendement baisse plus vite qu'une loi unique ne le dit.
Extrapolation (avec cette réserve) : la cible 2,5 demande **1,69 M** pas (loi 20 k) ou **2,22 M**
pas (loi 40 k) depuis le début, soit **1,3 à 2,7 M** pas de plus depuis 200 k — **21 à 44 h** de
GPU à 57 ms/pas.

### La courbe de longueur se dégrade

Sur la validation française, le 200 k vaut 3,1591 / 3,2047 / 3,6577 / **8,2262** à
128/256/512/1 000 octets ; le 60 k, 3,4902 / 3,4615 / 3,5169 / **7,9201**. Autrement dit : **plus
le modèle apprend, plus il est bon dans la longueur qu'on lui donne et plus il se dégrade
au-delà** — à 512 octets le gain de 140 000 pas devient une **perte** (+0,14), et à 1 000 octets
aussi (+0,31 ; les deux explosent, la table absolue n'ayant rien appris au-delà de 511). Même
mécanisme que R1.1, et argument direct pour R1.2.

## Lecture

1. **Le levier du compute est réel, et il ne coûte pas le français.** Les trois mesures hors
   domaine **baissent** (−0,42, −1,06, −1,05) : la largeur ne se paie pas, elle progresse. Le
   français de domaine baisse de 0,33, soit **9,5 %** — le meilleur gain relatif avec le grand
   corpus (−10,5 %).
2. **Mais la porte 2,5 n'est pas une affaire de pas.** À 3,16, il manque **0,66**, et la loi place
   la cible à **plus d'un million de pas** — plus d'une journée de GPU pour un facteur 1,26. Le
   rendement mesuré est de **−0,09 par 100 000 pas** dans la phase lente : la porte n'est pas
   atteignable par le compute seul à cette recette.
3. **Le gain s'inverse avec la longueur** : c'est le résultat le plus utile pour la ligne R. Le
   compute rend le modèle **meilleur à la longueur entraînée** (128) et **pire au-delà** (512).
   Entraîner plus longtemps sans entraîner plus long **durcit** le verrou de longueur.
4. **Le transfert au corpus propre ne bouge presque pas** (9,27 → 9,13) : le modèle de wiki reste
   un modèle de wiki. Ce n'est pas une régression — c'est la confirmation que la PPL mesure
   l'appariement de domaine (N2.aa), et que la porte 2,5 se joue sur le corpus propre avec un
   modèle entraîné dessus.

## Ce qui pourrait le rendre faux

- **Un seul lancement par budget** ; la recette n'est pas déterministe (les décalages de position
  viennent de `random`, non semé, et les noyaux GPU ne le sont pas). Contrôle de répétition : les
  **60 000 premiers pas** du run de 200 k redonnent ceux de N2.ac à la perte près (1,2569 contre
  1,2579) et à **0,09 de PPL** près sur la validation interne (3,390 contre 3,480) — c'est le
  bruit de lancement, et il est **3,7× plus petit** que le gain mesuré.
- **La validation interne est le tail du grand corpus** (50,9 Mo), pas un fichier tenu à part ;
  les validations d'évaluation (fr et grand) sont, elles, des fichiers distincts. Les deux
  donnent le même ordre de grandeur.
- **La concaténation met le français en premier** : la première moitié du corpus est française, et
  le découpage interne réserve les 5 % finaux (donc du grand corpus) à la validation
  d'entraînement.
- **200 000 pas n'est pas la convergence** : la perte finale (1,205) est encore au-dessus de son
  plancher de bruit, et la trajectoire ne montre pas de plateau.
- **La loi de puissance est un ajustement, pas une mesure** : l'exposant varie de 0,089 à 0,099
  selon la plage, et rien ne dit qu'il ne s'effondrera pas avant 2,5. C'est une **borne de
  lecture**, pas une prédiction.
- **Le contrôle par permutation** donne 181,9 et 199,9 : très au-dessus du signal, mais pas
  exactement 256, parce que les marginales d'octets et le canal restent informatifs. Il prouve que
  le mètre lit l'**ordre**, pas qu'il soit parfait.

## Ce que ça change pour N2 et pour R1

- **La recette de production reste N2.ac** (60 k) tant que R1 n'a pas livré une fenêtre entraînée :
  le 200 k est meilleur partout **sauf à 512 octets**, et il coûte 3,3× le compute.
- **La porte < 2,5 doit changer de levier** : le compute seul demande > 1 M de pas ; la piste
  « plus de texte » est déjà un négatif (N2.aa). Restent la **capacité** et l'**architecture de
  fenêtre** — et R1.2 vient de montrer que la fenêtre entraînée paie à octets constants.
- **La longueur est le seul axe qui recule** dans ce cycle : c'est là qu'il faut mettre le
  prochain run, pas dans un 500 k pas.

## Fichiers

- Modèle : `work/n2ac/mix-200k.pt` (`sha256_drvm` `bec5470e…`) ; témoin `work/n2w/mix-60k.pt`.
- Corpus : `data/wiki_mix/propre/{train,val}.txt` et `.canal` ; manifeste
  [`corpus-wiki-big-propre.json`](corpus-wiki-big-propre.json).
- Banc : `work/n2ac/eval_200k.py`, `work/n2ac/eval_longueurs.py`, `work/n2ac/table_200k.py`,
  `work/n2ac/trajectoire.py` ; journal d'entraînement `work/n2ac/mix-200k.log`.
- Mesures : [`n2-200k.json`](n2-200k.json) ; fiches amont
  [`n2-melange`](rapport-n2-melange.md), [`n2-1go`](rapport-n2-corpus-1go.md),
  [`n2-r11`](rapport-n2-r11.md).
