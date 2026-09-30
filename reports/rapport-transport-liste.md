# Phase 3.2 — transporter la LISTE au lieu du vecteur

**En une ligne** : le flux peut voyager en liste creuse (871 octets au lieu de
3 623), mais à seuil 5 % le découpage coûte **×1,8 de perplexité** — la courbe
est là, avec le seuil où ça casse.

## Le protocole, mesuré

Deux modes dans le même en-tête de 39 octets — magie, version, mode, plage,
position, dimension, échelle, **et les réglages d'activation** :

| mode | contenu | octets par flux (Qwen2.5-0.5B, 896 canaux) |
|---|---|---|
| 0 · dense f32 | `896 × f32` | **3 623** (39 + 3 584) |
| 1 · listes | `n × (indice u16 · valeur i16)` | 39 + 4 × actifs |

Le mode 1 est le format du disque, à l'octet près. La réponse est encodée comme
la demande : un pair qui parle en listes reçoit des listes.

## La courbe (40 jetons, 12 couches de chaque côté)

| seuil | activité | octets/flux (aller) | octets/flux (retour) | perplexité locale | perplexité répartie | écart |
|---|---|---|---|---|---|---|
| dense f32 | 100 % | 3 623 | 3 623 | 144,8289 | **144,8289** | **0,00e0** |
| listes 0,00 | 100,0 % (896) | 3 622 | 3 622 | 144,8289 | 141,0539 | 2,6e-2 |
| listes 0,02 | 60,4 % (541) | 2 203 | 2 677 | 203,8033 | 213,7739 | 4,9e-2 |
| listes 0,05 | 24,0 % (215) | 897 | 993 | 493,0344 | 893,1350 | 8,1e-1 |
| listes 0,10 | 36,5 % (327) | 1 347 | 216 | 35 483,0643 | 66 813,6606 | 8,8e-1 |

Trois lectures, dans l'ordre d'importance :

1. **Le mode dense est fidèle au bit près** (0,00e0) : le découpage ne change
   rien, et les réglages d'activation qui voyagent dans l'en-tête garantissent
   que les deux nœuds quantifient pareil. Sans eux : écart 0,69.
2. **Le gain de taille ne vient que de la sparsité.** À seuil 0, la liste est
   pleine : 4 octets par canal, exactement comme le dense — le même nombre
   d'octets, pour une perte de 2,6 %. La valeur occupant 16 bits sur le fil, le
   seul levier est de *jeter* des canaux.
3. **Jeter coûte cher, et pas linéairement.** À 0,02 (60 % d'activité) on a déjà
   perdu la fidélité (4,9e-2) ; à 0,05 (24 %) l'écart est ×1,8 ; à 0,10 la
   perplexité locale elle-même explose (35 483) parce que le flux tronqué détruit
   l'état du modèle — et la ligne 0,10 n'est donc pas comparable aux autres.

## Ce que la courbe a appris sur le fond

Le rejeu d'une trace quantifiée sur 16 bits redonnait la perplexité **exacte**
(19,3885), mais ici 16 bits coûtent 2,6 % : la différence n'est pas la précision,
c'est **ce qu'on quantifie**. La trace encode l'entrée NORMÉE d'une couche ; le
transport encode le résidu brut, dont la dynamique est bien plus large — une
échelle unique par vecteur donne une erreur *absolue* constante, donc une erreur
*relative* énorme sur les petits canaux, et l'erreur se compose sur douze
couches.

D'où les deux suites possibles :

* **une échelle par bloc de 32 canaux** (comme le cache KV) au lieu d'une échelle
  par vecteur : faite, c'est `--flux-blocs` ci-dessus — erreur relative bornée
  par bloc, et deux octets de moins par neurone actif ;
* **transmettre l'entrée normée** de la première couche distante : essayée,
  **RÉFUTÉE**, voir ci-dessous.

### L'entrée normée : réfutation, et pourquoi

L'idée semblait bonne — la trace encode l'entrée normée d'une couche et son rejeu
sur 16 bits redonne la perplexité exacte. Un drapeau `--flux-norme` a donc été
écrit : le pilote envoie `rmsnorm(résidu, attn_norm[12])`, le nœud distant saute
sa propre norme d'entrée. Le banc de contrôle est sans pitié : **en mode dense,
où le transport est exact, l'écart passe de 0,00e0 à 5,61e0** (perplexité 119
contre 18,02). Ce n'est pas une perte de précision, c'est un calcul faux.

