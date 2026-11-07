# Inventaire Panini — état daté du 7 novembre 2026

> **Mission.** Inventaire complet et daté des 14 dépôts de l'écosystème Panini pour préparer le
> chantier autonome d'une semaine d'intégration avec Drave (`../Qtrinet/`, 7 → 14/11/2026).
> **Lecture seule** : aucun commit, aucun fichier de code, de doc ou de configuration modifié,
> `git status` lancé avec `--no-optional-locks`. Un seul effet de bord, documenté au §5.7 : un
> `sqlite3` de lecture a checkpointé le WAL d'une base de corpus. Les deux seuls fichiers écrits sont ce rapport et son JSON.
>
> **Méthode.** `git log` / `status` / `submodule status`, lecture des README, docs et journaux de
> bord, comptages (`find`, `du`, `wc`), lecture directe des artefacts JSON. **Aucune suite de tests
> n'a été exécutée** : les leurs coûtent de 45 min à 3 h 30. Les chiffres cités sont ceux que
> Panini **publie**, avec leur date et leur chemin — ils sont repris, pas re-mesurés.

---

## 0. Ce qu'il faut retenir

1. **Un seul dépôt est vivant au sens fort : `Panini/research`** (= `Panini-Research`, qui est un
   lien symbolique vers lui). 1 622 commits, dernier le **25/10/2026**, 182 194 lignes de Python,
   50 124 lignes de noyau formel. L'hôte `Panini` est un conteneur de sous-modules, actif jusqu'au
   **22/10/2026**.
2. **Sept des treize autres dépôts sont des échafaudages** : LICENSE + README de 1 à 4 lignes +
   templates GitHub. Seuls `Panini-FS` (Rust, 581 fichiers), `OntoWave` (TypeScript, 81 fichiers,
   sous-module sans clone standalone) et `ExecutionOrchestrator` (CLI + 3 drivers) ont du code.
3. **La surface partageable est réelle et déjà à moitié chez Drave** : corpus UDHR (532 langues
   côté Panini ; 456 langues × 30 articles + Glottolog côté Drave, **même source XML**), signatures
   14 atomes en JSON pur, corpus d'or CIC portable (42 verdicts).
4. **Un seul lien documenté côté Panini, et il pointe vers un fichier absent** : le §6 du
   `README.md` renvoie à `Qtrinet/docs/agent/panini-nipada.md`, qui n'existe pas ; le document réel
   est `Qtrinet/docs/methode/panini-nipada.md`. Dans `Panini/research/`, « Drave » n'apparaît
   **nulle part** (0 occurrence vérifiée).
