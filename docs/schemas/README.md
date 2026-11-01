# Les schémas — index et convention

> **Ce que ce dossier est.** Les **illustrations** de Drave, en **SVG** : les schémas directs
> des concepts, les schémas du natif et de l'impulsionnel, deux sources générées par docwatch et
> les quatorze schémas de la synthèse
> (`docs/theorie/synthese/schemas/`). Chaque SVG direct a un `viewBox`, un `<title>`, un `<desc>` et
> `role="img"` ; aucun n'utilise de ressource externe.
>
> **La règle.** Pas d'ASCII art. Un schéma est un SVG, directement, converti depuis Mermaid ou
> PlantUML, ou un **bloc inline** rendu par docwatch. Voir
> [`docs/methode/illustrations.md`](../methode/illustrations.md) ; vérifier avec
> `python3 tools/verifier_schemas.py`.

## Les schémas des concepts

| schéma | ce qu'il montre | où il est utilisé |
|---|---|---|
| [modules-cerveau-langage.svg](modules-cerveau-langage.svg) | M1 hub → code RSN → bus → M2–M7, M4 → M8 | [les modules](../theorie/modules-cerveau-langage.md) |
| [protocole-semantique.svg](protocole-semantique.svg) | surface L1 → encodeur → z → décodeur + L2 → surface L2 | [le protocole](../theorie/protocole-semantique.md) |
| [jeux-symboliques.svg](jeux-symboliques.svg) | surface → RSN-jeu → décision, l'étage 2 ne voit jamais la surface | [les jeux](../theorie/jeux-symboliques.md) |
| [format-flux.svg](format-flux.svg) | l'en-tête DRVF de 79 octets et le contrat d'activation | [le format](../implantation/format-flux.md) |
| [backlog-dependances.svg](backlog-dependances.svg) | le graphe des dépendances du backlog A/B/N/R, par couche | [le graphe](../pilotage/backlog/dependances.md) |

## Les schémas du natif et de l'impulsionnel

| schéma | ce qu'il montre | où il est utilisé |
|---|---|---|
| [natif-niveaux.svg](natif-niveaux.svg) | N1 surface → N2 RSN → N3 pensée, et le raccourci interdit | [le modèle natif](../theorie/modele-natif.md) |
| [natif-cout-activite.svg](natif-cout-activite.svg) | les listes valuées : le coût suit l'activité, pas la taille | [le modèle natif](../theorie/modele-natif.md) |
| [natif-drvm.svg](natif-drvm.svg) | les quatre sections de DRVM et les trois formats | [le modèle natif](../theorie/modele-natif.md) |
| [natif-graphe-n0.svg](natif-graphe-n0.svg) | `drave-n0` : blocs, régions, têtes précoces, pont, pensée | [le modèle natif](../theorie/modele-natif.md) |
| [natif-pertes.svg](natif-pertes.svg) | les sept pertes du natif et ce qu'elles empêchent | [le modèle natif](../theorie/modele-natif.md) |
| [natif-original.svg](natif-original.svg) | les six gestes qui distinguent Drave | [le modèle natif](../theorie/modele-natif.md) |
| [natif-portes.svg](natif-portes.svg) | les portes N0 → N4 | [le modèle natif](../theorie/modele-natif.md) |
| [natif-quotient.svg](natif-quotient.svg) | la RSN comme quotient : surfaces, corps, annotation, miroir | [le modèle natif](../theorie/modele-natif.md) |
| [natif-types.svg](natif-types.svg) | la matrice des types et le théorème de non-fuite de la surface | [le modèle natif](../theorie/modele-natif.md) |
| [natif-neutralite.svg](natif-neutralite.svg) | neutre et informatif : les deux sondes et les quatre quadrants | [le modèle natif](../theorie/modele-natif.md) |
| [natif-rejeu.svg](natif-rejeu.svg) | la pile de déterminisme et le diff qui localise la divergence | [le modèle natif](../theorie/modele-natif.md) |
| [natif-anti-patrons.svg](natif-anti-patrons.svg) | six façons de casser la séparation, et leur test | [le modèle natif](../theorie/modele-natif.md) |
| [natif-modes.svg](natif-modes.svg) | cinq réalisations du même contrat typé, et le bus qui ne voit que le type | [le modèle natif](../theorie/modele-natif.md) · [le bloc D&C](../implantation/diehl-cook.md) |
| [natif-granularite.svg](natif-granularite.svg) | la granularité : monolithe contre petits blocs, et le coût de la liaison | [le modèle natif](../theorie/modele-natif.md) |
| [diehl-cook-architecture.svg](diehl-cook-architecture.svg) | Poisson, LIF, STDP, inhibition latérale, seuil adaptatif | [le bloc D&C](../implantation/diehl-cook.md) |
| [diehl-cook-placements.svg](diehl-cook-placements.svg) | les trois placements légaux et le raccourci interdit | [le bloc D&C](../implantation/diehl-cook.md) |
| [diehl-cook-contrat.svg](diehl-cook-contrat.svg) | ports, `φ(RSN)`, annotation et refus du chargeur | [le bloc D&C](../implantation/diehl-cook.md) |
| [diehl-cook-temps.svg](diehl-cook-temps.svg) | du spike au fait DRVF : 0,5 ms, 1 000 pas, une trace | [le bloc D&C](../implantation/diehl-cook.md) |
| [diehl-cook-pipeline.svg](diehl-cook-pipeline.svg) | le pipeline de référence à trois niveaux et le miroir | [le bloc D&C](../implantation/diehl-cook.md) |
| [diehl-cook-boucle.svg](diehl-cook-boucle.svg) | la boucle d'entraînement et ses contrôles négatifs | [le bloc D&C](../implantation/diehl-cook.md) |
| [diehl-cook-dynamique.svg](diehl-cook-dynamique.svg) | STDP, poids, seuil adaptatif et WTA : le clustering compétitif | [le bloc D&C](../implantation/diehl-cook.md) |
| [diehl-cook-taux.svg](diehl-cook-taux.svg) | pourquoi c'est un modèle de taux, et le contrôle qui tranche | [le bloc D&C](../implantation/diehl-cook.md) |
| [diehl-cook-memoire.svg](diehl-cook-memoire.svg) | la mémoire N2 : RSN, φ, prototypes, graphe, annotation | [le bloc D&C](../implantation/diehl-cook.md) |
| [diehl-cook-banc.svg](diehl-cook-banc.svg) | le banc v0 pré-enregistré : hypothèses et contrôles | [le bloc D&C](../implantation/diehl-cook.md) |
| [diehl-cook-conformite.svg](diehl-cook-conformite.svg) | la pyramide des tests et les tolérances | [le bloc D&C](../implantation/diehl-cook.md) |

