#!/usr/bin/env python3
"""mesure_maitres.py — les principes des maîtres changent-ils la décision ?

Chaque mesure a un **contrôle** : la même recherche sans les principes. Ce n'est
pas une évaluation de force absolue (le moteur reste faible), c'est la réponse à
« le principe déplace-t-il le coup choisi, et dans le bon sens ? ».

- échecs : le premier coup (e4/d4/Nf3/c4 contre le coup du dépôt), le livre
  d'ouvertures, l'accord avec le coup du maître sur trois parties du domaine
  public, et les mats en un ;
- dames : maîtres contre sans-maîtres, même profondeur, 20 parties ;
- go : le premier coup (coin/côté) et une capture, avec et sans prior ;
- cartes : la politique du whist contre la politique du dépôt et contre le
  hasard, 1 000 donnes.
"""
from __future__ import annotations

import random
import time

from .codecs import lit
from .maitres import (LIVRE, PARTIES, PRINCIPES, SOURCES, cle_livre,
                      eval_dames_maitres, eval_echecs_maitres,
                      politique_cartes_maitres, prior_go)
from .pensee import Budget, decide_cartes, decide_dames, decide_echecs, decide_go
from .regles import cartes as C
from .regles import dames as D
from .regles import echecs as E
from .regles import go as G


# ---------------------------------------------------------------------------
# Échecs
# ---------------------------------------------------------------------------
def _positions_echecs(pgn: str):
    lec = lit(pgn, jeu="echecs", niveau=4)
    if not lec.ok:
        return None, None, lec.erreurs[:3]
    _, coups = E.partie_depuis_rsn(lec.rsn)
    pos = E.Position.depart()
    positions = []
    for c in coups:
        positions.append(pos.fen())
        pos.joue(c)
    return positions, coups, []


def _accord_parties(profondeur: int, temps: float, debut: int = 8) -> dict:
    total = 0
    avec = 0
    sans = 0
    details = []
    for partie in PARTIES:
        positions, coups, err = _positions_echecs(partie["pgn"])
        if positions is None:
            details.append({"nom": partie["nom"], "erreur": err})
            continue
        n = 0
        for i in range(debut, len(coups)):
            pos = E.Position.depuis_fen(positions[i])
            etat = E.rsn_depuis_position(pos)
            maître = coups[i].uci()
            for maitres in (False, True):
                d = decide_echecs(etat, Budget(profondeur=profondeur, temps_s=temps,
                                               maitres=maitres, graine=0))
                choisi = E.coup_depuis_action(d.coup).uci() if d.coup else None
                if maitres:
                    avec += int(choisi == maître)
                else:
                    sans += int(choisi == maître)
            total += 1
            n += 1
        details.append({"nom": partie["nom"], "positions": n,
                        "erreurs": err})
    return {"positions": total, "avec_maitres": avec, "sans_maitres": sans,
            "details": details}


def _suite_livre(n: int = 10) -> dict:
    pos = E.Position.depart()
    suivis = 0
    for _ in range(n):
        etat = E.rsn_depuis_position(pos)
        d = decide_echecs(etat, Budget(profondeur=3, temps_s=2, livre=True))
        if d.coup is None:
            break
        c = E.coup_depuis_action(d.coup)
        if c.uci() not in LIVRE.get(cle_livre(pos), []):
            break
        pos.joue(c)
        suivis += 1
    return {"suivis": suivis, "demandes": n,
            "positions_livre": len(LIVRE), "lignes": 5}


def mesure_echecs_maitres(rapide: bool) -> dict:
    depart = E.rsn_depuis_position(E.Position.depart())
    ouverture = {}
    for maitres in (False, True):
        d = decide_echecs(depart, Budget(profondeur=3, temps_s=5, maitres=maitres))
        ouverture["avec" if maitres else "sans"] = (
            E.coup_depuis_action(d.coup).uci() if d.coup else None)
    ouverts = {"e2e4", "d2d4", "g1f3", "c2c4"}
    # mats en un, avec et sans les principes
    mats = {}
    positions_mats = [
        "6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1",
        "7k/5Q2/6K1/8/8/8/8/8 w - - 0 1",
        "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 4 4",
    ]
    for maitres in (False, True):
        bons = 0
        for fen in positions_mats:
            pos = E.Position.depuis_fen(fen)
            d = decide_echecs(E.rsn_depuis_position(pos),
                              Budget(profondeur=3, temps_s=3, maitres=maitres))
            if d.coup is None:
                continue
            c = E.coup_depuis_action(d.coup)
            u = pos.joue(c)
            if not pos.coups_legaux() and pos.en_echec(pos.trait):
                bons += 1
            pos.annule(u)
        mats["avec" if maitres else "sans"] = bons
    accord = _accord_parties(2 if rapide else 3, 0.4 if rapide else 0.8,
                             debut=8 if not rapide else 12)
    return {
        "premier_coup": ouverture,
        "premier_coup_maitre": {k: v in ouverts for k, v in ouverture.items()},
        "livre": _suite_livre(10),
        "mats_en_un": mats,
        "accord_parties": accord,
    }


