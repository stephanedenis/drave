# Rapport — l'empreinte mémoire : ce qui réduit vraiment ce qu'il faut charger

Session du 01/10, de 10 h 47 à 17 h 35. Modèle d'étude : Qwen3-30B-A3B
(48 couches, 128 experts, top-8), dont on sait produire les traces de routage.
Cible : DeepSeek-V4.1-Flash (40 couches, **384 experts**, top-6, 365,7 Go).

**Résultat principal** : l'empreinte de V4.1 tombe de 365,7 Go à **50–80 Go**,
non pas en découpant les experts mais parce que **56 % du modèle (203 Go) est une
table d'engram creuse par nature**, qu'il suffit de mmapper. Une session de
10 000 jetons n'en touche que **4,6 Mo**.

## La question

Un modèle de 365 Go ne tient pas dans 125 Go de RAM. Que peut-on **ne pas
charger** ? Et parmi les pistes — découpage plus fin, grappes par langue, cache,
restriction du vocabulaire — lesquelles paient réellement ?

Toutes les mesures qui suivent viennent de traces de routage réelles
(`DRAVE_TRACE_EXPERTS`), pas d'estimations.

## 1. La granularité : la courbe s'arrête à l'expert

Volume lu par appel utile, quand un expert manque et qu'on charge sa grappe :

| taille de grappe | cache 16 | cache 32 | cache 64 |
|---|---|---|---|
| 64 experts | 59,64 | 51,69 | 5,31 |
| 16 | 9,72 | 5,73 | 0,87 |
| 4 | 2,47 | 0,92 | 0,16 |
| **1 expert** | **0,40** | **0,21** | **0,04** |

La courbe s'améliore à chaque division **parce qu'on se rapproche de l'expert**.
En dessous, il n'y a pas de signal : **un expert est l'unité que le routeur
décide**, un neurone ne l'est pas.

Et la sparsité des activations, elle, **n'est pas exploitable** :

| seuil d'activation | perplexité | facteur |
|---|---|---|
| 0 (référence) | **7,6139** | — |
| 0,05 | 2 182,37 | **×287** |
| 0,10 | 10 592,25 | ×1 391 |
| 0,25 | 727 099,03 | ×95 500 |

Seulement 12,5 % des neurones tirent, et les 10 % les plus lourds portent 82 à
86 % de la masse — mais **couper les autres détruit le modèle dès 5 %**.

*Au passage : `matvec_q4` calcule une liste creuse puis **reconstruit un vecteur
dense** avant le produit. Le compteur le confirme — « projections : 0,0 M
événements par token ». La sparsité est calculée et jetée.*

## 2. Le vocabulaire : 13 %, et c'est un plafond de fait

Tokenisation de 8,3 Mo de français (3 050 991 jetons) avec le tokenizer de Qwen3
(151 936 tokens) :

| jetons lus | identifiants distincts | % du vocabulaire |
|---|---|---|
| 10 000 | 1 462 | 0,96 % |
| 100 000 | 4 659 | 3,07 % |
| 1 000 000 | 15 768 | 10,38 % |
| 3 050 991 | **19 793** | **13,03 %** |

Exposant de Heaps ≈ **0,21** : la couverture croît très lentement. Atteindre 50 %
demanderait des milliards de jetons. **13 % est un plafond de fait.**

### Le piège qu'il fallait éviter

| | perplexité |
|---|---|
| complète (151 936 tokens) | **25,3748** |
| restreinte aux 19 793 tokens français | **24,3108** |

La perplexité restreinte **baisse** — ce n'est pas un gain : en retirant des
tokens on retire de la masse au dénominateur du softmax. **Deux perplexités
calculées sur des vocabulaires différents ne sont pas comparables.**

La mesure comparable est le **rang** :

| | |
|---|---|
| rang médian du vrai token | **3** |
| p90 | 250 |
| maximum | 4 319 |

| vocabulaire gardé | vrais jetons présents |
|---|---|
| top-1 024 | 96,1 % |
| top-4 096 | 99,2 % |
| **top-16 384** | **100,0 %** |

### La langue de sortie suit celle de l'entrée

Sur 127 positions d'un texte français : **top-1 français dans 126 cas (99,2 %)**.
Masse hors vocabulaire français : médiane **0,44 %**, mais maximum 40,4 %.

Combien de tokens portent la masse :

