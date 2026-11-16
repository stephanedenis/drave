#!/usr/bin/env python3
"""generateur.py — une phrase brute → des structures candidates (v0 heuristique).

Ce n'est pas un analyseur syntaxique : c'est un **générateur de candidats** à faire valider par
un humain. Il segmente (GN, GV, GP, REL, SUB), devine des rôles par la préposition, puis produit
plusieurs candidats en variant l'**attachement** de chaque segment ambigu (GN le plus proche ou
GV le plus proche).

    python3 generateur.py "Le chat de la voisine qui dort sur le toit se réveille."
    python3 generateur.py --json "..."     # la structure complète
"""
from __future__ import annotations

import json
import re
import unicodedata

DET = set("le la les l un une ce cet cette ces mon ma mes ton ta tes son sa ses "
          "notre nos votre vos leur leurs quel quelle quels quelles".split())
PREP = set("a au aux de du des d en dans par pour sur sous avec sans chez vers entre depuis "
           "pendant durant contre malgre selon pres loin devant derriere apres avant".split())
RELATIFS = set("qui que qu dont ou quoi".split())
CONJ = set("et ou mais donc or ni car quand comme si parce puisque lorsque pendant quoique".split())
COORD = set("et ou mais donc or ni car".split())
SUBORD = set("quand comme si parce puisque lorsque pendant quoique".split())
PRON = set("je j tu il elle on nous vous ils elles me te se lui leur moi toi soi y en ce cela ca".split())
AUX = set("est sont etait etaient ete etre ai as a avons avez ont avait avaient eu".split())
ADVERBES_TEMPS = set("hier aujourd'hui demain maintenant ici la toujours jamais souvent deja encore tard tot".split())
# Les adjectifs courants : ils aident à trancher un homographe en fin de GN
# (« le grand lit », « la vieille porte ») et l'intensif « si fort que ».
ADJECTIFS = set("""
grand grande grands grandes petit petite petits petites vieux vieille vieilles vieil
beau belle beaux belles joli jolie jolis jolies nouveau nouvelle nouveaux nouvelles
jeune jeunes bon bonne bons bonnes mauvais mauvaise mauvaises
long longue longs longues court courte courts courtes haut haute hauts hautes
bas basse basses gros grosse grosses mince minces propre propres sale sales
triste tristes simple simples faux fausse vrai vraie vrais dernier derniere
premier premiere autre autres meme memes seul seule seuls seules doux douce
dur dure durs dures chaud chaude froid froide noirs noir noire noires
blanc blanche blancs blanches rouge rouges vert verte verts vertes bleu bleue bleus bleues
gris grise jaune jaunes plein pleine vide vides lourd lourde leger legere
heureux heureuse malheureux malheureuse content contente fache fachee
calme calmes fort forte forts fortes divers diverse faible faibles rapide rapides lent lente
facile faciles difficile difficiles important importante importants importantes
riche riches pauvre pauvres vilain vilaine
""".split())
ADVERBES_SI = set("fort vite bien mal peu trop tant tellement souvent longtemps rarement tot tard".split())
PONCT = set(".,;:!?…()«»")

# Les subordonnants : un mot simple, ou un mot qui ne l'est que devant « que / qu'il ».
# Le rôle est celui de la **subordonnée**, pas du mot : « quand » = temps, « parce que » = cause.
SUBORD_SIMPLE = {"quand": "temps", "lorsque": "temps", "comme": "cause", "si": "hypothese",
                 "puisque": "cause", "quoique": "concession"}
SUBORD_QUE = {"parce": "cause", "bien": "concession", "pendant": "temps", "tandis": "temps",
              "afin": "but", "apres": "temps", "avant": "temps", "des": "temps",
              "alors": "temps", "pour": "but", "sans": "maniere", "encore": "concession"}
