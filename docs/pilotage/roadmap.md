# La roadmap de Drave — un seul plan, quatre chantiers

> **Un seul document de plan.** Le **moteur** (A), l'**intelligence** (B), le **natif** (N) et le **lecteur** (R).
> L'ordre se décide par la **valeur** et les **dépendances**, jamais par une date. Les chiffres, les séries et les
> contrôles vivent dans [`reports/`](../../reports/) ; ici : l'état, la prochaine action, et ce qui bloque.
>
> **Détail et histoire** : l'ancien plan A/B est archivé dans
> [`roadmap-detail-2026-10-29.md`](../archive/roadmap-detail-2026-10-29.md), le détail N dans
> [`roadmap-native-2026-10-29.md`](../archive/roadmap-native-2026-10-29.md). Les **fiches de fonctionnalité** sont
> dans [`backlog/index.md`](backlog/index.md) ; le **graphe des dépendances** est dans
> [`backlog/dependances.md`](backlog/dependances.md). La **page vivante** est [`en-cours.md`](en-cours.md).

## Comment lire cette roadmap

- **Les états** : ✅ mesuré et écrit · 🔬 en cours · ⏳ à faire · 🧱 bloqué par une infra absente.
- **Le carpe diem** : pas d'échéance. Un chantier est **fait** quand il est **mesuré**, **écrit** (fiche + docs) et
  **committé** ; tant qu'il ne l'est pas, il reste dans la liste — et on ne l'annonce pas avant.
- **DSH ne reste jamais en attente** : chaque ligne a une **prochaine action** ; si elle est bloquée, on prend la
  suivante. La file d'attente n'existe pas : il y a toujours un chantier non bloqué à faire avancer.
- **Un chiffre sans contrôle négatif n'est pas un résultat** : chaque critère de succès nomme son contrôle.
- **Un seul plan, quatre chantiers** : les **deux programmes de la vision** (moteur, intelligence) se découpent en
  **A** (moteur), **B** (intelligence), **N** (natif) et **R** (lecteur). A et B sont l'existant ; N est la ligne
  native ; R est la **nouvelle ligne lecteur**, qui donne une cible mesurable aux deux autres. On charge **un**
  chantier, pas le document entier.

## En un coup d'œil

| chantier | ce qu'il couvre | état | prochaine action |
|---|---|---|---|
| **A — le moteur** | formats, placement, transport, rejeu, matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4, A6.2 bloqués** ; A2.6 partiel ; A3.2/A3.3 mesurées ; **A8.3 refusé, A8.3c expliqué** | **A2.6** (experts : A6.2 bloqué) ; réduire le lot |
| **B — l'intelligence** | langue, pensée, jeux, maîtres, banc externe, sémantique, modules | ✅ B1–B12 ; **B1.5 corpus**, **B12.10 et B10.2bis closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste | B11.10 (cartes) ; B10.3 attend un **encodeur qui porte** |
| **N — le natif** | DRVM, `drave-n0`, distillation, usage, échelle | 🔬 N0/N1 mesurés ; **N0.3b close** ; N2 plafonne à 2,708 ; N4 partiel | **N2** (la hiérarchie), **N4** (consigne courte) |
| **R — le lecteur** | document, politique de lecture, fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; R0.4 **pilote négatif** ; **R4.1–R4.3 mesurées** | **R0.4** — négatifs difficiles ; **R4.4 bloqué** (OCR) |

## L'ordre du jour (carpe diem)

L'ordre est **la valeur / le coût**, pas la date. La dernière mise à jour est le **2026-10-29**.

1. **R0 — le lecteur v0** : **R0.1, R0.2 et R0.3 sont mesurés** (51 pages ; récupération **1,000** à
   30 % sur 5 types et **249 questions**) ; **R0.4** (tête de survol) est un **pilote négatif**
   (0,601 contre BM25 0,836) et **R0.5** (routeur) un **signal** (AUC 0,785, règle non transférable).
   **R4.1 — le bloc tableaux** est **mesurée** (996 cellules, **802** exactes, texte plat **0/3**),
   **R4.2 — le bloc code** aussi (294 fichiers, 24/24 extraits, texte seul **0/3**) et **R4.3 —
   le bloc maths** (32 formules, 10/10 dérivées, surface **0/3**) ; **R4.4 est bloqué** (OCR).
