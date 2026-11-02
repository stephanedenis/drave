"""gold_reel.py — 40 phrases réelles supplémentaires (20 françaises, 20 anglaises).

Elles ne sont pas des phrases du bloc ni du générateur : elles sont écrites après, avec leurs
POS, leurs segments GN/GV/GP/REL/SUB et leur pragmatique. Le fichier `gold_reel.json` est généré
par `construire()` ; le gold réel total devient **60 phrases** (20 de `gold.py` + 40).
"""
from __future__ import annotations

import json
import pathlib

PHRASES = [
    ("r001", "fr", "Le chien mange une pomme.",
     [("Le", "DET"), ("chien", "NOUN"), ("mange", "VERB"), ("une", "DET"), ("pomme", "NOUN")],
     [("GN", "Le chien", "agent"), ("GV", "mange", "prédicat"), ("GN", "une pomme", "patient")], {"acte": "assertion"}),
    ("r002", "fr", "La fille lit le journal.",
     [("La", "DET"), ("fille", "NOUN"), ("lit", "VERB"), ("le", "DET"), ("journal", "NOUN")],
     [("GN", "La fille", "agent"), ("GV", "lit", "prédicat"), ("GN", "le journal", "patient")], {"acte": "assertion"}),
    ("r003", "fr", "Nous aimons la musique.",
     [("Nous", "PRON"), ("aimons", "VERB"), ("la", "DET"), ("musique", "NOUN")],
     [("GN", "Nous", "agent"), ("GV", "aimons", "prédicat"), ("GN", "la musique", "patient")], {"acte": "assertion"}),
    ("r004", "fr", "Le soleil brille.",
     [("Le", "DET"), ("soleil", "NOUN"), ("brille", "VERB")],
     [("GN", "Le soleil", "agent"), ("GV", "brille", "prédicat")], {"acte": "assertion"}),
    ("r005", "fr", "Elle parle à son frère.",
     [("Elle", "PRON"), ("parle", "VERB"), ("à", "PREP"), ("son", "DET"), ("frère", "NOUN")],
     [("GN", "Elle", "agent"), ("GV", "parle", "prédicat"), ("GP", "à son frère", "destinataire", "parle")], {"acte": "assertion"}),
    ("r006", "fr", "Les élèves écoutent le professeur.",
     [("Les", "DET"), ("élèves", "NOUN"), ("écoutent", "VERB"), ("le", "DET"), ("professeur", "NOUN")],
     [("GN", "Les élèves", "agent"), ("GV", "écoutent", "prédicat"), ("GN", "le professeur", "patient")], {"acte": "assertion"}),
    ("r007", "fr", "Le chat dort sur la chaise.",
     [("Le", "DET"), ("chat", "NOUN"), ("dort", "VERB"), ("sur", "PREP"), ("la", "DET"), ("chaise", "NOUN")],
     [("GN", "Le chat", "agent"), ("GV", "dort", "prédicat"), ("GP", "sur la chaise", "lieu", "dort")], {"acte": "assertion"}),
    ("r008", "fr", "Il pleut depuis hier.",
     [("Il", "PRON"), ("pleut", "VERB"), ("depuis", "PREP"), ("hier", "ADV")],
     [("GN", "Il", "agent"), ("GV", "pleut", "prédicat"), ("GP", "depuis hier", "temps", "pleut")], {"acte": "assertion"}),
    ("r009", "fr", "Je ne comprends pas.",
     [("Je", "PRON"), ("ne", "ADV"), ("comprends", "VERB"), ("pas", "ADV")],
     [("GN", "Je", "agent"), ("GV", "ne comprends pas", "prédicat")], {"acte": "assertion", "negation": True}),
    ("r010", "fr", "Tu viens demain ?",
     [("Tu", "PRON"), ("viens", "VERB"), ("demain", "ADV")],
     [("GN", "Tu", "agent"), ("GV", "viens", "prédicat")], {"acte": "question"}),
    ("r011", "fr", "Le train part à midi.",
     [("Le", "DET"), ("train", "NOUN"), ("part", "VERB"), ("à", "PREP"), ("midi", "NOUN")],
     [("GN", "Le train", "agent"), ("GV", "part", "prédicat"), ("GP", "à midi", "temps", "part")], {"acte": "assertion"}),
    ("r012", "fr", "La voiture est rapide.",
     [("La", "DET"), ("voiture", "NOUN"), ("est", "AUX"), ("rapide", "ADJ")],
     [("GN", "La voiture", "agent"), ("GV", "est rapide", "prédicat")], {"acte": "assertion"}),
    ("r013", "fr", "Ils ont acheté une maison.",
     [("Ils", "PRON"), ("ont", "AUX"), ("acheté", "VERB"), ("une", "DET"), ("maison", "NOUN")],
     [("GN", "Ils", "agent"), ("GV", "ont acheté", "prédicat"), ("GN", "une maison", "patient")], {"acte": "assertion"}),
    ("r014", "fr", "Le livre que j'ai lu est passionnant.",
     [("Le", "DET"), ("livre", "NOUN"), ("que", "CONJ"), ("j'ai", "PRON"), ("lu", "VERB"),
      ("est", "AUX"), ("passionnant", "ADJ")],
     [("GN", "Le livre", "patient"), ("REL", "que j'ai lu", "qualité", "livre"), ("GV", "est passionnant", "prédicat")], {"acte": "assertion"}),
    ("r015", "fr", "Le film dont elle parle est sorti.",
     [("Le", "DET"), ("film", "NOUN"), ("dont", "PRON"), ("elle", "PRON"), ("parle", "VERB"),
      ("est", "AUX"), ("sorti", "VERB")],
     [("GN", "Le film", "patient"), ("REL", "dont elle parle", "qualité", "film"), ("GV", "est sorti", "prédicat")], {"acte": "assertion"}),
    ("r016", "fr", "Elle est peut-être fatiguée.",
     [("Elle", "PRON"), ("est", "AUX"), ("peut-être", "ADV"), ("fatiguée", "ADJ")],
     [("GN", "Elle", "agent"), ("GV", "est peut-être fatiguée", "prédicat")], {"acte": "assertion", "modalite": True}),
    ("r017", "fr", "Nous devons travailler.",
     [("Nous", "PRON"), ("devons", "VERB"), ("travailler", "VERB")],
     [("GN", "Nous", "agent"), ("GV", "devons travailler", "prédicat")], {"acte": "assertion", "modalite": True}),
    ("r018", "fr", "La souris est prête à manger.",
     [("La", "DET"), ("souris", "NOUN"), ("est", "AUX"), ("prête", "ADJ"), ("à", "PREP"), ("manger", "VERB")],
     [("GN", "La souris", "agent"), ("GV", "est prête", "prédicat"), ("GP", "à manger", "but", ["prête", "souris"])],
     {"acte": "assertion", "double_sens": True}),
    ("r019", "fr", "Le vent souffle fort.",
     [("Le", "DET"), ("vent", "NOUN"), ("souffle", "VERB"), ("fort", "ADV")],
     [("GN", "Le vent", "agent"), ("GV", "souffle", "prédicat")], {"acte": "assertion"}),
    ("r020", "fr", "Les enfants jouent dans le parc.",
     [("Les", "DET"), ("enfants", "NOUN"), ("jouent", "VERB"), ("dans", "PREP"), ("le", "DET"), ("parc", "NOUN")],
     [("GN", "Les enfants", "agent"), ("GV", "jouent", "prédicat"), ("GP", "dans le parc", "lieu", ["jouent", "enfants"])], {"acte": "assertion"}),
    ("r021", "en", "The dog eats an apple.",
     [("The", "DET"), ("dog", "NOUN"), ("eats", "VERB"), ("an", "DET"), ("apple", "NOUN")],
     [("GN", "The dog", "agent"), ("GV", "eats", "prédicat"), ("GN", "an apple", "patient")], {"acte": "assertion"}),
    ("r022", "en", "The girl reads the newspaper.",
     [("The", "DET"), ("girl", "NOUN"), ("reads", "VERB"), ("the", "DET"), ("newspaper", "NOUN")],
     [("GN", "The girl", "agent"), ("GV", "reads", "prédicat"), ("GN", "the newspaper", "patient")], {"acte": "assertion"}),
    ("r023", "en", "We love music.",
     [("We", "PRON"), ("love", "VERB"), ("music", "NOUN")],
     [("GN", "We", "agent"), ("GV", "love", "prédicat"), ("GN", "music", "patient")], {"acte": "assertion"}),
    ("r024", "en", "The sun shines.",
     [("The", "DET"), ("sun", "NOUN"), ("shines", "VERB")],
     [("GN", "The sun", "agent"), ("GV", "shines", "prédicat")], {"acte": "assertion"}),
    ("r025", "en", "She talks to her brother.",
     [("She", "PRON"), ("talks", "VERB"), ("to", "PREP"), ("her", "DET"), ("brother", "NOUN")],
     [("GN", "She", "agent"), ("GV", "talks", "prédicat"), ("GP", "to her brother", "destinataire", "talks")], {"acte": "assertion"}),
    ("r026", "en", "The students listen to the teacher.",
     [("The", "DET"), ("students", "NOUN"), ("listen", "VERB"), ("to", "PREP"), ("the", "DET"), ("teacher", "NOUN")],
     [("GN", "The students", "agent"), ("GV", "listen", "prédicat"), ("GP", "to the teacher", "destinataire", "listen")], {"acte": "assertion"}),
    ("r027", "en", "The cat sleeps on the chair.",
     [("The", "DET"), ("cat", "NOUN"), ("sleeps", "VERB"), ("on", "PREP"), ("the", "DET"), ("chair", "NOUN")],
     [("GN", "The cat", "agent"), ("GV", "sleeps", "prédicat"), ("GP", "on the chair", "lieu", "sleeps")], {"acte": "assertion"}),
    ("r028", "en", "It rains since yesterday.",
     [("It", "PRON"), ("rains", "VERB"), ("since", "PREP"), ("yesterday", "ADV")],
     [("GN", "It", "agent"), ("GV", "rains", "prédicat"), ("GP", "since yesterday", "temps", "rains")], {"acte": "assertion"}),
    ("r029", "en", "I do not understand.",
     [("I", "PRON"), ("do", "AUX"), ("not", "ADV"), ("understand", "VERB")],
     [("GN", "I", "agent"), ("GV", "do not understand", "prédicat")], {"acte": "assertion", "negation": True}),
    ("r030", "en", "You come tomorrow?",
     [("You", "PRON"), ("come", "VERB"), ("tomorrow", "ADV")],
     [("GN", "You", "agent"), ("GV", "come", "prédicat")], {"acte": "question"}),
    ("r031", "en", "The train leaves at noon.",
     [("The", "DET"), ("train", "NOUN"), ("leaves", "VERB"), ("at", "PREP"), ("noon", "NOUN")],
     [("GN", "The train", "agent"), ("GV", "leaves", "prédicat"), ("GP", "at noon", "temps", "leaves")], {"acte": "assertion"}),
    ("r032", "en", "The car is fast.",
     [("The", "DET"), ("car", "NOUN"), ("is", "AUX"), ("fast", "ADJ")],
     [("GN", "The car", "agent"), ("GV", "is fast", "prédicat")], {"acte": "assertion"}),
    ("r033", "en", "They bought a house.",
     [("They", "PRON"), ("bought", "VERB"), ("a", "DET"), ("house", "NOUN")],
     [("GN", "They", "agent"), ("GV", "bought", "prédicat"), ("GN", "a house", "patient")], {"acte": "assertion"}),
    ("r034", "en", "The book that I read is exciting.",
     [("The", "DET"), ("book", "NOUN"), ("that", "CONJ"), ("I", "PRON"), ("read", "VERB"),
      ("is", "AUX"), ("exciting", "ADJ")],
     [("GN", "The book", "patient"), ("REL", "that I read", "qualité", "book"), ("GV", "is exciting", "prédicat")], {"acte": "assertion"}),
    ("r035", "en", "The film she talks about is out.",
     [("The", "DET"), ("film", "NOUN"), ("she", "PRON"), ("talks", "VERB"), ("about", "PREP"),
      ("is", "AUX"), ("out", "ADV")],
     [("GN", "The film", "patient"), ("REL", "she talks about", "qualité", "film"), ("GV", "is out", "prédicat")], {"acte": "assertion"}),
    ("r036", "en", "She is maybe tired.",
     [("She", "PRON"), ("is", "AUX"), ("maybe", "ADV"), ("tired", "ADJ")],
     [("GN", "She", "agent"), ("GV", "is maybe tired", "prédicat")], {"acte": "assertion", "modalite": True}),
    ("r037", "en", "We must work.",
     [("We", "PRON"), ("must", "AUX"), ("work", "VERB")],
     [("GN", "We", "agent"), ("GV", "must work", "prédicat")], {"acte": "assertion", "modalite": True}),
    ("r038", "en", "The mouse is ready to eat.",
     [("The", "DET"), ("mouse", "NOUN"), ("is", "AUX"), ("ready", "ADJ"), ("to", "PREP"), ("eat", "VERB")],
     [("GN", "The mouse", "agent"), ("GV", "is ready", "prédicat"), ("GP", "to eat", "but", ["ready", "mouse"])],
     {"acte": "assertion", "double_sens": True}),
    ("r039", "en", "The wind blows hard.",
     [("The", "DET"), ("wind", "NOUN"), ("blows", "VERB"), ("hard", "ADV")],
     [("GN", "The wind", "agent"), ("GV", "blows", "prédicat")], {"acte": "assertion"}),
    ("r040", "en", "The children play in the park.",
     [("The", "DET"), ("children", "NOUN"), ("play", "VERB"), ("in", "PREP"), ("the", "DET"), ("park", "NOUN")],
     [("GN", "The children", "agent"), ("GV", "play", "prédicat"), ("GP", "in the park", "lieu", ["play", "children"])], {"acte": "assertion"}),
]


