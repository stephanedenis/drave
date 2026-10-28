from __future__ import annotations
import unittest
try:
    from tools.kv_gen import mesurer
    _TORCH = True
except ImportError:
    _TORCH = False


@unittest.skipUnless(_TORCH, "torch absent")
class TestKVGen(unittest.TestCase):
    def test_gen(self):
        r = mesurer(device="cpu", n=2)
        self.assertIn("identiques", r)


if __name__ == "__main__":
    unittest.main()
