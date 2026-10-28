# La roadmap de Drave — deux programmes, un ordre, aucune date

> **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Compteurs
> unifiés (**49 portes, 8 chapitres, 185 fichiers / 252 JSON, 54 documents**), chemins archivés
> corrigés (`docs/archive/`), B10–B12 réintégrés dans les cartes. **Les règles d'`AGENTS.md`
> ne changent pas.** *Spécifique : le bas de la page (ordre du jour, file, décisions) est
> remis à jour ; B11 précède B12.*

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

## En un coup d'œil

| programme | ce qui est mesuré | ce qui reste ouvert |
|---|---|---|
| **A — le moteur** | A1–A8 : les formats, le placement, le transport, le rejeu, les matériels | A3.4 (Colab), A5.4 (FPGA), A6.2 (MoE local) — **bloqués** |
| **B — l'intelligence** | B1–B12 : la langue, la pensée, les jeux, les maîtres, le banc externe, la sémantique | B1.5 (corpus), B10.3 (décodeur), B12.10 (modules) |

**Charger ce bloc, puis la section A ou B** ; le document entier (450 lignes) est une référence, pas un
chargement par défaut. Le détail de chaque ligne est dans les tableaux ci-dessous.


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
| A3.4 | **Démonstration Colab** : préremplissage réparti | 🔬 | le préremplissage par lots est **fait et fidèle** (0,00e0) ; reste le runtime Colab ([`docs/archive/colab-reparti.md`](archive/colab-reparti.md)) |
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

### A7 — La grappe déportée

**Le cœur de la vision, et le pas qui n'est pas encore fait** : exécuter une **couche** (ou une grappe de neurones)
sur une **autre ressource**, pilotée par les flux — pas seulement transporter le flux, mais *faire le calcul
ailleurs*.

| # | chantier | état | critère de succès |
|---|---|---|---|
| A7.1 | **La greffe** : injecter un état prélevé là où le calcul se fait | ✅ la **porte de la greffe** (648 s) : l'injection est **branchée**, la greffe porte tout le contenu | mesuré |
| A7.2 | **Une couche exécutée ailleurs** : la même sortie, un autre nœud | ✅ | le **relais ne change pas un chiffre** (`porte-topologie`, 92 s, 42.5477) ; le coût du flux : **1 608 octets/flux**, **0,25 Mbit/s**, latence ≤ 20 ms — [`rapport-mode4-lot-listes.md`](../reports/rapport-mode4-lot-listes.md) |
| A7.3 | **La grappe intra-couche** : un sous-ensemble de neurones, pas une frontière de couche | ✅ mesuré | le **top-1024** (21 % des 4 864 neurones FFN) rend la **même perplexité** (30,7286 à quatre décimales) ; 64 et 256 l'effondrent — la grappe a une **taille minimale** mesurable — [`reports/rapport-grappe-intra-couche.md`](../reports/rapport-grappe-intra-couche.md) |
| A7.4 | **La grappe déportée** : le flux ne transporte que les valeurs utiles | ✅ mesuré | le format v2 (masque + valeurs) coûte **4,22× moins** que le dense (1 704 o contre 7 196 o) et la porte du flux rend **60,8135 / 60,8135** — les mêmes chiffres, [`reports/rapport-grappe-deportee.md`](../reports/rapport-grappe-deportee.md) |
| A7.17 | **Cache KV int8 sur 64 jetons** | ✅ **positive** | 64/64 jetons greedy identiques (accord 1,0) avec `CacheInt8` stocké ; un prompt, pas d'échantillonnage |
| A7.16 | **Cache KV int8 stocké** | ✅ **positive** | `CacheInt8` remplace `DynamicCache` : 32/32 jetons greedy identiques (accord 1,0) ; le cache réellement stocké est int8, pas un hook |
| A7.15 | **64 jetons avec K/V int8** | ✅ **positive** | 64/64 jetons greedy identiques (accord 1,0), texte identique ; un prompt, pas d'échantillonnage |
| A7.14 | **Génération avec K/V int8** | ✅ **positive** | 16 jetons greedy **identiques** (16/16, accord 1,0) avec K/V int8 par canal sur 24 couches ; un prompt, pas d'échantillonnage |
| A7.13 | **K/V int8 sur 512 jetons** | ✅ **positive** | 511 jetons, 24 couches : PPL **4,6979356** base et int8, Δ **0,0** ; un seul texte, pas de génération |
| A7.12 | **PPL avec K/V int8** | ✅ **positive** | hooks sur les 24 couches de Qwen 0.5B : PPL **2,6792016** → **2,6792004**, Δ **−1,17e-6** ; 85 jetons, 5 textes courts ; pas de génération |
| A7.11 | **Attention avec KV int8** | ✅ **stable** | diff max **0,0154**, moyenne **0,0048**, **argmax 97,66 %**, corrélation **0,99998**, ratio **0,266** ; Q aléatoire, pas de modèle |
| A7.10 | **Cache KV int8** | ⚠️ **compromis** | **17 420 o** contre **65 548** (ratio **0,266**), **272 o/jeton**, **25,5 Mio** contre **96,0 Mio** pour 4 096 jetons ; diff max **0,0155**, moyenne **0,0050** ; fidélité modèle non mesurée |
| A7.9 | **Cache KV à distance** | ❌ **négatif** | une couche **1 024 o/jeton** (0,25× le hidden) ; **24 couches 24 580 o/jeton**, **96 Mio pour 4 096 jetons** (6× le hidden) ; fidélité exacte, 0,179 ms loopback ; il faut garder le KV côté serveur ou le quantifier |
| A7.8 | **Hidden int8 par canal** | ⚠️ **compromis** | ratio **36–39 %**, argmax **1,0**, diff max **0,5–1,7**, KL **~1e-3** ; lossy mais décision stable ; PPL non mesurée ; 896 échelles f32 (3,6 ko/requête) |
| A7.7 | **Hidden int8** | ❌ **négatif** | int8 par tenseur : argmax **0**, diff **26,6**, KL **10,2** ; par jeton : argmax **0,83–0,93**, diff **17,0**, KL **0,12–0,37** ; volume **34,6 %** du dense mais fidélité insuffisante ; bf16 reste meilleur (argmax 1,0, 2× moins que f32) |
| A7.6 | **Une couche à distance** | ✅ **mesuré** | Qwen 0.5B couche 12 dans un second processus : logits **identiques au bit près** 3/3, **ΔPPL +0** ; RTT **4,052 ms**, **4 105 o/jeton**, **3 987,6 jetons/s** ; sparse/dense **1,027×** (hidden réel dense, pas de gain) |
| A7.5b | **Seuil réseau du sparse** | ✅ **mesuré** | dense **7 416 o**, sparse **1 672 o** (4,44×) ; encodage **0,254 vs 0,688 ms**, décodage **0,369 vs 0,490 ms** ; gain **1,94× à 0 ms**, **1,006× à 100 ms** ; seuil **−0,60 ms** : sparse gagne toujours sur ce lien |
| A7.5 | **La grappe sur le réseau** : transporter le flux v2 entre deux processus, mesurer latence, octets et fidélité | ✅ **mesuré** | **4,44×** moins d'octets (1 672 o contre 7 416), fidélité **1 792/1 792**, messages **5/5** identiques, **0,125 ms** loopback ; contrôle dense — [`reports/rapport-grappe-reseau.md`](../reports/rapport-grappe-reseau.md) |

