"""
Drave — modèle minimal entraînable en numpy pur (aucune dépendance ML).

But : disposer d'un modèle *réellement appris* (pas aléatoire) pour tester si la
quantification ternaire / multi-bits préserve sa fonction.

Tâche synthétique : un « professeur » (MLP aléatoire figé) étiquette des vecteurs
gaussiens en 10 classes ; l'« élève » (MLP 32→64→10) apprend à reproduire ces
étiquettes. On mesure ensuite la dégradation due à la quantification des poids.
"""

from __future__ import annotations

import numpy as np


# --------------------------------------------------------------------------- #
# Données
# --------------------------------------------------------------------------- #


def make_dataset(n: int, d_in: int = 32, n_class: int = 10, seed: int = 0,
                 teacher_seed: int = 1234):
    """Étiquettes produites par un professeur **non linéaire figé**.

    ⚠️ Le professeur dépend de `teacher_seed` (constant), PAS de `seed` : sans cela
    les jeux d'entraînement et de test auraient deux professeurs différents et
    l'accuracy resterait au niveau du hasard.
    """
    rng_t = np.random.default_rng(teacher_seed)
    Wt1 = rng_t.normal(0, 1 / np.sqrt(d_in), size=(d_in, 64)).astype(np.float32)
    Wt2 = rng_t.normal(0, 1 / np.sqrt(64), size=(64, n_class)).astype(np.float32)

    def teacher(X):
        return np.maximum(X @ Wt1, 0) @ Wt2       # non linéaire (ReLU)

    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, d_in)).astype(np.float32)
    y = teacher(X).argmax(axis=1)
    return X, y


def softmax(z: np.ndarray) -> np.ndarray:
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


# --------------------------------------------------------------------------- #
# Modèle : MLP 2 couches, entraînement SGD manuel
# --------------------------------------------------------------------------- #


class MLP:
    def __init__(self, d_in: int, d_hidden: int, n_class: int, seed: int = 1):
        rng = np.random.default_rng(seed)
        # initialisation type He
        self.W1 = (rng.normal(0, np.sqrt(2 / d_in), size=(d_in, d_hidden))).astype(np.float32)
        self.b1 = np.zeros(d_hidden, dtype=np.float32)
        self.W2 = (rng.normal(0, np.sqrt(2 / d_hidden), size=(d_hidden, n_class))).astype(np.float32)
        self.b2 = np.zeros(n_class, dtype=np.float32)

    # -- forward ----------------------------------------------------------- #
    def forward(self, X, W1=None, b1=None, W2=None, b2=None):
        W1 = self.W1 if W1 is None else W1
        b1 = self.b1 if b1 is None else b1
        W2 = self.W2 if W2 is None else W2
        b2 = self.b2 if b2 is None else b2
        z1 = X @ W1 + b1
        a1 = np.maximum(z1, 0)          # ReLU
        z2 = a1 @ W2 + b2
        return z1, a1, z2, softmax(z2)

    def predict(self, X, **kw):
        return self.forward(X, **kw)[3].argmax(axis=1)

    def accuracy(self, X, y, **kw):
        return float((self.predict(X, **kw) == y).mean())

    # -- entraînement ------------------------------------------------------ #
    def train(self, X, y, epochs: int = 300, lr: float = 0.05, batch: int = 128,
              seed: int = 0, verbose: bool = False, masks=None):
        """SGD. `masks` = (mask1, mask2) appliqués après chaque pas — c'est le
        réentraînement à masque fixe de la recette prune → retrain → quantize."""
        rng = np.random.default_rng(seed)
        n = X.shape[0]
        n_class = self.b2.size
        hist = []
        for ep in range(epochs):
            idx = rng.permutation(n)
            tot = 0.0
            for s in range(0, n, batch):
                b = idx[s:s + batch]
                xb, yb = X[b], y[b]
                m = xb.shape[0]
                z1, a1, z2, p = self.forward(xb)
                # gradient de la cross-entropy softmax
                dz2 = (p - np.eye(n_class, dtype=np.float32)[yb]) / m
                dW2 = a1.T @ dz2
                db2 = dz2.sum(axis=0)
                da1 = dz2 @ self.W2.T
                dz1 = da1 * (z1 > 0)
                dW1 = xb.T @ dz1
                db1 = dz1.sum(axis=0)
                for p_, g in ((self.W1, dW1), (self.b1, db1), (self.W2, dW2), (self.b2, db2)):
                    p_ -= lr * g.astype(np.float32)
                if masks is not None:                    # masque fixe (élagage)
                    self.W1 *= masks[0]
                    self.W2 *= masks[1]
                tot += float(-np.log(np.clip(p[np.arange(m), yb], 1e-12, None)).mean())
            if ep % 50 == 0 or ep == epochs - 1:
                hist.append((ep, tot / max(1, n // batch)))
                if verbose:
                    print(f"    epoch {ep:4d}  loss={hist[-1][1]:.4f}")
        return hist
