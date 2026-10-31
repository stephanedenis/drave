# Session 4e86f5e2 — Dépôt /home/stephane/GitHub/Qtrinet, s

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `4e86f5e2-cc8e-43d7-8be0-ba9622de2dc7` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 14:55 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 25 |
| Appels d'outils | 37 |
| Fichiers touchés | 0 |
| Commandes | 25 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Dépôt /home/stephane/GitHub/Qtrinet, sprint 24 h. Sous-agent A15 : compléter M9 par des **lésions croisées et des contrôles sham** sur les modules réels, sans modifier les modules existants.  État : - `tools/cerveau/lesion.py` : `batterie_lesions()` CPU (M1 contexte, M2 proxy, M3, M4, M5, M6, M7, M8) ; M2 réel `voies.py` validé (action 98,63→12,33, de 91,78→2,05). - M2 `voies.py`, M5 `predictif.py … [1456 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Dépôt /home/stephane/GitHub/Qtrinet, sprint 24 h. Sous-agent A15 : compléter M9 par des **lésions croisées et des contrô … [1736 caractères tronqués]

*37 appels d'outils.* Actions notables :

- bash — List repo and cerveau directory
- bash — Count lines in cerveau modules
- read
- bash — List classes and functions in key modules
- bash — Check M2 base, GPU and torch availability
- bash — Locate python env and base config
- bash — Probe python interpreters for torch
- bash — Check torch in venv-drave
- bash — Search for existing double dissociation work
- bash — Search for A15 references
- bash — Read brain modules report
- bash — Find sprint A15 context
- bash — Scan rest of pipeline M2 module
- bash — Read sequences and sommeil headers
- … et 12 autres

**Synthèse produite :**

⏵ Writing `tools/cerveau/lesion_complet.py` (benches, sham, dose-response, doubles)

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List repo and cerveau directory
- **T1** Count lines in cerveau modules
- **T1** List classes and functions in key modules
- **T1** Check M2 base, GPU and torch availability
- **T1** Locate python env and base config
- **T1** Probe python interpreters for torch
- **T1** Check torch in venv-drave
- **T1** Search for existing double dissociation work
- **T1** Search for A15 references
- **T1** Read brain modules report
- **T1** Find sprint A15 context
- **T1** Scan rest of pipeline M2 module
- **T1** Read sequences and sommeil headers
- **T1** Read M5 plateau findings in corrections report
- **T1** Search reports for M5 plateau
- **T1** Read pipeline M2 report
- **T1** Read M5 correction details
- **T1** Inspect universal field values
- **T1** Inspect predictif constants
- **T1** Inspect experience_m7
- **T1** Inspect M8 experience functions
- **T1** Read memory module API
- **T1** Read span/nback details
- **T1** Read episodic memory API
- **T1** Check M7 flux preparation

## 4. Mesures et résultats marquants

- **T1** `reports/rapport-cerveau-modules.md:77:- **M2** est **valide** : la double dissociation est nette (`de` 93,2 %, lésion dorsale 0,7 %, lésion`
- **T1** `reports/README.md:38:| [`rapport-cerveau-modules.md`](rapport-cerveau-modules.md) | **B12** : les modules M1–M9 — hub **528/528**, mémoire épisodique **1,0** ; M2 double dissociation (`action` 98,6 %,`
- **T1** `docs/synthese/index.md:132:| **B12 — les modules cerveau-langage M1–M9** : bus réel, **M1 528/528**, **M2 98,6 / 93,2** (double dissociation), **M8 96,48 %** hors stock ; **M5/M6/M7** négatifs ou faib`
- **T1** `docs/carte.md:57:| **B12** les modules cerveau-langage | **premier passage** — M1 528/528 ; M2 **98,6 / 93,2** (double dissociation) ; M8 **96,48 %** hors stock ; M5/M6/M7 négatifs ; M9 lésions | [les`
- **T1** `docs/roadmap.md:354:| B12.2 | **M2 voies ventrales/dorsales** | ⚠️ **vu + règles** | `aug-formes` : `de` **95,2 %, inédit 13/20**, `chemin_0` **88,1 %, 6/14** ; `aug-pos` : `vers` **95,4 %, 13,3/20**,`
- **T1** `./journal/2026-10-27.md:36:| 09:49 | `b563a155` | B12 — PIPELINE M1→M4→M8 : 528/528, COMPLÉTION 96,3 %, PROTOYPES 7 |`
- **T1** `./journal/2026-10-27_docs.md:13:| 09:49 | `b563a155` | B12 — PIPELINE M1→M4→M8 : 528/528, COMPLÉTION 96,3 %, PROTOYPES 7 | `2026-10-27.md`, `2026-10-27_docs.md`, `2026-10-27_sprint-24h.md` (+3) |`
- **T1** `| complétion (champs) | **96,33 %** |`
- **T1** `- **M2** : lésions croisées des têtes ; ventrale 98,6 → 9,6 %, dorsale 93,2 → 0,7 %.`
- **T1** `- **M5** : sans transitions → 1,1 %.`
- **T1** `- **M6** : sans porte → 30 %.`
- **T1** `- **M8** : les 106 épisodes de test sont hors mémoire → 0 % ; les prototypes consolidés → 96,48 %.`
- **T1** `1. **M1** est un **hub de lecture fiable** : 528/528 avec contexte, 100 % en canonique et en invariance.`
- **T1** `2. **M4** est une **mémoire épisodique exacte** sur le corpus : rappel 1,0, complétion 97,9 %,`
- **T1** `ne bat pas la majorité ; la porte est à 70 % ; la neuromodulation ne change rien ; le sommeil dégrade.`
- **T1** `5. **M8** généralise aux épisodes non stockés : **96,48 %** contre **0 %** ; la consolidation résume, elle ne`
- **T1** `- **M2** est **valide** : la double dissociation est nette (`de` 93,2 %, lésion dorsale 0,7 %, lésion`
- **T1** `ventrale `action` 9,6 %) ; le point qui a débloqué est le **dernier état caché**, pas seulement la moyenne.`
- **T1** `415:            "M2 n'ajoute rien à la chaîne : M1 lit 100 % des 146 items réels, "`
- **T1** `416:            "M2 93–94 %, et aucun étage ne consomme M2. Remplacer M1 par M2 "`
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
- **T1** `143:**12,4 %** sur le proxy, M3 **0**, M4 **0**, M5 **?**, M6 **?**, M7 **?**, M8 **0**. M2 est un`
- **T1** `reports/rapport-jeux-symboliques.md:143:| plateau vide 5×5 | **25** coups légaux |`
- **T1** `reports/rapport-langues-maitres.md:149:10/10 contre 3/10. Sur 5×5, le plateau est trop petit : le bord est déjà le choix de la base, et la capture`
- **T1** `reports/rapport-pipeline-m2.md:25:| M5 `source` avec plateau | **18,70 %** (majoritaire 6,49 %) ; surprise **2,423** |`
- **T1** `reports/rapport-pipeline-m2.md:26:| M5 `source` sans plateau | **12,60 %** ; surprise **3,112** |`
- **T1** `> Résultat : **non**. M1 lit **100 %** des 146 items `de`/`vers` ; M2 lit **93,4 / 93,6 %** ; et`
- **T1** `| M1 avec contexte | **100 %** | **100 %** |`
- **T1** `| M1 sans contexte | 94,5 % | 94,5 % |`
- **T1** `| M2 avec contexte | **93,4 %** | **93,6 %** |`
- **T1** `| M2 sans contexte | 93,6 % | 93,6 % |`
- **T1** `- M2 **vu** : 126/126 ; **inédit couvert** : 79,5 % (`de`), 82,1 % (`vers`) ; **nouvelle classe** 0/7.`
- **T1** `| M5 `source` avec plateau | **18,70 %** (majoritaire 6,49 %) ; surprise **2,423** |`
- **T1** `| M5 `source` sans plateau | **12,60 %** ; surprise **3,112** |`
- **T1** `| M5 `source` sans transitions | 14,29 % |`
- **T1** `| M5 `source` M1 sans contexte | 28,03 % (n=396) — **artefact de couverture** |`
- **T1** `| M6 confluence | **94,32 %** |`
- **T1** `| M6 commutation | **94,95 %** |`
- **T1** `### Correction M5 : le 28,03 % est une perte de couverture`
- **T1** `Le « M1 sans contexte » de M5 ne lit que **396 pas sur 770** (couverture **51,4 %**) : seuls les`
- **T1** `référence fait exactement **28,03 %** : ce n'est pas un gain, c'est une **sélection**. Pour`
- **T1** ``cible`, le brut 13,10 % a une couverture de **74,5 %** ; `go` tombe à **0 %** avec une surprise`
- **T1** `de **18,21 nat**. Le chiffre honnête est donc **M5 sans contexte = 12,60 % sur 770**, pas 28,03 %.`
- **T1** `| M1 sans contexte | **70,83 %** (déficit 29,17) |`
- **T1** `| M2 lésion dorsale `de` | **2,05 %** (déficit 91,32) |`
- **T1** `| M2 lésion dorsale `vers` | **2,74 %** (déficit 90,87) |`
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
- **T1** `388-    Le suffixe est le dernier 20 % du flux ; la mémoire est gelée à la fin du`
- **T1** `390-    même capacité), avec le taux de gains et un IC 95 % normal.`
- **T1** `899-    préfixe. La mémoire est gelée à la fin du préfixe ; le suffixe (20 %) est`
- **T1** `682-        2. ``codes_tenus`` : 3 graines, 20 % des codes exclus par jeu, évaluation`