5. **Trois vocabulaires à ne pas confondre** : 14 atomes + 9 dhātus (Research, référence) ; 7 dhātu
   + 34 atomes (Panini-FS, ligne divergente) ; 9 dhātu (ancien `docs/` de l'hôte). Une table
   atomes ↔ niveaux Drave doit se fonder **uniquement** sur V14 de Research.

---

## 1. État des 14 dépôts

| Dépôt | Branche | Dernier commit | Date | Propre | Taille | Suivis | Ce que c'est |
|---|---|---|---|---|---|---|---|
| **Panini** (hôte) | main | `9b80c32` docs(readme) : réécriture complète — état réel, 7 axes, lien Drave | 2026-10-22 22:16 | **non** : 23 lignes (16 M, 7 ??) | **34 G** (dont `research` 25 G, `modules` 1,7 G) | 4 645 | hôte : sous-modules + docs + ouvrage |
| **Panini-Research** | HEAD détachée | `e10d695` docs(incident) : la classe vue depuis les KITS | 2026-10-25 09:45 | **non** : 36 M + 545 971 ?? | **25 G** | 74 708 | **le laboratoire** : noyau + NIPADA |
| **Panini-FS** | master | `b90d3bd` test(e2e) : accept live modules docs title variant | 2026-04-13 | oui (0) | 1,7 G (modules, FS inclus) | 697 (local) / 581 (pin) | FS sémantique Rust + déploiements |
| **Panini-SemanticCore** | main | `6ba7b8b` chore(templates) | 2025-09-06 | oui | 40 K | 9 | échafaudage |
| **Panini-AttributionRegistry** | main | `ad635ad` chore(templates) | 2025-09-06 | oui | 36 K | 9 | échafaudage |
| **Panini-AutonomousMissions** | main | `c85a240` chore(templates) | 2025-09-06 | oui | 40 K | 9 | échafaudage (fusion annoncée dans Execution) |
| **Panini-CloudOrchestrator** | main | `e3baee3` docs(migration) Option B | 2025-08-30 | oui | 20 K | 4 | échafaudage (fusion annoncée) |
| **Panini-CoLabController** | main | `87f6dde` docs: bump — ressources cloud | 2025-11-12 | oui | 28 K | 5 | README de 227 lignes, **aucun code** |
| **Panini-CopilotageShared** | main | `270f197` feat: copilotage rules | 2025-09-07 | oui | 44 K | 11 | règles + workflows CI |
| **Panini-DatasetsIngestion** | main | `23ed336` chore(templates) | 2025-09-06 | oui | 36 K | 9 | échafaudage |
| **Panini-ExecutionOrchestrator** | main | `08fa790` chore(templates) | 2025-09-06 | oui | 68 K | 17 | squelette CLI + 3 drivers + mission echo |
| **Panini-PublicationEngine** | main | `65462cf` chore(templates) | 2025-09-06 | oui | 40 K | 9 | échafaudage |
| **Panini-SpecKit-Shared** | main | `e965fcf` Initial Commit v1.0.0 | 2025-10-02 | oui | 164 K | 23 | constitutions, règles, templates |
| **Panini-UltraReactive** | main | `8fb776b` chore(templates) | 2025-09-06 | oui | 40 K | 9 | échafaudage (renommé MonitoringWatchdog) |

### 1.1 Deux états pour un même dépôt — le piège de lecture

Les clones `../Panini-*` et les **pins de sous-modules** dans `Panini/modules/` ne sont pas au même
point :

- **Les clones standalone sont gelés** : dernier `fetch` entre septembre 2025 et avril 2026. Le
  `Panini-FS` local est à `b90d3bd` (13/04/2026, 332 commits) alors que `origin/master` porte déjà
  `9588bd5` (08/09/2026, **472 commits**, +140), commit que le clone **ne possède même pas**.
- **Les pins sont plus récents** : les 12 pins de `Panini/modules/*` datent tous du **2026-09-08**
  (commit « docs(arch) : bloc-pointeur court »), et `research` est pinné à `6f8b67b` alors que le
  checkout est à `e10d695` (**+193 commits non pointés** dans l'index de l'hôte, du 19 au 25/10).
- **Conséquence pratique** : lire `../Panini-FS` donne un état vieux de sept mois. Pour l'état
  vivant, lire `Panini/modules/core/filesystem` (pin 08/09/2026) — ou rafraîchir le clone, ce que
  la lecture seule interdit ici.

### 1.2 Propreté : ce que « non propre » veut dire

- **Panini (hôte)** : 16 `M` (14 sous-modules + `docs/index.md` + `.github/copilot-instructions.md`)
  et 7 `??` — dont **`CONTEXTE-IA.md` et `PHILOSOPHIE.md`, les deux documents normatifs** du dépôt,
  et **`docs/ouvrage/`**, l'ouvrage de référence (~40 fichiers). Les documents qui font autorité ne
  sont donc **pas committés**.
- **Panini-Research** : 36 fichiers suivis modifiés (dont `src/nipada/formalkernel/reels.py`,
  `src/nipada/compute/dhatu_token_program.py`), plus **545 971 fichiers non suivis** — `nipada/encyclopedia` (8,1 G,
  568 441 fichiers) et `nipada/corpus/_cache/wikipedia_dump` (2,6 G, 151 191 fichiers). Aucune
  perte : ce sont des données de travail, mais un `git clean` ou un vidage de disque les emporte.

---

## 2. Les dépôts, un par un

### 2.1 `Panini/` — l'hôte (le plus détaillé)

**Ce qu'il fait.** Dépôt conteneur : le laboratoire (`research/`), les composants d'infrastructure
(`modules/`, 13 sous-modules) et la documentation d'écosystème. Son `src/` propre est modeste
(`panini_engine` : `analyzer_server`, `github_connector`, `registry_writer`, `colab_client` ;
`cloud/api_rest.py` ; `github_sync/`), et ses **7 tests** (`tests/test_analyzer_server.py`,
`test_github_connector.py`, `test_git_registry.py`, `test_imports.py`, `test_oauth_manager.py`,
`test_registry_writer_integration.py`) ne couvrent que cette plomberie.

**Documents clés.**

| Document | Rôle | État |
|---|---|---|
| `README.md` (199 l.) | **la référence des 7 axes** et du lien Drave (§6) | réécrit le 22/10/2026, propre |
| `CONTEXTE-IA.md` (384 l.) | contexte **normatif** (prime sur tout) | **non committé** |
| `PHILOSOPHIE.md` (240 l.) | finalité | **non committé** |
| `docs/index.md` | index de la documentation | modifié, non committé |
| `docs/ARCHITECTURE_REAL_6PROJECTS.md`, `PROJECT_RESPONSIBILITY_MATRIX.md` | architecture et frontières | 2025, partiellement périmé |
| `docs/ouvrage/` | *Panini, théories d'un projet (2025-2026)* : histoire reconstruite depuis 172 journaux (266 375 lignes) | **non committé**, ~40 fichiers |
| `docs/journal-de-bord/` | 35 fichiers, 126 367 lignes ; dernier `2026-09-08.md` | vivant jusqu'au 08/09 |
| `.github/copilot-instructions.md` | routage opérationnel + les 4 projets | modifié |

**Ce qui est ouvert.**

- **Rattrapage documentaire** : l'ouvrage, le contexte normatif et la philosophie attendent un
  commit ; `docs/index.md` et `copilot-instructions.md` sont modifiés sans commit.
- **Bump du pointeur `research`** : `6f8b67b` (19/10) → `e10d695` (25/10), **193 commits**, dont
  les 23 lemmes du 24 et les 13 du 25/10.
- **Docs 2025 périmées à trancher** : `ROADMAP_PHASED_4PHASES.md` (janvier 2026, Panini-FS +
  Pensine-Web, jamais exécutée), `ETAT-TRIANGLE-RECHERCHE.md` (maturités 70/45 %, septembre 2025),
  `ROADMAP-RECHERCHE.md` (9 dhātu, obsolète face à V14).
- **Pas de porte** : un seul workflow CI (`async_compression.yml`), aucun script de vérification
  d'écosystème.

**Comment ils vérifient.** Pas au niveau de l'hôte : la vérification est déléguée au sous-module
`research` (voir 2.2). Le journal du 08/09/2026 enregistre la seule porte d'ensemble : « G1-G4
vertes — 722 tests, DTP 48/48, R² = 0,909139 reproduit ».

**Chiffres publiés (avec source).** 722 tests passés, 1 sauté (`research/README.md`, 08/09/2026) ;
DTP 48/48 = 0 % WER ; R² = 0,909139 sur 655 paires et 114 textes (`nipada/falsification/
pairs334_axes_v1.json`) ; R² reproduit à 0,907849 sur 648 paires, écart de 7 paires documenté
(`GATES_G1_G3_REPORT_2026-09-07.md`).

**Lien Drave.** Un seul endroit : `README.md` §6 (table « ce que Panini apporte / ce que Drave
apporte en retour »), plus la citation de `Qtrinet/docs/agent/panini-nipada.md` — **chemin cassé**.
Aucune donnée produite par l'hôte n'est destinée à Drave ; `corpus/protoatheism` (36 M, 42 œuvres)
est un **plan d'acquisition** : la plupart des dossiers contiennent un `STATUS_PENDING.txt`, pas un
texte.

**Données partageables.** `corpus/protoatheism_tokens/*.jsonl` (120 K, tokens par œuvre) ;
`data/` (78 M) = analyses dhātu de septembre 2025, à ne pas réutiliser sans vérification.

---

### 2.2 `Panini-Research/` — le laboratoire (le cœur)

**Ce qu'il fait.** Un système formel (CIC-lite en Python, noyau ℝ localisé par coupures de
Dedekind) et **NIPADA**, la couche descriptive qui décompose le texte en 14 atomes, le reconstruit
par DTP (0 % WER annoncé) et le stocke dans un graphe encyclopédique flou. Le dépôt porte aussi les
corpus, les lexiques, la généalogie des langues et la théorie — 74 708 fichiers suivis, 182 194
lignes de Python.

