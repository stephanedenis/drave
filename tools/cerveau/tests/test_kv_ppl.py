from __future__ import annotations
import unittest
try:
    from tools.kv_ppl import mesurer
    _TORCH = True
except ImportError:
    _TORCH = False


@unittest.skipUnless(_TORCH, "torch absent")
class TestKVPpl(unittest.TestCase):
    def test_mesure(self):
        r = mesurer(device="cpu")
        self.assertGreater(r["ppl_base"], 0)
        self.assertGreater(r["ppl_kv_int8"], 0)


if __name__ == "__main__":
    unittest.main()
