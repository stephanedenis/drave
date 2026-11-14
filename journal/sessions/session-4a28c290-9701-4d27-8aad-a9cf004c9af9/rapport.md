# Session session- — Fiche de coordination N2 : mètre eval_n2_propre

> **Journaux :** [le jour](../../2026-11-13/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-4a28c290-9701-4d27-8aad-a9cf004c9af9` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-13 21:38 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 82 |
| Appels d'outils | 115 |
| Fichiers touchés | 3 |
| Commandes | 77 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J4.1 : la coordination N2 — le mètre `eval_n2_propre.py` lit les checkpoints RoPE comme des positions absolues (8,02 au lieu de 2,79). **Ne modifie rien dans N2** (ni `entrainer_native.py`, ni `native_model.py`, ni `work/`). Écris une fiche de coordination `reports/rapport-coordination-n2.md` + JSON : le bug, le correctif proposé (--rope), les chiffres, la commande exacte pour la session N2.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J4.1 : la coordination N2 — le mètre `eval_n2_propre.py` lit les checkpoints RoPE comme des positions absolues (8, … [280 caractères tronqués]

*115 appels d'outils.* Actions notables :

- bash — List repository root
- bash — Show git status and recent commits
- glob
- read
- bash — Find N2 related files
- bash — Find RoPE code in native model
- bash — Find rope options in trainer
- bash — List work dirs and N2 artifacts
- bash — Inspect native model structure
- bash — Find python files mentioning rope
- bash — List N2 reports and recent journal days
- bash — List N2 work artifacts
- bash — Search documents for the numbers
- bash — Find references to eval_n2_propre
- … et 89 autres

**Synthèse produite :**

Fiche écrite, avec son JSON :

- `reports/rapport-coordination-n2.md`
- `reports/rapport-coordination-n2.json`

**Le résultat principal corrige la prémisse** : le bug a **deux** causes, pas une.

1. `charge()` construit `NativeModel` (positions absolues) au lieu de `NativeModelRoPE` ; `strict=False` charge les 127 clés sans alerte.
2. `ppl_protocole()` ne passe **pas le canal**, alors que `propre512-8k` a été entraîné avec `--canal data/corpus_propre/train.canal`.

Conséquence mesurée : **`--rope` seul rend 40,0658 à 128**, pas 2,79. Il faut `--rope --canal-dir` pour retrouver **2,9726 / 2,8988 / 2,8443 / 2,7856**.

Le piège de longueur est explicité : **8,02** est le `val` à **128** ; **2,79** est la PPL à **1 024**. À longueur égale 128, la référence est **2,9726**.

**Commande exacte pour la session N2, aujourd’hui sans patch** (elle donne 2,79) :

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 \
  ~/gpu-env/bin/python work/n2ac/eval_longueurs.py \
  work/n2ac/propre512-8k.pt --rope \
  --longueurs 128,256,512,1024 --val data/corpus_propre
```

Attendu : `2.9726 / 2.8988 / 2.8443 / 2.7856`.

La fiche contient aussi le diff proposé (`--rope`, `--canal-dir`, `--longueurs` liste avec 1024, garde-fou sidecar), la commande après patch, le test à 1 024 (`2,8566`, manque `0,3566`) et les contrôles négatifs (`1 692,39` / `1 880,66`).

**Aucun fichier de N2 modifié** (`native_model.py`, `entrainer_native.py`, `work/` intacts), aucun commit. Vérifications : JSON valide, `porte-tableaux` verte (tableaux + 3 847 liens). La revue de documentation signale seulement les deux compteurs à mettre à jour par la session principale : `713 → 714` fiches, `806 → 807` JSON.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/eval_n2_propre_rope.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md` | 1 | 14 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.json` | 1 | 6 |

### Commandes exécutées (échantillon)

- **T1** List repository root
- **T1** Show git status and recent commits
- **T1** Find N2 related files
- **T1** Find RoPE code in native model
- **T1** Find rope options in trainer
- **T1** List work dirs and N2 artifacts
- **T1** Inspect native model structure
- **T1** Find python files mentioning rope
- **T1** List N2 reports and recent journal days
- **T1** List N2 work artifacts
- **T1** Search documents for the numbers
- **T1** Find references to eval_n2_propre
- **T1** Find J4.1 task references
- **T1** Read J4.1 plan context
- **T1** List n2ac directory
- **T1** Read checkpoint sidecars
- **T1** Check GPU and python environment
- **T1** Reproduce absolute-position eval on RoPE checkpoint
- **T1** Reproduce RoPE meter onporte checkpoint
- **T1** Reproduce absolute eval on rope2048 checkpoint
- **T1** Reproduce RoPE eval on rope2048 checkpoint
- **T1** Inspect silent partial load mechanics
- **T1** Check existing coordination reports
- **T1** Find coordination fiche conventions
- **T1** Read task file report header
- **T1** Check date, branch, HEAD
- **T1** Read porte propre fiche header
- **T1** List J4 tasks and acceptance
- **T1** Inspect chantier work dir
- **T1** Check report/JSON pairing conventions
- **T1** Inspect etat-a JSON reference
- **T1** Read result naming convention
- **T1** Check absolute control checkpoint
- **T1** Verify checkpoints and sha256
- **T1** Measure wrong length curve on RoPE checkpoint
- **T1** Check absolute control with absolute meter
- **T1** Test RoPE model with eval_n2_propre protocol without canal
- **T1** Inspect gate training script for canal
- **T1** Read RoPE trainer
- **T1** Cross-check canal on/off with RoPE model
- … et 37 autres

## 4. Mesures et résultats marquants

- **T1** `9c7f71dc PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE`
- **T1** `reports/rapport-encodage.md:15:| non structuré | 2 | 49.6 % | 72.46 % | 1.50 | **5.02** | 18.02 | 2.00 | 1.22 | 2.0 |`
- **T1** `reports/rapport-e5-distillation.md:575:| **distillé, KL PLEIN**, taux 1e-3 *(le réglage publié)* | 748,02 | 561,11 | **24,9 %** | **38,9 %** |`
- **T1** `./reports/rapport-file-taches.md:51:| T09 | N2 | La porte propre (0,29 manquant à 2,7856) : données ou capacité | reports/n2-*, work/n2ac/, tools/entrainer_native.py, GPU | recette N2 1 024 | aucun ex`
- **T1** `./data/corpus_wiki_de/train.txt:2078305:Das Verfassungsreferendum auf den Komoren 2009 fand am 17. Mai 2009 statt. Die Wähler sollten über eine neue Verfassung abstimmen, die nach Meinung ihrer Befürw`
- **T1** `./data/corpus_wiki_de/train.txt:2248383:Der Guru Plug ist ein kompakter Plug Computer mit niedrigem Stromverbrauch, der mit einem auf Debian basierenden Linux-System ausgeliefert wird. Er wird von der`
- **T1** `[still running after 60000ms; moved to background job bash-13]`
- **T1** `0, Quadro RTX 5000, 154 MiB, 16384 MiB, 0 %`
- **T1** `1, Quadro RTX 5000, 4 MiB, 16384 MiB, 0 %`
- **T1** `reports/rapport-pont-semantique.md:261:aucune coordination ; seule la lecture `W` (64×896) s'ajuste, et ses blocs sont`
- **T1** `| T09 | N2 | La porte propre (0,29 manquant à 2,7856) : données ou capacité | reports/n2-*, work/n2ac/, tools/entrainer_native.py, GPU | recette N2 1 024 | aucun externe ; GPU libres (0 %) | python3 t`
- **T1** `> fenêtre est le **seul bras dont la courbe descend avec la longueur** : à octets égaux (33 Mo),`
- **T1** `> **capacité ne ferme pas la porte** : à fenêtre 512, init aléatoire et 33 Mo vus, 11,47 M donne`
- **T1** `corpus dédupliqué, split par chunks, **0 % de fuite**). La chaîne honnête y valait **3,0904** avec`
- **T1** `- **Deux bras à octets égaux** (33 Mo vus), RoPE, 34,3 M, lot 8, lr 3e-4, graine 1, init`
- **T1** `1. **fenêtre 512**, 8 000 pas × 8 × 512 ;`
- **T1** `2. **fenêtre 256** (seq 128), 32 000 pas × 8 × 128.`
- **T1** `82:  choisie à 5 %. **Ce n'est pas une mesure courante** : le JSON dit « pas de chiffre courant » ; la`
- **T1** `(règle) et A8.3a (régime 1 %) au HEAD.`
- **T1** `machine a 125 Go de RAM et 2 × 16 Go de VRAM, et trois fiches l'ont fait tourner.`
- **T1** `# Corpus : data/corpus_propre (train 3,24 Mo, val 180 Ko, 0 % de fuite — N2.h).`
- **T1** `# Deux bras à OCTETS ÉGAUX (33 Mo vus), init base-wiki-45m, canal :`
- **T1** `#   1. fenêtre 512, 8 000 pas × 8 × 512`
- **T1** `#   2. fenêtre 256 (seq 128), 32 000 pas × 8 × 128`
- **T1** `130:- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**`
- **T1** `36:| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art.,`
- **T1** `38:**État au 07/11 18 h 30.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) rég`
- **T1** `114:[N2] lasts 4 days and is 30% complete and is colored in #b26a00`
- **T1** `199:| **N2** | la distillation : corpus, professeur, [curriculum](../theorie/glossaire/entrees/curriculum.md) | 🔬 | **N2.h** — corpus dédupliqué (**0 %** de fuite) : la chaîne propre vaut **3,0904**, `
- **T1** `207:   jeu **contaminé à 32,8 %** — voir [N2.d](../../reports/rapport-n2-budget.md)) ; **N2.h3** montre que le`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : M docs/pilotage/references-non-regression.md D  journal/2026-11-13/README.md D  journal/2026-11-13/docs.md MM journal/README.md MM journal/THEMES.md MM journal/sessions/MANIFEST.md MM journal/sessions
- **T1** : (no output) [exit code: 1]
- **T1** : ls: cannot access 'reports/rapport-coordination-n2.*': No such file or directory [exit code: 2]

