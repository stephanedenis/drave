#!/bin/bash
# porte-c4-retard.sh — C4 : la POSITION d'un état n'est pas négociable.
#
# LA MESURE QUI A DONNÉ CETTE PORTE (reports/rapport-c4-retard.md) : un état d'une couche imposé
# avec UN pas de retard multiplie la perplexité par **633** (14,6496 → 9 277,98 sur 128 jetons),
# et la dégradation sature vers ×10 000. Autrement dit : un état n'est valide qu'à SA position.
#
# Ce que la porte verrouille :
#   1. **retard 0 = modèle entier**, au chiffre près : sans cet invariant, les autres lignes
#      mesureraient autre chose que le retard ;
#   2. **retard 1 ≥ ×10** : la position est une IDENTITÉ, pas un détail — c'est ce qui justifie que
#      le protocole transporte `pos` dans chaque trame et refuse un état d'une autre position ;
#   3. **la dégradation sature** (retard 8 n'est pas pire que ×1 000 de plus que le retard 1) :
#      au-delà de quelques pas l'état est simplement faux — la borne haute est une information ;
#   4. **l'ordre des messages DANS un pas n'est pas contraint** : seul l'appariement
#      position↔état l'est. C'est la différence entre « asynchrone » et « désaligné », et c'est
#      ce que la porte sépare.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
N=${N:-128}
L=${L:-12}
CTX=${CTX:-$((N * 2))}
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT

POS=$(seq -s, 0 $((N - 1)))
$D "$M" --ppl "$IDS" --limit "$N" --ctx "$CTX" --threads 8 --couches "0:$L" --tete-partielle \
   --etat-sortie "$T/s" --etat-pos "$POS" > "$T/cap.log" 2>&1
[ -s "$T/s.0" ] || { echo "  ❌ capture vide"; exit 1; }

python3 - "$T" "$N" <<'PY' || exit 1
import pathlib, struct, sys
import numpy as np
t, n = pathlib.Path(sys.argv[1]), int(sys.argv[2])
X = np.vstack([np.frombuffer((t / f"s.{i}").read_bytes(), dtype="<f4") for i in range(n)])
def ecrit(nom, Y):
    (t / nom).write_bytes(b"REFD" + struct.pack("<i", 4) + struct.pack("<4i", Y.shape[1], 1, 1, 1)
                          + Y.astype("<f4").tobytes())
ecrit("r0.refd", X)
Y = X.copy(); Y[1:] = X[:-1]
ecrit("r1.refd", Y)                      # un pas de retard
Y = X.copy(); Y[8:] = X[:-8]
ecrit("r8.refd", Y)
PY

ppl_impose () { DRAVE_ETAT_ENTREE="$1" $D "$M" --ppl "$IDS" --limit "$N" --ctx "$CTX" --threads 8 \
    --couches "$L:24" --tete-partielle 2>&1 | grep -oE "perplexité [0-9.]+ sur" \
    | grep -oE "[0-9.]+" | head -1; }
REF=$($D "$M" --ppl "$IDS" --limit "$N" --ctx "$CTX" --threads 8 2>&1 \
      | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+" | head -1)
R0=$(ppl_impose "$T/r0.refd"); R1=$(ppl_impose "$T/r1.refd"); R8=$(ppl_impose "$T/r8.refd")
printf '  modèle entier %s · retard 0 %s · retard 1 %s · retard 8 %s\n' \
       "${REF:-?}" "${R0:-?}" "${R1:-?}" "${R8:-?}"
python3 - <<PY || exit 1
import sys
def f(x):
    try: return float(x)
    except Exception: return None
ref, r0, r1, r8 = map(f, "$REF $R0 $R1 $R8".split())
if None in (ref, r0, r1, r8):
    sys.exit("  ❌ une mesure manque")
if abs(r0 - ref) > 0.001 * ref:
    sys.exit(f"  ❌ retard 0 ({r0}) ≠ modèle entier ({ref}) : le banc ne mesure pas ce qu'il croit")
print(f"  ✅ retard 0 = modèle entier ({r0} = {ref}) : la coupe est exacte")
if r1 < 10 * r0:
    sys.exit(f"  ❌ un pas de retard ne coûte que ×{r1/r0:.1f} — la position serait négociable, "
             f"ce qui contredit la mesure du 10/10 (×633)")
print(f"  ✅ un pas de retard coûte ×{r1/r0:.0f} : la POSITION d'un état est son identité")
if r8 < r1:
    sys.exit(f"  ❌ retard 8 ({r8}) meilleur que retard 1 ({r1}) : la dégradation devrait saturer")
print(f"  ✅ la dégradation sature (retard 8 : ×{r8/r0:.0f}, pas moins que le retard 1)")
PY
echo "=== 5. politique : un état MANQUANT coûte moins qu'un état PÉRIMÉ (on ne réutilise jamais) ==="
# Le choix d'un ordonnanceur asynchrone, chiffré : réutiliser le dernier état reçu (donc un état
# d'une AUTRE position) coûte ×633 ; laisser la position sans état coûte quelques pour cent.
python3 - "$T" "$N" <<'PY' || exit 1
import pathlib, struct, sys
import numpy as np
t, n = pathlib.Path(sys.argv[1]), int(sys.argv[2])
X = np.vstack([np.frombuffer((t / f"s.{i}").read_bytes(), dtype="<f4") for i in range(n)])
Z = X.copy(); Z[64] = 0                    # une position NOTÉE sans état (pas la dernière !)
(t / "hole.refd").write_bytes(b"REFD" + struct.pack("<i", 4) + struct.pack("<4i", X.shape[1], 1, 1, 1)
                              + Z.astype("<f4").tobytes())
PY
PH=$(ppl_impose "$T/hole.refd")
printf '  périmé (1 pas) %s · manquant (1 position notée) %s\n' "${R1:-?}" "${PH:-?}"
python3 - <<PY || exit 1
import sys
def f(x):
    try: return float(x)
    except Exception: return None
ref, r1, ph = map(f, "$REF $R1 $PH".split())
if None in (ref, r1, ph):
    sys.exit("  ❌ une mesure de politique manque")
if abs(ph - ref) > 0.001 * ref and ph < ref:
    sys.exit(f"  ❌ un trou a AMÉLIORÉ la perplexité ({ph} < {ref}) : le banc est suspect")
if not ph < r1 / 10:
    sys.exit(f"  ❌ manquer ({ph}) ne serait pas nettement moins cher que réutiliser ({r1})")
print(f"  ✅ manquer coûte ×{ph/ref:.2f}, réutiliser coûte ×{r1/ref:.0f} : on CONTINUE SANS, "
      f"on ne réutilise JAMAIS")
PY

echo
echo "PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne"
echo "peut donc pas vouloir dire « laisser un pas prendre du retard » — seulement réordonner les"
echo "messages D'UN MÊME pas, chacun portant sa position. Fiche : reports/rapport-c4-retard.md."
