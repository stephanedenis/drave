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

**Prochaine action** : aucune — la table est faite, la quantification testée en 4 et 8 bits (un curseur).

### A2 — Répartir sur les composants d'une machine

| # | chantier | état | critère de succès |
|---|---|---|---|
| A2.1 | **Cache KV sur deux cartes** (paginé) | ✅ | attention à 1 M de clés : 968 → **13,2 ms** |
| A2.2 | **Attention complète sur GPU** (décodage et préremplissage) | ✅ | 22,16 → **3,29 ms/jeton** (÷6,7) |
| A2.3 | **Projections Q8_0 et tête Q6_K sur GPU** (opt-in) | ✅ | 15,6 → 6,2 ms/jeton ; tête : 7,58 → **3,60** |
| A2.4 | **Cache d'experts MXFP4** | ✅ mesuré, **verdict : non** | +6 % — on ne l'active pas tel quel, et c'est écrit |
| A2.5 | **Top-k dans le noyau d'attention GPU** — le dernier chemin qui retombe sur le CPU | ✅ mesuré — opt-in (`DRAVE_GPU_TOPK=1`) | le noyau fusionné (**1 lancement**) gagne jusqu'à ~64 k, la chaîne séparée au-delà (×1,43 à 1 M) ; le croisement **65 k-131 k** et le seuil `SEUIL_NOYAU4 = 131_072` sont **mesurés** ; conforme à 9,7e-7 à 1 M — [`reports/rapport-gpu-topk-tout.md`](../reports/rapport-gpu-topk-tout.md) |
| A2.6 | **Ordonnanceur de placement** : chaque opérateur là où son flux coûte le moins cher (2 GPU, CPU, VRAM, RAM, NVMe) | 🔬 — la règle écrite **et appliquée** | le module [`placement.rs`](../drave-core/src/placement.rs) (les bandes mesurées, `cout`, `classement`, `kv_en_vram`, et la **règle générale `choisir`** — le moins cher **où ça tient**, **4 tests verts**) ; la décision du **KV** y passe ; la **tête** a été essayée par la règle puis **revertée** (le 4 bits coûte +10 % de PPL : la place n'est pas la qualité) ; la mesure à 8 k : **×1,93** / **×5,8** — [`reports/rapport-placement-kv-8k.md`](../reports/rapport-placement-kv-8k.md) ; reste l'ordonnanceur complet (experts, tête) |

**Prochaine action** : aucune — le noyau fusionné et la règle `choisir` sont faits ; la tête a été essayée puis revertée.

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

**Prochaine action** : aucune — `porte-diff-couche` est verte dans la passe (18 s).

### A5 — Formats, matériels, énergie

| # | chantier | état | critère de succès |
|---|---|---|---|
| A5.1 | **Trois matériels** : SIMD x86, PTX sur Quadro, logique FPGA | ✅ | noyaux écrits et vérifiés |
| A5.2 | **Quantification du KV choisie par la mesure** | ✅ | l'écart int8 (+3,0 % à 8 192) est **attribué aux clés** ; clés f16 = **+0,018 %** pour 39 % de la taille ; l'int4 coûte +364 % — le débat n'est pas « combien de bits » mais **où sont les échelles** |
| A5.3 | **Quantification par bloc, par couche** | ✅ — la sensibilité mesurée, la politique écrite | le coût de l'int8 est **tout** dans les premières couches : 8 bits sur 0-11 → **+2,28 %**, sur 12-23 → **+0,03 %** (0,5 B, 255 jetons) ; la politique : les tardives peuvent passer en 8 bits sans perte mesurable — [`reports/rapport-kv-par-couche.md`](../reports/rapport-kv-par-couche.md) ; le 4 bits sur les tardives coûte **+2,7 %** (elles tolèrent le 8, pas le 4) |
| A5.4 | **Le FPGA** : un opérateur complet, alimenté par le même format de flux | 🧱 | dépend d'un accès matériel (le PE événementiel et le lecteur DDR3 existent et sont vérifiés) |

**Prochaine action** : aucune — le 8 bits tardif est gratuit (+0,03 %), le 4 bits +2,7 % ; A5.4 est bloquée par le matériel.

### A6 — Apprendre des flux

Le flux n'est pas qu'une exécution, c'est une donnée.

| # | chantier | état | critère de succès |
|---|---|---|---|
| A6.1 | **Capteur hebbien** : apprendre des journaux d'activation | ✅ mesuré — **négatif** | le capteur coûte +3,0 % ; la création de nœuds par Hebb n'ajoute rien sur 69 % des poids ; et les **produits** n'ajoutent que **+0,0045** de R² sur la couche 6 (la trace linéaire explique déjà 92 %) — [`reports/rapport-hebbien-produits.md`](../reports/rapport-hebbien-produits.md) ; la piste restante : les couches creuses, et le classement par la trace |
| A6.2 | **Routage appris** (MoE) : les experts choisis par les logs | ⏳ | qualité égale, coût de routage ÷10 |
| A6.3 | **Élagage guidé par les logs** : retirer les neurones qui ne s'allument jamais | ✅ mesuré — le critère est **vide** | **0 neurone mort** sur 116 736 (255 jetons) ; **63 %** s'allument à moins de 0,1 % (les rares, pas les morts) ; le top 10 % porte **19 %** de la masse — l'élagage exige un corpus de calibration plus large et la perplexité après masque — [`reports/rapport-elagage-logs.md`](../reports/rapport-elagage-logs.md) |

**Prochaine action** : aucune — A6.1 et A6.3 ont rendu leurs négatifs (les produits +0,0045 ; aucun neurone mort).

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
| B1.6 | **Le dialogue réel** : la conversation spontanée | ✅ mesuré au 1,5 B, **références indépendantes** | **DiaBLa +35,0/+39,3** (les `.ref`, 4 981 paires) contre **+40,3/+44,2** (post-édition) et **+27,0/+30,4** (OpenSubtitles) au même 1,5 B : le biais de la post-édition est de **+5**, et le **dialogue spontané reste plus facile que les sous-titres** — la carte gagne sa ligne, le 3 B gagne **+2 à +3 points** (+38,1/+41,3 contre +35,0/+39,3) : la traduction profite de la taille quand la lisibilité y perd ; le 7 B n'a pas pu être mesuré (15,2 Go de poids sur 15,55) — [`reports/rapport-dialogue-diabla.md`](../reports/rapport-dialogue-diabla.md) |

**Prochaine action** : B1.5 seule — **bloquée** (pas de corpus scientifique humain) ; B1.6 est **mesuré** (DiaBLa).

### B2 — La représentation et le raisonnement (étage 2)

| # | chantier | état | critère de succès |
|---|---|---|---|
| B2.1 | **La RSN** : une représentation partagée, mais non alignée | ✅ | pont 28-69 %, cos 0,78-0,92, insensible à la taille |
| B2.2 | **La composition** | ✅ | 0,61 / 0,84 → **0,76 / 0,865** au 7 B |
| B2.3 | **Le raisonnement synthétique** : dans l'état, aligné par un pont linéaire | ✅ | 1,00 → 0,51 ; pont 0,46-1,00 ; quatre langues, douze personnes, trois échelles |
| B2.4 | **L'alignement appris** : bilingue, contraste, saturation | ✅ | 0,656 → 0,742 → **0,753** ; le prix (in-langue 98,7 → 77,6) |
| B2.5 | **Le raisonnement naturel** (XNLI) | ✅ | 0,50-0,59 ; pont 0,59 → **0,77** (fine-tuning) ; le domaine compte plus que le volume |
| B2.6 | **Le plan multi-tâches** : entraîner le plan **et** le raisonnement ensemble | ✅ mesuré — **0,364** | l'EN→FR reste au chiffre de la tâche seule (0,364) ; l'in-langue baisse (0,375), l'EN monte (0,511) — **la ligne plan est définitivement close** |
| B2.7 | **Le 32 B** : la profondeur et l'alignement à une échelle de plus | ✅ mesuré — **le confondant tranché** | à profondeur relative fixe (50 %), le 32 B donne **0,600 / 0,772** (contre 0,410/0,49 à la couche 18, précoce) : la « décroissance avec la taille » était **l'effet de la couche** — mais **l'échelle n'aide pas de façon monotone** : le **14 B** (0,6305/0,815 à la couche 24, **0,7189/0,8701 à la 30**) est **le meilleur des quatre points** — mais **à 83 %, la taille sature** : le **3 B** à la couche 30 donne **0,7269/0,8568** sur le même jeu, une quasi-égalité — et le **14 B plafonne** à sa couche 36 (0,7376/0,8715 : le pont ne bouge plus après la 30) — [`reports/rapport-32b-couche-confondant.md`](../reports/rapport-32b-couche-confondant.md) |
| B2.8 | **Le raisonnement naturel à l'échelle** : XNLI au 14 B/32 B, et un corpus naturel plus dur | ✅ mesuré | **DACCORD +26,9, GQNLI +56,7, XNLI +35,9** de marge (1,5 B, contrôles au hasard) ; **chaque modèle a son pic tardif** : 1,5 B **0,810** (c. 22), 3 B **0,865** (c. 30), 14 B **0,7189/0,8701** (c. 30) — et à **50 %**, le **32 B** mène (0,5997) devant le 1,5 B (0,5783), le 3 B (0,5020) et le **14 B dernier** (0,4833) : **la profondeur décide autant que le modèle**, et le 14 B balaie **+0,147** entre son pire et son meilleur point — [`reports/rapport-32b-couche-confondant.md`](../reports/rapport-32b-couche-confondant.md) |

**Prochaine action** : aucune — le plan résiste, l'échelle est tracée (les pics), DiaBLa est mesuré.

### B3 — Le plan et la dynamique

| # | chantier | état | critère de succès |
|---|---|---|---|
| B3.1 | **L'état de plan** : le contexte joint des 4 phrases | ✅ | 0,43 (FR→FR) ; c'est la meilleure représentation du plan |
| B3.2 | **La résistance** : ponts, bilinguisme, contraste, récurrence | ✅ | tous échouent (0,25-0,39) ; l'apparent transfert est un effet côté cible |
| B3.3 | **La dynamique** : un état qui porte plusieurs pas | ✅ mesuré | le pas n'existe pas au-delà du contexte (mesures 113-115) ; le plan s'entraîne (119-124) |

**Prochaine action** : aucune — la ligne est **définitivement** close (B2.6 testé, mesure 168).

---

## L'ordre du jour (carpe diem)

L'ordre est **la valeur / le coût**, pas la date. **Toutes les lignes non bloquées sont mesurées** (24/10) :

1. ~~B2.6 — le plan multi-tâches~~ **fait** (168 : 0,364, la ligne plan est close).
2. ~~A2.5 — le top-k GPU~~ **fait** (le noyau fusionné, le seuil 131 072 mesuré).
3. ~~A4.3 — le diff par couche dans la porte~~ **fait** (`porte-diff-couche`, 18 s, **verte dans la passe**).
4. ~~A1.5 / A5.3 — la décision par couche~~ **fait** (l'int8 sur les tardives +0,03 %, le 4 bits +2,7 % — un curseur).
5. ~~A2.6 — l'ordonnanceur~~ **partiel** (la règle `choisir`, 4 tests ; le KV l'applique ; la tête essayée puis **revertée**).
6. ~~A6.1 / A6.3~~ **faits et négatifs** (les produits +0,0045 ; aucun neurone mort sur 116 736).
7. ~~B2.7 / B2.8 / B1.6~~ **faits** (le 32 B, les pics par modèle, DiaBLa).
8. **Ce qui reste, nommé** : le pic du 32 B (**OOM**, la VRAM de 16 Go ; la cause est documentée), la prose scientifique
   (**corpus absent**), A6.2 (**pas de MoE local**), A3.4 (**compte Colab**), A5.4 (**FPGA**).

## La file « jamais en attente »

Quand une ligne est bloquée (corpus, compte, matériel), on prend la suivante — et le travail ne s'arrête pas :

- **fait, mesuré** : B2.6, B2.7, B2.8, A2.5, A2.6 (la règle ; la tête **revertée**), A4.3, A1.5, A5.3, A6.1, A6.3 ;
- **bloqué, nommé** : B1.5 (le corpus d'articles), A3.4 (le compte Colab), A5.4 (le FPGA) — B1.6 est **fait**
  (DiaBLa, références indépendantes) ;
- **clos** : B3 (le plan résiste), la falaise du raisonnement (erratum 6), la répartition réseau (le transport est
  fidèle).

## Ce qui est bloqué, et par quoi

| ligne | bloque par | ce qu'il faudrait |
|---|---|---|
| B1.5 prose scientifique | aucun corpus parallèle humain d'articles FR/EN | un corpus (revue, actes, manuel) traduit par des humains |
| A3.4 Colab | le compte et le runtime Colab | un compte (la recette est dans `docs/colab-reparti.md`) |
| A5.4 FPGA | l'accès au matériel Stratix V | la carte (le design existe) |

## Journal des décisions

- **30/09** — le renommage Qtrinet → Drave ; le moteur Rust *est* l'architecture par listes.
- **07/10** — la passe K3 est liée au **disque** (133 Mio/s, 87,6 % d'occupation) ; le levier est la taille du lot.
- **22/10** — le périmètre entrée-sortie est **arrêté au français inclus** ; l'étage 2 devient le chantier principal.
- **23/10** — la vision est **recentrée sur les flots** (ce document) ; les deux programmes avancent en parallèle.