La raison est simple une fois écrite : la norme d'entrée n'est pas seulement
l'entrée de l'attention, c'est aussi **ce qui reste à côté** — la connexion
résiduelle a besoin du résidu, pas de sa version normée. En remplaçant le résidu
par l'entrée normée, on casse `x = x + attention(norme(x))` dès la première
couche distante. Pour que l'idée marche, il faudrait transmettre **les deux**
(deux fois plus d'octets, aucun gain) ou reconstruire le résidu par
`x = hn · rms(x) / w` — exact sur le papier, fragile là où `w` s'approche de
zéro.

Le drapeau a été retiré, et c'est la mesure du mode dense qui l'a dit. Une
hypothèse réfutée vaut mieux qu'un mode « presque juste » qu'on aurait gardé.

## Ajouts de la session

* `--flux-liste` : le pilote envoie des listes ; le nœud moteur suit le mode reçu.
* **Version dans chaque en-tête** (3.5) : un pair en version 99 est refusé avec
  `flux en version 99, cette build parle la 4 (pair incompatible : rien n'a été
  interprété)` — vérifié avec un client Python qui envoie un faux en-tête.
* **Les réglages d'activation voyagent** : niveaux, seuil, top-k, renorm. Deux
  nœuds lancés avec des seuils différents calculaient deux choses différentes en
  silence (écart 0,69 mesuré) ; le client impose désormais les siens.
* `tools/pair_factice.py` : un pair qui parle le protocole sans charger de
  modèle et **dit** ce qu'il reçoit. C'est lui qui a montré que le flux fait 896
  canaux quand mon compteur en annonçait 919 (division par 39 au lieu de 40).


## Ajout — l'échelle par bloc de 32 canaux (`--flux-blocs`)

Trois octets par neurone actif (indice u16, valeur **i8**) plus une échelle f32
par bloc de 32. Le seuil reste global — c'est lui qui décide de la sparsité.

| seuil | activité | octets/flux | écart | à comparer aux listes i16 |
|---|---|---|---|---|
| 0,00 | 98,1 % | 2 793 | 7,1e-2 | 3 622 octets · 2,6e-2 |
| 0,02 | 60,4 % | **1 778** | **2,2e-3** | 2 203 octets · 4,9e-2 |
| 0,05 | 24,0 % | 799 | 1,1e0 | 897 octets · 8,1e-1 |

**En régime creux, l'échelle par bloc gagne sur les deux tableaux** : à seuil
0,02, ÷1,24 d'octets *et* une fidélité vingt fois meilleure (2,2e-3 contre
4,9e-2). C'est cohérent : une échelle unique par vecteur donne une erreur
*absolue* constante, donc catastrophique en relatif sur les canaux faibles ; une
échelle par bloc borne l'erreur *relative*, ce qui autorise des valeurs à un
octet.

À pleine densité, en revanche, l'i16 avec une échelle globale est plus fidèle
(2,6e-2 contre 7,1e-2) — mais à pleine densité il n'y a rien à gagner : 2 793
octets contre 3 623, et les deux modes sont de toute façon « taille du dense ».
**Le régime qui compte est le régime creux, et c'est là que les blocs gagnent.**

Configuration utilisable aujourd'hui : `--flux-blocs --act-thresh 0.01`, soit
**÷2,3 sur le fil pour 2,7 %** de perplexité.

### Sur du vrai texte, les chiffres sont plus sobres

Le banc ci-dessus utilise des identifiants synthétiques (`1, 2, 3, …`) dont la
perplexité se compte en centaines : toute erreur de logit y est amplifiée. Mesuré
sur **256 jetons de WikiText-2**, où la référence locale vaut 18,02 :

| mode | seuil | activité | octets/flux | écart |
|---|---|---|---|---|
| dense f32 | — | 100 % | 3 623 | **0,00e0** |
| blocs | 0,01 | 78,6 % | 2 268 | 2,7e-2 |
| blocs | 0,02 | 59,2 % | 1 745 | 1,4e-1 |
| listes i16 | 0,02 | 59,2 % | 2 159 | 1,6e-1 |

