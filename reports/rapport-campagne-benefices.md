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

## Résumé — les cinq résultats qui comptent, et les manques

*Détail et conditions dans les sections indiquées ; le verdict famille par famille
est au § 0 bis.*

| # | résultat | mesure |
|---|---|---|
| 1 | **Le chemin par listes n'approxime RIEN** | à encodage de poids égal, `--push` et `--dense` produisent des logits **identiques au bit près** (`cmp` sur 4 254 216 octets) et la même suite gloutonne (§ 22) |
| 2 | **La parcimonie doit être APPRISE, pas imposée** | à 25 % gardés : témoin **10,8758** de perplexité, modèle entraîné creux **5,1719** (−52 %) · à 50 % : 5,3032 contre 5,0606 · **chaque modèle n'est bon que dans son régime**, et la distillation ne s'y ajoute pas (−0,3 %) — elle rattrape le routage, pas la parcimonie (§ 5 ter) |
| 3 | **Le routage seul s'inverse à dim 512 — la distillation le rattrape** | routé : −2,6 % (256), −2,9 % (384), **+10 % (512)** · routé **distillé** : **4,3305 contre 4,5686** au dense (−5,2 %), à 12,8 M paires/jeton des deux côtés (§ 5 bis) |
| 4 | **Le brouillon spéculatif paie quand la cible est bornée par le disque** | ×0,70 à 0,210× de coût relatif · ×1,09 à 0,134× · **×1,52 à 0,039×** — c'est le rapport de coût qui décide, pas l'acceptation (§ 1 bis) |
| 5 | **La mémoire tient, et les gros modèles tournent** | **18 aiguilles sur 18** de 512 à **12 288 jetons** (§ 9) · V4-Flash **365,7 Go sur 125 Go de RAM, 37,6 Go résidents** (§ 12) · gpt-oss rend **15,6017**, la valeur attendue au chiffre près (§ 0 ter) |

**Les cinq manques, consignés comme manques** : les **encodeurs** (`bge-m3`
inexécutable), le **noyau Q8 des experts** (un modèle routé ne peut pas être
exécuté en listes), le **lot sur un modèle plus gros que la RAM** (V4.1 refuse le
chemin par lots, et il a raison), le **décodage spéculatif** (aucune ligne de
moteur, et le cahier des charges est mesuré), et la **qualité** des modèles plus
gros que la RAM (coût mesuré, perplexité sans valeur).

**Cinq pièges de méthode ont été trouvés et corrigés** (§ 16, § 17) — dont un
binaire plus vieux que ses correctifs, une porte qui ne pouvait pas passer, et un
cache qui survivait à son correctif. Ils comptent autant que les chiffres : trois
mesures publiées ont été refaites à cause d'eux.

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
| **contexte long — la mémoire** | ✅ **elle tient, et plus loin qu'annoncé** | **18 aiguilles sur 18** retrouvées, de 512 à **12 288 jetons**, à 10 %, 50 % et 90 % de profondeur (§ 9) |
| **contexte long — le coût** | ✅ réglable | KV int8 : +1,5 % (512 j.) à +3,0 % (8 192 j.) · paginé : **0,03 Go au lieu de 25,77 Go** à 1 M |
| **préremplissage par lots** | ✅ ×1,4 en RAM, ⚠️ disque non testé | 0,5 B, 512 jetons : **16,8 → 23,7 tok/s** et PPL **identique** (13,1368 → 13,1359) · sur le 30B le lot n'a lu que le **cache de pages** (10,9 Go à froid, 0 ensuite) |
| **code** | ✅ mesuré, décalage de tâche | codestral-22B : **133,08** de PPL sur de la prose (255 jetons) = **1,842 bit/octet**, contre **0,983** pour un 0,5 B — un 22 B **1,87× pire** qu'un 0,5 B hors de sa tâche |
| **raisonnement** | ✅ mesuré, contre-intuitif | r1-distill-1.5B : **1,326 bit/octet**, **2,7× pire** que le 0,5 B (0,983) |
| **MoE / routage d'experts** | ✅ mesuré | 4 experts sur 128 (3,1 %) · déséquilibre **×3,90** · **847 octets** par jeton à router |
| **multilingue (399 langues)** | ✅ mesuré, et c'est le point faible du modèle | **3,227 bit/octet** contre 0,951 en prose — **3,4× pire** · densité **identique** (71 %) · seuil absolu : PPL **×11**, le k-WTA tient (§ 10 ter) |
| **sémantique multilingue** | ✅ le résultat publié **survit** au correctif d'échelle | pic de séparation à la **couche 13** (+0,0391) sur 398 langues, bande 10-15 — et l'ancien lecteur donnait +0,0349 au même endroit |
| **parcimonie imposée** | ✅ reproduit, et nuancé | à −30 % d'événements : seuil **+69 %** de PPL, k-WTA **+4 %** (facteur 17) · en dense, **aucune lecture économisée** |
| **parcimonie APPRISE** | ✅ **la réponse qui décide** — et elle est nette | à 50 % gardés : témoin **5,3032**, `kwta050` **5,0606 (−4,6 %)** · à 25 % : témoin **10,8758**, `kwta025` **5,1719 (−52 %)** · **chaque modèle n'est bon que dans son régime** · à dim 512 la recette tient (**6,0503 → 4,9649**, lecture ÷4) — mais le débit ne distingue plus listes et dense (213 contre 211 tok/s) : **le modèle tient dans les caches, les lectures économisées étaient gratuites** (§ 5 ter) |
| **sortie contrainte** | ✅ **gagne par construction** | **×1,36-1,42** de débit *et* garantie que la sortie appartient à l'ensemble autorisé |
| **modèle plus gros que la RAM** | ✅ **démontré, et vérifié au chiffre près** | V4-Flash **365,7 Go sur 125 Go de RAM** : **37,6 Go résidents**, 37,7 Go lus, 266 s pour 16 jetons · gpt-oss (63 Go) : **PPL 15,6017 sur 510 jetons — la valeur attendue, à l'identique** (porte tenue à 02 h 58) |
| **répartition à deux nœuds** | ✅ **porte tenue** | écart **0,0000 %** et flux **0,00e0** — sur le modèle dense, routé **et distillé** |
| **embeddings / recherche** | ❌ **manque** | `bge-m3` lisible en en-tête, **inexécutable** (ni encodeur bidirectionnel ni pooling) |
| **décodage spéculatif** | ⚠️ **le chantier n'existe pas, mais le gain est démontré dans la niche du projet** | trois paires mesurées par le moteur : ×0,70 (brouillon à 0,21×) · ×1,09 (0,13×) · **×1,52 pour un brouillon à 0,039× de sa cible** — c'est le **rapport de coût** qui décide, et il est minimal quand la cible est bornée par le disque (§ 1 bis) |
| **routage à l'échelle** | ⚠️ **le routage seul s'inverse à dim 512, la distillation le rattrape et dépasse** | routé seul : −3,5 % (val, 256) → −1,4 % (384) → **+1,4 % (512)** · **routé distillé : 4,3305 contre 4,5686 au dense (−5,2 %)**, le gain du distillat croissant avec la taille (−2,5 % → −9,3 % → **−13,8 %**) · **12,8 M paires/jeton des deux côtés** |
| **structure innée** | ✅ **le masque aléatoire coûte 1 % et divise les lectures par 4** | connectome tiré à la naissance (25 % des connexions, jamais modifié) : **5,0472** contre 4,9959 au témoin dense, **81,6 M** d'événements/fenêtre contre 336,7 M, **276** tok/s contre 131 (§ 4 bis de `biologie-pour-drave.md`) |
| **fidélité listes ↔ dense** | ✅ **exacte, démontrée** | logits identiques **au bit près** (`cmp` sur 4 254 216 octets) et mêmes jetons gloutons, à encodage de poids égal ; ×0,02 à ×3,19 selon la densité |

