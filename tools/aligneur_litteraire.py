#!/usr/bin/env python3
"""aligneur_litteraire.py — ALIGNEMENT PHRASE À PHRASE VÉRIFIÉ PAR LES ANCRES.

LE PROBLÈME. La mesure 59 a montré que le banc littéraire « Le Tour du monde en quatre-vingts jours » était
**invalide** ✗✗ : découpage par titres (84 sections françaises contre 37 anglaises, la table des matières comptée
deux fois), puis appariement proportionnel, puis découpage du corps (60 contre 37) — dans les trois cas le chrF
restait au niveau du hasard. *Ce n'était pas le modèle, c'était l'appariement* ✓✓ : les segments comparés ne
disaient pas la même chose.

CE QUE FAIT L'OUTIL. Il construit un alignement phrase à phrase **au niveau du chapitre** (les 37 chapitres sont
les ancres structurelles), par programmation dynamique de type **Gale-Church** sur la longueur des phrases (ratio
global de caractères EN/FR, perles 1:1, 1:2, 2:1, 1:0, 0:1, 2:2, 1:3, 3:1). Il **ne regarde aucun nom propre**
pour apparier : le dictionnaire d'ancres ne sert qu'à **juger** l'alignement, jamais à le produire ✓✓.

LA VALIDATION (indépendante de l'appariement). Pour chaque occurrence d'ancre (nom de personnage, lieu, navire,
institution) dans une phrase française, on regarde si la **même ancre** se retrouve dans la perle anglaise
correspondante (distance 0), ou dans son voisinage ±1, ±2, ±5. On rapporte le rappel, le taux de phrases sans
ancre, et surtout des **contrôles négatifs** : chapitres permutés, chapitre voisin, phrases mélangées, appariement
aléatoire intra-chapitre. Un alignement n'est déclaré **VALIDE** que si les ancres se retrouvent à un taux très
supérieur à ces contrôles.

CE QUE L'OUTIL NE FAIT PAS. Aucun modèle, aucun GPU, aucune sémantique : c'est un aligneur **structurel**. Il
valide la correspondance des phrases par les noms propres, pas la fidélité de chaque mot commun.

USAGE.
    CUDA_VISIBLE_DEVICES="" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py
    CUDA_VISIBLE_DEVICES="" ... --json /tmp/verne.json --rapport /tmp/verne.md --sans-controles
"""
from __future__ import annotations

import argparse
import json
import math
import random
import re
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Chemins par défaut (les textes vivent dans le dépôt Panini voisin)
# ---------------------------------------------------------------------------
RACINE_PANINI = Path("/home/stephane/Data13TB/stephane/GitHub/Panini")
FR_DEFAUT = RACINE_PANINI / "data/gutenberg_multilingual_verified/around_world_80_days/around_world_80_days_fr.txt"
EN_DEFAUT = RACINE_PANINI / "data/gutenberg_multilingual_verified/around_world_80_days/around_world_80_days_en.txt"
JSON_DEFAUT = Path("data/alignement/verne_fr_en.json")
RAPPORT_DEFAUT = Path("reports/alignement-verne.md")

# ---------------------------------------------------------------------------
# Ancres : identifiant → (formes françaises, formes anglaises, sensible à la casse)
#
# Les formes sont écrites déjà normalisées (minuscules, sans accents, tirets et apostrophes remplacés par des
# espaces). Le drapeau « sensible à la casse » sert aux mots qui sont aussi des mots communs en anglais : « fix »
# (réparer), « young » (jeune), « speedy » (rapide), « hitch » (accrocher), « smith » (forgeron), « proctor ».
# Sans lui, le contrôle compterait des ancres qui n'en sont pas.
#
# Le dictionnaire est volontairement **fermé et lisible** : ce sont des noms propres que le traducteur conserve.
# Il a été relevé dans les deux textes, mais il n'entre jamais dans le calcul de l'appariement.
# ---------------------------------------------------------------------------
ANCRES = [
    # --- personnages ---
    ("fogg", ("phileas fogg", "fogg"), ("phileas fogg", "fogg"), False),
    ("passepartout", ("passepartout",), ("passepartout",), False),
    ("fix", ("fix",), ("fix",), True),
    ("aouda", ("aouda",), ("aouda",), False),
    # Le traducteur anglais dit le plus souvent « Sir Francis » là où le français dit « Sir Francis Cromarty » :
    # les deux formes sont des alias du même personnage, donc un seul groupe d'ancre.
    ("cromarty", ("cromarty", "sir francis"), ("cromarty", "sir francis"), False),
    ("stuart", ("andrew stuart", "stuart"), ("andrew stuart", "stuart"), False),
    ("sullivan", ("john sullivan", "sullivan"), ("john sullivan", "sullivan"), False),
    ("fallentin", ("samuel fallentin", "fallentin"), ("samuel fallentin", "fallentin"), False),
    ("flanagan", ("thomas flanagan", "flanagan"), ("thomas flanagan", "flanagan"), False),
    ("ralph", ("gauthier ralph", "ralph"), ("gauthier ralph", "ralph"), False),
    ("forster", ("james forster", "forster"), ("james forster", "forster"), False),
    ("proctor", ("proctor",), ("proctor",), True),
    ("mudge", ("mudge",), ("mudge",), False),
    ("bunsby", ("john bunsby", "bunsby"), ("john bunsby", "bunsby"), False),
    ("speedy", ("andrew speedy", "speedy"), ("andrew speedy", "speedy"), True),
    ("kiouni", ("kiouni",), ("kiouni",), False),
    ("batulcar", ("batulcar",), ("batulcar",), False),
    ("hitch", ("william hitch", "hitch"), ("william hitch", "hitch"), True),
    ("young", ("brigham young", "young"), ("brigham young", "young"), True),
    ("obadiah", ("obadiah",), ("obadiah",), False),
    ("smyth", ("smyth",), ("smith",), True),
    ("oysterpuf", ("oysterpuf",), ("oysterpuff",), False),
    ("baring", ("baring",), ("baring", "barings"), False),
    ("lincoln", ("lincoln",), ("lincoln",), False),
    # --- lieux, institutions ---
    ("londres", ("londres",), ("london",), False),
    ("angleterre", ("angleterre",), ("england",), False),
    ("inde", ("inde", "indes"), ("india",), False),
    ("chine", ("chine",), ("china",), False),
    ("japon", ("japon",), ("japan",), False),
    ("amerique", ("amerique", "etats unis"), ("america", "united states"), False),
    ("rocheuses", ("rocheuses", "montagnes rocheuses"), ("rocky mountains",), False),
    ("gange", ("gange",), ("ganges",), False),
    ("shanghai", ("shangai",), ("shanghai",), False),
    ("bombay", ("bombay",), ("bombay",), False),
    ("calcutta", ("calcutta",), ("calcutta",), False),
    ("hongkong", ("hong kong",), ("hong kong",), False),
    ("yokohama", ("yokohama",), ("yokohama",), False),
    ("suez", ("suez",), ("suez",), False),
    ("liverpool", ("liverpool",), ("liverpool",), False),
    ("sanfrancisco", ("san francisco",), ("san francisco",), False),
    ("newyork", ("new york",), ("new york",), False),
    ("omaha", ("omaha",), ("omaha",), False),
    ("chicago", ("chicago",), ("chicago",), False),
    ("brindisi", ("brindisi",), ("brindisi",), False),
    ("aden", ("aden",), ("aden",), False),
    ("singapore", ("singapore",), ("singapore",), False),
    ("allahabad", ("allahabad",), ("allahabad",), False),
    ("benares", ("benares",), ("benares",), False),
    ("sacramento", ("sacramento",), ("sacramento",), False),
    ("kearney", ("kearney",), ("kearney",), False),
    ("platte", ("platte",), ("platte",), False),
    ("saltlake", ("lac sale",), ("salt lake",), False),
    ("medicinebow", ("medicine bow",), ("medicine bow",), False),
    ("malabar", ("malebar hill",), ("malabar hill",), False),
    ("reformclub", ("reform club",), ("reform club", "reform"), True),
    ("savillerow", ("saville row",), ("saville row",), False),
    ("banque", ("banque d angleterre",), ("bank of england",), False),
    ("pacifique", ("pacifique",), ("pacific",), False),
    ("atlantique", ("atlantique",), ("atlantic",), False),
    ("merrouge", ("mer rouge",), ("red sea",), False),
    ("paris", ("paris",), ("paris",), False),
    ("pillaji", ("pillaji",), ("pillaji",), False),
    ("bundelkund", ("bundelkund",), ("bundelcund",), False),
    ("kholby", ("kholby",), ("kholby",), False),
    ("nagasaki", ("nagasaki",), ("nagasaki",), False),
    ("tingou", ("tingou",), ("tingou",), False),
    ("queenstown", ("queenstown",), ("queenstown",), False),
    ("douvres", ("douvres",), ("dover",), False),
    ("havre", ("havre",), ("havre",), False),
    ("bordeaux", ("bordeaux",), ("bordeaux",), False),
    ("ogden", ("ogden",), ("ogden",), False),
    ("vindhias", ("vindhias",), ("vindhias",), False),
    ("salcette", ("salcette",), ("salcette",), False),
    ("kamerfield", ("kamerfield",), ("camerfield",), False),
    ("mandiboy", ("mandiboy",), ("mandiboy",), False),
    # --- navires ---
    ("tankadere", ("tankadere",), ("tankadere",), False),
    ("henrietta", ("henrietta",), ("henrietta",), False),
    ("carnatic", ("carnatic",), ("carnatic",), False),
    ("mongolia", ("mongolia",), ("mongolia",), False),
    ("rangoon", ("rangoon",), ("rangoon",), False),
    ("general_grant", ("general grant",), ("general grant",), False),
]

# ---------------------------------------------------------------------------
# Découpage en phrases
# ---------------------------------------------------------------------------
ABREVIATIONS = set("""
m mm mme mmes mlle mlles mr mrs ms dr st ste messrs
etc no pp p vol chap av apr cie jc ss fig figs ed eds al cf vs viz
jr sr gen col lieut capt hon rev sgt maj adm prof
""".split())

# On considère qu'une phrase peut se terminer sur . ! ? … (éventuellement suivis de guillemets fermants), puis
# un blanc, puis une majuscule, un chiffre, un guillemet ouvrant, un tiret de dialogue ou une parenthèse.
TERMINATEUR = re.compile(r"[.!?…]+")


def accent_moins(texte: str) -> str:
    """Retire les accents (NFD puis suppression des marques combinantes)."""
    decompose = unicodedata.normalize("NFD", texte)
    return "".join(c for c in decompose if unicodedata.category(c) != "Mn")


