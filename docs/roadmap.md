# La roadmap de Drave — deux programmes, un ordre, aucune date

> Suite de [`docs/vision.md`](vision.md). Le projet a **deux programmes** : le **moteur** (les flux de données, les
> cinq axes) et l'**intelligence** (les deux étages). Ils avancent **en parallèle** ; l'ordre se décide par la
> **valeur** et les **dépendances**, jamais par une date.

## Comment lire cette roadmap

- **Les états** : ✅ mesuré et écrit · 🔬 en cours · ⏳ à faire · 🧱 bloqué par une infra absente.
- **Le carpe diem** : pas d'échéance. Un chantier est **fait** quand il est **mesuré**, **écrit** (fiche + docs) et
  **committé** ; tant qu'il ne l'est pas, il reste dans la liste — et on ne l'annonce pas avant.
- **DSH ne reste jamais en attente** : chaque ligne a une **prochaine action** ; si elle est bloquée, on prend la
  suivante dans l'ordre. La file d'attente n'existe pas : il y a toujours un chantier non bloqué à faire avancer.
- **Un chiffre sans contrôle négatif n'est pas un résultat** : chaque critère de succès nomme son contrôle (le
  plancher, les paires mélangées, les étiquettes mélangées).

---

## Programme A — Le moteur (la drave, les flux)

### A1 — Observer et régler, neurone par neurone

Un flux de listes est observable par construction : on peut compter, tracer, comparer, sans rien reconstruire.

| # | chantier | état | critère de succès |
|---|---|---|---|
| A1.1 | **Format de trace** (DRVF v2/v3) : par couche et position, les neurones actifs (indice + valeur) | ✅ | 132 Mo pour 512 jetons (258 ko/jeton) et +8 % de temps ; la v3 (i8, échelle par bloc de 32) fait 45,1 Mo contre 66,4, au prix de +0,074 % de perplexité au rejeu |
| A1.2 | **Diff par couche** : où deux exécutions divergent, à quel jeton, quels neurones | ✅ | KV f32 contre int8 → première divergence **couche 1, jeton 0**, 896 neurones, 2,9e-3 de dynamique ; couche la plus touchée : FFN 2 |
| A1.3 | **Le format EST le contrat d'échange** (A3) : versionné, en-tête + paires | ✅ | codec de référence : aller-retour identique sur 132 Mo ; le rejeu redonne les mêmes logits |
| A1.4 | **Profilage par neurone** : densité par couche, part des 10 % les plus forts, neurones dominants | ✅ | densité **20 à 56 %** selon la couche ; top 10 % → **33,1 %** de la magnitude ; **0,08 %** de neurones chauds > 90 % du temps |
| A1.5 | **La décision par couche** : la quantification et le chemin (push/pull) choisis par la mesure, couche par couche | ✅ | la **table** (la densité par couche + le croisement 22 %) et la **vérification** : PPL **identique** (28,4015) entre le push et le dense, le dense **2 %** plus rapide (9,2 contre 9,4 s à 255 jetons) — [`reports/rapport-decision-par-couche.md`](../reports/rapport-decision-par-couche.md) |

**Prochaine action** : A1.5 (la table par couche), puis A1.1-A1.2 dans les portes (voir A4).

### A2 — Répartir sur les composants d'une machine

| # | chantier | état | critère de succès |
|---|---|---|---|
| A2.1 | **Cache KV sur deux cartes** (paginé) | ✅ | attention à 1 M de clés : 968 → **13,2 ms** |
| A2.2 | **Attention complète sur GPU** (décodage et préremplissage) | ✅ | 22,16 → **3,29 ms/jeton** (÷6,7) |
| A2.3 | **Projections Q8_0 et tête Q6_K sur GPU** (opt-in) | ✅ | 15,6 → 6,2 ms/jeton ; tête : 7,58 → **3,60** |
| A2.4 | **Cache d'experts MXFP4** | ✅ mesuré, **verdict : non** | +6 % — on ne l'active pas tel quel, et c'est écrit |
| A2.5 | **Top-k dans le noyau d'attention GPU** — le dernier chemin qui retombe sur le CPU | ✅ mesuré — opt-in (`DRAVE_GPU_TOPK=1`) | le noyau fusionné (**1 lancement**) gagne jusqu'à ~64 k, la chaîne séparée au-delà (×1,43 à 1 M) ; le croisement **65 k-131 k** et le seuil `SEUIL_NOYAU4 = 131_072` sont **mesurés** ; conforme à 9,7e-7 à 1 M — [`reports/rapport-gpu-topk-tout.md`](../reports/rapport-gpu-topk-tout.md) |
| A2.6 | **Ordonnanceur de placement** : chaque opérateur là où son flux coûte le moins cher (2 GPU, CPU, VRAM, RAM, NVMe) | 🔬 — la règle écrite **et appliquée** | le module [`placement.rs`](../drave-core/src/placement.rs) (les bandes mesurées, `cout`, `classement`, `kv_en_vram` avec la réserve de 1 Go, **3 tests verts**) ; la décision du **KV** y passe (le refus est nommé) ; la mesure à 8 k : **×1,93** / **×5,8** — [`reports/rapport-placement-kv-8k.md`](../reports/rapport-placement-kv-8k.md) ; reste l'ordonnanceur complet (experts, tête) |

