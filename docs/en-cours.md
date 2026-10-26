2026-10-26

# En ce moment

**Mis à jour : 2026-10-26, 14 h 30 HAE (heure locale, EDT).**

> Cette page dit **où l'on va, ce qui est en cours, où l'on en est, et ce qu'il reste** aux trois horizons. Les
> détails — chaque chiffre, chaque fiche — sont dans [`reports/`](../reports/), la théorie dans
> [`synthese/`](synthese/index.md), le plan dans [`roadmap.md`](roadmap.md). **Ici, on ne garde que l'actualité.**

## Où l'on va (l'objectif final)

**Démontrer que la structure bat la taille, et construire le moteur qui rend cette structure observable,
décomposable, répartissable et rejouable.**

Deux programmes : le **moteur** (les flux, les cinq axes) et l'**intelligence** (l'entrée-sortie linguistique, puis
la pensée abstraite jugée sur des **opérations** — l'étage 2 ne se bâtit pas sur une entrée-sortie qui n'est pas
fiable). La thèse n'est plus une hypothèse : **la sonde est plate dès le 1,5 B** (0,7256 / 0,7269 / 0,7189), **le
pont plafonne à 0,87**, et à profondeur fixe le 14 B est **dernier** (0,4833) — dix fois la taille pour +0,001.
Voir [`vision.md`](vision.md) et [`mission.md`](agent/mission.md).

## Ce qui est en cours (l'actualité du 26/10)

**La nouvelle phase**, après la révision de la raison d'être, de la stratégie et du plan :

1. **A7 la grappe déportée** : la couche exécutée ailleurs rend **le même chiffre** (`porte-topologie`, 92 s,
   42.5477), le flux coûte **1 608 octets/flux**, et la **grappe intra-couche** (le top-1024, 21 % des neurones FFN)
   rend la **même perplexité** ; et la **grappe déportée** (A7.4 : le flux v2 coûte **4,22× moins**, les chiffres
   identiques) — **A7 est complète**.
