#!/usr/bin/env python3
"""r13_anglais.py — R13.3/R13.4 : le BPE perd-il à octets égaux, sur l'anglais ?

POURQUOI CE SCRIPT EXISTE. R13.3 a mesuré les bits/octet de bytes, BPE 512 et BPE 1024 sur
`corpus_en.txt`, mais **le script n'a pas été committé** : la fiche ne donnait que les chiffres.
R13.4 est la **deuxième graine** demandée par R13.3 ; ce script est le dispositif reproductible,
et il accepte la graine pour que les deux mesures soient comparables.

Ce qu'il fait, dans l'ordre :
  1. entraîne les tokenizers BPE 512 et 1024 sur le corpus d'entraînement, tokenise la validation
     avec le MÊME tokenizer (pas de fuite) ;
  2. entraîne trois modèles natifs de même architecture avec la MÊME graine : bytes (vocab 256),
     BPE 512, BPE 1024 — aux pas demandés ;
  3. lit `bits_par_octet_val` des trois JSON d'entraînement, calcule les écarts et écrit le JSON.

Usage :
  python3 tools/r13_anglais.py --graine 2 --sortie reports/r13.4-anglais.json
  python3 tools/r13_anglais.py --graine 2 --pas-bytes 20 --pas-512 10 --pas-1024 8   # pipeline
"""
from __future__ import annotations
import argparse
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time

RACINE = pathlib.Path(__file__).resolve().parent.parent
PY = os.environ.get("PY", "/home/stephane/gpu-env/bin/python")
DEVICE = os.environ.get("DEVICE", "cuda")


def run(cmd: list[str], journal: pathlib.Path) -> str:
    """Exécute une commande dans la racine ; garde le journal ; lève en cas d'échec."""
    with open(journal, "w", encoding="utf-8") as f:
        p = subprocess.run(cmd, cwd=RACINE, stdout=f, stderr=subprocess.STDOUT, text=True)
    if p.returncode != 0:
        raise SystemExit(f"échec : {' '.join(cmd[:4])}… (voir {journal})\n"
                         + "\n".join(journal.read_text(errors="ignore").splitlines()[-5:]))
    return journal.read_text(encoding="utf-8", errors="ignore")


def tokeniser(corpus: pathlib.Path, vocab: int, dossier: pathlib.Path, nom: str,
              tokenizer: pathlib.Path | None = None) -> dict:
    """Tokenise un corpus ; rend les stats (octets, jetons, octets/jeton, réversible)."""
    tok = dossier / f"{nom}-{vocab}.json"
    ids = dossier / f"{nom}-{vocab}-ids.pt"
    octets = dossier / f"{nom}-{vocab}-octets.pt"
    stats = dossier / f"{nom}-{vocab}-stats.json"
    cmd = [PY, "tools/tokenizer_bpe.py", "--corpus", str(corpus), "--vocab", str(vocab),
           "--sortie-tokenizer", str(tok), "--sortie-ids", str(ids),
           "--sortie-octets", str(octets), "--stats", str(stats)]
    if tokenizer is not None:
        cmd += ["--tokenizer", str(tokenizer)]
    run(cmd, dossier / f"{nom}-{vocab}.log")
    return json.loads(stats.read_text())


def entrainer(ids: pathlib.Path, val_ids: pathlib.Path, val_octets: int, vocab: int,
              octets: int, pas: int, graine: int, dossier: pathlib.Path,
              nom: str) -> dict:
    """Entraîne un modèle natif ; rend son JSON d'entraînement."""
    sortie = dossier / f"{nom}.pt"
    cmd = [PY, "-m", "tools.entrainer_native_tokens",
           "--ids", str(ids), "--val-ids", str(val_ids), "--val-octets", str(val_octets),
           "--vocab", str(vocab), "--octets", str(octets), "--pas", str(pas),
           "--seq", "128", "--lot", "8", "--device", DEVICE, "--graine", str(graine),
           "--sortie", str(sortie), "--drvm", str(dossier / f"{nom}.drvm")]
    run(cmd, dossier / f"{nom}.log")
    return json.loads(pathlib.Path(str(sortie) + ".json").read_text())


