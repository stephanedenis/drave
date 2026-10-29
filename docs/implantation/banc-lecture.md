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

## 6. Le lecteur modèle

Le lecteur extractif plafonne (25 à 75 % même en lisant tout) : c'est lui qu'il faut changer,
pas la sélection. Le banc accepte donc `--lecteur modele` : un **Qwen2.5-0.5B** sur **GPU** via
`llama-cli` (build CUDA, `-ngl 99`, `--temp 0`), sans API ni réseau, en génération **greedy**.
Un seul GPU (`CUDA_VISIBLE_DEVICES=0`) : l'autre reste à N2.

**Ce qui change, et ce qui ne change pas.** La sélection est identique — même contrôleur, mêmes
budgets. Seul l'answerer change : il reçoit les passages sélectionnés, dans l'ordre de lecture,
bornés par la **fenêtre** (1 200 caractères, ~300 jetons). Le modèle ne « lit » pas tout : il lit
ce qui tient, et c'est précisément pour cela que la sélection compte.

**Les trois façons de remplir la fenêtre**, à budget égal :

| mode | ce qu'il représente |
|---|---|
| `controlee_0.30` | le contrôleur de R0.2 : les passages qu'il a choisis |
| `debut_0.30` | la **troncature naïve** : les premiers passages du document — ce que fait un lecteur qui n'a pas de politique |
| `aleatoire_0.30` | des passages au hasard, même budget |

La comparaison qui décide est **contrôleur contre début** : si sélectionner ne bat pas prendre
le début, le contrôleur ne sert à rien.

**Ce n'est pas une porte.** La génération coûte ~1,9 s par appel sur GPU (contre 8 à 15 s sur
le CPU du moteur), soit une minute pour 30 questions : la porte reste extractive et rapide, la
mesure modèle se lance à la main et vit dans `reports/`.

**Le runtime fait partie du dispositif.** Le même GGUF, le même prompt et le même greedy
donnanent des réponses différentes selon le moteur (BOS, pénalité de répétition, découpage du
prompt) : 0,6 sur le moteur CPU, 0,5 sur `llama-cli`. Aucun chiffre de lecteur ne se cite sans
son runtime.

**Ce qui pourrait la rendre fausse** : un modèle de 0,5 B peut échouer pour des raisons de
capacité et non de sélection — la comparaison « contrôleur contre début » reste valable, mais
le taux absolu ne dit rien d'un grand modèle ; la fenêtre de 512 jetons est un réglage, pas une
propriété du document ; et un prompt de complétion n'est pas une consigne (pas d'instruction
système ici).

## 7. La montée en R0.3

Le pilote est la **première tranche** du banc complet : 30 documents (5 types × 6), 10
questions par document, trois budgets, et la courbe vitesse-compréhension par type. Ce qui
manque n'est pas le harnais — il est écrit — c'est le **corpus annoté** : les 20 questions
sont un pilote, pas les 300 du banc complet.

## 8. Voir aussi

- [La fiche R03](../pilotage/backlog/R03-banc-lecture-rapide.md) — le contrat et la porte.
- [Le contrôleur de lecture](lecteur-controleur.md) — ce que le banc mesure.
- [Le graphe de document](document-graph.md) — la découpe que le banc consomme.
