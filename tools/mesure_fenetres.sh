#!/bin/bash
# mesure_fenetres.sh — le protocole d'évaluation des modèles entraînés ICI.
#
# POURQUOI HUIT FENÊTRES DE 128. Ces modèles sont entraînés sur des fenêtres de
# 128 jetons. Les évaluer sur une fenêtre plus longue les fait sortir de leur
# distribution : mesuré, la perplexité TRIPLE à 2 048 et le classement s'inverse.
# La mesure de record est donc huit tranches contiguës de 128 jetons, moyennées
# en log (moyenne géométrique), ce qui est la moyenne des NLL par jeton.
#
# CE QUE LE SCRIPT ÉCRIT AUSSI : les paires par jeton (l'unité d'iso-lecture sans
# laquelle « routé contre dense » ne veut rien dire) et les événements en listes.
#
# Usage :
#   mesure_fenetres.sh <modele.gguf> [--ids F] [--fenetres 8] [--taille 128]
#                      [--threads 8] [--chemins "--dense --push"] [--etiquette nom]
set -u

D=${D:-./drave-core/target/release/drave}
CORPUS=${CORPUS:-data/corpus_en_val.txt}
MODELE=""; IDS=""; FENETRES=8; TAILLE=128; THREADS=8; CHEMINS="--push"; ETIQ=""
while [ $# -gt 0 ]; do
    case "$1" in
        --ids) IDS="$2"; shift 2 ;;
        --fenetres) FENETRES="$2"; shift 2 ;;
        --taille) TAILLE="$2"; shift 2 ;;
        --threads) THREADS="$2"; shift 2 ;;
        --chemins) CHEMINS="$2"; shift 2 ;;
        --etiquette) ETIQ="$2"; shift 2 ;;
        *) MODELE="$1"; shift ;;
    esac
done
[ -n "$MODELE" ] || { echo "usage : mesure_fenetres.sh <modele.gguf> [--ids F] ..."; exit 2; }
[ -f "$MODELE" ] || { echo "modèle absent : $MODELE"; exit 2; }
[ -n "$ETIQ" ] || ETIQ=$(basename "$MODELE" .gguf)

# Les identifiants sont les OCTETS du corpus de validation : ces modèles sont
# byte-level (vocabulaire 256), donc l'identifiant EST l'octet. On garde assez
# d'octets pour toutes les fenêtres, et un peu plus (le moteur note n-1 jetons).
if [ -z "$IDS" ]; then
    IDS="/tmp/ids_fenetres_${FENETRES}x${TAILLE}_$(basename "$CORPUS")"
    if [ ! -s "$IDS" ]; then
        head -c $(( (FENETRES + 1) * TAILLE + 8 )) "$CORPUS" \
            | od -An -tu1 -v | tr -s ' ' '\n' | grep -v '^$' | paste -sd, - > "$IDS"
    fi
fi
[ -s "$IDS" ] || { echo "identifiants indisponibles"; exit 3; }

echo "# $ETIQ · $FENETRES fenêtres de $TAILLE jetons · $CHEMINS · $(cut -d' ' -f1 /proc/loadavg) de charge"
NLL_DIR=$(mktemp -d); n_fenetres=0
for w in $(seq 1 "$FENETRES"); do
    depuis=$(( (w - 1) * TAILLE ))
    # `--chemins` porte UN ou PLUSIEURS jeux d'options, séparés par « ; ». Le
    # découpage par espaces était un piège : « --push --act-topk 500 » devenait
    # TROIS chemins, dont deux invalides, et la moyenne portait sur autre chose
    # que ce qui était demandé (mesuré : un « 0 événements » inexplicable).
    while IFS= read -r chemin; do
        [ -n "$chemin" ] || continue
        sortie=$(timeout 1800 $D "$MODELE" --ppl "$IDS" --limit "$TAILLE" --depuis "$depuis" \
                     --ctx $(( TAILLE * 2 )) --threads "$THREADS" $chemin 2>&1)
        ppl=$(echo "$sortie" | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+" | tail -1)
        jetons=$(echo "$sortie" | grep -oE "sur [0-9]+ tokens" | grep -oE "[0-9]+" | tail -1)
        paires=$(echo "$sortie" | grep -oE "paires \(poids × activation\) par token : .*" | head -1 | sed 's/.*total //')
        ev=$(echo "$sortie" | grep -oE "\((\s*[0-9]+) événements" | grep -oE "[0-9]+" | head -1)
        # Le DÉBIT est mesuré sous la charge du moment : il n'est publiable qu'avec
        # elle, mais il est indispensable pour dire ce que le moteur rend vraiment.
        ts=$(echo "$sortie" | grep -oE "[0-9.]+ tok/s effectifs" | grep -oE "^[0-9.]+")
        printf "  %-4s fenêtre %d (depuis %d) : PPL %-10s %s jetons" \
               "$chemin" "$w" "$depuis" "${ppl:-?}" "${jetons:-?}"
        [ -n "$paires" ] && printf " · %s paires/jeton" "$paires"
        [ -n "$ev" ] && printf " · %s événements" "$ev"
        [ -n "$ts" ] && printf " · %s tok/s" "$ts"
        printf "\n"
        if [ -n "$ppl" ]; then
            # UN FICHIER PAR CHEMIN : moyenner ensemble le dense et le creux
            # donnerait un chiffre qui ne décrit ni l'un ni l'autre (mesuré : une
            # « moyenne sur 24 fenêtres » qui mélangeait trois exécutions).
            cle=$(printf '%s' "$chemin" | tr -c 'A-Za-z0-9' '_')
            echo "$ppl" >> "$NLL_DIR/$cle"
            n_fenetres=$((n_fenetres + 1))
        fi
    done <<< "$(printf '%s' "$CHEMINS" | tr ';' '\n')"
done
for f in "$NLL_DIR"/*; do
    [ -s "$f" ] || continue
    nom=$(basename "$f" | tr '_' ' ')
    awk -v nom="$nom" '{ s += log($1); n++ } END { printf "  → %-42s PPL moyenne (log) sur %d fenêtres : %.4f\n", nom, n, exp(s/n) }' "$f"
done
rm -rf "$NLL_DIR"
