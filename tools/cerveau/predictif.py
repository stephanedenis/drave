#!/usr/bin/env python3
"""M5 — codage prédictif : prédire une cible **variable**, mesurer l'erreur.

Leçon mesurée (sprint 24 h, corpus `sequences.corpus`) : l'ancienne cible
`action` est **structurellement constante** par jeu — `action()` dans
`universaux.py` classe le coup par la *forme* du code (présence de `de`/`vers`,
de `chemin`, de `case`…), pas par sa sémantique. Résultat : échecs = toujours
`deplacer`, dames = toujours `prendre`, morpion = toujours `jouer_case` ; seul go
varie (`poser` 92 %, `passer` 8 %). Prédire `action` ne peut donc pas battre la
classe majoritaire : le 98,9 % publié était le taux de cette constante.

Le module change de cible et mesure honnêtement :

- `action` — la cible historique, gardée comme témoin ;
- `source` — la case de départ (`de` aux échecs, `chemin_0` aux dames) ;
- `cible`  — la case d'arrivée (`vers`, dernier `chemin`, `point`, `case`).

Trois ordres de Markov (0 = marginale par jeu, 1 = pas précédent, 2 = deux pas),
avec **repli hiérarchique Dirichlet** pour que la surprisal reste calibrée même
quand un contexte est rare. On oppose au modèle la **baseline majoritaire** et
sa **surprisal marginale**, on décompose par jeu, et un **contrôle négatif par
permutation** des cibles (même marginale, structure détruite) vérifie que le
gain, s'il existe, n'est pas du bruit d'échantillonnage.

Le résultat attendu est un négatif net sur le *contenu* : les parties sont
générées par un tirage **uniforme parmi les coups légaux**, et le code observé
ne porte pas le plateau. Le seul gain réel est mécanique (alternance de trait,
case libérée) ; il est isolé par `baseline_tour` et par le plancher oracle de la
fiche. Voir `/tmp/a1-m5-m6.md` pour les chiffres.

Sprint A6 : le **plateau** (`Pas.contexte`, produit par `resume_contexte`) est
maintenant une observation du prédicteur. `contexte=True` restreint la loi aux
valeurs compatibles avec l'occupation observée (source = mes pièces ; cible =
cases non occupées par moi) et mélange cette loi temporelle masquée à
l'uniforme sur ces candidats (`melange`). Aucune règle de déplacement n'est
utilisée : le gain est celui de l'observation du plateau, l'écart restant à
l'oracle est la géométrie des coups. `permuter_contextes` est le contrôle
négatif (masque conservé, bon plateau détruit). Voir `/tmp/a6-m5-m6.md`.
"""
from __future__ import annotations

import collections
import dataclasses
import math
import random
import re

from .sequences import Sequence

# Champ du code qui porte la « source » du coup, quand il existe.
CHAMPS_SOURCE = {"echecs": "de", "dames": "chemin_0"}
CIBLES = ("action", "source", "cible")


def valeur(pas, cible: str = "cible"):
    """La valeur de la cible pour un pas (ou un code typé).

    `pas` peut être un `Pas` (attribut `.code`) ou directement le dictionnaire
    du code. Rend `None` quand la cible n'a pas de sens pour ce jeu (un go n'a
    pas de case de départ).
    """
    code = getattr(pas, "code", pas)
    if not isinstance(code, dict):
        raise TypeError("valeur attend un Pas ou un code typé (dict)")
    jeu = code.get("jeu")
    if cible == "action":
        return code.get("action")
    if cible == "source":
        champ = CHAMPS_SOURCE.get(jeu)
        return code.get(champ) if champ else None
    if cible == "cible":
        if jeu == "echecs":
            return code.get("vers")
        if jeu == "dames":
            for champ in ("chemin_2", "chemin_1", "chemin_0"):
                if code.get(champ) is not None:
                    return code[champ]
            return None
        if jeu == "go":
            return code.get("point")
        if jeu == "morpion":
            return code.get("case")
        return None
    raise ValueError(f"cible inconnue : {cible!r} (connues : {', '.join(CIBLES)})")


