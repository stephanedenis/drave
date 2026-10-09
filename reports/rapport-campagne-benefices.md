# Campagne 24 h — où Drave est à son meilleur, tâche par tâche

> 08/10 21 h → 09/10. Rapport **vivant** : il est mis à jour au fil des étapes.
> File : `tools/campagne-benefices.sh`. Journaux bruts : `/tmp/campagne24/`.
> Plan : `docs/campagne-benefices.md`.
>
> Règle de lecture : chaque chiffre porte ses conditions (corpus, tokenizer,
> charge de fond). La charge a oscillé entre 3 et 18 pendant la campagne
> (entraînements en parallèle) — les mesures **déterministes** (perplexité,
> comptes d'événements) n'en dépendent pas, les **temps** oui, et c'est écrit.

---

## 0. Le piège qui a failli tout fausser

`data/wikitext2_test.txt.ids` **vient d'un autre tokenizer** que Qwen2.5 :
`201,438,10498…` là où le modèle produit `198,284,8397…`. Sur les mêmes octets :

| identifiants | perplexité (256 jetons, ctx 512) |
|---|---:|
| ceux du dépôt | **7 710,72** |
| tokenisés par le modèle | **17,43** |

Un facteur 442. La règle est désormais dans le script : **chaque modèle tokenise
son propre corpus**. C'est aussi la première chose à vérifier avant de croire une
perplexité publiée quelque part.

---

## 0 bis. Le verdict, famille par famille

Le tableau qui répond à la question posée, chaque ligne portant sa mesure. ⏳ =
file encore en cours.

| famille de tâches | verdict | mesure |
|---|---|---|
| **langage** (perplexité) | ✅ tourne — **le routage gagne aux petites échelles, et PERD à dim 512** | à lecture égale : dim 256 dense **5,0155** → routé **4,8858** (−2,6 %) → **distillé 4,7642 (−5,0 %)** · dim 384 : 5,0108 → 4,8646 (−2,9 %) · **dim 512 : 4,5686 → 5,0255 (+10 %)**, 12,8 M paires/jeton des deux côtés (§ 5 bis) |
| **génération / latence** | ✅ mesuré | TTFT **27,9 ms**, **29,0 tok/s** (0,5 B) · 114,6 ms, 7,1 tok/s (1,5 B) |
| **contexte long — la mémoire** | ✅ **elle tient** | **12 aiguilles sur 12** retrouvées, de 512 à **4 096 jetons**, à 10 %, 50 % et 90 % de profondeur |
| **contexte long — le coût** | ✅ réglable | KV int8 : +1,5 % (512 j.) à +3,0 % (8 192 j.) · paginé : **0,03 Go au lieu de 25,77 Go** à 1 M |
| **préremplissage par lots** | ✅ ×1,4 en RAM, ⚠️ disque non testé | 0,5 B, 512 jetons : **16,8 → 23,7 tok/s** et PPL **identique** (13,1368 → 13,1359) · sur le 30B le lot n'a lu que le **cache de pages** (10,9 Go à froid, 0 ensuite) |
| **code** | ✅ mesuré, décalage de tâche | codestral-22B : **117,91** de PPL sur de la prose = **1,797 bit/octet**, contre **0,983** pour un 0,5 B — un 22 B 1,8× **pire** qu'un 0,5 B hors de sa tâche |
| **raisonnement** | ✅ mesuré, contre-intuitif | r1-distill-1.5B : **1,326 bit/octet**, **2,7× pire** que le 0,5 B (0,983) |
| **MoE / routage d'experts** | ✅ mesuré | 4 experts sur 128 (3,1 %) · déséquilibre **×3,90** · **847 octets** par jeton à router |
| **multilingue (399 langues)** | ✅ mesuré, et c'est le point faible du modèle | **3,227 bit/octet** contre 0,951 en prose — **3,4× pire** · densité **identique** (71 %) · seuil absolu : PPL **×11**, le k-WTA tient (§ 10 ter) |
| **sémantique multilingue** | ✅ le résultat publié **survit** au correctif d'échelle | pic de séparation à la **couche 13** (+0,0391) sur 398 langues, bande 10-15 — et l'ancien lecteur donnait +0,0349 au même endroit |
| **parcimonie imposée** | ✅ reproduit, et nuancé | à −30 % d'événements : seuil **+69 %** de PPL, k-WTA **+4 %** (facteur 17) · en dense, **aucune lecture économisée** |
| **sortie contrainte** | ✅ **gagne par construction** | **×1,36-1,42** de débit *et* garantie que la sortie appartient à l'ensemble autorisé |
| **modèle plus gros que la RAM** | ✅ **démontré** | V4-Flash **365,7 Go sur 125 Go de RAM** : **37,6 Go résidents**, 37,7 Go lus, 266 s pour 16 jetons · gpt-oss (63 Go) : passe de 256 jetons **non finie en 90 min** |
| **répartition à deux nœuds** | ✅ **porte tenue** | écart **0,0000 %** et flux **0,00e0** — sur le modèle dense, routé **et distillé** |
| **embeddings / recherche** | ❌ **manque** | `bge-m3` lisible en en-tête, **inexécutable** (ni encodeur bidirectionnel ni pooling) |
| **décodage spéculatif** | ❌ manque, et chiffré **par le moteur** | paire alignée (HF) : 3,35 jetons sur 8 acceptés, **×1,20** · paire mal appariée (moteur) : **0,88 sur 8, ×0,70** — un brouillon rejeté coûte plus qu'il ne rapporte (§ 1 et 1 bis) |
| **routage à l'échelle** | ❌ **le gain s'inverse à dim 512** | val : −3,5 % (256) → −1,4 % (384) → **+1,4 % (512)** · moteur : 4,5686 → 5,0255 ; même recette, mêmes 40 000 pas, **12,8 M paires/jeton des deux côtés** |
| **fidélité listes ↔ dense** | ✅ **exacte, démontrée** | logits identiques **au bit près** (`cmp` sur 4 254 216 octets) et mêmes jetons gloutons, à encodage de poids égal ; ×0,02 à ×3,19 selon la densité |

**En une phrase** : Drave gagne **par construction** sur les sorties contraintes,
**par sa structure** quand le modèle est creux — mais seulement aux petites
échelles : le routage entraîné rend −2,6 % à dim 256 et −2,9 % à dim 384, puis
**+10 % (il perd) à dim 512**, à lecture égale (12,8 M paires/jeton des deux côtés,
§ 5 bis) — **par ses circonstances** sur les modèles plus gros que la RAM, et
**perd** sur un modèle dense ordinaire, où le chemin par listes coûte 1,8 à 2,1×
pour rien.

**Quatre corrections de méthode sont consignées dans ce rapport**, et elles
comptent autant que les chiffres : le tokenizer étranger (`data/…ids`, facteur
442), la fenêtre d'évaluation trop courte (trois protocoles, trois réponses), le
cache qui survit à son correctif, et le **binaire plus vieux que ses correctifs**
— trois commits de `drave-core/src` n'étaient pas dans le binaire qui a mesuré la
campagne (§ 17).

### 0 ter. L'état de la campagne au 9 octobre, 1 h 05

Les **neuf étapes** de `tools/campagne-benefices.sh` sont allées au bout
(`=== campagne terminée ===` à 01 h 03), et les portes rendent **22 vertes · 1
rouge** :

| porte rouge | pourquoi | suite |
|---|---|---|
| `gpt-oss-120b MXFP4 ctx 256` — attendu **15,6017** | la passe de 512 jetons a été **tuée par son délai de 2 400 s** pendant que deux autres processus lisaient le même fichier de 63 Go. Le résultat est vide, pas faux | relancée seule à 01 h 04, machine libre de tout autre lecteur |

Tout le reste est vert, y compris `cargo test --release` (**77 tests**), les 17
formats confrontés à libggml, la porte de correction contre llama.cpp
(100 % des positions utiles au-dessus de 0,95, top-1 94,4 %), la porte Mistral, et
les cinq modes de découpage à deux nœuds (écart **0,00e0** pour les modes 0, 1 et
3, 3,65e-2 pour le mode 2, 4,45e-3 pour le mode 4).

---

## 1. Le décodage spéculatif : ×1,2, pas ×2 — mesuré avant d'écrire du moteur

Le moteur n'a **aucune** implémentation du décodage spéculatif, et le brouillon
qui dort sur le disque (`eagle3-gpt-oss-120b`) ne peut pas servir seul : un Eagle3
s'attache aux états cachés de sa cible. Avant d'écrire du moteur, il fallait le
chiffre qui décide — `tools/speculatif.py`, brouillon Qwen2.5-0.5B pour cible
Qwen2.5-1.5B (même tokenizer), 40 préfixes de 64 jetons, k = 8 :

| mesure | valeur |
|---|---|
| acceptation moyenne | **3,35 jetons sur 8 (41,9 %)** |
| médiane · min · max | 3 · 0 · 8 |
| au moins 1 / 2 / 3 / 4 acceptés | 68 % · 60 % · 52 % · 42 % |
| gain espéré si le brouillon coûte **0,25×** la cible | ×1,45 |
| gain espéré s'il coûte **0,33×** | **×1,20** |
| gain espéré s'il coûte **0,50×** | ×0,87 |

**Conclusion, et elle est négative pour la version naïve** : un petit modèle de la
même famille propose en moyenne 3,35 jetons justes sur 8, et le gain net dépend
entièrement du coût relatif du brouillon. Sur cette machine, où le décodage est
borné par la bande passante mémoire, un 0,5 B coûte environ un tiers d'un 1,5 B
par pas : **×1,20**. La feuille de route attendait ×1,58 (mesuré sur le
préremplissage par lots) — on en est loin, et ce n'est pas un défaut
d'implémentation : c'est le taux d'acceptation qui plafonne.

Ce que cela dit pour la suite : un brouillon **générique** ne paie pas. Il faut un
brouillon **aligné** sur sa cible (distillé, ou une tête Eagle3 qui consomme les
états cachés de la cible) — c'est-à-dire un chantier d'entraînement, pas une
option de moteur. Le chiffre est là pour éviter d'écrire le mauvais code.

### 1 bis. Le même chiffre, mesuré PAR LE MOTEUR — et il est bien plus dur

`tools/speculatif_moteur.py` refait la mesure sans HuggingFace : deux GGUF, le
moteur, `--temp 0`, et la comparaison porte sur les **identifiants générés**
(`--- ids générés`), donc sans re-tokenisation. Le vocabulaire partagé est
**vérifié** avant de conclure (même sonde → mêmes identifiants, sinon l'outil
refuse).

Paire mesurée : brouillon **Qwen2.5-0.5B Q8_0** (modèle de base) → cible
**R1-distill-Qwen-1.5B Q4_K_M** (distillat de raisonnement), 8 invites de prose,
48 jetons, k = 8 :

| mesure | valeur |
|---|---|
| acceptation moyenne | **0,88 jeton sur 8 (11 %)** |
| P(préfixe ≥ 1 / 2 / 5) | 38 % · 12 % · 12 % |
| coût relatif du brouillon | 0,210× (14,47 vs 3,04 tok/s, sous charge 30-40) |
| gain net attendu | **×0,70** — il COÛTE |

**Pourquoi 11 % ici et 41,9 % en § 1 : la paire, pas le moteur.** La mesure HF
comparait Qwen2.5-0.5B à **Qwen2.5-1.5B** — même famille *et* même post-
entraînement. Ici la cible a reçu une distillation de raisonnement que le
brouillon n'a pas : les deux modèles divergent **au premier jeton**. Vérifié sur
une invite, texte en clair : le brouillon propose « …which were **not accepted** by
the Convention », la cible « …which were **later used** by other poets » — deux
continuations également plausibles, acceptation nulle.

**La leçon est plus dure que celle du § 1** : ce n'est pas la taille du brouillon
qui décide, c'est **le partage de son post-entraînement**. Un brouillon de la même
famille mais d'une autre recette ne propose rien d'acceptables — et un brouillon
rejeté coûte plus qu'il ne rapporte. Les paires alignées (1,5 B → 14 B, même
recette R1) sont en cours de mesure ; c'est là que le rapport de coût change de
camp, pas sur la taille.

