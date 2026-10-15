# État du cerveau Drave — capacités, expériences, prochaine action

> **2026-10-12 16:45 HAE** (EDT, UTC−4 — lire `date`, jamais une horloge supposée : voir
> `docs/organisation-du-depot.md` § 4). Ce fichier est **l'état**, par rapport aux roadmaps :
> ce qui est fait, avec le chiffre qui le prouve, et ce qui reste. Il ne raconte pas les rounds
> (c'est `journal/`) et ne porte pas les mesures en détail (ce sont les fiches
> `reports/campagne-benefices/`, une par expérience).
>
> **Révision du 12/10 — le plan de travail (§ 6), et lui seul.** Trois constats, chacun vérifié :
> une action était **périmée** (la carte des sorties de H avait tourné le 11/10 à 00 h 15, le plan
> la disait « reste à lancer ») ; une **manquait** (le moteur ne voit pas l'array NVMe, que le
> § 7.2 de `docs/configuration-nvme-raid-amd.md` attend sur le nœud 1) ; une **exception tombe**
> (`porte-topologie.sh` après un redémarrage — sortie vérifiée le 12/10). Le chantier des
> **lecteurs parallèles** y entre avec le chiffre qui manquait (×3,8 entre 1 et 8 lecteurs sur
> l'array). **Aucun chiffre de capacité n'a bougé** : `git log --since="2026-10-11 06:30" --
> drave-core/src` est **vide**, donc les 34 portes vertes du 11/10 restent valides. Fiche de la
> machine : [`reports/rapport-raid0-nvme.md`](../reports/rapport-raid0-nvme.md).
>
> Roadmaps de référence : `docs/plan-cerveau-complet.md` (les douze capacités),
> `docs/roadmap-drave.md`, `docs/modele-pour-drave.md` § 3 (dessins H/I/J),
> `docs/biologie-pour-drave.md` (expériences E1-E9), `docs/manques.md` (ce qui manque).

## 1. Les douze capacités

| # | capacité | état | le chiffre qui le prouve | où |
|---|---|---|---|---|
| **C1** | graphe de régions | ✅ fait | la topologie **pilote** le découpage : même perplexité, écart **0,00e0** ; relais 3 régions / 3 instances : **0,00e0** | `tools/porte-topologie.sh` · fiche 34 |
| **C2 (cycle 2 régions)** | la validation du plan | ✅ **FAIT le 14/10 — et le cycle non entraîné DIVERGE** | le validateur accepte un cycle **si et seulement si** un de ses liens est `recurrent` avec `delai_ms` > 0 ; le pilote `tools/derouler.py` **déroule** les pas de temps (état brut transporté par `DRAVE_ETAT_ENTREE`, format REFD). Mesuré : deux régions enchaînées = le modèle d'un seul tenant (**14,6496 = 14,6496**, écart **0,00e0**), le **pas 1** du graphe récurrent = cette même référence (**0,00e0**), puis la boucle amplifie : **275,52 → 940,22 → 2 988,46** en 4 pas ; trajectoire **déterministe** (`cmp`), coût publié (**N pas × régions** exécutions), refus en **code 3** (cycle nu, récurrent sans délai) et **code 2** (pilote : `--pas-temps 0`, région distante, entrées multiples) | `porte-cycle-c2.sh` · [`rapport-cycle-c2.md`](../reports/rapport-cycle-c2.md) · [`note-cycle-c2.md`](note-cycle-c2.md) |
| **C2 (récurrence)** | boucle sur soi (`--recurrence α`) | 🟡 **implémentée, bornée… et NUISIBLE** | le zéro est exact au bit près, la boucle est déterministe et ne coûte aucune paire ; mais la lecture du signal **présent** tombe de R² **0,906** à **0,112** (α = 0,5) et celle du passé de −0,35 à **−4,87** : la boucle réinjecte la **transformation** du réseau, pas son entrée ⇒ un écho, pas une mémoire | `tools/porte-recurrence.sh` · [`rapport-c2-recurrence.md`](../reports/rapport-c2-recurrence.md) |
| **C2** | deux entrées, une règle | ✅ fait | deux entrées se **somment**, la somme **arbitre** (7/7) ; bascule à **α = 0,60** contre **0,509** prédit | fiche 03 |
| **C2/C6** | greffe d'état | ✅ fait | l'état injecté **transfère le contenu** ; ma première conclusion négative était un **décalage d'un jeton**, corrigée | fiche 28 · `porte-greffe.sh` |
| **C3** | délais par lien | ✅ fait | un délai change le **temps**, jamais un chiffre (+3,1 s pour 50 ms × 64 pas, même perplexité) ; instrument **calibré** : 50 ms injectés → **50,2** mesurés | `porte-delais.sh` · fiche 43 |
| **C4** | horloges par région | 🟡 premier pas, **et le prix du retard est mesuré** | **un état n'est valide qu'à SA position : un pas de retard coûte ×633** (14,6496 → 9 277,98) et un **état manquant** ×1,05 ⇒ politique tranchée : **on continue sans, on ne réutilise jamais** (×633 contre ×1,06) ; l'asynchronisme ne peut pas « laisser un pas prendre du retard », seulement réordonner les messages d'un même pas (`tools/porte-c4-retard.sh`, [`reports/rapport-c4-retard.md`](../reports/rapport-c4-retard.md)) ; `--pas-max` borne la terminaison et **refuse un résultat partiel** (code **5**) ; asynchronisme réel : gigue **40 %** (localhost) et **49 %** (5 ms/message) ; **2,62** messages par pas après fusion des écritures | `porte-horloge.sh` · fiche 44 |
| **C5** | bus multi-canaux | ✅ fait | canal neutre ⇒ empreintes **identiques** ; gain 1,5 ⇒ la sortie change ; un bus de **relais** agit à travers les instances | `porte-bus.sh` |
| **C5bis** | bus par fichier | ✅ fait | un canal poussé de l'extérieur change la région du milieu : **66,0379** contre **59,0790** | `porte-bus.sh` |
| **C5ter** | bus par le réseau | ✅ fait | socket ≡ statique (**0,00e0**) ; neutre ≡ référence (**0,00e0**) ; plein vol ≠ les deux | `porte-bus-socket.sh` |
| **C6** | mémoire épisodique | ✅ fait | **élagage 83 %**, rappel **96,3 %** à 50 % de dégradation, round-trip **exact**, Δ = **11 jetons sur 2 048** ; le rappel dépend de **l'indice** (1 sur 8) et **n'est pas continu** (50 vs 1 006) ; la clé de fenêtre **dégrade** (prédiction réfutée) | fiches 24, 29, 30, 31 · `porte-episodique.sh`, `porte-indice.sh`, `porte-melange.sh` |
| **C7** | consolidation | ✅ **fait, et désormais mesurée DANS LES POIDS (14/10)** | l'**exemplaire** bat la **moyenne** (7 % du magasin → **87 %** de rappel) ; rejeu répété = **point fixe exact** (0,00e0) ; et la consolidation par rejeu **change le modèle** : LoRA rang 8 sur 8 couches (**0,07 %** des paramètres), 2 époques sur 10 morceaux ⇒ le MOTEUR rend, sur des textes **jamais rejoués**, m20 **19,1247 → 15,9804** (**−16,4 %**) et m32 **7,4250 → 6,9333** (**−6,6 %**) — mais **+1,3 %** sur un **autre corpus** : elle **spécialise**. Contrôles : LoRA nul ⇒ GGUF **identique au bit**, LoRA aléatoire ⇒ **+1,5 %** (la borne du « gain gratuit »), rejeu **mélangé** ⇒ validation ×8 et époque choisie **0** (rien n'est publié) | `porte-consolidation.sh`, `porte-episodique.sh` · [`rapport-consolidation-c7.md`](../reports/rapport-consolidation-c7.md) **Courbe du sommeil (14/10, 23 h)** : −5,57 % (3 morceaux rejoués), −6,70 % (6), −7,67 % (10), **−9,98 %** (20) sur un texte jamais rejoué ; le coût hors domaine est **bruité** (−0,41 à +3,30 %) — le point le plus efficient est le rejeu **court** ([`rapport-sommeil-budget.md`](../reports/rapport-sommeil-budget.md)). **Et les facultés COMPOSENT** : `tools/porte-cerveau.sh` (43ᵉ porte) exécute entrée + mémoire + délai + récurrence **dans une seule commande** et vérifie que chacune agit encore (quatre sorties distinctes, déterminisme au bit près). |
| **C8** | périphérie et réflexes (plan § C8) | ✅ **périphérie + mémoire livrées, réflexe mesuré** | sur **le même texte**, le chemin tronqué à 16 couches passe de **456 586,60** (tête empruntée) à **845,45** (adaptateur entraîné, test sur positions jamais vues) : **÷540** — le modèle complet vaut **14,2342** sur ce texte, donc le réflexe reste **×59** derrière. Ça surapprend vite (meilleur test à l'époque 6, ×127 train/test à la fin) ; **sur un texte JAMAIS VU** : avec 30 morceaux d'entraînement (le morceau de test exclu), la tête empruntée rend **697 572** et la tête entraînée **84,99**, à **×5,7** du modèle complet (15,02) ; avec 7 morceaux seulement : 202,17 — **les données comptent**, et **la non-linéarité n'aide pas** à cette échelle (272 contre 51 au linéaire) ; et **il va plus vite** : ×1,54 en génération, TTFT ÷2,4 ⇒ le compromis est **×1,54 de vitesse pour ×59** (même texte), **×5,7** (texte neuf) ou **×25** (autre corpus) d'écart au modèle complet | `porte-reflexe.sh` · fiches 26, [`sonde-profondeur`](../reports/rapport-c8-sonde-profondeur.md), [`tête entraînée`](../reports/rapport-c8-tete-entrainee.md), [`généralisation`](../reports/rapport-c8-generalisation.md), [`transfert de corpus`](../reports/rapport-c8-transfert-corpus.md) |
| **C9 (latéralité)** | deux jumeaux, échange par couche | 🟡 **échange exact, gain NUL (mesuré)** | échange désactivé = modèle seul (27,4964 = 27,4964) ; jumeaux identiques ⇒ rien ne change ; jumeau bruité récupéré (163,17 → 36,13) **mais le contrôle donne le même chiffre** (36,1307, écart 0,000 %) : c'est une moyenne, pas une latéralité. La fusion de deux **vues valides** ne bat pas la meilleure des deux (127 jetons : 15,39 contre 14,65) | `tools/porte-jumeaux.sh` · [`reports/rapport-c9-lateralite.md`](../reports/rapport-c9-lateralite.md) |
| **C9** | pont entre régions | ✅ fait | **448 fibres = +2,81 %** et **÷1,8** en octets ; falaise **entre 448 et 392** ; à budget égal **quantifier bat élaguer de 83 %** | `porte-pont.sh` · fiche 25 |
| **C9×C1** | où couper | ✅ fait | **8 coupes, une seule perplexité (113,0068)** sans perte ; le coût du pont va de **+0,52 %** (coupe après 18 couches) à **+17,09 %** (après 15) — facteur **30** ⇒ **couper tard** | `porte-coupe.sh`, `tools/carte_coupe.sh` · fiche 27 |
| **C10** | budgets | ✅ **clos** | trois budgets, trois codes distincts : octets (**6**), latence (**8**), paires (**9**) ; loi de latence **3,4 ms/token par ms de RTT** | fiches 32, 42 |
| **C11** | pannes et registre | ✅ fait | panne de lien **nommée**, code **7**, jamais de résultat partiel ; le **registre de régions** remplace les adresses dans les topologies | `porte-pannes.sh`, `porte-registre.sh` · fiches 33, 35 |
| **C12** | trace globale | ✅ fait | **126 croisements**, aucune divergence ; une trace faussée d'**un bit** est détectée et nommée | `porte-trace.sh` |
| **C12bis** | trace du nœud, fusion | ✅ fait | **94 liens** identiques ; 1 bit changé ⇒ **DIVERGENT** (code 3) ; format v1 **refusé** | `porte-fusion.sh` |

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
> après la tête réflexe. **La structure est LIVRÉE** (`--memoire K`, `--sortie-memoire F`,
> `tools/porte-memoire.sh`) : la poursuite de `v[t−8]` depuis la mémoire donne **R² 1,000 et une
> erreur nulle**, pour **aucune paire de plus**. **La conception d'origine**
> dans [`docs/note-peripherie-c8.md`](note-peripherie-c8.md) § 6 (mémoire exacte, coût nul en paires,
> pas d'amélioration par réinjection, bornage explicite). Détail :
> [`reports/rapport-c8-peripherie.md`](../reports/rapport-c8-peripherie.md) · conception :
> [`docs/note-peripherie-c8.md`](note-peripherie-c8.md).


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
| **E1** | connectome inné | ✅ **RE-MESURÉ le 11/10 : il coûte 9 %, pas 1 %** | masque aléatoire fixé à la naissance, **couverture vérifiée dans le fichier** (24,0 % d'occupation pour 25 % demandés) : **8,0317** à 25 % (**+9,4 %**) et **8,6970** à 12,5 % (**+18,4 %**) contre **7,3429** au témoin dense. L'ancien « 1 % » décrivait l'**attention seule** (le masque ne couvrait que les `nn.Linear`, 5,8 % des poids) ([`rapport-e1-e2-connectome-croissance.md`](../reports/rapport-e1-e2-connectome-croissance.md)) |
| **E3** | deux axes appris | ✅ | ÷2 lectures à qualité égale ; ÷7,8 à dim 384 |
| **E4** | équilibre E/I (inférence **et** entraînement) | ✅ | l'hypothèse est vraie **dans un seul sens** : l'inhibition **dégrade** de façon monotone (15,6908 → 19,4791 à la couche 12) ; l'optimum **intérieur** est du côté **amplification** (couche 0, gain 0,75 : **12,9635** contre 14,6496, **−11,5 %**) ; **falaise** à 0,25 (996,04) ; **les gains ne se composent pas** ; **côté entraînement, le ratio cortical de signes COÛTE** : 0,5 → 2,2729 bits/octet, 0,8 → 2,3838 (+4,9 %), 0,9 → 2,5188 (+10,8 %), dégradation monotone ([`rapport-e4-ratio-signes.md`](../reports/rapport-e4-ratio-signes.md)) |
| **E6** | poids log-normaux | ⚠️ **chiffres RÉTRACTÉS, puis corrigés** | le plan 2×2 refait proprement (occupation identique dans les quatre cases) : à **25 %** gardés — dense **49,4291** · signes figés + magnitudes libres **41,6677** · log-normal signes libres **59,1526** · log-normal signes figés **71,1531**. ⇒ **la loi log-normale COÛTE** (seul effet cohérent, ×1,20 à ×1,71) et **la contrainte de signe n'a pas d'effet cohérent** (×1,19 dans un sens, ×0,83 dans l'autre : interaction). Les chiffres du 11/10 annonçant ×1,09 et « trois graines » sont **retirés** : ils venaient de deux défauts du harnais (l'attention n'était pas élaguée pour les variantes reparamétrées ; l'inverse était appliqué deux fois à l'installation, poids ±12 au lieu de ±0,08). Les deux défauts sont **rallumables** et surveillés par `tools/porte-harnais-invariants.sh` ([`rapport`](../reports/rapport-e6-poids-lognormaux.md)) |
| **E7/E8** | nouveauté, décorrélation | ✅ mesurées | la nouveauté **empire** la règle ; la décorrélation est **inerte**, et sa courbe de dose converge vers « ne rien apprendre » |
| **E2** | croissance des connexions | 🟡 **RE-MESURÉE : la conclusion publiée est RENVERSÉE** | la croissance locale (10 % → 25 %, connexions choisies par le ∣gradient∣ accumulé) donne **8,1550** à 20,9 % d'occupation, contre **8,1827** pour un masque **statique** à densité égale (20,3 %) et **8,6970** à 12,9 % : elle n'est donc **pas « pire que le hasard »**, elle est légèrement meilleure (0,3 %, dans le bruit d'une graine). L'ancien verdict venait du même défaut de couverture **et** d'un gradient lu sur `mod.weight.grad` (qui vaut `None` quand le poids est reparamétré : la croissance ne voyait aucun gradient). Les deux sont corrigés et surveillés par `porte-audit-drapeaux.sh` ([`rapport-e1-e2-connectome-croissance.md`](../reports/rapport-e1-e2-connectome-croissance.md)) |
| **E5** | rejeu et distillation | ⏳ cadrée | le moteur trace et rejoue (C7 : point fixe exact) ; l'outil de distillation existe |
| **E9** | — | ⏳ | — |

## 4. Dessins de modèle (`docs/modele-pour-drave.md` § 3)

> **Les lettres H et I étaient INVERSÉES ici** jusqu'au 10/10 (cet état appelait « I » la profondeur
> routée et « H » le budget d'événements). La référence est `docs/modele-pour-drave.md` § 3 :
> **H = routage par profondeur**, **I = budget d'événements appris**, **J = quantification par
> listes**. Corrigé, parce que deux documents qui permutent deux lettres rendent toute citation
> ambiguë.

- **H — profondeur routée** : **borne MESURÉE le 10/10, et la CARTE DES SORTIES tranche** — l'oracle
  **parfait** ne peut sortir tôt que **28,76 · 30,93 · 41,98 · 42,33 %** des jetons selon qu'on sort
  à **12 · 16 · 20 · 22** couches sur 24, soit au mieux **12,6 %** des paires (et c'est la sortie la
  plus **précoce** qui gagne : 25 % de 12 couches battent 42 % de 2). Un routeur **réel** (seuil de
  confiance) n'atteint la parité qu'à la sortie **22** — **+0,05 point**, dans le bruit — pour
  **0,39 %** des paires : entre la borne et le gain atteignable il y a un facteur **32**. Le facteur
  limitant est le **chemin court** (un adaptateur posé après coup, 20-30 % de justesse contre
  47,73 %), pas le routeur — manque **N4**. Chaîne hors-ligne vérifiée *contre* le moteur (0,013 % et
  0,006 %). [`borne`](../reports/rapport-design-H-profondeur-routee.md) ·
  [`carte des sorties`](../reports/rapport-design-H-carte-sorties.md) ·
  `tools/porte-profondeur-routee.sh`, `tools/carte-sortie-profondeur.sh`.
- **Gain par couche** (`--gain`, mesuré à part) : couche 0 à 0,75 ⇒ **−11,5 %** de perplexité, mais
  **2 couches utiles seulement** et la composition des gains **dégrade**. Ce n'est pas H : c'est
  une réduction d'activations dans une couche, pas un saut de couche.
- **I — budget d'événements appris** et **J — quantification adaptée aux listes** : dessins
  évalués, **jamais entraînés** (manque **N4**).

## 5. Les instruments (et leur état au 10 octobre)

- **39 portes** `tools/porte-*.sh` — **passe du 2026-10-13 à 13 h 44 : 37 vertes, 2 rouges**
  (~82 min), les deux rouges étant `porte-indice` (le critère
  **contrôle apparié** du 13/10 : l'indice réel ne bat pas le témoin) et `porte-melange` (le
  mélange ne rend pas le code de A — nommés dans `docs/references-non-regression.md`). La passe du
  **2026-10-11 à 06 h 30** en comptait **34 vertes sur 34** (85 min 8 s) ; trois sont nées le
  12/10 : **`porte-prechargement.sh`** (S4 : à la
  demande / `madvise` / fils / tampons, cache évincé avant chaque bras), **`porte-m5-brouillon.sh`**
  (le fichier déclare ses 3 couches de brouillon et les porte — vue rouge sur un modèle qui ne les
  déclare pas), **`porte-push-paresseux.sh`** (la forme « listes » paresseuse rend le même texte
  gourmand, et vue rouge avec `DRAVE_PUSH_FAUX=1`) **`porte-tableaux.sh`** (un tableau Markdown
  au mauvais nombre de cellules ne rend pas — et personne ne le voit) et
  **`porte-echange-experts.sh`** (le routage imposé est inerte par défaut, **exact** sur son propre
  routage — vu rouge sans `DRAVE_TRACE_EXPERTS_ORDRE` — et vivant sur un routage étranger). Repères :
  `docs/references-non-regression.md`. La nuit
  en a ajouté **six** — sauvegarde du modèle, occupation × élagage, invariants du harnais, audit des
  drapeaux, occupation du moteur, poids creux — et **chacune a été vue ROUGE** avec son défaut
  rallumé par une variable d'environnement : c'est ce qui distingue une porte d'une décoration. La
  veille au soir, la passe avait montré que `porte-gain.sh` § 9 était **rouge depuis le v7** et
  démasqué `porte-tokenizer-kimi.sh` **verte en ne comparant aucun jeton**.
  Une porte a été **retirée** : `porte-signes-figes.sh`, dont le seuil de qualité mesurait un
  artefact (elle est devenue rouge toute seule une fois le défaut corrigé) — remplacée par
  `porte-harnais-invariants.sh`, qui verrouille les **invariants** au lieu d'un résultat.
- **122 tests** `cargo test`, crate **std seul, zéro dépendance**, profil `release` = binaire de
  mesure.
- Mesures dédiées : `tools/carte-fenetre-puits.sh` (fenêtre × puits d'attention),
  `tools/decouper-rapport.py` (un rapport par expérience), `tools/aiguille.py`,
  `tools/proxy_latence.py`, et pour le dessin H : `tools/lecture_etat.py` (relecture d'état
  partagée), `tools/verifier_chaine_etat.py` (la relecture reproduit-elle le moteur ?),
  `tools/profondeur_routee_oracle.py` (borne, cascade, témoin), `tools/carte-sortie-profondeur.sh`
  (où sortir), `tools/occupation_poids.py` (occupation d'un GGUF — manque M9), et
  `tools/m8_plage_activations.py` · `tools/m8_simulation_export.py` (M8).

## 6. ▶ Prochaine action

> **REPRISE APRÈS REDÉMARRAGE :** `/tmp` est vidé, et depuis le 12/10 **plus aucune porte n'en
> dépend** : `porte-topologie.sh` a ses prérequis **régénérés** (modèle dense à 24 couches,
> identifiants tokenisés dans `~/IA/scratch/prerequis/`, limite bornée à 255) — porte tenue
> (30,4363 puis 42,5477, écarts **0,00e0**) ; les trois portes à aiguille (`porte-greffe`,
> `porte-indice`, `porte-melange`) lisent un fichier **versionné dans le dépôt**
> (`tools/niah_4096_0.5.txt`, régénérable par `tools/construire-niah.py`) — il vivait dans
> `/tmp/campagne24` et sa disparition avait rendu trois portes « code 2 » le 12/10.
> Détail : `REPRISE.md` § 2.

**1. Passe complète des portes — QUATRE passes les 12 et 13/10, la dernière à 35 vertes sur 37**
(§ 5). Les deux rouges sont **instruits** : le critère d'indice extérieur de `porte-indice` et
`porte-melange` est **marginal par construction** (2 fenêtres sur 5 passent,
`reports/rapport-niah-fragilite.md`) — ils ne disent rien du moteur. Les **valeurs des portes n'ont
pas bougé** de toute la nuit. La porte du flux, rejouée après chaque
changement, rend **exactement** ses valeurs de référence (61,9920 / 60,8135) : c'est elle qui a
attrapé la paresse trop large du chargement (61,9920 → 58,8636), et c'est pour ça qu'elle se paie
après toute modification du chemin d'exécution.

**2. ~~Le moteur ne voit pas l'array~~ — FAIT le 12/10** (commit `be29ebc4`). `--materiel` rend
maintenant `DISQ /home/stephane/IA · 162 Go libres · nœud 1` : la liste n'est plus en dur
(`materiel.rs`), et le nœud d'un array se lit sur **ses disques** (`/sys/block/md0/md/dev-*/`) —
`md0` n'a pas de `device/numa_node`. Le § 7.2 de `docs/configuration-nvme-raid-amd.md` est satisfait.

**3. Les lecteurs parallèles — premier pas FAIT, et le suivant est chiffré.** `DRAVE_TAMPONS=1`
lit les experts **retenus** par `pread`, **par offset croissant**, dans des tampons à nous, et le
calcul lit ces octets (`reports/rapport-s4-prechargement-moteur.md` § 5) : **6,22 Go lus et 3,40 s**
de passe contre **10,90 Go et 3,70 s** pour les fils qui entrent les pages, et 9,52 Go / 5,97 s à la
demande — perplexité identique dans les quatre bras. Ce qui reste, et qui est mesuré :
**`pread` par huit fils rend 3 995 Mo/s** contre 1 126 à la demande (`tools/banc-experts.py`), mais
il demande des **tampons** — c'est-à-dire un **pool** et du **recouvrement**, pas des défauts de
page. Note de conception : `docs/note-lecteurs-paralleles.md`.
Le **pool de tampons** est fait aussi — et **neutre en temps** (mesuré : 2,4 s avant, 2,3-2,4 s
après, perplexité identique) : l'hypothèse des défauts de page est réfutée, `glibc` réutilise déjà
ces blocs. Il est gardé pour borner la mémoire (7,1 Mo au lieu de ~1 Go vivant) et pour rendre les
allocations visibles (`[tampons] 32 allocations, 9184 réutilisations`). Reste : le **recouvrement**, dont
l'ampleur est cernée — une passe de 8 jetons dure **2,3 s au total** (moteur déjà chargé), et
l'idée de Strata (prélecturer la couche suivante) avait déjà été mesurée **sans gain** (30,47 s
sans, 32,05 s avec). Le recouvrement ne peut porter que sur la part de **lecture**, que les tampons
ont déjà réduite de 75 % : c'est un pas à faible rendement, et il est dit comme tel.

**4. Le chargement construisait 2,7 Go de « listes » pour rien — FAIT** (commit `2bbecc86`) :
**26,95 s → 7,36 s** sur Qwen3-30B, **6,85 s → 0,60 s** sur le 0,5B, sans déplacer un chiffre ; la
forme push est construite **au premier usage réel** (l'inférence la prend, les passes `--ppl` non :
93 constructions contre 0), verrouillé par `tools/porte-push-paresseux.sh` — vue **rouge** avec
`DRAVE_PUSH_FAUX=1`. Ce qui reste : les **7,36 s** de déquantification + reconstruction Q8 ; le
chemin `--q4` les évite (**2,63 s**) mais **change la représentation** (emprunt des blocs Q4_K du
fichier, plus fidèle) — c'est une **décision**, pas une évidence.

**5. La VRAM : ce qui coûte est l'ALLOCATION, pas le lien** (mesuré le 12/10,
`reports/rapport-vram-transfert.md`). Un expert MXFP4 monté avec allocation coûte **11,72 ms**
(0,38 Go/s) ; dans **un tampon réutilisé**, **1,05 ms** (4,19 Go/s) — 91 % du coût était
l'allocation ; en Q4_K, 0,269 ms contre 0,171 ms. Le noyau GPU, lui, rend 0,1 ms là où le CPU met
1,3 ms (Q4_K) et 65,8 ms (MXFP4). **Prochaine action** : un **pool de tampons VRAM** avant toute
autre optimisation du déport ; le recouvrement ensuite (le noyau est plus court que la copie, donc
c'est le calcul CPU qu'il faut recouvrir). Première commande :
`DRAVE_GPU=1 ./drave-core/target/release/drave <modele> --gpu-banc --matrix blk.0.ffn_gate_exps.weight`.

**5bis. Deux portes rouges par CONSTRUCTION — le critère est à refaire, pas le moteur.**
`porte-indice` et `porte-melange` exigent qu'un indice extérieur tombe plus près de l'aiguille que
le hasard ; mesuré sur **cinq fenêtres** du même corpus, le critère passe **deux fois** (1,21× et
1,69×) et échoue **trois fois** (jusqu'à 2,13× pire). L'entrée de la campagne n'a jamais été
versionnée ; elle l'est maintenant (`tools/niah_4096_0.5.txt`, `tools/construire-niah.py --fenetre`).
**La correction a été faite le 13/10 (13 h 35) : un contrôle apparié** — même invite, même longueur,
une question qui ne désigne pas l'aiguille — et **il tue l'effet** : sur la fenêtre versionnée,
l'indice réel tombe à 482 jetons et le **témoin** à 459 ; sur la fenêtre qui passait le test du
hasard, l'indice réel tombe à 315 et le témoin à **1**. Ce que la porte mesurait n'est donc **pas**
porté par le sens de la question — les deux rouges restent, mais leur cause est maintenant
**structurelle et nommée** au lieu de dépendre d'un seuil contre le hasard. Fiche :
[`reports/rapport-niah-fragilite.md`](../reports/rapport-niah-fragilite.md) § 2bis.

**6. Dessin H — la carte des sorties a tourné (11/10 00 h 15) : ce n'est pas le point de sortie qui
limite.** Quatre sorties (12, 16, 20, 22 sur 24) : l'accord de l'oracle monte quand on sort tard,
mais le **gain atteignable s'effondre** — un routeur réel n'atteint la parité qu'à **22**
(47,78 % contre 47,73 %, **+0,05 point**, dans le bruit) pour **0,39 %** des paires, soit un facteur
**32** avec la borne (12,6 %). Le facteur limitant est le **chemin court**, c'est-à-dire le manque
**N4**, pas le choix de D. **Les sorties précoces ont été mesurées (13/10 02 h 27) : la réponse est non, et c'est chiffré.**
La sortie **8** porte le meilleur produit théorique — **16,96 %** des paires épargnées au mieux,
4,8× la sortie 22 — mais le **routeur réel y perd 0,30 point** (47,43 % contre 47,73 % pour le
chemin long) : aux sorties précoces, aucun seuil de confiance n'atteint la parité. La sortie 4
redescend (16,49 %). **Le facteur limitant est donc confirmé : la qualité du chemin court (N4)**,
pas la profondeur de sortie. Fiche :
[`rapport-design-H-sorties-precoces.md`](../reports/rapport-design-H-sorties-precoces.md).
Ce qui reste ouvert de ce dessin : la **génération libre** (décodage, pas perplexité — un autre
protocole), et le manque N4 lui-même.

**7. Fenêtre × puits d'attention — MESURÉ : le DRAIN porte la qualité** (fiche
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
La **non-monotonie observée à 512 jetons est close** : elle est du **corpus** (sur un second
corpus l'ordre s'inverse : 256 bat 128 de 5,4 %), et à 512 jetons **fenêtre 384 + 64 puits = +0,3 %**
seulement pour ÷1,33 de clés. **La loi de la frontière en N a été cherchée (13/10 03 h 58) : il n'y en a pas — il y a un
régime sûr, et il est robuste.** À N = 2 048, garder **la moitié** des clés coûte **+0,5 % à
+2,1 %** sur **sept** textes ; garder le **quart** va de **+2,8 %** à
**+49,2 %** — un **facteur 17,6 selon le texte**, qui domine toute tendance en N et explique la
non-monotonie déjà notée. À N = 4 096, sur cinq textes, la moitié des clés coûte **+0,4 % à +3,0 %** (donc le
« ≤2 % » ne vaut qu'à 2 048) et le quart **+3,2 % à +9,3 %** — l'étendue dépend donc **aussi** de N.
Conséquence : budgéter la moitié des clés (~1 % en moyenne, **jusqu'à 3 %**), et ne jamais
promouvoir un réglage plus agressif sur un seul texte. **Et les deux façons de dépenser cette moitié se valent** :
fenêtre 1 024 pure (+0,5 à +2,1 %) ou fenêtre 512 + 512 puits (+0,3 à +2,1 %) — le partage
fenêtre/drain est un paramètre d'**implémentation**, pas de qualité. Fiche :
[`rapport-loi-frontiere-fenetre.md`](../reports/rapport-loi-frontiere-fenetre.md).

**8. C9 (latéralité) et C4 (retard) — mesurés, leurs suites sont nommées.** Latéralité : l'échange
est exact, le gain entre deux vues est **nul** (et la récupération d'un jumeau bruité = une moyenne,
contrôle à 0,000 %) — **la suite — `--echange experts` sur un modèle routé — est MESURÉE le 13/10, et elle est
NÉGATIVE** : échanger les **choix d'experts** entre deux instances qui voient des textes différents
détruit le calcul (×92,6 en échangeant tout), et à la couche où le modèle est le plus robuste (la
dernière) l'effet **change de signe selon le texte** (×0,81 · ×1,46 · ×1,26) ; un routage
**aléatoire** y fait aussi bien ou mieux, donc il n'y a **pas** de transfert. Le mécanisme
(capture `DRAVE_TRACE_EXPERTS` + imposition `DRAVE_ROUTAGE_FORCER`, invariant **exact** verrouillé
par `tools/porte-echange-experts.sh`) reste ; la piste latérale, non
([`rapport-c9-echange-experts.md`](../reports/rapport-c9-echange-experts.md)) ; le coût compressé est de
**÷4 d'octets pour +3,0 %** (8 bits par bloc), et quantifier bat élaguer **encore**. Retard : un pas
coûte **×633**, un état manquant **×1,06** ⇒ l'ordonnanceur **continue sans** et ne réutilise jamais
([`rapport-c4-retard.md`](../reports/rapport-c4-retard.md)).

**9. C8 — l'échelle est mesurée : la courbe monte encore, la capacité n'est pas la limite, donc le
manque est bien N4.** Sur un morceau **jamais vu** : **1 032,58** (4 morceaux) · 369,22 (8) ·
260,81 (15) · **179,59** (30) — ÷5,75 pour ×7,5 de données, ÷1,4 par doublement en fin de courbe ;
et à données égales un adaptateur **non linéaire** (896→512→896) rend **376,01**, **2,1× pire**.
**Et la profondeur de sortie est un levier bon marché dès que le lecteur est entraîné** : à
k = 30 morceaux, la tête entraînée rend **179,59** (profondeur 16), **205,58** (12), **267,98** (8) et
**534,91** (4) — soit ×1,14 · ×1,30 · ×2,00 par 4 couches —, là où la tête **empruntée**
s'effondre de 449 500 à **24,7 millions** sur les mêmes états. **L'état précoce est lisible**
(÷46 000 par rapport à la tête du modèle) : c'est le lecteur qui manquait. Les deux leviers
— **données** et **profondeur** — **se multiplient largement** : le rapport 8/16 couches vaut 1,69 ·
1,47 · 1,49 pour 4, 15 et 30 morceaux, mais il **dépend du texte** (×1,17 sur un second morceau de
test) : le facteur va de 1,2 à 1,7, la direction ne change pas. *Deux contrôles* : la
**graine** pèse 0,7 % (178,39 contre 179,59) — la courbe tient —, mais le **morceau de test** pèse
**×10** (17,35 sur m20 contre 179,59 sur m32) et la **forme** de la courbe ne se transporte pas :
de 15 à 30 morceaux, m32 gagne ÷1,45 et m20 ÷22,8. Seule la **direction** (plus de données aide)
est robuste — aucune loi chiffrée ne se tire d'un seul morceau de test.
> **Rectifié le 14/10** (voir le paragraphe ci-dessous et
> [`reports/rapport-n4-dessin-b.md`](../reports/rapport-n4-dessin-b.md) § 4) : **ces trois chiffres
> de m20 (17,35, et le ÷22,8 de la « falaise ») ont été mesurés avec m20 DANS la liste
> d'entraînement** — donc ni « jamais vu », ni comparable à m32. Le facteur ×10 n'est pas établi,
> la falaise est le passage du morceau dans l'entraînement, et le rapport 8/16 « de 1,2 à 1,7 »
> perd son second point d'appui. Ce qui reste : la graine pèse 0,7 %, m32 est propre, et la
> direction (plus de données aide) tient.
Conclusion : entraîner le **chemin court** (N4) est la seule voie qui reste — agrandir la tête est
mesuré contre-productif, et sortir plus tôt coûte peu. **Trois dessins proposés**, du moins cher au
plus cher (adaptateur d'entrée → adaptateurs par couche → routeur de profondeur), avec **cinq portes
écrites avant le code** : [`docs/note-chemin-court-n4.md`](note-chemin-court-n4.md). **Et la mesure
qui dit lequel** : l'état profond est prédictible à **R² 0,65** depuis l'état précoce par une carte
**linéaire**, mais les pas élémentaires le sont mieux (0,78 et 0,75) → la composition n'est pas
linéaire, **~35 % de la variance profonde est CRÉÉE par les couches intermédiaires**
(`tools/predictibilite_etats.py`) : c'est le dessin **B** (adaptateurs par couche) qui l'attaque,
pas le A.

**Et le dessin B est mesuré (14/10) : il paie, et d'autant plus qu'on sort tôt.** À profondeur 8,
sur les deux morceaux réellement jamais vus et **deux graines** : **203,32 / 210,44**
(`lora+adaptateur`) contre **268,13 / 249,79** (adaptateur seul sur couches gelées) sur m32, soit
**÷1,19 à ÷1,32** — et **rien** sur m20 (163,26 / 172,53 contre 165,65 / 160,56 : ÷1,01 et ×1,07,
dans le bruit de graine). À profondeur 4 : **283,67 contre 520,28** (÷1,83) sur m32 et **187,98
contre 307,88** (÷1,64) sur m20 — le gain **grandit quand on sort tôt**, ce que la prédictibilité
des états annonçait. Le LoRA **seul**, à tête gelée, ne suffit pas (×1,33 et ×1,45 sur m20), sauf à
profondeur 4 où l'état entraîné redevient lisible par la tête du modèle (÷1,84 / ÷1,13, une graine).
Fiche : [`rapport-n4-dessin-b.md`](../reports/rapport-n4-dessin-b.md). **Deux corrections de mesure
y sont établies** : le m20 publié à **17,35** était mesuré avec **m20 dans la liste
d'entraînement** (la fuite vaut **×8,0** à profondeur 8 et **×14,4** à profondeur 4 ; la commande
du 13/10 — `seq 0 29` pour `--train` **et** `--test m20` — est retrouvée), et **14,2342 est un
chiffre de CORPUS** (moyenne géométrique des 33 morceaux : 14,4283 mesuré ici), pas un chiffre de
morceau — sur m32 le modèle complet vaut **7,42**, donc les rapports « ×N du modèle complet » des
fiches C8 sont deux fois trop optimistes. **Et la PORTE D'EXÉCUTION est franchie (14/10,
14 h 10-15 h 00) : le chemin court est mesuré par le MOTEUR.** `tools/exporter_gguf_dense.py`
écrit un GGUF **dense Qwen2** (biais q/k/v, tête liée, métadonnées KV copiées verbatim — les
38 paires, tokenizer compris) et fusionne les LoRA (`W ← W + (α/r)·B·A`) ;
`drave --adaptateur-sortie F` applique le lecteur appris (`h × h` f32 brut) à l'état **brut** avant
la norme finale d'une plage, sur les **trois** chemins de forward. Mesuré par `drave`, à
profondeur 8, sur les deux morceaux jamais vus : `adaptateur` seul **272,45** (m32) / **168,85**
(m20), `lora+adaptateur` **185,67** / **136,33** ⇒ **÷1,47** et **÷1,24** — le moteur retrouve
torch à **2 %** (quantification Q8_0 : le modèle complet montre le même +3 %). Trois contrôles
dans la 40ᵉ porte (`tools/porte-adaptateur-sortie.sh`) : écriture fidèle (7,4242 et 4 481 378,8799
**au chiffre près** sur le fichier réécrit), invariant d'identité bit à bit, et **le drapeau
agit** (une demi-échelle, que la norme ne peut pas absorber, multiplie la perplexité par 2,9) — les
trois cas invalides rendant **code 2**. Fiche :
[`rapport-n4-porte-execution.md`](../reports/rapport-n4-porte-execution.md). **Ce qui reste** :
trancher la **variabilité** — à graine fixée, le dessin A est reproductible au chiffre près, mais
les bras qui rétropropagent à travers les couches donnent ÷1,32 · ÷1,46 · ÷1,43 sur m32 (trois
exécutions) : le signe est stable, la taille varie de ±10 % — et mesurer la **génération libre**
(décodage, pas perplexité) sur le chemin court. Fiche :
[`rapport-c8-echelle.md`](../reports/rapport-c8-echelle.md). *(Historique, gardé pour la
comparaison : la tête entraînée généralise — ÷540 même texte, ×5,7 du modèle sur un texte neuf avec
30 morceaux.)* Décodabilité mesurée à 4, 8, 12, 16,
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
`tools/c8_carte_profondeur.sh`, `tools/c8_sonde_lineaire.py`, `tools/n4_dessin_b.py` (dessin B,
14/10 : LoRA sur les couches basses + adaptateur de sortie, portes de concordance torch ↔ moteur),
`tools/exporter_gguf_dense.py` (porte d'exécution : GGUF dense Qwen2, LoRA fusionné) et
`tools/porte-adaptateur-sortie.sh` (40ᵉ porte : écriture fidèle, invariant d'identité, effet du
drapeau, refus).

**Ce qui a changé dans le moteur (12/10, nuit) — les mesures sont dans trois fiches.** La
**prélecture parallèle** des experts (calcul d'une passe : 7,70 s → 3,65 s), la **lecture
séquentielle dans nos tampons** (`DRAVE_TAMPONS=1` : 6,22 Go lus / 3,40 s contre 10,90 / 3,70 pour
les fils), le **chargement paresseux** (26,95 s → 7,36 s sur Qwen3-30B) et le **coût réel d'un
transfert VRAM** (allocation = 37 à 91 % du coût). Fiches :
[`prechargement`](../reports/rapport-s4-prechargement-moteur.md) ·
[`chargement`](../reports/rapport-chargement-paresseux.md) ·
[`VRAM`](../reports/rapport-vram-transfert.md).

**Ce qui a changé dans la machine (12/10) — pour mémoire, ce n'est pas une action.** L'**array
raid0** de 4 NVMe (938 Go, monté `~/IA`, **nœud 1**) porte les modèles lourds et les artefacts :
V4.1-Flash-Q2 (341 Go), 5 shards de K3 sur 32 (228 Go), les clusters réécrits (116 Go). Mesuré :
**92 µs** par entrée d'engram de 264 octets contre 27 713 µs sur le mécanique, **7,45 Go/s** en
lecture à 8 flux, **2,86 Go/s** en écriture ; le **QPI ne coûte rien** à cette bande (trois
placements : 7,41 / 7,42 / 7,47 Go/s) — mais il faut des lecteurs parallèles pour l'atteindre,
d'où le point 3. **Aucune redondance** : rien d'unique n'y vit sans copie, et les 116 Go
d'artefacts sont sauvegardés sur le mécanique, vérifiés **octet pour octet** (12/10). Ce qui n'a
**pas** gagné à être déplacé, mesuré : la compilation de `drave-core` (48,03 s cible HDD contre
48,79 s cible array — la cible reste sur le HDD) et le cache `uv` (il **lie** son cache aux
environnements : deux systèmes de fichiers le feraient copier). Politique, chiffres et outils
(`etat-raid.sh`, `banc-io.py`, `banc-numa-raid.py`) : `~/IA/README.md` · fiche
[`reports/rapport-raid0-nvme.md`](../reports/rapport-raid0-nvme.md).

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
8. un **zéro inexprimable** est un défaut : `if drapeau > 0` transforme « zéro » en « défaut » ;
9. **un contrôle tautologique ne contrôle rien** : sous reparamétrisation, `module.weight` **est
   déjà** `signes · clamp(θ).exp()` — le « écart 0 » affiché ne vérifiait rien. Le vrai contrôle se
   fait **après** le retrait de la reparamétrisation. M8 est resté ouvert deux jours pour cela ;
10. **`tie_word_embeddings` partage un TENSEUR, pas une formule** : `lm_head.weight` **est**
    `model.embed_tokens.weight`. Reparamétrer l'un **casse le partage en silence** — l'autre reste
    figé à sa valeur initiale, et l'écriture suivante écrase le mauvais tenseur (M8, corrigé le
    10/10 ; `named_parameters(remove_duplicate=False)` révèle les partages) ;
11. **une mesure à un seul moment ne dit pas *où* ça casse** : recalculer la **même** grandeur à
    chaque étape (avant/après restauration, matérialisation, relecture) est ce qui a trouvé M8 —
    et c'est ce que la porte `tools/porte-sauvegarde-modele.sh` verrouille désormais ;
12. **écrire dans un poids reparamétré n'écrit RIEN** : `mod.weight` est une valeur *calculée*, donc
    `mul_`/`copy_` remplissent un temporaire — en silence. Trois sites du harnais le faisaient
    (élagage, masque, ratio de signes) : tout passe par `ecrire_poids`, qui écrit dans le
    **paramètre** et **vérifie** l'effet. Corollaire : **un poids log-normal ne peut pas être nul**
    (`e^−12 = 6,1e-6`), donc l'élagage n'y fait zéro qu'à la quantification — le harnais **compte**
    ces poids (221 184 à 50 %) au lieu de laisser croire le contraire.
