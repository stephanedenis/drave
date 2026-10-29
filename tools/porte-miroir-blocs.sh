#!/bin/bash
# porte-miroir-blocs.sh — le miroir entrée/sortie des trois blocs structurels.
#
# POURQUOI CETTE PORTE EXISTE. La règle du dépôt est que toute mesure d'entrée se double
# d'une mesure de SORTIE : un lecteur qui ne sait pas restituer ce qu'il a lu n'a pas lu,
# il a filtré. R4.1, R4.2 et R4.3 mesuraient l'entrée (grille, AST, valeur) ; cette porte
# exige la sortie : rendre, relire, retrouver le MÊME objet.
#
#   R4.1 — la grille rendue en Markdown/CSV, relue : 34/34.
#   R4.2 — le module rendu par `ast.unparse`, relu : 296/296.
#   R4.3 — la formule (et sa dérivée) rendue en LaTeX, relue : 42/42.
#
# Et pour chacun, un contrôle négatif : le texte plat pour la grille, la source aplatie
# pour le code, la formule sans parenthèses pour les maths — doivent ÉCHOUER.
#
# Ce qu'elle ne vérifie PAS : les fusions de tableau (Markdown/CSV ne les expriment pas,
# comptées à part) ; la fidélité au caractère près (le miroir compare le SENS : textes de
# cellules, forme de l'AST).
#
# Usage : tools/porte-miroir-blocs.sh
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE MIROIR — LES TROIS BLOCS ==="
ECHEC=0
for bloc in tableaux code maths; do
  if python3 "tools/bloc_${bloc}.py" --miroir > "/tmp/miroir-${bloc}.json"; then
    if ! python3 - "$bloc" "/tmp/miroir-${bloc}.json" <<'PY'
import json, sys
bloc, chemin = sys.argv[1], sys.argv[2]
d = json.load(open(chemin, encoding="utf-8"))
print(f"  {bloc:10s} {d['justes']}/{d['total']} exacts · contrôle négatif "
      f"{'perdu (bien)' if d['negatif_perd'] else 'NON PERDU'}")
PY
    then
      echo "  ${bloc:10s} ❌ restitution illisible"
      ECHEC=1
    fi
  else
    echo "  ${bloc:10s} ❌ échec"
    ECHEC=1
  fi
done
if [ "$ECHEC" = 0 ]; then
  echo "✅ porte miroir verte"
else
  echo "❌ porte miroir ROUGE"
fi
exit "$ECHEC"
