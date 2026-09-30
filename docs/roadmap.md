# Roadmap

> Suite de [`docs/vision.md`](vision.md). Cinq phases, de ce qui se fait **tout de
> suite sur cette machine** à ce qui demande une infra (Colab, FPGA). Chaque
> phase a un critère de succès **mesurable**, et l'état de chaque chantier est
> marqué : ✅ fait · 🔬 en cours · ⏳ à faire · 🧱 bloqué par une infra absente.

## Phase 0 — La drave observable (aucune infra)

**Objectif** : faire du flux de listes un objet de première classe, qu'on
enregistre et qu'on compare. Sans cela, tout le reste se débugue à l'aveugle.

| # | chantier | état | critère de succès |
|---|---|---|---|
| 0.1 | **Format de trace du flux** : par (couche, position), la liste des neurones actifs (indice + valeur), l'échelle, le nombre | ✅ | écrit et relu sans perte ; **132 Mo pour 512 jetons** (258 ko/jeton), **+8 % de temps** — mesuré |
| 0.2 | **Diff par couche** (`tools/diff_flux.py`) : où deux exécutions divergent, à quel jeton, quels neurones | ✅ | démontré : KV f32 contre int8 → première divergence **couche 1, jeton 0**, 896 neurones, 2,9e-3 de la dynamique ; couche la plus touchée : **FFN 2** |
| 0.3 | **Le format EST le contrat d'échange** (phase 3) : versionné, en-tête + paires | ✅ | codec de référence (`tools/flux_codec.py`) : aller-retour **identique** sur 132 Mo ; **et le rejeu dans le moteur redonne les mêmes logits** (`--flux-forcer`) |
| 0.4 | **Profilage par neurone généralisé** : trace exploitable par couche et par expert, pas seulement des compteurs | ✅ | `tools/profil_flux.py` : densité par couche, part des 10 % les plus forts, neurones dominants, export CSV |

## Phase 1 — La drave mesurée (aucune infra)

**Objectif** : que chaque décision d'exécution soit *choisie par la mesure*, et
plus aucun repli silencieux.

| # | chantier | état | critère de succès |
|---|---|---|---|
| 1.1 | **Top-k dans le noyau d'attention GPU** — `--attn-topk 256` améliore la perplexité (234,88 contre 298,56 à 2 048) mais retombe sur le CPU | ⏳ | plus aucun repli CPU dans le chemin long contexte |
| 1.2 | **Quantification choisie par la mesure** : par couche, par tenseur, plutôt qu'un réglage global | 🔬 | la densité par couche varie de **20 % à 56 %** (`reports/rapport-analyse-flux.md`) : la décision push/pull est une propriété de la COUCHE, pas du modèle |
| 1.3 | **Purge des seuils codés en dur** : le placement (KV, experts, tête) décidé par une règle explicite, pas par un `if` | ⏳ | une table de décision documentée, réglée par des mesures |
| 1.4 | **Écart int8 résiduel** (+3,0 % contre +0,8 % chez llama.cpp à 8 192) | ⏳ | **expérience conçue** : garder les CLÉS en f32 et quantifier les VALEURS, puis l'inverse — c'est la seule façon d'attribuer l'écart entre les scores et la somme pondérée |

## Phase 2 — La drave répartie localement (aucune infra)

**Objectif** : la machine entière comme un seul flux — deux GPU, 40 cœurs, et le
disque quand la mémoire ne suffit plus.

