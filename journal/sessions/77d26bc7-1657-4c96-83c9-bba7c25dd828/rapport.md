# Session 77d26bc7 — Tu travailles dans /home/stephane/Data13

> **Journaux :** [le jour](../../2026-11-07/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `77d26bc7-1657-4c96-83c9-bba7c25dd828` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-07 00:49 |
| Durée | 0.0 h |
| Tours | 1 |
| Messages | 12 |
| Appels d'outils | 16 |
| Fichiers touchés | 0 |
| Commandes | 14 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **re-auditer le produit sur les textes libres** avec le code de la nuit (23 h 30 → 00 h 50), en lecture seule.  Contexte : `tools/drave.py` (CLI : `analyser`, `--fichier`, `--jsonl`, `--partition`), `tools/bloc_linguistique.py`. Les audits précédents : `reports/rapport-fiabilite-produit.md` (50 tex … [1811 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **re-auditer le pro … [2091 caractères tronqués]

*16 appels d'outils.* Actions notables :

- bash — Vérifier branche et état du dépôt
- bash — Vérifier existence des fichiers clés
- read
- bash — Inspecter la structure des JSON d'audit
- bash — Inspecter banc_50.resultats
- bash — Lire le rapport de fiabilité existant
- bash — Suite du rapport fiabilité
- bash — Voir les commits de la nuit
- bash — Repérer contrat et frontières dans le module
- bash — Lire contrat et robustesse du JSON
- bash — Lire la logique de frontières de phrase
- bash — Lire le découpage de phrases actuel
- bash — Lire le dispositif des 40 frontières
- bash — Tester la CLI actuelle
- … et 1 autres

**Synthèse produite :**

⏵ Cartographie du dépôt et des audits existants avant de rejouer les textes

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Vérifier branche et état du dépôt
- **T1** Vérifier existence des fichiers clés
- **T1** Inspecter la structure des JSON d'audit
- **T1** Inspecter banc_50.resultats
- **T1** Lire le rapport de fiabilité existant
- **T1** Suite du rapport fiabilité
- **T1** Voir les commits de la nuit
- **T1** Repérer contrat et frontières dans le module
- **T1** Lire contrat et robustesse du JSON
- **T1** Lire la logique de frontières de phrase
- **T1** Lire le découpage de phrases actuel
- **T1** Lire le dispositif des 40 frontières
- **T1** Tester la CLI actuelle
- **T1** Lister les 50 textes du banc

## 4. Mesures et résultats marquants

- **T1** `| temps CLI (50 phrases) | **136,8–226,6 ms**, médiane **152,7 ms** |`
- **T1** `| temps interne (API) | **0,2–45,1 ms**, médiane **1,0 ms** |`
- **T1** `langue=und script=Latn source=heuristique · 13 étiquettes · unités sémantiques=2 (85.7% du texte)`
- **T1** `Le **démarrage** (`--version`, 10 passages) coûte **134–192 ms**, médiane **146 ms**. Pour une`
- **T1** `phrase courte, **plus de 95 % du temps CLI est le démarrage**, pas l'analyse (0,8 ms pour f01).`
- **T1** ``evaluer` coûte **530–543 ms** sur le gold vivant et **577–600 ms** avec `--gold` ; `rejouer``
- **T1** `**146–149 ms**. Les cinq textes les plus lents en CLI`
- **T1** `sont f50 (226,6 ms), f02 (193,8), f05 (181,6), f35 (180,3), f44 (179,1) — l'ordre est surtout`
- **T1** `du bruit de démarrage, sauf f50. En interne, les plus lents sont f50 (45,1 ms), f43 (7,9),`
- **T1** `Le coût est **superlinéaire** (×16,4 de temps pour ×5 de texte entre 10 k et 50 k) ; à 10 000`
- **T1** `caractères, le CLI reste sous la seconde, mais le JSON fait **2,76 Mo** (indenté). Un document`
- **T1** `de 50 000 caractères coûte **5,4 s** et **11,5 Mo** : il n'y a ni plafond ni mode compact.`
- **T1** `| 10 000 car., phrases répétées | 0 | **590–765 ms** | 10 362 | **2 763 666 o** | spans valides, déterminisme |`
- **T1** `| 10 000 car., `a` × 10 000 | 0 | **172 ms** | 7 | 42 482 o | un seul token |`
- **T1** `| 10 000 car., ponctuation | 1 | **155 ms** | — | 0 | refus `vide` (raison fausse) |`
- **T1** `| mode lisible, `a` × 10 000 | 0 | 153 ms | — | 10 457 o | **ligne de 10 010 caractères** |`
- **T1** `10. **Taille et lot** : 2,76 Mo pour 10 000 caractères, 11,5 Mo pour 50 000 ; une invocation =`
- **T1** `26c7b7ab 07 00:16 ROADMAP ET JOURNAL — LA NUIT FINIT À F1 0,7535, POS 86,25 %, 236/237, COUVERTURE 0,9916 ; LA CONVENTION DU SUJET`
- **T1** `5a067ba5 06 23:45 ROADMAP ET JOURNAL — LA NUIT FINIT À 236/237, COUVERTURE 0,9916, POS 86,25 %, 2 SPANS ; r264 RÉGLÉ`
- **T1** `ba42d4cc 06 23:26 FICHE — LES TROIS RÈGLES REJETÉES (PARTICIPES, R4-FR GÉNÉRIQUE, PARTICIPE APRÈS AVOIR) ; POS RESTE À 86,25 %`
- **T1** `c43dd5cc 06 23:23 B13 — LA RÈGLE « QUE » (PRON APRÈS UN NOM, CONJ AILLEURS) : POS 85,84 → 86,25 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `6432bdb9 06 23:09 JOURNAL ET ROADMAP — LA NUIT DES ÉTATS : N2/S/R/A INVENTORIÉS, FRONTIÈRE CORRIGÉE (A6.2 LIBRE), POS 85,84 %, PONCT, R4-FR ; ÉTAT HORODATÉ`
- **T1** `6b976cb1 06 23:05 B13 — R4-FR FILTRÉ (ADJECTIF CONNU OU SUFFIXE) : POS 85,75 → 85,84 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `7a45325f 06 22:57 B13 — LA PONCTUATION A UNE POS (PONCT) : POS 85,00 → 85,75 %, MIROIR 0,196 → 0,2276, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `bfd98892 06 21:32 DOC PRODUIT — RESYNCHRONISÉE : POS 85,00 %, F1 0,6482, ATTACHEMENT 235/236, GELÉ 85,32 / 0,6511 ; SORTIE D'EVALUER REJOUÉE`
- **T1** `bb67dd59 06 21:14 ÉTAT ET JOURNAL — LA NUIT DES P0 : POS 85,00 %, ATTACHEMENT 235/236, FRONTIÈRES 0/40, PARTITION ÉTIQUETÉE, CONTRAT V1`
- **T1** `"Taille : 2,76 Mo de JSON pour 10 000 caractères (10 362 étiquettes) ; pas de JSONL, pas de lot, une invocation = un texte.",`