**En une phrase** : Drave gagne **par construction** sur les sorties contraintes,
**par sa structure** quand le modèle est creux — mais seulement aux petites
échelles : le routage entraîné rend −2,6 % à dim 256 et −2,9 % à dim 384, puis
**+10 % (il perd) à dim 512**, à lecture égale (12,8 M paires/jeton des deux côtés,
§ 5 bis) — **par ses circonstances** sur les modèles plus gros que la RAM, et
**perd** sur un modèle dense ordinaire, où le chemin par listes coûte 1,8 à 2,1×
pour rien.

**Trois documents accompagnent ce rapport** : `docs/modele-pour-drave.md` (quel
modèle *ad hoc* l'architecture récompense — moteur contre modèle, dix dessins
évalués), `docs/biologie-pour-drave.md` (ce que les connectomes imposent comme
contraintes, et l'expérience E1 mesurée) et `docs/impulsion-pure-apprenant.md` (un
exécutant événementiel n'est pas encore un apprenant événementiel, et pourquoi).

**Quatre corrections de méthode sont consignées dans ce rapport**, et elles
comptent autant que les chiffres : le tokenizer étranger (`data/…ids`, facteur
442), la fenêtre d'évaluation trop courte (trois protocoles, trois réponses), le
cache qui survit à son correctif, et le **binaire plus vieux que ses correctifs**
— trois commits de `drave-core/src` n'étaient pas dans le binaire qui a mesuré la
campagne (§ 17).

### 0 ter. L'état de la campagne au 9 octobre, 1 h 05

Les **neuf étapes** de `tools/campagne-benefices.sh` sont allées au bout
(`=== campagne terminée ===` à 01 h 03), et les portes rendent **22 vertes · 1
rouge** — puis, à 02 h 58, **23 vertes · 0 rouge**.

| porte | état | ce qui s'est passé |
|---|---|---|
| `gpt-oss-120b MXFP4 ctx 256` — attendu **15.6017** | ✅ **rend 15.6017 sur 510 jetons**, au chiffre près | elle avait expiré **deux fois** (2 400 s puis 5 400 s). Le délai était en cause, pas le moteur : à 0,074 tok/s mesuré (32 jetons en 432 s), 512 jetons demandent ~1 h 55. Délai recalibré (`GATE_GPTOSS_DELAI`, défaut 9 000 s) ; relancée seule, elle rend la valeur **attendue à l'identique** |

Tout le reste est vert, y compris `cargo test --release` (**77 tests**), les 17
formats confrontés à libggml, la porte de correction contre llama.cpp
(100 % des positions utiles au-dessus de 0,95, top-1 94,4 %), la porte Mistral, et
les cinq modes de découpage à deux nœuds (écart **0,00e0** pour les modes 0, 1 et
3, 3,65e-2 pour le mode 2, 4,45e-3 pour le mode 4).

**Ce que cette porte dit vraiment** : le moteur reproduit **au chiffre près** la
perplexité de référence d'un modèle de 63 Go en MXFP4, exécuté en dense, sur le
disque. C'est la vérification la plus lourde du dépôt, et elle ne tenait qu'à un
délai mal calibré — une porte qui ne peut pas passer ne vérifie rien, et celle-ci
était dans ce cas depuis sa mise en service.

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
famille mais d'une autre recette ne propose rien d'acceptable — et un brouillon
rejeté coûte plus qu'il ne rapporte.

**La paire ALIGNÉE, mesurée le 9 octobre** (brouillon R1-distill-1,5 B → cible
R1-distill-14 B : même famille, même distillation, même tokenizer, 8 invites de
48 jetons) :

| mesure | paire alignée (1,5 B → 14 B) | paire mal appariée (0,5 B → 1,5 B) |
|---|---:|---:|
| acceptation moyenne | **1,25 jeton sur 8 (15,6 %)** | 0,88 sur 8 (11 %) |
| P(préfixe ≥ 1 / 2 / 8) | 38 % · 12 % · 12 % | 38 % · 12 % · 0 % |
| coût relatif du brouillon | **0,134×** (7,05 vs 0,95 tok/s) | 0,210× |
| **gain net attendu** | **×1,09** | ×0,70 |

**L'alignement aide, mais il ne suffit pas** : 15,6 % au lieu de 11 %, et un gain
net qui passe de ×0,70 (il coûte) à ×1,09 (il ne rapporte presque rien). Le
brouillon ne coûte pourtant qu'un dixième de la cible — c'est bien
**l'acceptation** qui plafonne, pas l'économie de calcul.

**Une réserve, et elle est de taille** : cette acceptation est la borne **gloutonne**
(`--temp 0`), le critère le plus sévère possible — il exige que le brouillon
choisisse *exactement* l'argmax de la cible à chaque position. Le décodage
spéculatif réel échantillonne et accepte selon un rapport de probabilités : son
taux est **plus élevé** que celui-ci. Ce qui est mesuré ici est donc un plancher,
et il dit déjà que la version gloutonne ne paie pas.

**Et la troisième paire renverse le verdict — mais pas par l'acceptation.** Un
brouillon **minuscule** (Qwen2.5-0.5B Q8, 0,53 Go) pour la **même grande cible**
(R1-14B, 9 Go) :

| paire | acceptation | **coût relatif du brouillon** | gain net |
|---|---:|---:|---:|
| 0,5 B → 1,5 B | 11 % | 0,210× | **×0,70** (il coûte) |
| 1,5 B → 14 B (même recette) | 15,6 % | 0,134× | ×1,09 |
| **0,5 B → 14 B** | 12,5 % | **0,039×** | **×1,52** |

**C'est le RAPPORT DE COÛT qui décide, pas l'acceptation.** Avec un brouillon qui
coûte 4 % de sa cible, accepter un jeton sur huit suffit à gagner 1,5× — et cette
paire est la *moins* bien appariée des trois. À l'inverse, la paire la mieux
appariée (1,5 B → 14 B) ne rapporte que ×1,09 parce que son brouillon coûte 13 %.

**Et c'est exactement le régime que Drave vise** : quand la cible est plus grosse
que la RAM, elle est bornée par le **disque**, et le brouillon — qui tient en
mémoire — devient relativement gratuit. Le décodage spéculatif n'est donc pas mort
(§ 1) : il est **intéressant précisément là où le modèle cible ne tient pas en
mémoire**, ce qui est la niche du projet.

**Quatre réserves, toutes mesurées ou nommées :**
1. l'acceptation est la borne **gloutonne** (la plus sévère) ; le décodage réel
   échantillonne et accepte davantage ;
2. le coût relatif dépend de la charge (26,93 vs 1,05 tok/s ici) — c'est un ordre
   de grandeur, pas une constante ;
3. vérifier k jetons d'un coup demande le **préremplissage par lots** sur la cible,
   qui existe (`--lot`) mais n'est pas branché sur le décodage ;
4. la mémoire du brouillon s'ajoute : 0,53 Go pour un 0,5 B, à côté d'une cible de
   9 à 63 Go, c'est négligeable — mais ce n'est pas zéro.

**Ce qu'il faudrait pour aller plus loin** : un brouillon entraîné *sur les sorties
de sa cible* (distillation croisée, ou tête Eagle3 branchée sur les états cachés de
la cible). Les trois mesures donnent le cahier des charges : à 0,04× de coût
relatif, accepter 25 % à k = 8 donnerait **×2,0**.

*(Le taux d'acceptation est déterministe — `--temp 0` — donc exact malgré la
charge ; le coût relatif, lui, dépend de la charge et n'est qu'un ordre de
grandeur : 0,210 ici contre 0,245 en § 1 pour la même paire de tailles.)*

---

## 2. Les deux familles de tâches que Drave ne couvre pas

Constatées, et consignées comme manques — pas comme résultats :

| famille | état | ce qui manque |
|---|---|---|
| **embeddings / recherche** | `bge-m3` (BERT, 24 couches, vocab 250 002) est **lisible en en-tête** mais **inexécutable** | le moteur exige `blk.0.attn_norm.weight` et une attention causale ; il n'a ni encodeur bidirectionnel ni pooling |
| **décodage spéculatif** | `eagle3-gpt-oss-120b` (0,84 Go, 1 couche) présent sur le disque | aucune notion de brouillon dans le moteur (`grep eagle brouillon specul` = 0) — et la mesure par le moteur (§ 1 bis) ajoute une condition que le code ne peut pas lever : **le brouillon doit partager le post-entraînement de sa cible**, sinon il n'accepte rien (0,88 jeton sur 8). Le chantier commence par un entraînement, pas par une option |

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
| codestral-22B Q4_K_M | **133,08** ✅ *(tokenizer corrigé, 255 j.)* | **1,842** | — | 63,6 Go | 11,3 Go | 35 657 avant correctif · 117,91 sur 63 jetons |
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
même mesure donne **133,08** sur 255 jetons — soit **1,842 bit/octet**, contre
**0,983** pour un Qwen2.5-0.5B sur le même texte. *(Le chiffre publié plus tôt,
117,91, portait sur 63 jetons seulement ; la ligne de la grille est maintenant
mesurée au même protocole que les autres — 256 jetons, contexte 256 — et c'est
cette valeur qui vaut. Le rapport est corrigé, pas complété.)*

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

## 5. Les modèles entraînés ici, mesurés DANS le moteur — ce que le routage et la distillation rapportent

**Le protocole, et il a fallu le corriger** — et la courbe de ce paragraphe
**s'inverse à dim 512**, ce que le § 5 bis mesure. Le moteur évalue une fenêtre contiguë
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

**Un manque mesuré, découvert en préparant l'expérience « routé ET creux »** : le
chargeur d'experts n'accepte que les formats à noyau dédié (Q4_K, Q6_K, MXFP4,
Q4_0) et les super-blocs de 256 poids (`list::sans_noyau`). Un tenseur d'experts en
**Q8_0 — le seul format qui donne accès au chemin par listes** — est refusé :

    [moe] couche 0 : « blk.0.ffn_gate_exps.weight » de type Q8_0
          — format sans noyau ni déquantification

**Conséquence, et elle est structurelle** : aujourd'hui, **un modèle routé ne peut
pas être exécuté en listes**. Le routage économise des *experts*, pas des
*événements* ; la parcimonie d'activation, qui est ce que les listes exploitent, ne
peut pas s'appliquer aux experts. C'est la limite la plus nette du moteur pour la
thèse « routage + événements », et elle tient en une ligne de format.

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

**Et la distillation renverse le renversement.** Le distillat du routé 512 a été
entraîné et mesuré dans la nuit (professeur : le dense 512, mêmes 40 000 pas) :

| dim | dense | routé | **routé distillé** | gain du distillat sur son jumeau routé |
|---:|---:|---:|---:|---:|
| 256 | 5,0155 | 4,8858 | **4,7642** | −2,5 % |
| 384 | 5,0108 | 4,8646 | **4,4113** | −9,3 % |
| **512** | 4,5686 | 5,0255 | **4,3305** | **−13,8 %** |

**Le gain de la distillation croît avec la taille : −2,5 %, −9,3 %, −13,8 %**, et
il est assez grand à dim 512 pour compenser un routage qui, seul, perdait 10 %.
Le modèle produit ici est donc **5,2 % meilleur que son jumeau dense à lecture
égale** (12,8 M paires par jeton de part et d'autre, vérifié par le compteur du
moteur) — alors que sa partie routée seule était 10 % pire.

**Et l'hypothèse « sous-entraîné » a été testée — elle est vraie en fp32, fausse
après export.** Le même routé 512, entraîné **80 000 pas** au lieu de 40 000 :

| routé 512 | validation fp32 (bits/octet) | PPL moteur (8 × 128) | écart de quantification |
|---|---:|---:|---:|
| 40 000 pas | 1,8843 | 5,0255 | **+0,445 bit/octet** |
| **80 000 pas** | **1,8237** ✅ meilleur | **5,3845** ❌ pire | **+0,605 bit/octet** |

**Deux fois plus d'entraînement améliore le modèle en fp32 (1,8237 — mieux que son
jumeau dense, 1,8580) et le dégrade après quantification.** L'écart entre les deux
est le prix de l'export en Q4_0, et il **croît avec l'entraînement** : +0,445 puis
+0,605 bit/octet, soit +36 %. Le chiffre du moteur est fidèle — la porte de
correction a été passée sur ce modèle (corrélation des logits **0,9998**, 100 % des
positions utiles au-dessus de 0,95, top-1 98,4 %).

