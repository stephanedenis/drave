#!/usr/bin/env python3
"""bloc_linguistique.py — le bloc d'étiquetage linguistique, du graphème à la pragmatique.

Un seul contrat (`BlocLinguistique.analyser`) et **plusieurs implémentations** :

  - `Heuristique` : CPU, déterministe, ultra-rapide ; elle étiquette la surface et produit des
    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
  - `MockNeuronal` : une implémentation neuronale **de contrat**, déterministe, pour tester la
    substitution et le parallèle sans GPU ;
  - `NeuronalLLM` : l'adaptateur réel, qui interroge un modèle local (`llama-cli`) et rend le
    même type d'annotation ;
  - `NeuronalLLMPOS` : le **tagger** neuronal réel — un modèle local, une liste de tokens, des
    POS alignés par grammaire GBNF ; c'est l'implémentation qualifiée sur le gold ;
  - `Parallele` et `Cascade` : les deux modes de composition. Le parallèle fusionne les
    étiquettes par confiance ; la cascade n'envoie au neuronal que le **résidu** des niveaux
    que l'heuristique ne couvre pas.

La sortie est une **annotation typée** — pas le corps de la RSN : chaque étiquette porte son
`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script` et ses `candidats`.
La couche sémantique ne reçoit que `unites_semantiques` ; l'heuristique peut donc l'activer à
une **fraction** du coût, avant même que le neuronal ait fini.

    python3 tools/bloc_linguistique.py --texte "Le chat de la voisine qui dort sur le toit se réveille."
    python3 tools/bloc_linguistique.py --mode parallele --fichier page.txt --json
    python3 tools/bloc_linguistique.py --autotest --udhr data/udhr/articles.jsonl

Le contrat est dans `docs/implantation/bloc-linguistique.md` ; la fiche dans
`reports/rapport-bloc-linguistique.md` ; la porte dans `tools/porte-bloc-linguistique.sh`.
"""
from __future__ import annotations

import os

import argparse
import collections
import copy
import json
import pathlib
import re
import subprocess
import sys
import threading
import time
import unicodedata
import urllib.request
from dataclasses import dataclass, field
from typing import Protocol, Sequence

RACINE = pathlib.Path(__file__).resolve().parent.parent
NIVEAUX = ("graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours",
           "pragmatique", "document")
SOURCES = ("heuristique", "neuronal", "humain")
SCRIPT_NEUTRE = "Zyyy"

# --------------------------------------------------------------------------- types


@dataclass(frozen=True)
class Span:
    debut: int
    fin: int

    def json(self) -> dict:
        return {"debut": self.debut, "fin": self.fin}


@dataclass
class Etiquette:
    niveau: str
    type: str
    valeur: str
    debut: int
    fin: int
    source: str = "heuristique"
    confiance: float = 0.5
    candidats: list[str] = field(default_factory=list)
    langue: str = "und"
    script: str = SCRIPT_NEUTRE
    meta: dict = field(default_factory=dict)

    def json(self) -> dict:
        return {
            "niveau": self.niveau, "type": self.type, "valeur": self.valeur,
            "debut": self.debut, "fin": self.fin, "source": self.source,
            "confiance": round(float(self.confiance), 4),
            "candidats": list(self.candidats), "langue": self.langue,
            "script": self.script, "meta": dict(self.meta),
        }


@dataclass
class Annotation:
    texte: str
    langue: str = "und"
    script: str = SCRIPT_NEUTRE
    etiquettes: list[Etiquette] = field(default_factory=list)
    refus: str = ""
    trace: list[dict] = field(default_factory=list)
    cout: dict = field(default_factory=dict)
    unites_semantiques: list[Span] = field(default_factory=list)
    fraction_semantique: float = 0.0
    source: str = "heuristique"
    contexte: str = ""

    def par_niveau(self) -> dict[str, list[Etiquette]]:
        sortie: dict[str, list[Etiquette]] = collections.defaultdict(list)
        for e in self.etiquettes:
            sortie[e.niveau].append(e)
        return dict(sortie)

    def couverture(self) -> dict[str, float]:
        """La confiance maximale par niveau — la couverture *déclarée*, pas une précision."""
        return {n: round(max((e.confiance for e in es), default=0.0), 4)
                for n, es in self.par_niveau().items()}

    def json(self, avec_duree: bool = False) -> dict:
        cout = dict(self.cout)
        if not avec_duree:
            cout.pop("duree_s", None)
        return {
            "texte": self.texte, "langue": self.langue, "script": self.script,
            "source": self.source, "refus": self.refus,
            "etiquettes": [e.json() for e in self.etiquettes],
            "unites_semantiques": [u.json() for u in self.unites_semantiques],
            "fraction_semantique": round(float(self.fraction_semantique), 4),
            "trace": list(self.trace), "cout": cout, "contexte": self.contexte,
        }


class BlocLinguistique(Protocol):
    nom: str

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation: ...


class RefusNeuronal(RuntimeError):
    """Le modèle n'a pas rendu une annotation exploitable — le contrat refuse, il n'invente pas."""


# --------------------------------------------------------------------------- profils de langue


def _normaliser(texte: str) -> str:
    return unicodedata.normalize("NFC", texte).casefold()


def _trigrammes(texte: str) -> list[str]:
    t = _normaliser(texte)
    return [t[i:i + 3] for i in range(max(0, len(t) - 2))]


def _profil(texte: str, top: int = 200) -> dict[str, int]:
    c = collections.Counter(_trigrammes(texte))
    return dict(c.most_common(top))


def charger_profils_udhr(chemin: pathlib.Path, train=(0, 14), test=(15, 30),
                         min_train: int = 5, min_test: int = 3,
                         top: int = 200) -> tuple[dict[str, dict], list[tuple[str, str, str]]]:
    """Construit des profils de trigrammes par langue et un jeu de test tenu à l'écart.

    Le corpus UDHR est **parallèle** : les articles 0–14 servent de profil, les articles 15–30
    de test. Un profil est une donnée, pas un prompt : il se versionne et se rejoue.
    """
    par_langue: dict[str, list[tuple[int, str, str]]] = collections.defaultdict(list)
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        d = json.loads(ligne)
        par_langue[d.get("iso3", "und")].append((int(d.get("art", 0)),
                                                 d.get("texte", ""), d.get("script", SCRIPT_NEUTRE)))
    profils: dict[str, dict] = {}
    tests: list[tuple[str, str, str]] = []
    for langue, articles in par_langue.items():
        if langue == "und":
            continue
        train_txt = [t for a, t, _ in articles if train[0] <= a <= train[1]]
        test_lst = [(t, s) for a, t, s in articles if test[0] <= a <= test[1]]
        if len(train_txt) < min_train or len(test_lst) < min_test:
            continue
        scripts = collections.Counter(s for _, _, s in articles)
        profils[langue] = {
            "trigrammes": _profil(" ".join(train_txt), top),
            "script": scripts.most_common(1)[0][0],
            "n_train": len(train_txt), "n_test": len(test_lst),
        }
        tests.extend((langue, t, s) for t, s in test_lst)
    return profils, tests


def _score_profil(tri: collections.Counter, profil: dict[str, int]) -> float:
    total = sum(tri.values())
    if not total:
        return 0.0
    return sum(min(c, profil.get(tg, 0)) for tg, c in tri.items()) / total


def detecter_langue(texte: str, profils: dict[str, dict] | None = None,
                    indice: str | None = None) -> tuple[str, float, dict[str, float]]:
    """La langue par recouvrement de trigrammes ; l'indice est un **prior**, pas un verdict."""
    if profils:
        tri = collections.Counter(_trigrammes(texte))
        scores = {langue: _score_profil(tri, p["trigrammes"]) for langue, p in profils.items()}
        if indice and indice in scores:
            scores[indice] = min(1.0, scores[indice] + 0.02)
        if not scores:
            return "und", 0.0, {}
        classement = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
        langue, meilleur = classement[0]
        second = classement[1][1] if len(classement) > 1 else 0.0
        if meilleur <= 0.0:
            return "und", 0.0, scores
        confiance = min(1.0, (meilleur - second) / meilleur + 0.2 * meilleur)
        return langue, round(confiance, 4), scores
    # profil de secours : mots-outils de quelques langues
    mots = set(re.findall(r"[a-zà-ÿ']+", _normaliser(texte)))
    scores = {l: len(mots & set(LEXIQUES[l])) / max(1, len(mots)) for l in LEXIQUES}
    if indice and indice in scores:
        scores[indice] += 0.02
    if not scores or max(scores.values()) <= 0:
        return "und", 0.0, scores
    langue = max(scores, key=scores.get)
    return langue, round(min(1.0, scores[langue] * 2), 4), scores


# --------------------------------------------------------------------------- script


def _script_char(ch: str) -> str:
    if not ch.isalpha():
        return ""
    try:
        nom = unicodedata.name(ch)
    except ValueError:
        return ""
    prefixes = (
        ("LATIN", "Latn"), ("CYRILLIC", "Cyrl"), ("GREEK", "Grek"), ("ARABIC", "Arab"),
        ("HEBREW", "Hebr"), ("DEVANAGARI", "Deva"), ("THAI", "Thai"), ("HIRAGANA", "Jpan"),
        ("KATAKANA", "Jpan"), ("HANGUL", "Hang"), ("CJK", "Hani"), ("IDEOGRAPH", "Hani"),
        ("BENGALI", "Beng"), ("TAMIL", "Taml"), ("TELUGU", "Telu"), ("KANNADA", "Knda"),
        ("MALAYALAM", "Mlym"), ("GUJARATI", "Gujr"), ("GURMUKHI", "Guru"), ("SINHALA", "Sinh"),
        ("MYANMAR", "Mymr"), ("ETHIOPIC", "Ethi"), ("GEORGIAN", "Geor"), ("ARMENIAN", "Armn"),
        ("THAANA", "Thaa"), ("SYRIAC", "Syrc"), ("CHEROKEE", "Cher"), ("TIBETAN", "Tibt"),
        ("MONGOLIAN", "Mong"), ("CANADIAN SYLLABICS", "Cans"), ("TIFINAGH", "Tfng"),
        ("TAI VIET", "Tavt"), ("CHAKMA", "Cakm"), ("YI ", "Yiii"), ("JAVANESE", "Java"),
        ("TAI THAM", "Lana"), ("GRANTHA", "Gran"), ("VAI", "Vaii"), ("TAGALOG", "Tglg"),
        ("ADLAM", "Adlm"), ("LAO", "Laoo"), ("KHMER", "Khmr"),
    )
    for prefixe, code in prefixes:
        if prefixe in nom:
            return code
    return ""


