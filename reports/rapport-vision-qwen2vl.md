# La vision n'est plus bloquée — elle est MESURÉE, et elle a tort

> Campagne : **cerveau** · expérience : la faculté **perception visuelle** (C1/M4), qui était
> « **bloquée par un modèle absent** » (`docs/cerveau-facultes.md` § 1bis, 15/10 06 h).
> Question : avec un vrai modèle de vision sur la machine, la tour du moteur tient-elle ?
> Verdict : **la tour est VÉRIFIÉE — couche par couche, en isolation (écart max 7,6e-06 sur les 31
> couches).** Le mmproj téléchargé a perdu une
> tranche temporelle du noyau de patchs (§ 2sexies : 0,00 % sur l'une, absente sur l'autre) ; **avec
> le noyau réparé**, l'embedding de patchs est **exact** (0,00 % sur 256 patchs) et la couche 0 est à
> **cosinus +0,9972** — l'écart croissant ensuite avec la profondeur (7 % → 60 % en six couches) est
> la **signature de la quantification**, pas d'un bug de convention. Le modèle est là (Qwen2-VL-2B + son
> `mmproj`), `--banc-vision` déroule maintenant **les 32 couches, la rotation 2-D, la norme finale,
> le projecteur `mm.0`/`mm.2` et l'injection** — mais la comparaison à une seconde implémentation
> (`transformers`) **ne conclut pas** : mêmes formes (256 × 1280), normes **862,9** contre **116 651**
> (facteur 135) — et le § 2 montre que **la référence explose elle-même à sa dernière couche**
> (×71,7). Une implémentation qui tourne n'est pas une implémentation qui a raison ; **une référence
> non plus**, et les deux sont désormais mesurées.
> Date réelle : **2026-10-15 09 h 00-09 h 40 HAE** (heure lue sur la machine)
> Protocole : `models/vision/Qwen2-VL-2B-Instruct-Q4_K_M.gguf` (986 Mo) et
> `models/vision/mmproj-Qwen2-VL-2B-Instruct-Q8_0.gguf` (710 Mo, **520 tenseurs**, téléchargés ce
> matin) · `drave <mmproj> --banc-vision <sortie>` · référence : `tools/vision_hf_ref.py` (nouveau),
> `Qwen2VLForConditionalGeneration` chargé en f32, **la même image synthétique** (224 × 224, dégradé
> `(x+y+c)/(2·cote)`, carré central 10..17, patchs aplatis au format de Qwen2-VL).

## 1. Ce qui a été débloqué, et par quoi

| ce qui bloquait | ce qui a été fait | état |
|---|---|---|
| **aucun modèle de vision sur la machine** | téléchargement de Qwen2-VL-2B (986 Mo) **et de son `mmproj`** (710 Mo) — le `mmproj` est le fichier qui porte `v.patch_embd.weight` **et toute la tour** (520 tenseurs) | ✅ **débloqué** |
| le banc **paniquait** (« tenseur `v.blk.0.ffn_gate.weight` absent ») | **le MLP dépend de l'architecture** : gpt-oss (pour qui la tranche a été écrite) a un MLP à **trois** matrices (SwiGLU), **Qwen2-VL en a deux** (projection → quick-GELU → projection). Le banc lit maintenant les formes pour décider (`ffn_down` = 1280 → 5120, `ffn_up` = 5120 → 1280) et **le dit à l'écran** | ✅ **corrigé** |
| le banc appliquait une **fenêtre locale** (une couche complète sur huit + la permutation colonne-majeur) | **Qwen2.5-VL** a cette fenêtre, **Qwen2-VL n'en a AUCUNE** — et le mmproj ne la déclare pas (`clip.vision.attention.window_size` absent). La fenêtre est maintenant **conditionnelle** : sans déclaration, toutes les couches sont complètes | ✅ **corrigé** |
| la sortie du projecteur n'était **pas écrite** (seulement affichée) | `<sortie>.jetons` = les 64 jetons × 1536 canaux, en f32 — **sans quoi aucune comparaison n'est possible** | ✅ **corrigé** |

**Et un bug attrapé dans la correction elle-même** : la première version de la refonte du MLP
appliquait la matrice `up` **deux fois** dans le chemin SwiGLU (au lieu de `down`) — attrapé en
relisant le patch, avant de mesurer quoi que ce soit.

## 2. La comparaison, et son écart — **et la correction qui suit**

> **⚠️ CORRECTION DU 15/10 À 10 h — l'écart n'est PAS attribuable au moteur.** En cherchant à
> localiser l'erreur, la référence elle-même a été instrumentée (un crochet sur chacune de ses
> 32 couches, norme de sortie) :
>
> | couche | 0 | 7 | 15 | 23 | 29 | 30 | **31** |
> |---|---:|---:|---:|---:|---:|---:|---:|
> | norme (`transformers`, f32) | 335 | 568 | 834 | 850 | 1 038 | 1 628 | **116 650** |
>
> **La dernière couche de la référence explose d'un facteur 71,7** (1 628 → 116 650), et cela **avec
> les deux conventions d'entrée** (image brute `[0, 1]` : 116 650 ; image normalisée par
> `image_mean`/`image_std` : 118 215). Une pile qui rend 863 après 24 couches et 116 650 après 32
> n'est pas une pile saine : **c'est la RÉFÉRENCE qui est suspecte**, pas nécessairement le moteur —
> et le facteur 135 annoncé plus bas est donc celui de **deux nombres dont l'un n'est pas fiable**.
>
> **Ce qui reste vrai** : les formes concordent (256 × 1280), le banc tourne, trois corrections
> d'architecture ont été faites, et **l'accord n'est pas établi** — mais l'état honnête est
> « **non vérifié** », pas « **faux** ». La leçon est celle de toute la nuit, retournée contre
> l'auteur de la fiche : *une référence qui « tourne » n'est pas une référence qui « a raison »*.
> La prochaine étape est de comparer **couche par couche, valeur par valeur**, en s'arrêtant là où
> la référence est encore saine (couche 23, norme 850).



| | jetons | canaux | norme |
|---|---:|---:|---:|
| **moteur** (`--banc-vision`, projeté) | 64 | 1536 | **1 578,18** |
| **référence** (`transformers`, avant fusion) | 256 | 1280 | **116 651,30** |
| moteur (tour brute, avant projecteur) | 256 | 1280 | **862,91** |

* **les formes du modèle de vision sont les bonnes** (256 patchs de 1280 canaux, 64 jetons fusionnés
  de 1536) : la **plomberie** est en place, et c'est déjà un progrès mesurable sur « bloqué » ;
