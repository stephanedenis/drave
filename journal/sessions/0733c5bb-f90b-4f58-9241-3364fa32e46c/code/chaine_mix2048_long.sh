#!/usr/bin/env bash
# chaine_mix2048_long.sh — la production à 2 048 avec 15 000 pas (suite de mix2048-3.75k).
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet || exit 1
export PYTHONPATH=. CUDA_VISIBLE_DEVICES=${1:-0}
~/gpu-env/bin/python work/n2ac/entrainer_rope.py \
  --corpus data/wiki_mix/propre/train.txt --canal data/wiki_mix/propre/train.canal \
  --seq 2048 --window 2048 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512 \
  --init work/n2ac/mix2048-3.75k.pt --pas 11250 \
  --sortie work/n2ac/mix2048-15k.pt --drvm work/n2ac/mix2048-15k.drvm \
  > work/n2ac/mix2048-15k.log 2>&1
echo "mix2048-15k fini $(date '+%H:%M:%S')"
