"""
Qtrinet — lecteur GGUF minimal (numpy pur, aucune dépendance).

Ne lit que ce dont on a besoin pour l'analyse de structure :
  - l'en-tête et les métadonnées (architecture, dimensions, nombre de têtes),
  - les tenseurs en F32 / F16 / Q8_0 / Q4_0 (suffisant pour étudier la structure),
  - les blocs de quantification (échelle + valeurs entières).

Format GGUF : magic "GGUF", version u32, n_tensors u64, n_kv u64,
puis les paires clé/valeur de métadonnées, puis les descripteurs de tenseurs,
puis (après alignement) les données.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from pathlib import Path

import numpy as np

# types de métadonnées GGUF
GGUF_UINT8, GGUF_INT8, GGUF_UINT16, GGUF_INT16 = 0, 1, 2, 3
GGUF_UINT32, GGUF_INT32, GGUF_FLOAT32, GGUF_BOOL = 4, 5, 6, 7
GGUF_STRING, GGUF_ARRAY, GGUF_UINT64, GGUF_INT64, GGUF_FLOAT64 = 8, 9, 10, 11, 12

# types de tenseurs ggml
GGML_F32, GGML_F16 = 0, 1
GGML_Q4_0, GGML_Q4_1 = 2, 3
GGML_Q8_0 = 8

_BLOCK = {GGML_Q4_0: (32, 18), GGML_Q8_0: (32, 34)}   # (valeurs/bloc, octets/bloc)
_ITEMSIZE = {GGML_F32: 4, GGML_F16: 2}


@dataclass
class TensorInfo:
    name: str
    shape: tuple[int, ...]
    ttype: int
    offset: int


class GGUF:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.f = open(self.path, "rb")
        magic = self.f.read(4)
        if magic != b"GGUF":
            raise ValueError("ce n'est pas un fichier GGUF")
        self.version = self._u32()
        self.n_tensors = self._u64()
        self.n_kv = self._u64()
        self.meta: dict = {}
        for _ in range(self.n_kv):
            k = self._str()
            self.meta[k] = self._value(self._u32())
        self.tensors: dict[str, TensorInfo] = {}
        for _ in range(self.n_tensors):
            name = self._str()
            nd = self._u32()
            dims = tuple(self._u64() for _ in range(nd))
            ttype = self._u32()
            off = self._u64()
            # ggml stocke les dimensions en sens inverse de numpy
            self.tensors[name] = TensorInfo(name, tuple(reversed(dims)), ttype, off)
        align = int(self.meta.get("general.alignment", 32))
        pos = self.f.tell()
        self.data_start = (pos + align - 1) // align * align

    # ---------------------------------------------------------------- lecture
    def _u32(self): return struct.unpack("<I", self.f.read(4))[0]
    def _u64(self): return struct.unpack("<Q", self.f.read(8))[0]
    def _str(self):
        n = self._u64()
        if n > 1 << 20:            # garde-fou : signe d'un désalignement
            raise ValueError(f"longueur de chaîne absurde ({n}) — flux désaligné")
        return self.f.read(n).decode("utf-8", "replace")

    def _value(self, vt: int):
        if vt == GGUF_STRING:  return self._str()
        if vt == GGUF_BOOL:    return bool(struct.unpack("<B", self.f.read(1))[0])  # 1 octet !
        if vt == GGUF_UINT8:   return struct.unpack("<B", self.f.read(1))[0]
        if vt == GGUF_INT8:    return struct.unpack("<b", self.f.read(1))[0]
        if vt == GGUF_UINT16:  return struct.unpack("<H", self.f.read(2))[0]
        if vt == GGUF_INT16:   return struct.unpack("<h", self.f.read(2))[0]
        if vt == GGUF_UINT32:  return self._u32()
        if vt == GGUF_INT32:   return struct.unpack("<i", self.f.read(4))[0]
        if vt == GGUF_FLOAT32: return struct.unpack("<f", self.f.read(4))[0]
        if vt == GGUF_UINT64:  return self._u64()
        if vt == GGUF_INT64:   return struct.unpack("<q", self.f.read(8))[0]
        if vt == GGUF_FLOAT64: return struct.unpack("<d", self.f.read(8))[0]
        if vt == GGUF_ARRAY:
            et = self._u32()
            n = self._u64()
            return [self._value(et) for _ in range(n)]
        raise ValueError(f"type de métadonnée inconnu : {vt}")

    # -------------------------------------------------------------- tenseurs
    def dequant(self, name: str) -> np.ndarray:
        """Retourne le tenseur en float32 (Q8_0/Q4_0 déquantifiés simplement)."""
        t = self.tensors[name]
        n = int(np.prod(t.shape))
        self.f.seek(self.data_start + t.offset)

        if t.ttype == GGML_F32:
            a = np.frombuffer(self.f.read(n * 4), dtype=np.float32).copy()
        elif t.ttype == GGML_F16:
            a = np.frombuffer(self.f.read(n * 2), dtype=np.float16).astype(np.float32)
        elif t.ttype in _BLOCK:
            bs, nb = _BLOCK[t.ttype]
            raw = self.f.read(n // bs * nb)
            if t.ttype == GGML_Q8_0:
                blk = np.frombuffer(raw, dtype=np.dtype([("d", "<f2"), ("q", "i1", bs)]))
                a = (blk["q"].astype(np.float32) * blk["d"].astype(np.float32)[:, None]).ravel()
            else:   # Q4_0 : 16 octets = 32 valeurs 4 bits, avec décalage de 8
                blk = np.frombuffer(raw, dtype=np.dtype([("d", "<f2"), ("qs", "u1", 16)]))
                lo = (blk["qs"] & 0x0F).astype(np.int16) - 8
                hi = (blk["qs"] >> 4).astype(np.int16) - 8
                # ggml : les bs/2 premiers niveaux viennent des nibbles BAS
                q = np.concatenate([lo, hi], axis=1)
                a = (q.astype(np.float32) * blk["d"].astype(np.float32)[:, None]).ravel()
        else:
            raise NotImplementedError(f"type ggml {t.ttype} non géré ({name})")
        return a.reshape(t.shape).astype(np.float32)

    def raw_levels(self, name: str) -> np.ndarray:
        """Niveaux entiers quantifiés AVANT mise à l'échelle (Q4_0 / Q8_0).

        C'est la valeur « telle que stockée » — celle que l'idée de répétition
        d'adresse cherche à éliminer.
        """
        t = self.tensors[name]
        if t.ttype not in _BLOCK:
            raise NotImplementedError("niveaux bruts : Q4_0/Q8_0 seulement")
        bs, nb = _BLOCK[t.ttype]
        n = int(np.prod(t.shape))
        self.f.seek(self.data_start + t.offset)
        raw = self.f.read(n // bs * nb)
        if t.ttype == GGML_Q8_0:
            blk = np.frombuffer(raw, dtype=np.dtype([("d", "<f2"), ("q", "i1", bs)]))
            q = blk["q"].astype(np.int16)
        else:
            blk = np.frombuffer(raw, dtype=np.dtype([("d", "<f2"), ("qs", "u1", bs // 2)]))
            lo = (blk["qs"] & 0x0F).astype(np.int16) - 8
            hi = (blk["qs"] >> 4).astype(np.int16) - 8
            q = np.concatenate([lo, hi], axis=1)
        return q.reshape(-1).reshape(t.shape).astype(np.int8)

    def arch(self) -> str:
        return str(self.meta.get("general.architecture", "?"))

    def cfg(self, key: str, default=None):
        return self.meta.get(f"{self.arch()}.{key}", default)

    def close(self):
        self.f.close()
