# Session session- — Clôture V3 et rapport bilan

> **Journaux :** [le jour](../../2026-11-16/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-b3e96cb1-fb3b-4593-a2a6-b034ae644413` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-16 03:01 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 128 |
| Appels d'outils | 173 |
| Fichiers touchés | 7 |
| Commandes | 136 |
| Sous-agents | 0 |
| Commits | 2 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche V3 (clôture) : la clôture de la nuit — le rapport `reports/rapport-bilan-exploitable-2.md` + JSON (les 9 tâches T/U/V, les chiffres, les négatifs), la mise à jour de `docs/pilotage/en-cours.md` et de la roadmap, le **tag annoté** `exploitable-2026-11-16` sur le dernier commit vert, et le relevé des portes (`work/portes/`, sans relancer la passe).

## 2. Déroulé, étape par étape

### Tour 1 — Tâche V3 (clôture) : la clôture de la nuit — le rapport `reports/rapport-bilan-exploitable-2.md` + JSON (les 9 tâches T/ … [234 caractères tronqués]

*173 appels d'outils.* Actions notables :

- bash — Inspect repository status and recent log
- bash — List workspace, work/portes and reports
- bash — List exploitable/bilan reports
- bash — Inspect latest door pass directory
- bash — List tags and decorated recent commits
- bash — Check branches and full recent log
- bash — Find planning docs mentioning tasks
- bash — List pilotage docs and search en-cours
- read
- bash — Find journal entries for 2026-11-16
- bash — Search task plan for T/U/V tasks
- bash — Find files mentioning T6/U3/V3
- bash — Read 2026-11-16 journal entries
- bash — Locate T/U/V in roadmap
- … et 145 autres

**Synthèse produite :**

**V3 — clôture faite.** Le bilan de la nuit est écrit et committé.

- **Rapport** : `reports/rapport-bilan-exploitable-2.md` + `reports/rapport-bilan-exploitable-2.json`.
  Il couvre les **9 tâches mesurées T1–T6 · U1–U3**, les **deux vérifications V1–V2** et cette clôture :
  produit installable, JSON **2 139** objets / **8** rôles, **10 000 mots 0,82 s** (α **1,076**, diff vide),
  roue **1 727 201 o** (sans gold → **4**), profils **20/20** (ambigu **`und`**), `--strict` **0,8625/0,8891**,
  exemples **27/27** — avec **12 négatifs** nommés (clone public, or de S, mock neuronal, confiance non calibrée, etc.).
- **Portes** : relevé `work/portes/roue-1116/` lu **sans relancer la passe** → **86 portes, 82 vertes, 4 rouges**
  (`indice`, `melange` structurelles ; `produit` et `sessions` de circonstance).
  Vérification ciblée dans `work/portes/verif-cloture-1116/` : `sessions` **0**, `produit` **0**
  (`--strict` 5 tests, exemples 27/27, autotest 183/183) → **84 vertes, 2 rouges structurelles**.
- **État et roadmap** : `docs/pilotage/en-cours.md` et `docs/pilotage/roadmap.md` mis à jour
  (compteurs **771/866**, passe du 16/11, V3, tag) ; `references-non-regression.md` et journal du 16/11 complétés.
- **Tag annoté** : `exploitable-2026-11-16` sur le dernier commit vert **`ae3c24f2`** (V2).
  Contrôles : `git cat-file -t` → `tag` ; `git rev-parse exploitable-2026-11-16^{}` → `ae3c24f2`.
- **Commit** : `3c10e3ee` — *V3 — la clôture…* ; poussé sur `origin/s/v7`, `origin/master` et le tag.
- **Vérifications finales** : `revue_documentation.py` ✅, `verifie_en_cours.py` ✅, `taille_documents.py` ✅,
  `verifie_journal.py` ✅, `porte-tableaux.sh` ✅, `verifier_schemas.py` ✅.

Prochaine mesure désignée : **J4 — l’or de rôles** ; Panini attend ses 26 signatures et la décision `auto` reste humaine.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-exploitable-2.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 10 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md` | 0 | 2 |

### Commandes exécutées (échantillon)

- **T1** Inspect repository status and recent log
- **T1** List workspace, work/portes and reports
- **T1** List exploitable/bilan reports
- **T1** Inspect latest door pass directory
- **T1** List tags and decorated recent commits
- **T1** Check branches and full recent log
- **T1** Find planning docs mentioning tasks
- **T1** List pilotage docs and search en-cours
- **T1** Find journal entries for 2026-11-16
- **T1** Search task plan for T/U/V tasks
- **T1** Find files mentioning T6/U3/V3
- **T1** Read 2026-11-16 journal entries
- **T1** Locate T/U/V in roadmap
- **T1** Inspect existing bilan exploitable
- **T1** Search session plan for V tasks
- **T1** Find exploitable files and references to bilan 2
- **T1** Read latest doors registry
- **T1** Read doors runner script
- **T1** Inspect door pass directory contents
- **T1** Count registry entries and gates
- **T1** Check tolerated red gates
- **T1** Read tails of the four red gates
- **T1** List red entries and duplicates
- **T1** Check specific gate entries
- **T1** Read produit gate script
- **T1** Read produit strict failure log
- **T1** Read doors method and tolerated red references
- **T1** Show commit dates
- **T1** Find V1 commit and working tree status
- **T1** Check strict test logs timestamps
- **T1** Read previous closure report
- **T1** Inspect previous closure JSON structure
- **T1** Read headers of U/V fiches
- **T1** Read U1 10k and controls
- **T1** Read U2 controls and negatives
- **T1** Read U3 measure and negatives
- **T1** Read V1 real gold and negative control
- **T1** Read V2 details and limits
- **T1** Search session digest for V3 plan
- **T1** Search session report for V3 plan
- … et 96 autres

## 4. Mesures et résultats marquants

- **T1** `d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO`
- **T1** `83adaa2b T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE`
- **T1** `9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS`
- **T1** `7f0e8320 T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))`
- **T1** `39:| **L/B13 — Pensée (session `e181ce02`)** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**, 2–8 cœurs | **166/166** (6 S`
- **T1** `195:   **0,7539**, acte **1,0**) ; **DRVM/native** par la règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **gold 432 : acte 0,9954** ; **f`
- **T1** `| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO | `en`
- **T1** `| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO |`
- **T1** `33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**`
- **T1** `35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1`
- **T1** `166:**U1 — les O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),`
- **T1** `315:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes`
- **T1** `390:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `[still running after 60000ms; moved to background job bash-16]`
- **T1** `92:| `porte-homeostasie.sh` | 495 s | ✅ porte tenue (×0 exact · activité monotone · dominance reproduite) |`
- **T1** `d19f0fc7 2026-11-16 00:19:47 -0500 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127`
- **T1** `83adaa2b 2026-11-15 23:40:39 -0500 T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,7`
- **T1** `9a291c8b 2026-11-15 23:30:16 -0500 T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS`
- **T1** `7f0e8320 2026-11-15 23:10:00 -0500 T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))`
- **T1** `bb68b820 J12.1 — LE §334 EST UNE GÉOMÉTRIE DE FILIATION : 655 LIGNES = 495 PAIRES UNIQUES (160 DOUBLONS, 7 AUTO-PAIRES), 48 TEXTES, 44 SIGNATURES ; H0 0,909139 / 0,906307 (488), DATE 0,0089 APRÈS TOPO`
- **T1** `9c7f71dc PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE`
- **T1** `bb67dd59 ÉTAT ET JOURNAL — LA NUIT DES P0 : POS 85,00 %, ATTACHEMENT 235/236, FRONTIÈRES 0/40, PARTITION ÉTIQUETÉE, CONTRAT V1`
- **T1** `"corpus": "418/438 paires exactes (95,4 %), 8/8 contrôles",`
- **T1** `# U1 — les deux O(k²) sont bornés : 10 000 mots de **4,0 s à 0,82 s** (×4,9), α de **1,53 à 1,08**, sorties **identiques au bit près**`
- **T1** `> **3,991 s à 0,816 s** (×4,9) ; la mémoire reste au même niveau (**127,4 Mio** contre`
- **T1** `| ×1 | 247 | 124 | 0,050 | **0,032** | ×1,55 |`
- **T1** `| ×2 | 494 | 248 | 0,113 | **0,078** | ×1,46 |`
- **T1** `| ×4 | 988 | 496 | 0,300 | **0,144** | ×2,08 |`
- **T1** `| ×8 | 1 976 | 992 | 0,828 | **0,308** | ×2,69 |`
- **T1** `| ×16 | 3 952 | 1 984 | 2,461 | **0,618** | ×3,98 |`
- **T1** `| ×32 | 7 904 | 3 968 | 8,863 | **1,478** | ×6,00 |`
- **T1** `| ×40 | 9 880 | 4 960 | 13,691 | **1,777** | ×7,70 |`
- **T1** `> l'artefact de profils (802 110 octets) ajoute ~0,33 Mo : la roue courante fait **2 055 192`
- **T1** `# V1 — `evaluer --strict` : les quatre modes locaux, la cascade à 86,25 % / 88,91 %, le plancher 0,70 qui mord`
- **T1** `> quatre modes, et sort en **0** : cascade POS **86,25 %** (612) et **88,91 %** (452), soit`
- **T1** `| fonction `Heuristique.analyser` | **3,991 s** | **0,816 s** | **×4,89** |`
- **T1** `| débit (fonction) | 2 506 mots/s | **12 259 mots/s** | ×4,89 |`
- **T1** `| CLI `--json` | 5,011 s | **1,668 s** | ×3,00 |`
- **T1** `| sérialisation JSON seule | 0,628 s | 0,628 s | ×1,00 |`
- **T1** `| pic RSS (fonction) | 129 936 Ko (126,9 Mio) | 130 452 Ko (**127,4 Mio**) | +0,5 Mio |`
- **T1** `| pic RSS (CLI) | 171 316 Ko (167,3 Mio) | 171 864 Ko (167,8 Mio) | +0,5 Mio |`
- **T1** `Le CLI ne gagne « que » ×3 parce que les **0,63 s de `json.dumps`** et le démarrage ne`
- **T1** `soit **+0,4 %** — le prix du temps linéaire.`
- **T1** `**après** correction des deux premiers. Le profil final du bloc ×32 (24,5 s profilées) ne`
- **T1** ``_cible_proche` à **14,5 s** et `_est_adverbe_seul` à **11,6 s** sur le bloc ×16 : ces trois`
- **T1** `langues stratifiées** (5 familles × 4, 10 écritures), choisies pour l'égalité exacte de`
- **T1** `ne dit pas que les 398 langues font 100 %. L'autotest complet le dit :`
- **T1** `- **La roue n'est pas minimale** : l'artefact ajoute ~0,33 Mo compressés à la roue U2`
- **T1** `- **`--profils` est une option** : elle charge l'artefact (~800 Ko) et score 398 profils par`
- **T1** `La valeur observée au rejeu est de **4,0 à 5,8 ms** selon l'exécution. C'est une mesure locale à`
- **T1** `| `drave evaluer` | F1 **81,88 %**, attachement **88,70 %** | **conforme** |`
- **T1** `4/4 : `rôle=agent`, `→ chat`, F1 **79,02 %**, `ATTACHEMENT exact 99.58 %`.`
- **T1** `43304:TROIS TAUX V3 (145) : (a) cible == cibles[0] : 141/145 = 97,24 % ; (b) cible in cibles : 143/145 = 98,62 % ; (c) cible == tête d'une cible : 143/145 = 98,62 %. Écart (b−a) = +2 cas, +1,38 pt ; p`
- **T1** `43305:TROIS TAUX V3 (239) : (a) 141/239 = 59,00 % ; (b) 143/239 = 59,83 % ; (c) 143/239 = 59,83 % ; +2 (+0,84 pt).`
- **T1** `43308:GAINS ET CONTRÔLE. Les 2 gains sont s108 et s122 (GP synthétiques), où le bloc choisit « papier », la 2e cible. Sur hand+reel : 114/115 = 99,13 %, écart 0. V3 a corrigé g002/g012/r018/r230 ; il `
- **T1** `52203:**29 tâches** : **8 autonomes** (exécutées en grande partie), **11 en coordination**, **10 bloquées** ; **18 mentions périmées** corrigées dans les documents. L'audit de fiabilité (A24) a mesuré`
- **T1** `9801:**29 tâches** : **8 autonomes** (exécutées en grande partie), **11 en coordination**, **10 bloquées** ; **18 mentions périmées** corrigées dans les documents. L'audit de fiabilité (A24) a mesuré `
- **T1** `[still running after 600000ms; moved to background job bash-5231]`
- **T1** `[still running after 600000ms; moved to background job bash-5232]`
- **T1** `[still running after 600000ms; moved to background job bash-5235]`
- **T1** `[still running after 600000ms; moved to background job bash-5238]`
- **T1** `[still running after 600000ms; moved to background job bash-5239]`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `"preuve": "sans tools/structures : rôle objet au lieu de agent, attachement 88,70 % au lieu de 99,58 %",`
- **T1** `"consequence": "un débutant ne voit pas la sortie de la notice ; le F1 81,88 % n'est pas un gain"`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; **19/19 verdicts `/paragraphes`** (11 accepté`
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 15/11 (nuit).** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **F1 0,7902**, `
- **T1** `**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (hasard`
- **T1** `**14,8 Mo** JSON ; α = **1,55**, `_groupes_partition`/`_cible_proche` **O(k²)**.`
- **T1** `**U1 — les O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),`
- **T1** `| `porte-delais.sh` | 21 s | ✅ le temps, lui, augmente : 6.77 s → 9.67 s (+2.9 s ≈ 50 ms × 64 pas) |`
- **T1** `| `porte-homeostasie.sh` | 495 s | ✅ porte tenue (×0 exact · activité monotone · dominance reproduite) |`
- **T1** `| `porte-jeux.sh` | 104 s | ✅ la porte des jeux tient : 100 % au niveau 4, 33/33 paires invariantes, 0 collision, |`
- **T1** `| `porte-mistral.sh` | 8 s | ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= plancher  |`
- **T1** `| `porte-pont.sh` | 79 s | ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux |`
- **T1** `| `porte-reflexe.sh` | 141 s | ✅ 3. l'accord est mesuré AVANT (0.4 %) et APRÈS — la mesure est branchée |`
- **T1** `| `porte-reparti-moteur.sh` | 3 s | PORTE TENUE : le découpage ne change pas la perplexité (écart relatif 0.0000 %) |`
- **T1** `38:**État au 15/11 (nuit).** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **F1 0,7902*`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.`
- **T1** `-| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ;`
- **T1** `+| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ;`
- **T1** `-**État au 15/11 (nuit).** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **F1 0,7902**,`
- **T1** `+**État au 15/11 (nuit).** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **F1 0,7902**,`
- **T1** `[still running after 60000ms; moved to background job bash-125]`
- **T1** `docs/pilotage/roadmap.md:33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 c`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : #!/bin/bash # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait. # # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS # (`--attn-window` en r
- **T1** : ae3c24f2 V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE c37fed06 B1 — LE PROTOCOLE À DATE CONTRÔLÉE 
- **T1** : (no output) [exit code: 1]

## 6. Commits

- V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON" 2>&1 | ta
- ps -ef | grep -E 'pre-commit|committing|git commit|porte-|revue_doc|journal' | grep -v grep | head -20

