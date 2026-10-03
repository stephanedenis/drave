# Sprint 16 — Le poste dominant de V4.1 : les experts sur NVMe — mesurer la réutilisation, garder en RAM ce qui se répète, publier le gain

- **Début** : 22:32 · **Fin** : 23:05 (33 min — les mesures étaient courtes :
  la passe V4.1 est à 22 s depuis le bloc 15) · **Objectif** : le poste `proj+mlp`
  (3 530 ms/token à ctx 32) est de la lecture d'experts — mesurer la réutilisation,
  garder en RAM ce qui se répète **sans changer un chiffre**, publier le gain.
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. Le résultat principal est NÉGATIF, et c'est la mesure qui le dit

Le cache RAM d'experts (`DRAVE_EXPERTS_RAM=<Mo>`, LRU par octets) **rend la passe
plus lente**, et d'autant plus qu'on lui donne de mémoire :

| cache RAM | passe ctx 32 (31 jetons) | vs sans cache |
|---|---|---|
| aucun | **145,1 s** | — |
| 4 Go | 151,2 s | **+4 %** |
| 32 Go | 175,5 s | **+21 %** |

La perplexité est identique dans les trois cas (**115 521,8693**) et les 2 544
vides sont **identiques au bit près** : le cache ne change rien au calcul, il
change le temps — en mal. Le mécanisme est clair : **le noyau fait déjà ce
travail**. `buff/cache` garde ~95 Go de pages du fichier ; recopier les experts en
espace utilisateur ajoute un second exemplaire (mémoire + `memcpy` à chaque
lecture manquée) **sans retirer les lectures NVMe**, puisque les pages étaient
déjà résidentes. Plus le budget est grand, plus il y a de copies, plus c'est lent.

Le drapeau reste, **éteint par défaut**, et son annonce porte son verdict : c'est
la seule façon de re-mesurer là où le cache de pages est petit.

### 2. La trace qui rendait l'idée plausible (et pourquoi elle ne suffisait pas)

`DRAVE_TRACE_EXPERTS` sur **63 jetons de wiki réel** (V4.1, 6 experts par couche,
40 couches) :

