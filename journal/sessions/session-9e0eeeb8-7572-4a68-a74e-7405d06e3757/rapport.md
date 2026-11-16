# Session session- — Ajouter --strict à evaluer

> **Journaux :** [le jour](../../2026-11-16/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-9e0eeeb8-7572-4a68-a74e-7405d06e3757` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-16 02:13 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 151 |
| Appels d'outils | 177 |
| Fichiers touchés | 7 |
| Commandes | 105 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche V1 (exploitable, la suite du bilan T6) : `evaluer --strict` — le banc de recherche (`evaluer_gold.py`) mesure quatre modes et la cascade locale avec le plancher 0,70 ; le CLI ne le fait pas. Ajoute `--strict` à `evaluer` : mesure la **cascade locale** (`MockNeuronal`) sur 612 et le réel 452, **applique le plancher 0,70** (un échec = code 1), affiche les quatre modes (heuristique, neuronal, p … [173 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche V1 (exploitable, la suite du bilan T6) : `evaluer --strict` — le banc de recherche (`evaluer_gold.py`) mesure quat … [453 caractères tronqués]

*177 appels d'outils.* Actions notables :

- bash — List repo root and git state
- bash — Find references to evaluer_gold
- bash — Find evaluer files
- bash — Search evaluer in tools
- bash — Read evaluer_gold.py start
- bash — Read evaluer CLI section
- bash — Read remainder of evaluer_gold.py
- bash — Search drave.py for relevant terms
- bash — Find T6 references
- bash — Find block classes
- bash — Read T6 bilan report
- bash — Read MockNeuronal and Cascade classes
- bash — Find V1/T6 mentions in state docs
- bash — Read parser construction
- … et 135 autres

**Synthèse produite :**

\## V1 — `evaluer --strict` livré

\### Ce qui a été ajouté

- **`tools/drave.py`** : nouveau drapeau `--strict` sur `evaluer`.
  - mesure les **quatre modes** : heuristique, `MockNeuronal`, parallèle, cascade ;
  - sur le **gold vivant 612** et le **gold réel 452** ;
  - affiche POS, F1, tête et le **delta contre l'heuristique** ;
  - applique le **plancher 0,70** à la cascade POS sur les deux golds ;
  - sort en **code 1** si l'un des deux est sous le plancher ;
  - contrôle négatif intégré : cascade dégradée (POS forcé à `X`) → **0,0000**, `code: 1` ;
  - exclusif avec `--gold`, `--tagger`, `--par-langue` (code 5).

\### Chiffres mesurés

| gold | mode | POS | F1 | tête | ΔPOS vs heuristique |
|---|---|---:|---:|---:|---:|
| **612** | heuristique | **0,8625** | 0,7902 | 0,9029 | — |
| 612 | neuronal | 0,7540 | 0,7651 | 0,8807 | −10,85 pts |
| 612 | parallèle | 0,8625 | 0,7902 | 0,9029 | +0,00 |
| 612 | **cascade** | **0,8625** | 0,7902 | 0,9029 | +0,00 |
| **452** | heuristique | **0,8891** | 0,7906 | 0,8990 | — |
| 452 | neuronal | 0,7621 | 0,7448 | 0,8697 | −12,70 pts |
| 452 | parallèle | 0,8891 | 0,7906 | 0,8990 | +0,00 |
| 452 | **cascade** | **0,8891** | 0,7906 | 0,8990 | +0,00 |

**Plancher** : cascade POS **0,8625** (612) et **0,8891** (452) → **code 0**.  
**Contrôle négatif** : cascade dégradée **0,0000** → **code 1** ; un test vérifie aussi que `cmd_evaluer` rend bien 1 quand le verdict est faux.

\### Fichiers

- `tools/drave.py` — `--strict`, `PLANCHER_STRICT`, `_evaluer_strict`, `_verdict_strict`, `_formater_strict`.
- `tools/tests/test_evaluer_strict.py` — **5 tests** (quatre modes, sortie lisible, négatif code 1, options exclusives, aide).
- `tools/porte-produit.sh` — exécute le nouveau test.
- `tools/verifier_faq.py` — `--strict` n’est plus une option fantôme.
- `docs/produit/README.md` **§ 3.3** — notice du mode strict, sortie réelle, limites.
- `docs/pilotage/en-cours.md` et `docs/pilotage/roadmap.md` — état et ligne V1.
- `reports/rapport-evaluer-strict.md` — fiche complète.
- `reports/evaluer-strict.json` — rapport JSON.
- `reports/README.md` et `reports/INDEX.md` — indexation.

\### Vérifications

- `tools/tests/test_evaluer_strict.py` : **5/5**.
- `pytest` strict + produit : **35 passed**.
- `tools/porte-produit.sh` : **verte**, dont `evaluer --strict : Ran 5 tests`.
- `tools/porte-bloc-linguistique.sh` : **verte**.
- `revue_documentation.py`, `taille_documents.py`, `porte-tableaux.sh`, `verifier_faq.py` (10/10), `verifie_en_cours.py`,
… [285 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py` | 0 | 9 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-produit.sh` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md` | 0 | 8 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 14 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 7 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 6 |

### Commandes exécutées (échantillon)

- **T1** List repo root and git state
- **T1** Find references to evaluer_gold
- **T1** Find evaluer files
- **T1** Search evaluer in tools
- **T1** Read evaluer_gold.py start
- **T1** Read evaluer CLI section
- **T1** Read remainder of evaluer_gold.py
- **T1** Search drave.py for relevant terms
- **T1** Find T6 references
- **T1** Find block classes
- **T1** Read T6 bilan report
- **T1** Read MockNeuronal and Cascade classes
- **T1** Find V1/T6 mentions in state docs
- **T1** Read parser construction
- **T1** Find cascade local reports
- **T1** Inspect gold counts
- **T1** Read four modes report
- **T1** Read four modes 432 report
- **T1** Measure four modes on 612 and 452
- **T1** List tests and evaluer tests
- **T1** Find CLI tests
- **T1** Read product test style
- **T1** Read tagger evaluer tests
- **T1** Find doc section 3.3
- **T1** Show evaluer help
- **T1** Read product README section 3.3
- **T1** Read README context and reel
- **T1** Inspect existing uncommitted diffs
- **T1** Read results method
- **T1** Inspect four modes qualification thresholds
- **T1** Search floor 0.70 references
- **T1** Read qualifier_quatre_modes
- **T1** Read cascade thresholds and floors report
- **T1** Inspect Etiquette dataclass
- **T1** Inspect Annotation class
- **T1** Read Etiquette and Annotation definitions
- **T1** Check cascade neuronal calls
- **T1** Read pyproject
- **T1** Read product gates
- **T1** Inspect _dumps
- … et 65 autres

## 4. Mesures et résultats marquants

- **T1** `> (**2 493 mots/s**, **126 Mio**, **14,8 Mo** de JSON) ; la CLI rend **20/20** cas et **cinq`
- **T1** `> perd le sous-module S (attachement **88,70 %** au lieu de **99,58 %**), et le **gold de S**`
- **T1** ``langue=fr`, 20 étiquettes et deux syntagmes ; `drave evaluer` rend POS **86,25 %**, F1`
- **T1** `**81,88 %**, attachement exact **88,70 %**, avec le contrôle négatif **1,67 %**. Le **JSON** est`
- **T1** `| F1 | **81,88 %** | **79,02 %** |`
- **T1** `| attachement exact | **88,70 %** | **99,58 %** |`
- **T1** `| JSON | — | **14 795 890 octets** (14,8 Mo) |`
- **T1** `**Le coût fixe.** Cent phrases courtes (661 mots, médiane 6) coûtent **1,10 ms/appel** pour la`
- **T1** `fonction, **191,6 ms/appel** pour le CLI (démarrage compris), et **0,369 s** en un seul`
- **T1** ``--jsonl` : le lot est **×52,6** plus rapide que 100 CLI séparés. Pour un corpus, utiliser le lot`
- **T1** `(159,5/appel), **1,17 s/phrase**, soit **×299** le lot heuristique. Le réseau porte **109,1 s sur`
- **T1** `doublements passent de **2,29** à **3,72**, le modèle quadratique donne **R² 0,99995** et`
- **T1** `et `_est_adverbe_seul` (768 048 appels sur le bloc ×16) amplifient. Le nombre de **syntagmes**,`
- **T1** `**`--duree`.** Le drapeau ajoute `cout.duree_s` — **4,7 à 5,6 ms** sur « Le chat dort. »,`
- **T1** `**5,9 ms** sur la phrase longue — **et rien d'autre** : sans le drapeau le champ est **absent**,`
- **T1** `docs/pilotage/roadmap.md:33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 c`
- **T1** `docs/pilotage/roadmap.md:35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 lan`
- **T1** `docs/pilotage/roadmap.md:84:canonique**, le strict **5/46** ; temps CLI médian **159,2 ms**, API **2,7 ms**. Comparaison`
- **T1** `docs/pilotage/roadmap.md:309:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** +`
- **T1** `docs/pilotage/roadmap.md:328:| **N2** | la distillation : corpus, professeur, [curriculum](../theorie/glossaire/entrees/curriculum.md) | 🔬 | **N2.h** — corpus dédupliqué (**0 %** de fuite) : la chaîne`
- **T1** `docs/pilotage/roadmap.md:384:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantiq`
- **T1** `self.assertEqual(donnees["tagger"]["cout"]["appels"], 2)  # 2 phrases × 1 tagger`
- **T1** `self.assertEqual(cout["appels"], 500)     # 1 appel pour 2 phrases, × 500`
- **T1** `self.assertEqual(cout["tokens"], 8500)    # 17 tokens pour 2 phrases, × 500`
- **T1** `POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)`
- **T1** `SYNTAGMES   F1 79.02 %  (P 78.60 % / R 79.44 %)`
- **T1** `tête      F1 90.29 %  (P 92.61 % / R 88.08 %)`
- **T1** `vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture`
- **T1** `ATTACHEMENT exact 99.58 % · couverture 99.58 % · exact sur span 100.00 % · top-k 98.74 %`
- **T1** `tête      couverture 100.00 % · top-k 99.16 %`
- **T1** `PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %`
- **T1** `FRACTION SÉMANTIQUE 54.76 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)`
- **T1** `**Lecture.** `exact 99.58 %` est le **rendement** (238/239 cibles) ; `exact sur span 100.00 %` est`
- **T1** ``--gold` mesure le gold gelé 602 (F1 78,82 %, POS 86,25 %). La commande sort **0** : elle ne`
- **T1** `POS 94.51 % (fermé 98.30 %, ouvert 90.54 %) · SYNTAGMES F1 86.56 % (tête 95.27 %)`
- **T1** `ATTACHEMENT exact 98.86 % · couverture 98.86 % · top-k 98.86 % · PRAGMATIQUE acte 99.52 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 2.27 % (graine 0, 88 cibles)`
- **T1** `POS 81.59 % (fermé 90.92 %, ouvert 73.25 %) · SYNTAGMES F1 74.75 % (tête 87.33 %)`
- **T1** `ATTACHEMENT exact 100.00 % · couverture 100.00 % · top-k 98.68 % · PRAGMATIQUE acte 99.75 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.99 % (graine 0, 151 cibles)`
- **T1** `POS (94,51 % contre 81,59 %) et en syntagmes (F1 86,56 % contre 74,75 %) ; l'attachement est`
- **T1** `**88,91 %**, F1 **79,06 %**, attachement **99,46 %**. Sans lui, `evaluer` publie la ligne`
- **T1** `langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `| [rapport-a83-defaut.md](rapport-a83-defaut.md) | A8.3 — le défaut place+perte n'est pas neutre : les portes épinglées bougent de −5,9 % à +19,5 % |`
- **T1** `| [rapport-a83a-coupe.md](rapport-a83a-coupe.md) | A8.3a — `porte-coupe` : le régime 1 % écrase la variance du point de coupe |`
- **T1** `| [rapport-a83a-flux.md](rapport-a83a-flux.md) | A8.3a — `porte-flux` : le régime 1 % a ses propres références |`
- **T1** `| [rapport-a83a-pont.md](rapport-a83a-pont.md) | A8.3a — `porte-pont` : le régime 1 % change la falaise |`
- **T1** `| [rapport-a83d-lot-threads.md](rapport-a83d-lot-threads.md) | A8.3d — le lot n'est pas les threads : l'écart de 1,90 % survit à 1 thread |`
- **T1** `| [rapport-autotest-parallele.md](rapport-autotest-parallele.md) | B13 — la vérification parallèle : 183/183 en 1 min 54 (×2,4) |`
- **T1** `| [rapport-speculatif-reflexe.md](rapport-speculatif-reflexe.md) | Le réflexe propose, le cerveau vérifie — acceptation 2 à 30 % (le cerveau non entraîné : 0 %) |`
- **T1** `| [rapport-vitesse-v41.md](rapport-vitesse-v41.md) | Rapport — La nuit des optimisations V4.1 : ×3,54 sur la passe, et pas un chiffre changé |`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-tagger-lot.md`](rapport-tagger-lot.md) | **X3/R0.7** — le tagger **en lot** : **1 000 items** (677 textes), **672 appels réseau**, **99 971 tokens**, **685,2 s**, **87,6 items/min**, **40,`
- **T1** `| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `| [`rapport-pos-anglais-v2.md`](rapport-pos-anglais-v2.md) | **B13** — POS **83,83 %** (R2a/R3/R2b), F1 **0,6181** |`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.`
- **T1** `**14,8 Mo** JSON ; α = **1,55**, `_groupes_partition`/`_cible_proche` **O(k²)**.`
- **T1** `**U1 — les O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),`
- **T1** `20/20. Trois limites : clone public 88,70 % d'attachement au lieu de 99,58 %, O(k²) (α = 1,55),`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T1** `**100 scans simulés** : la photo passe de **55,9 %** à **6,7 %** de [WER](../theorie/glossaire/entrees/wer.md) (test **5,7 %**) et la`
- **T1** `**préservation** du lecteur atteint **90–97 %** sur **4 familles sur 5** (propre **96,7 %** ;`
- **T1** `fax **56,7 %**, la limite d'information) ; les **colonnes** tombent de **89,4 %** à **0,5 %**,`
- **T1** `les **tableaux** donnent **92,6 %** de cellules exactes, et **trois vrais scans** s'accordent à`
- **T1** `**7,10 %** et **88,4 %** de mots, l'**ordre des colonnes** prouvé (**15,3 %** contre **98,0 %**`
- **T1** `611 ms. La restitution depuis un document lu est **R31**.`
- **T1** `suivante, jamais l'attente. **N5 est gelé** jusqu'au verdict de R11 sur le contexte ; B10.3 attend un **z qui porte** : l'objectif mot a levé le décodeur (32,5 ; **26,7 sur JW, au-dessus du plancher 1`
- **T1** `[A1–A8] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[A8.0/A8.3a] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[A8.3b/c] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[A2.6] lasts 2 days and is 30% complete and is colored in #b26a00`
- **T1** `heuristique    86.25 %         —   79.02 %         —   90.29 %         —`
- **T1** `neuronal       75.40 % -10.85 pts   76.51 % -2.51 pts   88.07 % -2.22 pts`
- **T1** `parallele      86.25 % +0.00 pts   79.02 % +0.00 pts   90.29 % +0.00 pts`
- **T1** `cascade        86.25 % +0.00 pts   79.02 % +0.00 pts   90.29 % +0.00 pts`
- **T1** `heuristique    88.91 %         —   79.06 %         —   89.90 %         —`
- **T1** `neuronal       76.21 % -12.70 pts   74.48 % -4.58 pts   86.97 % -2.93 pts`
- **T1** `parallele      88.91 % +0.00 pts   79.06 % +0.00 pts   89.90 % +0.00 pts`
- **T1** `cascade        88.91 % +0.00 pts   79.06 % +0.00 pts   89.90 % +0.00 pts`
- **T1** `PLANCHER 0.70 — cascade POS 86.25 % (612) ✅ · 88.91 % (452) ✅ — code 0`
- **T1** `CONTRÔLE NÉGATIF cascade dégradée (POS forcé à X) · POS 0.00 % < 0.70 ✅ (échec attendu, code 1)`
- **T1** `heuristique    86.25 %           —   79.02 %           —   90.29 %           —`
- **T1** `neuronal       75.40 %  -10.85 pts   76.51 %   -2.51 pts   88.07 %   -2.22 pts`
- **T1** `parallele      86.25 %   +0.00 pts   79.02 %   +0.00 pts   90.29 %   +0.00 pts`
- **T1** `cascade        86.25 %   +0.00 pts   79.02 %   +0.00 pts   90.29 %   +0.00 pts`
- **T1** `heuristique    88.91 %           —   79.06 %           —   89.90 %           —`
- **T1** `neuronal       76.21 %  -12.70 pts   74.48 %   -4.58 pts   86.97 %   -2.93 pts`
- **T1** `parallele      88.91 %   +0.00 pts   79.06 %   +0.00 pts   89.90 %   +0.00 pts`
- **T1** `cascade        88.91 %   +0.00 pts   79.06 %   +0.00 pts   89.90 %   +0.00 pts`
- **T1** `236:cascade        86.25 %   +0.00 pts   79.02 %   +0.00 pts   90.29 %   +0.00 pts`
- **T1** `244:cascade        88.91 %   +0.00 pts   79.06 %   +0.00 pts   89.90 %   +0.00 pts`
- **T1** `247:PLANCHER 0.70 — cascade POS 86.25 % (612) ✅ · 88.91 % (452) ✅ — code 0`
- **T1** `248:CONTRÔLE NÉGATIF cascade dégradée (POS forcé à X) · POS 0.00 % < 0.70 ✅ (échec attendu, code 1)`
- **T1** `255:**code 1**. Ici la cascade vaut **86,25 %** (612) et **88,91 %** (452) : **code 0**.`
- **T1** `490:langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `+| [rapport-evaluer-strict.md](rapport-evaluer-strict.md) | V1 — `evaluer --strict` : les quatre modes locaux, la cascade à 86,25 % / 88,91 %, le plancher 0,70 qui mord |`
- **T1** `| [rapport-prelire-grappe.md](rapport-prelire-grappe.md) | S4 — le préchargement par grappe : la lecture à la demande rend 29 Mo/s là où la grappe rend 1 230 |`
- **T1** `188:| [rapport-evaluer-strict.md](rapport-evaluer-strict.md) | V1 — `evaluer --strict` : les quatre modes locaux, la cascade à 86,25 % / 88,91 %, le plancher 0,70 qui mord |`
- **T1** `...................................                                      [100%]`
- **T1** `docs/produit/README.md:235:parallele      86.25 %   +0.00 pts   79.02 %   +0.00 pts   90.29 %   +0.00 pts`
- **T1** `docs/produit/README.md:243:parallele      88.91 %   +0.00 pts   79.06 %   +0.00 pts   89.90 %   +0.00 pts`
- **T1** `parallèle      86.25 %   +0.00 pts   79.02 %   +0.00 pts   90.29 %   +0.00 pts`
- **T1** `| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO | `en`
- **T1** `| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO |`
- **T1** `parallèle      88.91 %   +0.00 pts   79.06 %   +0.00 pts   89.90 %   +0.00 pts`
- **T1** `**code 1**. Ici la cascade vaut **86,25 %** (612) et **88,91 %** (452) : **code 0**.`

