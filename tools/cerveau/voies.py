#!/usr/bin/env python3
"""M2 — deux voies : ventrale (quoi) et dorsale (où/comment).

Un même encodeur de surface, **gelé**, alimente deux familles de têtes :

- la voie **ventrale** lit l'**action** ;
- la voie **dorsale** lit un ou plusieurs champs de lieu : `de`, `vers`,
  `point`, `chemin_0`…

Chaque tête est indépendante : on peut en léser une (logits aléatoires) sans
toucher les autres. C'est la double dissociation minimale, étendue à plusieurs
champs dorsaux.

L'entraînement est **synthétique** (`items_synth`) ; l'évaluation porte sur les
surfaces **réelles** (`items`). Le module expose aussi les ablations :

- `pool="mean"` : moyenne seule (ablation du dernier état) ;
- `pool="last"` : dernier état seul ;
- `contexte=True` : ajout du RSN de contexte, encodé par le même encodeur gelé.

Les surfaces et le contexte sont normalisés (`normaliser`) puis lus en octets,
comme dans le prototype d'origine. L'API `entrainer`/`evaluer` reste compatible
avec `batterie.py` quand aucun champ dorsal supplémentaire n'est demandé.

## Généralisation aux surfaces inédites (A5)

Deux leviers sont ajoutés, tous deux **désactivés par défaut** :

- `augmentation_*` (voir `augmenter`) : le corpus d'entraînement est étendu par
  les **règles** des jeux (positions variées, coups légaux) et par des
  **familles de surfaces** absentes du corpus synthétique : UCI collé / espacé /
  tireté, SAN anglais et français, prises `x`, promotions, NLG `de … vers …`,
  `from … to …`, dames numérique `9x18` et algébrique `b6xd4`, go SGF `B[dd]`
  et français `ligne 4 colonne 4`. Aucune surface réelle n'est utilisée : la
  liste `exclure_surfaces` (les surfaces des items réels) sert de **garde
  anti-fuite**, toute surface générée dont la forme normalisée y figure est
  jetée. Les items de test restent donc réellement inédits.
- `normaliseur=` : permet d'évaluer et d'entraîner avec une normalisation plus
  agressive (`normaliser_coordonnees`) sans changer les défauts.
"""
from __future__ import annotations

import collections
import functools
import random
import re

import torch
import torch.nn as nn
import torch.nn.functional as F

from semantique.entrainer import pad
from semantique.normalisation import normaliser
from semantique.typed_corpus import ItemType, decouper, items, octets
from semantique.universaux import CHAMPS, code_rsn, resume_contexte

VALEURS = dict(CHAMPS)
CHAMPS_DORSAUX = ("de", "vers", "point", "chemin_0", "chemin_1")
POOLS = ("mean", "last", "mean+last")


@functools.lru_cache(maxsize=1 << 16)
def _normaliser(texte: str) -> str:
    """`normaliser` mémoïsé : les mêmes surfaces reviennent à chaque pas."""
    return normaliser(texte)


def normaliser_coordonnees(texte: str) -> str:
    """Normalisation plus agressive des coordonnées, après `normaliser`.

    Les concepts `[...]` sont laissés intacts ; hors concepts, on isole les
    séparateurs (`-`, `x`, `=`) et on sépare les coordonnées collées
    (`e2e4` → `e2 e4`, `a7a8q` → `a7 a8 q`, `nf3` → `n f3`). Deux écritures
    d'un même coup tendent alors vers la même forme — au prix d'un recouvrement
    de surface plus élevé, qui doit être recompté, pas supposé.
    """
    t = _normaliser(texte)
    morceaux = re.split(r"(\[[^\]]+\])", t)
    out = []
    for i, morceau in enumerate(morceaux):
        if i % 2 == 1:  # un concept normalisé
            out.append(morceau)
            continue
        s = re.sub(r"\s*[-–—/]\s*", " ", morceau)
        s = re.sub(r"\s*[x×]\s*", " x ", s)
        s = re.sub(r"\s*=\s*", " = ", s)
        s = re.sub(r"([a-h][1-8])(?=[a-h][1-8])", r"\1 ", s)
        s = re.sub(r"([a-h][1-8])(?=[qrbn](?:\s|$))", r"\1 ", s)
        s = re.sub(r"(?<![a-z])([kqrbn])([a-h][1-8])\b", r"\1 \2", s)
        s = re.sub(r"\s+", " ", s).strip()
        out.append(s)
    return re.sub(r"\s+", " ", " ".join(x for x in out if x)).strip()


