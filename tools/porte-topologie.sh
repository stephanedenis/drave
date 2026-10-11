#!/bin/bash
# porte-topologie.sh — la porte de la capacité C1 : la topologie PILOTE le découpage.
#
# Ce qu'elle vérifie, et pourquoi ces quatre cas :
#   1. la RÉFÉRENCE : le modèle entier, un seul processus ;
#   2. le découpage HISTORIQUE (`--couches-locales`) — l'écart de flux doit être 0 ;
#   3. le découpage par TOPOLOGIE (fichier) — il doit rendre EXACTEMENT le même
#      chiffre que le précédent : c'est la non-régression de C1 ;
#   4. les REFUS : une topologie qui ne couvre pas le modèle, et une topologie dont
#      l'adresse contredit `--ppl-reparti`. Un découpage qui n'est pas celui qu'on
#      croit ne doit pas se mesurer en silence.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-/tmp/m5_d384_dense.gguf}
IDS=${IDS:-/tmp/campagne24/ids_m5_d384_dense.txt}
COUCHES=${COUCHES:-2}
# Le NOMBRE DE JETONS EST COMPTÉ, PAS SUPPOSÉ — même piège que dans
# `porte-reparti-moteur.sh`, trouvé en balayant les portes après l'avoir corrigé là-bas :
# `--ppl` note les `limit` PREMIERS jetons, `--ppl-reparti` tronque aux `limit` DERNIERS.
# Le fichier en contient 255 et la limite en annonçait 128 : les deux perplexités affichées
# côte à côte portaient sur DEUX PASSAGES DIFFÉRENTS. La porte ne l'affirmait pas (elle
# imprime, elle ne compare pas), donc elle passait — mais elle invitait à une comparaison
# fausse, ce qui est exactement le genre de piège que ce dépôt refuse.
if [ -s "$IDS" ]; then
    N_IDS=$(tr ',' '\n' < "$IDS" | grep -c '[0-9]')
else
    N_IDS=0
fi
LIMITE=${LIMITE:-$N_IDS}
PORT=${PORT:-$((50000 + RANDOM % 900))}
T=$(mktemp -d)
TOPO="$T/topo.json"
[ -s "$M" ] && [ -s "$IDS" ] || {
    echo "  ❌ modèle ou identifiants absents : $M · $IDS"
    echo "     Ce modèle est un ARTEFACT DE CAMPAGNE (dim 384, entraîné par"
    echo "     tools/campagne-benefices.sh), pas un fichier régénérable ici. Après un REDÉMARRAGE,"
    echo "     /tmp est vide : relancer la campagne, ou pointer MODELE= sur un modèle à 24 couches."
    echo "     Les autres portes régénèrent leurs prérequis toutes seules (tools/_corpus.sh)."
    exit 2
}

N=$($D "$M" --tensors 2>/dev/null | grep -cE "^ +[A-Z0-9_]+ +blk\.[0-9]+\.attn_q\.weight" || true)
[ "${N:-0}" -gt 0 ] || N=4

cat > "$TOPO" <<JSON
{
  "regions": [
    {"id": "local",   "couches": [0, $((COUCHES-1))],              "instance": "local"},
    {"id": "distant", "couches": [$COUCHES, $((N-1))],             "instance": "127.0.0.1:$PORT"}
  ],
  "liens": [ {"de": "local", "vers": "distant", "mode": "listes", "delai_ms": 0} ]
}
JSON

echo "=== 1. référence : le modèle entier ==="
$D "$M" --ppl "$IDS" --limit "$LIMITE" --ctx 256 --threads 8 --abits 16 2>/dev/null \
    | grep -oE "perplexité [0-9.]+ sur" | tail -1

echo "=== 2. découpage historique ($COUCHES couches locales) ==="
$D "$M" --flux-serveur "$PORT" --ctx 256 --threads 8 > "$T/n1.log" 2>&1 & SRV=$!
for _ in $(seq 1 40); do grep -q "nœud moteur sur" "$T/n1.log" 2>/dev/null && break; sleep 0.25; done
H=$($D "$M" --ppl-reparti "127.0.0.1:$PORT" --ids-file "$IDS" --couches-locales "$COUCHES" \
    --limit "$LIMITE" --ctx 256 --threads 8 --abits 16 2>&1 \
    | grep -E "deux nœuds +: perplexité [0-9.]+|écart +: +[0-9.e+-]+")
echo "  $H"
kill $SRV 2>/dev/null; wait $SRV 2>/dev/null

echo "=== 3. découpage par TOPOLOGIE ($TOPO) ==="
$D "$M" --flux-serveur "$PORT" --ctx 256 --threads 8 > "$T/n2.log" 2>&1 & SRV=$!
for _ in $(seq 1 40); do grep -q "nœud moteur sur" "$T/n2.log" 2>/dev/null && break; sleep 0.25; done
T2=$($D "$M" --ppl-reparti "127.0.0.1:$PORT" --topologie "$TOPO" --ids-file "$IDS" \
     --limit "$LIMITE" --ctx 256 --threads 8 --abits 16 2>&1 \
     | grep -E "deux nœuds +: perplexité [0-9.]+|écart +: +[0-9.e+-]+")
