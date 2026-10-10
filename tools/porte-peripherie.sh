#!/bin/bash
# porte-peripherie.sh — C8, moitié PÉRIPHÉRIE : une entrée, une sortie, un délai.
#
# CE QUE LA CAPACITÉ DOIT FAIRE (docs/plan-cerveau-complet.md § C8, et la conception est dans
# docs/note-peripherie-c8.md) : des **régions frontière** — une entrée à horloge propre, un
# effecteur avec délai — et la métrique du projet, les **événements (paires) par décision**.
#
# Ce que cette porte verrouille :
#   1. **entrée constante ⇒ sortie constante**, au BIT PRÈS : deux exécutions identiques rendent
#      des fichiers identiques (`cmp`), et à gain nul tous les pas rendent le MÊME état ;
#   2. **le délai est réel** : les valeurs injectées sont décalées d'EXACTEMENT N pas (vérifié sur
#      le journal du moteur, pas sur une impression), et le délai change la sortie ;
#   3. **les refus sont explicites** (code 2) : type d'entrée inconnu, `--sortie` absente, canal
#      hors du modèle, jeton hors vocabulaire — un drapeau qui ne peut rien faire doit REFUSER ;
#   4. **la métrique du plan est calculée** : paires (poids × activation) par décision, et un
#      réflexe (`--couches 0:K`) en coûte MOINS qu'une passe complète — le prix du raccourci ;
#      la qualité du raccourci, elle, se mesure dans une fiche (`reports/rapport-c8-*.md`).
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
[ -s "$M" ] || { echo "  ❌ modèle absent : $M"; exit 2; }
[ -x "$D" ] || { echo "  ❌ binaire du moteur absent : $D"; exit 2; }
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT

# Un signal qui bouge (une marche montante), plus un commentaire et une ligne vide : les deux
# doivent être ignorés sans bruit.
printf '0.0\n1.0\n2.0\n3.0\n# ceci est un commentaire\n\n2.0\n1.0\n0.0\n' > "$T/signal.txt"

# stdout au silence : la porte ne garde que ce qu'elle vérifie (les lignes de configuration du
# moteur noyaient les cinq sections) ; stderr va dans le journal, où les valeurs injectées se lisent.
# stdout DANS UN FICHIER (et non /dev/null) : le résumé de la périphérie — dont l'annonce du
# tampon — sort sur stdout, tandis que les valeurs injectées sortent sur stderr. Les deux sont
# donc gardés, et chaque section lit celui qu'elle vérifie (premier essai : l'annonce cherchée
# dans stderr, donc introuvable).
run () { $D "$M" --entree "signal:$T/signal.txt" --sortie "$1" --ctx 8 --threads 8 "${@:2}" \
         > "$T/out.txt" 2> "$T/err.txt"; }

echo "=== 1. deux exécutions identiques ⇒ sortie identique AU BIT PRÈS ==="
run "$T/a.f32"; ca=$?
run "$T/b.f32"; cb=$?
[ "$ca" = 0 ] && [ "$cb" = 0 ] || { echo "  ❌ la périphérie n'a pas tourné (code $ca / $cb)"; tail -2 "$T/err.txt"; exit 1; }
cmp -s "$T/a.f32" "$T/b.f32" || { echo "  ❌ deux exécutions identiques donnent des sorties DIFFÉRENTES"; exit 1; }
taille=$(stat -c %s "$T/a.f32")
pas=$((taille / 4 / 896))
[ "$pas" = 7 ] || { echo "  ❌ 7 valeurs attendues (commentaire et ligne vide ignorés), $pas pas écrits"; exit 1; }
echo "  ✅ identiques au bit près · $pas pas · $taille octets"

echo "=== 2. entrée CONSTANTE ⇒ sortie CONSTANTE (gain nul : même état à tous les pas) ==="
run "$T/g0.f32" --entree-gain 0
python3 - "$T/g0.f32" <<'PY' || exit 1
import struct, sys
octets = open(sys.argv[1], "rb").read()
pas = len(octets) // 4 // 896
premier = octets[:896 * 4]
for i in range(1, pas):
    if octets[i * 896 * 4:(i + 1) * 896 * 4] != premier:
        sys.exit(f"  ❌ le pas {i} diffère du premier alors que l'entrée est constante")
print(f"  ✅ {pas} pas identiques : entrée constante ⇒ sortie constante")
PY

echo "=== 3. le DÉLAI décale les valeurs injectées d'exactement N pas ==="
run "$T/d3.f32" --delai 3
# Les valeurs injectées sont lues dans le journal du MOTEUR (`[peripherie] pas t : entrée v`),
# comparées au signal du fichier : c'est la seule façon de ne pas confondre « le délai change la
# sortie » (vrai même si le décalage est faux) avec « le délai vaut 3 ».
grep -oE "pas [0-9]+ : entrée [-0-9.e]+" "$T/err.txt" > "$T/injectees.txt"
python3 - "$T/injectees.txt" <<'PY' || exit 1
import re, sys
signal = [0.0, 1.0, 2.0, 3.0, 2.0, 1.0, 0.0]          # le fichier, commentaires retirés
lignes = open(sys.argv[1]).read().splitlines()
if len(lignes) != len(signal):
    sys.exit(f"  ❌ {len(lignes)} pas journalisés pour {len(signal)} valeurs")
