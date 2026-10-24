#!/bin/bash
# Porte du DIFF PAR COUCHE : deux exécutions, et le diff NOMME la couche et le jeton.
#
# Pourquoi elle existe : après un changement de quantification ou de noyau, on
# sait dire « la perplexité a bougé de 0,01 » — pas OÙ. `tools/diff_flux.py`
# répond à la question ; cette porte vérifie trois choses, à chaque passage, sur
# le 0,5 B :
#   1. la REPRODUCTIBILITÉ : deux exécutions identiques (même prompt, temp 0) ont
#      un flux identique, neurone par neurone — un non-déterminisme caché échoue
#      ici, avant d'être pris pour une régression ;
#   2. la LOCALISATION : avec le KV en 8 bits, la divergence est NOMMÉE (couche,
#      jeton, nombre de neurones) ;
#   3. le CONTRAT : elle commence à la couche 1, au premier jeton TRACÉ (le 1 :
#      les positions de la trace sont 1-basées) — le KV du premier jeton est
#      quantifié le premier ; une autre origine est un défaut de noyau, pas un
#      effet de la quantification.
#
#   tools/porte-diff-couche.sh        la porte (~30 s)
#
# Notes :
#  · le KV par défaut est f32 (32 bits) sur cette machine ; `DRAVE_KV_BITS=8`
#    force l'int8 — c'est la variation qui exerce la quantification ;
#  · les couches tracées sont peu nombreuses (0 à 7) : le journal reste petit et
#    la première divergence, si elle existe, est dans la fenêtre.

set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
MODELE=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
PROMPT=${PROMPT:-"Le ciel est bleu parce que la lumière du soleil est diffusée par l'air."}
COUCHES=${COUCHES:-0,1,2,3,4,5,6,7}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-diff-XXXXXX")

[ -x "$D" ] || { echo "  $D absent : construire d'abord (cargo build --release)"; exit 1; }
[ -f "$MODELE" ] || { echo "  modèle $MODELE absent"; exit 1; }

lance() {  # $1 = trace ; l'environnement de l'appelant est transmis (DRAVE_KV_BITS…)
  "$D" "$MODELE" --infer --prompt "$PROMPT" --n 8 --ctx 64 --threads 8 --temp 0 \
        --trace-couches "$COUCHES" --trace-flux "$1" >"$T/$(basename "$1").log" 2>&1 \
    || { echo "  ❌ l'exécution pour $(basename "$1") a échoué"; tail -3 "$T/$(basename "$1").log"; exit 1; }
  [ -s "$1" ] || { echo "  ❌ trace vide : $(basename "$1")"; exit 1; }
}

echo "porte du diff par couche · $MODELE · couches $COUCHES"
lance "$T/a.drvf"
lance "$T/b.drvf"

# 1. la reproductibilité : deux exécutions identiques, même flux
out=$(python3 tools/diff_flux.py "$T/a.drvf" "$T/b.drvf" 2>&1)
if echo "$out" | grep -q "IDENTIQUES"; then
  echo "  ✅ deux exécutions identiques → flux identique, neurone par neurone"
else
  echo "  ❌ non-déterminisme : deux exécutions identiques divergent"
  echo "$out" | head -3
  exit 1
fi

# 2 et 3. la localisation et le contrat : KV int8 contre le défaut f32
DRAVE_KV_BITS=8 lance "$T/c.drvf"
out=$(python3 tools/diff_flux.py "$T/a.drvf" "$T/c.drvf" 2>&1)
prem=$(echo "$out" | grep "première divergence" | head -1)
if [ -z "$prem" ]; then
  echo "  ❌ aucune divergence avec le KV en 8 bits : la quantification n'est pas exercée"
  echo "$out" | head -2
  exit 1
fi
echo "  ✅ divergence localisée : ${prem#première divergence : }"
if echo "$prem" | grep -q "couche 1 · jeton 1"; then
  echo "  ✅ le contrat est tenu : la divergence commence à la couche 1, premier jeton tracé"
else
  echo "  ❌ le contrat est rompu : attendu couche 1 · jeton 1 — lu : ${prem#première divergence : }"
  exit 1
fi
echo "  → le diff nomme la couche et le jeton : une régression se lit, elle ne se devine pas (A4.3)"
