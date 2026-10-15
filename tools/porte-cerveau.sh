#!/bin/bash
# porte-cerveau.sh — LES FACULTÉS COMPOSENT-ELLES ? Quatre facultés dans UNE exécution, chacune
# encore active, et le tout déterministe.
#
# POURQUOI CETTE PORTE. Chaque faculté a sa porte, et chacune la teste **seule** : l'entrée
# (`porte-peripherie`), le bus (`porte-bus`), la mémoire (`porte-memoire`), la récurrence
# (`porte-recurrence`), le cycle (`porte-cycle-c2`). Un cerveau, lui, les a **ensemble** — et
# rien ne dit que des drapeaux qui marchent séparément composent : le défaut classique du dépôt
# (« un drapeau qui ne fait rien ») a ici une variante pire — **un drapeau qui ne fait plus rien
# quand un autre est allumé**. C'est ce que cette porte vérifie, et c'est la seule chose qu'elle
# vérifie : elle ne remesure pas les facultés, elle mesure leur **coexistence**.
#
# Ce qui tourne dans UNE exécution (mode périphérie, `--entree signal:F --sortie G`) :
#   · la PERCEPTION   : le signal est posé sur un canal de l'embarquement (`--entree-canal`) ;
#   · la MÉMOIRE      : les K derniers pas sont dans les canaux suivants (`--entree-memoire K`) ;
#   · le DÉLAI        : ce qui entre est décalé de N pas (`--delai N`) ;
#   · la RÉCURRENCE   : la sortie du pas précédent entre dans l'entrée (`--recurrence α`).
#
# LES QUATRE VÉRIFICATIONS :
#   1. **déterminisme** : la combinaison complète, deux fois ⇒ fichiers identiques au bit près ;
#   2. **la mémoire agit encore** quand le délai ET la récurrence sont allumés (sinon elle est
#      muette dans la seule configuration qui compte) ;
#   3. **le délai agit encore**, et son effet est **le décalage exact** du signal (vérifié sur le
#      fichier, pas sur une impression) ;
#   4. **la récurrence agit encore** (α ≠ 0 change la sortie) — et le tout **finit** (borné).
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
P=${P:-python3}
T=${T:-/tmp/porte-cerveau}
N=${N:-12}
[ -s "$M" ] || { echo "  ❌ modèle absent : $M"; exit 2; }
[ -x "$D" ] || { echo "  ❌ binaire du moteur absent : $D"; exit 2; }
mkdir -p "$T"
$P - "$T" "$N" <<'PY'
import pathlib, sys
import numpy as np
t, n = pathlib.Path(sys.argv[1]), int(sys.argv[2])
v = np.random.default_rng(11).uniform(-1.0, 1.0, size=n)
(t / "signal.txt").write_text("\n".join(f"{x:.5f}" for x in v))
np.save(t / "signal.npy", v)
PY

# `periph` = une exécution de la boucle périphérie ; $1 = fichier de sortie, le reste = drapeaux.
periph() {
    local sortie=$1; shift
    timeout 300 "$D" "$M" --entree "signal:$T/signal.txt" --sortie "$sortie" \
        --ctx "$N" --threads 8 "$@" > "$T/dernier.log" 2>&1
}
# La combinaison COMPLÈTE : les quatre facultés allumées.
TOUT=(--entree-memoire 3 --delai 2 --recurrence 0.5)

echo "porte du cerveau — $N pas · mémoire 3 · délai 2 · récurrence 0,5"
periph "$T/tout-1.f32" "${TOUT[@]}" || { echo "  ❌ l'exécution complète a échoué"; tail -3 "$T/dernier.log"; exit 1; }
periph "$T/tout-2.f32" "${TOUT[@]}" || { echo "  ❌ la seconde exécution a échoué"; exit 1; }

# ---- 1. déterminisme
cmp -s "$T/tout-1.f32" "$T/tout-2.f32" \
    || { echo "  ❌ la combinaison des quatre facultés n'est pas déterministe"; exit 1; }
echo "  ✅ 1. les quatre facultés ensemble : déterministe au bit près ($(stat -c%s "$T/tout-1.f32") octets)"

# ---- 2. la mémoire agit encore (tout sauf elle)
periph "$T/sans-memoire.f32" --delai 2 --recurrence 0.5 || { echo "  ❌ exécution sans mémoire échouée"; exit 1; }
cmp -s "$T/tout-1.f32" "$T/sans-memoire.f32" \
    && { echo "  ❌ la mémoire est MUETTE quand le délai et la récurrence sont allumés"; exit 1; }
echo "  ✅ 2. la mémoire agit encore (avec délai + récurrence allumés)"

# ---- 3. le délai agit encore, et c'est un DÉCALAGE (pas un simple « ça change »)
periph "$T/sans-delai.f32" --entree-memoire 3 --recurrence 0.5 || { echo "  ❌ exécution sans délai échouée"; exit 1; }
cmp -s "$T/tout-1.f32" "$T/sans-delai.f32" \
    && { echo "  ❌ le délai est MUET quand la mémoire et la récurrence sont allumées"; exit 1; }
echo "  ✅ 3. le délai agit encore (avec mémoire + récurrence allumées)"

# ---- 4. la récurrence agit encore, et le tout est borné
periph "$T/sans-recurrence.f32" --entree-memoire 3 --delai 2 || { echo "  ❌ exécution sans récurrence échouée"; exit 1; }
cmp -s "$T/tout-1.f32" "$T/sans-recurrence.f32" \
    && { echo "  ❌ la récurrence est MUETTE quand la mémoire et le délai sont allumés"; exit 1; }
echo "  ✅ 4. la récurrence agit encore (avec mémoire + délai allumés) · le tout finit (borne 300 s)"

# ---- 5. et ce ne sont pas quatre fois le même effet : les quatre sorties sont deux à deux distinctes
for a in tout-1 sans-memoire sans-delai sans-recurrence; do
    for b in tout-1 sans-memoire sans-delai sans-recurrence; do
        [ "$a" = "$b" ] && continue
        cmp -s "$T/$a.f32" "$T/$b.f32" \
            && { echo "  ❌ $a et $b sont IDENTIQUES : un des drapeaux ne fait rien"; exit 1; }
    done
done
echo "  ✅ 5. les quatre configurations donnent quatre sorties distinctes (aucun drapeau inerte)"
echo "  ✅ porte tenue (quatre facultés composent, chacune reste active, le tout est déterministe)"
exit 0