**Prochaine action** : aucune sur A7.5 — le transport sparse est **mesuré** (4,44×, fidélité 100 %, 0,125 ms loopback). La suite (exécution d'une couche à distance, WAN) reste **hors plan**.

### A8 — L'ordonnanceur place **et** perte

La leçon de la tête (le 4 bits « qui tient » coûte +10 % de PPL) : **un ordonnanceur qui ne porte que la place prend
une mauvaise décision.**

| # | chantier | état | critère de succès |
|---|---|---|---|
| A8.1 | **La règle de place** | ✅ `placement::choisir`, 4 tests | mesuré |
| A8.3 | **La règle branchée** : la précision du KV choisie par le budget de perte | ✅ mesuré — **opt-in** (`DRAVE_PERTE_MAX`) | la règle rend **exactement** le choix de la main (`12-23:8`) : **30,7286** des deux côtés, contre 30,7660 en f32 — [`reports/rapport-regle-placement-perte.md`](../reports/rapport-regle-placement-perte.md) |
| A8.2 | **Le terme de perte** : chaque précision a son coût mesuré (PPL) | ✅ `choisir_avec_perte` + **3 tests** | l'int8 tardif (+0,03 %) passe un budget de **1 %**, l'int4 tardif (+2,7 %) exige **5 %**, la tête 4 bits (+10 %) est **refusée** à 5 %, l'int4 global (+364 %) jamais — la leçon de la tête est devenue une règle |

**Prochaine action** : aucune sur A8 — la règle est **branchée en opt-in** (A8.3) ; pour la passer **par défaut**, il
faut d'abord **épingler les portes** qui mesurent une PPL (elles ont bougé le 24/10 : `porte-coupe` est tombée). La
place reste à appliquer aux experts (A6.2, bloqué faute de MoE local).

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
| B2.8 | **Le raisonnement naturel à l'échelle** : XNLI au 14 B/32 B, et un corpus naturel plus dur | ✅ mesuré | **DACCORD +26,9, GQNLI +56,7, XNLI +35,9** de marge (1,5 B, contrôles au hasard) ; **chaque modèle a son pic tardif** : 1,5 B **0,810** (c. 22), 3 B **0,865** (c. 30), 14 B **0,7189/0,8701** (c. 30) — et sur XNLI, **la sonde sature dès le 1,5 B** : 0,7256 (c. 22), 0,7269 (3 B), 0,7189 (14 B), **dix fois la taille pour +0,001** — et à **50 %**, le **32 B** mène (0,5997) devant le 1,5 B (0,5783), le 3 B (0,5020) et le **14 B dernier** (0,4833) : **la profondeur décide autant que le modèle**, et le 14 B balaie **+0,147** entre son pire et son meilleur point — [`reports/rapport-32b-couche-confondant.md`](../reports/rapport-32b-couche-confondant.md) |

**Prochaine action** : aucune — le plan résiste, l'échelle est tracée (les pics), DiaBLa est mesuré.

### B3 — Le plan et la dynamique

| # | chantier | état | critère de succès |
|---|---|---|---|
| B3.1 | **L'état de plan** : le contexte joint des 4 phrases | ✅ | 0,43 (FR→FR) ; c'est la meilleure représentation du plan |
| B3.2 | **La résistance** : ponts, bilinguisme, contraste, récurrence | ✅ | tous échouent (0,25-0,39) ; l'apparent transfert est un effet côté cible |
| B3.3 | **La dynamique** : un état qui porte plusieurs pas | ✅ mesuré | le pas n'existe pas au-delà du contexte (mesures 113-115) ; le plan s'entraîne (119-124) |

**Prochaine action** : aucune — la ligne est **définitivement** close (B2.6 testé, mesure 168).

### B4 — Les opérateurs abstraits

La carte de l'étage 2 est faite : l'état **porte** le raisonnement (la sonde), le pont l'**aligne** (0,87), le plan
**résiste**. Ce qui manque, ce sont les **opérations** : les transformations abstraites (composer, inférer, ordonner)
que la carte ne mesure pas encore.

| # | chantier | état | critère de succès |
|---|---|---|---|
| B4.1 | **L'opérateur** : une transformation de l'état, indépendante de la langue et de la surface | ✅ mesuré — **négatif** | la **négation** n'est **pas** portée par l'état : le flip est à **0,4148** (sous le hasard 0,5) et la garde à **0,5852** (au-dessus) — la sonde lit la **relation de surface**, pas l'**opération** ; la référence (0,8103) tient — [`reports/rapport-operateur-negation.md`](../reports/rapport-operateur-negation.md) |
| B4.2 | **L'opérateur appris** : la négation entraînée dans l'état (comme le plan, mesure 119), pas lue par la sonde | ✅ mesuré — **apprenable, pas transférable** | une sonde **réentraînée** sur le nié lit la relation basculée à **0,7042** (hasard 0,5, contrôle 0,4952) ; mais la sonde de l'original ne lit pas le nié (0,4148) et réciproquement (0,3312) — **l'opérateur est une géométrie locale, pas une direction** — [`reports/rapport-operateur-negation.md`](../reports/rapport-operateur-negation.md) |
| B4.3 | **Les deux opérations dans un seul opérateur** : l'identité et la négation, apprises ensemble | ✅ mesuré — **elles coexistent** | le mélange (l'original + le nié) lit l'original à **0,7749** et le nié à **0,6977** (contrôle 0,4791) : l'opérateur est un **sous-espace** (une relation + une polarité), pas une direction — [`reports/rapport-operateur-negation.md`](../reports/rapport-operateur-negation.md) |
| B4.4 | **La composition** : le nié du nié revient-il à l'original ? | ✅ mesuré — **négatif** | le double nié n'est pas lu comme l'original : **0,5691** (contre 0,8103 de référence), et le mélange est **sous** le hasard (0,3601) — l'opérateur n'est pas une **algèbre**, les opérations sont des sous-espaces appris (B4.3) — [`reports/rapport-operateur-negation.md`](../reports/rapport-operateur-negation.md) |
| B4.5 | **La composition apprise** : le nié du nié entraîné comme une tâche | ✅ mesuré — **apprenable, faiblement** | le triple (original, nié, double nié) lit le double à **0,6174** (contrôle 0,4598) — **+0,117** sur le hasard, contre 0,8103 pour l'original : *rien ne se compose gratuitement* — [`reports/rapport-operateur-negation.md`](../reports/rapport-operateur-negation.md) |
| B4.6 | **Le LoRA de la négation** : apprendre l'opération dans les poids (le rang 8, les 723 paires niées) | ✅ mesuré — **négatif** | l'entraînement converge (la perte 0,0022) et le modèle reste intact (0,8135), mais le `flip_sonde` est **0,2283** = `1 − garde_sonde` (0,7717) : *le LoRA apprend à **inverser** la lecture, pas à transférer l'opération* — [`reports/rapport-operateur-negation.md`](../reports/rapport-operateur-negation.md) |

