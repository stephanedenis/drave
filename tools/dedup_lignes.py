#!/usr/bin/env python3
"""dedup_lignes.py — dédoublonner un texte **ligne à ligne**, en flux, à mémoire bornée.

POURQUOI. `reports/rapport-dedup-blocs.md` a mesuré que le dédoublonnage **par blocs** ne
retire rien sur `data/corpus_wiki_fr_texte/train.txt` (112 blocs sur 112 gardés, 0 %) : la
duplication y est courte et diffuse. La mesure exacte de ce rapport — 53,98 % des lignes
répétées pour 8,28 % des octets — désigne la **ligne** comme la bonne maille. Cet outil la
traite en **une passe**, sans jamais charger le fichier en RAM.

MÉTHODE.

1. **Lecture en flux.** `for ligne in fichier` sur un lecteur binaire : une ligne à la fois,
   tampon d'entrée fixe (4 Mio). Aucun fichier entier en RAM.
2. **Normalisation.** Par défaut, seuls les **espaces de fin** sont retirés (`bytes.rstrip()`,
   qui enlève aussi le `\\n`, le `\\r` d'un CRLF et les tabulations finales). `--normaliser`
   ajoute les **minuscules ASCII** et **compacte** les espaces : `b" ".join(ligne.split())`,
   qui réduit toute suite d'espaces blancs à un espace et rogne les bords. La ligne originale
   n'est jamais modifiée dans la sortie : on écrit **telle quelle** la première occurrence.
3. **Hachage 64 bits.** `BLAKE2b(digest_size=8)` sur la ligne normalisée. Pas de `hash()`
   de Python : il est salé par processus, donc non reproductible d'une passe à l'autre.
   Le 0 est remappé à 1 (sentinelle de case vide).
4. **Décision.** Table de hachage **exacte** à adressage ouvert linéaire (`array('Q')`,
   8 octets par case) : une ligne déjà présente est **écartée**, une ligne neuve est **gardée**
   (première occurrence) et insérée. Ce n'est pas un filtre de Bloom : il n'y a **pas de faux
   positifs** ; il reste les collisions 64 bits, négligeables (voir le rapport).
5. **Lignes vides.** Une ligne est « vide » si elle est vide **après** le retrait des espaces
   de fin. Toutes les lignes vides sont **préservées** et **jamais insérées** dans la table :
   ce sont les séparateurs de paragraphes (23,0 M de lignes sur le corpus). Une ligne faite
   uniquement d'espaces est donc préservée aussi, et comptée `lignes_vides`.
6. **Budget mémoire.** `--memoire-mo` est un **plafond**. Le modèle, explicite :

       plancher      = 48 Mio   (interpréteur, tampons d'E/S 3 × 4 Mio, journal, marge)
       octets_table  = (budget − plancher), arrondi à la puissance de 2 inférieure
       capacité      = octets_table / 8          (une case = 8 octets)
       entrées_max   = 0,8 × capacité            (charge maximale, sondage linéaire)

   Un budget inférieur au plancher + 8 Mio est refusé **au départ** :
   `ERREUR budget_memoire_impossible`, code 3. Si la table atteint `entrées_max` pendant la
   passe : `ERREUR capacite_depassee`, code 3 (il faut plus de mémoire, ou un autre outil).
   Toutes les 65 536 lignes, le chien de garde relit `ru_maxrss` et sort en
   `ERREUR memoire_depassee` (code 3) si le RSS dépasse le plafond. Le plafond est le budget,
   ou `--test-plafond-mo` (hameçon de test, masqué) pour prouver que le garde-fou sait échouer.
7. **Contrôle de sortie.** `--verifier` relit la sortie par blocs de 8 Mio et compare
   octets, lignes et sha256 aux compteurs de la passe. Une divergence est
   `ERREUR verification_echouee` (code 4), et non un succès silencieux.

CE QUE L'OUTIL NE FAIT PAS. Il ne reconnaît pas une ligne **presque** identique (un mot
changé, une casse Unicode non ASCII, un texte reflué) ; il ne déduplique pas à travers les
retours à la ligne ; il ne juge pas si une ligne répétée mérite d'être retirée (une ligne de
tableau ou de catégorie peut être utile). Il applique une définition **exacte** de la
répétition, après la normalisation choisie.

Usage :
  python3 tools/dedup_lignes.py --entree data/corpus_wiki_fr_texte/train.txt \\
      --sortie work/dedup/train-lignes.txt --memoire-mo 2048 \\
      --json reports/dedup-lignes-7.5go.json --verifier
  python3 tools/dedup_lignes.py --autotest
  python3 tools/dedup_lignes.py --entree F --sortie G --memoire-mo 8
                                   # → ERREUR budget_memoire_impossible, code 3

Codes de sortie : 0 = ok, 2 = paramètre/entrée/sortie invalide, 3 = mémoire (budget
impossible, capacité dépassée, RSS au-delà du plafond), 4 = vérification de sortie échouée.
Aucun fichier de `data/` n'est jamais écrit : une `--sortie` sous `data/` est refusée.
"""
from __future__ import annotations

