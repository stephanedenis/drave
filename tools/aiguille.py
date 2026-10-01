#!/usr/bin/env python3
"""Aiguille dans la botte de foin — version 2, celle qui mesure vraiment.

La perplexité ne dit pas si un modèle RETROUVE une information. Ce script plante
un code à une profondeur donnée dans un contexte long, puis le redemande.

Ce qui a changé par rapport à la v1 (mesurée et arrêtée) :

1. **le remplissage est du vrai texte VARIÉ** (`data/wikitext2_test.txt`), et non
   la même phrase recopiée jusqu'à la longueur voulue. Un remplissage répété ne
   teste rien : le modèle pouvait répondre en devinant la structure. Chaque sonde
   prend en plus une FENÊTRE DIFFÉRENTE du corpus, pour que les sondes ne
   partagent pas leur remplissage ;
2. **la réponse est longue** (`--n 40` par défaut) : un code peut sortir au
   deuxième ou troisième jeton, et s'arrêter à 8 jetons faisait échouer des
   sondes que le modèle savait résoudre ;
3. **le préremplissage par lots** (`--lot`) rend chaque sonde abordable : le
   moteur ne l'utilisait que pour la perplexité ;
4. le contexte réellement atteint est **lu dans la sortie du moteur** (le
   tokenizer ne fait pas 4 caractères par jeton pour tout le monde), et une
   sonde n'est comptée que si le contexte demandé a bien été construit.

Usage :
    aiguille.py <modele.gguf> <longueurs> <profondeurs> [options]

Exemples :
    aiguille.py models/Qwen2.5-1.5B-Q4_K_M.gguf 1024,2048 0.1,0.5,0.9 --lot 256
    aiguille.py /chemin/gpt-oss-120b-MXFP4.gguf 4096 0.1,0.5,0.9 --lot 512 --gpu
"""
import argparse
import os
import re
import subprocess
import sys
import time

Q = "./drave-core/target/release/drave"
CORPUS = "data/wikitext2_test.txt"
CODE = "AZUR-7391"
AIGUILLE = f" Pour memoire, le code de verification de la reunion est {CODE}. "
QUESTION = ("Quel est le code de verification de la reunion ? "
            "Reponds par le code seul, puis une phrase d'explication.")


def charger_corpus():
    texte = open(CORPUS, encoding="utf-8", errors="replace").read()
    # WikiText-2 garde des artefacts (« @-@ », titres, espaces multiples) : on
    # normalise pour que le remplissage ressemble à du texte ordinaire.
    texte = texte.replace("@-@", "-").replace("@,@", ",").replace("@.@", ".")
    return " ".join(texte.split())


