# R06 v5 — la courbe de calibration : ~50 golds suffisent, les poids appris n'ajoutent rien

> **Ligne de roadmap** : R06 (relecture) · **Date** : 2026-10-30 · **Verdict** : ✅ **la cascade
> à confiance se calibre avec ~50 questions** — 0,906 à k=49 sur le lexical (0,911 à k=124),
> 0,399 à k=25 sur les paraphrases (0,415 à k=42) ; ❌ **les poids appris ne valent pas mieux**
> que les poids fixés (égaux sur le lexical, **pires** sur les paraphrases : 0,366 contre 0,415).
>
> **Dispositif** : test **fixe** (les impaires), calibration tirée des paires (20 tirages par
> taille), seuil réglé sur le tirage, taux mesuré sur le test ; JSON
> [`r06-courbe-calibration.json`](r06-courbe-calibration.json).

## La question

La cascade à confiance calibrée égale l'oracle (R06 v4), mais elle exige des **golds** pour
régler son seuil. Combien ? Et les poids de la confiance (fixés à la main : 0,5 couverture +
0,3 accord + 0,2 dispersion) méritent-ils d'être appris ?

## La courbe

| k (golds) | lexical — fixé | lexical — appris | paraphrases — fixé | paraphrases — appris |
|---:|---:|---:|---:|---:|
| 5–12 | 0,891 ± 0,034 | 0,891 ± 0,034 | 0,350 ± 0,037 | 0,332 ± 0,044 |
| 16–24 | 0,899 ± 0,022 | 0,898 ± 0,024 | 0,393 ± 0,031 | 0,365 ± 0,020 |
| 25–49 | **0,906 ± 0,007** | 0,906 ± 0,007 | **0,399 ± 0,030** | 0,371 ± 0,020 |
| 74–99 | 0,908 ± 0,004 | 0,908 ± 0,004 | 0,395 ± 0,024 | 0,374 ± 0,018 |
| 124 / 42 | 0,911 | 0,911 | 0,415 | 0,366 |

**~50 golds suffisent** sur le lexical (0,906 contre 0,911 au maximum) ; **~25** sur les
paraphrases (0,399 contre 0,415). Le plateau est atteint tôt : la calibration est **bon marché**.

**Les poids appris n'apportent rien** : identiques sur le lexical (le signal dominant, la
couverture, impose le même ordre), et **inférieurs** sur les paraphrases (0,366 contre 0,415) —
la logistique sur-apprend 25 à 42 exemples. Les poids fixés restent.

## Le pilote, complété

Le modèle manquait sur les 20 questions du pilote ; il est rejoué (40 appels GPU) :

| jeu | extractif | modèle | oracle |
|---|---:|---:|---:|
| lexical (248) | **0,874** | 0,231 | 0,915 |
| paraphrases (83) | 0,265 | **0,373** | 0,458 |
| **pilote (20)** | **0,600** | 0,400 | — |

Le pilote est un corpus **mixte** où l'extractif gagne — cohérent avec R0.3 : le choix du lecteur
est une affaire de corpus, et le pilote est du côté lexical.

## Ce que ça dit

1. **Le coût de la calibration est faible** : ~50 questions avec golds par corpus, et la
   politique est à 1 point du maximum.
2. **La confiance fixée à la main est suffisante** : apprendre les poids sur 25–50 exemples
   dégrade (sur-apprentissage) ; il faudrait des centaines d'exemples pour que l'apprentissage
   paie — et les poids fixés sont déjà bons.
3. **La recette de déploiement est complète** : 50 golds → le seuil → la cascade à confiance, à
   ~1 point de l'oracle, avec 12 % d'appels modèle sur un corpus lexical et 85 % sur un corpus
   de paraphrases.

## Ce qui pourrait le rendre faux

- **20 tirages** par taille : la dispersion est estimée grossièrement (les écarts-types vont de
  0,004 à 0,044) ;
- **le test fixe** (les impaires) est le même d'un tirage à l'autre : la variance mesurée est
  celle de la calibration seule ;
- **deux corpus** : la courbe est un motif, pas une loi ;
- **les golds** : la calibration suppose les réponses connues — c'est un échantillon annoté, pas
  la production.

## Fichiers

- `tools/declencheur.py --courbe` — la courbe (tailles × tirages × poids fixés/appris).
- `reports/r06-courbe-calibration.json`, `reports/r03-pilote-modele.json` — les mesures.
