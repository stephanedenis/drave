#!/bin/bash
# porte-cycle-c2.sh — C2 : le cycle à deux régions est-il EXACT, borné, déterministe, et son coût
# est-il dit ?
#
# POURQUOI CETTE PORTE. C2 était la dernière capacité que le validateur REFUSAIT, et pour une
# bonne raison : un graphe cyclique n'a pas « une passe = un résultat ». Il se DÉROULE (chaque
# région lit l'état des autres du pas précédent), et c'est le pilote `tools/derouler.py` qui
# déroule — le moteur, lui, exécute une région et transporte son état. Les cinq portes étaient
# écrites AVANT le code (`docs/note-cycle-c2.md` § 4) ; les voici, dans l'ordre :
#
#   1. un graphe SANS lien récurrent est inchangé : deux régions enchaînées doivent rendre
#      EXACTEMENT la perplexité du modèle d'un seul tenant — c'est la non-régression de tout
#      l'existant (le découpage ne change rien, `porte-reparti-moteur` le prouve déjà) ;
#   2. le PREMIER PAS du cycle est cette même chaîne (il n'y a pas d'état d'avant) : le graphe
#      récurrent doit donc rendre, au pas 1, la perplexité de la référence — au chiffre près ;
#   3. le déroulé est BORNÉ et annoncé : `--pas-temps` absent ou nul est refusé, un cycle sans
#      lien récurrent est refusé (code 2), un lien récurrent sans délai est refusé (code 2) ;
#   4. le COÛT est mesuré et publié : N pas = N × (nombre de régions) exécutions ;
#   5. l'état est EXPLICITE : deux déroulés identiques rendent la MÊME trajectoire, et la
#      divergence — si elle a lieu — est PUBLIÉE, pas cachée (la note l'exige : un cycle à gain
#      ≥ 1 diverge, et une porte qui ne dirait que l'égalité mentirait sur la moitié du sujet).
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
P=${P:-python3}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
LIMITE=${LIMITE:-128}
PAS=${PAS:-4}
T=${T:-/tmp/porte-cycle-c2}
[ -s "$M" ] || { echo "  ❌ modèle absent : $M"; exit 2; }
[ -x "$D" ] || { echo "  ❌ binaire du moteur absent : $D"; exit 2; }
. tools/_corpus.sh
mkdir -p "$T"
$P - "$IDS" "$T/morceau.txt" "$LIMITE" <<'PY'
import pathlib, re, sys
ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(sys.argv[1]).read_text()) if x.strip()]
pathlib.Path(sys.argv[2]).write_text(",".join(str(x) for x in ids[:int(sys.argv[3])]))
PY

$P - "$T" <<'PY'
import json, pathlib
t = pathlib.Path(__import__("sys").argv[1])
R = [{"id": "r0", "couches": [0, 11], "instance": "local"},
     {"id": "r1", "couches": [12, 23], "instance": "local"}]
(t / "chaine.json").write_text(json.dumps({"regions": R, "liens": [
    {"de": "r0", "vers": "r1", "mode": "listes", "delai_ms": 0}]}, indent=1))
(t / "cycle.json").write_text(json.dumps({"regions": R, "liens": [
    {"de": "r0", "vers": "r1", "mode": "listes", "delai_ms": 0},
    {"de": "r1", "vers": "r0", "mode": "listes", "delai_ms": 1, "recurrent": True}]}, indent=1))
dist = json.loads((t / "chaine.json").read_text())
dist["regions"][1]["instance"] = "127.0.0.1:49152"
(t / "distante.json").write_text(json.dumps(dist, indent=1))
nu = json.loads((t / "cycle.json").read_text()); nu["liens"][1].pop("recurrent")
(t / "cycle-nu.json").write_text(json.dumps(nu, indent=1))
sd = json.loads((t / "cycle.json").read_text()); sd["liens"][1]["delai_ms"] = 0
(t / "cycle-sans-delai.json").write_text(json.dumps(sd, indent=1))
PY