# ---------------------------------------------------------------------------
# Dames
# ---------------------------------------------------------------------------
def _materiel_dames(pos: D.Position) -> int:
    s = 0
    for q in pos.cases:
        if q == D.VIDE:
            continue
        v = 175 if q in (D.BLANC_DAME, D.NOIR_DAME) else 100
        s += v if D._couleur(q) == D.BLANC else -v
    return s


def _partie_dames(maitre_blanc: bool, graine: int, profondeur: int,
                  temps: float, les_deux_base: bool = False) -> int:
    pos = D.Position.depart()
    for _ in range(80):
        if pos.terminal():
            break
        pos_rsn = D.rsn_depuis_position(pos)
        maitres = False if les_deux_base else (
            maitre_blanc if pos.trait == D.BLANC else not maitre_blanc)
        d = decide_dames(pos_rsn, Budget(profondeur=profondeur, temps_s=temps,
                                         maitres=maitres, graine=graine))
        if d.coup is None:
            break
        c = D.coup_depuis_action(d.coup, pos)
        pos = pos.applique(c)
    return _materiel_dames(pos)


def mesure_dames_maitres(rapide: bool) -> dict:
    n = 6 if rapide else 20
    profondeur = 3 if rapide else 4
    temps = 0.15 if rapide else 0.4
    resultats = []
    for i in range(n):
        maitre_blanc = i % 2 == 0
        s = _partie_dames(maitre_blanc, i, profondeur, temps)
        gagnant = "blanc" if s > 0 else "noir" if s < 0 else "nulle"
        maitre_gagne = (maitre_blanc and gagnant == "blanc") or (
            not maitre_blanc and gagnant == "noir")
        resultats.append({"graine": i, "maitre_blanc": maitre_blanc,
                          "materiel": s, "gagnant": gagnant,
                          "maitre_gagne": maitre_gagne})
    base_blanc = 0
    for i in range(n):
        s = _partie_dames(True, i, profondeur, temps, les_deux_base=True)
        base_blanc += int(s > 0)
    return {"parties": n, "profondeur": profondeur,
            "maitres_gagnent": sum(r["maitre_gagne"] for r in resultats),
            "base_blanc_gagne": base_blanc,
            "resultats": resultats}


# ---------------------------------------------------------------------------
# Go
# ---------------------------------------------------------------------------
def _premier_go(maitres: bool, graines: int = 10) -> dict:
    points = []
    for g in range(graines):
        pos = G.Position.depart(5, 0)
        d = decide_go(pos.vers_rsn(), Budget(playouts=20, temps_s=5,
                                            graine=g, maitres=maitres))
        p = d.coup.corps.get("point") if d.coup else None
        if p is None:
            points.append(None)
            continue
        row, col = divmod(p, 5)
        dmin = min(row, col, 4 - row, 4 - col)
        points.append({"point": p, "bord": dmin <= 1})
    return {"graines": graines,
            "bord": sum(1 for p in points if p and p["bord"]),
            "points": points}


def _capture_go(maitres: bool, graines: int = 10) -> dict:
    # blanc (0,1)=1 n'a qu'une liberté, (0,2)=2 ; noir joue 2 et le capture.
    plateau = [G.VIDE] * 25
    plateau[0] = G.NOIR
    plateau[1] = G.BLANC
    plateau[6] = G.NOIR
    pos = G.Position(5, plateau, G.NOIR)
    choix = []
    for g in range(graines):
        d = decide_go(pos.vers_rsn(), Budget(playouts=20, temps_s=5,
                                            graine=g, maitres=maitres))
        choix.append(d.coup.corps.get("point") if d.coup else None)
    return {"graines": graines, "capture": sum(1 for p in choix if p == 2),
            "choix": choix}


