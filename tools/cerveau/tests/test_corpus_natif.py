from __future__ import annotations
import pathlib, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from tools.corpus_natif import construire


class TestCorpusNatif(unittest.TestCase):
    def test_fenetres(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d)/"c.bin"; p.write_bytes(bytes(range(256))*10)
            r = construire(str(p), fenetre=32, pas=16, max_fenetres=100, val=10)
            self.assertEqual(r["fenetres"], 100)
            self.assertEqual(r["train"] + r["val"], 100)
            self.assertEqual(len(r["offsets_train"]), 90)


if __name__ == "__main__":
    unittest.main()
