# Session 8eda56f8 — Dépôt /home/stephane/GitHub/Qtrinet, s

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `8eda56f8-9964-432f-8fa4-d5ad537369b7` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 15:11 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 19 |
| Appels d'outils | 27 |
| Fichiers touchés | 0 |
| Commandes | 22 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Dépôt /home/stephane/GitHub/Qtrinet, sprint 24 h. Sous-agent A17 : compléter M9 par des **lésions croisées, sham et dose-réponse**, sans modifier les modules existants.  État : - `tools/cerveau/lesion.py` : `batterie_lesions()` CPU ; M2 réel `voies.py` validé (action 98,63→12,33, de 91,78→2,05). - M2 `voies.py`, M5 `predictif.py`, M6 `gating.py`, M8 `sommeil.py`. - Tests : `PYTHONPATH=tools python … [1317 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Dépôt /home/stephane/GitHub/Qtrinet, sprint 24 h. Sous-agent A17 : compléter M9 par des **lésions croisées, sham et dose … [1597 caractères tronqués]

*27 appels d'outils.* Actions notables :

- bash — List cerveau tools and tests
- bash — Show git status and recent log
- read
- bash — Count lines of relevant modules
- bash — Read gating and sommeil top sections
- bash — List gating API
- bash — List sommeil and sequences API
- bash — Find pipelines chaining modules
- bash — Check torch, CUDA, base availability
- bash — Look for venv and dependency files
- bash — Search for Python environment
- bash — Check venv torch and base model
- bash — Find M9 roadmap context
- bash — Search existing cross-lesion mentions
- … et 9 autres

**Synthèse produite :**

⏵ Benchmarking the real M2 lesion path before designing the new battery

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List cerveau tools and tests
- **T1** Show git status and recent log
- **T1** Count lines of relevant modules
- **T1** Read gating and sommeil top sections
- **T1** List gating API
- **T1** List sommeil and sequences API
- **T1** Find pipelines chaining modules
- **T1** Check torch, CUDA, base availability
- **T1** Look for venv and dependency files
- **T1** Search for Python environment
- **T1** Check venv torch and base model
- **T1** Find M9 roadmap context
- **T1** Search existing cross-lesion mentions
- **T1** Read sequences and batterie M5/M6
- **T1** Read M2 pipeline docs and main measure
- **T1** Run existing cerveau tests with timing
- **T1** Inspect M7 and M6 APIs
- **T1** Read M6 decision policies and metrics
- **T1** Inspect MemoireTravail API
- **T1** Inspect M7 configurations
- **T1** Inspect M8 public experience functions
- **T1** Run real M2 lesion once and time it

## 4. Mesures et résultats marquants

- **T1** `comparée à la langue cible. Son « exactitude » de 72,9 % était donc le taux du`
- **T1** `politique « toujours non » obtient 75 %, et chaque canal seul (langue ou sens)`
- **T1** `obtient 75 % aussi, avec 25 % de faux positifs. La seule politique qui dépasse`
- **T1** `le taux de base est la **conjonction** (sens ET langue) : exactitude 94,3 %,`
- **T1** `exactitude équilibrée 88,6 %, 0 faux positif, 5 faux négatifs. Les 5 FN sont`
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
- **T1** `docs/roadmap.md:361:| B12.9 | **M9 lésion** | ✅ **table** | contexte **29,2 %** ; M2 ventrale **24,7 %** ; M2 dorsale **2,1 %** ; M7 **13,7 %** ; M3 **0** ; M4 **0** ; M5 **1,1 %** ; M6 **30 %** ; M8 `
- **T1** `docs/roadmap.md:369:| B13.1 | **Chaîne sémantique M1→M5→M6→M8** | ✅ **intégration** | M1 **528/528** ; M5 contexte **18,7 % vs 12,6 %** (surprise 2,423 vs 3,112) ; M6 **94,3 %** / switch **94,95 %** ;`
- **T1** `docs/synthese/index.md:132:| **B12 — les modules cerveau-langage M1–M9** : bus réel, **M1 528/528**, **M2 98,6 / 93,2** (double dissociation), **M8 96,48 %** hors stock ; **M5/M6/M7** négatifs ou faib`
- **T1** `docs/modules-cerveau-langage.md:28:| **M2 voies** | ventrale (`action`) / dorsale (`de`) | `action` global **86,4 %** ; `de` **93,6 %** (3 graines) = **126/126 vus + 10,7/20 inédits** ; lésions croisé`
- **T1** `docs/carte.md:58:| **B12** les modules cerveau-langage | **premier passage** — M1 528/528 ; M2 **98,6 / 93,2** (double dissociation) ; M8 **96,48 %** hors stock ; M5/M6/M7 négatifs ; M9 lésions | [les`
- **T1** `reports/rapport-cerveau-modules.md:54:- **M2** : lésions croisées des têtes ; ventrale 98,6 → 9,6 %, dorsale 93,2 → 0,7 %.`
- **T1** `reports/rapport-cerveau-modules.md:77:- **M2** est **valide** : la double dissociation est nette (`de` 93,2 %, lésion dorsale 0,7 %, lésion`
- **T1** `reports/README.md:39:| [`rapport-cerveau-modules.md`](rapport-cerveau-modules.md) | **B12** : les modules M1–M9 — hub **528/528**, mémoire épisodique **1,0** ; M2 double dissociation (`action` 98,6 %,`
- **T1** `journal/2026-10-26_deepseek.md:125:**Les modules M1–M9 (B12).** Premier prototype Python de la couche cerveau-langage : bus d’événements, hub typé, voies ventrales/dorsales, mémoire de travail, mémoir`
- **T1** `388-    Le suffixe est le dernier 20 % du flux ; la mémoire est gelée à la fin du`
- **T1** `390-    même capacité), avec le taux de gains et un IC 95 % normal.`
- **T1** `899-    préfixe. La mémoire est gelée à la fin du préfixe ; le suffixe (20 %) est`
- **T1** `682-        2. ``codes_tenus`` : 3 graines, 20 % des codes exclus par jeu, évaluation`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 1, in <module> ModuleNotFoundError: No module named 'torch' [exit code: 1]
- **T1** : Error: tool call aborted