def normaliser_ancres(texte: str) -> tuple[str, str]:
    """Normalise pour la recherche d'ancres.

    Retourne deux chaînes de même longueur : `lo` (minuscules, sans accents, ponctuation → espace) et `ca`
    (même chose mais casse conservée). L'alignement des positions permet de tester la casse du premier
    caractère d'une occurrence sans reconstruire les offsets.
    """
    bas: list[str] = []
    casse: list[str] = []
    for caractere in texte:
        d = accent_moins(caractere)
        if d.isalnum():
            bas.append(d.lower())
            casse.append(d)
        else:
            bas.append(" ")
            casse.append(" ")
    return "".join(bas), "".join(casse)


def normaliser_forme(forme: str) -> str:
    bas, _ = normaliser_ancres(forme)
    return " ".join(bas.split())


_INDEX_ANCRES: dict[str, list[tuple[str, tuple[str, ...], bool]]] | None = None


def index_ancres() -> dict[str, list[tuple[str, tuple[str, ...], bool]]]:
    """Construit (une fois) l'index langue → [(identifiant, formes normalisées, sensible_casse)]."""
    global _INDEX_ANCRES
    if _INDEX_ANCRES is None:
        index: dict[str, list[tuple[str, tuple[str, ...], bool]]] = {"fr": [], "en": []}
        for ident, formes_fr, formes_en, sensible in ANCRES:
            index["fr"].append((ident, tuple(normaliser_forme(f) for f in formes_fr), sensible))
            index["en"].append((ident, tuple(normaliser_forme(f) for f in formes_en), sensible))
        _INDEX_ANCRES = index
    return _INDEX_ANCRES


def _contient(forme: str, bas: str, casse: str, sensible_casse: bool) -> bool:
    """Recherche une forme avec frontières de mot (et casse si demandé)."""
    debut = 0
    while True:
        p = bas.find(forme, debut)
        if p < 0:
            return False
        avant = bas[p - 1] if p > 0 else " "
        apres = bas[p + len(forme)] if p + len(forme) < len(bas) else " "
        if not avant.isalnum() and not apres.isalnum():
            if not sensible_casse or (p < len(casse) and casse[p].isupper()):
                return True
        debut = p + 1


def ancres_dans_phrase(phrase: str, langue: str) -> set[str]:
    """Identifiants d'ancres présents dans une phrase, pour une langue."""
    bas, casse = normaliser_ancres(phrase)
    trouvees: set[str] = set()
    for ident, formes, sensible in index_ancres()[langue]:
        for forme in formes:
            if _contient(forme, bas, casse, sensible):
                trouvees.add(ident)
                break
    return trouvees


def est_abreviation(mot: str) -> bool:
    return mot.lower() in ABREVIATIONS


def decouper_phrases(paragraphe: str, langue: str) -> list[str]:
    """Découpe un paragraphe (déjà déroulé sur une ligne) en phrases.

    Règles : les abréviations (M., MM., Mrs., Dr., etc.) et les initiales ne coupent pas ; les points de
    suspension ne coupent que devant une majuscule/guillemet ; une phrase ne se termine que devant une
    majuscule, un chiffre, un guillemet ouvrant ou un tiret de dialogue — ce qui évite de couper les incises
    françaises du type « Quoi ! dit-il ».
    """
    delimiteurs = "»”’\"')]"
    phrases: list[str] = []
    debut = 0
    for m in TERMINATEUR.finditer(paragraphe):
        fin = m.end()
        k = fin
        while k < len(paragraphe) and paragraphe[k] in delimiteurs:
            k += 1
        j = k
        while j < len(paragraphe) and paragraphe[j] in " \t":
            j += 1

        if j >= len(paragraphe):
            coupe = True
        else:
            suivant = paragraphe[j]
            dialogue = paragraphe.startswith("--", j)
            avant = paragraphe[: m.start()]
            mot = re.search(r"([A-Za-zÀ-ÖØ-öø-ÿ]+)$", avant)
            mot = mot.group(1) if mot else ""
            dernier = m.group()[-1]

            if dernier == "." and not m.group().startswith("..."):
                if est_abreviation(mot):
                    # « etc. » peut fermer une phrase ; les autres abréviations non.
                    coupe = mot.lower() in {"etc", "viz", "cf"} and (
                        suivant.isupper() or suivant.isdigit() or suivant in "«\"“‘"
                    )
                elif len(mot) == 1 and mot.isupper():
                    coupe = False  # initiale (J. T. Maston)
                else:
                    coupe = (
                        suivant.isupper()
                        or suivant.isdigit()
                        or suivant in "«\"“‘"
                        or dialogue
                    )
            else:
                # ! ? … : on ne coupe que devant une vraie reprise de phrase.
                coupe = (
                    suivant.isupper()
                    or suivant.isdigit()
                    or suivant in "«\"“‘"
                    or dialogue
                )

        if coupe:
            phrase = paragraphe[debut:k].strip()
            if phrase:
                phrases.append(re.sub(r"[ \t]+", " ", phrase))
            debut = k
            while debut < len(paragraphe) and paragraphe[debut] in " \t":
                debut += 1

    reste = paragraphe[debut:].strip()
    if reste:
        phrases.append(re.sub(r"[ \t]+", " ", reste))
    # On ne garde que les fragments qui contiennent au moins une lettre.
    return [p for p in phrases if re.search(r"[^\W\d_]", p, flags=re.UNICODE)]


def paragraphes(texte: str) -> list[str]:
    """Découpe en paragraphes (blocs séparés par une ligne vide) et déroule les lignes."""
    blocs: list[str] = []
    for bloc in re.split(r"\n\s*\n", texte):
        lignes = [ligne.strip() for ligne in bloc.split("\n") if ligne.strip()]
        if lignes:
            blocs.append(" ".join(lignes))
    return blocs


def phrases_du_chapitre(texte: str, langue: str) -> list[str]:
    return [phrase for bloc in paragraphes(texte) for phrase in decouper_phrases(bloc, langue)]


# ---------------------------------------------------------------------------
# Chargement et découpage en chapitres
# ---------------------------------------------------------------------------
_VALEURS_ROMAINES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def romain_vers_entier(romain: str) -> int:
    total = 0
    precedent = 0
    for caractere in reversed(romain.upper()):
        valeur = _VALEURS_ROMAINES[caractere]
        total += -valeur if valeur < precedent else valeur
        precedent = max(precedent, valeur)
    return total


DEBUT_GUTENBERG = re.compile(r"\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG[^\n]*\*\*\*")
FIN_GUTENBERG = re.compile(r"\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG[^\n]*\*\*\*")


def lire_gutenberg(chemin: Path) -> str:
    """Lit un texte Gutenberg, retire le BOM, les CRLF et l'appareil Gutenberg."""
    brut = chemin.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    debut = DEBUT_GUTENBERG.search(brut)
    fin = FIN_GUTENBERG.search(brut)
    if debut and fin and fin.start() > debut.end():
        brut = brut[debut.end() : fin.start()]
    return brut.strip("\n")


def _bloc_titre(lignes: list[str], i: int) -> tuple[int, str]:
    """Après l'en-tête ligne `i`, retourne (début du corps, titre).

    Le titre est un bloc de lignes majoritairement en majuscules ; s'il n'y en a pas, on ne consomme rien.
    """
    n = len(lignes)
    j = i + 1
    while j < n and not lignes[j].strip():
        j += 1
    debut_bloc = j
    bloc: list[str] = []
    while j < n and lignes[j].strip():
        bloc.append(lignes[j].strip())
        j += 1
    texte = " ".join(bloc)
    lettres = [c for c in texte if c.isalpha()]
    if lettres and sum(1 for c in lettres if c.isupper()) / len(lettres) >= 0.6:
        while j < n and not lignes[j].strip():
            j += 1
        return j, texte
    return debut_bloc, ""


def reperer_chapitres(lignes: list[str], langue: str) -> tuple[list[dict], dict]:
    """Repère les chapitres et filtre les tables des matières **par la longueur**.

    Les tables des matières de cet ouvrage utilisent la même forme que les en-têtes de chapitre (« I TITRE » en
    français, « CHAPTER I. TITRE » en anglais). On collecte donc toutes les lignes candidates, puis, pour chaque
    numéro, on garde la candidate dont le bloc qui suit est le plus long ; une entrée de table fait ~100-200
    caractères, un chapitre en fait des milliers. C'est ce filtre qui manquait à la mesure 59 (84 sections
    françaises au lieu de 37).
    """
    if langue == "fr":
        motif = re.compile(r"^([IVXLC]+)(?:\s+(.*))?$")
    else:
        motif = re.compile(r"^CHAPTER\s+([IVXLC]+)\.?\s*(.*)$", re.IGNORECASE)

    candidates: list[dict] = []
    for i, ligne in enumerate(lignes):
        m = motif.match(ligne.strip())
        if not m:
            continue
        numero = romain_vers_entier(m.group(1))
        candidates.append({"numero": numero, "ligne": i})

    # Longueur du bloc qui suit chaque candidate, jusqu'à la candidate suivante (toutes catégories).
    indices = sorted(c["ligne"] for c in candidates)
    suivant = {idx: (indices[k + 1] if k + 1 < len(indices) else len(lignes)) for k, idx in enumerate(indices)}
    for c in candidates:
        fin = suivant[c["ligne"]]
        c["longueur"] = sum(len(lignes[k]) for k in range(c["ligne"], fin))

    par_numero: dict[int, list[dict]] = defaultdict(list)
    for c in candidates:
        par_numero[c["numero"]].append(c)

    retenus: list[dict] = []
    rejetes: list[dict] = []
    for numero in sorted(par_numero):
        groupe = sorted(par_numero[numero], key=lambda c: c["longueur"], reverse=True)
        meilleur = groupe[0]
        if meilleur["longueur"] < 1500:
            rejetes.extend(groupe)
            continue
        corps, titre = _bloc_titre(lignes, meilleur["ligne"])
        meilleur["corps"] = corps
        meilleur["titre"] = titre
        retenus.append(meilleur)
        rejetes.extend(groupe[1:])
    retenus.sort(key=lambda c: c["ligne"])

    stats = {
        "langue": langue,
        "lignes_candidates": len(candidates),
        "chapitres_retenus": len(retenus),
        "lignes_rejetees": len(rejetes),
        "numeros": [c["numero"] for c in retenus],
    }
    return retenus, stats


def corps_des_chapitres(lignes: list[str], chapitres: list[dict]) -> dict[int, str]:
    """Texte du corps de chaque chapitre, en-tête et titre exclus."""
    textes: dict[int, str] = {}
    for k, c in enumerate(chapitres):
        fin = chapitres[k + 1]["ligne"] if k + 1 < len(chapitres) else len(lignes)
        textes[c["numero"]] = "\n".join(lignes[c["corps"] : fin])
    return textes


