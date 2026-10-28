from __future__ import annotations
import pathlib, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from tools.drvm import TensorSpec, write_drvm
from tools.drvm_trace import rejouer, tracer
from tools.drvm import read_drvm


def _m():
    return {"format":"DRVM","version":0,"model":{"name":"t"},
            "graph":{"blocks":[{"id":"b0","kind":"input"}]},"execution":{}}


class TestTrace(unittest.TestCase):
    def test_trace_replay(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)/"a.drvm"
            write_drvm(p,_m(),[TensorSpec("b0.w",b"abc",bloc="b0")])
            t=tracer(str(p))
            self.assertEqual(len(t["tenseurs"]),1)
            r=rejouer(str(p),t)
            self.assertTrue(r["identiques"]); self.assertTrue(r["manifeste_sha256"])

    def test_trace_detecte(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)/"a.drvm"
            write_drvm(p,_m(),[TensorSpec("b0.w",b"abc",bloc="b0")])
            t=tracer(str(p)); t["tenseurs"][0]["sha256"]="0"*64
            r=rejouer(str(p),t)
            self.assertFalse(r["identiques"])


if __name__ == "__main__":
    unittest.main()
