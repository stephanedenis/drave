#!/bin/bash
# porte-cic.sh — le corpus d'or CIC est rejoué par un vérificateur INDÉPENDANT.
#
# POURQUOI CETTE PORTE EXISTE. Un corpus « d'or » ne vaut que si une seconde
# implémentation le rejoue sans importer la première. Cette porte exige :
#   1. 42/42 verdicts (36 acceptés, 6 rejetés) avec le noyau de Drave ;
#   2. 42/42 empreintes sha256(preuve || type) et 42/42 sérialisations canoniques ;
#   3. B3 : 42/42 types de de Bruijn clos et bien formés (`[] ⊢ type : sort n`),
#      42/42 preuves closes, et le sha256 rejoué par une SECONDE implémentation
#      (FIPS 180-4, sans hashlib) sur le corpus, les 42 couples et les 24 termes ;
#   4. l'artefact portable byte-identique à la source Panini (sha256 du fichier) ;
#   5. le contrôle négatif : altérer un octet d'une preuve acceptée la rejette
#      (36/36), altérer un octet d'un type le rend invalide ou rejette la preuve
#      (42/42), et les 1 020 mutations de eq(2,2) sont toutes rejetées ;
#   6. la non-trivialité : « accepte tout » et « rejette tout » échouent ;
#   7. un corpus localement corrompu (preuve OU type) est REFUSÉ (code 1).
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
t = m["type_de_bruijn"]
s = m["sha256_independant"]
a = m["controles_negatifs"]["octet_altere"]
at = m["controles_negatifs"]["type_altere"]
e = m["controles_negatifs"]["octet_altere_exhaustif"]
n = m["controles_negatifs"]["non_trivialite"]
assert m["verdict"] == "pass", f"verdict global {m['verdict']}"
assert r["verdicts"] == 42 and r["accord"] == 42 and r["desaccord"] == 0, r
assert r["attendus_acceptes"] == 36 and r["attendus_rejetes"] == 6, r
assert i["empreintes"] and r["empreintes_valides"] == 42, i
assert i["empreintes_pures"] and r["empreintes_pures_valides"] == 42, i
assert i["serialisation_entrees"] and r["serialisations_canoniques"] == 42, i
assert i["sha256_corpus"], i
assert i["type_de_bruijn"] and t["types_clos"] == 42, t
assert t["types_bien_formes"] == 42 and t["preuves_closes"] == 42, t
assert t["verdict"] == "pass", t
assert s["verdict"] == "pass", s
assert s["corpus"]["concordant"], s["corpus"]
assert s["entrees"]["empreintes_declarees_ok"] == 42, s
assert s["entrees"]["concordantes_hashlib"] == 42, s
assert s["environnement"]["concordants_hashlib"] == 24, s
assert a["mutations"] == 36 and a["acceptes_apres_mutation"] == 0, a
assert a["empreintes_changees"] == 36 and a["empreintes_pures_changees"] == 36, a
assert at["mutations"] == 42 and at["acceptes_apres_mutation"] == 0, at
assert at["empreintes_changees"] == 42 and at["empreintes_pures_changees"] == 42, at
assert e["mutations"] == 1020 and e["acceptes_apres_mutation"] == 0, e
assert n["accepte_tout"]["desaccord"] == 6, n
assert n["rejette_tout"]["desaccord"] == 36, n
print(f"  42/42 verdicts · 42/42 empreintes · 42/42 sérialisations")
print(f"  de Bruijn : {t['types_bien_formes']}/42 types bien formés · "
      f"{t['preuves_closes']}/42 preuves closes · niveaux {t['niveaux_observes']}")
print(f"  sha256 2e implémentation : corpus ok · "
      f"{s['entrees']['concordantes_hashlib']}/42 couples · "
      f"{s['environnement']['concordants_hashlib']}/24 termes · {s['autotest']['vecteurs']} vecteurs")
print(f"  octet altéré : 36/36 rejetés · type altéré : 42/42 rejetés · "
      f"exhaustif {e['preuve']} : {e['mutations']}/{e['mutations']} rejetés")
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
echo "  corpus corrompu (preuve) : refusé (code 1)"

# B3 : même contrôle de bout en bout sur le TYPE. Le type muté doit être
# refusé par la vérification de de Bruijn et/ou par l'empreinte.
python3 - "$T/corpus-type-corrompu.json" <<'PY' || exit 1
import json, sys
src = "tools/tests/cic/corpus_dor_cic_v1.json"
d = json.load(open(src, encoding="utf-8"))
e = next(x for x in d["entrees"] if x["verdict"] == "accepte")
b = bytearray(bytes.fromhex(e["type_hex"]))
b[-1] = (b[-1] + 1) % 256
e["type_hex"] = b.hex()
json.dump(d, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False)
PY
if python3 tools/verificateur_cic.py --corpus "$T/corpus-type-corrompu.json" \
        --sha256 "" --sans-controles > "$T/corrompu-type.log" 2>&1; then
    echo "  ❌ un corpus au TYPE corrompu a été ACCEPTÉ — la vérification de de Bruijn ne sert à rien"
    exit 1
fi
echo "  corpus corrompu (type) : refusé (code 1)"

python3 tools/tests/test_verificateur_cic.py > "$T/tests-j122.log" 2>&1 || {
    echo "  ❌ les tests J12.2 du vérificateur échouent"
    tail -20 "$T/tests-j122.log"
    exit 1
}
python3 tools/tests/test_verificateur_cic_v2.py > "$T/tests-b3.log" 2>&1 || {
    echo "  ❌ les tests B3 du vérificateur échouent"
    tail -20 "$T/tests-b3.log"
    exit 1
}
N122=$(sed -nE 's/^Ran ([0-9]+) tests? in .*/\1/p' "$T/tests-j122.log" | tail -1)
NB3=$(sed -nE 's/^Ran ([0-9]+) tests? in .*/\1/p' "$T/tests-b3.log" | tail -1)
N=$(( ${N122:-0} + ${NB3:-0} ))
echo "  tests : ${N122:-?} (J12.2) + ${NB3:-?} (B3) = $N cas"
echo "✅ porte CIC verte : 42/42 verdicts, empreintes, de Bruijn, sha256 2e implémentation,"
echo "   preuves et types altérés rejetés, corpus corrompu refusé"
