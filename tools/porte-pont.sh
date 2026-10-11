#!/bin/bash
# porte-pont.sh — la porte des capacités C9/C10 : le PONT à fibres limitées.
#
# LA QUESTION, ET ELLE EST CELLE DU CORPS CALLEUX. Deux régions d'un modèle échangent
# un état à chaque pas. Combien faut-il échanger pour ne rien perdre ? La réponse ne
# se devine pas : c'est une courbe qualité ↔ octets par pas.
#
# LES DEUX PIÈGES QUE CETTE PORTE A TROUVÉS, et qui ont changé sa forme :
#
#   1. le pont n'était appliqué QUE du pilote vers le nœud ; le nœud renvoyait tout
#      (1 096 octets à l'aller contre 1 959 au retour). Un corps calleux à moitié
#      coupé n'est pas un pont : les deux processus reçoivent maintenant le même
#      `--pont-k` ;
#   2. **en dense f32, élaguer ne réduit AUCUN octet** : le flux envoie 896 valeurs,
#      que 448 d'entre elles soient nulles ou non. Le pont ne fait alors que perdre
#      de la qualité — 3 664 octets et +7,8 % de perplexité à 448 fibres. C'est
#      l'ENCODAGE qui convertit la parcimonie en octets (`--flux-blocs`,
#      `--flux-liste`), et c'est pourquoi la courbe est mesurée en « listes par blocs ».
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
. tools/_corpus.sh    # régénère le corpus si /tmp a été effacé (redémarrage)
LIMITE=${LIMITE:-48}
PORT=${PORT:-$((55000 + RANDOM % 500))}
T=$(mktemp -d)
TOPO="$T/topo.json"
cat > "$TOPO" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"d","couches":[12,23],"instance":"127.0.0.1:$PORT"}],
 "liens":[{"de":"local","vers":"d","mode":"f32"}]}
JSON
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }

