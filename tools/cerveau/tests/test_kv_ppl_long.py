from __future__ import annotations
import unittest
try:
    from tools.kv_ppl_long import mesurer
    _TORCH = True
except ImportError:
    _TORCH = False


@unittest.skipUnless(_TORCH, "torch absent")
class TestKVPplLong(unittest.TestCase):
    def test_mesure(self):
        r = mesurer(ntok=32, device="cpu")
        self.assertGreater(r["ppl_base"], 0)


if __name__ == "__main__":
    unittest.main()
