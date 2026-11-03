#!/usr/bin/env bash
# chaine_prod_zero.sh — la production SANS N2.ac : même recette (RoPE, seq 512) et mêmes octets
# ajoutés (61,4 Mo = 15 000 pas × 8 × 512 que le fine-tune de production), mais départ depuis
# une initialisation aléatoire figée. Isole ce que l'affinage doit à N2.ac.
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet || exit 1
export PYTHONPATH=. CUDA_VISIBLE_DEVICES=${1:-1}
~/gpu-env/bin/python work/n2ac/entrainer_rope.py \
  --corpus data/wiki_mix/propre/train.txt --canal data/wiki_mix/propre/train.canal \
  --seq 512 --window 512 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512 \
  --init work/n2ac/init-figee.pt --pas 15000 \
  --sortie work/n2ac/mix512-zero-15k.pt --drvm work/n2ac/mix512-zero-15k.drvm \
  > work/n2ac/mix512-zero-15k.log 2>&1
echo "mix512-zero-15k fini $(date '+%H:%M:%S')"
