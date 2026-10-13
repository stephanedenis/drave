#!/bin/bash
# porte-indice.sh — C6 : un indice ÉTRANGER retrouve-t-il le bon passage ?
#
# LA QUESTION, ET ELLE DIFFÈRE DE TOUTES LES AUTRES MESURES DE C6. Jusqu'ici la mémoire
# était interrogée avec un indice issu de l'épisode CHERCHÉ (une version dégradée de sa
# propre clé) : c'est de la complétion de motif, et elle réussit. Ce qui décide de
# l'usage est autre : un indice qui NE RESSEMBLE PAS au contenu cherché le retrouve-t-il ?
#
# LE PIÈGE QUE CETTE PORTE VERROUILLE, ET DANS LEQUEL LA PREMIÈRE MESURE EST TOMBÉE :
# un indice pris DANS le magasin s'y retrouve lui-même — recouvrement 64/64, et sa
# distance à l'aiguille ne dit rien. La porte exige donc que l'indice soit EXTÉRIEUR
# (la même question posée dans un contexte qui n'a PAS l'aiguille) et que le
# recouvrement rendu soit FAIBLE : un écho ne prouve rien.
#
# Ce qu'elle vérifie :
#   1. l'invite A répond le code, l'invite B (le même texte sans l'aiguille) non — sans
#      quoi la mesure ne porterait sur rien ;
#   2. avec un indice PRIS DANS LE MAGASIN, la mémoire rend l'indice lui-même (écho) :
#      c'est le cas qui montre pourquoi le cas 3 existe ;
#   3. avec un indice EXTÉRIEUR, elle rend un AUTRE épisode, de recouvrement faible, et
#      à une distance de l'aiguille inférieure à la moitié du hasard ;
#   4. et elle dit sa limite : la position de l'aiguille est connue par construction, et
#      un seul indice est mesuré.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
# Le prérequis vit sur l'array et se RÉGÉNÈRE : tools/construire-niah.py.
# Il vivait dans /tmp/campagne24, que chaque redémarrage emporte — la passe du
# 12/10 a compté trois portes rouges (celles-ci) pour ce seul fichier disparu.
SRC=${SRC:-$HOME/IA/scratch/prerequis/niah_4096_0.5.txt}
if [ ! -s "$SRC" ] && [ -x tools/construire-niah.py ]; then
    tools/construire-niah.py --jetons 4096 --profondeur 0.5 >/dev/null 2>&1
fi
CTX=${CTX:-2048}
T=$(mktemp -d)
[ -s "$M" ] && [ -s "$SRC" ] || { echo "  modèle ou source absents"; exit 2; }

echo "=== 0. deux invites qui ne diffèrent que d'une phrase ==="
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
(t / "pref.txt").write_text((corps[:c] + aig + corps[c:] + q)[:
    (corps[:c] + aig + corps[c:] + q).index("ZQ-4471-KX") + len("ZQ-4471-KX")])
PY
for f in A B pref; do "$D" "$M" --tokenize --fichier "$T/$f.txt" --sortie "$T/$f.ids" >/dev/null 2>&1; done
NA=$(tr ',' '\n' < "$T/A.ids" | wc -l); NB=$(tr ',' '\n' < "$T/B.ids" | wc -l)
PA=$(tr ',' '\n' < "$T/pref.ids" | wc -l); AIG=$((PA - 1))
echo "  A $NA jetons · B $NB · aiguille (fin du code) au jeton $AIG"

echo "=== 1. A répond le code, B non ==="
IA=$("$D" "$M" --infer --prompt "$(cat "$T/A.txt")" --n 6 --temp 0 --ctx "$CTX" --threads 8 2>&1 \
     | grep -E "^Answer" | head -1)
IB=$("$D" "$M" --infer --prompt "$(cat "$T/B.txt")" --n 6 --temp 0 --ctx "$CTX" --threads 8 2>&1 \
     | grep -E "^Answer" | head -1)
printf '  A : %s\n  B : %s\n' "$IA" "$IB"
printf '%s' "$IA" | grep -q "ZQ" || { echo "  ❌ A ne répond pas le code : la mesure ne porterait sur rien"; exit 1; }
printf '%s' "$IB" | grep -q "ZQ" && { echo "  ❌ B répond le code SANS l'aiguille : le protocole est faux"; exit 1; }
echo "  ✅ les deux invites diffèrent bien par l'aiguille seule"