def detecter_script(texte: str) -> str:
    c = collections.Counter(_script_char(ch) for ch in texte if ch.isalpha())
    c.pop("", None)
    if not c:
        return SCRIPT_NEUTRE
    if c.get("Jpan", 0) or (c.get("Hani", 0) and (c.get("Jpan", 0) or c.get("Hang", 0))):
        return "Jpan"
    if c.get("Hang", 0):
        return "Hang"
    if c.get("Hani", 0):
        return "Hani"
    return c.most_common(1)[0][0]


# --------------------------------------------------------------------------- lexiques


LEXIQUES = {
    "fr": set("le la les l un une des de du d à au aux et ou mais donc or ni car que qui quoi "
              "dont où je tu il elle on nous vous ils elles me te se lui leur mon ma mes ton "
              "ta tes son sa ses ce cet cette ces est sont était étaient être avoir ai as a "
              "avons avez ont ne pas plus jamais rien très dans sur sous avec pour par en".split()),
    "en": set("the a an of to and or but nor for so yet in on at by with from as is are was "
              "were be been being have has had do does did not no never this that these those "
              "i you he she it we they me him her us them my your his its our their".split()),
    "de": set("der die das den dem des ein eine einer eines und oder aber denn sondern nicht "
              "kein keine ist sind war waren sein haben hat hatte ich du er sie es wir ihr "
              "mit von zu aus bei nach über unter für durch".split()),
    "es": set("el la los las un una unos unas de del a al y o pero sino que quien como donde "
              "yo tú él ella nosotros vosotros ellos me te se le les mi tu su nuestro vuestro "
              "es son era eran ser haber he has ha han no nunca muy en con por para".split()),
    "it": set("il lo la i gli le un uno una di del della a al alla e o ma però che chi cui "
              "dove io tu lui lei noi voi loro mi ti si ci vi mio tuo suo nostro vostro è sono "
              "era erano essere avere ho hai ha hanno non mai molto in con per su tra fra".split()),
    "pt": set("o a os as um uma uns umas de do da dos das a ao aos à às e ou mas porém que quem "
              "como onde eu tu ele ela nós vós eles elas me te se lhe lhes meu tua seu nosso "
              "vosso é são era eram ser haver tenho tem têm não nunca muito em com por para".split()),
    "nl": set("de het een en of maar want dat die dit deze ik jij hij zij wij jullie zij mij "
              "jou hem haar ons hen mijn jouw zijn haar ons jullie hun is zijn was waren hebben "
              "heeft had niet geen zeer in op aan met van voor door".split()),
}

POS_FERME = {
    "fr": {
        "DET": set("le la les l un une ce cet cette ces mon ma mes ton ta tes son sa ses notre nos votre vos leur leurs quel quelle quels quelles".split()),
        "PREP": set("à a au aux de du des d en dans par pour sur sous avec sans chez vers entre depuis pendant durant contre malgré selon près loin devant derrière après avant".split()),
        "PRON": set("je j tu il elle on nous vous ils elles me te se lui leur moi toi soi y en ce cela ça qui que quoi dont où".split()),
        "CONJ": set("et ou mais donc or ni car quand comme si parce puisque lorsque pendant qu".split()),
        "AUX": set("est sont était étaient été être ai as a avons avez ont avait avaient eu avoir suis es sommes êtes".split()),
        "ADV": set("ne n pas plus jamais rien très bien mal ici hier demain aujourd'hui peut-être fort souvent toujours déjà encore tard tôt ainsi alors aussi".split()),
        "NUM": set("deux trois quatre cinq six sept huit neuf dix".split()),
    },
    "en": {
        "DET": set("the a an this that these those my your his her its our their".split()),
        "PREP": set("of to in on at by with from for about into over under between through during without".split()),
        "PRON": set("i you he she it we they me him her us them who whom which that".split()),
        "CONJ": set("and or but nor for so yet because although while if when".split()),
        "AUX": set("is are was were be been being have has had do does did can could will would shall should may might must".split()),
        "ADV": set("not never very well here yesterday today tomorrow often always already still too".split()),
        "NUM": set("one two three four five six seven eight nine ten".split()),
    },
}

VERBES = {
    "fr": set("dort dorment dormait mange mangeons mangent mangeait court courent courait vu voir vois "
              "voit voyons voyez voient dit disons dites disent viendrait viens vient venons venez "
              "viennent aboie aboient joue jouons jouent jouait lit lisons lisez lisent pars partons "
              "partez partent fini finis finit finissons finissez finissent arrive arrives arrivez "
              "arrivent pleut pleuvoir habite habites habitent parle parlons parlez parlent explique "
              "expliquons expliquez expliquent souffle soufflent chante chantent chantes peut peux "
              "pouvons pouvez peuvent doit devons devez doivent pourrait pourrais pourrions pourriez "
              "pourraient devrait devrais voudrais voudrait veux veut voulons voulez veulent prend "
              "prends prenons prenez prennent donne donnes donnons donnez donnent trouve trouves "
              "trouvons trouvez trouvent cherche cherches cherchons cherchez cherchent regarde "
              "regardes regardons regardez regardent écoute écoutes écoutons écoutez écoutent ouvre "
              "ouvres ouvrons ouvrez ouvrent ferme fermes fermons fermez ferment commence commences "
              "commençons commencez commencent essaie essaies essayons essayez essaient attrape "
              "attrapes attrapons attrapez attrapent".split()),
    "en": set("sleeps sleep slept saw see seen says said comes came plays played reads read is are "
              "was were have has had does did do come go goes went make makes made take takes took "
              "give gives gave find finds found open opens opened close closes closed start starts "
              "started finish finishes finished look looks looked listen listens listened buy buys "
              "bought sell sells sold rain rains rained eat eats ate".split()),
}
ADJECTIFS = {
    "fr": set("petite petit petits petites grand grande grands grandes rouge rouges vieille vieux "
              "vieilles vieil intéressant intéressante intéressants intéressantes malade malades prêt "
              "prête prêts prêtes content contents heureux heureuse triste beau belle beaux belles "
              "joli jolie bon bonne bons bonnes mauvais mauvaise jeune jeunes nouveau nouvelle "
              "nouveaux nouvelles chaud chaude froid froide noir noire blanc blanche vert verte bleu "
              "bleue long longue court courte facile difficile important importante".split()),
    "en": set("ready interesting old young big small red blue green black white good bad happy sad "
              "beautiful nice long short easy difficult important".split()),
}
MOTS_DOUBLE_SENS = set("canard avocat livre temps voler glace note carte point mousse manche mode "
                       "duck".split())

SUFFIXES = ("ment", "tions", "tion", "ités", "ité", "eux", "euse", "ables", "able", "isme",
            "istes", "iste", "ance", "ence", "er", "ir", "ez", "ons", "ait", "aient", "ing",
            "ed", "ly", "ness", "ful", "less", "ship", "ous", "ive", "al")
PREFIXES = ("re", "ré", "dé", "des", "pré", "pro", "anti", "auto", "co", "con", "in", "im",
            "un", "non", "sur", "sous", "inter", "trans", "ultra")

CONNECTEURS = {
    "contraste": set("mais cependant pourtant néanmoins toutefois en revanche whereas however "
                     "but yet although though nevertheless".split()),
    "cause": set("car parce puisque comme because since".split()),
    "conséquence": set("donc ainsi alors par conséquent consequently therefore hence so".split()),
    "but": set("pour afin pour que afin que in order to so that".split()),
}

VERBES_IMPERATIFS = set("va viens prends fais dis regarde écoute donne cherche trouve ouvre ferme "
                        "go take come look give find open close".split())


def _role_gp(prep: str) -> str:
    p = prep.casefold()
    if p in {"dans", "sur", "sous", "chez", "vers", "entre", "devant", "derrière", "près", "loin",
             "in", "on", "at", "under", "between"}:
        return "lieu"
    if p in {"pendant", "depuis", "durant", "avant", "après", "during", "since", "before", "after"}:
        return "temps"
    if p in {"pour", "afin", "for", "to"}:
        return "but"
    if p in {"par", "by"}:
        # `par` + GN est l'**agent** d'un passif (`Le chat est mangé par le chien`) ;
        # `avec`/`sans` restent le moyen.
        return "agent"
    if p in {"avec", "sans", "with", "without"}:
        return "moyen"
    if p in {"à", "a", "au", "aux", "to"}:
        return "destinataire"
    if p in {"de", "du", "des", "of", "from"}:
        return "theme"
    return "complément"


# --------------------------------------------------------------------------- heuristique