# Les élisions qui portent le subordonnant dans le même jeton (« lorsqu'il », « puisqu'elle »).
SUBORD_ELIDE = {"lorsqu": "temps", "puisqu": "cause", "quoiqu": "concession"}
# Verbes de lieu/état : « à la maison » après « rester » est un lieu, pas un destinataire.
# Copules : « est mon voisin » est un GV attributif, pas un GV « est » + un GN.
COPULES = set("""
est sont etait etaient sera seront serait seraient semble semblent parait paraissent
reste restent devient deviennent
""".split())
VERBES_LIEU = set("""
reste restes restons restez restent suis es est sommes etes sont etais etait etions etiez etaient
vais vas va allons allez vont allais allait allions alliez allaient
habite habites habitons habitez habitent vivais vivait vivions viviez vivaient vis vit vivons vivez vivent
viens vient venons venez viennent venais venait venions veniez venaient
pars part partons partez partent partais partait partions partiez partaient
arrive arrives arrivons arrivez arrivent arrivais arrivait arrivions arriviez arrivaient
entre entres entrons entrez entrent entrais entrait entrions entriez entraient
sors sort sortons sortez sortent sortais sortait sortions sortiez sortaient
monte montes montons montez montent descend descends descendons descendez descendent
retourne retournes retournons retournez retournent tombe tombes tombons tombez tombent
""".split())

# Verbes conjugués fréquents : un GN ne les avale pas (« La femme parle »).
# Lexique assumé, pas un étiqueteur : les homographes nominaux (« la ferme », « le fait »,
# « le lit ») restent une limite nommée — le GN s'arrête avant eux.
VERBES_FINIS = set("""
parle parles parlent parlons parlez parlais parlait parlaient
mange manges mangent mangeons mangez mangeais mangeait mangeaient
dort dors dorment dormons dormez dormais dormait dormaient
court cours courent courons courez courais courait couraient
rit ris rient rions riez riais riait riaient
chante chantes chantent chantons chantez chantais chantait chantaient
crie cries crient crions criez criais criait criaient
danse danses dansent dansons dansez dansais dansait dansaient
travaille travailles travaillent travaillons travaillez travaillais travaillait travaillaient
regarde regardes regardent regardons regardez regardais regardait regardaient
ecoute ecoutes ecoutent ecoutons ecoutez ecoutais ecoutait ecoutaient
pense penses pensent pensons pensez pensais pensait pensaient
croit crois croient croyons croyez croyais croyait croyaient
dit dis disent disons dites disais disait disaient
voit vois voient voyons voyez voyais voyait voyaient
prend prends prennent prenons prenez prenais prenait prenaient
surprend surprennent surprenons surprenez surprenais surprenait surprenaient
donne donnes donnent donnons donnez donnais donnait donnaient
aime aimes aiment aimons aimez aimais aimait aimaient
veut veux veulent voulons voulez voulais voulait voulaient
peut peux peuvent pouvons pouvez pouvais pouvait pouvaient
doit dois doivent devons devez devais devait devaient
fait fais font faisons faites faisais faisait faisaient
lit lis lisent lisons lisez lisais lisait lisaient
ecrit ecris ecrivent ecrivons ecrivez ecrivais ecrivait ecrivaient
achete achetes achetent achetons achetez achetais achetait achetaient
vend vends vendent vendons vendez vendais vendait vendaient
cherche cherches cherchent cherchons cherchez cherchais cherchait cherchaient
trouve trouves trouvent trouvons trouvez trouvais trouvait trouvaient
porte portes portent portons portez portais portait portaient
demeure demeures demeurent demeurons demeurez demeurais demeurait demeuraient demeurera
ouvre ouvres ouvrent ouvrons ouvrez ouvrais ouvrait ouvraient
ferme fermes ferment fermons fermez fermais fermait fermaient
commence commences commencent commencons commencez commencais commencait commencaient
finit finis finissent finissons finissez finissais finissait finissaient
joue joues jouent jouons jouez jouais jouait jouaient
apprend apprends apprennent apprenons apprenez apprenais apprenait apprenaient
comprend comprends comprennent comprenons comprenez comprenais comprenait comprenaient
connait connais connaissent connaissons connaissez connaissais connaissait connaissaient
attend attends attendent attendons attendez attendais attendait attendaient
repond reponds repondent repondons repondez repondais repondait repondaient
demande demandes demandent demandons demandez demandais demandait demandaient
montre montres montrent montrons montrez montrais montrait montraient
garde gardes gardent gardons gardez gardais gardait gardaient
laisse laisses laissent laissons laissez laissais laissait laissaient
passe passes passent passons passez passais passait passaient
sort sors sortent sortons sortez sortais sortait sortaient
""".split())

