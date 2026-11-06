# La file des tâches — inventaire, trois files et ordre pour 09 h 30 → 12 h

> **Ligne de roadmap** : B13 (moteur de pensée) · **Date** : 2026-11-06, 10 h 20 HNE · **Branche** : `s/v7` · **HEAD mesuré** : `7679a2d4`.
> **Mission** : inventer toutes les prochaines actions nommées dans `roadmap.md`, `en-cours.md`, `plan-travail.md` § 9 et § 12, `backlog/index.md`, `backlog/dependances.md`, `references-non-regression.md` et les 12 fiches récentes ; les classer en trois files ; détecter doublons et périmées ; proposer l'ordre de la fenêtre.
> **Verdict** : **29 tâches** — **8 autonomes**, **11 en coordination**, **10 bloquées** ; **6 doublons**, **18 périmées**, **12 dépendances cachées**.
> **Ce que cette fiche n'est pas** : un commit, une modification d'existant, ou une mesure nouvelle sur S/D/N2. Elle ne crée que deux fichiers neufs.

## 1. Résumé exécutif

La file est **courte** une fois les doublons retirés : **8 tâches sont exécutables en autonomie** dans le territoire L/B13 et le pilotage, **11 demandent une coordination** (S, D, N2, A, produit), **10 sont bloquées** par une ressource externe nommée. Le reste de ce que les documents appellent « ce qui reste » est **déjà fait** ou **mal daté** : 18 mentions périmées, dont 6 répétées dans 3 à 7 documents.

Trois constats changent la lecture de l'état :

- **La rouge `cascade_pos` est un choix de méthode, pas un manque de mesure** : la porte échoue parce que `priorite_par_defaut()` ne rend la priorité par niveau que si `DEEPSEEK_KEY_FILE` est posé ; avec la clé, le `MockNeuronal` fait tomber la cascade à 0,3454. Poser la clé ne corrige donc rien.
- **S n'est plus bloquée par l'humain** : `validations.jsonl` contient **150 verdicts humains** et `paragraphes-validations.jsonl` **19 verdicts sur les 9 paragraphes** (a001 à a009). La roadmap dit encore « aucun verdict humain, le fichier n'existe pas ».
- **A2.6 n'est pas une ligne libre** : ses experts sont bloqués par A6.2, sa tête est refusée, A8.3a est fait et la question du lot est répondue. Le graphe la garde pourtant à la frontière.

L'ordre proposé tient en **trois vagues** de 4 sous-agents au plus, après la **vague 0 déjà exécutée** par la session principale (produit `drave` v0, commits `bdeca168`, `a9907a1b`, `62dad657`) : fermer la rouge et documenter le produit ; trancher les 17 spans et l'état ; clore, publier et mesurer les portes légères.

## 2. Méthode et état de l'arbre

**Sources lues** : `docs/pilotage/roadmap.md` (382 l.), `en-cours.md` (145 l., version 10 h 20), `plan-travail.md` § 9 et § 12 (deux sections 9 : l. 163 et 403), `backlog/index.md` (37 fiches), `backlog/dependances.md` (43 arêtes, 3 plafonds), `references-non-regression.md` (84 portes), les 12 fiches `reports/rapport-*.md` les plus récentes, les fiches produit (`rapport-produit-v0.md`, `rapport-autotest-parallele.md`) et les fiches de blocage (`rapport-a26-bilan.md`, `rapport-a26-lot-disque.md`, `rapport-n2-r12-2048.md`, `rapport-s-paragraphes.md`).

**Mesures rejouées** (pas seulement lues) : `python3 -m tools.pensee.autotest` (183/183), `python3 tools/tests/linguistique/evaluer_gold.py --json` (exit 1, `cascade_pos=false`), `bash tools/porte-bloc-linguistique.sh` (exit 1), `bash tools/porte-produit.sh` (exit 0), `bash tools/porte-sessions.sh` (exit 1), `bash tools/porte-ressources.sh` (exit 0), la suite documentaire (`revue`, `taille`, `en-cours`, `journal`, `liens`, `schémas`, `backlog`) et `python3 tools/drave.py --help`.

**État de l'arbre** : `s/v7`, HEAD `7679a2d4` à 10 h 20. L'arbre est **sale avant** l'inventaire (journal, sept `reports/` modifiés, `tools/structures` modifié, `reports/rapport-s-paragraphes.md` non suivi) et il **bouge pendant** : `en-cours` a été réécrit à 10 h 20 et HEAD est passé de `62dad657` à `7679a2d4`. Toute mesure de cette fiche est donc horodatée.

