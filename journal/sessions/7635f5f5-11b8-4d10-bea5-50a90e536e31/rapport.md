# Session 7635f5f5 — Tu travailles dans /home/stephane/Data13

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `7635f5f5-11b8-4d10-bea5-50a90e536e31` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 21:13 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 16 |
| Appels d'outils | 24 |
| Fichiers touchés | 0 |
| Commandes | 16 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état du chantier R** (le lecteur : R0.7 tagger, R1.2-1024, R44, R2/R3/R5) — lecture seule, aucun code.  Contexte : `docs/pilotage/roadmap.md` (R), `docs/pilotage/en-cours.md`, les fiches `reports/rapport-r*.md`, `tools/` (le tagger : `evaluer_tagger.py`? cherche), le modèle natif (`tools/native_model.py` … [1298 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état du chantier R** (le  … [1578 caractères tronqués]

*24 appels d'outils.* Actions notables :

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
- … et 3 autres

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

