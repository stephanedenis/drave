# B13 — la fenêtre : contre-fiche — le BFS atteint le but en 331 nœuds ; l'oracle Manhattan et le Greedy échouent par fitness, pas la fenêtre

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 ·
> **Verdict** : ✅❌ **contre-fiche** — la fenêtre **est solvable** (BFS : 331 nœuds, 52 états) ; l'**oracle** (Manhattan) et le Greedy
> échoue : 200 nœuds, 1 sonde, 65 appels, sans but ; le 7B `porte_fenetre` échoue aussi (200
> nœuds, 35 sonde, 97,3 s) ; le labyrinthe (200/2), l'aveugle (200/0) et le hasard (200/12)
> échouent. **Le problème est solvable** : le BFS l'atteint à 331 nœuds ; l'A*/le Greedy échouent par **fitness** (score + heuristique),
> pas par carte. Les correctifs `_etat_pw` (t réel) et `Moteur.boucle` (break) sont dans ce commit.
>
> **Dispositif** : [`qualifier_porte_fenetre_drvm.py`](../tools/tests/qualifier_porte_fenetre_drvm.py) ;
> [`operateurs.py`](../tools/pensee/operateurs.py) (`LABYRINTHE_PORTE_FENETRE`, `REGISTRE_PW`,
> `PolitiqueLLM(jeu="porte_fenetre")`) ; JSON
> [`pensee-porte-fenetre.json`](pensee-porte-fenetre.json).

## 1. Ce qui était mesuré

La fenêtre (`LABYRINTHE_PORTE_FENETRE`) : la porte `(3,3)` n'est libre que lorsque `t % 3 == 0` ;
l'horloge avance à chaque pas, saut ou **attente**. C'est la suite des portes (27 nœuds), minute
(26), mobile (faible), bouge (faible), stochastique (5/5). La question : le prompt avec l'horloge
suffit-il, et le test discrimine-t-il ?

## 2. Le dispositif

- **Problème** : `LABYRINTHE_PORTE_FENETRE`, `REGISTRE_PW` (`pas`, `saut`, `attendre`, `sonde`),
  but `(4,4)`, budget 200, A*.
- **Prompt `porte_fenetre`** : les murs, la porte `(3,3)`, « libre seulement si `t % 3 == 0` »,
  l'horloge, « réponds bas quand `t % 3 == 0`, sinon **attends** ».
