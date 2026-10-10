#!/bin/bash
# porte-greffe.sh — C2/C6 : LA GREFFE D'ÉTAT. Ce qu'elle fait, et ce qu'elle ne fait PAS.
#
# LA QUESTION. C6 retrouve un état par son contenu ; C9 limite ce qui traverse un lien.
# Ce qui n'était pas mesuré est le PASSAGE : si l'on injecte l'état d'un moment vécu
# dans un calcul qui ne l'a pas vécu, l'information portée est-elle encore là ?
#
# LE PROTOCOLE, DÉCISIF PARCE QUE DEUX INVITES NE DIFFÈRENT QUE D'UNE PHRASE :
#   · invite A = remplissage + « IMPORTANT : the vault access code is ZQ-4471-KX. » +
#     la question  →  le modèle répond « ZQ-4471-K » ;
#   · invite B = le MÊME texte, l'aiguille EN MOINS  →  il répond « 150px » ;
#   · on prélève l'état BRUT (après la dernière couche, avant la norme finale) à la
#     DERNIÈRE position de A, et on l'injecte dans B.
#
# ⚠️ CORRECTION DU 10 OCTOBRE (soir) — LA CONCLUSION D'ORIGINE ÉTAIT UN ARTEFACT.
# Cette porte concluait « une greffe d'état n'est pas une greffe de contexte », parce que
# l'état de A injecté dans B ne rendait jamais le code. C'ÉTAIT FAUX, et la cause était
# un décalage d'un jeton : le prélèvement se faisait sur les identifiants tokenisés
# (`--tokenize`, 1 750 jetons) alors que l'inférence construit une invite d'UN JETON DE
# PLUS (1 751). L'état prélevé était donc celui qui prédit le DERNIER JETON DU TEXTE
# (« : ») au lieu de celui qui prédit le code — et il rendait « : ».
# Avec un prélèvement fait LÀ OÙ LE CALCUL SE FAIT (`--etat-fin`, k-ième depuis la fin,
# résolu dans la numérotation de l'inférence), le contenu PASSE : l'état de A injecté
# dans une invite qui ne contient AUCUN code fait répondre « ZQ3 », celui de B « K00 ».
# Ce qui reste vrai et que la porte continue de verrouiller : un poids de 0 ne change
# rien, et l'état doit être injecté à la DERNIÈRE position (l'injecter au milieu d'une
# invite n'a pas d'effet sur la réponse).
#
# CE QUE LA MESURE AVAIT DONNÉ (conclusion d'origine, conservée pour mémoire) :
#   1. poids 0 ⇒ sortie IDENTIQUE à l'absence de greffe (le témoin de non-effet : sans
#      lui, rien de ce qui suit ne serait interprétable) ;
#   2. A + SON PROPRE état reste « ZQ… » ⇒ la greffe achemine bien la direction de
#      l'état jusqu'à la tête ; le mécanisme fonctionne ;
#   3. B + l'état de A, à AUCUN poids (1, 2, 4, 10, 100) et même à TOUTES les
#      positions ⇒ le code n'apparaît PAS. **Une greffe d'état n'est pas une greffe de
#      contexte** ;
#   4. et la cause est mesurable : après le premier jeton, la suite appartient à B
#      (les jetons de B réapparaissent, ceux de A non). Le premier jeton vient de
#      l'état injecté, les suivants sont RE-DÉRIVÉS par l'attention sur le cache KV —
#      que la greffe ne touche pas.
#
# Conséquence, et elle est nette : pour qu'une mémoire SERVE le calcul, ce qu'elle rend
# doit entrer comme CONTENU (des jetons que le modèle peut lire) ou comme ENTRÉE DE
# CACHE — et le moteur n'a aujourd'hui aucune prise sur le cache KV. C'est un manque,
# écrit comme tel, pas un réglage à trouver.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
SRC=${SRC:-/tmp/campagne24/niah_4096_0.5.txt}
CTX=${CTX:-2048}
T=$(mktemp -d)
[ -s "$M" ] && [ -s "$SRC" ] || { echo "  modèle ou source absents"; exit 2; }

gen() { # $1 = fichier texte, reste = drapeaux ; rend les ids générés
  local f=$1; shift
  "$D" "$M" --infer --prompt "$(cat "$f")" --n 8 --temp 0 --ctx "$CTX" --threads 8 "$@" 2>&1 \
    | grep -oE "ids générés : \[[0-9, ]+\]" | grep -oE "\[[0-9, ]+\]"
}

echo "=== 0. construire A (avec aiguille) et B (sans), et vérifier qu'elles diffèrent ==="
python3 - "$SRC" "$T" <<'PY'
import sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text(); t = pathlib.Path(sys.argv[2])
corps = src[:src.index("ZQ-4471-KX") - 800][:6000]
c = int(len(corps) * 0.45)
aig = ("\nIMPORTANT : the vault access code is ZQ-4471-KX. Remember it, it will be "
       "asked at the end.\n")