# ----------------------------------------------------------------------
# Le contexte de plateau (`resume_contexte`) : ce que le prédicteur voit.
# ----------------------------------------------------------------------
def _champ_contexte(contexte: str, nom: str) -> str | None:
    m = re.search(rf"(?:^| ){re.escape(nom)}=(\[[^\]]*\]|[^ ]*)", contexte)
    return m.group(1) if m else None


def plateau_contexte(contexte: str, jeu: str):
    """Décode `resume_contexte` en (occupants, trait), indexés comme les codes.

    Rend `(None, None)` si le contexte est vide ou d'un format inconnu. Les
    index sont ceux des champs `de`, `vers`, `point`, `case`, `chemin_*` : c'est
    la convention du corpus, pas une règle du jeu.
    """
    if not contexte:
        return None, None
    trait = _champ_contexte(contexte, "trait")
    if jeu == "echecs":
        fen = _champ_contexte(contexte, "plateau")
        if not fen:
            return None, None
        occ: list = []
        for ch in fen:
            if ch.isdigit():
                occ.extend(["."] * int(ch))
            elif ch != "/":
                occ.append(ch)
        return (occ if len(occ) == 64 else None), trait
    if jeu == "dames":
        cases = _champ_contexte(contexte, "cases")
        if not cases:
            return None, None
        occ = cases.split(",")
        return (occ if len(occ) == 32 else None), trait
    if jeu == "go":
        plat = _champ_contexte(contexte, "plateau")
        if not plat:
            return None, None
        try:
            occ = [int(x) for x in plat.strip("[]").replace(" ", "").split(",") if x]
        except ValueError:
            return None, None
        return (occ if len(occ) == 81 else None), trait
    if jeu == "morpion":
        cases = _champ_contexte(contexte, "cases")
        if not cases:
            return None, None
        occ = cases.split(",")
        return (occ if len(occ) == 9 else None), trait
    return None, None


def candidats_contexte(contexte: str, jeu: str, cible: str):
    """Les valeurs de `cible` compatibles avec le plateau, ou None.

    Le filtre est **purement observable** : pour `source`, les cases occupées
    par le trait (on ne peut déplacer que sa pièce) ; pour `cible`, les cases
    qui ne sont pas occupées par le trait (case vide, ou pièce adverse pour une
    prise). Aucune règle de déplacement n'est utilisée : la géométrie des coups
    reste inconnue, c'est ce que mesure l'écart à l'oracle.
    """
    occ, trait = plateau_contexte(contexte, jeu)
    if occ is None or trait is None:
        return None
    if jeu == "echecs":
        propres = set("PNBRQK") if trait == "w" else set("pnbrqk")
    elif jeu == "dames":
        propres = set("wW") if trait == "w" else set("bB")
    elif jeu == "go":
        propres = {trait}
    elif jeu == "morpion":
        propres = {trait}
    else:
        return None
    if cible == "source":
        return frozenset(i for i, o in enumerate(occ) if str(o) in propres)
    if cible == "cible":
        if jeu == "echecs":
            return frozenset(i for i, o in enumerate(occ) if str(o) not in propres)
        if jeu in ("dames", "morpion"):
            return frozenset(i for i, o in enumerate(occ) if o == ".")
        if jeu == "go":
            return frozenset(i for i, o in enumerate(occ) if o == 0)
    return None


def champ_cible(code: dict, cible: str) -> str | None:
    """Le nom du champ à permuter pour le contrôle négatif."""
    if cible == "action":
        return "action"
    if cible == "source":
        return CHAMPS_SOURCE.get(code.get("jeu"))
    if cible == "cible":
        jeu = code.get("jeu")
        if jeu == "echecs":
            return "vers"
        if jeu == "dames":
            return "chemin_2" if code.get("chemin_2") is not None else "chemin_1"
        if jeu == "go":
            return "point"
        if jeu == "morpion":
            return "case"
    return None


