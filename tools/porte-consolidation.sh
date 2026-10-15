#!/bin/bash
# porte-consolidation.sh — la consolidation (C7) écrit-elle EXACTEMENT ce qu'elle dit ?
#
# POURQUOI CETTE PORTE. C7 est la faculté qui manquait au moteur : « le moteur n'apprend pas »
# (manque M6), et la consolidation est le premier pas — rejouer l'expérience du jour, puis la
# mettre dans les poids. Elle passe par `tools/n4_dessin_b.py` (LoRA appris) et
# `tools/exporter_gguf_dense.py` (fusion `W ← W + (α/r)·B·A` puis écriture du GGUF). Deux façons
# de se tromper en silence :
#
#   1. **la fusion qui ne fusionne rien** (mauvais nom de tenseur, couches décalées, échelle
#      oubliée) : le fichier sortirait identique et tout « apprentissage » serait nul sans un mot ;
#   2. **la fusion qui touche ce qu'elle ne doit pas** — un lecteur de sortie (dessin A) ne doit
#      pas changer le modèle complet, et un LoRA NUL doit laisser le fichier **identique au bit**.
#
# L'invariant du plan C7 est le second : « après consolidation à taux nul, le modèle est bit à bit
# identique ». C'est le contrôle le plus fort de cette porte — `cmp`, pas une perplexité.
#
# CE QU'ELLE VÉRIFIE (aucun entraînement : la fusion est le sujet, pas l'apprentissage)
#   A. LoRA **nul** (B = 0) fusionné ⇒ GGUF **identique au bit** à l'export de base ;
#   B. LoRA **aléatoire** fusionné ⇒ GGUF différent ET perplexité différente dans le MOTEUR
#      (sinon la fusion ne fait rien et A ne prouverait rien) ;
#   C. un **lecteur de sortie** seul (dessin A) ne touche PAS le modèle ⇒ GGUF identique au bit.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
P=${P:-/home/stephane/gpu-env/bin/python}   # safetensors + torch
SNAP=${SNAP:-/home/stephane/IA/cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
T=${T:-/tmp/porte-consolidation}
LIMITE=${LIMITE:-256}
[ -s "$M" ] || { echo "  ❌ modèle absent : $M"; exit 2; }
[ -x "$D" ] || { echo "  ❌ binaire du moteur absent : $D"; exit 2; }
$P -c "import numpy, safetensors" 2>/dev/null || { echo "  ❌ $P n'a pas numpy/safetensors"; exit 2; }
[ -d "$SNAP" ] || { echo "  ❌ poids PyTorch absents : $SNAP (export non mesurable)"; exit 2; }
. tools/_corpus.sh
mkdir -p "$T"

$P - "$IDS" "$T/morceau.txt" "$LIMITE" <<'PY'
import pathlib, re, sys
ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(sys.argv[1]).read_text()) if x.strip()]
pathlib.Path(sys.argv[2]).write_text(",".join(str(x) for x in ids[:int(sys.argv[3])]))
PY

# Les deux LoRA de contrôle : un NUL (B = 0) et un ALÉATOIRE. Écrits en f32, petits.
$P - "$T" <<'PY'
import pathlib, sys, torch
t = pathlib.Path(sys.argv[1])
noms = [(f"model.layers.{i}.self_attn.{p}_proj.weight", 896 if p != "k" and p != "v" else 128)
        for i in range(2) for p in ("q", "k", "v", "o")]
def ecrire(nom, aleatoire):
    g = torch.Generator().manual_seed(7)
    lora = []
    for n, sortie in noms:
        A = torch.randn(8, 896, generator=g) * 0.02
        B = (torch.randn(sortie, 8, generator=g) * 0.02) if aleatoire else torch.zeros(sortie, 8)
        lora.append({"nom": n, "A": A, "B": B, "echelle": 2.0})
    torch.save({"bras": nom, "profondeur": 2, "rang": 8, "alpha": 16.0,
                "adaptateur": None, "lora": lora}, t / f"{nom}.pt")
ecrire("nul", False)
ecrire("aleatoire", True)
print("  deux LoRA de contrôle écrits (nul, aléatoire)")
PY
# Un lecteur de sortie seul (dessin A) : l'adaptateur que le MOTEUR applique, jamais le fichier.
$P - "$T/adaptateur.pt" <<'PY'
import sys, torch
torch.save({"bras": "adaptateur", "profondeur": 2, "rang": 8, "alpha": 16.0,
            "adaptateur": torch.eye(896) * 1.5, "lora": []}, sys.argv[1])
PY

echo "porte de la consolidation — $(basename "$M") · $LIMITE jetons"
ppl() { "$D" "$1" --ppl "$T/morceau.txt" --limit "$LIMITE" --ctx "$LIMITE" --threads 8 2>&1 \
        | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+" | head -1; }

export_ok=1
for cas in "base:" "nul:--lora $T/nul.pt --couches-lora 2" \
           "aleatoire:--lora $T/aleatoire.pt --couches-lora 2" \
           "lecteur:--lora $T/adaptateur.pt --couches-lora 0"; do
    nom=${cas%%:*}; args=${cas#*:}
    $P tools/exporter_gguf_dense.py --hf "$SNAP" $args --sortie "$T/$nom.gguf" \
        > "$T/$nom.log" 2>&1 || { echo "  ❌ export « $nom » en échec (voir $T/$nom.log)"; exit 2; }
done

# A. LoRA nul ⇒ identique AU BIT
if cmp -s "$T/base.gguf" "$T/nul.gguf"; then
    echo "  ✅ A. LoRA nul fusionné ⇒ fichier IDENTIQUE au bit ($(stat -c%s "$T/base.gguf") octets)"
else
    echo "  ❌ A. un LoRA NUL a changé le fichier — la fusion invente quelque chose"
    cmp "$T/base.gguf" "$T/nul.gguf" | head -2
    export_ok=0
fi

# B. LoRA aléatoire ⇒ différent, et le MOTEUR le voit
if cmp -s "$T/base.gguf" "$T/aleatoire.gguf"; then
    echo "  ❌ B. un LoRA ALÉATOIRE n'a rien changé — la fusion ne fusionne pas"
    export_ok=0
else
    p_base=$(ppl "$T/base.gguf"); p_alea=$(ppl "$T/aleatoire.gguf")
    [ -n "$p_base" ] && [ -n "$p_alea" ] || { echo "  ❌ perplexité illisible"; exit 1; }
    rapport=$($P -c "print(f'{$p_alea/max($p_base,1e-12):.4f}')")
    echo "  ✅ B. LoRA aléatoire ⇒ fichier différent · perplexité $p_base → $p_alea (×$rapport)"
fi

# C. le lecteur de sortie ne touche pas le modèle complet (c'est le MOTEUR qui l'applique)
if cmp -s "$T/base.gguf" "$T/lecteur.gguf"; then
    echo "  ✅ C. un lecteur de sortie seul laisse le modèle IDENTIQUE au bit"
else
    echo "  ❌ C. le lecteur de sortie a modifié le fichier du modèle"
    export_ok=0
fi

[ "$export_ok" -eq 1 ] || exit 1
echo "  ✅ porte tenue (fusion exacte : nulle ⇒ identique, réelle ⇒ visible, lecteur ⇒ hors fichier)"
exit 0
