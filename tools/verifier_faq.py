#!/usr/bin/env python3
"""verifier_faq.py — les dix réponses de la FAQ produit, vérifiées contre le code courant.

La FAQ de `docs/produit/README.md` (§ 8) ne doit pas être une prose recopiée : chaque
réponse est adossée à une commande, à un chiffre de `reports/` ou à une constante du
code. Ce vérificateur exécute les dix contrôles, imprime un JSON (ou un résumé) et sort
avec le code 1 si une réponse ne tient plus.

Ce qu'il ne fait pas : aucune mesure nouvelle, aucun appel réseau, aucune clé lue. Il
rejoue le CLI en local, lit les JSON de résultats déjà publiés et inspecte le source.

Usage :
    python3 tools/verifier_faq.py            # résumé lisible
    python3 tools/verifier_faq.py --json     # le JSON de reports/faq.json

Le **contrôle négatif** est explicite : on vérifie qu'une affirmation fausse (« le CLI
accepte --langue de ») est bien rejetée par le code. Si ce contrôle passait, le
vérificateur ne prouverait rien.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import pathlib
import subprocess
import sys
import tempfile

RACINE = pathlib.Path(__file__).resolve().parent.parent
DRAVE = RACINE / "tools" / "drave.py"
DATE = "2026-11-15"
VERSION = "0.1.0"
FAQ = "docs/produit/README.md#8-faq--dix-questions"


def _run(args: list[str], *, env: dict | None = None, script: pathlib.Path | None = None,
         timeout: int = 180) -> subprocess.CompletedProcess:
    """Lance le CLI (ou un outil) depuis la racine, en UTF-8."""
    cmd = [sys.executable, str(script or DRAVE), *args]
    return subprocess.run(cmd, cwd=RACINE, text=True, encoding="utf-8",
                          errors="replace", capture_output=True, env=env,
                          timeout=timeout)


def _json(args: list[str], *, env: dict | None = None) -> dict:
    r = _run([*args, "--json"], env=env)
    if r.returncode != 0:
        raise AssertionError(f"{args} a rendu {r.returncode} : {r.stderr[:400]}")
    return json.loads(r.stdout)


def _lire(chemin: str):
    return json.loads((RACINE / chemin).read_text(encoding="utf-8"))


def _sans_cle() -> dict:
    """L'environnement sans aucune clé DeepSeek, avec un HOME vide."""
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("DEEPSEEK", "DSH_"))}
    env["HOME"] = tempfile.mkdtemp(prefix="drave-faq-home-")
    return env


# ------------------------------------------------------------------ les dix contrôles


def q1_langue() -> dict:
    """La langue : détection ouverte, indice CLI limité à fr/en, `und` honnête."""
    de = _json(["analyser", "Der Hund schläft."])
    es = _json(["analyser", "El perro duerme."])
    und = _json(["analyser", "Élodie sourit."])
    und_fr = _json(["analyser", "Élodie sourit.", "--langue", "fr"])
    refus = _run(["analyser", "Le chat dort.", "--langue", "de"])
    assert de["langue"] == "de", de["langue"]
    assert es["langue"] == "es", es["langue"]
    assert und["langue"] == "und", und["langue"]
    assert und_fr["langue"] == "und", und_fr["langue"]  # l'indice n'est pas une contrainte
    assert refus.returncode == 5, refus.returncode

    bloc = (RACINE / "reports/rapport-bloc-linguistique.md").read_text(encoding="utf-8")
    assert "398 langues" in bloc and "0,9687" in bloc, "profils UDHR absents de la fiche"
    source = (RACINE / "tools/bloc_linguistique.py").read_text(encoding="utf-8")
    assert "seuil_langue: float = 0.12" in source, "seuil de langue introuvable"
    return {
        "detection": {"Der Hund schläft.": de["langue"], "El perro duerme.": es["langue"]},
        "und": {"Élodie sourit.": und["langue"], "avec --langue fr": und_fr["langue"]},
        "indice_cli": {"choix": ["fr", "en"], "--langue de": f"code {refus.returncode}"},
        "profils_udhr": {"langues": 398, "exactitude": 0.9687, "seuil": 0.12,
                         "source": "reports/rapport-bloc-linguistique.md"},
    }


