from __future__ import annotations
import json, pathlib, struct, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from tools.drvm import (ALIGNEMENT, DRVMError, HEADER, MAGIC, VERSION,
                        TensorSpec, read_drvm, write_drvm)


def _manifest():
    return {
        "format": "DRVM", "version": VERSION,
        "model": {"name": "test", "parametres": 4, "tokenizer": {"kind": "bytes", "vocab": 256}},
        "graph": {
            "regions": [{"id": "r0", "blocks": ["b0"]}],
            "blocks": [{"id": "b0", "kind": "input", "inputs": [], "outputs": ["h"]}],
            "routes": [], "heads": [], "thought": None, "bridge": None,
        },
        "execution": {"activation": "DRVF", "placement": "local"},
    }


class TestDRVM(unittest.TestCase):
    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "m.drvm"
            h = write_drvm(p, _manifest(), [TensorSpec("b0.w", b"\x01\x02\x03\x04", shape=(2, 2), bloc="b0")])
            self.assertEqual(len(h), 64)
            with read_drvm(p) as m:
                self.assertEqual(bytes(m.tensor("b0.w")), b"\x01\x02\x03\x04")
                self.assertEqual(m.manifest["model"]["name"], "test")
                self.assertEqual(int(m.manifest["tensors"][0]["offset"]), 0)

    def test_version_refusee(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "m.drvm"
            write_drvm(p, _manifest(), [TensorSpec("b0.w", b"x", bloc="b0")])
            b = bytearray(p.read_bytes())
            struct.pack_into("<H", b, 4, 99)
            p.write_bytes(b)
            with self.assertRaises(DRVMError):
                read_drvm(p)

    def test_bloc_inconnu(self):
        m = _manifest()
        m["graph"]["blocks"][0]["kind"] = "quantum"
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(DRVMError):
                write_drvm(pathlib.Path(d) / "m.drvm", m, [TensorSpec("b0.w", b"x", bloc="b0")])

    def test_tronque(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "m.drvm"
            write_drvm(p, _manifest(), [TensorSpec("b0.w", b"x" * 100, bloc="b0")])
            p.write_bytes(p.read_bytes()[:-10])
            with self.assertRaises(DRVMError):
                read_drvm(p)

    def test_alignement(self):
        self.assertEqual(ALIGNEMENT, 64)
        self.assertEqual(HEADER.size, 92)
        self.assertEqual(MAGIC, b"DRVM")

    def test_deux_tenseurs_alignes(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "m.drvm"
            write_drvm(p, _manifest(), [
                TensorSpec("b0.a", b"a" * 3, bloc="b0"),
                TensorSpec("b0.b", b"b" * 70, bloc="b0"),
            ])
            with read_drvm(p) as m:
                self.assertEqual(int(m.manifest["tensors"][0]["offset"]), 0)
                self.assertEqual(int(m.manifest["tensors"][1]["offset"]), 64)
                self.assertEqual(bytes(m.tensor("b0.b")), b"b" * 70)


if __name__ == "__main__":
    unittest.main()
