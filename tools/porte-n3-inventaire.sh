#!/bin/bash
# porte-n3-inventaire.sh — la couverture N3, vérifiée à chaque passe.
#
# POURQUOI CETTE PORTE EXISTE. Les 17 portes `porte-n3-*` prouvent chacune une
# brique, mais **rien** ne prouvait que la liste des briques et celle des portes
# coïncident encore. N3.1 (29/10) affirmait « sortie précoce : service non » et
# « k-WTA/routes : aucune porte » ; N3.2b0 et N3.3a l'ont refutée le même jour ;
# six jours plus tard la fiche de backlog disait toujours « ⏳ une porte par
# brique ». Un inventaire écrit à la main pourrit en silence — c'est le défaut
# d'une porte qu'on croit verte sans l'avoir lancée, appliqué à la documentation.
#
# Ce que cette porte verrouille (statique, aucun run, ~1 s) :
#   1. chaque porte N3 est citée par une fiche et chaque porte citée existe ;
#   2. chaque JSON N3 est cité par une fiche et chaque JSON cité existe ;
#   3. les portes passent `bash -n` ;
#   4. les seuils de couverture ne baissent pas (18 portes, 21 fiches, 20 JSON).
# Le contrôle négatif est l'autotest de l'outil : retirer une porte, ajouter une
# porte orpheline, retirer un JSON ou en ajouter un orphelin doit ÉCHOUER.
set -u
cd "$(dirname "$0")/.."
echo "=== l'inventaire N3 : la couverture ne peut pas pourrir en silence ==="
python3 tools/n3_inventaire.py --autotest || { echo "  ❌ le vérificateur ne sait pas échouer"; exit 1; }
python3 tools/n3_inventaire.py || exit 1