**Documents clés.**

| Document | Rôle |
|---|---|
| `README.md` | architecture à deux niveaux, loi H₀, état au 08/09/2026 |
| `AGENTS.md` (47 l.) | routage par tâche (noyau / produit / journal / reprise) |
| `docs/noyau/J4_CATALOGUE.md` | **catalogue des théorèmes vérifiés de ℝ_loc** (état 20/10/2026) |
| `docs/noyau/CHANTIERS.md` | **statut unique des chantiers C1-C8** (21/10/2026) |
| `docs/noyau/VALIDATIONS.md` | historique des runs (durées, commits, échecs) |
| `docs/noyau/DIRECTIVE_NOYAU.md`, `J4_PASSATION.md` | méthode et passation |
| `docs/ARCHITECTURE_NOYAU_NIPADA_v2.0.md`, `philosophy-theory/DOCUMENT_DE_CONTEXTE_v3.0.md` | sources uniques du vocabulaire |
| `docs/NIPADA_SESSION_*_FINAL_REPORT.md` | rapports de session (§476-481, juin 2026) |
| `NIPADA_BACKLOG.md` | backlog P0 (redressement du pipeline, 14/07/2026) |
| `docs/journal-de-bord/` | 81 fichiers, 50 902 lignes ; dernier `2026-10-25.md` |
| `docs/ouvrage/` (dans l'hôte) | l'histoire longue, reconstruite |

**Ce qui est ouvert.**

- **Noyau (J4)** : C4d (lois algébriques du produit) et C5 (inverse) sont avancés ; **C6
  (continuité ε-δ) est en cours** ; **C7 (complétude métrique / compacité) et C8 (catalogues) sont
  `TODO`**. Le dernier journal (25/10) annonce `mul_cut_located` / `c6j` « en cours » : la clôture
  de ℝ_loc par le **produit** manque encore. Après quoi ℝ_loc sera clos par `+`, `−`, `|·|`,
  inverse et produit.
- **NIPADA produit** : le backlog du 14/07/2026 est explicite — **P0 « restaurer ce qui marchait le
  3 juillet »**, phases A1-A4 et R1-R4 **toutes « À faire »** (benchmark 20 textes, diagnostic des
  **54 tests cassés**, réparation des imports `compiler/` vs `compute/`, retour de DTP et du beam
  search). Les règles anti-dérive gèlent toute nouveauté tant que ce n'est pas réparé.
- **Dette de vérification** : deux audits d'intégrité (18-19/10/2026) concluent « dépôt sain » mais
  signalent les travaux non commités volumineux.
- **Asymétrie de rythme** : le noyau avance la nuit (23 lemmes le 24/10, 13 le 25/10) ; le produit
  est arrêté depuis juillet. **C'est le noyau, pas NIPADA, qui est le visage mûr du dépôt.**

**Comment ils vérifient (les 4 portes, et le noyau à 4 niveaux).**

| Porte | Commande | Résultat publié |
|---|---|---|
| **G1** environnement | `pytest tests/` | 589 passed (07/09), puis **722 passed / 1 skipped** (08/09) |
| **G2** DTP | `python -m nipada.benchmark` | **48/48 = 100 % identité, 0 % WER** ; `genre_accuracy` 0,25 |
| **G3** calibrage R² | script §334 | 0,907849/648 reproduit vs 0,909139/655 officiel (écart documenté) |
| **G4** hold-out | `nipada/falsification/nipada_holdout_v1.json` | 23/114 textes vierges, gelé |

Et pour le noyau seul, **quatre niveaux** : kit (secondes-minutes) → chaîne ℝ réelle (10-40 min) →
validation lourde (1-3 h) → **audit global des constantes** (`scripts/noyau/audit_consts.py
--toutes`), qui exige « aucune manquante » (dernier : 296 defs, 412 consts, 25/10). Les tests
formels complets : **339 passés / 16 sautés / 0 échec en 47 min** (audit du 19/10).

**Chiffres publiés.** 722 tests ; DTP 48/48 ; R² 0,909139 (655 paires, 114 textes, α = 0,67, graphe
v35 : 1 753 nœuds, 19 951 arêtes) ; graphe encyclopédique 15 881 nœuds / 43 931 liens ; cache de
noyau ×10 000 (52 s → 5 ms ; noyau ℝ 1 h 23 → 0,23 s) ; tactique ℚ ×180-190 ; 15 langues
différenciées.

**Lien Drave.** **Aucun dans les fichiers** — 0 occurrence de « Drave » ou « Qtrinet » dans
`research/`. Le lien n'existe que par la théorie (14 atomes, généalogie) et par les données
(UDHR, signatures). Les avertissements que Drave a déjà recopiés (β époque/généalogie) viennent de
`nipada/falsification/nipada_v150_validation.json`.

**Données partageables.** Voir §3.4-3.5 : UDHR 532 langues, signatures 14 dim, corpus d'or CIC,
généalogie `LANG_TREE`, lexiques V14, API REST.

---

### 2.3 `Panini-FS/` — le FS sémantique (ligne divergente)

**Ce qu'il fait.** Écosystème de « compression sémantique universelle » : un FS en Rust (RocksDB,
Tantivy, FUSE3) qui décompose les contenus en dhātu et les recompose, plus une couche
d'exploitation (Colab, déploiements, doctors, site de docs). **Vocabulaire propre : 7 dhātu
(COMM, ITER, TRANS, DECIDE, LOCATE, GROUP, SEQ) et 34 atomes** — ni les 9 dhātus ni les 14 atomes
de Research.

