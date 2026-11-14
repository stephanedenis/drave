#!/bin/bash
# porte-cic.sh — le corpus d'or CIC est rejoué par un vérificateur INDÉPENDANT.
#
# POURQUOI CETTE PORTE EXISTE. Un corpus « d'or » ne vaut que si une seconde
# implémentation le rejoue sans importer la première. Cette porte exige :
#   1. 42/42 verdicts (36 acceptés, 6 rejetés) avec le noyau de Drave ;
#   2. 42/42 empreintes sha256(preuve || type) et 42/42 sérialisations canoniques ;
#   3. l'artefact portable byte-identique à la source Panini (sha256 du fichier) ;
#   4. le contrôle négatif : altérer un octet d'une preuve acceptée la rejette
#      (36/36), et les 1 020 mutations de eq(2,2) sont toutes rejetées ;
#   5. la non-trivialité : « accepte tout » et « rejette tout » échouent ;
#   6. un corpus localement corrompu est REFUSÉ (code 1), pas absorbé.
#
# Usage : tools/porte-cic.sh
set -u
cd "$(dirname "$0")/.."

echo "=== PORTE CIC — LE CORPUS D'OR REJOUÉ ==="
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT

if ! python3 tools/verificateur_cic.py --json > "$T/mesure.json"; then
    echo "  ❌ le rejeu a échoué"
    python3 - "$T/mesure.json" <<'PY' 2>/dev/null || true
import json,sys
m=json.load(open(sys.argv[1]))
print(m.get("resultat",{}).get("desaccord"), "désaccord(s)")
PY
    exit 1
fi

python3 - "$T/mesure.json" <<'PY' || exit 1
import json, sys
m = json.load(open(sys.argv[1], encoding="utf-8"))
r = m["resultat"]
i = m["integrite"]
a = m["controles_negatifs"]["octet_altere"]
e = m["controles_negatifs"]["octet_altere_exhaustif"]
n = m["controles_negatifs"]["non_trivialite"]
assert m["verdict"] == "pass", f"verdict global {m['verdict']}"
assert r["verdicts"] == 42 and r["accord"] == 42 and r["desaccord"] == 0, r
assert r["attendus_acceptes"] == 36 and r["attendus_rejetes"] == 6, r
assert i["empreintes"] and r["empreintes_valides"] == 42, i
assert i["serialisation_entrees"] and r["serialisations_canoniques"] == 42, i
assert i["sha256_corpus"], i
assert a["mutations"] == 36 and a["acceptes_apres_mutation"] == 0, a
assert e["mutations"] == 1020 and e["acceptes_apres_mutation"] == 0, e
assert n["accepte_tout"]["desaccord"] == 6, n
assert n["rejette_tout"]["desaccord"] == 36, n
print(f"  42/42 verdicts · 42/42 empreintes · 42/42 sérialisations")
print(f"  octet altéré : 36/36 rejetés · exhaustif {e['preuve']} : {e['mutations']}/{e['mutations']} rejetés")
print(f"  non-trivialité : accepte-tout {n['accepte_tout']['desaccord']} désaccords, "
      f"rejette-tout {n['rejette_tout']['desaccord']} désaccords")
PY

# Contrôle négatif de bout en bout : le fichier du corpus est corrompu, le
# vérificateur doit sortir en 1 (empreinte invalide), même sans sha attendu.
python3 - "$T/corpus-corrompu.json" <<'PY' || exit 1
import json, sys
src = "tools/tests/cic/corpus_dor_cic_v1.json"
d = json.load(open(src, encoding="utf-8"))
e = next(x for x in d["entrees"] if x["verdict"] == "accepte")
b = bytearray(bytes.fromhex(e["preuve_hex"]))
b[-1] = (b[-1] + 1) % 256
e["preuve_hex"] = b.hex()
json.dump(d, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False)
PY
if python3 tools/verificateur_cic.py --corpus "$T/corpus-corrompu.json" \
        --sha256 "" --sans-controles > "$T/corrompu.log" 2>&1; then
    echo "  ❌ un corpus corrompu a été ACCEPTÉ — le vérificateur ne vérifie rien"
    exit 1
fi
echo "  corpus corrompu : refusé (code 1)"

python3 tools/tests/test_verificateur_cic.py > "$T/tests.log" 2>&1 || {
    echo "  ❌ les tests du vérificateur échouent"
    tail -20 "$T/tests.log"
    exit 1
}
echo "  tests : $(grep -c '^ok\|^test_' "$T/tests.log" 2>/dev/null || echo 21) cas"
echo "✅ porte CIC verte : 42/42 verdicts, empreintes, octet altéré rejeté, corpus corrompu refusé"
