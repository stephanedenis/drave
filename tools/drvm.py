#!/usr/bin/env python3
"""drvm.py — DRVM v0, le conteneur natif du modèle Drave.

DRVM n'est pas un GGUF amélioré : c'est un conteneur de **graphe** et de **blocs**.
Le manifeste porte les blocs, les ports, les routes, les têtes, le pont et la
cellule de pensée ; le payload porte les tenseurs alignés, lisibles par bloc et
mmap-ables. Le lecteur refuse une version ou un type de bloc qu'il ne connaît pas.

Structure :
  en-tête 92 o (magie, version, tailles, offsets, deux SHA-256)
  manifeste JSON canonique, aligné sur 64 o
  payload de tenseurs, chaque tenseur aligné sur 64 o

CLI :
  python3 tools/drvm.py inspect MODELE.drvm
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mmap
import os
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

MAGIC = b"DRVM"
VERSION = 0
ALIGNEMENT = 64
HEADER = struct.Struct("<4sHH I Q Q 32s 32s")  # 92 octets
BLOCS_CONNUS = {
    "input", "local_mixer", "sparse_ffn", "state", "early_head",
    "thought", "bridge", "output",
}
SECTIONS = ("model", "graph", "tensors", "execution")


class DRVMError(ValueError):
    """Erreur de format DRVM."""


@dataclass
class TensorSpec:
    name: str
    data: bytes
    dtype: str = "f32"
    shape: tuple[int, ...] = ()
    bloc: str = ""
    quant: str | None = None
    sparsity: float = 0.0


@dataclass
class DrvmFile:
    manifest: dict[str, Any]
    _mm: mmap.mmap
    _fichier: Any
    payload_offset: int = 0
    tensors: dict[str, dict[str, Any]] = field(default_factory=dict)

    def tensor(self, name: str) -> memoryview:
        t = self.tensors.get(name)
        if t is None:
            raise DRVMError(f"tenseur inconnu : {name}")
        off = self.payload_offset + int(t["offset"])
        n = int(t["nbytes"])
        return memoryview(self._mm)[off:off + n]

    def close(self) -> None:
        try:
            self._mm.close()
        finally:
            self._fichier.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


def _canonique(manifest: dict[str, Any]) -> bytes:
    return json.dumps(manifest, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def _aligne(n: int) -> int:
    return (int(n) + ALIGNEMENT - 1) // ALIGNEMENT * ALIGNEMENT


def _valide(manifest: dict[str, Any]) -> None:
    for section in SECTIONS:
        if section not in manifest:
            raise DRVMError(f"section absente : {section}")
    if manifest.get("format") != "DRVM":
        raise DRVMError("format != DRVM")
    if manifest.get("version") != VERSION:
        raise DRVMError(f"version non supportée : {manifest.get('version')}")
    blocs = manifest["graph"].get("blocks")
    if not isinstance(blocs, list) or not blocs:
        raise DRVMError("graphe sans bloc")
    ids = set()
    for b in blocs:
        if "id" not in b or "kind" not in b:
            raise DRVMError(f"bloc incomplet : {b!r}")
        if b["id"] in ids:
            raise DRVMError(f"bloc dupliqué : {b['id']}")
        ids.add(b["id"])
        if b["kind"] not in BLOCS_CONNUS:
            raise DRVMError(f"type de bloc inconnu : {b['kind']}")
    for t in manifest["tensors"]:
        if t.get("bloc") not in ids:
            raise DRVMError(f"tenseur rattaché à un bloc inconnu : {t.get('bloc')}")
        if int(t["nbytes"]) <= 0 or int(t["offset"]) % ALIGNEMENT:
            raise DRVMError(f"tenseur mal aligné ou vide : {t.get('name')}")


def write_drvm(path: str | os.PathLike, manifest: dict[str, Any],
               tensors: list[TensorSpec]) -> str:
    """Écrit un DRVM et retourne le SHA-256 du fichier."""
    manifest = json.loads(json.dumps(manifest))  # copie
    manifest.setdefault("format", "DRVM")
    manifest.setdefault("version", VERSION)
    if not tensors:
        raise DRVMError("aucun tenseur")
    noms = set()
    specs = []
    offset = 0
    for t in tensors:
        if t.name in noms:
            raise DRVMError(f"tenseur dupliqué : {t.name}")
        noms.add(t.name)
        if not t.data:
            raise DRVMError(f"tenseur vide : {t.name}")
        offset = _aligne(offset)
        specs.append({
            "name": t.name, "bloc": t.bloc, "dtype": t.dtype,
            "shape": list(t.shape), "offset": offset, "nbytes": len(t.data),
            "quant": t.quant, "sparsity": t.sparsity,
        })
        offset += len(t.data)
    manifest["tensors"] = specs
    _valide(manifest)
    mj = _canonique(manifest)
    mj_pad = mj + b"\0" * (_aligne(len(mj)) - len(mj))
    payload = bytearray()
    for t in tensors:
        payload.extend(b"\0" * (_aligne(len(payload)) - len(payload)))
        payload.extend(t.data)
    header = HEADER.pack(
        MAGIC, VERSION, HEADER.size, len(mj), HEADER.size + len(mj_pad),
        HEADER.size + len(mj_pad) + len(payload),
        hashlib.sha256(mj).digest(), hashlib.sha256(payload).digest(),
    )
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with tmp.open("wb") as f:
        f.write(header); f.write(mj_pad); f.write(payload)
    os.replace(tmp, p)
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_drvm(path: str | os.PathLike, verifier: bool = True) -> DrvmFile:
    """Lit un DRVM, vérifie l'en-tête, le manifeste et le payload (SHA-256)."""
    p = Path(path)
    f = p.open("rb")
    try:
        raw = f.read(HEADER.size)
        if len(raw) != HEADER.size:
            raise DRVMError("fichier trop court pour l'en-tête")
        magic, version, hsize, mlen, poff, total, msha, psha = HEADER.unpack(raw)
        if magic != MAGIC:
            raise DRVMError(f"mauvaise magie : {magic!r}")
        if version != VERSION:
            raise DRVMError(f"version non supportée : {version}")
        if hsize != HEADER.size or poff < hsize + mlen or poff > total:
            raise DRVMError("en-tête incohérent")
        if total != p.stat().st_size:
            raise DRVMError("taille de fichier incohérente")
        f.seek(hsize)
        mj = f.read(mlen)
        if hashlib.sha256(mj).digest() != msha:
            raise DRVMError("hash du manifeste invalide")
        try:
            manifest = json.loads(mj.decode("utf-8"))
        except Exception as e:
            raise DRVMError(f"manifeste JSON invalide : {e}") from e
        _valide(manifest)
        f.seek(0)
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        if verifier and hashlib.sha256(mm[poff:]).digest() != psha:
            mm.close()
            raise DRVMError("hash du payload invalide")
    except Exception:
        f.close()
        raise
    return DrvmFile(manifest=manifest, _mm=mm, _fichier=f, payload_offset=poff,
                    tensors={t["name"]: t for t in manifest["tensors"]})


def inspecter(path: str | os.PathLike) -> dict[str, Any]:
    with read_drvm(path) as d:
        return {
            "fichier": str(path),
            "manifest_sha256": hashlib.sha256(_canonique(d.manifest)).hexdigest(),
            "modele": d.manifest["model"],
            "blocs": [b["id"] for b in d.manifest["graph"]["blocks"]],
            "tenseurs": len(d.manifest["tensors"]),
            "octets_payload": sum(int(t["nbytes"]) for t in d.manifest["tensors"]),
            "version": d.manifest["version"],
        }


def main() -> None:
    ap = argparse.ArgumentParser(description="DRVM v0 — conteneur natif Drave")
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("inspect")
    i.add_argument("fichier")
    a = ap.parse_args()
    if a.cmd == "inspect":
        print(json.dumps(inspecter(a.fichier), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