**Documents clés.** `README.md` (159 l., écosystème en 7 dossiers), `docs/avancement.md` (résultats
de février 2026), `docs/dhatu-framework.md` (7 dhātu + 34 atomes), `docs/vision.md`,
`docs/publications.md`, `docs/livre/`, `e2e/`.

**Ce qui est ouvert.** Le dépôt est un **chantier d'exploitation** (build Rust, e2e Playwright,
déploiements) arrêté au 08/09/2026 ; le clone local est en retard de 140 commits. Aucune mention de
Drave.

**Chiffres publiés (02/2026, `docs/avancement.md`).** 34 atomes validés sur 14 langues ; 7/7
langues européennes ≥ 90 % de couverture (anglais 94,4 %, français 90,1 %) ; Gutenberg 62 textes
~3 M mots ; Wikipédia 973 articles, 2,2 M mots ; couverture globale 76,8 % sur ~8 M mots ; Dolt
~215 Mo ; PaniniWeb Rust v0.1 (4 crates, 71 tests).

**Pour Drave.** Rien de directement réutilisable **sauf** comme précédent : c'est la seule ligne du
projet qui a mesuré une couverture lexicale multilingue à grande échelle. Ses 7 dhātu / 34 atomes
ne doivent pas entrer dans la table J2.

---

### 2.4 Les onze modules d'infrastructure

| Module | Fichiers | Contenu réel | Verdict |
|---|---|---|---|
| `ExecutionOrchestrator` | 21 | `cli.py`, `drivers/{local,colab,cloud}.py`, `missions/echo.py`, README avec roadmap | **seul squelette exécutable** |
| `SpecKit-Shared` | 23-27 | `constitutions/panini-universal-constitution.md`, `rules/*.yml`, `templates/`, `.specify/` | outillage de spec, utilisable tel quel |
| `CopilotageShared` | 11 | `config.yml`, `rules/`, `workflows/ci-standard.yml` | conventions |
| `DatasetsIngestion` | 13 (pin) | `pyproject.toml`, LICENSE, README 1 ligne | **vide** |
| `CoLabController` | 5-9 | README 227 l. (stratégie Colab Pro : T4/P100/V100/A100, sessions 24 h), 1 journal | **doc seule** |
| `SemanticCore`, `AttributionRegistry`, `AutonomousMissions`, `CloudOrchestrator`, `PublicationEngine`, `UltraReactive` | 4-9 | LICENSE + README 1-4 l. + templates GitHub + CI | **échafaudages** |

Deux notes de migration (30/08/2025) annoncent la fusion d'`AutonomousMissions` et de
`CloudOrchestrator` dans `ExecutionOrchestrator` ; `UltraReactive` est renommé fonctionnellement
`MonitoringWatchdog`. **Rien de tout cela n'est advenu** — les dépôts sont restés des coquilles.

### 2.5 Deux sous-modules hors liste, à connaître

- **`modules/ontowave/`** (`Panini/modules/ontowave`, pin 08/09/2026) : 81 fichiers TypeScript/Vue,
  visualisation ontologique, `package.json`, `tests/`. C'est le seul composant « produit » vivant
  hors Research.
- **`copilotage/`** : journal d'agents (`JOURNAL_AUTO_*`), dernier commit 19/05/2026 ; à ne jamais
  déplacer (règle du dépôt).

---

## 3. Synthèse

### 3.1 Les 7 axes de recherche

Source : `Panini/README.md` §2 (réécrit le 22/10/2026). Les états sont ceux du README.

| # | Axe | Objet | Où | État déclaré |
|---|---|---|---|---|
| 1 | **Noyau formel (J4)** | ℝ localisé : ordre, corps, distance, complétude | `research/src/nipada/formalkernel/` | **actif** — ~35 400 l. (50 124 mesurées), théorèmes vérifiés |
| 2 | **NIPADA** | moteur de sémantique computationnelle (graphe, dhātus, DTP) | `research/src/nipada/` | **actif** (produit, pipeline arrêté depuis juillet) |
| 3 | **Linguistique** | 14 atomes (V14), universaux, généalogie des langues | `research/philosophy-theory/`, `research/data/` | **actif** |
| 4 | **Corpus & ingestion** | Gutenberg, UDHR, Wikipédia — multilingue | `research/data/`, `corpus/` | **actif** |
| 5 | **Philosophie & théorie** | épistémologie du noyau, Ł3, cadres théoriques | `research/philosophy-theory/` | **actif** |
| 6 | **Moteur d'inférence (Drave)** | flots de données, AER, modèles décomposables | `../Qtrinet/` | **actif, projet lié** |
| 7 | **Infrastructure** | colab/cloud, FPGA, attribution, visualisation (OntoWave) | `modules/`, `research/panini-fs/` | **selon chantier** |

