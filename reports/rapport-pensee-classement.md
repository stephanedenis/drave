# B13 — le classement : l'exact passe de 0,2260 à 0,6438 — et le gold mélange deux conventions

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **171/171 portes** : la cible de S était souvent un **GN entier** (« Le garçon », « Les enfants
> jouent ») ; elle est désormais **réduite à sa tête** (le verbe plein du texte de la cible s'il y
> en a un, sinon son dernier mot). Sur les 146 segments au bon span : **exact 33 → 94**
> (0,2260 → **0,6438**). Mais le contrôle révèle que le gold **mélange deux conventions** :
> **51 cibles verbes**, **95 cibles noms** (antécédents de REL, têtes de GP).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-classement.json`](pensee-classement.json).

## 1. Avant / après (146 segments au bon span)

| mesure | avant | **cible réduite à sa tête** | écart |
|---|---:|---:|---:|
| top1 | 115 (0,7877) | 114 (0,7808) | −1 |
| top-k | 132 (0,9041) | 132 (0,9041) | 0 |
| **exact** | **33 (0,2260)** | **94 (0,6438)** | **+61 (×2,8)** |
| tête top1 / top-k | 114 / 131 | 113 / 131 | −1 / 0 |

Rendement global (÷ 239 cibles) : top1 0,4770, top-k 0,5523, exact **0,3933**.

## 2. Le contrôle qui change la lecture : deux conventions dans le gold

| type | cibles **verbe** | cibles **nom/autre** | justes (verbe / nom) |
|---|---:|---:|---:|
| GP | 36 | 48 | 25 / 20 |
| REL | 0 | 26 | — / 22 |
| SUB | 15 | 21 | 12 / 15 |
| **tout** | **51** | **95** | **37 / 57** |

**Ce que ça dit** :

- **Le gain est réel** (33 → 94) : la réduction à la tête répare 61 cas que la cible S entière
  ratait.
- **Mais la métrique n'est pas homogène** : pour un **GP**, la cible est tantôt le **verbe**
  (`joue`), tantôt un **nom** (`frère`, `hier`) ; pour un **REL**, c'est l'**antécédent**
  (`livre`, `film`), jamais un verbe.
- **Le 0,6438 n'est donc pas « 94 % d'attachement juste »** : c'est 94 accords avec un gold à
  deux conventions. La fiche le dit au lieu de le cacher.
- **La prochaine mesure devra trancher la convention** : ou le gold est homogénéisé (verbe pour
  les compléments, antécédent pour les relatifs), ou la mesure est scindée par type.

## 3. Ce que ce banc ne dit pas

- **Les 52 échecs** : non qualifiés (verbe hors lexique, cible non verbale, GV multiple).
- **La convention voulue** : elle n'est pas documentée dans le gold.
- **Le top-k est lenient** (sous-chaînes) : 0,9041 n'est pas 90 % d'exact.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 4. Ce qui pourrait rendre cette fiche fausse

- **la réduction à la tête** dépend du lexique verbal et du dernier mot ;
- **`texte.find(brute)`** prend la première occurrence (ambigu si le texte se répète) ;
- **le gold** : 612 phrases, deux conventions mêlées ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 5. La suite

1. **Homogénéiser la convention des cibles** (verbe vs nom) — la vraie mesure.
2. **Les 52 échecs** : les qualifier.
3. **Le top-k strict** : l'égalité exacte dans les candidats, pas la sous-chaîne.
4. **Politique DRVM/native** : quand les poids seront là.

## 6. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — cible réduite à sa tête.
- [`autotest.py`](../tools/pensee/autotest.py) — T168, 171/171.
- [`pensee-classement.json`](pensee-classement.json) — avant/après et conventions.
