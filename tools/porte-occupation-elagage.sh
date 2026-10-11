#!/bin/bash
# porte-occupation-elagage.sh — le fichier porte-t-il l'élagage qu'il ANNONCE ?
#
# CE QUE LA PORTE VERROUILLE, et pourquoi :
#   1. **l'occupation du fichier exporté correspond à la cible annoncée** — un modèle entraîné avec
#      `--elagage 0.25` doit stocker ~25 % de poids non nuls, pas 78 %. C'est le défaut trouvé le
#      11/10 : la sélection du **meilleur point** de validation restaurait un pas où la rampe
#      d'élagage ne gardait encore que 78 % des poids, et le fichier était publié comme « 25 % de
#      poids gardés ». La conclusion d'E6 s'en trouvait **inversée** ;
#   2. **le harnais l'ANNONCE** (`# élagage FINAL réappliqué…`) : une correction silencieuse serait
#      un autre défaut qui attend ;
#   3. **la porte a été vue ROUGE** avec l'ancien comportement rallumé
#      (`DRAVE_SANS_ELAGAGE_FINAL=1`) — sans quoi elle ne prouverait rien.
#
# CE QU'ELLE NE VERROUILLE PAS : la *qualité* du modèle élagué (c'est E6, et c'est un autre
# protocole), ni le coût en paires — le compteur du moteur ne voit pas l'occupation (manque M9).
set -u
cd "$(dirname "$0")/.."
P=${P:-/home/stephane/gpu-env/bin/python}
T=${TRAVAIL:-/tmp/porte-occupation}
PAS=${PAS:-600}
CIBLE=${CIBLE:-0.25}
TEXTE=${TEXTE:-data/wikitext2_test.txt}
DELAI=${DELAI:-1200}

for f in "$TEXTE" data/corpus_en.txt data/corpus_en_val.txt; do
    [ -s "$f" ] || { echo "  ❌ $f manquant : cette porte entraîne un petit modèle"; exit 2; }
done
$P -c "import torch, transformers" 2>/dev/null || { echo "  ❌ $P n'a pas torch/transformers"; exit 2; }
rm -rf "$T"; mkdir -p "$T"

echo "=== 1. entraîner avec --elagage $CIBLE (le meilleur point est choisi AVANT la rampe) ==="
timeout "$DELAI" $P -u tools/entrainer_moteur.py --famille route --dim 192 --couches 4 --tetes 4 \
    --cache 768 --experts 8 --k 2 --seq 128 --lot 32 --lr 3e-4 --graine 1 --pas "$PAS" \
    --eval-tous 200 --elagage-tous 200 --elagage "$CIBLE" --sortie "$T/modele" \
    > "$T/entrainement.log" 2>&1
CODE=$?
[ "$CODE" = 0 ] || { echo "  ❌ l'entraînement a échoué (code $CODE)"; tail -8 "$T/entrainement.log" | sed 's/^/    /'; exit 1; }
grep -E "meilleur point|élagage FINAL" "$T/entrainement.log" | sed 's/^/  /'
echo
echo "=== 2. exporter, puis LIRE l'occupation dans le fichier ==="
timeout "$DELAI" $P tools/exporter_gguf.py --hf "$T/modele" --sortie "$T/modele.gguf" \
    > "$T/export.log" 2>&1 || { echo "  ❌ l'export a échoué"; tail -5 "$T/export.log" | sed 's/^/    /'; exit 1; }
$P tools/occupation_poids.py --modele "$T/modele.gguf" | sed -n '3,12p' | sed 's/^/  /'
OCC=$($P tools/occupation_poids.py --modele "$T/modele.gguf" \
      | grep -E "^\| \*\*total" | grep -oE "[0-9.]+ %" | tr -d ' %')

echo
echo "=== 3. le verrou ==="
$P - "$OCC" "$CIBLE" <<'PY'
import sys
occ, cible = float(sys.argv[1]) / 100.0, float(sys.argv[2])
# On tolère un peu AU-DESSUS de la cible (le plancher des poids log-normaux, la quantification qui
# ne met pas tout à zéro) mais PAS un écart du type « 78 % au lieu de 25 % ».
plafond = cible + 0.10
print(f"  occupation lue : {occ:.1%} · cible annoncée : {cible:.0%} · plafond toléré : {plafond:.0%}")
if occ > plafond:
    print(f"  ❌ le fichier stocke {occ:.1%} de poids non nuls pour une cible de {cible:.0%} :")
    print("     il porte l'élagage de la RAMPE au pas du meilleur point, pas la cible (défaut du 11/10)")
    sys.exit(1)
if occ < cible - 0.05:
    print(f"  ⚠ occupation {occ:.1%} très en dessous de la cible {cible:.0%} : à regarder")
print(f"  ✅ le fichier porte bien l'élagage annoncé ({occ:.1%} pour {cible:.0%} demandés)")
PY
CODE=$?
[ "$CODE" = 0 ] || exit "$CODE"

# L'ANNONCE VIENT APRÈS LA MESURE : c'est l'OCCUPATION qui doit parler la première, sinon un
# rouge s'arrête sur une ligne de journal manquante au lieu de montrer le défaut lui-même.
if ! grep -q "élagage FINAL" "$T/entrainement.log"; then
    echo "  ❌ le harnais n'annonce PAS l'élagage final : le fichier pourrait porter celui de la"
    echo "     rampe sans que rien ne le dise"
    exit 1
fi
echo "  ✅ le harnais annonce l'élagage final (pas de correction silencieuse)"

echo
echo "✅ porte occupation × élagage : la cible annoncée est VÉRIFIÉE dans le fichier exporté"
echo "   (et le harnais annonce l'élagage final — vu ROUGE avec DRAVE_SANS_ELAGAGE_FINAL=1)."