Trois choses y sont nettes : le mode dense reste **exact** ; les blocs battent
toujours les listes à sparsité égale (1 745 contre 2 159 octets, et 14 % contre
16 % d'écart) ; et l'écart dépend du **corpus** bien plus que du seuil — 0,2 % sur
identifiants synthétiques à 40 jetons, 2,7 % sur du vrai texte à 256.

### L'écart selon la longueur : il DÉCROÎT

J'avais écrit que l'écart croissait avec la longueur. La courbe dit le contraire
(blocs, seuil 0,01, WikiText-2, contexte 512) :

| jetons | écart | octets/flux | activité |
|---|---|---|---|
| 64 | 1,37e-1 | 2 249 | 77,9 % |
| 128 | 6,37e-2 | 2 257 | 78,2 % |
| 256 | 2,74e-2 | 2 268 | 78,6 % |
| **1 024** | **1,32e-2** | **1 589** | 79,8 % |

Il décroît, et c'est logique : la perturbation est à peu près stationnaire par
jeton, donc son effet sur une perplexité *moyennée* se dilue quand la séquence
s'allonge. Ce qui change vraiment d'un banc à l'autre, c'est le **corpus** —
sur des identifiants synthétiques la perplexité se compte en milliers et la
sensibilité relative n'a rien à voir.

Donc la revendication honnête, sur du vrai texte, est celle du tableau
ci-dessous — **÷2,3 sur le fil pour 1,3 % d'écart à 1 024 jetons** (2,7 % à 256,
13,7 % à 64) (et 13,7 % d'écart à 64 jetons : sur une séquence courte,
l'erreur est chère). Ni le « ÷2 pour 0,2 % » que j'avais tiré du banc
synthétique, ni le « ça empire avec la longueur » que j'en avais déduit à tort —
les deux ont été écrits puis corrigés par la mesure.

### Les indices par écarts : ÷2,3 au total, à quantification IDENTIQUE

La liste d'indices est triée (les blocs sont parcourus dans l'ordre), donc
l'écart au neurone actif précédent tient sur **un octet** dans l'immense majorité
des cas ; 255 est l'échappement vers l'indice absolu. Deux octets par neurone
actif au lieu de trois.

| mode | octets/flux | écart | perplexité répartie |
|---|---|---|---|
| dense f32 | 3 623 | 0,00e0 | 18,0206 |
| blocs 0,01, indices u16 | 2 268 | 2,74e-2 | 21,8873 |
| **blocs 0,01, indices par écarts** | **1 568** | **2,74e-2** | **21,8873** |

Même écart, même perplexité au chiffre près : c'est du **rangement**, pas de la
perte — et c'est la meilleure façon de le prouver. Au total, le flux passe de
3 623 à 1 568 octets, soit **÷2,3**, pour 2,7 % d'écart sur 256 jetons de vrai
texte. À 20 jetons/s, cela demande **0,25 Mbit/s**.

## Ajout — le coût réel du découpage, et Nagle

Mesuré à 200 jetons, machine au repos, 12 couches par nœud, localhost :

| | avant | après |
|---|---|---|
| calcul local (12 couches) | 15,6 ms/jeton | 15,9 ms/jeton |
| attente du pair | **97,6 ms/jeton** | **16,1 ms/jeton** |
| rapport attente/calcul | **6,26×** | **1,01×** |
| durée du banc réparti | 24,5 s | **8,3 s** (référence locale : 8,2 s) |

L'attente de 97,6 ms n'était ni le calcul distant ni le débit : c'était **Nagle
et l'ACK différé**. Le pilote écrit un en-tête de 39 octets puis un corps ; sans
`TCP_NODELAY`, la seconde écriture attend l'acquittement de la première, que le
pair retarde — deux fois par jeton, une fois par sens. Une ligne de code
(`set_nodelay(true)`, des deux côtés) divise l'attente par six.

### Et si le lien est lent ? Mesuré avec un relais retardateur

Localhost est un plancher optimiste : `tools/proxy_latence.py` ajoute un délai
par message et on refait le banc (256 jetons de vrai texte, 12 couches par nœud).

| latence ajoutée | attente du pair | rapport au calcul local | durée du banc | écart |
|---|---|---|---|---|
| 0 ms | 16,8 ms/jeton | 1,01× | 11,0 s | 0,00e0 |
| 5 ms | 33,0 ms/jeton | 1,99× | 15,1 s | 0,00e0 |
| 20 ms | 81,8 ms/jeton | 4,89× | 27,6 s | 0,00e0 |

La fidélité ne bouge pas d'un bit (0,00e0 partout : la latence ne change pas le
calcul, elle change le temps). Et l'attente suit une droite simple :

```
attente ≈ calcul distant + 3,2 × (latence par message)
```

Le facteur 3,2 est le nombre de messages retardés par jeton dans ce banc (le flux
et sa réponse, dans les deux sens). **C'est la formule de la phase 3.3** :
le débit ne compte pas (0,25 Mbit/s suffisent), la latence compte quatre fois.

Application à Colab : un aller-retour de 60 ms donne 16 + 3,2 × 30 ≈ **112 ms par
jeton**, soit ~8 jetons/s au lieu de ~60 en local. Le découpage ne sert donc pas à
accélérer — il sert à faire tenir un modèle qui ne tient pas sur une machine, et
c'est ce que la démonstration devra montrer.

C'est aussi la réponse à la phase 3.3 : **le seuil de rentabilité est une
affaire de latence, pas de débit**. Par jeton, le flux pèse 3 623 octets (dense)
ou 1 989 (blocs à 68 % d'activité), et le calcul distant coûte 16 ms : le réseau
demande donc **moins de 1 Mbit/s par flux de jetons à 20 jetons/s**, ce qu'un
lien domestique fournit sans peine. Ce qui coûte, c'est l'aller-retour — et
seulement lui.
