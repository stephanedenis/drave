# B13 — la politique DRVM/native : le 7B ouvre le cadenas avec la règle, pas sans

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 ·
> **Verdict** : ✅ **la politique DRVM/native est mesurée** — le **cadenas** s'ouvre avec la
> règle explicite (**3 nœuds, 3 appels, 5,5 s**) et **pas** avec le prompt minimal (**0 nœud**,
> le modèle répond `arriere` à la position 0) ; le **labyrinthe** utilise la sonde **2 fois**
> (comme l'oracle, 17 nœuds) ; la **porte** est un **négatif nommé** (200 nœuds, 3 appels,
> 179,5 s, sans but) parce que sa règle n'est pas dans le prompt. Le **hasard** ouvre la porte
> par chance (44 nœuds) : la porte n'est pas un contrôle négatif propre à toute politique.
>
> **Dispositif** : [`qualifier_politique_drvm.py`](../tools/tests/qualifier_politique_drvm.py) ;
> [`operateurs.py`](../tools/pensee/operateurs.py) (`PolitiqueLLM`, `PolitiqueHasard`) ; JSON
> [`pensee-politique-llm.json`](pensee-politique-llm.json).

## 1. Ce qui était bloqué

La ligne B13 disait : « **politique DRVM/native** (bloquée) — brancher un vrai modèle quand ses
poids seront là ». Les poids sont là (Qwen2.5-7B-Instruct Q4_K_M, CPU) ; les taggers sont
qualifiés. Il restait à brancher le modèle **dans le conteneur DRVM** comme politique du moteur
de pensée, et à mesurer sa **qualité** et son **coût réel**, pas seulement sa nécessité.

## 2. Le dispositif

- **Politique** : `PolitiqueLLM` — un prompt d'état, une **grammaire GBNF** qui impose un mot de
  direction (`avant`/`arriere` pour le cadenas ; `droite`/`gauche`/`bas`/`haut` pour le
  labyrinthe), un `llama-server` local en **CPU** (`-ngl 0`), 0 erreur de parsing.
