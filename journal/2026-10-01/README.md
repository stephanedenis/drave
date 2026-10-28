# 2026-10-01

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-10-01/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**81 commits** · **8 session(s)** · **9 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| attention | 8 | [attention.md](attention.md) |
| distribue | 7 | [distribue.md](distribue.md) |
| docs | 15 | [docs.md](docs.md) |
| memoire | 8 | [memoire.md](memoire.md) |
| mesures | 11 | [mesures.md](mesures.md) |
| modele | 13 | [modele.md](modele.md) |
| moteur | 17 | [moteur.md](moteur.md) |
| outils | 1 | [outils.md](outils.md) |
| portes | 1 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `11b2d312-9a7e-4a4e-814f-ed0384ed9d4d` | Tu es relecteur ADVERSARIAL autonome | 2026-10-01 02:50 | 0.1 h | [rapport](../sessions/11b2d312-9a7e-4a4e-814f-ed0384ed9d4d/rapport.md) · [digest](../sessions/11b2d312-9a7e-4a4e-814f-ed0384ed9d4d/digest.md) |
| `13446299-79d8-497c-ba83-673c176a4637` | Tu es relecteur ADVERSARIAL autonome | 2026-10-01 00:54 | 0.2 h | [rapport](../sessions/13446299-79d8-497c-ba83-673c176a4637/rapport.md) · [digest](../sessions/13446299-79d8-497c-ba83-673c176a4637/digest.md) |
| `18c3f6d0-5bb1-45bb-9f94-ab0e7812218d` | Relecture ADVERSARIALE ciblée (10 minut | 2026-10-01 05:20 | 0.1 h | [rapport](../sessions/18c3f6d0-5bb1-45bb-9f94-ab0e7812218d/rapport.md) · [digest](../sessions/18c3f6d0-5bb1-45bb-9f94-ab0e7812218d/digest.md) |
| `6551e4dc-b73d-4df7-8fc4-b8c9fdbb0688` | Tu es un relecteur adverse. | 2026-10-01 11:57 | 0.1 h | [rapport](../sessions/6551e4dc-b73d-4df7-8fc4-b8c9fdbb0688/rapport.md) · [digest](../sessions/6551e4dc-b73d-4df7-8fc4-b8c9fdbb0688/digest.md) |
| `8288d350-b68e-4245-b903-5ef6d71910b4` | You are doing an ADVERSARIAL | 2026-10-01 05:52 | 0.1 h | [rapport](../sessions/8288d350-b68e-4245-b903-5ef6d71910b4/rapport.md) · [digest](../sessions/8288d350-b68e-4245-b903-5ef6d71910b4/digest.md) |
| `8a0aa6e5-1a5e-450f-a6ea-070eed249d63` | Tu es un relecteur adverse. | 2026-10-01 11:15 | 0.2 h | [rapport](../sessions/8a0aa6e5-1a5e-450f-a6ea-070eed249d63/rapport.md) · [digest](../sessions/8a0aa6e5-1a5e-450f-a6ea-070eed249d63/digest.md) |
| `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` | Continue avec REPRISE.md | 2026-09-28 14:46 | 222.5 h | [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md) |
| `ff364db0-d28f-47eb-973e-f13bdafd35a2` | Relecture ADVERSARIALE de clôture, dans | 2026-10-01 05:50 | 0.1 h | [rapport](../sessions/ff364db0-d28f-47eb-973e-f13bdafd35a2/rapport.md) · [digest](../sessions/ff364db0-d28f-47eb-973e-f13bdafd35a2/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:54 | `09adea5a` | Le k est un réglage : 0/3 au milieu à k=512, 3/3 à k=1024 (trois fenêtres par point) |
| 01:07 | `1425c79c` | Revue du sprint 4 : « trois fenêtres » étaient trois fois la même invite, et la portée du k était surestimée |
| 01:18 | `b14e4f28` | Contrôle dense à 8 192 : l'information est retrouvée (1002 s, prompt de 7963 jetons) — la question du k vs contexte est mesurable là |
| 01:37 | `9017f482` | Sprint 4 : cérémonie (le k est un réglage, la leçon des trois répétitions, planning du sprint 5) |
| 01:40 | `ee595197` | Pourquoi --lot 1 diffère de --lot 256 : 7e-4 nat par position, top-1 identique partout — c'est une amplification chaotique, pas un chemin faux |
| 02:20 | `508d3d87` | Grille refaite sur trois VRAIS textes : k=256 échoue 1 fois sur 3, pas 3 sur 3 |
| 02:49 | `0d50e756` | À 8 192 clés, k=1024 (12,5 %) suffit : le k nécessaire croît plus lentement que le contexte (deux points) |
| 02:58 | `a3691a53` | Revue du sprint 5 : la section 8 192 manquait, et « au plus » dépassait la mesure d'un facteur 10 |
| 03:37 | `13a5c9cc` | Sprint 5 : cérémonie (le taux remplace le verdict, la revue adverse, le pas de fenêtre corrigé) |
| 03:38 | `783f1f94` | Sprint 6 : le taux de récupération (9 fenêtres × 3 chemins) et le point 16 384 |
| 04:59 | `e4b3ebc5` | Le taux par fenêtre : 9 fenêtres contiguës, 8/9 en attention complète, et le mur du préremplissage |
| 05:25 | `361c1863` | Nuance : le facteur de ralentissement est un minorant (les deux exécutions à ctx 4608 n'ont jamais fini ; la même fenêtre rend en 85,1 s à ctx 5120) |
| 05:33 | `45a0c440` | Le « ralentissement » est un LIVELOCK : KvCache::assurer boucle sans fin si besoin > ctx (model.rs:1117) |
| 05:39 | `3209dc50` | Sprint 6 : cérémonie (le taux par fenêtre, le livelock du contexte, planning du sprint 7) |
| 05:46 | `c7fd7ea7` | REPRISE : le livelock corrigé, et le bilan des six résultats de la nuit |
| 05:46 | `32951e95` | Le livelock du contexte est corrigé : troncature annoncée au lieu d'une boucle infinie |
| 05:49 | `b3cba4c2` | README et REPRISE : prochaines étapes et compteur de lignes après la nuit |
| 06:09 | `1b9808e6` | Le correctif du livelock finissait en SIGABRT : c'est corrigé, et vérifié par le code de sortie |
| 06:53 | `17282a7e` | Le résultat de la nuit : à k=256 le taux est le MÊME que l'attention complète (8/9), et les échecs sont sur d'autres fenêtres |
| 07:06 | `beacdf96` | DeepSeek-V4.1-Flash : pas de poids ouverts — c'est DeepSeek-V4-Flash qui est téléchargé, et le plan d'adaptation est écrit |
| 07:40 | `2a7e6da8` | Sprint 7 : cérémonie (livelock corrigé deux fois, le taux final 8/9 = 8/9, et DeepSeek-V4-Flash téléchargé) |
| 07:40 | `e7db33bc` | DeepSeek-V4-Flash téléchargé (86,9 Go, 3 shards) : architecture et tokenizer lus depuis le shard 1, 784 tenseurs depuis le shard 2 — il manque le lien entre les deux |
| 07:41 | `dada3f61` | Journal : index des sessions (clôture de la nuit) |
| 07:44 | `836f4de7` | Journal : index des sessions (fin de nuit) |
| 09:40 | `b83d284f` | Découpage des MoE : la fréquence suffit, la co-activation n'ajoute rien (accord 1,000) |
| 09:42 | `aea1b10c` | Politique de stockage : la bibliothèque brute sur le mécanique, le NVMe pour nos artefacts (mesures à l'appui) |
| 09:42 | `e9cc44f6` | Modèles lourds : file de 1,14 To en téléchargement, plan écrit, état honnête |
| 10:08 | `7c1b9ff9` | Convertisseur GGUF → modèle éclaté en clusters : un fichier par cluster, vérifié par empreintes |
| 11:14 | `3eb0af71` | Un modèle éclaté se lit comme un seul : lecteur multi-fichiers, shards et clusters |
| 11:39 | `8f55e4fd` | Clusters exécutables : origine 15,2789 = clusters 15,2789, et les défauts trouvés en chemin |
| 11:56 | `b24a2e6e` | mmap (3,3x plus rapide, 3x moins de mémoire) et nœud partiel (2,36 Go pour un huitième des experts) |
| 11:58 | `6a2dfcb6` | Journal du bloc : mmap, nœud partiel, et le défaut prédit par la revue confirmé en vrai |
| 12:04 | `1ab1b697` | Cérémonie du sprint 08 : quatre objectifs, deux nés de la preuve d'exécution |
| 12:11 | `400047e3` | Rapports et sprint : les cinq défauts de la revue n°2 et le test qui manquait |
| 12:11 | `f98816d8` | Revue adverse : un défaut bloquant silencieux, et le test qui manquait au correctif |
| 12:15 | `9eea40b4` | La table des types ggml confrontée à libggml, et les huit types ajoutés après NVFP4 |
| 12:18 | `907e5c32` | Journal : inventaire des modèles lourds et vérificateur de table dans REPRISE |
| 12:18 | `8a2ff796` | Porte gpt-oss verte sur le binaire final : 15,1757 avec mmap, 21 minutes |
| 12:18 | `ae4531bf` | Inventaire des modèles lourds : 984 Go de poids annoncés par les descripteurs, 984 Go annoncés par HuggingFace |
| 12:19 | `4a4f8943` | Journal automatique |
| 12:21 | `73b2c1fd` | Courbe du nœud partiel : 1, 2, 4, 8 clusters — perplexité et mémoire |
| 12:35 | `d8700ae4` | Chaîne complète par les outils du dépôt : convertisseur -> clusters -> 15,2789 |
| 12:36 | `8e3198ab` | La file de 1 138 Go est terminée : 1 163 Go de modèles lourds, tous complets et lisibles |
| 12:36 | `ae9de47b` | Journal |
| 12:36 | `56a65246` | Journal de session |
| 17:42 | `c7c602d9` | L'empreinte memoire de DeepSeek-V4.1 : 365,7 Go -> 50-80 Go, et ce n'est pas en decoupant les experts |
| 17:43 | `a6c18ac5` | Journal |
| 17:43 | `418b5325` | Sprint 09 : ceremonie (onze pistes mesurees, trois retenues) |
| 17:43 | `65860083` | Trois dernieres pistes mesurees et ecartees : localite temporelle, ordre des experts, prechargement |
| 18:04 | `35aceacb` | Rejouer notre propre journal : notre usage ne change pas l'empreinte, la langue si |
| 18:08 | `27a642c5` | Analyse couche par couche du journal : il se place entre le francais et l'anglais |
| 18:09 | `4b6b225b` | Journal |
| 20:17 | `dcf6d65d` | REPRISE : analyse statique des poids |
| 20:17 | `958eb293` | Analyse statique : les experts sont orthogonaux, mais la periodicite de 12 est dans les POIDS |
| 20:54 | `679a26e4` | REPRISE : architecture memoire |
| 20:54 | `ed832cea` | Architecture memoire : ou mettre quoi, et le KV qu'on oubliait |
| 21:08 | `3b2e0d81` | CPU, hyperthreading, NUMA et NVMe : mesures, et la conclusion qui se retourne |
| 21:13 | `4dc1c577` | README : la topologie et la conclusion qui se retourne |
| 21:13 | `887d7514` | Topologie materielle : NVLink 25,8 Go/s, NUMA negligeable, pas de FPGA |
| 21:21 | `3de46239` | Paires hyperthread : +27 % quand les cœurs manquent, rien quand on les a tous |
| 21:22 | `d79f934c` | REPRISE : topologie materielle et affinites |
| 21:37 | `b2bc093b` | Detection materielle et heuristiques de configuration automatique |
| 21:39 | `954e0861` | Prelecture parallele : implementee, mesuree, sans effet (0,3 %) |
| 21:55 | `2d4738fd` | Tete restreinte a une liste de tokens : +15 %, mais la sortie change |
| 22:16 | `302fc88d` | Restreindre la tete de sortie : trois voies explorees, une seule survit |
| 22:21 | `8b1c0b9c` | Rapport : detection materielle et configuration automatique |
| 22:24 | `3372be41` | Plan materiel sensible au modele : il lit ses dimensions au lieu de les supposer |
| 22:26 | `60e19582` | mmap : 365,7 Go adresses en 0,08 s et 47 Mo de RSS |
| 22:31 | `6e38babe` | REPRISE : session d'implementation (detection materielle, heuristiques, engram) |
| 22:31 | `65036ddb` | Defauts de threads : les cœurs physiques, sans le 3/4 ni le /2 |
| 22:32 | `0c6bca8f` | Aide du moteur : les modes recents, et ce que chacun ne fait pas |
| 22:33 | `7c8899ad` | Materiel : distinguer dense et MoE (un modele dense affichait « 0 experts de 9,95 Mo ») |
| 22:38 | `8f936ee9` | tools/portes.sh : les portes du depot en une commande, comparees a leur valeur publiee |
| 22:41 | `5ba051f8` | Materiel : estimation du cout par jeton, d'apres les debits mesures |
| 22:47 | `f9a143bc` | Prelecture : quatrieme mecanisme mesure, quatrieme fois sans effet |
| 22:53 | `42917284` | Q2_K : dequantification implementee et verifiee contre ggml |
| 22:59 | `aa92cfc7` | IQ2_XXS : 93 Go de V4.1 debloques, et un bug que la lecture n'aurait pas vu |
| 23:02 | `0358eec9` | IQ1_M : 61 Go de DeepSeek-V4-Flash debloques (ecart 0,00e+00 avec ggml) |
| 23:04 | `f041ce67` | BF16 : lu et verifie (le f32 tronque a ses 16 bits de poids fort, exactement) |
| 23:29 | `dbae4f8e` | formats : Q5_K, Q5_0/1, Q3_K, IQ3_XXS, IQ1_S, IQ4_XS — et MXFP4 corrigé d'un facteur 2 |
| 23:49 | `475bee4d` | routage des experts : quatre conventions, facteur d'échelle, routage par table |

## Le récit de la journée (écrit à la main)

<!-- notes -->

<!-- /notes -->
