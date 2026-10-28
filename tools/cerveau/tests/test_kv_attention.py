from __future__ import annotations
import sys, pathlib, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from tools.kv_attention import mesurer


class TestKVAttention(unittest.TestCase):
    def test_mesure(self):
        r = mesurer(ntok=8)
        self.assertEqual(r["ntok"], 8)
        self.assertGreaterEqual(r["argmax_accord"], 0.0)
        self.assertLessEqual(r["argmax_accord"], 1.0)


if __name__ == "__main__":
    unittest.main()