2. **N2 — la distillation et la hiérarchie** (en cours) : 49 999 fenêtres, 4 sources ; professeur 30k **1,734**
   (0,794 bit/octet) ; student **3,123** à 20 000 pas ; meilleur **2,6998** ; plateau **2,708** ; porte **< 2,5 non
   atteinte**. Le levier retenu est la **hiérarchie** (état de section), portée par N2.
3. ~~N0.3b — la parité de perplexité DRVM ↔ GGUF~~ **close** : conversion **68,1917 / 92,1875**, natif **4,6585 / 18,6394**.
4. **N4 — l'usage** : la **consigne courte** tenue à l'écart ; SFT **24/24 vus, 0/4 tenus** ; service 69 octets /
   611 ms. La restitution depuis un document lu est **R31**.
5. **R11/R12 — la fenêtre** : après N2 ; PPL à 1 000 octets et aiguille native.
6. **R21/R31 — la mémoire et la restitution** : après R0.3 ; la restitution attend le gist.
7. **N3, R13** — les autonomes restants, qui remplissent la file « jamais en attente ».
8. **Les bloqués** : A3.4 (Colab), A5.4 (FPGA), A6.2 (MoE local), B1.5 (corpus scientifique) — on prend la ligne
   suivante, jamais l'attente. **N5 est gelé** jusqu'au verdict de R11 sur le contexte ; B10.3 attend un **z qui porte** : l'objectif mot a levé le décodeur (32,5 ; **26,7 sur JW, au-dessus du plancher 17,1**), le contrôle `z` montre qu'il ne lit que ~7 % du sens.

---

## Programme A — Le moteur (la drave, les flux)

Le moteur est **mature** : les cinq axes de la vision ont leurs mesures. Les lignes restantes sont des **lignes
ouvertes**, des **bloqués nommés** ou des **opt-in** à passer par défaut. Le détail chiffré et les fiches sont dans l'archive A/B.

| # | chantier | état | prochaine action |
|---|---|---|---|
| **A1** | observer et régler : trace v3, diff par couche, profilage, décision par couche | ✅ | aucune — la table est faite, la quantification testée |
| **A2** | placer sur une machine : KV paginé, GPU, top-k, ordonnanceur | ✅ / ⚠️ | **partielle** — tête 4 bits refusée (+10 % PPL), experts bloqués par **A6.2** ; [`bilan`](../../reports/rapport-a26-bilan.md) |
| **A3** | répartir : protocole v5, granularité, seuil, Colab | ✅ / 🧱 | **A3.2/A3.3 mesurées** ; **A3.4 bloqué** (compte Colab) |
| **A4** | rejouer, comparer : portes, références indépendantes, diff | ✅ | aucune |
| **A5** | formats, matériels, énergie : SIMD, PTX, FPGA, KV | ✅ / 🧱 | **A5.4 bloqué** (FPGA) ; le 8 bits tardif est gratuit (+0,03 %) |
| **A6** | apprendre des flux : capteur hebbien, routage MoE, élagage | ✅ / ⏳ | **A6.2 bloqué** (pas de MoE local) ; A6.1/A6.3 ont rendu leurs négatifs |
| **A7** | la grappe déportée : relais, grappe intra-couche, format sparse | ✅ | la suite (WAN) est **hors plan** |
| **A8** | l'ordonnanceur place **et** perte : `choisir_avec_perte` | ✅ **opt-in** ; 6 portes épinglées, A8.3 **échoue** (−5,9 % … +19,5 %) | **A8.3b** : isoler le mode de lot (le signe du mélange) |

**Ce qui compte pour R** : le moteur sait déjà exécuter un modèle externe (Qwen 0,5 B à 12 288 jetons), tracer,
rejouer et payer le calcul au prorata de l'activité. C'est le support de R0.

---

## Programme B — L'intelligence (les deux étages)

