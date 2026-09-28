# Convertisseur et chargement : ce que la mesure dit de faire

> Directive : « un convertisseur de modèle haute fidélité afin d'avoir un
> chargement optimal : abolition des zéros, identification des clusters et MoE,
> tuning CPU/hyperthread/core pour les calques sur CPU et similaires pour les
> calques sur GPU avec optimisation des calques en fonction des routes PCIe ».
>
> Ce document confronte chacun de ces quatre points à la mesure, puis propose le
> format et l'ordre de marche.

## 1. Ce que « chargement optimal » veut dire, mesuré

Le chargement d'un modèle passait par une **copie complète** : déquantifier les
f32, puis reconstruire les poids dans notre disposition. Mesuré sur le 0,5B
Q4_0 :

| | avant (copie) | après (emprunt) |
|---|---|---|
| chargement des 24 couches | 2,70 s | **0,845 s** |
| mémoire crête (fichier 353 Mo) | ~700 Mo | **413 Mo** |
| perplexité (510 jetons) | 21,0116 | **21,0110** |

Le gain de perplexité n'est pas un bruit : l'import réencodait l'échelle de bloc
sur 16 bits relatifs (erreur 1/32767), l'emprunt lit l'échelle d'origine. **La
lecture en place est plus fidèle que la conversion.**

➡️ **Conséquence de conception : dans le chemin dense, le convertisseur est
inutile.** Les blocs Q4_0 et MXFP4 du fichier se lisent tels quels : les nibbles
bas sont les poids 0–15 et les hauts les poids 16–31, donc les activations à
apparier sont **contiguës** — l'entrelacement de notre disposition était une
commodité, pas une nécessité. Un noyau AVX2 lit les blocs du fichier sans rien
réarranger, et les sommes entières restent **bit à bit identiques** (vérifié par
test unitaire).

Pour gpt-oss-120b, c'est la différence entre 121 Go (60 de fichier + 61 de copie)
et **60 Go** — c'est-à-dire entre ne pas tenir en mémoire et tenir.

## 2. Abolition des zéros : où elle paie, où elle coûte

Taux mesurés :

| source | zéros exacts |
|---|---|
| MXFP4 (gpt-oss-120b, 4 tenseurs) | **12,0 – 17,9 %** |
| Q8_0 (Qwen2.5-0.5B) | 0,76 % |

Un schéma à masque (32 bits de présence + 4 bits par poids non nul) coûte 1
bit/poids de masque :

| zéros | dense 4 bits | masque + valeurs | gain |
|---|---|---|---|
| 0 % | 16,0 o | 20,0 o | −25 % |
| 12 % | 16,0 o | 18,1 o | −13 % |
| 18 % | 16,0 o | 17,1 o | −7 % |
| **25 %** | 16,0 o | 16,0 o | **0 %** |
| 40 % | 16,0 o | 13,6 o | +15 % |
| 70 % | 16,0 o | 8,8 o | +45 % |

➡️ **Le seuil est à 25 %, et MXFP4 est à 12–18 % : en dense, abolir les zéros
coûte plus que ça ne rapporte.** En revanche :

- **en mode événements**, c'est déjà fait et c'est gratuit : un poids nul ne
  produit aucun événement. 15 % de zéros MXFP4 = 0,30 octet/poids économisé,
  soit 15 % du flux d'événements ;
- **en MoE**, c'est le vrai levier : un routeur top-4 sur 128 experts n'allume
  que **3 %** des poids du FFN. Ce n'est plus de l'abolition de zéros, c'est du
  non-chargement.

## 3. Identification des clusters

Deux usages distincts, à ne pas confondre :

1. **Grappes effectives** (destination) : réordonner la dimension de sortie pour
   que les destinations co-activées soient adjacentes. Mesuré précédemment :
   un élagage *contigu* est 30 % plus rapide qu'un élagage *dispersé* à taux
   égal — c'est l'effet de l'accumulateur. À retester sur les grosses couches
   (`ffn` 18 944 pour un 7B : accumulateur de 76 Ko, donc hors L1).
2. **MoE** : les experts sont **déjà** des clusters — un tenseur 3D
   `dims = (2880, 2880, 128)` empile 128 experts. Il n'y a pas de cluster à
   découvrir, il y a un tenseur à découper et un routeur à exécuter.

Le convertisseur doit donc produire : une **permutation** de la dimension de
sortie (avec sa table), et des **tranches d'experts** alignées sur des pages.

## 4. Placement CPU / GPU et routes PCIe

Ce que la machine a déjà mesuré :

| chemin | débit | usage |
|---|---|---|
| DDR3 de la carte FPGA | 9,66 Go/s | lecture de listes |
| CPU, 16 threads | 14–25 Go/s | tout ce qui précède |
| PCIe x8 (gen 3) | 6,5 Go/s | transfert CPU↔GPU |
| QSFP+ | 4,8 Go/s | inter-nœuds |
| NVLink (2× Quadro RTX 5000) | 25,78 Go/s | inter-GPU |
| GPU, lecture | 380 Go/s | poids denses |
| GPU, dispersion d'événements | 18,1 G év/s | mode push |

