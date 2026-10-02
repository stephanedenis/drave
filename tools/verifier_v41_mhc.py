#!/usr/bin/env python3
"""Vérifie la chaîne mHC **retardée** de DeepSeek-V4.1 sur le VRAI modèle.

Le moteur vide ses intermédiaires (`DRAVE_DUMP_COUCHES=<préfixe>`, un fichier
f32 par tenseur, couche et position) ; ce script les relit et refait le calcul
**hors du moteur**, en numpy, d'après les formules de la référence d'exécution
(vLLM `mhc_pre_delayed_torch`, `hc_collapse_triton`). Trois égalités :

  1. `hc_attn_pre(0, pos) == copie 0 de l'état` — au tout premier raccord, la
     référence replie avec `residual[:, 0]` et rien d'autre. Si le moteur
     appliquait encore la chaîne de V4 (repliement avec ses PROPRES `pre`), ce
     serait `(Σ pre)·embarquement`, c'est-à-dire un vecteur différent ;
  2. `hc_ffn_pre(0, pos) == sigmoïde(rms_norm(hc_ffn_in)·fn·scale + base) + eps`
     — les 24 mélanges, calculés sur le flux d'APRÈS le post de l'attention ;
  3. `hidden_final(0, pos) == rms_norm(Σ_c hc_ffn_pre[c]·l_last[c], output_norm)`
     — la tête de V4.1, qui n'a **aucun poids appris** : sa réduction EST la
     `pre` de la dernière FFN ;
  4. `hc_mel_ffn == Σ_c hc_pre_attn[c]·hc_ffn_in[c]` — **le maillon central** :
     l'entrée de la FFN se replie avec la `pre` de l'ATTENTION, pas avec la
     sienne. Sans ce contrôle, échanger les deux ne changerait ni ①, ni ②, ni ③
     (elles vivent toutes en aval de `l_last`).

Usage :
    python3 tools/verifier_v41_mhc.py <modele.gguf> <prefixe_dump> <tokens.ids> [couche]
"""
import struct
import sys

import numpy as np

F16, F32, Q8_0 = 1, 0, 8
TYPES_OCTETS = {0: 4, 1: 2, 2: 18, 3: 20, 8: 34}   # F32, F16, Q4_0, Q4_1, Q8_0


class Gguf:
    def __init__(self, chemin):
        self.f = open(chemin, "rb", buffering=0)
        if self.f.read(4) != b"GGUF":
            raise SystemExit("ce n'est pas un GGUF")
        self.version = struct.unpack("<I", self.f.read(4))[0]
        n_tensors, n_kv = struct.unpack("<QQ", self.f.read(16))
        self.alignement = 32
        for _ in range(n_kv):
            cle = self._chaine()
            t = struct.unpack("<I", self.f.read(4))[0]
            v = self._valeur(t)
            if cle == "general.alignment":
                self.alignement = int(v)
        self.tenseurs = {}
        for _ in range(n_tensors):
            nom = self._chaine()
            nd = struct.unpack("<I", self.f.read(4))[0]
            dims = [struct.unpack("<Q", self.f.read(8))[0] for _ in range(nd)]
            ttype = struct.unpack("<I", self.f.read(4))[0]
            off = struct.unpack("<Q", self.f.read(8))[0]
            self.tenseurs[nom] = (dims, ttype, off)
        fin = self.f.tell()
        self.donnees = (fin + self.alignement - 1) // self.alignement * self.alignement

    def _chaine(self):
        n = struct.unpack("<Q", self.f.read(8))[0]
        return self.f.read(n).decode("utf-8", "replace")

    def _valeur(self, t):
        tailles = {0: 1, 1: 1, 2: 2, 3: 2, 4: 4, 5: 4, 6: 4, 7: 1, 10: 8, 11: 8, 12: 8}
        fmt = {0: "<B", 1: "<b", 2: "<H", 3: "<h", 4: "<I", 5: "<i", 6: "<f",
               7: "<?", 10: "<Q", 11: "<q", 12: "<d"}
        if t == 8:
            return self._chaine()
        if t == 9:
            et = struct.unpack("<I", self.f.read(4))[0]
            n = struct.unpack("<Q", self.f.read(8))[0]
            return [self._valeur(et) for _ in range(n)]
        return struct.unpack(fmt[t], self.f.read(tailles[t]))[0]

    def lire(self, nom, lignes=None):
        """Rend le tenseur en f32 (F32 et F16 seulement). `lignes=(a,b)` ne lit
        que ces lignes — indispensable pour `token_embd` (129 280 × 5 120)."""
        dims, ttype, off = self.tenseurs[nom]
        n_in = dims[0]
        # Un tenseur 1-D (base, scale, norme) n'a qu'une « ligne » de `dims[0]` :
        # c'est le cas de `blk.0.hc_ffn_base.weight` [24].
        a, b = lignes if lignes else (0, dims[1] if len(dims) > 1 else 1)
        n = n_in * (b - a)
        self.f.seek(self.donnees + off + TYPES_OCTETS[ttype] * n_in * a)
        brut = self.f.read(TYPES_OCTETS[ttype] * n)
        if ttype == F32:
            return np.frombuffer(brut, dtype="<f4").astype(np.float64).reshape(b - a, n_in)
        if ttype == F16:
            return np.frombuffer(brut, dtype="<f2").astype(np.float64).reshape(b - a, n_in)
        raise SystemExit(f"{nom} : type {ttype}, ce vérificateur ne lit que F32 et F16")


