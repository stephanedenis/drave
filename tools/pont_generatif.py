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
        # LECTURE NON LINÉAIRE : le readout est linéaire sur les états. Y ajouter
        # leurs carrés ne coûte qu'une inversion, reste en forme fermée, et teste
        # si le plafond de +0,020 vient de la linéarité de la lecture.
        self.quadratique = False
        # PESÉE PAR LANGUE du fit (None = moindres carrés ordinaires). Voir
        # `ajuste` : sans elle, l'objectif est ABSOLU alors que la métrique est un
        # cosinus, et les langues à forte norme dominent la lecture partagée.
        self.pese = None
        # GAIN D'ENTRÉE : en calcul réservoir c'est LE réglage critique, et il
        # valait 1,0 depuis le début sans avoir jamais été balayé. Trop petit, le
        # tanh reste linéaire et le réservoir n'est qu'un filtre ; trop grand, il
        # sature et toutes les activations se ressemblent.
        self.gain_entree = 1.0
        # NORMALISATION PAR LANGUE : l'écart entre l'oracle (0,776) et notre
        # lecture (0,638) est un écart de TRANSFERT. Les états du réservoir ont
        # un décalage et une échelle propres à chaque langue — une lecture
        # ajustée sur trente langues ne tombe pas juste sur une autre. On
        # standardise donc les états langue par langue. C'est calculable à
        # l'inférence (on connaît nos propres activations), et cela n'utilise
        # AUCUNE étiquette : ce n'est pas une fuite.
        self.normalise = False

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
        B = self.rng.randn(k, self.H) / np.sqrt(self.H) * self.gain_entree

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
    def _norm(self, X):
        if not self.normalise:
            return X
        m = X.mean(0); e = X.std(0)
        return (X - m)/np.maximum(e, 1e-6)

    def phi(self, X):
        """La base de lecture. Linéaire par défaut ; `[X, X²]` si `--lecture
        quadratique`, ce qui reste en forme fermée (une seule inversion)."""
        if not self.quadratique:
            return X
        return np.hstack([X, X*X])

    def ajuste(self, idx, ride, mt, quel=slice(None)):
        X = self.phi(np.vstack([self._norm(self.X[i][:, idx]) for i in quel]))
        Y = np.vstack([self.Y[i] for i in quel])
        n = X.shape[1]
        if self.pese is None:
            return np.linalg.solve(X.T @ X + ride*len(X)*np.eye(n), X.T @ (Y - mt))
        # PESÉE PAR LANGUE. La régression minimise une erreur ABSOLUE : une langue
        # dont les cibles ont une norme double pèse quatre fois plus dans
        # l'objectif. Or la métrique finale est un COSINUS, insensible à l'échelle
        # — les deux sont incohérents, et la lecture partagée se met au service
        # des langues « fortes ». On rétablit la cohérence en pondérant chaque pas
        # par 1/norme², ce qui revient à minimiser l'erreur RELATIVE de chaque
        # langue. Les poids sont normalisés à 1 en moyenne pour que le terme de
        # ride garde la même échelle.
        w = np.concatenate([np.full(len(self.Y[i]), self.pese[i], dtype=np.float64)
                            for i in quel])
        w = w/w.mean()
        Xw = X*w[:, None]
        return np.linalg.solve(X.T @ Xw + ride*len(X)*np.eye(n), Xw.T @ (Y - mt))

    def fid(self, idx, W, mt, quel):
        X = self.phi(np.vstack([self._norm(self.X[i][:, idx]) for i in quel]))
        Y = np.vstack([self.Y[i] for i in quel])
        return cos_lignes(X @ W + mt, Y)

    def dernier(self, idx, W, mt, quel):
        return np.array([(self.phi(self._norm(self.X[i][:, idx])) @ W + mt)[-1] for i in quel])

    # -- critères d'attrition ------------------------------------------------
    def _W_neurones(self, W, K):
        """La part de la lecture qui correspond aux NEURONES.

        En lecture quadratique `W` a 2K lignes (`[états, états²]`) : les K
        premières sont celles des neurones, les autres celles de leurs carrés.
        Les critères d'attrition portent sur les neurones, donc sur les K
        premières."""
        return W[:K] if self.quadratique else W

    def contribution(self, W, idx):
        """Énergie que chaque neurone apporte à la sortie : ||w_k|| · ||x_k||."""
        X = np.vstack([x[:, idx] for x in self.X]).astype(np.float64)
        nx = np.sqrt((X**2).sum(0)) / np.sqrt(len(X))
        return nx * np.linalg.norm(self._W_neurones(W, len(idx)), axis=1)

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

    # -- ÉMERGENCE DE CONCEPTS COMMUNS ---------------------------------------
    def communs(self, idx, quel, L=64):
        """Version FAIBLE — corrèle des trajectoires rééchantillonnées.

        Elle compare des positions de contenu DIFFÉRENTES : le japonais emploie
        bien moins de jetons que l'abkhaze pour le même texte. Une valeur basse
        ne prouve donc PAS l'absence de concept commun. Gardée pour mémoire ;
        c'est `communs_fin` qui décide.
        """
        courbes = []
        for i in quel:
            X = self.X[i][:, idx]
            T = len(X)
            if T < 2:
                continue
            ti = np.linspace(0.0, 1.0, T)
            t = np.linspace(0.0, 1.0, L)
            courbes.append(np.stack([np.interp(t, ti, X[:, j])
                                     for j in range(X.shape[1])], axis=1))
        K = len(idx)
        if len(courbes) < 2:
            return np.zeros(K)
        acc = np.zeros(K); n = 0
        for a in range(len(courbes)):
            for b in range(a+1, len(courbes)):
                A = courbes[a] - courbes[a].mean(0)
                B = courbes[b] - courbes[b].mean(0)
                na = np.linalg.norm(A, axis=0); nb = np.linalg.norm(B, axis=0)
                ok = (na > 0) & (nb > 0)
                if not ok.any():
                    continue
                r = np.zeros(K)
                r[ok] = (A[:, ok]*B[:, ok]).sum(0)/(na[ok]*nb[ok])
                acc += r; n += 1
        return acc/max(n, 1)

    def communs_fin(self, idx, quel):
        """Un neurone est-il un CONCEPT COMMUN ? Mesure ALIGNÉE sur le contenu.

        Toutes les langues disent le MÊME texte : leur dernière position porte
        donc le même contenu. Pour chaque neurone on compare deux dispersions :

          - `dyn` : de combien il VARIE au fil du texte, dans une langue ;
          - `dis` : de combien il DIFFÈRE entre langues, à contenu égal.

        Un concept commun varie beaucoup sur le texte et peu entre les langues :
        il encode le contenu. Un trait de langue fait l'inverse. On rend
        `1 − dis/dyn`.
        """
        K = len(idx)
        dyn = np.zeros(K); fin = []
        for i in quel:
            X = self.X[i][:, idx]
            if len(X) < 2:
                continue
            dyn += X.std(0)
            fin.append(X[-1])
        if not fin:
            return np.zeros(K)
        dyn /= len(fin)
        if len(fin) < 2:
            return np.zeros(K)
        dis = np.std(np.array(fin), axis=0)
        return 1.0 - dis/np.maximum(dyn, 1e-12)

    def contraste(self, W):
        """Le readout se sert-il de DIFFÉRENCES entre neurones ?

        On sépare le mode commun (`mean_j W[j]`) des écarts. Si le mode commun
        porte tout, la lecture ne distingue rien — elle additionne. Si les écarts
        portent tout, la lecture ne fait que SOUSTRAIRE des concepts : c'est le
        signe qu'il faut une couche pour composer ce que la précédente ne sait
        plus séparer (le « OU exclusif » après le « ET » et le « OU »).
        """
        nm = float(np.linalg.norm(W.mean(0)))
        nd = float(np.linalg.norm(W - W.mean(0)))
        return nd/max(nm + nd, 1e-12)

    # -- RELECTURE DU CORPUS : RENFORCEMENT / ATROPHIE -----------------------
    def _recalcule_un(self, j, Ek=None):
        """Refait la trajectoire d'UN neurone à partir de ses seuls parents, qui
        sont gelés. Sert après un réajustement de ses poids."""
        w_par, w_self, b, c = self.poids[j]
        n_par = len(w_par)
        debut_par = self.debut_couche(c-1) if c > 0 else 0
        debut_c = self.debut_couche(c)
        r = j - debut_c
        for i, E in enumerate(self.E if Ek is None else Ek):
            T = len(E)
            Xpar = (self.X[i][:, debut_par:debut_par+n_par] if n_par > 0
                    else np.zeros((T, 0), dtype=np.float32))
            cam = self.X[i][:, debut_c:j]        # camarades de couche, antérieurs
            v = np.zeros(T, dtype=np.float32)
            sv = 0.0
            for t in range(T):
                drive = (float(Xpar[t] @ w_par)) if n_par > 0 else 0.0
                if r > 0:
                    drive += float(cam[t] @ w_self[:r])
                drive += float(w_self[r]*sv)
                sv = (1-self.a)*sv + self.a*np.tanh(drive + float(b @ E[t]))
                v[t] = sv
            self.X[i][:, j] = v

    def renforce(self, j, itr, mt, ride, eta=0.6):
        """RENFORCEMENT / ATROPHIE — la relecture du corpus qui suit la naissance
        d'une couche. **Aucune rétropropagation.**

        On relit le corpus pour mesurer ce qui reste à expliquer (le résidu), puis
        on renforce les entrées dont l'activation le capte et on atrophie les
        autres. C'est local : chaque neurone ne regarde que sa propre activation
        et le résidu, jamais le gradient d'une couche lointaine.
        """
        if j == 0 or len(itr) == 0:
            return 0.0
        idx = np.arange(j)
        W = self.ajuste(idx, ride, mt, itr)
        X = np.vstack([self.X[i][:, idx] for i in itr])
        Y = np.vstack([self.Y[i] for i in itr])
        R = Y - (self.phi(X) @ W + mt)        # ce qui reste à expliquer
        xj = np.concatenate([self.X[i][:, j] for i in itr]).astype(np.float64)
        if xj.std() == 0.0:
            return 0.0
        a_ = xj - xj.mean()
        b_ = R - R.mean(0)
        na = float(np.linalg.norm(a_))
        nb = np.linalg.norm(b_, axis=0)
        ok = (nb > 0) & np.isfinite(nb)
        if na == 0.0 or not ok.any():
            return 0.0
        # à quel point l'activation du nouveau-né capte le résidu, dans [0, 1]
        cap = float(np.abs(a_ @ b_[:, ok]).max()/(na*nb[ok].max()))
        f = 1.0 + eta*(2.0*cap - 1.0)          # cap>0,5 renforce · cap<0,5 atrophie
        w_par, w_self, bb, c = self.poids[j]
        self.poids[j] = (w_par*f, w_self*f, bb*f, c)
        self._recalcule_un(j)                  # la trajectoire suit les poids
        return cap

    def evalue(self, X, Y, W, mt):
        return cos_lignes(self.phi(np.vstack([self._norm(x) for x in X])) @ W + mt,
                          np.vstack(Y))

    def invariance(self, X, W, mt):
        return inv(np.array([(self.phi(self._norm(x)) @ W + mt)[-1] for x in X]))


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
    # `--val-liste F` : la validation est désignée par NOMS de langues, pas par
    # position. Un découpage positionnel ne tient pas dès qu'on change de corpus,
    # et il interdit un panel stratifié par écriture.
    if "--val-liste" in sys.argv:
        noms = {l.strip() for l in open(sys.argv[sys.argv.index("--val-liste")+1])
                if l.strip()}
        ival = [i for i, c in enumerate(cltr) if c in noms]
        itr = [i for i, c in enumerate(cltr) if c not in noms]
        assert ival and itr, "découpe vide — noms de langues inconnus du cache ?"
        print(f"# découpe par noms : {len(itr)} apprentissage · {len(ival)} validation")

    # ------------------------------------------------- SOUS-ENSEMBLE ACTIF
    #
    # La couche du professeur est CREUSE : 34 canaux sur 896 portent la moitié de
    # l'énergie, et 218 canaux sont propres à certaines langues. Ajuster les 896
    # dimensions densément, c'est payer pour du détail quasi nul et NON PARTAGÉ —
    # donc acheter de la fidélité avec l'invariance qu'on cherche.
    #
    # On restreint donc la cible aux canaux qui portent l'énergie. Le masque est
    # calculé sur l'APPRENTISSAGE SEUL : le lire sur le test serait une fuite.
    part_canaux = float(opt("--part-canaux", 0.0))
    if part_canaux > 0.0:
        E_ref = np.vstack([Ytr[i]**2 for i in itr]).sum(0)
        ordre = np.argsort(-E_ref)
        cum = np.cumsum(E_ref[ordre])/E_ref.sum()
        nk = int(np.searchsorted(cum, part_canaux) + 1)
        garde = np.sort(ordre[:nk])
        Ytr = [y[:, garde] for y in Ytr]
        Yte = [y[:, garde] for y in Yte]
        print(f"# SOUS-ENSEMBLE ACTIF : {nk}/{H} canaux portent {part_canaux:.0%} de "
              f"l'énergie ({nk/H:.0%} des canaux), masque lu sur l'apprentissage seul")

    # ------------------------------------------------ CANAUX PARTAGÉS
    #
    # Critère PRINCIPE, là où « 50 % de l'énergie » était un seuil arbitraire : on
    # ne garde que les canaux VIVANTS DANS LA PLUPART DES LANGUES. La mesure du
    # §2.2 dit que 218 canaux sur 896 (24 %) ne sont actifs que dans certaines
    # langues : ce sont eux qui coûtent l'invariance, et ce sont eux qu'on écarte.
    # Le masque est lu sur l'APPRENTISSAGE SEUL.
    # ------------------------------------------- CANAUX À CONSISTANCE INTER-LANGUE
    #
    # Le critère PRINCIPE, celui de la mission. Un canal est « à dominance
    # non-linguistique » si sa VALEUR est la même d'une langue à l'autre, à
    # contenu égal : toutes les langues disent le même texte, donc leur dernière
    # position porte le même contenu. On compare donc, canal par canal :
    #   `dis` — la dispersion ENTRE langues, à contenu égal ;
    #   `dyn` — la dispersion AU FIL DU TEXTE, dans une langue.
    # Consistance = `1 − dis/dyn`. Élevée : le canal dit le contenu. Basse : il dit
    # la langue. Masque lu sur l'APPRENTISSAGE SEUL.
    part_consist = float(opt("--part-consist", 0.0))
    if part_consist > 0.0:
        dyn = None; fin = []
        for i in itr:
            y = Ytr[i]
            dyn = y.std(0) if dyn is None else dyn + y.std(0)
            fin.append(y[-1])
        dyn /= len(itr)
        dis = np.std(np.array(fin), axis=0)
        consist = 1.0 - dis/np.maximum(dyn, 1e-12)
        nk = max(1, int(part_consist*H))
        garde = np.sort(np.argsort(-consist)[:nk])
        Ytr = [y[:, garde] for y in Ytr]
        Yte = [y[:, garde] for y in Yte]
        print(f"# CANAUX À CONSISTANCE : {nk}/{H} canaux les plus interlingues "
              f"({nk/H:.0%}), sur l'apprentissage seul · consistance retenue "
              f"{consist[garde].min():+.3f} à {consist[garde].max():+.3f} "
              f"(écartés : {consist.min():+.3f} à "
              f"{np.sort(consist)[::-1][nk] if nk < H else float('nan'):+.3f})")

    part_langues = float(opt("--part-langues", 0.0))
    if part_langues > 0.0:
        # « Vivant » = PRÉSENT, pas « d'amplitude suffisante » : la trace est
        # creuse, et un canal non écrit est un canal éteint. Un seuil de magnitude
        # gardait les 896 canaux (mesuré) — il ne mesurait rien.
        vivant = np.zeros(Ytr[0].shape[1])
        for i in itr:
            vivant += ((Ytr[i] != 0).mean(0) >= 0.05).astype(float)
        vivant /= len(itr)
        garde = np.where(vivant >= part_langues)[0]
        Ytr = [y[:, garde] for y in Ytr]
        Yte = [y[:, garde] for y in Yte]
        print(f"# CANAUX PARTAGÉS : {len(garde)}/{H} canaux présents dans au moins "
              f"{part_langues:.0%} des langues d'apprentissage "
              f"({len(garde)/H:.0%} des canaux)")

    print(f"# {len(cltr)} langues d'entraînement = {len(itr)} apprentissage + {len(ival)} validation")
    print(f"# {len(clte)} langues de TEST · a={a} · ride={ride} · graine={graine} · critère={critere}")
    print(f"# {cycles} cycles de {par_cycle} couches, puis attrition")
    print(f"# pas — apprentissage {sum(len(Etr[i]) for i in itr)} · validation "
          f"{sum(len(Etr[i]) for i in ival)} · test {sum(len(Ete[i]) for i in ite)}")

    # CENTRAGE DE L'ENTRÉE (`--centre-entree`) : on retire à chaque langue son
    # « jeton moyen ». Ce décalage est massivement propre à la langue (écriture,
    # morphologie) et ne dit aucun contenu — c'est le premier suspect de l'écart
    # de transfert. Calculable à l'inférence sur l'entrée elle-même, sans aucune
    # étiquette. À ne pas confondre avec la normalisation des ÉTATS, qui a échoué
    # (elle effaçait le décalage COMMUN, qui est la part partagée).
    if opt("--centre-entree", ""):
        Etr = [e - e.mean(0, keepdims=True) for e in Etr]
        Ete = [e - e.mean(0, keepdims=True) for e in Ete]
        print("# CENTRAGE DE L'ENTRÉE : le jeton moyen de chaque langue est retiré")

    # SEUIL PAR NEURONE (`--biais`) : on ajoute une colonne d'entrée CONSTANTE.
    # Chaque neurone tire alors un poids pour elle, donc un seuil propre — ce qui
    # déplace sa non-linéarité. Le passer par la colonne d'entrée évite de toucher
    # à la généalogie : c'est un canal de plus, rien d'autre.
    if opt("--biais", ""):
        col = float(np.sqrt(H))
        Etr = [np.hstack([e, np.full((len(e), 1), col, dtype=np.float32)]) for e in Etr]
        Ete = [np.hstack([e, np.full((len(e), 1), col, dtype=np.float32)]) for e in Ete]
        H = H + 1
        print(f"# SEUIL PAR NEURONE : colonne d'entrée constante de valeur {col:.1f}")

    P = Pont((cltr, Etr, Ytr), a, graine, H)
    P.gain_entree = float(opt("--gain-entree", 1.0))
    if opt("--normalise", ""):
        P.normalise = True
        print("# NORMALISATION PAR LANGUE des états (calculable à l'inférence, "
              "sans aucune étiquette)")
    if P.gain_entree != 1.0:
        print(f"# GAIN D'ENTRÉE : {P.gain_entree}")
    if opt("--lecture", "") == "quadratique":
        P.quadratique = True
        print("# LECTURE QUADRATIQUE : le readout voit [états, états²]")
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
        # `--naissance libre` : UN neurone à la fois. Aucun chiffre rond ne doit
        # sortir d'ici — 1, 2, 4, 8, … 256 étaient MON calendrier et MON plafond,
        # pas une découverte. Un compte rond est le signe qu'on a choisi la taille
        # au lieu de la mesurer.
        #
        # UNE COUCHE NE S'OUVRE PAS À LA SATURATION DE LA PRÉCÉDENTE. Elle
        # s'ouvre sur DEUX signes, et les deux se mesurent :
        #
        #   `communs`   — des CONCEPTS COMMUNS ont émergé : des neurones dont la
        #                 trajectoire suit le même contenu d'une langue à l'autre,
        #                 au lieu d'un trait de langue. Sans structure partagée à
        #                 composer, une couche de plus n'a rien à composer.
        #   `contraste` — la lecture a besoin de POIDS NÉGATIFS : elle soustrait
        #                 les concepts plus qu'elle ne les additionne. C'est le
        #                 « OU exclusif » : ce que le « ET » et le « OU » d'une
        #                 seule couche ne savent pas séparer.
        #
        # Une couche trop tôt est mesurablement mauvaise : la première règle en
        # ouvrait 24 pour 128 neurones (0,4937) contre 8 pour la même taille
        # (0,5059) — elle voulait le XOR avant d'avoir fini le ET et le OU.
        #
        # Ajouter la couche déclenche une RELECTURE du corpus : on réajuste par
        # renforcement/atrophie (voir `renforce`), jamais par rétropropagation.
        if opt("--naissance", "") == "libre":
            gain_min = float(opt("--gain-min", 0.0002))
            patience = int(opt("--patience", 12))
            seuil_commun = float(opt("--seuil-commun", 0.35))
            # part de neurones « concepts communs » exigée pour ouvrir une couche
            seuil_part = float(opt("--seuil-part", 0.5))
            seuil_contraste = float(opt("--seuil-contraste", 0.45))
            val_max = -1.0
            sans_gain = 0
            couche_neuve = True          # la toute première couche doit naître
            while P.compte_neurones < plafond:
                P.nait(1, nouvelle_couche=couche_neuve)
                if couche_neuve:
                    # AJOUTER UNE COUCHE = RELIRE LE CORPUS et réajuster par
                    # renforcement/atrophie, sans rétropropagation.
                    P.renforce(P.compte_neurones-1, itr, mt, ride)
                couche_neuve = False
                idx = np.arange(P.compte_neurones)
                W = P.ajuste(idx, ride, mt, itr)
                f_tr = P.fid(idx, W, mt, itr); f_va = P.fid(idx, W, mt, ival)
                gain = f_va - val_max if val_max > 0 else 0.0
                if f_va > val_max:
                    val_max = f_va
                if gain < gain_min:
                    sans_gain += 1
                else:
                    sans_gain = 0
                if P.compte_neurones % 8 == 0 or sans_gain >= patience:
                    com = P.communs_fin(idx, ival)
                    con = P.contraste(W)
                    part_commune = float((com > seuil_commun).mean())
                    Xte_g = P.recalcule(idx, Ete)
                    f_te = P.evalue(Xte_g, Yte, W, mt)
                    mg, mig = P.invariance(Xte_g, W, mt)
                    print(f"{'n' + str(P.compte_neurones):<12} {P.compte_neurones:>6} "
                          f"{len(P.couches):>7} {f_tr:>9.4f} {f_va:>8.4f} {f_te:>9.4f} "
                          f"{mg:>8.4f} {mig:>7.4f} | communs {com.mean():+.3f} "
                          f"({part_commune*100:>3.0f} %) · contraste {con:.3f}")
                    if f_va > meilleur["f_va"]:
                        meilleur = {"f_te": f_te, "neur": P.compte_neurones,
                                    "couch": len(P.couches), "f_tr": f_tr, "f_va": f_va,
                                    "inv": mg, "pire": mig, "etape": "naissance libre"}
                    # LES TROIS CONDITIONS, et elles doivent tenir ENSEMBLE :
                    #
                    #  1. la couche courante est ÉPUISÉE — les derniers neurones
                    #     n'apportent plus rien. Tant qu'un neurone de plus paie,
                    #     c'est LUI qu'il faut, pas une couche : un neurone sait
                    #     faire « ET » et « OU », et couvrir une activation
                    #     manquante est un travail de neurone, pas de couche.
                    #  2. des CONCEPTS COMMUNS existent — il y a de la structure
                    #     partagée à composer. Sans elle, une couche de plus n'a
                    #     rien à composer.
                    #  3. la lecture doit SOUSTRAIRE — les écarts portent
                    #     l'essentiel du readout. C'est le « OU exclusif », ce
                    #     qu'une seule couche ne sait pas séparer.
                    #
                    # Sans la condition 1, le critère déclenchait à CHAQUE pas :
                    # 9 couches pour 72 neurones, mesuré.
                    epuisee = sans_gain >= patience
                    # `part_commune` est déjà le pourcentage de neurones AU-DESSUS
                    # de `seuil_commun`. Comparer ici à une constante en dur (0,5)
                    # rendait `--seuil-commun` inopérant sur la DÉCISION : le
                    # drapeau ne changeait que l'affichage, jamais le déclenchement.
                    if epuisee and part_commune > seuil_part and con > seuil_contraste:
                        print(f"{'  → COUCHE NEUVE (épuisée + concepts + contraste)':<12} "
                              f"{P.compte_neurones:>6} {len(P.couches):>7}")
                        couche_neuve = True
                        sans_gain = 0
                if sans_gain >= 2*patience:
                    print(f"{'  → ARRÊT (couche neuve sans gain)':<12} "
                          f"{P.compte_neurones:>6} {len(P.couches):>7}")
                    break
            print(f"# née : {P.compte_neurones} neurones en {len(P.couches)} couches "
                  f"{P.couches}")
        else:
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
        # L'ATTRITION DOIT RENDRE LE MEILLEUR RÉSEAU, PAS LE DERNIER. Sans cela,
        # un seuil de validation plus grand que la perte totale fait descendre
        # jusqu'à un neurone : mesuré, 34 neurones (VAL 0,8353) jusqu'à 1
        # (0,8220) alors que le meilleur point était le réseau né. On garde donc
        # le meilleur passage, et on y revient à la fin.
        meilleur_passage = {"f": f_va, "poids": list(P.poids),
                            "X": [x.copy() for x in P.X],
                            "couches": list(P.couches), "n": P.compte_neurones}
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
            if f_va > meilleur_val:
                meilleur_val = f_va
                meilleur_passage = {"f": f_va, "poids": list(P.poids),
                                    "X": [x.copy() for x in P.X],
                                    "couches": list(P.couches), "n": P.compte_neurones}
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

        # ON REVIENT AU MEILLEUR PASSAGE : c'est lui le résultat de l'attrition.
        # Sans cela le réseau finit à un neurone, ce qui est mesurablement pire.
        mp = meilleur_passage
        if mp["n"] != P.compte_neurones:
            P.poids = mp["poids"]; P.X = mp["X"]
            P.couches = mp["couches"]; P.compte_neurones = mp["n"]
            print(f"{'  → retour au MEILLEUR passage':<30} {mp['n']:>6} "
                  f"{len(mp['couches']):>7} {'—':>9} {mp['f']:>8.4f}")

    # ---------------------------------------------------------------- ORACLE
    #
    # Où est le plafond : dans les CARACTÉRISTIQUES ou dans le TRANSFERT ?
    # On ajuste la lecture sur le TEST lui-même et on l'y évalue. Ce n'est PAS un
    # modèle — c'est un diagnostic. S'il plafonne comme nous, nos caractéristiques
    # ne contiennent pas plus ; s'il monte haut, c'est le transfert qui pèche.
    if opt("--oracle", ""):
        # ATTENTION : `Pont` ne détient QUE les langues d'entraînement. Évaluer
        # avec `P.fid(..., ite)` indexerait donc des langues d'ENTRAÎNEMENT — la
        # fuite déjà corrigée une fois. Les trajectoires du test se calculent
        # avec `recalcule(..., Ete)`.
        idx_o = np.arange(P.compte_neurones)
        Wtr = P.ajuste(idx_o, ride, mt, itr)

        def oracle_sur(Ek, Yk):
            Xk = P.recalcule(idx_o, Ek)
            A = P.phi(np.vstack(Xk)); B = np.vstack(Yk)
            Wo = np.linalg.solve(A.T @ A + ride*len(A)*np.eye(A.shape[1]),
                                 A.T @ (B - mt))
            return P.evalue(Xk, Yk, Wtr, mt), cos_lignes(A @ Wo + mt, B), Xk, Wo

        print(f"\n# ORACLE (lecture ajustée SUR le jeu évalué — diagnostic seulement)")
        nous_t, or_t, Xt, Wt = oracle_sur(Ete, Yte)
        mo, mio = P.invariance(Xt, Wt, mt)
        print(f"#   TEST        : nous {nous_t:.4f} · oracle {or_t:.4f} · "
              f"ÉCART {or_t-nous_t:+.4f} · invariance oracle {mo:.4f}")
        Ev = [Etr[i] for i in ival]; Yv = [Ytr[i] for i in ival]
        nous_v, or_v, _, _ = oracle_sur(Ev, Yv)
        print(f"#   VALIDATION  : nous {nous_v:.4f} · oracle {or_v:.4f} · "
              f"ÉCART {or_v-nous_v:+.4f}   (même vivier que l'apprentissage)")

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