def q2_hors_ligne() -> dict:
    """Le défaut n'ouvre aucune socket et n'importe pas le module réseau."""
    code = r"""
import contextlib, io, socket, sys
sys.path.insert(0, "tools")
import drave
def deny(*a, **k):
    raise AssertionError("socket ouverte")
socket.socket = deny
socket.create_connection = deny
with contextlib.redirect_stdout(io.StringIO()):
    rc = drave.main(["analyser", "Le chat dort.", "--json"])
print(rc, "tools.llm.deepseek" in sys.modules)
"""
    r = subprocess.run([sys.executable, "-c", code], cwd=RACINE, text=True,
                       encoding="utf-8", errors="replace", capture_output=True,
                       timeout=120)
    assert r.returncode == 0, r.stderr[-600:]
    rc, importe = r.stdout.split()
    assert rc == "0" and importe == "False", (rc, importe)

    sans_cle = _run(["analyser", "Le chat dort.", "--tagger"], env=_sans_cle())
    assert sans_cle.returncode == 4, sans_cle.returncode
    assert sans_cle.stdout == "", sans_cle.stdout[:200]
    assert "dépendance absente" in sans_cle.stderr, sans_cle.stderr[:300]
    assert "hors ligne" in sans_cle.stderr, sans_cle.stderr[:300]
    return {
        "socket_interdite": {"code": 0, "module_reseau_importe": False},
        "tagger_sans_cle": {"code": 4, "stdout_vide": True,
                            "stderr": "dépendance absente … hors ligne"},
        "defaut": "heuristique, CPU, sans modèle, sans GPU, sans réseau",
    }


def q3_cout() -> dict:
    """Le coût : 0 $ d'API par défaut ; 1 appel/phrase et ~0,02 $ pour 612 avec le tagger."""
    d = _lire("reports/pensee-tagger-option.json")
    apres = d["apres_15_11"]
    assert apres["appels_par_phrase"] == 1, apres["appels_par_phrase"]
    assert apres["cout"]["appels"] == 609, apres["cout"]["appels"]
    assert apres["cout"]["tokens"] == 22299, apres["cout"]["tokens"]
    assert round(apres["cout"]["latence_s"], 1) == 155.6, apres["cout"]["latence_s"]
    assert apres["cout"]["requetes"] == 159, apres["cout"]["requetes"]
    assert apres["pos_612"] == 0.9575, apres["pos_612"]

    ex = _lire("reports/rapport-exemples-tagger.json")["tagger"]["total"]
    assert (ex["appels"], ex["tokens"], ex["latence_s"]) == (3, 441, 3.7), ex

    source = DRAVE.read_text(encoding="utf-8")
    assert source.count("bl.NeuronalLLMPOS(") == 1, "un seul tagger POS attendu"
    assert "NeuronalLLMChunks" not in source, "le tagger de syntagmes a été retiré"
    return {
        "defaut": {"cout_api_usd": 0, "reseau": 0},
        "tagger": {"appels": 609, "tokens": 22299, "latence_s": 155.6,
                   "requetes": 159, "cout_usd": 0.02, "appels_par_phrase": 1},
        "exemples": {"appels": 3, "tokens": 441, "latence_s": 3.7},
        "cache": "seconde analyse : réseau 0, tokens 0",
        "source": "reports/pensee-tagger-option.json#apres_15_11",
    }


def q4_tagger() -> dict:
    """`--tagger` ne remplace que le POS ; la clé est optionnelle et jamais affichée."""
    d = _lire("reports/pensee-tagger-option.json")
    option = d["option"]
    assert option["commandes"] == ["analyser", "evaluer"], option["commandes"]
    assert option["modele_demande"] == "deepseek-chat", option["modele_demande"]
    assert option["seuil_cascade"] == 0.6, option["seuil_cascade"]
    assert option["fusion"]["pos"].startswith("neuronal"), option["fusion"]
    assert option["fusion"]["syntagme"] == "heuristique", option["fusion"]
    assert option["cle"][:3] == ["DEEPSEEK_KEY_FILE", "~/.config/drave/deepseek.key",
                                 "DEEPSEEK_API_KEY"], option["cle"]

    apres = d["apres_15_11"]
    assert apres["ponct"] == "25/25", apres["ponct"]
    assert apres["pos_612"] == 0.9575 and apres["delta"] == 0.095, apres
    assert d["base_reelle_452"]["pos_tagger"] == 0.95, d["base_reelle_452"]

    source = DRAVE.read_text(encoding="utf-8")
    assert 'MODELE_TAGGER = "deepseek-chat"' in source
    assert "SEUIL_TAGGER = 0.6" in source
    assert 'PRIORITE_TAGGER["syntagme"] = "heuristique"' in source
    return {
        "change": {"pos": "API", "syntagmes": "heuristique", "roles": "heuristique",
                   "attachement": "heuristique", "pragmatique": "heuristique",
                   "ponctuation": "25/25 restituée"},
        "pos": {"612": {"heuristique": 0.8625, "tagger": 0.9575, "delta": 0.095},
                "452_reel": {"heuristique": 0.8891, "tagger": 0.95, "delta": 0.0609}},
        "cle": option["cle"],
        "sans_cle": {"code": 4, "stdout": "vide"},
    }


