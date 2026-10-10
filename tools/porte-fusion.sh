#!/bin/bash
# porte-fusion.sh — la porte de la capacité C12bis : FUSIONNER les traces de
# plusieurs processus, et confronter les deux bouts de chaque lien.
#
# Ce que cette porte doit prouver, et pourquoi chaque cas existe :
#   1. une exécution répartie écrit DEUX traces (une par processus) — le nœud
#      n'en écrivait aucune, donc une divergence de lien n'était visible que d'un
#      bout, et on ne pouvait pas dire si c'est l'envoi ou la réception qui avait
#      dérivé ;
#   2. la fusion ORDONNE par le temps mural et CONFRONTE les deux bouts : en mode
#      dense, les empreintes doivent être identiques — le lien n'a rien changé ;
#   3. un seul bit changé dans la trace d'un nœud est DÉTECTÉ et attribué au lien
#      et au pas — sinon la fusion ne vérifie rien ;
#   4. une trace SANS horodatage (v1) est REFUSÉE au lieu d'être ordonnée par
#      numéro de pas : un ordre qui a l'air d'un ordre sans en être un.
# Une porte qui ne sait pas échouer ne vérifie rien : les cas 3 et 4 sont là pour ça.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
LIMITE=${LIMITE:-48}
PORT=${PORT:-$((52000 + RANDOM % 800))}
T=$(mktemp -d)
TOPO="$T/topo.json"
cat > "$TOPO" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"d","couches":[12,23],"instance":"127.0.0.1:$PORT"}],
 "liens":[{"de":"local","vers":"d","mode":"f32"}]}
JSON
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }

echo "=== 1. exécution répartie, trace des DEUX côtés ==="
$D "$M" --flux-serveur "$PORT" --topologie "$TOPO" --region d --ctx 256 --threads 8 \
   --trace-globale "$T/node.txt" > "$T/n.log" 2>&1 & N=$!
sleep 2
S=$($D "$M" --ppl-reparti "127.0.0.1:$PORT" --topologie "$TOPO" --ids-file "$IDS" \
     --limit "$LIMITE" --ctx 256 --threads 8 --flux f32 --trace-globale "$T/drv.txt" 2>&1)
CODE=$?
printf '%s\n' "$S" | grep -E "trace\]|deux nœuds" | sed 's/^/  /'
kill $N 2>/dev/null; wait $N 2>/dev/null
grep -E "trace\]" "$T/n.log" | sed 's/^/  nœud : /'
DL=$(grep -vc '^#' "$T/drv.txt" 2>/dev/null || echo 0)
NL=$(grep -vc '^#' "$T/node.txt" 2>/dev/null || echo 0)
echo "  croisements : pilote $DL · nœud $NL"
[ "$CODE" = 0 ] && [ "$DL" -gt 0 ] && [ "$NL" -gt 0 ] \
  || { echo "  ❌ le nœud n'a pas tracé (ou l'exécution a échoué, code $CODE)"; exit 1; }
grep -q "^# source d$" "$T/node.txt" \
  || { echo "  ❌ la trace du nœud ne porte pas sa région comme source"; exit 1; }

echo "=== 2. fusion : ordre par le temps mural + confrontation des liens ==="
F=$($D --fusionner-trace "$T/drv.txt" "$T/node.txt" --fusion-sortie "$T/fusion.txt" 2>&1)
FC=$?
printf '%s\n' "$F" | sed 's/^/  /'
[ "$FC" = 0 ] || { echo "  ❌ la fusion a échoué (code $FC)"; exit 1; }
printf '%s' "$F" | grep -q "0 divergents" \
  || { echo "  ❌ des liens divergent entre les deux bouts en mode dense"; exit 1; }
printf '%s' "$F" | grep -qE "[1-9][0-9]* identiques" \
  || { echo "  ❌ aucun lien n'a été confronté — la fusion ne vérifie rien"; exit 1; }
# L'ordre du fichier fusionné doit être celui du temps mural, sur toute la ligne.
python3 - "$T/fusion.txt" <<'PY' || exit 1
import sys
t = [float(l.split()[7]) for l in open(sys.argv[1]) if not l.startswith('#')]
assert t == sorted(t), "le fichier fusionné n'est pas ordonné par le temps mural"
print(f"  ✅ {len(t)} croisements fusionnés, ordonnés par le temps mural")
PY

echo "=== 3. un bit changé dans la trace du nœud ==="
python3 - "$T/node.txt" "$T/node_faux.txt" <<'PY'
import sys
lignes = open(sys.argv[1]).read().splitlines()
for i, l in enumerate(lignes):
    if l.startswith('d '):
        ch = l.split(); ch[4] = hex(int(ch[4], 16) ^ 1); lignes[i] = ' '.join(ch); break
open(sys.argv[2], 'w').write('\n'.join(lignes) + '\n')
PY
G=$($D --fusionner-trace "$T/drv.txt" "$T/node_faux.txt" 2>&1); GC=$?
printf '%s\n' "$G" | grep -E "DIVERGENT" | head -3 | sed 's/^/  /'
[ "$GC" = 3 ] || { echo "  ❌ un lien faux n'a pas fait sortir la fusion en erreur (code $GC)"; exit 1; }
printf '%s' "$G" | grep -q "local->pair pas" \
  || { echo "  ❌ la divergence n'est pas attribuée à son lien et à son pas"; exit 1; }
echo "  ✅ la divergence est détectée, attribuée (code 3)"

echo "=== 4. une trace sans horodatage est REFUSÉE, pas ordonnée au hasard ==="
grep -v '^#' "$T/node.txt" | awk '{print $1, $2, $3, $4, $5, $6}' > "$T/node_v1.txt"
V=$($D --fusionner-trace "$T/drv.txt" "$T/node_v1.txt" 2>&1); VC=$?
printf '%s\n' "$V" | head -2 | sed 's/^/  /'
[ "$VC" = 2 ] || { echo "  ❌ une trace v1 devrait être refusée (code $VC)"; exit 1; }
printf '%s' "$V" | grep -q "AUCUN horodatage" \
  || { echo "  ❌ le refus ne dit pas pourquoi"; exit 1; }
U=$($D --fusionner-trace "$T/drv.txt" 2>&1); UC=$?
[ "$UC" = 2 ] && echo "  ✅ v1 refusée (code 2), trace seule refusée (code 2)" \
  || { echo "  ❌ fusionner une seule trace devrait être refusé (code $UC)"; exit 1; }

echo "  trace fusionnée : $(grep -vc '^#' "$T/fusion.txt") lignes"
rm -rf "$T"
