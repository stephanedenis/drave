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

**Et la courbe dépend de l'échelle** — vérifié à dim 512 (15 h 07), mêmes recettes,
mêmes témoins :

| dim 512 | perplexité | paires/jeton | écart au témoin dense |
|---|---:|---:|---:|
| témoin dense (`m6_d512_dense`) | **4,5686** | 34,4 M | — |
| structure innée 25 % (`m16`) | **4,8745** | **9,2 M** | **+6,7 %** (÷3,7) |

**La courbe complète, aux deux échelles** (les deux mesures de dim 512 sont tombées
le 9 octobre à 15 h 07 et 16 h 16 ; paires/jeton prises à la même fenêtre 8) :

| modèle | dim 384 | lectures | dim 512 | lectures |
|---|---:|---:|---:|---:|
| **témoin dense** | 4,9959 · 21,1 M | — | **4,5686 · 34,4 M** | — |
| **structure innée 25 %** (aléatoire) | 5,0472 (+1,0 %) | ÷4,1 | **4,8745 (+6,7 %)** | ÷3,7 |
| **les deux axes appris** (k-WTA + élagage) | 5,1866 (+3,8 %) | ÷7,8 | **4,9345 (+8,0 %)** | ÷7,2 |
| un axe imposé (masque + k-WTA) | 6,0792 (+21,7 %) | ÷15,1 | — | — |

**Deux conclusions, et la seconde n'était pas attendue.**

1. **Les recettes tiennent à l'échelle** : la structure innée divise les lectures par
   3,7 à dim 512 (contre 4,1 à 384), les deux axes appris par 7,2 (contre 7,8). Les
   ordres de grandeur sont conservés.
2. **Mais leur PRIX croît avec la taille** : +1,0 % → **+6,7 %** pour la structure
   innée, +3,8 % → **+8,0 %** pour les deux axes appris. Un modèle plus grand a plus
   de capacité à perdre quand on lui retire la même fraction — et cela vaut pour les
   deux recettes, y compris celle où **c'est le modèle lui-même qui choisit** quelles
   connexions garder.

**Conséquence pour un modèle ad hoc** : le point de fonctionnement « ÷8 pour +4 % »
est un point **de dim 384**. À dim 512, le même point coûte +8 %. La courbe n'est pas
universelle — elle dépend de la taille, et toute affirmation sur la parcimonie doit
porter son échelle, comme les autres mesures de ce rapport.

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

## 23. Ce qui reste à mesurer (état de la file, 9 octobre 16 h)

**Tout ce que la campagne devait mesurer est mesuré**, et chaque famille a sa ligne
au § 0 bis. Ce qui reste ouvert n'est pas de la mesure en retard, c'est du **travail
identifié** — et il est consigné dans [`docs/manques.md`](manques.md) plutôt que dans
une liste d'attente :

| ce qui reste | où c'est écrit |
|---|---|
| huit manques du **moteur** (noyau de listes pour les experts, noyau de listes sur GPU, lot et hyper-connexions, encodeurs, décodage spéculatif, apprentissage embarqué, qualité des modèles > RAM, défaut de sauvegarde du modèle log-normal) | `docs/manques.md` § 1 |
| quatre manques du **modèle** (structure innée à l'échelle, deux axes à l'échelle, règle locale, trois dessins inédits jamais entraînés) | `docs/manques.md` § 2 |
| douze capacités d'**architecture** pour porter un cerveau, en six phases à portes mesurées | `docs/plan-cerveau-complet.md` |
| la **courbe lecture ↔ qualité** complète, y compris à dim 512 | § 5 quater, complété à 16 h 30 |
| la **modularisation** (espace de travail Cargo, profil d'itération, verrous par ressource) | `docs/modularisation.md` |

**Ce que la fenêtre a établi, en une ligne par famille** : le verdict du § 0 bis.
**Ce qu'elle a coûté en corrections** : cinq pièges de méthode (§ 16, § 17), dont un
binaire plus vieux que ses correctifs et une porte qui ne pouvait pas passer.
**Ce qu'elle laisse** : un modèle dont le coût se choisit à la conception (÷4 pour
+1 %, ÷8 pour +4 %), et un plan — pas une promesse — pour le reste.

---

## 24. Mémoire épisodique (C6) : ce qui marche, et ce qui ne marche PAS

Ajouté après la campagne, dans le sprint « cerveau ». Le module `episodique.rs`
(clé creuse k-WTA + index inversé) est mesuré sur des **états réels** du
Qwen2.5-0.5B-Q8, 300 états d'un même texte, clé de **64 canaux sur 896** (7,14 %).
Toutes les valeurs ci-dessous sont reproduites par `tools/porte-episodique.sh`.

**Ce qui marche, et c'est exact au bit près :**

- **round-trip 300/300** — relire avec sa propre clé rend l'état écrit, au bit près,
  y compris après passage par le disque (300/300 lectures identiques) ;
- **rappel** : 100 % à 0 % et 10 % de dégradation de l'indice, **96,7 % à 25 %**,
  **69,3 % à 50 %**, **15,3 % à 75 %** (N = 300 ; hasard = 0,33 %) ;
- **nouveauté** : un indice jamais écrit obtient un recouvrement moyen de
  **41,5/64** contre **64,0/64** pour un épisode connu — le magasin sait donc
  distinguer « je me souviens » de « ça ressemble »… **en moyenne**, car le pire des
  indices nouveaux atteint **57/64** : il existe des faux positifs.

**Ce qui ne marche PAS, et c'est le résultat le plus utile :**

- **l'index inversé n'élague RIEN.** Sur les 300 états, chaque lecture examine
  **300 candidats sur 300 (100 % du magasin)**, soit 19 200 comparaisons de canaux.
  La raison est mesurable : les états de langue naturelle sont **corrélés** — deux
  états différents partagent en moyenne **23,9 canaux sur 64** (37 %), donc toute
  clé d'indice recouvre presque tout le magasin. Le « plus proche voisin
  approximatif » prévu au plan n'a donc rien à approximer ici : c'est un balayage
  complet déguisé. La conséquence pratique est que le coût d'une lecture est
  **N × k comparaisons d'entiers** (0,3 M pour N = 10⁴) — acceptable — mais que la
  **mémoire** du magasin est N × dim × 4 octets (3,6 Go pour 10⁶ épisodes à 896
  canaux) : c'est la mémoire qui limite, pas le temps de lecture ;
- **à petit k, l'invariant de round-trip CASSE.** k = 8 : **81 des 300 états
  partagent la clé d'un autre** (pire multiplicité 7) et le round-trip tombe à
  **219/300**, tous les échecs expliqués par ces collisions. k = 16 : 288/300 ;
  k = 32 : 299/300 ; k = 64 : 300/300. Autrement dit : **l'invariant du plan n'est
  pas une propriété du code, c'est une propriété du couple (données, k)**, et la
  porte le vérifie au lieu de le supposer.

**Deux hypothèses testées, deux réfutations utiles** (mesures directes) :

| variante | séparation | élagage | rappel 50 % | rappel 75 % |
|---|---|---|---|---|
| référence (300 états consécutifs) | 23,9/64 | **100 % du magasin** | 69,3 % | 15,3 % |
| états **espacés** d'un jeton sur 8 (150 états, 1 200 jetons) | **24,0/64** | **100 %** | 87,3 % | 22,0 % |
| **décorrélé** (moyenne des états retirée) | **20,3/64** | **100 %** | 78,3 % | 22,0 % |

- **L'espacement ne change RIEN au recouvrement** (24,03 contre 23,88) : la
  corrélation des clés n'est donc **pas** un effet de voisinage de texte. C'était
  l'hypothèse naturelle, et elle est fausse — les états d'un modèle partagent une
  composante commune qui ne dépend pas de la distance entre les jetons ;
- **la décorrélation aide la qualité** (séparation 23,9 → 20,3, nouveauté 41,5 →
  37,5, rappel à 50 % 69,3 → **78,3 %**) **mais ne fait toujours éluder aucun
  candidat** : 100 % du magasin reste examiné. La raison est arithmétique et se
  calcule : 300 épisodes × 64 canaux = 19 200 entrées réparties sur 896 canaux
  (≈ 21 par canal), donc une clé d'indice touche 64 × 21 ≈ 1 340 entrées qui
  couvrent **tous** les épisodes. **Avec 64 canaux sur 896, l'index inversé ne peut
  pas éluder** — ce n'est pas un défaut du code, c'est un défaut de densité.

**Ce que cela indiquait pour la suite** : pour que l'index élude réellement, il faut
**plus de canaux et des clés plus creuses** — une **expansion** comme celle du gyrus
denté. L'expérience a été faite, et elle a demandé **trois** ingrédients, pas un.

### 24 bis. L'expansion du gyrus denté, et ce qu'elle exige en plus

L'expansion seule (896 → 4 096, 8 entrées signées par canal, hachage déterministe)
**améliore la séparation mais n'élague presque pas** :

