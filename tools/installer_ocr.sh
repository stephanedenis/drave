#!/bin/bash
# installer_ocr.sh — l'OCR de R4.4, installé SANS root dans `work/ocr/` (gitignoré).
#
# POURQUOI CE SCRIPT. La ligne R4.4 était bloquée par « aucun OCR installé » : ni tesseract,
# ni pytesseract, et un paquet système demanderait root. On télécharge donc les RPM openSUSE,
# on les extrait sous `work/ocr/root`, et on ne touche à rien d'autre. Le résultat est
# reproductible : `--verifie` dit la version installée, relancer le script ne retélécharge
# que ce qui manque.
#
# CE QU'IL NE FAIT PAS. Aucun `sudo`, aucune écriture hors de `work/ocr/`, aucun modèle
# neuronal : tesseract 5.5.3 et les données fra/eng/spa/osd. Un OCR neuronal (rapidocr,
# easyocr) serait un autre choix, avec un autre coût — il n'est pas fait ici.
#
# Usage :
#   tools/installer_ocr.sh              # installe (ou complète) et affiche la version
#   tools/installer_ocr.sh --verifie    # ne télécharge rien : dit ce qui est là, code 1 si absent
set -euo pipefail
cd "$(dirname "$0")/.."

PREFIXE=${TESSERACT_PREFIX:-$PWD/work/ocr/root}
DEPOT=${DEPOT:-https://download.opensuse.org/tumbleweed/repo/oss}
BIN="$PREFIXE/usr/bin/tesseract"
DATA="$PREFIXE/usr/share/tessdata"

RPM_X86=(
    "tesseract-ocr-5.5.3-4.1.x86_64.rpm"
    "libtesseract5-5.5.3-4.1.x86_64.rpm"
    "libleptonica6-1.87.0-1.6.x86_64.rpm"
)
RPM_NOARCH=(
    "tesseract-ocr-traineddata-fra-4.1.0+git.20240801.8741641-3.1.noarch.rpm"
    "tesseract-ocr-traineddata-eng-4.1.0+git.20240801.8741641-3.1.noarch.rpm"
    "tesseract-ocr-traineddata-spa-4.1.0+git.20240801.8741641-3.1.noarch.rpm"
    "tesseract-ocr-traineddata-osd-4.1.0+git.20240801.8741641-3.1.noarch.rpm"
)

version() {
    LD_LIBRARY_PATH="$PREFIXE/usr/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
    TESSDATA_PREFIX="$DATA" "$BIN" --version 2>/dev/null | head -1
}

langues() {
    LD_LIBRARY_PATH="$PREFIXE/usr/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
    TESSDATA_PREFIX="$DATA" "$BIN" --list-langs 2>/dev/null | sed '1d' | tr '\n' ' '
}

if [ "${1:-}" = "--verifie" ]; then
    if [ ! -x "$BIN" ]; then
        echo "  ❌ OCR absent : $BIN (lancer tools/installer_ocr.sh)"
        exit 1
    fi
    echo "  ✅ $(version) · langues : $(langues)"
    exit 0
fi

command -v rpm2cpio >/dev/null || { echo "  ❌ rpm2cpio absent"; exit 2; }
command -v cpio >/dev/null || { echo "  ❌ cpio absent"; exit 2; }
command -v curl >/dev/null || { echo "  ❌ curl absent"; exit 2; }

mkdir -p "$PREFIXE" "$PREFIXE/../rpm"
cd "$PREFIXE/../rpm"

telecharge() {  # $1 = sous-dossier du dépôt, $2 = fichier
    [ -s "$2" ] && return 0
    curl -fsSLO "$DEPOT/$1/$2"
}

for f in "${RPM_X86[@]}"; do telecharge x86_64 "$f"; done
for f in "${RPM_NOARCH[@]}"; do telecharge noarch "$f"; done

for f in *.rpm; do
    rpm2cpio "$f" | (cd "$PREFIXE" && cpio -idm --quiet)
done

# Les configs (`tsv`, `hocr`) ne sont pas dans le paquet de données ; on n'en dépend pas :
# l'appel passe `-c tessedit_create_tsv=1` (voir graphe_document_ocr.py). On les écrit quand
# même, parce qu'un utilisateur qui appelle tesseract à la main les cherchera.
mkdir -p "$DATA/configs"
printf 'tessedit_create_tsv 1\n' > "$DATA/configs/tsv"
printf 'tessedit_create_hocr 1\n' > "$DATA/configs/hocr"

echo "  ✅ $(version)"
echo "     langues : $(langues)"
echo "     binaire : $BIN"