| # | chantier | état | critère de succès |
|---|---|---|---|
| 2.1 | **Ordonnanceur de flux** : placer chaque opérateur là où son flux coûte le moins cher (2 GPU, CPU, VRAM, RAM, NVMe) | ⏳ | prefill à 8 k mesuré, placement décidé par la règle |
| 2.2 | **Streaming des poids depuis le NVMe** (3,5 Go/s) pour ce qui ne tient pas en RAM — c'est la même idée : ne lire que ce qui parle | ⏳ | un modèle > RAM exécuté, débit mesuré |
| 2.3 | **Cache d'experts rentable** : +6 % aujourd'hui ; grouper les trois projections par expert et supprimer les copies | ⏳ | ≥ +30 %, sinon abandonné (et écrit) |
| 2.4 | **KV sur deux cartes, politique de page** (le KV est paginé, la politique ne l'est pas) | ⏳ | 1 M de jetons tenus avec une politique d'éviction mesurée |

## Phase 3 — La drave distribuée (Colab, hors infra locale)

**Objectif** : deux machines qui se passent des listes, pas des matrices.

Le prototype se fera **avec Colab** : un *nœud moteur* (un bloc de couches) sur le
runtime Colab, un *nœud pilote* (embeddings, tête, échantillonnage) en local, et
entre les deux **le format de la phase 0** — c'est précisément pour cela qu'il est
défini avant.

| # | chantier | état | critère de succès |
|---|---|---|---|
| 3.1 | **Contrat d'échange v1** : tranche de liste = en-tête (couche, source, échelle, bits) + paires (destination, valeur) | ✅ | format écrit, relu, rejoué sans perte (phase 0.3/0.3bis) ; **transport TCP en place et FIDÈLE** (`--flux-serveur`, `--ppl-reparti`) — écart local/réparti **0,00e0** sur 40 et 199 flux, après correction de deux défauts (plage de couches ignorée par `forward`, norme finale appliquée deux fois) |
| 3.2 | **Granularité** : par couche, par bloc de canaux, par expert | 🔬 | livrés et mesurés : listes i16, **échelles par bloc de 32 canaux (valeurs i8)** et **indices par écarts** — `--flux-blocs --act-thresh 0.01` : **3 623 → 1 589 octets par flux (÷2,3) pour 1,3 % d'écart à 1 024 jetons** (2,7 % à 256, 13,7 % à 64) ; reste le cas MoE |
| 3.3 | **Seuil de rentabilité** : à partir de quel débit réseau le découpage gagne | 🔬 | mesuré jusqu'à 20 ms de latence par message (`tools/proxy_latence.py`) : **attente ≈ calcul distant + 3,2 × latence**, soit 1,01× le calcul local à 0 ms, 1,99× à 5 ms, 4,89× à 20 ms — le débit ne compte pas (0,25 Mbit/s), la latence compte quatre fois |
| 3.4 | **Démonstration Colab** : préremplissage réparti (le décodage reste séquentiel — c'est écrit dans la vision) | ⏳ | les mêmes logits qu'en local, à 1e-5 près |
| 3.5 | **Sûreté** : version du format, refus des flux incompatibles, pas de silence | ✅ | version dans chaque en-tête ; un pair en version 99 est refusé avec un message qui nomme les deux versions — vérifié avec un faux client |

## Phase 4 — La drave apprenante (recherche)

**Objectif** : le flux n'est pas qu'une exécution, c'est une donnée.

| # | chantier | état | critère de succès |
|---|---|---|---|
| 4.1 | **Capteur hebbien généralisé** : apprendre des journaux d'activation, déjà amorcé | ⏳ | une couche améliorée par apprentissage sur ses propres logs |
| 4.2 | **Routage appris** (MoE) : les experts choisis par les logs plutôt que par un routeur dense | ⏳ | qualité égale, coût de routage ÷10 |
| 4.3 | **Élagage guidé par les logs** : retirer les neurones qui ne s'allument jamais | ⏳ | modèle plus petit, perplexité égale |

## Phase 5 — La drave sur matériel (FPGA)

**Objectif** : le flux est natif sur du matériel événementiel — le premier âge du
projet avait raison, au mauvais moment.

| # | chantier | état | critère de succès |
|---|---|---|---|
| 5.1 | **PE événementiel** (Stratix V) : existe et synthétisé | ✅ | — |
| 5.2 | **Lecteur DDR3** : vérifié de bout en bout | ✅ | — |
| 5.3 | **Un opérateur complet sur FPGA** : une couche, alimentée par le même format de flux | 🧱 | dépend d'un accès matériel |
| 5.4 | **Comparaison énergie/jeton** CPU / GPU / FPGA | 🧱 | dépend d'un accès matériel |

## Ce qui commence maintenant

Phase 0, chantier 0.1 et 0.2 : **la trace du flux et le diff par couche**. Aucune
infra, et c'est le préalable à tout le reste — y compris à la phase 3, dont le
format d'échange n'est autre que le format de trace.

### Le format de trace (et donc d'échange), v1

```
en-tête de fichier :  magie "DRVF" · u16 version · u32 n_couches · u32 hidden
enregistrement      :  u16 couche · u32 position · u32 n_actifs · f32 echelle
                       puis n_actifs × ( u32 indice · i16 valeur )
fin                 :  u16 0xFFFF (sentinelle)
```

Compact (2 + 4 + 4 + 4 + 6 octets par neurone actif), sans ambiguïté, et
**exactement** ce qu'un nœud distant aurait besoin de recevoir pour continuer le
calcul : c'est la raison pour laquelle la phase 0 sert la phase 3.


## Journal des mesures de la phase 0

| date | mesure | valeur |
|---|---|---|
| 2026-09-30 | trace du flux, Qwen2.5-0.5B, 512 jetons, 24 couches, 2 points par couche | 12 288 listes · **132 Mo** · 6 octets par neurone actif · **+8 % de temps** |
| 2026-09-30 | calcul réparti sur deux processus (12 couches chacun), 40 jetons | écart local/réparti **0,00e0** (144,8289 = 144,8289) après correction de deux défauts ; avant : ×11,2 |
| 2026-09-30 | diff KV f32 contre KV int8 (perplexité 19,3885 contre 19,8059) | première divergence couche 1 jeton 0 · couche la plus touchée FFN 2 (3,9 × la dynamique) · 229 000 neurones changés sur 24 couches |
| 2026-09-30 | attribution du cache KV int8, 8 191 jetons, ctx 8 192 | f32 **14,2339** · int8 **14,6667** (+3,0 %) · **clés f32** + valeurs int8 **14,2372** (+0,023 %) · clés int8 + **valeurs f32** 14,6622 (+3,01 %) → **tout l'écart est dans les clés** |
| 2026-09-30 | protocole de flux v2, deux processus, localhost | en-tête de 39 octets (version, mode, réglages d'activation) · dense f32 **3 623 octets/flux** · listes i16 2 159 · **blocs + indices par écarts 1 568 (÷2,3)** pour 2,7 % d'écart à 256 jetons de vrai texte |
| 2026-09-30 | `TCP_NODELAY` sur le banc réparti, 200 jetons | attente du pair **97,6 → 16,1 ms** par jeton (calcul local : 15,9 ms) · banc complet 24,5 → **8,3 s**, soit le temps du calcul local (8,2 s), à logits identiques |
| 2026-09-30 | écart du transport selon la longueur, blocs à seuil 0,01 | **1,37e-1** à 64 jetons · 6,37e-2 à 128 · **2,74e-2** à 256 — il DÉCROÎT (l'erreur est stationnaire par jeton, la perplexité se moyenne) |
| 2026-09-30 | hypothèse « transmettre l'entrée normée », mode dense | écart **5,61e0** au lieu de 0,00e0 : RÉFUTÉE — la connexion résiduelle a besoin du résidu, pas de sa version normée |

Le second point est exactement ce que la vision promettait : **la divergence est
localisée**, pas seulement constatée. La première version de l'outil comparait les
entiers bruts de deux exécutions dont les échelles diffèrent et affichait des
écarts de 1e8 : c'est en le lisant qu'on l'a vu — le flux se compare
**déquantifié**, jamais brut.


### Phase 0.4 — le profilage par neurone, mesuré

`tools/profil_flux.py` lit une trace et rend, **par couche** : la densité
d'activation, la part de magnitude portée par les 10 % de neurones les plus
forts, les neurones dominants, et un export CSV.

Deux exécutions du même modèle, 512 jetons, 896 cachés par couche :

| réglage | densité par couche | taille de trace | top 10 % portent |
|---|---|---|---|
| `--abits 16` (défaut) | 99-100 % (rien n'est seuillé) | 132 Mo | 25 à 42 % |
| `--abits 8 --act-thresh 0.05` | **26 à 56 %** | **53 Mo** | 26 à 56 % |

Deux choses en sortent, et la seconde est le cœur de la vision :

1. la **part des 10 % les plus forts** (25-42 % selon les couches) reproduit, par
   couche, le chiffre global du projet (33,1 %) — le même phénomène, localisé ;
2. **la taille de la trace suit l'activité** : densité ÷2,3, trace ÷2,5. C'est
   l'argument de la vision, rendu mesurable sur un fichier : *le coût est
   proportionnel à ce qui parle*, et ce sera vrai du format d'échange de la
   phase 3 comme il l'est ici.

Réserve écrite : la ligne « seuil 0,05 » a une perplexité de 2 445 — c'est un
relevé de COÛT, pas de qualité ; le seuil est volontairement brutal.


### Phase 1.4 — l'attribution de l'écart int8 : FAITE

L'écart avec llama.cpp à 8 192 (+3,0 % contre +0,8 %) est attribué. Les deux
drapeaux annoncés (`DRAVE_KV_V_F32`, `DRAVE_KV_K_F32`) ont été terminés, et
l'expérience tournée sur 8 191 jetons :

| configuration | perplexité | écart au f32 | part de l'écart |
|---|---|---|---|
| cache f32 (référence) | **14,2339** | — | — |
| cache int8 complet | 14,6667 | +3,04 % | 100 % |
| **clés f32** · valeurs int8 | **14,2372** | **+0,023 %** | **99,2 % expliqué** |
| clés int8 · **valeurs f32** | 14,6622 | +3,01 % | 1,0 % seulement |

**Tout l'écart est dans les clés.** C'est cohérent avec leur rôle : une clé entre
dans le score, donc dans le softmax — une erreur de clé déplace le poids relatif
d'une position entière ; une valeur ne fait que pondérer la sortie, son erreur se
moyenne.

Conséquence utilisable tout de suite : `DRAVE_KV_BITS=8 DRAVE_KV_K_F32=1` donne un
cache à **75 % de la taille f32** pour +0,02 % de perplexité, là où l'int8 complet
(50 %) coûte +3,0 %. Notre quantificateur de VALEURS est donc bon ; c'est celui
des CLÉS qui est le maillon faible.

Deux suites, écrites avec leur critère de succès : **clés f32 · valeurs int4**
(62,5 % de la taille f32 — si les valeurs tolèrent 4 bits, ce réglage bat l'int8
complet en taille ET en qualité), et **un meilleur quantificateur de clés**
(échelle par tête, ou rotation orthogonale avant quantification) pour ramener
l'écart des clés sous les +0,8 % de llama.cpp. Détail :
`reports/rapport-attribution-kv.md`.

### Phase 0.3bis — le REJEU, et ce qu'il démontre pour la phase 3

`--flux-forcer <trace>` relit une trace et **remplace les activations calculées
par celles qui sont enregistrées** (déquantifiées). Si le rejeu redonne les mêmes
logits, alors **une liste suffit à continuer le calcul** — c'est exactement le
contrat qu'un nœud distant devra honorer, et il est donc déjà démontré
localement.

Mesuré, Qwen2.5-0.5B, 512 jetons, deux fenêtres de contexte, trace de 132 Mo :

```
sans rejeu  : perplexité 19.3885 sur 510 tokens
avec rejeu  : perplexité 19.3885 sur 510 tokens
```

Identique. Et le diagnostic (`DRAVE_FLUX_VERIF=1`) chiffre la fidélité de
l'encodage : écart relatif **1,5e-5** entre l'activation calculée et celle que la
trace impose — soit la quantification 16 bits, rien de plus.

**Le défaut trouvé en chemin, et corrigé** : la clé d'une liste était
`(couche, position DANS la fenêtre)`. Une exécution à plusieurs fenêtres
réécrivait donc les mêmes clés, et le rejeu rejouait la mauvaise : perplexité
**356 694** au lieu de 17,43. La clé est maintenant `(couche, compteur de jeton
global)` — même format sur le disque, sémantique non ambiguë. C'est le genre de
défaut qu'un rejeu attrape et qu'un diff ne voit pas.


### Phase 3 — ce qui tourne déjà, et ce qui ne tourne pas encore

Le transport existe : `--flux-serveur <port>` fait tourner un **nœud moteur** qui
charge le modèle, écoute, applique SA plage de couches au flux reçu et renvoie le
flux résultant ; `--ppl-reparti <hôte:port> --couches-locales N` fait tourner le
**pilote** qui garde les N premières couches, envoie le flux, reçoit l'état final
et note la perplexité.

Mesuré, deux processus, localhost, 12 couches de chaque côté : le calcul coupé
redonne **exactement** le calcul local — écart **0,00e0**, perplexité 144,8289 des
deux côtés, sur 40 jetons puis sur 200 (199 flux servis).

Il a fallu **deux corrections** pour y arriver, et la première ne suffisait pas :

1. **`forward` ignorait la plage de couches.** La boucle partait de `0` au lieu de
   `couche_debut..couche_fin` : le pilote calculait les 24 couches, envoyait
   l'état FINAL, et le nœud moteur recalculait les 24 couches par-dessus. C'était
   la cause principale. `forward_lot` et `forward_mla` respectaient déjà la plage ;
   `forward` était l'exception — exactement le genre d'asymétrie que le mode
   d'échec « analysé mais jamais appliqué » du dépôt produit.
2. **La norme finale était appliquée deux fois.** Le nœud moteur recevait
   `fin = n_layer`, donc son `forward` normait (`couche_fin >= n_layer`), et le
   pilote normait ensuite avec `norme_finale()`. La règle est maintenant portée
   par un drapeau explicite, `flux_brut` : un nœud intermédiaire rend TOUJOURS un
   flux résiduel brut, et la norme appartient au nœud qui possède la tête de
   sortie — une seule fois.

Le protocole, lui, n'a pas changé d'un octet : c'est le moteur qui était faux.

**Puis le transport lui-même** : `--flux-liste` fait voyager la LISTE (indice
u16, valeur i16, une échelle), c'est-à-dire le format du disque, au lieu du
vecteur dense f32. Mesuré à 40 jetons, par flux (aller) :

| mode | octets | écart de perplexité |
|---|---|---|
| dense f32 | 3 623 | **0,00e0** |
| listes, seuil 0,00 | 3 622 | 2,6e-2 |
| listes, seuil 0,02 | 2 203 | 4,9e-2 |
| listes, seuil 0,05 | 897 | 8,1e-1 |

Avec `--flux-blocs` (échelle par bloc de 32 canaux, valeurs i8), le régime creux
s'améliore : à sparsité égale (seuil 0,02, 59 % d'activité) les blocs font
**1 745 octets contre 2 159** pour la liste i16, et 14 % d'écart contre 16 % —
l'échelle par bloc borne l'erreur *relative*, l'échelle unique borne l'erreur
*absolue*. Les indices, eux, se rangent par **écarts** (un octet par neurone actif, 255 en
échappement) : 2 268 → **1 568 octets** à écart et perplexité IDENTIQUES — du
rangement, pas de la perte. Sur 256 jetons de vrai texte, le réglage recommandé
est donc le seuil **0,01** : **÷2,3 sur le fil pour 2,7 %** d'écart — et l'écart DÉCROÎT avec la
longueur (13,7 % à 64 jetons, 6,4 % à 128, 2,7 % à 256, **1,3 % à 1 024**) : la perturbation est
stationnaire par jeton, donc elle se dilue dans une perplexité moyennée. Ce qui
change d'un banc à l'autre, c'est le corpus, pas la longueur. Le rapport porte la
courbe et les deux formulations que la mesure a corrigées (« ÷2 pour 0,2 % »,
puis « ça empire avec la longueur »).

Et le coût réel du découpage, mesuré à 200 jetons sur localhost : le calcul local
de 12 couches prend 15,9 ms par jeton, l'attente du pair 16,1 ms — soit **1,01×**.
Le banc réparti entier (8,3 s) prend le temps du calcul local (8,2 s), à logits
identiques. Avant `TCP_NODELAY`, cette attente était de 97,6 ms (6,26×) : le
protocole payait Nagle et l'ACK différé, pas le réseau.

La leçon est écrite noir sur blanc : **le gain ne vient que de la sparsité**
(la valeur fait 16 bits sur le fil, donc une liste pleine coûte le dense), et
**jeter des canaux coûte cher** — l'écart est déjà de 2,6 % à 16 bits pleins,
alors que le rejeu d'une trace quantifiée 16 bits redonnait la perplexité exacte.
Ce n'est pas la précision qui diffère, c'est ce qu'on quantifie : le résidu brut
a une dynamique bien plus large que l'entrée normée qu'encode la trace.

La suite logique — transmettre l'entrée NORMÉE au lieu du résidu — a été essayée
et **réfutée** : en mode dense, où le transport est exact, l'écart passait de
0,00e0 à **5,61e0**. La norme d'entrée n'est pas seulement l'entrée de
l'attention : la connexion résiduelle a besoin du résidu lui-même. Le drapeau a
été retiré. Ce qui marche, c'est l'**échelle par bloc** (faite, `--flux-blocs`).
Détail et chiffres : `reports/rapport-transport-liste.md`.
Chiffres des trois états, mesurés sur le même banc de 40 jetons :

| état | perplexité locale | perplexité répartie | écart |
|---|---|---|---|
| avant correction | 144,8289 | 1 621,7239 | ×11,2 |
| après la norme seule | 144,8289 | 693,4492 | ×4,8 |
| après la plage de couches | 144,8289 | **144,8289** | **0,00e0** |

Ce qui est donc ACQUIS : le cadriciel d'échange, la séparation en deux nœuds, la
plage de couches par nœud, la norme finale appliquée par le seul nœud qui a la
tête — et la preuve que le découpage ne change pas un chiffre. Ce qui reste :
le transport lui-même (aujourd'hui du f32 dense, 3 604 octets par flux), la
granularité (3.2), le seuil de rentabilité (3.3) et la version du format (3.5).
