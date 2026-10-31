# Session 7a63b441 — Dépôt /home/stephane/GitHub/Qtrinet, s

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `7a63b441-9131-42c8-9f21-da97ea1dbaaa` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 12:03 |
| Durée | 0.6 h |
| Tours | 1 |
| Messages | 71 |
| Appels d'outils | 81 |
| Fichiers touchés | 3 |
| Commandes | 56 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Dépôt /home/stephane/GitHub/Qtrinet, sprint autonome 24 h. Sous-agent A9 : brancher **M2** (voies ventrales/dorsales) dans la chaîne B13 et mesurer le bout en bout, sans modifier les modules existants.  État : - `tools/cerveau/pipeline_semantique.py` : B13 M1→M5→M6→M8, M1 528/528, M5 contexte 18,7 % vs 12,6 %, M6 94,3 %, M8 57,95 % (borne haute). - `tools/cerveau/voies.py` : M2 `Voies` + `entraine … [1938 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Dépôt /home/stephane/GitHub/Qtrinet, sprint autonome 24 h. Sous-agent A9 : brancher **M2** (voies ventrales/dorsales) da … [2218 caractères tronqués]

*81 appels d'outils.* Actions notables :

- bash — List repo root and cerveau modules
- bash — Check file sizes and git status
- bash — Find semantique module and read pipeline
- bash — Read existing pipeline tests and sequences
- bash — Read voies.py part 1
- bash — List semantique modules
- bash — Read voies.py part 2
- bash — Read typed and synth corpora
- bash — Read voies.py part 3
- bash — Read voies tests and universaux
- bash — Find M2 reports
- bash — Read M1 M5 M6 M9 interfaces
- bash — List tmp results and M2 reports
- bash — Inspect base model and modele.py
- … et 61 autres

**Synthèse produite :**

⏵ Résumé final et chemins

\## Résultat

**M2 n'ajoute rien à la chaîne.** M1 lit **146/146** items réels `de`/`vers` ; M2 lit **93,4 / 93,6 %**. Le remplacer dans la chaîne **dégrade** le champ dorsal de **6,4–6,6 pts**, et aucun étage ne consomme M2 (M5 consomme M1, M6 appelle le codec directement).

| mesure | `de` | `vers` |
|---|---:|---:|
| M1 avec contexte | **100,00 %** | **100,00 %** |
| M1 sans contexte | 94,52 % | 94,52 % |
| M2 avec contexte (3 graines) | **93,38 % ± 0,40** | **93,61 % ± 0,79** |
| M2 vu / inédit / inédit couvert | 100 % / 10,3/20 / 10,3/13 | 100 % / 10,7/20 / 10,7/13 |
| Chaîne avec M2 | 93,38 % | 93,61 % |
| Chaîne sans M2 | **100 %** | **100 %** |

- **M2 seul** reproduit A3 (93,6/94,3) à 0,2–0,7 pt ; A5 à 1 000 pas avec augmentation plafonne à 95,2/95,4, toujours sous M1.
- **M5** : 18,70 % avec plateau vs 12,60 % sans (surprise 2,423 vs 3,112) ; plateau permuté 5,97 % / surprise 12,639. **M6** : 94,32 % (confluence), 94,95 % (commutation).
- **M9** : lésion dorsale M2 → 2,05/2,74 % ; lésion ventrale → action 13,01 %, champ intact ; M1 sans contexte → 70,83 % (code), 94,52 % (`de`/`vers`).
- **Correction importante** : le brut « M5 avec M1 lésé = 28,03 % » est un **artefact de sélection** (couverture 51,4 %, seuls les pas de dames survivent ; la référence y fait exactement 28,03 %, les 374 pas d'échecs à 8,82 % sont perdus). Le JSON contient la couverture et le détail par jeu.

\## Chemins

- `/tmp/a9-pipeline-m2.json` — chiffres, prédictions par item, couverture M5, lésions, commandes.
- `/tmp/a9-pipeline-m2.md` — rapport complet, limites et autocritique.
- `tools/cerveau/pipeline_semantique_m2.py` — module (working tree : +25/−5 pour la couverture M5).
- `tools/cerveau/tests/test_pipeline_semantique_m2.py` — 11 tests.

**Tests** : 11/11 OK ; suite complète `discover` **123 tests OK**. Aucun `git add/commit/checkout` ; docs, reports, journal, batterie non touchés.

**Note dépôt** : HEAD contient déjà B14 (même dispositif, mêmes chiffres). Notre apport est la correction du contrôle M5 M1-lésé et les champs de couverture ; le rapport B14 devrait être amendé sur ce point.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py` | 1 | 13 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_pipeline_semantique_m2.py` | 1 | 0 |
| `/tmp/a9-pipeline-m2.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** List repo root and cerveau modules
- **T1** Check file sizes and git status
- **T1** Find semantique module and read pipeline
- **T1** Read existing pipeline tests and sequences
- **T1** Read voies.py part 1
- **T1** List semantique modules
- **T1** Read voies.py part 2
- **T1** Read typed and synth corpora
- **T1** Read voies.py part 3
- **T1** Read voies tests and universaux
- **T1** Find M2 reports
- **T1** Read M1 M5 M6 M9 interfaces
- **T1** List tmp results and M2 reports
- **T1** Inspect base model and modele.py
- **T1** Read A3 and A5 M2 reports
- **T1** Read M2 training script
- **T1** Read B13 report and A6 M5/M6 results
- **T1** Read predictif.py rest
- **T1** Read codecs API
- **T1** Read Porte.executer
- **T1** Find codec lit
- **T1** Read Porte executer and init
- **T1** Inspect typed corpus and real corpus
- **T1** Evaluate M1 on de/vers subsets and sequences
- **T1** Check GPU availability
- **T1** Read normalisation and pad
- **T1** Benchmark M2 training and eval
- **T1** Inspect sequence contexts
- **T1** Read codec lit context use
- **T1** Inspect position/RSN conversions
- **T1** Test reconstructed contexts on sequence surfaces
- **T1** Retry reconstructed contexts on sequence surfaces
- **T1** Inspect morpion codec and state
- **T1** Inspect morpion coup_valide
- **T1** Verify seen/unseen masks
- **T1** Measure M1 528 and M6 reference
- **T1** Locate sections to fix
- **T1** Check syntax and device references
- **T1** Run smoke test of pipeline module
- **T1** Inspect smoke JSON structure
- … et 16 autres

