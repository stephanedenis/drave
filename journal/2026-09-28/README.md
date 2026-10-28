# 2026-09-28

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-09-28/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**37 commits** · **3 session(s)** · **8 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| attention | 3 | [attention.md](attention.md) |
| distribue | 1 | [distribue.md](distribue.md) |
| divers | 1 | [divers.md](divers.md) |
| docs | 11 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 4 | [mesures.md](mesures.md) |
| modele | 4 | [modele.md](modele.md) |
| moteur | 12 | [moteur.md](moteur.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `22bcae27-254b-47b2-acda-87467dab060c` | Étude de Qtrinet-bootstrap.md | 2026-09-25 11:56 | 74.8 h | [rapport](../sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md) · [digest](../sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md) |
| `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` | Continue avec REPRISE.md | 2026-09-28 14:46 | 222.5 h | [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md) |
| `e7dfe34f-d596-4f98-93c2-cad5a92d3b1e` | Tu travailles dans un dépôt | 2026-09-28 14:56 | 0.1 h | [rapport](../sessions/e7dfe34f-d596-4f98-93c2-cad5a92d3b1e/rapport.md) · [digest](../sessions/e7dfe34f-d596-4f98-93c2-cad5a92d3b1e/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 06:52 | `c504ebd6` | Lecteur MXFP4 exact (gpt-oss-120b) et analyse du passage a l'echelle |
| 07:17 | `250a1bf8` | Emprunt des blocs 4 bits en place : chargement x3,2, memoire /2, fidelite exacte |
| 07:40 | `6b379f5c` | Q4_K et Q6_K en place : le 7B et le 1,5B Q4_K_M tournent |
| 07:49 | `847f9abd` | Q6_K en place (AVX2) : tete divisee par 5, fidelite gagnee |
| 08:24 | `03176591` | Documentation : parc de modeles lisible, methode de verification, MoE |
| 08:24 | `f4434b99` | MoE : routage top-k et tranches par expert, le 30B-A3B tourne |
| 08:31 | `23850b97` | Journal : session du 28/09 (Q4_K/Q6_K/MXFP4 en place, MoE, 30B-A3B) |
| 08:46 | `1082358c` | Q8_0 en place, plan de placement, epinglage NUMA mesure |
| 11:21 | `2f87190f` | Tokenizer o200k verifie, briques gpt-oss, YaRN ; 120B charge et tourne |
| 11:57 | `0c79a989` | Journal : session du 28/09 (tokenizer o200k, briques gpt-oss, descente de perplexite) |
| 11:57 | `fb446715` | gpt-oss : perplexite 42 127 -> 39,8 en cinq etapes mesurees |
| 12:06 | `4270573c` | Chemin GPU operationnel : noyaux PTX, API pilote, tete de sortie deportee |
| 12:45 | `e5ac235e` | Journal : session du 28/09 (chemin GPU, seuil mesure) |
| 12:45 | `4a3789d6` | Deport GPU des projections d'attention : mesure, et ce que le bus decide |
| 12:57 | `f3b20f91` | Courbe qualite/octets par simulation de precision (5, 6, 7, 8 bits) |
| 12:58 | `8b9cf306` | Journal : courbe de precision |
| 13:23 | `1ae6543e` | Journal : format 6 bits |
| 13:23 | `6b2e50aa` | Format 6 bits empaquete : 0,75 octet/poids, et il BAT notre int8 |
| 13:31 | `5590c2ae` | Journal : 6 bits vectorise |
| 13:31 | `a018f43b` | 6 bits vectorise : il domine l'int8 sur les TROIS axes |
| 13:35 | `31c057cd` | Rapport : le moteur sur du vrai travail (deux tests reels sur le 30B MoE) |
| 13:42 | `ba9ce7e7` | Echantillonnage complet et sortie en flux : le moteur devient utilisable en direct |
| 13:45 | `adbee43d` | Journal : session multi-tours |
| 13:45 | `4a443992` | Session multi-tours interactive : le moteur sait tenir une conversation |
| 13:59 | `3ef012da` | Journal : gpt-oss genere correctement |
| 13:59 | `198d2e93` | gpt-oss : le modele fonctionne, la metrique non |
| 14:09 | `b819c8d9` | Journal : YaRN, resultats negatifs |
| 14:09 | `163a53e5` | gpt-oss : la perplexite monte avec la fenetre, et YaRN n'y remedie pas |
| 14:24 | `8a8d419d` | Journal : diagnostics gpt-oss |
| 14:24 | `19f88756` | gpt-oss : deux diagnostics de plus, dont un bug de cablage CLI |
| 14:40 | `2625a74d` | Journal : gabarit harmony |
| 14:40 | `df18aefd` | Gabarit harmony de gpt-oss : fait. Refactorisation CLI : abandonnee, et pourquoi. |
| 14:45 | `f57e1514` | REPRISE.md : base de reprise autonome |
| 17:24 | `72e7dc47` | gpt-oss : biais attn_output et fenetre par couche corriges, reference llama.cpp |
| 17:27 | `8ca0c582` | REPRISE : chiffres gpt-oss exacts (ids 15,1757 / texte 15,0757) |
| 20:06 | `d56d81f7` | Rotation : YaRN a retardement, et la temperature est la moitie nuisible |
| 20:45 | `1a139332` | Rotation : points 4096 et 4608, et la limite du test de generation |

## Le récit de la journée (écrit à la main)

<!-- notes -->

<!-- /notes -->
