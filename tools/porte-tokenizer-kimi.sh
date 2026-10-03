#!/bin/bash
# Compare nos identifiants à ceux du tokenizer OFFICIEL de Kimi-K3 (pur Python).
# Le tokenizer vit dans le shard 1 : la porte marche MÊME pendant le téléchargement.
K=${K3:-/home/stephane/Data13TB/stephane/modeles/gguf/Kimi-K3-UD-Q4_K_XL/Kimi-K3-UD-Q4_K_XL-00001-of-00032.gguf}
D=./drave-core/target/release/drave
ok=0; ko=0
while IFS= read -r -d $'\x1e' texte; do
    printf '%s' "$texte" > /tmp/tk_txt
    officiel=$(/usr/bin/python3.14 tools/tokenizer_kimi/reference_officielle.py < /tmp/tk_txt 2>/dev/null)
    $D "$K" --tokenize --fichier /tmp/tk_txt --sortie /tmp/tk_ids.txt >/dev/null 2>&1
    notre=$(cat /tmp/tk_ids.txt 2>/dev/null)
    if [ "$officiel" = "$notre" ]; then ok=$((ok+1)); else ko=$((ko+1)); echo "  DIVERGENCE sur : $(printf '%s' "$texte" | head -c 60)"; echo "    officiel : $(printf '%s' "$officiel" | head -c 100)"; echo "    nous     : $(printf '%s' "$notre" | head -c 100)"; fi
done
echo "identiques : $ok · divergents : $ko"
