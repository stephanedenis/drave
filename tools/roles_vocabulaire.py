"""roles_vocabulaire.py — le vocabulaire **fermé** des rôles de l'annotation.

Le produit publie un rôle par syntagme (`meta.role`). Les règles internes en produisent
plusieurs orthographes et plusieurs granularités : `prédicat`/`predicat`, `qualité`/
`qualite`, `patient`/`complément`/`groupe nominal` pour un GN, `possession` pour le
possesseur, etc. Un consommateur qui filtre `role == "predicat"` ne doit pas dépendre de
la règle qui a produit le segment.

Ce module est la **seule** table de passage. Il est pur (aucun import du bloc) pour que
les tests puissent le charger seul et pour que le schéma JSON puisse publier la même
liste (`tools/schemas/drave-annotation-v2.json`).

    from tools.roles_vocabulaire import ROLES, normaliser_role
    normaliser_role("prédicat")        # "predicat"
    normaliser_role("groupe nominal")  # "objet"
    normaliser_role("inventé")         # lève RoleHorsVocabulaire

Le vocabulaire est volontairement **petit** : huit rôles. Ce n'est pas une annotation
sémantique plus fine ; c'est une **normalisation** de ce que les règles publient déjà.
La table est exhaustive pour les rôles produits par `bloc_linguistique.py` et le
générateur S ; un rôle inconnu est une **erreur**, pas une valeur passée telle quelle.
"""
from __future__ import annotations

# Le vocabulaire fermé, dans l'ordre publié par le schéma. `predicat` est sans accent :
# c'est la forme canonique, pas une préférence d'affichage.
ROLES = (
    "predicat",
    "agent",
    "objet",
    "lieu",
    "temps",
    "qualite",
    "possesseur",
    "destinataire",
)

# La table des correspondances : la clé est le rôle **brut** (casse repliée, accents
# conservés), la valeur est un rôle du vocabulaire. Plusieurs bruts peuvent tomber sur le
# même rôle : c'est le but (patient/complément/thème sont des objets).
CORRESPONDANCES = {
    # prédicat
    "predicat": "predicat",
    "prédicat": "predicat",
    # agent
    "agent": "agent",
    # objet : le patient, le complément, le thème et le GN sans fonction identifiée
    "objet": "objet",
    "patient": "objet",
    "complément": "objet",
    "complement": "objet",
    "contenu": "objet",
    "theme": "objet",
    "thème": "objet",
    "groupe nominal": "objet",
    # lieu, temps
    "lieu": "lieu",
    "source": "lieu",
    "temps": "temps",
    # qualité : l'attribut, la manière et les circonstants de concession/cause
    "qualite": "qualite",
    "qualité": "qualite",
    "attribut": "qualite",
    "maniere": "qualite",
    "manière": "qualite",
    "concession": "qualite",
    "hypothese": "qualite",
    "hypothèse": "qualite",
    "cause": "qualite",
    "consequence": "qualite",
    "conséquence": "qualite",
    # possesseur
    "possesseur": "possesseur",
    "possession": "possesseur",
    # destinataire : le bénéficiaire et le but (la destination de l'action)
    "destinataire": "destinataire",
    "but": "destinataire",
    # objet instrumental : `avec le télescope` est un objet de l'action
    "moyen": "objet",
    "instrument": "objet",
}

# La même table, en lignes lisibles, pour la fiche et le rapport JSON.
TABLE = tuple({"brut": brut, "normalise": normalise}
              for brut, normalise in sorted(CORRESPONDANCES.items()))

# Le contrôle le plus direct : chaque rôle de la table tombe dans le vocabulaire.
if any(valeur not in ROLES for valeur in CORRESPONDANCES.values()):  # pragma: no cover
    raise AssertionError("correspondance de rôle hors vocabulaire")


class RoleHorsVocabulaire(ValueError):
    """Un rôle non vide n'appartient pas au vocabulaire fermé."""


def normaliser_role(role: str, strict: bool = True) -> str:
    """Le rôle canonique de `role` ; `""` reste `""` (absence de rôle).

    `strict=True` (défaut) lève `RoleHorsVocabulaire` pour un rôle inconnu : le produit
    ne publie pas silencieusement une valeur hors contrat. `strict=False` rend `""`,
    ce qui sert aux affichages qui ne doivent pas planter sur une entrée ancienne.
    """
    brut = (role or "").strip()
    if not brut:
        return ""
    canonique = CORRESPONDANCES.get(brut.casefold())
    if canonique is not None:
        return canonique
    if strict:
        raise RoleHorsVocabulaire(
            f"rôle hors vocabulaire : {brut!r} (attendu : {', '.join(ROLES)})")
    return ""


def est_dans_vocabulaire(role: str) -> bool:
    """Le rôle est-il vide ou dans le vocabulaire fermé ? (ne lève jamais)."""
    return not (role or "").strip() or normaliser_role(role, strict=False) != ""
