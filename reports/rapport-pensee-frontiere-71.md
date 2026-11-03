# L — la frontière sur les 71 langues : le script est tenu (71/71), la langue sur libellés courts ne l'est pas (0,137 contre 0,032)

> **Ligne de roadmap** : **L** (le bloc langue) · **Date** : 2026-11-03 · **Verdict** : ⚠️ **la frontière
> est nette** — sur le lexique multilingue des jeux (**71 langues, 35 concepts, 1487 labels**
> Wikidata), le niveau **graphème** est **tenu par le CPU** : la détection de script fait **71/71
> (1,0)** en **0,11 ms par langue**. Le niveau **multilingue** ne l'est **pas** : la détection de
> langue par trigrammes, en leave-one-out, fait **203/1486 =
> 0.1366** contre une **classe majoritaire à 0.0316** (`en`). C'est
> mieux que le hasard, mais **pas utilisable** : le contrôle « une heuristique rapide mais fausse
> coûte plus qu'un appel réseau » s'applique.

## 1. Le dispositif

- **Donnée** : `tools/jeux/lexique_multilingue.json` — 71 langues, 35 concepts, labels Wikidata
  (CC0) ; 1487 labels, courts (quelques mots).
- **Niveaux mesurés** : graphème (script) et multilingue (langue). Le **POS n'est pas mesuré** :
  le gold POS est FR/EN, les 71 langues n'en ont pas.
- **Script** : `detecter_script` sur le texte concaténé de chaque langue, contre ses écritures
  connues (`Arab`, `Cyrl`, `Deva`, `Hang`, `Jpan`, `Hani`… ; `Latn` par défaut).
- **Langue** : profils de trigrammes (`_profil`, 200 trigrammes) ; **leave-one-out** — on retire
  le label testé du profil de sa langue, on détecte, on compare ; **sans indice** (pas de prior).
- **Contrôle** : la classe majoritaire (`en`, 0.0316) — le taux doit la
  dépasser pour être utile.

## 2. Les résultats

| niveau | mesure | valeur | coût |
|---|---|---:|---|
| **graphème (script)** | justes / langues | **71/71 = 1,0** | 0,11 ms/langue |
| **multilingue (langue)** | justes / labels (LOO) | **203/1486 = 0.1366** | 0,57 ms/label |
| **classe majoritaire** | baseline | 0,032 | — |

- Le **script** est **tenu** : 71 langues, 71 scripts acceptés, aucune erreur — c'est le niveau
  que le CPU doit faire, et il le fait.
- La **langue** fait **4,3× la baseline** (0,137 / 0,032) mais reste **loin d'un détecteur** :
  sur des libellés de deux ou trois mots, les trigrammes ne suffisent pas.
- Le **POS** n'est pas dans ce tableau : il demanderait un gold par langue.

## 3. Le contrôle négatif

- **La classe majoritaire** (0,032) : le taux de langue la dépasse, donc le détecteur apprend
  **quelque chose** — mais 13,7 % n'est pas une couverture.
- **« Rapide mais faux »** : le détecteur coûte 0,57 ms/label ; s'il se trompe 86 % du temps, il
  **coûte plus** qu'un appel réseau qui tranche. C'est exactement le contrôle du contrat.
- **Le script** : 0,11 ms/langue pour 1,0 — le CPU est **sûr** là où il est fort.

## 4. Le texte long (UDHR) : la longueur est le levier

Sur le corpus **UDHR** (`data/udhr/articles.jsonl`, articles 0–14 en profil, article 15 en test) :

| mesure | valeur |
|---|---:|
| langues profilées | **398** |
| articles de test | **447** |
| **langue (accuracy)** | **0,9687** |
| script (accuracy) | **1,0** |
| **contrôle permuté** (profils mélangés) | **0,0022** (≈ 1/398) |
| durée | 3,56 s |

- **La langue sur texte long est fiable** (0,9687) ; le contrôle permuté tombe au hasard (0,0022),
  donc le score n'est pas un artefact.
- **Le contraste est net** : 0,9687 sur des articles, **0,137** sur des libellés de deux ou trois
  mots. La frontière n'est pas « le CPU sait / ne sait pas » : elle est **une question de longueur
  du texte**.
- Le **script** est à 1,0 dans les deux régimes.

## 5. Ce qui pourrait rendre ce résultat faux

- Les **écritures** de chaque langue sont une table (à relire) ; les langues à écriture mixte
  (`sr`, `az`, `uz`, `bs`) acceptent deux scripts.
- Les libellés sont **courts** : la détection de langue y est structurellement défavorisée.
- Le lexique est un **sous-ensemble** (35 concepts) des langues, pas un corpus.
- Un seul passage, sans indice.

## 6. La suite de L

1. **La porte des quatre modes** sur le gold 432 : heuristique, neuronal, parallèle, cascade —
   le même tableau, une ligne par mode.
2. **La langue sur texte long** : la mesure sur des phrases (pas des libellés) dirait si le
   détecteur est utilisable quand le texte est long.
3. **Le POS multilingue** : il demande un gold par langue ; il n'existe pas encore.

## 7. Fichiers

- [`pensee-frontiere-71.json`](pensee-frontiere-71.json) — la mesure et le détail par langue.
- [`tools/tests/linguistique/qualifier_frontiere_71.py`](../tools/tests/linguistique/qualifier_frontiere_71.py) —
  le banc.
- [`docs/theorie/contrat-bloc-langue.md`](../docs/theorie/contrat-bloc-langue.md) — le contrat.
