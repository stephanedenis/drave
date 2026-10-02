#!/bin/bash
# Les portes du dépôt, en une commande.
#
# Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien :
# chaque porte est comparée à la valeur ATTENDUE, et le script sort en erreur si
# l'une diverge. Les valeurs sont celles publiées dans les rapports.
#
#   tools/portes.sh            toutes les portes
#   tools/portes.sh rapide     sans gpt-oss (le seul qui prenne ~20 min)

set -u
cd "$(dirname "$0")/.."
D=./drave-core/target/release/drave
RAPIDE=${1:-}
ECHEC=0

[ -x "$D" ] || { echo "compiler d'abord : (cd drave-core && cargo build --release)"; exit 2; }

compare() {  # nom, attendu, obtenu
    if [ "$2" = "$3" ]; then
        printf "  %-42s %s  ✅\n" "$1" "$3"
    else
        printf "  %-42s %s  ❌ (attendu %s)\n" "$1" "${3:-—}" "$2"
        ECHEC=1
    fi
}

# Attention : le moteur affiche AUSSI une perplexité cumulée par fenêtre, avant
# le total. Prendre la première occurrence du motif donnait 17,431 (fenêtre 1) au
# lieu de 19,3885 (total) — un instrument faux qui accuse le code.
valeur() { grep -oE "=== perplexité [0-9]+\.[0-9]+" | grep -oE "[0-9]+\.[0-9]+" | head -1; }

echo "=== Portes ==="

# 1. Tests unitaires. Le seuil (48) protège le NOMBRE ; il ne dit rien d'un
#    test qui échoue au milieu — un `51 passed; 1 failed` passait la porte. Le
#    compte de tests en échec est donc vérifié séparément : une porte qui cache
#    un échec est une porte cassée (constaté le 02/10).
sortie=$( (cd drave-core && cargo test --release 2>&1) )
n=$(printf '%s' "$sortie" | grep -oE "[0-9]+ passed" | head -1 | cut -d' ' -f1)
ko=$(printf '%s' "$sortie" | grep -cE "^test result: FAILED|^error: test failed")
if [ "${n:-0}" -ge 48 ] && [ "${ko:-1}" -eq 0 ]; then
    printf "  %-42s %s  ✅\n" "cargo test --release" "${n} verts"
else
    printf "  %-42s %s  ❌ (échecs : %s)\n" "cargo test --release" "${n:-0} verts" "${ko:-?}"
    printf '%s' "$sortie" | grep -E "^test .* FAILED" | head -5
    ECHEC=1
fi

# 2. Perplexité Qwen2.5-0.5B, contexte 256.
v=$(timeout 600 $D models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt --ctx 256 \
    --abits 16 --threads 16 --limit 512 --dense 2>&1 | valeur)
compare "Qwen2.5-0.5B ctx 256" "19.3885" "$v"

# 3. Modèle en clusters, mêmes jetons que l'original.
A=/home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters-v2
if [ -d "$A" ]; then
    v=$(timeout 900 $D "$A" --ppl /tmp/ids_qwen.txt --ctx 64 --limit 8 --dense \
        --threads 8 --lot 1 2>&1 | valeur)
    compare "Qwen3-30B en clusters (origine : 799,8557)" "799.8557" "$v"
fi

# 4. Le plan matériel doit détecter les cœurs physiques, pas les threads.
v=$($D models/Qwen2.5-0.5B-Q8_0.gguf --materiel 2>/dev/null | grep -oE "^  threads +: [0-9]+" | grep -oE "[0-9]+")
att=$(nproc); att=$((att / 2))
[ "${v:-0}" -gt 0 ] && [ "${v:-0}" -le "$att" ] \
    && printf "  %-42s %s  ✅\n" "threads par défaut (physiques)" "$v" \
    || { printf "  %-42s %s  ❌\n" "threads par défaut" "${v:-—}"; ECHEC=1; }

# 5. Portes de FORMATS : chaque déquantificateur contre libggml.
if [ "$RAPIDE" = "rapide" ]; then
    echo "  (portes de formats : ignorées en mode rapide)"
else
    if command -v gcc >/dev/null && [ -f tools/portes_formats.sh ]; then
        r=$(timeout 1800 bash tools/portes_formats.sh 2>&1 | tail -1)
        case "$r" in
            *"0 divergence(s), 0 absent(s)"*)
                printf "  %-42s %s  ✅\n" "formats contre libggml" "${r#formats : }" ;;
            *)  printf "  %-42s %s  ❌\n" "formats contre libggml" "$r"; ECHEC=1 ;;
        esac
    fi
fi

