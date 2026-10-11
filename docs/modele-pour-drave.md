# Quel modèle pour Drave ? — évaluer un modèle *ad hoc*, pas le moteur

> 9 octobre 2026. Ce document sépare deux choses que les rapports mélangeaient
> jusqu'ici : **ce que le moteur Drave fait payer** (un coût précis, mesurable) et
> **ce qu'un modèle devrait être** pour que ce coût soit minimal. La campagne
> la campagne `reports/campagne-benefices/` (une fiche par expérience) a mesuré le moteur *sur des modèles faits pour
> d'autres architectures* ; ici on cherche la forme du modèle qui lui est propre —
> y compris inédite.

---

## 0. Moteur contre modèle : qui paie quoi

Les rapports de la campagne mesurent **le moteur** — mais toujours *sur des modèles
faits pour d'autres architectures*. La distinction n'est pas rhétorique : les mêmes
chiffres disent deux choses différentes selon la colonne où on les lit.

| mesure de la campagne | ce qu'elle établit sur le **MOTEUR** | ce qu'elle établit sur le **MODÈLE** |
|---|---|---|
| densité d'activation **71 %**, identique sur quatre corpus (§ 10 ter) | le chemin par listes n'est pas rentable au-dessus de ~22-25 % de densité — c'est une propriété du moteur, mesurée sur son banc | un modèle dense ordinaire **n'est pas un client** pour Drave : sa parcimonie ne dépend pas de la tâche, elle n'existe pas |
| k-WTA appris (§ 5 ter) | le moteur exécute un top-k **sans changer le calcul** (logits identiques au bit près, § 22) | la sparsité doit être **apprise**, et le taux d'exécution fait partie de la spécification du modèle |
| routage d'experts (§ 7, § 5 bis) | le moteur ouvre k experts sur 128 et n'en lit que les poids… **mais n'a pas de noyau de listes pour eux** (Q4_0, Q8 refusé) | le routage seul ne passe pas l'échelle (+10 % à dim 512) ; **la distillation le rattrape** (−5,2 %) |
| poids creux `--keep` (§ 6 de ce document) | le moteur compte les **non-nuls par ligne** : élaguer réduit les paires sans toucher aux activations | à 50 % de poids gardés la qualité **ne bouge pas** ; à 25 % elle s'effondre — et ces 50 % étaient *imposés*, pas appris |
| export Q4_0 contre Q8 (§ 5 bis) | la porte de correction tient dans les deux cas (corrélation 0,9998) : le moteur est fidèle | **le format fait partie du modèle** : deux fois plus d'entraînement améliore le fp32 (1,8237) et dégrade l'exporté (5,3845) — la pénalité de quantification passe de +0,445 à +0,605 bit/octet |
| lecture mmap **8,6 Mo/s** sur disque dur contre 243 Mo/s en séquentiel (§ 12 bis) | le moteur lit par défauts de page : sur un plateau, une page aléatoire coûte ~5 ms | un modèle dont les poids actifs sont **contigus** transformerait cette lecture en séquentiel — **×28 disponibles par un choix de disposition**, pas de code de noyau |
| découpage à deux nœuds : **3,4 ms par jeton et par ms de RTT** (§ 8 bis) | le transport est exact à toute latence (perplexité inchangée à 50 ms) | répartir ne paie que si le calcul local dépasse 3,4 ms × RTT : **la taille du modèle décide**, pas le réseau |
| tête restreinte : borne **×1,12** sur gpt-oss (§ 13) | le moteur sait restreindre une tête et garantir la sortie | le gain dépend du **rapport tête/corps** du modèle — donc d'un choix d'architecture (vocabulaire) |

**La règle qui sort de ce tableau** : quand une mesure est décevante, il faut savoir
*de qui* elle est décevante. Le chemin par listes est lent sur un modèle dense —
c'est le modèle qui n'est pas fait pour lui. Le décodage spéculatif ne paie pas sur
une cible qui tient en RAM — c'est la cible qui est trop rapide. Les experts ne
passent pas par les listes — **là, c'est le moteur qui manque** (noyau Q8 absent).

