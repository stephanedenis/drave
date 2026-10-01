#!/usr/bin/env python3
"""Convertisseur GGUF → « modèle éclaté en clusters », un fichier par cluster.

**Pourquoi.** Notre mode d'opération ne lit que les experts qu'un jeton allume, et
les modèles MoE publient leurs experts dans UN tenseur par couche
(`blk.N.ffn_gate_exps.weight [n_experts, …]`). Un nœud qui n'héberge que 16 experts
sur 128 lit donc un fichier de 18 Go pour en utiliser un huitième. Ici, chaque
cluster devient un **fichier GGUF autonome** : on l'ouvre seul, en mmap, et on ne
lit que sa tranche.

**Ce que le convertisseur NE fait pas** : il ne requantifie rien. Les octets des
poids sont copiés tels quels (les blocs de quantification sont alignés sur l'axe
des experts, donc une tranche d'expert est une plage d'octets exacte). Aucune perte,
aucune conversion, aucun choix de format de rechange.

**Sortie** (dans un dossier) :

    commun.gguf          ce qui n'est pas un expert : embeddings, sortie, attention,
                         normes, routeur de chaque couche
    cluster-00.gguf …    par cluster : les tranches d'experts de TOUTES les couches
    manifeste.json       rôle de chaque fichier, tenseurs portés, tailles, ordre des
                         experts, correspondance expert local ↔ identifiant global

Chaque fichier est un GGUF valide et lisible par le lecteur existant ; le champ
`<arch>.expert_count` y est ajusté au nombre d'experts du fichier, et le manifeste
porte la traduction vers les identifiants globaux.

Usage :
    convertir_clusters.py <source.gguf> <dossier> [--clusters 8] [--trace routage.txt]
                          [--mode experts|couches] [--verifier]
"""
import argparse
import hashlib
import json
import os
import struct
import sys
import time
from collections import defaultdict

# Types ggml et leur taille : octets par bloc, et éléments par bloc.
TYPES = {
    0:  ("F32", 4, 1), 1: ("F16", 2, 1), 2: ("Q4_0", 18, 32), 3: ("Q4_1", 20, 32),
    6: ("Q5_0", 22, 32), 7: ("Q5_1", 24, 32), 8: ("Q8_0", 34, 32),
    9: ("Q8_1", 36, 32), 10: ("Q2_K", 84, 256), 11: ("Q3_K", 110, 256),
    12: ("Q4_K", 144, 256), 13: ("Q5_K", 176, 256), 14: ("Q6_K", 210, 256),
    15: ("Q8_K", 292, 256), 39: ("MXFP4", 17, 32),
}


def taille_tenseur(ttype, dims):
    """Octets exacts d'un tenseur : blocs le long de la DERNIÈRE dimension."""
    nom, octets_bloc, elem_bloc = TYPES[ttype]
    n = 1
    for d in dims:
        n *= d
    if len(dims) > 1:
        n = n // dims[-1] * dims[-1]
    return n // elem_bloc * octets_bloc


class Lecteur:
    """Lecture séquentielle bornée d'un GGUF (en-têtes seulement)."""

    def __init__(self, chemin):
        self.f = open(chemin, "rb")
        self.chemin = chemin
        self.taille_fichier = os.path.getsize(chemin)

    def lire(self, n):
        b = self.f.read(n)
        if len(b) != n:
            raise EOFError(f"{self.chemin} : {n} octets demandés, {len(b)} lus")
        return b

    def u32(self):
        return struct.unpack("<I", self.lire(4))[0]

    def u64(self):
        return struct.unpack("<Q", self.lire(8))[0]

    def chaine(self):
        n = self.u64()
        return self.lire(n).decode("utf-8", errors="replace")


def sauter_valeur(l, ttype):
    """Avance sur une valeur de métadonnée (récursif pour les tableaux)."""
    if ttype == 0 or ttype == 1 or ttype == 7:
        l.lire(1)
    elif ttype == 2 or ttype == 3:
        l.lire(2)
    elif ttype in (4, 5, 6):
        l.lire(4)
    elif ttype in (10, 11, 12):
        l.lire(8)
    elif ttype == 8:
        l.chaine()
    elif ttype == 9:
        sous = l.u32()
        n = l.u64()
        for _ in range(n):
            sauter_valeur(l, sous)
    else:
        raise ValueError(f"type de métadonnée inconnu : {ttype}")