| position | rang du vrai token | 99 % de la masse | 99,9 % |
|---|---|---|---|
| 0 | 1 087 | **20 212** | 50 999 |
| 42 | 11 | 101 | 176 |
| 84 | 3 | **9** | 9 |
| 126 | 1 | **2** | 4 |

**Confiant : 2 à 9 tokens. Incertain : 20 000.** La restriction linguistique
(13 %) est toujours sûre ; une restriction plus agressive ne l'est que pour la
génération.

## 3. Les experts ne sont pas organisés par langue

Trois corpus de 1 024 jetons (français, anglais, code), même modèle :

| paire | Jaccard des experts | corrélation des fréquences |
|---|---|---|
| français / anglais | 0,752 | **r = 0,102** |
| français / code | 0,903 | r = 0,821 |
| anglais / code | 0,751 | **r = −0,009** |
| **français / français** (référence interne) | **0,805** | r = 0,995 |

Le recouvrement entre langues est **au niveau de la variabilité interne d'une
seule langue**. Experts « propres » à une langue : **1,7 à 3,1 %**.

Mais la **fréquence** diffère (r = 0,10), et un classifieur par plus proche
voisin reconnaît le corpus d'origine dans **79,8 %** des cas. **La langue est
lisible dans le routage — par des rééquilibrages de fréquence, pas par des
experts dédiés.** Les mêmes experts servent, dans des proportions différentes.

