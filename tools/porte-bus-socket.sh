#!/bin/bash
# porte-bus-socket.sh — la porte de la capacité C5ter : le bus par le RÉSEAU.
#
# POURQUOI CETTE PORTE EXISTE. C5bis diffusait un réglage par un FICHIER relu à
# chaque pas — donc il fallait un système de fichiers partagé, c'est-à-dire pas deux
# machines. Un bus qui n'atteint pas la deuxième machine n'est pas un bus distribué.
#
# CE QU'ELLE PROUVE, ET COMMENT ELLE LE PROUVE SANS AMBIGUÏTÉ DE TEMPS.
# La difficulté d'un bus, c'est que « quand la ligne arrive » décide de ce qu'elle
# affecte. La porte ne s'appuie donc PAS sur une course : la ligne est envoyée au
# nœud AVANT que le pilote ne se connecte, et le nœud n'accepte la connexion
# qu'après. L'ordre est alors garanti par la porte elle-même, pas par un `sleep`
# chanceux :
#
#   1. référence, aucun bus ;
#   2. bus STATIQUE sur le nœud (`--bus gain=2.0`) → la référence du réglage ;
#   3. bus par SOCKET, ligne envoyée avant la connexion du pilote → doit être
#      ÉGAL AU BIT PRÈS au cas 2 : c'est le même bus, pas un cousin ;
#   4. ligne NEUTRE par socket → doit être ÉGAL AU BIT PRÈS au cas 1 : le chemin
#      réseau ne perturbe rien (un canal neutre ne change rien — l'invariant de C5) ;
#   5. ligne envoyée EN PLEIN VOL → doit différer des cas 1 et 2 : un bus qui ne
#      peut moduler qu'au démarrage est un fichier de configuration, pas un bus.
#
# Les cas 3 et 4 sont des ÉGALITÉS EXACTES (0,00e0), pas des tolérances.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
. tools/_corpus.sh    # régénère le corpus si /tmp a été effacé (redémarrage)
LIMITE=${LIMITE:-48}
PORT=${PORT:-$((53000 + RANDOM % 500))}
BPORT=${BPORT:-$((54000 + RANDOM % 500))}
T=$(mktemp -d)
P1=${P1:-$PORT}
P2=${P2:-$((PORT + 1))}
TOPO="$T/topo.json"
# TROIS régions, et ce n'est pas un détail : le gain de la région FINALE est absorbé
# par la normalisation de sortie (une norme divise par la norme, donc un facteur
# scalaire y disparaît — mesuré : 113,0068 avec et sans gain=2,0 sur `d`). Un nœud du
# MILIEU, lui, alimente une autre région : sa sortie n'est pas normalisée avant, et
# le gain y est visible. C'est le piège documenté de C5, retombé dedans ici même.
cat > "$TOPO" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"n1","couches":[12,17],"instance":"127.0.0.1:$P1"},
  {"id":"n2","couches":[18,23],"instance":"127.0.0.1:$P2"}],
 "liens":[{"de":"local","vers":"n1","mode":"f32"},{"de":"n1","vers":"n2","mode":"f32"}]}
JSON
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }

# Envoie une ligne de modulation et rend la réponse du bus. Échoue bruyamment si le
# bus n'a pas répondu : un bus muet doit se voir tout de suite.
moduler() { # $1 = ligne, $2 = port
  python3 - "$1" "$2" <<'PY'
import socket, sys
ligne, port = sys.argv[1], int(sys.argv[2])
s = socket.create_connection(("127.0.0.1", port), timeout=5)
s.sendall((ligne + "\n").encode())
rep = s.makefile().readline().strip()
s.close()
print(rep)
sys.exit(0 if rep.startswith("OK") else 1)
PY
}

