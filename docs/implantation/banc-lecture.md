# Le banc de lecture — questions, modes, contrôles

> **Ce que ce document est.** La spécification de R0.3 (et du banc **pilote** qui mesure
> R0.2) : le corpus, les questions, les modes, les métriques et les contrôles négatifs. Le
> code est `tools/banc_lecture.py` ; la porte `tools/porte-lecteur.sh` ; les résultats dans
> `reports/`.
>
> **Chargement** : lire § 3 et § 4 pour interpréter un chiffre du banc.

## 1. Le besoin

La perplexité mesure la fluidité, pas la lecture. Sans un banc qui mesure la **restitution
à budget**, « rapide » n'est pas défini et aucune technique ne peut être départagée. Le banc
existe donc avant les optimisations, pas après.

## 2. Le corpus pilote

Cinq types, un document par type, quatre questions par document — vingt questions.

| type | document | ce qu'il éprouve |
|---|---|---|
| technique | `docs/implantation/format-flux.md` | des valeurs dans une prose dense et des blocs de code |
| prose | `docs/theorie/vision.md` | des définitions et des thèses |
| tableau | `docs/pilotage/roadmap.md` | des chiffres dans des tableaux larges |
| juridique | `data/onu/pdf/A_RES_80_1-fr.pdf` | un PDF réel, en-têtes courants, notes |
| code | `docs/implantation/document-graph.md` | un manifeste JSON et des définitions |

**Une question = trois champs** : la question, un **indice** qui localise le passage gold
dans le document, et une **valeur** courte qui doit se retrouver dans la réponse. Le harnais
**échoue** si l'indice est introuvable : un gold absent ferait mesurer du vide.

**Les questions sont lexicales** : aucun mot de la question n'est absent du document. Un
lecteur lexical ne peut pas répondre à une paraphrase sans mot commun ; poser une telle
question mesurerait le **lecteur**, pas le **contrôleur**. Les paraphrases sont un cas de
R0.3 avec un modèle, pas du pilote.

## 3. Les modes

| mode | ce qu'il fait |
|---|---|
| **intégrale** | tout est lu ; c'est la référence |
| **contrôlée** | le contrôleur lit 10 %, 30 % ou 50 % du document |
| **aléatoire** | le même budget, mais des passages tirés au hasard (graine fixe) |
| **mélangée** | les passages sont permutés avant la lecture (l'ordre ne doit pas aider) |
| **sans but** | la question est vide : le contrôleur ne doit pas répondre |
| **closed-book** | aucun passage : aucune réponse possible |

## 4. Les métriques

| métrique | ce qu'elle mesure | ce qu'elle ne mesure pas |
|---|---|---|
| **récupération** | le passage gold a-t-il été lu ? | la qualité de la réponse |
| **valeur** | la réponse contient-elle la valeur attendue ? | le raisonnement |
| **F1** | le recouvrement en mots entre la réponse et le gold | le sens |
| **octets** | le coût réel, contre celui de la lecture intégrale | le temps (à chaud) |

**La porte** exige, à **30 %** du budget et **par type** : récupération **≥ 0,90**, et
valeur **≥ 0,90 ×** celle de la lecture intégrale (si elle est non nulle). Et les quatre
contrôles doivent échouer : le hasard nettement plus bas, « sans but » sans réponse,
closed-book silencieux, « mélangée » sans effondrement.

## 5. Ce qui pourrait le rendre faux

- **petit N** : quatre questions par type ne font pas un taux ; un seul cas vaut 0,25 ;
- **gold choisi par indice** : l'indice localise un passage, il ne prouve pas que c'est le
  meilleur — un gold contestable biaise la récupération ;
- **contrôleur et lecteur partagent BM25** : « le choix du lecteur est toujours lu » est en
  partie structurel ; le chiffre non circulaire est la **récupération du gold** ;
- **questions lexicales** : le banc ne dit rien des paraphrases, et c'est assumé ;
- **corpus du dépôt** : cinq documents choisis par l'auteur du banc, pas un échantillon ;
- **temps non mesuré** : le coût est en octets, pas en secondes ; un modèle lent changerait
  la conclusion sur le débit.

## 6. La montée en R0.3

Le pilote est la **première tranche** du banc complet : 30 documents (5 types × 6), 10
questions par document, trois budgets, et la courbe vitesse-compréhension par type. Ce qui
manque n'est pas le harnais — il est écrit — c'est le **corpus annoté** : les 20 questions
sont un pilote, pas les 300 du banc complet.

## 7. Voir aussi

- [La fiche R03](../pilotage/backlog/R03-banc-lecture-rapide.md) — le contrat et la porte.
- [Le contrôleur de lecture](lecteur-controleur.md) — ce que le banc mesure.
- [Le graphe de document](document-graph.md) — la découpe que le banc consomme.