import argparse
import array
import datetime as dt
import hashlib
import json
import pathlib
import resource
import struct
import subprocess
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parent.parent

MIB = 1 << 20
PLANCHER_MO = 48.0       # interpréteur + tampons + journal + marge (mesuré, voir rapport)
TAMPON_IO_MO = 4.0       # tampon du lecteur, de l'écrivain et du lot de sortie
COUT_SLOT = 8            # array('Q') : 8 octets par case
CHARGE_MAX = 0.80        # on refuse d'insérer au-delà : sondage linéaire encore court
SLOTS_MIN = 1 << 20      # table minimale : 8 Mio, 838 860 entrées à charge 0,8
CHECK_LIGNES = 1 << 16   # chien de garde : toutes les 65 536 lignes
JOURNAL_MAX = 2000       # entrées de journal conservées dans le JSON

CODES_SORTIE = {
    "memoire_depassee": 3,
    "capacite_depassee": 3,
    "budget_memoire_impossible": 3,
    "verification_echouee": 4,
    "entree_invalide": 2,
    "sortie_invalide": 2,
    "sortie_interdite": 2,
    "parametre_invalide": 2,
}


class ErreurNommee(Exception):
    """Une erreur qui porte un nom : le nom est le contrat, le message est le détail."""

    def __init__(self, nom: str, message: str):
        super().__init__(f"{nom}: {message}")
        self.nom = nom
        self.message = message


# --- briques -----------------------------------------------------------------
def rss_max_octets() -> int:
    """RSS maximal du processus (ru_maxrss est en Kio sous Linux, en octets sous macOS).

    ATTENTION : sous Linux, `ru_maxrss` est **hérité** à travers fork/exec — un enfant
    lancé depuis un parent gros (cas de l'autotest) lit le pic du parent. C'est pourquoi
    le chien de garde utilise `rss_courant_octets()` ; `ru_maxrss` reste reporté à part,
    comme mesure externe (la passe principale, lancée depuis un shell, est propre).
    """
    brut = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return brut if sys.platform == "darwin" else brut * 1024


def rss_courant_octets() -> int:
    """RSS courant (VmRSS), sans l'héritage de ru_maxrss. Repli : ru_maxrss."""
    if sys.platform.startswith("linux"):
        try:
            with open("/proc/self/status", "rb") as f:
                for ligne in f:
                    if ligne.startswith(b"VmRSS:"):
                        return int(ligne.split()[1]) * 1024
        except OSError:
            pass
    return rss_max_octets()


def est_sous(chemin: pathlib.Path, racine: pathlib.Path) -> bool:
    return chemin == racine or racine in chemin.parents