def _san_francais(san: str) -> str:
    """SAN anglais → SAN français (R roi, D dame, T tour, F fou, C cavalier)."""
    if not san or san.startswith(("O-O", "o-o", "0-0")):
        return san
    table = {"K": "R", "Q": "D", "R": "T", "B": "F", "N": "C"}
    return table.get(san[0], san[0]) + san[1:]


class Voies(nn.Module):
    """Encodeur gelé + têtes ventrales/dorsales indépendantes."""

    nom = "M2-voies"

    def __init__(self, base: nn.Module, champs_dorsaux=("de",),
                 pool: str = "mean+last", contexte: bool = False):
        super().__init__()
        if pool not in POOLS:
            raise ValueError(f"pool inconnu : {pool!r} (attendu : {POOLS})")
        champs = tuple(champs_dorsaux)
        if not champs:
            raise ValueError("il faut au moins un champ dorsal")
        for nom in champs:
            if nom not in VALEURS:
                raise ValueError(f"champ dorsal inconnu : {nom!r}")
        self.base = base
        self.d_model = int(base.config.hidden_size)
        self.champs_dorsaux = champs
        self.pool = pool
        self.contexte = bool(contexte)
        n_pool = 2 if pool == "mean+last" else 1
        self.dim_entree = self.d_model * n_pool * (2 if self.contexte else 1)
        self.ventral = nn.Linear(self.dim_entree, len(VALEURS["action"]))
        self.dorsaux = nn.ModuleDict({
            nom: nn.Linear(self.dim_entree, len(VALEURS[nom])) for nom in champs
        })
        self._idx = {nom: {v: i for i, v in enumerate(VALEURS[nom])}
                     for nom in ("action",) + champs}
        # compatibilité avec le prototype d'origine
        self._idx_action = self._idx["action"]
        self._idx_de = {v: i for i, v in enumerate(VALEURS["de"])}
        self._idx_vers = {v: i for i, v in enumerate(VALEURS["vers"])}

    @property
    def dorsal(self) -> nn.Linear:
        """La première tête dorsale (compatibilité avec l'ancien `self.dorsal`)."""
        return self.dorsaux[self.champs_dorsaux[0]]

    def _pool(self, h: torch.Tensor, masque: torch.Tensor) -> torch.Tensor:
        m = masque.unsqueeze(-1).to(h.dtype)
        moyenne = (h * m).sum(1) / m.sum(1).clamp(min=1)
        if self.pool == "mean":
            return moyenne
        longueurs = masque.sum(1).clamp(min=1).long()
        idx = torch.arange(h.shape[0], device=h.device)
        dernier = h[idx, longueurs - 1]
        if self.pool == "last":
            return dernier
        return torch.cat([moyenne, dernier], dim=-1)

    def encode(self, ids, masque, ctx_ids=None, ctx_masque=None):
        s = self.base(input_ids=ids, attention_mask=masque, output_hidden_states=True)
        z = self._pool(s.hidden_states[-1], masque)
        if self.contexte:
            if ctx_ids is None or ctx_masque is None:
                raise ValueError("ce modèle attend un contexte (ctx_ids/ctx_masque)")
            sc = self.base(input_ids=ctx_ids, attention_mask=ctx_masque,
                           output_hidden_states=True)
            z = torch.cat([z, self._pool(sc.hidden_states[-1], ctx_masque)], dim=-1)
        return z

    def logits(self, ids, masque, ctx_ids=None, ctx_masque=None):
        h = self.encode(ids, masque, ctx_ids, ctx_masque)
        return self.ventral(h), {nom: tete(h) for nom, tete in self.dorsaux.items()}


def _lot(items_, lot, seq, rng, normaliseur=None):
    norm = normaliseur or _normaliser
    choix = [rng.choice(items_) for _ in range(lot)]
    return pad([octets(norm(i.texte), seq) for i in choix]), choix