*(Réserve : le corpus « code » contient les commentaires français de `tools/*.py`,
d'où le r = 0,82 avec le français. Le couple propre est français/anglais.)*

## 4. Un token ne prédit pas ses experts

Jaccard entre les occurrences du même token (tokens vus ≥ 4 fois) :

| couche | 0 | 8 | 20 | 36 |
|---|---|---|---|---|
| Jaccard | **0,499** | 0,088 | 0,056 | 0,065 |

Au-delà de la couche 0, c'est **au niveau du hasard**. Le routage dépend de la
représentation **contextuelle**, pas du token. Le « dictionnaire de
dictionnaires » token → neurones ne peut pas exister.

## 5. Le miroir : confirmé, mais pas celui qu'on croyait

| | Jaccard du même token |
|---|---|
| couches extrêmes (0-3, 44-47) | **0,259** |
| couches médianes (20-27) | **0,056** |

**Facteur 4,6**, forme en U nette : les couches extrêmes portent le lexical, le
milieu l'abstrait. L'entrée est plus marquée que la sortie (0,499 contre 0,349).

**Mais le miroir croisé n'existe pas** :

| paire | Jaccard |
|---|---|
| 0 / 47 | 0,030 |
| 1 / 46 | 0,028 |
| voisines (l, l+1) | 0,034 |

Les couches symétriques ne partagent rien. Le miroir est une propriété de chaque
couche, pas une correspondance entre couches.

## 6. La découverte : une périodicité de 12 couches

| écart entre couches | Jaccard moyen |
|---|---|
| 1 à 11 | ~0,035 |
| **12** | **0,323** |
| 16, 20 | ~0,035 |
| **24** | **0,210** |

Les 14 paires les plus fortes ont **toutes** un écart de 12 :

```
16/28 : 0.549    15/27 : 0.503    12/24 : 0.477    8/20  : 0.465
20/32 : 0.531    28/40 : 0.498    14/26 : 0.477   23/35  : 0.465
21/33 : 0.518    18/30 : 0.485    17/29 : 0.475   19/31  : 0.461
```

**Les experts de la couche L et de la couche L+12 se recouvrent à 32–55 %,
contre 3,5 % pour tout autre écart.** Le modèle a une structure en **4 blocs de
12 couches** qui réutilisent les mêmes experts.

**Ce que ça ne permet pas** : ces experts sont des tenseurs **différents**.
La périodicité dit qu'ils sont *appelés ensemble*, pas qu'ils sont *identiques*.
Aucune économie de stockage directe.

## 7. La réductibilité est uniforme

Combien d'experts garder pour couvrir X % des appels :

| | 90 % | 99 % | Gini |
|---|---|---|---|
| couches extrêmes | 60,0 | 92,2 | 0,575 |
| couches médianes | 60,1 | 92,0 | 0,560 |
| couches intermédiaires | 59,1 | 92,1 | 0,576 |

**Aucune différence.** Cibler « les extrêmes » n'apporte rien. Une exception,
mais à la sortie seulement :

| couche | 90 % | 99 % |
|---|---|---|
| **47** | **36** | 64 |
| 0 | 74 | 108 |

**Le top-k minimal d'un cache utile est le top-k du routeur** : en dessous de 8
experts, un cache ne sert **à rien** (0 % de succès — un jeton consomme ses 8
experts d'un coup).

### L'allocation par couche n'apporte rien non plus

| budget/couche | mémoire | uniforme | adaptatif | gain |
|---|---|---|---|---|
| 16 | 2,34 Go | 59,6 % | 59,6 % | −0,0 % |
| 32 | 4,68 Go | 79,0 % | 79,2 % | **+0,2 %** |
| 48 | 7,03 Go | 89,4 % | 90,6 % | +1,2 % |

Les couches diffèrent par leur concentration, mais leurs courbes de cache sont
**parallèles** : le gain marginal décroît au même rythme partout.

### Le pré-remplissage par langue ne sert à rien

| pré-remplissage | → français | → anglais |
|---|---|---|
| aucun (à froid) | 77,9 % | 78,5 % |
| chauds du français | 78,0 % | 78,5 % |
| chauds de l'anglais | 78,0 % | 78,6 % |

Le cache atteint son régime en **32 jetons** (59 % à 8 jetons, 80,5 % à 32).
Toute prédiction se heurte au même mur : ce qui coûte cher est le régime
permanent, et le cache y arrive seul.

## 8. LA DÉCOUVERTE : 56 % du modèle n'est pas un modèle de poids

Décomposition des 365,7 Go de DeepSeek-V4.1-Flash, par famille de tenseurs :

| famille | Go | % |
|---|---|---|
| **engram** | **203,4** | **55,6 %** |
| experts (MoE) | 152,9 | 41,8 % |
| attention (MLA) | 5,4 | 1,5 % |
| embedding + tête | 2,0 | 0,6 % |
| expert partagé | 1,5 | 0,4 % |
| indexeur / compresseur KV | 0,1 | 0,0 % |
| hyper-connections, normes, biais | 0,0 | 0,0 % |

Le plus gros tenseur du modèle n'est pas un expert : c'est
**`blk.N.engram_embd.weight`, à 101,4 Go par couche** (deux couches : 1 et 14),
en I8, de forme `[384 006 168, 264]`.

Or **ce n'est pas un tenseur de poids, c'est une table à accès aléatoire** :

| | |
|---|---|
| entrées | 384 006 168 par couche |
| taille d'une entrée | 264 octets |
| ce qu'elle indexe | des **n-grammes** jusqu'à 4 tokens |
| hâchage | 48 nombres premiers |
| vocabulaire comprimé | 99 092 |

Chaque jeton ne lit que les entrées de **ses** n-grammes. La charger serait une
faute de conception : c'est le cas d'usage exact du `mmap`.

### Combien d'entrées une session touche-t-elle vraiment ?

Sur 3 050 991 jetons de français :

| jetons | 1-gram | 2-gram | 3-gram | 4-gram | **total** | **mémoire du cache** |
|---|---|---|---|---|---|---|
| 1 000 | 411 | 762 | 880 | 924 | **2 977** | **0,8 Mo** |
| 10 000 | 1 462 | 3 953 | 5 596 | 6 265 | 17 276 | 4,6 Mo |
| 100 000 | 4 659 | 20 745 | 36 094 | 47 735 | 109 233 | 28,8 Mo |
| 1 000 000 | 15 768 | 132 627 | 277 627 | 409 984 | 836 006 | 220,7 Mo |
| 3 050 991 | 19 793 | 227 495 | 556 188 | 880 394 | 1 683 870 | **444,5 Mo** |

**Une session de 10 000 jetons touche 4,6 Mo d'une table de 101 Go.** Le rapport
est de 1 pour 22 000. La table entière n'a jamais besoin d'être en mémoire : le
`mmap` la rend adressable, et le noyau garde chaudes les quelques pages touchées.

## 9. Trois dernières pistes, et pourquoi elles ne paient pas

### La localité temporelle existe, mais ne suffit pas

Le jeton suivant réutilise-t-il les experts du précédent ?

| couche | réutilisation | hasard |
|---|---|---|
| 0 | 27,3 % | 6,2 % |
| 12 | **49,8 %** | 6,2 % |
| 24 | 45,5 % | 6,2 % |
| 47 | **51,9 %** | 6,2 % |

**Facteur 4 à 8 sur le hasard.** Un cache « experts du jeton précédent » — 8
entrées, prédiction gratuite — sert 27 à 52 % des appels. Mais un LRU de 32 fait
**78 %** : la localité temporelle est réelle et insuffisante.

### Les experts d'un jeton sont « rangés », mais ça n'aide pas sur NVMe

Étendue moyenne des rangs (experts ordonnés par fréquence) :

| couche | étendue | hasard |
|---|---|---|
| 0 | 68,6 | 99,6 |
| 24 | 60,1 | 99,6 |
| 47 | **30,8** | 99,6 |

Les experts d'un même jeton sont plus groupés que le hasard — c'est ce
qu'exploite `convertisseur --trace`, qui les réordonne par fréquence. Mais lire
par bloc contigu coûterait 30 à 70 experts au lieu de 8. **Sur NVMe, où il n'y a
pas de seek, lire 8 experts dispersés coûte exactement ce qu'ils pèsent.** La
localité ne paierait que sur disque mécanique — disqualifié par ailleurs
(0,06 Go/s en aléatoire).

### Le préchargement ne peut rien masquer

Le calcul d'une couche coûte **0,6 ms**, sa lecture **10,9 ms** : un rapport de
**18×**. Un préchargement prédictif, même parfait, ne masquerait que **6 %** de
l'attente. C'est le mur qui explique pourquoi aucune des pistes de prédiction
(token, langue, périodicité, jeton précédent) ne se traduit en gain.

## 10. Rejouer notre propre journal : ce que notre usage change

Les 28 sessions du `journal/` (59 Mo, 2,5 M jetons) rejouées à travers le modèle,
comparées aux corpus génériques :

| corpus | 50 % | 70 % | 80 % | 90 % | 99 % |
|---|---|---|---|---|---|
| **journal** (notre usage) | 16,9 | 30,8 | 41,6 | **58,1** | 92,5 |
| français générique | 18,1 | 33,2 | 44,1 | 59,3 | 92,1 |
| **anglais** | **11,4** | **23,0** | **31,6** | **44,5** | **72,7** |
| code | 16,7 | 31,5 | 41,9 | 56,3 | 88,6 |

Et le cache LRU est **le même partout** (78–80 % à 32 experts). Le journal a bien
un profil reconnaissable (70,8 % contre 25 % au hasard) mais **qui ne change pas
l'empreinte**.

**Ce qui la change, c'est la langue** : l'anglais demande **44,5 experts pour 90 %**
contre 59,3 pour le français. Soit, pour V4.1 :

| langue du contenu | 90 % des appels sur | Go d'experts |
|---|---|---|
| français | 46,3 % | **71** |
| **anglais** | **34,8 %** | **53** |

**18 Go d'écart.** Le code et la technique sont massivement anglais : c'est le
régime où V4.1 tiendra le plus facilement.

### Le cache d'engram pour notre usage réel

| jetons | entrées touchées | mémoire | part de la table (384 M) |
|---|---|---|---|
| 1 000 | 2 977 | **0,8 Mo** | 0,0008 % |
| 10 000 | 17 276 | 4,6 Mo | 0,0045 % |
| 100 000 | 109 233 | 28,8 Mo | 0,028 % |
| **2 510 800** (tout le journal) | 1 470 860 | **388 Mo** | **0,38 %** |

**388 Mo couvrent l'intégralité de notre journal** — après quoi l'engram ne
touche plus le disque. Et le vocabulaire de ce corpus fait **19 228 tokens
(12,66 %)**, ce qui confirme le plafond mesuré sur du français générique.

## 11. Ce que ça donne pour DeepSeek-V4.1-Flash

| | par jeton |
|---|---|
| experts (top-6 × 40 couches × 9,95 Mo) | **2,39 Go** |
| **engram (accès par n-gramme)** | **~2 Ko — 264 octets × 4 n-grammes × 2 couches** |
| tête de sortie (129 280 × 5120, F16) | **1,32 Go — 36 % du trafic** |
| embedding (chargé une fois) | 1,32 Go en mémoire |

| levier | trafic par jeton | statut |
|---|---|---|
| base | 3,71 Go | — |
| cache d'experts 25 % (32 par couche) | 1,82 Go | mesuré, à écrire |
| tête restreinte à la langue | **0,70 Go** | mesuré (top-1 à 99,2 %) |
| **empreinte mémoire, engram mmappé** | **45 à 78 Go** selon le cache d'experts | tient dans 125 Go |
| dont engram | **0 à 0,5 Go** (mmappé, cache de n-grammes) | au lieu de 203 Go |
| VRAM (2 Quadro, 32 Go) | 3 200 experts = 21 % du total | `CacheExperts` existe |

Sans cache, un jeton relit 551 424 experts pour 6 144 distincts — **un facteur 90
de relecture**. Le cache de 25 % élimine 99 % de ces relectures.

## 9. Les mesures d'infrastructure prises en chemin

| support | débit | note |
|---|---|---|
| VRAM (2 GPU) | ~750 Go/s | 9,7 Go en 13 ms (banc KV int4) |
| RAM | ~20 Go/s | memcpy, recoupé par le banc KV |
| NVMe, aléatoire, blocs 4 Mo | **5,5 Go/s** | cache chaud |
| NVMe, séquentiel | 2,1 Go/s | documenté |
| disque mécanique, séquentiel | 0,21 Go/s | écriture soutenue |
| **disque mécanique, aléatoire** | **0,06 Go/s** | 62,9 Go en 1 098 s — **3,5× pire** |

**Le disque mécanique est disqualifié pour le chargement à la demande** :
2,39 Go par jeton y coûteraient 40 s. Seul le NVMe convient.

*Incident de mesure, consigné : mon premier test de disque froid ne vérifiait pas
le retour de `pread` et a chronométré ce disque à **2 211 Go/s**. C'est le chiffre
absurde qui a alerté, pas le test. `O_DIRECT` échoue par ailleurs ici (errno 29),
donc le régime réellement froid n'est pas mesuré proprement.*

## 12. La conclusion : ce qu'il faut charger avant d'opérer

| | poids total | à charger | rapport |
|---|---|---|---|
| engram (2 couches) | 202,8 Go | **0,4 Go** (cache de n-grammes d'une session) | **1 / 500** |
| experts (40 couches) | 152,9 Go | 38 à 71 Go (cache de 25 à 90 %) | 1 / 4 à 1 / 2 |
| attention, embeddings, tête | 10,0 Go | 10,0 Go | 1 / 1 |
| **total** | **365,7 Go** | **~50 à 80 Go** | **1 / 5 à 1 / 7** |

**DeepSeek-V4.1-Flash tient dans 125 Go de RAM** — non parce qu'on découpe les
experts, mais parce que **56 % du modèle est une table creuse par nature** que
personne n'a besoin de charger.

C'est aussi la réponse à la question posée au début de la session : ce qu'il faut
réduire, ce ne sont ni les experts ni les couches, c'est **la table d'engram**.

## 13. Ce qui reste à faire

0. **Adapter l'empreinte à la langue** : 53 Go en anglais contre 71 en français.
   Le détecteur de langue existe déjà par le routage (79,8 %).
1. **L'accès mmappé à l'engram** : c'est la brique principale, et elle divise
   l'empreinte par 5 à lui seule. Elle est **plus simple** que le cache
   d'experts : pas de LRU à écrire, le noyau fait le travail.
2. **Le cache d'experts adossé au disque** : index `(couche, expert) → (fichier,
   offset, taille)` et le LRU qui existe déjà pour la VRAM. C'est la brique
   principale, et elle divise le trafic par 5.
2. **La tête restreinte par langue** : −30 % de trafic, le top-1 y est toujours.
3. **Le `forward` de `deepseek4`** : MLA réel, routage `noaux_tc`, IQ1_M/IQ2_XXS.
   Sans lui, aucune de ces mesures ne peut être refaite sur la cible.
4. **Les hyper-connections et l'engram** de V4.1 : sans spécification, hors de
   portée.

## Méthode — ce que cette session a appris sur la mesure

**Trois fois, un chiffre absurde a sauvé la conclusion** : un disque mécanique à
2 211 Go/s, une allocation de cache à 4,1 % partout, un total de 4 231 Go. À
chaque fois, c'est l'invraisemblance qui a alerté — pas le test.

**Une fois, un biais aurait pu devenir un résultat publié** : la perplexité
restreinte qui *baisse* de 25,37 à 24,31. Elle aurait suffi à annoncer un gain
inexistant.

**Et une hypothèse a été confirmée puis retournée** : le miroir existe (facteur
4,6) mais ne se traduit par aucune économie ; la langue est lisible dans le
routage (79,8 %) mais ne partitionne pas les experts. Les deux fois, la mesure
fine a contredit la mesure grossière — et c'est la fine qui décide.