**Prochaine action** : A2.5 (aucune infra, le dernier repli CPU), puis A2.6.

### A3 — Répartir sur plusieurs machines

| # | chantier | état | critère de succès |
|---|---|---|---|
| A3.1 | **Contrat d'échange** (protocole v5) : en-tête (couche, source, échelle, bits) + paires | ✅ | 79 octets d'en-tête, cinq modes (dense, listes, blocs, lot dense, lot en listes) ; transport TCP fidèle, écart local/réparti **0,00e0** |
| A3.2 | **Granularité** : par couche, par bloc, par expert | ✅ | listes i16, échelles par bloc, indices par écarts : **1 608 octets par flux** à 256 jetons ; le mode « lot en listes » : 1,5 ko/jeton contre 3,5 en dense (÷2,3) |
| A3.3 | **Seuil de rentabilité** : à quel débit/latence le découpage gagne | 🔬 | attente ≈ calcul distant + **3,2 × latence** : 1,01× à 0 ms, 1,99× à 5 ms, 4,89× à 20 ms ; le débit ne compte pas (0,25 Mbit/s) |
| A3.4 | **Démonstration Colab** : préremplissage réparti | 🔬 | le préremplissage par lots est **fait et fidèle** (0,00e0) ; reste le runtime Colab ([`docs/colab-reparti.md`](colab-reparti.md)) |
| A3.5 | **Sûreté** : version dans chaque en-tête, refus des flux incompatibles | ✅ | un pair en version 99 est refusé avec un message qui nomme les deux versions |

**Prochaine action** : A3.4 (la démo distante) — bloquée par le compte Colab ; en attendant, A3.2 (la granularité
par bloc et le cas MoE).

### A4 — Rejouer, comparer, ne pas régresser

Un flux est un journal, et un journal se rejoue.

| # | chantier | état | critère de succès |
|---|---|---|---|
| A4.1 | **Portes de non-régression** : deux chemins d'exécution rendent le même résultat | ✅ | Qwen ctx 256 = **19,3885** ; gpt-oss ctx 256 = **15,6017** |
| A4.2 | **Références indépendantes** : une seconde implémentation de la même formule | ✅ | MLA à **5,2e-7** contre numpy et **0,999024** contre llama.cpp ; patchs 5,4e-7 ; projecteur 1,7e-6 |
| A4.3 | **Diff par couche dans les portes** : après un changement de quantification ou de noyau, savoir *où* le calcul diverge | ✅ | la porte `porte-diff-couche.sh` : deux exécutions identiques → **flux identique** (reproductibilité) ; KV 8 bits → divergence **nommée** (couche 1, jeton 1, 857 neurones, 9,3e-5) ; `diff_flux.py` lit la **v2** (indices par écarts) |

**Prochaine action** : A4.3 (le diff dans la porte) — aucune infra.

### A5 — Formats, matériels, énergie

| # | chantier | état | critère de succès |
|---|---|---|---|
| A5.1 | **Trois matériels** : SIMD x86, PTX sur Quadro, logique FPGA | ✅ | noyaux écrits et vérifiés |
| A5.2 | **Quantification du KV choisie par la mesure** | ✅ | l'écart int8 (+3,0 % à 8 192) est **attribué aux clés** ; clés f16 = **+0,018 %** pour 39 % de la taille ; l'int4 coûte +364 % — le débat n'est pas « combien de bits » mais **où sont les échelles** |
| A5.3 | **Quantification par bloc, par couche** | 🔬 | la politique choisie par la mesure, pas par défaut |
| A5.4 | **Le FPGA** : un opérateur complet, alimenté par le même format de flux | 🧱 | dépend d'un accès matériel (le PE événementiel et le lecteur DDR3 existent et sont vérifiés) |

**Prochaine action** : A5.3 (la politique par bloc) — aucune infra ; A5.4 est bloquée par le matériel.

### A6 — Apprendre des flux

Le flux n'est pas qu'une exécution, c'est une donnée.