2. **B4 les opérateurs abstraits** : **B4.1** (la négation n'est pas une direction : flip 0,4148) ; **B4.2** (elle
   est **apprenable** — 0,7042 en réentraînant — mais **pas transférable**) ; **B4.3** (les deux opérations — l'identité
   et la négation — **coexistent** dans un seul opérateur : 0,7749/0,6977 — un **sous-espace**, pas une direction) ;
   **B4.4** (la **composition échoue** : le nié du nié ne revient pas, 0,5691 — ce n'est pas une **algèbre**) ;
   **B4.5** (elle **s'apprend**, faiblement : 0,6174 — *rien ne se compose gratuitement*) ; **B4.6** (le LoRA de la
   négation **inverse** la lecture : 0,2283 = 1 − 0,7717 — un **négatif** de plus, cohérent avec la géométrie de B4.2).
   **B4 est close.**
3. **A8 l'ordonnanceur place et perte** : le terme de perte est **codé et testé** (`choisir_avec_perte`, 3 tests)
   et la **règle est branchée** (A8.3, **opt-in** `DRAVE_PERTE_MAX` : elle rend le choix de la main, 30,7286 des deux côtés).
4. **B5/B6 les jeux symboliques** : la **RSN-jeu** (morpion, échecs, dames, go, cartes) et la **logique de la
   pensée**. Le corpus de 112 surfaces est couvert à **100 % au niveau 4**, les **33/33** paires équivalentes sont
   invariantes, les **8** groupes négatifs ne collisionnent pas ; la restitution est **112/112** et la perturbation
   **112/112**. Les règles sont justes (perft échecs six positions, dames 1→6), les **3/3** mats en un sont trouvés,
   la recherche des dames gagne **20/20** contre le joueur sans recherche, la politique des cartes fait **79,7 %**
   contre le hasard, et la **pensée est invariante 5/5**. Le MCTS du go est **faible à 60 playouts (1/3)** : négatif
   nommé, pas caché.
5. **B7/B8 les langues et les maîtres** : le **lexique multilingue** couvre **35 concepts** dans **71 langues**
   (**1 433 couples**, **32 langues fortes**) ; le corpus multilingue de **449 surfaces** est lu à **100 %** au
   niveau 4, les **11/11** paires sont invariantes, la permutation des libellés laisse **12/275** items forts
   (le sens s'effondre), la notation est lue **5 112/5 112** dans les 71 langues et les noms de jeux sont
   détectés **315/315**. Côté maîtres, **17 principes**, **9 sources**, **3 parties** : le premier coup des
   échecs passe de **Nc3** à **d4**, le livre tient **10/10**, les mats restent **3/3** ; les dames font
   **10 victoires, 10 nulles, 0 défaite** ; le go 9×9 passe de **3/10** à **10/10** coups de 3e/4e ligne. Deux
   **négatifs nommés** : l'accord avec le coup du maître ne bouge pas (**42/101** contre **41/101**) et la
   politique du whist **perd** contre la base (**44,7 %** contre **51,0 %**).

6. **B9 le banc externe** : **DeepSeek** (`deepseek-flash`) sert **310/310** prompts publics (300
   traductions UDHR, 30 articles × 10 langues, 10 jeux) ; **34 112** tokens d'entrée, **32 436** de
   sortie, **511,1 s** ; chrF **82,82** contre un **plancher 15,64** (espagnol 99,28, russe 98,86,
   français 96,58, italien 92,87, allemand 90,50 ; **hindi 58,45**, **swahili 54,83**). Le pilote à
   60 prompts surestimait l'allemand (99,42) et le chinois (87,70) : c'est le 30 articles qui fait
   foi. Côté natif, `route` tourne sur **`cuda`** ; la distillation à **310 exemples** (271/39, 500 pas,
   3 graines) a une **transition entre 9,23 M et 9,96 M** : **4,04 M** négatif (contrôle 2,7510 contre
   2,7709) ; **9,23 M** transitoire (moyenne +0,83 %, **1 graine/3**) ; **9,96 M** 3/3 (2,7389 contre
   2,7881, 1,76 %) ; **10,70 M** (1,65 %), **16,02 M** (1,92 %) et **22,54 M** (1,74 %) confirment.
   Le **masque calibré** est **quasi égal** à 4,04 M (2,7335 contre 2,7340, **0,02 %**) et à 10,70 M
   (2,7970 contre 2,7928, **0,15 %**) : pas de gain établi. La prochaine action est de resserrer la
   transition et de porter le masque dans le trainer.

**Ce que la journée a établi** : la **carte du raisonnement naturel** est close (trois courbes complètes, les pics
tardifs, la sonde qui sature dès le 1,5 B) ; **B4** est close — l'état porte les opérations, il ne les calcule pas
(0,4148 → 0,7042 → 0,7749/0,6977 → 0,5691 → 0,6174) ; **A7** est complète (le relais 42,5477, le flux 1 608
octets, la grappe exacte à 21 %) ; **A8** est branchée en **opt-in** (la règle rend le choix de la main) ; **les trois
passes** du 24/10 (10 h 53, 19 h 04, 21 h 35) sont **45/47** (les deux structurels seuls, aucun rouge nouveau,
**toutes les références stables**) ; celle du **25/10 à 04 h 51** est **44/2** (46 entrées, les **mêmes deux
structurelles**, et **aucune porte cassée par les instruments de C3.2**) ; celle du **25/10 à 22 h 18** est **45/3** (48 entrées ; les deux structurelles et `porte-homeostasie`, dont le LoRA de référence **temporaire** manquait — régénéré, la porte **repasse** → **46/2**) ; celle du **26/10 à 09 h 40** est **46/2** (48 entrées ; `porte-jeux` **étendue** verte, `porte-homeostasie` **verte**, seules les deux structurelles) ; **DiaBLa** au 3 B (+38,1/+41,3) ; le **14 B l24** était déjà mesuré (0,6305/0,8153) ; **C3.2 est fait** : un module de restitution **par famille**, et **4 familles sur 5
au-dessus de la référence** (de 14,7 % à 100 %) ; **B5/B6** sont mesurés — **112 items**, **100 %** au niveau 4,
**33/33** paires invariantes, **0 collision**, restitution **112/112**, perft des échecs et des dames exact,
**3/3** mats, **20/20** dames, politique des cartes **79,7 %**, pensée invariante **5/5** ; **B7/B8** sont
mesurés — **71 langues**, **449/449**, **11/11**, permutation **12/275**, notation **5 112/5 112** ; les
maîtres changent l'ouverture (**d4**), tiennent le livre (**10/10**), gagnent au go 9×9 (**10/10** contre
**3/10**), ne perdent pas aux dames (**0 défaite**) et **perdent aux cartes** (**44,7 %** contre **51,0 %**) ; **B9**
sort le langage des GPU : **DeepSeek** **310/310**, chrF **82,82** contre **15,64** ; la distillation native a
une **transition entre 9,23 et 9,96 M** — négative à **4,04 M**, transitoire à **9,23 M**, positive **3/3** à
**9,96 M** (1,76 %), **10,70 M** (1,65 %), **16,02 M** (1,92 %), **22,54 M** (1,74 %) et **26,99 M**
(**2,93 %**) ; **31,63 M**/500 pas quasi égal (0,27 %), **31,63 M**/1 000 pas 1,41 % ; **610 exemples / 20 langues** :
   3,71 % (3/3) à **500 pas**, **1,29 % à 750** (2/3), **−0,49 % à 1 000** (contrôle) ; **910 ex. /
   30 langues** : contrôle +0,23 %, 1/3 — l'effet se **dilue** et la fenêtre se **referme** ; la perte masquée
calibrée est **quasi égale** à 4,04 M (0,02 %) et 10,70 M (0,15 %).

## Où l'on en est (les chiffres qui comptent)

| | |
|---|---:|
| mesures de la fiche principale | **173** |
| portes (passe complète) | **49** — 47 vertes, 2 structurels (26/10 14 h 30 ; `porte-deepseek` incluse, `porte-jeux` verte) |
| porte-deepseek | **verte hors réseau** (20 tests, dry-run), **incluse dans la passe** |
| fiches / JSON de résultats | **164** / **236** |
| la sonde, au pic du 1,5 B | **0,810** (DACCORD l22) · **0,7256** (XNLI) |
| le pont, au pic du 14 B | **0,8715** (l36) — il plafonne à 0,87 |
| le KV int8 tardif / le 4 bits de la tête | **+0,03 %** / **+10 %** (reverté) |
| la sémantique des jeux (B5/B6) | **112 items, 100 % au niveau 4, 33/33 paires** |
| la sémantique des jeux, 71 langues (B7) | **71 langues, 35 concepts, 449/449, 11/11** |
| les principes des maîtres (B8) | **d4, livre 10/10, go 9×9 10/10, dames 0 défaite, cartes 44,7 % (négatif)** |
| le banc externe (B9) | **DeepSeek 310/310, chrF 82,82 contre 15,64 ; 610/20 : 3,71 % à 500 pas, 1,29 % à 750, −0,49 % à 1 000 ; 910/30 ne paie pas ; masque quasi égal** |

Le détail de la carte du raisonnement : [05](synthese/05-la-pensee-sans-verbaliser.md) et sa
[synthèse](../reports/rapport-carte-raisonnement-naturel.md).

## Les sept chantiers, en une ligne chacun

| chantier | état |
|---|---|
| **C1** corpus et généalogie | ✅ fait (UDHR 448 langues, Glottolog) |
| **C2** traduction | ✅ mesuré (le juge post-cutoff, le plancher, la marge) |
| **C3** restitution | ✅ mesuré (85 % pour un modèle spécialisé, détruite à 10 langues) ; **C3.2 fait** : un module par famille, **4 familles sur 5 au-dessus de la référence** (de 14,7 % à 100 %) |
| **C4** dialectes et styles | ✅ mesuré (lisibles ; l'époque reste à contrôler) |
| **C5** qualité par domaine | ✅ les **six registres** + le **dialogue spontané** (DiaBLa) |
| **C6** documentation | ✅ fait (l'inventaire, la revue, les portes) |
| **C7** pensée abstraite | ✅ **mesuré** — la carte est faite (l'état porte le raisonnement, le pont l'aligne à 0,87, le plan résiste), **B4 est close** (les six mesures) et **B5/B6** sont mesurés (les jeux) |

**B5/B6 — les jeux symboliques** (hors des sept chantiers C) : ✅ **mesuré** — la RSN-jeu et la logique des
cinq jeux, **112 items**, **100 %** au niveau 4, **33/33** paires, **0 collision** ; perft, mats, dames,
politique et invariance **5/5**. Concept : [`jeux-symboliques.md`](jeux-symboliques.md) ; fiche :
[`rapport-jeux-symboliques.md`](../reports/rapport-jeux-symboliques.md).

## Ce qui reste, aux trois horizons

**Court terme — les prochaines lignes**
1. **Aucune ligne non bloquée du plan n'est ouverte** : A7, B4, A8, C3.2 et B5/B6 sont mesurés. Ce qui reste est
   **nommé** (ci-dessous) ou **hors plan** (corpus externe des jeux, MCTS assez budgété, portage Rust, 9 familles de
   C3, comprendre l'indo-européen à 14,7 %).

**Moyen terme**
- **Les suites des jeux, hors plan** : un corpus **externe**, la détection avec contexte, le **ko positionnel**
  complet, un **MCTS budgété** pour être jugé, et le **portage Rust** du contrat RSN.
- **C3** : les **9 familles** au lieu de 5, et comprendre l'indo-européen à **14,7 %**.
- **B1.5 la prose scientifique** : bloquée, pas de corpus parallèle humain.
- Le **FPGA** (A5.4, le matériel), la **démonstration distante** (A3.4, le compte Colab), le **MoE** (A6.2, pas de
  modèle local).

**Objectif final**
- **L'intelligence** : une entrée-sortie **fiable** (étage 1, tenu : six registres, 24 langues, le dialogue) puis une
  **pensée abstraite indépendante de la langue**, jugée sur des **opérations** (étage 2 : la carte est faite, **B4 est close**, **B5/B6** sont mesurés).
- **Le moteur** : un modèle **décomposable** (la grappe), **répartissable** (le relais, fait), **observable** (la
  trace, le diff) et **rejouable** — la vision, tenue par ses mesures.

## Les questions ouvertes (consolidées ici, jamais bloquantes)

- **Bloquées par une ressource** : **B1.5** (le corpus d'articles humain), **A3.4** (le compte Colab), **A5.4** (la
  carte Stratix V), **A6.2** (un MoE local).
- **Ouvertes sans blocage** : le **pic du 32 B** (10-20 h en 4 bits, nommé, non forcé — la décision est humaine) ;
  et les **limites nommées des jeux** — la détection reste ambiguë sur les cases seules (`A1`, `E4`, `d4`), le go
  est en **ko simple**, le MCTS est faible à 60 playouts (1/3), et le contrat RSN n'est **pas porté** dans le moteur
  Rust.
- **Tranchée** : les **styles à époque contrôlée** — C4 est **mesuré** (les dialectes sont lisibles) ; ce qui reste est
  de **contrôler la date** dans tout test de style (la leçon Panini : la surface capte +0,138, la filiation +0,049),
  et c'est une **règle de méthode**, pas une ligne de plan.

## La carte de la documentation

[`carte.md`](carte.md) — **la carte des sujets** : un lien par fichier ; [`AGENTS.md`](../AGENTS.md) — la mission et les règles ; [`docs/README.md`](README.md) — l'inventaire ;
[`roadmap.md`](roadmap.md) — le plan et la file « jamais en attente » ; [`synthese/index.md`](synthese/index.md) — la
théorie ; [`jeux-symboliques.md`](jeux-symboliques.md) — **les jeux** (surface → RSN → pensée) ; [`reports/`](../reports/) et [`journal/`](../journal/) — les résultats et le récit.
