# Session session- — Rapport coordination S v2

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-e0896820-1b14-4849-a926-cc56f678b88d` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 02:15 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 92 |
| Appels d'outils | 156 |
| Fichiers touchés | 5 |
| Commandes | 123 |
| Sous-agents | 0 |
| Commits | 4 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche C2 : la coordination S, suite de J4.2 — écris `reports/rapport-coordination-s-v2.md` + JSON : l'état de la page `/` (le service de la v7), le pare-feu réseau, la commande de lancement, ce qui reste à S ; les 11 verdicts sont désormais committés (389b99f). **Ne touche pas `tools/structures/`.**

## 2. Déroulé, étape par étape

### Tour 1 — Tâche C2 : la coordination S, suite de J4.2 — écris `reports/rapport-coordination-s-v2.md` + JSON : l'état de la page `/ … [180 caractères tronqués]

*156 appels d'outils.* Actions notables :

- bash — Show recent git log and status
- bash — List repo root, reports, journal
- bash — Search for J4.2 and coordination S references
- bash — Search J4.2 and coordination-s references
- bash — Search firewall references
- bash — Show commits 389b99f and 31ce36fd
- bash — Inspect structures submodule commit 389b99f
- bash — Read plan.json around C2 mandate
- bash — Read existing S coordination report and JSON
- bash — Read v2 N2 report structure
- bash — Read S paragraphs report
- bash — Inspect structures directory and server
- bash — Search v7 service references in pilotage docs
- bash — Search v7 mentions excluding pensee
- … et 135 autres

**Synthèse produite :**

Terminé.

**Livrables**
- `reports/rapport-coordination-s-v2.md`
- `reports/rapport-coordination-s-v2.json`
- Mise à jour de `docs/pilotage/en-cours.md`, `docs/pilotage/roadmap.md`, `reports/INDEX.md` et `reports/README.md`.
- Commit **`f926b5bc`** (local, non poussé). Le sous-module reste propre, pointeur **`389b99f`** : **aucun fichier de `tools/structures/` modifié**.

**Ce que la fiche établit**
- **11 verdicts committés** (`389b99f`, pointeur `31ce36fd`) : **19/19 candidats, 11 acceptés, 8 exclus**, 0 note ; **56 tests** passent.
- **Page `/`** : aucun service S en écoute ; le port **8765** est tenu par `financemeteo` (pid 2725542). Mesure sur **9000** : **207 phrases / 369 candidats**, **0 `profondeur`** ; la v7 dynamique donne **359 candidats, 99 à ≥3**. La phrase « la page `/` sert la v7 » est fausse à l'état mesuré : `/paragraphes` est la seule fenêtre v7 (9/9, 19/19, 169/169 `profondeur`).
- **Pare-feu** : `firewalld` actif et enabled, mais `firewall-cmd`/`nft`/`iptables` non interrogeables sans root ; le défaut `--hote 127.0.0.1` rend le service local par construction. Commande de lancement sur **9000**, tunnel SSH ou ouverture root ; ne pas toucher 8765.
- **Migration** : la v1 comptait **5** candidats sans index ; en signature exacte, **41 paires (44 lignes)** n'ont pas de correspondance v7. Les 5 sont au-delà de la nouvelle longueur ; **36 seraient silencieusement recollées au mauvais candidat** par index. **106/147** sont sauvées par signature.
- **Reste à S** : décider la migration `/` v7 (106 conservées / 41 à re-juger), corriger les référents, rétro-traduction, couverture de la banque, docs, 71 langues.