def principal() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpus", default="data/corpus_en.txt")
    ap.add_argument("--val", default="data/corpus_en_val.txt")
    ap.add_argument("--graine", type=int, default=2)
    ap.add_argument("--pas-bytes", type=int, default=10000)
    ap.add_argument("--pas-512", type=int, default=5000)
    ap.add_argument("--pas-1024", type=int, default=4000)
    ap.add_argument("--sortie", default="reports/r13.4-anglais.json")
    a = ap.parse_args()
    corpus, val = RACINE / a.corpus, RACINE / a.val
    if not corpus.is_file() or not val.is_file():
        raise SystemExit(f"corpus absent : {corpus} / {val}")

    with tempfile.TemporaryDirectory(prefix="r13-anglais-") as td:
        d = pathlib.Path(td)
        print(f"=== R13 — {corpus.name} → {val.name} · graine {a.graine} ===", flush=True)

        print("1. tokenizers 512 et 1024 + validation séparée", flush=True)
        s512 = tokeniser(corpus, 512, d, "train")
        v512 = tokeniser(val, 512, d, "val", tokenizer=d / "train-512.json")
        s1024 = tokeniser(corpus, 1024, d, "train")
        v1024 = tokeniser(val, 1024, d, "val", tokenizer=d / "train-1024.json")
        print(f"   train {s512['octets']} octets · val {v512['octets']} octets · "
              f"val BPE 512 {v512['jetons']} · BPE 1024 {v1024['jetons']} jetons", flush=True)

        modeles: dict[str, dict] = {}
        print(f"2. bytes — {a.pas_bytes} pas, graine {a.graine}", flush=True)
        t0 = time.time()
        r = entrainer(d / "train-512-octets.pt", d / "val-512-octets.pt", v512["octets"],
                      256, s512["octets"], a.pas_bytes, a.graine, d, "bytes")
        modeles[f"bytes_{a.pas_bytes // 1000}k"] = {
            "pas": a.pas_bytes, "ppl_val": r["ppl_val"],
            "bits_par_octet_val": r["bits_par_octet_val"],
            "precision_main": r["precision_main"], "duree_s": r["duree_s"]}
        print(f"   {r['bits_par_octet_val']:.4f} bits/octet · {r['duree_s']:.0f} s", flush=True)

        for vocab, pas, cle in ((512, a.pas_512, "512"), (1024, a.pas_1024, "1024")):
            print(f"3. BPE {vocab} — {pas} pas, graine {a.graine}", flush=True)
            r = entrainer(d / f"train-{vocab}-ids.pt", d / f"val-{vocab}-ids.pt",
                          (v512 if vocab == 512 else v1024)["octets"], vocab,
                          s512["octets"], pas, a.graine, d, f"bpe{vocab}")
            modeles[f"bpe{vocab}_{pas // 1000}k"] = {
                "pas": pas, "ppl_val": r["ppl_val"],
                "bits_par_octet_val": r["bits_par_octet_val"],
                "precision_main": r["precision_main"], "duree_s": r["duree_s"]}
            print(f"   {r['bits_par_octet_val']:.4f} bits/octet · {r['duree_s']:.0f} s", flush=True)

    ref = modeles[f"bytes_{a.pas_bytes // 1000}k"]["bits_par_octet_val"]
    ecarts = {}
    for cle in ("512", "1024"):
        b = modeles[f"bpe{cle}_{(a.pas_512 if cle == '512' else a.pas_1024) // 1000}k"]
        ecarts[f"bpe{cle}"] = round(100.0 * (b["bits_par_octet_val"] - ref) / ref, 2)
    perd = all(v > 0 for v in ecarts.values())
    resultat = {
        "date": "2026-10-30",
        "ligne": "R13.4",
        "graine": a.graine,
        "corpus": f"{a.corpus} / {a.val}",
        "dispositif": "tools/r13_anglais.py",
        "donnees": {"train_octets": s512["octets"], "val_octets": v512["octets"],
                    "bpe512_val_jetons": v512["jetons"],
                    "bpe1024_val_jetons": v1024["jetons"]},
        "modeles": modeles,
        "ecarts_pct": ecarts,
        "verdict": ("le BPE perd encore à octets égaux sur l'anglais"
                    if perd else "le signe change avec cette graine"),
        "controle": "même tokenizer pour train et val, même architecture, même graine "
                    "pour bytes et BPE ; val séparée",
        "limites": ["une graine de plus, pas la convergence",
                    "anglais 100 Mo", "précision par jeton non comparable"],
        "prochain": ["plus de pas", "corpus multilingue"],
    }
    sortie = RACINE / a.sortie
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n")
    print(f"   → {sortie}")
    print(json.dumps({"ecarts_pct": ecarts, "verdict": resultat["verdict"]}, ensure_ascii=False))
    return 0 if perd else 1


if __name__ == "__main__":
    raise SystemExit(principal())
