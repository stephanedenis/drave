# R42 — Bloc code (AST, flux de données, exécution)

> **Statut** : mesurée · **Priorité** : P2 · **Programme** : R · **Dépend de** : R01
> **Ligne de roadmap** : R4.2 · **Fiche de résultat** : [`rapport-r42-bloc-code.md`](../../../reports/rapport-r42-bloc-code.md)
> **Résumé** : Lire du code par son AST et son exécution, pas comme un texte.
> **Glossaire** : [AST](../../theorie/glossaire/entrees/ast.md) · [parseur](../../theorie/glossaire/entrees/parseur.md).

## Le besoin

Lire du code demande la portée, le flux de données, les appels et l'exécution. Un parseur et un interpréteur classiques sont plus fiables qu'un modèle pour l'exactitude ; le modèle intervient pour l'intention.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | un fichier de code (langage supporté) et une question |
| **sortie** | un AST, un graphe de symboles, un résultat d'exécution ou une trace |
| **coût** | coût linéaire en nœuds ; l'exécution est bornée (sable) |
| **trace** | l'AST et l'exécution sont tracés |

## L'état

**Mesurée le 2026-10-29** — **294/294** fichiers de `tools/*.py` acceptés (**453 038** nœuds,
**1 722** fonctions, **73** classes) ; **24/24** extraits exécutés à la valeur exacte ; portée
et nom libre vérifiés (`x` module/fonction, `sous_total` signalé) ; le contrôle **texte seul
échoue 3/3** ; **7/7** refus nommés ; coût **×4,4** pour ×4 nœuds. Fiche :
[`rapport-r42-bloc-code.md`](../../../reports/rapport-r42-bloc-code.md) ; spec :
[`bloc-code.md`](../../implantation/bloc-code.md) ; porte `tools/porte-bloc-code.sh` ; JSON :
[`r42-bloc-code.json`](../../../reports/r42-bloc-code.json).

**Miroir entrée/sortie** : 296/296 modules rendus puis relus à l'identique, contrôle négatif perdu (296 exacts).

## Ce qui est mesuré

- couverture du parseur (fichiers acceptés)
- exactitude de l'exécution
- exactitude des questions de code (valeur, flux, bug)

## Portes

1. 20 extraits exécutés exactement
2. le contrôle « texte seul » échoue sur les questions de valeur
3. l'exécution est isolée et reproductible

## Contrôles négatifs

- texte seul ; AST aléatoire ; sans exécuteur
- extrait avec une erreur volontaire (doit être signalé)

## Ce qui pourrait le rendre faux

- les tests contiennent la réponse
- le langage supporté est un sous-ensemble trop petit
- l'exécution n'est pas isolée (sécurité)

## Étapes

1. ✅ choisir le langage et le parseur
2. ✅ implémenter l'AST, les symboles et l'exécuteur
3. ✅ mesurer parseur et exécution ; écrire la fiche

## Documents

- ✅ [`bloc-code.md`](../../implantation/bloc-code.md) — langage, AST, exécuteur, porte, limites.
- ✅ R4.2 marquée mesurée dans la roadmap ; prochaine action : **R4.3**.

## Voir aussi

- [Programme R](../roadmap.md#r4--les-blocs-structurels)
- [Analyse, § 6](../../theorie/lecture-rapide.md#6-par-type-de-document)
