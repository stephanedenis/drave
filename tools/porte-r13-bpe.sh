#!/bin/bash
# porte-r13-bpe.sh — R13.1 : un petit modèle natif BPE bat-il le modèle octets
# à budget d'OCTETS égal ?
#
# Deux modèles de même architecture (224, 6 blocs), même graine, même corpus
# français : le baseline est en octets (400 pas), le BPE en 512 jetons (200 pas)
# — 200 pas BPE voient ~405 k octets, 400 pas octets en voient ~410 k. On compare
# les BITS PAR OCTET, pas la PPL par jeton : le BPE a 1,98 octet/jeton.
set -u
cd "$(dirname "$0")/.."
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-r13-bpe-XXXXXX")
trap 'rm -rf "$T"' EXIT
[ -x "$PY" ] || { echo "  ❌ $PY absent"; exit 2; }
"$PY" -c "import torch, tokenizers" 2>/dev/null || { echo "  ❌ torch/tokenizers absents"; exit 2; }

echo "=== 1. tokenizer BPE 512 et corpus d'identifiants ==="
PYTHONPATH=. "$PY" tools/tokenizer_bpe.py --corpus data/corpus_fr.txt --vocab 512 \
  --sortie-tokenizer "$T/tok.json" --sortie-ids "$T/bpe_ids.pt" \
  --sortie-octets "$T/octets.pt" --stats "$T/stats.json" > "$T/tok.log" 2>&1 \
  || { echo "  ❌ tokenizer"; tail -3 "$T/tok.log"; exit 2; }
OCTETS=$("$PY" -c "import json;d=json.load(open('$T/stats.json'));print(d['octets'])")
REV=$("$PY" -c "import json;print(json.load(open('$T/stats.json'))['reversible'])")
[ "$REV" = "True" ] || { echo "  ❌ tokenizer non réversible"; exit 1; }
echo "  ✅ réversible · $OCTETS octets"

echo "=== 2. modèle octets : 400 pas ==="
PYTHONPATH=. CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-0} "$PY" -m tools.entrainer_native_tokens \
  --ids "$T/octets.pt" --vocab 256 --octets "$OCTETS" --pas 400 --seq 128 --lot 8 \
  --device cuda --graine 1 --sortie "$T/bytes.pt" --drvm "$T/bytes.drvm" > "$T/bytes.log" 2>&1 \
  || { echo "  ❌ entraînement octets"; tail -3 "$T/bytes.log"; exit 2; }
echo "  ✅ octets"

echo "=== 3. modèle BPE : 200 pas (~mêmes octets vus) ==="
PYTHONPATH=. CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-0} "$PY" -m tools.entrainer_native_tokens \
  --ids "$T/bpe_ids.pt" --vocab 512 --octets "$OCTETS" --pas 200 --seq 128 --lot 8 \
  --device cuda --graine 1 --sortie "$T/bpe.pt" --drvm "$T/bpe.drvm" > "$T/bpe.log" 2>&1 \
  || { echo "  ❌ entraînement BPE"; tail -3 "$T/bpe.log"; exit 2; }
echo "  ✅ BPE"

echo "=== 4. comparaison bits/octet ==="
"$PY" - "$T/bytes.pt.json" "$T/bpe.pt.json" "$T/stats.json" <<'PY' || exit 1
import json, sys
b = json.load(open(sys.argv[1])); p = json.load(open(sys.argv[2])); s = json.load(open(sys.argv[3]))
octets_b = 400 * 8 * 128
octets_p = 200 * 8 * 128 * s["octets_par_jeton"]
print(f"  octets vus : octets {octets_b} · BPE {octets_p:.0f} ({100*(octets_p-octets_b)/octets_b:+.1f} %)")
if abs(octets_p - octets_b) / octets_b > 0.03:
    sys.exit("  ❌ budgets d'octets non comparables")
if p["bits_par_octet"] >= b["bits_par_octet"]:
    sys.exit(f"  ❌ BPE {p['bits_par_octet']:.3f} ≥ octets {b['bits_par_octet']:.3f}")
gain = 100 * (b["bits_par_octet"] - p["bits_par_octet"]) / b["bits_par_octet"]
print(f"  ✅ BPE {p['bits_par_octet']:.3f} bits/octet · octets {b['bits_par_octet']:.3f} · gain {gain:.1f} %")
print(f"  PPL/jeton : octets {b['ppl_val']:.2f} · BPE {p['ppl_val']:.2f} · vocab {p['vocab']}")
PY
echo "PORTE TENUE : BPE natif réversible · budgets d'octets égaux · bits/octet meilleurs"