- **Contrôle** : prompt `labyrinthe` (sans l'horloge).
- **Politiques** : oracle `PolitiqueManhattan`, `PolitiqueAveugle`, `PolitiqueHasard`,
  `PolitiqueLLM(jeu="porte_fenetre")`, `PolitiqueLLM(jeu="labyrinthe")`.
- **Commande** :
  `python3 tools/tests/qualifier_porte_fenetre_drvm.py --endpoint http://127.0.0.1:18082 --sortie reports/pensee-porte-fenetre.json`.

## 3. Les résultats

| politique | but | nœuds | coût | appels | sonde | attendre | latence |
|---|---|---:|---:|---:|---:|---:|---:|
| **oracle (Manhattan)** | ❌ | 200 | 271,0 | 65 | 1 | 65 | 0,0 |
| aveugle | ❌ | 200 | 268,0 | 65 | 0 | 65 | 0,0 |
| hasard | ❌ | 200 | 312,0 | 61 | 12 | 61 | 0,0 |
| **LLM `porte_fenetre`** | ❌ | 200 | 396,0 | 53 | 35 | 54 | **97,3** |
| LLM `labyrinthe` | ❌ | 200 | 275,0 | 64 | 2 | 65 | 36,1 |

- **L'oracle échoue** : 200 nœuds, 1 sonde, 65 appels, sans but. **Aucune politique ne passe** :
  le problème n'est pas un test valide.
- **Le 7B échoue** (200/35/97,3 s) : il tente des `sonde` (35) et des `attendre` (54), mais
  n'atteint pas `(4,4)`.
- **Le labyrinthe** échoue (200/2) : sans l'horloge, il ne réessaie pas.

## 4. Les contrôles

- **Oracle** : ❌ — c'est le contrôle **décisif** : si l'oracle (le Manhattan, l'A*) ne passe pas,
  le problème est cassé (le `sonde_pw`/le `_libre_pw`/le `attendre`/le but).
- **Aveugle** : ❌ (200/0).
- **Hasard** : ❌ (200/12) — la chance ne suffit pas.
- **Labyrinthe** : ❌ (200/2).
- **Le 7B** : ❌ (200/35) — il ne peut pas réussir un problème que l'oracle ne réussit pas.

## 5. Ce qui pourrait rendre ce résultat faux

- **L'oracle échoue** : le problème (`LABYRINTHE_PORTE_FENETRE`/`REGISTRE_PW`) est **cassé**
  (le `sonde_pw`/le `_libre_pw`/l'`attendre`/le but). Ce n'est pas un résultat sur le 7B : c'est
  un **défaut du problème**, à réparer avant tout test.
- **Le 7B** (200/35/97,3 s) fait ce qu'il peut ; ses 54 `attendre` et 35 `sonde` montrent qu'il
  **suit** la règle, mais le problème ne mène pas au but.
- **La latence** (97,3 s) inclut la file du serveur ; 53 appels ; CPU seulement.
- **Le problème n'a pas de T** dans l'autotest (`t??_fenetre` absent) : il n'a jamais été validé.

## 6. La suite

1. **Réparer `LABYRINTHE_PORTE_FENETRE`** : le `_libre_pw`/le `sonde_pw`/l'`attendre`/le but ;
   l'oracle doit passer avant le 7B. C'est le prochain fait de la fenêtre.
2. **Le gold 200+** et la **pragmatique** (l'heuristique garde) : la ligne L.
3. **La fonction « la bonne réponse, pas le voisin »** (T132/T133, distracteurs r428–r432).
4. **La porte B13** : 140/140 (T132/T133 alignés 2/5).

## 7. Fichiers

- [`tools/tests/qualifier_porte_fenetre_drvm.py`](../tools/tests/qualifier_porte_fenetre_drvm.py) —
  le banc (oracle, aveugle, hasard, LLM).
- [`tools/pensee/operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueLLM(jeu="porte_fenetre")`,
  `LABYRINTHE_PORTE_FENETRE`, `REGISTRE_PW`.
- [`tools/tests/test_pensee_politique.py`](../tools/tests/test_pensee_politique.py) — 10 tests
  (le prompt fenêtre : `t % 3`, l'attente).
- [`pensee-porte-fenetre.json`](pensee-porte-fenetre.json) — les mesures, les seuils, les limites.


## 8. Contre-fiche (2026-11-02, round 36)

La conclusion « le problème est cassé » était **fausse**. Mesures :

| budget | BFS | A* | Greedy |
|---:|---|---|---|
| 200 | ❌ 44 états | ❌ 195 | ❌ 195 |
| 500 | ✅ **331 nœuds, 52 états** | ❌ 495 | ❌ 495 |
| 1 000 | ✅ 331, 52 | ❌ 995 | ❌ 995 |

- **Le BFS trouve `(4,4)`** en 331 nœuds : la carte, les opérateurs et `attendre` sont bons.
- L'**A\*/Greedy** échouent : `score_pw = 1/(1+Manhattan)` et `heuristique_pw = -Manhattan` les
  enferment dans `y ≤ 3` (les murs `(4,1)/(4,2)` bloquent la colonne 4).
- **Correctifs** : `_etat_pw` porte le `t` **réel** (18→44/195 états) ; `Moteur.boucle` sort sur
  `trouve` dans `for prop`. Le banc 7B doit être relancé avec **budget 500** et un guide BFS.


## 9. Store.push FIFO (round 42-43)

`Store.push` faisait `self.ouverts.setdefault(empreinte, len(self.ouverts))` : un nœud **re-poussé**
gardait son ancien numéro de file, donc la frontière du BFS **se figeait** sur les premiers
nœuds et le but n'était jamais atteint. Corrigé : un nœud absent prend `self._seq`, puis
`self._seq += 1` (vrai FIFO).

| budget | BFS avant | BFS après |
|---:|---|---|
| 200 | ❌ 44 états | ❌ 36 états |
| 500 | ❌ 44 états | ✅ **228 nœuds, 37 états** |

L'A* et le Greedy restent bloqués à 495 états : leur sélection par score n'est pas un BFS, et
le fitness Manhattan les égare — c'est un choix de stratégie, plus un bug de store.

**Le 7B reste à mesurer** sur la fenêtre avec l'oracle BFS corrigé (228 nœuds) : le banc 500
(`pensee-porte-fenetre-500.json`) donne le 7B ❌ (500/83/129 s) mais l'oracle ❌ aussi, donc il
doit être rejoué avec `Store.push` corrigé.


## 10. Test non discriminant (round 45-46)

Avec `Store.push` FIFO et l'oracle **BFS** (budget 500), **tout le monde passe** :

| politique | but | nœuds | sonde | attendre |
|---|---|---:|---:|---:|
| oracle (BFS) | ✅ | 228 | — | — |
| **aveugle** | ✅ | 215 | 11 | 49 |
| **hasard** | ✅ | 227 | 23 | 49 |
| **LLM `porte_fenetre`** | ✅ | 238 | 34 | 49 |
| LLM `labyrinthe` | ✅ | 234 | 30 | 49 |

- L'aveugle fait **mieux** que le 7B (215 vs 238) ; le labyrinthe (234) et le hasard (227) aussi.
- Le prompt `porte_fenetre` (t % 3, attends) **n'apporte rien** : la fenêtre, une fois `Store.push`
  réparé et le budget à 500, est un problème d'exploration que même l'aveugle résout.
- **Verdict** : la fenêtre n'est **pas discriminante** — comme la porte mobile et la porte qui bouge.
  Les tests qui discriminent restent : la **porte** (27 nœuds), la **minute** (26), la
  **stochastique** (5/5, labyrinthe 0/1).
