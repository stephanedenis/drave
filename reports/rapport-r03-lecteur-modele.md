# R0.3 (première tranche) — le lecteur modèle : sélectionner bat tronquer, d'une question

> **Ligne de roadmap** : R0.3 · **Date** : 2026-10-29 · **Verdict** : ⚠️ **mesure
> indicative** — le contrôleur domine la troncature naïve (**0,500** contre **0,400**) et le
> hasard (**0,000**) à fenêtre égale, mais sur **10 questions** et un modèle de **0,5 B** :
> l'écart agrégé vaut une question.
>
> **Dispositif** : 10 questions (2 par type), 5 types ; Qwen2.5-0.5B exécuté par le moteur
> Drave (greedy) ; fenêtre de 1 200 caractères ; `tools/lecteur_modele.py` +
> `tools/banc_lecture.py --lecteur modele` ; JSON brut
> [`r03-lecteur-modele.json`](r03-lecteur-modele.json) ; spec
> [`banc-lecture.md`](../docs/implantation/banc-lecture.md) § 6.

## La question

Le lecteur **extractif** de R0.2 plafonne : même en lisant tout, il ne trouve la valeur que
dans **25 à 75 %** des cas. Ce plafond est-il celui du **lecteur** ou celui du **document** ?
On branche un modèle qui lit le contexte sélectionné et on compare, à **fenêtre égale**, trois
façons de remplir la fenêtre : le **contrôleur** (les passages qu'il a choisis, par score), la
**troncature naïve** (les premiers passages, dans l'ordre de lecture), le **hasard**.

## Le dispositif

- **Le modèle** : Qwen2.5-0.5B, `--infer --temp 0 --ctx 512` par le moteur Drave ; aucune API,
  aucun réseau ; 12 jetons en 0,4 s (30 tok/s), ~15 s par appel avec le chargement.
- **Le contexte** : les passages sélectionnés, dans l'**ordre de priorité** (score décroissant
  pour le contrôleur, ordre de lecture pour la troncature), bornés à 1 200 caractères — la
  fenêtre coupe, et c'est justement pour cela que la sélection compte.
- **La question** : « Contexte : … Question : … Réponse : », et la réponse est ce qui suit le
  marqueur. Génération greedy, donc rejouable.
- **10 questions** : 2 par type, les deux premières du banc pilote de R0.2.

## Ce qui est mesuré

Taux de réponses qui contiennent la **valeur** attendue (0 = aucune, 1 = les deux questions) :

| type | contrôleur | début | hasard | closed-book |
|---|---:|---:|---:|---:|
| code | **1,00** | 0,50 | 0,00 | 0,00 |
| tableau | **0,50** | 0,00 | 0,00 | 0,00 |
| technique | 0,50 | 0,50 | 0,00 | 0,00 |
| juridique | 0,50 | 0,50 | 0,00 | 0,00 |
| prose | 0,00 | **0,50** | 0,00 | 0,00 |
| **agrégat** | **0,500** | **0,400** | **0,000** | **0,000** |

**Contrôleur devant 2 types, à égalité 2, derrière 1.** L'écart agrégé (0,500 contre 0,400)
vaut **une question** : c'est une indication, pas une mesure.

**Ce que les réponses montrent.** Le modèle répond juste quand le contexte porte la phrase
(« 3,663 octets par flux », « Le 19 septembre 2025 »), et se trompe quand il doit choisir entre
plusieurs passages proches (« La 4e session » au lieu de la quatre-vingtième). Sur la prose, la
troncature gagne : les documents du dépôt mettent la thèse dans leurs **premiers 1 200
caractères**, et le contrôleur, lui, sélectionne par recouvrement de mots — il rate la phrase
qui définit le mot « drave » parce qu'elle ne partage pas les mots de la question.

## Ce que la mesure a corrigé (et qui vaut d'être noté)

La première exécution paraissait catastrophique pour le contrôleur (0,000 sur deux types). Deux
défauts de **méthode**, pas de politique :

1. **Le mode « début » tombait sur la lecture intégrale** (un `startswith` manquant) : il lisait
   tout le document, puis la fenêtre le tronquait d'elle-même — il semblait battre le contrôleur
   alors qu'il avait un budget dix fois plus grand.
2. **Le contexte était construit dans l'ordre de lecture** : les passages les mieux scorés du
   contrôleur, souvent situés plus loin, étaient coupés par la fenêtre. Le contrôleur était jugé
   sur ce qu'il n'avait pas pu donner. Corrigé : il donne ses passages **par score décroissant**.

C'est le genre de faute qu'un banc doit attraper, et elle était invisible sans le modèle.

## Ce qui pourrait le rendre faux

- **10 questions** : un cas vaut 0,5 ; l'écart contrôleur/début est d'une question. Le banc
  complet (30 documents, 300 questions) est la seule façon de trancher.
- **Un modèle de 0,5 B** : il hallucine (« 4e session ») et répond partiellement (« 2 » pour
  « 2,6998 »). Le classement contrôleur/début reste valable — les deux lisent le même modèle —
  mais le taux absolu ne dit rien d'un grand modèle.
- **Prompt de complétion**, pas de consigne : le modèle n'est pas un assistant ici, il continue
  un texte. Un format instruct changerait les réponses.
- **La fenêtre de 1 200 caractères est un réglage** : plus large, la troncature gagne du terrain ;
  plus étroite, la sélection compte davantage. Ce n'est pas une propriété du document.
- **Le banc est choisi par l'auteur** (5 documents du dépôt) : pas un échantillon.

## Ce que ça change

La sélection a de la valeur avec un modèle — mais **le critère du contrôleur est aligné sur le
lecteur extractif** (BM25 des deux côtés), et c'est un biais : avec un modèle, la prose perd. La
prochaine action n'est donc pas « améliorer le modèle » mais **changer le critère de sélection**
et **passer le banc à l'échelle** :

1. le banc complet (30 documents, 300 questions) pour que 0,5 ne veuille plus dire « une question » ;
2. un critère de sélection qui ne soit pas le même BM25 que le lecteur (couverture de la
   question, diversité des passages, ou un scoreur appris sur les têtes précoces — R04/R05).

## Fichiers

- `tools/lecteur_modele.py` — le modèle comme lecteur (moteur local, greedy, extraction de la réponse).
- `tools/banc_lecture.py --lecteur modele` — les trois façons de remplir la fenêtre ; `--depuis` relit un JSON.
- `reports/r03-lecteur-modele.json` — les mesures brutes.
- `docs/implantation/banc-lecture.md` § 6 — le dispositif et ses limites.
