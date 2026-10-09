#!/bin/bash
# mesure_lot_disque.sh — le préremplissage par LOTS, mesuré sur le DISQUE.
#
# POURQUOI CE SCRIPT EXISTE. Le batch 5 avait comparé `--lot 1` à `--lot 4..64`
# sur le 30B : la première passe avait lu 10,9 Go et les suivantes ZÉRO octet. Le
# protocole mesurait donc le cache de pages, pas le lot (§ 14 du rapport). Ce qui
# manquait n'était pas le modèle : c'était **l'éviction**. On l'obtient sans être
# root avec `posix_fadvise(POSIX_FADV_DONTNEED)` sur le fichier du modèle, qui
# jette ses pages du cache — donc chaque réglage de lot repart à froid.
#
# CE QUI EST MESURÉ, PAR RÉGLAGE : les octets réellement lus (`File system
# inputs`), le temps mur, le débit et la perplexité. Le lot doit diviser les
# LECTURES ; s'il ne les divise pas, la mesure le dira.
#
# Usage :
#   mesure_lot_disque.sh <modele.gguf> <ids> [--lots "1 2 4 8 16"] [--limit 192]
#                        [--ctx 512] [--threads 20] [--journal F]
set -u
D=${D:-./drave-core/target/release/drave}
MODELE=""; IDS=""; LOTS="1 2 4 8 16"; LIMIT=192; CTX=512; THREADS=20; JOURNAL=""
while [ $# -gt 0 ]; do
    case "$1" in
        --lots) LOTS="$2"; shift 2 ;;
        --limit) LIMIT="$2"; shift 2 ;;
        --ctx) CTX="$2"; shift 2 ;;
        --threads) THREADS="$2"; shift 2 ;;
        --journal) JOURNAL="$2"; shift 2 ;;
        *) if [ -z "$MODELE" ]; then MODELE="$1"; else IDS="$1"; fi; shift ;;
    esac
done
[ -f "$MODELE" ] && [ -s "$IDS" ] || { echo "usage : mesure_lot_disque.sh <modele.gguf> <ids> [...]"; exit 2; }

dire() { echo "$*"; [ -n "$JOURNAL" ] && echo "[$(date '+%d/%m %H:%M:%S')] charge $(cut -d' ' -f1 /proc/loadavg) · $*" >> "$JOURNAL"; }

evincer() {  # jette les pages du modèle hors du cache, SANS root
    /home/stephane/gpu-env/bin/python - "$MODELE" <<'PY'
import os, sys
f = os.open(sys.argv[1], os.O_RDONLY)
taille = os.fstat(f).st_size
os.posix_fadvise(f, 0, taille, os.POSIX_FADV_DONTNEED)
os.close(f)
print(f"  (cache du modèle évincé : {taille/2**30:.1f} Go)")
PY
}

dire "# préremplissage par lots sur DISQUE · $(basename "$MODELE") · $LIMIT jetons, ctx $CTX"
dire "| lot | PPL | lus (Mio) | mur (s) | tok/s |"
dire "|---:|---:|---:|---:|---:|"
for lot in $LOTS; do
    evincer
    /usr/bin/time -v timeout 3600 $D "$MODELE" --ppl "$IDS" --limit "$LIMIT" --ctx "$CTX" \
        --threads "$THREADS" --lot "$lot" > /tmp/lot_disque.log 2> /tmp/lot_disque_temps.log
    ppl=$(grep -oE "perplexité [0-9.]+ sur" /tmp/lot_disque.log | grep -oE "[0-9.]+" | tail -1)
    ts=$(grep -oE "[0-9.]+ tok/s effectifs" /tmp/lot_disque.log | grep -oE "^[0-9.]+" | tail -1)
    lus=$(grep -oE "File system inputs: [0-9]+" /tmp/lot_disque_temps.log | grep -oE "[0-9]+$")
    mur=$(grep -oE "Elapsed \(wall clock\) time.*" /tmp/lot_disque_temps.log | grep -oE "[0-9:.]+$")
    dire "| $lot | ${ppl:-?} | $(( ${lus:-0} / 2048 )) | ${mur:-?} | ${ts:-?} |"
done
dire "# fin"
