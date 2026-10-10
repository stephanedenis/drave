> Campagne : **campagne-benefices** · expérience **12**
> Titre : 12. Le cas extrême : **365,7 Go sur une machine de 125 Go**
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 12. Le cas extrême : **365,7 Go sur une machine de 125 Go**

DeepSeek-V4.1-Flash Q2, exécuté par le moteur, mmappé, sans copie — deux fenêtres
minuscules, mais c'est le COÛT qui est la mesure ici :

| fenêtre | RSS | octets lus | temps |
|---|---:|---:|---:|
| 8 jetons, ctx 32 | **27,7 Go** | 32,5 Go | 216 s |
| 16 jetons, ctx 64 | **37,6 Go** | 37,7 Go | 266 s |

**Un modèle de 365,7 Go tourne sur une machine de 125 Go de RAM avec 38 Go
résidents.** Il n'est pas chargé, il est **ruisselé** : chaque passe lit ce qu'elle
touche et rien d'autre. C'est la revendication centrale du projet, mesurée sur le
plus gros modèle présent sur le disque.

**Ce que ces chiffres ne disent PAS, et il faut le dire** : la perplexité de ce
modèle sur ce corpus est énorme (13,2 M et 659 139) et n'a **aucune valeur** —
elle mélange une quantification Q2 agressive, une fenêtre de 16 jetons et une
tokenisation dont on n'a pas vérifié la réversibilité (§ 3). La ligne « modèle
plus gros que la RAM » du verdict porte donc sur **l'existence et le coût**, pas
sur la qualité.

### 12 bis. Le débit de lecture RÉEL : 8 Mo/s sur disque dur, 140-300 Mo/s sur NVMe

Le § 12 démontre qu'un modèle plus gros que la RAM **tourne**. Il ne dit pas à
quelle vitesse il *lit*, et c'est la question qui décide de l'usage. Mesuré le
9 octobre, machine au calme :

| disque | débit séquentiel (`dd` direct) | débit du moteur (mmap, page faults) | rapport |
|---|---:|---:|---:|
| **disque dur** (`sda`, modèles gguf) | **243 Mo/s** | **8,6 Mo/s** | **÷28** |
| **NVMe** (V4.1, 365 Go) | 1 600 Mo/s (mesuré au dépôt) | **140 à 300 Mo/s** | ÷5 à ÷11 |

**Le même moteur, le même code de lecture, deux comportements opposés** : sur NVMe,
les défauts de page coûtent peu et le streaming tient 140-300 Mo/s ; sur un disque
dur, une lecture aléatoire de 4 Ko coûte ~5 ms, soit ~2 000 IOPS et **8 Mo/s** —
vingt-huit fois moins que ce que le disque sait faire en séquentiel.

**Ce que cela explique, et ce que cela change** : les 90 minutes qu'une passe de
256 jetons met sur gpt-oss (§ 3), les 6,6 Mo/s du § 12, et le fait que le codestral
(13 Go) demande 25 minutes pour être lu. **Le facteur limitant n'est pas le moteur,
c'est le disque** — et sur un disque dur, la niche « modèle plus gros que la RAM »
se paie en heures, pas en minutes. Sur NVMe elle se paie en minutes. *(La
conséquence pratique est un préchargement séquentiel — `madvise(WILLNEED)` ou une
lecture ordonnée des experts — qui n'est pas implémenté ; c'est un manque, pas une
mesure.)*

---
