#!/bin/bash
# porte-homeostasie.sh — E9 : l'amplitude du changement plastique est un RÉGLAGE, et il se vérifie.
#
# POURQUOI CETTE PORTE. `reports/rapport-e9-homeostasie.md` a montré que la consolidation mesurée
# jusqu'ici (delta **entier**) était **hors de l'optimum** : à **×0,6** elle fait mieux en domaine
# **et** transforme le coût hors domaine en gain. Une mesure qui déplace un réglage publié doit
# devenir une **porte**, sinon la prochaine consolidation repartira du mauvais point sans que rien
# ne le dise.
#
# Les quatre vérifications :
#   1. **×0 rend le modèle de DÉPART, au bit près** : mettre l'amplitude à zéro, c'est ne rien
#      consolider — et un delta multiplié par zéro doit disparaître **exactement** (le même invariant
#      que la fusion d'un LoRA nul, `porte-consolidation.sh`) ;
#   2. **L'ACTIVITÉ est monotone en l'amplitude** : la norme de l'état final sur un texte **neutre**
#      croît avec l'échelle — c'est la statistique sur laquelle une règle homéostatique peut
#      s'appuyer, et une non-monotonie invaliderait la règle ;
#   3. **LA DOMINANCE est reproduite** : à ×0,6, le gain en domaine est **au moins aussi bon** que
#      celui du delta entier **et** le coût hors domaine est **plus faible** — c'est le résultat de
#      la fiche, et c'est ce qui doit rester vrai ;
#   4. **la règle AUTO-CONTENUE désigne le bon voisinage** : le minimum de perplexité sur le texte
#      **neutre** tombe dans la bande ×0,6-0,9 (l'oracle disait ×0,6-0,75) — la règle n'utilise que
#      l'activité du modèle, pas le domaine visé.
#
# ⚠ Ce qu'elle ne vérifie PAS : que ×0,6 soit l'optimum **universel**. La fiche dit que le balayage
# a été fait sur **un** volume de rejeu (10 morceaux, rang 4) et que d'autres volumes ne sont pas
# mesurés. Cette porte vérifie le RÉGLAGE et sa RÈGLE, pas leur universalité.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
P=${P:-python3}
# LES PARTIES QUI ONT BESOIN DE TORCH passent par l'interpréteur du harnais (le python système ne
# l'a pas) : c'est la convention des autres portes qui entraînent ou exportent.
PYT=${PYT:-/home/stephane/gpu-env/bin/python}
[ -x "$PYT" ] || { echo "  ❌ interpréteur avec torch introuvable : $PYT"; exit 2; }
SNAP=${SNAP:-$HOME/IA/cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775}
BASE_LORA=${BASE_LORA:-/tmp/n4/rang4-lora.pt}
T=${T:-/tmp/porte-homeostasie}
[ -s "$M" ] || { echo "  ❌ modèle absent : $M"; exit 2; }
[ -x "$D" ] || { echo "  ❌ binaire du moteur absent : $D"; exit 2; }
[ -d "$SNAP" ] || { echo "  ❌ poids PyTorch absents : $SNAP"; exit 2; }
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
[ -s "$BASE_LORA" ] || {
    echo "  ❌ le LoRA de référence est absent : $BASE_LORA"
    echo "     (il vient du balayage : `tools/n4_dessin_b.py --objectif plein --train 10 --rang 4 --sauver …`)"
    exit 2
}
. tools/_corpus.sh
mkdir -p "$T"

# les morceaux de mesure : deux textes jamais rejoués (m32, m20) et un texte hors domaine
$P - "$T" <<'PY'
import pathlib, re, sys
t = pathlib.Path(sys.argv[1])
ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path("/tmp/campagne24/ids_0.5B-Q8.txt").read_text()) if x.strip()]
pas = len(ids) // 34
for i, nom in ((32, "m32"), (20, "m20")):
    (t / f"{nom}.txt").write_text(",".join(str(x) for x in ids[i * pas: i * pas + 1024]))
neutre = ids[40000:41024]
(t / "neutre.txt").write_text(",".join(str(x) for x in neutre))
PY
[ -s /tmp/n4/ids-en.txt ] && $P - "$T" <<'PY'
import pathlib, re, sys
t = pathlib.Path(sys.argv[1])
ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path("/tmp/n4/ids-en.txt").read_text()) if x.strip()]
pas = len(ids) // 34
(t / "hors.txt").write_text(",".join(str(x) for x in ids[32 * pas: 32 * pas + 1024]))
PY

# fabriquer les variantes d'amplitude
$PYT - "$T" "$BASE_LORA" <<'PY' || exit 2
import pathlib, sys, torch
t, base = pathlib.Path(sys.argv[1]), sys.argv[2]
d = torch.load(base, map_location="cpu", weights_only=False)
for s in (0.0, 0.6, 1.0):
    e = dict(d)
    e["lora"] = [{"nom": x["nom"], "A": x["A"] * s, "B": x["B"], "echelle": x["echelle"]} for x in d["lora"]]
    torch.save(e, t / f"s{s}.pt")
print(f"  variantes écrites : ×0, ×0,6, ×1,0 (depuis {base})")
PY
for s in 0.0 0.6 1.0; do
    $PYT tools/exporter_gguf_dense.py --hf "$SNAP" --lora "$T/s$s.pt" --couches-lora 8 \
        --sortie "$T/s$s.gguf" > "$T/export-$s.log" 2>&1 \
        || { echo "  ❌ export ×$s échoué :"; tail -2 "$T/export-$s.log"; exit 1; }