class Predictif:
    """Un prédicteur de Markov à repli hiérarchique, une cible à la fois.

    `cible` vaut par défaut `"cible"` (la case d'arrivée) pour ne plus publier
    le score trompeur de `action`. Passer `cible="action"` reproduit l'ancien
    comportement, et `ordres=…` via `mesurer`.
    """

    nom = "M5-predictif"

    def __init__(self, cible: str = "cible", ordre: int = 1, kappa: float = 10.0,
                 contexte: bool = False, melange: float = 0.5) -> None:
        if cible not in CIBLES:
            raise ValueError(f"cible inconnue : {cible!r}")
        if ordre not in (0, 1, 2):
            raise ValueError("ordre doit valoir 0, 1 ou 2")
        if not 0.0 <= melange <= 1.0:
            raise ValueError("melange doit être dans [0, 1]")
        self.cible = cible
        self.ordre = ordre
        self.kappa = float(kappa)
        self.contexte = bool(contexte)
        # Poids du modèle temporel masqué ; le reste va à l'uniforme sur les
        # candidats du plateau. melange=1 : Markov masqué pur ; 0 : uniforme.
        self.melange = float(melange)
        self.transitions = collections.defaultdict(collections.Counter)   # ordre 1
        self.transitions2 = collections.defaultdict(collections.Counter)  # ordre 2
        self.marginal = collections.defaultdict(collections.Counter)      # ordre 0
        self.valeurs = collections.defaultdict(set)

    # ------------------------------------------------------------------
    def entrainer(self, sequences) -> None:
        """Compte les transitions de la cible, par jeu et par ordre."""
        for seq in sequences:
            pas = seq.pas
            for i in range(len(pas) - 1):
                a, b = pas[i], pas[i + 1]
                y = valeur(b, self.cible)
                cur = valeur(a, self.cible)
                if y is None or cur is None:
                    continue
                jeu = b.jeu
                self.marginal[jeu][y] += 1
                self.valeurs[jeu].add(y)
                self.transitions[(jeu, cur)][y] += 1
                if i >= 1:
                    prev = valeur(pas[i - 1], self.cible)
                    if prev is not None:
                        self.transitions2[(jeu, prev, cur)][y] += 1

    # ------------------------------------------------------------------
    def distribution(self, jeu: str, cur=None, precedent=None, contexte=None) -> dict:
        """La loi prédictive de la cible, lissée à chaque niveau.

        Du plus spécifique au plus général : ordre 2 → ordre 1 → marginale du
        jeu. Chaque niveau est interpolé avec `kappa` pseudo-comptes du niveau
        inférieur, ce qui garantit une probabilité non nulle partout.

        Si `contexte` est fourni et que le mode contexte est actif, la loi est
        restreinte aux valeurs **observables** du plateau (`candidats_contexte`)
        puis mélangée à l'uniforme sur ces candidats (`melange`). Le masque est
        appliqué après le repli : une valeur absente du plateau ne peut pas être
        prédite, même si elle est fréquente à l'entraînement.
        """
        valeurs = sorted(self.valeurs.get(jeu, ()))
        if not valeurs:
            return {}
        v = len(valeurs)
        p0 = self.marginal.get(jeu, collections.Counter())
        total0 = sum(p0.values()) or 1
        dist = {x: (p0[x] + self.kappa / v) / (total0 + self.kappa) for x in valeurs}
        if self.ordre >= 1 and cur is not None and (jeu, cur) in self.transitions:
            c = self.transitions[(jeu, cur)]
            total = sum(c.values())
            dist = {x: (c[x] + self.kappa * dist[x]) / (total + self.kappa) for x in valeurs}
        if self.ordre >= 2 and cur is not None and precedent is not None \
                and (jeu, precedent, cur) in self.transitions2:
            c = self.transitions2[(jeu, precedent, cur)]
            total = sum(c.values())
            dist = {x: (c[x] + self.kappa * dist[x]) / (total + self.kappa) for x in valeurs}
        if not self.contexte or not contexte:
            return dist
        cand = candidats_contexte(contexte, jeu, self.cible)
        if not cand:
            return dist
        z = sum(dist.get(x, 0.0) for x in cand)
        if z > 0:
            hist = {x: dist.get(x, 0.0) / z for x in cand}
        else:
            hist = {x: 1.0 / len(cand) for x in cand}
        if self.melange >= 1.0:
            masque = hist
        else:
            uniforme = 1.0 / len(cand)
            masque = {x: self.melange * hist[x] + (1.0 - self.melange) * uniforme
                      for x in cand}
        # Le masque est une croyance, pas une certitude : une petite fuite vers
        # la loi non masquée garde une probabilité finie à une cible que le
        # plateau contredit (utile au contrôle par permutation des contextes).
        fuite = 1e-6
        return {x: (1.0 - fuite) * masque.get(x, 0.0) + fuite * dist.get(x, 0.0)
                for x in set(masque) | set(dist)}

    def _choix(self, dist, jeu: str, contexte=None):
        """Argmax de la loi, restreint au masque quand il est actif.

        Le masque définit le support de la prédiction ; la petite fuite qui
        garde une probabilité finie à une cible contredite ne doit pas décider
        de l'argmax. À égalité (masque uniforme), l'ordre des valeurs tranche.
        """
        if self.contexte and contexte:
            cand = candidats_contexte(contexte, jeu, self.cible)
            if cand:
                return max(sorted(cand), key=lambda x: dist.get(x, 0.0))
        return max(dist, key=dist.get)

    def predire(self, code: dict, precedent=None, contexte=None) -> tuple:
        """Rend (valeur prédite, probabilité). `precedent` est une valeur de cible."""
        jeu = code.get("jeu")
        cur = valeur(code, self.cible)
        dist = self.distribution(jeu, cur, precedent, contexte)
        if not dist:
            return None, 0.0
        choix = self._choix(dist, jeu, contexte)
        return choix, dist[choix]

    # ------------------------------------------------------------------
    def evaluer(self, sequences) -> dict:
        """Exactitude, baseline majoritaire, surprisal et n sur des séquences.

        Ne prédit que les pas 1..n-1 : le premier pas n'a pas de passé. Les pas
        dont la cible est absente (source d'un go) sont ignorés.
        """
        n = ok = base = hors_vocab = 0
        surprise: list[float] = []
        surprise_base: list[float] = []
        for seq in sequences:
            pas = seq.pas
            for i in range(1, len(pas)):
                b = pas[i]
                y = valeur(b, self.cible)
                cur = valeur(pas[i - 1], self.cible)
                if y is None or cur is None:
                    continue
                jeu = b.jeu
                precedent = valeur(pas[i - 2], self.cible) if i >= 2 else None
                dist = self.distribution(jeu, cur, precedent,
                                         getattr(b, "contexte", None))
                if not dist:
                    continue
                if y not in dist or dist.get(y, 0.0) <= 0.0:
                    # valeur de test jamais vue à l'entraînement : hors vocabulaire
                    hors_vocab += 1
                    continue
                n += 1
                ok += int(self._choix(dist, jeu, getattr(b, "contexte", None)) == y)
                surprise.append(-math.log(dist[y]))
                p0 = self.marginal.get(jeu, collections.Counter())
                total0 = sum(p0.values()) or 1
                v = len(self.valeurs[jeu])
                p_base = (p0[y] + self.kappa / v) / (total0 + self.kappa)
                surprise_base.append(-math.log(p_base))
                base += int(max(sorted(p0), key=p0.get) == y)
        if n == 0:
            return {"exact": 0.0, "majoritaire": 0.0, "surprise": 0.0,
                    "surprise_majoritaire": 0.0, "gain": 0.0, "gain_surprise": 0.0,
                    "n": 0, "hors_vocabulaire": hors_vocab,
                    "cible": self.cible, "ordre": self.ordre}
        exact = ok / n
        maj = base / n
        sur = sum(surprise) / n
        sur_base = sum(surprise_base) / n
        return {"exact": exact, "majoritaire": maj, "surprise": sur,
                "surprise_majoritaire": sur_base,
                "gain": exact - maj, "gain_surprise": sur_base - sur,
                "n": n, "hors_vocabulaire": hors_vocab,
                "cible": self.cible, "ordre": self.ordre}

    # ------------------------------------------------------------------
    def mesurer(self, sequences, cibles=CIBLES, ordres=(0, 1, 2),
                graine: int = 3, fraction: float = 0.8, par_jeu: bool = True) -> dict:
        """Le protocole complet : split par partie, tous ordres, par jeu.

        Le split est **par partie** (aucun pas d'une partie de test n'a servi à
        l'entraînement), identique pour toutes les cibles et tous les ordres.
        """
        idx = list(range(len(sequences)))
        random.Random(graine).shuffle(idx)
        n_train = int(len(idx) * fraction)
        train = [sequences[i] for i in idx[:n_train]]
        test = [sequences[i] for i in idx[n_train:]]
        out = {"graine": graine, "fraction": fraction,
               "n_sequences_train": len(train), "n_sequences_test": len(test),
               "cibles": {}}
        for cible in cibles:
            res_cible = {}
            for ordre in ordres:
                m = Predictif(cible, ordre, contexte=self.contexte,
                              melange=self.melange)
                m.entrainer(train)
                r = m.evaluer(test)
                if par_jeu:
                    r["par_jeu"] = {}
                    for jeu in sorted({s.jeu for s in test}):
                        sous = [s for s in test if s.jeu == jeu]
                        rr = m.evaluer(sous)
                        if rr["n"]:
                            r["par_jeu"][jeu] = rr
                res_cible[f"ordre_{ordre}"] = r
            out["cibles"][cible] = res_cible
        return out

    # ------------------------------------------------------------------
    def diagnostic(self, sequences, cibles=CIBLES) -> dict:
        """Pourquoi une cible ne peut pas être prédite : sa dispersion.

        Rend, par jeu et par cible, le nombre de pas, de valeurs distinctes, le
        taux de la classe majoritaire et l'entropie (nats). Une cible à une
        seule valeur a une entropie nulle : aucun modèle ne peut la battre.
        """
        out = {}
        for cible in cibles:
            par_jeu = {}
            for jeu in sorted({s.jeu for s in sequences}):
                c = collections.Counter()
                n = 0
                for s in sequences:
                    if s.jeu != jeu:
                        continue
                    for pas in s.pas:
                        y = valeur(pas, cible)
                        if y is None:
                            continue
                        n += 1
                        c[y] += 1
                if not n:
                    continue
                total = sum(c.values())
                entropie = -sum((k / total) * math.log(k / total) for k in c.values())
                par_jeu[jeu] = {"n": n, "distincts": len(c),
                                "majoritaire": c.most_common(1)[0][1] / total,
                                "entropie": entropie}
            out[cible] = par_jeu
        return out


