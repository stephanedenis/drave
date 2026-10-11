#!/usr/bin/env python3
"""verifier_chaine_etat.py — la chaîne hors-ligne reproduit-elle la perplexité DU MOTEUR ?

POURQUOI CE SCRIPT EXISTE. Les mesures de profondeur routée (dessin H) lisent des états capturés
par le moteur et les repassent par la norme finale et la tête liée, hors du moteur, en Python.
Si cette relecture est fausse — mauvais tenseur, mauvaise norme, états lus à l'envers — les
chiffres qui en sortent sont faux **et rien ne le signale** : ils restent des nombres plausibles.

Ce script compare donc, sur la MÊME capture, la perplexité calculée hors-ligne et celle que le
moteur a imprimée pendant la capture. C'est une comparaison, pas une cohérence : les deux nombres
viennent de deux chemins de code différents, et l'un des deux est la référence.

Usage :
  tools/verifier_chaine_etat.py --etats /tmp/verif/e16 --ids F --modele M --ppl-attendue 456586.5954
"""
from __future__ import annotations

import argparse
import sys
import pathlib

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lecture_etat import Tete, charger_etats, charger_ids  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--etats", required=True, help="préfixe : PREFIXE.<position>")
    ap.add_argument("--ids", required=True)
    ap.add_argument("--modele", required=True)
    ap.add_argument("--ppl-attendue", type=float, required=True,
                    help="la perplexité imprimée par le moteur sur CETTE capture")
    ap.add_argument("--tolerance", type=float, default=2e-3,
                    help="écart relatif toléré (défaut 0,2 %%)")
    a = ap.parse_args()

    pos, X = charger_etats(a.etats)
    if len(pos) < 2:
        raise SystemExit(f"{a.etats} : {len(pos)} position(s), il en faut au moins 2")
    # La convention du moteur : `ppl = exp(nll / (ids.len() - 1))`, donc une prédiction par
    # position 0..len-2. On charge donc exactement les ids qui vont avec ces états.
    limite = int(pos.max()) + 2
    ids = charger_ids(a.ids, limite)
    if limite > len(ids):
        raise SystemExit(f"{a.ids} : {len(ids)} jetons, il en faut {limite} pour ces positions")
    if not np.array_equal(pos, np.arange(pos.min(), pos.max() + 1)):
        raise SystemExit("les positions ne sont pas contiguës : la comparaison au moteur "
                         "(qui prédit sur toutes les positions) ne serait pas exacte")
    y = ids[pos + 1]

    tete = Tete(a.modele)
    ppl = tete.ppl(X, y)
    ecart = abs(ppl - a.ppl_attendue) / max(a.ppl_attendue, 1e-12)
    print(f"  positions {pos.min()}..{pos.max()} ({len(pos)} états, {len(y)} prédictions)")
    print(f"  perplexité hors-ligne : {ppl:,.4f}")
    print(f"  perplexité du moteur  : {a.ppl_attendue:,.4f}")
    print(f"  écart relatif         : {100 * ecart:.4f} %  (toléré {100 * a.tolerance:.2f} %)")
    if ecart > a.tolerance:
        print("  ❌ la relecture hors-ligne NE reproduit PAS le moteur : tout chiffre qui en "
              "découle est à jeter")
        return 2
    print(f"  ✅ la chaîne hors-ligne reproduit le moteur à {100 * ecart:.4f} % près")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