---

## 1. Le coût, formalisé

Dans Drave, une passe avant ne paie pas « des paramètres », elle paie des
**paires (poids × activation)** :

    paires = Σ_{projections} Σ_{i ∈ activations vivantes}  (poids non nuls de la ligne i)

Trois conséquences, toutes vérifiées par la campagne :

| levier | effet sur les paires | où c'est mesuré |
|---|---|---|
| **sparsité d'activation** (entrées vivantes) | facteur direct | § 19, § 5 ter |
| **sparsité de poids** (non-nuls par ligne) | facteur direct | § 6 de ce document (mesuré le 9/10) |
| **routage** (quelles lignes existent) | facteur direct, par expert | § 7 |

Et deux coûts qui ne sont **pas** des paires :

- **le croisement push/pull** : au-dessus de ~22-25 % de densité, le chemin par
  listes coûte *plus cher* que le produit scalaire dense, même à paires égales
  (mesuré : ×0,02 à vide, ×1,54 à 50 %, ×3,19 à densité 1). **Un modèle ad hoc doit
  vivre sous ce seuil** ;
- **la lecture** : les paires doivent venir du disque. Mesuré le 9/10 : **8,6 Mo/s
  en mmap sur disque dur contre 243 Mo/s en séquentiel** (`dd` direct) — soit ÷28.
  Sur NVMe, 140-300 Mo/s (÷5 à ÷11). **La disposition des poids est donc un
  paramètre de conception du modèle**, pas un détail d'implémentation.

**Ce que le moteur ne fait PAS payer** : le nombre de couches (chaque couche ne paie
que ses paires), la taille du vocabulaire *d'entrée* (l'embedding est une lecture de
ligne), la VRAM (les projections peuvent rester sur le CPU), la RAM (mmap).

---

## 2. Ce que la campagne a déjà établi, et qui contraint le dessin

| fait mesuré | conséquence pour le modèle |
|---|---|
| la densité d'activation d'un modèle dense est **71 %**, identique sur prose, français, code et 399 langues (§ 10 ter) | un modèle ordinaire **ne peut pas** bénéficier des listes : sa parcimonie ne dépend pas de la tâche, elle n'existe pas |
| à 25 % gardés, un modèle ordinaire perd **+118 %** de perplexité ; le même entraîné avec k-WTA **s'améliore** (§ 5 ter) | la sparsité doit être **apprise**, et le taux d'exécution fait partie de la spécification |
| la distillation rattrape le **routage** (−13,8 % à dim 512) mais **pas** la parcimonie (−0,3 %) (§ 5 bis, 5 ter) | les deux leviers traitent des handicaps distincts : ne pas les confondre dans un dessin |
| 4 experts sur 128 (3,1 %), déséquilibre ×3,90 (§ 7) | le routage est un levier **fort** sur les paires — mais voir § 3 ci-dessous |
| la couche de sortie de gpt-oss pèse **12 %** des paires par jeton (§ 13) | la tête compte, et un **petit vocabulaire** la rend négligeable |
| le lot **ne divise pas** les lectures sur un MoE (§ 14 bis) | la sparsité par experts et le lot se contredisent : un dessin ad hoc doit choisir |

---

## 3. Les candidats, et ce que chacun vaut

Sept familles ont été examinées. Pour chacune : le gain **attendu** sur les paires,
l'état de la **mesure**, et ce qui manque.

### A. Modèle à activations creuses apprises (k-WTA) — **mesuré, gagnant**

Entraîner avec un k-WTA sur l'entrée de toutes les couches linéaires, exécuter avec
`--act-topk` au même taux.

- **Mesuré** : à 25 % gardés, perplexité **5,1719 contre 10,8758** au témoin à taux
  égal (−52 %) ; à dim 512, **4,9649 contre 6,0503** en dense ; paires ÷4.
