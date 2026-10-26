#!/usr/bin/env python3
"""mesure.py — le banc des jeux : couches, contrôles, puis pensée.

Deux séries, dans l'ordre du contrat :

1. **les couches linguistiques** — couverture par niveau (0→4), invariance
   entre surfaces équivalentes, non-collision des surfaces différentes,
   restitution, compactage, vitesse, contrôle par permutation du lexique et
   contrôle par étiquettes mélangées ;
2. **la pensée** — la logique de chaque jeu, mesurée par ses règles (perft,
   captures, ko), par sa force (morpion exact, MCTS, politique des cartes) et
   par son **invariance** : la même position écrite de plusieurs façons doit
   produire la même décision.

Le mode `--rapide` est celui de la porte : il garde les contrôles et les
mesures peu coûteuses. Le mode complet ajoute les perfts profonds et les
parties (MCTS, dames) ; il écrit `reports/jeux-mesures.json`.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import sys
import time
from collections import defaultdict

from .corpus import Corpus, construire_corpus
from .codecs import lit, rend
from .codecs.base import detecte_jeu
from .rsn import RSN
from .regles import cartes as C
from .regles import dames as D
from .regles import echecs as E
from .regles import go as G
from .regles import morpion as M


# ---------------------------------------------------------------------------
# 1. Les couches linguistiques
# ---------------------------------------------------------------------------
def _lecture(corpus: Corpus, niveau: int, item) -> RSN | None:
    lec = lit(item.texte, jeu=item.jeu, niveau=niveau, contexte=item.contexte)
    if lec.ok and lec.rsn is not None and lec.rsn.corps == item.attendu.corps:
        return lec.rsn
    return None


def couverture(corpus: Corpus, niveau: int) -> dict:
    total = len(corpus.items)
    bons = 0
    par_jeu: dict[str, int] = defaultdict(int)
    tot_jeu: dict[str, int] = defaultdict(int)
    for it in corpus.items:
        tot_jeu[it.jeu] += 1
        if _lecture(corpus, niveau, it) is not None:
            bons += 1
            par_jeu[it.jeu] += 1
    return {"niveau": niveau, "bons": bons, "total": total,
            "taux": round(bons / total, 4) if total else 0.0,
            "par_jeu": {j: {"bons": par_jeu[j], "total": tot_jeu[j]} for j in sorted(tot_jeu)}}


def mesure_couverture(corpus: Corpus) -> dict:
    return {str(n): couverture(corpus, n) for n in range(5)}


def invariance(corpus: Corpus, niveau: int) -> dict:
    paires: dict[str, list] = defaultdict(list)
    for it in corpus.items:
        if it.paire:
            paires[it.paire].append(it)
    bonnes = 0
    detail = {}
    for nom, items in sorted(paires.items()):
        hs = []
        for it in items:
            r = _lecture(corpus, niveau, it)
            hs.append(r.empreinte() if r is not None else None)
        ok = len(set(hs)) == 1 and hs[0] is not None
        bonnes += 1 if ok else 0
        detail[nom] = {"ok": ok, "n": len(items)}
    return {"niveau": niveau, "bonnes": bonnes, "total": len(paires),
            "taux": round(bonnes / len(paires), 4) if paires else 0.0, "detail": detail}


def mesure_invariance(corpus: Corpus) -> dict:
    return {str(n): invariance(corpus, n) for n in range(5)}


def collisions(corpus: Corpus, niveau: int = 4) -> dict:
    groupes: dict[str, list] = defaultdict(list)
    for it in corpus.items:
        if it.contre:
            groupes[it.contre].append(it)
    collisions_ = 0
    detail = {}
    for nom, items in sorted(groupes.items()):
        hs = []
        for it in items:
            r = _lecture(corpus, niveau, it)
            hs.append(r.empreinte() if r is not None else None)
        collision = len(set(hs)) == 1 and hs[0] is not None
        collisions_ += 1 if collision else 0
        detail[nom] = {"collision": collision, "n": len(items)}
    return {"niveau": niveau, "collisions": collisions_, "total": len(groupes),
            "detail": detail}


def _modules_lexique():
    # importés ici pour que la permutation puisse être posée/retirée proprement
    import jeux.codecs.cartes as CC
    import jeux.codecs.dames as CD
    import jeux.codecs.echecs as CE
    import jeux.codecs.morpion as CM
    return (CM, CE, CD, CC)


def controle_lexique(corpus: Corpus, niveau: int = 4) -> dict:
    from .lexique import LEX

    modules = _modules_lexique()
    base = couverture(corpus, niveau)
    perm = LEX
    for domaine in ("morpion.case", "morpion.symbole", "echecs.piece", "echecs.roque",
                    "dames.piece", "cartes.rang", "cartes.couleur", "go.passe"):
        perm = perm.permute(domaine, 1)
    anciens = [m.LEX for m in modules]
    try:
        for m in modules:
            m.LEX = perm
        apres = couverture(corpus, niveau)
    finally:
        for m, old in zip(modules, anciens):
            m.LEX = old
    return {"base": base["bons"], "permute": apres["bons"], "perdus": base["bons"] - apres["bons"],
            "taux_base": base["taux"], "taux_permute": apres["taux"]}


def controle_etiquettes(corpus: Corpus, niveau: int = 4, graine: int = 20261025) -> dict:
    rng = random.Random(graine)
    attendus = [it.attendu for it in corpus.items]
    rng.shuffle(attendus)
    bons = 0
    for it, att in zip(corpus.items, attendus):
        lec = lit(it.texte, jeu=it.jeu, niveau=niveau, contexte=it.contexte)
        if lec.ok and lec.rsn is not None and lec.rsn.corps == att.corps:
            bons += 1
    return {"bons": bons, "total": len(corpus.items),
            "taux": round(bons / len(corpus.items), 4) if corpus.items else 0.0}


_FORMAT_RESTITUTION = {
    "morpion": {"etat": "grille", "coup": "texte", "partie": "liste"},
    "echecs": {"etat": "fen", "coup": "uci", "partie": "pgn"},
    "dames": {"etat": "compact", "coup": "numerique", "partie": "liste"},
    "go": {"etat": "diagramme", "coup": "gtp", "partie": "sgf"},
    "cartes": {"etat": "donne", "coup": "carte", "main": "liste", "partie": "liste"},
}


def restitution(corpus: Corpus) -> dict:
    bons = 0
    total = 0
    echecs = []
    for it in corpus.items:
        fmt = _FORMAT_RESTITUTION.get(it.jeu, {}).get(it.nature)
        if not fmt:
            continue
        total += 1
        try:
            surface = rend(it.attendu, fmt, contexte=it.contexte)
            lec = lit(surface, jeu=it.jeu, niveau=4, contexte=it.contexte)
            ok = lec.ok and lec.rsn is not None and lec.rsn.empreinte() == it.attendu.empreinte()
        except Exception as e:
            ok = False
            surface = f"<{e}>"
        if ok:
            bons += 1
        else:
            echecs.append({"jeu": it.jeu, "nature": it.nature, "format": fmt,
                           "surface": surface, "texte": it.texte})
    return {"bons": bons, "total": total,
            "taux": round(bons / total, 4) if total else 0.0, "echecs": echecs[:10]}


def _perturbe(rsn: RSN) -> RSN:
    c = dict(rsn.corps)
    if rsn.nature == "etat":
        if rsn.jeu == "morpion":
            # le trait du morpion est DÉRIVÉ des comptes : on perturbe par un
            # coup valide (une case vide reçoit le trait), pas par un trait
            # impossible que la grille ne peut pas porter.
            cases = list(c.get("cases", []))
            if None in cases:
                i = cases.index(None)
                cases[i] = c.get("trait", "X")
                c["cases"] = cases
                c["trait"] = "O" if c.get("trait") == "X" else "X"
            else:
                c["cases"] = [("O" if x == "X" else "X") if x else x for x in cases]
        elif rsn.jeu == "echecs":
            c["trait"] = "b" if c.get("trait") == "w" else "w"
        elif rsn.jeu == "dames":
            c["trait"] = "w" if c.get("trait") == "b" else "b"
        elif rsn.jeu == "go":
            c["trait"] = 2 if c.get("trait") == 1 else 1
        elif rsn.jeu == "cartes":
            c["tour"] = (int(c.get("tour", 0)) + 1) % 4
    elif rsn.nature == "coup":
        if rsn.jeu == "morpion":
            c["case"] = (int(c["case"]) + 1) % 9
        elif rsn.jeu == "echecs":
            c["vers"] = (int(c["vers"]) + 8) % 64
        elif rsn.jeu == "dames":
            c["chemin"] = list(c["chemin"]) + [int(c["chemin"][-1])]
        elif rsn.jeu == "go":
            if c.get("passe"):
                c = {"taille": c.get("taille", 9), "point": 0}
            else:
                c["point"] = (int(c["point"]) + 1) % (int(c.get("taille", 9)) ** 2)
        elif rsn.jeu == "cartes":
            c["carte"] = (int(c["carte"]) + 1) % 52
    elif rsn.nature == "main":
        c["cartes"] = [int(c["cartes"][0]) + 1 if c.get("cartes") else 0] + list(c.get("cartes", []))[1:]
    elif rsn.nature == "partie" and c.get("coups"):
        if rsn.jeu == "morpion":
            c["coups"] = [(int(c["coups"][0]) + 1) % 9] + list(c["coups"][1:])
        else:
            premier = dict(c["coups"][0])
            if rsn.jeu == "echecs":
                c["coups"] = [dict(premier, de=(int(premier["de"]) + 8) % 64)] + list(c["coups"][1:])
            elif rsn.jeu == "go":
                n = int(premier.get("taille", 9))
                c["coups"] = [dict(premier, point=(int(premier["point"]) + 1) % (n * n))] + list(c["coups"][1:])
            elif rsn.jeu == "dames":
                c["coups"] = [dict(premier, chemin=list(premier["chemin"]) + [int(premier["chemin"][-1])])] + list(c["coups"][1:])
    return rsn.avec(corps=c)


def restitution_negative(corpus: Corpus) -> dict:
    """La perturbation sémantique doit survivre au rendu/relu."""
    detectees = 0
    total = 0
    for it in corpus.items:
        fmt = _FORMAT_RESTITUTION.get(it.jeu, {}).get(it.nature)
        if not fmt:
            continue
        total += 1
        perturbe = _perturbe(it.attendu)
        if perturbe.empreinte() == it.attendu.empreinte():
            continue
        try:
            surface = rend(perturbe, fmt, contexte=it.contexte)
            lec = lit(surface, jeu=it.jeu, niveau=4, contexte=it.contexte)
            detectee = (not lec.ok or lec.rsn is None
                        or lec.rsn.empreinte() != it.attendu.empreinte())
        except Exception:
            detectee = True
        detectees += 1 if detectee else 0
    return {"detectees": detectees, "total": total,
            "taux": round(detectees / total, 4) if total else 0.0}


def compacite(corpus: Corpus) -> dict:
    vus = set()
    js, bi = [], []
    for it in corpus.items:
        h = it.attendu.empreinte()
        if h in vus:
            continue
        vus.add(h)
        js.append(len(it.attendu.octets_json()))
        bi.append(len(it.attendu.octets_binaire()))
    return {"objets": len(vus),
            "json_moyen": round(sum(js) / len(js), 2) if js else 0,
            "binaire_moyen": round(sum(bi) / len(bi), 2) if bi else 0,
            "ratio": round(sum(bi) / sum(js), 4) if js else 0.0}


def vitesse(corpus: Corpus, niveau: int = 4) -> dict:
    t0 = time.perf_counter()
    for it in corpus.items:
        lit(it.texte, jeu=it.jeu, niveau=niveau, contexte=it.contexte)
    dt = time.perf_counter() - t0
    return {"niveau": niveau, "secondes": round(dt, 4),
            "par_seconde": round(len(corpus.items) / dt, 1) if dt else 0.0}


def detection(corpus: Corpus) -> dict:
    bons = 0
    ambigu = 0
    detail = []
    for it in corpus.items:
        j, s = detecte_jeu(it.texte)
        ok = j == it.jeu
        bons += 1 if ok else 0
        if not ok:
            detail.append({"jeu": it.jeu, "detecte": j, "score": round(s, 3),
                           "texte": it.texte[:60]})
    return {"bons": bons, "total": len(corpus.items),
            "taux": round(bons / len(corpus.items), 4),
            "echecs": detail[:20]}


def mesure_couches(corpus: Corpus) -> dict:
    return {
        "corpus": {"items": len(corpus.items),
                   "par_jeu": {j: len(v) for j, v in corpus.par_jeu().items()}},
        "couverture": mesure_couverture(corpus),
        "invariance": mesure_invariance(corpus),
        "collisions": collisions(corpus, 4),
        "controle_lexique": controle_lexique(corpus, 4),
        "controle_etiquettes": controle_etiquettes(corpus, 4),
        "restitution": restitution(corpus),
        "restitution_negative": restitution_negative(corpus),
        "compacite": compacite(corpus),
        "vitesse": {"niveau4": vitesse(corpus, 4), "niveau0": vitesse(corpus, 0)},
        "detection": detection(corpus),
    }


# ---------------------------------------------------------------------------
# 2. La pensée (règles, force, invariance)
# ---------------------------------------------------------------------------
def _perft_echecs(profondeur_max: int) -> dict:
    refs = [
        ("depart", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
         [20, 400, 8902, 197281]),
        ("kiwipete", "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
         [48, 2039, 97862, 4085603]),
        ("p3", "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1",
         [14, 191, 2812, 43238]),
        ("p4", "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1",
         [6, 264, 9467, 422333]),
        ("p5", "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8",
         [44, 1486, 62379, 2103487]),
        ("p6", "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10",
         [46, 2079, 89890, 3894594]),
    ]
    out = []
    for nom, fen, attendus in refs:
        pos = E.Position.depuis_fen(fen)
        t0 = time.perf_counter()
        vals = [pos.perft(d) for d in range(1, profondeur_max + 1)]
        dt = time.perf_counter() - t0
        out.append({"position": nom, "profondeur": profondeur_max,
                    "valeurs": vals, "attendus": attendus[:profondeur_max],
                    "ok": vals == attendus[:profondeur_max],
                    "secondes": round(dt, 3)})
    return {"positions": out, "ok": all(x["ok"] for x in out)}


def _perft_dames(profondeur_max: int) -> dict:
    attendus = [7, 49, 302, 1469, 7361, 36768]
    pos = D.Position.depart()
    t0 = time.perf_counter()
    vals = [pos.perft(d) for d in range(1, profondeur_max + 1)]
    dt = time.perf_counter() - t0
    return {"profondeur": profondeur_max, "valeurs": vals,
            "attendus": attendus[:profondeur_max],
            "ok": vals == attendus[:profondeur_max], "secondes": round(dt, 3)}


def _morpion_mesures(nparties: int = 200) -> dict:
    vide = M.etat_initial()
    valeur, coup = M.resous(vide)
    valeur = 0.0 if valeur == 0 else valeur
    # parfait contre parfait
    etat = vide
    while not M.terminal(etat):
        _, c = M.resous(etat)
        etat = M.applique_indice(etat, c)
    parfait = M.resultat(etat)
    # exact contre hasard, des deux côtés
    rng = random.Random(1)
    non_perdues = 0
    for _ in range(nparties):
        etat = vide
        while not M.terminal(etat):
            if M.trait(etat) == "X":
                _, c = M.resous(etat)
            else:
                c = rng.choice([x.corps["case"] for x in M.coups_legaux(etat)])
            etat = M.applique_indice(etat, c)
        if M.resultat(etat) != "O":
            non_perdues += 1
    # gourmand (sans recherche) contre exact : le contrôle négatif
    from .pensee import coup_morpion_sans_recherche

    perdues = 0
    for _ in range(nparties):
        etat = vide
        while not M.terminal(etat):
            if M.trait(etat) == "X":
                c = coup_morpion_sans_recherche(etat).corps["case"]
            else:
                _, c = M.resous(etat)
            etat = M.applique_indice(etat, c)
        if M.resultat(etat) == "O":
            perdues += 1
    return {"valeur_vide": valeur, "parfait": parfait,
            "exact_vs_hasard_non_perdues": non_perdues, "exact_vs_hasard_total": nparties,
            "gourmand_vs_exact_perdues": perdues, "gourmand_vs_exact_total": nparties}


def _mates_echecs() -> dict:
    # positions vérifiées par le moteur : le trait est blanc, il y a un mat en 1
    positions = [
        "6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1",
        "7k/5Q2/6K1/8/8/8/8/8 w - - 0 1",
        "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 4 4",
    ]
    from .pensee import Budget, coup_echecs_sans_recherche, decide_echecs

    resultats = []
    for fen in positions:
        pos = E.Position.depuis_fen(fen)
        etat = E.rsn_depuis_position(pos)
        d = decide_echecs(etat, Budget(profondeur=3, temps_s=3.0))
        trouve = False
        if d.coup is not None:
            c = E.coup_depuis_action(d.coup, pos)
            u = pos.joue(c)
            trouve = (not pos.coups_legaux()) and pos.en_echec(pos.trait)
            pos.annule(u)
        statique = coup_echecs_sans_recherche(etat)
        mat_statique = False
        if statique is not None:
            c = E.coup_depuis_action(statique, pos)
            u = pos.joue(c)
            mat_statique = (not pos.coups_legaux()) and pos.en_echec(pos.trait)
            pos.annule(u)
        resultats.append({"fen": fen, "trouve": trouve, "statique": mat_statique,
                          "coup": d.coup.corps if d.coup else None,
                          "noeuds": d.noeuds})
    return {"positions": resultats, "trouves": sum(r["trouve"] for r in resultats),
            "total": len(resultats), "statiques": sum(r["statique"] for r in resultats)}


def _go_regles() -> dict:
    # 1. plateau vide 5×5 : 25 coups légaux
    vide = G.Position.depart(5, 0)
    n_vide = len(vide.coups_legaux())
    # 2. capture
    b = [0] * 25
    def I(r, c): return r * 5 + c
    b[I(2, 2)] = G.NOIR
    for r, c in ((1, 2), (3, 2), (2, 1)):
        b[I(r, c)] = G.BLANC
    cap = G.Position(5, b, G.BLANC, -1, 0, 0)
    cap_ok = cap.coup_legal(I(2, 3)) and cap.joue(I(2, 3)).plateau[I(2, 2)] == G.VIDE
    # 3. suicide
    b2 = [0] * 25
    for r, c in ((0, 1), (1, 0)):
        b2[I(r, c)] = G.BLANC
    suicide = G.Position(5, b2, G.NOIR, -1, 0, 0)
    suicide_ok = not suicide.coup_legal(I(0, 0))
    # 4. ko
    b3 = [0] * 16
    def J(r, c): return r * 4 + c
    for r, c in ((0, 1), (1, 0), (2, 1)):
        b3[J(r, c)] = G.NOIR
    for r, c in ((0, 2), (1, 1), (1, 3), (2, 2)):
        b3[J(r, c)] = G.BLANC
    ko = G.Position(4, b3, G.NOIR, -1, 0, 0)
    q = ko.joue(J(1, 2))
    ko_ok = (q.ko == J(1, 1)) and (not q.coup_legal(J(1, 1)))
    # 5. score connu : croix noire sur 3×3, 4 pierres + 5 points de territoire
    b4 = [0] * 9
    for r, c in ((0, 1), (1, 0), (1, 2), (2, 1)):
        b4[r * 3 + c] = G.NOIR
    sc = G.Position(3, b4, G.NOIR, -1, 0, 0)
    score_ok = sc.score() == (90, 0)
    return {"vide_legaux": n_vide, "vide_ok": n_vide == 25,
            "capture_ok": cap_ok, "suicide_ok": suicide_ok,
            "ko_ok": ko_ok, "score_ok": score_ok,
            "ok": n_vide == 25 and cap_ok and suicide_ok and ko_ok and score_ok}


def _partie_go(playouts: int, graine: int, maxplies: int = 60) -> G.Position:
    from .pensee import Budget, decide

    pos = G.Position.depart(5, 0)
    rng = random.Random(graine + 10000)
    for _ in range(maxplies):
        if pos.terminal():
            break
        if pos.trait == G.NOIR:
            d = decide(pos.vers_rsn(), Budget(playouts=playouts, temps_s=20, graine=graine))
            if d.coup is None:
                break
            if d.coup.corps.get("passe"):
                pos = pos.passe_tour()
            else:
                pos = pos.joue(int(d.coup.corps["point"]))
        else:
            coups = pos.coups_legaux()
            if coups and rng.random() < 0.95:
                pos = pos.joue(rng.choice(coups))
            else:
                pos = pos.passe_tour()
    return pos


def _go_force(parties: int, playouts: int) -> dict:
    gagnees = 0
    details = []
    t0 = time.perf_counter()
    for g in range(parties):
        p = _partie_go(playouts, g)
        d = p.difference()
        gagnees += 1 if d > 0 else 0
        details.append({"graine": g, "difference": d, "resultat": p.resultat()})
    return {"gagnees": gagnees, "total": parties, "taux": round(gagnees / parties, 4),
            "playouts": playouts, "secondes": round(time.perf_counter() - t0, 2),
            "details": details}


def _cartes_force(nparties: int) -> dict:
    from .pensee import decide_cartes

    def partie(graine, type_noir="politique", type_blanc="hasard"):
        pos = C.Position.depart(graine)
        rng = random.Random(graine + 50000)
        while not pos.terminal():
            if pos.tour % 2 == 0:
                if type_noir == "politique":
                    c = pos.politique()
                elif type_noir == "sans_partenaire":
                    c = _politique_sans_partenaire(pos)
                elif type_noir == "sans_atout":
                    c = _politique_sans_atout(pos)
                else:
                    c = rng.choice(pos.coups_legaux())
            else:
                if type_blanc == "politique":
                    c = pos.politique()
                else:
                    c = rng.choice(pos.coups_legaux())
            pos = pos.joue(c)
        return pos

    def taux(type_noir, type_blanc):
        g = 0
        for i in range(nparties):
            p = partie(i, type_noir, type_blanc)
            g += 1 if p.plis[0] > p.plis[1] else 0
        return round(g / nparties, 4)

    # contrôle : la légalité de la politique
    illegales = 0
    essais = 0
    for i in range(nparties):
        pos = C.Position.depart(i)
        while not pos.terminal():
            c = pos.politique()
            essais += 1
            if not pos.coup_legal(c):
                illegales += 1
            pos = pos.joue(c)
    return {"politique_vs_hasard": taux("politique", "hasard"),
            "hasard_vs_hasard": taux("hasard", "hasard"),
            "sans_partenaire_vs_hasard": taux("sans_partenaire", "hasard"),
            "sans_atout_vs_hasard": taux("sans_atout", "hasard"),
            "illegales": illegales, "essais": essais,
            "parties": nparties}


def _politique_sans_partenaire(pos: C.Position) -> int:
    legal = pos.coups_legaux()
    if len(legal) == 1:
        return legal[0]
    if not pos.pli:
        couleurs: dict[int, list[int]] = {}
        for c in legal:
            couleurs.setdefault(C.couleur(c), []).append(c)
        s = max(couleurs, key=lambda x: (len(couleurs[x]), -x))
        return max(couleurs[s], key=C.rang)
    gagnants = [c for c in legal if pos.gagne_avec(c)]
    if gagnants:
        return min(gagnants, key=C.rang)
    return min(legal, key=C.rang)


def _politique_sans_atout(pos: C.Position) -> int:
    q = C.Position([list(m) for m in pos.mains], -1, pos.donneur,
                   pos.entameur, pos.tour, pos.pli, pos.plis)
    return q.politique()


def _dames_regles() -> dict:
    # perft court + trois positions de prise
    p = D.Position.depart()
    perft = [p.perft(d) for d in (1, 2, 3, 4, 5, 6)]
    attendus = [7, 49, 302, 1469, 7361, 36768]
    # une prise simple : b6 prend c5 en d4
    cases = [D.VIDE] * 32
    cases[8] = D.NOIR_PION
    cases[13] = D.BLANC_PION
    cap = D.Position(cases, D.NOIR)
    cap_ok = any(c.chemin == (8, 17) for c in cap.coups_legaux())
    # prise multiple : b6xd4xf2
    cases2 = list(cases)
    cases2[22] = D.BLANC_PION
    multi = D.Position(cases2, D.NOIR)
    multi_ok = any(c.chemin == (8, 17, 26) for c in multi.coups_legaux())
    # promotion
    cases3 = [D.VIDE] * 32
    cases3[24] = D.NOIR_PION
    promo = D.Position(cases3, D.NOIR)
    promo_ok = any(c.chemin[-1] // 4 == 7 for c in promo.coups_legaux())
    return {"perft": perft, "attendus": attendus, "perft_ok": perft == attendus,
            "prise_ok": cap_ok, "prise_multiple_ok": multi_ok, "promotion_ok": promo_ok,
            "ok": perft == attendus and cap_ok and multi_ok and promo_ok}


def _cartes_regles() -> dict:
    # pli : le plus haut atout gagne ; à défaut, la plus haute carte demandée
    def mk(cards, atout):
        return C.Position([[], [], [], []], atout, 0, 0, 0,
                          [[i, c] for i, c in enumerate(cards)], [0, 0])
    w1 = mk([C.carte_id(10, 2), C.carte_id(13, 2), C.carte_id(2, 2), C.carte_id(3, 2)], -1)
    w2 = mk([C.carte_id(14, 2), C.carte_id(2, 0), C.carte_id(2, 3), C.carte_id(3, 3)], 3)
    return {"plus_haute_ok": w1.gagnant_pli() == 1,
            "atout_ok": w2.gagnant_pli() == 3,
            "ok": w1.gagnant_pli() == 1 and w2.gagnant_pli() == 3}


def _invariance_pensee(corpus: Corpus, rapide: bool) -> dict:
    from .pensee import Budget, decide

    # pour chaque jeu, plusieurs surfaces du même état
    cas = []
    vide_m = M.etat_initial()
    cas.append(("morpion", [(".../.../...", vide_m), (". . . | . . . | . . .", vide_m)],
                vide_m, Budget()))
    dep_e = E.rsn_depuis_position(E.Position.depart())
    diag_e = rend(dep_e, "diagramme")
    cas.append(("echecs", [(E.Position.depart().fen(), dep_e), (diag_e, dep_e)],
                dep_e, Budget(profondeur=2, temps_s=3)))
    dep_d = D.rsn_depuis_position(D.Position.depart())
    diag_d = rend(dep_d, "diagramme")
    cas.append(("dames", [("bbbbbbbbbbbb........wwwwwwwwwwww b", dep_d), (diag_d, dep_d)],
                dep_d, Budget(profondeur=3, temps_s=3)))
    vide_g = G.Position.depart(5, 0).vers_rsn()
    diag_g = rend(vide_g, "diagramme")
    cas.append(("go", [(diag_g, vide_g), (diag_g.replace("\n", "\n "), vide_g)],
                vide_g, Budget(playouts=30 if rapide else 200, temps_s=10, graine=7)))
    deal = C.rsn_depuis_position(C.Position.depart(42))
    donne = rend(deal, "donne")
    # variante : les cartes en toutes lettres
    variante = donne
    for j in range(4):
        for c in deal.corps["mains"][j]:
            variante = variante.replace(C.nom_court(c), C.nom_carte(c, "fr"))
    cas.append(("cartes", [(donne, deal), (variante, deal)], deal, Budget()))

    resultats = []
    for jeu, surfaces, etat, budget in cas:
        decisions = []
        for texte, _ in surfaces:
            lec = lit(texte, jeu=jeu, niveau=4, contexte=None if jeu == "cartes" else etat)
            if not lec.ok:
                decisions.append(None)
                continue
            d = decide(lec.rsn, budget)
            decisions.append(d.coup.empreinte() if d.coup else None)
        resultats.append({"jeu": jeu, "identiques": len(set(decisions)) == 1 and decisions[0] is not None,
                          "decisions": decisions})
    return {"cas": resultats, "identiques": sum(1 for r in resultats if r["identiques"]),
            "total": len(resultats)}


def _invariance_negative() -> dict:
    """Changer le trait doit changer l'état ET les coups légaux."""
    etats = {
        "morpion": M.etat_initial(),
        "echecs": E.rsn_depuis_position(E.Position.depart()),
        "dames": D.rsn_depuis_position(D.Position.depart()),
        "go": G.Position.depart(5, 0).vers_rsn(),
        "cartes": C.rsn_depuis_position(C.Position.depart(42)),
    }
    resultats = []
    for jeu, etat in etats.items():
        c = dict(etat.corps)
        if jeu == "morpion":
            c["trait"] = "O" if c["trait"] == "X" else "X"
        elif jeu == "echecs":
            c["trait"] = "b" if c["trait"] == "w" else "w"
        elif jeu == "dames":
            c["trait"] = "w" if c["trait"] == "b" else "b"
        elif jeu == "go":
            c["trait"] = 2 if c["trait"] == 1 else 1
        elif jeu == "cartes":
            c["tour"] = (int(c["tour"]) + 1) % 4
        autre = etat.avec(corps=c)
        resultats.append({"jeu": jeu, "etat_different": etat.empreinte() != autre.empreinte()})
    return {"cas": resultats, "differents": sum(1 for r in resultats if r["etat_different"]),
            "total": len(resultats)}


