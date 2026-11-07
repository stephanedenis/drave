# Session session- — Table de correspondance atomes Panini et niveaux

> **Journaux :** [le jour](../../2026-11-07/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-a9b5216e-5f4b-4935-8ba0-2ec7d42aaf89` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-07 14:46 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 74 |
| Appels d'outils | 106 |
| Fichiers touchés | 2 |
| Commandes | 89 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J2.1 : la table de correspondance entre les **14 atomes** de Panini (∃ ∆ ∼ ↗ ⊙ ⧖ ◇ № ⊕ ⊗ λ ⊞ ≍ ≡) et nos **niveaux** (graphème, mot, pos, syntagme, phrase, pragmatique, discours, document). Lis `../Panini/README.md`, `../Panini-Research/`, `docs/theorie/genealogie-des-langues.md`. Produis `reports/rapport-atomes-niveaux.md` + JSON : 14 lignes, ce que chaque atome capte, quel niveau le porte, … [49 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J2.1 : la table de correspondance entre les **14 atomes** de Panini (∃ ∆ ∼ ↗ ⊙ ⧖ ◇ № ⊕ ⊗ λ ⊞ ≍ ≡) et nos **niveaux … [329 caractères tronqués]

*106 appels d'outils.* Actions notables :

- bash — List workspace and Panini directories
- bash — Check Qtrinet repo status and reports
- todo_write
- bash — Read head of Panini README
- bash — Read rest of Panini README
- bash — List research root and philosophy-theory
- bash — Find docs mentioning atom symbols
- bash — Find V14 atom docs
- bash — Locate atom symbols in cadres doc
- bash — Read V14 ablation grid
- bash — Read atom definition table in cadres
- bash — Read genealogie doc head
- bash — Find docs with syntagme
- bash — Find docs with grapheme level
- … et 90 autres

**Synthèse produite :**

**J2.1 terminé.** Deux livrables :

- [`reports/rapport-atomes-niveaux.md`](reports/rapport-atomes-niveaux.md) — la table **14 atomes × 8 niveaux**, avec pour chaque atome : ce qu’il capte, son **ancrage**, son **porteur**, sa **portée**, une **mesure possible** et son **contrôle négatif**.
- [`reports/atomes-niveaux.json`](reports/atomes-niveaux.json) — les 14 objets structurés, les 8 niveaux, la calibration des 44 œuvres et le protocole de mesure.

**Ce que dit la table**

| porteur | atomes |
|---|---|
| **phrase** | ∃, ∆, ⧖, ≡ |
| **syntagme** | ∼, ⊙, ⊕, λ |
| **discours** | ↗, ≍ |
| **mot** | № |
| **pos** | ⊗ |
| **pragmatique** | ◇ |
| **document** | ⊞ |
| **graphème** | aucun porteur — ancrage de ∆ et ≍ |

Le graphème est un **ancrage minimal**, pas un porteur sémantique : c’est un résultat explicite, pas un oubli.

**Calibration (lecture seule, 44 œuvres Panini)** : **33 paires** d’atomes à |r| ≥ 0,5 en brut, **4 composantes > 1**, **80,7 %** de variance sur les trois premières en CLR. Les parts sont compositionnelles : № ↔ ≡ passe de **+0,923** (brut) à **+0,577** (CLR), d’où le protocole CLR + permutations + corrélations partielles + corpus négatif.

**Limite nommée** : aucune mesure atome ↔ niveau n’est encore faite. La fiche livre la table, la calibration et le protocole ; **J2.2** construira le corpus commun et exécutera la mesure.

**Contrôles** : `FICHE-OK`, `grep '∃'` = 12, revue documentaire verte, `porte-tableaux` verte, budget T0 **3996/4000**. État mis à jour dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) (compteurs **710/803**, ligne J2.1). Commit **`9c7f71dc`**. Aucune écriture dans Panini.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-atomes-niveaux.md` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 9 |

### Commandes exécutées (échantillon)

- **T1** List workspace and Panini directories
- **T1** Check Qtrinet repo status and reports
- **T1** Read head of Panini README
- **T1** Read rest of Panini README
- **T1** List research root and philosophy-theory
- **T1** Find docs mentioning atom symbols
- **T1** Find V14 atom docs
- **T1** Locate atom symbols in cadres doc
- **T1** Read V14 ablation grid
- **T1** Read atom definition table in cadres
- **T1** Read genealogie doc head
- **T1** Find docs with syntagme
- **T1** Find docs with grapheme level
- **T1** Read contrat bloc langue
- **T1** Locate levels in contrat
- **T1** Read pre-traitement linguistique
- **T1** Read bloc linguistique report and JSON shape
- **T1** Find J2 references
- **T1** Find atom references in Qtrinet
- **T1** Read inventaire Panini head
- **T1** Read inventaire Panini conclusions
- **T1** Find atom name table
- **T1** Read J2 plan and panini-nipada method
- **T1** Inspect Panini atom signature JSON
- **T1** Find full atom name/prime table
- **T1** Read atom definitions in journal April 22
- **T1** Read atom table August and April 25
- **T1** Check glossary vocabulary
- **T1** Read glossary head
- **T1** Search glossary for linguistic levels
- **T1** List panini-related reports
- **T1** Inspect inventaire JSON shape
- **T1** Read result and filing methods
- **T1** Check current state and J2.1 references
- **T1** Check chantier supervisor state
- **T1** Inspect supervisor usage and task files
- **T1** Check recent commits and status
- **T1** Inspect supervisor state JSON
- **T1** Find J2.1 task definition
- **T1** Read supervisor head
- … et 49 autres

## 4. Mesures et résultats marquants

- **T1** `**Références** : `PORTEFEUILLE_CANDIDATS_NOYAU_v1.0.md` (A1) · `DOCUMENT_DE_CONTEXTE_v2.0.md` (critère de sortie, iso) · corpus §334 (114 textes, 655 paires, R²=0.909139)`
- **T1** `- **ΔDTP** = impact sur le benchmark 48/48 (0 % WER maintenu ?).`
- **T1** `- **Non porteur** : ΔDTP = 0 % WER maintenu ET |ΔH₀| ≤ 0.005 → candidat au retrait (constitue un V13 candidat) ;`
- **T1** `V14 organisé en 3 colonnes × 5 périodes avec triades de Döbereiner :`
- **T1** `**Résultat** : couverture NSM de 89% (58/65) → **100% (65/65)**. Confiance de 0.780 → 0.891 (+0.111). Total : 14 + 6 = 20 primitives.`
- **T1** `3. **ne pas confondre lisibilité et structure** ✗✓ : que la langue soit **lisible** dans l'état (80-100 %, mesure`
- **T1** `La grille de 60 langues, regroupée par niveau Glottolog, donne un ordre **monotone** : **même branche 30,7 %** >`
- **T1** `**même famille 22,0 %** > **familles différentes 15,2 %** (hasard 3,3 %) — *l'alignement du modèle suit la`
- **T1** `- **langues** : 448 langues UDHR ; la surface est **lue à 80-100 %** ; le **sens** se retrouve à **96 %** sur les`
- **T1** `paires bien couvertes, **16 %** sur 100 langues stratifiées, **3,5×** le hasard dans un vivier ouvert ;`
- **T1** `- **dialectes** : 100 % lisibles ; contenu retrouvé **30 à 100 %** selon la couverture de la langue ;`
- **T1** `- **styles / traducteurs** : 87-100 % lisibles ; contenu **6-24 %** — *et ce chiffre est encore confondu avec`
- **T1** `débit. Une cascade qui appelle le neuronal sur 90 % des phrases n'est pas une cascade : c'est un`
- **T1** `131:débit. Une cascade qui appelle le neuronal sur 90 % des phrases n'est pas une cascade : c'est un`
- **T1** `la photo de **55,9 % à 6,7 %** de WER et les colonnes de **89,4 % à 0,5 %** ; le réseau n'y est`
- **T1** `Le CPU paie les octets, le réseau paie les jetons. Une couche heuristique qui traite 90 % de la`
- **T1** `surface en O(octets) enlève au réseau ces 90 % de jetons **si** la porte les accepte. Le gain`
- **T1** `> substituables, un parallèle et une cascade, une activation sémantique à **51–76 %** ; la`
- **T1** `côté Panini ; 456 langues × 30 articles + Glottolog côté Drave, **même source XML**), signatures`
- **T1** `Pensine-Web, jamais exécutée), `ETAT-TRIANGLE-RECHERCHE.md` (maturités 70/45 %, septembre 2025),`
- **T1** `- Le plus « prêt à prouver » : **corpus d'or CIC** (`corpus_dor_cic_v1.json`, 46 Ko + TSV) : 3 defs,`
- **T1** `| Lexiques V14 | `data/v14_lexicon_enriched.json` (3,9 Mo) | `{lang: {ATOME: [mots]}}` | aucune | haute (qualité à vérifier) |`
- **T1** `| API REST | `src/nipada/api/api.py`, `server.py` | FastAPI : `/decompose`, `/reconstruct`, `/roundtrip`, `/compare`, `/atoms`, `/dhatus`, `/benchmark`, `/search`, `/hypotheses`, `/api/v1/*` | fastapi`
- **T1** `2. **Signatures 14 atomes** : **44 œuvres** × 14 flottants (somme 1), en JSON pur. Livrable : table`
- **T1** `cassés, backlog P0 entièrement « À faire ». **Ne pas promettre du 0 % WER.**`
- **T1** `- **L'API REST** : séduisante sur le papier, mais dépend de FastAPI **et** d'un graphe de 33-58 Mo ;`
- **T1** `V14 ; Drave apporte 456 langues × 30 articles et Glottolog.`
- **T1** `tradition`, échantillon de 20 langues (5 familles × 4), et une mesure de recouvrement des codes.`
- **T1** `croisée (deux checkers indépendants dans leur dépôt : `cic` et `cic_named`). 46 Ko.`
- **T1** `| 2 | **atomes V14 ↔ niveaux** (44 œuvres × 14 flottants, JSON pur) | table + 20 exemples mesurés | permuter les colonnes doit tuer le prédictif | signature lexicale : contrôler la date |`
- **T1** `docs/journal-de-bord/2026-04-25.md:1141:- ✅ **§121 — Stratification numérique ℕ → 𝕆 (`number_strata_v121.json`) : signatures factorisées par ratios *exactement égaux aux primes* (ℕ=19, ℤ=38=19×2 +ÊTRE`
- **T1** `docs/journal-de-bord/2026-06-02-session-478c-final.md:122:Top atoms: ESPACE (23.5%), ÊTRE (20.6%), SUJET (16.2%), TEMPS (8.8%)`
- **T1** `docs/journal-de-bord/2026-06-02-session-478c-final.md:140:| ESPACE | 15.8% | Hopi (15.8%), Walam Olum (23.5%) | Most texts: 7-15% |`
- **T1** `docs/NIPADA_SESSION_476_478c_FINAL_REPORT.md:77:| ESPACE | 15.8% | 15.4% | 23.5% | 5.3% | Walam Olum |`
- **T1** `docs/NIPADA_VULGARISATION.md:127:- MESURE = NOMBRE × RAPPORT = 19 × 5 = **95** — quantification d'une relation`
- **T1** `V14 organisé en 3 colonnes × 5 périodes :`
- **T1** `Question réflexive avant d'entamer §120 : « le système V7 actuel pourrait-il digérer *The Road to Reality* (Penrose, 1099 pages couvrant l'arithmétique, la géométrie, l'analyse complexe, les groupes, `
- **T1** `| ℤ | 38 = 19×2 | + ÊTRE (signe) |`
- **T1** `| ℚ | 190 = 38×5 | + RAPPORT |`
- **T1** `2 319 lignes de Rust sans dépendance, 5,3 G événements/s sur CPU, 16 jetons`
- **T1** `"API FastAPI /decompose (non demarree : fastapi + graphe 33-58 Mo)",`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 te`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV réglée** (sujet hors du GV +`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tranché (la tête du GN arrête `
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 07/11 14 h 40.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) réglé `
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T1** `**100 scans simulés** : la photo passe de **55,9 %** à **6,7 %** de [WER](../theorie/glossaire/entrees/wer.md) (test **5,7 %**) et la`
- **T1** `**préservation** du lecteur atteint **90–97 %** sur **4 familles sur 5** (propre **96,7 %** ;`
- **T1** `fax **56,7 %**, la limite d'information) ; les **colonnes** tombent de **89,4 %** à **0,5 %**,`
- **T1** `les **tableaux** donnent **92,6 %** de cellules exactes, et **trois vrais scans** s'accordent à`
- **T1** `**7,10 %** et **88,4 %** de mots, l'**ordre des colonnes** prouvé (**15,3 %** contre **98,0 %**`
- **T1** `611 ms. La restitution depuis un document lu est **R31**.`
- **T1** `-- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7549**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **contrat v1** validé ; frontières, partition, `
- **T1** `+- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV réglée** (sujet hors du GV `
- **T1** `- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (`
- **T1** `| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** ; R2/R3 attendent N5/N4 | **1 024 octets entraînés** ; **2 048** fini (2×10 000 pas) ; la restitution |`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir 0,2276 |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `| [`rapport-pos-anglais-v2.md`](rapport-pos-anglais-v2.md) | **B13** — POS **83,83 %** (R2a/R3/R2b), F1 **0,6181** |`
- **T1** `| [`rapport-autotest-parallele.md`](rapport-autotest-parallele.md) | **B13** — l'autotest parallèle : **183/183 en 1 min 54** (×2,4), mêmes verdicts |`
- **T1** `| [`rapport-cache-chunker.md`](rapport-cache-chunker.md) | **B13** — la validation A11 du cache : ×11,0 à 160 tokens, égalité 612/612, cache falsifié détecté |`
- **T1** `| [`rapport-cache-chunker-applique.md`](rapport-cache-chunker-applique.md) | **B13** — le cache appliqué : **×139** en chunker, ×1 en défaut (S domine), sortie identique, **181/181** |`
- **T1** `| [`rapport-cout-chunker.md`](rapport-cout-chunker.md) | **B13** — le coût du chunker : O(n²) confirmé, cache ×11,6 à 160 tokens |`
- **T1** `712:| [rapport-vitesse-v41.md](rapport-vitesse-v41.md) | Rapport — La nuit des optimisations V4.1 : ×3,54 sur la passe, et pas un chiffre changé |`
- **T1** `34:- **V14** (25 avril, §133-134) : 56 énoncés × 6 modes (texte, formule, diagramme, code, chimie, biologie). 12/14 atomes suffisants. Aucun nouveau premier nécessaire. Couverture cross-modale 100%.`
- **T1** `109:V14 organisé en 3 colonnes × 5 périodes avec triades de Döbereiner :`
- **T1** `- **V14** (25 avril, §133-134) : 56 énoncés × 6 modes (texte, formule, diagramme, code, chimie, biologie). 12/14 atomes suffisants. Aucun nouveau premier nécessaire. Couverture cross-modale 100%.`
- **T1** `7:> 44 œuvres de Panini montre **33 paires d'atomes à |r| ≥ 0,5** (brut), **4 composantes > 1** et **80,7 %** de`
- **T1** `201:**80,7 %** de la variance (6,967 · 2,845 · 1,491 · 1,260 · …). Autrement dit, dans ce corpus, les 14 atomes`
- **T1** `> 44 œuvres de Panini montre **33 paires d'atomes à |r| ≥ 0,5** (brut), **4 composantes > 1** et **80,7 %** de`
- **T1** `- `../../Panini/research/nipada/falsification/analytic_sigs_v1.json` : 44 œuvres × 14 parts, somme 1.`
- **T1** `**80,7 %** de la variance (6,967 · 2,845 · 1,491 · 1,260 · …). Autrement dit, dans ce corpus, les 14 atomes`
- **T1** `**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035`, convention des GV, schéma v2 et restitution v0 faits**, reste `g017` ; **S**`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `[still running after 60000ms; moved to background job bash-85]`
- **T1** `9c7f71dc PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : 8eb0cc49 B13 — RESTITUTION v0 : 46/46 SURFACES EXACTES, MIROIR STRICT 0,1087, LE MIROIR TROUVE LES SAUTS DE LIGNE 9a259953 B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 ÉCHEC)

## 6. Commits

- PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE" -m "Table de correspondance V14 (Research) × 8 niveaux Dr

