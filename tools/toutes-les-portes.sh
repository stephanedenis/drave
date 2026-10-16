#!/bin/bash
# toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait.
#
# POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS
# (`--attn-window` en réparti) que le v7 avait **délibérément retiré** en faisant voyager les
# trois réglages dans la trame (`main.rs:4432`). La porte ne pouvait donc plus passer — et
# personne ne l'a vu, parce que les portes étaient lancées **une par une**, à la main, quand
# on touchait la fonctionnalité du jour. Une porte qu'on croit verte et qui n'a pas tourné est
# exactement le défaut que ce dépôt traque (un drapeau inerte, une mesure qui ne mesure rien) :
# ici, appliqué aux instruments eux-mêmes.
#
# Ce que fait ce script, et ce qu'aucun autre ne faisait :
#   1. il lance **TOUTES** les `tools/porte-*.sh`, séquentiellement ;
#   2. il ne s'arrête PAS à la première rouge — il veut le tableau, pas la première tuile ;
#   3. il borne chaque porte dans le temps (`DELAI`, 1800 s par défaut) : une porte qui pend
#      est une porte ROUGE, pas une porte qu'on attend ;
#   4. il garde le journal de chacune (`JOURNAUX`) et n'affiche qu'une ligne par porte ;
#   5. il sort en 1 s'il y a la moindre rouge, en imprimant de quoi la relire.
#
# Usage :
#   tools/toutes-les-portes.sh                 # les 22 portes
#   PORTES="gain topologie" tools/toutes-les-portes.sh    # un sous-ensemble (filtre)
#   DELAI=300 tools/toutes-les-portes.sh       # borne plus serrée
#
# NOTE DE MESURE : les portes de latence et de gigue (`porte-delais`, `porte-flux`) mesurent
# des temps. Les lancer **seules** si un chiffre de temps doit être interprété ; ce script les
# enchaîne, donc il est fait pour le VERDICT (vert/rouge), pas pour le chronomètre.
set -u
cd "$(dirname "$0")/.."
DELAI=${DELAI:-1800}
FILTRE=${PORTES:-}
JOURNAUX=${JOURNAUX:-/tmp/portes-$(date +%m%d-%Hh%M)}
mkdir -p "$JOURNAUX"

portes=$(ls tools/porte-*.sh | sort)
if [ -n "$FILTRE" ]; then
    gardees=""
    for f in $FILTRE; do
        for g in $portes; do
            case "$(basename "$g")" in *"$f"*) gardees="$gardees $g";; esac
        done
    done
    portes=$(printf '%s\n' $gardees | sort -u)
fi

vertes=0; rouges=0; liste_rouges=""
echo "=== PASSE COMPLÈTE DES PORTES ($(printf '%s\n' $portes | grep -c . ) portes, borne ${DELAI} s) ==="
echo "    journaux : $JOURNAUX"
for g in $portes; do
    nom=$(basename "$g" .sh)
    j="$JOURNAUX/$nom.log"
    t0=$(date +%s)
    timeout "$DELAI" bash "$g" > "$j" 2>&1
    code=$?
    dt=$(( $(date +%s) - t0 ))
    # la dernière ligne ✅ dit CE QUE la porte a verrouillé ; sinon la dernière ❌, sinon la queue
    dernier=$(grep -E "✅|❌|ÉCHEC|TENUE" "$j" | tail -1 | cut -c1-96)
    if [ "$code" = 0 ]; then
        vertes=$((vertes+1)); marque="✅"
    else
        rouges=$((rouges+1)); liste_rouges="$liste_rouges $nom"
        [ "$code" = 124 ] && marque="⏱ (borne ${DELAI} s dépassée)" || marque="❌ code $code"
    fi
    printf '  %-22s %-26s %4d s  %s\n' "$nom" "$marque" "$dt" "$dernier"
    # ⚠️ LE REGISTRE, ET POURQUOI IL EXISTE. La synthèse ci-dessous part sur la SORTIE STANDARD ✗ — et
    # une passe lancée avec `| tail` (ou dont on ne garde que la fin ✓) la perd ✗✓ : il ne reste alors
    # que les journaux par porte, où le verdict ne se lit qu'au MARQUEUR (❌ ✓) — or l'audit du 16/10 a
    # montré que le marqueur n'est PAS le critère ✓ (une porte peut échouer sans ❌ dans son source ✓,
    # et le marqueur peut venir de l'outil qu'elle appelle ✓). Écrire le CODE DE SORTIE dans le dossier
    # des journaux rend le verdict **relisible** ✓, quelle que soit la façon dont la passe a été lancée ✓.
    printf '%s %s %s\n' "$nom" "$code" "$dt" >> "$JOURNAUX/registre.txt"
done

echo "--- $vertes vertes, $rouges rouges ---" | tee -a "$JOURNAUX/registre.txt"
if [ "$rouges" != 0 ]; then
    echo "À RELIRE (les six dernières lignes de chaque rouge) :"
    for nom in $liste_rouges; do
        echo "  --- $nom ---"
        tail -6 "$JOURNAUX/$nom.log" | sed 's/^/    /'
    done
    echo "Journaux complets : $JOURNAUX"
    exit 1
fi
echo "TOUTES LES PORTES SONT VERTES — et elles ont TOUTES tourné, ce que rien ne garantissait avant."
echo "Journaux : $JOURNAUX"