def mesure_pensee(rapide: bool = False) -> dict:
    n_parties_morpion = 100 if rapide else 200
    n_parties_cartes = 200 if rapide else 1000
    out = {
        "morpion": _morpion_mesures(n_parties_morpion),
        "echecs": {"perft": _perft_echecs(3 if rapide else 4), "mates": _mates_echecs()},
        "dames": {"regles": _dames_regles()},
        "go": {"regles": _go_regles()},
        "cartes": {"regles": _cartes_regles(), "force": _cartes_force(n_parties_cartes)},
        "invariance_pensee": _invariance_pensee(construire_corpus(), rapide),
        "invariance_negative": _invariance_negative(),
    }
    if not rapide:
        out["dames"]["force"] = _dames_force(20)
        out["go"]["force"] = _go_force(3, 60)
        out["echecs"]["auto_partie"] = _auto_partie_echecs()
    return out


def _auto_partie_echecs(nplis: int = 30) -> dict:
    from .pensee import Budget, decide_echecs

    pos = E.Position.depart()
    noeuds = 0
    for _ in range(nplis):
        if not pos.coups_legaux():
            break
        d = decide_echecs(E.rsn_depuis_position(pos), Budget(profondeur=2, temps_s=2))
        if d.coup is None:
            break
        c = E.coup_depuis_action(d.coup, pos)
        pos.joue(c)
        noeuds += d.noeuds
    return {"plis": nplis, "noeuds": noeuds, "final": pos.fen(),
            "ok": pos.rois[0] >= 0 and pos.rois[1] >= 0}