*(Le taux d'acceptation est déterministe — `--temp 0` — donc exact malgré la
charge ; le coût relatif, lui, dépend de la charge et n'est qu'un ordre de
grandeur : 0,210 ici contre 0,245 en § 1 pour la même paire de tailles.)*

---

## 2. Les deux familles de tâches que Drave ne couvre pas

Constatées, et consignées comme manques — pas comme résultats :

| famille | état | ce qui manque |
|---|---|---|
| **embeddings / recherche** | `bge-m3` (BERT, 24 couches, vocab 250 002) est **lisible en en-tête** mais **inexécutable** | le moteur exige `blk.0.attn_norm.weight` et une attention causale ; il n'a ni encodeur bidirectionnel ni pooling |
| **décodage spéculatif** | `eagle3-gpt-oss-120b` (0,84 Go, 1 couche) présent sur le disque | aucune notion de brouillon dans le moteur (`grep eagle\|brouillon\|specul` = 0) — et la mesure par le moteur (§ 1 bis) ajoute une condition que le code ne peut pas lever : **le brouillon doit partager le post-entraînement de sa cible**, sinon il n'accepte rien (0,88 jeton sur 8). Le chantier commence par un entraînement, pas par une option |

Ce sont les deux seules familles demandées par un usage courant qui manquent au
relevé : tout le reste (langage, génération, contexte long, code, raisonnement,
MoE, multilingue, lots, gros-modèle-sur-petite-machine) est couvert.

---

## 3. La grille de modèles — « ce modèle tourne-t-il, et à quel prix ? »

Mêmes 256 jetons, même contexte, chaque modèle tokenisant son propre corpus
(`/usr/bin/time -v` pour la mémoire et les octets lus).

| modèle | perplexité | **bits/octet** | tok/s | RSS | octets lus | condition |
|---|---:|---:|---:|---:|---:|---|
| Qwen2.5-0.5B Q8_0 | **17,43** | **0,983** | 28,7 | 1,28 Go | 0 | en cache |
| r1-distill-Qwen-1.5B Q4_K_M | **47,14** | **1,326** | 9,5 | 4,76 Go | 1,04 Go | lu du disque |
| r1-distill-Qwen-14B Q4_K_M | **14,30** | **0,915** | 0,5 | 39,8 Go | 8,71 Go | lu du disque, charge 47 |
| codestral-22B Q4_K_M | **117,91** ✅ *(tokenizer corrigé)* | **1,797** | — | 63,6 Go | 12,7 Go | mesure invalide avant le correctif (§ 3) |
| Qwen3-30B-A3B Q4_K_M (MoE) | **8,63** | **0,742** | — | **14,3 Go** | 11,8 Go | MoE, lu du NVMe |
| gpt-oss-120b MXFP4 | **expiré à 90 min** | — | — | 13,9 Go | **35,5 Go lus** | 63 Go depuis le disque dur |

**Le MoE gagne sur les deux tableaux — la thèse du projet démontrée par un modèle
qui n'a pas été fait pour ça.** Qwen3-30B-A3B (30 milliards de paramètres, 3
actifs) donne la **meilleure qualité de la grille** (0,742 bit/octet, mieux que le
14B dense à 0,915) pour **14,3 Go de mémoire résidente** — moins que le 14B
(39,8 Go) et trois fois moins que codestral-22B (63,6 Go). Un modèle plus gros qui
lit moins : exactement ce que le prototype routé cherche à reproduire en
l'entraînant.

**L'anomalie codestral : le TOKENIZER du moteur — et la mesure valide après correctif.**

Trois hypothèses ont été testées, les deux premières réfutées, la troisième
confirmée **et corrigée** (§ 3) :

