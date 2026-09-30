#!/bin/bash
# Prépare la répétition Colab : le dépôt en UN fichier, l'empreinte du modèle,
# et les commandes des deux côtés. Rien n'est envoyé nulle part — c'est vous qui
# téléversez, et le script vous dit quoi vérifier.
#
#   tools/preparer_colab.sh [modèle.gguf] [port]
set -u
cd "$(dirname "$0")/.."
MODELE=${1:-models/Qwen2.5-0.5B-Q8_0.gguf}
PORT=${2:-5599}
BUNDLE=/tmp/drave.bundle

echo "=== 1. le dépôt, en un fichier ==="
git bundle create "$BUNDLE" --all >/dev/null 2>&1 || { echo "échec du bundle"; exit 1; }
git bundle verify "$BUNDLE" 2>&1 | tail -1
echo "    $BUNDLE : $(stat -c%s "$BUNDLE") octets ($(du -h "$BUNDLE" | cut -f1))"
echo "    commit : $(git log --oneline -1)"

echo
echo "=== 2. le modèle (le MÊME des deux côtés) ==="
if [ -f "$MODELE" ]; then
    TAILLE=$(stat -c%s "$MODELE")
    EMPREINTE=$(sha256sum "$MODELE" | cut -c1-24)
    echo "    $MODELE : $((TAILLE / 1048576)) Mo"
    echo "    sha256 (24 premiers) : $EMPREINTE"
    echo "    → à coller dans la cellule 4 du notebook (constante ATTENDU)"
else
    echo "    $MODELE introuvable"
fi

echo
echo "=== 3. côté MACHINE LOCALE (le nœud moteur) ==="
cat <<COMMANDES
    cd $(pwd)/drave-core && cargo build --release
    ./target/release/drave ../$MODELE --flux-serveur 0.0.0.0:$PORT --ctx 256
    # puis rendez $PORT joignable depuis Colab, au choix :
    #   ngrok tcp $PORT                    (compte gratuit, donne hote:port)
    #   tailscale up                       (les deux côtés sur le même tailnet)
    #   ssh -R $PORT:localhost:$PORT votre-vps   (si vous avez une machine publique)
    # vérification locale : ss -ltn | grep $PORT
COMMANDES

echo
echo "=== 4. côté COLAB ==="
echo "    téléverser : $BUNDLE  et  $MODELE"
echo "    puis ouvrir colab/Drave-reparti.ipynb et suivre les cellules"
echo
echo "=== 5. ce qu'on attend ==="
cat <<'ATTENDU'
    écart : 0.00e0        (mode dense : le transport f32 est sans perte)
    transport : LOTS de 64 jetons · ~229 000 octets par lot · 4 lots pour 256 jetons
    temps : ~1,6 s de calcul local par LOT de 64 (12 couches) · l'attente du pair = son calcul + l'aller-retour
    ordre de grandeur à 60 ms d'aller-retour : ~8 jetons/s (le découpage ne sert pas à accélérer)
ATTENDU