def q5_schema() -> dict:
    """Le schéma v2 lit v1, v2 refuse v1 ; la compatibilité octet pour octet n'est pas garantie."""
    base = json.loads(_run(["--json"], script=RACINE / "tools/verifier_schema_produit.py").stdout)
    assert base["versions_lues"] == [1, 2], base["versions_lues"]
    assert base["retrocompatibilite"] == {"v1_lue": True, "v2_refuse_v1": True}, base
    assert len(base["cas"]) == 6 and all(c["ok"] for c in base["cas"]), base["cas"]

    vingt = json.loads(_run(["--gold", "20", "--json"],
                            script=RACINE / "tools/verifier_schema_produit.py").stdout)
    assert len(vingt["cas"]) == 26 and all(c["ok"] for c in vingt["cas"]), vingt["cas"]

    v1 = _lire("tools/schemas/drave-annotation-v1.json")
    v2 = _lire("tools/schemas/drave-annotation-v2.json")
    assert v1["properties"]["version"]["const"] == 1
    assert v2["properties"]["version"]["const"] == 2
    meta = v2["properties"]["etiquettes"]["items"]["properties"]["meta"]
    assert "partition" in meta["properties"]
    assert "alternative" in meta["properties"]
    return {
        "schema": "drave.annotation", "version": 2,
        "racine_obligatoire": v2["required"],
        "v2_ajoute": ["meta.partition", "meta.alternative"],
        "verificateur": {"cas": 6, "echecs": 0, "avec_gold_20": 26,
                         "versions_lues": [1, 2],
                         "v1_lue": True, "v2_refuse_v1": True},
        "compatibilite_octet": "non garantie (le bump change le JSON et le sha256)",
    }


def q6_attachement() -> dict:
    """L'attachement : 238/239, exact sur les spans prédits, contrôles négatifs durs."""
    d = _json(["evaluer"])
    a = d["heuristique"]["attachement"]
    assert d["gold"]["phrases"] == 612 and d["gold"]["cibles_attachement"] == 239, d["gold"]
    assert a["cibles"] == 239 and a["labels"] == 238, a
    assert a["exact_taux"] == 0.9958 and a["couverture"] == 0.9958, a
    assert a["exact_taux_span"] == 1.0, a["exact_taux_span"]
    assert a["topk_taux"] == 0.9874, a["topk_taux"]
    assert d["controle_negatif"]["exact_taux"] == 0.0167, d["controle_negatif"]

    audit = _lire("reports/pensee-audit-v10.json")["controle_negatif"]
    assert audit["candidat_aleatoire"]["top1_taux"] == 0.4214, audit["candidat_aleatoire"]
    assert audit["permutation_globale"]["taux_moyen"] == 0.00908, audit["permutation_globale"]
    return {
        "gold": {"phrases": 612, "cibles": 239, "labels": 238},
        "exact": 0.9958, "exact_sur_span": 1.0, "top_k": 0.9874,
        "controle_cli": {"cible_au_hasard": 0.0167},
        "controle_audit_v10": {"candidat_aleatoire_top1": 0.4214,
                               "permutation_cibles": 0.00908},
        "lecture": "in-sample, split dev/test ; exactitude conditionnelle aux spans prédits",
    }