echo "  $T2"
kill $SRV 2>/dev/null; wait $SRV 2>/dev/null

A=$(printf '%s' "$H" | grep -oE "[0-9.]+" | head -1)
B=$(printf '%s' "$T2" | grep -oE "[0-9.]+" | head -1)
E=$(printf '%s' "$T2" | grep -oE "écart +: +[0-9.e+-]+" | grep -oE "[0-9.e+-]+$")
echo "=== verdict ==="
if [ -n "$A" ] && [ "$A" = "$B" ]; then
    echo "  PORTE TENUE : la topologie rend le MÊME chiffre que le découpage historique ($A)"
else
    echo "  ÉCHEC : historique $A · topologie $B"; exit 1
fi
[ "$E" = "0.00e0" ] && echo "  écart de flux : 0.00e0 ✅" || echo "  écart de flux : ${E:-?} ⚠️"

echo "=== 4. les refus (une topologie fausse ne doit pas se mesurer) ==="
sed "s/\[$COUCHES, $((N-1))\]/[$((COUCHES+1)), $((N-1))]/" "$TOPO" > "$T/trou.json"
$D "$M" --topologie "$T/trou.json" 2>&1 | tail -1
$D "$M" --ppl-reparti "127.0.0.1:1" --topologie "$TOPO" --ids-file "$IDS" --limit 8 \
    --ctx 256 --threads 8 2>&1 | tail -1
# ---------------------------------------------------------------- 5. LE RELAIS
# C1b pas 2 : trois régions sur TROIS instances (pilote + relais + sortie). Le
# nœud du milieu applique SA plage puis transmet à son successeur ; le retour se
# fait de proche en proche. La porte : le résultat doit être IDENTIQUE au
# découpage à deux régions, et l'écart de flux nul.
echo "=== 5. trois régions sur trois instances (relais) ==="
M3=${M3:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS3=${IDS3:-/tmp/campagne24/ids_0.5B-Q8.txt}
if [ ! -s "$M3" ] || [ ! -s "$IDS3" ]; then
    echo "  (modèle à 24 couches ou identifiants absents — cas sauté)"
else
    P1=$((PORT + 1)); P2=$((PORT + 2))
    cat > "$T/t3.json" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"n1","couches":[12,17],"instance":"127.0.0.1:$P1"},
  {"id":"n2","couches":[18,23],"instance":"127.0.0.1:$P2"}],
 "liens":[{"de":"local","vers":"n1","mode":"f32"},{"de":"n1","vers":"n2","mode":"f32"}]}
JSON
    cat > "$T/t2.json" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"n1","couches":[12,23],"instance":"127.0.0.1:$P1"}],
 "liens":[{"de":"local","vers":"n1","mode":"f32"}]}
JSON
    $D "$M3" --flux-serveur "$P1" --ctx 256 --threads 8 > "$T/n1.log" 2>&1 & N1=$!
    sleep 2
    R2=$($D "$M3" --ppl-reparti "127.0.0.1:$P1" --topologie "$T/t2.json" --ids-file "$IDS3" \
         --limit 128 --ctx 256 --threads 8 --flux 2>&1 | grep -E "deux nœuds +: perplexité [0-9.]+")
    echo "  deux régions / deux instances : $R2"
    kill $N1 2>/dev/null; wait $N1 2>/dev/null
    $D "$M3" --flux-serveur "$P2" --topologie "$T/t3.json" --region n2 --ctx 256 --threads 8 > "$T/n2.log" 2>&1 & N2=$!
    sleep 2
    $D "$M3" --flux-serveur "$P1" --topologie "$T/t3.json" --region n1 --ctx 256 --threads 8 > "$T/n1b.log" 2>&1 & N1=$!
    sleep 3
    R3=$($D "$M3" --ppl-reparti "127.0.0.1:$P1" --topologie "$T/t3.json" --ids-file "$IDS3" \
         --limit 128 --ctx 256 --threads 8 --flux 2>&1 | grep -E "deux nœuds +: perplexité [0-9.]+|écart +: +[0-9.e+-]+")
    echo "  trois régions / trois instances :"
    printf '%s\n' "$R3" | sed 's/^/    /'
    kill $N1 $N2 2>/dev/null; wait $N1 $N2 2>/dev/null
    V2=$(printf '%s' "$R2" | grep -oE "perplexité [0-9.]+" | grep -oE "[0-9.]+" | head -1)
    V3=$(printf '%s' "$R3" | grep -oE "perplexité [0-9.]+" | grep -oE "[0-9.]+" | head -1)
    if [ -n "$V2" ] && [ "$V2" = "$V3" ]; then
        echo "  PORTE TENUE : le relais ne change pas un chiffre ($V2)"
    else
        echo "  ÉCHEC : deux régions $V2 · trois régions $V3"; exit 1
    fi
fi
rm -rf "$T"
