# Les parcours de lecture — cinq profils, cinq chemins, un seul corpus

> **Ce que ce document est.** Le **guidon** de la documentation : cinq **profils de lecteurs**, et
> pour chacun un **chemin court** qui couvre la théorie dont il a besoin — sans lire les 38 documents
> de théorie ni les 335 fiches du glossaire. Un document de théorie n'appartient qu'à **un** parcours
> principal ; les autres le citent, ils ne le réécrivent pas.

## Le principe : trois couches, pas trente documents

| couche | ce qu'elle porte | où elle vit |
|---|---|---|
| **le récit** | pourquoi, pour qui, ce que ça change — **une** page | [`../..//README.md`](../../README.md) · [la vision](vision.md) |
| **les parcours** (ce document) | le chemin de **chaque profil** | ici |
| **les références** | le détail, les chiffres, les mesures | [`synthese/`](synthese/index.md) · [`glossaire.md`](glossaire.md) · [`../../reports/`](../../reports/README.md) |

**La règle de non-redondance.** Un fait vit **une fois** ; les autres documents le **citent** (un lien,
pas une copie). Si deux documents disent la même chose, l'un des deux est en trop : on le supprime ou
on le réduit à un renvoi.

## Profil 1 — Le curieux : « c'est quoi, ce projet ? » (20 min)

**Le chemin** : [le README](../../README.md) → [la vision](vision.md) → [la vue d'ensemble en une image](synthese/schemas/vue-ensemble.svg).

**Ce qu'il couvre** : le problème, l'idée (les faits, le bus), ce que ça change, ce que ce n'est pas,
l'état du produit (l'analyse de texte hors ligne).

**Ce qu'il ne lit pas** : la méthode, les chiffres, les portes. C'est volontaire.

## Profil 2 — L'utilisateur : « je veux analyser un texte » (15 min)

**Le chemin** : [le démarrage produit](../produit/demarrage.md) → [la notice du produit](../produit/README.md) → [les exemples vérifiés](../produit/exemples.md).

**Ce qu'il couvre** : l'installation, les cinq commandes (`analyser`, `evaluer`, `rejouer`,
`restituer`, `generer`), le format JSON, les codes de sortie, les limites mesurées.

**Ce qu'il ne lit pas** : le moteur, le natif, la théorie. Le produit se juge sur la sortie.

## Profil 3 — L'ingénieur : « comment c'est construit ? » (2 h)

**Le chemin** : [l'architecture native](architecture-native.md) → [le traité du modèle natif](modele-natif.md) → [le format DRVF](../implantation/format-flux.md) → [le format DRVM](modele-natif.md#5-drvm--le-conteneur) → [les grappes](../implantation/format-clusters.md).

**Ce qu'il couvre** : les trois niveaux (surface, RSN, pensée), le bus, le graphe, le conteneur DRVM,
le protocole réseau v5, le découpage en grappes, l'exécution (push/pull, GPU/CPU/FPGA).

**Ce qu'il ne lit pas** : la méthode expérimentale, les résultats détaillés — sauf quand il en a besoin.

## Profil 4 — Le chercheur : « qu'est-ce que vous avez mesuré ? » (1 h)

**Le chemin** : [la synthèse en huit chapitres](synthese/index.md) → [les fiches de résultats](../../reports/README.md) → [la méthode](../methode/resultats.md) → [la non-régression](../pilotage/references-non-regression.md).

**Ce qu'il couvre** : les six résultats (traduction, raisonnement, les deux espaces de langue, le fil
d'une histoire, XNLI), les contrôles négatifs, les portes, ce qui pourrait rendre chaque résultat faux.

**Ce qu'il ne lit pas** : le produit, le démarrage. Il vient pour les mesures.

## Profil 5 — L'agent : « je dois agir sur le dépôt » (10 min)

**Le chemin** : [`AGENTS.md`](../../AGENTS.md) → [l'état courant](../pilotage/en-cours.md) → [la roadmap](../pilotage/roadmap.md) → [le document de sa tâche](../README.md#la-carte-de-la-documentation).

**Ce qu'il couvre** : les 12 règles, l'état daté, les chantiers, la file « jamais en attente », le
routage par tâche.

**Ce qu'il ne lit pas** : la théorie entière — il ne charge que le document de sa tâche.

## La carte des documents (ce qui reste)

**Assez de théorie pour tout couvrir, en 9 documents** :

| # | document | pour qui | mots |
|---|---|---|---:|
| 1 | [`vision.md`](vision.md) — le cœur, les cinq axes | 1, 2, 3, 4, 5 | 1 400 |
| 2 | [`architecture-native.md`](architecture-native.md) — le format et le modèle | 3 | 1 200 |
| 3 | [`modele-natif.md`](modele-natif.md) — le traité (trois niveaux, bus, graphe, DRVM) | 3 | 7 300 |
| 3 bis | [`rsn-3-niveaux.md`](rsn-3-niveaux.md) — la RSN (noyau, faits, affirmations) | 3, 4 | 1 700 |
| 3 ter | [`rsn-interface.md`](rsn-interface.md) — les cinq verbes, la substitution | 3 | 1 600 |
| 4 | [`synthese/`](synthese/index.md) — les huit chapitres (la théorie en récit) | 4 | 8 000 |
| 5 | [`protocole-semantique.md`](protocole-semantique.md) — le sens, le rejeu | 3, 4 | 600 |
| 6 | [`jeux-symboliques.md`](jeux-symboliques.md) — le raisonnement symbolique | 3, 4 | 900 |
| 7 | [`pensee-iterative.md`](pensee-iterative.md) — l'itération | 3, 4 | 500 |
| 8 | [`genealogie-des-langues.md`](genealogie-des-langues.md) — les 71 langues | 4 | 700 |
| 9 | [`glossaire.md`](glossaire.md) — les définitions (335 fiches) | tous, en consultation | 28 000 |

**Les documents transversaux** (pas de la théorie, mais utiles au chemin) :
[`carte.md`](carte.md) (l'index), [`histoire.md`](histoire.md) (le nom), [`glossaire.md`](glossaire.md)
(les mots), [`lecture-rapide.md`](lecture-rapide.md) (le backlog).

## Comment on tient la non-redondance

1. **Un fait, un document.** Le chiffre vit dans `reports/` ; le concept dans `docs/theorie/` ; l'état
   dans `en-cours`. Un document qui recopie un chiffre le fait **citer**.
2. **Un document, un parcours principal.** Le tableau ci-dessus dit lequel.
3. **La revue le vérifie** : `python3 tools/revue_documentation.py` signale les doublons de titre et
   les documents orphelins ; `bash tools/porte-tableaux.sh` vérifie que tout est lié.
4. **Quand un document grossit**, on le découpe par **question**, pas par **public** : un lecteur qui
   change de profil ne doit pas changer de document.

## Les limites

- Ce document **décrit** l'organisation ; il ne la **force** pas. Les documents existants qui
  débordent (le `modele-natif.md` à 7 300 mots, la `synthese/` à 8 000) restent à découper — c'est le
  chantier de fond, pas de ce guide.
- Les **profils** se recoupent : un ingénieur peut vouloir le produit, un curieux peut lire la
  synthèse. Les chemins sont des **raccourcis**, pas des frontières.
