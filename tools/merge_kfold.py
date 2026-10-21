#!/usr/bin/env python3
"""merge_kfold.py — pooler les plis d'une validation croisée (marge appariée + IC bootstrap)."""
from __future__ import annotations
import glob, json, sys
import numpy as np


def main() -> int:
    motif = sys.argv[1] if len(sys.argv) > 1 else "reports/kfold-7b-amp-*.json"
    pages = []
    for f in sorted(glob.glob(motif)):
        d = json.load(open(f))
        pages.extend(d["pages"])
    dd = np.array([x["chrf"] - x["plancher"] for x in pages])
    rng = np.random.default_rng(1234)
    boot = [float(np.mean(rng.choice(dd, len(dd), replace=True))) for _ in range(5000)]
    par_conte = {}
    for x in pages:
        par_conte.setdefault(x["histoire"], []).append(x["chrf"] - x["plancher"])
    print(f"{len(pages)} pages · chrF {np.mean([x['chrf'] for x in pages]):.1f} · "
          f"plancher {np.mean([x['plancher'] for x in pages]):.1f} · "
          f"marge {dd.mean():+.1f} [{np.percentile(boot, 2.5):+.1f} ; {np.percentile(boot, 97.5):+.1f}] · "
          f">0 {int((dd > 0).sum())}/{len(dd)}")
    for h, v in sorted(par_conte.items()):
        print(f"  {h}: n {len(v)} · marge {np.mean(v):+.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