def lire_entete(chemin):
    """→ (kv_brut, tenseurs, debut_donnees, alignement).

    `kv_brut` est le bloc d'octets des paires clé/valeur, recopié tel quel dans les
    fichiers de sortie : les métadonnées du modèle (tokenizer compris) voyagent
    sans être réencodées.
    """
    l = Lecteur(chemin)
    magic = l.lire(4)
    if magic != b"GGUF":
        raise ValueError(f"{chemin} : ce n'est pas un GGUF ({magic!r})")
    version = l.u32()
    n_tensors = l.u64()
    n_kv = l.u64()
    debut_kv = l.f.tell()
    alignement = 32
    for _ in range(n_kv):
        cle = l.chaine()
        ttype = l.u32()
        if cle == "general.alignment" and ttype == 4:
            alignement = struct.unpack("<I", l.lire(4))[0]
        else:
            sauter_valeur(l, ttype)
    fin_kv = l.f.tell()
    l.f.seek(debut_kv)
    kv_brut = l.lire(fin_kv - debut_kv)
    tenseurs = []
    for _ in range(n_tensors):
        nom = l.chaine()
        nd = l.u32()
        dims = [l.u64() for _ in range(nd)]
        dims.reverse()                    # ggml stocke à l'envers
        ttype = l.u32()
        offset = l.u64()
        tenseurs.append({"nom": nom, "dims": dims, "ttype": ttype,
                         "offset": offset, "octets": taille_tenseur(ttype, dims)})
    fin_entete = l.f.tell()
    debut_donnees = (fin_entete + alignement - 1) // alignement * alignement
    l.f.close()
    return kv_brut, tenseurs, debut_donnees, alignement, n_tensors, version


def ecrire_gguf(chemin, kv_brut, tenseurs, source, debut_donnees, alignement,
                morceaux):
    """Écrit un GGUF autonome.

    `tenseurs` : descripteurs (nom, dims, ttype) dans l'ordre d'écriture.
    `morceaux` : pour chacun, la liste de (offset_source, longueur) à recopier.
    """
    with open(chemin, "wb") as f:
        f.write(b"GGUF")
        f.write(struct.pack("<I", 3))                     # version 3, comme la source
        f.write(struct.pack("<Q", len(tenseurs)))
        # nombre de paires KV : relu dans le bloc brut (les 8 derniers octets lus
        # seraient fragiles) — on recompte en reparcourant le bloc.
        n_kv = parcourir_kv(kv_brut)[0]
        f.write(struct.pack("<Q", n_kv))
        f.write(kv_brut)
        decalage = 0
        for t in tenseurs:
            nom = t["nom"].encode("utf-8")
            f.write(struct.pack("<Q", len(nom)))
            f.write(nom)
            f.write(struct.pack("<I", len(t["dims"])))
            for d in reversed(t["dims"]):
                f.write(struct.pack("<Q", d))
            f.write(struct.pack("<I", t["ttype"]))
            f.write(struct.pack("<Q", decalage))
            decalage += t["octets"]
        fin = f.tell()
        reste = (alignement - fin % alignement) % alignement
        f.write(b"\0" * reste)
        with open(source, "rb") as g:
            for t, morceaux_t in zip(tenseurs, morceaux):
                ecrit = 0
                for offset, longueur in morceaux_t:
                    g.seek(debut_donnees + offset)
                    reste_a_copier = longueur
                    while reste_a_copier > 0:
                        bloc = g.read(min(8 << 20, reste_a_copier))
                        if not bloc:
                            raise EOFError(f"{source} : lecture courte")
                        f.write(bloc)
                        reste_a_copier -= len(bloc)
                    ecrit += longueur
                if ecrit != t["octets"]:
                    raise ValueError(f"{t['nom']} : {ecrit} octets écrits pour "
                                     f"{t['octets']} attendus")
    return os.path.getsize(chemin)


def lire_valeur(f, ttype):
    """Lit une valeur et renvoie ses octets BRUTS (réencodables tels quels)."""
    if ttype in (0, 1, 7):
        return f.lire(1)
    if ttype in (2, 3):
        return f.lire(2)
    if ttype in (4, 5, 6):
        return f.lire(4)
    if ttype in (10, 11, 12):
        return f.lire(8)
    if ttype == 8:
        n = f.u64()
        return struct.pack("<Q", n) + f.lire(n)
    if ttype == 9:
        sous = f.u32()
        n = f.u64()
        debut = f.p
        for _ in range(n):
            sauter_valeur(f, sous)
        return struct.pack("<I", sous) + struct.pack("<Q", n) + f.b[debut:f.p]
    raise ValueError(f"type {ttype}")