MOTIF = re.compile(r"[A-Za-zÀ-ÿ'’-]+|[.,;:!?…()«»]|\s+")


def _norm(mot: str) -> str:
    sans = unicodedata.normalize("NFD", mot.lower())
    return "".join(c for c in sans if unicodedata.category(c) != "Mn")


class Token:
    __slots__ = ("texte", "debut", "fin", "espace", "cls")

    def __init__(self, texte, debut, fin, espace):
        self.texte, self.debut, self.fin, self.espace = texte, debut, fin, espace
        brut = texte.lower()
        n = _norm(texte)
        prefixe = n.split("'")[0].split("’")[0]
        if texte.isspace():
            self.cls = "ESPACE"
        elif texte in PONCT:
            self.cls = "PONCT"
        elif brut == "à":
            self.cls = "PREP"
        elif brut == "a":
            self.cls = "AUX"
        elif brut == "où":
            self.cls = "RELATIF"
        elif brut == "ou":
            self.cls = "CONJ"
        elif n in DET or prefixe in DET:
            self.cls = "DET"
        elif n in PRON or prefixe in PRON:
            self.cls = "PRON"
        elif n in PREP or prefixe in PREP:
            self.cls = "PREP"
        elif n in RELATIFS or prefixe in RELATIFS:
            self.cls = "RELATIF"
        elif n in CONJ or prefixe in CONJ:
            self.cls = "CONJ"
        elif n in AUX or prefixe in AUX:
            self.cls = "AUX"
        else:
            self.cls = "MOT"


def _tokens(texte: str) -> list[Token]:
    return [Token(m.group(), m.start(), m.end(), m.group().isspace()) for m in MOTIF.finditer(texte)]


def _est_que(tok: Token) -> bool:
    n = _norm(tok.texte)
    return n.split("'")[0].split("’")[0] in ("que", "qu")


def _si_intensif(utiles: list[Token], i: int) -> bool:
    """Vrai si le « si » de `i` est l'intensif (« crie si fort »), pas le conditionnel."""
    if _norm(utiles[i].texte) != "si" or i + 1 >= len(utiles):
        return False
    suivant = _norm(utiles[i + 1].texte)
    return suivant in ADJECTIFS or suivant in ADVERBES_SI


def _marqueur(utiles: list[Token], i: int) -> str | None:
    """Le rôle de la subordonnée ouverte au jeton `i`, ou None.

    Deux familles : le mot simple (« quand », « comme ») et le mot qui ne subordonne que
    devant « que / qu'il » (« parce que », « bien qu'il »). Les élisions portent le
    subordonnant dans le même jeton (« lorsqu'il », « puisqu'elle »).
    """
    n = _norm(utiles[i].texte)
    brut = utiles[i].texte.lower()
    prefixe = n.split("'")[0].split("’")[0]
    # « si fort que », « si vite qu'il » : le si est un intensif, et le que ouvre la
    # **conséquence** — ce n'est ni une hypothèse ni un contenu.
    if n == "que" and i >= 2:
        avant, avant2 = _norm(utiles[i - 1].texte), _norm(utiles[i - 2].texte)
        if avant2 == "si" and (avant in ADJECTIFS or avant in ADVERBES_SI):
            return "consequence"
    if brut.startswith(("s'", "s’")) and n[2:].startswith(("il", "elle", "on", "ils", "elles", "y")):
        return "hypothese"
    if prefixe == "si" and i + 1 < len(utiles):
        suivant = _norm(utiles[i + 1].texte)
        if suivant in ADJECTIFS or suivant in ADVERBES_SI:
            return None
    if prefixe in SUBORD_ELIDE:
        return SUBORD_ELIDE[prefixe]
    if prefixe in SUBORD_SIMPLE:
        return SUBORD_SIMPLE[prefixe]
    if prefixe in SUBORD_QUE and i + 1 < len(utiles) and _est_que(utiles[i + 1]):
        return SUBORD_QUE[prefixe]
    return None