L'étage 1 (langue) est mesuré ; l'étage 2 (pensée) est mesuré dans ses opérations, avec des négatifs nommés.
La ligne ouverte est **B10.3** (décodeur) ; **B12.10** et **B10.2bis** sont **closes** (négatif) ; **B1.5** est bloquée par le corpus.

| # | chantier | état | prochaine action |
|---|---|---|---|
| **B1** | l'entrée-sortie linguistique : juge, chrF, registres, 24 langues, dialogue | ✅ | **B1.5 bloquée** (aucun corpus parallèle humain d'articles) |
| **B2** | représentation et raisonnement : RSN, composition, XNLI, 32 B | ✅ | aucune — l'échelle et la profondeur sont tracées |
| **B3** | le plan et la dynamique | ✅ **close** | aucune — le plan résiste (0,43), la ligne est close |
| **B4** | les opérateurs abstraits : négation, composition, LoRA | ✅ **close** | aucune — six mesures, le LoRA **inverse** la lecture |
| **B5** | la sémantique des jeux : contrat RSN-jeu, cinq niveaux, bruit | ✅ | aucune — 112 items, **100 %** au niveau 4 |
| **B6** | la logique dans la pensée : règles, recherche, cartes, invariance | ✅ | aucune — perft, **3/3** mats, dames **20/20**, cartes **79,7 %** |
| **B7** | les langues : 71 langues, 1 433 couples, 449 surfaces | ✅ | aucune — **449/449**, **11/11** paires invariantes |
| **B8** | les maîtres : 17 principes, 9 sources, livre, parties | ✅ | aucune — livre **10/10**, go 9×9 **10/10** contre 3/10, cartes **44,7 %** |
| **B9** | le banc externe et l'élève natif : DeepSeek, 610/910 prompts | ✅ | resserrer la transition **9,23–9,96 M** ; porter le masque dans le trainer |
| **B10** | le protocole sémantique : encodeur `z`, décodeur, raisonnement | ✅ / ❌ / ⏳ | **B10.3 bloqué** ; 5 leviers : l'**objectif mot** lève le décodeur (**32,5** UDHR, **26,7** JW > plancher 17,1) mais le `z` ne porte que **1,9–2,6** points — le verrou est l'encodeur |
| **B11** | la base d'universaux typés : schéma, parseur, codec, contexte | ✅ / ⚠️ | B11.10 (cartes et ambiguïtés) ; le codec lit **100 %** |
| **B12** | les modules cerveau-langage M1–M9 | ⚠️ / ❌ | **B12.10 close** (négatif : oracle = M8, M4 seul = 0) ; seul M1 est solide |
| **C3.2** | les modules par famille de langues | ✅ | aucune — **7/9 > 30 %**, moyenne **69,5 %**, contrôle **≤ 0,5 %** |

**Ce qui compte pour R** : le **codec classique** lit **100 %** des surfaces ; c'est la preuve qu'un bloc
classique peut être le meilleur lecteur d'un domaine. Le décodeur neuronal, lui, reste **sous le plancher** :
la restitution n'est pas acquise.

---

## Programme N — Le natif (DRVM, `drave-n0`, distillation)

**Repartir à neuf, pas à zéro.** On garde le moteur, le bus, DRVF, les portes et l'outillage ; on remplace la base
(GGUF, Qwen3-MoE, le modèle monolithique) par un **format** (DRVM) et un **modèle** (`drave-n0`) conçus pour les
mécanismes Drave. Détail complet : [`roadmap-native-2026-10-29.md`](../archive/roadmap-native-2026-10-29.md).

