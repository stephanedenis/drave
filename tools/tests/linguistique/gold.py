"""gold.py — le gold v0 du bloc linguistique : POS, syntagmes, pragmatique.

20 phrases (14 françaises, 6 anglaises), **écrites à la main** après le bloc : elles ne sont pas
tirées des 7 phrases du banc S ni des exemples du générateur. Chaque phrase porte ses tokens/POS,
ses segments (type + texte, spans calculés par sous-chaîne) et son pragmatique (acte, négation,
modalité, double sens). Le fichier `gold.json` est généré par `construire()`.
"""
from __future__ import annotations

import json
import pathlib

PHRASES = [
    ("g001", "fr", "Le chat dort.",
     [("Le", "DET"), ("chat", "NOUN"), ("dort", "VERB")],
     [("GN", "Le chat", "agent"), ("GV", "dort", "prédicat")], {"acte": "assertion"}),
    ("g002", "fr", "Le chat de la voisine dort.",
     [("Le", "DET"), ("chat", "NOUN"), ("de", "PREP"), ("la", "DET"), ("voisine", "NOUN"), ("dort", "VERB")],
     [("GN", "Le chat", "agent"), ("GP", "de la voisine", "possession", ["chat"]), ("GV", "dort", "prédicat")], {"acte": "assertion"}),
    ("g003", "fr", "La femme a vu l'homme dans le parc.",
     [("La", "DET"), ("femme", "NOUN"), ("a", "AUX"), ("vu", "VERB"), ("l'homme", "DET"),
      ("dans", "PREP"), ("le", "DET"), ("parc", "NOUN")],
     [("GN", "La femme", "agent"), ("GV", "a vu", "prédicat"), ("GN", "l'homme", "patient"),
      ("GP", "dans le parc", "lieu", ["vu", "l'homme"])], {"acte": "assertion"}),
    ("g004", "fr", "Il a couru pour attraper le bus.",
     [("Il", "PRON"), ("a", "AUX"), ("couru", "VERB"), ("pour", "PREP"), ("attraper", "VERB"),
      ("le", "DET"), ("bus", "NOUN")],
     [("GN", "Il", "agent"), ("GV", "a couru", "prédicat"), ("GP", "pour attraper le bus", "but", ["couru"])], {"acte": "assertion"}),
    ("g005", "fr", "Elle a dit qu'elle viendrait hier.",
     [("Elle", "PRON"), ("a", "AUX"), ("dit", "VERB"), ("qu'elle", "CONJ"), ("viendrait", "VERB"), ("hier", "ADV")],
     [("GN", "Elle", "agent"), ("GV", "a dit", "prédicat"), ("SUB", "qu'elle viendrait", "contenu", ["dit"])], {"acte": "assertion"}),
    ("g006", "fr", "Le chien du voisin aboie la nuit.",
     [("Le", "DET"), ("chien", "NOUN"), ("du", "PREP"), ("voisin", "NOUN"), ("aboie", "VERB"),
      ("la", "DET"), ("nuit", "NOUN")],
     [("GN", "Le chien", "agent"), ("GP", "du voisin", "possession", ["chien"]), ("GV", "aboie", "prédicat"),
      ("GN", "la nuit", "temps")], {"acte": "assertion"}),
    ("g007", "fr", "Les enfants jouent dans le jardin.",
     [("Les", "DET"), ("enfants", "NOUN"), ("jouent", "VERB"), ("dans", "PREP"), ("le", "DET"), ("jardin", "NOUN")],
     [("GN", "Les enfants", "agent"), ("GV", "jouent", "prédicat"), ("GP", "dans le jardin", "lieu", ["jouent", "enfants"])], {"acte": "assertion"}),
    ("g008", "fr", "Marie lit un livre.",
     [("Marie", "NOUN"), ("lit", "VERB"), ("un", "DET"), ("livre", "NOUN")],
     [("GN", "Marie", "agent"), ("GV", "lit", "prédicat"), ("GN", "un livre", "patient")], {"acte": "assertion"}),
    ("g009", "fr", "Il ne dort pas.",
     [("Il", "PRON"), ("ne", "ADV"), ("dort", "VERB"), ("pas", "ADV")],
     [("GN", "Il", "agent"), ("GV", "ne dort pas", "prédicat")], {"acte": "assertion", "negation": True}),
    ("g010", "fr", "Viens ici !",
     [("Viens", "VERB"), ("ici", "ADV")],
     [("GV", "Viens", "prédicat"), ("GP", "ici", "lieu", ["Viens"])], {"acte": "exclamation"}),
    ("g011", "fr", "Le livre que j'ai lu est intéressant.",
     [("Le", "DET"), ("livre", "NOUN"), ("que", "CONJ"), ("j'ai", "PRON"), ("lu", "VERB"),
      ("est", "AUX"), ("intéressant", "ADJ")],
     [("GN", "Le livre", "patient"), ("REL", "que j'ai lu", "qualité", ["livre"]), ("GV", "est intéressant", "prédicat")], {"acte": "assertion"}),
    ("g012", "fr", "Le canard est prêt à manger.",
     [("Le", "DET"), ("canard", "NOUN"), ("est", "AUX"), ("prêt", "ADJ"), ("à", "PREP"), ("manger", "VERB")],
     [("GN", "Le canard", "agent"), ("GV", "est prêt", "prédicat"), ("GP", "à manger", "but", ["prêt", "canard"])], {"acte": "assertion", "double_sens": True}),
    ("g013", "fr", "Peux-tu venir ?",
     [("Peux-tu", "VERB"), ("venir", "VERB")],
     [("GV", "Peux-tu venir", "prédicat")], {"acte": "question", "reponse": "oui"}),
    ("g014", "fr", "J'ai vu l'homme avec le télescope.",
     [("J'ai", "PRON"), ("vu", "VERB"), ("l'homme", "DET"), ("avec", "PREP"), ("le", "DET"), ("télescope", "NOUN")],
     [("GN", "J'ai", "agent"), ("GV", "vu", "prédicat"), ("GN", "l'homme", "patient"),
      ("GP", "avec le télescope", "moyen", "vu")], {"acte": "assertion"}),
    ("g015", "en", "The cat sleeps.",
     [("The", "DET"), ("cat", "NOUN"), ("sleeps", "VERB")],
     [("GN", "The cat", "agent"), ("GV", "sleeps", "prédicat")], {"acte": "assertion"}),
    ("g016", "en", "The woman saw the man in the park.",
     [("The", "DET"), ("woman", "NOUN"), ("saw", "VERB"), ("the", "DET"), ("man", "NOUN"),
      ("in", "PREP"), ("the", "DET"), ("park", "NOUN")],
     [("GN", "The woman", "agent"), ("GV", "saw", "prédicat"), ("GN", "the man", "patient"),
      ("GP", "in the park", "lieu", ["saw", "man"])], {"acte": "assertion"}),
    ("g017", "en", "She said that she would come yesterday.",
     [("She", "PRON"), ("said", "VERB"), ("that", "CONJ"), ("she", "PRON"), ("would", "AUX"),
      ("come", "VERB"), ("yesterday", "ADV")],
     [("GN", "She", "agent"), ("GV", "said", "prédicat"), ("SUB", "that she would come", "contenu", ["said"])],
     {"acte": "assertion", "modalite": True}),
    ("g018", "en", "He does not sleep.",
     [("He", "PRON"), ("does", "AUX"), ("not", "ADV"), ("sleep", "VERB")],
     [("GN", "He", "agent"), ("GV", "does not sleep", "prédicat")], {"acte": "assertion", "negation": True}),
    ("g019", "en", "It might rain.",
     [("It", "PRON"), ("might", "AUX"), ("rain", "VERB")],
     [("GN", "It", "agent"), ("GV", "might rain", "prédicat")], {"acte": "assertion", "modalite": True}),
    ("g020", "en", "The duck is ready to eat.",
     [("The", "DET"), ("duck", "NOUN"), ("is", "AUX"), ("ready", "ADJ"), ("to", "PREP"), ("eat", "VERB")],
     [("GN", "The duck", "agent"), ("GV", "is ready", "prédicat"), ("GP", "to eat", "but", ["ready", "duck"])],
     {"acte": "assertion", "double_sens": True}),
]


