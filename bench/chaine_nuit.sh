#!/bin/bash
# nuit.sh — la chaîne de la nuit : 10 000 pas, banc, grammaticalité, PPL wikitext2.
#   bash work/n4/nuit.sh <gpu> <corpus> <prefixe> <n_tranches>
set -u
GPU=$1; CORPUS=$2; PREFIX=$3; N=${4:-11}
PY=/home/stephane/gpu-env/bin/python
CK=""
for i in $(seq 1 "$N"); do
  INIT=""
  [ -n "$CK" ] && INIT="--init $CK"
  echo "=== tranche $i/$N $(date +%H:%M) ===" >> "work/n4/${PREFIX}.chaine.log"
  PYTHONPATH=. $PY -m tools.entrainer_native --corpus "$CORPUS" \
     --val data/wiki_mix/propre/val.txt --pas 10000 --seq 1024 --lot 8 --lr 1e-4 \
     --dim 896 --expert-hidden 896 --no-tetes --amp --device "cuda:$GPU" --graine 1 $INIT \
     --sortie "work/n4/${PREFIX}${i}.pt" --drvm "work/n4/${PREFIX}${i}.drvm" \
     >> "work/n4/${PREFIX}.chaine.log" 2>&1 || break
  CK="work/n4/${PREFIX}${i}.pt"
  PYTHONPATH=. $PY tools/banc_generation.py --modele "$CK" --n 128 --device "cuda:$GPU" \
     --sortie "reports/banc-generation-${PREFIX}${i}.json" >> "work/n4/${PREFIX}.chaine.log" 2>&1 || true
  PYTHONPATH=. $PY tools/banc_grammaticalite.py --entree "reports/banc-generation-${PREFIX}${i}.json" \
     --controle reports/banc-generation-aleatoire.json \
     --sortie "reports/banc-grammaticalite-${PREFIX}${i}.json" >> "work/n4/${PREFIX}.chaine.log" 2>&1 || true
  PYTHONPATH=. $PY tools/ppl_ckpt.py --modele "$CK" --val data/wikitext2_test.txt \
     --device "cuda:$GPU" --sortie "reports/ppl-wikitext2-${PREFIX}${i}.json" \
     >> "work/n4/${PREFIX}.chaine.log" 2>&1 || true
done
echo "=== chaîne $PREFIX finie $(date +%H:%M) ===" >> "work/n4/${PREFIX}.chaine.log"