| # | chantier | état | critère de succès |
|---|---|---|---|
| A6.1 | **Capteur hebbien** : apprendre des journaux d'activation | 🔬 | une couche améliorée par apprentissage sur ses propres logs |
| A6.2 | **Routage appris** (MoE) : les experts choisis par les logs | ⏳ | qualité égale, coût de routage ÷10 |
| A6.3 | **Élagage guidé par les logs** : retirer les neurones qui ne s'allument jamais | ⏳ | modèle plus petit, perplexité égale |

**Prochaine action** : A6.1 (le capteur, déjà amorcé).

---

## Programme B — L'intelligence (les deux étages)

### B1 — L'entrée-sortie linguistique (étage 1)

| # | chantier | état | critère de succès |
|---|---|---|---|
| B1.1 | **Le juge post-cutoff** : un texte neuf, jamais vu à l'entraînement | ✅ | le règlement 2025 (139 unités) ; l'UDHR contaminée (le 7 B récite) ; toutes les mesures refaites |
| B1.2 | **La qualité de traducteur** : chrF + plancher + marge + intervalle | ✅ | **55-76**, marge **+30 à +40**, répliquée sur un second règlement |
| B1.3 | **Les six registres** : juridique, presse, littéraire, parlé préparé, technique (JRC et prose), dialogue | ✅ | marges de +25,9 (littéraire) à +40,7 (parlé) ; la référence minée démasquée |
| B1.4 | **Les langues et la couverture** : 24 langues UE, les 20, le pidgin, le critère au français inclus | ✅ | +35,8 / +21,5 ; le pidgin écrit +5,8 (7 plis) ; le critère démographique tenu |
| B1.5 | **La prose scientifique** (articles) | 🧱 corpus — la recherche du 24/10 ne trouve que des **comparables** (LIMSI/BUCC) ou du juridique (ACL-SIGLEX) | un corpus parallèle **humain** d'articles ; le MultiUN couvre la prose technique institutionnelle |
| B1.6 | **Le dialogue réel** : la conversation spontanée | 🔬 — mesuré au 1,5 B, **avec réserve** | **DiaBLa +40,3/+44,2** contre **OpenSubtitles +27,0/+30,4** au même 1,5 B — mais **la référence DiaBLa est une post-édition** (le biais vers la machine) : c'est une **borne haute**, pas un septième registre ; les références indépendantes sont à récupérer (le GitHub du corpus) — [`reports/rapport-dialogue-diabla.md`](../reports/rapport-dialogue-diabla.md) |

**Prochaine action** : B1.5/B1.6 — la recherche de corpus. Si aucun corpus humain n'est trouvé, **la ligne se
déclare bloquée** et on passe à B2 ; la carte des registres reste celle de six registres + deux marges nommées.

### B2 — La représentation et le raisonnement (étage 2)

| # | chantier | état | critère de succès |
|---|---|---|---|
| B2.1 | **La RSN** : une représentation partagée, mais non alignée | ✅ | pont 28-69 %, cos 0,78-0,92, insensible à la taille |
| B2.2 | **La composition** | ✅ | 0,61 / 0,84 → **0,76 / 0,865** au 7 B |
| B2.3 | **Le raisonnement synthétique** : dans l'état, aligné par un pont linéaire | ✅ | 1,00 → 0,51 ; pont 0,46-1,00 ; quatre langues, douze personnes, trois échelles |
| B2.4 | **L'alignement appris** : bilingue, contraste, saturation | ✅ | 0,656 → 0,742 → **0,753** ; le prix (in-langue 98,7 → 77,6) |
| B2.5 | **Le raisonnement naturel** (XNLI) | ✅ | 0,50-0,59 ; pont 0,59 → **0,77** (fine-tuning) ; le domaine compte plus que le volume |
| B2.6 | **Le plan multi-tâches** : entraîner le plan **et** le raisonnement ensemble | ✅ mesuré — **0,364** | l'EN→FR reste au chiffre de la tâche seule (0,364) ; l'in-langue baisse (0,375), l'EN monte (0,511) — **la ligne plan est définitivement close** |
| B2.7 | **Le 32 B** : la profondeur et l'alignement à une échelle de plus | ✅ mesuré — mais **confondu par la couche** | le 32 B en nf4 (21 Go) : sonde FR **0,410**, pont **0,49** (le plus bas des quatre) ; **la couche 18 n'a pas la même profondeur relative** (64 % au 1,5 B, 28 % au 32 B) — la décroissance n'est **pas** attribuable à la taille ; la mesure à profondeur relative fixe est en file — [`reports/rapport-32b-couche-confondant.md`](../reports/rapport-32b-couche-confondant.md) |
| B2.8 | **Le raisonnement naturel à l'échelle** : XNLI au 14 B/32 B, et un corpus naturel plus dur | 🔬 — la première mesure faite | **DACCORD +26,9, GQNLI +56,7, XNLI +35,9** de marge (1,5 B, contrôles au hasard) : *le jeu dur est lisible, sa marge est la plus faible* ; et le **1,5 B lit mieux que le 3 B et le 14 B** (0,692 contre 0,502 et 0,481 ; pont **0,83** contre 0,592 et 0,627) — mais **confondu par la couche** (18 = 64 % de la profondeur au 1,5 B, 37 % au 14 B) : le renversement n'est pas attribuable à la taille, la mesure à profondeur fixe est en file — [`reports/rapport-nli-francais-dur.md`](../reports/rapport-nli-francais-dur.md) |