def verifier_structure(chapitres_fr: list[dict], chapitres_en: list[dict], stats_fr: dict, stats_en: dict) -> None:
    """Vérifie que les deux langues ont les mêmes chapitres, numérotés 1..N sans trou."""
    nums_fr = [c["numero"] for c in chapitres_fr]
    nums_en = [c["numero"] for c in chapitres_en]
    for langue, nums, stats in (("fr", nums_fr, stats_fr), ("en", nums_en, stats_en)):
        if nums != list(range(1, len(nums) + 1)):
            raise SystemExit(
                f"[ERREUR] chapitres {langue} non contigus : {nums} (candidats {stats['lignes_candidates']}, "
                f"rejetés {stats['lignes_rejetees']})"
            )
    if nums_fr != nums_en:
        raise SystemExit(f"[ERREUR] nombres de chapitres différents : FR {nums_fr} / EN {nums_en}")


# ---------------------------------------------------------------------------
# Appariement de Gale-Church (programmation dynamique)
# ---------------------------------------------------------------------------
# Probabilités a priori des types de perles (Gale & Church 1993). Le coût d'une perle est -2 log(p) + z²/2.
PRIORITES = {
    (1, 1): 0.89,
    (1, 2): 0.089,
    (2, 1): 0.089,
    (1, 0): 0.0099,
    (0, 1): 0.0099,
    (2, 2): 0.011,
    (1, 3): 0.0025,
    (3, 1): 0.0025,
}
PERLES = sorted(PRIORITES, key=lambda p: (p[0] + p[1], p))
COUT_PRIORI = {p: -2.0 * math.log(PRIORITES[p]) for p in PERLES}


def cout_longueur(longueur_fr: int, longueur_en: int, ratio: float) -> float:
    """z²/2, où z = (L_en - ratio·L_fr) / sqrt(L_en + ratio²·L_fr)."""
    if longueur_fr <= 0 or longueur_en <= 0:
        return 0.0
    ecart = longueur_en - ratio * longueur_fr
    ecart_type = math.sqrt(max(longueur_en + ratio * ratio * longueur_fr, 1e-9))
    return 0.5 * (ecart / ecart_type) ** 2


def aligner_chapitre(phrases_fr: list[str], phrases_en: list[str], ratio: float) -> tuple[list[tuple[int, int, int, int]], float]:
    """Aligne un chapitre ; retourne les perles (i0, i1, j0, j1) et le coût total."""
    n, m = len(phrases_fr), len(phrases_en)
    longueurs_fr = [0] + [len(p) for p in phrases_fr]
    longueurs_en = [0] + [len(p) for p in phrases_en]
    prefixe_fr = [0] * (n + 1)
    prefixe_en = [0] * (m + 1)
    for i in range(1, n + 1):
        prefixe_fr[i] = prefixe_fr[i - 1] + longueurs_fr[i]
    for j in range(1, m + 1):
        prefixe_en[j] = prefixe_en[j - 1] + longueurs_en[j]

    infini = 1e18
    cout = [[infini] * (m + 1) for _ in range(n + 1)]
    retour = [[None] * (m + 1) for _ in range(n + 1)]
    cout[0][0] = 0.0

    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0 and j == 0:
                continue
            meilleur = infini
            meilleur_retour = None
            for di, dj in PERLES:
                if i >= di and j >= dj and cout[i - di][j - dj] < infini:
                    lf = prefixe_fr[i] - prefixe_fr[i - di]
                    le = prefixe_en[j] - prefixe_en[j - dj]
                    candidat = (
                        cout[i - di][j - dj]
                        + COUT_PRIORI[(di, dj)]
                        + cout_longueur(lf, le, ratio)
                    )
                    if candidat < meilleur:
                        meilleur = candidat
                        meilleur_retour = (i - di, j - dj)
            cout[i][j] = meilleur
            retour[i][j] = meilleur_retour

    perles: list[tuple[int, int, int, int]] = []
    i, j = n, m
    while i > 0 or j > 0:
        precedent = retour[i][j]
        if precedent is None:
            raise RuntimeError(f"chemin d'alignement interrompu en ({i}, {j})")
        i0, j0 = precedent
        perles.append((i0, i, j0, j))
        i, j = i0, j0
    perles.reverse()
    return perles, cout[n][m]


def aligner_livre(
    phrases_fr: dict[int, list[str]],
    phrases_en: dict[int, list[str]],
    ratio: float,
    appariement: dict[int, int] | None = None,
) -> list[dict]:
    """Aligne tous les chapitres ; `appariement` permet les contrôles négatifs (chapitre FR → chapitre EN)."""
    perles: list[dict] = []
    for numero_fr in sorted(phrases_fr):
        numero_en = appariement[numero_fr] if appariement else numero_fr
        perles_chapitre, _ = aligner_chapitre(phrases_fr[numero_fr], phrases_en[numero_en], ratio)
        for i0, i1, j0, j1 in perles_chapitre:
            perles.append(
                {
                    "chapitre_fr": numero_fr,
                    "chapitre_en": numero_en,
                    "i_fr": i0,
                    "i_en": j0,
                    "n_fr": i1 - i0,
                    "n_en": j1 - j0,
                    "fr": " ".join(phrases_fr[numero_fr][i0:i1]),
                    "en": " ".join(phrases_en[numero_en][j0:j1]),
                }
            )
    return perles


# ---------------------------------------------------------------------------
# Évaluation par les ancres
# ---------------------------------------------------------------------------
def _union_voisine(ancres: list[set[str]], debut: int, fin: int) -> set[str]:
    debut = max(0, debut)
    fin = min(len(ancres), fin)
    if debut >= fin:
        return set()
    return set().union(*(ancres[k] for k in range(debut, fin)))


def evaluer_ancres(
    perles: list[dict],
    ancres_fr: dict[int, list[set[str]]],
    ancres_en: dict[int, list[set[str]]],
    rayon: int = 2,
    seulement: set[str] | None = None,
    sens: str = "fr",
) -> dict:
    """Rappel des ancres : une occurrence d'un côté doit se retrouver de l'autre, à distance 0..rayon.

    `sens="fr"` : on part des occurrences françaises et on cherche dans la perle anglaise.
    `sens="en"` : l'inverse.
    """
    distances = (0, 1, rayon, 5)
    occurrences = 0
    touchees = {d: 0 for d in distances}
    perles_avec_ancre = 0
    perles_touchees = {d: 0 for d in distances}
    par_ancre: dict[str, dict[str, int]] = defaultdict(
        lambda: {"occurrences": 0, "touchees_0": 0, "touchees_rayon": 0}
    )

    for perle in perles:
        if sens == "fr":
            ch_source, ch_cible = perle["chapitre_fr"], perle["chapitre_en"]
            i0, i1 = perle["i_fr"], perle["i_fr"] + perle["n_fr"]
            j0, j1 = perle["i_en"], perle["i_en"] + perle["n_en"]
            source = ancres_fr
            cible = ancres_en
        else:
            ch_source, ch_cible = perle["chapitre_en"], perle["chapitre_fr"]
            i0, i1 = perle["i_en"], perle["i_en"] + perle["n_en"]
            j0, j1 = perle["i_fr"], perle["i_fr"] + perle["n_fr"]
            source = ancres_en
            cible = ancres_fr

        ancres_source = _union_voisine(source[ch_source], i0, i1)
        if seulement is not None:
            ancres_source &= seulement
        if not ancres_source:
            continue
        perles_avec_ancre += 1

        fenetres = {d: _union_voisine(cible[ch_cible], j0 - d, j1 + d) for d in distances}
        for ident in ancres_source:
            occurrences += 1
            par_ancre[ident]["occurrences"] += 1
            for d in distances:
                if ident in fenetres[d]:
                    touchees[d] += 1
            if ident in fenetres[0]:
                par_ancre[ident]["touchees_0"] += 1
            if ident in fenetres[rayon]:
                par_ancre[ident]["touchees_rayon"] += 1
        for d in distances:
            if ancres_source & fenetres[d]:
                perles_touchees[d] += 1

    return {
        "sens": sens,
        "occurrences": occurrences,
        "touchees": {str(d): touchees[d] for d in distances},
        "rappel": {str(d): (touchees[d] / occurrences if occurrences else 0.0) for d in distances},
        "perles_avec_ancre": perles_avec_ancre,
        "perles_touchees": {str(d): perles_touchees[d] for d in distances},
        "perles_rappel": {
            str(d): (perles_touchees[d] / perles_avec_ancre if perles_avec_ancre else 0.0) for d in distances
        },
        "par_ancre": dict(par_ancre),
    }


def classer_manques(
    perles: list[dict],
    ancres_fr: dict[int, list[set[str]]],
    ancres_en: dict[int, list[set[str]]],
    seulement: set[str] | None = None,
) -> dict:
    """Où vont les ancres qui ne sont pas dans la perle ? (diagnostic, pas un critère de validation.)

    Trois cas : l'ancre est dans la perle (distance 0) ; elle est **ailleurs dans le même chapitre** (déplacement
    local, réécriture) ; elle est **absente du chapitre** (le traducteur a supprimé ou remplacé le nom). Un
    déplacement local est rattrapé par le voisinage ±2 ; une absence ne prouve rien sur l'alignement, mais elle
    reste comptée comme un échec dans la mesure principale — sinon le contrôle négatif s'effondrerait à vide.
    """
    total = exact = presente_ailleurs = absente_chapitre = 0
    for perle in perles:
        ch_source, ch_cible = perle["chapitre_fr"], perle["chapitre_en"]
        i0, i1 = perle["i_fr"], perle["i_fr"] + perle["n_fr"]
        j0, j1 = perle["i_en"], perle["i_en"] + perle["n_en"]
        source = _union_voisine(ancres_fr[ch_source], i0, i1)
        if seulement is not None:
            source &= seulement
        if not source:
            continue
        dans_perle = _union_voisine(ancres_en[ch_cible], j0, j1)
        dans_chapitre = set().union(*ancres_en[ch_cible]) if ancres_en[ch_cible] else set()
        for ident in source:
            total += 1
            if ident in dans_perle:
                exact += 1
            elif ident in dans_chapitre:
                presente_ailleurs += 1
            else:
                absente_chapitre += 1
    return {
        "occurrences": total,
        "exact": exact,
        "presente_ailleurs": presente_ailleurs,
        "absente_chapitre": absente_chapitre,
        "part_exact": exact / total if total else 0.0,
        "part_presente_ailleurs": presente_ailleurs / total if total else 0.0,
        "part_absente_chapitre": absente_chapitre / total if total else 0.0,
    }