| configuration (300 états) | séparation | candidats examinés | rappel 50 % | rappel 75 % |
|---|---|---|---|---|
| 896 canaux, k = 64 (référence) | 23,9/64 | **300/300 (0 % éludé)** | 69,3 % | 15,3 % |
| 4 096, k = 32 | 6,5/32 | 256/300 (15 %) | 36,3 % | 3,7 % |
| 8 192, k = 64 | 13,0/64 | 282/300 (6 %) | 33,7 % | 7,0 % |
| 16 384, k = 64 | **9,0/64** | 267/300 (11 %) | 48,7 % | 10,3 % |
| **16 384, k = 64, canaux ÉGALISÉS** | **0,38/64** | **51/300 (83 % éludé)** | **96,3 %** | **69,0 %** |

La cause de l'échec de l'expansion seule est **visible dans la distribution des
listes de l'index** : quelques canaux sont systématiquement grands (la projection les
rend sensibles à une direction commune), ils entrent dans presque toutes les clés, et
leur liste devient un « hub » — 7× la longueur moyenne. Toute clé d'indice tombe sur
eux, et l'index redevient un balayage complet. **Centrer et réduire chaque canal de
clé sur le magasin** (une égalisation d'usage, ce que le gyrus denté obtient par
normalisation et inhibition latérale) fait tomber la séparation à **0,38/64** — le
plancher théorique du hasard pour 64 canaux sur 16 384 étant 0,25 — et l'élagage
passe à **83 %**.

**Ce que la mémoire gagne, et ce qu'elle paie** (16 384 canaux, k = 64, N = 300) :

- comparaisons par lecture : **3 237** au lieu de 19 200 — **÷5,9** ;
- rappel à 25 % de dégradation : **100 %** (contre 96,7 %) ; à 50 % : **96,3 %**
  (69,3) ; à 75 % : **69,0 %** (15,3) ;
- nouveauté : un indice jamais écrit tombe à **16,2/64** (contre 41,5) — le pire des
  nouveaux passe de 57/64 à **40/64**, donc les faux positifs reculent sans disparaître ;
- round-trip : **300/300 au bit près**, y compris à travers le disque. Le magasin
  stocke les **états exacts** (896 canaux) ; seule la **clé** est dilatée — sinon le
  magasin coûterait 18× plus cher et ne pourrait plus rendre l'état d'origine.

**Le coût de l'expansion est FIXE, celui du balayage croît** : 131 072 additions par
lecture contre N × 64 comparaisons. Le seuil de rentabilité se calcule —
**N ≈ 2 048 épisodes** — et **en dessous, le balayage complet est moins cher**. Une
expansion n'est donc pas « meilleure » : elle est meilleure *à partir d'une certaine
taille de mémoire*, et le chiffre est écrit dans la sortie du programme pour que
personne ne l'oublie.

### 24 ter. Le résultat tient-il sur PLUSIEURS documents ? Oui — 240 états, 3 corpus

Les mesures ci-dessus portaient sur un seul texte, et c'était une condition à lever :
un magasin qui ne marche que sur un document n'est pas une mémoire, c'est un index.
Les 240 états viennent donc de **trois corpus différents** (code, français,
multilingue), chacun repartant d'un **cache neuf** — donc sans contexte partagé entre
documents.

| mesure | un texte (300 états) | **trois corpus (240 états)** |
|---|---|---|
| round-trip | 300/300 | **240/240 au bit près** |
| séparation | 0,38/64 | **1,22/64** (hasard : 0,25) |
| candidats examinés (dernier N) | 17 % du magasin | **15 %** (35 sur 240) |
| rappel 25 % / 50 % / 75 % | 100 / 96,3 / 69,0 % | **99,2 / 95,0 / 73,8 %** |
| nouveauté (jamais écrit / pire) | 16,2 / 40 | **10,6 / 38** |
| ligne de base nulle | 0,33 % | 0,42 % |

Le résultat **ne dépend donc pas d'un texte unique** : il tient sur des corpus
différents, avec des états qui ne partagent plus le contexte du document.

### 24 ter bis. À QUELLE DISTANCE la mémoire se trompe-t-elle ? (utile, et mesuré)

Savoir si la mémoire rend l'épisode **exact** est une chose ; savoir à quelle
**distance** elle se trompe en est une autre, et c'est celle qui décide de l'usage :
un épisode voisin de deux jetons situe un passage, un épisode à cinq cents jetons ne
situe rien. Les épisodes sont numérotés dans l'ordre du texte, donc la distance entre
identifiants **est** une distance en jetons. Deux documents mesurés (clés de 64 canaux
sur 16 384, expansion + égalisation) :

| configuration | rappel 25 % | rappel 50 % | rappel 75 % | Δ à 50 % | Δ à 75 % | candidats examinés |
|---|---|---|---|---|---|---|
| 300 états, sans expansion (64/896) | 96,7 % | 69,3 % | 15,3 % | 26 jetons | 71 | 100 % |
| 300 états, expansion + égalisation | 100 % | 96,3 % | 69,0 % | **2 jetons** | 24 | 17 % |
| **2 048 états**, expansion + égalisation | 99,9 % | **95,4 %** | 64,5 % | **11 jetons** | 86 | 19 % |

L'expansion et l'égalisation n'améliorent donc pas seulement le rappel et l'élagage :
elles rendent la mémoire **treize fois plus précise** en localisation (Δ 26 → 2 jetons
à 50 % de dégradation, à N = 300).

**La précision RELATIVE s'améliore avec la taille du document** : 2 jetons sur 300
valent 0,67 % du texte, 11 jetons sur 2 048 en valent **0,54 %**. Autrement dit :
quand la mémoire se trompe, **elle se trompe de près** — le voisinage du bon moment
reste retrouvé. C'est exactement la propriété qui rend une mémoire de contenu utile
pour situer un passage : elle n'a pas besoin d'être exacte pour être utilisable, et
elle le dit en jetons.

Sur ce même magasin de **2 048 épisodes** : round-trip **2 048/2 048 au bit près**,
séparation 0,37/64, élagage **81 %** (382 candidats sur 2 048), et un indice jamais
écrit tombe à 8,8/64 contre 64/64 pour un connu. La consolidation par rejeu y donne,
en mode **exemplaire**, 62,5 % du magasin pour 93,4 % de rappel (seuil 16) et 87,8 %
pour 99,1 % (seuil 32) — la conclusion du §24 quater tient donc à l'échelle.

### 24 ter ter. Un indice ÉTRANGER retrouve-t-il le bon passage ? Oui, grossièrement

Toutes les mesures précédentes interrogent la mémoire avec un indice **issu de
l'épisode cherché** (une version dégradée de sa propre clé) : c'est de la complétion de
motif, et elle réussit. La question qui décide de l'usage est autre : **un indice qui ne
ressemble pas au contenu cherché le retrouve-t-il ?** Mesure sur l'invite A du §28
(1 750 jetons, code planté au jeton **740**) :

| indice | épisode rendu | recouvrement | distance à l'aiguille | hasard |
|---|---|---|---|---|
| l'état de la question, **pris dans le magasin** | 1749 (lui-même) | 64/64 | 1 009 jetons | 448 |
| l'état de la question, **EXTÉRIEUR** (la même question posée dans un contexte qui n'a PAS l'aiguille) | 604 | **4/64** | **136 jetons** | 448 |

Le premier cas ne testait rien : l'indice était dans le magasin, il s'y retrouvait
lui-même (recouvrement 64/64) et sa distance de 1 009 jetons ne dit rien — c'est
pourquoi `--episodique-indice` accepte un état **extérieur**, qui n'est pas dans le
magasin.

Avec un indice extérieur qui ne partage que **4 canaux sur 64**, la mémoire rend un
épisode à **136 jetons** de l'information — **3,3× mieux que le hasard** (448).

**Et cette marge n'est PAS robuste — corrigé après une deuxième mesure.** En écrivant la
porte de ce résultat, la question a été écrite avec un **point d'interrogation** de plus
(« Answer with the code only? » au lieu de « … only. ») : le même protocole donne alors
un épisode à **378 jetons** de l'aiguille, toujours sous le hasard (448) mais **2,8 fois
plus loin**. Un état de question change donc beaucoup pour un caractère de différence.

| indice extérieur (contexte sans l'aiguille) | rendu | recouvrement | distance à l'aiguille | hasard |
|---|---|---|---|---|
| question terminée par « only. » | 604 | 4/64 | **136** | 448 |
| question terminée par « only? » | 362 | 3/64 | **378** | 448 |

**Conclusion honnête, et elle remplace la première** : le rappel par le contenu
**n'est pas sémantique** (il ne trouve pas l'aiguille depuis la seule question), et
l'effet de voisinage qu'on croyait tenir **dépend de la formulation exacte de l'indice**.
Ce qui reste solide, c'est le reste : l'écho (un indice pris dans le magasin s'y
retrouve lui-même, 64/64), la complétion de motif depuis une clé dégradée (§24 ter), et
la localisation en jetons quand l'indice VIENT du contenu cherché.

**Conditions** : deux indices extérieurs seulement, un seul texte, position de l'aiguille
plantée par construction. La mesure suivante — plusieurs questions, plusieurs textes, et
la **moyenne** des distances plutôt qu'un cas — n'est pas faite.

### 24 quater. Consolider par rejeu : garder un CAS bat résumer par une MOYENNE

