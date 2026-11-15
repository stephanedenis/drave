# Session session- — Rédiger la FAQ produit D3

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-3ee08872-fd34-4732-af49-0639cb5d82a9` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 05:53 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 128 |
| Appels d'outils | 173 |
| Fichiers touchés | 6 |
| Commandes | 148 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche D3 : la FAQ du produit — 10 questions qu'un utilisateur se pose (la langue, le hors-ligne, le coût, le tagger, le schéma, l'attachement, les spans inatteignables, la restitution, les limites, l'installation) avec les réponses **vérifiées** contre le code courant ; dans `docs/produit/README.md` (une section FAQ) + fiche `reports/rapport-faq.md` + JSON, commit.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche D3 : la FAQ du produit — 10 questions qu'un utilisateur se pose (la langue, le hors-ligne, le coût, le tagger, le  … [247 caractères tronqués]

*173 appels d'outils.* Actions notables :

- bash — Inspect repo state and recent commits
- bash — Check docs/produit and reports
- bash — Check sizes and current diff stat
- bash — Locate D3 references
- bash — Read D3 plan block
- bash — Read current state
- read
- bash — Show uncommitted doc changes
- bash — Check hooks and product gate
- bash — Read rest of product gate
- bash — Read pre-commit hook
- bash — Run CLI help and basic analysis
- bash — Inspect tagger/network code
- bash — Read top of drave.py
- … et 153 autres

**Synthèse produite :**

\## D3 — livré et commité

**Livrables**
- **FAQ** : `docs/produit/README.md` **§ 8** — les 10 questions demandées (langue, hors-ligne, coût, tagger, schéma, attachement, spans inatteignables, restitution, limites, installation), réponses adossées au code et aux fiches.
- **Fiche** : `reports/rapport-faq.md` — dispositif, tableau des 10 contrôles, sorties observées, contrôle négatif, ce qui pourrait rendre les réponses fausses.
- **JSON** : `reports/faq.json` — relevé complet (`observe`, `ok`, `erreur`, `controle_negatif`).
- **Vérificateur** : `tools/verifier_faq.py` — 10 contrôles exécutables, `--json`, `--autotest`.

**Vérification**
```text
python3 tools/verifier_faq.py
FAQ produit — 10/10 réponses vérifiées · contrôle négatif détecté
✅ FAQ vérifiée
```
Le contrôle négatif est réel : `--langue de` sort **2** et le schéma v2 **refuse** une annotation v1. Les chiffres cités restent ceux des fiches : **238/239** cibles (0,9958), `g017` **[9:28] attendu / [9:38] prédit** (règle rejetée, F1 0,7901), restitution v0 **46/46**, v1 **46/46**, v2 **19/46** cadres (**16** non vides, F1 0,5270), tagger **609 appels / 22 299 tokens / 155 s / ~0,02 $**.

**Contrôles passés**
- `bash tools/porte-produit.sh` → **✅ porte produit verte** (15 contrôles, autotest **183/183**)
- `python3 tools/revue_documentation.py` → ✅
- `bash tools/porte-tableaux.sh` → ✅
- `python3 tools/taille_documents.py` → ✅ (T0 **4000/4000**)
- `python3 tools/verifie_en_cours.py` → ✅

**Commit**
`5b2d07fc` — *D3 — LA FAQ DU PRODUIT : 10/10 RÉPONSES VÉRIFIÉES CONTRE LE CODE (10 CONTRÔLES, NÉGATIF DÉTECTÉ) ; D2 — LA RESTITUTION V2 (19/46 CADRES, F1 0,5270)*

Le commit inclut aussi **D2**, qui était déjà dans l’arbre et référencé par `en-cours`. Les **15 fichiers restants** non commités sont le travail en attente d’autres tâches (INDEX/README, anciens rapports, `gold-reel-50`, `s-paragraphes`).

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py` | 1 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-faq.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 8 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/mesures.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** Inspect repo state and recent commits
- **T1** Check docs/produit and reports
- **T1** Check sizes and current diff stat
- **T1** Locate D3 references
- **T1** Read D3 plan block
- **T1** Read current state
- **T1** Show uncommitted doc changes
- **T1** Check hooks and product gate
- **T1** Read rest of product gate
- **T1** Read pre-commit hook
- **T1** Run CLI help and basic analysis
- **T1** Inspect tagger/network code
- **T1** Read top of drave.py
- **T1** Read main and parser definition
- **T1** Read parser options
- **T1** Search offline tests
- **T1** Read tagger report
- **T1** Read restitution v2 report
- **T1** Read restitution v0/v1 reports
- **T1** Search install info
- **T1** Inspect schema v2
- **T1** Read reports conventions
- **T1** Read reports index top
- **T1** Run evaluer JSON and inspect keys
- **T1** Run schema verifier JSON
- **T1** Test language behavior and exit codes
- **T1** Test tagger without key exit 4
- **T1** Run restitution v0 bench JSON
- **T1** Run restitution v2 bench JSON
- **T1** Run single restitution JSON
- **T1** Inspect tagger option JSON
- **T1** Print restitution synthesis
- **T1** Print tagger 612 reference
- **T1** Inspect roles JSON structure
- **T1** Inspect updated tagger figures
- **T1** Locate current tagger cost figures
- **T1** Check packaging and Python version requirements
- **T1** Read repo README install section
- **T1** Check available Python versions
- **T1** Check Python 3.10 syntax usage
- … et 108 autres

