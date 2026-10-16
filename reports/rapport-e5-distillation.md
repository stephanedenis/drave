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