**Aucun existant modifié.** Un accident est à consigner : `python3 tools/index_reports.py --help` n'a pas d'`argparse` et a **réécrit `reports/INDEX.md`** ; le fichier a été restauré par `git restore -- reports/INDEX.md` (vérifié : plus de différence). C'est une commande à ne pas lancer sur l'arbre partagé.

## 3. File (a) — faisable en autonomie maintenant (8)

Critère : le fichier est dans le territoire **L/B13** (`tools/bloc_linguistique.py`, `tools/pensee/`, `tools/tests/linguistique/`), dans **`reports/`** (fichier neuf), ou dans le **pilotage** que l'agent principal tient seul (`en-cours`, `roadmap`, `chantiers`, `plan-travail`). Aucune écriture dans S, D, N2, `data/`, natifs.

| id | chantier | action | fichier / outil | dépend de | bloquant | commande exacte | prio |
|---|---|---|---|---|---|---|---|
| T01 | L | Rendre verte la porte bloc-linguistique : cascade_pos à 0,7465 contre l'heuristique 0,7581 | tools/bloc_linguistique.py (MockNeuronal, Cascade), tools/tests/linguistique/evaluer_gold.py | aucune (mesure locale) | aucun ; choix de méthode (Mock ou fusion), T138 attend 0,7465 | bash tools/porte-bloc-linguistique.sh ; python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/pensee-gold-porte.json | P0 |
| T02 | L | _pos anglais : 176 VERB tagués NOUN (A14), 450 confusions VERB vers NOUN dans la matrice | tools/bloc_linguistique.py, tools/tests/linguistique/gold_reel.py et .json, reports/pensee-pos-anglais.json | T01 non requis | aucun | python3 -m tools.pensee.autotest ; python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/pensee-gold.json | P1 |
| T03 | B13 | Trancher les 17 spans : corriger les 4 GP du gold sans préposition, acter les 12 formes synthétiques et la tokenisation qu'il ; fiche v13 | tools/tests/linguistique/gold_reel.py et .json ; reports/rapport-pensee-v13.md et JSON | v12 (222/222) | aucun ; interdiction d'étendre le lexique synthétique (ajustement au test) | python3 -m tools.pensee.autotest ; python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/pensee-gold.json | P1 |
| T04 | L | Refus r353 : la fusion par niveau refuse 1 phrase ; reproduire par l'API et corriger | tools/bloc_linguistique.py (_fusion) ; tools/tests/linguistique/qualifier_quatre_modes.py | clé API présente (36 o) | API non déterministe | DEEPSEEK_KEY_FILE=$HOME/.config/drave/deepseek.key python3 tools/tests/linguistique/qualifier_quatre_modes.py --sortie /tmp/qm.json | P2 |
| T05 | PRODUIT | Écrire la doc d'usage docs/produit/ : commandes, exemples, limites, codes de sortie | docs/produit/ (neuf) ; tools/drave.py | produit v0 (62dad657) | aucun | python3 tools/drave.py --help ; python3 tools/drave.py analyser "Le chat dort sur le toit." ; python3 tools/drave.py evaluer ; python3 tools/drave.py rejouer "Le chat dort." ; python3 tools/verifier_liens.py | P0 |
| T06 | PILOTAGE | Mettre l'état B13 à jour : 222/222, T132/T133 verts, 17 spans, passe du 06/11, prochaine action | docs/pilotage/en-cours.md, roadmap.md, chantiers.md, plan-travail.md | T03, T05 | un seul écrivain (agent principal) | python3 tools/revue_documentation.py ; python3 tools/verifie_en_cours.py ; python3 tools/taille_documents.py | P0 |
| T07 | PILOTAGE | Références de non-régression : 84 portes, ligne porte-produit, 4 rouges nommées (indice, melange, sessions, bloc-linguistique), lecteur vert | docs/pilotage/references-non-regression.md | T01 | aucun | ls tools/porte-*.sh ; bash tools/porte-produit.sh ; bash tools/porte-sessions.sh ; bash tools/porte-bloc-linguistique.sh | P1 |
| T08 | DOC | Corriger le double ## 9 de plan-travail.md (lignes 163 et 403) ; corriger le commentaire « 81 portes » de toutes-les-portes.sh | docs/pilotage/plan-travail.md ; tools/toutes-les-portes.sh (commentaire seulement) | aucune | aucun ; ne toucher que le commentaire de la porte | grep -n '^## 9' docs/pilotage/plan-travail.md ; bash tools/porte-tableaux.sh | P2 |

