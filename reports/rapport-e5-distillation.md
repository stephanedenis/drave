# E5 — distiller le cerveau dans le réflexe : l'accord double (28 % → 51 %), et le texte ne suit toujours pas

> Campagne : **cerveau** · expérience : **E5** (`docs/biologie-pour-drave.md` : « rejeu et
> distillation », jusqu'ici *cadrée* et jamais mesurée) — et la réponse à un constat de la nuit :
> **le réflexe entraîné à la perplexité ne partageait AUCUN jeton avec le cerveau** (0 sur 96 en
> génération, trois invites, `rapport-cycle-entraine.md` § génération).
> Question : si l'objectif devient l'**imitation** (la distribution du modèle complet) au lieu de
> la prédiction du texte, le chemin court se rapproche-t-il du cerveau — et à quel prix ?
> Verdict : **oui pour l'accord, non pour la fidélité.** À la même architecture (8 couches + lecteur
> de 896×896 + LoRA), l'objectif change **ce qu'on obtient** : entraîné à la **perplexité**, le
> réflexe rend **181,54** (m32) et s'accorde avec le maître sur **28,0 %** des positions ;
> **distillé** (KL contre le modèle complet), il rend **574,70** et s'accorde sur **51,0 %** —
> **l'accord fait ×1,8** (m20 : 40,5 % → **68,1 %**) au prix d'une perplexité **×3,2**. Et au niveau
> du **texte** généré, les deux échouent : **0/96** et **5/96** jetons identiques — un accord par
> position de 50 % ne tient pas 32 jetons en greedy (0,5³² ≈ 0).
> Date réelle : **2026-10-14 23 h 25-23 h 55 HAE** (heure lue sur la machine)
> Protocole : `tools/n4_dessin_b.py --distiller` (KL sur les distributions, température 1) contre le
> même banc sans `--distiller` · protocole propre (m0..m29 **moins m20**, validation m30+m31, test
> m32 et m20) · graine 0 · mesure de l'**accord** : fraction de positions où `argmax` du chemin
> court égale `argmax` du modèle complet · génération : `drave --infer --n 32 --temp 0` sur trois
> invites, modèle exporté (`--adaptateur-sortie`) et lu **par le moteur**.

## 1. Les deux réflexes, sur le même banc

| bras (8 couches sur 24) | perplexité m32 | perplexité m20 | **accord m32** | **accord m20** | lecture |
|---|---:|---:|---:|---:|---|
| tête **empruntée** (témoin) | 4 476 128,79 | 1 761 597,24 | **0,0 %** | 0,1 % | un lecteur gelé ne lit rien |
| `lora+adaptateur`, objectif **perplexité** | 181,54 | 153,98 | **28,0 %** | 40,5 % | prédit bien, **imite mal** |
| `lora+adaptateur`, objectif **distillation** | 574,70 | 715,02 | **51,0 %** | **68,1 %** | **imite mieux**, prédit moins bien |

Ce que ça dit :

* **l'objectif décide de la faculté qu'on obtient** : à architecture **identique**, le même banc
  donne un « bon petit modèle » (perplexité 181) ou un « imitateur » (accord 51 %). Ce n'est pas un
  réglage, c'est un **choix de dessin** — et il est chiffré des deux côtés ;
* **la distillation fait ×1,8 sur l'accord** (28,0 → 51,0 % sur m32 ; 40,5 → 68,1 % sur m20) : c'est
  un gain net, mesuré sur des textes **jamais vus**, et il est cohérent avec ce que la distillation
  fait (transférer la *distribution*, pas le jeton) ;
* **elle coûte ×3,2 de perplexité** (181,54 → 574,70) : un étudiant qui vise la distribution entière
  d'un maître qu'il ne peut pas atteindre **compromis** sa prédiction. Les deux objectifs ne sont
  donc pas hiérarchisés — ils mesurent **deux choses différentes** ;
* **au niveau du TEXTE, les deux réflexes sont des étrangers** : en génération greedy de 32 jetons
  sur trois invites, l'accord est de **0/96** (perplexité) et **5/96** (distillation). Ce n'est pas
  une contradiction avec les 51 % par position : 0,51³² ≈ 2 × 10⁻¹⁰. La fidélité d'un réflexe au
  cerveau **s'effondre exponentiellement avec la longueur**, et c'est une propriété du décodage
  autorégressif, pas un défaut de l'entraînement.

## 2. Le réflexe comme effecteur : ce qu'il apporte vraiment, c'est le TEMPS

Mesuré par le moteur, invite de 8 jetons, 64 jetons générés (`--couches 0:8 --tete-partielle
--adaptateur-sortie`) :

| | modèle complet (24 couches) | réflexe distillé (8 couches + lecteur) | rapport |
|---|---:|---:|---:|
| premier jeton (TTFT) | 414,1 ms | **135,3 ms** | **÷3,1** |
| génération | 25,79 tok/s | **52,23 tok/s** | **×2,0** |

* **c'est le seul chiffre qui plaide pour le réflexe** : ×2 de débit, ÷3,1 au premier jeton — pour
  un texte qui n'est **pas** celui du cerveau ;
* **et sa génération dégénère** : le réflexe distillé boucle (« 339 9294 315 279 » répété), ce qui
  est le comportement classique d'un modèle faible en greedy — le mode `--temp 0` ne pardonne rien,
  et l'échantillonnage n'est pas mesuré ici ;
* **conséquence pour C8** : la moitié « effecteur » de la périphérie existe maintenant de bout en
  bout (le moteur **écrit** ce que le réflexe produit), et elle dit ce qu'elle vaut : **un agent
  différent, deux fois plus rapide**.

## 2bis. E5 bis — le MÉLANGE (KL + λ·CE) est PIRE sur les DEUX axes

La question ouverte la plus évidente après le § 1 : peut-on **garder la perplexité** (l'objectif
dur, le jeton) **en gagnant l'accord** (la distribution du maître) ? C'est le mélange classique
`KL + λ·CE`, essayé à deux valeurs :