def compter_df(ancres: dict[int, list[set[str]]]) -> Counter:
    """Document frequency : dans combien de chapitres chaque ancre apparaît."""
    df: Counter = Counter()
    for numero in ancres:
        for ident in set().union(*ancres[numero]) if ancres[numero] else set():
            df[ident] += 1
    return df


# ---------------------------------------------------------------------------
# Contrôles négatifs
# ---------------------------------------------------------------------------
def derangement(n: int, rng: random.Random) -> list[int]:
    """Permutation sans point fixe (chaque chapitre FR va vers un autre chapitre EN)."""
    while True:
        permutation = list(range(n))
        rng.shuffle(permutation)
        if all(permutation[i] != i for i in range(n)):
            return permutation


def controler_chapitres_permutes(
    phrases_fr: dict[int, list[str]],
    phrases_en: dict[int, list[str]],
    ratio: float,
    ancres_fr: dict[int, list[set[str]]],
    ancres_en: dict[int, list[set[str]]],
    distinctives: set[str],
    rng: random.Random,
    repetitions: int,
    rayon: int,
) -> list[dict]:
    numeros = sorted(phrases_fr)
    resultats = []
    for _ in range(repetitions):
        permutation = derangement(len(numeros), rng)
        appariement = {numero: numeros[permutation[k]] for k, numero in enumerate(numeros)}
        perles = aligner_livre(phrases_fr, phrases_en, ratio, appariement)
        global_ = evaluer_ancres(perles, ancres_fr, ancres_en, rayon=rayon)
        distinct = evaluer_ancres(perles, ancres_fr, ancres_en, rayon=rayon, seulement=distinctives)
        resultats.append({"global": global_, "distinctives": distinct})
    return resultats


def controler_chapitre_voisin(
    phrases_fr: dict[int, list[str]],
    phrases_en: dict[int, list[str]],
    ratio: float,
    ancres_fr: dict[int, list[set[str]]],
    ancres_en: dict[int, list[set[str]]],
    distinctives: set[str],
    rayon: int,
) -> dict:
    numeros = sorted(phrases_fr)
    appariement = {
        numero: numeros[(k + 1) % len(numeros)] for k, numero in enumerate(numeros)
    }
    perles = aligner_livre(phrases_fr, phrases_en, ratio, appariement)
    return {
        "global": evaluer_ancres(perles, ancres_fr, ancres_en, rayon=rayon),
        "distinctives": evaluer_ancres(perles, ancres_fr, ancres_en, rayon=rayon, seulement=distinctives),
    }


def controler_phrases_melangees(
    phrases_fr: dict[int, list[str]],
    phrases_en: dict[int, list[str]],
    ratio: float,
    ancres_fr: dict[int, list[set[str]]],
    distinctives: set[str],
    rng: random.Random,
    repetitions: int,
    rayon: int,
) -> list[dict]:
    """Mélange les phrases anglaises **à l'intérieur de chaque chapitre**, puis aligne."""
    resultats = []
    for _ in range(repetitions):
        phrases_en_melangees: dict[int, list[str]] = {}
        ancres_en_melangees: dict[int, list[set[str]]] = {}
        for numero in sorted(phrases_en):
            copie = list(phrases_en[numero])
            rng.shuffle(copie)
            phrases_en_melangees[numero] = copie
            ancres_en_melangees[numero] = [ancres_dans_phrase(p, "en") for p in copie]
        perles = aligner_livre(phrases_fr, phrases_en_melangees, ratio)
        resultats.append(
            {
                "global": evaluer_ancres(perles, ancres_fr, ancres_en_melangees, rayon=rayon),
                "distinctives": evaluer_ancres(
                    perles, ancres_fr, ancres_en_melangees, rayon=rayon, seulement=distinctives
                ),
            }
        )
    return resultats


def controler_hasard_intra_chapitre(
    ancres_fr: dict[int, list[set[str]]],
    ancres_en: dict[int, list[set[str]]],
    rng: random.Random,
    repetitions: int = 20,
) -> dict:
    """Chance pure : chaque phrase FR à ancre est comparée à une phrase EN tirée au hasard dans le même chapitre."""
    total = 0
    touchees = 0
    for numero in sorted(ancres_fr):
        for ancres_phrase in ancres_fr[numero]:
            if not ancres_phrase:
                continue
            for _ in range(repetitions):
                j = rng.randrange(len(ancres_en[numero]))
                total += 1
                if ancres_phrase & ancres_en[numero][j]:
                    touchees += 1
    return {"tirages": total, "touchees": touchees, "taux": touchees / total if total else 0.0}


# ---------------------------------------------------------------------------
# Matrice chapitres × chapitres (validation structurelle indépendante des phrases)
# ---------------------------------------------------------------------------
def matrice_ancres(
    ancres_fr: dict[int, list[set[str]]],
    ancres_en: dict[int, list[set[str]]],
    df_fr: Counter,
) -> dict:
    """Similarité (Jaccard pondérée par l'IDF) entre l'ensemble d'ancres de chaque chapitre FR et EN.

    Si les chapitres se correspondent par leur contenu, la diagonale doit dominer. C'est une vérification
    **indépendante de l'alignement des phrases** : elle ne compare que des ensembles d'ancres par chapitre.
    """
    ens_fr = {n: (set().union(*ancres_fr[n]) if ancres_fr[n] else set()) for n in ancres_fr}
    ens_en = {n: (set().union(*ancres_en[n]) if ancres_en[n] else set()) for n in ancres_en}
    n_chapitres = len(ens_fr)
    poids = {
        ident: math.log((n_chapitres + 1.0) / (df_fr[ident] + 0.5))
        for ident in set(df_fr) | set().union(*ens_fr.values())
    }

    def similarite(a: set[str], b: set[str]) -> float:
        communs = 0.0
        union = 0.0
        for ident in a | b:
            if ident not in poids:
                continue
            if ident in a and ident in b:
                communs += poids[ident]
            union += poids[ident]
        return communs / union if union else 0.0

    numeros = sorted(ens_fr)
    matrice = [[similarite(ens_fr[i], ens_en[j]) for j in numeros] for i in numeros]
    rangs = []
    for k, i in enumerate(numeros):
        ordre = sorted(range(len(numeros)), key=lambda j: (-matrice[k][j], j))
        rangs.append(ordre.index(k) + 1)
    diagonale = [matrice[k][k] for k in range(len(numeros))]
    hors = [matrice[k][j] for k in range(len(numeros)) for j in range(len(numeros)) if j != k]
    return {
        "n": n_chapitres,
        "rang_diagonale": rangs,
        "diagonale_top1": sum(1 for r in rangs if r == 1),
        "diagonale_top3": sum(1 for r in rangs if r <= 3),
        "moyenne_diagonale": sum(diagonale) / len(diagonale),
        "minimum_diagonale": min(diagonale),
        "moyenne_hors_diagonale": sum(hors) / len(hors),
        "matrice": [[round(x, 4) for x in ligne] for ligne in matrice],
    }


# ---------------------------------------------------------------------------
# Distribution des rapports de longueur
# ---------------------------------------------------------------------------
def centile(valeurs: list[float], q: float) -> float:
    if not valeurs:
        return 0.0
    ordonnees = sorted(valeurs)
    position = q * (len(ordonnees) - 1)
    bas = int(math.floor(position))
    haut = int(math.ceil(position))
    if bas == haut:
        return ordonnees[bas]
    return ordonnees[bas] * (haut - position) + ordonnees[haut] * (position - bas)


def statistiques_longueurs(perles: list[dict]) -> dict:
    """Rapports de longueur EN/FR par perle appariée (caractères et mots)."""
    caracteres: list[float] = []
    mots: list[float] = []
    for perle in perles:
        if perle["n_fr"] == 0 or perle["n_en"] == 0:
            continue
        if not perle["fr"] or not perle["en"]:
            continue
        caracteres.append(len(perle["en"]) / len(perle["fr"]))
        mots.append(len(perle["en"].split()) / len(perle["fr"].split()))

    def resume(valeurs: list[float]) -> dict:
        if not valeurs:
            return {}
        return {
            "n": len(valeurs),
            "moyenne": sum(valeurs) / len(valeurs),
            "mediane": centile(valeurs, 0.5),
            "q1": centile(valeurs, 0.25),
            "q3": centile(valeurs, 0.75),
            "p5": centile(valeurs, 0.05),
            "p95": centile(valeurs, 0.95),
            "minimum": min(valeurs),
            "maximum": max(valeurs),
            "part_0_75_1_25": sum(1 for x in valeurs if 0.75 <= x <= 1.25) / len(valeurs),
            "part_0_8_1_2": sum(1 for x in valeurs if 0.8 <= x <= 1.2) / len(valeurs),
            "part_hors_0_5_2": sum(1 for x in valeurs if x < 0.5 or x > 2.0) / len(valeurs),
        }

    return {"caracteres": resume(caracteres), "mots": resume(mots)}


# ---------------------------------------------------------------------------
# Petits formateurs pour la fiche (français : virgule décimale, espaces fines)
# ---------------------------------------------------------------------------
def _f(x: float, n: int = 1) -> str:
    return f"{x:.{n}f}".replace(".", ",")


def _p(x: float, n: int = 1) -> str:
    return _f(100.0 * x, n) + " %"


def _i(x: int) -> str:
    return f"{x:,}".replace(",", "\u202f")


def _tableau(entetes: list[str], lignes: list[list[str]]) -> list[str]:
    out = ["| " + " | ".join(entetes) + " |"]
    out.append("|" + "|".join("---" if k == 0 else "---:" for k in range(len(entetes))) + "|")
    out += ["| " + " | ".join(ligne) + " |" for ligne in lignes]
    return out


