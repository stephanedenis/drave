# R06 v6 — la cascade à confiance est publiée : deux fichiers, un seuil, une recette

> **Ligne de roadmap** : R06 (relecture) · **Date** : 2026-10-30 · **Verdict** : ✅ **la
> calibration est publiée** — deux fichiers datés (`calibration-lexical.json`,
> `calibration-paraphrase.json`) portent l'empreinte du corpus gelé, le seuil et le taux de
> calibration ; `lecture.py --cascade --calibration` les lit ; **sur un découpage indépendant**,
> la cascade égale encore l'oracle (0,894) sur le lexical et bat les deux choix fixes (0,366
> contre 0,341 et 0,317) sur les paraphrases.
>
> **Dispositif** : `tools/calibrer.py` (banc → seuil → fichier), `--calibration` dans le
> pipeline, `--verifie` (reproductibilité) et `--teste` (hors échantillon) ; fichiers dans
> `tools/tests/documents/`.

## Le passage, du réglage à la politique

R06 v4/v5 avait le résultat mais pas la **publication** : le seuil se réglait à la main sur la
ligne de commande (`--seuil-confiance 0.16`), ce qui n'est pas une politique — c'est un réglage
de séance, invérifiable et non reproductible.

| avant | après |
|---|---|
| un seuil tapé à la main | un **fichier daté** : banc, empreinte du corpus gelé, n, seuil, taux de calibration, poids |
| pas de vérification | `--verifie` : recalcule le seuil sur le même échantillon (reproductible) |
| pas de test hors échantillon | `--teste` : la calibration (paires) appliquée aux impaires |
| réglage local | `lecture.py --cascade --calibration FICHIER` |

## Ce qui est mesuré

| calibration | n | seuil | test hors échantillon (n) | cascade | fixe extractif | fixe modèle | oracle | appels |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| lexical | 124 | 0,168 | 123 | **0,894** | 0,837 | 0,228 | **0,894** | 19 |
| paraphrases | 42 | 0,394 | 41 | **0,366** | 0,317 | 0,341 | 0,439 | 18 |

**La cascade calibrée égale l'oracle sur le lexical** (0,894) et **bat les deux choix fixes** sur
les paraphrases (0,366 contre 0,341 pour le modèle seul et 0,317 pour l'extractif) — sur un
**découpage différent** de celui de R06 v4 (paires/impaires par index, pas `[::2]`). Le résultat
n'est donc pas un artefact du découpage.

**Le coût** : 19 appels de modèle sur 123 questions lexicales (15 %), 18 sur 41 paraphrases
(44 %). ~1,9 s par appel : 36 s et 34 s.

## La recette de déploiement

1. **un banc** : ~50 questions du corpus avec leurs golds (la courbe R06 v5) ;
2. **la calibration** : `python3 tools/calibrer.py --banc … --extractif … --modele … --part paires
   --ecrit calibration-<corpus>.json` ;
3. **le pipeline** : `python3 tools/lecture.py --document … --question … --lecteur cascade
   --calibration calibration-<corpus>.json`.

L'empreinte du corpus gelé dans le fichier dit **à quelle version du corpus** le seuil
appartient : un corpus re-gelé invalide la calibration, visiblement.

## Ce qui pourrait le rendre faux

- **les golds** : la calibration exige un échantillon annoté (50 questions) — c'est le coût, pas
  un détail ;
- **le découpage** : paires/impaires par index ; un autre découpage donnerait ±2 points ;
- **les 19 et 18 appels** : une question d'écart à cette échelle ;
- **le corpus de paraphrases** est petit (83) : la courbe R06 v5 avait montré la saturation à ~25
  golds, mais le plateau est à 0,44 d'oracle — la marge est mince ;
- **l'empreinte** couvre le manifeste du corpus, pas l'extraction (R0.1) : un changement de
  `graphe_document.py` changerait les régions sans invalider la calibration.

## Ce que ça change

1. **La politique est publiée** : un fichier, un format, une commande — pas un réglage de séance.
2. **Le pipeline est complet** : extractif par défaut, `--auto` pour les valeurs, `--cascade
   --calibration` pour un corpus calibré.
3. **La prochaine action du programme R** n'est plus dans R0 : c'est la boucle de lecture
   (R11) ou la restitution (R31), toutes deux dépendantes de N2/R21.

## Fichiers

- `tools/calibrer.py` — la calibration, la vérification, le test hors échantillon.
- `tools/tests/documents/calibration-lexical.json`, `calibration-paraphrase.json` — les fichiers.
- `tools/lecture.py` — `--calibration`.
