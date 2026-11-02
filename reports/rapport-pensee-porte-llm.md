# B13 — la porte DRVM : la règle dans le prompt l'ouvre (27 nœuds, 4 sonde)

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 ·
> **Verdict** : ✅ **la porte est rouverte par la règle** — avec le prompt `porte` qui décrit la
> porte `(3,3)` et la règle « depuis `(3,2)`, la sonde l'ouvre si tu réponds `bas` », le 7B
> atteint le but en **27 nœuds**, **4 sonde**, **7 appels**, **12,0 s** ; **sans** la règle
> (l'ancien prompt du labyrinthe), il échouait à **200 nœuds**, 3 appels, **179,5 s**, sans but.
> L'**oracle** fait 28 nœuds/5 sonde ; l'**aveugle** échoue (200 nœuds, 61 sonde) ; le
> **hasard** ouvre par chance (44 nœuds, 7 sonde).
>
> **Dispositif** : [`qualifier_porte_drvm.py`](../tools/tests/qualifier_porte_drvm.py) ;
> [`operateurs.py`](../tools/pensee/operateurs.py) (`PolitiqueLLM`, `jeu="porte"`) ; JSON
> [`pensee-porte-llm.json`](pensee-porte-llm.json).

## 1. Ce qui était mesuré

La fiche DRVM/native ([`pensee-politique-llm`](rapport-pensee-politique-llm.md)) laissait la
**porte** comme un négatif : le 7B échouait (200 nœuds, 3 sonde, 179,5 s) parce que le prompt du
labyrinthe **ne décrivait pas la porte**. Le cadenas, lui, s'ouvrait avec la règle explicite
(3 nœuds) et pas sans (0). La question : la porte est-elle un négatif du **modèle** ou du
**prompt** ?

## 2. Le dispositif

- **Problème** : `LABYRINTHE_PORTE` — grille 5×5, murs `MURS_P`, porte `(3,3)` fermée, but
  `(4,4)` ; la `sonde` ouvre la porte **seulement** depuis `(3,2)` avec la direction `bas`
  (`sonde_p`), puis le chemin passe par `(3,3)` et `(4,3)`.
- **Prompt `porte`** : les murs du labyrinthe-porte, la porte `(3,3)`, la règle « depuis
  `(3,2)`, la sonde ouvre la porte si tu réponds `bas` », l'état `open` (oui/non), le but
  `(4,4)`. La grammaire GBNF impose `droite`/`gauche`/`bas`/`haut`.
- **Politiques** : oracle `PolitiqueManhattan` (elle dit `bas` à `(3,2)`), aveugle
  `PolitiqueAveugle`, hasard `PolitiqueHasard` (graine 0), LLM `PolitiqueLLM(jeu="porte")`.
  `DRVM`, `AStar`, `Budget(200)`.
- **Contrôle négatif du prompt** : l'ancien prompt (labyrinthe, sans la porte) est mesuré dans
  [`pensee-politique-llm.json`](pensee-politique-llm.json) : 200 nœuds, 3 appels, 179,5 s, sans
  but. Même modèle, mêmes poids, seule la description change.
- **Commande** :
  `python3 tools/tests/qualifier_porte_drvm.py --endpoint http://127.0.0.1:18082 --sortie reports/pensee-porte-llm.json`.

## 3. Les résultats

| politique | but | nœuds | coût | appels | sonde | latence |
|---|---|---:|---:|---:|---:|---:|
| **oracle** | ✅ | 28 | 58,0 | 7 | 5 | 0,0 |
| **aveugle** | ❌ | 200 | 483,0 | 66 | 61 | 0,0 |
| **hasard** | ✅ | 44 | 86,0 | 14 | 7 | 0,0 |
| **LLM, ancien prompt** (sans la porte) | ❌ | 200 | 265,0 | 95 | 3 | **179,5** |
| **LLM, prompt `porte`** | ✅ | **27** | **53,0** | **7** | **4** | **12,0** |

- **La règle fait la différence** : 200 nœuds/sans but → **27 nœuds/but**, 4 sonde, 7 appels,
  12,0 s. Le LLM fait **un nœud de moins que l'oracle** (27 contre 28) et **une sonde de moins**
  (4 contre 5) ; le coût symbolique est 53 contre 58. La différence de nœuds n'est pas une
  preuve de qualité (le tie-breaking de l'A*), mais le but et la sonde le sont.
- **Le hasard ouvre** la porte par chance (44 nœuds, 7 sonde) : la porte n'est pas un contrôle
  propre à **toute** politique ; c'est l'**aveugle** (200 nœuds, 61 sonde, sans but) qui la
  distingue.
- **La latence** : 12,0 s pour 7 appels (~1,7 s/appel) ; l'ancien prompt avait payé 179,5 s pour
  3 appels (file du serveur). Le nouveau run explore moins, donc appelle moins.

## 4. Les contrôles négatifs

- **Ancien prompt vs prompt `porte`** (même modèle, mêmes poids, même problème) : sans but à
  200 nœuds contre but à 27 nœuds. La **description** est la variable.
- **Aveugle** : 200 nœuds, 61 sonde, sans but — la porte reste fermée.
- **Hasard** : but par chance (44 nœuds) ; il ne prouve pas la politique, il montre que la
  porte n'est pas un négatif propre.
- **Oracle** : but, 28 nœuds, 5 sonde — la référence.

## 5. Ce qui pourrait rendre ce résultat faux

- **Le prompt `porte` est écrit après l'échec de l'ancien** : c'est une comparaison à deux
  points sur **un** problème. La règle est explicite et le modèle l'exécute ; il ne la
  **découvre** pas. Le résultat dit « le modèle suit une règle de porte », pas « le modèle
  comprend une porte ».
- **Le hasard ouvre la porte** (44 nœuds) : la porte seule n'est pas un contrôle de qualité ;
  c'est l'aveugle qui l'est.
- **Le nombre de nœuds** (27 vs 28) dépend du tie-breaking de l'A*, de l'ordre des opérateurs
  et de la politique ; ne pas lire comme un gain de qualité. Le but, la sonde et le coût sont
  les mesures.
- **La latence** inclut la file du serveur ; 12 s pour 7 appels est cohérent, 179,5 s pour 3
  appels ne l'était pas (l'ancien run était ralenti).
- **Une seule graine**, température 0, grammaire ; CPU seulement.
- **La porte B13** reste à 134/140 (six rouges S) ; la politique a **6 tests unitaires**, pas un
  T dans la porte B13.

## 6. La suite

1. **Une porte qui bouge** (`LABYRINTHE_PORTE_MINUTE`/`STO`) : la règle change avec le temps ou
   le bruit ; le prompt devra la porter, et le modèle devra la suivre. C'est le test de
   **généralisation** de la politique.
2. **Le coût** : comparer `PolitiqueLLM` à `PolitiqueApprise`/`PolitiqueReseau` (CPU, sans
   serveur) sur la même porte ; le LLM est ~1,7 s/appel.
3. **La pragmatique neuronale** et le **gold 200+ phrases** : la ligne L, pas B13.
4. **La porte B13** : les six rouges S ; les remettre à jour ou les qualifier.

## 7. Fichiers

- [`tools/pensee/operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueLLM` (`jeu="porte"`),
  la règle et le prompt.
- [`tools/tests/qualifier_porte_drvm.py`](../tools/tests/qualifier_porte_drvm.py) — le banc
  (oracle, aveugle, hasard, LLM).
- [`tools/tests/test_pensee_politique.py`](../tools/tests/test_pensee_politique.py) — 6 tests de
  contrat (cadenas, variantes, labyrinthe, porte, refus, serveur absent).
- [`pensee-porte-llm.json`](pensee-porte-llm.json) — les mesures, les seuils, les limites.
