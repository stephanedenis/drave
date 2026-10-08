# Session 67637ea9 — MISSION STRICTEMENT EN LECTURE SEULE.

| | |
|---|---|
| Identifiant | `67637ea9-78c6-4c20-a77c-0f90ee2a9ddc` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-08 09:19 |
| Durée | 0.0 h |
| Tours | 1 |
| Messages | 19 |
| Appels d'outils | 28 |
| Fichiers touchés | 0 |
| Commandes | 25 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — MISSION STRICTEMENT EN LECTURE SEULE. Tu ne dois RIEN écrire, RIEN modifier, RIEN exécuter qui écrive ou télécharge. Uniquement read/grep/glob et commandes bash de lecture (ls, wc, du, file, head). N'exécute AUCUN script Python du dépôt.  Dépôt : /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave, moteur d'inférence Rust dans drave-core/, outils Python dans tools/).  Tâche : trouver TOU … [2545 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — MISSION STRICTEMENT EN LECTURE SEULE. Tu ne dois RIEN écrire, RIEN modifier, RIEN exécuter qui écrive ou télécharge. Uni … [2825 caractères tronqués]

*28 appels d'outils.* Actions notables :

- bash — List repo root contents
- bash — List root py, src, sprints, colab
- bash — Find all py files outside tools
- bash — Grep training keywords outside tools
- read
- bash — Grep training keywords in root run scripts
- bash — Grep weight saving calls outside tools
- bash — Grep src and list other dirs
- bash — Check MLP usage and py files outside src
- bash — Grep colab notebook and Rust sources
- bash — Grep pont_semantique across repo
- bash — Check weight file existence
- bash — Inventory weight files maxdepth 4
- bash — Sample and count /tmp/drave artifacts
- … et 13 autres

**Synthèse produite :**

⏵ Résultat livré ; synthèse finale

**MISSION lecture seule respectée** : aucun script exécuté, seuls `ls/find/du/file/grep/sed/md5sum`.

**1) Seul apprentissage réel hors tools/ — `src/tiny_model.py`** (115 l., numpy pur)
- MLP 32→64→10 (LU l.22, 55), ReLU+softmax ; corpus **synthétique** : gaussiens 32 dims étiquetés en 10 classes par un professeur MLP **figé** (teacher_seed=1234, LU l.30-40).
- Loss = cross-entropy softmax, gradients à la main (LU l.97-104, 110) — **pas de torch/backward**.
- Optimiseur = SGD manuel `p -= lr*g` (LU l.105-106) ; défauts **epochs=300, lr=0.05, batch=128** (LU l.81) ; masques = « prune → retrain à masque fixe » (LU l.83-84, 107-109).
- **Aucun poids écrit** (grep np.save/savez/torch.save/state_dict/.npz/.pt hors tools = 0).

**2) Scripts racine qui l'appellent** (sortie = .md, jamais de poids) : `run_quantify.py` (l.40-47, 300 ép.), `run_clusters.py` (l.95, 140 ; 400 ép.), `run_precision.py` (l.105, retrain 150, lr 0.02), `run_encoding.py` (l.88, retrain 150), `run_sparsity.py` (build_and_train, 400 ép.).