| mesure | valeur |
|---|---|
| lectures d'experts | 15 360 |
| experts distincts touchés | **3 817** (24,9 % de l'espace) |
| 25 % des lectures | 106 experts (2,3 Go) |
| 50 % des lectures | **394 experts (8,5 Go)** |
| 75 % des lectures | 1 177 experts (25,3 Go) |
| 90 % des lectures | 2 281 experts (49,0 Go) |
| réutilisation entre jetons **consécutifs**, même couche | **31,9 %** des lectures |

Des lectures qui se concentrent sur 10 % des experts et un tiers de réutilisation
immédiate : tout disait qu'un cache en RAM devait gagner. Ce qui manquait dans le
raisonnement n'était pas dans la trace — c'était **le cache de pages du noyau**,
qui exploite déjà cette réutilisation, gratuitement.

### 3. Un vrai défaut trouvé en chemin, et corrigé

En écrivant le cache, l'expert 0 se copiait juste et les suivants non : le pas
entre experts était faux d'un **facteur 8** pour tous les formats quantifiés par
grille (ceux de V4.1). La cause : `Vue4.nb` compte des blocs de **32** pour tous
les formats sauf Q4_K/Q6_K, alors que `pas()` d'une grille est la taille d'un
**super-bloc de 256** — le produit `n_out × nb × pas()` surestimait l'expert.

Ce pas servait à la **prélecture** (`prelire_expert`) et à `expert()` : la
prélecture visait donc huit experts plus loin que celui qui allait être lu — un
défaut discret, qui ne change aucun chiffre mais qui gaspille les lectures
demandées. Corrigé par `Vue4::octets_expert()`, une seule expression pour les deux
chemins (lecture et prélecture).

## Rétrospective — garder / changer / doute

**Garder.**

- **Mesurer avant d'optimiser, même quand l'intuition est forte.** La trace donnait
  quatre chiffres qui poussaient tous dans le même sens ; la mesure de la passe a
  dit le contraire en trois minutes. Sans elle, le cache serait entré dans le
  dépôt comme une « optimisation » à +21 %.
- **Un drapeau de comparaison porte son verdict.** `DRAVE_EXPERTS_RAM` annonce
  désormais qu'il est mesuré plus lent, et pourquoi : personne ne le rallumera en
  croyant bien faire.

**Changer.**

- **Chercher le cache existant avant d'en écrire un.** Le noyau tenait déjà 95 Go
  de pages du modèle ; je l'ai découvert en mesurant, pas en lisant. La question à
  poser d'abord : « qui cache déjà ces octets, et à quel coût ? »
- **La trace ne mesure pas ce que coûte un octet servi.** Elle mesure la
  réutilisation logique ; elle ne dit rien de la hiérarchie mémoire. Un chiffre de
  réutilisation n'est pas une prédiction de gain.

**Doute.**

- Le verdict est mesuré à **ctx 32 sur 31 jetons**, sur une machine à 125 Go de
  RAM dont 95 en `buff/cache`. Sur une machine à 16 Go, ou sur une passe de
  1 024 jetons (où le cache de pages ne tient plus le flux), le même cache
  pourrait gagner : c'est pourquoi le drapeau reste.
- Le cache n'a pas été mesuré avec un budget **plus petit que la réutilisation
  immédiate** : ~1 Go ne copierait que les experts du jeton précédent, et le
  `memcpy` resterait payé à chaque manque.

## Planning du bloc 17 — grappes d'experts par CHALEUR mesurée

Le vrai levier n'est pas de cacher les octets, c'est d'en lire **moins**, ou de
les lire **mieux**. P9 l'a déjà démontré sur V4-Flash : le même calcul, mêmes
chiffres, 86,9 Go en 3 tranches = **111,8 s** contre 8 grappes = **39,9 s**
(×2,8), uniquement parce que les experts d'un jeton se trouvaient dans une région
plus étroite du disque.

Chantiers du bloc 17 :

1. **Re-trier par chaleur** : la trace du bloc 16 donne la fréquence de chaque
   expert ; `tools/clusters_moe.py` et `--clusters` savent déjà fabriquer des
   grappes. Construire une copie de V4.1 dont les experts sont rangés par
   fréquence décroissante (les 394 qui font 50 % des lectures d'abord), puis
   mesurer : lectures par jeton, secondes par jeton, **et vérifier la perplexité
   au chiffre près** (le re-tri ne doit rien changer au calcul).
2. **Mesurer l'effet du désordre** avant/après (lectures groupées contre
   aléatoires) : `proj+mlp` du profil, plus `/proc/diskstats` si utile.
3. **Publier** le gain à ctx 8 et ctx 32, avec la taille de la copie re-triée — et
   si le gain ne vient pas, l'écrire aussi.

## Portes

- `tools/portes.sh rapide` : voir le journal du bloc (63 tests, Qwen 19,3885,
  clusters 799,8557, V4-Flash 8430,4966, engram, cinq modes de flux).
- V4.1 : perplexité 115 521,8693 (ctx 32) et 1 743 713,6243 (ctx 8) **inchangées**
  dans toutes les variantes mesurées ; 2 544 vides identiques au bit près.

## Ce qui reste, nommé

- **Le cache RAM d'experts est un résultat négatif**, pas un chantier : il reste
  éteint, documenté, et re-mesurable ailleurs.
- **`proj+mlp` reste le poste dominant** (3 530 ms/token à ctx 32) : c'est de la
  lecture d'experts, et le remède est structurel (re-tri, grappes), pas un cache.
- Le **SIMD f32** (bloc 15) attend toujours sa décision : il change des bits, donc
  la référence de non-régression.
