#!/usr/bin/env python3
"""Compare notre déquantification d'un super-bloc à celle de **libggml**.

    tools/verifier_formats.py <modele.gguf> <tenseur> [index] [--type N]

La référence est la bibliothèque ggml elle-même (`tools/ref_ggml_bloc.c`), pas
une seconde lecture du format écrite ici : une réimplémentation Python partage
les mêmes erreurs de lecture et validerait un déquantificateur faux — c'est
exactement ce qui est arrivé pour IQ2_XXS (pas de 8 octets sur `qs` au lieu de
4), IQ1_M (échelles lues en premier alors qu'elles sont en dernier) et Q2_K
(mauvais indice d'échelle).

Le côté Rust est interrogé par `drave <modele> --bloc <tenseur>:<index>`, qui
passe par `row_f32` — le chemin du chargement réel du modèle. Vérifier un
déquantificateur par un chemin qui n'est pas celui du moteur ne prouve rien.

Sortie : écart max et verdict ; code de retour 1 si divergence.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyse_experts_statique import Lecteur  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRAVE = os.path.join(RACINE, "drave-core/target/release/drave")
REF = os.environ.get("REF_GGML_BLOC", "/tmp/ref_ggml_bloc")

# Octets par super-bloc de 256 poids, pour les types que nous savons lire.
OCTETS_256 = {
    0: 1024,   # F32
    1: 512,    # F16
    2: 144,    # Q4_0   : 18 o / 32 poids
    3: 160,    # Q4_1   : 20 o / 32
    6: 176,    # Q5_0   : 22 o / 32
    7: 192,    # Q5_1   : 24 o / 32
    8: 272,    # Q8_0   : 34 o / 32
    10: 84,    # Q2_K
    11: 110,   # Q3_K
    12: 144,   # Q4_K
    13: 176,   # Q5_K
    14: 210,   # Q6_K
    16: 66,    # IQ2_XXS
    18: 98,    # IQ3_XXS
    19: 50,    # IQ1_S
    23: 136,   # IQ4_XS
    29: 56,    # IQ1_M
    30: 512,   # BF16
    39: 136,   # MXFP4  : 17 o / 32
}


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    modele, nom = sys.argv[1], sys.argv[2]
    index = 0
    type_force = None
    reste = sys.argv[3:]
    while reste:
        a = reste.pop(0)
        if a == "--type":
            type_force = int(reste.pop(0))
        else:
            index = int(a)
    lect = Lecteur(modele)
    if nom not in lect.tenseurs:
        proches = [k for k in lect.tenseurs if nom in k][:5]
        print(f"tenseur « {nom} » absent de {modele}"
              + (f" — proches : {proches}" if proches else ""))
        return 2
    dims, ttype, offset = lect.tenseurs[nom]
    if type_force is not None:
        ttype = type_force
    if ttype not in OCTETS_256:
        print(f"type {ttype} non couvert par ce vérificateur (voir OCTETS_256)")
        return 2
    bloc = OCTETS_256[ttype]
    debut = lect.debut + offset + index * bloc
    ref = subprocess.run([REF, modele, str(debut), str(ttype)],
                         capture_output=True, text=True)
    if ref.returncode != 0:
        print("référence ggml en échec :", ref.stderr.strip()[:300])
        return 2
    attendu = [float(x) for x in ref.stdout.split()]
    nous = subprocess.run([DRAVE, modele, "--bloc", f"{nom}:{index}"],
                          capture_output=True, text=True)
    vals = [float(l) for l in nous.stdout.splitlines()
            if l.strip() and not l.startswith("tenseur")]
    if not vals:
        print("drave n'a rien rendu :", (nous.stderr.strip() or nous.stdout)[:300])
        return 2
    n = min(len(attendu), len(vals))
    ecart = max(abs(a - b) for a, b in zip(attendu[:n], vals[:n]))
    echelle = max(abs(a) for a in attendu[:n]) or 1.0
    print(f"{nom} · dims {dims} · type {ttype} · bloc {index}")
    print(f"  ggml  8 : {[f'{v:.6f}' for v in attendu[:8]]}")
    print(f"  nous  8 : {[f'{v:.6f}' for v in vals[:8]]}")
    print(f"  {n} valeurs · écart max {ecart:.2e} (échelle {echelle:.2e})")
    ok = ecart < 1e-6
    print("CONCORDE" if ok else "DIVERGE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
