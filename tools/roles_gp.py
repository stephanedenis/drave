"""roles_gp.py — les rôles des groupes prépositionnels (restitution v3).

La v2 lisait la **préposition seule** : `à` était toujours un destinataire, `de` toujours
un thème, `avec` toujours un moyen. La v3 ajoute le **contexte** : ce qui suit la
préposition (un lieu, un temps, une personne, un infinitif) et ce qui la précède (un GN
ou un GV, un passif). Le rôle sort alors parmi les cinq catégories nommées par la tâche
— `lieu`, `temps`, `destinataire`, `possession`, `complement` — plus les rôles déjà
connus (`theme`, `moyen`, `but`, `agent`, `maniere`, `concession`, `source`).

Le module est **pur** (pas d'import du bloc linguistique) : il peut être testé seul, et
le bloc le réutilise. La fonction de compatibilité `_role_gp(prep)` du bloc garde son
ancien comportement quand aucun contexte n'est fourni ; c'est la v3 qui passe le
contexte.

    from tools.roles_gp import role_gp
    role_gp("à", suivant="la maison")          # lieu
    role_gp("à", suivant="14 h")               # temps
    role_gp("à", suivant="Marie")              # destinataire
    role_gp("de", suivant="la voisine", precedent="GN")   # possession
    role_gp("de", suivant="son projet", precedent="GV")   # theme
    role_gp("avec", suivant="le télescope")    # moyen
"""
from __future__ import annotations

import re

# Les cinq rôles que la v3 doit séparer (la tâche) ; `complement` est le repli.
ROLES_GP = ("lieu", "temps", "destinataire", "possession", "complement")
# Les deux orthographes du moyen : le gold S dit `instrument`, la règle dit `moyen`.
MOYEN = ("moyen", "instrument")

# --------------------------------------------------------------------------- lexiques

# Adverbes, noms et repères temporels. On garde les accents : `dès` n'est pas `des`.
TEMPS = frozenset("""
demain hier aujourd'hui aujourdhui maintenant midi minuit matin matinee matinée soir soiree
soirée nuit jour journee journée semaine semaines quinzaine mois annee année annees années
ans heure heures fois instant minute minutes seconde secondes moment periode période siecle
siècle printemps ete été automne hiver lundi mardi mercredi jeudi vendredi samedi dimanche
janvier fevrier février mars avril mai juin juillet aout août septembre octobre novembre
decembre décembre noel noël paques pâques tot tôt tard bientot bientôt ensuite puis enfin
deja déjà jamais toujours souvent parfois quelquefois recemment récemment actuellement
desormais désormais auparavant jadis apres apres-midi après après-midi avant-hier
apres-demain après-demain hier-soir ce-soir aujourdhui aujourd'hui
""".split())

# Noms de lieux communs et de grandes villes/pays : un repère géographique, pas une liste
# de noms propres. Un nom propre inconnu après `à` reste un destinataire (le défaut).
LIEUX = frozenset("""
maison parc ecole école gare salle rue ville pays bord toit jardin bureau magasin
restaurant hopital hôpital plage montagne foret forêt riviere rivière mer ciel chambre cuisine
cour grange haie fichier dossier notes table canape canapé sol route chemin pont quartier
village campagne capitale province region région continent monde endroit lieu place batiment
bâtiment immeuble appartement etage étage escalier porte fenetre fenêtre mur plafond usine
ferme marche marché cinema cinéma theatre théâtre musee musée bibliotheque bibliothèque
universite université college collège lycee lycée hotel hôtel aeroport aéroport port station
arret arrêt coin cote côté haut bas fond centre milieu rive frontiere frontière bois champ pre
pré vallon colline berge lac etang étang fleuve ocean océan terre air espace
home house school office room city town country street station airport park garden
""".split())

VILLES = frozenset("""
paris lyon marseille londres berlin rome madrid new york tokyo quebec québec montreal
montréal ottawa france canada belgique suisse espagne italie allemagne angleterre
etats-unis états-unis chine japon inde afrique europe asie amerique amérique normandie
bretagne provence alsace bordeaux toulouse nice nantes strasbourg lille rennes
""".split())

