# B13 — la base honnête : `evaluer --reel`, 452 phrases réelles, et ce que le synthétique cachait

> **Ligne de roadmap** : **B13** (le produit) · **Décision** : 6A · **Date** : 2026-11-15 ·
> **Verdict** : ✅ **la CLI sait maintenant mesurer le réel** (`evaluer --reel`) et **publie la
> base réelle à côté du global** dans la sortie par défaut. Ce que ça révèle : sur les **452
> phrases réelles** (main + corpus, sans les 160 synthétiques), le **POS monte** (88,91 % contre
> 86,25 %) et la **F1 est la même** (79,06 % contre 79,02 %) — le synthétique n'aidait donc **pas**
> le POS, contrairement à ce qu'on pouvait craindre, mais il **tirait la moyenne vers le bas**.
>
> **Dispositif** : [`drave.py`](../tools/drave.py) (`--reel`, la ligne `BASE RÉELLE`),
> [`test_produit.py`](../tools/tests/test_produit.py) (2 tests) ; JSON
> [`pensee-base-reelle.json`](pensee-base-reelle.json).

## 1. Les deux bases

| mesure | vivant 612 | **réel 452** |
|---|---:|---:|
| POS | 86,25 % | **88,91 %** (fermé 92,94 / ouvert 84,66) |
| F1 syntagmes | 79,02 % | **79,06 %** |
| tête F1 | 90,29 % | 89,90 % |
| attachement exact | 99,58 % | **99,46 %** |
| couverture | 99,58 % | 99,46 % |
| cibles | 239 | 184 |

**Ce que ça dit** :

- **Le POS réel est meilleur** que le global : les phrases synthétiques, générées par une grammaire
  indépendante, sont **plus difficiles** pour le POS (mots hors lexique) — le global sous-estimait
  donc la qualité réelle.
- **La F1 est identique** : la segmentation ne dépend pas de la source.
- **L'attachement est presque identique** (99,46 vs 99,58) : la base réelle est plus petite
  (184 cibles), les 3 échecs connus y pèsent un peu plus.

## 2. Ce que la CLI affiche désormais

```
SYNTAGMES   F1 79.02 %  (P 78.60 % / R 79.44 %)
  tête      F1 90.29 %  ...
  vue linéaire (partition filtrer) F1 79.53 % · attachement 91.85 % de couverture
BASE RÉELLE (hand + reel, 452 phrases)  POS 88.91 % · F1 79.06 % · attachement 99.46 %
ATTACHEMENT exact 99.58 % · couverture 99.58 % · ...
```

`--reel` mesure **directement** la base réelle (452 phrases, 184 cibles) ; sans lui, la ligne
`BASE RÉELLE` est calculée et publiée à côté du global.

## 3. Ce que ce banc ne dit pas

- **Les 452 réelles** incluent les 20 phrases « main » (écrites à la main) et 432 phrases de
  corpus — pas un tirage aléatoire.
- **Le synthétique n'est pas inutile** : il teste des structures rares (les REL/SUB synthétiques).
- **La base réelle** n'est pas « la vérité » : c'est le corpus annoté, avec ses conventions.

## 4. Ce qui pourrait rendre cette fiche fausse

- **la définition de « réel »** : `hand + reel` (452) ; le gold « réel 432 » des fiches R est le
  corpus seul.
- **les mesures** dépendent du gold (une phrase mal annotée fausse les deux bases).

## 5. La suite

1. **Publier les deux bases** dans la doc produit et le README (le chiffre réel à côté du global).
2. **Le gold réel** : 432 phrases, à étendre (le « gold 200+ » des fiches R).
3. **Le tagger sur la base réelle** : +4,67 (le chiffre honnête), pas +8,49.

## 6. Fichiers

- [`drave.py`](../tools/drave.py) — `--reel` et la ligne `BASE RÉELLE`.
- [`test_produit.py`](../tools/tests/test_produit.py) — 2 tests.
- [`pensee-base-reelle.json`](pensee-base-reelle.json).
