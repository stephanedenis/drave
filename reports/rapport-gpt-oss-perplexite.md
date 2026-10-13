# Perplexité de gpt-oss : deux bugs réels, une prémisse fausse

> Session du 28/09 (reprise de `REPRISE.md` §6.a). Tous les chiffres de ce
> rapport sont **mesurés** sur cette machine, avec le corpus
> `/tmp/wt2_txt.txt` (20 000 premiers octets de `data/wikitext2_test.txt`),
> gpt-oss-120b MXFP4, `--ctx 256 --dense --threads 16`, sauf mention contraire.

## 1. Ce qu'on croyait

`REPRISE.md` §6.a annonçait : perplexité **39,8** « au lieu de l'ordre de 6 »,
génération correcte, et une perplexité qui **croît avec la fenêtre**
(39,8 à 63 jetons, 129,9 à 511). Trois hypothèses étaient en lice : le gabarit
harmony, un codage de position faux (YaRN), et un bug de calcul restant.

## 2. Ce qui était réellement cassé

### a. Le biais de la projection de sortie d'attention était ignoré

gpt-oss déclare `attention_bias = true` : ses projections Q, K, V **et O** ont un
biais. Le chargeur passait bien les biais de Q, K et V, mais `None` pour
`attn_output` — un décalage constant ajouté à la sortie de chaque couche, donc
amplifié 36 fois.

Mesure, 63 jetons, tout le reste identique :

| | perplexité (63 jetons) |
|---|---|
| avant (biais O ignoré) | **39,80** |
| après (biais O chargé) | **20,84** |

### b. La fenêtre glissante s'appliquait aux 36 couches au lieu d'une sur deux

gpt-oss alterne `sliding_attention` (couches paires) et `full_attention`
(couches impaires) — c'est écrit dans son `config.json` (`layer_types`) et
llama.cpp le reproduit par `set_swa_pattern(2)`. Notre moteur lisait bien la
fenêtre déclarée (128) mais l'appliquait à **toutes** les couches : au-delà de
128 jetons, la moitié du réseau perdait l'information lointaine. C'est
exactement la signature observée « la perplexité croît avec la fenêtre ».

Mesure, 511 jetons :

| | perplexité (511 jetons) |
|---|---|
| fenêtre sur toutes les couches (motif 1, ancien comportement) | *(série C)* |
| fenêtre une couche sur deux (motif 2, corrigé) | **15,08** |
| aucune fenêtre | *(série C)* |

La trace de chargement dit maintenant lequel des deux régimes est actif :

```
[config] fenêtre glissante 128 sur 18/36 couches (motif 2 alterné)
```

### c. Un troisième bug, latent : les puits appris des couches pleines

Le softmax des couches **non fenêtrées** n'ajoutait pas le logit du puits appris
(`attn_sinks.weight`), alors que le chemin groupé — celui que gpt-oss emprunte —
le faisait déjà. La correction est juste (HF concatène la colonne du puits avant
le softmax puis la retire du numérateur), mais **son effet mesuré est nul sur
gpt-oss** : 20,8361 avant, 20,8361 après, au chiffre près. Elle protégera les
modèles qui empruntent ce chemin.

## 3. La référence externe : notre moteur n'était pas le maillon faible

Nouvel outil : `tools/ref_logits.cpp` évalue **exactement la même suite
d'identifiants** avec llama.cpp (mêmes positions, aucun BOS ajouté, une seule
séquence, un seul batch) et écrit les logits bruts, que
`tools/compare_logits.py` compare position par position.

| protocole (mêmes 63/511 prédictions) | llama.cpp | drave-core |
|---|---|---|
| 63 jetons, YaRN (la configuration déclarée par le modèle) | **38,37** | **41,11** |
| 511 jetons, YaRN, une seule fenêtre de 512 | **169,67** | **174,34** |

Sur les 63 positions : corrélation des logits **0,999976**, **top-1 identique
partout**, ∣ΔNLL∣ médian 0,076, max 1,49. L'écart résiduel est la
quantification de nos activations (15 bits, une échelle par vecteur) contre le
f32 de llama.cpp — pas une erreur de calcul.

**Conclusion : la prémisse « la perplexité devrait valoir ~6 » était fausse.**
Avec la configuration que le modèle déclare, *llama.cpp lui-même* donne 38,4 à
63 jetons et 169,7 à 511. gpt-oss est un modèle de raisonnement entraîné en
format harmony ; le wikitext brut n'est pas sa distribution. Notre moteur n'a
jamais été le problème — il est maintenant **meilleur que la référence** sur ce
modèle, parce qu'il sait éteindre YaRN (voir §4).

## 4. YaRN : le désactiver vaut ×9 sur ce modèle

