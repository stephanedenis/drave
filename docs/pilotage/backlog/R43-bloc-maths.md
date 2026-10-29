# R43 — Bloc maths (notation, définitions, évaluation)

> **Statut** : mesurée · **Priorité** : P3 · **Programme** : R · **Dépend de** : R01
> **Ligne de roadmap** : R4.3 · **Fiche de résultat** : [`rapport-r43-bloc-maths.md`](../../../reports/rapport-r43-bloc-maths.md)
> **Résumé** : Lire une formule, suivre une définition et évaluer symboliquement.
> **Glossaire** : [CAS](../../theorie/glossaire/entrees/cas.md) · [parseur](../../theorie/glossaire/entrees/parseur.md).

## Le besoin

Les maths ne se lisent pas comme de la prose : il faut la précédence, les définitions, les preuves. Un parseur LaTeX/MathML et un noyau symbolique classique donnent l'exactitude ; le modèle aide à l'intention.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | une formule ou un bloc LaTeX/MathML et une question |
| **sortie** | un AST mathématique, une évaluation symbolique ou un pas de preuve |
| **coût** | coût polynomial borné ; le CAS est un bloc classique |
| **trace** | l'AST et l'évaluation sont tracés |

## L'état

**Mesurée le 2026-10-29** — **32/32** formules exactes (fractions) et **32/32** recoupées par
**sympy** ; **10/10** dérivées justes (5 points, oracle sympy) ; **6/6** équations (dont
**1 refus** d'une non linéaire) ; **8/8** refus nommés ; le contrôle **surface échoue 3/3** ;
coût **×4,1** pour ×4 termes. Le CAS est **interne** ; sympy ne sert que d'oracle (la
dépendance est mesurée, pas cachée). Fiche :
[`rapport-r43-bloc-maths.md`](../../../reports/rapport-r43-bloc-maths.md) ; spec :
[`bloc-maths.md`](../../implantation/bloc-maths.md) ; porte `tools/porte-bloc-maths.sh` ; JSON :
[`r43-bloc-maths.json`](../../../reports/r43-bloc-maths.json).

**Miroir entrée/sortie** : 42/42 formules et dérivées rendus puis relus à l'identique, contrôle négatif perdu (42 exacts).

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

1. ✅ choisir le parseur et le CAS (interne, oracle sympy)
2. ✅ implémenter l'AST, l'évaluation, la dérivée et la résolution
3. ✅ mesurer parse et exactitude ; écrire la fiche

## Documents

- ✅ [`bloc-maths.md`](../../implantation/bloc-maths.md) — notation, parseur, CAS, porte, limites.
- ✅ R4.3 marquée mesurée dans la roadmap ; **R4.4 est bloqué** (aucun OCR sur la machine).

## Voir aussi

- [Programme R](../roadmap.md#r4--les-blocs-structurels)
- [Analyse, § 6](../../theorie/lecture-rapide.md#6-par-type-de-document)