def _entrees(mor, seq, seq_ctx, contexte, contextes=None, normaliseur=None):
    """Prépare surfaces + contexte (facultatif) pour un lot d'items."""
    norm = normaliseur or _normaliser
    x, masque = pad([octets(norm(i.texte), seq) for i in mor])
    if not contexte:
        if contextes is not None:
            raise ValueError("contexte fourni à un modèle sans contexte")
        return x, masque, None, None
    if contextes is None:
        contextes = [i.contexte for i in mor]
    if len(contextes) != len(mor):
        raise ValueError("un contexte par item est requis")
    c, cm = pad([octets(t, seq_ctx) for t in contextes])
    return x, masque, c, cm


def _cibles(choix, nom, idx, device):
    return torch.tensor([idx[i.code[nom]] for i in choix], dtype=torch.long,
                        device=device)


def _aleatoire_like(t: torch.Tensor, g: torch.Generator) -> torch.Tensor:
    return torch.randn(t.shape, generator=g, device=t.device, dtype=t.dtype)


# ---------------------------------------------------------------------------
# Augmentation synthétique par les règles (A5) — aucune surface réelle
# ---------------------------------------------------------------------------
# Positions structurées pour couvrir roque, promotion, prise en passant. Elles
# sont volontairement différentes des contextes du corpus réel : ce sont des
# positions d'entraînement, pas les items de test.
_FENS_ECHECS = (
    "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1",   # roques
    "8/P6k/8/8/8/8/7p/4K3 w - - 0 1",                        # promotions
    "4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1",                     # prise en passant
    "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
)


def _positions_echecs(n: int, graine: int):
    """Départ + positions structurées + `n` positions d'une partie aléatoire."""
    import jeux.regles.echecs as E

    rng = random.Random(graine)
    out = [E.Position.depart()]
    for fen in _FENS_ECHECS:
        try:
            out.append(E.Position.depuis_fen(fen))
        except Exception:  # une FEN de secours ne doit jamais bloquer l'entraînement
            continue
    pos = E.Position.depart()
    for _ in range(n):
        coups = pos.coups_legaux()
        if not coups or pos.terminal():
            break
        pos.joue(rng.choice(coups))
        out.append(pos.copie())
    return out


def _positions_dames(n: int, graine: int):
    """Départ + `n` positions d'une partie aléatoire de dames."""
    import jeux.regles.dames as D

    rng = random.Random(graine)
    out = [D.Position.depart()]
    pos = D.Position.depart()
    for _ in range(n):
        coups = pos.coups_legaux()
        if not coups or pos.terminal():
            break
        pos = pos.applique(rng.choice(coups))
        out.append(pos)
    return out


def _textes_echecs(pos, coup):
    """Les surfaces d'un coup d'échecs, par famille (langue incluse)."""
    import jeux.regles.echecs as E
    from jeux.lexique_multilingue import MULTI

    c0 = E.indice_vers_case(coup.de)
    c1 = E.indice_vers_case(coup.vers)
    lettre = "PNBRQK"[E.typ(pos.plateau[coup.de]) - 1]
    prise = pos.plateau[coup.vers] != 0 or coup.drapeau == E.EP
    sortie = [
        (f"{c0}{c1}", "uci", "notation"),
        (f"{c0} {c1}", "uci-espace", "notation"),
        (f"{c0}-{c1}", "uci-tiret", "notation"),
        (f"{lettre} {c0} {c1}", "piece-espace", "notation"),
        (f"{lettre} {c0}-{c1}", "piece-tiret", "notation"),
    ]
    if prise:
        sortie += [(f"{c0}x{c1}", "prise", "notation"),
                   (f"{lettre}x{c1}", "prise-piece", "notation")]
    san = pos.san(coup)
    sortie.append((san, "san", "notation"))
    if san.endswith(("+", "#")):
        sortie.append((san[:-1], "san", "notation"))
    fr = _san_francais(san.rstrip("+#"))
    if fr != san:
        sortie.append((fr, "san-fr", "notation"))
    if coup.promotion:
        pl = "NBRQ"[coup.promotion - E.CAVALIER]
        sortie += [(f"{c0}{c1}{pl.lower()}", "promo-uci", "notation"),
                   (f"{c1}={pl}", "promo-eq", "notation"),
                   (f"{c0}-{c1}={pl}", "promo-long", "notation")]
    for langue in ("fr", "en"):
        formes = MULTI.formes(f"echecs.piece.{lettre}", langue)
        if not formes:
            continue
        p = formes[0]
        if langue == "fr":
            sortie += [(f"{p} de {c0} vers {c1}", "nlp-fr", "fr"),
                       (f"le {p} de {c0} vers {c1}", "nlp-fr", "fr"),
                       (f"le {p} {c0} va en {c1}", "nlp-fr", "fr")]
        else:
            sortie += [(f"{p} from {c0} to {c1}", "nlp-en", "en"),
                       (f"{p} {c0} to {c1}", "nlp-en", "en")]
    return sortie


