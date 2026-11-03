#!/usr/bin/env bash
# chaine_porte.sh — la porte < 2,5 sur le corpus propre, avec et sans fenêtre.
#
# Corpus : data/corpus_propre (train 3,24 Mo, val 180 Ko, 0 % de fuite — N2.h).
# Deux bras à OCTETS ÉGAUX (33 Mo vus), init base-wiki-45m, canal :
#   1. fenêtre 512, 8 000 pas × 8 × 512
#   2. fenêtre 256 (seq 128), 32 000 pas × 8 × 128
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet || exit 1
export PYTHONPATH=. CUDA_VISIBLE_DEVICES=${1:-1}
~/gpu-env/bin/python work/n2ac/entrainer_rope.py \
  --corpus data/corpus_propre/train.txt --canal data/corpus_propre/train.canal \
  --seq 512 --window 512 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512 \
  --init work/n2j/base-wiki-45m.pt --pas 8000 \
  --sortie work/n2ac/propre512-8k.pt --drvm work/n2ac/propre512-8k.drvm \
  > work/n2ac/propre512-8k.log 2>&1
echo "propre512-8k fini $(date '+%H:%M:%S')"
~/gpu-env/bin/python work/n2ac/entrainer_rope.py \
  --corpus data/corpus_propre/train.txt --canal data/corpus_propre/train.canal \
  --seq 128 --window 256 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512 \
  --init work/n2j/base-wiki-45m.pt --pas 32000 \
  --sortie work/n2ac/propre128-32k.pt --drvm work/n2ac/propre128-32k.drvm \
  > work/n2ac/propre128-32k.log 2>&1
echo "propre128-32k fini $(date '+%H:%M:%S')"