Lecture critique : les axes 1 et 3 sont **réellement** actifs (commits quotidiens en octobre) ;
l'axe 2 est actif en code mais **bloqué en produit** (backlog P0) ; l'axe 4 est actif en ingestion
mais **non consolidé** (545 971 fichiers non suivis) ; l'axe 6 est **déclaré, pas instrumenté** ;
l'axe 7 est à l'arrêt depuis septembre.

### 3.2 Les 14 atomes sémantiques (V14)

**Où ils sont définis — six couches, une seule source de vérité.**

| Couche | Fichier | Forme |
|---|---|---|
| **Liste canonique (ordre)** | `research/src/nipada/core/hardware_mapping.py`, `V14_ATOMS` | `list[str]` de 14 noms |
| **Sémantique / prédictions** | `research/philosophy-theory/GRILLE_ABLATION_V14_v0.1.md` | table : atome, **nombre premier**, rôle, prédiction d'ablation |
| **Statut épistémique** | `research/philosophy-theory/DOCUMENT_DE_CONTEXTE_v3.0.md` | « vocabulaire **candidat révisable** », plus un dogme |
| **Lexiques** | `research/data/v14_lexicon_enriched.json` (3,9 Mo) | `{langue: {ATOME: [mots…]}}` |
| **Signatures** | `research/nipada/falsification/analytic_sigs_v1.json` | `{œuvre: {ATOME: fréquence}}` — **44 œuvres**, somme 1 |
| **Format d'échange** | `research/data/udhr_demo.nipada` (v0.3.0) | texte auto-portant : `§1: ∃ {iso:[eng:BEING, fra:ÊTRE]}…` |

**Les 14, avec leur symbole, leur premier et leur rôle** (source : grille d'ablation + `.nipada`) :

| # | Atome | Symbole | Premier | Rôle | Porteur ? (prédiction) |
|---|---|---|---|---|---|
| 1 | **ÊTRE** | ∃ | 2 | existence, substrat | témoin : retrait **catastrophique** |
| 2 | **DIFFÉRENCE** | ∆ | 3 | gradient entre états | témoin : casse |
| 3 | **RAPPORT** | ∼ | 5 | relation | témoin : casse |
| 4 | **ORIENTATION** | ↗ | 7 | direction du flux | témoin : dégrade (lien H₀) |
| 5 | **SUJET** | ⊙ | 11 | agent, expérienceur | porteur modéré |
| 6 | **TEMPS** | ⧖ | 13 | durée, séquence | porteur modéré |
| 7 | **MODALITÉ** | ◇ | 17 | possible / nécessaire (Ł3) | spéculatif |
| 8 | **NOMBRE** | № | 19 | quantité, cardinalité | faible (candidat au retrait) |
| 9 | **ESPACE** | ⊕ | 23 | localisation, métaphore | porteur modéré |
| 10 | **OPÉRATION** | ⊗ | 29 | action, acte (les dhātus ACT) | témoin : casse |
| 11 | **FONCTION** | λ | 31 | finalité, usage | spéculatif |
| 12 | **STRUCTURE** | ⊞ | 37 | organisation, agencement | porteur modéré |
| 13 | **SYMÉTRIE** | ≍ | 41 | symétrie, équilibre | **meilleur candidat au retrait** |
| 14 | **ÉQUATION** | ≡ | 43 | égalité, équivalence | faible en philo, fort en technique |

**Sont-ils utilisables par Drave ? Oui, à trois conditions.**

1. **En lecture directe** : `analytic_sigs_v1.json` est un `{texte: {14 flottants}}` pur, sans
   dépendance ; `v14_lexicon_enriched.json` est un dictionnaire par langue. Un script Drave peut
   les charger aujourd'hui.
2. **Par API** : `POST /decompose` renvoie `{text, lang, v14_signature: dict[str,float],
   active_atoms, dominant_atom, time_ms}` (`research/src/nipada/api/api.py`). FastAPI + un graphe de
   33-58 Mo à charger : **à tester avant de s'y engager**.
3. **Avec un avertissement** : la signature est **lexicale** (projection de mots sur des listes),
   donc **de surface** — c'est précisément ce que leur §150 mesure (β époque +0,138 vs filiation
   +0,049). Toute mesure Drave doit contrôler la date et la surface.

**Les 9 dhātus** (instructions, `hardware_mapping.DHATUS`) : `EXIST, TRANS, EVAL, LOCATE, FEEL,
ACT, QUAL, REL, KNOW`.

### 3.3 La généalogie des langues

**Où elle vit.**

| Pièce | Chemin | Forme | Volume |
|---|---|---|---|
| **Registre** | `research/src/nipada/signing/language_genealogy.py` | `LANG_TREE: dict[code, LangInfo]` — dataclass gelée `(code, family, branch, epoch, morphological_type, script, closest_kin, notes)` | **29 langues** |
| **Distance** | même fichier, `lang_distance(l1,l2)` | 0 même langue / 0,15 même branche / 0,40 même famille / 0,75 familles différentes / 1,00 inconnu | fonction |
| **Chaînes de transfert** | `research/src/nipada/compute/cross_lingual_projector.py` | `LANGUAGE_GENEALOGY_TREE` + projection X → ancêtre → V14 | projet |
| **Étiquettes de corpus** | `research/data/udhr_corpus.json` (532 langues) | `family`, `branch`, `tradition` par langue | 532 |
| **Généalogie réelle (Drave)** | `Qtrinet/data/udhr/genealogie.json` | `famille` + `branche` = **chemin de glottocodes** + `niveau` | **456 langues** |
| **Théorie** | `Qtrinet/docs/theorie/genealogie-des-langues.md` | les 6 niveaux (famille → traducteur) + l'avertissement | doc |

