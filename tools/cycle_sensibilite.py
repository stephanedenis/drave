#!/usr/bin/env python3
"""cycle_sensibilite.py — LE PAS DE TEMPS DU CYCLE EST-IL CONTRACTANT ? (C2)

POURQUOI CETTE MESURE. Le cycle C2 diverge (perplexité 11,84 → 103,06 → 714,61 → 2 873,96 en quatre
pas), et l'hypothèse « c'est une fuite d'échelle » a été **réfutée** le 16/10 : renormer l'état à
chaque pas rend la divergence **~1 000 fois pire** (`rapport-cycle-c2.md` § 6). Ce qui reste n'est donc
pas une question d'**amplitude** mais de **sensibilité** : le pas de temps **amplifie-t-il** une petite
différence, ou l'atténue-t-il ?

CE QUI EST MESURÉ, ET COMMENT. On prend un état d'entrée x, on le fait passer par **un pas complet**
(les régions du cycle, dans l'ordre du plan validé par le moteur), et on compare la sortie de deux
entrées distantes de ε :

    λ = ‖F(x + ε·δ) − F(x)‖ / ‖ε·δ‖        (δ aléatoire de norme 1, graine fixée)

* **λ > 1** : le pas **amplifie** — l'itération ne peut pas converger, et **aucun** objectif
  d'entraînement ne peut y changer quoi que ce soit sans changer λ ✗ (c'est l'explication candidate
  des quatre objectifs qui ont échoué) ;
* **λ < 1** : le pas **contracte** — alors la divergence n'est pas locale, et il faut chercher ailleurs
  (le point de départ, l'entrée, l'accumulation) ;
* on mesure aussi λ pour un pas **composé de plusieurs pas** (λ^k attendu si le régime est linéaire ✗ —
  s'il ne l'est pas, c'est que la non-linéarité domine, et c'est une information de plus).

Usage :
  python tools/cycle_sensibilite.py --topologie /tmp/c2/cycle.json --morceau m32.txt \\
      [--limite 128] [--epsilon 1e-3] [--graine 0] [--pas 1]
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from derouler import ecrire_refd, lire_etats, plan_du_moteur   # noqa: E402


def executer_region(moteur, modele, morceau, limite, threads, couches, etats, travail, nom, env_extra,
                    imposer=True):
    """Exécute UNE région et rend (états de sortie, perplexité).

    `imposer=False` : la région tourne sur SON entrée (l'embarquement du texte), sans état imposé —
    c'est ce qu'il faut pour l'amorce, et c'est aussi ce que fait le premier pas d'un cycle réel.
    """
    refd = travail / f"entree-{nom}.refd"
    if imposer:
        ecrire_refd(refd, etats)
    prefixe = travail / f"etat-{nom}"
    for f in prefixe.parent.glob(prefixe.name + ".*"):
        f.unlink()
    cmd = [moteur, modele, "--ppl", morceau, "--limit", str(limite), "--ctx", str(limite),
           "--threads", str(threads), "--couches", f"{couches[0]}:{couches[1] + 1}",
           "--etat-sortie", str(prefixe),
           # ⚠ `--etat-pos` attend une LISTE d'indices séparés par des virgules (c'est ce que fait
           # `derouler.py`) — pas une plage « 0:64 », qui ne décharge rien et fait échouer la lecture
           # suivante sur un fichier absent.
           "--etat-pos", ",".join(str(p) for p in range(limite))]
    env = {**os.environ, **env_extra}
    if imposer:
        env["DRAVE_ETAT_ENTREE"] = str(refd)
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise SystemExit(f"région {nom} : code {r.returncode}\n{r.stderr[-400:]}")
    m = re.search(r"perplexité ([0-9.]+) sur", r.stdout + r.stderr)
    return lire_etats(prefixe, list(range(limite))), (float(m.group(1)) if m else float("nan"))


def un_pas(a, regions, ordre, x, travail, nom, amorce=False):
    """UN PAS COMPLET du cycle : les régions dans l'ordre du plan, chacune recevant l'état de la
    précédente. C'est exactement ce que fait `derouler.py`, mais sur un état IMPOSÉ — ce qui permet
    de comparer deux entrées distantes de ε."""
    courant = x
    ppl = float("nan")
    for i, rid in enumerate(ordre):
        r = regions[rid]
        courant, ppl = executer_region(a.moteur, a.modele, a.morceau, a.limite, a.threads,
                                       r["couches"], courant, travail, f"{nom}-{i}", {},
                                       imposer=not (amorce and i == 0))
    return courant, ppl


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topologie", required=True)
    ap.add_argument("--morceau", required=True)
    ap.add_argument("--limite", type=int, default=128)
    ap.add_argument("--epsilon", type=float, default=1e-3)
    ap.add_argument("--graine", type=int, default=0)
    ap.add_argument("--pas", type=int, default=1, help="nombre de pas composés (λ mesuré sur la composition)")
    ap.add_argument("--moteur", default="./drave-core/target/release/drave")
    ap.add_argument("--modele", default="models/Qwen2.5-0.5B-Q8_0.gguf")
    ap.add_argument("--threads", type=int, default=8)
    a = ap.parse_args()

    import json
    topo = json.loads(pathlib.Path(a.topologie).read_text())
    regions = {r["id"]: r for r in topo["regions"]}
    ordre, _ = plan_du_moteur(a.moteur, a.modele, a.topologie)
    print(f"cycle : ordre d'un pas = {' '.join(ordre)}")

    travail = pathlib.Path(tempfile.mkdtemp(prefix="cycle-sens-"))
    try:
        # L'ÉTAT DE DÉPART : celui que le cycle produit lui-même au premier pas (on ne part donc pas
        # d'un état arbitraire, mais d'un état RÉEL du cycle).
        ids = [int(x) for x in pathlib.Path(a.morceau).read_text().replace("\n", ",").split(",") if x.strip()]
        x0, _ = executer_region(a.moteur, a.modele, a.morceau, a.limite, a.threads,
                                regions[ordre[0]]["couches"], None, travail, "amorce", {},
                                imposer=False)
        x0, ppl0 = un_pas(a, regions, ordre, x0, travail, "base")   # un VRAI pas du cycle
        print(f"état de départ : {len(x0)} positions × {x0[0].shape[0]} · perplexité {ppl0:,.4f}")

        rng = np.random.default_rng(a.graine)
        delta = [rng.standard_normal(e.shape).astype("<f4") for e in x0]
        n = float(np.sqrt(sum(float((d ** 2).sum()) for d in delta)))
        delta = [d / n for d in delta]
        x1 = [e + a.epsilon * d for e, d in zip(x0, delta)]

        for k in (1, a.pas) if a.pas > 1 else (1,):
            y0, ppl_a = un_pas(a, regions, ordre, x0, travail, f"y0-{k}")
            for _ in range(k - 1):
                y0, _ = un_pas(a, regions, ordre, y0, travail, f"y0-{k}")
            y1, ppl_b = un_pas(a, regions, ordre, x1, travail, f"y1-{k}")
            for _ in range(k - 1):
                y1, _ = un_pas(a, regions, ordre, y1, travail, f"y1-{k}")
            ecart_entree = float(np.sqrt(sum(float(((b - c) ** 2).sum()) for b, c in zip(x1, x0))))
            ecart_sortie = float(np.sqrt(sum(float(((b - c) ** 2).sum()) for b, c in zip(y1, y0))))
            lam = ecart_sortie / ecart_entree
            print(f"  {k} pas : écart d'entrée {ecart_entree:.3e} → écart de sortie {ecart_sortie:.3e}"
                  f" · λ = {lam:.4f}" + (f" (λ^(1/{k}) = {lam ** (1 / k):.4f})" if k > 1 else ""))
            print(f"      perplexité : {ppl_a:,.2f} (entrée x) contre {ppl_b:,.2f} (entrée x + ε·δ)"
                  f" — soit {abs(ppl_b - ppl_a) / ppl_a * 100:.4f} % pour une perturbation de {a.epsilon:g}")

        print()
        print("  λ > 1 : le pas AMPLIFIE — aucune itération ne peut converger, et aucun objectif")
        print("          d'entraînement n'y changera rien sans changer λ.")
        print("  λ < 1 : le pas CONTRACTE — la divergence n'est pas locale, chercher ailleurs.")
    finally:
        shutil.rmtree(travail, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
