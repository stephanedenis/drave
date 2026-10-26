import unittest

from jeux.rsn import (Annotation, ErreurRSN, RSN, decode_binaire, differences,
                      encode_binaire, meme_corps)


class TestRSN(unittest.TestCase):
    def test_ordre_des_cles_ne_change_pas_lempreinte(self):
        a = RSN("morpion", "etat", {"taille": 3, "trait": "X", "cases": [None] * 9})
        b = RSN("morpion", "etat", {"cases": [None] * 9, "trait": "X", "taille": 3})
        self.assertEqual(a.empreinte(), b.empreinte())
        self.assertEqual(a.octets_json(), b.octets_json())

    def test_annotation_hors_empreinte(self):
        a = RSN("morpion", "etat", {"taille": 3, "cases": [None] * 9, "trait": "X"})
        b = a.avec_annotation(langue="fr", surface="tout autre chose", confiance=0.2)
        self.assertEqual(a.empreinte(), b.empreinte())
        self.assertNotEqual(a.annotation, b.annotation)

    def test_binaire_aller_retour(self):
        a = RSN("echecs", "coup", {"de": 52, "vers": 36, "promotion": None, "roque": None})
        buf = a.octets_binaire()
        b = decode_binaire(buf)
        self.assertEqual(a.empreinte(), b.empreinte())
        self.assertLess(len(buf), len(a.octets_json()))

    def test_binaire_avec_annotation(self):
        a = RSN("go", "coup", {"taille": 9, "point": 48},
                Annotation(langue="fr", format="gtp", confiance=0.9,
                           ambiguites=("A",), surface="D4", niveau=4))
        b = decode_binaire(encode_binaire(a, avec_annotation=True))
        self.assertEqual(a.empreinte(), b.empreinte())
        self.assertEqual(b.annotation.langue, "fr")
        self.assertEqual(b.annotation.ambiguites, ("A",))

    def test_flottant_refuse(self):
        with self.assertRaises(ErreurRSN):
            RSN("go", "etat", {"komi": 6.5})

    def test_differences(self):
        a = RSN("morpion", "etat", {"taille": 3, "cases": [None] * 9, "trait": "X"})
        b = RSN("morpion", "etat", {"taille": 3, "cases": ["X"] + [None] * 8, "trait": "O"})
        d = differences(a.corps, b.corps)
        self.assertIn(("corps.cases[0]", None, "X"), d)
        self.assertIn(("corps.trait", "X", "O"), d)
        ok, _ = meme_corps(a, b)
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
