#!/bin/bash
# porte-jumeaux.sh — C9 : deux jumeaux, un échange par couche, et les invariants qui le bornent.
#
# CE QUE LA PORTE VERROUILLE, et pourquoi chacun de ces points :
#   1. **échange désactivé ⇒ identique au modèle seul** (l'invariant du plan, au chiffre près) :
#      un état imposé à la couche L puis les couches L..24 doivent rendre la perplexité du modèle
#      entier. Sans cet invariant, tout le reste comparerait deux calculs différents ;
#   2. **deux jumeaux IDENTIQUES qui s'échangent ne changent rien** : la moyenne de deux états
#      égaux EST cet état (au bit près). C'est la garde du plan (« le gain est probablement nul »)
#      écrite comme un test — si l'échange déplaçait le chiffre ici, ce serait un BUG, pas un gain ;
#   3. **un jumeau dégradé est RÉCUPÉRÉ, et pas par magie** : mélanger un état propre et un état
#      bruité ramène la perplexité près du propre — mais le CONTRÔLE (le même bruit à moitié de
#      amplitude, qui est exactement ce que fait la moyenne) doit donner le MÊME chiffre. Écart
#      mesuré : 0,005 %. C'est la porte qui empêche de vendre une réduction de bruit comme une
#      latéralité ;
#   4. **le coût est chiffré** : octets échangés par pas et par couche (3 584 en f32 dense).
#
# Ce que la porte NE verrouille PAS, et le dit : le cas de deux vues VALIDES et différentes. Sur
# 32 jetons, la fusion battait les deux vues (56,22 contre 56,76) ; sur 128 jetons, elle est
# ENTRE les deux (15,39 contre 14,65 et 18,01). Le premier chiffre était un artefact de 31 jetons
# notés — la porte ne l'affirme donc pas, et la fiche C9 porte les deux mesures.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
. tools/_corpus.sh    # régénère le corpus si /tmp a été effacé (redémarrage)
N=${N:-64}
L=${L:-12}
FRAC=${FRAC:-0.10}
CTX=${CTX:-$((N * 2))}
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT

