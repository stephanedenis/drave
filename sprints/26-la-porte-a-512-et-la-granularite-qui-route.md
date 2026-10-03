# Sprint 26 — La porte à ctx 512, le coût qui ne croît pas, et la granularité qui route

- **Début** : 09:40 · **Fin** : 11:20
- **Objectif** : après le bloc 25 (le « coût croissant » était le disque dur), deux
  choses deviennent possibles : porter la **porte de correction** à un contexte
  deux fois plus long, et répondre par la mesure à une question de conception
  posée par le propriétaire du projet — **séparer couches et grappes en listes plus
  fines pour réduire les flux entre unités de traitement**.
- **Engagement de fin** : dépôt vert, machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. La porte de correction à ctx 512 : TENUE (511 positions)

Modèle sur NVMe, chemin **par défaut** (scalaire, bit à bit celui des références) ;
référence llama.cpp sur la même fenêtre, mêmes identifiants :

| mesure | llama.cpp | Drave |
|---|---|---|
| perplexité (511 prédictions) | **6,0030** | **6,2612** (+4,3 %) |
| corrélation par position | min **0,941811** (pos 305) · moyenne **0,989879** | |
| top-1 identique | **475/511 (93,0 %)** | |
| sous 0,95 | 2/511 (0,4 %) · plancher 0,90 respecté | |

**Le résultat le plus fort est le diagnostic par tranches** : 0-63 → 0,98534,
64-255 → 0,98934, 256-510 → **0,99142**. L'accord **s'améliore** avec la position :
aucune dérive de rotation, de blocs compressés ni de fenêtre glissante sur 511
positions. Et l'écart de perplexité (+4,3 %) est **plus faible** qu'à 255 positions
(+9,0 %) : allonger la fenêtre n'aggrave rien.

### 2. Le coût par jeton ne croît pas avec le contexte

| | ctx 64 (63 jetons) | **ctx 512 (511 jetons)** |
|---|---|---|
| passe | 2,50 s/jeton | **2,58 s/jeton** |
| attention | ~1 013 ms | 1 137,72 ms |
| `proj+mlp` | 1 472 ms | 1 414,10 ms |

