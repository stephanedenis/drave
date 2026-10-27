# Glossaire raisonné de Drave

> **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Compteurs unifiés
> (**49 portes, 8 chapitres, 181 fichiers / 248 JSON, 54 documents**), chemins archivés corrigés
> (`docs/archive/`), B10–B12 réintégrés dans les cartes. **Les règles d'`AGENTS.md` ne changent
> pas.** *Le contenu du glossaire reste ; la méta (54 docs / 181 fichiers) et le parcours de
> lecture sont corrigés.*

Ce document explique **tout le vocabulaire** employé dans `docs/` (54 documents hors archive) et
`reports/` (181 fichiers, 248 JSON), pour quelqu'un qui ne
connaît ni les grands modèles de langage, ni le matériel, ni le vocabulaire de la
mesure de performance. Il se lit seul : chaque notion est définie sur place, et
chaque définition renvoie au fichier du dépôt qui l'emploie.

---

## Mode d'emploi

**Ce que contient une entrée.** Chaque entrée suit le même patron :

> **Terme** *(forme développée française ; forme anglaise)* — définition en une à
> trois phrases, sans prérequis. La définition dit **où** le moteur s'en sert
> (fichier, outil ou drapeau du dépôt, avec un numéro de ligne quand il aide) et,
> quand une source externe stable existe, la référence **Réf.** (article,
> spécification, documentation officielle).

**Conventions de lecture.**

- `chemin:ligne` renvoie à un fichier **du dépôt**, à la ligne indiquée. Exemple :
  `docs/vision.md:34`.
- Les liens externes pointent vers des articles ou des spécifications ; quand je
  n'ai pas pu vérifier l'adresse, je cite l'article **par son titre et ses
  auteurs, sans lien** — c'est une règle du dépôt, on n'invente pas d'URL.
- Un terme qui a **plusieurs sens** dans le corpus est signalé ; c'est le cas de
  *CDC*, *mode*, *porte*, *grappe* et *tête*.
- Les valeurs numériques citées ici sont celles des documents, **à leur date**.
  Elles ne sont pas re-mesurées par ce glossaire ; la section
  « Points relevés, non corrigés » en bas signale celles qui se contredisent.

**Ce que ce document n'est pas.** Ce n'est ni un tutoriel d'inférence, ni un
résumé de la feuille de route. Il ne corrige aucun autre fichier : les erreurs,
contradictions et chiffres périmés croisés en le rédigeant sont **listés à la fin**,
avec `fichier:ligne` et citation, sans être modifiés.

**Sections 10 et 11 — ajoutées après coup.** Le glossaire couvrait le moteur, le
matériel et la mesure ; il ne couvrait pas le **pont linguistico-sémantique**, le
travail en cours. Le §10 comble ce trou (professeur, réservoir, lecture, oracle,
invariance, attrition, fragmentation…) et son §10.9 définit les termes employés
**dans** ces définitions. Le §11 liste les sources externes ajoutées, en distinguant
celles dont l'adresse a été vérifiée de celles citées par titre.

**Périmètre.** `docs/` (54 documents hors archive) et `reports/` (181 fichiers, 248 JSON) ; les
9 fichiers de `sprints/` sont couverts pour leur vocabulaire propre (boxing, cérémonie,
porte). Le code est cité pour dire *où* un terme est utilisé (`drave-core/src/`,
`tools/`), mais le glossaire ne décrit pas le code ligne à ligne. Les fichiers
`README.md`, `REPRISE.md` et `Qtrinet-bootstrap.md` sont à la racine, hors
périmètre : ils sont signalés quand ils portent un chiffre utilisé partout.

---

## Parcours de lecture conseillé

**Si tu ne lis qu'un document, lis `docs/vision.md`** (121 lignes) : c'est la
vision — des listes d'activation plutôt que des matrices, cinq axes, ce que le
projet n'est pas, et le nom. Tout le reste du dépôt en découle.

Ensuite, dans cet ordre :

1. **`docs/histoire.md`** (78 lignes) — pourquoi le projet s'appelait Qtrinet et
   s'appelle Drave, et la table de conversion des anciens noms de variables. À
   lire tôt : tous les rapports antérieurs au 30/09/2026 emploient encore
   « Qtrinet », `QT_*` et `qtrinet-core`.
2. **`docs/roadmap.md`** (430 lignes) — l'état réel de chaque chantier, phase par
   phase, avec les chiffres et leur date. C'est le document qui dit ce qui est
   fait (✅), en cours (🔬), à faire (⏳) ou bloqué (🧱).
3. **`docs/format-flux.md`** (209 lignes) — le format `DRVF` : ce qu'est une trace,
   comment elle se relit, et le protocole réseau **v5** avec ses cinq modes. Le
   cœur technique du projet est là.
