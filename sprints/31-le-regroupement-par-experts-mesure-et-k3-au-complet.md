# Sprint 31 — Le regroupement par experts mesuré, et Kimi-K3 au complet

- **Début** : ~12:45 · **Fin** : ~14:45
- **Objectif** : le bloc 30 a mesuré que les experts reviennent (46,9 % de
  réutilisation immédiate, 86,8 % pour un LRU de 32 par couche) et que le
  décodage ne peut rien en faire — un jeton n'a pas de voisins. Restait le
  **préremplissage** : là, les jetons d'un lot qui ont choisi le même expert
  partagent UNE lecture de sa matrice. Le mécanisme existe (`forward_lot`), il
  n'avait jamais été mesuré. Pendant ce temps, les 1,5 To de Kimi-K3 finissaient
  d'arriver.
- **Engagement de fin** : dépôt vert, machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. Le regroupement par experts existe déjà. Il vaut ×1,58.

Qwen3-30B-A3B (128 experts, 8 par jeton), invite de **192 jetons**, modèle sur
NVMe, 16 fils, 3 passes par point (`tools/mesure-prefill-lot.sh`, neuf) :

| lot | prompt_s | tok/s | CPU % | mur_s |
|---|---|---|---|---|
| 1 | 33,23 | 5,77 | ~995 | 60,5 |
| 2 | **24,51** | 7,83 | ~889 | 51,1 |
| 4 | 23,29 | 8,27 | ~864 | 50,3 |
| 8 | 23,17 | 8,27 | ~854 | 50,6 |
| 16 | 22,45 | 8,53 | ~851 | 49,3 |
| 32 | 21,91 | 8,77 | ~839 | 48,9 |
| 64 | 21,27 | 9,03 | ~831 | 48,2 |
| 192 | **21,00** | 9,20 | ~827 | 47,8 |

**×1,58 de lot 1 à lot 192**, et l'essentiel est pris dès le lot 2 (×1,36). Le
CPU passe de 995 % à 827 % : le chemin par lots fait plus avec moins de cœurs.

### 2. Ce que les octets disent, et où le temps décroche

`tools/analyse_union_experts.py` (neuf) compte, sur la trace de routage réelle,
le nombre **exact** de matrices lues — `N×k` en mode jeton, `Σ|union|` en mode
groupe :

| bloc | gain octets | exp-éq/jeton | gain TEMPS |
|---|---|---|---|
| 1 | 1,00× | 8,000 | 1,00× |
| 2 | 1,31× | 6,111 | **1,36×** |
| 4 | 1,72× | 4,664 | 1,43× |
| 8 | 2,27× | 3,527 | 1,43× |
| 16 | 3,11× | 2,572 | 1,48× |
| 32 | 4,53× | 1,766 | 1,52× |
| 64 | 7,08× | 1,130 | 1,56× |
| 192 | **15,51×** | 0,516 | **1,58×** |

Deux faits, et ils ne disent pas la même chose :

- **au lot 2, le temps suit les octets** (1,31× contre 1,36×) : le chemin jeton
  était bien limité par les octets d'experts, et la corrélation du routage entre
  jetons voisins (46,9 %) fait déjà le travail ;
- **au-delà, le temps décroche** : 15,5× moins d'octets d'experts pour 1,58× de
  temps. Les experts ne sont plus le mur — le calcul dense (attention, normes,
  tête) et l'ordonnancement le sont. **Le levier « octets » s'épuise vers le lot
  8** ; c'est écrit ici plutôt que découvert plus tard sur un modèle géant.

### 3. Un défaut trouvé en mesurant : `--lot N` change la sortie, en silence

Première chose que la trace a montrée : **le routage diffère entre lot 1 et
lot 192 sur 7 838 des 9 312 lignes**. Génération gloutonne, même invite :

```
lot 1   : [67554, 512, 82497, 271, 14374, 220, 16, 13]
lot 2   : [67554, 512, 56698, 20538, 271, 2304, 44320, 56698]
lot 8   : [67554, 512, 56698, 20538, 271, 2304, 44320, 56698]
lot 192 : [67554, 512, 56698, 20538, 271, 2304, 44320, 56698]
```

