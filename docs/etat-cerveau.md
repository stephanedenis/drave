# État du cerveau Drave — capacités, expériences, prochaine action

> **2026-10-10 15:56 HAE** (EDT, UTC−4 — lire `date`, jamais une horloge supposée : voir
> `docs/organisation-du-depot.md` § 4). Ce fichier est **l'état**, par rapport aux roadmaps :
> ce qui est fait, avec le chiffre qui le prouve, et ce qui reste. Il ne raconte pas les rounds
> (c'est `journal/`) et ne porte pas les mesures en détail (ce sont les fiches
> `reports/campagne-benefices/`, une par expérience).
>
> Roadmaps de référence : `docs/plan-cerveau-complet.md` (les douze capacités),
> `docs/roadmap-drave.md`, `docs/modele-pour-drave.md` § 3 (dessins H/I/J),
> `docs/biologie-pour-drave.md` (expériences E1-E9), `docs/manques.md` (ce qui manque).

## 1. Les douze capacités

| # | capacité | état | le chiffre qui le prouve | où |
|---|---|---|---|---|
| **C1** | graphe de régions | ✅ fait | la topologie **pilote** le découpage : même perplexité, écart **0,00e0** ; relais 3 régions / 3 instances : **0,00e0** | `tools/porte-topologie.sh` · fiche 34 |
| **C2** | deux entrées, une règle | ✅ fait | deux entrées se **somment**, la somme **arbitre** (7/7) ; bascule à **α = 0,60** contre **0,509** prédit | fiche 03 |
| **C2/C6** | greffe d'état | ✅ fait | l'état injecté **transfère le contenu** ; ma première conclusion négative était un **décalage d'un jeton**, corrigée | fiche 28 · `porte-greffe.sh` |
| **C3** | délais par lien | ✅ fait | un délai change le **temps**, jamais un chiffre (+3,1 s pour 50 ms × 64 pas, même perplexité) ; instrument **calibré** : 50 ms injectés → **50,2** mesurés | `porte-delais.sh` · fiche 43 |
| **C4** | horloges par région | 🟡 premier pas, **et le prix du retard est mesuré** | **un état n'est valide qu'à SA position : un pas de retard coûte ×633** (14,6496 → 9 277,98) et un **état manquant** ×1,05 ⇒ politique tranchée : **on continue sans, on ne réutilise jamais** (×633 contre ×1,06) ; l'asynchronisme ne peut pas « laisser un pas prendre du retard », seulement réordonner les messages d'un même pas (`tools/porte-c4-retard.sh`, [`reports/rapport-c4-retard.md`](../reports/rapport-c4-retard.md)) ; `--pas-max` borne la terminaison et **refuse un résultat partiel** (code **5**) ; asynchronisme réel : gigue **40 %** (localhost) et **49 %** (5 ms/message) ; **2,62** messages par pas après fusion des écritures | `porte-horloge.sh` · fiche 44 |
| **C5** | bus multi-canaux | ✅ fait | canal neutre ⇒ empreintes **identiques** ; gain 1,5 ⇒ la sortie change ; un bus de **relais** agit à travers les instances | `porte-bus.sh` |
| **C5bis** | bus par fichier | ✅ fait | un canal poussé de l'extérieur change la région du milieu : **66,0379** contre **59,0790** | `porte-bus.sh` |
| **C5ter** | bus par le réseau | ✅ fait | socket ≡ statique (**0,00e0**) ; neutre ≡ référence (**0,00e0**) ; plein vol ≠ les deux | `porte-bus-socket.sh` |
| **C6** | mémoire épisodique | ✅ fait | **élagage 83 %**, rappel **96,3 %** à 50 % de dégradation, round-trip **exact**, Δ = **11 jetons sur 2 048** ; le rappel dépend de **l'indice** (1 sur 8) et **n'est pas continu** (50 vs 1 006) ; la clé de fenêtre **dégrade** (prédiction réfutée) | fiches 24, 29, 30, 31 · `porte-episodique.sh`, `porte-indice.sh`, `porte-melange.sh` |
| **C7** | consolidation | ✅ fait | l'**exemplaire** bat la **moyenne** (7 % du magasin → **87 %** de rappel) ; rejeu répété = **point fixe exact** (0,00e0) | `porte-episodique.sh` |
| **C8** | périphérie et réflexes (plan § C8) | 🟢 **périphérie LIVRÉE et réflexe mesuré ; la mémoire du signal manque** | sur **le même texte**, le chemin tronqué à 16 couches passe de **456 586,60** (tête empruntée) à **845,45** (adaptateur entraîné, test sur positions jamais vues) : **÷540** — le modèle complet vaut **14,2342** sur ce texte, donc le réflexe reste **×59** derrière. Ça surapprend vite (meilleur test à l'époque 6, ×127 train/test à la fin) ; **sur un texte JAMAIS VU** : avec 30 morceaux d'entraînement (le morceau de test exclu), la tête empruntée rend **697 572** et la tête entraînée **84,99**, à **×5,7** du modèle complet (15,02) ; avec 7 morceaux seulement : 202,17 — **les données comptent**, et **la non-linéarité n'aide pas** à cette échelle (272 contre 51 au linéaire) ; et **il va plus vite** : ×1,54 en génération, TTFT ÷2,4 ⇒ le compromis est **×1,54 de vitesse pour ×59** (même texte), **×5,7** (texte neuf) ou **×25** (autre corpus) d'écart au modèle complet | `porte-reflexe.sh` · fiches 26, [`sonde-profondeur`](../reports/rapport-c8-sonde-profondeur.md), [`tête entraînée`](../reports/rapport-c8-tete-entrainee.md), [`généralisation`](../reports/rapport-c8-generalisation.md), [`transfert de corpus`](../reports/rapport-c8-transfert-corpus.md) |
> **Ce que « C8 » recouvre, et où on en est.** Le plan (`docs/plan-cerveau-complet.md` § C8) définit
> C8 comme la **périphérie** : des régions frontière d'**entrée** et de **sortie**, et des
> **réflexes** — des liens qui court-circuitent le graphe profond — avec pour invariant « entrée
> constante ⇒ sortie constante » et pour validation une **tâche fermée** mesurée en événements par
> décision. Ce qui est mesuré ici est la moitié **réflexe** : un chemin court qui lit un état
> intermédiaire, sa tête entraînée, sa généralisation et sa vitesse. Les interfaces sont **livrées** :
> `--entree signal:F`, `--entree-canal/-gain/-jeton`, `--delai N`, `--recurent`, `--sortie F`, avec
> la porte `tools/porte-peripherie.sh` (déterminisme au bit près, entrée constante ⇒ sortie
> constante, délai exact, quatre refus, paires par décision). La **tâche fermée** est mesurée :
> le signal **courant** est dans la sortie (R² **0,992** en récurrent, 4 096 pas) mais **pas** le
> signal d'il y a 8 pas (R² **−0,681**, et une lecture **non linéaire** ne le trouve pas non plus).
> Deux références tranchent : un **tampon de 8 pas** résout la tâche exactement (R² 1,000) et une
> **récurrence qui fuit** n'y arrive pas (0,104 — un intégrateur rend la *somme*, pas le pas d'il y
> a 8). Remettre le passé **en entrée** (`--entree-memoire 8`, en récurrent) le rend **partiellement**
> lisible : R² **+0,283** contre −0,399 sans. **Retenir demande une STRUCTURE — un tampon lu
> directement (R² 1,000), pas la transformation du réseau** — et c'est le deuxième manque de C8
> après la tête réflexe. **La conception de cette structure est écrite avec ses quatre portes**
> dans [`docs/note-peripherie-c8.md`](note-peripherie-c8.md) § 6 (mémoire exacte, coût nul en paires,
> pas d'amélioration par réinjection, bornage explicite). Détail :
> [`reports/rapport-c8-peripherie.md`](../reports/rapport-c8-peripherie.md) · conception :
> [`docs/note-peripherie-c8.md`](note-peripherie-c8.md).
| **C9 (latéralité)** | deux jumeaux, échange par couche | 🟡 **échange exact, gain NUL (mesuré)** | échange désactivé = modèle seul (27,4964 = 27,4964) ; jumeaux identiques ⇒ rien ne change ; jumeau bruité récupéré (163,17 → 36,13) **mais le contrôle donne le même chiffre** (36,1307, écart 0,000 %) : c'est une moyenne, pas une latéralité. La fusion de deux **vues valides** ne bat pas la meilleure des deux (127 jetons : 15,39 contre 14,65) | `tools/porte-jumeaux.sh` · [`reports/rapport-c9-lateralite.md`](../reports/rapport-c9-lateralite.md) |
| **C9** | pont entre régions | ✅ fait | **448 fibres = +2,81 %** et **÷1,8** en octets ; falaise **entre 448 et 392** ; à budget égal **quantifier bat élaguer de 83 %** | `porte-pont.sh` · fiche 25 |
| **C9×C1** | où couper | ✅ fait | **8 coupes, une seule perplexité (113,0068)** sans perte ; le coût du pont va de **+0,52 %** (coupe après 18 couches) à **+17,09 %** (après 15) — facteur **30** ⇒ **couper tard** | `porte-coupe.sh`, `tools/carte_coupe.sh` · fiche 27 |
| **C10** | budgets | ✅ **clos** | trois budgets, trois codes distincts : octets (**6**), latence (**8**), paires (**9**) ; loi de latence **3,4 ms/token par ms de RTT** | fiches 32, 42 |
| **C11** | pannes et registre | ✅ fait | panne de lien **nommée**, code **7**, jamais de résultat partiel ; le **registre de régions** remplace les adresses dans les topologies | `porte-pannes.sh`, `porte-registre.sh` · fiches 33, 35 |
| **C12** | trace globale | ✅ fait | **126 croisements**, aucune divergence ; une trace faussée d'**un bit** est détectée et nommée | `porte-trace.sh` |
| **C12bis** | trace du nœud, fusion | ✅ fait | **94 liens** identiques ; 1 bit changé ⇒ **DIVERGENT** (code 3) ; format v1 **refusé** | `porte-fusion.sh` |

## 2. Le chemin réparti (ce qui compte pour « distribuable »)

- **Protocole v8** (trame de 99 octets) : les réglages **voyagent** — fenêtre d'attention,
  motif, puits d'attention, top-k, seuils, niveaux — et le nœud **annonce son compte de paires**
  (u64), donc le pilote sait ce que coûte la moitié distante.
- **Ce qui a été corrigé parce que ça ne voyageait pas ou n'agissait pas** : `--ffn-gain` (round 20),
  `--attn-window`/`--swa-pattern`/`--attn-sinks` côté **pilote** (round 42), le budget de **paires**
  (v8), et **`--attn-sinks 0`**, qui était **inexprimable** (10 octobre, fiche 47).
- **Économie du lien** : latence **3,4 ms/token par ms de RTT** ; pas = **4 messages** → **2,62**
  après fusion des écritures (−20 % de durée de pas à 5 ms/message).
- **Ce qui reste** : l'asynchronisme réel (C4) et l'ordonnanceur qui le tolère (gigue 49 %).

## 3. Expériences de biologie (`docs/biologie-pour-drave.md`)

| # | expérience | état | chiffre |
|---|---|---|---|
| **E1** | connectome inné | ✅ | un connectome **aléatoire** coûte **1 %** de perplexité et **divise les lectures par 4** (25 %) ; à 12,5 % : +13,7 % |
| **E3** | deux axes appris | ✅ | ÷2 lectures à qualité égale ; ÷7,8 à dim 384 |
| **E4** | équilibre excitation/inhibition | ✅ | l'hypothèse est vraie **dans un seul sens** : l'inhibition **dégrade** de façon monotone (15,6908 → 19,4791 à la couche 12) ; l'optimum **intérieur** est du côté **amplification** (couche 0, gain 0,75 : **12,9635** contre 14,6496, **−11,5 %**) ; **falaise** à 0,25 (996,04) ; **les gains ne se composent pas** |
| **E6** | poids log-normaux | ❌ échec de code | le fichier sauvé **ne reproduit pas** le modèle entraîné (13,0614 contre 2,2662 bits/octet) — manque **M8**, cause ouverte |
| **E7/E8** | nouveauté, décorrélation | ✅ mesurées | la nouveauté **empire** la règle ; la décorrélation est **inerte**, et sa courbe de dose converge vers « ne rien apprendre » |
| **E2/E5** | croissance des connexions, rejeu | ⏳ cadrées | leviers présents dans le moteur, protocole à écrire |
| **E9** | — | ⏳ | — |

## 4. Dessins de modèle (`docs/modele-pour-drave.md` § 3)

- **I — profondeur routée** : mesuré (**−11,5 %** au gain 0,75 de la couche 0), mais **2 couches
  utiles seulement** et la composition des gains **dégrade** ; à entraîner pour de vrai.
- **H — budget d'événements appris** et **J — quantification adaptée aux listes** : dessins
  évalués, **jamais entraînés** (manque **N4**).

## 5. Les instruments (et leur état au 10 octobre)

- **25 portes** `tools/porte-*.sh` — **passe complète le 2026-10-10 19 h 10 : 25 vertes sur 25, 57 min**
  (`tools/toutes-les-portes.sh`, chaque porte bornée, journaux gardés ; détail dans
  `reports/rapport-passe-complete-portes.md`). La passe a servi à deux choses : elle a montré que
  `porte-gain.sh` § 9 était **rouge depuis le v7** (elle exigeait un refus que le v7 a retiré), et
  elle a démasqué `porte-tokenizer-kimi.sh` **verte en ne comparant aucun jeton** (elle lisait
  `stdin`, que personne ne lui fournissait) — corrigée, elle compare 10 textes en 7,5 s.
- **122 tests** `cargo test`, crate **std seul, zéro dépendance**, profil `release` = binaire de
  mesure.
- Mesures dédiées : `tools/carte-fenetre-puits.sh` (fenêtre × puits d'attention),
  `tools/decouper-rapport.py` (un rapport par expérience), `tools/aiguille.py`,
  `tools/proxy_latence.py`.

## 6. ▶ Prochaine action

**1. Passe complète des portes** (`tools/toutes-les-portes.sh`) — verdict à consigner dans
`journal/2026-10-10.md` et dans `docs/manques.md` (la ligne « les 23 portes sont vertes » était
une affirmation sur une suite qui n'avait **jamais tourné comme une suite**).

**2. Fenêtre × puits d'attention — MESURÉ : le DRAIN porte la qualité** (fiche
[`reports/rapport-fenetre-puits-attention.md`](../reports/rapport-fenetre-puits-attention.md)).
À **512 jetons**, **fenêtre 128 + 64 puits** = **13,3968** contre **13,1368** (**+2,0 %**) pour
**192 clés sur 512** (**÷2,67**). À **2 048 jetons**, la grille étendue tranche : **fenêtre 512 +
512 puits** rend **10,4046** contre **10,3703** (**+0,33 %**) pour **1 024 clés sur 2 048**
(**÷2**), et **fenêtre 1 024 + 128 puits** rend **10,3652** pour **÷1,78**. Autrement dit : **le
drain doit grandir avec la séquence**, et il porte l'information du début que la fenêtre coupe —
quelques puits suffisent à *drainer*, il en faut beaucoup plus pour *porter*. Zéro puits
**casse** le modèle (1297,54 à fenêtre 32 contre 29,02 à 4). À **4 096 jetons**, la frontière se
déplace : (512, 512) coûte **+5,4 %** (12,8824 contre 12,2177) et (1 024, 1 024) **+1,9 %**
(12,4466) — **le prix croît avec N à fraction de clés constante**, et garder **la moitié** des
clés reste le régime sûr. **Prix réel en temps, mesuré** (débit, 4 096 jetons, machine au repos) :
attention complète **17,1 tok/s** ; fenêtre 512 + 512 puits (÷4 de clés) **19,1 tok/s**, soit
**+12 %** seulement ; les configurations plus larges sont dans le bruit. **La fenêtre est un levier
de parcimonie (clés, paires, octets), pas de vitesse locale** — c'est en réparti qu'elle paie.
Reste ouvert : la loi de la frontière en N.

**0. C9 (latéralité) et C4 (retard) — mesurés, leurs suites sont nommées.** Latéralité : l'échange
est exact, le gain entre deux vues est **nul** (et la récupération d'un jumeau bruité = une moyenne,
contrôle à 0,000 %) — la suite plausible est `--echange experts` sur un modèle routé
([`rapport-c9-lateralite.md`](../reports/rapport-c9-lateralite.md)) ; le coût compressé est de
**÷4 d'octets pour +3,0 %** (8 bits par bloc), et quantifier bat élaguer **encore**. Retard : un pas
coûte **×633**, un état manquant **×1,06** ⇒ l'ordonnanceur **continue sans** et ne réutilise jamais
([`rapport-c4-retard.md`](../reports/rapport-c4-retard.md)).

**3. C8 — la tête entraînée généralise (÷540 même texte, ×5,7 du modèle sur un texte neuf avec 30 morceaux) ; reste l'échelle.** Décodabilité mesurée à 4, 8, 12, 16,
20 et 24 couches (45,9 / 45,5 / 46,1 / 40,8 / 37,8 / 34,8 % parmi les 256 plus fréquents) contre
qualité du chemin tronqué (12,4 M / 3,8 M / 3,3 M / 1,13 M / 3 210 / 9,43). L'information est là
tôt, la qualité n'arrive que tard : **le maillon faible est la tête**, et la suite est une tête
**non linéaire** entraînée par profondeur, jugée à sa **perplexité**. C'est fait pour un
**adaptateur** sur **un texte** : **845,45** contre 456 586,60 (÷540), à ×59 du modèle complet.
La généralisation est mesurée ([`rapport-c8-generalisation.md`](../reports/rapport-c8-generalisation.md)) :
**85** sur un morceau tenu à l'écart (30 morceaux d'entraînement) contre 15,02 pour le modèle
complet, 202 avec 7 morceaux — la non-linéarité n'aide pas à cette échelle, faute de réglage. Et
le **transfert à un autre corpus** est mesuré ([`rapport-c8-transfert-corpus.md`](../reports/rapport-c8-transfert-corpus.md)) :
entraînée sur la campagne et testée sur de la **prose**, la tête rend **210,21** contre
**363 649** pour la tête empruntée (÷1 730), à ×25 du modèle complet — le coût du domaine est
**×2,6**. Le **transfert inter-langue** a été tenté ([`rapport-c8-inter-langue.md`](../reports/rapport-c8-inter-langue.md)) :
il **échoue** (aucun gain depuis le français sur un morceau multilingue) — mais le corpus est
l'UDHR **parallèle**, donc les morceaux ne sont pas indépendants, et le chiffre « 3,1 contre 29,9 »
qui semblait donner raison à la tête est une **recopie de contenu**. Le protocole propre reste à
faire : découper **par langue** au lieu de découper en morceaux consécutifs. Les autres questions :
la **régularisation**, et **qualité × vitesse par profondeur**. Outils : `tools/c8_entrainer_tete.py`, `tools/c8_corpus.sh`,
`tools/c8_carte_profondeur.sh`, `tools/c8_sonde_lineaire.py`.

## 7. Les corrections à ne pas réintroduire

1. `--limit` **diffère selon le chemin** (`--ppl` = N premiers jetons, `--ppl-reparti` = N
   derniers) ⇒ dans une porte, compter les jetons du fichier ;
2. une position ne se devine pas : `--tokenize` ≠ `--prompt` ⇒ `--etat-fin` (k-ième depuis la fin) ;
3. `..Default::default()` donne **0,0** à un f32 (un poids de greffe nul, en silence) ;
4. `sys.exit("message")` sort **toujours en 1** — une porte « verte » rendait 1 ;
5. une porte rouge s'instruit **jusqu'à sa cause** (la rouge de répartition accusait le modèle,
   c'était la porte) ;
6. **deux nombres égaux ne prouvent pas qu'ils mesurent la même chose** (18,5520 = 18,5520 était
   deux réglages inertes ; 0 ≡ 4 puits était un zéro **avalé**) ;
7. **une mesure d'inertie faite là où l'inertie est attendue ne dit rien** (les puits d'attention
   sont inertes **sans fenêtre** — par construction) ;
8. un **zéro inexprimable** est un défaut : `if drapeau > 0` transforme « zéro » en « défaut ».
