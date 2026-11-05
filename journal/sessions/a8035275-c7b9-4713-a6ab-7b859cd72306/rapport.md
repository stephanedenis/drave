# Session a8035275 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `a8035275-c7b9-4713-a6ab-7b859cd72306` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 13:11 |
| Durée | 0.5 h |
| Tours | 1 |
| Messages | 50 |
| Appels d'outils | 60 |
| Fichiers touchés | 1 |
| Commandes | 47 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **diagnostiquer les 57 échecs du top-k strict** de l'attachement.  Contexte : `tools/tests/linguistique/evaluer_gold.py` expose `charger()` (612 phrases) et `evaluer_bloc` ; `tools/bloc_linguistique.py` expose `Heuristique`. Sur les 145 segments gold dont le span est prédit, la cible du go … [1931 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **diagnost … [2211 caractères tronqués]

*60 appels d'outils.* Actions notables :

- bash — Check git status and repo layout
- bash — Count lines in key files and list reports
- read
- bash — Locate attachment logic in bloc_linguistique
- bash — List gold files and inspect first phrase
- bash — Reproduce top-k measurement numbers
- bash — Dump details for 57 strict failures
- bash — Locate S generator and cibles_s
- bash — Find the literal source of structure la plus proche
- bash — Inspect structures generator attachment
- bash — Read base segmentation and analyser
- bash — Deep-dive special failure cases
- bash — Locate verb lexicon and POS function
- bash — Measure F1 head-reduction gain
- … et 39 autres

**Synthèse produite :**

⏵ Diagnostic livré : 57 échecs qualifiés, 3 correctifs chiffrés

\## Verdict

Les **57 échecs du top-k strict** sont tous qualifiés (0 « autre »), sur **145 segments au bon span** : cible en sous-chaîne **134** (0,9241), en égalité exacte **88** (0,6069). Le **top-1 est déjà juste 123/145** (0,8483), et **41 des 57 échecs ont déjà la bonne cible choisie** : le top-k strict mesure surtout la **forme des candidats**, pas la règle d'attachement.

\## Effectifs par cause

| # | Cause | Eff. | Dont sous-chaîne |
|---|---|---:|---:|
| C1 | Candidat S non réduit — cible nominale REL (« … → Le livre ») | 26 | 26 |
| C2 | Candidat S non réduit — cible verbale GP (« … → Les fleurs poussent ») | 17 | 17 |
| C3 | Candidat S non réduit — cible attribut (« … → est prêt ») | 2 | 2 |
| C4 | Verbe anglais hors lexique (`fly`, `climbs`, `flows`, `swims`, `get`, `smiles`, `wait`, `belongs`) | 8 | 0 |
| C5 | GP génitif — tête du GN à gauche jamais candidate | 1 | 0 |
| C6 | Verbe français hors lexique, aucun GV (`marche`) | 1 | 0 |
| C7 | Candidat tokenisé avec enclitique (`appelle-moi`) | 1 | 1 |
| C8 | GV du S mal délimité (`Peut-être`, `viendra`) | 1 | 0 |
| | **Total** | **57** | **46** |

Types : REL 26, GP 29, SUB 2 — sources : hand 3, reel 43, synthétique 11.

\## 3 correctifs (simulés, non appliqués)

1. **F1 — réduire chaque candidat S à sa tête : +45 segments.** `tools/bloc_linguistique.py`, `Heuristique.analyser` (branche 5. syntagmes, construction de `noms` l. 826 et `candidats` l. 858/874/892) + helper existant `_tete_nom` (l. 616). Réduit `« … → Le livre »` à `livre`, `« … → Les fleurs poussent »` à `poussent`. Top-1 inchangé.
2. **F2 — compléter le lexique verbal anglais : +8 segments.** `_est_verbe` (l. 428) via `VERBES_CONNUS` (l. 374), et `VERBES["en"]` (l. 319) pour le POS. Ajoute `fly, climb, flow, swim, get, smile, wait, belong` + flexions. **+8 top-1, 0 régression.**
3. **F3 — repli par tokens : +4 segments.** `Heuristique._verbes_proches` (l. 670) et `_cible_proche` (l. 643) : tête du GN à gauche pour un GP, verbes reconnus dans une fenêtre, découpe des enclitiques, formes manquantes (`marche`, `appelle`, `viendra`). Top-1 +4 conditionnel.

**Cumul simulé** : 88 → 133 (0,9172) → 141 (0,9724) → **145/145 (1,0)**. Top-1 : 123 → 123 → 131 → 135\*. Ces gains sont des **bornes hautes sur le même gold**, pas une généralisation.

\## Contrôle négatif et limites

- F1 avec le **premier** token au lieu de la tête : **0/45** ; F2 avec 8 verbes anglais non pertinents 
… [949 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md` | 1 | 3 |

### Commandes exécutées (échantillon)

- **T1** Check git status and repo layout
- **T1** Count lines in key files and list reports
- **T1** Locate attachment logic in bloc_linguistique
- **T1** List gold files and inspect first phrase
- **T1** Reproduce top-k measurement numbers
- **T1** Dump details for 57 strict failures
- **T1** Locate S generator and cibles_s
- **T1** Find the literal source of structure la plus proche
- **T1** Inspect structures generator attachment
- **T1** Read base segmentation and analyser
- **T1** Deep-dive special failure cases
- **T1** Locate verb lexicon and POS function
- **T1** Measure F1 head-reduction gain
- **T1** Simulate English lexicon fix
- **T1** Measure elision-aware F1 and negative control
- **T1** Find existing pensee JSON conventions
- **T1** Inspect JSON report schemas
- **T1** Find reports mentioning attachment top-k
- **T1** Read sample fiche and JSON structure
- **T1** Read prior attachment-target report
- **T1** Read prior proximity-target report
- **T1** Read prior attachment JSON numbers
- **T1** Check recent history of bloc and gold
- **T1** Run evaluer_gold current output
- **T1** Check HEAD and local diffs for eval files
- **T1** Extract attachment numbers from eval
- **T1** Check gold file history
- **T1** Diff eval files since lexicon commit
- **T1** Inspect convention commit changes
- **T1** Classify all 57 failures mechanically
- **T1** Corrected categories, fix gains, controls
- **T1** Check verb recognition for target forms
- **T1** Debug token verb scan for r080
- **T1** Debug F3 extra candidates per case
- **T1** Find all mutations of VERBES_CONNUS
- **T1** Check lexicon mutation after analysis
- **T1** Verify deliverable filenames are new
- **T1** Generate diagnostic JSON with 57 rows
- **T1** Regenerate JSON with corrected controls
- **T1** Validate generated JSON structure
- … et 7 autres

## 4. Mesures et résultats marquants

- **T1** `> **1,0/1,0/0,994/0,889**, cascade **67,1 %**, **attachement par tête couverture 1,0 / top-1 0,957 / top-k 1,0** (span 0,323/0,338), hasard 0,015 ; **36 cibles ambiguës annotées en double lecture**. ⚠`
- **T1** `couvre **67,1 %** du texte en unités sémantiques.`
- **T1** `# B13 — la cible par proximité : l'exact passe de 0,0042 à 0,0544 (×13)`
- **T1** `> **exact 1 (0,0042)** à **13 (0,0544)** — **×13**. La tête fait **94/145 (0,6483)** contre 81`
- **T1** `| **exact** | **1 (0,0042)** | **13 (0,0544)** | **+12 (×13)** |`
- **T1** `- **La proximité est un signal réel** : +13 top1 et **×13 en exact** — le verbe le plus proche est`

