#!/usr/bin/env python3
"""lecteur_controleur.py — R0.2 : choisir ce qu'on lit, et le payer.

POURQUOI CE FICHIER. La sortie précoce d'un modèle décide quand le prochain octet est
facile ; elle ne décide pas ce qui vaut la peine d'être lu. Il manque une **politique** :
survoler, balayer, lire, relire, s'arrêter — avec un budget et une trace.

Le point de mesure n'est pas le débit, c'est la **compréhension par unité de calcul**. On
compare donc deux lectures du MÊME document avec le MÊME lecteur : la lecture intégrale
(tout est lu) et la lecture contrôlée (une fraction du budget). Si le contrôleur choisit
bien, il retrouve le passage de la réponse intégrale pour une fraction du coût.

Trois décisions de conception, et leurs raisons :

  1. **le budget est en OCTETS de texte effectivement lus** — pas en régions, pas en
     secondes : un octet lu est un octet payé, et le graphe de document (R0.1) donne déjà
     les offsets exacts ;
  2. **le lecteur est constant** — seule la sélection change. Sinon on mesurerait le
     modèle, pas le contrôleur ;
  3. **le contrôleur est classique** (titres, premières phrases, BM25, regex) : c'est ce
     qui permet de dire si la lecture rapide est un problème de **contrôleur** — et pas
     encore une fois de modèle.

Usage :
  python3 tools/lecteur_controleur.py --manifeste /tmp/m.json --question "…" --budget 0,3
  python3 tools/lecteur_controleur.py --document docs/theorie/vision.md --question "…"
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import re
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document  # noqa: E402  (le manifeste de R0.1)

# Les mots outils ne portent pas la question. Les retirer n'est pas de la linguistique,
# c'est ce qui empêche « quelle est la taille de l'en-tête » de scorer sur « est/la/de ».
STOPWORDS = {
    "le", "la", "les", "de", "des", "du", "un", "une", "et", "en", "a", "au", "aux", "que",
    "qui", "quoi", "dont", "ou", "où", "pour", "par", "sur", "dans", "avec", "est", "sont",
    "ce", "cet", "cette", "ces", "il", "elle", "ils", "elles", "on", "se", "sa", "son",
    "ses", "leur", "leurs", "ne", "pas", "plus", "moins", "comme", "mais", "si", "tout",
    "tous", "toute", "toutes", "quel", "quelle", "quels", "quelles", "combien", "quand",
    "comment", "pourquoi", "the", "of", "and", "to", "is", "are", "what", "how", "many",
}

RE_JETON = re.compile(r"[0-9a-zà-öø-ÿ]+")
RE_PHRASE = re.compile(r"(?<=[.!?…])\s+(?=[0-9A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ«\"(])")
RE_VALEUR = re.compile(r"\b\d[\d\s.,]*\s?(octets?|ko|mo|go|%|ms|s|×|pts?)?\b", re.I)
RE_DATE = re.compile(r"\b(\d{1,2}\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|"
                     r"octobre|novembre|décembre)\s+\d{4}|\d{4}-\d{2}-\d{2})\b", re.I)


def jetons(texte: str) -> list[str]:
    return [j for j in RE_JETON.findall(texte.lower()) if j not in STOPWORDS and len(j) > 1]


# ------------------------------------------------------------------ les passages

def passages(manifeste: dict) -> list[dict]:
    """Le document en passages lisibles : une phrase, une ligne de tableau, une ligne de
    code. Chaque passage porte son offset exact dans le flux (R0.1), donc sa citation."""
    out: list[dict] = []
    section = "DÉBUT"
    for region in manifeste["regions"]:
        if region["type"] == "blanc":
            continue
        if region["type"] in ("titre", "section"):
            section = region["id"]
        texte = region["texte"]
        brut = texte.split("\n") if region["type"] in ("tableau", "code", "liste") \
            else RE_PHRASE.split(texte)
        position = 0
        for morceau in brut:
            morceau = morceau.strip()
            if len(morceau) < 3:
                position += len(morceau) + 1
                continue
            # l'offset du morceau dans la région : on le retrouve par recherche, en
            # avançant — un morceau peut apparaître deux fois, l'avance le désambiguïse.
            trouve = texte.find(morceau, position)
            if trouve < 0:
                trouve = texte.find(morceau)
            position = trouve + len(morceau) if trouve >= 0 else position
            debut = region["start"] + len(texte[:trouve].encode("utf-8")) if trouve >= 0 \
                else region["start"]
            out.append({
                "indice": len(out),
                "region": region["id"], "type": region["type"], "section": section,
                "texte": morceau, "start": debut, "octets": len(morceau.encode("utf-8")),
                "prov": region["prov"],
            })
    return out


# ------------------------------------------------------------------------ BM25

class Index:
    """BM25 sur les passages. Volontairement simple : le contrôleur n'a pas besoin d'un
    meilleur scoreur, il a besoin d'un scoreur **constant** entre les deux lectures."""

    k1, b = 1.5, 0.75

    def __init__(self, passages: list[dict]):
        self.passages = passages
        self.jetons = [jetons(p["texte"]) for p in passages]
        self.tf = [Counter(j) for j in self.jetons]
        self.longueurs = [len(j) for j in self.jetons]
        self.moyenne = (sum(self.longueurs) / len(self.longueurs)) if self.longueurs else 1.0
        self.df: Counter = Counter()
        for j in self.jetons:
            self.df.update(set(j))
        self.n = max(len(passages), 1)

    def scores(self, question: str) -> list[float]:
        requete = jetons(question)
        if not requete:
            return [0.0] * self.n
        scores = []
        for i in range(self.n):
            score = 0.0
            for jeton in requete:
                if jeton not in self.tf[i]:
                    continue
                df = self.df.get(jeton, 0)
                idf = math.log(1 + (self.n - df + 0.5) / (df + 0.5))
                tf = self.tf[i][jeton]
                score += idf * (tf * (self.k1 + 1)) / (
                    tf + self.k1 * (1 - self.b + self.b * self.longueurs[i] / self.moyenne))
            scores.append(score)
        return scores


