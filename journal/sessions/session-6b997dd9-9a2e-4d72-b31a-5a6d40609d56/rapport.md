# Session session- — Re-mesurer 50 textes libres J11.3

> **Journaux :** [le jour](../../2026-11-14/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-6b997dd9-9a2e-4d72-b31a-5a6d40609d56` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-14 04:43 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 111 |
| Appels d'outils | 127 |
| Fichiers touchés | 6 |
| Commandes | 92 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J11.3 : re-mesurer les 50 textes libres avec le code de la semaine (F1 0,7902, le schéma v2, la restitution) : plantages, chevauchements (les deux vues), les 8 champs, le temps. Fiche `reports/rapport-robustesse-semaine.md` + JSON, comparaison avec l'audit A26.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J11.3 : re-mesurer les 50 textes libres avec le code de la semaine (F1 0,7902, le schéma v2, la restitution) : pla … [147 caractères tronqués]

*127 appels d'outils.* Actions notables :

- bash — List workspace root and reports
- bash — Search for task identifiers
- bash — Find J11 task references
- bash — Read product retest report
- bash — Locate J11 sections
- bash — Read restitution v1 report head
- bash — Read roadmap J11 section
- bash — Read semaine-autonome and en-cours
- bash — Search for the 8 fields and schema v2
- bash — Find relevant tools and tests
- bash — Read schema v2 report
- bash — Print schema v2 JSON
- bash — Inspect retest and audit JSON
- bash — Read 50-text test
- … et 106 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_robustesse_semaine.py` | 1 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-robustesse-semaine.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qrineç/tools/..` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 14 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** List workspace root and reports
- **T1** Search for task identifiers
- **T1** Find J11 task references
- **T1** Read product retest report
- **T1** Locate J11 sections
- **T1** Read restitution v1 report head
- **T1** Read roadmap J11 section
- **T1** Read semaine-autonome and en-cours
- **T1** Search for the 8 fields and schema v2
- **T1** Find relevant tools and tests
- **T1** Read schema v2 report
- **T1** Print schema v2 JSON
- **T1** Inspect retest and audit JSON
- **T1** Read 50-text test
- **T1** Read audit A26 report
- **T1** Print product retest JSON
- **T1** Read restitution v1 measurement script
- **T1** Locate key functions
- **T1** Check git state and recent commits
- **T1** Read restitution bench functions
- **T1** Inspect 50-text bank structure
- **T1** Locate CLI analyser and restitution defs
- **T1** Read analyser CLI and Annotation
- **T1** Find retest harness references
- **T1** List tools python files
- **T1** Read schema verifier
- **T1** Check evaluer JSON output
- **T1** Extract evaluation summary
- **T1** Quick baseline measurement of 50 texts
- **T1** Run restitution v1 on 50 texts
- **T1** Read mesure annotation v1 detail
- **T1** Baseline auto language measurement
- **T1** Inspect edge-case texts
- **T1** Check CLI JSON serialization
- **T1** Read dumps function
- **T1** Read audit A26 rest
- **T1** Read A26 control negative and conclusion
- **T1** Read current schema tests
- **T1** Compare A26 per-text overlap counts
- **T1** Check keys of bank results
- … et 52 autres

## 4. Mesures et résultats marquants

- **T1** `63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../..`
- **T1** `> **65,84 % des jetons** et **75,19 % des caractères** ; stabilité structurelle`
- **T1** `**Lecture.** Les segments ne couvrent que **65,84 %** des jetons : le plancher lexical`
- **T1** `devant, mais l'anglais est **100 % réel** quand le français ajoute **160 synthétiques** ; sur le`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T1** `**100 scans simulés** : la photo passe de **55,9 %** à **6,7 %** de [WER](../theorie/glossaire/entrees/wer.md) (test **5,7 %**) et la`
- **T1** `**préservation** du lecteur atteint **90–97 %** sur **4 familles sur 5** (propre **96,7 %** ;`
- **T1** `fax **56,7 %**, la limite d'information) ; les **colonnes** tombent de **89,4 %** à **0,5 %**,`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 te`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../re`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; **porte d'écriture** (hors script, hasard) ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `docs/archive/plan-deepseek41-complet.md:452:> formats. Il n'est pas un signe de défaut de calcul — les 88,9 % de top-1`
- **T1** `reports/rapport-c9-lateralite.md:80:   **listes creuses** k=128 coûtent **+35,5 %** là où les 8 bits coûtent **+3,0 %**. C'est la même`
- **T1** `reports/rapport-e1-e2-connectome-croissance.md:31:seule** : les 83 % de poids d'experts n'étaient jamais masqués. Le coût reste **modéré** (le`
- **T1** `reports/rapport-pool-tampons.md:37:  (les 8 gardés couvrent les tailles du modèle), et **7,1 Mo** retenus au lieu de ~1 Go de tampons`
- **T1** `que le rang 1 est la bonne coupe ni que la relation est réciproque.`
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
- **T1** `"Les segments ne couvrent que 65,84 % des jetons et 75,19 % des caractères en "`
- **T1** `f"couverture {surface['couverture']:.2%}",`
- **T1** `f"couverture {mots['couverture']:.2%}",`
- **T1** `f"couverture {pos['couverture']:.2%}",`
- **T1** `f"· unités sémantiques={len(a.unites_semantiques)} ({a.fraction_semantique:.1%} du texte)"`
- **T1** `| 10 000 car., phrases répétées | 0 | **590–765 ms** | 10 362 | **2 763 666 o** | spans valides, déterminisme |`
- **T1** `| 10 000 car., `a` × 10 000 | 0 | **172 ms** | 7 | 42 482 o | un seul token |`
- **T1** `| 10 000 car., ponctuation | 1 | **155 ms** | — | 0 | refus `vide` (raison fausse) |`
- **T1** `| mode lisible, `a` × 10 000 | 0 | 153 ms | — | 10 457 o | **ligne de 10 010 caractères** |`
- **T1** `10. **Taille et lot** : 2,76 Mo pour 10 000 caractères, 11,5 Mo pour 50 000 ; une invocation =`
- **T1** `temps CLI   : médiane 155.2 ms (134.4–239.9) · API médiane 2.9 ms`
- **T1** `temps CLI   : médiane 159.2 ms (142.3–257.7) · API médiane 2.7 ms`
- **T1** `| [rapport-c4-retard.md](rapport-c4-retard.md) | C4 — le prix d'un état en retard : **×633 pour UN pas**, et ce que ça impose à un ordonnanceur |`
- **T1** `| [rapport-c8-generalisation.md](rapport-c8-generalisation.md) | C8 — la tête réflexe sur des textes JAMAIS VUS : jusqu'à ×5,7 du modèle complet |`
- **T1** `| [rapport-c8-tete-entrainee.md](rapport-c8-tete-entrainee.md) | C8 — une TÊTE ENTRAÎNÉE pour sa profondeur : ×540 sur la tête empruntée |`
- **T1** `| [rapport-consolidation-balayage.md](rapport-consolidation-balayage.md) | Le balayage de la consolidation — un optimum INTÉRIEUR de capacité (rang 4) et de pas (3e-4), qui ne composent PAS |`
- **T1** `| [rapport-consolidation-c7.md](rapport-consolidation-c7.md) | C7 — la consolidation : le rejeu met bien l'expérience dans les poids (−16,4 % en domaine, **+1,3 % hors domaine**) |`
- **T1** `| [rapport-consolidation-structure-partagee.md](rapport-consolidation-structure-partagee.md) | Ce qui se consolide, c'est la STRUCTURE PARTAGÉE — même mémorisation (−22,5 %), transfert −7,4 % ou +1,2 `
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `| [rapport-s-analyseur.md](rapport-s-analyseur.md) | S — L'analyseur contre les structures écrites à la main : 7/7 séquences, 93,9 % de couverture |`
- **T1** `| [rapport-s-corpus-reel.md](rapport-s-corpus-reel.md) | S — L'analyseur lit le français propre (65,5 % de GN+GV), pas le CEGEP OCR (8,5 %, plancher du mélange) |`
- **T1** `| [rapport-familles-9.md](rapport-familles-9.md) | C3.2c — les 9 familles : 7 sur 9 au-dessus de 30 % |`
- **T1** `**521/532** étiquetées Glottolog), le top-1 de voisinage est de la même famille **66,1 %** (hasard`
- **T1** `10,3 %) et de la même branche **26,1 %** (hasard 2,5 %). Mais **hors écriture, tout est au hasard**`
- **T1** `(famille 9,9 % contre 8,1 %, sœur 0,7 % contre 0,8 %) ; dans la même écriture, la famille monte à`
- **T1** `**69,8 %** et la sœur à **27,8 %**. Le retrieval parallèle 30 articles le chiffre : sur les **25`
- **T1** `autre segment ; couverture **65,84 % des jetons**, **75,19 % des caractères**. La limite est la`
- **T1** `docs/pilotage/en-cours.md:63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produ`
- **T1** `| **J2** | après-midi : corpus commun | ✅ fait | **21 textes**, 5 familles, 10 écritures, **418/438** paires exactes (95,4 %), 8/8 contrôles | `c3467170` (avec J3.1) | corpus multi-époques / multi-gen`
- **T1** `+canonique**, le strict **5/46** ; temps CLI médian **159,2 ms**, API **2,7 ms**. Comparaison`
- **T1** `+Temps CLI médian **159,2 ms**, API **2,7 ms**. Fiche`
- **T1** `[still running after 60000ms; moved to background job bash-92]`

## 5. Erreurs rencontrées

4 sorties en erreur ou divergentes. Les premières :

- **T1** : 09e54143 J11.2 — EVALUER --PAR-LANGUE : FR 0,8159/0,7475 (151/151), EN 0,9451/0,8656 (87/88), GLOBAL INCHANGÉ 84e393bb J11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉS, r035 DÉSORMAIS PRÉDIT ; 
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 5, in <module>   File "<stdin>", line 5, in <genexpr> KeyError: 'chevauchements_syntagme' [exit code: 1]
- **T1** : docs.md memoire.md mesures.md portes.md README.md --- # 2026-11-14  > **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier > [`journal/2026-11-14/`](README.md). Le récit écrit
- **T1** : 84e393bb J11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉS, r035 DÉSORMAIS PRÉDIT ; F1 0,7902, ATTACHEMENT 238/238  docs/pilotage/en-cours.md                          |   15 +-  docs/pilotage/ro

## 6. Commits

- J11.3 — LES 50 TEXTES LIBRES : 0 PLANTAGE, 50/50 SCHÉMA V2, 115 CHEVAUCHEMENTS ALTERNATIVE / 0 FILTRER ; RESTITUTION 46/46, STRICT 0,1087 (F1 0,7902)"

