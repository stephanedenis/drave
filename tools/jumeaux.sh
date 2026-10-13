#!/bin/bash
# jumeaux.sh — C9, latéralité : deux instances jumelles échangent leur état à une couche.
#
# CE QUE LA LATÉRALITÉ VEUT DIRE, ET CE QU'ELLE NE PEUT PAS FAIRE. Le plan
# (`docs/plan-cerveau-complet.md` § C9) demande deux instances jumelles du même modèle et un lien
# **homotopique par couche**, avec un invariant : **échange désactivé ⇒ chaque instance est
# identique au modèle seul**. La conception (`docs/note-lateralite-c9.md`) ajoute la garde qui
# compte : **deux jumeaux identiques avec la même entrée ne peuvent PAS gagner** — ils calculent
# déjà la même chose. Ce banc mesure donc deux choses séparées :
#
#   1. l'ÉCHANGE est exact et coûte ce qu'il coûte (invariant du plan) ;
#   2. ce que l'échange APPORTE quand les deux vues diffèrent — et il faut, pour le dire
#      honnêtement, un **CONTRÔLE** : mélanger un état propre et un état bruité, c'est d'abord
#      une réduction de bruit (le mélange a la moitié du bruit). Le contrôle est donc l'état
#      bruité à la moitié du bruit : si le mélange ne fait pas mieux que lui, l'échange n'a RIEN
#      apporté de plus que la moyenne — et c'est ce qu'il faut publier.
#
# Usage : tools/jumeaux.sh [jetons] [couche] [fraction_de_bruit]
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
. tools/_corpus.sh   # régénère le corpus s'il manque (voir l'en-tête du fichier)
N=${1:-32}          # jetons
L=${2:-12}          # couche où les jumeaux se parlent
FRAC=${3:-0.10}     # bruit du jumeau dégradé, en fraction de la RMS de l'état
# Le contexte SUIT la longueur : à 128 jetons et ctx 64, toutes les mesures sortaient vides
# (« ? ») — le moteur ne peut pas noter plus de jetons que son contexte.
CTX=${CTX:-$(( N * 2 ))}
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT

[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }

ppl () { # $@ = drapeaux ; imprime la perplexité
    $D "$M" --ppl "$IDS" --limit "$N" --ctx "$CTX" --threads 8 "$@" 2>&1 \
      | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+" | head -1
}
ppl_impose () { # $1 = fichier d'état imposé (REFD) ; $@ = drapeaux supplémentaires
    local f=$1; shift
    DRAVE_ETAT_ENTREE="$f" $D "$M" --ppl "$IDS" --limit "$N" --ctx "$CTX" --threads 8 \
      --couches "$L:24" --tete-partielle "$@" 2>&1 \
      | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+" | head -1
}

POS=$(seq -s, 0 $((N - 1)))
echo "=== capture des deux VUES (couches 0:$L, $N jetons) ==="
# Vue A : l'attention complète. Vue B : attention FENÊTRÉE — une vue valide, mais différente.
$D "$M" --ppl "$IDS" --limit "$N" --ctx "$CTX" --threads 8 --couches "0:$L" --tete-partielle \
   --etat-sortie "$T/a" --etat-pos "$POS" > "$T/cap_a.log" 2>&1
$D "$M" --ppl "$IDS" --limit "$N" --ctx "$CTX" --threads 8 --couches "0:$L" --tete-partielle \
   --attn-window 8 --etat-sortie "$T/b" --etat-pos "$POS" > "$T/cap_b.log" 2>&1
[ -s "$T/a.0" ] && [ -s "$T/b.0" ] || { echo "  ❌ capture incomplète"; exit 1; }

