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
# Motif SERRÉ (« N  x.x % ( ») : depuis C7, la sortie contient aussi des lignes de
# consolidation qui commencent par deux nombres, et les confondre faisait lire une
# ligne de consolidation comme une ligne de courbe (attrapé par la porte elle-même).
lignes = [l for l in open(sys.argv[1]).read().splitlines() if re.match(r"^\s+\d+\s+[\d.]+ % \(", l)]
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

echo "=== 3bis. la mémoire LOCALISE : l'erreur est en JETONS, et elle est petite ==="
# Savoir si la mémoire rend l'épisode EXACT est une chose ; savoir à quelle DISTANCE
# elle se trompe en est une autre, et c'est celle qui décide de l'usage : un épisode
# voisin de deux jetons situe le passage, un épisode à cinq cents jetons ne situe rien.
# Les épisodes sont numérotés dans l'ordre du texte, donc la distance entre
# identifiants EST une distance en jetons.
python3 - "$T/s1.txt" <<'PYLOC' || exit 1
import re, sys
t = open(sys.argv[1]).read()
lignes = [l for l in t.splitlines() if re.match(r"^\s+\d+\s+[\d.]+ % \(", l)]
if not lignes:
    sys.exit("  ❌ aucune ligne de courbe")
dernier = lignes[-1]
cellules = re.findall(r"(\d+\.\d) % \((\d+\.\d+)\) Δ(\d+)", dernier)
if len(cellules) < 5:
    sys.exit(f"  ❌ la courbe ne porte pas les cinq dégradations : {dernier}")
vals = [(float(a), float(b), int(c)) for a, b, c in cellules]
# À 0 % et 25 % de dégradation, la localisation doit être exacte et précise.
for i, seuil in ((0, 0), (2, 5)):
    pct, base, delta = vals[i]
    if delta > seuil:
        sys.exit(f"  ❌ à {pct} % de dégradation, l'erreur moyenne est de {delta} jetons "
                 f"(seuil {seuil}) — la mémoire ne localise pas")
print(f"  ✅ localisation : Δ = {vals[0][2]} jeton à 0 %, {vals[2][2]} à 25 %, "
      f"{vals[3][2]} à 50 %, {vals[4][2]} à 75 % de dégradation")
# Et la dégradation doit COÛTER en précision aussi, pas seulement en exactitude.
if vals[4][2] <= vals[0][2]:
    sys.exit("  ❌ l'erreur de localisation ne bouge pas avec la dégradation : la mesure "
             "ne dit rien")
print(f"  ✅ et l'erreur croît avec la dégradation ({vals[0][2]} → {vals[4][2]} jetons) : "
      "quand la mémoire se trompe, elle se trompe de PRÈS")
PYLOC

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
echo "=== 6. expansion + égalisation : l'index doit ÉLUDER pour de vrai ==="
# Le cas qui a demandé trois ingrédients : dilater (gyrus denté), décorréler, et
# ÉGALISER l'usage des canaux. Sans le troisième, la séparation s'améliore mais
# l'index n'élude pas (des canaux « hub » portent tout le magasin).
K6=${K6:-64}
EXP=${EXP:-16384}
S3=$(timeout 1200 "$D" "$M" --episodique-essai "$N" --episodique-k "$K6" \
     --episodique-expansion "$EXP" --episodique-decorreler --episodique-normaliser \
     --ids-file "$IDS" --ctx 512 --threads 8 2>&1) || { echo "  ❌ l'essai a échoué"; exit 1; }
printf '%s\n' "$S3" | grep -E "expansion|égalisation|coût de|clé |round-trip|séparation|listes" | sed 's/^/  /'
printf '%s\n' "$S3" | tail -2 | sed 's/^/  /'
printf '%s\n' "$S3" > "$T/s3.txt"
python3 - "$T/s3.txt" "$N" <<'PYVERIF' || exit 1
import re, sys
t = open(sys.argv[1]).read(); n = int(sys.argv[2])
rt = re.search(r"round-trip\s*:\s*(\d+)/(\d+)", t)
if not rt or int(rt.group(1)) != n:
    sys.exit("  ❌ le round-trip doit rester EXACT avec l'expansion : " + (rt.group(0) if rt else "absent"))
sep = re.search(r"séparation\s*:\s*recouvrement moyen ([\d.]+)/(\d+)", t)
if not sep: sys.exit("  ❌ mesure de séparation absente")
part = float(sep.group(1)) / int(sep.group(2))
if part > 0.10:
    sys.exit("  ❌ la séparation doit tomber sous 10 %% de la clé, elle est à %.1f %%" % (100*part))
lignes = [l for l in t.splitlines() if re.match(r"^\s+\d+\s+[\d.]+ % \(", l)]
m = re.search(r"co\u00fbt (\d+) cand\. \((\d+) % du magasin\)", lignes[-1])
if not m:
    m = re.search(r"co\u00fbt (\d+) cand\. \((\d+) % du magasin\)", lignes[-1].replace("û", "u"))
if not m: sys.exit("  ❌ coût illisible : " + lignes[-1])
cand, pct = int(m.group(1)), int(m.group(2))
if pct > 50:
    sys.exit("  ❌ l'index doit ÉLUDER la moitié du magasin au moins, il en examine %d %%" % pct)
vals = [float(x) for x in re.findall(r"(\d+\.\d) %", lignes[-1])]
if vals[2] < 90.0:
    sys.exit("  ❌ le rappel à 25 %% de dégradation doit rester >= 90 %%, il est à %s %%" % vals[2])
print("  ✅ round-trip exact (%d/%d), séparation %.1f %% de la clé, élagage %d %% (%d candidats), rappel 25 %% : %s %%"
      % (n, n, 100*part, 100-pct, cand, vals[2]))
