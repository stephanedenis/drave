#!/usr/bin/env bash
# porte-banc-performance — le banc de performance mesure, et son JSON est complet.
#
# Ce qu'elle vérifie : les 12 tests des fondations (préfixe exact, bloc de phrases entières,
# ajustements linéaire/quadratique/log-log, lecture de la ligne TAGGER, extrapolation), puis
# un passage COURT du banc (1 000 mots, 20 phrases, 3 tailles, bloc ×1/×2/×4) hors ligne.
# Elle ne juge PAS le chiffre de performance (il dépend de la machine) : elle vérifie que le
# banc tourne, que le JSON porte les mesures et que le contrôle de linéarité est calculé.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
ko=0
dit() { printf '  %s %s\n' "$1" "$2"; }
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

if python3 tools/tests/test_banc_performance.py >"$tmp/tests.log" 2>&1; then
  dit ✅ "tests : $(grep -oE 'Ran [0-9]+ tests' "$tmp/tests.log" | head -1)"
else
  dit ❌ "tests en échec (voir ci-dessous)"; tail -20 "$tmp/tests.log"; ko=1
fi

if timeout 300 python3 tools/banc_performance.py \
     --mots 1000 --phrases-courtes 20 --tailles 250,500,1000 \
     --bloc-repetitions 1,2,4 --repetitions 1 \
     --sortie "$tmp/performance.json" >"$tmp/banc.log" 2>&1; then
  dit ✅ "passage court : $(grep -c 'banc :' "$tmp/banc.log") étapes"
else
  dit ❌ "passage court en échec (code $?)"; tail -20 "$tmp/banc.log"; ko=1
fi

if [ -f "$tmp/performance.json" ] && python3 - "$tmp/performance.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
assert d["schema"] == "drave.performance" and d["version"] == 1, d.get("schema")
assert d["corpus"]["mots"] == 1000, d["corpus"]["mots"]
assert len(d["corpus"]["prefixe_sha256"]) == 64
r = d["mesures"]["reel_10000"]
assert r["fonction"]["duree_analyse_s"]["mediane"] > 0, r["fonction"]
assert r["fonction"]["rss_kb"]["mediane"] > 0, r["fonction"]
assert r["cli"]["octets"] > 0, r["cli"]
assert r["cli"]["etiquettes"] > 0, r["cli"]
c = d["mesures"]["cent_courtes"]
assert c["appels_fonction"]["appels"] == 20, c["appels_fonction"]["appels"]
assert c["appels_cli"]["appels"] == 20, c["appels_cli"]["appels"]
assert c["appels_cli"]["codes"] == [0], c["appels_cli"]["codes"]
b = d["echelle"]["bloc_repete"]
assert len(b["mesures"]) == 3, len(b["mesures"])
assert b["ajustements"]["loglog"]["alpha"] > 0
assert d["echelle"]["instrument"]["quadratique"]["loglog"]["alpha"] > 0
assert isinstance(d["verdict"]["controle_lineaire"], bool)
assert d["verdict"]["prochaine_action"]
print("JSON complet : 1000 mots, 20 phrases, 3 points d'échelle, contrôle calculé")
PY
then
  dit ✅ "JSON : contrat et mesures présents"
else
  dit ❌ "JSON incomplet ou invalide"; ko=1
fi

printf 'Le chat dort.\n\nLe chien mange.\n' >"$tmp/texte.txt"
if timeout 120 python3 tools/banc_performance.py --profil "$tmp/texte.txt" \
     --sortie "$tmp/profil.json" >/dev/null 2>&1 \
   && python3 -c "import json,sys; d=json.load(open('$tmp/profil.json')); assert d['mots']>=4 and d['top'];" 2>/dev/null; then
  dit ✅ "mode profil : fonctions dominantes exportées"
else
  dit ❌ "mode profil en échec"; ko=1
fi

[ "$ko" -eq 0 ] && { echo "✅ porte banc-performance verte"; exit 0; } || { echo "❌ porte banc-performance rouge"; exit 1; }
