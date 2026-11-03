# B13 — la porte minute : la règle l'ouvre (26 nœuds, 4 sonde, 6,4 s) ; le prompt labyrinthe échoue (200, 3, 101,6 s)

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 ·
> **Verdict** : ✅ **la porte minute s'ouvre avec la règle** — avec le prompt `porte` (la porte
> `(3,3)`, la sonde depuis `(3,2)` si tu réponds `bas`), le 7B atteint le but en **26 nœuds**,
> **4 sonde**, **7 appels**, **6,40 s** ; avec le prompt `labyrinthe` (sans la porte), il échoue à
> **200 nœuds**, **3 sonde**, **101,6 s**, sans but. L'**oracle** (Manhattan) fait 27 nœuds/5
> sonde ; l'**aveugle** échoue (200 nœuds, 61 sonde) ; le **hasard** ouvre par chance (43 nœuds,
> 7 sonde).
>
> **Dispositif** : [`qualifier_porte_minute_drvm.py`](../tools/tests/qualifier_porte_minute_drvm.py) ;
> [`operateurs.py`](../tools/pensee/operateurs.py) (`LABYRINTHE_PORTE_MINUTE`, `REGISTRE_PM`,
> `PolitiqueLLM(jeu="porte")`) ; JSON
> [`pensee-porte-minute.json`](pensee-porte-minute.json).

## 1. Ce qui était mesuré

La porte DRVM ([`pensee-porte-llm`](rapport-pensee-porte-llm.md)) était ouverte par la règle
(27 nœuds, 4 sonde) et pas sans (200 nœuds, 3 sonde). La **porte minute** est sa variante :
la sonde ouvre la porte `(3,3)` **un tour** et passe **dans le même pas** (`REGISTRE_PM`). La
question : la règle dans le prompt tient-elle sur cette variante, et le test **discrimine**-t-il
la règle ?

## 2. Le dispositif

- **Problème** : `LABYRINTHE_PORTE_MINUTE` — grille 5×5, murs `MURS_P`, porte `(3,3)`, but
  `(4,4)` ; opérateurs `pas` (symbolique), `saut` (numérique), `sonde` (neuronal, 5) : la sonde
  ouvre et passe dans le même pas si la politique vise la porte.
- **Prompt `porte`** : les murs, la porte `(3,3)`, « depuis `(3,2)`, la sonde ouvre la porte si
  tu réponds `bas` », l'état `open`, le but `(4,4)`.
- **Contrôle du prompt** : même modèle, même problème, le prompt `labyrinthe` (les murs, la
  position, le but ; **pas** la porte).
- **Politiques** : oracle `PolitiqueManhattan` (la porte T18), aveugle `PolitiqueAveugle`, hasard
  `PolitiqueHasard` (graine 0), LLM `PolitiqueLLM(jeu="porte")`, LLM `PolitiqueLLM(jeu="labyrinthe")`.
  `DRVM`, `AStar`, `Budget(200)`.
- **Commande** :
  `python3 tools/tests/qualifier_porte_minute_drvm.py --endpoint http://127.0.0.1:18082 --sortie reports/pensee-porte-minute.json`.

## 3. Les résultats

| politique | but | nœuds | coût | appels | sonde | latence |
|---|---|---:|---:|---:|---:|---:|
| **oracle** (Manhattan) | ✅ | 27 | 57,0 | 7 | 5 | 0,0 |
| **aveugle** | ❌ | 200 | 483,0 | 66 | 61 | 0,0 |
| **hasard** | ✅ | 43 | 85,0 | 14 | 7 | 0,0 |
| **LLM, prompt `porte`** | ✅ | **26** | **52,0** | **7** | **4** | **6,40** |
| **LLM, prompt `labyrinthe`** | ❌ | 200 | 265,0 | 95 | 3 | **101,6** |

- **La règle fait la différence** : 200 nœuds/sans but → **26 nœuds/but**, 4 sonde, 7 appels,
  6,40 s. Le LLM fait **un nœud de moins que l'oracle** (26 contre 27) et une sonde de moins
  (4 contre 5) ; le coût 52 contre 57. La différence de nœuds n'est pas une preuve de qualité
  (le tie-breaking de l'A*), mais le but et la sonde le sont.
- **Le prompt labyrinthe échoue** : 200 nœuds, 3 sonde, 101,6 s, sans but — le même modèle, le
  même problème, seule la description change. C'est le **contrôle négatif du prompt**.
- **Le hasard ouvre** la porte par chance (43 nœuds, 7 sonde) ; la porte est sur le chemin, donc
  le hasard peut la viser. L'**aveugle** échoue (200 nœuds, 61 sonde).
- **La latence** : 6,40 s pour 7 appels (~0,91 s/appel) ; le labyrinthe a payé 101,6 s pour
  95 appels (file du serveur).

## 4. Les contrôles

- **Prompt `porte` vs `labyrinthe`** (même modèle, mêmes poids, même problème) : but à 26 nœuds
  contre pas de but à 200. La description est la variable.
- **Aveugle** : 200 nœuds, 61 sonde, sans but.
- **Hasard** : but par chance (43 nœuds) ; il ne prouve pas la politique, il montre que la porte
  est sur le chemin.
- **Oracle** : but, 27 nœuds, 5 sonde — la référence.

## 5. Ce qui pourrait rendre ce résultat faux

- **La porte minute est une variante de la porte** : la sonde ouvre et passe dans le même pas ;
  le « mouvement » est petit, et la porte est sur le chemin de `(4,4)`. Le contrôle `labyrinthe`
  échoue quand même (200 nœuds, 3 sonde) : la règle compte.
- **Le hasard ouvre** (43 nœuds) : la porte seule n'est pas un contrôle de qualité ; c'est
  l'aveugle et le labyrinthe qui le sont.
- **Le nombre de nœuds** (26 vs 27) dépend du tie-breaking de l'A*, de l'ordre des opérateurs et
  de la politique ; ne pas lire comme un gain de qualité. Le but, la sonde et le coût sont les
  mesures.
- **La latence** inclut la file du serveur ; 6,4 s pour 7 appels est cohérent, 101,6 s pour 95
  appels l'est aussi (le labyrinthe explore 200 nœuds).
- **Une seule graine**, température 0, grammaire ; CPU seulement.
- **La porte B13** reste à 134/140 (4 S + 2 test périmé) ; la politique a des tests unitaires,
  pas un T dans la porte B13.

## 6. La suite

1. **La porte mobile** (`LABYRINTHE_PORTE_MOBILE_0/1`, deux positions `(3,3)` et `(1,3)`, dont
   une hors du chemin) : c'est le test qui discrimine la position de la porte.
2. **La porte stochastique** : la porte saute avec une probabilité ; la règle doit porter le
   risque.
3. **Le gold 200+ phrases** et la **pragmatique** (l'heuristique garde) : la ligne L.
4. **La porte B13** : les 4 attendus du S `647205a` et le test anaphorique T132/T133.

## 7. Fichiers

- [`tools/tests/qualifier_porte_minute_drvm.py`](../tools/tests/qualifier_porte_minute_drvm.py) —
  le banc (oracle, aveugle, hasard, LLM porte, LLM labyrinthe).
- [`tools/pensee/operateurs.py`](../tools/pensee/operateurs.py) — `LABYRINTHE_PORTE_MINUTE`,
  `REGISTRE_PM`, `PolitiqueLLM(jeu="porte")`.
- [`pensee-porte-minute.json`](pensee-porte-minute.json) — les mesures, les seuils, les limites.
