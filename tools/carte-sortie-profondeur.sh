#!/bin/bash
# carte-sortie-profondeur.sh — dessin H : **où** sortir ? L'accord et la qualité en fonction de la
# profondeur de sortie.
#
# LA QUESTION QUE LA MESURE PRÉCÉDENTE LAISSE OUVERTE. `porte-profondeur-routee.sh` mesure **une**
# sortie : 16 couches sur 24. Sa borne (l'accord) ne vaut que pour ce point, et le rapport le dit :
# un chemin court lu après 20 couches serait bien meilleur, donc la borne serait plus haute — mais
# il épargne moins de couches (4 au lieu de 8). Entre les deux, il y a un **optimum**, et il se
# mesure : c'est cette carte.
#
# CE QU'ELLE TRACE, POUR CHAQUE PROFONDEUR DE SORTIE D :
#   · le chemin long est TOUJOURS le même (l'état de 24 couches lu par la tête du modèle) ;
#   · le chemin court est l'état de D couches lu par un adaptateur **entraîné pour ce D** ;
#   · l'accord (la borne de l'oracle), la justesse des deux, et l'écart entre eux **sur les jetons
#     que le seuil de confiance choisit** (la colonne qui décide si un modèle routé est viable).
#
# Le résultat intéressant n'est pas « quel D gagne » mais **la forme de la courbe** : si l'accord
# monte lentement quand on sort tard, le dessin H n'a pas de bon point ; s'il monte vite, il en a un.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
TEXTE=${TEXTE:-data/wikitext2_test.txt}
P=${P:-/home/stephane/gpu-env/bin/python}
T=${TRAVAIL:-/tmp/carte-sortie-profondeur}
N=${N:-8192}
SORTIES=${SORTIES:-"12 16 20 22"}
TEST_MIN=${TEST_MIN:-1000}
TEST_MAX=${TEST_MAX:-3000}
EPOQUES=${EPOQUES:-30}
DELAI=${DELAI:-2400}

for f in "$D" "$M" "$TEXTE"; do
    [ -e "$f" ] || { echo "  ❌ $f manquant"; exit 2; }
done
$P -c "import torch" 2>/dev/null || { echo "  ❌ $P n'a pas torch"; exit 2; }
mkdir -p "$T"
IDS="$T/corpus.ids"
if [ ! -s "$IDS" ]; then
    "$D" "$M" --tokenize --fichier "$TEXTE" --sortie "$IDS" > "$T/tokenize.log" 2>&1
fi
[ -s "$IDS" ] || { echo "  ❌ la tokenisation n'a rien écrit"; exit 1; }
echo "corpus : $(tr ',' '\n' < "$IDS" | wc -l) jetons · sorties étudiées : $SORTIES"

echo
echo "=== 1. capturer l'état de chaque profondeur de sortie (et le chemin long) ==="
mkdir -p "$T/e24"
POS_TOUT=$(seq -s, 4 $((N - 1)))
POS_TEST=$(seq -s, "$TEST_MIN" "$TEST_MAX")
"$D" "$M" --ppl "$IDS" --limit $((TEST_MAX + 2)) --ctx "$N" --threads 8 --couches 0:24 \
    --etat-sortie "$T/e24/etat" --etat-pos "$POS_TEST" > "$T/e24.log" 2>&1 &
LONGS="$!"
for S in $SORTIES; do
    mkdir -p "$T/d$S"
    "$D" "$M" --ppl "$IDS" --limit "$N" --ctx "$N" --threads 8 --couches "0:$S" \
        --tete-partielle --etat-sortie "$T/d$S/etat" --etat-pos "$POS_TOUT" > "$T/d$S.log" 2>&1 &
done
wait "$LONGS" || { echo "  ❌ le parcours 24 couches a échoué"; exit 1; }
wait
for S in $SORTIES; do
    n=$(ls -1 "$T/d$S"/etat.* 2>/dev/null | grep -cE '\.[0-9]+$')
    echo "  sortie $S : $n états"
    [ "$n" -ge $((N - 8)) ] || { echo "  ❌ trop peu d'états pour la sortie $S"; exit 1; }
done

echo
echo "=== 2. la mesure, une profondeur de sortie à la fois ==="
for S in $SORTIES; do
    timeout "$DELAI" $P tools/profondeur_routee_oracle.py \
        --etats16 "$T/d$S/etat" --etats24 "$T/e24/etat" --ids "$IDS" --modele "$M" \
        --limite "$N" --test-min "$TEST_MIN" --test-max "$TEST_MAX" --train-partie apres \
        --epoques "$EPOQUES" --graine 0 > "$T/oracle-$S.log" 2>&1
    c=$?
    [ "$c" = 0 ] || { echo "  ❌ sortie $S : la mesure a échoué (code $c)"; tail -8 "$T/oracle-$S.log" | sed 's/^/    /'; exit 1; }
    echo "  sortie $S : mesurée"
done

echo
echo "=== 3. la carte ==="
$P - "$T" "$SORTIES" <<'PY'
import pathlib, re, sys
T, sorties = pathlib.Path(sys.argv[1]), sys.argv[2].split()
def nombre(t, motif):
    m = re.search(motif, t)
    return float(m.group(1).replace(",", "")) if m else None
lignes = []
for s in sorties:
    t = (T / f"oracle-{s}.log").read_text()
    just_long = nombre(t, r"long — 24 couches.*?\| ([\d.,]+) % \|")
    just_court = nombre(t, r"court — \d+ couches.*?\| ([\d.,]+) % \|")
    ppl_court = nombre(t, r"court — \d+ couches.*?\| ([\d.,]+) \|")
    accord = nombre(t, r"ACCORD court/long : ([\d.,]+) %")
    dernier = re.findall(r"^\| ([\d.]+) \| ([\d.]+) % \| ([\d.]+) % \| ([\d.]+) % \| ([\d.]+) % \| "
                         r"([\d.]+) % \|$", t, re.M)
    part = juste = None
    if dernier:
        _, part, juste, _, _, _ = dernier[-1]
        part, juste = float(part), float(juste)
    if None in (just_long, just_court, accord):
        print(f"  ❌ sortie {s} : chiffres illisibles"); sys.exit(1)
    lignes.append((int(s), just_long, just_court, ppl_court, accord, part, juste))
print("| sortie | couches sautées | ppl court | justesse court | justesse long | **accord** | "
      "part sortie (seuil 0,99) | justesse globale |")
print("|---|---:|---:|---:|---:|---:|---:|---:|")
for s, jl, jc, pc, ac, part, juste in lignes:
    print(f"| {s} / 24 | {24 - s} | {pc:,.4f} | {jc:.2f} % | {jl:.2f} % | **{ac:.2f} %** | "
          f"{part:.1f} % | {juste:.2f} % |")
meilleur = max(lignes, key=lambda l: l[4] * (24 - l[0]) / 24)
print()
print(f"Meilleur produit (accord × couches sautées) : sortie **{meilleur[0]}**, soit "
      f"**{meilleur[4] * (24 - meilleur[0]) / 24:.1f} %** des paires épargnées — au mieux, avec un "
      f"routeur parfait.")
print("Lecture : la colonne « accord » est ce qu'un routeur PARFAIT épargnerait sans rien changer ;")
print("la dernière colonne est ce qu'un seuil de confiance atteint réellement, à comparer à la")
print("justesse du chemin long seul (colonne 5).")
PY