def ecrit_json(chemin: str | pathlib.Path, objet: dict) -> None:
    p = pathlib.Path(chemin)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(objet, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def modele_memoire(budget_o: int) -> dict:
    """Budget → capacité de table. Le plafond est le budget ; la table est le seul gros poste."""
    plancher_o = int(PLANCHER_MO * MIB)
    dispo = budget_o - plancher_o
    minimum = SLOTS_MIN * COUT_SLOT
    if dispo < minimum:
        raise ErreurNommee(
            "budget_memoire_impossible",
            f"budget {budget_o / MIB:.0f} Mio < plancher {PLANCHER_MO:.0f} Mio "
            f"+ {minimum / MIB:.0f} Mio (table minimale de {SLOTS_MIN} cases à "
            f"{COUT_SLOT} o) — augmentez --memoire-mo",
        )
    slots_max = dispo // COUT_SLOT
    capacite = 1 << (slots_max.bit_length() - 1)
    entrees_max = int(capacite * CHARGE_MAX)
    return {
        "budget_mio": round(budget_o / MIB, 1),
        "plancher_mio": PLANCHER_MO,
        "structure": "table de hachage exacte à adressage ouvert linéaire (array('Q'))",
        "octets_par_slot": COUT_SLOT,
        "capacite_slots": capacite,
        "octets_table": capacite * COUT_SLOT,
        "charge_max": CHARGE_MAX,
        "entrees_max": entrees_max,
    }


def verifie_sortie(chemin: pathlib.Path, octets_attendus: int,
                   lignes_attendues: int, sha_attendu: str) -> dict:
    """Relit la sortie par blocs et compare octets, lignes et sha256 aux compteurs."""
    sha = hashlib.sha256()
    octets = sauts = 0
    dernier = b""
    with open(chemin, "rb", buffering=int(TAMPON_IO_MO * MIB)) as f:
        while True:
            bloc = f.read(int(TAMPON_IO_MO * MIB))
            if not bloc:
                break
            sha.update(bloc)
            octets += len(bloc)
            sauts += bloc.count(b"\n")
            dernier = bloc[-1:]
    lignes = sauts + (1 if octets and dernier != b"\n" else 0)
    constat = {
        "methode": "relecture séquentielle par blocs de 4 Mio",
        "octets_relus": octets,
        "lignes_relues": lignes,
        "sha256_relu": sha.hexdigest(),
    }
    problemes = []
    if octets != octets_attendus:
        problemes.append(f"octets {octets} ≠ {octets_attendus}")
    if lignes != lignes_attendues:
        problemes.append(f"lignes {lignes} ≠ {lignes_attendues}")
    if sha.hexdigest() != sha_attendu:
        problemes.append("sha256 différent")
    if problemes:
        raise ErreurNommee("verification_echouee", " ; ".join(problemes))
    constat["verifie"] = True
    return constat


# --- le cœur -----------------------------------------------------------------
def execute(a, rapport: dict) -> None:
    t0 = time.perf_counter()
    entree = pathlib.Path(a.entree).resolve()
    sortie = pathlib.Path(a.sortie).resolve()

    if not entree.is_file():
        raise ErreurNommee("entree_invalide", f"{entree} n'est pas un fichier lisible")
    if entree == sortie:
        raise ErreurNommee("sortie_invalide", "l'entrée et la sortie sont le même fichier")
    if est_sous(sortie, RACINE / "data"):
        raise ErreurNommee("sortie_interdite", f"{sortie} est sous data/ (lecture seule)")
    if sortie.parent.exists() and not sortie.parent.is_dir():
        raise ErreurNommee("sortie_invalide", f"{sortie.parent} n'est pas un répertoire")
    sortie.parent.mkdir(parents=True, exist_ok=True)

    taille = entree.stat().st_size
    rapport["entree"]["octets"] = taille

    budget_o = int(a.memoire_mo * MIB)
    mem = modele_memoire(budget_o)
    plafond_o = int(a.test_plafond_mo * MIB) if a.test_plafond_mo else budget_o
    mem["plafond_test_mio"] = a.test_plafond_mo or None
    mem["plafond_mio"] = round(plafond_o / MIB, 1)
    rapport["memoire"].update(mem)

    # Une seule grosse allocation, dimensionnée par le budget. array('Q', [0]) * n alloue
    # directement n cases (pas de pic à 2 × n) ; les pages sont touchées à l'écriture.
    try:
        table = array.array("Q", [0]) * mem["capacite_slots"]
    except MemoryError as e:  # le noyau a dit non : c'est encore une erreur de budget
        raise ErreurNommee(
            "memoire_depassee",
            f"allocation de {mem['octets_table'] / MIB:.0f} Mio refusée par le noyau ({e})",
        ) from e

    hach = hashlib.blake2b
    unpack = struct.unpack_from
    tab = table
    masque = mem["capacite_slots"] - 1
    entrees_max = mem["entrees_max"]
    normaliser = a.normaliser
    tampon_o = int(TAMPON_IO_MO * MIB)

    lignes_lues = lignes_gardees = lignes_ecartees = 0
    lignes_vides = 0
    octets_lus = octets_gardes = octets_ecartes = octets_vides = 0
    premiere_vide_octets = None
    plus_longue = 0
    slots_utilises = 0
    rss_max = 0
    rss_ru = 0
    journal: list[dict] = []
    prochain_check = CHECK_LIGNES
    prochain_journal = t0 + 10.0
    sha = hashlib.sha256()
    tampon = bytearray()

    f_in = open(entree, "rb", buffering=tampon_o)
    try:
        f_out = open(sortie, "wb", buffering=tampon_o)
    except OSError:
        f_in.close()
        raise

    # Le chien de garde vaut aussi pour l'allocation : un plafond de test de 1 Mio doit
    # échouer tout de suite, sans attendre la première ligne. On mesure le VmRSS courant,
    # pas ru_maxrss : ce dernier est hérité à travers fork/exec (cf. rss_max_octets).
    rss_max = rss_courant_octets()
    rss_ru = rss_max_octets()
    if rss_max > plafond_o:
        f_in.close()
        f_out.close()
        raise ErreurNommee(
            "memoire_depassee",
            f"RSS max {rss_max / MIB:.0f} Mio > plafond {plafond_o / MIB:.0f} Mio "
            f"après allocation de la table",
        )

    try:
        for ligne in f_in:
            lignes_lues += 1
            n = len(ligne)
            octets_lus += n
            if n > plus_longue:
                plus_longue = n

            if normaliser:
                contenu = b" ".join(ligne.split()).lower()
            else:
                contenu = ligne.rstrip()

            if not contenu:
                # Séparateur de paragraphe : toujours écrit, jamais haché ni inséré.
                lignes_vides += 1
                octets_vides += n
                if premiere_vide_octets is None:
                    premiere_vide_octets = n
                garder = True
            else:
                h = unpack("<Q", hach(contenu, digest_size=8).digest())[0] or 1
                i = h & masque
                garder = True
                while True:
                    v = tab[i]
                    if v == h:
                        garder = False
                        break
                    if v == 0:
                        if slots_utilises >= entrees_max:
                            raise ErreurNommee(
                                "capacite_depassee",
                                f"{slots_utilises} lignes uniques > entrées max "
                                f"{entrees_max} (table {mem['capacite_slots']} cases, "
                                f"charge max {CHARGE_MAX}) à la ligne {lignes_lues} — "
                                f"augmentez --memoire-mo",
                            )
                        tab[i] = h
                        slots_utilises += 1
                        break
                    i = (i + 1) & masque
                if not garder:
                    lignes_ecartees += 1
                    octets_ecartes += n

            if garder:
                tampon += ligne
                lignes_gardees += 1
                octets_gardes += n
                if len(tampon) >= tampon_o:
                    f_out.write(tampon)
                    sha.update(tampon)
                    tampon.clear()

            if lignes_lues >= prochain_check:
                prochain_check += CHECK_LIGNES
                rss_max = max(rss_max, rss_courant_octets())
                rss_ru = max(rss_ru, rss_max_octets())
                if rss_max > plafond_o:
                    raise ErreurNommee(
                        "memoire_depassee",
                        f"RSS max {rss_max / MIB:.0f} Mio > plafond "
                        f"{plafond_o / MIB:.0f} Mio à la ligne {lignes_lues}",
                    )
                maintenant = time.perf_counter()
                if maintenant >= prochain_journal and len(journal) < JOURNAL_MAX:
                    prochain_journal = maintenant + 10.0
                    entree_journal = {
                        "lignes_lues": lignes_lues,
                        "pct_lignes_ecartees": round(100 * lignes_ecartees / lignes_lues, 2),
                        "rss_mio": round(rss_max / MIB, 1),
                        "s": round(maintenant - t0, 1),
                    }
                    journal.append(entree_journal)
                    print(
                        f"[{lignes_lues:>12,} lignes] "
                        f"{entree_journal['pct_lignes_ecartees']:5.2f} % écartées, "
                        f"RSS {entree_journal['rss_mio']:7.1f} Mio, "
                        f"{entree_journal['s']:6.1f} s",
                        file=sys.stderr, flush=True,
                    )

        if tampon:
            f_out.write(tampon)
            sha.update(tampon)
            tampon.clear()
    finally:
        f_in.close()
        f_out.close()

    duree_passe = time.perf_counter() - t0
    rss_max = max(rss_max, rss_courant_octets())
    rss_ru = max(rss_ru, rss_max_octets())
    if rss_max > plafond_o:
        raise ErreurNommee(
            "memoire_depassee",
            f"RSS max {rss_max / MIB:.0f} Mio > plafond {plafond_o / MIB:.0f} Mio "
            f"en fin de passe",
        )

    sha_hex = sha.hexdigest()
    lignes_non_vides = lignes_lues - lignes_vides
    lignes_non_vides_gardees = lignes_gardees - lignes_vides
    # Ce que donnerait la même passe si les lignes vides étaient dédoublonnées comme dans
    # le diagnostic exact (toutes sauf la première) : directement comparable aux 53,98 %.
    vides_ecartees_equiv = max(0, lignes_vides - 1)
    octets_vides_ecartes_equiv = max(0, octets_vides - (premiere_vide_octets or 0))
    lignes_equiv = lignes_ecartees + vides_ecartees_equiv
    octets_equiv = octets_ecartes + octets_vides_ecartes_equiv

    rapport["sortie"].update({
        "octets": octets_gardes,
        "sha256": sha_hex,
        "lignes": lignes_gardees,
    })
    rapport["lignes"] = {
        "lues": lignes_lues,
        "gardees": lignes_gardees,
        "ecartees": lignes_ecartees,
        "vides_lues": lignes_vides,
        "vides_gardees": lignes_vides,
        "non_vides_lues": lignes_non_vides,
        "non_vides_gardees": lignes_non_vides_gardees,
        "non_vides_ecartees": lignes_ecartees,
        "plus_longue_ligne_octets": plus_longue,
    }
    rapport["octets"] = {
        "entree": octets_lus,
        "sortie": octets_gardes,
        "gardes": octets_gardes,
        "ecartes": octets_ecartes,
        "vides_gardes": octets_vides,
        "non_vides_entree": octets_lus - octets_vides,
        "non_vides_sortie": octets_gardes - octets_vides,
    }
    rapport["taux"] = {
        "pct_lignes_ecartees": round(100 * lignes_ecartees / lignes_lues, 3)
        if lignes_lues else 0.0,
        "pct_lignes_ecartees_hors_vides": round(
            100 * lignes_ecartees / lignes_non_vides, 3) if lignes_non_vides else 0.0,
        "pct_octets_ecartes": round(100 * octets_ecartes / octets_lus, 3)
        if octets_lus else 0.0,
        "pct_octets_vides": round(100 * octets_vides / octets_lus, 3)
        if octets_lus else 0.0,
        "pct_lignes_gardees": round(100 * lignes_gardees / lignes_lues, 3)
        if lignes_lues else 0.0,
        "pct_lignes_vides": round(100 * lignes_vides / lignes_lues, 3)
        if lignes_lues else 0.0,
        "pct_sortie": round(100 * octets_gardes / octets_lus, 3) if octets_lus else 0.0,
    }
    rapport["table"] = {
        "slots_utilises": slots_utilises,
        "charge_finale": round(slots_utilises / mem["capacite_slots"], 4),
        "entrees_max": entrees_max,
    }
    rapport["memoire"].update({
        "rss_max_mio": round(rss_max / MIB, 1),
        "rss_max_source": "maximum de VmRSS (/proc/self/status), échantillonné après "
                          "allocation puis toutes les 65 536 lignes",
        "ru_maxrss_mio": round(rss_ru / MIB, 1),
        "marge_mio": round((budget_o - rss_max) / MIB, 1),
        "marge_ru_maxrss_mio": round((budget_o - rss_ru) / MIB, 1),
        "plafond_atteint": False,
    })
    rapport["integrite"] = {
        "sha256_sortie": sha_hex,
        "octets": octets_gardes,
        "lignes": lignes_gardees,
        "verifie": False,
    }
    rapport["duree_s"] = None  # rempli après l'éventuelle vérification de sortie
    rapport["debit_mio_s"] = None
    rapport["journal"] = journal
    rapport["journal_tronque"] = len(journal) >= JOURNAL_MAX
    # Contrôle interne : la somme des longueurs lues doit être la taille du fichier.
    rapport["integrite_lecture"] = {
        "octets_lus": octets_lus,
        "octets_stat": taille,
        "coherent": octets_lus == taille,
    }

    if a.verifier:
        rapport["integrite"].update(
            verifie_sortie(sortie, octets_gardes, lignes_gardees, sha_hex))

    duree = time.perf_counter() - t0
    rapport["duree_s"] = round(duree, 1)
    rapport["duree_passe_s"] = round(duree_passe, 1)
    rapport["duree_verification_s"] = round(duree - duree_passe, 1) if a.verifier else 0.0
    rapport["debit_mio_s"] = round((taille / MIB) / duree_passe, 1) if duree_passe else None
    rapport["debit_total_mio_s"] = round((taille / MIB) / duree, 1) if duree else None

    # Comparaison directe avec le diagnostic exact du rapport blocs (§ 4.3).
    rapport["comparaison_blocs"] = {
        "source": "reports/rapport-dedup-blocs.md § 4.3 (mesure exacte, 2026-11-18)",
        "lignes_dupliquees_pct_diagnostic": 53.98,
        "octets_dupliques_pct_diagnostic": 8.28,
        "lignes_vides_diagnostic": 23037969,
        "note": "le diagnostic supprimait toutes les lignes vides sauf une ; ici toutes "
                "sont préservées, d'où deux taux : effectif (vides gardées) et équivalent "
                "(vides dédoublonnées comme le diagnostic)",
        "mesure_equivalente": {
            "lignes_ecartees": lignes_equiv,
            "pct_lignes_ecartees": round(100 * lignes_equiv / lignes_lues, 3)
            if lignes_lues else 0.0,
            "octets_ecartes": octets_equiv,
            "pct_octets_ecartes": round(100 * octets_equiv / octets_lus, 3)
            if octets_lus else 0.0,
        },
    }
    rapport["verdict"] = "ok"


# --- manifeste ---------------------------------------------------------------
def squelette(a) -> dict:
    return {
        "outil": "tools/dedup_lignes.py",
        "date": dt.datetime.now().isoformat(timespec="seconds"),
        "verdict": None,
        "entree": {
            "chemin": str(pathlib.Path(a.entree).resolve()) if a.entree else None,
            "octets": None,
            "mtime": None,
        },
        "sortie": {
            "chemin": str(pathlib.Path(a.sortie).resolve()) if a.sortie else None,
            "octets": 0, "sha256": None, "lignes": 0,
        },
        "parametres": {
            "memoire_mo": a.memoire_mo,
            "normaliser": bool(a.normaliser),
            "hachage": "BLAKE2b-64 (digest_size=8, non salé)",
            "lecture": "flux ligne à ligne, tampon 4 Mio",
            "verifier": bool(a.verifier),
        },
        "memoire": {},
        "table": {},
        "lignes": {},
        "octets": {},
        "taux": {},
        "integrite": {},
        "comparaison_blocs": {},
        "duree_s": None,
        "duree_passe_s": None,
        "duree_verification_s": None,
        "debit_mio_s": None,
        "debit_total_mio_s": None,
        "journal": [],
        "journal_tronque": False,
    }


# --- contrôle négatif --------------------------------------------------------
# Une ligne par cas ; les indices sont utilisés pour construire la sortie attendue.
LIGNES_CONTROLE = [
    b"ligne unique alpha   \n",     # 0 : première occurrence, espaces de fin conservés
    b"ligne unique alpha\n",        # 1 : copie exacte après rstrip → écartée
    b"ligne unique alpha   \n",     # 2 : copie exacte → écartée
    b"ligne differente beta\n",     # 3 : ligne différente → gardée
    b"\n",                          # 4 : vide → préservée
    b"\n",                          # 5 : vide → préservée
    b"   \n",                       # 6 : vide après rstrip → préservée (et comptée vide)
    b"Bonjour le Monde\n",          # 7 : gardée par défaut ; gardée si --normaliser
    b"bonjour le monde\n",          # 8 : gardée par défaut ; écartée si --normaliser
    b"espaces   internes\n",        # 9 : gardée par défaut
    b"espaces internes\n",          # 10 : gardée par défaut ; écartée si --normaliser
    b"\n",                          # 11 : vide → préservée
]
GARDES_DEFAUT = [0, 3, 4, 5, 6, 7, 8, 9, 10, 11]
GARDES_NORMALISE = [0, 3, 4, 5, 6, 7, 9, 11]


def lance_autotest(repertoire: pathlib.Path) -> tuple[bool, dict]:
    repertoire = repertoire.resolve()
    if est_sous(repertoire, RACINE / "data"):
        raise ErreurNommee("sortie_interdite", f"{repertoire} est sous data/ (lecture seule)")
    repertoire.mkdir(parents=True, exist_ok=True)
    outil = str(pathlib.Path(__file__).resolve())

    controle = repertoire / "controle.txt"
    controle.write_bytes(b"".join(LIGNES_CONTROLE))
    attendu_defaut = b"".join(LIGNES_CONTROLE[i] for i in GARDES_DEFAUT)
    attendu_normalise = b"".join(LIGNES_CONTROLE[i] for i in GARDES_NORMALISE)
    n_vides = sum(1 for ligne in LIGNES_CONTROLE if not ligne.rstrip())

    def lance(nom: str, args: list[str]) -> tuple[int, dict, str]:
        json_path = repertoire / f"{nom}.json"
        cmd = [sys.executable, outil, *args, "--json", str(json_path)]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        manifeste = json.loads(json_path.read_text()) if json_path.exists() else {}
        return p.returncode, manifeste, (p.stderr or "") + (p.stdout or "")

    cas: list[dict] = []

    def verifie(nom: str, condition: bool, detail) -> None:
        cas.append({"nom": nom, "ok": bool(condition), "detail": detail})

    def lance_controle(nom: str, sortie: str, *extra: str) -> tuple[int, dict, bytes]:
        rc, r, log = lance(nom, ["--entree", str(controle), "--sortie", str(repertoire / sortie),
                                 "--memoire-mo", "64", *extra])
        chemin = repertoire / sortie
        return rc, r, (chemin.read_bytes() if chemin.exists() else b"")

    # Passe de référence, sans normalisation.
    rc1, r1, sortie1 = lance_controle("defaut", "defaut.txt")
    verifie("a_ligne_unique_gardee",
            rc1 == 0 and r1.get("lignes", {}).get("non_vides_gardees") == 6,
            {"rc": rc1, "non_vides_gardees": r1.get("lignes", {}).get("non_vides_gardees")})
    verifie("b_copie_exacte_ecartee",
            r1.get("lignes", {}).get("ecartees") == 2,
            {"ecartees": r1.get("lignes", {}).get("ecartees"), "attendu": 2})
    # (b) et (c) séparément, sur deux fichiers de deux lignes : une copie exacte, une copie
    # qui ne diffère que par les espaces de fin. Chacune doit laisser la première occurrence.
    fichier_b = repertoire / "copie-exacte.txt"
    fichier_b.write_bytes(LIGNES_CONTROLE[0] + LIGNES_CONTROLE[2])
    rc_b, r_b, _ = lance("copie_exacte", [
        "--entree", str(fichier_b), "--sortie", str(repertoire / "copie-exacte-sortie.txt"),
        "--memoire-mo", "64"])
    sortie_b = (repertoire / "copie-exacte-sortie.txt").read_bytes()
    verifie("b_copie_exacte_seule_ecartee",
            rc_b == 0 and r_b.get("lignes", {}).get("ecartees") == 1
            and sortie_b == LIGNES_CONTROLE[0],
            {"rc": rc_b, "ecartees": r_b.get("lignes", {}).get("ecartees"),
             "sortie_identique": sortie_b == LIGNES_CONTROLE[0]})
    fichier_c = repertoire / "copie-espaces.txt"
    fichier_c.write_bytes(LIGNES_CONTROLE[0] + LIGNES_CONTROLE[1])
    rc_c, r_c, _ = lance("copie_espaces", [
        "--entree", str(fichier_c), "--sortie", str(repertoire / "copie-espaces-sortie.txt"),
        "--memoire-mo", "64"])
    sortie_c = (repertoire / "copie-espaces-sortie.txt").read_bytes()
    verifie("c_espaces_de_fin_seuls_ecartes",
            rc_c == 0 and r_c.get("lignes", {}).get("ecartees") == 1
            and sortie_c == LIGNES_CONTROLE[0],
            {"rc": rc_c, "ecartees": r_c.get("lignes", {}).get("ecartees"),
             "sortie_identique": sortie_c == LIGNES_CONTROLE[0]})
    verifie("c_espaces_de_fin_ecartes_par_defaut", sortie1 == attendu_defaut,
            {"sortie_octets": len(sortie1), "attendu_octets": len(attendu_defaut),
             "identique": sortie1 == attendu_defaut})
    verifie("c_premiere_occurrence_telle_quelle",
            sortie1.startswith(b"ligne unique alpha   \n"),
            {"prefixe": sortie1[:24].decode("utf-8", "replace")})
    verifie("d_ligne_differente_gardee",
            b"ligne differente beta\n" in sortie1,
            {"presente": b"ligne differente beta\n" in sortie1})
    verifie("e_lignes_vides_preservees",
            r1.get("lignes", {}).get("vides_lues") == n_vides
            and sortie1.count(b"\n") == len(GARDES_DEFAUT),
            {"vides_attendues": n_vides, "vides_json": r1.get("lignes", {}).get("vides_lues"),
             "lignes_sortie": sortie1.count(b"\n")})
    verifie("e_ligne_espaces_preservee", b"   \n" in sortie1,
            {"presente": b"   \n" in sortie1})

    # Stabilité : deux passes identiques → même sha256 et même sortie.
    rc1b, r1b, sortie1b = lance_controle("defaut_bis", "defaut-bis.txt")
    verifie("f_deux_passes_meme_sha256",
            r1.get("sortie", {}).get("sha256") == r1b.get("sortie", {}).get("sha256")
            and sortie1 == sortie1b,
            {"sha1": r1.get("sortie", {}).get("sha256"),
             "sha2": r1b.get("sortie", {}).get("sha256"),
             "sorties_identiques": sortie1 == sortie1b})

    # --normaliser : minuscules + espaces compactés → trois copies de plus écartées.
    rc2, r2, sortie2 = lance_controle("normalise", "normalise.txt", "--normaliser")
    verifie("normaliser_ecarte_minuscules_et_espaces",
            rc2 == 0 and r2.get("lignes", {}).get("ecartees") == 4
            and sortie2 == attendu_normalise,
            {"rc": rc2, "ecartees": r2.get("lignes", {}).get("ecartees"),
             "attendu": 4, "identique": sortie2 == attendu_normalise})
    rc2b, r2b, _ = lance_controle("normalise_bis", "normalise-bis.txt", "--normaliser")
    verifie("normaliser_stable",
            r2.get("sortie", {}).get("sha256") == r2b.get("sortie", {}).get("sha256"),
            {"sha1": r2.get("sortie", {}).get("sha256"),
             "sha2": r2b.get("sortie", {}).get("sha256")})

    # Budget impossible : refus au départ, nommé, code 3.
    rc3, r3, log3 = lance("budget_impossible", [
        "--entree", str(controle), "--sortie", str(repertoire / "jamais.txt"),
        "--memoire-mo", "8"])
    verifie("budget_impossible_nomme",
            rc3 == 3 and r3.get("erreur", {}).get("nom") == "budget_memoire_impossible",
            {"rc": rc3, "erreur": r3.get("erreur"),
             "stderr": log3.strip().splitlines()[-1:]})

    # Capacité dépassée : 850 000 lignes uniques dans une table de 2^20 cases (838 860
    # entrées max à charge 0,8) → erreur nommée, pas une corruption silencieuse.
    grosses = repertoire / "grosses.txt"
    with open(grosses, "wb", buffering=int(TAMPON_IO_MO * MIB)) as f:
        for debut in range(0, 850_000, 20_000):
            f.write(b"".join(
                b"ligne unique %08d\n" % i
                for i in range(debut, min(debut + 20_000, 850_000))))
    rc4, r4, log4 = lance("capacite_depassee", [
        "--entree", str(grosses), "--sortie", str(repertoire / "grosses-sortie.txt"),
        "--memoire-mo", "56"])
    verifie("capacite_depassee_nommee",
            rc4 == 3 and r4.get("erreur", {}).get("nom") == "capacite_depassee",
            {"rc": rc4, "erreur": r4.get("erreur"),
             "stderr": log4.strip().splitlines()[-1:]})

    # Chien de garde : plafond de test de 1 Mio → memoire_depassee dès l'allocation.
    rc5, r5, log5 = lance("chien_de_garde", [
        "--entree", str(controle), "--sortie", str(repertoire / "partiel.txt"),
        "--memoire-mo", "64", "--test-plafond-mo", "1"])
    verifie("chien_de_garde_memoire_depassee",
            rc5 == 3 and r5.get("erreur", {}).get("nom") == "memoire_depassee",
            {"rc": rc5, "erreur": r5.get("erreur")})

    # Vérification de sortie : le chemin heureux doit dire « vérifié ».
    rc6, r6, _ = lance("verifie", [
        "--entree", str(controle), "--sortie", str(repertoire / "verifie.txt"),
        "--memoire-mo", "64", "--verifier"])
    verifie("verification_sortie_ok",
            rc6 == 0 and r6.get("integrite", {}).get("verifie") is True,
            {"rc": rc6, "integrite": r6.get("integrite")})

    resume = {
        "ok": all(c["ok"] for c in cas),
        "outil": "tools/dedup_lignes.py",
        "controle": {
            "chemin": str(controle),
            "lignes": len(LIGNES_CONTROLE),
            "octets": controle.stat().st_size,
            "vides": n_vides,
        },
        "attendu": {
            "defaut_octets": len(attendu_defaut),
            "normalise_octets": len(attendu_normalise),
        },
        "cas": cas,
        "passe_defaut": r1,
        "passe_normalisee": r2,
    }
    ecrit_json(repertoire / "autotest.json", resume)
    return resume["ok"], resume


# --- CLI ---------------------------------------------------------------------
def parse(argv=None):
    ap = argparse.ArgumentParser(
        description="Dédoublonner un fichier texte ligne à ligne, en flux, à mémoire bornée.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--entree", help="fichier texte à dédupliquer (lecture seule)")
    ap.add_argument("--sortie", help="fichier de sortie (lignes gardées, telles quelles)")
    ap.add_argument("--memoire-mo", dest="memoire_mo", type=float, default=2048.0,
                    help="plafond mémoire en Mio (défaut 2048)")
    ap.add_argument("--normaliser", action="store_true",
                    help="minuscules ASCII + espaces compactés (en plus du retrait des "
                         "espaces de fin)")
    ap.add_argument("--json", default=None, help="manifeste JSON de la passe")
    ap.add_argument("--verifier", action="store_true",
                    help="relire la sortie et vérifier octets, lignes et sha256")
    ap.add_argument("--autotest", action="store_true", help="contrôle négatif reproductible")
    ap.add_argument("--repertoire", default=str(RACINE / "work/dedup/autotest-lignes"),
                    help="répertoire de l'autotest")
    ap.add_argument("--test-plafond-mo", dest="test_plafond_mo", type=float, default=0.0,
                    help=argparse.SUPPRESS)  # hameçon de test du chien de garde
    a = ap.parse_args(argv)
    if not a.autotest and (not a.entree or not a.sortie):
        ap.error("--entree et --sortie sont requis (ou --autotest)")
    return a


def valide(a) -> None:
    if a.memoire_mo <= 0:
        raise ErreurNommee("parametre_invalide", "--memoire-mo doit être > 0")
    if a.test_plafond_mo < 0:
        raise ErreurNommee("parametre_invalide", "--test-plafond-mo doit être ≥ 0")


def main(argv=None) -> int:
    a = parse(argv)
    if a.autotest:
        try:
            ok, resume = lance_autotest(pathlib.Path(a.repertoire))
        except ErreurNommee as e:
            print(f"ERREUR {e.nom}: {e.message}", file=sys.stderr)
            return CODES_SORTIE.get(e.nom, 1)
        print(json.dumps(resume, ensure_ascii=False, indent=1))
        return 0 if ok else 1

    rapport = squelette(a)
    t_debut = time.perf_counter()
    try:
        valide(a)
        entree = pathlib.Path(a.entree)
        if entree.is_file():
            st = entree.stat()
            rapport["entree"].update({
                "octets": st.st_size,
                "mtime": dt.datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
            })
        execute(a, rapport)
    except ErreurNommee as e:
        rapport["verdict"] = "erreur"
        rapport["erreur"] = {"nom": e.nom, "message": e.message}
        rapport["duree_s"] = round(time.perf_counter() - t_debut, 1)
        if a.json:
            ecrit_json(a.json, rapport)
        print(f"ERREUR {e.nom}: {e.message}", file=sys.stderr)
        return CODES_SORTIE.get(e.nom, 1)
    except KeyboardInterrupt:
        print("interrompu", file=sys.stderr)
        return 130

    if a.json:
        ecrit_json(a.json, rapport)
    print(json.dumps({
        "entree_octets": rapport["entree"]["octets"],
        "sortie_octets": rapport["sortie"]["octets"],
        "lignes_lues": rapport["lignes"]["lues"],
        "lignes_gardees": rapport["lignes"]["gardees"],
        "lignes_ecartees": rapport["lignes"]["ecartees"],
        "pct_lignes_ecartees": rapport["taux"]["pct_lignes_ecartees"],
        "pct_octets_ecartes": rapport["taux"]["pct_octets_ecartes"],
        "duree_s": rapport["duree_s"],
        "duree_passe_s": rapport["duree_passe_s"],
        "rss_max_mio": rapport["memoire"].get("rss_max_mio"),
        "sha256": rapport["sortie"]["sha256"],
    }, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
