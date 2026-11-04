"""Tests du store de Pensée — la file FIFO ne se fige pas.

Le bug (03/11) : `push` numérotait avec `len(self.ouverts)`. Après un `pop`, la
longueur baisse et le nœud suivant **réutilise** un numéro déjà pris — deux nœuds
à égalité de score sont alors départagés par leur empreinte, pas par l'ordre
d'ouverture, et le BFS voit une frontière qui ne suit plus la file.

Le correctif : un compteur monotone `_seq`, et un nœud re-poussé **après un pop**
reprend un numéro neuf. Ces tests échouent sur l'ancien code (2/3) et passent sur
le nouveau : c'est le contrôle négatif.
"""
import pathlib
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))
from tools.pensee.store import Store  # noqa: E402


class TestFileFIFO(unittest.TestCase):
    def test_pas_de_collision_apres_pop(self):
        s = Store()
        s.push("z", 1.0)  # 0
        s.push("b", 1.0)  # 1
        self.assertEqual([f for _, _, f in s.frontier()], ["z", "b"])
        self.assertEqual(s.pop(), "z")
        s.push("a", 1.0)  # 2 ; l'ancien code donnait 1, en collision avec b
        self.assertEqual([f for _, _, f in s.frontier()], ["b", "a"])

    def test_repush_prend_un_numero_neuf(self):
        s = Store()
        s.push("a", 1.0)  # 0
        s.push("b", 1.0)  # 1
        self.assertEqual(s.pop(), "a")
        s.push("a", 1.0)  # 2
        self.assertEqual([f for _, _, f in s.frontier()], ["b", "a"])

    def test_frontier_trie_par_score(self):
        s = Store()
        s.push("bas", 0.2)
        s.push("haut", 0.9)
        self.assertEqual([f for _, _, f in s.frontier()], ["haut", "bas"])


if __name__ == "__main__":
    unittest.main()
