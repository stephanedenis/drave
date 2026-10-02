# Session b13a6032 — Tu travailles dans le dépôt

| | |
|---|---|
| Identifiant | `b13a6032-4f62-4e86-aa1f-03864a455c83` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-02 15:03 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 17 |
| Appels d'outils | 43 |
| Fichiers touchés | 0 |
| Commandes | 5 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet. NE MODIFIE AUCUN FICHIER (lecture seule stricte).  MISSION : dépouiller l'EN-TÊTE (docstring de module, commentaires d'en-tête, constantes de tête) ET LA DÉFINITION DE LA LIGNE DE COMMANDE (argparse : `add_argument`, `help=`, `nargs`, `choices`, `default`) de ces 24 scripts Python, dans /home/stephane/Data13TB/stephane/Gi … [1978 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet. NE MODIFIE AUCUN FICHIER (lecture seule str … [2258 caractères tronqués]

*43 appels d'outils.* Actions notables :

- bash — Count lines in the 24 target scripts
- bash — Locate argparse and main blocks in all scripts
- read
- bash — List top-level constants in five scripts
- bash — Check undocumented flags and cluster output names
- bash — Inspect trace_compacite functions and session_report outputs
- send_message

**Synthèse produite :**

\### tools/aiguille.py  (219 lignes)
- Rôle : « Aiguille dans la botte de foin — version 2, celle qui mesure vraiment. » La perplexité ne dit pas si un modèle RETROUVE une information : plante un code (« AZUR-7391 ») à une profondeur donnée dans un contexte long, puis le redemande. Remplissage = vrai texte varié (`data/wikitext2_test.txt`), fenêtre différente par sonde ; réponse longue ; préremplissage par lots ; contexte réellement atteint relu dans la sortie du moteur.
- Positional args : `modele` (l.127), `longueurs` CSV de contextes (l.128), `profondeurs` CSV de fractions 0..1 (l.129). Usage docstring l.27-28.
- Options CLI : `--n` (int, 40, "jetons générés (réponse)") l.130 — `--threads` (int, 16, sans help) l.131 — `--lot` (int, 256, "lot de préremplissage") l.132 — `--timeout` (int, 7200, sans help) l.133 — `--gpu` (store_true, "DRAVE_GPU=1 (déport des projections)") l.134 — `--gpu-kv` (store_true, "DRAVE_GPU=1 DRAVE_GPU_KV=1 (KV en VRAM)") l.135 — `--attn-topk` (int, 0, "--attn-topk N (0 = attention complète)") l.140-141 — `--gpu-topk` (store_true, "DRAVE_GPU=1 DRAVE_GPU_KV=1 DRAVE_GPU_TOPK=1") l.142-143 — `--journal` (str, "", sans help) l.144. Contraintes : `--gpu-topk` exige `--attn-topk N` sinon ap.error (l.149-150) ; `--attn-topk` doit être ≥0 (l.151-152). Aucun `choices`/`nargs`.
- Constantes/vocabulaire de tête : `Q="./drave-core/target/release/drave"` l.41 ; `CORPUS="data/wikitext2_test.txt"` l.42 ; `CODE="AZUR-7391"` l.43 ; `AIGUILLE` l.44 ; `QUESTION` l.45-46 ; env DRAVE_GPU / DRAVE_GPU_KV / DRAVE_GPU_TOPK l.74-82.
- Formats lus/écrits : lit wikitext2 (normalisation `@-@ @,@ @.@`, l.53) ; lance le moteur `--infer --chat --flux --prompt --n --ctx --threads --temp 0 --lot [--attn-topk]` l.83-91 ; journal markdown `| contexte | profondeur | trouvé | secondes | détail |` l.205-215 ; `sys.exit(main())` l.219.

\### tools/analyse_empreinte.py  (208 lignes)
- Rôle : « Chiffrer l'empreinte mémoire d'un MoE depuis une trace de routage. » Rend : courbe succès/empreinte par couche, verdict sur l'allocation non uniforme, taille minimale utile d'un cache LRU, structure périodique (Jaccard par écart de couches), extrapolation.
- Positional : `trace` (l.70). Usage l.4-10.
- Options CLI : `--limite` (int, None, "ne lire que les N premiers jetons") l.71-72 — `--modele` (str, None, "nom d'un modèle connu pour l'extrapolation (deepseek4, deepseek41, qwen3moe)") l.73-75. Parser : `description=__doc__`, `RawDescriptionHelpFormatter` l.68-69.
- Constantes/vocabu
… [24251 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Count lines in the 24 target scripts
- **T1** Locate argparse and main blocks in all scripts
- **T1** List top-level constants in five scripts
- **T1** Check undocumented flags and cluster output names
- **T1** Inspect trace_compacite functions and session_report outputs

## 4. Mesures et résultats marquants

- **T1** `26:CHUNK = 256 << 20          # 256 Mo`

