#!/usr/bin/env bash
# chaine_2048.sh — R1.2 poussé à 2 048 octets, puis la production à la même fenêtre.
#
#   1. wiki_fr, RoPE, seq 2 048 / fenêtre 2 048, 1 250 pas = 20,5 Mo (octets constants avec
#      R1.1 et R1.2) — depuis base-wiki-45m
#   2. + 11 250 pas depuis ce point = 12 500 pas (4× les octets)
#   3. mélange de production, seq 2 048, 3 750 pas = 61,4 Mo (octets constants avec N2.ac),
#      depuis mix-60k
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet || exit 1
export PYTHONPATH=. CUDA_VISIBLE_DEVICES=0
WIKI="--corpus data/wiki_fr/propre/train.txt --canal data/wiki_fr/propre/train.canal \
 --seq 2048 --window 2048 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512"

~/gpu-env/bin/python work/n2ac/entrainer_rope.py $WIKI --pas 1250 \
  --init work/n2j/base-wiki-45m.pt \
  --sortie work/n2ac/rope2048-1.25k.pt --drvm work/n2ac/rope2048-1.25k.drvm \
  > work/n2ac/rope2048-1.25k.log 2>&1
echo "rope2048-1.25k fini $(date '+%H:%M:%S')"

~/gpu-env/bin/python work/n2ac/entrainer_rope.py $WIKI --pas 11250 \
  --init work/n2ac/rope2048-1.25k.pt \
  --sortie work/n2ac/rope2048-12.5k.pt --drvm work/n2ac/rope2048-12.5k.drvm \
  > work/n2ac/rope2048-12.5k.log 2>&1
echo "rope2048-12.5k fini $(date '+%H:%M:%S')"

~/gpu-env/bin/python work/n2ac/entrainer_rope.py \
  --corpus data/wiki_mix/propre/train.txt --canal data/wiki_mix/propre/train.canal \
  --seq 2048 --window 2048 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512 \
  --init work/n2w/mix-60k.pt --pas 3750 \
  --sortie work/n2ac/mix2048-3.75k.pt --drvm work/n2ac/mix2048-3.75k.drvm \
  > work/n2ac/mix2048-3.75k.log 2>&1
echo "mix2048-3.75k fini $(date '+%H:%M:%S')"