def _textes_dames(coup):
    """Les surfaces d'un coup de dames : numérique, algébrique, français."""
    import jeux.regles.dames as D

    algs = [D.indice_vers_case(i) for i in coup.chemin]
    nums = [str(i + 1) for i in coup.chemin]
    prise = len(coup.chemin) > 2
    sep = "x" if prise else "-"
    sortie = [
        (" ".join(algs), "alg-espace", "notation"),
        (sep.join(algs), "alg-sep", "notation"),
        (" ".join(nums), "num-espace", "notation"),
        (sep.join(nums), "num-sep", "notation"),
    ]
    if prise:
        sortie.append(("-".join(algs), "alg-tiret", "notation"))
    c0, c1 = algs[0], algs[-1]
    if prise:
        sortie += [(f"le pion {c0} prend en {c1}", "nlp-fr", "fr"),
                   (f"pion {c0} prend {c1}", "nlp-fr", "fr")]
    else:
        sortie += [(f"le pion de {c0} vers {c1}", "nlp-fr", "fr"),
                   (f"pion de {c0} vers {c1}", "nlp-fr", "fr")]
    return sortie


def _textes_go(point: int):
    """Les surfaces d'un point de go : GTP, SGF, français spatial."""
    import jeux.regles.go as G

    gtp = G.point_vers_gtp(point, 9)
    sgf = G.point_vers_sgf(point, 9)
    ligne, colonne = 9 - point // 9, point % 9 + 1
    return [
        (gtp, "gtp", "notation"),
        (f"B[{sgf}]", "sgf", "notation"),
        (f"W[{sgf}]", "sgf", "notation"),
        (f"ligne {ligne} colonne {colonne}", "go-fr", "fr"),
        (f"jouer en {gtp}", "go-fr", "fr"),
        (f"pierre noire en {gtp}", "go-fr", "fr"),
        (f"pierre blanche en {gtp}", "go-fr", "fr"),
    ]


