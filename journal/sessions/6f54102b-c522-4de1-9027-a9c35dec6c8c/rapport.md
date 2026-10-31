# Session 6f54102b — Nous sommes dans /home/stephane/GitHub/Q

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `6f54102b-c522-4de1-9027-a9c35dec6c8c` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 09:41 |
| Durée | 0.8 h |
| Tours | 1 |
| Messages | 67 |
| Appels d'outils | 69 |
| Fichiers touchés | 2 |
| Commandes | 51 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Nous sommes dans /home/stephane/GitHub/Qtrinet (dépôt Drave). Sprint autonome 24 h. Tu es un sous-agent chargé d'étendre M2 (voies ventrales/dorsales) du prototype `tools/cerveau/`.  État actuel mesuré : - M2 `tools/cerveau/voies.py` : encodeur `route` gelé, moyenne + dernier état caché ; entraînement synthétique 300 pas ; test sur 146 surfaces réelles. - Résultat : `action` 98,6 %, `de` 93,2 % ;  … [1815 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Nous sommes dans /home/stephane/GitHub/Qtrinet (dépôt Drave). Sprint autonome 24 h. Tu es un sous-agent chargé d'étendre … [2095 caractères tronqués]

*69 appels d'outils.* Actions notables :

- bash — List repo and cerveau directories
- bash — Check file sizes
- read
- bash — List cerveau tests
- bash — Find M2 usage in batterie
- bash — Read universaux CHAMPS
- bash — Read M2 batterie function
- bash — Read synth corpus head
- bash — Read typed corpus
- bash — Check model dir and GPU env
- bash — Read config, normalisation, tests
- bash — Corpus field statistics
- bash — Inspect real/synth fields and contexts
- bash — Find all references to voies module
- … et 44 autres

**Synthèse produite :**

⏵ Bilan M2 : vers décodable, point/chemin négatifs, rapport écrit

\## Ce qui a été fait

- `tools/cerveau/voies.py` étendu : têtes dorsales multiples (`de`, `vers`, `point`, `chemin_0`), pools `mean` / `last` / `mean+last`, contexte RSN, lésions ventrale/dorsale, évaluation par champ et split vu/inédit.
- `tools/cerveau/tests/test_voies.py` ajouté : 6 tests, tous verts.
- Livrables : **`/tmp/a3-m2.json`**, **`/tmp/a3-m2.md`** (brut : `/tmp/a3-m2-partial.json`).
- Le chemin historique M2 reproduit exactement : `action` 98,63 %, `de` 93,15 %, n = 146.

\## Chiffres principaux (`mean+last`, 300 pas, 3 graines)

| champ | n | exact | majorité | macro | surfaces vues | inédit couvert |
|---|---:|---:|---:|---:|---:|---:|
| `vers` | 146 | **94,3 %** ± 0,4 | 47,3 % | 37,4 % | 100 % (126) | 89,7 % (11,7/13) |
| `de` | 146 | **93,6 %** ± 0,4 | 47,9 % | 33,0 % | 100 % (126) | 82,1 % (10,7/13) |
| `point` | 70 | 95,7 % | **97,1 %** | 65,7 % | 100 % (66) | 25,0 % (1/4) |
| `chemin_0` | 70 | 83,3 % | **97,1 %** | **28,6 %** | 99,4 % (56) | 20,5 % (2,7/13) |

- `vers` est décodable ; son plafond de couverture est 95,2 % (7 items de classes jamais vues : roque, `exd6`, promotion).
- `point` est **non concluant** (sous la majorité, 68/70 items de la même classe).
- `chemin_0` est un **négatif net** : sous la majorité, macro-rappel au niveau du hasard.
- Lésions : ventrale → action 13-14 % (hasard 12,5 %), champs dorsaux intacts ; dorsale → champs 1-2 % (hasard 1,2-1,5 %), action intacte. Double dissociation nette, mais architecturale.

\## Ablations

- `mean` seul à 300 pas s'effondre (de 47,9 %, vers 50,0 %, point 4,3 %) par **sous-entraînement**, pas par absence d'information. À 1 000 pas : 89,7 / 91,1 / 94,3 / 81,4 ; `mean+last` à 1 000 pas : 92,5 / 94,5 / 95,7 / 78,6 (1 graine). Gain honnête du dernier état : **~+2,7 / +3,4 / +1,4 / −2,9 pts**.
- `last` seul égale `mean+last` sur `de`/`vers`/`point` et le dépasse sur `chemin_0` : la moyenne n'ajoute rien, voire nuit.
- Contexte : **aucun gain dorsal** ; il aide l'action comme identifiant de jeu (93,6 % vs 87,4 %), avec chute à 26,1 % si le contexte est permuté. La tête `point` en contexte a divergé sur une graine (5,7 %), moyenne non interprétable.

\## Autocritique majeure