# Le nœud prend le MÊME `--pont-k` que le pilote : c'est la seule façon d'avoir un
# pont dans les deux sens.
nœud() { $D "$M" --flux-serveur "$PORT" --ctx 256 --threads 8 "$@" > "$T/n.log" 2>&1 & echo $!; }
pilote() {
  $D "$M" --ppl-reparti "127.0.0.1:$PORT" --topologie "$TOPO" --ids-file "$IDS" \
     --limit "$LIMITE" --ctx 256 --threads 8 "$@" 2>&1
}
ppl() { printf '%s\n' "$1" | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$"; }
aller() { printf '%s\n' "$1" | grep -oE "[0-9]+ octets par flux" | head -1 | grep -oE "^[0-9]+"; }
retour() { printf '%s\n' "$1" | grep -oE "[0-9]+ au retour" | head -1 | grep -oE "^[0-9]+"; }

echo "=== 1. pont entier : identique au mode sans pont, dans LES DEUX encodages ==="
N=$(nœud); sleep 2
A=$(pilote --flux); REF=$(ppl "$A"); OD=$(aller "$A")
kill $N 2>/dev/null; wait $N 2>/dev/null
N=$(nœud); sleep 2
B=$(pilote --flux --pont-k 0); Z=$(ppl "$B")
kill $N 2>/dev/null; wait $N 2>/dev/null
N=$(nœud); sleep 2
C=$(pilote --flux --pont-k 4096); G=$(ppl "$C")
kill $N 2>/dev/null; wait $N 2>/dev/null
printf '%s\n' "$A" | grep -E "deux nœuds" | sed 's/^/  /'
echo "  dense f32 — sans pont : $REF · --pont-k 0 : $Z · --pont-k 4096 : $G"
[ "$REF" = "$Z" ] && [ "$REF" = "$G" ] \
  || { echo "  ❌ un pont entier doit être identique au mode sans pont"; exit 1; }
N=$(nœud); sleep 2
BL0=$(pilote --flux-blocs); REFB=$(ppl "$BL0")
kill $N 2>/dev/null; wait $N 2>/dev/null
N=$(nœud --pont-k 0); sleep 2
BL1=$(pilote --flux-blocs --pont-k 0); ZB=$(ppl "$BL1")
kill $N 2>/dev/null; wait $N 2>/dev/null
echo "  blocs — sans pont : $REFB · --pont-k 0 : $ZB"
[ "$REFB" = "$ZB" ] || { echo "  ❌ pont entier non identique en mode blocs"; exit 1; }
echo "  ✅ pont entier identique dans les deux encodages"

echo "=== 2. la courbe (listes par blocs) : perplexité ↔ fibres ↔ octets ==="
printf '  %8s  %12s  %10s  %10s  %10s\n' "fibres" "perplexité" "octets->" "octets<-" "ecart %"
OA=$(aller "$BL0"); OR=$(retour "$BL0")
printf '  %8s  %12s  %10s  %10s  %10s\n' "896" "$REFB" "$OA" "$OR" "0.000"
: > "$T/courbe.txt"
for K in 672 448 224 112; do
  N=$(nœud --pont-k "$K"); sleep 2
  R=$(pilote --flux-blocs --pont-k "$K"); P=$(ppl "$R")
  kill $N 2>/dev/null; wait $N 2>/dev/null
  [ -n "$P" ] || { echo "  ❌ aucune perplexité rendue à $K fibres"; exit 1; }
  AK=$(aller "$R"); RK=$(retour "$R")
  python3 -c "
a, b = float('$REFB'), float('$P')
print('  %8d  %12s  %10s  %10s  %9.3f %%' % ($K, '$P', '$AK', '$RK', 100.0*(b-a)/a))"
  echo "$K $P $AK $RK" >> "$T/courbe.txt"
done

echo "=== 3. le pont est SYMÉTRIQUE, et il ÉCONOMISE des octets ==="
python3 - "$T/courbe.txt" "$OA" "$OR" <<'PY' || exit 1
import sys
pts = [l.split() for l in open(sys.argv[1])]
oa, or_ = int(sys.argv[2]), int(sys.argv[3])
for ch in pts:
    k, al, ret = int(ch[0]), int(ch[2]), int(ch[3])
    if ret >= or_:
        sys.exit(f"  ❌ à {k} fibres le RETOUR ne maigrit pas : {ret} contre {or_} sans pont")
    if al >= oa:
        sys.exit(f"  ❌ à {k} fibres l'ALLER ne maigrit pas : {al} contre {oa} sans pont")
dernier = pts[-1]
print(f"  ✅ les deux sens maigrissent : {oa}->{dernier[2]} à l'aller, "
      f"{or_}->{dernier[3]} au retour ({dernier[0]} fibres)")
PY

echo "=== 4. monotonie : plus de fibres ne peut pas faire pire ==="
python3 - "$T/courbe.txt" "$REFB" <<'PY' || exit 1
import sys
pts = [(int(l.split()[0]), float(l.split()[1])) for l in open(sys.argv[1])]
pts.append((896, float(sys.argv[2])))
pts.sort()
for (a, pa), (b, pb) in zip(pts, pts[1:]):
    if pa < pb - 1e-9:
        sys.exit(f"  ❌ la perplexité remonte en ajoutant des fibres : {a} -> {pa}, {b} -> {pb}")
pire = max(pts, key=lambda x: x[1])
print(f"  ✅ monotone sur {len(pts)} points · la pire est {pire[1]} à {pire[0]} fibres")
PY

echo "=== 5. élaguer COÛTE (sinon le pont n'est branché nulle part) ==="
PETIT=$(awk '$1 == 112 {print $2}' "$T/courbe.txt")
[ -n "$PETIT" ] || { echo "  ❌ mesure à 112 fibres absente"; exit 1; }
python3 -c "
import sys
a, b = float('$REFB'), float('$PETIT')
if b <= a:
    sys.exit('  ❌ 112 fibres sur 896 ne changent RIEN : le pont nest pas branché')
print('  ✅ 112 fibres sur 896 : %s -> %s (+%.2f %%)' % (a, b, 100.0*(b-a)/a))" || exit 1

echo "=== 6. PIÈGE : en dense f32, élaguer ne réduit AUCUN octet ==="
N=$(nœud --pont-k 448); sleep 2
D448=$(pilote --flux --pont-k 448); PD=$(ppl "$D448")
kill $N 2>/dev/null; wait $N 2>/dev/null
AD=$(aller "$D448"); RD=$(retour "$D448")
echo "  dense f32 à 448 fibres : $PD · $AD octets à l'aller, $RD au retour"
python3 - "$REF" "$PD" "$AD" "$OD" <<'PY' || exit 1
# La comparaison est EN DENSE DES DEUX CÔTÉS : la référence est l'exécution dense
# SANS pont, pas l'exécution en blocs (les confondre faisait échouer le cas pour une
# raison qui n'avait rien à voir — attrapé au premier essai).
import sys
ref, pd, ad, oa = float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
if ad != oa:
    sys.exit(f"  ❌ en dense f32 le nombre d'octets ne devrait PAS changer : {ad} contre {oa}")
if pd <= ref:
    sys.exit("  ❌ à 448 fibres la perplexité devrait être pire qu'à 896")
print(f"  ✅ en dense f32 : {ad} octets AVANT et APRÈS (aucune économie), et la "
      f"perplexité passe de {ref} à {pd}")
PY

echo "=== 7. à budget égal, QUANTIFIER bat ÉLAGUER ==="
P448=$(awk '$1 == 448 {print $2}' "$T/courbe.txt")
O448=$(awk '$1 == 448 {print $3}' "$T/courbe.txt")
echo "  blocs entier : $REFB à $OA octets · blocs + 448 fibres : $P448 à $O448 octets"
python3 - "$REFB" "$P448" "$O448" "$OA" <<'PY' || exit 1
import sys
refb, p448, o448, oa = float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
if o448 >= oa:
    sys.exit(f"  ❌ le pont de 448 fibres devrait coûter moins d'octets : {o448} contre {oa}")
rend_blocs = (refb / oa) * 1000.0
rend_pont = (p448 / o448) * 1000.0
if rend_pont < rend_blocs:
    sys.exit("  ❌ le pont élagué aurait un meilleur rendement que l'encodage complet")
print(f"  ✅ rendement (perplexité pour 1 000 octets) : blocs entier {rend_blocs:.1f} · "
      f"pont 448 fibres {rend_pont:.1f} — {100.0*(rend_pont-rend_blocs)/rend_blocs:.1f} % pire")
PY

echo "=== 8. LA FALAISE est entre 448 et 392 fibres ==="
# Mesurée en localisant : 448 fibres coûtent +2,81 %, 392 en coûtent +25,35 %. Ce n'est
# pas une pente, c'est une marche — et une marche à cet endroit dit quelque chose de
# précis : l'état au point de coupe a environ 450 canaux porteurs, et en dessous on
# entame le signal. Le cas verrouille les DEUX côtés de la marche.
N=$(nœud --pont-k 392); sleep 2
R392=$(pilote --flux-blocs --pont-k 392); P392=$(ppl "$R392")
kill $N 2>/dev/null; wait $N 2>/dev/null
printf '%s\n' "$R392" | grep -E "transport" | sed 's/^/  /'
python3 - "$REFB" "$P448" "$P392" <<'PY' || exit 1
import sys
refb, p448, p392 = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
d448, d392 = 100.0 * (p448 - refb) / refb, 100.0 * (p392 - refb) / refb
if d448 >= 5.0:
    sys.exit(f"  ❌ 448 fibres devraient coûter moins de 5 % : {d448:.2f} %")
if d392 <= 10.0:
    sys.exit(f"  ❌ 392 fibres devraient coûter plus de 10 % (la falaise) : {d392:.2f} %")
print(f"  ✅ 448 fibres : +{d448:.2f} % · 392 fibres : +{d392:.2f} % — la marche est entre les deux")
PY

rm -rf "$T"