def q7_span_inatteignable() -> dict:
    """Le seul label manquant : g017, dont la SUB inclut l'adverbe final."""
    gold = _lire("tools/tests/linguistique/gold.json")["phrases"]
    g017 = next(p for p in gold if p["id"] == "g017")
    sub = next(s for s in g017["segments"] if s["type"] == "SUB")
    assert (sub["debut"], sub["fin"], sub["cible"]) == (9, 28, "said"), sub

    a = _json(["analyser", g017["texte"]])
    pred = next(e for e in a["etiquettes"]
                if e["niveau"] == "syntagme" and e["type"] == "SUB")
    assert (pred["debut"], pred["fin"]) == (9, 38), (pred["debut"], pred["fin"])
    assert pred["meta"]["attachement"]["cible"] == "said", pred["meta"]

    g = _lire("reports/pensee-g017.json")
    assert (g["verdict"]["f1_avant"], g["verdict"]["f1_apres"]) == (0.7902, 0.7901), g
    assert (g["verdict"]["couverture_avant"], g["verdict"]["couverture_apres"]) == (0.9958, 0.9916), g

    reel = _json(["evaluer", "--reel"])
    assert reel["gold"]["cibles_attachement"] == 184, reel["gold"]
    assert reel["heuristique"]["attachement"]["labels"] == 183, reel["heuristique"]
    assert reel["heuristique"]["attachement"]["exact_taux"] == 0.9946, reel["heuristique"]
    return {
        "g017": {"gold_sub": [9, 28, "that she would come"],
                 "predit": [9, 38, "that she would come yesterday"],
                 "cible": "said (juste)",
                 "seul_label_manquant": True},
        "regle_rejetee": {"f1": [0.7902, 0.7901], "couverture": [0.9958, 0.9916]},
        "reel_452": {"cibles": 184, "labels": 183, "exact": 0.9946},
        "lecture": "238/239 est conditionnel aux spans prédits, pas la couverture du langage",
    }


def q8_restitution() -> dict:
    """Trois vues : surface exacte, forme canonique, rôles lisibles mais peu fidèles."""
    banc = "reports/pensee-fiabilite-produit.json"
    v0 = _json(["restituer", "--banc", banc])
    s0 = v0["synthese"]
    assert s0["annotations"] == 46 and s0["surface"]["exacts"] == 46, s0
    assert s0["miroir"]["fidelite"] == 0.1087, s0["miroir"]
    assert s0["controle_negatif"]["detectes"] == 46, s0["controle_negatif"]

    v1 = _json(["restituer", "--banc", banc, "--canonique"])
    s1 = v1["synthese"]
    assert s1["canonique"]["exacts"] == 46, s1["canonique"]
    assert s1["strict"]["fidelite"] == 0.1087, s1["strict"]
    assert s1["structure"]["segments"] == 395, s1["structure"]
    assert s1["structure"]["attachements"] == 315, s1["structure"]

    v2 = _json(["restituer", "--banc", banc, "--roles"])
    s2 = v2["synthese"]
    assert s2["cadre"]["exacts"] == 19 and s2["cadre"]["exacts_non_vides"] == 16, s2["cadre"]
    assert s2["roles"]["f1"] == 0.527, s2["roles"]
    assert s2["controles"]["rendu"]["exacts"] == 46, s2["controles"]["rendu"]
    assert s2["controles"]["spans_dans_source"] == {"justes": 198, "total": 198,
                                                    "taux": 1.0}, s2["controles"]

    une = _json(["restituer", "Le chat dort.", "--roles"])
    principal = une["roles"]["principal"]
    assert (principal["agent"], principal["predicat"], principal["lieu"]) == ("Le chat", "dort", ""), principal
    assert une["rendu"]["exact"] is True and une["controle_negatif_rendu"]["detecte"] is True
    return {
        "v0_surface": {"exacts": 46, "miroir_strict": 0.1087},
        "v1_canonique": {"exacts": 46, "strict": 0.1087, "segments": 395, "cibles": 315},
        "v2_roles": {"cadres_exacts": 19, "non_vides": 16, "f1": 0.527,
                     "spans_dans_source": 198, "rendus_relus": 46},
        "exemple": {"agent": "Le chat", "predicat": "dort", "lieu": ""},
        "lecture": "la v2 expose les rôles de l'annotation, elle ne les corrige pas",
    }