class Heuristique:
    """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""

    nom = "heuristique"

    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
                 seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
                 union: bool = True):
        self.profils = profils
        self.segmenter_s = segmenter_s
        self.seuil_ouvert = seuil_ouvert
        self.seuil_langue = seuil_langue
        self.union = union

    # -- langues / script ---------------------------------------------------
    def _langue(self, texte: str, indice: str | None) -> tuple[str, float, str]:
        langue, conf, _ = detecter_langue(texte, self.profils, indice)
        script = detecter_script(texte)
        if conf < self.seuil_langue:
            return "und", conf, script
        return langue, conf, script

    # -- tokens -------------------------------------------------------------
    @staticmethod
    def _mots(texte: str) -> list[tuple[int, int, str, str]]:
        motif = re.compile(r"\b[ldmtsnLDMTNS]['’](?=\w)|\w+(?:['’\-]\w+)*|\d+(?:[.,]\d+)*|https?://\S+|[\U0001F300-\U0001FAFF]|[^\w\s]")
        sortie = []
        for m in motif.finditer(texte):
            t = m.group()
            if t.startswith(("http://", "https://")):
                typ = "url"
            elif t[0].isdigit():
                typ = "nombre"
            elif re.fullmatch(r"[^\w\s]", t):
                typ = "ponctuation"
            elif len(t) == 1 and ord(t) >= 0x1F300:
                typ = "emoji"
            else:
                typ = "mot"
            sortie.append((m.start(), m.end(), t, typ))
        return sortie

    @staticmethod
    def _phrases(texte: str) -> list[tuple[int, int, str, str]]:
        # frontières : ponctuation forte + espace ; on protège les abréviations et les décimales
        motif = re.compile(r"[^.!?…]+(?:[.!?…]+|$)", re.S)
        sortie = []
        for m in motif.finditer(texte):
            morceau = m.group()
            if not morceau.strip():
                continue
            debut = m.start()
            fin = m.end()
            # une phrase qui finit par une abréviation connue n'est pas finie
            while re.search(r"\b(?:M|MM|Mme|Dr|Pr|etc|cf|p|pp|art|vol)\.\s*$", texte[debut:fin]):
                suivant = motif.search(texte, fin)
                if not suivant:
                    break
                fin = suivant.end()
                morceau = texte[debut:fin]
            typ = "interrogative" if "?" in morceau else ("exclamative" if "!" in morceau else "déclarative")
            sortie.append((debut, fin, morceau, typ))
        return sortie

    @staticmethod
    def _negation(phrase: str) -> bool:
        return bool(re.search(r"\b(?:ne|n['’])\b.{0,40}\b(?:pas|plus|jamais|rien|guère)\b", phrase, re.I)
                    or re.search(r"\b(?:not|no|never|none|nothing|n't)\b", phrase, re.I))

    @staticmethod
    def _modalite(phrase: str) -> bool:
        return bool(re.search(r"\b(?:peut|peuvent|peux|pouvons|pouvez|doit|doivent|devons|devez|"
                              r"pourrait|pourraient|pourrais|devrait|devraient|voudrais|voudrait|"
                              r"faut|falloir|might|may|must|should|could|would|can)\b", phrase, re.I))

    # -- POS ----------------------------------------------------------------
    def _pos(self, langue: str, mot: str) -> tuple[str, bool, float]:
        lex = POS_FERME.get(langue, POS_FERME["fr"])
        n = _normaliser(mot).split("'")[0].split("’")[0]
        for classe, mots in lex.items():
            if n in mots:
                return classe, False, 0.92
        if n in VERBES.get(langue, VERBES["fr"]):
            return "VERB", True, 0.72
        if n in ADJECTIFS.get(langue, ADJECTIFS["fr"]):
            return "ADJ", True, 0.68
        if re.fullmatch(r"\d+(?:[.,]\d+)*", mot):
            return "NUM", False, 0.95
        if mot[:1].isupper() and mot[1:].islower() and mot not in {"Le", "La", "Les", "Un", "Une", "The"}:
            return "NOUN", True, 0.55
        if len(n) >= 4 and n.endswith(("ment", "ly")):
            return "ADV", True, 0.45
        if len(n) >= 4 and n.endswith(("tion", "sion", "ness", "ity", "ité", "ance", "ence")):
            return "NOUN", True, 0.45
        if len(n) >= 4 and n.endswith(("er", "ir", "ing", "ed")):
            return "VERB", True, 0.4
        if len(n) >= 4 and n.endswith(("eux", "euse", "able", "ible", "ous", "ive", "al")):
            return "ADJ", True, 0.38
        return ("NOUN" if (n and n[0].islower()) else "MOT"), True, 0.3

    # -- morphèmes ----------------------------------------------------------
    @staticmethod
    def _morphemes(mot: str) -> list[tuple[str, int, int, str]]:
        n = _normaliser(mot)
        sortie = []
        for suf in SUFFIXES:
            if len(n) > len(suf) + 2 and n.endswith(suf):
                sortie.append(("suffixe", len(mot) - len(suf), len(mot), suf))
                break
        for pre in PREFIXES:
            if len(n) > len(pre) + 2 and n.startswith(pre):
                sortie.append(("préfixe", 0, len(pre), pre))
                break
        return sortie

    # -- syntagmes ----------------------------------------------------------
    def _syntagmes_s(self, texte: str) -> list[dict] | None:
        if not self.segmenter_s:
            return None
        try:
            if str(RACINE / "tools/structures") not in sys.path:
                sys.path.insert(0, str(RACINE / "tools/structures"))
            import generateur  # le générateur S, importé en lecture seule
            return generateur.analyser(texte)
        except Exception:
            return None

    def _cibles_s(self, texte: str) -> dict:
        """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).

        Lecture seule de l'API interne du S : `_tokens`/`_segmente` rendent les `Segment` avec
        `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut retenu est la cible la plus proche
        (GP, puis GN, puis GV), comme le premier candidat de `analyser`.
        """
        if not self.segmenter_s:
            return {}
        try:
            import generateur
            base = generateur._segmente(texte, generateur._tokens(texte))
            return {(s.debut, s.fin, s.type): (s.cible_gp or s.cible_nom or s.cible_verbe)
                    for s in base}
        except Exception:
            return {}

    @staticmethod
    def _cible_proche(texte: str, segment: dict, gvs: list[dict]) -> str | None:
        """La cible d'un segment : le **verbe du GV le plus proche** (règle de proximité).

        Rend `None` si le segment est lui-même un GV ou s'il n'y a pas de GV. Le verbe est le
        dernier token du GV (`a vu` → `vu`, `est mangé` → `mangé`).
        """
        if segment.get("type") == "GV" or not gvs:
            return None
        def ecart(g: dict) -> int:
            if g["fin"] <= segment["debut"]:
                return segment["debut"] - g["fin"]
            if g["debut"] >= segment["fin"]:
                return g["debut"] - segment["fin"]
            return 0
        g = min(gvs, key=ecart)
        mots = re.findall(r"[\wÀ-ÿ'-]+", texte[g["debut"]:g["fin"]])
        return mots[-1] if mots else None

    @staticmethod
    def _verbes_proches(texte: str, segment: dict, gvs: list[dict],
                        k: int = 3) -> list[str]:
        """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
        if segment.get("type") == "GV" or not gvs:
            return []
        def ecart(g: dict) -> int:
            if g["fin"] <= segment["debut"]:
                return segment["debut"] - g["fin"]
            if g["debut"] >= segment["fin"]:
                return g["debut"] - segment["fin"]
            return 0
        verbes: list[str] = []
        for g in sorted(gvs, key=ecart)[:k]:
            mots = re.findall(r"[\wÀ-ÿ'-]+", texte[g["debut"]:g["fin"]])
            if mots and mots[-1] not in verbes:
                verbes.append(mots[-1])
        return verbes

    def _syntagmes_simple(self, texte: str, langue: str) -> list[dict]:
        mots = self._mots(texte)
        lex = POS_FERME.get(langue, POS_FERME["fr"])
        segments: list[dict] = []
        i = 0
        while i < len(mots):
            d, f, t, typ = mots[i]
            n = _normaliser(t)
            if typ == "mot" and n in lex.get("DET", set()):
                j = i + 1
                while j < len(mots) and mots[j][3] == "mot" and _normaliser(mots[j][2]) not in lex.get("PREP", set()) | lex.get("CONJ", set()) | lex.get("AUX", set()):
                    j += 1
                role = "groupe nominal"
                # le passif sans `par` : GN + AUX (être) + participe → le sujet est un patient
                if j < len(mots) and _normaliser(mots[j][2]) in {
                        "est", "sont", "était", "étaient", "été", "sera", "seront",
                        "suis", "es", "sommes", "êtes"}:
                    role = "patient"
                segments.append({"type": "GN", "role": role, "niveau": 0,
                                 "debut": d, "fin": mots[j - 1][1],
                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
                i = j
                continue
            if typ == "mot" and n in lex.get("PREP", set()) and i + 1 < len(mots):
                j = i + 1
                while j < len(mots) and mots[j][3] == "mot":
                    j += 1
                segments.append({"type": "GP", "role": _role_gp(t), "niveau": 1,
                                 "debut": d, "fin": mots[j - 1][1],
                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
                i = j
                continue
            if typ == "mot" and (n in lex.get("AUX", set()) or (i + 1 < len(mots) and _normaliser(mots[i + 1][2]) in lex.get("AUX", set()))):
                j = i + 1
                while j < len(mots) and mots[j][3] == "mot":
                    j += 1
                segments.append({"type": "GV", "role": "prédicat", "niveau": 0,
                                 "debut": d, "fin": mots[j - 1][1],
                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
                i = j
                continue
            if typ == "mot" and n in {"qui", "que", "qu", "dont", "où", "which", "that", "who"}:
                j = i + 1
                while j < len(mots) and mots[j][3] == "mot":
                    j += 1
                segments.append({"type": "REL", "role": "qualité", "niveau": 1,
                                 "debut": d, "fin": mots[j - 1][1],
                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
                i = j
                continue
            i += 1
        return segments

    # -- analyse ------------------------------------------------------------
    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        t0 = time.perf_counter()
        texte = texte or ""
        trace: list[dict] = []
        if not texte.strip() or not any(ch.isalpha() or ch.isdigit() for ch in texte):
            return Annotation(texte=texte, refus="vide", source=self.nom,
                              trace=[{"etape": "refus", "raison": "vide"}],
                              cout={"octets": len(texte.encode()), "duree_s": round(time.perf_counter() - t0, 6)})

        lg, conf_lg, script = self._langue(texte, langue)
        trace.append({"etape": "langue", "langue": lg, "script": script, "confiance": conf_lg,
                      "indice": langue or ""})
        etiquettes: list[Etiquette] = []
        unites: list[Span] = []

        # 1. graphème — des plages de classes, pas un caractère par étiquette
        classes = {"L": "lettres", "N": "chiffres", "P": "ponctuation", "Z": "espace",
                   "S": "symbole", "M": "marque"}
        i = 0
        while i < len(texte):
            cat = unicodedata.category(texte[i])[0]
            j = i + 1
            while j < len(texte) and unicodedata.category(texte[j])[0] == cat:
                j += 1
            if cat in classes:
                etiquettes.append(Etiquette("graphème", classes[cat], texte[i:j], i, j,
                                            self.nom, 0.99, langue=lg, script=script))
            i = j

        # 2. mot + POS fermées / ouvertes
        mots = self._mots(texte)
        for d, f, t, typ in mots:
            etiquettes.append(Etiquette("mot", typ, t, d, f, self.nom, 0.98, langue=lg, script=script))
            if typ == "mot":
                classe, ouvert, conf = self._pos(lg, t)
                etiquettes.append(Etiquette("pos", classe, t, d, f, self.nom, conf,
                                            candidats=[] if not ouvert else [classe.lower()],
                                            langue=lg, script=script, meta={"ouvert": ouvert}))
                if ouvert:
                    unites.append(Span(d, f))
                # 3. morphème (candidat, basse confiance)
                for genre, md, mf, aff in self._morphemes(t):
                    etiquettes.append(Etiquette("morphème", genre, aff, d + md, d + mf,
                                                self.nom, 0.32, candidats=[genre],
                                                langue=lg, script=script))

        # 4. phrase + pragmatique
        for d, f, p, typ in self._phrases(texte):
            etiquettes.append(Etiquette("phrase", "type", typ, d, f, self.nom, 0.85,
                                        langue=lg, script=script))
            if self._negation(p):
                etiquettes.append(Etiquette("phrase", "négation", "oui", d, f, self.nom, 0.65,
                                            langue=lg, script=script))
            if self._modalite(p):
                etiquettes.append(Etiquette("phrase", "modalité", "oui", d, f, self.nom, 0.55,
                                            langue=lg, script=script))
            premier = next((m.group() for m in re.finditer(r"\w+", p)), "")
            acte = ("question" if typ == "interrogative" else
                    "exclamation" if typ == "exclamative" else
                    "ordre" if premier.casefold() in VERBES_IMPERATIFS else "assertion")
            etiquettes.append(Etiquette("pragmatique", "acte", acte, d, f, self.nom, 0.45,
                                        candidats=["assertion", "question", "ordre"],
                                        langue=lg, script=script))
            if (" ou " in p or "«" in p or "“" in p
                    or any(m in _normaliser(p) for m in MOTS_DOUBLE_SENS)):
                etiquettes.append(Etiquette("pragmatique", "double_sens", "candidat", d, f,
                                            self.nom, 0.25, candidats=["littéral", "figuré"],
                                            langue=lg, script=script))

        # 5. syntagmes : le générateur S (candidats) ou un chunker simple
        cands = self._syntagmes_s(texte)
        cibles_s = self._cibles_s(texte) if cands else {}
        if cands:
            for c in cands[:1]:
                noms = [x.get("nom", "") for x in cands]
                for s in c.get("segments", []):
                    att = c.get("attachement") or {}
                    if att.get("segment") == s.get("texte"):
                        cible = att.get("cible")
                    else:
                        cible = cibles_s.get((s.get("debut"), s.get("fin"), s.get("type")))
                    if not cible:
                        gvs = [x for x in c.get("segments", []) if x.get("type") == "GV"]
                        cible = self._cible_proche(texte, s, gvs)
                    meta = {"role": s.get("role", ""), "niveau": s.get("niveau", 0)}
                    if cible:
                        meta["attachement"] = {"segment": s.get("texte", ""), "cible": cible}
                    gvs = [x for x in c.get("segments", []) if x.get("type") == "GV"]
                    candidats = list(noms) + self._verbes_proches(texte, s, gvs)
                    etiquettes.append(Etiquette("syntagme", s.get("type", "GN"),
                                                s.get("texte", ""), s.get("debut", 0),
                                                s.get("fin", 0), self.nom,
                                                0.55 if len(cands) == 1 else 0.4,
                                                candidats=candidats, langue=lg, script=script,
                                                meta=meta))
        else:
            for s in self._syntagmes_simple(texte, lg):
                meta = {"role": s["role"], "niveau": s["niveau"]}
                cible = self._cible_proche(texte, s, [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"])
                if cible:
                    meta["attachement"] = {"segment": s["texte"], "cible": cible}
                gvs_s = [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"]
                etiquettes.append(Etiquette("syntagme", s["type"], s["texte"], s["debut"],
                                            s["fin"], self.nom, 0.35,
                                            candidats=[s["type"]] + self._verbes_proches(texte, s, gvs_s),
                                            langue=lg, script=script, meta=meta))
        # 5 bis. union : les segments du chunker que le générateur S ne fournit pas
        if cands and self.union:
            deja = {(s.get("type"), s.get("debut"), s.get("fin"))
                    for s in cands[0].get("segments", [])}
            for s in self._syntagmes_simple(texte, lg):
                if (s["type"], s["debut"], s["fin"]) in deja:
                    continue
                etiquettes.append(Etiquette("syntagme", s["type"], s["texte"], s["debut"],
                                            s["fin"], self.nom, 0.30,
                                            candidats=[s["type"]], langue=lg, script=script,
                                            meta={"role": s["role"], "niveau": s["niveau"],
                                                  "union": True}))
    
        # 6. discours / document
        for d, f, p, _ in self._phrases(texte):
            mots_p = set(_normaliser(p).split())
            for relation, marqueurs in CONNECTEURS.items():
                touche = sorted(mots_p & marqueurs)
                if touche:
                    etiquettes.append(Etiquette("discours", "connecteur", touche[0], d, f,
                                                self.nom, 0.55, candidats=[relation],
                                                langue=lg, script=script))
                    break
        paragraphes = []
        for m in re.finditer(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", texte):
            if m.group().strip():
                paragraphes.append((m.start(), m.end(), m.group()))
        for d, f, p in paragraphes:
            etiquettes.append(Etiquette("discours", "paragraphe", "suite", d, f, self.nom, 0.5,
                                        candidats=["suite", "contraste", "cause", "conséquence"],
                                        langue=lg, script=script))
            titre = (p.lstrip().startswith("#") or
                     bool(re.match(r"^\s*(?:\d+[.)]|[IVXLC]+[.)])\s+", p)) or
                     (len(p.strip()) < 80 and p.strip().endswith((":", ".")) is False and
                      p.strip() == p.strip().upper()))
            etiquettes.append(Etiquette("document", "titre" if titre else "paragraphe",
                                        p.strip()[:60], d, f, self.nom, 0.7,
                                        langue=lg, script=script))
        if contexte:
            etiquettes.append(Etiquette("pragmatique", "contexte", contexte[:200], 0, len(texte),
                                        "humain", 1.0, langue=lg, script=script))

        # 7. unités sémantiques : ouvertes + syntagmes ambiguës, dédupliquées
        unites = _fusionner(unites)
        longueur = sum(u.fin - u.debut for u in unites)
        fraction = longueur / max(1, len(texte))
        etiquettes.sort(key=lambda e: (e.debut, e.fin, e.niveau))
        trace.append({"etape": "niveaux", "etiquettes": len(etiquettes),
                      "niveaux": sorted({e.niveau for e in etiquettes}),
                      "unites_semantiques": len(unites), "fraction": round(fraction, 4)})
        return Annotation(texte=texte, langue=lg, script=script, etiquettes=etiquettes,
                          trace=trace, source=self.nom, unites_semantiques=unites,
                          fraction_semantique=round(fraction, 4), contexte=contexte or "",
                          cout={"octets": len(texte.encode()), "caracteres": len(texte),
                                "etiquettes": len(etiquettes), "duree_s": round(time.perf_counter() - t0, 6)})


def _fusionner(spans: Sequence[Span]) -> list[Span]:
    spans = sorted(set(spans), key=lambda s: (s.debut, s.fin))
    sortie: list[Span] = []
    for s in spans:
        if not sortie or s.debut > sortie[-1].fin:
            sortie.append(s)
        else:
            sortie[-1] = Span(sortie[-1].debut, max(sortie[-1].fin, s.fin))
    return sortie


# --------------------------------------------------------------------------- neuronal


class MockNeuronal:
    """Le neuronal **de contrat** : même sortie, source `neuronal`, déterministe, sans GPU.

    Il ne prétend pas être un modèle : il prouve que le contrat accepte une autre implémentation,
    que le parallèle fusionne et que la cascade n'appelle le neuronal que sur le résidu.
    """

    nom = "neuronal"

    def __init__(self, profils: dict[str, dict] | None = None):
        self.profils = profils

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        t0 = time.perf_counter()
        lg = detecter_langue(texte, self.profils, langue)[0]
        if lg == "und" and langue:
            lg = langue
        script = detecter_script(texte)
        etiquettes: list[Etiquette] = []
        unites: list[Span] = []
        h = Heuristique(segmenter_s=False)
        for d, f, t, typ in h._mots(texte):
            if typ == "mot":
                classe, _, _ = h._pos(lg, t)
                if classe in {"NOUN", "VERB", "ADJ", "ADV", "MOT"}:
                    etiquettes.append(Etiquette("pos", classe, t, d, f, self.nom, 0.82,
                                                langue=lg, script=script, meta={"ouvert": True}))
                    unites.append(Span(d, f))
                    for genre, md, mf, aff in h._morphemes(t):
                        etiquettes.append(Etiquette("morphème", genre, aff, d + md, d + mf,
                                                    self.nom, 0.8, candidats=[genre],
                                                    langue=lg, script=script))
        for d, f, p, typ in h._phrases(texte):
            etiquettes.append(Etiquette("phrase", "type", typ, d, f, self.nom, 0.9,
                                        langue=lg, script=script))
            acte = ("question" if typ == "interrogative" else
                    "exclamation" if typ == "exclamative" else "assertion")
            etiquettes.append(Etiquette("pragmatique", "acte", acte, d, f, self.nom, 0.8,
                                        candidats=[acte], langue=lg, script=script))
        for s in h._syntagmes_simple(texte, lg):
            etiquettes.append(Etiquette("syntagme", s["type"], s["texte"], s["debut"], s["fin"],
                                        self.nom, 0.78, candidats=[s["type"]], langue=lg,
                                        script=script, meta={"role": s["role"], "niveau": s["niveau"]}))
        unites = _fusionner(unites)
        fraction = sum(u.fin - u.debut for u in unites) / max(1, len(texte))
        return Annotation(texte=texte, langue=lg, script=script, etiquettes=etiquettes,
                          source=self.nom, unites_semantiques=unites,
                          fraction_semantique=round(fraction, 4),
                          trace=[{"etape": "neuronal", "niveaux": sorted({e.niveau for e in etiquettes})}],
                          cout={"octets": len(texte.encode()), "etiquettes": len(etiquettes),
                                "duree_s": round(time.perf_counter() - t0, 6)})


class NeuronalLLM:
    """L'adaptateur réel : un prompt JSON, un modèle local, le même contrat.

    On ne simule pas un modèle absent : si `llama-cli` ou le fichier manque, l'adaptateur lève
    `RefusNeuronal`. Le `MockNeuronal` sert aux tests de contrat, pas à la qualité.
    """

    nom = "neuronal"

    def __init__(self, modele: str | pathlib.Path, llama_cli: str = "llama-cli",
                 max_jetons: int = 256, timeout: int = 120):
        self.modele = str(modele)
        self.llama_cli = llama_cli
        self.max_jetons = max_jetons
        self.timeout = timeout

    def _prompt(self, texte: str, langue: str | None, contexte: str | None) -> str:
        return (
            "Tu es un étiqueteur linguistique. Réponds UNIQUEMENT par un objet JSON valide, "
            "sans texte autour. Schéma : {\"langue\":\"fr\",\"script\":\"Latn\","
            "\"etiquettes\":[{\"niveau\":\"phrase|pragmatique|syntagme|pos\","
            "\"type\":\"...\",\"valeur\":\"...\",\"debut\":0,\"fin\":0,\"confiance\":0.8}]}. "
            "Niveaux attendus : phrase.type, pragmatique.acte, syntagme (GN/GV/GP/REL/SUB). "
            f"Langue indiquée : {langue or 'inconnue'}. Contexte : {contexte or 'aucun'}.\n"
            f"Texte : {texte}"
        )

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        t0 = time.perf_counter()
        if not pathlib.Path(self.modele).exists():
            raise RefusNeuronal(f"modèle absent : {self.modele}")
        try:
            sortie = subprocess.run(
                [self.llama_cli, "-m", self.modele, "-p", self._prompt(texte, langue, contexte),
                 "-n", str(self.max_jetons), "--temp", "0", "--no-display-prompt"],
                capture_output=True, text=True, timeout=self.timeout)
        except (OSError, subprocess.TimeoutExpired) as e:
            raise RefusNeuronal(str(e)) from e
        texte_sortie = sortie.stdout.strip()
        debut = texte_sortie.find("{")
        fin = texte_sortie.rfind("}")
        if debut < 0 or fin <= debut:
            raise RefusNeuronal(f"pas de JSON : {texte_sortie[:120]!r}")
        try:
            d = json.loads(texte_sortie[debut:fin + 1])
        except json.JSONDecodeError as e:
            raise RefusNeuronal(f"JSON invalide : {e}") from e
        lg = d.get("langue", langue or "und")
        lg = {"fr": "fra", "en": "eng", "de": "deu", "es": "spa", "it": "ita",
              "pt": "por", "nl": "nld"}.get(lg, lg)
        script = d.get("script", detecter_script(texte))
        etiquettes = []
        for e in d.get("etiquettes", []):
            if e.get("niveau") not in NIVEAUX:
                continue
            debut_e = max(0, min(int(e.get("debut", 0)), len(texte)))
            fin_e = max(debut_e, min(int(e.get("fin", debut_e)), len(texte)))
            etiquettes.append(Etiquette(e["niveau"], str(e.get("type", "")), str(e.get("valeur", "")),
                                        debut_e, fin_e, self.nom, float(e.get("confiance", 0.5)),
                                        langue=lg, script=script))
        return Annotation(texte=texte, langue=lg, script=script, etiquettes=etiquettes,
                          source=self.nom, trace=[{"etape": "neuronal-llm", "modele": self.modele}],
                          cout={"octets": len(texte.encode()), "etiquettes": len(etiquettes),
                                "duree_s": round(time.perf_counter() - t0, 6)})


CLASSES_POS = ("DET", "NOUN", "VERB", "ADJ", "ADV", "PREP", "PRON", "AUX", "CONJ",
               "NUM", "INTJ", "PUNCT")


def grammaire_pos(n: int) -> str:
    """La grammaire GBNF : exactement `n` classes, dans l'ordre — le JSON ne peut pas dériver."""
    corps = " tag" + ' ("," tag)' * (n - 1) if n > 1 else " tag"
    texte = 'root ::= "{\\"pos\\":["' + corps + ' "]}"\n'
    texte += "tag ::= " + " | ".join('"\\"%s\\""' % c for c in CLASSES_POS) + "\n"
    return texte


class NeuronalLLMPOS:
    """Le **tagger** neuronal réel : un modèle local, des POS alignés sur la tokenisation du bloc.

    Le modèle ne rend pas une annotation complète : il rend **une classe par token**, contrainte
    par une grammaire GBNF (`grammaire_pos`) qui interdit un JSON tronqué, un token manquant ou
    une classe hors du jeu. Les spans sont ceux de `Heuristique._mots` (la tokenisation du bloc),
    pas ceux que le modèle inventerait ; c'est ce qui rend la mesure POS exacte.

    Le modèle est servi par `llama-server` (`/v1/chat/completions`, `grammar`) : le serveur est
    lancé une fois, le modèle chargé une fois, et les 180 phrases coûtent une passe CPU, pas
    180 chargements. `transport` est injectable pour tester le contrat sans modèle.

    La confiance par défaut (`0.6`) est **celle du seuil ouvert de l'heuristique** (0.55) : dans
    une `Cascade`, le tagger ne remplace donc que les tokens que l'heuristique déclare peu sûrs,
    et laisse les classes fermées (0.92) à l'heuristique. C'est la politique mesurée.
    """

    nom = "neuronal"

    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18081",
                 confiance: float = 0.6, timeout: int = 180, max_jetons: int = 0,
                 transport=None, cache: bool = True):
        self.modele = str(modele)
        self.endpoint = endpoint.rstrip("/")
        self.confiance = float(confiance)
        self.timeout = timeout
        self.max_jetons = max_jetons
        self.transport = transport or self._post
        self.cache = cache
        self.appels = 0
        self._cache: dict[tuple[str, str | None], Annotation] = {}
        self._verrou = threading.Lock()

    @staticmethod
    def _tokens(texte: str) -> list[tuple[int, int, str]]:
        return [(d, f, t) for d, f, t, typ in Heuristique._mots(texte)
                if typ in ("mot", "nombre")]

    @staticmethod
    def _invite(tokens: Sequence[str]) -> str:
        return ("Tu es un étiqueteur morphosyntaxique du français. Pour chaque token de la liste, "
                "donne sa classe grammaticale. Réponds UNIQUEMENT par un objet JSON "
                "{\"pos\":[...]} avec exactement un élément par token, dans l'ordre, sans texte "
                "autour.\n"
                "Classes : " + ", ".join(CLASSES_POS) + ".\n"
                "Tokens : " + json.dumps(list(tokens), ensure_ascii=False) + "\nRéponse :")

    def _post(self, invite: str, grammaire: str, max_jetons: int) -> str:
        corps = {"messages": [{"role": "user", "content": invite}], "temperature": 0,
                 "max_tokens": max_jetons, "grammar": grammaire}
        requete = urllib.request.Request(
            self.endpoint + "/v1/chat/completions",
            data=json.dumps(corps).encode("utf-8"),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(requete, timeout=self.timeout) as reponse:
            sortie = json.loads(reponse.read().decode("utf-8"))
        return sortie["choices"][0]["message"]["content"]

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        t0 = time.perf_counter()
        script = detecter_script(texte)
        lg = langue or "und"
        if not texte.strip():
            return Annotation(texte=texte, langue=lg, script=script, refus="vide", source=self.nom)
        cle = (texte, langue)
        if self.cache and cle in self._cache:
            return copy.deepcopy(self._cache[cle])
        tokens = self._tokens(texte)
        if not tokens:
            return Annotation(texte=texte, langue=lg, script=script, refus="vide", source=self.nom)
        noms = [t for _, _, t in tokens]
        grammaire = grammaire_pos(len(noms))
        max_jetons = self.max_jetons or max(32, 6 * len(noms))
        try:
            with self._verrou:
                self.appels += 1
            sortie = self.transport(self._invite(noms), grammaire, max_jetons)
            debut, fin = sortie.find("{"), sortie.rfind("}")
            if debut < 0 or fin <= debut:
                raise ValueError(f"pas de JSON : {sortie[:120]!r}")
            pos = json.loads(sortie[debut:fin + 1]).get("pos")
            if not isinstance(pos, list) or len(pos) != len(tokens):
                raise ValueError(f"longueur POS {len(pos) if isinstance(pos, list) else '?'}"
                                 f" / {len(tokens)}")
            etiquettes = []
            for (d, f, mot), classe in zip(tokens, pos):
                classe = str(classe).upper()
                if classe not in CLASSES_POS:
                    raise ValueError(f"classe inconnue : {classe!r}")
                etiquettes.append(Etiquette("pos", classe, mot, d, f, self.nom, self.confiance,
                                            langue=lg, script=script, meta={"modele": True}))
            annotation = Annotation(texte=texte, langue=lg, script=script, etiquettes=etiquettes,
                                    source=self.nom,
                                    trace=[{"etape": "neuronal-pos", "modele": self.modele}],
                                    cout={"octets": len(texte.encode()), "tokens": len(tokens),
                                          "duree_s": round(time.perf_counter() - t0, 6)})
        except Exception as e:
            annotation = Annotation(texte=texte, langue=lg, script=script, source=self.nom,
                                    refus=f"neuronal-pos: {type(e).__name__}: {str(e)[:160]}",
                                    trace=[{"etape": "neuronal-pos", "erreur": str(e)[:160]}],
                                    cout={"octets": len(texte.encode()),
                                          "duree_s": round(time.perf_counter() - t0, 6)})
        if self.cache:
            self._cache[cle] = annotation
        return annotation


ETIQUETTES_BIO = ("O", "B-GN", "I-GN", "B-GV", "I-GV", "B-GP", "I-GP",
                  "B-REL", "I-REL", "B-SUB", "I-SUB")
TYPES_SYNTAGME = ("GN", "GV", "GP", "REL", "SUB")
EXEMPLES_BIO = (
    (["Un", "oiseau", "chante"], ["B-GN", "I-GN", "B-GV"]),
    (["La", "voisine", "de", "Paul", "arrive"],
     ["B-GN", "I-GN", "B-GP", "I-GP", "B-GV"]),
    (["Elle", "a", "vu", "le", "bus", "dans", "la", "rue"],
     ["B-GN", "B-GV", "I-GV", "B-GN", "I-GN", "B-GP", "I-GP", "I-GP"]),
    (["Le", "livre", "que", "tu", "lis", "tombe"],
     ["B-GN", "I-GN", "B-SUB", "I-SUB", "I-SUB", "B-GV"]),
    (["Il", "part", "demain"], ["B-GN", "B-GV", "O"]),
)


def grammaire_bio(n: int) -> str:
    """La grammaire GBNF des étiquettes BIO : exactement `n` étiquettes, dans l'ordre."""
    corps = " tag" + ' ("," tag)' * (n - 1) if n > 1 else " tag"
    texte = 'root ::= "{\\"bio\\":["' + corps + ' "]}"\n'
    texte += "tag ::= " + " | ".join('"\\"%s\\""' % t for t in ETIQUETTES_BIO) + "\n"
    return texte


class NeuronalLLMChunks:
    """Le tagger de **syntagmes** réel : une étiquette BIO par token, puis les spans.

    Le modèle local rend `{"bio":[...]}` — une étiquette par token, contrainte par la
    grammaire `grammaire_bio` ; le bloc **reconstruit** les syntagmes à partir des tokens et
    de leurs offsets. Un `B-X` ouvre un syntagme, un `I-X` le continue, `O` le ferme ; une
    étiquette `I-X` orpheline ouvre un syntagme (tolérance déclarée). Les spans sont donc
    ceux de la tokenisation du bloc, pas ceux que le modèle inventerait.

    Le prompt est **few-shot** (cinq exemples hors gold) : sans exemple, le modèle confond
    les frontières (DET hors GN, GV sans auxiliaire) et le gain disparaît. Le tagger rend
    le niveau `syntagme` seulement ; le POS et la pragmatique restent à `NeuronalLLMPOS` et
    à l'heuristique.
    """

    nom = "neuronal"

    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18082",
                 confiance: float = 0.6, timeout: int = 180, max_jetons: int = 0,
                 transport=None, cache: bool = True):
        self.modele = str(modele)
        self.endpoint = endpoint.rstrip("/")
        self.confiance = float(confiance)
        self.timeout = timeout
        self.max_jetons = max_jetons
        self.transport = transport or self._post
        self.cache = cache
        self.appels = 0
        self._cache: dict[tuple[str, str | None], Annotation] = {}
        self._verrou = threading.Lock()

    @staticmethod
    def _tokens(texte: str) -> list[tuple[int, int, str]]:
        return [(d, f, t) for d, f, t, typ in Heuristique._mots(texte)
                if typ in ("mot", "nombre")]

    @staticmethod
    def _invite(tokens: Sequence[str]) -> str:
        invite = ("Tu es un segmenteur en syntagmes du français. Pour chaque token de la liste, "
                  "donne son étiquette BIO. Réponds UNIQUEMENT par un objet JSON {\"bio\":[...]} "
                  "avec exactement un élément par token, dans l'ordre, sans texte autour.\n"
                  "Étiquettes : O (hors syntagme), B-GN/I-GN (groupe nominal), B-GV/I-GV (groupe "
                  "verbal), B-GP/I-GP (groupe prépositionnel), B-REL/I-REL (relative), "
                  "B-SUB/I-SUB (subordonnée). B-X ouvre un syntagme, I-X le continue, O est un "
                  "token hors syntagme.\nExemples :\n")
        for toks, tags in EXEMPLES_BIO:
            invite += ("Tokens : " + json.dumps(toks, ensure_ascii=False) + " -> "
                       + json.dumps({"bio": tags}, ensure_ascii=False) + "\n")
        return invite + "Tokens : " + json.dumps(list(tokens), ensure_ascii=False) + "\nRéponse :"

    def _post(self, invite: str, grammaire: str, max_jetons: int) -> str:
        corps = {"messages": [{"role": "user", "content": invite}], "temperature": 0,
                 "max_tokens": max_jetons, "grammar": grammaire}
        requete = urllib.request.Request(
            self.endpoint + "/v1/chat/completions",
            data=json.dumps(corps).encode("utf-8"),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(requete, timeout=self.timeout) as reponse:
            sortie = json.loads(reponse.read().decode("utf-8"))
        return sortie["choices"][0]["message"]["content"]

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        t0 = time.perf_counter()
        script = detecter_script(texte)
        lg = langue or "und"
        if not texte.strip():
            return Annotation(texte=texte, langue=lg, script=script, refus="vide", source=self.nom)
        cle = (texte, langue)
        if self.cache and cle in self._cache:
            return copy.deepcopy(self._cache[cle])
        tokens = self._tokens(texte)
        if not tokens:
            return Annotation(texte=texte, langue=lg, script=script, refus="vide", source=self.nom)
        noms = [t for _, _, t in tokens]
        grammaire = grammaire_bio(len(noms))
        max_jetons = self.max_jetons or max(32, 8 * len(noms))
        try:
            with self._verrou:
                self.appels += 1
            sortie = self.transport(self._invite(noms), grammaire, max_jetons)
            debut, fin = sortie.find("{"), sortie.rfind("}")
            if debut < 0 or fin <= debut:
                raise ValueError(f"pas de JSON : {sortie[:120]!r}")
            bio = json.loads(sortie[debut:fin + 1]).get("bio")
            if not isinstance(bio, list) or len(bio) != len(tokens):
                raise ValueError(f"longueur BIO {len(bio) if isinstance(bio, list) else '?'}"
                                 f" / {len(tokens)}")
            etiquettes = []
            courant: list | None = None
            for (d, f, mot), etiquette in zip(tokens, bio):
                etiquette = str(etiquette).upper()
                if etiquette not in ETIQUETTES_BIO:
                    raise ValueError(f"étiquette inconnue : {etiquette!r}")
                if etiquette == "O":
                    if courant:
                        etiquettes.append(_syntagme_bio(courant, texte, self.nom, self.confiance,
                                                        lg, script))
                        courant = None
                    continue
                prefixe, typ = etiquette.split("-", 1)
                if prefixe == "B" or courant is None or courant[0] != typ:
                    if courant:
                        etiquettes.append(_syntagme_bio(courant, texte, self.nom,
                                                        self.confiance, lg, script))
                    courant = [typ, d, f]
                else:
                    courant[2] = f
            if courant:
                etiquettes.append(_syntagme_bio(courant, texte, self.nom, self.confiance,
                                                lg, script))
            annotation = Annotation(texte=texte, langue=lg, script=script, etiquettes=etiquettes,
                                    source=self.nom,
                                    trace=[{"etape": "neuronal-syntagmes", "modele": self.modele}],
                                    cout={"octets": len(texte.encode()), "tokens": len(tokens),
                                          "syntagmes": len(etiquettes),
                                          "duree_s": round(time.perf_counter() - t0, 6)})
        except Exception as e:
            annotation = Annotation(texte=texte, langue=lg, script=script, source=self.nom,
                                    refus=f"neuronal-syntagmes: {type(e).__name__}: {str(e)[:160]}",
                                    trace=[{"etape": "neuronal-syntagmes", "erreur": str(e)[:160]}],
                                    cout={"octets": len(texte.encode()),
                                          "duree_s": round(time.perf_counter() - t0, 6)})
        if self.cache:
            self._cache[cle] = annotation
        return annotation


def _syntagme_bio(courant: list, texte: str, nom: str, confiance: float,
                  langue: str, script: str) -> Etiquette:
    typ, debut, fin = courant
    return Etiquette("syntagme", typ, texte[debut:fin], debut, fin, nom, confiance,
                     langue=langue, script=script, meta={"bio": True})


class NeuronalLLMCompose:
    """Deux taggers neuronaux, **une** annotation : POS + syntagmes, même contrat.

    Le composite n'invente rien : il appelle les deux taggers (chacun avec son cache), réunit
    leurs étiquettes et leurs traces, et laisse `source = neuronal`. C'est le bloc que la
    cascade complète branche ; la pragmatique reste à l'heuristique, qui la tient à 1,0 sur le
    gold. Un refus d'un des deux taggers n'efface pas l'autre : l'annotation est **partielle**,
    et `refus` dit lequel a manqué.
    """

    nom = "neuronal"

    def __init__(self, pos: BlocLinguistique, chunks: BlocLinguistique,
                 pragma: BlocLinguistique | None = None):
        self.pos = pos
        self.chunks = chunks
        self.pragma = pragma

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        a = self.pos.analyser(texte, langue, contexte)
        b = self.chunks.analyser(texte, langue, contexte)
        c = self.pragma.analyser(texte, langue, contexte) if self.pragma else None
        etiquettes = a.etiquettes + b.etiquettes + (c.etiquettes if c else [])
        refus = "; ".join(x for x in (a.refus, b.refus, c.refus if c else "") if x)
        lg = a.langue if a.langue != "und" else b.langue
        script = a.script if a.script != SCRIPT_NEUTRE else b.script
        return Annotation(
            texte=texte, langue=lg, script=script, etiquettes=etiquettes,
            source=self.nom, refus=refus,
            trace=a.trace + b.trace + (c.trace if c else []) + [
                {"etape": "compose",
                 "niveaux": sorted({e.niveau for e in etiquettes})}],
            cout={"octets": len(texte.encode()), "etiquettes": len(etiquettes),
                  "duree_s": round(a.cout.get("duree_s", 0.0) + b.cout.get("duree_s", 0.0)
                                   + (c.cout.get("duree_s", 0.0) if c else 0.0), 6)})


ACTES = ("assertion", "question", "exclamation")


def grammaire_pragma() -> str:
    """La grammaire GBNF de l'objet pragmatique : quatre champs, des valeurs fermées."""
    texte = ('root ::= "{\\"acte\\":" acte ",\\"negation\\":" bool ",\\"modalite\\":" bool '
             '",\\"double_sens\\":" bool "}"\n')
    texte += 'acte ::= ' + ' | '.join('"\\"%s\\""' % a for a in ACTES) + '\n'
    texte += 'bool ::= "true" | "false"\n'
    return texte


class NeuronalLLMPragmatique:
    """Le tagger **pragmatique** réel : acte, négation, modalité, double sens.

    Le modèle local rend un objet JSON à quatre champs, contraint par la grammaire
    `grammaire_pragma` : l'acte (`assertion`, `question`, `exclamation`), puis trois
    booléens. Le bloc construit les étiquettes `pragmatique.acte`, `phrase.négation`,
    `phrase.modalité` et `pragmatique.double_sens` ; c'est le même contrat que l'heuristique.
    La confiance 0,6 le destine à la cascade : l'acte et le double sens passent devant
    l'heuristique (0,45), la négation et la modalité restent à l'heuristique (0,85).
    """
    nom = "neuronal"

    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18082",
                 confiance: float = 0.6, timeout: int = 120, max_jetons: int = 64,
                 transport=None, cache: bool = True):
        self.modele = str(modele)
        self.endpoint = endpoint.rstrip("/")
        self.confiance = float(confiance)
        self.timeout = timeout
        self.max_jetons = max_jetons
        self.transport = transport or self._post
        self.cache = cache
        self.appels = 0
        self._cache: dict[tuple[str, str | None], Annotation] = {}
        self._verrou = threading.Lock()

    @staticmethod
    def _invite(texte: str) -> str:
        return ("Tu es un étiqueteur pragmatique du français. Analyse la phrase et réponds "
                "UNIQUEMENT par un objet JSON {\"acte\":\"assertion|question|exclamation\","
                "\"negation\":true|false,\"modalite\":true|false,\"double_sens\":true|false}. "
                "acte = l'acte de parole ; negation = une négation explicite ; modalite = "
                "possibilité, obligation ou incertitude ; double_sens = une ambiguïté voulue. "
                f"Texte : {texte}")

    def _post(self, invite: str, grammaire: str, max_jetons: int) -> str:
        corps = {"messages": [{"role": "user", "content": invite}], "temperature": 0,
                 "max_tokens": max_jetons, "grammar": grammaire}
        requete = urllib.request.Request(
            self.endpoint + "/v1/chat/completions",
            data=json.dumps(corps).encode("utf-8"),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(requete, timeout=self.timeout) as reponse:
            sortie = json.loads(reponse.read().decode("utf-8"))
        return sortie["choices"][0]["message"]["content"]

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        t0 = time.perf_counter()
        script = detecter_script(texte)
        lg = langue or "und"
        if not texte.strip():
            return Annotation(texte=texte, langue=lg, script=script, refus="vide", source=self.nom)
        cle = (texte, langue)
        if self.cache and cle in self._cache:
            return copy.deepcopy(self._cache[cle])
        try:
            with self._verrou:
                self.appels += 1
            sortie = self.transport(self._invite(texte), grammaire_pragma(), self.max_jetons)
            debut, fin = sortie.find("{"), sortie.rfind("}")
            if debut < 0 or fin <= debut:
                raise ValueError(f"pas de JSON : {sortie[:120]!r}")
            donnees = json.loads(sortie[debut:fin + 1])
            acte = str(donnees.get("acte", "")).lower()
            if acte not in ACTES:
                raise ValueError(f"acte inconnu : {acte!r}")
            negation = bool(donnees.get("negation", False))
            modalite = bool(donnees.get("modalite", False))
            double_sens = bool(donnees.get("double_sens", False))
            n = len(texte)
            etiquettes = [Etiquette("pragmatique", "acte", acte, 0, n, self.nom,
                                    self.confiance, langue=lg, script=script)]
            if negation:
                etiquettes.append(Etiquette("phrase", "négation", "", 0, n, self.nom,
                                            self.confiance, langue=lg, script=script))
            if modalite:
                etiquettes.append(Etiquette("phrase", "modalité", "", 0, n, self.nom,
                                            self.confiance, langue=lg, script=script))
            if double_sens:
                etiquettes.append(Etiquette("pragmatique", "double_sens", "", 0, n, self.nom,
                                            self.confiance, langue=lg, script=script))
            annotation = Annotation(texte=texte, langue=lg, script=script, etiquettes=etiquettes,
                                    source=self.nom,
                                    trace=[{"etape": "neuronal-pragmatique", "modele": self.modele}],
                                    cout={"octets": len(texte.encode()),
                                          "duree_s": round(time.perf_counter() - t0, 6)})
        except Exception as e:
            annotation = Annotation(texte=texte, langue=lg, script=script, source=self.nom,
                                    refus=f"neuronal-pragmatique: {type(e).__name__}: {str(e)[:160]}",
                                    trace=[{"etape": "neuronal-pragmatique", "erreur": str(e)[:160]}],
                                    cout={"octets": len(texte.encode()),
                                          "duree_s": round(time.perf_counter() - t0, 6)})
        if self.cache:
            self._cache[cle] = annotation
        return annotation


# --------------------------------------------------------------------------- compositions


def _supprimer_chevauchements(etiquettes: list[Etiquette],
                              priorite_syntagme: str = "heuristique") -> list[Etiquette]:
    """Les alternatives se suppriment **par type** quand les types sont complémentaires.

    `pos` et `syntagme` sont des alternatives de **span** : on garde la plus confiante.
    Pour le **syntagme**, la politique par défaut (`heuristique`) garde la segmentation de
    l'heuristique ; `confiance` laisse la plus confiante gagner (le tagger neuronal à 0,6
    passe devant l'heuristique à 0,4). `phrase` (type/négation/modalité), `pragmatique` (acte/double_sens/contexte), `discours`
    (paragraphe/connecteur) et `document` (titre/paragraphe) portent des types **complémentaires**
    sur le même span : les supprimer ensemble effacerait la négation au profit du type."""
    modes = {"pos": "span", "syntagme": "span", "phrase": "type", "pragmatique": "type",
             "discours": "type", "document": "type"}
    gardees: list[Etiquette] = [e for e in etiquettes if e.niveau not in modes]
    for niveau, mode in modes.items():
        groupes = {}
        for e in (x for x in etiquettes if x.niveau == niveau):
            groupes.setdefault(e.type if mode == "type" else "", []).append(e)
        for _, es in groupes.items():
            if niveau == "syntagme" and priorite_syntagme == "heuristique":
                candidates = sorted(es, key=lambda e: (0 if e.source == "heuristique" else 1,
                                                       e.fin - e.debut, -e.confiance))
            else:
                candidates = sorted(es, key=lambda e: (-e.confiance, e.debut, e.fin))
            retenues: list[Etiquette] = []
            for e in candidates:
                if any(not (e.fin <= g.debut or e.debut >= g.fin) for g in retenues):
                    continue
                retenues.append(e)
            gardees.extend(retenues)
    return sorted(gardees, key=lambda e: (e.debut, e.fin, e.niveau))


# La priorité **par niveau** de la fusion : le neuronal tient POS/syntagmes/tête,
# l'heuristique tient phrase/pragmatique/discours/document. C'est la réparation de la
# fusion : les deux sources ne concourent plus par confiance sur les mêmes niveaux.
def priorite_par_defaut() -> dict | None:
    """La fusion par niveau si un neuronal réel est joignable (clé DeepSeek), sinon la confiance.

    Le mock a montré que le niveau perd (0,3432) ; le réel (deux passes) a montré qu'il gagne
    (0,9389). Le défaut suit donc la **présence d'un réel**, pas une doctrine.
    """
    return PRIORITE_NIVEAU if os.environ.get("DEEPSEEK_KEY_FILE") else None


PRIORITE_NIVEAU = {
    "graphème": "heuristique", "morphème": "heuristique", "mot": "heuristique",
    "pos": "neuronal", "syntagme": "neuronal", "phrase": "heuristique",
    "pragmatique": "heuristique", "discours": "heuristique", "document": "heuristique",
}

# La finesse **par sous-type** : le neuronal gagne l'acte et le double sens, l'heuristique
# garde la négation et la modalité (mesuré : 0,9954 au neuronal contre 0,9676 à l'heuristique
# pour la négation). Un niveau entier ne peut pas exprimer ce partage.
PRIORITE_TYPE = {
    ("pragmatique", "acte"): "neuronal",
    ("pragmatique", "double_sens"): "neuronal",
    ("phrase", "négation"): "heuristique",
    ("phrase", "modalité"): "heuristique",
}


def _fusion(a: Annotation, b: Annotation, source: str,
            priorite_syntagme: str = "heuristique",
            priorite_par_niveau: dict | None = None,
            priorite_par_type: dict | None = None) -> Annotation:
    """Fusion déterministe : la meilleure confiance par (niveau, span, type) ; les candidats
    sont réunis ; la langue/le script vont à la meilleure confiance.

    Si `priorite_par_niveau` est donné, la fusion choisit **la source par niveau** (le
    neuronal pour POS/syntagmes, l'heuristique pour la pragmatique) au lieu de faire
    concourir les deux par confiance — c'est la réparation mesurée par la porte des quatre
    modes : l'ancienne fusion rendait 0,928/0,802/0,857, sous le neuronal seul.
    """
    meilleures: dict[tuple, Etiquette] = {}
    for e in a.etiquettes + b.etiquettes:
        cle = (e.niveau, e.debut, e.fin, e.type, e.source)
        if cle not in meilleures or e.confiance > meilleures[cle].confiance:
            meilleures[cle] = e
        else:
            meilleures[cle].candidats = sorted(set(meilleures[cle].candidats) | set(e.candidats))
    if priorite_par_niveau:
        # Choix **strict** par niveau : la source désignée, sans repli. Le repli (prendre
        # l'autre source quand la première n'a rien) ajoutait 46 phrases de syntagmes
        # heuristiques faux — 0,8069 au lieu de 0,8226 : il est retiré. Les niveaux absents
        # du dict gardent toutes les sources.
        choisis = dict(priorite_par_niveau)
        types = dict(priorite_par_type or {})
        etiquettes = []
        for e in meilleures.values():
            src = types.get((e.niveau, e.type), choisis.get(e.niveau))
            if src is None or e.source == src:
                etiquettes.append(e)
        # La source est choisie par niveau : plus d'arbitrage de chevauchement à faire.
    else:
        etiquettes = _supprimer_chevauchements(list(meilleures.values()), priorite_syntagme)
    if a.langue != "und" and (b.langue == "und" or a.langue == b.langue):
        lg, script = a.langue, a.script
    else:
        lg, script = b.langue, b.script
    unites = _fusionner(a.unites_semantiques + b.unites_semantiques)
    fraction = sum(u.fin - u.debut for u in unites) / max(1, len(a.texte))
    return Annotation(texte=a.texte, langue=lg, script=script, etiquettes=etiquettes,
                      source=source, unites_semantiques=unites,
                      fraction_semantique=round(fraction, 4),
                      trace=a.trace + b.trace + [{"etape": "fusion", "source": source,
                              "a": a.source, "b": b.source}],
                      cout={"octets": len(a.texte.encode()),
                            "etiquettes": len(etiquettes),
                            "duree_s": round(a.cout.get("duree_s", 0) + b.cout.get("duree_s", 0), 6)})


class Parallele:
    """Les deux implémentations en parallèle : le contrat est le même, la fusion est explicite."""

    nom = "parallele"

    def __init__(self, blocs: Sequence[BlocLinguistique],
                 priorite_syntagme: str = "heuristique",
                 priorite_par_niveau: dict | None = None,
                 priorite_par_type: dict | None = None):
        if len(blocs) != 2:
            raise ValueError("le parallèle attend exactement deux blocs")
        self.blocs = list(blocs)
        self.priorite_syntagme = priorite_syntagme
        self.priorite_par_niveau = (priorite_par_niveau if priorite_par_niveau is not None
                                     else priorite_par_defaut())
        self.priorite_par_type = dict(priorite_par_type or {})

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        a = self.blocs[0].analyser(texte, langue, contexte)
        b = self.blocs[1].analyser(texte, langue, contexte)
        return _fusion(a, b, self.nom, self.priorite_syntagme, self.priorite_par_niveau,
                       self.priorite_par_type)


class Cascade:
    """L'heuristique d'abord ; le neuronal seulement si un niveau reste sous le seuil."""

    nom = "cascade"

    def __init__(self, heuristique: BlocLinguistique, neuronal: BlocLinguistique,
                 seuil: float = 0.6, niveaux=("morphème", "pos", "syntagme", "discours", "pragmatique"),
                 priorite_syntagme: str = "heuristique",
                 priorite_par_niveau: dict | None = None,
                 priorite_par_type: dict | None = None):
        self.h = heuristique
        self.n = neuronal
        self.seuil = seuil
        self.niveaux = niveaux
        self.priorite_syntagme = priorite_syntagme
        self.priorite_par_niveau = (priorite_par_niveau if priorite_par_niveau is not None
                                     else priorite_par_defaut())
        self.priorite_par_type = dict(priorite_par_type or {})
        self.appels_neuronal = 0

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        a = self.h.analyser(texte, langue, contexte)
        couv = a.couverture()
        residuel = [n for n in self.niveaux if couv.get(n, 0.0) < self.seuil]
        if not residuel:
            a.source = self.nom
            a.trace.append({"etape": "cascade", "residuel": [], "appel_neuronal": False})
            return a
        self.appels_neuronal += 1
        b = self.n.analyser(texte, langue, contexte)
        fusion = _fusion(a, b, self.nom, self.priorite_syntagme, self.priorite_par_niveau,
                         self.priorite_par_type)
        fusion.trace.append({"etape": "cascade", "residuel": residuel, "appel_neuronal": True,
                             "seuil": self.seuil})
        return fusion


class CoucheSemantique:
    """Le consommateur : il ne reçoit que les unités, pas le texte entier.

    C'est le point du contrat : l'heuristique peut activer cette couche **avant** le neuronal,
    sur une fraction des unités ; le neuronal affine ensuite le résidu.
    """

    def __init__(self, cout_par_octet: float = 1.0):
        self.cout_par_octet = cout_par_octet
        self.appels = 0

    def activer(self, annotation: Annotation) -> dict:
        self.appels += 1
        octets = sum(u.fin - u.debut for u in annotation.unites_semantiques)
        return {"unites": len(annotation.unites_semantiques),
                "octets": octets,
                "fraction": round(annotation.fraction_semantique, 4),
                "cout": round(octets * self.cout_par_octet, 4),
                "source": annotation.source,
                "langue": annotation.langue}


# --------------------------------------------------------------------------- autotest


ECHANTILLONS = {
    "fr": "Le chat de la voisine qui dort sur le toit se réveille. Va voir le chat ! "
          "Il ne dort pas, mais il a peut-être faim.",
    "en": "The cat of the neighbor who sleeps on the roof wakes up. Do you see the cat? "
          "It is not sleeping, but it may be hungry.",
    "de": "Die Katze der Nachbarin, die auf dem Dach schläft, wacht auf. Siehst du die Katze?",
    "es": "El gato de la vecina que duerme en el tejado se despierta. ¿Ves el gato?",
    "it": "Il gatto della vicina che dorme sul tetto si sveglia. Vedi il gatto?",
}


def _resume_annotation(a: Annotation) -> dict:
    par = a.par_niveau()
    return {"langue": a.langue, "script": a.script, "source": a.source, "refus": a.refus,
            "niveaux": {n: len(es) for n, es in sorted(par.items())},
            "couverture": a.couverture(),
            "fraction_semantique": round(a.fraction_semantique, 4),
            "etiquettes": len(a.etiquettes)}


def autotest(udhr: pathlib.Path, sortie: pathlib.Path | None = None) -> dict:
    """Mesure la langue, le script, la substitution, le parallèle, la cascade et l'activation."""
    rapport: dict = {"date": time.strftime("%Y-%m-%dT%H:%M:%S"), "niveaux": list(NIVEAUX)}
    profils, tests = charger_profils_udhr(udhr, test=(15, 15), min_test=1)
    t0 = time.perf_counter()
    justes = 0
    scripts_justes = 0
    par_langue: dict[str, list[int]] = collections.defaultdict(lambda: [0, 0])
    for langue, texte, script in tests:
        detectee, conf, _ = detecter_langue(texte, profils)
        par_langue[langue][0] += 1
        if detectee == langue:
            justes += 1
            par_langue[langue][1] += 1
        if detecter_script(texte) == script or (detecter_script(texte) == "Hani" and script in {"Hans", "Hant"}):
            scripts_justes += 1
    duree = time.perf_counter() - t0
    rapport["langue"] = {
        "langues_profil": len(profils), "articles_test": len(tests),
        "accuracy": round(justes / max(1, len(tests)), 4),
        "accuracy_script": round(scripts_justes / max(1, len(tests)), 4),
        "duree_s": round(duree, 3),
        "langues": {k: v for k, v in sorted(par_langue.items()) if v[0] >= 3},
    }
    # contrôle négatif : labels de profils permutés
    noms = sorted(profils)
    permutes = {noms[i]: profils[noms[(i + 1) % len(noms)]].copy() for i in range(len(noms))}
    justes_permutes = 0
    for langue, texte, _ in tests:
        detectee, _, _ = detecter_langue(texte, permutes)
        justes_permutes += int(detectee == langue)
    rapport["controle_permute"] = {"accuracy": round(justes_permutes / max(1, len(tests)), 4),
                                   "attendu": "proche du hasard"}

    # niveaux, substitution, parallèle, cascade, activation sur les échantillons
    h = Heuristique(profils=profils)
    n = MockNeuronal(profils)
    p = Parallele([h, n])
    c = Cascade(h, n)
    sem = CoucheSemantique()
    niveaux_vus: set[str] = set()
    substitutions = []
    for langue, texte in ECHANTILLONS.items():
        ah = h.analyser(texte, langue)
        an = n.analyser(texte, langue)
        ap = p.analyser(texte, langue)
        ac = c.analyser(texte, langue)
        sa = sem.activer(ah)
        sn = sem.activer(an)
        niveaux_vus |= {e.niveau for e in ah.etiquettes} | {e.niveau for e in an.etiquettes}
        substitutions.append({
            "langue": langue,
            "heuristique": _resume_annotation(ah),
            "neuronal_mock": _resume_annotation(an),
            "parallele": _resume_annotation(ap),
            "cascade": _resume_annotation(ac),
            "activation_heuristique": sa,
            "activation_neuronal": sn,
            "schema_identique": set(ah.json()) == set(an.json()),
            "sources_parallele": sorted({e.source for e in ap.etiquettes}),
        })
    rapport["echantillons"] = substitutions
    rapport["niveaux_vus"] = sorted(niveaux_vus)
    rapport["niveaux_manquants"] = sorted(set(NIVEAUX) - niveaux_vus)
    rapport["controles"] = {
        "vide_refus": h.analyser("").refus,
        "ponctuation_refus": h.analyser("... !!! ???").refus,
        "langue_inconnue": h.analyser("qqqqq zzzzz wwwww").langue,
        "indice_faux": h.analyser(ECHANTILLONS["en"], "fr").langue,
        "rejeu_identique": h.analyser(ECHANTILLONS["fr"], "fr").json() == h.analyser(ECHANTILLONS["fr"], "fr").json(),
    }
    rapport["verdicts"] = {
        "langue": rapport["langue"]["accuracy"] >= 0.85,
        "script": rapport["langue"]["accuracy_script"] >= 0.85,
        "permute_faible": rapport["controle_permute"]["accuracy"] <= 0.10,
        "niveaux": len(niveaux_vus) >= 7,
        "substitution": all(s["schema_identique"] for s in substitutions),
        "parallele": all("heuristique" in s["sources_parallele"] and "neuronal" in s["sources_parallele"]
                         for s in substitutions),
        "activation": all(s["activation_heuristique"]["fraction"] < 1.0 for s in substitutions),
        "vide": h.analyser("").refus == "vide",
        "inconnue": rapport["controles"]["langue_inconnue"] == "und",
        "rejeu": rapport["controles"]["rejeu_identique"],
    }
    rapport["ok"] = all(rapport["verdicts"].values())
    if sortie:
        sortie.parent.mkdir(parents=True, exist_ok=True)
        sortie.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return rapport


# --------------------------------------------------------------------------- CLI


def _annotation_depuis_args(args) -> Annotation:
    if args.texte:
        texte = args.texte
    elif args.fichier:
        texte = pathlib.Path(args.fichier).read_text(encoding="utf-8")
    else:
        texte = sys.stdin.read()
    profils = None
    if args.profils:
        profils, _ = charger_profils_udhr(pathlib.Path(args.profils))
    h = Heuristique(profils=profils)
    n = MockNeuronal(profils)
    if args.mode == "heuristique":
        return h.analyser(texte, args.langue, args.contexte)
    if args.mode == "neuronal":
        if args.neuronal_reel:
            return NeuronalLLM(args.modele).analyser(texte, args.langue, args.contexte)
        return n.analyser(texte, args.langue, args.contexte)
    if args.mode == "parallele":
        return Parallele([h, n]).analyser(texte, args.langue, args.contexte)
    if args.mode == "cascade":
        return Cascade(h, n, seuil=args.seuil).analyser(texte, args.langue, args.contexte)
    raise SystemExit(f"mode inconnu : {args.mode}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--texte", default="")
    ap.add_argument("--fichier", default="")
    ap.add_argument("--langue", default=None)
    ap.add_argument("--contexte", default=None)
    ap.add_argument("--mode", default="heuristique",
                    choices=["heuristique", "neuronal", "parallele", "cascade"])
    ap.add_argument("--seuil", type=float, default=0.6)
    ap.add_argument("--neuronal-reel", action="store_true",
                    help="utilise NeuronalLLM (llama-cli) au lieu du mock")
    ap.add_argument("--modele", default=str(RACINE / "models/Qwen2.5-0.5B-Q4_0.gguf"))
    ap.add_argument("--profils", default="", help="articles.jsonl UDHR pour les profils de langue")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--duree", action="store_true")
    ap.add_argument("--autotest", action="store_true")
    ap.add_argument("--udhr", default=str(RACINE / "data/udhr/articles.jsonl"))
    ap.add_argument("--sortie", default="")
    args = ap.parse_args()
    if args.autotest:
        rapport = autotest(pathlib.Path(args.udhr), pathlib.Path(args.sortie) if args.sortie else None)
        print(json.dumps({k: rapport[k] for k in ("langue", "controle_permute", "niveaux_vus",
                                                  "niveaux_manquants", "controles", "verdicts", "ok")},
                         ensure_ascii=False, indent=1))
        return 0 if rapport["ok"] else 1
    a = _annotation_depuis_args(args)
    if args.json:
        print(json.dumps(a.json(avec_duree=args.duree), ensure_ascii=False, indent=1))
    else:
        print(f"langue={a.langue} script={a.script} source={a.source} refus={a.refus or '-'}")
        for n, es in sorted(a.par_niveau().items()):
            for e in es[:4]:
                print(f"  {n:12s} {e.type:14s} {e.valeur[:40]!r} [{e.debut}:{e.fin}] "
                      f"conf={e.confiance:.2f} src={e.source}")
        print(f"unités sémantiques : {len(a.unites_semantiques)} "
              f"({a.fraction_semantique:.1%} du texte)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
