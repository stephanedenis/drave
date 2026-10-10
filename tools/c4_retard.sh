#!/bin/bash
# c4_retard.sh — C4 : le PRIX D'UN ÉTAT EN RETARD, c'est-à-dire la question d'un ordonnanceur asynchrone.
#
# POURQUOI CETTE MESURE. C4 (horloges par région) demande l'**asynchronisme réel** : chaque région
# avance à son rythme, et une région peut recevoir l'état d'une autre **avec du retard**. Avant
# d'écrire un ordonnanceur, il faut savoir **ce que coûte le retard** : si un pas de retard ne
# coûte rien, on peut tolérer beaucoup ; s'il coûte cher, la borne de péremption doit être serrée.
#
# CE QUI EST MESURÉ, ET COMMENT. On capture l'état de la couche L à chaque position, puis on
# l'impose **décalé de k positions** (l'état de la position p−k sert à la position p). C'est
# exactement ce que fait une région en retard d'un pas : elle fournit un état qui décrit le monde
# d'AVANT. La perplexité qui en résulte est le prix du retard.
#
# Ce n'est pas une simulation du protocole : c'est la borne **optimiste** du coût du retard (l'état
# arrive, il est juste vieux). Ce qu'un vrai asynchronisme ajoute — l'ordre des messages, la
# péremption, la reprise — n'est pas mesuré ici, et c'est écrit dans la fiche.
#
# Usage : tools/c4_retard.sh [jetons] [couche] [retards]
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
N=${1:-128}
L=${2:-12}
RETARDS=${3:-"0 1 2 4 8 16"}
CTX=${CTX:-$((N * 2))}
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }

POS=$(seq -s, 0 $((N - 1)))
$D "$M" --ppl "$IDS" --limit "$N" --ctx "$CTX" --threads 8 --couches "0:$L" --tete-partielle \
   --etat-sortie "$T/s" --etat-pos "$POS" > "$T/cap.log" 2>&1
[ -s "$T/s.0" ] || { echo "  ❌ capture vide (faut-il --tete-partielle ?)"; exit 1; }

python3 - "$T" "$N" "$RETARDS" <<'PY'
import pathlib, struct, sys
import numpy as np
t, n, retards = pathlib.Path(sys.argv[1]), int(sys.argv[2]), [int(x) for x in sys.argv[3].split()]
X = np.vstack([np.frombuffer((t / f"s.{i}").read_bytes(), dtype="<f4") for i in range(n)])
def ecrit(nom, Y):
    (t / nom).write_bytes(b"REFD" + struct.pack("<i", 4) + struct.pack("<4i", Y.shape[1], 1, 1, 1)
                          + Y.astype("<f4").tobytes())
for k in retards:
    Y = X.copy()
    if k > 0:
        Y[k:] = X[:n - k]          # l'état de p−k sert à la position p : une région en retard
    ecrit(f"r{k}.refd", Y)
print(f"  {n} états de {X.shape[1]} canaux · retards testés : {retards}")
PY

REF=$($D "$M" --ppl "$IDS" --limit "$N" --ctx "$CTX" --threads 8 2>&1 \
      | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+" | head -1)
echo "  modèle entier (référence) : $REF"
printf '  %-8s %-14s %s\n' "retard" "perplexité" "prix"
prec=""
for k in $RETARDS; do
    v=$(DRAVE_ETAT_ENTREE="$T/r$k.refd" $D "$M" --ppl "$IDS" --limit "$N" --ctx "$CTX" --threads 8 \
        --couches "$L:24" --tete-partielle 2>&1 | grep -oE "perplexité [0-9.]+ sur" \
        | grep -oE "[0-9.]+" | head -1)
    printf '  %-8s %-14s %s\n' "$k" "${v:-?}" "$(python3 -c "
r, v = float('$REF'), float('${v:-0}')
print(f'{v/r:+.2f}×' if v > 0 and r > 0 else '?')")"
    prec=$v
done
echo
echo "Lecture : le retard 0 est l'invariant (coupe exacte). Chaque pas de retard supplémentaire"
echo "donne un état qui décrit un monde plus ancien : le prix est ce que l'ordonnanceur doit borner."
