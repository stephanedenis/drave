# R06 — la relecture : relire plus ne sert à rien, changer de lecteur ne s'aiguille pas

> **Ligne de roadmap** : R0.4 (troisième tête) · **Date** : 2026-10-29 · **Verdict** : ❌ **trois
> négatifs** — (1) relire davantage ne change **jamais** la réponse extractive (0/249, 0/84) ;
> (2) la relecture-changeement-de-lecteur ne rattrape que **2 questions sur 9** déclenchées et
> en **manque 15** ; (3) le déclencheur lexical ne sépare pas (1–3 mots communs pour les vraies
> questions, 1 pour le hors-sujet).
>
> **Dispositif** : pipeline R0.6 (extractif, seuil 1,0) sur 84 paraphrases ; comparaison des
> modes 30 % et 100 % du banc ; JSON [`r06-relecture.json`](r06-relecture.json) ; spec
> [`pipeline-lecture.md`](../docs/implantation/pipeline-lecture.md).

## La prémisse, testée d'abord

La fiche suppose qu'une **relecture ciblée** rattrape une réponse incertaine. Test direct : sur
les deux bancs, combien de questions ont une réponse **fausse à 30 %** et **juste à 100 %** ?

| banc | 30 % faux → 100 % juste | 30 % juste → 100 % faux |
|---|---:|---:|
| 249 questions lexicales | **0** | 0 |
| 84 paraphrases | **0** | 0 |

**Zéro, exactement.** Ce n'est pas un hasard : le lecteur extractif répond avec le **passage le
mieux score**, et ce passage est **toujours lu** (il est en tête du classement). Lire plus ne
change donc jamais sa réponse — le budget ne peut pas améliorer l'extractif. La relecture qui
pourrait aider n'est pas « relire plus », c'est **changer de lecteur**.

## La relecture comme changement de modalité

Déclencheur testé : le **refus** du pipeline (meilleur score sous le seuil). Sur les 84
paraphrases :

| politique | exactitude | modèle appelé |
|---|---:|---:|
| extractif seul | 0,286 | 0 |
| modèle seul | **0,381** | 84 |
| **règle** : refus → modèle | 0,310 | 9 |

La règle récupère **2 questions sur 9** déclenchées, en **manque 15** (extractif faux, modèle
juste, mais le refus n'a pas tiré) et fait **7 fausses alertes**. Elle ajoute 2,4 points à
l'extractif, mais reste **7 points sous le modèle seul** : le déclencheur coûte plus qu'il ne
rapporte.

## Pourquoi le déclencheur échoue

- **le score BM25 n'est pas une confiance** : il dépend de l'échelle du document (la leçon de
  R0.5) ; un seuil calibré sur un document refuse 32 % des paraphrases d'un autre (mesuré :
  le seuil 3,8 coûtait 6,7 points avant d'être ramené à 1,0) ;
- **les mots communs ne séparent pas** : les vraies questions du pilote partagent 1 à 3 mots
  avec leur réponse, le hors-sujet (« trois ») en partage 1 — mesuré, identique ;
- **la contradiction n'est pas étiquetée** : sans jeu de contradictions, on ne peut pas
  entraîner le volet « contredit une autre région » de la fiche.

## Ce qui n'a pas pu être testé

La porte 3 de la fiche — « la relecture récupère une information que le gist a perdue » —
suppose le **gist** (R21), qui n'est pas construit. Elle reste ouverte et nommée.

## Ce qui pourrait le rendre faux

- **le déclencheur par refus est un choix** : un déclencheur **appris** (sur les scores, la
  dispersion, l'accord entre passages) ferait peut-être mieux — mais il demande un jeu
  d'entraînement et le même test de transfert que R0.4/R0.5, qui ont échoué ;
- **l'échantillon** : 84 questions, 9 déclenchements ;
- **le modèle** : un 0,5 B ; un plus grand modèle rendrait le « toujours le modèle » meilleur
  encore, et le déclencheur plus inutile ;
- **le coût** : 1,9 s par appel n'est pas modélisé dans la règle.

## Ce que ça change

1. **La relecture n'est pas un second passage** : pour un lecteur extractif, le budget au-delà
   du top-k est sans effet. La fiche R06 doit être réécrite autour du **changement de
   modalité**, pas de la relecture.
2. **Le choix extractif/modèle est une décision de corpus**, pas de question : sur un corpus
   lexical l'extractif gagne (0,600 au pilote), sur un corpus de paraphrases le modèle gagne
   (0,381 contre 0,286). Un seuil par question ne fait pas cette différence.
3. **Le pipeline garde son défaut extractif** (seuil 1,0) : refuser 32 % des questions d'un
   autre corpus coûte plus que le faux positif qu'il évite.

## Fichiers

- `reports/r06-relecture.json` — les mesures (84 questions, la règle, les contrôles).
- `tools/lecture.py` — le refus (seuil 1,0) et le changement de lecteur.
- `docs/implantation/pipeline-lecture.md` — le contrat, corrigé du seuil.
