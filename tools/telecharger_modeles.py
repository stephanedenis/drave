#!/usr/bin/env python3
"""Télécharge les modèles LOURDS, par tranches, avec reprise.

Pourquoi par tranches : le pont Xet de Hugging Face refuse un GET plein sur le
fichier de 365,7 Go de `antirez/deepseek-v4.1-flash-gguf` (HTTP 400) alors qu'il
sert très bien une requête `Range` (HTTP 206). Mesuré, pas supposé. La découpe a
un second mérite : une coupure réseau ne coûte que la tranche en cours.

Le NVMe ne sert plus qu'aux fichiers que NOUS produisons : les modèles bruts vont
sur le disque mécanique (`/home/stephane/Data13TB/stephane/modeles/gguf`).

Usage :
    telecharger_modeles.py --manifeste tools/manifeste_modeles_lourds.json
    telecharger_modeles.py --seulement Kimi-K2.7-Code-UD-IQ1_M
    telecharger_modeles.py --etat          # où en est chaque fichier
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time

RACINE = "https://huggingface.co"
CHUNK = 256 << 20          # 256 Mo
DEST_DEFAUT = "/home/stephane/Data13TB/stephane/modeles/gguf"
LIBRE_MINIMUM_GO = 300     # on s'arrête bien avant de remplir le disque


def humain(n):
    return f"{n / 1e9:.1f} Go"


def _tranche(url, dest, debut, fin, etat, cle, journal, essais=6):
    """Télécharge [debut, fin] (bornes incluses) et l'écrit à sa place.

    L'avancement est noté par tranche dans un sidecar JSON : un arrêt reprend
    exactement où il en était, sans relire ce qui est déjà écrit.
    """
    pos = etat.get(cle, debut)
    fd = os.open(dest, os.O_WRONLY)
    part = f"{dest}.part{cle}"
    while pos <= fin:
        haut = min(pos + CHUNK, fin + 1) - 1
        ok = False
        for essai in range(essais):
            r = subprocess.run(
                ["curl", "-sSL", "-f", "--retry", "3", "--retry-delay", "10",
                 "--retry-all-errors", "-r", f"{pos}-{haut}", "-o", part, url],
                capture_output=True, text=True)
            if r.returncode == 0 and os.path.exists(part) and \
               os.path.getsize(part) == haut - pos + 1:
                ok = True
                break
            time.sleep(5 * (essai + 1))
        if not ok:
            os.close(fd)
            return False
        with open(part, "rb") as g:
            os.pwrite(fd, g.read(), pos)
        os.remove(part)
        pos = haut + 1
        etat[cle] = pos
    os.close(fd)
    return True


def telecharger(url, dest, octets, journal, fils=6, essais=6):
    """Complète `dest` jusqu'à `octets`, en `fils` tranches parallèles.

    Mesuré : le débit d'une connexion va de 5 à 62 Mo/s selon les instants ; six
    connexions sur des tranches disjointes lissent ça — et le fichier de 365,7 Go
    n'a pas d'autre moyen d'aller vite, puisqu'il est seul.
    """
    import threading
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest) and os.path.getsize(dest) >= octets:
        return True
    fichier_etat = dest + ".etat.json"
    etat = json.load(open(fichier_etat)) if os.path.exists(fichier_etat) else {}
    with open(dest, "ab"):
        pass
    if os.path.getsize(dest) < octets:
        with open(dest, "r+b") as f:
            f.truncate(octets)
    pas = (octets + fils - 1) // fils
    bornes = [(i * pas, min(octets, (i + 1) * pas) - 1) for i in range(fils)]
    bornes = [(a, b) for a, b in bornes if a <= b]
    t0 = time.time()
    echec = []

    def ouvrier(i, a, b):
        if not _tranche(url, dest, a, b, etat, i, journal, essais):
            echec.append(i)

    vifs = [threading.Thread(target=ouvrier, args=(i, a, b))
            for i, (a, b) in enumerate(bornes) if etat.get(i, a) <= b]
    for t in vifs:
        t.start()
    dernier = 0.0
    while any(t.is_alive() for t in vifs):
        time.sleep(10)
        fait = sum(min(etat.get(i, a), b + 1) - a for i, (a, b) in enumerate(bornes))
        if time.time() - dernier > 30:
            journal(f"  {humain(fait)} / {humain(octets)} "
                    f"({100 * fait / octets:.1f} %, "
                    f"{fait / max(1e-9, time.time() - t0) / 1e6:.0f} Mo/s)")
            json.dump(etat, open(fichier_etat, "w"))
            dernier = time.time()
    for t in vifs:
        t.join()
    if echec:
        journal(f"  ÉCHEC des tranches {echec}")
        return False
    if os.path.exists(fichier_etat):
        os.remove(fichier_etat)
    return os.path.getsize(dest) >= octets


def libre_go(chemin):
    return shutil.disk_usage(chemin).free / 1e9


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifeste", default="tools/manifeste_modeles_lourds.json")
    ap.add_argument("--dest", default=DEST_DEFAUT)
    ap.add_argument("--seulement", default="")
    ap.add_argument("--etat", action="store_true")
    ap.add_argument("--journal", default="/tmp/telechargement_lourds.log")
    args = ap.parse_args()

    entrees = json.load(open(args.manifeste, encoding="utf-8"))
    if args.seulement:
        entrees = [e for e in entrees if e["nom"] == args.seulement]
        if not entrees:
            print(f"aucune entrée nommée {args.seulement}")
            return 1

    def journal(texte):
        ligne = f"{time.strftime('%H:%M:%S')}  {texte}"
        print(ligne, flush=True)
        with open(args.journal, "a", encoding="utf-8") as f:
            f.write(ligne + "\n")

    if args.etat:
        # ⚠️ Le fichier est PRÉALLOCÉ à sa taille finale (pour écrire des tranches
        # au bon endroit) : `getsize` dit donc 100 % dès le premier octet reçu.
        # L'avancement réel est dans le sidecar de tranches.
        par_nom = {}
        for e in entrees:
            d = par_nom.setdefault(e["nom"], [0, 0])
            p = os.path.join(args.dest, e["nom"], os.path.basename(e["chemin"]))
            etat_side = p + ".etat.json"
            fait = 0
            if os.path.exists(etat_side):
                # Les tranches notent leur prochaine position ABSOLUE : sommer les
                # valeurs compterait les débuts de tranche. On retire ces débuts
                # (mêmes bornes que `telecharger`, donc `fils` tranches égales).
                et = json.load(open(etat_side))
                fils = max(1, len(et))
                pas = (e["octets"] + fils - 1) // fils
                fait = min(sum(max(0, int(v) - int(i) * pas)
                               for i, v in et.items()), e["octets"])
            elif os.path.exists(p):
                fait = min(os.path.getsize(p), e["octets"])
            d[0] += fait
            d[1] += e["octets"]
        for nom, (fait, total) in sorted(par_nom.items()):
            print(f"{nom:28} {humain(fait):>10} / {humain(total):>10}  "
                  f"{100 * fait / max(1, total):5.1f} %")
        print(f"libre : {libre_go(args.dest):.0f} Go")
        return 0

    for e in entrees:
        nom, chemin, octets = e["nom"], e["chemin"], e["octets"]
        url = f"{RACINE}/{e['repo']}/resolve/main/{chemin}"
        dest = os.path.join(args.dest, nom, os.path.basename(chemin))
        if os.path.exists(dest) and os.path.getsize(dest) >= octets:
            continue
        libre = libre_go(args.dest)
        if libre < LIBRE_MINIMUM_GO:
            journal(f"ARRÊT : {libre:.0f} Go libres (< {LIBRE_MINIMUM_GO} Go)")
            return 1
        journal(f"{nom} · {os.path.basename(chemin)} · {humain(octets)} "
                f"({libre:.0f} Go libres)")
        if not telecharger(url, dest, octets, journal):
            journal(f"{nom} : INCOMPLET sur {os.path.basename(chemin)}")
            return 1
        journal(f"{nom} · {os.path.basename(chemin)} : fait")
    journal("=== FILE TERMINÉE ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
