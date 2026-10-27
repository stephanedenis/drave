from __future__ import annotations

import random
import unittest

from cerveau.memoire_travail import MemoireTravail
from cerveau.sequences import partie
from semantique.universaux import CHAMPS


def code(**kw):
    c = {nom: None for nom, _ in CHAMPS}
    c.update(kw)
    return c


A = code(jeu="echecs", action="deplacer", de=52, vers=36)
B = code(jeu="echecs", action="deplacer", de=62, vers=45)
C = code(jeu="morpion", action="jouer_case", case=0, symbole="X")
D = code(jeu="cartes", action="jouer_carte", carte=47)
E = code(jeu="go", action="poser", point=48, taille=9)


class Seq:
    def __init__(self, codes):
        self.pas = [type("P", (), {"code": c})() for c in codes]


class TestMemoireTravail(unittest.TestCase):
    def test_span_est_la_capacite(self):
        # Le span ne peut pas échouer : charger() copie exactement les codes.
        rng = random.Random(1)
        seqs = [[{nom: rng.choice(vals) for nom, vals in CHAMPS} for _ in range(12)]
                for _ in range(20)]
        m = MemoireTravail(12)
        r = m.span([Seq(s) for s in seqs])
        self.assertEqual(r["span"], 12)
        self.assertEqual(r["exact"], 1.0)

    def test_interference_positionnelle(self):
        # Cinq cibles, huit distracteurs : le tampon de 12 garde 4 cibles.
        # Similaires (mutants) et dissemblables donnent le MÊME taux : aucune
        # interférence sémantique, seulement l'éviction FIFO.
        def retention(dis):
            m = MemoireTravail(12)
            for c in [A, B, C, D, E] + dis:
                m.pousser(c)
            return sum(1 for c in (A, B, C, D, E) if m.retrouver(c)["exact"]) / 5

        similaires = [code(jeu="echecs", action="deplacer", de=52, vers=35),
                      code(jeu="echecs", action="deplacer", de=61, vers=45),
                      code(jeu="morpion", action="jouer_case", case=1, symbole="X"),
                      code(jeu="cartes", action="jouer_carte", carte=46),
                      code(jeu="go", action="poser", point=49, taille=9),
                      code(jeu="echecs", action="deplacer", de=53, vers=36),
                      code(jeu="morpion", action="jouer_case", case=2, symbole="X"),
                      code(jeu="cartes", action="jouer_carte", carte=45)]
        dissemblables = [code(jeu="dames", action="prendre", chemin_0=8),
                         code(jeu="dames", action="prendre", chemin_0=9),
                         code(jeu="morpion", action="jouer_case", case=4),
                         code(jeu="morpion", action="jouer_case", case=8),
                         code(jeu="cartes", action="jouer_carte", carte=34),
                         code(jeu="cartes", action="jouer_carte", carte=50),
                         code(jeu="go", action="poser", point=30, taille=9),
                         code(jeu="go", action="passer", passe=True, taille=9)]
        self.assertEqual(retention(similaires), retention(dissemblables))
        self.assertEqual(retention(similaires), 0.8)

    def test_leurre_proche_distance_un(self):
        m = MemoireTravail(12)
        m.pousser(A)
        leurre = code(jeu="echecs", action="deplacer", de=52, vers=44)
        self.assertTrue(m.retrouver(A)["exact"])
        r = m.retrouver(leurre)
        self.assertFalse(r["exact"])
        self.assertEqual(r["distance"], 1)

    def test_bruit_detruit_l_exactitude(self):
        # Un code corrompu sur un champ n'est plus relu exactement : aucune
        # correction d'erreur, le taux exact chute en (1-p)^n.
        rng = random.Random(2)
        seqs = [[{nom: rng.choice(vals) for nom, vals in CHAMPS} for _ in range(5)]
                for _ in range(100)]

        def exact(p):
            ok = 0
            for s in seqs:
                b = [dict(c) for c in s]
                for c in b:
                    if rng.random() < p:
                        nom = rng.choice([n for n, _ in CHAMPS])
                        c[nom] = rng.choice([v for v in dict(CHAMPS)[nom] if v != c[nom]])
                m = MemoireTravail(12)
                m.charger(b)
                ok += int(all(m.lire(i) == s[i] for i in range(5)))
            return ok / len(seqs)

        self.assertEqual(exact(0.0), 1.0)
        self.assertLess(exact(0.2), 0.5)

    def test_saturation_capacite(self):
        rng = random.Random(3)
        base = [{nom: rng.choice(vals) for nom, vals in CHAMPS} for _ in range(12)]
        seqs = [Seq(base)]
        self.assertEqual(MemoireTravail(3).span(seqs)["span"], 3)
        self.assertEqual(MemoireTravail(7).span(seqs)["span"], 7)
        m = MemoireTravail(3)
        m.charger(base[:3])
        self.assertTrue(all(m.lire(i) == base[i] for i in range(3)))
        m.charger(base[:4])  # 4 > 3 : décalage silencieux, plus aucune position exacte
        self.assertFalse(any(m.lire(i) == base[i] for i in range(4)))

    def test_span_reel_ne_depend_pas_du_contenu(self):
        s = partie("echecs", 0, 5)
        self.assertGreaterEqual(MemoireTravail(12).span([s])["span"], 1)


if __name__ == "__main__":
    unittest.main()
