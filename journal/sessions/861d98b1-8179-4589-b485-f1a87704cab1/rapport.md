# Session 861d98b1 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-10-19/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `861d98b1-8179-4589-b485-f1a87704cab1` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-19 14:15 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 102 |
| Appels d'outils | 102 |
| Fichiers touchés | 1 |
| Commandes | 70 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave Natif », tout en français). Ta tâche est un sous-chantier AUTONOME et PRÉCIS : construire et VALIDER un alignement phrase-à-phrase entre l'original français et la traduction anglaise du « Tour du monde en quatre-vingts jours » de Jules Verne, pour servir de banc de traduction littéraire.  CONTEXTE (à lire a … [4105 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave Natif », tout en français).  … [4385 caractères tronqués]

*102 appels d'outils.* Actions notables :

- bash — List source text files and sizes
- bash — Locate measure 59 in report
- bash — Read measure 59 narrative
- bash — Show heads of both texts
- bash — Find chapter-like lines in French text
- bash — Count CHAPTER lines in English
- bash — Show French body start
- bash — Find bare roman numeral lines in French
- bash — Inspect English body and tails
- bash — Check line formatting and end markers
- bash — Explore chapter markers with Python
- bash — Locate Gutenberg body boundaries
- bash — List tools, data, reports directories
- bash — Inspect French dialogue formatting
- … et 77 autres

**Synthèse produite :**

⏵ Vérification finale des sorties et rédaction du bilan

\## Verdict : **VALIDE**

L'alignement est validé par des ancres **indépendantes de l'appariement** (elles ne servent jamais à aligner, seulement à juger) : **93,2 % des occurrences d'ancres distinctives se retrouvent à ±2**, contre **0,3 %** quand on permute les chapitres (**×272,5**), et **83,6 %** à distance 0.

\## Fichiers créés (aucun fichier existant modifié, aucun commit)

- Outil : `tools/aligneur_litteraire.py` — CPU, bibliothèque standard, aucun modèle.
- JSON : `data/alignement/verne_fr_en.json` — 3 397 paires, 1,3 Mo (gitignoré).
- Fiche : `reports/alignement-verne.md` — 200 lignes, dispositif + chiffres + contrôles + limites.

Reproduction : `CUDA_VISIBLE_DEVICES="" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py` (~24 s).

Remarque : `reports/traduction-eurlex-0.5b.json`, non suivi, n'est pas de moi — je n'y ai pas touché.

\## Chapitres et tables des matières

- **37 chapitres français / 37 chapitres anglais**, numéros contigus 1..37 et identiques.
- Chaque langue donne **74 lignes candidates** : 37 entrées de table des matières (même forme que les en-têtes : `I TITRE` / `CHAPTER I. TITRE`) + 37 vrais en-têtes.
- Filtre **par longueur** : pour chaque numéro, on garde la candidate dont le bloc suivant est le plus long (≥ 1 500 caractères ; une entrée de table fait ~100). **37 lignes de table écartées par langue**, puis vérification de contiguïté et d'identité des numéros.

\## Paires alignées

- 4 275 phrases FR / 3 526 phrases EN.
- **3 464 perles** Gale-Church (chapitre par chapitre, ratio global EN/FR = 0,875) ; **3 397 perles appariées** des deux côtés, dont **2 570 paires 1:1 strictes** (2:1 : 628 ; 1:2 : 86 ; 3:1 : 81 ; 1:0 : 59 ; 2:2 : 29 ; 0:1 : 8 ; 1:3 : 3).
- Couverture : **4 216 phrases FR (98,6 %)** et **3 518 EN (99,8 %)** ; 59 phrases FR et 8 EN non appariées.

\## Rappel des ancres et contrôles négatifs

81 groupes d'ancres (personnages, lieux, navires, institutions), cherchés avec frontières de mot, insensibles aux accents et à la casse (majuscule exigée pour `fix`, `young`, `speedy`, `hitch`, `smith`, `proctor`, `reform`).

| mesure (FR → EN) | toutes ancres | distinctives (≤ 6 chapitres) |
|---|---:|---:|
| occurrences | 2 686 | 587 |
| distance 0 | 81,1 % | **83,6 %** |
| ±1 | 90,2 % | 91,3 % |
| **±2** | 92,7 % | **93,2 %** |
| ±5 | 95,6 % | 96,1 % |

