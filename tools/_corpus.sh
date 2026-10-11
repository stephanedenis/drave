#!/bin/bash
# _corpus.sh — le corpus d'identifiants des portes, RÉGÉNÉRÉ s'il manque.
#
# POURQUOI CE FICHIER EXISTE. Seize portes lisent `/tmp/campagne24/ids_0.5B-Q8.txt`, un fichier de
# `/tmp` — donc **effacé par un redémarrage**. La porte refuse alors (code 2) et donne l'impression
# d'une régression, alors que c'est un fichier temporaire qui a disparu.
#
# Or ce corpus est **reproductible au bit près** : `data/wikitext2_test.txt` tokenisé par le
# tokenizer du modèle. Vérifié par `cmp` le 11/10 : identique. On le régénère donc au lieu d'en
# dépendre — et s'il n'est pas régénérable, on le dit et on sort en 2 (convention du dépôt).
#
# MODE D'EMPLOI : après la ligne `IDS=${IDS:-…}`, une porte écrit `. tools/_corpus.sh`.
# Le script suppose que `$D`, `$M` et `$IDS` sont définis, et que le répertoire courant est la
# racine du dépôt (les portes font `cd "$(dirname "$0")/.."` en tête).
if [ ! -s "$IDS" ]; then
    echo "  (corpus $IDS absent — régénéré depuis data/wikitext2_test.txt, bit à bit identique)"
    mkdir -p "$(dirname "$IDS")" 2>/dev/null || true
    "$D" "$M" --tokenize --fichier data/wikitext2_test.txt --sortie "$IDS" >/dev/null 2>&1
fi
[ -s "$IDS" ] || {
    echo "  ❌ corpus $IDS absent ET non régénérable (data/wikitext2_test.txt manquant ?)"
    exit 2
}
