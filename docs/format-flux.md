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

## Transport (phase 3, TCP)

```
requête   magie        u32          0x44525631 (« DRV1 »)
          couche_debut u32
          couche_fin   u32
          position     u32
          dimension    u32
          puis dimension × f32
réponse   même en-tête, puis dimension × f32
```

Le flux voyage en **f32** sur le réseau alors qu'il est quantifié sur le disque :
c'est un choix de simplicité pour le banc d'essai, pas une obligation — la version
quantifiée du transport est ce que la phase 3 devra mesurer (octets par jeton ×
latence).

## Invariants vérifiés

| invariant | comment il est vérifié |
|---|---|
| deux implémentations indépendantes lisent le même fichier | Rust (`--trace-flux`) et Python (`tools/flux_codec.py`) : aller-retour **identique** sur 132 396 736 octets |
| un rejeu redonne le même résultat | `--flux-forcer` : perplexité **19,3885** avec et sans rejeu (chemin par jeton), **17,4294** (chemin par lots) |
| la fidélité de l'encodage est chiffrée | `DRAVE_FLUX_VERIF=1` : écart relatif **1,5e-5**, soit la quantification 16 bits |
| la taille suit l'activité | densité ÷2,3 → trace ÷2,5 (132 Mo → 53 Mo) |
