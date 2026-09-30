# Compacité de la trace — le disque paie trois fois le câble

> **Fait depuis (même jour).** La variante « écarts » est **implémentée et
> mesurée** dans le moteur (DRVF v2, lecteur rétrocompatible v1) : trace dense de
> 512 jetons **132 396 736 → 66 370 408 octets (−49,87 %)**, rejeu `--flux-forcer`
> **identique** (perplexité 19,3885 dans les deux cas), et la relecture par
> `tools/flux_codec.py` — l'implémentation indépendante — donne exactement les
> mêmes 24 576 listes et 22 008 776 neurones actifs. Le rejeu annonce maintenant
> ses compteurs (`N listes servies, M manquantes`), ce qui a mis au jour une
> trace ancienne dont les clés étaient décalées d'un jeton : elle se rejouait en
> silence avec une perplexité fausse (1958,72 au lieu de 19,3885).
>
> **Et la v3 est faite** (`DRAVE_TRACE_BLOCS=1`) : valeurs i8 + échelle f16 par
> bloc de 32 canaux. Mesuré sur la même trace dense : **45 079 930 octets**
> (−65,9 % par rapport à la v1, −32,1 % par rapport à la v2), au prix de
> **+0,074 % de perplexité au rejeu** (19,4029 contre 19,3885) et d'une erreur par
> valeur de **0,085 % RMS** du max de la liste — la prévision de ce rapport était
> 0,077-0,081 %, elle tient. La v3 est avec perte, donc la v2 reste le défaut.
>
> Reste : l'emballage zstd en étape EXTERNE (−79 % au total, mesuré ici) — le
> moteur est en `std` seul, il n'embarque pas de compresseur, et c'est très bien
> ainsi : `zstd -19` sur le fichier fait le travail sans une ligne de code.

**En une ligne** : la trace DRVF v1 coûte **6,04 octets par neurone actif** quand
le transport en coûte ~2 ; les **indices u32 en sont les deux tiers**, et les
ramener à un octet par écarts divise la trace par deux **sans perdre un seul
indice** — le reste (valeurs i8, échelles f16, zstd) porte le total à **−79 %**.

