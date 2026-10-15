#!/bin/bash
# carte-facultes.sh — LE CERVEAU DRAVE, FACULTÉ PAR FACULTÉ, MESURÉ SUR PLACE.
#
# CE QUE C'EST, ET CE QUE CE N'EST PAS. Ce n'est pas une porte : elle ne juge pas, elle
# **montre**. C'est la forme exécutable de `docs/cerveau-facultes.md` — pour chaque faculté, la
# commande qui l'exerce **maintenant**, le chiffre qu'elle rend, et son coût. Une carte périmée
# est pire qu'une carte absente : c'est pourquoi chaque ligne est **mesurée à l'exécution** et non
# recopiée d'une fiche. Les facultés qui demandent deux nœuds (trace globale, budgets) ou un
# entraînement (réflexe entraîné, mémoire de travail du modèle) sont **citées** avec leur chiffre
# et leur fiche — elles ne sont pas rejouables en trois minutes, et le dire vaut mieux que de les
# simuler.
#
# Usage : tools/carte-facultes.sh [--limite 256]
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
LIMITE=${LIMITE:-256}
[ -s "$M" ] || { echo "  ❌ modèle absent : $M"; exit 2; }
[ -x "$D" ] || { echo "  ❌ binaire du moteur absent : $D"; exit 2; }
. tools/_corpus.sh
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
python3 - "$IDS" "$T/morceau.txt" "$LIMITE" <<'PY'
import pathlib, re, sys
ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(sys.argv[1]).read_text()) if x.strip()]
pathlib.Path(sys.argv[2]).write_text(",".join(str(x) for x in ids[:int(sys.argv[3])]))
PY
ppl() { "$D" "$M" --ppl "$T/morceau.txt" --limit "$LIMITE" --ctx "$LIMITE" --threads 8 "$@" 2>&1 \
        | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+" | head -1; }

echo "carte des facultés — $(basename "$M") · $LIMITE jetons · $(date '+%H:%M')"
echo

# ---- 1. PERCEPTION (périphérie) : une entrée, une sortie, un délai
python3 -c "
import numpy as np
np.sin(np.linspace(0, 6.28, 8)).astype('<f4').tofile('$T/signal.f32')"
peri() { "$D" "$M" --entree "signal:$T/signal.f32" --sortie "$1" --ctx 8 --threads 8 "${@:2}" \
         >/dev/null 2>&1; }
peri "$T/a.f32"; peri "$T/b.f32"
if cmp -s "$T/a.f32" "$T/b.f32"; then det="identiques au bit près"; else det="DIFFÉRENTES"; fi
peri "$T/d2.f32" --delai 2
echo "1. PERCEPTION      entrée signal (8 pas) : deux exécutions $det · délai 2 appliqué ($(stat -c%s "$T/d2.f32") octets)"
echo "                   coût : 0 paire de plus (l'entrée est posée, pas calculée)"
echo

# ---- 2. MÉMOIRE DE TRAVAIL : le tampon exact du moteur
peri "$T/sans.f32"
peri "$T/memoire.f32" --entree-memoire 8
if cmp -s "$T/sans.f32" "$T/memoire.f32"; then mem="INERTE"; else mem="change la sortie"; fi
echo "2. MÉMOIRE DE TRAVAIL  tampon de 8 pas (--entree-memoire 8) : $mem"
echo "                   R² 1,000 sur v[t−8] (moteur, mesure du 13/10) pour 0 paire de plus"
echo

# ---- 3. RÉFLEXES : le chemin court, et son prix
p_plein=$(ppl "")
p_court=$(ppl --couches 0:8 --tete-partielle)
echo "3. RÉFLEXES        complet $p_plein · chemin court 8 couches (tête empruntée) $p_court"
echo "                   tête entraînée : ÷1,47 (m32) et ÷1,24 (m20) mesurés par le MOTEUR — rapport-n4-porte-execution.md"
echo

# ---- 4. ATTENTION SÉLECTIVE : la fenêtre et le drain
p_fenetre=$(ppl --attn-window 64 --attn-sinks 64)
echo "4. ATTENTION       fenêtre 64 + 64 puits : $p_fenetre contre $p_plein (complet)"
echo "                   la moitié des clés coûte +0,4 à +3,0 % selon le texte — rapport-loi-frontiere-fenetre.md"
echo

# ---- 5. MÉMOIRE ÉPISODIQUE : écriture, relecture, séparation
epi=$("$D" "$M" --episodique-essai 300 --episodique-k 64 --ids-file "$IDS" --ctx 512 --threads 8 2>&1 \
      | grep -E "round-trip|séparation|nouveauté" | tr '\n' ' ' | sed 's/  */ /g')
echo "5. ÉPISODIQUE      ${epi:-essai non lisible}"
echo

# ---- 6. CONSOLIDATION : l'invariant du taux nul (bit à bit)
if [ -d "$HOME/IA/cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct" ]; then
    SNAP=$(ls -d "$HOME/IA/cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct"/snapshots/* | head -1)
    PY=/home/stephane/gpu-env/bin/python
    $PY -c "
import torch
torch.save({'lora': []}, '$T/nul.pt')" 2>/dev/null
    $PY tools/exporter_gguf_dense.py --hf "$SNAP" --sortie "$T/base.gguf" >/dev/null 2>&1
    $PY tools/exporter_gguf_dense.py --hf "$SNAP" --lora "$T/nul.pt" --sortie "$T/nul.gguf" >/dev/null 2>&1
    if cmp -s "$T/base.gguf" "$T/nul.gguf"; then cons="identique au bit"; else cons="DIFFÉRENT"; fi
    echo "6. CONSOLIDATION   LoRA nul fusionné ⇒ GGUF $cons (l'invariant du plan C7)"
else
    echo "6. CONSOLIDATION   (poids PyTorch absents : invariant non rejoué)"
fi
echo "                   −16,4 % en domaine, +1,3 % hors domaine — rapport-consolidation-c7.md"
echo

# ---- 7. CYCLES : un pas exact, puis la divergence
if [ -f /tmp/c2/cycle.json ]; then
    $PY tools/derouler.py --topologie /tmp/c2/cycle.json --pas-temps 1 --morceau "$T/morceau.txt" \
        --limite 128 --sortie "$T/cyc" --moteur "$D" --modele "$M" > "$T/cyc.log" 2>&1
    pas1=$(grep -oE "perplexité [0-9.,]+" "$T/cyc.log" | head -1 | grep -oE "[0-9.]+")
    ref=$("$D" "$M" --ppl "$T/morceau.txt" --limit 128 --ctx 128 --threads 8 2>&1 \
          | grep -oE "perplexité [0-9.]+" | grep -oE "[0-9.]+")
    echo "7. CYCLES          pas 1 du graphe récurrent $pas1 · chaîne (référence) $ref"
    echo "                   non entraîné, la boucle diverge : 14,65 → 2 988 en 4 pas — rapport-cycle-c2.md"
else
    echo "7. CYCLES          (topologie de test absente : /tmp/c2/cycle.json)"
fi
echo

# ---- 8. LANGAGE : décoder
gen=$("$D" "$M" --infer --prompt "Le ciel est bleu parce que" --n 8 --ctx 64 --threads 8 --temp 0 2>&1 \
      | grep -oE "ids générés : \[[0-9, ]*\]" | head -1)
echo "8. LANGAGE         ${gen:-génération non lisible}"
echo

echo "CITÉES (non rejouables en trois minutes, chiffres et fiches dans docs/cerveau-facultes.md) :"
echo "  • latéralité      échange exact, gain NUL (36,1307 = 36,1307)      porte-jumeaux.sh"
echo "  • inhibition E/I  gain 0,75 ⇒ −11,5 % ; l'inhibition dégrade       rapport-e4-ratio-signes.md"
echo "  • modulation      canal neutre ⇒ identique ; aucun signal n'améliore porte-bus.sh"
echo "  • délais/réseau   +3,1 s pour 50 ms × 64 pas, perplexité inchangée porte-delais.sh"
echo "  • budgets         trois refus distincts : octets 6, latence 8, paires 9  porte-budget.sh"
echo "  • trace globale   126 croisements, 1 bit ⇒ DIVERGENT (code 3)      porte-trace.sh"
echo "  • règle locale    la meilleure des cinq est « ne rien faire »      rapport-e1-e2-connectome-croissance.md"
exit 0