def reecrire_kv(kv_brut, remplacements):
    """Réécrit le bloc KV avec les valeurs remplacées (`{clé: entier}`)."""
    class Faux2(Lecteur):
        def __init__(self, b):
            self.b, self.p = b, 0

        def lire(self, n):
            v = self.b[self.p:self.p + n]
            self.p += n
            return v
    f = Faux2(kv_brut)
    out = bytearray()
    while f.p < len(kv_brut):
        n = f.u64()
        cle = f.lire(n).decode("utf-8", errors="replace")
        t = f.u32()
        valeur = lire_valeur(f, t)
        if cle in remplacements:
            nouveau = remplacements[cle]
            if t == 4:
                valeur = struct.pack("<I", nouveau)
            elif t in (10, 5):
                valeur = struct.pack("<" + ("Q" if t == 10 else "i"), nouveau)
            else:
                raise ValueError(f"{cle} : type {t} non géré pour la réécriture")
        out += struct.pack("<Q", n) + cle.encode("utf-8") + struct.pack("<I", t) + valeur
    return bytes(out)


def parcourir_kv(kv_brut):
    """→ (nombre de paires, architecture) en reparcourant le bloc brut."""
    class Faux:
        def __init__(self, b):
            self.b, self.p = b, 0

        def lire(self, n):
            v = self.b[self.p:self.p + n]
            self.p += n
            return v

        def u32(self):
            return struct.unpack("<I", self.lire(4))[0]

        def u64(self):
            return struct.unpack("<Q", self.lire(8))[0]

        def chaine(self):
            return self.lire(self.u64()).decode("utf-8", errors="replace")
    f = Faux(kv_brut)
    n, arch = 0, None
    while f.p < len(kv_brut):
        cle = f.chaine()
        t = f.u32()
        if cle == "general.architecture" and t == 8:
            arch = f.chaine()
        else:
            sauter_valeur(f, t)
        n += 1
    return n, arch


def ordre_experts(trace, couche, ne):
    """Ordre des experts par fréquence décroissante (trace de routage), sinon
    l'ordre naturel. C'est la seule décision « intelligente » du convertisseur, et
    elle vient d'une mesure : les experts chauds d'abord, pour que le premier
    cluster soit celui qu'un nœud veut garder."""
    if not trace:
        return list(range(ne))
    import collections
    compte = collections.Counter()
    for ligne in trace.get(couche, []):
        compte.update(ligne)
    return sorted(range(ne), key=lambda e: (-compte.get(e, 0), e))


def lire_trace(chemin):
    par_couche = defaultdict(list)
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            m = ligne.split()
            if len(m) < 3:
                continue
            par_couche[int(m[0])].append([int(x) for x in m[2:]])
    return par_couche


