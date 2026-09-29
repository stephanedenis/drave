#!/usr/bin/env python3
"""Aiguille dans la botte de foin : la seule mesure de qualité qui compte à
contexte long (la perplexité ne dit pas si le modèle RETROUVE une information).

Le contexte est un texte de remplissage ; l'aiguille est une phrase absurde
plantée à une profondeur donnée ; la question est posée APRÈS le texte. On
compte le nombre de sondes où le code exact de l'aiguille réapparaît.

Usage : aiguille.py <modele.gguf> <longueurs> <profondeurs> [--n 32]
"""
import subprocess, sys, time

Q = "./qtrinet-core/target/release/qtrinet-core"
REMPLISSAGE = ("Le service de documentation conserve les comptes rendus des "
               "reunions trimestrielles du comite. Chaque compte rendu rappelle "
               "les decisions prises et les actions a mener. ")

def sonde(modele, ctx, profondeur, n=32, threads=8):
    code = "AZUR-7391"
    aiguille = f" Le code de verification de la reunion est {code}. "
    # Le texte est découpé en phrases ; l'aiguille est insérée à la profondeur
    # demandée, puis la question est posée à la fin.
    cible = int(ctx * profondeur)
    avant = REMPLISSAGE * (cible // 20 + 1)
    apres = REMPLISSAGE * ((ctx - cible) // 20 + 1)
    texte = avant + aiguille + apres
    question = "Quel est le code de verification de la reunion ? Reponds par le code seul."
    t0 = time.time()
    r = subprocess.run([Q, modele, "--infer", "--chat", "--flux",
                        "--prompt", texte + "\n" + question,
                        "--n", str(n), "--ctx", str(ctx + 512),
                        "--threads", str(threads), "--temp", "0"],
                       capture_output=True, text=True, timeout=7200)
    sortie = r.stdout + r.stderr
    trouve = code in sortie.split("prompt :")[-1]
    return trouve, time.time() - t0, sortie

def main():
    modele = sys.argv[1]
    longueurs = [int(x) for x in sys.argv[2].split(",")]
    profondeurs = [float(x) for x in sys.argv[3].split(",")]
    print(f"aiguille : {modele}")
    print(f"{'contexte':>9} {'profondeur':>11} {'trouvé':>7} {'secondes':>9}")
    for ctx in longueurs:
        for p in profondeurs:
            try:
                ok, dt, _ = sonde(modele, ctx, p)
            except subprocess.TimeoutExpired:
                ok, dt = False, float("nan")
            print(f"{ctx:>9} {p:>11.2f} {'oui' if ok else 'NON':>7} {dt:>9.1f}", flush=True)

if __name__ == "__main__":
    main()