# --------------------------------------------------------------- le contrôleur

class Controleur:
    """La politique : cinq actions, un budget, une trace. Chaque décision est un événement
    rejouable, et le coût est celui des octets réellement lus."""

    def __init__(self, passages: list[dict], question: str, budget_octets: int,
                 critere: str = "bm25"):
        self.passages = passages
        self.question = question
        self.budget = max(budget_octets, 1)
        self.index = Index(passages)
        self.scores = self.index.scores(question)
        if critere == "couverture":
            # BM25 récompense la RARETÉ des mots ; il ne voit pas qu'un passage contient
            # *tous* les mots de la question. La couverture le voit, et c'est ce qui
            # distingue une définition d'une phrase qui parle du même sujet.
            jetons_question = set(jetons(question))
            for i in range(len(passages)):
                couverture = len(jetons_question & set(self.index.jetons[i])) / max(len(jetons_question), 1)
                self.scores[i] += 2.0 * couverture
        self.lus: list[int] = []
        self.cout = 0
        self.evenements: list[dict] = []
        self.raison = "budget épuisé"

    # -- l'état
    def reste(self) -> int:
        return self.budget - self.cout

    def _trace(self, action: str, cout: int, **champs) -> None:
        self.evenements.append({"action": action, "cout": cout, "reste": self.reste(), **champs})

    def _lire(self, indices: list[int], action: str, raison: str) -> None:
        for i in indices:
            if i in self.lus or self.reste() <= 0:
                continue
            cout = self.passages[i]["octets"]
            if cout > self.reste():
                continue
            self.lus.append(i)
            self.cout += cout
            self._trace(action, cout, passage=i, score=round(self.scores[i], 3), raison=raison)

    # -- les actions
    def survol(self) -> list[int]:
        """Lire les en-têtes (titre/section) : c'est le sommaire, et il coûte peu."""
        entetes = [i for i, p in enumerate(self.passages) if p["type"] in ("titre", "section")]
        self._lire(entetes, "survol", "sommaire")
        return entetes

    def classer(self) -> dict[str, float]:
        """Le score d'une section : le meilleur de ses passages, plus un bonus de type si la
        question demande une valeur (un tableau ou du code porte les valeurs)."""
        demande_valeur = bool(RE_VALEUR.search(self.question) or RE_DATE.search(self.question))
        scores: dict[str, float] = {}
        for i, p in enumerate(self.passages):
            s = self.scores[i]
            if demande_valeur and p["type"] in ("tableau", "code", "liste"):
                s *= 1.15
            scores[p["section"]] = max(scores.get(p["section"], 0.0), s)
        return dict(sorted(scores.items(), key=lambda kv: (-kv[1], kv[0])))

    def lecture(self, classement: dict[str, float], part_max: float = 0.8) -> None:
        """Lire les PASSAGES dans l'ordre du score — pas les sections entières. Une section
        coûte trop cher pour un budget de 30 % ; une phrase coûte ce qu'elle vaut. On garde
        20 % du budget pour le balayage et la relecture."""
        if not self.scores or max(self.scores) <= 0:
            self.raison = "aucun passage ne répond à la question"
            return
        meilleur = max(self.scores)
        for i in sorted(range(len(self.passages)), key=lambda k: (-self.scores[k], k)):
            if self.reste() <= 0 or self.cout >= self.budget * part_max:
                self.raison = "part de budget de lecture atteinte"
                break
            if self.scores[i] < meilleur * 0.10:
                self.raison = "score marginal trop bas"
                break
            self._lire([i], "lecture", f"score {self.scores[i]:.2f}")

    def balayage(self) -> None:
        """La question demande une valeur précise (un nombre, une date, un nom) : on balaie
        le texte pour elle, et on ne paie que les passages qui la portent."""
        motif = RE_DATE.search(self.question)
        if motif:
            for i, p in enumerate(self.passages):
                if i in self.lus or self.reste() <= 0:
                    continue
                if RE_DATE.search(p["texte"]):
                    self._lire([i], "balayage", "date trouvée")
        elif RE_VALEUR.search(self.question):
            for i, p in enumerate(self.passages):
                if i in self.lus or self.reste() <= 0:
                    continue
                if re.search(r"\b\d", p["texte"]):
                    self._lire([i], "balayage", "valeur trouvée")

    def relecture(self) -> None:
        """Si aucun passage lu ne répond, on relit le voisinage des meilleurs scores : la
        réponse est peut-être dans la phrase d'avant ou d'après."""
        if not self.lus or max(self.scores[i] for i in self.lus) > 0:
            return
        for section in list(self.classer())[:2]:
            indices = [i for i, p in enumerate(self.passages) if p["section"] == section]
            self._lire(indices, "relecture", "aucun score positif : voisinage")

    def lire_tout(self) -> dict:
        """La lecture INTÉGRALE : tout est lu, aucun choix. C'est la référence à laquelle la
        lecture contrôlée se compare — même lecteur, même question, tout le texte."""
        for i in range(len(self.passages)):
            self._lire([i], "lecture", "intégrale")
        self.raison = "lecture intégrale"
        return {
            "question": self.question, "budget_octets": self.budget, "cout_octets": self.cout,
            "part": round(self.cout / max(self.budget, 1), 3),
            "passages_lus": list(range(len(self.passages))), "evenements": self.evenements,
            "raison": self.raison,
        }

    def lire(self) -> dict:
        """La trajectoire complète. L'ordre des actions est la politique, et c'est elle que
        la porte mesure — pas le scoreur."""
        self.survol()
        classement = self.classer()
        self.lecture(classement)
        self.balayage()
        self.relecture()
        if not self.evenements:
            self.raison = "rien n'a pu être lu dans le budget"
        return {
            "question": self.question, "budget_octets": self.budget, "cout_octets": self.cout,
            "part": round(self.cout / max(self.budget, 1), 3),
            "passages_lus": self.lus, "evenements": self.evenements, "raison": self.raison,
        }


