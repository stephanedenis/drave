#!/usr/bin/env bash
# chaine_r1.sh — le reste du banc R1, sur le GPU que N2 ne prend pas (le 200 k est sur 0).
#
#   1. R1.1 graine 2 (contrôle de graine)            : 20 000 pas × 8 × 128, fenêtre 256
#   2. R1.2 budget constant (mêmes octets vus)       :  5 000 pas × 8 × 512, fenêtre 512
#   3. R1.2 (mêmes pas que R1.1)                     : 20 000 pas × 8 × 512, fenêtre 512
#
# Le point de départ, le corpus, le canal, le lr et la supervision sont identiques à N2.z.
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet || exit 1
export PYTHONPATH=. CUDA_VISIBLE_DEVICES=1

COMMUN="--corpus data/wiki_fr/propre/train.txt --canal data/wiki_fr/propre/train.canal \
 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512 \
 --init work/n2j/base-wiki-45m.pt"

~/gpu-env/bin/python work/n2ac/entrainer_rope.py $COMMUN \
  --pas 20000 --seq 128 --window 256 --graine 2 \
  --sortie work/n2ac/rope-20k-g2.pt --drvm work/n2ac/rope-20k-g2.drvm \
  > work/n2ac/rope-20k-g2.log 2>&1
echo "R11-g2 fini $(date '+%H:%M:%S')"

~/gpu-env/bin/python work/n2ac/entrainer_rope.py $COMMUN \
  --pas 5000 --seq 512 --window 512 \
  --sortie work/n2ac/rope512-5k.pt --drvm work/n2ac/rope512-5k.drvm \
  > work/n2ac/rope512-5k.log 2>&1
echo "R12-5k fini $(date '+%H:%M:%S')"

~/gpu-env/bin/python work/n2ac/entrainer_rope.py $COMMUN \
  --pas 20000 --seq 512 --window 512 \
  --sortie work/n2ac/rope512-20k.pt --drvm work/n2ac/rope512-20k.drvm \
  > work/n2ac/rope512-20k.log 2>&1
echo "R12-20k fini $(date '+%H:%M:%S')"
