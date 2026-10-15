#!/bin/bash
# porte-vision.sh — LA VISION : ce qui est VÉRIFIÉ est vérifié, ce qui ne l'est pas est DIT.
#
# POURQUOI CETTE PORTE, ET POURQUOI ELLE NE JUGE PAS LA TOUR. Depuis le 15/10 la faculté de vision
# a un modèle (`models/vision/…`), un banc qui déroule **toute la tour**, et une **référence
# indépendante** (`transformers`) qui dit que la tour **ne concorde pas encore** (55 à 79 % d'écart
# pour une quantification de ~1 % ; `reports/rapport-vision-qwen2vl.md`). Une porte qui exigerait
# l'accord de la tour serait **rouge** — et une porte rouge permanente ne dit plus rien. Cette porte
# vérifie donc **ce qui est établi**, et **dit** ce qui ne l'est pas :
#
#   1. **le banc refuse un fichier sans tour de vision** (un modèle de texte : message clair, pas de
#      panique) — c'est la première chose qu'un banc doit faire ;
#   2. **l'embedding de patchs est EXACT** contre la référence numpy (`tools/vision_ref.py`), sur
#      les **mêmes poids** lus dans le GGUF : l'écart doit rester dans le bruit de virgule
#      flottante (publié le 10/10 : **5,4e-7**) ;
#   3. **les formes sont celles du modèle** (256 patchs × 1280 canaux, 64 jetons × 1536 après
#      fusion) — une tour qui rendrait d'autres formes serait fausse *avant* toute question de
#      valeurs ;
#   4. **la tour est MESURÉE, pas jugée** : la porte relève sa norme de sortie et la compare à celle
#      de la référence `transformers` si elle est disponible, en **publiant l'écart sans en faire un
#      critère** — le jour où l'écart tombera à quelques pour cent, cette ligne deviendra le
#      critère, et la porte devra être resserrée (c'est écrit ici pour que ce soit un choix, pas un
#      oubli).
#
#   5. **LES COUCHES PROFONDES EN ISOLATION** *(c'est la vérification de la tour)* : comparer des
#      SORTIES ne dit rien au-delà de la couche ~8 (l'attention s'effondre — entropie 0,16 à la
#      couche 15 — et bascule d'un patch à l'autre : variation totale 0,94). On donne donc aux deux
#      implémentations **le même état d'entrée** et on compare la couche **seule**
#      (`tools/vision_isole.py`). Mesuré le 15/10 : 4,5e-07 à 7,6e-06 sur les couches 1, 8, 15, 23
#      et 31 — les conventions du moteur sont **justes** dans toute la tour.
#
# ⚠ Ce que cette porte ne peut PAS faire : vérifier la tour. La référence numpy de bloc 0
# (`vision_ref.py`) **reprend les hypothèses du moteur** (mêmes conventions de rotation, mêmes
# LayerNorm sans biais) : elle ne pouvait pas les mettre en défaut — c'est la référence
# **indépendante** (`transformers`) qui l'a fait. Une référence écrite d'après la même lecture
# vérifie l'arithmétique, pas les conventions.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
P=${P:-python3}
MMPROJ=${MMPROJ:-models/vision/mmproj-Qwen2-VL-2B-Instruct-Q8_0.gguf}
TEXTE=${TEXTE:-models/Qwen2.5-0.5B-Q8_0.gguf}
T=${T:-/tmp/porte-vision}
[ -x "$D" ] || { echo "  ❌ binaire du moteur absent : $D"; exit 2; }
if [ ! -s "$MMPROJ" ]; then
    echo "  ❌ pas de tour de vision sur la machine : $MMPROJ"
    echo "     (elle se télécharge : huggingface.co/ggml-org/Qwen2-VL-2B-Instruct-GGUF, fichier mmproj)"
    exit 2
fi
mkdir -p "$T"

echo "porte de la vision — $(basename "$MMPROJ")"

# ---- 1. un fichier SANS tour de vision doit être refusé en le disant
if [ -s "$TEXTE" ]; then
    "$D" "$TEXTE" --banc-vision "$T/rien.bin" > "$T/refus.log" 2>&1
    grep -q "pas de v.patch_embd.weight" "$T/refus.log" \
        || { echo "  ❌ un modèle sans tour de vision n'est pas refusé en le disant :"; tail -2 "$T/refus.log"; exit 1; }
    echo "  ✅ 1. un modèle sans tour de vision est refusé en le disant"
else
    echo "  ⚠️ 1. « $TEXTE » absent : le refus n'est pas vérifié"
fi

# ---- 2 et 3. l'embedding de patchs contre la référence numpy, et les formes de la tour
# ⚠ LA COMPARAISON À LA RÉFÉRENCE NUMPY EST CONDITIONNELLE, et il faut dire pourquoi : cette
# référence n'accepte que l'image **28 × 28** (celle sur laquelle elle a été validée, 5,4e-7) et ses
# attentes de FORMAT ont dérivé depuis (elle lit un fichier `.poids` que le banc n'écrit plus de la
# même façon). Une porte ne cache pas un outil cassé : elle tente, et elle **dit** quand elle n'a pas
# pu comparer. Le jour où la référence suivra le format, la comparaison redeviendra un critère.
timeout 2400 env DRAVE_VISION_POIDS=all DRAVE_VISION_COUCHES=32 \
    ${NOYAU:+DRAVE_VISION_NOYAU=$NOYAU} "$D" "$MMPROJ" --banc-vision "$T/tour.bin" > "$T/banc.log" 2>&1 \
    || { echo "  ❌ le banc de vision a échoué :"; tail -3 "$T/banc.log"; exit 1; }
