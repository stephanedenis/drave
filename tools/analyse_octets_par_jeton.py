#!/usr/bin/env python3
"""analyse_octets_par_jeton.py — combien d'octets de POIDS un jeton fait-il lire ?

Lit l'en-tête d'un GGUF (sans lire les données), repère les tenseurs d'experts,
et calcule le volume lu par jeton :

    octets/jeton = Σ_couches [ (k_routés / n_experts) × octets(exps)
                               + octets(expert partagé) ]

C'est le chiffre qui décide de trois choses :
  - si un modèle tient en RAM (sinon chaque passe relit ces octets du disque) ;
  - ce que coûterait un chemin GPU qui streame les poids (PCIe) au lieu de les
    garder en VRAM ;
  - ce que coûte un découpage en nœuds (chaque nœud ne lit que sa part).

Usage : analyse_octets_par_jeton.py <modele.gguf> [--experts-par-jeton N]
                                    [--tous]
"""
import struct
import sys

# Éléments par bloc et octets par bloc des formats ggml (le strict nécessaire ;
# un type absent est signalé, jamais deviné).
TYPES = {
    0: ("F32", 1, 4), 1: ("F16", 1, 2), 2: ("Q4_0", 32, 18), 3: ("Q4_1", 32, 20),
    6: ("Q5_0", 32, 22), 7: ("Q5_1", 32, 24), 8: ("Q8_0", 32, 34), 9: ("Q8_1", 32, 36),
    10: ("Q2_K", 256, 84), 11: ("Q3_K", 256, 110), 12: ("Q4_K", 256, 144),
    13: ("Q5_K", 256, 176), 14: ("Q6_K", 256, 210), 15: ("Q8_K", 256, 292),
    16: ("IQ2_XXS", 256, 66), 17: ("IQ2_XS", 256, 74), 18: ("IQ3_XXS", 256, 98),
    19: ("IQ1_S", 256, 50), 20: ("IQ4_NL", 32, 18), 21: ("IQ3_S", 256, 110),
    22: ("IQ2_S", 256, 82), 23: ("IQ4_XS", 256, 136), 24: ("I8", 1, 1),
    25: ("I16", 1, 2), 26: ("I32", 1, 4), 27: ("I64", 1, 8), 28: ("F64", 1, 8),
    29: ("IQ1_M", 256, 56), 30: ("BF16", 1, 2),
    # 39 = MXFP4 (32 poids = 1 octet d'exposant + 16 octets de 4 bits),
    # le format des experts de gpt-oss — et de quelques tenseurs de V4-Flash.
    39: ("MXFP4", 32, 17),
}

TAILLE_SCALAIRE = {0: 1, 1: 1, 2: 2, 3: 2, 4: 4, 5: 4, 6: 4, 7: 1,
                   10: 8, 11: 8, 12: 8}


class Lecteur:
    def __init__(self, chemin):
        self.f = open(chemin, "rb")

    def lire(self, n):
        d = self.f.read(n)
        if len(d) != n:
            raise EOFError(f"en-tête tronqué ({len(d)} < {n})")
        return d

    def scalaire(self, t):
        n = TAILLE_SCALAIRE[t]
        brut = self.lire(n)
        return struct.unpack({1: "<b", 2: "<H", 3: "<h", 4: "<I", 5: "<i", 6: "<f",
                              7: "<?", 10: "<Q", 11: "<q", 12: "<d"}[t], brut)[0]

    def chaine(self):
        n = struct.unpack("<Q", self.lire(8))[0]
        return self.lire(n).decode("utf-8", "replace")

    def valeur(self, t):
        if t == 8:
            return self.chaine()
        if t == 9:
            te = struct.unpack("<I", self.lire(4))[0]
            n = struct.unpack("<Q", self.lire(8))[0]
            return [self.valeur(te) for _ in range(n)]
        return self.scalaire(t)