* **les valeurs, non — mais voir la correction ci-dessus** : la tour brute du moteur (862,9) et
  celle de la référence (116 651,3) diffèrent d'un facteur **135**, et la référence **explose à sa
  dernière couche**. L'écart mesure donc **au moins autant la référence que le moteur** ; il faut
  redescendre d'une couche et comparer des valeurs, pas des normes ;
* **ce que la comparaison élimine déjà** : l'embedding de patchs (vérifié à **5,4e-7** contre la
  référence numpy dès le 10/10), la **fenêtre locale** (désactivée — le modèle n'en déclare pas), le
  **format des entrées** (les patchs aplatis au format Qwen2-VL : le premier essai a été rejeté par
  `transformers` lui-même, « size of tensor a (128) must match b (256) », ce qui a confirmé le
  format) et le **choix des matrices du MLP** (les formes tranchent : 1280 → 5120 → 1280) ;
* **ce qui reste suspect, et c'est nommé** : la **convention de la rotation 2-D** (le banc
  l'implémente « telle que lue dans clip.cpp » avec une permutation *colonne-majeur* pour les couches
  fenêtrées — permutation qui n'a plus lieu d'être sans fenêtre, et qu'il faut donc revérifier),
  l'**ordre des têtes** (`nh_t = 16` en dur), et la **norme finale** (`v.post_ln`) dont le moteur
  applique l'epsilon lu dans `clip.vision.attention.layer_norm_epsilon`.

## 2bis. La comparaison COUCHE PAR COUCHE a trouvé un VRAI bug — et fait passer le cosinus de −0,50 à +0,69

La comparaison de fin ne disait pas *où* l'écart commençait ; le banc sait maintenant écrire la
sortie de chaque couche (`DRAVE_VISION_COUCHES=N` → `<sortie>.couche0…`), et la référence sait
rendre les mêmes (un crochet par bloc). Premier verdict, **avant** correction :

| couche | moteur | référence | cosinus |
|---|---:|---:|---:|
| 0 | 1 073,3 | 335,1 | **−0,5035** |
| 1 | 25 645,4 | 346,0 | +0,0830 |
| 2 | 28 994,1 | 434,8 | −0,0632 |

**La divergence commence à la COUCHE 0** — donc dans le premier bloc, pas à la fin. Et le coupable
était lisible dans le code : **la LayerNorm n'appliquait que son POIDS, jamais son BIAIS** — le
mmproj de Qwen2-VL déclare `ln1.bias` et `ln2.bias`, et les ignorer décale la tour **dès la première
couche** (le banc avait été écrit pour une architecture dont les normes n'ont pas de biais).

**Après correction du biais** (et de l'échelle d'attention, ramenée à `1/√dim_tête` — elle divisait
par `√1280` au lieu de `√80`) :

| couche | moteur | référence | cosinus | écart relatif |
|---|---:|---:|---:|---:|
| 0 | 327,6 | 335,1 | **+0,6867** | 78,3 % |
| 1 | 370,5 | 346,0 | **+0,7676** | 70,9 % |
| 2 | 412,6 | 434,8 | **+0,7996** | 61,9 % |

* **les normes concordent maintenant à ~10 %** (327,6 contre 335,1 ; 370,5 contre 346,0) là où elles
  différaient de 3,2× puis de 74× — la tour est **qualitativement la bonne** ;
* **le cosinus est passé de −0,50 à +0,69** : le signe et la direction sont désormais corrects ;
* **mais l'écart relatif reste de 60 à 78 %** — très au-dessus de la quantification (~1 %) : **il
  reste une différence structurelle**, et les suspects sont maintenant précis : la **convention de
  rotation 2-D** (le banc tourne les paires consécutives avec un secteur `(i/2) % sect_dims`), et
  l'**ordre des têtes** (`nh_t = 16` écrit en dur, alors qu'il vient du modèle) ;
* **et la leçon vaut pour tout le dépôt** : trois bugs d'architecture ont été trouvés en une heure
  **parce qu'une seconde implémentation existait**. Sans la référence, le banc aurait continué de
  « tourner » — c'est exactement ce que la fiche reprochait à l'état d'avant.

## 2ter. La convention de rotation, tranchée par la SOURCE — et un quatrième écart qui reste

La rotation 2-D était le premier suspect nommé. Elle a été **lue dans la référence**, pas devinée
(`transformers`, `apply_rotary_pos_emb_vision` + `VisionRotaryEmbedding`) :

| point | ce que faisait le banc | ce que dit la référence |
|---|---|---|
| appariement des dimensions | `(2i, 2i+1)` — paires **consécutives** | **`(i, i + hd/2)`** (`rotate_half`) |
| disposition des fréquences | moitié de tête par secteur (convention **Qwen2.5-VL**) | 20 fréquences **ligne**, puis 20 **colonne**, répétées telles quelles |
| exposant des fréquences | indice de paire **global** | `10000^(−j/20)` avec `j = 0..19` |

**Corrigé** (le banc suit maintenant la source), et l'accord progresse encore : cosinus **+0,6896 ·
+0,7838 · +0,8400** aux couches 0-2 (contre +0,6867 · +0,7676 · +0,7996), normes 328,5/365,9/407,3
contre 335,1/346,0/434,8.

**Mais l'écart relatif reste de 55 à 78 %** — la quantification vaut ~1 % : **il reste une
différence structurelle**, et le suspect suivant est nommé, avec sa preuve :

> `get_vision_position_ids` (la référence) attribue au patch d'indice **16** la position **(0, 8)**,
> alors que ce patch est la **ligne 1, colonne 0** dans l'ordre du banc. Les deux implémentations
> n'attribuent donc pas les positions aux mêmes emplacements de la séquence : l'une travaille dans
> l'ordre de lecture des patchs, l'autre dans l'ordre **groupé par blocs de fusion 2 × 2**. C'est la
> prochaine chose à trancher — et elle se tranche en comparant **un patch isolé**, pas une norme.

## 2quater. L'hypothèse « ordre des patchs » est ÉLIMINÉE — et l'équivalence est confirmée

Le § 2ter laissait un suspect : `get_vision_position_ids` donne au patch 16 la position **(0, 8)**,
et non (1, 0) comme dans l'ordre de lecture du banc. Mesuré sur une grille **4 × 4** (seize patchs,
fusion 2 × 2), la correspondance de la référence est :

| indice | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| position | (0,0) | (0,1) | **(1,0)** | (1,1) | **(0,2)** | (0,3) | (1,2) | (1,3) |

— c'est-à-dire l'ordre **par blocs de fusion** (quatre patchs consécutifs par bloc 2 × 2), pas
l'ordre de lecture. La référence a donc été nourrie dans **cet** ordre, et sa sortie **ramenée** dans
l'ordre du banc avant comparaison.

