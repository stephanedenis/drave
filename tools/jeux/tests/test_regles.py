import unittest

from jeux.regles import cartes as C
from jeux.regles import dames as D
from jeux.regles import echecs as E
from jeux.regles import go as G
from jeux.regles import morpion as M


class TestMorpionRegles(unittest.TestCase):
    def test_valeur_exacte(self):
        v, c = M.resous(M.etat_initial())
        self.assertEqual(v, 0.0)
        self.assertIn(c, range(9))

    def test_partie_parfaite_nulle(self):
        etat = M.etat_initial()
        while not M.terminal(etat):
            _, c = M.resous(etat)
            etat = M.applique_indice(etat, c)
        self.assertEqual(M.resultat(etat), "N")
        self.assertEqual(len(M.etats_atteignables()), 5478)


class TestEchecsRegles(unittest.TestCase):
    def test_perft_references(self):
        refs = [
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", [20, 400, 8902]),
            ("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
             [48, 2039, 97862]),
            ("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1", [14, 191, 2812]),
            ("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1",
             [6, 264, 9467]),
            ("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8",
             [44, 1486, 62379]),
            ("r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10",
             [46, 2079, 89890]),
        ]
        for fen, attendus in refs:
            pos = E.Position.depuis_fen(fen)
            self.assertEqual([pos.perft(d) for d in range(1, len(attendus) + 1)], attendus, fen)

    def test_san_aller_retour(self):
        pos = E.Position.depart()
        for san in ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "O-O"]:
            c, cands, err = pos.parse_san(san)
            self.assertIsNotNone(c, (san, err))
            self.assertEqual(pos.san(c), san)
            pos.joue(c)

    def test_roque_ep_promotion(self):
        pos = E.Position.depuis_fen("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
        c, _, _ = pos.parse_san("O-O")
        self.assertEqual((c.de, c.vers, c.drapeau), (60, 62, E.ROQUE_K))
        c, _, _ = pos.parse_san("O-O-O")
        self.assertEqual((c.de, c.vers, c.drapeau), (60, 58, E.ROQUE_Q))
        pos = E.Position.depuis_fen("rnbqkbnr/ppp1pppp/8/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3")
        c, _, _ = pos.parse_san("exd6")
        self.assertEqual((c.de, c.vers, c.drapeau), (28, 19, E.EP))
        pos = E.Position.depuis_fen("8/P7/8/8/8/8/7p/4K2k w - - 0 1")
        c, _, _ = pos.parse_san("a8=Q")
        self.assertEqual((c.de, c.vers, c.promotion), (8, 0, E.DAME))


class TestDamesRegles(unittest.TestCase):
    def test_perft_references(self):
        pos = D.Position.depart()
        self.assertEqual([pos.perft(d) for d in range(1, 7)],
                         [7, 49, 302, 1469, 7361, 36768])

    def test_prises_obligatoires(self):
        cases = [D.VIDE] * 32
        cases[8] = D.NOIR_PION
        cases[13] = D.BLANC_PION
        cases[22] = D.BLANC_PION
        pos = D.Position(cases, D.NOIR)
        self.assertEqual([c.chemin for c in pos.coups_legaux()], [(8, 17, 26)])
        # une prise simple, et le pion capturé disparaît
        cases = [D.VIDE] * 32
        cases[8] = D.NOIR_PION
        cases[13] = D.BLANC_PION
        pos = D.Position(cases, D.NOIR)
        q = pos.applique(pos.coups_legaux()[0])
        self.assertEqual(q.cases[13], D.VIDE)
        self.assertEqual(q.cases[17], D.NOIR_PION)

    def test_promotion(self):
        cases = [D.VIDE] * 32
        cases[24] = D.NOIR_PION
        pos = D.Position(cases, D.NOIR)
        for c in pos.coups_legaux():
            if c.chemin[-1] // 4 == 7:
                q = pos.applique(c)
                self.assertEqual(q.cases[c.chemin[-1]], D.NOIR_DAME)
                return
        self.fail("aucune promotion générée")


class TestGoRegles(unittest.TestCase):
    def test_vide_capture_suicide_ko(self):
        self.assertEqual(len(G.Position.depart(5, 0).coups_legaux()), 25)
        b = [0] * 25
        def I(r, c): return r * 5 + c
        b[I(2, 2)] = G.NOIR
        for r, c in ((1, 2), (3, 2), (2, 1)):
            b[I(r, c)] = G.BLANC
        p = G.Position(5, b, G.BLANC, -1, 0, 0)
        q = p.joue(I(2, 3))
        self.assertEqual(q.plateau[I(2, 2)], G.VIDE)
        b2 = [0] * 25
        for r, c in ((0, 1), (1, 0)):
            b2[I(r, c)] = G.BLANC
        self.assertFalse(G.Position(5, b2, G.NOIR, -1, 0, 0).coup_legal(I(0, 0)))
        b3 = [0] * 16
        def J(r, c): return r * 4 + c
        for r, c in ((0, 1), (1, 0), (2, 1)):
            b3[J(r, c)] = G.NOIR
        for r, c in ((0, 2), (1, 1), (1, 3), (2, 2)):
            b3[J(r, c)] = G.BLANC
        p3 = G.Position(4, b3, G.NOIR, -1, 0, 0)
        q3 = p3.joue(J(1, 2))
        self.assertEqual(q3.ko, J(1, 1))
        self.assertFalse(q3.coup_legal(J(1, 1)))

    def test_score_connu(self):
        b = [0] * 9
        for r, c in ((0, 1), (1, 0), (1, 2), (2, 1)):
            b[r * 3 + c] = G.NOIR
        p = G.Position(3, b, G.NOIR, -1, 0, 0)
        self.assertEqual(p.score(), (90, 0))

    def test_coordonnees(self):
        self.assertEqual(G.gtp_vers_point("D4", 9), 48)
        self.assertEqual(G.point_vers_gtp(48, 9), "D4")
        self.assertEqual(G.sgf_vers_point("dd", 9), 30)
        self.assertEqual(G.point_vers_sgf(30, 9), "dd")


class TestCartesRegles(unittest.TestCase):
    def test_gagnant_du_pli(self):
        def mk(cards, atout):
            return C.Position([[], [], [], []], atout, 0, 0, 0,
                              [[i, c] for i, c in enumerate(cards)], [0, 0])
        w1 = mk([C.carte_id(10, 2), C.carte_id(13, 2), C.carte_id(2, 2), C.carte_id(3, 2)], -1)
        self.assertEqual(w1.gagnant_pli(), 1)
        w2 = mk([C.carte_id(14, 2), C.carte_id(2, 0), C.carte_id(2, 3), C.carte_id(3, 3)], 3)
        self.assertEqual(w2.gagnant_pli(), 3)

    def test_fournir_la_couleur(self):
        pos = C.Position.depart(0)
        premier = pos.coups_legaux()[0]
        p = pos.joue(premier)
        demandee = C.couleur(premier)
        main = p.mains[p.tour]
        if any(C.couleur(c) == demandee for c in main):
            self.assertTrue(all(C.couleur(c) == demandee for c in p.coups_legaux()))

    def test_donne_reproductible(self):
        a = C.Position.depart(42)
        b = C.Position.depart(42)
        self.assertEqual(a.cle(), b.cle())
        self.assertEqual(sum(len(m) for m in a.mains), 52)


if __name__ == "__main__":
    unittest.main()