def lire_entete(chemin):
    l = Lecteur(chemin)
    magie = l.lire(4)
    assert magie == b"GGUF", f"{chemin} : ce n'est pas un GGUF ({magie!r})"
    version = struct.unpack("<I", l.lire(4))[0]
    n_tensors, n_kv = struct.unpack("<QQ", l.lire(16))
    for _ in range(n_kv):
        l.chaine()
        t = struct.unpack("<I", l.lire(4))[0]
        l.valeur(t)
    tenseurs = []
    for _ in range(n_tensors):
        nom = l.chaine()
        nd = struct.unpack("<I", l.lire(4))[0]
        dims = [struct.unpack("<Q", l.lire(8))[0] for _ in range(nd)]
        ttype = struct.unpack("<I", l.lire(4))[0]
        l.lire(8)  # décalage dans le fichier
        tenseurs.append((nom, dims, ttype))
    return version, tenseurs


def octets(dims, ttype):
    n = 1
    for d in dims:
        n *= d
    if ttype not in TYPES:
        raise KeyError(f"type ggml {ttype} inconnu de ce script")
    _, par_bloc, taille_bloc = TYPES[ttype]
    return n // par_bloc * taille_bloc, TYPES[ttype][0]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    chemin = sys.argv[1]
    k = 6
    if "--experts-par-jeton" in sys.argv:
        k = int(sys.argv[sys.argv.index("--experts-par-jeton") + 1])
    version, tenseurs = lire_entete(chemin)
    print(f"{chemin} : version {version}, {len(tenseurs)} tenseurs")

    exps = {}   # couche -> octets des tenseurs *_exps (gate+up+down)
    shexp = {}  # couche -> octets de l'expert partagé
    formats = {}
    total = 0
    for nom, dims, ttype in tenseurs:
        o, fmt = octets(dims, ttype)
        total += o
        formats[fmt] = formats.get(fmt, 0) + o
        parties = nom.split(".")
        if len(parties) >= 3 and parties[0] == "blk":
            couche = int(parties[1])
            if "exps" in nom:
                exps[couche] = exps.get(couche, 0) + o
            elif "shexp" in nom:
                shexp[couche] = shexp.get(couche, 0) + o
    if not exps:
        print("aucun tenseur d'experts : modèle dense, rien à calculer")
        return 0
    n_experts = None
    for nom, dims, _ in tenseurs:
        if "exps" in nom and len(dims) == 3:
            n_experts = dims[2]
            break
    n_experts = n_experts or 256
    par_jeton = sum((k / n_experts) * o for o in exps.values()) + sum(shexp.values())
    print(f"\n{len(exps)} couches à experts · {n_experts} experts · {k} routés par jeton")
    print(f"  poids totaux du fichier      : {total/1e9:8.2f} Go")
    print(f"  dont experts (toutes couches): {sum(exps.values())/1e9:8.2f} Go")
    print(f"  dont expert partagé          : {sum(shexp.values())/1e9:8.2f} Go")
    print(f"  formats                      : " +
          " · ".join(f"{f} {o/1e9:.2f} Go" for f, o in
                     sorted(formats.items(), key=lambda x: -x[1])[:6]))
    print(f"\n  ⇒ OCTETS DE POIDS PAR JETON  : {par_jeton/1e9:8.3f} Go")
    print(f"     à 6,5 Go/s sur le bus (PCIe x8, chiffre du dépôt) : "
          f"{par_jeton/6.5e9*1e3:6.0f} ms/jeton")
    print(f"     à 20 Go/s (lecture CPU mesurée)                   : "
          f"{par_jeton/20e9*1e3:6.0f} ms/jeton")
    print(f"     à 200 Mo/s (disque dur, lectures non cachées)     : "
          f"{par_jeton/200e6:6.1f} s/jeton")
    if "--tous" in sys.argv:
        print("\n  détail par couche (Go) : experts · partagé")
        for c in sorted(exps):
            print(f"    couche {c:3d} : {exps[c]/1e9:7.3f} · {shexp.get(c, 0)/1e9:7.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
