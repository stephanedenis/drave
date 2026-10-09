#!/usr/bin/env python3
"""speculatif_moteur.py — le taux d'acceptation, mesuré PAR LE MOTEUR, sur des GGUF.

POURQUOI UN DEUXIÈME OUTIL. `tools/speculatif.py` mesure l'acceptation avec
HuggingFace, en fp16, sur des modèles téléchargés — et le rapport en a tiré
« ×1,20, insuffisant ». Mais Drave n'exécute pas des modèles fp16 : il exécute
des GGUF quantifiés, dont le coût par pas est proportionnel aux OCTETS, pas aux
paramètres. Le rapport de coût brouillon/cible qui décide du gain net n'est donc
pas celui de HF. Ici, les deux modèles sont ceux du disque, exécutés par le
moteur, et le rapport de coût est MESURÉ (tok/s des deux côtés).

CE QUI EST MESURÉ, EXACTEMENT. `--infer --prompt` imprime
`--- ids générés : [..]`, la suite d'identifiants produite en décodage glouton
(`--temp 0`). On ne re-tokenise donc rien : les deux suites sont comparées
identifiant par identifiant. Le préfixe commun donne, pour chaque position, le
nombre de jetons que le brouillon aurait fait accepter.

LE CONTRÔLE QUI REND LE CHIFFRE CRÉDIBLE. Le brouillon et la cible doivent
partager leur vocabulaire, sinon la comparaison ne mesure rien : l'outil le
VÉRIFIE (même texte → mêmes identifiants) et refuse de conclure si ce n'est pas
le cas.

Usage :
    speculatif_moteur.py --brouillon D.gguf --cible C.gguf [--n 48] [--k 8]
                         [--prompts 8] [--threads 20] [--journal sortie.log]
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

MOTEUR = "./drave-core/target/release/drave"
CORPUS = "data/wikitext2_test.txt"


def lancer(commande, delai):
    p = subprocess.run(commande, capture_output=True, text=True, timeout=delai)
    return p.stdout, p.stderr, p.returncode


def identifiants_generes(sortie):
    """Extrait `--- ids générés : [12, 34, ..]` — ou None si absent."""
    m = re.search(r"--- ids générés : \[([^\]]*)\]", sortie)
    if not m:
        return None
    return [int(x) for x in re.findall(r"\d+", m.group(1))]


def debit(sortie):
    m = re.search(r"généré\s+: \d+ tokens en [0-9.]+ s\s+\(([0-9.]+) tok/s\)", sortie)
    return float(m.group(1)) if m else None


def inférer(modele, invite, n, threads, delai):
    cmd = [MOTEUR, modele, "--infer", "--prompt", invite, "--n", str(n),
           "--temp", "0", "--ctx", "256", "--threads", str(threads)]
    out, err, code = lancer(cmd, delai)
    ids = identifiants_generes(out)
    if ids is None:
        raise RuntimeError(f"pas d'identifiants générés (code {code})\n{err[-800:]}")
    return ids, debit(out), out


def identifiants_tokenises(sortie):
    """La ligne d'identifiants de `--tokenize` : que des nombres séparés d'espaces.

    Elle n'est pas la dernière (le moteur imprime ensuite le contrôle de
    réversibilité « recolle : … ») — s'y fier donnait 0 identifiant des deux
    côtés, donc un faux « vocabulaire NON partagé ».
    """
    for ligne in sortie.splitlines():
        mots = ligne.split()
        if mots and all(m.isdigit() for m in mots):
            return [int(m) for m in mots]
    return []


def vocabulaire_identique(modele_a, modele_b, sonde):
    """Même texte → mêmes identifiants ? Sinon la comparaison ne veut rien dire."""
    cmd = lambda m: [MOTEUR, m, "--tokenize", "--texte", sonde]
    a, _, _ = lancer(cmd(modele_a), 300)
    b, _, _ = lancer(cmd(modele_b), 300)
    ia, ib = identifiants_tokenises(a), identifiants_tokenises(b)
    return ia == ib and len(ia) > 0, len(ia), len(ib)


def invites_du_corpus(n, taille=320):
    """n extraits de prose réelle : on mesure la langue, pas des questions."""
    texte = Path(CORPUS).read_text(encoding="utf-8", errors="replace")
    morceaux, i = [], 0
    while len(morceaux) < n and i + taille < len(texte):
        bout = texte[i:i + taille].strip()
        if len(bout) > taille // 2:
            morceaux.append(bout)
        i += taille * 7          # des extraits espacés, pas la même page
    return morceaux[:n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brouillon", required=True)
    ap.add_argument("--cible", required=True)
    ap.add_argument("--n", type=int, default=48, help="jetons générés par invite")
    ap.add_argument("--k", type=int, default=8, help="profondeur spéculative testée")
    ap.add_argument("--prompts", type=int, default=8)
    ap.add_argument("--threads", type=int, default=20)
    ap.add_argument("--delai", type=int, default=3600)
    ap.add_argument("--journal", default=None)
    a = ap.parse_args()

    lignes = []

    def dire(s=""):
        print(s)
        lignes.append(s)

    dire(f"# décodage spéculatif mesuré par le moteur")
    dire(f"brouillon : {a.brouillon}")
    dire(f"cible     : {a.cible}")

    sonde = "Le moteur ne lit que les poids qu'une activation touche."
    ok, na, nb = vocabulaire_identique(a.brouillon, a.cible, sonde)
    dire(f"vocabulaire partagé : {'oui' if ok else 'NON'} "
         f"({na} vs {nb} identifiants sur la même sonde)")
    if not ok:
        dire("REFUS : les deux modèles ne partagent pas leurs identifiants — "
             "l'acceptation mesurée ne voudrait rien dire.")
        if a.journal:
            Path(a.journal).write_text("\n".join(lignes) + "\n", encoding="utf-8")
        return 2

    invites = invites_du_corpus(a.prompts)
    lcp, deb_b, deb_c, echecs = [], [], [], 0
    dire("")
    dire(f"| # | jetons brouillon | jetons cible | préfixe commun | tok/s brouillon | tok/s cible |")
    dire("|---|---:|---:|---:|---:|---:|")
    for i, invite in enumerate(invites):
        try:
            ib, tb, _ = inférer(a.brouillon, invite, a.n, a.threads, a.delai)
            ic, tc, _ = inférer(a.cible, invite, a.n, a.threads, a.delai)
        except Exception as e:                       # une invite qui échoue ne
            echecs += 1                              # jette pas la campagne
            dire(f"| {i} | échec | échec | — | — | — |")
            print(f"  (invite {i} : {e})", file=sys.stderr)
            continue
        p = 0
        while p < len(ib) and p < len(ic) and ib[p] == ic[p]:
            p += 1
        lcp.append(p)
        if tb: deb_b.append(tb)
        if tc: deb_c.append(tc)
        dire(f"| {i} | {len(ib)} | {len(ic)} | **{p}** | {tb or 0:.2f} | {tc or 0:.2f} |")

    if not lcp:
        dire("aucune invite n'a abouti — rien à conclure.")
        if a.journal:
            Path(a.journal).write_text("\n".join(lignes) + "\n", encoding="utf-8")
        return 1

    k = a.k
    accept = [sum(1 for x in lcp if x >= j) / len(lcp) for j in range(1, k + 1)]
    a_moyen = sum(accept)
    dire("")
    dire(f"## acceptation, {len(lcp)} invites, {a.n} jetons, décodage glouton"
         + (f" · {echecs} échec(s)" if echecs else ""))
    dire("")
    dire("| k (jetons proposés) | " + " | ".join(str(j) for j in range(1, k + 1)) + " |")
    dire("|---|" + "---:|" * k)
    dire("| P(préfixe ≥ k) | " + " | ".join(f"{100*x:.0f} %" for x in accept) + " |")
    dire("")
    dire(f"jetons acceptés par tour (espérance, k={k}) : **{a_moyen:.2f} sur {k}** "
         f"· préfixe médian {sorted(lcp)[len(lcp)//2]} · max {max(lcp)}")

    if deb_b and deb_c:
        r = (sum(deb_c) / len(deb_c)) / (sum(deb_b) / len(deb_b))   # coût relatif
        r = 1.0 / r if r > 1 else r
        gain = (a_moyen + 1) / (k * r + 1)
        dire("")
        dire(f"coût relatif mesuré du brouillon : **{r:.3f}×** la cible "
             f"({sum(deb_b)/len(deb_b):.2f} vs {sum(deb_c)/len(deb_c):.2f} tok/s)")
        dire(f"gain net attendu à k={k} : **×{gain:.2f}** "
             f"(= ({a_moyen:.2f}+1) / ({k}×{r:.3f}+1))")
        # Le seuil qui décide : en dessous, le brouillon coûte plus qu'il ne rapporte.
        break_even = a_moyen / k
        dire(f"seuil de rentabilité : il faut r < {break_even:.3f}× "
             f"(acceptation moyenne {a_moyen/k:.1%} par jeton proposé)")
    else:
        dire("")
        dire("débits illisibles : le gain net n'est pas calculable, "
             "seule l'acceptation l'est.")

    if a.journal:
        Path(a.journal).write_text("\n".join(lignes) + "\n", encoding="utf-8")
        print(f"\n(journal écrit dans {a.journal})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
