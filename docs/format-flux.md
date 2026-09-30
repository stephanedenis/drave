# Le format de flux (DRVF v1) — spécification

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
          version      u16          = 1
          n_couches    u32
          cachés       u32
liste     couche       u16          < 1000 : entrée d'attention
                                    >= 1000 : entrée de FFN (couche - 1000)
          jeton        u32          COMPTEUR GLOBAL de jeton, pas la position
          n_actifs     u32
          échelle      f32
          puis n_actifs × ( indice u32 · valeur i16 )
fin       sentinelle   u16          0xFFFF (optionnelle : la fin de fichier suffit)
```

Taille : `14 + 6 × n_actifs` octets par liste. Mesuré : **6,02 octets par neurone
actif**, et 505 ko par jeton sur une exécution dense (deux listes par couche).

## Le point qui a coûté un bug

`jeton` est un **compteur global**, pas la position dans la fenêtre de contexte.
Avec la position, deux fenêtres réécrivaient les mêmes clés `(couche, position)`
et le rejeu rejouait la mauvaise : perplexité **356 694** au lieu de 17,43. Le
format sur le disque n'a pas changé ; c'est la sémantique du champ qui est
maintenant explicite — et c'est exactement le genre de précision qu'une
spécification doit porter.

## Transport (phase 3, TCP) — protocole v3

```
en-tête (26 octets, identique à l'aller et au retour)
          magie        u32          0x44525631 (« DRV1 »)
          version      u8           4   (refusée si différente, en le disant)
          mode         u8           0 = f32 dense · 1 = liste quantifiée
                                    2 = listes à échelle par bloc · 3 = LOT
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
```

Le **mode 3 est le préremplissage réparti** : `n` états d'un coup, la position
étant celle du premier jeton du lot. La dimension ne voyage pas — chaque nœud la
connaît par son modèle, et les deux doivent charger le **même GGUF**. Mesuré :
256 jetons en **4 lots** de 64 (écart **0,00e0** avec la référence locale découpée
de la même façon), ou en **1 seul lot de 917 543 octets** — un aller-retour pour
tout un préremplissage, au lieu d'un par jeton. Réserve honnête : le lot voyage en
f32 dense (3,5 ko par jeton) ; le lot en listes est le mode 4, pas encore écrit.

Le **mode 1 est le format du disque**, à l'octet près : deux octets d'indice,
deux octets de valeur, une échelle par liste. Transporter la liste plutôt que le
vecteur dense, c'est le sujet même de la phase 3 — « des listes, pas des
matrices » vaut aussi sur le câble. La réponse est encodée **comme la demande** :
un pair qui parle en listes reçoit des listes, il n'y a pas deux réglages à
garder cohérents entre deux machines.

La version est dans **chaque** en-tête, et un pair d'une autre version est refusé
avec un message qui nomme les deux versions :

```
[flux] arrêt : flux en version 99, cette build parle la 4 (pair incompatible : rien n'a été interprété)
```

Le passage de la version 2 à la 3 n'est pas cosmétique : un pair en version 2 qui
recevrait un lot lirait `n × 4` octets d'un corps qui en fait `n × dimension × 4`,
se désynchroniserait, puis dirait « mode inconnu » — un refus exact mais tardif et
muet sur la cause.

C'est le critère de la phase 3.5 : pas de silence, pas de devinette.

Le mode dense coûte **3 620 octets par flux** (26 d'en-tête + 896 × 4) pour
Qwen2.5-0.5B ; le mode liste coûte 26 + 4 × (nombre d'actifs), donc il gagne dès
que l'activité descend sous 100 %. Les deux sont mesurés côte à côte dans
`reports/rapport-transport-liste.md`.

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
| deux implémentations indépendantes lisent le même fichier | Rust (`--trace-flux`) et Python (`tools/flux_codec.py`) : aller-retour **identique** sur 132 396 736 octets |
| un rejeu redonne le même résultat | `--flux-forcer` : perplexité **19,3885** avec et sans rejeu (chemin par jeton), **17,4294** (chemin par lots) |
| la fidélité de l'encodage est chiffrée | `DRAVE_FLUX_VERIF=1` : écart relatif **1,5e-5**, soit la quantification 16 bits |
| la taille suit l'activité | densité ÷2,3 → trace ÷2,5 (132 Mo → 53 Mo) |
| le découpage ne change pas le résultat | deux processus, 12 couches chacun : écart local/réparti **0,00e0** (144,8289 = 144,8289), 40 puis 199 flux |
| un lot ne change pas le résultat non plus | 256 jetons en 4 lots de 64 : écart **0,00e0** (18,0851 = 18,0851) ; en 1 lot de 256 : **0,00e0** (918 ko sur le fil) |
| les deux nœuds quantifient PAREIL | un serveur lancé avec `--topk-q 900` et un client avec `--topk-q 4` donnent quand même **0,00e0** : les réglages du client gagnent (vérifié) |
| l'en-tête fait exactement `TAILLE_TETE` octets | `assert_eq!` dans les deux émetteurs — un octet de trop décale tout le corps en silence et ne se voit qu'au flux suivant |