Le **schéma des chantiers** n'est plus un fichier : c'est un bloc **PlantUML inline** dans
[`en-cours.md`](../pilotage/en-cours.md) (structure et états, sans axe de temps) et un **Gantt
indicatif** inline dans la [`roadmap.md`](../pilotage/roadmap.md#le-gantt-indicatif) ; docwatch les
rend en SVG, la source reste dans la page.

## Les sources générées par docwatch

docwatch convertit un source **Mermaid** (`.mmd`) ou **PlantUML** (`.puml`) en `<source>.svg` à la
demande. L'image Markdown pointe vers ce SVG généré, **même s'il n'est pas versionné**.

![Le pipeline des schémas](pipeline.mmd.svg)

*Source : [pipeline.mmd](pipeline.mmd) ; docwatch génère `pipeline.mmd.svg`.*

![Choisir une source de schéma](decision.puml.svg)

*Source : [decision.puml](decision.puml) ; docwatch génère `decision.puml.svg`.*

## Les schémas de la synthèse

| schéma | ce qu'il montre | où il est utilisé |
|---|---|---|
| [vue-ensemble.svg](../theorie/synthese/schemas/vue-ensemble.svg) | Drave en une image : texte, régions, bus, sortie | [chapitre 1](../theorie/synthese/01-le-cerveau-drave.md) · [index](../theorie/synthese/index.md) |
| [anatomie-coupe.svg](../theorie/synthese/schemas/anatomie-coupe.svg) | trois découpages et le coût du pont | [chapitres 1](../theorie/synthese/01-le-cerveau-drave.md) et [2](../theorie/synthese/02-anatomie-interne.md) |
| [modes.svg](../theorie/synthese/schemas/modes.svg) | les six modes d'exécution | [chapitre 3](../theorie/synthese/03-les-modes-et-les-portes.md) |
| [facultes.svg](../theorie/synthese/schemas/facultes.svg) | C1–C12 et les apports E1–E9 | [chapitre 4](../theorie/synthese/04-les-facultes-et-la-biologie.md) |
| [pensee.svg](../theorie/synthese/schemas/pensee.svg) | penser sans verbaliser | [chapitre 5](../theorie/synthese/05-la-pensee-sans-verbaliser.md) |
| [methode.svg](../theorie/synthese/schemas/methode.svg) | mesurer, contrôler, écrire, porter | [chapitre 6](../theorie/synthese/06-comment-savoir.md) |
| [couche-commune.svg](../theorie/synthese/schemas/couche-commune.svg) | surface → RSN → surface | [chapitre 7](../theorie/synthese/07-modeles-alternatifs-entree-sortie.md) |
| [operations.svg](../theorie/synthese/schemas/operations.svg) | les six mesures de B4 et la grappe | [chapitre 8](../theorie/synthese/08-les-operations.md) |
| [bus-evenements.svg](../theorie/synthese/schemas/bus-evenements.svg) | les faits, la liste valuée, le bus | [chapitres 1](../theorie/synthese/01-le-cerveau-drave.md) et [2](../theorie/synthese/02-anatomie-interne.md) |
| [etages.svg](../theorie/synthese/schemas/etages.svg) | les deux étages et le miroir | [chapitre 5](../theorie/synthese/05-la-pensee-sans-verbaliser.md) · [index](../theorie/synthese/index.md) |
| [parcours.svg](../theorie/synthese/schemas/parcours.svg) | trois parcours de lecture | [l'index](../theorie/synthese/index.md) |
| [fiche-concept.svg](../theorie/synthese/schemas/fiche-concept.svg) | l'anatomie d'une fiche concept | [l'index](../theorie/synthese/index.md) |
| [glossaire.svg](../theorie/synthese/schemas/glossaire.svg) | les onze familles du glossaire | [l'index](../theorie/synthese/index.md) |
| [portes.svg](../theorie/synthese/schemas/portes.svg) | la passe des portes et le registre | [chapitre 3](../theorie/synthese/03-les-modes-et-les-portes.md) · [l'index](../theorie/synthese/index.md) |

## Ajouter un schéma

1. choisir le dossier : `docs/schemas/` pour un concept, `docs/theorie/synthese/schemas/` pour la synthèse ;
2. écrire le SVG direct, ou un source `.mmd`/`.puml` (docwatch génère `<source>.svg`) ;
3. lui donner un `viewBox`, un `<title>`, un `<desc>` et `role="img"` ;
4. l'insérer dans la page avec un lien **relatif** et un texte alternatif ;
5. l'ajouter à ce tableau ;
6. lancer `python3 tools/verifier_schemas.py`.

> *Un schéma qui n'est pas référencé est un schéma qui n'existe pas.*
