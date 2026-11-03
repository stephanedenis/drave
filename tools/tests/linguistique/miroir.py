"""Le miroir entrée/sortie du bloc linguistique : restitution et fidélité.

Règle 6 : toute mesure d'entrée se double d'une mesure de sortie. `rendre` reconstruit
le texte depuis les étiquettes de **surface** (`graphème`, `mot`) ; `fidelite` le compare
à la source. La **fluidité** (longueur, ponctuation) n'est pas la **fidélité** : une
restitution peut être fluide et infidèle, ou fidèle et hachée.
"""
from __future__ import annotations

import re

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import tools.bloc_linguistique as bl
from tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc


def rendre(a: bl.Annotation) -> str:
    """Reconstruit le texte depuis les étiquettes de surface, sans lire `a.texte`."""
    g = [e for e in a.etiquettes if e.niveau == "graphème"]
    if not g:
        return ""
    return "".join(e.valeur for e in sorted(g, key=lambda e: (e.debut, e.fin)))


def fidelite(a: bl.Annotation, source: str) -> float:
    """1.0 si la restitution égale la source, 0.0 sinon (la mesure est binaire ici)."""
    return 1.0 if rendre(a) == source else 0.0


def rendre_mots(a: bl.Annotation) -> str:
    """Restitution depuis le niveau `mot` : la surface, token par token, espacée."""
    mots = [e for e in a.etiquettes if e.niveau == "mot"]
    return " ".join(e.valeur for e in sorted(mots, key=lambda e: (e.debut, e.fin)))


def fidelite_mots(a: bl.Annotation, source: str) -> float:
    """La fidélité des mots : la suite des tokens est-elle celle de la source ?"""
    return 1.0 if rendre_mots(a) == " ".join(source.split()) else 0.0


def rendre_pos(a: bl.Annotation) -> str:
    """La sortie **sémantique** : les mots reconstruits depuis leurs étiquettes POS."""
    pos = [e for e in a.etiquettes if e.niveau == "pos"]
    return " ".join(e.valeur for e in sorted(pos, key=lambda e: (e.debut, e.fin)))


def fidelite_pos(a: bl.Annotation, source: str) -> float:
    """La fidélité de la sortie POS : la suite des mots étiquetés est-elle la source ?"""
    return 1.0 if rendre_pos(a) == " ".join(source.split()) else 0.0


def rendre_pos_espaces(a: bl.Annotation, texte: str) -> str:
    """La sortie POS **avec les intervalles d'origine** : les trous (ponctuation, espaces)
    sont repris de la source, pas perdus."""
    pos = sorted([e for e in a.etiquettes if e.niveau == "pos"],
                 key=lambda e: (e.debut, e.fin))
    out = []
    last = 0
    for e in pos:
        if e.debut > last:
            out.append(texte[last:e.debut])
        out.append(texte[e.debut:e.fin])
        last = max(last, e.fin)
    if last < len(texte):
        out.append(texte[last:])
    return "".join(out)


def fidelite_pos_espaces(a: bl.Annotation, source: str) -> float:
    return 1.0 if rendre_pos_espaces(a, source) == source else 0.0


def resume(a: bl.Annotation) -> str:
    """La sortie **sémantique** : le résumé par les syntagmes (GN, GV), pas le texte."""
    seg = [e for e in a.etiquettes if e.niveau == "syntagme"]
    return " ".join(e.valeur for e in sorted(seg, key=lambda e: (e.debut, e.fin)))


def rappel_resume(a: bl.Annotation, source: str) -> float:
    """La part des mots de la source que le résumé couvre (rappel des tokens)."""
    mots = set(source.split())
    rendus = set(resume(a).split())
    return round(len(mots & rendus) / max(1, len(mots)), 4)


