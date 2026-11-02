#!/usr/bin/env bash
# chaine_zero.sh — le contrôle « depuis zéro » de R1.1 : même initialisation figée, deux schémas.
#
#   A. absolu : positions apprises 0…511, décalage aléatoire dans [0, 384] (recette N2.z)
#   B. RoPE   : mêmes blocs, q/k tournés, aucune position apprise
# Mêmes 20 000 pas × 8 × 128, même corpus, même canal, même lr. Seul le schéma change.
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet || exit 1
export PYTHONPATH=. CUDA_VISIBLE_DEVICES=1
COMMUN="--corpus data/wiki_fr/propre/train.txt --canal data/wiki_fr/propre/train.canal \
 --pas 20000 --seq 128 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512 \
 --init work/n2ac/init-figee.pt"

~/gpu-env/bin/python tools/entrainer_native.py $COMMUN --positions-aleatoires 384 \
  --sortie work/n2ac/zero-absolu.pt --drvm work/n2ac/zero-absolu.drvm \
  > work/n2ac/zero-absolu.log 2>&1
echo "zero-absolu fini $(date '+%H:%M:%S')"

~/gpu-env/bin/python work/n2ac/entrainer_rope.py $COMMUN --window 256 \
  --sortie work/n2ac/zero-rope.pt --drvm work/n2ac/zero-rope.drvm \
  > work/n2ac/zero-rope.log 2>&1
echo "zero-rope fini $(date '+%H:%M:%S')"
