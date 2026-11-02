"""gold_synthetique.py — le gold étendu : 160 phrases générées par une grammaire indépendante.

Les 20 phrases de `gold.py` sont **réelles** (écrites à la main) ; celles-ci sont **synthétiques** :
une grammaire hors du bloc (GN, GV, GP, REL, SUB, question, exclamation, impératif, négation,
modalité, double sens) et un lexique **disjoint** des listes de l'heuristique (renard, montagne,
saute, calme…), pour mesurer la **généralisation** des classes ouvertes. La grammaire produit
l'annotation (POS, segments, pragmatique) ; l'heuristique ne voit que le texte.
"""
from __future__ import annotations

import json
import pathlib
import random

DET = [("le", "M"), ("la", "F"), ("les", "P"), ("un", "M"), ("une", "F"),
       ("ce", "M"), ("cette", "F"), ("mon", "M"), ("ma", "F")]
N = [("renard", "M"), ("montagne", "F"), ("rivière", "F"), ("cheval", "M"), ("fenêtre", "F"),
     ("cuisine", "F"), ("chemin", "M"), ("village", "M"), ("forêt", "F"), ("nuage", "M"),
     ("étoile", "F"), ("jardin", "M"), ("papier", "M"), ("lettre", "F"), ("voyage", "M"),
     ("chanson", "F"), ("canard", "M"), ("livre", "M"), ("avocat", "M")]
V = [("saute", "S"), ("marche", "S"), ("nage", "S"), ("crie", "S"), ("rêve", "S"),
     ("prépare", "S"), ("range", "S"), ("compte", "S"), ("dessine", "S"), ("observe", "S"),
     ("écoute", "S"), ("cherche", "S"), ("trouve", "S"), ("ouvre", "S"), ("ferme", "S"),
     ("commence", "S"), ("finit", "S")]
ADJ = [("calme", "E"), ("sombre", "E"), ("brillant", "M"), ("brillante", "F"),
       ("doux", "M"), ("douce", "F"), ("secret", "M"), ("secrète", "F"),
       ("ancien", "M"), ("ancienne", "F"), ("rapide", "E"), ("lent", "M"), ("lente", "F")]
PREP = ["dans", "sur", "sous", "avec", "pour", "de", "à", "chez", "vers", "devant"]
PRON = ["il", "elle", "nous", "vous", "ils", "elles"]
PROPRE = ["Marie", "Paul", "Alice", "Lucas", "Emma", "Hugo"]
ADV = ["ici", "hier", "demain", "souvent", "toujours", "vite", "bien", "fort"]
AUX = ["a", "est", "ont", "sont"]
MODAL = ["peut", "doit", "pourrait", "devrait"]
DOUBLE = {"canard", "livre", "avocat"}


