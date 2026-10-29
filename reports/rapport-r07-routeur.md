# R0.5 — le routeur : le signal prédit (0,785), la règle ne transfère pas

> **Ligne de roadmap** : R0.5 · **Date** : 2026-10-29 · **Verdict** : ⚠️ **partiel** — le signal
> BM25 **prédit** quel lecteur gagne (AUC **0,785**, contrôles à 0,41), mais un **seuil
> absolu ne transfère pas** d'un banc à l'autre (0,496 et 0,421, contre 0,855 et 0,737 pour le
> choix fixe). Le routeur n'est **pas déployé**.
>
> **Dispositif** : ré-analyse des mesures de R0.3 — 267 questions (248 lexicales, 19
> paraphrases), deux lecteurs, quatre JSON ; deux signaux (max BM25, couverture question ↔
> document) ; transfert par leave-one-bench-out ; JSON brut
> [`r07-routeur.json`](r07-routeur.json).

## La question

Deux régimes mesurés : le **lexical** gagne sur les questions qui partagent les mots du document
(0,72–1,00 contre 0,23), le **modèle** gagne sur les paraphrases (0,717 contre 0,30). Un seul
lecteur perd la moitié des cas. Le routeur doit choisir — la seule question qui compte est :
**le signal prédit-il quel lecteur va gagner, et la règle tient-elle d'un banc à l'autre ?**

## Le dispositif

- **267 questions** : 248 du banc complet (lexicales) + 19 du banc durci (paraphrases) ;
- **deux lecteurs** : extractif (R0.2) et modèle (R0.3), sur les mêmes questions ;
- **deux signaux** : le **meilleur score BM25** des passages du document (avec son échelle, donc
  non comparable d'un document à l'autre), et la **couverture** — la fraction des mots de la
  question présents dans le document (sans échelle) ;
- **le transfert** : le seuil est appris sur un banc, **testé sur l'autre** ; c'est la seule
  façon de savoir si la règle est portable.

## Ce qui est mesuré

| mesure | valeur |
|---|---|
| questions où les deux lecteurs **diffèrent** | **184** / 267 |
| **AUC du signal BM25** | **0,785** |
| AUC de la couverture | 0,529 |
| AUC du signal aléatoire | 0,407 |
| AUC de la longueur de la question (faux signal) | 0,395 |
| exactitude : fixe extractif | **0,816** |
| exactitude : fixe modèle | 0,270 |
| exactitude : **oracle** (le bon lecteur à chaque fois) | **0,888** |

**Le signal BM25 sait quelque chose** (0,785 contre 0,407 au hasard ; la longueur, faux signal,
est à 0,395). La couverture, elle, ne sait rien (0,529) : les paraphrases partagent encore assez
de mots avec le document pour que la couverture ne baisse pas.

**Mais le seuil ne transfère pas** :

| seuil appris sur l'autre banc, testé sur | exactitude du routeur | choix fixe | oracle |
|---|---:|---:|---:|
| le banc lexical (n=248) | **0,496** | 0,855 | 0,899 |
| le banc des paraphrases (n=19) | **0,421** | 0,737 | 0,737 |

Un routeur mal calibré **coûte 30 points** sur le banc lexical, alors que le gain maximal
possible (oracle) n'est que de **7 points** (0,888 contre 0,816). Le rapport bénéfice/risque est
mauvais : **on ne déploie pas**.

## Ce que ça dit

1. **Le signal existe** : l'AUC 0,785 n'est pas du hasard, et les contrôles le confirment.
2. **La règle manque** : un seuil **absolu** dépend de l'échelle des scores, donc du document et
   du corpus. Il faut un signal **relatif** (z-score, percentile par document) ou un routeur
   **appris avec le test de transfert** — et le banc des paraphrases (19 questions) est trop
   petit pour l'apprendre.
3. **Le gain est concentré** : 7 points au mieux, sur 19 questions sur 267. Le routeur est un
   raffinement, pas un levier — tant que le régime paraphrase reste rare dans le corpus.

## Ce qui pourrait le rendre faux

- **19 questions paraphrases** : le seuil appris dessus est une estimation à ±0,1 ;
- **deux bancs de natures différentes** (questions générées vs écrites) : le transfert mesure
  aussi ce changement de nature, pas seulement l'échelle ;
- **la valeur binaire** (juste/faux) : une réponse partielle compte comme fausse ;
- **les lecteurs ne sont pas au même coût** : générer coûte 1,9 s, rendre un passage ~0 ; le
  routeur devrait intégrer ce prix, ce n'est pas fait ici ;
- **l'oracle suppose qu'on sache toujours qui a raison** : c'est un plafond, pas une politique.

## Ce que ça change

1. **Le choix par défaut reste l'extractif** : 0,816 contre 0,270, et il ne coûte rien. Le
   modèle s'appelle **à la demande**, pas par défaut.
2. **R07 reste ouverte** avec un chemin nommé : un signal relatif par document, un routeur
   appris, et un banc paraphrase plus grand.
3. **La leçon de méthode** : un signal qui prédit n'est pas une règle qui décide. La différence
   se mesure par le transfert, pas par l'AUC.

## Fichiers

- `tools/routeur.py` — les deux signaux, l'AUC, le transfert, les contrôles.
- `reports/r07-routeur.json` — les 267 lignes et les agrégats.
- `reports/r03-banc-complet.md`, `reports/r03-banc-durci.md` — les deux régimes mesurés.
