# Session a117a3c1 — Dépôt /home/stephane/GitHub/Qtrinet, s

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `a117a3c1-8325-4a63-8e8f-14fea0bce484` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 10:30 |
| Durée | 0.7 h |
| Tours | 1 |
| Messages | 76 |
| Appels d'outils | 83 |
| Fichiers touchés | 4 |
| Commandes | 62 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Dépôt /home/stephane/GitHub/Qtrinet, sprint 24 h. Sous-agent A6 : tenter une dernière amélioration de M5/M6 après les négatifs A1, sans toucher aux autres modules.  État A1 : - M5 `predictif.py` : `action` constante ; `source` +6,1 pts mais mécanique ; `cible` surprisal −0,04 ; code observé sans plateau. - M6 `gating.py` : conjonction 94,3 % / base 75 %, commutation 0, 2 surfaces fr/en identiques. … [1623 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Dépôt /home/stephane/GitHub/Qtrinet, sprint 24 h. Sous-agent A6 : tenter une dernière amélioration de M5/M6 après les né … [1903 caractères tronqués]

*83 appels d'outils.* Actions notables :

- bash — List repo root and cerveau tools
- bash — Find M5 and M6 module files
- read
- bash — List tests and previous A1 artifacts
- bash — Read sequences module head
- bash — Read previous A1 report
- bash — Read M5 and M6 tests head
- bash — Inspect resume_contexte implementation
- bash — Inspect typed_corpus context fields
- bash — Read universaux head
- bash — Inspect A1 JSON structure
- todo_write
- bash — Locate oracle code in A1 script
- bash — Inspect battery M5/M6 interface
- … et 66 autres

**Synthèse produite :**

⏵ Résultat A6 : M5 gagne avec le plateau, M6 reste un sélecteur sans coût

**M5 — le plateau donne un gain réel de surprisal (3 graines, split 80/20 par partie)**

| cible / ordre | sans contexte | avec plateau (mélange 50/50) | gain |
|---|---:|---:|---:|
| source 1 | 3,224 nat / 10,6 % | 2,480 nat / 16,5 % | **+0,744 nat, +5,9 pt** |
| source 2 | 3,214 nat / 13,8 % | 2,468 nat / 17,4 % | **+0,747 nat, +3,6 pt** |
| cible 1 | 3,520 nat / 8,7 % | 3,031 nat / 12,3 % | **+0,489 nat, +3,6 pt** |
| cible 2 | 3,521 nat / 10,8 % | 3,016 nat / 14,6 % | **+0,504 nat, +3,8 pt** |

`action` est le témoin : les quatre bras y sont identiques (97,4 %, H = 0,087). Le masque ne s'applique pas à un label de format.

- **Oracle A1** : aucun bras ne le dépasse. Le masque uniforme seul l'atteint exactement à go (4,323 nat) et morpion (1,497 nat) ; le mélange comble 78 % (go), 98 % (morpion), 26–67 % (échecs/dames). L'écart restant est la géométrie des coups, pas le plateau.
- **Contrôle négatif** : contextes permutés (même distribution, mauvais pas) → source H ≈ 12,4 (Δ −9,2 nat), cible H ≈ 6,6 (Δ −3,1), exact 1,5–9,3 %. Le gain vient bien du **bon** plateau.
- **Baseline tour** : source 9,5 %, cible 7,7 % ; le contexte la dépasse, sauf `cible` aux échecs à l'exact (6,6 % contre 7,2 %), où la surprisal s'améliore quand même (3,89 → 3,60).
- **Intégration** : mode `Predictif(contexte=True, melange=0.5)` opt-in, défaut `contexte=False` pour ne pas modifier `batterie.m5` ni la lésion M5, qui n'ont pas été touchés.

**M6 — vraie porte de tâche (sens vs langue), conflit et commutation**

792 essais (352 switch / 352 repeat, 396 congruent / 396 incongruent), 9 blocs par groupe : 5 `sens`, 4 `langue`, ce qui équilibre exactement les transitions.

- Porte dure : **94,95 %**, conflit **0,000**, commutation **0,000** ; sens 100 %, langue 88,6 % (macro 92,5 %).
- Témoins : meilleur canal seul 77,8 %, indice aléatoire 73,5 %, inverse 50 %, tout-non 50 % → la consigne apporte +17,1 pt.
- Contrôle positif de persévération : coût de commutation **−44,3 pt**, congruent 0, incongrient −88,6 pt. L'instrument détecte un coût s'il y en a un ; la porte réelle n'en a pas.
- Canal lexical : 77,3 % d'identification sur 22 couples surface × langue ; la tâche langue monte à 88,6 % car c'est un jugement binaire. **Le canal lexical suffit à la tâche langue, pas au sens ; le contrôle exécutif se réduit à un sélecteur de canal**, sans inhibition ni commutation mesurables sur B7.

**Tests** : `PYTHONPATH=
… [713 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/a6_explore.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py` | 0 | 8 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py` | 0 | 5 |
| `/tmp/a6_m5_m6.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** List repo root and cerveau tools
- **T1** Find M5 and M6 module files
- **T1** List tests and previous A1 artifacts
- **T1** Read sequences module head
- **T1** Read previous A1 report
- **T1** Read M5 and M6 tests head
- **T1** Inspect resume_contexte implementation
- **T1** Inspect typed_corpus context fields
- **T1** Read universaux head
- **T1** Inspect A1 JSON structure
- **T1** Locate oracle code in A1 script
- **T1** Inspect battery M5/M6 interface
- **T1** Read A1 oracle implementation
- **T1** Print sample contexts and codes
- **T1** Print go and morpion contexts
- **T1** Find board index helpers in rules
- **T1** Read chess board index and RSN encoding
- **T1** Read battery M5/M6 functions
- **T1** Read A1 replay helper header
- **T1** Run plateau mask exploration
- **T1** Prototype learned geometry model for cible
- **T1** Rerun geometry model with positive mix
- **T1** Read working memory module
- **T1** Read lesion and battery M9
- **T1** Run existing M5 tests
- **T1** Run M6 switch task scratch
- **T1** Diagnose language channel error count
- **T1** Patch metrics and rerun M6
- **T1** Quick M5 arms check on one seed
- **T1** Fix OOV handling with context mask
- **T1** Add mask leak and rerun M5 arms
- **T1** Inspect M5 lesion code
- **T1** Read rest of M5 tests
- **T1** Add and run M5 context tests
- **T1** Fix and rerun M5 tests
- **T1** Check small-split context numbers
- **T1** Fix comparison and rerun M5 tests
- **T1** Read M6 test tail
- **T1** Add and run M6 switch tests
- **T1** Run full cerveau test discovery
- … et 22 autres

## 4. Mesures et résultats marquants

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
- **T1** `Plafond d'identifiabilité : 4 essais appariés (4 GO + 4 traduction, 2 codes × 2 langues) ne peuvent donner au mieux que 4/8 : l'exactitude maximale est 95.5 %. Au point de fonctionnement « rejeter les`
- **T1** `### L'ancienne mesure M6 (72,9 %) était un artefact`
- **T1** `Sur les 70 items fr/en de `typed_corpus` (55 fr, 15 en), l'ancienne porte donne 68.6 % à 70.0 % (moyenne 69.6 %) selon `PYTHONHASHSEED`, et un coût de commutation de -0.170 à -0.150. Le 72,9 % publié `
- **T1** ``Predictif()` a désormais pour cible par défaut `cible` (case d'arrivée), pas `action`. `batterie.m5` publiera donc ~12,5 % d'exact (gain +3,7 pt) au lieu de 98,9 %, et la lésion M9 `M5_sans_transitio`
- **T1** `- **Tient** : la tâche M6 est soluble et bien posée (conjonction 94,3 %, 0 FP) ; les politiques mono-canal sont au taux de base (75 %) ; le canal sens lit 20/20 textes ; la porte est déterministe.`
- **T1** `563-    (96,48 %) est rappelée pour mémoire : ses 106 codes sont tous dans le train,`
- **T1** `603-              "L'hybride 100 % de la queue est tautologique (clé = code cible) ; "`
- **T1** `604-              "clé par surface, sa couverture sur codes tenus est 0 %."))`
- **T1** `| action | 1 | sans | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |`
- **T1** `| action | 1 | masque_uniforme | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |`
- **T1** `| action | 1 | masque_hist | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |`
- **T1** `| action | 1 | masque_melange | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |`
- **T1** `| action | 2 | sans | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |`
- **T1** `| action | 2 | masque_uniforme | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |`
- **T1** `| action | 2 | masque_hist | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |`
- **T1** `| action | 2 | masque_melange | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |`
- **T1** `| source | 1 | sans | 843 | 10.6 % | 5.7 % | 3.224 | +0.376 | +0.000 | +0.000 |`
- **T1** `| source | 1 | masque_uniforme | 843 | 16.5 % | 5.7 % | 2.598 | +1.002 | +0.626 | +0.059 |`
- **T1** `| source | 1 | masque_hist | 843 | 16.5 % | 5.7 % | 2.686 | +0.914 | +0.539 | +0.059 |`
- **T1** `| source | 1 | masque_melange | 843 | 16.5 % | 5.7 % | 2.480 | +1.120 | +0.744 | +0.059 |`
- **T1** `| source | 2 | sans | 843 | 13.8 % | 5.7 % | 3.214 | +0.386 | +0.000 | +0.000 |`
- **T1** `| source | 2 | masque_uniforme | 843 | 17.4 % | 5.7 % | 2.598 | +1.002 | +0.617 | +0.036 |`
- **T1** `| source | 2 | masque_hist | 843 | 17.4 % | 5.7 % | 2.733 | +0.867 | +0.481 | +0.036 |`
- **T1** `| source | 2 | masque_melange | 843 | 17.4 % | 5.7 % | 2.468 | +1.132 | +0.747 | +0.036 |`
- **T1** `| cible | 1 | sans | 1498 | 8.7 % | 6.0 % | 3.520 | -0.088 | +0.000 | +0.000 |`
- **T1** `| cible | 1 | masque_uniforme | 1499 | 12.3 % | 6.0 % | 3.109 | +0.328 | +0.411 | +0.036 |`
- **T1** `| cible | 1 | masque_hist | 1498 | 12.3 % | 6.0 % | 3.208 | +0.223 | +0.312 | +0.036 |`
- **T1** `| cible | 1 | masque_melange | 1499 | 12.3 % | 6.0 % | 3.031 | +0.406 | +0.489 | +0.036 |`
- **T1** `| cible | 2 | sans | 1498 | 10.8 % | 6.0 % | 3.521 | -0.089 | +0.000 | +0.000 |`
- **T1** `| cible | 2 | masque_uniforme | 1499 | 14.6 % | 6.0 % | 3.109 | +0.328 | +0.412 | +0.038 |`
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
- **T1** `| action | 1 | masque_uniforme | 97.4 % | 0.087 | +0.000 |`
- **T1** `| action | 1 | masque_melange | 97.4 % | 0.087 | +0.000 |`
- **T1** `| action | 2 | masque_uniforme | 97.4 % | 0.087 | +0.000 |`
- **T1** `| action | 2 | masque_melange | 97.4 % | 0.087 | +0.000 |`
- **T1** `| source | 1 | masque_uniforme | 5.0 % | 12.075 | -8.851 |`
- **T1** `| source | 1 | masque_melange | 5.0 % | 12.031 | -8.806 |`
- **T1** `| source | 2 | masque_uniforme | 6.4 % | 12.071 | -8.856 |`
- **T1** `| source | 2 | masque_melange | 6.4 % | 12.015 | -8.801 |`
- **T1** `| cible | 1 | masque_uniforme | 8.4 % | 6.686 | -3.167 |`
- **T1** `| cible | 1 | masque_melange | 8.4 % | 6.603 | -3.083 |`
- **T1** `| cible | 2 | masque_uniforme | 9.3 % | 6.677 | -3.157 |`
- **T1** `| cible | 2 | masque_melange | 9.3 % | 6.584 | -3.063 |`
- **T1** `| action | 97.4 % | 100.0 % | 100.0 % | 90.8 % | 100.0 % |`
- **T1** `| source | 9.5 % | 7.1 % | 12.3 % | — | — |`
- **T1** `| cible | 7.7 % | 7.2 % | 11.5 % | 1.4 % | 11.6 % |`
- **T1** `| **porte de tâche** | 94.9 % | +0.000 | +0.000 |`
- **T1** `| sens | 77.8 % | -0.444 | +0.000 |`
- **T1** `| langue | 67.2 % | -0.429 | +0.000 |`
- **T1** `| tache_inversee | 50.0 % | -0.874 | +0.000 |`
- … (tronqué)

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : piece ('echecs', 'P') n 589 deltas 4 top [(-8, 314), (-16, 266), (-9, 6), (-7, 3)] piece ('echecs', 'n') n 199 deltas 8 top [(17, 77), (15, 69), (10, 15), (6, 12), (-17, 10), (-15, 9)] piece ('echecs'
- **T1** : ### source 1   sans exact=0.126 maj=0.065 H=3.112 gainH=+0.428 n=770   unif exact=0.087 maj=0.065 H=2.578 gainH=+0.961 n=770   hist exact=0.187 maj=0.065 H=2.570 gainH=+0.970 n=770   mix  exact=0.187 

