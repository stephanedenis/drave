# B13 — la partition des syntagmes : les alternatives sont étiquetées, les mesures ne bougent pas

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (produit) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Le P0-3 est fermé sans perte** : les **239 paires** de chevauchement des deux audits sont
> **toutes** des paires S × chunker (53,1 % de S qui contient le chunker, 33,5 % l'inverse,
> 2,5 % de mêmes bornes, 10,9 % de croisements). Le mode **`alternative`** (défaut) garde les deux
> segments et écrit **`meta.alternative`** (le préféré, la relation, `retire`) : **F1 0,6482,
> exact 235/236, POS 85,00 %** — les mesures de la base, **sans déduplication silencieuse**. Le mode
> **`filtrer`** (option) donne une vue linéaire : **F1 0,6954 (+0,047)** mais **217/218** (18
> attachements en moins), les S retirés restant dans `meta.alternative`.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`partition=`,
> `_expliciter_partition`, `meta.alternative`) ; fiche A29
> [`rapport-partition-syntagmes.md`](rapport-partition-syntagmes.md) ; JSON
> [`pensee-partition-integrees.json`](pensee-partition-integrees.json).

## 1. Les quatre modes

| mode | paires | F1 | exact | coût JSON |
|---|---:|---:|---:|---:|
| **`alternative`** (défaut) | 239 | **0,6482** | **235/236** | +10,4 % |
| `filtrer_union` | 91 | 0,6163 | 217/239 → 217/218 | +7,2 % |
| `filtrer` (partition stricte) | **0** | **0,6954** | 217/218 | +2,0 % |
| `brut` (avant) | 239 | 0,6482 | 235/236 | — |

**Ce que ça dit** :

- **L'alternative étiquetée ne perd rien** : elle documente le chevauchement (le client choisit) au
  lieu de le cacher.
- **La partition stricte gagne 0,047 de F1** mais perd **18 attachements** : c'est le compromis à
  exposer, pas à imposer.
- **La déduplication silencieuse** (l'ancien comportement de la fusion) perdait 14 attachements
  sans trace : elle est remplacée.

## 2. Ce que le client reçoit

`meta.alternative` = `{"prefere": <bool>, "relation": "inclut|inclus|meme_span|croise",
"retire": <bool>}`. Le rang 1 reste le **chunker le plus large** (179/207 groupes avec un span du
gold, 86,5 %).

## 2 bis. Le strip de la fusion

La fusion **déduplique** les segments ; les `meta.alternative` de l'heuristique pouvaient donc
pointer vers des segments **absents**. Un **strip** retire ces clés de la copie fusionnée : plus
de référence morte dans les compositions (mesures inchangées : 0,85 / 0,6482 / 235-236).

## 3. Contrôles (A29)

**Reproduction des deux audits** (107 + 132 paires), **chunker seul** (0 chevauchement),
**S sans union**, **filtre inverse**, **hasard même nombre** (placebo). Le mode `alternative` est
**strictement** celui de la base : POS, F1 et attachement identiques.

## 4. Ce que ce banc ne dit pas

- **Le gold ne tranche pas** : il ne dit pas quel segment d'une paire est « le bon ».
- **La partition stricte** n'est pas le défaut : elle perd des attachments.
- **Le coût JSON** (+10,4 %) n'est pas mesuré côté client.

## 5. Ce qui pourrait rendre cette fiche fausse

- **`meta.alternative`** est un schéma nouveau : il n'est pas dans le schéma v1 publié ;
- **la relation** dépend de la définition du chevauchement (strict) ;
- **le rang 1** est une heuristique (le chunker le plus large).

## 6. La suite

1. **Publier `meta.alternative`** dans le schéma v1 (version 2 ?).
2. **Trancher le défaut produit** : `alternative` (fidèle) ou `filtrer` (linéaire).
3. **Mesurer** le coût JSON côté client.

## 7. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — les quatre modes.
- [`rapport-partition-syntagmes.md`](rapport-partition-syntagmes.md) — la fiche A29.
- [`pensee-partition-integrees.json`](pensee-partition-integrees.json).