def _dames_force(nparties: int) -> dict:
    from .pensee import Budget, coup_dames_sans_recherche, decide_dames

    def partie(graine):
        pos = D.Position.depart()
        rng = random.Random(graine)
        for _ in range(80):
            if pos.terminal():
                break
            if pos.trait == D.NOIR:
                d = decide_dames(D.rsn_depuis_position(pos), Budget(profondeur=4, temps_s=2))
                if d.coup is None:
                    break
                c = D.coup_depuis_action(d.coup, pos)
            else:
                c = D.coup_depuis_action(coup_dames_sans_recherche(
                    D.rsn_depuis_position(pos)), pos)
            pos = pos.applique(c)
        # adjudication : matériel (dames 175, pions 100)
        def mat(coul):
            return sum(175 if p in (D.NOIR_DAME, D.BLANC_DAME) else 100
                       for p in pos.cases if D._couleur(p) == coul and p != D.VIDE)
        return mat(D.NOIR) > mat(D.BLANC)

    g = sum(1 for i in range(nparties) if partie(i))
    return {"gagnees": g, "total": nparties, "taux": round(g / nparties, 4)}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def verdict(mesures: dict, rapide: bool) -> tuple[bool, list[str]]:
    echecs = []
    c = mesures["couches"]
    if c["couverture"]["4"]["taux"] != 1.0:
        echecs.append(f"couverture niveau 4 : {c['couverture']['4']['taux']}")
    if c["invariance"]["4"]["taux"] != 1.0:
        echecs.append(f"invariance niveau 4 : {c['invariance']['4']['taux']}")
    if c["collisions"]["collisions"] != 0:
        echecs.append(f"collisions négatives : {c['collisions']['collisions']}")
    if c["restitution"]["taux"] != 1.0:
        echecs.append(f"restitution : {c['restitution']['taux']}")
    if c["restitution_negative"]["taux"] != 1.0:
        echecs.append(f"perturbation non détectée : {c['restitution_negative']['taux']}")
    if c["controle_lexique"]["perdus"] <= 0:
        echecs.append("le lexique ne porte plus (permutation sans effet)")
    if c["controle_etiquettes"]["taux"] >= 0.5:
        echecs.append("les étiquettes mélangées passent encore")
    if c["couverture"]["0"]["taux"] >= 0.9:
        echecs.append("le niveau 0 couvre presque tout : l'ablation ne prouve rien")
    if "pensee" not in mesures:
        return (not echecs), echecs
    m = mesures["pensee"]
    if m["morpion"]["valeur_vide"] != 0.0:
        echecs.append(f"morpion valeur vide : {m['morpion']['valeur_vide']}")
    if m["morpion"]["exact_vs_hasard_non_perdues"] != m["morpion"]["exact_vs_hasard_total"]:
        echecs.append("morpion exact vs hasard : une défaite")
    if m["echecs"]["perft"]["ok"] is not True:
        echecs.append("perft échecs")
    if m["dames"]["regles"]["ok"] is not True:
        echecs.append("règles dames")
    if m["go"]["regles"]["ok"] is not True:
        echecs.append("règles go")
    if m["cartes"]["regles"]["ok"] is not True:
        echecs.append("règles cartes")
    if m["cartes"]["force"]["illegales"] != 0:
        echecs.append("politique cartes illégale")
    if m["cartes"]["force"]["politique_vs_hasard"] <= 0.55:
        echecs.append(f"politique cartes faible : {m['cartes']['force']['politique_vs_hasard']}")
    if m["invariance_pensee"]["identiques"] != m["invariance_pensee"]["total"]:
        echecs.append("invariance de la pensée")
    if m["invariance_negative"]["differents"] != m["invariance_negative"]["total"]:
        echecs.append("contrôle négatif de la pensée")
    return (not echecs), echecs


