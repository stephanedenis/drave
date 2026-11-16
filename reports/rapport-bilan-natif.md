# Le bilan du 16/11 — le natif : le diagnostic est tranché

> **La question du jour.** « Que manque-t-il pour que le modèle Drave natif soit exploitable ? »
> **La réponse, mesurée.** Il **modélise** (PPL 2,40) et **ne compose pas** (le banc : la
> répétition 15 en greedy, 0,87 de mots valides) ; **l'échelle achète le vocabulaire** (0,247 →
> 0,494 → 0,870 sur trois tailles) **pas la composition** (la répétition monte 1 → 6 → 15) ; le
> **tokenizer** n'est pas le levier (les R13 : +0,4 % en français à l'échelle) ; il reste
> **l'échelle, la donnée, l'alignement et le runtime**.

## 1. Les sept livrables

| # | livrable | ce qu'il dit |
|---|---|---|
| 1 | [`banc-generation.json`](banc-generation.json) + [la fiche](rapport-banc-generation.md) | 20 prompts × 3 réglages : 0,87 de mots valides, répétition 15, 36 octets/s ; le contrôle aléatoire 0,336 |
| 2 | [`banc-grammaticalite.json`](banc-grammaticalite.json) + [le banc](../tools/banc_grammaticalite.py) | notre analyseur juge le modèle : GV 6,9 contre 2,3, mais ciment 0,335 contre 0,791 |
| 3 | [`banc-generation-11m/21m.json`](banc-generation-21m.json) | l'échelle : les mots valides 0,247 → 0,494 → **0,870** ; la répétition 1 → 6 → **15** |
| 4 | [`rapport-natif-exploitable.md`](rapport-natif-exploitable.md) | la synthèse : les 4 leviers chiffrés, les 4 paliers, le coût |
| 5 | [`drave generer`](../tools/drave.py) | le modèle accessible (torch + checkpoint, JSON), les refus propres (code 4), le caveat |
| 6 | [`fiche-modele-natif.md`](fiche-modele-natif.md) | la carte du modèle : identité, données, mesures, limites, usage prévu, licence |
| 7 | [`natif-plan.md`](../docs/pilotage/natif-plan.md) | le plan : 4 paliers, les critères falsifiables, les risques |
| 8 | [`rapport-natif-numpy.md`](rapport-natif-numpy.md) + [`drvm_infere.py`](../tools/drvm_infere.py) | **le natif sans torch** : le DRVM en numpy, **4/4 de parité** avec torch, ~0,6 s/octet |
| 9 | [`rapport-native-reproductibilite.md`](rapport-native-reproductibilite.md) | **le 2,40 annoncé n'est pas reproductible** (17,3 à 22,6 sur le val actuel, 18,55 sur le gold) : le corpus n'est pas épinglé |
| 10 | [`banc-grammaticalite-echelle.json`](banc-grammaticalite-echelle.json) | la syntaxe à l'échelle : GV **1,90 → 2,65 → 6,90**, ciment **0,137 → 0,278 → 0,335** |

## 2. La conclusion

Le natif est un **prototype de recherche complet** : l'entraînement, la génération, le service, le
DRVM, la distillation, le SFT — tout existe et tourne. **Ce qui manque n'est pas la plomberie,
c'est la qualité** : un 34 M qui a mémorisé les mots et les boucles du corpus.

**Le pas suivant** (le palier 1) : un **100–150 M sur 3–6 Go propres**, avec **le banc dès le
premier checkpoint** et un critère falsifiable — **50 octets cohérents, la répétition ≤ 3**. La
donnée est le vrai goulot (1 Go aujourd'hui, 3–6 Go nécessaires), et son territoire est **D** : je
ne l'ai pas touchée.

## 2 bis. La passe complète

La **passe du 16/11 (12 h 26 → 14 h 48)** : **86 portes, 82 vertes, 2 rouges structurelles**
(`porte-indice`, `porte-melange`) + `porte-bloc-code` **transitoire** (×2,40 pour ×4 pendant la
passe, **verte en isolation**) + `porte-sessions` (le mandat, rafraîchi). Journal :
`work/portes/passe-1611n/`.

## 3. Ce que ce bilan ne dit pas

- Il ne promet pas de date : le palier 1 dépend du temps CPU et de la collecte des données.
- Il ne juge pas la **valeur** du natif : un modèle qui modélise a des usages (le scoring, les
  représentations) qui ne demandent pas la génération.
- Il ne dit pas que l'échelle suffira : la répétition doit être traitée (les données dédupliquées,
  la régularisation) — le palier 1 le testera.

## 4. Les fichiers

- Les bancs : `tools/banc_generation.py`, `tools/banc_grammaticalite.py`.
- Les JSON : `reports/banc-generation*.json`, `reports/banc-grammaticalite.json`.
- Les fiches : `rapport-banc-generation.md`, `rapport-natif-exploitable.md`, `fiche-modele-natif.md`.
- Le plan : `docs/pilotage/natif-plan.md`.
- La CLI : `python3 tools/drave.py generer --prompt "…" --n 64` (torch requis).
