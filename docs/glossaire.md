# Glossaire raisonné de Drave

Ce document explique **tout le vocabulaire** employé dans `docs/` (18 documents) et
`reports/` (60 rapports, plus 9 fichiers dans `sprints/`), pour quelqu'un qui ne
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

**Périmètre.** `docs/` (18 documents) et `reports/` (60 rapports) ; les 9 fichiers
de `sprints/` sont couverts pour leur vocabulaire propre (boxing, cérémonie,
porte). Le code est cité pour dire *où* un terme est utilisé (`drave-core/src/`,
`tools/`), mais le glossaire ne décrit pas le code ligne à ligne. Les fichiers
`README.md`, `REPRISE.md` et `Qtrinet-bootstrap.md` sont à la racine, hors
périmètre : ils sont signalés quand ils portent un chiffre utilisé partout.

---

## Parcours de lecture conseillé

**Si tu ne lis qu'un document, lis `docs/vision.md`** (279 lignes) : c'est la
vision — des listes d'activation plutôt que des matrices, cinq axes, ce que le
projet n'est pas, et le nom. Tout le reste du dépôt en découle.

Ensuite, dans cet ordre :

1. **`docs/histoire.md`** (78 lignes) — pourquoi le projet s'appelait Qtrinet et
   s'appelle Drave, et la table de conversion des anciens noms de variables. À
   lire tôt : tous les rapports antérieurs au 30/09/2026 emploient encore
   « Qtrinet », `QT_*` et `qtrinet-core`.
2. **`docs/roadmap.md`** (311 lignes) — l'état réel de chaque chantier, phase par
   phase, avec les chiffres et leur date. C'est le document qui dit ce qui est
   fait (✅), en cours (🔬), à faire (⏳) ou bloqué (🧱).
3. **`docs/format-flux.md`** (188 lignes) — le format `DRVF` : ce qu'est une trace,
   comment elle se relit, et le protocole réseau **v5** avec ses cinq modes. Le
   cœur technique du projet est là.
4. **`docs/sprints.md`** (75 lignes) — comment le travail est découpé (sprints de
   2 h), ce qu'est une « porte », une rétrospective, un engagement de fin de
   sprint. Indispensable pour comprendre le ton des rapports.
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
9. **`docs/plan-deepseek41-complet.md`** — le chantier en cours : exécuter un
   modèle réel (V4.1) **en listes**, avec ses deux portes (correction et Drave).

Pour aller plus loin : `docs/programme-recherche.md` (la thèse et ses critères
d'arrêt), `docs/comparaison-spiking.md` (ce que les réseaux à spikes changent),
`docs/plan-mla-vision.md` (attention latente et vision), et — quand un chiffre
semble contradictoire — `reports/rapport-coherence-docs-2.md`, l'audit qui recense
les affirmations périmées du corpus.

À la racine, `README.md` (36 ko) donne l'état général et `REPRISE.md` (81 ko) le
journal de reprise détaillé ; ils emploient le même vocabulaire que ce glossaire.

---


## Les onze familles

Le glossaire fait **2 274 lignes** : il est découpé en **onze familles**, chacune atteignable
directement. Les liens vers ce fichier continuent de fonctionner.

| famille | fichier | lignes |
|---|---|---:|
| **1.** 1. Le projet, ses noms, sa méthode | [01-le-projet-ses-noms-sa-methode.md](glossaire/01-le-projet-ses-noms-sa-methode.md) | 177 |
| **2.** 2. Modèles et architectures | [02-modeles-et-architectures.md](glossaire/02-modeles-et-architectures.md) | 357 |
| **3.** 3. Formats, quantification, encodage | [03-formats-quantification-encodage.md](glossaire/03-formats-quantification-encodage.md) | 189 |
| **4.** 4. Le moteur Drave : exécution, structures, outils | [04-le-moteur-drave-execution-structures-out.md](glossaire/04-le-moteur-drave-execution-structures-out.md) | 211 |
| **5.** 5. Flux, protocole et transport | [05-flux-protocole-et-transport.md](glossaire/05-flux-protocole-et-transport.md) | 118 |
| **6.** 6. Répartition, matériel et énergie | [06-repartition-materiel-et-energie.md](glossaire/06-repartition-materiel-et-energie.md) | 203 |
| **7.** 7. Mesure, qualité et méthode expérimentale | [07-mesure-qualite-et-methode-experimentale.md](glossaire/07-mesure-qualite-et-methode-experimentale.md) | 148 |
| **8.** 8. Points relevés, non corrigés | [08-points-releves-non-corriges.md](glossaire/08-points-releves-non-corriges.md) | 147 |
| **9.** 9. Sources externes citées | [09-sources-externes-citees.md](glossaire/09-sources-externes-citees.md) | 73 |
| **10.** 10. Le pont linguistico-sémantique — le vocabulaire de l'émulation | [10-le-pont-linguistico-semantique-le-vocabu.md](glossaire/10-le-pont-linguistico-semantique-le-vocabu.md) | 508 |
| **11.** 11. Sources externes ajoutées par le §10 | [11-sources-externes-ajoutees-par-le-10.md](glossaire/11-sources-externes-ajoutees-par-le-10.md) | 44 |