def _fin_clause(utiles: list[Token], j: int) -> int:
    """Fin d'une subordonnée : ponctuation ou coordination, sans avaler la principale."""
    while j < len(utiles):
        t = utiles[j]
        if t.cls == "PONCT":
            break
        if t.cls == "CONJ" and _norm(t.texte) in COORD:
            break
        j += 1
    return j


def _dernier_mot(texte: str) -> str:
    mots = [m.group() for m in MOTIF.finditer(texte)
            if m.group().strip() and _norm(m.group()) not in PREP | DET]
    return _norm(mots[-1]) if mots else ""


def _infinitif(tok: Token) -> bool:
    n = _norm(tok.texte)
    return tok.cls == "MOT" and len(n) > 2 and n.endswith(("er", "ir", "re"))


def _role_gp(prep: str, segs: list["Segment"], utiles: list[Token], i: int) -> str:
    """Le rôle du GP, par la préposition **et son contexte** (ce qui précède, ce qui suit).

    Le contexte est ce qui distingue « de la voisine » (possession, après un GN) de
    « de son projet » (thème, après un GV), « à manger » (but, infinitif) de « à Marie »
    (destinataire), ou « par Marie » (agent, après un passif) de « par la porte » (moyen).
    """
    def _proche(types: tuple[str, ...]) -> "Segment | None":
        for s in reversed(segs):
            if s.type in types:
                return s
        return None

    if prep in {"de", "du", "des", "d"}:
        proche = _proche(("GN", "GV"))
        return "possession" if proche is not None and proche.type == "GN" else "theme"
    if prep in {"a", "au", "aux"}:
        if i + 1 < len(utiles) and _infinitif(utiles[i + 1]):
            return "but"
        gv = _proche(("GV",))
        if gv is not None and _dernier_mot(gv.texte) in VERBES_LIEU:
            return "lieu"
        return "destinataire"
    if prep == "avec":
        return "instrument"
    if prep == "pour":
        return "but"
    if prep == "par":
        gv = _proche(("GV",))
        if gv is not None and "ete" in _norm(gv.texte).split():
            return "agent"
        return "moyen"
    if prep in {"dans", "sur", "sous", "chez", "vers", "entre", "devant", "derriere", "pres", "loin"}:
        return "lieu"
    if prep in {"pendant", "depuis", "durant", "avant", "apres"}:
        return "temps"
    if prep == "malgre":
        return "concession"
    if prep == "selon":
        return "source"
    if prep == "sans":
        return "maniere"
    if prep == "en":
        return "lieu"
    return "complement"


class Segment:
    __slots__ = ("debut", "fin", "type", "role", "niveau", "texte", "cible_nom", "cible_gp",
                 "cible_verbe", "parent", "profondeur")

    def __init__(self, debut, fin, texte, typ, role, niveau=0):
        self.debut, self.fin, self.texte = debut, fin, texte
        self.type, self.role, self.niveau = typ, role, niveau
        self.cible_nom = None   # le GN le plus proche à gauche
        self.cible_gp = None    # la tête du GP le plus proche à gauche
        self.cible_verbe = None  # le GV le plus proche à gauche
        self.parent = None      # l'index du segment père dans la liste
        self.profondeur = 0     # la profondeur dans l'arbre (le GV racine = 0)

    def dict(self):
        return {"debut": self.debut, "fin": self.fin, "texte": self.texte,
                "type": self.type, "role": self.role, "niveau": self.niveau,
                "parent": self.parent, "profondeur": self.profondeur}


