#!/bin/bash
# c8_corpus.sh — capturer des états de profondeur sur PLUSIEURS textes, pour une tête qui généralise.
#
# POURQUOI. La première tête entraînée (10 octobre) a été apprise sur la **première moitié d'un
# texte** et évaluée sur la **seconde** : 845,45 de perplexité contre 456 586,60 pour la tête
# empruntée (÷540). Mais les deux moitiés parlent du même sujet, avec le même vocabulaire — le
# chiffre mesure donc surtout une adaptation au TEXTE. La question qui décide pour C8 est :
# **une tête entraînée sur des textes sait-elle lire un texte qu'elle n'a JAMAIS vu ?**
#
# Ce script découpe le corpus en morceaux pris à des ENDROITS DIFFÉRENTS, capture l'état de
# profondeur 16 pour chacun, et laisse l'entraîneur séparer : morceaux d'entraînement d'un côté,
# morceaux de test de l'autre.
#
# Usage : tools/c8_corpus.sh [nb_morceaux] [jetons_par_morceau] [profondeur]
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
MORCEAUX=${1:-8}
TAILLE=${2:-1024}
COUCHES=${3:-16}
T=${T:-/tmp/c8-corpus}

[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }
mkdir -p "$T"

python3 - "$IDS" "$T" "$MORCEAUX" "$TAILLE" <<'PY'
import pathlib, re, sys
ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(sys.argv[1]).read_text()) if x.strip()]
t, n, taille = pathlib.Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
# Il faut que les morceaux NE SE RECOUVRENT PAS : l'espacement vaut len/(n+1), donc il doit
# dépasser la taille d'un morceau. Exiger « 3× » était plus strict que nécessaire et refusait
# des découpages légitimes (85 625 jetons pour 40 morceaux de 1 024 : espacement 2 088).
if len(ids) // (n + 1) <= taille:
    raise SystemExit(f"corpus trop court : {len(ids)} jetons pour {n} morceaux de {taille} "
                     f"(il faut un espacement > {taille})")
# morceaux RÉPARTIS dans tout le corpus, jamais recouvrants
pas = len(ids) // (n + 1)
for i in range(n):
    debut = i * pas
    chunk = ids[debut:debut + taille]
    (t / f"morceau-{i}.txt").write_text(",".join(str(x) for x in chunk))
    print(f"  morceau {i} : jetons {debut}..{debut + taille}")
PY

POS=$(seq -s, 4 $((TAILLE - 1)))
for i in $(seq 0 $((MORCEAUX - 1))); do
    prefixe="$T/etat-m$i"
    rm -f "$prefixe".*
    $D "$M" --ppl "$T/morceau-$i.txt" --limit "$TAILLE" --ctx "$TAILLE" --threads 8 \
       --couches "0:$COUCHES" --tete-partielle --etat-sortie "$prefixe" --etat-pos "$POS" \
       > "$T/capture-$i.log" 2>&1
    ppl=$(grep -oE "perplexité [0-9.]+ sur" "$T/capture-$i.log" | grep -oE "[0-9.]+" | head -1)
    n=$(ls "$prefixe".* 2>/dev/null | wc -l)
    printf '  morceau %s : %s états · perplexité tronquée %s\n' "$i" "$n" "${ppl:-?}"
done

echo
echo "Entraîner sur les morceaux 0..$((MORCEAUX - 2)), tester sur le DERNIER (jamais vu) :"
train=$(for i in $(seq 0 $((MORCEAUX - 2))); do printf '%s,' "$T/etat-m$i"; done | sed 's/,$//')
echo "  CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python tools/c8_entrainer_tete.py \\"
echo "     --train $train --test $T/etat-m$((MORCEAUX - 1)) \\"
echo "     --ids $T/morceau-$((MORCEAUX - 1)).txt --modele $M --limite $TAILLE --epoques 20"
echo "(l'entraîneur refuse les identifiants qui ne correspondent pas aux états : morceau de test)"