| # | chantier | état | prochaine action |
|---|---|---|---|
| **N0** | le format DRVM : manifeste, payload, lecture, convertisseurs, trace/rejeu, refus | ✅ | aucune — N0.3b est **close** (conversion et natif) |
| **N1** | `drave-n0` : 11,47 M, 6 blocs, octets, attention locale, FFN creux, 3 têtes précoces | ✅ | aucune — PPL **3,465** avec pont (**4,080** sans) ; têtes **57,6 / 61,6 / 62,1 %** contre **62,7 %** ; réflexe **−24,05 %** de temps pour **−1,61** point ; pensée **λ = 0,709** ; cache **19,25×** |
| **N2** | la distillation : 49 999 fenêtres, 4 sources, professeur Qwen/DeepSeek | 🔬 | **N2** — la **hiérarchie** (état de section, 3 graines) ; porte **< 2,5** non atteinte (meilleur **2,6998**, plateau **2,708**) |
| **N3** | les opérations natives : k-WTA, routes, sortie précoce, pont, rejeu, placement | 🔬 **couvert par brique** | **N3.2a/b0/b1/b2 · N3.3a/b/c · N3.4a/b/c · N3.4d · N3.5a/b/c/d/e/f ✅** ; N3.6 composition ; B11.10 |
| **N4** | l'usage : génération, service, SFT, sûreté | ✅ / ⚠️ | **N4** — la **consigne courte** tenue à l'écart (**24/24 vus, 0/4 tenus**) ; la lecture est **R31** |
| **N5** | l'échelle : 50–100 M, corpus élargi | ⏸ **gelé** | après le verdict de **R11** sur le contexte ; BPE si R13 le justifie |

**Les trois leçons N qui contraignent R** :

1. **Le contexte est le verrou.** 129 octets est le meilleur point (**PPL 2,6998**) ; **130** est négatif
   (**2,7149**), **136** (**2,974**), **160** (**3,804**), **256** (**5,675**). À **2 000 octets**, la PPL native
   est **54,04**. Le modèle **surapprend sa longueur** : allonger le contexte demande un **autre schéma**, pas un
   curriculum de plus.
2. **Le saut de calcul existe, le saut de contenu n'existe pas.** La sortie précoce gagne **24,05 %** de temps en
   perdant **1,61 point** ; c'est une décision sur la **confiance du prochain octet**, pas sur la **pertinence**.
3. **La mémoire manque.** Le signal courant est lisible (R² **0,992**), celui d'il y a 8 pas ne l'est pas
   (**−0,681**), et l'entraînement l'aggrave (**−1,091 → −2,773**). Le tampon gelé lit **+0,879**, mais le réseau
   ne s'en sert pas.

---

## Programme R

**Synthèse : [le programme R en une page](programme-r.md)** — ce qui tient, ce qui ne tient pas, les trois lois. — Le lecteur (la nouvelle cible)

**La cible** : lire un document **comme un humain lit vite** — survoler, balayer, lire sélectivement, revenir — en
payant le calcul au prorata de ce qui est lu, et **prouver** la compréhension par la restitution. Le concept, les
14 techniques et les cinq couches manquantes sont dans [`lecture-rapide.md`](../theorie/lecture-rapide.md).