## 4. File (b) — coordination requise (11)

Critère : la tâche est réelle et non bloquée par une ressource externe, mais elle s'écrit dans un territoire qui n'est pas celui de la fenêtre (S, D, N2, A, produit) ou elle demande un arbitrage d'architecture. On **lit, on propose, on ne code pas** dans ces fichiers.

| id | chantier | action | fichier / outil | dépend de | bloquant | commande exacte | prio |
|---|---|---|---|---|---|---|---|
| T09 | N2 | La porte propre (0,29 manquant à 2,7856) : données ou capacité | reports/n2-*, work/n2ac/, tools/entrainer_native.py, GPU | recette N2 1 024 | aucun externe ; GPU libres (0 %) | python3 tools/eval_n2_propre.py <checkpoint> (pas de commande unique) | P0 |
| T10 | R1 | Aiguille native >= 15/18 à 4 000 non atteinte (copie 0,0078) : décider R11 close ou passer à R2.1 (tampon en entrée) | reports/rapport-n2-r12-2048.md ; backlog/R11-contexte-hierarchique.md ; backlog/R21-memoire-travail-gist.md | R11/R12 mesurées | décision d'architecture | python3 tools/verifie_backlog.py | P1 |
| T11 | N4 | Consigne courte : construire le jeu, entraîner, évaluer tenu à l'écart (24/24 vus, 0/4 tenus) | backlog/N4-usage-sft.md ; reports/n4-* ; N2/GPU | recette N2 | aucun externe ; GPU libres | python3 tools/eval_n2_propre.py <checkpoint> (pas de commande unique) | P1 |
| T12 | S | Inventorier et proposer l'intégration des verdicts humains : 19 validations sur les 9 paragraphes, 150 sur la banque ; vérifier la couverture, S écrit et commite le pointeur | tools/structures/donnees/paragraphes-validations.jsonl ; validations.jsonl ; page /paragraphes | sous-module S | route /paragraphes en 404 sur 8765 ; sous-module modifié non committé | ls tools/structures/donnees/*validations*.jsonl ; curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8765/paragraphes | P1 |
| T13 | S | Proposer la règle du nom après un adjectif hors lexique (« Le fait divers surprend ») ; S l'écrit | tools/structures/generateur.py ; tools/structures/donnees/ | T12 | sous-module S, territoire | pas de commande unique ; test dans le sous-module | P2 |
| T14 | B9 | Resserrer la transition 9,23–9,96 M ; porter le masque dans le trainer | reports/b9-* (absent) ; tools/entrainer_native.py | N2 | objet non défini dans une fiche | pas de commande nommée | P2 |
| T15 | B13 | gold 200+ : définir l'objet (gold linguistique 432 ou gold de pensée) avant d'exécuter | tools/tests/linguistique/gold_reel.* ; docs/pilotage/roadmap.md | v12 | libellé ambigu, 7 occurrences, aucune définition | grep -rn 'gold 200+' docs/pilotage | P1 |
| T16 | PRODUIT | Appliquer les correctifs de l'audit de fiabilité du produit | reports/rapport-produit-bloc-l.md (absent) ; reports/pensee-produit-bloc-l.json (absent) ; tools/drave.py | audit 14114f3d en cours | artefact absent | bash tools/porte-produit.sh (après l'audit) | P1 |
| T17 | DOC | Régénérer reports/INDEX.md (625 fiches annoncées, 678 sur disque) et vérifier les compteurs | reports/INDEX.md (généré) ; tools/index_reports.py | hub | l'outil réécrit l'INDEX et n'a pas de --help | python3 tools/index_reports.py (hub seulement) ; python3 tools/revue_documentation.py | P2 |
| T18 | A2.6 | Trancher la frontière : A2.6 n'est pas libre (experts bloqués A6.2, tête refusée, A8.3a fait, lot répondu) ; le retirer de la frontière du graphe | docs/pilotage/backlog/dependances.md ; backlog/A2.6-ordonnanceur.md ; reports/rapport-a26-bilan.md | A6.2 | A6.2 (MoE local) | python3 tools/verifie_backlog.py | P1 |
| T19 | DOC | Appliquer les 42 écarts de cohérence v8 (5 lignes README, en-têtes historiques) | reports/README.md ; 8 fiches et 8 JSON | hub | fiches existantes à modifier (hors fenêtre) | python3 tools/revue_documentation.py | P2 |

