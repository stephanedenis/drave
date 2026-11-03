#!/usr/bin/env bash
# chaine_2048_wiki.sh — R1.2 à 2 048 octets (wiki_fr), octets constants puis pas constants.
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet || exit 1
export PYTHONPATH=. CUDA_VISIBLE_DEVICES=${1:-1}
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
