# B13 — la porte mobile : le 7B échoue à (3,3) (200 nœuds, 3 sonde) et passe à (1,3) comme l'aveugle (26/2) et le labyrinthe (29/5) ; test non discriminant

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 ·
> **Verdict** : ❌ **la porte mobile ne qualifie pas la politique** — le 7B, avec le prompt
> `porte_mobile` (la position de la porte), **échoue à `(3,3)`** (200 nœuds, 3 sonde, 228,8 s)
> et **passe à `(1,3)`** (28 nœuds, 4 sonde, 14,4 s) ; mais à `(1,3)`, l'**aveugle** (26 nœuds,
> 2 sonde), le **hasard** (28/4) et le **labyrinthe** (29/5) passent **aussi**. L'oracle
> (Manhattan) et la **Q-table** (`PolitiqueAppriseMobile`, T31) passent les deux positions.
> La porte mobile est un **test faible** : elle ne discrimine ni la position ni la règle.
>
> **Dispositif** : [`qualifier_porte_mobile_drvm.py`](../tools/tests/qualifier_porte_mobile_drvm.py) ;
> [`operateurs.py`](../tools/pensee/operateurs.py) (`PolitiqueLLM(jeu="porte_mobile")`,
> `LABYRINTHE_PORTE_MOBILE_0/1`, `REGISTRE_PMOB`) ; JSON
> [`pensee-porte-mobile.json`](pensee-porte-mobile.json).

## 1. Ce qui était mesuré

La porte mobile (`LABYRINTHE_PORTE_MOBILE_0/1`) place la porte en **`(3,3)`** ou en **`(1,3)`**
— cette dernière est dans un mur du labyrinthe. La sonde ouvre la porte si la politique **vise**
sa direction depuis une case voisine. C'est la suite de la porte (27 nœuds) et de la porte minute
(26 nœuds) : la question est de savoir si la **position** de la porte dans le prompt suffit, et
si le test **discrimine** la politique.

## 2. Le dispositif

- **Deux problèmes** : `LABYRINTHE_PORTE_MOBILE_0` (porte `(3,3)`) et `_1` (porte `(1,3)`) ;
  `REGISTRE_PMOB` (`pas`, `saut`, `sonde`), but `(4,4)`, budget 200, A*.
- **Prompts** : `porte_mobile` (les murs, la porte mobile `(px,py)`, la règle « depuis une case
  voisine, la sonde l'ouvre si tu vises sa direction », l'état `open`, le but) et `labyrinthe`
  (sans la porte : le contrôle).
- **Politiques** : oracle `PolitiqueManhattan`, `PolitiqueAveugle`, `PolitiqueHasard`,
  `PolitiqueLLM(jeu="porte_mobile")`, `PolitiqueLLM(jeu="labyrinthe")`, et la Q-table
  `PolitiqueAppriseMobile(1000 épisodes)` (la référence sans A*, T31).
- **Commande** :
  `python3 tools/tests/qualifier_porte_mobile_drvm.py --endpoint http://127.0.0.1:18082 --sortie reports/pensee-porte-mobile.json`.

## 3. Les résultats

| porte | politique | but | nœuds | coût | appels | sonde | latence |
|---|---|---:|---:|---:|---:|---:|---:|
| **(3,3)** | oracle | ✅ | 29 | 60,0 | 7 | 5 | 0,0 |
| **(3,3)** | aveugle | ❌ | 200 | 483,0 | 66 | 61 | 0,0 |
| **(3,3)** | hasard | ✅ | 45 | 88,0 | 14 | 7 | 0,0 |
| **(3,3)** | **LLM `porte_mobile`** | ❌ | 200 | 265,0 | 95 | 3 | **228,8** |
| **(3,3)** | LLM `labyrinthe` | ❌ | 200 | 265,0 | 95 | 3 | 144,0 |
| **(1,3)** | oracle | ✅ | 29 | 59,0 | 7 | 5 | 0,0 |
| **(1,3)** | **aveugle** | ✅ | 26 | 44,0 | 7 | 2 | 0,0 |
| **(1,3)** | hasard | ✅ | 28 | 54,0 | 7 | 4 | 0,0 |
| **(1,3)** | **LLM `porte_mobile`** | ✅ | 28 | 54,0 | 7 | 4 | **14,4** |
| **(1,3)** | LLM `labyrinthe` | ✅ | 29 | 59,0 | 7 | 5 | 17,1 |