**Bilan de B4** : les opérations sont des **géométries apprises**, locales, non compositionnelles gratuitement —
et la composition s'apprend à un coût (0,6174). *L'état porte les opérations, mais il ne les calcule pas.*

**Prochaine action** : aucune sur B4 — la ligne est close ; les suites sont **hors du plan** (le LoRA qui modifie
l'état, mesure 119 ; une troisième opération). Le plan a repris à **A8.3** (branché), **A7.3** (mesuré), puis
**B5/B6** (mesurés), puis **B7/B8** (mesurés), puis **B9** (le banc externe).

### B5 — La sémantique des jeux symboliques

La carte de l'étage 2 est faite, les opérateurs sont mesurés ; il manquait une **entrée-sortie symbolique** qui ne
dépende ni de la langue ni de la notation. B5 est cette entrée-sortie, appliquée à cinq jeux (morpion, échecs,
dames, go, cartes) et à deux langues. Le concept est dans [`docs/jeux-symboliques.md`](jeux-symboliques.md) ; la
fiche et le JSON dans [`reports/rapport-jeux-symboliques.md`](../reports/rapport-jeux-symboliques.md).

| # | chantier | état | critère de succès |
|---|---|---|---|
| B5.1 | **Le contrat RSN-jeu** : jeu + nature + corps canonique + annotation hors empreinte, encodage binaire `RSNB` | ✅ mesuré | 41 objets distincts ; **128,93 o** de JSON → **71,10 o** de binaire (**0,5515**), aller-retour identique |
| B5.2 | **Les cinq niveaux (0→4) et les cinq codecs** | ✅ mesuré | **112 items**, couverture **50 / 77 / 105 / 110 / 112** (niveaux 0→4) ; **33/33** paires invariantes au niveau 4 ; **0 collision** |
| B5.3 | **La restitution et le bruit** | ✅ mesuré | restitution **112/112**, perturbation **112/112**, lexique permuté **112 → 92** (20 items perdus), étiquettes mélangées **7/112** |
| B5.4 | **La détection et les ambiguïtés** | ✅ mesuré | **100/112** sans indice de jeu ; les **12** échecs sont des surfaces ambiguës **nommées** (`A1`, `E4`, `d4`, `b6-c5`…) |

**Prochaine action** : aucune — la ligne est mesurée ; les suites (corpus externe, détection avec contexte,
autres langues) sont **hors du plan**.

### B6 — La logique dans la pensée

L'étage 2 ne lit que la RSN ; B6 est sa **logique de jeu**, mesurée par les règles d'abord, par la force ensuite,
et par l'**invariance de la décision** enfin.

| # | chantier | état | critère de succès |
|---|---|---|---|
| B6.1 | **Les règles et le perft** | ✅ mesuré | échecs : six positions, profondeur 4, **197 281 · 4 085 603 · 43 238 · 422 333 · 2 103 487 · 3 894 594** (exacts) ; dames : **7 · 49 · 302 · 1 469 · 7 361 · 36 768** ; go : capture, suicide, ko, score |
| B6.2 | **La recherche** | ✅ mesuré | morpion : valeur **0**, partie parfaite **nulle**, exact contre hasard **200/200** sans défaite ; échecs : **3/3** mats en un (statique **1/3**) ; dames : **20/20** contre le joueur sans recherche |
| B6.3 | **La politique des cartes** | ✅ mesuré | **79,7 %** contre le hasard (1 000 donnes), **0 / 52 000** coup illégal ; hasard 48,6 %, sans partenaire 75,6 %, sans atout 73,5 % |
| B6.4 | **L'invariance de la pensée** | ✅ mesuré | **5/5** jeux donnent la même décision sur deux surfaces du même état ; contrôle négatif **5/5** (le trait change l'empreinte) |

**Prochaine action** : aucune — la ligne est mesurée. Le MCTS du go est un **négatif nommé** à 60 playouts
(**1/3** contre le hasard) : les règles sont justes, la force n'est pas établie ; un budget plus grand et un
corpus externe sont hors plan.

### B7 — Les langues : le même sens dans 71 langues

