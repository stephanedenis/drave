#!/bin/bash
# porte-episodique.sh — la porte de la capacité C6 : mémoire épisodique.
#
# CE QU'ELLE PROUVE, ET POURQUOI CHAQUE CAS EXISTE.
#   1. l'invariant du plan : écrire puis relire **avec la même clé** rend la valeur
#      écrite AU BIT PRÈS (round-trip) ;
#   2. le passage par le DISQUE ne change aucune lecture — un invariant qui ne
#      survit pas au fichier n'est pas un invariant ;
#   3. le rappel DÉCROÎT quand l'indice se dégrade — une prédiction falsifiable ;
#   4. un indice JAMAIS écrit obtient un recouvrement plus faible qu'un indice écrit :
#      sans cela, le magasin ne sait pas refuser, il rend toujours son meilleur
#      candidat ;
#   5. à petit k, les clés ENTRENT EN COLLISION et le round-trip CASSE — et la porte
#      exige que les échecs soient TOUS expliqués par les collisions. C'est le cas
#      le plus important : il montre que l'invariant dépend du couple (données, k),
#      donc qu'il se mesure au lieu de se supposer.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
N=${N:-300}
K=${K:-64}
T=$(mktemp -d)
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }

essai() { # $1 = k, $2 = fichier magasin (vide = aucun)
  local extra=()
  [ -n "$2" ] && extra=(--episodique-fichier "$2")
  timeout 900 "$D" "$M" --episodique-essai "$N" --episodique-k "$1" --ids-file "$IDS" \
     --ctx 512 --threads 8 "${extra[@]}" 2>&1
}

echo "=== 1. round-trip, séparation, nouveauté (k=$K) ==="
S=$(essai "$K" "$T/magasin.txt") || { echo "  ❌ l'essai a échoué"; exit 1; }
printf '%s\n' "$S" | grep -E "clés distinctes|round-trip|séparation|nouveauté|fichier" | sed 's/^/  /'

printf '%s' "$S" | grep -qE "round-trip +: $N/$N" \
  || { echo "  ❌ le round-trip n'est pas exact à k=$K : l'invariant de C6 est rompu"; exit 1; }
echo "  ✅ round-trip exact ($N/$N) et clés deux à deux distinctes"

echo "=== 2. le disque ne change aucune lecture ==="
printf '%s' "$S" | grep -qE "fichier +: .* → relu, $N/$N lectures identiques" \
  || { echo "  ❌ le passage par le fichier change des lectures"; exit 1; }
echo "  ✅ $N lectures identiques après passage par le disque"

echo "=== 3. le rappel décroît quand l'indice se dégrade ==="
printf '%s\n' "$S" | grep -E "^ +[0-9]+ +[0-9]" | sed 's/^/  /'
# La sortie de l'essai est écrite dans un fichier : un heredoc ET un `<<<` sur la
# même commande se disputent l'entrée standard, et c'est le `<<<` qui gagne — Python
# recevait alors le journal du modèle comme programme (attrapé au premier essai).
printf '%s\n' "$S" > "$T/s1.txt"
python3 - "$T/s1.txt" <<'PY' || exit 1
import re, sys
lignes = [l for l in open(sys.argv[1]).read().splitlines() if re.match(r"^\s+\d+\s+\d", l)]
if not lignes:
    sys.exit("  ❌ aucune ligne de courbe lue")
# dernière ligne = le plus grand N : c'est là que la dégradation se voit
ch = re.findall(r"(\d+\.\d) %", lignes[-1])
vals = [float(x) for x in ch]
assert len(vals) >= 5, f"5 colonnes attendues, {len(vals)} lues"
assert all(a >= b for a, b in zip(vals, vals[1:])), \
    f"le rappel doit décroître avec la dégradation : {vals}"
assert vals[0] == 100.0, f"un indice intact doit retrouver l'épisode : {vals[0]}"
assert vals[-1] < vals[0], "une dégradation de 75 % doit coûter quelque chose"
print(f"  ✅ monotonie respectée : {vals[0]} % → {vals[-1]} % (0 % → 75 % de dégradation)")
PY

echo "=== 4. un indice jamais écrit doit être moins bien retrouvé ==="
python3 - "$T/s1.txt" <<'PY' || exit 1
import re, sys
t = open(sys.argv[1]).read()
m = re.search(r"recouvrement moyen ([\d.]+)/\d+ pour un épisode CONNU, ([\d.]+)/\d+", t)
if not m: sys.exit("  ❌ la mesure de nouveauté est absente")
connu, nouveau = float(m.group(1)), float(m.group(2))
if nouveau >= connu:
    sys.exit(f"  ❌ un indice JAMAIS écrit obtient {nouveau} contre {connu} pour un connu : "
             "le magasin ne sait pas refuser")
print(f"  ✅ connu {connu} > jamais écrit {nouveau} : le magasin distingue « je me souviens » "
      "de « ça ressemble »")
PY

echo "=== 5. à petit k, les collisions EXPLIQUENT les échecs de round-trip ==="
S2=$(essai 8 "") || { echo "  ❌ l'essai a échoué"; exit 1; }
printf '%s\n' "$S2" | grep -E "clés distinctes|round-trip|échecs expliqués" | sed 's/^/  /'
printf '%s\n' "$S2" > "$T/s2.txt"
python3 - "$T/s2.txt" <<'PY' || exit 1
import re, sys
t = open(sys.argv[1]).read()
d = re.search(r"clés distinctes\s*:\s*(\d+)/(\d+)", t)
r = re.search(r"round-trip\s*:\s*(\d+)/(\d+)", t)
e = re.search(r"échecs expliqués\s*:\s*(\d+) par COLLISION.*?(\d+) par ÉGALITÉ", t, re.S)
if not (d and r and e): sys.exit("  ❌ mesures de collision absentes")
distincts, total = int(d.group(1)), int(d.group(2))
exacts = int(r.group(1))
coll, egal = int(e.group(1)), int(e.group(2))
if distincts != exacts:
    sys.exit(f"  ❌ {total - distincts} collisions de clés mais {total - exacts} échecs de "
             "round-trip : les échecs ne sont PAS tous expliqués par les collisions")
if coll + egal != total - exacts:
    sys.exit(f"  ❌ le compte des causes ({coll} + {egal}) ne boucle pas sur {total - exacts} échecs")
if total - exacts == 0:
    sys.exit("  ❌ à k=8 on attend des collisions : le cas ne prouve rien")
print(f"  ✅ {total - exacts} échecs, tous expliqués : {coll} collisions, {egal} égalités "
      "de recouvrement")
PY
echo
echo "  ✅ la porte C6 est franchie — et elle dit ses conditions : $N états consécutifs d'un"
echo "     seul texte, k=$K, aucun élagage obtenu par l'index (100 % du magasin examiné)."
rm -rf "$T"