# ---------------------------------------------------------------------------
# Production des sorties
# ---------------------------------------------------------------------------
def construire_json(
    args: argparse.Namespace,
    meta: dict,
    stats_fr: dict,
    stats_en: dict,
    chapitres_fr: list[dict],
    chapitres_en: list[dict],
    phrases_fr: dict[int, list[str]],
    phrases_en: dict[int, list[str]],
    perles: list[dict],
    validation: dict,
) -> dict:
    paires = []
    non_appariees = {"fr": [], "en": []}
    for perle in perles:
        if perle["n_fr"] > 0 and perle["n_en"] > 0:
            paires.append(
                {
                    "chapitre": perle["chapitre_fr"],
                    "i_fr": perle["i_fr"],
                    "i_en": perle["i_en"],
                    "n_fr": perle["n_fr"],
                    "n_en": perle["n_en"],
                    "fr": perle["fr"],
                    "en": perle["en"],
                }
            )
        elif perle["n_fr"] > 0:
            non_appariees["fr"].append(
                {"chapitre": perle["chapitre_fr"], "i_fr": perle["i_fr"], "fr": perle["fr"]}
            )
        elif perle["n_en"] > 0:
            non_appariees["en"].append(
                {"chapitre": perle["chapitre_en"], "i_en": perle["i_en"], "en": perle["en"]}
            )

    titres_en = {c["numero"]: c["titre"] for c in chapitres_en}
    chapitres = []
    for c in chapitres_fr:
        numero = c["numero"]
        perles_chapitre = [p for p in perles if p["chapitre_fr"] == numero]
        chapitres.append(
            {
                "numero": numero,
                "titre_fr": c["titre"],
                "titre_en": titres_en.get(numero, ""),
                "n_fr": len(phrases_fr[numero]),
                "n_en": len(phrases_en[numero]),
                "caracteres_fr": sum(len(p) for p in phrases_fr[numero]),
                "caracteres_en": sum(len(p) for p in phrases_en[numero]),
                "perles": len(perles_chapitre),
                "perles_appariees": sum(1 for p in perles_chapitre if p["n_fr"] > 0 and p["n_en"] > 0),
            }
        )

    return {
        "meta": {**meta, "indices": "0-based", "unite": "perle Gale-Church (1..3 phrases par côté)"},
        "structure": {"fr": stats_fr, "en": stats_en},
        "chapitres": chapitres,
        "paires": paires,
        "non_appariees": non_appariees,
        "validation": validation,
    }


