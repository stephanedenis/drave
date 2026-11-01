"""trace.py — le profil DRVF `thought` : une enveloppe, un rejeu, un diff.

Le format de flux DRVF décrit les activations ; ce profil transporte une **trace de pensée** :
le problème, l'état racine (ses candidats) et la liste des événements (parent, enfant, opérateur,
paramètres, score, coût, stratégie). Il ne transporte pas le corps à chaque pas : il transporte
l'empreinte, et le rejeu **recalcule** chaque enfant avec l'opérateur du problème.

    en-tête   "DRVF"                     4 octets
              version     u16  = 1
              profil      u16  = 1 (thought)
              longueur    u32
    charge    JSON canonique  {"profil","version","probleme","racine","evenements"}

Le rejeu échoue si un enfant ne se recalcule pas, si son empreinte diffère ou si son score a été
modifié : une trace n'est pas une ré-exécution, c'est une **preuve**.
"""
from __future__ import annotations

import json
import pathlib
import struct

from .coeur import Candidat, Etat
from .store import Evenement, Store, Trace, diff

MAGIC = b"DRVF"
VERSION = 1
PROFIL_THOUGHT = 1
TAILLE_ENTETE = 12


def _etat_depuis_dict(d: dict) -> Etat:
    candidats = tuple(
        Candidat(c["id"], c["corps"], c.get("annotation", {}), c.get("statut", "hypothese"))
        for c in d["candidats"])
    return Etat(d["id"], d.get("parent"), int(d.get("profondeur", 0)), candidats,
                d.get("statut", "ouvert"))


def encoder(trace: Trace, store: Store, racine: str, probleme_nom: str = "") -> bytes:
    """Encode la trace et l'état racine ; le store complet n'est pas nécessaire au rejeu."""
    etat = store.get(racine)
    if etat is None:
        raise ValueError(f"racine inconnue : {racine[:8]}")
    corps = {
        "profil": "thought",
        "version": VERSION,
        "probleme": probleme_nom,
        "racine": {"empreinte": racine, "etat": etat.vers_dict()},
        "evenements": [ev.vers_dict() for ev in trace.evenements],
    }
    charge = json.dumps(corps, ensure_ascii=False, sort_keys=True,
                        separators=(",", ":")).encode("utf-8")
    return MAGIC + struct.pack("<HHI", VERSION, PROFIL_THOUGHT, len(charge)) + charge


def decoder(octets: bytes) -> dict:
    if len(octets) < TAILLE_ENTETE or octets[:4] != MAGIC:
        raise ValueError("ce n'est pas un flux DRVF")
    version, profil, longueur = struct.unpack("<HHI", octets[4:TAILLE_ENTETE])
    if version != VERSION or profil != PROFIL_THOUGHT:
        raise ValueError(f"profil inconnu : version {version}, profil {profil}")
    if len(octets) - TAILLE_ENTETE != longueur:
        raise ValueError("longueur de charge incohérente")
    doc = json.loads(octets[TAILLE_ENTETE:].decode("utf-8"))
    if doc.get("profil") != "thought":
        raise ValueError("profil JSON incohérent")
    if "racine" not in doc or "evenements" not in doc:
        raise ValueError("trace incomplète")
    return doc


def ecrire(trace: Trace, store: Store, racine: str, chemin: pathlib.Path,
           probleme_nom: str = "") -> pathlib.Path:
    chemin = pathlib.Path(chemin)
    chemin.write_bytes(encoder(trace, store, racine, probleme_nom))
    return chemin


def lire(chemin: pathlib.Path) -> dict:
    return decoder(pathlib.Path(chemin).read_bytes())


def rejouer(doc: dict, probleme) -> tuple[Store, Trace]:
    """Recalcule chaque enfant : une empreinte ou un score modifié doit lever."""
    etat0 = _etat_depuis_dict(doc["racine"]["etat"])
    if etat0.empreinte() != doc["racine"]["empreinte"]:
        raise ValueError("l'état racine ne correspond pas à son empreinte")
    store = Store()
    racine = store.put(etat0)
    trace = Trace()
    for ev in doc["evenements"]:
        parent = store.get(ev["parent"])
        if parent is None:
            raise ValueError(f"parent absent : {ev['parent'][:8]}")
        try:
            operateur = probleme.operateurs[ev["operateur"]]
        except KeyError as e:
            raise ValueError(f"opérateur inconnu : {ev['operateur']}") from e
        enfants = operateur(parent, ev["params"])
        enfant = next((x for x in enfants if x.empreinte() == ev["enfant"]), None)
        if enfant is None:
            raise ValueError(f"l'empreinte {ev['enfant'][:8]} n'est pas recalculée")
        score = probleme.score(enfant)
        if abs(score - float(ev["score"])) > 1e-9:
            raise ValueError(f"score divergent sur {ev['enfant'][:8]}: "
                             f"{score} != {ev['score']}")
        store.put(enfant)
        store.edge(ev["parent"], ev["enfant"], ev["operateur"], ev["params"], score)
        trace.pas(ev["parent"], ev["enfant"], ev["operateur"], ev["params"], score,
                  int(ev.get("cout", 1)), ev.get("strategie", ""))
    return store, trace


def diff_fichiers(a: bytes, b: bytes) -> int | None:
    """Premier événement divergent entre deux flux (racine, opérateur, score)."""
    da, db = decoder(a), decoder(b)
    if da.get("racine") != db.get("racine") or da.get("probleme") != db.get("probleme"):
        return 0
    ea, eb = da["evenements"], db["evenements"]
    for i, (x, y) in enumerate(zip(ea, eb)):
        if (x.get("parent"), x.get("enfant"), x.get("operateur"), x.get("score")) != \
           (y.get("parent"), y.get("enfant"), y.get("operateur"), y.get("score")):
            return i
    if len(ea) != len(eb):
        return min(len(ea), len(eb))
    return None