| hypothèse | verdict |
|---|---|
| le moteur exécute mal l'architecture Mistral | **réfutée** — porte Mistral : corrélation 1,0000, top-1 100 % |
| le modèle est spécialisé pour le code, mauvais en prose | **confirmée**, mais seulement après correction |
| le tokenizer du moteur perd les espaces (SentencePiece) | **confirmée et corrigée** |

Avant le correctif, le corpus était découpé par un tokenizer qui mangeait les
espaces : **35 657** de perplexité, chiffre sans valeur. Après le correctif, la
même mesure donne **117,91** sur 63 jetons — soit **1,797 bit/octet**, contre
**0,983** pour un Qwen2.5-0.5B sur le même texte.

**Un modèle de 22 milliards de paramètres est donc 1,8× PIRE qu'un 0,5 B sur de
la prose**, parce qu'il a été entraîné pour du code. C'est le décalage de tâche
annoncé, et il n'était mesurable qu'avec un tokenizer juste.

**La perplexité n'est PAS comparable d'un tokenizer à l'autre.** Codestral
(32 768 entrées) découpe ce texte en **288 554** jetons là où Qwen en fait
**85 626** : son « PPL » se lit sur une autre échelle. La colonne **bits/octet**
est la seule unité commune — `log₂(PPL) × jetons / octets`, recalculée depuis le
journal de tokenisation de chaque modèle. Le tableau la porte pour que la
comparaison reste possible.

**Un résultat contre-intuitif, et il est solide** : les trois premiers modèles
partagent **exactement le même tokenizer** (leurs fichiers d'identifiants
commencent par les mêmes jetons `198,284,8397,…`), donc leurs chiffres se
comparent directement. Or le **r1-distill-1.5B est 2,7× PIRE que le 0.5B** sur
cette tâche (1,326 contre 0,983 bit/octet). Ce n'est pas la quantification
(Q4_K_M contre Q8_0) qui explique un tel écart : c'est le modèle — un distillat de
raisonnement, entraîné pour produire de longues chaînes de pensée, est mauvais en
modélisation de langue pure. **La taille ne dit pas la qualité pour une tâche
donnée** ; c'est exactement ce que la question « pour tout type de tâches »
demandait de vérifier, et la réponse est non.

Le 14B redresse la barre (0,915 bit/octet) mais à **0,5 tok/s** sous charge 47 —
le temps, lui, n'est pas une mesure propre ici, et c'est écrit dans le journal.

**gpt-oss-120b : la passe de 256 jetons n'a PAS fini en 90 minutes** (délai
atteint), après avoir lu **35,5 Go** avec 13,9 Go résidents. C'est un résultat en
soi : sur ce disque et sous cette charge, une passe de 256 jetons sur un modèle de
63 Go **ne tient pas dans un créneau de 90 minutes**. Une fenêtre plus courte
(32 jetons) a été relancée pour obtenir le chiffre manquant.

*(tableau complété à mesure ; `tools/campagne_synthese.py` le régénère depuis les
journaux, colonne `bits/octet` comprise)*

---

## 4. Ce que le dépôt sait déjà, par famille de tâches (avant cette campagne)

Consolidé des rapports existants, pour que les chiffres du jour se lisent dans un
ensemble plutôt que seuls. Chaque ligne cite sa source.

| famille | acquis mesuré | source |
|---|---|---|
| **langage (perplexité)** | Qwen2.5-0.5B ctx 256 = **19,3885** · gpt-oss ctx 256 = **15,1757** (portes de non-régression) | `tools/portes.sh`, `REPRISE.md` |
| **débit CPU, sans BLAS** | 0,5 B quantifié : **15,8 tok/s**, 5,3 G événements/s, 16/16 jetons identiques à numpy | `rapport-inference.md` |
| **préremplissage par lots** | ×1,58 sur Qwen3-30B-A3B (invite de 192 jetons, NVMe), et **15,5× moins d'octets d'experts** | `rapport-prefill-par-experts.md` |
| **contexte long** | KV int8 : **+1,5 %** de PPL à 512 jetons, **+3,0 %** à 8 192 (int4 : +364 %) ; KV paginé : **0,03 Go au lieu de 25,77 Go** à 1 M | `rapport-placement-bits-kv.md`, `docs/contexte-long.md` |
| **attention sur GPU** | **22,16 → 3,29 ms/jeton** (÷6,7) au décodage, ×2,8 en préremplissage ; tête 7,58 → 3,60 ms | `docs/contexte-long.md` |
| **MoE / routage** | Qwen3-30B-A3B : **4 experts sur 128** par couche et par jeton (3,1 %) ; porte clusters **799,8557** | `rapport-localite-activation.md`, `portes.sh` |
| **parcimonie imposée** | k-WTA 85 % = **−13,1 % d'événements pour +0,46 % de PPL** ; le seuil absolu est 10× pire | `rapport-campagne-parcimonie.md` |
| **modèle plus gros que la RAM** | Kimi-K3 (1,5 To) sur 125 Go : passe de 4 jetons = **206,58 Gio lus**, 133 Mio/s, disque occupé 87,6 %, CPU 21 % — **26,5 min**, contre 42 min/jeton pour llama.cpp | `rapport-passe-k3-disque.md` |
| **répartition** | deux nœuds, cinq modes : écart **0,00e0** sur les modes exacts ; **1 608 octets** par flux à 256 jetons ; attente ≈ calcul distant + 3,2 × latence | `porte-flux.sh`, `docs/roadmap.md` |
| **routage d'experts à l'échelle** | 72 % des octets d'une passe sont les experts, **relus à chaque jeton** ; le dense est lu une fois et partagé | `rapport-passe-k3-disque.md` |
| **multilingue / sémantique** | bande **10–15 sur 24 couches** (42–62 % de séparation) sur **398 langues** ; couche 0 : séparation nulle | `rapport-cycle-rapide.md` |
| **embeddings** | **rien** — `bge-m3` est inexécutable (§ 2) | cette campagne |
| **décodage spéculatif** | **rien** dans le moteur ; le taux d'acceptation mesuré est de 41,9 % (§ 1) | cette campagne |

Deux lignes de ce tableau sont des **manques**, et elles sont écrites comme telles :
c'est la moitié de la réponse à « pour tout type de tâches ».

---

## 5. Les modèles entraînés ici, mesurés DANS le moteur — routage ET distillation gagnent

