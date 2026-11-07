# État du chantier R — le lecteur : le tagger n'est pas à 0,944 contre 0,85, R1.2-1024 est mesuré, R4.4 attend la vérité humaine

> **Ligne de roadmap** : **R** (le lecteur) · **Date** : 2026-11-06, 22 h 10 HNE · **Branche** :
> `s/v7` · **HEAD** : `97256b8f` (le HEAD a bougé pendant l'audit : `de7c9113` → `7a876f70` →
> `97256b8f` ; les mesures de POS ont été refaites au HEAD final, à l'identique) ·
> **Mission** : lecture seule, aucun code, aucun fichier existant modifié ; **deux fichiers neufs**.
>
> **Verdict** : ⚠️ **la chaîne R est saine là où elle est mesurée, et trois récits sont en retard.**
> **R0.1–R0.6 sont vertes ou closes avec leur négatif** ; **R4.1–R4.3 sont vertes** ; **R4.4 est
> mesurée et gardée par deux portes vertes**, mais sa porte « **10 pages réelles avec vérité
> humaine** » n'est pas atteinte — **l'OCR n'est plus le blocage, la vérité humaine l'est**.
> **R1.2-1024 est un run fait et documenté** (20 000 pas, **2,6256** à 1 000 octets, artifact
> présent), mais **la ligne n'est pas close** dans la roadmap et **le miroir de copie du modèle
> 20 k n'existe pas**. Le **tagger** a deux mesures, pas une : **7B local sur 180 phrases**
> (POS **0,8483**, cascade **0,9440**) et **API DeepSeek sur 432 phrases réelles** (POS
> **0,9389**). Le **0,85 d'aujourd'hui** est l'heuristique sur **612 phrases** ; le tagger n'a
> **jamais** été mesuré sur ces 612. L'écart honnête est donc **+7,34 pts** sur le gold 180
> (heuristique **0,7749** aujourd'hui) et **+6,35 pts** sur le réel 432 (heuristique **0,8754**
> aujourd'hui), **pas +9,4** (0,9440 − 0,8500) : ce serait comparer deux corpus. Enfin, **R2.1
> n'est pas bloquée par N5** : le tampon en entrée lit déjà **+0,879** ; R3.1 est bloquée par
> **N4** (24/24 vus, 0/4 tenus), R5.2 par le **chrF 39,6**.
>
> **Dispositif** : lecture de `docs/pilotage/roadmap.md`, `en-cours.md`, des fiches
> `docs/pilotage/backlog/R*.md`, des `reports/rapport-r*.md`, `rapport-n2-*.md`,
> `rapport-pensee-gold-*.md`, `rapport-pensee-quatre-modes-*.md`,
> `rapport-memoire-travail-n5.md`, `rapport-file-taches.md` ; **rejeux ciblés** :
> `porte-document`, `porte-lecteur`, `porte-lecture`, `porte-balayage`, `porte-bloc-tableaux`,
> `porte-bloc-code`, `porte-bloc-maths`, `porte-bloc-linguistique`, `porte-ocr`,
> `porte-ocr-scans`, `routeur.py`, `banc_complet.py --verifie`, `evaluer_gold.py`. Aucun
> entraînement, aucun commit, aucun existant modifié.
>
> **Ce que cette fiche n'est pas** : un nouveau résultat expérimental. Elle **rejoue** des
> commandes existantes, **lit** les mesures déjà publiées et **dater** ce qui est fait, ce qui
> est mesuré sans être clos, ce qui est bloqué et ce qui reste.

## 1. Ce que j'ai rejoué (et ce que ça donne)

| commande | résultat | ce que ça prouve |
|---|---|---|
| `bash tools/porte-document.sh` | **exit 0** · 30 documents, **51 pages**, **1 466 régions**, fidélité **1,000** | R0.1 tient : partition, provenance, rejeu, 3 contrôles négatifs |
| `bash tools/porte-lecteur.sh` | **exit 0** · à 30 % du budget, **1,000** sur les **5 types** | R0.2 tient : la lecture contrôlée préserve la lecture intégrale |
| `bash tools/porte-lecture.sh` | **exit 0** · **7/7** contrôles ; seuils 0,168 / 0,394 reproductibles | R0.6 tient : budget, provenance, refus, rejeu, calibration |
| `bash tools/porte-balayage.sh` | **exit 0** · **223 spans**, **6/6** contrôles | R0.4-balayage tient : offsets exacts, rejeu, négatifs |
| `bash tools/porte-bloc-tableaux.sh` | **exit 0** · **35 tableaux**, **970 cellules**, provenance **776/776**, opérations **8/8** | R4.1 tient ; les chiffres de la roadmap (996/802) sont antérieurs |
| `bash tools/porte-bloc-code.sh` | **exit 0** · **342/342** fichiers, **24/24** exécutions, **7/7** refus | R4.2 tient ; la roadmap dit 294 fichiers |
| `bash tools/porte-bloc-maths.sh` | **exit 0** · **32/32** formules, **10/10** dérivées, **6/6** équations, **8/8** refus | R4.3 tient |
| `bash tools/porte-bloc-linguistique.sh` | **exit 0** · 10 verdicts vrais, POS **0,85** | R0.7 heuristique tient ; le tagger n'y est pas |
| `bash tools/porte-ocr.sh` | **exit 0** · WER **4,48 %**, parité **90 %**, dégradé **26,67 %** | R4.4-pilote tient ; les 10 pages sont des **rendus**, pas des scans |
| `bash tools/porte-ocr-scans.sh` | **exit 0** · 5 familles, colonnes, tableaux | R4.4-scans tient sur le simulé + les 3 vrais livres |
| `python3 tools/routeur.py --json /tmp/routeur-etat-r.json` | **exit 0** · AUC **0,839** ; fixe **0,871 / 0,373** ; transfert **0,819 / 0,313** | R0.5 est **close (négatif)** : le signal prédit, la règle ne transfère pas |
| `python3 tools/banc_complet.py --verifie tools/tests/documents/bench-complet.json` | **exit 0** · **248 questions**, 30 documents, 5 types, 0 problème | le banc R0.3 est cohérent ; la fiche dit **249** |
| `python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/…` | **exit 0** · POS **0,8500** (fermé **0,9295**, ouvert **0,7746**) sur **3 179 jetons** ; syntagmes F1 **0,6482**, tête **0,7673** ; attachement **235/236** ; pragmatique **0,9967 / 0,9771 / 0,9886 / 0,9444** | R0.7 heuristique est à **0,85** sur le gold **612** — le chiffre « 0,765 / gold 360 » de la roadmap est périmé |

**Ce que je n'ai pas rejoué** : le modèle du banc R0.3 (GPU, Qwen2.5-0.5B), la tête de survol
R0.4 (états précoces Qwen), les entraînements R1.1/R1.2 (checkpoints `work/`), la porte BPE
R1.3 (GPU), les scans réels R4.4 (les portes les rejouent depuis le cache). Les commandes sont
nommées dans les tableaux ; les chiffres de ces lignes sont ceux des fiches, datés.

## 2. Inventaire — chaque ligne R, son état, sa commande, son chiffre

### R0 — le lecteur v0 (système, sans entraînement)

| ligne | état | chiffre publié | commande qui vérifie | rejeu 2026-11-06 |
|---|---|---|---|---|
| **R0.1** graphe de document | ✅ **fait** | **51 pages**, fidélité **1,000**, partition exacte, 3 contrôles | `bash tools/porte-document.sh` | **vert** : 30 docs, 51 pages, 1 466 régions |
| **R0.2** contrôleur de lecture | ✅ **fait** | **1,000** à **30 %** sur **5 types** | `bash tools/porte-lecteur.sh` | **vert** : 5/5 types à 1,000 à 30 % |
| **R0.3** banc complet | ✅ **fait** | **249** questions (banc : **248**) ; extractif **1,000** à 30 % ; modèle **0,231** contre début **0,042** ; durci 84 paraphrases : modèle **0,375**, lexical **0,269** | `python3 tools/banc_complet.py --verifie tools/tests/documents/bench-complet.json` (banc) ; mesures : fiches `r03-banc-complet`, `r03-banc-durci` | **vert** : 248 questions, 0 problème |
| **R0.4** têtes de lecture | ⚠️ **partiel** : survol ❌ **close négative**, balayage ✅, relecture ❌ | survol v4 **0,540** contre BM25 **0,720** ; balayage rappel@10 **0,984** / **0,702** ; relecture **0/249** ; cascade calibrée = oracle (**0,911 / 0,415** ; la roadmap cite **0,894**) | `bash tools/porte-balayage.sh` ; `python3 tools/tete_survol.py` (non rejoué) ; `lecture.py --cascade` (fiche `r06-cascade-confiance`) | **balayage vert** : 223 spans, 6/6 |
| **R0.5** routeur extractif/génératif | ❌ **close (négatif)** | AUC **0,839** ; transfert **0,819 / 0,313** contre fixe **0,871 / 0,373** | `python3 tools/routeur.py --json /tmp/routeur.json` | **rejoué** : AUC 0,839, 331 questions |
| **R0.6** pipeline de lecture | ✅ **fait** | **12/20** au pilote, **9/10** refusés (le titre dit 10/10), **7/8** au modèle ; **7/7** contrôles | `bash tools/porte-lecture.sh` | **vert** : 7/7, calibration 0,168 / 0,394 |
| **R0.7** couche linguistique | ✅ **fait (heuristique)** ; 🔬 **tagger mesuré, non branché** | **398 langues** à **0,9687**, script **1,0000** ; gold **612** : POS **0,8500**, syntagmes F1 **0,6482**, tête **0,7673**, attachement **235/236**, pragmatique **0,9967 / 0,9771 / 0,9886 / 0,9444** ; tagger : voir § 5 | `bash tools/porte-bloc-linguistique.sh` ; `python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/gold.json` ; tagger : `qualifier_neuronal.py` / `qualifier_quatre_modes.py` | **vert** : POS 0,85 ; **roadmap périmée** (gold 360 / POS 0,765) |

### R1 — la fenêtre native

| ligne | état | chiffre publié | commande qui vérifie | rejeu 2026-11-06 |
|---|---|---|---|---|
| **R1.1** contexte hiérarchique / positions | 🔬 **partiel** : porte PPL tenue, porte aiguille non tenue | PPL à 1 000 octets **3,2545** (fenêtre 256) contre **8,2024** (absolu), soit **0,97×** la PPL à 129 (porte 1,5×) ; **aiguille native ≥ 15/18 à 4 000 : non atteinte** ; miroir de copie **0,0078** au mieux | `work/n2ac/eval_fenetre.py`, `work/n2ac/mirroir_copie.py` (fichier réel : `mirroir_copie.py`), `work/n2ac/eval_production.py` | **non rejoué** (checkpoints `work/`, GPU) ; chiffres des fiches `n2-r11`, `n2-r12-2048` |
| **R1.2** curriculum de contexte | 🔬 **run 1 024-20 k fait et documenté ; ligne non close** | **1 024 / 20 000 pas** : **2,9955** à 128, **2,6256** à 1 000, **2,5429** à 4 000 sur `val_fr` ; **2 048** à octets constants ne bat pas 1 024 (**3,0466 / 2,6501 / 2,5513**), à pas constants gagne **−0,08 à −0,10** | `python3 work/n2ac/eval_production.py work/n2ac/rope1024-20k.pt` (banc de la fiche) ; artifact `work/n2ac/rope1024-20k.pt` | **non rejoué** ; artifact, JSON et fiche présents ; voir § 3 |
| **R1.3** tokenisation | ✅ **décidée : octets** | à octets égaux : BPE 512 **+0,39 %** (bruit), BPE 1024 **+3,92 / +4,09 %**, anglais **+4,22 / +6,59 %** | `bash tools/porte-r13-bpe.sh` (GPU) ; fiches `r13-decision`, `r13.2-vocab1024` | **non rejoué** (GPU) ; décision inchangée |

### R2 et R3 — la mémoire et la restitution

| ligne | état | chiffre / porte | commande | ce qui bloque |
|---|---|---|---|---|
| **R2.1** mémoire de travail / gist | ⏳ **à faire, non bloquée par N5** | porte : indice en section 2 après lecture de la section 5, **avec citation** ; closed-book échoue ; le tampon gelé lit **+0,879**, le LoRA **+0,964**, le réseau seul **−1,091 → −2,773** | **aucune** ; à créer (banc gist + tampon `tools/memoire_travail.py --entree-memoire 8`) | rien d'externe ; il faut le tampon en entrée, pas un entraînement de mémoire |
| **R2.2** mémoire épisodique / relecture | ⏳ **après R2.1** | porte : la relecture récupère ce que le gist a perdu ; sans store, échec ; store borné sur 50 documents | **aucune** | R2.1 |
| **R3.1** SFT de lecture | 🧱 **bloquée par N4 et R2.1** | porte : **≥ 80 %** des instructions **tenues à l'écart** ; le contrôle **24/24 vus** ne compte pas ; N4 est **0/4 tenu** | **aucune** ; jeu tenu à l'écart à construire | N4 (consigne courte) + R2.1 |
| **R3.2** citations et provenance | ⏳ **après R3.1** | porte : chaque citation pointe un span exact ; le contrôle sans citation est plus bas | **aucune** | R3.1 |

### R4 — les blocs structurels

| ligne | état | chiffre publié | commande qui vérifie | rejeu 2026-11-06 |
|---|---|---|---|---|
| **R4.1** tableaux | ✅ **fait** | roadmap : **996 cellules**, **802** exactes, texte plat **0/3** ; porte actuelle : **970 cellules**, provenance **776/776**, **8/8** opérations | `bash tools/porte-bloc-tableaux.sh` | **vert** : 35 tableaux, 970 cellules, 8/8, contrôles 3/3 |
| **R4.2** code | ✅ **fait** | roadmap : **294 fichiers**, **24/24** extraits, texte seul **0/3** ; porte actuelle : **342/342** fichiers, **24/24** exécutions, **7/7** refus | `bash tools/porte-bloc-code.sh` | **vert** : 342/342, 24/24, 7/7 |
| **R4.3** maths | ✅ **fait** | **32 formules**, **10/10** dérivées, **6/6** équations, surface **0/3** | `bash tools/porte-bloc-maths.sh` | **vert** : 32/32, 10/10, 6/6, 8/8 refus |
| **R4.4** vision / OCR | 🔬 **partiel** : mesuré et gardé, porte humaine non atteinte | 5 familles : photo **55,9 → 6,7 %** de WER (test **5,7 %**) ; préservation **96,7 / 93,3 / 90,0 / 90,0 / 56,7 %** ; colonnes **89,4 → 0,5 %** ; tableaux **92,6 %** ; **3 vrais livres × 10 pages** : WER **7,10 / 36,26 / 8,73 %** contre la couche OCR ; ordre des colonnes **15,32 / 7,09 / 12,80 %** contre **97,98 / 96,06 / 99,20 %** en ordre inverse | `bash tools/porte-ocr.sh` ; `bash tools/porte-ocr-scans.sh` | **les deux vertes** ; la porte « **10 pages réelles avec vérité humaine** » reste ouverte ; voir § 4 |

### R5 — la lecture croisée et le multilingue

| ligne | état | porte | commande | ce qui bloque |
|---|---|---|---|---|
| **R5.1** multi-documents | ⏳ **après R3** | réponse comparative avec **deux sources citées** ; le contrôle à une seule source échoue | **aucune** | R3.1/R3.2 ; le manque **M4** (encodeur exécutable) |
| **R5.2** lecture en traduction | 🧱 **bloquée par B10.3** | chrF **> 39,6** ; la réponse ne dépend pas de la langue source | **aucune** | le décodeur est à **12,7 / 5,3** contre le plancher **39,6** |

**Lecture d'ensemble** : sur **20 lignes R**, **9 sont faites et vérifiées** (R0.1, R0.2, R0.3,
R0.6, R0.7 heuristique, R1.3, R4.1, R4.2, R4.3), **2 sont closes négatives** (R0.4-survol, R0.5),
**3 sont mesurées sans être closes** (R1.1, R1.2-1024, R4.4), **5 sont à faire** (R2.1, R2.2,
R3.1, R3.2, R5.1) et **1 est bloquée** (R5.2). La frontière réelle n'est donc pas « R1.2 à
faire » : c'est **R0.7 (tagger) et R2.1 (gist)**.

## 3. R1.2-1024 — ce qui est fait, ce qui reste

### 3.1 Ce qui est fait

Le run **`rope1024-20k`** est un **vrai fait mesuré**, pas une intention :

- **entraînement** : 34,3 M, RoPE, **séquence = fenêtre = 1 024**, **17 500 pas ajoutés** aux
  2 500 du run court (donc **20 000 pas**), **164 Mo vus**, init `work/n2ac/rope1024-2.5k.pt`,
  perte finale **1,0206**, PPL interne **2,6609**, **8 000 s** de calcul ;
- **artifact** : `work/n2ac/rope1024-20k.pt` (**131 Mo**), `.drvm` (SHA
  `76628995a51cd54d52d564112f557bacfbea5f6119947c7b20f710e060f4e9af`), `.pt.json`, `.log` ;
- **évaluation** (`reports/n2-r12-2048.json`) : `val_fr` **2,9955** à 128, **2,6256** à 1 000,
  **2,5429** à 4 000 ; `val_big` **3,3086 / 2,9055 / 2,8828** ; littérature **5,6071** ; anglais
  **7,8817** ; wikitext2 **8,7751** ; corpus propre **7,7208** ; contrôle permuté **195,3449** ;
- **fiche** : [`rapport-n2-r12-2048`](rapport-n2-r12-2048.md) § 5, et la loi de la fenêtre dans
  [`rapport-n2-fenetre`](rapport-n2-fenetre.md) ; **commit** `c7ef9bc4` ;
- **marqueur d'audit** : `rapport-file-taches.md` P8 dit **« Fait (20 000 pas) »**.

### 3.2 Ce qui reste

1. **La ligne n'est pas close dans les documents.** La roadmap dit **⏳ R1.2**, l'`en-cours` dit
   « **R1 — R1.2-1024** » et « **1 024 octets entraînés** » comme prochaine action, alors que le
   run existe. C'est un **retard de statut**, pas un manque de mesure. La correction appartient
   au hub (je ne modifie pas `docs/pilotage/`).
2. **Le miroir de copie du modèle 20 k n'existe pas.** Les miroirs présents sont
   `miroir-rope1024-2.5k.json`, `miroir-mix1024-60k.json`, `miroir-rope512.json`, etc. ; aucun
   `rope1024-20k` ni `rope2048-20k`. Or c'est le contrôle qui décide si la fenêtre **sert à
   lire** ou seulement à baisser la PPL. Le chiffre publié (**0,0078** au mieux) vient du 2,5 k
   et de la production, pas du 20 k.
3. **La stabilité n'est pas multi-graines.** La porte dit « 1 000 octets stable, pas un point
   isolé » : la **courbe** 128 → 4 000 est stable et monotone, et le contrôle « même texte »
   sature à 1 024 ; mais il n'y a **qu'un lancement par point** (la fiche le dit). « Stable »
   au sens d'un grain unique n'est pas mesuré.
4. **Le 2 048 est fini mais ne change pas le point d'équilibre.** À **octets constants**
   (164 Mo), 2 048 est **derrière** 1 024 partout (3,0466 contre 2,9955 à 128 ; 2,6501 contre
   2,6256 à 1 000 ; 2,5513 contre 2,5429 à 4 000) ; à **pas constants** (20 000), il gagne
   **−0,083 / −0,088 / −0,105** à 128 / 1 000 / 4 000, avec **328 Mo** vus. Le run
   `rope2048-20k.pt` existe (131 Mo) ; le 2 048 n'est donc pas « à faire », il est **mesuré et
   négatif à budget d'octets égal**.
5. **Le 1 024-20 k n'est pas le modèle de production.** Il n'a vu que `wiki_fr` ; son
   `val_big` à 1 000 est **2,9055**, pas sous 2,5. Les chiffres **2,4759 / 2,4373** de
   l'`en-cours` sont ceux d'un **autre** modèle (production, 1 024, 30 k pas), pas de
   `rope1024-20k`. Ne pas les attribuer à R1.2-1024.

**Ce que R1.2-1024 prouve** : à **octets constants**, la fenêtre entraînée paie jusqu'à
**1 024** ; le gain est **−0,63** à 1 000 octets contre la fenêtre 256 à même budget (2,6256
contre 3,2545), et **−0,69** à 4 000. C'est le levier de la fenêtre, pas un point isolé.
**Ce qu'il ne prouve pas** : que le modèle **restitue** (le miroir est muet), ni que le gain
tienne sur un autre corpus (le `val_big` le rappelle).

## 4. R4.4 — les scans : l'OCR n'est plus le blocage, la vérité humaine l'est

### 4.1 Les deux portes sont vertes

- **`porte-ocr.sh`** (pilote, 10 pages **rendues** à 300 dpi, 6 PDF, 3 langues) : **exit 0** ;
  WER **4,48 %**, rappel **97,37 %**, parité de passage **27/30 (90 %)**, valeur stricte
  **25/30 (83,33 %)**, sans OCR **0/30** ; page dégradée : WER **17,08 %**, parité **26,67 %**.
- **`porte-ocr-scans.sh`** (5 familles, colonnes, tableaux) : **exit 0** ; les 5 familles
  tiennent leurs planchers, les colonnes et les tableaux aussi ; page noire **0 mot**,
  mono-colonne **écart 0,00**, sans redressement **0 %** de cellules, texte à plat **0 cellule
  localisée**.

### 4.2 Les chiffres publiés (et ce qu'ils ne sont pas)

| famille | WER dev | WER test | préservation dev (auto + exp) |
|---|---:|---:|---:|
| propre (contrôle) | 4,14 % | **3,01 %** | **96,7 %** |
| photocopie | 6,34 % | **4,69 %** | **93,3 %** |
| photo | **6,68 %** (brut **55,85 %**) | **5,68 %** | **90,0 %** |
| papier | 6,87 % (test brut 53,15 %) | **6,38 %** | **90,0 %** |
| fax | 21,90 % | **15,52 %** | **56,7 %** |

- **colonnes** : deux colonnes **89,44 → 0,54 %** (propre), **90,11 → 1,03 %** (photocopie),
  **88,32 → 6,52 %** (photo) ; mono-colonne **0,00** d'écart ; le contrôle sans gouttière
  échoue bien (50 %+).
- **tableaux** : **92,6 %** de cellules exactes (propre, 500/540), **69,1 %** (photocopie,
  373/540), **62,4 %** (photo, 337/540) ; sans redressement **0 %** ; texte à plat **0/54**
  cellules localisées (53,7 % des valeurs présentes).
- **trois vrais livres** (Internet Archive) : *Voyage au centre de la terre* **7,10 %**,
  *Vingt mille lieues sous les mers* **36,26 %** (mais rappel **88,38 %** : c'est l'**ordre**
  qui diverge, pas les mots), *Germinal* **8,73 %** ; l'**ordre des colonnes** est prouvé sur le
  lexique du second : **15,32 / 7,09 / 12,80 %** contre **97,98 / 96,06 / 99,20 %** en ordre
  inverse.

### 4.3 La porte « 10 pages réelles avec vérité humaine » n'est pas atteinte

- Les **30 pages réelles** (3 livres × 10) sont comparées à la **couche OCR du PDF**, pas à une
  **vérité humaine**. Le JSON le dit : `reference = "couche OCR du PDF (Internet Archive) — pas
  une vérité humaine"`. Ce sont des **accords entre moteurs**, pas des exactitudes.
- La porte de la fiche est **« 10 pages scannées réelles, de bout en bout, avec une vérité
  humaine »**. Le **compte** de pages est largement dépassé (30), la **nature** de la référence
  ne l'est pas.
- Le **fax 1 bit** (**21,90 %** de WER dev, **56,7 %** de préservation) et l'**exposant
  fusionné** (« développement 10 ») sont des **limites nommées** ; les tableaux **sans traits**,
  les **3 colonnes** (52,5 % de WER) et le **flou fort** (σ = 4 : 49,63 → 53,24 %) aussi.
- **L'OCR n'est plus le blocage** : tesseract **5.5.3** est installé (`work/ocr/root`), les deux
  portes sont vertes, le corpus OCR CEGEP est restauré à **62 documents** (train 4 440 987 o,
  val 12 536, test 10 524 ; SHA `f57154df…`, `dd605833…`, `1c9ab734…` vérifiés aujourd'hui).
  Le blocage est **la vérité humaine sur 10 pages**, pas l'outil.

### 4.4 Le statut est contradictoire dans les documents

| document | ce qu'il dit |
|---|---|
| `roadmap.md` (R4.4) | 🔬 **« mesuré sur scans simulés ; ouvert sur les scans réels »** |
| `roadmap.md` (bloqués) | **« R4.4 les scans »** bloquée par l'absence de vérité humaine |
| `en-cours.md` (chantiers) | **« R4.4 close »** |
| `backlog/R44` | **« partiel »**, la porte reste ouverte |
| `rapport-r44-scans.md` (verdict) | **« la ligne reste ouverte pour les scans réels de bout en bout »** |
| `rapport-r44-scans.md` (dernière section) | **« R4.4 est close avec ses limites nommées »** |

**Le statut juste** : **R4.4 est partielle — mesure faite et gardée, porte humaine non atteinte.**
« Close » au sens des limites nommées (fax, exposant, tableaux sans traits) est défendable ;
« close » au sens de la porte (10 pages réelles avec vérité humaine) ne l'est pas. Les deux
phrases de la même fiche ne peuvent pas être vraies ensemble.

## 5. Le tagger — où il est, ce qu'il mesure, sur quel corpus, quel écart

### 5.1 Où il est

Le tagger n'est pas un fichier unique ; c'est **une classe, deux routes et quatre bancs** :

| pièce | rôle |
|---|---|
| `tools/bloc_linguistique.py` → **`NeuronalLLMPOS`** (l. 1727) | le tagger POS : tokenise avec `Heuristique._mots`, envoie la liste des tokens, impose une classe par token par **grammaire GBNF** ; les spans sont ceux du bloc, pas ceux du modèle |
| `tools/tests/linguistique/qualifier_neuronal.py` | le banc **local** : lance `llama-server`, 180 phrases, heuristique / neuronal / cascade, contrôles, JSON |
| `tools/tests/linguistique/qualifier_cascade.py` | le banc **local** de la cascade complète (POS + syntagmes), 180 phrases |
| `tools/tests/linguistique/qualifier_quatre_modes.py` | le banc **API DeepSeek** (`deepseek-chat`), **gold réel 432**, six modes (heuristique, neuronal, parallèle, cascade, parallèle_niveau, cascade_niveau) |
| `reports/pensee-gold-neuronal.json` · `pensee-gold-cascade.json` · `pensee-quatre-modes-432-run2.json` | les mesures |
| `reports/rapport-pensee-gold-neuronal.md` · `-syntagmes` · `-cascade` · `rapport-pensee-quatre-modes*.md` | les fiches |

**Ce qu'il mesure** : le POS **au token**, en **exactitude exacte**, sur les **12 classes du
bloc** — `DET, NOUN, VERB, ADJ, ADV, PREP, PRON, AUX, CONJ, NUM, INTJ, PUNCT`. Ce n'est **pas**
le jeu Universal Dependencies (17 étiquettes), et il ne rend **ni morphologie, ni traits, ni
syntagmes** ; le syntagme est un autre tagger (`NeuronalLLMChunks`), la pragmatique un troisième.
La tokenisation est celle de `Heuristique._mots` (mots et nombres, sans ponctuation) ; le gold et
le bloc coïncident sur **180/180** phrases (vérifié dans la fiche).

### 5.2 Sur quel corpus — et pourquoi c'est le nœud

| route | corpus | phrases / jetons | ce qui est mesuré |
|---|---|---:|---|
| **7B local** (Qwen2.5-7B-Instruct Q4_K_M, `llama-server` b11017, **CPU** `-ngl 0`) | `gold.json` **20 réelles** (14 fr / 6 en) + `gold_synthetique.json` **160 synthétiques** (fr) | **180 / 804** | POS **0,8483** seul, cascade 0,6 **0,9440** ; 20 réelles **0,9238**, 160 synthétiques **0,9471** ; 0 refus, 180 appels, 3,043 s de moyenne, 548 s |
| **API DeepSeek** (`deepseek-chat`, température 0, règle 11) | `gold_reel.json` **432 réelles** (228 fr / 204 en) | **432 / 2 375** | POS **0,9389** (run 2 ; run 1 **0,9309** ; t03 **0,9385**), syntagmes **0,8241**, tête **0,8797**, acte **0,0** (l'heuristique garde **0,9954**) ; 858 appels, 254 454 tokens, 807,6 s |
| **gold courant** (le 0,85) | 20 + 432 + 160 | **612 / 3 179** | **l'heuristique seulement** : POS **0,8500** (fermé 0,9295, ouvert 0,7746) ; le tagger n'y a **jamais** été mesuré |

### 5.3 L'écart avec l'heuristique — le vrai calcul

Le chiffre **0,85** est l'heuristique sur le **gold 612** (3 179 jetons), refait au HEAD
`97256b8f`. Le **0,9440** est la cascade du **7B local sur le gold 180** (804 jetons). Ce ne sont
**pas** deux nombres du même corpus ; les soustraire (0,9440 − 0,8500 = +0,0940) est une
**erreur de corpus**. Voici les comparaisons honnêtes :

| corpus | heuristique **aujourd'hui** | tagger | écart | statut |
|---|---:|---:|---:|---|
| **180** (20 + 160) | **0,7749** | **0,8483** (7B seul) | **+0,0734** | mesure du 2026-11-02, heuristique rejouée aujourd'hui |
| **180**, cascade | **0,7749** | **0,9440** (cascade 0,6) | **+0,1691** | la cascade publiée est de 2026-11-02 ; l'écart est arithmétique, pas un re-run |
| **432 réel** | **0,8754** | **0,9389** (API) | **+0,0635** | mesure API du 2026-11-04, heuristique rejouée aujourd'hui |
| **612** (gold courant) | **0,8500** | **non mesuré** | **—** | c'est le trou à combler |

**Les chiffres publiés étaient justes contre leur baseline d'alors, mais leur baseline a
vieilli** :

| publication | baseline d'alors | tagger | écart publié | baseline aujourd'hui | écart aujourd'hui |
|---|---:|---:|---:|---:|---:|
| 7B local, 180 ([fiche](rapport-pensee-gold-neuronal.md)) | 0,7512 | 0,8483 | +0,0971 | 0,7749 | **+0,0734** |
| 7B local, cascade 180 ([fiche](rapport-pensee-gold-cascade.md)) | 0,7512 | 0,9440 | **+0,1928** | 0,7749 | **+0,1691** |
| API 432, run 2 ([fiche](rapport-pensee-quatre-modes-run2.md)) | 0,7444 | 0,9389 | **+0,1945** | 0,8754 | **+0,0635** |

**Pourquoi la baseline a monté** : l'heuristique du bloc L a gagné **+13,1 pts** sur le réel 432
(0,7444 → 0,8754) et **+2,4 pts** sur le 180 (0,7512 → 0,7749) entre le 04/11 et le 06/11
(paquet POS sûr, classes fermées, `NUM`). Le tagger, lui, n'a pas été rejoué. **L'avantage du
tagger a donc fondu** : il reste **+6 à +7 pts** sur le réel, pas **+19**.

**Ce que cela ne dit pas** : le tagger n'est **pas** inutile — 0,9389 contre 0,8754 reste un
gain, et la cascade peut encore valoir plus que le seul POS. Mais **le +19 pts est un artefact
de corpus et de date**, et **le +9,4 pts contre 0,85 n'existe pas**.

### 5.4 Ce qui reste, et la règle 11

- **Le modèle 7B local n'est plus sur le disque** : `models/` ne contient que les Qwen2.5-0.5B
  (`Q4_0`, `Q8_0`) ; les deux shards GGUF du 7B (4,68 Go) sont **absents**. La commande
  `python3 tools/tests/linguistique/qualifier_neuronal.py --limite 1` échoue aujourd'hui avec
  `modèle absent : …/models/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf`. Le cache Hugging
  Face contient le 7B en **safetensors** (15 Go), pas en GGUF : rejouer le 7B demanderait un
  **re-téléchargement** (SHA-256 dans le JSON) ou une **re-quantisation** (qui change le modèle).
- **La règle 11** : « les professeurs passent par l'API DeepSeek, jamais par un serveur local
  (`llama-server`, `ollama`) ». Le 7B local a été mesuré **sur CPU** (`-ngl 0`), sans toucher aux
  GPU de N2, mais il reste un **serveur local** ; la route **autorisée** est l'**API DeepSeek**,
  déjà branchée dans `qualifier_quatre_modes.py` (clé présente, 36 o). La mesure locale est donc
  **historique et non reproductible en l'état** ; la mesure API est **la route courante**.
- **Le trou** : le tagger API n'a pas été mesuré sur le **gold 612** (il s'arrête à 432 réelles).
  C'est la prochaine mesure (action 1 ci-dessous), et elle seule donnera l'écart contre **0,85**.

## 6. La chaîne R2 / R3 / R5 — ce qui attend quoi

| ligne | dépend de | état réel | ce qu'il faut pour la débloquer |
|---|---|---|---|
| **R2.1** gist | R0.1, R1 (mesurée) | **libre** ; le tampon gelé lit **+0,879** | construire le **tampon en entrée** et le gist (résumé, entités, faits, offsets) ; mesurer la question multi-sections avec citation |
| **R2.2** relecture | R2.1 | après R2.1 | store de régions, éviction, déclencheur |
| **R3.1** SFT | R2.1, **N4** | **bloquée par N4** : 24/24 vus, **0/4 tenus** | N4 (consigne courte) **et** R2.1 ; jeu tenu à l'écart par document |
| **R3.2** citations | R3.1 | après R3.1 | réponse + citation + support |
| **R5.1** multi-documents | R3.1/R3.2, M4 | après R3 | retrieval, comparaison, provenance, contradictions |
| **R5.2** traduction | B10.3 | **bloquée par le chrF** (12,7 / 5,3 contre **39,6**) | un décodeur au-dessus du plancher |

**La correction de l'`en-cours`** : « **R2/R3 attendent N5/N4** » est trop grossier.
**R2.1 n'attend ni N5 ni N4** : N5 est la ligne d'échelle (50–100 M), gelée, et le tampon est une
**structure**, pas un entraînement de mémoire — la fiche N5 dit elle-même que le réseau
n'apprend pas (**−1,091 → −2,773**) et que la structure donne **+0,879**. **R3.1** attend **N4**
et R2.1 ; **R5.1** attend R3 ; **R5.2** attend B10.3. La frontière réelle est donc **R2.1**, pas
« N5 ».

## 7. Les trois prochaines actions de R, mesurables

### Action 1 — Re-mesurer le tagger POS sur le gold 612 (R0.7), et publier l'écart contre 0,8500

- **Pourquoi** : c'est le seul trou du tagger ; le 0,9440 est sur 180, le 0,9389 sur 432, le
  0,8500 sur 612. Sans ce chiffre, la ligne R0.7 reste « mesurée deux fois, jamais sur le gold
  courant ».
- **Commande** : `DEEPSEEK_KEY_FILE=~/.config/drave/deepseek.key python3
  tools/tests/linguistique/qualifier_quatre_modes.py --sortie /tmp/tagger-612.json` **après**
  extension du chargeur au gold 612 (le banc charge aujourd'hui `gold_reel.json` seul ; il faut
  ajouter `gold.json` + `gold_synthetique.json`, ou lancer 432 + 180 et agréger). Le run 432
  coûte **858 appels, 254 454 tokens, 807,6 s** ; le 612 en coûtera ~**1 200 appels, ~360 k
  tokens, ~20 min**.
- **Mesure** : POS exact sur 612, ventilé **432 réel / 160 synthétique / 20 hand** ; écart contre
  **0,8500** ; contrôles **majoritaire 0,2289**, **permutation 0,1729** ; refus ; coût.
- **Seuil de décision** : si l'écart est **< +2 pts**, le tagger POS n'est **pas additif** au
  gold courant → le **fermer** comme négatif nommé et garder l'heuristique ; si **≥ +5 pts**,
  l'intégrer à la cascade **via l'API** (jamais le 7B local, règle 11).

### Action 2 — Rejouer le miroir de copie sur `rope1024-20k` (et `rope2048-20k`), puis trancher R1.1

- **Pourquoi** : R1.2-1024 est mesuré, mais **le contrôle de lecture du modèle 20 k manque** ;
  tous les miroirs existants sont au hasard (**0,0078** au mieux), y compris à 16 octets. C'est
  le contrôle qui dit si la fenêtre **sert à lire** ou seulement à baisser la PPL, et donc si
  R1.1 peut être close.
- **Commande** : `PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/mirroir_copie.py
  work/n2ac/rope1024-20k.pt --rope --sortie /tmp/mirroir-1024-20k.json` (le fichier réel est
  `mirroir_copie.py`, avec deux r ; la fiche cite `miroir_copie.py`). Refaire avec
  `rope2048-20k.pt`.
- **Mesure** : justesse top-1 à **16, 64, 128, 200, 240, 255, 300, 400** octets ; 8 sondes.
- **Seuil de décision** : si **≤ 0,01 partout** (attendu), enregistrer le **négatif** et clore
  R1.1 « aiguille non atteinte, copie non créée par la fenêtre » ; si **> 0,5 à d ≤ 240**, la
  fenêtre crée un circuit de copie → **rouvrir R1.1** et refaire l'aiguille à 4 000.
- **Coût** : quelques minutes, GPU libre (l'`en-cours` le dit), 8 sondes.

### Action 3 — Construire R2.1 : le gist v0 avec tampon en entrée, et mesurer sa porte

- **Pourquoi** : R1 est mesuré (R1.2-1024) ; **R2.1 est la frontière suivante**, et elle n'est
  **pas** bloquée par N5. Le tampon gelé lit déjà **+0,879** ; le réseau seul est à **−1,091**
  et l'entraînement l'aggrave (**−2,773**). C'est la **structure** qu'il faut mettre en entrée.
- **Construction** : sections et offsets de **R0.1** ; tampon `--entree-memoire 8` de
  `tools/memoire_travail.py` ; gist = résumé par section + table d'entités/faits/dates +
  citations ; état borné. Banc à créer (`tools/banc_gist.py` ou équivalent).
- **Mesure** : sur des documents multi-sections, question dont l'**indice est en section 2 après
  lecture de la section 5** ; exactitude **gist contre closed-book** ; **citation exacte** ;
  taux d'oubli ; documents courts (pas de perte).
- **Contrôles négatifs** : closed-book, gist aléatoire, gist complet (oracle), question dont la
  réponse est dans une seule section.
- **Seuil de décision** : le gist doit **battre le closed-book** d'une marge pré-enregistrée
  (proposition : **+10 pts**), avec citation exacte **≥ 0,90** et **aucune** perte sur les
  documents courts ; sinon, le gist n'est pas une mémoire, c'est un fichier.

**R4.4 n'est pas dans les trois** : sa porte est **bloquée par la vérité humaine**, pas par
l'OCR. La chaîne est prête (deux portes vertes, 30 pages réelles) ; ce qui manque est un
**corpus de 10 pages avec transcript humain**. C'est une dépendance **humaine**, pas un run.

## 8. Écarts documentaires à corriger (hors de mon territoire)

Je n'ai modifié aucun document de pilotage ; voici ce que le hub doit corriger :

| # | où | ce qui est écrit | ce qui est mesuré |
|---|---|---|---|
| 1 | `roadmap.md` R0.7 | gold **360**, POS **0,765** | gold **612**, POS **0,8500** |
| 2 | `roadmap.md` R0.7 | tagger **0,9440** comme s'il valait contre 0,85 | 0,9440 est sur **180**, contre **0,7749** aujourd'hui ; sur 432, **0,9389** contre **0,8754** |
| 3 | `en-cours.md` R | « **R0.7 — tagger** » dans ce qui reste | le tagger est mesuré (7B local + API) ; il reste **à re-mesurer sur 612** et à **décider** |
| 4 | `en-cours.md` R | « **R1 — R1.2-1024** », « 1 024 octets entraînés » | le run **existe** (20 000 pas, 2,6256 à 1 000) ; c'est le **statut** qui est en retard |
| 5 | `en-cours.md` R | « **R4.4 close** » | la porte **humaine** est ouverte ; la fiche elle-même dit « reste ouverte » |
| 6 | `en-cours.md` R | « **R2/R3 attendent N5/N4** » | **R2.1 n'attend ni N5 ni N4** ; R3.1 attend N4 |
| 7 | `en-cours.md` B13 | **178/178** | **183/183** au HEAD ; la porte L est verte |
| 8 | `rapport-r03-banc-complet.md` | **249** questions | le banc vérifie **248** |
| 9 | `rapport-r06-pipeline.md` (titre) | **10/10 refusés** | le corps dit **9/10** ; la roadmap dit 9/10 |
| 10 | `roadmap.md` R4.1 | **996 cellules**, **802** exactes | la porte : **970 cellules**, **776/776** de provenance |
| 11 | `roadmap.md` R4.2 | **294 fichiers** | la porte : **342/342** |
| 12 | `rapport-n2-r11.md` / `rapport-n2-fenetre.md` | `work/n2ac/miroir_copie.py` | le fichier réel est `work/n2ac/mirroir_copie.py` (deux r) |
| 13 | `rapport-r44-scans.md` | « la ligne reste ouverte » **et** « R4.4 est close » | les deux ne peuvent pas être vrais ; statut juste : **partielle** |

## 9. Ce qui pourrait rendre cette fiche fausse

- **Le tagger API n'a pas été rejoué** : les 0,9389 / 0,8241 / 0,8797 sont du **2026-11-04**
  (run 2), pas d'aujourd'hui. `deepseek-chat` peut avoir changé ; deux passes seulement
  (0,9389, 0,9389, 0,9385). Le coût (858 appels, 254 k tokens, 13 min) est la raison.
- **Le 7B local n'est pas reproductible** : les shards GGUF sont **absents** de `models/` ; le
  cache HF est en safetensors. Les 0,8483 / 0,9440 sont **historiques**.
- **Les 0,7749 et 0,8754 sont mes ré-runs** de l'heuristique au HEAD `97256b8f`, sur les mêmes
  golds (inchangés depuis le 02/11). Les 0,7512 / 0,7444 des fiches sont les **mêmes golds avec
  l'ancien code** ; l'écart est le **gain de l'heuristique**, pas une erreur de mesure.
- **Le 0,8500 est l'heuristique, pas le tagger** ; le tagger n'a **jamais** vu les 612. Le
  +6,35 est sur **432 réelles** ; le +7,34 est sur **180** (dont 160 synthétiques). Aucun des
  deux n'est le chiffre du gold 612.
- **R0.3, R0.4-survol, R1.1, R1.2, R1.3 n'ont pas été rejoués** (GPU, checkpoints `work/`). Leurs
  chiffres sont ceux des fiches, datés ; les commandes sont nommées.
- **R4.4** : les portes tournent sur des **caches** (`work/r44/`) ; les scans réels sont
  comparés à la **couche OCR**, pas à l'humain. Les 30 pages ne valent pas 10 pages avec vérité
  humaine.
- **Le HEAD a bougé pendant l'audit** (`de7c9113` → `7a876f70` → `97256b8f`) ; les portes R ont
  tourné à `de7c9113`, la POS a été refaite à `97256b8f` (identique), et les commits
  intermédiaires sont **sans effet mesuré** sur le bloc (`5940ea53` : « aucun effet mesuré »).
- **La date de référence est le 2026-11-06** ; les chiffres de l'`en-cours` et de la roadmap
  peuvent avoir bougé depuis.

## 10. Fichiers et commandes

- **Cette fiche** : `reports/rapport-etat-r.md` ; **données** : `reports/pensee-etat-r.json`.
- **Lues** : `docs/pilotage/roadmap.md` (R), `en-cours.md`, `backlog/R01…R52`,
  `reports/rapport-r01…r07`, `r13*`, `r44-*`, `n2-r11`, `n2-fenetre`, `n2-r12-2048`,
  `pensee-gold-neuronal`, `pensee-gold-syntagmes`, `pensee-gold-cascade`,
  `pensee-quatre-modes-432`, `pensee-quatre-modes-run2`, `memoire-travail-n5`, `file-taches`.
- **Rejouées** : `bash tools/porte-document.sh` ; `bash tools/porte-lecteur.sh` ;
  `bash tools/porte-lecture.sh` ; `bash tools/porte-balayage.sh` ;
  `bash tools/porte-bloc-tableaux.sh` ; `bash tools/porte-bloc-code.sh` ;
  `bash tools/porte-bloc-maths.sh` ; `bash tools/porte-bloc-linguistique.sh` ;
  `bash tools/porte-ocr.sh` ; `bash tools/porte-ocr-scans.sh` ;
  `python3 tools/routeur.py --json /tmp/routeur-etat-r.json` ;
  `python3 tools/banc_complet.py --verifie tools/tests/documents/bench-complet.json` ;
  `python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/pensee-gold-etat-r.json`.
- **Non rejouées** : `tools/tete_survol.py` ; `work/n2ac/eval_fenetre.py` ;
  `work/n2ac/mirroir_copie.py` ; `bash tools/porte-r13-bpe.sh` ; les scans réels (portes
  rejouées depuis le cache).
- **Aucun code, aucun commit, aucun existant modifié** ; les portes écrivent dans `work/`
  (ignoré) et `/tmp`.
