#!/usr/bin/env bash
# chaine_1024.sh — R1.2 à 1 024 octets : deux budgets dans la MÊME trajectoire.
#
#   1. 2 500 pas × 8 × 1 024 = 20,5 Mo vus — les mêmes octets que R1.1 et R1.2-512
#   2. + 17 500 pas depuis ce point = 20 000 pas (4× les octets, comme R1.2-512)
#
# RoPE, fenêtre 1 024, init base-wiki-45m, canal. Le point 2 reprend le point 1 : un seul
# entraînement continu, deux points de contrôle, donc deux comparaisons contrôlées.
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet || exit 1
export PYTHONPATH=. CUDA_VISIBLE_DEVICES=0
COMMUN="--corpus data/wiki_fr/propre/train.txt --canal data/wiki_fr/propre/train.canal \
 --seq 1024 --window 1024 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512 \
 --init work/n2j/base-wiki-45m.pt"

~/gpu-env/bin/python work/n2ac/entrainer_rope.py $COMMUN --pas 2500 \
  --sortie work/n2ac/rope1024-2.5k.pt --drvm work/n2ac/rope1024-2.5k.drvm \
  > work/n2ac/rope1024-2.5k.log 2>&1
echo "rope1024-2.5k fini $(date '+%H:%M:%S')"

~/gpu-env/bin/python work/n2ac/entrainer_rope.py \
  --corpus data/wiki_fr/propre/train.txt --canal data/wiki_fr/propre/train.canal \
  --seq 1024 --window 1024 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512 \
  --init work/n2ac/rope1024-2.5k.pt --pas 17500 \
  --sortie work/n2ac/rope1024-20k.pt --drvm work/n2ac/rope1024-20k.drvm \
  > work/n2ac/rope1024-20k.log 2>&1
echo "rope1024-20k fini $(date '+%H:%M:%S')"