def repondre(a: bl.Annotation) -> str:
    """La **réponse** : selon l'acte, une reformulation minimale (pas une répétition)."""
    acte = next((e.valeur for e in a.etiquettes
                 if e.niveau == "pragmatique" and e.type == "acte"), "assertion")
    if acte == "question":
        return "réponse : oui ou non, selon le contexte"
    if acte == "ordre":
        return "ordre reçu"
    return "assertion notée"


def fidelite_reponse(a: bl.Annotation) -> float:
    """1.0 si la réponse correspond à l'acte détecté (une classe, pas le texte)."""
    acte = next((e.valeur for e in a.etiquettes
                 if e.niveau == "pragmatique" and e.type == "acte"), "assertion")
    rep = repondre(a)
    return 1.0 if ((acte == "question" and rep.startswith("réponse"))
                   or (acte == "ordre" and rep == "ordre reçu")
                   or (acte == "assertion" and rep == "assertion notée")) else 0.0


def repondre_contenu(a: bl.Annotation) -> str | None:
    """La réponse **au contenu** : None — le bloc n'a pas de modèle pour répondre.

    C'est un résultat : la sortie la plus riche est celle que l'heuristique **ne peut pas**
    produire. Elle demande un modèle (le neuronal réel, toujours bloqué).
    """
    return None


def repondre_extraction(a: bl.Annotation) -> str | None:
    """La réponse par **extraction** : le premier GN de la phrase, à défaut le GV.

    Ce n'est pas une réponse *au* contenu : c'est ce que l'heuristique peut arracher au texte
    (le sujet, ou le prédicat). La fiche mesure ce que cela vaut.
    """
    gn = [e for e in a.etiquettes if e.niveau == "syntagme" and e.type == "GN"]
    if gn:
        return gn[0].valeur
    gv = [e for e in a.etiquettes if e.niveau == "syntagme" and e.type == "GV"]
    return gv[0].valeur if gv else None


def fidelite_extraction(phrases: list[dict], bloc=None) -> dict:
    """Le taux de questions pour lesquelles l'extraction trouve une réponse."""
    bloc = bloc or bl.Heuristique()
    q = [p for p in phrases if "?" in p["texte"]]
    trouvees = 0
    for p in q:
        a = bloc.analyser(p["texte"], p["langue"])
        if repondre_extraction(a) is not None:
            trouvees += 1
    return {"questions": len(q), "trouvees": trouvees,
            "taux": round(trouvees / max(1, len(q)), 4)}


def repondre_dirigee(a: bl.Annotation) -> str | None:
    """La réponse **dirigée** : pour une question fermée, `non` si la phrase nie, sinon `oui`.

    C'est une heuristique de surface (la négation), pas une compréhension : si la question
    porte sa négation, la réponse s'inverse — c'est le piège que la fiche mesure.
    """
    acte = next((e.valeur for e in a.etiquettes
                 if e.niveau == "pragmatique" and e.type == "acte"), "assertion")
    if acte != "question":
        return None
    nie = any(e.niveau == "phrase" and e.type == "négation" for e in a.etiquettes)
    lg = getattr(a, "langue", "fr")
    if lg not in ("fr", "en"):
        lg = "fr"  # la langue non détectée : repli sur le français du gold
    if nie:
        # la question nie : le français répond « si » (accord), l'anglais « yes »
        return "si" if lg == "fr" else "yes"
    return "oui" if lg == "fr" else "yes"


def repondre_contextuel(a: bl.Annotation, a_prec: bl.Annotation | None = None) -> str | None:
    """La réponse **contextuelle** : la phrase précédente tranche l'accord (fait constaté → non).

    Si la phrase précédente est une assertion affirmative, la question négative **constate**
    (réponse `non`/`no`) ; si elle nie, la question **demande l'accord** (`si`/`yes`).
    """
    acte = next((e.valeur for e in a.etiquettes
                 if e.niveau == "pragmatique" and e.type == "acte"), "assertion")
    if acte != "question":
        return None
    lg = getattr(a, "langue", "fr")
    if lg not in ("fr", "en"):
        lg = "fr"
    if a_prec is None:
        return repondre_dirigee(a)
    nie_prec = any(e.niveau == "phrase" and e.type == "négation" for e in a_prec.etiquettes)
    if nie_prec:
        return "si" if lg == "fr" else "yes"
    return "non" if lg == "fr" else "no"


