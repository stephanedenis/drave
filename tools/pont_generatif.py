#!/usr/bin/env python3
"""pont_generatif.py — le réseau NAÎT, puis subit une ATTRITION qui le fait généraliser.

Deux phases, dans cet ordre, et c'est l'apprentissage qui décide des tailles.

PHASE GÉNÉRATIVE. On part d'un seul neurone. Chaque pas de croissance ajoute une
COUCHE de neurones. Une couche nouvelle ne lit que les couches ANTÉRIEURES (plus
elle-même) : jamais l'inverse. Conséquence exacte, et c'est ce qui rend la
croissance gratuite — les trajectoires déjà calculées ne sont PAS perturbées, on
ne calcule que la couche qui naît. Le coût total de la croissance vaut donc à peu
près celui du réseau final, pas la somme de tous les états intermédiaires.

PHASE D'ATTRITION. Périodiquement, on retire les neurones REDONDANTS — ceux dont
la trajectoire se reconstruit à partir des autres — puis on RÉAJUSTE la lecture
sur les survivants. C'est le réajustement qui fait généraliser : la capacité
retirée doit être réabsorbée par les unités qui restent, ce qui remplace des
détecteurs particuliers par des concepts plus larges. Une coupe qui ne réajuste
pas ne généralise rien, elle appauvrit.

Rien ne se rétropropage : A et B sont aléatoires et GELÉS, seule la lecture W
s'ajuste par moindres carrés ridgés.

Usage :
  pont_generatif.py <train.npz> <test.npz> [--a 0.2] [--ride 0.3] [--val 4]
                    [--attrition 1] [--seuil 0.02] [--max-couches 9] [--graine 5]
"""
import sys
import numpy as np


# ------------------------------------------------------------------ lecture
def charge(p):
    z = np.load(p, allow_pickle=True)
    cles = [str(c) for c in z["cles"]]
    E = [z[f"E{i}"].astype(np.float32) for i in range(len(cles))]
    Y = [z[f"Y{i}"].astype(np.float32) for i in range(len(cles))]
    return cles, E, Y, int(z["hidden"])


def cos_lignes(A, B):
    na = np.linalg.norm(A, axis=1); nb = np.linalg.norm(B, axis=1)
    ok = (na > 0) & (nb > 0)
    return float(np.mean(np.sum(A[ok]*B[ok], axis=1)/(na[ok]*nb[ok])))


def inv(V):
    n = np.linalg.norm(V, axis=1, keepdims=True); n[n == 0] = 1
    S = (V/n) @ (V/n).T
    iu = np.triu_indices(len(V), 1)
    return float(S[iu].mean()), float(S[iu].min())