Le chemin par lots est cohérent avec lui-même (lots 2 à 192 identiques) mais
**diffère du chemin jeton par jeton dès le 3e jeton**, et rien ne le disait.
Quantifié, parce qu'un « ça diverge » sans chiffre ne se décide pas :

| mesure (invite de 192 jetons, lot 1 contre lot 8) | valeur |
|---|---|
| perplexité | 19,172 contre **19,143** (+0,15 %) |
| argmax identique | **191/191 = 100 %** |
| corrélation de Pearson | min **0,99719**, médiane 1,00000 |
| \|Δlogit\| médian | 0,0129 |

Donc : ce n'est pas un autre modèle, c'est le même à 1e-2 près sur les logits —
mais une chaîne gloutonne amplifie, et le 3e jeton part ailleurs. **Le moteur
l'annonce maintenant** (`[options] lot N : …`), avec ces chiffres.

### 4. Deux compteurs muets, refermés

En lisant la mesure, « paires experts » tombait de **1 811,9 M à 18,7 M par
jeton** entre lot 1 et lot 2 — un chiffre qui s'effondre de 97 % sans raison
visible fait croire à une optimisation qui n'existe pas. Cause : `gemm_dense_q4`
ne tient pas de compteur, et le chemin par lots ne comptait donc que les jetons
de génération. Corrigé (experts, plus la sortie d'attention `wo`, qui était le
seul produit du chemin par lots à ne pas se compter : 507,5 M contre 902,6 M
pour le MÊME calcul). Après correction : **2 717,8 M (lot 1) contre 2 721,1 M
(lot 8)**, soit 0,12 % — et la perplexité est inchangée au chiffre près.

### 5. Un piège désarmé : les experts partagés

`forward_lot` n'applique QUE les experts routés : aucune occurrence de `shexp`
dans tout son corps. Sur un modèle qui a des experts partagés (DeepSeek, Kimi),
`--lot N > 1` calculait donc un autre modèle, en silence. Aucun modèle du parc
n'était touché (Qwen3-MoE et gpt-oss n'en ont pas ; V4 est protégé par le refus
sur les hyper-connexions ; Kimi-K3 passe par le chemin MLA jeton par jeton) —
mais le piège était armé pour le jour où. Il **refuse** maintenant, comme les
hyper-connexions.

### 6. Kimi-K3 est arrivé, en entier

32/32 shards, **1 508,7 Go**, vérifiés à l'octet contre Hugging Face.

- `--config` : 93 couches — **1 dense, 68 KDA, 24 MLA**, 896 experts (16 par
  jeton), latent 3 584, routage sigmoïde avec renormalisation, **inventaire
  COMPLET** (aucun tenseur attendu ne manque). Une cadence inattendue est
  signalée : **la couche 92 est MLA alors que 92 % 4 ≠ 3** — 24 couches MLA et
  non 23, la dernière fait exception.
- porte du tokenizer contre l'implémentation officielle : **3 identiques,
  0 divergent**.