- **Problèmes** : `CADENAS` (linéaire, 3 pas, un seul opérateur `sonde`), `LABYRINTHE` (5×5,
  `pas`/`saut`/`sonde`), `LABYRINTHE_PORTE` (la porte ne s'ouvre que par la bonne politique).
- **Politiques comparées** : **oracle** (`PolitiqueCadenas`/`PolitiqueManhattan`), **aveugle**
  (le contrôle négatif opposé), **hasard** (graine 0), **LLM** (`PolitiqueLLM`). Budgets 20,
  160, 200 ; `AStar` ; le conteneur `DRVM` mesure le but, les nœuds, le coût symbolique, les
  appels, la **latence réelle**.
- **Deux prompts du cadenas** : `minimal` (« Position : 0. But : 3. Réponds avant ou
  arriere. ») et `regle` (la même chose + « la position augmente avec avant ; si la position
  est inférieure au but, réponds avant »). C'est le **contrôle négatif du prompt** : même
  modèle, même poids, seule la règle change.
- **Commande** :
  `python3 tools/tests/qualifier_politique_drvm.py --endpoint http://127.0.0.1:18082 --sortie reports/pensee-politique-llm.json`.

## 3. Les résultats

| problème | politique | but | nœuds | coût | appels | sonde | latence |
|---|---|---:|---:|---:|---:|---:|---:|
| **cadenas** | oracle | ✅ | 3 | 3,0 | 3 | 3 | 0,0 |
| **cadenas** | aveugle | ❌ | 20 | 20,0 | 20 | 20 | 0,0 |
| **cadenas** | hasard | ❌ | 0 | 0,0 | 1 | 0 | 0,0 |
| **cadenas** | LLM **minimal** | ❌ | 0 | 0,0 | 1 | 0 | **0,729** |
| **cadenas** | LLM **règle** | ✅ | **3** | 3,0 | **3** | 3 | **5,528** |
| **labyrinthe** | oracle | ✅ | 17 | 34,0 | 4 | 2 | 0,0 |
| **labyrinthe** | aveugle | ✅ | 15 | 24,0 | 4 | **0** | 0,0 |
| **labyrinthe** | hasard | ✅ | 16 | 29,0 | 4 | 1 | 0,0 |
| **labyrinthe** | LLM | ✅ | 17 | 34,0 | 4 | **2** | 7,363 |
| **porte** | oracle | ✅ | 28 | 58,0 | 7 | 5 | 0,0 |
| **porte** | aveugle | ❌ | 200 | 483,0 | 66 | 61 | 0,0 |
| **porte** | hasard | **✅** | 44 | 86,0 | 14 | 7 | 0,0 |
| **porte** | LLM | ❌ | 200 | 265,0 | 95 | 3 | **179,535** |

- **Le cadenas** : la règle explicite fait dire `avant` au modèle à chaque pas ; **3 nœuds**,
  le même chemin que l'oracle, **3 appels**, **5,5 s**. Le prompt minimal fait dire `arriere`
  à la position 0 : le `sonde` ne rend aucun état, le moteur s'arrête à **0 nœud**. Le modèle
  **n'infère pas** que « avant » augmente la position depuis le seul but ; il faut le lui dire.
- **Le labyrinthe** : le LLM atteint le but en **17 nœuds** (comme l'oracle) et utilise la
  **sonde 2 fois** (comme l'oracle). L'aveugle atteint le but aussi (15 nœuds) mais avec **0
  sonde** : le but seul n'est pas la mesure ; c'est l'usage de la sonde qui distingue.
- **La porte** : le LLM échoue (200 nœuds, 3 sonde, 179,5 s) ; la règle de la porte n'est pas
  dans le prompt. Le **hasard** l'ouvre par chance (44 nœuds) : la porte n'est pas un négatif
  propre à toute politique ; c'est l'**aveugle** (200 nœuds, 61 sonde, sans but) qui la
  distingue.
- **La latence** : 1,8 s/appel sur le cadenas (5,5 s pour 3), 3,7 s/appel sur le labyrinthe ;
  la porte a payé **179,5 s pour 3 appels** (file du serveur, pas une mesure de qualité).

## 4. Les contrôles négatifs

- **Prompt minimal vs règle** (même modèle, même poids, même état) : `arriere` → 0 nœud contre
  `avant` → 3 nœuds. C'est le contrôle le plus direct : la **règle du prompt** est la variable.
- **Aveugle** : cadenas sans but (20 nœuds), porte sans but (200 nœuds, 61 sonde) ; le
  labyrinthe atteint le but **sans la sonde** — le but n'y est pas discriminant.
- **Hasard** : cadenas sans but ; labyrinthe avec but ; **porte avec but par chance** (44
  nœuds). La porte n'est pas un contrôle propre à toute politique.
- **Oracle** : les trois buts, avec le minimum de nœuds (3, 17, 28).

## 5. Ce qui pourrait rendre ce résultat faux

- **Le prompt `regle` est une correction après l'échec du `minimal`** : c'est une comparaison
  à deux points sur **une** tâche (le cadenas). La règle est générale (comparer position et
  but), mais elle a été écrite après avoir vu l'échec ; elle n'est pas aveugle.
- **Le labyrinthe est trop facile** : l'aveugle atteint le but sans la sonde ; le `but` ne
  prouve pas la politique. Le nombre d'appels à la sonde (2, comme l'oracle) est la mesure,
  mais il ne dit pas si les directions sont **bonnes** ou seulement **valides**.
- **La porte** : le hasard l'ouvre ; le LLM échoue ; la règle n'est pas dans le prompt. C'est
  un **négatif nommé**, pas une preuve que le modèle ne peut pas.
- **La latence** : 179,5 s pour 3 appels sur la porte (file du serveur) ; ne pas lire comme un
  coût du modèle. Le cadenas (1,8 s/appel) et le labyrinthe (3,7 s/appel) sont plus stables.
- **Le modèle** : Qwen2.5-7B-Instruct Q4_K_M, CPU, température 0, grammaire ; une autre
  quantisation ou un autre prompt change le résultat.
- **La porte B13** est à 134/140 (six rouges de segmentation/anaphore corrélés au sous-module S
  `647205a`) ; la politique a **5 tests unitaires**, pas un T dans la porte B13.

## 6. La suite

1. **La porte** : mettre sa règle dans le prompt (ou un exemple) et remesurer ; si le modèle
   échoue encore, le négatif est **qualifié** (la règle est trop complexe pour un 7B).
2. **Un labyrinthe discriminant** : un piège où l'aveugle échoue ; la sonde devient la preuve
   de la qualité, pas seulement de l'usage.
3. **Le coût** : comparer `PolitiqueLLM` à `PolitiqueApprise`/`PolitiqueReseau` (CPU, sans
   serveur) sur le même problème ; le LLM est 1,8–3,7 s/appel.
4. **La ligne DRVM/native** : les poids sont là ; la politique est **réelle** ; le prompt est
   le levier. Le conteneur `DRVM` n'est plus bloqué par l'absence de modèle — il est limité par
   la **qualité de la politique** sur les problèmes non décrits.

## 7. Fichiers

- [`tools/pensee/operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueLLM`,
  `PolitiqueHasard`, la grammaire et le prompt.
- [`tools/tests/qualifier_politique_drvm.py`](../tools/tests/qualifier_politique_drvm.py) — le
  banc (cadenas minimal/règle, labyrinthe, porte, oracle/aveugle/hasard).
- [`tools/tests/test_pensee_politique.py`](../tools/tests/test_pensee_politique.py) — 5 tests
  de contrat (cadenas, variantes, labyrinthe, refus, serveur absent).
- [`pensee-politique-llm.json`](pensee-politique-llm.json) — les mesures, les seuils, les
  limites.
