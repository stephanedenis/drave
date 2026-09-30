#!/bin/bash
# Le côté LOCAL de la démonstration Colab : un nœud moteur qui écoute, et les
# trois façons de le rendre joignable depuis un runtime distant.
#
#   tools/colab_cote_local.sh [modèle.gguf] [port]
#
# Le script ne configure PAS le tunnel à votre place (il demande un compte, ou une
# machine publique) : il vérifie ce qui peut l'être, il lance le nœud, et il
# affiche la commande exacte à coller dans le notebook.
set -u
cd "$(dirname "$0")/.."
MODELE=${1:-models/Qwen2.5-0.5B-Q8_0.gguf}
PORT=${2:-5599}
BIN=./drave-core/target/release/drave

echo "=== 1. vérifications ==="
[ -x "$BIN" ] || { echo "  $BIN absent : lancez « cd drave-core && cargo build --release »"; exit 1; }
[ -f "$MODELE" ] || { echo "  $MODELE introuvable"; exit 1; }
echo "  binaire : $($BIN --version 2>/dev/null || echo 'drave')"
echo "  modèle  : $MODELE ($(( $(stat -c%s "$MODELE") / 1048576 )) Mo)"
echo "  sha256 (24 premiers, à coller dans la cellule 4 du notebook) :"
echo "            $(sha256sum "$MODELE" | cut -c1-24)"
if pgrep -x drave > /dev/null; then
    echo "  ⚠ un autre « drave » tourne déjà (campagne de mesure ?) : le nœud s'y ajoutera"
fi

echo
echo "=== 2. le nœud moteur écoute ==="
echo "  sur 0.0.0.0:$PORT — donc au-delà de localhost, ce qu'il faut pour un pair distant"
$BIN "$MODELE" --flux-serveur "0.0.0.0:$PORT" --ctx 256 > /tmp/noeud_colab.log 2>&1 &
NOEUD=$!
for i in $(seq 1 60); do ss -ltn 2>/dev/null | grep -q ":$PORT " && break; sleep 0.5; done
if ! ss -ltn 2>/dev/null | grep -q ":$PORT "; then
    echo "  ✗ le port n'écoute pas — voir /tmp/noeud_colab.log"; kill $NOEUD 2>/dev/null; exit 1
fi
echo "  ✓ il écoute (journal : /tmp/noeud_colab.log)"

echo
echo "=== 3. rendez-le joignable depuis Colab (au choix) ==="
cat <<CONSEILS
  a) ngrok (compte gratuit, un authtoken) :
       ngrok tcp $PORT
     → notez l'adresse « tcp://X.tcp.ngrok.io:YYYY » : dans le notebook, HOTE=X.tcp.ngrok.io, PORT=YYYY
  b) Tailscale (les deux côtés sur le même tailnet) :
       tailscale up && tailscale ip -4
     → dans le notebook, HOTE=<ip 100.x.y.z>, PORT=$PORT
  c) SSH inverse (si vous avez une machine publique) :
       ssh -R $PORT:localhost:$PORT votre-vps
     → dans le notebook, HOTE=<votre-vps>, PORT=$PORT

  Notre avis : (a) pour un premier essai, (b) si vous voulez refaire la
  manipulation souvent. Le débit nécessaire est ridicule (< 1 Mbit/s) ; c'est la
  LATENCE qui décide, et elle est la même dans les trois cas.
CONSEILS

echo
echo "=== 4. ce que vous verrez dans le notebook ==="
cat <<'ATTENDU'
      écart : 0.00e0                 ← le critère, en mode dense
      transport : LOTS de 64 jetons · 229455 octets par lot · 4 lots
      temps : ~1,6 s de calcul local par lot · l'attente du pair = son calcul + l'aller-retour
ATTENDU

echo
echo "=== nœud en cours (Ctrl-C pour l'arrêter) ==="
trap 'kill $NOEUD 2>/dev/null; echo; echo "nœud arrêté"; exit 0' INT TERM
while kill -0 $NOEUD 2>/dev/null; do sleep 2; done
echo "le nœud s'est arrêté de lui-même — journal :"
tail -3 /tmp/noeud_colab.log