C7, au sens du plan, veut rejouer des épisodes pour modifier des **poids**. Ce n'est
pas ce qui est mesuré ici, et il faut dire pourquoi : le moteur n'entraîne pas, et
les règles locales qu'il possède déjà (hebbien différentiel) ont été mesurées
**dégradantes** sur la perplexité (`docs/hebbien-differentiel-et-biologie.md` :
8,8246 avec la règle contre 8,3869 sans). Rejouer pour ajouter du bruit n'est pas
consolider. Ce qui se mesure ici est la consolidation **de la mémoire** : rejouer les
épisodes et **fusionner ceux dont les clés co-activent** — deux souvenirs que le même
indice rappelle n'en sont qu'un.

La fusion demande une décision, et les deux réponses possibles ne se valent pas.
300 états, clés de 64 canaux sur 16 384 (expansion + égalisation) :

| seuil (canaux partagés) | **MOYENNE** : prototypes · compression · rappel | **EXEMPLAIRE** : prototypes · compression · rappel |
|---|---|---|
| 1 | 39 · 13,0 % · **22,3 %** | 21 · **7,0 %** · **87,0 %** |
| 2 | 116 · 38,7 % · 13,3 % | 57 · 19,0 % · **87,3 %** |
| 4 | 176 · 58,7 % · 18,7 % | 107 · 35,7 % · **93,0 %** |
| 8 | 200 · 66,7 % · 34,0 % | 154 · 51,3 % · **95,3 %** |
| 16 | 234 · 78,0 % · 56,0 % | 203 · 67,7 % · **97,3 %** |
| 32 | 274 · 91,3 % · 82,7 % | 269 · 89,7 % · **98,7 %** |

Le « rappel » est le rappel d'**appartenance** : la lecture doit rendre le prototype
qui *contient* l'épisode interrogé.

**Le résultat, et son mécanisme.** L'exemplaire (garder le premier cas absorbé, clé
comprise) **compresse plus ET rappelle mieux** que la moyenne, à tous les seuils. La
raison est mécanique et se vérifie dans le tableau : la clé d'une **moyenne** est
recalculée depuis un point qui n'a jamais existé, donc elle ne coïncide avec la clé
d'**aucun** membre — un indice venu d'un membre ne retrouve plus son prototype
(22,3 % à seuil 1, et **13,3 %** à seuil 2, pire qu'à seuil 1 : la moyenne s'éloigne
quand elle agrège). L'exemplaire, lui, garde la clé d'un cas réel : 7 % du magasin
suffit à 87 % de rappel, et 51 % du magasin à 95,3 %.

Autrement dit : **abstraire par moyennage détruit la rappelabilité**, et ce n'est pas
une opinion sur la mémoire, c'est une propriété de la clé. Cela reproduit, avec un
mécanisme mesuré, le débat classique entre théorie du prototype et théorie des
exemplaires — et tranche dans le sens des exemplaires *pour cette forme de mémoire*.

**Et le rejeu RÉPÉTÉ est un POINT FIXE, pas une usure** — la question laissée
ouverte au-dessus, maintenant mesurée (mode exemplaire, seuil 4, 300 états) :

