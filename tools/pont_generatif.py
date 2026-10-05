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
    """Réseau récurrent PROFOND : chaque couche ne lit que la PRÉCÉDENTE.

    C'est ce qui donne un sens au mot « couche ». Dans la version précédente,
    chaque neurone lisait TOUS les neurones nés avant lui, quelle que soit leur
    couche : ouvrir une couche ou ajouter un neurone y produisaient exactement le
    même calcul (vérifié — n=104 donnait 0,4930 / 0,9368 dans les deux cas). Les
    24 « couches » n'étaient qu'une numérotation.

    Ici :
      - un neurone de la couche 0 lit l'entrée `e_t` et les siens (récurrence) ;
      - un neurone de la couche c lit la couche c-1 ENTIÈRE (au même instant t)
        et les siens, nés avant lui ;
      - il ne lit JAMAIS les couches plus basses directement.

    Conséquence voulue : on peut ÉPUISER une couche — y ajouter les neurones qui
    manquent pour les activations non encore couvertes — sans que cela revienne à
    créer de la profondeur. Une couche neuve ne se justifie que lorsqu'elle
    compose ce que la précédente ne sait plus séparer : le « OU exclusif » après
    le « ET » et le « OU ».
    """

    def __init__(self, donnees, a, graine, H, decal=0):
        self.langues, self.E, self.Y = donnees
        self.a = a
        self.H = H
        self.rng = np.random.RandomState(graine + decal)
        self.X = [np.zeros((len(e), 0), dtype=np.float32) for e in self.E]
        self.couches = []          # taille de chaque couche, dans l'ordre
        self.compte_neurones = 0
        # GÉNÉALOGIE : de quoi RECALCULER un sous-ensemble de survivants sans les
        # retirés. Sans elle, une attrition ne réduit rien — elle masque.
        # Chaque neurone : (w_parents, w_couche, b, couche)
        self.poids = []

    # -- indices -------------------------------------------------------------
    def debut_couche(self, c):
        return sum(self.couches[:c])

    def taille_couche(self, c):
        return self.couches[c] if 0 <= c < len(self.couches) else 0

    # -- naissance -----------------------------------------------------------
    def nait(self, k, nouvelle_couche=True):
        """Fait naître k neurones, soit dans une couche NEUVE, soit dans la
        couche courante (pour couvrir les activations qui manquent encore)."""
        n_avant = self.compte_neurones
        if nouvelle_couche or not self.couches:
            c = len(self.couches)
            deja = 0
            c_par = c - 1
        else:
            c = len(self.couches) - 1
            deja = self.couches[-1]
            c_par = c - 1
        n_par = self.taille_couche(c_par) if c_par >= 0 else 0
        debut_par = self.debut_couche(c_par) if c_par >= 0 else 0

        W_par = (self.rng.randn(k, n_par) / np.sqrt(max(n_par, 1))
                 if n_par > 0 else np.zeros((k, 0)))
        W_self = self.rng.randn(k, deja + k) / np.sqrt(max(deja + k, 1))
        B = self.rng.randn(k, self.H) / np.sqrt(self.H)

        for i, (E, X) in enumerate(zip(self.E, self.X)):
            T = len(E)
            Xpar = (X[:, debut_par:debut_par+n_par] if n_par > 0
                    else np.zeros((T, 0), dtype=np.float32))
            S = np.zeros((T, k), dtype=np.float32)
            s = np.zeros(deja + k)          # l'état de la couche : anciens + neufs
            for t in range(T):
                # la couche PRÉCÉDENTE est lue au même instant t : elle est déjà
                # entièrement calculée, et elle ne bougera plus.
                drive = (Xpar[t] @ W_par.T) if n_par > 0 else 0.0
                drive = drive + s @ W_self.T
                s = np.concatenate([s[:deja],
                                    (1-self.a)*s[deja:] + self.a*np.tanh(drive + B @ E[t])])
                S[t] = s[deja:]
            self.X[i] = np.hstack([X, S])

        for r in range(k):
            self.poids.append((W_par[r].copy(), W_self[r].copy(), B[r].copy(), c))
        if nouvelle_couche or not self.couches:
            self.couches.append(k)
        else:
            self.couches[-1] += k
        self.compte_neurones += k
        return self.compte_neurones

    # -- lecture -------------------------------------------------------------
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

    # -- critères d'attrition ------------------------------------------------
    def contribution(self, W, idx):
        """Énergie que chaque neurone apporte à la sortie : ||w_k|| · ||x_k||."""
        X = np.vstack([x[:, idx] for x in self.X]).astype(np.float64)
        nx = np.sqrt((X**2).sum(0)) / np.sqrt(len(X))
        return nx * np.linalg.norm(W, axis=1)

    def redondance(self, W, idx):
        """Part de chaque neurone DÉJÀ DITE par les autres.

        Pour la Gram `G = XᵀX`, la variance de `x_j` non expliquée par les autres
        est le complément de Schur `1/(G⁻¹)_jj`, donc la part expliquée vaut
        `1 − 1/((G⁻¹)_jj · G_jj)` — une seule inversion, pas K.
        On retire en premier ceux qui sont à la fois expliqués ET utiles.
        """
        X = np.vstack([x[:, idx] for x in self.X]).astype(np.float64)
        G = X.T @ X
        d = np.diag(G).copy(); d[d == 0] = 1.0
        Gi = np.linalg.inv(G + 1e-6*np.trace(G)/len(G)*np.eye(len(G)))
        explique = np.clip(1.0 - (1.0/np.diag(Gi))/d, 0.0, 1.0)
        return explique * self.contribution(W, idx)

    # -- RECALCUL HONNÊTE ----------------------------------------------------
    def recalcule(self, S, Ek=None):
        """Refait les trajectoires des SEULS survivants, couche par couche.

        Les retirés ne contribuent plus rien. C'est la seule façon de savoir si
        une réduction est réelle : un neurone dont la trajectoire a été calculée
        par d'autres n'est pas « un neurone », c'est une caractéristique profonde.
        """
        S = list(S)
        pos = {j: r for r, j in enumerate(S)}
        EK = self.E if Ek is None else Ek
        Xn = [np.zeros((len(E), len(S)), dtype=np.float32) for E in EK]
        for c in sorted({self.poids[j][3] for j in S}):
            membres = [j for j in S if self.poids[j][3] == c]
            par = [j for j in S if self.poids[j][3] == c-1]
            ipar = [pos[j] for j in par]
            imem = [pos[j] for j in membres]
            m = len(membres)
            # poids des parents survivants vers chaque membre, et poids internes
            Pp = np.zeros((m, len(par)))
            Ps = np.zeros((m, m))
            for r, j in enumerate(membres):
                wp, ws, _, _ = self.poids[j]
                for q, pj in enumerate(par):
                    if pj - self.debut_couche(c-1) < len(wp):
                        Pp[r, q] = wp[pj - self.debut_couche(c-1)]
                for q, mj in enumerate(membres[:r+1]):
                    if mj - self.debut_couche(c) < len(ws):
                        Ps[r, q] = ws[mj - self.debut_couche(c)]
            Bs = np.array([self.poids[j][2] for j in membres])
            for i, E in enumerate(EK):
                T = len(E)
                Xpar = Xn[i][:, ipar] if ipar else np.zeros((T, 0), dtype=np.float32)
                s = np.zeros(m)
                for t in range(T):
                    drive = (Xpar[t] @ Pp.T) if ipar else 0.0
                    s = (1-self.a)*s + self.a*np.tanh(drive + s @ Ps.T + Bs @ E[t])
                    Xn[i][t, imem] = s
        return Xn

    def compacte(self, S):
        """Réécrit la généalogie sur les survivants et renumérote les couches."""
        S = list(S)
        # les trajectoires se calculent AVANT le remappage : `recalcule` lit
        # `self.poids` avec les indices de l'ancienne numérotation.
        Xn = self.recalcule(S)
        nouvelles = []
        tailles = {}
        for j in S:
            c = self.poids[j][3]
            tailles[c] = tailles.get(c, 0) + 1
        renomme = {c: i for i, c in enumerate(sorted(tailles))}
        for j in S:
            wp, ws, b, c = self.poids[j]
            nouvelles.append((wp.copy(), ws.copy(), b.copy(), renomme[c]))
        self.poids = nouvelles
        self.X = Xn
        self.couches = [tailles[c] for c in sorted(tailles)]
        self.compte_neurones = len(S)
        return len(S)

    def couches_de(self, S):
        return sorted({self.poids[j][3] for j in S})

    def evalue(self, X, Y, W, mt):
        return cos_lignes(np.vstack(X) @ W + mt, np.vstack(Y))

    def invariance(self, X, W, mt):
        return inv(np.array([(x @ W + mt)[-1] for x in X]))