# Pronoms et noms de personne : servent au `à` + copule (possession) et au `à` + personne.
PERSONNES = frozenset("""
moi toi lui elle nous vous eux elles fils fille pere père mere mère frere frère soeur sœur
ami amie enfant homme femme mari epouse épouse voisin voisine collegue collègue patron
cliente client medecin médecin professeur etudiant étudiant eleve élève chat chien
""".split())

# Verbes de lieu/mouvement : un `à` après eux penche pour le lieu, même sans nom de lieu.
VERBES_LIEU = frozenset("""
reste restes restons restez restent suis es est sommes etes êtes sont etais étais etait était
etions étions etiez étiez etaient étaient vais vas va allons allez vont allais allait allions
alliez allaient habite habites habitons habitez habitent vivais vivait vivions viviez vivaient
vis vit vivons vivez vivent viens vient venons venez viennent venais venait venions veniez
venaient pars part partons partez partent partais partait partions partiez partaient
arrive arrives arrivons arrivez arrivent arrivais arrivait arrivions arriviez arrivaient
entre entres entrons entrez entrent entrais entrait entrions entriez entraient sors sort
sortons sortez sortent sortais sortait sortions sortiez sortaient monte montes montons montez
montent descends descend descendons descendez descendent retourne retournes retournons
retournez retournent tombe tombes tombons tombez tombent
""".split())

VEHICULES = frozenset("""
voiture train bus avion bateau velo vélo pied metro métro taxi camion moto
car plane ship boat bike
""".split())

PREP_TEMPS = frozenset("""
pendant depuis durant avant apres après dès jusqu'à jusqua during since before after
""".split())
PREP_MOYEN = frozenset("avec with".split())
PREP_BUT = frozenset("pour afin for".split())
PREP_POSSESSION = frozenset("de du des d' d of from".split())
PREP_DEST = frozenset("a à au aux to".split())
PREP_LIEU = frozenset("""
dans sur sous chez vers entre devant derriere derrière pres près loin in on at under between
over above below behind near around through across
""".split())
PREP_AUTRES = {
    "malgre": "concession", "malgré": "concession", "selon": "source",
    "sans": "maniere",
}
PREP_CONNUES = (PREP_TEMPS | PREP_MOYEN | PREP_BUT | PREP_POSSESSION | PREP_DEST
                | PREP_LIEU | frozenset(PREP_AUTRES) | frozenset({"en", "par", "by"}))

# Mots qui ressemblent à un infinitif mais n'en sont pas (noms en -er/-ir/-re).
FAUX_INFINITIFS = frozenset("""
hier hiver fer mer pere père mere mère frere frère ver cher leger léger premier dernier
papier quartier metier métier pilier soulier tablier danger etranger étranger berger plombier
cuisinier jardinier ouvrier policier pompier pommier prunier cerisier laurier cahier clavier
fichier dossier panier grenier atelier chantier escalier palier seminaire séminaire necessaire
nécessaire annuaire horaire repertoire répertoire territoire laboratoire observatoire
refractaire réfractaire miroir trottoir couloir mouchoir tiroir ardoise fraise braise chaise
""".split())

# Verbes anglais fréquents employés après `to` : `to eat` = but, `to Mary` = destinataire.
VERBES_EN = frozenset("""
eat go see be have do make take get come know think say tell give find work call try ask
need feel become leave put mean keep let begin seem help talk turn start show hear play run
move like live believe hold bring happen write provide sit stand lose pay meet include
continue set learn change lead understand watch follow stop create speak read allow add
spend grow open walk win offer remember love consider appear buy wait serve die send expect
build stay fall cut reach kill remain
""".split())

MOT = re.compile(r"[0-9A-Za-zÀ-ÖØ-öø-ÿ]+(?:['’][0-9A-Za-zÀ-ÖØ-öø-ÿ]+)?")
DET = frozenset("""
le la les l' un une des du de d' the a an mon ma mes ton ta tes son sa ses notre nos votre vos
leur leurs ce cette ces cet
""".split())


# --------------------------------------------------------------------------- outils


def normaliser(texte: str) -> str:
    """Minuscules, apostrophe droite ; les accents sont **gardés** (`dès` ≠ `des`)."""
    return (texte or "").strip().casefold().replace("’", "'")


def mots(texte: str) -> list[str]:
    return MOT.findall(texte or "")


def tete(texte: str) -> str:
    """La tête du GN : le premier mot qui n'est pas un déterminant, casse d'origine."""
    for m in MOT.finditer(texte or ""):
        if normaliser(m.group()) not in DET:
            return m.group()
    return ""


