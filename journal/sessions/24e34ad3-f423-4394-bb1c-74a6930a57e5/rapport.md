# Session 24e34ad3 — Tu travailles dans /home/stephane/Data13

> **Journaux :** [le jour](../../2026-11-14/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `24e34ad3-f423-4394-bb1c-74a6930a57e5` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-14 09:53 |
| Durée | 1.5 h |
| Tours | 1 |
| Messages | 142 |
| Appels d'outils | 165 |
| Fichiers touchés | 5 |
| Commandes | 100 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **intégrer le tagger POS par API DeepSeek dans la CLI, en option** (décision 1A du 14/11). La mesure est faite : le tagger vaut **0,9475** contre **0,8625** pour l'heuristique sur le gold 612 (**+8,49 pts**), pour ~0,04 $ sur tout le corpus. Il faut l'exposer **sans** changer le défaut (hors ligne, … [2946 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **intégrer le tagge … [3226 caractères tronqués]

*165 appels d'outils.* Actions notables :

- bash — Vérifier l'état git et la branche
- bash — Compter les lignes des pièces clés
- read
- bash — Repérer les classes neuronales dans le bloc
- bash — Chercher le harnais qualifier_tagger_612
- bash — Lire le harnais 612 et l'évaluateur gold
- bash — Vérifier la présence de la clé et du cache
- bash — Lire les tests produit existants
- bash — Chercher la décision 1A et le chiffre du tagger
- bash — Chercher les rapports tagger existants
- bash — Lire le récit de mesure du 14/11
- bash — Inspecter le rapport tagger 612
- bash — Chercher la mention de la décision 1A
- bash — Lire l'état et la roadmap autour du tagger
- … et 124 autres

**Synthèse produite :**

⏵ Livraison terminée : option `--tagger`, mesure, tests et doc en place

**Commande**
```bash
python3 tools/drave.py analyser "TEXTE" --tagger [--json|--jsonl]
python3 tools/drave.py evaluer --tagger [--par-langue] [--json]
```
Clé : `DEEPSEEK_KEY_FILE` → `~/.config/drave/deepseek.key` → `DEEPSEEK_API_KEY` (repli `DSH_*`). Sans clé : code **4**, message clair, rien sur `stdout`, aucune trace de la clé. Cache mémoire par texte + cache disque du client : la seconde analyse ne refait aucun appel et rend le même JSON. Le défaut, sans le drapeau, est resté l'heuristique hors ligne (comparaison octet pour octet en test).

**Mesure** (20 premières phrases `hand`, 105 tokens, cache neuf)
- POS **0,8857 → 0,9714**, soit **+8,57 pts** (fermé +7,02, ouvert +10,42) ; syntagmes F1, tête, attachement et acte **inchangés** (la fusion ne remplace que le POS).
- **40 appels**, **11 868 tokens**, 39,49 s, 0 refus ; modèle renvoyé `deepseek-flash`.
- Cache chaud : 40 appels transport, **0 réseau, 0 token**, JSON identique.
- Référence 612 : **0,8625 → 0,9475 (+8,49)**, 1 218 appels, 358 962 tokens, ~21 min, ~0,04 $ ; par source : `hand` +8,57, **réel 432 +4,67**, `synth` +21,46 ; 1 refus (`s015`).

**Tests / portes**
- `tools/tests/test_tagger_api.py` : **14 tests OK**, aucun réseau (transport factice, POS remplacés, JSON v2 valide + v1 lisible, cache, défaut inchangé, code 4, ordre de la clé, `evaluer --tagger`).
- `tools/tests/test_produit.py` : **18 tests OK**.
- `revue_documentation` ✅ · `taille_documents` ✅ · `porte-produit` ✅ (183/183).

**Limites**
- Les 20 phrases sont les 20 `hand`, le sous-ensemble le plus facile : ne pas généraliser le +8,57 ; le 612 agrégé vaut +8,49 et le réel 432 seul +4,67.
- Le tagger de syntagmes du composite est appelé mais sa sortie n'est pas utilisée par la fusion (2 appels/phrase, piste 1 appel ~0,02 $ non mesurée).
- `PONCT` n'est plus étiqueté par l'option (le tagger ne reçoit que mots et nombres).
- Modèle effectivement renvoyé `deepseek-flash` ; la mesure exige un cache neuf.
- Aucune porte ne fait d'appel API : le chemin réseau réel est couvert par la mesure 20 phrases et un contrôle 1 phrase.

**État** : code, tests, fiche `reports/rapport-tagger-option.md` et JSON `reports/pensee-tagger-option.json` sont dans le commit `0bbdbbb3` (fait par la session parente). Restent non committées 3 lignes de `docs/produit/README.md` (note cache + lien § 8) ; la ligne R d'`en-cours` mérite d'être requalifiée (« route API derrière drapeau » → liv
… [52 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py` | 0 | 15 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py` | 1 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-option.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md` | 0 | 12 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 2 |

### Commandes exécutées (échantillon)

- **T1** Vérifier l'état git et la branche
- **T1** Compter les lignes des pièces clés
- **T1** Repérer les classes neuronales dans le bloc
- **T1** Chercher le harnais qualifier_tagger_612
- **T1** Lire le harnais 612 et l'évaluateur gold
- **T1** Vérifier la présence de la clé et du cache
- **T1** Lire les tests produit existants
- **T1** Chercher la décision 1A et le chiffre du tagger
- **T1** Chercher les rapports tagger existants
- **T1** Lire le récit de mesure du 14/11
- **T1** Inspecter le rapport tagger 612
- **T1** Chercher la mention de la décision 1A
- **T1** Lire l'état et la roadmap autour du tagger
- **T1** Lire la décision 1A
- **T1** Inspecter la doc produit
- **T1** Lire la porte produit et le registre des portes
- **T1** Repérer la fusion et les priorités
- **T1** Repérer Annotation.json
- **T1** Lire evaluer_bloc en entier
- **T1** Vérifier les packages et le schéma
- **T1** Lire le budget de contexte
- **T1** Lire la méthode de résultat/fiche
- **T1** Lancer le smoke test de base
- **T1** Lancer les portes doc de base
- **T1** Comprendre les compteurs de la revue
- **T1** Lire le comptage de la revue
- **T1** Lire les fonctions de comptage
- **T1** Compter les fiches et JSON sur disque
- **T1** Lire le vérificateur de schéma
- **T1** Vérifier fastjsonschema et l'import du client
- **T1** Vérifier la couverture de la phrase test
- **T1** Comparer cascade et cascade_niveau sur la pragmatique
- **T1** Comprendre l'interdiction de résultats dans docs
- **T1** Lire la navigation/orphelins de la revue
- **T1** Inspecter les index de reports
- **T1** Vérifier trace et cout dans les schémas
- **T1** Comparer syntagmes et attachement des modes
- **T1** Chercher une spécification existante du --tagger
- **T1** Chercher une tentative antérieure
- **T1** Lire la décision du parent sur le tagger
- … et 60 autres

## 4. Mesures et résultats marquants

- **T1** `docs/pilotage/roadmap.md:33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 c`
- **T1** `docs/pilotage/roadmap.md:354:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantiq`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `99:| [rapport-cache-chunker.md](rapport-cache-chunker.md) | Cache du chunker — validation indépendante : ×11,0 à 160 tokens, égalité 612/612 |`
- **T1** `journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:62049:| tagger API | — | **94,75 % (+8,49 pts)** — la décision R est tranchée |`
- **T1** `journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md:10467:| tagger API | — | **94,75 % (+8,49 pts)** — la décision R est tranchée |`
- **T1** `**Le constat.** Notre analyseur trouve la classe grammaticale de chaque mot avec **86,25 %** de justesse. Le même exercice confié à un modèle par API atteint **94,75 %** — soit **+8,5 points**, pour *`
- **T1** `- **C. Ne pas l'intégrer** : on garde 86,25 %, gratuit et hors ligne.`
- **T1** `langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `'12,5 %' [(0, 2, '12', 'nombre'), (2, 3, ',', 'ponctuation'), (3, 4, '5', 'nombre'), (5, 6, '%', 'ponctuation')]`
- **T1** `POS         exactitude 88.57 %  (fermé 87.72 %, ouvert 89.58 %)`
- **T1** `SYNTAGMES   F1 90.16 %  (P 83.33 % / R 98.21 %)`
- **T1** `tête      F1 97.39 %  (P 94.92 % / R 100.00 %)`
- **T1** `vue linéaire (partition filtrer) F1 82.57 %  · attachement 69.23 % de couverture`
- **T1** `ATTACHEMENT exact 92.31 % · couverture 92.31 % · exact sur span 100.00 % · top-k 92.31 %`
- **T1** `tête      couverture 100.00 % · top-k 100.00 %`
- **T1** `PRAGMATIQUE acte 100.00 % · négation 100.00 % · modalité 95.00 % · double sens 90.00 %`
- **T1** `FRACTION SÉMANTIQUE 48.35 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 23.08 % (graine 0, 13 cibles)`
- **T1** `POS         exactitude 97.14 % (fermé 94.74 %, ouvert 100.00 %) · Δ +8.57 pts vs heuristique`
- **T1** `SYNTAGMES   F1 90.16 % (tête 97.39 %) — conservés à l'heuristique`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `langue=fr script=Latn source=cascade · 19 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `[still running after 60000ms; moved to background job bash-4989]`
- **T1** `131:POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)`
- **T1** `134:  vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture`
- **T1** `| **la performance du cache** (×139, conditions) | [`reports/rapport-cache-chunker-applique.md`](../../reports/rapport-cache-chunker-applique.md) |`
- **T1** `POS         exactitude 100.00 % (fermé 100.00 %, ouvert 100.00 %) · Δ +0.00 pts vs heuristique`
- **T1** `SYNTAGMES   F1 90.91 % (tête 100.00 %) — conservés à l'heuristique`
- **T1** `POS 100.00 % (fermé 100.00 %, ouvert 100.00 %) · SYNTAGMES F1 90.91 % (tête 100.00 %)`
- **T1** `ATTACHEMENT exact 100.00 % · couverture 100.00 % · top-k 100.00 % · PRAGMATIQUE acte 100.00 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 100.00 % (graine 0, 1 cibles)`
- **T1** `TAGGER POS 100.00 % · Δ +0.00 pts · SYNTAGMES F1 90.91 % (tête 100.00 %)`
- **T1** `**La mesure.** Sur les **20 phrases `hand`** du gold (105 tokens) : POS **88,57 % → 97,14 %**`
- **T1** `(**+8,57 pts**), syntagmes et attachement **inchangés**. Sur le **gold 612** : **86,25 % →`
- **T1** `94,75 %** (**+8,49 pts**), mais le gain du seul **réel 432** est **+4,67** (le synthétique porte`
- **T1** `-- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../r`
- **T1** `+- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`, déclaré inatteignable le 14/11 — décision 2A)** ; **`s065` ré`
- **T1** `64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`, inatteignable)** ; **`s065` réglé** ; **`r035`**, **convent`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : #!/bin/bash # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait. # # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS # (`--attn-window` en r
- **T1** : #!/bin/bash # porte-deepseek.sh — le banc externe, sans réseau et sans clé. # # CE QU'ELLE VERROUILLE : #   1. les tests de l'adaptateur, du corpus professeur et de la distillation #      (transport f

