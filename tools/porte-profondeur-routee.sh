#!/bin/bash
# porte-profondeur-routee.sh — dessin H : ce qu'un routeur PARFAIT épargnerait, et ce qu'un
# routeur RÉEL atteint.
#
# CE QUE LA PORTE VERROUILLE, et pourquoi chacun de ces points :
#   1. **la chaîne hors-ligne reproduit le moteur** (deux profondeurs, < 0,2 %) : les chiffres du
#      dessin H sortent d'une relecture d'états en Python, hors du moteur. Si cette relecture est
#      fausse, les chiffres restent plausibles et rien ne le signale. La porte compare donc, sur
#      la MÊME capture, la perplexité hors-ligne et celle que le moteur imprime ;
#   2. **le chemin court est GENUINEMENT plus mauvais** : si l'adaptateur de 16 couches égalait le
#      modèle, il n'y aurait pas de question de routage — et si on lisait l'inverse (un chemin
#      court meilleur), ce serait le signe d'une fuite de données, pas d'un résultat ;
#   3. **la borne de l'oracle est un chiffre, pas un espoir** : la part des jetons où le chemin
#      court rend la MÊME réponse que le chemin long. C'est le maximum qu'un routeur parfait
#      pourrait sortir tôt sans changer une seule décision ;
#   4. **aucun seuil de confiance n'atteint la qualité du chemin long** : c'est le résultat de la
#      porte, et il est NÉGATIF. Le verrouiller empêche de le relire plus tard comme un gain ;
#   5. **mais le seuil SÉLECTIONNE** : à part de jetons égale, le seuil de confiance bat le tirage
#      au hasard. C'est ce qui distingue « le mécanisme ne marche pas » de « le chemin court est
#      trop faible » — deux conclusions opposées pour la suite.
#
# CE QUE LA PORTE NE VERROUILLE PAS, et le dit : le résultat porte sur UN texte et sur UN point de
# sortie (16 couches sur 24). La comparaison est jeton par jeton, en contexte imposé — elle ne dit
# pas ce que deviendrait une séquence libre dont les décisions changeraient en route.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
# LE CORPUS EST TOKENISÉ PAR LA PORTE, avec le tokenizer du modèle. `data/wikitext2_test.txt.ids`
# existe dans le dépôt mais vient d'un AUTRE tokenizer : le modèle complet y rend 7 379 de
# perplexité au lieu de 16,6, et une perplexité absurde rendrait toute la mesure absurde sans que
# rien ne le signale (constaté, puis écarté — `docs/campagne-benefices.md` § « deux corpus »).
TEXTE=${TEXTE:-data/wikitext2_test.txt}
P=${P:-/home/stephane/gpu-env/bin/python}
T=${TRAVAIL:-/tmp/porte-profondeur-routee}
N=${N:-8192}
# Le TEST est pris au DÉBUT et l'entraînement APRÈS : le chemin long ne parcourt alors que la zone
# de test (`--limit TEST_MAX+2`) au lieu des 8 192 jetons, et la porte divise son temps sans rien
# changer à ce qu'elle mesure. Le chemin court, lui, doit couvrir tout le texte (il s'entraîne sur
# la fin) — c'est le seul parcours complet qui reste.
TEST_MIN=${TEST_MIN:-1000}
TEST_MAX=${TEST_MAX:-3000}
EPOQUES=${EPOQUES:-30}
DELAI=${DELAI:-2400}

for f in "$D" "$M" "$TEXTE"; do
    [ -e "$f" ] || { echo "  ❌ $f manquant : cette porte mesure le dessin H sur le corpus du dépôt"; exit 2; }
done
$P -c "import torch" 2>/dev/null || { echo "  ❌ $P n'a pas torch : la relecture d'état en a besoin"; exit 2; }
mkdir -p "$T"

echo "=== 0. le corpus, tokenisé par le modèle ==="
rm -f "$T/corpus.ids"
"$D" "$M" --tokenize --fichier "$TEXTE" --sortie "$T/corpus.ids" 2>&1 | sed 's/^/  /'
IDS="$T/corpus.ids"
[ -s "$IDS" ] || { echo "  ❌ la tokenisation n'a rien écrit"; exit 1; }
JETONS=$(tr ',' '\n' < "$IDS" | wc -l)
[ "$JETONS" -ge "$N" ] || { echo "  ❌ $JETONS jetons pour une mesure à $N : corpus trop court"; exit 1; }