def augmenter(champs=CHAMPS_DORSAUX, familles=("formes",), positions: int = 0,
              graine: int = 0, exclure_surfaces=None,
              normaliseur=None) -> list[ItemType]:
    """Génère des surfaces synthétiques par les règles, hors surfaces réelles.

    `familles` : `"formes"` (familles de surfaces sur les positions déjà
    couvertes) et/ou `"positions"` (positions variées : une partie aléatoire de
    `positions` demi-coups + positions structurées roque/promotion/e.p.).

    `exclure_surfaces` : surfaces **réelles** (brutes) à ne jamais produire.
    La comparaison se fait après `normaliseur` (défaut : `normaliser`), donc
    toute forme normalisée déjà présente dans le corpus réel est écartée. C'est
    la garde anti-fuite : les items réels restent inédits à l'entraînement.
    """
    norm = normaliseur or _normaliser
    interdits = {norm(t) for t in (exclure_surfaces or ())}
    champs = tuple(champs)
    vus: set = set()
    out: list[ItemType] = []

    def ajoute(texte, r, code, famille, langue, contexte):
        texte = texte.strip()
        if not texte:
            return
        forme = norm(texte)
        if forme in interdits:
            return
        cle = (forme, tuple(code.get(nom) for nom in champs))
        if cle in vus:
            return
        vus.add(cle)
        out.append(ItemType(texte, code, r.jeu, "coup", langue,
                            f"aug-{famille}", famille, contexte))

    besoin = set()
    if any(nom in ("de", "vers") for nom in champs):
        besoin.add("echecs")
    if "point" in champs:
        besoin.add("go")
    if any(nom.startswith("chemin") for nom in champs):
        besoin.add("dames")

    if "echecs" in besoin:
        import jeux.regles.echecs as E

        positions_e = ([E.Position.depart()] if "positions" not in familles
                       else _positions_echecs(positions or 40, graine))
        for pos in positions_e:
            ctx = resume_contexte(E.rsn_depuis_position(pos))
            for coup in pos.coups_legaux():
                r = E.action_depuis_coup(coup)
                code = code_rsn(r)
                for texte, famille, langue in _textes_echecs(pos, coup):
                    ajoute(texte, r, code, famille, langue, ctx)

    if "dames" in besoin:
        import jeux.regles.dames as D

        positions_d = ([D.Position.depart()] if "positions" not in familles
                       else _positions_dames(positions or 40, graine))
        for pos in positions_d:
            ctx = resume_contexte(D.rsn_depuis_position(pos))
            for coup in pos.coups_legaux():
                r = D.action_depuis_coup(coup)
                code = code_rsn(r)
                for texte, famille, langue in _textes_dames(coup):
                    ajoute(texte, r, code, famille, langue, ctx)

    if "go" in besoin:
        import jeux.regles.go as G
        from jeux.rsn import RSN

        ctx = resume_contexte(G.Position.depart(9, 65).vers_rsn())
        for point in range(81):
            r = RSN("go", "coup", {"taille": 9, "point": point})
            code = code_rsn(r)
            for texte, famille, langue in _textes_go(point):
                ajoute(texte, r, code, famille, langue, ctx)

    return out


