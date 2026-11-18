# Session d67a9bb1 — Intérêt pour le FPGA maintenant

> **Journaux :** [le jour](../../2026-11-17/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `d67a9bb1-090e-4f69-baf2-a831c00aa275` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-17 09:50 |
| Durée | 23.4 h |
| Tours | 9 |
| Messages | 356 |
| Appels d'outils | 370 |
| Fichiers touchés | 30 |
| Commandes | 262 |
| Sous-agents | 2 |
| Commits | 18 |
| Compactages de contexte | 0 |

## Objectifs déclarés

- **create** — Ajouter au format DRVM les variantes d'implémentation par bloc (`impl` + `contrat {version, tolerance}`), les faire exécuter par les deux moteurs (Rust `native.rs` et numpy `tools/drvm_infere.py`), exposer la provenance dans l'inspecteur et la trace, et livrer une porte `porte-n3-variante` qui prouv
… [260 caractères tronqués]
- **complete** — Ajouter au format DRVM les variantes d'implémentation par bloc (`impl` + `contrat {version, tolerance}`), les faire exécuter par les deux moteurs (Rust `native.rs` et numpy `tools/drvm_infere.py`), exposer la provenance dans l'inspecteur et la trace, et livrer une porte `porte-n3-variante` qui prouv
… [260 caractères tronqués]
- **create** — Rendre `graph.routes` vivant dans le manifeste DRVM : schéma minimal déterministe (route conditionnelle par position vers un profil de bloc `local_mixer`), validation et refus dans les deux lecteurs, exécution par le moteur Rust (les deux moteurs refusent ce qu'ils n'exécutent pas), provenance dans 
… [306 caractères tronqués]
- **complete** — Rendre `graph.routes` vivant dans le manifeste DRVM : schéma minimal déterministe (route conditionnelle par position vers un profil de bloc `local_mixer`), validation et refus dans les deux lecteurs, exécution par le moteur Rust (les deux moteurs refusent ce qu'ils n'exécutent pas), provenance dans 
… [306 caractères tronqués]
- **create** — Livrer `porte-n3-moteurs` : prouver que les deux moteurs du même manifeste DRVM (Rust `native.rs` et numpy `drvm_infere.py`) rendent les mêmes logits dans la tolérance déclarée, pour les profils `defaut` et `bloque`, avec les contrôles négatifs qui rendent le comparateur non vide (une différence rée
… [164 caractères tronqués]
- **complete** — Livrer `porte-n3-moteurs` : prouver que les deux moteurs du même manifeste DRVM (Rust `native.rs` et numpy `drvm_infere.py`) rendent les mêmes logits dans la tolérance déclarée, pour les profils `defaut` et `bloque`, avec les contrôles négatifs qui rendent le comparateur non vide (une différence rée
… [164 caractères tronqués]
- **create** — Ajouter le profil d'implémentation `court` (fenêtre d'attention divisée par 4) au format DRVM et au moteur Rust, prouver qu'il n'est PAS substituable (logits différents) et qu'il PAIE en temps sur une charge dominée par l'attention, mesurer son coût de qualité (perplexité) sur un modèle entraîné, re
… [221 caractères tronqués]
- **complete** — Ajouter le profil d'implémentation `court` (fenêtre d'attention divisée par 4) au format DRVM et au moteur Rust, prouver qu'il n'est PAS substituable (logits différents) et qu'il PAIE en temps sur une charge dominée par l'attention, mesurer son coût de qualité (perplexité) sur un modèle entraîné, re
… [221 caractères tronqués]
- **create** — De 00 h 30 à 16 h le 18/11, en charge de TOUS les chantiers, machine dédiée : (1) épingler le corpus natif (sha256, manifeste, fiche) et lancer l'entraînement 100 M sur GPU avec bancs aux checkpoints ; (2) mesurer la grammaticalité du 100 M ; (3) instruire A2.6 (experts et tête) ; (4) exécuter les l
… [191 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — aurait-on un intérêt pour le FPGA maintenant?

**Tour 2** — j'ai 4 cartes FPGA Stratix V dans un mining rig. J'ai les cables pour les connecter en boucle de 40gbps. l'ensemble serait accessible via un cable ethernet dédié

**Tour 3** — considérant que certains modules on des équivalents heuristiques ou logique floue, peut-on ajouter les différentes options d'implémentation pour chaque module et avoir un routage flexible entre les modules

**Tour 4** — vas-y

**Tour 5** — go, continue tant qu'on est sur le tarif réduit de DeepSeek (jour ici, nuit en chine)

**Tour 6** — vas-y avec les prochains chantiers, continue tant qu'on est sur le tarif réduit de DeepSeek (jour ici, nuit en chine)

**Tour 7** — le rig n'est pas prêt (c'est un chantier en soit) continue sur d'autre chose

**Tour 8** — on est en soirée, donc tarif de jour en chine. fais des tâches qui demandent peu de réflexion et beaucoup de calcul local.

**Tour 9** — commit et push, puis sois autonome jusqu'à 16h. Tu est en charge de tous les chantiers. Coordonne-les et utilise beaucoup de subagents au besoin

## 2. Déroulé, étape par étape

### Tour 1 — aurait-on un intérêt pour le FPGA maintenant?

*15 appels d'outils.* Actions notables :

- grep
- bash — List repository root and pilotage docs
- read
- bash — Check FPGA card presence and recent commits
- bash — Check date and USB/PCI device list
- bash — Inspect sibling FPGA repo for DDR3 capacity and PCIe status
- bash — Check whether the Stratix V card is visible on PCIe
- bash — Read resource/method notes listing the FPGA
- bash — Check FPGA device nodes and November journal mentions
- bash — Read roadmap blocked-resource table
- bash — Date the FPGA verdict reports and read scaling argument

**Synthèse produite :**

⏵ Vérification du matériel et des chiffres FPGA avant réponse

**Réponse courte : non — et la seule chose qui a changé, c'est que la carte n'est plus là.**

Vérifié à l'instant sur la machine (17/11, 09 h 51) : **aucun device Altera sur PCIe ni sur USB**, pas de `/dev/ttyUSB*`. La Stratix V n'est branchée sur rien. A5.4 n'est donc pas « bloquée administrativement » ([roadmap](docs/pilotage/roadmap.md), [fiche](docs/pilotage/backlog/A5.4-fpga.md)) : elle est bloquée physiquement, en plus du reste.

**Pourquoi le verdict de septembre/octobre tient** — le mur est la mémoire, pas le calcul :

| même flux, 0,5 B Q8, 1 jeton = 352,8 M événements = 0,7 Go de listes | tok/s |
|---|---|
| FPGA, 1 carte, plafond **DDR3 9,66 Go/s** (72 ms/jeton, quoi que fasse la logique) | **13,7** *projeté* |
| CPU, mode push, **mesuré** | **15,6** |
| CPU, noyau dense int8, **mesuré** | **36,4** |
| GPU, listes / dense | **51 / ~770** |

La carte est **sous le CPU déjà mesuré**, dans son propre mode de prédilection. Elle lit 1/3 de la RAM et 1/40 de la VRAM ; ses 4 Go de DDR3 sont la mémoire la plus petite et la plus lente de la machine. Et la mesure de [architecture-mémoire §14](reports/rapport-architecture-memoire.md) n'a pas bougé : lire une couche coûte 18× son calcul — un accélérateur de calcul sur un chemin où le calcul pèse 5 % ne peut rien gagner.

**Ce qui a changé depuis, et qui empire le cas** : les modèles ont grossi (engram 365 Go mmap, MoE 18,56 Go, cache KV), et tous les murs actuels sont de la **bande passante**. Le seul chantier *compute-bound* de la maison est l'entraînement — or le PE est justement « 176 ALM, **0 DSP**, aucun multiplieur » : l'exact inverse de ce qu'il faut pour du dense fp16. L'AMP GPU à 2,4× le CPU ne se transpose pas.

**Les trois seuls intérêts qui restent, et leur prix :**

1. **Énergie** : 8,3 nJ/événement *projeté* contre 57 nJ CPU *mesuré* (7×). Aucun budget joules dans la roadmap ; et il faudrait PCIe + contrôleur DDR3 pour seulement le mesurer.
2. **Ring 2–4 cartes** : 92,8 tok/s projetés à 4 cartes ([rapport-cpu-aer](reports/rapport-cpu-aer.md)) — le seul argument d'échelle. Prix : 4 cartes, contrôleur DDR3, séquenceur, chemin retour, QSFP+ (rien de tout ça n'existe), pour un modèle 0,5 B que le GPU fait déjà 8× plus vite.
3. **Preuve de portabilité bit-exacte** du format sur un hôte sans multiplieur (l'argument CDC) : à moitié faite (PE + lecteur vérifiés et synthétisés, 309 020 événements), mais la moitié qui reste exige la carte.


… [717 caractères tronqués]

### Tour 2 — j'ai 4 cartes FPGA Stratix V dans un mining rig. J'ai les cables pour les connecter en boucle de 40gbps. l'ensemble sera … [41 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Read Stratix V card specs (QSFP+, PCIe, power)
- bash — Read host diagnostic script and multicard plan
- bash — Read the CPU/AER report assumptions
- bash — Check SSH hosts and known machines
- bash — Look for an existing GPU scatter benchmark
- bash — Check card power and GPU scatter notes

**Synthèse produite :**

⏵ Réponse : ce que 4 cartes + ring changent, et la seule porte qui décide

**Oui — mais pas pour le débit. Pour la seule chose que rien d'autre dans la maison ne fait.**

Ce que tu décris remplit exactement les deux conditions que le dépôt s'était lui-même fixées : « le FPGA n'a de sens qu'à partir de **2–4 cartes** » ([rapport-cpu-aer](reports/rapport-cpu-aer.md), verdict 4) et « le ring 40G n'a de sens que pour des **cartes déportées** » ([multicartes](docs/../FPGA-Stratix-V/docs/multicartes.md) §3). Un mining rig à 4 cartes, relié en boucle QSFP+ et accessible par Ethernet, c'est la topologie que la doc décrivait sans l'avoir.

**Ce que 4 cartes donnent (chiffres du dépôt)**

| | 4 cartes | comparaison |
|---|---|---|
| mémoire | **16 Go** (4 × 4 Go DDR3) | = 1 GPU ; 32 Go en tout sur la machine |
| bande passante agrégée | **38,6 Go/s** | CPU 28,7 · GPU 380 |
| débit d'événements | **19,3 G év/s** *projeté* (4 × 4,83) | CPU 5,3 mesuré · 1 GPU 18,1 mesuré (dispersion) |
| ring | **4,8 Go/s par lien** | sous la DDR3 d'une carte (9,66) → **les poids ne doivent jamais traverser le ring** |
| énergie | ~8,3 nJ/év *projeté* → ~160 W | GPU 12,7 nJ → seulement **1,5×**, pas 7× (les 7× sont contre le CPU) |

Deux conséquences structurelles : (1) seules les **activations** traversent le ring — 3,5 Mo par jeton, 0,7 ms par saut, négligeable devant 18 ms de lecture ; (2) l'**Ethernet dédié ne gêne pas** l'inférence : si les poids restent sur les cartes, seuls les jetons passent (quelques Ko). Et pour un modèle ≤ 4 Go (le 0,5 B Q8), **pas besoin du ring du tout** : 4 cartes en data-parallel = 4 × 13,7 ≈ **55 tok/s**.

**Le hic, et il est décisif.** Le seul avantage de vitesse du FPGA sur le GPU (le 7B à 5 % de densité : 92,8 tok/s projetés à 4 cartes contre ~52 en mode listes) est mesuré contre la **dispersion GPU non optimisée** (`np.add.at`-class, 18,1 G év/s), alors que la VRAM peut lire 380 Go/s. Un noyau scatter à accumulateurs par banc (sans atomiques) est une journée de travail — et s'il dépasse 19,3 G év/s, l'argument de débit du ring meurt et il ne reste que la démonstration. **C'est la porte à franchir avant d'écrire une ligne de RTL.**

**Le prix, sans fard** : les 4 pièces RTL manquantes ([bilan §4](reports/bilan-multi-materiel.md)) restent à faire — contrôleur DDR3 (le ref design UniPHY existe), séquenceur sur 168 matrices, chemin retour accumulateur → liste, opérations non matricielles — plus la chaîne 40G, dont **aucun exemple n'est publié** sur cett
… [1487 caractères tronqués]

### Tour 3 — considérant que certains modules on des équivalents heuristiques ou logique floue, peut-on ajouter les différentes optio … [85 caractères tronqués]

*12 appels d'outils.* Actions notables :

- bash — List source tree and Rust core
- bash — Search vision docs for module substitution and routing
- bash — Read block/contract model in native model doc
- bash — Inspect Rust traits and enums for dispatch
- bash — Check whether manifest routes are implemented
- bash — Read vision on substitutability and roadmap N0
- bash — List CLI flags and check variant provenance in trace
- bash — Check roadmap/backlog routing items and R0.5
- bash — Read DRVM manifest parsing for graph/routes
- bash — Read N3.3a routes report
- bash — Check DRVM writers and unread manifest fields
- job_kill

**Synthèse produite :**

⏵ Réponse : variantes par bloc et routage, ce que le dépôt permet déjà et ce qui manque

**Oui — l'idée est déjà la théorie du dépôt ; ce qui manque, c'est le contrat *exécutable*.**

Trois choses existent déjà : la [vision](docs/theorie/vision.md) (propriété 2 : deux implémentations du même contrat se remplacent sans toucher au bus), le [théorème d'indifférence](docs/theorie/modele-natif.md) (« le mode d'opération est privé », le bus ne voit que des types, un coût et une trace), et le manifeste DRVM qui porte déjà `graph.routes`, `regions`, `heads`, `thought` avec un `kind` en liste fermée et refus des inconnus. `placement.rs` porte même la règle de coût.

**Mais il y a un défaut à corriger avant d'ajouter quoi que ce soit** : le lecteur Rust parse `blocks` et `tensors`, refuse une version ou un `kind` inconnus — puis **ignore silencieusement** `routes`, `regions`, `heads`, `thought`. Un modèle qui déclare ses routes et s'exécute comme si elles n'existaient pas, c'est exactement ce que le doc interdit (« un modèle à moitié compris qui s'exécute quand même est un modèle qui ment »).

**Ce qu'il faut ajouter — trois champs, pas plus** :

```json
{"id":"b0","kind":"local_mixer","impl":"dense","contrat":{"version":1,"tolerance":0.0}}
```
plus, dans la trace : `impl`, `params`, `seed`. Et le coût mesuré par variante (octets, ms, énergie) : c'est tout ce que le consommateur a le droit de voir. Trois couches — **contrat** (public : signature, tolérance, champs de trace), **variantes** (privées : dense, heuristique, floue, API, distante — la techno ne sort jamais du bloc), **route** (sélection, statique par défaut).

**L'avertissement empirique, et c'est le point le plus important** : le routage flexible a **déjà** été essayé ici, quatre fois, et quatre négatifs — R0.5 (routeur extractif/génératif : AUC 0,839, mais transfert **0,819/0,313** contre **0,871/0,373** pour le choix fixe, [rapport](reports/rapport-r07-routeur.md)), puis R06 v1, la cascade v2, le déclencheur, le pipeline. Même diagnostic partout : **un seuil absolu ne transfère pas ; le choix dépend du document**. Donc : les variantes coûtent peu ; le *routeur* coûte cher et a déjà perdu une fois. Il ne s'ajoute pas comme un interrupteur, il se conquiert comme un résultat — avec le choix fixe pour contrôle négatif.

**Les trois pièges à nommer** : (1) **explosion combinatoire** — n blocs × k variantes, donc variantes seulement là où deux implémentations sont *déjà mesurées* ; (2) **non-déterminisme** — 
… [1439 caractères tronqués]

### Tour 4 — vas-y

*68 appels d'outils.* Actions notables :

- bash — Check git state and DRVM-related gates
- bash — Find the routes schema in the docs
- bash — Read the refusal and routes gates
- bash — Find DRVM manifest writers
- read
- bash — Read the DRVM exporter
- bash — Inspect real DRVM manifests
- bash — Check git hooks before committing
- glob
- bash — Compare manifest keys across real DRVM files
- bash — Read GGUF to DRVM manifest construction
- bash — Survey all DRVM manifests for exact key sets
- bash — Check Python test layout and inspect command
- bash — Find existing Python tests and DRVM gates
- … et 43 autres

**Synthèse produite :**

⏵ Récapitulatif du correctif livré et de la suite

**Fait, mesuré, committé — `97579a55`.**

Le défaut était réel : le format DRVM **déclarait** `routes`, `regions`, `heads`, `thought`, `bridge`, et le lecteur Rust n'en lisait **aucun**. Un manifeste avec une route s'exécutait comme si la route n'existait pas — le « modèle qui ment » que `modele-natif.md` interdit. Corrigé dans **les deux lecteurs** (Rust et `tools/drvm.py`), mêmes messages :

```
DRVM invalide : routes non exécutées : 1 route(s) — le lecteur refuse ce qu'il ne sait pas exécuter
```
(exit 3 côté Rust, `DRVMError` côté Python, sur le même fichier)

**Ce qui est verrouillé maintenant** : clés **fermées** aux cinq niveaux (racine, `graph`, bloc, `execution`, `thought`, région) ; région / tête / pont qui nomme un bloc absent → refus nommé ; `thought.steps` négatif ou fractionnaire → refus ; `routes` vide accepté, route déclarée **refusée** ; et `write_drvm` refuse aussi — **un manifeste ne peut plus naître menteur**.

**Le dispositif** (`porte-n3-refus` §4) : 10 cas mutés, les deux lecteurs, mêmes messages ; contrôles négatifs = le DRVM valide passe, l'écriture avec route est refusée, et **les 62 DRVM du disque restent lisibles**.

**Portes** : n3 ×18 **vertes** (11 h 16), `produit`/`document`/`etat`/`poids-creux` **vertes** (11 h 18). Tests Rust **136/137** — la rouge (`tests_vars::DRAVE_POS_DESYNC`) est **préexistante à HEAD**, hors de ce diff. Python : 189 tests, 1 erreur d'import préexistante (`test_bus`, `PYTHONPATH`).

Deux notes de transparence : le hook a balayé le journal de la session active dans le commit (15 fichiers ; c'est son comportement), et `tools/chantier/plan.json` reste non committé (session Pensée).

**Ce que ça débloque pour ta question** — le manifeste est maintenant un contrat vérifié, donc la suite est exactement ton idée, dans cet ordre :

1. `impl` + `contrat {version, tolerance}` par bloc, avec **refus d'une `impl` inconnue** (même mécanique que `kind`) ;
2. **provenance** dans la trace (`impl`, `params`, `seed`) — sans elle, deux variantes sont indistinguables au rejeu ;
3. **table de routes statique** dans `graph.routes` (le champ existe et est déjà contrôlé) — pas de routeur appris avant ;
4. **test d'indifférence** + contrôle négatif : deux implémentations du même contrat → même sortie à la tolérance près ; une impl hors contrat doit **échouer**, sinon le test ne teste rien ;
5. **coût mesuré par variante** (le `placement.rs` a déjà la règle).

Et le garde-fou 
… [290 caractères tronqués]

### Tour 5 — go, continue tant qu'on est sur le tarif réduit de DeepSeek (jour ici, nuit en chine)

*104 appels d'outils.* Actions notables :

- get_goal
- bash — Survey the native engine functions
- create_goal
- read
- bash — Read the drvm-pas-hex command
- bash — Check how the gate count is verified
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drvm.py`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drvm.py`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/native_model.py`
- bash — Add impl constants and Bloc fields
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/drvm.rs`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/drvm.rs`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/drvm.rs`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drvm.py`
- … et 67 autres

**Synthèse produite :**

⏵ Récapitulatif des cinq commits et de l'état du chantier

**Cinq commits, tous verts, tous mesurés.** Le chantier « variantes + routage » est passé d'une idée à un contrat exécuté.

| commit | ce qui est établi | le chiffre |
|---|---|---|
| `97579a55` | le lecteur refuse ce qu'il n'exécute pas (clés fermées, deux lecteurs) | **13 refus nommés**, 62 DRVM relus |
| `20648db7` | substitution = contrat : `impl` + `contrat` par bloc, indifférence mesurée | **4,768e-07** ≤ 1e-4 |
| `337715d1` | le moteur numpy exécute `bloque` et refuse `flou` | **2,831e-07** |
| `49904862` | **les routes sont exécutées** (seuil 0 / 10⁹ / mixte) | **bit-exact / bit-exact / 5,779e-03** |
| `b480a439` | les deux moteurs rendent le même corps, gardé à chaque passe | **3,576e-07 / 2,384e-07** |

**Ce que ça change dans le manifeste** — deux mécanismes, deux usages, désormais séparés :

```json
{"id":"b0","kind":"local_mixer","impl":"bloque","contrat":{"version":0,"tolerance":1e-4}}
{"id":"r0","bloc":"b1","si":{"kind":"position","seuil":512},"alors":"flou","sinon":"defaut"}
```
`impl` = **substitution** (même fonction, autre algorithme → indifférence dans la tolérance). `routes` = **routage** (autre fonction, même signature → la substitution est interdite, et le test doit le dire). Le nom du profil est public (manifeste → hash → trace), l'algorithme est privé, et **chaque moteur refuse ce qu'il n'exécute pas**.

**Trois portes nouvelles** (89 au total) : `porte-n3-variante`, `porte-n3-route`, `porte-n3-moteurs`. Toutes ont un contrôle négatif qui **doit échouer** : `flou` échoue l'indifférence (5,790e-03), le comparateur ne doit pas être aveugle, numpy refuse les routes. La porte des routes a d'ailleurs **trouvé un vrai bug** : l'indice de bloc venait de la position dans `graph.blocks` au lieu du `i` de `b{i}` — la route ne s'appliquait jamais. C'est le bit-exact qui l'a révélé.

**Les limites, écrites dans les fiches** : un modèle, une graine, un pas ; `bloque` n'est **pas plus rapide** ici (0,98–0,99×) ; le coût du routage n'est pas chronométré ; et surtout, **la politique de routage reste une question ouverte** — R0.5 et R06 ont montré quatre fois qu'un seuil global ne transfère pas. La porte prouve le mécanisme, pas qu'il faut router.

**Ce que je ferais ensuite, et pourquoi ce n'est plus du même chantier** : la suite n'est pas un mécanisme de plus, c'est une **politique** qui batte le choix fixe sur un banc (la condition nommée par R0.5 : calibration apprise par document, plus
… [802 caractères tronqués]

### Tour 6 — vas-y avec les prochains chantiers, continue tant qu'on est sur le tarif réduit de DeepSeek (jour ici, nuit en chine)

*36 appels d'outils.* Actions notables :

- create_goal
- bash — Check the native perplexity command
- bash — Add the court profile to the format and engine
- bash — Measure court vs defaut on a synthetic window-dominated model
- bash — Check the court window boundary behaviour
- bash — Inspect the trained model config
- bash — Measure perplexity defaut vs court on the trained model
- bash — Clean timing and a second text for perplexity
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-n3-court.sh`
- bash — Run the court gate
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n3-court.md`
- bash — Update counters and state for the court profile
- bash — Run N3 suite and key gates with court
- bash — Look for an in-distribution corpus
- … et 22 autres

**Synthèse produite :**

⏵ Bilan des trois chantiers de ce tour et de ce qu'ils tranchent

**Trois chantiers de plus, trois commits, et une décision tranchée.**

| commit | chantier | le chiffre |
|---|---|---|
| `de967b7b` | **N3.10 — `court`** : fenêtre divisée par 4, premier profil qui paie | **0,694×** le temps ; PPL **23,7480 → 23,5824** sur 2 048 o ; bit-exact < 64 o, **3,633e-02** au-delà |
| `24cb295e` | **A5.4 — le matériel existe** : 4 cartes + ring 40G + Ethernet | 16 Go, 38,6 Go/s agrégés, 19,3 G év/s projetés |
| `a0d7fa3b` | **P1 — le GPU scatter** : la porte qui décide du FPGA | **29,37 G év/s** sur **une** carte vs **19,3 G** pour **4** |

**Le résultat qui compte : P1 ferme l'argument de débit du FPGA.** Sur la même Quadro, la dispersion avec accumulateurs par bancs fait **29,37 G év/s** (268 M événements, int32 exact) — **1,52× la projection des 4 cartes**. Et le chiffre de référence du bilan (18,1 G) était mou : la même carte fait **25,65 G** avec la simple primitive à atomiques. Deux effets secondaires mesurés : la banque achète de la **contention** (3,2× à O=1024) et **pas** de la bande passante — à O=65 536 elle s'effondre (1,16 G), ce qui est le contrôle négatif du mécanisme. Toutes les méthodes rendent le **même** accumulateur, et le harnais est vérifié contre `np.bincount` (écart 0).

**Ce qu'il reste au FPGA, nommé et plus faible** : l'énergie (**1,5×** projeté sur le GPU, pas 7× — les 7× sont contre le CPU), le déterminisme bit-exact, la capacité (16 Go, égale à un GPU) et la **démonstration du réparti**. La décision de rouvrir A5.4 ne se prend plus sur le débit : elle se prend sur **P2** (le ring tient-il 4,8 Go/s ?) — et P2 demande le rig.

**Sur le routage** : `court` est le premier profil qui donne un arbitrage coût/qualité — mais sur ce modèle entraîné, la fenêtre de 1 024 n'est **pas utilisée** au-delà de 256 (PPL inchangée, ~5 % de temps). Il n'y a donc rien à router *ici* ; la politique demanderait un modèle et un corpus où la fenêtre longue sert, ce que la maison n'a pas encore.

**Où en est le dépôt** : 8 commits sur la journée, **90 portes** (dont 22 N3), **786 fiches**, **877 JSON**, état **1 735 mots**, revue de documentation verte, graphe backlog cohérent. Tests Rust **138/139** — la rouge (`tests_vars`) est préexistante à HEAD. La session N2 a du travail en cours dans l'arbre (`tools/banc_generation.py`, `reports/banc-generation-100m.json`) : je n'y ai pas touché, c'est à elle de le committer.

**Les deux prochaines actions, et leur condit
… [263 caractères tronqués]

### Tour 7 — le rig n'est pas prêt (c'est un chantier en soit) continue sur d'autre chose

*31 appels d'outils.* Actions notables :

- bash — Read the env-var completeness test
- bash — Read VARS_LUES and the source() helper
- bash — Compute the env-var list delta
- bash — Locate the two variables and any documentation table
- bash — Read the end of VARS_LUES
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs`
- bash — Run the Rust tests after the vars fix
- bash — Fix the comment reference and re-run tests
- bash — Commit the env-var test fix
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/bench/drvm_profils.py`
- bash — Simplify the profile bench loop
- bash — Run the profile bench on the trained model
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-profils-modele.md`
- … et 17 autres

**Synthèse produite :**

⏵ Bilan des quatre derniers commits et de la matrice de capacités

**Quatre commits de plus, et la ligne N3 est maintenant close proprement.**

| commit | chantier | le chiffre |
|---|---|---|
| `6d720eaa` | **tests** : `NATIVE_PROFONDEUR` et `POS_DESYNC` déclarées | suite Rust **139/139** |
| `0e5da7bd` | **profils sur le 34 M entraîné** | `bloque` **+0,04 %**, `flou` **+2,09 %**, `court` **−0,70 %** de PPL |
| `7c219067` | **numpy exécute `court`** | parité Rust ↔ numpy **2,980e-07** sur 128 octets |
| `a85da6f3` | **backlog N3** : cinq fiches, étape 5 | **22 portes** (17 au 04/11) |

**La nuance qui compte, et elle est écrite dans la fiche** : le contrat d'indifférence porte sur les **logits** (5e-7, sous 1e-4), **pas sur la perplexité**. `bloque` déplace la PPL de **+0,04 %** — la PPL est une fonction non linéaire de tous les logits, où le décalage s'accumule. Promettre l'invariance de la PPL aurait été un mensonge de plus. À l'inverse, `flou` coûte **+2,09 %** (une dégradation réelle), et `court` **−0,70 %** (la fenêtre de 1 024 n'est pas utilisée au-delà de 256 sur ce modèle). Les temps de cette passe ne sont **pas** interprétables (machine partagée : `bloque`, à coût identique, varie de −17 % à +4 %) — le chiffre de temps valide reste le banc contrôlé (0,694×).

**La matrice de capacités des deux moteurs, désormais explicite** :

| | Rust | numpy |
|---|---|---|
| `defaut`, `bloque`, `court` | ✅ | ✅ (parité 2,98–3,58e-07) |
| `flou` | ✅ | **refusé** (nommé) |
| routes | ✅ (seuil 0/10⁹ bit-exacts) | **refusées** (nommées) |

Chaque moteur déclare ce qu'il exécute et refuse le reste — c'est la règle du format appliquée aux moteurs eux-mêmes.

**Les temps valides, sans bruit** : `court` **0,694×** sur une charge dominée par l'attention (11 passes alternées, CV 3–6 %) ; **29,37 G év/s** pour la dispersion GPU (P1, sur 268 M d'événements, bit-exact contre `np.bincount`).

**Ce que je ne fais pas, et pourquoi** : la politique de routage demanderait un modèle et un corpus où la fenêtre longue **sert** (celui-ci ne l'utilise pas au-delà de 256) ; P2 demanderait le rig (chantier à part entière, comme tu l'as dit) ; `flou` dans numpy serait de la complétude sans usage (il coûte 2 % de PPL et ne gagne rien). Les lignes A2.6 et N2 appartiennent à d'autres sessions.

**État du dépôt** : 12 commits sur la journée, **90 portes**, **787 fiches**, **878 JSON**, état **1 750 mots**, revue de documentation verte, graphe backlog cohérent, tests Rust **139/139**. Le tra
… [340 caractères tronqués]

### Tour 8 — on est en soirée, donc tarif de jour en chine. fais des tâches qui demandent peu de réflexion et beaucoup de calcul loca … [2 caractères tronqués]

*48 appels d'outils.* Actions notables :

- bash — List trained models and their configs
- bash — Batch profile benchmarks on five trained models
- bash — Run the GPU scatter grid across accumulator sizes
- bash — Assemble the GPU scatter grid table
- bash — List and parse the grid JSONs correctly
- bash — Merge the scatter grid into one JSON
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gpu-scatter-grille.md`
- bash — Commit the scatter grid fiche
- bash — Check the profile batch progress
- bash — Check card-to-card variance on both GPUs
- bash — Add the two-GPU control and check batch progress
- bash — Measure Rust vs numpy parity on the real 34M model
- bash — Wait and check batch progress
- bash — Wait for the batch to finish
- … et 32 autres

**Synthèse produite :**

⏵ Bilan des trois gros calculs locaux (grille, cinq modèles, passe complète)

**Trois calculs longs, trois commits, zéro nouvelle rouge.**

**1. La grille du scatter GPU** (`d6e08d6a`) — 5 tailles d'accumulateur × 4 bancs :

| O \ B | atomiques | B=16 | B=64 |
|---:|---:|---:|---:|
| 512 | 4,76 | 28,16 | **28,52** |
| 1 024 | 8,42 | 27,14 | **27,53** |
| 4 096 | 25,18 | 26,51 | **26,57** |
| 16 384 | **26,58** | 26,64 | 2,73 |
| 65 536 | **26,98** | 2,70 | 1,16 |

La banque est un **remède à la contention**, pas un accélérateur : **6,0×** à 512 sorties, 1,06× à 4 096, et elle **se retourne** à 65 536 (le tableau de bancs ne tient plus dans le cache). Les deux cartes donnent le même plateau (25,20 / 25,23 en atomiques). Même le pire cas (25,2 G) reste au-dessus des 19,3 G projetés pour 4 cartes.

**2. Les profils sur cinq modèles entraînés** (`18d49ce7`) — 34,3 M chacun, même texte de 2 055 octets :

| modèle | fenêtre | `bloque` Δ | `flou` Δ | `court` Δ |
|---|---:|---:|---:|---:|
| base-en-34m | 256 | +0,00 % | +1,94 % | +1,46 % |
| base-multi-34m | 256 | +0,00 % | +1,07 % | +3,09 % |
| mix1024-60k | 1 024 | +0,04 % | +2,09 % | −0,70 % |
| propre512-8k | 512 | −0,04 % | +6,99 % | **−12,13 %** |
| rope2048-20k | 2 048 | +0,00 % | +3,09 % | **+4,57 %** |

`bloque` ne biaise pas (±0,04 %, des deux signes) ; `flou` est **toujours** une perte (5/5) ; `court` **change de signe** selon le modèle — le « gratuit » de mix1024 était une exception. Contrôle : sur le vrai modèle, Rust ↔ numpy à **1,526e-05** (≤ 1e-4).

**3. La passe complète** (`e6fa9c0d`) — 90 portes, **87 vertes, 3 rouges**, 116 min de calcul, cumul 6 981 s :
- `indice` (862 s) et `melange` (106 s) : **structurelles**, connues ;
- `sessions` (0 s) : **circonstance** — le mandat `e181ce02` est périmé de 1 896 min, c'est à sa session de rafraîchir son heartbeat ;
- **aucune rouge nouvelle** : les 22 portes N3 (dont les quatre du jour) sont vertes.

J'ai vu au passage le commit `02cc66d4` d'une autre session (`plans-tarif.md`) : il place les tâches API en remisée (11 h 30 → 19 h 30 EST) et le local en pleine — ce lot est exactement dans sa file « locale ».

État : **90 portes**, 789 fiches, 880 JSON, état 1 635 mots, tests Rust **139/139**. La session N2 garde son travail non committé (`tools/banc_generation.py`, `reports/banc-generation-100m.json`) : je n'y touche pas.

### Tour 9 — commit et push, puis sois autonome jusqu'à 16h. Tu est en charge de tous les chantiers. Coordonne-les et utilise beaucou … [24 caractères tronqués]

*50 appels d'outils.* Actions notables :

- bash — Inspect pending work, remote and branch
- bash — Inspect the N2 bench JSON and plan diff
- bash — Read the generation bench fiche
- bash — Read the 100M bench numbers and the random control
- bash — Read the generation bench arguments
- bash — Run matched 34M and random generation benches on GPU
- bash — Save the matched bench JSONs to reports
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-banc-generation-100m.md`
- bash — Locate the N2 bullet and counters
- bash — Integrate the 100M result into the state
- bash — Fix the date and JSON counter
- bash — Read the current state header
- bash — Apply the header and counter fixes
- bash — Read the exact current state lines
- … et 36 autres

**Synthèse produite :**

⏵ Écriture de l'outil d'épinglage du corpus (sha256, manifeste, autotest)

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drvm.py` | 0 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_drvm_trace.py` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/drvm.rs` | 0 | 8 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-n3-refus.sh` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/modele-natif.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/native_model.py` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drvm_infere.py` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drvm_trace.py` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-n3-variante.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n3-variante.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-n3-route.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n3-route.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-n3-moteurs.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n3-moteurs.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-n3-court.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n3-court.md` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/A5.4-fpga.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/bench/gpu_scatter.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gpu-scatter.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/bench/drvm_profils.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-profils-modele.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gpu-scatter-grille.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-profils-5-modeles.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-banc-generation-100m.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/epingle_corpus.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-epingle.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-natif-val-deux-decoupages.md` | 1 | 0 |

### Sous-agents lancés

- tour 9 — Reconnaissance A2.6 experts
- tour 9 — Grammaticalité du 100 M

### Commandes exécutées (échantillon)

- **T1** List repository root and pilotage docs
- **T1** Check FPGA card presence and recent commits
- **T1** Check date and USB/PCI device list
- **T1** Inspect sibling FPGA repo for DDR3 capacity and PCIe status
- **T1** Check whether the Stratix V card is visible on PCIe
- **T1** Read resource/method notes listing the FPGA
- **T1** Check FPGA device nodes and November journal mentions
- **T1** Read roadmap blocked-resource table
- **T1** Date the FPGA verdict reports and read scaling argument
- **T2** Read Stratix V card specs (QSFP+, PCIe, power)
- **T2** Read host diagnostic script and multicard plan
- **T2** Read the CPU/AER report assumptions
- **T2** Check SSH hosts and known machines
- **T2** Look for an existing GPU scatter benchmark
- **T2** Check card power and GPU scatter notes
- **T3** List source tree and Rust core
- **T3** Search vision docs for module substitution and routing
- **T3** Read block/contract model in native model doc
- **T3** Inspect Rust traits and enums for dispatch
- **T3** Check whether manifest routes are implemented
- **T3** Read vision on substitutability and roadmap N0
- **T3** List CLI flags and check variant provenance in trace
- **T3** Check roadmap/backlog routing items and R0.5
- **T3** Read DRVM manifest parsing for graph/routes
- **T3** Read N3.3a routes report
- **T3** Check DRVM writers and unread manifest fields
- **T4** Check git state and DRVM-related gates
- **T4** Find the routes schema in the docs
- **T4** Read the refusal and routes gates
- **T4** Find DRVM manifest writers
- **T4** Read the DRVM exporter
- **T4** Inspect real DRVM manifests
- **T4** Check git hooks before committing
- **T4** Compare manifest keys across real DRVM files
- **T4** Read GGUF to DRVM manifest construction
- **T4** Survey all DRVM manifests for exact key sets
- **T4** Check Python test layout and inspect command
- **T4** Find existing Python tests and DRVM gates
- **T4** Read the gate qualifier for DRVM
- **T4** Find hand-built manifests in tools and gates
- … et 222 autres

## 4. Mesures et résultats marquants

- **T1** `7f23e55b NATIF — LE CACHE KV MESURÉ (×1,9, PARITÉ 3/3) : LE JETON COÛTE 11 MS PARCE QUE LE CPU LIT 136 MO DE POIDS (MEMORY-BOUND), PAS PARCE QU'IL RECALCULE ; LE GPU EST AU LANCEMENT (11 MS À VIDE)`
- **T1** `14ef014d ÉTUDE — LES 2 GPU NVLink VS CPU : L'ENTRAÎNEMENT ×12-39 (×77 EN TANDEM), LE PRÉFILL ×12, LE NVLink 23 Go/s, MAIS LE 34 M EST SOUS-UTILISÉ ET LA GÉNÉRATION EST BLOQUÉE PAR LE CACHE KV (×20-50 `
- **T1** `v14_l2_distance.sv        Kernel 1 — Distance L2 V14 (Q0.16, 14 DSP, 2 cycles)`
- **T1** `nipada_k1.sdc             Contraintes timing 200 MHz`
- **T1** `nipada_k2.sdc             Contraintes timing 200 MHz`
- **T1** `./docs/carte-storey-peak.md:46:| DDR3 | **4 Go**, DIMM 240 broches, **72 bits avec ECC**, 1600 MT/s | **9 662 Mo/s lecture / 7 816 Mo/s écriture** (mesuré, [blog part 6](https://j-marjanovic.io/strati`
- **T1** `./docs/carte-storey-peak.md:47:| PCIe | Connecteur x16, **2 Hard IP PCIe Gen3 x8 distincts** (pièce custom) | **6,5 Go/s par interface**, **11–12 Go/s** avec les deux ([blog part 8](https://j-marjanov`
- **T1** `./docs/carte-storey-peak.md:58:| `CLK_PCIE1` | `PIN_AF6/AF5` | 100 MHz (période 10 ns) | refclk Hard IP PCIe n°1 |`
- **T1** `./docs/carte-storey-peak.md:59:| `CLK_PCIE2` | `PIN_AF34/AF35` | 100 MHz | refclk Hard IP PCIe n°2 |`
- **T1** `./docs/carte-storey-peak.md:138:| [chisel-stuff / pcie-endpoint](https://github.com/j-marjanovic/chisel-stuff/tree/master/example-14-pcie-endpoint) | Endpoint PCIe + DMA écrit en Chisel (6,5 Go/s par `
- **T1** `| S — la banque validée | **`/paragraphes` fini** : 9/9 paragraphes, 19/19 candidats, 11 acceptés, 8 exclus, **11 verdicts committés (`389b99f`)** ; **banque 150 verdicts / 74 des 207 phrases** (35,7 `
- **T1** `- **R0** : un contrôleur **classique** + un modèle externe atteint-il **90 %** de la compréhension à **30 %** du`
- **T1** `60e19582 2026-10-01 22:26:07 -0400 mmap : 365,7 Go adresses en 0,08 s et 47 Mo de RSS`
- **T1** `| CPU, borné bande passante (28,7 Go/s) | 14.51 | 68.9 |`
- **T1** `| CPU, borné noyau (7,79 G év/s) | 44.93 | 22.3 |`
- **T1** `cache : 183999808.9 G événements/s mesurés contre 0.35 G nécessaires par token.`
- **T1** `3. **Une carte FPGA ≈ ce CPU** (23 contre 22 tok/s) : le CPU a`
- **T1** `3× la bande passante (28,7 contre 9,66 Go/s) mais il est limité par sa`
- **T2** `| DSP 18×18 | **[à vérifier]** (ordre de 1 000+) | non utilisé par les kernels « zéro DSP » |`
- **T2** `> ⚠️ **Correction d'une erreur fréquente** : les chiffres « ~622 000 ALM / 2 567 M20K / 66`
- **T2** `> `device/5SGSKF40I3LNAC.md`) ne correspondent **pas** au D5. Le D5 = 172 600 ALM, 1 963 M20K.`
- **T2** `**Conséquence directe** : 4,9 Mo de RAM embarquée = ~19,6 M poids en 2 bits. Tout modèle ou`
- **T2** `| DDR3 | **4 Go**, DIMM 240 broches, **72 bits avec ECC**, 1600 MT/s | **9 662 Mo/s lecture / 7 816 Mo/s écriture** (mesuré, [blog part 6](https://j-marjanovic.io/stratix-v-accelerator-card-from-ebay-`
- **T2** `| PCIe | Connecteur x16, **2 Hard IP PCIe Gen3 x8 distincts** (pièce custom) | **6,5 Go/s par interface**, **11–12 Go/s** avec les deux ([blog part 8](https://j-marjanovic.io/stratix-v-accelerator-car`
- **T2** `| Réseau | **2 × QSFP+ 40GbE** (SFF-8436) | 40GBASE-CR4/SR4 = **4 voies × 10,3125 Gbps** par port, ≈ 5 Go/s brut, ≈ 4,8 Go/s utiles |`
- **T2** `| `CLK_125M` | `PIN_M23` | 125 MHz | horloge générale |`
- **T2** `| `CLK_PCIE1` | `PIN_AF6/AF5` | 100 MHz (période 10 ns) | refclk Hard IP PCIe n°1 |`
- **T2** `| `CLK_PCIE2` | `PIN_AF34/AF35` | 100 MHz | refclk Hard IP PCIe n°2 |`
- **T2** `| `CLK_QSFP_OSC` | `PIN_T7/T6` | **644,53125 MHz** (période 1,551 ns) | **refclk des transceivers 40G** |`
- **T2** `> Le 644,53125 MHz est la refclk standard du 10,3125 Gbps : la chaîne QSFP+ dispose donc`
- **T2** `docs/carte-storey-peak.md-15-| Die de référence | `5SGSMD5` (D5), boîtier F40 (1517-FBGA, 40×40 mm), température industrielle |`
- **T2** `docs/carte-storey-peak.md-17-| Format | 111 mm × 168 mm, hauteur pleine, demi-longueur, **refroidissement actif obligatoire** |`
- **T2** `docs/carte-storey-peak.md-46-| DDR3 | **4 Go**, DIMM 240 broches, **72 bits avec ECC**, 1600 MT/s | **9 662 Mo/s lecture / 7 816 Mo/s écriture** (mesuré, [blog part 6](https://j-marjanovic.io/stratix-`
- **T2** `docs/carte-storey-peak.md-47-| PCIe | Connecteur x16, **2 Hard IP PCIe Gen3 x8 distincts** (pièce custom) | **6,5 Go/s par interface**, **11–12 Go/s** avec les deux ([blog part 8](https://j-marjanovic`
- **T2** `docs/carte-storey-peak.md:48:| Réseau | **2 × QSFP+ 40GbE** (SFF-8436) | 40GBASE-CR4/SR4 = **4 voies × 10,3125 Gbps** par port, ≈ 5 Go/s brut, ≈ 4,8 Go/s utiles |`
- **T2** `docs/carte-storey-peak.md-57-| `CLK_125M` | `PIN_M23` | 125 MHz | horloge générale |`
- **T2** `docs/carte-storey-peak.md-58-| `CLK_PCIE1` | `PIN_AF6/AF5` | 100 MHz (période 10 ns) | refclk Hard IP PCIe n°1 |`
- **T2** `docs/carte-storey-peak.md-59-| `CLK_PCIE2` | `PIN_AF34/AF35` | 100 MHz | refclk Hard IP PCIe n°2 |`
- **T2** `docs/carte-storey-peak.md:60:| `CLK_QSFP_OSC` | `PIN_T7/T6` | **644,53125 MHz** (période 1,551 ns) | **refclk des transceivers 40G** |`
- **T2** `docs/carte-storey-peak.md:62:> Le 644,53125 MHz est la refclk standard du 10,3125 Gbps : la chaîne QSFP+ dispose donc`
- **T2** `docs/carte-storey-peak.md-104-| BAR | Region 0 = **256 Mo**, Region 2 = 1 Ko |`
- **T2** `docs/multicartes.md-55-| NVLink (GPU0↔GPU1) | **25,781 Go/s par lien**, 1 lien par GPU | **mesuré** (`nvidia-smi nvlink -s`) |`
- **T2** `docs/multicartes.md-56-| PCIe Gen3 ×16 | ≈ 12–13 Go/s utiles | |`
- **T2** `docs/multicartes.md-57-| PCIe Gen3 ×8 (carte FPGA) | **6,5 Go/s** | mesuré par Jan Marjanovic |`
- **T2** `docs/multicartes.md:58:| QSFP+ 40GbE | ≈ 4,8 Go/s utiles | |`
- **T2** `docs/multicartes.md:60:**Hiérarchie réelle : NVLink > PCIe ×16 > QSFP+ 40G ≈ PCIe ×8.**`
- **T2** `docs/multicartes.md-62-débit (4,8 < 6,5 Go/s) — il n'a de sens que **pour des cartes déportées**, ou comme banc`
- **T2** `docs/multicartes.md-78-  (13 Go/s agrégés) plutôt que le 40G.`
- **T2** `docs/multicartes.md:86:- Refclk disponible : `CLK_QSFP_OSC` = **644,53125 MHz** (période 1,551 ns, `PIN_T7/T6`).`
- **T2** `- **CPU2** (bus `9f`–`ff`, NUMA node 1) : les 2 slots ×16 pour les cartes FPGA.`
- **T2** `- Les GPU sont sur le node 0 → tout échange GPU↔FPGA traverse le QPI (≈ 2×16 GT/s).`
- **T2** `- La carte consomme **x8** (un Hard IP) — le port amont du slot est ×16.`
- **T2** `- Sans bifurcation : **1 endpoint x8 par carte = 6,5 Go/s par carte** (mesuré).`
- **T2** `| 1 carte | Slot1_CPU2 | 6,5 Go/s | état actuel |`
- **T2** `| **2 cartes** | Slot1_CPU2 + Slot2_CPU2 | **13 Go/s** | recommandé, aucun compromis |`
- **T2** `| 3 cartes | + Slot3 (x4 Gen2) | 13 + 2 Go/s | la 3ᵉ carte est bridée à ×4 |`
- **T2** `| 4 cartes | riser PLX PEX8747 | 13 + partagé | l'upstream ×16 du riser (≈ 15,75 Go/s) devient le goulot |`
- **T2** `> slot ×16. Vérifier que ses slots aval sont **câblés ×16** (beaucoup ne le sont qu'en ×8),`
- **T2** `| NVLink (GPU0↔GPU1) | **25,781 Go/s par lien**, 1 lien par GPU | **mesuré** (`nvidia-smi nvlink -s`) |`
- **T2** `| PCIe Gen3 ×16 | ≈ 12–13 Go/s utiles | |`
- **T2** `| PCIe Gen3 ×8 (carte FPGA) | **6,5 Go/s** | mesuré par Jan Marjanovic |`
- **T2** `| QSFP+ 40GbE | ≈ 4,8 Go/s utiles | |`
- **T2** `**Hiérarchie réelle : NVLink > PCIe ×16 > QSFP+ 40G ≈ PCIe ×8.**`
- **T2** `débit (4,8 < 6,5 Go/s) — il n'a de sens que **pour des cartes déportées**, ou comme banc`
- **T2** `(13 Go/s agrégés) plutôt que le 40G.`
- **T2** `(accumulateur, 4096 × 24 bits = **12 Kio**, tient dans les M20K) ;`
- **T2** `- bande passante lecture séquentielle : **11.5 Go/s**`
- **T2** `- dispersion (`np.bincount`) : **183999808.87 G événements/s**`
- **T2** `- dispersion (`np.add.at`) : 364797216.41 G événements/s`
- **T2** `| Lecture séquentielle | 4,1 Go/s | 23,4 | **28,7** | 28,2 |`
- **T2** `| Dispersion pure | 0,96 G év/s | 3,46 | 3,20 | 3,22 |`
- **T2** `## Projection 7B (densité 5 %, 0,476 b/poids)`
- **T2** `Le débit varie de **0,011 ms à 0,95 ms sur la même matrice** (rapport 86) selon ce`
- **T2** `## Montée en charge (meilleur de 3 passes, densité 100 %)`
- **T2** `➡️ **~0,15–0,18 G év/s par thread**, optimum vers 28–32 threads, soit ~0,8–1,3`
- **T2** `événement par cycle CPU. Une carte à 124 MHz × 32 PEs = 4 G év/s vise donc`
- **T2** `> Mesures prises avec le bureau actif (load ~1,5–5) : ±20 % d'une passe à l'autre,`
- **T2** `La première campagne annonçait « fusion DIVERGENTE au rang 0 : 3838 vs 3513 » et un`
- **T2** `chemin 2-listes à 7,53 G év/s. **Les deux chiffres étaient faux.** Le chemin`
- **T3** `attention locale (fenêtre 256), un **FFN creux routé** (8 experts, top-2, k-WTA 25 %), **3 têtes précoces**`
- **T3** `//! | VRAM (noyau warp) | 84,9 Go/s |`
- **T3** `//! | RAM, 20 cœurs physiques | 22,5 Go/s |`
- **T3** `//! | RAM, 10 cœurs + leurs hyperthreads | 18,7 Go/s (+27 % sur 10 cœurs secs) |`
- **T3** `//! | RAM, 20 cœurs + hyperthreads | 18,9 Go/s — **rien de plus** |`
- **T3** `//! | NVMe, 1 lecteur | 5,4 Go/s |`
- **T3** `//! | **NVMe, 16 lecteurs** | **31,1 Go/s** |`
- **T3** `/// deux fils d'une même paire partagent L1 et L2, ce qui vaut +27 % quand`
- **T3** `/// Liens NVLink actifs : 25,8 Go/s sur cette machine, soit 2× le PCIe.`
- **T3** `//! | VRAM | 84,9 Go/s | le KV au-delà de ~2-4 k jetons, l'attention, la tête |`
- **T3** `//! | RAM | 22,5 Go/s | les poids (mmap, non copiés), le KV court |`
- **T3** `//! | NVMe | 3,5 Go/s | les poids qui ne tiennent pas en RAM (streaming) |`
- **T3** `//! mesure du 24/10 valide la première ligne : le KV en VRAM donne ×1,93 sur le`
- **T3** `//! préremplissage à 8 k et ×5,8 sur l'attention.`
- **T3** `198:   30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T3** `250:[N0/N1] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T3** `docs/pilotage/roadmap.md:198:   30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.m`
- **T3** `[still running after 60000ms; moved to background job bash-26]`
- **T5** `defaut  médiane   87.0 ms  (CV 1 %)`
- **T5** `bloque  médiane   86.4 ms  (CV 14 %)`
- **T5** `[s/v7 20648db7] N3.7 — LES VARIANTES SONT UN CONTRAT : SUBSTITUTION 4,768e-07 ≤ 1e-4 · CONTRÔLE NÉGATIF 5,790e-03 > 1e-4 · COÛT 87,0/86,4 ms (0,99×)`
- **T5** `20648db7 N3.7 — LES VARIANTES SONT UN CONTRAT : SUBSTITUTION 4,768e-07 ≤ 1e-4 · CONTRÔLE NÉGATIF 5,790e-03 > 1e-4 · COÛT 87,0/86,4 ms (0,99×)`
- **T5** `./reports/rapport-natif-numpy.md:7:> **Le chiffre.** `tools/drvm_infere.py` charge les **127 tenseurs** du DRVM (130,9 Mo) en`
- **T5** `defaut  médiane   85.9 ms  (CV 2 %)`
- **T5** `bloque  médiane   84.1 ms  (CV 5 %)`
- **T5** `defaut  médiane   85.1 ms  (CV 2 %)`
- **T5** `bloque  médiane   84.5 ms  (CV 11 %)`
- **T6** `defaut  médiane   83.6 ms  (CV 4 %)`
- **T6** `court   médiane   55.9 ms  (CV 4 %)`
- **T6** `defaut  médiane   83.9 ms  min   78.0  CV 3 %`
- **T6** `court   médiane   56.1 ms  min   51.3  CV 3 %`
- **T6** `defaut  médiane   80.8 ms  (CV 3 %)`
- **T6** `court   médiane   56.0 ms  (CV 6 %)`
- **T6** `[s/v7 de967b7b] N3.10 — `COURT` : LE PREMIER PROFIL QUI PAIE — BIT-EXACT < 64 o · 3,633e-02 AU-DELÀ · 0,694× LE TEMPS · SUR LE 34 M PPL 23,7480 → 23,5824 ET ~5 %`
- **T6** `de967b7b N3.10 — `COURT` : LE PREMIER PROFIL QUI PAIE — BIT-EXACT < 64 o · 3,633e-02 AU-DELÀ · 0,694× LE TEMPS · SUR LE 34 M PPL 23,7480 → 23,5824 ET ~5 %`
- **T6** `0, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T6** `1, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T6** `index_add         2.66 ms  →  25.22 G év/s`
- **T6** `bancs_b1          2.69 ms  →  24.91 G év/s`
- **T6** `bancs_b4          2.54 ms  →  26.40 G év/s`
- **T6** `bancs_b16         2.47 ms  →  27.15 G év/s`
- … (tronqué)

## 5. Erreurs rencontrées

7 sorties en erreur ou divergentes. Les premières :

- **T4** : pre-commit === hook contenu === --- .git/hooks/pre-commit #!/bin/sh # pre-commit — l'état accompagne le fait, le journal accompagne le code. # # Versionné dans tools/hooks/ et installé par tools/insta
- **T4** : |            ^^^^^^^^  warning: the `ids:` in this pattern is redundant     --> src/main.rs:1751:9      | 1751 |         ids: mut ids, ids_file, prompt, n: n_new, temp, top_p, topk, rep_pen, hist,    
- **T4** : -rwxr-xr-x. 2 stephane stephane 3218824 17 nov 11:14 drave-core/target/release/drave DRVM v0 · 6 blocs · 30 tenseurs · payload 31488 o   bloc input        input   bloc b0           local_mixer [stderr
- **T5** : ... 110 |     pub fn est_vide(&self) -> bool { self.lignes.is_empty() } 400 | pub fn existe(chemin: &str) -> bool { Path::new(chemin).is_file() } 187 | impl Episodique { ... 193 |     pub fn est_vide(
- **T5** : ok ---- tests_vars::les_vars_lues_sont_completes stdout ----  thread 'tests_vars::les_vars_lues_sont_completes' (3595551) panicked at src/main.rs:9068:13: DRAVE_NATIVE_PROFONDEUR est lu dans le source
- **T8** : [stderr] Traceback (most recent call last):   File "<stdin>", line 3, in <module>   File "<stdin>", line 3, in <lambda> ValueError: invalid literal for int() with base 10: 'n' [exit code: 1]
- **T9** : work/n2ac/mix1024-100m.drvm work/n2ac/mix1024-100m.pt work/n2ac/mix1024-100m.pt.json === json du pt === {  "modele": "drave-n0",  "parametres": 73366568,  "corpus": "data/wiki_mix/propre/train.txt",  

## 6. Commits

- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -F - <<'MSG' 2>&1 | tail -15 DRVM — LE LECTEUR REFUSE CE QU'IL N'EXÉCUTE PAS : routes/régions/t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -F - <<'MSG' 2>&1 | tail -8 N3.7 — LES VARIANTES SONT UN CONTRAT : SUBSTITUTION 4,768e-07 ≤ 1e-
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/drvm.py tools/drvm_infere.py tools/drave.py tools/porte-n3-variante.sh reports/rapport-n3-va
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/drvm.py drave-core/src/drvm.rs drave-core/src/native.rs drave-core/src/main.rs tools/drvm_in
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/porte-n3-moteurs.sh reports/rapport-n3-moteurs.md docs/pilotage/en-cours.md docs/pilotage/ro
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/drvm.py drave-core/src/drvm.rs drave-core/src/native.rs tools/porte-n3-court.sh reports/rapp
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/backlog/A5.4-fpga.md docs/pilotage/roadmap.md docs/pilotage/en-cours.md && git commi
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add bench/gpu_scatter.py reports/rapport-gpu-scatter.md reports/gpu-scatter.json docs/pilotage/backlog
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('drave-core/src/main.rs'); s = p.read_text() old = "    /
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add bench/drvm_profils.py reports/rapport-profils-modele.md reports/profils-34m.json docs/pilotage/en-
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/drvm.py tools/drvm_infere.py tools/porte-n3-moteurs.sh tools/porte-n3-court.sh reports/rappo
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/backlog/N3-operations-natives.md docs/pilotage/en-cours.md && git commit -F - <<'MSG
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add bench/gpu_scatter.py reports/rapport-gpu-scatter-grille.md reports/rapport-profils-5-modeles.md re
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/references-non-regression.md docs/pilotage/en-cours.md && git commit -F - <<'MSG' 2>
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/banc_generation.py tools/chantier/plan.json reports/banc-generation-100m.json reports/banc-g
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/epingle_corpus.py reports/corpus-epingle.json reports/rapport-corpus-epingle.md docs/pilotag
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() old = '| 

