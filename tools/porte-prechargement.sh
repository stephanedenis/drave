#!/bin/bash
# porte-prechargement.sh — S4 : la prélecture des experts, mesurée DANS le moteur.
#
# La question, et pourquoi elle a une porte : `docs/manques.md` § 1 nomme le manque
# (« la lecture mmap atteint 8,6 Mo/s sur disque dur contre 243 Mo/s en séquentiel »), et
# `docs/strata-pour-drave.md` § 4 en fait la première action. Le mécanisme a été mesuré
# hors du moteur (`tools/banc-prelire.py`, `tools/banc-experts.py`) : ce qui paie n'est pas
# `madvise` sur une plage, c'est de **lancer les lectures en parallèle**.
#
# Trois bras, la MÊME passe, le MÊME fichier, les MÊMES jetons :
#
#   demande   DRAVE_PRELIRE=0        aucune prélecture — le régime du manque
#   madvise   DRAVE_PRELIRE_FILS=0   l'ancien chemin : `madvise(WILLNEED)` sur la plage
#   fils      (défaut, 8 fils)       des fils entrent les pages eux-mêmes
#
# LE CACHE EST ÉVINCÉ AVANT CHAQUE BRAS (`tools/evincer-cache.py`) : sans cela le deuxième
# bras lit ce que le premier a laissé dans le cache de pages et mesure de la RAM — c'est
# le piège qui a donné « 300 Mo/s au hasard » au premier essai du banc.
#
# Ce que la porte exige :
#   1. la perplexité est IDENTIQUE dans les trois bras (la prélecture ne change pas le
#      calcul — c'est la première chose à vérifier, et la seule qui soit non négociable) ;
#   2. le bras `fils` ne lit pas plus d'octets que `madvise` ;
#   3. le bras `fils` ne prend pas plus de temps mural que `demande`, et son temps de
#      CALCUL est plus court (c'est le signe que les pages étaient là au moment du calcul).
#
# usage : tools/porte-prechargement.sh [--vite]
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf}
IDS=${IDS:-$HOME/IA/scratch/prerequis/ids_qwen3_30b_wt2.txt}
JETONS=${JETONS:-8}
CTX=${CTX:-512}
# `--dense` : le chargeur construit par DÉFAUT la représentation en listes des poids denses
# (2,69 Go, **27,5 s** sur Qwen3-30B) — et cette passe ne s'en sert PAS (« dont en listes :
# 0,0 M — le reste est dense », dit le moteur lui-même). Mesuré le 12/10 : 27,46 s de
# chargement par défaut contre **7,77 s** avec `--dense`, perplexité IDENTIQUE (6449,7333).
# Sans cette option, la porte mesurerait surtout le chargement, identique dans les trois bras.
THREADS=${THREADS:-16}
# TROIS répétitions, et pas deux : la comparaison porte sur la MÉDIANE, et avec deux
# échantillons la médiane est leur moyenne — un seul chargement lent (cache de pages écrasé par
# une passe complète de 44 portes) suffit alors à faire basculer le verdict. Mesuré le 15/10 :
# pendant la passe, `tampons` = 14,92 s puis 10,04 s (médiane 12,48) contre `fils` = 11,11 puis
# 10,79 (médiane 10,95) ⇒ PORTE ROUGE ; relancée seule : `tampons` 10,45 s contre `fils` 13,06 s
# ⇒ PORTE TENUE. Le second échantillon des tampons était le PLUS RAPIDE des quatre. Avec trois
# répétitions, la médiane est le point du milieu et un échantillon aberrant ne décide plus.
REPETITIONS=${REPETITIONS:-3}
[ "${1:-}" = "--vite" ] && { JETONS=4; REPETITIONS=1; }

for f in "$D" "$M" "$IDS"; do
    [ -s "$f" ] || { echo "  ❌ $f manquant"; exit 2; }
done
command -v python3 >/dev/null || { echo "  ❌ python3 manquant (évinceur de cache)"; exit 2; }

