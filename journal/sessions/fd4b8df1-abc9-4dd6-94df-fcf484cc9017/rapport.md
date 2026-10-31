# Session fd4b8df1 — Nous sommes dans /home/stephane/GitHub/Q

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `fd4b8df1-abc9-4dd6-94df-fcf484cc9017` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 09:41 |
| Durée | 0.6 h |
| Tours | 1 |
| Messages | 68 |
| Appels d'outils | 90 |
| Fichiers touchés | 6 |
| Commandes | 70 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Nous sommes dans /home/stephane/GitHub/Qtrinet (dépôt Drave). Sprint autonome 24 h. Tu es un sous-agent chargé de M7 (neuromodulation), M8 (sommeil/consolidation) et M9 (lésions/ablations) du prototype `tools/cerveau/`.  État actuel mesuré : - M7 `tools/cerveau/neuromodulation.py` : mémoire bornée 16 places, rétention 3,64 % en FIFO = 3,64 % avec nouveauté ; aucun effet. - M8 `tools/cerveau/sommei … [2247 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Nous sommes dans /home/stephane/GitHub/Qtrinet (dépôt Drave). Sprint autonome 24 h. Tu es un sous-agent chargé de M7 (ne … [2527 caractères tronqués]

*90 appels d'outils.* Actions notables :

- bash — List cerveau prototype files
- bash — Check git status and recent log
- read
- bash — Read typed_corpus head
- bash — Read existing tests
- bash — Run baseline tests and check torch/model
- bash — Inspect corpus stats
- bash — Reproduce M8 baseline numbers
- bash — Reproduce M7 retention numbers
- bash — Look for a Python environment with torch
- bash — Search existing lesion references and M8 report
- bash — Read prior battery outputs
- bash — Check M8 report and envs
- bash — Check venv-drave for torch
- … et 64 autres

**Synthèse produite :**

⏵ Clôture M7/M8/M9 : vérification des livrables et résumé

Sprint M7/M8/M9 terminé. Livrables écrits et testés.

\## Chemins

- `/tmp/a2-m7-m8-m9.json` — résultats complets (M7 30 permutations, M8, M9, référence M2 CPU, limites)
- `/tmp/a2-m7-m8-m9.md` — rapport chiffré, commandes, verdicts, autocritique
- Code : `tools/cerveau/neuromodulation.py`, `tools/cerveau/sommeil.py`, `tools/cerveau/lesion.py`
- Tests : `tools/cerveau/tests/test_neuromodulation.py`, `test_sommeil.py`, `test_lesion.py`

\## Résultats

**M7 — négatif net.** Le banc historique était faux : `MemoireLimitee.stocker` gardait les 16 premiers arrivés (« gel »), pas FIFO. La métrique 3,64 % = 16/439 est le plafond mathématique : toutes les politiques l'atteignent, hasard compris. Sur 30 permutations appariées : LFU +23,1 pts de répétés ; nouveauté surface −19,6 pts ; incertitude −38,7 pts de suffixe code ; récompense (proxy `prendre`/`promouvoir`) −53,3 pts. Aucun signal neuromodulateur ne bat FIFO. La clé code (fifo_code) gagne +15,7 pts, mais ajouter la nouveauté à cette clé coûte −68,5 pts. Contrôle positif Zipf réussi (LFU +17,8, récompense informative +19,6, hasard −1,2).

**M8 — 96,48 % reproduit, mais ce n'est pas une généralisation.** Exact 65,09 % (pas 0 %), champs non nuls 85,96 %, dédup code 24,14 % d'exact. Baseline par jeu 96,10 % : le groupe action n'apporte que +0,38 pt. Un tirage aléatoire d'un code mémorisé par groupe fait 96,35 %. Sur codes tenus à l'écart, exact **0,0000** partout ; l'hybride prototypes+épisodes fait 100 % sur la queue uniquement parce que tous les codes y sont vus — c'est M4, pas le sommeil.

**M9 — `lesion.py`.** Batterie CPU en 6,9 s, sham nul partout, dose-réponse M3, contrôle positif M5, double dissociation M2. Déficits : M1 0,292 ; M2 0,524/0,630 ; M3 1,0 ; M4 1,0 ; M5 0,037 seulement (ordre 2 = 0) ; M6 0,193 ; M7 négatif (la modulation coûte) ; M8 0,184/0,651 sur codes vus, **0 sur codes neufs**. Référence `voies.py` CPU : action 98,63→10,96, de 91,78→0,68 ; le proxy M9 reproduit la structure, pas les magnitudes.

\## Tests

Mes 22 tests passent (5,22 s). La découverte complète (59 tests) échoue sur `test_voies.py`, ajouté par un autre sous-agent : il importe `torch` au niveau module, absent du `python3` du dépôt. Je ne l'ai pas modifié. `batterie.py` est intact ; sa table M9 reste l'ancienne (`1 − lésé`), à ne pas confondre avec `batterie_lesions()` (`intacte − lésée` + sham).

Aucun `git add/commit/checkout`, aucun `docs/`, `reports/`, `journal/` ou
… [22 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_neuromodulation.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** List cerveau prototype files
- **T1** Check git status and recent log
- **T1** Read typed_corpus head
- **T1** Read existing tests
- **T1** Run baseline tests and check torch/model
- **T1** Inspect corpus stats
- **T1** Reproduce M8 baseline numbers
- **T1** Reproduce M7 retention numbers
- **T1** Look for a Python environment with torch
- **T1** Search existing lesion references and M8 report
- **T1** Read prior battery outputs
- **T1** Check M8 report and envs
- **T1** Check venv-drave for torch
- **T1** Read brain modules report
- **T1** Inspect codecs API for confidence
- **T1** Read codecs head
- **T1** Inspect codecs package
- **T1** Read codecs init
- **T1** Measure codec confidence/ambiguity
- **T1** Read Lecture dataclass
- **T1** Estimate M7 suffix oracle and coverage
- **T1** Prototype M7 policies and metrics
- **T1** Run M7 paired permutations
- **T1** Benchmark M1 and M4 costs
- **T1** Measure M6/M5/M8 baselines and splits
- **T1** Compute M8 joint/hybrid/ablation baselines
- **T1** M8 conditional and deduplicated metrics
- **T1** Inspect base model config
- **T1** Time model load in venv
- **T1** Check synthetic corpus for M2
- **T1** Read synth corpus head
- **T1** Confirm legacy memory keeps first 16
- **T1** Start real M2 CPU training in background
- **T1** Run M7 experience and inspect
- **T1** Patch sort and rerun M7
- **T1** Patch synthetic control and run 30 perms
- **T1** Write partial JSON and MD for M7
- **T1** Write partial M7 markdown
- **T1** Patch and run M8 experience
- **T1** Fix sort and run M8
- … et 30 autres

## 4. Mesures et résultats marquants

- **T1** `8cf29faf B12 — M5 ORDRE 2 SANS GAIN, M7 NOUVEAUTÉ PAR SURFACE SANS EFFET ; M6 72,9 %`
- **T1** `091203d1 B12 — M2 ACTION 98,6 % / DE 93,2 % (LÉSIONS 19,2 / 3,4) ; M7 NUL À CAPACITÉ 16`
- **T1** `Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]`
- **T1** `Loading weights:  89%|████████▉ | 80/90 [00:00<00:00, 791.37it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 833.88it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 945.61it/s]`
- **T1** `38:- **M8** : les 106 épisodes de test sont hors mémoire → 0 % ; les prototypes consolidés → 96,48 %.`
- **T1** `48:   ne bat pas la majorité ; la porte est à 70 % ; la neuromodulation ne change rien ; le sommeil dégrade.`
- **T1** `49:5. **M8** généralise aux épisodes non stockés : **96,48 %** contre **0 %** ; la consolidation résume, elle ne`
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
- **T1** `Loading weights:  90%|█████████ | 81/90 [00:00<00:00, 796.64it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 875.71it/s]`
- **T1** `L.append(f"\n### Verdict M7\n\n- `{r['verdict']}`\n- La métrique historique 3,64 % est le plafond 16/439 : **toutes** les politiques l'atteignent (`plafond_surface_atteint_par_toutes`) ; elle ne peut `
- **T1** `- Plafonds : surface finale 3.6446% (16/439), code 55.17% (16/29).`
- **T1** `varie (`poser` 92 %, `passer` 8 %). Prédire `action` ne peut donc pas battre la`
- **T1** `classe majoritaire : le 98,9 % publié était le taux de cette constante.`
- **T1** `comparée à la langue cible. Son « exactitude » de 72,9 % était donc le taux du`
- **T1** `politique « toujours non » obtient 75 %, et chaque canal seul (langue ou sens)`
- **T1** `obtient 75 % aussi, avec 25 % de faux positifs. La seule politique qui dépasse`
- **T1** `le taux de base est la **conjonction** (sens ET langue) : exactitude 94,3 %,`
- **T1** `exactitude équilibrée 88,6 %, 0 faux positif, 5 faux négatifs. Les 5 FN sont`
- **T1** `"M5 : retirer les transitions ne change pas l'exact (98,93 % = majoritaire)",`
- **T1** `"M8 : l'exact sur codes jamais vus reste 0 %"`
- **T1** `| **M7** | rétention bornée, 30 permutations appariées | plafond surface **3,6446 %** = 16/439 ; aucun signal ne bat FIFO ; LFU = +24,4 pts de répétés ; nouveauté surface = −18,5 pts ; incertitude = −`
- **T1** `| **M8** | prototypes vs codes neufs | 96,48 % champs reproduit ; exact **65,09 %** (pas 0 %) ; non nuls **85,96 %** ; codes uniques **24,14 %** ; codes neufs exact **0 %** ; baseline per-game 96,10 %`
- **T1** `- Champs dominés par `None` : `de` 72,3 %, `vers` 72,3 %, `carte` 69,5 %, `case` 87,9 %, `symbole` 87,9 %, `point` 86,7 %, `chemin_0/1` 86,7 %, `taille` 83,5 %. 12/15 champs ont >98 % d'exactitude agr`
- **T1** `- **M8** : le split par codes tenus à l'écart a de petits tests (6 à 192 items) et les champs restent à ~93 % parce que la réponse est dominée par `None` ; l'exact 0 est le seul chiffre robuste.`
- **T1** `10:| **M7** | rétention bornée, 30 permutations appariées | plafond surface **3,6446 %** = 16/439 ; aucun signal ne bat FIFO ; LFU = +23,1 pts de répétés ; nouveauté surface = −19,6 pts ; incertitude `

## 5. Erreurs rencontrées

8 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] sed: can't read tools/jeux/codecs.py: No such file or directory [exit code: 2]
- **T1** : joint prototype: champs 0.9647798742138365 exact 0.6509433962264151 hybride: champs 1.0 exact 1.0 vus 106 / 106 global: champs 0.7805031446540881 exact 0.0 sham groupes mélangés: champs 0.749056603773
- **T1** : flux 528 t 0.59 [stderr] Traceback (most recent call last):   File "<stdin>", line 4, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", line 454, i
- **T1** : written 4.7 s -rw-r--r--. 1 stephane stephane 77657 27 oct 10:01 /tmp/a2-m7-m8-m9.json [stderr]   File "<stdin>", line 19     L.append(f"\n### Verdict M7\n\n- `{r['verdict']}`\n- La métrique historiqu
- **T1** : patched [stderr] Traceback (most recent call last):   File "<stdin>", line 3, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", line 351, in experience_m8 
- **T1** : patched [stderr] Traceback (most recent call last):   File "<stdin>", line 3, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", line 443, in batterie_lesion
- **T1** : patched [stderr] Traceback (most recent call last):   File "<stdin>", line 3, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", line 460, in batterie_lesion
- **T1** : -rw-r--r--. 1 stephane stephane 313 27 oct 09:55 /tmp/a2-m2-cpu.json -rw-r--r--. 1 stephane stephane 456 27 oct 09:55 /tmp/a2-m2-cpu.out   "de": 0.00684931506849315,   "n": 146  },  "secondes": 38.289