**Le protocole, et il a fallu le corriger.** Le moteur évalue une fenêtre contiguë
de `--limit` jetons ; ces modèles ont été **entraînés sur des fenêtres de 128
jetons**. Les évaluer sur 256, 512 ou 2 048 positions les fait sortir de leur
distribution (à 2 048, la perplexité triple et le classement s'inverse). La mesure
retenue est donc **huit fenêtres de 128 jetons** (`--depuis` décale le début),
moyennées en log — dans la longueur d'entraînement, sur huit tranches du fichier
de validation. Toutes les portes de logits sont tenues.

| modèle | paramètres | PPL moyenne (8 × 128) | paires/jeton | vs jumeau dense |
|---|---:|---:|---:|---:|
| `m5_d256_dense` | 3,2 M | 5,0155 | 3,2 M | — |
| `m5_d256_route` | 10,3 M | 4,8858 | 3,2 M | −2,6 % |
| **`m5_d256_route_distille`** | 10,3 M | **4,7642** | 3,2 M | **−5,0 %** |
| `m5_d384_dense` *(le professeur)* | 7,2 M | 5,0108 | 7,2 M | — |
| `m5_d384_route` | 44,4 M | 4,8646 | 7,2 M | −2,9 % |
| **`m5_d384_route_distille`** | 44,4 M | **4,4113** | 7,2 M | **−12,0 %** |

**Trois résultats, et le troisième est le plus fort.**

1. **Le routage gagne à lecture exactement égale** (vérifié par le compteur du
   moteur) : −2,6 % et −2,9 % de perplexité en stockant 3,2× et 6,2× plus de
   paramètres. C'est la thèse du projet — un modèle plus gros qui lit autant.
2. **La distillation ajoute, et son gain CROÎT avec la taille** : −2,5 % à
   dim 256, **−9,3 % à dim 384**. Le professeur (dense dim 384, 5,0108) est
   **battu par son élève** (4,4113), qui lit pourtant 1,92 M poids par jeton au
   lieu de 7,2 M.
3. **Au total, à lecture égale, le modèle produit ici est 12 % meilleur que son
   jumeau dense** — sans un paramètre de plus à lire.

**Une réserve qui reste** : les débits. À `d256` le routé est plus rapide que le
dense en listes (662,8 contre 442,3 tok/s), à `d384` plus lent (184,0 contre
255,0) — le regroupement des jetons par expert a un coût fixe qui pèse quand le
modèle grandit. Le gain de qualité, lui, tient dans les deux cas.

**Et les experts ne passent PAS par les listes** : écrits en Q4_0, format pour
lequel le moteur n'a pas de noyau de listes, ils sont exécutés en dense. La mesure
honnête du coût est donc la colonne « paires/jeton », égale par construction.

### 5 bis. Le gain du routage N'EST PAS monotone : il s'inverse à dim 512

La courbe s'arrête d'abord à dim 384 dans ce rapport. L'échelle 512 a été
entraînée **avec exactement le même protocole** (4 couches, 40 000 pas, mêmes
données), et le résultat renverse la tendance — **deux mesures indépendantes le
disent**, la validation à l'entraînement et le moteur après export :

| dim | dense (val, bits/octet) | routé (val) | gain du routage | PPL moteur (8 × 128) |
|---:|---:|---:|---:|---|
| 256 | 2,0074 | 1,9373 | **−3,5 %** | 5,0155 → 4,8858 (−2,6 %) |
| 384 | 1,9020 | 1,8762 | −1,4 % | 5,0108 → 4,8646 (−2,9 %) |
| **512** | **1,8580** | **1,8843** | **+1,4 % — le routé PERD** | **4,5686 → 5,0255 (+10 %)** |

**Et c'est bien à lecture ÉGALE**, vérifié par le compteur du moteur sur les deux
modèles exportés : **12,8 M de paires par jeton de part et d'autre** (attention
3,2 M pour les deux ; experts 9,5 M + partagé 0,1 M pour le routé contre partagé
9,6 M pour le dense).

Deux réserves, et elles sont dans la mesure : les deux modèles ont reçu
**40 000 pas**, alors que le routé stocke 78,8 M paramètres contre 12,7 M — il est
donc possible qu'il soit **sous-entraîné** à cette échelle, et c'est une hypothèse,
pas un résultat. La distillation du routé 512 (professeur : son jumeau dense) est
en cours et dira si le levier du § 5 rattrape ce renversement.

**Ce que cela change dans ce rapport** : la phrase « le routage gagne » n'est vraie
qu'aux petites échelles. À dim 512, **un modèle dense deux fois plus petit lit
autant et fait mieux** — et c'est la première fois que la campagne mesure un
résultat qui va contre la thèse du projet. Il est consigné comme tel.

---

## 7. Répartir par EXPERTS : ce que coûterait l'unité de travail naturelle

Le dépôt découpe par **plages de couches** (prouvé, écart 0,00e0). Mais l'unité
naturelle d'un modèle routé, c'est l'**expert** — et la sommation inter-nœuds
n'existe pas (`Moe::ou` → `None` → `continue` : un nœud partiel saute l'expert
absent sans un mot). `tools/census_routage.py` donne les trois chiffres qui
décident, mesurés sur `m4_route` (4 couches, 8 experts, top-2, 1 024 jetons) :

| couche | charge max | charge moyenne | déséquilibre | experts pour 90 % des jetons |
|---|---:|---:|---:|---:|
| 0 | 537 | 256 | **×2,10** | 5 sur 8 |
| 1 | 517 | 256 | ×2,02 | 7 sur 8 |
| 2 | 703 | 256 | **×2,75** | 6 sur 8 |
| 3 | 999 | 256 | **×3,90** | 4 sur 8 |

**Trois enseignements, et le troisième commande la suite.**

1. **Le déséquilibre est réel** : jusqu'à **3,9×** entre l'expert le plus chargé
   et la moyenne. Un partage naïf par experts donnerait un nœud 4 fois plus
   chargé que l'autre — il faut un routeur qui équilibre, ou un découpage qui
   tienne compte de la charge mesurée.
2. **On ne peut pas élaguer** : à top-2 sur 8, **4 à 7 experts** sont nécessaires
   pour couvrir 90 % des jetons. Tous servent ; la « localité » qui justifierait
   de n'en garder que quelques-uns n'existe pas à cette échelle.
