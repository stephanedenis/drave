#!/bin/bash
# porte-sauvegarde-modele.sh — le fichier sauvé reproduit-il le modèle ENTRAÎNÉ ?
#
# CE QUE LA PORTE VERROUILLE, et pourquoi chacun de ces points :
#   1. **la perte de validation ne bouge à AUCUNE des quatre étapes** — après la boucle, après la
#      restauration du meilleur point, après la matérialisation des poids, après relecture du
#      disque. C'est la mesure qui a trouvé M8 : le modèle changeait à la matérialisation
#      (3,6465 → 8,8257 bits/octet), et **personne ne mesurait là**, seulement avant et après ;
#   2. **le variant log-normal est le cas qui cassait**, et il repasse : sa tête est **liée** à la
#      table d'entrée (`tie_word_embeddings`), et reparamétrer un tenseur PARTAGÉ casse le partage
#      en silence — la table restait figée pendant l'entraînement, puis recevait les poids de la
#      tête. La porte exige donc que le harnais **NOMME** le module partagé qu'il exclut : une
#      exclusion silencieuse serait un autre défaut qui attend ;
#   3. **le témoin dense reste vert** : sans lui, on ne saurait pas si la porte mesure la
#      reproductibilité ou le variant ;
#   4. **le contrôle est APRÈS, pas avant** : sous reparamétrisation, `module.weight` **est déjà**
#      la valeur du `forward` — comparer les deux avant le retrait compare une expression à
#      elle-même et rend toujours zéro (c'est le faux contrôle qui a laissé M8 ouvert deux jours).
#
# COÛT : deux courts entraînements (200 pas), ~1 min en tout.
set -u
cd "$(dirname "$0")/.."
P=${P:-/home/stephane/gpu-env/bin/python}
T=${TRAVAIL:-/tmp/porte-sauvegarde-modele}
PAS=${PAS:-200}
DONNEES=${DONNEES:-data/corpus_en.txt}
VALIDATION=${VALIDATION:-data/corpus_en_val.txt}
DELAI=${DELAI:-1800}

for f in "$DONNEES" "$VALIDATION"; do
    [ -s "$f" ] || { echo "  ❌ $f manquant : cette porte entraîne deux petits modèles"; exit 2; }
done
$P -c "import torch, transformers" 2>/dev/null || {
    echo "  ❌ $P n'a pas torch/transformers : cette porte entraîne"; exit 2; }
rm -rf "$T"; mkdir -p "$T"

C="--famille route --dim 192 --couches 4 --tetes 4 --cache 768 --experts 8 --k 2 --seq 128 \
   --lot 32 --lr 3e-4 --graine 1 --pas $PAS --eval-tous $PAS"
ECHEC=0

for VARIANT in dense lognormal; do
    EXTRA=""; [ "$VARIANT" = lognormal ] && EXTRA="--poids-lognormaux"
    echo "=== $VARIANT ==="
    timeout "$DELAI" $P -u tools/entrainer_moteur.py $C $EXTRA --verifier-sauvegarde \
        --sortie "$T/$VARIANT" > "$T/$VARIANT.log" 2>&1
    CODE=$?
    grep -E "POIDS PARTAGÉS|#   .*partagé|VÉRIFICATION|#   après|écart de poids" "$T/$VARIANT.log" \
        | sed 's/^/  /'
    if [ "$CODE" != 0 ]; then
        echo "  ❌ le fichier sauvé ne reproduit pas le modèle entraîné (code $CODE)"
        ECHEC=1
        continue
    fi
    # Les quatre moments doivent être ÉGAUX — on les relit dans le journal, pas dans une variable.
    # Le premier nombre de chaque ligne, quel que soit le libellé du moment (« la boucle » fait
    # deux mots, un motif `[a-z]+ +nombre` en ratait un et la porte comptait 3 moments sur 4).
    QUATRE=$(grep -E "^  #   après" "$T/$VARIANT.log" \
             | awk '{for (i = 1; i <= NF; i++) if ($i ~ /^[0-9]+\.[0-9]+$/) {print $i; break}}')
    N=$(printf '%s\n' "$QUATRE" | grep -c .)
    if [ "$N" != 4 ]; then
        echo "  ❌ $N moment(s) mesuré(s) au lieu de 4 : la vérification n'a pas tourné en entier"
        ECHEC=1
        continue
    fi
    MIN=$(printf '%s\n' "$QUATRE" | sort -n | head -1)
    MAX=$(printf '%s\n' "$QUATRE" | sort -n | tail -1)
    if [ "$MIN" != "$MAX" ]; then
        echo "  ❌ la perte de validation CHANGE entre les étapes : $MIN … $MAX"
        ECHEC=1
        continue
    fi
    echo "  ✅ les quatre moments donnent la même perte : $MIN"
    # LE CAS QUI CASSAIT doit être NOMMÉ, pas contourné en silence.
    if [ "$VARIANT" = lognormal ]; then
        if grep -q "POIDS PARTAGÉS" "$T/$VARIANT.log" && grep -q "lm_head" "$T/$VARIANT.log"; then
            echo "  ✅ le module partagé (lm_head ↔ table d'entrée) est exclu ET nommé"
        else
            echo "  ❌ la tête liée n'est pas exclue/nommée : le partage des poids casserait en"
            echo "     silence, et le fichier sauvé ne serait plus le modèle entraîné (M8)"
            ECHEC=1
        fi
    fi
    echo
done

[ "$ECHEC" = 0 ] || { echo "❌ porte sauvegarde du modèle : ÉCHEC"; exit 1; }
echo "✅ porte sauvegarde du modèle : la perte de validation est la MÊME aux quatre étapes"
echo "   (boucle, restauration, matérialisation, disque), pour le témoin dense ET pour le variant"
echo "   log-normal — et le poids partagé qui cassait le partage est exclu et nommé."
