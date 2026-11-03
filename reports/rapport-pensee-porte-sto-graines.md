# B13 — la porte stochastique, cinq graines : le 7B passe 5/5 (28–34 nœuds, 5–7 sonde) ; le labyrinthe 0/1, l'aveugle 0/1

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 ·
> **Verdict** : ✅ **le 7B passe 5/5 sur les cinq graines** — le tirage `random.random() < 0,8`
> de la porte stochastique est **fixé** (`random.seed(0..4)`) : le prompt `porte_sto`
> (80 %, réessaie) atteint le but aux **cinq** graines, en **28–34 nœuds**, **5–7 sonde**,
> 7–9 appels ; le **labyrinthe** (sans la règle) échoue (200 nœuds, 3 sonde) ; l'**aveugle**
> échoue (200/61) ; l'**oracle** passe (31/6). Le 5/5 est **reproductible**.
>
> **Dispositif** : [`qualifier_porte_sto_graines.py`](../tools/tests/qualifier_porte_sto_graines.py) ;
> [`operateurs.py`](../tools/pensee/operateurs.py) (`LABYRINTHE_PORTE_STO`, `REGISTRE_PSTO`,
> `PolitiqueLLM(jeu="porte_sto")`) ; JSON
> [`pensee-porte-sto-graines.json`](pensee-porte-sto-graines.json).

## 1. Ce qui était mesuré

La porte stochastique (80 %) est le premier test de porte qui **discrimine** la politique
(31/6 contre 200/3 pour le labyrinthe). Mais une seule exécution ne dit pas si le 7B passe
**5/5** : le tirage `random.random()` n'était pas fixé. Ici on rejoue `LABYRINTHE_PORTE_STO`
avec `random.seed(0..4)` et on mesure le LLM et les contrôles.

## 2. Le dispositif

- **Problème** : `LABYRINTHE_PORTE_STO` (`REGISTRE_PSTO`), but `(4,4)`, budget 200, A*.
- **Prompt** : `porte_sto` (les murs, la porte `(3,3)`, « depuis `(3,2)`, la sonde l'ouvre si tu
  réponds `bas`, **80 %** de chance, **réessaie** »).
- **Graines** : `random.seed(0)`, `1`, `2`, `3`, `4` avant chaque run.
- **Contrôles** : le `labyrinthe` (sans la règle), l'`aveugle`, l'`oracle` (Manhattan).
- **Commande** :
  `python3 tools/tests/qualifier_porte_sto_graines.py --endpoint http://127.0.0.1:18082 --sortie reports/pensee-porte-sto-graines.json`.

## 3. Les résultats

| graine | politique | but | nœuds | sonde | appels | latence |
|---:|---|---|---:|---:|---:|---:|
| 0 | LLM `porte_sto` | ✅ | 31 | 6 | 8 | 13,1 |
| 1 | LLM `porte_sto` | ✅ | 28 | 5 | 7 | 25,9 |
| 2 | LLM `porte_sto` | ✅ | 34 | 7 | 9 | 39,4 |
| 3 | LLM `porte_sto` | ✅ | 28 | 5 | 7 | 52,1 |
| 4 | LLM `porte_sto` | ✅ | 28 | 5 | 7 | 64,9 |
| 0 | LLM `labyrinthe` | ❌ | 200 | 3 | — | 182,7 |
| 0 | aveugle | ❌ | 200 | 61 | — | 0 |
| 0 | oracle | ✅ | 31 | 6 | — | 0 |

- **5/5** : le 7B atteint le but aux cinq graines (28–34 nœuds, 5–7 sonde). Le 80 % (le
  réessai) tient ; le 5/5 est **reproductible** (les graines sont fixées).
- **Les contrôles échouent** : le labyrinthe (200/3) et l'aveugle (200/61) ; l'oracle passe
  (31/6). Le test **discrimine**.
- **Les latences** (13,1 → 64,9 s) sont **cumulatives** (le champ `latence` du `PolitiqueLLM`
  s'accumule) : par run, ~13 s ; la dernière inclut les quatre précédentes.

## 4. Les contrôles

- **Labyrinthe** : ❌ (200/3) — sans la règle, le modèle ne réessaie pas.
- **Aveugle** : ❌ (200/61) — le `droite` ne vise pas la porte.
- **Oracle** : ✅ (31/6).
- **Le hasard** n'est pas rejoué (la chance de la porte 80 % est la limite nommée de la fiche
  `pensee-porte-sto`).

## 5. Ce qui pourrait rendre ce résultat faux

- **Les graines** sont fixées (0–4) : le 5/5 est reproductible, mais ce n'est pas un échantillon
  aléatoire ; le hasard (la porte 80 %) reste la limite.
- **Une seule exécution par graine** ; la latence cumulative n'est pas une latence par run.
- **Le labyrinthe et l'aveugle** sont mesurés sur la graine 0 seulement ; leur échec est net
  (200 nœuds) et déjà mesuré à la graine 0 dans la fiche `pensee-porte-sto`.
- **La porte est sur le chemin** ; l'aveugle/labyrinthe échouent quand même : la règle compte.
- **CPU seulement**, température 0, grammaire ; le 7B peut passer par chance une graine.

## 6. La suite

1. **La fenêtre temporelle** (`LABYRINTHE_PORTE_FENETRE`, `attendre`, `t % 3 == 0`) : la porte
   n'est libre qu'à l'heure ; le prompt doit porter l'horloge.
2. **Le gold 200+** et la **pragmatique** (l'heuristique garde) : la ligne L.
3. **La fonction « la bonne réponse, pas le voisin »** (T132/T133, distracteurs r428–r432).
4. **La porte B13** : les 140/140 tiennent (T132/T133 alignés 2/5).

## 7. Fichiers

- [`tools/tests/qualifier_porte_sto_graines.py`](../tools/tests/qualifier_porte_sto_graines.py) —
  le banc (5 graines, contrôles).
- [`tools/pensee/operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueLLM(jeu="porte_sto")`,
  `LABYRINTHE_PORTE_STO`, `REGISTRE_PSTO`.
- [`pensee-porte-sto-graines.json`](pensee-porte-sto-graines.json) — les cinq graines, les
  contrôles, les seuils.