Sens inverse EN → FR (distinctives) : 86,6 % à 0, 95,8 % à ±2. Les manques sont surtout des **déplac
… [2947 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aligneur_litteraire.py` | 1 | 17 |

### Commandes exécutées (échantillon)

- **T1** List source text files and sizes
- **T1** Locate measure 59 in report
- **T1** Read measure 59 narrative
- **T1** Show heads of both texts
- **T1** Find chapter-like lines in French text
- **T1** Count CHAPTER lines in English
- **T1** Show French body start
- **T1** Find bare roman numeral lines in French
- **T1** Inspect English body and tails
- **T1** Check line formatting and end markers
- **T1** Explore chapter markers with Python
- **T1** Locate Gutenberg body boundaries
- **T1** List tools, data, reports directories
- **T1** Inspect French dialogue formatting
- **T1** Prototype chapter detection
- **T1** Prototype sentence segmentation
- **T1** Extract candidate proper nouns
- **T1** Count name occurrences in both texts
- **T1** Prototype Gale-Church alignment and anchor recall
- **T1** Run negative controls and chapter anchor matrix
- **T1** Verify anchor pair occurrences with word boundaries
- **T1** Check alternate spellings for anchors
- **T1** Inspect existing tool style
- **T1** Check Python version and git status
- **T1** Compile and run tool without negative controls
- **T1** Debug chapter body extraction
- **T1** Run tool without negative controls
- **T1** Re-run tool without negative controls
- **T1** Locate negative-control report code
- **T1** Show code to patch
- **T1** Run full tool with negative controls to /tmp
- **T1** Inspect JSON samples and structure
- **T1** Inspect chapter 1 opening alignment
- **T1** Per-chapter diagnostics and longest sentences
- **T1** Diagnose weaker chapters and anchor misses
- **T1** Merge Cromarty anchors and rerun baseline
- **T1** Per-chapter and per-anchor recall after merge
- **T1** Classify anchor misses as moved vs absent
- **T1** Show evaluer_ancres block
- **T1** Show par_ancre section
- … et 30 autres

## 4. Mesures et résultats marquants

- **T1** `| **propre** | **0,93-1,72** | 46-269 | 6-12 % | french |`
- **T1** `| **fautes 10 %** | **5,09-5,21** ✓✓ (×3-5) | 302-948 | **41-42 %** ✓✓ | french ✗ |`
- **T1** `| **langue mêlée 30 %** | **2,48-3,18** ✓ (×1,5-3) | 156-371 | 19-22 % ✓ | french ✗✗ |`
- **T1** `| **accents perdus** | 1,35-2,19 ✓ (×1,3-1,5) | 66-330 | 12-17 % ✓ | french ✗ |`
- **T1** `* **MAIS LA LANGUE NE LE VOIT PAS** ✗✗ : elle répond « french » dans **les quatre** cas ✓✗, y compris avec **30 % de`
- **T1** `* **ce que cela donne à la couche** ✓✓ : l'entrée peut être **annotée** (« surprisal 5,2, 41 % de tokens coûteux »)`
- **T1** `| 0,5 B | 4 | 1 | 1 | 4 | 40 % | 0,63 |`
- **T1** `| 1,5 B | 6 | 0 | 2 | 2 | 60 % | 0,64 |`
- **T1** `| 3 B | 4 | 2 | 2 | 2 | 40 % | 0,59 |`
- **T1** `| **7 B** | **2** | 2 | **3** | 3 | **20 %** ✗✗ | **0,74** |`
- **T1** `[still running after 60000ms; moved to background job bash-229]`
- **T1** `· **fautes** : 10 % des caractères remplacés par un caractère voisin ✓ ;`
- **T1** `· **langue mêlée** : 30 % du texte remplacé par l'article anglais correspondant ✓✓ ;`
- **T1** `1493:            f"{neg_moyen:.1%} à ±{args.rayon} (seuil {args.seuil_controle:.0%})",`
- **T1** `1504:            f"{neg_moyen:.1%} quand les chapitres sont permutés (×{facteur:.0f}) ; les 37 chapitres se "`
- **T1** `f"{rappel_reel:.1%} à ±{args.rayon} (seuil {args.seuil_rappel:.0%})",`
- **T1** `f"{neg_moyen:.1%} à ±{args.rayon} (seuil {args.seuil_controle:.0%})",`
- **T1** `f"les ancres distinctives se retrouvent à {rappel_reel:.1%} à ±{args.rayon}, contre "`
- **T1** `f"{neg_moyen:.1%} quand les chapitres sont permutés (×{facteur:.0f}) ; les 37 chapitres se "`
- **T1** `VERDICT : VALIDE — les ancres distinctives se retrouvent à 88.8% à ±2, contre 0.3% quand les chapitres sont permutés (×281) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout`
- **T1** `VERDICT : VALIDE — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 parto`
- **T1** `verdict: True les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).`
- **T1** `| `cromarty` | 53 | 81,1 % | 90,6 % |`
- **T1** `| `stuart` | 31 | 87,1 % | 90,3 % |`
- **T1** `| `rangoon` | 31 | 61,3 % | 80,6 % |`
- **T1** `| `carnatic` | 29 | 86,2 % | 96,6 % |`
- **T1** `| `proctor` | 24 | 87,5 % | 91,7 % |`
- **T1** `| `henrietta` | 24 | 87,5 % | 95,8 % |`
- **T1** `| `omaha` | 21 | 95,2 % | 100,0 % |`
- **T1** `| `tankadere` | 20 | 85,0 % | 100,0 % |`
- **T1** `Le point faible est `rangoon` (61,3 % à distance 0) : le traducteur paraphrase parfois le nom du navire (« the steamer », « the first few days of the voyage ») là où le français l'écrit ; l'ancre manq`
- **T1** `**Par chapitre** (≥ 5 occurrences distinctives) : le rappel à distance 0 va de 45,5 % (chapitre 9) à 100,0 % (chapitre 6). Les chapitres sous 70 % sont : 9 (45,5 %), 17 (57,1 %), 15 (65,0 %), 14 (65,5`
- **T1** `**Phrases sans ancre** : 55,1 % des phrases françaises et 51,4 % des phrases anglaises ne contiennent aucun nom propre du dictionnaire ; 45,1 % des perles n'ont d'ancre ni d'un côté ni de l'autre. C'e`
- **T1** `**VALIDE** — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).`
- **T1** `- ✓ **rappel des ancres distinctives** : 93,2 % à ±2 (seuil 80,0 %)`
- **T1** `- ✓ **contrôle négatif (chapitres permutés)** : 0,3 % à ±2 (seuil 10,0 %)`
- **T1** `- ✓ **facteur au-dessus du hasard** : ×272,5 (seuil ×8)`
- **T1** `fogg           présent FR dans  631 paires ; même ancre EN  525 (83.2 %)`
- **T1** `passepartout   présent FR dans  415 paires ; même ancre EN  348 (83.9 %)`
- **T1** `aouda          présent FR dans  131 paires ; même ancre EN  110 (84.0 %)`
- **T1** `fix            présent FR dans  261 paires ; même ancre EN  213 (81.6 %)`
- **T1** `londres        présent FR dans   60 paires ; même ancre EN   50 (83.3 %)`
- **T1** `bombay         présent FR dans   58 paires ; même ancre EN   51 (87.9 %)`
- **T1** `reform         présent FR dans   37 paires ; même ancre EN   32 (86.5 %)`
- **T1** `5:**Verdict** : **VALIDE** — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale `
- **T1** `85:| rappel à distance 0 | 81,1 % | 83,6 % |`
- **T1** `87:| rappel ±2 | 92,7 % | 93,2 % |`
- **T1** `131:| **alignement réel** | 92,7 % | 93,2 % | 83,6 % |`
- **T1** `140:**Hasard pur, phrase contre phrase dans le même chapitre** : 38 400 tirages, **15,62 %** de rencontres d'ancres. C'est un plancher **phrase contre phrase** — conservateur, parce que les noms propr`
- **T1** `172:2. **La tolérance ±2 absorbe les différences de découpage.** Le taux à distance 0 (83,6 % sur les distinctives) est le chiffre honnête ; le ±2 (93,2 %) dit qu'une phrase voisine porte souvent le m`
- **T1** `174:4. **Le contrôle négatif « chapitres permutés » n'est pas un hasard parfait** : les chapitres voisins partagent des personnages, et l'anglais d'un chapitre peut contenir les mêmes noms qu'un autre`
- **T1** `183:**VALIDE** — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout`
- **T1** `189:- ✓ **rappel des ancres distinctives** : 93,2 % à ±2 (seuil 80,0 %)`
- **T1** `resume: les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur contenu (diagonale n° 1 partout).`
- **T1** `True rappel des ancres distinctives : 93,2 % à ±2 (seuil 80,0 %)`
- **T1** `True contrôle négatif (chapitres permutés) : 0,3 % à ±2 (seuil 10,0 %)`
- **T1** `True facteur au-dessus du hasard : ×272,5 (seuil ×8)`

## 5. Erreurs rencontrées

5 sorties en erreur ou divergentes. Les premières :

- **T1** : count: 0 [exit code: 1]
- **T1** : DANS LEQUEL PHILEAS FOGG ET PASSEPARTOUT S'ACCEPTENT RM-CM-^ICIPROQUEMENT L'UN^M$ around_world_80_days_fr.txt: Unicode text, UTF-8 (with BOM) text, with CRLF line terminators around_world_80_days_en.t
- **T1** : COMPILE_OK [1/7] lecture des textes… [2/7] repérage des chapitres (filtre par longueur)…       FR 74 candidates → 37 chapitres ; EN 74 → 37 [3/7] découpage en phrases…       FR 4275 phrases / 408378 c
- **T1** : [1/7] lecture des textes… [2/7] repérage des chapitres (filtre par longueur)…       FR 74 candidates → 37 chapitres ; EN 74 → 37 [3/7] découpage en phrases…       FR 4275 phrases / 408378 caractères ;
- **T1** : [1/7] lecture des textes… [2/7] repérage des chapitres (filtre par longueur)…       FR 74 candidates → 37 chapitres ; EN 74 → 37 [3/7] découpage en phrases…       FR 4275 phrases / 408378 caractères ;