def entrainer(base, pas: int = 400, lot: int = 32, seq: int = 64, graine: int = 1,
              device: str = "cuda", synth: bool = False, champs=None,
              pool: str = "mean+last", contexte: bool = False, seq_ctx: int = 192,
              augmentation=False, familles=("formes",), positions: int = 0,
              exclure_surfaces=None, normaliseur=None):
    """Entraîne les têtes sur les surfaces synthétiques.

    `champs` est la liste des champs dorsaux à apprendre. Par défaut `("de",)`,
    ce qui reproduit le prototype d'origine (une seule tête dorsale).

    Pour plusieurs champs, chaque pas forme un lot composite : un bloc d'items
    par champ (et un bloc d'action), une seule passe avant, et une perte par
    tête calculée sur son bloc. L'encodeur étant gelé, c'est équivalent à des
    passes séparées ; c'est simplement plus rapide.

    `augmentation` : `False` (défaut, comportement A3), `True` (familles
    `familles`) ou un tuple de familles (`"formes"`, `"positions"`). Voir
    `augmenter` ; `exclure_surfaces` est la garde anti-fuite (par défaut, les
    surfaces réelles de `items()`, jamais utilisées à l'entraînement).
    """
    rng = random.Random(graine)
    norm = normaliseur or _normaliser
    its = items()
    champs = tuple(champs or ("de",))
    if synth:
        from semantique.synth_corpus import items_synth
        syn = items_synth()
        train_par_champ = {
            nom: [i for i in syn if i.code.get(nom) is not None] for nom in champs
        }
        train_action = [i for i in syn if i.code.get("action") is not None]
        val = its
        if champs == ("de",):
            # compatibilité stricte avec le prototype : 146 surfaces réelles
            val = [i for i in its if i.code.get("de") is not None]
    else:
        train, val = decouper(its, graine, 0.2)
        train_par_champ = {
            nom: [i for i in train if i.code.get(nom) is not None] for nom in champs
        }
        train_action = [i for i in train if i.code.get("action") is not None]
        if champs == ("de",):
            train_par_champ = {
                "de": [i for i in train if i.code.get("de") is not None]
            }
            train_action = train_par_champ["de"]
            val = [i for i in val if i.code.get("de") is not None]
    if augmentation:
        familles_aug = (tuple(augmentation)
                        if isinstance(augmentation, (tuple, list))
                        else tuple(familles))
        exclure = (exclure_surfaces if exclure_surfaces is not None
                   else [i.texte for i in its])
        ajout = augmenter(champs, familles=familles_aug, positions=positions,
                          graine=graine, exclure_surfaces=exclure,
                          normaliseur=norm)
        for nom in champs:
            train_par_champ[nom].extend(i for i in ajout
                                        if i.code.get(nom) is not None)
        train_action.extend(i for i in ajout
                            if i.code.get("action") is not None)
    for nom, sous in train_par_champ.items():
        if not sous:
            raise ValueError(f"aucun item d'entraînement pour le champ {nom!r}")

    m = Voies(base, champs_dorsaux=champs, pool=pool, contexte=contexte).to(device)
    for p in m.base.parameters():
        p.requires_grad = False
    opt = torch.optim.AdamW([
        {"params": m.ventral.parameters(), "lr": 1e-3},
        {"params": [p for t in m.dorsaux.values() for p in t.parameters()], "lr": 1e-3},
    ])
    idx_action = m._idx["action"]

    for _ in range(1, pas + 1):
        if len(champs) == 1:
            # Chemin historique : un seul lot porte action + champ dorsal.
            nom = champs[0]
            (x, masque), choix = _lot(train_par_champ[nom], lot, seq, rng, norm)
            ctx = ([i.contexte for i in choix] if contexte else None)
            x, masque, c, cm = _entrees(choix, seq, seq_ctx, contexte, ctx, norm)
            va, vd = m.logits(
                x.to(device), masque.to(device),
                c.to(device) if c is not None else None,
                cm.to(device) if cm is not None else None,
            )
            perte = (F.cross_entropy(va, _cibles(choix, "action", idx_action, device))
                     + F.cross_entropy(vd[nom],
                                       _cibles(choix, nom, m._idx[nom], device)))
        else:
            # Lot composite : action + un bloc par champ dorsal.
            choix_action = [rng.choice(train_action) for _ in range(lot)]
            choix_par = {
                nom: [rng.choice(train_par_champ[nom]) for _ in range(lot)]
                for nom in champs
            }
            choix_total = choix_action + [i for nom in champs for i in choix_par[nom]]
            ctx = ([i.contexte for i in choix_total] if contexte else None)
            x, masque, c, cm = _entrees(choix_total, seq, seq_ctx, contexte, ctx, norm)
            va, vd = m.logits(
                x.to(device), masque.to(device),
                c.to(device) if c is not None else None,
                cm.to(device) if cm is not None else None,
            )
            # La voie ventrale voit tout le lot composite (tous les blocs ont
            # une action) : plus d'exemples par pas, sans toucher aux têtes
            # dorsales, qui ne reçoivent leur perte que sur leur bloc.
            perte = F.cross_entropy(
                va, _cibles(choix_total, "action", idx_action, device))
            debut = lot
            for nom in champs:
                fin = debut + lot
                perte = perte + F.cross_entropy(
                    vd[nom][debut:fin],
                    _cibles(choix_par[nom], nom, m._idx[nom], device))
                debut = fin
        opt.zero_grad()
        perte.backward()
        opt.step()
    return m, val


def _stats_classes(pred, cible, n_classes_tete: int):
    """Exactitude, hasard, majorité, rappel macro et rappel par classe."""
    n = len(cible)
    ok = sum(int(a == b) for a, b in zip(pred, cible))
    classes = collections.Counter(cible)
    par_classe = {}
    for c, cnt in sorted(classes.items(), key=lambda kv: (-kv[1], str(kv[0]))):
        bons = sum(1 for a, b in zip(pred, cible) if b == c and a == c)
        par_classe[str(c)] = {"n": cnt, "rappel": bons / cnt}
    macro = sum(v["rappel"] for v in par_classe.values()) / max(1, len(par_classe))
    return {
        "n": n,
        "exact": ok / max(1, n),
        "chance": 1.0 / n_classes_tete,
        "majorite": max(classes.values(), default=0) / max(1, n),
        "n_classes": len(classes),
        "n_classes_tete": n_classes_tete,
        "macro_rappel": macro,
        "par_classe": par_classe,
    }


