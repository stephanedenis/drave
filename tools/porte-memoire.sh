#!/bin/bash
# porte-memoire.sh — C8 : la MÉMOIRE de la région frontière, retenue HORS du réseau.
#
# POURQUOI ELLE EXISTE. La tâche fermée de C8 (poursuivre un signal) n'était pas résolue, et la
# mesure a nommé la cause : l'état de sortie porte le signal **courant** (R² 0,992) mais pas celui
# d'il y a 8 pas (R² −0,681, y compris pour une lecture non linéaire) ; un tampon remis **en
# entrée** ne le rend que partiellement (+0,283) ; une **ligne à retard** le rend exactement
# (1,000). Autrement dit : **retenir demande une structure qui ne passe pas par la
# transformation du réseau** (reports/rapport-c8-peripherie.md). Le moteur l'a maintenant :
# `--memoire K` retient les K derniers signaux injectés, `--sortie-memoire F` les écrit.
#
# Ce que la porte verrouille, et pourquoi chacun :
#   1. **la mémoire est EXACTE** (au bit près) : c'est un tampon, pas un approximateur — la
#      comparaison se fait en f32 des DEUX côtés (comparer des octets écrits en f32 à des flottants
#      relus en f64 fabrique un écart de 5,9e-08 qui n'existe pas) ;
#   2. **elle ne coûte AUCUNE paire** : la mémoire ne traverse aucune couche ⇒ les paires par
#      décision doivent être identiques avec et sans elle. C'est la métrique du plan ;
#   3. **les pas d'avant le remplissage valent 0** et sont écrits (le fichier a une valeur par pas) ;
#   4. **les refus sont explicites** (code 2) : mémoire plus longue que la séquence, ou mémoire sans
#      fichier de sortie (une mémoire invérifiable ne vaut pas mieux que pas de mémoire) ;
#   5. **`--memoire 0` est EXPRIMABLE** et vaut « pas de mémoire » (leçon `--attn-sinks` : un zéro
#      qui n'existe pas est un défaut) — et il donne exactement le même résultat que sans le drapeau.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
K=${K:-8}
NPAS=${NPAS:-32}
[ -s "$M" ] || { echo "  ❌ modèle absent : $M"; exit 2; }
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT

python3 - "$T" "$NPAS" <<'PY'
import pathlib, sys
import numpy as np
t, n = pathlib.Path(sys.argv[1]), int(sys.argv[2])
rng = np.random.default_rng(3)
v = rng.uniform(-2, 2, n)
# le signal est écrit en texte À 9 CHIFFRES et relu en f32 : le banc et le moteur voient alors
# exactement les mêmes nombres, et « exact au bit près » veut dire quelque chose.
(t / "sig.txt").write_text("\n".join(f"{x:.9g}" for x in v))
(t / "sig.f32").write_bytes(v.astype("<f4").tobytes())
print(f"  signal : {n} pas · RMS {np.sqrt((v**2).mean()):.3f}")
PY

run () { $D "$M" --entree "signal:$T/sig.txt" --ctx 8 --threads 8 "$@" 2> "$T/err.txt"; }

echo "=== 1. la mémoire est EXACTE (f32 des deux côtés) ==="
run --sortie "$T/etats.f32" --memoire "$K" --sortie-memoire "$T/memoire.f32" > "$T/out.txt" || {
    echo "  ❌ la périphérie n'a pas tourné"; tail -2 "$T/err.txt"; exit 1; }
python3 - "$T" "$K" "$NPAS" <<'PY' || exit 1
import pathlib, struct, sys
import numpy as np
t, k, n = pathlib.Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
sig = np.frombuffer((t / "sig.f32").read_bytes(), dtype="<f4")          # LA MÊME source que le moteur
mem = np.frombuffer((t / "memoire.f32").read_bytes(), dtype="<f4")
if len(mem) != n:
    sys.exit(f"  ❌ {len(mem)} valeurs écrites pour {n} pas")
attendu = np.concatenate([np.zeros(k, dtype="<f4"), sig[:n - k]])
if not np.array_equal(mem, attendu):
    ecarts = np.abs(mem.astype(np.float64) - attendu.astype(np.float64))
    sys.exit(f"  ❌ la mémoire n'est pas exacte : écart max {ecarts.max():.3e}")
print(f"  ✅ mémoire EXACTE : {n} valeurs, {k} pas de retard, écart 0 (comparaison en f32)")
PY
grep -q "MÉMOIRE           : $K pas retenus" "$T/out.txt" || { echo "  ❌ la mémoire n'est pas annoncée"; exit 1; }

echo "=== 2. elle ne coûte AUCUNE paire (la métrique du plan) ==="
P1=$(grep -oE "paires par pas *: [0-9.]+ M" "$T/out.txt" | grep -oE "[0-9.]+")
run --sortie "$T/etats2.f32" > "$T/out2.txt"
P2=$(grep -oE "paires par pas *: [0-9.]+ M" "$T/out2.txt" | grep -oE "[0-9.]+")
printf '  avec mémoire %s M · sans %s M\n' "${P1:-?}" "${P2:-?}"
[ -n "$P1" ] && [ "$P1" = "$P2" ] || { echo "  ❌ la mémoire change le coût en paires"; exit 1; }
cmp -s "$T/etats.f32" "$T/etats2.f32" || { echo "  ❌ la mémoire change l'état de sortie"; exit 1; }
echo "  ✅ mêmes paires, même état : la mémoire ne traverse aucune couche"

echo "=== 3. les refus sont explicites (code 2) ==="
# `run` envoie stderr dans $T/err.txt : c'est LÀ que le refus se lit (l'essai qui cherchait dans
# la sortie de `run` a conclu « refus muet » sur un refus parfaitement dit — même famille que le
# message de la porte cherché dans le mauvais flux).
refus () { local desc="$1"; shift; run "$@" > "$T/refus.out" 2>&1; local c=$?
    [ "$c" = 2 ] || { echo "  ❌ $desc : code $c au lieu de 2"; exit 1; }
    grep -q "REFUS" "$T/err.txt" || { echo "  ❌ $desc : refus muet"; exit 1; }
    echo "  ✅ $desc"; }
refus "mémoire plus longue que la séquence" --sortie "$T/x.f32" --memoire 999 --sortie-memoire "$T/y.f32"
refus "mémoire sans fichier de sortie"      --sortie "$T/x.f32" --memoire "$K"

echo "=== 4. le ZÉRO est exprimable : --memoire 0 = pas de mémoire, même résultat ==="
run --sortie "$T/etats0.f32" --memoire 0 > "$T/out0.txt"; c0=$?
[ "$c0" = 0 ] || { echo "  ❌ --memoire 0 refusé (code $c0) : le zéro doit être exprimable"; exit 1; }
cmp -s "$T/etats2.f32" "$T/etats0.f32" || { echo "  ❌ --memoire 0 change le résultat"; exit 1; }
echo "  ✅ --memoire 0 accepté, et identique à l'absence du drapeau"
echo
echo "PORTE TENUE : la mémoire retient les K derniers signaux HORS du réseau, exactement, sans"
echo "coûter une seule paire, et elle refuse ce qu'elle ne peut pas faire. C'est la structure dont"
echo "la mesure de C8 avait montré l'absence (l'état : R² −0,68 ; un tampon : 1,000)."
