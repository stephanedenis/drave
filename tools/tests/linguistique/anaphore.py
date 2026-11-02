"""anaphore.py — résolution heuristique des pronoms anaphoriques (L, discours).

Le module résout `il/elle/ils/elles/it/he/she/they` vers le **dernier nom** rencontré avant le
pronom. Il est mesuré sur les phrases de discours du gold (r301–r320), qui portent une
annotation `coref` à la main.
"""
from __future__ import annotations

PRONOMS = {"il", "elle", "ils", "elles", "it", "he", "she", "they"}


def resoudre(mots: list[dict]) -> dict[str, str]:
    """Résout chaque pronom anaphorique vers le dernier nom (en minuscules)."""
    dernier, liens = None, {}
    for mot in mots:
        texte = mot["texte"].lower()
        if mot["pos"] == "NOUN":
            dernier = texte
        elif texte in PRONOMS and dernier is not None:
            liens[texte] = dernier
    return liens


def mesurer(phrases: list[dict]) -> dict:
    """Compare les liens résolus aux liens du gold (`coref`)."""
    total = justes = phrases_avec = 0
    details = []
    for phrase in phrases:
        attendu = (phrase.get("pragma") or {}).get("coref") or {}
        if not attendu:
            continue
        phrases_avec += 1
        obtenu = resoudre(phrase["mots"])
        for pronom, cible in attendu.items():
            total += 1
            if obtenu.get(pronom) == cible:
                justes += 1
            else:
                details.append({"id": phrase["id"], "pronom": pronom,
                                "attendu": cible, "obtenu": obtenu.get(pronom)})
    return {"phrases": phrases_avec, "liens": total, "justes": justes,
            "taux": round(justes / total, 4) if total else 0.0, "erreurs": details}
