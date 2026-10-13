#!/bin/bash
# loi-fenetre-textes.sh — le prix d'une fenêtre d'attention, MOYENNÉ sur plusieurs textes.
#
# POURQUOI CET OUTIL. La mesure du 13/10 (`reports/rapport-loi-frontiere-fenetre.md`) a montré que
# le prix d'une fenêtre dépend **beaucoup** du texte : à N = 2 048 et fenêtre N/2, il va de +0,5 % à
# +2,1 % sur sept textes (robuste), mais à fenêtre N/4 il va de +2,8 % à **+49,2 %** (facteur 17,6).
# Une mesure sur un seul texte ne dit donc rien — et l'outil `carte-fenetre-puits.sh` n'en prend
# qu'un. Celui-ci prend **le même N sur plusieurs fenêtres du corpus** et publie la moyenne, le
# minimum, le maximum et l'étendue : c'est ce qu'il faut pour dire « la moitié des clés est le
# régime sûr » avec une barre d'erreur, au lieu de le dire sur un texte.
#
# Usage : tools/loi-fenetre-textes.sh <N> [fenêtres…]
#   ex.  tools/loi-fenetre-textes.sh 4096 2048 1024      # N = 4096, fenêtres N/2 et N/4
# Variables : TEXTES (décalages du corpus, défaut « 0 10000 20000 30000 »), IDS (corpus tokenisé)
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
PRE=${PRE:-$HOME/IA/scratch/prerequis}
IDS=${IDS:-$PRE/ids_0.5B_wt2_8192.txt}
TEXTES=${TEXTES:-"0 10000 20000 30000"}
N=${1:?usage : loi-fenetre-textes.sh <N> [fenêtres…]}; shift
FENETRES=${*:-$((N/2)) $((N/4))}

[ -s "$M" ] || { echo "  ❌ modèle absent : $M"; exit 2; }
if [ ! -s "$IDS" ]; then
    echo "  (corpus tokenisé absent — régénéré depuis data/wikitext2_test.txt)"
    "$D" "$M" --tokenize --fichier data/wikitext2_test.txt --sortie "$IDS" >/dev/null 2>&1
fi
[ -s "$IDS" ] || { echo "  ❌ corpus $IDS absent et non régénérable"; exit 2; }

# les découpages : un fichier d'identifiants par décalage (le même N jetons à chaque fois)
for off in $TEXTES; do
    f="$PRE/ids_0.5B_wt2_off$off.txt"
    [ -s "$f" ] || python3 - "$IDS" "$f" "$off" "$N" <<'PY'
import sys, pathlib
ids = pathlib.Path(sys.argv[1]).read_text().strip().split(",")
off, n = int(sys.argv[3]), int(sys.argv[4])
pathlib.Path(sys.argv[2]).write_text(",".join(ids[off:off + n]) + "\n")
PY
done

echo "N = $N · fenêtres $FENETRES · textes (décalages) : $TEXTES"
T=$(mktemp -d)
lignes=""
for off in $TEXTES; do
    f=$([ "$off" = 0 ] && echo "$IDS" || echo "$PRE/ids_0.5B_wt2_off$off.txt")
    ref=$("$D" "$M" --ppl "$f" --ctx "$N" --limit "$N" --threads 8 2>&1 \
          | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+")
    [ -n "$ref" ] || { echo "  ❌ référence illisible pour le décalage $off"; exit 1; }
    ligne="$off $ref"
    for fen in $FENETRES; do
        # `--attn-sinks 0` N'EST PAS « pas de puits » — mesuré le 13/10 à N=4096, fenêtre 2048 :
        # 55,9647 avec, 12,3112 sans (référence 12,2177). Le zéro est un piège : il active le
        # mécanisme avec zéro puits et casse l'attention. On OMET donc le drapeau.
        v=$("$D" "$M" --ppl "$f" --ctx "$N" --limit "$N" --threads 8 \
            --attn-window "$fen" 2>&1 \
            | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+")
        ligne="$ligne ${v:-NA}"
    done
    lignes="$lignes$ligne\n"
    echo "  décalage $off : $ligne"
done
python3 - "$N" "$FENETRES" <<PY
import statistics as st
lignes = "$lignes".strip().split("\\n")
fen = "$FENETRES".split()
lignes = [l.split() for l in lignes if l.strip()]
print()
print("| décalage | référence | " + " | ".join(f"fenêtre {f}" for f in fen) + " |")
print("|---:|---:|" + "---:|" * len(fen))
for l in lignes:
    off, ref = l[0], float(l[1])
    print(f"| {off} | {ref:.4f} | " + " | ".join(
        f"**+{100*(float(v)/ref - 1):.1f} %**" for v in l[2:]) + " |")
print()
for i, f in enumerate(fen):
    prix = [100 * (float(l[2 + i]) / float(l[1]) - 1) for l in lignes]
    print(f"  fenêtre {f} ({100*int(f)//$N} % de N) : moyenne **+{st.mean(prix):.1f} %** · "
          f"de +{min(prix):.1f} % à +{max(prix):.1f} % · étendue **{max(prix)-min(prix):.1f} points** "
          f"sur {len(prix)} textes")
PY
rm -rf "$T"