# ------------------------------------------------------------------ le pont
class Pont:
    """Réseau récurrent en CASCADE : une couche ne lit que les précédentes."""

    def __init__(self, donnees, a, graine, H, decal=0):
        self.langues, self.E, self.Y = donnees
        self.a = a
        self.H = H
        self.rng = np.random.RandomState(graine + decal)
        self.X = [np.zeros((len(e), 0), dtype=np.float32) for e in self.E]
        self.couches = []          # taille de chaque couche, dans l'ordre de naissance
        self.compte_neurones = 0
        # GÉNÉALOGIE : pour chaque neurone né, ses poids (vers 0..j, lui compris) et
        # sa couche. Sans elle, on ne peut pas RECALCULER les survivants seuls — et
        # une attrition qu'on ne peut pas recalculer ne réduit rien : elle ne fait
        # que masquer des colonnes dont la trajectoire a été calculée par les autres.
        self.poids = []            # (w de longueur j+1, b de longueur H, couche)
        self.couche_de = []

    # -- croissance : ajoute UNE couche de k neurones -----------------------
    def nait(self, k):
        n_avant = self.compte_neurones
        n_apres = n_avant + k
        # la couche lit les n_avant neurones existants ET elle-même (récurrence)
        W = self.rng.randn(k, n_apres) / np.sqrt(max(n_apres, 1))
        B = self.rng.randn(k, self.H) / np.sqrt(self.H)
        for i, (E, X) in enumerate(zip(self.E, self.X)):
            T = len(E)
            S = np.zeros((T, k), dtype=np.float32)
            s = np.zeros(k)
            for t in range(T):
                # les couches ANTÉRIEURES sont lues à t-1 : elles ne bougent pas
                drive = (X[t-1] @ W[:, :n_avant].T) if (t > 0 and n_avant > 0) else 0.0
                s = (1-self.a)*s + self.a*np.tanh(drive + W[:, n_avant:] @ s + B @ E[t])
                S[t] = s
            self.X[i] = np.hstack([X, S])
        for r in range(k):
            self.poids.append((W[r].copy(), B[r].copy(), len(self.couches)))
        self.couches.append(k)
        self.compte_neurones = n_apres
        return n_apres

    # -- lecture : moindres carrés ridgés sur un SOUS-ENSEMBLE de neurones ---
    def ajuste(self, idx, ride, mt, quel=slice(None)):
        X = np.vstack([self.X[i][:, idx] for i in quel])
        Y = np.vstack([self.Y[i] for i in quel])
        n = X.shape[1]
        return np.linalg.solve(X.T @ X + ride*len(X)*np.eye(n), X.T @ (Y - mt))

    def fid(self, idx, W, mt, quel):
        X = np.vstack([self.X[i][:, idx] for i in quel])
        Y = np.vstack([self.Y[i] for i in quel])
        return cos_lignes(X @ W + mt, Y)

    def dernier(self, idx, W, mt, quel):
        return np.array([(self.X[i][:, idx] @ W + mt)[-1] for i in quel])

    def redondance(self, W, idx):
        """Part de chaque neurone qui est DÉJÀ DITE par les autres.

        On cherche les neurones dont la trajectoire se reconstruit à partir des
        autres : ce sont eux qui portent un concept particulier là où un concept
        plus général suffirait. Le retrait par contribution, lui, ne fait que
        couper les faibles — il n'énonce rien.

        Le calcul est exact et tient en UNE inversion. Pour la matrice de Gram
        `G = XᵀX`, la part de variance de `x_j` non expliquée par les autres vaut
        le complément de Schur `1/(G⁻¹)_jj`, donc la part EXPLIQUÉE vaut
        `1 − 1/((G⁻¹)_jj · G_jj)` — sans jamais inverser K matrices (K−1)×(K−1).

        On retire en premier ceux qui sont à la fois **expliqués** et **utiles** :
        `score = expliqué × contribution`.
        """
        X = np.vstack([x[:, idx] for x in self.X]).astype(np.float64)
        G = X.T @ X
        d = np.diag(G).copy()
        d[d == 0] = 1.0
        Gi = np.linalg.inv(G + 1e-6*np.trace(G)/len(G)*np.eye(len(G)))
        explique = 1.0 - (1.0/np.diag(Gi))/d
        explique = np.clip(explique, 0.0, 1.0)
        return explique * self.contribution(W, idx)

    def contribution(self, W, idx):
        """Énergie que chaque neurone apporte à la sortie : ||w_k|| · ||x_k||.

        Calculée sur les SEULS neurones vivants : après un retrait, `W` a la taille
        des survivants et non celle du réseau né."""
        X = np.vstack([x[:, idx] for x in self.X]).astype(np.float64)
        nx = np.sqrt((X**2).sum(0)) / np.sqrt(len(X))
        return nx * np.linalg.norm(W, axis=1)

    # -- RECALCUL HONNÊTE : on refait les trajectoires des SEULS survivants ---
    def recalcule(self, S, Ek=None):
        """Reconstruit le réseau réduit à `S` et rend ses trajectoires.

        Les neurones retirés ne contribuent plus RIEN. C'est la seule façon de
        savoir si la réduction est réelle ou cosmétique : un neurone de 9e couche
        dont la trajectoire a été calculée par 256 autres n'est pas « un neurone »,
        c'est une caractéristique profonde, et l'annoncer comme tel serait mentir.

        La récurrence des survivants est la même que celle qui les a fait naître —
        `s = (1-a)s + a·tanh(Ps·s + Bs·e)` — où `Ps` ne porte que les poids des
        survivants vers les survivants.
        """
        S = list(S)
        K = len(S)
        Ps = np.zeros((K, K))
        for r, j in enumerate(S):
            w = self.poids[j][0]
            for rr, pj in enumerate(S[:r]):
                if pj < j:
                    Ps[r, rr] = w[pj]          # prédécesseur survivant
            Ps[r, r] = w[j]                    # soi-même
        Bs = np.array([self.poids[j][1] for j in S])
        Xn = []
        for E in (self.E if Ek is None else Ek):
            T = len(E)
            Sst = np.zeros((T, K), dtype=np.float32)
            s = np.zeros(K)
            for t in range(T):
                s = (1-self.a)*s + self.a*np.tanh(Ps @ s + Bs @ E[t])
                Sst[t] = s
            Xn.append(Sst)
        return Xn

    def evalue(self, X, Y, W, mt):
        Xa = np.vstack(X); Ya = np.vstack(Y)
        return cos_lignes(Xa @ W + mt, Ya)

    def invariance(self, X, W, mt):
        return inv(np.array([(x @ W + mt)[-1] for x in X]))

    def couches_de(self, S):
        return sorted({self.poids[j][2] for j in S})


