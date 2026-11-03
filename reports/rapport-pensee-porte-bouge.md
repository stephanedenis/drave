# B13 — la porte qui bouge : le 7B la passe (25 nœuds, 2 sonde) comme l'aveugle (25/2) et le labyrinthe (28/5) ; test non discriminant

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 ·
> **Verdict** : ❌ **la porte qui bouge ne qualifie pas la politique** — le 7B, avec le prompt
> `porte_bouge` (la phase `t % 6` et la porte du moment), passe (25 nœuds, 2 sonde, 13,4 s) ;
> mais l'**aveugle** (25/2), le **hasard** (27/4) et le **labyrinthe** (28/5) passent **aussi**.
> L'oracle (Manhattan) fait 28/5 ; la **Q-table** `PolitiqueAppriseBouge` (236 états-Q) passe en
> **10 pas**. La phase dans le prompt **ne change rien** : le test est faible.
>
> **Dispositif** : [`qualifier_porte_bouge_drvm.py`](../tools/tests/qualifier_porte_bouge_drvm.py) ;
> [`operateurs.py`](../tools/pensee/operateurs.py) (`LABYRINTHE_PORTE_BOUGE`, `REGISTRE_PB`,
> `PolitiqueLLM(jeu="porte_bouge")`) ; JSON
> [`pensee-porte-bouge.json`](pensee-porte-bouge.json).

## 1. Ce qui était mesuré

La porte qui bouge (`LABYRINTHE_PORTE_BOUGE`) : la porte est en `(3,3)` ou `(1,3)` selon la
phase `t % 6` (`_d_bouge(t)`, période 3), le pas avance l'horloge, la sonde ouvre la porte **du
moment** si la politique vise sa direction. C'est la suite de la porte (27 nœuds), de la porte
minute (26 nœuds) et de la porte mobile (test faible) : la question est de savoir si la phase
dans le prompt suffit, et si le test **discrimine**.

## 2. Le dispositif

- **Problème** : `LABYRINTHE_PORTE_BOUGE`, `REGISTRE_PB` (`pas`, `saut`, `sonde`), but `(4,4)`,
  budget 200, A*.
- **Prompt `porte_bouge`** : les murs, la **phase** `t` (t % 6), la porte du moment
  `(px,py)`, la règle « depuis une case voisine, la sonde l'ouvre si tu vises sa direction »,
  l'état `open`, le but. Le **contrôle** : prompt `labyrinthe` (sans la phase ni la porte).
- **Politiques** : oracle `PolitiqueManhattan` (T34), `PolitiqueAveugle`, `PolitiqueHasard`,
  `PolitiqueLLM(jeu="porte_bouge")`, `PolitiqueLLM(jeu="labyrinthe")`, et la Q-table
  `PolitiqueAppriseBouge(1000 épisodes)` (la référence sans A*, T34).
- **Commande** :
  `python3 tools/tests/qualifier_porte_bouge_drvm.py --endpoint http://127.0.0.1:18082 --sortie reports/pensee-porte-bouge.json`.

## 3. Les résultats

| politique | but | nœuds | coût | appels | sonde | latence |
|---|---|---:|---:|---:|---:|---:|
| oracle (Manhattan) | ✅ | 28 | 58,0 | 7 | 5 | 0,0 |
| **aveugle** | ✅ | 25 | 43,0 | 7 | 2 | 0,0 |
| **hasard** | ✅ | 27 | 53,0 | 7 | 4 | 0,0 |
| **LLM `porte_bouge`** | ✅ | 25 | 43,0 | 7 | 2 | **13,4** |
| **LLM `labyrinthe`** | ✅ | 28 | 58,0 | 7 | 5 | **13,3** |
| Q-table `PolitiqueAppriseBouge` | ✅ | — | — | — | — | 10 pas |

- **Tout le monde passe** : l'aveugle (25/2), le hasard (27/4), le LLM (25/2), le labyrinthe
  (28/5), l'oracle (28/5). La phase dans le prompt **ne change rien** : le 7B fait exactement
  le score de l'aveugle.
- **La Q-table** (236 états-Q, 1000 épisodes) passe en **10 pas** : la référence robuste.
- **Le test ne discrimine pas** : les portes `(3,3)`/`(1,3)` sont sur les chemins de l'aveugle
  et du labyrinthe ; l'A* explore ; la sonde ouvre la porte du moment.

## 4. Les contrôles

- **Prompt `porte_bouge` vs `labyrinthe`** : 25/2 contre 28/5 — les deux passent ; la phase
  n'est pas la variable.
- **Aveugle** : ✅ (25/2) — son `droite` ouvre la porte `(1,3)` depuis `(0,3)`.
- **Hasard** : ✅ (27/4) — la chance suffit.
- **Q-table** : ✅ (10 pas) — la référence sans A*.
- **Oracle** : ✅ (28/5).

## 5. Ce qui pourrait rendre ce résultat faux

- **Le test est faible** : les portes sont sur les chemins ; l'aveugle et le labyrinthe
  passent ; la phase n'est pas nécessaire. Le test ne mesure pas la politique.
- **Le 7B fait le score de l'aveugle** (25/2) : il n'ajoute rien ; c'est un **négatif** pour le
  prompt `porte_bouge`, pas une preuve.
- **Le hasard** passe (27/4) : la chance suffit.
- **La latence** (13,4 s) inclut la file du serveur ; 7 appels ; CPU seulement.
- **Une seule graine**, température 0, grammaire ; la Q-table a 1000 épisodes.

## 6. La suite

1. **La porte stochastique** (`LABYRINTHE_PORTE_STO`, `sonde_p_sto` à 80 %) : la porte peut
   **refuser** ; l'aveugle et le labyrinthe devraient échouer, la règle compter.
2. **La fenêtre temporelle** (`LABYRINTHE_PORTE_FENETRE`, `attendre`, `t % 3 == 0`) : la porte
   n'est libre qu'à l'heure ; le prompt doit porter l'horloge.
3. **Le gold 200+** et la **pragmatique** (l'heuristique garde) : la ligne L.
4. **La fonction « la bonne réponse, pas le voisin »** (T132/T133, distracteurs r428–r432).

## 7. Fichiers

- [`tools/tests/qualifier_porte_bouge_drvm.py`](../tools/tests/qualifier_porte_bouge_drvm.py) —
  le banc (oracle, Q-table, aveugle, hasard, LLM).
- [`tools/pensee/operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueLLM(jeu="porte_bouge")`,
  `LABYRINTHE_PORTE_BOUGE`, `REGISTRE_PB`, `PolitiqueAppriseBouge`.
- [`tools/tests/test_pensee_politique.py`](../tools/tests/test_pensee_politique.py) — 8 tests
  (le prompt bouge : la phase, la porte `(1,3)`).
- [`pensee-porte-bouge.json`](pensee-porte-bouge.json) — les mesures, les seuils, les limites.