## 5. File (c) — bloquée (10)

Critère : une ressource externe nommée manque (matériel, corpus, encodeur, poids, verdict humain). La règle « jamais en attente » s'applique : on prend la ligne suivante de la file (a) ou (b), on ne bloque pas la fenêtre.

| id | chantier | action | bloquant | Ce qu'il faudrait | preuve |
|---|---|---|---|---|---|
| T20 | A3.4 | Démonstration Colab | compte et runtime Colab | un compte et un runtime Colab ; la recette est dans docs/archive/colab-reparti.md | roadmap:351 ; backlog/A3.4-colab.md |
| T21 | A5.4 | Opérateur FPGA complet | carte Stratix V absente | la carte Stratix V ; le design existe | roadmap:352 ; backlog/A5.4-fpga.md |
| T22 | A6.2 | Routage MoE appris | aucun MoE local ne tient dans 16 Go | un MoE qui tient dans 16 Go, ou une machine plus grande | roadmap:353 ; backlog/A6.2-moe-local.md |
| T23 | A2.6 | Experts de l'ordonnanceur | A6.2 (MoE local) | un MoE local (A6.2) | rapport-a26-bilan.md:30 |
| T24 | B1.5 | Prose scientifique : corpus parallèle humain FR/EN | aucun corpus parallèle humain | un corpus licite (revue, actes, manuel) traduit par des humains | roadmap:350 ; backlog/B1.5-prose-scientifique.md |
| T25 | B10.3 | Raisonnement sur z gelé | décodeur sous le plancher chrF 39,6 | une attention croisée, 20–30 articles, 3 graines | roadmap:354 ; backlog/B10.3-raisonnement-z.md |
| T26 | R44 | 10 pages scannées réelles avec vérité humaine | pas de vérité humaine ; fax 1 bit et exposant fusionné | 10 pages scannées avec vérité humaine ; le fax 1 bit reste une limite | roadmap:355 ; backlog/R44 ; OCR 5.5.3 dans work/ocr/root |
| T27 | N5 | L'échelle 50–100 M | gelé jusqu'au verdict de R11 | le verdict de R11 sur le contexte | roadmap:340 ; dependances:207 |
| T28 | R21 | Chaîne mémoire vers restitution vers lecture croisée (R21, R31, R51) | R11 non close, N4 ouvert, R31/R32 spécifiés | R11 close, N4 livré, R31 et R32 mesurés | dependances:106-115 ; programme-r:288 |
| T29 | L | Neuronal réel local (7B) et restitution/traduction | règle 11 interdit un 7B local ; la restitution attend R31 | des poids et un service ; l'API DeepSeek pour le neuronal, pas un 7B local | AGENTS règle 11 ; porte-ressources vert ; rapport-produit-v0.md §3 |

## 6. Doublons (6)

Même action nommée dans plusieurs documents, ou même libellé pour deux objets. Un doublon n'est pas une faute de frappe : il fait croire à deux chantiers et double le travail de mesure.

| # | action | où | preuve | décision |
|---|---|---|---|---|
| D1 | dev/test à re-mesurer | v9, v10, v11 §6 ; plan-travail §9 vague 7 | v12 : dev 153/153, test 69/69 ; rapport-dev-test-v10 | Une seule mesure, faite ; retirer des suites |
| D2 | Les N spans | v5 (52), v7 (43), r1r3 (27), v9 (20), v10 (19), v11 (18), v12 (17) | v12 §2 : 17 spans (8 REL, 5 SUB, 4 GP) | Seul 17 est vivant ; les autres sont historiques |
| D3 | T132/T133 | roadmap:178 ; chantiers:90 ; plan:39 et 195 ; en-cours:131 | autotest : T132 5/5, T133 5/5 | Fermer ; retirer les 5 mentions |
| D4 | Passe complète | en-cours:131 ; plan:401 ; references:3 | ea7d3275 ; registre 06/11 (79/4) | Une seule passe de référence ; la prochaine sera 84 portes |
| D5 | gold 200+ | roadmap:31 et 178 ; chantiers:83 et 89 ; en-cours:131 ; plan:39 et 195 | 7 occurrences, aucune définition | Définir l'objet avant d'en faire une tâche |
| D6 | A2.6 experts | roadmap:30 et 146 ; chantiers:84 ; dependances:162 ; en-cours:120 ; backlog/A2.6 | rapport-a26-bilan.md:30 | Une seule ligne, bloquée A6.2 ; retirer de la frontière |