Deux enseignements pour le placement :

- **NUMA d'abord** : 20,7 → **24,7 Go/s** en liant un socket (mesuré au banc).
  Un plan de placement qui ignore les nœuds NUMA laisse 20 % sur la table, et
  probablement bien plus sur un modèle qui ne tient pas dans un socket.
- **La route PCIe est le goulot d'un montage hybride** : à 6,5 Go/s, envoyer un
  flux d'événements au GPU coûte plus cher que de le calculer sur CPU tant que
  le CPU tient 5,3 G év/s (≈ 10,6 Go/s d'événements). **Le seuil d'intérêt du
  GPU par PCIe est donc proche de 1** : il ne se justifie que si le GPU calcule
  *plus* que ce qu'on lui envoie — c'est-à-dire s'il garde les poids et ne reçoit
  que les activations.

## 5. Format proposé : `QTNT`

Un conteneur, un index, des sections alignées.

```
en-tête      magie, version, nb_calques, nb_tenseurs, alignement (2 Mo), graine
index        par tenseur :
               nom, rôle (Wq/Wk/Wv/Wo/gate/up/down/routeur/expert),
               calque, rang d'expert, dimensions,
               encodage (blocs_source | dense4 | listes),
               offset (aligné), taille, empreinte,
               statistiques (zéros, blocs vides, variances de grappe),
               placement (cpu|gpu, nœud NUMA, nb de threads conseillé,
                          route (pcie|nvlink|qsFP), priorité de préchargement)
permutation  table de réordonnancement de la dimension de sortie (clusters)
sections     blocs de poids, alignés 2 Mo (grosses pages, lecture directe)
```

Règles de conception, chacune adossée à une mesure :

1. **Les poids restent dans leur format d'origine** quand il est déjà en 4 bits
   (`blocs_source`) : c'est ce qui rend la conversion **fidèle par
   construction** — il n'y a rien à convertir.
2. **Les listes d'événements ne sont pas matérialisées** : 1,98 o/poids × 120 G
   = 237 Go, impossible. Elles se dérivent **par expert et à la demande**.
3. **Une tranche par expert**, alignée, pour que le chargement d'un expert soit
   une lecture contiguë — et pour que le cache d'experts chauds soit possible.
4. **L'index est en tête** : le plan de placement se lit avant les poids, donc on
   peut décider où charger chaque calque sans avoir lu le modèle.
5. **L'alignement 2 Mo** est ce qui permettra les grosses pages le jour où mmap
   sera disponible (`std` seul ne l'expose pas ; en attendant, `pread` par
   section donne déjà le chargement à la demande).

## 6. Fidélité : comment on la prouve

La fidélité n'est pas une intention, c'est un test. Trois niveaux, du plus fort
au plus faible :

| niveau | critère | état |
|---|---|---|
| **bit à bit** | même forme d'exécution, même résultat | ✅ obtenu (push/pull/auto : PPL 19,2641 identique ; AVX2 vs scalaire : identique) |
| **exact** | aucun réencodage : les octets du fichier sont ceux exécutés | ✅ obtenu pour Q4_0 et MXFP4 (emprunt) |
| **équivalent** | même perplexité à l'arrondi près | ✅ (import 21,0116 contre emprunt 21,0110) |

Un convertisseur qui réencode doit prouver le niveau « exact » ou renoncer à
l'appeler haute fidélité. C'est exactement ce que la double quantification avait
coûté : **12 % de perplexité** sur Q4_0 avant qu'on s'en aperçoive.

## 7. Ordre de marche

| # | chantier | état | gain mesuré ou attendu |
|---|---|---|---|
| 1 | emprunt des blocs en place (Q4_0, MXFP4) | ✅ **fait** | chargement ×3,2, mémoire ÷2, fidélité exacte |
| 2 | lecteur **Q4_K / Q6_K** | à faire | ouvre 7B → 32B |
| 3 | **routeur MoE** + tranches par expert | à faire | gpt-oss-120b : 61 Go/jeton → 2,7 Go/jeton |
| 4 | conteneur `QTNT` + index de placement | à faire | plan CPU/GPU/NUMA lisible avant les poids |
| 5 | placement : épinglage NUMA, threads par calque | à faire | 20,7 → 24,7 Go/s mesuré au banc |
| 6 | **Q8_0 en place** (le noyau `q8_dot_at` existe déjà pour la tête) | à faire | supprime la dernière copie du chemin int8 |
| 7 | mmap (appel système direct) | à faire | grosses pages, partage entre processus |

Les points 1 et 6 sont ce qui rend un modèle de 60 Go **chargeable** ; 2 et 3
sont ce qui le rend **exécutable** ; 4 et 5 sont ce qui le rend **efficace**.