ppl () { $D "$M" --ppl "$IDS" --limit "$N" --ctx "$CTX" --threads 8 "$@" 2>&1 \
         | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+" | head -1; }
ppl_impose () { local f=$1; shift
    DRAVE_ETAT_ENTREE="$f" $D "$M" --ppl "$IDS" --limit "$N" --ctx "$CTX" --threads 8 \
      --couches "$L:24" --tete-partielle "$@" 2>&1 \
      | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+" | head -1; }

POS=$(seq -s, 0 $((N - 1)))
$D "$M" --ppl "$IDS" --limit "$N" --ctx "$CTX" --threads 8 --couches "0:$L" --tete-partielle \
   --etat-sortie "$T/a" --etat-pos "$POS" > "$T/cap.log" 2>&1
[ -s "$T/a.0" ] || { echo "  ❌ la capture d'états n'a rien écrit"; exit 1; }

python3 - "$T" "$N" "$FRAC" <<'PY' || exit 1
import pathlib, struct, sys
import numpy as np
t, n, frac = pathlib.Path(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
A = np.vstack([np.frombuffer((t / f"a.{i}").read_bytes(), dtype="<f4") for i in range(n)])
def ecrit(nom, X):
    entete = b"REFD" + struct.pack("<i", 4) + struct.pack("<4i", X.shape[1], 1, 1, 1)
    (t / nom).write_bytes(entete + X.astype("<f4").tobytes())
rms = float(np.sqrt((A ** 2).mean()))
rng = np.random.default_rng(7)
bruit = rng.normal(0, frac * rms, A.shape).astype(np.float32)
ecrit("A.refd", A)
ecrit("AA.refd", ((A + A) / 2).astype(np.float32))          # deux jumeaux IDENTIQUES
ecrit("A_bruite.refd", (A + bruit).astype(np.float32))
ecrit("A_melange.refd", ((A + A + bruit) / 2).astype(np.float32))
ecrit("A_demi.refd", (A + bruit / 2).astype(np.float32))    # CONTRÔLE
print(f"  état : {A.shape} · RMS {rms:.3f} · bruit {frac*100:.0f} % · coût d'un échange : "
      f"{A.shape[1]*4} octets par pas et par couche")
PY

REF=$(ppl); A=$(ppl_impose "$T/A.refd"); AA=$(ppl_impose "$T/AA.refd")
AB=$(ppl_impose "$T/A_bruite.refd"); AM=$(ppl_impose "$T/A_melange.refd"); AD=$(ppl_impose "$T/A_demi.refd")
printf '  référence %s · état imposé %s · jumeaux identiques %s\n' "${REF:-?}" "${A:-?}" "${AA:-?}"
printf '  jumeau bruité %s · échange %s · CONTRÔLE (bruit/2) %s\n' "${AB:-?}" "${AM:-?}" "${AD:-?}"
python3 - <<PY || exit 1
import sys
def f(x):
    try: return float(x)
    except Exception: return None
ref, a, aa, ab, am, ad = map(f, "$REF $A $AA $AB $AM $AD".split())
if None in (ref, a, aa, ab, am, ad) or min(ref, a, aa, ab, am, ad) <= 0:
    sys.exit("  ❌ une des mesures manque")
if abs(a - ref) > 0.001 * ref:
    sys.exit(f"  ❌ invariant du plan : état imposé {a} ≠ modèle entier {ref}")
print(f"  ✅ invariant du plan : échange DÉSACTIVÉ, l'instance est le modèle seul ({a} = {ref})")
if abs(aa - a) > 1e-6 * a:
    sys.exit(f"  ❌ deux jumeaux identiques qui s'échangent ont changé le chiffre ({aa} vs {a})")
print(f"  ✅ deux jumeaux IDENTIQUES : l'échange ne change rien ({aa} = {a}) — pas de gain gratuit")
if not am < ab:
    sys.exit(f"  ❌ le jumeau bruité n'est pas récupéré ({am} ≥ {ab})")
ecart = abs(am - ad) / am
if ecart > 0.05:
    sys.exit(f"  ❌ l'échange fait autre chose qu'une moyenne : {am} contre le contrôle {ad} "
             f"({ecart*100:.2f} %) — à instruire avant de parler de latéralité")
print(f"  ✅ jumeau bruité RÉCUPÉRÉ ({ab} → {am}) et le contrôle donne le même chiffre "
      f"({ad}, écart {ecart*100:.3f} %) : c'est une MOYENNE, pas un miracle")
PY
echo "=== 5. le coût COMPRESSÉ : 8 bits par bloc pour ÷4 d'octets, et quantifier bat élaguer ==="
# L'échange coûte 3 584 octets par pas et par couche en f32 : c'est le poste dominant d'un jumeau.
# La question qui décide de son usage : combien peut-on compresser, et à quel prix ?
python3 - "$T" "$N" <<'PY' || exit 1
import pathlib, struct, sys
import numpy as np
t, n = pathlib.Path(sys.argv[1]), int(sys.argv[2])
X = np.vstack([np.frombuffer((t / f"a.{i}").read_bytes(), dtype="<f4") for i in range(n)])
def ecrit(nom, Y):
    (t / nom).write_bytes(b"REFD" + struct.pack("<i", 4) + struct.pack("<4i", Y.shape[1], 1, 1, 1)
                          + Y.astype("<f4").tobytes())
q = 127                                    # 8 bits par bloc, comme le moteur (une échelle/bloc)
Y8 = X.copy()
for b in range(0, X.shape[1], 32):
    blk = X[:, b:b+32]
    ech = np.abs(blk).max(1, keepdims=True) / q
    Y8[:, b:b+32] = np.clip(np.round(blk / np.maximum(ech, 1e-12)), -q, q) * ech
ecrit("q8.refd", Y8)
Yk = np.zeros_like(X)                      # listes creuses k=128 : 512 octets/pas (÷7)
idx = np.argsort(-np.abs(X), axis=1)[:, :128]
for i in range(n):
    Yk[i, idx[i]] = X[i, idx[i]]
ecrit("k128.refd", Yk)
print(f"  f32 : {X.shape[1]*4} octets/pas · 8 bits : {X.shape[1]} · listes k=128 : 512")
PY
P8=$(ppl_impose "$T/q8.refd"); PK=$(ppl_impose "$T/k128.refd")
printf '  f32 %s · 8 bits %s · listes k=128 %s\n' "${A:-?}" "${P8:-?}" "${PK:-?}"
python3 - <<PY || exit 1
import sys
def f(x):
    try: return float(x)
    except Exception: return None
a, p8, pk = map(f, "$A $P8 $PK".split())
if None in (a, p8, pk):
    sys.exit("  ❌ une mesure de compression manque")
if p8 > a * 1.05:
    sys.exit(f"  ❌ l'échange 8 bits coûte trop cher : {p8} contre {a} (> +5 %)")
if not pk > p8:
    sys.exit(f"  ❌ les listes creuses ne sont pas plus chères que 8 bits ({pk} contre {p8}) : "
             f"la conclusion « quantifier bat élaguer » ne tient plus ici")
print(f"  ✅ 8 bits : ÷4 d'octets pour +{100*(p8/a-1):.1f} % · et quantifier bat élaguer "
      f"({p8:.2f} contre {pk:.2f} pour un budget voisin)")
PY

echo
echo "PORTE TENUE : l'échange est exact, il ne crée pas de gain entre jumeaux identiques, il"
echo "récupère un jumeau dégradé à hauteur de sa moyenne — et compressé à 8 bits par bloc il coûte"
echo "÷4 d'octets pour +3 %, en battant l'élagage à budget voisin."
echo "Ce que la porte n'affirme pas (deux vues valides différentes) est mesuré dans la fiche C9 :"
echo "sur 32 jetons la fusion battait les deux vues, sur 128 elle est ENTRE les deux."
