# Session DSH — relecture

- identifiant : `dcaa24d6-0017-4382-be21-8244c0fb9b7a`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-02 15:03:48
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet. NE MODIFIE AUCUN FICHIER (lecture seule stricte).

MISSION : dépouiller INTÉGRALEMENT (fichiers courts : 48-132 lignes, lis-les en entier) ces 8 scripts shell dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ :
portes.sh, portes_formats.sh, verifier_table_types.sh, inventaire_modeles_lourds.sh, extraire_tables_ggml.sh, preparer_colab.sh, colab_cote_local.sh, sprint.sh.

Pour CHAQUE script, extraire :
1. Le rôle (commentaires d'en-tête, citer le texte).
2. TOUTES les variables d'environnement lues/écrites (DRAVE_*, MODEL*, etc.) avec fichier:ligne.
3. Tous les arguments positionnels / options (`$1`, `$2`, `case`, `getopts`, `--xxx`) avec fichier:ligne et rôle.
4. Toutes les commandes externes importantes invoquées (`python3 tools/...`, `cargo run`, `nvidia-smi`, `sha256sum`, `convert_hf_to_gguf.py`, `ssh`, etc.) avec les drapeaux passés et fichier:ligne.
5. Les fichiers/chemins d'entrée-sortie utilisés (modèles, JSON, logs) avec fichier:ligne.
6. Les seuils/constantes et listes de modèles codées en dur.

FORMAT DE SORTIE (texte brut, dense, pas d'introduction) : un bloc par script `### tools/nom.sh (N lignes)`, avec sous-puces : Rôle / Variables / Arguments / Commandes / Entrées-sorties / Constantes. Cite les numéros de ligne exacts. N'invente rien ; cite le texte source quand le rôle est ambigu. Sois exhaustif.
Your parent agent id is "f2de810a-b765-444d-b3cc-d8fce1ba2105". Before you finish, send your result to that agent with send_message({ agent_id: "f2de810a-b765-444d-b3cc-d8fce1ba2105", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

### 👤 Utilisateur

Current runtime context. This snapshot supersedes earlier runtime-context snapshots.

Current DSH file policy: danger-full-access. The DSH file sandbox does not restrict file modifications by available operations.

Approval prompts are disabled in this session: actions that require approval are rejected automatically — do not request sandbox escalation (do not set `sandbox_permissions`).

You are a delegated subagent: your permission scope was fixed when you were started and cannot be widened from inside this session — operations that require approval are rejected automatically. When the task needs access beyond that scope, do not retry the denied operation; state the limitation in your reply so the delegating agent can handle it.

### 👤 Utilisateur

<system-reminder>
A skill is a reusable set of task-specific instructions. The following skills are available in this session:

<available_skills>
- `microsoft-foundry`: Deploy, evaluate, fine-tune, and manage Foundry agents end-to-end with azd: hosted agent scaffold/run/deploy, prompt agent create, batch eval, continuous eval, prompt optimizer, Agent Optimizer scaffold, agent.yaml, dataset curation from traces, model fine-tuning (SFT/DPO/RFT). USE FOR: azd ai agent, azd provision/deploy, deploy agent, hosted agent, create agent, add tool to agent, invoke agent, evaluate agent, continuous eval, continuous monitoring, agent CI/CD, optimize prompt, improve prom...
</available_skills>

If the user names a skill, or the task clearly matches a skill's description, call the `skill` tool with the exact skill name before taking task actions. Load all applicable skills, then follow their full instructions. This catalog contains summaries only; do not infer or follow a skill's instructions until it has been loaded.
A user may also invoke a skill directly; its <skill_content> block then appears in this conversation. Follow it, and do not call the `skill` tool again for that skill.
</system-reminder>

### 🤖 Assistant

⏵ Reading the 8 shell scripts in full, starting with line counts.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && wc -l portes.sh portes_formats.sh verifier_table_types.sh inventaire_modeles_lourds.sh extraire_tables_ggml.sh preparer_colab.sh colab_cote_local.sh sprint.sh", "description": "Count lines of the 8 target scripts"}`

  ```
132 portes.sh
   74 portes_formats.sh
  121 verifier_table_types.sh
   48 inventaire_modeles_lourds.sh
   55 extraire_tables_ggml.sh
   54 preparer_colab.sh
   69 colab_cote_local.sh
   76 sprint.sh
  629 total
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/portes.sh"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/portes.sh</path>
<type>file</type>
<content>
1: #!/bin/bash
2: # Les portes du dépôt, en une commande.
3: #
4: # Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien :
5: # chaque porte est comparée à la valeur ATTENDUE, et le script sort en erreur si
6: # l'une diverge. Les valeurs sont celles publiées dans les rapports.
7: #
8: #   tools/portes.sh            toutes les portes
9: #   tools/portes.sh rapide     sans gpt-oss (le seul qui prenne ~20 min)
10: 
11: set -u
12: cd "$(dirname "$0")/.."
13: D=./drave-core/target/release/drave
14: RAPIDE=${1:-}
15: ECHEC=0
16: 
17: [ -x "$D" ] || { echo "compiler d'abord : (cd drave-core && cargo build --release)"; exit 2; }
18: 
19: compare() {  # nom, attendu, obtenu
20:     if [ "$2" = "$3" ]; then
21:         printf "  %-42s %s  ✅\n" "$1" "$3"
22:     else
23:         printf "  %-42s %s  ❌ (attendu %s)\n" "$1" "${3:-—}" "$2"
24:         ECHEC=1
25:     fi
26: }
27: 
28: # Attention : le moteur affiche AUSSI une perplexité cumulée par fenêtre, avant
29: # le total. Prendre la première occurrence du motif donnait 17,431 (fenêtre 1) au
30: # lieu de 19,3885 (t
… [5795 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the remaining 7 scripts in full.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/portes_formats.sh"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_table_types.sh"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/portes_formats.sh</path>
<type>file</type>
<content>
1: #!/usr/bin/env bash
2: # Portes des FORMATS : chaque déquantificateur comparé à libggml, bloc par bloc.
3: #
4: #   tools/portes_formats.sh [type ...]
5: #
6: # Pourquoi : nos déquantificateurs sont écrits d'après le C de ggml, et les cinq
7: # premiers essais se sont tous trompés (IQ2_XXS : pas de 8 octets sur `qs` ;
8: # IQ1_M : échelles lues en premier alors qu'elles sont en DERNIER ; Q2_K : indice
9: # d'échelle ; Q5_K : bits hauts relus au lieu d'avancés ; Q6_K : quants
10: # entrelacés au lieu de groupés). Aucun n'a été trouvé par relecture : tous l'ont
11: # été par comparaison à la bibliothèque. Cette porte rend la comparaison
12: # reproductible, et refuse de « passer » si le témoin a disparu du disque — un
13: # test qui saute est un test qui ne dit rien.
14: #
15: # La référence est liée à libggml (voir tools/ref_ggml_bloc.c).
16: set -u
17: cd "$(dirname "$0")/.."
18: RACINE=$PWD
19: MODELES=${DRAVE_MODELES:-/home/stephane/Data13TB/stephane/modeles/gguf}
20: LLAMA=${DRAVE_LLAMA:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}
21: REF=${REF_GGML_BLOC:-/t
… [3983 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_table_types.sh</path>
<type>file</type>
<content>
1: #!/bin/bash
2: # Confronte la table des tailles de types ggml du moteur à celle de `libggml`.
3: #
4: # Pourquoi cet outil existe : `octets_tensor` doit connaître, pour chaque type,
5: # le nombre de poids par bloc et la taille d'un bloc. Cette table est **relevée**
6: # depuis ggml et non devinée — mais rien n'empêche ggml d'ajouter un type demain,
7: # et un type absent est compté zéro octet. C'est exactement ainsi qu'un inventaire
8: # a annoncé 8,56 Go pour 86,9 Go de fichiers (les experts en `iq1_m`).
9: #
10: # Le moteur signale désormais un type inconnu ; cet outil dit lesquels manquent,
11: # en lisant la vérité dans la bibliothèque elle-même.
12: #
13: #   tools/verifier_table_types.sh [chemin de llama.cpp]
14: #
15: # Rend 0 si les tables concordent sur tous les types testés, 1 sinon.
16: 
17: set -u
18: cd "$(dirname "$0")/.."
19: RACINE=${1:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}
20: SRC=drave-core/src/gguf.rs
21: 
22: [ -d "$RACINE" ] || { echo "llama.cpp introuvable : $RACINE"; exit 2; }
23: [ -f "$SRC" ] || { echo "source introuvable :
… [4793 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Continuing with the next batch of scripts.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/inventaire_modeles_lourds.sh"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/extraire_tables_ggml.sh"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/inventaire_modeles_lourds.sh</path>
<type>file</type>
<content>
1: #!/bin/bash
2: # Inventorie les modèles lourds téléchargés et CONFRONTE les poids annoncés par
3: # les descripteurs GGUF aux tailles annoncées par HuggingFace.
4: #
5: # C'est la vérification croisée la plus large dont on dispose : si la table des
6: # types ggml était fausse d'un seul type, l'écart apparaîtrait sur des centaines
7: # de gigaoctets. Elle ne lit que les en-têtes (le plus gros fichier fait 366 Go).
8: #
9: #   tools/inventaire_modeles_lourds.sh [dossier]
10: 
11: set -u
12: cd "$(dirname "$0")/.."
13: D=${1:-/home/stephane/Data13TB/stephane/modeles/gguf}
14: BIN=./drave-core/target/release/drave
15: 
16: [ -x "$BIN" ] || { echo "compiler d'abord : cargo build --release"; exit 2; }
17: 
18: printf "%-28s %-12s %5s %8s %12s\n" "modèle" "architecture" "fich." "tenseurs" "poids lus"
19: printf -- "------------------------------------------------------------------------\n"
20: for d in "$D"/*/; do
21:     n=$(basename "$d")
22:     f=$(ls "$d"*.gguf 2>/dev/null | head -1)
23:     [ -z "$f" ] && continue
24:     # Un shard sur trois suffit : le le
… [1112 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/extraire_tables_ggml.sh</path>
<type>file</type>
<content>
1: #!/usr/bin/env bash
2: # Extrait les tables de ggml (grilles IQ) au format Rust, ou VÉRIFIE que celles
3: # embarquées dans drave-core/src/formats.rs sont bien celles de ggml.
4: #
5: #   tools/extraire_tables_ggml.sh            imprime le code Rust des tables
6: #   tools/extraire_tables_ggml.sh verifier   compare avec formats.rs (code 1 si écart)
7: #
8: # Pourquoi : ces tables font 4 à 16 Ko de constantes. Les recopier à la main est
9: # une faute qui ne se voit pas — une grille fausse d'une seule entrée donne des
10: # poids faux sur un seul motif de bits, donc une perplexité un peu haute et rien
11: # d'autre. La seule garantie utile est de pouvoir REDIRE d'où vient chaque
12: # valeur, et de comparer automatiquement.
13: set -eu
14: cd "$(dirname "$0")/.."
15: LLAMA=${DRAVE_LLAMA:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}
16: EXE=${TMPDIR:-/tmp}/extraire_tables_ggml
17: 
18: gcc -O2 -I"$LLAMA/ggml/include" -I"$LLAMA/ggml/src" tools/extraire_tables_ggml.c \
19:     -o "$EXE" -L"$LLAMA/build/bin" -lggml -lggml-base -Wl,-rpath,"$LLAMA/build/bin"
20: 
… [1293 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the final three scripts.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/preparer_colab.sh"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/colab_cote_local.sh"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/sprint.sh"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/preparer_colab.sh</path>
<type>file</type>
<content>
1: #!/bin/bash
2: # Prépare la répétition Colab : le dépôt en UN fichier, l'empreinte du modèle,
3: # et les commandes des deux côtés. Rien n'est envoyé nulle part — c'est vous qui
4: # téléversez, et le script vous dit quoi vérifier.
5: #
6: #   tools/preparer_colab.sh [modèle.gguf] [port]
7: set -u
8: cd "$(dirname "$0")/.."
9: MODELE=${1:-models/Qwen2.5-0.5B-Q8_0.gguf}
10: PORT=${2:-5599}
11: BUNDLE=/tmp/drave.bundle
12: 
13: echo "=== 1. le dépôt, en un fichier ==="
14: git bundle create "$BUNDLE" --all >/dev/null 2>&1 || { echo "échec du bundle"; exit 1; }
15: git bundle verify "$BUNDLE" 2>&1 | tail -1
16: echo "    $BUNDLE : $(stat -c%s "$BUNDLE") octets ($(du -h "$BUNDLE" | cut -f1))"
17: echo "    commit : $(git log --oneline -1)"
18: 
19: echo
20: echo "=== 2. le modèle (le MÊME des deux côtés) ==="
21: if [ -f "$MODELE" ]; then
22:     TAILLE=$(stat -c%s "$MODELE")
23:     EMPREINTE=$(sha256sum "$MODELE" | cut -c1-24)
24:     echo "    $MODELE : $((TAILLE / 1048576)) Mo"
25:     echo "    sha256 (24 premiers) : $EMPREINTE"
26:     echo "    → à coller dans la c
… [1386 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/colab_cote_local.sh</path>
<type>file</type>
<content>
1: #!/bin/bash
2: # Le côté LOCAL de la démonstration Colab : un nœud moteur qui écoute, et les
3: # trois façons de le rendre joignable depuis un runtime distant.
4: #
5: #   tools/colab_cote_local.sh [modèle.gguf] [port]
6: #
7: # Le script ne configure PAS le tunnel à votre place (il demande un compte, ou une
8: # machine publique) : il vérifie ce qui peut l'être, il lance le nœud, et il
9: # affiche la commande exacte à coller dans le notebook.
10: set -u
11: cd "$(dirname "$0")/.."
12: MODELE=${1:-models/Qwen2.5-0.5B-Q8_0.gguf}
13: PORT=${2:-5599}
14: BIN=./drave-core/target/release/drave
15: 
16: echo "=== 1. vérifications ==="
17: [ -x "$BIN" ] || { echo "  $BIN absent : lancez « cd drave-core && cargo build --release »"; exit 1; }
18: [ -f "$MODELE" ] || { echo "  $MODELE introuvable"; exit 1; }
19: echo "  binaire : $($BIN --version 2>/dev/null || echo 'drave')"
20: echo "  modèle  : $MODELE ($(( $(stat -c%s "$MODELE") / 1048576 )) Mo)"
21: echo "  sha256 (24 premiers, à coller dans la cellule 4 du notebook) :"
22: echo "            $(sha256sum "$MODELE" | cut
… [2261 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/sprint.sh</path>
<type>file</type>
<content>
1: #!/bin/bash
2: # Boxing temps réel d'un sprint de 2 h : démarrage, état, clôture avec la trame
3: # de cérémonie (revue · rétrospective · planning).
4: #
5: #   tools/sprint.sh start "<objectif du sprint>"
6: #   tools/sprint.sh status
7: #   tools/sprint.sh close
8: #   tools/sprint.sh list
9: #
10: # Le sprint vit dans `sprints/` : un fichier par sprint, et `COURANT` qui dit
11: # lequel tourne. La durée est de 2 h (SCRUM_DUREE pour un autre boxing, en
12: # secondes : SCRUM_DUREE=3600 pour une heure).
13: set -u
14: cd "$(dirname "$0")/.."
15: DUREE=${SCRUM_DUREE:-7200}
16: COURANT=sprints/COURANT
17: 
18: maintenant() { date +%s; }
19: hm() { date -d "@$1" +"%H:%M"; }
20: restant() { # secondes → « 1 h 07 »
21:     local s=$1
22:     if [ "$s" -lt 0 ]; then echo "dépassé de $(( -s / 60 )) min"; return; fi
23:     echo "$((s / 3600)) h $(printf %02d $(( (s % 3600) / 60 )))"
24: }
25: 
26: case "${1:-status}" in
27: start)
28:     objectif=${2:?"usage : sprint.sh start \"<objectif>\""}
29:     num=1
30:     [ -f "$COURANT" ] && num=$(( $(cut -d' ' -f1 "$COURANT") + 1 ))
31:
… [2633 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Grepping for env vars and command invocations to confirm exhaustiveness.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && for f in portes.sh portes_formats.sh verifier_table_types.sh inventaire_modeles_lourds.sh extraire_tables_ggml.sh preparer_colab.sh colab_cote_local.sh sprint.sh; do echo \"--- $f\"; grep -nE '\\$\\{?[A-Z_][A-Z0-9_]*' \"$f\"; d … [69 caractères tronqués]`

  ```
--- portes.sh
17:[ -x "$D" ] || { echo "compiler d'abord : (cd drave-core && cargo build --release)"; exit 2; }
51:v=$(timeout 600 $D models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt --ctx 256 \
57:if [ -d "$A" ]; then
58:    v=$(timeout 900 $D "$A" --ppl /tmp/ids_qwen.txt --ctx 64 --limit 8 --dense \
64:v=$($D models/Qwen2.5-0.5B-Q8_0.gguf --materiel 2>/dev/null | grep -oE "^  threads +: [0-9]+" | grep -oE "[0-9]+")
71:if [ "$RAPIDE" = "rapide" ]; then
89:    v=$($D "$2" --config 2>/dev/null | grep -oE "routage +: .*" | head -1)
96:route "GLM-5.3 : sigmoïde ×2,5" "$M/GLM-5.3-UD-IQ1_S/GLM-5.3-UD-IQ1_S-00001-of-00006.gguf" "sigmoïde"
97:route "Kimi-K2.7 : sigmoïde ×2,827" "$M/Kimi-K2.7-Code-UD-IQ1_M/Kimi-K2.7-Code-UD-IQ1_M-00001-of-00008.gguf" "sigmoïde"
98:route "V4-Flash : racine de softplus" "$M/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf" "racine de softplus"
99:route "Qwen3-235B : softmax" "$M/Qwen3-235B-A22B-Q2_K/Qwen3-235B-A22B-Instruct-2507-Q2_K-00001-of-00002.gguf" "softmax"
105:if [ "$RAPIDE" != "rapide" ]; then
107:    if [ -f "$O" ]; then
108:        v=$($D "$O" --config 2>/dev/null | grep -oE "calculable +: .*")
116:            $D "$O"
… [7282 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && for f in portes.sh portes_formats.sh verifier_table_types.sh inventaire_modeles_lourds.sh extraire_tables_ggml.sh preparer_colab.sh colab_cote_local.sh sprint.sh; do echo \"--- $f\"; grep -nE 'getopts|--[a-z]|nvidia-smi|sha256s … [176 caractères tronqués]`

  ```
--- portes.sh
17:[ -x "$D" ] || { echo "compiler d'abord : (cd drave-core && cargo build --release)"; exit 2; }
39:sortie=$( (cd drave-core && cargo test --release 2>&1) )
43:    printf "  %-42s %s  ✅\n" "cargo test --release" "${n} verts"
45:    printf "  %-42s %s  ❌ (échecs : %s)\n" "cargo test --release" "${n:-0} verts" "${ko:-?}"
51:v=$(timeout 600 $D models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt --ctx 256 \
52:    --abits 16 --threads 16 --limit 512 --dense 2>&1 | valeur)
58:    v=$(timeout 900 $D "$A" --ppl /tmp/ids_qwen.txt --ctx 64 --limit 8 --dense \
59:        --threads 8 --lot 1 2>&1 | valeur)
64:v=$($D models/Qwen2.5-0.5B-Q8_0.gguf --materiel 2>/dev/null | grep -oE "^  threads +: [0-9]+" | grep -oE "[0-9]+")
74:    if command -v gcc >/dev/null && [ -f tools/portes_formats.sh ]; then
75:        r=$(timeout 1800 bash tools/portes_formats.sh 2>&1 | tail -1)
89:    v=$($D "$2" --config 2>/dev/null | grep -oE "routage +: .*" | head -1)
101:# 7. gpt-oss : `--config` d'abord (gratuit), puis la perplexité (~20 min).
102:#    La porte `--config` existe parce qu'un refus FAUX est un refus trompeur :
108:        v=$($D "$O" --config 2>/dev/null | grep -oE "calculable +: .*
… [3149 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && grep -nE '^\\s*export|IFS=|LD_LIBRARY_PATH|TMPDIR' portes.sh portes_formats.sh verifier_table_types.sh inventaire_modeles_lourds.sh extraire_tables_ggml.sh preparer_colab.sh colab_cote_local.sh sprint.sh; echo \"[exit $?]\"", " … [50 caractères tronqués]`

  ```
portes_formats.sh:23:IFS=$'\n'
verifier_table_types.sh:53:LD_LIBRARY_PATH="$RACINE/build/bin" "$TMP/tailles" | sort -n > "$TMP/ggml.txt"
extraire_tables_ggml.sh:16:EXE=${TMPDIR:-/tmp}/extraire_tables_ggml
[exit 0]
  ```

### 🤖 Assistant

⏵ Sending the full report to the parent agent.

- **send_message** `{"agent_id": "f2de810a-b765-444d-b3cc-d8fce1ba2105", "message": "RAPPORT — 8 scripts shell de /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ (lecture seule, aucun fichier modifié). Tous lus intégralement.\n\n### tools/portes.sh (132 lignes)\n- Rôle : l.2-6 « Les portes du dépôt, en une comma … [21998 caractères tronqués]`

  ```
message delivered to agent f2de810a-b765-444d-b3cc-d8fce1ba2105
  ```

### 🤖 Assistant

⏵ Report sent to parent; delivering the same findings here.

### tools/portes.sh (132 lignes)
- **Rôle** : l.2-6 « Les portes du dépôt, en une commande. » / « Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien : chaque porte est comparée à la valeur ATTENDUE, et le script sort en erreur si l'une diverge. Les valeurs sont celles publiées dans les rapports. » Usage l.8-9 : `tools/portes.sh` (toutes) ou `tools/portes.sh rapide` (« sans gpt-oss (le seul qui prenne ~20 min) »).
- **Variables** : l.11 `set -u` ; l.12 `cd "$(dirname "$0")/.."` ; l.13 `D=./drave-core/target/release/drave` ; l.14 `RAPIDE=${1:-}` ; l.15 `ECHEC=0` ; l.39 `sortie` ; l.40 `n` ; l.41 `ko` ; l.51/58/64/75/89/108/119 `v`/`r`/`p` ; l.56 `A=/home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters-v2` ; l.65 `att=$(nproc); att=$((att / 2))` ; l.95 `M=/home/stephane/Data13TB/stephane/modeles/gguf` ; l.106 `O=.../gpt-oss-120b-MXFP4.gguf`. Aucune ENV DRAVE_*/MODEL* lue, aucun `export`.
- **Arguments** : `$1` → `RAPIDE` (l.14), seule valeur testée `rapide` (l.71, l.105). Pas de getopts. Paramètres internes : `$1/$2/$3` = nom/attendu/obtenu dans `compare()` (l.19-25) ; `$1/$2/$3` = nom/modèle/motif dans `route()` (l.87-94, appels l.96-99).
- **Commandes** : `cargo test --release` dans `drave-core` (l.39) ; `command -v gcc` (l.74) ; `bash tools/portes_formats.sh` sous `timeout 1800` (l.75) ; `nproc` (l.65) ; `$D` avec `--ppl /tmp/ids_qwen.txt --ctx 256 --abits 16 --threads 16 --limit 512 --dense` (l.51-52), `--ppl ... --ctx 64 --limit 8 --dense --threads 8 --lot 1` (l.58-59), `--materiel` (l.64), `--config` (l.89, l.108), `--tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_oss_512.txt` (l.116), `--ppl /tmp/ids_oss_512.txt --ctx 256 --dense --threads 16 --limit 512` (l.119-120) ; `timeout` 600/900/1800/2400 (l.51,58,75,119) ; pipes `grep -oE`/`head`/`cut` (l.31,40,41,46,64,89,108).
- **Entrées-sorties** : `models/Qwen2.5-0.5B-Q8_0.gguf` (l.51,64) ; `/tmp/ids_qwen.txt` (l.51,58) ; `$A` clusters Qwen3-30B (l.56,58) ; 4 GGUF sous `$M` (l.96-99) ; `$O` gpt-oss (l.106,108,116,119) ; `/tmp/wt2_txt.txt` (l.115) alimenté par `data/wikitext2_test.txt` (`head -c 20000`, l.115) ; `/tmp/ids_oss_512.txt` (l.114,116,118,119) ; `tools/portes_formats.sh` (l.74-75).
- **Constantes** : seuils tests `-ge 48` (l.42) et `ko -eq 0` (l.42) ; timeouts 600/900/1800/2400 (l.51,58,75,119) ; `--ctx 256` (l.51,119), `--ctx 64` (l.58) ; `--abits 16` (l.52) ; `--threads 16` (l.52,120), `8` (l.59) ; `--limit 512` (l.52,120), `8` (l.58) ; `--lot 1` (l.59) ; attendus `19.3885` (l.53), `799.8557` (l.60, « origine : 799,8557 »), `15.6017` (l.121) ; commentaire l.29-30 (17,431 = fenêtre 1, instrument faux) ; `head -5` (l.46) ; threads `>0` et `<= nproc/2` (l.65-66) ; motif formats `*"0 divergence(s), 0 absent(s)"*` (l.77) ; routages attendus `sigmoïde` (l.96,97), `racine de softplus` (l.98), `softmax` (l.99) ; gpt-oss `*": oui"*` (l.110) ; `exit 2` (l.17), `exit $ECHEC` (l.132). Modèles codés en dur : GLM-5.3-UD-IQ1_S-00001-of-00006 (l.96), Kimi-K2.7-Code-UD-IQ1_M-00001-of-00008 (l.97), DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003 (l.98), Qwen3-235B-A22B-Instruct-2507-Q2_K-00001-of-00002 (l.99).

### tools/portes_formats.sh (74 lignes)
- **Rôle** : l.2 « Portes des FORMATS : chaque déquantificateur comparé à libggml, bloc par bloc. » ; usage l.4 `tools/portes_formats.sh [type ...]` ; l.6-13 : cinq premiers essais faux (IQ2_XXS, IQ1_M, Q2_K, Q5_K, Q6_K), « refuse de « passer » si le témoin a disparu du disque — un test qui saute est un test qui ne dit rien. » ; l.15 « La référence est liée à libggml (voir tools/ref_ggml_bloc.c). »
- **Variables** : l.16 `set -u` ; l.17 cd racine ; l.18 `RACINE=$PWD` ; l.19 `MODELES=${DRAVE_MODELES:-/home/stephane/Data13TB/stephane/modeles/gguf}` (**DRAVE_MODELES**) ; l.20 `LLAMA=${DRAVE_LLAMA:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}` (**DRAVE_LLAMA**) ; l.21 `REF=${REF_GGML_BLOC:-/tmp/ref_ggml_bloc}` (**REF_GGML_BLOC**) ; l.22 `VERIF=tools/verifier_formats.py` ; l.23 `IFS=$'\n'` ; l.25 `ok=0; ko=0; abs=0` ; l.27 `BATTERIE` ; l.53 `filtre="${*:-}"` ; l.55-58 `lib/fich/tens/typ` ; l.65-66 `sortie`/`sortie2`. Aucun export.
- **Arguments** : tous les positionnels → `filtre="${*:-}"` (l.53), testé contre le libellé (l.59 `if [ -n "$filtre" ] && ! echo " $filtre " | grep -q " $lib "; then continue; fi`) ; valeurs = F32, F16, Q4_0, Q5_0, Q8_0, Q2_K, Q3_K, Q4_K, Q5_K, Q6_K, IQ2_XXS, IQ3_XXS, IQ1_S, IQ4_XS, IQ1_M, BF16, MXFP4. Pas de getopts/--options.
- **Commandes** : `gcc -O2 -I"$LLAMA/ggml/include" -I"$LLAMA/ggml/src" tools/ref_ggml_bloc.c -o "$REF" -L"$LLAMA/build/bin" -lggml -lggml-base -Wl,-rpath,"$LLAMA/build/bin"` (l.49-50, recompil si `-nt`, l.48 ; `|| exit 2` l.50) ; `python3 "$VERIF" "$fich" "$tens" 0` (l.65) et `... 7` (l.66), `tail -1` ; `cut -d'|' -f1..4 | xargs` (l.55-58) ; exigence `"CONCORDE"` sur les deux blocs (l.67).
- **Entrées-sorties** : 17 modèles sous `$MODELES` + `$RACINE/models/Qwen2.5-0.5B-Q4_0.gguf` (l.28-44) ; tenseurs : blk.0.attn_norm.weight (l.28), token_embd.weight (l.29-33,35), output.weight (l.32), blk.0.attn_output.weight (l.34), blk.0.ffn_down.weight (l.36,37), blk.0.ffn_gate_exps.weight (l.38,42), blk.1.ffn_down_exps.weight (l.39), blk.3.ffn_gate_exps.weight (l.40), blk.11.ffn_down_exps.weight (l.41), blk.0.ffn_gate_inp.weight (l.43), blk.0.ffn_down_exps.weight (l.44) ; témoin `$REF` (l.21,48,49) ; ligne finale l.73 `formats : $ok concorde(s), $ko divergence(s), $abs absent(s)` ; statut l.74 `[ $ko -eq 0 ] && [ $abs -eq 0 ]`.
- **Constantes** : type ggml par entrée : F32=0 (l.28), F16=1 (l.29), Q4_0=2 (l.30), Q5_0=6 (l.31), Q8_0=8 (l.32), Q2_K=10 (l.33), Q3_K=11 (l.34), Q4_K=12 (l.35), Q5_K=13 (l.36), Q6_K=14 (l.37), IQ2_XXS=16 (l.38), IQ3_XXS=18 (l.39), IQ1_S=19 (l.40), IQ4_XS=23 (l.41), IQ1_M=29 (l.42), BF16=30 (l.43), MXFP4=39 (l.44) ; blocs testés 0 et 7 (l.65-66) ; modèles : codestral-22b-v0.1-q4_k_m.gguf (l.28,35), bge-m3-FP16.gguf (l.29), qwen2.5-0.5b-instruct-q4_k_m.gguf (l.31,32,37), Qwen3-235B-A22B-Q2_K/...-00001-of-00002.gguf (l.33,34), Muse-Glimmer-30B-AD-Q4_K_M.gguf (l.36), DeepSeek-V4.1-Flash-Q2/DeepSeek-V4.1-Flash-Q2.gguf (l.38), Kimi-K2.7-Code-UD-IQ1_M-00002-of-00008.gguf (l.39), GLM-5.3-UD-IQ1_S-00002-of-00006.gguf (l.40), GLM-5.3-Flash-UD-IQ1_S-00002-of-00003.gguf (l.41), DeepSeek-V4-Flash-UD-IQ1_M-00002-of-00003.gguf (l.42,43), gpt-oss-120b-MXFP4.gguf (l.44).

### tools/verifier_table_types.sh (121 lignes)
- **Rôle** : l.2 « Confronte la table des tailles de types ggml du moteur à celle de `libggml`. » ; l.6-8 (« un inventaire a annoncé 8,56 Go pour 86,9 Go de fichiers (les experts en `iq1_m`) ») ; usage l.13 `tools/verifier_table_types.sh [chemin de llama.cpp]` ; l.15 « Rend 0 si les tables concordent sur tous les types testés, 1 sinon. »
- **Variables** : l.17 `set -u` ; l.18 cd racine ; l.19 `RACINE=${1:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}` ; l.20 `SRC=drave-core/src/gguf.rs` ; l.25 `TMP=$(mktemp -d)` ; l.26 `trap 'rm -rf "$TMP"' EXIT` ; l.81 `manquants=0; divergents=0; verifies=0` ; l.104 `inconnus=""` ; boucles `t`/`bloc`/`taille`/`ligne` (l.82-96, 105-109) ; `$2`/`$3` l.90-91 viennent de `set -- $ligne` (l.89), pas de la CLI. Aucune ENV, aucun export.
- **Arguments** : `$1` = chemin llama.cpp (l.19, défaut /home/.../llama.cpp) ; pas d'options.
- **Commandes** : `gcc -I"$RACINE/ggml/include" -I"$RACINE/ggml/src" "$TMP/tailles.c" -o "$TMP/tailles" -L"$RACINE/build/bin" -lggml -lggml-base` avec `2>"$TMP/gcc.err"` (l.50-51) ; `sed 's/^/  /' ... | head -5` (l.52) ; `LD_LIBRARY_PATH="$RACINE/build/bin" "$TMP/tailles" | sort -n > "$TMP/ggml.txt"` (l.53) ; `python3 - "$SRC"` heredoc (l.56-73) : isole `pub fn octets_tensor_opt` (l.60-61), regex `(\d+)(?:u64)?\s*=>\s*\(\s*(\d+)(?:u64)?\s*,\s*([^)]+?)\s*\)` (l.62), substitue `TAILLE_Q4K as u64`→144 (l.65), `TAILLE_Q6K as u64`→210 (l.66) ; `grep -E "^$t "` (l.83,106) ; printf l.85,91.
- **Entrées-sorties** : `$RACINE` + `drave-core/src/gguf.rs` (l.20) ; temporaires `$TMP/tailles.c` (l.29,50), `$TMP/tailles` (l.50,53), `$TMP/gcc.err` (l.51,52), `$TMP/ggml.txt` (l.53,83,109), `$TMP/rust.txt` (l.56,75,96,106) ; C embarqué l.29-49 (boucle `for (int t = 0; t <= 64; t++)` l.33 ; bornes l.44 `if (bs <= 0 || bs > 1024 || ts == 0 || ts > 1024) continue;` ; `printf("%d %lld %zu\n", t, (long long)bs, ts)` l.45).
- **Constantes** : 0..64 (l.33) ; ≤1024 (l.44) ; 144 (l.65), 210 (l.66) ; résumé l.111 `types confondus : $verifies · divergents : $divergents · absents du moteur : $manquants` ; avertissement l.114-118 (trous d'énumération, valeurs non initialisées) ; `head -5` (l.52) ; `exit 2` (l.22,23,52,77), `exit 1` si `divergents -gt 0` (l.120), `exit 0` (l.121).

### tools/inventaire_modeles_lourds.sh (48 lignes)
- **Rôle** : l.2-3 « Inventorie les modèles lourds téléchargés et CONFRONTE les poids annoncés par les descripteurs GGUF aux tailles annoncées par HuggingFace. » ; l.5-7 « si la table des types ggml était fausse d'un seul type, l'écart apparaîtrait sur des centaines de gigaoctets. Elle ne lit que les en-têtes (le plus gros fichier fait 366 Go). » ; usage l.9 `tools/inventaire_modeles_lourds.sh [dossier]`.
- **Variables** : l.11 `set -u` ; l.12 cd racine ; l.13 `D=${1:-/home/stephane/Data13TB/stephane/modeles/gguf}` ; l.14 `BIN=./drave-core/target/release/drave` ; l.21 `n` ; l.22 `f` ; l.25 `ligne` ; l.27 `arch` ; l.28 `nf` ; l.29 `nt` ; l.30 `go` ; Python : `m`, `par`, `total`, `f`, `k`. Aucune ENV, aucun export.
- **Arguments** : `$1` = dossier des modèles (l.13) ; pas d'options.
- **Commandes** : `timeout 600 "$BIN" "$f" --tensors` (l.25, stderr jeté) filtré `grep -E "·.*tenseurs" | head -1` (l.25) ; `ls "$d"*.gguf | head -1` (l.22) ; `cut -d' ' -f1` (l.27) ; `grep -oE "[0-9]+ fichiers"` (l.28), `"[0-9]+ tenseurs"` (l.29), `"[0-9.]+ Go de poids"` (l.30) ; `python3 - <<'PY'` (l.36) agrégeant `f['octets'] / 1e9` (l.38-47) ; message d'erreur `cargo build --release` (l.16).
- **Entrées-sorties** : `$D` + un `*.gguf` par sous-dossier (l.20-22) ; `tools/manifeste_modeles_lourds.json` (l.35, ouvert l.38) ; stdout : en-têtes l.18-19, lignes l.31 (`%10s Go`), bloc HuggingFace l.45-47.
- **Constantes** : `timeout 600` (l.25) ; `1e9` (l.42) ; formats `%-28s %-12s %5s %8s %12s` (l.18), `%8.1f Go` (l.45) ; `(illisible)` (l.26) ; `exit 2` (l.16).

### tools/extraire_tables_ggml.sh (55 lignes)
- **Rôle** : l.2-3 « Extrait les tables de ggml (grilles IQ) au format Rust, ou VÉRIFIE que celles embarquées dans drave-core/src/formats.rs sont bien celles de ggml. » ; usage l.5-6 (dump sans argument ; `verifier` « compare avec formats.rs (code 1 si écart) ») ; l.8-12 : tables de 4 à 16 Ko, « une grille fausse d'une seule entrée donne des poids faux sur un seul motif de bits, donc une perplexité un peu haute et rien d'autre. »
- **Variables** : l.13 `set -eu` ; l.14 cd racine ; l.15 `LLAMA=${DRAVE_LLAMA:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}` (**DRAVE_LLAMA**) ; l.16 `EXE=${TMPDIR:-/tmp}/extraire_tables_ggml` (**TMPDIR**) ; Python : `table`, `genere`, `embarque`, `noms`, `echec`, `a`, `b`, `ecarts`. Aucun export.
- **Arguments** : `$1` ; mode dump si `"${1:-}" != "verifier"` (l.21-24, `exit 0` l.23) ; sinon vérification ; code de sortie `sys.exit(echec)` (l.54).
- **Commandes** : `gcc -O2 -I"$LLAMA/ggml/include" -I"$LLAMA/ggml/src" tools/extraire_tables_ggml.c -o "$EXE" -L"$LLAMA/build/bin" -lggml -lggml-base -Wl,-rpath,"$LLAMA/build/bin"` (l.18-19) ; `"$EXE"` (l.22) ; `"$EXE" > "$EXE.rs"` (l.26) ; `python3 - "$EXE.rs" drave-core/src/formats.rs` heredoc (l.27-54), regex `pub static {nom}\s*:[^=]*=\s*\[(.*?)\n\];` (l.32), extraction `-?\d+` (l.35).
- **Entrées-sorties** : `tools/extraire_tables_ggml.c` (l.18) ; includes/lib de `$LLAMA` (l.18-19) ; exécutable `$EXE` (l.16,22,26) ; `$EXE.rs` (l.26,27) ; `drave-core/src/formats.rs` (l.27,44) ; stdout : code Rust (l.22) ou rapport (l.44,48,51-52).
- **Constantes** : `-O2`, `-Wl,-rpath` (l.18-19) ; tables comparées l.39 : `IQ2XXS_GRID`, `KSIGNS_IQ2XS`, `IQ1S_GRID`, `IQ3XXS_GRID`, `KVALS_IQ4NL` ; messages « MANQUANTE » (l.44), « identique (N valeurs) » (l.48), « DIVERGE : N valeur(s) sur M — premier écart » (l.51-52).

### tools/preparer_colab.sh (54 lignes)
- **Rôle** : l.2-4 « Prépare la répétition Colab : le dépôt en UN fichier, l'empreinte du modèle, et les commandes des deux côtés. Rien n'est envoyé nulle part — c'est vous qui téléversez, et le script vous dit quoi vérifier. » ; usage l.6 `tools/preparer_colab.sh [modèle.gguf] [port]`.
- **Variables** : l.7 `set -u` ; l.8 cd racine ; l.9 `MODELE=${1:-models/Qwen2.5-0.5B-Q8_0.gguf}` ; l.10 `PORT=${2:-5599}` ; l.11 `BUNDLE=/tmp/drave.bundle` ; l.22 `TAILLE=$(stat -c%s "$MODELE")` ; l.23 `EMPREINTE=$(sha256sum "$MODELE" | cut -c1-24)`. Aucune ENV, aucun export.
- **Arguments** : `$1` = .gguf (l.9) ; `$2` = port (l.10, défaut 5599) ; pas d'options.
- **Commandes** : `git bundle create "$BUNDLE" --all` (l.14, échec → `exit 1`) ; `git bundle verify "$BUNDLE" | tail -1` (l.15) ; `stat -c%s` (l.16,22) ; `du -h | cut -f1` (l.16) ; `git log --oneline -1` (l.17) ; `sha256sum | cut -c1-24` (l.23) ; here-doc l.33-41 : `cd $(pwd)/drave-core && cargo build --release` (l.34), `./target/release/drave ../$MODELE --flux-serveur 0.0.0.0:$PORT --ctx 256` (l.35) ; commentaires : `ngrok tcp $PORT` (l.37), `tailscale up` (l.38), `ssh -R $PORT:localhost:$PORT votre-vps` (l.39), `ss -ltn | grep $PORT` (l.40).
- **Entrées-sorties** : `$MODELE` (l.9,21,23,24,28,45) ; `/tmp/drave.bundle` (l.11,14,15,16,45) ; `colab/Drave-reparti.ipynb` (l.46) ; stdout sections 1-5 (l.13,20,32,44,48) + bloc ATTENDU l.49-54.
- **Constantes** : port 5599 (l.10) ; 1048576 (l.24) ; empreinte 24 car. (l.23,25) ; `--ctx 256` (l.35) ; l.26 « à coller dans la cellule 4 du notebook (constante ATTENDU) » ; attendus l.50-53 : `écart : 0.00e0 (mode dense : le transport f32 est sans perte)`, `LOTS de 64 jetons · ~229 000 octets par lot · 4 lots pour 256 jetons`, `~1,6 s de calcul local par LOT de 64 (12 couches)`, `~8 jetons/s` à 60 ms ; `exit 1` (l.14).

### tools/colab_cote_local.sh (69 lignes)
- **Rôle** : l.2-3 « Le côté LOCAL de la démonstration Colab : un nœud moteur qui écoute, et les trois façons de le rendre joignable depuis un runtime distant. » ; usage l.5 ; l.7-9 « Le script ne configure PAS le tunnel à votre place (il demande un compte, ou une machine publique) : il vérifie ce qui peut l'être, il lance le nœud, et il affiche la commande exacte à coller dans le notebook. »
- **Variables** : l.10 `set -u` ; l.11 cd racine ; l.12 `MODELE=${1:-models/Qwen2.5-0.5B-Q8_0.gguf}` ; l.13 `PORT=${2:-5599}` ; l.14 `BIN=./drave-core/target/release/drave` ; l.31 `NOEUD=$!` ; l.32 `i`. Aucune ENV, aucun export.
- **Arguments** : `$1` = modèle gguf (l.12) ; `$2` = port (l.13) ; pas d'options.
- **Commandes** : `$BIN --version` (l.19) ; `stat -c%s` (l.20) ; `sha256sum | cut -c1-24` (l.22) ; `pgrep -x drave` (l.23) ; `$BIN "$MODELE" --flux-serveur "0.0.0.0:$PORT" --ctx 256 > /tmp/noeud_colab.log 2>&1 &` (l.30) ; `for i in $(seq 1 60); do ss -ltn 2>/dev/null | grep -q ":$PORT " && break; sleep 0.5; done` (l.32) ; `ss -ltn | grep -q ":$PORT "` (l.33) ; `kill $NOEUD` (l.34,66) ; `trap ... INT TERM` (l.66) ; `while kill -0 $NOEUD; do sleep 2; done` (l.67) ; `tail -3 /tmp/noeud_colab.log` (l.69) ; here-doc l.40-54 : `ngrok tcp $PORT` (l.42), `tailscale up && tailscale ip -4` (l.45), `ssh -R $PORT:localhost:$PORT votre-vps` (l.48) ; conseil `cd drave-core && cargo build --release` (l.17).
- **Entrées-sorties** : `$MODELE` (l.12,18,20,22,30) ; `/tmp/noeud_colab.log` (l.30,34,36,69) ; stdout sections 1-4 (l.16,28,39,57) + bloc ATTENDU l.58-62 ; mentions notebook (l.21,43,46,49).
- **Constantes** : port 5599 (l.13) ; 1048576 (l.20) ; empreinte 24 car. (l.22) ; `--ctx 256` (l.30) ; `0.0.0.0` (l.29,30) ; 60×0,5 s ≈ 30 s (l.32) ; `sleep 2` (l.67) ; `tail -3` (l.69) ; attendus l.59-61 : `écart : 0.00e0`, `LOTS de 64 jetons · 229455 octets par lot · 4 lots`, `~1,6 s de calcul local par lot` ; « < 1 Mbit/s », « c'est la LATENCE qui décide » (l.52-53) ; `exit 1` (l.17,18,34).

### tools/sprint.sh (76 lignes)
- **Rôle** : l.2-3 « Boxing temps réel d'un sprint de 2 h : démarrage, état, clôture avec la trame de cérémonie (revue · rétrospective · planning). » ; usage l.5-8 (`start "<objectif du sprint>"`, `status`, `close`, `list`) ; l.10-12 « Le sprint vit dans `sprints/` : un fichier par sprint, et `COURANT` qui dit lequel tourne. La durée est de 2 h (SCRUM_DUREE pour un autre boxing, en secondes : SCRUM_DUREE=3600 pour une heure). »
- **Variables** : l.13 `set -u` ; l.14 cd racine ; l.15 `DUREE=${SCRUM_DUREE:-7200}` (**SCRUM_DUREE**) ; l.16 `COURANT=sprints/COURANT` ; `restant()` : `local s=$1` (l.21) ; start : `objectif` (l.28), `num` (l.29-30), `debut`/`fin` (l.31), `slug` (l.32), `fic` (l.33) ; status/close : `num/debut/fin` via `read -r` (l.46,56), `m` (l.47,57), `fic` (l.57). Aucun export.
- **Arguments** : `$1` = sous-commande via `case "${1:-status}"` (l.26) : `start` (l.27), `status` (l.44), `close` (l.54), `list` (l.72), `*` → usage + `exit 1` (l.75) ; `$2` = objectif obligatoire pour start (l.28 `objectif=${2:?"usage : sprint.sh start \"<objectif>\""}`) ; pas de getopts/--options.
- **Commandes** : `date +%s` (l.18) ; `date -d "@$1" +"%H:%M"` (l.19) ; `cut -d' ' -f1 "$COURANT"` (l.30) ; `tr`/`cut -c1-40`/`sed 's/-$//'` (l.32) ; `printf` (l.34,36-40,48,58,60-67) ; `head -3 "sprints/$(printf '%02d' "$num")-"*.md | tail -1` (l.49) ; `git log --oneline --since="@$debut" | wc -l` (l.51,62) ; `git log --oneline --since="@$debut" | sed 's/^/     /'` (l.52) ; `git log --format='- \`%h\` %s' --since="@$debut" | sed 's/^/  /'` (l.63) ; `ls sprints/$(printf '%02d' "$num")-*.md` (l.57) ; `rm -f "$COURANT"` (l.69) ; `head -1 "$f"` (l.73).
- **Entrées-sorties** : `sprints/COURANT` (l.16,30,34,45,46,55,56,69 ; contenu `"%s %s %s\n" num debut fin`, l.34) ; `sprints/%02d-%s.md` (l.33,41 `>`, l.68 `>>` ; relu l.49,57) ; `sprints/*.md` (l.73) ; stdout l.42,48-52,58,70,73.
- **Constantes** : `SCRUM_DUREE` défaut 7200 s = 2 h (l.15) ; 3600 (l.23) ; slug 40 car. (l.32) ; `%02d` (l.33,57) ; « boxing de %s min » (l.37-38) ; l.40 « **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité. » ; trame l.60-67 (« ## Revue — ce qui est livré, mesuré », `Durée : %s min (boxing %s min). Commits : %s.`, « ## Rétrospective — garder / changer » avec `- **Garder**`, `- **Changer**`, `- **Doute**`, « ## Planning — le sprint suivant », tableau `| # | chantier | critère de succès |`) ; `exit 0` (l.45,55), `exit 1` (l.75).

**Remarques transversales** : aucun des 8 scripts n'invoque `nvidia-smi`, `convert_hf_to_gguf.py`, `cargo run` ni `ssh` en exécution réelle (`ssh -R`/`ngrok`/`tailscale` ne figurent que dans des here-docs d'instructions : preparer_colab.sh l.37-40, colab_cote_local.sh l.42-48) ; `cargo` n'apparaît qu'en `cargo test --release` réel (portes.sh l.39) et en conseil `cargo build --release` (inventaire l.16, preparer_colab l.34, colab_cote_local l.17). ENV réellement lues : DRAVE_MODELES (portes_formats.sh:19), DRAVE_LLAMA (portes_formats.sh:20, extraire_tables_ggml.sh:15), REF_GGML_BLOC (portes_formats.sh:21), TMPDIR (extraire_tables_ggml.sh:16), SCRUM_DUREE (sprint.sh:15) ; LD_LIBRARY_PATH inline (verifier_table_types.sh:53) ; IFS modifié (portes_formats.sh:23) ; **aucun `export`** dans les 8 fichiers. Fichiers partagés : tools/ref_ggml_bloc.c et /tmp/ref_ggml_bloc (portes.sh:74-75 ↔ portes_formats.sh:15,48-50), tools/verifier_formats.py (portes_formats.sh:22), tools/extraire_tables_ggml.c (extraire_tables_ggml.sh:18), drave-core/src/formats.rs (extraire_tables_ggml.sh:27), drave-core/src/gguf.rs (verifier_table_types.sh:20), tools/manifeste_modeles_lourds.json (inventaire_modeles_lourds.sh:35,38), /tmp/noeud_colab.log + port 5599 (preparer_colab.sh ↔ colab_cote_local.sh). Aucun fichier modifié — lecture seule stricte respectée ; rapport transmis à l'agent parent `f2de810a-b765-444d-b3cc-d8fce1ba2105`.

