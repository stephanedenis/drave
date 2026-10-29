# R02 — Contrôleur de lecture (survol, balayage, sélectif, relecture)

> **Statut** : spécifiée · **Priorité** : P0 · **Programme** : R · **Dépend de** : R01
> **Ligne de roadmap** : R0.2 · **Fiche de résultat attendue** : rapport-r02-controleur.md (à créer dans `reports/`)
> **Résumé** : Choisir, pour un but et un budget, la prochaine action de lecture et sa profondeur.

## Le besoin

La sortie précoce décide quand le prochain octet est facile, pas ce qui vaut la peine d'être lu. Il manque une politique qui choisit entre survoler, balayer, lire, relire et s'arrêter.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | un document (R01), un but (question ou tâche), un budget (événements/paires/octets) |
| **sortie** | une trajectoire de lecture : régions lues/sautées, action, raison, coût cumulé |
| **coût** | le budget est la contrainte ; le coût est compté en événements et en octets |
| **trace** | chaque décision est un événement tracé (région, action, score, budget restant) |

## Ce qui est mesuré

- exactitude de la réponse contre la lecture intégrale, par type
- coût réel (événements, octets, secondes) et ratio à la lecture intégrale
- exactitude de citation : la réponse cite-t-elle la bonne région ?

## Portes

1. à 30 % du budget, ≥ 90 % de l'exactitude de la lecture intégrale sur 3 types
2. le critère d'arrêt est explicite et reproductible
3. le rejeu de la trajectoire redonne la même réponse

## Contrôles négatifs

- régions aléatoires au même budget (le contrôle doit être nettement plus bas)
- sections mélangées (le contrôleur ne doit pas profiter de l'ordre)
- sans but : le contrôleur ne doit pas battre le hasard

## Ce qui pourrait le rendre faux

- les spans gold sont dans les titres et le contrôleur les lit sans comprendre
- le contrôleur est réglé sur le jeu de test
- le modèle répond de mémoire (closed-book) au lieu de lire

## Étapes

1. définir les actions et le budget ; écrire le traceur
2. implémenter les scoreurs classiques (TOC, titres, premières/dernières phrases, BM25/regex)
3. implémenter la politique et le critère d'arrêt
4. mesurer sur le banc R03 ; écrire la fiche

## Documents à écrire

- `lecteur-controleur.md` (actions, budget, trace, politique, dans `docs/implantation/`)
- mettre à jour la ligne R0.2 de la roadmap

## Voir aussi

- [Programme R](../roadmap.md#programme-r--le-lecteur-la-nouvelle-cible)
- [Analyse, § 5.3](../../theorie/lecture-rapide.md#53-la-politique-de-lecture-l3--le-cœur-du-sujet)