def _sujet(a: bl.Annotation) -> str | None:
    """Le sujet de surface : pronom sujet, puis forme inversée, puis GN, puis premier NOUN."""
    for e in a.etiquettes:
        if e.niveau == "pos" and e.type == "PRON":
            return e.valeur
    # Forme inversée : « mange-t-il » / « dort-elle » / « partent-ils » sont UN token
    # (NOUN ou VERB) ; le sujet est le dernier segment du mot.
    for e in a.etiquettes:
        if e.niveau == "pos" and e.type in ("NOUN", "VERB") and "-" in e.valeur:
            morceaux = e.valeur.split("-")
            if len(morceaux) >= 2:
                return morceaux[-1]
    for e in a.etiquettes:
        if e.niveau == "syntagme" and e.type == "GN":
            return e.valeur
    for e in a.etiquettes:
        if e.niveau == "pos" and e.type == "NOUN":
            return e.valeur
    return None


def _simple(a: bl.Annotation) -> bool:
    """Vrai si la phrase n'a **pas** de subordonnée (SUB) ni de syntagme prépositionnel (GP).

    La paire assertion ↔ question est une phrase **simple** : « Tu viens demain. » (GV + GP de
    temps) n'a pas de SUB ; « Si tu viens, nous partirons. » en a une — ce n'est pas la paire.
    """
    if ";" in a.texte:
        return False  # juxtaposition : deux propositions, pas une phrase simple
    return not any(e.niveau == "syntagme" and e.type in ("SUB",) for e in a.etiquettes)


NEGATIONS = {"ne", "n'", "pas", "plus", "jamais", "rien", "personne"}


def _adverbes(a: bl.Annotation) -> set[str]:
    """Les adverbes **hors négation** (le complément thématique de la paire)."""
    return {e.valeur.lower() for e in a.etiquettes
            if e.niveau == "pos" and e.type == "ADV" and e.valeur.lower() not in NEGATIONS}


def _acte(a: bl.Annotation) -> str:
    """L'acte pragmatique de l'annotation (assertion par défaut)."""
    return next((e.valeur for e in a.etiquettes
                 if e.niveau == "pragmatique" and e.type == "acte"), "assertion")


def _verbe(a: bl.Annotation) -> str | None:
    """Le premier verbe de surface de l'annotation (le prédicat de la paire).

    La forme inversée « mange-t-il » est UN token étiqueté NOUN : le verbe est son **premier
    segment**. Sans cette branche, `_verbe` rendait None et la paire ne pouvait pas se former.
    """
    for e in a.etiquettes:
        if e.niveau == "pos" and e.type == "VERB":
            return e.valeur
    for e in a.etiquettes:
        if e.niveau == "pos" and e.type in ("NOUN", "VERB") and "-" in e.valeur:
            return e.valeur.split("-")[0]
    return None


