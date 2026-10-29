# R07 — Routeur extractif / génératif (quel lecteur pour cette question ?)

> **Statut** : partiel · **Priorité** : P1 · **Programme** : R · **Dépend de** : R02, R03
> **Ligne de roadmap** : R0.5 · **Résultat** : [rapport-r07-routeur.md](../../../reports/rapport-r07-routeur.md) — signal AUC **0,785** ; v1 seuil **non transférable** (0,496 / 0,421) ; **v2** z-score **0,734** / 0,474, toujours sous le choix fixe. Il faut plus de paraphrases.
> **Résumé** : Choisir, pour une question et un document, entre **rendre le passage** (extractif) et **générer** (modèle) — parce qu'aucun des deux ne gagne partout.

## Le besoin

Deux régimes ont été mesurés, pas supposés :

- sur des questions qui **partagent les mots du document** (banc complet, 249 questions), le
  lecteur **extractif** donne 0,72–1,00 de réponses justes et le modèle **0,23** ;
- sur des **paraphrases** (banc durci, 19 questions), le modèle donne **0,717** et l'extractif
  **0,30**.

Utiliser un seul lecteur, c'est perdre la moitié des cas. Il faut un **routeur** : une règle
simple, mesurable, qui choisit le lecteur et **dit pourquoi**.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | une question, le document, les passages sélectionnés et leurs scores BM25 |
| **sortie** | une décision `{extractif, génératif}` et son motif (le signal, sa valeur, le seuil) |
| **coût** | le signal se calcule sur des scores déjà là : **négligeable** devant une génération |
| **trace** | le signal, le seuil, la décision et l'issue sont tracés, donc rejouables |

**Le signal candidat** : le **meilleur score BM25** des passages sélectionnés (ou le recouvrement
question ↔ document). S'il est haut, les mots de la question sont dans le document : l'extractif
suffit. S'il est bas, la question parle d'autre chose : il faut le modèle.

## Ce qui est mesuré

- **l'exactitude de la décision** : le routeur choisit-il le lecteur qui a raison, sur les
  questions où les deux **diffèrent** ? (quand ils sont d'accord, le choix n'a pas d'enjeu) ;
- **le regret** : la perte moyenne contre un **oracle** qui choisirait toujours le bon lecteur ;
- **le gain** : le routeur fait-il mieux que **chacun** des deux lecteurs fixes, sur **les deux
  bancs** ? C'est la seule formulation qui compte.

## Portes

1. sur **chaque** banc, le routeur fait **≥ max(extractif, modèle) − 0,05** ;
2. il choisit le bon lecteur sur **≥ 80 %** des questions où les deux diffèrent ;
3. le seuil et la décision sont **rejouables** (aucun aléa, aucune horloge).

## Contrôles négatifs

- **toujours extractif** et **toujours génératif** : le routeur doit les battre sur au moins un
  banc, et ne doit pas leur être inférieur sur l'autre ;
- **signal aléatoire** : la décision tirée au sort doit faire moins bien ;
- **signal = longueur de la question** : si ce faux signal fait aussi bien, le vrai n'apporte
  rien ;
- **oracle** : le plafond ; un routeur qui l'atteint est un routeur parfait, pas un résultat.

## Ce qui pourrait le rendre faux

- **le seuil est réglé sur les bancs** : il faut le fixer sur un banc et le tester sur l'autre,
  ou le choisir par un principe (pas par balayage) ;
- **les deux bancs sont petits et inégaux** (249 et 19) : une question durcie vaut 0,05 ;
- **le signal est lexical** : par construction il ne voit pas les paraphrases — c'est le
  principe du routeur, pas un défaut, mais il faut le vérifier ;
- **la valeur binaire** (juste/faux) masque les réponses partielles ;
- **deux lecteurs différents par leur coût** : générer coûte 1,9 s, rendre un passage ~0 ; un
  routeur qui choisit le modèle à tort paie ce prix.

## Étapes

1. calculer le signal sur les deux bancs à partir des scores existants ;
2. balayer le seuil **sur un banc**, figer, **tester sur l'autre** ;
3. mesurer décision, regret, gain ; écrire la fiche ;
4. brancher la décision dans le pipeline de lecture (R0.2/R0.3) et l'exposer dans la trace.

## Documents à écrire

- `routeur.md` (signal, seuil, décision, dans `docs/implantation/`) ;
- la fiche de résultat dans `reports/`.

## Voir aussi

- [Le programme R](../roadmap.md#programme-r--le-lecteur-la-nouvelle-cible)
- [Le banc complet](../../../reports/rapport-r03-banc-complet.md) — le régime lexical.
- [Le banc durci](../../../reports/rapport-r03-banc-durci.md) — le régime paraphrase.
- [Le contrôleur](R02-controleur-lecture.md) — ce qui sélectionne les passages.
