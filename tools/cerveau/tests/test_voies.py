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

if _TORCH:
    from cerveau.voies import Voies, entrainer, evaluer, evaluer_champs
from semantique.typed_corpus import ItemType


if _TORCH:
    class _Base(nn.Module):
        """Encodeur minimal : assez pour tester les formes, pas pour apprendre."""

        def __init__(self, d: int = 16, vocab: int = 256):
            super().__init__()
            self.config = SimpleNamespace(hidden_size=d)
            self.emb = nn.Embedding(vocab, d)

        def forward(self, input_ids, attention_mask, output_hidden_states=True):
            h = self.emb(input_ids)
            return SimpleNamespace(hidden_states=[h, h])
else:
    _Base = object


def _items():
    base = {"jeu": "echecs", "action": "deplacer", "de": None, "vers": None,
            "point": None, "chemin_0": None}
    return [
        ItemType("e2e4", {**base, "de": 52, "vers": 36}, "echecs", "coup",
                 "notation", "p1", "synthetique", "echecs depart"),
        ItemType("g1f3", {**base, "de": 62, "vers": 45}, "echecs", "coup",
                 "notation", "p2", "synthetique", "echecs depart"),
        ItemType("D4", {**base, "action": "poser", "point": 48}, "go", "coup",
                 "notation", "p3", "synthetique", "go depart"),
        ItemType("b6 c5", {**base, "chemin_0": 8}, "dames", "coup",
                 "notation", "p4", "synthetique", "dames depart"),
    ]


@unittest.skipUnless(_TORCH, "torch absent du python courant")
class TestVoies(unittest.TestCase):
    def test_formes_des_tetes(self):
        m = Voies(_Base(16), champs_dorsaux=("de", "vers", "point"),
                  pool="mean+last", contexte=True)
        ids = torch.tensor([[65, 66, 67], [68, 69, 70]])
        masque = torch.ones_like(ids)
        cids = torch.tensor([[97, 98, 99], [100, 101, 102]])
        cmasque = torch.ones_like(cids)
        va, vd = m.logits(ids, masque, cids, cmasque)
        self.assertEqual(tuple(va.shape), (2, 8))
        self.assertEqual(tuple(vd["de"].shape), (2, 65))
        self.assertEqual(tuple(vd["vers"].shape), (2, 65))
        self.assertEqual(tuple(vd["point"].shape), (2, 82))
        self.assertEqual(m.dim_entree, 16 * 2 * 2)
        self.assertIs(m.dorsal, m.dorsaux["de"])

    def test_pools(self):
        m = Voies(_Base(16), champs_dorsaux=("de",), pool="mean")
        self.assertEqual(m.dim_entree, 16)
        m = Voies(_Base(16), champs_dorsaux=("de",), pool="last")
        self.assertEqual(m.dim_entree, 16)
        m = Voies(_Base(16), champs_dorsaux=("de",), pool="mean+last",
                  contexte=True)
        self.assertEqual(m.dim_entree, 16 * 2 * 2)

    def test_le_contexte_change_le_code(self):
        m = Voies(_Base(16), champs_dorsaux=("de",), pool="mean+last",
                  contexte=True).eval()
        ids = torch.tensor([[65, 66, 67]])
        masque = torch.ones_like(ids)
        c1 = torch.tensor([[97, 98, 99]])
        c2 = torch.tensor([[100, 101, 102]])
        z1 = m.encode(ids, masque, c1, masque)
        z2 = m.encode(ids, masque, c2, masque)
        self.assertFalse(torch.allclose(z1, z2))

    def test_evaluation_et_lesions(self):
        m = Voies(_Base(16), champs_dorsaux=("de", "vers", "point", "chemin_0"),
                  pool="mean+last", contexte=False).eval()
        its = _items()
        r = evaluer_champs(m, its, champs=("de", "vers", "point", "chemin_0"),
                           device="cpu", lesions=True, retour_pred=True)
        self.assertEqual(r["de"]["n"], 2)
        self.assertEqual(r["vers"]["n"], 2)
        self.assertEqual(r["point"]["n"], 1)
        self.assertEqual(r["chemin_0"]["n"], 1)
        self.assertIn("ventrale", r["de"]["lesions"])
        self.assertIn("dorsale", r["de"]["lesions"])
        self.assertEqual(r["action_global"]["n"], 4)
        self.assertEqual(len(r["de"]["ok"]), 2)
        # API historique : un seul champ, sortie plate
        legacy = evaluer(m, its, device="cpu", champ="de")
        self.assertEqual(legacy["n"], 2)
        self.assertIn("action", legacy)
        self.assertIn("de", legacy)

    def test_contexte_melange_et_vide(self):
        m = Voies(_Base(16), champs_dorsaux=("de",), pool="mean+last",
                  contexte=True).eval()
        its = _items()
        for mode in ("melange", "vide"):
            r = evaluer_champs(m, its, champs=("de",), device="cpu",
                               lesions=False, contexte_mode=mode,
                               retour_pred=False)
            self.assertEqual(r["de"]["n"], 2)

    def test_entrainement_court(self):
        base = _Base(8)
        m, val = entrainer(base, pas=1, lot=2, seq=16, graine=1, device="cpu",
                           synth=True, champs=("de", "vers"))
        self.assertEqual(tuple(m.champs_dorsaux), ("de", "vers"))
        self.assertIn("de", m.dorsaux)
        self.assertIn("vers", m.dorsaux)
        self.assertEqual(m.dim_entree, 8 * 2)
        self.assertGreater(len(val), 0)


if __name__ == "__main__":
    unittest.main()
