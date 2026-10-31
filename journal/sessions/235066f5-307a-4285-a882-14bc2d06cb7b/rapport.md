# Session 235066f5 — Dépôt /home/stephane/GitHub/Qtrinet, s

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `235066f5-307a-4285-a882-14bc2d06cb7b` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 11:38 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 31 |
| Appels d'outils | 39 |
| Fichiers touchés | 0 |
| Commandes | 39 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Dépôt /home/stephane/GitHub/Qtrinet, sprint autonome 24 h. Sous-agent A8 : construire et mesurer une **chaîne sémantique** B13 avec les modules corrigés, sans toucher aux modules existants.  État corrigé (à utiliser tel quel) : - M1 `hub.py` : codec typé exact, 528/528 avec contexte, 70,8 % sans contexte. - M2 `voies.py` : têtes `de`/`vers` ; vues 126/126 ; inédit 13/20 (aug-formes) ; `point`/`che … [1828 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Dépôt /home/stephane/GitHub/Qtrinet, sprint autonome 24 h. Sous-agent A8 : construire et mesurer une **chaîne sémantique … [2108 caractères tronqués]

*39 appels d'outils.* Actions notables :

- bash — List repo root and cerveau tools
- bash — Check git status and recent log
- bash — Count lines in cerveau modules and list tests
- bash — Read start of hub.py
- bash — Read batterie.py
- bash — Find files mentioning 528
- bash — List voies.py API
- bash — List APIs of predictif, gating, sommeil, lesion
- bash — Read predictif.py first part
- bash — Read predictif.py second part
- bash — Read gating.py first part
- bash — Read gating.py executer section
- bash — Read gating switch task section
- bash — Read sommeil.py first part
- … et 24 autres

**Synthèse produite :**

⏵ Écriture du module `pipeline_semantique.py` (chaîne M1→M5→M6→M8→M9)

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List repo root and cerveau tools
- **T1** Check git status and recent log
- **T1** Count lines in cerveau modules and list tests
- **T1** Read start of hub.py
- **T1** Read batterie.py
- **T1** Find files mentioning 528
- **T1** List voies.py API
- **T1** List APIs of predictif, gating, sommeil, lesion
- **T1** Read predictif.py first part
- **T1** Read predictif.py second part
- **T1** Read gating.py first part
- **T1** Read gating.py executer section
- **T1** Read gating switch task section
- **T1** Read sommeil.py first part
- **T1** Search for 94.95 metric
- **T1** Read lesion.py m8 and battery
- **T1** Read lesion.py intro and M1 lesion
- **T1** Read lesion M5 and M6
- **T1** List semantic/jeux modules and read typed_corpus
- **T1** Read corpus.py
- **T1** Read universaux API
- **T1** Count corpus items and inspect one
- **T1** List existing A-series result files
- **T1** Read brain corrections report
- **T1** Read A6 M5-M6 report
- **T1** Read gating tests
- **T1** Read existing pipeline and tests
- **T1** Search for selection API in tools
- **T1** Read sequences corpus generator
- **T1** Corpus statistics
- **T1** Verify M1 exact and list paire sizes
- **T1** Verify M1 exact and list paire sizes
- **T1** Verify M1 on native 528 items
- **T1** Prototype M5 trained on games, evaluated on 528 items
- **T1** Prototype M6 language selection
- **T1** Prototype M8 split and LOO
- **T1** Prototype M1 with permuted contexts
- **T1** Count distinct contexts per game
- **T1** Measure M6 language selection balanced

## 4. Mesures et résultats marquants

- **T1** `74c1fd86 B12 — M2 AUG-POS : VERS 95,4 % INÉDIT 13,3/20 ; DE 92,2 % ; POINT = MAJORITÉ ; AUCUNE VARIANTE NE DOMINE`
- **T1** `varie (`poser` 92 %, `passer` 8 %). Prédire `action` ne peut donc pas battre la`
- **T1** `classe majoritaire : le 98,9 % publié était le taux de cette constante.`
- **T1** `comparée à la langue cible. Son « exactitude » de 72,9 % était donc le taux du`
- **T1** `politique « toujours non » obtient 75 %, et chaque canal seul (langue ou sens)`
- **T1** `obtient 75 % aussi, avec 25 % de faux positifs. La seule politique qui dépasse`
- **T1** `le taux de base est la **conjonction** (sens ET langue) : exactitude 94,3 %,`
- **T1** `exactitude équilibrée 88,6 %, 0 faux positif, 5 faux négatifs. Les 5 FN sont`
- **T1** `"""Intervalle de Wilson à 95 % pour une proportion."""`
- **T1** `champ**. Le score publié, 96,48 % sur 106 épisodes de test, est réel mais il est`
- **T1** `- les champs sont **dominés par ``None``** : 12 des 15 champs ont plus de 98 %`
- **T1** ```None``. Sur les valeurs non nulles, la précision tombe à ~84 % sur tout le`
- **T1** `corpus (~86 % sur la queue), et les trois champs porteurs (``de``, ``vers``,`
- **T1** ```carte``) sont à ~50 %, ~50 % et ~22–28 % conditionnellement.`
- **T1** `- le score **exact** n'est pas 0 % : il vaut 65,1 % sur la queue, 24,1 % sur les`
- **T1** `- groupé par ``(jeu)`` seul, le prototype fait déjà 96,10 % : le groupe`
- **T1** `l'exact est 0 % par construction. Un prototype est une marginale, pas une`
- **T1** `repli sur le prototype sinon). L'hybride porte l'exact à 100 % sur la queue,`
- **T1** ```jeu`` porte les champs à 89,20 %, le backoff ``type→groupe→jeu→global`` à`
- **T1** `90,11 %, mais les champs non nuls ne passent que de 61,26 % à 63,51 %, dont`
- **T1** ```chemin``) sont à 0 % hors coïncidences de marginale ;`
- **T1** `les surfaces déjà vues, soit 0 % sur un code tenu à l'écart.`
- **T1** `reports/rapport-cerveau-corrections.md:102:- **Tâche de gate de tâche** (sens/langue, 792 essais) : **94,95 %**, base 50 % ; conflit **0,000**, commutation **0,000** ; la langue seule est à 88,6 %, le`
- **T1** `reports/rapport-cerveau-corrections.md:157:- **M6** : **sélecteur de tâche** à 94,95 % (base 50 %), mais **conflit 0** et **commutation 0** ;`
- **T1** `(96,48 %) est rappelée pour mémoire : ses 106 codes sont tous dans le train,`
- **T1** `"L'hybride 100 % de la queue est tautologique (clé = code cible) ; "`
- **T1** `"clé par surface, sa couverture sur codes tenus est 0 %."))`
- **T1** `"M5 : les transitions ne gagnent que 3,7 pts (12,45 -> 8,79 %) ; "`
- **T1** `"l'ordre 2 ne gagne rien ; l'ancien 98,9 % était la constante action",`
- **T1** `"M8 : le 96,48 % publié est intra-code (106/106 codes de test "`
- **T1** `"sont dans le train, plafond corpus du groupe 57,95 %)",`
- **T1** `> **Objet.** Les premiers chiffres B12 (M2 93,2 %, M3 12/12, M4 1,0, M8 96,48 %) étaient`
- **T1** `| sans contexte | **70,8 %** |`
- **T1** `| canonique | **100 %** |`
- **T1** `| invariance | **100 %** |`
- **T1** `## 2. M2 — le 93,2 % était du recouvrement de surfaces`
- **T1** `| `de` moyen 3 graines | **93,6 %** |`
- **T1** `| `de` sur surfaces inédites | **10,7 / 20 = 53,3 %** |`
- **T1** `| `vers` moyen 3 graines | **94,3 %** |`
- **T1** `| `vers` inédit | **11,7 / 20 = 58,3 %** |`
- **T1** `| `point` | 95,7 % **< majorité 97,1 %** |`
- **T1** `| `chemin_0` | 84,3 % **< majorité 97,1 %** |`
- **T1** ``de`, **l'action est constante** : 98,6 % = la majorité, donc la tête ventrale ne prouve rien ;`
- **T1** `**+1,4** sur `point`, **−2,9** sur `chemin_0` ; `mean` seul atteint 89,7 % sur `de` à 1 000 pas.`
- **T1** ``aug-formes` : `de` **95,2 %**, inédit **13/20** ; `chemin_0` **88,1 %**, inédit **6/14** ;`
- **T1** ``point` 96,7 %, inédit 1,7/4 ; `vers` 93,8 %, inédit 11/20.`
- **T1** ``aug-pos` : `de` **92,2 %**, inédit **8,7/20** ; `vers` **95,4 %**, inédit **13,3/20** ;`
- **T1** ``point` **97,14 % = majorité**, inédit 2/4 ; `chemin_0` **86,7 %**, inédit 6/14.`
- **T1** `- **Plus d'entraînement dégrade l'inédit** : à 1 000 pas, `de` tombe à **9,3/20** (46,7 %)`
- **T1** `contre 10,7/20 à 300 pas ; les formes vues restent à 100 %. Le split inédit est un **priori de`
- **T1** `(`de` : 52 ×6, 62 ×6, 57 ×1) et **3** (`vers` : 36 ×6, 45 ×6, 42 ×1). Les 10,7/13 et 11,7/13`
- **T1** `- **Bruit** : p50(span 12) = **5,5 %** (analytique 5,6 %) ; à p=5 %, les champs restent à 99,64 %`
- **T1** `mais les 12 codes exacts tombent à **52,5 %** : aucune correction.`
- **T1** `- La complétion 97,9 % s'explique par **72,35 % `vers=None`** (15/15) et **27,65 % à 14/15** :`
- **T1** `0,7235 + 0,2765 × 14/15 = **0,9816** ; c'est de l'identité, pas de la complétion.`
- **T1** `- **Fausse mémoire** : 98,96 % des leurres à 1 champ reçoivent une valeur fausse ; 65,4 % renvoient`
- **T1** `Prédire `action` ne peut pas battre la majorité : **97,46 % = 97,46 %** sur 1 538 transitions,`
- **T1** ``source` ordre 1 **12,60 % vs 6,49 %** (+6,10 pts), ordre 2 **14,42 %** ; `cible` ordre 1`
- **T1** `**7,92 % vs 5,80 %** (+2,12 pts) mais **surprisal −0,04 nat** (gain de mode). Les dames portent`
- **T1** `- Nouvelle tâche de conflit fr/en (88 essais, 4 conditions) : **94,32 %** de conjonction,`
- **T1** `**88,64 %** équilibrée, VP 17, FP 0, FN 5 ; mais les politiques « langue seule », « sens seul » et`
- **T1** `« tout non » sont **toutes à 75 %** : chaque canal seul a 25 % de faux positifs.`
- **T1** `- **Tâche de gate de tâche** (sens/langue, 792 essais) : **94,95 %**, base 50 % ; conflit **0,000**, commutation **0,000** ; la langue seule est à 88,6 %, le sens à 100 %. C'est un **sélecteur de tâch`
- **T1** `- Deux surfaces sont identiques fr/en (`go D4`, `tic-tac-toe A1`) : plafond exact **95,45 %** ; la`
- **T1** `- La mémoire à 16 places ne peut retenir que **16/439 = 3,64 %** des surfaces : toutes les`
- **T1** `## 8. M8 — le 96,48 % est la marginale, pas la généralisation`
- **T1** `- 12/15 champs sont constants ; le score **96,48 %** est dominé par la marginale.`
- **T1** `- Exact réel : **65,1 %** (pas 0 %) ; champs non nuls : **85,96 %**.`
- **T1** `- Baseline **par jeu** : **96,10 %** de champs, exact **63,2 %** ; le groupe `(jeu, action)` n'apporte`
- **T1** `- **106/106 codes de la queue sont dans le train** ; l'oracle par paire fait 100 % et le plafond`
- **T1** `contextuel `(jeu, action)` vaut **57,95 %**, sous les 65,1 % publiés : la queue est un`
- **T1** `- Sur codes jamais vus : **leave-one-code-out**, exact **0 % par construction** ; champs **90,1 %**`
- **T1** `en backoff type→groupe→jeu→global, mais champs **non nuls 63,5 %** et les coordonnées`
- **T1** `(`de`, `vers`, `point`, `carte`, `case`, `chemin`) à **0 %** ; les prototypes ne peuvent pas produire`
- **T1** `un code neuf. **M8 ne généralise pas** ; il résume la marginale. Le 96,48 % est un plafond de`
- **T1** `M9 (CPU) estime les déficits par privation : M1 **29,2 %**, M2 ventrale **13,8 %** / dorsale`
- **T1** `**12,4 %** sur le proxy, M3 **0**, M4 **0**, M5 **?**, M6 **?**, M7 **?**, M8 **0**. M2 est un`
- **T1** `M1 → M4 → M8 : **528/528**, **7 prototypes**, **96,33 %** de complétion sur 120 codes partiels.`
- **T1** `- **M1** est **solide** : codec exact + bus, 528/528, 70,8 % sans contexte, 100 % canonique.`
- **T1** `- **M6** : **sélecteur de tâche** à 94,95 % (base 50 %), mais **conflit 0** et **commutation 0** ;`
- **T1** `la langue seule est à 88,6 %. Pas d'inhibition exécutive mesurée.`
- **T1** `- **M7** : **négatif** — 3,64 % = plafond 16/439 ; LFU +23 pts, aucun signal neuromodulateur.`
- **T1** `- **M8** : **marginal** — 96,48 % de champs, exact 65,1 %, baseline par jeu 96,10 %,`
- **T1** `leave-one-code-out exact **0** ; coordonnées 0 % sur codes neufs.`
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
- **T1** `| source | 2 | masque_hist | 843 | 17.4 % | 5.7 % | 2.733 | +0.867 | +0.481 | +0.036 |`
- **T1** `| source | 2 | masque_melange | 843 | 17.4 % | 5.7 % | 2.468 | +1.132 | +0.747 | +0.036 |`
- **T1** `| cible | 1 | sans | 1498 | 8.7 % | 6.0 % | 3.520 | -0.088 | +0.000 | +0.000 |`
- **T1** `| cible | 1 | masque_uniforme | 1499 | 9.4 % | 6.0 % | 3.109 | +0.328 | +0.411 | +0.007 |`
- **T1** `| cible | 1 | masque_hist | 1498 | 12.3 % | 6.0 % | 3.208 | +0.223 | +0.312 | +0.036 |`
- **T1** `| cible | 1 | masque_melange | 1499 | 12.3 % | 6.0 % | 3.031 | +0.406 | +0.489 | +0.036 |`
- **T1** `| cible | 2 | sans | 1498 | 10.8 % | 6.0 % | 3.521 | -0.089 | +0.000 | +0.000 |`
- **T1** `| cible | 2 | masque_uniforme | 1499 | 9.4 % | 6.0 % | 3.109 | +0.328 | +0.412 | -0.014 |`
- **T1** `| cible | 2 | masque_hist | 1498 | 14.6 % | 6.0 % | 3.228 | +0.203 | +0.292 | +0.038 |`
- **T1** `| cible | 2 | masque_melange | 1499 | 14.6 % | 6.0 % | 3.016 | +0.420 | +0.504 | +0.038 |`
- **T1** `| source | 1 | echecs | 455 | 8.0 % | 3.7 % | 2.796 | 2.357 | +0.439 | 67.0 % |`
- **T1** `| source | 1 | dames | 389 | 26.4 % | 8.1 % | 2.116 | 1.152 | +0.964 | 37.3 % |`
- **T1** `| source | 2 | echecs | 455 | 8.3 % | 3.7 % | 2.810 | 2.357 | +0.453 | 67.4 % |`
- **T1** `| source | 2 | dames | 389 | 28.0 % | 8.1 % | 2.072 | 1.152 | +0.920 | 36.4 % |`
- **T1** `| cible | 1 | echecs | 455 | 6.6 % | 3.6 % | 3.603 | 2.786 | +0.816 | 26.0 % |`
- **T1** `| cible | 1 | dames | 389 | 20.4 % | 9.7 % | 2.120 | 1.118 | +1.002 | 38.1 % |`
- **T1** `| cible | 1 | go | 368 | 1.0 % | 1.2 % | 4.471 | 4.323 | +0.148 | 77.5 % |`
- **T1** `| cible | 1 | morpion | 287 | 24.9 % | 11.0 % | 1.507 | 1.497 | +0.011 | 98.3 % |`
- **T1** `| cible | 2 | echecs | 455 | 6.8 % | 3.6 % | 3.617 | 2.786 | +0.831 | 28.3 % |`
- **T1** `| cible | 2 | dames | 389 | 28.2 % | 9.7 % | 2.040 | 1.118 | +0.922 | 40.6 % |`
- **T1** `| cible | 2 | go | 368 | 1.2 % | 1.2 % | 4.472 | 4.323 | +0.149 | 77.7 % |`
- **T1** `| cible | 2 | morpion | 287 | 26.1 % | 11.0 % | 1.516 | 1.497 | +0.019 | 96.9 % |`
- … (tronqué)

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 11, in <module> AttributeError: 'ItemType' object has no attribute 'attendu' [exit code: 1]