3. **Le volume à router est négligeable, la latence ne l'est pas.** L'état
   transporté vaut **847 octets** par jeton (79 d'en-tête + 192 × 4) — du même
   ordre que les **848 octets** mesurés pour un flux de couche. Ce qui coûte,
   c'est l'aller-retour par couche, pas les octets : le dépôt a mesuré
   `attente ≈ calcul distant + 3,2 × latence`. Répartir par experts multiplie
   donc les allers-retours que répartir par couches évite.

---

## 8. Les tâches à SORTIE CONTRAINTE : une matrice qu'on ne lit pas

La tête de sortie est **la plus grosse matrice du modèle** : vocabulaire × cachés.
Pour le 0,5 B, 151 936 × 896 = **136 M poids, soit 136 Mo lus par jeton** — un
cinquième du modèle entier pour une seule projection. Or une classification ou un
choix multiple n'a que quelques sorties valides : `--tete-restreinte` ne calcule
que celles-là.

Mesure entrelacée, 64 jetons générés, 0,5 B Q8_0, 8 fils :

| tête | tour 1 | tour 2 | moyenne |
|---|---:|---:|---:|
| complète (151 936 jetons) | 14,79 tok/s | 16,14 tok/s | 15,47 |
| **restreinte à 3 jetons** | **21,92** | **22,07** | **22,00** |

**×1,42 de débit**, et la tête restreinte est **stable** (21,92 / 22,07 là où la
complète varie de 14,79 à 16,14 — moins de travail, donc moins de sensibilité à
la charge).

**Le second bénéfice compte plus que le premier, et il ne se mesure pas en
tok/s** : la sortie **ne peut pas** être hors de l'ensemble autorisé. Dans l'essai,
le modèle a produit `neutral negative negative positive positive negative neutral
positive` — des réponses incohérentes (un 0,5 B ne sait pas juger un sentiment),
**mais jamais un mot hors des trois étiquettes**. Pour une tâche de production,
cela vaut plus que la vitesse : plus de post-traitement, plus de reprise, plus de
réponse invalide à rattraper.

C'est donc la **première famille de tâches où l'architecture de Drave gagne par
construction** plutôt que par ses circonstances (modèle plus gros que la RAM) —
et elle ne demande aucun modèle particulier.

Le batch 7 refait la mesure sur le 1,5 B et sur gpt-oss-120b, où le rapport
tête/corps est différent.

---

## 9. La mémoire TIENT : l'aiguille est retrouvée à toutes les profondeurs

La perplexité moyenne ne dit pas si un modèle **retrouve** un fait précis. Test :
un code unique planté dans une botte de foin, à trois profondeurs (10 %, 50 %,
90 %), et une question à la fin. Qwen2.5-0.5B Q8_0, `--infer`, 12 jetons, `temp 0` :

| longueur | profondeur 10 % | 50 % | 90 % |
|---|---:|---:|---:|
| 512 jetons | ✅ | ✅ | ✅ |
| 1 024 | ✅ | ✅ | ✅ |
| 2 048 | ✅ | ✅ | ✅ |
| 4 096 | ✅ | ✅ | ✅ |

**12 configurations sur 12 retrouvent le code**, y compris à 4 096 jetons avec un
modèle de 0,5 B. C'est une mesure de **tâche**, pas de perplexité : le cache KV du
moteur, sa quantification et sa pagination ne détruisent pas la mémoire du
contexte. C'est exactement ce que la revendication « contexte long » devait
démontrer, et c'est la première fois qu'elle l'est sur une tâche.

**Réserve, et elle est sérieuse sur les temps** : cette série a tourné **en
parallèle de la campagne** (un défaut d'enchaînement corrigé depuis), donc deux
gros modèles lisaient le disque en même temps. Les **verdicts** (retrouvé/perdu)
n'en dépendent pas ; les **durées** oui — de 26 s à 609 s pour la même taille,
selon ce que le disque faisait à ce moment-là.

---

## 10. La génération : TTFT et débit, mesure directe

| modèle | invite | TTFT | débit de génération |
|---|---:|---:|---:|
| Qwen2.5-0.5B Q8_0 | 11 jetons en 0,307 s | **27,9 ms** | **29,0 tok/s** |
| r1-distill-1.5B Q4_K_M | 11 jetons en 1,260 s | 114,6 ms | 7,1 tok/s |
| r1-distill-14B Q4_K_M | *en cours* | | |
| Qwen3-30B-A3B | *en cours* | | |
| gpt-oss-120b MXFP4 | *en cours* | | |

Ces chiffres-là portent la **latence perçue** d'un usage réel, que la perplexité
ne donne pas : un premier jeton en 28 ms et 29 jetons/s sur un 0,5 B, c'est un
assistant utilisable ; 7 jetons/s, c'est déjà pénible.

---

## 10 bis. Quatre tâches, sorties verbatim — et c'est le MODÈLE qui limite, pas le moteur

Le batch 4 les avait prévues sur gpt-oss-120b (5 × 1 h de lectures du même fichier
de 63 Go, en concurrence avec la mesure PPL). Refaites ici sur le **0,5 B**, qui
suffit à répondre à la seule question qui compte : le moteur produit-il une sortie
**exploitable** ? Sorties **telles quelles**, `temp 0`, 64 jetons.

| tâche | sortie du 0,5 B | verdict |
|---|---|---|
| **code** | `def fibonacci(n):` … gère `n <= 0`, `n == 1`, `n == 2` … | ✅ **correcte et utilisable** |
| traduction FR | *« The river carries the logs to the mill. (No translation is needed) »* puis *« Le ruisseau transporte les feuilles au mill. »* | ❌ refuse, puis traduit faux (`feuilles` = leaves, `mill` non traduit) |
| arithmétique | entame un raisonnement juste (« we need to calculate the difference… ») | ⚠️ **tronquée** à 64 jetons — la réponse n'apparaît pas |
| résumé | *« The engine is a key component in the development of the new generation of engines. »* | ❌ hallucination, puis recopie de l'entrée |

**Ce que cela dit.** Le moteur a produit une **fonction Python correcte** avec un
modèle de 0,5 B — sur la tâche où le format est contraint (du code), il tient. Sur
la traduction, l'arithmétique et le résumé, c'est le **modèle** qui échoue, pas
l'exécution : Drave est un moteur, il fait ce que le modèle sait faire. C'est
aussi pourquoi la ligne « sortie contrainte » du verdict est la seule où
l'architecture gagne *par construction*.

*(Débit de ces essais : 0,84 tok/s, sous une charge de fond de **84** — trois gros
modèles lus en parallèle. Le chiffre ne dit rien du modèle ; il dit que mesurer
sous cette charge ne vaut que pour les sorties, pas pour les temps.)*

---

## 10 ter. La densité d'activation ne dépend PAS de la tâche — la qualité, si

Même modèle (Qwen2.5-0.5B Q8_0), même matériel, quatre corpus, 192 jetons : la
question du batch 2 était « le bénéfice événementiel dépend-il de la tâche ? ».

| corpus | jetons/octet | PPL | **bits/octet** | paires/jeton | **densité** |
|---|---:|---:|---:|---:|---:|
| prose anglaise | 0,2385 | 15,85 | **0,951** | 495,9 M | **71 %** |
| français | 0,2783 | 11,19 | **0,969** | 495,9 M | **71 %** |
| code | 0,3117 | 7,09 | **0,881** | 495,9 M | **71 %** |
| **399 langues** (UDHR, article 1) | 0,4113 | **229,84** | **3,227** | 495,9 M | **71 %** |

**La densité est identique dans les quatre cas — 71 %, à 0,002 point près**
(67,766 / 67,767 / 67,766 / 67,764 milliards d'événements). Autrement dit : **le
bénéfice événementiel ne dépend pas de la tâche**, il dépend du **modèle**. Un
modèle dense reste dense quelle que soit l'entrée ; c'est la parcimonie
*entraînée* qui la change, et rien d'autre. L'hypothèse « telle tâche réveille
moins de neurones » est **réfutée** ici — y compris sur un corpus qui change
complètement d'écriture et de langue.

**Ce qui dépend de la tâche, c'est la qualité.** En bits/octet — la seule unité
comparable entre tokenizers — le même modèle prédit le **code mieux que la prose**
(0,881 contre 0,951) et le **français moins bien que l'anglais** (0,969 contre
0,951). Les perplexités brutes disent l'inverse (7,09 pour le code contre 15,85
pour la prose) uniquement parce que le code se tokenise en jetons plus longs :
c'est exactement le piège que la colonne bits/octet neutralise.

**Et sur 399 langues, le même modèle est 3,4× pire qu'en prose** (3,227 contre
0,951 bit/octet) — la ligne la plus défavorable du relevé. La réserve est dans la
nature du corpus : ce n'est pas *une* langue, c'est un empilement de 399 langues
dont beaucoup sont peu dotées, donc cela mesure une **couverture**, pas une
performance linguistique. C'est néanmoins la réponse à « pour tout type de
tâches » : sur cette famille, l'échelle de 0,5 B ne suffit pas, et **la densité
d'activation ne bouge pas d'un iota** — le moteur événementiel n'y gagne donc
rien de plus qu'ailleurs ; c'est le modèle qui est en défaut.

