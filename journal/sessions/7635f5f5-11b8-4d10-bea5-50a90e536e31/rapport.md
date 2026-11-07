# Session 7635f5f5 — Tu travailles dans /home/stephane/Data13

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `7635f5f5-11b8-4d10-bea5-50a90e536e31` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 21:13 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 35 |
| Appels d'outils | 58 |
| Fichiers touchés | 0 |
| Commandes | 46 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état du chantier R** (le lecteur : R0.7 tagger, R1.2-1024, R44, R2/R3/R5) — lecture seule, aucun code.  Contexte : `docs/pilotage/roadmap.md` (R), `docs/pilotage/en-cours.md`, les fiches `reports/rapport-r*.md`, `tools/` (le tagger : `evaluer_tagger.py`? cherche), le modèle natif (`tools/native_model.py` … [1298 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état du chantier R** (le  … [1578 caractères tronqués]

*58 appels d'outils.* Actions notables :

- bash — Vérifier branche et état git
- bash — Lister fiches R et outils
- bash — Structure roadmap et taille docs
- bash — Chercher le tagger
- read
- bash — Chercher R1.2-1024
- bash — Chercher le tagger dans les fiches
- bash — Lister fiches R1.2/tagger et scripts
- bash — Chercher R1.2-1024 et chiffre 3,0107
- bash — Chercher commits R1
- bash — Lire table des tâches P8/P17
- bash — Localiser le code du tagger
- bash — Lister portes et outils R
- bash — Structure des fiches tagger
- … et 34 autres

**Synthèse produite :**

⏵ Inventaire du chantier R : lecture de la roadmap et de l'état courant

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Vérifier branche et état git
- **T1** Lister fiches R et outils
- **T1** Structure roadmap et taille docs
- **T1** Chercher le tagger
- **T1** Chercher R1.2-1024
- **T1** Chercher le tagger dans les fiches
- **T1** Lister fiches R1.2/tagger et scripts
- **T1** Chercher R1.2-1024 et chiffre 3,0107
- **T1** Chercher commits R1
- **T1** Lire table des tâches P8/P17
- **T1** Localiser le code du tagger
- **T1** Lister portes et outils R
- **T1** Structure des fiches tagger
- **T1** Chercher POS 85 et fichiers gold
- **T1** Inventaire des classes du bloc L
- **T1** Lire l'intro du paquet POS 85 %
- **T1** Voir le banc d'évaluation POS
- **T1** Inspecter les golds
- **T1** Rejouer l'évaluation POS du bloc L
- **T1** Compter les phrases et jetons des golds
- **T1** Lire les quatre lectures du JSON
- **T1** Compter les tokens du gold tagger
- **T1** Extraire POS des quatre lectures
- **T1** Rejouer la porte du bloc linguistique
- **T1** Inspecter la structure du JSON POS
- **T1** Vérifier artefacts N2 et tagger
- **T1** Lire les JSON des mesures R1.2 et tagger
- **T1** Vérifier présence du 7B
- **T1** Lire mesures tagger et contrôles
- **T1** Lire l'en-tête des portes R
- **T1** Lire la fiche pilote OCR
- **T1** Rejouer les portes R rapides
- **T1** Rejouer la porte des scans OCR
- **T1** Lister les fiches backlog R
- **T1** Vérifier le corpus OCR restauré
- **T1** Extraire les chiffres des portes vertes
- **T1** Lire statuts des fiches R2/R3/R5
- **T1** Lire les en-têtes des fiches R0
- **T1** Chiffres R0.2 et aides R0.3/R0.5
- **T1** Agrégat R0.2 et fiche multifichiers
- … et 6 autres

## 4. Mesures et résultats marquants

- **T1** `reports/rapport-r1-preparation.md:25:Dès que N2 livre sa hiérarchie, R1.1/R1.2 se mesurent sur les corpus préparés : les documents, le PDF, l'OCR et les dix corpus Wikipédia sont les entrées ; les éva`
- **T1** `reports/rapport-n2-r11.md:203:- **R1.2 n'est mesuré qu'à un budget** (5 000 pas × 512) : les mêmes pas que R1.1`
- **T1** `reports/rapport-n2-fenetre.md:32:| **R1.2-1 024** | `data/wiki_fr` | **1 024 / 1 024** | **2 500** | **20,5 Mo** | `base-wiki-45m` |`
- **T1** `reports/rapport-n2-fenetre.md:33:| R1.2-1 024 long | `data/wiki_fr` | 1 024 / 1 024 | 20 000 | 164 Mo | (suite du précédent) |`
- **T1** `reports/n2-fenetre.json:293:   "R1.2-1024": "wiki_fr, 1 024/1 024, 2 500 pas, 20,5 Mo, init base-wiki-45m",`
- **T1** `reports/n2-fenetre.json:294:   "R1.2-1024-long": "wiki_fr, 1 024/1 024, +17 500 pas (20 000), 164 Mo",`
- **T1** `docs/pilotage/en-cours.md:131:**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+ ; **S** — poursuivre la validation ; **N4** — consigne ; `
- **T1** `fff4825f ROADMAP — LA LEÇON DU CORPUS DE 831 Mo : LA DONNÉE DEMANDE PLUS DE PAS, PAS PLUS DE TEXTE`
- **T1** `015d7c56 B13 — LA PARTITION DES SYNTAGMES (P0-3) : meta.alternative PAR DÉFAUT (MESURES INCHANGÉES), filtrer EN OPTION (F1 +0,047) ; outside/feel CORRIGÉS, POS 85,00 %`
- **T1** `5c5d3b52 B13 — LE PAQUET POS SÛR (CLASSES FERMÉES + R4-EN) : POS 83,83 → 84,96 %, 37 CORRIGÉS / 0 CASSÉ, ATTACHEMENT INCHANGÉ ; 183/183`
- **T1** `e2258fb9 DOC PRODUIT — LES CHIFFRES À JOUR : POS 83,83 %, F1 64,74 %, ATTACHEMENT 235/236 (98,33 %), 3 SPANS ; SORTIE D'EVALUER REJOUÉE`
- **T1** `2ba393b0 B13 — LA POS À 83,83 % (R2a/R3/R2b) : F1 0,5849 → 0,6181, ANGLAIS 0,6341 → 0,7273, ATTACHEMENT INCHANGÉ (222/222) ; 183/183`
- **T1** `| P14 | A8.3 : réduire le lot ou l'assumer | roadmap:152 ; chantiers:84 | a26-lot-disque : 503 Mio constant, +27 % tok/s, PPL -0,006 % | Lot >= 2 assumé |`
- **T1** `reports/INDEX.md:608:| [rapport-pos-r4-integre.md](rapport-pos-r4-integre.md) | B13 — le paquet POS sûr : classes fermées anglaises + R4-en, POS 84,96 % |`
- **T1** `reports/rapport-partition-integree.md:8:> exact 235/236, POS 85,00 %** — les mesures de la base, **sans déduplication silencieuse**. Le mode`
- **T1** `reports/rapport-pos-r4-integre.md:1:# B13 — le paquet POS sûr : classes fermées anglaises + R4-en, POS 84,96 %`
- **T1** `reports/rapport-pos-r4.md:31:- **Paquet sûr** (R4-en + classes fermées) : **+1,19 dev / +1,11 test**, POS **85,00 %**, **37/0**,`
- **T1** `reports/rapport-pos-r4.md:408:   POS 85,00 %, 37/0, 2 faux→faux, F1 +0,0007, attachement 222/222. C’est le meilleur rapport`
- **T1** `reports/rapport-pos-r4.md:457:85,00 %** (dev 84,94 / test 85,11), **37 correctifs / 0 cassé / 2 faux→faux** : c’est exactement le`
- **T1** `reports/README.md:22:| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr : classes fermées + R4-en, **84,96 %** |`
- **T1** `- **R4 bilingue** : **+0,74 dev / +0,71 test** (POS 84,55 %), **23 correctifs / 0 cassé**, F1`
- **T1** `- **Classes fermées** : **+0,78 dev / +0,81 test** (POS 84,62 %), **25 correctifs / 0 cassé**,`
- **T1** `- **Paquet sûr** (R4-en + classes fermées) : **+1,19 dev / +1,11 test**, POS **85,00 %**, **37/0**,`
- **T1** `- **Paquet max** (R4 bilingue + classes fermées) : **+1,51 / +1,51**, POS **85,34 %**, **48/0**,`
- **T1** `# porte-lecteur.sh — R0.2 : à 30 % du budget, le contrôleur retrouve la réponse.`
- **T1** `# récupération ≥ 90 % à 30 % du budget, réponse préservée, hasard nettement plus bas, et`
- **T1** `# R4.4 — l'OCR lit dix pages à 4,48 % de WER, parité 90 %, et la page « photo » tombe à 26,7 %`
- **T1** `| A_RES_80_10-fr p2 | fra | 558 | **2,15 %** | 97,85 % | 94,3 | 5 |`
- **T1** `| A_RES_80_10-en p2 | eng | 546 | **1,10 %** | 98,90 % | 94,8 | 4 |`
- **T1** `| A_RES_80_10-es p2 | spa | 577 | **2,08 %** | 98,09 % | 94,5 | 4 |`
- **T1** `| A_RES_80_1-en p1 | eng | 294 | 4,76 % | 98,30 % | 93,5 | 3 |`
- **T1** `| A_RES_80_1-es p1 | spa | 326 | 5,52 % | 98,77 % | 92,9 | 3 |`
- **T1** `| A_RES_80_1-fr p1 | fra | 315 | 4,44 % | 99,68 % | 90,5 | 3 |`
- **T1** `| A_RES_80_10-en p1 | eng | 316 | 9,18 % | 93,04 % | 91,5 | 3 |`
- **T1** `| A_RES_80_10-es p1 | spa | 284 | 9,15 % | 94,72 % | 92,1 | 3 |`
- **T1** `| A_RES_80_10-fr p1 | fra | 305 | 12,13 % | 92,79 % | 89,4 | 2 |`
- **T1** `| A_RES_80_1-en p2 | eng | 250 | 0,40 % | 99,60 % | 95,7 | 0 |`
- **T1** `**Agrégat** : **3 771 mots**, **169 éditions** → **WER 4,48 %** · rappel **97,37 %** ·`
- **T1** `précision **97,82 %** · confiance moyenne pondérée par les mots **93,2**.`
- **T1** `| la **valeur** de la question est dans le passage choisi | **30/30 (100 %)** | **25/30 (83,33 %)** |`
- **T1** `| le **passage** choisi est le même (F1 mots ≥ 0,90) | — | **27/30 (90,00 %)** |`
- **T1** `| contrôle **sans OCR** (manifeste vide) | — | **0/30 (0,00 %)** |`
- **T1** `| **page dégradée** (photo simulée : 0,35× la définition, flou, JPEG q20, 0,8° de travers) | le WER monte, la parité baisse | **WER 17,08 %** contre 4,48 % · exactitude **12/30 (40 %)** · parité de pa`
- **T1** `Le contrôle dégradé est le plus important : **la parité tombe de 90 % à 26,7 %**. C'est la`
- **T1** `- L'OCR **lit le français, l'anglais et l'espagnol** d'un PDF propre à **4,48 %** de WER, avec une`
- **T1** `confiance **93,2** : le texte est là, et il est là **au bon endroit** (rappel 97,4 %).`
- **T1** `- La **parité de passage à 90 %** dit que le lecteur extractif de R0.2 se comporte presque`
- **T1** `- Le **contrôle dégradé** dit que ce n'est pas encore un lecteur de **scans** : 26,7 % de parité`
- **T1** `✅ à 30 % du budget, la lecture contrôlée récupère ≥ 90 % des passages de la`
- **T1** `4. coût        : ×4.05 de temps pour ×4 cellules (2.68 ms / 150 cellules)`
- **T1** `# R0.2 — le contrôleur de lecture : 100 % de récupération à 30 % du budget`
- **T1** `> **Verdict** : ✅ le contrôleur **préserve la lecture intégrale** à **30 %** du budget sur`
- **T1** `> 1,9 s/appel) ; budgets 10/30/50 % ; JSON bruts`
- **T1** `> porte 1 est franchie sur le lexical** (rappel@10 **0,984** ≥ 0,95) à **0,1 ms par requête** ;`
- **T1** `46:✅ à 30 % du budget, la lecture contrôlée récupère ≥ 90 % des passages de la`
- **T1** `{"modele": "drave-n0 34,3 M (384/512), RoPE, seq = fenêtre", "corpus": "data/wiki_fr/propre/train.txt (186 Mo) + canal", "budget": "20,5 Mo vus pour la loi (20 000 / 5 000 / 2 500 / 1 250 pas) ; 164 M`

