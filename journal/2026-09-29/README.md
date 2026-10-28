# 2026-09-29

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-09-29/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**68 commits** · **1 session(s)** · **8 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| attention | 10 | [attention.md](attention.md) |
| distribue | 2 | [distribue.md](distribue.md) |
| divers | 1 | [divers.md](divers.md) |
| docs | 16 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 6 | [mesures.md](mesures.md) |
| modele | 5 | [modele.md](modele.md) |
| moteur | 27 | [moteur.md](moteur.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` | Continue avec REPRISE.md | 2026-09-28 14:46 | 222.5 h | [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 07:08 | `f04f0589` | Item 1 : protocole de perplexite longue --depuis N |
| 07:23 | `51a14a0b` | Item 3 : cache KV quantifie int8 et int4 empaquete |
| 07:36 | `37266bd9` | Item 5 : echelles par bloc pour DenseQ8 -- hypothese refutee |
| 07:48 | `aa70d548` | Item 6 : une seule analyse de la ligne de commande pour les quatre modes |
| 08:55 | `21ac631d` | Item 7 (1/2) : noyau GPU une warp par ligne, la tete redevient deportable |
| 09:46 | `fba67b61` | Item 4 : prefill par lots -- justesse corrigee, debit a mesurer au calme |
| 10:01 | `0dc505a7` | Rapport localite d'activation (idees PowerInfer mesurees) + etat des 8 chantiers |
| 10:08 | `3091473d` | Item 7 (2/2) : noyaux GPU 4 bits -- MXFP4 et Q4_K, une warp par ligne |
| 10:36 | `5719501b` | Item 4 : MoE par lots -- regroupement des jetons par expert |
| 11:02 | `aef0b8aa` | Plan 1 M : etat reel des six etapes et ce qui se mesure tout de suite |
| 11:02 | `72fbe30a` | Item 2 : le seuil de rotation, tranche par une comparaison appariee |
| 11:31 | `6a64b354` | Item 3 : KV quantifie mesure aussi a 4 600 jetons, et compare a llama.cpp |
| 11:57 | `fd695bc5` | Item 8 : premiers resultats d'attention creuse (et ils sont opposes) |
| 12:09 | `71dbcf5c` | Item 4 : le GEMM sur le pool, et le gain reel attribue poste par poste |
| 12:15 | `b9ba6ce5` | REPRISE : toutes les mesures du tour huit chantiers, et la suite ordonnee |
| 12:20 | `25893301` | Aiguille : le 0.5B echoue 6 fois sur 6 (limite du modele, pas du moteur) |
| 12:41 | `833a843d` | Aiguille : test arrete, et pourquoi (remplissage trop repetitif, prefill trop lent) |
| 12:41 | `26b75874` | KV a echelles par bloc de 32 : int8 de +7,1 % a +1,5 %, int4 de +384 % a +219 % |
| 13:06 | `98cdf1bf` | KV par bloc : mesure longue (4 591 jetons) -- int8 +3,4 %, int4 +287 % |
| 13:54 | `2383eaea` | préremplissage par lots : attention groupée, tête en lot, et un pointeur gras |
| 14:06 | `f5788625` | noyau Q6_K sur GPU, et tête Q6_K déportée dans le moteur |
| 14:29 | `bc168979` | E4 : KV déporté en VRAM, attention sur le GPU, mesuré à 1 M de clés |
| 14:30 | `8438883b` | docs: préciser que QT_GPU_KV exige QT_GPU (le pilote ne s'ouvre que sur QT_GPU) |
| 14:32 | `a5936037` | docs E4 : comment le noyau d'attention a été validé (cas dégénérés, trois bugs) |
| 14:44 | `e6a5effd` | KV déporté : corriger la copie du chemin par lots |
| 15:45 | `19535755` | rotation : le seuil de bascule à 4 096 était trop bas (mesuré à 5 120) |
| 16:53 | `91ebee72` | journal : archive automatique |
| 16:53 | `54f9fa61` | KV quantifié mesuré à 8 192 jetons, la longueur de la comparaison llama.cpp |
| 16:55 | `b5ff0b1d` | E4 : miroir VRAM paginé (capacité doublée à la demande) |
| 17:05 | `45948e2d` | porte gpt-oss : préciser qu'elle se mesure SANS QT_GPU |
| 18:05 | `a64328d3` | GPU : dépaquetage vectorisé du noyau d'attention (×1,8 à ×2,3 à 1 M de clés) |
| 18:28 | `5dfa6b19` | Chantier 1-2 : aiguille v2, experts MXFP4 en VRAM, attention par lots déportée |
| 18:46 | `bc5aa9a6` | Chantier 3 : cache KV CPU paginé (0,03 Go à ctx 1 M au lieu de 25,77 Go) |
| 18:56 | `6664eef7` | REPRISE : feuille de route réécrite et pièges des variables d'environnement |
| 19:27 | `4512f697` | Chantiers 1, 2b, 2c : aiguille 12/12, attention par lots déportée ×2,8, experts +6 % |
| 19:31 | `38d4d8bd` | Chantiers 2d et 2e : noyau de tête AVX2, KV réparti sur les deux GPU |
| 19:39 | `c8661869` | docs : plan détaillé pour MLA et la vision (chantier 5) |
| 20:02 | `86ffc004` | journal : archive automatique |
| 20:04 | `660244ea` | MLA : le harnais est prêt (modèle synthétique + référence numpy) |
| 20:08 | `d5ee7a05` | MLA : le moteur retrouve la référence numpy à 5,2e-7 près |
| 20:09 | `2d173f1f` | vision : relevé du projecteur mmproj (paramètres et nommage réels) |
| 20:48 | `15170886` | Rotation à 16 384 jetons : le RoPE simple gagne encore (35,18 contre 1 133,02) |
| 20:49 | `a50a5a58` | vision : inventaire exact des tenseurs (et deux corrections du plan) |
| 20:51 | `2ca9e0d4` | Vision : l'embedding de patchs est fait et validé (5,4e-7 contre numpy) |
| 20:53 | `c165fcfd` | Vision : le projecteur est validé aussi (1,7e-6) — les deux extrémités du chemin image tiennent |
| 20:56 | `0c7d3166` | vision : détailler le pas suivant (couche, rotation 2-D, attention locale, injection) |
| 20:57 | `9cdc4aea` | Vision : une couche du ViT est validée aussi (1,8e-6) |
| 20:58 | `8c51fe41` | vision : une RÉFÉRENCE existe sur la machine (libmtmd d'ollama) |
| 21:01 | `7802cc85` | Vision : la tour entière tourne (32 couches + v.post_ln) |
| 21:05 | `43eee825` | Vision : le point d'injection des embeddings est en place |
| 21:06 | `6c5ed867` | vision : la structure de paramètres de libmtmd est sondée (l'ABI n'est plus un obstacle) |
| 21:07 | `0a6bca2c` | vision : le programme de référence va jusqu'au chargement du projecteur |
| 21:09 | `defd5fe0` | vision : mtmd va jusqu'au tokenize, qui échoue (état exact et hypothèses) |
| 21:10 | `301f65bb` | vision : deux hypothèses de plus testées sur mtmd_tokenize, aucune ne suffit |
| 21:11 | `1e9a350c` | vision : la fenêtre locale lue dans la source de llama.cpp (et la rotation localisée) |
| 21:11 | `93b5e6d4` | vision : l'API de mtmd est connue (en-tête récupéré), le blocage est nommé |
| 21:12 | `b032a366` | vision : la convention de rotation 2-D lue dans la source de llama.cpp |
| 21:13 | `8ba80509` | vision : la rotation 2-D est implémentée (quatre blocs, convention de clip.cpp) |
| 21:23 | `1961ea4b` | vision : le chemin image est complet (224 × 224 → 64 jetons de 3584 dimensions) |
| 21:24 | `7ec4cf90` | vision : le détail de la rotation lu dans ggml — mon implémentation est à corriger |
| 21:37 | `081c669a` | vision : rotation corrigée d'après ggml — et un défaut d'ordre mis au jour |
| 21:41 | `c13232dc` | vision : l'ordre du pipeline est corrigé — et la preuve est que le chiffre CHANGE |
| 21:46 | `c1c100eb` | vision : la rotation est confirmée par la source, et une variante de fenêtre découverte |
| 21:46 | `d084e437` | vision : la chaîne complète est démontrée, de l'image aux logits |
| 21:47 | `26af06ba` | REPRISE : l'item 3 (rotation) reflète la mesure à 16 k et le seuil porté à 4 × |
| 21:47 | `c6695f4e` | journal : archive automatique |
| 21:47 | `095e0933` | REPRISE : l'item 5 reflète l'état final (chaîne vision démontrée, réserves nommées) |
| 21:47 | `a42ebb3a` | REPRISE : MLA et vision tous deux faits, avec leurs réserves nommées |

## Le récit de la journée (écrit à la main)

<!-- notes -->

<!-- /notes -->
