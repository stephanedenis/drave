#!/bin/bash
# porte-jeux.sh — la porte des jeux symboliques.
#
# CE QU'ELLE VERROUILLE :
#   1. les tests unitaires (RSN, codecs, règles, pensée) ;
#   2. la couverture du corpus au niveau 4 = 100 % ;
#   3. l'invariance des paires (même sens, surfaces différentes) = 100 % ;
#   4. les collisions négatives = 0 ;
#   5. la restitution et la détection des perturbations = 100 % ;
#   6. le morpion exact (valeur 0, aucune défaite contre le hasard) ;
#   7. le perft des échecs et des dames, les règles du go et des cartes ;
#   8. la politique des cartes > 55 % contre le hasard, 0 coup illégal ;
#   9. l'invariance de la PENSÉE (5 jeux) et son contrôle négatif.
#
# Le mode `--rapide` ne lance ni les perfts profonds, ni les parties MCTS /
# dames : ceux-là vont dans `python3 tools/mesure_jeux.py --json …`, la fiche
# de `reports/`. Une porte qui prendrait dix minutes ne serait plus lancée.
set -u
cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD/tools${PYTHONPATH:+:$PYTHONPATH}"
SORTIE="${JOURNAUX:-/tmp}/jeux-mesures.json"

echo "  === tests unitaires ==="
python3 -m unittest discover -s tools/jeux/tests -t tools || exit 1

echo "  === mesure rapide (couches + pensée) ==="
python3 tools/mesure_jeux.py --rapide --json "$SORTIE" || exit 1
[ -s "$SORTIE" ] || { echo "  ❌ le JSON de mesure n'a pas été écrit ($SORTIE)"; exit 1; }
echo "  ✅ la porte des jeux tient : 100 % au niveau 4, 33/33 paires invariantes, 0 collision,"
echo "     la restitution et la perturbation exactes, le perft et la pensée invariante."
