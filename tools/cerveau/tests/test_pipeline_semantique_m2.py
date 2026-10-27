from __future__ import annotations

import unittest
from types import SimpleNamespace

try:
    import torch
    import torch.nn as nn
    _TORCH = True
except ImportError:
    torch = None
    nn = None
    _TORCH = False

from jeux.regles import echecs as E
from jeux.rsn import RSN
from semantique.universaux import CHAMPS, code_rsn

if _TORCH:
    from cerveau.hub import Hub
    from cerveau.pipeline_semantique_m2 import (
        CHAMPS_DORSAUX,
        PipelineSemantiqueM2,
        code_vide,
        contexte_depuis_resume,
    )
    from cerveau.sequences import Pas, Sequence, corpus
    from cerveau.voies import VALEURS, Voies
    from semantique.typed_corpus import items as corpus_items


if _TORCH:
    class _Base(nn.Module):
        """Encodeur minimal : les formes suffisent, pas l'apprentissage."""

        def __init__(self, d: int = 16, vocab: int = 256):
            super().__init__()
            self.config = SimpleNamespace(hidden_size=d)
            self.emb = nn.Embedding(vocab, d)

        def forward(self, input_ids, attention_mask,
                    output_hidden_states=True):
            h = self.emb(input_ids)
            return SimpleNamespace(hidden_states=[h, h])


@unittest.skipUnless(_TORCH, "torch absent du python courant")
class TestPipelineSemantiqueM2(unittest.TestCase):
    def test_m1_percoit_et_stocke(self):
        p = PipelineSemantiqueM2(voies=None, device="cpu")
        ctx = E.rsn_depuis_position(E.Position.depart())
        code = p.percevoir("Nf3", "echecs", ctx)
        self.assertEqual(code["de"], 62)
        self.assertEqual(code["vers"], 45)
        self.assertEqual(len(p.memoire.episodes), 1)

    def test_coder_voies_sans_modele(self):
        p = PipelineSemantiqueM2(voies=None, device="cpu")
        self.assertIsNone(p.coder_voies("e2e4", "echecs"))
        with self.assertRaises(ValueError):
            p.lesionner_m2([])

    def test_coder_voies_faux_modele(self):
        m = Voies(_Base(16), champs_dorsaux=CHAMPS_DORSAUX,
                  pool="mean+last", contexte=False)
        p = PipelineSemantiqueM2(voies=m, device="cpu")
        code = p.coder_voies("e2e4", "echecs")
        self.assertEqual(set(code), {"action", "de", "vers"})
        self.assertIn(code["action"], VALEURS["action"])
        self.assertIn(code["de"], VALEURS["de"])
        self.assertIn(code["vers"], VALEURS["vers"])

    def test_coder_voies_avec_contexte(self):
        m = Voies(_Base(16), champs_dorsaux=CHAMPS_DORSAUX,
                  pool="mean+last", contexte=True)
        p = PipelineSemantiqueM2(voies=m, device="cpu")
        ctx = E.rsn_depuis_position(E.Position.depart())
        a = p.coder_voies("Nf3", "echecs", ctx)
        b = p.coder_voies("Nf3", "echecs", "echecs etat trait=w")
        self.assertEqual(set(a), {"action", "de", "vers"})
        self.assertEqual(set(b), {"action", "de", "vers"})

    def test_etape_rend_les_deux_lectures(self):
        m = Voies(_Base(16), champs_dorsaux=CHAMPS_DORSAUX,
                  pool="mean+last", contexte=False)
        p = PipelineSemantiqueM2(voies=m, device="cpu")
        ctx = E.rsn_depuis_position(E.Position.depart())
        r = p.etape("Nf3", "echecs", ctx)
        self.assertEqual(set(r), {"M1", "M2"})
        self.assertEqual(r["M1"]["de"], 62)
        self.assertEqual(set(r["M2"]), {"action", "de", "vers"})

    def test_contexte_depuis_resume_les_quatre_jeux(self):
        hub = Hub()
        for seq in corpus(0, 1, 2):
            for pas in seq.pas:
                ctx = contexte_depuis_resume(pas.contexte, pas.jeu)
                self.assertIsNotNone(ctx, pas.jeu)
                self.assertEqual(hub.percevoir(pas.surface, pas.jeu, ctx),
                                 pas.code,
                                 f"{seq.jeu} {pas.surface}")

    def test_code_vide(self):
        c = code_vide("go")
        self.assertEqual(c["jeu"], "go")
        for nom, _ in CHAMPS:
            if nom != "jeu":
                self.assertIsNone(c[nom])

    def test_lesionner_m1(self):
        p = PipelineSemantiqueM2(voies=None, device="cpu")
        items = [i for i in corpus_items() if i.code.get("de") is not None][:10]
        r = p.lesionner_m1(items)
        self.assertEqual(r["n"], 10)
        self.assertEqual(r["de"]["n"], 10)
        self.assertGreaterEqual(r["code_exact"], 0.0)
        self.assertLessEqual(r["code_exact"], 1.0)

    def test_lesionner_m2(self):
        m = Voies(_Base(16), champs_dorsaux=CHAMPS_DORSAUX,
                  pool="mean+last", contexte=False)
        p = PipelineSemantiqueM2(voies=m, device="cpu")
        items = [i for i in corpus_items()
                 if i.code.get("de") is not None][:8]
        r = p.lesionner_m2(items)
        for nom in CHAMPS_DORSAUX:
            self.assertEqual(r[nom]["n"], len(items))
            self.assertIn("ventrale", r[nom]["lesions"])
            self.assertIn("dorsale", r[nom]["lesions"])

    def test_lesionner_m5(self):
        def pas(de, vers):
            r = RSN("echecs", "coup", {"de": de, "vers": vers})
            return Pas("echecs", code_rsn(r), "", "", r)

        seq = Sequence("echecs", (pas(52, 36), pas(45, 45), pas(36, 28)))
        p = PipelineSemantiqueM2(voies=None, device="cpu")
        r = p.lesionner_m5([seq], [seq])
        for nom in ("avec_plateau", "sans_plateau", "sans_transitions"):
            self.assertIn(nom, r)
            self.assertIn("exact", r[nom])

    def test_selectionner(self):
        p = PipelineSemantiqueM2(voies=None, device="cpu")
        r = p.selectionner()
        self.assertEqual(r["n"], 88)
        self.assertGreater(r["exact"], 0.9)


if __name__ == "__main__":
    unittest.main()
