from __future__ import annotations
import sys, pathlib, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from tools.kv_int8 import decoder, encoder, mesurer
from tools.kv_reseau import _kv


class TestKVInt8(unittest.TestCase):
    def test_aller_retour(self):
        kv = _kv(8)
        b = encoder(kv)
        self.assertEqual(decoder(b).shape, kv.shape)

    def test_mesure(self):
        r = mesurer(ntok=8)
        self.assertLess(r["ratio"], 1.0)
        self.assertGreaterEqual(r["diff_max"], 0.0)


if __name__ == "__main__":
    unittest.main()
