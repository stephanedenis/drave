from __future__ import annotations
import pathlib, sys, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from tools.vdc import departs_vdc, ordre_vdc, vdc


class TestVDC(unittest.TestCase):
    def test_premiers_termes(self):
        self.assertEqual([vdc(i) for i in range(4)], [0.0, 0.5, 0.25, 0.75])

    def test_deterministe(self):
        self.assertEqual(departs_vdc(10, 16, 1000, 128), departs_vdc(10, 16, 1000, 128))

    def test_ordre_permutation(self):
        o = ordre_vdc(8)
        self.assertEqual(sorted(o), list(range(8)))

    def test_bornes(self):
        d = departs_vdc(0, 100, 129, 128)
        self.assertTrue(all(0 <= x < 129 for x in d))


if __name__ == "__main__":
    unittest.main()
