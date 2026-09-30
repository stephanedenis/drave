# Le format de flux (DRVF) — spécification

Ce format sert **trois choses à la fois**, et c'est délibéré :

1. la **trace** d'exécution (`--trace-flux`) : ce qui s'est passé, couche par
   couche ;
2. le **rejeu** (`--flux-forcer`) : on réinjecte les activations enregistrées et
   le calcul repart de là ;
3. le **transport** (phase 3, `--flux-serveur` / `--ppl-reparti`) : ce qu'un nœud
   distant reçoit pour continuer le calcul.

Un seul format pour les trois, parce que ce sont les mêmes octets : une liste
d'activation est une liste d'activation, qu'elle aille sur le disque ou sur le
réseau.

## Fichier (trace, `.bin`)

```
en-tête   "DRVF"                    4 octets
          version      u16          = 2 (défaut) ou 3 (`DRAVE_TRACE_BLOCS=1`)
          n_couches    u32
          cachés       u32
liste     couche       u16          < 1000 : entrée d'attention
                                    >= 1000 : entrée de FFN (couche - 1000)
          jeton        u32          COMPTEUR GLOBAL de jeton, pas la position
          n_actifs     u32
          échelle      f32
          puis n_actifs × ( indice u32 · valeur i16 )           [version 1]
          puis n_actifs × ( écart u8 · valeur i16 )             [version 2]
                l'écart de 255 annonce l'indice ABSOLU sur les deux octets suivants
fin       sentinelle   u16          0xFFFF (optionnelle : la fin de fichier suffit)
```