**Vérifications** : revue de documentation ✅, tableaux/liens ✅, T0 **3 996/4 000** ✅, `en-cours` ✅, sous-module propre ✅.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s-v2.md` | 1 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/INDEX.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 12 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 2 |

### Commandes exécutées (échantillon)

- **T1** Show recent git log and status
- **T1** List repo root, reports, journal
- **T1** Search for J4.2 and coordination S references
- **T1** Search J4.2 and coordination-s references
- **T1** Search firewall references
- **T1** Show commits 389b99f and 31ce36fd
- **T1** Inspect structures submodule commit 389b99f
- **T1** Read plan.json around C2 mandate
- **T1** Read existing S coordination report and JSON
- **T1** Read v2 N2 report structure
- **T1** Read S paragraphs report
- **T1** Inspect structures directory and server
- **T1** Search v7 service references in pilotage docs
- **T1** Search v7 mentions excluding pensee
- **T1** Read S state report
- **T1** Read page / analysis and A1 migration
- **T1** Check banque-v7, running servers, firewall
- **T1** Search banque-v7 migration artifacts
- **T1** Inspect running server process details
- **T1** Query firewall state and rules
- **T1** Query page / and inspect routes
- **T1** Read recent journal days
- **T1** Search recent journals for service and firewall
- **T1** Search session reports for v7 service
- **T1** Inspect structures data and v7 fields
- **T1** Inspect server routes and static index
- **T1** Read tree measurement tool
- **T1** Find server entry points and v7 service refs
- **T1** Verify git pointer and verdicts at 389b99f
- **T1** Read firewall config and network interfaces
- **T1** Search all session logs for firewall and port 8765
- **T1** Check firewall tools and DBus access
- **T1** Locate firewalld configuration files
- **T1** Search all journals for firewall-cmd usage
- **T1** Inspect DBus policy and sudoers for firewall
- **T1** Test LAN reachability and inspect port 3080
- **T1** Inspect C1 commit pattern
- **T1** Read current en-cours state
- **T1** Find S lines in en-cours and roadmap
- **T1** Run server on port 9000 and measure page state
- … et 83 autres

## 4. Mesures et résultats marquants

- **T1** `6560a0a5 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612)`
- **T1** `2d7a7f2b 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5)`
- **T1** `ce7241d5 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS`
- **T1** `./reports/rapport-cycle-entraine.md:1:# C2 bis — le cycle ENTRAÎNÉ : ×228 au pas 4, mais il dégrade encore (et le moteur le confirme)`
- **T1** `./reports/ocr-cegep-64.json:5: "verdict": "le re-split 64 (2/1/1) est contaminé : DOC2 placé en val est un quasi-doublon de l'ancien train (18/20 fenêtres de 500 o, 17 001 o contigus) ; le contrôle 8 `
- **T1** `./reports/pensee-cache-chunker.json:4: "verdict": "Cache VALIDÉ. Le O(n²) du chemin chunker est confirmé : 1+2·S appels à _syntagmes_simple (97/193/769 à 160/320/1 280 tokens), pente log-log 1,71-2,00`
- **T1** `./reports/pensee-cache-chunker.json:237:  "longueurs": "C1, C2 et OFF : 42/42 (7 longueurs × 2 chemins × 3 variantes)",`
- **T1** `docs/pilotage/chantiers.md:84:| **B — l'intelligence** | le sens, la logique, les jeux, les maîtres : que sait faire le système ? | ✅ B1–B12 ; B10.3 bloqué (encodeur) ; **B13** state store v0 + DRVF +`
- **T1** `reports/rapport-tableau-mesures.md:99:| T01 | POS API (tagger neuronal seul) | 612 · 3 179 jetons | 0,8625 (2 742/3 179) | **0,9475** (3 012/3 179) | **+8,49 pts** [7,23 ; 9,74] | majoritaire 0,2145 ;`
- **T1** `reports/rapport-tableau-mesures.md:269:| C05 | Tagger — planchers | majoritaire, classe fréquente, permutation, uniforme | 0,2145 / 0,2491 / 0,1667 / 0,0833 ; McNemar 344/74, p = 1,1 × 10⁻⁴² | pass | `
- **T1** `140feb6 S — L'ANALYSEUR LIT LE FRANÇAIS PROPRE (65,5 %), PAS LE CEGEP OCR (8,5 %, PLANCHER DU MÉLANGE)`
- **T1** `"mandat": "Tâche B2 : les 14 atomes comme prédicteurs des 8 niveaux Drave — sur les 44 œuvres × 14 flottants (JSON plat, lecture seule chez Panini), mesure la prédiction d'un niveau (POS, syntagmes, a`
- **T1** `8 lots × 16 fenêtres ; tout est déterministe (2,7856 deux fois).`
- **T1** `docs/pilotage/roadmap.md:34:| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tr`
- **T1** `docs/pilotage/roadmap.md:38:**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL `
- **T1** `docs/pilotage/roadmap.md:457:| S — la banque validée | **`/paragraphes` fini** : 9/9 paragraphes, 19/19 candidats, 11 acceptés, 8 exclus, **11 verdicts non committés** ; **banque 150 verdicts / 74 des`
- **T1** `> (35,7 %), **84 lectures acceptées**, mais la page sert les **369 candidats stockés le 02/11**,`
- **T1** `| notation | **5 112/5 112** | 72 items × 71 langues |`
- **T1** `| permutation des libellés | **186/449** ; **12/275** forts (4,4 %) | contrôle négatif |`
- **T1** `confirme : mélanger les libellés fait tomber les items forts de **275/275 à 12/275** (4,4 %), donc`
- **T1** `**340, 342, 343, 343, 344** sur 449 — le taux (~76 %) est stable, le chiffre exact non ; la cause`
- **T1** `candidats jugés (**35,7 %**), **0 phrase partielle**, **133 phrases sans aucun verdict**`
- **T1** `(64,3 %) ; **147/369 candidats** sont jugés (**39,8 %**). Les 7 phrases du banc sont **7/7**`
- **T1** `jugées ; les 200 phrases de littérature sont **67/200** (33,5 %).`
- **T1** `| phrases jugées en entier | **74/207** (35,7 %) |`
- **T1** `| phrases sans verdict | **133** (64,3 %) |`
- **T1** `| candidats jugés | **147/369** (39,8 %) |`
- **T1** `| lectures acceptées (dernier verdict) | **84** (73 + 11), **57,1 %** de 147 |`
- **T1** `| lectures exclues | **63**, **42,9 %** |`
- **T1** `| verdicts avec contexte | **6/147** (4,1 %) |`
- **T1** `| notes | **1/150** (0,7 %) |`
- **T1** `paires, **3 lignes supersédées** (2 % des lignes). Le seul `double_sens` n'a pas survécu : la`
- **T1** `soit **99 à ≥ 3** (27,6 %), et **294/371** formes avec un antécédent proposé, **77 sans** (20,8 %).`
- **T1** `UDHR × 10 langues, avec référence humaine), le lanceur (`tools/llm/enseignant.py`) et la mesure`
- **T1** `(57,1 %, dont 73 `resolu` = 49,7 % et 11 `compatible` = 7,5 %) et **63/147** exclues (42,9 %).`
- **T1** `**La couverture est partielle et datée.** 74/207 phrases (35,7 %), 147/369 candidats (39,8 %),`
- **T1** `**Le contexte est un décor.** 141/147 verdicts finaux au niveau 0, 6 avec contexte (4,1 %). Le`
- **T1** `règles, les vagues 5 et 6 ont été écrites **après** les règles, et le corpus réel donne **65,5 %**`
- **T1** `de GN+GV sur la littérature propre contre **9,1 %** pour le mélange — et **8,5 %** sur le CEGEP`
- **T1** `| **le gold est de la même main** | 61/61, contrôles 104/106/0,10 ; corpus 65,5 % vs 9,1 % | nouvelle vague holdout, autre main, après les règles |`
- **T1** `de double-codage, pas de test-retest. Les 57,1 % de la banque et les 57,9 % des paragraphes`
- **T1** `chiffre exact ne doit pas être cité comme un point ; le taux ~76 % est la seule lecture`
- **T1** `| 05:37 | `bb68b820` | J12.1 — LE §334 EST UNE GÉOMÉTRIE DE FILIATION : 655 LIGNES = 495 PAIRES UNIQUES (160 DOUBLONS, 7 AUTO-PAIRES), 48 TEXTES, 44 SIGNATURES ; H0 0,909139 / 0,906307 (488), DATE 0,0`
- **T1** `**521/532** étiquetées Glottolog), le top-1 de voisinage est de la même famille **66,1 %** (hasard`
- **T1** `10,3 %) et de la même branche **26,1 %** (hasard 2,5 %). Mais **hors écriture, tout est au hasard**`
- **T1** `(famille 9,9 % contre 8,1 %, sœur 0,7 % contre 0,8 %) ; dans la même écriture, la famille monte à`
- **T1** `**69,8 %** et la sœur à **27,8 %**. Le retrieval parallèle 30 articles le chiffre : sur les **25`
- **T1** `autre segment ; couverture **65,84 % des jetons**, **75,19 % des caractères**. La limite est la`
- **T1** `Temps CLI médian **159,2 ms**, API **2,7 ms**. Fiche`
- **T1** `La loi H0 se reproduit (**R² = 0,909139** sur 655 lignes, **0,906307** sur 488 paires uniques non auto) ;`
- **T1** `le retrieval brut donne **61,4 %** de même tradition et **56,8 %** de voisins à ≤50 ans ; les contrôles`
- **T1** `croisés ramènent la filiation à **50,0 %** (p=0,0492, Holm 0,128) et l'époque à **53,8 %** (p=0,373).`
- **T1** `Seule une petite prédiction d'année intra-tradition survit (**R²=0,042**, p=0,0086, Holm 0,034). Le`
- **T1** `| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |`
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |`
- **T1** `journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/rapport.md:8490:- **`tesseract`** lit la page **661/839** (79 %) ; la fin vers **03 h 52**, puis la ligne et l'ajout au train.`
- **T1** `journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/rapport.md:9489:- **T1** `travail : **sans OCR 0/30**, et la page « photo » simulée tombe à **17,08 %** de WER et **26,7 %**``
- **T1** `journal/sessions/session-9f876d8f-5661-44f0-b052-0770211328ec/rapport.md:125:- **T1** `8:> (35,7 %), **84 lectures acceptées**, mais la page sert les **369 candidats stockés le 02/11**,``
- **T1** `n2-analyse c7232b3 ANALYSEUR — L'ADVERBE DE TEMPS ET LE « QU'ELLE » : 7/7 SÉQUENCES, 94 % DE COUVERTURE`
- **T1** `journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/digest.md:36649:  4/24     12876525.1391 46.7 %`
- **T1** `-**Mis à jour : 2026-11-15, 01 h 50 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**`
- **T1** `+**Mis à jour : 2026-11-15, 02 h 15 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**`
- **T1** `**Mis à jour : 2026-11-15, 02 h 15 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 te`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 canoniq`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](../..`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 cano`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tranché (la tête du GN arrête `
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet du`
- **T1** `| S — la banque validée | **`/paragraphes` fini** : 9/9 paragraphes, 19/19 candidats, 11 acceptés, 8 exclus, **11 verdicts non committés** ; **banque 150 verdicts / 74 des 207 phrases** (35,7 %), mais`
- **T1** `- **R0** : un contrôleur **classique** + un modèle externe atteint-il **90 %** de la compréhension à **30 %** du`
- **T1** `bb68b820 J12.1 — LE §334 EST UNE GÉOMÉTRIE DE FILIATION : 655 LIGNES = 495 PAIRES UNIQUES (160 DOUBLONS, 7 AUTO-PAIRES), 48 TEXTES, 44 SIGNATURES ; H0 0,909139 / 0,906307 (488), DATE 0,0089 APRÈS TOPO`
- **T1** `"protocole": "validation data/corpus_propre/val.txt, fenêtres Van der Corput dans les chunks de 8192, 8 lots × 16 fenêtres"`
- **T1** `| [rapport-consolidation-balayage.md](rapport-consolidation-balayage.md) | Le balayage de la consolidation — un optimum INTÉRIEUR de capacité (rang 4) et de pas (3e-4), qui ne composent PAS |`
- **T1** `| [rapport-consolidation-c7.md](rapport-consolidation-c7.md) | C7 — la consolidation : le rejeu met bien l'expérience dans les poids (−16,4 % en domaine, **+1,3 % hors domaine**) |`
- **T1** `| [rapport-consolidation-structure-partagee.md](rapport-consolidation-structure-partagee.md) | Ce qui se consolide, c'est la STRUCTURE PARTAGÉE — même mémorisation (−22,5 %), transfert −7,4 % ou +1,2 `
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |`
- **T1** `"etat": "74/207 phrases complètes (35,7 %), 133 sans verdict, 147/369 candidats, 1 note, 1 annotateur",`
- **T1** `-**Mis à jour : 2026-11-15, 02 h 15 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**`
- **T1** `+**Mis à jour : 2026-11-15, 02 h 35 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**`
- **T1** `-- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 t`
- **T1** `+- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **`
- **T1** `-| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tranché (la tête du GN arrête`
- **T1** `+| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; **19/19 verdicts `/paragraphes`** (11 accept`
- **T1** `-| S — la banque validée | **`/paragraphes` fini** : 9/9 paragraphes, 19/19 candidats, 11 acceptés, 8 exclus, **11 verdicts non committés** ; **banque 150 verdicts / 74 des 207 phrases** (35,7 %), mai`
- **T1** `+| S — la banque validée | **`/paragraphes` fini** : 9/9 paragraphes, 19/19 candidats, 11 acceptés, 8 exclus, **11 verdicts committés (`389b99f`)** ; **banque 150 verdicts / 74 des 207 phrases** (35,7`
- **T1** `[still running after 60000ms; moved to background job bash-101]`
- **T1** `- **T1** `| [rapport-consolidation-structure-partagee.md](rapport-consolidation-structure-partagee.md) | Ce qui se consolide, c'est la STRUCTURE PARTAGÉE — même mémorisation (−22,5 %), transfert −7,4 `
- **T1** `- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |``
- **T1** `- **T1** `"etat": "74/207 phrases complètes (35,7 %), 133 sans verdict, 147/369 candidats, 1 note, 1 annotateur",``
- **T1** `- **T1** `-**Mis à jour : 2026-11-15, 02 h 15 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**``
- **T1** `- **T1** `+**Mis à jour : 2026-11-15, 02 h 35 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**``
- **T1** `- **T1** `-- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes*`
- **T1** `- **T1** `+- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b9`
- **T1** `- **T1** `-| S — la banque validée | **`/paragraphes` fini** : 9/9 paragraphes, 19/19 candidats, 11 acceptés, 8 exclus, **11 verdicts non committés** ; **banque 150 verdicts / 74 des 207 phrases** (35`
- **T1** `- **T1** `[still running after 60000ms; moved to background job bash-101]``

## 5. Erreurs rencontrées

9 sorties en erreur ou divergentes. Les premières :

- **T1** : 292c70b5 C1 — LA COMMANDE N2 VALIDÉE : --rope + canal (2,7856), JAMAIS --rope SEUL (40,0658), TÉMOIN 3,09 5891ef8a ÉTAT — T0 TENU : LA LIGNE FAIT RACCOURCIE 6560a0a5 1A — LE TAGGER SUR LA BASE RÉELLE 
- **T1** : ---systemctl firewalld--- active enabled ---firewall-cmd--- Error: Did not receive a reply. Possible causes include: the remote application did not send a reply, the message bus security policy blocke
- **T1** : ===== 2026-11-14 README ===== # 2026-11-14  > **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier > [`journal/2026-11-14/`](README.md). Le récit écrit à la main est conservé 
- **T1** : journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/rapport.md:7930:- **`tesseract`** lit la page **392/718** du CSS ; il finira vers **02 h 00**. journal/sessions/fe3c05f0-834b-44f2-8739-501865d652
- **T1** : MESURE_ARBRE {"phrases": 207, "candidats": 359, "segments": 2308, "profondeur_max": {"0": 2, "1": 37, "2": 221, "3": 84, "4": 13, "5": 2}, "niveaux": {"0": 359, "1": 1268, "2": 556, "3": 108, "4": 15,
- **T1** : ---nft as user--- netlink: Error: cache initialization failed: Operation not permitted Error: Operation not permitted (perhaps you must be root?) code 1 ---iptables as user--- Fatal: can't open lock f
- **T1** : ---ahead/behind--- 0	1 ---submodule ahead/behind--- 0	0 ---last parent commits touching S--- cb6ccab4 J14.1 — LA CLÔTURE : 84 PORTES, 81 VERTES, 3 ROUGES NOMMÉES (SESSIONS RÉPARÉE, INDICE ET MELANGE S
- **T1** : == /home/stephane/.bash_history [exit code: 1]
- **T1** : # 2026-11-15  > **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier > [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans > le bloc « not

## 6. Commits

- C2 — LA PAGE / NE SERT PAS LA V7 : 369 CANDIDATS SANS PROFONDEUR, 41 VERDICTS À RE-JUGER ; PORT 8765 PRIS, PARE-FEU ACTIF ; LES 11 VERDICTS COMMITTÉS (389b99f)"
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet git add reports/rapport-coordination-s-v2.md reports/rapport-coordination-s-v2.json git commit --amend --no-e
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet git add reports/rapport-coordination-s-v2.md reports/rapport-coordination-s-v2.json docs/pilotage/en-cours.md
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet git add reports/rapport-coordination-s-v2.md reports/rapport-coordination-s-v2.json docs/pilotage/en-cours.md

