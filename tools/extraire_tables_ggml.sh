#!/usr/bin/env bash
# Extrait les tables de ggml (grilles IQ) au format Rust, ou VÉRIFIE que celles
# embarquées dans drave-core/src/formats.rs sont bien celles de ggml.
#
#   tools/extraire_tables_ggml.sh            imprime le code Rust des tables
#   tools/extraire_tables_ggml.sh verifier   compare avec formats.rs (code 1 si écart)
#
# Pourquoi : ces tables font 4 à 16 Ko de constantes. Les recopier à la main est
# une faute qui ne se voit pas — une grille fausse d'une seule entrée donne des
# poids faux sur un seul motif de bits, donc une perplexité un peu haute et rien
# d'autre. La seule garantie utile est de pouvoir REDIRE d'où vient chaque
# valeur, et de comparer automatiquement.
set -eu
cd "$(dirname "$0")/.."
LLAMA=${DRAVE_LLAMA:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}
EXE=${TMPDIR:-/tmp}/extraire_tables_ggml

gcc -O2 -I"$LLAMA/ggml/include" -I"$LLAMA/ggml/src" tools/extraire_tables_ggml.c \
    -o "$EXE" -L"$LLAMA/build/bin" -lggml -lggml-base -Wl,-rpath,"$LLAMA/build/bin"

if [ "${1:-}" != "verifier" ]; then
  "$EXE"
  exit 0
fi

"$EXE" > "$EXE.rs"
python3 - "$EXE.rs" drave-core/src/formats.rs <<'PY'
import re, sys

def table(texte, nom):
    """Renvoie la liste des entiers de la table `nom` (tous formats confondus)."""
    m = re.search(rf"pub static {nom}\s*:[^=]*=\s*\[(.*?)\n\];", texte, re.S)
    if not m:
        return None
    return [int(x) for x in re.findall(r"-?\d+", m.group(1))]

genere = open(sys.argv[1]).read()
embarque = open(sys.argv[2]).read()
noms = ["IQ2XXS_GRID", "KSIGNS_IQ2XS", "IQ1S_GRID", "IQ3XXS_GRID", "KVALS_IQ4NL"]
echec = 0
for nom in noms:
    a, b = table(genere, nom), table(embarque, nom)
    if b is None:
        print(f"  {nom:14s} MANQUANTE dans {sys.argv[2]}")
        echec = 1
        continue
    if a == b:
        print(f"  {nom:14s} identique ({len(a)} valeurs)")
    else:
        ecarts = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
        print(f"  {nom:14s} DIVERGE : {len(ecarts)} valeur(s) sur {len(a)} — "
              f"premier écart {ecarts[0] if ecarts else '—'}")
        echec = 1
sys.exit(echec)
PY