- **À `(3,3)`, le 7B échoue** : 200 nœuds, 3 sonde, 228,8 s, sans but — comme le prompt
  `labyrinthe` (200/3/144,0). Le modèle ne vise pas la porte au bon moment ; l'A* explore.
- **À `(1,3)`, tout le monde passe** : l'aveugle (26/2), le hasard (28/4), le LLM (28/4), le
  labyrinthe (29/5), l'oracle (29/5). Le test **ne discrimine pas**.
- **La Q-table** (`PolitiqueAppriseMobile`, 1000 épisodes, 170 états-Q) passe **les deux**
  positions en **8 pas** ; l'oracle aussi. La politique robuste est la Q-table, pas le 7B.
- **Le hasard** passe `(3,3)` (45/7) et `(1,3)` (28/4) : la porte est sur le chemin, et
  l'aveugle la vise par `droite` à `(1,3)` (`(0,3)` → `(1,3)`).

## 4. Les contrôles

- **Prompt `porte_mobile` vs `labyrinthe`** : à `(3,3)`, les deux échouent (200/3) ; à `(1,3)`,
  les deux passent (28/4 et 29/5). La position de la porte dans le prompt **ne change pas** le
  résultat.
- **Aveugle** : `(3,3)` ❌ (200/61), `(1,3)` ✅ (26/2) — la porte `(1,3)` est sur son chemin.
- **Hasard** : ✅ aux deux — la chance suffit.
- **Q-table** : ✅ aux deux (8 pas) — la référence sans A*.
- **Oracle** : ✅ aux deux (29/5).

## 5. Ce qui pourrait rendre ce résultat faux

- **Le test est faible** : à `(1,3)`, l'aveugle et le labyrinthe passent ; à `(3,3)`, le 7B et
  le labyrinthe échouent. Le mobile ne mesure ni la position ni la règle ; il mesure l'A* et la
  chance.
- **Le 7B à `(3,3)`** : 3 sonde, 95 appels, 228,8 s — le modèle ne vise pas la porte depuis
  `(3,2)` ; le prompt donne pourtant `(3,3)`. C'est un **échec du prompt/du modèle**, pas du
  problème.
- **La latence** (228,8 s) inclut la file du serveur ; 95 appels à ~2,4 s ; CPU seulement.
- **Le hasard** et l'aveugle passent `(1,3)` : la porte est sur le chemin ; le contrôle propre
  serait une porte **hors** du chemin, pas seulement une autre position.
- **Une seule graine**, température 0, grammaire ; la Q-table a 1000 épisodes.

## 6. La suite

1. **La porte stochastique** (`LABYRINTHE_PORTE_STO`/`_etat_pb`, `PolitiqueAppriseAleatoire`) :
   la porte saute ; l'aveugle et le labyrinthe devraient échouer, la règle compter.
2. **La porte temporelle** (`_etat_pw`, `attendre`, `sonde_pw`) : la porte n'est libre qu'à
   `t % 3 == 0` ; le prompt doit porter l'horloge, et l'A* attend.
3. **Le gold 200+ phrases** et la **pragmatique** (l'heuristique garde) : la ligne L.
4. **La porte B13** : les 4 attendus du S `647205a` (le S a livré le corpus réel/banque 200) et
   le test anaphorique T132/T133.

## 7. Fichiers

- [`tools/tests/qualifier_porte_mobile_drvm.py`](../tools/tests/qualifier_porte_mobile_drvm.py) —
  le banc (deux positions, oracle, Q-table, aveugle, hasard, LLM).
- [`tools/pensee/operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueLLM(jeu="porte_mobile")`,
  `LABYRINTHE_PORTE_MOBILE_0/1`, `REGISTRE_PMOB`.
- [`tools/tests/test_pensee_politique.py`](../tools/tests/test_pensee_politique.py) — 7 tests
  (le prompt mobile : la porte `(1,3)`, la position `(1,2)`, les murs sans la porte).
- [`pensee-porte-mobile.json`](pensee-porte-mobile.json) — les deux positions, les seuils, les
  limites.
