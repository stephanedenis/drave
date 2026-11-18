#!/bin/bash
# porte-a2.6-experts.sh — la règle de placement des experts : bande, coût, refus, trace.
#
# POURQUOI CETTE PORTE EXISTE. La reconnaissance A2.6 (18/11) a montré qu'**aucune
# porte ne mesurait le placement des experts** : la règle pouvait être fausse sans
# qu'une seule rougisse. Le 18/11, `placement.rs` a reçu la bande mesurée (7,0 Go/s
# par lecteur, saturation à 8), le coût, le refus nommé et la trace, avec 5 tests.
# Cette porte les nomme un par un : un test renommé ou supprimé rougit ici.
#
# Ce qu'elle ne vérifie pas : que la règle soit BRANCHÉE dans `model.rs` (elle ne
# l'est pas encore — c'est la tâche A2.6 suivante) ; elle vérifie que la règle
# existe, qu'elle reproduit la mesure et qu'elle refuse en le disant.
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE A2.6 — LA RÈGLE DES EXPERTS ==="
SORTIE=$(cd drave-core && cargo test --release placement 2>&1)
CODE=$?
echo "$SORTIE" | grep -E "^test result" | tail -1
if [ "$CODE" -ne 0 ]; then
    echo "$SORTIE" | tail -5
    echo "  ❌ cargo test placement en échec (code $CODE)"
    exit 1
fi
for t in la_bande_des_experts_reproduit_les_mesures \
         le_cout_des_experts_reproduit_la_mesure \
         le_refus_des_experts_est_nomme \
         les_experts_tiennent_en_vram_quand_elle_est_libre \
         la_trace_des_experts_dit_les_chiffres; do
    if ! echo "$SORTIE" | grep -q "placement::tests::$t ... ok"; then
        echo "  ❌ test manquant ou en échec : $t"
        exit 1
    fi
done
echo "  ✅ bande 4,93/6,99 Go/s · coût 156,9 ms pour 1,097 Go/jeton · refus nommé · trace"
exit 0
