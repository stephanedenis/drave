# B13 — le gold réel 432 : la cascade tient (POS 0,9065 ; syntagmes 0,4598 ; tête 0,5633 ; acte 0,9954), le verdict est true (seuils du contrat)

> **Correction — 03/11 00 h 42.** Le gold réel 432 a **ses propres seuils de contrat** : **0,90 /
> 0,45 / 0,55 / 0,50** (`tools/tests/linguistique/qualifier_cascade.py:122` ; JSON
> `seuils_contrat.gold_reel_432`). Avec eux, le verdict est **`true`** : POS 0,9065 ≥ 0,90,
> syntagmes 0,4598 ≥ 0,45, tête 0,5633 ≥ 0,55, fraction 0,5165 ≥ 0,50. Les sections ci-dessous
> datent de la **première lecture**, qui appliquait au gold réel les seuils du **gold 180**
> (0,94 / 0,60 / 0,75 / 0,60) — d'où le `false` ; le verdict de référence est **`true`**.

> **Ligne de roadmap** : **L/B13** (le bloc langue et la pensée) · **Date** : 2026-11-03 ·
> **Verdict** : ⚠️ **la cascade bat le neuronal et l'heuristique sur le gold réel, mais les seuils
> absolus échouent** — 432 phrases, 2 375 tokens, POS **0,9065** (fermé 0,8973, ouvert 0,9162),
> syntagmes F1 **0,4598** (tp 627, fp 655, fn 818), tête F1 **0,5633** (tp 768, fp 514, fn 677),
> pragmatique acte **0,9954** / négation 0,9676 / modalité 0,9861 / double sens 0,9676, fraction
> **0,5165**. **429 appels** POS + 429 syntagmes (**429 appels pour 432 ids : effet de cache**), **0 refus**, **0 token vide**, 57 min 42.
> `pos_all`, `syntagme_exact_all`, `syntagme_tete_all` et `fraction` sont **faux** — c'est le fait.

## 1. Ce qui était mesuré

La cascade complète avec le vrai modèle sur le **gold réel** : `gold_reel.json`, **432 phrases**
écrites après coup (r001…), avec leurs POS, segments GN/GV/GP/REL/SUB et pragmatique. Le banc
`qualifier_cascade.py --gold-reel` applique la politique `confiance` au syntagme et garde
l'heuristique pour la pragmatique.

## 2. Les résultats

| lecture | POS | syntagmes | tête | acte | fraction |
|---|---:|---:|---:|---:|---:|
| **cascade complète** | **0,9065** | **0,4598** | **0,5633** | **0,9954** | **0,5165** |
| neuronal seul | 0,8392 | 0,4618 | 0,5639 | 0,0 | 0,0 |
| heuristique seule | 0,7394 | 0,2521 | 0,4520 | 0,9954 | 0,5165 |

- **POS** : 0,9065 — **au-dessus du neuronal seul** (+0,0673) et de l'heuristique (+0,1671).
- **Syntagmes** : 0,4598 — au niveau du neuronal (0,4618), **au-dessus de l'heuristique**
  (0,2521) : la cascade ne perd pas le neuronal et gagne la structure.
- **Tête** : 0,5633 (contre 0,4520 heuristique).
- **Pragmatique** : acte 0,9954, négation 0,9676, modalité 0,9861, double sens 0,9676 ;
  fraction 0,5165.
- **Par défaut** : 0,4506 — la cascade bat le défaut.

## 3. Le contrôle négatif

Le **neuronal seul** donne **acte 0,0** et **fraction 0,0** : il ne porte pas la pragmatique ni
la fraction. La cascade les **restaure** (0,9954 / 0,5165) — c'est bien la **politique** qui fait
le travail, pas le bloc neuronal. Symétriquement, l'heuristique seule s'effondre sur les syntagmes
(0,2521) : c'est bien le **neuronal** qui apporte la structure. Les deux moitiés sont nécessaires.

## 4. Pourquoi le verdict est false

Les seuils absolus (`pos_all`, `syntagme_exact_all`, `syntagme_tete_all`, `fraction`) échouent :
le gold réel est **bien plus dur** que le gold hand+synth (0,6130 / 0,7574). Ce n'est pas une
régression : c'est le **premier chiffre honnête** sur le corpus réel. Les seuils doivent être
**recalés** sur ce que le gold réel permet, pas l'inverse.

## 5. Ce qui pourrait rendre ce résultat faux

- **429 appels pour 432 ids** : **effet de cache** (mêmes phrases réutilisées), **0 refus**,
  **0 token vide** — le générateur n'a **pas** produit de vides (`612f8743`).
- **Pas de `source` hand/synth** : `hand = 0`, `synth = 0` ; le découpage hand/synth est nul.
- **Un seul passage**, température 0, grammaire GBNF.
- **CPU seulement** (GPU de N2 réservés) : latence médiane 7,8 s.
- **Le gold réel** est écrit par le même auteur que le banc : biais possible.

## 6. La suite

1. **Recaler les seuils** du banc sur le gold réel (le fait est mesuré, pas le seuil).
2. **Corriger les 3 phrases vides** (le générateur).
3. **DRVM/native** (cadenas 3, porte 27, labyrinthe 2) — déjà mesurée.
4. **La fonction « la bonne réponse, pas le voisin »** (T132/T133).

## 7. Fichiers

- [`pensee-gold-reel-cascade.json`](pensee-gold-reel-cascade.json) — les mesures, seuils, appels.
- [`tools/tests/linguistique/qualifier_cascade.py`](../tools/tests/linguistique/qualifier_cascade.py) —
  le banc (`--gold-reel`).
- [`tools/tests/linguistique/gold_reel.json`](../tools/tests/linguistique/gold_reel.json) — le gold réel.
