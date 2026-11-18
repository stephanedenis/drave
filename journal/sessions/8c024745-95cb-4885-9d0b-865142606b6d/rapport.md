# Session 8c024745 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-18/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `8c024745-95cb-4885-9d0b-865142606b6d` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-18 08:58 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 23 |
| Appels d'outils | 29 |
| Fichiers touchés | 0 |
| Commandes | 21 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave, en français). La machine est dédiée : 2 GPU Quadro RTX 5000 libres, 40 threads.  TÂCHE : mesurer la GRAMMATICALITÉ du modèle natif de 100 M (work/n2ac/mix1024-100m.pt) avec le banc existant, et comparer au 34 M déjà mesuré.  Étapes : 1. Lis reports/rapport-grammaticalite*.md (ou le rapport qui porte le banc  … [1875 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave, en français). La machine est  … [2155 caractères tronqués]

*29 appels d'outils.* Actions notables :

- bash — Liste les fichiers de grammaticalité
- glob
- read
- bash — Cherche les rapports de grammaticalité
- bash — Lit les JSON de grammaticalité et le rapport 100M
- bash — Vérifie banc_generation et JSON de génération
- bash — Vérifie GPU, torch et fichiers modèles
- bash — Inspecte structure des JSON de génération
- bash — Compte les paramètres des deux modèles
- bash — Cherche le contexte du 100M et l'état git
- bash — Vérifie la fenêtre et l'analyseur
- bash — Vérifie le protocole 128 octets du 34M
- bash — Génère 100M, 20 prompts, 128 octets, cuda:0
- bash — Lit le récit du 16 novembre sur le modèle
- … et 11 autres

**Synthèse produite :**

⏵ Test à blanc du pipeline de grammaticalité sur les JSON 64 octets existants

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Liste les fichiers de grammaticalité
- **T1** Cherche les rapports de grammaticalité
- **T1** Lit les JSON de grammaticalité et le rapport 100M
- **T1** Vérifie banc_generation et JSON de génération
- **T1** Vérifie GPU, torch et fichiers modèles
- **T1** Inspecte structure des JSON de génération
- **T1** Compte les paramètres des deux modèles
- **T1** Cherche le contexte du 100M et l'état git
- **T1** Vérifie la fenêtre et l'analyseur
- **T1** Vérifie le protocole 128 octets du 34M
- **T1** Génère 100M, 20 prompts, 128 octets, cuda:0
- **T1** Lit le récit du 16 novembre sur le modèle
- **T1** Affiche les échantillons 100M à 64 octets
- **T1** Lit la ligne N de l'état courant
- **T1** Vérifie l'activité GPU et CPU du job
- **T1** Vérifie l'état détaillé du processus
- **T1** Compare l'heure et l'âge du processus
- **T1** Contrôle l'avancement du job
- **T1** Teste le banc de grammaticalité sur les données 64 octets
- **T1** Attend et vérifie le job de génération
- **T1** Attend la fin de la génération

## 4. Mesures et résultats marquants

- **T1** `1. **Le vocabulaire est saturé dès 34 M** : 0,884 contre 0,882 en greedy — l'échelle ×3 n'achète`
- **T1** `0, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T1** `1, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T1** `| 15:52 | `14ef014d` | ÉTUDE — LES 2 GPU NVLink VS CPU : L'ENTRAÎNEMENT ×12-39 (×77 EN TANDEM), LE PRÉFILL ×12, LE NVLink 23 Go/s, MAIS LE 34 M EST SOUS-UTILISÉ ET LA GÉNÉRATION EST BLOQUÉE PAR LE CAC`
- **T1** ``×12` · `×77` · `×20` · `23 Go` · `0,137` · `0,278` · `0,335` · `0,247` · `0,494` · `0,870``
- **T1** `0, 1 MiB, 0 %`
- **T1** `1, 1 MiB, 0 %`
- **T1** `0, 502 MiB, 57 %`
- **T1** `1, 4 MiB, 0 %`

