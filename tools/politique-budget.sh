#!/bin/bash
# politique-budget.sh — LE BUDGET D'ATTENTION A-T-IL UNE BONNE TAILLE PAR TEXTE ?
#
# LA QUESTION, ET ELLE EST CELLE DU PLAN (C5 modulation, C10 budgets). Le dépôt a mesuré :
#   · garder **la moitié** des clés coûte de **+0,4 % à +3,0 %** selon le texte, le **quart** de
#     +2,8 % à +49,2 % (rapport-loi-frontiere-fenetre.md) ;
#   · et **où** dépenser (uniforme ou par couche) est un levier de **second ordre**
#     (rapport-budget-attention-allocation.md).
# Ce qui n'est pas mesuré est la conséquence pratique : si le coût dépend du texte, alors **un
# budget uniforme est soit trop cher, soit insuffisant** — et une **politique** (donner à chaque
# texte ce qu'il lui faut) devrait battre l'uniforme **à budget moyen égal**.
#
# CE QUE CE SCRIPT MESURE, ET COMMENT IL LE DIT. Sur N textes et trois budgets (toutes les clés,
# la moitié, le quart), il relève la perplexité du MOTEUR, puis :
#   1. pour chaque texte, le **budget minimal** qui reste à ≤ +1 % du budget complet ;
#   2. ce que coûte une **politique uniforme** (« la moitié partout ») : combien de textes passent
#      le +1 %, et de combien elle dépasse sur les autres ;
#   3. ce que coûte la **politique par texte** au **même budget moyen** — et c'est la comparaison
#      qui tranche.
#
# ⚠️ CE N'EST PAS UNE PORTE : elle ne juge pas, elle mesure. Et elle ne prétend pas qu'une
# politique est *implémentée* : elle mesure ce qu'une politique **donnerait**, à partir de trois
# exécutions réelles par texte.
#
# Usage : tools/politique-budget.sh [--limite 512]
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
P=${P:-python3}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
LIMITE=${LIMITE:-512}
TOLERANCE=${TOLERANCE:-1.0}
PUITS=${PUITS:-64}
T=${T:-/tmp/politique-budget}
MORCEAUX=${MORCEAUX:-"5 10 15 20 25 30 31 32"}
[ -s "$M" ] || { echo "  ❌ modèle absent : $M"; exit 2; }
[ -x "$D" ] || { echo "  ❌ binaire du moteur absent : $D"; exit 2; }
. tools/_corpus.sh
mkdir -p "$T"

$P - "$IDS" "$T" "$LIMITE" "$MORCEAUX" <<'PY'
import pathlib, re, sys
ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(sys.argv[1]).read_text()) if x.strip()]
t, taille = pathlib.Path(sys.argv[2]), int(sys.argv[3])
idx = [int(x) for x in sys.argv[4].split()]
pas = len(ids) // 34
for i in idx:
    (t / f"m{i}.txt").write_text(",".join(str(x) for x in ids[i * pas: i * pas + taille]))
PY

ppl() {   # $1 = fichier, $2 = drapeaux
    "$D" "$M" --ppl "$1" --limit "$LIMITE" --ctx "$LIMITE" --threads 8 $2 2>&1 \
        | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+" | head -1
}

# LE FICHIER DE MESURES EST REPARTI DE ZÉRO : sans cela, une deuxième exécution AJOUTE ses lignes
# aux précédentes et le tableau compte 16 textes au lieu de 8 (attrapé en relançant le script).
rm -f "$T/mesures.txt"
echo "politique de budget — $(basename "$M") · $LIMITE jetons · tolérance +$TOLERANCE %"
echo
printf '%-6s %14s %14s %14s\n' "texte" "complet" "moitié" "quart"
for i in $MORCEAUX; do
    f="$T/m$i.txt"
    p_c=$(ppl "$f" "")
    p_m=$(ppl "$f" "--attn-window $((LIMITE / 2)) --attn-sinks $PUITS")
    p_q=$(ppl "$f" "--attn-window $((LIMITE / 4)) --attn-sinks $PUITS")
    [ -n "$p_c" ] && [ -n "$p_m" ] && [ -n "$p_q" ] || { echo "  ❌ perplexité illisible sur m$i"; exit 1; }
    printf '%-6s %14s %14s %14s\n' "m$i" "$p_c" "$p_m" "$p_q"
    echo "$i $p_c $p_m $p_q" >> "$T/mesures.txt"
done

echo
$P - "$T/mesures.txt" "$TOLERANCE" "$LIMITE" "$PUITS" <<'PY'
import pathlib, sys
lignes = [l.split() for l in pathlib.Path(sys.argv[1]).read_text().splitlines() if l.strip()]
tol, limite, puits = float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
# clés par couche (moyenne) : complet = limite ; moitié = limite/2 + puits ; quart = limite/4 + puits
cles = {"complet": limite, "moitié": limite / 2 + puits, "quart": limite / 4 + puits}
lignes = [(int(i), float(c), float(m), float(q)) for i, c, m, q in lignes]
print(f"| texte | complet | moitié | quart | budget minimal ≤ +{tol:g} % | clés de ce budget |")
print("|---|---:|---:|---:|---|---:|")
minimal = {}
for i, c, m, q in lignes:
    choix = "complet"
    if (m - c) / c * 100 <= tol:
        choix = "moitié"
        if (q - c) / c * 100 <= tol:
            choix = "quart"
    minimal[i] = choix
    print(f"| m{i} | {c:,.4f} | {m:,.4f} ({(m-c)/c*100:+.2f} %) | {q:,.4f} ({(q-c)/c*100:+.2f} %) | "
          f"**{choix}** | {cles[choix]:.0f} |")
n = len(lignes)
moyenne_politique = sum(cles[minimal[i]] for i, *_ in lignes) / n
moyenne_uniforme = cles["moitié"]
passent_uniforme = sum(1 for i, c, m, q in lignes if (m - c) / c * 100 <= tol)
print()
print(f"**Politique par texte** : budget moyen **{moyenne_politique:.0f} clés**, "
      f"tous les textes à ≤ +{tol:g} % (par construction).")
print(f"**Politique uniforme** (la moitié partout) : budget moyen **{moyenne_uniforme:.0f} clés**, "
      f"et **{passent_uniforme}/{n}** textes tiennent le +{tol:g} %.")
depasse = [(i, (m - c) / c * 100) for i, c, m, q in lignes if (m - c) / c * 100 > tol]
if depasse:
    pire = max(depasse, key=lambda x: x[1])
    print(f"  · les {len(depasse)} textes qui ne tiennent pas montent jusqu'à "
          f"**+{pire[1]:.2f} %** (m{pire[0]}).")
# LA COMPARAISON HONNÊTE SE FAIT À TOLÉRANCE ÉGALE : la référence n'est pas « la moitié partout »
# (elle ne tient pas la tolérance), c'est « tout au complet » — même qualité, budget maximal.
gain = (limite - moyenne_politique) / limite * 100
perte_uniforme = (moyenne_uniforme - limite) / limite * 100
print(f"  · **à tolérance égale** (tout au complet = {limite} clés, même qualité), la politique "
      f"par texte tient partout pour **{gain:.1f} % de clés en moins**.")
print(f"  · l'uniforme « la moitié partout » économise davantage "
      f"({abs(perte_uniforme):.1f} % de clés) mais **casse la tolérance sur "
      f"{n - passent_uniforme}/{n} textes** — il ne compare pas la même chose.")
PY
exit 0