echo "=== 1. la chaîne hors-ligne reproduit-elle le moteur ? (avant toute mesure) ==="
# Deux profondeurs, 127 jetons, et la perplexité que le MOTEUR imprime pendant la capture.
POSC=$(seq -s, 0 126)
for PROF in 16 24; do
    if [ "$PROF" = 16 ]; then COUCHES="0:16"; else COUCHES="0:24"; fi
    timeout "$DELAI" "$D" "$M" --ppl "$IDS" --limit 128 --ctx 128 --threads 8 \
        --couches "$COUCHES" --tete-partielle --etat-sortie "$T/v$PROF" --etat-pos "$POSC" \
        > "$T/v$PROF.log" 2>&1
    PPL=$(grep -oE "perplexité [0-9.]+ sur" "$T/v$PROF.log" | tail -1 | grep -oE "[0-9.]+")
    [ -n "$PPL" ] || { echo "  ❌ aucune perplexité dans $T/v$PROF.log : la capture a échoué"; exit 1; }
    [ -s "$T/v$PROF.126" ] || { echo "  ❌ la capture $PROF couches n'a rien écrit"; exit 1; }
    echo "  — profondeur $PROF (moteur : $PPL)"
    $P tools/verifier_chaine_etat.py --etats "$T/v$PROF" --ids "$IDS" --modele "$M" \
        --ppl-attendue "$PPL" || exit 1
done

echo
echo "=== 2. capturer les deux profondeurs sur $N jetons ==="
# 16 couches : TOUT le texte — l'adaptateur s'entraîne sur la FIN, après la zone de test.
# 24 couches : seulement la zone de TEST, et le parcours est BORNÉ à cette zone (`--limit`) : sans
# cela, le moteur traverse 8 192 jetons pour n'en garder que deux mille.
# LES DEUX CAPTURES TOURNENT ENSEMBLE : en série elles prennent le double, et rien ne les lie.
POS16=$(seq -s, 4 $((N - 1)))
POS24=$(seq -s, "$TEST_MIN" "$TEST_MAX")
mkdir -p "$T/e16" "$T/e24"
T0=$(date +%s)
"$D" "$M" --ppl "$IDS" --limit "$N" --ctx "$N" --threads 8 --couches 0:16 \
    --tete-partielle --etat-sortie "$T/e16/etat" --etat-pos "$POS16" > "$T/e16.log" 2>&1 &
PID16=$!
"$D" "$M" --ppl "$IDS" --limit $((TEST_MAX + 2)) --ctx "$N" --threads 8 --couches 0:24 \
    --etat-sortie "$T/e24/etat" --etat-pos "$POS24" > "$T/e24.log" 2>&1 &
PID24=$!
wait "$PID16"; C16=$?
wait "$PID24"; C24=$?
echo "  parcours terminés en $(( $(date +%s) - T0 )) s (codes $C16 et $C24)"
N16=$(ls -1 "$T"/e16/etat.* 2>/dev/null | grep -cE '\.[0-9]+$')
N24=$(ls -1 "$T"/e24/etat.* 2>/dev/null | grep -cE '\.[0-9]+$')
echo "  états capturés : $N16 en profondeur 16 · $N24 en profondeur 24"
# Un état écrit à moitié (fichier tronqué) ferait échouer la lecture plus loin avec un message
# obscur : on le refuse ici, où l'on sait encore pourquoi.
[ "$C16" = 0 ] && [ "$C24" = 0 ] || { echo "  ❌ un parcours a échoué"; tail -5 "$T/e16.log" "$T/e24.log" | sed 's/^/    /'; exit 1; }
[ "$N16" -ge $((N - 8)) ] || { echo "  ❌ trop peu d'états en profondeur 16 ($N16)"; exit 1; }
[ "$N24" -ge $((TEST_MAX - TEST_MIN - 8)) ] || { echo "  ❌ trop peu d'états en profondeur 24 ($N24)"; exit 1; }

echo
echo "=== 3. la mesure : borne de l'oracle, cascade, témoin ==="
timeout "$DELAI" $P tools/profondeur_routee_oracle.py \
    --etats16 "$T/e16/etat" --etats24 "$T/e24/etat" --ids "$IDS" --modele "$M" \
    --limite "$N" --test-min "$TEST_MIN" --test-max "$TEST_MAX" --train-partie apres \
    --epoques "$EPOQUES" --graine 0 > "$T/oracle.log" 2>&1
CODE=$?
[ "$CODE" = 0 ] || { echo "  ❌ la mesure a échoué (code $CODE) :"; tail -15 "$T/oracle.log" | sed 's/^/    /'; exit 1; }
grep -E "^(test|entraînement)|^\||ACCORD|oracle \(|point de comparaison|confiance moyenne|  ⚠" "$T/oracle.log" | sed 's/^/  /'

echo
echo "=== 4. les verrous ==="
$P - "$T/oracle.log" <<'PY'
import re, sys
t = open(sys.argv[1]).read()
def nombre(motif, defaut=None):
    m = re.search(motif, t)
    return float(m.group(1).replace(",", "")) if m else defaut

