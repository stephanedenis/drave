# R03 — Banc de lecture rapide (corpus, tâches, contrôles)

> **Statut** : mesurée · **Priorité** : P0 · **Programme** : R · **Dépend de** : R01, R02
> **Ligne de roadmap** : R0.3 · **Tranches** : [R0.2, 20 questions](../../../reports/rapport-r02-controleur.md) · [lecteur modèle](../../../reports/rapport-r03-lecteur-modele.md) · [banc complet, 249 questions](../../../reports/rapport-r03-banc-complet.md) · [banc durci, 19 puis 84 paraphrases](../../../reports/rapport-r03-banc-durci.md) — mesuré (modèle 0,375 contre lexical 0,269 sur 84 ; **83** depuis la dérive de `continuite.md` ; **corpus gelé** depuis le 30/10)
> **Résumé** : Mesurer la compréhension par unité de calcul, par type de document, avec des contrôles négatifs.
> **Glossaire** : [banc de lecture rapide](../../theorie/glossaire/entrees/banc-de-lecture-rapide.md) · [span](../../theorie/glossaire/entrees/span.md) · [closed-book](../../theorie/glossaire/entrees/closed-book.md) · [F1](../../theorie/glossaire/entrees/f1.md) · [chrF](../../theorie/glossaire/entrees/chrf.md) · [contrôle négatif](../../theorie/glossaire/entrees/controle-negatif.md).

## Le besoin

La PPL mesure la fluidité, pas la lecture. Sans un banc qui mesure la restitution à budget, « rapide » n'est pas défini et aucune technique ne peut être départagée.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | 30 documents (5 types × 6), 10 questions/spans gold par document, 4 modes de lecture |
| **sortie** | un JSON de mesures + une fiche : exactitude, citation, événements, octets, secondes |
| **coût** | le banc doit tourner sur le moteur existant, avec un modèle externe |
| **trace** | chaque essai est rejouable (document, mode, budget, graine) |

## Ce qui est mesuré

- exactitude (exact/F1) par type et par mode
- exactitude de citation et taux de réponses non supportées
- coût (événements/paires, octets, secondes) et ratio à la lecture intégrale

## Portes

1. une courbe vitesse-compréhension par type, avec le point 30 % / 90 %
2. le contrôle négatif (régions aléatoires) est nettement plus bas
3. le banc est reproductible : même document, même mode, même résultat

## Contrôles négatifs

- closed-book : le modèle répond sans le document ; il doit échouer
- régions aléatoires au même budget ; sections mélangées
- questions dont la réponse est dans le titre seul : à retirer ou à compter comme fuite

## Ce qui pourrait le rendre faux

- petit N : 30 documents ne suffisent pas à conclure par type
- les spans gold ou les réponses fuient dans les titres
- le temps est mesuré à chaud ou sur un cache

## Étapes

1. construire le corpus et les questions (5 types × 6 × 10)
2. écrire le harnais (4 modes, 3 budgets) et le contrôle closed-book
3. passer le banc avec un modèle externe ; écrire la fiche
4. décider si le blocage est le contrôleur ou le modèle

## Documents à écrire

- `banc-lecture.md` (corpus, tâches, métriques, contrôles, dans `docs/implantation/`)
- la fiche de résultat dans `reports/`

## Voir aussi

- [Programme R](../roadmap.md#programme-r--le-lecteur-la-nouvelle-cible)
- [Analyse, § 7](../../theorie/lecture-rapide.md#7-le-banc-qui-manque-et-qui-peut-démarrer-sans-entraîner)
