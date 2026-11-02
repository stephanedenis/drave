"""anaphore.py — résolution heuristique des pronoms anaphoriques (L, discours).

Le module résout `il/elle/ils/elles/it/he/she/they` vers le **dernier nom** rencontré avant le
pronom. Il est mesuré sur les phrases de discours du gold (r301–r320), qui portent une
annotation `coref` à la main.
"""
from __future__ import annotations

PRONOMS = {"il", "elle", "ils", "elles", "it", "he", "she", "they"}
OBJETS = {"le", "la", "les", "lui", "leur", "it", "him", "her", "them", "us", "me", "te", "nous", "vous"}


def _dans_pp(mots: list[dict], i: int) -> bool:
    """Vrai si le nom i est dans un PP (précédé d'un DET puis d'une PREP, ou d'une PREP)."""
    if i >= 1 and mots[i - 1]["pos"] in ("PREP", "DET"):
        if mots[i - 1]["pos"] == "PREP":
            return True
        if i >= 2 and mots[i - 2]["pos"] == "PREP":
            return True
    return False


def resoudre(mots: list[dict], ignorer_pp: bool = False) -> dict[str, str]:
    """Résout chaque pronom anaphorique vers le dernier nom (en minuscules).

    `ignorer_pp=True` écarte les noms des groupes prépositionnels (le PP locatif est le piège
    de r324/r328).
    """
    dernier, liens = None, {}
    for i, mot in enumerate(mots):
        texte = mot["texte"].lower()
        if mot["pos"] == "NOUN":
            if not (ignorer_pp and _dans_pp(mots, i)):
                dernier = texte
        elif mot["pos"] == "PRON" and texte in (PRONOMS | OBJETS) and dernier is not None:
            liens[texte] = dernier
    return liens


SUJETS = {"il", "elle", "ils", "elles", "it", "he", "she", "they"}
OBJETS_ROLE = {"le", "la", "les", "lui", "leur", "l'", "it", "him", "her", "them"}
ROLES_SUJET = ("agent",)
ROLES_OBJET = ("patient", "destinataire", "attribut")


def _dernier_mot(segment: dict) -> str | None:
    mots = [m for m in segment["texte"].split() if any(c.isalpha() for c in m)]
    return mots[-1].lower() if mots else None


def resoudre_roles(mots: list[dict], segments: list[dict]) -> dict[str, str]:
    """Résout les pronoms par le **rôle du segment** : sujet → agent, objet → patient."""
    agent = patient = None
    for seg in segments:
        nom = _dernier_mot(seg)
        if nom is None or nom in (SUJETS | OBJETS_ROLE):
            continue
        if seg.get("role") in ROLES_SUJET:
            agent = nom
        elif seg.get("role") in ROLES_OBJET:
            patient = nom
    liens, vus = {}, set()
    for mot in mots:
        if mot["pos"] != "PRON":
            continue
        texte = mot["texte"].lower()
        if texte in OBJETS_ROLE and patient is not None:
            liens[texte] = patient
        elif texte in SUJETS and agent is not None and texte not in vus:
            liens[texte] = agent
            vus.add(texte)
    return liens


INTRANSITIFS = {"dort", "dorment", "rêve", "rêvent", "sleeps", "sleep", "dream", "dreams",
                "répond", "répondent", "answers", "answer", "pleut", "pleuvent", "rains",
                "vient", "viennent", "comes", "come", "part", "partent", "leaves", "leave"}


def _verbe(mots: list[dict]) -> str | None:
    for mot in mots:
        if mot["pos"] == "VERB":
            return mot["texte"].lower()
    return None