## 7. Périmées (18)

La tâche est encore listée alors que la mesure ou le commit qui la ferme existe. La preuve est soit un commit, soit une commande rejouée, soit un fichier présent sur disque.

| # | tâche encore listée | où | preuve | statut réel |
|---|---|---|---|---|
| P1 | T132/T133 2/5 | roadmap:178 ; chantiers:90 | autotest : 5/5 et 5/5 | Verts ; mention périmée |
| P2 | B13 178/178 et 183/183 portes | en-cours:98 et 131 ; roadmap:31 | v12 : 222/222 ; autotest : 183/183 | 222/222 ; 183/183 |
| P3 | dev/test à re-mesurer | v9, v10, v11 §6 | v12 : 153/153 et 69/69 | Fait |
| P4 | Merge master si autorisé | v9 §6.3 | commit fa1b0c6e (master à jour, 375 commits) | Fait |
| P5 | Passe complète après les runs | plan:401 ; en-cours:131 | commit ea7d3275 ; registre 06/11 | Faite (79 vertes, 4 rouges) |
| P6 | Les 43, 52, 27, 20, 19, 18 spans | v5, v7, r1r3, v9, v10, v11 §6 | v12 §2 : 17 spans | 17 ; les autres sont des instantanés |
| P7 | 200 000 pas N2 | roadmap:197 (la même cellule dit 200k fait puis le redemande) | en-cours:122 ; roadmap:197 | Fait |
| P8 | R1.2-1024 | en-cours:131 | rapport-n2-r12-2048 ; rope1024-20k | Fait (20 000 pas) |
| P9 | Ce qui reste des opérations N3 | dependances:88 et 164 | en-cours:97 ; porte-n3-inventaire | N3 clos |
| P10 | R44 bloquée par l'absence d'OCR | dependances:113 | R44 fiche ; tesseract 5.5.3 ; porte-ocr-scans verte | OCR installé ; reste la vérité humaine |
| P11 | S : aucun verdict humain, validations.jsonl absent | roadmap:356 | 150 enregistrements humains ; 19 sur les paragraphes | Verdicts présents ; à intégrer |
| P12 | S : a001–a003 faits, 8 restants | en-cours:59 | 9 phrases ont des verdicts (19 enregistrements) | Les 9 ont des verdicts ; couverture à vérifier |
| P13 | A2.6 libre : experts et tête | roadmap:30 ; dependances:162 | rapport-a26-bilan ; a26-lot-disque | Experts bloqués ; tête refusée ; A8.3a fait ; lot répondu |
| P14 | A8.3 : réduire le lot ou l'assumer | roadmap:152 ; chantiers:84 | a26-lot-disque : 503 Mio constant, +27 % tok/s, PPL -0,006 % | Lot >= 2 assumé |
| P15 | 83 portes | references:49 ; en-cours (version 09 h 35) ; toutes-les-portes:21 | 84 scripts ; porte-produit commitée et verte | 84 |
| P16 | 625 fiches (INDEX) | reports/INDEX.md:3 | 678 fiches sur disque | 678 ; INDEX à régénérer |
| P17 | R0.7 tagger | en-cours:131 | roadmap R0.7 : tagger 7B POS 0,9440 ; règle 11 | Mesuré ; le local 7B est interdit |
| P18 | e181ce02 : l'API rejoue le gold | en-cours:72 | produit v0 (62dad657) ; autotest 183/183 | Fait ; mention périmée |

## 8. Dépendances cachées (12)

Ce qui n'est pas écrit dans la ligne de tâche mais qui décide de son exécution. C'est la partie la plus utile de l'inventaire : une file qui ignore ces dépendances se croit libre là où elle est bloquée, ou bloquée là où elle est libre.

