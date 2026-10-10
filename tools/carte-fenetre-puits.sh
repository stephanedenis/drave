#!/bin/bash
# carte-fenetre-puits.sh — la question que le §47 a ouverte.
#
# MESURÉ AU §47 : sous une fenêtre de 32, le défaut de 4 puits n'est pas l'optimum — 24 puits
# rendent 15,4339 contre 18,1141 (−14,8 %, `--limit 128`) — et SANS puits la fenêtre CASSE le
# modèle (1297,5437). Le drain est donc PORTEUR. D'où la question qui décide de l'intérêt de
# toute l'affaire :
#
#   **Le drain rend-il la fenêtre moins coûteuse — c'est-à-dire existe-t-il un couple
#   (fenêtre, puits) qui APPROCHE l'attention complète (14,6496) en ne notant qu'une fraction
#   des clés ?**
#
# Si oui, c'est le levier qui attaque le poste dominant (les scores d'attention sont O(N) par
# jeton, la fenêtre les rend O(W)) sans payer en qualité. Si non, la fenêtre est un coût sec et
# il faut le dire.
#
# Ce script balaie fenêtre × puits et imprime un tableau markdown ; il note aussi les PAIRES
# d'attention par jeton, c'est-à-dire ce qu'on économise réellement.
#
# Usage : tools/carte-fenetre-puits.sh [limit]   (défaut 128)
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
LIMITE=${1:-128}
CTX=${CTX:-512}
# Balayage réglable : FENETRES et PUITS (le drain et la fenêtre sont deux leviers du MÊME
# budget de clés notées : fenêtre + puits).
FENETRES=${FENETRES:-16 32 64 128}
PUITS=${PUITS:-0 8 16 24 32}
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }

# Chaque case rend « perplexité · secondes · tok/s » : la QUALITÉ et le PRIX RÉEL. Le temps
# n'est pas décoratif — la fenêtre ne réduit que les scores d'attention, qui ne sont qu'un
# poste du calcul (la FFN domine), donc le gain de temps est TOUJOURS plus petit que le gain
# de clés, et c'est exactement ce qu'il faut mesurer plutôt que supposer.
mesure () { # $@ = drapeaux ; imprime « perplexité secondes tok/s »
    local sortie
    sortie=$($D "$M" --ppl "$IDS" --limit "$LIMITE" --ctx "$CTX" --threads 8 "$@" 2>&1)
    local ppl sec tok
    ppl=$(printf '%s' "$sortie" | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+")
    # Les secondes : dernier « (N.N s) » de la sortie (la ligne de synthèse est la dernière).
    # Le premier motif exigeait la phrase entière sur UNE ligne — la sortie du moteur la coupe
    # parfois, et la carte affichait « ? s » sans le dire.
    # Les secondes : dernier « (N.N s) » de la sortie. Les LIGNES SONT RECOLLÉES d'abord : la
    # sortie mêle stdout et stderr, et une ligne de journal peut s'insérer AU MILIEU de la ligne
    # de synthèse — le motif ne trouvait alors rien et la carte affichait « ? s » sans le dire
    # (deux essais successifs s'y sont cassés les dents).
    sec=$(printf '%s' "$sortie" | tr '\n' ' ' | grep -oE "\([0-9]+[.,][0-9]+ s\)" | tail -1 \
          | grep -oE "[0-9]+[.,][0-9]+")
    tok=$(printf '%s' "$sortie" | grep -oE "[0-9.]+ tok/s effectifs" | grep -oE "[0-9.]+")
    printf '%s·%s s·%s tok/s' "${ppl:-?}" "${sec:-?}" "${tok:-?}"
}

REFO=$(mesure)
echo "référence (aucune fenêtre, $LIMITE jetons) : $REFO  ·  clés notées par jeton ≈ $LIMITE"
echo
printf '| fenêtre \\ puits |'
for n in $PUITS; do printf ' %s |' "$n"; done
echo
printf '|---|'
for n in $PUITS; do printf '%s|' '---'; done
echo
for f in $FENETRES; do
    printf '| **%s** |' "$f"
    for n in $PUITS; do
        if [ "$n" = 0 ]; then v=$(mesure --attn-window "$f"); else v=$(mesure --attn-window "$f" --attn-sinks "$n"); fi
        printf ' %s |' "${v:-?}"
    done
    echo
done
echo
echo "Chaque case : « perplexité · secondes · tok/s ». Clés notées par jeton ≈ fenêtre + puits,"
echo "contre $LIMITE pour l'attention complète — c'est le SEUL poste que la fenêtre réduit, donc le"
echo "gain de temps est plus petit que le gain de clés : c'est mesuré ici, pas supposé."
