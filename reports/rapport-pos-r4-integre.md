# B13 — le paquet POS sûr : classes fermées anglaises + R4-en, POS 84,96 %

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Deux leviers mesurés et intégrés** (fiche A27 : [`rapport-pos-r4.md`](rapport-pos-r4.md)) :
> la complétion des **classes fermées anglaises** (`where`, `whose`, `mine` PRON ; `as` CONJ ;
> `am` AUX ; `late`, `out`, `maybe`, `hard`, `far`, `again`, `now`, `down`, `outside` ADV ;
> `outside` retiré de PREP) et **R4-en** (après une copule, un mot inconnu est un ADJECTIF
> attribut). Résultat : **POS 0,8383 → 0,8496** (+1,13 pt), **0 cassé**, **F1 et attachement
> inchangés** (0,6474 ; 235/236).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`POS_FERME["en"]`,
> boucle 3 c), [`autotest.py`](../tools/pensee/autotest.py) (8 assertions) ; JSON
> [`pensee-pos-r4-integration.json`](pensee-pos-r4-integration.json).

## 1. Le paquet

| levier | effet mesuré (A27) | intégré |
|---|---|---|
| **classes fermées** | +0,78 dev / +0,81 test, 25 corrigés / 0 cassé | ✅ |
| **R4-en** (copule → ADJ) | +0,41 dev / +0,31 test, 12 corrigés / 0 cassé | ✅ |
| **R4 bilingue** (max) | +1,51/+1,51 mais 11 faux→faux et 6 faux positifs libres | ❌ rejeté |

## 2. Avant / après

| mesure | avant | **après** |
|---|---:|---:|
| POS (tout) | 0,8383 | **0,8496** |
| POS dev / test | 0,8375 / 0,8400 | **0,8490 / 0,8511** |
| POS fermé / ouvert | 0,9133 / 0,7673 | **0,9295 / 0,7746** |
| F1 syntagmes | 0,6474 | 0,6474 (inchangé) |
| attachement | 235/236 | **235/236** (inchangé) |

**Ce que ça dit** :

- **Les classes fermées manquaient** : 25 tokens anglais (`where`, `late`, `out`, `as`…) étaient
  mal tagués faute d'entrées ; l'ajout ne touche pas les autres niveaux.
- **R4-en est sûr** en anglais (le français est laissé de côté : 5 faux positifs libres sur 8
  changements).
- **L'attachement ne bouge pas** : ces tags ne changent pas les frontières des segments.

## 2 bis. Ce que R4 **ne** fait pas — les pertes (A27, § 9)

- **17 faux→faux** sur le gold (dont 9 français) : des tokens déjà faux qui le restent.
- Sur les **50 textes libres**, **5 des 8 changements français sont faux** (`arrivés`, `parfois`,
  `reportée`, `entrés`, `acceptés`) contre 3 justes (`gratuite`, `cohérent`, `ouverte`) — c'est
  pourquoi **R4-fr n'est pas intégré**.
- Les **noms nus** (`He is doctor`, `She is president`) et les **participes irréguliers** (`born`,
  `hung`) deviennent ADJ.
- **Classes fermées** : 1 faux positif libre (`Where` interrogatif) ; `where`, `as`, `late`,
  `outside`, `hard`, `down`, `fast` sont **ambigus** (la liste choisit la majorité du gold) ;
  `when` en PRON vaut −3.

## 3. Contrôles (A27)

**Placebo** (mêmes actions, jetons aléatoires) : −0,25 à −0,44 pt — les règles gagnent par le
contexte, pas par hasard. **37 corrigés / 0 cassé** sur dev+test.

## 4. Ce que ce banc ne dit pas

- **Le test** (347 tokens anglais) : petit.
- **R4 bilingue** : rejeté (faux positifs) ; le français attend une règle plus sûre.
- **Les 50 textes libres** : 1 faux positif (`where`) signalé par A27.

## 5. Ce qui pourrait rendre cette fiche fausse

- **`outside` retiré de PREP** : « outside the house » se trompe désormais ;
- **la copule** : une liste de formes ;
- **les 25 corrections** sont concentrées sur l'anglais.

## 6. La suite

1. **R4 français** avec une condition plus stricte (pas de faux positifs).
2. **Les faux→faux** (8 pour R4-en) : des tokens déjà faux qui le restent.
3. **Trancher** `outside` (PREP ou ADV selon le contexte).

## 7. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — les deux leviers.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`rapport-pos-r4.md`](rapport-pos-r4.md) — la fiche A27.
- [`pensee-pos-r4-integration.json`](pensee-pos-r4-integration.json).
