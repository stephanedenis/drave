#!/bin/bash
# CHANTIER 3 — LA PORTE DE CORRECTION DU DÉCOUPAGE.
#
# Deux nœuds doivent donner EXACTEMENT ce que donne la passe monolithe. On
# coupe à la couche 13, donc on TRAVERSE la banque de la couche 12 : c'est le
# point où un découpage naïf se trompe, parce que le nœud 2 a besoin de l'entrée
# BRUTE empilée à la couche 12, pas seulement du flux.
#
#   A : couches 0..12   -> relais (flux + pile)
#   B : couches 13..25  <- relais A
#   C : couches 0..25   (monolithe)
#
# B et C doivent être IDENTIQUES AU BIT. Toute différence est un défaut du
# découpage, et le bit-à-bit ne laisse rien passer.
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
D=./drave-core/target/release/drave
K=/home/stephane/Data13TB/stephane/modeles/gguf/Kimi-K3-UD-Q4_K_XL/Kimi-K3-UD-Q4_K_XL-00001-of-00032.gguf
J=/tmp/test_plage.log
R=/tmp/plage_relais.bin
rm -f /tmp/pl_A-* /tmp/pl_B-* /tmp/pl_C-* "$R"
: > "$J"

echo "##### A : couches 0..12" | tee -a "$J"
DRAVE_K3_PASSE=93 DRAVE_DUMP_COUCHES=/tmp/pl_A DRAVE_K3_RELAIS_SORTIE="$R" \
    $D "$K" --k3-essai --couches 0:13 2>&1 | grep -E "plage|relais|passe " | tee -a "$J"

echo "" | tee -a "$J"
echo "##### B : couches 13..25, à partir du relais A" | tee -a "$J"
DRAVE_K3_PASSE=93 DRAVE_DUMP_COUCHES=/tmp/pl_B DRAVE_K3_RELAIS_ENTREE="$R" \
    $D "$K" --k3-essai --couches 13:26 2>&1 | grep -E "plage|relais|passe " | tee -a "$J"

echo "" | tee -a "$J"
echo "##### C : couches 0..25 (monolithe)" | tee -a "$J"
DRAVE_K3_PASSE=93 DRAVE_DUMP_COUCHES=/tmp/pl_C \
    $D "$K" --k3-essai --couches 0:26 2>&1 | grep -E "plage|passe " | tee -a "$J"

echo "" | tee -a "$J"
echo "##### COMPARAISON BIT À BIT (couche 25)" | tee -a "$J"
ok=1
for i in 0 1 2 3; do
    b=/tmp/pl_B-l_out-25-$i.bin; c=/tmp/pl_C-l_out-25-$i.bin
    if [ -f "$b" ] && [ -f "$c" ]; then
        if cmp -s "$b" "$c"; then
            echo "  jeton $i : IDENTIQUE ($(stat -c%s "$b") octets)" | tee -a "$J"
        else
            echo "  jeton $i : DIFFÉRENT — $(cmp "$b" "$c" 2>&1 | head -1)" | tee -a "$J"; ok=0
        fi
    else
        echo "  jeton $i : fichier manquant ($b / $c)" | tee -a "$J"; ok=0
    fi
done
[ $ok -eq 1 ] && echo "PORTE TENUE : le découpage ne change pas un bit" | tee -a "$J" \
              || echo "PORTE EN ÉCHEC" | tee -a "$J"
echo "=== fin ===" | tee -a "$J"