Taille : `14 + 6 × n_actifs` en v1, `14 + 3 × n_actifs` en v2. Mesuré sur une
trace **dense** : **6,02 octets par neurone actif** en v1, **3,01** en v2 ; sur une
trace creuse (39,9 % d'activité) : 6,04 et 3,04 — deux centièmes de plus, parce que
l'en-tête de liste de 14 octets pèse alors sur trois fois moins de neurones.

### Version 2 : les indices par écarts

La liste est triée, donc l'écart au neurone précédent tient sur **un octet** dans
99,9997 % des cas (22 échappements sur 8 790 000 mesurés). Trois octets par
neurone actif au lieu de six, et c'est du RANGEMENT, pas de la perte :

| | version 1 | version 2 |
|---|---|---|
| trace dense, 512 jetons | 132 396 736 o | **66 370 408 o (−49,87 %)** |
| rejeu (`--flux-forcer`) | 19,3885 | **19,3885 — identique** |
| listes · neurones actifs | 24 576 · 22 008 776 | identiques (relus par Python) |

### Version 3 : valeurs i8 et échelle f16 par bloc (`DRAVE_TRACE_BLOCS=1`)

Encore une échelle par **bloc de 32 canaux**, mais en f16, et des valeurs sur un
octet. C'est **avec perte**, donc la v3 n'est pas le défaut :

| | version 2 | version 3 |
|---|---|---|
| trace dense, 512 jetons | 66 370 408 o | **45 079 930 o (−32,1 %)** |
| rejeu `--flux-forcer` | 19,3885 | **19,4029 (+0,074 %)** |
| neurones actifs | 22 008 776 | 21 630 645 (−1,7 % : les valeurs qui s'arrondissent à zéro ne sont pas écrites) |
| erreur par valeur | nulle | RMS **0,085 %** du max de la liste (max 0,394 %) |

Le rejeu par LOTS n'accepte pas la v3 (il réinjecte les entiers d'origine, que la
v3 n'a plus) : il le dit au lieu de compter des listes manquantes en silence.

Le lecteur lit **les trois versions** (1, 2 et 3) ; une version inconnue est refusée en la
nommant. Le rejeu annonce désormais ce qu'il a servi — `24 576 listes servies,
0 manquantes` — parce qu'une trace dont les clés ne correspondent plus se
rejouait en silence avec une perplexité fausse.

## Le point qui a coûté un bug

`jeton` est un **compteur global**, pas la position dans la fenêtre de contexte.
Corollaire à connaître : avec `--depuis` (fenêtres qui se recouvrent), un même
jeton traité dans deux fenêtres consomme DEUX clés — une trace ne se rejoue donc
qu'avec la même configuration de fenêtres. C'est dit ici parce que c'est le seul
cas où la clé n'est pas une simple fonction du jeton.
Avec la position, deux fenêtres réécrivaient les mêmes clés `(couche, position)`
et le rejeu rejouait la mauvaise : perplexité **356 694** au lieu de 17,43. Le
format sur le disque n'a pas changé ; c'est la sémantique du champ qui est
maintenant explicite — et c'est exactement le genre de précision qu'une
spécification doit porter.

## Transport (phase 3, TCP) — protocole v5

```
en-tête (79 octets, identique à l'aller et au retour)
          magie        u32          0x44525631 (« DRV1 »)
          version      u8           5   (refusée si différente, en le disant)
          mode         u8           0 = f32 dense · 1 = liste quantifiée
                                    2 = listes à échelle par bloc · 3 = LOT dense
                                    4 = LOT en listes (mode 2 répété par état)
          couche_debut u32
          couche_fin   u32
          position     u32
          n            u32          dimension (mode 0) ou actifs (mode 1)
          échelle      f32          mode 1 uniquement
          niveaux      f32          ┐
          seuil        f32          │ le CONTRAT D'ACTIVATION : ces réglages
          top-k        u32          │ changent les chiffres, donc ils voyagent —
          renorm       u8           │ et le client impose les siens au serveur
          7 × top-k    u32          │ (q, k, v, o, gate, up, down)
          attn_top-k   u32          │
          q·k top-k    u32          │
          moe top-k    u32          ┘
corps     mode 0 : n × f32
          mode 1 : n × ( indice u16 · valeur i16 )
          mode 2 : n_blocs u32 · n_blocs × f32 · longueur u32 · paires
          mode 3 : n × dimension × f32   (n = nombre d'ÉTATS, pas de canaux)
          mode 4 : n × [ a_j u32 · n_blocs_j u32 · longueur_j u32 ·
                         n_blocs_j × f32 (échelles) · longueur_j octets de paires ]
```

Le **mode 4 est le même lot, en listes** : chaque état est encodé comme le mode 2
(indices par écarts, valeurs i8, une échelle f32 par bloc de 32 canaux) et
auto-délimité par ses trois tailles, lues avant toute allocation. Mesuré à 256
jetons, 16 par lot, seuil 0,01 : **1,5 ko par jeton au lieu de 3,5** (÷2,3) pour
un écart de **3,03e-2** — le mode est avec perte, comme le mode 2, et le critère
est qu'il ne coûte pas plus de 1,5 fois celui-ci. Un mode inconnu est refusé
**avant** toute lecture de corps (il l'était après, donc désynchronisé).

Le **mode 3 est le préremplissage réparti** : `n` états d'un coup, la position
étant celle du premier jeton du lot. La dimension ne voyage pas — chaque nœud la
connaît par son modèle, et les deux doivent charger le **même GGUF**. Mesuré :
256 jetons en **4 lots** de 64 (écart **0,00e0** avec la référence locale découpée
de la même façon), ou en **1 seul lot de 917 583 octets** — un aller-retour pour
tout un préremplissage, au lieu d'un par jeton. Réserve honnête : le lot voyage en
f32 dense (3,5 ko par jeton) ; le lot en listes est le mode 4, pas encore écrit.

Le **mode 1 est le format du disque**, à l'octet près : deux octets d'indice,
deux octets de valeur, une échelle par liste. Transporter la liste plutôt que le
vecteur dense, c'est le sujet même de la phase 3 — « des listes, pas des
matrices » vaut aussi sur le câble. La réponse est encodée **comme la demande** :
un pair qui parle en listes reçoit des listes, il n'y a pas deux réglages à
garder cohérents entre deux machines.

La version est dans **chaque** en-tête, et un pair d'une autre version est refusé
avec un message qui nomme les deux versions en présence :

```
[flux] arrêt : flux en version 99, cette build parle la 4 (pair incompatible : rien n'a été interprété)
```

Le passage de la version 2 à la 3 n'est pas cosmétique : un pair en version 2 qui
recevrait un lot lirait `n × 4` octets d'un corps qui en fait `n × dimension × 4`,
se désynchroniserait, puis dirait « mode inconnu » — un refus exact mais tardif et
muet sur la cause.

C'est le critère de la phase 3.5 : pas de silence, pas de devinette.

Le mode dense coûte **3 663 octets par flux** (79 d'en-tête + 896 × 4) pour
Qwen2.5-0.5B ; le mode liste coûte 79 + 4 × (nombre d'actifs) et le mode blocs
79 + 4 + 112 + 4 + 2 × actifs, donc ils gagnent dès que l'activité descend — le
mode blocs gagne même à pleine activité depuis que ses indices sont des écarts.

Les chiffres mesurés de `reports/rapport-transport-liste.md` datent d'un en-tête
de **39 octets** (protocole v3, avant les top-k) : ajouter 40 octets par flux pour
avoir les valeurs d'aujourd'hui — négligeable devant 3 663, mais écrit ici pour
que personne ne compare deux tableaux de deux époques.

### Qui applique la norme finale (règle, pas détail)

Un flux qui circule est un **résidu brut**. La norme finale n'appartient qu'au
nœud qui possède la tête de sortie, et elle s'applique **une fois**. Le nœud
moteur le déclare par un drapeau explicite (`flux_brut`) plutôt que de le déduire
de sa plage de couches : « ma plage va jusqu'à la dernière couche » et « je dois
normer » sont deux choses différentes, et les confondre a coûté la fidélité du
découpage (798,3 au lieu de 18,2).

## Invariants vérifiés

| invariant | comment il est vérifié |
|---|---|
| deux implémentations indépendantes lisent le même fichier | Rust (`--trace-flux`) et Python (`tools/flux_codec.py`) : aller-retour **identique** en v1 (132 396 736 octets) et en v2 (24 576 listes, 22 008 776 actifs des deux côtés) |
| un rejeu redonne le même résultat | `--flux-forcer` : perplexité **19,3885** avec et sans rejeu (chemin par jeton), **17,4294** (chemin par lots) |
| la fidélité de l'encodage est chiffrée | `DRAVE_FLUX_VERIF=1` : écart relatif **1,5e-5**, soit la quantification 16 bits |
| la taille suit l'activité | densité ÷2,3 → trace ÷2,5 (132 Mo → 53 Mo) |
| une version inconnue est refusée | v1/v2/v3 lues, toute autre refusée en la nommant ; le rejeu ANNONCE ses comptes (`N servies, M manquantes`) |
| le découpage ne change pas le résultat | deux processus, 12 couches chacun : écart local/réparti **0,00e0** (144,8289 = 144,8289), 39 puis 199 flux (le dernier jeton n'est pas envoyé) |
| un lot ne change pas le résultat non plus | 256 jetons en 4 lots de 64 : écart **0,00e0** (18,0851 = 18,0851) ; en 1 lot de 256 : **0,00e0** (918 ko sur le fil) |
| les deux nœuds quantifient PAREIL | un serveur lancé avec `--topk-q 900` et un client avec `--topk-q 4` donnent quand même **0,00e0** : les réglages du client gagnent — vérifié le 30/09 après `d59d061`, la première vérification (avant le correctif) était tautologique |
| l'en-tête fait exactement `TAILLE_TETE` octets | `assert_eq!` dans les deux émetteurs — un octet de trop décale tout le corps en silence et ne se voit qu'au flux suivant |