ppl_directe=$("$D" "$M" --ppl "$T/morceau.txt" --limit "$LIMITE" --ctx "$LIMITE" --threads 8 2>&1 \
              | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+" | head -1)
[ -n "$ppl_directe" ] || { echo "  ❌ perplexité directe illisible"; exit 1; }
echo "porte du cycle C2 — référence (modèle d'un seul tenant, $LIMITE jetons) : $ppl_directe"

# ------------------------------------------------ 1. la chaîne de deux régions est EXACTE
$P tools/derouler.py --topologie "$T/chaine.json" --pas-temps 1 --morceau "$T/morceau.txt" \
    --limite "$LIMITE" --sortie "$T/chaine" --moteur "$D" --modele "$M" --travail "$T/travail-chaine" \
    > "$T/chaine.log" 2>&1 || { echo "  ❌ le déroulé de la chaîne a échoué"; tail -3 "$T/chaine.log"; exit 1; }
ppl_chaine=$(grep -oE "perplexité [0-9.,]+" "$T/chaine.log" | tail -1 | grep -oE "[0-9.]+")
ecart=$($P -c "print(f'{abs(float(\"$ppl_chaine\".replace(chr(44),\"\"))-float(\"$ppl_directe\"))/float(\"$ppl_directe\"):.2e}')")
$P -c "import sys; sys.exit(0 if float('$ecart') < 5e-4 else 1)" \
    || { echo "  ❌ la chaîne de régions rend $ppl_chaine au lieu de $ppl_directe (écart $ecart)"; exit 1; }
echo "  ✅ 1. chaîne de 2 régions EXACTE : $ppl_chaine (écart $ecart)"

# ------------------------------------------------ 2 et 5. le cycle : pas 1 = la référence
$P tools/derouler.py --topologie "$T/cycle.json" --pas-temps "$PAS" --morceau "$T/morceau.txt" \
    --limite "$LIMITE" --sortie "$T/cycle" --moteur "$D" --modele "$M" --travail "$T/travail-cycle" \
    > "$T/cycle.log" 2>&1 || { echo "  ❌ le déroulé du cycle a échoué"; tail -3 "$T/cycle.log"; exit 1; }
ppl_pas1=$(grep -oE "perplexité [0-9.,]+" "$T/cycle.log" | head -1 | grep -oE "[0-9.]+")
ecart1=$($P -c "print(f'{abs(float(\"$ppl_pas1\".replace(chr(44),\"\"))-float(\"$ppl_directe\"))/float(\"$ppl_directe\"):.2e}')")
$P -c "import sys; sys.exit(0 if float('$ecart1') < 5e-4 else 1)" \
    || { echo "  ❌ le pas 1 du cycle rend $ppl_pas1 au lieu de $ppl_directe (écart $ecart1)"; exit 1; }
echo "  ✅ 2. pas 1 du cycle EXACT : $ppl_pas1 (écart $ecart1)"

traj=$(grep -oE "perplexité [0-9.,]+" "$T/cycle.log" | grep -oE "[0-9.]+" | tr '\n' ' ')
echo "     trajectoire ($PAS pas) : $traj"
divergence=$($P -c "
import sys
v = [float(x) for x in '$traj'.split()]
print('DIVERGE' if v[-1] > 2 * v[0] else 'STABLE')")
dernier=$(echo "$traj" | awk '{print $NF}')
echo "     ⇒ le cycle NON ENTRAÎNÉ $divergence (pas 1 : $ppl_pas1 → pas $PAS : $dernier)"

# ... et deux déroulés identiques rendent la MÊME trajectoire
$P tools/derouler.py --topologie "$T/cycle.json" --pas-temps "$PAS" --morceau "$T/morceau.txt" \
    --limite "$LIMITE" --sortie "$T/cycle2" --moteur "$D" --modele "$M" --travail "$T/travail-cycle2" \
    > "$T/cycle2.log" 2>&1 || { echo "  ❌ le second déroulé a échoué"; exit 1; }
for i in $(seq 1 "$PAS"); do
    cmp -s "$T/cycle-t$i.f32" "$T/cycle2-t$i.f32" \
        || { echo "  ❌ trajectoire NON déterministe au pas $i"; exit 1; }
done
echo "  ✅ 5. trajectoire déterministe : $PAS pas identiques (cmp) · divergence publiée"

# ------------------------------------------------ 3. les refus
# ⚠️ LA NOTE DISAIT « code 2 » (écrite avant le code) ; le MOTEUR, lui, sort en **3** sur une
# topologie invalide — c'est sa convention établie (`--topologie` invalide ⇒ 3), et la porte
# vérifie donc 3. Le pilote, lui, sort en **2** (la convention « on ne peut pas mesurer »).
refus_moteur() {   # $1 = description, $2 = fichier de topologie
    "$D" "$M" --topologie "$2" >/dev/null 2>&1
    local code=$?
    [ "$code" -eq 3 ] || { echo "  ❌ $1 : code $code au lieu de 3"; exit 1; }
}
refus_pilote() {   # $1 = description ; le reste = arguments
    local d=$1; shift
    "$P" tools/derouler.py "$@" >/dev/null 2>&1
    local code=$?
    [ "$code" -eq 2 ] || { echo "  ❌ $1 : code $code au lieu de 2"; exit 1; }
}
refus_moteur "cycle sans lien récurrent" "$T/cycle-nu.json"
refus_moteur "lien récurrent sans délai" "$T/cycle-sans-delai.json"
refus_pilote "pilote : --pas-temps 0" --topologie "$T/cycle.json" --pas-temps 0 \
    --morceau "$T/morceau.txt" --limite "$LIMITE" --sortie "$T/x" --moteur "$D" --modele "$M"
refus_pilote "pilote : région distante" --topologie "$T/distante.json" --pas-temps 1 \
    --morceau "$T/morceau.txt" --limite "$LIMITE" --sortie "$T/x" --moteur "$D" --modele "$M"
echo "  ✅ 3. borné et annoncé : cycle nu (code 3) · récurrent sans délai (code 3) · pilote : pas-temps 0 (code 2) et région distante (code 2) refusés"

# ------------------------------------------------ 4. le coût est dit
cout="$T/cycle-cout.txt"
executions=$(grep -oE "^executions [0-9]+" "$cout" | grep -oE "[0-9]+")
attendu=$((PAS * 2))
[ "$executions" = "$attendu" ] || { echo "  ❌ coût : $executions exécutions au lieu de $attendu"; exit 1; }
echo "  ✅ 4. coût publié : $PAS pas × 2 régions = $executions exécutions ($(grep -oE '^secondes [0-9.]+' "$cout" | cut -d' ' -f2) s)"
echo "  ✅ porte tenue (chaîne exacte · pas 1 exact · borné · coût dit · trajectoire déterministe)"
exit 0