| configuration | 63 jetons | 511 jetons (une fenêtre) |
|---|---|---|
| RoPE simple (défaut du moteur) | **20,84** | **18,58** |
| YaRN ×32 (ce que déclare le modèle) | 41,11 | 174,34 |

Ce n'est pas un bug d'implémentation :

- la formule de notre `rope_yarn` a été comparée numériquement à celle de
  `transformers` (`_compute_yarn_parameters`) : **identique**, aux deux indices
  de rampe près (nous tronquons `floor`/`ceil` comme llama.cpp, HF non —
  0,27 % d'écart au plus sur une fréquence, aucun sur les 18 autres) ;
- en mode YaRN, nos logits reproduisent ceux de llama.cpp (corrélation
  0,999976 au premier jeton, top-1 identique sur 63 positions) ;
- l'implémentation **officielle** d'OpenAI (`gpt_oss/torch/model.py`, fonction
  `_compute_concentration_and_inv_freq`) applique YaRN **à toutes les
  positions** dès que `scaling_factor > 1`, exactement comme HF et llama.cpp ;
  la concentration `0,1·ln(32)+1` est appliquée au cosinus **et** au sinus, donc
  aux requêtes et aux clés.

Autrement dit : les trois implémentations de référence appliquent un YaRN
statique à contexte court, et cela **dégrade** la perplexité d'un facteur 9 sur
ce modèle. Notre défaut (YaRN éteint) est donc un choix mesuré, pas un oubli.

Piste restante, non testée : appliquer YaRN **seulement au-delà** de
`initial_context_length` (4 096) — c'est la seule façon de garder le gain à
contexte court *et* l'extension à 128 k. Le protocole est en §7.

## 5. Le gabarit harmony : hypothèse réfutée

L'idée était : si la perplexité est mauvaise parce que le modèle est jugé hors de
son format, la présenter **dans** son format doit l'effondrer. Mesuré : c'est
l'inverse.

Le format harmony de gpt-oss a une contrainte que rien ne laissait deviner :
**le tour d'assistant commence par le canal `analysis`**. Juste après
`<|start|>assistant<|channel|>`, la distribution du modèle est sans ambiguïté
(logits décodés) :

| jeton suivant | probabilité |
|---|---|
| `analysis` | **0,9999** |
| `final` | 0,0001 |

Forcer `final` met donc le modèle dans un état qu'il ne comprend pas, et tout ce
qui suit est prédit au hasard — parfois **pire que le hasard** (NLL 13,4 pour une
uniforme à 12,2). Les montages mesurés, tous sur le même corpus :

| montage | perplexité |
|---|---|
| texte dans des messages `assistant` consécutifs | 443 |
| consigne + texte en canal `final` | 3 432 |
| tours alternés user/assistant, deux messages par fenêtre | 8 463 |
| « suite réelle » : préfixe en message `user`, suite en `final` forcé | 677 321 |
| **montage canonique** : message système officiel + `analysis` **puis** `final` | **26,0** |
| même montage, `analysis` retiré (tout le reste identique) | 9 625 |
| **texte brut, même contexte** | **13,7** |

Deux confirmations indépendantes :

- le montage canonique et sa variante sans `analysis` ont été construits **en
  fichiers d'identifiants**, hors du code harmony du moteur : le facteur 370
  entre les deux ne doit rien à notre implémentation ;
- le message système compte aussi : « You are a helpful assistant. » au lieu du
  message officiel (« You are ChatGPT… ») fait passer le même montage de 9 625 à
  677 321 — le modèle prédit « Chat » avec p = 0,77 après « You are ».

**Conclusion : dans le meilleur montage possible, le format harmony rend le texte
deux fois MOINS prévisible que le texte brut.** Le modèle n'est pas décalibré
hors de son format ; il est simplement mauvais en wikitext, et le format
l'entraîne vers autre chose.

## 6. Vérification gratuite : le tokenizer o200k

Les 4 424 identifiants produits par notre tokenizer sur le corpus sont
**identiques un à un** à ceux de `llama-tokenize` (0 écart). Le découpage n'a
jamais été en cause.

## 7. Effet de bord utile : `--tokenize` ne lit plus 62 Go

`Gguf::open` lit le fichier entier — nécessaire pour les poids, absurde pour les
métadonnées. Or `--tokenize` et le garde-fou de vocabulaire de `--ppl`
l'appelaient : chaque mesure de gpt-oss lisait donc **deux fois** les 62 Go.

`Gguf::open_meta` ne lit que l'en-tête (par tranches croissantes) et ces deux
chemins l'utilisent. Mesuré sur gpt-oss : `--tokenize` passe de ~60 s à
**0,385 s**, identifiants inchangés, et chaque `--ppl` économise une lecture
complète. Le contrôle de non-régression Qwen ne bouge pas (19,3885).

## 8. Contexte long : la rotation, la température, et ce qui dégrade vraiment

Le chantier suivant était le **YaRN à retardement** : n'appliquer l'étirement
qu'au-delà du contexte initial. En le mesurant, deux choses sont apparues.

### a. La moitié nuisible de YaRN, c'est la température

YaRN a deux composantes : l'**interpolation des basses fréquences** (qui étend
la portée) et la **mise à l'échelle de température** `mscale = 1 + 0,1·ln f` (qui
compense l'entropie du softmax quand les clés se multiplient). Le moteur sait
maintenant les activer séparément (`DRAVE_YARN_MSCALE`).

