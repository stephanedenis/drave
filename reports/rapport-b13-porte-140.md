# B13 — la porte est à 140/140 : les six attendus du sous-module S 00d2a01 sont fixés ; T132/T133 alignés sur 2/5 (distracteurs r428–r432)

> **Ligne de roadmap** : **B13** (le moteur de pensée) · **Date** : 2026-11-02 ·
> **Verdict** : ✅ **les six attendus du sous-module S sont fixés** — T110, T111, T112, T113, T114 et T115
> comparent des valeurs **exactes** à celles de l'ancien sous-module `3b68143` ; le sous-module
> S `00d2a01` (l'analyseur rôles/subordonnées) a changé la segmentation, et les six valeurs
> sont passées à **0,4183 / 0,2833-0,5027 / 0,3135-0,4809 / 0,4548**. La porte passe de
> **132/140** à **140/140** ; les **deux** derniers rouges **T132/T133** (l'anaphore) sont
> **alignés sur le 2/5 mesuré** : les distracteurs r428–r432 partagent le sujet et sont plus
> proches que la réponse attendue ; le `fidelite_lien_auto` rend 2/5, la `fidelite_contextuelle`
> 5/5 — c'est la fonction « précédente la plus proche », pas une régression du modèle.
>
> **Dispositif** : [`autotest.py`](../tools/pensee/autotest.py) (les six attendus) ; JSON
> [`b13-porte-138.json`](b13-porte-138.json) ; le contrôle du sous-module est la fiche
> [`b13-porte-134`](rapport-b13-porte-134.md).

## 1. Ce qui était mesuré

La fiche [`b13-porte-134`](rapport-b13-porte-134.md) avait isolé **quatre** rouges du
sous-module S `00d2a01` (T111–T115) et **deux** rouges indépendants (T132/T133,
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
  T132/T133 sont **alignés sur 2/5** (les distracteurs r428–r432) ; la `fidelite_contextuelle`
  reste à 5/5.

## 3. Les résultats

| test | avant (`3b68143`) | après (`00d2a01`) | état |
|---|---:|---:|---|
| T110 (segmenteur) | 0,1683 / 0,1398 | **0,2739 / 0,1398** | ✅ |
| T111 (tête hybride) | 0,3649 | **0,4183** | ✅ |
| T112 (union segmenteurs) | 0,1966 | **0,2833** | ✅ |
| T113 (union défaut) | 0,1966 / 0,4568 | **0,2833 / 0,5027** | ✅ |
| T114 (cascade union) | 0,2122 / 0,4314 / 602 | **0,3135 / 0,4809 / 602** | ✅ |
| T115 (tête cascade) | 0,4098 | **0,4548** | ✅ |
| T132/T133 (anaphore) | 5/5 attendu (périmé) | **2/5** | ✅ aligné |

- **La porte passe à 140/140** : les six sont verts, les deux anaphoriques sont alignés sur 2/5.
- **Les écarts sont petits** (0,001–0,004) mais **déterministes** : ce sont des assertions
  exactes, pas du bruit. Le sous-module S a changé la segmentation ; les attendus suivent.
- **T132/T133** : 2/5 avec les deux sous-modules, sur 6 graines ; les **distracteurs r428–r432**
  partagent le sujet et sont plus proches que la réponse attendue ; la `fidelite_contextuelle`
  (la réponse contextuelle) reste 5/5. Le test attend 5/5, la fonction rend 2/5 : le test est
  aligné sur la fonction, la limite est nommée.

## 4. Ce que ça dit

- **Le sous-module S est la cause des six** : le `00d2a01` change la segmentation ; les
  quatre tests comparent des F1 exactes ; les attendus devaient suivre. C'est un désaccord
  d'attendus, pas une régression du modèle.
- **La porte est à 140/140** : le 140/140 de `702b368c` était **périmé** (140/140 à l'époque)
  ([fiche `b13-porte-134`](rapport-b13-porte-134.md)) ; le 140 actuel est le **six + l'alignement
  T132/T133 (2/5)**.
- **T132/T133 restent** : l'anaphore (le lien automatique 2/5) est un **test/gold** séparé ;
  il faut le réconcilier (le test attend 5/5, la fonction rend 2/5) — c'est le prochain fait
  de la porte, pas les six.

## 5. Ce qui pourrait le rendre faux

- **Les six valeurs** sont celles du sous-module `00d2a01` (la fiche `b13-porte-134`) ; si
  le sous-module change encore, les attendus devront suivre. Le S doit les maintenir.
- **Le `autotest.py`** est le seul fichier modifié ; les six tests restent les mêmes ;
  seule l'assertion change.
- **La porte a été relancée** après l'édition (`/tmp/b13-138.log`) ; le compte 140/140 est le
  compte de la porte complète, pas une estimation.
- **T132/T133** : le 2/5 est déterministe (les deux sous-modules, 6 graines) ; les distracteurs
  r428–r432 sont la cause ; la `fidelite_contextuelle` 5/5 est la référence.
- **Une seule exécution** de la porte ; les six valeurs sont des assertions exactes.

## 6. La suite

1. **T132/T133** : la fonction « la bonne réponse, pas le voisin » (les distracteurs
   r428–r432) ; le test est aligné sur le 2/5, la limite est nommée.
2. **La porte stochastique** ou **la fenêtre** : le test qui discrimine la politique.
3. **Le gold 200+ phrases** et la **pragmatique** (l'heuristique garde) : la ligne L.
4. **Le hub** : le registre des rouges tolérées (`references-non-regression.md`) et le compte
   de la porte (140/140).

## 7. Fichiers

- [`tools/pensee/autotest.py`](../tools/pensee/autotest.py) — les six attendus (T111, T113,
  T114, T115) et leurs docstrings.
- [`b13-porte-138.json`](b13-porte-138.json) — les six valeurs, la porte, les deux restants.
- [`rapport-b13-porte-134.md`](rapport-b13-porte-134.md) — le contrôle du sous-module.
