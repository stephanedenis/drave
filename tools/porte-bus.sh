#!/bin/bash
# porte-bus.sh — la porte de la capacité C5 : le bus de modulation.
#
# L'invariant, et il a des dents :
#   1. bus NEUTRE (`gain=1`)      -> les empreintes de la trace sont IDENTIQUES à
#      celles d'une exécution sans bus : le bus ne change rien, au bit près ;
#   2. bus NON NEUTRE (`gain=1.5`) -> la perplexité CHANGE : le bus est branché.
#      Sans ce cas, « canal nul => rien » serait vrai d'un bus qui ne fait rien ;
#   3. bus non neutre sur le NŒUD -> la région distante l'applique aussi.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
LIMITE=${LIMITE:-64}
PORT=${PORT:-$((52000 + RANDOM % 800))}
T=$(mktemp -d)
cat > "$T/topo.json" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"d","couches":[12,23],"instance":"127.0.0.1:$PORT"}],
 "liens":[{"de":"local","vers":"d","mode":"f32"}]}
JSON
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }
nœud() { $D "$M" --flux-serveur "$PORT" --ctx 256 --threads 8 "$@" > "$T/n.log" 2>&1 & echo $!; }
ppl() { $D "$M" --ppl-reparti "127.0.0.1:$PORT" --topologie "$T/topo.json" --ids-file "$IDS" \
        --limit "$LIMITE" --ctx 256 --threads 8 --flux "$@" 2>&1 \
        | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$"; }

echo "=== 1. bus NEUTRE : la sortie doit être identique AU BIT PRÈS ==="
N=$(nœud); sleep 2
A=$(ppl --trace-globale "$T/sans.txt"); kill $N 2>/dev/null; wait $N 2>/dev/null
N=$(nœud); sleep 2
B=$(ppl --bus gain=1 --trace-globale "$T/neutre.txt"); kill $N 2>/dev/null; wait $N 2>/dev/null
echo "  sans bus : $A · bus neutre : $B"
sans_det() { grep -v '^#' "$1" | awk '{print $1, $2, $3, $4, $5}'; }
if [ "$A" = "$B" ] && diff -q <(sans_det "$T/sans.txt") <(sans_det "$T/neutre.txt") >/dev/null; then
    echo "  ✅ perplexité ET empreintes identiques ($(grep -vc '^#' "$T/sans.txt") croisements, horodatage exclu)"
else
    echo "  ❌ le bus neutre a changé quelque chose"; exit 1
fi

echo "=== 2. bus NON NEUTRE : le bus doit être BRANCHÉ ==="
N=$(nœud); sleep 2
C=$(ppl --bus gain=1.5 --trace-globale "$T/gain.txt"); kill $N 2>/dev/null; wait $N 2>/dev/null
echo "  gain=1.5 : $C"
if [ "$C" != "$A" ]; then echo "  ✅ la sortie change : le bus agit"
else echo "  ❌ gain non neutre sans effet : le bus n'est pas branché"; exit 1; fi
diff -q <(sans_det "$T/gain.txt") <(sans_det "$T/sans.txt") >/dev/null \
    && { echo "  ❌ les empreintes n'ont pas changé"; exit 1; } || echo "  ✅ les empreintes changent aussi"

echo "=== 3. le bus sur un nœud RELAIS (région du MILIEU) ==="
# Le gain du nœud FINAL est absorbé par la normalisation de sortie (une norme
# divise par la norme : un facteur scalaire y disparaît). C'est un nœud du MILIEU
# qui prouve que le bus traverse les instances — sa sortie alimente une autre
# région, elle n'est pas normalisée avant.
P1=$((PORT + 1)); P2=$((PORT + 2))
cat > "$T/t3.json" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"n1","couches":[12,17],"instance":"127.0.0.1:$P1"},
  {"id":"n2","couches":[18,23],"instance":"127.0.0.1:$P2"}],
 "liens":[{"de":"local","vers":"n1","mode":"f32"},{"de":"n1","vers":"n2","mode":"f32"}]}
