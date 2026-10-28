# 2026-10-05

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-10-05/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**69 commits** · **1 session(s)** · **9 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| apprentissage | 3 | [apprentissage.md](apprentissage.md) |
| attention | 2 | [attention.md](attention.md) |
| distribue | 7 | [distribue.md](distribue.md) |
| docs | 21 | [docs.md](docs.md) |
| memoire | 7 | [memoire.md](memoire.md) |
| mesures | 19 | [mesures.md](mesures.md) |
| modele | 5 | [modele.md](modele.md) |
| moteur | 2 | [moteur.md](moteur.md) |
| portes | 3 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` | Continue avec REPRISE.md | 2026-09-28 14:46 | 222.5 h | [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 07:03 | `ea0e8ce2` | K3 : la question ouverte est TRANCHÉE — c'est la CAPACITÉ du cache, pas la dispersion |
| 08:02 | `e81fa30a` | Morcellement des experts : l'élagage par fréquence, mesuré — la fréquence n'est pas l'importance |
| 08:20 | `c4ffbc8b` | Note : la voie événementielle — prédire une couche pour ne transporter que l'imprévu |
| 08:34 | `b36e46e4` | Mesure : le plateau sémantique est à la couche 23 sur 48 — la coupe est une FENÊTRE, pas un point |
| 08:43 | `5e53c744` | Bloc 0-9 : première borne d'approximabilité — 19 % de la variance après dix couches avec DEUX directions |
| 08:52 | `1a109291` | Note : les corpus de Panini-Research — 11,5 M mots, et TROIS œuvres parallèles |
| 09:08 | `1ba332fd` | Ingestion : l'UDHR récupérée (456 langues, 30 articles alignés), Wikipedia trouvé en local (81 Go, 6 langues) |
| 09:18 | `d20c3bab` | UDHR : extracteur d'unités alignées — 400 langues, les 30 articles, 42 unités |
| 09:32 | `f29b4f56` | Apprentissage hebbien différentiel : implémenté dans le moteur, et mesuré |
| 09:36 | `5a7e76b6` | Hebb différentiel : le test hors échantillon N'A PAS TOURNÉ, et j'explique pourquoi |
| 09:55 | `950dbdbb` | Plateau multilingue à l'échelle : 10 langues, 4 écritures, pic à 42 % de la profondeur |
| 10:05 | `e29ba520` | Un modèle haut de gamme converge MIEUX : pic 0,693 contre 0,649, et surtout pire paire 0,471 contre 0,280 |
| 10:15 | `7fd59f6c` | VERDICT : la règle hebbienne locale ne transfère PAS — et dégrade les langues non vues |
| 10:16 | `3ad2c0e1` | La LECTURE ne rattrape rien : combiner les couches DILUE l'invariance |
| 10:17 | `b149d79c` | Note : la règle contrastive — quoi construire, et pourquoi c'est elle |
| 10:19 | `7930616d` | LE FONDEMENT EST VALIDÉ : la langue est soustractible, et le témoin le prouve |
| 10:35 | `6e2884d0` | LE PONT : une matrice 896x896 rend la langue invisible, mieux que le professeur |
| 10:43 | `7f5630ab` | Le pont validé à l'échelle : 20 langues d'entraînement, 20 JAMAIS vues |
| 10:47 | `8b159bea` | Le pont devient un ARTEFACT utilisable, et l'étiquetage est corrigé |
| 11:00 | `0db119db` | UN SEUL NEURONE SUFFIT : 0,9492 d'invariance contre 0,6284 pour le professeur |
| 11:03 | `d876d238` | Le pont rang-1 est l'artefact, et la sonde est un échec de protocole — dit tel quel |
| 11:18 | `99919da2` | Ajouter des neurones DÉTRUIT la fidélité ; ajouter une COUCHE la sauve |
| 11:31 | `0f2c02f8` | LA COUCHE RÉCURRENTE GAGNE : réservoir 64 neurones, 0,59 fidélité / 0,91 invariance / 0,84 pire paire |
| 11:44 | `12346ae5` | Coût du professeur : 77-83 % des traces sont des couches jamais lues |
| 11:47 | `05197025` | Le chargement n'est pas borné par --couches, et l'attention quadratique interdit les longues passes |
| 12:46 | `d13aef7e` | OUI, le modèle est optimisable : +7 pts d'invariance, +11 pts de pire paire, à coût nul |
| 12:52 | `1dffbcfc` | Le gain d'optimisation RÉPLIQUE sur la tâche 10x plus dure |
| 13:00 | `e39f6fc3` | Le pont GÉNÉRATIF : naissance par couches, puis attrition qui généralise |
| 13:01 | `d577699c` | Critère de REDONDANCE : retirer ce que les autres disent déjà |
| 13:03 | `da8c11f3` | Le génératif CONFIRMÉ sur 10x plus de données, et les cycles croissance->attrition |
| 13:04 | `27e8f3ed` | L'ATTRITION PÉRIODIQUE paie : deux cycles battent une passe |
| 13:12 | `e82c5df8` | Cycles confirmés sur la tâche 10x plus dure : +68 % d'avantage sur la constante |
| 13:19 | `ad52e51e` | Le plateau de croissance est trouvé (~470 neurones), et l'ATTRITION fait mieux que la croissance |
| 13:28 | `07c2fcdc` | compare_professeurs.py : les professeurs et notre pont sur le MÊME périmètre |
| 13:47 | `f671101d` | RECTIFICATION : un pont par professeur — il n'y a pas de couche sémantique universelle |
| 13:48 | `187f3ebe` | Contamination mesurée : les 32 jetons générés SONT dans la trace |
| 13:50 | `041a7797` | Vérifié au jeton près : --n 32 donne 542 positions, --n 0 en donne 510, différence exactement 32 |
| 14:17 | `bb7c3fc5` | La cascade préfère les réglages OPPOSÉS au réservoir plat |
| 14:34 | `0c3e2671` | Contrôle de robustesse : 12 tirages, médiane honnête +0,0412 |
| 14:55 | `3acef496` | TRONCATURE : le défaut le plus grave, et ce qu'il fait aux résultats publiés |
| 16:14 | `f2d8314f` | RÉSULTAT NÉGATIF : sur données propres, l'avantage de la cascade s'efface |
| 16:21 | `eca18c0f` | REPRISE.md : état 16h20 — pont génératif, résultat négatif sur données propres |
| 16:39 | `5d89095c` | LA LOI : fidélité et invariance s'échangent à taux fixe (r = 0,992) |
| 17:53 | `9c01e9b3` | Couches RÉELLES, naissance libre, et récapitulatif |
| 17:58 | `694efc31` | Déclencheur de couche révisé : concepts communs + besoin de poids négatifs |
| 18:34 | `4ba90227` | Sous-ensemble actif : la droite d'échange MONTE (+14 pts de fidélité, +18 % des canaux) |
| 18:54 | `f7c7b52f` | L'INVARIANT : le pont apporte +0,020, quelle que soit la cible |
| 18:55 | `aeb7f125` | CONCLUSION : la fidélité est portée par l'invariance de la cible, pas par le modèle |
| 19:27 | `9a661018` | Lecture non linéaire : le plafond passe de +0,020 à +0,024 (+18 %) |
| 19:28 | `314b3cc8` | journal |
| 20:22 | `635d3c43` | Le plafond est dans le TRANSFERT, pas dans les caractéristiques ; l'attrition ne généralise pas |
| 20:50 | `5d007972` | RECTIFICATION : l'oracle du §10.2 était faux ; le plafond est 0,7076, pas 0,7762 |
| 20:51 | `5497c343` | journal |
| 21:08 | `402c2e11` | La restriction réduit aussi l'ÉCART de transfert (−28 %), confirmé sur les deux panneaux |
| 21:12 | `7f27148c` | Ce que la restriction NE fait PAS : la contribution du pont reste +0,020 |
| 21:14 | `62982faa` | L'attrition corrigée : une décision, plus une démolition |
| 22:24 | `58f1e0d8` | Phase 2 : corpus PARALLÈLE riche — Romeo and Juliet, 24 scènes alignées en/fr |
| 22:41 | `809fc83f` | Phase 1 lancée : 392 langues UDHR · phase 2 chaînée après |
| 22:43 | `538eea48` | Phase 3 chaînée : Wikipedia pour la RICHESSE, pas pour l'invariance |
| 22:54 | `ed926279` | pont_parallele.py : l'invariance sur un corpus apparié se mesure SEGMENT par SEGMENT |
| 22:56 | `9c5ae5a9` | Traçage PAR UNITÉ : l'invariance à dix points au lieu d'un |
| 22:57 | `5a82625e` | invariance_unites.py : l'invariance par unité, et une pire paire qui porte sur quelque chose |
| 23:00 | `74577bc2` | Lecteur tolérant à la TRONCATURE : une trace interrompue reste exploitable |
| 23:01 | `fbc8b1c6` | pont_unites.py : notre pont mesuré PAR UNITÉ, professeur contre sortie |
| 23:02 | `0380bf51` | Correction : le correctif annoncé au commit précédent n'avait pas été fait |
| 23:03 | `0d0e3383` | Analyse finale chaînée : Romeo, Wikipedia, et l'invariance par unité |
| 23:36 | `230ee303` | Deux erreurs de ma part, et un résultat mesuré qui les tranche |
| 23:48 | `21aafc9e` | 11 % des langues étaient TRONQUÉES à ctx 2048 — corrigé à ctx 4096, sans surcoût |
| 23:50 | `1424c5d1` | Rapport : extension à toutes les langues — périmètre, convention, découpage, 5 phases |

## Le récit de la journée (écrit à la main)

<!-- notes -->

<!-- /notes -->
