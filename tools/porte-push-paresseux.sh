#!/bin/bash
# porte-push-paresseux.sh — la forme « listes » construite à la demande rend-elle LE MÊME calcul ?
#
# POURQUOI CETTE PORTE. Le 12/10, la forme « listes » (`PushMat`) est devenue **paresseuse** :
# elle n'est plus construite au chargement mais au premier usage réel, depuis le fichier. Le gain
# est mesuré (chargement 26,95 s → 7,36 s sur Qwen3-30B ; 6,85 s → 0,60 s sur Qwen2.5-0.5B) et il
# ne vaut QUE si le résultat est identique — or une reconstruction tardive peut diverger de la
# construction d'avance (élagage appliqué entre-temps, mauvais nom de tenseur, dimensions
# inversées). `DRAVE_PUSH_TOT=1` refait la construction d'avance : c'est le témoin.
#
# CE QU'ELLE VÉRIFIE
#   1. le texte GÉNÉRÉ (ids, `--temp 0`) est identique en paresseux et en avance ;
#   2. une passe `--ppl` ne construit AUCUNE forme paresseuse (sinon la paresse ne sert à rien)
#      et charge au moins 2× plus vite que la construction d'avance ;
#   3. et elle sait ÉCHOUER : avec `DRAVE_PUSH_FAUX=1` (forme construite depuis des zéros), les
#      ids DOIVENT différer — sans quoi elle ne vérifie rien.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-data/wikitext2_test.txt.ids}
PROMPT=${PROMPT:-"Le ciel est bleu parce que"}
N=${N:-16}
[ -s "$M" ] || { echo "  ❌ modèle absent : $M"; exit 2; }

ids_de() {   # $1 = réglages d'environnement ; rend les ids générés
    env $1 "$D" "$M" --infer --prompt "$PROMPT" --n "$N" --ctx 64 --threads 8 --temp 0 2>&1 \
        | grep -oE "ids générés : \[[0-9, ]*\]" | head -1
}
# LE NOMBRE CHANGE D'UNITÉ SELON SA GRANDEUR : le moteur imprime « 601.03ms » (durée `{:?}`)
# quand le chargement est rapide, et « 7.36s » sinon. La première version de cette porte ne
# parsait que les secondes : elle passait sur une machine lente et rendait une chaîne VIDE sur
# une machine rapide — trouvé par la passe complète du 13/10 à 02 h 18, pas par relecture.
# On lit donc l'unité, et on normalise en secondes.
charge_de() {  # $1 = réglages ; rend le temps de chargement en secondes
    env $1 "$D" "$M" --ppl "$IDS" --ctx 64 --limit 2 --threads 8 2>&1 \
        | grep -oE "chargées en [0-9.]+(µs|ms|s)" | head -1 | grep -oE "[0-9.]+(µs|ms|s)"
}

# Conversion en secondes, et REFUS de mesurer sur du vide : une porte qui lit une chaîne vide
# et se contente d'un `float("")` échoue sans dire pourquoi.
en_secondes() {
    case "$1" in
        *µs) python3 -c "print(float('${1%µs}')/1e6)" ;;
        *ms) python3 -c "print(float('${1%ms}')/1e3)" ;;
        *s)  python3 -c "print(float('${1%s}'))" ;;
        *)   echo "VIDE" ;;
    esac
}

echo "porte de la paresse — $(basename "$M")"
I_PARe=$(ids_de "")
I_AVANCE=$(ids_de "DRAVE_PUSH_TOT=1")
I_FAUX=$(ids_de "DRAVE_PUSH_FAUX=1")
echo "  paresseux : ${I_PARe:0:60}…"
echo "  d'avance  : ${I_AVANCE:0:60}…"

[ -n "$I_PARe" ] && [ -n "$I_AVANCE" ] || { echo "  ❌ aucune génération lisible"; exit 1; }
if [ "$I_PARe" != "$I_AVANCE" ]; then
    echo "  ❌ la forme paresseuse ne rend PAS le même texte que la forme construite d'avance"
    exit 1
fi
echo "  ✅ même texte (16 jetons gourmands) en paresseux et en avance"

if [ "$I_FAUX" = "$I_PARe" ]; then
    echo "  ❌ la porte ne sait pas échouer : DRAVE_PUSH_FAUX=1 rend le MÊME texte"
    exit 1
fi
echo "  ✅ vue ROUGE avec un défaut volontaire (DRAVE_PUSH_FAUX=1 change le texte)"

# La paresse ne doit rien construire là où le chemin push n'est pas pris, et doit charger plus vite.
T_PARe=$(en_secondes "$(charge_de "")")
T_AVANCE=$(en_secondes "$(charge_de "DRAVE_PUSH_TOT=1")")
if [ "$T_PARe" = "VIDE" ] || [ "$T_AVANCE" = "VIDE" ]; then
    echo "  ❌ le temps de chargement est illisible (paresseux=« $T_PARe », avance=« $T_AVANCE »)"
    echo "     sortie brute du moteur (paresseux) :"
    env "$D" "$M" --ppl "$IDS" --ctx 64 --limit 2 --threads 8 2>&1 | grep -i "charg" | head -3 | sed 's/^/       /'
    exit 1
fi
n_constructions=$(env "$D" "$M" --ppl "$IDS" --ctx 64 --limit 2 --threads 8 2>&1 \
                    | grep -c "^\[push\]")
python3 - "$T_PARe" "$T_AVANCE" "$n_constructions" <<'PY' || exit 1
import sys
paresse, avance, n = float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
print(f"  chargement : paresseux {paresse:.2f} s · d'avance {avance:.2f} s "
      f"({avance / max(paresse, 1e-9):.1f}× plus rapide)")
if n != 0:
    sys.exit(f"  ❌ une passe --ppl a construit {n} forme(s) paresseuse(s) : la paresse ne sert à rien")
print("  ✅ aucune construction paresseuse sur une passe --ppl")
if avance / max(paresse, 1e-9) < 2.0:
    sys.exit(f"  ❌ le gain de chargement est sous le facteur 2 ({avance/paresse:.2f}×)")
print("  PORTE TENUE")
PY