- **Prix** : néant à son taux d'entraînement (le modèle creux fait *mieux* que
  dense) ; hors de son régime, 0,4 à 1,4 point de perplexité.
- **Statut** : recette établie, reproductible (`--kwta` + `--act-topk`).

### B. Modèle à POIDS creux — **mesuré le 9/10, et c'est le levier oublié**

Le chemin par listes compte les **non-nuls par ligne** : élaguer les poids réduit
les paires *sans toucher aux activations*. Mesuré sur `m8_d512_kwta25` (128 jetons,
`DRAVE_SANS_EMPRUNT=1` pour comparer la même arithmétique) :

| poids gardés (par ligne) | activations | perplexité | **paires (événements)** |
|---|---:|---:|---:|
| 100 % | 100 % | 4,2831 | 1 585 574 447 |
| 100 % | 25 % | **3,9152** | 398 967 618 |
| **50 %** | **25 %** | **3,9139** | **201 308 279** |
| 25 % | 25 % | 13,0141 | 100 757 395 |

**Deux résultats.** 1) Les deux leviers **se multiplient** : 1 586 M → 399 M → 201 M
→ 101 M de paires, soit **÷7,9** pour la combinaison 50 %/25 %. 2) À 50 % de poids
gardés, **la perplexité ne bouge pas** (3,9139 contre 3,9152) — l'élagage imposé
coûte zéro à ce taux. À 25 % il s'effondre (+232 %) : la limite est entre les deux.

**ET C'EST APPRIS, MAINTENANT — mesuré le 9/10 à 11 h 32.** `m11_d384_kwta25_elag50`
= `kwta025` (activations à 25 %, apprises) **+ élagage appris à 50 %** des poids :

| dim 384 | aucune parcimonie | 50 % act. | **25 % act.** |
|---|---|---|---|
| `kwta025` seul | 6,4282 · 335,3 M | 5,8131 · 168,3 M | 5,1719 · 84,2 M |
| **+ poids élagués appris** | **6,0422 · 165,9 M** | **5,6842 · 84,7 M** | **5,1866 · 42,2 M** |

**÷2 lectures à chaque point, qualité inchangée** (+0,3 % à 25 % d'activations,
−6,0 % en dense). Cumulé, le modèle lit **huit fois moins** que le témoin sans
parcimonie, pour une perplexité comparable : c'est la vérification de l'hypothèse
« les deux facteurs se multiplient », cette fois avec les deux **appris**.

### C. Routage d'experts — **mesuré : fort sur les paires, aveugle aux événements**

- **Mesuré** : 4 experts sur 128 (3,1 %) ; −2,6 % à dim 256, −2,9 % à 384 à lecture
  égale, **+10 % à dim 512** — et la distillation rattrape (−5,2 % vs le dense).
- **La limite, et elle est structurelle** : les experts sont écrits en **Q4_0**,
  format sans noyau de listes, et le chargeur **refuse Q8_0** pour les experts. Un
  modèle routé **économise des experts, pas des événements** : à l'intérieur des
  experts, tout est lu.
- **Conséquence pour un dessin ad hoc** : A et B doivent s'appliquer **dans** les
  experts, ce qui demande le noyau Q8 par expert — sinon le routage et la parcimonie
  ne se rencontrent jamais.

### D. Disposition « par événements » des poids — **inédit, motivé par une mesure**

