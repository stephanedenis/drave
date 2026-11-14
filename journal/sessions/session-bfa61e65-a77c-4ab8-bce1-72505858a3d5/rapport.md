# Session session- — Corriger span g017 avec règle adverbe

> **Journaux :** [le jour](../../2026-11-14/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-bfa61e65-a77c-4ab8-bce1-72505858a3d5` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-14 00:41 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 99 |
| Appels d'outils | 126 |
| Fichiers touchés | 1 |
| Commandes | 109 |
| Sous-agents | 0 |
| Commits | 2 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J6.1 : le dernier span du gold, `g017` (« She said that she would come yesterday. ») — le gold attend la SUB « that she would come » (sans « yesterday »), le bloc l'inclut. Reproduis, propose UNE règle mesurée (l'adverbe final de temps hors de la SUB), vérifie dev/test et l'attachement, fiche `reports/rapport-g017.md` + JSON, commit. Si la règle casse autre chose, écris la fiche du rejet.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J6.1 : le dernier span du gold, `g017` (« She said that she would come yesterday. ») — le gold attend la SUB « tha … [277 caractères tronqués]

*126 appels d'outils.* Actions notables :

- bash — Inspect repo root and git state
- bash — List reports and pilotage docs
- bash — Find files mentioning g017
- bash — Find the sentence
- read
- job_kill
- grep
- bash — List linguistics tools
- bash — Show g017 gold JSON
- bash — Check file sizes and gate script
- bash — Read evaluator start
- bash — Read evaluator rest
- bash — Reproduce g017 prediction vs gold
- bash — Inspect Etiquette class
- … et 100 autres

**Synthèse produite :**

**J6.1 terminé — règle mesurée puis rejetée.**

\## Reproduction

`g017` : le bloc prédit `SUB 9:38` (« that she would come **yesterday** ») alors que le gold attend `SUB 9:28` (« that she would come »). La cible d'attachement `said` était déjà correcte : le défaut est le span, pas l'attachement.

\## La règle mesurée

Retirer le dernier token d'une SUB quand c'est un adverbe de `ADVERBES_TEMPS` (`hier`, `demain`, `yesterday`, `tomorrow`…) suivi d'une ponctuation ou de la fin.

| mesure | base | règle | Δ |
|---|---:|---:|---:|
| F1 all | 0,7902 | 0,7901 | −0,0001 |
| F1 dev | 0,7875 | 0,7886 | **+0,0011** |
| F1 test | 0,7962 | 0,7934 | **−0,0028** |
| tp / fp / fn | 1480 / 403 / 383 | 1479 / 402 / 384 | −1 / −1 / +1 |
| attachement | 237/238 | 236/237 | −1 |
| couverture | 0,9958 | 0,9916 | −0,0042 |

La règle corrige `g017` et retire un faux positif de `g005`, mais **casse `r264`** (« qu'il vient demain ») et **`r288`** (« that he comes tomorrow »). Les deux cas favorables sont en **dev**, les deux défavorables en **test** : le gain est in-sample, la perte est hors échantillon. Contrôles : placebo 0,7107 ; ADV large 0,7885 ; variante gardée 0,7909 / 238/239 mais réglée sur 2 cas de dev, non retenue.

\## Décision

La convention du gold est contradictoire sur la même construction : `g005`/`g017` excluent l'adverbe final, `r264`/`r288` l'incluent. **Aucun code de production modifié** ; l'état reste à **237/238 (0,9958)**, F1 **0,7902**. `g017` reste un span, mais c'est désormais une **convention à trancher**, pas une règle de code. Prochaine action : trancher la convention, puis `s065` (J6.2).

\## Livrables

- Fiche de rejet : [`reports/rapport-g017.md`](reports/rapport-g017.md)
- JSON : [`reports/pensee-g017.json`](reports/pensee-g017.json)
- État : `docs/pilotage/en-cours.md` (J6.1, prochaine action)
- Journal : `journal/2026-11-14/README.md`
- Commit : **`64d9dd23`**

Portes : `porte-bloc-linguistique` **verte**, revue de documentation, `porte-tableaux`, budget T0 (**3 995 / 4 000**), `verifie_en_cours`, `verifie_journal` et `verifier_schemas` **verts**.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-g017.md` | 1 | 1 |

### Commandes exécutées (échantillon)

- **T1** Inspect repo root and git state
- **T1** List reports and pilotage docs
- **T1** Find files mentioning g017
- **T1** Find the sentence
- **T1** List linguistics tools
- **T1** Show g017 gold JSON
- **T1** Check file sizes and gate script
- **T1** Read evaluator start
- **T1** Read evaluator rest
- **T1** Reproduce g017 prediction vs gold
- **T1** Inspect Etiquette class
- **T1** Reproduce g017 prediction vs gold
- **T1** Read gold split logic
- **T1** Find gold SUB spans ending in ADV
- **T1** Read current state doc
- **T1** Inspect spans JSON keys
- **T1** Baseline metrics on all/dev/test
- **T1** Find prior final-adverb reports
- **T1** Search convention GV references
- **T1** Measure blanket final-time-adverb rule
- **T1** Diff predicted segments precisely
- **T1** Read bloc imports
- **T1** Find sys.path/import in bloc
- **T1** Remeasure with correct RACINE
- **T1** Check dev/test membership of key phrases
- **T1** Find J6 context in plans
- **T1** Read Pensée session plan
- **T1** Inspect gold segments of key phrases
- **T1** Measure guarded variant and placebo
- **T1** Run bloc linguistique gate baseline
- **T1** Find test references to key sentences
- **T1** Inspect autotest SUB tests
- **T1** Read autotest span tests
- **T1** Find prior rejection sheets and g017 mentions
- **T1** Read g017 history in audit r1r3
- **T1** Read g017 history in audit v10
- **T1** Find predicate guards
- **T1** Git history of predicate guard
- **T1** Check if autotest is a gate
- **T1** Inspect gate registry
- … et 69 autres

## 4. Mesures et résultats marquants

- **T1** `[still running after 60000ms; moved to background job bash-3]`
- **T1** `[still running after 60000ms; moved to background job bash-4]`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 te`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV réglée** (sujet hors du GV +`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `- **Note** : l'attachement est à **236/237 (0,9916)**, la couverture 0,9916, POS **86,25 %**, F1 **0,7535**, 2 spans ; la seule rouge est`
- **T1** `CPU + neuronal de contrat, parallèle/cascade, activation 51–76 %) ; **398 langues à 0,9687**,`
- **T1** `**tête 0,560**, pragmatique **1,0/1,0/0,994/0,889** ; cascade (mock) **67,1 %** ;`
- **T1** `- **Un seul split déterministe** (`crc32 % 3`), sans validation croisée ; les chiffres`
- **T1** `c43dd5cc B13 — LA RÈGLE « QUE » (PRON APRÈS UN NOM, CONJ AILLEURS) : POS 85,84 → 86,25 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `6b976cb1 B13 — R4-FR FILTRÉ (ADJECTIF CONNU OU SUFFIXE) : POS 85,75 → 85,84 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `7a45325f B13 — LA PONCTUATION A UNE POS (PONCT) : POS 85,00 → 85,75 %, MIROIR 0,196 → 0,2276, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `38:**État au 07/11 18 h 30.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) rég`
- **T1** `180:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes`
- **T1** `255:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV réglée** (sujet hors du G`
- **T1** `(R² 0,30) — la surface capte l'époque ; tout test de style contrôle la date, tout test de famille`
- **T1** `"Le split est un seul découpage déterministe (crc32 % 3), sans validation croisée.",`
- **T1** `- DOC PRODUIT — LES CHIFFRES À JOUR : POS 83,83 %, F1 64,74 %, ATTACHEMENT 235/236 (98,33 %), 3 SPANS ; SORTIE D'EVALUER REJOUÉE" -- docs/produit/README.md docs/p`
- **T1** `- B13 — LE PAQUET POS SÛR (CLASSES FERMÉES + R4-EN) : POS 83,83 → 84,96 %, 37 CORRIGÉS / 0 CASSÉ, ATTACHEMENT INCHANGÉ ; 183/183" -- tools/bloc_linguistique.py to`
- **T1** `- B13 — LA PARTITION DES SYNTAGMES (P0-3) : meta.alternative PAR DÉFAUT (MESURES INCHANGÉES), filtrer EN OPTION (F1 +0,047) ; outside/feel CORRIGÉS, POS 85,00 %"`
- **T1** `- ÉTAT ET JOURNAL — LA NUIT DES P0 : POS 85,00 %, ATTACHEMENT 235/236, FRONTIÈRES 0/40, PARTITION ÉTIQUETÉE, CONTRAT V1" -- docs/pilotage/en-cours.md journal/2026`
- **T1** `- DOC PRODUIT — RESYNCHRONISÉE : POS 85,00 %, F1 0,6482, ATTACHEMENT 235/236, GELÉ 85,32 / 0,6511 ; SORTIE D'EVALUER REJOUÉE" -- docs/produit/README.md 2>&1 | tai`
- **T1** `- B13 — LA PONCTUATION A UNE POS (PONCT) : POS 85,00 → 85,75 %, MIROIR 0,196 → 0,2276, F1 ET ATTACHEMENT INCHANGÉS ; 183/183" -- tools/bloc_linguistique.py tools/`
- **T1** `- B13 — R4-FR FILTRÉ (ADJECTIF CONNU OU SUFFIXE) : POS 85,75 → 85,84 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183" -- tools/bloc_linguistique.py tools/pensee/autotest`
- **T1** `- JOURNAL ET ROADMAP — LA NUIT DES ÉTATS : N2/S/R/A INVENTORIÉS, FRONTIÈRE CORRIGÉE (A6.2 LIBRE), POS 85,84 %, PONCT, R4-FR" -- journal/2026-11-06/README.md docs/`
- **T1** `- JOURNAL ET ROADMAP — LA NUIT DES ÉTATS : N2/S/R/A INVENTORIÉS, FRONTIÈRE CORRIGÉE (A6.2 LIBRE), POS 85,84 %, PONCT, R4-FR ; ÉTAT HORODATÉ" -- journal/2026-11-06`
- **T1** `- B13 — LA RÈGLE « QUE » (PRON APRÈS UN NOM, CONJ AILLEURS) : POS 85,84 → 86,25 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183" -- tools/bloc_linguistique.py tools/pens`
- **T1** `- FICHE — LES TROIS RÈGLES REJETÉES (PARTICIPES, R4-FR GÉNÉRIQUE, PARTICIPE APRÈS AVOIR) ; POS RESTE À 86,25 %" -- reports/rapport-pos-ponctuation.md docs/pilotag`
- **T1** `- ROADMAP ET JOURNAL — LA NUIT FINIT À 236/237, COUVERTURE 0,9916, POS 86,25 %, 2 SPANS ; r264 RÉGLÉ" -- docs/pilotage/roadmap.md journal/2026-11-06/README.md doc`
- **T1** `- ROADMAP ET JOURNAL — LA NUIT FINIT À F1 0,7535, POS 86,25 %, 236/237, COUVERTURE 0,9916 ; LA CONVENTION DU SUJET" -- docs/pilotage/roadmap.md journal/2026-11-06`
- **T1** `48 37 - **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référ`
- **T1** `63 112 - **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902*`
- **T1** `132 26 - **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (err`
- **T1** `133 27 - **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (a`

## 5. Erreurs rencontrées

4 sorties en erreur ou divergentes. Les premières :

- **T1** : texte: She said that she would come yesterday. gold segments: [('GN', 0, 3, 'She', None), ('GV', 4, 8, 'said', None), ('SUB', 9, 28, 'that she would come', ['said'])] pred segments: [stderr] Traceback
- **T1** : 8eb0cc49 B13 — RESTITUTION v0 : 46/46 SURFACES EXACTES, MIROIR STRICT 0,1087, LE MIROIR TROUVE LES SAUTS DE LIGNE 9a259953 B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 ÉCHEC)
- **T1** : (no output) [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "/tmp/g017/mesure.py", line 218, in <module>     sortie.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")           

## 6. Commits

- J6.1 — g017 : LA RÈGLE DE L'ADVERBE FINAL HORS SUB EST REJETÉE (G017 GAGNÉ EN DEV, R264/R288 PERDUS EN TEST ; F1 0,7901, TEST −0,0028, ATTACHEMENT 236/237) ; CO
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF' import pathlib p=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text() old='**Mis à