def resoudre_semantique(mots: list[dict], segments: list[dict]) -> dict[str, str]:
    """Sémantique : verbe intransitif → proximité ; transitif → rôles du segment."""
    vb = _verbe(mots)
    intransitif = vb in INTRANSITIFS
    agent = patient = None
    for seg in segments:
        nom = _dernier_mot(seg)
        if nom is None or nom in (SUJETS | OBJETS_ROLE):
            continue
        if seg.get("role") in ROLES_SUJET:
            agent = nom
        elif seg.get("role") in ROLES_OBJET:
            patient = nom
    liens, vus = {}, set()
    for i, mot in enumerate(mots):
        if mot["pos"] != "PRON":
            continue
        texte = mot["texte"].lower()
        if texte in OBJETS_ROLE and patient is not None:
            liens[texte] = patient
        elif texte in SUJETS and texte not in vus:
            if intransitif:
                avant = [m for m in mots[:i] if m["pos"] == "NOUN" and not _dans_pp(mots, mots.index(m))]
                if avant:
                    liens[texte] = avant[-1]["texte"].lower()
            elif agent is not None:
                liens[texte] = agent
            vus.add(texte)
    return liens


def mesurer_pondere(phrases: list[dict], part_train: float = 0.67) -> dict:
    """Vote pondéré : poids appris sur une part, évalués sur l'autre."""
    regles = {
        "dernier_nom": lambda m, s: resoudre(m, ignorer_pp=True),
        "role": resoudre_roles,
        "hybride": resoudre_hybride,
        "semantique": resoudre_semantique,
    }
    liens = []
    for phrase in phrases:
        attendu = (phrase.get("pragma") or {}).get("coref") or {}
        if not attendu:
            continue
        verdicts = {nom: f(phrase["mots"], phrase["segments"]) for nom, f in regles.items()}
        for pronom, cible in attendu.items():
            liens.append(({nom: v.get(pronom) for nom, v in verdicts.items()},
                          pronom, cible))
    n_train = int(round(len(liens) * part_train))
    train, test = liens[:n_train], liens[n_train:]
    grille = [(a, b, c, d) for a in (0, 1, 2) for b in (0, 1, 2)
              for c in (0, 1, 2) for d in (0, 1, 2) if a + b + c + d > 0]
    noms = list(regles)

    def score(poids, items):
        justes = 0
        for cands, pronom, cible in items:
            votes = {}
            for nom, w in zip(noms, poids):
                if cands[nom] is not None:
                    votes[cands[nom]] = votes.get(cands[nom], 0) + w
            if votes:
                gagnant = max(votes.items(), key=lambda kv: kv[1])
                justes += gagnant[0] == cible
        return justes

    meilleur = max(grille, key=lambda p: score(p, train))
    return {"train": len(train), "test": len(test),
            "poids": dict(zip(noms, meilleur)),
            "justes_train": score(meilleur, train),
            "justes_test": score(meilleur, test),
            "taux_test": round(score(meilleur, test) / max(1, len(test)), 4)}


def mesurer_cv(phrases: list[dict], plis: int = 5, graine: int = 0) -> dict:
    """Validation croisée : poids appris sur k−1 plis, testés sur le pli restant."""
    import random as _r
    regles = {
        "dernier_nom": lambda m, s: resoudre(m, ignorer_pp=True),
        "role": resoudre_roles,
        "hybride": resoudre_hybride,
        "semantique": resoudre_semantique,
    }
    liens = []
    for phrase in phrases:
        attendu = (phrase.get("pragma") or {}).get("coref") or {}
        if not attendu:
            continue
        verdicts = {nom: f(phrase["mots"], phrase["segments"]) for nom, f in regles.items()}
        for pronom, cible in attendu.items():
            liens.append(({nom: v.get(pronom) for nom, v in verdicts.items()},
                          pronom, cible))
    rng = _r.Random(graine)
    rng.shuffle(liens)
    taille = len(liens) // plis
    grille = [(a, b, c, d) for a in (0, 1, 2) for b in (0, 1, 2)
              for c in (0, 1, 2) for d in (0, 1, 2) if a + b + c + d > 0]
    noms = list(regles)

    def score(poids, items):
        justes = 0
        for cands, pronom, cible in items:
            votes = {}
            for nom, w in zip(noms, poids):
                if cands[nom] is not None:
                    votes[cands[nom]] = votes.get(cands[nom], 0) + w
            if votes:
                gagnant = max(votes.items(), key=lambda kv: kv[1])
                justes += gagnant[0] == cible
        return justes

    resultats = []
    for i in range(plis):
        test = liens[i * taille:(i + 1) * taille] if i < plis - 1 else liens[i * taille:]
        train = [l for j, l in enumerate(liens) if l not in test]
        meilleur = max(grille, key=lambda p: score(p, train))
        resultats.append({"pli": i + 1, "poids": dict(zip(noms, meilleur)),
                          "train": len(train), "test": len(test),
                          "justes": score(meilleur, test)})
    total_test = sum(r["test"] for r in resultats)
    total_justes = sum(r["justes"] for r in resultats)
    return {"plis": resultats, "justes": total_justes, "test": total_test,
            "taux": round(total_justes / max(1, total_test), 4)}