**Son état.** Le registre Panini est **petit mais propre** (29 langues, 7 familles : indo-européen,
ouralien, sémitique, sino-tibétain, japonique, coréen, turcique), avec époque et type morphologique
— utile pour *choisir un proxy*, pas pour *prouver une parenté*. La généalogie **réelle et
complète** est déjà chez Drave (Glottolog, 456 langues, chemins de glottocodes). **L'intégration
consiste donc à aligner deux représentations, pas à importer une théorie.**

**Ce que Panini a établi (et qui est déjà recopié chez Drave).** `nipada_v150_validation.json` :
OLS de la dissimilarité de signature sur `d_graph`, `dyear/1000 ans` et `same_tradition` →
**époque +0,1378**, **filiation +0,0489**, tradition +0,0022, R² = 0,3004. H1 (stratification) et H2
(LOOCV tradition) sont **KO**, H3 (régression) **OK**, et le go/no-go de la phase religieuse est
**NO-GO**. Autrement dit : *la signature de surface capte l'époque, pas la filiation* — et leur
propre test de parenté est un échec assumé.

**Ses corpus.** Le corpus §334 (114 textes actifs : 104 traditions + 10 références ; 655 paires ;
philosophie et religion, du brahmanisme au matérielisme grec) et, pour la généalogie comparée,
l'UDHR (532 langues, même article) et les 27 catalogues d'acquisition (`catalog_*_v206*.json`,
70 œuvres chacun ≈ 1 890 candidats par tradition et par époque). **Attention : l'axe comparé du
§334 est la tradition, pas la langue** — `lang_a` vaut `eng` 408 fois, est vide 245 fois et `fra`
2 fois ; les signatures V14 exportées couvrent **44 œuvres**.

### 3.4 Les corpus disponibles

| Corpus | Volume | Format | Langues | Où | Partageable ? |
|---|---|---|---|---|---|
| **UDHR, article 1** | 229 Ko, 532 langues | JSON `udhr-v2.0-xml` : `{name, iso, script, dir, text, family, branch, tradition}` | **532** | `research/data/udhr_corpus.json` (+ `udhr_decomposed_v14.json`, `udhr_convergence_v14.json`) | **oui, immédiatement** (déjà chez Drave : 456 langues × 30 articles) |
| **UDHR, 30 articles** | 28 Mo | XML `udhr_XXX.xml` + `langues.jsonl`, `genealogie.json`, `familles/*.jsonl` | 456 | `Qtrinet/data/udhr/` | déjà intégré côté Drave |
| **§334 (philosophie/religion)** | 114 textes actifs ; 102 fichiers `sources/` (9,5 Mo) ; signatures de 44 œuvres | `.txt` un fichier par œuvre + signatures JSON | surtout **anglais** (408 paires), 245 sans étiquette, 2 en français ; les œuvres grecques, arabes, sanskrites et chinoises sont comparées en traduction | `research/nipada/corpus/_cache/sources/`, `nipada/falsification/` | **oui** (textes du domaine public), avec la fiche `pairs334_axes_v1.json` |
| **Gutenberg** | 1 999 métadonnées ; **1 943 téléchargés** ; 332 fichiers (271 Mo) ; 5 curatés | SQLite `books(id,title,lang,authors,subjects,downloads,url,fetched)` + `.txt` | en, fr, de, es | `research/data/mass_ingestion/*.db`, `_cache/public_domain_auto/gutendex/`, `_cache/gutenberg_curated/` | oui (domaine public) |
| **Wikipédia** | **151 191 fichiers, 2,6 Go** + backlogs (en 20 935, de 18 740, fr 15 636) | un `.txt` par article | en, de, fr | `research/nipada/corpus/_cache/wikipedia_dump/` | oui, mais non suivi par git |
| **Textes sacrés / suttacentral / MIT Classics** | 21 Mo + 13 Mo + 2 Mo | `.txt` par section | pi, en, gr | `_cache/sacred_texts/`, `_cache/suttacentral/`, `_cache/mit_aristotle_*` | oui |
| **Protoathéisme (hôte)** | 36 Mo, 42 œuvres | dossiers + `STATUS_PENDING.txt` | en, fr, la… | `Panini/corpus/protoatheism/` | **non : acquisition inachevée** |
| **Tokens protoathéisme** | 120 Ko | JSONL | — | `Panini/corpus/protoatheism_tokens/` | oui |

**Formats de référence pour un corpus commun.**

- Le plus simple : **UDHR JSON** (`udhr_corpus.json`) — un texte parallèle identique dans 532
  langues, avec famille/branche/tradition. C'est le seul corpus où Panini et Drave ont **déjà** des
  données comparables, issues de la **même source** (`eric-muller/udhr`, fichiers `udhr_XXX.xml`).
- Le plus riche : **signatures §334** — `pairs334_axes_v1.json` donne, pour chaque paire,
  `d_topo`, `d_lex`, `d_H`, `cos`, `trad_*`, `lang_*` : une table prête pour un test de retrieval.
- Le plus « prêt à prouver » : **corpus d'or CIC** (`corpus_dor_cic_v1.json`, 46 Ko + TSV) : 3 defs,
  21 consts, **42 entrées** (36 `accepte`, 6 `rejette`), chacune avec preuve et type sérialisés en
  de Bruijn (hex) et une empreinte SHA-256. Sa doctrine : « toute implémentation doit reproduire
  exactement ces verdicts à partir de cet artefact seul ».

### 3.5 Interfaces et données partageables (ce que Drave peut consommer)