def dump(prefixe, nom, couche, pos):
    return np.fromfile(f"{prefixe}-{nom}-{couche}-{pos}.bin", dtype="<f4").astype(np.float64)


def rms_norm(x, poids, eps):
    return x / np.sqrt(np.mean(x * x) + eps) * poids


def main():
    chemin, prefixe, ids_f = sys.argv[1], sys.argv[2], sys.argv[3]
    # La COUCHE : elle se lit dans les vides (le préfixe est le même, seul le
    # numéro de couche change). La câbler en dur sur 0 ferait comparer la tête à
    # la `pre` d'une autre couche dès que la plage en contient deux.
    import glob as _g, re as _re
    couches = sorted({int(_re.search(r"-hc_attn_pre-(\d+)-", f).group(1))
                      for f in _g.glob(f"{prefixe}-hc_attn_pre-*-*.bin")})
    assert len(couches) == 1, f"vides de plusieurs couches {couches} : relancer plage par plage"
    couche = int(sys.argv[4]) if len(sys.argv) > 4 else couches[-1]
    ids = [int(v) for v in open(ids_f).read().strip().split(",") if v != ""]
    g = Gguf(chemin)
    fn = g.lire("blk.0.hc_ffn_fn.weight")            # [24, 4·5120]
    base = g.lire("blk.0.hc_ffn_base.weight").reshape(-1)
    scale = g.lire("blk.0.hc_ffn_scale.weight").reshape(-1)
    norme = g.lire("output_norm.weight").reshape(-1)
    h = norme.size
    # `base` fait `2·hc + hc²` : on en tire `hc` plutôt que de l'écrire en dur.
    hc = int((-2 + (4 + 4 * base.size) ** 0.5) / 2)
    eps = 1e-20          # `deepseek41.rms_norm_eps`
    hc_eps = 1e-6        # `deepseek41.hc_eps`
    print(f"# {chemin}\n# h={h} · hc={hc} · eps={eps:g} · hc_eps={hc_eps:g} · "
          f"{len(fn)} lignes de mélange")

    emb = g.lire("token_embd.weight", (min(ids), max(ids) + 1))
    # Les positions évaluées se lisent dans les VIDES : `--limit N` n'exécute que
    # les N premiers jetons, alors que le fichier d'identifiants peut en contenir
    # des milliers. Supposer « tout le fichier » demandait des fichiers absents.
    import glob
    positions = sorted(int(f.rsplit("-", 1)[1][:-4])
                       for f in glob.glob(f"{prefixe}-hc_attn_pre-0-*.bin"))
    print(f"# positions vides : {positions}")
    echecs = 0
    for pos in positions:
        tok = ids[pos]
        pre = dump(prefixe, "hc_attn_pre", couche, pos)
        ligne = emb[tok - min(ids)]
        e1 = np.max(np.abs(pre - ligne))
        # 2. les mélanges du raccord FFN
        xin = dump(prefixe, "hc_ffn_in", couche, pos)
        mel_attendu = dump(prefixe, "hc_ffn_pre", couche, pos)
        # ④ le maillon central : le repliement de l'entrée de la FFN
        pre_attn = dump(prefixe, "hc_pre_attn", couche, pos)
        mel_ffn = dump(prefixe, "hc_mel_ffn", couche, pos)
        mel_calcule = (pre_attn.reshape(hc, 1) * xin.reshape(hc, h)).sum(axis=0)
        e4 = np.max(np.abs(mel_calcule - mel_ffn))
        plat = xin / np.sqrt(np.mean(xin * xin) + eps)
        mixes = fn @ plat
        sig = 1.0 / (1.0 + np.exp(-(mixes[:hc] * scale[0] + base[:hc])))
        mel = sig + hc_eps
        e2 = np.max(np.abs(mel - mel_attendu))
        # 3. la tête : repliement par `hc_ffn_pre` puis norme finale
        llast = dump(prefixe, "l_last", couche, pos).reshape(hc, h)
        attendu = rms_norm((mel_attendu.reshape(hc, 1) * llast).sum(axis=0), norme, eps)
        obtenu = dump(prefixe, "hidden_final", couche, pos)
        e3 = np.max(np.abs(attendu - obtenu))
        dyn = np.max(np.abs(obtenu))
        etat = "OK " if max(e1, e2, e3, e4) < 1e-4 * max(dyn, 1e-9) + 1e-6 else "ÉCART"
        print(f"  pos {pos} (jeton {tok}) : copie0 {e1:.3e} · mélanges {e2:.3e} · "
              f"repli FFN {e4:.3e} · tête {e3:.3e}   (dynamique {dyn:.3e})  {etat}")
        if etat == "ÉCART":
            echecs += 1
    print("VERDICT : " + ("les quatre égalités tiennent" if echecs == 0
                          else f"{echecs} position(s) en écart"))
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
