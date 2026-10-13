#!/bin/bash
# porte-m5-brouillon.sh — M5/S1 : le brouillon est DANS le fichier, et il y reste.
#
# CE QU'ELLE VÉRIFIE AUJOURD'HUI (et qui est vert) : le GGUF de V4.1 **déclare** ses couches de
# brouillon et les **porte**. C'est le prérequis de M5 — « trouver un brouillon » n'est plus la
# question — et c'est une non-régression : un fichier remplacé, un GGUF re-téléchargé sans ces
# couches, et le décodage spéculatif redevient impossible **sans que rien ne le dise**.
# Fiche : `reports/rapport-v41-couches-brouillon.md`.
#
# CE QU'ELLE NE VÉRIFIE PAS ENCORE, ET QUI EST NOMMÉ ICI POUR NE PAS PASSER EN SILENCE : le chemin
# de décodage spéculatif du moteur. Les critères sont écrits (`docs/strata-pour-drave.md` § S1,
# « La porte ») et ils ne sont pas exécutables tant que le moteur n'exécute pas les couches 37-39 :
#   1. jeton **gourmand identique** au chemin sans brouillon sur N positions (la sortie ne change
#      pas, seule la vitesse change) ;
#   2. **taux d'acceptation** par type de tâche ;
#   3. et la porte doit être vue **ROUGE** avec un brouillon volontairement désaligné — sans quoi
#      elle ne vérifie rien (`REPRISE.md` § 4, règle 1).
# Le jour où ce chemin existe, ces trois points deviennent des sections de CE fichier.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-$HOME/IA/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf}

if [ ! -s "$M" ]; then
    echo "  (modèle absent : $M — prérequis non vérifiable ici)"
    exit 0
fi

# 1. la config embarquée déclare le brouillon
cfg=$(python3 tools/lire_meta_gguf.py "$M" deepseek41.config 2>/dev/null | grep -oE '"dspark_target_layer_ids":\[[0-9,]*\]|"num_nextn_predict_layers":[0-9]+')
cibles=$(printf '%s' "$cfg" | grep -oE '\[[0-9,]*\]')
couches=$(printf '%s' "$cfg" | grep -oE '"num_nextn_predict_layers":[0-9]+' | grep -oE '[0-9]+$')
if [ "$cibles" != "[37,38,39]" ] || [ "${couches:-0}" != "3" ]; then
    echo "  ❌ le fichier ne déclare plus ses 3 couches de brouillon (cibles=$cibles, n=$couches)"
    exit 1
fi

# 2. les tenseurs sont là — 25 par couche, 75 en tout
n=$($D "$M" --tensors 2>/dev/null | grep -cE "blk\.(37|38|39)\.")
if [ "$n" != "75" ]; then
    echo "  ❌ 75 tenseurs attendus pour blk.37-39, $n trouvés"
    exit 1
fi

echo "  ✅ brouillon déclaré (cibles $cibles) et porté : $n tenseurs, 41 263 M poids"
echo "     (le chemin spéculatif du moteur reste à faire — critères dans docs/strata-pour-drave.md § S1)"
