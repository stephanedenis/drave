import unittest

from jeux.codecs import detecte_jeu, lit, rend
from jeux.corpus import construire_corpus
from jeux.mesure import collisions, couverture, invariance, restitution
from jeux.regles import cartes as C
from jeux.regles import dames as D
from jeux.regles import echecs as E
from jeux.regles import go as G
from jeux.regles import morpion as M
from jeux.rsn import RSN


class TestCouches(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = construire_corpus()

    def test_couverture_niveau4(self):
        c = couverture(self.corpus, 4)
        self.assertEqual(c["bons"], c["total"])

    def test_ablation_monotone(self):
        taux = [couverture(self.corpus, n)["taux"] for n in range(5)]
        self.assertEqual(taux, sorted(taux))
        self.assertLess(taux[0], 0.6)
        self.assertEqual(taux[4], 1.0)

    def test_invariance_niveau4(self):
        i = invariance(self.corpus, 4)
        self.assertEqual(i["bonnes"], i["total"])

    def test_collisions(self):
        c = collisions(self.corpus, 4)
        self.assertEqual(c["collisions"], 0)

    def test_restitution(self):
        r = restitution(self.corpus)
        self.assertEqual(r["bons"], r["total"], r["echecs"])


class TestAmbiguites(unittest.TestCase):
    def test_coordonnees_nues_refusees(self):
        for surface in ("A1", "E4", "d4", "b6-c5"):
            l = lit(surface)
            self.assertFalse(l.ok, surface)
            self.assertTrue(l.erreurs, surface)
            self.assertIn("ambigu", " ".join(l.erreurs).lower(), surface)

    def test_jeu_explicite_leve_l_ambiguite(self):
        self.assertTrue(lit("A1", jeu="morpion", niveau=4).ok)
        self.assertTrue(lit("E4", jeu="go", niveau=4).ok)
        self.assertTrue(lit("d4", jeu="go", niveau=4).ok)
        self.assertTrue(lit("b6-c5", jeu="dames", niveau=4).ok)

    def test_surfaces_non_ambigues_inchangees(self):
        self.assertEqual(lit("e2e4").jeu, "echecs")
        self.assertEqual(lit("2D").jeu, "cartes")


class TestMorpion(unittest.TestCase):
    def test_grille_et_trait(self):
        l = lit("X O X | . . . | . . .", jeu="morpion", niveau=4)
        self.assertTrue(l.ok)
        self.assertEqual(l.rsn.corps["cases"][:3], ["X", "O", "X"])
        self.assertEqual(l.rsn.corps["trait"], "O")

    def test_case_nommee(self):
        vide = M.etat_initial()
        for texte, i in (("A1", 0), ("B1", 1), ("milieu", 4), ("haut gauche", 0),
                         ("bas droite", 8)):
            l = lit(texte, jeu="morpion", niveau=4, contexte=vide)
            self.assertTrue(l.ok, texte)
            self.assertEqual(l.rsn.corps["case"], i, texte)
            self.assertEqual(l.rsn.corps["symbole"], "X")

    def test_o_au_trait(self):
        ctx = M.applique_indice(M.etat_initial(), 4)
        l = lit("O joue en bas à droite", jeu="morpion", niveau=4, contexte=ctx)
        self.assertTrue(l.ok)
        self.assertEqual(l.rsn.corps, {"case": 8, "symbole": "O"})


class TestEchecs(unittest.TestCase):
    def setUp(self):
        self.depart = E.rsn_depuis_position(E.Position.depart())

    def test_fen_et_uci(self):
        l = lit(E.Position.depart().fen(), jeu="echecs", niveau=4)
        self.assertTrue(l.ok)
        self.assertEqual(l.rsn.empreinte(), self.depart.empreinte())
        l = lit("e2e4", jeu="echecs", niveau=4, contexte=self.depart)
        self.assertTrue(l.ok)
        self.assertEqual(l.rsn.corps, {"de": 52, "vers": 36, "promotion": None, "roque": None})

    def test_san_francais(self):
        for texte in ("Nf3", "Cf3", "cavalier de g1 vers f3", "g1f3"):
            l = lit(texte, jeu="echecs", niveau=4, contexte=self.depart)
            self.assertTrue(l.ok, texte)
            self.assertEqual(l.rsn.corps["de"], 62, texte)
            self.assertEqual(l.rsn.corps["vers"], 45, texte)

    def test_roque(self):
        ctx = E.rsn_depuis_position(E.Position.depuis_fen(
            "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1"))
        for texte, de, vers, roque in (("O-O", 60, 62, "K"), ("petit roque", 60, 62, "K"),
                                       ("O-O-O", 60, 58, "Q"), ("grand roque", 60, 58, "Q")):
            l = lit(texte, jeu="echecs", niveau=4, contexte=ctx)
            self.assertTrue(l.ok, texte)
            self.assertEqual(l.rsn.corps, {"de": de, "vers": vers,
                                           "promotion": None, "roque": roque}, texte)

    def test_en_passant_et_promotion(self):
        ctx = E.rsn_depuis_position(E.Position.depuis_fen(
            "rnbqkbnr/ppp1pppp/8/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3"))
        l = lit("exd6", jeu="echecs", niveau=4, contexte=ctx)
        self.assertTrue(l.ok)
        self.assertEqual(l.rsn.corps["de"], 28)
        self.assertEqual(l.rsn.corps["vers"], 19)
        ctx2 = E.rsn_depuis_position(E.Position.depuis_fen("8/P7/8/8/8/8/7p/4K2k w - - 0 1"))
        l = lit("a8=Q", jeu="echecs", niveau=4, contexte=ctx2)
        self.assertTrue(l.ok)
        self.assertEqual(l.rsn.corps["promotion"], "q")

    def test_fen_ep_inutile_canonisee(self):
        a = lit("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
                jeu="echecs", niveau=4)
        b = lit("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
                jeu="echecs", niveau=4)
        self.assertTrue(a.ok and b.ok)
        self.assertEqual(a.rsn.empreinte(), b.rsn.empreinte())

    def test_pgn(self):
        l = lit("1. e4 e5 2. Nf3 Nc6", jeu="echecs", niveau=4)
        self.assertTrue(l.ok)
        self.assertEqual(l.rsn.nature, "partie")
        self.assertEqual(len(l.rsn.corps["coups"]), 4)


class TestDames(unittest.TestCase):
    def setUp(self):
        self.depart = D.rsn_depuis_position(D.Position.depart())

    def test_compact_et_diagramme(self):
        for texte in ("bbbbbbbbbbbb........wwwwwwwwwwww b", rend(self.depart, "diagramme")):
            l = lit(texte, jeu="dames", niveau=4)
            self.assertTrue(l.ok, texte)
            self.assertEqual(l.rsn.empreinte(), self.depart.empreinte())

    def test_prise_simple_et_multiple(self):
        cases = [D.VIDE] * 32
        cases[8] = D.NOIR_PION
        cases[13] = D.BLANC_PION
        cases[22] = D.BLANC_PION
        ctx = D.rsn_depuis_position(D.Position(cases, D.NOIR))
        for texte, chemin in (("9x18x27", [8, 17, 26]), ("b6xd4xf2", [8, 17, 26]),
                              ("le pion b6 prend en d4 puis f2", [8, 17, 26])):
            l = lit(texte, jeu="dames", niveau=4, contexte=ctx)
            self.assertTrue(l.ok, texte)
            self.assertEqual(l.rsn.corps["chemin"], chemin, texte)

    def test_coup_simple_noir_et_blanc(self):
        l = lit("9-14", jeu="dames", niveau=4, contexte=self.depart)
        self.assertTrue(l.ok)
        self.assertEqual(l.rsn.corps["chemin"], [8, 13])
        ctxb = D.rsn_depuis_position(D.Position(D.Position.depart().cases, D.BLANC))
        l = lit("c3-d4", jeu="dames", niveau=4, contexte=ctxb)
        self.assertTrue(l.ok)
        self.assertEqual(l.rsn.corps["chemin"], [21, 17])


class TestGo(unittest.TestCase):
    def setUp(self):
        self.vide = G.Position.depart(9, 65).vers_rsn()

    def test_diagramme_et_gtp(self):
        l = lit(rend(self.vide, "diagramme"), jeu="go", niveau=4)
        self.assertTrue(l.ok)
        self.assertEqual(l.rsn.empreinte(), self.vide.empreinte())
        l = lit("D4", jeu="go", niveau=4, contexte=self.vide)
        self.assertTrue(l.ok)
        self.assertEqual(l.rsn.corps, {"taille": 9, "point": 48})

    def test_sgf_et_passe(self):
        l = lit("B[dd]", jeu="go", niveau=4, contexte=self.vide)
        self.assertTrue(l.ok)
        self.assertEqual(l.rsn.corps, {"taille": 9, "point": 30})
        for texte in ("pass", "passer", "je passe"):
            l = lit(texte, jeu="go", niveau=4, contexte=self.vide)
            self.assertTrue(l.ok, texte)
            self.assertTrue(l.rsn.corps.get("passe"), texte)

    def test_illegal_sur_occupation(self):
        p = G.Position.depuis_rsn(self.vide)
        ctx = p.joue(G.gtp_vers_point("D4", 9)).vers_rsn()
        l = lit("D4", jeu="go", niveau=4, contexte=ctx)
        self.assertFalse(l.ok)


class TestCartes(unittest.TestCase):
    def test_donne_aller_retour(self):
        etat = C.rsn_depuis_position(C.Position.depart(42))
        l = lit(rend(etat, "donne"), jeu="cartes", niveau=4)
        self.assertTrue(l.ok)
        self.assertEqual(l.rsn.empreinte(), etat.empreinte())

    def test_noms_fr_en_et_court(self):
        etat = C.rsn_depuis_position(C.Position.depart(42))
        tour = int(etat.corps["tour"])
        carte = etat.corps["mains"][tour][0]
        for texte in (C.nom_court(carte), C.nom_carte(carte, "fr"), C.nom_carte(carte, "en")):
            l = lit(texte, jeu="cartes", niveau=4, contexte=etat)
            self.assertTrue(l.ok, texte)
            self.assertEqual(l.rsn.corps["carte"], carte, texte)

    def test_main_triee(self):
        l = lit("Q♥ A♥ K♥", jeu="cartes", niveau=4)
        self.assertTrue(l.ok)
        self.assertEqual(l.rsn.corps["cartes"], [42, 46, 50])


class TestDetection(unittest.TestCase):
    def test_indices_distinctifs(self):
        cas = [
            ("XOX/.../...", "morpion"),
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "echecs"),
            ("bbbbbbbbbbbb........wwwwwwwwwwww b", "dames"),
            ("(;GM[1]FF[4]SZ[9];B[dd];W[ee])", "go"),
            ("whist atout=H | N: AS KH | E: QD | S: JC | W: 2D", "cartes"),
        ]
        for texte, jeu in cas:
            j, _ = detecte_jeu(texte)
            self.assertEqual(j, jeu, texte)


if __name__ == "__main__":
    unittest.main()
