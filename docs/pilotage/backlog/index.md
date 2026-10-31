# Le backlog des fonctionnalités — index

> **Ce que ce dossier est.** Une **fiche par fonctionnalité** à documenter et à implémenter : le programme
> **R (le lecteur)** et les lignes ouvertes des programmes A, B et N. Une fiche n'est **pas** un résultat :
> elle porte le besoin, le contrat, la porte, les contrôles négatifs et ce qui pourrait la rendre fausse. Le
> résultat, quand il existe, vit dans `reports/`.
>
> **La roadmap** est [`../roadmap.md`](../roadmap.md) ; l'**analyse** qui a ouvert le programme R est
> [`../../theorie/lecture-rapide.md`](../../theorie/lecture-rapide.md) ; l'**état courant** est
> [`../en-cours.md`](../en-cours.md). **Chargement** : une fiche à la fois, jamais le dossier entier. **29 fiches** : 19 pour R, 10 pour les lignes
> ouvertes A/B/N ; le **graphe** des dépendances est dans [`dependances.md`](dependances.md).

## Comment utiliser une fiche

1. **Lire le besoin et le contrat** — c'est ce qui dit si la fonctionnalité est prête à être codée.
2. **Vérifier la porte et les contrôles négatifs** — sans eux, la fonctionnalité n'est pas mesurable.
3. **Écrire la fiche de résultat dans `reports/`** quand la mesure existe, puis mettre à jour la fiche et la
   roadmap.
4. **Aucune mesure nouvelle dans cette fiche** : les chiffres cités sont des **états déjà mesurés** (avec leur
   fiche dans `reports/`) ; une mesure nouvelle va dans la fiche de résultat, jamais ici.
5. **Une fiche = un contrat.** Si la fonctionnalité change de contrat, on change la fiche, pas le résultat.

## Les statuts

| statut | sens |
|---|---|
| **idée** | le besoin est nommé, le contrat n'est pas écrit |
| **spécifiée** | le contrat, la porte et les contrôles sont écrits (cette fiche) |
| **prête** | les dépendances sont levées, on peut coder |
| **à faire** | spécifiée, pas commencée ; la fiche dit par quoi commencer |
| **en cours** | quelqu'un la code ; la fiche dit où |
| **partiel** | une partie est mesurée, l'autre reste ; la fiche dit laquelle |
| **mesurée** | la fiche de résultat existe et est liée |
| **bloquée** | une dépendance nommée l'empêche d'avancer |
| **abandonnée** | le négatif est écrit ; on ne la refait pas |

## Les priorités

**P0** = prochaine action non bloquée ; **P1** = après P0 ou dépend d'une ligne en cours ; **P2** = utile mais
non bloquant ; **P3** = plus tard, ou dépend d'un bloc absent (vision, maths, WAN).

## Le programme R (lecteur)

**20 fiches.** La colonne « dépend de » ne porte que les **arêtes dures** ; les plafonds et les
contraintes mesurées sont dans chaque fiche et dans le [graphe](dependances.md). Le chemin le plus
long est `R01 → R02 → R03 → R31 → R32 → R51`.

| id | fiche | statut | prio | dépend de | ligne |
|---|---|---|---|---|---|
| R01 | [Graphe de document et registre de régions](R01-graphe-document.md) | mesurée | P0 | — | R0.1 |
| R02 | [Contrôleur de lecture](R02-controleur-lecture.md) | mesurée | P0 | R01 | R0.2 |
| R03 | [Banc de lecture rapide](R03-banc-lecture-rapide.md) | mesurée | P0 | R01, R02 | R0.3 |
| R04 | [Tête de survol](R04-tete-survol.md) | mesurée | P1 | R03, R01 | R0.4 |
| R05 | [Tête de balayage](R05-tete-balayage.md) | mesurée | P1 | R03, R01 | R0.4 |
| R06 | [Tête de relecture](R06-tete-relecture.md) | partiel | P2 | R03, R21, R22 | R0.4 |
| R07 | [Routeur extractif / génératif](R07-routeur-extractif-generatif.md) | mesurée | P1 | R02, R03 | R0.5 |
| R11 | [Contexte hiérarchique et état de section](R11-contexte-hierarchique.md) | spécifiée | P1 | R01, N1, N2 | R1.1 |
| R12 | [Curriculum de contexte long](R12-curriculum-contexte.md) | spécifiée | P1 | R11 | R1.2 |
| R13 | [Tokenisation : octets ou BPE](R13-tokenisation-bpe.md) | mesurée | P2 | — | R1.3 |
| R21 | [Mémoire de travail et gist](R21-memoire-travail-gist.md) | spécifiée | P1 | R01, R11 | R2.1 |
| R22 | [Mémoire épisodique et relecture](R22-memoire-episodique.md) | spécifiée | P2 | R01, R21 | R2.2 |
| R31 | [Restitution : SFT de lecture](R31-restitution-sft.md) | spécifiée | P1 | R01, R03, R21 | R3.1 |
| R32 | [Citations et provenance](R32-citations-provenance.md) | spécifiée | P2 | R31, R01, R21 | R3.2 |
| R41 | [Bloc tableaux](R41-bloc-tableaux.md) | mesurée | P2 | R01 | R4.1 |
| R42 | [Bloc code (AST, exécution)](R42-bloc-code.md) | mesurée | P2 | R01 | R4.2 |
| R43 | [Bloc maths](R43-bloc-maths.md) | mesurée | P3 | R01 | R4.3 |
| R44 | [Encodeur visuel / OCR](R44-encodeur-visuel.md) | bloquée | P3 | R41, R42, R43 | R4.4 |
| R51 | [Lecture croisée / multi-documents](R51-lecture-croisee.md) | spécifiée | P3 | R31, R32, R03, R01 | R5.1 |
| R52 | [Décodeur multilingue](R52-multilingue-decodeur.md) | spécifiée | P3 | B10.3, R31, R32 | R5.2 |