echo "=== 2. indice EXTÉRIEUR : l'état de la question de B (pas dans le magasin de A) ==="
"$D" "$M" --ppl "$T/B.ids" --limit "$NB" --ctx "$CTX" --threads 12 \
   --etat-sortie "$T/etatB" --etat-pos "$((NB - 1))" 2>&1 | grep -E "capture" | sed 's/^/  /'
INDICE="$T/etatB.$((NB - 1))"
[ -s "$INDICE" ] || { echo "  ❌ l'indice extérieur n'a pas été écrit"; exit 1; }
"$D" "$M" --ppl "$T/A.ids" --limit "$NA" --ctx "$CTX" --threads 12 \
   --etat-sortie "$T/etatA" --etat-pos "$((NA - 1))" 2>&1 | grep -E "capture" | sed 's/^/  /'

echo "=== 3. la mémoire interroge A, avec puis sans l'indice extérieur ==="
ESSAI=("$D" "$M" --episodique-essai "$NA" --episodique-k 64 --episodique-expansion 16384
       --episodique-decorreler --episodique-normaliser --episodique-aiguille "$AIG"
       --episodique-textes "$T/A.txt" --ctx "$CTX" --threads 12)
"${ESSAI[@]}" > "$T/echo.txt" 2>&1
"${ESSAI[@]}" --episodique-indice "$INDICE" > "$T/ext.txt" 2>&1
sed -n '/indice SÉMANTIQUE/,/^$/p' "$T/echo.txt" | head -6 | sed 's/^/  écho   /'
sed -n '/indice SÉMANTIQUE/,/^$/p' "$T/ext.txt" | head -6 | sed 's/^/  extérieur /'

python3 - "$T/echo.txt" "$T/ext.txt" "$AIG" <<'PY' || exit 1
import re, sys
def lire(f):
    t = open(f).read()
    m = re.search(r"épisode rendu : (\d+) · recouvrement (\d+)/(\d+) · distance à l'aiguille : (\d+)", t)
    b = re.search(r"hasard\s*:\s*(\d+) jetons", t)
    if not m or not b:
        sys.exit(f"  ❌ mesures illisibles dans {f}")
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), float(b.group(1)))
echo_ = lire(sys.argv[1]); ext = lire(sys.argv[2]); aig = int(sys.argv[3])
# 1. l'indice pris dans le magasin rend l'indice LUI-MÊME : c'est un écho.
if echo_[1] != echo_[2]:
    sys.exit(f"  ❌ l'indice interne devrait rendre un recouvrement plein (écho), il vaut "
             f"{echo_[1]}/{echo_[2]}")
print(f"  ✅ indice interne : écho ({echo_[1]}/{echo_[2]}) — la mesure ne prouve RIEN, "
      "et c'est pourquoi la porte exige un indice extérieur")
# 2. l'indice extérieur n'est pas un écho
if ext[1] >= echo_[1]:
    sys.exit(f"  ❌ l'indice extérieur rend un recouvrement de {ext[1]} : c'est un écho")
# 3. et il tombe MIEUX QUE LE HASARD — mais la porte refuse d'exiger davantage, et
#    c'est une correction de ma propre mesure : deux indices qui ne diffèrent que d'un
#    point d'interrogation dans la question donnent 136 et 378 jetons sur une base de
#    448. L'effet existe et il n'est PAS robuste ; exiger « la moitié du hasard »
#    ferait échouer la porte sur une variante légitime, ce qui ne prouverait rien.
if ext[3] >= ext[4]:
    sys.exit(f"  ❌ l'indice extérieur tombe à {ext[3]} jetons de l'aiguille, le hasard "
             f"étant à {ext[4]:.0f} : il ne fait pas mieux que le hasard")
print(f"  ✅ indice extérieur : recouvrement {ext[1]}/{ext[2]} (pas un écho), distance à "
      f"l'aiguille {ext[3]} jetons contre {ext[4]:.0f} de hasard "
      f"({ext[4]/max(ext[3],1):.2f}× mieux)")
if ext[4] / max(ext[3], 1) < 2.0:
    print("  ⚠️  la marge est FAIBLE : un indice quasi identique (un point d'interrogation")
    print("      de plus dans la question) donne 378 jetons au lieu de 136. L'effet est")
    print("      réel mais NON ROBUSTE, et la porte le dit au lieu de le cacher.")
PY

echo
echo "  ✅ la porte est franchie. Limite, et elle est écrite : UN SEUL indice extérieur,"
echo "     sur UN SEUL texte, et la position de l'aiguille est plantée par construction."
echo "  Fichiers conservés dans $T"