| longueur | RoPE simple | YaRN **sans** mscale | YaRN complet (référence) |
|---|---|---|---|
| 512 | **18,58** | 19,65 | 174,34 |
| 1 024 | **46,94** | 71,35 | 417,65 |
| 2 048 | **121,75** | 192,63 | 722,56 |
| 4 096 | **170,78** | 400,13 | — |

Retirer la température divise la perplexité par **8,9** à 512 jetons, 5,9 à
1 024, 3,8 à 2 048. C'est donc la température — pas l'interpolation — qui rend
le YaRN déclaré catastrophique sur du texte brut, alors que HF, llama.cpp et
l'implémentation officielle d'OpenAI l'appliquent toutes telle quelle (et que
notre moteur les reproduit au chiffre près quand on la garde).

Le RoPE simple gagne à **toutes** les longueurs mesurées, y compris à 4 096 —
la longueur initiale du modèle. Le seuil de bascule du mode retardé n'est donc
pas un croisement mesuré, mais une décision d'ingénierie prudente (au-delà de la
fenêtre d'entraînement, le RoPE simple extrapole) ; la mesure qui la trancherait
— le RoPE simple à 8 192 — est en cours (`/tmp/audela_4096.log`).

Le défaut du moteur devient donc : **RoPE simple sous la longueur initiale,
interpolation seule au-delà** ; `DRAVE_YARN=1` rétablit le comportement de
référence pour qui veut comparer.

### b. La dégradation avec la longueur n'est PAS un bug du moteur

La perplexité grimpe fortement avec la longueur (×9 pour le RoPE simple entre
512 et 4 096), et le profil par profondeur (`--ppl-profil`, ajouté pour ça) le
localise :

```
   0-255 : 13,715      768-1023 : 204,466     2048-2303 : 183,081
 256-511 : 25,142     1024-1279 : 292,803     2816-3071 : 212,334
 512-767 : 68,511     1536-1791 : 532,616     3584-3839 : 542,885
```

Deux causes se superposent, et une seule est imputable au moteur :

- **le contenu** : la même tranche de 260 jetons prise plus loin dans le corpus
  (jetons 1400-1659) donne 59,36 **à la position 0**, contre 13,94 pour la
  tranche initiale — le corpus n'est pas homogène ;
- **la position** : la même tranche à sa place réelle (~1400) tombe dans une
  tranche à ~380-500, soit un facteur ~7 de plus.

La référence tranche : **llama.cpp, mêmes 2 048 identifiants, un seul lot,
YaRN déclaré, donne 714,83 ; notre moteur 722,56** (1,1 % d'écart, la même
signature que les 3 à 7 % mesurés à 63 et 512 jetons). La dégradation avec la
longueur est donc **celle du modèle sur du texte brut hors distribution** — pas
un défaut de calcul. C'est aussi ce qui rend le chiffrage du 1 M
(`docs/contexte-long.md`) une affaire d'ingénierie mémoire et de préremplissage,
pas de rotation.

## 9. Ce qui reste ouvert

1. **YaRN à retardement** : n'appliquer l'étirement qu'au-delà de 4 096
   (`initial_context_length` du modèle). C'est la seule façon de garder le gain à
   contexte court *et* l'extension à 128 k. Protocole : corpus de 8 000 jetons,
   `--ctx 4096`, quatre passes (simple/YaRN × court/long), ≈ 13 min par passe sur
   le 120B. À noter : la **génération est correcte dans les deux modes** (sans
   YaRN : « Canberra. » ; avec : « The capital city of Australia is Canberra. »),
   donc l'enjeu est la calibration, pas la fluidité.
2. **Quantification des activations** : l'écart résiduel avec llama.cpp
   (∣ΔNLL∣ médian 0,076) vient de notre int15 à une échelle par vecteur, contre
   le f32 de la référence. C'est le même chantier que les échelles par bloc de
   `DenseQ8` (`REPRISE.md` §6.e).
3. Le reste de `REPRISE.md` §6 (noyaux GPU, contexte long, vision) est inchangé.

