#!/bin/bash
# checkpoint_bench.sh — le banc complet d'un checkpoint : génération (128 o) puis grammaticalité.
#
#   bash bench/checkpoint_bench.sh work/n3/r1.pt [nom]
#
# Deux JSON : reports/banc-generation-<nom>.json et reports/banc-grammaticalite-<nom>.json.
# Le protocole est celui de la fiche du 34 M (20 prompts, 128 octets, 3 réglages, contrôle
# aléatoire n=128, graine 1234) : c'est ce qui rend le checkpoint comparable à la référence.
set -u
CK=${1:?checkpoint .pt}
NOM=${2:-$(basename "$CK" .pt)}
PY=${PY:-/home/stephane/gpu-env/bin/python}
GPU=${GPU:-0}
cd "$(dirname "$0")/.."
PYTHONPATH=. "$PY" tools/banc_generation.py --modele "$CK" --n 128 --device "cuda:$GPU" \
    --sortie "reports/banc-generation-$NOM.json" || exit 1
PYTHONPATH=. "$PY" tools/banc_grammaticalite.py \
    --entree "reports/banc-generation-$NOM.json" \
    --controle reports/banc-generation-aleatoire.json \
    --sortie "reports/banc-grammaticalite-$NOM.json" || exit 1
echo "bancs : reports/banc-generation-$NOM.json · reports/banc-grammaticalite-$NOM.json"