python3 - "$T" "$N" "$FRAC" <<'PY'
import pathlib, struct, sys
import numpy as np
t, n, frac = pathlib.Path(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
def lit(p):
    return np.vstack([np.frombuffer((t / f"{p}.{i}").read_bytes(), dtype="<f4") for i in range(n)])
def ecrit(nom, X):
    entete = b"REFD" + struct.pack("<i", 4) + struct.pack("<4i", X.shape[1], 1, 1, 1)
    (t / nom).write_bytes(entete + X.astype("<f4").tobytes())
A, B = lit("a"), lit("b")
rms = float(np.sqrt((A ** 2).mean()))
rng = np.random.default_rng(7)
bruit = rng.normal(0, frac * rms, A.shape).astype(np.float32)
A_bruite = (A + bruit).astype(np.float32)
ecrit("A.refd", A)                      # vue A seule (l'invariant : == modèle entier)
ecrit("B.refd", B)                      # vue B seule (fenêtrée)
ecrit("B_melange.refd", ((A + B) / 2).astype(np.float32))   # échange A↔B
ecrit("A_bruite.refd", A_bruite)        # jumeau dégradé
ecrit("A_melange.refd", ((A + A_bruite) / 2).astype(np.float32))  # échange A↔A(bruité)
# CONTRÔLE : le même bruit, à la moitié de l'amplitude — c'est ce que « mélanger » fait au bruit.
ecrit("A_demi.refd", (A + bruit / 2).astype(np.float32))
print(f"états : {A.shape} · RMS {rms:.3f} · bruit {frac*100:.0f} % ({frac*rms:.3f}) "
      f"· octets échangés par pas : {A.shape[1]*4} (f32 dense)")
PY

echo
echo "=== ce que chaque vue (et chaque échange) donne ==="
REF=$(ppl)
A=$(ppl_impose "$T/A.refd")
B=$(ppl_impose "$T/B.refd")
BM=$(ppl_impose "$T/B_melange.refd")
AB=$(ppl_impose "$T/A_bruite.refd")
AM=$(ppl_impose "$T/A_melange.refd")
AD=$(ppl_impose "$T/A_demi.refd")
printf '  %-42s %s\n' "modèle entier (référence)" "$REF"
printf '  %-42s %s\n' "vue A seule (invariant : = référence)" "${A:-?}"
printf '  %-42s %s\n' "vue B seule (fenêtrée)" "${B:-?}"
printf '  %-42s %s\n' "échange A↔B (moyenne)" "${BM:-?}"
printf '  %-42s %s\n' "jumeau A BRUITÉ ($FRAC)" "${AB:-?}"
printf '  %-42s %s\n' "échange A↔A(bruité) (moyenne)" "${AM:-?}"
printf '  %-42s %s\n' "CONTRÔLE : bruit à moitié (même énergie)" "${AD:-?}"
echo
python3 - <<PY
import sys
def f(x):
    try: return float(x)
    except Exception: return None
ref, a, b, bm, ab, am, ad = map(f, "$REF $A $B $BM $AB $AM $AD".split())
if None in (ref, a, b, bm, ab, am, ad) or min(ref,a,b,bm,ab,am,ad) <= 0:
    sys.exit("  ❌ une des mesures manque")
print(f"  invariant du plan      : vue A = référence ? {'OUI' if abs(a-ref) < 1e-3*ref else 'NON ('+str(a)+' contre '+str(ref)+')'}")
print(f"  échange A↔B            : {bm:.4f} contre A {a:.4f} et B {b:.4f} → " +
      ("mieux que les deux" if bm < min(a,b) else "PAS mieux que la meilleure des deux"))
print(f"  échange A↔A(bruité)    : {am:.4f} contre A(bruité) {ab:.4f} → " +
      (f"il RÉCUPÈRE (×{ab/am:.1f})" if am < ab else "aucune récupération"))
ecart = abs(am-ad)/am
print(f"  CONTRÔLE (bruit/2)     : {ad:.4f} · écart avec l'échange {ecart*100:.3f} % → " +
      ("l'échange n'apporte RIEN de plus que la moyenne (c'est une réduction de bruit)" if ecart < 0.05
       else "l'échange fait autre chose qu'une moyenne de bruit — À INSTRUIRE"))
PY
echo
echo "Lecture : l'échange est EXACT (invariant du plan) et il coûte 3 584 octets par pas et par"
echo "couche échangée en f32 dense. Ce qu'il apporte de plus qu'une moyenne, c'est le contrôle qui"
echo "le dit — et s'il n'apporte rien, c'est écrit."
