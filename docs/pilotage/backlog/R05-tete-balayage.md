# R05 — Tête de balayage (requête → spans)

> **Statut** : partielle · **Priorité** : P1 · **Programme** : R · **Dépend de** : R03, R01 · **Contraint par** : le manque M4 (aucun encodeur exécutable)
> **Ligne de roadmap** : R0.4 · **Résultat** : [rapport-r05-balayage.md](../../../reports/rapport-r05-balayage.md) — chemin **classique** mesuré : rappel@10 **0,984** (lexical), **0,702** (paraphrases), 0,1 ms ; **branché dans le pipeline** (`--lecteur span`) : **0,944** sur les questions à valeur contre 0,851 pour l'extractif ; la tête n'est pas ajoutée (même mur que R0.4). `--lecteur auto` : **+0,109** sur un corpus de valeurs, **−0,150** sur un corpus mixte (nombres en mots, classement du span).
> **Résumé** : Retrouver les spans qui répondent à une requête, en combinant index classique et scoreur neuronal.
> **Glossaire** : [retrieval](../../theorie/glossaire/entrees/retrieval.md) · [span](../../theorie/glossaire/entrees/span.md) · [lecture rapide](../../theorie/glossaire/entrees/lecture-rapide.md).

## Le besoin

Le balayage humain trouve un nom, un chiffre, une date sans lire tout le document. Le moteur n'a ni encodeur exécutable (M4) ni scoreur de spans : il faut un chemin classique (BM25/regex) et, si nécessaire, une petite tête.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | une requête (question, terme, valeur) et les régions de R01 |
| **sortie** | un classement de spans avec offsets, score et type (nombre, date, nom, phrase) |
| **coût** | index classique d'abord ; la tête ne s'ajoute que si elle paie |
| **trace** | chaque span retenu est tracé avec son score et son offset |

## Ce qui est mesuré

- rappel@k et exactitude des valeurs (nombres, dates, noms)
- temps de recherche par requête
- gains sur la courbe de R03 en mode balayage

## Portes

1. rappel@10 ≥ 95 % sur les nombres et les dates
2. la tête bat BM25 sur les paraphrases, à budget égal
3. les offsets sont exacts et rejouables

## Contrôles négatifs

- requête aléatoire ; index mélangé ; spans négatifs
- requête dont le terme est dans tous les documents

## Ce qui pourrait le rendre faux

- le terme de la requête est dans le span gold par construction
- l'index contient la réponse et le scoreur ne fait que la recopier
- la tokenisation change les offsets

## Étapes

1. construire l'index de spans (regex pour nombres/dates, BM25 pour le texte)
2. mesurer le rappel et le temps ; ajouter la tête si le rappel des paraphrases manque
3. brancher dans le contrôleur ; écrire la fiche

## Documents à écrire

- `tete-balayage.md` (index, scoreur, offsets, porte, dans `docs/implantation/`)
- mettre à jour R0.4

## Voir aussi

- [Programme R](../roadmap.md#r0--le-lecteur-v0-système-sans-entraînement)
- [Analyse, § 4](../../theorie/lecture-rapide.md#4-les-14-techniques-et-leur-état)
