#!/usr/bin/env python3
"""Construit un identifiant de perplexité au format harmony CANONIQUE.

Le montage forcé `<|start|>assistant<|channel|>final<|message|>texte` est hors
distribution : le modèle attend d'abord le canal `analysis` (mesuré : p=0,9999
contre 0,0001 pour `final`). Ce script construit donc la séquence telle que
l'implémentation officielle la produirait : message système complet, tour
utilisateur, puis un canal `analysis` court, puis le canal `final` qui porte le
texte à noter.

Sortie : /tmp/harmony_canonique.ids (identifiants) et /tmp/harmony_canonique.dep
(indice du premier jeton de contenu), pour que la perplexité du contenu seul
puisse être recalculée depuis les logits exportés.
"""
import subprocess, sys, os

Q = "/home/stephane/Data13TB/stephane/GitHub/Drave/drave-core/target/release/drave"
M = "/home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf"

DEB, FIN, MSG, CANAL = 200006, 200007, 200008, 200005


def encode(texte, nom):
    """Passe par le tokenizer du moteur (jamais un autre découpage)."""
    f_in = f"/tmp/harmony_piece_{nom}.txt"
    f_out = f"/tmp/harmony_piece_{nom}.ids"
    open(f_in, "w").write(texte)
    subprocess.run([Q, M, "--tokenize", "--fichier", f_in, "--sortie", f_out],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    brut = open(f_out).read()
    return [int(x) for x in brut.replace(",", " ").split()]


def tour(role, contenu_ids, canal=None):
    ids = [DEB] + encode(role, f"role_{role}_{canal or ''}") + []
    if canal:
        ids += [CANAL] + encode(canal, f"canal_{canal}")
    ids += [MSG] + contenu_ids + [FIN]
    return ids


def main():
    # `--sans-analysis` : même séquence SANS le message `analysis` — le contrôle
    # qui dit si la perplexité catastrophique vient du montage ou du moteur.
    sans_analysis = "--sans-analysis" in sys.argv
    suffixe = "_sans_analysis" if sans_analysis else ""
    prefixe = open("/tmp/wt2_prefixe.txt").read()
    contenu = open("/tmp/wt2_suite.txt").read()
    systeme = ("You are ChatGPT, a large language model trained by OpenAI.\n"
               "Knowledge cutoff: 2024-06\nCurrent date: 2025-09-28\n\n"
               "Reasoning: medium\n\n"
               "# Valid channels: analysis, commentary, final. "
               "Channel must be included for every message.")
    ids = tour("system", encode(systeme, "systeme"))
    ids += tour("user", encode(prefixe, "prefixe"))
    if not sans_analysis:
        ids += tour("assistant", encode("We are asked to continue the provided text.", "analysis"),
                    canal="analysis")
    debut_contenu = len(ids) + len([DEB] + encode("assistant", "role_assistant_final") +
                                   [CANAL] + encode("final", "canal_final") + [MSG])
    ids += tour("assistant", encode(contenu, "contenu"), canal="final")

    f_ids = f"/tmp/harmony_canonique{suffixe}.ids"
    f_dep = f"/tmp/harmony_canonique{suffixe}.dep"
    open(f_ids, "w").write(" ".join(map(str, ids)))
    open(f_dep, "w").write(str(debut_contenu))
    print(f"{f_ids} : {len(ids)} jetons, contenu noté à partir de l'indice {debut_contenu}"
          f" ({len(ids) - debut_contenu - 1} jetons)")


if __name__ == "__main__":
    main()
