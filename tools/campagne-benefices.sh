#!/bin/bash
# campagne-benefices.sh — 24 h de mesures : où Drave est à son meilleur, tâche par tâche.
#
# POURQUOI CETTE CAMPAGNE. Le dépôt a mesuré beaucoup de choses, mais presque
# toujours sur UN modèle (Qwen2.5-0.5B) et UN type de tâche (la perplexité). La
# question posée est plus large : pour quelles TÂCHES l'architecture par listes
# est-elle le bon outil, et de combien ? Ce script parcourt les familles
# disponibles sur cette machine et consigne, pour chacune, la mesure qui décide.
#
# Chaque étape : un journal, un délai maximal, et une ligne de synthèse. Une
# étape qui échoue n'arrête pas la file — elle est consignée comme échouée.
#
#   tools/campagne-benefices.sh              toute la file
#   tools/campagne-benefices.sh grille       une seule étape
#   tools/campagne-benefices.sh --liste      les étapes disponibles
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
C=${CAMPAGNE_DIR:-/tmp/campagne24}
G=/home/stephane/Data13TB/stephane/modeles/gguf
mkdir -p "$C"
JOURNAL="$C/journal.txt"

dire() { echo "[$(date '+%d/%m %H:%M:%S')] charge $(cut -d' ' -f1 /proc/loadavg) · $*" | tee -a "$JOURNAL"; }

# LES IDENTIFIANTS SE TOKENISENT AVEC LE MODÈLE QUI VA LES LIRE.
# `data/wikitext2_test.txt.ids` existe dans le dépôt, mais il vient d'un AUTRE
# tokenizer (il commence par 201,438,10498… là où Qwen2.5 produit
# 198,284,8397…). Le donner à Qwen2.5-0.5B ne mesure pas le modèle : il mesure
# la perplexité d'un texte découpé par quelqu'un d'autre — **7710** au lieu de
# **17,43**, sur les mêmes octets. Toute la campagne serait partie de là.
ids_pour() {  # ids_pour <nom> <modele> <corpus>
    local sortie="$C/ids_$1.txt"
    if [ ! -s "$sortie" ]; then
        "$D" "$2" --tokenize --fichier "$3" --sortie "$sortie" >/dev/null 2>&1 \
            || { dire "ids/$1 : tokenisation impossible"; return 1; }
    fi
    printf '%s' "$sortie"
}

# ----------------------------------------------------------------- étape 1
# GRILLE DE MODÈLES : « ce modèle tourne-t-il, et à quel prix ? »
# On mesure, pour chaque famille disponible : le chargement, la mémoire
# résidente, les octets lus, le débit et la perplexité. C'est la table qui dit
# ce que la niche « modèle plus gros que la RAM » vaut, modèle par modèle.
etape_grille() {
    local corpus=data/wikitext2_test.txt
    local modeles=(
        "0.5B-Q8|models/Qwen2.5-0.5B-Q8_0.gguf|600"
        "r1-1.5B|$G/deepseek-r1-distill-qwen-1.5b-q4_k_m.gguf|900"
        "r1-14B|$G/deepseek-r1-distill-qwen-14b-q4_k_m.gguf|1800"
        "codestral-22B|$G/codestral-22b-v0.1-q4_k_m.gguf|1800"
        "qwen3-30B-A3B|/home/stephane/FastNVMe/qwen3-30b-a3b-Q4_K_M.gguf|1800"
        "gpt-oss-120B|$G/gpt-oss-120b-MXFP4.gguf|5400"
    )
    for entree in "${modeles[@]}"; do
        IFS='|' read -r nom chemin delai <<< "$entree"
        [ -f "$chemin" ] || { dire "grille/$nom : fichier absent ($chemin)"; continue; }
        local ids="$C/ids_$nom.txt"
        if [ ! -s "$ids" ]; then
            "$D" "$chemin" --tokenize --fichier "$corpus" --sortie "$ids" \
                > "$C/grille_${nom}_tokenize.log" 2>&1 \
                || { dire "grille/$nom : tokenisation impossible (tokenizer non couvert ?)"; continue; }
        fi
        # 256 jetons, contexte 256 : la référence du dépôt, comparable d'un
        # modèle à l'autre. `/usr/bin/time -v` donne le RSS et les octets lus.
        /usr/bin/time -v timeout "$delai" "$D" "$chemin" --ppl "$ids" \
            --limit 256 --ctx 256 --threads 20 \
            > "$C/grille_${nom}_ppl.log" 2> "$C/grille_${nom}_temps.log"
        local code=$?
        local ppl rss lus
        ppl=$(grep -oE "perplexité [0-9.]+ sur" "$C/grille_${nom}_ppl.log" | grep -oE "[0-9.]+" | tail -1)
        rss=$(grep -oE "Maximum resident set size \(kbytes\): [0-9]+" "$C/grille_${nom}_temps.log" | grep -oE "[0-9]+$")
        lus=$(grep -oE "File system inputs: [0-9]+" "$C/grille_${nom}_temps.log" | grep -oE "[0-9]+$")
        dire "grille/$nom : code $code · PPL ${ppl:-?} · RSS $(( ${rss:-0} / 1024 )) Mo · lus $(( ${lus:-0} / 2048 )) Mio"
    done
}