# n2 (dernière région) est TOUJOURS sans bus : c'est n1, le relais du milieu, qu'on
# module. `$1` = port du bus (vide = aucun), `$2` = nom du journal, reste = drapeaux.
PIDS=()
nœuds() { # $1 = port bus n1 (vide = aucun), $2 = étiquette, $3.. = drapeaux de n1
  local bp="$1"; shift; local etq="$1"; shift
  $D "$M" --flux-serveur "$P2" --topologie "$TOPO" --region n2 --ctx 256 --threads 8 \
     > "$T/log_${etq}_n2.txt" 2>&1 & PIDS+=($!)
  sleep 2
  local args=()
  [ -n "$bp" ] && args+=(--bus-serveur "$bp")
  $D "$M" --flux-serveur "$P1" --topologie "$TOPO" --region n1 --ctx 256 --threads 8 \
     "${args[@]}" "$@" > "$T/log_${etq}_n1.txt" 2>&1 & PIDS+=($!)
  sleep 2
}
arrêter() { for p in "${PIDS[@]}"; do kill "$p" 2>/dev/null; done
            for p in "${PIDS[@]}"; do wait "$p" 2>/dev/null; done; PIDS=(); }
pilote() {
  $D "$M" --ppl-reparti "127.0.0.1:$P1" --topologie "$TOPO" --ids-file "$IDS" \
     --limit "$LIMITE" --ctx 256 --threads 8 --flux f32 2>&1
}
ppl() { printf '%s\n' "$1" | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$"; }

echo "=== 1. référence : aucun bus ==="
nœuds "" ref
R=$(pilote); REF=$(ppl "$R")
arrêter
echo "  perplexité de référence : $REF"

echo "=== 2. bus STATIQUE sur le nœud (--bus gain=2.0) ==="
nœuds "" stat --bus gain=2.0
S=$(pilote); STAT=$(ppl "$S")
arrêter
grep -E "bus\]" "$T/log_stat_n1.txt" | tail -1 | sed 's/^/  /'
echo "  perplexité avec gain statique : $STAT"
[ "$STAT" != "$REF" ] || { echo "  ❌ le gain statique ne change RIEN — le bus n'est pas branché"; exit 1; }

echo "=== 3. bus par SOCKET, ligne envoyée avant la connexion du pilote ==="
nœuds "$BPORT" sock
REP=$(moduler "MODULATION gain 2.0" "$BPORT") || { echo "  ❌ le bus n'a pas répondu"; arrêter; exit 1; }
echo "  bus : $REP"
Q=$(pilote); DYN=$(ppl "$Q")
arrêter
echo "  perplexité par socket : $DYN"
python3 -c "
import sys
a, b = float('$DYN'), float('$STAT')
e = abs(a - b)
print(f'  écart socket / statique : {e:.6e}')
sys.exit(0 if e == 0.0 else 1)" \
  || { echo "  ❌ le bus par socket NE VAUT PAS le bus statique (le même réglage doit donner le même calcul)"; exit 1; }
echo "  ✅ identique au bit près (0,00e0)"
grep -q "reçu par le réseau" "$T/log_sock_n1.txt" || { echo "  ❌ le bus n'a pas appliqué la ligne"; exit 1; }

echo "=== 4. ligne NEUTRE par socket : rien ne doit changer ==="
B2=$((BPORT + 1))
nœuds "$B2" neutre
REP=$(moduler "MODULATION gain 1.0" "$B2") || { echo "  ❌ le bus n'a pas répondu"; arrêter; exit 1; }
echo "  bus : $REP"
V=$(pilote); NEUT=$(ppl "$V")
arrêter
python3 -c "
import sys
a, b = float('$NEUT'), float('$REF')
print(f'  écart neutre / référence : {abs(a-b):.6e}')
sys.exit(0 if a == b else 1)" \
  || { echo "  ❌ le chemin réseau perturbe le calcul (canal neutre)"; exit 1; }
echo "  ✅ identique au bit près (0,00e0)"

echo "=== 5. ligne envoyée EN PLEIN VOL ==="
# POURQUOI UNE EXÉCUTION PLUS LONGUE ICI. Le pilote met ~0,6 s à charger le modèle
# AVANT sa première connexion : moduler à 0,6 s arrivait donc encore avant le pas 0,
# et la porte mesurait — sans le voir — le cas 3 une deuxième fois (constaté : la
# modulation « en plein vol » valait exactement le réglage dès le pas 0). Le run est
# donc allongé à 256 pas (~8 s) et la ligne part à 3 s, franchement au milieu.
LIM_VOL=${LIM_VOL:-256}
B3=$((BPORT + 2))
nœuds "$B3" vol
$D "$M" --ppl-reparti "127.0.0.1:$P1" --topologie "$TOPO" --ids-file "$IDS" \
   --limit "$LIM_VOL" --ctx 256 --threads 8 --flux f32 > "$T/vol.txt" 2>&1 &
PID=$!
sleep 3
REP=$(moduler "MODULATION gain 2.0" "$B3") && echo "  bus : $REP (pendant que le pilote calcule)"
wait $PID 2>/dev/null
VOL=$(ppl "$(cat "$T/vol.txt")")
grep -E "deux nœuds" "$T/vol.txt" | sed 's/^/  /'
arrêter
echo "  perplexité modulée en plein vol : $VOL  (référence $REF · dès le pas 0 $STAT)"
grep -q "reçu par le réseau" "$T/log_vol_n1.txt" || { echo "  ❌ le nœud n'a pas appliqué la ligne"; exit 1; }
python3 -c "
import sys
v, r, s = float('$VOL'), float('$REF'), float('$STAT')
if v == r: sys.exit('  ❌ la modulation en plein vol n\'a rien changé')
if v == s: sys.exit('  ❌ la modulation a valu un réglage appliqué dès le pas 0 — elle est arrivée trop tard ou trop tôt pour être « en vol »')
print(f'  ✅ en plein vol : ni la référence ({r}), ni le réglage dès le pas 0 ({s})')" || exit 1

echo "=== 6. le bus du PILOTE : neutre par socket, inerte AU BIT PRÈS ==="
# Le bus du pilote s'ouvre au démarrage, si bien qu'on ne peut pas garantir
# l'instant d'arrivée d'une ligne. Mais une ligne NEUTRE n'a pas besoin d'instant :
# appliquée à n'importe quel pas, elle ne change rien. C'est donc un cas exact sans
# course — et il prouve du même coup que le serveur du pilote répond et valide.
B4=$((BPORT + 3))
nœuds "" pilbus
$D "$M" --ppl-reparti "127.0.0.1:$P1" --topologie "$TOPO" --ids-file "$IDS" \
   --limit "$LIMITE" --ctx 256 --threads 8 --flux f32 --bus-serveur "$B4" \
   > "$T/pilbus.txt" 2>&1 & PID=$!
sleep 1.2
REP=$(moduler "MODULATION gain 1.0" "$B4") && echo "  bus du pilote : $REP"
wait $PID 2>/dev/null
PIL=$(ppl "$(cat "$T/pilbus.txt")")
arrêter
python3 -c "
import sys
a, b = float('$PIL'), float('$REF')
print(f'  neutre côté pilote / référence : {abs(a-b):.6e}')
sys.exit(0 if a == b else 1)" \
  || { echo "  ❌ le bus du pilote perturbe le calcul (canal neutre)"; exit 1; }
echo "  ✅ identique au bit près (0,00e0)"

echo "=== 7. le bus du PILOTE branché : une ligne non neutre change le résultat ==="
B5=$((BPORT + 4))
nœuds "" pilbus2
$D "$M" --ppl-reparti "127.0.0.1:$P1" --topologie "$TOPO" --ids-file "$IDS" \
   --limit "$LIMITE" --ctx 256 --threads 8 --flux f32 --bus-serveur "$B5" \
   > "$T/pilbus2.txt" 2>&1 & PID=$!
sleep 1.2
REP=$(moduler "MODULATION gain 2.0" "$B5") && echo "  bus du pilote : $REP"
wait $PID 2>/dev/null
PIL2=$(ppl "$(cat "$T/pilbus2.txt")")
arrêter
echo "  perplexité avec le bus du pilote modulé : $PIL2 (référence $REF)"
python3 -c "
import sys
r, p = float('$REF'), float('$PIL2')
# Un sys.exit AVEC un message sort TOUJOURS en code 1 : la branche de succès
# passait un message, donc la porte rendait 1 en ayant tout réussi. Et pas
# d'apostrophe inversée ici : dans une chaîne bash entre guillemets, elle lance
# une substitution de commande (attrapé au premier essai).
if p == r:
    sys.exit('  ❌ le bus du pilote est branché nulle part')
print(f'  ✅ le bus du pilote agit ({r} -> {p})')" || exit 1

rm -rf "$T"
