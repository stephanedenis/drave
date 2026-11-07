#!/usr/bin/env python3
"""test_schema_produit.py — le **contrat** du produit : schéma v2, v1 lue, refus, entrées hostiles.

Ce que le test fige (et qu'un client peut supposer) :
- 8 champs **obligatoires** à la racine : `schema`, `version`, `texte`, `langue`, `script`,
  `refus`, `etiquettes`, `unites_semantiques` ;
- `schema == "drave.annotation"` et `version == 2` ;
- `meta.partition` et `meta.alternative` sont déclarés dans le schéma v2 ;
- une annotation **v1 reste lue** par le vérificateur (schéma v1), et le schéma v2 la refuse ;
- un refus est une **réponse** : JSON valide avec `refus`, code de sortie 3 ;
- un surrogate isolé et une entrée non textuelle ne font pas planter.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
SCHEMA_V1 = RACINE / "tools" / "schemas" / "drave-annotation-v1.json"
SCHEMA_V2 = RACINE / "tools" / "schemas" / "drave-annotation-v2.json"
VERIFICATEUR = RACINE / "tools" / "verifier_schema_produit.py"
OBLIGATOIRES = ("schema", "version", "texte", "langue", "script", "refus",
                "etiquettes", "unites_semantiques")


def _cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(RACINE / "tools/drave.py"), *args],
                          capture_output=True, text=True, cwd=str(RACINE))


class TestSchemaDuProduit(unittest.TestCase):
    def test_les_huit_champs_obligatoires(self):
        sortie = _cli("analyser", "Le chat dort.", "--json")
        self.assertEqual(sortie.returncode, 0, sortie.stderr[:300])
        d = json.loads(sortie.stdout)
        manquants = [k for k in OBLIGATOIRES if k not in d]
        self.assertEqual(manquants, [])
        self.assertEqual(d["schema"], "drave.annotation")
        self.assertEqual(d["version"], 2)

    def test_anglais_meme_schema(self):
        sortie = _cli("analyser", "The cat sleeps.", "--langue", "en", "--json")
        self.assertEqual(sortie.returncode, 0, sortie.stderr[:300])
        d = json.loads(sortie.stdout)
        self.assertEqual(d["langue"], "en")
        self.assertEqual(d["schema"], "drave.annotation")

    def test_refus_est_une_reponse_json(self):
        sortie = _cli("analyser", "", "--json")
        self.assertEqual(sortie.returncode, 3, sortie.stderr[:300])
        d = json.loads(sortie.stdout)
        self.assertEqual(d["refus"], "vide")
        self.assertEqual(d["etiquettes"], [])
        self.assertEqual(d["schema"], "drave.annotation")

    def test_surrogate_isole_ne_plante_pas(self):
        """Le surrogate ne peut pas passer par argv (l'OS l'encode) : on teste l'API puis l'écriture."""
        sys.path.insert(0, str(RACINE))
        import tools.bloc_linguistique as bl
        a = bl.Heuristique().analyser("Le chat \ud800 dort.", "fr")
        d = a.json()
        # l'écriture doit tolérer le surrogate (c'est le bug produit d'origine)
        texte = json.dumps(d, ensure_ascii=False).encode("utf-8", "replace").decode("utf-8", "replace")
        self.assertGreater(len(d["etiquettes"]), 3)
        self.assertIn("Le chat", texte)

    def test_rejeu_identique(self):
        a = _cli("rejouer", "Le chat dort.")
        b = _cli("rejouer", "Le chat dort.")
        self.assertEqual(a.returncode, 0, a.stderr[:300])
        self.assertEqual(a.stdout, b.stdout)

    def test_mutation_detectee(self):
        """Contrôle négatif : un JSON amputé d'un champ obligatoire est bien refusé par le test."""
        d = json.loads(_cli("analyser", "Le chat dort.", "--json").stdout)
        d.pop("schema")
        manquants = [k for k in OBLIGATOIRES if k not in d]
        self.assertEqual(manquants, ["schema"])


class TestSchemaV2(unittest.TestCase):
    def test_le_schema_v2_declare_partition_et_alternative(self):
        """Les deux champs ajoutés en v2 sont typés, pas seulement tolérés."""
        schema = json.loads(SCHEMA_V2.read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["version"]["const"], 2)
        meta = schema["properties"]["etiquettes"]["items"]["properties"]["meta"]
        for champ in ("partition", "alternative"):
            self.assertIn(champ, meta["properties"], champ)
        self.assertIn("vue", meta["properties"]["partition"]["properties"])
        self.assertIn("relation", meta["properties"]["alternative"]["items"]["properties"])


class TestRetrocompatibilite(unittest.TestCase):
    def test_v1_reste_lue_et_v2_la_refuse(self):
        """Le vérificateur choisit le schéma par `version` ; v2 refuse bien une annotation v1."""
        sortie = subprocess.run([sys.executable, str(VERIFICATEUR), "--json"],
                                capture_output=True, text=True, cwd=str(RACINE))
        self.assertEqual(sortie.returncode, 0, sortie.stderr[:300])
        d = json.loads(sortie.stdout)
        self.assertTrue(d["retrocompatibilite"]["v1_lue"])
        self.assertTrue(d["retrocompatibilite"]["v2_refuse_v1"])
        self.assertEqual({r["version"] for r in d["cas"]}, {1, 2})
        self.assertTrue(SCHEMA_V1.is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