JSON
$D "$M" --flux-serveur "$P2" --topologie "$T/t3.json" --region n2 --ctx 256 --threads 8 > "$T/n2.log" 2>&1 & N2=$!
sleep 2
$D "$M" --flux-serveur "$P1" --topologie "$T/t3.json" --region n1 --bus gain=1.5 --ctx 256 --threads 8 > "$T/n1.log" 2>&1 & N1=$!
sleep 3
R=$($D "$M" --ppl-reparti "127.0.0.1:$P1" --topologie "$T/t3.json" --ids-file "$IDS" \
     --limit "$LIMITE" --ctx 256 --threads 8 --flux 2>&1 | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
kill $N1 $N2 2>/dev/null; wait $N1 $N2 2>/dev/null
# et le même montage SANS bus, pour comparaison
$D "$M" --flux-serveur "$P2" --topologie "$T/t3.json" --region n2 --ctx 256 --threads 8 > "$T/n2b.log" 2>&1 & N2=$!
sleep 2
$D "$M" --flux-serveur "$P1" --topologie "$T/t3.json" --region n1 --ctx 256 --threads 8 > "$T/n1b.log" 2>&1 & N1=$!
sleep 3
R0=$($D "$M" --ppl-reparti "127.0.0.1:$P1" --topologie "$T/t3.json" --ids-file "$IDS" \
      --limit "$LIMITE" --ctx 256 --threads 8 --flux 2>&1 | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
kill $N1 $N2 2>/dev/null; wait $N1 $N2 2>/dev/null
echo "  relais sans bus : $R0 · relais avec bus gain=1.5 : $R"
[ -n "$R" ] && [ "$R" != "$R0" ] && echo "  ✅ le bus traverse les instances et agit sur la région du milieu" \
    || { echo "  ❌ le bus du nœud relais est sans effet"; exit 1; }
echo "=== 4. bus diffusé par FICHIER DE CONTRÔLE, sur un nœud RELAIS (C5bis) ==="
# Le canal voyage par un fichier relu avant chaque trame : un autre processus peut
# donc le changer PENDANT l'exécution — c'est ce qui en fait un bus.
P1=$((PORT + 1)); P2=$((PORT + 2))
cat > "$T/t3.json" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"n1","couches":[12,17],"instance":"127.0.0.1:$P1"},
  {"id":"n2","couches":[18,23],"instance":"127.0.0.1:$P2"}],
 "liens":[{"de":"local","vers":"n1","mode":"f32"},{"de":"n1","vers":"n2","mode":"f32"}]}
JSON
relais() { # relais <contenu du fichier de contrôle>
    printf '%s\n' "$1" > "$T/ctl.txt"
    $D "$M" --flux-serveur "$P2" --topologie "$T/t3.json" --region n2 --ctx 256 --threads 8 > "$T/n2.log" 2>&1 & local N2=$!
    sleep 2
    $D "$M" --flux-serveur "$P1" --topologie "$T/t3.json" --region n1 --bus-fichier "$T/ctl.txt" --ctx 256 --threads 8 > "$T/n1.log" 2>&1 & local N1=$!
    sleep 3
    local r
    r=$($D "$M" --ppl-reparti "127.0.0.1:$P1" --topologie "$T/t3.json" --ids-file "$IDS" \
        --limit "$LIMITE" --ctx 256 --threads 8 --flux 2>&1 | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
    kill $N1 $N2 2>/dev/null; wait $N1 $N2 2>/dev/null
    printf '%s' "$r"
}
R0=$(relais "# aucun canal"); R1=$(relais "MODULATION gain 1.5")
echo "  fichier sans canal : $R0 · canal gain=1,5 : $R1"
[ -n "$R1" ] && [ "$R1" != "$R0" ] && echo "  ✅ le canal diffusé par fichier change la région du milieu" \
    || { echo "  ❌ le fichier de contrôle est sans effet"; exit 1; }
rm -rf "$T"