## 4. Mesures et résultats marquants

- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **5`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 canoniq`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](../..`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `-**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet d`
- **T1** `+**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet d`
- **T1** `langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `> **88,57 % → 97,14 %** sur 20 phrases `hand` (**+8,57 pts**), cohérent avec le **0,9475 contre`
- **T1** `- **Classe tirée au hasard** (12 classes, graine 0) : **10,48 %** ; **classe majoritaire**`
- **T1** `(`VERB`) : **22,86 %**. Le tagger (97,14 %) et l'heuristique (88,57 %) sont très au-dessus :`
- **T1** `> **65,84 % des jetons** et **75,19 % des caractères** ; stabilité structurelle`
- **T1** `fidélité    : exacte 1.0000 · caractères 1.0000 · couverture 100.00%`
- **T1** `mots        : exacte 0.0000 · caractères 0.9286 · couverture 84.62%`
- **T1** `pos         : exacte 0.0000 · caractères 0.9286 · couverture 84.62%`
- **T1** `de caractères (0,9286) dit, elle, que 93 % des caractères sont au bon endroit.`
- **T1** `22:| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |`
- **T1** `41:| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `| [`rapport-pos-anglais-v2.md`](rapport-pos-anglais-v2.md) | **B13** — POS **83,83 %** (R2a/R3/R2b), F1 **0,6181** |`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `| [rapport-a83-defaut.md](rapport-a83-defaut.md) | A8.3 — le défaut place+perte n'est pas neutre : les portes épinglées bougent de −5,9 % à +19,5 % |`
- **T1** `| [rapport-a83a-coupe.md](rapport-a83a-coupe.md) | A8.3a — `porte-coupe` : le régime 1 % écrase la variance du point de coupe |`
- **T1** `| [rapport-a83a-flux.md](rapport-a83a-flux.md) | A8.3a — `porte-flux` : le régime 1 % a ses propres références |`
- **T1** `| [rapport-a83a-pont.md](rapport-a83a-pont.md) | A8.3a — `porte-pont` : le régime 1 % change la falaise |`
- **T1** `| [rapport-a83d-lot-threads.md](rapport-a83d-lot-threads.md) | A8.3d — le lot n'est pas les threads : l'écart de 1,90 % survit à 1 thread |`
- **T1** `| [rapport-autotest-parallele.md](rapport-autotest-parallele.md) | B13 — la vérification parallèle : 183/183 en 1 min 54 (×2,4) |`
- **T1** `| [rapport-c4-retard.md](rapport-c4-retard.md) | C4 — le prix d'un état en retard : **×633 pour UN pas**, et ce que ça impose à un ordonnanceur |`
- **T1** `| [rapport-c8-generalisation.md](rapport-c8-generalisation.md) | C8 — la tête réflexe sur des textes JAMAIS VUS : jusqu'à ×5,7 du modèle complet |`
- **T1** `| [rapport-c8-tete-entrainee.md](rapport-c8-tete-entrainee.md) | C8 — une TÊTE ENTRAÎNÉE pour sa profondeur : ×540 sur la tête empruntée |`
- **T1** `| [rapport-cache-chunker-applique.md](rapport-cache-chunker-applique.md) | B13 — le cache du chunker appliqué : ×139 en chunker, ×1 en défaut (S domine) |`
- **T1** `| [rapport-cache-chunker.md](rapport-cache-chunker.md) | Cache du chunker — validation indépendante : ×11,0 à 160 tokens, égalité 612/612 |`
- **T1** `reports/rapport-architecture-memoire.md:341:| anglais | 5,8 % | 1,155 s | 0,982 s | **+15 %** |`
- **T1** `reports/rapport-tete-restreinte.md:42:| anglais | 5,8 % | 1,155 s | 0,982 s | **+15 %** |`
- **T1** `**Mesuré au 06/11** : POS **85,00 %**, syntagmes F1 **0,6482**, attachement **235/236**`
- **T1** `POS         exactitude 88.91 %  (fermé 92.94 %, ouvert 84.66 %)`
- **T1** `SYNTAGMES   F1 79.06 %  (P 81.28 % / R 76.95 %)`
- **T1** `tête      F1 89.90 %  (P 93.84 % / R 86.28 %)`
- **T1** `vue linéaire (partition filtrer) F1 79.53 %  · attachement 91.85 % de couverture`
- **T1** `ATTACHEMENT exact 99.46 % · couverture 99.46 % · exact sur span 100.00 % · top-k 98.91 %`
- **T1** `tête      couverture 100.00 % · top-k 99.45 %`
- **T1** `PRAGMATIQUE acte 99.56 % · négation 96.90 % · modalité 98.45 % · double sens 96.46 %`
- **T1** `FRACTION SÉMANTIQUE 50.82 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 0.00 % (graine 0, 184 cibles)`
- **T1** `docs/archive/modele-pour-drave.md:30:| découpage à deux nœuds : **3,4 ms par jeton et par ms de RTT** (§ 8 bis) | le transport est exact à toute latence (perplexité inchangée à 50 ms) | répartir ne pa`
- **T1** `docs/schemas/pipeline.mmd.svg:2:<svg id="my-svg" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="flowchart" style="max-width: 1259.11px; background-co`
- **T1** `docs/pilotage/en-cours.md:64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **re`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) | `en-cours.md`, `README.md`, `
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) | `en-cours.md`, `README.md`, `me`
- **T1** ``0,092` · `0,160` · `0,811` · `0,657` · `0,440` · `0,429` · `2,7856` · `40,0658` · `95,00 %` · `95,75 %``
- **T1** `"sortie": "drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)\nlangue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)\nPOS  Le/DET chat/NOUN dort/VER`
- **T1** `"sortie": "drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)\nlangue=en script=Latn source=cascade · 38 étiquettes · unités sémantiques=3 (45.7% du texte)\nPOS  The/DET day/NOUN when/PRO`
- **T1** `reports/rapport-audit-v10.md:214:| **permutation globale des cibles** (top-1) | **220/220 = 1,0** | moyenne **1,997/220 = 0,908 %** ; médiane 2 ; max 10 ; p95 5 | **0/2 000** |`
- **T1** `reports/rapport-audit-v10.md:215:| **candidat aléatoire** (top-1) | **220/220 = 1,0** | moyenne **92,7/220 = 42,14 %** (585 candidats, 2,66/label) | **0/2 000** |`
- **T1** `reports/rapport-audit-v10.md:221:aléatoire » est haut (42,14 %) parce que les listes de candidats contiennent presque toujours`
- **T1** `reports/rapport-audit-v10.md:224:1,17 % de réussite ; le top-1 aléatoire, lui, vaut 42,14 %. Les deux contrôles donnent p = 0.`
- **T1** `reports/rapport-audit-v10.md:370:  candidats laisse 1,17 % de réussite, le top-1 aléatoire 42,14 % ; les deux donnent p = 0.`
- **T1** `reports/pensee-audit-v10.json:734:   "lecture": "0,908 % en moyenne contre 100 % observé"`
- **T1** `reports/pensee-audit-v10.json:746:   "lecture": "42,14 % en moyenne contre 100 % observé"`
- **T1** `reports/pensee-audit-v10.json:1235:  "Le top-k officiel (sous-chaîne) est peu discriminant : la permutation des listes de candidats laisse 1,17 % de réussite ; le top-1 aléatoire vaut 42,14 %. Les deu`
- **T1** `214:| **permutation globale des cibles** (top-1) | **220/220 = 1,0** | moyenne **1,997/220 = 0,908 %** ; médiane 2 ; max 10 ; p95 5 | **0/2 000** |`
- **T1** `215:| **candidat aléatoire** (top-1) | **220/220 = 1,0** | moyenne **92,7/220 = 42,14 %** (585 candidats, 2,66/label) | **0/2 000** |`
- **T1** `216:| **permutation des listes de candidats** (top-k, égalité) | **219/220 = 0,9955** | moyenne **2,18/220 = 0,99 %** ; max 8 | **0/2 000** |`
- **T1** `217:| **permutation des listes de candidats** (top-k, sous-chaîne) | **219/220 = 0,9955** | moyenne **2,58/220 = 1,17 %** ; max 9 | **0/2 000** |`
- **T1** `"lecture": "0,908 % en moyenne contre 100 % observé"`
- **T1** `"lecture": "42,14 % en moyenne contre 100 % observé"`
- **T1** `"lecture": "0,99 % en moyenne contre 99,55 % observé (critère = égalité)"`
- **T1** `"lecture": "1,17 % en moyenne contre 99,55 % observé (critère officiel = sous-chaîne)"`
- **T1** `64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 cano`
- **T1** `[still running after 60000ms; moved to background job bash-98]`
- **T1** `devant, mais l'anglais est **100 % réel** quand le français ajoute **160 synthétiques** ; sur le`

## 6. Commits

- D3 — LA FAQ DU PRODUIT : 10/10 RÉPONSES VÉRIFIÉES CONTRE LE CODE (10 CONTRÔLES, NÉGATIF DÉTECTÉ) ; D2 — LA RESTITUTION V2 (19/46 CADRES, F1 0,5270)" -m "- FAQ §

