#!/usr/bin/env python3
"""verifier_liens.py — LES LIENS RELATIFS DES DOCUMENTS RÉSOLVENT-ILS ?

POURQUOI. Un document qui renvoie à une fiche **renommée** ou **supprimée** ne casse rien au moment
où on l'écrit ✗ : il casse **six semaines plus tard**, quand quelqu'un suit le lien et tombe sur un
fichier absent ✓. Et un document de ce dépôt **est** fait de renvois ✗ (chaque affirmation porte sa
fiche ✓, chaque fiche porte sa porte ✗) : les liens **sont** la documentation ✓. Les vérifier coûte
deux secondes ✓ et se fait à chaque passe ✓ (appelé par `porte-tableaux.sh`, la porte des documents ✓).

CE QUI EST EXAMINÉ : les liens relatifs de `docs/*.md` et `reports/*.md` — les documents **écrits à la
main** ✓. Les **journaux** sont exclus ✗ : ils sont auto-générés et renvoient à des sessions
(`sessions/<id>/rapport.md`) qui ne sont pas versionnées ✓ ; les signaler serait du bruit ✗✓. Les
**exemples de code** sont exclus aussi ✗ (un `[chemin](chemin)` dans un bloc ``` n'est pas un lien ✓),
**et les cibles sans barre ni point** ✓ (le même motif écrit **en prose**, pour décrire la vérification
elle-même, dans `rapport-coherence-docs-2.md` ✓ — les deux familles de faux positifs que le premier
essai a comptées ✓✗).

Usage : python3 tools/verifier_liens.py [--racine .]   (code 0 = tous les liens résolvent)
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

MOTIF = re.compile(r"\]\(([^)#]+?)(?:#[^)]*)?\)")


def sans_blocs_de_code(texte: str) -> str:
    return re.sub(r"```.*?```", "", texte, flags=re.S)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--racine", default=".")
    a = ap.parse_args()
    r = pathlib.Path(a.racine)
    manquants, total = [], 0
    for motif in ("docs/*.md", "reports/*.md"):
        for doc in sorted(r.glob(motif)):
            texte = sans_blocs_de_code(doc.read_text(errors="replace"))
            for lien in MOTIF.findall(texte):
                if lien.startswith(("http://", "https://", "mailto:")) or " " in lien:
                    continue                       # un lien externe, ou une phrase : pas un chemin
                if "/" not in lien and "." not in lien:
                    # ⚠️ UNE CIBLE SANS BARRE NI POINT EST UN EXEMPLE, PAS UN CHEMIN : le document
                    # `rapport-coherence-docs-2.md` écrit `[texte](chemin)` EN PROSE, pour décrire la
                    # vérification des liens elle-même ✗✓ — et c'est ce que le premier essai a compté,
                    # trois fois ✓. Aucun vrai renvoi de ce dépôt n'a cette forme (une fiche a un `.md`,
                    # un dossier a un `/`) ✓.
                    continue
                total += 1
                if not (doc.parent / lien).resolve().exists():
                    manquants.append(f"{doc.relative_to(r)} → {lien}")
    if manquants:
        print(f"  ❌ {len(manquants)} lien(s) relatif(s) ne résolvent pas (sur {total} examinés) :")
        for m in manquants[:20]:
            print(f"     {m}")
        if len(manquants) > 20:
            print(f"     … et {len(manquants) - 20} autre(s)")
        return 1
    print(f"  ✅ {total} lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
