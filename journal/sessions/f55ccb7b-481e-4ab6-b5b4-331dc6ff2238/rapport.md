# Session f55ccb7b — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `f55ccb7b-481e-4ab6-b5b4-331dc6ff2238` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 13:11 |
| Durée | 1.0 h |
| Tours | 1 |
| Messages | 107 |
| Appels d'outils | 111 |
| Fichiers touchés | 2 |
| Commandes | 61 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **prototype autonome d'un classement appris** des candidats d'attachement.  Contexte : `tools/tests/linguistique/evaluer_gold.py` expose `charger()` (612 phrases, segments gold avec `cibles`) et `evaluer_bloc` ; `tools/bloc_linguistique.py` expose `Heuristique` (annotation avec étiquettes  … [2160 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **prototyp … [2440 caractères tronqués]

*111 appels d'outils.* Actions notables :

- bash — Vérifier branche et arborescence
- read
- bash — Localiser les fonctions utiles
- bash — Inspecter format gold
- bash — Lancer l'évaluation gold actuelle
- bash — Statistiques des cibles gold
- bash — Extraire les chiffres d'attachement
- bash — Diagnostic des cas prédits et erreurs
- bash — Inspecter étiquettes et POS de cas clés
- bash — Mesurer la couverture du vivier
- bash — Tester des règles simples sur les 145 cas
- bash — Déboguer r080
- bash — Tester une règle manuelle par type/préposition
- bash — Vérifier cibles auxiliaires et unicité
- … et 83 autres

**Synthèse produite :**

⏵ Conclusion et résumé final

**Livrables créés (aucun fichier existant modifié, aucun commit) :**
- `tools/tests/linguistique/classement_cible.py` — prototype autonome, stdlib seule, n'écrit que le JSON.
- `reports/rapport-classement-appris.md` — fiche complète.
- `reports/pensee-classement-appris.json` — résultats, poids par pli, 145 prédictions auditées, empreinte du bloc.

**Protocole.** 145 segments gold au span prédit (GP 83, REL 26, SUB 36) ; vivier de tokens pleins construit sans le gold (cible couverte 144/145) ; features demandées + interactions type×nature et génitif×nature ; régression logistique maison (descente de gradient, L2, classes pondérées) ; split par parité d'id de phrase dans les deux sens, puis regroupé hors-pli.

**Taux d'exactitude :**

| | modèle appris | règle live 137 | règle committée 123 |
|---|---:|---:|---:|
| pairs → impairs (66) | **66 (1,0000)** | 64 (0,9697) | 60 (0,9091) |
| impairs → pairs (79) | **76 (0,9620)** | 73 (0,9241) | 63 (0,7975) |
| moyenne | **0,9810** | 0,9469 | 0,8533 |
| regroupé (145) | **142 (0,9793)** | 137 (0,9448) | 123 (0,8483) |

**Contrôles.** Hasard uniforme dans le vivier : 0,3876 attendu ; le **rang 0 seul** (premier candidat de la liste gauche→droite→dedans) fait déjà **139/145** (0,9586). Contre la règle live à 137 : **+5**, McNemar 7/2, **p = 0,18**, bootstrap **[−0,7 ; +7,6] pts** → non significatif. Contre l'état committé 123 : +19, p = 6,6e-05.

**Recommandation : ne pas intégrer le classement appris en l'état.** La règle live a absorbé l'essentiel pendant la session (123 → 129 → 137, empreinte `6e843018`) ; il ne reste que +5 non significatif, avec 2 régressions (`r048`, `r068`) et 25 poids pour +3 sur le simple prior de rang. En revanche, deux signaux sont à retenir : le **vivier ordonné** (139/145, gratuit) et le **fallback quand la cible est vide** (`g002`, `s041`, +2 sans risque). Le modèle à 142/145 reste la meilleure borne trouvée sur ce gold, mais son dessin de features a été informé par les 145 segments : il n'est pas validé pour un corpus neuf.

**Réserve de provenance :** `bloc_linguistique.py` et `evaluer_gold.py` ont été modifiés par d'autres agents pendant la session ; le JSON fige l'empreinte du bloc lu et le script se relance en ~25 s si la règle bouge encore.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py` | 1 | 25 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md` | 1 | 7 |

### Commandes exécutées (échantillon)

- **T1** Vérifier branche et arborescence
- **T1** Localiser les fonctions utiles
- **T1** Inspecter format gold
- **T1** Lancer l'évaluation gold actuelle
- **T1** Statistiques des cibles gold
- **T1** Extraire les chiffres d'attachement
- **T1** Diagnostic des cas prédits et erreurs
- **T1** Inspecter étiquettes et POS de cas clés
- **T1** Mesurer la couverture du vivier
- **T1** Tester des règles simples sur les 145 cas
- **T1** Déboguer r080
- **T1** Tester une règle manuelle par type/préposition
- **T1** Vérifier cibles auxiliaires et unicité
- **T1** Trouver fiches existantes sur l'attachement
- **T1** Lister fiches linguistiques
- **T1** Repérer les blocs à nettoyer
- **T1** Premier run du prototype
- **T1** Auditer les erreurs du modèle
- **T1** Run avec stabilité
- **T1** Recouvrement paraphrases et taille du vivier
- **T1** Localiser l'insertion des ablations
- **T1** Run avec ablations
- **T1** Vérifier convergence, poids et cohérence
- **T1** Repérer les défauts d'époques et le repère
- **T1** Mettre à jour les défauts d'époques
- **T1** Run convergence
- **T1** Vérifier convergence effective
- **T1** Sensibilité l2 et epochs
- **T1** Chercher la ligne roadmap attachement
- **T1** Vérifier doublons d'ids par segment
- **T1** Run final et compilation
- **T1** Voir si bloc_linguistique a changé
- **T1** Confirmer la règle live et l'empreinte
- **T1** Comparer les deux snapshots
- **T1** Lister les 6 changements de règle
- **T1** Vérifier stabilité du fichier
- **T1** Voir le diff courant
- **T1** Score de la règle live actuelle
- **T1** Run du modèle sur la règle à 137
- **T1** Détail du gain résiduel
- … et 21 autres

## 4. Mesures et résultats marquants

- **T1** `repères: {'exactitude_entrainement': 0.9931, 'rang0_justes': 139, 'rang0_taux': 0.9586}`
- **T1** `rang             -3.3357`
- **T1** `rang0 139`
- **T1** `rang              -3.2324  -3.4390 OK`
- **T1** `552:    rang0_ok = 0`
- **T1** `557:        rang0_ok += int(s["candidats"][0]["texte"] == s["cible"])`
- **T1** `559:              "rang0_justes": rang0_ok, "rang0_taux": _taux(rang0_ok, app_n)}`
- **T1** `repères: {'exactitude_entrainement': 0.9931, 'rang0_justes': 139, 'rang0_taux': 0.9586, 'rang0_par_type': {'GP': {'n': 83, 'justes': 78, 'taux': 0.9398}, 'REL': {'n': 26, 'justes': 26, 'taux': 1.0}, '`
- **T1** `rang             -3.3359`
- **T1** `rang              -3.2328  -3.4390  mm`
- **T1** `178:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes`
- **T1** `253:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `rang             -3.2459`
- **T1** `repere {'exactitude_entrainement': 0.9931, 'rang0_justes': 139, 'rang0_taux': 0.9586, 'rang0_par_type': {'GP': {'n': 83, 'justes': 78, 'taux': 0.9398}, 'REL': {'n': 26, 'justes': 26, 'taux': 1.0}, 'SU`
- **T1** `rang              -3.112  -3.380  -3.246`
- **T1** `modèle juste, rang0 faux: 3 ['g014', 'g016', 'g003']`
- **T1** `rang0 juste, modèle faux: 0 []`
- **T1** `règle juste, rang0 faux: 5 ['g014', 'g016', 'r048', 'r068', 'g003']`
- **T1** `rang0 juste, règle faux: 7 ['g002', 'g012', 'r018', 's108', 's122', 'r309', 's041']`
- **T1** `OK rang0 139`
- **T1** `5:> **142/145 (0,9793)** hors-pli contre **137/145 (0,9448)** pour la règle live (empreinte `6e843018`, 13:51) : **+5**, McNemar 7/2, **p = 0,18**, IC 95 % bootstrap **[-0,7 ; +7,6] pts** → **non sign`
- **T1** `3:> **Ligne de roadmap** : **B13** (moteur de pensée, attachement) · **Date** : 2026-11-05 · **Verdict** : ❌ **ne pas intégrer le classement appris en l'état** ; le signal utile est le **vivier ordonn`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : clés égales True 145 145 prédictions modèle différentes: 0 prédictions règle différentes: 6 viviers différents: 0 exact modèle 142 142 exact règle 123 129 == changements règle [stderr] Traceback (most
- **T1** : pas de ruff [exit code: 2]