Le 93,2 % d'origine sur `de` est **126/126 sur les surfaces déjà vues** et **10/20 sur les inédites** (3 graines : 10, 11, 10). Recouvrement des surfaces normalisées : 86,3 % (`de`/`vers`), 94,3 % (`point`), 80 % (`chemin_0`). Les chiffres globaux me
… [407 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py` | 1 | 1 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_voies.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** List repo and cerveau directories
- **T1** Check file sizes
- **T1** List cerveau tests
- **T1** Find M2 usage in batterie
- **T1** Read universaux CHAMPS
- **T1** Read M2 batterie function
- **T1** Read synth corpus head
- **T1** Read typed corpus
- **T1** Check model dir and GPU env
- **T1** Read config, normalisation, tests
- **T1** Corpus field statistics
- **T1** Inspect real/synth fields and contexts
- **T1** Find all references to voies module
- **T1** Read entrainer pad
- **T1** Real label distributions and normalised forms
- **T1** Inspect distributions and normalized test sets
- **T1** Reproduce baseline M2 and time it
- **T1** Compute surface overlap and class coverage
- **T1** Measure baseline seen vs unseen surface split
- **T1** Run baseline seen/unseen split
- **T1** Subset baselines and class distributions
- **T1** Per-item baseline predictions on unseen surfaces
- **T1** Time corpus generation
- **T1** Validate default path after refactor
- **T1** Quick 4-field run one seed
- **T1** One-seed ablation signals
- **T1** Probe mean vs last features
- **T1** Test mean feature convergence with minibatches
- **T1** Background mean+last 1000 steps
- **T1** Background mean-only 1000 steps
- **T1** Write experiment driver
- **T1** Patch driver for timebox
- **T1** Locate MD sections to patch
- **T1** Patch MD for 1000-step control
- **T1** Run 3-seed experiment driver
- **T1** Write preliminary JSON
- **T1** Write preliminary MD report
- **T1** Run new voies tests
- **T1** Inspect partial results
- **T1** Inspect seed results detail
- … et 11 autres

## 4. Mesures et résultats marquants

- **T1** `./run_quantify.py:274:        "faut que ~312 voies de MAC (≈ 9 400 ALM, 5 % du FPGA) pour saturer les 9,66 Go/s. "`
- **T1** `./run_sparsity.py:175:          "≈ 3 400 ALM pour 312 voies (**2 % du FPGA**) — c'est payable.",`
- **T1** `./run_precision.py:9:**mémoire** (312 voies suffisent à saturer la DDR3 ; 95 % du FPGA dort). Ajouter`
- **T1** `./run_precision.py:166:          "   passante. Le débit est fixé par la DDR3 (9,66 Go/s) ; 312 voies suffisent à la",`
- **T1** `./run_precision.py:174:          "   (mux + add/sub). Pour 312 voies : ~11 000 ALM, soit **6 % du FPGA** au lieu",`
- **T1** `Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 958.77it/s]`
- **T1** `de: n_test=146 surfaces_vues=126 (86.3%) paires_vues=126 (86.3%) classes 6 plafond_couverture=0.952 ctx_vides=0`
- **T1** `vers: n_test=146 surfaces_vues=126 (86.3%) paires_vues=126 (86.3%) classes 8 plafond_couverture=0.952 ctx_vides=0`
- **T1** `point: n_test=70 surfaces_vues=66 (94.3%) paires_vues=66 (94.3%) classes 3 plafond_couverture=1.000 ctx_vides=0`
- **T1** `chemin_0: n_test=70 surfaces_vues=56 (80.0%) paires_vues=56 (80.0%) classes 3 plafond_couverture=0.986 ctx_vides=0`
- **T1** `chemin_1: n_test=70 surfaces_vues=56 (80.0%) paires_vues=56 (80.0%) classes 3 plafond_couverture=0.886 ctx_vides=0`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 913.24it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 932.18it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 971.00it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1028.33it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1054.79it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 944.09it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1098.12it/s]`
- **T1** `| `de` | 146 | 93.6 % ± 0.4 % | 47.9 % | 1.5 % | 33.0 % | 100.0 % (126) | 53.3 % (20) | 82.1 % (13) |`
- **T1** `| `vers` | 146 | 94.3 % ± 0.4 % | 47.3 % | 1.5 % | 37.4 % | 100.0 % (126) | 58.3 % (20) | 89.7 % (13) |`
- **T1** `| `point` | 70 | 95.7 % ± 0.0 % | 97.1 % | 1.2 % | 65.7 % | 100.0 % (66) | 25.0 % (4) | 25.0 % (4) |`
- **T1** `| `chemin_0` | 70 | 83.3 % ± 0.8 % | 97.1 % | 1.5 % | 28.6 % | 99.4 % (56) | 19.0 % (14) | 20.5 % (13) |`
- **T1** `*Lecture.* `vers` est **décodable** : 94,3 % global, 100 % sur les 126 surfaces vues, et 11,7/13 (89,7 %) sur les surfaces inédites dont la classe est couverte. Les 7 items de classes jamais vues (roq`
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
- **T1** `- **`chemin_0` reste au hasard, et même en dessous de la majorité** : 83,3 % global contre 97,1 % de majorité, macro-rappel 0,286 contre 1/3 au hasard. Les surfaces réelles inédites (`9x18`, `b6xd4`, `
- **T1** `- **`point` est non concluant** : 95,7 % global, en dessous de la majorité (97,1 %). La macro-rappel (0,657) vient de la classe D5 (1 item, surface vue) et de D4 ; la classe 30 (`B[dd]`, surface inédi`
- **T1** `- **`vers` : plafond de couverture** : 7 items sur 146 ont une classe absente du synthétique (roque, `exd6`, promotion). Ils sont à 0 par construction ; le maximum atteignable est 95,2 %. Le résultat `
- **T1** `- **Recouvrement de templates** : 86,3 % des surfaces réelles de `de`/`vers` sont déjà vues après normalisation. Sur le prototype d'origine, `de` fait 126/126 sur ces surfaces et 10/20 sur les inédite`
- **T1** `1. `vers` est **linéairement décodable** par l'encodeur gelé : 94,3 % global, 100 % sur les surfaces vues, 11,7/13 (89,7 %) sur les inédites couvertes. C'est le champ dorsal le plus solide avec `de`.`
- **T1** `2. `de` est reproduit (93,6 % ; 93,2 % sur le prototype d'origine) ; le dernier état est le porteur principal de l'information, mais la moyenne seule n'est pas vide : à convergence, elle atteint 89,7 `
- **T1** `3. Le **contexte RSN n'apporte rien aux champs dorsaux** ; il aide l'action comme identifiant de jeu (93,6 % vs 87,4 %, chute à 26,1 % si permuté). Le test reste sous-alimenté par des contextes consta`
- **T1** `"chemin_0": "83,3 % < majorité 97,1 % ; macro 0,286 < 1/3 ; inédit 19,0 % ; négatif net.",`
- **T1** `"point": "95,7 % < majorité 97,1 % ; macro 0,657 ; inédit 25 % ; non concluant (68/70 même classe).",`
- **T1** `"vers": "94,3 % ; plafond de couverture 95,2 % ; 7 items de classes inconnues à 0 ; inédit couvert 89,7 % (11,7/13).",`
- **T1** `"contexte": "Aucun gain dorsal ; le contexte aide l'action (93,6 % vs 87,4 %) comme identifiant de jeu, et le permuter fait tomber l'action à 26,1 %. La tête point du modèle contexte a divergé sur la `
- **T1** `"de_global": "93,2 % d'origine = 126/126 sur surfaces vues + 10/20 sur inédites (3 graines) : chiffre global gonflé par le recouvrement de templates."`
- **T1** `"Le recouvrement de surfaces normalisées est de 86,3 % pour de/vers, 94,3 % pour point, 80 % pour chemin_0 : l'exactitude globale mesure surtout la mémoire de templates.",`
- **T1** `"À 300 pas, mean seul est sous-entraîné (variance inter-exemples faible) ; à 1 000 pas il atteint 89,7 % sur de. La comparaison à pas égal exagère le gain du dernier état ; à 1 000 pas le gain de mean`
- **T1** `"Le contexte synthétique est constant par jeu (position de départ) : l'ablation ne teste pas un contexte de position. Il aide néanmoins l'action comme identifiant de jeu (93,6 % vs 87,4 %), pas les ch`
- **T1** `"La tête point du modèle contexte a divergé sur une graine (5,7 %) : les moyennes d'exactitude sur 3 graines masquent cette instabilité ; il faut regarder les graines.",`
- **T1** `"note": "Graine 3 divergée : la tête point prédit la classe 39 pour presque tout (rappel D4 = 4,4 %). Les graines 1-2 sont à 95,7 % et 94,3 %. La moyenne 65,2 % ± 51,5 % n'est pas interprétable."`
- **T1** `"note": "Le contexte est utilisé par la voie ventrale comme identifiant de jeu : permuté, l'action tombe à 26,1 % ; vide, à 43,6 %. Les champs dorsaux, eux, ne changent pas (de/vers) : le contexte n'a`
- **T1** `Loading weights:  96%|█████████▌| 86/90 [00:00<00:00, 859.12it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 893.16it/s]`
- **T1** `98:- **`chemin_0` ne fait pas mieux qu'un prédicteur majoritaire, et son macro-rappel est au niveau du hasard** : 83,3 % global contre 97,1 % de majorité, macro-rappel 0,286 contre 1/3 au hasard. Les `

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : =============== de n 146 classes 6   distrib [(52, 70), (62, 68), (60, 4), (8, 2), (28, 1), (57, 1)] [stderr] Traceback (most recent call last):   File "<stdin>", line 12, in <module> TypeError: objec
- **T1** : [stderr] Traceback (most recent call last):   File "/tmp/a3_baseline_split.py", line 6, in <module>     from semantique.typed_corpus import items, synth_corpus, octets ImportError: cannot import name 
- **T1** : md patch ok [exit code: 1]