## Les lignes ouvertes A/B/N

**16 fiches compactes.** Elles ne recopient pas les mesures : elles disent l'état, ce qui bloque, la porte et la
prochaine action. Les mesures sont dans `reports/` et dans l'archive de la roadmap.

| id | fiche | statut | prio | dépend de | ligne |
|---|---|---|---|---|---|
| N0.3b | [Parité de perplexité DRVM ↔ GGUF](N0.3b-parite-ppl.md) | mesurée | P1 | N0 | N0.3b |
| N2 | [Distillation native (50 000 séquences)](N2-distillation.md) | en cours | P1 | N1 | N2 |
| N4 | [Usage : SFT, service, sûreté](N4-usage-sft.md) | partiel | P1 | — | N4 |
| B10.2bis | [Décodeur à attention croisée](B10.2bis-decodeur-attention-croisee.md) | mesurée | P2 | — | B10.2bis |
| B10.3 | [Raisonnement sur `z` gelé](B10.3-raisonnement-z.md) | bloquée | P2 | B10.2bis | B10.3 |
| B12.10 | [Pipeline M1 → M4 → M8](B12.10-pipeline-m1-m4-m8.md) | mesurée | P2 | B12 | B12.10 |
| A3.4 | [Démonstration Colab](A3.4-colab.md) | bloquée | P3 | A3 | A3.4 |
| A5.4 | [Opérateur FPGA complet](A5.4-fpga.md) | bloquée | P3 | A5 | A5.4 |
| A6.2 | [Routage MoE appris](A6.2-moe-local.md) | bloquée | P3 | A6 | A6.2 |
| B1.5 | [Prose scientifique (corpus humain)](B1.5-prose-scientifique.md) | bloquée | P3 | B1 | B1.5 |
| B11.10 | [Cartes et ambiguïtés de la RSN](B11.10-cartes-ambiguites.md) | mesurée | P2 | B11 | B11.10 |
| A2.6 | [Ordonnanceur : experts et tête](A2.6-ordonnanceur.md) | partiel | P2 | A2 | A2.6 |
| N3 | [Opérations natives en production](N3-operations-natives.md) | partiel | P2 | N1 | N3 |
| A3.2 | [Granularité du flux](A3.2-granularite.md) | mesurée | P2 | A3 | A3.2 |
| A3.3 | [Seuil de rentabilité](A3.3-seuil.md) | mesurée | P2 | A3.2 | A3.3 |
| A8.0 | [Portes PPL épinglées](A8.0-portes-ppl.md) | mesurée | P2 | A8 | A8.0 |
| A8.3 | [Passer la règle place+perte par défaut](A8.3-defaut.md) | mesurée | P3 | A8.0 | A8.3 |

## Le modèle de fiche

Toute nouvelle fiche part de [`_modele.md`](_modele.md). Le modèle impose les sections : besoin, contrat (entrée,
sortie, coût, trace), mesures, portes, contrôles négatifs, ce qui pourrait la rendre fausse, étapes, documents à
écrire, voir aussi. Une fiche sans **porte** ni **contrôle négatif** n'est pas une fiche : c'est un vœu.

## Le glossaire

Les termes du backlog sont définis dans la **famille 12** du glossaire :
[la lecture, le document et leurs mesures](../../theorie/glossaire/12-la-lecture-le-document-et-ses-mesures.md).
Chaque fiche lie ses termes en tête ; les entrées clés sont
[lecture rapide](../../theorie/glossaire/entrees/lecture-rapide.md) ·
[contrôleur de lecture](../../theorie/glossaire/entrees/controleur-de-lecture.md) ·
[graphe de document](../../theorie/glossaire/entrees/graphe-de-document.md) ·
[gist](../../theorie/glossaire/entrees/gist.md) ·
[span](../../theorie/glossaire/entrees/span.md) ·
[closed-book](../../theorie/glossaire/entrees/closed-book.md) ·
[SFT](../../theorie/glossaire/entrees/sft.md) ·
[chrF](../../theorie/glossaire/entrees/chrf.md) ·
[AST](../../theorie/glossaire/entrees/ast.md) ·
[OCR](../../theorie/glossaire/entrees/ocr.md) ·
[DRVM](../../theorie/glossaire/entrees/drvm.md) ·
[contrôle négatif](../../theorie/glossaire/entrees/controle-negatif.md) ·
[graphe de dépendances](../../theorie/glossaire/entrees/graphe-de-dependances.md).

## Ce qui n'est pas dans ce dossier

- **les résultats** : ils sont dans `reports/` ; une fiche de backlog ne porte pas de chiffre ;
- **le plan** : il est dans [`../roadmap.md`](../roadmap.md) ; la fiche dit *comment* on mesure, la roadmap dit
  *quand* on y va ;
- **l'histoire** : elle est dans `journal/` et dans `docs/archive/`.

## Voir aussi

- [Le graphe des dépendances](dependances.md) — les arêtes dures, les plafonds, la frontière et les priorités.
- [La roadmap unique](../roadmap.md) — les programmes A, B, N, R et l'ordre du jour.
- [L'analyse de la lecture rapide](../../theorie/lecture-rapide.md) — les 14 techniques et les cinq couches.
- [L'état courant](../en-cours.md) — la prochaine action.
- [Les résultats](../../../reports/README.md) — les fiches mesurées.