| Surface | Chemin | Format | Dépendances | Maturité |
|---|---|---|---|---|
| Signatures V14 par texte | `nipada/falsification/analytic_sigs_v1.json` | `{texte: {ATOME: float}}` | aucune | **haute** |
| Lexiques V14 | `data/v14_lexicon_enriched.json` (3,9 Mo) | `{lang: {ATOME: [mots]}}` | aucune | haute (qualité à vérifier) |
| Paires §334 | `nipada/falsification/pairs334_axes_v1.json` | 655 objets `{a,b,d_topo,d_lex,d_H,cos,trad,lang}` | aucune | **haute** |
| Corpus d'or CIC | `nipada/falsification/corpus_dor_cic_v1.{json,tsv}` | preuve/type hex + verdict + sha256 | aucune | **haute** |
| Généalogie | `src/nipada/signing/language_genealogy.py` | Python (dataclass) | `nipada` | moyenne (export JSON à faire) |
| API REST | `src/nipada/api/api.py`, `server.py` | FastAPI : `/decompose`, `/reconstruct`, `/roundtrip`, `/compare`, `/atoms`, `/dhatus`, `/benchmark`, `/search`, `/hypotheses`, `/api/v1/*` | fastapi + graphe 33-58 Mo | **moyenne (non testée ici)** |
| Format `.nipada` | `data/udhr_demo.nipada` (v0.3.0) | texte auto-portant | aucune | moyenne (spec incomplète) |

### 3.6 Prêt à intégrer dans la semaine vs trop immature

**Prêt (données existantes, format stable, aucune dépendance lourde).**

1. **Alignement UDHR** : 532 langues (Panini, art. 1) contre 456 (Drave, 30 articles) + Glottolog.
   Livrable : table de correspondance des codes et des familles, échantillon commun, mesure de
   recouvrement. *Risque faible, tout est déjà sur disque.*
2. **Signatures 14 atomes** : **44 œuvres** × 14 flottants (somme 1), en JSON pur. Livrable : table
   atomes ↔ niveaux Drave + 20 exemples mesurés (le J2 du plan de semaine).
3. **Corpus d'or CIC** : 42 verdicts portables. Livrable : un vérificateur indépendant côté Drave
   (ou un simple rejeu) et le taux d'accord. *Le contrôle négatif est inclus : altérer un octet
   doit produire un rejet.*
4. **Généalogie comparée** : `LANG_TREE` (29 langues) + `genealogie.json` (456) + l'avertissement
   β. Livrable : la fiche à deux faces du J3.

**Trop immature (ne pas engager la semaine).**

- **Le produit NIPADA** (DTP, reconstruction) : pipeline arrêté depuis le 3 juillet, 54 tests
  cassés, backlog P0 entièrement « À faire ». **Ne pas promettre du 0 % WER.**
