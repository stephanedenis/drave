# Session 56f3ba0f — Dépôt /home/stephane/GitHub/Qtrinet, s

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `56f3ba0f-66b3-4728-a4cd-201951538ed1` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 10:30 |
| Durée | 0.9 h |
| Tours | 1 |
| Messages | 116 |
| Appels d'outils | 144 |
| Fichiers touchés | 7 |
| Commandes | 71 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Dépôt /home/stephane/GitHub/Qtrinet, sprint 24 h. Sous-agent A7 : améliorer M8 (sommeil/consolidation) et M9 (lésions), après les négatifs A2.  État A2 : - M8 `sommeil.py` : 96,48 % de champs, exact 65,1 %, baseline par jeu 96,10 %, 0 % exact sur codes jamais vus ; prototypes par (jeu, action). - M9 `lesion.py` : `batterie_lesions()` CPU, sham nul, M2 proxy bayésien. - Corpus : `semantique.typed_c … [1536 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Dépôt /home/stephane/GitHub/Qtrinet, sprint 24 h. Sous-agent A7 : améliorer M8 (sommeil/consolidation) et M9 (lésions),  … [1816 caractères tronqués]

*144 appels d'outils.* Actions notables :

- bash — List repo and cerveau structure
- bash — Line counts of key files
- read
- bash — Check base model and GPU availability
- bash — Read typed_corpus head
- bash — Read universaux
- bash — Read tests for sommeil and lesion
- bash — Corpus stats
- bash — Find base model provenance
- bash — Inspect synth corpus module
- bash — Look for voies tests
- bash — Count non-null fields in real corpus
- bash — Benchmark real voies M2 pipeline on GPU
- bash — Inspect code/paire mapping
- … et 108 autres

**Synthèse produite :**

⏵ Clôture A7 : résumé, chiffres et chemins

\## Résumé A7

**M8 — négatif net, et cette fois prouvé.** En leave-one-code-out sur les 29 codes du corpus (528 items), l'exact d'un prototype conditionné est **0,000 à chaque pli, par construction** : il ne peut rendre qu'un code déjà vu, et le code testé n'est pas dans le train. Les 3 graines à codes tenus à l'écart confirment (exact 0, zéro code test vu dans le train).

- Champs : global 74,94 %, `jeu` 89,20 %, `(jeu,action)` 89,20 %, `(jeu,action,type)` 88,97 %, backoff `type→groupe→jeu→global` 90,11 %.
- Non nuls : 4,60 / 61,26 / 59,71 / 59,02 / 63,51 %. Le conditionnement fin **perd** 0,23 pt de champs et 2,24 pts de non nuls ; le backoff ne regagne que le motif de `None` (+0,91 pt de champs, +2,24 pts de non nuls, +4,26 pts de coordonnées).
- Les non nuls justes sont `jeu` 100 %, `action` 93,1 %, `taille` 100 %, `symbole` 75 %, `chemin_0` 66,7 %, `de` 37,5 % (sous-type roque) ; `vers`, `point`, `carte`, `case`, `roque`, `promotion`, `passe` = **0 %**.
- Le 96,48 % / 65,1 % publié est **intra-code** : 106/106 codes de test sont dans le train, l'oracle par paire fait 100 %, et le plafond contextuel corpus vaut 57,95 % — sous le 65,1 %, donc la queue est un sous-ensemble favorable. Le split par paire fuit (61 à 109 items de test sur 108–151 ont un code vu).
- L'hybride historique est **tautologique** (clé = code cible entier) ; clé par surface, couverture 19,81 % sur la queue et **0 %** sur codes tenus.
- Contrôle clé permutée : la clé ne vaut que ~3 pts (87,83 → 84,69 %).

**M9 — le vrai `voies.py` tourne** (GPU Quadro RTX 5000, ~15 s train+éval, 300 pas, graine 1, torch seedé) : intacte action 98,63 / `de` 93,15 ; lésée ventrale 12,33 / 93,15 ; lésée dorsale 98,63 / 2,05 ; déficits `intacte−lésée` **+86,30** et **+91,10** ; double dissociation vraie. Réserve honnête : l'action est constante sur ce sous-ensemble, la majorité vaut 98,63 = le score intact, donc seule la tête `de` est informative.

Cohérence avec `batterie.py` (non modifié) : M1/M2/M3/M4/M5/M6/M8 concordent exactement. Audit : le seul `1−lésée` de `lesion.py` (M4 `par_champ`) est corrigé ; le M9 de `batterie.py` publie des scores bruts, pas des déficits (incohérence chiffrée, non corrigée car hors périmètre).

**Tests** : 85 tests OK en 28,2 s (dont 8 ajoutés), M2 réel inclus. Batterie M1–M8 complète en 26,85 s.

\## Chemins

- `/tmp/a7-m8-m9.json` — mesures complètes (M8 LOO/graines/contrôles/queue, M9 M2 réel, cohérence `batterie.py`, audit).

… [503 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py` | 0 | 20 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py` | 0 | 17 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py` | 0 | 5 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py` | 0 | 6 |
| `/tmp/a7_mesure.py` | 1 | 1 |
| `/tmp/a7_patch.py` | 1 | 0 |
| `/tmp/a7-m8-m9.md` | 2 | 0 |

### Commandes exécutées (échantillon)

- **T1** List repo and cerveau structure
- **T1** Line counts of key files
- **T1** Check base model and GPU availability
- **T1** Read typed_corpus head
- **T1** Read universaux
- **T1** Read tests for sommeil and lesion
- **T1** Corpus stats
- **T1** Find base model provenance
- **T1** Inspect synth corpus module
- **T1** Look for voies tests
- **T1** Count non-null fields in real corpus
- **T1** Benchmark real voies M2 pipeline on GPU
- **T1** Inspect code/paire mapping
- **T1** Run baseline cerveau test suite
- **T1** Read Predictif.evaluer
- **T1** Check M1/M6 intact values
- **T1** Inspect M7 deltas convention
- **T1** Grep for 1-minus patterns in lesion.py
- **T1** Explore modal mass per key
- **T1** Explore honest LOO ladder numbers
- **T1** Per-field LOO accuracy on held-out codes
- **T1** Measure hierarchical backoff ladder LOO
- **T1** Write partial JSON/MD deliverables
- **T1** Smoke-test experience_contexte
- **T1** Smoke-test experience_contexte
- **T1** Smoke-test experience_contexte
- **T1** Run experience_contexte and inspect outputs
- **T1** Re-read lesion header
- **T1** View M4 current code
- **T1** Locate M4/M8/battery line numbers
- **T1** Smoke-test battery with proxy M2
- **T1** Smoke-test battery with proxy M2
- **T1** Run real voies M2 lesion path
- **T1** Run real voies M2 lesion path
- **T1** Check refined verdict values
- **T1** Run sommeil tests
- **T1** Run lesion tests with proxy M2
- **T1** Re-run lesion tests with proxy M2
- **T1** Re-run lesion tests with proxy M2
- **T1** Identify missing deficit identity key
- … et 31 autres

## 4. Mesures et résultats marquants

- **T1** `Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1114.50it/s]`
- **T1** `387-    Le suffixe est le dernier 20 % du flux ; la mémoire est gelée à la fin du`
- **T1** `389-    même capacité), avec le taux de gains et un IC 95 % normal.`
- **T1** `Loading weights:  90%|█████████ | 81/90 [00:00<00:00, 800.31it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 878.15it/s]`
- **T1** `Loading weights:  78%|███████▊  | 70/90 [00:00<00:00, 697.86it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 830.81it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 922.68it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1053.82it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1004.54it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1137.30it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1033.57it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1142.02it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1125.47it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 991.49it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1071.76it/s]`
- **T1** `Loading weights: 100%|██████████| 90/90 [00:00<00:00, 964.59it/s]`
- **T1** `battery M8 note le sommeil porte la structure des champs (motif de None, +15,2 pts de champs et +58,9 pts de non nuls contre la marginale globale) ; il ne produit aucun code jamais vu (exact nul par c`
- **T1** `96,48 % publié est une **reconstruction intra-code** : ses 106 items de test`
- **T1** `+2,24 pts de non nuls, et les coordonnées du coup restent à 0 % hors`
- **T1** `couvre 0 % des codes tenus à l'écart.`
- **T1** `Double dissociation nette : lésion ventrale → action 98,63 → 12,33 % ; lésion`
- **T1** `9a3f753d B12 — M5 CONTEXTE : SOURCE +0,626 NAT, CIBLE +0,411 ; M6 SÉLECTEUR 94,95 % MAIS CONFLIT 0`

