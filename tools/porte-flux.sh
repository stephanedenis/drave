#!/bin/bash
# Porte du DÉCOUPAGE : deux nœuds, un petit modèle, cinq modes de flux.
#
# Pourquoi elle existe : le défaut de la `pre` reçue (sprint 13) a vécu jusqu'à
# ce qu'on compare des tenseurs à la main sur un modèle de 365 Go et quatre
# minutes par passe. Aucune porte ne couvrait un COUPLE DE NŒUDS ; celle-ci le
# fait en quelques secondes, sur Qwen2.5-0.5B, et elle attrape trois familles de
# défauts d'un coup :
#   · la couture (l'état rendu par le second nœud doit être celui de la passe
#     complète — pour les modes exacts, au bit près) ;
#   · le cadriciel de flux lui-même (en-tête, mode, compte `np`, positions) ;
#   · l'accord entre les modes (un mode avec perte ne doit pas coûter plus que
#     son codec).
#
# Les modes 0 (f32 dense), 1 et 3 (lot dense) sont EXACTS : écart attendu 0,00e0.
# Les modes 2 et 4 passent par le codec quantifié (indices par écarts, valeurs i8,
# une échelle par bloc de 32 canaux) : leur écart est une perte assumée, et la
# porte vérifie qu'il reste sous un plafond mesuré, pas qu'il est nul.
#
#   tools/porte-flux.sh            la porte
#   MODELE=... tools/porte-flux.sh autre modèle (dense, sans hyper-connexions)

set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
MODELE=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
N_IDS=${N_IDS:-24}
COUCHES=${COUCHES:-12}
CTX=${CTX:-64}
PORT=${PORT:-$((48000 + RANDOM % 1000))}

# Tout ce qui est écrit par cette porte vit dans SON répertoire : deux
# exécutions concurrentes (ou une porte lancée depuis un autre dépôt) ne se
# tronquent plus le journal — le `grep` de disponibilité pouvait lire la ligne
# de l'autre serveur et croire que le sien écoutait.
TRAVAIL=$(mktemp -d "${TMPDIR:-/tmp}/porte-flux-XXXXXX")
LOG_SRV="$TRAVAIL/serveur.log"
IDS="$TRAVAIL/ids.txt"

[ -x "$D" ] || { echo "  $D absent : construire d'abord (cargo build --release)"; exit 1; }
[ -s "$MODELE" ] || { echo "  $MODELE absent"; exit 1; }
if [ ! -s "$IDS" ]; then
    "$D" "$MODELE" --tokenize --fichier data/wikitext2_test.txt \
         --sortie "$IDS" >/dev/null 2>&1
fi
[ -s "$IDS" ] || { echo "  jetons de test indisponibles"; exit 1; }

# Le nœud moteur : sa plage de couches est IMPOSÉE par le flux reçu, il n'a donc
# qu'à écouter. Il sert UNE connexion puis s'arrête (« arrêt : failed to fill
# whole buffer », après le dernier flux) : on en relance donc un par mode, en
# attendant qu'il écoute vraiment plutôt que de dormir au hasard.
SRV=""
demarrer_serveur() {
    : > "$LOG_SRV"
    "$D" "$MODELE" --flux-serveur "$PORT" --ctx "$CTX" --threads 8 \
         > "$LOG_SRV" 2>&1 &
    SRV=$!
    for _ in $(seq 1 120); do
        grep -q "nœud moteur sur" "$LOG_SRV" 2>/dev/null && return 0
        kill -0 $SRV 2>/dev/null || { echo "  le nœud moteur est mort :"; tail -3 "$LOG_SRV"; return 1; }
        sleep 0.5
    done
    echo "  le nœud moteur n'écoute pas après 60 s"; return 1
}
arreter_serveur() { if [ -n "$SRV" ]; then kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; SRV=""; fi; }
trap 'arreter_serveur; rm -rf "$TRAVAIL"' EXIT

echec=0
ecart2=""
tester() {   # nom, plafond d'écart, arguments du pilote
    local nom="$1" plafond="$2"; shift 2
    demarrer_serveur || { printf "  %-34s %s\n" "$nom" "❌ nœud moteur"; echec=1; return; }
    local sortie code
    # `timeout` sur le PILOTE aussi : une régression du cadriciel qui bloque le
    # pair (lecture d'un corps qui n'arrive pas — c'est ce que faisait un mode 3
    # sans préfixe v6) laissait la porte tourner jusqu'au `timeout` de
    # `portes.sh`, et un `timeout` externe rend un code que personne ne lisait.
    sortie=$(timeout 180 "$D" "$MODELE" --ppl-reparti "127.0.0.1:$PORT" \
             --couches-locales "$COUCHES" --limit "$N_IDS" --ctx "$CTX" --threads 8 "$@" 2>&1)
    code=$?
    arreter_serveur
    local ecart
    ecart=$(printf '%s\n' "$sortie" | grep -oE "écart +: +[0-9.e+-]+" | grep -oE "[0-9.e+-]+$")
    local ppl_ref ppl_deux
    ppl_ref=$(printf '%s\n' "$sortie" | grep -oE "référence locale +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
    ppl_deux=$(printf '%s\n' "$sortie" | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
    if [ -z "$ecart" ] || [ "$code" != "0" ]; then
        printf "  %-34s %s\n" "$nom" "❌ pas d'écart mesuré (code $code)"; echec=1
        printf '%s\n' "$sortie" | tail -3 | sed 's/^/      /'
        return
    fi
    # Le mode 2 est le codec de référence (avec perte) : le mode 4 emploie le
    # MÊME codec par état, donc il ne doit pas être plus dégradé que lui. Un
    # plafond unique et large pour les deux ne distinguerait pas « mode 4
    # correct » de « mode 4 dégradé au niveau du mode 2 ».
    if [ "$nom" = "mode 2 — listes par blocs" ]; then ecart2="$ecart"; fi
    if [ "$nom" = "mode 4 — lot en listes" ] && [ -n "$ecart2" ]; then
        local ok4
        ok4=$(python3 -c "print('oui' if float('$ecart')<=float('$ecart2') else 'non')" 2>/dev/null)
        if [ "$ok4" != "oui" ]; then
            printf "  %-34s %s  ❌ (mode 4 %s > mode 2 %s)\n" "$nom" "$ecart" "$ecart" "$ecart2"; echec=1
            return
        fi
    fi
    # Comparaison numérique sans `bc` : l'écart est en notation scientifique.
    local ok
    ok=$(python3 -c "import sys;print('oui' if float('$ecart')<=float('$plafond') else 'non')" 2>/dev/null)
    if [ "$ok" = "oui" ]; then
        printf "  %-34s %s  ✅  (réf %s / deux nœuds %s)\n" "$nom" "$ecart" "$ppl_ref" "$ppl_deux"
    else
        printf "  %-34s %s  ❌ (plafond %s)\n" "$nom" "$ecart" "$plafond"; echec=1
    fi
}

# Plafonds : 0 pour les modes SANS perte (0, 1, 3) ; pour les deux modes à codec
# quantifié, une valeur mesurée majorée d'un facteur ~2 — et le mode 4 doit en
# plus rester sous le mode 2 (même codec, un état à la fois).
tester "mode 0 — f32 dense"          "0"      --flux
tester "mode 1 — listes quantifiées" "0"      --flux-listes
tester "mode 2 — listes par blocs"   "6e-2"   --flux-blocs --lot 1
tester "mode 3 — lot dense f32"      "0"      --lot 4
tester "mode 4 — lot en listes"      "1e-2"   --lot 4 --flux-blocs

arreter_serveur
exit $echec
