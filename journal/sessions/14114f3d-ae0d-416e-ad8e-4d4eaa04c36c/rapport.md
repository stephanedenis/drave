# Session 14114f3d — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `14114f3d-ae0d-416e-ad8e-4d4eaa04c36c` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 09:31 |
| Durée | 1.2 h |
| Tours | 1 |
| Messages | 63 |
| Appels d'outils | 76 |
| Fichiers touchés | 5 |
| Commandes | 58 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer la fiabilité « produit » du bloc linguistique** — qu'est-ce qu'un utilisateur peut utiliser en autonomie, et qu'est-ce qui est encore fragile ?  Contexte : `tools/bloc_linguistique.py` (`Heuristique`, `analyser`), `tools/tests/linguistique/evaluer_gold.py` (`charger`, `evaluer_bl … [1929 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer  … [2209 caractères tronqués]

*76 appels d'outils.* Actions notables :

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
- … et 50 autres

**Synthèse produite :**

⏵ Construction du banc de 50 phrases libres et du harnais d'audit

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/audit_produit_bl/phrases.py` | 1 | 0 |
| `/tmp/audit_produit_bl/audit.py` | 1 | 0 |
| `/tmp/audit_produit_bl/performance.py` | 1 | 0 |
| `/tmp/audit_produit_bl/performance_final.py` | 1 | 0 |
| `/tmp/audit_produit_bl/extra.py` | 1 | 0 |

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
- **T1** Calculer les statistiques agrégées de robustesse
- **T1** Quantifier attachements, titres, connecteurs, URL
- **T1** Compléter les mesures de contrat et compositions
- **T1** Mesurer la détection de langue avec et sans profils
- **T1** Tester cascade, fusion refus/contexte, décimales
- **T1** Vérifier les appels neuronal de la cascade sur le gold
- **T1** Mesurer le coût des modes composés
- **T1** Lire le style des JSON de fiches
- **T1** Lire le début de la fiche cohérence v8
- **T1** Exécuter les mesures finales et le démarrage à froid
- **T1** Corriger et relancer les mesures finales
- **T1** Vérifier la croissance du coût jusqu'à 4000 mots
- **T1** Profiler une analyse de 2000 mots
- **T1** Contrôles négatifs et simulation du correctif chevauchement
- **T1** Tester les mutations et simuler la déduplication sur le gold
- … et 18 autres

## 4. Mesures et résultats marquants

- **T1** `la cascade (mock de contrat) préserve ces chiffres et couvre **67,1 %** en unités sémantiques.`
- **T1** `(les réels passent de 40 % à 80 % en tête avec les deux lectures). Le **vrai** modèle neuronal est **refusé**`
- **T1** `- **L'attachement par tête couvre 100 %** ; le gold annote 29 cibles ambiguës en double lecture,`
- **T1** `MOTS '12,5 %' [(0, 2, '12', 'nombre'), (2, 3, ',', 'ponctuation'), (3, 4, '5', 'nombre'), (5, 6, '%', 'ponctuation')]`
- **T1** `"permutation": "1,997/220 (0,908 %) p=0",`
- **T1** `"candidat_aleatoire": "42,14 % top-1"`
- **T1** `99.2 ms 32`
- **T1** `109.0 ms 32`
- **T1** `113.3 ms 32`
- **T1** `200 median_s 0.019 ms/mot 0.096 labels 1061`
- **T1** `500 median_s 0.07 ms/mot 0.139 labels 2613`
- **T1** `1000 median_s 0.166 ms/mot 0.166 labels 5218`
- **T1** `2000 median_s 0.482 ms/mot 0.241 labels 10438`
- **T1** `4000 median_s 1.574 ms/mot 0.394 labels 20826`
- **T1** `f15 'Les prix ont augmenté de 12,5 % entre janvier et mars 2024, soit 3 poi' | nb 1`
- **T1** `e34 'The prices rose by 12.5% between January and March 2024, three points ' | nb 1`
- **T1** `### e34 'The prices rose by 12.5% between January and March 2024, three points more than expected.'`
- **T1** `[(0, 22, "'The prices rose by 12.'"), (22, 89, "'5% between January and March 2024, three points more than expected.'")]`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : MOTS 'https://example.com/a.pdf' [(0, 5, 'https', 'mot'), (5, 6, ':', 'ponctuation'), (6, 7, '/', 'ponctuation'), (7, 8, '/', 'ponctuation'), (8, 15, 'example', 'mot'), (15, 16, '.', 'ponctuation'), (
- **T1** : SIMULATION dedupe: paires 132 -> 0 | syntagmes 362 -> 292 | attachements 265 -> 215 | phrases 31 labels syntagme retirés 70 attachements retirés 50 [stderr] Traceback (most recent call last):   File "
- **T1** : ### mutations span_hors_texte detectee True | ['chevauchement_syntagme', 'span_hors_texte'] cible_absente detectee True | ['chevauchement_syntagme', 'cible_absente'] chevauchement_syntagme detectee Tr