- **budget par jeton, mesuré sur le fichier complet** (plus d'extrapolation) :

| poste | Go par jeton | part |
|---|---|---|
| experts routés (16 sur 896) | 25,830 | 29,8 % |
| partagé + attention + tête | 60,958 | 70,2 % |
| **TOTAL** | **86,787** | |

  Inventaire des 2 573 tenseurs : 2 722,7 G poids en MXFP4 (experts) et
  **56,1 G poids en Q8_0** (tout le dense) — d'où les 59,6 Go/jeton du dense.
  **Le dense pèse 2,3× les experts routés** : aucune technique sur les experts
  ne peut adresser plus de 30 % du trafic d'un jeton.

### 7. Ce que ça implique pour K3, chiffré

- **Décodage** : 86,787 Go/jeton. Le plancher RAM (40 Go/s, mesuré) est
  2,17 s/jeton ; le NVMe (3,4 Go/s) 25,5 s. Aucun cache n'y change rien : le
  modèle ne tient pas.
- **Préremplissage** : les 59,6 Go du dense sont lus **une fois pour tout le
  lot**, et les experts suivent l'union. À 1 000 jetons, le coût par jeton tombe
  vers **0,09 Go** — mille fois moins. C'est le seul régime où K3 est
  envisageable ici, et c'est exactement la thèse du dépôt : transporter des
  listes plutôt que refaire le calcul dense.
- **Mais le calcul, lui, ne s'amortit pas.** Par jeton : 98,3 GFLOP pour les
  experts routés (1 488 matrices 3072×3584) + 112,2 GFLOP pour le dense
  (56,1 G poids) = **~210 GFLOP**. Le moteur tient 56,7 GFLOP/s mesurés
  (Qwen3-30B-A3B, lot 192 : 1,19 TFLOP en 21,0 s) → **~3,7 s/jeton de calcul
  pur**, même en préremplissage. C'est une estimation, et elle est annoncée
  comme telle : elle se remplacera par une mesure quand le chemin complet sera
  branché.

**Verdict du bloc** : le levier « lire moins d'octets » est réel mais il est
borné — à 30 % du trafic pour K3, et par le calcul dès le lot 8 sur ce matériel.
Le préremplissage reste la seule porte, et elle coûte 3,7 s/jeton de calcul.

## Relecture adversariale de mes propres chiffres

1. **Le premier balayage était faux d'un facteur 17.** Un `drave` du balayage
   précédent tournait encore pendant le lot 2 : 580 s au lieu de 24. Deux pools
   de 16 fils sur 40 CPU se disputent les cœurs ET la bande. Le script refuse
   maintenant de tourner sans le dire, et le protocole est « rien d'autre ».
2. **×1,58 est mesuré sur un modèle dont les experts ne sont que 56 % des
   octets d'un jeton.** Sur K3, où ils sont 30 %, le même levier vaudra moins —
   la transposition est un raisonnement, pas une mesure, et elle est écrite
   comme telle.
3. **Le gain temps ne suit pas le gain octets au-delà du lot 2.** Présenter
   « 15,5× moins d'octets » comme un gain de vitesse serait faux ; les deux
   colonnes sont côte à côte dans le tableau pour que ça se voie.
4. **La divergence lot 1 / lot N n'est pas forcément bénigne.** 191/191
   d'accord sur l'argmax d'invite ne garantit rien sur 10 000 jetons. Elle est
   annoncée, chiffrée, pas excusée.
5. **Le budget K3 est mesuré, les GFLOP/s sont empruntés à un autre modèle.**
   Le rapport des deux est une extrapolation.

## Une hypothèse avancée puis RÉFUTÉE (même bloc)

Le plateau du gain au-delà du lot 2 appelait une explication. La voici, telle
qu'elle a été écrite avant d'être testée : le GEMM 4 bits balaie les lignes une
fois par tuile de jetons, donc **déchiffre les poids `t/tuile` fois** — à tuile 8
fixe et lot 192, vingt-quatre fois. Une tuile plus grande devait donc gagner.

Mesuré (`DRAVE_TUILE_LOT`, lot 32, invite de 192 jetons, 16 fils) :

| tuile | prompt_s (4 passes) | moyenne |
|---|---|---|
| 8 (la constante historique) | 21,74 · 21,24 · 20,24 · 21,67 | **21,22** |
| 16 | 21,46 · 20,96 | **21,21** |
| 64 (déduite de 256 Kio d'activations) | 20,30 · 21,61 · 24,30 · 21,73 | **21,99** |

**Aucune différence, et la grande tuile est plutôt derrière.** L'hypothèse est
fausse : le déchiffrage des poids n'est pas ce qui borne ce noyau. La constante
reste donc à **8**, la valeur avec laquelle tout le reste du bloc a été mesuré,
et `DRAVE_TUILE_LOT` est laissé comme banc d'essai — pas comme réglage.

Le plateau vient donc d'ailleurs : la part dense (attention, normes, tête) ne
s'amortit pas par le regroupement des experts, et c'est elle qui prend la main.

## Environnement de mesure, dit honnêtement

La fin du bloc a été mesurée pendant que `llama.cpp-k3` chargeait Kimi-K3 :
**711 Go lus en 1 h 50** à travers le cache de pages, ce qui évince le modèle de
mesure en cours de route. Les chiffres du tableau principal (le balayage des
lots) ont été pris **avant**, machine au repos ; ceux de l'essai de tuile ont été
pris **pendant**, et c'est précisément pourquoi la conclusion est « aucune
différence » et non « ×1,3 » : dans cet environnement, un écart de 30 % n'est pas
attribuable.

