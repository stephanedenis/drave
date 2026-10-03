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

[ -x "$D" ] || { echo "  $D absent : construire d'abord (cargo build --release)"; exit 1; }
[ -s "$MODELE" ] || { echo "  $MODELE absent"; exit 1; }
if [ ! -s /tmp/porte_flux_ids.txt ]; then
    "$D" "$MODELE" --tokenize --fichier data/wikitext2_test.txt \
         --sortie /tmp/porte_flux_ids.txt >/dev/null 2>&1
fi
[ -s /tmp/porte_flux_ids.txt ] || { echo "  jetons de test indisponibles"; exit 1; }

# Le nœud moteur : sa plage de couches est IMPOSÉE par le flux reçu, il n'a donc
# qu'à écouter. Il sert UNE connexion puis s'arrête (« arrêt : failed to fill
# whole buffer », après le dernier flux) : on en relance donc un par mode, en
# attendant qu'il écoute vraiment plutôt que de dormir au hasard.
SRV=""
demarrer_serveur() {
    "$D" "$MODELE" --flux-serveur "$PORT" --ctx "$CTX" --threads 8 \
         > /tmp/porte_flux_srv.log 2>&1 &
    SRV=$!
    for _ in $(seq 1 120); do
        grep -q "nœud moteur sur" /tmp/porte_flux_srv.log 2>/dev/null && return 0
        kill -0 $SRV 2>/dev/null || { echo "  le nœud moteur est mort :"; tail -3 /tmp/porte_flux_srv.log; return 1; }
        sleep 0.5
    done
    echo "  le nœud moteur n'écoute pas après 60 s"; return 1
}
arreter_serveur() { if [ -n "$SRV" ]; then kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; SRV=""; fi; }
trap 'arreter_serveur' EXIT

echec=0
tester() {   # nom, plafond d'écart, arguments du pilote
    local nom="$1" plafond="$2"; shift 2
    demarrer_serveur || { printf "  %-34s %s\n" "$nom" "❌ nœud moteur"; echec=1; return; }
    local sortie
    sortie=$("$D" "$MODELE" --ppl-reparti "127.0.0.1:$PORT" \
             --couches-locales "$COUCHES" --limit "$N_IDS" --ctx "$CTX" --threads 8 "$@" 2>&1)
    arreter_serveur
    local ecart
    ecart=$(printf '%s\n' "$sortie" | grep -oE "écart +: +[0-9.e+-]+" | grep -oE "[0-9.e+-]+$")
    local ppl_ref ppl_deux
    ppl_ref=$(printf '%s\n' "$sortie" | grep -oE "référence locale +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
    ppl_deux=$(printf '%s\n' "$sortie" | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
    if [ -z "$ecart" ]; then
        printf "  %-34s %s\n" "$nom" "❌ pas d'écart mesuré"; echec=1
        printf '%s\n' "$sortie" | tail -3 | sed 's/^/      /'
        return
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

tester "mode 0 — f32 dense"          "0"      --flux
tester "mode 1 — listes quantifiées" "0"      --flux-listes
tester "mode 2 — listes par blocs"   "5e-2"   --flux-blocs --lot 1
tester "mode 3 — lot dense f32"      "0"      --lot 4
tester "mode 4 — lot en listes"      "5e-2"   --lot 4 --flux-blocs

arreter_serveur
exit $echec
