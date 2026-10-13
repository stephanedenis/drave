#!/bin/bash
# greffe_etat.sh — C2/C6 : la GREFFE D'ÉTAT. Un souvenir peut-il être injecté dans un
# calcul qui ne l'a pas vécu ?
#
# LA QUESTION, ET ELLE EST CELLE DE LA MÉMOIRE QUI SERT. C6 sait stocker et retrouver
# un état par son contenu ; C9 sait limiter ce qui traverse un lien. Ce qui n'était pas
# mesuré est le PASSAGE : si l'on injecte l'état d'un moment vécu dans un calcul qui ne
# l'a pas vécu, l'information qu'il portait est-elle encore là ? C'est ce qu'un cerveau
# fait quand l'hippocampe rappelle un épisode au cortex.
#
# LE PROTOCOLE, ET IL EST DÉCISIF PARCE QU'IL COMPARE DEUX INVITES QUI NE DIFFÈRENT QUE
# D'UNE PHRASE :
#   · invite A = remplissage + « IMPORTANT : the vault access code is ZQ-4471-KX. » +
#     la question. Le modèle répond « ZQ-4471-K » ;
#   · invite B = le MÊME texte, l'aiguille EN MOINS. Le modèle ne peut pas répondre ;
#   · on prélève l'état BRUT (après la dernière couche) à la DERNIÈRE position de A, et
#     on l'injecte à la dernière position de B, avec un poids balayé.
# Si B + greffe répond le code, l'état transplanté PORTE l'information jusqu'à la sortie.
# Si B + greffe ne le répond pas, alors un état résiduel ne suffit pas — et c'est un
# résultat, avec sa cause à chercher (l'échelle, la direction, ou le fait que la tête
# a besoin de tout le contexte et pas d'un état).
#
# POURQUOI UNE INVITE COURTE (1 500 jetons) ET NON 4 152 : la mécanique se mesure sur
# une invite qui tient en une passe de quelques secondes. Une première version à 4 152
# jetons coûtait 400 s par prélèvement, pour la même question.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
# LA BOTTE DE FOIN EST VERSIONNÉE ICI (`tools/niah_4096_0.5.txt`), et c'est une correction de
# méthode : celle de la campagne (8-10 octobre) vivait dans `/tmp/campagne24/`, donc elle a
# disparu au premier redémarrage, et trois portes ont rendu « code 2 » le 12/10 pour ce seul
# fichier. Un fichier d'entrée de mesure qui n'est pas versionné rend la mesure non
# reproductible : on ne peut plus distinguer « le moteur a changé » de « l'entrée a changé ».
# `tools/construire-niah.py` le régénère si besoin (même graine, même corpus).
SRC=${SRC:-tools/niah_4096_0.5.txt}
if [ ! -s "$SRC" ] && [ -x tools/construire-niah.py ]; then
    tools/construire-niah.py --jetons 4096 --profondeur 0.5 --sortie "$SRC" >/dev/null 2>&1
fi
CTX=${CTX:-2048}
ALPHAS=${ALPHAS:-"0 1 2 4 10 100"}
T=$(mktemp -d)
[ -s "$M" ] && [ -s "$SRC" ] || { echo "  modèle ou source absents"; exit 2; }

echo "=== 0. construire les deux invites (mêmes textes, l'aiguille en moins) ==="
python3 - "$SRC" "$T" <<'PY'
import sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text(); t = pathlib.Path(sys.argv[2])
corps = src[:src.index("ZQ-4471-KX") - 800][:6000]
coupe = int(len(corps) * 0.45)
aig = ("\nIMPORTANT : the vault access code is ZQ-4471-KX. Remember it, it will be "
       "asked at the end.\n")
