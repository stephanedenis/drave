"""Tests du bloc linguistique — contrat, substitution, parallèle, cascade, activation."""
import json
import pathlib
import stat
import sys
import tempfile
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl

TEXTE = "Le chat de la voisine qui dort sur le toit se réveille. Va voir le chat !"


class TestBlocLinguistique(unittest.TestCase):
    def setUp(self):
        self.h = bl.Heuristique(segmenter_s=False)
        self.n = bl.MockNeuronal()

    def test_niveaux_et_spans(self):
        a = self.h.analyser(TEXTE, "fr")
        niveaux = {e.niveau for e in a.etiquettes}
        self.assertEqual(set(bl.NIVEAUX) - niveaux, set(), f"niveaux manquants : {set(bl.NIVEAUX)-niveaux}")
        for e in a.etiquettes:
            self.assertGreaterEqual(e.debut, 0)
            self.assertLessEqual(e.fin, len(TEXTE))
            self.assertLessEqual(e.debut, e.fin)

    def test_langue_et_script(self):
        for texte, langue in (("Le chat dort dans la maison.", "fr"),
                              ("The cat sleeps in the house.", "en"),
                              ("Die Katze schläft im Haus.", "de"),
                              ("El gato duerme en la casa.", "es"),
                              ("Il gatto dorme in casa.", "it")):
            lg, conf, _ = bl.detecter_langue(texte)
            self.assertEqual(lg, langue)
            self.assertGreater(conf, 0)
        self.assertEqual(bl.detecter_script("Привет мир"), "Cyrl")
        self.assertEqual(bl.detecter_script("مرحبا بالعالم"), "Arab")
        self.assertEqual(bl.detecter_script("नमस्ते दुनिया"), "Deva")
        self.assertEqual(bl.detecter_script("你好世界"), "Hani")

    def test_substitution(self):
        a = self.h.analyser(TEXTE, "fr")
        b = self.n.analyser(TEXTE, "fr")
        self.assertEqual(set(a.json()), set(b.json()))
        self.assertEqual(a.source, "heuristique")
        self.assertEqual(b.source, "neuronal")
        self.assertIn("heuristique", {e.source for e in a.etiquettes})
        self.assertIn("neuronal", {e.source for e in b.etiquettes})

    def test_parallele(self):
        p = bl.Parallele([self.h, self.n]).analyser(TEXTE, "fr")
        sources = {e.source for e in p.etiquettes}
        self.assertEqual(sources, {"heuristique", "neuronal"})
        self.assertEqual(p.source, "parallele")
        # le syntagme heuristique (le générateur S) n'est pas écrasé par le mock
        syn = [e for e in p.etiquettes if e.niveau == "syntagme"]
        self.assertTrue(any(e.source == "heuristique" for e in syn))

    def test_cascade(self):
        c = bl.Cascade(self.h, self.n, seuil=0.9)
        a = c.analyser(TEXTE, "fr")
        self.assertGreaterEqual(c.appels_neuronal, 1)
        self.assertEqual(a.source, "cascade")
        etapes = [t for t in a.trace if t.get("etape") == "cascade"]
        self.assertTrue(etapes)
        self.assertTrue(etapes[-1]["residuel"])

    def test_activation_semantique(self):
        a = self.h.analyser(TEXTE, "fr")
        sem = bl.CoucheSemantique()
        r = sem.activer(a)
        self.assertLess(r["fraction"], 1.0)
        self.assertGreater(r["unites"], 0)
        self.assertLess(r["cout"], len(TEXTE))

    def test_refus(self):
        self.assertEqual(self.h.analyser("").refus, "vide")
        self.assertEqual(self.h.analyser("... !!! ???").refus, "vide")
        self.assertEqual(self.h.analyser("qqqqq zzzzz wwwww").langue, "und")

    def test_rejeu(self):
        self.assertEqual(self.h.analyser(TEXTE, "fr").json(),
                         self.h.analyser(TEXTE, "fr").json())

    def test_adaptateur_neuronal_avec_faux_modele(self):
        d = pathlib.Path(tempfile.mkdtemp())
        faux = d / "faux_llama.py"
        faux.write_text(
            "#!/usr/bin/env python3\nimport json\n"
            "print(json.dumps({'langue':'fr','script':'Latn','etiquettes':["
            "{'niveau':'phrase','type':'type','valeur':'déclarative','debut':0,'fin':4,'confiance':0.9},"
            "{'niveau':'pragmatique','type':'acte','valeur':'assertion','debut':0,'fin':4,'confiance':0.8}]}))\n",
            encoding="utf-8")
        faux.chmod(faux.stat().st_mode | stat.S_IEXEC)
        modele = pathlib.Path(__file__).resolve()
        n = bl.NeuronalLLM(modele, llama_cli=str(faux), timeout=10)
        a = n.analyser("Le chat dort.", "fr")
        self.assertEqual(a.source, "neuronal")
        self.assertEqual(a.langue, "fra")
        self.assertEqual({e.niveau for e in a.etiquettes}, {"phrase", "pragmatique"})

    def test_tagger_neuronal_pos_avec_faux_transport(self):
        appels = []

        def transport(invite, grammaire, max_jetons):
            appels.append((invite, grammaire, max_jetons))
            return '{"pos":["DET","NOUN","VERB"]}'

        n = bl.NeuronalLLMPOS("faux-modele", transport=transport)
        a = n.analyser("Le chat dort.", "fr")
        self.assertEqual(a.source, "neuronal")
        self.assertEqual([(e.debut, e.fin, e.type) for e in a.etiquettes],
                         [(0, 2, "DET"), (3, 7, "NOUN"), (8, 12, "VERB")])
        self.assertEqual(n.appels, 1)
        self.assertIn('"pos"', appels[0][0])
        self.assertIn("tag", appels[0][1])
        b = n.analyser("Le chat dort.", "fr")
        self.assertEqual(n.appels, 1, "le cache doit éviter le second appel")
        self.assertEqual(a.json(), b.json())

    def test_tagger_neuronal_pos_refus(self):
        n = bl.NeuronalLLMPOS("faux-modele", transport=lambda *_: "pas de json")
        a = n.analyser("Le chat dort.", "fr")
        self.assertTrue(a.refus)
        self.assertEqual(a.etiquettes, [])
        self.assertEqual(a.source, "neuronal")

    def test_tagger_neuronal_chunks_avec_faux_transport(self):
        def transport(invite, grammaire, max_jetons):
            return '{"bio":["B-GN","I-GN","B-GV"]}'

        n = bl.NeuronalLLMChunks("faux-modele", transport=transport)
        a = n.analyser("Le chat dort.", "fr")
        self.assertEqual(a.source, "neuronal")
        self.assertEqual([(e.type, e.debut, e.fin) for e in a.etiquettes],
                         [("GN", 0, 7), ("GV", 8, 12)])
        self.assertEqual(n.appels, 1)
        b = n.analyser("Le chat dort.", "fr")
        self.assertEqual(n.appels, 1, "le cache doit éviter le second appel")
        self.assertEqual(a.json(), b.json())

    def test_tagger_neuronal_chunks_refus(self):
        n = bl.NeuronalLLMChunks("faux-modele", transport=lambda *_: '{"bio":["B-GN"]}')
        a = n.analyser("Le chat dort.", "fr")
        self.assertTrue(a.refus)
        self.assertEqual(a.etiquettes, [])

    def test_tagger_neuronal_pragmatique(self):
        def transport(*_):
            return '{"acte":"question","negation":true,"modalite":false,"double_sens":false}'

        n = bl.NeuronalLLMPragmatique("faux-modele", transport=transport)
        a = n.analyser("Viens-tu ?", "fr")
        etiquettes = {(e.niveau, e.type): e.valeur for e in a.etiquettes}
        self.assertEqual(etiquettes[("pragmatique", "acte")], "question")
        self.assertIn(("phrase", "négation"), etiquettes)
        self.assertNotIn(("phrase", "modalité"), etiquettes)
        self.assertNotIn(("pragmatique", "double_sens"), etiquettes)
        self.assertEqual(n.appels, 1)
        n.analyser("Viens-tu ?", "fr")
        self.assertEqual(n.appels, 1, "le cache doit éviter le second appel")

    def test_priorite_syntagme_confiance(self):
        defaut = bl.Parallele([bl.Heuristique(), bl.MockNeuronal()]).analyser(TEXTE, "fr")
        confiance = bl.Parallele([bl.Heuristique(), bl.MockNeuronal()],
                                 priorite_syntagme="confiance").analyser(TEXTE, "fr")
        n_defaut = sum(1 for e in defaut.etiquettes
                       if e.niveau == "syntagme" and e.source == "neuronal")
        n_confiance = sum(1 for e in confiance.etiquettes
                          if e.niveau == "syntagme" and e.source == "neuronal")
        self.assertGreater(n_confiance, n_defaut)

    def test_compose_pos_et_syntagmes(self):
        pos = bl.NeuronalLLMPOS("faux-modele",
                                transport=lambda *_: '{"pos":["DET","NOUN","VERB"]}')
        chunks = bl.NeuronalLLMChunks("faux-modele",
                                      transport=lambda *_: '{"bio":["B-GN","I-GN","B-GV"]}')
        compose = bl.NeuronalLLMCompose(pos, chunks)
        a = compose.analyser("Le chat dort.", "fr")
        self.assertEqual({e.niveau for e in a.etiquettes}, {"pos", "syntagme"})
        self.assertEqual({e.source for e in a.etiquettes}, {"neuronal"})
        self.assertEqual(a.refus, "")
        self.assertEqual(pos.appels, 1)
        self.assertEqual(chunks.appels, 1)


if __name__ == "__main__":
    unittest.main()
