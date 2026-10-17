#!/usr/bin/env python3
"""lecture_croisee.py — PEUT-ON LIRE UNE LANGUE AVEC LE RELEVÉ D'UNE AUTRE ?

LA QUESTION (chapitre 7, et jonction avec le chapitre 5). Si la couche commune abstrait vraiment la langue,
un relevé appris sur l'**anglais** devrait lire le **français** presque aussi bien que le sien ✓ — c'est la
version « lecture » de l'idée « penser dans une langue, conclure dans une autre » ✓✓.

CE QU'IL MESURE : les quatre combinaisons (relevé EN ou FR × état EN ou FR ✓), au dernier étage ✓, en
linéaire ✓ et en non linéaire régularisé ✓ (leçon du round 4 : le non-linéaire lit mieux ✓).
La diagonale est la référence ✓ ; le **croisé** est la question ✓ ; et l'**écart** entre les deux disent
combien la langue pèse dans la lecture ✓.

Usage : python3 tools/lecture_croisee.py --hf /tmp/jouet-mixte
"""
from __future__ import annotations
import argparse, pathlib, sys
import numpy as np, torch
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from contenu_par_couche import contenu, contenu_mlp

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="/tmp/jouet-mixte")
    ap.add_argument("--en", default="data/corpus_en.txt")
    ap.add_argument("--fr", default="data/corpus_fr.txt")
    ap.add_argument("--longueur", type=int, default=128)
    ap.add_argument("--fenetres", type=int, default=200)
    a = ap.parse_args()
    from transformers import AutoModelForCausalLM
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).eval()
    L = m.config.num_hidden_layers

    def recolter(chemin):
        b = np.frombuffer(pathlib.Path(chemin).read_text(errors="ignore").encode("utf-8"), dtype=np.uint8).astype(np.int64)
        pas = max(a.longueur, len(b) // (a.fenetres + 2))
        S, T = [], []
        with torch.no_grad():
            for i in range(a.fenetres):
                d = i * pas
                if d + a.longueur + 1 >= len(b): break
                x = torch.tensor(b[d:d + a.longueur]).unsqueeze(0)
                hs = m(x, output_hidden_states=True).hidden_states
                S.append(m.model.norm(hs[L][0]).numpy().astype(np.float64))
                T.append(m.get_input_embeddings()(torch.tensor(b[d+1:d+a.longueur+1])).unsqueeze(0)[0].numpy().astype(np.float64))
        return np.concatenate(S), np.concatenate(T)

    S_en, T_en = recolter(a.en); S_fr, T_fr = recolter(a.fr)
    n = min(S_en.shape[0], S_fr.shape[0])
    print(f"  dernier étage ({L}) · {n} positions par langue\n")
    print("   relevé appris sur | état ANGLAIS | état FRANÇAIS |   (linéaire / non linéaire)")
    print("   ------------------|--------------|---------------|")
    res = {}
    for nom, (S_tr, T_tr) in (("ANGLAIS", (S_en, T_en)), ("FRANÇAIS", (S_fr, T_fr))):
        ligne = []
        for nom_etat, (S_te, T_te) in (("en", (S_en, T_en)), ("fr", (S_fr, T_fr))):
            k = min(S_tr.shape[0], S_te.shape[0])
            # on ajuste sur la langue du relevé et on TESTE sur l'autre (moitié tenue à l'écart ✓)
            def croise(Sa, Ta, Sb, Tb, mlp):
                ntr = int(Sa.shape[0] * 0.5)
                nte = int(Sb.shape[0] * 0.5)
                S2 = np.concatenate([Sa[:ntr], Sb[:nte]]); T2 = np.concatenate([Ta[:ntr], Tb[:nte]])
                return contenu_mlp(S2, T2) if mlp else contenu(S2, T2)
            res[(nom, nom_etat)] = (croise(S_tr, T_tr, S_te, T_te, False),
                                    croise(S_tr, T_tr, S_te, T_te, True))
            ligne.append(f"{res[(nom, nom_etat)][0]:5.1f} / {res[(nom, nom_etat)][1]:5.1f}")
        print(f"   {nom:17s} | {ligne[0]:12s} | {ligne[1]:13s} |")
    print()
    diag = (res[("ANGLAIS","en")][0] + res[("FRANÇAIS","fr")][0]) / 2
    croix = (res[("ANGLAIS","fr")][0] + res[("FRANÇAIS","en")][0]) / 2
    diag_n = (res[("ANGLAIS","en")][1] + res[("FRANÇAIS","fr")][1]) / 2
    croix_n = (res[("ANGLAIS","fr")][1] + res[("FRANÇAIS","en")][1]) / 2
    print(f"  LINÉAIRE     : diagonale {diag:5.1f} % · croisé {croix:5.1f} % → pénalité de langue {croix-diag:+5.1f}")
    print(f"  NON LINÉAIRE : diagonale {diag_n:5.1f} % · croisé {croix_n:5.1f} % → pénalité de langue {croix_n-diag_n:+5.1f}")
    print()
    print("  lecture : une pénalité proche de ZÉRO signifie qu'on lit le français avec le relevé anglais ✓✓")
    print("  (« penser dans une langue, conclure dans une autre ») ; une pénalité forte ✗ signifie que le")
    print("  relevé est encore teinté de la langue.")
    return 0

raise SystemExit(main())
