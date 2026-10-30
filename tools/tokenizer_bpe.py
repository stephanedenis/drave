#!/usr/bin/env python3
"""tokenizer_bpe.py — R13.1 : entraîne un BPE byte-level et tokenise un corpus.

Sortie : le tokenizer (JSON), les identifiants BPE (.pt) et les identifiants
octets (.pt), plus un JSON de stats (vocab, octets, jetons, octets/jeton,
réversibilité). Aucun modèle n'est entraîné ici.
"""
from __future__ import annotations

import argparse
import json
import pathlib

import torch
from tokenizers import Tokenizer, decoders, models, pre_tokenizers, trainers


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="data/corpus_fr.txt")
    ap.add_argument("--vocab", type=int, default=512)
    ap.add_argument("--tokenizer", default="", help="tokenizer existant (sinon entraîné)")
    ap.add_argument("--sortie-tokenizer", required=True)
    ap.add_argument("--sortie-ids", required=True)
    ap.add_argument("--sortie-octets", required=True)
    ap.add_argument("--stats", required=True)
    a = ap.parse_args()
    texte = pathlib.Path(a.corpus).read_text(errors="replace")
    if a.tokenizer:
        tok = Tokenizer.from_file(a.tokenizer)
    else:
        tok = Tokenizer(models.BPE(unk_token=None))
        tok.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
        tok.decoder = decoders.ByteLevel()
        ent = trainers.BpeTrainer(vocab_size=a.vocab, special_tokens=[],
                                  initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
                                  show_progress=False)
        tok.train_from_iterator([texte], ent)
        tok.save(a.sortie_tokenizer)
    enc = tok.encode(texte)
    ids = torch.tensor(enc.ids, dtype=torch.long)
    torch.save(ids, a.sortie_ids)
    octets = texte.encode()
    torch.save(torch.tensor(list(octets), dtype=torch.long), a.sortie_octets)
    stats = {
        "corpus": a.corpus, "vocab": tok.get_vocab_size(),
        "octets": len(octets), "jetons": len(enc.ids),
        "octets_par_jeton": len(octets) / len(enc.ids),
        "reversible": tok.decode(enc.ids) == texte,
        "tokenizer": a.sortie_tokenizer,
    }
    pathlib.Path(a.stats).write_text(json.dumps(stats, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps(stats, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