def trouver_precedente(question: dict, phrases: list[dict], bloc=None) -> dict | None:
    """Le lien **automatique** : la phrase précédente de la **paire** (même sujet ET même verbe).

    La proximité seule choisit le voisin : « Il ne mange pas ? » → « Il pleut. » (r428) plutôt
    que « Il mange. » (r424). Le critère de paire (sujet + verbe) passe avant, et la proximité
    ne sert que de repli quand aucun verbe ne concorde.
    """
    bloc = bloc or bl.Heuristique()
    a = bloc.analyser(question["texte"], question["langue"])
    sujet = _sujet(a)
    verbe = _verbe(a)
    if not sujet:
        return None
    idx = next((i for i, p in enumerate(phrases) if p.get("id") == question.get("id")), -1)
    # Une question se lie à une **assertion**, jamais à une autre question : c'est ce qui
    # distingue « Viens-tu demain ? » (r304) de « Tu viens demain. » (r423).
    acte_q = _acte(a)
    repli = None
    for p in reversed(phrases[:idx] if idx > 0 else []):
        b = bloc.analyser(p["texte"], p["langue"])
        s = _sujet(b)
        if not (s and _normaliser_egal(s, sujet)):
            continue
        if acte_q == "question" and _acte(b) != "assertion":
            continue
        if acte_q == "question" and not _simple(b):
            continue
        # Paire thématique : même complément (adverbe hors négation) — « demain » rapproche
        # r423 de r408, pas r306 « Il ne vient pas. ».
        if acte_q == "question" and (_adverbes(b) ^ _adverbes(a)):
            continue
        v = _verbe(b)
        if verbe and v and _normaliser_egal(v, verbe):
            return p
        if repli is None:
            repli = p
    return repli


def trouver_suivante(question: dict, phrases: list[dict], bloc=None) -> dict | None:
    """Le lien **avant** : la phrase suivante de la paire (même sujet, verbe, adverbe).

    Miroir de `trouver_precedente` : r408 « Ne viens-tu pas demain ? » est suivi de r423
    « Tu viens demain. » — l'assertion vient **après** la question dans le gold. Le lien
    arrière ne peut pas la trouver par construction ; celui-ci regarde devant.
    """
    bloc = bloc or bl.Heuristique()
    a = bloc.analyser(question["texte"], question["langue"])
    sujet = _sujet(a)
    verbe = _verbe(a)
    if not sujet:
        return None
    idx = next((i for i, p in enumerate(phrases) if p.get("id") == question.get("id")), -1)
    acte_q = _acte(a)
    repli = None
    for p in (phrases[idx + 1:] if 0 <= idx < len(phrases) - 1 else []):
        b = bloc.analyser(p["texte"], p["langue"])
        s = _sujet(b)
        if not (s and _normaliser_egal(s, sujet)):
            continue
        if acte_q == "question" and _acte(b) != "assertion":
            continue
        if acte_q == "question" and not _simple(b):
            continue
        if acte_q == "question" and (_adverbes(b) ^ _adverbes(a)):
            continue
        v = _verbe(b)
        if verbe and v and _normaliser_egal(v, verbe):
            return p
        if repli is None:
            repli = p
    return repli


def fidelite_lien_avant(phrases: list[dict], bloc=None) -> dict:
    """Le taux de paires (question, assertion suivante) retrouvées par le lien avant."""
    paires = [(f"r{408 + k}", f"r{423 + k}") for k in range(5)]
    par_id = {p["id"]: p for p in phrases}
    justes = 0
    for qid, pid in paires:
        if qid not in par_id or pid not in par_id:
            continue
        tr = trouver_suivante(par_id[qid], phrases, bloc)
        justes += bool(tr and tr["id"] == pid)
    return {"paires": len(paires), "justes": justes, "taux": round(justes / max(1, len(paires)), 4)}


def _normaliser_egal(a: str, b: str) -> bool:
    n = lambda s: " ".join(str(s).lower().split())
    return n(a) == n(b)


def lien_coref(phrase: dict, phrases: list[dict]) -> list[tuple[str, str, str]]:
    """La **coréférence comme lien** : chaque pronom lié pointe la phrase de son antécédent.

    Renvoie [(pronom, antécédent, id_phrase_antécédent)]. La phrase de l'antécédent est la
    dernière phrase antérieure qui contient le mot de l'antécédent.
    """
    from tools.tests.linguistique.anaphore import resoudre_meta
    liens = resoudre_meta(phrase["mots"], phrase["segments"])
    idx = next((i for i, p in enumerate(phrases) if p.get("id") == phrase.get("id")), -1)
    sortie = []
    for pronom, nom in liens.items():
        cible = None
        for p in reversed(phrases[:idx] if idx > 0 else []):
            mots = set(re.findall(r"[a-zà-ÿ']+", p["texte"].lower().replace("’", "'")))
            if nom.lower() in mots:
                cible = p.get("id")
                break
        sortie.append((pronom, nom, cible))
    return sortie