def principal(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rapide", action="store_true",
                    help="contrôles et mesures courtes (porte)")
    ap.add_argument("--json", default=None,
                    help="écrire le JSON complet à ce chemin")
    ap.add_argument("--couches-seulement", action="store_true")
    a = ap.parse_args(argv)
    corpus = construire_corpus()
    t0 = time.perf_counter()
    mesures = {"date": "2026-10-25", "rapide": a.rapide,
               "couches": mesure_couches(corpus)}
    if not a.couches_seulement:
        mesures["pensee"] = mesure_pensee(a.rapide)
    mesures["secondes"] = round(time.perf_counter() - t0, 2)
    ok, echecs = verdict(mesures, a.rapide)
    mesures["verdict"] = {"ok": ok, "echecs": echecs}
    if a.json:
        pathlib.Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(a.json).write_text(json.dumps(mesures, ensure_ascii=False, indent=2),
                                        encoding="utf-8")
    c = mesures["couches"]
    print(f"  couverture : " + " · ".join(
        f"n{n} {c['couverture'][str(n)]['bons']}/{c['couverture'][str(n)]['total']}"
        for n in range(5)))
    print(f"  invariance : " + " · ".join(
        f"n{n} {c['invariance'][str(n)]['bonnes']}/{c['invariance'][str(n)]['total']}"
        for n in range(5)))
    print(f"  collisions : {c['collisions']['collisions']} · "
          f"restitution : {c['restitution']['bons']}/{c['restitution']['total']} · "
          f"perturbation : {c['restitution_negative']['taux']:.3f}")
    print(f"  lexique : {c['controle_lexique']['perdus']} items perdus · "
          f"étiquettes : {c['controle_etiquettes']['taux']:.3f} · "
          f"compacité : {c['compacite']['ratio']:.3f}")
    if "pensee" in mesures:
        m = mesures["pensee"]
        print(f"  morpion : vide {m['morpion']['valeur_vide']} · "
              f"exact/hasard {m['morpion']['exact_vs_hasard_non_perdues']}/"
              f"{m['morpion']['exact_vs_hasard_total']} · "
              f"gourmand perd {m['morpion']['gourmand_vs_exact_perdues']}")
        print(f"  échecs : perft {m['echecs']['perft']['ok']} · "
              f"mats {m['echecs']['mates']['trouves']}/{m['echecs']['mates']['total']} · "
              f"statiques {m['echecs']['mates']['statiques']}")
        print(f"  dames : {m['dames']['regles']['ok']} · "
              f"go : {m['go']['regles']['ok']} · "
              f"cartes : {m['cartes']['force']['politique_vs_hasard']:.3f} vs hasard")
        print(f"  pensée invariante : {m['invariance_pensee']['identiques']}/"
              f"{m['invariance_pensee']['total']} · "
              f"contrôle négatif : {m['invariance_negative']['differents']}/"
              f"{m['invariance_negative']['total']}")
        if "force" in m.get("go", {}):
            print(f"  go MCTS : {m['go']['force']['gagnees']}/{m['go']['force']['total']}")
        if "force" in m.get("dames", {}):
            print(f"  dames recherche : {m['dames']['force']['gagnees']}/{m['dames']['force']['total']}")
    print(f"  ({mesures['secondes']} s)")
    if not ok:
        print("  ❌ " + " ; ".join(echecs))
        return 1
    if a.couches_seulement:
        print("  ✅ couches : les contrôles tiennent")
    else:
        print("  ✅ couches et pensée : les contrôles tiennent")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