def _stats(m, mor, nom, pa, pf, retour_pred: bool = False):
    pred = [VALEURS[nom][p] for p in pf]
    cible = [it.code[nom] for it in mor]
    pred_a = [VALEURS["action"][p] for p in pa]
    cible_a = [it.code["action"] for it in mor]
    res = _stats_classes(pred, cible, len(VALEURS[nom]))
    res_a = _stats_classes(pred_a, cible_a, len(VALEURS["action"]))
    res["action"] = res_a["exact"]
    res["action_macro_rappel"] = res_a["macro_rappel"]
    res["action_par_classe"] = res_a["par_classe"]
    if retour_pred:
        res["pred"] = pred
        res["cible"] = cible
        res["ok"] = [int(a == b) for a, b in zip(pred, cible)]
        res["pred_action"] = pred_a
        res["cible_action"] = cible_a
        res["ok_action"] = [int(a == b) for a, b in zip(pred_a, cible_a)]
    return res


def _passe(m, mor, nom, device, lese=None, contextes=None, seq=64, seq_ctx=192,
           graine_lesion=0, lot=64, normaliseur=None):
    """Une passe avant sur `mor`, avec lésion éventuelle de la voie choisie."""
    if lese not in (None, "ventral", "dorsal"):
        raise ValueError(f"lésion inconnue : {lese!r}")
    if nom not in m.dorsaux:
        raise KeyError(f"le modèle n'a pas de tête {nom!r}")
    pa_all, pf_all = [], []
    g = None
    for d in range(0, len(mor), lot):
        sous = mor[d:d + lot]
        ctxs = contextes[d:d + lot] if contextes is not None else None
        x, masque, c, cm = _entrees(sous, seq, seq_ctx, m.contexte, ctxs,
                                    normaliseur)
        va, vd = m.logits(
            x.to(device), masque.to(device),
            c.to(device) if c is not None else None,
            cm.to(device) if cm is not None else None,
        )
        if lese:
            if g is None:
                g = torch.Generator(device=va.device)
                g.manual_seed(int(graine_lesion) & 0x7FFFFFFF)
            if lese == "ventral":
                va = _aleatoire_like(va, g)
            else:
                vd = {k: _aleatoire_like(v, g) for k, v in vd.items()}
        pa_all.extend(va.argmax(1).tolist())
        pf_all.extend(vd[nom].argmax(1).tolist())
    return pa_all, pf_all


@torch.no_grad()
def evaluer(m, val, device: str = "cuda", lese: str | None = None, champ=None,
            normaliseur=None):
    """Évaluation historique : action + premier champ dorsal, sur ses items réels."""
    m.eval()
    champ = champ or m.champs_dorsaux[0]
    sous = [it for it in val if it.code.get(champ) is not None]
    if not sous:
        raise ValueError(f"aucun item réel pour le champ {champ!r}")
    pa, pf = _passe(m, sous, champ, device, lese=lese, normaliseur=normaliseur)
    idx_a = m._idx["action"]
    idx_f = m._idx[champ]
    ok_a = sum(int(pa[j] == idx_a[it.code["action"]]) for j, it in enumerate(sous))
    ok_f = sum(int(pf[j] == idx_f[it.code[champ]]) for j, it in enumerate(sous))
    return {"action": ok_a / len(sous), champ: ok_f / len(sous), "n": len(sous)}


