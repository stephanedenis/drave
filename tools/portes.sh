#!/bin/bash
# Les portes du dépôt, en une commande.
#
# Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien :
# chaque porte est comparée à la valeur ATTENDUE, et le script sort en erreur si
# l'une diverge. Les valeurs sont celles publiées dans les rapports.
#
#   tools/portes.sh            toutes les portes
#   tools/portes.sh rapide     sans gpt-oss (le seul qui prenne ~20 min)

set -u
cd "$(dirname "$0")/.."
D=./drave-core/target/release/drave
RAPIDE=${1:-}
ECHEC=0

[ -x "$D" ] || { echo "compiler d'abord : (cd drave-core && cargo build --release)"; exit 2; }

compare() {  # nom, attendu, obtenu
    if [ "$2" = "$3" ]; then
        printf "  %-42s %s  ✅\n" "$1" "$3"
    else
        printf "  %-42s %s  ❌ (attendu %s)\n" "$1" "${3:-—}" "$2"
        ECHEC=1
    fi
}

# Attention : le moteur affiche AUSSI une perplexité cumulée par fenêtre, avant
# le total. Prendre la première occurrence du motif donnait 17,431 (fenêtre 1) au
# lieu de 19,3885 (total) — un instrument faux qui accuse le code.
valeur() { grep -oE "=== perplexité [0-9]+\.[0-9]+" | grep -oE "[0-9]+\.[0-9]+" | head -1; }

echo "=== Portes ==="

# 1. Tests unitaires.
n=$( (cd drave-core && cargo test --release 2>&1) | grep -oE "[0-9]+ passed" | head -1 | cut -d' ' -f1)
[ "${n:-0}" -ge 35 ] && printf "  %-42s %s  ✅\n" "cargo test --release" "${n} verts" \
                     || { printf "  %-42s %s  ❌\n" "cargo test --release" "${n:-0} verts"; ECHEC=1; }

# 2. Perplexité Qwen2.5-0.5B, contexte 256.
v=$(timeout 600 $D models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt --ctx 256 \
    --abits 16 --threads 16 --limit 512 --dense 2>&1 | valeur)
compare "Qwen2.5-0.5B ctx 256" "19.3885" "$v"

# 3. Modèle en clusters, mêmes jetons que l'original.
A=/home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters-v2
if [ -d "$A" ]; then
    v=$(timeout 900 $D "$A" --ppl /tmp/ids_qwen.txt --ctx 64 --limit 8 --dense \
        --threads 8 --lot 1 2>&1 | valeur)
    compare "Qwen3-30B en clusters (origine : 799,8557)" "799.8557" "$v"
fi

# 4. Le plan matériel doit détecter les cœurs physiques, pas les threads.
v=$($D models/Qwen2.5-0.5B-Q8_0.gguf --materiel 2>/dev/null | grep -oE "^  threads +: [0-9]+" | grep -oE "[0-9]+")
att=$(nproc); att=$((att / 2))
[ "${v:-0}" -gt 0 ] && [ "${v:-0}" -le "$att" ] \
    && printf "  %-42s %s  ✅\n" "threads par défaut (physiques)" "$v" \
    || { printf "  %-42s %s  ❌\n" "threads par défaut" "${v:-—}"; ECHEC=1; }

# 5. gpt-oss : le seul long.
if [ "$RAPIDE" != "rapide" ]; then
    echo "  (gpt-oss : ~20 min, ignoré si non demandé)"
fi

echo ""
[ "$ECHEC" = 0 ] && echo "toutes les portes sont vertes" || echo "AU MOINS UNE PORTE A DIVERGÉ"
exit $ECHEC
