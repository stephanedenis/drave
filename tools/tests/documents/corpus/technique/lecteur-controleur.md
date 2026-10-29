# Le contrôleur de lecture — cinq actions, un budget, une trace

> **Ce que ce document est.** La spécification de R0.2 : ce qu'un contrôleur de lecture
> choisit, ce qu'il paie, et ce qui permet de rejouer sa trajectoire. Le code est
> `tools/lecteur_controleur.py` ; le banc et la porte sont dans
> [`banc-lecture.md`](banc-lecture.md) ; les chiffres vivent dans `reports/`.
>
> **Chargement** : lire § 2 et § 3 pour coder contre le contrôleur.

## 1. Le besoin

La sortie précoce d'un modèle décide quand le prochain octet est facile ; elle ne décide
pas ce qui vaut la peine d'être lu. Il manque une politique : survoler, balayer, lire,
relire, s'arrêter — et **payer** ce qu'on lit. Sans elle, « lecture rapide » n'est qu'un
débit, et un débit ne dit rien de la compréhension.

## 2. Le contrat

| élément | contenu |
|---|---|
| **entrée** | un manifeste de graphe (R0.1), une **question**, un **budget** en octets |
| **sortie** | une trajectoire : les passages lus, le coût cumulé, la raison de l'arrêt |
| **coût** | les **octets de texte effectivement lus** — pas les régions, pas les secondes |
| **trace** | un événement par décision : action, coût, reste, passage, score, raison |
| **rejeu** | aucun aléa, aucun horodatage : la même entrée donne la même trajectoire |

Le budget est une **fraction du document** (10 %, 30 %, 50 %) : c'est ce qui rend les
documents comparables entre eux.

## 3. Les cinq actions

| action | ce qu'elle lit | ce qu'elle coûte | pourquoi elle existe |
|---|---|---|---|
| **survol** | les en-têtes (`titre`, `section`) | leur texte | c'est le sommaire : il oriente tout le reste, et il est court |
| **balayage** | les passages qui portent la valeur demandée (nombre, date) | ces passages | une question de valeur n'a pas besoin de lire la prose |
| **lecture** | les passages, dans l'ordre du score | ces passages | le cœur : lire peu, mais les bons |
| **relecture** | le voisinage des meilleurs scores, si aucun ne répond | ces passages | une réponse est souvent dans la phrase d'avant |
| **arrêt** | rien | rien | le critère doit être explicite, donc rejouable |

L'arrêt se déclenche sur l'une de ces raisons, toujours nommée dans la trace : part de
budget atteinte, score marginal trop bas, aucun passage ne répond, budget épuisé.

## 4. La politique

1. **survol** — lire les en-têtes ; ils coûtent peu et situent la question ;
2. **classement** — BM25 question ↔ passage, avec un bonus de type si la question demande
   une valeur (un tableau ou du code porte les valeurs) ;
3. **lecture** — les passages dans l'ordre du score, jusqu'à **80 %** du budget ; on
   s'arrête quand le score passe sous **10 %** du meilleur : un passage qui ne partage
   presque rien avec la question ne vaut pas son prix ;
4. **balayage** — si la question est une valeur ou une date, les passages qui la portent,
   dans le budget restant ;
5. **relecture** — si aucun passage lu ne score, le voisinage des deux meilleures sections.

Les 20 % réservés au balayage et à la relecture sont une décision de politique, pas un
réglage : un contrôleur qui dépense tout en lecture ne peut plus vérifier.

## 5. Le lecteur

Le lecteur est **constant** entre la lecture intégrale et la lecture contrôlée : un
extractif qui prend le passage le mieux scoré et le rend **avec sa citation** (région,
offset). Une règle le rend honnête : son index est celui du **document entier**, calculé
une fois ; lire moins ne change pas son modèle de la question, seulement ce qu'il peut
choisir. Sans cette règle, il recalculait ses IDF sur le sous-ensemble lu et changeait
d'avis — un artefact qui faisait croire à un échec du contrôleur.

## 6. Ce que le contrôleur ne fait pas

- **il ne comprend pas** : il score des mots ; une paraphrase sans mot commun ne se
  retrouve pas (c'est un cas de modèle, pas de politique) ;
- **il ne rédige pas** : il rend un passage et sa citation, pas une réponse construite ;
- **il ne juge pas la confiance** : la relecture se déclenche sur l'absence de score, pas
  sur une incertitude calibrée (R06) ;
- **il ne traverse pas les documents** : un document, une question (R51).

## 7. Voir aussi

- [La fiche R02](../pilotage/backlog/R02-controleur-lecture.md) — le contrat et la porte.
- [Le banc de lecture](banc-lecture.md) — les questions, les modes, les contrôles.
- [Le graphe de document](document-graph.md) — les régions et les offsets que le contrôleur lit.
- [La lecture rapide](../theorie/lecture-rapide.md) — pourquoi la politique est le levier.
