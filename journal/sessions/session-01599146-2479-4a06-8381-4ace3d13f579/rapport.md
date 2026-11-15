# Session session- — Tâche E2 : cas d'erreur tagger

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-01599146-2479-4a06-8381-4ace3d13f579` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 06:34 |
| Durée | 0.6 h |
| Tours | 1 |
| Messages | 138 |
| Appels d'outils | 167 |
| Fichiers touchés | 8 |
| Commandes | 95 |
| Sous-agents | 0 |
| Commits | 2 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche E2 : les cas d'erreur de `--tagger` — la clé absente (code 4), la clé invalide (code 4, message clair), le réseau coupé (code 4 ou repli heuristique ?), le refus du modèle ; documente le comportement **réel** de chacun dans `docs/produit/README.md` § 3.7 et une fiche `reports/rapport-tagger-erreurs.md` + JSON, avec un test pour chacun dans `tools/tests/test_tagger_api.py` (transport factice) … [9 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche E2 : les cas d'erreur de `--tagger` — la clé absente (code 4), la clé invalide (code 4, message clair), le réseau  … [289 caractères tronqués]

*167 appels d'outils.* Actions notables :

- bash — Check repo state and recent commits
- glob
- read
- bash — Find tagger implementation references
- bash — Find tagger code in drave.py
- bash — Find tagger classes in bloc_linguistique
- bash — Find tagger section in product README
- bash — Search for E2 task references
- bash — Read chantier plan
- bash — Read E2 plan entry
- bash — Inspect existing tagger reports
- bash — Search for error handling patterns
- bash — Check git history for tagger error handling
- bash — Find all tagger error docs in README
- … et 120 autres

**Synthèse produite :**

I'll implement the error-handling contract, then add the tests, docs and report. Let me set up a task list first.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `tools/drave.py` | 0 | 7 |
| `tools/tests/test_tagger_api.py` | 0 | 3 |
| `docs/produit/README.md` | 0 | 5 |
| `reports/rapport-tagger-erreurs.md` | 1 | 1 |
| `docs/pilotage/en-cours.md` | 0 | 10 |
| `docs/pilotage/roadmap.md` | 0 | 5 |
| `journal/2026-11-15/mesures.md` | 0 | 2 |
| `reports/rapport-tagger-erreurs.json` | 0 | 4 |

### Commandes exécutées (échantillon)

- **T1** Check repo state and recent commits
- **T1** Find tagger implementation references
- **T1** Find tagger code in drave.py
- **T1** Find tagger classes in bloc_linguistique
- **T1** Find tagger section in product README
- **T1** Search for E2 task references
- **T1** Read chantier plan
- **T1** Read E2 plan entry
- **T1** Inspect existing tagger reports
- **T1** Search for error handling patterns
- **T1** Check git history for tagger error handling
- **T1** Find all tagger error docs in README
- **T1** Probe actual CLI error behavior
- **T1** Find tests for NeuronalLLMPOS
- **T1** Find gates running tagger tests
- **T1** Find where tagger tests are invoked
- **T1** Inspect gate scripts
- **T1** Find Cascade class
- **T1** Check no-network default test
- **T1** Find network import guarantees
- **T1** Look at task mandate style
- **T1** Probe evaluer with invalid key
- **T1** Inspect recent report style
- **T1** Check import path for DeepSeek
- **T1** Verify new error behavior
- **T1** Run existing tagger tests
- **T1** Run tagger tests with new error cases
- **T1** Understand table gate
- **T1** Check current and commit dates
- **T1** Capture missing-key behavior
- **T1** Measure all error cases for the report
- **T1** Measure evaluer with network failure
- **T1** Run mutation negative control and restore
- **T1** Generate report JSON from measurements
- **T1** Generate report JSON (fixed)
- **T1** Run documentation review
- **T1** Run Markdown table gate
- **T1** Inspect en-cours counters and header
- **T1** Read en-cours relevant sections
- **T1** Find roadmap B13/R0.7 lines
- … et 55 autres

## 4. Mesures et résultats marquants

- **T1** `145:POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)`
- **T1** `148:  vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture`
- **T1** `reports/rapport-e2-croissance.md:47:| **E2** (cette fiche) | la croissance locale ne bat pas ce masque aléatoire à densité égale (+0,9 %) |`
- **T1** `reports/rapport-e1-e2-connectome-croissance.md:1:# E1 et E2, re-mesurés : le connectome aléatoire coûte 9 % (pas 1 %), et la croissance n'est PAS pire que le hasard`
- **T1** `reports/rapport-m2-secours.md:11:| casse (`E2E4`) | **98,67 %** | 92,88 % | 93,47 % | M1 gagne |`
- **T1** `reports/rapport-coherence-docs-2.md:100:| 41 | `docs/implantation/contexte-long.md:101-102` (E2) | KV int8 « **fait** (échelle par vecteur) », « mesuré : **+7,1 %** (llama.cpp : +3,1 %) » | le même do`
- **T1** `reports/rapport-coherence-vision.md:62:| `contexte-long.md` | **corrigé, 5 sites** | E1 mesuré (−20 % / −31 %) ; E2 et E3 aux valeurs **par bloc de 32** ; **E6 MLA « non testable » → validée** ; **E7 `
- **T1** `> **88,57 % → 97,14 %** sur 20 phrases `hand` (**+8,57 pts**), cohérent avec le **0,9475 contre`
- **T1** `2d7a7f2b 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5)`
- **T1** `ce7241d5 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS`
- **T1** `**86,25 % à 95,75 %** (**+9,5 pts**) ; sur le réel 452, de **88,91 % à 95,00 %** (**+6,1**).`
- **T1** `| **total** | **17** | **14/17 = 82,35 %** | **16/17 = 94,12 %** | **+2 tokens** |`
- **T1** `synthétiques. Le POS réel (**88,91 %**) est **meilleur** que le global (**86,25 %**) : le`
- **T1** `contrôle négatif « cible exacte tirée au hasard » est à **0,00 %** : c'est le plancher.`
- **T1** `"sortie": "drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)\nlangue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)\nPOS  Le/DET chat/NOUN dort/VER`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **5`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **att. 238/239**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../..`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](../..`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**`
- **T1** `35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1`
- **T1** `38:**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet`
- **T1** `288:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes`
- **T1** `363:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `devant, mais l'anglais est **100 % réel** quand le français ajoute **160 synthétiques** ; sur le`
- **T1** `| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |`
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) | `en-cours.md`, `README.md`, `
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) | `en-cours.md`, `README.md`, `me`
- **T1** ``0,5270` · `0,092` · `0,160` · `0,811` · `0,657` · `0,440` · `0,429` · `2,7856` · `40,0658` · `95,00 %` · `95,75 %``
- **T1** `-- **Fait** : B13 **183/183** ; **POS 86,25 %**, **att. 238/239**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../.`
- **T1** `+- **Fait** : B13 **183/183** ; **POS 86,25 %**, **att. 238/239**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../.`
- **T1** `porte-c4-retard        ✅                          32 s  PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne`
- **T1** `porte-coupe            ✅                         138 s    ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit`
- **T1** `porte-delais           ✅                          21 s    ✅ le temps, lui, augmente : 6.91 s → 9.67 s (+2.8 s ≈ 50 ms × 64 pas)`
- **T1** `[still running after 60000ms; moved to background job bash-87]`
- **T1** `31:| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |`
- **T1** `32:| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |`
- **T1** `[still running after 60000ms; moved to background job bash-95]`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 48, in <module>   File "<stdin>", line 7, in sans_stdout KeyError: 'commande' Traceback (most recent call last):   File "<frozen runp

## 6. Commits

- TAGGER — LES CAS D'ERREUR MESURÉS : CLÉ REFUSÉE → CODE 4 (AVANT 0), RÉSEAU ET RÉPONSE NON CONFORME → REPLI HEURISTIQUE CODE 0 ; 4/4 CAS, 18/18 CONTRÔLES" -m "Tâ
- TAGGER — LES CAS D'ERREUR MESURÉS : REFUS D'AUTHENTIFICATION → CODE 4 (AVANT 0), RÉSEAU ET RÉPONSE NON CONFORME → REPLI HEURISTIQUE CODE 0 ; 4/4 CAS, 18/18 CONT

