from __future__ import annotations

import pathlib
import struct
import sys
import unittest

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from tools.couche_distante import (  # noqa: E402
    ENTETE_REQ,
    ENTETE_RESP,
    MAGIC_REQ,
    OP_FORWARD,
    VERSION,
    bits_masque,
    decoder_flux,
    encoder_flux,
    fidelite_np,
    intersection_topk,
    kl_divergence_np,
    lire_entete,
    perplexite_np,
    recevoir_exact,
    statistiques,
)


class _SocketFactice:
    """Socket minimal pour tester le framing sans réseau."""

    def __init__(self, morceaux: list[bytes]):
        self.morceaux = list(morceaux)

    def recv(self, n: int) -> bytes:
        if not self.morceaux:
            return b""
        morceau = self.morceaux[0]
        if len(morceau) <= n:
            return self.morceaux.pop(0)
        self.morceaux[0] = morceau[n:]
        return morceau[:n]


class TestEntetes(unittest.TestCase):
    def test_tailles(self):
        self.assertEqual(ENTETE_REQ.size, 38)
        self.assertEqual(ENTETE_RESP.size, 34)

    def test_bits_masque(self):
        self.assertEqual(bits_masque(0), 0)
        self.assertEqual(bits_masque(1), 1)
        self.assertEqual(bits_masque(7), 1)
        self.assertEqual(bits_masque(8), 1)
        self.assertEqual(bits_masque(9), 2)
        self.assertEqual(bits_masque(16128), 2016)

    def test_recevoir_exact_morceaux(self):
        sock = _SocketFactice([b"ab", b"cde", b"f"])
        self.assertEqual(recevoir_exact(sock, 6), b"abcdef")

    def test_recevoir_exact_eof(self):
        with self.assertRaises(EOFError):
            recevoir_exact(_SocketFactice([b"ab"]), 3)

    def test_lire_entete(self):
        brut = ENTETE_REQ.pack(
            MAGIC_REQ, VERSION, OP_FORWARD, 0, 0, 0, 2, 4, 8, 16, 32, 32, 0
        )
        champs = lire_entete(_SocketFactice([brut]), ENTETE_REQ, MAGIC_REQ)
        self.assertEqual(champs[2], OP_FORWARD)
        self.assertEqual(champs[6], 2)
        self.assertEqual(champs[7], 4)

    def test_lire_entete_mauvais_magic(self):
        brut = ENTETE_REQ.pack(
            b"NOPE", VERSION, OP_FORWARD, 0, 0, 0, 2, 4, 8, 16, 32, 32, 0
        )
        with self.assertRaises(ValueError):
            lire_entete(_SocketFactice([brut]), ENTETE_REQ, MAGIC_REQ)


class TestFlux(unittest.TestCase):
    def test_dense_aller_retour(self):
        rng = np.random.default_rng(0)
        x = rng.normal(size=(3, 8)).astype(np.float32)
        x[0, 0] = 0.0
        payload, meta = encoder_flux(x)
        y = decoder_flux(payload, 3, 8, sparse=False)
        np.testing.assert_array_equal(x, y)
        self.assertEqual(meta["nval"], 24)
        self.assertEqual(len(payload), 3 * 8 * 4)

    def test_sparse_aller_retour(self):
        x = np.zeros((4, 8), dtype=np.float32)
        x[0, 1] = 1.5
        x[3, 7] = -2.25
        payload, meta = encoder_flux(x, sparse=True)
        y = decoder_flux(payload, 4, 8, sparse=True)
        np.testing.assert_array_equal(x, y)
        self.assertEqual(meta["nval"], 2)
        self.assertEqual(meta["nmask"], 4)
        self.assertLess(len(payload), 4 * 8 * 4)

    def test_sparse_moins_efficace_si_dense(self):
        x = np.ones((2, 8), dtype=np.float32)
        payload_sparse, _ = encoder_flux(x, sparse=True)
        payload_dense, _ = encoder_flux(x)
        self.assertGreater(len(payload_sparse), len(payload_dense))

    def test_sparse_gagne_avec_des_zeros(self):
        x = np.zeros((2, 64), dtype=np.float32)
        x[:, :4] = 1.0  # 93,75 % de zéros
        payload_sparse, _ = encoder_flux(x, sparse=True)
        payload_dense, _ = encoder_flux(x)
        self.assertLess(len(payload_sparse), len(payload_dense))

    def test_zero_signe_normalise(self):
        x = np.array([[0.0, -0.0, 1.5]], dtype=np.float32)
        payload, _ = encoder_flux(x, sparse=True)
        y = decoder_flux(payload, 1, 3, sparse=True)
        np.testing.assert_array_equal(x, y)  # -0.0 == +0.0 en valeur
        self.assertTrue(np.signbit(x[0, 1]))
        self.assertFalse(np.signbit(y[0, 1]))

    def test_liste_python(self):
        payload, meta = encoder_flux([[1.0, 0.0], [0.0, 2.0]])
        y = decoder_flux(payload, meta["ntok"], meta["h"])
        np.testing.assert_array_equal(y, np.array([[1.0, 0.0], [0.0, 2.0]], np.float32))

    def test_forme_invalide(self):
        with self.assertRaises(ValueError):
            encoder_flux(np.zeros(4, dtype=np.float32))

    def test_dense_tronque(self):
        payload, meta = encoder_flux(np.ones((2, 4), dtype=np.float32))
        with self.assertRaises(ValueError):
            decoder_flux(payload[:-4], meta["ntok"], meta["h"])

    def test_sparse_tronque(self):
        x = np.zeros((2, 16), dtype=np.float32)
        x[0, 0] = 1.0
        payload, meta = encoder_flux(x, sparse=True)
        with self.assertRaises(ValueError):
            decoder_flux(payload[:-4], meta["ntok"], meta["h"], sparse=True)

    def test_sparse_masque_incoherent(self):
        x = np.zeros((1, 8), dtype=np.float32)
        x[0, 0] = 1.0
        payload, _ = encoder_flux(x, sparse=True)
        # On retire les valeurs : le masque annonce 1 bit, il n'y a plus de valeur.
        masque = payload[:1]
        with self.assertRaises(ValueError):
            decoder_flux(masque, 1, 8, sparse=True)


