#!/bin/bash
# porte-tableaux.sh — un tableau Markdown qui ne rend pas est un tableau qui n'existe PAS.
#
# POURQUOI CETTE PORTE EXISTE. Le 13/10, le premier tableau de `docs/etat-cerveau.md` s'affichait
# comme du TEXTE dans mdserve : une seule ligne (`| **C2 (cycle 2 régions)** | … |`) avait
# **4 cellules pour 5 colonnes** — un lien qui avait glissé d'une colonne. Le rendu (mistune,
# puis markdown_it, puis markdown) refuse alors le tableau ENTIER, sans rien dire : les 13 lignes
# disparaissent de la page et personne ne le voit, parce que le texte est toujours là, en gris.
#
# CE QU'ELLE VÉRIFIE (trois conditions, toutes nécessaires au rendu) :
#   1. l'en-tête et le séparateur d'un tableau ont le MÊME nombre de cellules ;
#   2. chaque ligne du corps a ce nombre de cellules ;
#   3. aucun `\|` ne subsiste : mistune ne le déséchappe NI dans un espace de code NI dans la
#      prose (il s'affiche alors littéralement). Pour une barre de valeur absolue dans du code,
#      on écrit `∣` (U+2223), qui rend partout et ne casse pas la lecture.
# Les tableaux DANS une citation (`> | … |`) sont valides et vérifiés aussi.
#
# CE QU'ELLE NE VÉRIFIE PAS : les tableaux « écrasés » sur une seule ligne (perte de retours à la
# ligne à l'écriture) — ils ne sont pas détectables sans heuristique, et un faux positif dans une
# porte coûte plus cher que le défaut. Cas connus, laissés tels quels et nommés :
# `journal/2026-10-10-reprise-historique.md` en porte huit, dans un récit historique.
#
# Usage : tools/porte-tableaux.sh            # docs, reports, journal, sprints, README, REPRISE
#         CIBLES="docs" tools/porte-tableaux.sh
set -u
cd "$(dirname "$0")/.."
CIBLES=${CIBLES:-"docs reports journal sprints README.md REPRISE.md"}
python3 - $CIBLES <<'PY'
import pathlib, re, sys

def depouille(l):
    s = l.rstrip("\n")
    if s.lstrip().startswith('>'):
        s = s.lstrip()[1:]
    return s.strip()

def cellules(l):
    s = depouille(l)
    if s.startswith('|'): s = s[1:]
    if s.endswith('|') and not s.endswith('\\|'): s = s[:-1]
    return len(re.split(r'(?<!\\)\|', s))

def est_sep(l):
    return bool(re.fullmatch(r"\|?(\s*:?-{2,}:?\s*\|)+\s*:?-{2,}:?\s*\|?", depouille(l)))

def est_ligne(l):
    s = depouille(l)
    return s.startswith('|')

fichiers = []
for c in sys.argv[1:]:
    p = pathlib.Path(c)
    if p.is_dir():
        fichiers += [f for f in sorted(p.rglob('*.md'))
                     if 'sessions' not in f.parts and 'archive' not in f.parts]
    elif p.is_file():
        fichiers.append(p)

def ressemble_a_une_ligne(l):
    """Une ligne qui a l'air d'une ligne de tableau : elle commence et finit par `|` et porte au
    moins deux barres non échappées. Sert à voir les lignes ORPHELINES — celles d'un tableau
    interrompu par autre chose (une citation, une règle, un paragraphe), qui ne rendent pas.
    C'est le défaut trouvé le 13/10 : un bloc de citation s'était glissé au milieu du tableau des
    capacités, et les lignes C9 à C12bis se sont retrouvées hors du tableau, en texte."""
    s = depouille(l)
    return s.startswith('|') and s.endswith('|') and len(re.split(r'(?<!\\)\|', s)) >= 3