La couche de B5 était FR/EN. B7 ajoute un **lexique multilingue** (35 concepts, **71 langues**, **1 433
couples**) construit depuis Wikidata (CC0) et un **corpus multilingue** de **449 surfaces**. La notation (FEN,
SAN, UCI, GTP, SGF, binaire) reste **indépendante de la langue** : c'est le recours de toutes les langues sans
libellé.

| # | chantier | état | critère de succès |
|---|---|---|---|
| B7.1 | **Le lexique multilingue** (pièces, rangs, enseignes, noms de jeux, notions de maîtres) | ✅ mesuré | **71 langues**, **35 concepts**, **1 433 couples** ; **32 langues fortes** (pièces N/P + un rang et une enseigne) ; source Wikidata, licences CC0 |
| B7.2 | **Le corpus multilingue** (pièce + cases, rang + enseigne, nom du jeu + coordonnée) | ✅ mesuré | **449/449** au niveau 4 ; **66 langues** avec des items, **62** avec des items forts ; **11/11** paires invariantes |
| B7.3 | **Les contrôles** : permutation des libellés, notation, détection | ✅ mesuré | permutation **12/275** items forts restants (**4,4 %**) ; notation **5 112/5 112** (72 items × 71 langues) ; détection des jeux **315/315** |
| B7.4 | **La langue détectée** et les limites | ✅ mesuré | langue exacte **343/449** (**76,4 %**) ; libellés Wikidata = des **lemmes**, pas des formes fléchies ; **5 langues** sans item (`ky`, `lo`, `mt`, `si`, `yo`) ; `e4`/`E4` restent **ambiguës** échecs/go |

**Prochaine action** : aucune — la ligne est mesurée. Les suites (grammaire multilingue, formes fléchies, corpus
externe) sont **hors du plan** ; la notation est le recours qui n'attend pas ces suites.

### B8 — Les maîtres : les principes encodés, mesurés, et leurs négatifs

Les livres des maîtres sont une **connaissance** : B8 en tire **17 principes**, **9 sources** (sept ouvrages du
domaine public — Lasker 1925, Capablanca 1921, Nimzowitsch 1925, Tarrasch 1931, Payne 1756, Smith 1908,
Cavendish 1884 —, les proverbes traditionnels du go et le morpion résolu), un **livre de 28 positions**, trois
**parties** du domaine public (Opéra 1858, Immortelle 1851, Toujours verte 1852), et les encode dans la pensée.

| # | chantier | état | critère de succès |
|---|---|---|---|
| B8.1 | **La base des maîtres** | ✅ mesuré | **17 principes**, **9 sources**, **3 parties** validées jusqu'au mat, **28 positions** de livre |
| B8.2 | **Échecs** : évaluation, livre, accord avec les maîtres | ✅ mesuré — **positif et négatif** | premier coup **d4** (sans : **Nc3**) ; livre **10/10** ; mats **3/3** ; accord avec le coup du maître **42/101** avec les principes contre **41/101** sans — **+1, non significatif** |
| B8.3 | **Dames** : évaluation augmentée contre l'évaluation du dépôt | ✅ mesuré — **positif avec biais nommé** | **10 victoires, 10 nulles, 0 défaite** en 20 parties (même profondeur 4) ; la base, elle, ne gagne **aucune** des 20 parties avec les Blancs (**0 victoire**) — le biais de couleur est **nommé** |
| B8.4 | **Go** : les proverbes comme prior de MCTS | ✅ mesuré — **positif sur 9×9, sans effet sur 5×5** | 9×9 : **10/10** coups de 3e/4e ligne avec le prior contre **3/10** sans ; 5×5 : premier coup **10/10** des deux côtés ; capture **10/10** des deux côtés |
| B8.5 | **Cartes** : la politique du whist contre la politique du dépôt | ✅ mesuré — **négatif** | **44,7 %** contre la base (51,0 %) ; contre le hasard **78,5 %** contre **82,4 %** ; l'ablation (sans honneur **43,5 %**, sans seconde **45,7 %**, sans troisième **46,5 %**) ne rattrape pas la base |

**Prochaine action** : aucune — la ligne est mesurée. Les suites (un moteur plus profond, un corpus de parties
plus large, une politique de cartes avec enchères) sont **hors du plan** ; le négatif des cartes est **nommé**,
pas maquillé.

**Bilan de B7/B8** : les langues **ne dépendent plus de deux lexiques** ; la notation reste le recours
universel ; les principes **changent l'ouverture** (d4), **tiennent le livre** (10/10), **gagnent au go 9×9**
(10/10 contre 3/10) et **ne perdent pas aux dames** (0 défaite), mais ils **ne battent pas la base aux cartes**
(44,7 % contre 51,0 %) et **ne rapprochent pas du coup du maître** (42 contre 41 sur 101). *La connaissance des
livres n'est pas la force ; elle est une entrée, et elle se mesure comme telle.*

### B9 — Le banc externe et l'élève natif

Le langage sort des GPU : **DeepSeek** sert de **professeur** (traduction, jugements, génération,
évaluation), et les 2 × RTX 5000 restent au **modèle natif** `route` / `drave-core` et aux mesures
**boîte blanche**. La licence autorise explicitement la **distillation** et l'**entraînement** à
partir des sorties. Concept : [`docs/llm-externe.md`](llm-externe.md) ; fiche :
[`reports/rapport-deepseek.md`](../reports/rapport-deepseek.md).

| # | chantier | état | critère de succès |
|---|---|---|---|
| B9.1 | **L'adaptateur et la porte** : API compatible OpenAI, cache, dry-run, clé par fichier | ✅ mesuré | **20 tests** hors réseau ; `porte-deepseek` **verte** ; appel live de contrôle : **16 jetons**, **0,868 s** |
| B9.2 | **Le corpus professeur** : 310 puis 610 et 910 prompts publics | ✅ mesuré | **310/310** (chrF **82,82** contre **15,64**), puis **610/610** (20 langues) et **910/910** (30 langues), 0 échec ; détail : [`rapport-deepseek.md`](../reports/rapport-deepseek.md) |
| B9.3 | **La distillation** : `route` sur GPU, contrôle par permutation | ✅ **mesuré — transition 9,23–9,96 M** | 4,04 M négatif ; 9,23 M transitoire ; **31,63 M / 610 ex. : 4,40 % (3/3, meilleur écart)** ; fenêtre **3,71 % / 1,29 % / −0,49 %** ; 910/30 négatif ; masque sans gain. Détail : [`rapport-deepseek.md`](../reports/rapport-deepseek.md). |
| B9.4 | **La répartition** : DeepSeek pour le langage, GPU pour le natif | ✅ décidé | `route` **4,04 M** et **22,54 M** sur **`cuda`** ; le grand modèle fait **1,18 M** poids lus/jeton/couche, 500 pas en **52–56 s** ; Qwen 0.5B ne reste que **référence blanche** |