def main():
    tr_p, te_p = sys.argv[1], sys.argv[2]

    def opt(nom, defaut):
        return sys.argv[sys.argv.index(nom)+1] if nom in sys.argv else defaut

    a = float(opt("--a", 0.2))
    ride = float(opt("--ride", 0.3))
    n_val = int(opt("--val", 4))
    attrition = int(opt("--attrition", 1))
    seuil = float(opt("--seuil", 0.02))
    graine = int(opt("--graine", 5))
    part = float(opt("--part", 1.0))
    critere = opt("--critere", "redondance")
    cycles = int(opt("--cycles", 3))
    par_cycle = int(opt("--couches-par-cycle", 3))
    plafond = int(opt("--plafond", 256))

    cltr, Etr, Ytr, H = charge(tr_p)
    clte, Ete, Yte, _ = charge(te_p)
    if part < 1.0:
        garde = max(1, int(len(cltr)*part))
        cltr, Etr, Ytr = cltr[:garde], Etr[:garde], Ytr[:garde]
    ival = list(range(n_val))
    itr = list(range(n_val, len(cltr)))
    ite = list(range(len(clte)))
    print(f"# {len(cltr)} langues d'entraînement = {len(itr)} apprentissage + {len(ival)} validation")
    print(f"# {len(clte)} langues de TEST · a={a} · ride={ride} · graine={graine} · critère={critere}")
    print(f"# {cycles} cycles de {par_cycle} couches, puis attrition")
    print(f"# pas — apprentissage {sum(len(Etr[i]) for i in itr)} · validation "
          f"{sum(len(Etr[i]) for i in ival)} · test {sum(len(Ete[i]) for i in ite)}")

    P = Pont((cltr, Etr, Ytr), a, graine, H)
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)
    Yte_a = np.vstack(Yte)
    base = cos_lignes(np.tile(mt, (len(Yte_a), 1)), Yte_a)
    print(f"# constante témoin sur le TEST : {base:.4f}")

    meilleur = {"f_va": -1.0, "f_te": -1.0}
    for cycle in range(1, cycles+1):
        # ------------------------------------------------------- CROISSANCE
        print(f"\n########## CYCLE {cycle} — CROISSANCE ##########")
        print(f"{'après':<30} {'neur.':>6} {'couch.':>7} {'fid appr':>9} {'fid VAL':>8} "
              f"{'fid TEST':>9} {'invar.':>8} {'pire':>7}")
        # ------------------------------------------------------------ NAISSANCE
        #
        # `--naissance libre` : UN neurone à la fois, et c'est l'apprentissage qui
        # décide. Aucun chiffre rond ne doit sortir d'ici — 1, 2, 4, 8, 16, 32,
        # 64, 128, 256 étaient MON calendrier et MON plafond, pas une découverte.
        # Un compte rond est le signe qu'on a choisi la taille au lieu de la
        # mesurer.
        #
        # ET ON ÉPUISE LA COUCHE AVANT D'EN OUVRIR UNE. Un neurone seul sait faire
        # « ET » et « OU » ; il faut une SECONDE couche pour un « OU exclusif ».
        # Ouvrir une couche dèsl que le dernier neurône rapporte moins que la
        # moyenne de sa couche, c'est vouloir le XOR avant d'avoir fini le ET et
        # le OU — et c'est mesurablement mauvais : la première version de cette
        # règle ouvrait 24 couches pour 128 neurones et donnait 0,4937 de fidélité
        # de test, contre 0,5059 pour la même taille en 8 couches.
        #
        # D'où deux phases, et le passage de l'une à l'autre est une MESURE :
        #   A. on ajoute des neurones à la couche courante tant qu'ils paient ;
        #   B. quand elle est SATURÉE, on essaie une couche neuve — et on continue
        #      seulement si son premier neurone paie.
        if opt("--naissance", "") == "libre":
            gain_min = float(opt("--gain-min", 0.0002))
            patience = int(opt("--patience", 12))
            val_max = -1.0
            sans_gain = 0
            saturee = 0
            while P.compte_neurones < plafond:
                # en phase A on remplit la couche ; en phase B on en ouvre une
                nouvelle = (saturee >= patience) or not P.couches
                P.nait(1, nouvelle_couche=nouvelle)
                idx = np.arange(P.compte_neurones)
                W = P.ajuste(idx, ride, mt, itr)
                f_tr = P.fid(idx, W, mt, itr); f_va = P.fid(idx, W, mt, ival)
                gain = f_va - val_max if val_max > 0 else 0.0
                if f_va > val_max:
                    val_max = f_va
                if nouvelle:
                    saturee = 0
                if gain < gain_min:
                    sans_gain += 1
                    saturee += 1
                else:
                    sans_gain = 0
                    saturee = 0
                if P.compte_neurones % 8 == 0 or nouvelle or sans_gain >= patience:
                    Xte_g = P.recalcule(idx, Ete)
                    f_te = P.evalue(Xte_g, Yte, W, mt)
                    mg, mig = P.invariance(Xte_g, W, mt)
                    print(f"{'n' + str(P.compte_neurones) + (' COUCHE ' + str(len(P.couches)) if nouvelle else ''):<30} "
                          f"{P.compte_neurones:>6} {len(P.couches):>7} {f_tr:>9.4f} {f_va:>8.4f} "
                          f"{f_te:>9.4f} {mg:>8.4f} {mig:>7.4f}")
                    if f_va > meilleur["f_va"]:
                        meilleur = {"f_te": f_te, "neur": P.compte_neurones,
                                    "couch": len(P.couches), "f_tr": f_tr, "f_va": f_va,
                                    "inv": mg, "pire": mig, "etape": "naissance libre"}
                # on ne s'arrête que si une COUCHE NEUVE ne paie pas non plus :
                # tant qu'on est en phase A, une couche saturée n'est pas la fin.
                if sans_gain >= 2*patience:
                    print(f"{'  → ARRÊT (couche neuve sans gain)':<30} "
                          f"{P.compte_neurones:>6} {len(P.couches):>7}")
                    break
            print(f"# née : {P.compte_neurones} neurones en {len(P.couches)} couches "
                  f"{P.couches}")
            break

        arret_naissance = opt("--arret-naissance", "")
        gain_naissance = float(opt("--gain-naissance", 0.001))
        sans_gain = 0
        val_prec = None
        for _ in range(par_cycle):
            # Cycle 1 : chaque couche DOUBLE (1,1,2,4,…) pour atteindre vite la
            # zone utile. Cycles suivants : on AJOUTE sans doubler — le réseau a
            # déjà une taille qui compte, et doubler le ferait exploser.
            k = (max(1, P.compte_neurones) if cycle == 1
                 else max(2, P.compte_neurones//4))
            if P.compte_neurones + k > plafond:
                k = plafond - P.compte_neurones
            if k <= 0:
                break
            P.nait(k)
            idx = np.arange(P.compte_neurones)
            W = P.ajuste(idx, ride, mt, itr)
            f_tr = P.fid(idx, W, mt, itr); f_va = P.fid(idx, W, mt, ival)
            Xte_g = P.recalcule(idx, Ete)
            f_te = P.evalue(Xte_g, Yte, W, mt); mg, mig = P.invariance(Xte_g, W, mt)
            print(f"{'C' + str(cycle) + ' naissance couche ' + str(len(P.couches)) + ' (+' + str(k) + ')':<30} "
                  f"{P.compte_neurones:>6} {len(P.couches):>7} {f_tr:>9.4f} {f_va:>8.4f} "
                  f"{f_te:>9.4f} {mg:>8.4f} {mig:>7.4f}")
            # SÉLECTION SUR LA VALIDATION, jamais sur le test : choisir le réseau
            # d'après son score de test serait regarder la réponse avant de choisir.
            if f_va > meilleur["f_va"]:
                meilleur = {"f_te": f_te, "neur": P.compte_neurones,
                            "couch": len(P.couches), "f_tr": f_tr, "f_va": f_va,
                            "inv": mg, "pire": mig, "etape": f"C{cycle} croissance"}
            if val_prec is not None and f_va - val_prec < gain_naissance:
                sans_gain += 1
            else:
                sans_gain = 0
            val_prec = max(val_prec, f_va) if val_prec is not None else f_va
            if arret_naissance and sans_gain >= 3:
                print(f"{'  → naissance ARRÊTÉE (3 sans gain)':<30} {P.compte_neurones:>6} "
                      f"{len(P.couches):>7}")
                break
        # -------------------------------------------------------- ATTRITION
        if not attrition:
            continue
        print(f"\n########## CYCLE {cycle} — ATTRITION ({critere}) ##########")
        print(f"{'après':<30} {'neur.':>6} {'couch.':>7} {'fid appr':>9} {'fid VAL':>8} "
              f"{'fid TEST':>9}")
        idx = np.arange(P.compte_neurones)
        W = P.ajuste(idx, ride, mt, itr)
        f_va = P.fid(idx, W, mt, ival)
        meilleur_val = f_va
        while len(idx) > 1:
            sc = (P.redondance(W, idx) if critere == "redondance"
                  else P.contribution(W, idx))
            n_ret = max(1, len(idx)//4)
            ordre = np.argsort(sc)
            garde = sorted(int(i) for i in ordre[n_ret:])
            if len(garde) == len(idx):
                break
            X2 = P.recalcule(garde)
            X_sauve, P.X = P.X, X2
            idx2 = np.arange(len(garde))
            W2 = P.ajuste(idx2, ride, mt, itr)
            f2 = P.fid(idx2, W2, mt, ival)
            if f2 < meilleur_val - seuil:
                P.X = X_sauve
                print(f"{'retrait REFUSÉ (' + str(n_ret) + ' → VAL ' + format(f2, '.4f') + ')':<30} "
                      f"{len(idx):>6} {'—':>7} {'—':>9} {f_va:>8.4f}")
                break
            idx, W, f_va = idx2, W2, f2
            meilleur_val = max(meilleur_val, f_va)
            Xte_a = P.recalcule(garde, Ete)
            f_te = P.evalue(Xte_a, Yte, W, mt)
            print(f"{'retrait de ' + str(n_ret) + ' (recalculé)':<30} {len(garde):>6} "
                  f"{len(P.couches_de(garde)):>7} {P.fid(idx, W, mt, itr):>9.4f} {f_va:>8.4f} "
                  f"{f_te:>9.4f}")
            if f_va > meilleur["f_va"]:
                mv, miv = P.invariance(Xte_a, W, mt)
                meilleur = {"f_te": f_te, "neur": len(garde),
                            "couch": len(P.couches_de(garde)),
                            "f_tr": P.fid(idx, W, mt, itr), "f_va": f_va,
                            "inv": mv, "pire": miv, "etape": f"C{cycle} attrition"}
            # on COMPACTE : la croissance du cycle suivant doit partir des survivants
            P.compacte(garde)

    print(f"\n=== MEILLEUR RÉSEAU SELON LA VALIDATION ({meilleur['etape']}) ===")
    print(f"  taille           : {meilleur['neur']} neurones · {meilleur['couch']} couches")
    print(f"  fidélité appr.   : {meilleur['f_tr']:.4f}")
    print(f"  fidélité VAL     : {meilleur['f_va']:.4f}")
    print(f"  fidélité TEST    : {meilleur['f_te']:.4f}   (constante témoin : {base:.4f})")
    print(f"  invariance TEST  : {meilleur['inv']:.4f} · pire paire {meilleur['pire']:.4f}")
    print(f"\n# état final du réseau : {P.compte_neurones} neurones · {len(P.couches)} couches "
          f"({P.couches})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
