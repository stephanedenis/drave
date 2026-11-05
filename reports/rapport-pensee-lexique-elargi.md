# B13 — le lexique élargi : l'exact passe de 0,8082 à 0,8483

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **174/174 portes** : `vu`, `couru`, `accroché` n'étaient **pas** reconnus comme verbes — le
> bloc prenait l'auxiliaire (`a`) pour la cible. Le lexique verbal reçoit les **participes
> irréguliers** et une trentaine de verbes courants. Sur les 146 segments au bon span (avant) et 145 après :
> **exact 118 → 123** (0,8082 → **0,8483**), top1 0,8690, top-k **0,9241**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`VERBES_CONNUS`),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-lexique-elargi.json`](pensee-lexique-elargi.json).

## 1. Avant / après (145 segments au bon span)

| mesure | avant (146) | **lexique élargi** (145) | écart |
|---|---:|---:|---:|
| top1 | 122 (0,8356) | **126 (0,8690)** | +4 (sur 146 → 145) |
| top-k | 132 (0,9041) | **134 (0,9241)** | +2 |
| **exact** | **118 (0,8082)** | **123 (0,8483)** | **+5** |
| verbes | 48/51 | **60/63** (0,9524) | +12 |
| noms | 70/95 | **63/82** (0,7683) | −7 |

Rendement global (÷ 239 cibles) : top1 0,5272, top-k 0,5607, exact **0,5146**.

**Ce que ça dit** :

- **Les participes irréguliers manquaient** : « vu » n'était pas un verbe pour `_est_verbe`, donc
  « a vu » donnait `a` ; le lexique les reconnaît maintenant.
- **Attention à la lecture des conventions** : la part « verbes » passe de 51 à **63** cibles et
  la part « noms » de 95 à **82** — non parce que le gold a changé, mais parce que la
  **classification** `_est_verbe` reconnaît plus de cibles comme verbes. Les deux colonnes ne
  sont donc pas comparables d'une fiche à l'autre ; seul l'**exact global** l'est (+5 : 118 → 123).
- **Les noms baissent en apparence** (0,7368 → 0,7683 en taux, mais 70 → 63 en nombre) : le
  déplacement vient de la reclassification.
- **La négative est explicite** : 22/145 restent faux.

> **Note du 2026-11-05 (attachement v2)** : cette fiche décrit l'état **avant** la vague de
> sous-agents ; l'attachement v2 donne **exact 137/145 (0,9448)** et **top-k strict 0,9724**.
> Voir [attachement v2](rapport-pensee-attachement-v2.md).

## 2. Ce que ce banc ne dit pas

- **Les 22 échecs** : verbes hors lexique (`fly`, `climbs`, `flows`, `wait`, `swims`, `passes`,
  `get`, `smiles`) et noms cibles hors du GN à gauche.
- **La couverture du lexique** n'est pas mesurée hors gold.
- **Le top-k est lenient** (sous-chaînes).
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 3. Ce qui pourrait rendre cette fiche fausse

- **le lexique est écrit à la main** : les verbes ajoutés ne sont pas les cibles du gold (liste
  générale), mais un recoupement est possible ;
- **`_est_verbe` sert aussi à classer** les cibles : la répartition verbes/noms dépend de lui ;
- **le gold** : 612 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Les 22 échecs** : les qualifier (verbes hors lexique, noms cibles).
2. **Documenter la convention** dans le gold.
3. **Les subordonnées** : demander à S (81 spans).
4. **Politique DRVM/native** : quand les poids seront là.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `VERBES_CONNUS` élargi.
- [`autotest.py`](../tools/pensee/autotest.py) — T171, 174/174.
- [`pensee-lexique-elargi.json`](pensee-lexique-elargi.json) — avant/après.
