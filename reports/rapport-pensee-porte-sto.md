# B13 — la porte stochastique : le 7B l'ouvre (31 nœuds, 6 sonde, 13,0 s) ; sans la règle, 200/3/182,6 s ; le hasard par chance

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 ·
> **Verdict** : ✅ **la porte stochastique discrimine** — le 7B, avec le prompt `porte_sto`
> (la porte `(3,3)`, la sonde depuis `(3,2)` si tu réponds `bas`, **80 %** de chance, et
> « réessaie »), atteint le but en **31 nœuds**, **6 sonde**, **8 appels**, **13,0 s** ; sans
> la règle (prompt `labyrinthe`), il échoue à **200 nœuds**, **3 sonde**, **182,6 s**, sans but.
> L'**oracle** fait 28 nœuds/5 sonde ; l'**aveugle** échoue (200 nœuds, 61 sonde) ; la
> **Q-table** `PolitiqueAppriseOuverte` (80 %) passe en **9 pas / 2 essais** ; le **hasard**
> passe par chance (44/7) — la limite est nommée.
>
> **Dispositif** : [`qualifier_porte_sto_drvm.py`](../tools/tests/qualifier_porte_sto_drvm.py) ;
> [`operateurs.py`](../tools/pensee/operateurs.py) (`LABYRINTHE_PORTE_STO`, `REGISTRE_PSTO`,
> `PolitiqueLLM(jeu="porte_sto")`) ; JSON
> [`pensee-porte-sto.json`](pensee-porte-sto.json).

## 1. Ce qui était mesuré

La porte stochastique (`LABYRINTHE_PORTE_STO`) : depuis `(3,2)`, la sonde ouvre la porte
`(3,3)` avec **80 %** de chance ; en cas d'échec, le pas ne change pas l'état (il faut
**réessayer**). C'est le test qui doit **discriminer** la politique, après la porte (27 nœuds),
la minute (26), la mobile (test faible) et la bouge (test faible). La question : la règle
« 80 %, réessaie » dans le prompt suffit-elle, et le test discrimine-t-il ?

## 2. Le dispositif

- **Problème** : `LABYRINTHE_PORTE_STO`, `REGISTRE_PSTO` (`pas`, `saut`, `sonde`), but
  `(4,4)`, budget 200, A*.
- **Prompt `porte_sto`** : les murs, la porte `(3,3)`, « depuis `(3,2)`, la sonde l'ouvre si tu
  réponds `bas`, mais elle ne s'ouvre qu'avec **80 %** de chance ; en cas d'échec, **réessaie** »,
  l'état `open`, le but.
- **Contrôle** : prompt `labyrinthe` (sans la porte).
- **Politiques** : oracle `PolitiqueManhattan`, `PolitiqueAveugle`, `PolitiqueHasard`,
  `PolitiqueLLM(jeu="porte_sto")`, `PolitiqueLLM(jeu="labyrinthe")`, et la Q-table
  `PolitiqueAppriseOuverte(1000 épisodes)` (T33, la référence sans A*).
- **Commande** :
  `python3 tools/tests/qualifier_porte_sto_drvm.py --endpoint http://127.0.0.1:18082 --sortie reports/pensee-porte-sto.json`.

## 3. Les résultats

| politique | but | nœuds | coût | appels | sonde | latence |
|---|---|---:|---:|---:|---:|---:|
| oracle (Manhattan) | ✅ | 28 | 58,0 | 7 | 5 | 0,0 |
| **aveugle** | ❌ | 200 | 483,0 | 66 | 61 | 0,0 |
| **hasard** | ✅ | 44 | 86,0 | 14 | 7 | 0,0 |
| **LLM `porte_sto`** | ✅ | **31** | **66,0** | **8** | **6** | **13,0** |
| **LLM `labyrinthe`** | ❌ | 200 | 265,0 | 95 | 3 | **182,6** |
| Q-table `PolitiqueAppriseOuverte` | ✅ | — | — | — | — | 9 pas, 2 essais |

- **La règle fait la différence** : 200 nœuds/sans but (le labyrinthe, 182,6 s) → **31 nœuds/but**
  (6 sonde, 8 appels, 13,0 s). Le 7B **réessaie** (6 sonde) et passe.
- **Le test discrimine** : l'aveugle échoue (200/61) ; le labyrinthe échoue (200/3) ; le 7B passe.
  C'est le premier test de porte qui **sépare** la politique de l'aveugle et du labyrinthe.
- **La Q-table** (74 états-Q, 1000 épisodes) passe en **9 pas / 2 essais** (le 80 %).
- **Le hasard** passe par chance (44/7) : la porte peut s'ouvrir à 80 % du premier coup ; la
  limite est nommée (le contrôle propre est l'aveugle et le labyrinthe).

## 4. Les contrôles

- **Prompt `porte_sto` vs `labyrinthe`** : but à 31 nœuds (6 sonde) contre pas de but à 200
  (3 sonde). La règle « 80 %, réessaie » est la variable.
- **Aveugle** : ❌ (200/61) — le `droite` ne vise pas la porte.
- **Labyrinthe** : ❌ (200/3) — sans la porte, le modèle ne réessaie pas.
- **Hasard** : ✅ par chance (44/7) — la 80 % du premier coup.
- **Q-table** : ✅ (9 pas, 2 essais) — la référence.
- **Oracle** : ✅ (28/5).

## 5. Ce qui pourrait rendre ce résultat faux

- **Le hasard passe** (44/7) : la porte s'ouvre à 80 % ; le contrôle propre est l'aveugle et le
  labyrinthe, pas le hasard.
- **Le tirage aléatoire** (`random.random()`) n'est pas fixé ; une seule exécution ; le 6 sonde
  du 7B et les 2 essais de la Q-table en dépendent. Le test pourrait être rejoué 5 fois.
- **La latence** (13,0 s) inclut la file du serveur ; 8 appels ; CPU seulement.
- **Le 7B** fait 31 nœuds (l'oracle 28) : le tie-breaking de l'A* ; le but et la sonde sont les
  mesures.
- **La porte est sur le chemin** ; l'aveugle/labyrinthe échouent quand même : la règle compte.

## 6. La suite

1. **Cinq graines** sur la porte stochastique : le 7B passe-t-il 5/5 ? (le tirage aléatoire).
2. **La fenêtre temporelle** (`LABYRINTHE_PORTE_FENETRE`, `attendre`, `t % 3 == 0`) : la porte
   n'est libre qu'à l'heure ; le prompt doit porter l'horloge.
3. **Le gold 200+** et la **pragmatique** (l'heuristique garde) : la ligne L.
4. **La fonction « la bonne réponse, pas le voisin »** (T132/T133, distracteurs r428–r432).

## 7. Fichiers

- [`tools/tests/qualifier_porte_sto_drvm.py`](../tools/tests/qualifier_porte_sto_drvm.py) —
  le banc (oracle, Q-table, aveugle, hasard, LLM).
- [`tools/pensee/operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueLLM(jeu="porte_sto")`,
  `LABYRINTHE_PORTE_STO`, `REGISTRE_PSTO`.
- [`tools/tests/test_pensee_politique.py`](../tools/tests/test_pensee_politique.py) — 9 tests
  (le prompt `porte_sto` : le 80 %, le réessai).
- [`pensee-porte-sto.json`](pensee-porte-sto.json) — les mesures, les seuils, les limites.
