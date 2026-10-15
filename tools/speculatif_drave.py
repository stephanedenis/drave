#!/usr/bin/env python3
"""speculatif_drave.py — LE RÉFLEXE PROPOSE, LE CERVEAU VÉRIFIE — et on mesure le taux.

POURQUOI CE FICHIER EXISTE, ET CE QU'IL AJOUTE. `tools/speculatif.py` (8 oct) mesure le taux
d'acceptation entre **deux modèles HuggingFace** (un 0,5B pour un 1,5B) : c'est la mesure *avant*
d'écrire du moteur. Depuis la nuit du 14-15/10, il y a **autre chose à mesurer** : un **réflexe
entraîné dans ce dépôt** — le chemin court (8 couches sur 24) avec un lecteur appris ou un LoRA
distillé, exporté en GGUF, lu **par le moteur** — qui génère **deux fois plus vite** que le cerveau
entier mais ne produit **pas** le même texte (accord par position : 28 % à la perplexité, 51 %
distillé ; 0 à 5 jetons sur 96 en génération libre).

La question qui restait : **à quoi sert un réflexe qui se trompe ?** Réponse : à **proposer**. Le
réflexe propose K jetons, le cerveau en vérifie K **en une passe**, garde le préfixe ratifié et
corrige le premier jeton faux. C'est le décodage spéculatif — et la seule quantité qui décide de
son intérêt est le **taux d'acceptation**, mesuré ici **dans le moteur**, avec les modèles du dépôt.

CE QUI EST MESURÉ, par bras de brouillon :
  · le **taux d'acceptation** (jetons ratifiés / jetons proposés) — l'accord réflexe/cerveau mesuré
    **sans aucune sonde** : deux générations gourmandes comparées jeton à jeton ;
  · les **jetons par vérification** (1 + acceptés) : c'est le gain brut du décodage ;
  · le **temps**, brut, **avec** le chargement du modèle à chaque appel (le pilote relance le
    moteur à chaque tour : c'est lent et c'est dit — le taux, lui, n'en dépend pas).

Usage :
  python tools/speculatif_drave.py --n 24 --K 4 \\
      --brouillon "models/Qwen2.5-0.5B-Q8_0.gguf --couches 0:8 --tete-partielle" \\
      --brouillon "/tmp/n4/e5-distille.gguf --couches 0:8 --tete-partielle --adaptateur-sortie /tmp/n4/e5-adaptateur.f32"
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import time

MOTIF = re.compile(r"(?:tokens|ids) générés : \[([0-9,\s]*)\]")


def generer(moteur: str, modele: str, drapeaux: list[str], seq: list[int], k: int,
            travail: pathlib.Path) -> tuple[list[int], float]:
    """k jetons gourmands depuis `seq`, produits par le MOTEUR (aucun modèle en Python)."""
    f = travail / "sequence.ids"
    f.write_text(",".join(str(x) for x in seq))
    t = time.time()
    p = subprocess.run([moteur, modele, "--infer", "--ids-file", str(f), "--n", str(k),
                        "--ctx", "512", "--threads", "8", "--temp", "0"] + drapeaux,
                       capture_output=True, text=True, timeout=900)
    dt = time.time() - t
    m = MOTIF.search(p.stdout)
    if not m:
        raise SystemExit(f"  ❌ le moteur n'a pas rendu de jetons :\n{p.stdout[-300:]}\n{p.stderr[-300:]}")
    return [int(x) for x in re.findall(r"[0-9]+", m.group(1))], dt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--moteur", default="./drave-core/target/release/drave")
    ap.add_argument("--verifieur", default="models/Qwen2.5-0.5B-Q8_0.gguf")
    ap.add_argument("--invite", default="Le ciel est bleu parce que")
    ap.add_argument("--n", type=int, default=24, help="jetons à produire")
    ap.add_argument("--K", type=int, default=4, help="jetons proposés par tour")
    ap.add_argument("--brouillon", action="append", default=[],
                    help="« MODELE DRAPEAUX… » — répétable : un bras par brouillon")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    travail = pathlib.Path("/tmp/speculatif-drave")
    travail.mkdir(parents=True, exist_ok=True)
    # L'invite est tokenisée UNE fois par le moteur, puis TOUT se fait en identifiants : un
    # aller-retour texte → jetons → texte ne redonne pas toujours la même suite, et le pilote
    # n'a aucune raison de passer par le texte après le premier pas.
    txt = travail / "invite.txt"
    txt.write_text(a.invite)
    subprocess.run([a.moteur, a.verifieur, "--tokenize", "--fichier", str(txt),
                    "--sortie", str(travail / "invite.ids")], capture_output=True, text=True)
    depart = [int(x) for x in re.findall(r"[0-9]+", (travail / "invite.ids").read_text())]
    print(f"invite : {len(depart)} jetons · {a.n} jetons à produire · K = {a.K}")

    bras = a.brouillon or [f"{a.verifieur} --couches 0:8 --tete-partielle"]
    resultats = {}
    for spec in bras:
        morceaux = spec.split()
        modele, drapeaux = morceaux[0], morceaux[1:]
        nom = pathlib.Path(modele).name + (" " + " ".join(drapeaux) if drapeaux else "")
        seq, generes, proposes, acceptes, tours, secondes = list(depart), [], 0, 0, 0, 0.0
        while len(generes) < a.n:
            k = min(a.K, a.n - len(generes))
            prop, t1 = generer(a.moteur, modele, drapeaux, seq, k, travail)
            vrai, t2 = generer(a.moteur, a.verifieur, [], seq, k, travail)
            secondes += t1 + t2
            accord = 0
            for x, y in zip(prop, vrai):
                if x != y:
                    break
                accord += 1
            proposes += len(prop)
            acceptes += accord
            tours += 1
            generes.extend(prop[:accord])
            if accord < len(vrai):
                generes.append(vrai[accord])          # la CORRECTION : le jeton du cerveau
            elif len(generes) < a.n:
                suite, t3 = generer(a.moteur, a.verifieur, [], seq + prop, 1, travail)
                secondes += t3
                generes.extend(suite)
            seq = list(depart) + generes
            print(f"    tour {tours:>2} : proposé {prop} · cerveau {vrai} · ratifiés {accord}/{len(prop)}")
        taux = acceptes / max(proposes, 1)
        resultats[nom] = {"taux_acceptation": taux, "jetons_par_verification": len(generes) / max(tours, 1),
                          "proposes": proposes, "acceptes": acceptes, "tours": tours,
                          "secondes": secondes, "generes": generes}
        print(f"  → {nom}\n     taux d'acceptation **{taux * 100:.1f} %** ({acceptes}/{proposes}) · "
              f"{len(generes) / max(tours, 1):.2f} jetons par vérification · "
              f"{secondes:.1f} s pour {len(generes)} jetons\n")

    print("| brouillon (réflexe) | taux d'acceptation | jetons / vérification | temps |")
    print("|---|---:|---:|---:|")
    for nom, r in resultats.items():
        print(f"| `{nom}` | **{r['taux_acceptation'] * 100:.1f} %** | {r['jetons_par_verification']:.2f} | "
              f"{r['secondes']:.1f} s |")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(resultats, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
