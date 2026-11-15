# Session session- — Ajout exemples --tagger et --reel dans la doc

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-e73a3601-e2c6-417c-a009-88ffadca4e61` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 04:35 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 136 |
| Appels d'outils | 155 |
| Fichiers touchés | 8 |
| Commandes | 96 |
| Sous-agents | 0 |
| Commits | 2 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche D1 : les exemples de `docs/produit/exemples.md` — ajoute 3 exemples avec `--tagger` (la sortie réelle avec la clé, le coût affiché) et 2 avec `--reel` (la base honnête), et vérifie que les sorties collent au code courant (F1 0,7902, 238/239, schéma v2). Fiche `reports/rapport-exemples-tagger.md` + JSON, commit.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche D1 : les exemples de `docs/produit/exemples.md` — ajoute 3 exemples avec `--tagger` (la sortie réelle avec la clé, … [198 caractères tronqués]

*155 appels d'outils.* Actions notables :

- bash — List repository root
- bash — Show git status and recent commits
- bash — List product docs and line count
- bash — Find tagger and reel options
- job_kill
- read
- bash — Inspect drave CLI flags
- bash — Check branch and API key availability
- bash — Run offline evaluation JSON
- bash — Inspect DeepSeek client cache
- bash — Extract key evaluation metrics
- bash — Test tagger with live API call
- bash — Find example reports and cache size
- bash — Search report indexes for examples
- … et 120 autres

**Synthèse produite :**

Tâche D1 terminée.

\## Ce qui a été ajouté à `docs/produit/exemples.md`

Le document passe de **5 à 10 blocs** :

**3 exécutions `--tagger`** (clé réelle, cache disque neuf, coût affiché) :
- `g001` « Le chat dort. » — POS identique, `PONCT` restitué : **1 appel, 130 tokens, 1,1 s**
- `g011` « Le livre que j'ai lu… » — `lu` **NOUN → VERB** : **1 appel, 157 tokens, 1,5 s**
- `r241` « The day when we left… » — `when` **CONJ → PRON** (le gold attend PRON) : **1 appel, 154 tokens, 1,1 s**

Total : **3 appels, 441 tokens, 3,7 s**, ~**0,0004 $** (estimation). Sur les **17 tokens du gold** de ces phrases : **14/17 → 16/17** — un chiffre d'exemple, pas une mesure ; les chiffres globaux restent **0,9575 vs 0,8625** sur 612 (+9,5) et **0,9500 vs 0,8891** sur le réel 452 (+6,1).

**2 exécutions `--reel`** (base honnête) :
- `evaluer --reel` : **452 phrases, 2 480 tokens, 184 cibles**, POS **0,8891**, F1 **0,7906**, attachement **183/184 = 0,9946**
- `evaluer --reel --json` : le même contrat en JSON (`gold.nom`, `gold.phrases: 452`, `reel: null`, contrôle négatif **0,00 %**)

\## Vérification contre le code courant

- F1 **0,7902** (P 0,7860 / R 0,7944), attachement **238/238 labels**, **238/239 cibles = 0,9958**.
- Les **3 annotations `--tagger` sont en schéma v2** (`schema: drave.annotation`, `version: 2`), validées **3/3** ; le schéma refuse une version 3 et un champ obligatoire retiré.
- Les **5 nouveaux blocs sont reproduits 5/5** par un comparateur qui rejoue les commandes.
- **Contrôle négatif** : doc mutée (`lu/VERB` → `lu/NOUN`) → **4/5**, écart détecté sur `6.2`.

J'ai aussi recalé `docs/produit/README.md` § 3.7 sur le code courant : **1 appel/phrase**, `PONCT` restitué, **0,9575** sur 612, **22 299 tokens / 155 s / ~0,02 $**.

\## Portes et contrôles

- `bash tools/porte-produit.sh` → **✅ porte produit verte** (autotest **183/183**)
- `revue_documentation.py`, `porte-tableaux.sh`, `taille_documents.py`, `verifie_en_cours.py`, `verifie_journal.py`, `verifier_schemas.py` : **verts**

\## Commits

- `d23780d7` — D1, doc + fiche + JSON + état/roadmap
- `e42bac4f` — journal du 15/11

Fichiers principaux : [`docs/produit/exemples.md`](docs/produit/exemples.md), [`reports/rapport-exemples-tagger.md`](reports/rapport-exemples-tagger.md), [`reports/rapport-exemples-tagger.json`](reports/rapport-exemples-tagger.json). Les modifications non liées déjà présentes dans l'arbre de travail ont été laissées intactes.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md` | 0 | 8 |
| `/tmp/verifier_d1.py` | 1 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-exemples-tagger.md` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 9 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/docs.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** List repository root
- **T1** Show git status and recent commits
- **T1** List product docs and line count
- **T1** Find tagger and reel options
- **T1** Inspect drave CLI flags
- **T1** Check branch and API key availability
- **T1** Run offline evaluation JSON
- **T1** Inspect DeepSeek client cache
- **T1** Extract key evaluation metrics
- **T1** Test tagger with live API call
- **T1** Find example reports and cache size
- **T1** Search report indexes for examples
- **T1** Inspect existing replay report JSON
- **T1** Search product notice for tagger and reel sections
- **T1** Find task D1 in state and roadmap
- **T1** Search current work plan for D1
- **T1** Inspect plan JSON structure
- **T1** Read D1 plan block
- **T1** Fresh-cache tagger on g001
- **T1** Fresh-cache tagger on g011
- **T1** Fresh-cache tagger on r241
- **T1** Inspect gold JSON structure
- **T1** Show gold entries for chosen examples
- **T1** Search real gold for r241
- **T1** Show heuristic POS for the three examples
- **T1** Placeholder check outputs
- **T1** Show heuristic POS and schema version
- **T1** Run evaluer --reel text output
- **T1** Run evaluer --reel JSON and extract fields
- **T1** Capture tagger JSON and verify schema v2
- **T1** Inspect journal layout
- **T1** Read reports indexes
- **T1** Read today's journal entries
- **T1** Check index and journal tool usage
- **T1** Check system and commit dates
- **T1** Inspect uncommitted change scope
- **T1** Inspect documentation review checks
- **T1** Compute current counters
- **T1** Inspect product gate script
- **T1** Produce exact reel JSON extract with jq
- … et 56 autres

## 4. Mesures et résultats marquants

- **T1** `./reports/README.md:22:| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |`
- **T1** `./reports/rapport-bilan-nuit.md:11:| **le tagger en option** (`--tagger`) | POS **95,75 %** sur 612 (+9,5), **95,00 %** sur le réel 452 (+6,1) ; **1 appel**/phrase ; `PONCT` restitué ; ~0,02 $ | [`rap`
- **T1** `./reports/rapport-bilan-nuit.md:12:| **la base honnête** (`--reel`) | 452 phrases : POS **88,91 %**, F1 **79,06 %**, attachement **99,46 %** ; publiée à côté du global | [`rapport-base-reelle.md`](rap`
- **T1** `[still running after 60000ms; moved to background job bash-4]`
- **T1** `langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `docs/pilotage/en-cours.md:64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **re`
- **T1** `langue=fr script=Latn source=cascade · 43 étiquettes · unités sémantiques=3 (48.6% du texte)`
- **T1** `langue=en script=Latn source=cascade · 38 étiquettes · unités sémantiques=3 (45.7% du texte)`
- **T1** `POS         exactitude 88.91 %  (fermé 92.94 %, ouvert 84.66 %)`
- **T1** `SYNTAGMES   F1 79.06 %  (P 81.28 % / R 76.95 %)`
- **T1** `tête      F1 89.90 %  (P 93.84 % / R 86.28 %)`
- **T1** `vue linéaire (partition filtrer) F1 79.53 %  · attachement 91.85 % de couverture`
- **T1** `ATTACHEMENT exact 99.46 % · couverture 99.46 % · exact sur span 100.00 % · top-k 98.91 %`
- **T1** `tête      couverture 100.00 % · top-k 99.45 %`
- **T1** `PRAGMATIQUE acte 99.56 % · négation 96.90 % · modalité 98.45 % · double sens 96.46 %`
- **T1** `FRACTION SÉMANTIQUE 50.82 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 0.00 % (graine 0, 184 cibles)`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `| [`rapport-pos-anglais-v2.md`](rapport-pos-anglais-v2.md) | **B13** — POS **83,83 %** (R2a/R3/R2b), F1 **0,6181** |`
- **T1** `| [`rapport-cache-chunker-applique.md`](rapport-cache-chunker-applique.md) | **B13** — le cache appliqué : **×139** en |`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `| [rapport-elagage-logs.md](rapport-elagage-logs.md) | A6.3 — l'élagage guidé par les logs : aucun neurone ne s'allume jamais, mais 63 % s'allument à peine |`
- **T1** `| [rapport-familles-9.md](rapport-familles-9.md) | C3.2c — les 9 familles : 7 sur 9 au-dessus de 30 % |`
- **T1** `| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |`
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) | `en-cours.md`, `README.md`, `
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) | `en-cours.md`, `README.md`, `me`
- **T1** ``0,092` · `0,160` · `0,811` · `0,657` · `0,440` · `0,429` · `2,7856` · `40,0658` · `95,00 %` · `95,75 %``
- **T1** `**27 326 tokens de sortie** (totaux à ±0,5 % près, six prompts dupliqués).`
- **T1** `| **unités sémantiques** | les spans candidats à la RSN et la fraction du texte | **55,4 %** du texte en moyenne |`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : s/v7 deepseek.key [exit code: 1]
- **T1** : === Le chat dort. === Le livre que j'ai lu est intéressant. === The day when we left was beautiful. [stderr]   File "<string>", line 1     import json,sys; a=json.load(sys.stdin); print(" ".join(f"{e[
- **T1** : old block words 122 [stderr] Traceback (most recent call last):   File "<stdin>", line 6, in <module> ValueError: substring not found [exit code: 1]

## 6. Commits

- git commit -F - <<'MSG' D1 — LES EXEMPLES DU TAGGER ET DE LA BASE RÉELLE : 3 BLOCS --tagger (441 TOKENS, 3,7 S), 2 BLOCS --reel (452 PHRASES, POS 88,91, F1 79,0
- git add journal git commit -F - <<'MSG' JOURNAL — 2026-11-15 : D1, LES EXEMPLES --tagger (441 TOKENS, 3,7 S) ET --reel (452 PHRASES) SONT DANS LA DOC ; 5/5 REJO