# ----------------------------------------------------------------------
# Baseline « tour » : la seule structure mécanique des parties aléatoires.
# ----------------------------------------------------------------------
def baseline_tour(sequences_train, sequences_test, cible: str = "cible") -> dict:
    """Majorité conditionnée par (jeu, parité du pas).

    Sert à décomposer le gain du Markov : si le modèle ne fait pas mieux que
    cette baseline, il n'a appris que l'alternance de trait (une règle du jeu),
    pas le contenu des coups.
    """
    comptes = collections.defaultdict(collections.Counter)
    connus = set()
    for seq in sequences_train:
        for i, pas in enumerate(seq.pas):
            y = valeur(pas, cible)
            if y is not None:
                comptes[(pas.jeu, i % 2)][y] += 1
                connus.add((pas.jeu, y))
    n = ok = 0
    for seq in sequences_test:
        for i in range(1, len(seq.pas)):
            pas = seq.pas[i]
            y = valeur(pas, cible)
            if y is None or valeur(seq.pas[i - 1], cible) is None:
                continue
            if (pas.jeu, y) not in connus:
                continue
            c = comptes.get((pas.jeu, i % 2))
            if not c:
                continue
            n += 1
            ok += int(max(sorted(c), key=c.get) == y)
    return {"n": n, "exact": ok / n if n else 0.0, "cible": cible}