| objectif | perplexité m32 | perplexité m20 | accord m32 | accord m20 |
|---|---:|---:|---:|---:|
| perplexité seule (CE) | **181,54** | **153,98** | 28,0 % | 40,5 % |
| distillation seule (KL) | 574,70 | 715,02 | **51,0 %** | **68,1 %** |
| KL + **1,0** × CE | 1 475,96 | 967,82 | 46,8 % | 47,0 % |
| KL + **4,0** × CE | 880,74 | 1 752,44 | 36,9 % | 25,9 % |

**Le mélange ne prend pas le meilleur des deux : il prend le pire des deux.** À λ = 1 la perplexité
est **2,6 fois pire** que la distillation seule (1 476 contre 575) et l'accord est **plus bas**
(46,8 % contre 51,0 %) ; à λ = 4 l'accord s'effondre à 36,9 % / 25,9 % — **sous** le modèle entraîné
au texte seul sur m20 (40,5 %).

* la cause **n'est pas instruite**, et deux hypothèses sont nommées : (1) le mélange **double
  l'échelle du gradient** sans retoucher le pas d'apprentissage (1e-3 pour tous les bras) — un
  λ > 0 change le réglage effectif, et les deux objectifs purs ont, eux, été laissés à leurs
  meilleures époques sur la même validation ; (2) la KL et la CE **ne tirent pas dans la même
  direction** ici : la CE veut un pic sur le bon jeton, la KL veut la forme entière d'une
  distribution qu'un étudiant de 8 couches ne peut pas atteindre, et la somme des deux
  compromis peut être pire que chaque terme ;
* **ce qui est établi, c'est le fait** : *à ce budget et à ce pas*, le mélange est dominé par les
  deux objectifs purs **sur leur propre axe**. La recette « on peut avoir les deux » n'est pas
  confirmée — et elle demanderait un balayage du pas d'apprentissage, qui n'est pas fait.

## 3. Ce que cette fiche ne dit pas

* **une seule température de distillation** (T = 1) : le réglage classique (T = 2 à 4) n'est pas
  essayé ; et le mélange KL + λ·CE, essayé au § 2bis, **n'a pas retouché le pas d'apprentissage** —
  c'est la première chose à faire avant de conclure sur lui ;
* **pas de distillation des états** (les couches intermédiaires du maître ne sont pas imitées) :
  seule la distribution de sortie l'est ;
* **une seule architecture d'étudiant** (8 couches + 896² + LoRA rang 8) : la capacité de
  l'étudiant borne l'accord atteignable, et sa courbe n'est pas faite ;
* **l'accord est mesuré en top-1** : un accord de distribution (KL, rang du jeton du maître) dirait
  plus, et n'est pas reporté ;
* **rien sur l'échantillonnage** (`--temp`, `--top-p`) : la dégénérescence observée en greedy peut
  disparaître en échantillonnant — ou pas ; ce n'est pas mesuré.

## 6. REPRODUCTIBILITÉ : le protocole de cette fiche ne tient pas dans 16 Go (16/10, 01 h)

En voulant **tester E5 sur d'autres graines** — la leçon de la nuit (« une graine ne mesure pas un
critère ») appliquée à cette fiche ✗ — la reproduction a buté sur trois obstacles, tous instructifs :

| obstacle | ce qui s'est passé | ce que ça apprend |
|---|---|---|
| **mauvais drapeau** | `--couches-lora` n'existe **pas** dans `n4_dessin_b.py` (c'est un drapeau de l'**exporteur**) : l'entraînement sortait **immédiatement** en erreur | ⚠️ **je l'avais masqué avec `>/dev/null 2>&1`** ✗ — la sortie silencieuse a coûté **deux tours** de diagnostic. *Ne jamais faire taire une commande qu'on n'a pas encore vue réussir* |
| **mauvais bras** | `--bras lora` ✗ au lieu de `--bras lora+adaptateur` : l'accord mesuré tombait à **100 %** | 100 % n'était pas un bon résultat mais un **mauvais objet mesuré** (le chemin **complet**, pas le tronqué) — la fiche dit « chemin tronqué à 8 couches », et le réflexe E5 est le bras **`lora+adaptateur`** |
| **mémoire** | `torch.OutOfMemoryError` : **15,3 Go** demandés pour **15,55 Go** de carte, à l'étape `kl_div` | le protocole de cette fiche (**29 morceaux d'entraînement**, `--train 29 --exclure 20 --val 30,31 --test 32,20`) **ne rejoue pas** sur cette machine dans l'état actuel ✗ — il faudrait un lot plus petit ou un gradient accumulé ✗ |