| # | dépendance cachée | preuve | conséquence |
|---|---|---|---|
| H1 | DEEPSEEK_KEY_FILE change la priorité de fusion | sans clé : None, cascade par confiance 0,7465 ; avec clé : niveau 0,3454 | La porte est rouge dans les deux cas ; ne pas « corriger » en posant la clé |
| H2 | A2.6 est à la frontière mais son action est bloquée | rapport-a26-bilan.md:30 | Le graphe annonce 3 items libres, dont un bloqué |
| H3 | R44 est dite bloquée par l'OCR, qui est installé | tesseract 5.5.3 dans work/ocr/root ; porte-ocr-scans verte | Le vrai blocage est la vérité humaine |
| H4 | La 84e porte n'est ni dans la passe ni dans les références | porte-produit.sh commitée (62dad657), verte ; refs:49 dit 83 | Toute passe complète suivante sera à 84 |
| H5 | Les validations S existent mais l'état dit bloqué | 150 + 19 enregistrements humains ; sous-module modifié | S n'est pas bloquée par l'humain ; elle est à intégrer |
| H6 | index_reports.py n'a pas de --help et réécrit l'INDEX | --help a modifié reports/INDEX.md (restauré) | Ne jamais lancer cet outil sur l'arbre partagé sans commit |
| H7 | L'arbre bouge pendant l'inventaire | HEAD 62dad657 vers 7679a2d4 ; en-cours réécrit à 10 h 20 | Toute mesure doit nommer son HEAD ; les compteurs changent |
| H8 | Collisions d'identifiants | manques.md N3/N4/N5 (modèle) contre roadmap N3/N4/N5 | Une tâche peut être prise pour une autre ; toujours nommer le document |
| H9 | La passe complète coûte 2 h 29 | references:5-6 | Incompatible avec la fenêtre ; ne lancer que des sous-ensembles légers |
| H10 | Chaque fiche neuve change les compteurs | 678/771 ; cette fiche : 679/772 ; trois fiches de vague : 682/775 | La revue échoue au prochain commit si en-cours n'est pas mis à jour |
| H11 | Les heartbeats sont un prérequis de commit | porte-sessions : e181ce02 391 min, hub 1941 min | Rouge de coordination, pas de code |
| H12 | eval_n2_propre.py exige un checkpoint | argparse : point positionnel | Pas de commande unique pour N2 ; nommer le checkpoint |

## 9. Ordre d'exécution — 09 h 30 → 12 h

**Ce qui est déjà fait (vague 0, 09 h 31–09 h 56)** : le premier produit — `drave` v0 (`analyser`, `evaluer`, `rejouer`, `--version`), le smoke test de 6 cas, `porte-produit` (84e porte, verte) et l'autotest parallèle (183/183 en 1 min 54). Commits `bdeca168`, `a9907a1b`, `62dad657`, `7679a2d4`. La file ci-dessous commence donc à **10 h 30** et tient en trois vagues de 30–35 min.

**Règle de vague** : 4 sous-agents au plus, **fichiers disjoints**, aucun ne commite. L'agent principal **rejoue** les mesures annoncées, écrit la fiche de vague (`reports/rapport-vague-N.md` + JSON), met à jour `en-cours` et commite **une fois** par vague avec `git add` explicite. Une vague sans mesure reproduite ne produit ni fiche ni commit.

| vague | sous-agent | mandat | sortie | interdits |
|---|---|---|---|---|
| V1 | cascade | Rendre verte la porte bloc-linguistique (T01) ; mesure avant/après ; diff et fiche de vague | tools/bloc_linguistique.py ; reports/rapport-vague-1.md | Pas de commit ; pas de test modifié sans justification écrite |
| V1 | doc-produit | Écrire docs/produit/drave-cli.md et exemples (T05) ; exécuter chaque commande citée | docs/produit/ (neuf) | Pas de tools/ ; pas de pilotage ; pas de commit |
| V1 | audit-portes | Auditer les 84 portes et les 4 rouges (T07) ; lire les registres, ne rien lancer de lourd | tableau pour rapport-vague-1 | Aucune écriture ; pas de passe complète |
| V1 | pos-anglais | Diagnostiquer _pos anglais (T02) : compte, exemples, règles candidates ; pas de code | reports/pensee-pos-anglais.json ; section de fiche | Pas de code ; pas de gold |
| V2 | spans-gold | Identifier les 4 GP sans préposition, les 12 synthétiques et la tokenisation (T03) ; proposer un diff de gold | reports/pensee-spans-v13.json ; section de fiche | Pas d'écriture du gold ; pas de lexique synthétique |
| V2 | r353 | Reproduire le refus r353 par l'API (T04) ; qualifier la cause | note pour rapport-vague-2 | Pas de code ; documenter le coût de l'appel |
| V2 | s-validations | Inventorier les 19 validations paragraphes et les 150 de la banque (T12) ; couverture par phrase | note pour rapport-vague-2 | Pas d'écriture du sous-module ; pas de commit du pointeur |
| V2 | doc-index | Compter les fiches de l'INDEX et lister les manquantes (T17) ; proposer la commande | note pour rapport-vague-2 | Ne pas lancer index_reports.py sur l'arbre partagé |
| V3 | etat-final | Préparer le bloc d'état B13 (T06) : chiffres, prochaine action, rouges | note pour l'agent principal | Pas d'écriture de pilotage |
| V3 | produit-final | Finaliser docs/produit et rejouer porte-produit (T05) | docs/produit/ | Pas de commit |
| V3 | file-taches | Finaliser la présente fiche et son JSON | reports/rapport-file-taches.md ; reports/pensee-file-taches.json | Aucun existant modifié |
| V3 | passe-legere | Lancer PORTES="produit bloc-linguistique sessions tableaux" et lire le registre | work/portes-vague-3/registre.txt | Pas de passe complète ; lire par awk, jamais par un tube |