def _premier_go_9(maitres: bool, graines: int = 10,
                  playouts: int = 200) -> dict:
    """Sur 9×9, avec assez de playouts pour exploiter le prior."""
    points = []
    for g in range(graines):
        pos = G.Position.depart(9, 0)
        d = decide_go(pos.vers_rsn(), Budget(playouts=playouts, temps_s=20,
                                            graine=g, maitres=maitres))
        p = d.coup.corps.get("point") if d.coup else None
        if p is None:
            points.append(None)
            continue
        row, col = divmod(p, 9)
        dmin = min(row, col, 8 - row, 8 - col)
        points.append({"point": p, "ligne": dmin})
    return {"graines": graines,
            "ligne_3_4": sum(1 for p in points if p and p["ligne"] in (2, 3)),
            "points": points}


def mesure_go_maitres(rapide: bool) -> dict:
    graines = 6 if rapide else 10
    g9 = 3 if rapide else 10
    p9 = 120 if rapide else 200
    return {
        "premier_sans": _premier_go(False, graines),
        "premier_avec": _premier_go(True, graines),
        "premier_9_sans": _premier_go_9(False, g9, p9),
        "premier_9_avec": _premier_go_9(True, g9, p9),
        "capture_sans": _capture_go(False, graines),
        "capture_avec": _capture_go(True, graines),
    }


# ---------------------------------------------------------------------------
# Cartes
# ---------------------------------------------------------------------------
def _partie_cartes(graine: int, maitres_ns: bool, maitres_eo: bool,
                   hasard_eo: bool = False) -> str | None:
    pos = C.Position.depart(graine)
    rng = random.Random(graine + 999)
    while not pos.terminal():
        equipe = C.equipe(pos.tour)
        if hasard_eo and equipe == 1:
            c = rng.choice(pos.coups_legaux())
        else:
            maitres = maitres_ns if equipe == 0 else maitres_eo
            d = decide_cartes(C.rsn_depuis_position(pos),
                              Budget(maitres=maitres, graine=graine))
            c = d.coup.corps["carte"] if d.coup else pos.coups_legaux()[0]
        pos = pos.joue(c)
    return pos.resultat()


def _partie_politiques(graine: int, poli_ns, poli_eo) -> str | None:
    pos = C.Position.depart(graine)
    while not pos.terminal():
        equipe = C.equipe(pos.tour)
        c = (poli_ns if equipe == 0 else poli_eo)(pos)
        pos = pos.joue(c)
    return pos.resultat()


def mesure_cartes_maitres(rapide: bool) -> dict:
    n = 200 if rapide else 1000
    base = lambda p: p.politique()  # noqa: E731
    variantes = {
        "complet": lambda p: politique_cartes_maitres(p),
        "sans_honneur": lambda p: politique_cartes_maitres(p, honneur=False),
        "sans_seconde": lambda p: politique_cartes_maitres(p, seconde=False),
        "sans_troisieme": lambda p: politique_cartes_maitres(p, troisieme=False),
        "seconde_seule": lambda p: politique_cartes_maitres(p, troisieme=False, honneur=False),
    }
    ablation = {}
    for nom, poli in variantes.items():
        gains = sum(1 for g in range(n)
                    if _partie_politiques(g, poli, base) == "N-S")
        ablation[nom] = gains
    compte = {"maitres_vs_base": ablation["complet"],
              "base_vs_base": sum(1 for g in range(n)
                                  if _partie_politiques(g, base, base) == "N-S"),
              "maitres_vs_hasard": 0, "base_vs_hasard": 0}
    for g in range(n):
        if _partie_cartes(g, True, False, hasard_eo=True) == "N-S":
            compte["maitres_vs_hasard"] += 1
        if _partie_cartes(g, False, False, hasard_eo=True) == "N-S":
            compte["base_vs_hasard"] += 1
    return {"donnes": n, **compte, "ablation": ablation}


# ---------------------------------------------------------------------------
def mesure_maitres(rapide: bool = True) -> dict:
    t0 = time.perf_counter()
    echecs = mesure_echecs_maitres(rapide)
    dames = mesure_dames_maitres(rapide)
    go = mesure_go_maitres(rapide)
    cartes = mesure_cartes_maitres(rapide)
    return {
        "principles": len(PRINCIPES),
        "sources": len(SOURCES),
        "livre": len(LIVRE),
        "parties": len(PARTIES),
        "echecs": echecs,
        "dames": dames,
        "go": go,
        "cartes": cartes,
        "duree_s": round(time.perf_counter() - t0, 3),
    }


if __name__ == "__main__":
    import argparse
    import json
    ap = argparse.ArgumentParser()
    ap.add_argument("--complet", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    if __name__ == "__main__":
        resultat = (mesure_langues if "mesure_maitres" == "mesure_langues" else mesure_maitres)(
            rapide=not args.complet)
    if args.json:
        import pathlib
        pathlib.Path(args.json).write_text(
            json.dumps(resultat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(resultat, ensure_ascii=False, indent=1))
