#!/bin/bash
# porte-recurrence.sh — C2 : la région consomme sa PROPRE sortie du pas précédent.
#
# CE QUE LE PLAN DEMANDE (docs/plan-cerveau-complet.md § C2) : « une région peut consommer sa
# propre sortie du pas précédent (état explicite par région) », interface `recurrent: true`. Le
# validateur de topologie **refuse encore un cycle** dans un graphe ; la boucle est donc
# implémentée là où elle est mesurable : dans la région frontière, avec un poids DÉCLARÉ
# (`--recurrence α` : x0(t) += α · h(t−1)).
#
# Ce que la porte verrouille :
#   1. **α = 0 laisse le calcul EXACTEMENT comme sans le drapeau** (au bit près) : le zéro est
#      exprimable — leçon `--attn-sinks`, appliquée d'avance ;
#   2. **la boucle est réelle et déterministe** : α > 0 change la sortie, et deux exécutions
#      identiques rendent des fichiers identiques au bit près ;
#   3. **elle ne coûte AUCUNE paire** : la rétroaction ne traverse aucune couche de plus — les
#      paires par décision sont identiques avec et sans.
#   4. **les bornes sont explicites** : α négatif ou absurde est REFUSÉ (code 2) — une récurrence
#      qui ne converge pas ne doit pas rendre un chiffre.
#
# CE QUE LA PORTE NE VERROUILLE PAS, et qui est mesuré dans la fiche
# (`reports/rapport-c2-recurrence.md`) : **la boucle DÉGRADE la lisibilité du signal** — le
# présent passe de R² 0,906 à 0,112 (α = 0,5) et le passé de −0,35 à −4,87 (α = 1,0). La porte
# vérifie que la boucle existe et qu'elle est bornée ; elle ne prétend pas qu'elle aide.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
NPAS=${NPAS:-32}
[ -s "$M" ] || { echo "  ❌ modèle absent : $M"; exit 2; }
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
python3 - "$T" "$NPAS" <<'PY'
import pathlib, sys
t, n = pathlib.Path(sys.argv[1]), int(sys.argv[2])
import random
random.seed(9)
(t / "sig.txt").write_text("\n".join(f"{random.uniform(-2, 2):.9g}" for _ in range(n)))
PY
run () { $D "$M" --entree "signal:$T/sig.txt" --ctx 8 --threads 8 "$@" > "$T/out.txt" 2> "$T/err.txt"; }

echo "=== 1. α = 0 EST l'absence de récurrence (au bit près) ==="
run --sortie "$T/none.f32"; c1=$?
run --sortie "$T/zero.f32" --recurrence 0; c2=$?
[ "$c1" = 0 ] && [ "$c2" = 0 ] || { echo "  ❌ la périphérie n'a pas tourné"; tail -2 "$T/err.txt"; exit 1; }
cmp -s "$T/none.f32" "$T/zero.f32" || { echo "  ❌ --recurrence 0 diffère de l'absence du drapeau"; exit 1; }
echo "  ✅ identiques : le zéro est exprimable"

echo "=== 2. la boucle est réelle et DÉTERMINISTE ==="
run --sortie "$T/a.f32" --recurrence 0.5
run --sortie "$T/b.f32" --recurrence 0.5
cmp -s "$T/a.f32" "$T/b.f32" || { echo "  ❌ deux exécutions identiques diffèrent (la boucle n'est pas déterministe)"; exit 1; }
cmp -s "$T/none.f32" "$T/a.f32" && { echo "  ❌ --recurrence 0.5 ne change rien : la boucle n'existe pas"; exit 1; }
echo "  ✅ la boucle change la sortie, et deux exécutions identiques sont identiques"

echo "=== 3. elle ne coûte aucune paire ==="
P1=$(grep -oE "paires par pas *: [0-9.]+ M" "$T/out.txt" | grep -oE "[0-9.]+")
run --sortie "$T/c.f32"
P2=$(grep -oE "paires par pas *: [0-9.]+ M" "$T/out.txt" | grep -oE "[0-9.]+")
printf '  avec récurrence %s M · sans %s M\n' "${P1:-?}" "${P2:-?}"
[ -n "$P1" ] && [ "$P1" = "$P2" ] || { echo "  ❌ la récurrence change le coût en paires"; exit 1; }
echo "  ✅ mêmes paires : la rétroaction ne traverse aucune couche de plus"

echo "=== 4. les bornes sont explicites (code 2) ==="
for A in -1 100; do
    $D "$M" --entree "signal:$T/sig.txt" --sortie "$T/x.f32" --ctx 8 --threads 8 --recurrence "$A" \
       > "$T/ref.log" 2>&1
    c=$?
    [ "$c" = 2 ] || { echo "  ❌ --recurrence $A : code $c au lieu de 2"; exit 1; }
    grep -q "REFUS" "$T/ref.log" || { echo "  ❌ --recurrence $A refusé sans le dire"; exit 1; }
    echo "  ✅ --recurrence $A refusé et expliqué"
done
echo
echo "PORTE TENUE : la boucle existe, elle est déterministe, elle ne coûte aucune paire, son zéro"
echo "est exprimable et ses bornes sont refusées. Ce qu'elle FAIT à la lisibilité (elle la dégrade :"
echo "présent 0,906 → 0,112) est mesuré dans reports/rapport-c2-recurrence.md — la porte ne le"
echo "cache pas, elle ne le prétend pas non plus."