**3) Inférence/mesure seulement** : run_8bit_perfection, run_cpu, run_harness, run_list_mode, run_real_clusters, run_value_encoding ; src/{bpe_np,encoding,gguf_min,roofline,sparsity,ternary,transformer_np}.py ; colab/Drave-reparti.ipynb (pilote réparti) ; drave-core/ (Rust : aucun backward/gradient/optimiseur, « optimisation » = perf, loss_log.bin = mesure) ; bench/*.c, sprints/ (31 .md), docs/reports/journal/data/models.

**4) Poids** : `…/stephane/pont_semantique.npz` 1 382 064 o 05-10 10:45 et `corpus/udhr/pont_semantique.npz` 1 382 064 o 05-10 10:47 (md5 **identiques**) ; `corpus/udhr/pont_semantique_r1.npz` 16 560 o 05-10 11:02. Écrits par `tools/pont_recurrent.py` l.192 (env `DRAVE_PONT_SORTIE`, ridge forme fermée), lus par `tools/applique_pont.py` l.58 ; r1 = `--rang 1` (**SUPPOSÉ**, seulement cité dans docs).

**5) /home/stephane/Data13TB/stephane/ maxdepth 4** : 19 fichiers, hors pont_semantique* rien de ML (model.pkl trombinoscope, dump_state.bin llama.cpp, .pkl equipment-hauru, .bin système).

**6) /tmp/drave*** : **11 573** entrées, **557 Mo** ; 11 563 .bin d'activations prof/fin (attn_brut 1290×2, comp 904×2, q/kv/qr 860×2, l/hc 430×2, idx 147×2) = dumps drave-core, pas des poids ; ex. `/tmp/drave_prof-attn_brut-0-0.bin` 131 072 o 02-10 15:28, `/tmp/drave_fin-attn_brut-0-0.bin` idem 15:23, `/tmp/drave-fige` 1 881 632 o 01-10 11:39 ; + drave.bundle 4,88 Mo, drave-fige2..6, drave_avant_iq1m, drave_avec_vb_jeté
… [233 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List repo root contents
- **T1** List root py, src, sprints, colab
- **T1** Find all py files outside tools
- **T1** Grep training keywords outside tools
- **T1** Grep training keywords in root run scripts
- **T1** Grep weight saving calls outside tools
- **T1** Grep src and list other dirs
- **T1** Check MLP usage and py files outside src
- **T1** Grep colab notebook and Rust sources
- **T1** Grep pont_semantique across repo
- **T1** Check weight file existence
- **T1** Inventory weight files maxdepth 4
- **T1** Sample and count /tmp/drave artifacts
- **T1** Inspect tmp drave families
- **T1** Grep tools savers and bench C
- **T1** List actual tmp drave names
- **T1** Sample tmp drave families with sizes
- **T1** Count training calls per run script
- **T1** Extract training constants
- **T1** Find r1 producer and pont readers
- **T1** Confirm r1 producer and file identity
- **T1** Read headers of non-training run scripts
- **T1** Check rang variable in pont_recurrent
- **T1** Check tmp drave extensions and samples
- **T1** Grep sprints for training mentions

## 4. Mesures et résultats marquants

- **T1** `./reports/rapport-toutes-langues.md:5634:Régression ridge en forme fermée, `ride = 1,0`. **300 traces** (50 articles × 6 langues),`
- **T1** `./reports/rapport-toutes-langues.md:5871:300 traces (50 articles × 6 langues), **164 775 positions**, fenêtre de 3 jetons, ridge 1,0 :`
- **T1** `./journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:873:1. **NVLink / 32 Go unifiés (faux).** Le Quadro RTX 5000 (Turing TU104) n'a pas de connecteur NVLink : le pont NVLink Turing Quadr`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:40973:location: https://cas-bridge.xethub.hf.co/xet-bridge-us/6aa49210e29d415b0d586896/251678a726c44fac5535e70869cbc79e0bb290f4352b974`
- **T1** `./journal/sessions/b13a6032-4f62-4e86-aa1f-03864a455c83/digest.md:1645:- Constantes : `OLLAMA = "/usr/lib/ollama"` l.22 ; `MODELE = .../Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf` l.23 ; `MMPROJ = .../mmproj-`
- **T1** `./journal/sessions/f2de810a-b765-444d-b3cc-d8fce1ba2105/digest.md:1408:- Constantes : `OLLAMA = "/usr/lib/ollama"` l.22 ; `MODELE = .../Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf` l.23 ; `MMPROJ = .../mmproj-`
- **T1** `./journal/sessions/f2de810a-b765-444d-b3cc-d8fce1ba2105/digest.md:1667:- Constantes : `OLLAMA = "/usr/lib/ollama"` l.22 ; `MODELE = .../Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf` l.23 ; `MMPROJ = .../mmproj-`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:11544:- Le pont rang-1 est l'artefact, et la sonde est un échec de protocole — dit tel quel  Artefact : pont_semantique_r1.npz (W0 89`
- **T1** `./REPRISE.md:184:> **L'artefact rang-1** : `/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz``
- **T1** `tools/compare_logits.py:87:    rang = 1 + sum(1 for v in ligne if v > ligne[cible])`
- **T1** `tools/discriminant_contenu.py:177:    print(f"\n# rang 0 = notre sortie · rang r = projection sur les r meilleures")`
- **T1** `tools/discriminant_transfert.py:184:    print(f"  {'NOTRE PONT (rang 0)':<20}{rn[0]:>10.1f}{rn[1]:>11.1f}{rn[2]:>10.3f}"`
- **T1** `tools/discriminant_transfert.py:210:        paires(clte, Mte, "rang 0 — NOTRE PONT")`
- **T1** `tools/energie_du_contenu.py:97:          f"rang utile (99 %) {int(np.searchsorted(np.cumsum(np.sort(w)[::-1])/w.sum(), 0.99))+1}")`
- **T1** `tools/etats_sans_langue.py:168:    print(f"\n# rang 0 = notre sortie actuelle, sans retrait.")`
- **T1** `tools/pont_fidele.py:5:LE SOUS-ESPACE du rang courant. Comparer un rang 1 et un rang 64 ainsi revient à`
- **T1** `W0 : 896 × 1        P : 896 × 1        moy : 896`
- **T1** `1. QUALITÉ — perplexité sur WikiText-2 (le standard léger, ~358 ko).`
- **T1** `20:Usage : pont_recurrent.py <dossier_train> <dossier_test> [--couche 10] [--rang 64]`
- **T1** `Usage : pont_recurrent.py <dossier_train> <dossier_test> [--couche 10] [--rang 64]`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : === .train( / build_and_train par fichier === run_8bit_perfection.py : 0 run_clusters.py : 2 run_cpu.py : 0 run_encoding.py : 3 run_harness.py : 0 run_list_mode.py : 0 run_precision.py : 3 run_quantif