# ----------------------------------------------------------------- étape 2
# PARCIMONIE SUR UN VRAI MODÈLE : « le coût suit-il l'activité ? »
# Seuil et k-WTA, puis le même calcul en dense et en listes. C'est la promesse
# fondatrice du projet, mesurée sur un modèle non entraîné pour ça.
etape_parcimonie() {
    local m=models/Qwen2.5-0.5B-Q8_0.gguf
    local ids
    ids=$(ids_pour 0.5B-Q8 "$m" data/wikitext2_test.txt) || return 1
    for reglage in "--act-thresh 0" "--act-thresh 0.001" "--act-thresh 0.005" \
                   "--act-thresh 0.01" "--act-thresh 0.02" "--act-thresh 0.05" \
                   "--act-topk 1000" "--act-topk 900" "--act-topk 850" "--act-topk 800" \
                   "--act-topk 700" "--act-topk 500"; do
        for chemin in "--dense" "--push"; do
            local etiquette
            etiquette=$(echo "$reglage $chemin" | tr -d ' -' | tr '.' '_')
            timeout 300 "$D" "$m" --ppl "$ids" --limit 256 --ctx 512 --threads 20 \
                $reglage $chemin > "$C/parcimonie_$etiquette.log" 2>&1
            local ppl ev ts
            ppl=$(grep -oE "perplexité [0-9.]+ sur" "$C/parcimonie_$etiquette.log" | grep -oE "[0-9.]+" | tail -1)
            ev=$(grep -oE "\((\s*[0-9]+) événements" "$C/parcimonie_$etiquette.log" | grep -oE "[0-9]+" | head -1)
            ts=$(grep -oE "[0-9.]+ tok/s effectifs" "$C/parcimonie_$etiquette.log" | grep -oE "^[0-9.]+")
            dire "parcimonie/$etiquette : PPL ${ppl:-?} · événements ${ev:-?} · ${ts:-?} tok/s"
        done
    done
}

# ----------------------------------------------------------------- étape 3
# CONTEXTE LONG : le cache KV est le seul poste qui grandit avec l'usage.
etape_contexte() {
    local m=models/Qwen2.5-0.5B-Q8_0.gguf
    local ids
    ids=$(ids_pour 0.5B-Q8 "$m" data/wikitext2_test.txt) || return 1
    for ctx in 512 1024 2048 4096 8192; do
        /usr/bin/time -v timeout 900 "$D" "$m" --ppl "$ids" --limit 256 --ctx "$ctx" \
            --threads 20 > "$C/contexte_$ctx.log" 2> "$C/contexte_${ctx}_temps.log"
        local ppl rss kv
        ppl=$(grep -oE "perplexité [0-9.]+ sur" "$C/contexte_$ctx.log" | grep -oE "[0-9.]+" | tail -1)
        kv=$(grep -oE "cache KV : [0-9]+ bits" "$C/contexte_$ctx.log" | head -1)
        rss=$(grep -oE "Maximum resident set size \(kbytes\): [0-9]+" "$C/contexte_${ctx}_temps.log" | grep -oE "[0-9]+$")
        dire "contexte/$ctx : PPL ${ppl:-?} · $kv · RSS $(( ${rss:-0} / 1024 )) Mo"
    done
}

# ----------------------------------------------------------------- étape 4
# PRÉREMPLISSAGE PAR LOTS : l'axe 1 de la feuille de route. Un lot partage les
# octets du dense entre ses jetons ; c'est le seul levier qui multiplie un débit
# de DISQUE.
etape_lot() {
    local m=models/Qwen2.5-0.5B-Q8_0.gguf
    local ids
    ids=$(ids_pour 0.5B-Q8 "$m" data/wikitext2_test.txt) || return 1
    for lot in 1 2 4 8 16 32 64; do
        timeout 900 "$D" "$m" --ppl "$ids" --limit 512 --ctx 512 --threads 20 \
            --lot "$lot" > "$C/lot_$lot.log" 2>&1
        local ppl ts
        ppl=$(grep -oE "perplexité [0-9.]+ sur" "$C/lot_$lot.log" | grep -oE "[0-9.]+" | tail -1)
        ts=$(grep -oE "[0-9.]+ tok/s effectifs" "$C/lot_$lot.log" | grep -oE "^[0-9.]+")
        dire "lot/$lot : PPL ${ppl:-?} · ${ts:-?} tok/s"
    done
}

