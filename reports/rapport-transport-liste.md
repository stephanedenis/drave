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

D'où les deux suites possibles, par ordre de propreté :

* **transmettre l'entrée normée** de la première couche distante (le nœud
  distant saute sa propre norme d'entrée) : c'est ce que la trace fait déjà, et
  c'est bien conditionné ;
* **une échelle par bloc de 32 canaux** (comme le cache KV) au lieu d'une échelle
  par vecteur : même coût par valeur, erreur relative bornée par bloc, une
  centaine d'octets de plus par flux.

Aucune des deux n'est faite ici : ce rapport s'arrête à la mesure, et l'écrit.

## Ajouts de la session

* `--flux-liste` : le pilote envoie des listes ; le nœud moteur suit le mode reçu.
* **Version dans chaque en-tête** (3.5) : un pair en version 99 est refusé avec
  `flux en version 99, cette build parle la 2 (pair incompatible : rien n'a été
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

Configuration utilisable aujourd'hui : `--flux-blocs --act-thresh 0.01`.

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
16 % d'écart) ; mais **l'écart croît avec la longueur** — 0,2 % à 40 jetons
synthétiques, 2,7 % à 256 jetons de vrai texte à seuil 0,01, 14 % à 0,02. Une
erreur de flux se compose sur douze couches ET sur toute la séquence.

Donc la revendication honnête est : **÷1,6 sur le fil pour 2,7 %** à seuil 0,01,
et non « ÷2 pour 0,2 % ». Le vrai remède n'est pas le seuil, c'est le signal
transmis (voir les deux suites ci-dessus).

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

C'est aussi la réponse à la phase 3.3 : **le seuil de rentabilité est une
affaire de latence, pas de débit**. Par jeton, le flux pèse 3 623 octets (dense)
ou 1 989 (blocs à 68 % d'activité), et le calcul distant coûte 16 ms : le réseau
demande donc **moins de 1 Mbit/s par flux de jetons à 20 jetons/s**, ce qu'un
lien domestique fournit sans peine. Ce qui coûte, c'est l'aller-retour — et
seulement lui.
