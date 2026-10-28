from __future__ import annotations
import sys, pathlib, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from tools.kv_reseau import decoder_kv, encoder_kv, _kv


class TestKVReseau(unittest.TestCase):
    def test_aller_retour(self):
        kv = _kv(8)
        b = encoder_kv(kv)
        self.assertTrue((decoder_kv(b) == kv).all())

    def test_mesure(self):
        from tools.kv_reseau import mesurer
        r = mesurer(ntok=8, essais=2)
        self.assertTrue(r["fidelite"])
        self.assertEqual(r["messages_identiques"], True)


if __name__ == "__main__":
    unittest.main()