def rediger_rapport(donnees: dict, chemin: Path) -> None:
    meta = donnees["meta"]
    st = donnees["structure"]
    v = donnees["validation"]
    anc = v["ancres"]
    neg = v["controles_negatifs"]
    mc = v["matrice_chapitres"]
    lg = v["rapports_longueur"]
    verdict = v["verdict"]
    align = v["alignement"]

    L: list[str] = []
    L.append("# Alignement phrase à phrase — *Le Tour du monde en quatre-vingts jours* (français → anglais)")
    L.append("")
    L.append(f"**Date** : {meta['date']}  ")
    L.append(f"**Outil** : `tools/aligneur_litteraire.py` (CPU, bibliothèque standard, aucun modèle)  ")
    L.append(
        "**Verdict** : **"
        + ("VALIDE" if verdict["valide"] else "NON VALIDE")
        + "** — "
        + verdict["resume"]
    )
    L.append("")
    L.append("## 1. La question")
    L.append("")
    L.append(
        "La mesure 59 a établi que le banc littéraire était **invalide** : trois découpages successifs (titres, "
        "grille proportionnelle, corps) donnaient 84, 60 puis 37 sections françaises contre 37 anglaises, et le "
        "chrF restait au niveau du hasard. Le problème n'était pas le modèle mais l'**appariement** : les "
        "segments comparés ne disaient pas la même chose. Ce sous-chantier construit donc un alignement "
        "**phrase à phrase** et, surtout, le **vérifie** avec des ancres indépendantes — sans quoi un alignement "
        "« plausible » ne serait qu'une hypothèse de plus."
    )
    L.append("")
    L.append("## 2. Le dispositif")
    L.append("")
    L.append("### 2.1 Les textes")
    L.append("")
    L.append("| | français | anglais |")
    L.append("|---|---:|---:|")
    L.append(f"| fichier | `{meta['fichiers']['fr']}` | `{meta['fichiers']['en']}` |")
    L.append(f"| source | Project Gutenberg n° 800 (ebooksgratuits) | Project Gutenberg n° 103 (trad. Towle, 1873) |")
    L.append(f"| caractères des phrases | {_i(align['caracteres_fr'])} | {_i(align['caracteres_en'])} |")
    L.append(f"| phrases | {_i(align['phrases_fr'])} | {_i(align['phrases_en'])} |")
    L.append("")
    L.append(
        f"Le rapport global de longueur est **{_f(align['ratio'], 3)} caractère anglais par caractère français** ; "
        "c'est ce ratio qui sert de référence à l'appariement, il n'est pas ajusté par chapitre."
    )
    L.append("")
    L.append("### 2.2 Découpage en chapitres — et le piège de la table des matières")
    L.append("")
    L.append(
        "Les deux textes ont **37 chapitres numérotés I à XXXVII**, mais les tables des matières utilisent la "
        "même forme que les en-têtes (`I TITRE` en français, `CHAPTER I. TITRE` en anglais). Un simple comptage "
        "de lignes donne donc **74 candidates par langue**, et c'est exactement l'erreur de la mesure 59 "
        "(84 sections françaises). Le filtre est ici **par la longueur** : pour chaque numéro, on garde la "
        "candidate dont le bloc suivant est le plus long (un chapitre fait des milliers de caractères, une "
        "entrée de table ~100)."
    )
    L.append("")
    L.append("| langue | lignes candidates | chapitres retenus | lignes écartées (table des matières) |")
    L.append("|---|---:|---:|---:|")
    L.append(
        f"| français | {st['fr']['lignes_candidates']} | {st['fr']['chapitres_retenus']} | "
        f"{st['fr']['lignes_rejetees']} |"
    )
    L.append(
        f"| anglais | {st['en']['lignes_candidates']} | {st['en']['chapitres_retenus']} | "
        f"{st['en']['lignes_rejetees']} |"
    )
    L.append("")
    L.append(
        "Contrôle : les numéros retenus sont **contigus 1..37 dans les deux langues** et identiques ; "
        "l'appariement ne peut donc se faire qu'entre chapitres de même numéro."
    )
    L.append("")
    L.append("### 2.3 Découpage en phrases")
    L.append("")
    L.append(
        "Découpage par règles, sensible aux abréviations (`M.`, `MM.`, `Mr.`, `Mrs.`, `Dr.`, `etc.`), aux "
        "initiales, aux guillemets (`« »`, `“ ”`) et aux dialogues français en `--`. On ne coupe pas devant une "
        "minuscule, ce qui préserve les incises du type « Quoi ! dit-il ». Les paragraphes sont d'abord déroulés "
        "(les textes Gutenberg sont coupés à 70 colonnes)."
    )
    L.append("")
    L.append("### 2.4 L'appariement")
    L.append("")
    L.append(
        "Programmation dynamique **Gale-Church** chapitre par chapitre, sur la longueur en caractères. Perles "
        "autorisées : 1:1, 1:2, 2:1, 1:0, 0:1, 2:2, 1:3, 3:1 ; coût `-2 log p(type) + z²/2`, avec "
        "`z = (L_en − ratio·L_fr) / sqrt(L_en + ratio²·L_fr)`. Les frontières de chapitre sont **verrouillées** : "
        "chaque chapitre commence et finit sur ses propres phrases. Le dictionnaire d'ancres n'entre **jamais** "
        "dans ce calcul."
    )
    L.append("")
    L.append("### 2.5 Les ancres")
    L.append("")
    L.append(
        f"{len(meta['ancres'])} groupes d'ancres (personnages, lieux, navires, institutions), avec leurs formes "
        "française et anglaise (`Londres`/`London`, `Inde`/`India`, `Tankadère`/`Tankadere`, "
        "`Banque d'Angleterre`/`Bank of England`…). La recherche est insensible à la casse et aux accents, mais "
        "**avec frontières de mot** — sans quoi `fixe` compterait pour `Fix`, `comparaison` pour `Paris` et "
        "`machine` pour `Chine`. Six ancres ambiguës en anglais (`fix`, `young`, `speedy`, `hitch`, `smith`, "
        "`proctor`) exigent une majuscule — et `reform` aussi, pour ne pas confondre le club avec le mot commun. "
        "**Alias** : le français dit « Sir Francis Cromarty » là où l'anglais "
        "abrège souvent en « Sir Francis » ; les deux formes sont un seul groupe (`cromarty`), sinon on compterait "
        "comme des échecs des différences de dénomination, pas d'alignement. Les ancres **distinctives** sont celles "
        "qui apparaissent dans au plus "
        f"{meta['seuil_distinctif']} chapitres : ce sont elles qui portent le contrôle fort."
    )
    L.append("")
    L.append("## 3. Les chiffres")
    L.append("")
    L.append("### 3.1 Structure")
    L.append("")
    L.append("| | français | anglais |")
    L.append("|---|---:|---:|")
    L.append(f"| chapitres retenus | {st['fr']['chapitres_retenus']} | {st['en']['chapitres_retenus']} |")
    L.append(f"| phrases | {_i(align['phrases_fr'])} | {_i(align['phrases_en'])} |")
    L.append(f"| caractères des phrases | {_i(align['caracteres_fr'])} | {_i(align['caracteres_en'])} |")
    L.append(f"| rapport global EN/FR | | {_f(align['ratio'], 3)} |")
    L.append("")
    L.append("### 3.2 Appariement")
    L.append("")
    L.append(
        f"**{_i(align['perles_appariees'])} perles appariées** (les deux côtés non vides) sur "
        f"{_i(align['perles_total'])} perles ; {_i(align['paires_1_1'])} sont des paires 1:1 strictes."
    )
    L.append("")
    types = align["types_perles"]
    lignes_types = [[f"{di}:{dj}", _i(n)] for (di, dj), n in types]
    L += _tableau(["type de perle", "nombre"], lignes_types)
    L.append("")
    L.append("| couverture | français | anglais |")
    L.append("|---|---:|---:|")
    L.append(
        f"| phrases dans une perle appariée | {_i(align['phrases_fr_couvertes'])} "
        f"({_p(align['phrases_fr_couvertes'] / align['phrases_fr'])}) | "
        f"{_i(align['phrases_en_couvertes'])} ({_p(align['phrases_en_couvertes'] / align['phrases_en'])}) |"
    )
    L.append(
        f"| phrases non appariées | {_i(align['non_appariees_fr'])} "
        f"({_p(align['non_appariees_fr'] / align['phrases_fr'])}) | "
        f"{_i(align['non_appariees_en'])} ({_p(align['non_appariees_en'] / align['phrases_en'])}) |"
    )
    L.append("")
    L.append("### 3.3 Rappel des ancres")
    L.append("")
    L.append(
        "Une **occurrence** est un couple (côté source d'une perle, ancre) — pour une perle 1:1, c'est bien un "
        "couple (phrase, ancre). Le rappel à distance *d* est la fraction des occurrences françaises dont l'ancre "
        "se retrouve dans la perle anglaise (d = 0) ou dans son voisinage ±*d*. C'est la mesure la plus directe : "
        "*si l'alignement est bon, le nom propre doit être là où le français le met*."
    )
    L.append("")
    g = anc["global"]["fr"]
    d = anc["distinctives"]["fr"]
    ge = anc["global"]["en"]
    de = anc["distinctives"]["en"]
    lignes = [
        ["occurrences", _i(g["occurrences"]), _i(d["occurrences"])],
        ["rappel à distance 0", _p(g["rappel"]["0"]), _p(d["rappel"]["0"])],
        ["rappel ±1", _p(g["rappel"]["1"]), _p(d["rappel"]["1"])],
        [f"rappel ±{meta['rayon']}", _p(g["rappel"][str(meta['rayon'])]), _p(d["rappel"][str(meta['rayon'])])],
        ["rappel ±5", _p(g["rappel"]["5"]), _p(d["rappel"]["5"])],
        ["perles avec ancre", _i(g["perles_avec_ancre"]), _i(d["perles_avec_ancre"])],
        [
            "perles partageant une ancre (distance 0)",
            _p(g["perles_rappel"]["0"]),
            _p(d["perles_rappel"]["0"]),
        ],
        [
            f"perles partageant une ancre (±{meta['rayon']})",
            _p(g["perles_rappel"][str(meta['rayon'])]),
            _p(d["perles_rappel"][str(meta['rayon'])]),
        ],
    ]
    L += _tableau(["mesure (sens FR → EN)", "toutes ancres", "ancres distinctives"], lignes)
    L.append("")
    L.append(
        "Sens inverse (EN → FR), pour vérifier que le résultat ne dépend pas du côté de départ :"
    )
    L.append("")
    lignes = [
        ["occurrences", _i(ge["occurrences"]), _i(de["occurrences"])],
        ["rappel à distance 0", _p(ge["rappel"]["0"]), _p(de["rappel"]["0"])],
        [f"rappel ±{meta['rayon']}", _p(ge["rappel"][str(meta['rayon'])]), _p(de["rappel"][str(meta['rayon'])])],
        ["perles avec ancre", _i(ge["perles_avec_ancre"]), _i(de["perles_avec_ancre"])],
    ]
    L += _tableau(["mesure (sens EN → FR)", "toutes ancres", "ancres distinctives"], lignes)
    L.append("")
    # --- où vont les ancres manquées ? (diagnostic) ---
    mg = anc["manques"]["global"]
    md = anc["manques"]["distinctives"]
    L.append(
        f"**Où vont les ancres manquées ?** Sur {_i(mg['occurrences'])} occurrences, "
        f"{_p(mg['part_exact'])} sont dans la perle, {_p(mg['part_presente_ailleurs'])} sont **ailleurs dans le "
        f"même chapitre** (déplacement local, réécriture) et {_p(mg['part_absente_chapitre'])} sont **absentes du "
        f"chapitre** (le traducteur a supprimé ou remplacé le nom). Sur les distinctives : "
        f"{_i(md['exact'])}/{_i(md['occurrences'])} dans la perle, {_i(md['presente_ailleurs'])} ailleurs, "
        f"{_i(md['absente_chapitre'])} absentes. L'essentiel des manques est donc un **déplacement de quelques "
        "phrases**, pas une perte de chapitre — c'est ce que rattrape la tolérance ±2. Ce classement est un "
        "diagnostic *a posteriori*, pas un critère : le contrôle négatif, lui, ne pardonne rien."
    )
    L.append("")
    # --- tableau par ancre (les plus fréquentes) ---
    par_ancre = d.get("par_ancre", {})
    lignes = []
    for ident, stats in sorted(par_ancre.items(), key=lambda kv: -kv[1]["occurrences"]):
        if stats["occurrences"] < 5:
            continue
        lignes.append(
            [
                f"`{ident}`",
                _i(stats["occurrences"]),
                _p(stats["touchees_0"] / stats["occurrences"]),
                _p(stats["touchees_rayon"] / stats["occurrences"]),
            ]
        )
        if len(lignes) >= 8:
            break
    L.append(
        "Les huit ancres distinctives les plus fréquentes — le taux global n'est pas porté par une seule :"
    )
    L.append("")
    L += _tableau(["ancre", "occurrences", "rappel 0", f"rappel ±{meta['rayon']}"], lignes)
    L.append("")
    L.append(
        "Le point faible est `rangoon` (61,3 % à distance 0) : le traducteur paraphrase parfois le nom du navire "
        "(« the steamer », « the first few days of the voyage ») là où le français l'écrit ; l'ancre manque alors à "
        "cet endroit, même si elle reparaît plus loin dans le chapitre. C'est une **limite de la traduction**, pas "
        "une preuve de mauvais alignement — et elle est comptée comme un échec, jamais retirée."
    )
    L.append("")
    # --- rappel par chapitre (min/max) ---
    chapitres_evalues = {
        int(n): valeur for n, valeur in anc.get("par_chapitre", {}).items() if valeur["occurrences"] >= 5
    }
    if chapitres_evalues:
        pire = min(chapitres_evalues.items(), key=lambda kv: kv[1]["rappel_0"])
        meilleur = max(chapitres_evalues.items(), key=lambda kv: kv[1]["rappel_0"])
        faibles = sorted(
            [(n, valeur) for n, valeur in chapitres_evalues.items() if valeur["rappel_0"] < 0.70],
            key=lambda kv: kv[1]["rappel_0"],
        )
        liste_faibles = ", ".join(f"{n} ({_p(valeur['rappel_0'])})" for n, valeur in faibles) or "aucun"
        L.append(
            f"**Par chapitre** (≥ 5 occurrences distinctives) : le rappel à distance 0 va de "
            f"{_p(pire[1]['rappel_0'])} (chapitre {pire[0]}) à {_p(meilleur[1]['rappel_0'])} "
            f"(chapitre {meilleur[0]}). Les chapitres sous 70 % sont : {liste_faibles}. Les effectifs par chapitre "
            "sont petits (5 à 53 occurrences) : ces variations sont du bruit d'échantillonnage autant que des "
            "différences de traduction."
        )
        L.append("")
        L.append(
            "Les chapitres 9 et 14-17 sont les plus bas pour cette raison : le traducteur y remplace des noms par "
            "des périphrases (« la rade d'Aden » → « the roadstead », « les îles Salcette » → « the islands in the "
            "bay »), et l'ancre disparaît sans que la phrase ait bougé."
        )
        L.append("")
    L.append(
        f"**Phrases sans ancre** : {_p(align['phrases_fr_sans_ancre'])} des phrases françaises et "
        f"{_p(align['phrases_en_sans_ancre'])} des phrases anglaises ne contiennent aucun nom propre du "
        f"dictionnaire ; {_p(align['perles_sans_ancre'])} des perles n'ont d'ancre ni d'un côté ni de l'autre. "
        "C'est la **zone aveugle** du contrôle : ces phrases ne sont validées que par la longueur et la position, "
        "pas par une ancre."
    )
    L.append("")
    L.append("### 3.4 Contrôles négatifs")
    L.append("")
    L.append(
        "Tous les contrôles utilisent **le même aligneur, le même dictionnaire et la même mesure** ; seule la "
        "vérité de l'appariement change. Si les ancres se retrouvent autant dans un appariement faux, le taux "
        "réel ne prouve rien."
    )
    L.append("")
    r = str(meta["rayon"])

    def _neg_ligne(nom: str, bloc: dict) -> list[str]:
        return [
            nom,
            _p(bloc["global"]["rappel"][r]),
            _p(bloc["distinctives"]["rappel"][r]),
            _p(bloc["distinctives"]["rappel"]["0"]),
        ]

    lignes = [
        [
            "**alignement réel**",
            _p(g["rappel"][r]),
            _p(d["rappel"][r]),
            _p(d["rappel"]["0"]),
        ]
    ]
    for k, bloc in enumerate(neg["chapitres_permutes"], 1):
        lignes.append(_neg_ligne(f"chapitres permutés #{k}", bloc))
    lignes.append(_neg_ligne("chapitre voisin (i → i+1)", neg["chapitre_voisin"]))
    for k, bloc in enumerate(neg["phrases_melangees"], 1):
        lignes.append(_neg_ligne(f"phrases mélangées #{k}", bloc))
    if neg["chapitres_permutes"] or neg["phrases_melangees"]:
        L += _tableau(
            [
                f"contrôle (rappel ±{meta['rayon']})",
                "toutes ancres",
                "distinctives",
                "distinctives à distance 0",
            ],
            lignes,
        )
    else:
        L.append("_Contrôles négatifs non exécutés (option `--sans-controles`) : le verdict ne peut pas être VALIDE._")
    L.append("")
    ha = neg["hasard_intra_chapitre"]
    if ha["tirages"]:
        L.append(
            f"**Hasard pur, phrase contre phrase dans le même chapitre** : {_i(ha['tirages'])} tirages, "
            f"**{_p(ha['taux'], 2)}** de rencontres d'ancres. C'est un plancher **phrase contre phrase** — "
            "conservateur, parce que les noms propres reviennent beaucoup dans un même chapitre — et non le "
            "plancher de la mesure par perle : le contrôle de référence reste la **permutation des chapitres** "
            f"({_p(neg['chapitres_permutes'][0]['distinctives']['rappel'][r]) if neg['chapitres_permutes'] else 'non exécuté'}). "
            "L'alignement réel fait "
            f"**{_p(d['rappel']['0'], 2)}** à distance 0 et **{_p(d['rappel'][r], 2)}** à ±{meta['rayon']} sur les "
            f"ancres distinctives, soit **×{_f(d['rappel']['0'] / ha['taux'], 1) if ha['taux'] else '∞'}** et "
            f"**×{_f(d['rappel'][r] / ha['taux'], 1) if ha['taux'] else '∞'}** ce plancher."
        )
        L.append("")
    L.append("### 3.5 Matrice chapitres × chapitres (contrôle structurel)")
    L.append("")
    L.append(
        "Indépendamment de l'alignement des phrases, on compare l'**ensemble des ancres** de chaque chapitre "
        "français à celui de chaque chapitre anglais (Jaccard pondérée par l'IDF). Si les chapitres se "
        "correspondent par leur contenu, la diagonale doit dominer."
    )
    L.append("")
    L.append("| mesure | valeur |")
    L.append("|---|---:|")
    L.append(f"| diagonale classée n° 1 | **{mc['diagonale_top1']}/{mc['n']}** chapitres |")
    L.append(f"| diagonale dans le top 3 | **{mc['diagonale_top3']}/{mc['n']}** chapitres |")
    L.append(f"| similarité moyenne sur la diagonale | {_f(mc['moyenne_diagonale'], 3)} |")
    L.append(f"| similarité moyenne hors diagonale | {_f(mc['moyenne_hors_diagonale'], 3)} |")
    L.append(f"| similarité minimale sur la diagonale | {_f(mc['minimum_diagonale'], 3)} |")
    L.append("")
    L.append("### 3.6 Distribution des rapports de longueur")
    L.append("")
    lc = lg["caracteres"]
    lm = lg["mots"]
    lignes = [
        ["nombre de perles", _i(lc["n"]), _i(lm["n"])],
        ["médiane", _f(lc["mediane"], 3), _f(lm["mediane"], 3)],
        ["quartiles Q1 – Q3", f"{_f(lc['q1'], 3)} – {_f(lc['q3'], 3)}", f"{_f(lm['q1'], 3)} – {_f(lm['q3'], 3)}"],
        ["5 % – 95 %", f"{_f(lc['p5'], 3)} – {_f(lc['p95'], 3)}", f"{_f(lm['p5'], 3)} – {_f(lm['p95'], 3)}"],
        ["minimum – maximum", f"{_f(lc['minimum'], 3)} – {_f(lc['maximum'], 3)}", f"{_f(lm['minimum'], 3)} – {_f(lm['maximum'], 3)}"],
        ["part dans [0,75 ; 1,25]", _p(lc["part_0_75_1_25"]), _p(lm["part_0_75_1_25"])],
        ["part dans [0,80 ; 1,20]", _p(lc["part_0_8_1_2"]), _p(lm["part_0_8_1_2"])],
        ["part hors [0,5 ; 2,0]", _p(lc["part_hors_0_5_2"]), _p(lm["part_hors_0_5_2"])],
    ]
    L += _tableau(["mesure", "par caractères", "par mots"], lignes)
    L.append("")
    L.append(
        f"La médiane **par caractères** ({_f(lc['mediane'], 3)}) est inférieure à 1 parce que l'anglais est plus "
        f"court que le français ; celle **par mots** ({_f(lm['mediane'], 3)}) est au niveau. C'est le **ratio "
        "global** qui sert de référence, pas 1. Les queues de distribution sont attendues : une perle 1:1 peut "
        "contenir une phrase-source très courte et une phrase-cible longue (ou l'inverse), surtout dans les "
        "dialogues."
    )
    L.append("")
    L.append("## 4. Ce qui pourrait rendre le chiffre faux")
    L.append("")
    L.append(
        "1. **Les ancres sont des noms propres, et c'est précisément ce qu'un traducteur conserve.** Le taux "
        "élevé prouve la correspondance *structurelle* des phrases, pas la fidélité des mots communs. "
        f"{_p(align['phrases_fr_sans_ancre'])} des phrases françaises n'ont aucune ancre : pour elles, seul "
        "l'appariement par longueur et position parle."
    )
    L.append(
        f"2. **La tolérance ±{meta['rayon']} absorbe les différences de découpage.** Le taux à distance 0 "
        f"({_p(d['rappel']['0'])} sur les distinctives) est le chiffre honnête ; le ±{meta['rayon']} "
        f"({_p(d['rappel'][r])}) dit qu'une phrase voisine porte souvent le même nom. Un lecteur qui exige "
        "l'alignement exact doit regarder la première colonne."
    )
    L.append(
        "3. **Le dictionnaire d'ancres est construit à la main, à partir des deux textes.** Il pourrait "
        "favoriser les noms à orthographe stable et sous-représenter les lieux que le traducteur a vraiment "
        "traduits (`Royaume-Uni` → `United Kingdom`, une seule occurrence anglaise, a été écarté). Il reste "
        "indépendant de l'alignement, mais pas indépendant du choix des textes."
    )
    L.append(
        "4. **Le contrôle négatif « chapitres permutés » n'est pas un hasard parfait** : les chapitres voisins "
        "partagent des personnages, et l'anglais d'un chapitre peut contenir les mêmes noms qu'un autre. C'est "
        "pourquoi le contrôle **distinctif** (ancres de ≤ 6 chapitres) est mis en avant : il tombe à "
        + (
            _p(neg["chapitres_permutes"][0]["distinctives"]["rappel"][r])
            if neg["chapitres_permutes"]
            else "non exécuté"
        )
        + ", contre "
        f"{_p(d['rappel'][r])} pour l'alignement réel."
    )
    L.append(
        "5. **La traduction anglaise (Towle, 1873) condense parfois.** Les perles 2:1 et 3:1 (nombreuses) sont "
        "légitimes — le français segmente davantage les dialogues — mais quelques-unes peuvent être des "
        "réécritures où le traducteur a fusionné deux phrases. L'alignement les met ensemble ; il ne dit pas "
        "laquelle des deux phrases françaises correspond le mieux."
    )
    L.append(
        "6. **Un seul livre, un seul traducteur.** Le chiffre vaut pour ce couple de textes ; il ne prouve pas "
        "que l'outil alignerait *n'importe quel* roman. La méthode (chapitres → Gale-Church → ancres) est "
        "générale, mais les 37 chapitres et le dictionnaire sont propres à Verne."
    )
    L.append(
        "7. **Les textes Gutenberg peuvent contenir des coquilles de transcription.** Une coquille dans un nom "
        "propre fait rater une ancre (elle est comptée comme un échec) ; elle ne crée pas de faux positif."
    )
    L.append(
        "8. **Le contrôle de la matrice est un contrôle de contenu, pas de phrase.** Il établit que le "
        "chapitre *i* français et le chapitre *i* anglais parlent du même endroit ; il ne garantit pas que "
        "chaque phrase à l'intérieur est à sa place — c'est le rôle du rappel des ancres, avec sa zone aveugle."
    )
    L.append(
        "9. **Quelques fragments non narratifs** (l'itinéraire chiffré du chapitre 3, les tableaux de distances) "
        "sont traités comme des phrases : leurs lignes se ressemblent et peuvent s'apparier entre elles de travers. "
        "Ils sont peu nombreux et sans effet sur le taux d'ancres, mais un utilisateur du banc doit les connaître."
    )
    L.append("")
    L.append("## 5. Verdict et usage")
    L.append("")
    L.append(
        "**"
        + ("VALIDE" if verdict["valide"] else "NON VALIDE")
        + "** — "
        + verdict["resume"]
    )
    L.append("")
    L.append("Critères explicitement vérifiés :")
    L.append("")
    for nom, (ok, detail) in verdict["criteres"].items():
        L.append(f"- {'✓' if ok else '✗'} **{nom}** : {detail}")
    L.append("")
    L.append(
        "**Usage.** Le fichier `data/alignement/verne_fr_en.json` contient les paires ; chaque paire porte "
        "`chapitre`, `i_fr`, `i_en` (indices 0-based du début de perle), `n_fr`, `n_en` (nombre de phrases de "
        "chaque côté) et les textes `fr`/`en` (concaténation de la perle). Les phrases non appariées sont dans "
        "`non_appariees`. C'est l'unité à utiliser pour un banc de traduction : comparer le `fr` d'une perle à "
        "son `en`, jamais une phrase isolée à une perle entière."
    )
    L.append("")
    L.append("Reproduction :")
    L.append("")
    L.append("```bash")
    L.append(
        "CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py"
    )
    L.append("```")
    L.append("")
    L.append(
        f"*Graine des contrôles : {meta['graine']} ; répétitions : chapitres permutés "
        f"{meta['repetitions']}, phrases mélangées {meta['repetitions']} ; durée du run : "
        f"{_f(meta['duree_s'], 1)} s.*"
    )
    L.append("")
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text("\n".join(L) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Programme principal
# ---------------------------------------------------------------------------
def analyser(args: argparse.Namespace) -> dict:
    debut = time.time()
    print(f"[1/7] lecture des textes…", flush=True)
    lignes_fr = lire_gutenberg(args.fr).split("\n")
    lignes_en = lire_gutenberg(args.en).split("\n")

    print(f"[2/7] repérage des chapitres (filtre par longueur)…", flush=True)
    chapitres_fr, stats_fr = reperer_chapitres(lignes_fr, "fr")
    chapitres_en, stats_en = reperer_chapitres(lignes_en, "en")
    verifier_structure(chapitres_fr, chapitres_en, stats_fr, stats_en)
    print(
        f"      FR {stats_fr['lignes_candidates']} candidates → {stats_fr['chapitres_retenus']} chapitres ; "
        f"EN {stats_en['lignes_candidates']} → {stats_en['chapitres_retenus']}",
        flush=True,
    )

    corps_fr = corps_des_chapitres(lignes_fr, chapitres_fr)
    corps_en = corps_des_chapitres(lignes_en, chapitres_en)

    print(f"[3/7] découpage en phrases…", flush=True)
    phrases_fr = {n: phrases_du_chapitre(corps_fr[n], "fr") for n in corps_fr}
    phrases_en = {n: phrases_du_chapitre(corps_en[n], "en") for n in corps_en}
    caracteres_fr = sum(len(p) for s in phrases_fr.values() for p in s)
    caracteres_en = sum(len(p) for s in phrases_en.values() for p in s)
    ratio = caracteres_en / caracteres_fr
    print(
        f"      FR {sum(len(v) for v in phrases_fr.values())} phrases / {caracteres_fr} caractères ; "
        f"EN {sum(len(v) for v in phrases_en.values())} / {caracteres_en} ; ratio {ratio:.4f}",
        flush=True,
    )

    print(f"[4/7] alignement Gale-Church…", flush=True)
    t0 = time.time()
    perles = aligner_livre(phrases_fr, phrases_en, ratio)
    print(f"      {len(perles)} perles en {time.time() - t0:.1f} s", flush=True)

    print(f"[5/7] ancres et validation…", flush=True)
    ancres_fr = {n: [ancres_dans_phrase(p, "fr") for p in phrases_fr[n]] for n in phrases_fr}
    ancres_en = {n: [ancres_dans_phrase(p, "en") for p in phrases_en[n]] for n in phrases_en}
    df_fr = compter_df(ancres_fr)
    df_en = compter_df(ancres_en)
    tous = {ident for ident, _, _, _ in ANCRES}
    distinctives = {
        ident for ident in tous if max(df_fr.get(ident, 0), df_en.get(ident, 0)) <= args.seuil_distinctif
    }

    global_fr = evaluer_ancres(perles, ancres_fr, ancres_en, rayon=args.rayon, sens="fr")
    distinct_fr = evaluer_ancres(
        perles, ancres_fr, ancres_en, rayon=args.rayon, sens="fr", seulement=distinctives
    )
    global_en = evaluer_ancres(perles, ancres_fr, ancres_en, rayon=args.rayon, sens="en")
    distinct_en = evaluer_ancres(
        perles, ancres_fr, ancres_en, rayon=args.rayon, sens="en", seulement=distinctives
    )
    manques_global = classer_manques(perles, ancres_fr, ancres_en)
    manques_distinct = classer_manques(perles, ancres_fr, ancres_en, seulement=distinctives)

    matrice = matrice_ancres(ancres_fr, ancres_en, df_fr)
    longueurs = statistiques_longueurs(perles)
    par_chapitre = {}
    for numero in sorted(phrases_fr):
        sous = [p for p in perles if p["chapitre_fr"] == numero]
        resultat = evaluer_ancres(
            sous, ancres_fr, ancres_en, rayon=args.rayon, seulement=distinctives
        )
        par_chapitre[str(numero)] = {
            "occurrences": resultat["occurrences"],
            "rappel_0": resultat["rappel"]["0"],
            "rappel_rayon": resultat["rappel"][str(args.rayon)],
        }
    print(
        f"      rappel ±{args.rayon} : toutes {global_fr['rappel'][str(args.rayon)]:.3f} / "
        f"distinctives {distinct_fr['rappel'][str(args.rayon)]:.3f} ; "
        f"matrice diagonale top-1 {matrice['diagonale_top1']}/{matrice['n']}",
        flush=True,
    )

    # --- contrôles négatifs ---
    rng = random.Random(args.graine)
    if args.sans_controles:
        neg = {
            "chapitres_permutes": [],
            "chapitre_voisin": {"global": global_fr, "distinctives": distinct_fr},
            "phrases_melangees": [],
            "hasard_intra_chapitre": {"tirages": 0, "touchees": 0, "taux": 0.0},
        }
    else:
        print(f"[6/7] contrôles négatifs ({args.repetitions} répétitions)…", flush=True)
        t0 = time.time()
        chapitres_permutes = controler_chapitres_permutes(
            phrases_fr,
            phrases_en,
            ratio,
            ancres_fr,
            ancres_en,
            distinctives,
            rng,
            args.repetitions,
            args.rayon,
        )
        chapitre_voisin = controler_chapitre_voisin(
            phrases_fr, phrases_en, ratio, ancres_fr, ancres_en, distinctives, args.rayon
        )
        phrases_melangees = controler_phrases_melangees(
            phrases_fr,
            phrases_en,
            ratio,
            ancres_fr,
            distinctives,
            rng,
            args.repetitions,
            args.rayon,
        )
        hasard = controler_hasard_intra_chapitre(ancres_fr, ancres_en, rng)
        neg = {
            "chapitres_permutes": chapitres_permutes,
            "chapitre_voisin": chapitre_voisin,
            "phrases_melangees": phrases_melangees,
            "hasard_intra_chapitre": hasard,
        }
        print(f"      contrôles en {time.time() - t0:.1f} s", flush=True)

    # --- statistiques d'appariement ---
    types = Counter((p["n_fr"], p["n_en"]) for p in perles)
    perles_appariees = [p for p in perles if p["n_fr"] > 0 and p["n_en"] > 0]
    phrases_fr_couvertes = sum(p["n_fr"] for p in perles_appariees)
    phrases_en_couvertes = sum(p["n_en"] for p in perles_appariees)
    total_fr = sum(len(v) for v in phrases_fr.values())
    total_en = sum(len(v) for v in phrases_en.values())
    perles_sans_ancre = sum(
        1 for p in perles_appariees if not (_union_voisine(ancres_fr[p["chapitre_fr"]], p["i_fr"], p["i_fr"] + p["n_fr"]) or
                                            _union_voisine(ancres_en[p["chapitre_en"]], p["i_en"], p["i_en"] + p["n_en"]))
    )
    alignement = {
        "perles_total": len(perles),
        "perles_appariees": len(perles_appariees),
        "paires_1_1": types.get((1, 1), 0),
        "types_perles": sorted([[[di, dj], n] for (di, dj), n in types.items()], key=lambda x: (-x[1], x[0])),
        "phrases_fr": total_fr,
        "phrases_en": total_en,
        "caracteres_fr": caracteres_fr,
        "caracteres_en": caracteres_en,
        "ratio": ratio,
        "phrases_fr_couvertes": phrases_fr_couvertes,
        "phrases_en_couvertes": phrases_en_couvertes,
        "non_appariees_fr": total_fr - phrases_fr_couvertes,
        "non_appariees_en": total_en - phrases_en_couvertes,
        "phrases_fr_sans_ancre": sum(1 for n in ancres_fr for a in ancres_fr[n] if not a) / total_fr,
        "phrases_en_sans_ancre": sum(1 for n in ancres_en for a in ancres_en[n] if not a) / total_en,
        "perles_sans_ancre": perles_sans_ancre / len(perles_appariees) if perles_appariees else 0.0,
    }

    # --- verdict ---
    rappel_reel = distinct_fr["rappel"][str(args.rayon)]
    if neg["chapitres_permutes"]:
        neg_moyen = sum(b["distinctives"]["rappel"][str(args.rayon)] for b in neg["chapitres_permutes"]) / len(
            neg["chapitres_permutes"]
        )
    else:
        neg_moyen = None
    facteur = (rappel_reel / neg_moyen) if (neg_moyen is not None and neg_moyen > 0) else (
        float("inf") if neg_moyen == 0 else None
    )
    criteres = {
        "structure 37 / 37": (
            stats_fr["chapitres_retenus"] == 37 and stats_en["chapitres_retenus"] == 37,
            f"{stats_fr['chapitres_retenus']} chapitres FR et {stats_en['chapitres_retenus']} EN, numéros identiques",
        ),
        "matrice des chapitres (diagonale n° 1)": (
            matrice["diagonale_top1"] == matrice["n"],
            f"{matrice['diagonale_top1']} / {matrice['n']} chapitres ont leur homologue en première position",
        ),
        "rappel des ancres distinctives": (
            rappel_reel >= args.seuil_rappel,
            f"{_p(rappel_reel)} à ±{args.rayon} (seuil {_p(args.seuil_rappel)})",
        ),
        "contrôle négatif (chapitres permutés)": (
            neg_moyen is not None and neg_moyen <= args.seuil_controle,
            (
                f"{_p(neg_moyen)} à ±{args.rayon} (seuil {_p(args.seuil_controle)})"
                if neg_moyen is not None
                else "contrôles non exécutés"
            ),
        ),
        "facteur au-dessus du hasard": (
            facteur is not None and facteur >= args.seuil_facteur,
            f"×{_f(facteur, 1)} (seuil ×{args.seuil_facteur:.0f})" if facteur is not None else "non calculable",
        ),
    }
    valide = all(ok for ok, _ in criteres.values())
    if valide:
        resume = (
            f"les ancres distinctives se retrouvent à {_p(rappel_reel)} à ±{args.rayon}, contre "
            f"{_p(neg_moyen)} quand les chapitres sont permutés (×{facteur:.0f}) ; les 37 chapitres se "
            "correspondent par leur contenu (diagonale n° 1 partout)."
        )
    else:
        ratees = [nom for nom, (ok, _) in criteres.items() if not ok]
        resume = "critères non réunis : " + ", ".join(ratees) + "."
    verdict = {
        "valide": valide,
        "resume": resume,
        "criteres": criteres,
        "seuils": {
            "rappel_distinctif": args.seuil_rappel,
            "controle_negatif": args.seuil_controle,
            "facteur": args.seuil_facteur,
        },
    }

    validation = {
        "ancres": {
            "global": {"fr": global_fr, "en": global_en},
            "distinctives": {"fr": distinct_fr, "en": distinct_en},
            "df_fr": dict(sorted(df_fr.items(), key=lambda x: -x[1])),
            "df_en": dict(sorted(df_en.items(), key=lambda x: -x[1])),
            "liste_distinctives": sorted(distinctives),
            "seuil_distinctif": args.seuil_distinctif,
            "manques": {"global": manques_global, "distinctives": manques_distinct},
            "par_chapitre": par_chapitre,
        },
        "controles_negatifs": neg,
        "matrice_chapitres": matrice,
        "rapports_longueur": longueurs,
        "alignement": alignement,
        "verdict": verdict,
        "hypothese": {
            "appariement": "Gale-Church par chapitre, longueurs en caractères, ratio global",
            "ancres": "indépendantes de l'appariement ; utilisées seulement pour juger",
        },
    }

    meta = {
        "titre": "Le Tour du monde en quatre-vingts jours — alignement FR → EN",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "outil": "tools/aligneur_litteraire.py",
        "version": "1.0",
        "fichiers": {"fr": str(args.fr), "en": str(args.en)},
        "graine": args.graine,
        "repetitions": args.repetitions,
        "rayon": args.rayon,
        "seuil_distinctif": args.seuil_distinctif,
        "ancres": [ident for ident, _, _, _ in ANCRES],
        "duree_s": time.time() - debut,
        "ratio_global": ratio,
    }

    donnees = construire_json(
        args,
        meta,
        stats_fr,
        stats_en,
        chapitres_fr,
        chapitres_en,
        phrases_fr,
        phrases_en,
        perles,
        validation,
    )
    return donnees


def principal() -> int:
    ap = argparse.ArgumentParser(
        description="Alignement phrase à phrase vérifié par les ancres (Le Tour du monde en 80 jours)."
    )
    ap.add_argument("--fr", type=Path, default=FR_DEFAUT, help="texte français (Gutenberg)")
    ap.add_argument("--en", type=Path, default=EN_DEFAUT, help="texte anglais (Gutenberg)")
    ap.add_argument("--json", type=Path, default=JSON_DEFAUT, help="sortie JSON des paires")
    ap.add_argument("--rapport", type=Path, default=RAPPORT_DEFAUT, help="fiche de mesure markdown")
    ap.add_argument("--graine", type=int, default=20260227, help="graine des contrôles négatifs")
    ap.add_argument("--repetitions", type=int, default=3, help="répétitions des contrôles négatifs")
    ap.add_argument("--rayon", type=int, default=2, help="voisinage de validation (phrases)")
    ap.add_argument(
        "--seuil-distinctif", type=int, default=6, help="une ancre est distinctive si elle apparaît dans ≤ N chapitres"
    )
    ap.add_argument("--seuil-rappel", type=float, default=0.80, help="seuil de rappel des ancres distinctives")
    ap.add_argument("--seuil-controle", type=float, default=0.10, help="seuil du contrôle négatif")
    ap.add_argument("--seuil-facteur", type=float, default=8.0, help="facteur minimal au-dessus du contrôle")
    ap.add_argument("--sans-controles", action="store_true", help="saute les contrôles négatifs (tests rapides)")
    args = ap.parse_args()

    if not args.fr.exists() or not args.en.exists():
        print(f"[ERREUR] texte introuvable : {args.fr} ou {args.en}", file=sys.stderr)
        return 2

    donnees = analyser(args)

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(donnees, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    rediger_rapport(donnees, args.rapport)

    v = donnees["validation"]["verdict"]
    print(f"[7/7] écrit : {args.json} ({len(donnees['paires'])} paires) et {args.rapport}", flush=True)
    print(
        f"      VERDICT : {'VALIDE' if v['valide'] else 'NON VALIDE'} — {v['resume']}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
