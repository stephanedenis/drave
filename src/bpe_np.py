"""
Qtrinet — tokenizer BPE byte-level minimal, reconstruit depuis les métadonnées GGUF.

Aucune dépendance. Suffisant pour mesurer une perplexité sur WikiText-2.
"""

from __future__ import annotations

import re
from functools import lru_cache

# découpage GPT-2 (approximation fidèle de la regex utilisée par llama.cpp)
# Équivalent stdlib de la regex GPT-2/llama.cpp (qui utilise \p{L} et \p{N},
# non supportés par le module `re` de Python) :
#   \p{L}+  →  [^\W\d_]+      (lettres Unicode)
#   \p{N}+  →  \d+             (chiffres Unicode)
_SPLIT = re.compile(
    r"'s|'t|'re|'ve|'m|'ll|'d| ?[^\W\d_]+| ?\d+| ?[^\s\w]+|\s+(?!\S)|\s+"
)


def _bytes_to_unicode() -> dict[int, str]:
    bs = (list(range(ord("!"), ord("~") + 1)) + list(range(ord("¡"), ord("¬") + 1))
          + list(range(ord("®"), ord("ÿ") + 1)))
    cs = bs[:]
    n = 0
    for b in range(256):
        if b not in bs:
            bs.append(b)
            cs.append(256 + n)
            n += 1
    return dict(zip(bs, [chr(c) for c in cs]))


class BPETokenizer:
    def __init__(self, tokens: list[str], merges: list[str], add_bos: int | None = None,
                 add_eos: int | None = None):
        self.id_to_tok = tokens
        self.tok_to_id = {t: i for i, t in enumerate(tokens)}
        self.ranks: dict[tuple[str, str], int] = {}
        for i, m in enumerate(merges):
            a, _, b = m.partition(" ")
            self.ranks[(a, b)] = i
        self.byte_enc = _bytes_to_unicode()
        self.bos, self.eos = add_bos, add_eos
        # cache : les mêmes mots reviennent en masse dans un corpus
        self._cache: dict[str, list[int]] = {}

    def _bpe(self, word: str) -> list[int]:
        cached = self._cache.get(word)
        if cached is not None:
            return cached
        syms = list(word)
        while len(syms) > 1:
            best, best_rank = None, None
            for i in range(len(syms) - 1):
                r = self.ranks.get((syms[i], syms[i + 1]))
                if r is not None and (best_rank is None or r < best_rank):
                    best, best_rank = i, r
            if best is None:
                break
            syms = syms[:best] + [syms[best] + syms[best + 1]] + syms[best + 2:]
        ids = [self.tok_to_id[s] for s in syms if s in self.tok_to_id]
        self._cache[word] = ids
        return ids

    def encode(self, text: str) -> list[int]:
        out: list[int] = []
        for piece in _SPLIT.findall(text):
            w = "".join(self.byte_enc[b] for b in piece.encode("utf-8"))
            out.extend(self._bpe(w))
        return out

    def decode(self, ids: list[int]) -> str:
        s = "".join(self.id_to_tok[i] for i in ids)
        inv = {v: k for k, v in self.byte_enc.items()}
        return bytes(inv[c] for c in s if c in inv).decode("utf-8", "replace")

    @classmethod
    def from_gguf(cls, g) -> "BPETokenizer":
        toks = g.meta["tokenizer.ggml.tokens"]
        merges = g.meta.get("tokenizer.ggml.merges", [])
        bos = g.meta.get("tokenizer.ggml.bos_token_id")
        eos = g.meta.get("tokenizer.ggml.eos_token_id")
        return cls(toks, merges, bos, eos)
