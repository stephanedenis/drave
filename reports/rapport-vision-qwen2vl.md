# La vision n'est plus bloquée — elle est MESURÉE, et elle a tort

> Campagne : **cerveau** · expérience : la faculté **perception visuelle** (C1/M4), qui était
> « **bloquée par un modèle absent** » (`docs/cerveau-facultes.md` § 1bis, 15/10 06 h).
> Question : avec un vrai modèle de vision sur la machine, la tour du moteur tient-elle ?
> Verdict : **la tour TOURNE, et elle n'est PAS vérifiée.** Le modèle est là (Qwen2-VL-2B + son
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
