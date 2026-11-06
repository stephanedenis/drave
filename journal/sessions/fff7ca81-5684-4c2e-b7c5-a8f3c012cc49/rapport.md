# Session fff7ca81 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `fff7ca81-5684-4c2e-b7c5-a8f3c012cc49` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 21:12 |
| Durée | 1.0 h |
| Tours | 1 |
| Messages | 75 |
| Appels d'outils | 81 |
| Fichiers touchés | 8 |
| Commandes | 65 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **améliorer le top-k** de l'attachement (état `f908d7b0`) et le mesurer, sans modifier le code du dépôt.  Contexte : `tools/bloc_linguistique.py` (`Heuristique`, `_candidats_precedent`, `_verbes_proches`), `tools/tests/linguistique/evaluer_gold.py` (`evaluer_bloc`). État : 212 labels, exac … [1615 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **améliore … [1895 caractères tronqués]

*81 appels d'outils.* Actions notables :

- bash — Show branch, status, and top-level files
- bash — List linguistique tests and reports
- bash — Check sizes of key files and existing topk reports
- bash — Recent commits and references to state f908d7b0
- bash — Read existing topk diagnostic report
- bash — Read existing strict topk report
- read
- bash — Locate candidate functions in bloc_linguistique.py
- bash — Locate class and helpers
- bash — Run baseline gold evaluation
- bash — Print attachment metrics in full
- bash — Read gold split and loader
- bash — Count phrases and targets per gold file
- bash — Compare vivant vs gele attachment metrics
- … et 64 autres

**Synthèse produite :**

\## Résultat — top-k v8

Deux fichiers neufs, aucun existant modifié, aucun commit :
- [`reports/rapport-topk-v8.md`](reports/rapport-topk-v8.md)
- [`reports/pensee-topk-v8.json`](reports/pensee-topk-v8.json)

Mesure de départ confirmée : **212 labels, exact 212/212, top-k 177/239 = 0,7406** (dev 120/163 ; test 57/76). Les **62 échecs** se séparent en **27 spans non prédits** et **35 échecs de couverture de candidats**.

\### Les 5 motifs principaux

1. **Antécédent REL absent = 32/35 échecs de couverture** (26 EN + 6 FR). Cause précise : `prec = s` (l. 1148 et 1175) est exécuté **avant** `_candidats_precedent(texte, s, prec)` (l. 1154/1181) ; le helper reçoit le segment lui-même, la branche `REL → GN` est morte. La branche S ne l'appelle pas.
2. **Le choix est déjà bon 212/212** : le top-k rate par **incohérence de liste** (cible choisie absente des candidats), pas par décision d'attachement.
3. **R1 répare 34/35** avec les seuls GN prédits : **34 ajouts, 34 hits (100 %)**, +28 dev, +6 test.
4. **Résidus** : 2 GP hand (g002, g006), où la convention génitive existe dans `_repli_cible_gp` pour la cible mais pas pour les candidats ; 1 SUB r309 où « viendra » est tagué NOUN. Le « verbe de la principale » est déjà couvert par `_verbes_proches` (0 ajout, 0 gain).
5. **Plafond = couverture de span** : 27 spans (REL 16, SUB 6, GP 5 ; 19 synthétiques, 7 reel, 1 hand). Réel : 145/184 = 0,7880 → **176/184 = 0,9565**. Synthétique : 32/55 → **36/55 = 0,6545**.

\### Top-k dev/test par règle

| règle | dev | test | all | ajouts / hits |
|---|---:|---:|---:|---:|
| base | 120/163 | 57/76 | 177/239 | — |
| **R1** antécédent REL + GP génitif | **148/163 (+28)** | **63/76 (+6)** | **211/239 (+34)** | 34 / 34 |
| R2 verbe propre de SUB (si aucun candidat verbal) | 120/163 (0) | 58/76 (+1) | 178/239 (+1) | 19 / 1 |
| R3 voisinage POS VERB ≤ 3 | 120/163 (0) | 57/76 (0) | 177/239 (0) | 2 / 0 |
| **R1+R2** | **148/163 (+28)** | **64/76 (+7)** | **212/239 (+35)** | 53 / 35 |

Pertes **0** partout (complétion additive) ; exact inchangé **212/212**. Coût : 2,434 → 2,684 candidats/label (max 5 inchangé).

\### Contrôles négatifs

Permutation croisée des listes **1,82/239** ; hasard global **5,49** ; hasard typé langue+type **24,36** ; permutation des seuls ajouts **177,11** ; hasard des seuls ajouts **177,30** — retour à la base. Brasser l'ordre intra-liste laisse **212** : le top-k est insensible à l'ordre, il ne mesure pas le classement.

\### Recommandation

1. Corriger le site d'app
… [925 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/topk_v8_diag.py` | 1 | 0 |
| `/tmp/topk_v8_rules.py` | 1 | 0 |
| `/tmp/topk_v8_controls.py` | 1 | 0 |
| `/tmp/topk_v8_final.py` | 1 | 0 |
| `/tmp/topk_v8_variantes.py` | 1 | 0 |
| `/tmp/topk_v8_refined.py` | 1 | 0 |
| `/tmp/topk_v8_build_json.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-v8.md` | 1 | 3 |

### Commandes exécutées (échantillon)

- **T1** Show branch, status, and top-level files
- **T1** List linguistique tests and reports
- **T1** Check sizes of key files and existing topk reports
- **T1** Recent commits and references to state f908d7b0
- **T1** Read existing topk diagnostic report
- **T1** Read existing strict topk report
- **T1** Locate candidate functions in bloc_linguistique.py
- **T1** Locate class and helpers
- **T1** Run baseline gold evaluation
- **T1** Print attachment metrics in full
- **T1** Read gold split and loader
- **T1** Count phrases and targets per gold file
- **T1** Compare vivant vs gele attachment metrics
- **T1** Run topk diagnostic, first part
- **T1** See remaining failure details
- **T1** List coverage failures compactly
- **T1** Cross-tabs and GP detail
- **T1** Inspect annotations for representative failures
- **T1** Run completion-rule simulation
- **T1** Fix split test and rerun
- **T1** Rerun and print compact rule results
- **T1** Exact cross-tabs for span vs coverage failures
- **T1** Patch and run noise/control script
- **T1** Fix script and show noise stats
- **T1** Show R2/R3 noise and controls
- **T1** Show control results
- **T1** Dev/test balance and target counts
- **T1** Run consolidated measurement
- **T1** Fix and rerun consolidated measurement
- **T1** Fix tuple keys and rerun
- **T1** Inspect final results JSON
- **T1** Verify target files are new
- **T1** Read verb lexicon and _est_verbe
- **T1** Check date convention and last commit
- **T1** Look at latest v7 coverage report style
- **T1** Check code drift since f908d7b0
- **T1** Quantify PP ambiguity of nearest-GN rule on REL
- **T1** R1 additions and precision by type
- **T1** Dedup additions by label key
- **T1** R1 additions by base success and hit
- … et 25 autres

