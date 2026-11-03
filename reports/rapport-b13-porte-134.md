# B13 — la porte est à 134/140 : le 140/140 de 702b368c ne se rejoue pas ; quatre rouges viennent du sous-module S

> **Ligne de roadmap** : **B13** (le moteur de pensée) · **Date** : 2026-11-02 ·
> **Verdict** : ❌ **la porte est à 134/140** — **4 rouges** viennent du sous-module S `647205a`
> (T111, T113–T115 ; l'ancien `3b68143` les passe, **138/140**) et **2** (T132/T133) d'un
> **test périmé** : `fidelite_lien_auto` rend **2/5** sur l'arbre exact du commit `702b368c`
> — qui annonçait **140/140** — avec **les deux sous-modules** et sur **6 graines de hash**.
> **Le 140/140 ne se rejoue pas ; le compte était périmé.**
>
> **Dispositif** : worktrees `702b368c` + `3b68143`, HEAD + `3b68143`, HEAD + `647205a` ;
> [`miroir.py`](../tools/tests/linguistique/miroir.py) (`fidelite_lien_auto`) ; JSON
> [`b13-porte-134.json`](b13-porte-134.json).

## 1. Ce qui était dit

Le commit `702b368c` (15 h 57) annonçait **140/140 portes** ; l'état et la roadmap ont repris
ce chiffre. Depuis, la porte rend **134/140** et six tests échouent : T111, T113, T114, T115
(segmentation/hybride) et T132, T133 (lien anaphorique). L'hypothèse initiale — « six rouges
du sous-module S » — était **fausse** pour deux d'entre eux.

## 2. Le dispositif

- **Trois arbres** : le commit `702b368c` (celui du 140/140) avec son sous-module **exact**
  `3b68143` ; HEAD avec `3b68143` ; HEAD avec `647205a` (le sous-module S courant).
- **Le même code** pour les trois (ou le code de `702b368c` pour le premier) ; `miroir.py`,
  `gold_reel.json` et `evaluer_gold.py` ont **aucun diff** entre `702b368c` et HEAD.
- **Les deux mesures** : la porte complète (`tools/pensee/autotest.py`, 140 tests, 4,5 min) sur
  HEAD old/new ; le **test direct** `fidelite_lien_auto(charger())` sur les trois arbres et
  sous **6 graines** `PYTHONHASHSEED` (0–5).
- Les worktrees n'ont pas `data/` ; les tests B13 utilisent le gold **suivi** ; HEAD (avec
  `data/`) rend le même 2/5 — `data/` n'est pas la variable.

## 3. Les résultats

| arbre | sous-module | anaphora T132/T133 | 4 tests S | porte |
|---|---|---|---:|---:|
| `702b368c` | `3b68143` | **2/5** | passent | **138/140** (inféré) |
| HEAD | `3b68143` | **2/5** | passent | **138/140** |
| HEAD | `647205a` | **2/5** | **échouent** | **134/140** |

- **Le 140/140 ne se rejoue pas** : l'arbre exact de `702b368c` (son code, son sous-module
  `3b68143`, son gold) rend **2/5** sur `fidelite_lien_auto` ; la porte complète y serait
  **138/140**. Le compte de 15 h 57 était **périmé** (la porte a été comptée avant l'état final
  du gold, ou le compte est faux) ; il n'est pas reproductible.
- **Quatre rouges du sous-module S** : avec `3b68143`, les quatre passent (138/140) ; avec
  `647205a`, ils échouent (134/140) — c'est le seul changement.
- **Deux rouges du test anaphorique** : T132/T133 rendent **2/5** avec **les deux**
  sous-modules, sur **6 graines** (0–5) — ce n'est ni le S, ni le hash, ni `data/` ; c'est une
  **incohérence test/gold** : le test attend 5/5, la fonction rend 2/5, de façon déterministe.

**Les quatre valeurs du S** :