**La métrique** n'est pas le débit : c'est **la compréhension par unité de calcul** — une courbe
vitesse-compréhension, avec un **contrôle négatif** (ce qu'on perd quand on saute). Un « lecteur rapide » qui ne
sait pas dire ce qu'il a sauté n'est pas un lecteur, c'est un filtre.

### Les six phases

| phase | livrable | ce qui est mesuré | dépend de |
|---|---|---|---|
| **R0 — le lecteur v0** | graphe de document, contrôleur classique, banc | exactitude, citation, événements, octets, secondes ; courbe par type | **rien** (modèle externe) |
| **R1 — la fenêtre native** | contexte hiérarchique, curriculum, tokenisation | PPL à 1 000 octets, aiguille native, stabilité | R0, N1 ; plafonné par N2 |
| **R2 — la mémoire** | gist, entités, store épisodique, relecture | réponse multi-sections, citation, relecture | R1, et le négatif de mémoire (acquis) |
| **R3 — la restitution** | SFT de lecture, réponse/résumé/extraction, citations | exactitude tenue à l'écart, fidélité | R0, R2 ; plafonné par N4 |
| **R4 — les blocs structurels** | tableaux ✅, code ✅, maths ✅, vision/OCR 🧱 | extraction exacte, exécution, layout | R0 |
| **R5 — la lecture croisée** | multi-documents, retrieval, multilingue | comparaison, provenance, traduction | R3 ; encodeur exécutable (manque M4) |

### R0 — le lecteur v0 (système, sans entraînement)

C'est la **priorité** : un lecteur au niveau **système**, avec le moteur existant et un modèle externe, pour
établir la cible avant de la porter dans le natif.

| # | fonctionnalité | état | porte |
|---|---|---|---|
| **R0.1** | **graphe de document** : régions typées (titre, section, paragraphe, tableau, code, maths, figure), offsets, provenance ; parseurs PDF/HTML/DOCX/Markdown ; sans modèle | ✅ **51 pages**, fidélité **1,000** | 50 pages découpées, provenance exacte, rejeu identique |
| **R0.2** | **contrôleur de lecture** : `survol`, `balayage`, `lecture`, `relecture`, `arrêt` ; budget en octets ; classique d'abord (TOC, titres, premières/dernières phrases, BM25/regex) | ✅ **1,000** à 30 % sur **5 types** | à 30 % du budget, **≥ 90 %** de la réponse de la lecture intégrale sur **3 types** |
| **R0.3** | **banc de lecture rapide** : 30 documents, 5 types, 10 questions/spans gold, modes intégral/écrémage/balayage/sélectif, contrôles closed-book, régions aléatoires, sections mélangées | ✅ **249 questions** : extractif **1,000** à 30 % ; modèle **0,231** contre début **0,042**. **Durci** (84 paraphrases) : modèle **0,375**, lexical **0,269** | une courbe vitesse-compréhension par type ; le contrôle négatif **échoue** |
| **R0.6** | **pipeline de lecture** : l'assemblage R0.1–R0.3 — budget, provenance, refus, rejeu ; extractif par défaut, modèle sur demande | ✅ **12/20** au pilote, **9/10** refusés, **7/8** au modèle, porte 7/7 ; **voie auto** : +0,109 sur les valeurs, −0,150 sur le mixte | — (livré) |
| **R0.5** | **routeur extractif / génératif** : choisir le lecteur selon la question (signal BM25), parce qu'aucun des deux ne gagne partout | ⚠️ **signal AUC 0,826** ; z-score transfère 0,802 mais reste sous le choix fixe | le routeur bat chaque lecteur fixe sur les deux bancs |
| **R0.4** | **têtes de lecture** : `survol` (pertinence d'une région), `balayage` (requête → spans), `relecture` (confiance/contradiction), greffées sur les têtes précoces | ❌ **survol** : v1 0,601/0,836, v2 0,448/0,811, v3 0,575/0,745 ; **relecture** : relire plus ne change rien (0/249) ; **cascade** +1,2 pt (9 appels) ; **balayage** : classique ✅ rappel@10 0,984/0,702 | la tête bat le contrôle classique à budget égal |

**Ordre arrêté** : **R0.1**, puis **R0.2**, puis **R0.3** (la courbe de R0.3 est la mesure jointe de R0.2) ; R0.4
seulement après la ligne de base.
**Contrôles négatifs** : régions aléatoires au même budget, sections mélangées, questions dont la réponse est dans le
titre, **closed-book**. **Ce qui pourrait le rendre faux** : spans gold dans les titres, contrôleur réglé sur le
test, modèle qui répond de mémoire, petit N, temps mesuré à chaud.

### R1 — la fenêtre native

| # | fonctionnalité | état | porte |
|---|---|---|---|
| **R1.1** | **contexte hiérarchique** : span → paragraphe → section → document, avec un **état de section** ; le modèle n'a pas besoin de voir toute la page | ⏳ | PPL à 1 000 octets dans un facteur **1,5** de celle à 129 ; aiguille **native** ≥ 15/18 à 4 000 octets |
| **R1.2** | **curriculum de contexte** : une recette qui ne refait pas les négatifs 130/136/160/256 ; piste : états de résumé, pas seulement des positions | ⏳ | 1 000 octets **stable**, pas un point isolé |
| **R1.3** | **tokenisation** : octets ou BPE ; la décision est **mesurée**, pas doctrinale | 🔬 **condition** | à octets égaux, français BPE **1,8142/1,8726** contre **1,8021** ; anglais **2,7522/2,8147** contre **2,6408** ; à pas égaux −9,4 % |

**Ce qui bloque** : les 130–256 sont **tous négatifs**. R1.1 doit être tenté **avant** R1.2 : si la hiérarchie
suffit, le contexte brut n'est pas le premier chantier.

### R2 — la mémoire

| # | fonctionnalité | état | porte |
|---|---|---|---|
| **R2.1** | **mémoire de travail / gist** : état de résumé par section, table d'entités et de faits, tampon en entrée | ⏳ | réponse dont l'indice est en section 2 après lecture de la section 5, **avec citation** ; closed-book échoue |
| **R2.2** | **mémoire épisodique / relecture** : store de régions (offsets), KV avec éviction, déclencheur de relecture | ⏳ | la relecture récupère une information que le gist a perdue ; contrôle : sans le store, échec |

**Ce qui bloque** : le négatif de mémoire est établi — le réseau ne retient pas le signal à 8 pas. R2.1 doit donc commencer par
le **tampon en entrée** (qui lit déjà **+0,879**), pas par un entraînement de mémoire.

### R3 — la restitution

| # | fonctionnalité | état | porte |
|---|---|---|---|
| **R3.1** | **SFT de lecture** : réponse, résumé, extraction, refus ; jeux tenus à l'écart | ⏳ | **≥ 80 %** des instructions tenues à l'écart ; le contrôle 24/24 vus ne compte pas |
| **R3.2** | **citations et provenance** : chaque réponse cite la région et l'offset | ⏳ | exactitude de citation ; le contrôle sans citation est plus bas |

**Ce qui bloque** : N4.6 est **24/24 vus, 0/4 tenus** ; le décodeur sémantique est **sous le plancher chrF**
(12,7 / 5,3 contre 39,6). La restitution est le **chantier le plus dur** après le contexte.

### R4 — les blocs structurels

| # | fonctionnalité | état | porte |
|---|---|---|---|
| **R4.1** | **tableaux** : parseur 2D, en-têtes, cellules, opérations classiques (filtre, jointure, agrégat) | ✅ **996 cellules**, **802** exactes, texte plat **0/3** | extraction exacte sur 100 cellules ; contrôle : texte plat |
| **R4.2** | **code** : AST, portée, flux de données, exécuteur/interpréteur bloc | ✅ **294 fichiers**, **24/24** extraits, texte seul **0/3** | réponse par exécution exacte ; contrôle : lecture du texte seul |
| **R4.3** | **maths** : LaTeX/MathML, définitions, preuve ; CAS bloc | ✅ **32 formules**, **10/10** dérivées, surface **0/3** | évaluation symbolique exacte ; contrôle : surface |
| **R4.4** | **vision/OCR** : scans, figures, layout | 🧱 **bloqué** : aucun OCR sur la machine | 10 pages scannées, même réponse que le texte natif |

**Principe** : ces blocs sont **classiques d'abord**. Le bus les accepte comme les blocs neuronaux ; un parseur
de tableaux n'a pas besoin d'être appris.

### R5 — la lecture croisée et le multilingue

| # | fonctionnalité | état | porte |
|---|---|---|---|
| **R5.1** | **multi-documents** : index, retrieval, comparaison, provenance, contradictions | ⏳ après R3 | réponse comparative avec deux sources citées ; contrôle : une seule source |
| **R5.2** | **lecture en traduction** : décodeur au-dessus du plancher chrF, puis lecture multilingue | ⏳ après B10.3 | chrF > **39,6** ; la réponse ne dépend pas de la langue source |

### Ce que R ne fait pas

- **Ce n'est pas « lire à 1 000 mots/minute »** : la revue de Rayner et al. (2016) montre que la vitesse élevée
  avec compréhension pleine n'est pas au rendez-vous ; le levier est l'**allocation**, pas le débit.
- **Ce n'est pas « ajouter des paramètres »** : à 20 000 pas, le student 21,63 M fait **3,381** contre **3,123**
  pour 11,47 M ; la capacité à budget égal donne **−8,1 %**, mais le prior domine. La structure d'abord.
- **Ce n'est pas « la vision avant le texte »** : la plupart des documents sont du texte structuré ; les parseurs
  classiques sont moins chers et mesurables. R4.4 vient après R4.1–R4.3.
- **Ce n'est pas « un résumeur avant un lecteur »** : le décodeur est sous le plancher ; on mesurerait le plancher.

**Les fiches de fonctionnalité** : [`backlog/index.md`](backlog/index.md) — une fiche par fonctionnalité R, avec le
contrat, la porte, les contrôles négatifs et ce qui pourrait la rendre fausse.
**Les termes** : [glossaire, famille 12](../theorie/glossaire/12-la-lecture-le-document-et-ses-mesures.md) — lecture
rapide, graphe de document, gist, mesures et blocs structurels.

---

## La file « jamais en attente »

Quand une ligne est bloquée (corpus, compte, matériel), on prend la suivante — et le travail ne s'arrête pas :

- **non bloqué, à faire** : **R0.5** (routeur, `8156fdcb`) ; **R0.4** (négatifs difficiles) ;
  **N2** (la hiérarchie) ; **N4** (consigne courte) ; **N3/R13** (natif/lecteur) ;
  **N3** (opérations natives) ; **R13** (octets ou BPE) ; **A8.3b** (mode de lot) ;
- **gelé** : **N5** (50–100 M) — après le verdict de R11 sur le schéma ;
- **bloqué, nommé** : B1.5 (corpus d'articles), A3.4 (compte Colab), A5.4 (FPGA), A6.2 (pas de MoE local),
  B10.3 (B10.2bis absent du backlog), **R4.4** (aucun OCR : ni tesseract ni pytesseract) ;
- **clos** : B2.6 (le plan multi-tâches), B3 (le plan résiste), B4 (les opérateurs), B5/B6 (les jeux), B7/B8
  (langues et maîtres), C3.2 (familles), N0.3b (parité DRVM ↔ GGUF), B12.10 (intégration, négatif).

## Ce qui est bloqué, et par quoi

| ligne | bloqué par | ce qu'il faudrait |
|---|---|---|
| B1.5 prose scientifique | aucun corpus parallèle humain d'articles FR/EN | un corpus (revue, actes, manuel) traduit par des humains |
| A3.4 Colab | le compte et le runtime Colab | un compte (la recette est dans `docs/archive/colab-reparti.md`) |
| A5.4 FPGA | l'accès au matériel Stratix V | la carte (le design existe) |
| A6.2 MoE local | aucun MoE local ne tient dans 16 Go de VRAM | un MoE qui tient, ou une machine plus grande |
| B10.3 raisonnement sur `z` | le décodeur est sous le plancher chrF | une attention croisée, 20–30 articles, 3 graines |

## Les questions ouvertes

- **R0** : un contrôleur **classique** + un modèle externe atteint-il **90 %** de la compréhension à **30 %** du
  coût sur trois types de documents ?
- **R1** : la **hiérarchie portée par N2** suffit-elle à lire **1 000 octets** sans refaire les négatifs 130–256 ?
- **R2** : un **gist** explicite bat-il le **closed-book** sur une question dont l'indice est loin ?
- **N2** : le student peut-il descendre sous **2,5** de PPL, ou le plateau **2,708** est-il la capacité du corpus ?
- **B10.3** : un décodeur à attention croisée dépasse-t-il le plancher **39,6** de chrF ?

## Le détail et l'histoire

- **A/B — détail mesuré** : [`roadmap-detail-2026-10-29.md`](../archive/roadmap-detail-2026-10-29.md) (473 lignes,
  archive).
- **N — détail mesuré** : [`roadmap-native-2026-10-29.md`](../archive/roadmap-native-2026-10-29.md) (176 lignes,
  archive).
- **Les fiches** : [`reports/README.md`](../../reports/README.md) et [`reports/INDEX.md`](../../reports/INDEX.md).
- **Le graphe des dépendances** : [`backlog/dependances.md`](backlog/dependances.md) — 41 arêtes dures,
  3 plafonds, la frontière et les sous-items.
- **Le récit daté** : [`journal/`](../../journal/README.md) ; le journal des décisions de la roadmap est dans
  [`journal/2026-10-27/decisions-roadmap.md`](../../journal/2026-10-27/decisions-roadmap.md).
- **Le concept du lecteur** : [`lecture-rapide.md`](../theorie/lecture-rapide.md) ; le **backlog** :
  [`backlog/index.md`](backlog/index.md).