for t, l in enumerate(lignes):
    v = float(re.search(r"entrée ([-0-9.e]+)", l).group(1))
    attendu = signal[t - 3] if t >= 3 else 0.0
    if abs(v - attendu) > 1e-6:
        sys.exit(f"  ❌ pas {t} : injecté {v}, attendu {attendu} (délai 3)")
print(f"  ✅ les {len(signal)} pas sont décalés de 3, valeurs vérifiées une à une")
PY
cmp -s "$T/a.f32" "$T/d3.f32" && { echo "  ❌ le délai ne change pas la sortie"; exit 1; }
echo "  ✅ et le délai change bien la sortie"

echo "=== 4. les refus sont explicites (code 2) ==="
refus () { # $1 = description, $@ = drapeaux
    local desc="$1"; shift
    $D "$M" "$@" --ctx 8 --threads 8 > "$T/refus.log" 2>&1
    local code=$?
    [ "$code" = 2 ] || { echo "  ❌ $desc : code $code au lieu de 2"; tail -2 "$T/refus.log"; exit 1; }
    grep -q "REFUS" "$T/refus.log" || { echo "  ❌ $desc : refuse sans le DIRE"; exit 1; }
    grep -q "Rien n'a été calculé\|REFUS" "$T/refus.log" || { echo "  ❌ $desc : refus muet"; exit 1; }
    echo "  ✅ $desc"
}
refus "type d'entrée inconnu (image:)"    --entree "image:$T/signal.txt" --sortie "$T/x.f32"
refus "sortie absente"                    --entree "signal:$T/signal.txt"
refus "canal hors du modèle"              --entree "signal:$T/signal.txt" --sortie "$T/x.f32" --entree-canal 99999
refus "jeton hors vocabulaire"            --entree "signal:$T/signal.txt" --sortie "$T/x.f32" --entree-jeton 999999999

echo "=== 4 bis. le TAMPON d'entrée : il change la sortie, et il refuse de déborder ==="
run "$T/m8.f32" --entree-memoire 8
grep -q "tampon d'entrée   : 8 pas" "$T/out.txt" || { echo "  ❌ le tampon n'est pas annoncé"; exit 1; }
cmp -s "$T/a.f32" "$T/m8.f32" && { echo "  ❌ --entree-memoire ne change pas la sortie"; exit 1; }
$D "$M" --entree "signal:$T/signal.txt" --sortie "$T/x.f32" --ctx 8 --threads 8 \
   --entree-canal 895 --entree-memoire 8 > "$T/refus.log" 2>&1
[ "$?" = 2 ] || { echo "  ❌ un tampon qui déborde du modèle devrait être refusé (code 2)"; exit 1; }
grep -q "REFUS" "$T/refus.log" || { echo "  ❌ débordement refusé sans le dire"; exit 1; }
echo "  ✅ le tampon change la sortie et refuse de déborder (canal 895 + 8 pas > 896)"

echo "=== 5. la métrique du plan : paires par DÉCISION, et le réflexe en coûte moins ==="
# UNE exécution par mesure, et on ne garde QUE la ligne de métrique : le premier essai
# concaténait deux exécutions et gardait tout — le python recevait « [config] cache KV… »
# au lieu d'un nombre (syntax error, pas un chiffre faux, mais un échec incompréhensible).
complet=$($D "$M" --entree "signal:$T/signal.txt" --sortie "$T/c.f32" --ctx 8 --threads 8 2>/dev/null \
          | grep -E "paires par pas" | grep -oE "[0-9.]+ M" | grep -oE "[0-9.]+")
reflexe=$($D "$M" --entree "signal:$T/signal.txt" --sortie "$T/r.f32" --ctx 8 --threads 8 \
          --couches 0:8 --tete-partielle 2>/dev/null \
          | grep -E "paires par pas" | grep -oE "[0-9.]+ M" | grep -oE "[0-9.]+")
echo "  passe complète : ${complet:-?} M paires par décision · réflexe 8/24 couches : ${reflexe:-?} M"
[ -n "$complet" ] && [ -n "$reflexe" ] || { echo "  ❌ la métrique n'est pas rendue"; exit 1; }
python3 -c "
import sys
c, r = float('$complet'), float('$reflexe')
if not (r < c * 0.8):
    sys.exit(f'  ❌ le réflexe ne coûte pas moins : {r} M contre {c} M par décision')
print(f'  ✅ le réflexe coûte {100*(1-r/c):.0f} % de moins par décision ({r} M contre {c} M)')
" || exit 1
echo
echo "PORTE TENUE : l'entrée est injectée, la sortie est écrite, le délai est exact, les refus sont"
echo "dits, et chaque décision a son prix en paires. Ce qui reste à mesurer n'est PAS ici : c'est"
echo "la QUALITÉ d'une tâche fermée (poursuite de consigne) et le compromis du réflexe — fiches C8."