## 4. Mesures et résultats marquants

- **T1** `varie (`poser` 92 %, `passer` 8 %). Prédire `action` ne peut donc pas battre la`
- **T1** `classe majoritaire : le 98,9 % publié était le taux de cette constante.`
- **T1** `comparée à la langue cible. Son « exactitude » de 72,9 % était donc le taux du`
- **T1** `politique « toujours non » obtient 75 %, et chaque canal seul (langue ou sens)`
- **T1** `obtient 75 % aussi, avec 25 % de faux positifs. La seule politique qui dépasse`
- **T1** `le taux de base est la **conjonction** (sens ET langue) : exactitude 94,3 %,`
- **T1** `exactitude équilibrée 88,6 %, 0 faux positif, 5 faux négatifs. Les 5 FN sont`
- **T1** `| `de` | 146 | 3660 | 6 / 10 / 65 | 47.9 % | 1.5 % | 86.3 % | 95.2 % | 65.0 % |`
- **T1** `| `vers` | 146 | 3660 | 8 / 16 / 65 | 47.3 % | 1.5 % | 86.3 % | 95.2 % | 65.0 % |`
- **T1** `| `point` | 70 | 10044 | 3 / 81 / 82 | 97.1 % | 1.2 % | 94.3 % | 100.0 % | 100.0 % |`
- **T1** `| `chemin_0` | 70 | 392 | 3 / 4 / 65 | 97.1 % | 1.5 % | 80.0 % | 98.6 % | 92.9 % |`
- **T1** `Le recouvrement de surface est le point critique : `de` et `vers` ont 86,3 % de leurs surfaces réelles déjà vues sous forme normalisée, `point` 94,3 %, `chemin_0` 80,0 %. L'exactitude globale est donc`
- **T1** `| `de` | 146 | 93.6 % ± 0.4 % | 47.9 % | 1.5 % | 33.0 % | 100.0 % (126) | 53.3 % (20) | 82.1 % (13) |`
- **T1** `| `vers` | 146 | 94.3 % ± 0.4 % | 47.3 % | 1.5 % | 37.4 % | 100.0 % (126) | 58.3 % (20) | 89.7 % (13) |`
- **T1** `| `point` | 70 | 95.7 % ± 0.0 % | 97.1 % | 1.2 % | 65.7 % | 100.0 % (66) | 25.0 % (4) | 25.0 % (4) |`
- **T1** `| `chemin_0` | 70 | 83.3 % ± 0.8 % | 97.1 % | 1.5 % | 28.6 % | 99.4 % (56) | 19.0 % (14) | 20.5 % (13) |`
- **T1** `*Lecture.* `vers` est **décodable** : 94,3 % global, 100 % sur les 126 surfaces vues, et 11,7/13 (89,7 %) sur les surfaces inédites dont la classe est couverte. Les 7 items de classes jamais vues (roq`
- **T1** `| `de` | 92.7 % | 93.6 % | 14.2 % | 93.6 % | 92.7 % | 2.1 % |`
- **T1** `| `vers` | 92.7 % | 94.3 % | 14.2 % | 94.3 % | 92.7 % | 1.1 % |`
- **T1** `| `point` | 98.6 % | 95.7 % | 15.7 % | 95.7 % | 98.6 % | 1.0 % |`
- **T1** `| `chemin_0` | 81.4 % | 83.3 % | 7.1 % | 83.3 % | 81.4 % | 2.4 % |`
- **T1** `Action globale (n = 528) : 87.4 % ; lésion ventrale 13.1 % ; lésion dorsale 87.4 %.`
- **T1** `La double dissociation est nette : la lésion ventrale fait tomber l'action au hasard (1/8 = 12,5 %) sans toucher le champ dorsal ; la lésion dorsale fait tomber le champ au hasard sans toucher l'actio`
- **T1** `| `mean+last` | 300 | 87.4 % | 93.6 % | 94.3 % | 95.7 % | 83.3 % |`
- **T1** `| `mean-300†` | 300 | 50.0 % | 47.9 % | 50.0 % | 4.3 % | 80.0 % |`
- **T1** `| `last` | 300 | 80.9 % | 93.6 % | 94.1 % | 95.7 % | 90.0 % |`
- **T1** `| `mean+last*` | 1000 | 87.3 % | 92.5 % | 94.5 % | 95.7 % | 78.6 % |`
- **T1** `| `mean*` | 1000 | 77.8 % | 89.7 % | 91.1 % | 94.3 % | 81.4 % |`
- **T1** `| `de` | 93.6 % | 47.9 % | 93.6 % | 92.5 % | 89.7 % | -2.7 % |`
- **T1** `| `vers` | 94.3 % | 50.0 % | 94.1 % | 94.5 % | 91.1 % | -3.4 % |`
- **T1** `| `point` | 95.7 % | 4.3 % | 95.7 % | 95.7 % | 94.3 % | -1.4 % |`
- **T1** `| `chemin_0` | 83.3 % | 80.0 % | 90.0 % | 78.6 % | 81.4 % | 2.9 % |`
- **T1** `**Le piège d'optimisation.** À 300 pas, la moyenne seule paraît au hasard (de 48,0 %, vers 50,0 %, point 4,3 %). Ce n'est pas une absence d'information : une sonde linéaire sur les mêmes features moye`
- **T1** `| `de` | 92.5 % | 89.7 % | -2.7 % |`
- **T1** `| `vers` | 94.5 % | 91.1 % | -3.4 % |`
- **T1** `| `point` | 95.7 % | 94.3 % | -1.4 % |`
- **T1** `| `chemin_0` | 78.6 % | 81.4 % | 2.9 % |`
- **T1** `| `de` | 93.6 % | 93.6 % | 93.4 % | 92.7 % | 0.2 % | 1/0, p = 1 |`
- **T1** `| `vers` | 94.3 % | 93.8 % | 93.8 % | 94.3 % | 0.0 % | 1/1, p = 1 |`
- **T1** `| `point` | 95.7 % | 65.2 % ± 51.5 %* | 72.9 % | 94.8 % | -7.6 % | 0/16, p = 3.05e-05 |`
- **T1** `| `chemin_0` | 83.3 % | 82.9 % | 84.3 % | 82.9 % | -1.4 % | 0/3, p = 0.25 |`
- **T1** ``*` `point` : la moyenne cache une divergence de la graine 3 (5,7 % ; graines 1-2 : 95,7 % et 94,3 %). La tête prédit alors la classe 39 pour presque tout ; le résultat `point` en contexte n'est pas i`
- **T1** `**Bilan contrasté.** Sur les champs dorsaux, le contexte **n'apporte rien** : `de` est identique, `vers`/`chemin_0` bougent de moins d'un point, et permuter ou vider le contexte ne dégrade pas signifi`
- **T1** `- **`chemin_0` ne fait pas mieux qu'un prédicteur majoritaire, et son macro-rappel est au niveau du hasard** : 83,3 % global contre 97,1 % de majorité, macro-rappel 0,286 contre 1/3 au hasard. Les sur`
- **T1** `- **`point` est non concluant** : 95,7 % global, en dessous de la majorité (97,1 %). La macro-rappel (0,657) vient de la classe D5 (1 item, surface vue) et de D4 ; la classe 30 (`B[dd]`, surface inédi`
- **T1** `- **`vers` : plafond de couverture** : 7 items sur 146 ont une classe absente du synthétique (roque, `exd6`, promotion). Ils sont à 0 par construction ; le maximum atteignable est 95,2 %. Le résultat `
- **T1** `- **Recouvrement de templates** : 86,3 % des surfaces réelles de `de`/`vers` sont déjà vues après normalisation. Sur le prototype d'origine, `de` fait 126/126 sur ces surfaces et 10/20 sur les inédite`
- **T1** `1. `vers` est **linéairement décodable** par l'encodeur gelé : 94,3 % global, 100 % sur les surfaces vues, 11,7/13 (89,7 %) sur les inédites couvertes. C'est le champ dorsal le plus solide avec `de`.`
- **T1** `2. `de` est reproduit (93,6 % ; 93,2 % sur le prototype d'origine) ; le dernier état est le porteur principal de l'information, mais la moyenne seule n'est pas vide : à convergence, elle atteint 89,7 `
- **T1** `3. Le **contexte RSN n'apporte rien aux champs dorsaux** ; il aide l'action comme identifiant de jeu (93,6 % vs 87,4 %, chute à 26,1 % si permuté). Le test reste sous-alimenté par des contextes consta`
- **T1** `| `de` | 146 | 20 | 13 | {52: 6, 62: 6, 60: 4, 28: 1, 8: 2, 57: 1} | 65.0 % |`
- **T1** `| `vers` | 146 | 20 | 13 | {36: 6, 45: 6, 62: 2, 58: 2, 19: 1, 0: 2, 42: 1} | 65.0 % |`
- **T1** `| `point` | 70 | 4 | 4 | {48: 3, 30: 1} | 100.0 % |`
- **T1** `| `chemin_0` | 70 | 14 | 13 | {8: 12, 21: 1, 9: 1} | 92.9 % |`
- **T1** `| `baseline-1000` | 92.7 % ± 1.0 % | 100.0 % (126/146) | 46.7 % (9.3/20) | 71.8 % (9.3/13) | — (—) | 91.6 % |`
- **T1** `| `aug-formes` | 95.2 % ± 0.0 % | 100.0 % (126/146) | 65.0 % (13.0/20) | 100.0 % (13.0/13) | — (—) | 92.9 % |`
- **T1** `| `aug-pos` | 92.2 % ± 1.0 % | 100.0 % (126/146) | 43.3 % (8.7/20) | 46.2 % (6.0/13) | 38.1 % (2.7/7) | 95.9 % |`
- **T1** `| `aug-pos-mean` | 91.8 % ± 0.0 % | 100.0 % (126/146) | 40.0 % (8.0/20) | 38.5 % (5.0/13) | 42.9 % (3.0/7) | 95.2 % |`
- **T1** `| `aug-pos-last` | 94.5 % ± 0.0 % | 100.0 % (126/146) | 60.0 % (12.0/20) | 69.2 % (9.0/13) | 42.9 % (3.0/7) | 93.8 % |`
- **T1** `| `aug-pos-ctx` | 95.2 % ± 0.0 % | 100.0 % (126/146) | 65.0 % (13.0/20) | 100.0 % (13.0/13) | 0.0 % (0.0/7) | 98.6 % |`
- **T1** `| `aug-pos-norm` | 91.8 % ± 0.0 % | 100.0 % (128/146) | 33.3 % (6.0/18) | 27.3 % (3.0/11) | 42.9 % (3.0/7) | 94.5 % |`
- **T1** `| `francais` | 4 | 50.0 % | 50.0 % | 25.0 % |`
- **T1** `| `san` | 11 | 30.3 % | 63.6 % | 42.4 % |`
- **T1** `| `uci` | 5 | 80.0 % | 80.0 % | 60.0 % |`
- **T1** `| `baseline-1000` | 94.3 % ± 0.4 % | 100.0 % (126/146) | 58.3 % (11.7/20) | 89.7 % (11.7/13) | — (—) | 91.6 % |`
- **T1** `| `aug-formes` | 93.8 % ± 0.0 % | 100.0 % (126/146) | 55.0 % (11.0/20) | 84.6 % (11.0/13) | — (—) | 92.9 % |`
- **T1** `| `aug-pos` | 95.4 % ± 0.4 % | 100.0 % (126/146) | 66.7 % (13.3/20) | 84.6 % (11.0/13) | 33.3 % (2.3/7) | 95.9 % |`
- **T1** `| `aug-pos-mean` | 50.0 % ± 0.0 % | 51.6 % (126/146) | 40.0 % (8.0/20) | 46.2 % (6.0/13) | 28.6 % (2.0/7) | 95.2 % |`
- **T1** `| `aug-pos-last` | 96.6 % ± 0.0 % | 100.0 % (126/146) | 75.0 % (15.0/20) | 92.3 % (12.0/13) | 42.9 % (3.0/7) | 93.8 % |`
- **T1** `| `aug-pos-ctx` | 94.5 % ± 0.0 % | 100.0 % (126/146) | 60.0 % (12.0/20) | 84.6 % (11.0/13) | 14.3 % (1.0/7) | 98.6 % |`
- **T1** `| `aug-pos-norm` | 95.2 % ± 0.0 % | 100.0 % (128/146) | 61.1 % (11.0/18) | 81.8 % (9.0/11) | 28.6 % (2.0/7) | 94.5 % |`
- **T1** `| `francais` | 4 | 50.0 % | 50.0 % | 50.0 % |`
- **T1** `| `san` | 11 | 51.5 % | 45.5 % | 63.6 % |`
- **T1** `| `uci` | 5 | 80.0 % | 80.0 % | 86.7 % |`
- **T1** `| `baseline-1000` | 95.7 % ± 0.0 % | 100.0 % (66/70) | 25.0 % (1.0/4) | 25.0 % (1.0/4) | — (—) | 98.6 % |`
- **T1** `| `aug-formes` | 96.7 % ± 0.8 % | 100.0 % (66/70) | 41.7 % (1.7/4) | 41.7 % (1.7/4) | — (—) | 100.0 % |`
- **T1** `| `aug-pos` | 97.1 % ± 0.0 % | 100.0 % (66/70) | 50.0 % (2.0/4) | 50.0 % (2.0/4) | — (—) | 99.5 % |`
- **T1** `| `aug-pos-mean` | 5.7 % ± 0.0 % | 6.1 % (66/70) | 0.0 % (0.0/4) | 0.0 % (0.0/4) | — (—) | 98.6 % |`
- **T1** `| `aug-pos-last` | 97.1 % ± 0.0 % | 100.0 % (66/70) | 50.0 % (2.0/4) | 50.0 % (2.0/4) | — (—) | 97.1 % |`
- **T1** `| `aug-pos-ctx` | 95.7 % ± 0.0 % | 100.0 % (66/70) | 25.0 % (1.0/4) | 25.0 % (1.0/4) | — (—) | 100.0 % |`
- **T1** `| `aug-pos-norm` | 97.1 % ± 0.0 % | 100.0 % (66/70) | 50.0 % (2.0/4) | 50.0 % (2.0/4) | — (—) | 100.0 % |`
- **T1** `| `gtp` | 3 | 33.3 % | 55.6 % | 66.7 % |`
- **T1** `| `sgf` | 1 | 0.0 % | 0.0 % | 0.0 % |`
- **T1** `| `baseline-1000` | 81.0 % ± 2.2 % | 98.8 % (56/70) | 9.5 % (1.3/14) | 10.3 % (1.3/13) | — (—) | 81.4 % |`
- **T1** `| `aug-formes` | 88.1 % ± 2.2 % | 99.4 % (56/70) | 42.9 % (6.0/14) | 46.2 % (6.0/13) | — (—) | 84.3 % |`
- **T1** `| `aug-pos` | 86.7 % ± 5.0 % | 97.6 % (56/70) | 42.9 % (6.0/14) | 38.5 % (5.0/13) | 100.0 % (1.0/1) | 90.5 % |`
- **T1** `| `aug-pos-mean` | 90.0 % ± 0.0 % | 98.2 % (56/70) | 57.1 % (8.0/14) | 61.5 % (8.0/13) | 0.0 % (0.0/1) | 88.6 % |`
- **T1** `| `aug-pos-last` | 85.7 % ± 0.0 % | 96.4 % (56/70) | 42.9 % (6.0/14) | 46.2 % (6.0/13) | 0.0 % (0.0/1) | 91.4 % |`
- **T1** `| `aug-pos-ctx` | 92.9 % ± 0.0 % | 100.0 % (56/70) | 64.3 % (9.0/14) | 61.5 % (8.0/13) | 100.0 % (1.0/1) | 90.0 % |`
- **T1** `| `aug-pos-norm` | 84.3 % ± 0.0 % | 100.0 % (56/70) | 21.4 % (3.0/14) | 15.4 % (2.0/13) | 100.0 % (1.0/1) | 92.9 % |`
- **T1** `| `algebrique` | 2 | 16.7 % | 50.0 % | 83.3 % |`
- **T1** `| `francais` | 1 | 66.7 % | 100.0 % | 0.0 % |`
- **T1** `| `numerique` | 11 | 3.0 % | 36.4 % | 39.4 % |`
- **T1** `**Lecture des ablations (1 graine).** `mean` seul s'effondre : vers inédit 40.0 % (global 50.0 %), point inédit 0.0 % (global 5.7 %) ; `last` est le meilleur sur vers inédit 75.0 % (15.0/20), donc le `
- **T1** `| `de` | 46.7 % (9.3/20) | 65.0 % (13.0/20) | 43.3 % (8.7/20) | +18.3 pts | -3.3 pts |`
- **T1** `| `vers` | 58.3 % (11.7/20) | 55.0 % (11.0/20) | 66.7 % (13.3/20) | -3.3 pts | +8.3 pts |`
- **T1** `| `point` | 25.0 % (1.0/4) | 41.7 % (1.7/4) | 50.0 % (2.0/4) | +16.7 pts | +25.0 pts |`
- **T1** `| `chemin_0` | 9.5 % (1.3/14) | 42.9 % (6.0/14) | 42.9 % (6.0/14) | +33.3 pts | +33.3 pts |`
- **T1** `- **`point` et `chemin_0` sont dominés par la majorité** (97,1 %) : leur exactitude globale ne distingue pas un décodeur d'un prédicteur majoritaire. Seuls les sous-ensembles inédits et le macro-rappe`
- **T1** `| **M5** contexte | `source`, ordre 1, split 80/20 par partie, 160 parties test | **18,70 %** (majoritaire 6,49 %) ; surprise **2,423** vs **3,539** |`
- **T1** `| **M5** sans contexte | même split | **12,60 %** ; surprise **3,112** |`
- **T1** `| **M6** | conjonction 88 essais | **94,32 %** (base 75 %) |`
- **T1** `| **M6** | tâche sens/langue 792 essais | **94,95 %** (base 50 %), commutation 0 |`
- **T1** `| **M8** | prototypes sur les 528 épisodes (non tenus à l'écart) | champs **96,14 %**, exact **57,95 %**, 7 prototypes |`
- **T1** `| **M9** | M1 sans contexte | **70,83 %** |`
- **T1** `- **M8** est mesuré **sur les épisodes stockés** : 57,95 % d'exact ne dit rien de la généralisation ;`
- **T1** `| action | 1 | sans | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |`
- **T1** `| action | 1 | masque_uniforme | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |`
- **T1** `| action | 1 | masque_hist | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |`
- **T1** `| action | 1 | masque_melange | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |`
- **T1** `| action | 2 | sans | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |`
- **T1** `| action | 2 | masque_uniforme | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |`
- **T1** `| action | 2 | masque_hist | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |`
- **T1** `| action | 2 | masque_melange | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |`
- **T1** `| source | 1 | sans | 843 | 10.6 % | 5.7 % | 3.224 | +0.376 | +0.000 | +0.000 |`
- **T1** `| source | 1 | masque_uniforme | 843 | 8.0 % | 5.7 % | 2.598 | +1.002 | +0.626 | -0.027 |`
- **T1** `| source | 1 | masque_hist | 843 | 16.5 % | 5.7 % | 2.686 | +0.914 | +0.539 | +0.059 |`
- **T1** `| source | 1 | masque_melange | 843 | 16.5 % | 5.7 % | 2.480 | +1.120 | +0.744 | +0.059 |`
- **T1** `| source | 2 | sans | 843 | 13.8 % | 5.7 % | 3.214 | +0.386 | +0.000 | +0.000 |`
- **T1** `| source | 2 | masque_uniforme | 843 | 8.0 % | 5.7 % | 2.598 | +1.002 | +0.617 | -0.058 |`
- … (tronqué)

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : /tmp/a1-m5-m6.json /tmp/a1-m5-m6.md /tmp/a2-m2-cpu.json /tmp/a2-m7-m8-m9.json /tmp/a2-m7-m8-m9.md /tmp/a2-m7-m8-m9-part1.md /tmp/a2-m7-m8-m9-part2.md /tmp/a2-m7-m8-m9-part3.md /tmp/a3-m2.json /tmp/a3-
- **T1** : [stderr] sed: can't read tools/jeux/codecs.py: No such file or directory [exit code: 2]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 37, in <module>   File "<stdin>", line 16, in ctx_depuis_resume ValueError: invalid literal for int() with base 10: 'e6' [exit code: 