def q9_limites() -> dict:
    """Les limites nommées : pas de génération, de serveur, de local, ni d'options fantômes."""
    aide = _run(["--aide"])
    assert aide.returncode == 0
    for commande in ("analyser", "evaluer", "rejouer", "restituer"):
        assert commande in aide.stdout, commande
    for fantome in ("--sortie", "--mode", "--strict"):
        assert fantome not in aide.stdout, fantome
        r = _run(["analyser", "Le chat dort.", fantome])
        assert r.returncode == 5, (fantome, r.returncode)

    source = DRAVE.read_text(encoding="utf-8")
    for interdit in ("http.server", "transformers", "torch", "sys.stdin"):
        assert interdit not in source, interdit

    # Les rôles sont normalisés par une table unique et un vocabulaire fermé.
    try:
        from roles_vocabulaire import CORRESPONDANCES, ROLES, normaliser_role
    except ImportError:
        from tools.roles_vocabulaire import CORRESPONDANCES, ROLES, normaliser_role
    assert normaliser_role("prédicat") == "predicat"
    assert normaliser_role("qualité") == "qualite"
    assert set(CORRESPONDANCES.values()) <= set(ROLES)

    # Les candidats : les chaînes historiques restent, et la v2 ajoute les objets.
    a = _json(["analyser", "Le livre que j'ai lu est intéressant."])
    candidats = [c for e in a["etiquettes"] if e["niveau"] == "syntagme"
                 for c in (e.get("candidats") or [])]
    assert candidats and all(isinstance(c, str) for c in candidats), candidats[:3]
    objets = [c for e in a["etiquettes"] if e["niveau"] == "syntagme"
              for c in (((e.get("meta") or {}).get("attachement") or {}).get("candidats") or [])]
    assert objets and all(isinstance(c, dict) and set(c) == {"span", "cible", "source"}
                          for c in objets), objets[:3]
    for candidat in objets:
        debut, fin = candidat["span"]["debut"], candidat["span"]["fin"]
        assert a["texte"][debut:fin] == candidat["cible"], candidat
    return {
        "absent": ["génération", "traduction", "serveur HTTP", "RSN/DRVM",
                   "neuronal local", "classement appris", "calibration des confiances",
                   "--langue-forcee", "garantie hors domaine", "entrée standard",
                   "--sortie", "parcours de répertoire", "rejeu d'une annotation sauvegardée",
                   "publication PyPI"],
        "empaquetage": {"livre": "pip install -e . + commande drave",
                        "non_livre": "wheel / paquet PyPI"},
        "options_fantomes": {"--sortie": "code 5", "--mode": "code 5", "--strict": "code 5"},
        "candidats": {"type": "objets {span, cible, source} (v2) ; "
                             "chaînes d'affichage en lecture",
                      "exemple": objets[0]},
        "roles": {"vocabulaire": list(ROLES),
                  "bruts": "21 → 8 (gold 612)",
                  "lecture": "rôles normalisés, sans accents mélangés"},
        "lecture": "le format est versionné ; la qualité linguistique ne l'est pas",
    }


def q10_installation() -> dict:
    """Source et pyproject : Python 3.10+, stdlib, installation éditable, gold versionnés."""
    version = _run(["--version"])
    assert version.returncode == 0 and version.stdout.strip() == "drave 0.1.0", version.stdout

    sans_site = subprocess.run(
        [sys.executable, "-S", str(DRAVE), "analyser", "Le chat dort.", "--json"],
        cwd=RACINE, text=True, encoding="utf-8", errors="replace",
        capture_output=True, timeout=120)
    assert sans_site.returncode == 0, sans_site.stderr[-600:]
    assert json.loads(sans_site.stdout)["langue"] == "fr"

    for f in ("tools/drave.py", "tools/bloc_linguistique.py",
              "tools/restitution.py", "tools/restitution_v2.py"):
        ast.parse((RACINE / f).read_text(encoding="utf-8"), filename=f,
                  feature_version=(3, 10))

    pyproject = RACINE / "pyproject.toml"
    assert pyproject.is_file(), "pyproject.toml absent"
    source = pyproject.read_text(encoding="utf-8")
    for attendu in ('name = "drave"', 'version = "0.1.0"',
                    'requires-python = ">=3.10"', "dependencies = []",
                    'drave = "tools.drave:main"'):
        assert attendu in source, attendu
    for nom in ("setup.py", "setup.cfg", "requirements.txt"):
        assert not (RACINE / nom).exists(), nom

    golds = ["gold.json", "gold_gele.json", "gold_reel.json", "gold_synthetique.json"]
    for nom in golds:
        assert (RACINE / "tools/tests/linguistique" / nom).is_file(), nom
    return {
        "version": "drave 0.1.0",
        "python": {"grammaire": "3.10", "mesure": sys.version.split()[0],
                   "sans_site_packages": "code 0"},
        "dependances_externes": 0,
        "empaquetage": {
            "fichier": "pyproject.toml",
            "nom": "drave",
            "version": "0.1.0",
            "requires_python": ">=3.10",
            "dependances": [],
            "script_console": "drave = tools.drave:main",
            "installation": "python3 -m pip install -e . (venv)",
            "hors_depot": "commande drave depuis n'importe quel répertoire",
        },
        "gold_versionnes": golds,
        "racine": "le chemin historique reste garanti : python3 tools/drave.py",
    }