| test | attendu (`3b68143`) | mesuré (`647205a`) |
|---|---:|---:|
| T111 (tête hybride) | 0,3649 | **0,3676** |
| T113 (union défaut) | 0,1966 / 0,4568 | **0,1961 / 0,4592** |
| T114 (cascade union) | 0,2122 / 0,4314 / 602 | **0,2109 / 0,4336 / 602** |
| T115 (tête cascade) | 0,4098 | **0,4119** |

Les écarts sont petits (0,001–0,003) mais **déterministes** ; ce sont les valeurs exactes que
les tests comparent. Le S `647205a` change la segmentation ; les attendus de T111/T113–T115
sont ceux de `3b68143`.

## 4. Ce que ça dit

- **Le chiffre de la porte n'était pas fiable** : le 140/140 annoncé par `702b368c` ne se
  rejoue pas sur son propre arbre ; le vrai compte à ce commit est **138/140**. La leçon rejoint
  la règle des portes : un compte se lit à l'exécution, jamais dans un message.
- **Le sous-module S est en cause pour quatre tests** : son changement de segmentation déplace
  les F1 de T111/T113–T115, qui comparent des valeurs **exactes**. Ce n'est pas une
  « régression » du modèle, c'est un **désaccord d'attendus** : le S a changé, les tests n'ont
  pas suivi.
- **Le test anaphorique est en cause pour deux** : `fidelite_lien_auto` rend 2/5 alors que le
  test attend 5/5 ; c'est déterministe, avec les deux sous-modules. Le test ou la fonction/gold
  doit être corrigé ; le 140/140 le masquait.

## 5. Ce qui pourrait le rendre faux

- **Le worktree `702b368c` n'a pas `data/`** : les tests B13 utilisent le gold suivi, et HEAD
  avec `data/` rend le même 2/5 ; `data/` n'est pas la variable. Le worktree 702 a le
  sous-module **exact** (`git ls-tree 702b368c tools/structures` = `3b68143`).
- **La porte complète de 702 n'a pas été relancée** : l'anaphora directe (2/5) et la porte
  HEAD/`3b68143` (138/140) l'encadrent ; les autres 138 tests sont indépendants du code ajouté
  depuis (les tests du bloc/heuristique n'ont pas changé). Le 138/140 est **inféré** avec cette
  réserve.
- **Le 140/140 de `702b368c`** a pu être compté avant la dernière écriture du gold dans le
  commit ; le message le dit 140/140, l'arbre rend 2/5. C'est un **compte périmé**, pas une
  preuve que le test passait.
- **Une seule exécution par porte** : les quatre valeurs du S sont des assertions exactes,
  déterministes ; l'anaphora est déterministe sur 6 graines.
- **Le sous-module S `647205a`** est un fait de la session S (38/39 types, 99/100 rôles) ; les
  quatre attendus doivent être mis à jour **par S**, pas maquillés ici.
- **La porte B13 n'est pas tolérée** : `references-non-regression.md` ne liste pas ces rouges ;
  c'est une régression au sens de la règle 3.

## 6. La suite

1. **S** : mettre à jour les attendus T111/T113–T115 (les quatre valeurs ci-dessus) ou revenir à
   `3b68143` ; c'est son changement de segmentation.
2. **T132/T133** : réconcilier le test (5/5) avec `fidelite_lien_auto` (2/5) — corriger le test,
   le gold ou la fonction ; le 140/140 est périmé.
3. **Le hub** : corriger le compte de la porte dans l'état/la roadmap (134/140, pas 140/140) et
   décider de la tolérance.
4. **L/B13** : le gold 200+, la porte qui bouge, la cascade complète restent les faits suivants.

## 7. Fichiers

- Les logs : `/tmp/b13-old.log` (138/140), `/tmp/b13-new.log` (134/140), le test direct 702
  (2/5) — non versionnés.
- [`b13-porte-134.json`](b13-porte-134.json) — les trois arbres, les valeurs, les graines.
- [`tools/pensee/autotest.py`](../tools/pensee/autotest.py) — les tests T111/T113–T115/T132/T133.
- [`tools/tests/linguistique/miroir.py`](../tools/tests/linguistique/miroir.py) —
  `fidelite_lien_auto`.
- Sous-module : `3b68143` (ancien, 138/140) → `647205a` (courant, 134/140).