def _consomme(toks, i, classes):
    j = i
    while j < len(toks) and toks[j].cls in classes:
        j += 1
    return j


def construire_arbre(segs: list["Segment"]) -> None:
    """Le père et la profondeur : le GV principal est la racine, les GN ses enfants, et les
    GP/REL/SUB s'accrochent au plus proche segment à gauche (GN, GP ou GV). L'indentation
    (`niveau`) devient la profondeur réelle, pas un niveau plat par type."""
    if not segs:
        return
    gv = [k for k, s in enumerate(segs) if s.type == "GV"]
    racine = gv[0] if gv else 0
    # le plus proche segment à gauche, entretenu au fil du balayage (O(k) au lieu de O(k²))
    dernier: int | None = None
    for k, s in enumerate(segs):
        if k == racine:
            s.parent, s.profondeur = None, 0
        elif s.type in ("GV", "GN"):
            s.parent, s.profondeur = racine, 1
        else:
            indice = dernier if dernier is not None else racine
            parent = segs[indice]
            s.parent = indice
            s.profondeur = parent.profondeur + 1
        if s.type in ("GN", "GP", "GV"):
            dernier = k
    for s in segs:
        s.niveau = s.profondeur


def _segmente(texte: str, toks: list[Token]) -> list[Segment]:
    utiles = [t for t in toks if t.cls != "ESPACE"]
    segs: list[Segment] = []
    i = 0
    while i < len(utiles):
        t = utiles[i]
        if t.cls == "PONCT":
            i += 1
            continue
        marqueur = _marqueur(utiles, i)
        if marqueur:
            # « parce qu'elle est fatiguée », « bien qu'il soit tard » : la subordonnée
            # commence au subordonnant et va jusqu'à la ponctuation ou la coordination.
            j = _fin_clause(utiles, i + 1)
            segs.append(Segment(t.debut, utiles[j - 1].fin, texte[t.debut:utiles[j - 1].fin],
                                "SUB", marqueur, 1))
            i = j
            continue
        if t.cls == "RELATIF":
            j, vu_verbe = i + 1, False
            while j < len(utiles) and utiles[j].cls not in ("PONCT", "CONJ", "RELATIF"):
                if utiles[j].cls == "PRON" and vu_verbe:
                    break
                if utiles[j].cls == "AUX" and vu_verbe:
                    break
                if (utiles[j].cls == "MOT" and vu_verbe
                        and _norm(utiles[j].texte) in ADVERBES_TEMPS):
                    break
                vu_verbe = vu_verbe or utiles[j].cls == "MOT"
                j += 1
            # « que » après un verbe est un complément, après un nom une relative.
            precedent = segs[-1].type if segs else None
            if _norm(t.texte).split("'")[0].split("’")[0] in ("que", "qu") and precedent == "GV":
                segs.append(Segment(t.debut, utiles[j - 1].fin, texte[t.debut:utiles[j - 1].fin],
                                    "SUB", "contenu", 1))
            else:
                segs.append(Segment(t.debut, utiles[j - 1].fin, texte[t.debut:utiles[j - 1].fin],
                                    "REL", "qualite", 1))
            i = j
            continue
        if t.cls in ("DET", "PRON") and not (t.cls == "PRON" and i + 1 < len(utiles)
                                             and utiles[i + 1].cls in ("AUX", "MOT")):
            j, mots, tete = i, 0, False
            while j < len(utiles) and utiles[j].cls in ("DET", "PRON", "MOT") and mots < 3:
                if (utiles[j].cls == "MOT" and mots >= 1
                        and (_norm(utiles[j].texte) in VERBES_FINIS
                             or _norm(utiles[j].texte) in VERBES_LIEU)):
                    # Homographe : le mot est un nom si le suivant est un auxiliaire/copule
                    # (« la petite ferme est ») ou un autre verbe (« le simple fait surprend »).
                    suivant = utiles[j + 1] if j + 1 < len(utiles) else None
                    apres = utiles[j + 2] if j + 2 < len(utiles) else None
                    precedent = utiles[j - 1] if j > 0 else None
                    nom = suivant is not None and (
                        suivant.cls == "AUX"
                        or (suivant.cls == "MOT"
                            and (_norm(suivant.texte) in VERBES_FINIS
                                 or _norm(suivant.texte) in VERBES_LIEU)))
                    # « le fait divers surprend » : homographe + adjectif, puis le verbe
                    if not nom and suivant is not None and _norm(suivant.texte) in ADJECTIFS:
                        if apres is None or apres.cls == "PONCT" or (
                                apres.cls == "MOT" and (_norm(apres.texte) in VERBES_FINIS
                                                        or _norm(apres.texte) in VERBES_LIEU)):
                            nom = True
                    if not nom and not tete and precedent is not None:
                        adjectif = _norm(precedent.texte) in ADJECTIFS
                        determinant = precedent.cls == "DET"
                        if (adjectif or determinant) and (suivant is None or suivant.cls == "PONCT"):
                            nom = True
                    if not nom:
                        break
                    tete = True
                elif utiles[j].cls == "MOT" and _norm(utiles[j].texte) not in ADJECTIFS:
                    tete = True
                if utiles[j].cls == "MOT":
                    mots += 1
                j += 1
            segs.append(Segment(t.debut, utiles[j - 1].fin, texte[t.debut:utiles[j - 1].fin],
                                "GN", "agent" if not any(s.type == "GV" for s in segs) else "patient"))
            i = j
            continue
        if t.cls == "PREP":
            j = _consomme(utiles, i + 1, {"DET", "MOT"})
            if j == i + 1:
                i += 1          # une préposition sans contenu n'est pas un GP
                continue
            segs.append(Segment(t.debut, utiles[j - 1].fin, texte[t.debut:utiles[j - 1].fin],
                                "GP", _role_gp(_norm(t.texte), segs, utiles, i), 1))
            i = j
            continue
        if t.cls == "CONJ":
            if _norm(t.texte) in COORD:
                i += 1          # coordination : une nouvelle proposition, pas une subordonnée
                continue
            j = i + 1
            while j < len(utiles) and utiles[j].cls not in ("PONCT", "CONJ"):
                j += 1
            segs.append(Segment(t.debut, utiles[j - 1].fin, texte[t.debut:utiles[j - 1].fin],
                                "SUB", "contenu", 1))
            i = j
            continue
        if t.cls == "MOT" and _norm(t.texte) in ADVERBES_TEMPS:
            segs.append(Segment(t.debut, t.fin, t.texte, "GP", "temps", 1))
            i += 1
            continue
        # PRON/AUX/MOT : un GV — mais il s'arrête avant un subordonnant (« il travaille afin »).
        j = i
        while j < len(utiles) and (utiles[j].cls in ("PRON", "AUX", "MOT")
                                   or (utiles[j].cls == "CONJ" and _si_intensif(utiles, j))):
            if j > i and _marqueur(utiles, j):
                break
            if (j > i and utiles[j].cls == "MOT"
                    and _norm(utiles[j].texte) in ADVERBES_TEMPS):
                break
            j += 1
        if j == i:
            j = i + 1
        # copule + groupe nominal attribut : « est mon voisin » ne se coupe pas en « est » + GN.
        if (j < len(utiles) and utiles[j].cls == "DET"
                and _norm(utiles[j - 1].texte) in COPULES):
            k, mots = j + 1, 0
            while k < len(utiles) and utiles[k].cls in ("DET", "MOT") and mots < 3:
                if utiles[k].cls == "MOT":
                    mots += 1
                k += 1
            j = k
        segs.append(Segment(t.debut, utiles[j - 1].fin, texte[t.debut:utiles[j - 1].fin],
                            "GV", "predicat", 0))
        i = j
    # Le passif : « a été écrite par Marie » — le GN sujet est patient, « par » est agent.
    for k, s in enumerate(segs):
        if s.type == "GV" and len(_norm(s.texte).split()) >= 3 and "ete" in _norm(s.texte).split():
            for g in reversed(segs[:k]):
                if g.type == "GN":
                    g.role = "patient"
                    break
            for g in segs[k + 1:]:
                if g.type == "GP" and _norm(g.texte).split()[:1] == ["par"]:
                    g.role = "agent"
                    break
    # les cibles d'attachement : GN, tête du GP et GV les plus proches à gauche
    def _tete_gp(g):
        mots = [m for m in MOTIF.finditer(texte, g.debut, g.fin) if m.group().strip()
                and _norm(m.group()) not in PREP | DET]
        return mots[-1].group() if mots else None
    # un balayage unique : la cible est le **plus proche** segment de chaque type à
    # gauche ; on l'entretient au lieu de reparcourir le préfixe pour chaque segment.
    dernier_gn = dernier_gp = dernier_gv = None
    for s in segs:
        if s.cible_nom is None and dernier_gn is not None:
            s.cible_nom = dernier_gn
        if s.cible_gp is None and dernier_gp is not None:
            s.cible_gp = dernier_gp
        if s.cible_verbe is None and dernier_gv is not None:
            s.cible_verbe = dernier_gv
        if s.type == "GN":
            dernier_gn = s.texte
        elif s.type == "GP":
            tete = _tete_gp(s)
            if tete is not None:
                dernier_gp = tete
        elif s.type == "GV":
            dernier_gv = s.texte
    construire_arbre(segs)
    return segs