def construire() -> dict:
    phrases = []
    for pid, langue, texte, pos, segments, pragma in PHRASES:
        mots, curseur = [], 0
        for mot, classe in pos:
            i = texte.find(mot, curseur)
            assert i >= 0, f"{pid}: token introuvable {mot!r}"
            mots.append({"texte": mot, "pos": classe, "debut": i, "fin": i + len(mot)})
            curseur = i + len(mot)
        segs, curseur = [], 0
        for item in segments:
            typ, txt, role = item[:3]
            cible = item[3] if len(item) > 3 else None
            cibles = cible if isinstance(cible, list) else ([cible] if cible else [])
            i = texte.find(txt, curseur)
            assert i >= 0, f"{pid}: segment introuvable {txt!r}"
            seg = {"type": typ, "texte": txt, "role": role, "debut": i, "fin": i + len(txt)}
            if cibles:
                seg["cibles"] = cibles
                seg["cible"] = cibles[0]
            segs.append(seg)
            curseur = i + len(txt)
        phrases.append({"id": pid, "langue": langue, "texte": texte, "mots": mots,
                        "segments": segs, "pragma": pragma, "source": "reel"})
    return {"version": 1, "source": "reel", "note": "40 phrases réelles supplémentaires.",
            "phrases": phrases}


if __name__ == "__main__":
    sortie = pathlib.Path(__file__).with_name("gold_reel.json")
    sortie.write_text(json.dumps(construire(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(PHRASES)} phrases réelles → {sortie}")