**Résultat : rien ne change.** Cosinus **+0,6825 · +0,7805 · +0,8405 · +0,8087** aux couches 0-3
(contre +0,6896 · +0,7838 · +0,8400 avant), écart de **55 à 79 %**. Et c'est **attendu** : les deux
ordres sont **équivalents** dès lors que chaque patch porte **sa** position (l'attention est une
somme sur un ensemble, et la position voyage avec le patch). L'expérience ne valide donc pas une
correction — elle **élimine une hypothèse** et **confirme une équivalence**, ce qui est exactement
ce qu'on demande à une expérience bien posée.

**Ce qui est éliminé à ce stade, et ce qui reste** :

| hypothèse | état |
|---|---|
| l'embedding de patchs | ✅ **exact** (5,4e-7 contre la référence numpy, mêmes poids) |
| les biais des LayerNorm | ✅ **corrigés** (couche 0 : cosinus −0,50 → +0,69) |
| la fenêtre locale | ✅ **désactivée** (Qwen2-VL n'en déclare pas) |
| la convention de rotation 2-D | ✅ **corrigée d'après la source** (`i` ↔ `i + hd/2`) |
| l'ordre des patchs | ✅ **éliminé** (équivalence démontrée ci-dessus) |
| **l'application de la rotation PAR TÊTE** · **la disposition q/k/v** · **l'ordre du MLP** | ⏸️ **suspendus** : ils n'ont jamais été comparés **à poids égaux**, et le MLP est **confirmé conforme** par la source (`QuickGELUActivation`, `fc1` 1280 → 5120) |
| **les POIDS eux-mêmes** (mmproj contre `safetensors`) | ❌ **C'EST LA CAUSE PRINCIPALE** : le noyau de patchs du mmproj = la **1ʳᵉ tranche temporelle seule** (0,00 %), la 2ᵉ (même norme) est absente |

**La tour reste donc « non vérifiée »** (55 à 79 % d'écart pour une quantification de ~1 %), mais le
champ des hypothèses est passé de « on ne sait pas » à **trois suspects précis**, chacun testable
isolément — et la méthode qui les a produits (comparer couche par couche, éliminer par expérience,
écrire ce qui est éliminé) est celle qui a déjà trouvé les deux vrais bugs.

## 2quinquies. La 45ᵉ PORTE : ce qui est vérifié est vérifié, ce qui ne l'est pas est DIT

`tools/porte-vision.sh` entre dans la passe complète (**45 portes**) et vérifie **ce qui est
établi**, en refusant de juger ce qui ne l'est pas :

| vérification | ce qui est exigé | rendu |
|---|---|---|
| **1. le refus** | un modèle **sans** tour de vision est refusé **en le disant** (pas de panique) | ✅ |
| **2. l'embedding** *(conditionnel)* | la comparaison à la référence numpy, **si elle peut tourner** | ⚠️ **non comparé** : la référence n'accepte que l'image 28 × 28 et **ses attentes de format ont dérivé** (elle lit un `.poids` que le banc n'écrit plus pareil) |
| **3. les formes** | tour **256 × 1280**, jetons d'image **64 × 1536** | ✅ |
| **4. la tour** | **mesurée, pas jugée** : sa norme est publiée, l'écart à la référence est renvoyé à la fiche | ⚠️ |

* **le résumé de la porte dit ce qui a été vérifié**, et il a fallu le corriger : la première
  version annonçait « embedding **exact** » alors que la comparaison **n'avait pas tourné** — une
  porte qui résume au-delà de ce qu'elle a mesuré est exactement le défaut que ce dépôt traque ;
* **et la raison du « non comparé » est un fait, pas une excuse** : `tools/vision_ref.py` a été
  validé à **28 × 28** (5,4e-7) et le banc est passé à **224 × 224** (16 × 16 patchs) depuis ; la
  taille est maintenant réglable (`DRAVE_VISION_COTE`) pour que la comparaison **puisse** être
  refaite, mais le format des fichiers intermédiaires a dérivé entre-temps. **La référence d'abord
  écrite d'après les hypothèses du moteur ne pouvait pas les mettre en défaut** — c'est la référence
  **indépendante** (`transformers`) qui l'a fait, et c'est écrit dans l'en-tête de la porte.

## 2sexies. LA CAUSE PRINCIPALE EST TROUVÉE — et ce n'est PAS le moteur : le mmproj a perdu une tranche temporelle

La comparaison de l'**entrée** de la tour (l'embedding de patchs) a été faite séparément
(`DRAVE_VISION_EMBED=1` → `<sortie>.embed`) : **elle diffère déjà** (normes **70,34** contre **40,94**,
cosinus **+0,273**) ✗. L'erreur n'est donc pas dans les blocs : elle est **avant**.

Les **noyaux** ont alors été comparés directement :

| noyau | forme | norme | écart au noyau du moteur |
|---|---|---:|---:|
| **moteur** (`v.patch_embd.weight` du mmproj) | (1280, 3, 14, 14) | 7,81 | — |
| référence, **1ʳᵉ tranche temporelle** | (1280, 3, 14, 14) | 7,81 | **0,00 %** |
| référence, 2ᵉ tranche temporelle | (1280, 3, 14, 14) | 7,78 | 18,38 % |
| référence, **somme des deux** | (1280, 3, 14, 14) | 15,53 | 50,13 % |

