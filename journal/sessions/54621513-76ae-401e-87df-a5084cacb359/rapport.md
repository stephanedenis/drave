# Session 54621513 — Nous sommes dans /home/stephane/GitHub/Q

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `54621513-76ae-401e-87df-a5084cacb359` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 09:41 |
| Durée | 0.7 h |
| Tours | 1 |
| Messages | 74 |
| Appels d'outils | 78 |
| Fichiers touchés | 4 |
| Commandes | 65 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Nous sommes dans /home/stephane/GitHub/Qtrinet (dépôt Drave). Sprint autonome 24 h. Tu es un sous-agent chargé de M5 (codage prédictif) et M6 (gating/contrôle exécutif) du prototype `tools/cerveau/`.  État actuel mesuré : - M5 `tools/cerveau/predictif.py` : prédit l'action suivante ; exact 98,9 % = majoritaire 98,9 %, aucun gain ; l'ordre 2 n'a rien changé. - M6 `tools/cerveau/gating.py` : exact 7 … [2050 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Nous sommes dans /home/stephane/GitHub/Qtrinet (dépôt Drave). Sprint autonome 24 h. Tu es un sous-agent chargé de M5 (co … [2330 caractères tronqués]

*78 appels d'outils.* Actions notables :

- bash — List repo and cerveau directory
- bash — Count lines in cerveau files
- read
- bash — Inspect multilingual lexicon module
- bash — Inspect tests and detecte_langue usages
- bash — Run diagnostic of current M5/M6
- bash — List fr/en items with codes
- bash — Inspect multilingual corpus construction
- bash — Inspect codec base API and hub
- bash — List B7 fr/en surfaces
- bash — Measure detection and semantic reading on B7 fr/en
- bash — Inspect dames rules code
- bash — Inspect echecs action derivation
- bash — Prototype M5 targets and gains
- … et 57 autres

**Synthèse produite :**

\## Résultat — M5/M6 mesurés, testés, documentés

**Fichiers modifiés** (aucun commit, aucun autre fichier touché) :
- `tools/cerveau/predictif.py` — cibles `action`/`source`/`cible`, ordres 0/1/2, repli Dirichlet, baselines majoritaire et « tour », oracle documenté, contrôle négatif par permutation, diagnostic de dispersion.
- `tools/cerveau/gating.py` — vraie tâche de conflit B7 fr/en (88 essais : go/traduction/langue/ni), politiques comparées, exactitude équilibrée/Wilson/MCC, commutation appariée, contrôle positif de persévération, canal langue déterministe.
- `tools/cerveau/tests/test_predictif.py`, `tools/cerveau/tests/test_gating.py` — 18 tests, tous OK.

**Livrables** : `/tmp/a1-m5-m6.json` (28,5 Ko) et `/tmp/a1-m5-m6.md` (14,5 Ko).

\### M5 — le 98,9 % était la classe constante
`action` est un indicateur de **format** : échecs=toujours `deplacer`, dames=toujours `prendre`, morpion=toujours `jouer_case` ; seul go varie (92 % poser). Sur `corpus(0,200,12)` :
- `action` : 97,46 % = majoritaire, gain 0 ; ordre 2 sans effet.
- `source` : 12,60 % vs 6,49 % (ordre 1, +6,1 pt, +0,43 nat), mais le gain est **mécanique** : dames +8,8 pt (au-dessus de la baseline tour), échecs +3,2 pt **sous** la baseline tour.
- `cible` : +2,1 pt (ordre 1) mais surprisal **négative** (−0,04 nat) ; ordre 2 +5,6 pt, surprisal −0,04. Seules les dames gagnent réellement (+6 à +13 pt, +0,26 à +0,36 nat).
- Oracle avec plateau : H 1,1–2,8 nats selon jeu/cible, contre 2,6–4,9 pour le modèle → **le code observé ne contient pas le plateau** ; le tirage uniforme parmi les coups légaux borne le prédictible.
- Contrôles permutation : l'exact dépasse le null, mais le gain de surprisal reste négatif pour `cible` → gain de mode, pas d'information.