| cycle | prototypes | compression | rappel (vs épisodes d'origine) | erreur |
|---|---|---|---|---|
| 1 | 107 | 35,7 % | 93,0 % | 4,37e-1 |
| 2 | 107 | 35,7 % | 93,0 % | **0,00e0** |
| 3 à 8 | 107 | 35,7 % | 93,0 % | **0,00e0** |

Rien ne bouge à partir du deuxième cycle, et l'erreur est **exactement nulle** : après
une consolidation, chaque prototype est son propre exemplaire, et deux prototypes ne
partagent plus assez de canaux pour être fusionnés. Le rappel est mesuré contre les
épisodes **d'origine** (les appartenances sont composées à travers les cycles), et il
reste à 93,0 % — donc **rejouer une mémoire ne l'use pas**, contrairement à ce que le
rejeu fait aux poids quand la règle est mauvaise (voir plus haut : 8,8246 contre
8,3869). La stabilité est une propriété de la règle de fusion, et elle est exacte.

**Ce qui reste non mesuré, et c'est écrit** : si la fusion améliore ou dégrade le
**rappel depuis un indice bruité** (ici l'indice est toujours non dégradé), et la
reconstruction de l'état d'origine à partir d'une clé dilatée.

**Conditions** : Qwen2.5-0.5B-Q8, expansion par hachage (8 entrées signées par canal),
égalisation calculée **sur le magasin** (en déploiement il faut donc la stocker avec
lui, et la recalculer quand il grandit).

**Conditions de ces chiffres** : 300 états d'un seul texte (ou un sur huit), un seul
modèle (0,5 B), k = 64. Le rappel après consolidation, sur des épisodes venus de
**textes différents** (plusieurs documents), ou avec un indice dégradé de façon
**corrélée** plutôt qu'aléatoire, **n'est pas mesuré ici**.

## 25. Le pont entre deux régions (C9/C10) : combien de fibres, et à quel prix

Ajouté dans le sprint « cerveau ». La question est celle du **corps calleux** : deux
régions d'un modèle échangent un état à chaque pas ; combien faut-il en échanger pour
ne rien perdre ? `--pont-k K` ne garde que les K plus grandes amplitudes de l'état
échangé, **dans les deux sens** (le nœud reçoit le même réglage), et le moteur publie
les **octets réellement échangés**. Modèle 0,5 B, 896 canaux, 48 pas, région locale
= couches 0-11, distante = 12-23.

**D'abord un piège, mesuré : en dense f32, élaguer ne réduit AUCUN octet.** Le flux
envoie 896 valeurs, que 448 d'entre elles soient nulles ou non :

| encodage | fibres | perplexité | octets/flux (aller) | écart |
|---|---|---|---|---|
| dense f32 | 896 | 113,0068 | 3 664 | — |
| dense f32 | **448** | **121,8551** | **3 664** | **+7,83 % pour zéro octet gagné** |
| dense f32 | 224 | 248,5349 | 3 664 | +119,9 % |
| listes par blocs | 896 | **111,9225** | 1 951 | — |
| listes par blocs | 672 | 112,9891 | 1 543 | +0,95 % |
| listes par blocs | **448** | **115,0632** | **1 096** | **+2,81 %, ÷1,8 en octets** |
| listes par blocs | 224 | 233,8589 | 648 | +108,9 % |
| listes par blocs | 112 | 1 153,3098 | 424 | +930,5 % |

**C'est l'encodage qui convertit la parcimonie en octets**, pas le pont. La courbe
utile est donc celle en « listes par blocs » (2 octets par neurone actif, indices par
écarts), et elle dit trois choses :

1. **on peut couper le corps calleux en deux** : 448 fibres sur 896 coûtent **+2,81 %**
   de perplexité et **÷1,8** en octets par pas (1 951 → 1 096) ;
2. **on ne peut pas le couper en quatre** : entre 448 et 224 fibres, la perplexité
   passe de +2,81 % à **+108,9 %** — la falaise est nette, et elle est **entre** ces
   deux points ;
3. **la falaise est localisée, et c'est une MARCHE, pas une pente** : entre 448 et
   392 fibres, le coût passe de **+2,81 %** à **+25,35 %** — soit neuf fois plus de
   dégradation pour 11 % de fibres en moins :

   | fibres | perplexité | octets/flux | écart |
   |---|---|---|---|
   | 896 | 111,9225 | 1 951 | — |
   | 560 | 114,2250 | 1 319 | +2,06 % |
   | **448** | **115,0632** | **1 096** | **+2,81 %** |
   | **392** | **140,2979** | **984** | **+25,35 %** |
   | 336 | 150,1778 | 872 | +34,18 % |
   | 280 | 166,0824 | 760 | +48,39 % |
   | 224 | 233,8589 | 648 | +108,95 % |

   Une marche à cet endroit dit quelque chose de précis : l'état au point de coupe a
   de l'ordre de **450 canaux porteurs**, et en dessous on entame le signal, pas le
   bruit ;
4. **à budget d'octets égal, élaguer est bien moins efficace que quantifier** :
   le rendement (perplexité pour 1 000 octets) est de 57,4 pour l'encodage complet
   contre 105,0 pour le pont de 448 fibres — **83 % pire**. Autrement dit : garder
   tous les canaux et réduire leur précision vaut mieux que jeter la moitié des
   canaux, sur ce lien comme sur les poids.

**Ce que la porte verrouille** (`tools/porte-pont.sh`, 7 cas) : pont entier ≡ sans
pont **dans les deux encodages** (perplexité identique) · les deux sens **maigrissent**
quand on élargit le pont · la courbe est **monotone** en les fibres (5 points) ·
élaguer **coûte** (sinon le pont n'est branché nulle part) · et le piège du dense f32
est vérifié comme tel (mêmes octets, perplexité pire).

**Ce qu'il faut en retenir pour distribuer** : sur ce modèle et ce découpage,
**garder tous les canaux et les quantifier** (listes par blocs, 2 octets par neurone
actif) donne la meilleure qualité par octet ; si le lien est vraiment contraint,
**couper à 448 fibres sur 896** (la moitié) coûte +2,81 % et divise les octets par
1,8 ; **ne pas descendre sous 448** — la marche est juste en dessous. Et si le lien
est dense (f32), élaguer ne sert à rien : cela ne fait que perdre.

**Conditions** : un seul modèle (0,5 B, 24 couches, découpage 12/12), 48 pas,
`--limit 48`, liaison locale TCP. Le pont n'est pas testé sur un modèle plus grand —
où la largeur d'état est plus grande, donc où le même *nombre* de fibres représente
une fraction plus petite ; ni sur un découpage différent (le point de coupe change la
largeur utile de l'état).

## 26. Le réflexe (C8) : un chemin court qui ne sait RIEN, et pourquoi

Un réflexe médullaire ne remonte pas au cortex : il répond par un chemin court. Dans
le moteur, ce chemin existe déjà — `--couches 0,L` tronque le modèle et
`--tete-partielle` applique la tête à la fin de la plage. La question mesurable n'est
donc pas « peut-on faire un réflexe ? » mais **« à partir de quelle profondeur un
réflexe tombe-t-il d'accord avec le modèle entier ? »**. Mesuré sur Qwen2.5-0.5B-Q8
(24 couches), 32 jetons réels, `--reflexe-essai` :

| couches | accord | accord top-5 | **cos(état tronqué, état final)** | ms/jeton | plus rapide |
|---|---|---|---|---|---|
| 1 | 0,0 % | 0,0 % | 0,044 | 4,5 | 18,5× |
| 2 | 3,1 % | 3,1 % | −0,009 | 7,0 | 11,9× |
| 4 | 0,0 % | 0,0 % | 0,013 | 16,7 | 4,9× |
| 8 | 0,0 % | 0,0 % | 0,058 | 32,3 | 2,6× |
| 12 | 0,0 % | 0,0 % | 0,083 | 49,6 | 1,7× |
| 16 | 0,0 % | 0,0 % | 0,145 | 61,7 | 1,3× |
| 20 | 6,2 % | 15,6 % | 0,320 | 79,8 | 1,0× |
| **24** | **100,0 %** | 100,0 % | **1,000** | 93,2 | — |

**Il n'y a pas de sortie précoce utilisable dans ce modèle** : jusqu'à 16 couches sur
24 (deux tiers de la profondeur), l'accord avec le modèle entier est de **0 %**, et il
ne décolle qu'à 24 — c'est-à-dire quand le réflexe *est* le modèle. Le gain de temps,
lui, est bien réel (une couche est 18,5× plus rapide) : l'échec n'est pas un artefact
de mesure.

**Et la cause est mesurée, pas supposée** : la **cosinus** entre l'état tronqué et
l'état final vaut 0,044 à une couche, **0,145 à seize** et 1,000 à vingt-quatre.
L'état intermédiaire est **presque orthogonal** à l'état final — la tête du modèle est
celle de sa dernière couche, et lit une direction que seules les dernières couches
produisent. Un réflexe court ne peut donc pas réutiliser cette tête : il lui faudrait
sa **propre** lecture entraînée (un petit module sur l'entrée), ce que le moteur ne
sait pas produire — et c'est un manque, pas un résultat.

**Conséquence pour la distribution** : le découpage en régions ne peut pas s'appuyer
sur une sortie anticipée d'une région pour aller plus vite. La seule sortie valide est
celle de la dernière couche, donc **le chemin est au moins aussi long que le
modèle** — ce que C1/C9 mesurent par ailleurs en latence et en fibres.

**Conditions** : un seul modèle (0,5 B, 24 couches), 32 jetons, sortie précoce **sans
tête dédiée**, accord mesuré sur le jeton de plus forte probabilité (la calibration de
la distribution tronquée n'est pas mesurée). Un modèle plus profond ou entraîné
autrement pourrait se comporter différemment : c'est une mesure, pas une loi.

## 27. OÙ COUPER le modèle ? Le point de coupe est neutre — sauf à cause du lien

Le découpage en régions (C1) et le pont (C9) avaient chacun été mesurés à **un seul
endroit** : 12 couches locales, 12 distantes. Rien ne disait que 12/12 soit le bon
endroit. Mesure sur Qwen2.5-0.5B-Q8 (24 couches), 48 jetons, huit points de coupe.

**1. Avec un lien SANS PERTE (dense f32), le point de coupe ne change RIEN :**

| coupe locale/distante | 4/20 | 6/18 | 8/16 | 10/14 | 12/12 | 15/9 | 18/6 | 20/4 |
|---|---|---|---|---|---|---|---|---|
| perplexité | 113,0068 | 113,0068 | 113,0068 | 113,0068 | 113,0068 | 113,0068 | 113,0068 | 113,0068 |

Huit valeurs identiques à la quatrième décimale : c'est l'invariant de C1, vérifié
sur huit coupes et non sur une seule. Le découpage est une affaire de **répartition du
calcul**, pas de résultat.

**2. Avec un lien ENCODÉ (listes par blocs), le même découpage s'écarte de 8,9 % :**

| coupe | 4/20 | 6/18 | 12/12 | 18/6 |
|---|---|---|---|---|
| perplexité | 116,3407 | **108,8721** | 111,9225 | **118,5275** |

Ce n'est donc pas le découpage qui change le résultat, c'est **l'erreur de
quantification du lien**, et elle dépend de l'état échangé — donc de la profondeur à
laquelle on coupe. À noter que trois coupes sur quatre font **mieux** que le lien sans
perte (108,87 et 111,92 contre 113,01) : la quantification du lien agit ici comme une
perturbation, pas seulement comme une perte.

**3. Le coût d'un pont de 448 fibres dépend aussi du point de coupe — et fortement :**

| coupe | 12/12 | 15/9 | 18/6 |
|---|---|---|---|
| coût du pont (448 fibres sur 896) | +2,81 % | **+17,09 %** | **+0,52 %** |

**Il y a donc un bon endroit pour couper, et ce n'est pas le milieu** : couper après
18 couches (6 distantes) rend le pont presque gratuit (+0,52 %), couper après 15 le
rend très cher (+17,09 %) — trente fois plus. Interprétation : l'état échangé à la
couche 18 est **redondant** (on peut en jeter la moitié), celui de la couche 15 ne
l'est pas. C'est cohérent avec la mesure de C8 : la direction de l'état se construi
tardivement (cos 0,145 avec l'état final à 16 couches, 0,320 à 20).

**Conséquence pratique pour distribuer** : couper **tard** si le lien est étroit, et
vérifier le coût du pont *au point de coupe choisi* — il varie d'un facteur 30 sur le
même modèle. La référence de perplexité d'un découpage encodé n'est pas celle du
modèle entier : elle doit être mesurée pour chaque coupe.

**Conditions** : un seul modèle (0,5 B, 24 couches), 48 jetons, encodage « listes par
blocs », pont symétrique (le même `--pont-k` des deux côtés). Les huit coupes sont
testées en dense f32, quatre en encodé ; les points intermédiaires (13, 14, 16, 17) ne
sont pas mesurés.

## 28. La greffe d'état (C2/C6) : elle TRANSFÈRE le contenu — ma première conclusion était fausse

> **CORRECTION DU 10 OCTOBRE (soir).** Ce qui suit concluait « une greffe d'état n'est pas
> une greffe de contexte ». **C'était un artefact d'un décalage d'un jeton**, pas une
> propriété du moteur : le prélèvement se faisait sur les identifiants tokenisés
> (`--tokenize`, 1 750 jetons) alors que l'inférence construit une invite d'**un jeton de
> plus** (1 751). L'état prélevé était donc celui qui prédit le dernier jeton du texte
> (« : ») au lieu de celui qui prédit le code.
>
> **Mesuré à nouveau, avec le prélèvement fait là où le calcul se fait** (`--etat-fin`,
> k-ième position depuis la fin, résolue dans la numérotation de l'inférence) :
>
> | état injecté dans une invite qui ne contient AUCUN code | réponse |
> |---|---|
> | état final de l'invite A (code `ZQ-4471-KX`) | **`ZQ3`** |
> | état final de l'invite B (code `KJ-9999-QP`) | **`K00`** |
>
> **Le contenu passe.** La greffe d'état est donc un mécanisme utilisable — et c'est le
> fondement de l'entrée de cache (C2) qui reste à construire. La leçon de méthode, elle,
> reste : **une position ne se devine pas, elle se capture là où le calcul se fait** ;
> trois mesures ont échoué pour cette raison avant que `--etat-fin` n'existe.

### 28 bis. Ce que la greffe d'état faisait vraiment (texte d'origine, conservé)

C6 sait stocker un état et le retrouver par son contenu ; C9 sait limiter ce qui
traverse un lien. Restait le **passage** : si l'on injecte l'état d'un moment vécu dans
un calcul qui ne l'a pas vécu, l'information portée est-elle encore là ? C'est ce qu'un
cerveau fait quand l'hippocampe rappelle un épisode au cortex. Mesure ajoutée par
`--fusion-etat` / `--fusion-pos` / `--fusion-alpha` (l'état brut, avant la norme
finale, est augmenté à la position choisie).

**Le protocole ne fait différer deux invites que d'une phrase** — c'est ce qui le rend
décisif : l'invite A (1 750 jetons) contient « IMPORTANT : the vault access code is
ZQ-4471-KX. », l'invite B est **le même texte, l'aiguille en moins**. Qwen2.5-0.5B-Q8
répond `ZQ-4471-K` à A et `150px` à B. On prélève l'état de la **dernière position** de
A et on l'injecte dans B, à sa dernière position.

| cas | mesure |
|---|---|
| témoin, poids **0** | sortie **identique** à B sans greffe (`220,16,20,15,…`) |
| **A + son propre état**, poids 100 | `25, 57, 48, 12, 19, 19, 22, 16` — **le contenu de A est toujours là** |
| **B + l'état de A**, poids 1 / 2 / 4 / 10 / 100 | **jamais le code** (`220,16,20,15,…` puis `25,16,20,15,…`) |
| B + l'état de A à **toutes** les positions, poids 100 | `25,25,25,25,…` — dégénéré |

**Ce qui est établi, en trois points :**

1. **l'injection est branchée** — un poids de 0 ne change rien (à la sortie près, au
   jeton près), et A greffé de son propre état conserve le contenu de A. Le mécanisme
   n'est donc pas en cause ;
2. **une greffe d'état n'est pas une greffe de contexte** : le code n'apparaît à AUCUN
   poids, ni même en injectant à toutes les positions (ce qui dégénère la sortie) ;
3. **et la cause est mesurée** : le **premier** jeton change (`220 → 25`, il vient de
   l'état injecté) mais **la suite reste celle de B** (`16, 20, 15`). Les jetons
   suivants sont **re-dérivés par l'attention sur le cache KV**, que la greffe ne touche
   pas. Un état résiduel est une **direction pour la tête**, pas un souvenir que le
   modèle peut relire.

**Conséquence, et elle est nette** : pour qu'une mémoire **serve** le calcul, ce qu'elle
rend doit entrer comme **contenu** (des jetons que le modèle peut lire — c'est le RAG
ordinaire) ou comme **entrée de cache** (un état rangé comme clé/valeur que l'attention
peut interroger). Le moteur n'a aujourd'hui **aucune prise sur le cache KV** : c'est un
manque, écrit comme tel, et non un réglage à trouver.

**Ce que la mesure ne dit pas** : elle porte sur un modèle de 0,5 B, une invite de
1 750 jetons, et une seule position d'injection (la dernière). Une injection à une
position *antérieure* du contexte, ou une injection **répétée à chaque pas** (un état
maintenu, comme le ferait un cache), n'ont pas été essayées — la seconde est
précisément ce qu'un cache mémoire demanderait.

## 29. La mémoire QUI SERT : retrieval → injection, de bout en bout

Après la correction du §28 (la greffe d'état transfère bien le contenu), la chaîne
complète devient mesurable : **indexer un document long, le retrouver par le contenu,
et injecter l'état retrouvé dans un calcul qui n'a pas vécu l'épisode**. Nouveau drapeau
`--episodique-extraire F` : il écrit l'état de l'épisode RETROUVÉ, en reconstruisant
l'état vécu (la moyenne est rajoutée si le magasin est décorrélé — sans quoi on
injecterait un état centré, qui n'est celui d'aucun moment).

Protocole : magasin de **1 750 états** de l'invite A (code `ZQ-4471-KX` au jeton 740,
expansion 16 384 + décorrélation + égalisation), indice **extérieur** = l'état final de
l'invite B (le même texte SANS le code), puis injection de l'état retrouvé dans une
invite qui ne contient aucun code.

| étape | mesure |
|---|---|
| rappel | épisode **437**, recouvrement 25/64, **303 jetons** de l'aiguille (hasard 448) |
| état extrait | 896 valeurs, norme **306,31** |
| injection α = 0 | `150px` — aucun effet (témoin) |
| **injection α = 0,2 et 1** | **`The vault access code is`** |
| injection α = 5 | `"150px` (saturé) |

**Ce que la chaîne fait, et ce qu'elle ne fait pas.** Injecter l'état retrouvé fait
**dire au modèle la phrase-cadre de l'aiguille** (« The vault access code is ») alors que
le contexte injecté ne contient ni le code ni cette phrase : l'information a donc bien
voyagé de la mémoire jusqu'à la sortie. Mais **le code lui-même n'est pas produit** — et
la raison est en haut du tableau, pas en bas : l'épisode retrouvé est à **303 jetons** de
l'aiguille, et à cette position le préfixe ne contient pas encore le code.

**Le goulot est donc le RAPPEL, pas la greffe.** La chaîne
`index → retrouver → injecter` fonctionne de bout en bout ; c'est la qualité du rappel
par un indice purement sémantique qui limite (303 jetons contre 448 de hasard, soit
1,5× — faible, et cohérent avec le §24 ter ter qui mesurait 136 et 378 selon la
formulation de l'indice).

**Deux réserves, écrites** : (1) l'état stocké est la sortie **normalisée** du moteur
(norme 306) alors que la greffe injecte un résidu brut (norme 54-66) — l'échelle est
absorbée par la normalisation finale, mais un magasin qui stockerait le résidu brut
serait plus cohérent, et ce n'est pas fait ; (2) un seul indice, un seul texte.

## 30. Le rappel par le contenu dépend de l'INDICE, pas de la mémoire (8 indices)

Le §29 avait montré que la chaîne mémoire → injection fonctionne, et que le goulot est le
RAPPEL. Restait à savoir **pourquoi** : la mémoire est-elle mauvaise, ou est-ce l'indice
choisi ? La question se répond par une distribution, pas par un point — d'où un
prélèvement de **huit positions** dans l'invite B (de la dernière à la 128ᵉ depuis la
fin), chacune servant d'indice extérieur au magasin de A (aiguille au jeton 740, hasard
448).

| indice (position dans B) | épisode rendu | distance à l'aiguille |
|---|---|---|
| 1594 (128ᵉ depuis la fin) | 1630 | 890 |
| 1658 (64ᵉ) | 393 | 347 |
| 1690 (32ᵉ) | 437 | 303 |
| 1706 (16ᵉ) | 393 | 347 |
| 1714 (8ᵉ) | 1743 | 1 003 |
| **1718 (4ᵉ)** | **690** | **50** |
| 1720 (2ᵉ) | 429 | 311 |
| 1721 (dernière) | 437 | 303 |

**Moyenne 444 · médiane 329 · meilleure 50 · pire 1 003 · hasard 448.**

**Ce que la distribution dit, et elle est plus instructive qu'un point :**

1. **un indice existe qui trouve l'aiguille** : la position 1718 (quatre jetons avant la
   fin) tombe à **50 jetons**, soit **9× mieux que le hasard** — c'est le voisinage
   immédiat, largement assez près pour que le préfixe de l'épisode contienne le fait ;
2. **mais un seul sur huit** : les sept autres sont à 303-1 003 jetons, c'est-à-dire au
   niveau du hasard (moyenne 444 contre 448). Le §24 ter ter qui annonçait « 3,3× mieux
   que le hasard » était donc un **tirage chanceux** parmi cette distribution — et sa
   fragilité (136 puis 378 selon un point d'interrogation) s'explique par la même cause ;
3. **la limite n'est donc pas la mémoire, c'est le choix de l'indice** — et ce choix ne se
   devine pas : il n'y a aucune raison de préférer la dernière position (303 jetons) à la
   quatrième depuis la fin (50 jetons).

**Suite — dix indices, et le résultat est plus tranchant que prévu.** Les six dernières
positions ont été prélevées une à une (la 4ᵉ était la gagnante) :

| position depuis la fin | jeton (déduit) | distance à l'aiguille |
|---|---|---|
| 1 | `:` | 303 |
| 2 | `Answer` | 311 |
| 3 | `.` | 533 |
| **4** | **`only`** | **50** |
| **5** | **`code`** | **1 006** |
| 6 | `the` | 1 005 |
| 8, 16, 32, 64, 128 | — | 1 003 · 347 · 303 · 347 · 890 |

Les six dernières positions, dans l'ordre : **303 · 311 · 533 · 50 · 1 006 · 1 005**.

**Deux jetons VOISINS — « code » et « only » — donnent 1 006 et 50 jetons.** Rien de
lexical n'explique cela : les deux états ont lu presque le même texte. Ce que ces deux
points disent, c'est que **le rappel n'est pas une fonction continue de l'indice** : la
clé est un k-WTA (les 64 plus grands canaux sur 16 384), donc une petite variation de
l'état fait **entrer et sortir des canaux**, et la clé saute. Il n'y a donc aucune pente à
suivre pour « s'approcher » du bon indice — c'est ce qui rend le choix de l'indice
impossible à deviner, et c'est un mécanisme, pas une fatalité.

**Ce que cela indique pour la suite, et ce n'est pas mesuré** : rendre la clé **stable** en
la formant sur une FENÊTRE de positions (union ou intersection des k-WTA voisins) au lieu
d'un seul jeton — ce qui lisserait l'hypersensibilité au prix de la précision ; ou
interroger avec plusieurs indices et garder le meilleur (mais le recouvrement ne les
départage pas : celui du gagnant, 25/64, n'est pas le plus élevé) ; ou **abandonner le
rappel sémantique** pour ce qu'il ne sait pas faire et faire entrer le contenu comme
jetons (RAG ordinaire).

## 31. Clé de FENÊTRE : la prédiction est RÉFUTÉE, et elle confirme la leçon du §24 quater

Le §30 avait identifié le mécanisme de l'hypersensibilité du rappel : la clé est un
**k-WTA** (64 canaux sur 16 384), donc une petite variation de l'état fait entrer et
sortir des canaux et **la clé saute** — deux jetons voisins donnaient 1 006 et 50 jetons.
Prédiction falsifiable qui en découle : **former la clé sur la moyenne de W positions
voisines doit lisser la clé et réduire l'hypersensibilité**. Mesuré (magasin de 1 750
états, aiguille au jeton 740, hasard 448) avec les deux indices extrêmes :

| fenêtre de clé | indice « only » (le bon) | indice « code » (le mauvais) | **séparation** |
|---|---|---|---|
| **1** (position seule) | **50** | 1 006 | **1,31/64** |
| 4 | 653 | 1 005 | 1,73/64 |
| 16 | 573 | 1 004 | 4,58/64 |
| 64 | **449** (= le hasard) | 1 004 | **19,94/64** |

**La prédiction est réfutée, et proprement :**

1. le lissage **ne réduit pas** l'hypersensibilité — il **détruit le bon indice**, qui
   passe de 50 jetons (9× mieux que le hasard) à **449**, c'est-à-dire exactement le
   hasard, pendant que le mauvais reste mauvais (1 006 → 1 004) ;
2. la **séparation s'effondre** : de 1,31 à **19,94 canaux partagés sur 64** — la clé
   d'une moyenne ressemble à celle de tout le monde, donc elle ne distingue plus rien.

**Et cela confirme, par une troisième voie indépendante, la leçon du §24 quater** : dans
cette mémoire, **abstraire par moyennage détruit la rappelabilité**. Le prototype moyen
était mal rappelé (22 % contre 87 % pour l'exemplaire), la clé moyenne ne retrouve pas le
bon passage, et la fenêtre moyenne fait tomber le meilleur indice au hasard. Trois
mesures, trois mécanismes différents, une seule conclusion : **la sélectivité de cette
mémoire EST la netteté de sa clé**, et l'hypersensibilité à l'indice en est le prix.

**Conséquence pour la suite, et elle change de direction** : puisque le lissage est exclu,
et puisque le choix de l'indice n'est pas devinable (§30), le rappel par le contenu n'est
pas la bonne primitive pour retrouver un passage depuis une question. Ce qui reste
défendable est ce qui a été mesuré comme solide : la **complétion de motif** depuis une
clé dégradée (Δ = 2 jetons à 50 % de dégradation à N = 300, 11 jetons à N = 2 048), la
localisation en jetons, et l'**injection** d'un état retrouvé. Retrouver un passage depuis
une question demande autre chose — des jetons (RAG ordinaire) ou une clé apprise.

## 32. Budget d'octets par lien (C10) : déclaré, et vérifié sur ce qui PASSE

Le plan demande des **budgets par lien** (`{paires/s, octets/s, ms}`) vérifiés au
démarrage. La mesure a imposé une correction au plan : **la taille d'un flux n'est pas une
propriété du mode**, elle dépend de l'ACTIVITÉ réelle — 1 951 octets par pas en listes par
blocs à 97,7 % d'activité, **1 096 à 50 %** (§31). Un contrôle au démarrage ne pourrait
donc comparer qu'à une valeur nominale inventée.

Le budget est donc déclaré dans la topologie (`"budget_octets": N` sur un lien) et
**comparé à ce qui passe**, au pas où il passe :

| cas | mesure |
|---|---|
| aucun budget (défaut) | perplexité **111,9225**, 1 951 octets par pas, code 0 |
| budget **généreux** (2 451) | perplexité **111,9225** — identique, code 0 |
| budget **insuffisant** (975) | le premier flux fait **1 860 octets** ⇒ arrêt **au pas 0**, message nommant le lien, les octets, le budget et le pas, **code 6**, et **aucune perplexité rendue** |

**Ce que la porte verrouille** (`tools/porte-budget.sh`, 3 cas) : un budget généreux ne
change rien ; un budget insuffisant arrête l'exécution **en le disant** ; et surtout
**aucun résultat partiel n'est rendu** — une perplexité calculée sur un transport qui n'est
pas celui qui a été déclaré aurait l'air d'un résultat. C'est la même règle que C4 (borne
de pas atteinte) et que le pont (C9) : *s'arrêter et le dire*, jamais rendre un chiffre qui
mentirait sur ses conditions.

**Suite — le budget de LATENCE, troisième volet du plan** (`{paires/s, octets/s, ms}`).
Déclaré par `"budget_ms": N` sur un lien, il se compare à l'**allé-retour mesuré** de chaque
pas. Mesuré (mêmes conditions que ci-dessus) :

| cas | mesure |
|---|---|
| latence **généreuse** (100 000 ms) | perplexité **111,9225** — identique, code 0 |
| latence **insuffisante** (1 ms) | `LATENCE DÉPASSÉE … : **20,1 ms pour un budget de 1 ms, au pas 0**` · **code 8** · aucune perplexité |

Quatre codes d'arrêt distincts désormais : **5** = borne de pas (C4) · **6** = budget
d'octets (C10) · **7** = panne de lien (C11) · **8** = budget de latence (C10). Un script
peut donc nommer la cause sans lire les messages.

**Un défaut de porte attrapé au passage** : la porte écrasait la variable `D` (le chemin du
binaire) avec la sortie du pilote, et le cas suivant échouait sur un code **127**
(« command not found ») — l'échec ne disait rien de ce qu'on mesurait.

**Détail mesuré au passage** : le PREMIER flux est plus gros que la moyenne (1 860 contre
1 951 en moyenne par pas sur 47 pas, mais le premier contient l'état le plus dense) — un
budget déclaré juste sous la moyenne arrête donc dès le premier pas, ce qui est le
comportement voulu et le plus sûr.

## 33. Pannes de lien (C11) : nommées, avec un code distinct, et sans résultat partiel

Le plan prévoyait, pour une région perdue, une politique `best-effort` où « la région est
sautée, l'écart est annoncé ». **La mesure oblige à refuser cette sémantique** : un modèle
dont on saute douze couches ne calcule pas une version approchée du même résultat, il
calcule **un autre modèle** — et l'« écart » annoncé serait un écart entre deux choses
différentes. La seule conduite honnête est de **s'arrêter en disant tout**.

Ce qui est implémenté, et mesuré par `tools/porte-pannes.sh` (3 cas) :

| cas | mesure |
|---|---|
| exécution nominale | perplexité **33,0156**, code **0** |
| **pair tué en cours de route** | `PANNE sur le lien local → d : le pair a fermé avant de rendre son état… L'exécution s'arrête **au pas 12** (**43 968 octets** échangés jusque-là). AUCUNE perplexité n'est rendue` · code **7** |
| **pair absent** | `PANNE : le pair local → 127.0.0.1:61342 est INJOIGNABLE (Connection refused)` · code **7**, en **2 s**, aucune perplexité |

Le code de sortie est **distinct** : 5 = borne de pas (C4), 6 = budget dépassé (C10),
**7 = panne de lien**. Un script peut donc distinguer les trois causes d'arrêt.

**Deux défauts trouvés en écrivant la porte**, tous les deux dans le moteur :
1. un pair absent faisait **paniquer** le pilote (`expect("connexion au nœud moteur")`,
   code 134 illisible) — au lieu de nommer le lien et de ne rien rendre. Corrigé ;
2. la porte elle-même attendait `client connecté` dans le journal du nœud pour tuer le
   pair : fragile, et elle échouait pour une raison qui n'était pas celle qu'elle mesure
   (port en TIME_WAIT, pilote qui calcule 10 s de référence locale avant de se connecter).
   Elle chronomètre maintenant la mort, et juge sur le code et le message.

**Ce qui reste du plan §3.2 sur les pannes, et qui n'est PAS fait** : la reprise. Un pair
qui revient n'a plus son cache KV, donc continuer serait faux ; reprendre proprement
demanderait de rejouer le préfixe (checkpoint/restart), ce qui n'existe pas.

## 34. La porte rouge de répartition : un DÉFAUT DE PORTE, pas un défaut du modèle

Le tour de vérification avait laissé **une rouge non expliquée** : `porte-reparti-moteur`,
perplexité entière **321,9623** contre répartie **132,8349** (écart 58,7 %) avec un **flux
bit-exact (0,00e0)**. La porte teste « notre modèle entraîné ici est-il découpable sans
changer un chiffre ».

**Trois hypothèses éliminées par la mesure :**

| hypothèse | test | résultat |
|---|---|---|
| le **routage d'experts** ne survit pas au découpage | même porte sur la variante DENSE (`/tmp/moteur_dense.gguf`) | **échoue aussi** (37,8 %) — ce n'est pas le routage |
| le **transport** altère les états | la porte imprime l'écart de flux | **0,00e0** |
| notre modèle est **intrinsèquement** non découpable | — | contredit par le résultat final, ci-dessous |

**La cause, trouvée en comparant les deux chemins à la main** : le fichier d'identifiants
contient **255 jetons**, et la porte en annonçait **128**. Or les deux chemins fenêtrent
**différemment** :

```text
--ppl          … note les `limit` PREMIERS jetons          → 127 jetons notés (0..127)
--ppl-reparti  … « 256 jetons fournis > limite 128 (ctx 256) : troncature aux 128 derniers »
                                                            → jetons 128..255
```

**La porte comparait donc deux textes différents** — et 37 à 58 % d'« écart de perplexité »
entre deux passages sans rapport est un chiffre parfaitement normal.

**Après correction** (le nombre de jetons est **compté** dans le fichier, plus supposé) :

| modèle | référence entière | répartie | écart |
|---|---|---|---|
| `moteur_dense.gguf` | 173,0196 | **173,0196** | **0,0000 %** |
| `moteur_route.gguf` | 173,0196 | **173,0196** | **0,0000 %** |

**PORTE TENUE — et les deux variantes, dense et routée, sont découpables au chiffre près.**
C'est un résultat du sprint « cerveau » : le modèle entraîné ici (Qwen3-MoE, corpus
d'octets) **survit au découpage**, routage compris, ce que la porte rouge laissait croire
faux pendant deux jours.

**Deux leçons, et la seconde est pour le moteur** : (1) une porte qui échoue doit être
instruite jusqu'à sa cause — celle-ci accusait le modèle, et c'était la porte ; (2)
`--limit` ne veut pas dire la même chose dans les deux chemins (`N` premiers en perplexité,
`N` derniers en réparti) : c'est une **asymétrie de protocole** à connaître, et elle est
maintenant écrite dans la porte qui l'a subie.

## 35. Découverte : le registre des régions (C11)

Une topologie qui écrit `"instance": "127.0.0.1:50001"` décrit **un** déploiement ; la même
topologie sur trois machines en demanderait trois. Le plan (§3.2, ligne « découverte »)
prévoit un registre statique puis dynamique : voici le statique, `--registre FICHIER`, dont
chaque ligne donne `region hote:port`.

**Ce qui est résolu, et ce qui ne l'est pas** : une instance qui contient déjà un `:` est une
adresse et n'est **pas** touchée — les topologies existantes continuent de marcher au
caractère près. Sinon elle est cherchée dans le registre, et une région **absente est
refusée en la nommant** : un repli silencieux sur `localhost` ferait parler le moteur à la
mauvaise machine. La résolution se fait des deux côtés (pilote et nœud relais).

`tools/porte-registre.sh`, 3 cas, verts :

| cas | mesure |
|---|---|
| topologie **nommée** + registre | perplexité **113,0068**, code 0 |
| même topologie, **adresse en dur** | perplexité **113,0068** — **identique** |
| région **absente** du registre | refus en la nommant, **code 2**, rien n'est calculé |

**Un défaut trouvé en écrivant la porte** : le contrôle de cohérence (« la région distante
est sur X mais `--ppl-reparti` dit Y ») comparait l'adresse à l'instance **brute** — une
topologie qui *nomme* ses régions était donc refusée comme contradictoire (code 3), alors
que les deux sources disaient la même chose. **La résolution doit précéder le contrôle**,
et c'est maintenant écrit dans le code à cet endroit.

## 36. Balayage des portes : le piège de fenêtre était LATENT dans une deuxième porte

Le §34 avait montré qu'une porte rouge accusait le modèle alors que c'était la porte :
`--limit` ne veut pas dire la même chose dans les deux chemins (`--ppl` note les `limit`
**premiers** jetons, `--ppl-reparti` **tronque aux `limit` derniers**). La question qui suit
est mécanique : **combien d'autres portes portent le même piège ?**

Balayage des 20 portes (celles qui invoquent `--ppl-reparti`) :

| porte | `--ppl` entier | comparaison à un entier ? | verdict |
|---|---|---|---|
| **porte-reparti-moteur** | oui | **oui, et elle affirme l'égalité** | **corrigée** (§34) |
| **porte-topologie** | oui | **non — elle imprime côte à côte** | **corrigée ici** |
| porte-flux | non | non : elle lit la « référence **locale** » du run réparti | sain par construction |
| 11 autres | non | non : elles comparent réparti à réparti | sains par construction |

**`porte-topologie` avait le piège à l'état latent** : son fichier d'identifiants contient
**255** jetons et sa limite en annonçait **128**, donc la perplexité de référence (premiers
128 jetons) et celle du découpage (derniers 128) **portaient sur deux passages différents**
— affichées l'une sous l'autre, comme si elles se comparaient. La porte ne l'affirmait pas,
donc elle passait ; mais elle **invitait à une comparaison fausse**, ce qui est exactement le
genre de piège que ce dépôt refuse.

Après correction (le nombre de jetons est compté) : **référence 5,3719 · découpage 5,3719**,
écart de flux **0,00e0** — les deux nombres affichés parlent enfin du même texte.

**La règle, écrite une fois pour toutes** : dans une porte, `--limit` doit valoir **le nombre
de jetons du fichier** (compté, pas écrit à la main) dès qu'un chemin réparti intervient. Les
deux portes qui le faisaient à la main s'étaient trompées toutes les deux.

## 37. E4 — l'équilibre excitation/inhibition : l'hypothèse est VRAIE dans un sens seulement

L'hypothèse biologique (E4) : un réseau cortical équilibré vit près d'un point où excitation
et inhibition se compensent, et un déséquilibre dans **un** sens ou dans l'autre coûte.
Transposée au moteur avec le levier existant `--ffn-gain couche:valeur`, la question
mesurable est : **existe-t-il un gain de la FFN, par couche, qui AMÉLIORE la perplexité — et
est-il intérieur ?** Qwen2.5-0.5B-Q8, 128 jetons, référence **14,6496**.

| gain | couche 0 | couche 1 | couche 2 | couche 6 | couche 12 | couche 18 |
|---|---|---|---|---|---|---|
| **1,0** | **14,6496** | **14,6496** | **14,6496** | **14,6496** | **14,6496** | **14,6496** |
| 0,75 | **12,9635** | 13,9844 | 15,9977 | — | — | — |
| 0,5 | 14,1057 | **13,7907** | 18,1670 | 15,2081 | 14,9512 | 15,4868 |
| 0,25 | **996,0390** | 14,2423 | 20,3067 | — | — | — |
| 0,0 | 56 860,57 | — | — | 17,6825 | 15,6908 | 17,4291 |
| −0,25 | 41 039,85 | — | — | 20,7224 | 16,3034 | 18,9574 |
| −0,5 | 70 349,61 | — | — | 27,6019 | 17,1200 | 21,2038 |
| −1,0 | 112 958,21 | — | — | 65,1286 | 19,4791 | 30,2514 |

**Trois résultats, et le premier est un invariant :**

1. **`--ffn-gain L:1.0` EST l'absence de réglage** : 14,6496 exactement, sur trois couches
   (0, 6, 18). Sans cet invariant, aucune autre ligne ne comparerait quoi que ce soit — et
   c'est la porte qui l'exige ;
2. **du côté INHIBITION, la courbe est MONOTONE et l'optimum intérieur est réfuté** : à la
   couche 12, tout gain inférieur à 1 dégrade, et de plus en plus (15,69 · 16,30 · 17,12 ·
   19,48). L'hypothèse « un peu d'inhibition fait du bien » est **fausse** ici ;
3. **du côté AMPLIFICATION, l'optimum est INTÉRIEUR et net sur les premières couches** :
   couche 0 à **0,75** → **12,9635**, soit **−11,5 %** ; couche 1 à 0,5 → 13,7907 (−5,9 %) ;
   la couche 2 n'a plus d'optimum utile (son meilleur point est ≥ 1,0). Et sous l'optimum il
   y a une **falaise** : la couche 0 à 0,25 donne **996,04**, **68× pire** — un gain trop
   faible à la première couche ne dégrade pas un peu, il casse le modèle.

**Ce que cela dit du modèle, et c'est le plus intéressant** : le profil optimal n'est pas
plat — il **décroît avec la profondeur** (optimum à 0,75 puis 0,5 puis ≥ 1,0). Les premières
couches ont donc besoin d'**être amplifiées** et les suivantes non ; autrement dit, la
« balance » d'un transformeur n'est pas la même à toutes les profondeurs, et un profil appris
par couche est un levier **mesuré** (−11,5 % sur un réglage, sans rien entraîner).

**Et le bénéfice est LOCALISÉ : le profil complet, sur les 24 couches, à gain 0,75.**

| couche | 0 | 1 | 2 | 3 | 4-16 | 17 | 19 | 21 | 23 |
|---|---|---|---|---|---|---|---|---|---|
| écart à la référence | **−11,5 %** | **−4,5 %** | **+9,2 %** | **+10,6 %** | ±1 % | +3,8 % | −0,1 % | +4,3 % | +5,7 % |

**Seules les couches 0 et 1 gagnent à être amplifiées** ; les couches 2 et 3 **perdent
beaucoup** (+9,2 % et +10,6 %, elles ne supportent pas d'être atténuées) ; les couches 4 à 16
restent dans ±1 % (neutres), et seules 17, 21 et 23 repassent au-dessus de +3 %. Le
déséquilibre n'est donc **pas réparti sur la profondeur : il est à l'ENTRÉE** — les deux
premières couches ont besoin d'être amplifiées, et le reste du réseau est déjà à son point.

**Et les gains NE SE COMPOSENT PAS — le profil défait le meilleur réglage seul.**
`--ffn-gain` accepte maintenant une liste (`0:0.75,1:0.5`), ce qui rend la question mesurable :

| profil | perplexité | écart |
|---|---|---|
| **`0:0.75` seul** | **12,9635** | **−11,51 %** |
| `1:0.5` seul | 13,7907 | −5,86 % |
| `0:0.75,1:0.5` | 13,7679 | −6,02 % |
| `0:0.9,1:0.6` | 13,4209 | −8,39 % |
| `0:0.75,1:0.5,2:1.0` | **13,7679** | identique au précédent |

**Ajouter le gain de la couche 1 DÉGRADE le résultat de la couche 0** (12,9635 → 13,7679) : les
deux réglages s'antagonisent en partie, ils ne s'additionnent pas. Le meilleur profil mesuré
est donc **un réglage SEUL**. Et la dernière ligne est le témoin qui rend les autres lisibles :
un gain de **1,0 dans un profil est exactement neutre** (13,7679 = 13,7679), donc l'identité
tient aussi à l'intérieur d'un profil.

**Conséquence pour le dessin I**, et elle est plus dure que celle du §37 : non seulement le
profil n'a que deux couches utiles, mais **le composer empire les choses**. Un profil appris
aurait donc à découvrir que la bonne réponse est « une seule couche, un seul gain » — ce qu'un
apprentissage par gradient sur peu de paramètres peut très bien ne pas trouver, puisqu'il
optimiserait les deux ensemble.

**Généralise-t-il ? Deux axes testés, et les deux disent la même chose : la direction tient,
la magnitude dépend des conditions.**

| axe | mesure |
|---|---|
| **autre quantification** (Q4_0 au lieu de Q8_0) | gain 0,75 à la couche 0 → **14,7453** contre **15,8055** sans réglage = **−6,7 %** |
| **fenêtre d'évaluation** (256 jetons au lieu de 128) | **17,1915** contre **17,4315** = **−1,4 %** (au lieu de −11,5 %) |

**L'effet n'est donc pas un artefact d'une quantification** : il vaut −6,7 % sur Q4_0 et
−11,5 % sur Q8_0. Mais **il décroît fortement avec la fenêtre** : −11,5 % sur 128 jetons,
−1,4 % sur 256. Le chiffre de −11,5 % est un **point de mesure**, pas une propriété du modèle,
et c'est écrit ainsi — la porte exige d'ailleurs que la magnitude décroisse, donc un futur
relecteur ne pourra pas citer le meilleur chiffre sans voir la condition.

**Conditions** : un seul modèle (0,5 B) en deux quantifications, deux fenêtres (128 et 256
jetons), un seul jeu d'identifiants ; l'optimum à 0,75 est un point de la grille
(0,5 · 0,75 · 1,0), il n'est pas localisé plus finement ; deux profils à deux couches testés,
plus un à trois couches.

## 38. Un drapeau qui ne faisait RIEN dans le chemin réparti (`--ffn-gain`)

En cherchant à mesurer l'interaction du gain d'entrée (§37) avec le **découpage**, la mesure
a rendu **exactement le même chiffre avec et sans le drapeau** (42,5477 dans les deux cas).
Ce n'était pas une absence d'effet : c'était une absence de **câblage**.

`--ffn-gain` était appliqué dans `run_infer` et dans `run_ppl`, et **pas** dans
`run_ppl_reparti` : dans le chemin réparti — celui sur lequel porte tout ce sprint — le
réglage ne faisait **rien, en silence**. C'est la famille de défauts que ce dépôt traque
(« un drapeau qui ne fait rien »), et celui-ci comptait double : un réglage fin qui ne survit
pas à la distribution est exactement ce qu'on ne veut pas découvrir en production.

**Corrigé** (le même câblage que les deux autres chemins), et mesuré :

| chemin | sans réglage | avec `0:0.75` |
|---|---|---|
| réparti (2 nœuds, 12/12 couches) | **180,5245** | **222,3496** — le drapeau **agit** |

Le signe de l'effet en réparti (222 > 180, sur 32 jetons) n'est pas celui du chemin local
(−11,5 % sur 128 jetons) : la fenêtre de 32 jetons est trop courte pour conclure quoi que ce
soit sur la qualité, et **cette comparaison-là n'est pas une mesure de qualité** — c'est un
contrôle de CÂBLAGE. La porte le traite comme tel : elle exige que les deux chiffres
**diffèrent**, pas qu'ils s'améliorent.

**Et le piège de fenêtre a mordu une troisième fois** dans cette même tentative : `--ppl` avec
`--limit 128` note les **128 premiers** jetons d'un fichier qui en compte 85 625, tandis que
`--ppl-reparti` **tronque aux 128 derniers**. Une comparaison entre les deux chemins doit donc
toujours porter sur un fichier dont la longueur **est** la limite — ou sur la « référence
locale » du même run. C'est écrit dans trois portes maintenant, et c'est écrit ici.

**La porte** : `tools/porte-gain.sh`, cas 8 (le drapeau doit agir en réparti), 8 cas verts.

## 39. Audit des drapeaux par CHEMIN : une méthode de criblage, et sa portée exacte

Après avoir trouvé `--ffn-gain` non câblé dans le chemin réparti (§38), la question qui suit
est mécanique : **combien d'autres drapeaux ne sont câblés que dans certains chemins ?**

**La méthode** (criblage statique) : extraire de `main.rs` les bornes des trois fonctions
d'exécution (`run_infer`, `run_ppl`, `run_ppl_reparti`), puis comparer les ensembles
d'assignations `mdl.<champ> = …` de chacune.

| fonction | champs assignés en propre |
|---|---|
| `run_infer` | 30 |
| `run_ppl` | 16 |
| **`run_ppl_reparti`** | **3** |

**Et c'est là qu'il faut être précis sur ce que la méthode PROUVE.** Le criblage a annoncé 29
champs « absents des autres chemins » pour `run_infer`, dont `act_thresh`, `act_topk`,
`attn_topk`, `qk_topk`, `moe_topk`… Or ces champs **sont** câblés dans les autres chemins — par
le **helper** `appliquer_quantification(&mut mdl, &opt)`, que le criblage ne lit pas. Le
criblage a donc un **angle mort** : il ne voit que les assignations écrites *dans* la fonction.

**Ce qu'il a réellement établi** : le chemin réparti assigne 3 champs en propre, le helper en
couvre 7 de plus, et c'est **précisément ce qui restait hors des deux** qui contenait le défaut
trouvé — `ffn_gain`, ni dans le helper, ni dans la fonction. La méthode a donc **servi**, à
condition de ne pas confondre « absent du criblage » avec « non câblé ».

**Ce qui n'est PAS concluant, et il faut le dire** : les candidats restants
(`--attn-window`, `--attn-sinks`, `--swa-pattern`, `--patch`, `--hebb-*`, `--flux-forcer`,
`--trace-flux`) n'ont **pas** été départagés — la tentative de mesure en chemin réparti a rendu
des perplexités **vides** (extraction en échec), et une mesure vide ne prouve rien. Ils sont
donc **à instruire**, pas déclarés sains ni défectueux.

**Prochaine commande, écrite ici pour être exécutable telle quelle** : pour chaque candidat,
comparer en chemin réparti `--limit <longueur du fichier>` avec et sans le drapeau (jamais
`--limit` écrit à la main, cf. §36), et exiger que les deux chiffres **diffèrent** — c'est un
contrôle de câblage, pas une mesure de qualité.

## Annexe — manifeste des journaux

Les journaux bruts sont dans `/tmp/campagne24/`. **59 fichiers d'étape (79 Kio)**,
plus **17 journaux de chaînes** (`journal.txt`, `journal2..15`). Chaque étape a
laissé ses journaux, et chacun porte sa mesure de tête :

| étape | journaux | mesure de tête (vérifiable dans le journal) |
|---|---:|---|
| 1 · `grille` | 6 | 0,5 B **17,4315** · 1,5 B 47,14 · 14 B 14,30 · codestral 35 657 (binaire périmé) · 30B **8,6327** · gpt-oss expiré |
| 2 · `parcimonie` | 24 | 12 réglages × 2 chemins · k-WTA 70 % : **+4 % pour −30 % d'événements** |
| 3 · `contexte` | 10 | perplexité **constante** (17,4315) par construction · RSS 1 248-1 249 Mo |
| 4 · `lot` | 9 | PPL **13,1368 → 13,1359** · débit 16,8 → 23,7 tok/s |
| 5 · `routage` | 2 | **1 826,2 M** de paires d'experts par jeton · 4 experts sur 128 |
| 6 · `sémantique` | 4 | pic de séparation **couche 13** (+0,0391) sur 398 langues, bande 10-15 |
| 7 · `noyau` | 1 | bande passante **21,5 Go/s** · push/pull **×3,19** à densité 1 |
| 8 · `répartition` | 2 | cinq modes · écart **0,0000 %** · flux 0,00e0 (modes 0, 1, 3) |
| 9 · `portes` | 1 | **22 vertes · 1 rouge** lors de la campagne — la porte gpt-oss a expiré sous contention, puis **rend 15,6017** (la valeur attendue) relancée seule : **23 · 0** |

**Ce que le manifeste dit du protocole** : aucune étape n'a été rejouée après coup
pour « arranger » un chiffre — les valeurs publiées viennent de ces fichiers, y
compris celles qui ont été **corrigées** (codestral, sémantique, porte gpt-oss), et
la correction est écrite à côté de la valeur d'origine.