Sur disque dur, le moteur lit à **8,6 Mo/s** là où le disque donne 243 Mo/s : la
faute aux défauts de page *aléatoires*. Un modèle dont les poids actifs d'une même
décision sont **contigus** (experts en blocs, lignes regroupées par fréquence
d'activation, en-têtes au début) transformerait cette lecture en séquentiel.

- **Gain attendu** : jusqu'à **×28** sur le débit de lecture dans la niche « plus
  gros que la RAM » — c'est-à-dire la différence entre 90 minutes et 3 minutes pour
  une passe gpt-oss.
- **Ce qui manque** : un exporteur qui réordonne, et rien d'autre — le moteur lit
  par pointeur et n'impose aucun ordre. **C'est le candidat le moins coûteux à
  tester et le plus spécifique à Drave.**

### E. Tête et vocabulaire — **mesuré, et c'est un choix de modèle**

La couche de sortie est lue **en entier** à chaque jeton (0,58 G de poids pour
gpt-oss, 12 % des paires). Un vocabulaire de 32 k au lieu de 201 k divise ce poste
par 6 ; un modèle **byte-level** (vocabulaire 256, comme ceux entraînés ici) le rend
négligeable. Les modèles de la campagne sont byte-level pour cette raison.

- **Mesuré** : tête restreinte ×1,36-1,42 (0,5 B) ; sur gpt-oss la borne est ×1,12
  et l'essentiel est ailleurs (experts).
- **Conséquence** : à qualité égale, **un petit vocabulaire est un avantage
  structurel** en Drave — l'inverse de l'usage courant, où le vocabulaire est
  choisi pour la compression du texte.

### F. Attention : ce que le contexte coûte vraiment

Les paires d'attention croissent avec la longueur (0,15 M/jeton à 128 jetons mais
910 M/jeton sur le 30B à 512 jetons, § 14 bis). Un dessin ad hoc doit **borner** ce
poste : fenêtre glissante (le moteur l'implémente pour gpt-oss), cache compressé
partagé (V4), ou état récurrent (KDA de Kimi).

- **Mesuré** : la mémoire tient jusqu'à **12 288 jetons** (18/18, § 9) ; le KV int8
  coûte +1,5 à +3,0 % (§ 0 bis) ; le KV paginé fait 0,03 Go au lieu de 25,77 Go à
  1 M.
- **Ce qui manque** : un modèle entraîné ici **avec** fenêtre glissante ou état
  récurrent, pour mesurer ce que la borne coûte en qualité *quand elle est apprise*.

### G. Le lot et le routage se contredisent — **mesuré**

Sur un MoE lu du disque, augmenter le lot **ne divise pas** les lectures : l'union
des experts touchés par une passe sature (§ 14 bis). Un modèle ad hoc destiné au
disque doit donc soit **router peu** (peu d'experts, très creusés), soit **accepter
de lire tout le jeu chaud** — les deux ne se cumulent pas.

### H. Routage par PROFONDEUR (chaque jeton ne traverse que k couches) — **inédit, et Drave l'exécute déjà**

Le levier le plus violent sur les paires n'est pas de réduire les activations d'une
couche, c'est de **ne pas exécuter la couche du tout** : une couche sautée vaut
zéro paire. Le moteur sait déjà exécuter une plage de couches (`--couches`, nœud
partiel, découpage à deux nœuds) et son protocole de flux transporte une liste
d'activations, pas un tenseur — donc **sauter une couche est une décision locale,
pas une reconstruction**.

- **Gain attendu** : proportionnel au taux de saut — un jeton qui traverse 2 des 4
  couches divise ses paires par 2, et se cumule avec A et B.
- **Ce qui manque** : un modèle entraîné ainsi (mixture-of-depths) **et** un routeur
  de profondeur bon marché — c'est un projet d'entraînement, pas de moteur.
- **Pourquoi c'est spécifiquement Drave** : dans une architecture dense classique,
  sauter une couche casse le graphe et impose des masques ; dans une architecture
  événementielle, c'est simplement « ne rien envoyer ».
- **MESURÉ le 10/10 : la borne est ≈ 9,6 % des paires, et le facteur limitant est le
  chemin court, pas le routeur.** Deux chemins relus **hors du moteur** (chaîne
  vérifiée *contre* le moteur : 0,013 % et 0,006 %) sur 3 925 jetons jamais vus :
  l'état de **24** couches lu par la tête du modèle (perplexité **16,5611**,
  justesse **44,97 %**) contre l'état de **16** couches lu par un adaptateur entraîné
  (**1 343,48** · **20,33 %**). **Un oracle parfait ne pourrait sortir tôt que
  `28,76 %` des jetons sans changer une seule décision** — soit **≈ 9,6 % des paires**
  (un tiers des couches sur 29 % des jetons), et il faudrait qu'il soit parfait. Un
  routeur réel ne dispose que de la **confiance** du chemin court : **aucun seuil
  n'atteint la qualité du chemin long** (le meilleur, à 5,1 % de jetons sortis, rend
  `44,74 %` contre `44,97 %`). Mais le seuil **sélectionne** (+2,87 points sur le
  hasard à part égale) et, sur les 5 % de jetons les plus sûrs, l'écart court/long
  tombe de **24,6 à 4,5 points** — c'est ce chiffre qu'un modèle entraîné pour la
  sortie anticipée devrait **renverser**. Détail :
  [`rapport-design-H-profondeur-routee.md`](../reports/rapport-design-H-profondeur-routee.md),
  porte `tools/porte-profondeur-routee.sh`.
