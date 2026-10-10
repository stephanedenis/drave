# État du cerveau Drave — capacités, expériences, prochaine action

> **2026-10-10 10:40 HAE** (EDT, UTC−4 — lire `date`, jamais une horloge supposée : voir
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
| **C4** | horloges par région | 🟡 premier pas | `--pas-max` borne la terminaison et **refuse un résultat partiel** (code **5**) ; asynchronisme réel : gigue **40 %** (localhost) et **49 %** (5 ms/message) ; **2,62** messages par pas après fusion des écritures | `porte-horloge.sh` · fiche 44 |
| **C5** | bus multi-canaux | ✅ fait | canal neutre ⇒ empreintes **identiques** ; gain 1,5 ⇒ la sortie change ; un bus de **relais** agit à travers les instances | `porte-bus.sh` |
| **C5bis** | bus par fichier | ✅ fait | un canal poussé de l'extérieur change la région du milieu : **66,0379** contre **59,0790** | `porte-bus.sh` |
| **C5ter** | bus par le réseau | ✅ fait | socket ≡ statique (**0,00e0**) ; neutre ≡ référence (**0,00e0**) ; plein vol ≠ les deux | `porte-bus-socket.sh` |
| **C6** | mémoire épisodique | ✅ fait | **élagage 83 %**, rappel **96,3 %** à 50 % de dégradation, round-trip **exact**, Δ = **11 jetons sur 2 048** ; le rappel dépend de **l'indice** (1 sur 8) et **n'est pas continu** (50 vs 1 006) ; la clé de fenêtre **dégrade** (prédiction réfutée) | fiches 24, 29, 30, 31 · `porte-episodique.sh`, `porte-indice.sh`, `porte-melange.sh` |
| **C7** | consolidation | ✅ fait | l'**exemplaire** bat la **moyenne** (7 % du magasin → **87 %** de rappel) ; rejeu répété = **point fixe exact** (0,00e0) | `porte-episodique.sh` |
| **C8** | réflexe | 🟡 premier pas | un chemin court ne sait **rien** : accord **0 %** jusqu'à 16/24 couches, cos **0,145** — il faut une **tête entraînée par profondeur** | `porte-reflexe.sh` · fiche 26 |
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

- **22 portes** `tools/porte-*.sh` — la **passe complète** se fait par
  `tools/toutes-les-portes.sh` (toutes, séquentiellement, bornées dans le temps, journaux
  gardés). Une porte lancée « une par une, à la main » avait laissé `porte-gain.sh` **rouge
  depuis le v7** sans que personne le voie (fiche 47).
- **122 tests** `cargo test`, crate **std seul, zéro dépendance**, profil `release` = binaire de
  mesure.
- Mesures dédiées : `tools/carte-fenetre-puits.sh` (fenêtre × puits d'attention),
  `tools/decouper-rapport.py` (un rapport par expérience), `tools/aiguille.py`,
  `tools/proxy_latence.py`.

## 6. ▶ Prochaine action

**1. Passe complète des portes** (`tools/toutes-les-portes.sh`) — verdict à consigner dans
`journal/2026-10-10.md` et dans `docs/manques.md` (la ligne « les 23 portes sont vertes » était
une affirmation sur une suite qui n'avait **jamais tourné comme une suite**).

**2. Fenêtre × puits d'attention : jusqu'où la fenêtre est-elle gratuite ?** Mesuré (fiche 47 et
carte) : à 128 jetons, l'attention complète vaut **14,6496** ; fenêtre 64 + 24 puits vaut
**14,9614** (+2,1 %) et fenêtre 16 + 32 puits **16,2566**. La question qui décide : sur
**512 jetons**, quel couple (fenêtre, puits) égale l'attention complète en ne notant qu'une
fraction des clés ? Commande : `FENETRES="64 128 256" PUITS="0 32 64" tools/carte-fenetre-puits.sh 512`.

**3. C8 (suite) — une tête entraînée par profondeur.** Le réflexe ne peut pas lire un état
intermédiaire (cos 0,145) : entraîner une tête linéaire sur l'état de la couche 16 et mesurer son
accord avec le modèle entier, avec `tools/entrainer_moteur.py`, protocole de `porte-reflexe.sh`.

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
