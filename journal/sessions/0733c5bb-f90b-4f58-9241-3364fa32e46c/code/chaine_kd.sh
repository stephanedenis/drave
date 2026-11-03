#!/usr/bin/env bash
# chaine_kd.sh — distillation native : le professeur long (1 024) dans un élève 11,47 M à 512.
# Deux alphas, même init aléatoire (graine 1), mêmes 8 000 pas et mêmes octets que le bras « dur »
# de référence (cap-1147m-512).
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet || exit 1
export PYTHONPATH=. CUDA_VISIBLE_DEVICES=${1:-1}
for A in 0.5 0.9; do
  ~/gpu-env/bin/python work/n2ac/distiller_natif.py \
    --professeur work/n2ac/rope1024-20k.pt \
    --corpus data/wiki_fr/propre/train.txt --canal data/wiki_fr/propre/train.canal \
    --seq 512 --window 512 --lot 8 --lr 3e-4 --graine 1 --dim 224 --expert-hidden 288 \
    --pas 8000 --alpha $A --T 2 \
    --sortie work/n2ac/kd-1147m-512-a$A.pt --drvm work/n2ac/kd-1147m-512-a$A.drvm \
    > work/n2ac/kd-1147m-512-a$A.log 2>&1
  echo "kd a=$A fini $(date '+%H:%M:%S')"
done