**Portes et commits par vague.**

| vague | créneau | mesure de sortie | fiche | portes avant commit | commit |
|---|---|---|---|---|---|
| **1** | 10 h 30–11 h 00 | `bloc-linguistique` verte, `docs/produit` écrit, 84 portes auditées, POS anglais diagnostiqué | `reports/rapport-vague-1.md` + JSON | `porte-bloc-linguistique`, `porte-produit`, `autotest`, `revue` | 1 commit : correctif + doc + fiche + état |
| **2** | 11 h 00–11 h 35 | 17 spans tranchés (4 GP corrigés ou actés), r353 qualifié, validations S inventoriées, INDEX planifié | `reports/rapport-vague-2.md` + JSON | `autotest`, `evaluer_gold`, `revue`, `liens` | 1 commit : décision spans + fiche + état + références 84 |
| **3** | 11 h 35–12 h 10 | état B13 clos, doc produit finalisée, file des tâches livrée, passe légère verte | `reports/rapport-vague-3.md` + JSON | `revue`, `tableaux`, `verifie_en_cours`, `taille_documents`, `porte-sessions` | 1 commit : état + doc + file + passe |

**Protocole de commit (arbre partagé).** `git add` explicite, jamais `-A`. Index alterné (`GIT_INDEX_FILE=/tmp/index.<session> git read-tree HEAD`), puis resynchronisation de l'index principal (`git read-tree HEAD`, sans toucher à l'arbre). Ne pas committer `tools/structures` (sous-module) ni les modifications des autres sessions. Mettre à jour les compteurs **dans le même commit** : cette fiche fait passer `reports/` de **678/771** à **679/772** ; les trois fiches de vague feraient **682/775**. La revue ne signale que les compteurs ; la navigation passe parce que la fiche se lie elle-même. Un lien depuis `reports/README.md` ou l'INDEX régénéré reste la bonne pratique.

**Ce que la fenêtre ne fait pas** : pas de passe complète (2 h 29, cf. `references:5-6`), pas d'écriture S/D/N2, pas de `git add -A`, pas de lancement de `index_reports.py` sur l'arbre partagé, pas de correction du gold synthétique (ce serait ajuster au test).

## 10. Commandes vérifiées

Vérification par `ls` et, quand l'outil le supporte, par `--help` ou une exécution réelle. Le tableau distingue **existe** de **exécutée** : une commande peut exister et coûter 2 h 29.