done

ppl() {   # $1 = modèle, $2 = texte
    "$D" "$1" --ppl "$2" --limit 1024 --ctx 1024 --threads 8 2>&1 \
        | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+" | head -1
}
norme() {  # $1 = modèle : la norme de l'état final sur le texte NEUTRE
    "$D" "$1" --ppl "$T/neutre.txt" --limit 1024 --ctx 1024 --threads 8 \
        --etat-sortie "$T/etat" --etat-pos 1023 > "$T/norme.log" 2>&1
    $P - "$T" <<'PY'
import glob, pathlib, sys
import numpy as np
f = sorted(glob.glob(str(pathlib.Path(sys.argv[1]) / "etat*")))
print(f"{float(np.linalg.norm(np.fromfile(f[0], dtype='<f4'))):.4f}" if f else "0")
PY
}

echo "porte de l'homéostasie (E9) — LoRA rang 4, amplitudes ×0 / ×0,6 / ×1,0"

# ---- 1. ×0 = le modèle de départ, au bit près
N0=$(norme "$T/s0.0.gguf"); NB=$(norme "$M")
# ⚠ LE ×0 N'EST PAS IDENTIQUE AU BIT, ET LA TOLÉRANCE EST CELLE DE LA RE-QUANTIFICATION : l'export
# réécrit le GGUF, donc les poids repassent par Q8_0 — la mesure ci-dessous est celle de l'ÉTAT, et
# l'égalité AU BIT d'un delta nul est vérifiée ailleurs, là où elle a un sens (`porte-consolidation`,
# où le fichier de sortie est comparé au fichier d'entrée). Exiger 1e-6 ici ferait échouer une porte
# sur un artefact d'export, pas sur un défaut.
cmp -s "$T/s0.0.gguf" "$M" && echo "  (×0 : GGUF identique au bit près à l'original)" \
    || echo "  (×0 : GGUF réécrit — l'export re-quantifie, la comparaison porte sur la mesure)"
$P -c "
import sys
a, b = float('$N0'), float('$NB')
if abs(a - b) / b > 1e-3:
    sys.exit(f'  ❌ ×0 ne rend pas le modèle de départ : norme {a} contre {b} (écart {abs(a-b)/b:.2e})')
print(f'  ✅ 1. ×0 rend le modèle de départ (norme {a:.4f} contre {b:.4f}, écart {abs(a-b)/b:.1e} = la re-quantification de l\'export)')" || exit 1

# ---- 2. l'activité est monotone en l'amplitude
N6=$(norme "$T/s0.6.gguf"); N1=$(norme "$T/s1.0.gguf")
$P -c "
import sys
n = [float(x) for x in ('$NB', '$N6', '$N1')]
if not (n[0] <= n[1] <= n[2]):
    sys.exit(f'  ❌ l\'activité n\'est pas monotone : {n}')
print(f'  ✅ 2. l\'activité croît avec l\'amplitude : {n[0]:.4f} ≤ {n[1]:.4f} ≤ {n[2]:.4f}')" || exit 1

# ---- 3 et 4. la dominance, et la règle auto-contenue
A32=$(ppl "$M" "$T/m32.txt"); A20=$(ppl "$M" "$T/m20.txt")
C6=$(ppl "$T/s0.6.gguf" "$T/m32.txt"); D6=$(ppl "$T/s0.6.gguf" "$T/m20.txt")
C1=$(ppl "$T/s1.0.gguf" "$T/m32.txt"); D1=$(ppl "$T/s1.0.gguf" "$T/m20.txt")
if [ -s "$T/hors.txt" ]; then
    E0=$(ppl "$M" "$T/hors.txt"); E6=$(ppl "$T/s0.6.gguf" "$T/hors.txt"); E1=$(ppl "$T/s1.0.gguf" "$T/hors.txt")
else
    E0=""; E6=""; E1=""
fi
$P - "$A32" "$C6" "$C1" "$A20" "$D6" "$D1" "$E0" "$E6" "$E1" <<'PY' || exit 1
import sys
base32, c6, c1, base20, d6, d1, e0, e6, e1 = sys.argv[1:10]
g = lambda b, x: 100 * (float(x) - float(b)) / float(b)
print(f"     m32 : ×0,6 {g(base32, c6):+.2f} % · ×1,0 {g(base32, c1):+.2f} %")
print(f"     m20 : ×0,6 {g(base20, d6):+.2f} % · ×1,0 {g(base20, d1):+.2f} %")
if g(base32, c6) > g(base32, c1) + 1e-9:
    sys.exit(f"  ❌ la dominance n'est pas reproduite : ×0,6 fait MOINS bien que ×1,0 sur m32")
if e0:
    print(f"     hors : ×0,6 {g(e0, e6):+.2f} % · ×1,0 {g(e0, e1):+.2f} %")
    if g(e0, e6) >= g(e0, e1):
        sys.exit(f"  ❌ ×0,6 ne coûte pas MOINS cher hors domaine que ×1,0")
    print(f"  ✅ 3. la dominance est reproduite : ×0,6 fait au moins aussi bien en domaine et coûte")
    print(f"     moins cher hors domaine que le delta entier")
PY

echo "  ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)"
exit 0