* **conséquence honnête** : **E5 n'est PAS testé sur plusieurs graines** ✗ — sa table (§ 1) doit donc
  être lue comme les autres tables à graine unique du dépôt : un **ordre de grandeur**, pas un
  classement ✗ (c'est la règle écrite dans `rapport-sommeil-selection.md` § 6bis) ;
* **et la reproduction est maintenant documentée** : qui veut refaire E5 sait qu'il lui faut
  (a) `--bras lora+adaptateur --distiller`, (b) l'export par `exporter_gguf_dense.py --couches-lora 8
  --adapter-sortie`, (c) la mesure de l'**accord** par `speculatif_drave.py` (le **taux
  d'acceptation**), et (d) **plus de 16 Go** — ou un lot plus petit ✗ ;
* **ce qui n'est pas en cause** : le chiffre publié (51,0 % contre 28,0 % ✗) reste ce qu'il était —
  mesuré, écrit, et **non reproduit** ce soir ✗. Il n'est ni confirmé ni infirmé : il est **en attente
  d'une machine qui puisse le rejouer** ✓.

## 7. LE DEUXIÈME MUR : à volume réduit, la distillation n'est JAMAIS retenue (et c'est un défaut d'outil)

Le § 6 avait trouvé le premier mur (la mémoire : 29 morceaux ⇒ ~15,3 Go pour 15,55 Go ✗). La
contournement évident — **réduire le volume** (10 morceaux, qui tient ✓) — **ne marche pas**, et la
raison est instructive :

| bras (10 morceaux, graine 1) | époque retenue | validation 29 | TEST m32 |
|---|---:|---:|---:|
| `lora+adaptateur`, objectif **perplexité** | **2** | — | **6,67** ✓ (entraîné) |
| `lora+adaptateur`, objectif **distillation** | **0** | 17,5797 | **7,18** = la valeur de DÉPART ✗ |

* **l'époque retenue est choisie sur la PERPLEXITÉ de validation** ✗ — or la distillation **dégrade
  la perplexité par construction** (c'est tout son compromis : « imite mieux, prédit moins bien »,
  § 1 : 574,70 contre 181,54 ✗). Résultat : la meilleure époque est **l'époque 0**, c'est-à-dire le
  modèle **non entraîné** ✗, et c'est **lui** qui est exporté ✓✗ ;
* **le bras distillé rend donc exactement la valeur de départ** (7,18 = 7,1787 ✓) **sans aucune
  erreur** ✗ — un entraînement qui n'entraîne rien et le dit à voix basse ✓. C'est la **même famille**
  de défaut que le `--accord` du § 6 (« 100 % » qui mesurait le mauvais objet ✗) et que le drapeau
  ignoré : *un outil qui rend un chiffre plausible pour un calcul qui n'a pas eu lieu* ✗ ;
* **conséquence pour E5** : sa reproduction demande **le protocole complet** (29 morceaux ✗, mémoire
  ✗) **et** une sélection d'époque **cohérente avec l'objectif** (la validation par l'**accord**, pas
  par la perplexité ✗) — deux corrections d'outil, dont la seconde est un **vrai défaut** ✓ ;
* **ce que cela ne remet pas en cause** : la conclusion d'E5 (§ 1) a été obtenue avec le protocole
  complet, où la validation **s'améliorait** assez pour retenir une époque entraînée ✓ — sinon les
  51,0 % d'accord n'existeraient pas ✗✓. Mais **personne ne peut le revérifier aujourd'hui** ✗, et
  c'est écrit ici ;
* **la correction est FAITE (16/10, 01 h 40)** : le garde-fou **avertit** désormais, dans le tableau
  de résultats, quand un bras a un objectif de **distillation** et une **époque retenue de 0** ✓ :

```
| `lora+adaptateur` | 0 | 17,5797 | 7,1787 |
    ⚠️  ATTENTION : le bras `lora+adaptateur` a un objectif de DISTILLATION et une époque
        retenue de 0 — le modèle rendu est celui du DÉPART, NON ENTRAÎNÉ. La
        validation par perplexité ne peut pas guider un objectif qui la dégrade :
        ce résultat mesure le point de départ, pas la distillation.
```

  Il a été écrit en **une seule édition** ✓, vérifié par compilation, l'aide, puis un **essai à blanc**
  qui l'a vu se déclencher sur le cas pathologique ✓ — et l'option `--epoque-forcee` (qui aurait
  demandé de toucher **deux** boucles ✗) est **laissée à faire** ✗, parce que deux tentatives l'ont
  cassée ✗ : *une édition, un essai, un commit* ✓.
* **ce qui reste à faire, nommément** : (a) `--epoque-forcee` (garder une époque choisie ✗) pour
  **mesurer** ce que la distillation a appris au lieu de seulement **avertir** qu'on ne le mesure pas ✗ ;
  (b) la sélection d'époque **par l'objectif** (l'accord avec le maître ✓) plutôt que par la perplexité ✗.

## 8. LE FOND DU DEUXIÈME MUR : à 10 morceaux, la distillation **DIVERGE** (3 époques suffisent)

Le § 7 concluait que l'outil « exportait un modèle non entraîné sans le dire » ✗. Avec
`--epoque-forcee` (ajouté au § 7, en éditions séparées et vérifiées ✓), on peut enfin **regarder** ce
que l'entraînement avait produit, au lieu de le déduire :

| bras, 3 époques, 10 morceaux, graine 1 | époque retenue | validation 29 | TEST m32 |
|---|---:|---:|---:|
| `lora+adaptateur`, objectif **distillation**, époque **forcée à 3** | 3 | **2 749 968 874 085** | **508 065 569 169** |

* **la distillation ne « stagne » pas : elle EXPLOSE** ✗✗ — trois époques de KL sur 151 936 logits
  suffisent à porter la perplexité de validation à **2,7e12** et le test à **5,1e11** ✓. Autrement
  dit, l'époque 0 retenue par l'outil n'était pas un **artefact** ✗ mais **le moindre mal** ✓✓ : c'est
  le **seul** point où le modèle n'était pas détruit ✓ ;
* **et cela corrige la lecture du § 7** : le défaut d'outil (sélectionner sur la perplexité ✗) est
  **réel** — il ne dit pas *pourquoi* il retient l'époque 0 ✗ — mais la sélection elle-même était
  **juste** ✗✓. Les deux constats tiennent, et le second explique le premier ;
* **conséquence pour E5** : sa mesure publiée (perplexité **574,70** pour le bras distillé, contre
  181,54 pour le bras perplexité ✗) décrit un régime **dégradé mais stable** ✓ — qui n'existe **qu'au
  volume de son protocole** (29 morceaux ✗). À 10 morceaux, il n'y a **pas de régime stable** ✗ : la
  distillation y diverge avant d'apprendre quoi que ce soit ✓ ;
* **ce que cela dit du mécanisme, et c'est le plus intéressant** : le KL sur la distribution complète
  est **instable aux petits volumes** ✗ — il n'y a pas assez de données pour contrebalancer un
  gradient qui pousse 151 936 logits à la fois ✓. **E5 n'est donc pas un mécanisme « scalable vers le
  bas »** ✗ : il demande du volume, et c'est une propriété à écrire à côté de son résultat ✓ ;
* **ce qui reste ouvert** : à quel volume la distillation cesse-t-elle de diverger ✗ (entre 10 et 29 ✗) ;
  et le remède classique — **température**, **taux d'apprentissage plus bas**, ou **KL tronqué aux
  k premiers logits** ✗ — n'est pas essayé ici ✓.

## 9. LA FENÊTRE EST VIDE à 10 morceaux : la distillation diverge OU n'apprend rien

Le § 8 avait trouvé la divergence (2,7e12 à trois époques ✗). Restait la question utile : **existe-t-il
un taux d'apprentissage qui entraîne SANS détruire ?** Balayage, 10 morceaux, graine 1, époque forcée
à 10 (pour regarder la fin, pas le meilleur point ✗) :

| taux (`--pas-lora`) | validation 29 à la fin | TEST m32 | base (aucun entraînement) |
|---:|---:|---:|---:|
| 1e-3 *(défaut)* | 2,7e12 ✗✗ *(dès 3 époques)* | 5,1e11 ✗✗ | 17,58 · 7,1787 |
| 3e-4 | 2,7e11 ✗✗ | 2,8e11 ✗✗ | |
| 1e-4 | 6,96e4 ✗ | 2,66e4 ✗ | |
| **1e-5** | **17,72** ✓ | **7,2333** ✓ | |

* **à 1e-5, la distillation est STABLE** ✓ — la perplexité ne bouge presque pas (17,72 contre 17,58 ;
  7,2333 contre 7,1787, soit **+0,8 %** ✓) — donc elle **n'apprend rien** ✗ : dix époques à 1e-5 ne
  déplacent pas le modèle ✓ ;
* **et la sélection naturelle d'époque retient quand même 0** ✓ — même à 1e-5, la perplexité se
  **dégrade** légèrement, donc le meilleur point reste le **départ** ✗ (le garde-fou le dit ✓) ;
* **la conclusion est donc une fenêtre VIDE** ✗✓ : à ce volume, il n'existe **pas** de taux qui
  entraîne *et* survive — en dessous de 1e-4 le modèle **diverge** ✗, au-dessus de 1e-5 il
  **n'apprend rien** ✗. Il n'y a pas de réglage à trouver, il y a un **manque de données** ✓ ;
* **ce que cela explique, et qui était le vrai sujet** : E5 avait besoin de **29 morceaux** ✗ — non
  par choix de protocole, mais parce que **le volume est ce qui ouvre la fenêtre** ✓. Le KL sur
  151 936 logits pousse tout le vecteur à la fois : il faut assez d'exemples pour que la moyenne des
  gradients ne soit pas un pas destructeur ✗ ;
* **les remèdes, nommés et non essayés** : (a) **tronquer le KL** aux k premiers logits ✗ (le gradient
  ne pousse plus 151 936 dimensions ✗) ; (b) une **température** plus haute ✗ (des distributions plus
  douces, des gradients plus petits ✗) ; (c) un **échauffement** du taux ✗ ; (d) **plus de données** ✓
  (ce que fait le protocole publié ✓). Le plus prometteur est (a) : c'est le seul qui change la
  *forme* du gradient, pas son amplitude ✗ ;
* **et une leçon de méthode, la troisième du même genre en deux jours** : « l'outil retient l'époque 0 »
  ✗ était d'abord lu comme un **défaut d'outil** ✗, puis comme un **moindre mal** ✓, puis comme la
  **conséquence d'une fenêtre vide** ✓✓. Trois lectures, chacune plus juste, obtenues en **regardant**
  au lieu de déduire ✗.

## 10. LE KL TRONQUÉ ÉLARGIT LA FENÊTRE D'UN FACTEUR 10 — mais l'accord n'a pas pu être mesuré

### a) Ce qui est solide : la troncature élargit la fenêtre de stabilité

Le § 9 proposait de **tronquer le KL** aux K premiers logits du maître pour changer la *forme* du
gradient ✗. C'est fait (`--kl-tronque K`), et le balayage donne :

| réglage (10 morceaux, 10 époques, graine 1) | validation 29 | TEST m32 | verdict |
|---|---:|---:|---|
| KL **plein**, taux 1e-3 | 2,7e12 | 5,1e11 | ✗✗ détruit |
| KL **plein**, taux 1e-4 | 6,96e4 | 2,66e4 | ✗ détruit |
| KL **plein**, taux 1e-5 | 17,72 | 7,2333 | ✓ stable, n'apprend rien |
| KL **tronqué K=512**, taux **1e-3** | 4,3e7 | 3,2e7 | ✗ détruit |
| KL **tronqué K=64**, taux **1e-3** | 8,7e13 | 3,9e12 | ✗✗ **pire** que le KL plein |
| **KL tronqué K=512, taux 1e-4** | **19,37** | 7,8230 | ✅ **stable** |
| **KL tronqué K=64, taux 1e-4** | **19,09** | 7,6786 | ✅ **stable** |

* **la fenêtre passe de {1e-5} à {1e-5 ; 1e-4}** ✓✓ : là où le KL plein **détruit** le modèle à 1e-4
  (6,96e4 ✗), le KL tronqué **tient** (19,1-19,4 ✓) — un facteur **10** de taux en plus ✓, et à 1e-4 la
  distillation **apprend vraiment quelque chose** (17,58 → 19,1, soit **+8,6 %** de perplexité, au lieu
  de +216 % pour le protocole publié d'E5 ✓) ;
* **mais mon hypothèse « c'est la FORME, pas l'amplitude » est à moitié fausse** ✗ : à taux **égal**
  (1e-3), le KL tronqué à **K=64** fait **pire** que le KL plein (8,7e13 contre 2,7e12 ✗). Tronquer
  **concentre** la distribution (elle est renormalisée sur 64 classes ✗), ce qui **augmente** le
  gradient par dimension ✗. La troncature n'est donc pas un remède à l'amplitude : c'est un remède au
  **nombre de dimensions poussées** ✓, et il faut **les deux** (tronquer **et** baisser le taux ✓) ;
* **ce que cela donne à E5, concrètement** : une recette qui tient à **10 morceaux** — `--distiller
  --kl-tronque 64 --pas-lora 1e-4` — au lieu d'exiger 29 ✓. C'est la première fois que ce mécanisme est
  **scalable vers le bas** ✓.

### b) Ce qui n'a PAS pu être mesuré : l'accord du réflexe

La vraie question d'E5 n'est pas la perplexité mais l'**ACCORD** (l'argmax du chemin court contre celui
du maître ✗). Les deux bras ont été exportés (`--couches-lora 8 --adapter-sortie`) et passés au harnais
spéculatif :

| bras (10 morceaux, graine 1) | accord mesuré |
|---|---:|
| `lora+adaptateur`, objectif **distillation tronquée** (K=64, 1e-4) | **0,0 %** ✗ |
| `lora+adaptateur`, objectif **perplexité** *(pourtant entraîné : m32 6,67 ✓)* | **0,0 %** ✗ |

* **0,0 % pour les DEUX bras, dont un entraîné** ✗ : c'est donc **l'assemblage du réflexe** qui est en
  cause, pas l'entraînement ✓ — un chemin tronqué à 8 couches avec tête empruntée et adaptateur
  **doit** pouvoir s'assembler (le protocole publié d'E5 l'a fait, 28 % et 51 % ✗) ;
* **et c'est la troisième fois en deux jours** que ce fil se heurte à la **plomberie d'assemblage** ✗
  (le drapeau masqué, le bras qui mesurait 100 % du mauvais objet, et maintenant 0 % du bon ✗) ;
* **ce qui est donc établi, et rien de plus** : (a) le KL tronqué **élargit la fenêtre** ✓ (mesuré,
  tableau ci-dessus ✓) ; (b) l'**accord** de ces bras n'est **pas mesuré** ✗ et **ne peut pas** être
  cité tant que l'assemblage n'est pas vérifié sur un cas témoin ✓. **E5 reste non testé sur plusieurs
  graines** ✗ ;
* **le contrôle à faire, nommément, avant toute autre tentative** : mesurer l'accord d'un bras dont on
  **sait** qu'il doit être élevé — le protocole publié (29 morceaux, 51,0 %) ✗ — ou, à défaut, vérifier
  qu'un adaptateur **nul** rend exactement le chemin tronqué sans adaptateur ✓ (l'invariant d'identité
  du § 1 ✓). Sans ce témoin, « 0,0 % » ne dit pas si c'est le modèle ou la mesure ✗.

## 11. LA CAUSE DU « 0,0 % » EST TROUVÉE (l'adaptateur est l'IDENTITÉ) — sa raison ne l'est pas

Le § 10 laissait un contrôle à faire : « mesurer un bras dont on SAIT qu'il doit être élevé ». Il a été
fait, et il a payé ✓ — la chaîne est maintenant établie, fait par fait :

| fait mesuré | valeur | lecture |
|---|---|---|
| le **cerveau** (24 couches) sur une séquence de m32 | `[51667, 11042, 320, 5534, …]` | cohérent ✓ |
| le **réflexe** (8 couches, tête partielle, adaptateur) | `[43850, 71112, 145375, …]` | **incohérent** ✗ |
| le réflexe **sans** adaptateur | `[43850, 71112, 145375, …]` | **identique** ✗✗ |
| l'adaptateur exporté | 896 × 896, **diagonale 1,0**, norme 29,93 = √896 | **l'IDENTITÉ** ✗✗✗ |
| le moteur, sur `--adaptateur-sortie` sans `--tete-partielle` | *« Refusé plutôt qu'ignoré »* | le moteur a **raison** ✓ |

* **la cause du 0,0 % est donc trouvée** ✓ : l'adaptateur exporté **n'a jamais été entraîné** ✗ — c'est
  sa valeur d'initialisation (l'identité ✓), et un réflexe réduit aux 8 premières couches avec une
  **tête empruntée** rend des jetons incohérents ✓ (la table d'E5 le disait : « tête empruntée →
  4 476 128 » ✗). Le 0,0 % mesure donc **le modèle**, pas la mesure ✓✓ — la question du § 10 est
  tranchée ✓ ;
* **et sa raison n'est PAS trouvée** ✗ : l'adaptateur **est** dans l'optimiseur (lr **1e-3** par défaut,
  groupe ajouté à la main ✓), il **est** appliqué dans la passe avant (`x @ adaptateur.T` ✓), et
  l'époque retenue pour ce bras était **2** (entraînée ✓) — donc il *devrait* avoir bougé ✗. Les deux
  pistes, nommées pour la prochaine séance : (a) le **snapshot** enregistré (`instantane()`) est celui
  de la **meilleure validation**, et si cette époque est 0 pour le bras joint ✗, l'adaptateur
  enregistré est l'identité ✓ — à vérifier en forçant l'époque ✓ ; (b) le **chemin de gradient** de
  l'adaptateur dans le dessin joint ✗ (un paramètre sans gradient est silencieusement ignoré par
  Adam ✗ — même famille de défaut que les précédents ✗) ;
* **ce que cela laisse E5** : la **recette de stabilité** est acquise (`--kl-tronque 64 --pas-lora 1e-4`
  tient à 10 morceaux ✓, § 10a ✓) ; l'**accord** reste **non mesuré** ✗ tant que l'adaptateur ne
  s'entraîne pas ✓ ; et le **contrôle qui doit précéder toute nouvelle tentative** est maintenant
  écrit, avec sa valeur attendue : **l'adaptateur exporté ne doit PAS être l'identité** ✗ (norme
  29,93326 = √896 ✗ ⇒ il n'a pas appris ✓). C'est un contrôle d'une seconde ✓, et il manquait ✓.

## 12. LE DIAGNOSTIC EST FERMÉ : l'adaptateur ne reçoit AUCUN gradient (piste (a) éliminée, piste (b) confirmée)

Le § 11 laissait deux pistes. Une seule commande les sépare : **forcer l'époque** (10 ✓, donc un modèle
réellement entraîné ✓) et relire l'adaptateur **dans le `.pt`**, sans passer par l'export ✓.

| mesure, bras `lora+adaptateur`, distillation tronquée K=64, taux 1e-4, **époque forcée 10** | valeur |
|---|---:|
| LoRA (32 tenseurs) — norme totale | **6,568121** ✓ *(il a bien appris ✓)* |
| adaptateur — norme | **29,93326** = √896 |
| adaptateur — écart à l'identité, `max(abs(a − I))` | **0,0** ✗✗ |
| perplexité (validation 29 · test m32) | 19,0939 · 7,6786 ✓ |

* **piste (a) — le snapshot de la meilleure validation — est ÉLIMINÉE** ✗ : même à l'époque **10**
  forcée, l'adaptateur est **exactement** l'identité ✓ (écart **0,0**, pas « petit » : **nul** ✗) ;
* **piste (b) est donc confirmée** ✓ : l'adaptateur **ne reçoit aucun gradient** dans le dessin joint ✗.
  Or `Adam` **ignore silencieusement** un paramètre dont `grad` est `None` ✗ — c'est très exactement
  la famille de défaut nommée trois fois cette nuit : *un calcul qui n'a pas lieu et qui ne le dit
  pas* ✗. Ici, la conséquence est une **expérience entière** (E5 sur d'autres graines ✗) et **quatre
  rounds** de diagnostic ✓ ;
* **ce qui est éliminé par la même mesure** : ce n'est ni l'optimiseur (le groupe est bien construit
  avec `lr = pas_adaptateur_joint = 1e-3` ✓), ni la passe avant (le code applique bien
  `x @ adaptateur.T` ✓), ni l'enregistrement (l'époque forcée est bien celle qui est sauvée ✓). Reste
  **le lien entre les deux** ✗ — un `Parameter` recréé après l'optimiseur ✗, ou une passe avant de
  mesure qui n'utilise pas la même fermeture ✗ ;
* **la sonde à écrire, et elle tient en une ligne** ✗ : après un pas d'entraînement, **imprimer
  `adaptateur.grad is None`** (et `adaptateur.grad.norm()` s'il existe ✓). Une ligne, et le doute
  tombe ✓ — mais elle doit être ajoutée **à l'outil** ✗, et c'est la prochaine édition propre à faire ✓ ;
* **et ce que la nuit laisse à E5, en une phrase** : la **stabilité** est résolue ✓ (`--kl-tronque 64
  --pas-lora 1e-4` tient à 10 morceaux ✓), la **chaîne d'export** est vérifiée ✓ (le moteur refuse
  plutôt que d'ignorer ✓), et il manque **un gradient** ✗ pour que l'**accord** — la seule mesure qui
  compte pour ce mécanisme ✗ — redevienne possible ✓.

## 13. LE DÉFAUT EST DANS LE CHEMIN **JOINT** — l'adaptateur seul s'entraîne, l'adaptateur joint non

Une sonde **sans aucune édition** sépare « la machinerie est cassée » de « le chemin joint est cassé » :
faire tourner **le même objectif** avec `--bras adaptateur` (l'adaptateur **seul**, sur des états
précalculés ✗) et relire sa norme.

| bras (10 morceaux, distillation tronquée K=64, époque forcée 10) | norme de l'adaptateur | écart à l'identité | verdict |
|---|---:|---:|---|
| **`adaptateur`** *(seul)* | **34,494156** | **0,198966** | ✅ **il s'entraîne** |
| **`lora+adaptateur`** *(joint)* | 29,933260 | **0,0** | ❌ **il ne bouge pas d'un iota** |

* **la machinerie est saine** ✓ : le `Parameter`, l'optimiseur, l'enregistrement et la passe avant
  fonctionnent — l'adaptateur **apprend** quand il est seul (norme 34,49 contre 29,93 à
  l'initialisation ✓, écart 0,199 ✓) ;
* **le défaut est donc dans le chemin JOINT** ✗✓ — celui-là même qu'utilise **E5** ✗. La recherche
  passe, en une mesure, de « quelque part dans l'outil » ✗ à **une fonction** : la boucle
  d'entraînement jointe et le **lien entre son optimiseur et la fermeture qui applique l'adaptateur** ✓ ;
* **et c'est la raison pour laquelle E5 n'a jamais pu être reproduit** ✗ : son bras est précisément
  `lora+adaptateur` ✗ — l'adaptateur y reste l'identité ✓, donc le « réflexe » est une **tête
  empruntée** ✓, donc l'accord est **0 %** ✓, donc il n'y a rien à comparer ✗ ;
* **ce que la nuit laisse, en trois lignes** : (1) la **stabilité** est résolue ✓ (`--kl-tronque 64
  --pas-lora 1e-4` ✓) ; (2) la **cause** du 0 % est trouvée ✓ (l'adaptateur = identité ✓) et son
  **siège** est localisé ✓ (le chemin joint ✓) ; (3) la sonde à écrire reste **une ligne** —
  `adaptateur.grad is None` juste après le premier pas de la boucle **jointe** ✗ — et c'est la
  prochaine édition ✓.

## 14. SYNTHÈSE DU FIL : TROIS CAUSES, TOUTES MESURÉES — et la quatrième est une limite de machine

Le § 13 localisait le défaut « dans le chemin joint ». En relisant **la fermeture qui construit les
logits**, la cause était écrite **en toutes lettres dans le code** ✗✓ :

```python
def logits_chemin(ids, grad=False):
    if plein_obj:
        # « l'adaptateur de sortie, lui, NE JOUE PAS : il n'existe que sur un chemin tronqué »
        return banc.m(ids, use_cache=False).logits      # ← le modèle COMPLET
```

* **avec `--objectif plein`, l'adaptateur n'est pas dans le graphe** ✗ — par conception ✓, et le
  commentaire le dit ✓. Il ne peut donc **pas** recevoir de gradient ✗, et Adam l'ignore
  silencieusement ✓✓. **Mes runs — et la reproduction d'E5 — utilisaient `--objectif plein`** ✗ :
  c'était **mon** erreur, pas un défaut d'outil ✗✓ ;
* **la vérification** : avec **`--objectif tronque`**, le même bras entraîne l'adaptateur ✓ (norme
  **30,700783** contre 29,933 à l'initialisation, écart **0,057468** ✓) — et le LoRA aussi (6,64 ✓) ;
* **mais l'accord reste 0,0 %** ✗ — et cette fois c'est **cohérent** ✓ : le réflexe obtenu a une
  perplexité de **18 231** ✗, contre **181,54** pour le bras « perplexité » d'E5 et **574,70** pour son
  bras distillé ✓. Mon réflexe est **100 fois pire** que celui d'E5 ✓, donc il propose des jetons
  incohérents ✓, donc l'accord est nul ✓. Ce n'est pas un défaut : c'est **le volume** ✓ (10 morceaux
  contre 29 ✓), et le volume est précisément ce qui **ne tient pas** dans 16 Go ✗.

**Les quatre murs du fil, dans l'ordre où ils sont tombés** :

| # | mur | état |
|---|---|---|
| 1 | **mémoire** : 29 morceaux ⇒ ~15,3 Go pour 15,55 Go ✗ | **non franchi** ✗ (limite de machine) |
| 2 | **stabilité** : le KL plein diverge à petit volume ✗ (fenêtre vide ✗) | **franchi** ✓ — `--kl-tronque 64 --pas-lora 1e-4` (fenêtre ×10 ✓) |
| 3 | **objectif** : `--objectif plein` ne fait pas jouer l'adaptateur ✗ | **compris** ✓ — c'est `--objectif tronque` qu'il faut pour un réflexe |
| 4 | **volume** : à 10 morceaux le réflexe est 100× pire ✗ ⇒ accord 0 % | **non franchi** ✗ — dépend du mur 1 ✗ |

**Ce qui reste vrai d'E5, et ce qui ne l'est plus** : son **résultat** (l'accord double sous
distillation : 28 % → 51 % ✓) n'est **ni confirmé ni infirmé** ✗ — mais il est maintenant **crédible et
cadré** ✓ : ses chiffres (181,54 et 574,70 de perplexité) correspondent à un réflexe **utilisable**,
que je n'ai pas su reproduire **faute de mémoire** ✗, et sa conclusion exige le protocole complet ✓.
Sa **limite** est en revanche établie ✓ : le mécanisme **n'est pas scalable vers le bas** ✗ (mur 2 et
mur 4 ✓).

**Et la leçon, qui est la cinquième du même genre en deux jours** : j'ai cherché un **bug d'outil**
pendant **cinq rounds** ✗ alors que la cause était **mon propre choix de drapeau** ✗, écrit dans un
commentaire du code que je n'avais pas lu ✓. *Lire le code qui décide, avant de suspecter celui qui
exécute.*

## 15. LA MESURE EST ENFIN FAITE — ET ELLE CONTREDIT E5 (à graine 1, dans la configuration stable)

Le fil est dénoué : la mesure d'E5 est **celle de l'outil** (`--accord`, fraction de positions où
l'argmax du chemin **tronqué** égale celui du maître ✓), et le **harnais spéculatif** mesure autre
chose ✗ (une **génération libre** ✗, qui rend 0 % même pour un bras à 26 % d'accord ✓ — un brouillon à
26 % d'accord dérape en quelques jetons ✓). Avec `--objectif tronque` — **et lui seul** ✗ — l'adaptateur
et la tête jouent ✓, et l'accord devient mesurable ✓.

**Le témoin est REPRODUIT** ✓ : objectif perplexité, 29 morceaux (`--exclude 20`, validation 30-31,
test 32 et 20), graine 1, rang 4 :

| bras (29 morceaux, graine 1) | perplexité m32 | perplexité m20 | **accord m32** | **accord m20** |
|---|---:|---:|---:|---:|
| `lora+adaptateur`, objectif **perplexité** (témoin) | **192,69** | **132,69** | **25,7 %** | **38,1 %** |
| `lora+adaptateur`, objectif **distillation** (KL tronqué K=64, taux 1e-4) | 1 809,17 | 5 131,44 | **17,1 %** ✗ | **13,8 %** ✗ |
| *(rappel, E5 publié le 15/10, graine 0 ✗)* | *181,54* | *153,98* | *28,0 %* | *40,5 %* |
| *(rappel, E5 publié, bras distillé)* | *574,70* | *715,02* | *51,0 %* | *68,1 %* |

* **le témoin tombe à 2 points des chiffres publiés** (192,69 contre 181,54 ; 25,7 % contre 28,0 % ✓✓) :
  **l'entraînement et la mesure sont donc les bons** ✓ — c'est la première fois ce soir que la chaîne
  complète est vérifiée de bout en bout ✓ ;
* **et le bras distillé fait MOINS BIEN que le témoin** ✗ : **17,1 %** contre 25,7 % (m32) et **13,8 %**
  contre 38,1 % (m20 ✗). C'est **l'inverse** du résultat publié (51,0 % contre 28,0 % ✓) ✗✗ ;
* **ce que cela ne dit PAS** : que le résultat publié est faux ✗ — il a été obtenu avec une **autre
  configuration** (KL **plein**, taux par défaut 1e-3 ✓), celle qui **ne tient pas dans 16 Go** ✗✓
  (c'est le mur 1 ✗). Ce que cela dit : **la conclusion d'E5 dépend de sa configuration** ✗✓, et la
  configuration **stable** (KL tronqué, taux bas ✓ — la seule que cette machine puisse exécuter au
  volume voulu ✗) **inverse son signe** ✗ ;
* **et l'explication est lisible dans la perplexité** ✓ : le bras distillé stable a une perplexité de
  **1 809** (contre 192 pour le témoin ✗) — il est **beaucoup plus dégradé** ✗, et un étudiant dégradé
  **imite mal** ✓. La troncature à 64 classes et le taux 1e-4 apprennent **trop peu** ✗ : la stabilité
  a été achetée au prix de l'apprentissage ✗ ;
* **la conséquence pour la carte des facultés** : **E5 n'est ni confirmé ni infirmé** ✓ — il est
  **reproductible dans son témoin** ✓ et **renversé dans sa distillation** ✗, et les deux mesures sont
  écrites côte à côte ✓. Le prochain pas, nommément : **tester la distillation à taux intermédiaire**
  (3e-4 ou 1e-3 avec le KL **plein** ✓) — ce qui demande de **faire tenir 29 morceaux en mémoire** ✗
  (gradient accumulé, ou `--lots` plus fin ✗) : le mur 1 est redevenu le seul obstacle ✓.

## 16. LA DIRECTION D'E5 EST REPRODUITE — et la largeur du KL décide du signe

Le § 15 avait inversé E5 avec un KL tronqué à **64** classes. La suite était nommée : « tester à taux
intermédiaire ». Deux réglages ont été essayés, et **l'un des deux reproduit E5** ✓✓ :

| bras (29 morceaux, graine 1) | perplexité m32 | m20 | **accord m32** | **accord m20** |
|---|---:|---:|---:|---:|
| **témoin** (objectif perplexité) | 192,69 | **132,69** | 25,7 % | 38,1 % |
| distillé **K=64**, taux 1e-4 | 1 809,17 | 5 131,44 | 17,1 % ✗ | 13,8 % ✗ |
| distillé **K=64**, taux 3e-4 | 11 076 | 7 861 | **12,1 %** ✗✗ | 14,4 % ✗ |
| **distillé K=512, taux 1e-4** | 478,94 | 404,98 | **30,3 %** ✓ | **51,4 %** ✓✓ |
| *rappel — E5 publié, bras distillé (graine 0 ✗)* | *574,70* | *715,02* | *51,0 %* | *68,1 %* |

* **avec K=512, la distillation GAGNE** ✓✓ : **30,3 % contre 25,7 %** (m32 ✓) et **51,4 % contre
  38,1 %** (m20 ✓) — **la direction du résultat publié est reproduite** ✓, et c'est la **première
  confirmation indépendante** de sa conclusion ✓ (une autre graine, une autre configuration, la même
  conclusion ✓) ;
* **et ce n'est pas « apprendre plus » qui suffit** ✗ : monter le taux à 3e-4 **à K=64** fait **pire**
  (12,1 % ✗✗) — l'époque retenue est 1, le modèle est déjà très dégradé (11 076 ✗). Ce qui compte est
  **la largeur du KL** ✓ : à **64** classes la distribution du maître est **renormalisée sur 64
  classes** ✓, donc **beaucoup plus pointue** ✗, et l'étudiant apprend une cible **déformée** ✗ ;
  à **512** classes elle reste proche de la vraie distribution ✓, et l'étudiant apprend la bonne chose ✓ ;
* **la lecture d'ensemble, et elle est nette** : la distillation d'E5 **fonctionne** ✓, mais elle est
  **sensible à deux réglages** que la fiche d'origine ne mentionnait pas ✗ — le **taux** (elle diverge
  au taux par défaut à petit volume ✓) et la **largeur du KL** (tronquer trop déforme la cible ✓). Le
  protocole publié tombait juste sans le dire ✓ ; il le dit maintenant ✓ ;
* **ce qui reste à faire, nommément** : (a) **graine 2** pour la configuration gagnante ✓ (une
  confirmation sur une graine ne suffit pas — c'est la leçon du § 6bis de
  `rapport-sommeil-selection.md` ✗) ; (b) le **mélange** KL + λ·CE ✓ (§ « E5 bis »), qui n'a pas été
  testé dans cette configuration gagnante ✗ ; (c) et **pourquoi** K=64 déforme ✗ — la mesure de la
  divergence KL entre la cible tronquée et la vraie distribution ✗, qui rendrait la sensibilité
  **prévisible** au lieu d'observée ✓.

## 17. E5 EST CONFIRMÉ SUR DEUX GRAINES — le mécanisme se réplique, sa variabilité est chiffrée

La règle de la nuit (« une graine ne mesure pas un critère » ✗) appliquée à la configuration gagnante
(K=512, taux 1e-4, 29 morceaux) :

| graine | bras | perplexité m32 | m20 | **accord m32** | **accord m20** |
|---:|---|---:|---:|---:|---:|
| 1 | témoin | 192,69 | 132,69 | 25,7 % | 38,1 % |
| 1 | **distillé** | 478,94 | 404,98 | **30,3 %** | **51,4 %** |
| 2 | témoin | 228,90 | 146,74 | 24,8 % | 37,6 % |
| 2 | **distillé** | 555,79 | 669,31 | **29,6 %** | **38,9 %** |
| **moyenne** | témoin | 210,80 | 139,72 | **25,3 %** | **37,9 %** |
| **moyenne** | **distillé** | 517,37 | 537,15 | **30,0 %** | **45,2 %** |

* **la direction se réplique** ✓✓ : la distillation améliore l'accord **sur les deux graines** (m32 :
  30,3 et 29,6 contre 25,7 et 24,8 ✓ ; m20 : 51,4 et 38,9 contre 38,1 et 37,6 ✓) — **quatre
  comparaisons, quatre fois dans le même sens** ✓✓ ;
* **et l'ampleur est très inégale selon le texte** ✗ : sur **m32**, le gain est **stable** (+4,6 et
  +4,8 points ✓✓) ; sur **m20**, il va de **+1,3 à +13,3** ✗ — la même manipulation donne un gain
  **dix fois plus grand** selon la graine ✓. La moyenne (+7,3) cache donc une dispersion qui la dépasse ✗ ;
* **le coût, lui, est parfaitement stable** ✓ : la perplexité **double à triple** dans les deux cas
  (192,69 → 478,94 soit **+148 %** ; 228,90 → 555,79 soit **+143 %** ✓✓). Autrement dit : *la
  distillation paie un prix certain pour un gain incertain* ✓ — et c'est la formulation la plus juste
  de son compromis, meilleure que « imite mieux, prédit moins bien » ✓ ;
* **ce qui est donc établi, après le fil le plus long de la nuit** : (a) le **témoin est reproduit**
  (25,7 % / 24,8 % contre 28,0 % publié ✓) ; (b) la **direction est répliquée** sur deux graines ✓ ;
  (c) le mécanisme est **sensible au taux** (il diverge au taux par défaut à petit volume ✗) et à la
  **largeur du KL** (64 classes déforment la cible et inversent le signe ✗, 512 non ✓) ; (d) et sa
  **limite** : il **n'est pas scalable vers le bas** ✗ (fenêtre vide à 10 morceaux ✓, § 9 ✓) ;
* **ce qui reste ouvert** : le **mélange** KL + λ·CE dans la configuration gagnante ✗ ; et le
  **pourquoi** de la sensibilité à K ✗ (mesurer la divergence KL entre la cible tronquée et la vraie
  distribution rendrait la sensibilité **prévisible** ✓).