# 6. Convention de routage annoncée : elle doit correspondre à ce que le GGUF
#    déclare. C'est la porte qui manquait quand quatre modèles sur cinq étaient
#    routés avec la convention d'un cinquième.
route() {  # nom, modele, motif attendu
    [ -f "$2" ] || { printf "  %-42s %s\n" "$1" "absent"; return; }
    v=$($D "$2" --config 2>/dev/null | grep -oE "routage +: .*" | head -1)
    case "$v" in
        *"$3"*) printf "  %-42s %s  ✅\n" "$1" "$3" ;;
        *)      printf "  %-42s %s  ❌ (attendu %s)\n" "$1" "${v:-—}" "$3"; ECHEC=1 ;;
    esac
}
M=/home/stephane/Data13TB/stephane/modeles/gguf
route "GLM-5.3 : sigmoïde ×2,5" "$M/GLM-5.3-UD-IQ1_S/GLM-5.3-UD-IQ1_S-00001-of-00006.gguf" "sigmoïde"
route "Kimi-K2.7 : sigmoïde ×2,827" "$M/Kimi-K2.7-Code-UD-IQ1_M/Kimi-K2.7-Code-UD-IQ1_M-00001-of-00008.gguf" "sigmoïde"
route "V4-Flash : racine de softplus" "$M/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf" "racine de softplus"
route "Qwen3-235B : softmax" "$M/Qwen3-235B-A22B-Q2_K/Qwen3-235B-A22B-Instruct-2507-Q2_K-00001-of-00002.gguf" "softmax"

# 6bis. V4-Flash : le modèle de la famille V4 tourne EN ENTIER (43 couches, les
#       trois régimes d'attention : brute, HCA, CSA + indexeur). Sa perplexité
#       est un chiffre de référence : si elle dérive, c'est que le calcul a
#       changé. Les identifiants viennent de SON tokenizer, jamais d'un autre.
V4=/home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf
if [ -f "$V4" ]; then
    v=$($D "$V4" --config 2>/dev/null | grep -oE "calculable +: .*")
    case "$v" in
        *": oui"*) printf "  %-42s %s  ✅\n" "V4-Flash : --config le dit calculable" "oui" ;;
        *)         printf "  %-42s %s  ❌\n" "V4-Flash : --config le dit calculable" "${v:-—}"; ECHEC=1 ;;
    esac
    if [ ! -s /tmp/ids_v4flash.txt ]; then
        [ -s /tmp/wt2_txt.txt ] || head -c 20000 data/wikitext2_test.txt > /tmp/wt2_txt.txt
        $D "$V4" --tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_v4flash.txt >/dev/null 2>&1
    fi
    if [ -s /tmp/ids_v4flash.txt ]; then
        p=$(timeout 2400 $D "$V4" --ppl /tmp/ids_v4flash.txt --ctx 32 --limit 5 \
            --dense --threads 16 2>&1 | valeur)
        compare "V4-Flash 43 couches ctx 32" "8430.2968" "$p"
    fi
elif [ "$RAPIDE" != "rapide" ]; then
    printf "  %-42s %s\n" "V4-Flash 43 couches ctx 32" "modèle absent"
fi

# 6ter. Engram : l'adressage des tables de V4.1 doit tomber dans les bornes de
#       chaque colonne. C'est gratuit (métadonnées seules) et c'est la porte qui
#       protège la seule partie de l'engram qui est validée.
V41=/home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf
if [ -f "$V41" ]; then
    r=$($D "$V41" --engram-adresses /tmp/portes_adresses.bin 2>/dev/null)
    case "$r" in
        *"480000 adresses"*)
            printf "  %-42s %s  ✅\n" "engram V4.1 : adressage" \
                "$(printf '%s' "$r" | grep -oE 'rangées DISTINCTES : [0-9]+' | head -1)" ;;
        *)  printf "  %-42s %s  ❌\n" "engram V4.1 : adressage" "pas de sortie"; ECHEC=1 ;;
    esac
fi

# 7. gpt-oss : `--config` d'abord (gratuit), puis la perplexité (~20 min).
#    La porte `--config` existe parce qu'un refus FAUX est un refus trompeur :
#    `attn_sinks` était compté comme un manque V4 alors que les puits appris sont
#    implémentés, et gpt-oss répondait « calculable : NON » (corrigé le 02/10).
if [ "$RAPIDE" != "rapide" ]; then
    O=/home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf
    if [ -f "$O" ]; then
        v=$($D "$O" --config 2>/dev/null | grep -oE "calculable +: .*")
        case "$v" in
            *": oui"*) printf "  %-42s %s  ✅\n" "gpt-oss : --config le dit calculable" "oui" ;;
            *)         printf "  %-42s %s  ❌\n" "gpt-oss : --config le dit calculable" "${v:-—}"; ECHEC=1 ;;
        esac
        # Les identifiants viennent du tokenizer du modèle, jamais d'un autre.
        if [ ! -s /tmp/ids_oss_512.txt ]; then
            [ -s /tmp/wt2_txt.txt ] || head -c 20000 data/wikitext2_test.txt > /tmp/wt2_txt.txt
            $D "$O" --tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_oss_512.txt >/dev/null 2>&1
        fi
        if [ -s /tmp/ids_oss_512.txt ]; then
            p=$(timeout 2400 $D "$O" --ppl /tmp/ids_oss_512.txt --ctx 256 --dense \
                --threads 16 --limit 512 2>&1 | valeur)
            compare "gpt-oss-120b MXFP4 ctx 256" "15.6017" "$p"
        else
            printf "  %-42s %s\n" "gpt-oss-120b MXFP4 ctx 256" "identifiants indisponibles"
        fi
    else
        printf "  %-42s %s\n" "gpt-oss-120b MXFP4 ctx 256" "modèle absent"
    fi
fi

echo ""
[ "$ECHEC" = 0 ] && echo "toutes les portes sont vertes" || echo "AU MOINS UNE PORTE A DIVERGÉ"
exit $ECHEC