def normaliser_role(role: str) -> str:
    """Un rôle canonique : `prédicat`→`predicat`, `instrument`→`moyen`, accents retirés."""
    r = normaliser(role)
    if not r:
        return ""
    return {"predicat": "predicat", "prédicat": "predicat", "qualite": "qualite",
            "qualité": "qualite", "complement": "complement", "complément": "complement",
            "instrument": "moyen", "moyen": "moyen"}.get(r, r)


def est_temps(texte: str) -> bool:
    """Le texte qui suit la préposition est-il un repère temporel ?"""
    n = normaliser(texte)
    if not n:
        return False
    for m in mots(n)[:2]:
        if m in TEMPS:
            return True
    if re.fullmatch(r"\d{1,4}", n):                       # 9, 14, 2020
        return True
    if re.search(r"\d{1,2}\s*h(?:\s*\d{2})?", n):        # 14 h, 14h30, 9 h 05
        return True
    if re.search(r"\d{1,2}\s*:\s*\d{2}", n):             # 14:30
        return True
    if re.search(r"\d{1,2}\s*/\s*\d{1,2}(?:\s*/\s*\d{2,4})?", n):  # 12/03/2026
        return True
    if re.search(r"\d{1,4}\s*(ans?|annees?|années?|jours?|mois|semaines?|heures?|minutes?|"
                 r"secondes?|siecles?|siècles?)\b", n):
        return True
    if re.fullmatch(r"\d{4}", mots(n)[0] if mots(n) else ""):      # 2020
        return True
    return False


def est_lieu(texte: str) -> bool:
    """Le texte qui suit la préposition est-il un lieu (nom commun ou ville/pays) ?"""
    t = tete(texte)
    if not t:
        return False
    n = normaliser(t)
    return n in LIEUX or n in VILLES


def est_personne(texte: str) -> bool:
    t = tete(texte)
    return bool(t) and normaliser(t) in PERSONNES


def est_infinitif(texte: str, langue: str = "fr") -> bool:
    """`à manger` (but) vs `à Marie` (destinataire)."""
    t = tete(texte)
    if not t:
        return False
    n = normaliser(t)
    if n in FAUX_INFINITIFS:
        return False
    if langue == "en":
        return n in VERBES_EN
    return len(n) > 2 and n.endswith(("er", "ir", "re"))


def est_passif(precedent_texte: str) -> bool:
    """Un `par` après un auxiliaire + participe est un agent, pas un moyen."""
    n = normaliser(precedent_texte)
    return bool(re.search(r"\b(est|sont|etais|était|etaient|étaient|ete|été|sera|seront|suis|"
                          r"es|sommes|etes|êtes|was|were|is|are|been|be)\b", n))


def est_preposition(prep: str) -> bool:
    """La chaîne est-elle une préposition connue ? (`hier` et `demain` ne le sont pas.)"""
    return normaliser(prep).rstrip("'") in PREP_CONNUES


# --------------------------------------------------------------------------- la règle


def role_gp(prep: str, suivant: str = "", precedent: str = "",
            precedent_texte: str = "", langue: str = "fr") -> str:
    """Le rôle d'un GP, par la préposition **et son contexte**.

    `precedent` est le type du syntagme qui précède (`GN`, `GV`, …), `precedent_texte`
    son texte. `suivant` est ce qui suit la préposition dans le GP. Le défaut est
    `complement` : un rôle n'est jamais inventé par élimination.
    """
    p = normaliser(prep)
    base = p.rstrip("'")

    if base in PREP_TEMPS:
        return "temps"
    if base in PREP_MOYEN:
        return "moyen"
    if base in PREP_BUT:
        return "but"
    if base in {"par", "by"}:
        return "agent" if est_passif(precedent_texte) else "moyen"
    if base in PREP_LIEU:
        # `vers 9 h`, `dans trois jours`, `sur deux ans` : le temps prime sur le lieu.
        return "temps" if est_temps(suivant) else "lieu"
    if base in PREP_POSSESSION:
        # `de la voisine` après un GN = possession ; `de son projet` après un GV = thème.
        return "possession" if precedent == "GN" else "theme"
    if base in PREP_DEST:
        if est_infinitif(suivant, langue):
            return "but"
        if est_temps(suivant):
            return "temps"
        if est_lieu(suivant):
            return "lieu"
        # `Le livre est à moi` : copule + pronom/personne = possession, pas destinataire.
        if est_passif(precedent_texte) and (est_personne(suivant) or "moi" in normaliser(suivant)):
            return "possession"
        if (normaliser(precedent_texte).split()[:1] and
                normaliser(precedent_texte).split()[0] in {"est", "sont", "etait", "était",
                                                          "sera", "seront", "suis", "es"}
                and (est_personne(suivant) or "moi" in normaliser(suivant))):
            return "possession"
        return "destinataire"
    if base == "en":
        if est_temps(suivant):
            return "temps"
        if est_lieu(suivant):
            return "lieu"
        if re.match(r"^[a-zà-ÿ']+ant\b", normaliser(suivant)):
            return "maniere"       # `en haussant les épaules`
        if normaliser(suivant).split()[:1] and normaliser(suivant).split()[0] in VEHICULES:
            return "moyen"         # `en voiture`
        return "lieu"
    if base in PREP_AUTRES:
        return PREP_AUTRES[base]
    return "complement"


