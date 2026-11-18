#!/usr/bin/env python3
"""dedup_blocs.py — dédoublonner du texte par blocs, à mémoire bornée.

POURQUOI. `tools/corpus_propre.py` garde **tous** les shingles en mémoire (≈ 80 Go par Go
de texte, cf. `reports/rapport-n2-corpus-1go.md`) : dédupliquer les 7,50 Go de
`data/corpus_wiki_fr_texte/train.txt` demanderait ≈ 600 Go de RAM pour 125 Go installés.
Ici, la mémoire est **bornée par construction** : on lit le fichier en blocs, on décide
bloc par bloc, et le jeu des shingles « déjà vus » est **échantillonné** à un taux dérivé
du budget (`--memoire-mo`).

MÉTHODE.

1. **Découpe.** Blocs de `--bloc-mo` Mio, coupés au dernier saut de ligne (aucune ligne
   n'est coupée), plus une marge de contexte **après** le bloc (2 % du bloc, au plus
   1 Mio, ou `--recouvrement-mo`) : elle sert à terminer les fenêtres qui commencent dans
   les derniers octets du bloc. Le **cœur** est ce qui sera écrit.
2. **Normalisation.** Minuscules ASCII (`bytes.lower`) et espaces horizontaux réduits
   (`[ \\t\\r\\f\\v]+` → un espace). Les **sauts de ligne sont conservés** : c'est ce qui
   permet l'ancrage ci-dessous.
3. **Ancrage des shingles (le point clé).** Un shingle est une fenêtre de `--shingle`
   octets (96), hachée **BLAKE2b** — 64 bits par défaut, 32 bits en option. Les fenêtres
   sont prises à des positions **définies par le contenu** : le début de chaque ligne,
   puis tous les `--pas` octets à l'intérieur de la ligne. Une copie du texte, même
   insérée à un décalage quelconque, produit donc **les mêmes ancres** — et les mêmes
   hachages. Une grille à pas fixe ancrée sur les offsets du fichier ne le ferait pas :
   une copie décalée de d octets ne partagerait une fenêtre que si d ≡ 0 (mod pas), soit
   1 chance sur pas (mesuré : 0,01 % de shingles vus à pas 96 contre 0,24 % avec
   l'ancrage, sur 20 Mo — voir `work/dedup/diagnostic_ancrage.py`). Les hachages sont
   échantillonnés par `h & masque == 0`, condition elle aussi définie par le contenu :
   une copie est donc échantillonnée exactement comme son original.
4. **Décision.** Un bloc dont **≥ `--seuil`** de ses shingles échantillonnés sont déjà
   dans l'ensemble est **écarté** ; sinon il est **gardé** (ses octets sont écrits) et ses
   shingles sont insérés. L'insertion a lieu **après** la décision : les répétitions
   internes à un bloc ne comptent pas comme « déjà vu ». Les shingles d'un bloc écarté
   sont quand même insérés (une 3ᵉ copie doit être écartée même si la 2ᵉ ne l'a pas été).
5. **Budget mémoire.** Le taux d'échantillonnage `p` et la capacité du jeu sont calculés
   **avant** la lecture, à partir du budget, de la taille du fichier et du coût mesuré
   d'une entrée de `set` :

       plancher  = 4 × (bloc + recouvrement) + 32 Mio + 48 Mio   (copies + interpréteur)
       capacité  = (budget − plancher) / coût_mesuré_d_une_entrée
       p         = plus grande puissance de 2 ≤ 0,5 × capacité / (1,5 × octets / pas)

   Le 1,5 compte les ancres de début de ligne, qui s'ajoutent à celles du pas. Le facteur
   0,5 est une marge : le `set` de CPython double sa table en grandissant (pic ≈ 1,5 × la
   table finale), et le coût mesuré (80 o par entrée) inclut ce pic. À chaque bloc, le
   chien de garde relit `resource.getrusage(RUSAGE_SELF).ru_maxrss` et **sort en erreur
   nommée** si le RSS dépasse le budget (`ERREUR memoire_depassee`, code 3) ; idem si le
   jeu dépasse la capacité (`capacite_depassee`). Un budget inférieur au plancher est
   refusé au départ (`budget_memoire_impossible`).

CE QUE L'OUTIL N'EST PAS. Ce n'est pas un dédoublonnage au sens de `corpus_propre.py` :
la décision est **par bloc**, donc un bloc n'est écarté que si *son* contenu est
majoritairement déjà vu. Une répétition dispersée (quelques pour cent répartis sur tout
le fichier) ne fait tomber aucun bloc de 64 Mio sous le seuil : elle est **mesurée**
(taux de shingles déjà vus) mais **pas retirée**. Le seuil et la taille de bloc décident
donc de ce qui est retiré, pas seulement le taux de duplication.

Usage :
  python3 tools/dedup_blocs.py --entree data/corpus_wiki_fr_texte/train.txt \\
      --sortie work/dedup/train.txt --bloc-mo 64 --memoire-mo 2048 \\
      --json reports/dedup-blocs-7.5go.json
  python3 tools/dedup_blocs.py --autotest          # contrôle négatif reproductible
  python3 tools/dedup_blocs.py --entree F --sortie G --memoire-mo 64 --bloc-mo 64
                                                   # → ERREUR budget_memoire_impossible

Codes de sortie : 0 = ok, 2 = paramètre/entrée invalide, 3 = mémoire (budget dépassé ou
impossible). Aucun fichier de `data/` n'est jamais écrit : `--sortie` y est refusé.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import pathlib
import random
import re
import resource
import struct
import subprocess
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parent.parent
HBLANC = re.compile(rb"[ \t\r\f\v]{2,}")   # suites de 2+ espaces ; les \n restent
#                                                              (un espace seul est déjà normalisé et ne doit pas
#                                                               allouer : re.sub garde toutes les occurrences)
MOT = re.compile(r"[0-9A-Za-zÀ-ÖØ-öø-ÿ']+")

# --- modèle de mémoire (voir docstring) --------------------------------------
FACTEUR_BLOC = 4.0        # copies transitoires d'un bloc : tampon, brut, normalisé, concaténé
DIVERS_BLOC_MO = 32.0     # listes d'ancres, tampons de lecture, sortie
PLANCHER_MO = 48.0        # interpréteur, I/O, divers hors bloc
MARGE_CAPACITE = 0.5      # on ne vise que la moitié de la capacité estimée du set
ECHANTILLON_MIN = 1 << 20  # taux minimal 1/1 048 576, en dessous : erreur nommée
LONGUEUR_MIN_BLOC = 8     # un bloc vaut au moins 8 shingles
JOURNAL_MAX = 2000        # entrées de journal conservées dans le JSON
COUT_ENTREE_OCTETS = 80.0  # octets par entrée de set (mesuré, voir cout_entree())

CODES_SORTIE = {
    "memoire_depassee": 3,
    "capacite_depassee": 3,
    "budget_memoire_impossible": 3,
    "echantillon_trop_faible": 3,
    "entree_invalide": 2,
    "sortie_invalide": 2,
    "sortie_interdite": 2,
    "parametre_invalide": 2,
}

MIB = 1 << 20


class ErreurNommee(Exception):
    """Une erreur qui porte un nom : le nom est le contrat, le message est le détail."""

    def __init__(self, nom: str, message: str):
        super().__init__(f"{nom}: {message}")
        self.nom = nom
        self.message = message


# --- briques -----------------------------------------------------------------
def normalise(bloc: bytes) -> bytes:
    """Minuscules ASCII + suites d'espaces horizontaux réduites. Les sauts de ligne restent.

    Le motif exige **2 espaces ou plus** : `[ \t\r\f\v]+` matcherait chaque espace
    simple et `re.sub` garderait une entrée par occurrence (33 Mio de pic pour 1 Mio de
    texte, mesuré) — `{2,}` ne coûte rien sur de la prose, où les espaces sont simples.
    """
    return HBLANC.sub(b" ", bloc.lower())


def melange(x: int) -> int:
    """splitmix64 : une graine entière → 64 bits bien répartis, sans état."""
    x = (x + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
    x = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
    x = ((x ^ (x >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
    return x ^ (x >> 31)


def hacheur(bits: int, graine: int):
    """Renvoie (fonction de hachage d'une fenêtre, décalage de graine)."""
    if bits == 64:
        def h(w: bytes) -> int:
            return struct.unpack("<Q", hashlib.blake2b(w, digest_size=8).digest())[0]
    else:
        def h(w: bytes) -> int:
            return struct.unpack("<I", hashlib.blake2b(w, digest_size=4).digest())[0]
    return h, melange(graine) & ((1 << bits) - 1)


def cout_entree() -> dict:
    """Coût d'une entrée de `set`, mesuré sur cette machine le 2026-11-18.

    Un `set` de 10 000 000 d'entiers 64 bits distincts atteint `ru_maxrss` = 757 Mio,
    soit **79,4 octets par entrée** : table de 26,8 o/entrée (16 o par case, charge 0,6),
    entier de 28 o, pic du dernier doublement de table et arènes du tas comprises. Les
    petits `set` coûtent bien plus par entrée (table minimale) : calibrer à 20 000
    donnerait 105 o/entrée et gaspillerait un facteur 4 — d'où la constante mesurée,
    avec une marge (on plafonne le jeu à la moitié de la capacité calculée).
    """
    return {"cout_entree_octets": COUT_ENTREE_OCTETS,
            "source": "mesure 2026-11-18 : set de 10 M d'entiers 64 bits = 757 Mio "
                      "de ru_maxrss, soit 79,4 o/entrée"}


def rss_max_octets() -> int:
    """RSS maximal du processus (ru_maxrss est en Kio sous Linux, en octets sous macOS)."""
    brut = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return brut if sys.platform == "darwin" else brut * 1024


def est_sous(chemin: pathlib.Path, racine: pathlib.Path) -> bool:
    return chemin == racine or racine in chemin.parents


def ecrit_json(chemin: str | pathlib.Path, objet: dict) -> None:
    p = pathlib.Path(chemin)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(objet, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def parametres_json(a) -> dict:
    return {
        "bloc_mo": a.bloc_mo,
        "memoire_mo": a.memoire_mo,
        "shingle_octets": a.shingle,
        "pas": a.pas,
        "seuil": a.seuil,
        "hash_bits": a.hash_bits,
        "graine": a.graine,
        "recouvrement_mo": a.recouvrement_mo,
    }


def valide(a) -> None:
    if not (0.0 <= a.seuil <= 1.0):
        raise ErreurNommee("parametre_invalide", f"--seuil {a.seuil} hors de [0, 1]")
    if a.shingle < 8:
        raise ErreurNommee("parametre_invalide", f"--shingle {a.shingle} < 8 octets")
    if a.pas < 1:
        raise ErreurNommee("parametre_invalide", f"--pas {a.pas} < 1")
    if a.bloc_mo <= 0 or a.memoire_mo <= 0:
        raise ErreurNommee("parametre_invalide", "les tailles doivent être positives")
    if a.hash_bits not in (32, 64):
        raise ErreurNommee("parametre_invalide", f"--hash-bits {a.hash_bits} ∉ {{32, 64}}")
    if a.test_plafond_mo and a.test_plafond_mo <= 0:
        raise ErreurNommee("parametre_invalide", "--test-plafond-mo doit être > 0")


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
    bloc_o = max(int(a.bloc_mo * MIB), a.shingle * LONGUEUR_MIN_BLOC, 4096)
    if a.recouvrement_mo is None:
        rec_o = max(a.shingle, min(MIB, int(0.02 * bloc_o)))
        rec_origine = "2 % du bloc, plafonné à 1 Mio"
    else:
        rec_o = max(a.shingle, int(a.recouvrement_mo * MIB))
        rec_origine = "--recouvrement-mo"

    budget_o = int(a.memoire_mo * MIB)
    cal = cout_entree()
    besoin_bloc = FACTEUR_BLOC * (bloc_o + rec_o) + DIVERS_BLOC_MO * MIB
    plancher = besoin_bloc + PLANCHER_MO * MIB
    attendus = max(1, math.ceil(1.5 * taille / a.pas))

    rapport["memoire"].update({
        "budget_mio": round(budget_o / MIB, 1),
        "plancher_mio": round(plancher / MIB, 1),
        "bloc_mio": round(bloc_o / MIB, 2),
        "recouvrement_octets": rec_o,
        "recouvrement_origine": rec_origine,
        "cout_entree": cal,
        "ancres_attendues": attendus,
    })

    marge_min = 32 * MIB
    if budget_o < plancher + marge_min:
        raise ErreurNommee(
            "budget_memoire_impossible",
            f"budget {budget_o / MIB:.0f} Mio < plancher {plancher / MIB:.0f} Mio "
            f"(4 × (bloc {bloc_o / MIB:.1f} + recouvrement {rec_o / MIB:.2f}) "
            f"+ {DIVERS_BLOC_MO:.0f} + {PLANCHER_MO:.0f} Mio) + {marge_min / MIB:.0f} Mio "
            f"pour le jeu de shingles",
        )

    dispo = budget_o - plancher
    capacite = int(dispo / cal["cout_entree_octets"])
    if capacite < 1000:
        raise ErreurNommee(
            "budget_memoire_impossible",
            f"{capacite} entrées de set seulement après le plancher — budget inutile",
        )
    p_cible = MARGE_CAPACITE * capacite / attendus
    if p_cible >= 1.0:
        k = 0
    else:
        if p_cible <= 0:
            raise ErreurNommee("echantillon_trop_faible", "échantillon nul")
        k = math.ceil(-math.log2(p_cible))
        if k > 20:
            raise ErreurNommee(
                "echantillon_trop_faible",
                f"taux 1/{1 << k} < 1/{ECHANTILLON_MIN} : budget {budget_o / MIB:.0f} Mio "
                f"trop petit pour {taille / MIB:.0f} Mio d'entrée (capacité {capacite} entrées)",
            )
    masque = (1 << k) - 1
    p = 1.0 / (1 << k)
    plafond_o = int(a.test_plafond_mo * MIB) if a.test_plafond_mo else budget_o

    rapport["memoire"].update({
        "capacite_entrees": capacite,
        "taux_echantillonnage": f"1/{1 << k}",
        "p": p,
        "plafond_test_mio": a.test_plafond_mo or None,
    })
    rapport["shingles"].update({
        "shingle_octets": a.shingle,
        "pas": a.pas,
        "hash_bits": a.hash_bits,
        "graine": a.graine,
        "taux_echantillonnage": f"1/{1 << k}",
        "ancrage": "début de ligne + tous les --pas octets dans la ligne "
                   "(positions définies par le contenu : insensibles au décalage)",
    })

    hach, graine = hacheur(a.hash_bits, a.graine)
    seuil = a.seuil
    w = a.shingle
    pas = a.pas

    vus: set[int] = set()
    journal: list[dict] = []
    dist = {b: 0 for b in ("0", "0-1", "1-5", "5-20", "20-50", "50-80", "80-95", "95-100")}

    blocs = gardes = ecartes = 0
    octets_gardes = octets_ecartes = 0
    lignes_gardees = 0
    tot_c = vus_c = vus_inclus = 0
    calc = 0
    rss_max = 0
    sha = hashlib.sha256()
    f_entree = open(entree, "rb")
    f_sortie = open(sortie, "wb")

    tampon = bytearray()
    base = 0

    def remplir(jusqua: int) -> None:
        nonlocal tampon
        while base + len(tampon) < jusqua:
            morceau = f_entree.read(min(jusqua - (base + len(tampon)), 8 * MIB))
            if not morceau:
                return
            tampon += morceau

    def classe(fraction: float) -> str:
        if fraction <= 0.0:
            return "0"
        for borne, nom in ((0.01, "0-1"), (0.05, "1-5"), (0.2, "5-20"),
                           (0.5, "20-50"), (0.8, "50-80"), (0.95, "80-95")):
            if fraction < borne:
                return nom
        return "95-100"

    debut = 0
    dernier_affichage = 0.0
    try:
        while debut < taille:
            blocs += 1
            cible_fin = min(debut + bloc_o, taille)
            besoin = min(taille, cible_fin + rec_o)
            remplir(besoin)

            if cible_fin >= taille:
                fin = taille
            else:
                rel_cible = cible_fin - base
                rel_min = max(0, (debut + bloc_o // 2) - base)
                idx = tampon.rfind(b"\n", rel_min, rel_cible)
                fin = cible_fin if idx < 0 else base + idx + 1

            ext_fin = min(taille, fin + rec_o)
            p1 = debut - base
            p2, p3 = fin - base, ext_fin - base
            brut_coeur = bytes(tampon[p1:p2])
            n_coeur = normalise(brut_coeur)
            n_suffixe = normalise(bytes(tampon[p2:p3]))
            norm = n_coeur + n_suffixe
            fin_n = len(n_coeur)      # le cœur commence à 0 : le bloc est coupé sur un \n
            L = len(norm)

            liste: list[int] = []
            tot_bloc = vus_bloc = 0
            ancre = 0
            while ancre < fin_n:
                nl = norm.find(b"\n", ancre)
                fin_ligne = nl if 0 <= nl < fin_n else fin_n
                pos = ancre
                while pos < fin_ligne and pos + w <= L:
                    hh = hach(norm[pos:pos + w]) ^ graine
                    calc += 1
                    if not (hh & masque):
                        tot_c += 1
                        tot_bloc += 1
                        vu = hh in vus
                        if vu:
                            vus_c += 1
                            vus_bloc += 1
                        liste.append(hh)
                    pos += pas
                ancre = fin_ligne + 1

            fraction = vus_bloc / tot_bloc if tot_bloc else 0.0
            garde = (tot_bloc == 0) or (fraction < seuil)
            # second taux, comparable à l'inventaire : on compte aussi les répétitions
            # internes au bloc (même définition qu'une passe unique sur le fichier)
            if liste and len(liste) <= 1_000_000:
                loc: set[int] = set()
                inclus = 0
                for h in liste:
                    if h in vus or h in loc:
                        inclus += 1
                    loc.add(h)
                vus_inclus += inclus
            vus.update(liste)

            if garde:
                f_sortie.write(brut_coeur)
                sha.update(brut_coeur)
                lignes_gardees += brut_coeur.count(b"\n")
                octets_gardes += len(brut_coeur)
                gardes += 1
            else:
                octets_ecartes += len(brut_coeur)
                ecartes += 1

            rss = rss_max_octets()
            rss_max = max(rss_max, rss)
            if rss > plafond_o:
                raise ErreurNommee(
                    "memoire_depassee",
                    f"RSS max {rss / MIB:.0f} Mio > plafond {plafond_o / MIB:.0f} Mio "
                    f"au bloc {blocs}",
                )
            if len(vus) > capacite:
                raise ErreurNommee(
                    "capacite_depassee",
                    f"{len(vus)} entrées > capacité {capacite} au bloc {blocs} — "
                    f"le modèle de budget est faux",
                )

            dist[classe(fraction)] += 1
            if len(journal) < JOURNAL_MAX:
                journal.append({
                    "bloc": blocs,
                    "debut": debut,
                    "fin": fin,
                    "octets": len(brut_coeur),
                    "lignes": brut_coeur.count(b"\n"),
                    "shingles": tot_bloc,
                    "vus": vus_bloc,
                    "fraction": round(fraction, 4),
                    "garde": garde,
                    "rss_mio": round(rss / MIB, 1),
                })

            maintenant = time.perf_counter()
            if blocs <= 200 or maintenant - dernier_affichage > 5.0:
                dernier_affichage = maintenant
                print(
                    f"[bloc {blocs}] {debut / MIB:.0f}/{taille / MIB:.0f} Mio, "
                    f"{fraction:.1%} vu, {'gardé' if garde else 'écarté'}, "
                    f"RSS {rss / MIB:.0f} Mio, {maintenant - t0:.0f} s",
                    file=sys.stderr, flush=True,
                )

            debut = fin
            garder_depuis = max(0, debut - rec_o - base)
            if garder_depuis > 0:
                del tampon[:garder_depuis]
                base += garder_depuis
    finally:
        f_entree.close()
        f_sortie.close()

    duree = time.perf_counter() - t0
    rapport["sortie"].update({
        "chemin": str(sortie),
        "octets": sortie.stat().st_size if sortie.exists() else 0,
        "sha256": sha.hexdigest(),
        "lignes": lignes_gardees,
    })
    rapport["blocs"].update({
        "total": blocs,
        "gardes": gardes,
        "ecartes": ecartes,
        "octets_gardes": octets_gardes,
        "octets_ecartes": octets_ecartes,
        "pct_octets_ecartes": round(100 * octets_ecartes / taille, 3) if taille else 0.0,
    })
    rapport["shingles"].update({
        "calcules": calc,
        "echantillonnes": tot_c,
        "vus": vus_c,
        "vus_pct": round(100 * vus_c / tot_c, 3) if tot_c else 0.0,
        "vus_incluant_bloc": vus_inclus,
        "vus_incluant_bloc_pct": round(100 * vus_inclus / tot_c, 3) if tot_c else 0.0,
        "definition": "vus_pct = déjà présents avant le bloc (métrique de décision) ; "
                      "vus_incluant_bloc_pct = y compris les répétitions internes au bloc "
                      "(même définition qu'une passe unique, comparable à l'inventaire)",
    })
    rapport["distribution"] = {"fraction_seuil": dist}
    rapport["journal_blocs"] = journal
    rapport["journal_tronque"] = blocs > len(journal)
    rapport["duree_s"] = round(duree, 1)
    rapport["debit_mio_s"] = round((taille / MIB) / duree, 1) if duree else None
    rapport["memoire"]["rss_max_mio"] = round(rss_max / MIB, 1)
    rapport["memoire"]["marge_mio"] = round((budget_o - rss_max) / MIB, 1)
    rapport["verdict"] = "ok"


def squelette(a) -> dict:
    return {
        "outil": "tools/dedup_blocs.py",
        "date": dt.datetime.now().isoformat(timespec="seconds"),
        "verdict": None,
        "entree": {"chemin": str(pathlib.Path(a.entree).resolve()) if a.entree else None,
                   "octets": None,
                   "mtime": None},
        "sortie": {"chemin": str(pathlib.Path(a.sortie).resolve()) if a.sortie else None,
                   "octets": 0, "sha256": None, "lignes": 0},
        "parametres": parametres_json(a),
        "memoire": {},
        "shingles": {},
        "blocs": {},
        "distribution": {},
        "duree_s": None,
        "journal_blocs": [],
        "comparaison_inventaire": {
            "source": "reports/rapport-donnees-inventaire.md § 1",
            "shingles_vus_pct_crc32_pas96": 2.93,
            "duplication_reelle_estimee_pct": 2.0,
            "note": "même fenêtre (96 o), mais la grille de l'inventaire est à pas fixe "
                    "(offset du fichier) : elle sous-estime, une copie décalée n'y partage "
                    "une fenêtre que si le décalage est multiple du pas",
        },
    }


# --- contrôle négatif --------------------------------------------------------
VOCABULAIRE = (
    "la le les un une des du de au aux et ou mais donc or ni car que qui quoi dont où "
    "il elle ils elles nous vous on je tu se sa son ses leur leurs ce cet cette ces "
    "être avoir faire dire aller venir voir savoir pouvoir vouloir devoir falloir "
    "temps jour nuit matin soir année siècle monde pays ville région rivière montagne "
    "mer forêt chemin route pont maison église château village quartier rue place "
    "homme femme enfant père mère frère sœur ami voisin maître élève école livre page "
    "mot phrase texte histoire récit roman poème auteur lecteur œuvre époque "
    "guerre paix roi reine prince peuple armée soldat voyage retour départ arrivée "
    "ciel terre eau feu air vent pluie neige soleil lune étoile lumière ombre couleur "
    "rouge bleu vert noir blanc grand petit long court haut bas vieux jeune beau "
    "nouveau premier dernier même autre tout chaque plusieurs quelques certain "
    "toujours jamais souvent parfois déjà encore ici là ailleurs partout "
    "commencer finir continuer changer devenir rester passer entrer sortir monter "
    "descendre ouvrir fermer prendre donner recevoir trouver perdre chercher "
    "penser croire comprendre apprendre enseigner écrire lire parler écouter "
    "marcher courir travailler dormir manger boire vivre mourir aimer haïr"
).split()

VOCABULAIRE_TECH = (
    "système réseau données protocole mesure calcul modèle structure fonction "
    "variable nombre valeur ensemble graphe arbre liste table colonne ligne "
    "algorithme processus mémoire disque processeur signal fréquence onde "
    "énergie matière atome molécule cellule organe tissu espèce population "
    "échantillon hypothèse expérience résultat méthode analyse synthèse "
    "théorème preuve démonstration axiome définition lemme corollaire "
    "vecteur matrice tenseur dérivée intégrale limite suite série "
    "capteur moteur circuit tension courant puissance rendement "
    "logiciel matériel serveur client fichier format octet bit registre "
    "compression stockage lecture écriture transfert débit latence "
    "modèle apprentissage couche neurone poids gradient perte "
    "validation test corpus texte jeton vocabulaire séquence attention "
    "convergence itération paramètre hyperparamètre bruit biais variance"
).split()


def genere_texte(graine: int, n_paragraphes: int, octets_par_paragraphe: int,
                 vocabulaire: list[str]) -> bytes:
    """Texte pseudo-français déterministe, paragraphes de taille exacte (octets UTF-8)."""
    rng = random.Random(graine)
    sortie = bytearray()
    for _ in range(n_paragraphes):
        para = bytearray()
        while True:
            n = rng.randint(8, 18)
            phrase = " ".join(rng.choice(vocabulaire) for _ in range(n))
            phrase = (phrase[0].upper() + phrase[1:] + ". ").encode("utf-8")
            if len(para) + len(phrase) > octets_par_paragraphe - 2:
                break
            para += phrase
        para += b" " * (octets_par_paragraphe - 1 - len(para)) + b"\n"
        sortie += para
    return bytes(sortie)


def disperse(texte: bytes, fraction: float, graine: int, vocabulaire: list[str]) -> bytes:
    """Remplace `fraction` des mots par d'autres, dispersés : la copie « 10 % modifiée »."""
    s = texte.decode("utf-8")
    rng = random.Random(graine)
    mots = list(MOT.finditer(s))
    choisis = set(rng.sample(range(len(mots)), int(len(mots) * fraction)))
    sortie: list[str] = []
    pos = 0
    for i, m in enumerate(mots):
        if i in choisis:
            sortie.append(s[pos:m.start()])
            sortie.append(rng.choice(vocabulaire))
            pos = m.end()
    sortie.append(s[pos:])
    return "".join(sortie).encode("utf-8")


def lance_autotest(repertoire: pathlib.Path) -> tuple[bool, dict]:
    repertoire = repertoire.resolve()
    if est_sous(repertoire, RACINE / "data"):
        raise ErreurNommee("sortie_interdite", f"{repertoire} est sous data/ (lecture seule)")
    repertoire.mkdir(parents=True, exist_ok=True)
    outil = str(pathlib.Path(__file__).resolve())
    paragraphe = 2048
    n_para = 128
    A = genere_texte(11, n_para, paragraphe, VOCABULAIRE)
    X = genere_texte(22, n_para, paragraphe, VOCABULAIRE)
    D = genere_texte(33, n_para, paragraphe, VOCABULAIRE_TECH)
    B = A
    # C : un paragraphe sur dix remplacé → ≈ 9,4 % des octets neufs, uniformément par bloc
    paras = [A[i:i + paragraphe] for i in range(0, len(A), paragraphe)]
    remp = [X[i:i + paragraphe] for i in range(0, len(X), paragraphe)]
    for i in range(9, len(paras), 10):
        paras[i] = remp[i]
    C = b"".join(paras)
    assert len(A) == len(B) == len(C) == n_para * paragraphe
    controle = repertoire / "controle.txt"
    controle.write_bytes(A + B + C + D)
    # copie décalée : précéder B d'une ligne de 23 octets décale tout le fichier
    decalage = b"note de bas de page.\n"
    controle_decale = repertoire / "controle_decale.txt"
    controle_decale.write_bytes(A + decalage + B + D)
    C2 = disperse(A, 0.10, 44, VOCABULAIRE)
    controle_disp = repertoire / "controle_disperse.txt"
    controle_disp.write_bytes(A + C2)

    def lance(nom: str, args: list[str]) -> tuple[int, dict, str]:
        json_path = repertoire / f"{nom}.json"
        cmd = [sys.executable, outil, *args, "--json", str(json_path)]
        p = subprocess.run(cmd, capture_output=True, text=True)
        rapport = json.loads(json_path.read_text()) if json_path.exists() else {}
        return p.returncode, rapport, (p.stderr or "") + (p.stdout or "")

    def fractions(rapport: dict) -> list[float]:
        return [b["fraction"] for b in rapport.get("journal_blocs", [])]

    def gardes(rapport: dict) -> list[bool]:
        return [b["garde"] for b in rapport.get("journal_blocs", [])]

    cas: list[dict] = []

    def verifie(nom: str, condition: bool, detail) -> None:
        cas.append({"nom": nom, "ok": bool(condition), "detail": detail})

    commun = ["--entree", str(controle), "--bloc-mo", "0.0625"]
    rc1, r1, log1 = lance("seuil080", [*commun, "--sortie", str(repertoire / "garde-080.txt"),
                                      "--seuil", "0.8", "--memoire-mo", "512"])
    g1 = gardes(r1)
    f1 = fractions(r1)
    verifie("a_texte_unique_garde", all(g1[0:4]) and rc1 == 0, {"blocs": g1[0:4], "rc": rc1})
    verifie("b_copie_exacte_ecartee", not any(g1[4:8]), {"blocs": g1[4:8], "fractions": f1[4:8]})
    verifie("b_fraction_1", all(x == 1.0 for x in f1[4:8]), {"fractions": f1[4:8]})
    verifie("c_copie_10pct_ecartee_a_080", not any(g1[8:12]),
            {"blocs": g1[8:12], "fractions": f1[8:12]})
    verifie("d_texte_different_garde", all(g1[12:16]), {"blocs": g1[12:16], "fractions": f1[12:16]})
    attendu = A + D
    sortie1 = (repertoire / "garde-080.txt").read_bytes()
    verifie("sortie_egale_a_plus_d", sortie1 == attendu,
            {"octets": len(sortie1), "attendu": len(attendu)})
    verifie("budget_respecte_controle", r1.get("memoire", {}).get("rss_max_mio", 1e9)
            < r1.get("memoire", {}).get("budget_mio", 0),
            {"rss_max_mio": r1.get("memoire", {}).get("rss_max_mio"),
             "budget_mio": r1.get("memoire", {}).get("budget_mio")})

    # stabilité : deux passes identiques
    rc2, r2, _ = lance("seuil080_bis", [*commun, "--sortie", str(repertoire / "garde-080-bis.txt"),
                                        "--seuil", "0.8", "--memoire-mo", "512"])
    verifie("stable_sha256", r1.get("sortie", {}).get("sha256") == r2.get("sortie", {}).get("sha256"),
            {"sha1": r1.get("sortie", {}).get("sha256"),
             "sha2": r2.get("sortie", {}).get("sha256")})
    verifie("stable_blocs", gardes(r1) == gardes(r2) and fractions(r1) == fractions(r2),
            {"identiques": gardes(r1) == gardes(r2)})
    verifie("stable_octets", r1.get("sortie", {}).get("octets") == r2.get("sortie", {}).get("octets"),
            {"octets": r1.get("sortie", {}).get("octets")})

    # seuil 0,95 : C (≈ 90 % vu) repasse
    rc3, r3, _ = lance("seuil095", [*commun, "--sortie", str(repertoire / "garde-095.txt"),
                                    "--seuil", "0.95", "--memoire-mo", "512"])
    g3 = gardes(r3)
    f3 = fractions(r3)
    verifie("c_garde_a_095", all(g3[8:12]), {"blocs": g3[8:12], "fractions": f3[8:12]})
    verifie("c_fraction_entre_080_et_095", all(0.80 <= x < 0.95 for x in f3[8:12]),
            {"fractions": f3[8:12]})
    verifie("sortie_095_egale_a_plus_c_plus_d",
            (repertoire / "garde-095.txt").read_bytes() == A + C + D,
            {"octets": (repertoire / "garde-095.txt").stat().st_size})

    # copie décalée de 23 octets : doit être écartée (c'est ce qu'une grille fixe rate)
    rc4, r4, _ = lance("decale", ["--entree", str(controle_decale),
                                  "--sortie", str(repertoire / "garde-decale.txt"),
                                  "--bloc-mo", "0.0625", "--seuil", "0.8",
                                  "--memoire-mo", "512"])
    g4 = gardes(r4)
    f4 = fractions(r4)
    verifie("copie_decalee_ecartee", not any(g4[4:8]), {"blocs": g4[4:8], "fractions": f4[4:8]})

    # 10 % dispersé : les shingles sont locaux, la copie est gardée
    rc5, r5, _ = lance("disperse", ["--entree", str(controle_disp),
                                    "--sortie", str(repertoire / "garde-disperse.txt"),
                                    "--bloc-mo", "0.0625", "--seuil", "0.8",
                                    "--memoire-mo", "512"])
    g5 = gardes(r5)
    f5 = fractions(r5)
    verifie("copie_10pct_disperse_gardee", all(g5[4:8]), {"blocs": g5[4:8], "fractions": f5[4:8]})

    # 32 bits : mêmes décisions sur un petit fichier (collisions négligeables)
    rc6, r6, _ = lance("hash32", [*commun, "--sortie", str(repertoire / "garde-32.txt"),
                                  "--seuil", "0.8", "--hash-bits", "32", "--memoire-mo", "512"])
    verifie("hash32_memes_decisions", gardes(r6) == g1,
            {"hash32": gardes(r6)[:16], "identique": gardes(r6) == g1})

    # budget impossible : refus au départ, nommé
    rc7, r7, log7 = lance("budget_impossible", ["--entree", str(controle),
                                                "--sortie", str(repertoire / "jamais.txt"),
                                                "--bloc-mo", "64", "--memoire-mo", "64"])
    verifie("budget_impossible_nomme",
            rc7 == 3 and r7.get("erreur", {}).get("nom") == "budget_memoire_impossible",
            {"rc": rc7, "erreur": r7.get("erreur"), "stderr": log7.strip().splitlines()[-1:]})

    # chien de garde : plafond de test abaissé → memoire_depassee
    rc8, r8, log8 = lance("chien_de_garde", [*commun, "--sortie", str(repertoire / "partiel.txt"),
                                             "--seuil", "0.8", "--memoire-mo", "256",
                                             "--test-plafond-mo", "8"])
    verifie("chien_de_garde_memoire_depassee",
            rc8 == 3 and r8.get("erreur", {}).get("nom") == "memoire_depassee",
            {"rc": rc8, "erreur": r8.get("erreur")})

    resume = {
        "ok": all(c["ok"] for c in cas),
        "controle": str(controle),
        "textes": {"A": len(A), "B": len(B), "C": len(C), "C2": len(C2), "D": len(D),
                   "paragraphe_octets": paragraphe, "paragraphes": n_para,
                   "decalage_octets": len(decalage)},
        "fractions": {"b": f1[4:8], "c": f1[8:12], "d": f1[12:16],
                      "c_decale": f4[4:8], "c_disperse": f5[4:8]},
        "cas": cas,
    }
    ecrit_json(repertoire / "autotest.json", resume)
    return resume["ok"], resume


# --- CLI ---------------------------------------------------------------------
def parse(argv=None):
    ap = argparse.ArgumentParser(
        description="Dédoublonner un fichier texte par blocs, à mémoire bornée.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--entree", help="fichier texte à dédupliquer (lecture seule)")
    ap.add_argument("--sortie", help="fichier de sortie (les blocs gardés)")
    ap.add_argument("--bloc-mo", dest="bloc_mo", type=float, default=64.0,
                    help="taille d'un bloc en Mio (défaut 64)")
    ap.add_argument("--memoire-mo", dest="memoire_mo", type=float, default=2048.0,
                    help="budget mémoire en Mio (défaut 2048)")
    ap.add_argument("--shingle", type=int, default=96, help="fenêtre en octets (défaut 96)")
    ap.add_argument("--seuil", type=float, default=0.8,
                    help="fraction de shingles déjà vus au-delà de laquelle un bloc est écarté")
    ap.add_argument("--json", default=None, help="manifeste JSON de la passe")
    ap.add_argument("--pas", type=int, default=48,
                    help="un shingle tous les --pas octets dans une ligne (défaut 48)")
    ap.add_argument("--hash-bits", dest="hash_bits", type=int, choices=(32, 64), default=64,
                    help="largeur des hachages (défaut 64)")
    ap.add_argument("--graine", type=int, default=0, help="décale les hachages (échantillon)")
    ap.add_argument("--recouvrement-mo", dest="recouvrement_mo", type=float, default=None,
                    help="marge de contexte après le bloc, en Mio "
                         "(défaut : 2 %% du bloc, max 1 Mio)")
    ap.add_argument("--autotest", action="store_true", help="contrôle négatif reproductible")
    ap.add_argument("--repertoire", default=str(RACINE / "work/dedup/controle"),
                    help="répertoire de l'autotest")
    ap.add_argument("--test-plafond-mo", dest="test_plafond_mo", type=float, default=0.0,
                    help=argparse.SUPPRESS)  # hameçon de test du chien de garde
    a = ap.parse_args(argv)
    if not a.autotest and (not a.entree or not a.sortie):
        ap.error("--entree et --sortie sont requis (ou --autotest)")
    return a


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
            rapport["entree"].update({"octets": st.st_size,
                                      "mtime": dt.datetime.fromtimestamp(st.st_mtime)
                                      .isoformat(timespec="seconds")})
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
        "duree_s": rapport["duree_s"],
        "debit_mio_s": rapport["debit_mio_s"],
        "rss_max_mio": rapport["memoire"].get("rss_max_mio"),
        "budget_mio": rapport["memoire"].get("budget_mio"),
        "blocs": rapport["blocs"],
        "shingles": rapport["shingles"],
        "sortie": {k: v for k, v in rapport["sortie"].items() if k != "chemin"},
    }, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
