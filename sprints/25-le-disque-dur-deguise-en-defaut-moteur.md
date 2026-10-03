# Sprint 25 — Le disque dur déguisé en défaut moteur (et le tandem GPU chiffré)

- **Début** : 08:20 · **Fin** : 09:40
- **Objectif** : le bloc 24 a laissé une courbe gênante — « le coût par jeton croît
  avec la position » (2,5 s à 31 jetons, 6,45 s à 255, ≈60 s à 1 024) — et une
  ablation qui semblait accuser le chemin des blocs compressés (×1,8). Ce bloc doit
  trouver la cause. Il a trouvé autre chose : **l'instrument était faux**.
- **Engagement de fin** : dépôt vert, machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. La variable cachée : le modèle était sur un DISQUE DUR

`lsblk` sur le volume « 11 To » : `WDC WD120EFGX`, **ROTA = 1** — un disque
rotationnel. V4-Flash y vivait (86,9 Go), et le cache de pages est partagé : chaque
grosse passe (V4.1, 341 Go) évince les pages du modèle. Un run a alors tourné
**14 minutes sans finir une seule fenêtre de 63 jetons** — le symptôme exact d'un
modèle lu au disque.

L'outil écrit pour le vérifier (`tools/analyse_octets_par_jeton.py`, en-têtes GGUF
seulement) donne l'arithmétique : **2,669 Go de poids par jeton** pour V4-Flash
(43 couches × 6/256 experts + partagé ; formats mêlés IQ3_XXS/IQ2_XXS/IQ1_M/MXFP4),
**3,893 Go** pour V4.1. À 200 Mo/s, cela fait **13,3 s/jeton** — le run pathologique
s'explique au chiffre près.

### 2. Le protocole rejoué à l'identique, sur NVMe

Même binaire, mêmes identifiants, mêmes drapeaux (ctx 64, 252 jetons, quatre
fenêtres, `DRAVE_SIMD_DOT=1`) ; seule la **copie du modèle** change (86,9 Go copiés
sur le NVMe, tailles vérifiées octet à octet) :

| | disque dur | **NVMe** |
|---|---|---|
| total | 1 027,7 s | **567,1 s (×1,81)** |
| débit par fenêtre | 0,5 → 0,3 → 0,2 → 0,2 (**décroît**) | **0,4 · 0,4 · 0,4 · 0,4 (plat)** |
| `proj+mlp` | 3 046,73 ms/token | **1 315,43 ms/token** |
| `attention` | 1 000,01 ms/token | 902,66 ms/token |

**La croissance n'existe pas quand le stockage suit.** Et l'ablation qui accusait
les blocs compressés (`DRAVE_SANS_BLOCS=1`, 561,4 s) donne sur NVMe **567,1 s** :
la même chose. Elle « gagnait » parce qu'elle tournait avec un cache plus chaud.

### 3. Ce que ça corrige, et la leçon

- Le plan (P6) attribuait la croissance à un défaut du moteur, puis à l'empreinte
  des experts, puis — après mesure — au chemin des blocs. **Les trois étaient
  faux** : c'était le placement du fichier.
- La mesure « `read_bytes` = 0 » qui innocentait le disque avait été faite sur un
  run de 93 jetons **avec le cache chaud** : elle ne prouvait rien sur un run long.
  Un échantillon de `read_bytes` **pendant** toute la passe, pas à un instant
  choisi, est désormais la règle pour toute mesure de débit.
- Ce qui reste vrai : le coût croît avec la **longueur du contexte** (attention et
  blocs), et c'est maintenant mesurable proprement.

### 4. Le tandem GPU : chiffré, pas supposé

`reports/rapport-gpu-tandem-nvlink.md` : deux Quadro RTX 5000 (32 Go de VRAM au
total, NVLink 25,78 Go/s) sont **au repos** pendant les passes V4-Flash/V4.1, parce
que le chemin GPU du moteur exige que les poids résident en VRAM — or un jeton a
besoin de 2,7 à 3,9 Go de poids et le modèle en pèse 87 à 366. Planchers mesurés :
VRAM 7-10 ms/jeton · RAM CPU 133-195 ms · bus PCIe x8 411-599 ms · disque dur
13-20 s. Le CPU est à 2,06 s/jeton (V4-Flash, SIMD) : **5 à 7× au-dessus du
plancher PCIe**, donc borné par le calcul. Un chemin *streaming* (tampons pinned,
noyaux PTX de déquantification, regroupement par expert, double-tampon) vaut ×5 à
×7 — il n'existe pas, et trois bancs sont nommés avant d'écrire du CUDA.

## Rétrospective — garder / changer / doute

**Garder.** Le réflexe « rejouer le protocole à l'identique en ne changeant QU'UNE
chose ». C'est ce qui a transformé une conclusion fausse (un défaut moteur) en un
fait exploitable (×1,81 par le placement du fichier). Aucune lecture de code
n'aurait donné ça.

**Garder (2).** Le chiffre avant l'explication : `analyse_octets_par_jeton.py` a
donné 2,669 Go/jeton et 13,3 s/jeton au disque dur — le run « incompréhensible » de
14 minutes est tombé à l'arithmétique près.

**Changer.** J'ai écrit **trois causes successives** pour le même phénomène en deux
blocs (empreinte des experts, puis blocs compressés) sans avoir éliminé la variable
la plus banale : *où est le fichier*. La règle « mesurer avant de conclure » doit
s'appliquer d'abord aux variables d'environnement du protocole — stockage, cache,
charge machine — avant les hypothèses sur le code.

**Changer (2).** La mesure qui innocentait le disque (`read_bytes` = 0) était un
**instantané** pris sur un run court et chaud. Un instantané n'est pas une mesure
d'intervalle : les compteurs `/proc/<pid>/io` doivent être échantillonnés **pendant
toute la passe** et rapportés au temps, pas lus une fois.

**Doute.** La copie du modèle sur NVMe a coûté 6 minutes et 87 Go ; elle restera
tant qu'on mesure, mais elle **change la machine** (233 Go libres au lieu de 320).
Ce n'est pas neutre pour la suite : toute mesure de débit publiée avant ce bloc doit
dire sur quel support elle a été faite. Le plan le dit maintenant, les anciens
rapports ne le disent pas — c'est une dette de traçabilité, nommée ici.

**Doute (2).** La croissance **avec la longueur du contexte** (6,45 s/jeton à ctx
256 contre 2,5 s à ctx 64) n'est pas encore re-mesurée sur NVMe. Elle pourrait,
elle aussi, se réduire à quelque chose de banal (le nombre de blocs visibles, ou
simplement le cache). Tant qu'elle n'est pas mesurée proprement, elle ne doit servir
à aucun argument — pas même à celui-ci.
