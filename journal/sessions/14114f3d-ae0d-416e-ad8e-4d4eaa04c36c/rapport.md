# Session 14114f3d — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `14114f3d-ae0d-416e-ad8e-4d4eaa04c36c` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 09:31 |
| Durée | 0.4 h |
| Tours | 1 |
| Messages | 30 |
| Appels d'outils | 41 |
| Fichiers touchés | 3 |
| Commandes | 25 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer la fiabilité « produit » du bloc linguistique** — qu'est-ce qu'un utilisateur peut utiliser en autonomie, et qu'est-ce qui est encore fragile ?  Contexte : `tools/bloc_linguistique.py` (`Heuristique`, `analyser`), `tools/tests/linguistique/evaluer_gold.py` (`charger`, `evaluer_bl … [1929 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer  … [2209 caractères tronqués]

*41 appels d'outils.* Actions notables :

- bash — Vérifier branche et état du dépôt
- bash — Lister outils, tests linguistiques, rapports
- bash — Compter lignes des fichiers cibles
- bash — Vérifier existence des fiches
- read
- bash — Lister classes et fonctions du module
- bash — Lire débuts des fiches audit et dev-test
- bash — Rejouer l'évaluation gold de référence
- bash — Vérifier commit et propreté des fichiers cibles
- bash — Lire les tests existants du bloc
- bash — Repérer les portes liées au bloc
- bash — Lire le contrat documenté du bloc
- bash — Lire la suite du contrat documenté
- bash — Vérifier le corpus UDHR et ses codes langue
- … et 15 autres

**Synthèse produite :**

⏵ Construction du banc de 50 phrases libres et du harnais d'audit

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/audit_produit_bl/phrases.py` | 1 | 0 |
| `/tmp/audit_produit_bl/audit.py` | 1 | 0 |
| `/tmp/audit_produit_bl/performance.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Vérifier branche et état du dépôt
- **T1** Lister outils, tests linguistiques, rapports
- **T1** Compter lignes des fichiers cibles
- **T1** Vérifier existence des fiches
- **T1** Lister classes et fonctions du module
- **T1** Lire débuts des fiches audit et dev-test
- **T1** Rejouer l'évaluation gold de référence
- **T1** Vérifier commit et propreté des fichiers cibles
- **T1** Lire les tests existants du bloc
- **T1** Repérer les portes liées au bloc
- **T1** Lire le contrat documenté du bloc
- **T1** Lire la suite du contrat documenté
- **T1** Vérifier le corpus UDHR et ses codes langue
- **T1** Vérifier dépendance générateur et variable d'environnement
- **T1** Lire l'API du générateur S
- **T1** Rejouer l'évaluation et sauver le JSON de référence
- **T1** Extraire les chiffres de référence du JSON
- **T1** Exécuter le harnais de robustesse et contrat
- **T1** Corriger la collision de clé et relancer
- **T1** Inspecter les anomalies détectées
- **T1** Inspecter cas limites et déterminisme
- **T1** Mesurer temps, mémoire et déterminisme
- **T1** Inspecter la stabilité du contrat
- **T1** Inspecter le format des codes langue
- **T1** Inspecter qualitativement des sorties représentatives

## 4. Mesures et résultats marquants

- **T1** `la cascade (mock de contrat) préserve ces chiffres et couvre **67,1 %** en unités sémantiques.`
- **T1** `(les réels passent de 40 % à 80 % en tête avec les deux lectures). Le **vrai** modèle neuronal est **refusé**`
- **T1** `- **L'attachement par tête couvre 100 %** ; le gold annote 29 cibles ambiguës en double lecture,`