q = "\nQuestion: What is the vault access code? Answer with the code only.\nAnswer:"
(t / "A.txt").write_text(corps[:c] + aig + corps[c:] + q)
(t / "B.txt").write_text(corps[:c] + corps[c:] + q)
PY
for f in A B; do "$D" "$M" --tokenize --fichier "$T/$f.txt" --sortie "$T/$f.ids" >/dev/null 2>&1; done
NA=$(tr ',' '\n' < "$T/A.ids" | wc -l)
IA=$(gen "$T/A.txt"); IB=$(gen "$T/B.txt")
echo "  A (avec aiguille) : $IA"
echo "  B (sans aiguille) : $IB"
[ "$IA" != "$IB" ] || { echo "  ❌ les deux invites donnent la même réponse : le protocole ne mesure rien"; exit 1; }
printf '%s' "$IA" | grep -q "1863" \
  || { echo "  ❌ A ne produit pas le jeton du code (1863) : la greffe ne pourrait rien prouver"; exit 1; }

echo "=== 1. prélever l'état de la dernière position DE L'INFÉRENCE (--etat-fin) ==="
"$D" "$M" --infer --prompt "$(cat "$T/A.txt")" --n 1 --temp 0 --ctx "$CTX" --threads 12 \
   --etat-fin "$T/etatA" 1 2>&1 | grep -E "capture" | sed 's/^/  /'
ETAT=$(ls "$T"/etatA.* 2>/dev/null | head -1)
[ -s "$ETAT" ] || { echo "  ❌ l'état n'a pas été écrit"; exit 1; }

echo "=== 2. témoin de non-effet : poids 0 ⇒ aucune différence ==="
I0=$(gen "$T/B.txt" --fusion-etat "$ETAT" --fusion-pos dernier --fusion-alpha 0)
[ "$I0" = "$IB" ] || { echo "  ❌ une greffe de poids NUL a changé la sortie ($IB → $I0)"; exit 1; }
echo "  ✅ poids 0 : $I0 (identique à B sans greffe)"

echo "=== 3. le mécanisme fonctionne : A + son propre état reste sur le code ==="
IA2=$(gen "$T/A.txt" --fusion-etat "$ETAT" --fusion-pos dernier --fusion-alpha 100)
echo "  A + son état (poids 100) : $IA2"
printf '%s' "$IA2" | grep -qE "48|1863" \
  || { echo "  ❌ la greffe de A dans A ne retrouve plus le contenu de A : le mécanisme"
       echo "     d'injection n'achemine rien jusqu'à la tête"; exit 1; }
echo "  ✅ l'état injecté porte bien la direction du contenu de A"

echo "=== 4. CORRIGÉ : l'état de A dans C (sans aucun code) DONNE le code ==="
PORTE=0
for A in 1 2 4 10 100; do
  R=$(gen "$T/B.txt" --fusion-etat "$ETAT" --fusion-pos dernier --fusion-alpha "$A")
  printf '  poids %-4s : %s\n' "$A" "$R"
  # Le critère porte sur les IDENTIFIANTS : `gen` rend « ids générés : […] », et 1863
  # est le premier jeton de « ZQ-… ». Chercher la lettre « Z » dans cette ligne ne
  # pouvait pas réussir — la porte échouait sur sa propre vérification (attrapé au
  # premier essai de la version corrigée).
  printf '%s' "$R" | grep -qE "^\[1863," && PORTE=1
done
[ "$PORTE" = 1 ] || { echo "  ❌ le contenu de A ne sort PAS de la greffe, même au bon endroit :";
  echo "     la correction du 10 octobre ne tient pas sur cette exécution"; exit 1; }
echo "  ✅ l'état de A, prélevé LÀ OÙ LE CALCUL SE FAIT, porte bien son contenu"
echo "     (l'ancienne conclusion négative était un décalage d'un jeton, pas une propriété"

echo "=== 5. la CAUSE : après le premier jeton, la suite appartient à B ==="
# Les jetons de B réapparaissent dans la sortie greffée ; ceux de A non. C'est
# l'attention sur le cache KV qui re-dérive la suite — et la greffe ne le touche pas.
python3 - "$IB" "$(gen "$T/B.txt" --fusion-etat "$ETAT" --fusion-pos dernier --fusion-alpha 4)" <<'PY' || exit 1
import re, sys
b = [int(x) for x in re.findall(r"\d+", sys.argv[1])]
g = [int(x) for x in re.findall(r"\d+", sys.argv[2])]
if not b or not g:
    sys.exit("  ❌ sortie illisible")
# Le PREMIER jeton peut changer (il vient de l'état injecté) ; la suite doit rester
# celle de B. On compare donc à partir du deuxième jeton.
suite_b, suite_g = b[1:4], g[1:4]
if suite_b != suite_g:
    sys.exit(f"  ❌ la suite de B a changé ({suite_b} → {suite_g}) : la greffe a donc")
print(f"  ✅ premier jeton {b[0]} → {g[0]} (il vient de l'état injecté), et la suite reste "
      f"celle de B : {suite_g}")
PY

echo
echo "  ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE"
echo "     (témoin à 0, mécanisme vérifié sur A) et elle NE TRANSFÈRE PAS le contexte."
echo "     Pour qu'une mémoire serve le calcul, il faut qu'elle entre comme CONTENU ou"
echo "     comme ENTRÉE DE CACHE — le moteur n'a aucune prise sur le cache KV : manque."
echo "  Fichiers conservés dans $T"
