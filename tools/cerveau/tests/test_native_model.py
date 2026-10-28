from __future__ import annotations
import tempfile, pathlib, unittest
try:
    import torch
    from tools.native_model import NativeConfig, NativeModel, exporter_drvm
    from tools.drvm import read_drvm
    _TORCH = True
except ImportError:
    _TORCH = False


@unittest.skipUnless(_TORCH, "torch absent")
class TestNativeModel(unittest.TestCase):
    def test_formes(self):
        cfg = NativeConfig(d_model=32, n_blocks=2, n_heads=4, expert_hidden=16,
                           n_experts=4, early_blocks=(1,))
        m = NativeModel(cfg).eval()
        out = m(torch.randint(0, 256, (2, 8)))
        self.assertEqual(out["logits"].shape, (2, 8, 256))
        self.assertEqual(len(out["early"]), 1)
        self.assertEqual(out["rsn"].shape, (2, 8, cfg.rsn_dim))

    def test_arret_precoce(self):
        cfg = NativeConfig(d_model=32, n_blocks=4, n_heads=4, expert_hidden=16,
                           n_experts=4, early_blocks=(1, 2, 3))
        m = NativeModel(cfg).eval()
        out = m.forward_jusqua(torch.randint(0, 256, (1, 8)), 2)
        self.assertEqual(out["logits"].shape, (1, 8, 256))
        self.assertIsNotNone(out["early"])

    def test_taille_12m(self):
        m = NativeModel()
        n = m.nb_parametres()
        self.assertGreater(n, 9_000_000)
        self.assertLess(n, 14_000_000)

    def test_export_drvm(self):
        cfg = NativeConfig(d_model=32, n_blocks=2, n_heads=4, expert_hidden=16,
                           n_experts=4, early_blocks=(1,), rsn_dim=8)
        m = NativeModel(cfg).eval()
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "n0.drvm"
            h = exporter_drvm(m, str(p))
            self.assertEqual(len(h), 64)
            with read_drvm(p) as f:
                self.assertEqual(f.manifest["model"]["name"], "drave-n0")
                self.assertIn("b0", [b["id"] for b in f.manifest["graph"]["blocks"]])
                self.assertGreater(len(f.manifest["tensors"]), 5)

    def test_kwta(self):
        from tools.native_model import SparseFFN
        cfg = NativeConfig(d_model=16, expert_hidden=8, n_experts=2, kwta=0.25)
        f = SparseFFN(cfg).eval()
        x = torch.randn(1, 3, 16)
        y = f(x)
        self.assertEqual(y.shape, (1, 3, 16))


if __name__ == "__main__":
    unittest.main()
