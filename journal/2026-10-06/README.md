# 2026-10-06

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-10-06/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**70 commits** · **1 session(s)** · **7 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| apprentissage | 1 | [apprentissage.md](apprentissage.md) |
| distribue | 6 | [distribue.md](distribue.md) |
| docs | 5 | [docs.md](docs.md) |
| memoire | 2 | [memoire.md](memoire.md) |
| mesures | 52 | [mesures.md](mesures.md) |
| modele | 2 | [modele.md](modele.md) |
| moteur | 2 | [moteur.md](moteur.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` | Continue avec REPRISE.md | 2026-09-28 14:46 | 222.5 h | [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:10 | `1a42f81e` | Signal précoce : plus de langues AIDENT (+23 % d'avantage), contrairement à ma mesure antérieure |
| 00:22 | `06134457` | Courbe de dose complète : elle NE sature PAS — le gain marginal par langue augmente |
| 00:24 | `a96b5538` | Dimensionnement de l'analyse finale, mesuré — et décision de ne PAS optimiser |
| 00:51 | `99a89ecf` | Signal précoce sur le panel STRATIFIÉ : l'écart de transfert était un artefact |
| 01:28 | `0ce0f3fc` | Bug : --seuil-commun ne pilotait PAS la décision, seulement l'affichage |
| 01:43 | `cf54f8b5` | Mon seuil de couche par défaut était TROP STRICT — la profondeur forcée paie |
| 01:53 | `dad554e1` | Optimum du seuil de couche : 0,25, et c'est un maximum INTÉRIEUR |
| 03:17 | `e85847a6` | Plateau sur 392 langues : le 'sous-ensemble partagé' s'effondre de 678 à 48 canaux |
| 03:18 | `2bdae7e9` | LIVRABLE PHASE 2 : le pont sur 301 langues — fid TEST 0,7430, invariance 0,9827 |
| 03:23 | `99878faa` | Bug de guetteur : 'TERMINE' matchait la sous-chaîne de 'caches TERMINE' |
| 04:00 | `43adee16` | Le piège du droit d'exécution, trois fois — corrigé à la racine |
| 04:01 | `644cf5c3` | Restriction ou pas : comparaison complète, et correction de mon invariant |
| 04:18 | `00b65d41` | Le plateau du professeur est à la couche 8, pas 10 — ma cible était mal choisie |
| 04:27 | `9070ecf1` | Romeo : le pont TRANSFÈRE sur du texte littéraire (0,6660 anglais -> 0,5802 français) |
| 04:38 | `e89dbe3e` | Couche 8 contre couche 10 : la correction de cible PAIE (+0,0213 sur le transfert) |
| 04:42 | `6b4a75ef` | Audit de cohérence : deux affirmations périmées pointées dans mes propres rapports |
| 04:43 | `75d590a6` | Audit (suite) : le TITRE du rapport génératif promettait ce que son corps réfute |
| 04:44 | `47152fd7` | Audit (fin) : les deux mêmes incohérences étaient dans recapitulatif.md |
| 05:10 | `377339d5` | Le gain de la couche 8 est ROBUSTE : +0,0215 sur trois graines (variation 0,0005) |
| 05:11 | `0ccef36c` | PIÈGE : l'invariance sur Wikipedia ne veut rien dire (segments non appariés) |
| 05:15 | `4e12ea69` | CORRECTION : la 'richesse' n'est PAS dans le nombre de canaux actifs |
| 07:36 | `e8ae5a28` | Domaine ou langue ? testé — et l'expérience est INCOMPLÈTE, je le signale |
| 07:39 | `b7fcce9a` | Signal précoce : la couche 8 gagne aussi au niveau des UNITÉS (+0,0381) |
| 07:41 | `0b91cb0c` | La pire paire (dzo) : hypothèse de longueur testée et RÉFUTÉE |
| 07:44 | `37429ed9` | Les langues éloignées partagent une NORME plus grande, pas une densité différente |
| 08:12 | `338d1948` | Le pont ne sert pas toutes les langues également — et la fidélité EST le témoin constant |
| 08:20 | `482240ca` | Réservoir multi-échelle : +8,8% sur l'apport propre, mais ce n'était pas la cause |
| 08:55 | `e036749c` | Le réservoir ne sert presque à rien : l'entrée SEULE fait mieux, sans un neurone |
| 09:20 | `b2e5631f` | Couche 8 contre couche 10 au niveau des unités : +0,0495 de fidélité |
| 09:28 | `b15a6048` | Contrôle de capacité : l'entrée gagne par nature, sans que ce soit tranché |
| 09:41 | `4de5b2f1` | Le §29 n'est PAS un artefact d'alignement — mesuré, et Wikipedia transfère mieux |
| 10:30 | `c36bb6bb` | Introspection du bloc : trois erreurs, dont un chiffre de tête qui ne disait pas ce qu'il semblait |
| 10:40 | `c660fde3` | Correction du §29 : le réservoir n'était pas inutile, il était TROP PETIT |
| 11:25 | `8374ad48` | Où va le temps : profil mesuré, et un remède gratuit à 5,8x |
| 11:36 | `8dfb6dc5` | Protocole à deux panneaux : le goulot est le TRANSFERT, pas les caractéristiques |
| 11:58 | `1404baca` | Le ride était 10 à 30 fois trop fort, et l'écart de transfert n'est pas du sur-apprentissage |
| 12:08 | `0554a720` | Correction du §38.2 : le tanh sature PRESQUE TOUJOURS, c'est l'état moyenné qui reste petit |
| 12:17 | `d15c870f` | La courbe ne plafonne pas (800 neurones → 0,6821) et baisser le gain est RÉFUTÉ |
| 12:36 | `b8e8f601` | Le profil porte tout le protocole — et il révèle un écart d'invariance majeur |
| 13:03 | `ab91def0` | Glossaire : section 10 complète sur le pont, avec les termes de ses propres définitions |
| 13:04 | `d6746330` | NLMS à pas fin : à 0,0075 de la ridge, et moins chère au-delà de 900 caractéristiques |
| 13:18 | `ce3b05d1` | Jalon : 392 langues tracées aux couches 8 ET 10, zéro échec |
| 13:39 | `f30b14b9` | Croissance vectorisée sur les langues : 28 s → 1,76 s par neurone, identité bit à bit |
| 13:48 | `817ca1bb` | Couche 8 contre couche 10 à 392 langues : 41 sur 41 s'améliorent, ZÉRO régresse |
| 14:02 | `48aa0d98` | Premier corpus MULTI-DOMAINE et ALIGNÉ : 482 articles Wikipedia en 6 langues |
| 15:27 | `6b1cad40` | Deuxième œuvre parallèle (Crime et Châtiment, en-es) et généralisation du test domaine/langue |
| 15:50 | `f6d40c8b` | Fidélité et invariance tirent en sens opposé quand le réseau grandit |
| 16:11 | `5ad2f09e` | Ajuster la lecture SOUS CONTRAINTE d'invariance : +0,042 d'invariance pour 0,008 de fidélité |
| 16:41 | `a3abff2d` | Croissance + attrition à 392 langues : 182 neurones, TEST 0,6340, invariance 0,8659 |
| 16:46 | `d355fec2` | La contrainte d'invariance déplace la courbe, elle ne supprime pas la tension |
| 17:16 | `61248ebc` | La contrainte d'invariance fonctionne DANS la croissance, à 16-20 pour 1 |
| 17:22 | `0b9599c6` | Un drave ORPHELIN volait 18 cœurs : 60 s par trace au lieu de 16 |
| 18:13 | `75cc1b7e` | Domaine ou langue : enfin testable, et la réponse est 'à égalité' |
| 18:22 | `8be5966e` | Le garde-fou du §30 a attrapé une SECONDE occurrence du même bug |
| 18:30 | `44f0c9f4` | Le pont transfère sur le corpus Wikipedia multi-domaine, sur TROIS paires de langues |
| 19:44 | `e266e217` | Croissance sous contrainte, protocole ENTIER : 147 neurones, oracle sur les deux panneaux |
| 19:45 | `83cd4256` | LA question du §41 est tranchée : notre sortie ÉCRASE la distinction contenu/langue |
| 20:05 | `c3de2df4` | Réécrire l'objectif : la structure du professeur EST atteignable, mais l'objectif à deux curseurs est NON CONVEXE |
| 20:26 | `603b7a69` | La piste 'le moindres carrés néglige les petites composantes' est RÉFUTÉE par sa prémisse |
| 20:47 | `a41a27b7` | Le rétrécissement est réel (3,4x) mais n'est pas la cause ; et la cible du §58 n'est pas stable |
| 20:58 | `09b0218f` | Le défaut est LOCALISÉ et QUANTIFIÉ : notre sortie porte 12x moins d'énergie de CONTENU |
| 21:29 | `120d50c5` | Le remède est trouvé mais n'est pas déployable — et un piège de méthode |
| 21:41 | `7414653c` | Cinquième remède écarté : le sous-espace du contenu appris ne se TRANSFÈRE pas |
| 21:52 | `33d40182` | Le centrage de l'entrée : premier levier de la série à la fois efficace ET déployable |
| 22:24 | `1f6dc82e` | Bug de découpage dans MES outils : l'ajustement ne portait que sur DEUX langues |
| 22:45 | `09291d7c` | Deux leviers DÉPLOYABLES qui se combinent : le rapport passe de 1,46 à 3,06 |
| 23:16 | `7c3413d9` | Le rapport est INVARIANT D'ÉCHELLE (identité), et imposer la covariance de la cible échoue |
| 23:38 | `3b50b1ac` | Le discriminant fonctionne : rapport 6,96 (64 % de la cible) — et la frontière est tracée |
| 23:50 | `97fc5ea1` | OÙ ENTRE LA LANGUE : dans l'entrée, pas dans le réservoir — et le réservoir l'AMPLIFIE |
| 23:51 | `f9186a3c` | Glossaire : §10.10, le vocabulaire de la mesure contenu/langue |

## Le récit de la journée (écrit à la main)

<!-- notes -->

<!-- /notes -->