ROLES_AMBIGUS = {"pour": ["cause"]}


def _role_attache(role: str, genre: str) -> str | None:
    """Le rôle change avec l'attachement : instrument/attribut, possession/thème."""
    if role == "instrument" and genre == "GN":
        return "attribut"
    if role == "possession" and genre == "GV":
        return "theme"
    if role == "theme" and genre == "GN":
        return "possession"
    return None


def analyser(texte: str, max_candidats: int = 4) -> list[dict]:
    """Rend des structures candidates : un segment ambigu varie à la fois."""
    toks = _tokens(texte)
    base = _segmente(texte, toks)
    ambigus = [s for s in base if s.type in ("GP", "REL")
               and (s.cible_nom or s.cible_gp or s.cible_verbe)]
    s = ambigus[-1] if ambigus else None
    variantes = []  # (role, cible, niveau)
    if s is not None:
        if s.cible_gp:
            variantes.append((_role_attache(s.role, "GP"), ("GP", s.cible_gp), 2))
        if s.cible_nom:
            variantes.append((_role_attache(s.role, "GN"), ("GN", s.cible_nom), 1))
        if s.cible_verbe:
            variantes.append((_role_attache(s.role, "GV"), ("GV", s.cible_verbe), 1))
        if s.type == "GP":
            prep = _norm(s.texte.split()[0].strip("«»")) if s.texte.split() else ""
            for role in ROLES_AMBIGUS.get(prep, []):
                if role != s.role:
                    variantes.append((role, None, s.niveau))
    if not variantes:
        variantes = [(None, None, 0)]
    candidats, vus = [], set()
    for role, cible, niveau in variantes:
        segs = []
        for x in base:
            copie = Segment(x.debut, x.fin, x.texte, x.type, x.role, x.niveau)
            copie.parent, copie.profondeur = x.parent, x.profondeur
            copie.cible_nom, copie.cible_gp, copie.cible_verbe = x.cible_nom, x.cible_gp, x.cible_verbe
            if s is not None and x is s:
                copie.niveau = niveau
                if role:
                    copie.role = role
            segs.append(copie)
        attachement = ({"segment": s.texte, "cible": cible[1], "genre": cible[0]}
                       if cible else None)
        nom = (f"« {s.texte.strip()} » → {cible[1]}" if cible else
               f"« {s.texte.strip()} » = {role}" if role else "structure la plus proche")
        lecture = (f"« {s.texte.strip()} » se rattache à « {cible[1].strip()} »" if cible else
                   f"« {s.texte.strip()} » est un complément de {role}." if role else
                   "chaque segment se rattache à la cible la plus proche.")
        clé = json.dumps([[(x.debut, x.fin, x.type, x.role, x.niveau) for x in segs], attachement],
                         sort_keys=True)
        if clé in vus:
            continue
        vus.add(clé)
        candidats.append({"nom": nom, "lecture": lecture, "attachement": attachement,
                          "segments": [x.dict() for x in segs]})
        if len(candidats) >= max_candidats:
            break
    return candidats




