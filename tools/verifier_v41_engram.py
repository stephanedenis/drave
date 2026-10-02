#!/usr/bin/env python3
"""Vérifie l'**engram de V4.1** de bout en bout, hors du moteur.

Le moteur vide, pour chaque jeton et chaque couche d'engram, la projection `kv`
(25 600 valeurs) et le flux APRÈS injection (`engram_sortie`). Ce script les
recalcule en Python :

  1. les **adresses** : `tools/engram_reference.py:hachage` (transcription de
     `vllm/models/deepseek_v41/common/engram.py`, déjà validée) — donc une
     seconde implémentation, écrite depuis la source externe ;
  2. la **lecture des rangées** : 24 rangées de 264 octets (256 e4m3 + 8 échelles
     e8m0 par blocs de 32) lues dans la vraie table de 101 Go ;
  3. l'**assemblage** : `flatten(-2)` des 24 colonnes → 6 144 valeurs, puis
     `wkv` [25 600, 6 144] → `hc` clés + **une valeur partagée** ;
  4. l'**injection** (`_fused_engram_post_wkv_kernel`) sur le flux d'entrée, qui
     est le `l_last` de la couche précédente (vidé lui aussi).

Ce que ce script prouve : l'ordre d'assemblage des colonnes, la projection, la
lecture des rangées et l'injection — sur le vrai fichier, aux vraies adresses.
Ce qu'il ne prouve pas : le masque d'image (un texte seul n'en a aucun) ni la
comparaison à vLLM exécuté.

Usage :
    python3 tools/verifier_v41_engram.py <modele.gguf> <prefixe_dump> <tokens.ids> <couche_engram> [positions…]
"""
import os
import struct
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier_v41_mhc import Gguf                      # lecteur GGUF (F32/F16)
from engram_reference import hachage                   # hachage de référence

OCTETS_RANGEE = 264
VALEURS_RANGEE = 256


def e4m3(b):
    """e4m3 (OCP FP8) → f32, sans infini (exposant plein + mantisse pleine = NaN)."""
    s = (b >> 7) & 1
    e = (b >> 3) & 0xF
    m = b & 0x7
    if e == 0:
        v = (m / 8.0) * 2.0 ** -6
    elif e == 0xF and m == 0x7:
        v = 0.0
    else:
        v = (1.0 + m / 8.0) * 2.0 ** (e - 7)
    return -v if s else v


def e8m0(b):
    return 0.0 if b == 255 else 2.0 ** (b - 127)