def resoudre_meta(mots: list[dict], segments: list[dict]) -> dict[str, str]:
    """Méta-règle : vote majoritaire des quatre règles, égalité → dernier nom."""
    regles = [resoudre(mots, ignorer_pp=True), resoudre_roles(mots, segments),
              resoudre_hybride(mots, segments), resoudre_semantique(mots, segments)]
    pronoms = set()
    for r in regles:
        pronoms.update(r)
    liens = {}
    for p in pronoms:
        votes = {}
        for r in regles:
            if p in r:
                votes[r[p]] = votes.get(r[p], 0) + 1
        if votes:
            meilleur = max(votes.values())
            cands = [c for c, n in votes.items() if n == meilleur]
            liens[p] = (regles[0].get(p) if p in regles[0] and regles[0][p] in cands
                        else cands[0])
    return liens


def mesurer_meta(phrases: list[dict]) -> dict:
    """Compare `resoudre_meta` aux liens du gold."""
    total = justes = phrases_avec = 0
    details = []
    for phrase in phrases:
        attendu = (phrase.get("pragma") or {}).get("coref") or {}
        if not attendu:
            continue
        phrases_avec += 1
        obtenu = resoudre_meta(phrase["mots"], phrase["segments"])
        for pronom, cible in attendu.items():
            total += 1
            if obtenu.get(pronom) == cible:
                justes += 1
            else:
                details.append({"id": phrase["id"], "pronom": pronom,
                                "attendu": cible, "obtenu": obtenu.get(pronom)})
    return {"phrases": phrases_avec, "liens": total, "justes": justes,
            "taux": round(justes / total, 4) if total else 0.0, "erreurs": details}


def _liens_attendus(phrases: list[dict]) -> list[tuple]:
    liens = []
    for phrase in phrases:
        attendu = (phrase.get("pragma") or {}).get("coref") or {}
        for pronom, cible in attendu.items():
            liens.append((phrase["id"], pronom, cible))
    return liens


def _par_regle(phrases: list[dict], resolv) -> list[bool]:
    res = []
    for phrase in phrases:
        attendu = (phrase.get("pragma") or {}).get("coref") or {}
        obtenu = resolv(phrase["mots"], phrase["segments"])
        for pronom, cible in attendu.items():
            res.append(obtenu.get(pronom) == cible)
    return res


def kappa(a: list[bool], b: list[bool]) -> float:
    """Cohen's kappa entre deux séries de verdicts binaires."""
    n = len(a)
    if n == 0:
        return 0.0
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pa1 = sum(a) / n
    pb1 = sum(b) / n
    pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    return round((po - pe) / (1 - pe), 4) if pe != 1 else 0.0


def accords(phrases: list[dict]) -> dict:
    """Les kappas pairwise des quatre règles de coréférence."""
    regles = {
        "dernier_nom": lambda m, s: resoudre(m, ignorer_pp=True),
        "role": resoudre_roles,
        "hybride": resoudre_hybride,
        "semantique": resoudre_semantique,
    }
    verdicts = {nom: _par_regle(phrases, f) for nom, f in regles.items()}
    paires = {}
    noms = list(verdicts)
    for i in range(len(noms)):
        for j in range(i + 1, len(noms)):
            paires[f"{noms[i]}/{noms[j]}"] = kappa(verdicts[noms[i]], verdicts[noms[j]])
    return {"verdicts": {k: sum(v) for k, v in verdicts.items()}, "paires": paires}


