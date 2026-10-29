# R06 v4 — la cascade à confiance calibrée égale l'oracle, hors échantillon

> **Ligne de roadmap** : R06 (relecture) · **Date** : 2026-10-29 · **Verdict** : ✅ **le
> déclencheur est trouvé** — la cascade à confiance, **calibrée sur une moitié du corpus**,
> atteint **0,911** sur le lexical (fixe 0,870, oracle 0,911) et **0,415** sur les paraphrases
> (fixe 0,366, oracle 0,415), **hors échantillon**, avec **15** et **35** appels de modèle.
>
> **Dispositif** : `lecture.py --cascade --seuil-confiance S` ; confiance = 0,5 × couverture +
> 0,3 × accord + 0,2 × dispersion ; seuil calibré sur les questions paires, testé sur les
> impaires ; JSON [`r06-cascade-confiance.json`](r06-cascade-confiance.json).

## Le protocole

Un seuil calibré sur le **test** est un oracle, pas une politique. On coupe donc chaque corpus en
deux : la **calibration** (questions paires) choisit le seuil qui maximise le taux, le **test**
(questions impaires) mesure la politique — sans jamais voir le test.

## Ce qui est mesuré

| corpus | calibrage (n) | seuil | **test : cascade** | fixe extractif | fixe modèle | **oracle** | appels modèle |
|---|---:|---:|---:|---:|---:|---:|---:|
| lexical | 124 | 0,16 | **0,911** | 0,870 | 0,260 | **0,911** | 15 / 123 |
| paraphrases | 42 | 0,53 | **0,415** | 0,268 | 0,366 | **0,415** | 35 / 41 |

**La cascade calibrée égale l'oracle sur les deux corpus, hors échantillon.** Elle bat le
meilleur choix fixe de **+4,1 points** (lexical) et **+4,9 points** (paraphrases) — et elle paie
le modèle **15 fois** sur 123 questions lexicales (les questions où l'extractif est douteux),
**35 fois** sur 41 paraphrases (où le modèle est presque toujours le bon choix).

## Ce que ça dit — le verrou est levé

R0.5, R06 v1 et la cascade v2 échouaient parce qu'un **seuil absolu** ne transférait pas. La
réponse n'était pas un autre score, c'était un **protocole** :

1. **des signaux sans échelle** (couverture, accord, dispersion) — l'AUC transfère (1,000/0,891) ;
2. **un seuil calibré par corpus** — un échantillon avec golds suffit (124 et 42 questions) ;
3. **une politique qui paie le modèle au bon endroit** — 12 % des questions lexicales, 85 % des
   paraphrases.

C'est la loi « le corpus décide » rendue **opérationnelle** : le corpus ne décide plus du lecteur
en bloc, il fournit la calibration ; le déclencheur choisit ensuite question par question.

## Ce qui pourrait le rendre faux

- **la calibration exige des golds** : un échantillon du corpus avec les réponses ; sans lui, pas
  de seuil — c'est une contrainte de déploiement, pas un détail ;
- **les poids de la confiance sont fixés à la main** (0,5/0,3/0,2) : un apprentissage les
  réglerait mieux, au risque du sur-apprentissage ;
- **l'égalité avec l'oracle** est exacte à la question près sur 123 et 41 questions : à confirmer
  sur d'autres corpus ;
- **le coût** : 1,9 s par appel de modèle ; 15 appels = 28 s pour 123 questions, 35 = 66 s pour
  41 — la cascade à confiance est plus chère que l'extractif seul, et c'est le prix du gain.

## Ce que ça change

1. **La relecture a son déclencheur** : la fiche R06 passe de « triple négatif » à « cascade à
   confiance calibrée » — le verrou unique du programme R est levé.
2. **Le pipeline a sa politique complète** : extractif par défaut, `--auto` pour un corpus de
   valeurs, `--cascade --seuil-confiance S` pour un corpus calibré.
3. **La leçon de méthode** : trois échecs de seuil ont produit un succès — en changeant de
   protocole (calibrer, pas transférer), pas en changeant de score.

## Fichiers

- `tools/lecture.py` — `confiance()` et `--cascade --seuil-confiance`.
- `reports/r06-cascade-confiance.json` — les mesures hors échantillon.
