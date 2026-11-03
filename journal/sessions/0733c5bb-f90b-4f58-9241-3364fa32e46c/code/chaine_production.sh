#!/usr/bin/env bash
# chaine_production.sh — la fenêtre sur le MODÈLE DE PRODUCTION (mélange 1 Go).
#
# On part de `work/n2w/mix-60k.pt` (N2.ac : 60 000 pas à seq 128, 3,4902 en domaine) et on
# l'affine avec RoPE sur des séquences longues, à **octets constants** (61,4 Mo = 60 000 × 8 × 128) :
#
#   1. seq 512  → 15 000 pas (61,4 Mo)
#   2. seq 1 024 → 7 500 pas (61,4 Mo), depuis le même point de départ (pas depuis le 1)
#
# Deux recettes comparables à N2.ac à octets égaux ; l'évaluation se fait à 128 / 512 / 1 000.
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet || exit 1
export PYTHONPATH=. CUDA_VISIBLE_DEVICES=1
COMMUN="--corpus data/wiki_mix/propre/train.txt --canal data/wiki_mix/propre/train.canal \
 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512 --init work/n2w/mix-60k.pt"

~/gpu-env/bin/python work/n2ac/entrainer_rope.py $COMMUN --seq 512 --window 512 --pas 15000 \
  --sortie work/n2ac/mix512-15k.pt --drvm work/n2ac/mix512-15k.drvm \
  > work/n2ac/mix512-15k.log 2>&1
echo "mix512-15k fini $(date '+%H:%M:%S')"

~/gpu-env/bin/python work/n2ac/entrainer_rope.py $COMMUN --seq 1024 --window 1024 --pas 7500 \
  --sortie work/n2ac/mix1024-7.5k.pt --drvm work/n2ac/mix1024-7.5k.drvm \
  > work/n2ac/mix1024-7.5k.log 2>&1
echo "mix1024-7.5k fini $(date '+%H:%M:%S')"
