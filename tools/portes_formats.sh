#!/usr/bin/env bash
# Portes des FORMATS : chaque déquantificateur comparé à libggml, bloc par bloc.
#
#   tools/portes_formats.sh [type ...]
#
# Pourquoi : nos déquantificateurs sont écrits d'après le C de ggml, et les cinq
# premiers essais se sont tous trompés (IQ2_XXS : pas de 8 octets sur `qs` ;
# IQ1_M : échelles lues en premier alors qu'elles sont en DERNIER ; Q2_K : indice
# d'échelle ; Q5_K : bits hauts relus au lieu d'avancés ; Q6_K : quants
# entrelacés au lieu de groupés). Aucun n'a été trouvé par relecture : tous l'ont
# été par comparaison à la bibliothèque. Cette porte rend la comparaison
# reproductible, et refuse de « passer » si le témoin a disparu du disque — un
# test qui saute est un test qui ne dit rien.
#
# La référence est liée à libggml (voir tools/ref_ggml_bloc.c).
set -u
cd "$(dirname "$0")/.."
RACINE=$PWD
MODELES=${DRAVE_MODELES:-/home/stephane/Data13TB/stephane/modeles/gguf}
LLAMA=${DRAVE_LLAMA:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}
REF=${REF_GGML_BLOC:-/tmp/ref_ggml_bloc}
VERIF=tools/verifier_formats.py
IFS=$'\n'

ok=0; ko=0; abs=0
# libellé | fichier | tenseur | type ggml
BATTERIE=(
  "F32        | $MODELES/codestral-22b-v0.1-q4_k_m.gguf                             | blk.0.attn_norm.weight              | 0"
  "F16        | $MODELES/bge-m3-FP16.gguf                                            | token_embd.weight                   | 1"
  "Q4_0       | $RACINE/models/Qwen2.5-0.5B-Q4_0.gguf                                | token_embd.weight                   | 2"
  "Q5_0       | $MODELES/qwen2.5-0.5b-instruct-q4_k_m.gguf                           | token_embd.weight                   | 6"
  "Q8_0       | $MODELES/qwen2.5-0.5b-instruct-q4_k_m.gguf                           | output.weight                       | 8"
  "Q2_K       | $MODELES/Qwen3-235B-A22B-Q2_K/Qwen3-235B-A22B-Instruct-2507-Q2_K-00001-of-00002.gguf | token_embd.weight                 | 10"
  "Q3_K       | $MODELES/Qwen3-235B-A22B-Q2_K/Qwen3-235B-A22B-Instruct-2507-Q2_K-00001-of-00002.gguf | blk.0.attn_output.weight            | 11"
  "Q4_K       | $MODELES/codestral-22b-v0.1-q4_k_m.gguf                             | token_embd.weight                   | 12"
  "Q5_K       | $MODELES/Muse-Glimmer-30B-AD-Q4_K_M.gguf                             | blk.0.ffn_down.weight               | 13"
  "Q6_K       | $MODELES/qwen2.5-0.5b-instruct-q4_k_m.gguf                           | blk.0.ffn_down.weight               | 14"
  "IQ2_XXS    | $MODELES/DeepSeek-V4.1-Flash-Q2/DeepSeek-V4.1-Flash-Q2.gguf          | blk.0.ffn_gate_exps.weight          | 16"
  "IQ3_XXS    | $MODELES/Kimi-K2.7-Code-UD-IQ1_M/Kimi-K2.7-Code-UD-IQ1_M-00002-of-00008.gguf | blk.1.ffn_down_exps.weight       | 18"
  "IQ1_S      | $MODELES/GLM-5.3-UD-IQ1_S/GLM-5.3-UD-IQ1_S-00002-of-00006.gguf        | blk.3.ffn_gate_exps.weight          | 19"
  "IQ4_XS     | $MODELES/GLM-5.3-Flash-UD-IQ1_S/GLM-5.3-Flash-UD-IQ1_S-00002-of-00003.gguf | blk.11.ffn_down_exps.weight     | 23"
  "IQ1_M      | $MODELES/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00002-of-00003.gguf | blk.0.ffn_gate_exps.weight | 29"
  "BF16       | $MODELES/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00002-of-00003.gguf | blk.0.ffn_gate_inp.weight  | 30"
  "MXFP4      | $MODELES/gpt-oss-120b-MXFP4.gguf                                     | blk.0.ffn_down_exps.weight          | 39"
)

# Compilation de la référence ggml (une fois par exécution).
if [ ! -x "$REF" ] || [ tools/ref_ggml_bloc.c -nt "$REF" ]; then
  gcc -O2 -I"$LLAMA/ggml/include" -I"$LLAMA/ggml/src" tools/ref_ggml_bloc.c -o "$REF" \
      -L"$LLAMA/build/bin" -lggml -lggml-base -Wl,-rpath,"$LLAMA/build/bin" || exit 2
fi

filtre="${*:-}"
for ligne in "${BATTERIE[@]}"; do
  lib=$(echo "$ligne" | cut -d'|' -f1 | xargs)
  fich=$(echo "$ligne" | cut -d'|' -f2 | xargs)
  tens=$(echo "$ligne" | cut -d'|' -f3 | xargs)
  typ=$(echo "$ligne" | cut -d'|' -f4 | xargs)
  if [ -n "$filtre" ] && ! echo " $filtre " | grep -q " $lib "; then continue; fi
  if [ ! -f "$fich" ]; then
    printf '  %-10s ABSENT   %s\n' "$lib" "$fich"; abs=$((abs+1)); continue
  fi
  # Deux blocs par format : le premier, et un plus loin — un décalage faux se
  # voit au deuxième, pas au premier (les deux valent zéro quand index = 0).
  sortie=$(python3 "$VERIF" "$fich" "$tens" 0 2>&1 | tail -1)
  sortie2=$(python3 "$VERIF" "$fich" "$tens" 7 2>&1 | tail -1)
  if [ "$sortie" = "CONCORDE" ] && [ "$sortie2" = "CONCORDE" ]; then
    printf '  %-10s OK       %s\n' "$lib" "$tens"; ok=$((ok+1))
  else
    printf '  %-10s DIVERGE  %s : %s / %s\n' "$lib" "$tens" "$sortie" "$sortie2"; ko=$((ko+1))
  fi
done
echo "formats : $ok concorde(s), $ko divergence(s), $abs absent(s)"
[ $ko -eq 0 ] && [ $abs -eq 0 ]
