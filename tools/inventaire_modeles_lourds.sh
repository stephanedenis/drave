#!/bin/bash
# Inventorie les modèles lourds téléchargés et CONFRONTE les poids annoncés par
# les descripteurs GGUF aux tailles annoncées par HuggingFace.
#
# C'est la vérification croisée la plus large dont on dispose : si la table des
# types ggml était fausse d'un seul type, l'écart apparaîtrait sur des centaines
# de gigaoctets. Elle ne lit que les en-têtes (le plus gros fichier fait 366 Go).
#
#   tools/inventaire_modeles_lourds.sh [dossier]

set -u
cd "$(dirname "$0")/.."
D=${1:-/home/stephane/Data13TB/stephane/modeles/gguf}
BIN=./drave-core/target/release/drave

[ -x "$BIN" ] || { echo "compiler d'abord : cargo build --release"; exit 2; }

printf "%-28s %-12s %5s %8s %12s\n" "modèle" "architecture" "fich." "tenseurs" "poids lus"
printf -- "------------------------------------------------------------------------\n"
for d in "$D"/*/; do
    n=$(basename "$d")
    f=$(ls "$d"*.gguf 2>/dev/null | head -1)
    [ -z "$f" ] && continue
    # Un shard sur trois suffit : le lecteur va chercher les autres.
    ligne=$(timeout 600 "$BIN" "$f" --tensors 2>/dev/null | grep -E "·.*tenseurs" | head -1)
    [ -z "$ligne" ] && { printf "%-28s (illisible)\n" "$n"; continue; }
    arch=$(echo "$ligne" | cut -d' ' -f1)
    nf=$(echo "$ligne" | grep -oE "[0-9]+ fichiers" | cut -d' ' -f1)
    nt=$(echo "$ligne" | grep -oE "[0-9]+ tenseurs" | cut -d' ' -f1)
    go=$(echo "$ligne" | grep -oE "[0-9.]+ Go de poids" | cut -d' ' -f1)
    printf "%-28s %-12s %5s %8s %10s Go\n" "$n" "$arch" "$nf" "$nt" "$go"
done

echo ""
echo "Tailles annoncées par HuggingFace (tools/manifeste_modeles_lourds.json) :"
python3 - <<'PY'
import json, collections
m = json.load(open('tools/manifeste_modeles_lourds.json'))
par = collections.defaultdict(float)
for f in m:
    if f.get('octets'):
        par[f['nom']] += f['octets'] / 1e9
total = 0.0
for k in sorted(par):
    print(f"  {k:28s} {par[k]:8.1f} Go")
    total += par[k]
print(f"  {'TOTAL':28s} {total:8.1f} Go")
PY