**Le seuil absolu, lui, s'effondre sur ce corpus** : `--act-thresh 0,05` fait
passer la perplexité de 229,8 à **2 542** (et l'événementiel de 67,8 à 29,2 G) —
soit ×11, alors que le k-WTA au même taux d'événements ne coûte que quelques pour
cent (§ 19). Le résultat du § 19 n'est donc pas une propriété de la prose
anglaise : il tient sur les quatre corpus.

---

## 12. Le cas extrême : **365,7 Go sur une machine de 125 Go**

DeepSeek-V4.1-Flash Q2, exécuté par le moteur, mmappé, sans copie — deux fenêtres
minuscules, mais c'est le COÛT qui est la mesure ici :

| fenêtre | RSS | octets lus | temps |
|---|---:|---:|---:|
| 8 jetons, ctx 32 | **27,7 Go** | 32,5 Go | 216 s |
| 16 jetons, ctx 64 | **37,6 Go** | 37,7 Go | 266 s |

**Un modèle de 365,7 Go tourne sur une machine de 125 Go de RAM avec 38 Go
résidents.** Il n'est pas chargé, il est **ruisselé** : chaque passe lit ce qu'elle
touche et rien d'autre. C'est la revendication centrale du projet, mesurée sur le
plus gros modèle présent sur le disque.

**Ce que ces chiffres ne disent PAS, et il faut le dire** : la perplexité de ce
modèle sur ce corpus est énorme (13,2 M et 659 139) et n'a **aucune valeur** —
elle mélange une quantification Q2 agressive, une fenêtre de 16 jetons et une
tokenisation dont on n'a pas vérifié la réversibilité (§ 3). La ligne « modèle
plus gros que la RAM » du verdict porte donc sur **l'existence et le coût**, pas
sur la qualité.

---

## 13. La tête restreinte, sur deux modèles de plus

`--tete-restreinte` sur une tâche à trois étiquettes (positive / negative /
neutral), 64 jetons, deux tours entrelacés, sous charge 41-46 :

| modèle | tête complète | **tête restreinte** | gain |
|---|---:|---:|---:|
| Qwen2.5-0.5B | 17,35 / 15,73 tok/s | **21,40 / 23,85** | **×1,36** |
| r1-distill-1.5B | 4,66 / 8,45 tok/s | **6,27 / 7,08** | ×1,11 (bruité) |

Et le contrôle qui compte, sur les mêmes journaux : la sortie de la tête
**restreinte** ne contient que les mots autorisés — les occurrences d'étiquettes
passent de **10 à 67** (0,5 B) et de **7 à 67** (1,5 B), parce que le modèle ne
*peut pas* produire autre chose. La tête complète, elle, écrit du texte libre.

**Ce qui est robuste ici, c'est la garantie, pas le débit** : le gain de vitesse
dépend du rapport tête/corps du modèle (×1,36 sur un 0,5 B, à peine sur un 1,5 B
où d'autres postes dominent), alors que la contrainte de sortie, elle, est
**structurelle** — et c'est la seule ligne du verdict où l'architecture gagne sans
dépendre ni du modèle ni de la machine.

**Et sur un modèle plus gros que la RAM, la tête restreinte ne gagne RIEN** — la
mesure qui manquait, faite le 9 octobre sur gpt-oss-120B (63 Go, MXFP4, disque),
même invite, 64 jetons :

| passe (gpt-oss-120B, 20 threads) | 64 jetons | tok/s | conditions |
|---|---:|---:|---|
| tête complète, 1er essai | **aucun jeton en 3 600 s** | — | une autre passe lisait les mêmes 63 Go |
| tête restreinte (3 jetons) | 163,9 s | 0,39 | cache chaud, lecteur concurrent |
| tête complète, 2e essai | 171,9 s | 0,37 | cache chaud, lecteur concurrent |
| tête restreinte, 2e essai | **71,0 s** | **0,90** | cache chaud, **seule** |

**Les durées ne sont pas comparables entre elles** (la lecture concurrente du même
fichier les domine : 3 600 s contre 164 s pour la même tâche), mais une borne,
elle, ne dépend pas de la charge : la couche de sortie de ce modèle pèse
**0,58 G de poids par jeton sur 4,93 G de paires lues, soit 12 %**. Restreindre la
tête ne peut donc pas rapporter plus de **×1,12** ici — et l'essentiel est dans les
**experts** (3 583 M paires/jeton), que la tête restreinte ne touche pas.

Le diagnostic de colonnes, imprimé par la même passe, va dans le même sens :
94,8 % des coordonnées d'entrée de la tête sont vivantes, donc un stockage par
colonnes n'éviterait que **5 %** de la matrice. **Sur un MoE plus gros que la RAM,
le levier n'est ni la tête ni sa disposition : c'est le routage des experts.**

*(Rappel de méthode : le premier essai « tête complète » a été tué par le délai de
3 600 s **pendant** qu'une mesure de perplexité lisait le même fichier de 63 Go —
c'est un résultat sur la contention, pas sur la tête. Les deux passes à cache
chaud donnent ×1,05, très en dessous de la borne de ×1,12.)*

---

## 14. Une mesure à refaire : le lot sur le 30B a mesuré le cache de pages

Batch 5, Qwen3-30B-A3B depuis le NVMe, `--lot` de 1 à 64 :

| lot | PPL | tok/s | octets lus | mur |
|---:|---:|---:|---:|---:|
| 1 | 7,6139 | 0,4 | **10 954 Mio** | 345 s |
| 4 | 7,6098 | 1,4 | 0 | 118 s |
| 8 | 7,6098 | 1,4 | 0 | 118 s |
| 32 | 7,6098 | 1,2 | 0 | 138 s |
| 64 | 7,6098 | 1,2 | 0 | 135 s |

**Le protocole a mesuré le cache de pages, pas le lot** : seule la première passe
a lu (10,9 Go, à froid) ; les suivantes ont tout trouvé en mémoire (0 octet lu) et
durent toutes ~2 minutes. La comparaison lot 1 / lot 4 n'est donc **pas** une
mesure du lot — c'est une mesure de « à froid contre à chaud ». Les PPL, elles,
sont identiques (7,6098 à partir du lot 4), ce qui confirme au moins que **le lot
ne change pas le résultat**.

Pour mesurer le lot, il faut un modèle plus gros que la mémoire — ce que le § 12
donne — ou vider le cache entre les passes, ce que la campagne ne peut pas faire
sans root.

### 14 bis. Le protocole corrigé : éviction sans root, et le résultat n'est pas celui qu'on attendait

`posix_fadvise(POSIX_FADV_DONTNEED)` jette les pages d'un fichier hors du cache
**sans être root** : c'est ce qui manquait. `tools/mesure_lot_disque.sh` évince le
modèle avant **chaque** réglage — le journal le confirme (« cache du modèle
évincé : 17,3 Go ») — puis lit les octets réellement lus dans `File system inputs`.

Qwen3-30B-A3B depuis le NVMe, 192 jetons, ctx 512, à froid à chaque passe :

| `--lot` | PPL | **octets lus** | mur | tok/s |
|---:|---:|---:|---:|---:|
| 1 | 7,4244 | **12 586 Mio** | 2 min 06 | 2,1 |
| 2 | 7,4228 | 17 520 Mio | 2 min 14 | 1,9 |
| 4 | 7,4228 | **21 006 Mio** | 4 min 12 | 0,9 |
| 8 | 7,4228 | 17 338 Mio | 4 min 03 | 0,9 |
| 16 | 7,4228 | 13 360 Mio | 1 min 18 | 3,8 |

**La perplexité est invariante au lot** (7,4228 dès le lot 2 — 0,02 % d'écart avec
le lot 1) : c'est le résultat net, et il confirme le § 20 sur un second modèle.

**Les octets lus, eux, ne baissent pas** — ils montent, puis redescendent, pour un
fichier de 17,3 Go. Le mécanisme est visible dans les compteurs du moteur : les
paires d'experts **par jeton** valent 1 840,7 M au lot 1 et 1 821,4 M au lot 16,
soit **le même chiffre** — le moteur regroupe bien les jetons par expert et ne
relit pas un expert pour chaque jeton du lot. Ce qui change avec le lot, c'est
**l'union des experts touchés par une passe** : sur 48 couches à 128 experts et
4 experts par jeton, une passe de 192 jetons finit par ouvrir **presque tous les
experts de toutes les couches**, quel que soit le découpage en lots. Le disque
n'est donc pas un levier de lot sur un MoE : il l'est sur un modèle **dense**, où
chaque passe relit les mêmes poids — et là, c'est le nombre de **jetons par passe**
qui amortit la lecture, pas la taille du lot.

**Ce que cette mesure ne dit pas** : les temps. Ils varient de 78 s à 252 s pour la
même quantité de calcul, sous une charge de fond de 30 à 40 (d'autres lectures de
modèles tournaient). La colonne tok/s n'est publiable qu'avec cette réserve, et
l'ordre de grandeur seul est utilisable.

---

## 16. Deux pièges de méthode, consignés

**Un cache qui survit à son correctif.** La mesure sémantique avec l'échelle
corrigée a d'abord rendu **exactement les chiffres publiés** (couche 0 : +0,0002 ;
couche 4 : +0,0156) — parce que le cache de vecteurs de `/tmp` datait de la
session précédente, **avant** le correctif du lecteur. Un cache qui ne porte pas
la version de l'outil qui l'a écrit fait mesurer l'ancien code avec le nouveau :
les fichiers ont été supprimés et la comparaison relancée à caches neufs.

**Un outil dont l'option `--cache` écrase les deux côtés.** Dans
`premiere_couche_semantique.py`, la même expression
`opt("--cache", "/tmp/pcs_a1")` sert aux DEUX dossiers comparés (A et B) : passer
`--cache X` fait donc écrire les deux jeux dans `X.moyenne.npz`, et la
comparaison oppose un dossier à lui-même. Sans `--cache`, les deux défauts sont
distincts et tout va bien — c'est pourquoi le piège ne s'était pas vu.

---

## 17. L'instrument : le binaire de la campagne était plus VIEUX que ses correctifs

**Le fait.** `drave-core/target/release/drave` portait la date du 8 octobre 11 h 00.
Trois commits touchant `drave-core/src` sont **postérieurs** : `8de0612` (11 h 08,
`--ids-file` ignoré en mode réparti), `ddebb6b` (23 h 26, tokenizers SentencePiece),
`9cdfbd7` (00 h 05, le banc des encodages qui plantait sur les K-quants). Les
correctifs existaient donc dans les sources et **pas dans le binaire qui a mesuré
la campagne** — ils avaient été compilés à part (`CARGO_TARGET_DIR=/tmp/target-spm`)
pour ne pas déranger la campagne en cours, et jamais promus.

**La preuve, en une commande.** Le même texte, les deux binaires :

| binaire | « The river carries the logs to the mill » |
|---|---|
| celui de la campagne (8/10 11 h 00) | **31 jetons**, recolle `"Therivercarriesthelogstothemill"` |
| celui des correctifs (`/tmp/target-spm`, 00 h 02) | **8 jetons**, recolle `" The river carries the logs to the mill"` |

**Ce qui est touché, et ce qui ne l'est pas.** Seuls les modèles à tokenizer
**SentencePiece** (Mistral, Codestral, Llama, Gemma). Tous les autres — Qwen,
Qwen3-MoE, gpt-oss, V4 — sont en BPE byte-level, chemin qui n'a pas changé. Et le
dépôt porte la vérification : `--tokenize` imprime un contrôle de réversibilité, et
les six journaux de tokenisation de la campagne disent lesquels sont valides :

| modèle | contrôle de réversibilité (journal de la campagne) |
|---|---|
| Qwen2.5-0.5B · R1-1,5B · R1-14B · Qwen3-30B-A3B · gpt-oss-120B | **texte reconstruit identique ✅** |
| codestral-22B | **DIVERGE** — l'instrument a signalé lui-même sa propre ligne |

**Ce que cela change dans ce rapport** : la ligne « codestral-22B » de la grille
(§ 3) porte **35 657**, chiffre mesuré sur un texte dont les espaces étaient
mangés, et **117,91** après correctif — c'est le corrigé qui est retenu, et il a
été obtenu avec le binaire corrigé. Les fichiers d'identifiants en cache
(`ids_codestral-22B.txt`) sont, eux, **empoisonnés** : ils ont été produits par le
binaire périmé et doivent être refaits, pas réutilisés.

**Deux corrections de code sont nées de ce constat :**
1. le contrôle de réversibilité distingue maintenant l'écart d'**un espace de tête**
   — la convention `add_dummy_prefix` de SentencePiece, qui faisait afficher
   « DIVERGE à l'octet 0 » sur *tous* les modèles SPM pour un octet de convention —
   d'une **vraie** perte d'information, qui reste signalée comme telle ;
2. `DRAVE_SANS_EMPRUNT=1` devient obligatoire pour toute comparaison dense/listes :
   sans lui on compare deux schémas de quantification, pas deux chemins
   d'exécution (§ 22).

**La leçon de méthode** : un correctif non promu est un correctif qui n'existe pas,
et un cache d'identifiants ne porte pas la version de l'outil qui l'a écrit. Les
deux pièges du § 16 sont de la même famille — et celui-ci est le plus coûteux,
parce qu'il ne se voyait que sur un modèle sur six.

---

## 18. Le résultat publié SURVIT au correctif d'échelle (sémantique multilingue)

La bande sémantique « 10–15 sur 24 couches » avait été mesurée avec un lecteur qui
**ignorait l'échelle par enregistrement** des traces DRVF. Le lecteur est corrigé ;
la question était : le résultat tient-il ? Caches **neufs** des deux côtés,
398 langues, article 1 contre article 2, pooling moyenne :

| couche | ancienne lecture | **échelle corrigée** |
|---|---:|---:|
| 0 | +0,0002 | **+0,0030** |
| 4 | +0,0156 | +0,0175 |
| 12 | — | +0,0354 |
| **13** | **+0,0344** | **+0,0395** |
| 14 | — | +0,0342 |
| 15 | — | +0,0326 |

**La bande 10–15 tient, et le pic reste à la couche 13** — légèrement plus marqué
après correction (+0,0395 contre +0,0344). Ce qui change : la couche 0 n'est plus
« exactement nulle » (+0,0030), ce qui est cohérent — l'échelle par enregistrement
n'est pas uniforme d'une couche à l'autre, et son omission écrasait
différentiellement les premières couches.

**C'est le premier résultat publié du dépôt qui soit revérifié après un correctif
de lecteur, et il survit.** La conclusion (une bande 10–15, un plateau, un effet
petit sur un fond anisotrope élevé) reste celle du `rapport-cycle-rapide.md`.

---

## 19. La parcimonie imposée, sur 24 réglages : le k-WTA écrase le seuil, encore

Qwen2.5-0.5B Q8_0, 256 jetons, ctx 512, deux familles de réglages et les deux
chemins d'exécution. **Seules les colonnes déterministes sont utilisables** :
`acttopk1000dense` et `actthresh0dense` sont *la même configuration* et donnent
12,1 et 22,6 tok/s — le bruit de temps vaut ×2 sous cette charge de fond (67-84).
Les PPL, les événements et les paires, eux, sont exacts.

| réglage | PPL (dense / listes) | M événements/jeton | **PPL à −30 % d'événements** |
|---|---|---:|---:|
| aucune parcimonie | 17,43 / 17,41 | 354 | — |
| seuil 0,1 % | 17,34 / 17,31 | 344 | −2,6 % d'évts |
| seuil 0,5 % | 17,84 / 17,87 | 312 | **+2,3 % de PPL** |
| seuil 1 % | 21,01 / 20,53 | 281 | **+20 %** |
| seuil 2 % | 29,50 / 29,48 | 229 | **+69 %** |
| seuil 5 % | **3 176** / 3 714 | 151 | effondrement |
| k-WTA 85 % | 17,69 / 17,40 | 302 | −15 % |
| k-WTA 80 % | 17,58 / 17,43 | 284 | −20 % |
| k-WTA 70 % | 18,11 / 18,92 | 248 | **+4 % pour −30 % d'évts** |
| k-WTA 50 % | 28,36 / 30,56 | 177 | +63 % |

**Le résultat du dépôt se reproduit au chiffre près, un autre jour, sous une autre
charge : le seuil absolu est inutilisable, le k-WTA tient.** À −30 % d'événements,
le seuil coûte **+69 %** de perplexité là où le k-WTA coûte **+4 %** — un facteur 17.

**Et une nuance que la mesure ajoute** : dans le chemin **dense**, la parcimonie ne
réduit **aucune lecture** (495,4 M paires/jeton dans tous les cas) — elle ne fait
que mettre à zéro des activations. Ce n'est que dans le chemin **par listes** que
les événements baissent (354 → 248 M). Autrement dit, **la parcimonie imposée ne
paie que si le moteur exécute en listes** ; en dense, elle ne coûte que la qualité.

**Correction du 9 octobre : les deux colonnes de ce tableau ne comparent pas la
même arithmétique.** En mode `--dense`, le moteur *emprunte* les blocs Q8_0 du
fichier tels quels (schéma d'échelle de llama.cpp) ; en mode `--push`, il
reconstruit ses propres listes depuis les poids déquantifiés (notre schéma). Même
corpus, même modèle, aucune parcimonie : **17,4315 emprunté · 17,4084 reconstruit ·
17,4084 en listes**. L'écart entre les colonnes dense et listes du tableau
ci-dessus (0,1 à 0,5 %) vient donc **de l'encodage des poids, pas du chemin
d'exécution** — et la variable d'environnement `DRAVE_SANS_EMPRUNT=1` le prouve :
elle ramène le dense sur les listes, au chiffre près, puis au **bit près** (§ 22).

---

## 20. Contexte et lots : deux réponses, dont une qui n'est pas celle qu'on croit

**Contexte long — le protocole mesurait le cache, pas la qualité.** L'étape fait
varier `--ctx` de 512 à 8 192 en gardant `--limit 256` : la perplexité est donc
**constante par construction** (17,4315), et ce qui varie est l'allocation du
cache KV. Résultat : **RSS 1 248-1 249 Mo pour tous les contextes**, cache KV en
32 bits. Autrement dit, à fenêtre courte, le contexte déclaré ne coûte rien — et
c'est la mesure d'aiguille (§ 9) qui porte la qualité à longue portée, pas
celle-ci. La campagne dit maintenant lequel des deux mesure quoi.

**Lots — ×1,4, et la perplexité ne bouge pas.** Qwen2.5-0.5B, 512 jetons :

| `--lot` | 1 | 2 | 4 | 8 | 16 | 32 | 64 |
|---|---:|---:|---:|---:|---:|---:|---:|
| PPL | 13,1368 | 13,1359 | 13,1359 | 13,1359 | 13,1359 | 13,1359 | 13,1359 |
| tok/s | 16,8 | 18,4 | **23,2** | 23,2 | 21,5 | **23,7** | 13,1 |

**Le lot ne change pas le résultat** (perplexité identique au chiffre près dès le
lot 2) et il apporte **×1,4 de débit** (16,8 → 23,7), avec un plateau de 4 à 32 et
une chute à 64. C'est le même ordre que le ×1,58 du dépôt, mesuré ici sur un
modèle qui tient en RAM — donc **sans le disque**, ce qui est le point : le lot
paie même quand rien n'est lu du disque.

*(Les temps restent mesurés sous charge 66-81 : l'ordre de grandeur est là, la
décimale non.)*

---

## 21. Le noyau, re-mesuré : le croisement est là, et il coûte à densité 1

`drave <modèle>` sans autre argument refait la mesure fondatrice du projet sur le
binaire du jour — Qwen2.5-0.5B, 64 Mo lus, 20 threads, sous charge 44 :

| mesure | valeur |
|---|---|
| bande passante mémoire | **21,5 Go/s** |
| forme listes (push) | 15,88 bits/poids (int8 + listes de rangs) |
| forme dense (pull) | 8,00 bits/poids |
| push, 0 événement | 233 134 matvec/s (**0,004 ms**) · **×0,02** du dense |
| push, 43 560 événements | 40 027 matvec/s · ×0,10 |
| push, 430 359 événements | 10 474 matvec/s · ×0,36 |
| push, 1 076 785 événements | 4 498 matvec/s · ×0,86 |
| push, 2 152 648 événements | 2 473 matvec/s · **×1,54** |
| pull (dense), tous les cas | 3 830-3 875 matvec/s (0,26 ms) |

**Le croisement est entre 1,08 et 2,15 M d'événements**, et il est franc : à vide
les listes sont **50× plus rapides**, à pleine densité **1,5 à 3,2× plus lentes**
(le journal de l'étape retient ×3,19 sur la dernière ligne). Ce n'est pas une
contradiction avec le seuil de 22 % du dépôt : c'est la même courbe, vue en
événements au lieu de la fraction. **Et cela dit pourquoi le chemin dense reste le
défaut sur un modèle dense** : à 71 % de densité (§ 10 ter), on est du mauvais côté
du croisement, d'un facteur 2 à 3.

---

## 22. Les listes ne calculent pas une approximation : les logits sont identiques AU BIT PRÈS

Le résultat qui compte pour l'architecture, et il tient en une commande. Même
modèle (Qwen2.5-0.5B Q8_0), mêmes 7 jetons, `--logits-bin` écrit les logits
`(positions × 151 936)` en f32 ; on compare les fichiers octet par octet :

| chemin | perplexité (7 jetons) | fichier de logits |
|---|---:|---|
| `--push` (listes) | 920,0752 | 4 254 216 octets |
| `--dense` + `DRAVE_SANS_EMPRUNT=1` | **920,0752** | **identique au bit près** ✅ (`cmp`) |
| `--dense` (blocs Q8_0 empruntés) | 795,0325 | divergent (autre encodage des poids) |

**Le chemin par listes n'approxime rien.** À encodage de poids égal, il produit
les **mêmes octets** que le produit scalaire dense — et la même suite de jetons en
décodage glouton (`[3541, 10908, 1134, 14789, 12422, 355, 13, 356]` des deux
côtés, contre `[512, 13309, 321, 1788, …]` pour le dense à blocs empruntés). Ce qui
diffère entre les deux chemins n'est pas le calcul, c'est **ce qu'on a le droit de
sauter** : un poids nul ne contribue rien, donc l'omettre est exact — et c'est
toute l'architecture.

**Deux conséquences pratiques.** 1) Toute comparaison dense/listes doit fixer
`DRAVE_SANS_EMPRUNT=1`, sinon elle mesure deux quantifications (§ 19). 2) Sur un
modèle **4 bits** la question ne se pose même pas : le moteur n'a qu'un chemin
(`DenseQ4`), sans événements — la forme 4 bits ne paie aucun des deux avantages.
C'est un argument de plus pour entraîner des modèles **creux en 8 bits** (§ 5)
plutôt que d'élaguer des modèles 4 bits.

---

## 23. Ce qui reste à mesurer (état de la file, 9 octobre 1 h 45)

**Fait depuis la première rédaction de cette liste** : `parcimonie` (§ 19), `contexte`
et `lot` (§ 20), `routage` (§ 7), `semantique` (§ 18), `noyau` (§ 21), `repartition`
(§ 8 et porte tenue), `portes` (22 vertes, 1 rouge — § 0 ter), `batch 2` (§ 10 ter,
quatre corpus), `batch 3` (§ 9), les paires entraînées (§ 5), l'équivalence bit à
bit (§ 22), la tête restreinte sur gpt-oss (§ 13), le lot à froid avec éviction
(§ 14 bis), et l'acceptation spéculative mesurée par le moteur (§ 1 bis).

**Encore en file — et ce sont des manques, pas des résultats :**

| manque | état exact |
|---|---|
| **embeddings / encodeurs** | `bge-m3` est lisible en en-tête et **inexécutable** : ni attention bidirectionnelle, ni pooling. Le manque le plus net du relevé, et rien ne l'a entamé aujourd'hui |
| **décodage spéculatif** | le taux d'acceptation est mesuré pour deux paires, dont une mal appariée (§ 1 bis) ; les paires **alignées à grande cible** (1,5 B → 14 B, 0,5 B → 14 B) tournent, et c'est là que le rapport de coût peut changer de camp. Aucune ligne de moteur n'est écrite, et c'est délibéré |
| **modèles entraînés creux** | `m7_d384_kwta50` et `m7_d384_kwta25` (k-WTA appris) puis `m8_d384_route_creux` (routé **et** creux) sont en file pour la nuit : la question « la parcimonie doit-elle être imposée ou apprise ? » n'a pas encore de réponse mesurée |
| **échelle du routage** | la courbe s'arrête à dim 384 (−2,6 % à 256, −2,9 % à 384) ; dim 512 est entraîné, sa mesure et sa distillation sont en file |
| **qualité des modèles plus gros que la RAM** | le § 12 ne mesure que **l'existence et le coût** (365,7 Go sur 125 Go). La perplexité publiée pour V4-Flash n'a aucune valeur et c'est écrit |
| **porte gpt-oss de la campagne** | relancée **seule** à 01 h 04 (la première passe a été tuée par son délai sous contention) ; à cache froid, elle demande sa demi-heure |
| **codestral corrigé sur 256 jetons** | le run de contrôle a **expiré** (délai de 1 800 s) sous la contention des autres lecteurs. La valeur publiée reste celle à **63 jetons** (117,91), obtenue avec le binaire corrigé |

**Ce que cette liste dit du reste de la fenêtre** : les trois chaînes de nuit
(`nuit2_m6`, `nuit3_kwta`, `nuit4_route_creux`) sont sérialisées par marqueurs et
occupent le GPU jusqu'au matin ; la mesure de l'acceptation spéculative à grande
cible et la porte gpt-oss occupent le processeur et le disque en attendant. Aucune
de ces files ne peut fausser les autres : elles ne partagent ni les mêmes fichiers,
ni les mêmes répertoires de cache, et les mesures déterministes (perplexité,
identifiants, octets lus) ne dépendent pas de la charge — ce qui n'est pas le cas
des débits, et c'est écrit à chaque fois.