class P:
    def __init__(self, rng):
        self.rng = rng

    def det(self, genre):
        choix = [d for d in DET if d[1] == genre or d[1] == "P"]
        return self.rng.choice(choix)[0]

    def nom(self):
        return self.rng.choice(N)

    def adj(self, genre):
        choix = [a for a in ADJ if a[1] == genre or a[1] == "E"]
        return self.rng.choice(choix)[0]

    def verbe(self):
        return self.rng.choice(V)[0]

    def gn(self):
        r = self.rng.random()
        if r < 0.15:
            return [(self.rng.choice(PRON), "PRON")], "PRON"
        if r < 0.25:
            return [(self.rng.choice(PROPRE), "NOUN")], "PROPRE"
        nom, genre = self.nom()
        tokens = [(self.det(genre), "DET")]
        if self.rng.random() < 0.4:
            tokens.append((self.adj(genre), "ADJ"))
        tokens.append((nom, "NOUN"))
        return tokens, "GN"

    def gv(self):
        r = self.rng.random()
        v = self.verbe()
        if r < 0.35:
            return [(v, "VERB")], []
        if r < 0.55:
            return [(self.rng.choice(AUX), "AUX"), (v, "VERB")], []
        if r < 0.70:
            gn, _ = self.gn()
            return [(v, "VERB")] + gn, []
        if r < 0.85:
            prep = self.rng.choice(PREP)
            gn, _ = self.gn()
            return [(v, "VERB"), (prep, "PREP")] + gn, [(prep, gn)]
        if r < 0.93:
            genre = self.rng.choice(["M", "F"])
            return [(self.rng.choice(AUX), "AUX"), (self.adj(genre), "ADJ")], []
        return [(self.rng.choice(ADV), "ADV"), (v, "VERB")], []

    def phrase(self, pid):
        """Une phrase, ses tokens/POS, ses segments (index) et son pragmatique."""
        mode = self.rng.choice(["sv", "sv_gp", "rel", "sub", "question", "exclamation",
                                "imperatif", "negation", "modal", "double"])
        tokens, segs, pragma = [], [], {"acte": "assertion", "negation": False,
                                        "modalite": False, "double_sens": False}
        if mode == "sv":
            gn, _ = self.gn(); tokens += gn; s = len(tokens) - len(gn); segs.append(("GN", s, len(tokens)))
            gv, gps = self.gv(); tokens += gv; v = s + len(gn); segs.append(("GV", v, len(tokens)))
            v_txt = next((t for t, p in gv if p == "VERB"), gv[-1][0])
            for prep, g in gps:
                i = v + [t[0] for t in gv].index(prep) + 1
                segs.append(("GP", i, i + len(g), [v_txt, gn[-1][0]]))
        elif mode == "sv_gp":
            gn, _ = self.gn(); tokens += gn; segs.append(("GN", 0, len(tokens)))
            v = self.verbe(); tokens.append((v, "VERB")); segs.append(("GV", len(tokens) - 1, len(tokens)))
            prep = self.rng.choice(PREP); gn2, _ = self.gn(); tokens.append((prep, "PREP"))
            i = len(tokens); tokens += gn2; segs.append(("GP", i - 1, len(tokens), [v, gn[-1][0]]))
        elif mode == "rel":
            gn, _ = self.gn(); tokens += gn; segs.append(("GN", 0, len(tokens)))
            i = len(tokens); nom = gn[-1][0]; tokens.append(("qui", "PRON"))
            v = self.verbe(); tokens.append((v, "VERB"))
            segs.append(("REL", i, len(tokens), [nom]))
            v2 = self.verbe(); tokens.append((v2, "VERB")); segs.append(("GV", len(tokens) - 1, len(tokens)))
        elif mode == "sub":
            gn, _ = self.gn(); tokens += gn; segs.append(("GN", 0, len(tokens)))
            v = self.verbe(); tokens.append((v, "VERB")); segs.append(("GV", len(tokens) - 1, len(tokens)))
            i = len(tokens); tokens.append(("que", "CONJ"))
            gn2, _ = self.gn(); tokens += gn2; v2 = self.verbe(); tokens.append((v2, "VERB"))
            segs.append(("SUB", i, len(tokens), [v]))
        elif mode == "question":
            gn, _ = self.gn(); tokens += gn; segs.append(("GN", 0, len(tokens)))
            v = self.verbe(); tokens.append((v, "VERB")); segs.append(("GV", len(tokens) - 1, len(tokens)))
            pragma["acte"] = "question"; pragma["reponse"] = "oui"; tokens.append(("?", "PONCT"))
        elif mode == "exclamation":
            gn, _ = self.gn(); tokens += gn; segs.append(("GN", 0, len(tokens)))
            v = self.verbe(); tokens.append((v, "VERB")); segs.append(("GV", len(tokens) - 1, len(tokens)))
            pragma["acte"] = "exclamation"; tokens.append(("!", "PONCT"))
        elif mode == "imperatif":
            v = self.verbe(); tokens.append((v.capitalize(), "VERB")); segs.append(("GV", 0, 1))
            pragma["acte"] = "exclamation"; tokens.append(("!", "PONCT"))
        elif mode == "negation":
            gn, _ = self.gn(); tokens += gn; segs.append(("GN", 0, len(tokens)))
            i = len(tokens); tokens.append(("ne", "ADV")); v = self.verbe(); tokens.append((v, "VERB"))
            tokens.append(("pas", "ADV")); segs.append(("GV", i, len(tokens)))
            pragma["negation"] = True
        elif mode == "modal":
            gn, _ = self.gn(); tokens += gn; segs.append(("GN", 0, len(tokens)))
            i = len(tokens); tokens.append((self.rng.choice(MODAL), "VERB"))
            tokens.append((self.verbe(), "VERB")); segs.append(("GV", i, len(tokens)))
            pragma["modalite"] = True
        else:  # double
            nom, genre = self.rng.choice([x for x in N if x[0] in DOUBLE])
            tokens = [(self.det(genre), "DET"), (nom, "NOUN")]
            segs.append(("GN", 0, 2))
            v = self.verbe(); tokens.append((v, "VERB")); segs.append(("GV", 2, 3))
            pragma["double_sens"] = True
        mots, pos, segments = [], [], []
        for t, p in tokens:
            if p == "PONCT":
                continue
            mots.append((t, p))
        # le texte final (ponctuation séparée)
        ponct = "?" if pragma["acte"] == "question" else ("!" if pragma["acte"] == "exclamation" else "")
        texte = " ".join(t for t, _ in mots) + ponct
        # segments : les indices portent sur les tokens hors ponctuation
        for item in segs:
            typ, a, b = item[:3]
            if b <= a:
                continue
            segments.append(item)
        return {"id": pid, "langue": "fr", "texte": texte, "tokens": mots,
                "segments_idx": segments, "pragma": pragma, "source": "synthetique"}


def construire(n=160, graine=42) -> dict:
    rng = random.Random(graine)
    p = P(rng)
    vus, phrases = set(), []
    essais = 0
    while len(phrases) < n and essais < n * 20:
        essais += 1
        d = p.phrase(f"s{len(phrases) + 1:03d}")
        if d["texte"] in vus:
            continue
        vus.add(d["texte"])
        # spans des mots et des segments
        mots, curseur = [], 0
        for t, pos in d.pop("tokens"):
            i = d["texte"].find(t, curseur)
            assert i >= 0, (d["texte"], t)
            mots.append({"texte": t, "pos": pos, "debut": i, "fin": i + len(t)})
            curseur = i + len(t)
        segments = []
        for item in d.pop("segments_idx"):
            typ, a, b = item[:3]
            cible = item[3] if len(item) > 3 else None
            cibles = cible if isinstance(cible, list) else ([cible] if cible else [])
            debut = mots[a]["debut"]
            fin = mots[b - 1]["fin"]
            seg = {"type": typ, "texte": d["texte"][debut:fin], "role": typ.lower(),
                   "debut": debut, "fin": fin}
            if cibles:
                seg["cibles"] = cibles
                seg["cible"] = cibles[0]
            segments.append(seg)
        d["mots"] = mots
        d["segments"] = segments
        phrases.append(d)
    return {"version": 1, "source": "synthetique", "graine": graine,
            "note": "160 phrases d'une grammaire indépendante ; lexique disjoint de l'heuristique.",
            "phrases": phrases}


if __name__ == "__main__":
    sortie = pathlib.Path(__file__).with_name("gold_synthetique.json")
    sortie.write_text(json.dumps(construire(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"gold synthétique écrit → {sortie}")
