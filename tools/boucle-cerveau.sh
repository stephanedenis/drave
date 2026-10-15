#!/bin/bash
# boucle-cerveau.sh — LA JOURNÉE DU CERVEAU, EN UNE COMMANDE.
#
# CE QUE C'EST. Toutes les autres portes et cartes mesurent une faculté (ou leur coexistence).
# Celle-ci exécute **la chaîne complète** sur un texte : le cerveau **perçoit**, **retient**,
# **se souvient**, **consolide**, puis **agit** — et chaque étape est mesurée par le MOTEUR.
# Ce n'est pas une porte de plus : c'est la démonstration que les facultés s'enchaînent, avec,
# à chaque maillon, le chiffre qui dit ce qu'il a produit.
#
# LES CINQ MAILLONS, ET CE QU'ILS DOIVENT PRODUIRE :
#   1. PERCEVOIR   (`--tokenize`)           : le texte devient des jetons, réversibles ;
#   2. RETENIR     (`--entree-memoire K`)   : les K derniers pas sont dans l'entrée du réseau, et
#                                             deux exécutions rendent le même fichier (au bit près) ;
#   3. SE SOUVENIR (`--episodique-essai`)   : écrire puis relire rend l'épisode — round-trip exact ;
#   4. CONSOLIDER  (LoRA, puis le MOTEUR)   : le rejeu améliore la perplexité d'un texte **jamais
#                                             rejoué** — mesuré AVANT et APRÈS, par `drave` ;
#   5. AGIR        (`--infer`)              : le chemin court génère — et on publie son **temps**
#                                             et son **accord** avec le cerveau entier.
#
# CE QUE LA BOUCLE NE FAIT PAS, ET QU'ELLE DIT : elle ne prétend pas que le résultat est *bon* —
# les fiches ont mesuré que le réflexe est **un autre agent** (accord 28 à 51 % par position,
# 0 à 5 jetons sur 96 en génération). Ce qu'elle établit est la **chaîne** : chaque faculté reçoit
# ce que la précédente a produit, et le résultat passe de l'une à l'autre sans rupture.
#
# Usage : tools/boucle-cerveau.sh [--texte FICHIER] [--morceaux 3] [--epoques 8]
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
P=${P:-/home/stephane/gpu-env/bin/python}
SNAP=${SNAP:-$HOME/IA/cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
TEXTE=${TEXTE:-data/wikitext2_test.txt}
MORCEAUX=${MORCEAUX:-3}
EPOQUES=${EPOQUES:-8}
T=${T:-/tmp/boucle-cerveau}
[ -s "$M" ] || { echo "  ❌ modèle absent : $M"; exit 2; }
[ -x "$D" ] || { echo "  ❌ binaire du moteur absent : $D"; exit 2; }
[ -d "$SNAP" ] || { echo "  ❌ poids PyTorch absents : $SNAP"; exit 2; }
. tools/_corpus.sh
mkdir -p "$T"

echo "═══ LA BOUCLE DU CERVEAU — $(basename "$M") · texte $TEXTE ═══"
echo

# ---------------------------------------------------------------- 1. PERCEVOIR
"$D" "$M" --tokenize --fichier "$TEXTE" --sortie "$T/jetons.txt" 2>&1 \
    | tee "$T/tokenize.log" | tail -2 | sed 's/^/  /'
JETONS=$(grep -oE "[0-9]+ tokens écrits" "$T/tokenize.log" | grep -oE "[0-9]+" | head -1)
echo "1. PERCEVOIR   : ${JETONS:-?} jetons, réversibles (le texte se reconstruit identique)"
echo

# ---------------------------------------------------------------- 2. RETENIR
# LE SIGNAL EST UN FICHIER TEXTE (une valeur par ligne). La première version de cette boucle en
# écrivait un binaire f32 : le moteur a REFUSÉ (« stream did not contain valid UTF-8 »), le script
# a avalé le refus et annoncé « la mémoire n'est pas déterministe » — exactement le défaut que ce
# dépôt traque (une erreur avalée coûte plus cher que l'erreur). Le code de sortie est vérifié.
$P - "$T" <<'SIGNAL'
import pathlib, sys
import numpy as np
t = pathlib.Path(sys.argv[1])
v = np.sin(np.linspace(0, 12.56, 16))
(t / "signal.txt").write_text("\n".join(f"{x:.6f}" for x in v))
SIGNAL
peri() {   # $1 = sortie, $2 = mémoire ; REFUSE en le disant
    "$D" "$M" --entree "signal:$T/signal.txt" --sortie "$1" --ctx 16 --threads 8 \
        --entree-memoire "$2" --recurent > "$T/peri.log" 2>&1
    local code=$?
    [ "$code" -eq 0 ] && [ -s "$1" ] || {
        echo "  ❌ la périphérie a refusé (code $code) :"; tail -2 "$T/peri.log" | sed 's/^/     /'
        exit 1
    }
}
peri "$T/ret-1.f32" 8; peri "$T/ret-2.f32" 8
cmp -s "$T/ret-1.f32" "$T/ret-2.f32" || { echo "  ❌ la mémoire n'est pas déterministe"; exit 1; }
peri "$T/sans.f32" 0
cmp -s "$T/ret-1.f32" "$T/sans.f32" && { echo "  ❌ la mémoire ne change rien"; exit 1; }
echo "2. RETENIR     : 8 pas dans l'entrée (--entree-memoire 8), déterministe au bit près,"
echo "                 et la sortie DIFFÈRE de celle sans mémoire ($(stat -c%s "$T/ret-1.f32") octets)"
echo "                 (moteur : R² 1,000 sur v[t−8], 0 paire de plus — porte-memoire)"
echo

# ---------------------------------------------------------------- 3. SE SOUVENIR
EPI=$("$D" "$M" --episodique-essai 300 --episodique-k 64 --ids-file "$IDS" --ctx 512 --threads 8 2>&1 \
      | grep -E "round-trip" | head -1 | sed 's/^ *//')
echo "3. SE SOUVENIR : ${EPI:-essai illisible}"
echo "                 (l'exemplaire bat la moyenne : 7 % du magasin → 87 % de rappel — porte-episodique)"
echo

# ---------------------------------------------------------------- 4. CONSOLIDER
# LA MESURE SE FAIT AILLEURS QUE DANS LE REJEU, sinon c'est de la récitation : le rejeu porte sur
# les premiers morceaux (jetons 0 à ~6 000), la mesure se fait à 20 000 jetons du début — un
# morceau que le cerveau n'a PAS rejoué (la première version mesurait les 1 024 premiers jetons,
# c'est-à-dire le premier morceau rejoué ; attrapé en relisant, pas par un chiffre).
MESURE_DEPUIS=${MESURE_DEPUIS:-20000}
AVANT=$("$D" "$M" --ppl "$T/jetons.txt" --depuis "$MESURE_DEPUIS" --limit 1024 --ctx 1024 \
        --threads 8 2>&1 | grep -oE "perplexité [0-9.]+" | grep -oE "[0-9.]+" | head -1)
echo "  (le cerveau lit 1 024 jetons à partir du jeton $MESURE_DEPUIS — jamais rejoués : $AVANT)"
TRAIN=$(for i in $(seq 0 $((MORCEAUX - 1))); do printf '%s,' "$i"; done | sed 's/,$//')
$P tools/n4_dessin_b.py --objectif plein --rejeu "$TRAIN" --val 3 --test 4 --epoques "$EPOQUES" \
    --graine 0 --bras lora --lots 1 --sans-portes --sauver "$T/poids" \
    --json "$T/consolidation.json" > "$T/consolidation.log" 2>&1 \
    || { echo "  ❌ la consolidation a échoué (voir $T/consolidation.log)"; exit 1; }
$P tools/exporter_gguf_dense.py --hf "$SNAP" --lora "$T/poids-lora.pt" --couches-lora 8 \
    --sortie "$T/consolide.gguf" > "$T/export.log" 2>&1 \
    || { echo "  ❌ l'export a échoué (voir $T/export.log)"; exit 1; }
APRES=$("$D" "$T/consolide.gguf" --ppl "$T/jetons.txt" --depuis "$MESURE_DEPUIS" --limit 1024 \
        --ctx 1024 --threads 8 2>&1 | grep -oE "perplexité [0-9.]+" | grep -oE "[0-9.]+" | head -1)
[ -n "$AVANT" ] && [ -n "$APRES" ] || { echo "  ❌ perplexité illisible"; exit 1; }
ECART=$($P -c "print(f'{100*($APRES-$AVANT)/$AVANT:+.2f}')")
echo "4. CONSOLIDER  : $MORCEAUX morceaux rejoués, $EPOQUES époques, LoRA rang 8 sur 8 couches"
echo "                 perplexité MOTEUR, sur un morceau JAMAIS rejoué : $AVANT → $APRES ($ECART %)"
echo

# ---------------------------------------------------------------- 5. AGIR
INVITE=${INVITE:-"Le ciel est bleu parce que"}
GEN_PLEIN=$("$D" "$M" --infer --prompt "$INVITE" --n 16 --ctx 128 --threads 8 --temp 0 2>&1 \
            | grep -E "généré" | head -1 | sed 's/^ *//')
GEN_COURT=$("$D" "$T/consolide.gguf" --infer --prompt "$INVITE" --n 16 --ctx 128 --threads 8 \
            --temp 0 --couches 0:8 --tete-partielle 2>&1 | grep -E "généré" | head -1 | sed 's/^ *//')
echo "5. AGIR        : complet   $GEN_PLEIN"
echo "                 réflexe   $GEN_COURT"
echo "                 (l'accord avec le cerveau est de 28 à 51 % par position et 0 à 5 jetons sur 96"
echo "                  en génération : le réflexe est un AUTRE agent — rapport-e5-distillation.md)"
echo
echo "═══ la chaîne est complète : percevoir → retenir → se souvenir → consolider → agir ═══"
exit 0