just_long = nombre(r"long — 24 couches.*?\| ([\d.,]+) % \|")
just_court = nombre(r"court — 16 couches.*?\| ([\d.,]+) % \|")
accord = nombre(r"ACCORD court/long : ([\d.,]+) %")
oracle = nombre(r"oracle \(le meilleur des deux par jeton\) : ([\d.,]+) %")
ref = nombre(r"tout en long = ([\d.,]+) %")
court_seul = nombre(r"tout en court = ([\d.,]+) %")
conf_ok = nombre(r"d'accord avec le long : ([\d.,]+)")
conf_ko = nombre(r"ne l'est pas : ([\d.,]+)")
manquants = [n for n, v in (("justesse long", just_long), ("justesse court", just_court),
                            ("accord", accord), ("oracle", oracle), ("référence", ref),
                            ("confiance accord", conf_ok), ("confiance désaccord", conf_ko))
             if v is None]
if manquants:
    print(f"  ❌ chiffres illisibles dans la sortie : {', '.join(manquants)}"); sys.exit(1)

echecs = []
# 2. le chemin court est genuinement plus mauvais (et pas l'inverse : ce serait une fuite)
if not just_court < just_long - 10:
    echecs.append(f"le chemin court ({just_court} %) n'est pas nettement plus mauvais que le "
                  f"long ({just_long} %) : soit l'expérience ne mesure rien, soit il y a une fuite")
# 3. la borne de l'oracle est un chiffre
if not 5.0 <= accord <= 95.0:
    echecs.append(f"accord = {accord} % : hors de la plage où la mesure a un sens")
if not oracle > just_long:
    echecs.append(f"l'oracle ({oracle} %) ne bat pas le chemin long seul ({just_long} %) : "
                  f"les deux chemins sont trop proches pour que le routage ait un objet")
# 4. aucun seuil n'atteint la qualité du long : le résultat NÉGATIF
lignes = re.findall(r"^\| ([\d.]+) \| ([\d.]+) % \| ([\d.]+) % \| ([\d.]+) % \| ([\d.]+) % \| "
                    r"([\d.]+) % \|$", t, re.M)
if len(lignes) < 4:
    echecs.append(f"{len(lignes)} ligne(s) de cascade lue(s) : la table est incomplète")
for seuil, part, juste, court_sur, long_sur, temoin in lignes:
    if float(seuil) > 0 and float(juste) >= ref:
        echecs.append(f"seuil {seuil} : {juste} % ≥ {ref} % (chemin long seul) — un seuil "
                      f"atteint donc la qualité de référence, la porte doit être réécrite")
# 4 bis. LE verrou du résultat : sur les jetons que le seuil choisit, le chemin court reste
# derrière le chemin long. C'est ce qui dit que le problème n'est pas le ROUTEUR mais le CHEMIN —
# et qu'un modèle routé devrait d'abord renverser cette colonne-là.
if lignes:
    seuil_max, _, _, court_haute, long_haute, _ = lignes[-1]
    if not float(court_haute) < float(long_haute):
        echecs.append(f"au seuil {seuil_max}, le chemin court ({court_haute} %) atteint le chemin "
                      f"long ({long_haute} %) sur les jetons sortis : la conclusion « le chemin "
                      f"court est le facteur limitant » ne tient plus")
# 5. le seuil sélectionne : il bat le témoin au hasard à part égale
gagnants = [(s, float(j) - float(w)) for s, p, j, cs, ls, w in lignes if float(s) > 0]
if not gagnants or max(d for _, d in gagnants) < 1.0:
    echecs.append("le seuil de confiance ne bat PAS le tirage au hasard : la confiance du chemin "
                  "court ne porte aucune information sur le désaccord")
if not conf_ok > conf_ko + 0.1:
    echecs.append(f"confiance moyenne {conf_ok} (accord) contre {conf_ko} (désaccord) : "
                  f"l'écart est trop faible pour être un signal")

print(f"  chemin long  : {just_long} % · chemin court : {just_court} % · "
      f"témoin tout-court : {court_seul} %")
print(f"  borne de l'oracle (accord) : {accord} % · oracle par jeton : {oracle} %")
print(f"  meilleur gain du seuil sur le hasard : +{max(d for _, d in gagnants):.2f} points")
print(f"  confiance : {conf_ok} quand le court a raison contre le long, {conf_ko} sinon")
if lignes:
    print(f"  au seuil {seuil_max} ({lignes[-1][1]} % des jetons sortis) : chemin court "
          f"{court_haute} % contre chemin long {long_haute} % SUR LES MÊMES JETONS")
if echecs:
    for e in echecs:
        print(f"  ❌ {e}")
    sys.exit(1)
print(f"  ✅ chemin court nettement plus mauvais, borne de l'oracle chiffrée")
print("  ✅ aucun seuil de confiance n'atteint la qualité du chemin long (résultat négatif)")
print("  ✅ le seuil sélectionne quand même : +{:.2f} points sur le hasard à part égale".format(
    max(d for _, d in gagnants)))
PY
CODE=$?
[ "$CODE" = 0 ] || exit "$CODE"

echo
echo "✅ porte profondeur routée : 16 couches contre 24 sur $N jetons de $(basename "$IDS"),"
echo "   chaîne hors-ligne vérifiée contre le moteur, borne de l'oracle mesurée, cascade et témoin."
echo "   Journal complet : $T/oracle.log"