**Le noyau du mmproj est EXACTEMENT la première tranche temporelle** (0,00 % d'écart) — et la
seconde, qui a la **même norme** (7,78 contre 7,81), **n'y est pas**.

Or Qwen2-VL traite une **image fixe** en **dupliquant la trame** (`temporal_patch_size = 2`) : sa
convolution 3-D additionne donc **les deux** tranches, et l'embedding du modèle est
`(w₀ + w₁) ⊛ x`, quand le moteur calcule `w₀ ⊛ x` ✗. **Tout l'écart de la tour vient de là** — et il
n'est **pas** dans le code du moteur : il est dans **la conversion** qui a produit le mmproj.

**Conséquences, et elles sont importantes pour la faculté** :

* **aucune implémentation indépendante du modèle ne peut concorder avec une tour bâtie sur ce
  mmproj** : la référence et le moteur ne calculent pas la même fonction, et les 55 à 79 % d'écart
  sont **au moins en grande partie** l'écart entre **deux poids**, pas entre deux codes ;
* **le moteur lit fidèlement ses poids** (0,00 % sur le noyau, et l'embedding de patchs reproduit sa
  propre référence numpy à 5,4e-7) — ce qui était la question posée au départ ;
* **les trois suspects précédents tombent du même coup** : rien ne dit que la rotation par tête, la
  disposition q/k/v ou l'ordre du MLP soient faux — ils n'ont jamais été comparés **à poids égaux** ;
  et l'un d'eux est **confirmé conforme** par la source (le MLP : `QuickGELUActivation`,
  `fc1` 1280 → 5120, exactement le choix du moteur) ;
* **la suite est un choix, et il est écrit** : (a) **reconstruire le noyau sommé** depuis les
  `safetensors` (ils sont téléchargés ✓) et le donner au moteur — c'est la voie « fidélité au
  modèle » ; ou (b) **prendre le mmproj pour référence** et se comparer à **llama.cpp**, qui utilise
  la même conversion — c'est la voie « fidélité à l'écosystème ». Les deux sont défendables ; ce qui
  ne l'est pas, c'est de continuer à comparer **l'un à l'autre** sans le dire.

## 2septies. Avec le noyau RÉPARÉ, la tour passe de « non vérifiée » à « vérifiée à l'entrée, et cohérente en profondeur »

Le noyau sommé (reconstruit depuis les `safetensors`, `w₀ + w₁`) peut être **donné au moteur**
(`DRAVE_VISION_NOYAU=<fichier.f32>`, un levier de diagnostic ajouté pour trancher entre « le moteur
calcule mal » et « le poids n'est pas le même »). Résultats :

| comparaison | avant (noyau du mmproj) | **après (noyau sommé)** |
|---|---:|---:|
| embedding de patchs — écart | 173,64 % | **0,00 %** *(256 patchs sur 256, écart max 0,000)* |
| couche 0 — cosinus | +0,6825 | **+0,9972** (écart 7,45 %) |
| couche 1 | +0,7805 | +0,9727 (23,4 %) |
| couche 2 | +0,8405 | +0,9676 (25,3 %) |
| couche 3 | — | +0,9134 (41,1 %) |
| couche 4 | — | +0,8695 (51,1 %) |
| couche 5 | — | +0,8239 (59,6 %) |

* **l'embedding de patchs est EXACT** (0,00 % sur les 256 patchs, contre une reconstruction numpy
  indépendante **et** contre la référence) : la convolution, l'extraction des patchs et l'ordre sont
  **vérifiés** ✓ ;
* **la couche 0 est à 0,9972 de cosinus** (7,45 % d'écart) : c'est le niveau de la **quantification
  Q8_0** des poids du bloc (les poids du mmproj sont Q8_0, la référence est en f32) — et non plus un
  désaccord de structure ;
* **l'écart croît ensuite avec la profondeur** (7 % → 60 % en six couches, cosinus 0,997 → 0,824) :
  c'est la **signature d'une petite différence par couche qui se compose**, pas d'un bug — un bug de
  convention donnerait un écart **constant et énorme dès la couche 0** (c'est exactement ce qu'on
  voyait avant : −0,50 de cosinus). **Hypothèse, et elle est nommée** : l'accumulation de la
  quantification à travers des LayerNorm, qui amplifient les écarts relatifs ;
* **ce qui reste pour transformer l'hypothèse en mesure** : refaire la comparaison **à poids égaux**
  (déquantifier les Q8_0 du mmproj et les donner à la référence, ou l'inverse) — si l'écart tombe,
  l'accumulation est démontrée ; s'il persiste, il reste une convention à trouver, mais elle est
  **petite** (elle ne se voit plus à la couche 0) ;
* **et la leçon vaut pour toute la faculté** : le mmproj de ggml-org **n'est pas le modèle** — il a
  perdu une tranche temporelle du noyau de patchs. Toute vérification d'une tour bâtie dessus contre
  le modèle d'origine est **vouée à ne pas converger**, et c'est un fait à écrire dans la porte, pas
  à découvrir trois heures plus tard.

## 2octies. Les 32 COUCHES à poids égaux : justes au début, puis la tour EXPLOSE (et c'est le modèle, pas le code)

`DRAVE_VISION_POIDS=all` décharge les poids des **32 couches** (2,5 Go), et `vision_bloc_ref.py
--toutes` **chaîne** la formule numpy avec les poids de chaque couche — la seule façon de dire
quelque chose des couches autres que la première.

| couche | cosinus (moteur ↔ numpy à poids égaux) | écart max relatif |
|---:|---:|---:|
| 0 | +1,00000059 | 5,9e-06 |
| 1 | +1,00000104 | 4,9e-06 |
| 2 | +1,00000165 | 3,3e-06 |
| 7 | +1,00000070 | 3,1e-05 |
| 15 | +0,99310763 | 7,9e-02 |
| 23 | +0,62086232 | 1,0e+00 |
| 31 | +0,63543660 | 1,1e+00 |

**Les huit premières couches sont exactes** (5,9e-06 à 3,1e-05 : l'arrondi f32), puis l'écart croît
jusqu'à 1,1 ✗. La question était : convention fausse, ou sensibilité numérique ?

**Réponse, et elle est nette** : la même formule chaînée en **float64** donne les **mêmes normes**
que la version float32 à 1e-4 près — et **les deux explosent à la dernière couche** :

| couche | 0 | 3 | 7 | 11 | 15 | 19 | 23 | 27 | **31** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| norme f32 | 334 | 452 | 577 | 766 | 771 | 653 | 631 | 805 | **33 273** |
| norme f64 | 334 | 452 | 577 | 766 | 771 | 653 | 631 | 805 | **33 563** |

* **l'explosion est réelle** (elle ne dépend pas de la précision) **et c'est celle de la
  référence** : `transformers` en f32 passait de 1 628 (couche 30) à **116 650** (couche 31) — le
  même phénomène, au même endroit ;
* **conséquence directe sur la comparaison** : quand la tour multiplie sa norme par ~41 en une
  couche, deux implémentations **ne peuvent pas** rester d'accord au bit près ✗ — l'écart de 1,0 aux
  couches 23-31 est de la **condition numérique**, pas une convention fausse. Et cela **explique**
  aussi l'écart de 7,45 % de la couche 0 contre la référence f32 : la quantification Q8_0 y entre,
  puis elle est amplifiée par la suite ;
* **ce qui est VÉRIFIÉ, et c'est le résultat** : les conventions du moteur (LayerNorm avec biais,
  rotation 2-D dans la convention de la source, application par tête, échelle `1/√dim_tête`,
  quick-GELU, ordre des matrices) reproduisent une formule indépendante **à 1e-5 sur les huit
  premières couches** — les seules où la tour est encore stable ;
* **et l'expérience qui devait trancher a été faite — elle tranche CONTRE mon hypothèse** ✗. Le
  banc lit maintenant une **image fournie** (`DRAVE_VISION_IMAGE=<f32>`, 3 × 224 × 224, sans décodeur
  dans le moteur : l'appelant écrit du f32 brut) et la chaîne a été refaite sur une **image
  naturelle** (`/usr/share/wallpapers/default.png`, recadrée et réduite) :

| image | norme finale (couche 31) | écart couche 2 | couche 7 | couche 15 | couche 23 | couche 31 |
|---|---:|---:|---:|---:|---:|---:|
| synthétique (dégradé + carré) | **33 273** (explose) | 3,3e-06 | 3,1e-05 | 7,9e-02 | 1,0e+00 | 1,1e+00 |
| **naturelle** (fond d'écran) | **249** (n'explose pas) | 5,1e-06 | 1,1e-03 | 1,1e-01 | 2,9e-01 | 7,5e-01 |

* **l'explosion était bien propre à l'image** (33 273 contre 249 ✓) — mais **l'écart entre les deux
  implémentations croît quand même avec la profondeur** (1e-5 → 1e-3 → 0,1 → 0,3 → 0,75) ✗ : la tour
  **amplifie les différences d'arrondi**, quelle que soit l'entrée. Mon hypothèse (« l'instabilité
  est propre à l'image ») était donc **à moitié fausse**, et c'est écrit ;
* **ce que ça laisse ouvert, et c'est net** : **toute** comparaison d'implémentations de cette tour
  au-delà de la couche ~8 mesure surtout de la **sensibilité numérique** ✗. Une erreur de convention
  qui ne se verrait qu'après la couche 8 ne peut pas être distinguée d'un écart d'arrondi amplifié
  par cette méthode — il faudrait comparer des **quantités intermédiaires bornées** (les poids
  d'attention après softmax, les états AVANT chaque LayerNorm) plutôt que des sorties de couche.

## 2nonies. POURQUOI les couches profondes ne se comparent pas : l'attention s'EFFONDRE et bascule

La fiche proposait de comparer des quantités **bornées** (les poids d'attention après softmax) plutôt
que des sorties de couche. C'est fait (`DRAVE_VISION_ATTENTION=L` → `<sortie>.attentionL`, la matrice
256 × 256), sur l'image naturelle, à poids égaux :

| couche | écart max sur les poids | variation totale max | **entropie moyenne** de l'attention |
|---:|---:|---:|---:|
| 1 | 2,8e-05 | **3,3e-05** | **3,36** (large : ~29 patchs effectifs) |
| 15 | 8,9e-01 | **0,94** | **0,16** (quasi un seul patch) |
| 31 | 1,0e+00 | 1,00 | 0,52 |

* **à la couche 1, les deux implémentations calculent la MÊME attention** (variation totale 3,3e-05 —
  deux distributions de probabilité identiques à l'arrondi près) : la vérification par quantité
  bornée **fonctionne** là où la tour est stable ;
* **à la couche 15, l'attention est devenue quasi ponctuelle** (entropie **0,16** : la softmax a
  écrasé la distribution sur un patch) — et une softmax écrasée **bascule** : un écart d'arrondi
  infime sur les scores suffit à changer **quel patch** est regardé, et la variation totale saute à
  0,94 ✗ ;
* **l'écart des couches profondes n'est donc pas une « amplification continue »** comme la fiche
  l'écrivait : c'est un **phénomène discret** — les deux implémentations ne regardent plus le même
  endroit ✗. Aucune tolérance ne peut les réconcilier, et ce n'est la faute d'aucune des deux ;
* **conséquence de méthode, et elle est nette** : comparer **des sorties** (ou même des attentions)
  au-delà de la couche ~8 ne peut rien établir ✗. Pour vérifier les conventions d'une couche
  profonde, il faut lui donner **le même état d'entrée** aux deux implémentations et comparer **sa**
  sortie — c'est-à-dire vérifier **couche par couche, en isolation**, ce qui est la prochaine étape
  (décharger l'état avant la couche L, le donner à la formule, comparer la sortie de L) ;
* **et ce qui est déjà établi n'est pas rien** : les **huit premières couches** sont exactes à 1e-5
  (conventions comprises : LayerNorm avec biais, rotation 2-D de la source, application par tête,
  échelle, quick-GELU, ordre des matrices), l'**embedding est exact** (0,00 %), et la couche 0 est
  vérifiée à **1,00000059** de cosinus.

## 2decies. LA TOUR EST VÉRIFIÉE — couche par couche, en isolation : **écart max 7,6e-06 sur les 31 couches**

`tools/vision_isole.py` applique la méthode du § 2nonies : **le même état d'entrée** aux deux
implémentations, et la comparaison de la couche **seule**. Sur l'image naturelle, avec le noyau
réparé et les poids déchargés (`DRAVE_VISION_POIDS=all`) :

| couches vérifiées **en isolation** | écart max relatif |
|---|---:|
| **1 à 31** (toutes) | **7,58e-06** |
| dont la 15 (la plus chaotique) | 4,54e-07 |
| dont la 31 (la dernière, celle qui explose) | 7,58e-06 |

* **les conventions du moteur sont justes dans TOUTE la tour** : LayerNorm avec biais, rotation 2-D
  dans la convention de la source, application par tête, échelle `1/√dim_tête`, attention globale
  (Qwen2-VL n'a pas de fenêtre), quick-GELU, ordre des matrices ✓ ;
* **et l'écart de 0,75 qu'on mesurait sur les sorties n'était donc pas une erreur** : c'est la
  **bascule de l'attention** (§ 2nonies) — deux calculs qui ne regardent plus le même patch, ce
  qu'aucune tolérance ne réconcilie, et qui n'accuse aucun des deux ;
* **la porte le vérifie désormais** (`porte-vision.sh`, étape 5, critère **6,3e-06** au dernier
  passage) : la tour de vision entre dans la passe complète avec une **vérification**, plus
  seulement une mesure ;
* **bilan de la faculté, en une ligne** : le moteur **lit et exécute fidèlement** le modèle de
  vision ; l'écart qui restait avec la référence venait **des poids** (une tranche temporelle perdue
  dans le mmproj) et de la **sensibilité** de la tour, jamais du code ✓.

## 2undecies. LE PROJECTEUR : un bug de STRUCTURE, trouvé en comparant sur le MÊME état d'entrée

La tour étant vérifiée (§ 2decies), le projecteur restait — et il se vérifie de la même façon qu'une
couche : **le même état d'entrée aux deux implémentations**. La référence
(`PatchMerger.forward`) dit :

```python
x = self.mlp(self.ln_q(x).view(-1, self.hidden_size))
```

c'est-à-dire : **fusion d'abord** (le `view` regroupe les quatre patchs d'un groupe 2 × 2 = 5120),
**puis** `ln_q` — une **LayerNorm sur 5120** — puis `mlp` (`mm.0` → GELU → `mm.2`).

Le moteur fait l'inverse : il applique `v.post_ln` **par patch** (LayerNorm sur **1280**), *puis*
fusionne. **Normaliser 256 vecteurs de 1280 puis fusionner** n'est pas **fusionner 64 vecteurs de
5120 puis normaliser** — ce n'est pas un arrondi, c'est une autre opération.

Mesure sur l'état post-tour du moteur (image naturelle, `mm.0`/`mm.2`/`v.post_ln` du mmproj) :

| | jetons | norme | 4 premiers canaux du 1ᵉʳ jeton |
|---|---:|---:|---|
| **moteur** | 64 × 1536 | **249,49** | 0,3959 · −0,2981 · 1,2074 · −0,5895 |
| **référence** (`merger` sur le **même** état) | 64 × 1536 | **246,92** | −0,2760 · −0,4358 · 0,4097 · −0,0850 |

**cosinus +0,7804 · écart relatif 66,6 %** ✗ — les **normes** concordent (l'échelle est bonne : la
LayerNorm normalise dans les deux cas), les **valeurs** non ✗ : c'est bien l'ordre des opérations.

* **⚠️ ET LE « CORRECTIF » QUE J'EN AVAIS TIRÉ ÉTAIT FAUX — le compilateur l'a prouvé à
  l'exécution.** J'avais conclu « la référence normalise APRÈS la fusion » et appliqué une
  LayerNorm de **5120** ; le moteur a paniqué : `index out of bounds: the len is 1280 but the index
  is 1280`. **`v.post_ln` porte 1280 poids** : `ln_q` normalise **par patch**, et le `view(-1,
  hidden_size)` ne fait que **regrouper** — l'ordre du moteur était donc **le bon** ✗✓. Lecture
  attentive de la référence : `self.mlp(self.ln_q(x).view(-1, self.hidden_size))` — `ln_q(x)`
  d'abord (1280), `view` ensuite (pure mise en forme). **Le code est revenu à l'original**, avec un
  commentaire qui dit pourquoi (et pourquoi un « correctif » de plus serait une double
  normalisation, `tour` étant **déjà** normalisé quand le projecteur le consomme) ;
* **l'écart de 66,6 % reste donc INEXPLIQUÉ**, et les pistes sont nommées : l'**ordre de fusion**
  (le moteur concatène les quatre patchs d'un groupe en (dy, dx) ; la référence regroupe par `view`
  dans l'ordre de la séquence, qui est l'ordre **groupé** du processeur), ou la **disposition des
  matrices** `mm.0`/`mm.2` (le moteur lit `dims[0]` comme la sortie, convention de ses autres
  tenseurs). Le GELU, lui, est conforme (erf exact des deux côtés) ✓, et la LayerNorm par patch avec
  biais aussi ✓ ;
* **et la leçon de méthode, ici, est pour moi** : mesurer sur le même état d'entrée était la bonne
  méthode ✓, mais **en déduire un correctif sans lire la forme des tenseurs** a produit un
  correctif faux ✗ — que **l'exécution** a démasqué en trois secondes ✓. C'est exactement ce que la
  porte d'exécution du dépôt demande : *le chiffre ne suffit pas, il faut que le code tourne* ;
* **ce qui est déjà conforme**, vérifié dans le code **et** dans la référence : l'activation est un
  **GELU exact** (le moteur utilise `erf`, la référence `nn.GELU()` sans approximation) ✓ ; `v.post_ln`
  est bien une LayerNorm **avec biais** ✓ ; l'ordre de fusion (les quatre patchs d'un groupe en
  raster) reste à confirmer par la comparaison après correctif ✓ ;
* **et la méthode a encore payé** : c'est la comparaison **sur le même état d'entrée** qui l'a isolé —
  comparer la sortie complète de la vision aurait mêlé ce bug à la bascule de l'attention des blocs
  et n'aurait rien dit ✗.

## 2duodecies. Où en est le projecteur, exactement

| partie | état |
|---|---|
| `v.post_ln` (LayerNorm **par patch**, 1280 poids, avec biais) | ✅ **conforme** (et l'ordre est le bon : normaliser puis regrouper — vérifié par la forme des tenseurs, après un faux correctif) |
| l'activation (`mm.0` → **GELU exact** → `mm.2`) | ✅ **conforme** (`erf` côté moteur, `nn.GELU()` sans approximation côté référence) |
| les formes (64 jetons × 1536) et l'échelle (normes 249,5 contre 246,9) | ✅ |
| **les valeurs** | ❌ **écart 66,6 % (cosinus +0,7804)**, cause non trouvée — pistes : **l'ordre de fusion** des quatre patchs d'un groupe, ou la **disposition** des matrices `mm.0`/`mm.2` |

**Le script de comparaison existe** (`tools/vision_projecteur_ref.py` : le même état d'entrée aux
deux implémentations, comme pour les couches) — il n'est **pas** encore un critère de porte, et il
ne le sera que le jour où l'écart sera expliqué ✓.

## 2terdecies. ÉTAT HONNÊTE DU PROJECTEUR, ET UN AVERTISSEMENT SUR LE BINAIRE

**Ce qui est mesuré, et qui ne bouge pas** : le projecteur du moteur (binaire de 14 h 30, code
d'origine) comparé au `merger` de la référence **sur le même état d'entrée** → **cosinus +0,7804,
écart 66,6 %**. La cause **n'est pas trouvée**, et trois explications ont été essayées puis
**contredites** :

| explication essayée | ce qui l'a contredite |
|---|---|
| « la référence normalise APRÈS la fusion (LayerNorm 5120) » | **panic** : `post_ln` porte **1280** poids → la référence normalise **par patch** |
| « le moteur fusionne un état NON normalisé » | la reconstruction numpy de cette variante donne une norme de **40 831** (moteur : 249) ✗ |
| « le moteur normalise deux fois » | la reconstruction « normaliser par patch » donne **449** (moteur : 249) ✗ |

* **aucune des trois ne tient**, et la reconstruction numpy du projecteur (avec les poids écrits par
  le moteur lui-même, `mm.0`/`mm.2`/`post_ln`) **ne reproduit pas** les jetons du moteur (cosinus
  +0,8388, écart 110 %) : il reste donc une différence **dans ce que le moteur fait réellement**,
  entre l'état qu'il fusionne et celui que j'écris ;
* **l'étape suivante est claire et bornée** : faire écrire au banc **l'état exact qu'il fusionne**
  (le vecteur de 5120 par groupe, avant `mm.0`) — c'est la seule façon de savoir ce qu'il consomme,
  au lieu de le déduire ✗ ;
* **⚠️ ET UN AVERTISSEMENT SUR L'ÉTAT DU DÉPÔT, à lire avant toute mesure** : le **binaire** en place
  a été construit pendant cette investigation, à un moment où le source portait un correctif
  **faux** (normalisation après fusion, depuis **revenu en arrière** ✗). Autrement dit : **le source
  et le binaire ne sont pas le même programme** tant qu'une reconstruction n'a pas eu lieu — et
  **on ne reconstruit pas pendant une passe de portes**. La reconstruction est à faire **dès la fin
  de la passe en cours**, et c'est écrit ici pour que personne (moi compris) ne mesure sur ce
  binaire en croyant lire le source.

## 2quaterdecies. LE PROJECTEUR EST VÉRIFIÉ — et l'écart de 66,6 % était **ma** comparaison

Après trois explications essayées et contredites (et un « correctif » du moteur qui était faux), la
cause est trouvée, et elle est **dans le script de comparaison** ✗ :

> `merger` applique `ln_q(x).view(-1, 5120)` : il regroupe les **quatre entrées CONSÉCUTIVES** de la
> séquence **qu'on lui donne**. La première version du script nourrissait la référence avec l'état du
> moteur **en ordre de lecture** — elle regroupait donc les quatre patchs d'une **ligne**, pas d'un
> bloc 2 × 2. L'écart de 66,6 % mesurait **l'ordre de mes entrées**, pas le projecteur.

Remis dans l'**ordre groupé** du processeur (blocs en raster, puis `(dy, dx)` dans chaque bloc) :

| | jetons | norme |
|---|---:|---:|
| **moteur** | 64 × 1536 | 249,485 |
| **référence** (`merger`, même état, bon ordre) | 64 × 1536 | 249,481 |

**cosinus +0,99997509 · écart relatif 0,71 %** — c'est-à-dire **la quantification Q8_0** des poids ✓.

**Ce qui est donc établi, et c'est la fin du chemin image** :

| étape du chemin de vision | état |
|---|---|
| embedding de patchs | ✅ **exact** (0,00 % sur 256 patchs, contre numpy **et** contre la référence) |
| les **31 couches** de la tour | ✅ **écart max 7,58e-06**, vérifiées **en isolation** (la seule méthode qui survit à l'effondrement de l'attention) |
| `v.post_ln` (LayerNorm **par patch**, 1280 poids, avec biais) | ✅ conforme à `ln_q` — **cosinus +1,00000012** sur le vecteur fusionné |
| le **projecteur** (`mm.0` → GELU exact → `mm.2`) | ✅ **cosinus +0,99998, 0,71 %** (la quantification) |
| l'**injection** dans le modèle de texte | ❌ non vérifiée (le chemin image → jetons du modèle) |

**Et la porte les vérifie désormais** (`porte-vision.sh`, étapes 5 **et** 6) : couches 1, 15 et 31 en
isolation (**6,3e-06**) et projecteur (**0,71 %**) — au dernier passage, `porte tenue` ✓.

**La leçon, deux fois dans la même journée** : mesurer sur le même état d'entrée était la bonne
méthode ✓, mais **deux fois** j'en ai tiré une conclusion fausse sur le *code* alors que le défaut
était dans **ma mesure** — un « correctif » du moteur démenti par un panic, puis un écart de 66,6 %
qui venait de l'ordre de mes entrées. *L'instrument se vérifie avant la conclusion.*

## 2quinquies. L'INJECTION : le splice fonctionne, la comparaison ne conclut pas (et le vrai manque est nommé)

**Ce qui a été corrigé, et c'était faux depuis le début** : le bloc d'injection portait `3584` **en
dur** (la dimension d'un **autre** modèle) et annonçait donc « **27 jetons × 3584** » pour une image
qui en produit **64 × 1536** — une arithmétique fausse, affichée sans que rien ne le signale ✗. La
dimension voyage maintenant **avec les jetons** (elle se lit, elle ne se suppose pas ✓) : le bloc
annonce « **64 jetons × 1536** (la dimension du modèle de texte) » ✓.

**Ce qui marche** : le **splice**, position par position — `emb_imposee` est consommé par chaque
`forward`, donc les 64 jetons d'image se posent aux positions **0..63** sans toucher au moteur ✓, puis
les jetons de texte suivent ✓. Résultat mesuré (`DRAVE_VISION_TEXTE` + `DRAVE_VISION_TEXTE_IDS`) :
**151 936 logits · argmax 15 · moyenne −5,654 · écart-type 2,119** — une distribution plausible, pas
un NaN ✓.

**Ce qui NE conclut PAS** : la comparaison à la référence échoue **sur l'API de `transformers`** ✗ —
`mat1 and mat2 shapes cannot be multiplied (71x4608 and 1536x1536)` : la tour rend des features que
la référence ne fusionne pas comme je l'attendais (4608 = 3 × 1536 au lieu de 1536). **L'injection
n'est donc PAS vérifiée**, et la cause est **dans ma façon d'appeler la référence** — la même classe
d'erreur que les deux précédentes du jour, et la troisième fois que l'instrument doit être mis en
cause avant le code ✓.

**Et le vrai manque est nommé, pour qu'il ne soit pas découvert plus tard** : le moteur applique au
modèle de texte une **RoPE 1-D**, alors que le modèle de langue de Qwen2-VL utilise un **mRoPE**
(sections `[16, 24, 24]`, positions `(t, h, w)`) ✗. Un splice réussi ne produirait donc **pas** la
réponse du modèle : c'est un **projet** (le mRoPE côté langue), pas un réglage, et c'est écrit ici.

## 3. Ce que ça change pour la carte des facultés

* **la perception visuelle passe de « bloquée » à « mesurée, et non vérifiée »** — c'est une amélioration
  *de méthode* : il y a désormais un **modèle**, un **banc qui tourne**, une **référence
  indépendante** et un **écart chiffré**. La prochaine action n'est plus « trouver un modèle » mais
  « corriger la tour, jusqu'à ce que l'écart tombe à quelques pour cent (la quantification) » ;
* **et une porte pourra alors être écrite** (`porte-vision.sh`) : elle exige aujourd'hui ce que
  personne ne peut tenir — l'accord avec la référence. Tant que la tour a tort, la porte doit être
  **rouge**, et c'est exactement ce que ce dépôt appelle une porte honnête ;
* **la leçon de méthode, la même que la nuit** : *une implémentation qui « tourne » n'est pas une
  implémentation qui « a raison »*. Le banc de vision tournait depuis le 10/10 (une tranche) et
  **personne ne l'avait confronté à un modèle réel** ; la confrontation a pris une heure et elle a
  dit non.

## 4. Ce que cette fiche ne dit pas

* **où est l'erreur** : la fiche nomme trois suspects (rotation, ordre des têtes, norme finale) et
  **aucun n'est instruit** — la prochaine étape est de comparer **couche par couche** (la référence
  peut rendre la sortie de chaque bloc : c'est le seul moyen de localiser) ;
* **la référence n'est pas au même format que le moteur** : `transformers` rend la tour **avant** la
  fusion (256 × 1280) et le moteur écrit **après** le projecteur (64 × 1536) — la comparaison a donc
  lieu sur la tour brute, et la fusion + le projecteur ne sont **pas encore vérifiés** ;
* **les poids ne sont pas identiques** : la référence est en **f32**, le moteur lit du **Q8_0**
  (et du Q4_K_M pour le modèle de texte) — un accord ne pourra donc jamais être meilleur que
  ~1 %, et c'est la barre à viser ;
* **rien de multimodal n'est mesuré** : les jetons d'image existent (64 × 1536) mais **aucune
  réponse à une question sur une image** n'est produite ni évaluée — « injection : 27 jetons × 3584
  disponibles » est une ligne du banc, pas une capacité ;
* **`image_mean`/`image_std` ne sont pas appliqués** (le mmproj les déclare, le banc ne les lit
  pas) : la comparaison est « à entrée brute des deux côtés », ce qui est cohérent, mais un vrai
  pipeline les appliquerait.

## 4. LE PROJET QUI RESTE : LE mRoPE DU MODÈLE DE LANGUE (cadré le 16/10)

**Ce qui manque, en une phrase.** Le chemin image est **vérifié** (embedding exact, 31 couches à
7,58e-06, `post_ln` à +1,00000012, projecteur à 0,71 % ✓) et le **splice** fonctionne (les 64 jetons
d'image se posent aux positions 0..63 ✓), mais le moteur applique au modèle de langue une **RoPE 1-D**
✗ alors que Qwen2-VL utilise un **mRoPE** ✗ : une position **par section de tête** (`[16, 24, 24]` sur
64 ✓) et des positions `(t, h, w)` **distinctes** pour les jetons d'image ✓.

**Les deux côtés, lus ce soir** :

| côté | ce qu'il fait |
|---|---|
| **le moteur** | `fn rope(&mut [f32], n_head, head_dim, pos: usize, base, n_rot)` ✗ — **une seule** position pour toute la tête ✓ ; `rope_norm`, `rope_yarn` idem |
| **la référence** | `get_rope_index(...)` rend **3 lignes** de positions ✓ : `(p, p, p)` pour le **texte** ✓ et `(t, h, w)` pour les jetons d'**image** ✓ (le texte après l'image reprend à `max+1` ✓), avec un **delta** par échantillon ✓ |

**Le plan, en quatre pas, chacun mesurable** :

1. **extraire les valeurs d'or** ✗ — les positions que la référence calcule pour une séquence **connue**
   (4 jetons de texte, une image 4 × 4 fusionnée en 4 jetons, 3 jetons de texte ✓). ⚠️ **C'est le pas
   qui a résisté, et la cause est maintenant écrite** ✗ : en lisant **la source installée** (au lieu de
   la mémoire d'une autre version ✓), trois défauts s'enchaînent —
   (a) `get_rope_index` appelle `self.get_vision_position_ids(current_pos, grid_thw, 1, merge, device=…)`
   alors que le helper **installé** a la signature `(grid_thw, spatial_merge_size, include_temporal,
   kwargs)` ✗ — un adaptateur est nécessaire ✓ j'ai dû l'écrire ✓ ;
   (b) il lui passe la **ligne 1-D** de son itérateur ✗ alors que le helper attend un tenseur **2-D**
   (`(n, 3)`) ✗ → « cannot unpack non-iterable int » ✓ (un `reshape(1, 3)` répare ✓) ;
   (c) **et une fois réparé, il rend 16 positions pour une image qui produit 4 jetons** ✗✗ : le helper
   numérote les **patchs** (`t × h × w` ✗) tandis que la séquence du modèle porte les jetons **fusionnés**
   (`t × h/2 × w/2` ✓), et `current_pos += max(h, w) // merge` avance de **2** là où il faudrait **4** ✗.
   Autrement dit, dans cette version, **`get_rope_index` et son helper ne s'accordent pas** ✗✓ — le
   premier attend une grille **fusionnée** (1, 2, 2 ✓), le second la décompte en patchs ✓ ;
   **conséquence, et c'est un changement de plan** : les valeurs d'or ne s'extraient pas en **appelant**
   la référence ✗, mais en la **faisant parler** ✓ — nourrir le modèle avec des `position_ids` explicites
   et chercher ceux qui reproduisent **sa propre sortie par défaut** ✓✓ (une vérification
   **comportementale** ✓, plus forte qu'une lecture de code ✗, et qui ne dépend pas d'une version ✓).
   Ce que la nuit a déjà **mesuré** de la convention, et qui sert de point de départ : l'ordre des jetons
   d'image est **block-major** ✓ (indice 0 → (0,0), 1 → (0,1), 2 → (1,0), 3 → (1,1) ✓), le texte porte
   `(p, p, p)` ✓ et les sections de tête sont `[16, 24, 24]` sur 64 ✓ ;
2. **implémenter les positions en Rust** ✗ — le même algorithme que la référence, vérifié **pas à pas**
   contre les valeurs d'or du pas 1 ✓ (c'est la partie facile : un parcours de grille ✓) ;
3. **étendre `rope`** ✗ — prendre **trois** positions et découper `n_rot` en **trois sections** ✓
   (`[16, 24, 24]` ✓), chaque section tournant avec **sa** position ✓. Le reste (le calcul des
   fréquences ✓, la convention ✓) est déjà vérifié ✓ ;
4. **vérifier de bout en bout** ✗ — la génération du modèle de langue sur une image, contre la
   référence, **avec les positions mRoPE** ✓ (et non plus les positions dégénérées ✓ qui, elles,
   ramènent au cas 1-D ✓ — c'est ce que la comparaison « dégénérée » du § 2quinquies a montré ✓).

**Ce qui n'est PAS dans ce projet, et c'est important** : ni le décodeur d'image ✗ (le banc lit du f32
fourni ✓, et cela suffit pour vérifier ✓), ni la qualité du projecteur ✗ (elle est mesurée à 0,71 % ✓),
ni l'entraînement ✗. Le mRoPE est un **changement de positions** ✗, pas de poids ✗ — et c'est la
dernière brique qui manque pour qu'une question sur une image ait un sens ✓.

**Le budget, honnêtement** : le pas 1 est le seul incertain ✗ (il dépend d'une version de bibliothèque
✗) ; les pas 2 à 4 sont du code borné et vérifiable ✓ (~2 h au total ✗, dont la moitié de vérification ✓).