- **Le noyau formel** comme *service* : il est prouvé et vérifiable, mais c'est un assistant de
  preuve lent (1-3 h par validation lourde) et **le produit ℝ n'est pas clos** (`mul_cut_located`
  en cours). Il est prêt comme **artefact** (corpus d'or), pas comme **exécuteur**.
- **Les 11 modules** : coquilles. Seul `ExecutionOrchestrator` a un squelette ; `CoLabController`
  n'a que de la documentation.
- **Panini-FS** : ligne divergente (7 dhātu / 34 atomes), clone local en retard de 140 commits,
  aucun lien avec Drave.
- **L'API REST** : séduisante sur le papier, mais dépend de FastAPI **et** d'un graphe de 33-58 Mo ;
  à ne tester qu'après le reste, et à considérer comme un bonus.

---

## 4. Les trois intégrations les plus mûres

### 4.1 Le corpus UDHR et la généalogie — **la plus mûre, à faire en J2**

**Pourquoi.** Même source XML des deux côtés, données déjà présentes, format texte + JSON, aucune
dépendance. Panini apporte 532 langues étiquetées (famille/branche/tradition) et sa décomposition
V14 ; Drave apporte 456 langues × 30 articles et Glottolog.

**Premier livrable.** Un `data/udhr/` commun : table `iso3 → fichier → famille → branche →
tradition`, échantillon de 20 langues (5 familles × 4), et une mesure de recouvrement des codes.
**Mesure** : nombre de langues appariées, taux d'accord des familles, langues orphelines.
**Contrôle négatif** : deux langues de **familles différentes** doivent donner un retrieval faible,
deux langues **sœurs** un retrieval fort ; si les deux se valent, la mesure ne mesure rien.
**Risque** : les codes ISO ne sont pas les mêmes (Panini utilise des variantes `007`, `008`… ;
Drave a normalisé en `iso3`) — c'est le vrai travail.

### 4.2 Les signatures 14 atomes — **la plus utile pour la table atomes ↔ niveaux**

**Pourquoi.** `analytic_sigs_v1.json` est un JSON plat, sans dépendance ; les 14 atomes ont un
ordre canonique, un symbole et un premier ; Drave a des niveaux (POS, syntagmes, pragmatique) et des
mesures. La confrontation est faisable en une journée.

**Premier livrable.** Une table `atome → niveau(x) Drave` + 20 exemples mesurés (corrélation entre
la part d'un atome et la présence d'un niveau), sur des textes présents des deux côtés.
**Mesure** : 20 exemples, coefficient par atome, cas contradictoires listés.
**Contrôle négatif** : permuter les colonnes de la matrice de signatures — la table doit perdre son
pouvoir prédictif ; sinon, elle ne capte que la longueur du texte.
**Risque** : la signature est **lexicale** ; l'époque domine (β +0,138). Toute corrélation doit être
contrôlée par la date et la langue.

### 4.3 Le corpus d'or CIC — **la plus vérifiable**

**Pourquoi.** C'est le seul artefact Panini qui soit **auto-portant et falsifiable** : 42 entrées,
preuve et type en de Bruijn hexadécimal, empreinte SHA-256, verdict, et une doctrine de validation
croisée (deux checkers indépendants dans leur dépôt : `cic` et `cic_named`). 46 Ko.

**Premier livrable.** Un vérificateur Drave indépendant (ou un rejeu du checker) qui reproduit les
42 verdicts, et le taux d'accord avec Panini.
**Mesure** : 42/42 attendus ; nombre d'écarts ; temps de rejeu.
**Contrôle négatif** : altérer un octet d'une preuve → doit être **rejeté** ; sinon le vérificateur
accepte n'importe quoi.
**Risque** : il faut réimplémenter le format de sérialisation (de Bruijn) — plus coûteux que
l'UDHR, mais le résultat est un **verrou** : « nos deux systèmes vérifient les mêmes preuves ».

**Alternative si le temps manque** : la généalogie à deux faces (4.1 sans le corpus) ou l'API
`/decompose` — mais l'API est la seule des surfaces qui ne soit pas garantie sans exécution.

---

## 5. Pièges et écarts documentaires

1. **Le lien Drave du README Panini pointe vers un fichier absent** :
   `Qtrinet/docs/agent/panini-nipada.md` n'existe pas (le dossier `docs/agent/` est vide) ; le
   document réel est `Qtrinet/docs/methode/panini-nipada.md`. À corriger côté Panini — ou côté
   Drave, en créant le chemin attendu.
2. **Les documents normatifs de l'hôte ne sont pas committés** : `CONTEXTE-IA.md`,
   `PHILOSOPHIE.md`, `docs/ouvrage/` sont `??`. Un `git clean` les emporte.
3. **Deux états par dépôt** : clones standalone gelés (2025-09 → 2026-04) contre pins de
   sous-modules (2026-09-08). Lire le clone donne une image fausse de `Panini-FS`.
4. **Trois vocabulaires** : 14/9 (Research) / 34/7 (Panini-FS) / 9 (docs hôte). La table J2 doit
   dire « V14 de Research ».
5. **Le R² est un instrument, pas un résultat publiable** : leur propre critique du 14/07
   (`CRITIQUE_NIPADA_2026-07-14.md`) note l'absence de hold-out, et le hold-out v1 (23 textes) est
   **gelé**. Le critère de sortie qu'ils revendiquent est la **restitution sans perte**, pas le R².
6. **La généalogie de Panini ne prouve rien** : leurs tests H1/H2 sont KO et le go/no-go religieux
   est NO-GO. Ce qui est vrai, c'est l'avertissement (époque > filiation).
7. **Une lecture SQLite a modifié un fichier de données (à signaler)** : pour inventorier les
   corpus, un `sqlite3` en lecture a ouvert `research/data/mass_ingestion/corpus_expansion.db`,
   qui était en mode WAL. La connexion a **checkpointé le WAL** dans le fichier principal
   (4 096 → 57 344 octets, `-wal` disparu) : les 381 lignes sont intactes et même plus durables,
   mais le fichier apparaît désormais `M` dans `git status`. **Ne pas le restaurer par
   `git checkout`** : les lignes qui n'existaient que dans le WAL seraient perdues. Aucun fichier de
   code, de doc ou de configuration n'a été touché.
8. **Le dépôt « vivant » est un sous-module en HEAD détachée** : un commit accidentel dans
   `Panini/research` peut être perdu (pas de branche). Leur `AGENTS.md` le dit : commits explicites
   uniquement.

---

## 6. Annexe — commandes de rejeu (lecture seule)

```bash
cd /home/stephane/Data13TB/stephane/GitHub
# état des 14 dépôts
for d in Panini Panini-Research Panini-SemanticCore Panini-AttributionRegistry \
         Panini-AutonomousMissions Panini-CloudOrchestrator Panini-CoLabController \
         Panini-CopilotageShared Panini-DatasetsIngestion Panini-ExecutionOrchestrator \
         Panini-FS Panini-PublicationEngine Panini-SpecKit-Shared Panini-UltraReactive; do
  git --no-optional-locks -C "$d" log -1 --format="$d %h %ad %s" --date=short
  git --no-optional-locks -C "$d" status --porcelain | wc -l
done

# les 14 atomes et les 9 dhātus
sed -n '64,77p' Panini/research/src/nipada/core/hardware_mapping.py

# les signatures et les paires
python3 -c "import json;d=json.load(open('Panini/research/nipada/falsification/analytic_sigs_v1.json'));print(len(d), len(next(iter(d.values()))))"
python3 -c "import json;d=json.load(open('Panini/research/nipada/falsification/pairs334_axes_v1.json'));print(d['n_pairs'], d['r2_L2'])"

# le corpus d'or
python3 -c "import json,collections;d=json.load(open('Panini/research/nipada/falsification/corpus_dor_cic_v1.json'));print(len(d['entrees']), collections.Counter(e['verdict'] for e in d['entrees']))"

# l'UDHR des deux côtés
python3 -c "import json;d=json.load(open('Panini/research/data/udhr_corpus.json'));print(d['total_languages'], d['article'])"
wc -l Qtrinet/data/udhr/langues.jsonl
```

---

## 7. Annexe — les deux fichiers écrits

- `Qtrinet/reports/rapport-inventaire-panini.md` (ce fichier)
- `Qtrinet/reports/pensee-inventaire-panini.json` (version machine : dépôts, axes, atomes, corpus,
  interfaces, maturité, actions)

**Aucun commit. Aucun fichier de code, de doc ou de configuration modifié dans `Panini*`. Un seul
fichier de données a bougé** (`research/data/mass_ingestion/corpus_expansion.db`, checkpoint SQLite
involontaire, §5.7) — à ne pas restaurer par `git checkout`.
