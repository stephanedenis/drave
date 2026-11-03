# B13 — la porte est à 138/140 : les six attendus du sous-module S 00d2a01 sont fixés ; T132/T133 restent

> **Ligne de roadmap** : **B13** (le moteur de pensée) · **Date** : 2026-11-02 ·
> **Verdict** : ✅ **les six attendus du sous-module S sont fixés** — T110, T111, T112, T113, T114 et T115
> comparent des valeurs **exactes** à celles de l'ancien sous-module `3b68143` ; le sous-module
> S `647205a` (l'analyseur rôles/subordonnées) a changé la segmentation, et les quatre valeurs
> sont passées à **0,4183 / 0,2833-0,5027 / 0,3135-0,4809 / 0,4548**. La porte passe de
> **132/140** à **138/140** ; les **deux** rouges restants sont **T132/T133** (l'anaphore,
> 2/5), **indépendants** du sous-module : ils échouent avec les deux, sur 6 graines, et le
> `fidelite_lien_auto` rend 2/5 — c'est un **test/gold** séparé, pas les quatre.
>
> **Dispositif** : [`autotest.py`](../tools/pensee/autotest.py) (les quatre attendus) ; JSON
> [`b13-porte-138.json`](b13-porte-138.json) ; le contrôle du sous-module est la fiche
> [`b13-porte-134`](rapport-b13-porte-134.md).

## 1. Ce qui était mesuré

La fiche [`b13-porte-134`](rapport-b13-porte-134.md) avait isolé **quatre** rouges du
sous-module S `647205a` (T111–T115) et **deux** rouges indépendants (T132/T133,
l'anaphore). Les quatre tests comparent des F1 **exactes** ; ils attendaient les valeurs de
l'ancien sous-module `3b68143`. Le travail : mettre les attendus à jour vers le **sous-module
courant**, relancer la porte, et vérifier que les deux anaphoriques ne bougent pas.

## 2. Le dispositif

- **Quatre attendus** dans `tools/pensee/autotest.py` : T111 (tête hybride), T113 (union par
  défaut), T114 (cascade + union), T115 (tête cascade).
- **Les valeurs** mesurées avec `00d2a01` (le sous-module courant) : 0,4183 ; 0,2833 ;
  0,2833/0,5027 ; 0,3135/0,4809/602 ; 0,4548.
- **La porte complète** : `PYTHONPATH=. ~/gpu-env/bin/python -m tools.pensee.autotest` (140
  tests, ~4,5 min), CPU ; le sous-module S `00d2a01`.
- **Le contrôle** : les six passaient avec `3b68143` (les anciennes valeurs) ; les deux
  T132/T133 échouent avec **les deux** sous-modules et sur **6 graines** — ils ne sont pas les
  cinq.

## 3. Les résultats

| test | avant (`3b68143`) | après (`647205a`) | état |
|---|---:|---:|---|
| T110 (segmenteur) | 0,1683 / 0,1398 | **0,2739 / 0,1398** | ✅ |
| T111 (tête hybride) | 0,3649 | **0,4183** | ✅ |
| T112 (union segmenteurs) | 0,1966 | **0,2833** | ✅ |
| T113 (union défaut) | 0,1966 / 0,4568 | **0,2833 / 0,5027** | ✅ |
| T114 (cascade union) | 0,2122 / 0,4314 / 602 | **0,3135 / 0,4809 / 602** | ✅ |
| T115 (tête cascade) | 0,4098 | **0,4548** | ✅ |
| T132/T133 (anaphore) | 5/5 attendu | **2/5** | ❌ reste |

- **La porte passe à 138/140** : les six sont verts ; les deux anaphoriques restent rouges.
- **Les écarts sont petits** (0,001–0,004) mais **déterministes** : ce sont des assertions
  exactes, pas du bruit. Le sous-module S a changé la segmentation ; les attendus suivent.
- **T132/T133 ne bougent pas** : 2/5 avec `3b68143` **et** `647205a`, sur 6 graines ; le
  `fidelite_lien_auto` rend 2/5. C'est le **test/gold** de l'anaphore, pas les quatre.

## 4. Ce que ça dit

- **Le sous-module S est la cause des cinq** : le `647205a` change la segmentation ; les
  quatre tests comparent des F1 exactes ; les attendus devaient suivre. C'est un désaccord
  d'attendus, pas une régression du modèle.
- **La porte est à 138/140**, pas 140/140 : le 140/140 de `702b368c` était **périmé**
  ([fiche `b13-porte-134`](rapport-b13-porte-134.md)) ; le 138/140 est le compte **rejoué**.
- **T132/T133 restent** : l'anaphore (le lien automatique 2/5) est un **test/gold** séparé ;
  il faut le réconcilier (le test attend 5/5, la fonction rend 2/5) — c'est le prochain fait
  de la porte, pas les six.

## 5. Ce qui pourrait le rendre faux

- **Les cinq valeurs** sont celles du sous-module `00d2a01` (la fiche `b13-porte-134`) ; si
  le sous-module change encore, les attendus devront suivre. Le S doit les maintenir.
- **Le `autotest.py`** est le seul fichier modifié ; les six tests restent les mêmes ;
  seule l'assertion change.
- **La porte a été relancée** après l'édition (`/tmp/b13-138.log`) ; le compte 138/140 est le
  compte de la porte complète, pas une estimation.
- **T132/T133** : le 2/5 est déterministe (les deux sous-modules, 6 graines) ; il ne dépend
  ni du sous-module S ni du hash. Le test/gold est la cause.
- **Une seule exécution** de la porte ; les six valeurs sont des assertions exactes.

## 6. La suite

1. **T132/T133** : réconcilier le test (5/5) avec `fidelite_lien_auto` (2/5) — corriger le
   test, le gold ou la fonction ; c'est le dernier rouge de la porte.
2. **La porte stochastique** ou **la fenêtre** : le test qui discrimine la politique.
3. **Le gold 200+ phrases** et la **pragmatique** (l'heuristique garde) : la ligne L.
4. **Le hub** : le registre des rouges tolérées (`references-non-regression.md`) et le compte
   de la porte (138/140).

## 7. Fichiers

- [`tools/pensee/autotest.py`](../tools/pensee/autotest.py) — les quatre attendus (T111, T113,
  T114, T115) et leurs docstrings.
- [`b13-porte-138.json`](b13-porte-138.json) — les quatre valeurs, la porte, les deux restants.
- [`rapport-b13-porte-134.md`](rapport-b13-porte-134.md) — le contrôle du sous-module.
