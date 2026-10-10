#!/bin/bash
# porte-tokenizer-kimi.sh — nos identifiants contre ceux du tokenizer OFFICIEL de Kimi-K3.
#
# ELLE ÉTAIT VERTE EN NE COMPARANT RIEN. Elle lisait une liste de textes sur **stdin**, que
# personne ne lui fournissait : la boucle lisait EOF immédiatement, imprimait
# « identiques : 0 · divergents : 0 » et sortait en **0**. C'est la famille de défauts que ce
# dépôt traque — une vérification qui ne peut pas échouer — trouvée en regardant le TEMPS de la
# passe complète : 0 seconde pour une porte censée charger un modèle et un tokenizer.
#
# Corrigé : les textes sont DANS la porte (jeu couvrant ce qui casse un tokenizer : accents,
# emoji, CJK, arabe, code, nombres, espaces), la porte REFUSE de verdir si le nombre de
# comparaisons est nul, et un manque de prérequis est ROUGE (code 2), pas vert.
#
# Le tokenizer vit dans le shard 1 : la porte marche MÊME pendant le téléchargement du modèle.
K=${K3:-/home/stephane/Data13TB/stephane/modeles/gguf/Kimi-K3-UD-Q4_K_XL/Kimi-K3-UD-Q4_K_XL-00001-of-00032.gguf}
D=./drave-core/target/release/drave
REF=tools/tokenizer_kimi/reference_officielle.py
PY=${PY:-/usr/bin/python3.14}
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT

[ -s "$K" ] || { echo "  ❌ shard de tokenizer absent : $K"; exit 2; }
[ -s "$REF" ] || { echo "  ❌ tokenizer de référence absent : $REF"; exit 2; }
[ -x "$PY" ] || { echo "  ❌ $PY (l'interpréteur de la référence) est absent"; exit 2; }
[ -x "$D" ] || { echo "  ❌ binaire du moteur absent : $D"; exit 2; }

# Le jeu de textes :  comme séparateur (même convention que la lecture ci-dessous).
if [ -n "${TEXTES:-}" ] && [ -s "${TEXTES}" ]; then
    cp "$TEXTES" "$T/textes.bin"
else
    printf '%s\x1e' \
      "Bonjour le monde" \
      "Où sont les accents ? É à ç ü ß" \
      "emoji : 🚀🧠🔥" \
      "日本語のテキスト、これはテストです" \
      "العربية نص تجريبي" \
      "code : fn main() { let x = 1; } // commentaire" \
      "1 234,56 € et 42 % et 3.14159" \
      "   espaces   et\ttabulations\t" \
      "URL : https://exemple.org/a?b=c&d=e#f" \
      "Ligne1\nLigne2" > "$T/textes.bin"
fi

ok=0; ko=0
while IFS= read -r -d $'\x1e' texte; do
    [ -n "$texte" ] || continue
    printf '%s' "$texte" > "$T/txt"
    officiel=$("$PY" "$REF" < "$T/txt" 2>/dev/null)
    $D "$K" --tokenize --fichier "$T/txt" --sortie "$T/ids.txt" >/dev/null 2>&1
    notre=$(cat "$T/ids.txt" 2>/dev/null)
    if [ "$officiel" = "$notre" ]; then ok=$((ok+1)); else
        ko=$((ko+1))
        echo "  DIVERGENCE sur : $(printf '%s' "$texte" | head -c 60)"
        echo "    officiel : $(printf '%s' "$officiel" | head -c 100)"
        echo "    nous     : $(printf '%s' "$notre" | head -c 100)"
    fi
done < "$T/textes.bin"
echo "identiques : $ok · divergents : $ko"
# LE GARDE-FOU QUI MANQUAIT : zéro comparaison n'est pas une réussite.
[ $((ok + ko)) -gt 0 ] || { echo "  ❌ AUCUNE comparaison n'a eu lieu (porte non exécutée)"; exit 1; }
[ "$ko" = 0 ] || { echo "  ❌ $ko divergence(s) avec le tokenizer officiel"; exit 1; }
echo "  ✅ $ok textes identiques au tokenizer officiel (accents, emoji, CJK, arabe, code, nombres)"
