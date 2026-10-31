# Session 0b2c86eb — Dépôt /home/stephane/GitHub/Qtrinet, s

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `0b2c86eb-7a8d-4eed-a3dd-fb165f1a8630` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 10:29 |
| Durée | 1.5 h |
| Tours | 1 |
| Messages | 123 |
| Appels d'outils | 128 |
| Fichiers touchés | 5 |
| Commandes | 101 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Dépôt /home/stephane/GitHub/Qtrinet, sprint autonome 24 h. Sous-agent A5 : améliorer la GÉNÉRALISATION de M2 aux surfaces inédites, sans toucher aux autres modules.  État mesuré (A3) : - `tools/cerveau/voies.py` : encodeur `route` gelé, têtes ventrales (action) / dorsales (de, vers, point, chemin_0), pools mean/last/mean+last, contexte optionnel, lésions. - Sur 146 items `de` : `de` moyen 93,6 % s … [2037 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Dépôt /home/stephane/GitHub/Qtrinet, sprint autonome 24 h. Sous-agent A5 : améliorer la GÉNÉRALISATION de M2 aux surface … [2317 caractères tronqués]

*128 appels d'outils.* Actions notables :

- bash — List cerveau dir and count lines
- bash — Check git status and recent log
- read
- bash — List semantique modules and line counts
- bash — Check tmp artifacts and base model
- bash — Find reports mentioning voies and inédits
- bash — Read A3 report md
- bash — Read A3 driver script
- bash — Read rest of A3 driver
- bash — Inspect A3 partial JSON
- bash — Check GPU state and base model
- bash — List unseen test surfaces per field
- bash — Read base config and model module
- bash — Read entrainer main script
- … et 101 autres

**Synthèse produite :**

⏵ Clôture d'A5 : résultats, autocritique et fichiers livrés

**Livrables**
- `/tmp/a5-m2-generalisation.json` — 7 conditions, masques par graine, prédictions par item, verdict, autocritique, garde anti-fuite.
- `/tmp/a5-m2-generalisation.md` — rapport complet.
- Dispositif : `/tmp/a5_driver.py`, `/tmp/a5_finalize.py`, `/tmp/a5_md.py` ; logs `/tmp/a5-main.log`, `/tmp/a5-ablations.log`.

**Code (uniquement les 2 fichiers autorisés)**
`tools/cerveau/voies.py` et `tools/cerveau/tests/test_voies.py` : `augmenter()` (templates UCI/SAN français/NLP, dames numérique-algébrique, go SGF/français, positions variées), `normaliser_coordonnees()`, paramètres `augmentation/positions/exclure_surfaces/normaliseur`, mémoïsation de `normaliser`. Rétro-compatible ; tests `test_voies` **8/8 OK**, `py_compile` OK. Aucun git de ma part.

**Résultats (1 000 pas, 3 graines, split inédit A3 gelé)**

| champ | baseline | aug-formes | aug-pos |
|---|---:|---:|---:|
| `de` | 9,3/20 | **13/20 (+18,3 pts)** | 8,7/20 (−3,3) |
| `vers` | 11,7/20 | 11/20 (−3,3) | **13,3/20 (+8,3)** |
| `point` | 1/4 | 1,7/4 (+16,7) | **2/4 (+25,0)** |
| `chemin_0` | 1,3/14 | **6/14 (+33,3)** | 6/14 (+33,3) |

La garde anti-fuite tient : `surfaces_train == surfaces_syn` partout, **0 surface réelle générée**, `vu` identique dans toutes les conditions.

**Verdict autocritique**
- Gain réel sur `chemin_0`, `point` et une partie de `de` ; **pas de gain uniforme** (`vers` négatif avec les templates seuls).
- Le split `de`/`vers` de A3 est trompeur : 13 inédits couverts, 3 classes, un prior par famille suffit à ~12/13. `aug-pos` **désapprend** les raccourcis `e4→52`/`Nf3→62` et baisse, tout en lisant par la règle les promotions `a8=Q`/`a7a8q` (0/3 → 3/3 des deux côtés) et `exd6` (2/3 sur `de`).
- Ablations 1 graine : mean s'effondre (`vers` 40 %, `point` 0 %) ; last meilleur sur `vers` (75 %) ; contexte +15 pts sur `de` mais −25 sur `point` ; normalisation agressive = négatif net (split 18/20, résidu `de` 33,3 %, `chemin` 21,4 %).
- Limites : roque 0/3 (surface unique exclue), `9x18x27` 0, McNemar pseudo-répliqué, pas de label-shuffle. L'échec `test_m8_sommeil` de la suite complète vient d'un autre agent (`sommeil.py`/`lesion.py`), pas de M2.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py` | 0 | 8 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_voies.py` | 0 | 2 |
| `/tmp/a5_driver.py` | 1 | 0 |
| `/tmp/a5_md.py` | 1 | 0 |
| `/tmp/a5_finalize.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** List cerveau dir and count lines
- **T1** Check git status and recent log
- **T1** List semantique modules and line counts
- **T1** Check tmp artifacts and base model
- **T1** Find reports mentioning voies and inédits
- **T1** Read A3 report md
- **T1** Read A3 driver script
- **T1** Read rest of A3 driver
- **T1** Inspect A3 partial JSON
- **T1** Check GPU state and base model
- **T1** List unseen test surfaces per field
- **T1** Read base config and model module
- **T1** Read entrainer main script
- **T1** Summarize A3 json meta and timing
- **T1** Inspect unseen items with contexts
- **T1** Inspect unseen items with contexts
- **T1** Read chess rules module part 1
- **T1** List chess/dames APIs
- **T1** Check partial JSON structure
- **T1** Find voies usages and read SAN/dames coup APIs
- **T1** Check lexique and go APIs
- **T1** Search SGF handling in jeux
- **T1** Show real/synth surface motifs per field
- **T1** Read go/dames/chess RSN helpers
- **T1** Read dames applique
- **T1** Benchmark 50 train steps and evaluation
- **T1** Read normalise_forme
- **T1** Check dames coordinate helpers and departure moves
- **T1** Thread normaliseur through evaluation functions
- **T1** Prototype augmentation and normalize
- **T1** Check running python process CPU
- **T1** Profile normaliser and imports with traceback dump
- **T1** Profile augmenter with traceback dump
- **T1** Profile positions augmentation
- **T1** Check augmentation coverage, leakage, examples
- **T1** Fix tests and run unit test suite
- **T1** Rewrite augmentation test and rerun
- **T1** Run voies tests verbosely
- **T1** Fix expected concept case and rerun voies tests
- **T1** Show concise test failure
- … et 61 autres

## 4. Mesures et résultats marquants

- **T1** `d28ad551 B12 — PIPELINE M1→M4→M8 : 528/528, COMPLÉTION 96,3 %, 7 PROTOTYPES (DOCS)`
- **T1** `b563a155 B12 — PIPELINE M1→M4→M8 : 528/528, COMPLÉTION 96,3 %, PROTOYPES 7`
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
- **T1** `ad("Le recouvrement de surface est le point critique : `de` et `vers` ont 86,3 % de "`
- **T1** `"leurs surfaces réelles déjà vues sous forme normalisée, `point` 94,3 %, "`
- **T1** `"`chemin_0` 80,0 %. L'exactitude globale est donc **gonflée par la mémoire de "`
- **T1** `ad("*Lecture.* `vers` est **décodable** : 94,5 % global, 100 % sur les 126 surfaces vues, "`
- **T1** `"de couverture est 95,2 %. `de` reproduit le résultat d'origine (93,8 % contre 93,2 %). "`
- **T1** `"hasard (1/8 = 12,5 %) sans toucher le champ dorsal ; la lésion dorsale fait tomber "`
- **T1** `"(de 48,0 %, vers 50,0 %, point 4,3 %). Ce n'est pas une absence d'information : "`
- **T1** `"une sonde linéaire sur les mêmes features moyennes atteint 89,7 % sur `de` après "`
- **T1** `"1 000 pas (et seulement 50,7 % après 300 pas). La moyenne a une variance "`
- **T1** `Quadro RTX 5000, 4 MiB, 16384 MiB, 0 %`
- **T1** `Quadro RTX 5000, 124 MiB, 16384 MiB, 0 %`
- **T1** `"vu": "126/126 = 100 %",`
- **T1** `Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 947.82it/s]`
- **T1** `[still running after 60000ms; moved to background job bash-1745]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 922.34it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1034.74it/s]`
- **T1** `| `de` | 146 | 20 | 13 | {52: 6, 62: 6, 60: 4, 28: 1, 8: 2, 57: 1} | 65.0 % |`
- **T1** `| `vers` | 146 | 20 | 13 | {36: 6, 45: 6, 62: 2, 58: 2, 19: 1, 0: 2, 42: 1} | 65.0 % |`
- **T1** `| `point` | 70 | 4 | 4 | {48: 3, 30: 1} | 100.0 % |`
- **T1** `| `chemin_0` | 70 | 14 | 13 | {8: 12, 21: 1, 9: 1} | 92.9 % |`
- **T1** `| `baseline-1000` | 92.7 % ± 1.0 % | 100.0 % | 46.7 % | 71.8 % | — | 91.6 % |`
- **T1** `| `francais` | 4 | 50.0 % |`
- **T1** `| `san` | 11 | 30.3 % |`
- **T1** `| `uci` | 5 | 80.0 % |`
- **T1** `| `baseline-1000` | 94.3 % ± 0.4 % | 100.0 % | 58.3 % | 89.7 % | — | 91.6 % |`
- **T1** `| `san` | 11 | 51.5 % |`
- **T1** `| `baseline-1000` | 95.7 % ± 0.0 % | 100.0 % | 25.0 % | 25.0 % | — | 98.6 % |`
- **T1** `| `gtp` | 3 | 33.3 % |`
- **T1** `| `sgf` | 1 | 0.0 % |`
- **T1** `| `baseline-1000` | 81.0 % ± 2.2 % | 98.8 % | 9.5 % | 10.3 % | — | 81.4 % |`
- **T1** `| `algebrique` | 2 | 16.7 % |`
- **T1** `| `francais` | 1 | 66.7 % |`
- **T1** `| `numerique` | 11 | 3.0 % |`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 981.01it/s]`
- **T1** `| `baseline-1000` | 92.7 % ± 1.0 % | 100.0 % | 46.7 % (9.3/20) | 71.8 % (9.3/13) | — (—) | 91.6 % |`
- **T1** `| `aug-formes` | 95.2 % ± 0.0 % | 100.0 % | 65.0 % (13.0/20) | 100.0 % (13.0/13) | — (—) | 92.9 % |`
- **T1** `| `aug-pos` | 92.2 % ± 1.0 % | 100.0 % | 43.3 % (8.7/20) | 46.2 % (6.0/13) | 38.1 % (2.7/7) | 95.9 % |`
- **T1** `| `francais` | 4 | 50.0 % | 50.0 % | 25.0 % |`
- **T1** `| `san` | 11 | 30.3 % | 63.6 % | 42.4 % |`
- **T1** `| `uci` | 5 | 80.0 % | 80.0 % | 60.0 % |`
- **T1** `269-       "`chemin_0` sont dominés par la majorité (97,1 %) ; leur exactitude globale ne "`
- **T1** `| `de` | 46.7 % (9.3/20) | 65.0 % (13.0/20) | 43.3 % (8.7/20) | +18.3 pts | -3.3 pts |`
- **T1** `| `vers` | 58.3 % (11.7/20) | 55.0 % (11.0/20) | 66.7 % (13.3/20) | -3.3 pts | +8.3 pts |`
- **T1** `| `point` | 25.0 % (1.0/4) | 41.7 % (1.7/4) | 50.0 % (2.0/4) | +16.7 pts | +25.0 pts |`
- **T1** `| `chemin_0` | 9.5 % (1.3/14) | 42.9 % (6.0/14) | 42.9 % (6.0/14) | +33.3 pts | +33.3 pts |`
- **T1** `- **`point` et `chemin_0` sont dominés par la majorité** (97,1 %) : leur exactitude globale ne distingue pas un décodeur d'un prédicteur majoritaire. Seuls les sous-ensembles inédits et le macro-rappe`
- **T1** `37:| `aug-pos-mean` | 91.8 % ± 0.0 % | 100.0 % | 40.0 % (8.0/20) | 38.5 % (5.0/13) | 42.9 % (3.0/7) | 95.2 % |`
- **T1** `38:| `aug-pos-last` | 94.5 % ± 0.0 % | 100.0 % | 60.0 % (12.0/20) | 69.2 % (9.0/13) | 42.9 % (3.0/7) | 93.8 % |`
- **T1** `39:| `aug-pos-ctx` | 95.2 % ± 0.0 % | 100.0 % | 65.0 % (13.0/20) | 100.0 % (13.0/13) | 0.0 % (0.0/7) | 98.6 % |`
- **T1** `40:| `aug-pos-norm` | 91.8 % ± 0.0 % | 100.0 % | 33.3 % (6.0/18) | 27.3 % (3.0/11) | 42.9 % (3.0/7) | 94.5 % |`
- **T1** `92:| `aug-pos-mean` | 50.0 % ± 0.0 % | 51.6 % | 40.0 % (8.0/20) | 46.2 % (6.0/13) | 28.6 % (2.0/7) | 95.2 % |`
- **T1** `93:| `aug-pos-last` | 96.6 % ± 0.0 % | 100.0 % | 75.0 % (15.0/20) | 92.3 % (12.0/13) | 42.9 % (3.0/7) | 93.8 % |`
- **T1** `94:| `aug-pos-ctx` | 94.5 % ± 0.0 % | 100.0 % | 60.0 % (12.0/20) | 84.6 % (11.0/13) | 14.3 % (1.0/7) | 98.6 % |`
- **T1** `95:| `aug-pos-norm` | 95.2 % ± 0.0 % | 100.0 % | 61.1 % (11.0/18) | 81.8 % (9.0/11) | 28.6 % (2.0/7) | 94.5 % |`
- **T1** `147:| `aug-pos-mean` | 5.7 % ± 0.0 % | 6.1 % | 0.0 % (0.0/4) | 0.0 % (0.0/4) | — (—) | 98.6 % |`
- **T1** `148:| `aug-pos-last` | 97.1 % ± 0.0 % | 100.0 % | 50.0 % (2.0/4) | 50.0 % (2.0/4) | — (—) | 97.1 % |`
- **T1** `**Lecture des ablations (1 graine).** `mean` seul s'effondre : vers inédit 40.0 % (global 50.0 %), point inédit 0.0 % (global 5.7 %) ; `last` est le meilleur sur vers inédit 75.0 % (15.0/20), donc le `
- **T1** `"negatif": "Pas de gain uniforme : vers ne gagne pas avec les templates seuls (-3,3 pts) ; aug-pos perd 4,3 pts sur de par rapport à la baseline ; le roque reste 0/3 (surface unique exclue) ; point et`
- **T1** `| `baseline-1000` | 92.7 % ± 1.0 % | 100.0 % (126/146) | 46.7 % (9.3/20) | 71.8 % (9.3/13) | — (—) | 91.6 % |`
- **T1** `| `aug-formes` | 95.2 % ± 0.0 % | 100.0 % (126/146) | 65.0 % (13.0/20) | 100.0 % (13.0/13) | — (—) | 92.9 % |`
- **T1** `| `aug-pos` | 92.2 % ± 1.0 % | 100.0 % (126/146) | 43.3 % (8.7/20) | 46.2 % (6.0/13) | 38.1 % (2.7/7) | 95.9 % |`
- **T1** `| `aug-pos-mean` | 91.8 % ± 0.0 % | 100.0 % (126/146) | 40.0 % (8.0/20) | 38.5 % (5.0/13) | 42.9 % (3.0/7) | 95.2 % |`
- **T1** `| `aug-pos-last` | 94.5 % ± 0.0 % | 100.0 % (126/146) | 60.0 % (12.0/20) | 69.2 % (9.0/13) | 42.9 % (3.0/7) | 93.8 % |`
- **T1** `| `aug-pos-ctx` | 95.2 % ± 0.0 % | 100.0 % (126/146) | 65.0 % (13.0/20) | 100.0 % (13.0/13) | 0.0 % (0.0/7) | 98.6 % |`
- **T1** `| `aug-pos-norm` | 91.8 % ± 0.0 % | 100.0 % (128/146) | 33.3 % (6.0/18) | 27.3 % (3.0/11) | 42.9 % (3.0/7) | 94.5 % |`

## 5. Erreurs rencontrées

5 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 2, in <module> ModuleNotFoundError: No module named 'semantique' [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "/tmp/a5_md.py", line 246, in <module>     raise SystemExit(main())                      ~~~~^^   File "/tmp/a5_md.py", line 75, in main     syn = {f
- **T1** : Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 981.01it/s] [aug-pos-mean] 11:38:38 [exit code: 2]
- **T1** : Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 981.01it/s] [aug-pos-mean] 11:40:59 [exit code: 2]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 2, in <module> ModuleNotFoundError: No module named 'semantique' [exit code: 1]