def ecrire_mapping(dossier, manifeste):
    """Écrit `mapping.tsv` : la seule chose qui relie un expert GLOBAL à sa ligne
    LOCALE. Le moteur est en Rust sans dépendance ; un JSON demanderait un
    parseur de plus à éprouver, alors qu'un tableau de trois colonnes se relit à
    l'œil — ce qui n'est pas un luxe pour la pièce dont dépend chaque expert.

    Vérifie au passage que la répartition est complète et sans doublon : un
    expert manquant ferait un modèle silencieusement amputé.
    """
    if manifeste.get("mode") != "experts":
        # En mode « couches », il n'y a pas d'experts à répartir : chaque fichier
        # porte des couches entières, et le moteur les lit en clair.
        return
    n_exp, K = manifeste["n_experts"], manifeste["clusters"]
    clusters = sorted((f for f in manifeste["fichiers"]
                       if f.get("role", "").startswith("cluster-")),
                      key=lambda f: f["role"])
    lignes, vus = [], {}
    for c, f in enumerate(clusters):
        assert f["role"] == f"cluster-{c:02d}", f["role"]
        for couche, globaux in sorted(f["experts_globaux_par_couche"].items(),
                                      key=lambda kv: int(kv[0])):
            for local, g in enumerate(globaux):
                if (int(couche), g) in vus:
                    raise SystemExit(f"mapping : expert {g} de la couche {couche} "
                                     f"placé deux fois")
                vus[(int(couche), g)] = (c, local)
                lignes.append((int(couche), local, g, c))
    n_couches = len(manifeste.get("experts", {}))
    attendu = n_couches * n_exp
    if len(vus) != attendu:
        raise SystemExit(f"mapping incomplet : {len(vus)} entrées pour "
                         f"{n_couches} couches × {n_exp} experts")
    chemin = os.path.join(dossier, "mapping.tsv")
    with open(chemin, "w", encoding="utf-8") as fo:
        fo.write("# drave-clusters-mapping v1\n")
        fo.write(f"# n_couches {n_couches} · n_experts {n_exp} · clusters {K}"
                 f" · experts_par_cluster {n_exp // K}\n")
        fo.write("# couche\tlocal\tglobal\tcluster\n")
        for couche, local, g, c in lignes:
            fo.write(f"{couche}\t{local}\t{g}\t{c}\n")
    print(f"mapping.tsv · {len(lignes)} entrées · {n_couches} couches · "
          f"{n_exp} experts · {K} clusters")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("dossier")
    ap.add_argument("--clusters", type=int, default=8)
    ap.add_argument("--trace", default="", help="trace de routage (ordre des experts)")
    ap.add_argument("--mode", choices=["experts", "couches"], default="experts")
    ap.add_argument("--verifier", action="store_true",
                    help="relit chaque fichier produit et compare les empreintes")
    args = ap.parse_args()

    t0 = time.time()
    kv_brut, tenseurs, debut_donnees, alignement, n_tensors, version = \
        lire_entete(args.source)
    trace = lire_trace(args.trace) if args.trace else None
    _, arch = parcourir_kv(kv_brut)
    print(f"{os.path.basename(args.source)} : {n_tensors} tenseurs, "
          f"{os.path.getsize(args.source) / 1e9:.1f} Go, arch {arch}, "
          f"alignement {alignement}")

    # ---- répartition des tenseurs
    experts = defaultdict(list)          # couche → tenseurs d'experts
    commun = []
    for t in tenseurs:
        if args.mode == "experts" and "_exps." in t["nom"]:
            couche = int(t["nom"].split(".")[1])
            experts[couche].append(t)
        else:
            commun.append(t)

    ne = 0
    if experts:
        premier = next(iter(experts.values()))[0]
        ne = premier["dims"][0]
        print(f"MoE : {len(experts)} couches × {ne} experts · "
              f"{sum(len(v) for v in experts.values())} tenseurs d'experts")

    os.makedirs(args.dossier, exist_ok=True)
    manifeste = {"source": os.path.abspath(args.source), "mode": args.mode,
                 "clusters": args.clusters, "n_experts": ne,
                 "fichiers": [], "experts": {}}

    # ---- mode « couches » : les blocs sont répartis par groupes de couches
    if args.mode == "couches":
        blocs = defaultdict(list)
        for t in commun:
            if t["nom"].startswith("blk."):
                blocs[int(t["nom"].split(".")[1])].append(t)
        if blocs:
            couches = sorted(blocs)
            par_cluster = (len(couches) + args.clusters - 1) // args.clusters
            noms_blocs = {t["nom"] for l in couches for t in blocs[l]}
            commun = [t for t in commun if t["nom"] not in noms_blocs]
    ecritures_couches = []
    if args.mode == "couches" and blocs:
        for c in range(args.clusters):
            prises = couches[c * par_cluster:(c + 1) * par_cluster]
            if prises:
                ecritures_couches.append((c, prises,
                                          [t for l in prises for t in blocs[l]]))


    # ---- commun.gguf
    if commun:
        chemin = os.path.join(args.dossier, "commun.gguf")
        octets = ecrire_gguf(chemin, kv_brut, commun, args.source, debut_donnees,
                             alignement, [[(t["offset"], t["octets"])] for t in commun])
        manifeste["fichiers"].append({"fichier": "commun.gguf", "role": "commun",
                                      "octets": octets,
                                      "tenseurs": [t["nom"] for t in commun]})
        print(f"commun.gguf      : {len(commun):4} tenseurs · {octets / 1e9:7.2f} Go")

    # ---- un fichier par cluster d'experts
    if experts:
        taille = (ne + args.clusters - 1) // args.clusters
        # par couche, l'ordre des experts vient de la trace
        ordres = {l: ordre_experts(trace, l, ne) for l in experts}
        manifeste["experts"] = {str(l): ordres[l] for l in sorted(ordres)}
        for c in range(args.clusters):
            ids = list(range(c * taille, min(ne, (c + 1) * taille)))
            if not ids:
                break
            nouveaux, morceaux = [], []
            for l in sorted(experts):
                for t in experts[l]:
                    # tranche d'experts : blocs alignés le long de l'axe 0
                    par_expert = t["octets"] // ne
                    assert par_expert * ne == t["octets"], \
                        f"{t['nom']} : la tranche d'expert n'est pas alignée"
                    plages = []
                    for e in ids:
                        global_id = ordres[l][e] if args.mode == "experts" else e
                        plages.append((t["offset"] + global_id * par_expert, par_expert))
                    nouveaux.append({"nom": t["nom"], "dims": [len(ids)] + t["dims"][1:],
                                     "ttype": t["ttype"], "octets": par_expert * len(ids)})
                    morceaux.append(plages)
            chemin = os.path.join(args.dossier, f"cluster-{c:02d}.gguf")
            kv_cluster = kv_brut
            if arch:
                kv_cluster = reecrire_kv(kv_brut, {f"{arch}.expert_count": len(ids)})
            octets = ecrire_gguf(chemin, kv_cluster, nouveaux, args.source, debut_donnees,
                                 alignement, morceaux)
            manifeste["fichiers"].append({
                "fichier": os.path.basename(chemin), "role": f"cluster-{c:02d}",
                "octets": octets, "experts_locaux": len(ids),
                "experts_globaux_par_couche": {str(l): [ordres[l][e] for e in ids]
                                               for l in sorted(experts)}})
            print(f"cluster-{c:02d}.gguf   : {len(nouveaux):4} tenseurs · "
                  f"{octets / 1e9:7.2f} Go · experts locaux 0..{len(ids) - 1}")

    for c, prises, tlist in ecritures_couches:
        chemin = os.path.join(args.dossier, f"cluster-{c:02d}.gguf")
        octets = ecrire_gguf(chemin, kv_brut, tlist, args.source, debut_donnees,
                             alignement, [[(t["offset"], t["octets"])] for t in tlist])
        manifeste["fichiers"].append({
            "fichier": os.path.basename(chemin), "role": f"cluster-{c:02d}",
            "octets": octets, "couches": prises,
            "tenseurs": [t["nom"] for t in tlist]})
        print(f"cluster-{c:02d}.gguf   : {len(tlist):4} tenseurs · "
              f"{octets / 1e9:7.2f} Go · couches {prises[0]}..{prises[-1]}")

    with open(os.path.join(args.dossier, "manifeste.json"), "w", encoding="utf-8") as f:
        json.dump(manifeste, f, indent=1, ensure_ascii=False)
    ecrire_mapping(args.dossier, manifeste)
    total = sum(x["octets"] for x in manifeste["fichiers"])
    print(f"\nmanifeste.json · {len(manifeste['fichiers'])} fichiers · "
          f"{total / 1e9:.2f} Go · {time.time() - t0:.1f} s")

    if args.verifier:
        # Vérification par EMPREINTES : on relit chaque fichier produit, on
        # recalcule l'empreinte de chaque tenseur, et on la compare à celle de la
        # tranche correspondante de la source. Une copie « qui a l'air bonne » ne
        # suffit pas : un décalage d'un bloc passerait inaperçu.
        print("vérification par empreintes…")
        source = open(args.source, "rb")
        erreurs, verifies = [], 0
        for x in manifeste["fichiers"]:
            chemin = os.path.join(args.dossier, x["fichier"])
            kv2, tens2, dd2, _, _, _ = lire_entete(chemin)
            with open(chemin, "rb") as f:
                for t in tens2:
                    f.seek(dd2 + t["offset"])
                    h_produit = hashlib.sha256(f.read(t["octets"])).hexdigest()
                    if not t["nom"].endswith("_exps.weight"):
                        src = next(u for u in tenseurs if u["nom"] == t["nom"])
                        source.seek(debut_donnees + src["offset"])
                        h_source = hashlib.sha256(source.read(src["octets"])).hexdigest()
                    else:
                        # tranche d'experts : on compare bloc à bloc dans la source
                        l = int(t["nom"].split(".")[1])
                        src = next(u for u in tenseurs if u["nom"] == t["nom"])
                        globaux = x.get("experts_globaux_par_couche", {}).get(str(l))
                        if not globaux:
                            continue
                        par_expert = src["octets"] // manifeste["n_experts"]
                        h = hashlib.sha256()
                        f.seek(dd2 + t["offset"])
                        for g in globaux:
                            source.seek(debut_donnees + src["offset"] + g * par_expert)
                            h.update(source.read(par_expert))
                        h_source = h.hexdigest()
                    verifies += 1
                    if h_source != h_produit:
                        erreurs.append(f"{x['fichier']} :: {t['nom']}")
        source.close()
        print(f"  {verifies} tenseurs vérifiés · "
              f"{'TOUT CONCORDE' if not erreurs else 'ÉCARTS : ' + ', '.join(erreurs[:5])}")
        return 1 if erreurs else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