@torch.no_grad()
def evaluer_champs(m, val, champs=None, device: str = "cuda", lesions: bool = True,
                   contexte_mode: str = "reel", graine: int = 0,
                   retour_pred: bool = False, seq: int = 64, seq_ctx: int = 192,
                   normaliseur=None):
    """Évalue chaque champ dorsal sur ses surfaces réelles.

    `contexte_mode` : `"reel"` (contexte de l'item), `"melange"` (contextes
    permutés globalement) ou `"vide"` (contexte vide). Les modes autres que
    `"reel"` ne valent que pour un modèle entraîné avec contexte.

    Retourne, par champ, l'exactitude, n, le hasard, la majorité, le rappel
    macro, le rappel par classe, et les lésions ventrale/dorsale. La clé
    `action_global` donne l'action sur l'ensemble des items fournis.
    """
    m.eval()
    champs = tuple(champs or m.champs_dorsaux)
    for nom in champs:
        if nom not in m.dorsaux:
            raise KeyError(f"le modèle n'a pas de tête {nom!r}")
    if contexte_mode not in ("reel", "melange", "vide"):
        raise ValueError(f"contexte_mode inconnu : {contexte_mode!r}")
    if contexte_mode != "reel" and not m.contexte:
        raise ValueError("mode de contexte demandé pour un modèle sans contexte")

    if contexte_mode == "melange":
        ctxs = [it.contexte for it in val]
        random.Random(graine).shuffle(ctxs)
        ctx_map = {id(it): ctxs[i] for i, it in enumerate(val)}
    elif contexte_mode == "vide":
        ctx_map = {id(it): "" for it in val}
    else:
        ctx_map = None

    def _ctx(sub):
        return None if ctx_map is None else [ctx_map[id(it)] for it in sub]

    out = {}
    for nom in champs:
        sous = [it for it in val if it.code.get(nom) is not None]
        if not sous:
            raise ValueError(f"aucun item réel pour le champ {nom!r}")
        cible_f = [it.code[nom] for it in sous]
        cible_a = [it.code["action"] for it in sous]
        pa, pf = _passe(m, sous, nom, device, contextes=_ctx(sous),
                        seq=seq, seq_ctx=seq_ctx, normaliseur=normaliseur)
        res = _stats(m, sous, nom, pa, pf, retour_pred=retour_pred)
        if lesions:
            pa_v, pf_v = _passe(m, sous, nom, device, lese="ventral",
                                contextes=_ctx(sous), seq=seq, seq_ctx=seq_ctx,
                                graine_lesion=graine + 1,
                                normaliseur=normaliseur)
            pa_d, pf_d = _passe(m, sous, nom, device, lese="dorsal",
                                contextes=_ctx(sous), seq=seq, seq_ctx=seq_ctx,
                                graine_lesion=graine + 2,
                                normaliseur=normaliseur)
            res["lesions"] = {
                "ventrale": {
                    "action": _exact_indices(pa_v, cible_a, m._idx["action"]),
                    nom: _exact_indices(pf_v, cible_f, m._idx[nom]),
                    "n": len(sous),
                },
                "dorsale": {
                    "action": _exact_indices(pa_d, cible_a, m._idx["action"]),
                    nom: _exact_indices(pf_d, cible_f, m._idx[nom]),
                    "n": len(sous),
                },
            }
        out[nom] = res

    # Action seule, sur tous les items fournis (contrôle de la voie ventrale).
    if champs:
        ctx_all = None if ctx_map is None else [ctx_map[id(it)] for it in val]
        pa, _ = _passe(m, val, champs[0], device, contextes=ctx_all,
                       seq=seq, seq_ctx=seq_ctx, normaliseur=normaliseur)
        cible_a = [it.code["action"] for it in val]
        res = _stats_classes([VALEURS["action"][p] for p in pa], cible_a,
                             len(VALEURS["action"]))
        if lesions:
            pa_v, _ = _passe(m, val, champs[0], device, lese="ventral",
                             contextes=ctx_all, seq=seq, seq_ctx=seq_ctx,
                             graine_lesion=graine + 3, normaliseur=normaliseur)
            pa_d, _ = _passe(m, val, champs[0], device, lese="dorsal",
                             contextes=ctx_all, seq=seq, seq_ctx=seq_ctx,
                             graine_lesion=graine + 4, normaliseur=normaliseur)
            res["lesions"] = {
                "ventrale": {
                    "action": _exact_indices(pa_v, cible_a, m._idx["action"]),
                    "n": len(val),
                },
                "dorsale": {
                    "action": _exact_indices(pa_d, cible_a, m._idx["action"]),
                    "n": len(val),
                },
            }
        out["action_global"] = res
    return out


def _exact_indices(pred, cible, idx):
    return sum(int(p == idx[c]) for p, c in zip(pred, cible)) / max(1, len(cible))
