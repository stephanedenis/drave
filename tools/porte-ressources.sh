#!/bin/bash
# porte-ressources.sh — le registre des ressources tient : autotest et cohérence.
#
# POURQUOI CETTE PORTE EXISTE. Le registre `tools/ressources.py` est consultatif : il n'empêche
# pas un job de tourner, il rend le conflit visible. Une porte doit vérifier ce qui est
# vérifiable sans la machine : le code du registre (autotest des 9 cas : claim, conflit, file,
# admission, check) et la cohérence du registre courant (aucune ressource sur-réservée).
#
# CE QU'ELLE NE VÉRIFIE PAS : le réel (processus GPU non déclarés, charge CPU, espace disque) —
# c'est `--actual`, informatif, et le mapping processus→claim reste manuel. Les avertissements
# de stockage (RAID à 33 Gio) et de NUMA (un GPU avec des fils sur cpu1) restent VISIBLES mais
# ne font pas échouer la porte : ce sont des limites nommées, pas des régressions.
#
# Usage : tools/porte-ressources.sh
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE RESSOURCES — REGISTRE, CLAIMS, COHÉRENCE ==="
if ! python3 tools/ressources.py --autotest; then
    echo "  ❌ autotest du registre en échec"
    exit 1
fi
if ! python3 tools/ressources.py --check; then
    echo "  ❌ registre incohérent : une ressource est sur-réservée"
    exit 1
fi
echo "  ✅ registre cohérent ; les avertissements de stockage/NUMA sont affichés, pas fatals"
echo "✅ porte ressources verte : autotest 9 cas et registre cohérent"
exit 0