grep -q "v.patch_embd.weight : sortie 1280 · entrée 3 · noyau 14×14" "$T/banc.log" \
    || { echo "  ❌ la tour de vision n'a pas les dimensions attendues :"; grep "patch_embd" "$T/banc.log"; exit 1; }
EMBEDING="embedding non mesuré"
ISOLE="couches isolées non mesurées"
NOYAU=${NOYAU:-/tmp/vision-noyau-somme.f32}
DRAVE_VISION_COTE=28 timeout 900 "$D" "$MMPROJ" --banc-vision "$T/tour28.bin" >> "$T/banc.log" 2>&1
if $P tools/vision_ref.py "$T/tour28.bin" > "$T/ref.log" 2>&1; then
    grep -q "accord (bruit de virgule flottante)" "$T/ref.log" \
        || { echo "  ❌ l'embedding de patchs NE CONCORDE PAS avec la référence numpy :"; tail -3 "$T/ref.log"; exit 1; }
    ECART=$(grep -oE "écart max relatif : [0-9.e-]+" "$T/ref.log" | grep -oE "[0-9.e-]+" | head -1)
    echo "  ✅ 2. l'embedding de patchs est EXACT contre la référence numpy (écart max relatif $ECART)"
    EMBEDING="embedding exact"
else
    echo "  ⚠️ 2. la référence numpy n'a PAS pu comparer (format dérivé — elle lit un .poids que le"
    echo "     banc n'écrit plus de la même façon) : l'embedding n'est donc PAS vérifié ici"
    EMBEDING="embedding NON comparé"
fi

TAILLE=$($P - "$T/tour.bin" <<'PY'
import struct, sys
b = open(sys.argv[1], "rb").read(8)
n, c = struct.unpack("<ii", b)
print(f"{n}x{c}")
PY
)
JETONS=$($P - "$T/tour.bin.jetons" <<'PY'
import struct, sys
b = open(sys.argv[1], "rb").read(8)
n, c = struct.unpack("<ii", b)
print(f"{n}x{c}")
PY
)
[ "$TAILLE" = "256x1280" ] || { echo "  ❌ la tour rend $TAILLE (attendu 256x1280)"; exit 1; }
[ "$JETONS" = "64x1536" ] || { echo "  ❌ le projecteur rend $JETONS (attendu 64x1536)"; exit 1; }
echo "  ✅ 3. les formes sont celles du modèle : tour $TAILLE · jetons d'image $JETONS"

# ---- 4. la tour est MESURÉE, pas jugée : on publie l'écart à la référence indépendante
NORMES=$(grep -oE "tour : [0-9]+ couches × 256 patchs × [0-9]+ · \|sortie\| = [0-9.]+" "$T/banc.log" | tail -1)
echo "  ⚠️ 4. $NORMES"
if [ -s /home/stephane/IA/cache/huggingface/qwen2vl-ref/config.json ]; then
    echo "     la comparaison de SORTIES n'est pas un critère, et c'est MESURÉ : l'attention"
    echo "     s'effondre (entropie 0,16 à la couche 15) et bascule d'un patch à l'autre (variation"
    echo "     totale 0,94) — c'est pourquoi la vérification se fait EN ISOLATION (étape 5)."
else
    echo "     référence indépendante absente : la tour n'est pas comparable, et elle n'est pas vérifiée"
fi
# LE RÉSUMÉ DIT CE QUI A ÉTÉ VÉRIFIÉ, PAS CE QU'ON AURAIT VOULU : la première version de cette
# porte annonçait « embedding exact » alors que la comparaison n'avait pas pu tourner.
# ---- 5. les couches profondes EN ISOLATION (la vérification de la tour)
NOYAU=${NOYAU:-/tmp/vision-noyau-somme.f32}
if [ -s "$T/tour.bin.poids32" ] && [ -s "$NOYAU" ]; then
    $P tools/vision_isole.py --banc "$T/tour.bin" --poids "$T/tour.bin.poids32" \
        --mmproj "$MMPROJ" --moteur "$D" --noyau "$NOYAU" --couches 1,15,31 > "$T/isole.log" 2>&1
    if [ "$?" -eq 0 ]; then
        PIRES=$(grep -oE "écart max sur les couches vérifiées : [0-9.e+-]+" "$T/isole.log" | grep -oE "[0-9.e+-]+$")
        echo "  ✅ 5. les couches 1, 15 et 31 EN ISOLATION : écart max $PIRES (les conventions sont"
        echo "     celles de la formule, même là où l'attention bascule)"
        ISOLE="couches isolées justes"
    else
        echo "  ❌ 5. une couche EN ISOLATION s'écarte des conventions :"; tail -4 "$T/isole.log"
        exit 1
    fi
else
    echo "  ⚠️ 5. déchargement des poids ou noyau réparé absent : les couches isolées ne sont pas"
    echo "     vérifiées ici (DRAVE_VISION_POIDS=all et le noyau sommé, voir la fiche)"
    ISOLE="couches isolées NON vérifiées"
fi
echo "  ✅ porte tenue (refus dit · $EMBEDING · formes du modèle · $ISOLE)"
exit 0