**Prochaine action** : **augmenter la capacité avec les données** (31,63 M / 610 fait **4,40 %**, contre 0,27 % à
310 : la capacité ne paie qu'avec les données ; le 910/30 ne paie pas ; le 1 000 pas efface l'effet : la **fenêtre
d'entraînement** et le **budget de modèle** sont les facteurs), **resserrer la transition
9,23–9,96 M**, et **porter le masque dans le trainer** (même boucle, warmup/clipping) pour une
comparaison propre. Le signe change avec la **capacité**, pas avec la quantité de données (310
exemples dans les deux cas) ; c'est le résultat à expliquer. Le contrôle par permutation et le
plancher chrF sont les garde-fous. Aucune ligne n'est bloquée : la clé est dans l'environnement,
les GPU sont libres.

**Bilan de B9** : le langage **sort des GPU** et le professeur est **fort là où la langue est
proche** (espagnol 99,28, russe 98,86, français 96,58, italien 92,87, allemand 90,50) ; il est
**faible en hindi et en swahili** (58,45 / 54,83). La distillation natif a une **transition entre
9,23 M et 9,96 M** : **négative à 4,04 M**, **transitoire à 9,23 M** (1 graine/3), **positive 3/3
à 9,96 M, 10,70 M, 16,02 M et 22,54 M** (1,76 %, 1,65 %, 1,92 %, 1,74 %). Le **masque calibré** à
4,04 M est **quasi égal** (2,7335 contre 2,7340, 0,02 %) : pas de gain établi. Le transfert existe,
mais il demande de la capacité ; le seuil est une **transition**, pas une marche.


### B10 — le protocole sémantique natif

| ligne | objet | état | mesure |
|---|---|---|---|
| B10.1 | **L'encodeur** : rejouer les articles UDHR en 10 langues, `z` partagé, contrastive + adversaire, NVLink | ✅ **mesuré** | rappel parallèle **0,426** contre **0,167** de hasard ; mélangé **0,172** ; sonde de langue **0,100** ; 250 pas, 31,63 M, 2 GPU NVLink |
| B10.2 | **Le décodeur sens → texte** : `z` gelé ou joint, décodeur séparé | ❌ **négatif** | chrF reconstruction **14,0**, traduction **5,4** contre un plancher **38,8** (référence tronquée ; **12,7 / 5,3 contre 39,6** en référence complète) ; diagnostic sous le plancher ; ablations : `z` 512 → rappel **0,278**, préfixe 64 → **12,4/6,7**, joint → **12,9/8,4**, 8 unités linéaires → rappel **0,237** |
| B10.3 | **Le raisonnement** sur `z` gelé | ⏳ **non branché** | attend un décodeur au-dessus du plancher |

**Ce que le premier passage a appris** : l'alignement seul collapse ; l'all-gather doit être différentiable ;
les gradients du décodeur écrasent l'encodeur (étages séparés) ; les articles du lot global doivent être
distincts. Prochaine action : décodeur à attention croisée, 20–30 articles, 3 graines, puis raisonnement.
Détail : [`rapport-semantique.md`](../reports/rapport-semantique.md).

### B11 — la base d'universaux typés

| ligne | objet | état | mesure |
|---|---|---|---|
| B11.1 | **Le schéma fixe** : 15 champs, 502 classes, one-hot déterministe ; NSM/Jackendoff/Sens-Texte/logique comme sources | ✅ **défini** | note [`semantique-universaux.md`](semantique-universaux.md) ; code [`universaux.py`](../tools/semantique/universaux.py) |
| B11.2 | **Le parseur natif typé** : `route` 31,63 M, pooling moyen, 15 têtes | ⚠️ **partiel** | réel seul : **48,3 % train / 0 % validation** (surapprentissage) ; synthétique : **45,1 %** de code exact sur surfaces réelles, `jeu` **83,1 %**, `de`/`vers` **90,0 / 89,4 %** |
| B11.3 | **Le codec classique** : lecture surface → RSN | ✅ **mesuré** | **79/79** et **449/449** RSN exactes (100 %) ; **surface originale 33/79** |
| B11.4 | **Données synthétiques / distillation du codec** | ✅ **mesuré** | 10 556 surfaces synthétiques, 71 langues, **aucune surface réelle** à l'entraînement ; test réel **45,1 %** ; **invariance 7,4 %** |
| B11.5 | **Cohérence inter-langues du natif** | ⚠️ **partiel** | normalisation lexicale : **55,7 %** de code exact et **37,0 %** d'invariance (contre 45,1 / 7,4) ; consistance softmax **38,3 %** (0) et adversaire **39,6 %** (0) restent deux négatifs |
| B11.6 | **Codec + contexte, mémoire** | ✅ **mesuré** | codec **528/528** avec contexte (100 %) ; sans contexte **374/528** (70,8 %) ; mémoire 470 cibles, **pas un modèle** ; natif normalisé 55,7 % |
| B11.7 | **Natif contextuel** | ⚠️ **partiel** | contexte **suffixé** : **59,8 %** de code exact et **40,7 %** d'invariance ; contexte **préfixé** : 0,4 % / 88,9 % (collapse) ; le codec reste à 100 % |
| B11.8 | **Contexte séparé** | ❌ **sans gain** | vecteur de contexte 512 + MLP : **59,1 %** / **40,7 %**, contre **59,8 %** / **40,7 %** pour le suffixe ; le verrou est ailleurs |
| B11.9 | **Restitution du code** | ✅ **mesuré** | **79/79** et **449/449** rendus, **aller-retour RSN 100 %** ; **surface originale 33/79** ; sans décodeur neuronal |
| B11.10 | **Cartes et ambiguïtés** | ⏳ **suivant** | `carte` **69,3 %** ; symbole du morpion, chemin des dames ; le codec lit 100 % |
| B11.11 | **Bilan** | ✅ **écrit** | [`bilan-b11.md`](../reports/bilan-b11.md) : objectif **non atteint**, raisonnement **non branché** |

**Bilan de B11** : le **contrat typé** est clair et déterministe, et le **codec classique** est aujourd'hui
le meilleur bloc linguistique du corpus (lecture exacte 100 %). Le **parseur natif typé** surapprend : il
faut de la **donnée synthétique/compositionnelle** ou de la **distillation**, pas seulement une tête fixe.
Détail : [`rapport-universaux.md`](../reports/rapport-universaux.md).

### B12 — les modules cerveau-langage M1–M9

| ligne | objet | état | mesure |
|---|---|---|---|
| B12.1 | **Bus + hub M1** | ✅ **mesuré** | **528/528** exact avec contexte ; sans contexte **70,8 %** ; canonique **100 %** ; invariance **100 %** ; 1 584 événements |
| B12.2 | **M2 voies ventrales/dorsales** | ⚠️ **vu + règles** | `aug-formes` : `de` **95,2 %, inédit 13/20**, `chemin_0` **88,1 %, 6/14** ; `aug-pos` : `vers` **95,4 %, 13,3/20**, promotions **0/3→3/3**, mais `de` 92,2 % et `chemin` 86,7 % ; `point` **97,14 % = majorité** ; double dissociation sur les vus |
| B12.3 | **M3 mémoire de travail** | ❌ **tautologique** | span 12/12 même avec des codes aléatoires ; n-back contrôle construit sur 5 items de même code ; interférence purement FIFO |
| B12.4 | **M4 mémoire épisodique** | ❌ **lookup** | 528 items, **29 codes** ; rappel 1,0 = doublons ; 0/6 codes non stockés, 0/10 complétions exactes, 0/7 valeurs inédites |
| B12.5 | **M5 prédictif** | ⚠️ **contexte** | sans contexte : action 97,5 % = majoritaire ; avec plateau : source **3,224→2,598 nat** (+5,9 pts), cible **3,520→3,109** (+3,6 pts), morpion **2,20→1,52 = oracle** ; échecs cible faible |
| B12.6 | **M6 gating** | ⚠️ **sélecteur** | tâche sens/langue 94,95 % (base 50 %) mais conflit **0**, commutation **0** ; langue seule 88,6 % ; pas un contrôle exécutif |
| B12.7 | **M7 neuromodulation** | ❌ **nul** | 3,64 % = plafond 16/439 ; LFU +23,1 pts sur les répétés, nouveauté −19,6, incertitude −38,7, récompense −53,3 ; aucun signal ne bat FIFO |
| B12.8 | **M8 sommeil** | ❌ **marginal** | 96,48 % de champs mais exact **65,1 %**, baseline par jeu **96,10 %** ; leave-one-code-out exact **0 % par construction**, non nuls 63,5 % ; coordonnées 0 % |
| B12.9 | **M9 lésion** | ✅ **table** | contexte **29,2 %** ; M2 ventrale **24,7 %** ; M2 dorsale **2,1 %** ; M7 **13,7 %** ; M3 **0** ; M4 **0** ; M5 **1,1 %** ; M6 **30 %** ; M8 **0** |
| B12.10 | **Pipeline M1 → M4 → M8** | ⚠️ **intégration** | **528/528**, 7 prototypes, 96,33 % de complétion — tautologique : M4 ne généralise pas, M8 est la marginale |
| B26.1 | **M6 conflit** | ❌ **nul** | réplication d'A6 : exact **94,95 %** (792 cas), conflit **0**, commutation **0** ; c'est un **sélecteur** sans compétition, pas un contrôle exécutif ; pas de réponse motrice |
| B25.1 | **M8 rejeu** | ❌ **négatif** | 23/6 codes, 442/86 épisodes ; M8 exact **0**, champs **74,6 %** ; **rejeu 0** ; **hybride 0** ; le prototype ne compose pas un code neuf |
| B24.1 | **Routeur confiance** | ⚠️ **partiel** | typo **56,2→63,7 %** (+7,5) mais espaces **41,8→34,2 %** (−7,5) ; round-trip M1 ne détecte que **31 %** des typos ; oracle **79,45 %** sur la typo ; aucun score ne domine |
| B23.1 | **Routeur M1→M2** | ⚠️ **partiel** | original **100 %**, casse **99,3 %**, phrase **92,5 %** = M1 ; espaces **41,8 %** vs M1 **11,6 %** ; typo **56,2 %** < M2 **68,3 %** (collision de lexique) ; pas un oracle |
| B22.1 | **M2 et les typos** | ⚠️ **niche robuste** | M1 suppression **32,8 %**, substitution **27,1 %**, insertion **44,5 %**, transposition **24,1 %** ; M2 `de` **72,6 / 62,3 / 66,4 / 70,5 %**, `vers` **80,1 / 65,8 / 70,6 / 73,3 %** ; avantage +21,9 à +46,5 pts |
| B21.1 | **M9 par dose** | ✅ **dose** | M3 span **0/4/8/12/12** (linéaire, tautologique) ; M5 ordre 0/1/2 **13,81/15,70/18,06 %** (+4,25 pts, surprise +0,012 nat) ; sham **nul** ; double lésion **non additive** |
| B19.1 | **M2 secours hors codec** | ⚠️ **typos seulement** | M1 original **100 %**, casse **98,7 %**, phrase **86,6 %** ; M1 espaces **34,8 %**, typo **36,6 %** ; M2 typo **71,2 / 76,7**, espaces **41,8 / 45,2**, phrase **0 / 0,7** ; niche réelle, pas un secours général |
| B18.1 | **Restitution canonique** | ✅ **involution** | **528/528** rendus, **528/528** relus, **0** échec ; codec bidirectionnel exact, pas un décodeur neuronal (B10 reste négatif) |
| B17.1 | **M7-bis dans la chaîne** | ✅ **filtre** | LFU **9,28 %** suffixe surface vs FIFO **5,03 %** ; suffixe code **74,69 vs 71,70 %** ; M8 couverture **70,75 %**, exact sur couverts **100 %** (lookup), généralisation **0 %** |
| B16.1 | **M7-bis LFU** | ✅ **fréquence** | LFU vs FIFO : **+23,1 pts** répétés (30/30), **+4,25** suffixe surface, **+8,7** nouveaux utiles ; LFU+récence **= LFU** ; contexte **−8,5** suffixe, **−42,9** répétés ; ce n'est pas de la neuromodulation |
| B14.1 | **M2 dans la chaîne** | ❌ **rameau** | M1 **100 %** (`de`/`vers`), M2 **93,4 / 93,6 %** ; **aucun étage ne consomme M2** ; M5 plateau **18,70 % vs 12,60 %** ; M6 **94,32 / 94,95 %** ; M2 n'ajoute rien et dégrade de **−6,6 / −6,4 pts** ; le « M5 M1-lésé 28,03 % » est une **couverture 51,4 %**, pas un gain |
| B15.1 | **M1 sur 66 langues** | ✅ **invariance** | **528/528** avec contexte, **70,8 %** sans ; **26/26** variantes et **15/15** interlangues invariantes ; contrôle permuté attendu **0 %**, donneur **90 %** ; 66/71 langues ; baseline surface **71,8 %** |
| B13.1 | **Chaîne sémantique M1→M5→M6→M8** | ✅ **intégration** | M1 **528/528** ; M5 contexte **18,7 % vs 12,6 %** (surprise 2,423 vs 3,112) ; M6 **94,3 %** / switch **94,95 %** ; M8 **57,95 %** exact sur épisodes stockés (borne haute) ; M9 M1 **70,8 %** |
| B12.11 | **Corrections** | ✅ **écrit** | [`rapport-cerveau-corrections.md`](../reports/rapport-cerveau-corrections.md) : seul M1 est solide ; M2 vu seulement ; M3–M8 structurels/négatifs |

**Bilan B12** : seul **M1** est solide ; **M2** est vu seulement, **M3/M4** sont structurels, **M5** gagne
seulement avec le contexte, **M6** est un sélecteur, **M7** est une fréquence (pas une neuromodulation),
**M8** est marginal, **M9** est une table de privations. Le prototype est un **échafaudage mesuré**, pas un
cerveau du langage. Détail : [`rapport-cerveau-corrections.md`](../reports/rapport-cerveau-corrections.md).


---

## La suite de C3 — les modules par famille

Le chantier C3 (la restitution) est **mesuré** : 85,1 % de fragments exacts à une langue, puis 30 % → 4,4 % → 0,4 % →
0,6 % à 1/10/50/448 langues — **la restitution exacte meurt entre 1 et 10 langues**. La suite est de donner à chaque
**famille** son module, au lieu d'un module unique.

| # | chantier | état | critère de succès |
|---|---|---|---|
| C3.2a | **Le découpage par famille** : `tools/decoupage_familles.py` groupe les articles par `famille` (la généalogie : 441 langues, 55 familles) | ✅ **fait** | **28 familles**, 362 langues, **12 383 articles** découpés ; **9 familles de 9 langues ou plus** (Indo-European 98, Atlantic-Congo 74, Austronesian 35, Sino-Tibetan 17, Turkic 14, Afro-Asiatic 12, Quechuan 11, Mayan 9, Uralic 9) — `data/udhr/familles/<slug>.jsonl` + `index.json` (reproductible, `data/` est gitignoré) |
| C3.2b | **Un module par famille** : `tools/lora_recopie.py --famille <famille>` | ✅ **mesuré** | l'indo-européen (98 langues, 3 688 articles) recopie à **100 %** après 200 pas (0 % avant), le **contrôle 0 %** — [`reports/rapport-modules-famille.md`](../reports/rapport-modules-famille.md) |
| C3.2e | **Sous-familles des autres familles** | ✅ **mesuré** | uralic côtier **100 %** contre **46,7 %** pour la famille ; benue-congo **88 %** contre 94 ; austronesian est **60,3 %** contre 61 ; afro-asiatic ouest **53,5 %** contre 60,2 ; le découpage explique l'uralic, pas les autres — [`reports/rapport-sous-familles-autres.md`](../reports/rapport-sous-familles-autres.md) |
| C3.2d | **Sous-familles IE** | ✅ **mesuré** | découpage glottolog : indo-iranien **100 %**, baltique **95,3**, italique **87,6**, celtique **79,9**, germanique **54,6** ; l'IE entier à **14,7 %** est un **effet de composition**, pas une incapacité — [`reports/rapport-ie-sous-familles.md`](../reports/rapport-ie-sous-familles.md) |
| C3.2c | **La comparaison à la courbe** : le module par famille doit **casser la chute entre 1 et 10 langues** | ✅ **mesuré — 9 familles** | **7/9 > 30 %**, moyenne **69,5 %**, médiane **64,4 %**, contrôle **≤ 0,5 %** : indo-européen **14,7 %**, atlantic-congo **94,0**, quechuan **88,2**, mayan **64,4**, afro-asiatic **60,2**, austronesian **61,0**, uralic **46,7**, turkic **96,1**, sino-tibetan **100** — [`reports/rapport-familles-9.md`](../reports/rapport-familles-9.md) |

**Prochaine action** : aucune — la ligne C3.2 est **close** (les trois sous-lignes mesurées). La suite éventuelle
(la courbe sur les **9 familles** au lieu de 5, et comprendre l'**indo-européen** à 14,7 %) est **hors du plan**.

**Ce qui pourrait le rendre faux** : le corpus UDHR est **parallèle** (les mêmes articles dans toutes les langues) —
un module par famille peut apprendre la **surface** de la famille sans apprendre la restitution. Le contrôle : la
**même mesure** à 1 langue (le 85,1 % de référence) doit tenir par famille, et la courbe doit être **comparée** à
celle du module unique. Le `sino-tibetan` partait de **40,5 %** avant l'entraînement (le modèle connaissait déjà une
partie des textes) : sa progression (59,5 points) est **moins parlante** que les autres — c'est écrit dans la fiche.

> **Suites B19–B23.** **B23** : un score de confiance M1, car la collision de lexique laisse la typo
> à 56,2 % ; **B22** : typos réelles et secours conditionnel ; **B21** : reproduire la dose M5 sur une
> autre lésion ; **B19** : la niche est la typo et les espaces, pas la phrase.

## L'ordre du jour (carpe diem)

L'ordre est **la valeur / le coût**, pas la date. **Les lignes non bloquées sont mesurées au fil des
phases** (dernière mise à jour : 27/10) :

1. ~~B2.6 — le plan multi-tâches~~ **fait** (168 : 0,364, la ligne plan est close).
2. ~~A2.5 — le top-k GPU~~ **fait** (le noyau fusionné, le seuil 131 072 mesuré).
3. ~~A4.3 — le diff par couche dans la porte~~ **fait** (`porte-diff-couche`, 18 s, **verte dans la passe**).
4. ~~A1.5 / A5.3 — la décision par couche~~ **fait** (l'int8 sur les tardives +0,03 %, le 4 bits +2,7 % — un curseur).
5. ~~A2.6 — l'ordonnanceur~~ **partiel** (la règle `choisir`, 4 tests ; le KV l'applique ; la tête essayée puis **revertée**).
6. ~~A6.1 / A6.3~~ **faits et négatifs** (les produits +0,0045 ; aucun neurone mort sur 116 736).
7. ~~B2.7 / B2.8 / B1.6~~ **faits** (le 32 B, les pics par modèle, DiaBLa).
8. **Ce qui reste, nommé** : le pic du 32 B (**OOM**, la VRAM de 16 Go ; la cause est documentée), la prose scientifique
   (**corpus absent**), A6.2 (**pas de MoE local**), A3.4 (**compte Colab**), A5.4 (**FPGA**).
9. **La nouvelle phase (24/10)** : **A7 la grappe déportée** (la plus proche de la vision), **B4 les opérateurs
   abstraits** (le plus neuf scientifiquement), **A8 l'ordonnanceur place et perte** (le plus ingénieur).
10. ~~B5 / B6 — la sémantique et la logique des jeux symboliques~~ **faites** (112 items, **100 %** au niveau 4,
    **33/33** paires invariantes, perft échecs/dames, mats, dames 20/20, politique 79,7 %).
11. **B10–B12 (27/10)** : le protocole sémantique (encodeur **0,426** ; décodeur **négatif**), la base typée
    (codec **100 %**, natif **59,8 / 40,7**, **surface 33/79**), les modules cerveau-langage (M1 **528/528**,
    M2 vu seulement, M8 marginal, M5/M6/M7 négatifs) — **corrigé** ; les suites sont **B10.3** (bloqué par le
    décodeur) et **B12.10** (intégration).
12. **A7.5 — la grappe sur le réseau** : le format sparse est mesuré (4,22×) ; le **transport réel** (latence,
    octets, fidélité entre processus) ne l'est pas. C'est le prochain chantier à valeur, aligné sur la vision
    du bus réparti.

## La file « jamais en attente »

Quand une ligne est bloquée (corpus, compte, matériel), on prend la suivante — et le travail ne s'arrête pas :

- **fait, mesuré** : B2.6, B2.7, B2.8, A2.5, A2.6 (la règle ; la tête **revertée**), A4.3, A1.5, A5.3, A6.1, A6.3 ;
- **la nouvelle phase (faite, mesurée)** : A7 (le relais, la grappe intra-couche à 21 %, la grappe déportée à
  4,22×), B4 (les **six** mesures de l'opérateur : pas une direction, apprenable, un sous-espace, pas une algèbre, une
  composition apprise, le LoRA qui **inverse**), A8 (la règle place+perte, **branchée en opt-in**) ;
- **la phase jeux (faite, mesurée)** : B5 (112 items, **100 %** au niveau 4, **33/33** paires, **0 collision**), B6
  (perft échecs/dames, morpion exact, **3/3** mats, dames **20/20**, politique **79,7 %**, invariance **5/5**), B7
  (**71 langues**, 449/449, 11/11 paires, permutation 12/275) et B8 (livre 10/10, go 9×9 **10/10** contre 3/10,
  dames 10 victoires/10 nulles/0 défaite, cartes **44,7 %** contre 51,0 % — négatif nommé), B9 (DeepSeek
  **310/310**, chrF **82,82** contre **15,64** de plancher ; distillation native **non établie** à 310 exemples,
  **2,7510** mélangé contre **2,7709** aligné — le contrôle bat l'aligné) ;
- **la phase sémantique et cerveau (faite, mesurée)** : B10 (encodeur **0,426** ; décodeur **négatif**
  14,0/5,4 contre 38,8 en référence tronquée ; 12,7/5,3 contre 39,6 en référence complète), B11 (codec
  **100 %**, natif **59,8 / 40,7**, **surface 33/79**), B12 (M1 **528/528**, M2 **98,6 / 93,2**, M8
  **96,48 %**, M5/M6/M7 **négatifs**) ; les suites sont **B10.3** et **B12.10** ;
- **bloqué, nommé** : B1.5 (le corpus d'articles), A3.4 (le compte Colab), A5.4 (le FPGA), A6.2 (pas de MoE
  local) — B1.6 est **fait** (DiaBLa, références indépendantes) ;
- **clos** : B3 (le plan résiste), la falaise du raisonnement (erratum 6), la répartition réseau (le transport est
  fidèle).

## Ce qui est bloqué, et par quoi

| ligne | bloque par | ce qu'il faudrait |
|---|---|---|
| B1.5 prose scientifique | aucun corpus parallèle humain d'articles FR/EN | un corpus (revue, actes, manuel) traduit par des humains |
| A3.4 Colab | le compte et le runtime Colab | un compte (la recette est dans `docs/archive/colab-reparti.md`) |
| A5.4 FPGA | l'accès au matériel Stratix V | la carte (le design existe) |
| A6.2 MoE local | aucun MoE local ne tient dans 16 Go de VRAM | un MoE qui tient, ou une machine plus grande |

> **Journal des décisions** : l'historique (30/09 → 27/10) est dans
> [`journal/2026-10-27_decisions-roadmap.md`](../journal/2026-10-27_decisions-roadmap.md).