# ----------------------------------------------------------------------
# Contrôle négatif : même marginale, structure détruite.
# ----------------------------------------------------------------------
def permuter(sequences, cible: str = "cible", graine: int = 0):
    """Permute les valeurs de la cible entre pas d'un même jeu.

    La marginale et le découpage sont conservés ; seule la liaison
    pas_précédent → pas_suivant est détruite. C'est le null du test.
    """
    rng = random.Random(graine)
    positions = collections.defaultdict(list)
    for si, seq in enumerate(sequences):
        for pi, pas in enumerate(seq.pas):
            champ = champ_cible(pas.code, cible)
            if champ is not None and pas.code.get(champ) is not None:
                positions[seq.jeu].append((si, pi, champ))
    remplacements: dict[tuple[int, int], tuple[str, object]] = {}
    for jeu, pos in positions.items():
        valeurs = [sequences[si].pas[pi].code[champ] for si, pi, champ in pos]
        rng.shuffle(valeurs)
        for (si, pi, champ), v in zip(pos, valeurs):
            remplacements[(si, pi)] = (champ, v)
    out = []
    for si, seq in enumerate(sequences):
        pas_out = []
        for pi, pas in enumerate(seq.pas):
            remplacement = remplacements.get((si, pi))
            if remplacement is None:
                pas_out.append(pas)
                continue
            champ, v = remplacement
            code = dict(pas.code)
            code[champ] = v
            pas_out.append(dataclasses.replace(pas, code=code))
        out.append(Sequence(seq.jeu, tuple(pas_out)))
    return out


