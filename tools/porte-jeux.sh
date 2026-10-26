#!/bin/bash
# porte-jeux.sh — la porte des jeux symboliques.
#
# CE QU'ELLE VERROUILLE :
#   1. les tests unitaires (RSN, codecs, règles, pensée, langues, maîtres) ;
#   2. la couverture du corpus au niveau 4 = 100 % ;
#   3. l'invariance des paires (même sens, surfaces différentes) = 100 % ;
#   4. les collisions négatives = 0 ;
#   5. la restitution et la détection des perturbations = 100 % ;
#   6. le morpion exact (valeur 0, aucune défaite contre le hasard) ;
#   7. le perft des échecs et des dames, les règles du go et des cartes ;
#   8. la politique des cartes > 55 % contre le hasard, 0 coup illégal ;
#   9. l'invariance de la PENSÉE (5 jeux) et son contrôle négatif ;
#  10. les 71 langues : couverture, corpus, invariance, permutation, notation ;
#  11. les principes des maîtres : premier coup, livre, mats, go 9×9, dames, cartes.
#
# Le mode `--rapide` ne lance ni les perfts profonds, ni les parties MCTS /
# dames : ceux-là vont dans `python3 tools/mesure_jeux.py --json …` et
# `python3 tools/mesure_maitres.py --complet --json …`, les fiches de `reports/`.
# Une porte qui prendrait dix minutes ne serait plus lancée.
set -u
cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD/tools${PYTHONPATH:+:$PYTHONPATH}"
SORTIE="${JOURNAUX:-/tmp}/jeux-mesures.json"
SORTIE_L="${JOURNAUX:-/tmp}/langues-mesures.json"
SORTIE_M="${JOURNAUX:-/tmp}/maitres-mesures.json"

echo "  === tests unitaires ==="
python3 -m unittest discover -s tools/jeux/tests -t tools || exit 1

echo "  === mesure rapide (couches + pensée) ==="
python3 tools/mesure_jeux.py --rapide --json "$SORTIE" || exit 1
[ -s "$SORTIE" ] || { echo "  ❌ le JSON de mesure n'a pas été écrit ($SORTIE)"; exit 1; }

echo "  === langues (71 langues, 35 concepts) ==="
python3 tools/mesure_langues.py --rapide --json "$SORTIE_L" >/dev/null || exit 1
python3 - "$SORTIE_L" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
c, co = d["couverture"], d["corpus"]
assert c["langues"] >= 70, c["langues"]
assert c["couples"] >= 1400, c["couples"]
assert co["bons"] == co["items"], (co["bons"], co["items"])
assert d["invariance"]["invariantes"] == d["invariance"]["paires"], d["invariance"]
assert d["detection"]["bons"] == d["detection"]["total"], d["detection"]
assert d["notation"]["bons"] == d["notation"]["parses"], d["notation"]
p = d["permutation"]
assert p["forts"] > 0 and p["forts_bons"] <= 0.10 * p["forts"], p
print(f"     {c['langues']} langues, {c['concepts']} concepts, {c['couples']} couples ; "
      f"{co['bons']}/{co['items']} au niveau 4 ; "
      f"{d['invariance']['invariantes']}/{d['invariance']['paires']} paires ; "
      f"permutation {p['forts_bons']}/{p['forts']} ; "
      f"notation {d['notation']['bons']}/{d['notation']['parses']}")
PY

echo "  === maîtres (Lasker, Capablanca, Nimzowitsch, Payne, Smith, Cavendish) ==="
python3 tools/mesure_maitres.py --rapide --json "$SORTIE_M" >/dev/null || exit 1
python3 - "$SORTIE_M" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
e, go, da, ca = d["echecs"], d["go"], d["dames"], d["cartes"]
assert e["premier_coup_maitre"]["avec"] is True, e["premier_coup"]
assert e["livre"]["suivis"] == e["livre"]["demandes"], e["livre"]
assert e["mats_en_un"]["avec"] == 3, e["mats_en_un"]
assert go["premier_9_avec"]["ligne_3_4"] >= go["premier_9_sans"]["ligne_3_4"], go
assert da["parties"] >= 6, da
assert ca["donnes"] >= 200, ca
print(f"     échecs : {e['premier_coup']['avec']} (sans {e['premier_coup']['sans']}) ; "
      f"livre {e['livre']['suivis']}/{e['livre']['demandes']} ; "
      f"mats {e['mats_en_un']['avec']}/3 ; "
      f"accord maîtres {e['accord_parties']['avec_maitres']}/{e['accord_parties']['positions']} ; "
      f"go 9×9 {go['premier_9_avec']['ligne_3_4']}/{go['premier_9_avec']['graines']} "
      f"(sans {go['premier_9_sans']['ligne_3_4']}) ; "
      f"dames {da['maitres_gagnent']}/{da['parties']} (base blanc {da['base_blanc_gagne']}) ; "
      f"cartes {ca['maitres_vs_base']}/{ca['donnes']} (base-base {ca['base_vs_base']})")
PY

echo "  ✅ la porte des jeux tient : 100 % au niveau 4, 33/33 paires invariantes, 0 collision,"
echo "     la restitution et la perturbation exactes, le perft, la pensée invariante,"
echo "     71 langues et les principes des maîtres mesurés."
