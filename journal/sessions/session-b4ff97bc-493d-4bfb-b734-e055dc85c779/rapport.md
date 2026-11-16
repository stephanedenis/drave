# Session session- — CLI drave profils : détection de langue

> **Journaux :** [le jour](../../2026-11-16/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-b4ff97bc-493d-4bfb-b734-e055dc85c779` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-16 01:31 |
| Durée | 0.5 h |
| Tours | 1 |
| Messages | 189 |
| Appels d'outils | 214 |
| Fichiers touchés | 5 |
| Commandes | 208 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche U3 (suite de T5) : `--profils` — exposer la **détection de langue** (les 398 langues de l'autotest UDHR) dans le CLI : `drave profils --texte` (ou `analyser --profils`) rend la langue probable, le script et la confiance, pour un texte donné ; mesure sur les 20 langues de l'échantillon UDHR (la précision), le contrôle négatif (un texte ambigu), la doc § 3. Fiche `reports/rapport-profils.md` + … [13 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche U3 (suite de T5) : `--profils` — exposer la **détection de langue** (les 398 langues de l'autotest UDHR) dans le C … [293 caractères tronqués]

*214 appels d'outils.* Actions notables :

- bash — Inspect repository root and git state
- bash — Read current state document
- bash — Search for 398 language references
- bash — List source and tools files
- bash — Search 398 excluding venv
- bash — Find UDHR-related files
- bash — Read pyproject and locate CLI
- bash — Read CLI start
- bash — Explore linguistics tests and language refs
- bash — Locate language profile functions and UDHR profile results
- bash — Read 71-language boundary qualifier
- bash — Read profile and script detection implementation
- bash — Read autotest UDHR implementation
- bash — Locate CLI commands
- … et 199 autres

**Synthèse produite :**

\## U3 — `drave profils` : la détection de langue UDHR exposée

**Livré.**

\### CLI

```bash
drave profils --texte "Le chat dort."
drave profils --texte "Привет мир" --json
drave profils --fichier article.txt --json
drave analyser "Le chat dort." --profils
```

La sortie rend **la langue probable** (ISO 639-3), **le script** et **la confiance** ; le JSON porte en plus `langue` (décision), `langue_probable`, `marge`, `seuil`, `sous_seuil`, `source`, `prior`, `candidats` et les métadonnées des profils. Sous le seuil `0,12`, la décision est `und` ; la langue probable reste publiée.

Deux chemins explicites :
- **texte long** → les **398 profils UDHR** (`source: profils`) ;
- **texte court** → prior des mots-outils des 7 langues du bloc (`source: lexique`), avec le désaccord visible dans `prior` vs `candidats` ;
- un mot isolé ou un mot-outil seul (`chat`, `le`) rend `und`.

\### Résultats mesurés

| mesure | résultat |
|---|---:|
| 20 langues de l'échantillon UDHR, article 15 | **20/20 = 1,0000** |
| script, article 15 | **20/20** |
| 20 langues, articles 15–30 | **313/320 = 0,9781** |
| script, articles 15–30 | **320/320** |
| autotest complet 398 langues, profils bruts | **433/447 = 0,9687** |
| chemin CLI (hybride court/long) | **431/447 = 0,9642** |
| profils permutés | **0/20** · **1/447 = 0,0022** |
| texte ambigu bilingue | **`und`**, confiance **0,0836 < 0,12** |

L’artefact fait **802 110 octets**, sha256 `33aee69d…` ; il est **identique** aux profils reconstruits depuis le corpus (0 différence) et voyage dans la roue (`drave profils` a été testé installé depuis `/tmp`). Roue sans l’artefact → **code 4**, `stdout` vide, pas de trace.

\### Fichiers

- `reports/rapport-profils.md` — la fiche.
- `reports/profils.json` — la mesure reproductible.
- `tools/profils_udhr.py` — chargement, détection, prior court, `ProfilsAbsents`.
- `tools/construire_profils_udhr.py` — construction déterministe des 398 profils + `--verifier`.
- `tools/mesurer_profils.py` — la mesure (20 langues, 398, permuté, contrôles, CLI).
- `tools/tests/linguistique/profils_udhr.json` — l’artefact embarqué.
- `tools/tests/test_profils.py` — **20 tests**.
- `tools/drave.py` — commande `profils`, option `analyser --profils`, `_HeuristiqueProfils`, code 4.
- `pyproject.toml` — `profils_udhr.json` dans les `package-data`.
- `tools/porte-bloc-linguistique.sh` et `tools/porte-produit.sh` — cas `profils` ajoutés.
- Documentation : `docs/produit/README.md` **§ 3.8**, `docs/produit/demarrage.md` **§
… [921 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/profils_udhr.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/construire_profils_udhr.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_profils.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_profils.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-profils.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Inspect repository root and git state
- **T1** Read current state document
- **T1** Search for 398 language references
- **T1** List source and tools files
- **T1** Search 398 excluding venv
- **T1** Find UDHR-related files
- **T1** Read pyproject and locate CLI
- **T1** Read CLI start
- **T1** Explore linguistics tests and language refs
- **T1** Locate language profile functions and UDHR profile results
- **T1** Read 71-language boundary qualifier
- **T1** Read profile and script detection implementation
- **T1** Read autotest UDHR implementation
- **T1** Locate CLI commands
- **T1** Read CLI command implementations
- **T1** Inspect UDHR corpus
- **T1** Read bloc linguistique report
- **T1** Read existing linguistic tests
- **T1** Read language test and find CLI tests
- **T1** Find tests exercising CLI
- **T1** Inspect gates
- **T1** Find U3 references
- **T1** Read product CLI tests
- **T1** Locate docs mentioning profiles
- **T1** Read bloc linguistique doc section 3
- **T1** Read usage docs
- **T1** Read U3 task details from bilan
- **T1** Inspect product docs sections
- **T1** Find section 3 references
- **T1** Read T5 report structure for precedent
- **T1** Read product README sections 3.5-3.7
- **T1** Read demarrage section 3
- **T1** Read doc multilingual and limits sections
- **T1** Read wheel report
- **T1** Read CLI test remainder
- **T1** Inspect schema fields
- **T1** Inspect language detection integration and thresholds
- **T1** Inspect UDHR language codes and scripts
- **T1** Measure existing UDHR profiles and sample
- **T1** Check deterministic evenly spaced 20-language sample
- … et 168 autres

## 4. Mesures et résultats marquants

- **T1** `d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO`
- **T1** `83adaa2b T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE`
- **T1** `9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS`
- **T1** `7f0e8320 T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.`
- **T1** `tools/structures/README.md:204:dans le cadre — 1 020 × 550 pour l'exemple, 1 398 et 1 613 px pour les deux autres paragraphes),`
- **T1** `reports/rapport-minimal.md:63:| modèle minimal — ternaire dense 2 b | 0.0 Mo | 0.000 | 13989862.4 | 312 | 9360 |`
- **T1** `reports/rapport-minimal.md:73:| 70B — ternaire CSR | 148750.0 Mo | 15398.551 | 0.1 | 37 | 1110 |`
- **T1** `reports/rapport-v41-mhc.md:299:       3 tokens notés — perplexité cumulée 39839289.516  (0.1 tok/s)`
- **T1** `reports/archive/rapport-toutes-langues.md:5937:| fr–pt | 3 375,0 | 98 % | 101,1 | 27 % | 33,398 | 363 % | ok |`
- **T1** `reports/archive/rapport-campagne-benefices.md:366:| **multilingue / sémantique** | bande **10–15 sur 24 couches** (42–62 % de séparation) sur **398 langues** ; couche 0 : séparation nulle | `rapport-c`
- **T1** `reports/toutes-langues/104-92-la-pire-paire-apres-echelle-de-en-a-486.md:30:| fr–pt | 3 375,0 | 98 % | 101,1 | 27 % | 33,398 | 363 % | ok |`
- **T1** `reports/campagne-benefices/007-04-ce-que-le-depot-sait-deja-par-famille-de.md:23:| **multilingue / sémantique** | bande **10–15 sur 24 couches** (42–62 % de séparation) sur **398 langues** ; couche 0 `
- **T1** `reports/rapport-loi-frontiere-fenetre.md:86:| 10 000 | 7,3980 | +1,5 % | +4,7 % |`
- **T1** `reports/rapport-pensee-silencieuse.md:24:| **B′. 1 pas silencieux, état NORMÉ** (échelle des entrées) | **292 935** | +3 035 398 % ✗✗ |`
- **T1** `./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:9766:docs/pilotage/roadmap.md:33:| **R — le lecteur** | document, politique de lecture, fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **`
- **T1** `./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:28003:| **L — le bloc langue** (nouveau) | le CPU peut-il étiqueter la surface et le réseau ne traiter que le résidu ? | ✅ **contrat +`
- **T1** `./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:29474:docs/pilotage/roadmap.md:33:| **R — le lecteur** | document, politique de lecture, fenêtre, mémoire, restitution | ✅ R0.1–R0.3 *`
- **T1** `./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:42422:docs/pilotage/chantiers.md:88:| **L — le bloc langue** (nouveau) | le CPU peut-il étiqueter la surface et le réseau ne traiter q`
- **T1** `./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:44220:docs/pilotage/chantiers.md:88:| **L — le bloc langue** (nouveau) | le CPU peut-il étiqueter la surface et le réseau ne traiter q`
- **T1** `./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md:41:  CPU + neuronal de contrat, parallèle/cascade, activation 51–76 %) ; **398 langues à 0,9687**,`
- **T1** `> substituables, un parallèle et une cascade, une activation sémantique à **51–76 %** ; la`
- **T1** `docs/produit/demarrage.md:53:> pour `evaluer` F1 **79,02 %** / attachement **99,58 %** (voir [`README.md`](README.md) § 3.1`
- **T1** `> **Le chiffre.** `--duree` ajoute `cout.duree_s` au JSON de `analyser` — **4,7 à 5,6 ms**`
- **T1** `> mesurés sur « Le chat dort. », **5,9 ms** sur la phrase longue — et **ne change rien`
- **T1** `| aide | `aide_globale`, 4 × 2 sous-commandes | ✅ 9/9 |`
- **T1** `| codes | usage × 3, refus × 2, clé absente, tableau de la notice | ✅ 7/7 |`
- **T1** `- **La durée est machine-dépendante** : les valeurs (4,7–5,9 ms) situent l'ordre de`
- **T1** `| `tools/tests/test_produit.py` | 6 tests T5 : durée JSON/JSONL, tableau, aide/help × 4, fichier inexistant, répertoire |`
- **T1** `fidélité    : exacte 1.0000 · caractères 1.0000 · couverture 100.00%`
- **T1** `mots        : exacte 0.0000 · caractères 0.9286 · couverture 84.62%`
- **T1** `pos         : exacte 0.0000 · caractères 0.9286 · couverture 84.62%`
- **T1** `**88,91 %**, F1 **79,06 %**, attachement **99,46 %**. Sans lui, `evaluer` publie la ligne`
- **T1** `langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `**La mesure.** Sur les **20 phrases `hand`** du gold (105 tokens) : POS **88,57 % → 97,14 %**`
- **T1** `(**+8,57 pts**), syntagmes et attachement **inchangés**. Sur le **gold 612** : **86,25 % →`
- **T1** `95,75 %** (**+9,5 pts**) ; sur le **réel 452**, **88,91 % → 95,00 %** (**+6,1 pts**) — le`
- **T1** `POS         exactitude 97.14 % (fermé 94.74 %, ouvert 100.00 %) · Δ +8.57 pts vs heuristique`
- **T1** `SYNTAGMES   F1 90.16 % (tête 97.39 %) — conservés à l'heuristique`
- **T1** `> pour `evaluer` F1 **79,02 %** / attachement **99,58 %** (voir [`README.md`](README.md) § 3.1`
- **T1** `langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)`
- **T1** `SYNTAGMES   F1 81.88 %  (P 86.64 % / R 77.62 %)`
- **T1** `tête      F1 90.83 %  (P 96.11 % / R 86.10 %)`
- **T1** `vue linéaire (partition filtrer) F1 81.88 %  · attachement 93.72 % de couverture`
- **T1** `BASE RÉELLE (hand + reel, 452 phrases)  POS 88.91 % · F1 80.14 % · attachement 91.85 %`
- **T1** `ATTACHEMENT exact 88.70 % · couverture 93.72 % · exact sur span 94.64 % · top-k 89.54 %`
- **T1** `tête      couverture 100.00 % · top-k 95.54 %`
- **T1** `PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %`
- **T1** `FRACTION SÉMANTIQUE 54.76 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)`
- **T1** ``CONTRÔLE NÉGATIF` est le garde-fou : une cible au hasard trouve **1,67 %**, l'attachement`
- **T1** `**88,70 %**. `--gold` mesure le gold gelé 602, `--reel` la base réelle 452, `--par-langue` le`
- **T1** `la cascade (mock de contrat) préserve ces chiffres et couvre **67,1 %** en unités sémantiques.`
- **T1** `(les réels passent de 40 % à 80 % en tête avec les deux lectures). Le **vrai** modèle neuronal est **refusé**`
- **T1** `[still running after 60000ms; moved to background job bash-41]`
- **T1** `./reports/rapport-ie-sous-familles.md:30:  (20 langues) à **54,6 %**.`
- **T1** `./reports/rapport-deepseek.md:213:point reste **610 exemples / 20 langues** (3,71 % à 500 pas), et le **310 / 10 langues** (2,93 %)`
- **T1** `./reports/rapport-inventaire-panini.md:440:tradition`, échantillon de 20 langues (5 familles × 4), et une mesure de recouvrement des codes.`
- **T1** `./reports/corpus-commun.json:743:    "principe": "20 langues stratifiées (5 familles glottolog × 4) + le français, pivot de Drave ; toutes les paires sont exactes après normalisation."`
- **T1** `127:Les cinq familles retenues couvrent **267/418 = 63,9 %** du pool exact ; le turcique (**17**,`
- **T1** `> appariables (**95,4 %**). **20 écarts de surface** sont **exclus, pas corrigés**. Les **8 contrôles**`
- **T1** `| fichiers communs | **453** | **99,3 %** de Drave ; **85,2 %** de Panini | l'intersection des identifiants de fichier |`
- **T1** `| article 1 côté Drave | 440 | 96,5 % de Drave | 16 fichiers Drave n'ont pas d'article 1 |`
- **T1** `| appariables article 1 | **438** | 96,7 % de l'intersection | 15 communs sans article 1, 2 Drave hors Panini |`
- **T1** `| **paires exactes** | **418** | **95,4 %** des appariables ; **78,6 %** de Panini | le corpus disponible |`
- **T1** `| écarts de surface | 20 | 4,6 % des appariables | exclus, pas corrigés |`
- **T1** `| Indo-European | 120 | 28,7 % | 5 |`
- **T1** `| Atlantic-Congo | 81 | 19,4 % | 4 |`
- **T1** `| Austronesian | 37 | 8,9 % | 4 |`
- **T1** `**Répartition** : 20 strates (5 × 4) + 1 pivot ; **10 écritures** — latin 11 textes, arabe 2,`
- **T1** `**14,8 Mo** JSON ; α = **1,55**, `_groupes_partition`/`_cible_proche` **O(k²)**.`
- **T1** `**U1 — les O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),`
- **T1** `20/20. Trois limites : clone public 88,70 % d'attachement au lieu de 99,58 %, O(k²) (α = 1,55),`
- **T1** `33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**`
- **T1** `166:**U1 — les O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),`
- **T1** `| **B — l'intelligence** | le sens, la logique, les jeux, les maîtres : que sait faire le système ? | ✅ B1–B12 ; B10.3 bloqué (encodeur) ; **B13** state store v0 + DRVF + **bloc linguistique** (POS **`
- **T1** `| **R — le lecteur** | un document, une question, un budget : réponse sourcée ou refus motivé ? | ✅ R0.1–R0.3 ; R0.4/R0.5 négatifs ; R4.1–R4.4 mesurés (R4.4 : 4/5 familles ≥ 90 %) | **R1.1/R1.2** (con`
- **T1** `| **L — le bloc langue** (nouveau) | le CPU peut-il étiqueter la surface et le réseau ne traiter que le résidu ? | ✅ **contrat + bloc v0** : 9 niveaux, **398 langues à 0,9687**, **gold 432 réels + 160`
- **T1** `| **D — les données** (nouveau) | avec quoi entraîne-t-on, et à quel prix ? | ✅ inventaire local ; **10 corpus texte intégral** (20,53 M art., 67,73 G car., 81,2 Go, **8 Ko 0**), **PDF** (322 Mo), **d`
- **T1** `| **B13 — le moteur de pensée** | penser est-il une recherche tracée sur des états pluriels ? | ✅ state store v0 + AC-3/alpha-bêta + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes** `
- **T1** `84:| **B — l'intelligence** | le sens, la logique, les jeux, les maîtres : que sait faire le système ? | ✅ B1–B12 ; B10.3 bloqué (encodeur) ; **B13** state store v0 + DRVF + **bloc linguistique** (POS`
- **T1** `88:| **L — le bloc langue** (nouveau) | le CPU peut-il étiqueter la surface et le réseau ne traiter que le résidu ? | ✅ **contrat + bloc v0** : 9 niveaux, **398 langues à 0,9687**, **gold 432 réels + `
- **T1** `90:| **B13 — le moteur de pensée** | penser est-il une recherche tracée sur des états pluriels ? | ✅ state store v0 + AC-3/alpha-bêta + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes`
- **T1** `| `porte-c4-retard.sh` | 29 s | PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne |`
- **T1** `| `porte-coupe.sh` | 131 s | ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit pour  |`
- **T1** `# la confiance du prior est sa part de mots-outils, sans le ×2 du repli`
- **T1** `langue=fra script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `langue=fra script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `**86,25 % à 95,75 %** (**+9,5 pts**) ; sur le réel 452, de **88,91 % à 95,00 %** (**+6,1**).`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-tagger-lot.md`](rapport-tagger-lot.md) | **X3/R0.7** — le tagger **en lot** : **1 000 items** (677 textes), **672 appels réseau**, **99 971 tokens**, **685,2 s**, **87,6 items/min**, **40,`
- **T1** `| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `reports/INDEX.md:637:| [rapport-performance-fix.md](rapport-performance-fix.md) | U1 — les deux O(k²) sont bornés : 10 000 mots de **4,0 s à 0,82 s** (×4,9), α de **1,53 à 1,08**, sorties **identiques`
- **T1** `| [rapport-s-analyseur.md](rapport-s-analyseur.md) | S — L'analyseur contre les structures écrites à la main : 7/7 séquences, 93,9 % de couverture |`
- **T1** `| [rapport-s-corpus-reel.md](rapport-s-corpus-reel.md) | S — L'analyseur lit le français propre (65,5 % de GN+GV), pas le CEGEP OCR (8,5 %, plancher du mélange) |`
- **T1** `| [rapport-vitesse-v41.md](rapport-vitesse-v41.md) | Rapport — La nuit des optimisations V4.1 : ×3,54 sur la passe, et pas un chiffre changé |`
- **T1** `+**La mesure.** Sur les **20 langues stratifiées** de l'échantillon UDHR (5 familles × 4,`
- **T1** `reports/rapport-roue.md:9:> l'artefact de profils (802 110 octets) ajoute ~0,33 Mo : la roue courante fait **2 055 129`
- **T1** `179:- **`--profils` est une option** : elle charge l'artefact (~800 Ko) et score 398 profils par`
- **T1** `...................                                                      [100%]`
- **T1** `reports/rapport-roue.md:9:> l'artefact de profils (802 110 octets) ajoute ~0,33 Mo : la roue courante fait **2 055 192`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 3, in <module> ModuleNotFoundError: No module named 'profils_udhr' [exit code: 1]
- **T1** : tools/porte-produit.sh [exit code: 2]

