from __future__ import annotations
import pathlib, struct, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from tools.gguf_drvm import drvm_vers_gguf, gguf_vers_drvm
from tools.convertir_clusters import lire_entete


def _gguf(path):
    kv = b""
    cle = b"general.alignment"
    kv += struct.pack("<Q", len(cle)) + cle + struct.pack("<I", 4) + struct.pack("<I", 32)
    with open(path, "wb") as f:
        f.write(b"GGUF"); f.write(struct.pack("<I", 3))
        f.write(struct.pack("<Q", 1)); f.write(struct.pack("<Q", 1)); f.write(kv)
        nom = b"t"
        f.write(struct.pack("<Q", len(nom)) + nom)
        f.write(struct.pack("<I", 2))
        f.write(struct.pack("<Q", 2)); f.write(struct.pack("<Q", 2))
        f.write(struct.pack("<I", 0)); f.write(struct.pack("<Q", 0))
        fin = f.tell(); f.write(b"\0" * ((32 - fin % 32) % 32))
        f.write(struct.pack("<4f", 1.0, 2.0, 3.0, 4.0))


class TestGGUFDRVM(unittest.TestCase):
    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            g = pathlib.Path(d) / "a.gguf"; m = pathlib.Path(d) / "a.drvm"; g2 = pathlib.Path(d) / "b.gguf"
            _gguf(g)
            r = gguf_vers_drvm(str(g), str(m))
            self.assertEqual(r["tenseurs"], 1)
            drvm_vers_gguf(str(m), str(g2))
            _, t, base, _, _, _ = lire_entete(str(g2))
            self.assertEqual(len(t), 1)
            with open(g2, "rb") as f:
                f.seek(base + t[0]["offset"]); b = f.read(t[0]["octets"])
            self.assertEqual(struct.unpack("<4f", b), (1.0, 2.0, 3.0, 4.0))


if __name__ == "__main__":
    unittest.main()
