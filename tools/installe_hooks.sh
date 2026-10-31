#!/bin/sh
# installe_hooks.sh — installe le hook pre-commit versionné (état + journal).
#
# Le hook est dans tools/hooks/pre-commit, pas seulement dans .git/hooks : il est
# ainsi versionné, relu en revue, et réinstallable. À lancer après un clone.
set -u
cd "$(dirname "$0")/.."
install -m 0755 tools/hooks/pre-commit .git/hooks/pre-commit \
    || { echo "  ❌ hook NON installé (voir l'erreur ci-dessus)"; exit 1; }
[ -x .git/hooks/pre-commit ] || { echo "  ❌ .git/hooks/pre-commit absent ou non exécutable"; exit 1; }
echo "  hook installé : .git/hooks/pre-commit (état + journal)"
