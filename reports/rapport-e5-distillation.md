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

## 3. Ce que cette fiche ne dit pas

* **une seule température de distillation** (T = 1) et un seul poids relatif (pas de mélange
  KL + CE) : le réglage classique (T = 2 à 4, ou KL + λ·CE) n'est pas essayé — et il pourrait
  rendre l'accord **sans** perdre la perplexité, ce qui est exactement la question ouverte ;
* **pas de distillation des états** (les couches intermédiaires du maître ne sont pas imitées) :
  seule la distribution de sortie l'est ;
* **une seule architecture d'étudiant** (8 couches + 896² + LoRA rang 8) : la capacité de
  l'étudiant borne l'accord atteignable, et sa courbe n'est pas faite ;
* **l'accord est mesuré en top-1** : un accord de distribution (KL, rang du jeton du maître) dirait
  plus, et n'est pas reporté ;
* **rien sur l'échantillonnage** (`--temp`, `--top-p`) : la dégénérescence observée en greedy peut
  disparaître en échantillonnant — ou pas ; ce n'est pas mesuré.
