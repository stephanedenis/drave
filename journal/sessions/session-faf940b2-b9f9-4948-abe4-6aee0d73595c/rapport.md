# Session session- — Robustesse de la CLI

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-faf940b2-b9f9-4948-abe4-6aee0d73595c` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 23:16 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 103 |
| Appels d'outils | 121 |
| Fichiers touchés | 0 |
| Commandes | 110 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche T5 (exploitable, 5/5) : la **robustesse de la CLI** — (1) `--duree` dans le JSON (le temps de l'analyse) ; (2) le **tableau des codes de sortie** (0 succès, 3 refus, 4 clé/dépendance, 5 usage) dans `docs/produit/README.md` et le `--aide` ; (3) `--aide`/`--help` vérifiés sur les quatre sous-commandes ; (4) un `--fichier` sur un chemin **inexistant** et un **répertoire** : le message et le cod … [124 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche T5 (exploitable, 5/5) : la **robustesse de la CLI** — (1) `--duree` dans le JSON (le temps de l'analyse) ; (2) le  … [404 caractères tronqués]

*121 appels d'outils.* Actions notables :

- bash — Check git status and list files
- bash — List key directories
- bash — Read product README
- bash — Find CLI implementation
- bash — Read CLI head
- bash — Find durations, file, exits in CLI
- bash — Read text/file and analyser
- bash — Read main and parser
- bash — Search spec for exit code 5 and duree
- bash — Inspect existing tests exit code assumptions
- bash — Read product tests
- bash — Read plan T5
- bash — Find code 2 references
- bash — Find usage/error messages
- … et 97 autres

**Synthèse produite :**

T5 est livré, mesuré, testé et committé.

\## Ce qui a été fait

1. **`--duree`** — ajouté à `analyser` pour `--json` et `--jsonl` : `cout.duree_s` (4,7–5,9 ms sur les phrases de test). Absent par défaut, donc le déterminisme de `--json` / `rejouer` est conservé. La durée est le **seul** ajout (texte et étiquettes identiques).

2. **Codes de sortie** — contrat passé à **0 succès / 3 refus / 4 clé ou dépendance / 5 usage / 1 autre erreur** :
   - `2` → `5` pour tous les usages (`argparse`, langue inconnue, options exclusives) ;
   - `--fichier` inexistant → **4** (`dépendance absente : fichier introuvable`) ;
   - `--fichier` sur un répertoire → **5** (`erreur d'usage : un répertoire n'est pas un fichier`) ;
   - refus de `rejouer` → **3** au lieu de 1 ;
   - tableau écrit dans `docs/produit/README.md` **et** dans `--aide`.

3. **`--aide` / `--help`** — les 8 combinaisons sur les 4 sous-commandes sortent **0** et affichent leur usage.

4. **Fixtures** — `reports/rapport-cli-robuste.md`, `reports/cli-robuste.json`, banc reproductible `tools/banc_cli_robuste.py` : **20/20 cas**. Tests ajoutés dans `tools/tests/test_produit.py` (durée JSON/JSONL, tableau, aide/help, fichier inexistant, répertoire) ; les attentes des autres tests CLI ont été alignées sur le nouveau code 5.

\## Vérifications

- `python3 tools/tests/test_produit.py` → **30 tests OK**
- `python3 tools/banc_cli_robuste.py` → **20/20 cas**
- `bash tools/porte-produit.sh` → **✅ porte produit verte** (autotest 183/183)
- `revue_documentation.py`, `porte-tableaux.sh`, `verifie_en_cours.py`, `verifie_journal.py`, `verifier_schemas.py`, `taille_documents.py` → verts
- Commit : **`9a291c8b`** — `T5 — LA CLI ROBUSTE : --DUREE …, CODES 0/3/4/5 …, AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS`

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Check git status and list files
- **T1** List key directories
- **T1** Read product README
- **T1** Find CLI implementation
- **T1** Read CLI head
- **T1** Find durations, file, exits in CLI
- **T1** Read text/file and analyser
- **T1** Read main and parser
- **T1** Search spec for exit code 5 and duree
- **T1** Inspect existing tests exit code assumptions
- **T1** Read product tests
- **T1** Read plan T5
- **T1** Find code 2 references
- **T1** Find usage/error messages
- **T1** Find cout/duree in block
- **T1** Read docs and faq verifier sections
- **T1** Search planning docs for T5
- **T1** Read planning and quickstart report
- **T1** Read quickstart error section
- **T1** Read block CLI and annotation json
- **T1** Read evaluer
- **T1** Find code 2 in faq artifacts
- **T1** Find all code 2 references
- **T1** Read product gate
- **T1** Check date, branch, state
- **T1** Read report format examples
- **T1** Locate README lines to edit
- **T1** Read exact README blocks
- **T1** Read CLI command list
- **T1** Read FAQ verifier top/main
- **T1** Find remaining code refs in product docs
- **T1** Apply CLI robustness changes
- **T1** Test duree JSON
- **T1** Test file and usage errors
- **T1** Inspect help outputs
- **T1** Test jsonl duration
- **T1** Add T5 tests and run
- **T1** Update product docs
- **T1** Update FAQ verifier and run
- **T1** Run product tests
- … et 70 autres

## 4. Mesures et résultats marquants

- **T1** `7f0e8320 T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))`
- **T1** `| **unités sémantiques** | les spans candidats à la RSN et la fraction du texte | **55,4 %** du texte en moyenne |`
- **T1** `1,67 %** (graine 0, 239 cibles). L'audit v10 publie un contrôle plus dur — un **candidat`
- **T1** `aléatoire** dans les listes donne **42,14 %** de top-1 — et la **permutation des cibles**`
- **T1** `**1,997/220 = 0,908 %** ; les deux donnent p = 0. Un chiffre sans sa contre-épreuve n'est pas un`
- **T1** `attachement 99,46 %). Les chiffres de la fiche v12 (0,6511/0,6482, 235/236) sont **datés** : ils`
- **T1** `langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
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
- **T1** `**Lecture.** Le porteur `REL [22:42]` est le **rang 2** d'un groupe de **3** segments ; ses deux`
- **T1** `alternatives sont au rang 1 (la REL longue `[22:54]`, qui le **contient** : `inclus`) et au rang 3`
- **T1** `fidélité    : exacte 1.0000 · caractères 1.0000 · couverture 100.00%`
- **T1** `mots        : exacte 0.0000 · caractères 0.9286 · couverture 84.62%`
- **T1** `pos         : exacte 0.0000 · caractères 0.9286 · couverture 84.62%`
- **T1** `**88,91 %**, F1 **79,06 %**, attachement **99,46 %**. Sans lui, `evaluer` publie la ligne`
- **T1** `langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `| **cache du chunker** | **×138,7** à 160 répétitions (9 817,7 → 70,8 ms) | banc de texte **répété**, chemin chunker |`
- **T1** `| **cache, chemin par défaut** | ×5,8 à 20 répétitions, puis **×1,0** à 80 et 160 | S domine le coût |`
- **T1** `| **cache, corpus réel** | **×1,2** | phrases réelles, 6,1 tokens/phrase |`
- **T1** `**Ce que le ×139 veut dire — et ne veut pas dire.** C'est la suppression du **O(n²)** du chunker`
- **T1** `réel, le gain est **×1,2** ; sur le chemin par défaut, **×1,0** à 80 et 160 répétitions. Annoncer`
- **T1** `« ×139 plus rapide » sans la condition serait faux. Ce que le cache garantit, c'est que les`
- **T1** `SYNTAGMES   F1 78.82 %  (P 78.18 % / R 79.46 %)`
- **T1** `tête      F1 90.25 %  (P 92.34 % / R 88.26 %)`
- **T1** `**86,25 % à 95,75 %** (**+9,5 pts**) ; sur le réel 452, de **88,91 % à 95,00 %** (**+6,1**).`
- **T1** `**1,67 %** ; l'audit v10 ajoute un **candidat aléatoire** dans les listes (**42,14 %** de top-1)`
- **T1** `et une **permutation des cibles** (**0,908 %**). La mesure est **in-sample** : les règles ont`
- **T1** `base réelle 452, **183/184 (99,46 %)**. Détail : [`rapport-g017.md`](../../reports/rapport-g017.md).`
- **T1** `| **la performance du cache** (×139, conditions) | [`reports/rapport-cache-chunker-applique.md`](../../reports/rapport-cache-chunker-applique.md) |`
- **T1** `docs/archive/cerveau-facultes.md:23:| **réflexes** | chemin court **entraîné** (LoRA couches basses + lecteur de sortie) | **÷1,47** (m32) et **÷1,24** (m20) à 8 couches, lus par le moteur | 0,07 % de`
- **T1** `docs/archive/cerveau-facultes.md:39:| **motricité / effecteurs** | `--sortie F` + réflexes ; le moteur **écrit** ce que le réflexe produit | le signal **courant** est dans la sortie (R² 0,992) ; le ré`
- **T1** `docs/archive/etat-cerveau.md:53:| **C7** | consolidation · **+ sélection par ÉTALEMENT (15/10, tempérée)** | ✅ **fait, et désormais mesurée DANS LES POIDS (14/10)** | l'**exemplaire** bat la **moyenne`
- **T1** `docs/archive/plan-mla-vision.md:666:projecteur : 64 groupes × 3584 valeurs, |sortie| = 515.8354`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:123:| A7.2 | **Une couche exécutée ailleurs** : la même sortie, un autre nœud | ✅ | le **relais ne change pas un chiffre** (`porte-topologie`, 92 s, 42.5477) `
- **T1** `docs/archive/roadmap-native-2026-10-29.md:54:| N0.9 | **Cache KV natif** | ✅ **parité** — sortie identique à Python, 53 octets en **592,6 ms** |`
- **T1** `docs/pilotage/manques.md:73:| **N5** | **mémoire d'un signal injecté** — le modèle n'en a aucune, **et il ne l'APPREND pas** | sonde linéaire **et** non linéaire sur l'état de sortie : le signal **cou`
- **T1** `docs/pilotage/backlog/N3-operations-natives.md:40:**Mesuré et couvert** — la **sortie précoce** (**−24,05 %** de temps pour **−1,61** point de`
- **T1** `docs/pilotage/roadmap.md:329:2. **Le saut de calcul existe, le saut de contenu n'existe pas.** La sortie précoce gagne **24,05 %** de temps en`
- **T1** `docs/theorie/glossaire/entrees/accumulateur.md:4:> **Fiche glossaire — Accumulateur.** Vecteur de sortie dans lequel le mode « push » disperse les contributions : `acc[destination] += valeur × poids`.`
- **T1** `docs/theorie/glossaire/index.json:906:      "resume": "Vecteur de sortie dans lequel le mode « push » disperse les contributions : `acc[destination] += valeur × poids`. Sa taille décide de tout : 4 09`
- **T1** `docs/theorie/synthese/07-modeles-alternatifs-entree-sortie.md:100:sortie : embeddings, tête, adaptateurs), **routés par segment** et **chargés à la demande** (5 ms / 530 Ko). C'est`
- **T1** `docs/implantation/convertisseur.md:283:| tête de sortie (Q8_0, 579 M poids) | 23 | 27 Go/s |`
- **T1** `docs/implantation/contexte-long.md:389:inchangés). Le poste « tête de sortie » du profil en lot tombe de 5,5 ms/jeton à`
- **T1** `docs/implantation/moteur-de-pensee.md:223:| **T51** | la fiabilité qui dérive est-elle suivie ? | 10 % puis 40 % : v final 0,56, 20/20, 8,0 pas | la fenêtre glissante suit la dérive |`
- **T1** `docs/implantation/moteur-de-pensee.md:225:| **T53** | la dérive continue est-elle suivie ? | 5 % → 50 % : v final 0,5, 20/20, 8,6 pas | le glissement se paie en pas |`
- **T1** `docs/implantation/moteur-de-pensee.md:226:| **T54** | la rupture est-elle absorbée ? | 90 % d'erreur : v final 0,12, 20/20, 8,0 pas | le filtre inverse l'observation |`
- **T1** `docs/produit/exemples.md:216:  JSON complet) ; la sortie lisible donne **2 unités**, soit **61,5 %** du texte.`
- **T1** `reports/rapport-optimisations.md:5:sorties, **4 303 745 événements** (ternaire issu des signes réels, densité 100 %).`
- **T1** `reports/rapport-capteur-hebbien.md:121:# trace hebbienne de la couche 12, 10 % des sorties, sur 1025 tokens réels`
- **T1** `reports/rapport-empreinte-memoire.md:463:| tête de sortie (129 280 × 5120, F16) | **1,32 Go — 36 % du trafic** |`
- **T1** `reports/rapport-architecture-memoire.md:30:| tête de sortie | 1,32 | Q4_K | **oui** | 63,2 ms | **15,5 ms** |`
- **T1** `reports/rapport-tete-restreinte.md:106:| restriction simple | **change la sortie** | +10 à +15 % | génération contrainte assumée |`
- **T1** `reports/rapport-portes-p0-p9.md:31:| **P9** — noyaux natifs | `matvec_f32` parallèle par lignes : **×9,34** sur l'attention de V4.1, **bit à bit identique** (2 544 vides comparés, 0 écart) ; déquantif`
- **T1** `reports/rapport-cache-experts-vram.md:20:| tête de sortie | 1,30 | 1,5 % |`
- **T1** `docs/pilotage/chantiers.md:84:| **B — l'intelligence** | le sens, la logique, les jeux, les maîtres : que sait faire le système ? | ✅ B1–B12 ; B10.3 bloqué (encodeur) ; **B13** state store v0 + DRVF +`
- **T1** `docs/pilotage/roadmap.md:201:   suivante, jamais l'attente. **N5 est gelé** jusqu'au verdict de R11 sur le contexte ; B10.3 attend un **z qui porte** : l'objectif mot a levé le décodeur (32,5 ; **26,7`
- **T1** `> `agent` / `chat`, et `evaluer` **81,88 %** / **88,70 %** au lieu de **79,02 %** / **99,58 %**.`
- **T1** `| `drave evaluer` | `/tmp/qs-doc/drave` | **0** | **86,25 %** | **81,88 %** | **88,70 %** |`
- **T1** `La sortie complète (612 phrases, 239 cibles, base réelle 452, contrôle négatif **1,67 %**) est`
- **T1** `dans le document (§ 3.3). Le contrôle négatif est **1,67 %** dans les deux configurations : il`
- **T1** `f"({a.fraction_semantique:.1%} du texte)")`
- **T1** `# T4 — la performance de `drave analyser` : 10 000 mots en 4,0 s, 126 Mio, 14,8 Mo de JSON ; le contrôle de linéarité **échoue** (α = 1,55)`
- **T1** `> fonction, 2 493 mots/s, 126 Mio de pic RSS, 14,8 Mo de JSON) ; ❌ **le contrôle négatif de`
- **T1** `> quadratique explique **R² 0,99995** contre **0,957** pour le linéaire. Le coupable est`
- **T1** `> **2 014 mots/s** (CLI), **128 972 Ko** de pic RSS (126 Mio ; 167,6 Mio pour le CLI),`
- **T1** `> Sur **100 phrases courtes** (661 mots, médiane 6 mots) : **1,10 ms/appel** pour la`
- **T1** `> fonction, **1,18 ms** de coût fixe, **191,6 ms/appel** pour le CLI (démarrage compris),`
- **T1** `> et **0,369 s** pour les 100 en un seul `--jsonl` (×52,6 vs 100 CLI). Avec `--tagger` et`
- **T1** `> soit **×299** le lot heuristique ; l'extrapolation aux 10 000 mots donne **797 appels**,`
- **T1** `"stdout": "drave 0.1.0 — analyse heuristique (CPU, hors ligne)\nlangue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)\nPOS  Le/DET chat/NOUN dort/VERB ./PONC`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/r`
- **T1** `38:**État au 15/11.** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact`
- **T1** `296:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes`
- **T1** `371:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `| `session-` | 2026-11-15 11:05 | 1.1 Mo | 226 Ko | 1 | 186 | 230 | 1 | 0 |`
- **T1** `| `session-` | 2026-11-14 05:43 | 0.7 Mo | 147 Ko | 1 | 121 | 138 | 1 | 0 |`
- **T1** `| `session-` | 2026-11-15 12:40 | 0.7 Mo | 113 Ko | 1 | 97 | 102 | 0 | 0 |`
- **T1** `-| `session-` | 2026-11-15 22:35 | 1.0 Mo | 173 Ko | 1 | 146 | 174 | 1 | 0 |`
- **T1** `+| `session-` | 2026-11-15 22:35 | 1.0 Mo | 179 Ko | 1 | 148 | 177 | 1 | 0 |`
- **T1** `| `session-` | 2026-11-14 03:46 | 0.7 Mo | 134 Ko | 1 | 81 | 114 | 1 | 0 |`
- **T1** `| `session-` | 2026-11-14 03:18 | 0.7 Mo | 162 Ko | 1 | 131 | 155 | 2 | 0 |`
- **T1** `| `session-` | 2026-11-15 02:15 | 0.7 Mo | 160 Ko | 1 | 92 | 156 | 3 | 0 |`
- **T1** `| `session-` | 2026-11-14 01:48 | 0.7 Mo | 148 Ko | 1 | 128 | 154 | 3 | 0 |`
- **T1** `| `session-` | 2026-11-07 10:48 | 0.0 Mo | 12 Ko | 1 | 5 | 0 | 0 | 0 |`
- **T1** `| `session-` | 2026-11-15 12:05 | 0.7 Mo | 153 Ko | 1 | 115 | 136 | 1 | 0 |`
- **T1** `+| `session-` | 2026-11-15 23:16 | 0.1 Mo | 45 Ko | 1 | 16 | 23 | 0 | 0 |`
- **T1** `-Total : 373.8 Mo de traces brutes.`
- **T1** `+Total : 374.0 Mo de traces brutes.`
- **T1** `| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |`
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |`
- **T1** `reports/rapport-n4-porte-execution.md:52:| matrice de mauvaise taille, ou fichier absent | refus, code **2** | code **2** (65536 octets pour 896×896) |`
- **T1** `[still running after 60000ms; moved to background job bash-93]`
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `-**État au 15/11.** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 2`
- **T1** `+**État au 15/11.** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 2`
- **T1** `[still running after 60000ms; moved to background job bash-106]`
- **T1** `9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS`
- **T1** ``analyser` rend `objet` / `—` au lieu de `agent` / `chat`, et `evaluer` **81,88 %** / **88,70 %**`
- **T1** `au lieu de **79,02 %** / **99,58 %**. Le document affiche la sortie réelle du clone et nomme`

## 6. Commits

- T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS"

