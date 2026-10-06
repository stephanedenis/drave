#!/usr/bin/env python3
"""LA POSITION SEULE — de combien l'alignement de l'UDHR gonfle-t-il la fidélité ?

LE DOUTE À LEVER. L'UDHR est UN texte traduit en 392 langues : à la position t,
toutes les langues disent la même chose. La couche 0 encode la position, donc une
lecture `e_t → y_t` peut apprendre « à la position t, sors le vecteur typique de
t » et réussir sans rien comprendre à la langue. Si c'est le cas, le §29 (l'entrée
seule bat le réservoir) mesure un artefact de corpus.

LE TÉMOIN QUI LE QUANTIFIE, et il n'a besoin d'AUCUNE lecture. On prédit la ligne t
d'une tranche de test par la MOYENNE des lignes t des tranches d'apprentissage :
c'est le meilleur prédicteur possible qui ne connaisse QUE la position. Aucun
paramètre, aucun neurone, aucune entrée.

Sur l'UDHR il devrait être élevé (le contenu est le même partout). Sur Wikipedia, où
les tranches sont des ARTICLES DIFFÉRENTS, il devrait s'effondrer. L'écart entre les
deux chiffres EST la taille du gonflement.

Usage : position_seule.py <cache_appr.npz> <cache_test.npz> [--appr 0.8]
"""
import sys

import numpy as np

sys.path.insert(0, "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools")
from pont_generatif import charge, cos_lignes  # noqa: E402


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def main():
    tr_p = sys.argv[1]
    te_p = (sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--')
            else None)
    if te_p is None:
        # un seul fichier : on coupe 80/20. C'est le cas de Wikipedia, où les
        # tranches sont des ARTICLES DIFFÉRENTS — le partage est donc arbitraire et
        # sans effet, ce qui est précisément ce qu'on veut mesurer.
        cles, E, Y, H = charge(tr_p)
        n = int(len(cles)*0.8)
        cltr, clte = cles[:n], cles[n:]
        Etr, Ete = E[:n], E[n:]
        Ytr, Yte = Y[:n], Y[n:]
    else:
        cltr, Etr, Ytr, H = charge(tr_p)
        clte, Ete, Yte, _ = charge(te_p)
    print(f"# apprentissage {len(cltr)} tranches · test {len(clte)} tranches · H={H}")

    # longueur commune : on ne peut moyenner la ligne t que jusqu'à la plus courte
    Lmin = min(min(len(y) for y in Ytr), min(len(y) for y in Yte))
    print(f"# tranche la plus courte : {Lmin} pas — moyenne faite sur [0, {Lmin}[")

    P = np.zeros((Lmin, H))
    for y in Ytr:
        P += y[:Lmin]
    P /= len(Ytr)

    # moyenne des longueurs pour situer les deux corpus
    print(f"# longueur moyenne — apprentissage "
          f"{np.mean([len(y) for y in Ytr]):.0f} · test "
          f"{np.mean([len(y) for y in Yte]):.0f}")

    tot = []
    for k in range(len(clte)):
        y = Yte[k][:Lmin]
        tot.append(cos_lignes(P, y))
    print(f"\n# FIDÉLITÉ DE LA POSITION SEULE")
    print(f"#   par tranche  : moyenne {np.mean(tot):.4f} · "
          f"médiane {np.median(tot):.4f} · min {np.min(tot):.4f} · "
          f"max {np.max(tot):.4f}")

    # et la constante (une seule ligne pour toutes les positions), pour comparer
    m = np.vstack([y[:Lmin] for y in Ytr]).mean(0)
    cons = [cos_lignes(np.tile(m, (Lmin, 1)), Yte[k][:Lmin]) for k in range(len(clte))]
    print(f"#   constante (sans position) : moyenne {np.mean(cons):.4f}")
    print(f"#   CE QUE LA POSITION AJOUTE : {np.mean(tot)-np.mean(cons):+.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