def permuter_contextes(sequences, graine: int = 0):
    """Permute les contextes entre pas d'un même jeu : le masque devient faux.

    Contrôle négatif du gain de plateau. La distribution des contextes (donc
    des masques) est conservée, mais chaque pas reçoit le plateau d'un autre
    pas : si le gain vient du **bon** contexte, il doit disparaître.
    """
    rng = random.Random(graine)
    positions = collections.defaultdict(list)
    for si, seq in enumerate(sequences):
        for pi in range(len(seq.pas)):
            positions[seq.jeu].append((si, pi))
    remplacements: dict[tuple[int, int], str] = {}
    for jeu, pos in positions.items():
        ctxs = [sequences[si].pas[pi].contexte for si, pi in pos]
        rng.shuffle(ctxs)
        for (si, pi), ctx in zip(pos, ctxs):
            remplacements[(si, pi)] = ctx
    out = []
    for si, seq in enumerate(sequences):
        pas_out = []
        for pi, pas in enumerate(seq.pas):
            pas_out.append(dataclasses.replace(pas, contexte=remplacements[(si, pi)]))
        out.append(Sequence(seq.jeu, tuple(pas_out)))
    return out


def controle_negatif(sequences_train, sequences_test, cible: str = "cible",
                     ordre: int = 1, permutations: int = 20,
                     graine: int = 0) -> dict:
    """Le gain observé dépasse-t-il le null de permutation des cibles ?

    On mélange les cibles de l'ensemble **entier** (train + test) par jeu, puis
    on refait le même split et le même entraînement. Si le gain observé est dans
    la distribution des gains permutés, il n'y a pas de structure séquentielle
    apprise : c'est le résultat négatif.
    """
    m = Predictif(cible, ordre)
    m.entrainer(list(sequences_train))
    observe = m.evaluer(list(sequences_test))
    toutes = list(sequences_train) + list(sequences_test)
    gains, gains_surprise = [], []
    for k in range(permutations):
        melange = permuter(toutes, cible, graine + k)
        train_p = melange[:len(sequences_train)]
        test_p = melange[len(sequences_train):]
        mp = Predictif(cible, ordre)
        mp.entrainer(train_p)
        rp = mp.evaluer(test_p)
        gains.append(rp["gain"])
        gains_surprise.append(rp["gain_surprise"])
    n = len(gains)
    moyenne = sum(gains) / n if n else 0.0
    variance = sum((g - moyenne) ** 2 for g in gains) / n if n else 0.0
    p_value = sum(g >= observe["gain"] for g in gains) / n if n else 1.0
    p_surprise = sum(g >= observe["gain_surprise"] for g in gains_surprise) / n if n else 1.0
    return {"cible": cible, "ordre": ordre, "permutations": n,
            "gain_observe": observe["gain"],
            "gain_surprise_observe": observe["gain_surprise"],
            "gain_null_moyen": moyenne, "gain_null_ecart": math.sqrt(variance),
            "gain_surprise_null_moyen": sum(gains_surprise) / n if n else 0.0,
            "p_value_gain": p_value, "p_value_gain_surprise": p_surprise}
