# 2026-10-03

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-10-03/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**106 commits** · **1 session(s)** · **8 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| attention | 10 | [attention.md](attention.md) |
| distribue | 9 | [distribue.md](distribue.md) |
| docs | 27 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 10 | [mesures.md](mesures.md) |
| modele | 4 | [modele.md](modele.md) |
| moteur | 21 | [moteur.md](moteur.md) |
| portes | 24 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` | Continue avec REPRISE.md | 2026-09-28 14:46 | 222.5 h | [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:01 | `7f60f39c` | Sprint 18 : clôture (28 min) — deux noyaux AVX2 bit-exacts (Q2_K et IQ1_M), portes toutes vertes |
| 00:02 | `fc28f19c` | REPRISE : la nuit des optimisations (×3,54 sur la passe V4.1, 5 670 tenseurs prouvés identiques) et les deux pistes refusées par la mesure |
| 01:16 | `20de26e3` | Bloc 19 : première passe V4.1 de 1 024 jetons (1 023 notés, PPL 1 287 700,8239, 60,6 min, aucun incident) — et le profil par profondeur n'avait aucun drapeau |
| 01:17 | `b37088ad` | Sprint 19 : clôture (76 min) — la passe longue est passée, le profil par profondeur est réparé, et 63 tests verts |
| 01:18 | `be5d2a11` | Docs : le drapeau --ppl-profil n'est plus « inexistant » — l'avertissement de docs/vision.md, le glossaire et le rapport d'audit des drapeaux ignorés sont mis à jour |
| 01:20 | `17bbd8e9` | Rapport de la nuit : les trois leviers (×3,54 sur la passe V4.1), les preuves d'égalité, et les deux idées refusées par la mesure |
| 01:20 | `e8a351e5` | Cohérence : le rapport d'audit des docs est daté (quatre de ses trouvailles sont corrigées depuis) et le mode du champ n est écrit pour les cinq modes |
| 02:54 | `b5e7d9c8` | ⚠️ V4.1 ne prédit pas : top-1 0/31, NLL 11,657 nats (uniforme 11,770) — V4-Flash, lui, est juste (1,875 contre 1,844 pour llama.cpp) |
| 02:56 | `9250879b` | Sprint 20 : clôture (103 min) — la passe longue a livré son verdict : V4.1 ne prédit pas, V4-Flash est juste |
| 03:24 | `14c52ae7` | Localisation V4.1 : huit hypothèses éliminées par ablation, et le défaut est cerné au chemin partagé tel que V4.1 l'instancie |
| 03:32 | `98c3401b` | Localisation V4.1, suite : l'embarquement est exact (0,000e+00), le biais de routeur du texte est le bon, et la règle du retard est CONFORME à la source publiée |
| 03:34 | `05c2416d` | Journal : index de session à jour |
| 03:34 | `3252ec7a` | Sprint 21 : clôture (35 min) — douze hypothèses éliminées, quatre pièces vérifiées, le défaut cerné au chemin des experts |
| 03:34 | `e5ce21c6` | Localisation V4.1 : la tête (1e-4) et le routeur (sélection identique à la trace) sont vérifiés en numpy — il ne reste que la COMPOSITION des experts |
| 03:47 | `3f096a17` | Défaut silencieux corrigé : --abits au-delà de 16 saturait (et parfois enroulait) les activations i16 — facteur 256 muet |
| 03:49 | `08fbf237` | Deux vides neufs pour rendre le chemin des experts vérifiable : ffn_hn (entrée normée du MoE, vérifiée en numpy à 1e-7) et moe_down (somme des experts routés) |
| 03:57 | `50db1505` | Sprint 21 : portes toutes vertes après les changements du bloc (64 tests, V4-Flash 8430,4966 inchangée) |
| 04:06 | `82a2f7e3` | Le chemin des experts de V4.1 est VÉRIFIÉ en numpy (écart 4e-5) — il ne reste que la composition de l'attention |
| 04:10 | `2a96b148` | Attention V4.1 : projections et normes VÉRIFIÉES (1e-6), un écart isolé sur la rotation du Q — instrument fourni, conclusion suspendue |
| 04:11 | `3dfa69e3` | Attention V4.1, premiers étages TOUS vérifiés à 1e-6 — l'écart sur q_rope était une faute de MON script |
| 04:14 | `e79cb2dc` | Plan P7 : la porte de correction est IMPOSSIBLE en l'état et c'est nommé — llama.cpp refuse l'architecture deepseek41 ; ce qui est vérifiable sans référence exécutable l'est (tableau des douze vérifications) |
| 04:14 | `7401db81` | Le cœur de l'attention V4.1 est vérifié — blocs compressés et règle de visibilité compris (7e-07) |
| 04:18 | `859d2b7b` | Porte Drave de P6 : DEUX des quatre points ne tiennent pas — flux illisible par l'outil d'analyse, rejeu non identique (mesuré) |
| 04:19 | `314ff84d` | Porte Drave de P6, point 1 CORRIGÉ : l'outil d'analyse lit les trois versions du format DRVF, et la porte est branchée |
| 04:21 | `6faea8f2` | Porte Drave de P6, point 2 : le rejeu est DÉFINI et VÉRIFIÉ — 0 liste manquante, écart ≤ 1e-5, et la cause de l'écart est mesurée |
| 04:30 | `293051a7` | Porte de correction de P6, mesurée sur V4-Flash avec des protocoles ALIGNÉS : logits à 1-2 %, corrélations ≥ 0,9979 — mais la perplexité n'est pas le bon instrument |
| 04:39 | `38fb6782` | Porte de correction P6 serrée : 63 positions, corrélation 0,9852, top-1 88,9 %, PPL à 6,4 % |
| 04:43 | `e57cd157` | Sprint 22 : la composition de V4.1 est vérifiée pièce par pièce, et les deux portes de P6, exécutées, étaient fausses deux fois sur quatre |
| 04:48 | `02ff0bac` | La porte de correction devient un OUTIL exécutable, branché dans portes.sh (Qwen, 71 positions) |
| 04:52 | `fce7f490` | compare_logits.py : un diagnostic par TRANCHES, pour distinguer une erreur de position d'une erreur de tête |
| 04:57 | `170d2900` | Plan P6 : la fenêtre de 63 prédictions ne juge pas la perplexité (seuil à 64), et elle le dit |
| 05:03 | `5b121781` | Glossaire : la porte de correction a maintenant des critères mesurés, et le rejeu une définition vérifiée |
| 05:38 | `a252e71c` | Plan P6 : le coût du contexte long est mesuré (60 s/jeton à ctx 1024), et --dense est inerte pour V4-Flash |
| 05:38 | `1b52c5b4` | Sprint 23 : la porte de correction serrée (63 positions, 6,4 % au lieu de 25 %), outillée (verdict + code retour), et le coût du contexte long mesuré |
| 06:01 | `e90e6b41` | Porte de correction à ctx 256 (255 positions) : TENUE, mais elle a d'abord ÉCHOUÉ sur un point, et le critère a été révisé par la mesure |
| 06:07 | `11d80f44` | Plan et sprint 23 : le coût du contexte long est attribué à ce qui est MESURÉ (proj+mlp double, l'attention reste plate), l'empreinte des experts reste une hypothèse nommée |
| 06:50 | `0553b8d0` | DRAVE_SIMD_DOT : le produit scalaire des experts vectorisé — ×2,06 sur la passe, et l'écart qu'il introduit est MESURÉ |
| 07:54 | `0c9d70b7` | Rapport : disque ou CPU ? — la mesure dit que le deuxième NVMe n'accélérerait pas les passes actuelles |
| 08:17 | `1d459614` | GPU : le tandem NVLink est au repos sur la charge principale, et les chiffres disent pourquoi |
| 08:30 | `1aa234cb` | Sprint 25 : le « coût qui croît avec la position » était le DISQUE DUR, pas le moteur — protocole rejoué à l'identique sur NVMe |
| 09:11 | `78460b47` | CORRECTION : le gain du SIMD était annoncé ×2,06 ; l'A/B entrelacé donne ×1,18 (passe) et ×1,37 (proj+mlp) |
| 09:14 | `d13e3532` | Granularité des listes : elle ROUTE, elle ne compresse pas — mesuré sur les activations réelles de V4-Flash |
| 09:15 | `dba369fe` | Plan P6 : porte de correction TENUE à ctx 512 (511 positions, top-1 93,0 %, +4,3 % de PPL) et le coût par jeton ne croît presque pas avec le contexte (2,58 s/jeton contre 2,50 à ctx 64) |
| 09:28 | `8bce1b40` | Sprint 26 : porte de correction TENUE à ctx 512, coût par jeton quasi constant, granularité qui route — portes toutes vertes |
| 09:30 | `28d3c9ff` | REPRISE : état du 03/10 (porte à ctx 512, coût plat, SIMD corrigé, granularité) |
| 09:38 | `eb0f9bec` | Porte Drave de P1 enfin outillée : les 24 poids de connexion hc sont écrits, relus et jugés |
| 09:39 | `c67e4d01` | analyse_hc.py : le test synthétique a trouvé une faute d'axe (sommer les positions au lieu des colonnes) — corrigé, et les deux cas sont vérifiés (bistochastique -> 0, faux -> 1) |
| 09:43 | `c9b77544` | Porte Drave de P1 TENUE : mesurée, et elle révèle une structure — les 16 connexions de V4-Flash sont une PERMUTATION |
| 09:45 | `30ee8596` | Audit : les deux portes, phase par phase (P0 à P9) — ce qui est tenu, ce qui est impossible et nommé, ce qui reste à la demande |
| 09:48 | `4973c78d` | Plan : renvoi vers l'audit des deux portes, phase par phase |
| 09:50 | `42dee800` | HC : la permutation tient sur V4.1 et à toutes les positions (332/332), et V4.1 est encore plus proche de l'identité |
| 09:51 | `b058f7f4` | HC : ce que coûterait une simplification en permutation — 6,4 % d'erreur L2 moyenne (V4-Flash), 8,2 % (V4.1) sur 332 matrices ; l'ablation qui mesurerait l'effet modèle est nommée |
| 09:52 | `90709486` | Audit : préciser ce que « flux » veut dire pour V4 — les paires sont comptées (16,2 G/jeton) mais la part en listes est NULLE, le calcul est dense. Le contrat d'échange est tenu, pas encore l'unité de calcul |
| 10:10 | `7d5a8fd9` | Réorientation : plan Kimi-K3 — exécuter en local ce qui ne tient pas en local |
| 10:13 | `08ced099` | Retrait de V4-Flash : copie NVMe supprimée, porte hc repointée sur V4.1 (testée), section 6bis marquée ARCHIVÉE dans portes.sh |
| 10:24 | `ce409dd7` | Porte de correction à ctx 1024 (1 023 positions) : accord MEILLEUR (moyenne 0,9914, top-1 93,5 %, PPL +1,7 %), mais elle a d'abord échoué sur une position où la référence est certaine |
| 10:25 | `bd9b9363` | Sprint 27 : porte P1 fermée (et elle révèle une permutation), portes auditées P0-P9, porte à ctx 1024 tenue sous critère révisé, bascule vers Kimi-K3 |
| 10:27 | `3e2d7014` | Spécification de l'architecture Kimi-K3, tirée de la référence (llama.cpp-k3 + code publié) |
| 10:32 | `d96952d7` | --config et --tokenize répondent sur un modèle EN COURS de téléchargement (et le disent) |
| 10:37 | `7f330f10` | Défaut SILENCIEUX corrigé : le motif de pré-découpage kimi manquait (Kimi-K2.7 ET Kimi-K3) |
| 10:42 | `8f73c6d2` | Deuxième défaut trouvé par un test unitaire : le découpage par casse enjambait les majuscules |
| 10:43 | `0d8cb93a` | Docs : la cible Kimi-K3, les deux défauts de tokenizer corrigés, et la référence llama.cpp-k3 |
| 10:44 | `d4b3150b` | Spec Kimi-K3 : cadence hybride VÉRIFIÉE sur le fichier (MLA aux couches 3,7,11,15), détail des projections MLA, MoE latent (routeur en pleine largeur) et res_mix final avant la tête |
| 10:55 | `a648f9e1` | KimI-K3 : les deux mathématiques neuves implémentées et testées SANS poids (SiTU, attention résiduelle) |
| 11:00 | `556739d5` | Sprint 28 : portes toutes vertes (69 tests), perplexité V4-Flash derrière ARCHIVE=1, et la leçon des pkill qui se tuent eux-mêmes |
| 11:01 | `f536b53c` | Spec Kimi-K3 : le KDA, sa porte bornée à -5, ses trois chemins de référence et les tenseurs qui serviront de points de comparaison |
| 11:04 | `05a906b4` | CORRECTION : un jeton de Kimi-K3 lit 87 Go de poids (pas 35) — et c'est l'ATTENTION qui domine, pas les experts |
| 11:05 | `984663db` | KDA (delta-net de Kimi-K3) : la récurrence implémentée et vérifiée contre une référence NumPy |
| 11:06 | `69cbff0c` | Sprint 29 : 87 Go par jeton (l'attention dépasse les experts), outils qui disent leur périmètre, et la récurrence du KDA vérifiée |
| 11:08 | `b97f929b` | KDA : porte bornée et convolution courte implémentées et testées — le test a attrapé une inversion de disposition d'état |
| 11:30 | `5ba0d881` | Réutilisation des experts MESURÉE : 46,9 % immédiate, 74,8 % avec le quart le plus chaud en cache |
| 11:43 | `913fe1c0` | Réutilisation : trois relevés (wikitext 48 et 128 jetons, code 128) — immédiate 47-49 %, un quart de cache sert 75-87 % |
| 11:44 | `d9dc8515` | Sprint 30 : la réutilisation des experts est mesurée — 47-49 % immédiate, un quart de cache sert 80-87 %, plafond 93 % |
| 11:45 | `d541216d` | Protocole de vérification de Kimi-K3 : les 13 points de comparaison de la référence, l'ordre, les tolérances, et le premier jalon (couche 0) |
| 11:49 | `45c757f1` | Débits remesurés : RAM 40 Go/s à 8 fils (pas 20), NVMe 3,4 Go/s à 4 flux — le budget de Kimi-K3 refait |
| 11:50 | `506046b0` | Séquence de l'après-téléchargement, automatique et ordonnée (5 étapes qui échouent en disant laquelle) |
| 11:51 | `2cd9719d` | Réutilisation : par couche (18 % à 69 %) et concentration du routage (10 % des experts servent 57 % des lectures) |
| 12:01 | `6b7b7fac` | Kimi-K3 : l'inventaire des tenseurs, vérifié sur le fichier (49 couches vues, cadence KDA/MLA confirmée) |
| 12:02 | `89a854aa` | Spec Kimi-K3 : notes d'exécution (poids empruntés, activations quantifiées, tailles d'état, ordre exact de la couche 0) |
| 12:03 | `5223a20c` | Journal (màj automatique) |
| 12:05 | `20e40578` | Croisement des maths K3 avec le code PUBLIÉ de Moonshot : SiTU, attention résiduelle, projections, convolution, porte bornée — identiques |
| 12:08 | `c357f9cf` | K3 : la passe avant de la couche 0 (f32) — structure d'abord, exactitude ensuite |
| 12:25 | `ca9125c0` | K3 : la couche 0 CALCULE sur le vrai fichier (test de fumée --k3-essai), et il a attrapé une convention de dimensions |
| 12:28 | `1cdc767c` | K3 : les dimensions des quatre types de couches sont CONFORMES au fichier (0 dense, 1 MoE+KDA, 3 MoE+MLA, 4 KDA) |
| 12:29 | `c29cbc2b` | K3 : la couche 0 vide ses sorties au format du moteur — la comparaison tenseur par tenseur n'attend plus que la référence |
| 12:31 | `b34a8e34` | Spec Kimi-K3 : l'ordre exact du MoE latent (routeur en pleine largeur, norme DANS le latent avant la remontée, biais en sélection) |
| 12:44 | `f0d980b8` | K3 : le MoE latent fonctionne — et 25,7 s/jeton sont devenus 1,36 s (×18,9) sans changer un chiffre |
| 12:51 | `dd4f0572` | K3 : la couche MLA calcule (couches 3, 7, 11…) — absorption par tête, nope sans rotation, porte sigmoïde pleine largeur |
| 12:53 | `2514e762` | K3 : le KDA extrait en pièce réutilisable (couches 1, 2, 4, 5, 6, 8…), avec sa remise à zéro d'état |
| 12:58 | `b0c14b95` | K3 : les quatre premières couches COMPOSÉES (0 dense, 1-2 MoE, 3 MLA) — la chaîne vérifiée, pas seulement les pièces |
| 14:27 | `3bf4ef3a` | Bloc 31 : le regroupement par experts vaut x1,58 — et Kimi-K3 est arrivé au complet |
| 15:03 | `c8ff34c6` | K3 complet : les sorties sont identiques à celles obtenues pendant le transfert |
| 15:39 | `058ea00f` | Tuile du GEMM par lots : hypothèse avancée, mesurée, RÉFUTÉE |
| 15:58 | `af1c3778` | ref_logits_k3 : la commande de liaison est écrite, le binaire n'a plus de mystère |
| 16:04 | `f2116f04` | Bloc 31 : la porte gpt-oss, son motif réel, et l'arbitrage assumé |
| 16:11 | `ff3a25a0` | REPRISE : le bloc 31 en tête — K3 complet, 86,787 Go par jeton, x1,58 par regroupement |
| 16:28 | `07bc7d53` | Tuile : l'essai repris machine au calme confirme la réfutation (20,02 s contre 20,32 s) |
| 18:05 | `053426c1` | K3 : la cadence des couches a une EXCEPTION, et le moteur ne l'a pas codée en dur |
| 18:16 | `1462acad` | K3 : composer 13 couches, le premier essai qui franchit une BANQUE |
| 19:45 | `aacb18c3` | K3 : les 13 premières couches, dont la BANQUE de la couche 12 — sorties finies |
| 20:06 | `36f1243a` | ref_logits : REF_SANS_REPACK, la porte qui rend la référence K3 exécutable ici |
| 22:03 | `94d51945` | Bloc 31 : la référence sur K3 — l'architecture passe, la politique mémoire non |
| 22:35 | `75c72364` | K3 : le premier jalon de vérification est NÉGATIF — et il désigne l'état, pas la forme |
| 22:57 | `61c8ba5b` | REPRISE : la baseline de la référence (42 min/jeton) et le jalon négatif, en tête |
| 22:57 | `e2bd0092` | K3 : la référence a tourné — 42 min/jeton, 11 % de CPU, 1,80 To lus pour 4 passes |
| 23:45 | `7a5e5d5b` | K3 : deux bugs trouvés par la comparaison — la norme L2 manquante, et la banque qui s'accumulait |

## Le récit de la journée (écrit à la main)

<!-- notes -->

<!-- /notes -->