**Ce que cela change dans la façon de choisir un modèle** : le format d'export fait
partie de la spécification. Un modèle entraîné plus longtemps n'est pas « meilleur »
en Drave si sa quantification coûte davantage — et c'est exactement l'argument du
dessin (J) de `docs/modele-pour-drave.md` : entraîner *pour* la grille dans laquelle
on exécutera. *(Ce modèle ne peut d'ailleurs pas être testé en 8 bits : le chargeur
d'experts refuse Q8_0 et F16 — les experts d'un MoE n'ont aujourd'hui que des
formats 4 bits.)*

**La recette qui sort de cette courbe est donc « router ET distiller »**, pas
« router » — et c'est la distillation, pas le routage, qui porte le gain aux
grandes échelles. Le mécanisme reste à expliquer (l'hypothèse la plus simple :
un élève à experts multiples profite beaucoup plus d'une cible dense que d'un
objectif d'argmax, parce que chaque expert voit moins d'exemples) — c'est une
hypothèse, pas une mesure, et elle est notée comme telle.

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

### 5 ter. La parcimonie : IMPOSÉE ou APPRISE ? La réponse est mesurée, et elle est nette

C'est **la** question de l'architecture événementielle sur un modèle dense, et elle
n'avait pas de réponse. Trois modèles **identiques par ailleurs** (dim 384, 4
couches, 6 têtes, FFN 1152, 40 000 pas, mêmes données, FFN exportée en Q8 pour que
le chemin par listes existe) :

