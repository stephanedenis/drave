#!/usr/bin/env python3
"""pipeline_semantique.py — B13 : la chaîne M1 → M5 → M6 → M8.

Ce n'est pas un nouveau module : c'est un **test d'intégration** des briques
corrigées, sur un seul flux. M1 lit le code, M5 prédit avec le plateau, M6
sélectionne la tâche, M8 consolide. M2 n'est pas inclus (il demande un
entraînement GPU séparé) ; M9 lèse M1/M5.

La chaîne ne prétend pas faire mieux que M1 seul : elle vérifie que les blocs
se parlent et que chaque mesure reste celle de son module.
"""
from __future__ import annotations

import collections
import json
import random
from pathlib import Path

from .bus import Bus
from .episodique import Episodique
from .gating import Porte
from .hub import Hub
from .predictif import Predictif
from .sequences import corpus
from .sommeil import Sommeil


class PipelineSemantique:
    nom = "B13-pipeline-semantique"

    def __init__(self) -> None:
        self.bus = Bus()
        self.hub = Hub(self.bus)
        self.predictif = Predictif(cible="source", ordre=1, contexte=True, melange=0.5)
        self.porte = Porte()
        self.memoire = Episodique()
        self.sommeil = Sommeil()

    # ---- M1 ---------------------------------------------------------
    def percevoir(self, texte: str, jeu: str, contexte=None):
        code = self.hub.percevoir(texte, jeu, contexte)
        if code is not None:
            self.memoire.stocker(texte, code, "?")
        return code

    # ---- M5 ---------------------------------------------------------
    def predire(self, sequences):
        self.predictif.entrainer(sequences)
        return self.predictif.evaluer(sequences)

    # ---- M6 ---------------------------------------------------------
    def selectionner(self, items=None):
        return self.porte.executer(items)

    # ---- M8 ---------------------------------------------------------
    def consolider(self, episodes=None, cle="groupe"):
        episodes = self.memoire.episodes if episodes is None else episodes
        return self.sommeil.consolider(episodes, cle=cle)

    # ---- M9 ---------------------------------------------------------
    def lesionner_m1(self, items):
        """M1 sans contexte : la mesure de privation, pas une lésion biologique."""
        ok = 0
        for it in items:
            from semantique.universaux import code_rsn
            c = self.hub.percevoir(it.texte, it.jeu, None)
            ok += int(c == code_rsn(it.attendu))
        return ok / max(1, len(items))

    def lesionner_m5(self, sequences):
        """M5 sans transitions : repli majoritaire."""
        sans = Predictif(cible="source", ordre=0)
        sans.entrainer(sequences)
        return sans.evaluer(sequences)


def mesurer(racine: str = "tools") -> dict:
    from jeux.corpus import construire_corpus
    from jeux.corpus_multilingue import construire_corpus_multilingue
    from semantique.typed_corpus import items as corpus_items
    from semantique.universaux import code_rsn

    p = PipelineSemantique()
    reels = [it for c in (construire_corpus(), construire_corpus_multilingue())
             for it in c.items if it.attendu.nature == "coup"]
    its = corpus_items()
    m1 = sum(int(p.percevoir(it.texte, it.jeu, it.contexte) == code_rsn(it.attendu)) for it in reels) / len(reels)

    seqs = corpus(0, 200, 12)
    idx = list(range(len(seqs)))
    random.Random(3).shuffle(idx)
    n = int(len(idx) * 0.8)
    train = [seqs[i] for i in idx[:n]]
    test = [seqs[i] for i in idx[n:]]
    p.predictif.entrainer(train)
    m5 = p.predictif.evaluer(test)
    sans = Predictif(cible="source", ordre=1, contexte=False)
    sans.entrainer(train)
    m5_sans = sans.evaluer(test)

    m6 = p.selectionner()
    switch = p.porte.executer_switch()

    p.memoire = Episodique()
    for it in its:
        p.memoire.stocker(it.texte, it.code, it.langue, it.paire)
    protos = p.consolider()
    m8 = p.sommeil.evaluer(p.memoire.episodes, protos)

    return {
        "M1": {"exact": m1, "n": len(reels)},
        "M5": {"avec_contexte": m5, "sans_contexte": m5_sans,
               "n_test": len(test)},
        "M6": {"executer": m6, "switch": switch},
        "M8": m8,
        "M9": {"M1_sans_contexte": p.lesionner_m1(reels)},
    }


def main() -> None:
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