\### M6 — la détection de langue n'est pas du contrôle exécutif
- Conjonction sens+langue : **94,32 %** exact, **88,64 %** équilibrée, VP 17, **FP 0, FN 5**, sensibilité 77,27 %, spécificité 100 %, MCC 0,848 (base « toujours non » 75 %).
- Langue-seule, sens-seul et tout-non : **toutes à 75 %** — seule la conjonction gagne.
- **Coût de commutation apparié = 0,000** (21 blocs switch / 21 repeat, mêmes stimuli) ; contrôle positif de persévération = 0,381 → l'instrument est sensible, la porte n'a pas de mémoire.
- 2 codes ont la même surface fr/en (`go D4`, `tic-tac-toe A1`) : plafond exact 95,45 %, sensibilité 81,82 %. La porte est à **1 essai du plafond** ; les 5 FN sont perceptifs, pas inhibiteurs.
- L'ancien 72,9 % : 70 items (55 fr/15 en), exact
… [615 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_predictif.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_gating.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** List repo and cerveau directory
- **T1** Count lines in cerveau files
- **T1** Inspect multilingual lexicon module
- **T1** Inspect tests and detecte_langue usages
- **T1** Run diagnostic of current M5/M6
- **T1** List fr/en items with codes
- **T1** Inspect multilingual corpus construction
- **T1** Inspect codec base API and hub
- **T1** List B7 fr/en surfaces
- **T1** Measure detection and semantic reading on B7 fr/en
- **T1** Inspect dames rules code
- **T1** Inspect echecs action derivation
- **T1** Prototype M5 targets and gains
- **T1** Prototype order 0/1/2 and turn baseline
- **T1** Estimate oracle ceiling per target
- **T1** Test semantic decoding without context
- **T1** Inspect lexicon matches for B7 fr/en items
- **T1** Check determinism of language detection across hash seeds
- **T1** Inspect langue_probable implementation
- **T1** Compare language channel variants
- **T1** Prototype final M5 evaluation
- **T1** Prototype per-game turn decomposition
- **T1** Rerun per-game decomposition
- **T1** Run the new M6 gate
- **T1** Debug switch replay errors
- **T1** Instrument switch cost computation
- **T1** Print perseveration decisions per trial
- **T1** Print full block error list
- **T1** Fix base rate and matched switch cost, rerun
- **T1** Run M5 full protocol
- **T1** Fix OOV and tour alignment, rerun M5
- **T1** Sweep kappa for calibration
- **T1** Fix determinism and tour alignment, rerun
- **T1** Decompose order-2 gains and exclusion baseline
- **T1** Check typed corpus compatibility and mesurer
- **T1** Run cerveau test suite
- **T1** Fix majority test and rerun suite
- **T1** Check batterie compatibility
- **T1** Reproduce old M6 across hash seeds
- **T1** Inspect old design block composition
- … et 25 autres

## 4. Mesures et résultats marquants

- **T1** `"""regles.dames — les dames anglaises (8×8), prises obligatoires.`
- **T1** `| action | 0 | 1538 | 97.5 % | 97.5 % | +0.0 pt | 0.086 | 0.086 | +0.000 |`
- **T1** `| action | 1 | 1538 | 97.5 % | 97.5 % | +0.0 pt | 0.087 | 0.086 | -0.000 |`
- **T1** `| action | 2 | 1538 | 97.5 % | 97.5 % | +0.0 pt | 0.087 | 0.086 | -0.001 |`
- **T1** `| source | 0 | 770 | 6.5 % | 6.5 % | +0.0 pt | 3.539 | 3.539 | +0.000 |`
- **T1** `| source | 1 | 770 | 12.6 % | 6.5 % | +6.1 pt | 3.112 | 3.539 | +0.428 |`
- **T1** `| source | 2 | 770 | 14.4 % | 6.5 % | +7.9 pt | 3.099 | 3.539 | +0.440 |`
- **T1** `| cible | 0 | 1465 | 5.8 % | 5.8 % | +0.0 pt | 3.375 | 3.375 | +0.000 |`
- **T1** `| cible | 1 | 1465 | 7.9 % | 5.8 % | +2.1 pt | 3.418 | 3.375 | -0.043 |`
- **T1** `| cible | 2 | 1465 | 11.4 % | 5.8 % | +5.6 pt | 3.410 | 3.375 | -0.035 |`
- **T1** `Lecture : l'ordre 0 est la baseline majoritaire par jeu. L'ancien M5 (`action`, ordre 1) donnait 98,9 % = la classe constante : `action` est constante par jeu (échecs `deplacer`, dames `prendre`, morp`
- **T1** `| source | 1 | echecs | 374 | 7.5 % | 4.3 % | +3.2 pt | 8.3 % | -0.8 pt | +0.184 |`
- **T1** `| source | 1 | dames | 396 | 17.4 % | 8.6 % | +8.8 pt | 12.9 % | +4.5 pt | +0.658 |`
- **T1** `| source | 2 | echecs | 374 | 7.2 % | 4.3 % | +2.9 pt | 8.3 % | -1.1 pt | +0.116 |`
- **T1** `| source | 2 | dames | 396 | 21.2 % | 8.6 % | +12.6 pt | 12.9 % | +8.3 pt | +0.746 |`
- **T1** `| cible | 1 | echecs | 373 | 5.6 % | 3.5 % | +2.1 pt | 8.3 % | -2.7 pt | +0.012 |`
- **T1** `| cible | 1 | dames | 396 | 15.4 % | 9.3 % | +6.1 pt | 12.1 % | +3.3 pt | +0.263 |`
- **T1** `| cible | 1 | go | 379 | 1.6 % | 1.6 % | +0.0 pt | 1.8 % | -0.3 pt | -0.509 |`
- **T1** `| cible | 1 | morpion | 317 | 8.8 % | 9.1 % | -0.3 pt | 12.9 % | -4.1 pt | +0.067 |`
- **T1** `| cible | 2 | echecs | 373 | 7.5 % | 3.5 % | +4.0 pt | 8.3 % | -0.8 pt | -0.036 |`
- **T1** `| cible | 2 | dames | 396 | 22.2 % | 9.3 % | +12.9 pt | 12.1 % | +10.1 pt | +0.364 |`
- **T1** `| cible | 2 | go | 379 | 1.6 % | 1.6 % | +0.0 pt | 1.8 % | -0.3 pt | -0.521 |`
- **T1** `| cible | 2 | morpion | 317 | 14.2 % | 9.1 % | +5.0 pt | 12.9 % | +1.3 pt | +0.046 |`
- **T1** `| action | morpion | 317 | 0.000 | 100.0 % |`
- **T1** `| action | echecs | 374 | 0.000 | 100.0 % |`
- **T1** `| action | go | 451 | 0.325 | 90.0 % |`
- **T1** `| action | dames | 396 | 0.000 | 100.0 % |`
- **T1** `| source | morpion | 0 | 0.000 | 0.0 % |`
- **T1** `| source | echecs | 374 | 2.375 | 17.1 % |`
- **T1** `| source | go | 0 | 0.000 | 0.0 % |`
- **T1** `| source | dames | 396 | 1.118 | 48.0 % |`
- **T1** `| cible | morpion | 317 | 1.521 | 26.1 % |`
- **T1** `| cible | echecs | 374 | 2.793 | 11.5 % |`
- **T1** `| cible | go | 379 | 4.323 | 1.3 % |`
- **T1** `| cible | dames | 396 | 1.083 | 48.2 % |`
- **T1** `| source | 1 | 1 | 12.6 % | +6.1 pt | 3.334 | +0.205 |`
- **T1** `| source | 1 | 10 | 12.6 % | +6.1 pt | 3.112 | +0.428 |`
- **T1** `| source | 1 | 50 | 12.6 % | +6.1 pt | 3.139 | +0.401 |`
- **T1** `| source | 2 | 1 | 14.4 % | +7.9 pt | 3.768 | -0.228 |`
- **T1** `| source | 2 | 10 | 14.4 % | +7.9 pt | 3.099 | +0.440 |`
- **T1** `| source | 2 | 50 | 13.8 % | +7.3 pt | 3.086 | +0.454 |`
- **T1** `| cible | 1 | 1 | 7.9 % | +2.1 pt | 3.917 | -0.542 |`
- **T1** `| cible | 1 | 10 | 7.9 % | +2.1 pt | 3.418 | -0.043 |`
- **T1** `| cible | 1 | 50 | 7.8 % | +2.0 pt | 3.280 | +0.095 |`
- **T1** `| cible | 2 | 1 | 11.4 % | +5.6 pt | 4.189 | -0.814 |`
- **T1** `| cible | 2 | 10 | 11.4 % | +5.6 pt | 3.410 | -0.035 |`
- **T1** `| cible | 2 | 50 | 10.9 % | +5.1 pt | 3.249 | +0.126 |`
- **T1** `**Conclusion M5.** Le 98,9 % n'était pas une prédiction : c'était la classe constante de `action`. Sur des cibles qui varient, il y a un gain réel aux dames (source/cible : +6 à +13 pt d'exact, +0,26 `
- **T1** `Tâche : 88 essais, 4 conditions équilibrées ({'go': 22, 'traduction': 22, 'langue': 22, 'ni': 22}), 11 codes × 2 langues cibles. La cible est un code typé et une langue ; la sonde est une surface B7. `
- **T1** `| conjonction | 94.3 % | 88.6 % | 77.3 % | 100.0 % | 17 | 0 | 5 | 66 |`
- **T1** `| langue | 75.0 % | 75.8 % | 77.3 % | 74.2 % | — | 17 | 5 | — |`
- **T1** `| sens | 75.0 % | 83.3 % | 100.0 % | 66.7 % | — | 22 | 0 | — |`
- **T1** `| tout_non | 75.0 % | 50.0 % | 0.0 % | 100.0 % | — | 0 | 22 | — |`
- **T1** `Taux de base (« toujours non ») : 75.0 %. Les trois politiques simples sont **toutes au taux de base** : la langue seule accepte les leurres de langue (25 % de FP), le sens seul accepte les traduction`
- **T1** `| go | 22 | 77.3 % | 17 |`
- **T1** `| traduction | 22 | 100.0 % | 0 |`
- **T1** `| langue | 22 | 100.0 % | 0 |`
- **T1** `| ni | 22 | 100.0 % | 0 |`
- **T1** `Coût de commutation apparié : **0.000** (21 blocs switch, 21 blocs repeat, mêmes stimuli ; erreur 6.0 % contre 6.0 %). Contrôle positif de persévération : **0.381** — l'instrument détecte bien une mém`
- **T1** `Canaux : langue 77.3 % (22 couples surface×langue), lecture 100.0 % (20 textes distincts). Surfaces identiques fr/en : ['go D4', 'tic-tac-toe A1'].`
- **T1** `Plafond d'identifiabilité : 4 essais sur 88 sont indistinguables (2 codes ont la même surface dans les deux langues) → exactitude maximale 95.5 %, sensibilité maximale 90.9 %. La porte est à 94,3 % et`
- **T1** `### L'ancienne mesure M6 (72,9 %) était un artefact`
- **T1** `Sur les 70 items fr/en de `typed_corpus` (55 fr, 15 en), l'ancienne porte donne 68.6 % à 70.0 % (moyenne 69.6 %) selon `PYTHONHASHSEED`, et un coût de commutation de -0.170 à -0.150. Or 39/55 items « `
- **T1** `- **Tient** : la tâche M6 est soluble et bien posée (conjonction 94,3 %, 0 FP) ; les politiques mono-canal sont au taux de base (75 %) ; le canal sens lit 20/20 textes ; la porte est déterministe.`
- **T1** `| action | morpion | 317 | 0.000 | 0.000 | +0.000 | 100.0 % |`
- **T1** `| action | echecs | 374 | 0.000 | 0.000 | +0.000 | 100.0 % |`
- **T1** `| action | go | 451 | 0.325 | 0.296 | -0.029 | 90.0 % |`
- **T1** `| action | dames | 396 | 0.000 | 0.000 | +0.000 | 100.0 % |`
- **T1** `| source | echecs | 374 | 2.375 | 3.641 | +1.266 | 17.1 % |`
- **T1** `| source | dames | 396 | 1.118 | 2.612 | +1.494 | 48.0 % |`
- **T1** `| cible | morpion | 317 | 1.521 | 2.131 | +0.610 | 26.1 % |`
- **T1** `| cible | echecs | 374 | 2.793 | 3.813 | +1.020 | 11.5 % |`
- **T1** `| cible | go | 379 | 4.323 | 4.912 | +0.589 | 1.3 % |`
- **T1** `| cible | dames | 396 | 1.083 | 2.646 | +1.563 | 48.2 % |`
- **T1** `88:**Conclusion M5.** Le 98,9 % n'était pas une prédiction : c'était la classe constante de `action`. Sur des cibles qui varient, il y a un gain réel aux dames (source/cible : +6 à +13 pt d'exact, +0,`
- **T1** `114:Plafond d'identifiabilité : 4 essais appariés (4 GO + 4 traduction, 2 codes × 2 langues) ne peuvent donner au mieux que 4/8 : l'exactitude maximale est 95.5 %. Au point de fonctionnement « rejeter`
- **T1** `124:### L'ancienne mesure M6 (72,9 %) était un artefact`
- **T1** `126:Sur les 70 items fr/en de `typed_corpus` (55 fr, 15 en), l'ancienne porte donne 68.6 % à 70.0 % (moyenne 69.6 %) selon `PYTHONHASHSEED`, et un coût de commutation de -0.170 à -0.150. Le 72,9 % pub`
- **T1** `Plafond d'identifiabilité : 4 essais appariés (4 GO + 4 traduction, 2 codes × 2 langues) ne peuvent donner au mieux que 4/8 : l'exactitude maximale est 95.5 %. Au point de fonctionnement « rejeter les`
- **T1** `Sur les 70 items fr/en de `typed_corpus` (55 fr, 15 en), l'ancienne porte donne 68.6 % à 70.0 % (moyenne 69.6 %) selon `PYTHONHASHSEED`, et un coût de commutation de -0.170 à -0.150. Le 72,9 % publié `
- **T1** ``Predictif()` a désormais pour cible par défaut `cible` (case d'arrivée), pas `action`. `batterie.m5` publiera donc ~12,5 % d'exact (gain +3,7 pt) au lieu de 98,9 %, et la lésion M9 `M5_sans_transitio`
- **T1** `"accepte les leurres de langue (25 % de FP), le sens seul accepte les traductions "`
- **T1** `"(25 % de FP). Seule la conjonction fait mieux. Son exactitude est de 94,3 %, "`
- **T1** `"mais la sensibilité n'est que de 77,3 % : les 5 FN sont **tous** des échecs du "`
- **T1** `a("### L'ancienne mesure M6 (72,9 %) était un artefact\n")`
- **T1** `"Le 72,9 % publié (51/70) est une autre graine de hachage : la valeur n'est pas "`
- **T1** `101:Taux de base (« toujours non ») : 75.0 %. Les trois politiques simples sont **toutes au taux de base** : la langue seule accepte les leurres de langue (25 % de FP), le sens seul accepte les traduc`
- **T1** `130:`Predictif()` a désormais pour cible par défaut `cible` (case d'arrivée), pas `action`. `batterie.m5` publiera donc ~12,5 % d'exact (gain +3,7 pt) au lieu de 98,9 %, et la lésion M9 `M5_sans_trans`
- **T1** `21:le taux de base est la **conjonction** (sens ET langue) : exactitude 94,3 %,`
- **T1** `22:exactitude équilibrée 88,6 %, 0 faux positif, 5 faux négatifs. Les 5 FN sont`

## 5. Erreurs rencontrées

8 sorties en erreur ou divergentes. Les premières :

- **T1** : n seqs 800 temps 2.4781277179718018 train/test seqs 640 160 action  n=1698 exact=0.9741 base=0.9741 gain=+0.0000 surprisal=0.088 base=0.087 dsur=-0.001    echecs   n= 408 exact=1.0000 base=1.0000 gain
- **T1** : action  ordre=0 n=1698 exact=0.9741 base=0.9741 gain=+0.0000 sur=0.087 surb=0.087 dsur=-0.000 action  ordre=1 n=1698 exact=0.9741 base=0.9741 gain=+0.0000 sur=0.088 surb=0.087 dsur=-0.000 action  ordr
- **T1** : echecs action {'n': 480, 'oracle_exact': 1.0, 'oracle_entropie': 0.0, 'coups_moyens': 24.2167} echecs source {'n': 480, 'oracle_exact': 0.1809, 'oracle_entropie': 2.3342, 'coups_moyens': 24.2167} eche
- **T1** : train 640 test 160 action o=0 n=1538 exact=0.9746 base=0.9746 gain=+0.0000 sur=0.086 base=0.086 dsur=-0.000 action o=1 n=1538 exact=0.9746 base=0.9746 gain=+0.0000 sur=0.087 base=0.086 dsur=-0.001 act
- **T1** : source o=1 n= 770 exact=0.1260 base=0.0649 gain=+0.0610 sur=3.334 dsur=+0.205 source o=2 n= 770 exact=0.1442 base=0.0649 gain=+0.0792 sur=3.768 dsur=-0.229   tour global {'n': 840, 'exact': 0.11785714
- **T1** : [stderr] Traceback (most recent call last):   File "/tmp/proto_m5d.py", line 3, in <module>     from cerveau.sequences import corpus ModuleNotFoundError: No module named 'cerveau' [exit code: 1]
- **T1** : diag action {'dames': {'n': 2400, 'distincts': 1, 'majoritaire': 1.0, 'entropie': -0.0}, 'echecs': {'n': 2400, 'distincts': 1, 'majoritaire': 1.0, 'entropie': -0.0}, 'go': {'n': 2400, 'distincts': 2, 
- **T1** : [stderr] Traceback (most recent call last):   File "/tmp/a1_oracle.py", line 78, in <module>     r=oracle_steps(jeu,[K[jeu]*1000+i for i in range(5)],cible)   File "/tmp/a1_oracle.py", line 47, in ora

