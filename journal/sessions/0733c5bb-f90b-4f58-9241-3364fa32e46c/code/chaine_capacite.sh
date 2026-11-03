#!/usr/bin/env bash
# chaine_capacite.sh — la fenêtre paie-t-elle autant à 11,47 M et 21,65 M qu'à 34,3 M ?
#
# Deux bras RoPE, initialisation aléatoire identique (graine 1), octets constants (33 Mo) :
#   A. fenêtre 512, 8 000 pas × 8 × 512
#   B. fenêtre 128 (seq 128), 32 000 pas × 8 × 128
# Usage : chaine_capacite.sh <device> <dim> <expert_hidden> <tag>
set -u
DEV=${1:-0}; DIM=${2:-296}; EH=${3:-416}; TAG=${4:-2165m}
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet || exit 1
export PYTHONPATH=. CUDA_VISIBLE_DEVICES=$DEV
~/gpu-env/bin/python work/n2ac/entrainer_rope.py \
  --corpus data/wiki_fr/propre/train.txt --canal data/wiki_fr/propre/train.canal \
  --seq 512 --window 512 --lot 8 --lr 3e-4 --graine 1 --dim $DIM --expert-hidden $EH --pas 8000 \
  --sortie work/n2ac/cap-$TAG-512.pt --drvm work/n2ac/cap-$TAG-512.drvm \
  > work/n2ac/cap-$TAG-512.log 2>&1
echo "cap-$TAG-512 fini $(date '+%H:%M:%S')"
~/gpu-env/bin/python work/n2ac/entrainer_rope.py \
  --corpus data/wiki_fr/propre/train.txt --canal data/wiki_fr/propre/train.canal \
  --seq 128 --window 256 --lot 8 --lr 3e-4 --graine 1 --dim $DIM --expert-hidden $EH --pas 32000 \
  --sortie work/n2ac/cap-$TAG-128.pt --drvm work/n2ac/cap-$TAG-128.drvm \
  > work/n2ac/cap-$TAG-128.log 2>&1
echo "cap-$TAG-128 fini $(date '+%H:%M:%S')"
