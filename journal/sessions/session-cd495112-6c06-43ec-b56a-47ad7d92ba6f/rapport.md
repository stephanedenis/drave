# Session session- — Réparation des points O(k²) et mesure α

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-cd495112-6c06-43ec-b56a-47ad7d92ba6f` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 23:43 |
| Durée | 0.8 h |
| Tours | 1 |
| Messages | 257 |
| Appels d'outils | 287 |
| Fichiers touchés | 8 |
| Commandes | 175 |
| Sous-agents | 0 |
| Commits | 5 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche U1 (exploitable, suite de T4) : **répare les deux points O(k²)** identifiés par T4 — `_groupes_partition` (toutes les paires de syntagmes) et `_cible_proche` (le tri de tous les GV pour chaque segment) — **sans changer les résultats** (les 612 phrases et le réel 452 : les mêmes F1, attachement, POS, au bit près) ; mesure le **α** de la croissance avant/après sur le bloc contrôlé de T4 (l'obj … [259 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche U1 (exploitable, suite de T4) : **répare les deux points O(k²)** identifiés par T4 — `_groupes_partition` (toutes  … [539 caractères tronqués]

*287 appels d'outils.* Actions notables :

- bash — Check repo state and recent commits
- bash — Locate the two functions
- bash — Find T4 performance report
- bash — Read the two functions
- bash — Locate linearity section in T4 report
- bash — Read bank performance next action & linearity
- bash — Read linearity section
- bash — Read performance JSON measurements
- bash — Find gold test infrastructure
- bash — Find gold reports and tests
- bash — Inspect gold files sizes
- bash — Find references to 612 and 452
- bash — Find gold evaluation scripts
- bash — Read gold evaluation tool
- … et 213 autres

**Synthèse produite :**

\## U1 — les deux O(k²) sont bornés, sorties identiques

**Résultat mesuré** (même bloc contrôlé T4, 247 mots ×1…×40 ; médianes de 3 répétitions) :

| mesure | avant | après |
|---|---:|---:|
| 10 000 mots — fonction | **3,991 s** | **0,816 s** (×4,89) |
| débit | 2 506 mots/s | **12 259 mots/s** |
| CLI `--json` | 5,011 s | **1,668 s** |
| pic RSS fonction | 126,9 Mio | **127,4 Mio** (+0,5 Mio) |
| JSON indenté | 14 795 890 o | **14 795 890 o** (identique) |
| **α** bloc contrôlé | **1,530** | **1,076** |
| ΔR² quadratique − linéaire | +0,0414 | **+0,00077** |
| contrôle linéaire | ❌ | ✅ |

**Objectif atteint** : α = 1,076 ≤ 1,15, terme quadratique non significatif.

\### Ce qui a été corrigé

- `_groupes_partition` : toutes les paires O(k²) → **balayage O(k log k)**.
- `_cible_proche` / `_verbes_proches` : tri de tous les GV à chaque segment → **`_IndexGV`** (gauche/droite/chevauchement + tas), O(log m + candidats).
- Le profil a ensuite nommé trois autres boucles quadratiques, corrigées sans changer les résultats :
  - `_sujet_hors_gv` (`any()` sur tous les segments par GV) → fins de GN triées + `bisect` ;
  - `_repli_cible_gp` / `_cible_rel_sujet` → `_IndexFins` / `_IndexSegments` ;
  - `construire_arbre` et les cibles de `_segmente` dans le générateur S → balayage O(k).
- `_expliciter_partition` : `deepcopy` des candidats → copie superficielle.

\### Contrôle négatif — diff vide

`python3 tools/verifier_performance_fix.py --comparer /tmp/u1-before /tmp/u1-after4` :

```
10/10 identiques — diff vide
```

Sont identiques **octet pour octet** : 10 000 mots, blocs ×1…×40, annotations des 612 phrases et des 452 réelles. Le générateur S a aussi été comparé directement sur **620 textes** : identique. Les métriques gold sont inchangées : POS **0,8625**, F1 syntagmes **0,7902**, attachement top-k **0,9874** sur 612 ; POS **0,8891**, F1 **0,7906**, top-k **0,9891** sur 452.

\### Tests et portes

- `tools/tests/linguistique/test_bloc_linguistique.py` : **25 tests OK** (dont 5 différentiels ancien/nouveau).
- `tools/structures/tests/test_generateur.py` : **27 tests OK**.
- `tools/tests/test_verifier_performance_fix.py` : **3 tests OK**.
- Portes ciblées U1 : **15/15 vertes** (`banc-performance`, `bloc-linguistique`, `produit`, `budget`, `état`, `sessions`, `registre`, etc.), puis **2/2** après commit.
- Revue de documentation, `verifie_en_cours`, `verifie_journal`, budget : **verts**.
- La passe complète des 86 portes n’a pas été relancée (précédent T6) ; les rouges
… [722 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py` | 0 | 22 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_generateur.py` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance-fix.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 11 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** Check repo state and recent commits
- **T1** Locate the two functions
- **T1** Find T4 performance report
- **T1** Read the two functions
- **T1** Locate linearity section in T4 report
- **T1** Read bank performance next action & linearity
- **T1** Read linearity section
- **T1** Read performance JSON measurements
- **T1** Find gold test infrastructure
- **T1** Find gold reports and tests
- **T1** Inspect gold files sizes
- **T1** Find references to 612 and 452
- **T1** Find gold evaluation scripts
- **T1** Read gold evaluation tool
- **T1** Read evaluer_gold CLI and tests
- **T1** Count gold sentences
- **T1** Read main of evaluer_gold
- **T1** Read bloc tests
- **T1** Read _cible_proche call sites
- **T1** Locate helper functions
- **T1** Read adverbe helper and subject function
- **T1** Read _est_adverbe_seul and _sujet_hors_gv
- **T1** List all call sites
- **T1** External call sites
- **T1** Inspect Annotation json output
- **T1** Read Annotation json emitter
- **T1** Read bank CLI options
- **T1** Read bank end and CLI
- **T1** Read argument parser
- **T1** Run baseline performance bank
- **T1** Run baseline gold evaluation
- **T1** Read partition explicit function rest
- **T1** Check partition filter mode
- **T1** Inspect baseline gold results
- **T1** Check baseline bank progress
- **T1** Read block construction
- **T1** Read Heuristique init defaults
- **T1** Generate baseline annotation JSONs
- **T1** Check imports
- **T1** Compile and run bloc tests
- … et 135 autres

## 4. Mesures et résultats marquants

- **T1** `83adaa2b T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE`
- **T1** `9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS`
- **T1** `7f0e8320 T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))`
- **T1** `# T4 — la performance de `drave analyser` : 10 000 mots en 4,0 s, 126 Mio, 14,8 Mo de JSON ; le contrôle de linéarité **échoue** (α = 1,55)`
- **T1** `> fonction, 2 493 mots/s, 126 Mio de pic RSS, 14,8 Mo de JSON) ; ❌ **le contrôle négatif de`
- **T1** `> quadratique explique **R² 0,99995** contre **0,957** pour le linéaire. Le coupable est`
- **T1** `> **2 014 mots/s** (CLI), **128 972 Ko** de pic RSS (126 Mio ; 167,6 Mio pour le CLI),`
- **T1** `> Sur **100 phrases courtes** (661 mots, médiane 6 mots) : **1,10 ms/appel** pour la`
- **T1** `> fonction, **1,18 ms** de coût fixe, **191,6 ms/appel** pour le CLI (démarrage compris),`
- **T1** `> et **0,369 s** pour les 100 en un seul `--jsonl` (×52,6 vs 100 CLI). Avec `--tagger` et`
- **T1** `> soit **×299** le lot heuristique ; l'extrapolation aux 10 000 mots donne **797 appels**,`
- **T1** `| pic RSS (fonction) | **128 972 Ko = 125,9 Mio** |`
- **T1** `| pic RSS (CLI) | **171 656 Ko = 167,6 Mio** |`
- **T1** `| taille du JSON indenté | **14 795 890 octets = 14,8 Mo** (1 480 octets/mot) |`
- **T1** `de démarrage et d'import, le reste en écriture de 14,8 Mo. Le JSONL compact est **plus gros**`
- **T1** `(17,7 Mo) que le JSON global (14,8 Mo) parce qu'il analyse chaque phrase séparément : le`
- **T1** `| 100 appels **fonction** séparés | **1,10 ms/appel** (médiane ; p95 2,14 ms ; 0,116 s pour 100) |`
- **T1** `| coût fixe ajusté `t = a + b·mots` | **a = 1,18 ms** · b = 0,00 ms/mot |`
- **T1** `| 100 appels **CLI** séparés | **191,6 ms/appel** (médiane ; p95 219,8 ms ; 19,43 s pour 100) |`
- **T1** `| pic RSS d'un appel CLI | **31 938 Ko = 31,2 Mio** (médiane) |`
- **T1** `| un seul `--jsonl` pour les 100 | **0,369 s**, soit **3,69 ms/phrase** |`
- **T1** `| accélération du lot vs 100 CLI | **×52,6** |`
- **T1** `Le **coût fixe de la fonction est ~1,1 ms** ; la pente par mot est négligeable sur cette`
- **T1** `plage de 3–12 mots. Le **coût fixe du CLI est ~190 ms**, presque entièrement le démarrage`
- **T1** `| pic RSS | **34 308 Ko = 33,5 Mio** |`
- **T1** `| comparaison au lot heuristique | **×299** (110,204 s contre 0,369 s) |`
- **T1** `chunker le plus large **est** ce span (86,5 %) ; le S le plus large ne l'est que 25 fois sur 244.`
- **T1** `1:# T4 — la performance de `drave analyser` : 10 000 mots en 4,0 s, 126 Mio, 14,8 Mo de JSON ; le contrôle de linéarité **échoue** (α = 1,55)`
- **T1** `211:| `_cible_proche` | 1 040 | **14,474 s** | 30 % |`
- **T1** `214:| `_groupes_partition` | 1 | **11,162 s** | 23 % |`
- **T1** `| 9 880 | 4 960 | 13,701 | 1,54 (×1,25 mot) | 1,25 | 1,56 |`
- **T1** `doublement (×1,25) : il vaut 1,54, soit presque le **1,56** attendu d'un quadratique.`
- **T1** `volontairement linéaire (`n × 200` additions) et une boucle volontairement quadratique`
- **T1** `## 6. Le coupable — le profil du bloc ×16`
- **T1** ``cProfile` sur le bloc ×16 (3 952 mots, 1 984 syntagmes) donne **48,6 s profilées** pour`
- **T1** `| `analyser` | 1 | 48,588 s | 100 % |`
- **T1** `| `_cible_proche` | 1 040 | **14,474 s** | 30 % |`
- **T1** `| `_expliciter_partition` | 1 | **14,330 s** | 29 % |`
- **T1** `| `_est_adverbe_seul` | **768 048** | **11,606 s** | 24 % |`
- **T1** `| `_groupes_partition` | 1 | **11,162 s** | 23 % |`
- **T1** `| `_sujet_hors_gv` | 1 | 5,964 s | 12 % |`
- **T1** `| `_verbes_proches` | 1 984 | 3,170 s | 7 % |`
- **T1** `| `deepcopy` | 171 610 | 3,019 s | 6 % |`
- **T1** `à k = 4 960 (bloc ×40), ~12,3 M. C'est la part qui double le plus vite.`
- **T1** `de pic RSS, **14,8 Mo** de JSON : c'est un traitement par lots confortable sur une`
- **T1** `- **100 phrases courtes en 1,1 ms** par appel de fonction ; le lot `--jsonl` fait **0,37 s**`
- **T1** `Le réseau porte **99 %** du temps ; le coût monétaire est ~0,05 $. À réserver au`
- **T1** `[still running after 60000ms; moved to background job bash-47]`
- **T1** `# un passage COURT du banc (1 000 mots, 20 phrases, 3 tailles, bloc ×1/×2/×4) hors ligne.`
- **T1** `docs/pilotage/en-cours.md:63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.m`
- **T1** `docs/pilotage/roadmap.md:33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 c`
- **T1** `docs/pilotage/roadmap.md:38:**État au 15/11 (nuit).** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **PO`
- **T1** `docs/pilotage/roadmap.md:306:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** +`
- **T1** `docs/pilotage/roadmap.md:381:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantiq`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/r`
- **T1** `- **Note** : l'attachement est à **236/237 (0,9916)**, la couverture 0,9916, POS **86,25 %**, F1 **0,7535**, 2 spans ; la seule rouge est`
- **T1** `CPU + neuronal de contrat, parallèle/cascade, activation 51–76 %) ; **398 langues à 0,9687**,`
- **T1** `**tête 0,560**, pragmatique **1,0/1,0/0,994/0,889** ; cascade (mock) **67,1 %** ;`
- **T1** `| 23:30 | `9a291c8b` | T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS | `en-cours.md`, `roadmap.md`, `README.m`
- **T1** `**14,8 Mo** JSON ; 100 phrases **1,10 ms** ; `--tagger` **1,17 s/phrase**.`
- **T1** `**Contrôle de linéarité négatif** : **α = 1,55**, **R² 0,99995** ;`
- **T1** `public** à **88,70 %** d'attachement au lieu de **99,58 %**, croissance **O(k²)** (α = **1,55**),`
- **T1** `65:- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../reports/r`
- **T1** `**U1 — les deux O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),`
- **T1** `- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../reports/rapp`
- **T1** `**14,8 Mo** JSON ; α = **1,55**, `_groupes_partition`/`_cible_proche` **O(k²)**.`
- **T1** `réparée, 86e porte `porte-banc-performance` verte. Trois limites : clone public 88,70 %`
- **T1** `d'attachement au lieu de 99,58 %, O(k²) (α = 1,55), gold de S non humain.`
- **T1** `| `porte-c4-retard.sh` | 29 s | PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne |`
- **T1** `| `porte-coupe.sh` | 131 s | ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit pour  |`
- **T1** `| `porte-delais.sh` | 21 s | ✅ le temps, lui, augmente : 6.77 s → 9.67 s (+2.9 s ≈ 50 ms × 64 pas) |`
- **T1** `| `porte-homeostasie.sh` | 495 s | ✅ porte tenue (×0 exact · activité monotone · dominance reproduite) |`
- **T1** `| `porte-jeux.sh` | 104 s | ✅ la porte des jeux tient : 100 % au niveau 4, 33/33 paires invariantes, 0 collision, |`
- **T1** `| `porte-mistral.sh` | 8 s | ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= plancher  |`
- **T1** `| `porte-pont.sh` | 79 s | ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux |`
- **T1** `| `porte-reflexe.sh` | 141 s | ✅ 3. l'accord est mesuré AVANT (0.4 %) et APRÈS — la mesure est branchée |`
- **T1** `| `porte-reparti-moteur.sh` | 3 s | PORTE TENUE : le découpage ne change pas la perplexité (écart relatif 0.0000 %) |`
- **T1** `+| [rapport-performance-fix.md](rapport-performance-fix.md) | U1 — les deux O(k²) sont bornés : 10 000 mots de **4,0 s à 0,82 s** (×4,9), α de **1,53 à 1,08**, sorties **identiques au bit près** |`
- **T1** `| [rapport-performance.md](rapport-performance.md) | T4 — la performance de `drave analyser` : 10 000 mots en 4,0 s, 126 Mio, 14,8 Mo de JSON ; le contrôle de linéarité **échoue** (α = 1,55) |`
- **T1** `[still running after 60000ms; moved to background job bash-149]`
- **T1** `d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO`
- **T1** `[still running after 60000ms; moved to background job bash-153]`

