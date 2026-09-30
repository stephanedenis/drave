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
| 3.1 | **Contrat d'échange v1** : tranche de liste = en-tête (couche, source, échelle, bits) + paires (destination, valeur) | 🔬 | format écrit, relu, rejoué sans perte (phase 0.3/0.3bis) ; **transport TCP en place** (`--flux-serveur`, `--ppl-reparti`) — 88 flux servis entre deux processus, mais la perplexité répartie n'est PAS encore fidèle (798 contre 18,2) : le défaut est identifié comme prochain chantier, pas maquillé |
| 3.2 | **Granularité** : par couche, par bloc de canaux, par expert | ⏳ | courbe : octets par jeton × latence pour chaque granularité |
| 3.3 | **Seuil de rentabilité** : à partir de quel débit réseau le découpage gagne | ⏳ | formule validée par une mesure locale (socket `localhost`) avant Colab |
| 3.4 | **Démonstration Colab** : préremplissage réparti (le décodage reste séquentiel — c'est écrit dans la vision) | ⏳ | les mêmes logits qu'en local, à 1e-5 près |
| 3.5 | **Sûreté** : version du format, refus des flux incompatibles, pas de silence | ⏳ | un flux d'une autre version est refusé avec un message clair |

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
| 2026-09-30 | diff KV f32 contre KV int8 (perplexité 19,3885 contre 19,8059) | première divergence couche 1 jeton 0 · couche la plus touchée FFN 2 (3,9 × la dynamique) · 229 000 neurones changés sur 24 couches |

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


### Phase 1.4 — l'expérience à faire, écrite pour ne pas la reperdre

L'écart avec llama.cpp à 8 192 (+3,0 % contre +0,8 %) n'est pas attribué. Deux
sources possibles, et une seule expérience les sépare :

| variante | ce qu'elle isole | réglage proposé |
|---|---|---|
| clés quantifiées, **valeurs en f32** | l'erreur qui passe par les SCORES | `DRAVE_KV_V_F32=1` |
| **clés en f32**, valeurs quantifiées | l'erreur qui passe par la SOMME PONDÉRÉE | `DRAVE_KV_K_F32=1` |

Le code à toucher est localisé : `KvCache::ecrire` (écrire dans `kf`/`vf` au lieu
de `kq`/`vq` selon le drapeau), `cle`/`valeur` (lire le bon tableau), `assurer`
(agrandir les tableaux f32 quand ils servent) et `new` (les allouer). Les appels
GPU doivent être désactivés dans ces variantes — le miroir suppose une
disposition homogène.

Ces deux drapeaux ont été commencés puis RETIRÉS : le temps restant ne permettait
pas de les finir et de les mesurer, et un demi-drapeau vaut moins qu'une
expérience écrite. C'est ici, avec les points de code exacts.


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

Mesuré, deux processus, localhost, 88 jetons de 896 cachés : **88 flux servis**,
aucune erreur de transport — et la perplexité répartie **ne correspond pas**
encore (798,3 contre 18,2178 en local).

Ce qui est donc ACQUIS : le cadriciel d'échange, la séparation en deux nœuds, la
plage de couches par nœud, la norme finale appliquée par le dernier nœud
seulement. Ce qui reste à trouver : pourquoi le calcul coupé diverge — les
candidats sont la position transmise (elle l'est), la norme d'entrée du nœud
distant (elle s'applique à la couche 12, correctement) et l'état du cache KV de
chaque nœud. C'est écrit ici comme un défaut OUVERT, avec ses chiffres.
