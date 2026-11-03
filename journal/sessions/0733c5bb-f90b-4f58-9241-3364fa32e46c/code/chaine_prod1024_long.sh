#!/usr/bin/env bash
# chaine_prod1024_long.sh — le compute AVEC la fenêtre : la production à 1 024, 30 000 pas.
#
# Part de mix1024-7.5k (déjà 7 500 pas à 1 024) et ajoute 22 500 pas → 368 Mo vus au total.
# C'est le test « la fenêtre rend-elle la porte 2,5 moins chère ? » sur le mélange de production.
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet || exit 1
export PYTHONPATH=. CUDA_VISIBLE_DEVICES=${1:-0}
~/gpu-env/bin/python work/n2ac/entrainer_rope.py \
  --corpus data/wiki_mix/propre/train.txt --canal data/wiki_mix/propre/train.canal \
  --seq 1024 --window 1024 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512 \
  --init work/n2ac/mix1024-7.5k.pt --pas 22500 \
  --sortie work/n2ac/mix1024-30k.pt --drvm work/n2ac/mix1024-30k.drvm \
  > work/n2ac/mix1024-30k.log 2>&1
echo "mix1024-30k fini $(date '+%H:%M:%S')"