def mesurer_semantique(phrases: list[dict]) -> dict:
    """Compare `resoudre_semantique` aux liens du gold."""
    total = justes = phrases_avec = 0
    details = []
    for phrase in phrases:
        attendu = (phrase.get("pragma") or {}).get("coref") or {}
        if not attendu:
            continue
        phrases_avec += 1
        obtenu = resoudre_semantique(phrase["mots"], phrase["segments"])
        for pronom, cible in attendu.items():
            total += 1
            if obtenu.get(pronom) == cible:
                justes += 1
            else:
                details.append({"id": phrase["id"], "pronom": pronom,
                                "attendu": cible, "obtenu": obtenu.get(pronom)})
    return {"phrases": phrases_avec, "liens": total, "justes": justes,
            "taux": round(justes / total, 4) if total else 0.0, "erreurs": details}


def resoudre_hybride(mots: list[dict], segments: list[dict]) -> dict[str, str]:
    """Hybride : sujet par le rôle (`agent`), objet par le dernier nom."""
    agent = None
    for seg in segments:
        nom = _dernier_mot(seg)
        if nom is None or nom in (SUJETS | OBJETS_ROLE):
            continue
        if seg.get("role") in ROLES_SUJET:
            agent = nom
    liens, vus = {}, set()
    for i, mot in enumerate(mots):
        if mot["pos"] != "PRON":
            continue
        texte = mot["texte"].lower()
        if texte in OBJETS_ROLE:
            avant = [m for m in mots[:i] if m["pos"] == "NOUN" and not _dans_pp(mots, mots.index(m))]
            if avant:
                liens[texte] = avant[-1]["texte"].lower()
        elif texte in SUJETS and agent is not None and texte not in vus:
            liens[texte] = agent
            vus.add(texte)
    return liens


def mesurer_hybride(phrases: list[dict]) -> dict:
    """Compare `resoudre_hybride` aux liens du gold."""
    total = justes = phrases_avec = 0
    details = []
    for phrase in phrases:
        attendu = (phrase.get("pragma") or {}).get("coref") or {}
        if not attendu:
            continue
        phrases_avec += 1
        obtenu = resoudre_hybride(phrase["mots"], phrase["segments"])
        for pronom, cible in attendu.items():
            total += 1
            if obtenu.get(pronom) == cible:
                justes += 1
            else:
                details.append({"id": phrase["id"], "pronom": pronom,
                                "attendu": cible, "obtenu": obtenu.get(pronom)})
    return {"phrases": phrases_avec, "liens": total, "justes": justes,
            "taux": round(justes / total, 4) if total else 0.0, "erreurs": details}


def mesurer_roles(phrases: list[dict]) -> dict:
    """Compare `resoudre_roles` aux liens du gold."""
    total = justes = phrases_avec = 0
    details = []
    for phrase in phrases:
        attendu = (phrase.get("pragma") or {}).get("coref") or {}
        if not attendu:
            continue
        phrases_avec += 1
        obtenu = resoudre_roles(phrase["mots"], phrase["segments"])
        for pronom, cible in attendu.items():
            total += 1
            if obtenu.get(pronom) == cible:
                justes += 1
            else:
                details.append({"id": phrase["id"], "pronom": pronom,
                                "attendu": cible, "obtenu": obtenu.get(pronom)})
    return {"phrases": phrases_avec, "liens": total, "justes": justes,
            "taux": round(justes / total, 4) if total else 0.0, "erreurs": details}


def mesurer(phrases: list[dict], ignorer_pp: bool = False) -> dict:
    """Compare les liens résolus aux liens du gold (`coref`)."""
    total = justes = phrases_avec = 0
    details = []
    for phrase in phrases:
        attendu = (phrase.get("pragma") or {}).get("coref") or {}
        if not attendu:
            continue
        phrases_avec += 1
        obtenu = resoudre(phrase["mots"], ignorer_pp=ignorer_pp)
        for pronom, cible in attendu.items():
            total += 1
            if obtenu.get(pronom) == cible:
                justes += 1
            else:
                details.append({"id": phrase["id"], "pronom": pronom,
                                "attendu": cible, "obtenu": obtenu.get(pronom)})
    return {"phrases": phrases_avec, "liens": total, "justes": justes,
            "taux": round(justes / total, 4) if total else 0.0, "erreurs": details}
