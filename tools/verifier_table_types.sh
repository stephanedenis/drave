#!/bin/bash
# Confronte la table des tailles de types ggml du moteur à celle de `libggml`.
#
# Pourquoi cet outil existe : `octets_tensor` doit connaître, pour chaque type,
# le nombre de poids par bloc et la taille d'un bloc. Cette table est **relevée**
# depuis ggml et non devinée — mais rien n'empêche ggml d'ajouter un type demain,
# et un type absent est compté zéro octet. C'est exactement ainsi qu'un inventaire
# a annoncé 8,56 Go pour 86,9 Go de fichiers (les experts en `iq1_m`).
#
# Le moteur signale désormais un type inconnu ; cet outil dit lesquels manquent,
# en lisant la vérité dans la bibliothèque elle-même.
#
#   tools/verifier_table_types.sh [chemin de llama.cpp]
#
# Rend 0 si les tables concordent sur tous les types testés, 1 sinon.

set -u
cd "$(dirname "$0")/.."
RACINE=${1:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}
SRC=drave-core/src/gguf.rs

[ -d "$RACINE" ] || { echo "llama.cpp introuvable : $RACINE"; exit 2; }
[ -f "$SRC" ] || { echo "source introuvable : $SRC"; exit 2; }

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# 1. La vérité : un programme lié à libggml imprime (type, bloc, taille).
cat > "$TMP/tailles.c" <<'C'
#include <stdio.h>
#include "ggml.h"
int main(void) {
    for (int t = 0; t <= 64; t++) {
        enum ggml_type ty = (enum ggml_type)t;
        // L'ORDRE COMPTE : les types creux (4, 5, 31…) n'ont pas d'entrée dans
        // la table des noms, et lire `ggml_type_name` avant d'avoir vérifié que
        // le type existe fait tomber le programme — sans un mot, la sortie
        // tamponnée n'étant jamais vidée. C'est arrivé en écrivant cet outil.
        int64_t bs = ggml_blck_size(ty);
        size_t ts = ggml_type_size(ty);
        // Un type absent de la table de ggml rend des valeurs NON INITIALISEES
        // (on a vu « bloc 139716407193616 ») : borner est le seul moyen de
        // distinguer un type récent d'un trou dans l'énumération.
        if (bs <= 0 || bs > 1024 || ts == 0 || ts > 1024) continue;
        printf("%d %lld %zu\n", t, (long long)bs, ts);
    }
    return 0;
}
C
gcc -I"$RACINE/ggml/include" -I"$RACINE/ggml/src" "$TMP/tailles.c" -o "$TMP/tailles" \
    -L"$RACINE/build/bin" -lggml -lggml-base 2>"$TMP/gcc.err" || {
    echo "compilation impossible contre libggml :"; sed 's/^/  /' "$TMP/gcc.err" | head -5; exit 2; }
LD_LIBRARY_PATH="$RACINE/build/bin" "$TMP/tailles" | sort -n > "$TMP/ggml.txt"

# 2. Ce que dit le moteur : les bras `N => (bloc, octets),` de octets_tensor_opt.
python3 - "$SRC" > "$TMP/rust.txt" <<'PY'
import re, sys
src = open(sys.argv[1]).read()
# On ne lit QUE la fonction de table, pour ne pas ramasser d'autres constantes.
debut = src.index("pub fn octets_tensor_opt")
corps = src[debut:src.index("\n    }", debut)]
for m in re.finditer(r'(\d+)(?:u64)?\s*=>\s*\(\s*(\d+)(?:u64)?\s*,\s*([^)]+?)\s*\)', corps):
    t, bloc, taille = int(m.group(1)), m.group(2), m.group(3).strip()
    # `TAILLE_Q4K as u64` et `210` se lisent pareil ; on résout les deux noms.
    taille = re.sub(r'TAILLE_Q4K as u64', '144', taille)
    taille = re.sub(r'TAILLE_Q6K as u64', '210', taille)
    bloc = re.sub(r'u64$', '', bloc)
    taille = re.sub(r'u64$', '', taille)
    if not taille.isdigit():
        print(f"# type {t} : taille non résolue ({taille})", file=sys.stderr)
        continue
    print(f"{t} {bloc} {taille}")
PY

if [ ! -s "$TMP/rust.txt" ]; then
    echo "aucune entrée lue dans $SRC — la forme de la table a changé"
    exit 2
fi

# 3. Comparaison.
manquants=0; divergents=0; verifies=0
while read -r t bloc taille; do
    ligne=$(grep -E "^$t " "$TMP/ggml.txt" || true)
    if [ -z "$ligne" ]; then
        printf "  type %-3s absent de la table du moteur (%s/%s)\n" "$t" "$bloc" "$taille"
        manquants=$((manquants + 1))
        continue
    fi
    set -- $ligne
    if [ "$2" != "$bloc" ] || [ "$3" != "$taille" ]; then
        printf "  type %-3s DIVERGE : moteur %s/%s, ggml %s/%s\n" "$t" "$bloc" "$taille" "$2" "$3"
        divergents=$((divergents + 1))
    else
        verifies=$((verifies + 1))
    fi
done < "$TMP/rust.txt"

# 4. Les types que ggml connaît et que le moteur ignore. Ce ne sont pas des
#    fautes — le moteur n'a pas à lire tous les formats — mais un type qu'on
#    rencontrerait dans un fichier réel serait compté zéro sans le dire.
# Les noms ne sont PAS demandés à ggml : `ggml_type_name` tombe sur les types
# récents dont la table de noms n'est pas remplie (segfault, pas de retour NULL).
# Le numéro et les deux nombres suffisent à compléter la table.
inconnus=""
while read -r t bloc taille; do
    if ! grep -qE "^$t " "$TMP/rust.txt"; then
        inconnus="$inconnus\n  type $t : bloc $bloc, $taille octets"
    fi
done < "$TMP/ggml.txt"

echo "types confondus : $verifies · divergents : $divergents · absents du moteur : $manquants"
if [ -n "$inconnus" ]; then
    echo -e "types connus de ggml que le moteur ne lit pas :$inconnus"
    echo "  (le moteur SIGNALE un type inconnu au lieu de le compter zéro ;"
    echo "   ajouter ces entrées à octets_tensor_opt pour les lire)"
    echo "  ATTENTION : certains numéros ne correspondent à AUCUN type (trou dans"
    echo "  l'énumération) et ggml rend alors des valeurs non initialisées ; elles"
    echo "  passent le filtre de bornes et apparaissent ici à tort."
fi
[ "$divergents" -gt 0 ] && exit 1
exit 0