class Table:
    """Accès direct à une table `blk.<l>.engram_embd.weight` (101 Go), par rangée."""

    def __init__(self, g, couche):
        nom = f"blk.{couche}.engram_embd.weight"
        self.dims, self.ttype, self.off = g.tenseurs[nom]
        self.base = g.donnees + self.off
        self.f = g.f

    def rangee(self, i):
        self.f.seek(self.base + i * OCTETS_RANGEE)
        r = self.f.read(OCTETS_RANGEE)
        vals = np.array([e4m3(b) for b in r[:VALEURS_RANGEE]], dtype=np.float64)
        ech = np.array([e8m0(r[VALEURS_RANGEE + i // 32]) for i in range(VALEURS_RANGEE)],
                       dtype=np.float64)
        return vals * ech


def dump(prefixe, nom, couche, pos):
    return np.fromfile(f"{prefixe}-{nom}-{couche}-{pos}.bin", dtype="<f4").astype(np.float64)


def rms_sans_poids(x, eps):
    return x / np.sqrt(np.mean(x * x) + eps)


def main():
    modele, prefixe, ids_f, couche = (sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
    positions = [int(v) for v in sys.argv[5:]]
    ids = [int(v) for v in open(ids_f).read().strip().split(",") if v != ""]
    g = Gguf(modele)

    def meta_i64(cle):
        # les listes sont dans les métadonnées : on les relit par le même chemin
        # que les tenseurs (le fichier les déclare sous `deepseek41.<cle>`).
        for nom in (f"deepseek41.{cle}", cle):
            if nom in g.metadonnees:
                return g.metadonnees[nom]
        raise SystemExit(f"métadonnée {cle} absente")

    # `max_ngram_size` et `n_heads` ne sont PAS des clefs GGUF : ils ne vivent
    # que dans le JSON `<arch>.config` recopié par le convertisseur — le moteur
    # les y lit aussi (`json_nombre("engram_max_ngram_size")`).
    import json as _json
    texte = g.metadonnees.get("deepseek41.config") or g.metadonnees.get("deepseek4.config") or "{}"
    conf = _json.loads(texte)
    conf = conf.get("text_config", conf)

    couches = meta_i64("engram.layer_ids")
    if couche not in couches:
        raise SystemExit(f"la couche {couche} ne porte pas d'engram ({couches})")
    ti = couches.index(couche)
    primes = meta_i64("engram.primes")
    multi = meta_i64("engram.multipliers")
    token_map = meta_i64("engram.token_map")
    max_ngram = int(conf.get("engram_max_ngram_size", 4))
    n_heads = int(conf.get("engram_n_heads", 8))
    pad_id = int(meta_i64("engram.pad_id"))
    nhc = (max_ngram - 1) * n_heads

    # Offsets : somme préfixe exclusive DANS chaque couche.
    offsets = []
    for l in range(len(couches)):
        courant = 0
        for col in range(nhc):
            offsets.append(courant)
            courant += primes[l * nhc + col]

    wkv = g.lire(f"blk.{couche}.engram_kv.weight")          # [25600, 6144]
    qn = g.lire(f"blk.{couche}.engram_q_norm.weight")       # [4, 5120]
    kn = g.lire(f"blk.{couche}.engram_k_norm.weight")
    hc, dim = qn.shape
    table = Table(g, couche)
    eps = 1e-20
    print(f"# couche {couche} (table {ti}) · hc {hc} · dim {dim} · {nhc} colonnes · "
          f"wkv {wkv.shape}")

    if not positions:
        positions = sorted(int(os.path.basename(f).split("-")[-1][:-4])
                           for f in __import__("glob").glob(f"{prefixe}-engram_kv-{couche}-*.bin"))
    echecs = 0
    for pos in positions:
        # ① les adresses, depuis la RÉFÉRENCE (pas depuis le Rust)
        adr = hachage(token_map, primes, offsets, multi, ids[:pos + 1],
                      list(range(pos + 1)), couches, max_ngram, n_heads, pad_id)
        bloc = adr[pos]
        # ② les 24 rangées et leur assemblage (colonne par colonne)
        rangee = np.zeros(nhc * VALEURS_RANGEE)
        for col in range(nhc):
            i = bloc[ti * nhc + col]
            rangee[col * VALEURS_RANGEE:(col + 1) * VALEURS_RANGEE] = table.rangee(i)
        # ③ la projection
        kv = wkv @ rangee
        obtenu_kv = dump(prefixe, "engram_kv", couche, pos)
        e1 = np.max(np.abs(kv - obtenu_kv))
        # ④ l'injection, sur le flux d'entrée (= `l_last` de la couche précédente)
        entree = dump(prefixe, "l_last", couche - 1, pos)
        sortie = np.zeros(hc * dim)
        for h in range(hc):
            xh = entree[h * dim:(h + 1) * dim]
            kh = kv[h * dim:(h + 1) * dim]
            val = kv[hc * dim:]
            hr = 1.0 / np.sqrt(np.mean(xh * xh) + eps)
            kr = 1.0 / np.sqrt(np.mean(kh * kh) + eps)
            dot = np.sum(xh * qn[h] * kn[h] * kh) * hr * kr / np.sqrt(dim)
            g_ = np.sqrt(max(abs(dot), 1e-6))
            if dot < 0:
                g_ = -g_
            porte = 1.0 / (1.0 + np.exp(-g_))
            sortie[h * dim:(h + 1) * dim] = xh + porte * val
        obtenu = dump(prefixe, "engram_sortie", couche, pos)
        e2 = np.max(np.abs(sortie - obtenu))
        dyn = np.max(np.abs(obtenu))
        ok = max(e1, e2) < 1e-4 * max(dyn, 1e-9) + 1e-6
        print(f"  pos {pos} : projection {e1:.3e} · injection {e2:.3e} "
              f"(dynamique {dyn:.3e})  {'OK ' if ok else 'ÉCART'}")
        if not ok:
            echecs += 1
    print("VERDICT : " + ("la projection et l'injection tiennent" if echecs == 0
                          else f"{echecs} position(s) en écart"))
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
