# Les schémas — index et convention

> **Ce que ce dossier est.** Les **illustrations** de Drave, en **SVG** : quatre schémas directs
> des concepts, deux sources générées par docwatch et les quatorze schémas de la synthèse
> (`docs/synthese/schemas/`). Chaque SVG direct a un `viewBox`, un `<title>`, un `<desc>` et
> `role="img"` ; aucun n'utilise de ressource externe.
>
> **La règle.** Pas d'ASCII art. Un schéma est un SVG, directement ou converti depuis Mermaid ou
> PlantUML. Voir [`docs/agent/illustrations.md`](../agent/illustrations.md) ; vérifier avec
> `python3 tools/verifier_schemas.py`.

## Les schémas des concepts

| schéma | ce qu'il montre | où il est utilisé |
|---|---|---|
| [modules-cerveau-langage.svg](modules-cerveau-langage.svg) | M1 hub → code RSN → bus → M2–M7, M4 → M8 | [les modules](../modules-cerveau-langage.md) |
| [protocole-semantique.svg](protocole-semantique.svg) | surface L1 → encodeur → z → décodeur + L2 → surface L2 | [le protocole](../protocole-semantique.md) |
| [jeux-symboliques.svg](jeux-symboliques.svg) | surface → RSN-jeu → décision, l'étage 2 ne voit jamais la surface | [les jeux](../jeux-symboliques.md) |
| [format-flux.svg](format-flux.svg) | l'en-tête DRVF de 79 octets et le contrat d'activation | [le format](../format-flux.md) |

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
| [vue-ensemble.svg](../synthese/schemas/vue-ensemble.svg) | Drave en une image : texte, régions, bus, sortie | [chapitre 1](../synthese/01-le-cerveau-drave.md) · [index](../synthese/index.md) |
| [anatomie-coupe.svg](../synthese/schemas/anatomie-coupe.svg) | trois découpages et le coût du pont | [chapitres 1](../synthese/01-le-cerveau-drave.md) et [2](../synthese/02-anatomie-interne.md) |
| [modes.svg](../synthese/schemas/modes.svg) | les six modes d'exécution | [chapitre 3](../synthese/03-les-modes-et-les-portes.md) |
| [facultes.svg](../synthese/schemas/facultes.svg) | C1–C12 et les apports E1–E9 | [chapitre 4](../synthese/04-les-facultes-et-la-biologie.md) |
| [pensee.svg](../synthese/schemas/pensee.svg) | penser sans verbaliser | [chapitre 5](../synthese/05-la-pensee-sans-verbaliser.md) |
| [methode.svg](../synthese/schemas/methode.svg) | mesurer, contrôler, écrire, porter | [chapitre 6](../synthese/06-comment-savoir.md) |
| [couche-commune.svg](../synthese/schemas/couche-commune.svg) | surface → RSN → surface | [chapitre 7](../synthese/07-modeles-alternatifs-entree-sortie.md) |
| [operations.svg](../synthese/schemas/operations.svg) | les six mesures de B4 et la grappe | [chapitre 8](../synthese/08-les-operations.md) |
| [bus-evenements.svg](../synthese/schemas/bus-evenements.svg) | les faits, la liste valuée, le bus | [chapitres 1](../synthese/01-le-cerveau-drave.md) et [2](../synthese/02-anatomie-interne.md) |
| [etages.svg](../synthese/schemas/etages.svg) | les deux étages et le miroir | [chapitre 5](../synthese/05-la-pensee-sans-verbaliser.md) · [index](../synthese/index.md) |
| [parcours.svg](../synthese/schemas/parcours.svg) | trois parcours de lecture | [l'index](../synthese/index.md) |
| [fiche-concept.svg](../synthese/schemas/fiche-concept.svg) | l'anatomie d'une fiche concept | [l'index](../synthese/index.md) |
| [glossaire.svg](../synthese/schemas/glossaire.svg) | les onze familles du glossaire | [l'index](../synthese/index.md) |
| [portes.svg](../synthese/schemas/portes.svg) | la passe des portes et le registre | [chapitre 3](../synthese/03-les-modes-et-les-portes.md) · [l'index](../synthese/index.md) |

## Ajouter un schéma

1. choisir le dossier : `docs/schemas/` pour un concept, `docs/synthese/schemas/` pour la synthèse ;
2. écrire le SVG direct, ou un source `.mmd`/`.puml` (docwatch génère `<source>.svg`) ;
3. lui donner un `viewBox`, un `<title>`, un `<desc>` et `role="img"` ;
4. l'insérer dans la page avec un lien **relatif** et un texte alternatif ;
5. l'ajouter à ce tableau ;
6. lancer `python3 tools/verifier_schemas.py`.

> *Un schéma qui n'est pas référencé est un schéma qui n'existe pas.*