# ------------------------------------------------------------------- le lecteur

def repondre(passages_lus: list[dict], question: str, scores: list[float] | None = None) -> dict | None:
    """Le lecteur extractif : le passage qui répond le mieux à la question, avec sa
    citation. C'est le MÊME lecteur pour la lecture intégrale et pour la lecture contrôlée.

    `scores` est l'index du DOCUMENT ENTIER, calculé une fois : lire moins ne doit pas
    changer le modèle de la question, seulement ce qu'on peut choisir. Sans cette règle, le
    lecteur recalculait ses IDF sur le sous-ensemble lu et changeait d'avis — un artefact
    qui faisait croire à un échec du contrôleur."""
    if not passages_lus:
        return None
    if scores is None:
        scores = Index(passages_lus).scores(question)
        meilleur = max(range(len(scores)), key=lambda i: (scores[i], -i))
        choix = meilleur
    else:
        choix = max(range(len(passages_lus)),
                    key=lambda i: (scores[passages_lus[i]["indice"]], -i))
        if scores[passages_lus[choix]["indice"]] <= 0:
            return None
    p = passages_lus[choix]
    score = scores[p["indice"]] if scores is not None else scores[choix]
    return {"texte": p["texte"], "region": p["region"], "start": p["start"],
            "octets": p["octets"], "score": round(score, 3), "prov": p["prov"]}


def lire_document(chemin: pathlib.Path, question: str, budget: float = 1.0,
                  critere: str = "bm25") -> dict:
    m = graphe_document.manifeste(chemin)
    tous = passages(m)
    total = sum(p["octets"] for p in tous)
    controleur = Controleur(tous, question, max(int(total * budget), 1))
    trajectoire = controleur.lire_tout() if budget >= 1.0 else controleur.lire()
    lus = [tous[i] for i in trajectoire["passages_lus"]]
    return {"trajectoire": trajectoire, "reponse": repondre(lus, question),
            "total_octets": total, "lecture_integrale": budget >= 1.0}


def main() -> int:
    ap = argparse.ArgumentParser(description="R0.2 — le contrôleur de lecture.")
    ap.add_argument("--document", type=pathlib.Path)
    ap.add_argument("--manifeste", type=pathlib.Path)
    ap.add_argument("--question", required=True)
    ap.add_argument("--budget", type=float, default=0.3)
    ap.add_argument("--critere", choices=("bm25", "couverture"), default="bm25")
    args = ap.parse_args()
    if args.manifeste:
        m = json.loads(args.manifeste.read_text(encoding="utf-8"))
        tous = passages(m)
        total = sum(p["octets"] for p in tous)
        controleur = Controleur(tous, args.question, int(total * args.budget), critere=args.critere)
        t = controleur.lire()
        r = repondre([tous[i] for i in t["passages_lus"]], args.question)
    elif args.document:
        resultat = lire_document(args.document, args.question, args.budget, critere=args.critere)
        t, r = resultat["trajectoire"], resultat["reponse"]
    else:
        ap.error("--document ou --manifeste est requis")
    print(json.dumps({"trajectoire": t, "reponse": r}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