- **Ce qui manque, précisé par la mesure** : non pas un routeur — la confiance suffit
  à sélectionner — mais un **chemin court entraîné pour ça** : un adaptateur posé
  après coup ne remplace pas huit couches.

### I. Budget d'ÉVÉNEMENTS appris, au lieu d'un k-WTA uniforme — **inédit, et mesurable aujourd'hui**

Le k-WTA de A coupe **le même taux partout** (25 % sur chaque couche, chaque
neurone). Or les couches ne se valent pas : la campagne a mesuré, projection par
projection, que `o` et `down` tolèrent 30 % gardés sans perdre 17 % de perplexité
là où `gate` et `up` s'effondrent (+101 %, +75 %, § 19 bis).

- **L'idée** : entraîner avec une **contrainte globale** (un budget d'événements par
  jeton, ex. 25 % du total) au lieu d'un taux local, et laisser le modèle répartir —
  une couche qui a besoin de toutes ses activations les garde, une autre tombe à
  5 %. La contrainte est un lagrangien sur le nombre de non-zéros attendus, donc
  dérivable par un seuil appris.
- **Gain attendu** : à budget égal, la perplexité d'un modèle qui *choisit* où être
  creux doit être meilleure que celle d'un modèle creusé uniformément.
- **PREMIER ESSAI, ET IL ÉCHOUE** (9/10, `m5_d384_dense_q8`, 127 jetons, mêmes
  conditions) : à événements comparables, une allocation **ciblée d'après le tableau
  de sensibilité du § 19 bis** (`o` et `down` à 30 %, le reste à 100 % → 689 M
  d'événements, soit l'équivalent d'un taux uniforme de 77 %) donne **3,9469** de
  perplexité, contre **3,6998** pour un taux uniforme de 70 % (629 M) — et **3,7169**
  sans aucune parcimonie (898 M).

  | allocation (même fenêtre) | événements | perplexité |
  |---|---:|---:|
  | aucune | 897 753 869 | 3,7169 |
  | **uniforme 70 %** | 629 364 528 | **3,6998** |
  | uniforme 50 % | 449 348 892 | **3,6521** |
  | ciblée (o/down 30 %) | 688 874 158 | 3,9469 |

  **La sensibilité par projection n'est pas transposable d'un modèle à l'autre** :
  le tableau du § 19 bis avait été mesuré sur Qwen2.5-0.5B, et sur notre modèle
  c'est l'inverse qui se produit. Le principe « répartir le budget » n'est donc pas
  réfuté — mais il doit être **appris**, pas déduit d'un autre modèle.
- **Ce qui manque** : un seuil appris par projection dans le harnais. C'est un
  changement **local** de l'entraînement (`--kwta` existe déjà), et la mesure se
  fait avec les outils de la campagne.

### J. Quantification adaptée au chemin par LISTES — **pratique, et chiffré**

Le chemin par listes stocke en **int8 + listes de rangs** : 15,88 bits par poids
mesurés, contre 8,00 pour la forme dense (§ 21 du rapport de campagne). Un modèle
entraîné pour cette grille (quantification-aware) garderait sa qualité à 8 bits
**tout en** ayant des listes d'événements — alors qu'aujourd'hui la forme 8 bits
coûte 2× le stockage de la forme 4 bits, laquelle n'a **aucun** noyau de listes.

- **Gain attendu** : le chemin événementiel sans le doublement de taille, donc la
  possibilité de l'employer sur un modèle qui ne tient pas en RAM.
- **PREUVE QUE CE N'EST PAS UN DÉTAIL** (9/10) : le même routé 512 entraîné 80 000
  pas au lieu de 40 000 est **meilleur en fp32** (1,8237 contre 1,8843 bits/octet)
  et **pire après export Q4_0** (perplexité moteur 5,3845 contre 5,0255). Le prix de
  la quantification est passé de **+0,445 à +0,605 bit/octet (+36 %)** — il croît
  avec l'entraînement. La porte de correction tenue sur ce modèle (corrélation
  0,9998) écarte l'erreur du moteur : c'est bien le modèle quantifié qui est moins
  bon.