# --------------------------------------------------------------------------- cas de séparation

# Les cas qui doivent se séparer : c'est le test le plus direct de la règle. Ils ne
# remplacent pas l'or (le gold S n'a que 18 occurrences des cinq rôles) ; ils montrent
# que la fonction ne renvoie pas un rôle constant.
CAS_SEPARATION = [
    # à + lieu / temps / destinataire
    {"prep": "à", "suivant": "la maison", "attendu": "lieu", "cas": "à + lieu"},
    {"prep": "à", "suivant": "Paris", "attendu": "lieu", "cas": "à + ville"},
    {"prep": "à", "suivant": "14 h", "attendu": "temps", "cas": "à + heure"},
    {"prep": "à", "suivant": "demain", "attendu": "temps", "cas": "à + jour"},
    {"prep": "à", "suivant": "Marie", "attendu": "destinataire", "cas": "à + personne"},
    {"prep": "à", "suivant": "manger", "attendu": "but", "cas": "à + infinitif"},
    # de + possession / thème
    {"prep": "de", "suivant": "la voisine", "precedent": "GN", "attendu": "possession",
     "cas": "de + GN"},
    {"prep": "de", "suivant": "son projet", "precedent": "GV", "attendu": "theme",
     "cas": "de + GV"},
    # avec + moyen
    {"prep": "avec", "suivant": "le télescope", "attendu": "moyen", "cas": "avec + moyen"},
    # lieu / temps par la préposition
    {"prep": "dans", "suivant": "le parc", "attendu": "lieu", "cas": "dans + lieu"},
    {"prep": "sur", "suivant": "le canapé", "attendu": "lieu", "cas": "sur + lieu"},
    {"prep": "pendant", "suivant": "deux heures", "attendu": "temps", "cas": "pendant + temps"},
    {"prep": "vers", "suivant": "9 h", "attendu": "temps", "cas": "vers + temps"},
    {"prep": "vers", "suivant": "la gare", "attendu": "lieu", "cas": "vers + lieu"},
    {"prep": "sur", "suivant": "deux ans", "attendu": "temps", "cas": "sur + durée"},
    {"prep": "en", "suivant": "2020", "attendu": "temps", "cas": "en + année"},
    {"prep": "en", "suivant": "voiture", "attendu": "moyen", "cas": "en + véhicule"},
    # agent / moyen
    {"prep": "par", "suivant": "Marie", "precedent": "GV",
     "precedent_texte": "La lettre a été écrite", "attendu": "agent", "cas": "par + passif"},
    {"prep": "par", "suivant": "la porte", "precedent": "GV",
     "precedent_texte": "Il entre", "attendu": "moyen", "cas": "par + moyen"},
    # anglais
    {"prep": "over", "suivant": "the lazy dog", "attendu": "lieu", "cas": "over + lieu"},
    {"prep": "to", "suivant": "Mary", "attendu": "destinataire", "cas": "to + personne"},
    {"prep": "to", "suivant": "the station", "attendu": "lieu", "cas": "to + lieu"},
    {"prep": "at", "suivant": "9", "attendu": "temps", "cas": "at + heure"},
    {"prep": "at", "suivant": "home", "attendu": "lieu", "cas": "at + lieu"},
]
