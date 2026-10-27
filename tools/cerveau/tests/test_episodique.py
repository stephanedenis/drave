from __future__ import annotations

import unittest

from cerveau.episodique import Episodique
from semantique.universaux import CHAMPS


def code(**kw):
    c = {nom: None for nom, _ in CHAMPS}
    c.update(kw)
    return c


A = code(jeu="echecs", action="deplacer", de=52, vers=36)   # e2e4
A2 = code(jeu="echecs", action="deplacer", de=52, vers=44)  # e2e3 (non stocké)
B = code(jeu="echecs", action="deplacer", de=52, vers=45)   # même `de`, autre `vers`
C = code(jeu="echecs", action="deplacer", de=52, vers=44)   # même que A2


class TestEpisodique(unittest.TestCase):
    def test_code_non_stocke_n_est_pas_generalise(self):
        e = Episodique()
        e.stocker("e2e4", A)
        r = e.rappel(A2)
        self.assertFalse(r["exact"])
        c = e.completion(A2)
        self.assertFalse(c["exact"])
        self.assertEqual(c["code"], A)          # le voisin stocké, pas le code absent
        self.assertNotEqual(c["code"], A2)

    def test_fausse_memoire_du_voisin(self):
        # Code proche mais différent : la complétion renvoie le stocké avec
        # 14/15 champs ; le champ modifié du leurre est écrasé dans 99 % des cas.
        e = Episodique()
        e.stocker("e2e4", A)
        c = e.completion(A2)
        self.assertFalse(c["exact"])
        self.assertGreater(c["similarite"], 0.9)
        self.assertLess(c["similarite"], 1.0)
        self.assertEqual(c["code"]["vers"], 36)  # pas la valeur du leurre (44)

    def test_cue_ambigu_marge_nulle(self):
        # Deux codes stockés ne diffèrent que par `vers` ; le cue partagé a
        # `vers=None`. Les deux scores sont à égalité : la séparation est dite
        # distincte mais le choix est arbitraire (marge 0).
        e = Episodique()
        e.stocker("a", A)
        e.stocker("b", B)
        cue = dict(A); cue["vers"] = None
        c = e.completion(cue)
        self.assertFalse(c["exact"])
        self.assertLess(abs(c["marge"]), 1e-12)
        self.assertTrue(e.separation(A, B)["distincts"])

    def test_marge_depend_de_l_ordre_d_insertion(self):
        cue = dict(A); cue["vers"] = None
        e1 = Episodique(); e1.stocker("a", A); e1.stocker("b", B)
        e2 = Episodique(); e2.stocker("b", B); e2.stocker("a", A)
        self.assertNotEqual(e1.completion(cue)["code"], e2.completion(cue)["code"])

    def test_rappel_exact_reste_strict(self):
        e = Episodique()
        e.stocker("e2e4", A)
        self.assertTrue(e.rappel(A)["exact"])
        self.assertFalse(e.rappel(A2)["exact"])

    def test_score_ne_discrimine_pas_completion_et_leurre(self):
        # Un cue partiel légitime (vers manquant) et un leurre complet (vers
        # faux) ont exactement le même score top1 : 14/15. Aucun seuil ne peut
        # accepter l'un et rejeter l'autre.
        e = Episodique()
        e.stocker("e2e4", A)
        partiel = dict(A); partiel["vers"] = None
        s_partiel = e.completion(partiel)["similarite"]
        s_leurre = e.completion(A2)["similarite"]
        self.assertAlmostEqual(s_partiel, s_leurre, places=12)


if __name__ == "__main__":
    unittest.main()