def main():
    tr_p, te_p = sys.argv[1], sys.argv[2]
    def opt(nom, defaut):
        return sys.argv[sys.argv.index(nom)+1] if nom in sys.argv else defaut
    a = float(opt("--a", 0.2))
    ride = float(opt("--ride", 0.3))
    n_val = int(opt("--val", 4))
    attrition = int(opt("--attrition", 1))
    seuil = float(opt("--seuil", 0.02))
    max_couches = int(opt("--max-couches", 9))
    graine = int(opt("--graine", 5))
    part = float(opt("--part", 1.0))   # fraction des langues d'entraînement utilisées
    critere = opt("--critere", "contribution")

    cltr, Etr, Ytr, H = charge(tr_p)
    clte, Ete, Yte, _ = charge(te_p)
    if part < 1.0:
        garde = max(1, int(len(cltr)*part))
        cltr, Etr, Ytr = cltr[:garde], Etr[:garde], Ytr[:garde]
    ival = list(range(n_val))                       # VALIDATION : langues d'entraînement
    itr = list(range(n_val, len(cltr)))             # APPRENTISSAGE
    ite = list(range(len(clte)))                    # TEST : jamais touché avant le rapport
    print(f"# {len(cltr)} langues d'entraînement = {len(itr)} apprentissage + {len(ival)} validation")
    print(f"# {len(clte)} langues de TEST · a={a} · ride={ride} · graine={graine}")
    print(f"# entraînement {sum(len(Etr[i]) for i in itr)} pas · validation "
          f"{sum(len(Etr[i]) for i in ival)} pas · test {sum(len(Ete[i]) for i in ite)} pas")

    d_tr = (cltr, Etr, Ytr)
    P = Pont(d_tr, a, graine, H)
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)
    tout = np.arange(0)

    print(f"\n{'après':<26} {'taille':>7} {'couch.':>7} {'fid appr':>9} {'fid VAL':>8} "
          f"{'fid TEST':>9} {'invar.':>8} {'pire':>7}")
    f_val_prec = -1.0
    for pas in range(max_couches):
        k = max(1, P.compte_neurones)          # chaque couche double le réseau
        P.nait(k)
        idx = np.arange(P.compte_neurones)
        W = P.ajuste(idx, ride, mt, itr)
        f_tr = P.fid(idx, W, mt, itr)
        f_va = P.fid(idx, W, mt, ival)
        etq = f"naissance couche {len(P.couches)} (+{k})"
        Xte_g = P.recalcule(idx, Ete)
        f_te = P.evalue(Xte_g, Yte, W, mt)
        mg, mig = P.invariance(Xte_g, W, mt)
        print(f"{etq:<26} {P.compte_neurones:>7} {len(P.couches):>7} {f_tr:>9.4f} {f_va:>8.4f} "
              f"{f_te:>9.4f} {mg:>8.4f} {mig:>7.4f}")
        if P.compte_neurones >= 256 and pas >= 4:
            break

    # ---------------------------------------------------------- ATTRITION
    #
    # On ne retire pas des COLONNES de lecture : on retire des NEURONES, puis on
    # RECALCULE les trajectoires des survivants sans les retirés. Sans ce recalcul,
    # « 1 neurone » ne voudrait rien dire — la trajectoire de ce neurone aurait été
    # calculée par les 256 autres.
    #
    # Le critère compare au MEILLEUR score de validation atteint, jamais au score
    # courant : comparer au courant transforme l'attrition en marche aléatoire vers
    # le bas, chaque pas étant petit mais la somme ne l'étant pas.
    vivants = list(range(P.compte_neurones))
    if attrition:
        print(f"\n# ATTRITION ({critere}) — on retire des NEURONES, on RECALCULE les "
              f"survivants, on RÉAJUSTE, et on garde si la validation tient")
        print(f"{'après':<30} {'neur.':>6} {'couch.':>7} {'fid appr':>9} {'fid VAL':>8} "
              f"{'fid TEST':>9}")
        idx = np.arange(len(vivants))
        W = P.ajuste(idx, ride, mt, itr)
        f_va = P.fid(idx, W, mt, ival)
        Xte_a = P.recalcule(vivants, Ete)
        print(f"{'réseau né (référence)':<30} {len(vivants):>6} {len(P.couches):>7} "
              f"{P.fid(idx, W, mt, itr):>9.4f} {f_va:>8.4f} "
              f"{P.evalue(Xte_a, Yte, W, mt):>9.4f}")
        meilleur = f_va
        while len(vivants) > 1:
            contrib = (P.redondance(W, idx) if critere == "redondance"
                   else P.contribution(W, idx))
            n_ret = max(1, len(vivants)//4)
            ordre = np.argsort(contrib)
            garde = sorted(vivants[i] for i in ordre[n_ret:])
            if len(garde) == len(vivants):
                break
            X2 = P.recalcule(garde)                 # <- le recalcul honnête
            X_sauve, P.X = P.X, X2
            idx2 = np.arange(len(garde))
            W2 = P.ajuste(idx2, ride, mt, itr)
            f2 = P.fid(idx2, W2, mt, ival)
            if f2 < meilleur - seuil:
                P.X = X_sauve
                print(f"{'retrait REFUSÉ (' + str(n_ret) + ' → VAL ' + format(f2, '.4f') + ')':<30} "
                      f"{len(vivants):>6} {'—':>7} {'—':>9} {f_va:>8.4f}")
                break
            vivants, idx, W, f_va = garde, idx2, W2, f2
            meilleur = max(meilleur, f_va)
            Xte_a = P.recalcule(vivants, Ete)
            print(f"{'retrait de ' + str(n_ret) + ' (recalculé)':<30} {len(vivants):>6} "
                  f"{len(P.couches_de(vivants)):>7} {P.fid(idx, W, mt, itr):>9.4f} {f_va:>8.4f} "
                  f"{P.evalue(Xte_a, Yte, W, mt):>9.4f}")

    # ------------------------------------------------------------- RAPPORT
    idx = np.arange(len(vivants))
    W = P.ajuste(idx, ride, mt, itr)
    f_tr = P.fid(idx, W, mt, itr)
    # Le TEST se calcule sur les trajectoires des langues TENUES À L'ÉCART,
    # produites par le réseau RÉDUIT — jamais sur les langues d'entraînement.
    Xte_red = P.recalcule(vivants, Ete)
    f_te = P.evalue(Xte_red, Yte, W, mt)
    m, mi = P.invariance(Xte_red, W, mt)
    Yte_a = np.vstack(Yte)
    base = cos_lignes(np.tile(mt, (len(Yte_a), 1)), Yte_a)
    print(f"\n=== RÉSEAU FINAL (trajectoires RECALCULÉES, pas masquées) ===")
    print(f"  taille           : {len(vivants)} neurones · {len(P.couches_de(vivants))} couches "
          f"réellement nécessaires (sur {len(P.couches)} nées)")
    print(f"  nées par couche  : {P.couches}")
    print(f"  fidélité appr.   : {f_tr:.4f}")
    print(f"  fidélité TEST    : {f_te:.4f}      (constante témoin : {base:.4f})")
    print(f"  invariance TEST  : {m:.4f} · pire paire {mi:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
