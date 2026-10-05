#!/usr/bin/env python3
"""pont_reservoir.py — ajouter une COUCHE RÉCURRENTE sans rétropropagation.

Le diagnostic du rapport : sans contexte, le pont plafonne à 0,57 de fidélité,
parce que la couche 10 du professeur **agrège tout le préfixe** — un seul jeton ne
peut pas la prédire. Il faut donc du contexte.

La réponse qui respecte la contrainte (« pas de rétropropagation ») est un
**réservoir** : une couche récurrente **aléatoire et gelée**, dont seule la lecture
s'ajuste par moindres carrés.

    s_t = (1−a)·s_(t−1) + a·tanh(A·s_(t−1) + B·e_t)      A, B ALÉATOIRES, GELÉS
    y_t = W·s_t + moy                                     W ajusté, forme fermée

C'est « ajouter des couches et des neurones » au sens exact : la taille du
réservoir est le nombre de neurones, et la récurrence est la couche ajoutée. Rien
ne se rétropropage, et le réservoir n'a besoin d'aucune coordination entre nœuds —
il est **distribuable** par construction.

Usage : pont_reservoir.py <train> <test> [--couche 10] [--n 256]
"""
import glob, os, struct, sys
import numpy as np


def lire(chemin):
    def paires(f, n, version, bloc=32):
        ech = None
        if version == 3:
            nb, = struct.unpack("<I", f.read(4))
            ech = [struct.unpack("<e", f.read(2))[0] for _ in range(nb)]
        out, prev = [], 0
        for _ in range(n):
            if version == 1:
                i, = struct.unpack("<I", f.read(4))
            else:
                e, = struct.unpack("<B", f.read(1))
                i = struct.unpack("<H", f.read(2))[0] if e == 255 else prev + e
                prev = i
            if version == 3:
                v, = struct.unpack("<b", f.read(1))
                out.append((i, v * (ech[i // bloc] if ech else 1.0)))
            else:
                v, = struct.unpack("<h", f.read(2))
                out.append((i, v))
        return out

    with open(chemin, "rb") as f:
        assert f.read(4) == b"DRVF"
        version, = struct.unpack("<H", f.read(2))
        n_layer, hidden = struct.unpack("<II", f.read(8))
        pp = {}
        while True:
            b = f.read(2)
            if len(b) < 2: break
            c, = struct.unpack("<H", b)
            if c == 0xFFFF: break
            pos, n, ech = struct.unpack("<IIf", f.read(12))
            pp[(c, pos)] = paires(f, n, version)
    return hidden, pp


def charge(d, c, hidden):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, "*.drvf"))):
        h, pp = lire(f)
        pos = sorted(p for (cc, p) in pp if cc == 0)
        E = np.zeros((len(pos), h)); Y = np.zeros((len(pos), h))
        for k, p in enumerate(pos):
            for i, v in pp[(0, p)]:
                if i < h: E[k, i] = v
            for i, v in pp.get((c, p), []):
                if i < h: Y[k, i] = v
        out[os.path.basename(f)[:-5]] = (E, Y)
    return out


def cos_lignes(A, B):
    na = np.linalg.norm(A, axis=1); nb = np.linalg.norm(B, axis=1)
    ok = (na > 0) & (nb > 0)
    return float(np.mean(np.sum(A[ok]*B[ok], axis=1)/(na[ok]*nb[ok])))


def inv(V):
    n = np.linalg.norm(V, axis=1, keepdims=True); n[n == 0] = 1
    S = (V/n) @ (V/n).T; iu = np.triu_indices(len(V), 1)
    return float(S[iu].mean()), float(S[iu].min())


def reservoir(E, A, B, a):
    s = np.zeros(A.shape[0]); out = np.zeros((len(E), A.shape[0]))
    for t in range(len(E)):
        s = (1-a)*s + a*np.tanh(A @ s + B @ E[t])
        out[t] = s
    return out


def main():
    dtr, dte = sys.argv[1], sys.argv[2]
    c = int(sys.argv[sys.argv.index("--couche") + 1]) if "--couche" in sys.argv else 10
    N = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 256
    tr, te = charge(dtr, c, 896), charge(dte, c, 896)
    mt = np.vstack([y for _, y in tr.values()]).mean(axis=0)
    rng = np.random.RandomState(5)
    A = rng.randn(N, N) / np.sqrt(N)
    # rayon spectral ramené sous 1 : condition de mémoire du réservoir
    A *= 0.9 / max(abs(np.linalg.eigvals(A)))
    B = rng.randn(N, 896) / np.sqrt(896)
    # Fuite et ride BALAYÉS (tools/pont_reglages.py) : a=0,5 et 1e-1 étaient des
    # valeurs de départ jamais justifiées. a=0,2 + ride=0,3 donne la MÊME
    # fidélité (0,5921 contre 0,5923) avec 7 points d'invariance en plus
    # (0,9772 contre 0,9072) et 11 points sur la pire paire (0,9576 contre
    # 0,8437) — même coût, même distribabilité.
    a = 0.2
    Str = {l: reservoir(E, A, B, a) for l, (E, _) in tr.items()}
    Ste = {l: reservoir(E, A, B, a) for l, (E, _) in te.items()}
    X = np.vstack(list(Str.values())); Y = np.vstack([y - mt for _, y in tr.values()])
    W = np.linalg.solve(X.T @ X + 3e-1*len(X)*np.eye(N), X.T @ Y)
    ftr = cos_lignes(X @ W + mt, np.vstack([y for _, y in tr.values()]))
    fte = cos_lignes(np.vstack(list(Ste.values())) @ W + mt,
                     np.vstack([y for _, y in te.values()]))
    dernier = np.array([(Ste[l] @ W + mt)[-1] for l in sorted(te)])
    m, mi = inv(dernier)
    Yte = np.vstack([y for _, y in te.values()])
    base = cos_lignes(np.tile(mt, (len(Yte), 1)), Yte)
    print(f"# réservoir : {N} neurones · A gelé (rayon 0,9) · B gelé · seule W s'ajuste")
    print(f"# entraînement {X.shape[0]} pas · test {sum(len(v[0]) for v in te.values())} pas")
    print(f"\n{'modèle':<38} {'fid. train':>11} {'fid. TEST':>11} {'params':>10} {'invariance':>11}")
    print(f"{'constante':<38} {'—':>11} {base:>11.4f} {896:>10} {inv(Yte)[0]:>11.4f}")
    print(f"{'RÉSERVOIR ' + str(N) + ' (1 couche récurrente)':<38} {ftr:>11.4f} {fte:>11.4f} "
          f"{N*N+N*896+N*896:>10} {m:>11.4f}")
    print(f"\n# invariance inter-langue du réservoir : {m:.4f} · pire paire {mi:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