POSSESSIFS = set("mon ma mes ton ta tes son sa ses notre nos votre vos leur leurs".split())
PROPRE = re.compile(r"\b(?:[A-ZÀ-Ý][a-zà-ÿ]{2,}|[A-ZÀ-Ý]{2,})\b")


def referents(texte: str, contexte: str = "") -> list[dict]:
    """Propose des antécédents pour chaque pronom/possessif : les GN et têtes de GP à gauche,
    les noms propres de la phrase, puis ceux du contexte (les phrases précédentes). Ce n'est pas
    une résolution : c'est la liste que l'humain tranche — et que l'arbre affiche en pointillés.
    """
    toks = _tokens(texte)
    segs = _segmente(texte, _tokens(texte))
    gns = [s for s in segs if s.type == "GN"]
    gps = [s for s in segs if s.type == "GP"]

    def noms_propres(texte_partiel: str) -> list[str]:
        return [m for m in PROPRE.findall(texte_partiel)
                if _norm(m) not in PRON and _norm(m) not in DET
                and _norm(m) not in VERBES_FINIS and _norm(m) not in VERBES_LIEU]

    def avant(pos: int) -> list[str]:
        c = [g.texte.strip() for g in gns if g.fin <= pos]
        for g in gps:
            if g.fin <= pos:
                mots = [m.group() for m in MOTIF.finditer(g.texte) if m.group().strip()
                        and _norm(m.group()) not in PREP | DET]
                if mots:
                    c.append(mots[-1])
        c += noms_propres(texte[:pos])
        return c

    hors = []
    if contexte:
        cs = _segmente(contexte, _tokens(contexte))
        hors += [g.texte.strip() for g in cs if g.type == "GN"]
        hors += noms_propres(contexte)

    sortie = []
    for t in toks:
        n = _norm(t.texte)
        if not (t.cls == "PRON" or (t.cls == "DET" and n in POSSESSIFS)):
            continue
        candidats = list(dict.fromkeys(c for c in avant(t.debut) + hors if c))
        sortie.append({"forme": t.texte, "debut": t.debut, "fin": t.fin,
                       "anaphore": n, "candidats": candidats})
    return sortie


ROLES_DEFAUT = {"GP": "complement", "SUB": "contenu", "REL": "qualite"}


def structure(texte: str, roles: bool = True) -> list[dict]:
    """La structure de base, sans variantes d'attachement ; `roles=False` coupe les règles.

    C'est ce que mesure `mesure_analyseur.py` : la segmentation et les rôles, pas le choix
    d'un candidat. `roles=False` rend les rôles par défaut (le contrôle « règles coupées »).
    """
    segs = _segmente(texte, _tokens(texte))
    sortie = []
    for s in segs:
        d = s.dict()
        if not roles and s.type in ROLES_DEFAUT:
            d["role"] = ROLES_DEFAUT[s.type]
        sortie.append(d)
    return sortie


if __name__ == "__main__":
    import sys
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    texte = args[0] if args else "Le chat de la voisine qui dort sur le toit se réveille."
    cs = analyser(texte)
    if "--json" in sys.argv:
        print(json.dumps(cs, ensure_ascii=False, indent=1))
    else:
        for c in cs:
            print(f"- {c['nom']}")
            for s in c["segments"]:
                print("   " + "  " * s["niveau"] + f"{s['texte']!r} [{s['type']} · {s['role']}]")