def liens_absents(phrases: list[dict]) -> list[dict]:
    """Les liens dont l'antécédent est **absent** du texte (ni avant, ni dans la phrase)."""
    out = []
    for p in phrases:
        mots = set(re.findall(r"[a-zà-ÿ']+", p["texte"].lower().replace("’", "'")))
        for pronom, nom, cible in lien_coref(p, phrases):
            if cible is None and nom.lower() not in mots:
                out.append({"id": p["id"], "pronom": pronom, "nom": nom, "texte": p["texte"]})
    return out


def classer_liens_coref(phrases: list[dict]) -> dict:
    """Les liens de coréférence classés : intra-phrase, inter-phrase, absents."""
    intra = inter = absent = 0
    for p in phrases:
        mots_phrase = set(re.findall(r"[a-zà-ÿ']+", p["texte"].lower().replace("’", "'")))
        for pronom, nom, cible in lien_coref(p, phrases):
            if cible is not None:
                inter += 1
            elif nom.lower() in mots_phrase:
                intra += 1
            else:
                absent += 1
    total = intra + inter + absent
    return {"liens": total, "intra": intra, "inter": inter, "absent": absent,
            "taux_intra": round(intra / max(1, total), 4),
            "taux_inter": round(inter / max(1, total), 4),
            "taux_absent": round(absent / max(1, total), 4)}


def mesurer_lien_coref(phrases: list[dict]) -> dict:
    """Le taux de liens de coréférence dont la phrase d'antécédent est retrouvée."""
    total = trouves = 0
    for p in phrases:
        for pronom, nom, cible in lien_coref(p, phrases):
            total += 1
            if cible is not None:
                trouves += 1
    return {"liens": total, "avec_phrase": trouves,
            "taux": round(trouves / max(1, total), 4)}


def fidelite_lien_auto(phrases: list[dict], bloc=None) -> dict:
    """Le taux de questions pièges où le lien automatique retrouve la bonne précédente."""
    bloc = bloc or bl.Heuristique()
    par_id = {p["id"]: p for p in phrases}
    paires = [(f"r{418 + k}", f"r{423 + k}") for k in range(5)]
    justes = 0
    for qid, pid in paires:
        if qid not in par_id:
            continue
        q = par_id[qid]
        trouvee = trouver_precedente(q, phrases, bloc)
        if trouvee is not None and trouvee.get("id") == pid:
            justes += 1
    return {"paires": len(paires), "justes": justes,
            "taux": round(justes / max(1, len(paires)), 4)}


def fidelite_contextuelle(phrases: list[dict], bloc=None) -> dict:
    """Le taux de questions pièges où la réponse contextuelle est juste."""
    bloc = bloc or bl.Heuristique()
    # les paires (assertion, question) : r423..r427 précèdent r418..r422
    paires = [(f"r{418 + k}", f"r{423 + k}") for k in range(5)]
    par_id = {p["id"]: p for p in phrases}
    justes = 0
    for qid, pid in paires:
        if qid not in par_id or pid not in par_id:
            continue
        q = par_id[qid]
        a = bloc.analyser(q["texte"], q["langue"])
        a_prec = bloc.analyser(par_id[pid]["texte"], par_id[pid]["langue"])
        ref = (q.get("pragma") or {}).get("reponse")
        justes += juge_egal(repondre_contextuel(a, a_prec), ref)
    return {"paires": len(paires), "justes": justes,
            "taux": round(justes / max(1, len(paires)), 4)}


