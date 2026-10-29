# R43 — Bloc maths (notation, définitions, évaluation)

> **Statut** : spécifiée · **Priorité** : P3 · **Programme** : R · **Dépend de** : R01
> **Ligne de roadmap** : R4.3 · **Fiche de résultat attendue** : rapport-r43-bloc-maths.md (à créer dans `reports/`)
> **Résumé** : Lire une formule, suivre une définition et évaluer symboliquement.

## Le besoin

Les maths ne se lisent pas comme de la prose : il faut la précédence, les définitions, les preuves. Un parseur LaTeX/MathML et un noyau symbolique classique donnent l'exactitude ; le modèle aide à l'intention.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | une formule ou un bloc LaTeX/MathML et une question |
| **sortie** | un AST mathématique, une évaluation symbolique ou un pas de preuve |
| **coût** | coût polynomial borné ; le CAS est un bloc classique |
| **trace** | l'AST et l'évaluation sont tracés |

## Ce qui est mesuré

- taux de parse exact
- exactitude symbolique (dérivée, simplification, substitution)
- exactitude des questions de définition

## Portes

1. 50 formules parsées et évaluées exactement
2. le contrôle « surface seule » échoue
3. les notations non standard sont signalées

## Contrôles négatifs

- texte seul ; parse aléatoire ; évaluation numérique seule
- formule ambiguë (doit être signalée)

## Ce qui pourrait le rendre faux

- le CAS externe fait tout le travail (dépendance non mesurée)
- le corpus ne couvre qu'une notation
- la réponse est dans l'énoncé

## Étapes

1. choisir le parseur et le CAS
2. implémenter l'AST et l'évaluation
3. mesurer parse et exactitude ; écrire la fiche

## Documents à écrire

- `bloc-maths.md` (notation, parseur, CAS, porte, dans `docs/implantation/`)
- mettre à jour R4.3

## Voir aussi

- [Programme R](../roadmap.md#r4--les-blocs-structurels)
- [Analyse, § 6](../../theorie/lecture-rapide.md#6-par-type-de-document)
