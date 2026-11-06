# B13 — R1/R2/R3 : exact 212/212 (1,0000), mais **+17 net** (24 gains, 7 régressions)

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
> **Commit** : `f908d7b0` · **État courant** · **Verdict** : ✅ chiffres, ⚠️ attribution corrigée
>
> **183/183 portes** : l'attachement est **juste 212/212 (1,0000)** sur les **212 labels** prédits
> (sur 239 cibles), **couverture 0,8870**, **F1 0,5763** (gelé 602 ; 0,5720 vivant), tête
> **0,7316** (gelé) ; **fr 129/129**, **en 83/83** ; **27 spans** restants.
>
> **Correction d'attribution (audit A19)** : la fiche annonçait « **+27 exacts, 0 perte** ». La
> mesure réelle du diff v7 → v8 est **24 gains bruts et 7 pertes, soit +17** (195 → 212). Les
> règles ne sont donc **pas** toutes gagnantes : R1a perd 6 REL françaises synthétiques, R1c
> perd `g017`, R2 perd `s037`. Le tableau ci-dessous donne les valeurs mesurées.

## 1. Les règles, mesurées (ablations A19)

| règle | gains | pertes | net |
|---|---:|---:|---:|
| **R1a** — `SUJETS` sans les relatifs (un pronom n'est plus un verbe) | +15 | −6 (r273, s069, s135, s032, s072, s115) | **+9** |
| **R1b** — modaux dans les auxiliaires | +1 (r247) | 0 | **+1** |
| **R1c** — second prédicat (AUX après prédicat, verbe après groupe verbal) | +4 (r224, r291, r115, r239) | −1 (g017) | **+3** |
| **R1** (faisceau) | 19 | 7 | **+13** |
| **R2** — SUB sans segment précédent | +4 (r215, r245, r279, r294) | −1 (s037) | **+3** |
| **R3a** — subordonnants par langue | 0 | 0 | **0** (inerte : ses membres sont déjà dans `RELATIFS`/`SUBORDONNANTS`) |
| **R3c** — `fall`/`call` | +2 (r102, r245) | 0 | **+2** |
| **total** | **24** | **7** | **+17** |

**Décomposition de 212** : 195 (v7) − 7 régressions + 23 des 26 gains de A17 + 1 (r102).

## 2. Avant / après

| mesure | v7 | **v8** |
|---|---:|---:|
| labels au bon span | 196 | **212** |
| **exact / labels** | 195/196 | **212/212 (1,0000)** |
| **couverture** | 0,8201 | **0,8870** |
| F1 syntagmes (gelé 602) | 0,5595 | **0,5763** |
| tête (gelé 602) | 0,7205 | **0,7316** |
| français (exact / labels) | 135/135 | **129/129** |
| anglais | 60/61 | **83/83** |
| **couverture française** | **0,894** | **0,854** (baisse) |
| spans perdus | 43 | **27** |
| top-k | 166 | **211** (après correctif du site d'appel) |

**Ce que ça dit** :

- **L'anglais gagne +23**, le français **recule** (135 → 129 exacts, couverture 0,894 → 0,854) :
  les 6 régressions sont des REL françaises synthétiques (« Paul qui marche marche », etc.).
- **Le 1,0/1,0 est exact/labels**, pas la couverture : ne pas le lire comme « l'attachement est
  résolu » (l'audit A19 le dit explicitement).
- **Les 27 spans restants** : **17 inatteignables** (12 synthétiques, 4 GP du gold sans
  préposition, 1 tokenisation) **+ 7 régressions** de ce round **+ 3 gains de A17 non intégrés**
  (`g017`, `r280`, `r153`).
- **R3a est inerte** : la fiche l'annonçait à +2 ; le code ne l'exerce pas (les subordonnants
  anglais sont déjà dans `SUBORDONNANTS`).
- **R3b** (garde déterminant dans le GP) n'est **pas** intégré : `r153` reste absent.

## 3. Contrôle négatif (mesuré, A19)

**Permutation globale des cibles** (2000 tirages) : **2,04/212** en moyenne (0,96 %) contre
**212/212** observé, p = 0. **Candidat aléatoire** : 35,9 % de top-1 (observé 100 %).
**Permutation des listes de candidats** : top-k 0,85 % (observé 83,5 %).

## 4. Ce que ce banc ne dit pas

- **Les 27 spans** : non prédits, donc hors mesure d'attachement.
- **Le test** : A17 a diagnostiqué sur dev **et** test ; le test n'est pas aveugle.
- **L'in-sample** : les règles sont dessinées sur ce gold.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 5. Ce qui pourrait rendre cette fiche fausse

- **les 6 régressions françaises** ne sont pas corrigées : le net est +17, pas +24 ;
- **R3a inerte** et **R3b absente** : les règles ne font pas ce que la fiche amont annonçait ;
- **le correctif `prec = s`** (top-k 211) est postérieur au commit `f908d7b0` ;
- un **audit** qui ne vérifie pas ces mesures (voir [audit R1/R3](rapport-audit-r1r3.md)).

## 6. La suite

1. **Corriger les 7 régressions** (les 6 REL françaises + `g017`) — c'est un net de +17 à
   défendre, ou +24 si elles sont réparées.
2. **R3b** (GP tronqué par un déterminant) et **R3a** (rendre la règle effective).
3. **Les 27 spans** : corriger le gold (ligne 98) et le lexique synthétique, ou les accepter.
4. **Politique DRVM/native** : quand les poids seront là.

## 7. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — R1, R2, R3a, R3c.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`rapport-spans-v7.md`](rapport-spans-v7.md) — le diagnostic A17.
- [`rapport-audit-r1r3.md`](rapport-audit-r1r3.md) — l'audit A19 (ablations).
- [`pensee-r1r3.json`](pensee-r1r3.json) — les chiffres.