4. **`docs/agent/resultats.md`** (47 lignes) — ce qu'un résultat doit porter
   (chiffre, dispositif, contrôle négatif, fiche) : la méthode qui donne son sens
   au reste.
5. **`reports/rapport-inference.md`** — la mesure fondatrice : un moteur de
   2 319 lignes de Rust sans dépendance, 5,3 G événements/s sur CPU, 16 jetons
   identiques sur 16 à la référence numpy.
6. **`reports/rapport-croisement-push-pull.md`** — la mesure qui fixe la frontière
   du projet : le chemin « push » (listes) bat le dense en dessous de ~22 % de
   densité d'activation, et perd au-dessus. Tout le reste en dépend.
7. **`docs/contexte-long.md`** — ce que « 1 M de jetons de contexte » veut dire, et
   par où ça casse (préremplissage, bande passante du cache, rotation).
8. **`docs/format-clusters.md`** — comment un modèle est éclaté en grappes
   (`commun.gguf` + `cluster-XX.gguf`) et pourquoi c'est le mécanisme de placement.
9. **`docs/synthese/index.md`** — la théorie en **huit chapitres** et sept schémas ;
   c'est la lecture qui relie le moteur, la langue et la pensée.

Pour aller plus loin, et pour l'histoire : `docs/archive/sprints.md` (la charte des
sprints de 2 h), `docs/archive/plan-deepseek41-complet.md` (le chantier V4.1),
`docs/archive/programme-recherche.md` (la thèse et ses critères d'arrêt),
`docs/archive/comparaison-spiking.md` (ce que les réseaux à spikes changent),
`docs/archive/plan-mla-vision.md` (attention latente et vision), et — quand un chiffre
semble contradictoire — `reports/rapport-coherence-docs-2.md`, l'audit qui recense
les affirmations périmées du corpus.

À la racine, `README.md` (19 ko) donne l'état général et `REPRISE.md` (12 ko) la
check-list de reprise ; ils emploient le même vocabulaire que ce glossaire.

---


## Les onze familles

Le glossaire fait **2 276 lignes** : il est découpé en **onze familles**, chacune atteignable
directement. Les liens vers ce fichier continuent de fonctionner.

| famille | fichier | lignes |
|---|---|---:|
| **1.** Le projet, ses noms, sa méthode | [01-le-projet-ses-noms-sa-methode.md](glossaire/01-le-projet-ses-noms-sa-methode.md) | 218 |
| **2.** Modèles et architectures | [02-modeles-et-architectures.md](glossaire/02-modeles-et-architectures.md) | 363 |
| **3.** Formats, quantification, encodage | [03-formats-quantification-encodage.md](glossaire/03-formats-quantification-encodage.md) | 195 |
| **4.** Le moteur Drave : exécution, structures, outils | [04-le-moteur-drave-execution-structures-out.md](glossaire/04-le-moteur-drave-execution-structures-out.md) | 217 |
| **5.** Flux, protocole et transport | [05-flux-protocole-et-transport.md](glossaire/05-flux-protocole-et-transport.md) | 124 |
| **6.** Répartition, matériel et énergie | [06-repartition-materiel-et-energie.md](glossaire/06-repartition-materiel-et-energie.md) | 209 |
| **7.** Mesure, qualité et méthode expérimentale | [07-mesure-qualite-et-methode-experimentale.md](glossaire/07-mesure-qualite-et-methode-experimentale.md) | 154 |
| **8.** Points relevés, non corrigés | [08-points-releves-non-corriges.md](glossaire/08-points-releves-non-corriges.md) | 153 |
| **9.** Sources externes citées | [09-sources-externes-citees.md](glossaire/09-sources-externes-citees.md) | 79 |
| **10.** Le pont linguistico-sémantique — le vocabulaire de l'émulation | [10-le-pont-linguistico-semantique-le-vocabu.md](glossaire/10-le-pont-linguistico-semantique-le-vocabu.md) | 514 |
| **11.** Sources externes ajoutées par le §10 | [11-sources-externes-ajoutees-par-le-10.md](glossaire/11-sources-externes-ajoutees-par-le-10.md) | 50 |

> **Les fiches par entrée.** L'index complet est [`glossaire/README.md`](glossaire/README.md) :
> **289 entrées**, une **fiche courte** par entrée dans [`glossaire/entrees/`](glossaire/entrees/), et
> un manifeste [`glossaire/index.json`](glossaire/index.json) pour docwatch. Les définitions complètes
> restent dans les 11 familles ci-dessus ; une fiche est une **carte**, pas une copie.