def sonde(modele, corpus, ctx, profondeur, offset, args):
    """Une sonde. `offset` décale la fenêtre de corpus pour varier le texte."""
    # Les tokenizers anglais tournent autour de 4,2 caractères par jeton ; la
    # longueur exacte est relue dans la sortie du moteur.
    cible = int(ctx * 4.2)
    besoin = cible + 400
    if offset + besoin > len(corpus):
        offset = 0
    remplissage = corpus[offset:offset + besoin]
    coupe = int(len(remplissage) * profondeur)
    # On coupe sur un espace pour ne pas hacher un mot.
    while coupe < len(remplissage) and remplissage[coupe] != " ":
        coupe += 1
    texte = remplissage[:coupe] + AIGUILLE + remplissage[coupe:]
    invite = texte + "\n\n" + QUESTION

    env = dict(os.environ)
    if args.gpu:
        env["DRAVE_GPU"] = "1"
    if args.gpu_kv:
        env["DRAVE_GPU"] = "1"
        env["DRAVE_GPU_KV"] = "1"
    if args.gpu_topk:
        env["DRAVE_GPU"] = "1"
        env["DRAVE_GPU_KV"] = "1"
        env["DRAVE_GPU_TOPK"] = "1"
    cmd = [Q, modele, "--infer", "--chat", "--flux", "--prompt", invite,
           "--n", str(args.n), "--ctx", str(ctx + 512), "--threads", str(args.threads),
           "--temp", "0", "--lot", str(args.lot)]
    if args.attn_topk > 0:
        cmd += ["--attn-topk", str(args.attn_topk)]
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=args.timeout,
                           env=env)
    except subprocess.TimeoutExpired:
        return None, time.time() - t0, "délai dépassé"
    sortie = r.stdout + r.stderr
    # Le moteur DIT quand un drapeau ne s'applique pas (« --attn-topk ... est
    # IGNORÉ en mode lot ») ; l'outil jetait ce message, et la grille a été
    # interprétée comme si l'attention creuse valait pour tout le passage. On le
    # remonte dans le détail de la sonde.
    avert = ""
    for ligne in sortie.splitlines():
        if "IGNORÉ" in ligne or "inactif" in ligne.lower():
            avert = " · " + ligne.strip()[:110]
            break
    m = re.search(r"prompt\s*:\s*(\d+) tokens", sortie)
    n_prompt = int(m.group(1)) if m else 0
    if n_prompt == 0:
        # Le moteur n'a pas démarré (chemin de modèle, option refusée…) : le
        # dire, au lieu de compter la sonde comme un échec du MODÈLE.
        premiere = next((l for l in sortie.splitlines() if l.strip()), "(aucune sortie)")
        return None, time.time() - t0, f"moteur muet : {premiere.strip()[:120]}"
    # Le texte GÉNÉRÉ : tout ce qui suit le marqueur de fin de prompt.
    corps = sortie.split("ids générés")[0]
    if "assistant" in corps:
        corps = corps.rsplit("assistant", 1)[-1]
    trouve = CODE in corps
    dt = time.time() - t0
    detail = f"prompt {n_prompt} jetons{avert}"
    return trouve, dt, detail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("modele")
    ap.add_argument("longueurs")
    ap.add_argument("profondeurs")
    ap.add_argument("--n", type=int, default=40, help="jetons générés (réponse)")
    ap.add_argument("--threads", type=int, default=16)
    ap.add_argument("--lot", type=int, default=256, help="lot de préremplissage")
    ap.add_argument("--timeout", type=int, default=7200)
    ap.add_argument("--gpu", action="store_true", help="DRAVE_GPU=1 (déport des projections)")
    ap.add_argument("--gpu-kv", action="store_true", help="DRAVE_GPU=1 DRAVE_GPU_KV=1 (KV en VRAM)")
    # Croisement avec l'attention creuse : le sprint 2 a rendu le top-k déporté
    # plus rapide que le CPU dès ~300 clés, mais la question qui compte pour la
    # MISSION n'est pas la vitesse : une attention qui ne garde que k clés
    # RETROUVE-T-ELLE encore l'information plantée à 4 k / 8 k / 16 k ?
    ap.add_argument("--attn-topk", type=int, default=0,
                    help="--attn-topk N (0 = attention complète)")
    ap.add_argument("--gpu-topk", action="store_true",
                    help="DRAVE_GPU=1 DRAVE_GPU_KV=1 DRAVE_GPU_TOPK=1")
    ap.add_argument("--journal", default="")
    args = ap.parse_args()
    # `--gpu-topk` sans `--attn-topk` affichait « top-k déporté » alors que le
    # moteur ne fait RIEN (il n'imprime qu'un conditionnel au chargement) : une
    # valeur affichée qui n'agit pas, exactement ce que ce dépôt traque.
    if args.gpu_topk and args.attn_topk <= 0:
        ap.error("--gpu-topk exige --attn-topk N (sinon le moteur ne déporte rien)")
    if args.attn_topk < 0:
        ap.error("--attn-topk doit être positif (0 = attention complète)")

    corpus = charger_corpus()
    longueurs = [int(x) for x in args.longueurs.split(",")]
    profondeurs = [float(x) for x in args.profondeurs.split(",")]
    print(f"aiguille v2 : {args.modele}")
    print(f"  remplissage : {CORPUS} ({len(corpus)} caractères), fenêtres décalées")
    topk = f" · attn-topk {args.attn_topk}" if args.attn_topk else " · attention COMPLÈTE"
    gpu = ("top-k déporté" if args.gpu_topk
           else ("KV " if args.gpu_kv else ("proj " if args.gpu else "non")))
    print(f"  lot {args.lot} · {args.n} jetons de réponse · GPU {gpu}{topk}")
    print(f"{'contexte':>9} {'profondeur':>11} {'trouvé':>7} {'secondes':>9}  détail")
    lignes = []
    offset = 0
    for ctx in longueurs:
        for p in profondeurs:
            ok, dt, detail = sonde(args.modele, corpus, ctx, p, offset, args)
            offset += 200_000          # fenêtre différente à chaque sonde
            if offset > len(corpus) - 400_000:
                offset = 0
            etat = "délai" if ok is None else ("oui" if ok else "NON")
            print(f"{ctx:>9} {p:>11.2f} {etat:>7} {dt:>9.1f}  {detail}", flush=True)
            lignes.append((ctx, p, etat, dt, detail))
    if args.journal:
        with open(args.journal, "w", encoding="utf-8") as f:
            f.write(f"# aiguille v2 — {args.modele}\n")
            f.write(f"lot {args.lot}, {args.n} jetons de réponse, {args.threads} fils, "
                    f"{'attn-topk ' + str(args.attn_topk) if args.attn_topk else 'attention complète'}, "
                    f"GPU {'top-k déporté' if args.gpu_topk else ('KV' if args.gpu_kv else ('proj' if args.gpu else 'non'))}\n\n")
            f.write("| contexte | profondeur | trouvé | secondes | détail |\n")
            f.write("|---|---|---|---|---|\n")
            for ctx, p, etat, dt, detail in lignes:
                f.write(f"| {ctx} | {p} | **{etat}** | {dt:.1f} | {detail} |\n")
        print(f"journal : {args.journal}")


if __name__ == "__main__":
    sys.exit(main())
