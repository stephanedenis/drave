# Session session- — Vérifier et corriger les exemples de la doc

> **Journaux :** [le jour](../../2026-11-16/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-a5cb52af-8e84-4452-a21e-1bba677dd8e4` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-16 02:29 |
| Durée | 0.5 h |
| Tours | 1 |
| Messages | 194 |
| Appels d'outils | 219 |
| Fichiers touchés | 8 |
| Commandes | 146 |
| Sous-agents | 0 |
| Commits | 4 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche V2 (exploitable) : les **exemples de la doc** — rejoue les 5 blocs de `docs/produit/exemples.md` avec le code courant (**les candidats objets, les rôles normalisés, la durée**) et corrige les sorties qui ont bougé ; vérifie le `demarrage.md` (les 3 commandes) ; le **contrôle négatif** : aucune sortie de la doc ne doit différer du code (un script de vérification `tools/verifie_exemples.py` si … [66 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche V2 (exploitable) : les **exemples de la doc** — rejoue les 5 blocs de `docs/produit/exemples.md` avec le code cour … [346 caractères tronqués]

*219 appels d'outils.* Actions notables :

- bash — Inspect workspace root and git state
- bash — List product docs
- read
- bash — Run current CLI basic example
- bash — Inspect working diff
- bash — Read working diff of CLI
- bash — Search new fields in CLI
- bash — Inspect current annotation fields
- bash — Find role normalization and duration
- bash — Full annotation g001
- bash — Read bloc annotation json method
- bash — Replay example 1 JSON
- bash — Replay example 2 JSON
- bash — Replay example 3 JSON
- … et 190 autres

**Synthèse produite :**

✅ **V2 terminée et committée** — `ae3c24f2`

- **5 blocs rejoués** : **3 corrigés** par la normalisation des rôles (`qualité` → `qualite`, `prédicat` → `predicat`, `groupe nominal` → `objet`) ; `g001` et le refus identiques hors enrichissement.
- **Candidats objets** : `meta.attachement.candidats` publié sur les 4 blocs JSON, **18 objets, 18 spans exacts, 0 faux**. **Durée** : `--duree` documenté, `cout.duree_s` absent par défaut.
- **Démarrage** : **3/3 commandes** conformes dans une copie **sans** `tools/structures` ; JSON **5 899 octets**, extrait 22 lignes, consommateur et `profils` vérifiés. La note « dépôt de développement » est vérifiée **4/4** (`agent`, `chat`, 79,02 %, 99,58 %).
- **Contrôle négatif** : `tools/verifie_exemples.py` — **27/27 cas, 0 écart** ; mutation `qualite` → `qualité` détectée **1/1**. Intégré à `tools/porte-produit.sh`.
- **Fiche + JSON** : `reports/rapport-exemples-v2.md`, `reports/rapport-exemples-v2.json`.
- **Vérifications** : porte produit **verte** (183/183), revue documentaire, budget de contexte, journal et état **verts**.

**Limites nommées** : les blocs `--tagger` ne sont pas rejoués par l'API (tokens/latence non reproductibles) ; la durée est une horloge murale non reproductible ; le démarrage est une copie source sans sous-module, pas un `git clone` + `venv` + `pip`.

Le commit inclut aussi la base **U1–U3/V1** qui était non committée dans l'arbre (profils UDHR, `--strict`, roue) : le CLI importe `profils_udhr` et la porte teste `--strict`, le commit ne démarre pas sans elle.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `docs/produit/exemples.md` | 0 | 19 |
| `tools/verifie_exemples.py` | 1 | 12 |
| `reports/rapport-exemples-v2.md` | 1 | 0 |
| `docs/pilotage/en-cours.md` | 0 | 12 |
| `docs/pilotage/roadmap.md` | 0 | 6 |
| `journal/2026-11-16/README.md` | 0 | 1 |
| `reports/README.md` | 0 | 3 |
| `tools/porte-produit.sh` | 0 | 2 |

### Commandes exécutées (échantillon)

- **T1** Inspect workspace root and git state
- **T1** List product docs
- **T1** Run current CLI basic example
- **T1** Inspect working diff
- **T1** Read working diff of CLI
- **T1** Search new fields in CLI
- **T1** Inspect current annotation fields
- **T1** Find role normalization and duration
- **T1** Full annotation g001
- **T1** Read bloc annotation json method
- **T1** Replay example 1 JSON
- **T1** Replay example 2 JSON
- **T1** Replay example 3 JSON
- **T1** Replay example 5 JSON
- **T1** Read role vocabulary
- **T1** Read related docs/tests diffs
- **T1** Recent commits
- **T1** Find feature commits
- **T1** Inspect feature commits stats
- **T1** Existing reports and verifiers
- **T1** See doc changes from T1-T2
- **T1** Search README for features
- **T1** Find existing checks referencing examples
- **T1** Read README key sections
- **T1** Replay refusal example
- **T1** Replay reel evaluation
- **T1** Separate refusal streams
- **T1** Check DeepSeek key availability
- **T1** Read prior examples replay report
- **T1** Inspect plan around V2
- **T1** Search state/roadmap for V2
- **T1** Read V2 acceptance criteria
- **T1** Read product gate
- **T1** Diff product gate
- **T1** Inspect U3 commit
- **T1** Last commits per file
- **T1** Check structures submodule
- **T1** Read quickstart report
- **T1** Find structures usage
- **T1** Find role generation logic
- … et 106 autres

## 4. Mesures et résultats marquants

- **T1** `langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO`
- **T1** `83adaa2b T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE`
- **T1** `9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS`
- **T1** `7f0e8320 T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))`
- **T1** `c43dd5cc B13 — LA RÈGLE « QUE » (PRON APRÈS UN NOM, CONJ AILLEURS) : POS 85,84 → 86,25 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `6b976cb1 B13 — R4-FR FILTRÉ (ADJECTIF CONNU OU SUFFIXE) : POS 85,75 → 85,84 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `5c5d3b52 B13 — LE PAQUET POS SÛR (CLASSES FERMÉES + R4-EN) : POS 83,83 → 84,96 %, 37 CORRIGÉS / 0 CASSÉ, ATTACHEMENT INCHANGÉ ; 183/183`
- **T1** `2ba393b0 B13 — LA POS À 83,83 % (R2a/R3/R2b) : F1 0,5849 → 0,6181, ANGLAIS 0,6341 → 0,7273, ATTACHEMENT INCHANGÉ (222/222) ; 183/183`
- **T1** `T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS`
- **T1** `chevauchement (v2) ; `rang: 1` est la vue préférée, pas une suppression.`
- **T1** `77:| **unités sémantiques** | les spans candidats à la RSN et la fraction du texte | **55,4 %** du texte en moyenne |`
- **T1** `89:1,67 %** (graine 0, 239 cibles). L'audit v10 publie un contrôle plus dur — un **candidat`
- **T1** `| **unités sémantiques** | les spans candidats à la RSN et la fraction du texte | **55,4 %** du texte en moyenne |`
- **T1** `1,67 %** (graine 0, 239 cibles). L'audit v10 publie un contrôle plus dur — un **candidat`
- **T1** `aléatoire** dans les listes donne **42,14 %** de top-1 — et la **permutation des cibles**`
- **T1** `**1,997/220 = 0,908 %** ; les deux donnent p = 0. Un chiffre sans sa contre-épreuve n'est pas un`
- **T1** `attachement 99,46 %). Les chiffres de la fiche v12 (0,6511/0,6482, 235/236) sont **datés** : ils`
- **T1** `POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)`
- **T1** `SYNTAGMES   F1 79.02 %  (P 78.60 % / R 79.44 %)`
- **T1** `**Lecture.** Le porteur `REL [22:42]` est le **rang 2** d'un groupe de **3** segments ; ses deux`
- **T1** `alternatives sont au rang 1 (la REL longue `[22:54]`, qui le **contient** : `inclus`) et au rang 3`
- **T1** `POS         exactitude 88.91 %  (fermé 92.94 %, ouvert 84.66 %)`
- **T1** `SYNTAGMES   F1 79.06 %  (P 81.28 % / R 76.95 %)`
- **T1** `tête      F1 89.90 %  (P 93.84 % / R 86.28 %)`
- **T1** `vue linéaire (partition filtrer) F1 79.53 %  · attachement 91.85 % de couverture`
- **T1** `ATTACHEMENT exact 99.46 % · couverture 99.46 % · exact sur span 100.00 % · top-k 98.91 %`
- **T1** `tête      couverture 100.00 % · top-k 99.45 %`
- **T1** `PRAGMATIQUE acte 99.56 % · négation 96.90 % · modalité 98.45 % · double sens 96.46 %`
- **T1** `FRACTION SÉMANTIQUE 50.82 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 0.00 % (graine 0, 184 cibles)`
- **T1** `sont inchangés ; les **2 unités** et **61,5 %** du texte aussi.`
- **T1** `segments du groupe 0 portent `meta.partition` (`membres: 3` ; rang 1 = REL longue, rang 2 = GV,`
- **T1** `rang 3 = REL courte) et `meta.alternative` avec les deux autres. La doc le dit maintenant au § 2.`
- **T1** `15:> `agent` / `chat`, et `evaluer` **81,88 %** / **88,70 %** au lieu de **79,02 %** / **99,58 %**.`
- **T1** `93:| `drave evaluer` | `/tmp/qs-doc/drave` | **0** | **86,25 %** | **81,88 %** | **88,70 %** |`
- **T1** `178:| `evaluer` — F1 | **81,88 %** | **79,02 %** |`
- **T1** `179:| `evaluer` — attachement exact | **88,70 %** | **99,58 %** |`
- **T1** `204:sous-module), rendent `agent` / `chat` et **79,02 % / 99,58 %**. C'est ce contraste qui prouve`
- **T1** `> `agent` / `chat`, et `evaluer` **81,88 %** / **88,70 %** au lieu de **79,02 %** / **99,58 %**.`
- **T1** `SYNTAGMES   F1 81.88 %  (P 86.64 % / R 77.62 %)`
- **T1** `tête      F1 90.83 %  (P 96.11 % / R 86.10 %)`
- **T1** `vue linéaire (partition filtrer) F1 81.88 %  · attachement 93.72 % de couverture`
- **T1** `BASE RÉELLE (hand + reel, 452 phrases)  POS 88.91 % · F1 80.14 % · attachement 91.85 %`
- **T1** `ATTACHEMENT exact 88.70 % · couverture 93.72 % · exact sur span 94.64 % · top-k 89.54 %`
- **T1** `tête      couverture 100.00 % · top-k 95.54 %`
- **T1** `PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %`
- **T1** `FRACTION SÉMANTIQUE 54.76 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)`
- **T1** `langue=fra script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; **19/19 verdicts `/paragraphes`** (11 accepté`
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 15/11 (nuit).** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **F1 0,7902**, `
- **T1** `**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (hasard`
- **T1** `devant, mais l'anglais est **100 % réel** quand le français ajoute **160 synthétiques** ; sur le`
- **T1** `canonique**, le strict **5/46** ; temps CLI médian **159,2 ms**, API **2,7 ms**. Comparaison`
- **T1** `sources acquises ne sont pas 102 URL (71 URL uniques). La loi H0 se reproduit (**R² = 0,909139** sur`
- **T1** `contre null **−0,129**, p=0,335). Sur les 44 signatures, le retrieval brut donne **61,4 %** de même`
- **T1** `tradition et **56,8 %** de voisins à ≤50 ans, mais les contrôles croisés ramènent la filiation à`
- **T1** `**50,0 %** (p=0,0492, Holm 0,128) et l'époque à **53,8 %** (p=0,373) ; seule une petite prédiction`
- **T1** `d'année intra-tradition survit (**R²=0,042**, p=0,0086, Holm 0,034). Le β époque **+0,138** de la v150`
- **T1** `**14,8 Mo** JSON ; α = **1,55**, `_groupes_partition`/`_cible_proche` **O(k²)**.`
- **T1** `**U1 — les O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),`
- **T1** `| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO |`
- **T1** `(`membres: 3` ; rang 1 = REL longue, rang 2 = GV, rang 3 = REL courte) et `meta.alternative``
- **T1** `comme « 100 % du langage » : c'est 100 % des spans prédits, sur **99,58 %** des cibles. Le cas`
- **T1** `JSON complet) ; la sortie lisible donne **2 unités**, soit **61,5 %** du texte. La durée`
- **T1** `langue=en script=Latn source=cascade · 38 étiquettes · unités sémantiques=3 (45.7% du texte)`
- **T1** `✅ note dev f1 — F1 79.02 %`
- **T1** `POS         exactitude 86.25 %  (fermé 93.73 %, ou`
- **T1** `✅ note dev attachement — ATTACHEMENT exact 99.58 %`
- **T1** `"detail": "F1 79.02 %"`
- **T1** `"detail": "ATTACHEMENT exact 99.58 %"`
- **T1** `langue=fr script=Latn source=heuristique · 43 étiquettes · unités sémantiques=3 (48.6% du texte)`
- **T1** `langue=en script=Latn source=heuristique · 37 étiquettes · unités sémantiques=2 (28.1% du texte)`
- **T1** `-  JSON complet) ; la sortie lisible donne **2 unités**, soit **61,5 %** du texte.`
- **T1** `+  JSON complet) ; la sortie lisible donne **2 unités**, soit **61,5 %** du texte. La durée`
- **T1** `| [rapport-evaluer-strict.md](rapport-evaluer-strict.md) | V1 — `evaluer --strict` : les quatre modes locaux, la cascade à 86,25 % / 88,91 %, le plancher 0,70 qui mord |`
- **T1** `| [rapport-familles-9.md](rapport-familles-9.md) | C3.2c — les 9 familles : 7 sur 9 au-dessus de 30 % |`
- **T1** `| [`rapport-tagger-lot.md`](rapport-tagger-lot.md) | **X3/R0.7** — le tagger **en lot** : **1 000 items** (677 textes), **672 appels réseau**, **99 971 tokens**, **685,2 s**, **87,6 items/min**, **40,`
- **T1** `| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |`
- **T1** `188:| [rapport-evaluer-strict.md](rapport-evaluer-strict.md) | V1 — `evaluer --strict` : les quatre modes locaux, la cascade à 86,25 % / 88,91 %, le plancher 0,70 qui mord |`
- **T1** `-20/20. Trois limites : clone public 88,70 % d'attachement au lieu de 99,58 %, O(k²) (α = 1,55),`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `25:| [`rapport-tagger-lot.md`](rapport-tagger-lot.md) | **X3/R0.7** — le tagger **en lot** : **1 000 items** (677 textes), **672 appels réseau**, **99 971 tokens**, **685,2 s**, **87,6 items/min**, **`

## 5. Erreurs rencontrées

7 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 496, in <module>     raise SystemExit(main())                      
- **T1** : [stderr] Traceback (most recent call last):   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 496, in <module>     raise SystemExit(main())                      
- **T1** : [stderr] Traceback (most recent call last):   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 496, in <module>     raise SystemExit(main())                      
- **T1** : [stderr] Traceback (most recent call last):   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_exemples.py", line 497, in <module>     raise SystemExit(main())                      
- **T1** : ✅ exemples §1 lisible — 10 ligne(s)   ✅ exemples §1 JSON — JSON exact   ✅ exemples §1 durée — duree_s=0.004704 (variable), octets exacts   ✅ exemples §2 JSON — JSON exact   ✅ exemples §3 JSON — JSON e
- **T1** : ✅ exemples §1 lisible — 10 ligne(s)   ✅ exemples §1 JSON — JSON exact   ✅ exemples §1 durée — duree_s=0.004057 (variable), octets exacts   ✅ exemples §2 JSON — JSON exact   ✅ exemples §3 JSON — JSON e
- **T1** : [stderr]   ❌ commit refusé : 1 fait(s) stagé(s) sans docs/pilotage/en-cours.md      · reports/README.md      → mettre l'état à jour, puis `git add docs/pilotage/en-cours.md`   ⛔ commit refusé : un fai

## 6. Commits

- V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE  Les cinq blo
- git add -- reports/README.md && git commit --amend --no-edit && git log -1 --oneline | head -1
- git add -- reports/README.md docs/pilotage/en-cours.md && git commit --amend --no-edit && git log -1 --oneline | head -1 && git status --short
- git add -- docs/pilotage/en-cours.md && git commit --amend --no-edit >/tmp/amend.log 2>&1; code=$?; tail -4 /tmp/amend.log; echo "code=$code"; git log -1 --onel