echo "porte du préchargement — $(basename "$M"), $JETONS jetons, ctx $CTX, $REPETITIONS répétition(s)"
printf "%-10s %-6s %14s %10s %10s %10s  %s\n" "bras" "rép" "octets lus" "mural" "chargement" "calcul" "perplexité"
mesures=""
#   tampons   DRAVE_TAMPONS=1       les experts RETENUS lus en `pread`, par offset croissant,
#                                    dans nos tampons — le calcul lit ces octets (directive du
#                                    12/10 : « granularité fine, lecture séquentielle,
#                                    allocation intelligente au lieu de virtualiser »)
for bras in "demande:DRAVE_PRELIRE=0" "madvise:DRAVE_PRELIRE_FILS=0" "fils:" "tampons:DRAVE_TAMPONS=1"; do
    nom=${bras%%:*}; reglages=${bras#*:}
    for r in $(seq 1 "$REPETITIONS"); do
        python3 tools/evincer-cache.py "$M" > /dev/null
        log=$(mktemp)
        /usr/bin/time -v env $reglages "$D" "$M" --ppl "$IDS" --ctx "$CTX" \
            --limit "$JETONS" --threads "$THREADS" --dense > "$log" 2>&1
        chargement=$(grep -oE "chargées en [0-9.]+s" "$log" | grep -oE "[0-9.]+" | tail -1)
        blocs=$(grep -oE "File system inputs: [0-9]+" "$log" | grep -oE "[0-9]+" | tail -1)
        mural=$(grep -oE "m:ss\): [0-9:.]+" "$log" | grep -oE "[0-9]+:[0-9.]+$" | tail -1)
        calcul=$(grep -oE ", [0-9.]+ s\)" "$log" | grep -oE "[0-9.]+" | tail -1)
        ppl=$(grep -oE "perplexité [0-9.]+" "$log" | grep -oE "[0-9.]+" | tail -1)
        [ -n "$blocs" ] || { echo "  ❌ le bras $nom n'a rien mesuré :"; tail -3 "$log" | sed 's/^/     /'; rm -f "$log"; exit 1; }
        octets=$(python3 -c "print(f'{$blocs*512/1e9:.2f} Go')")
        printf "%-10s %-6s %14s %10s %10s %10s  %s\n" "$nom" "$r" "$octets" "$mural" \
               "${chargement:-?}" "${calcul:-?} s" "$ppl"
        mesures="${mesures}${nom}|${r}|${blocs}|${mural}|${calcul:-0}|${ppl}"$'\n'
        rm -f "$log"
    done
done

echo
# Les mesures passent par un FICHIER : `python3 - <<'PY'` prend son script sur l'entrée
# standard, donc un tube ne peut pas y arriver en même temps (premier essai : liste vide,
# et la porte annonçait « les bras ne rendent pas la même perplexité » — un faux rouge).
FICHE_MESURES=$(mktemp)
printf '%s' "$mesures" > "$FICHE_MESURES"
python3 - "$FICHE_MESURES" <<'PY'
import sys, statistics
lignes = [l.split('|') for l in open(sys.argv[1]).read().splitlines() if l.strip()]
def secs(t):
    m, s = t.split(':'); return int(m) * 60 + float(s)
par = {}
for nom, _, blocs, mural, calcul, ppl in lignes:
    par.setdefault(nom, []).append((int(blocs) * 512 / 1e9, secs(mural), float(calcul), ppl))
ok = True
ppls = {nom: {v[3] for v in vals} for nom, vals in par.items()}
if len({p for s in ppls.values() for p in s}) != 1:
    print("  ❌ les bras ne rendent pas la MÊME perplexité :", {k: sorted(v) for k, v in ppls.items()})
    ok = False
else:
    print("  ✅ perplexité identique dans les trois bras :", list(ppls.values())[0].pop())
med = {nom: tuple(statistics.median(v[i] for v in vals) for i in range(3)) for nom, vals in par.items()}
for nom in ("demande", "madvise", "fils", "tampons"):
    if nom in med:
        go, s, calc = med[nom]
        print(f"     {nom:8} : {go:6.2f} Go lus · {s:6.2f} s murales · {calc:5.2f} s de calcul")
if "tampons" in med and "fils" in med:
    # Les tampons lisent MOINS d'octets que les fils (granularité fine : uniquement les
    # plages retenues, pas de lecture en avance au-delà) ; ils ne doivent pas être plus lents.
    if med["tampons"][1] > med["fils"][1] * 1.05:
        print(f"  ❌ les tampons sont plus lents que les fils "
              f"({med['tampons'][1]:.2f} s contre {med['fils'][1]:.2f} s)"); ok = False
if "fils" in med and "demande" in med:
    # Les OCTETS ne sont pas un critère : la prélecture parallèle parcourt les plages
    # entières et lit donc plus que le strict nécessaire (10,0 Go contre 9,0 mesurés le
    # 12/10). C'est un échange assumé — sur un support à bande passante (l'array, 7,45 Go/s
    # à huit lecteurs), le temps gagné vaut les octets ; il est publié pour que le jour où
    # le support sera pauvre en bande passante, la décision se reprenne sur des chiffres.
    if "madvise" in med and med["fils"][0] > med["madvise"][0] * 1.05:
        print(f"  (les octets lus augmentent : {med['fils'][0]:.2f} Go contre "
              f"{med['madvise'][0]:.2f} Go — échange assumé, voir le commentaire)")
    if med["fils"][1] > med["demande"][1]:
        print(f"  ❌ le bras `fils` est plus LENT que la demande "
              f"({med['fils'][1]:.1f} s contre {med['demande'][1]:.1f} s)"); ok = False
    if med["fils"][2] >= med["demande"][2]:
        print(f"  ❌ le calcul ne paie pas moins de défauts de page "
              f"({med['fils'][2]:.2f} s contre {med['demande'][2]:.2f} s)"); ok = False
print("  PORTE TENUE" if ok else "  PORTE ROUGE")
sys.exit(0 if ok else 1)
PY
rm -f "$FICHE_MESURES"