Mesures faites avec `tools/trace_compacite.py`, qui lit les traces avec
`tools/flux_codec.py` (l'implémentation de référence validée contre le Rust) et
ne fait que compter des octets : aucune troisième lecture du format n'a été
écrite.

---

## 1. L'incohérence, chiffrée avant d'être corrigée

Le disque et le réseau encodent la même information — une liste creuse valuée —
mais plus de la même façon :

| | indices | valeurs | échelles | coût par neurone actif |
|---|---|---|---|---|
| **disque, DRVF v1** | u32, 4 octets | i16, 2 octets | f32, 1 par liste | **6,04** (mesuré) |
| **réseau, mode 1** | u16, 2 octets | i16, 2 octets | f32, 1 par liste | 4 |
| **réseau, mode 2** (`--flux-blocs`, écarts) | **u8**, 1 octet | **i8**, 1 octet | f32, 1 par bloc de 32 | **~2** |

Autrement dit : ce qui circule sur le câble coûte trois fois moins cher que ce
qui dort sur le disque, pour la même information. Le mode 2 a été écrit et
mesuré pour le transport (`reports/rapport-transport-liste.md`) ; le disque, lui,
est resté à l'encodage de la phase 0.

## 2. Protocole de mesure

Deux traces **réelles** du projet, toutes deux en DRVF v1, relues telles quelles :

| trace | contenu | taille | neurones actifs | densité |
|---|---|---|---|---|
| `/tmp/flux_sparse.bin` | Qwen2.5-0.5B Q8_0, 256 jetons, 24 couches, seuil 0,05 | **53 092 562 o** | 8 791 414 | 39,9 % |
| `/tmp/flux_f32.bin` | même modèle, 512 jetons, `--abits 16` (rien n'est seuillé) | **132 396 736 o** | 22 008 776 | 99,9 % |

Ce sont les deux traces citées par le projet (« 132 Mo pour 512 jetons, 53 Mo en
version creuse »). Chaque variante est calculée **sur le même contenu** : on ne
rejoue ni le seuil ni le top-k, on ré-encode exactement les neurones actifs déjà
présents dans la trace.

Coût de chaque variante, par liste :

| variante | en-tête de liste | indices | valeurs | échelles |
|---|---|---|---|---|
| `actuel` | 10 o + échelle f32 | 4 o × actif | 2 o × actif | 4 o / liste |
| `écarts+i16` | 10 o + échelle f32 | 1 o × actif (+2 o par échappement) | 2 o × actif | 4 o / liste |
| `écarts+blocs` | 10 o + 8 o de queue | idem | 1 o × actif | 4 o / bloc de 32 canaux |
| `blocs f16` | idem | idem | 1 o × actif | **2 o** / bloc de 32 canaux |

Plus l'en-tête de fichier (14 o) et la sentinelle de fin (2 o, présente sur la
trace dense seulement). L'échappement d'indice coûte **3 octets** (le marqueur
255 **et** l'indice absolu u16) — c'est le prix de l'irrégularité, et il est
négligeable ici (§4). La conversion f32→f16 est implémentée à la main dans
l'outil (arrondi au plus proche pair) et a été vérifiée contre numpy sur
10 018 valeurs, dénormaux et infinis compris : **0 désaccord**.

## 3. Le tableau — trace creuse (53 Mo, 256 jetons)

| encodage | octets | o/actif | ratio | indices | valeurs | échelles | en-têtes |
|---|---:|---:|---:|---:|---:|---:|---:|
| **actuel** (u32 + i16) | 53 092 562 | 6,04 | 1,00 | 35 165 656 | 17 582 828 | 98 304 | 245 774 |
| écarts + i16 | 26 718 364 | 3,04 | 0,50 | 8 791 458 | 17 582 828 | 98 304 | 245 774 |
| écarts + blocs i8 | 20 777 766 | 2,36 | 0,39 | 8 791 458 | 8 791 414 | 2 752 512 | 442 382 |
| **blocs, échelles f16** | **19 401 510** | **2,21** | **0,37** | 8 791 458 | 8 791 414 | 1 376 256 | 442 382 |
| zstd niv. 3 sur l'actuel | 20 148 081 | 2,29 | 0,38 | — | — | — | — |
| zstd niv. 19 sur l'actuel | 16 157 273 | 1,84 | 0,30 | — | — | — | — |
| gzip niv. 6 sur l'actuel | 23 570 139 | 2,68 | 0,44 | — | — | — | — |
| **zstd niv. 19 sur écarts+blocs** | **11 128 840** | **1,27** | **0,21** | — | — | — | — |

Les lignes de compression du fichier entier sont des mesures réelles ; celles du
tableau affiché par l'outil (échantillon de 16 Mio) donnent 20 225 293 /
16 554 621 / 23 922 712 — l'extrapolation est juste à **2,5 % près**, ce qui a
été vérifié en compressant les 53 Mo entiers.

**Meilleure variante sans compression : `blocs f16`, 19 401 510 octets, −63,5 %.**
**Meilleur résultat tout court : `écarts+blocs` + zstd 19, 11 128 840 octets, −79,0 %.**

## 4. Ce que chaque poste pèse, et pourquoi l'ordre compte

Dans la trace actuelle, deux postes font 99,3 % du fichier :

* **indices u32 : 35 165 656 o = 66,2 %** — pour des indices qui tiennent sur un
  octet dans **99,9997 %** des cas (22 échappements sur 8 791 414, soit 44 octets
  payés sur 35 Mo). C'est le poste le plus gros **et** le moins coûteux à
  corriger : les indices sont déjà triés (propriété du format, vérifiée sur les
  deux traces), donc l'écart au neurone précédent est un petit entier. Le
  décodage reste une seule passe séquentielle, et le code Rust existe déjà
  (`recevoir_flux`, mode 2) : c'est du **rangement**, pas un nouveau format.
* **valeurs i16 : 17 582 828 o = 33,1 %** — le seul poste où l'on perd quelque
  chose. Le passage à i8 + échelle par bloc de 32 canaux en reprend 13,2 % en
  échelles : le gain net est de 5,94 Mo (−22 % de plus), pour une erreur RMS de
  **0,077 % du max de la liste**. Les échelles en f16 reprennent encore 1,38 Mo
  (7 % de la v2) sans toucher aux valeurs.
* **échelles + en-têtes : 0,65 %** du fichier actuel. Négligeables aujourd'hui,
  ils deviennent 15,4 % de la v2 : c'est le poste à surveiller ensuite, pas
  celui à optimiser d'abord.

Détail utile pour le décodage : les échelles de blocs émises sont 28 par liste
(896 canaux / 32), dont **99,6 % utiles** sur la trace creuse et **100 %** sur la
dense. Ne pas émettre les échelles des blocs vides ne gagnerait que 10 ko sur
53 Mo : ce n'est pas un levier, et garder l'indexation directe par bloc
(`echelles[i/32]`) est plus simple et plus robuste.

## 5. La trace dense (132 Mo, 512 jetons)

| encodage | octets | o/actif | ratio |
|---|---:|---:|---:|
| **actuel** (u32 + i16) | 132 396 736 | 6,02 | 1,00 |
| écarts + i16 | 66 370 406 | 3,02 | 0,50 |
| écarts + blocs i8 | 47 212 446 | 2,15 | 0,36 |
| **blocs, échelles f16** | **45 836 190** | **2,08** | **0,35** |
| zstd niv. 3 sur l'actuel | 41 675 229 | 1,89 | 0,31 |
| zstd niv. 19 sur l'actuel | 50 009 567 | 2,27 | 0,38 |
| gzip niv. 6 sur l'actuel | 80 012 553 | 3,64 | 0,60 |
| **zstd niv. 19 sur écarts+blocs** | **26 634 831** | **1,21** | **0,20** |

Les trois lignes de compression de l'actuel sont mesurées sur le fichier entier ;
l'outil, lui, projette depuis un échantillon de 16 Mio et donne 41 590 308 /
50 117 157 / 79 615 302, soit un écart de **0,2 % à 0,5 %** — l'extrapolation est
fiable sur les deux régimes.

Deux enseignements que la trace creuse ne donnait pas :

1. **Aucun échappement** sur 22 008 776 indices : quand la liste est presque
   pleine, les écarts valent 1 et l'encodage par écarts est encore plus efficace
   qu'en régime creux. Le coût de l'échappement est un non-sujet.
2. **zstd niveau 19 fait moins bien que le niveau 3** sur le format actuel
   (50,1 Mo contre 41,6 Mo). Vérifié sur quatre segments du fichier : ce n'est
   pas un artefact d'échantillon. Les 132 Mo de i16/u32 peu corrélés ne
   récompensent pas la recherche exhaustive du compresseur ; **le gain n'est pas
   dans la force brute, il est dans le format**. Sur la v2, en revanche, le
   niveau 19 redevient meilleur (26,6 contre 29,6 Mo) : un format plus régulier
   se compresse mieux, y compris par un compresseur plus exigeant.
3. Le passage i8 gagne **relativement plus** en dense (−29 %) qu'en creux
   (−22 %) : les 28 échelles de blocs y sont amorties par 896 valeurs pleines,
   alors qu'en régime creux elles se paient sur 358 actifs par liste.

## 6. Effet sur les traces déjà mesurées du projet

Application des ratios mesurés (projection linéaire — la propriété « la taille
suit l'activité » est déjà vérifiée par le projet : densité ÷2,3 → trace ÷2,5) :

| trace | aujourd'hui | v2 (i8, échelles f32) | v2 (échelles f16) | v2 + zstd 19 | gain total |
|---|---:|---:|---:|---:|---:|
| creuse, 256 jetons | 53,1 Mo | 20,8 Mo | 19,4 Mo | **11,1 Mo** | **−79 %** |
| dense, 512 jetons | 132,4 Mo | 47,2 Mo | 45,8 Mo | **26,6 Mo** | **−80 %** |
| dense, 1 024 jetons | ~265 Mo | ~94 Mo | ~92 Mo | ~53 Mo | −80 % |
| dense, 4 096 jetons | ~1,06 Go | ~378 Mo | ~367 Mo | ~213 Mo | −80 % |
| dense, 8 192 jetons | ~2,12 Go | ~755 Mo | ~733 Mo | ~426 Mo | −80 % |

La compression est mesurée sur la v2 **i8 à échelles f32** (donc un majorant : avec
les échelles f16, le fichier est plus petit avant compression).

À l'échelle du contexte 8 192 déjà utilisé pour l'attribution du cache KV, la
trace passe de **2,1 Go à 0,4 Go**. C'est ce qui rend la trace utilisable comme
artefact de travail, et non plus comme pièce à conviction qu'on hésite à écrire.

## 7. Recommandation pour DRVF v2

### À changer

1. **Indices par écarts, un octet, échappement 255 → u16 absolu.** Gain
   **−49,7 %** (creux) et **−49,9 %** (dense) **à information identique** : c'est
   du rangement, prouvé par la trace (22 échappements sur 8,79 M). C'est le
   premier changement à faire, et il ne demande aucune décision de qualité.
2. **Valeurs i8 + une échelle f32 par bloc de 32 canaux** (le mode 2 du réseau,
   à l'octet près). Gain supplémentaire **−22 %** (creux) / **−29 %** (dense),
   pour une erreur RMS de 0,08 % du max de la liste. Le seuil, lui, reste global :
   c'est lui qui décide de la sparsité, donc de la taille.
3. **Échelles en f16** plutôt que f32. Gain **−6,6 % de la v2** (1,38 Mo sur la
   creuse), pour une précision d'échelle largement suffisante (une échelle n'a
   pas besoin de 24 bits de mantisse : elle borne une dynamique *intra-bloc*).
   La conversion est triviale et déjà écrite dans l'outil.
4. **zstd sur le fichier, pas sur le flux.** C'est le levier le plus fort :
   −79 % au total, mais il ne s'applique **qu'au stockage**. Sur le réseau, un
   flux pèse 1,5 ko et c'est la latence qui coûte (`attente ≈ calcul + 3,2 ×
   latence`) : compresser un flux de 1,5 ko n'apporte rien et ajoute un aller-
   retour de négociation. Le zstd doit être un **emballage de fichier**
   (`.drvf.zst`, comme un `.gz`), pas une couche du protocole — le format reste
   lisible tel quel, l'emballage est optionnel.

### À ne pas changer

* **La magie et la version dans l'en-tête**, et le refus explicite d'un pair ou
  d'un fichier d'une autre version : c'est ce qui a évité les divergences
  silencieuses de la phase 3.5, et une v2 qui ne se nomme pas serait un piège.
* **L'en-tête de liste : couche u16, `jeton` u32 GLOBAL, `n_actifs` u32.**
  Le compteur global n'est pas un détail : c'est le bug qui a donné une
  perplexité de **356 694** au lieu de 17,43 quand on y avait mis la position.
  Et `n_actifs` explicite permet de sauter une liste sans la décoder — c'est ce
  qui rend le rejeu et la relecture partielle possibles.
* **L'ordre trié des indices.** C'est lui qui rend les écarts possibles ; le
  casser coûterait 2 octets par actif et un tri au décodage.
* **L'échelle f32 par liste du mode 1 réseau.** Les pairs actuels la lisent ;
  la v2 disque peut adopter le mode 2 sans retirer le mode 1 du protocole.
* **La sentinelle 0xFFFF et la lecture des traces v1.** Les 132 Mo et 53 Mo
  existants doivent rester relisibles par `flux_codec.py` et par le moteur :
  un format de trace qu'on ne peut plus relire est un format qu'on n'aurait pas
  dû adopter.
* **L'unicité disque/câble.** La v2 du disque doit être le **corps du mode 2**,
  comme la v1 était le mode 1 à l'octet près. Réinventer un troisième encodage
  pour le fichier recréerait exactement l'incohérence que ce rapport mesure.
* **La lisibilité.** Un `flux_codec.py` qui décode encore la v2 en dix lignes
  vaut mieux qu'un format « optimal » que seul son auteur sait relire.

### Ce qu'il reste à valider avant de basculer

1. **Le rejeu.** La trace n'est pas qu'un journal : `--flux-forcer` la
   réinjecte, et le contrat est « mêmes logits » (perplexité **19,3885** avec et
   sans rejeu en i16). Le i8 par bloc n'a jamais été testé sur la trace
   **normée** ; l'erreur mesurée ici (0,08 % du max) plaide pour, mais c'est le
   rejeu qui décide. Si l'écart dépasse le bruit, la v2 doit garder i16 pour les
   valeurs et ne prendre que les indices — elle gagnerait déjà 50 %.
2. **L'aller-retour Rust ↔ Python identique** sur les deux traces, comme pour la
   v1 : c'est ce test qui a validé le format une première fois.
3. **La rétrocompatibilité** : le décodeur v2 doit lire une trace v1, sinon les
   mesures déjà publiées deviennent des fichiers morts.

### Ordre d'exécution conseillé

| étape | gain cumulé (trace creuse) | risque |
|---|---:|---|
| indices par écarts u8 | −49,7 % | aucun (rangement) |
| + valeurs i8 et échelles par bloc | −60,9 % | qualité, à valider par rejeu |
| + échelles f16 | −63,5 % | aucun |
| + zstd 19 à l'écriture du fichier | **−79,0 %** | aucun (emballage optionnel) |

## 8. Ce que l'outil ne dit pas

* Il mesure des **tailles**, pas la perplexité du rejeu : les deuxièmes sont dans
  `reports/rapport-transport-liste.md` et devront être refaites sur la trace
  normée en v2.
* Il ne mesure pas le **temps de décodage** de la v2. L'attendu est neutre ou
  meilleur (une passe séquentielle, moins d'octets à lire), mais ce n'est pas
  mesuré ici.
* Les projections par nombre de jetons supposent une activité moyenne constante
  par jeton ; c'est vrai sur ces traces, ça ne le sera pas forcément sur une
  séquence dont la densité dérive en cours de génération.