| commande | existe | exécutée | état observé |
|---|---|---|---|
| bash tools/toutes-les-portes.sh | oui | non (2 h 29) | 84 portes ; la passe du 06/11 a 79 vertes et 4 rouges |
| bash tools/porte-bloc-linguistique.sh | oui | oui | exit 1 ; cascade_pos 0,7465 < 0,7581 |
| bash tools/porte-produit.sh | oui | oui | exit 0 ; 6 contrôles, autotest 183/183 |
| bash tools/porte-sessions.sh | oui | oui | exit 1 ; heartbeats e181ce02 et 1e7ef596 |
| bash tools/porte-ressources.sh | oui | oui | exit 0 ; aucun serveur local, GPU libres |
| bash tools/porte-tableaux.sh | oui | oui | exit 0 |
| python3 -m tools.pensee.autotest | oui | oui | 183/183 ; T132 5/5, T133 5/5, T140 7 mots |
| python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/x.json | oui | oui | exit 1 ; verdict cascade_pos=false |
| python3 tools/revue_documentation.py | oui | oui | exit 0 à 10 h 20 ; exit 1 à 10 h 15 (compteurs) |
| python3 tools/taille_documents.py | oui | oui | exit 0 |
| python3 tools/verifie_en_cours.py | oui | oui | exit 0 |
| python3 tools/verifie_journal.py | oui | oui | exit 0 |
| python3 tools/verifier_liens.py | oui | oui | exit 0 ; 3 487 liens |
| python3 tools/verifier_schemas.py | oui | oui | exit 0 ; 67 SVG |
| python3 tools/verifie_backlog.py | oui | oui | exit 0 ; frontière 3 : A2.6, N2, N4 |
| python3 tools/sessions.py --check --strict | oui | oui | signale les deux heartbeats ; porte-sessions sort 1 |
| python3 tools/drave.py --help | oui | oui | exit 0 ; analyser, evaluer, rejouer |
| python3 tools/eval_n2_propre.py | oui | non | argparse exige un checkpoint positionnel |
| python3 tools/index_reports.py | oui | non | pas de --help ; réécrit reports/INDEX.md |
| bash tools/porte-n2.sh | non | non | Absente : l'exemple de la mission est fictif |

**Deux pièges.** `tools/porte-n2.sh` **n'existe pas** : l'exemple de la mission est fictif ; N2 n'a pas de porte unique. `tools/index_reports.py` **n'a pas de `--help`** et réécrit l'INDEX : c'est un outil de hub, pas d'audit.

## 11. Limites de cette fiche

- **Instantané daté** : 10 h 20 HNE, HEAD `7679a2d4`. L'arbre est partagé ; `en-cours` a déjà été réécrit une fois pendant l'inventaire. Les chiffres de la fiche sont ceux de cette heure.
- **Pas de passe complète** : les 4 rouges viennent du registre du 06/11 (`work/portes-1106-01h28/registre.txt`) et de rejeux ciblés ; `indice` et `melange` n'ont pas été rejouées.
- **S n'est pas mesuré** : les 19 + 150 verdicts sont lus, pas rejoués ; la couverture par phrase (certaines ont 1 verdict, d'autres 3) reste à vérifier.
- **`gold 200+` n'est pas défini** : la fiche le classe en coordination (T15) au lieu d'inventer un objet.
- **Le produit** : `porte-produit` est verte, mais ses 6 contrôles ne couvrent pas la robustesse hors gold ; l'audit de fiabilité est en cours (session `14114f3d`) et n'a pas encore écrit sa fiche.
- **Les compteurs** : cette fiche et son JSON changent le disque (679/772). Sans mise à jour d'`en-cours` dans le même commit, `revue_documentation.py` échouera — c'est attendu, pas une régression.
- **Aucune modification d'existant** : seule exception, `reports/INDEX.md` réécrit par un `--help` malencontreux, puis restauré à l'identique (`git restore`).

## 12. Fichiers

- [`rapport-file-taches.md`](rapport-file-taches.md) — cette fiche.
- [`pensee-file-taches.json`](pensee-file-taches.json) — les 29 tâches, les 6 doublons, les 18 périmées, les 12 dépendances et l'ordre des vagues, en structure.
- Sources : `docs/pilotage/roadmap.md`, `en-cours.md`, `plan-travail.md`, `backlog/index.md`, `backlog/dependances.md`, `references-non-regression.md` ; `reports/rapport-pensee-v12.md`, `rapport-dev-test-v10.md`, `rapport-audit-v10.md`, `rapport-produit-v0.md`, `rapport-a26-bilan.md`, `rapport-a26-lot-disque.md`, `rapport-n2-r12-2048.md`, `rapport-s-paragraphes.md` ; registres `work/portes-1106-01h28/registre.txt` et `work/portes/passe-2404-23h45/registre.txt`.

**Ce que cette fiche ne fait pas** : elle ne commite rien, ne modifie aucun existant, ne mesure ni S, ni D, ni N2, et ne remplace pas la passe complète. Elle rend la file **exécutable** : chaque ligne a un fichier, une dépendance, un bloquant et, quand elle existe, une commande.