def construire() -> dict:
    phrases = []
    for pid, langue, texte, pos, segments, pragma in PHRASES:
        mots, curseur = [], 0
        for mot, classe in pos:
            i = texte.find(mot, curseur)
            assert i >= 0, f"{pid}: token introuvable {mot!r} après {curseur}"
            mots.append({"texte": mot, "pos": classe, "debut": i, "fin": i + len(mot)})
            curseur = i + len(mot)
        segs, curseur = [], 0
        for item in segments:
            typ, txt, role = item[:3]
            cible = item[3] if len(item) > 3 else None
            cibles = cible if isinstance(cible, list) else ([cible] if cible else [])
            i = texte.find(txt, curseur)
            assert i >= 0, f"{pid}: segment introuvable {txt!r} après {curseur}"
            seg = {"type": typ, "texte": txt, "role": role, "debut": i, "fin": i + len(txt)}
            if cibles:
                seg["cibles"] = cibles
                seg["cible"] = cibles[0]
            segs.append(seg)
            curseur = i + len(txt)
        phrases.append({"id": pid, "langue": langue, "texte": texte, "mots": mots,
                        "segments": segs, "pragma": pragma})
    return {"version": 1, "phrases": phrases,
            "note": "Gold v0, écrit à la main ; spans calculés par sous-chaîne."}


if __name__ == "__main__":
    sortie = pathlib.Path(__file__).with_name("gold.json")
    sortie.write_text(json.dumps(construire(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(PHRASES)} phrases, {sum(len(p[3]) for p in PHRASES)} tokens → {sortie}")
