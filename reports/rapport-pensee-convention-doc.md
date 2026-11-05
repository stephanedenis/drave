# B13 — la convention des cibles est documentée dans le gold

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **177/177 portes** : le gold ne disait pas ce qu'était une `cible` ; la lecture des données
> (T169, T172) est désormais **écrite dans le gold** (`CONVENTION_CIBLE`) et vérifiée par une
> porte. REL/SUB → **antécédent** (tête du GN à gauche) ; GP → **verbe gouverneur**, ou **nom
> complété** pour un génitif ; GN/GV → nom ou verbe dont le segment dépend.
>
> **Dispositif** : [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-convention-doc.json`](pensee-convention-doc.json).

## 1. Ce qui est écrit

| type | convention de la cible |
|---|---|
| **REL** | antécédent (tête du GN à gauche) |
| **SUB** | antécédent (tête du GN à gauche) |
| **GP** | verbe gouverneur ; nom complété pour un génitif |
| **GN / GV** | nom ou verbe dont le segment dépend |

**Ce que ça dit** :

- **Deux conventions coexistent** dans le même champ : c'est mesuré (63 cibles verbes, 82 noms
  sur 145 segments) et maintenant **documenté**, au lieu d'être deviné.
- **La mesure les publie séparément** (`attachement.verbe` / `attachement.nom`) : le taux global
  n'est comparable qu'à convention constante.
- **La porte T174 empêche la dérive** : si quelqu'un retire la documentation ou change un type,
  elle tombe.
- **La négative est explicite** : documenter ne rend pas les 22 échecs justes ; cela rend la
  lecture honnête.

## 2. Ce que ce banc ne dit pas

- **La convention voulue** par l'auteur du gold reste une reconstruction : le texte décrit ce
  que les données font, pas une intention déclarée.
- **Les 22 échecs** (11 hors candidats, 11 mal classés) ne bougent pas.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 3. Ce qui pourrait rendre cette fiche fausse

- **la lecture** : d'autres entrées du gold pourraient suivre une troisième convention ;
- **le décompte** 63/82 dépend de `_est_verbe` ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Réduire les candidats à leur tête** (top-k strict 0,6069).
2. **Le classement appris** (11 mal classés).
3. **Les subordonnées** : demander à S (81 spans).
4. **Politique DRVM/native** : quand les poids seront là.

## 5. Fichiers

- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `CONVENTION_CIBLE`.
- [`autotest.py`](../tools/pensee/autotest.py) — T174, 177/177.
- [`pensee-convention-doc.json`](pensee-convention-doc.json) — la convention.
