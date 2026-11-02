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
OBJETS_ROLE = {"le", "la", "les", "lui", "leur", "it", "him", "her", "them"}
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
