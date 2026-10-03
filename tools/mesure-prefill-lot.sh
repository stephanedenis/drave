#!/usr/bin/env bash
# mesure-prefill-lot.sh — ce que le REGROUPEMENT PAR EXPERT fait gagner au
# préremplissage, mesuré, pas supposé.
#
# En préremplissage par lots (`--lot N`, `forward_lot`), les jetons du lot qui
# ont choisi le même expert partagent UNE lecture de sa matrice : un seul
# `gemm_dense_q4` par expert non vide. Jeton par jeton, la même matrice est
# relue autant de fois qu'elle a d'ayants droit.
#
# Le script donne, pour chaque taille de lot :
#   - prompt_s  : le temps de préremplissage rendu par le moteur lui-même ;
#   - tok/s     : le débit qui en découle ;
#   - CPU %     : le taux d'occupation RÉEL (un lot qui parallélise mal se voit
#                 ici avant de se voir dans le temps) ;
#   - mur s     : le temps total du processus, chargement compris — il dit si
#                 le chiffre mesure le calcul ou la lecture du fichier.
#
# Règle : rien d'autre ne tourne pendant la mesure. Deux pools de 16 fils sur
# 40 CPU se disputent les cœurs ET la bande mémoire, et le chiffre obtenu ne
# mesure plus la taille du lot (constaté : ×17 sur un lot 2 mesuré pendant
# qu'un autre `drave` tournait encore).
#
# Usage : tools/mesure-prefill-lot.sh <modele.gguf> <ids-file> [lots…]
set -u
M="$1"; IDS="$2"; shift 2
LOTS=("$@"); [ ${#LOTS[@]} -eq 0 ] && LOTS=(1 2 4 8 16 32 64)
BIN="$(dirname "$0")/../drave-core/target/release/drave"
N=$(tr -cd ',' < "$IDS" | wc -c); N=$((N + 1))
REPS=${REPS:-2}
echo "# modèle  : $M"
echo "# invite  : $IDS ($N jetons) · threads 16 · ctx 512 · n 2 · $REPS passes"
echo "# support : $(df --output=source "$M" | tail -1)"
echo
printf '%-8s %10s %9s %8s %9s\n' lot prompt_s tok/s "CPU_%" "mur_s"
for L in "${LOTS[@]}"; do
    for r in $(seq "$REPS"); do
        out=$(/usr/bin/time -f "TIME %e %P" "$BIN" "$M" --infer --ids-file "$IDS" \
                        --n 2 --ctx 512 --lot "$L" --threads 16 2>&1)
        ps=$(echo "$out" | sed -n 's/^prompt  :.*en \([0-9.]*\) s.*/\1/p')
        ts=$(echo "$out" | sed -n 's/^prompt  :.*(\([0-9.]*\) tok\/s.*/\1/p')
        mur=$(echo "$out" | sed -n 's/^TIME \([0-9.]*\) .*/\1/p')
        cpu=$(echo "$out" | sed -n 's/^TIME [0-9.]* \([0-9]*\)%.*/\1/p')
        printf '%-8s %10s %9s %8s %9s\n' "$L.$r" "${ps:--}" "${ts:--}" "${cpu:--}" "${mur:--}"
    done
done