class TestMetriques(unittest.TestCase):
    def test_perplexite_uniforme(self):
        logits = np.zeros((2, 2), dtype=np.float32)
        res = perplexite_np(logits, np.array([0, 1]))
        self.assertAlmostEqual(res["perplexite"], 2.0, places=12)
        self.assertAlmostEqual(res["nll_moyenne"], np.log(2.0), places=12)
        self.assertEqual(res["ntok"], 2)

    def test_perplexite_cible_invalide(self):
        with self.assertRaises(ValueError):
            perplexite_np(np.zeros((1, 2), dtype=np.float32), np.array([2]))

    def test_fidelite_identique(self):
        ref = np.array([[2.0, 0.0], [0.0, 2.0]], dtype=np.float32)
        res = fidelite_np(ref, ref.copy())
        self.assertTrue(res["bits_identiques"])
        self.assertTrue(res["valeurs_identiques"])
        self.assertEqual(res["diff_max"], 0.0)
        self.assertEqual(res["argmax_accord"], 1.0)
        self.assertEqual(res["top5_intersection"], 1.0)
        self.assertEqual(res["top1024_intersection"], 1.0)  # k borné à V
        self.assertEqual(res["kl_moyenne"], 0.0)

    def test_fidelite_perturbee(self):
        ref = np.zeros((2, 16), dtype=np.float32)
        ref[0, :5] = [16.0, 15.0, 14.0, 13.0, 12.0]
        ref[1, 0] = 2.0
        split = ref.copy()
        split[0, :5] = 0.0
        split[0, 5:10] = [16.0, 15.0, 14.0, 13.0, 12.0]
        res = fidelite_np(ref, split)
        self.assertFalse(res["bits_identiques"])
        self.assertFalse(res["valeurs_identiques"])
        self.assertAlmostEqual(res["diff_max"], 16.0)
        self.assertAlmostEqual(res["argmax_accord"], 0.5)
        # k=5 : la ligne 0 a des top-5 disjoints, la ligne 1 identique.
        self.assertAlmostEqual(res["top5_intersection"], 0.5)
        self.assertGreater(res["kl_moyenne"], 0.0)

    def test_kl_identiques(self):
        p = np.array([[1.0, 2.0, 3.0], [3.0, 2.0, 1.0]], dtype=np.float32)
        self.assertAlmostEqual(kl_divergence_np(p, p.copy()), 0.0, places=12)
        self.assertAlmostEqual(kl_divergence_np(p, p + 5.0), 0.0, places=12)

    def test_kl_differentes(self):
        p = np.array([[10.0, 0.0, 0.0]], dtype=np.float32)
        q = np.array([[0.0, 10.0, 0.0]], dtype=np.float32)
        self.assertGreater(kl_divergence_np(p, q), 1.0)

    def test_intersection_topk(self):
        a = np.array([[3.0, 2.0, 1.0]], dtype=np.float32)
        self.assertEqual(intersection_topk(a, a.copy(), 1), 1.0)
        b = np.array([[1.0, 2.0, 3.0]], dtype=np.float32)
        self.assertEqual(intersection_topk(a, b, 1), 0.0)
        self.assertAlmostEqual(intersection_topk(a, b, 3), 1.0)

    def test_statistiques(self):
        res = statistiques([4.0, 1.0, 2.0, 3.0])
        self.assertEqual(res["n"], 4)
        self.assertEqual(res["min"], 1.0)
        self.assertEqual(res["max"], 4.0)
        self.assertEqual(res["mediane"], 2.5)
        self.assertEqual(res["moyenne"], 2.5)
        self.assertIsNone(statistiques([]))


if __name__ == "__main__":
    unittest.main()
