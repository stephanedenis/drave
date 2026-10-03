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
        # 8430,2968 -> 8430,4966 le 02/10 : la rotation des couches COMPRESSÉES est
        # passée du RoPE simple (régime retardé du moteur) à YaRN ×16 sans mscale,
        # comme llama.cpp (`deepseek4.cpp:872-879`) et vLLM (`rope.py:28-46`) —
        # `reports/rapport-v4-yarn-compresse.md`. Le chiffre bouge à peine parce
        # qu'à ctx 32 les deux régimes coïncident presque (YaRN n'interpole que les
        # basses fréquences) : c'est la comparaison par TENSEUR à la position 127
        # qui a validé le correctif (4,515e-03 contre 5,376e-03 d'écart à
        # llama.cpp), pas cette porte. Une valeur intermédiaire — 8405,9477 — a été
        # mesurée avec une rampe fausse (`original_context_length` est un u32, lu
        # par `as_f64` qui ne lit que les flottants : défaut 4 096 au lieu de
        # 65 536). Toute valeur V4-Flash antérieure au 03/10 est à revérifier.
        p=$(timeout 2400 $D "$V4" --ppl /tmp/ids_v4flash.txt --ctx 32 --limit 5 \
            --dense --threads 16 2>&1 | valeur)
        compare "V4-Flash 43 couches ctx 32" "8430.4966" "$p"
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

# 7ter. Le FLUX doit rester LISIBLE par un outil d'analyse : on produit une trace
#       avec un petit modèle (quelques secondes) et on la relit avec l'outil du
#       dépôt. C'est un CONTRAT DE FORMAT entre deux programmes — et il était
#       rompu : `analyse_flux.py` lisait la version 1 (indice u32 + i16) alors que
#       le moteur écrit la 2 (indices par écarts) depuis des semaines, donc
#       l'outil plantait sur toute trace réelle. Un outil d'analyse qu'on ne peut
#       pas exécuter sur une trace du moteur est un outil mort.
if [ -x tools/analyse_flux.py ]; then
    TRACE_FLUX=/tmp/porte_trace.drvf
    $D models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt --ctx 64 --limit 8 \
        --threads 8 --trace-flux $TRACE_FLUX >/dev/null 2>&1
    if python3 tools/analyse_flux.py $TRACE_FLUX >/tmp/porte_trace.txt 2>&1 \
       && grep -q "couche" /tmp/porte_trace.txt; then
        n=$(grep -c . /tmp/porte_trace.txt)
        printf "  %-42s %s  ✅\n" "le flux relu par tools/analyse_flux.py" "${n} lignes"
    else
        printf "  %-42s %s  ❌\n" "le flux relu par tools/analyse_flux.py" "échec"
        tail -2 /tmp/porte_trace.txt | sed 's/^/      /'
        ECHEC=1
    fi
fi

# 7quater. Le REJEU doit rendre la MÊME perplexité que la passe tracée — et servir
#          TOUTES les listes. Mesuré sur V4-Flash : trace complète = 688 listes,
#          rejeu = 688 servies, 0 manquante ; perplexité 4 221,0901 contre
#          4 221,071, soit 4,5e-06 relatif — l'écart vient de la SECONDE
#          quantification (la trace porte des activations quantifiées, le rejeu les
#          requantifie). Le critère de la porte est donc : aucune liste manquante,
#          et un écart sous 1e-5. Une trace PARTIELLE (--trace-couches) laisse des
#          listes manquantes : c'est annoncé, et c'est ce qui a fait croire à un
#          défaut de rejeu là où la trace était simplement incomplète.
if [ -x tools/analyse_flux.py ]; then
    TR2=/tmp/porte_rejeu.drvf
    p_ref=$($D models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt --ctx 64 --limit 12 \
            --threads 8 --trace-flux $TR2 2>&1 | valeur)
    sortie_rejeu=$($D models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt --ctx 64 --limit 12 \
            --threads 8 --flux-forcer $TR2 2>&1)
    p_rej=$(printf '%s\n' "$sortie_rejeu" | valeur)
    manquantes=$(printf '%s\n' "$sortie_rejeu" | grep -oE "[0-9]+ manquantes" | grep -oE "[0-9]+" | head -1)
    ecart=$(python3 -c "print(f'{abs($p_rej-$p_ref)/max($p_ref,1e-9):.2e}')" 2>/dev/null || echo "?")
    if [ "${manquantes:-1}" = "0" ] && python3 -c "import sys; sys.exit(0 if abs($p_rej-$p_ref)/max($p_ref,1e-9) <= 1e-5 else 1)" 2>/dev/null; then
        printf "  %-42s %s  ✅\n" "le rejeu de la trace (0 manquante, écart ≤ 1e-5)" "écart $ecart"
    else
        printf "  %-42s %s  ❌\n" "le rejeu de la trace (0 manquante, écart ≤ 1e-5)" \
               "écart $ecart · manquantes ${manquantes:-?}"
        ECHEC=1
    fi
fi

# 8. Le DÉCOUPAGE : deux nœuds, cinq modes de flux, un petit modèle (~20 s).
#    Elle manquait, et c'est exactement pour cela que la fuite de la `pre` reçue
#    (sprint 13) a vécu si longtemps : aucun test n'exerçait un COUPLE de nœuds.
#    Les modes exacts (0, 1, 3) doivent rendre 0,00e0 ; les modes à codec
#    quantifié (2, 4) ont une perte assumée, plafonnée à ce qui a été mesuré.
#
#    On lit le CODE RETOUR, pas seulement la présence de « ❌ » : la porte sort en
#    1 sur ses refus précoces (binaire absent, modèle absent, jetons
#    indisponibles) sans imprimer de croix, et un `timeout` rend une sortie
#    partielle — trois façons de dire « vert » sur un échec, relevées par la
#    relecture adverse du bloc 13 (démontré : modèle absent → ECHEC=0).
if [ -x tools/porte-flux.sh ]; then
    printf "\n=== Découpage (deux nœuds) ===\n"
    sortie_flux=$(timeout 900 tools/porte-flux.sh 2>&1)
    code_flux=$?
    printf '%s\n' "$sortie_flux"
    if [ "$code_flux" != "0" ] || printf '%s\n' "$sortie_flux" | grep -q "❌"; then
        printf "  %-42s %s  ❌\n" "porte du découpage (code $code_flux)" "échec"
        ECHEC=1
    fi
fi

echo ""
[ "$ECHEC" = 0 ] && echo "toutes les portes sont vertes" || echo "AU MOINS UNE PORTE A DIVERGÉ"
exit $ECHEC