**Prochaine action** : **B2.6** (le plan multi-tâches — aucune infra, la seule variante non testée), puis B2.7/B2.8.

### B3 — Le plan et la dynamique

| # | chantier | état | critère de succès |
|---|---|---|---|
| B3.1 | **L'état de plan** : le contexte joint des 4 phrases | ✅ | 0,43 (FR→FR) ; c'est la meilleure représentation du plan |
| B3.2 | **La résistance** : ponts, bilinguisme, contraste, récurrence | ✅ | tous échouent (0,25-0,39) ; l'apparent transfert est un effet côté cible |
| B3.3 | **La dynamique** : un état qui porte plusieurs pas | ✅ mesuré | le pas n'existe pas au-delà du contexte (mesures 113-115) ; le plan s'entraîne (119-124) |

**Prochaine action** : aucune — la ligne est **définitivement** close (B2.6 testé, mesure 168).

---

## L'ordre d'aujourd'hui (carpe diem)

L'ordre est **la valeur / le coût**, pas la date. Les quatre premiers ne dépendent d'aucune infra ; ils peuvent
tourner en parallèle sur deux GPU.

1. ~~B2.6 — le plan multi-tâches~~ **fait** (mesure 168 : 0,364, la ligne plan est close) ; le premier item est **A2.5**.
2. **A2.5 — le top-k GPU** (2-3 h, 1 GPU) : le dernier repli CPU du moteur.
3. **A4.3 — le diff par couche dans la porte** (1 h, CPU) : la condition du rejeu utile.
4. **A1.5 / A5.3 — la décision par couche** (2 h, CPU + 1 GPU) : la quantification et le chemin choisis par la mesure.
5. **B2.7 — le 32 B** (si la mémoire le permet : quantifié) : l'échelle au-delà du 14 B.
6. **A3.4 — la démo Colab** (le compte Colab) : la répartition réseau.
7. **B1.5/B1.6 — la prose scientifique et le dialogue réel** (la recherche de corpus) : en parallèle, sans bloquer.
8. **A5.4 — le FPGA** (le matériel) : bloqué, nommé, pas oublié.

## La file « jamais en attente »

Quand une ligne est bloquée (corpus, compte, matériel), on prend la suivante — et le travail ne s'arrête pas :

- **toujours faisable** : B2.6, B2.7, B2.8, A2.5, A2.6, A4.3, A1.5, A5.3, A6.1-A6.3 ;
- **bloqué, nommé** : B1.5 (corpus d'articles), B1.6 (corpus de conversation), A3.4 (compte Colab), A5.4 (FPGA) ;
- **clos** : B3 (le plan résiste), la falaise du raisonnement (erratum 6), la répartition réseau (le transport est
  fidèle).

## Ce qui est bloqué, et par quoi

| ligne | bloque par | ce qu'il faudrait |
|---|---|---|
| B1.5 prose scientifique | aucun corpus parallèle humain d'articles FR/EN | un corpus (revue, actes, manuel) traduit par des humains |
| B1.6 dialogue réel | aucun corpus de conversation spontanée FR/EN aligné | des transcriptions avec traductions |
| A3.4 Colab | le compte et le runtime Colab | un compte (la recette est dans `docs/colab-reparti.md`) |
| A5.4 FPGA | l'accès au matériel Stratix V | la carte (le design existe) |

## Journal des décisions

- **30/09** — le renommage Qtrinet → Drave ; le moteur Rust *est* l'architecture par listes.
- **07/10** — la passe K3 est liée au **disque** (133 Mio/s, 87,6 % d'occupation) ; le levier est la taille du lot.
- **22/10** — le périmètre entrée-sortie est **arrêté au français inclus** ; l'étage 2 devient le chantier principal.
- **23/10** — la vision est **recentrée sur les flots** (ce document) ; les deux programmes avancent en parallèle.
