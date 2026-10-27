from __future__ import annotations
import sys, pathlib, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from tools.seuil_reseau import mesurer


class TestSeuilReseau(unittest.TestCase):
    def test_seuil(self):
        r = mesurer()
        self.assertGreater(r["octets"]["dense"], r["octets"]["sparse"])
        self.assertEqual(len(r["latences"]), 5)
        self.assertIn("seuil_latence_ms", r)


if __name__ == "__main__":
    unittest.main()