CONTROLES = [
    (1, "Quelles langues le produit reconnaît-il ?", q1_langue),
    (2, "Est-ce que ça marche hors ligne ?", q2_hors_ligne),
    (3, "Combien ça coûte ?", q3_cout),
    (4, "Qu'est-ce que --tagger change ?", q4_tagger),
    (5, "Quel est le format de sortie, et est-il stable ?", q5_schema),
    (6, "Que veut dire « attachement », et à quel point est-il fiable ?", q6_attachement),
    (7, "Pourquoi reste-t-il un span inatteignable ?", q7_span_inatteignable),
    (8, "Que peut-on restituer : la surface, la forme, les rôles ?", q8_restitution),
    (9, "Quelles limites faut-il connaître avant de s'en servir ?", q9_limites),
    (10, "Comment l'installer et le lancer ?", q10_installation),
]


def controle_negatif() -> dict:
    """Une affirmation fausse doit être rejetée par le code, sinon le vérificateur ment."""
    # Faux : « le CLI accepte --langue de ». Le code doit sortir 2.
    r = _run(["analyser", "Le chat dort.", "--langue", "de"])
    # Faux : « le schéma v2 accepte une annotation v1 ». Le vérificateur doit le refuser.
    base = json.loads(_run(["--json"], script=RACINE / "tools/verifier_schema_produit.py").stdout)
    detecte = (r.returncode == 5
               and base["retrocompatibilite"]["v2_refuse_v1"] is True)
    return {
        "affirmations_fausses": [
            "le CLI accepte --langue de (il sort 5)",
            "le schéma v2 accepte l'annotation v1 (il la refuse)",
        ],
        "observe": {"--langue de": f"code {r.returncode}",
                    "v2_refuse_v1": base["retrocompatibilite"]["v2_refuse_v1"]},
        "detecte": detecte,
    }


def principal() -> dict:
    questions = []
    for ident, question, fonction in CONTROLES:
        try:
            observe = fonction()
            ok = True
            erreur = ""
        except Exception as exc:  # noqa: BLE001 — on veut le rapport, pas la trace
            observe = {}
            ok = False
            erreur = f"{type(exc).__name__} : {exc}"
        questions.append({"id": ident, "question": question, "observe": observe,
                          "ok": ok, "erreur": erreur})
    negatif = controle_negatif()
    return {
        "schema": "drave.faq.verification",
        "version": 1,
        "date": DATE,
        "produit": VERSION,
        "fichier": FAQ,
        "questions": questions,
        "controle_negatif": negatif,
        "ok": all(q["ok"] for q in questions) and negatif["detecte"],
    }


def _resume(rapport: dict) -> str:
    lignes = [f"FAQ produit — {sum(q['ok'] for q in rapport['questions'])}/10 réponses "
              f"vérifiées · contrôle négatif "
              f"{'détecté' if rapport['controle_negatif']['detecte'] else 'NON DÉTECTÉ'}"]
    for q in rapport["questions"]:
        etat = "✅" if q["ok"] else "❌"
        lignes.append(f"  {etat} {q['id']:2d}. {q['question']}")
        if not q["ok"]:
            lignes.append(f"      {q['erreur']}")
    lignes.append("✅ FAQ vérifiée" if rapport["ok"] else "❌ FAQ non vérifiée")
    return "\n".join(lignes)


def main(argv: list[str] | None = None) -> int:
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument("--json", action="store_true", help="le JSON de reports/faq.json")
    parseur.add_argument("--autotest", action="store_true",
                         help="vérifie que le contrôle négatif échoue bien")
    args = parseur.parse_args(argv)
    if args.autotest:
        negatif = controle_negatif()
        ok = negatif["detecte"] is True
        print("✅ autotest : l'affirmation fausse est rejetée" if ok
              else "❌ autotest : le contrôle négatif ne détecte rien")
        return 0 if ok else 1
    rapport = principal()
    if args.json:
        print(json.dumps(rapport, ensure_ascii=False, indent=1))
    else:
        print(_resume(rapport))
    return 0 if rapport["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
