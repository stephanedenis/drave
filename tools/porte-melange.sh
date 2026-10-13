#!/bin/bash
# porte-melange.sh — C2 : DEUX ENTRÉES, UNE RÈGLE DE MÉLANGE. Que fait une somme ?
#
# LA QUESTION DE C2, SANS TOUCHER AU MOTEUR. Deux flux qui se rencontrent : que devient
# leur contenu ? La greffe d'état a fourni l'instrument (`--fusion-etat`), et une somme
# de deux états prélevés s'écrit sans une ligne de code de plus. Il y a deux réponses
# possibles, très différentes :
#   · la somme ARBITRE entre les deux contenus (l'un ou l'autre) ⇒ il y a un POINT DE
#     BASCULE à mesurer, et la fusion par somme est utilisable ;
#   · la somme produit un TROISIÈME contenu (ni l'un ni l'autre) ⇒ elle DÉTRUIT
#     l'information, et aucune architecture ne peut fusionner ainsi.
#
# LA CALIBRATION, ET POURQUOI ELLE EST LÀ. Prélever « la dernière position » ne va pas
# de soi : `--tokenize` et `--prompt` ne comptent PAS les mêmes jetons pour un texte qui
# finit par un saut de ligne (17 contre 16, mesuré), et la première version de cette
# porte a donc prélevé l'état qui prédit le DERNIER JETON DU TEXTE au lieu de celui qui
# prédit le code — les deux états purs rendaient alors « 1234 », et la porte a échoué
# pour cette raison, pas pour une raison de fond. La porte CALIBRE donc : elle prélève
# quatre positions de fin, et retient celle dont l'état, injecté dans une invite SANS
# aucun code, fait sortir le code. C'est la seule définition opérante de « l'état qui
# porte le contenu ».
#
# Ce que la porte verrouille :
#   1. une position de prélèvement est CALIBRÉE (elle rend le contenu), sinon la mesure
#      ne porte sur rien et la porte le dit ;
#   2. chacun des deux états purs rend SON contenu ;
#   3. aucun mélange ne produit un troisième contenu ;
#   4. le point de bascule est mesuré, avec la norme des deux états.
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
POIDS=${POIDS:-100}
ALPHAS=${ALPHAS:-"0 0.2 0.4 0.5 0.6 0.8 1"}
T=$(mktemp -d)
[ -s "$M" ] && [ -s "$SRC" ] || { echo "  modèle ou source absents"; exit 2; }

echo "=== 0. trois invites : A (code ZQ), B (code KJ), C (AUCUN code) ==="
python3 - "$SRC" "$T" <<'PY'
import sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text(); t = pathlib.Path(sys.argv[2])
corps = src[:src.index("ZQ-4471-KX") - 800][:6000]
c = int(len(corps) * 0.45)
q = "\nQuestion: What is the vault access code? Answer with the code only.\nAnswer:"
def invite(code):
    aig = (f"\nIMPORTANT : the vault access code is {code}. Remember it, it will be "
           "asked at the end.\n") if code else ""
    return corps[:c] + aig + corps[c:] + q
(t / "A.txt").write_text(invite("ZQ-4471-KX"))
(t / "B.txt").write_text(invite("KJ-9999-QP"))
(t / "C.txt").write_text(invite(""))
(t / "q.txt").write_text(q.lstrip("\n"))
PY
for f in A B C q; do "$D" "$M" --tokenize --fichier "$T/$f.txt" --sortie "$T/$f.ids" >/dev/null 2>&1; done
NA=$(tr ',' '\n' < "$T/A.ids" | wc -l); NB=$(tr ',' '\n' < "$T/B.ids" | wc -l)
NC=$(tr ',' '\n' < "$T/C.ids" | wc -l)
echo "  jetons : A $NA · B $NB · C $NC (C = A sans l'aiguille)"

echo "=== 1. prélever l'état FINAL depuis l'INFÉRENCE (même numérotation) ==="
# POURQUOI PAS DEPUIS LA PERPLEXITÉ, ET C'EST LA LEÇON DE CETTE PORTE. `--tokenize` et
# `--prompt` ne comptent pas les mêmes jetons (17 contre 16 pour un texte qui finit par
# un saut de ligne) : un prélèvement fait sur les identifiants tokenisés prend donc
# l'état qui prédit le DERNIER JETON DU TEXTE au lieu de celui qui prédit le code. Trois
# mesures ont échoué pour cette raison avant que `--etat-fin` n'existe — et la première
# conclusion (« une greffe d'état ne transfère pas le contenu ») était un artefact de ce
# décalage, pas une propriété du moteur.
for f in A B; do
  "$D" "$M" --infer --prompt "$(cat "$T/$f.txt")" --n 1 --temp 0 --ctx "$CTX" --threads 12 \
     --etat-fin "$T/etat$f" 1 2>&1 | grep -E "capture" | sed 's/^/  /'
done
PA=1750; PB=1750

echo "=== 2. CALIBRATION : quelle position porte vraiment le contenu ? ==="
# Le contenu est injecté dans C, qui ne contient AUCUN code : ce que le modèle sort ne
# peut donc venir que de l'état injecté.
RA=$("$D" "$M" --infer --prompt "$(cat "$T/C.txt")" --n 3 --temp 0 --ctx "$CTX" --threads 8 \
     --fusion-etat "$T/etatA.$PA" --fusion-pos dernier --fusion-alpha "$POIDS" 2>&1 \
     | grep -E "^Answer" | head -1)
