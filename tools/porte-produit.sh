#!/usr/bin/env bash
# porte-produit — le premier produit : la CLI répond, le JSON est valide, le rejeu est identique.
#
# Ce qu'elle vérifie : `drave --version`, `analyser` (fr et en) rend un JSON parsable avec des
# étiquettes, `rejouer` rend le même sha256 deux fois, et le smoke test passe.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
ko=0
dit() { printf '  %s %s\n' "$1" "$2"; }

ver=$(python3 tools/drave.py --version 2>&1)
case "$ver" in drave*) dit ✅ "version : $ver" ;; *) dit ❌ "version : $ver"; ko=1 ;; esac

for langue in fr en; do
  case "$langue" in
    fr) texte="Le chat dort sur le toit." ;;
    en) texte="The cat sleeps on the roof." ;;
  esac
  sortie=$(python3 tools/drave.py analyser "$texte" --langue "$langue" --json 2>&1)
  if printf '%s' "$sortie" | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['langue'] == '$langue', d.get('langue')
assert len(d['etiquettes']) > 5, len(d['etiquettes'])
assert any(e['niveau'] == 'syntagme' for e in d['etiquettes'])
assert any(e['niveau'] == 'pos' for e in d['etiquettes'])
" 2>/dev/null; then
    dit ✅ "analyser $langue : JSON valide, étiquettes et syntagmes"
  else
    dit ❌ "analyser $langue : JSON invalide ou vide"; ko=1
  fi
done

a=$(python3 tools/drave.py rejouer "Le chat dort." 2>&1 | grep -o 'sha256 [0-9a-f]*' | head -1)
b=$(python3 tools/drave.py rejouer "Le chat dort." 2>&1 | grep -o 'sha256 [0-9a-f]*' | head -1)
if [ -n "$a" ] && [ "$a" = "$b" ]; then dit ✅ "rejeu : $a deux fois"; else dit ❌ "rejeu instable : '$a' vs '$b'"; ko=1; fi

if python3 tools/tests/test_produit.py >/tmp/porte-produit-tests.log 2>&1; then
  dit ✅ "smoke test : $(grep -oE 'Ran [0-9]+ tests' /tmp/porte-produit-tests.log | head -1)"
else
  dit ❌ "smoke test en échec (voir /tmp/porte-produit-tests.log)"; ko=1
fi

if python3 tools/verifier_schema_produit.py --gold 20 >/tmp/porte-produit-valide.log 2>&1; then
  dit ✅ "schéma v1 validé (5 cas + 20 phrases du gold)"
else
  dit ❌ "schéma v1 : validation en échec (voir /tmp/porte-produit-valide.log)"; ko=1
fi

if python3 tools/tests/test_produit_libre.py >/tmp/porte-produit-libre.log 2>&1; then
  dit ✅ "50 textes libres : $(grep -oE 'Ran [0-9]+ tests' /tmp/porte-produit-libre.log | head -1)"
else
  dit ❌ "50 textes libres en échec (voir /tmp/porte-produit-libre.log)"; ko=1
fi

if python3 tools/tests/test_schema_produit.py >/tmp/porte-produit-schema.log 2>&1; then
  dit ✅ "schéma v1 : $(grep -oE 'Ran [0-9]+ tests' /tmp/porte-produit-schema.log | head -1)"
else
  dit ❌ "schéma v1 en échec (voir /tmp/porte-produit-schema.log)"; ko=1
fi

refus=$(python3 tools/drave.py analyser "" --json 2>/dev/null); code=$?
if [ "$code" -eq 3 ] && printf '%s' "$refus" | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['refus'] and d['schema']" 2>/dev/null; then
  dit ✅ "refus : JSON avec refus, code 3"
else
  dit ❌ "refus : code $code, JSON non conforme"; ko=1
fi

if AUTOTEST_JOBS=8 timeout 600 python3 -m tools.pensee.autotest >/tmp/porte-produit-autotest.log 2>&1; then
  dit ✅ "autotest parallèle : $(grep -oE '[0-9]+/[0-9]+ portes tenues' /tmp/porte-produit-autotest.log | tail -1)"
else
  dit ❌ "autotest en échec (voir /tmp/porte-produit-autotest.log)"; ko=1
fi

[ "$ko" -eq 0 ] && { echo "✅ porte produit verte"; exit 0; } || { echo "❌ porte produit rouge"; exit 1; }