PYVERIF

echo "=== 7. consolidation par rejeu : l'EXEMPLAIRE doit battre la MOYENNE ==="
# Deux façons de faire un prototype, et une prédiction falsifiable : garder un CAS
# RÉEL (exemplaire) doit à la fois compresser PLUS et rappeler MIEUX qu'une moyenne,
# parce que la clé d'une moyenne ne coïncide avec la clé d'aucun membre.
python3 - "$T/s3.txt" <<'PYCONS' || exit 1
import re, sys
t = open(sys.argv[1]).read()
blocs = re.findall(r"prototype (MOYENNE|EXEMPLAIRE)[^\n]*\n(.*?)(?=\n  prototype|\n  le rappel)", t, re.S)
if len(blocs) != 2:
    sys.exit("  ❌ les deux blocs de consolidation sont absents ou illisibles")
mes = {}
for nom, corps in blocs:
    lignes = [l for l in corps.splitlines() if re.match(r"^\s+\d+\s+\d+", l)]
    # ligne du seuil 1 : prototypes, compression, rappel
    # Les colonnes sont « seuil prototypes compression % rappel % erreur » : le
    # signe % est un CHAMP à part, donc la compression est ch[2] et le rappel ch[4].
    ch = lignes[0].split()
    if len(ch) < 5 or ch[3] != "%" or ch[5] != "%":
        sys.exit("  \u274c ligne de consolidation inattendue : " + lignes[0])
    mes[nom] = (int(ch[1]), float(ch[2]), float(ch[4]))
pm, cm, rm = mes["MOYENNE"]
pe, ce, re_ = mes["EXEMPLAIRE"]
print("  MOYENNE    : seuil 1 -> %d prototypes (%.1f %% du magasin), rappel %.1f %%" % (pm, cm, rm))
print("  EXEMPLAIRE : seuil 1 -> %d prototypes (%.1f %% du magasin), rappel %.1f %%" % (pe, ce, re_))
if re_ <= rm:
    sys.exit("  ❌ l'exemplaire ne rappelle pas mieux que la moyenne (%.1f %% contre %.1f %%)" % (re_, rm))
if re_ < 80.0:
    sys.exit("  ❌ le rappel d'appartenance de l'exemplaire doit rester >= 80 %%, il est à %.1f %%" % re_)
if ce > 30.0:
    sys.exit("  ❌ l'exemplaire doit compresser sous 30 %% du magasin, il est à %.1f %%" % ce)
print("  ✅ à compression comparable, l'exemplaire rappelle : %.1f %% contre %.1f %%" % (re_, rm))
PYCONS

echo "=== 8. consolidation RÉPÉTÉE : c'est un POINT FIXE dès le 2e cycle ==="
# Rejouer une mémoire déjà consolidée ne doit ni la comprimer davantage ni l'user. La
# mesure le dit de façon exacte : à partir du 2e cycle, l'erreur de reconstruction est
# 0,00e0 (chaque prototype est son propre exemplaire) et le rappel d'appartenance ne
# bouge plus. Un point fixe, et pas une dégradation lente.
S4=$(timeout 1200 "$D" "$M" --episodique-essai "$N" --episodique-k "$K6" \
     --episodique-expansion "$EXP" --episodique-decorreler --episodique-normaliser \
     --episodique-cycles 4 --episodique-cycles-seuil 4 \
     --ids-file "$IDS" --ctx 512 --threads 8 2>&1) || { echo "  ❌ l'essai a échoué"; exit 1; }
printf '%s\n' "$S4" | sed -n '/consolidation RÉPÉTÉE/,/^$/p' | head -7 | sed 's/^/  /'
printf '%s\n' "$S4" > "$T/s4.txt"
python3 - "$T/s4.txt" <<'PYFIXE' || exit 1
import re, sys
t = open(sys.argv[1]).read()
bloc = t.split("consolidation RÉPÉTÉE")[1].split("consolidation par rejeu")[0]
lignes = [l.split() for l in bloc.splitlines() if re.match(r"^\s+\d+\s+\d+", l)]
if len(lignes) < 3:
    sys.exit(f"  ❌ cycles illisibles ({len(lignes)} lignes)")
# champs : cycle prototypes compression % rappel % erreur
etats = [(int(c[0]), int(c[1]), float(c[2]), float(c[4]), c[6]) for c in lignes]
c1 = etats[0]
for c in etats[1:]:
    if c[1] != c1[1] or abs(c[2] - c1[2]) > 1e-9 or abs(c[3] - c1[3]) > 1e-9:
        sys.exit(f"  ❌ la consolidation n'est pas un point fixe : cycle {c[0]} → "
                 f"{c[1]} prototypes, {c[2]} %, rappel {c[3]} % (cycle 1 : {c1[1]}, "
                 f"{c1[2]} %, {c1[3]} %)")
    if c[4] != "0.00e0":
        sys.exit(f"  ❌ au cycle {c[0]} l'erreur devrait être exactement nulle, "
                 f"elle est de {c[4]}")
print(f"  ✅ point fixe atteint dès le cycle 2 : {c1[1]} prototypes, {c1[2]} % du magasin, "
      f"rappel {c1[3]} %, erreur 0.00e0 sur les cycles suivants")
PYFIXE

echo
echo "  ✅ la porte C6 est franchie — et elle dit ses conditions : $N états consécutifs d'un"
echo "     seul texte, k=$K. Sans expansion, l'index n'élude RIEN (100 % du magasin) ; avec"
echo "     expansion + égalisation, il en élude plus de la moitié (cas 6)."
rm -rf "$T"