## 5. Erreurs rencontrées

4 sorties en erreur ou divergentes. Les premières :

- **T1** : tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/gold_reel.py tools/tests/linguistique/qualifier_cascade.py tools/tests/linguistique/qualifier_lien_appris.py tools/tests/linguistique/
- **T1** : groupes OK MISMATCH cible 3669 {'debut': 40, 'fin': 42, 'type': 'GP'} L None [(40, 41, 'L')] [exit code: 1]
- **T1** : /tmp/u1-before/performance-avant.json    247   124 0.050 rss 37860    494   248 0.113 rss 43108    988   496 0.300 rss 51948   1976   992 0.828 rss 70404   3952  1984 2.461 rss 107564   7904  3968 8.8
- **T1** : #!/bin/bash # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait. # # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS # (`--attn-window` en r

## 6. Commits

- U1 — générateur S : construire_arbre et cibles en O(k), sorties identiques (620 textes)" && git log --oneline -1
- U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE)
- U1 — LA FICHE POINTE SES COMMITS : AVANT 83ADAA2B, APRÈS D19F0FC7 (SOUS-MODULE 648ADCE)" 2>&1 | tail -20
- U1 — LA FICHE POINTE SES COMMITS : AVANT 83ADAA2B, APRÈS D19F0FC7 (SOUS-MODULE 648ADCE)" 2>&1 | tail -25
- U1 — LE CONTRÔLE DE L'INSTRUMENT EST CELUI DE LA PASSE : LINÉAIRE 0,71, QUADRATIQUE 2,11 (ET NON LES VALEURS DE T4)" 2>&1 | tail -20