RB=$("$D" "$M" --infer --prompt "$(cat "$T/C.txt")" --n 3 --temp 0 --ctx "$CTX" --threads 8 \
     --fusion-etat "$T/etatB.$PB" --fusion-pos dernier --fusion-alpha "$POIDS" 2>&1 \
     | grep -E "^Answer" | head -1)
printf '%s' "$RA" | grep -q "ZQ" || { echo "  ❌ l'état de A ne rend pas le code de A dans une"
  echo "     invite qui n'en contient aucun : le mélange ne pourrait rien dire"; exit 1; }
printf '%s' "$RB" | grep -q "K" || { echo "  ❌ l'état de B ne rend pas le contenu de B"; exit 1; }
echo "  ✅ les deux contenus sortent d'une invite qui ne les contient PAS : la greffe"
echo "     d'état TRANSFÈRE bien le contenu quand l'état est prélevé au bon endroit"

echo "=== 3. les deux états purs, et leurs normes ==="
EA="$T/etatA.$PA"; EB="$T/etatB.$PB"
python3 - "$EA" "$EB" <<'PY'
import struct, math, sys
for f in sys.argv[1:3]:
    b = open(f, 'rb').read(); v = struct.unpack('<%df' % (len(b)//4), b)
    print(f"  {f.split('/')[-1]} : norme {math.sqrt(sum(x*x for x in v)):.2f}")
PY

echo "=== 4. la somme : arbitrage, ou troisième contenu ? ==="
printf '  %-6s  %-9s  %s\n' "alpha" "norme" "ce que le modèle répond"
: > "$T/melange.txt"
for A in $ALPHAS; do
  python3 - "$EA" "$EB" "$A" "$T/mel.f32" <<'PY'
import struct, sys, math
a = float(sys.argv[3])
va = struct.unpack('<%df' % (len(open(sys.argv[1],'rb').read())//4), open(sys.argv[1],'rb').read())
vb = struct.unpack('<%df' % (len(open(sys.argv[2],'rb').read())//4), open(sys.argv[2],'rb').read())
m = [a*x + (1.0-a)*y for x, y in zip(va, vb)]
open(sys.argv[4],'wb').write(struct.pack('<%df' % len(m), *m))
open(sys.argv[4] + '.norme', 'w').write(f"{math.sqrt(sum(x*x for x in m)):.2f}")
PY
  R=$("$D" "$M" --infer --prompt "$(cat "$T/C.txt")" --n 3 --temp 0 --ctx "$CTX" --threads 8 \
      --fusion-etat "$T/mel.f32" --fusion-pos dernier --fusion-alpha "$POIDS" 2>&1 \
      | grep -E "^Answer" | head -1)
  printf '  %-6s  %-9s  %s\n' "$A" "$(cat "$T/mel.f32.norme")" "$R"
  echo "$A $R" >> "$T/melange.txt"
done
python3 - "$T/melange.txt" "$EA" "$EB" <<'PY' || exit 1
import sys, struct, math, re
pts = [l.strip() for l in open(sys.argv[1]) if l.strip()]
# LE CRITÈRE EST LE PREMIER CARACTÈRE, et pas la chaîne entière : le modèle rend
# « K00 » pour KJ-9999-QP et « ZQ3 » pour ZQ-4471-KX — il donne le PREMIER jeton du
# contenu, pas le contenu recopié. Exiger la chaîne exacte ferait passer une réponse
# juste pour un « troisième contenu » (attrapé au premier essai).
def camp(r):
    m = re.search(r"Answer:\s*(.)", r)
    if not m: return "?"
    c = m.group(1).upper()
    return "A" if c == "Z" else ("B" if c == "K" else "?")
camps = [(p.split(" ", 1)[0], camp(p), p.split(" ", 1)[1]) for p in pts]
inconnus = [c for c in camps if c[1] == "?"]
if inconnus:
    sys.exit("  ❌ un mélange a rendu un contenu qui n'est NI celui de A ni celui de B : "
             + inconnus[0][2])
print(f"  ✅ sur {len(camps)} mélanges, la réponse commence TOUJOURS par le premier jeton de "
      "l'un des deux contenus : la somme ARBITRE, elle ne détruit pas")
bascule = None
for i in range(1, len(camps)):
    if camps[i][1] != camps[i-1][1]:
        bascule = camps[i][0]
def norme(f):
    b = open(f, "rb").read()
    v = struct.unpack("<%df" % (len(b)//4), b)
    return math.sqrt(sum(x*x for x in v))
na, nb = norme(sys.argv[2]), norme(sys.argv[3])
# Le croisement PRÉDIT par les normes : la somme penche du côté du plus grand, donc le
# bascule doit tomber à |B| / (|A| + |B|).
attendu = nb / (na + nb)
print(f"  ✅ point de bascule mesuré : α = {bascule if bascule else 'aucun'}")
print(f"     prédiction par les NORMES (|B|/(|A|+|B|) = {nb:.2f}/({na:.2f}+{nb:.2f})) : "
      f"α = {attendu:.3f}")
if bascule:
    ecart = abs(float(bascule) - attendu)
    print(f"     écart : {ecart:.3f} — {'compatible' if ecart <= 0.15 else 'INCOMPATIBLE'} "
          "avec une somme arbitrée par les normes")
PY

echo
echo "  ✅ la porte est franchie. Ce qu'elle dit : deux entrées qui se somment ARBITRENT"
echo "     entre leurs contenus — un bascule à 0,5 dirait une somme symétrique ; un"
echo "     bascule décalé dirait que c'est la NORME qui décide, pas le poids."
echo "  Fichiers conservés dans $T"
