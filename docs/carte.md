# La carte de Drave — trouver un sujet en deux clics

> **Le hub de la documentation.** Chaque lien mène à **un fichier** — les ancres internes ne sont pas fiables
> selon le rendu (mdserve, le site, GitHub), et c'est le fichier qui est la bonne unité de navigation. Les six
> autres hubs : [l'état du moment](en-cours.md) · [la roadmap](roadmap.md) · [l'inventaire](README.md) ·
> [la synthèse](synthese/index.md) · [les résultats](../reports/README.md) · [le journal](../journal/README.md).

## Où l'on va, où l'on en est

| | |
|---|---|
| [la vision](vision.md) — la raison d'être, le cœur, les cinq axes, ce qu'elle n'est pas | |
| [la mission et la stratégie](agent/mission.md) — les deux programmes, la stratégie révisée du 24/10 | |
| [l'état du moment](en-cours.md) — où l'on va, ce qui est en cours, ce qui reste aux trois horizons | |
| [la roadmap](roadmap.md) — les deux programmes, les lignes A et B, la file « jamais en attente » | |
| [les références de non-régression](references-non-regression.md) — les passes complètes, les chiffres des portes | |
| [le glossaire](glossaire.md) — les onze familles de termes, et le vocabulaire non négociable | |

## Les concepts (un sujet, un fichier)

| le concept | où il vit |
|---|---|
| **les flots, les listes valuées** — les activations comme faits | [la vision § 1](vision.md) · [le format de flux](format-flux.md) · [l'architecture](architecture-cerveau-et-drave.md) |
| **le coût = octets / bande** — placer un opérateur | [la vision § 2](vision.md) · [le placement du KV](../reports/rapport-placement-kv-8k.md) |
| **le top-k GPU** — le noyau fusionné, le seuil | [le plan du top-k](plan-gpu-topk.md) · [la mesure](../reports/rapport-gpu-topk-tout.md) |
| **la répartition en réseau** — le transport fidèle | [la vision § 4](vision.md) · [le Colab](colab-reparti.md) · [la topologie](../tools/porte-topologie.sh) |
| **le rejeu et le diff** — la trace, les portes | [la vision § 5](vision.md) · [les portes](agent/portes.md) · [la non-régression](references-non-regression.md) |
| **les modes d'exécution** — les six façons de faire tourner | [la synthèse 03](synthese/03-les-modes-et-les-portes.md) · [le mode 4](plan-mode4-lot-listes.md) |
| **le cerveau, les facultés** — la carte | [la carte des facultés](cerveau-facultes.md) · [l'état du cerveau](etat-cerveau.md) · [la synthèse 04](synthese/04-les-facultes-et-la-biologie.md) |
| **la RSN, les unités de sens** — jamais le jeton | [le glossaire, famille 1](glossaire/01-le-projet-ses-noms-sa-methode.md) · [la généalogie des langues](genealogie-des-langues.md) |
| **le pont linéaire** — l'alignement des langues | [la synthèse 05](synthese/05-la-pensee-sans-verbaliser.md) · [la synthèse 07](synthese/07-modeles-alternatifs-entree-sortie.md) |
| **la structure bat la taille** — la thèse, mesurée | [la synthèse 05](synthese/05-la-pensee-sans-verbaliser.md) · [la carte du raisonnement](../reports/rapport-carte-raisonnement-naturel.md) |
| **le point de mesure** — la huitième leçon | [la synthèse 06](synthese/06-comment-savoir.md) · [le NLI dur](../reports/rapport-nli-francais-dur.md) |
| **les opérateurs abstraits** — l'étage 2 | [la négation, mesure B4.1](../reports/rapport-operateur-negation.md) · [la synthèse 05](synthese/05-la-pensee-sans-verbaliser.md) |
| **les négatifs** — ce que la mesure a refusé | [le capteur hebbien](../reports/rapport-hebbien-produits.md) · [l'élagage](../reports/rapport-elagage-logs.md) · [la tête 4 bits](../reports/rapport-placement-kv-8k.md) |

## Les sept chantiers

| chantier | où il vit |
|---|---|
| **C1** corpus et généalogie | [la généalogie](genealogie-des-langues.md) · [le corpus Panini](note-corpus-panini.md) · [l'ingestion](note-ingestion-corpus.md) |
| **C2** traduction | [la synthèse 07](synthese/07-modeles-alternatifs-entree-sortie.md) · [les mesures 39-76](../reports/07-mesures-couche-commune.md) |
| **C3** restitution | [la synthèse 07](synthese/07-modeles-alternatifs-entree-sortie.md) · [la garde de tête](modele-pour-drave.md) |
| **C4** dialectes et styles | [la généalogie](genealogie-des-langues.md) · [les mesures 42-47](../reports/07-mesures-couche-commune.md) |
| **C5** qualité par domaine | [les six registres](../reports/07-mesures-couche-commune.md) · [le NLI dur](../reports/rapport-nli-francais-dur.md) |
| **C6** documentation et rangement | [l'organisation](organisation-du-depot.md) · [l'inventaire](README.md) · [la présente carte](carte.md) |
| **C7** pensée abstraite | [la synthèse 05](synthese/05-la-pensee-sans-verbaliser.md) · [la négation](../reports/rapport-operateur-negation.md) |

## Les phases de la roadmap (le plan)

| phase | où elle vit |
|---|---|
| **A1** observer et régler | [la vision § 3](vision.md) · [le diff par couche](../tools/porte-diff-couche.sh) |
| **A2** répartir sur la machine | [la vision § 3](vision.md) · [le placement](../reports/rapport-placement-kv-8k.md) · [le top-k](plan-gpu-topk.md) |
| **A3** répartir en réseau | [la vision § 4](vision.md) · [le Colab](colab-reparti.md) |
| **A4** rejouer et comparer | [la vision § 5](vision.md) · [les portes](agent/portes.md) |
| **A5** formats, matériels, énergie | [la vision § 6](vision.md) · [le format de flux](format-flux.md) · [le NUMA](numa-segregation.md) |
| **A6** apprendre des flux | [le capteur hebbien](../reports/rapport-hebbien-produits.md) · [l'élagage](../reports/rapport-elagage-logs.md) · [l'heuristique](hebbien-differentiel-et-biologie.md) |
| **A7** la grappe déportée | [la roadmap](roadmap.md) · [la greffe](../tools/porte-greffe.sh) |
| **A8** l'ordonnanceur place et perte | [la roadmap](roadmap.md) · [le placement](../reports/rapport-placement-kv-8k.md) |
| **B1** l'entrée-sortie | [la roadmap](roadmap.md) · [la synthèse 07](synthese/07-modeles-alternatifs-entree-sortie.md) · [DiaBLa](../reports/rapport-dialogue-diabla.md) |
| **B2** la représentation et le raisonnement | [la roadmap](roadmap.md) · [la carte du raisonnement](../reports/rapport-carte-raisonnement-naturel.md) |
| **B3** le plan et la dynamique | [la synthèse 05](synthese/05-la-pensee-sans-verbaliser.md) · [la roadmap](roadmap.md) |
| **B4** les opérateurs abstraits | [la négation](../reports/rapport-operateur-negation.md) · [la roadmap](roadmap.md) |

## Les activités en cours

- **[l'état du moment](en-cours.md)** — la page qu'on lit si on ne lit qu'une page ;
- **[le journal du jour](../journal/2026-10-24.md)** et [l'index du journal](../journal/README.md) ;
- **[les fiches les plus récentes](../reports/README.md)** — l'index des 157 fiches ;
- **[la dernière passe de portes](references-non-regression.md)** — 47 portes, 45 vertes.

## Les schémas (les six SVG de la synthèse)

[la vue d'ensemble](synthese/schemas/vue-ensemble.svg) · [l'anatomie d'une coupe](synthese/schemas/anatomie-coupe.svg) ·
[les facultés](synthese/schemas/facultes.svg) · [les modes](synthese/schemas/modes.svg) ·
[la pensée](synthese/schemas/pensee.svg) · [les portes](synthese/schemas/portes.svg) ·
[la couche commune](synthese/schemas/couche-commune.svg).

## La théorie, les plans, les notes

- **la synthèse** : [l'index](synthese/index.md) · [01 le cerveau](synthese/01-le-cerveau-drave.md) ·
  [02 l'anatomie](synthese/02-anatomie-interne.md) · [03 les modes](synthese/03-les-modes-et-les-portes.md) ·
  [04 les facultés](synthese/04-les-facultes-et-la-biologie.md) · [05 la pensée](synthese/05-la-pensee-sans-verbaliser.md) ·
  [06 savoir](synthese/06-comment-savoir.md) · [07 les modèles alternatifs](synthese/07-modeles-alternatifs-entree-sortie.md) ;
- **les plans techniques** : [le cerveau complet](plan-cerveau-complet.md) · [le top-k GPU](plan-gpu-topk.md) ·
  [le mode 4](plan-mode4-lot-listes.md) · [le préremplissage réparti](plan-prefill-reparti.md) ·
  [MLA](plan-mla-vision.md) · [les modèles lourds](plan-modeles-lourds.md) · [DeepSeek 4.1](plan-deepseek41-complet.md) ·
  [Kimi K3](plan-kimi-k3.md) ;
- **les notes et la biologie** : [la biologie pour Drave](biologie-pour-drave.md) ·
  [le hebbien différentiel](hebbien-differentiel-et-biologie.md) · [le contexte long](contexte-long.md) ·
  [l'impulsion pure](impulsion-pure-apprenant.md) · [le spiking](comparaison-spiking.md) ·
  [Strata](strata-pour-drave.md) · [le modèle pour Drave](modele-pour-drave.md) · [la modularisation](modularisation.md) ·
  [l'architecture Kimi K3](architecture-kimi-k3.md) · [l'émulation du professeur](etat-emulation-professeur.md) ;
- **l'état et les manques** : [l'état](etat.md) · [l'état du cerveau](etat-cerveau.md) · [les manques](manques.md) ;
- **les normes** : [l'organisation du dépôt](organisation-du-depot.md) · [l'utilisation](utilisation.md) ·
  [les relations humaines](relations-humaines.md) · [le programme de recherche](programme-recherche.md).

## Le glossaire, famille par famille

[le hub](glossaire.md) · [1. le projet](glossaire/01-le-projet-ses-noms-sa-methode.md) ·
[2. les modèles](glossaire/02-modeles-et-architectures.md) · [3. les formats](glossaire/03-formats-quantification-encodage.md) ·
[4. le moteur](glossaire/04-le-moteur-drave-execution-structures-out.md) · [5. les flux](glossaire/05-flux-protocole-et-transport.md) ·
[6. la répartition](glossaire/06-repartition-materiel-et-energie.md) · [7. la mesure](glossaire/07-mesure-qualite-et-methode-experimentale.md) ·
[8. les points relevés](glossaire/08-points-releves-non-corriges.md) · [9. les sources](glossaire/09-sources-externes-citees.md) ·
[10. le pont linguistico-sémantique](glossaire/10-le-pont-linguistico-semantique-le-vocabu.md) ·
[11. les sources du § 10](glossaire/11-sources-externes-ajoutees-par-le-10.md).

## Le chapitre 7, partie par partie

[le hub du chapitre](../reports/07-mesures-couche-commune.md) ·
[1](../reports/07/p1.md) · [2](../reports/07/p2.md) · [3](../reports/07/p3.md) · [4](../reports/07/p4.md) ·
[5](../reports/07/p5.md) · [6](../reports/07/p6.md) · [7](../reports/07/p7.md) · [8](../reports/07/p8.md) ·
[9](../reports/07/p9.md) · [10](../reports/07/p10.md).