defauts = []
for f in fichiers:
    lignes = f.read_text(encoding='utf-8', errors='replace').splitlines()
    dans_bloc, i = False, 0
    while i < len(lignes):
        l = lignes[i]
        if l.lstrip().startswith('```'):
            dans_bloc = not dans_bloc; i += 1; continue
        if dans_bloc:
            i += 1; continue
        # `\|` n'est un défaut QUE là où mistune ne le déséchappe pas : dans un espace de code
        # (backticks) ou hors d'un tableau. Ailleurs il rend une barre, et c'est légitime — une
        # porte qui crie là où tout va bien se fait ignorer.
        if '\\|' in l:
            for m in re.finditer(r'`[^`]*`', l):
                if '\\|' in m.group(0):
                    defauts.append((f, i + 1, "« \\| » DANS un espace de code : il s'affiche "
                                              "littéralement — écrire ∣ (U+2223)"))
                    break
            else:
                if not est_ligne(l) and not est_sep(l) and l.strip() and not l.lstrip().startswith('#'):
                    defauts.append((f, i + 1, "« \\| » hors tableau : l'antislash s'affiche — hors tableau, "
                                              "une barre simple suffit (∣ pour une valeur absolue)"))
        # LIGNE ORPHELINE : elle a la forme d'une ligne de tableau, mais aucun en-tête ne la
        # précède — le tableau a été interrompu, et tout ce qui suit ne rend pas.
        if ressemble_a_une_ligne(l) and not est_ligne(l):
            defauts.append((f, i + 1, "ligne de tableau HORS d'un tableau — un tableau interrompu "
                                      "par une citation, une règle ou un paragraphe ?"))
            i += 1; continue
        if est_ligne(l) and not (i + 1 < len(lignes) and est_sep(lignes[i + 1])):
            defauts.append((f, i + 1, "ligne de tableau sans en-tête ni séparateur (orpheline)"))
            i += 1; continue
        if est_ligne(l) and i + 1 < len(lignes) and est_sep(lignes[i + 1]):
            attendu = cellules(lignes[i + 1])
            if cellules(l) != attendu:
                defauts.append((f, i + 1, f"en-tête {cellules(l)} cellules ≠ séparateur {attendu}"))
            i += 2
            while i < len(lignes) and est_ligne(lignes[i]):
                if cellules(lignes[i]) != attendu:
                    defauts.append((f, i + 1, f"{cellules(lignes[i])} cellules ≠ {attendu} attendues"))
                i += 1
            continue
        i += 1

if defauts:
    print(f"  ❌ {len(defauts)} tableau(x) ne rendront pas (mistune refuse le tableau ENTIER) :")
    for f, l, quoi in defauts[:20]:
        print(f"     {f}:{l} — {quoi}")
    sys.exit(f"  {len(fichiers)} fichier(s) examiné(s)")
print(f"  ✅ {len(fichiers)} fichier(s) : chaque tableau a le même nombre de cellules partout "
      f"(en-tête, séparateur, lignes), et aucun « \\| » ne s'affichera")
PY
# ⚠️ ET LE CODE DE SORTIE DE PYTHON DOIT ÊTRE CELUI DE LA PORTE. Sans cette ligne, `sys.exit(...)` du
# bloc ci-dessus n'arrêtait que **Python** ✗ : la porte **imprimait** ses défauts et sortait en **0**
# ✓✗ — une vérification qui ne peut pas échouer, exactement la famille de défaut que ce dépôt nomme la
# pire. Découvert le 16/10, après huit rounds de commits passés avec un tableau cassé ✓✗.
[ $? -eq 0 ] || exit 1

# ---- ET LES LIENS : un document de ce dépôt EST fait de renvois, et un renvoi mort ne casse rien au
# moment où on l'écrit — il casse six semaines plus tard. Deux secondes ici, à chaque passe.
python3 tools/verifier_liens.py || exit 1

# ---- ET LA PAGE VIVANTE DOIT SUIVRE LE TRAVAIL. `docs/en-cours.md` est la page que le serveur
# affiche en premier, et c'est elle qui répond à « où en est le travail ? » ✓. Une page qui date d'hier
# pendant qu'on commite aujourd'hui est **pire** qu'une page absente ✗ : elle affirme un état faux ✓.
# Ce contrôle est donc **daté**, objectif, et il échoue en disant QUOI faire ✓.
DERNIER=$(git log -1 --format=%ad --date=short 2>/dev/null || echo "")
PAGE=$(grep -oE "Mis à jour : [0-9]{4}-[0-9]{2}-[0-9]{2}" docs/en-cours.md 2>/dev/null | head -1 | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2}")
if [ -n "$DERNIER" ] && [ -n "$PAGE" ] && [ "$PAGE" != "$DERNIER" ]; then
    echo "  ❌ LA PAGE VIVANTE EST EN RETARD : docs/en-cours.md dit « Mis à jour : $PAGE »,"
    echo "     et le dernier commit date du $DERNIER."
    echo "     → mettre à jour docs/en-cours.md (l'état du travail, les questions ouvertes, ce qui est"
    echo "       nouveau), puis relancer cette porte. Un petit cycle sans page à jour est un cycle"
    echo "       que personne ne peut lire."
    exit 1
fi
echo "  ✅ la page vivante date du dernier commit ($PAGE)"
