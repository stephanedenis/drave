# N3 — Opérations natives : de la mesure à la production

> **Statut** : partiel · **Priorité** : P2 · **Programme** : N · **Dépend de** : N1
> **Ligne de roadmap** : N3 · **Fiches de résultat** :
> [`n4-porte-execution`](../../../reports/rapport-n4-porte-execution.md),
> [`n4-dessin-b`](../../../reports/rapport-n4-dessin-b.md),
> [`design-H`](../../../reports/rapport-design-H-profondeur-routee.md),
> [`n3.1-etat`](../../../reports/rapport-n3.1-etat.md),
> [`n3.2a-service`](../../../reports/rapport-n3.2a-service.md),
> [`n3.3a-routes`](../../../reports/rapport-n3.3a-routes.md),
> [`n3.2b0-profondeur`](../../../reports/rapport-n3.2b0-profondeur.md),
> [`n3.3b-sparsite`](../../../reports/rapport-n3.3b-sparsite.md),
> [`n3.3c-compte`](../../../reports/rapport-n3.3c-sparsite-compte.md),
> [`n3.4a-composition`](../../../reports/rapport-n3.4a-composition.md),
> [`n3.2b1-seuil`](../../../reports/rapport-n3.2b1-seuil.md),
> [`n3.2b2-cache`](../../../reports/rapport-n3.2b2-cache.md),
> [`n3.4b-pont`](../../../reports/rapport-n3.4b-pont.md),
> [`n3.4c-placement`](../../../reports/rapport-n3.4c-placement.md),
> [`n3.4d-couverture`](../../../reports/rapport-n3.4d-couverture.md),
> [`n3.5a-deux-regions`](../../../reports/rapport-n3.5a-deux-regions.md).
> **Résumé** : les briques natives mesurées (k-WTA, routes, sortie précoce, pont, rejeu,
> placement) doivent **tourner dans le moteur et être gardées par une porte**, pas rester
> dans un outil.

## Le besoin

Une brique mesurée hors du moteur n'est pas une capacité du modèle : elle ne s'exécute pas en
service, et rien ne la protège d'une régression. N3 est le passage **mesure → production →
porte** des opérations natives.

## L'état

**Partiel** — mesuré : la **sortie précoce** (**−24,05 %** de temps pour **−1,61** point de
perte ; le saut de calcul existe, le saut de contenu non), le **cache** (**19,25×**), le pont,
le rejeu et le placement (A2.6). La profondeur routée (dessin B) est **exécutée par le
moteur** : **÷1,47 / ÷1,24** à profondeur 8, avec une variabilité de ±10 % ; le chemin court
entraîné est le facteur limitant (**23,19 %** contre **47,73 %** pour le long).

**Ce qui reste** : un chemin natif distribué (le placement natif est une métadonnée), une
composition complète, et une architecture de cache si elle existe. N3.2a, N3.2b0, N3.2b1
(seuil), N3.2b2 (condition K/V), N3.3a/b/c, N3.4a (composition), N3.4b (pont) et N3.4c
(condition placement) sont **faits**.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | une brique mesurée (sortie précoce, k-WTA, routes, pont, rejeu) |
| **sortie** | la brique dans le moteur, avec son seuil et sa trace |
| **coût** | le temps gagné et la perte acceptée, mesurés à chaque passe |
| **trace** | l'événement de la brique (seuil, raison, couche) est rejoué |

## Portes

1. la brique **s'exécute dans le moteur** (pas dans un outil) ;
2. elle **gagne** sur le temps ou le calcul, à perte bornée ;
3. le **rejeu** redonne la même décision (seuil, couche, raison).

## Contrôles négatifs

- désactiver la brique : le temps doit revenir (le gain disparaît) ;
- un seuil aléatoire : la perte doit exploser (le seuil porte l'information) ;
- rejeu altéré : la décision doit différer (la trace n'est pas décorative).

## Ce qui pourrait le rendre faux

- la variabilité ±10 % entre exécutions peut masquer le gain ;
- la perte mesurée sur un corpus ne dit rien d'un autre ;
- le service n'a pas le même régime que la mesure (cache, lot).

## Étapes

1. ✅ les briques mesurées (sortie précoce, cache, pont, rejeu, profondeur routée) ;
2. ⏳ porter la sortie précoce et la profondeur routée dans le chemin de service ;
3. ⏳ une porte par brique (temps, perte, rejeu) ;
4. ⏳ k-WTA et routes : même traitement.

## Voir aussi

- [Programme N](../roadmap.md#programme-n--le-natif-drvm-drave-n0-distillation)
- [N4 — l'usage](N4-usage-sft.md)
- [Le modèle natif](../../theorie/architecture-native.md)
