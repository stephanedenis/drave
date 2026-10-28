# 2026-09-25

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-09-25/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**21 commits** · **2 session(s)** · **6 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| attention | 1 | [attention.md](attention.md) |
| docs | 3 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 7 | [mesures.md](mesures.md) |
| modele | 2 | [modele.md](modele.md) |
| moteur | 7 | [moteur.md](moteur.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `22bcae27-254b-47b2-acda-87467dab060c` | Étude de Qtrinet-bootstrap.md | 2026-09-25 11:56 | 74.8 h | [rapport](../sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md) · [digest](../sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md) |
| `27c99b10-c57e-4599-a23a-f7b1a54c17a1` | Tu écris un tokenizer BPE | 2026-09-25 19:40 | 0.2 h | [rapport](../sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/rapport.md) · [digest](../sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 13:48 | `88bfcdd2` | Test de principe : quantification ternaire / multi-bits d'un modèle minimal |
| 15:14 | `1f601a4e` | Élagage et approche par événement : où se situe le seuil de rentabilité |
| 15:26 | `3c6df267` | Encodage de structure : les deux listes signées éliminent la valeur |
| 15:34 | `8058018f` | Architecture push (AER) : oui, c'est pensable sur CPU — et c'est même à faire en premier |
| 15:38 | `f5f20a0c` | Tri + dédoublonnage des contributions : mesuré, et le verdict est contre-intuitif |
| 15:53 | `90643b14` | Grappes afférentes/efférentes : imposer la structure à la conversion |
| 16:53 | `56b7603a` | Un LLM dense n'expose pas de grappes naturelles (mesuré sur Qwen2.5-0.5B) |
| 17:15 | `6831972e` | Éliminer la valeur par répétition d'adresse : mesuré sur un vrai modèle 4 bits |
| 17:16 | `78e6a441` | Verdict valeur-unaire : réécrit (il se contredisait) |
| 17:31 | `e230f2ff` | 8 bits : la perfection est déjà atteinte — et correction du ×2,17 annoncé |
| 18:05 | `cbfc0ba8` | Harnais de test : perplexité 20,29 sur WikiText-2 + mesure du débit variable |
| 18:10 | `3b5eded1` | Correctif majeur : promotion float64 silencieuse (×30 sur le forward) |
| 18:33 | `a44dcbba` | qtrinet-core : moteur d'exécution par listes en Rust (std seul) |
| 18:52 | `960cd360` | qtrinet-core : pool persistant (×10 sur le coût fixe) et décodeurs rapides |
| 19:05 | `88d617a2` | Moteur d'événements : les 2 décodeurs sont exacts, mesures consolidées |
| 19:09 | `8bccc65b` | Moteur : fenêtre de réduction exacte, pool borné, exactitude aux 7 densités |
| 19:58 | `fa87057b` | Inférence complète en Rust : Qwen2.5-0.5B sans GPU, sans BLAS, sans dépendance |
| 20:02 | `896499de` | Mode dense de comparaison : l'architecture evenementielle coute 8 % sur CPU |
| 20:03 | `591b4765` | Inférence Rust : zéro avertissement, exemple de sortie, mode dense documenté |
| 22:06 | `231f1981` | README : reponse courte sur le 4 bits et le cout par evenement |
| 22:06 | `14a825db` | 4 bits : non, et la raison est plus intéressante que la réponse |

## Le récit de la journée (écrit à la main)

<!-- notes -->

<!-- /notes -->