**×1,03 de ctx 64 à ctx 512.** Ce que les blocs 23-24 prenaient pour une croissance
(jusqu'à « 60 s/jeton à ctx 1 024 ») était le disque dur. La mesure à ctx 1 024
redevient donc abordable — c'est le prochain palier, et il exercera 256 blocs
compressés (toujours sous le seuil de 512 de l'indexeur, donc toujours exact).

### 3. CORRECTION d'un chiffre publié : le gain du SIMD

L'A/B de la veille (×2,06 sur la passe, ×3,05 sur `proj+mlp`) était **faux** : le
run scalaire de référence tournait pendant qu'un processus `drave` survivant d'un
`timeout` occupait les cœurs (271,0 s puis 319,5 s pour le même travail, contre
157,8 s machine rendue). A/B **entrelacé** refait (3 scalaires, 2 SIMD) :

| | scalaire | SIMD |
|---|---|---|
| passe | **157,8 s** | **133,9 s** (**×1,18**) |
| `proj+mlp` | 1 472 ms | 1 078 ms (**×1,37**) |

Le rapport d'écart (+0,15 % de perplexité, corrélation 0,9981 contre notre propre
scalaire) est inchangé. Plan, `REPRISE.md` et `sprints/24` sont corrigés.

### 4. Granularité des listes : elle route, elle ne compresse pas

Mesuré sur les activations réelles de V4-Flash (43 couches × 4 positions, tenseur
`l_last` = le flux de coupure, 4 copies d'hyper-connexion = 16 384 valeurs =
**65 536 octets** en f32), avec l'encodeur DRVF de référence :

| G (listes) | err ≈ 0,05 | err ≈ 0,10 | err ≈ 0,20 |
|---|---|---|---|
| **1** | **55,3 %** | **43,3 %** | **26,7 %** |
| 4 | 66,0 % | 61,8 % | 54,5 % |
| 16 | 65,7 % | 60,0 % | 52,3 % |
| 64 | 64,6 % | 58,3 % | 50,6 % |
| 512 | 73,9 % | 68,1 % | 57,5 % |

**À fidélité égale, découper coûte plus cher** (en-tête de 14 o par liste, plus la
perte de l'échelle globale). Ce que la finesse apporte est ailleurs : une unité ne
reçoit que ses listes, une tranche d'énergie négligeable coûte **0 octet** (à
G = 64, ε = 1e-2 : 28,5 tranches sur 64 jetées, flux à 28,2 % du dense), et à seuil
égal une tranche fine a moins d'erreur (0,244 à G = 1 contre 0,030 à G = 512).

Et le fait qui **commande le placement** : **2,669 Go de poids par jeton** contre
**65 536 octets** d'activation à une coupure — quatre ordres de grandeur. Le
placement doit suivre les poids ; les flux d'activation, même denses, sont
abordables (2,5 µs sur NVLink contre 107 ms pour les poids du même jeton).

### 5. Le tandem GPU : chiffré

Deux Quadro RTX 5000 (32 Go de VRAM, NVLink 25,78 Go/s) sont **au repos** pendant
nos passes V4-Flash/V4.1 : le chemin GPU du moteur exige que les poids résident en
VRAM, or un jeton en demande 2,7 à 3,9 Go et le modèle en pèse 87 à 366. Planchers :
VRAM 7-10 ms/jeton · RAM CPU 133-195 ms · PCIe 411-599 ms · disque dur 13-20 s. Un
chemin *streaming* vaut ×5 à ×7 ; trois bancs sont nommés avant d'écrire du CUDA
(`reports/rapport-gpu-tandem-nvlink.md`).

## Rétrospective — garder / changer / doute

**Garder.** Refaire une mesure **entrelacée** quand la machine est partagée. Un seul
A/B non entrelacé a produit un chiffre faux (×2,06) publié dans le plan, `REPRISE`
et un sprint — et il a fallu une mesure indépendante (le scalaire à ctx 512 à
1 414 ms, incompatible avec les 3 271 ms annoncés) pour s'en apercevoir. La règle
« entrelacer les A/B » existait déjà dans `REPRISE.md` : elle n'a pas été suivie.

**Garder (2).** Le réflexe de dater chaque chiffre par son support de stockage. Le
protocole de ctx 512 n'était pas « impossible » (comme écrit au bloc 23), il était
impossible **sur disque dur**.

**Changer.** Une conclusion de conception ne se prend pas sur l'intuition, même
juste. L'idée « des listes plus fines réduisent les flux » est **vraie pour le
routage** et **fausse pour le volume agrégé** — et c'est la mesure, pas l'accord
avec l'interlocuteur, qui a tranché. Le rapport le dit avec les deux tableaux.

**Changer (2).** Le plan portait « la porte à ctx 256 » comme le maximum
raisonnable : c'était une limite de matériel prise pour une limite de méthode. Les
portes doivent être re-évaluées quand l'environnement change, sinon elles
deviennent des dogmes.

**Doute.** Le flux mesuré est celui de `l_last` (4 copies hc). Les autres coupures
possibles (`ffn_hn`, `moe_down`, `attn_out`, 4 096 valeurs) n'ont pas été
analysées séparément : si une coupure plus fine (par expert) était choisie, les
chiffres changeraient. C'est nommé dans le rapport (§5).

**Doute (2).** ctx 1 024 « redevient abordable » — c'est une extrapolation (×1,03 de
64 à 512), pas une mesure : la passe à ctx 1 024 pourrait réserver une surprise
(mémoire, blocs, cache). Elle est annoncée comme le prochain palier, pas comme un
acquis.
