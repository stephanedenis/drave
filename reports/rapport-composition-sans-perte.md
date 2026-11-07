# B13 — les compositions ne perdent plus : cascade = heuristique (0,8383, 235/236)

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ;
> l'état courant du bloc est dans [`en-cours`](../docs/pilotage/en-cours.md) (POS 86,25 %,
> F1 0,7535, attachement 236/237, couverture 0,9916, 2 spans).

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Le défaut de composition** (audit A26 : « la fusion dégrade le POS de 1,16 pt et perd 14 spans
> d'attachement ») est **fermé** : `Parallele` et `Cascade` rendent désormais **exactement** les
> mesures de l'heuristique — **POS 0,8383**, **F1 0,6474**, **attachement 235/236** — au lieu de
> **0,7465 / 0,6848 / 215/216**. Le verdict `cascade_pos` redevient une **comparaison** (et passe) ;
> le plancher 0,70 est retiré.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`MockNeuronal`,
> `_supprimer_chevauchements`, confiances 0,85), [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py)
> (verdict), [`autotest.py`](../tools/pensee/autotest.py) (4 assertions) ; JSON
> [`pensee-composition-sans-perte.json`](pensee-composition-sans-perte.json).

## 1. Les trois causes, dans l'ordre

| # | cause | correctif |
|---|---|---|
| 1 | le `MockNeuronal` ne rendait que `NOUN/VERB/ADJ/ADV/MOT` — les classes fermées manquaient | il rend **toutes** les classes (`meta.ouvert` selon `POS_FERME`) |
| 2 | les règles de contexte (3 bis, 3 a, 3 b) laissaient la confiance à 0,30/0,50 : le stub (0,82) gagnait la fusion | confiance **0,85** pour les étiquettes issues d'une règle de contexte |
| 3 | la fusion **dédupliquait** l'union heuristique (deux REL qui se chevauchent → une seule) | la segmentation heuristique est **autoritaire** : on ne la filtre pas, on n'ajoute que le non-chevauchement |

## 2. Avant / après

| mesure | heuristique | parallèle avant | **parallèle après** |
|---|---:|---:|---:|
| POS | 0,8383 | 0,7465 | **0,8383** |
| F1 syntagmes | 0,6474 | 0,6848 | **0,6474** |
| exact / labels | 235/236 | 215/216 | **235/236** |

**Le F1 de la composition baisse de 0,6848 à 0,6474 en apparence** : c'est parce qu'elle garde
maintenant les **deux** REL de l'union (dont le doublon de S), comme l'heuristique — la mesure est
la même que celle de l'heuristique, ce qui est l'objectif.

## 3. Contrôles

- **4 assertions** d'autotest recalées, **183/183**.
- **T138** : « défaut : confiance 0,8383, niveau 0,7465 » — la fusion par **niveau** (avec le stub)
  reste en dessous ; c'est le comportement du **stub**, pas de la composition.
- **Le verdict `cascade_pos`** redevient `cascade >= heuristique` : vrai.

## 4. Ce que ce banc ne dit pas

- **Le niveau** : la fusion par niveau avec le stub reste à 0,7465 (T138) — un vrai neuronal la
  dépasse (0,9389 documenté).
- **Le doublon REL** : la composition le garde comme l'heuristique ; le filtrer est une décision
  produit (la déduplication coûte 20 spans d'attachement).
- **Le `MockNeuronal`** reste un stub : il ne prouve pas la qualité neuronale.

## 5. Ce qui pourrait rendre cette fiche fausse

- **la confiance 0,85** est un choix : une vraie calibration la remplacerait ;
- **l'autorité heuristique** sur la segmentation est une politique, pas une loi ;
- **le niveau** : la priorité par niveau reste active avec une clé DeepSeek.

## 6. La suite

1. **Calibrer les confiances** (0,85 est arbitraire).
2. **Trancher le doublon** REL (produit : l'expliciter, pas le dédupliquer).
3. **Le niveau** : mesurer avec un vrai neuronal.

## 7. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — mock, fusion, confiances.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — le verdict.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`pensee-composition-sans-perte.json`](pensee-composition-sans-perte.json).