q = "\nQuestion: What is the vault access code? Answer with the code only.\nAnswer:"
(t / "A.txt").write_text(corps[:coupe] + aig + corps[coupe:] + q)
(t / "B.txt").write_text(corps[:coupe] + corps[coupe:] + q)
(t / "q.txt").write_text(q.lstrip("\n"))
print(f"  invite A {len((t/'A.txt').read_text())} octets · B "
      f"{len((t/'B.txt').read_text())} octets · question seule "
      f"{len((t/'q.txt').read_text())} octets")
PY
for f in A B q; do "$D" "$M" --tokenize --fichier "$T/$f.txt" --sortie "$T/$f.ids" >/dev/null 2>&1; done
NA=$(tr ',' '\n' < "$T/A.ids" | wc -l); NB=$(tr ',' '\n' < "$T/B.ids" | wc -l)
NQ=$(tr ',' '\n' < "$T/q.ids" | wc -l)
echo "  jetons : A $NA · B $NB · question $NQ"
[ "$NA" -gt 10 ] && [ "$NB" -gt 10 ] || { echo "  ❌ tokenisation vide"; exit 1; }

echo "=== 1. ce que chaque invite répond SANS greffe ==="
gen() { # $1 = fichier texte, reste = drapeaux
  local f=$1; shift
  "$D" "$M" --infer --prompt "$(cat "$f")" --n 8 --temp 0 --ctx "$CTX" --threads 12 "$@" 2>&1
}
GA=$(gen "$T/A.txt"); GA1=$(printf '%s\n' "$GA" | grep -E "^Answer" | head -1)
GB=$(gen "$T/B.txt"); GB1=$(printf '%s\n' "$GB" | grep -E "^Answer" | head -1)
GQ=$(gen "$T/q.txt"); GQ1=$(printf '%s\n' "$GQ" | grep -E "^Answer" | head -1)
printf '  A (avec aiguille) : %s\n  B (sans aiguille) : %s\n  question seule    : %s\n' \
       "$GA1" "$GB1" "$GQ1"
printf '%s' "$GA1" | grep -q "ZQ" || { echo "  ⚠️  A ne répond pas le code : la greffe";
  echo "     ne pourrait rien prouver. Choisir une autre invite ou un autre modèle."; }

echo "=== 2. prélever l'état de la DERNIÈRE position de A (une seule passe) ==="
$D "$M" --ppl "$T/A.ids" --limit "$NA" --ctx "$CTX" --threads 12 \
   --etat-sortie "$T/etatA" --etat-pos "$((NA - 1))" 2>&1 | grep -E "capture|perplexité" | sed 's/^/  /'
[ -s "$T/etatA.$((NA - 1))" ] || { echo "  ❌ l'état n'a pas été écrit"; exit 1; }
python3 - "$T/etatA.$((NA - 1))" <<'PY'
import struct, math, sys
b = open(sys.argv[1], 'rb').read()
v = struct.unpack('<%df' % (len(b) // 4), b)
print(f"  état prélevé : {len(v)} valeurs · rms {math.sqrt(sum(x*x for x in v)/len(v)):.3f} "
      f"· norme {math.sqrt(sum(x*x for x in v)):.2f}")
PY

echo "=== 3. greffer dans B (dernière position) ==="
printf '  %-8s  %s\n' "poids" "ce que B répond AVEC la greffe"
for A in $ALPHAS; do
  R=$(gen "$T/B.txt" --fusion-etat "$T/etatA.$((NA - 1))" --fusion-pos dernier --fusion-alpha "$A")
  L=$(printf '%s\n' "$R" | grep -E "^Answer" | head -1)
  printf '  %-8s  %s\n' "$A" "$L"
  printf '%s' "$L" | grep -q "ZQ" && echo "            ✅ la greffe a porté le code"
done
echo
echo "  lecture : le poids 0 est le témoin de non-effet. Si aucun poids ne porte le code,"
echo "  l'état transplanté ne suffit pas — et la cause est à chercher du côté de ce que la"
echo "  tête lit (l'échelle, la position, ou le contexte entier plutôt qu'un état)."
echo "  Fichiers conservés dans $T"