# ----------------------------------------------------------------- étape 5
# ROUTAGE D'EXPERTS : combien d'experts se réveillent, et quel volume circulerait
# si on les répartissait entre machines ? C'est la mesure qui décide de la
# granularité de la distribution.
etape_routage() {
    local m=/home/stephane/FastNVMe/qwen3-30b-a3b-Q4_K_M.gguf ids="$C/ids_qwen3-30B-A3B.txt"
    [ -s "$ids" ] || "$D" "$m" --tokenize --fichier data/wikitext2_test.txt --sortie "$ids" >/dev/null 2>&1
    timeout 1800 "$D" "$m" --ppl "$ids" --limit 128 --ctx 128 --threads 20 \
        > "$C/routage_30b.log" 2>&1
    dire "routage/30B : $(grep -oE 'experts [0-9.]+ M' "$C/routage_30b.log" | tail -1) · $(grep -oE 'perplexité [0-9.]+' "$C/routage_30b.log" | tail -1)"
    # Et la même chose sur le modèle ROUTÉ qu'on a entraîné, s'il est là.
    if [ -f /tmp/m4_route.gguf ]; then
        timeout 300 "$D" /tmp/m4_route.gguf --ppl "$C/ids_m4route.txt" --limit 128 --ctx 128 --threads 8 \
            > "$C/routage_modele.log" 2>&1
        dire "routage/modèle entraîné : $(grep -oE 'experts [0-9.]+ M' "$C/routage_modele.log" | tail -1)"
    fi
}

# ----------------------------------------------------------------- étape 6
# SÉMANTIQUE MULTILINGUE : le résultat publié (bande 10-15) a été calculé avec
# un lecteur qui IGNORAIT l'échelle par enregistrement. On le refait avec la
# correction et sans elle — la question est : le résultat survit-il ?
etape_semantique() {
    local t=/home/stephane/Data13TB/stephane/corpus/udhr
    for variante in "" "--sans-echelle"; do
        local etiquette
        etiquette=$(echo "sem${variante}" | tr -d ' -')
        timeout 3600 /home/stephane/gpu-env/bin/python tools/premiere_couche_semantique.py \
            "$t/article1_traces" "$t/article2_traces" --max-paires 40000 $variante \
            > "$C/${etiquette}.log" 2>&1
        dire "sémantique/${etiquette} : code $? · $(grep -c . "$C/${etiquette}.log") lignes"
    done
}

# ----------------------------------------------------------------- étape 7
# LE NOYAU : la loi du coût par événement, re-mesurée sur le binaire du jour.
etape_noyau() {
    timeout 900 "$D" models/Qwen2.5-0.5B-Q8_0.gguf --threads 20 \
        > "$C/noyau.log" 2>&1
    dire "noyau : $(grep -oE 'bande passante mémoire mesurée : [0-9.]+ Go/s' "$C/noyau.log" | head -1)"
    dire "noyau : $(grep -oE 'push/pull = ×[0-9.]+' "$C/noyau.log" | tail -1)"
}

# ----------------------------------------------------------------- étape 8
# RÉPARTITION : les deux portes, puis la carte de latence (à partir de quel
# aller-retour le réseau coûte plus que le calcul économisé).
etape_repartition() {
    timeout 1800 tools/porte-flux.sh > "$C/repartition_flux.log" 2>&1
    dire "répartition/flux : $(tail -1 "$C/repartition_flux.log")"
    if [ -f /tmp/m4_route.gguf ]; then
        MODELE=/tmp/m4_route.gguf IDS="$C/route_ids128.txt" LIMITE=128 \
            timeout 900 tools/porte-reparti-moteur.sh > "$C/repartition_modele.log" 2>&1
        dire "répartition/modèle : $(tail -1 "$C/repartition_modele.log")"
    fi
}

# ----------------------------------------------------------------- étape 9
# LES PORTES : rien n'est acquis si elles ne sont pas vertes.
etape_portes() {
    timeout 3600 tools/portes.sh > "$C/portes.log" 2>&1
    dire "portes : $(grep -cE "✅" "$C/portes.log") vertes · $(grep -cE "❌" "$C/portes.log") rouges"
}

# ---------------------------------------------------------------------- file
ETAPES=(grille parcimonie contexte lot routage semantique noyau repartition portes)
if [ "${1:-}" = "--liste" ]; then printf '%s\n' "${ETAPES[@]}"; exit 0; fi

if [ $# -gt 0 ]; then
    etape_$1
else
    dire "=== campagne démarrée (pid $$) ==="
    for e in "${ETAPES[@]}"; do
        dire "--- étape $e ---"
        etape_"$e"
    done
    dire "=== campagne terminée ==="
fi