- **témoin** : entraîné normalement, puis creusé à l'exécution (`--act-topk`) ;
- **`m7_d384_kwta050`** : entraîné **avec** le k-WTA à 50 % gardés ;
- **`m7_d384_kwta025`** : entraîné **avec** le k-WTA à 25 % gardés.

Le k-WTA d'entraînement est appliqué sur l'entrée de **toutes les couches
linéaires** — exactement l'opération que `--act-topk` impose ensuite. Protocole de
record : huit fenêtres de 128 jetons, moyennées en log, chemin par listes.

| modèle | entraîné à | aucune parcimonie | **50 % gardé** | **25 % gardé** |
|---|---|---:|---:|---:|
| **témoin** (creusé à l'exécution) | — | **4,9959** | 5,3032 (+6,2 %) | 10,8758 (**+118 %**) |
| **`kwta050`** | 50 % | 5,1858 | **5,0606 (−4,6 %)** | 5,7666 |
| **`kwta025`** | 25 % | 6,4282 | 5,8131 | **5,1719 (−52 %)** |
| événements/fenêtre | | 336 M | 168 M | 84 M |

*(Les pourcentages entre parenthèses sont l'écart au témoin **au même taux de
parcimonie**, qui est la seule comparaison juste.)*

**Quatre conclusions, et la dernière est la recette.**

1. **Apprise, la parcimonie ne coûte RIEN** : à 50 % gardés, `kwta050` fait
   *mieux* qu'en dense (5,0606 contre 5,1858), là où le témoin perd 6,2 %. Et à
   taux égal il est **4,6 % meilleur** que le témoin — pour moitié moins de
   lectures.
2. **À 25 %, l'écart devient un gouffre** : 5,1719 contre **10,8758**, soit
   **−52 %**. Ce qu'un modèle dense ordinaire ne supporte pas (un quart des
   activations), un modèle entraîné pour ça le supporte presque sans perte
   (6,4282 en dense → 5,1719 à 25 %, c'est-à-dire *mieux* creux que dense).
3. **Chaque modèle est meilleur dans SON régime** : `kwta050` gagne à 50 %
   (5,0606) et perd à 25 % (5,7666) ; `kwta025` gagne à 25 % (5,1719) et perd à
   50 % (5,8131). Il n'y a pas de modèle creux « universel » : **il faut
   l'entraîner au taux où on va l'exécuter**.
4. **La lecture suit exactement le taux, et le débit suit la lecture** : 336 M →
   168 M → 84 M d'événements par fenêtre, et le débit du chemin par listes monte de
   **~90 tok/s (dense) à ~143 (50 %) puis ~205 (25 %)** — soit **×1,6 et ×2,3**.
   La parcimonie n'est pas un artifice de comptage : elle réduit les paires lues,
   et le temps suit.

**C'est la recette du modèle nativement événementiel** : on n'élague pas un modèle
après coup, on l'entraîne à vivre creux, et on l'exécute **au taux où il a appris**
— ce que `--act-topk` sait faire. Le gain mesuré au taux de 25 % est de **×2 en
perplexité** (10,88 → 5,17) pour **quatre fois moins de paires lues**.

**La recette tient à l'échelle 512** — mêmes 40 000 pas, même témoin dense 512,
mêmes mesures (8 × 128) :

| `m8_d512_kwta25` (entraîné à 25 %) | aucune parcimonie | 50 % | **25 %** | 12,5 % | **chemin DENSE à 25 %** |
|---|---:|---:|---:|---:|---:|
| perplexité | 6,0503 | 5,5526 | **4,9649** | 5,3248 | 4,9011 |
| événements/fenêtre | 594,8 M | 299,2 M | **149,6 M** | 74,8 M | 0 |
| débit (tok/s) | 89,1 | 132,1 | **213,2** | 282,2 | **211,3** |

**Deux choses, dont une qui nuance la thèse.**

1. **La qualité suit la même loi qu'à dim 384** : le modèle est meilleur **creux que
   dense** (4,9649 à 25 % contre 6,0503 sans), et il perd 7 % quand on le pousse à
   12,5 %, deux fois plus creux que ce qu'il a appris. La lecture suit : 594,8 →
   149,6 M d'événements (÷4), et le débit monte de 89 à **213 tok/s**.
2. **Le temps, lui, ne distingue PLUS les deux chemins à cette échelle** : à top-k
   25 %, le chemin par listes fait 213,2 tok/s et le chemin **dense** 211,3 — égalité.
   La raison est mesurable : à 12,7 M paramètres, ce modèle tient dans les caches du
   processeur, donc **les lectures que les listes économisent étaient déjà
   gratuites**. L'avantage du chemin par listes est un avantage de **bande
   passante**, et il ne se voit que quand le modèle ne tient plus dans les caches —
   c'est-à-dire pas à cette échelle. *(Les deux chemins ne calculent pas exactement
   la même chose : l'écart de 1,3 % de perplexité entre 4,9649 et 4,9011 vient de
   l'encodage des poids, comme au § 22, pas de la parcimonie.)*

**La carte des taux est complète** (troisième point, `m10_d384_kwta125`, entraîné
à 12,5 % gardés — mêmes 40 000 pas, même témoin) :

| modèle (dim 384) | entraîné à | exécuté à | perplexité | événements/fenêtre |
|---|---|---:|---:|---:|
| témoin | — | 25 % | 10,8758 | 84 M |
| `kwta050` | 50 % | **50 %** | **5,0606** | 168 M |
| `kwta025` | 25 % | **25 %** | **5,1719** | 84 M |
| **`kwta125`** | 12,5 % | **12,5 %** | **5,5973** | **42 M** |

**Chaque division par deux des événements coûte 2 % puis 8 % de perplexité**
(5,0606 → 5,1719 → 5,5973) — alors que le même exercice imposé au témoin le fait
s'effondrer (+118 % à 25 %). La courbe de la parcimonie **apprise** est plate là où
la courbe imposée est verticale. À 42 M d'événements par fenêtre, on lit **seize
fois moins** que le témoin sans parcimonie (672 M) pour une perplexité de 5,60
contre 4,996 — soit **+12 % de perplexité pour ÷16 de lecture**, et le chemin par
listes y est environ deux fois plus rapide qu'à 50 %.

### 5 quater. La courbe lecture ↔ qualité, et la réponse finale

Cinq modèles **identiques par ailleurs** (dim 384, 4 couches, 40 000 pas, mêmes
données, FFN exportée en Q8), mesurés au protocole de record. La colonne « paires »
est celle de la fenêtre 8 (même préfixe pour tous, donc comparable) :

| modèle | ce qui est creux | perplexité | **paires/jeton** | lectures |
|---|---|---:|---:|---:|
| `m5_d384_dense` | rien (témoin) | **4,9959** | 21,1 M | — |
| **`m12` structure innée 25 %** (aléatoire, figée) | poids seuls, **imposés** | **5,0472** (+1,0 %) | **5,2 M** | ÷4,1 |
| **`m7` k-WTA 25 % appris** | activations, **apprises** | **5,1719** (+3,5 %) | **5,4 M** | ÷3,9 |
| **`m11` k-WTA 25 % + élagage 50 % appris** | **les deux, appris** | **5,1866** (+3,8 %) | **2,7 M** | **÷7,8** |
| `m15` masque inné 25 % + k-WTA 25 % | les deux, dont un imposé | 6,0792 (+21,7 %) | **1,4 M** | ÷15,1 |

**Trois lectures, et la troisième est la réponse.**

1. **Un seul axe suffit à diviser les lectures par quatre** — et il coûte 1 % quand il
   est **structurel** (masque inné) contre 3,5 % quand il est **d'activations**
   (k-WTA). La structure innée est le moins cher des deux.
2. **Les deux axes appris se cumulent presque gratuitement** : ÷7,8 lectures pour
   +3,8 % de perplexité (le second axe n'ajoute que 0,3 point).
3. **Imposer un axe coûte cher** : la même combinaison, mais avec la structure
   *imposée* au lieu d'apprise, passe de +3,8 % à **+21,7 %** de perplexité. À
   ÷15 lectures, le modèle imposé paie cinq fois plus que le modèle appris à ÷8.

**La réponse à « quel modèle pour Drave ? » est donc une courbe, pas un chiffre** :
**÷4 pour +1 %** (structure innée), **÷8 pour +4 %** (les deux axes appris),
**÷15 pour +22 %** (un axe imposé). Le point de fonctionnement se choisit ; il ne se
subit pas — et c'est exactement ce qu'une architecture événementielle permet de faire
pour la première fois : **borner le coût à la conception**.

**Et les deux axes SE CUMULENT quand les deux sont appris** (9 octobre, 11 h 32) :
`m11_d384_kwta25_elag50` reprend exactement `kwta025` (dim 384, 40 000 pas) **plus un
élagage appris à 50 %** des poids par ligne — même règle que `--keep`, appliquée
pendant l'entraînement à rampe cubique.

| dim 384 | aucune parcimonie | 50 % d'activations | **25 % d'activations** |
|---|---|---|---|
| `kwta025` (activations seules) | 6,4282 · 335,3 M | 5,8131 · 168,3 M | 5,1719 · **84,2 M** |
| **+ poids élagués APRIS (50 %)** | **6,0422 · 165,9 M** | **5,6842 · 84,7 M** | **5,1866 · 42,2 M** |
| écart | **−6,0 %** | −2,2 % | **+0,3 %** |

**Les lectures sont divisées par deux à chaque point de fonctionnement, et la
perplexité ne bouge pas** (5,1866 contre 5,1719 à 25 % d'activations, soit +0,3 %) —
elle s'améliore même en dense (−6,0 %). Cumulé avec la parcimonie d'activation, le
modèle lit **huit fois moins** que le témoin sans parcimonie (42,2 M contre 336 M
d'événements par fenêtre) pour une perplexité comparable.

**C'est la réponse à « quel modèle pour Drave ? »** : entraîné creux **sur les deux
axes** — activations (~25 %) et poids (~50 %) — plutôt que sur un seul.

**Les deux leviers ne se cumulent PAS** — mesuré le 9 octobre à 7 h 20. Un
quatrième modèle, `m9_d384_kwta25_distille`, reprend **exactement** la recette de
`kwta025` (dim 384, 40 000 pas, k-WTA 25 %) **plus** la distillation de l'enseignant
dense 384 — le levier qui vaut −13,8 % sur un modèle routé (§ 5 bis) :

| dim 384 | aucune parcimonie | 50 % | **25 %** |
|---|---:|---:|---:|
| `kwta025` (creux seul) | 6,4282 | 5,8131 | **5,1719** |
| **`kwta025` + distillé** | 6,3684 | 5,6770 | **5,1553** |
| **gain de la distillation** | −0,9 % | −2,3 % | **−0,3 %** |

**La distillation n'ajoute presque rien au creux appris.** Son gain, qui croît avec
l'échelle sur un modèle routé, valait −2,5 % (256), −9,3 % (384), −13,8 % (512) —
et ici, à dim 384 sur un modèle **dense** entraîné creux, il tombe à **−0,3 %**.

**Ce que cela dit** : les deux leviers ne traitent pas le même handicap. La
distillation rattrape ce que le **routage** coûte (chaque expert voit moins
d'exemples) ; elle n'a rien à rattraper sur un modèle dense, même creusé, où le
k-WTA ne fait que réduire le nombre d'activations sans retirer de capacité. Les
deux recettes sont donc **complémentaires par leur objet, pas additives par leur
effet** — et c'est mesuré, pas supposé.

**Ce que cela ne dit pas** : la plage de taux qu'un même modèle supporte. Les trois
modèles entraînés perdent hors de leur régime (0,4 à 1,4 point de perplexité), donc
la réponse est étroite — c'est un résultat, pas une réserve de politesse.

---

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

### 8 bis. La carte de latence : à partir de quand un réseau coûte plus que le calcul

Le découpage à deux nœuds est exact sur localhost (écart 0,00e0). Mais localhost
est un plancher optimiste : ce qui décide, sur un vrai réseau, n'est pas le débit
(0,25 Mbit/s de flux) mais **la latence par message**. `tools/proxy_latence.py`
est un relais TCP qui ajoute un délai réglable ; `tools/carte_latence.sh`
l'intercale entre le pilote et le nœud et refait la mesure pour chaque délai.
Modèle entraîné ici, 4 couches dont **2 locales** (donc deux frontières franchies
par jeton), 128 jetons :

| latence ajoutée par message | m5_d384 (44 M) | m6_d512 (79 M) | perplexité |
|---:|---:|---:|---|
| 0 ms (localhost) | ×5,32 | ×3,49 | **3,5140 / 3,6064** |
| +1 ms | ×6,31 | ×4,99 | identique |
| +2 ms | ×7,97 | ×11,47 | identique |
| +5 ms | ×12,96 | ×10,97 | identique |
| +10 ms | ×18,94 | ×17,71 | identique |
| +20 ms | ×37,54 | ×28,18 | identique |
| +50 ms | ×79,73 | ×56,11 | identique |

**La perplexité ne bouge PAS d'un chiffre à 50 ms de latence par message** : le
transport est exact quelle que soit la latence, et c'est la seule chose que le
découpage doit garantir.

**Le temps, lui, croît linéairement** — et la pente donne la règle :
**≈ 3,4 ms de plus par jeton pour chaque milliseconde d'aller-retour** (44 M) et
**3,3 ms** (79 M), soit ≈ 0,85 ms par jeton et par frontière et par ms de RTT.
*(Les valeurs individuelles portent le bruit de charge de la machine — un point
isolé de la colonne 79 M sort de la monotonie — mais les deux extrémités de chaque
série sont mesurées à quelques minutes d'intervalle, et c'est la pente entre elles
qui est retenue.)*
Le plancher localhost, lui, est de **×3,5 à ×5,3** : à ces tailles, un processus
unique gagne toujours.

**La règle qui en sort, et elle est utilisable** : répartir ne paie que si le
calcul local par jeton dépasse ≈ **3,4 ms × RTT**. Concrètement : sur un réseau
local à 0,2 ms, il faut un modèle plus lent que ~0,7 ms/jeton (soit ~1 400 tok/s) —
tout gagne ; sur un lien à 1 ms, il faut plus de 3,4 ms/jeton (moins de 300 tok/s),
et un 0,5 B à 34 ms/jeton est largement au-dessus ; sur un lien à 20 ms, il faut
plus de 68 ms/jeton, soit un modèle **plus lent que 15 tok/s** — c'est le cas d'un
14 B en Q4 sur cette machine (0,5 à 9 tok/s), et **pas** d'un 0,5 B.

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
modèle de 0,5 B.

**Étendu à 8 192 puis 12 288 jetons le 9 octobre** (`--n 24`, lot de
préremplissage 256, `temp 0`, remplissage `wikitext2_test.txt`, fenêtres décalées,
l'outil confirme « 2 fenêtres distinctes sur 2 sondes ») :

| longueur | profondeur 10 % | 50 % | 90 % | durées |
|---|---:|---:|---:|---:|
| 8 192 jetons | ✅ (7 963 j.) | ✅ (9 224 j.) | ✅ (8 033 j.) | 935 / 1 199 / 954 s |
| 12 288 jetons | ✅ (11 857 j.) | ✅ (12 474 j.) | ✅ (12 601 j.) | 1 815 / 1 964 / 2 055 s |

**18 sondes sur 18 retrouvent le code**, et la portée **triple** (12 288 au lieu de
4 096) sans qu'une seule échoue. C'est la mesure de tâche qui porte la
revendication « contexte long » — la perplexité moyenne, elle, ne dit rien de la
mémoire (§ 20), et le cache KV ne détruit pas l'information jusqu'à 12 288 jetons.

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

### 12 bis. Le débit de lecture RÉEL : 8 Mo/s sur disque dur, 140-300 Mo/s sur NVMe

Le § 12 démontre qu'un modèle plus gros que la RAM **tourne**. Il ne dit pas à
quelle vitesse il *lit*, et c'est la question qui décide de l'usage. Mesuré le
9 octobre, machine au calme :

| disque | débit séquentiel (`dd` direct) | débit du moteur (mmap, page faults) | rapport |
|---|---:|---:|---:|
| **disque dur** (`sda`, modèles gguf) | **243 Mo/s** | **8,6 Mo/s** | **÷28** |
| **NVMe** (V4.1, 365 Go) | 1 600 Mo/s (mesuré au dépôt) | **140 à 300 Mo/s** | ÷5 à ÷11 |

**Le même moteur, le même code de lecture, deux comportements opposés** : sur NVMe,
les défauts de page coûtent peu et le streaming tient 140-300 Mo/s ; sur un disque
dur, une lecture aléatoire de 4 Ko coûte ~5 ms, soit ~2 000 IOPS et **8 Mo/s** —
vingt-huit fois moins que ce que le disque sait faire en séquentiel.

**Ce que cela explique, et ce que cela change** : les 90 minutes qu'une passe de
256 jetons met sur gpt-oss (§ 3), les 6,6 Mo/s du § 12, et le fait que le codestral
(13 Go) demande 25 minutes pour être lu. **Le facteur limitant n'est pas le moteur,
c'est le disque** — et sur un disque dur, la niche « modèle plus gros que la RAM »
se paie en heures, pas en minutes. Sur NVMe elle se paie en minutes. *(La
conséquence pratique est un préchargement séquentiel — `madvise(WILLNEED)` ou une
lecture ordonnée des experts — qui n'est pas implémenté ; c'est un manque, pas une
mesure.)*

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

**Et le seul modèle plus gros que la RAM REFUSE le lot — explicitement.** Restait à
faire la mesure dans le régime où le lot devrait le plus payer : V4.1-Flash,
365,7 Go sur 125 Go. Mesure à `--lot 1` d'abord : **39 216 Mio lus**, 129 s.
Puis `--lot 16` :

    chemin par LOTS et hyper-connexions : ce chemin n'est pas porté (le résidu y est
    additionné au lieu d'être remélangé par `hc_post`) — utilisez `--lot 1`, ou
    implémentez-le. Le lot n'est pas neutre ici : il change le modèle

**Le moteur refuse plutôt que de rendre un chiffre faux**, et il dit pourquoi : sur
un modèle à hyper-connexions, une passe par lots additionnerait le résidu au lieu
de le remélanger, donc **ce n'est pas le même modèle** qui serait mesuré. C'est le
comportement voulu, et c'est le seul résultat possible aujourd'hui : **le seul
modèle plus gros que la RAM de cette machine ne peut pas être exécuté par lots**.
La question « le lot amortit-il les lectures du disque quand le modèle ne tient
pas en mémoire » reste donc **ouverte**, et ce n'est pas un oubli : c'est un
chemin de code qui n'existe pas (le § 23 le porte comme manque).

---

## 16. Deux pièges de méthode, consignés

**Un cache qui survit à son correctif.** La mesure sémantique avec l'échelle
corrigée a d'abord rendu **exactement les chiffres publiés** (couche 0 : +0,0002 ;
couche 4 : +0,0156) — parce que le cache de vecteurs de `/tmp` datait de la
session précédente, **avant** le correctif du lecteur. Un cache qui ne porte pas
la version de l'outil qui l'a écrit fait mesurer l'ancien code avec le nouveau :
les fichiers ont été supprimés et la comparaison relancée à caches neufs.

**Une chaîne qui attend son marqueur dans le mauvais journal.** Les chaînes de
nuit sont sérialisées par des marqueurs écrits en fin de journal (un `pgrep` sur un
script pas encore lancé rend la main tout de suite — piège déjà consigné). La
chaîne « creux 512 » attendait `chaîne creux terminée` dans **son** journal (8)
alors que la chaîne « creux » l'écrit dans le **sien** (7) : elle a patienté deux
heures devant un GPU libre, et c'est le même défaut que les trois autres — un
instrument qui ne dit pas ce qu'il attend. Corrigé, et le marqueur est maintenant
nommé avec son fichier dans le commentaire de la garde.

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

**Les correctifs sont maintenant PROMUS** (9 octobre, 5 h 46) : `cargo build
--release` refait, les **77 tests passent**, et le contrôle qui avait révélé le
problème donne le résultat attendu — Codestral découpe « The river carries the logs
to the mill » en **8 jetons** au lieu de 31, et recolle le texte exact. La porte de
répartition à deux nœuds a été **rejouée avec ce binaire** : perplexité 3,6064,
écart de flux **0.00e0**, porte tenue.

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

### 19 bis. Quelle projection tolère d'être creusée ? Le tableau qui manquait

Le top-k du moteur peut viser **une projection à la fois** (`--topk-o`, `--topk-down`,
`--topk-gate`, `--topk-up`). Même modèle, mêmes 256 jetons, chemin par listes :

| projection creusée | 70 % gardé | 50 % | 30 % | événements au top-k 30 % |
|---|---:|---:|---:|---:|
| `o` (sortie d'attention) | **−0,3 %** | +3,3 % | **+17 %** | 86,95 G (−3,8 %) |
| `down` (descente FFN) | +0,5 % | +3,5 % | **+16 %** | 71,98 G (−20 %) |
| `gate` (porte FFN) | **−1,9 %** | +11 % | **+101 %** | 71,83 G (−20 %) |
| `up` (montée FFN) | +2,3 % | +16 % | **+75 %** | 71,83 G (−20 %) |

*(PPL de référence sans creusage : 17,4084.)*

**Trois enseignements, et ils orientent l'entraînement.**

1. **Le creusage léger AMÉLIORE la perplexité** — `gate` à 70 % gagne 1,9 %, `o`
   0,3 %. La même chose était visible au § 19 sur le seuil à 0,1 %. La parcimonie
   n'est pas qu'un coût : à faible dose, c'est une régularisation.
2. **Les deux projections qui portent une activation CALCULÉE (`o`, `down`) sont
   les plus tolérantes** (+16-17 % à 30 % gardés) ; celles qui lisent le **flux
   résiduel** (`gate`, `up`, et `q/k/v` par construction) s'effondrent (+75 %,
   +101 %). Autrement dit : **ce n'est pas la projection qui compte, c'est ce
   qu'elle lit** — creuser le flux résiduel demande que le modèle ait appris à y
   vivre.
3. **Chaque projection ne pèse que ~20 % des événements** : creuser une seule
   d'entre elles ne peut pas rendre l'architecture gagnante ; c'est le top-k
   **global** (`--act-topk`) qui met tous les événements à l'échelle du taux gardé
   (354 → 248 M au § 19).

C'est exactement pourquoi le k-WTA des modèles entraînés cette nuit porte sur
**toutes les couches linéaires** : le flux résiduel est la partie difficile, et
c'est celle qu'un modèle nativement événementiel doit apprendre en premier.

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

## 22 bis. Ce que le nouveau matériel change, d'après ces mesures

La machine va recevoir une carte 4×NVMe (4 Patriot P320 256 Go, Gen3 ×4) en RAID,
sur l'autre processeur, plus une carte AMD 6 mini-DP pour l'affichage
(`docs/configuration-nvme-raid-amd.md`). Ce que la campagne permet de dire de
l'effet attendu — et ce qu'elle ne permet pas :

| mesure de la campagne | ce que le RAID change |
|---|---|
| **8,6 Mo/s** de lecture en mmap sur disque dur contre 243 Mo/s en séquentiel (§ 12 bis) | **c'est le poste le plus amélioré** : le même moteur sur NVMe tient déjà 140-300 Mo/s (§ 12 bis). Les 90 minutes d'une passe gpt-oss et les 21 minutes de chargement du codestral deviennent des minutes |
| **le lot ne divise pas les lectures sur un MoE** (§ 14 bis) | inchangé : c'est la **structure** (union des experts touchés par une passe) qui le veut, pas le disque |
| **les experts ne passent pas par les listes** (format Q4_0, noyau absent) | inchangé — c'est du code, pas du matériel |
| **la parcimonie apprise divise les paires lues par 4** (§ 5 ter) | **amplifié** : des lectures plus rapides ne rendent pas la parcimonie inutile, elles déplacent le seuil de rentabilité du chemin par listes vers des densités plus élevées |
| **répartir paie si le calcul dépasse 3,4 ms × RTT** (§ 8 bis) | inchangé : la règle ne dépend pas du disque mais du réseau et de la taille du modèle |
| **20 threads saturés, 2 sockets, NUMA asymétrique** (`docs/numa-segregation.md`) | le RAID sur l'autre socket ajoute un chemin PCIe sans retirer de voies au GPU — c'était le but du plan |

**Ce que ces mesures ne disent pas** : rien n'a été mesuré sur le RAID lui-même
(il n'est pas installé). Les chiffres ci-dessus sont des **attendus dérivés** de la
comparaison HDD/NVMe de la campagne, pas des mesures du nouveau matériel — et la
première chose à faire quand il arrivera est de refaire **la même mesure de débit
`dd` et la même passe à froid**, pour vérifier que l'écart tient.

---

## 23. Ce qui reste à mesurer (état de la file, 9 octobre 5 h 20)

**Fait depuis la première rédaction de cette liste** : `parcimonie` (§ 19 et 19 bis),
`contexte` et `lot` (§ 20), `routage` (§ 7), `semantique` (§ 18), `noyau` (§ 21),
`repartition` (§ 8 et porte tenue), `portes` (**23 vertes, 0 rouge** — § 0 ter),
`batch 2` (§ 10 ter, quatre corpus), `batch 3` (§ 9, étendu à 12 288 jetons),
les paires entraînées (§ 5 et 5 bis, trois échelles), l'équivalence bit à bit (§ 22),
la tête restreinte sur gpt-oss (§ 13), le lot à froid avec éviction (§ 14 bis),
la carte de latence (§ 8 bis), les trois paires spéculatives (§ 1 bis), et **la
réponse à « imposée ou apprise »** (§ 5 ter).

**Encore en file au moment d'écrire :**

| file | état |
|---|---|
| **`m8_d512_kwta25`** (dense 512, k-WTA 25 % appris) | en entraînement depuis 5 h 05 ; mesuré ensuite à 0 %, 50 %, 25 % **et en dense à 25 %** (le chemin dense contre les listes, à taux égal — la première fois que les listes peuvent gagner sur un modèle dense) |
| **aiguille à 12 288 jetons** | 1 profondeur sur 3 (11 857 jetons ✅) ; les deux autres relancées après un délai dépassé — chaque sonde coûte 20 à 30 minutes |
| **`m9_d384_kwta25_distille`** | creux **et** distillé : les deux leviers se cumulent-ils ? En file après la chaîne 512 |
| **`m9_d512_route_long`** | le routé 512 avec **80 000 pas** au lieu de 40 000 : l'hypothèse « sous-entraîné » est-elle la bonne ? |

**Manques qui restent des manques, et rien ne les a entamés :**

| manque | état exact |
|---|---|
| **embeddings / encodeurs** | `bge-m3` est lisible en en-tête et **inexécutable** : ni attention bidirectionnelle, ni pooling. C'est le manque le plus net du relevé |
| **experts en listes (Q8)** | le chargeur d'experts refuse les tenseurs Q8_0 (« format sans noyau ni déquantification ») : **un modèle routé ne peut pas être exécuté en listes**. Tant que ce noyau n'existe pas, « routage + activations creuses » n'existe pas non plus |
| **décodage spéculatif** | le gain est démontré dans la niche (×1,52 pour un brouillon à 0,039× de sa cible), mais **aucune ligne de moteur n'est écrite** : vérifier k jetons d'un coup demande de brancher le préremplissage par lots sur le décodage |
| **qualité des modèles plus gros que la RAM** | le § 12 ne mesure que l'existence et le coût (365,7 Go sur 125 Go) ; la perplexité publiée pour V4-Flash n'a aucune valeur, et c'est écrit |
| **lot sur un modèle plus gros que la RAM** | **impossible aujourd'hui** : le seul modèle > RAM de la machine (V4.1, hyper-connexions) **refuse** le chemin par lots — « le résidu y est additionné au lieu d'être remélangé par `hc_post` ». Le moteur a raison de refuser (ce ne serait pas le même modèle), mais la question « le lot amortit-il les lectures du disque » reste **ouverte** |
| **codestral corrigé sur 256 jetons** | le run de contrôle a expiré sous la contention ; la valeur publiée reste celle à **63 jetons** (117,91), obtenue avec le binaire corrigé |

**Ce que la fenêtre a établi, en une ligne par famille** : le verdict du § 0 bis.
**Ce qu'elle a coûté en corrections** : cinq pièges de méthode (§ 16, § 17), dont
un binaire plus vieux que ses correctifs et une porte qui ne pouvait pas passer.
**Ce qu'elle laisse d'ouvert** : les cinq manques ci-dessus, dont deux — les
encodeurs et le noyau Q8 des experts — sont des chantiers de code identifiés, pas
des inconnues.