- **Ce qui manque** : un entraînement avec bruit de quantification (le moteur a déjà
  la grille, `--abits`, et son banc d'encodages). **Et une limite de format** : les
  experts d'un MoE ne peuvent être ni Q8_0 ni F16 (le chargeur les refuse), donc un
  modèle routé ne peut pas même être *testé* en 8 bits aujourd'hui.

---

## 4. Le classement, et le modèle qui en sort

Par **gain sur les paires** × **certitude de la mesure** × **coût de mise en œuvre** :

| rang | levier | gain mesuré sur les paires | coût |
|---|---|---|---|
| 1 | **activations creuses apprises** (A) | **÷4** à 25 % gardés, qualité conservée | fait (`--kwta`, `--act-topk`) |
| 2 | **poids creux** (B) | **÷2** à 50 % gardés, qualité conservée | fait à l'exécution (`--keep`) ; **à apprendre** |
| 3 | **disposition par événements** (D) | jusqu'à **÷28 sur le débit de lecture** (disque dur) | exporteur à écrire |
| 4 | **routage** (C) | ÷32 sur les experts non lus | fait, mais **aveugle aux événements** sans noyau Q8 |
| 5 | **petit vocabulaire / tête** (E) | 12 % des paires chez gpt-oss | fait (byte-level) |
| 6 | **borne d'attention** (F) | dépend du contexte | partiel |
| 7 | **routage par profondeur** (H) | ÷ par le taux de saut, **cumulable** | modèle à entraîner |
| 8 | **budget d'événements appris** (I) | à budget égal, meilleure qualité | seuil par projection à coder |
| 9 | **quantification-aware pour les listes** (J) | événements sans doublement de taille | entraînement bruité |

**Le modèle ad hoc que ces mesures dessinent** — et il n'existe pas :

> Un modèle **byte-level** (tête négligeable), **entraîné creux sur les deux axes à
> la fois** (k-WTA à ~25 % sur les activations *et* élagage appris à ~50 % sur les
> poids par ligne), **routé** avec peu d'experts très creusés, dont les poids sont
> **rangés par groupes d'événements** pour que le disque lise en séquentiel, et dont
> l'attention est **bornée par une fenêtre apprise**.

Les mesures de ce document en donnent les trois premiers étages : ÷4 (activations),
÷2 (poids, et ils se multiplient : **÷7,9 mesuré**), et un facteur de lecture qui
peut aller jusqu'à ×28 sur disque dur. Les trois derniers demandent, dans l'ordre :
un noyau Q8 par expert, un exporteur qui réordonne, et un entraînement à fenêtre.

---

## 4 bis. Nos modèles à décharges fonctionnent-ils en GPU ? Non — et il y a deux raisons distinctes

Question posée le 9 octobre. Réponse vérifiée dans le code **et** par la mesure.

**Ce que le moteur sait déporter** (`gpu.rs`, 1 573 lignes) : les projections Q8_0
(`charger_proj` → noyau dense int8), le cache KV (`kv_*`), les scores d'attention et
leur top-k (`attn_scores`, `attn_topk_*`), et les experts MXFP4 / Q4_K
(`charger_mxfp4`, `charger_q4k`).

**Trois conditions pour qu'une projection parte sur le GPU** (model.rs, `Proj::load`) :

| condition | valeur | nos modèles |
|---|---|---|
| source **Q8_0** (forme dense 8 bits) | obligatoire | ✅ (FFN exportée en Q8) |
| **aucun élagage** (`keep >= 1.0`) | obligatoire | ❌ pour tout modèle à poids creux |
| taille **≥ 8 Mio** par projection | `SEUIL_GPU` | ❌ **0,45 à 0,80 Mio** — dix fois trop petits |

**Donc : aucun de nos modèles à décharges n'utilise le GPU.** Mesuré à l'instant :
`DRAVE_GPU=1` sur `m8_d512_kwta25` rend exactement la même perplexité (4,5656) et le
même débit, en annonçant au passage que le périphérique demandé est indisponible —
puis il retombe proprement sur le CPU, sans changer un chiffre.

**Et la seconde raison est plus profonde que la taille** : le noyau GPU est un
**produit dense** — `proj(m, x: &[i32], sx)` reçoit le **vecteur d'activation complet**,
zéros compris, et calcule le produit entier. Or tout l'avantage du chemin par listes
est de **ne pas lire les poids nuls**. Déporter une projection creuse sur ce noyau
**détruirait exactement ce que la parcimonie apporte** : on gagnerait la bande passante
de la carte et on perdrait le saut des lectures.

**Pour qu'un modèle à décharges aille sur GPU, il faudrait un noyau de LISTES sur la
carte** : n'envoyer que les indices non nuls et ne lire que les lignes de poids
correspondantes (un *gather* sur le périphérique, ou un format creux compressé). Ça
n'existe pas — c'est le pendant GPU exact du manque déjà consigné côté experts
(« le chargeur d'experts refuse Q8_0 »).

**Ce que le GPU sert déjà, en revanche** : sur **gpt-oss-120B**, les projections
d'attention sont en Q8_0 et pèsent **12,5 Mio** — au-dessus du seuil — donc elles
*sont* déportées dès `DRAVE_GPU=1`. Sur le 30B (Q4_K partout), aucune projection n'a
de forme dense 8 bits : rien à déporter. Le seuil de 8 Mio, lui, n'est pas arbitraire :
il vient de la mesure — 60 µs d'aller-retour contre 123 µs de calcul CPU pour la FFN
du 0,5 B (le CPU gagne), 187 contre 216 µs pour l'attention de gpt-oss (le GPU gagne).

---

## 5. Les expériences à faire, par ordre de rendement

1. ~~**Élagage appris** (B)~~ — **FAIT** (9/10, 11 h 32) : ÷2 lectures à qualité
   égale (+0,3 % à 25 % d'activations, −6,0 % en dense), et les deux axes se
   multiplient comme prévu. Il reste à descendre plus bas (25 % de poids) et à
   croiser avec la structure innée (chaîne `jour6`).
2. **Noyau Q8 par expert** (C) — sans lui, un modèle « routé et creux » ne peut pas
   exister ; c'est aussi la seule façon de mesurer ce que le routage vaut *en
   événements*. **Et son pendant GPU** : le noyau de listes sur la carte, sans lequel
   un modèle à décharges ne peut pas être déporté sans perdre ce que la parcimonie
   apporte (§ 4 bis).
3. **Disposition par événements** (D) — réordonner les tenseurs à l'export et
   re-mesurer le débit de lecture à froid. Le moteur n'a rien à changer.
4. **Fenêtre apprise** (F) — entraîner avec fenêtre glissante et comparer à
   contexte plein, à mémoire égale.

**Ce que ce document ne dit pas** : aucun de ces dessins n'a été entraîné *en
entier*. Le classement est fait de mesures isolées, pas d'un modèle complet — et
c'est écrit à chaque ligne du § 3.