def fidelite_dirigee(phrases: list[dict], bloc=None) -> dict:
    """Le taux de questions fermées où la réponse dirigée est juste (juge)."""
    bloc = bloc or bl.Heuristique()
    q = [p for p in phrases if "?" in p["texte"]]
    justes = 0
    for p in q:
        a = bloc.analyser(p["texte"], p["langue"])
        ref = (p.get("pragma") or {}).get("reponse")
        justes += juge_egal(repondre_dirigee(a), ref)
    return {"questions": len(q), "justes": justes,
            "taux": round(justes / max(1, len(q)), 4)}


def juge_egal(candidat, reference) -> float:
    """La comparaison normalisée du juge, localisée pour éviter un import circulaire."""
    if candidat is None or reference is None:
        return 0.0
    norm = lambda s: " ".join(str(s).lower().split())
    return 1.0 if norm(candidat) == norm(reference) else 0.0


def fidelite_contenu(phrases: list[dict], bloc=None) -> dict:
    """Le taux de réponses au contenu : 0 tant que le bloc n'a pas de modèle."""
    bloc = bloc or bl.Heuristique()
    repondues = 0
    for p in phrases:
        if "?" not in p["texte"]:
            continue
        a = bloc.analyser(p["texte"], p["langue"])
        if repondre_contenu(a) is not None:
            repondues += 1
    q = sum(1 for p in phrases if "?" in p["texte"])
    return {"questions": q, "repondues": repondues,
            "taux": round(repondues / max(1, q), 4)}


def fluidite(a: bl.Annotation) -> float:
    """La part de la longueur restituée qui est du texte (pas des trous)."""
    r = rendre(a)
    return round(len(r) / max(1, len(a.texte)), 4)


def mesurer(phrases: list[dict], bloc=None) -> dict:
    bloc = bloc or bl.Heuristique()
    fid = 0.0
    flu = []
    details = []
    for p in phrases:
        a = bloc.analyser(p["texte"], p["langue"])
        f = min(fidelite(a, p["texte"]), fidelite_mots(a, p["texte"]),
                fidelite_pos(a, p["texte"]))
        fid += f
        flu.append(fluidite(a))
        if f < 1.0:
            details.append({"id": p["id"], "source": p["texte"], "rendu": rendre(a)[:80]})
    n = max(1, len(phrases))
    return {"phrases": len(phrases), "fidelite": round(fid / n, 4),
            "fluidite": round(sum(flu) / n, 4), "echecs": details[:5]}


def main() -> int:
    ph = charger()
    for nom, bloc in (("heuristique", bl.Heuristique()),
                      ("cascade", bl.Cascade(bl.Heuristique(), bl.MockNeuronal()))):
        r = mesurer(ph, bloc)
        print(nom, r["phrases"], "fidélité", r["fidelite"], "fluidité", r["fluidite"],
              "échecs", len(r["echecs"]))
        fid_pos = sum(fidelite_pos(bloc.analyser(p["texte"], p["langue"]), p["texte"])
                      for p in ph) / max(1, len(ph))
        print(nom, "POS", round(fid_pos, 4))
        fid_esp = sum(fidelite_pos_espaces(bloc.analyser(p["texte"], p["langue"]), p["texte"])
                      for p in ph) / max(1, len(ph))
        print(nom, "POS+espaces", round(fid_esp, 4))
        rap = sum(rappel_resume(bloc.analyser(p["texte"], p["langue"]), p["texte"])
                  for p in ph) / max(1, len(ph))
        print(nom, "résumé rappel", round(rap, 4))
        q = [p for p in ph if "?" in p["texte"]]
        fr = sum(fidelite_reponse(bloc.analyser(p["texte"], p["langue"])) for p in q) / max(1, len(q))
        print(nom, "réponse", len(q), "questions", round(fr, 4))
        print(nom, "réponse au contenu", fidelite_contenu(ph, bloc))
        print(nom, "extraction", fidelite_extraction(ph, bloc))
        print(nom, "dirigée", fidelite_dirigee(ph, bloc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
