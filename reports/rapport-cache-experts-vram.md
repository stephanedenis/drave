# Rapport — un cache d'experts en VRAM pour Kimi-K3 : mesuré, et pourquoi c'est non

**Question** (venue de Strata, `github.com/architectds/Strata`, via la vidéo
« Local AI Is Now 6x Faster on Your PC ») : garder les experts les plus appelés
dans la VRAM rend-il Kimi-K3 plus rapide ici ?

**Réponse courte : non.** ×1,09 prédit, pour un plafond absolu de ×1,41 — contre
un plafond de ×3,1 pour le chantier du dense, qui est déjà nommé.

## 1. Le plafond, avant toute mesure

Trafic disque d'un jeton de Kimi-K3, sur les postes **déjà mesurés**
(`tools/budget_execution_locale.py`, fichier complet) :

| poste | Go/jeton | part |
|---|---:|---:|
| **experts routés** (16 sur 896) | 25,83 | 29,3 % |
| experts partagés (2 par couche) | 12,40 | 14,1 % |
| **dense Q8_0** (attention, KDA, MLA, routage) | 48,56 | **55,1 %** |
| tête de sortie | 1,30 | 1,5 % |
| **total** | **88,09** | |

Un cache d'experts ne peut retirer **que** les 25,83 Go routés. Donc :

| taux de succès | gain |
|---|---:|
| 100 % (impossible) | **×1,41** |
| 70 % | ×1,26 |
| 47 % | ×1,16 |
| 25 % | ×1,08 |

## 2. Ce que la VRAM peut tenir

2 × 16 Go = 32 Go. Une matrice d'expert K3 (3 × 3072 × 3584 à 4,25 bits) pèse
**17,5 Mo** → **1 828 matrices**, soit **19,7 par couche sur 896**.

Un jeton en choisit **16**. Le cache tient donc **1,2 jeton** — à peine plus que
le besoin d'un seul. C'est la différence de fond avec Strata : chez eux 512
experts par couche et 34-50 Go de experts **tiennent tous en RAM** ; ici 896 par
couche et 1 508 Go au total.

## 3. Le taux de succès, mesuré sur le routage RÉEL de K3

Trace de routage obtenue du moteur (`DRAVE_K3_TRACE_EXPERTS`), 23 couches MoE ×
24 jetons de texte réel = 552 relevés, 16 experts par jeton :

| | K3 (896 experts/couche, 16/jeton) | Qwen3-30B-A3B (128, 8/jeton) |
|---|---:|---:|
| réutilisation immédiate (t−1 → t) | **30,2 %** | 46,9 % |
| LRU 20 experts/couche | **28,7 %** | — |
| LRU 32 | 34,5 % | 86,8 % |
| LRU 128 | 49,8 % | — |

**K3 réutilise beaucoup moins**, et c'était prévisible : 16 experts sur 896
veulent dire un ensemble de travail bien plus dispersé, et le cache (19,7
places) fait à peine la taille d'un jeton (16).

## 4. Le verdict

Avec 32 Go de VRAM et 28,7 % de succès :
`88,09 / (88,09 − 0,287 × 25,83) = 88,09 / 80,68` = **×1,09**.

**Neuf pour cent.** Ce n'est pas une optimisation, c'est un arrondi — pour un
cache à écrire, à peupler, à faire évoluer avec la conversation, et à déboguer.

Et le même effort porté sur le **dense** (emprunter les blocs Q8_0 pour que le
cache de pages garde les 59,6 Go résidents) a un plafond de **×3,1** : 61 Go des
88,09 Go d'un jeton.

## 5. Ce qui rendrait le chiffre meilleur, et qu'il faut dire

- **24 jetons, c'est court.** Un cache « adapté à la conversation » comme celui
  de Strata fait mieux sur un long contexte où le sujet persiste. La courbe LRU
  monte lentement (49,8 % à 128 experts/couche), donc l'ordre de grandeur ne
  changerait pas, mais un contexte long et répétitif améliorerait le taux.
- **Un seul texte, de la prose.** Notre mesure Qwen donnait 47,9 % en prose et
  48,8 % en code : l'écart est faible, mais il existe.
- **Le plafond, lui, ne dépend d'aucune de ces réserves** : 29,3 % du trafic,
  ×1,41 même avec un cache parfait. C'est ce qui tranche.

## 6. Ce que Strata apporte quand même

Trois idées, dont une seule passe le calcul :

1. **cache d'experts en VRAM** — mesuré ici, ×1,09 : non ;
2. **prélecture par le routeur de la couche suivante** — non mesuré. Recouvrir
   la latence disque a du sens quand le disque est le mur, et le routeur de la
   couche N+1 ne coûte presque rien à évaluer ;
3. **budget résident** (`--resident-budget-gib`) — c'est exactement le chantier
   du dense, qu'ils ont aussi identifié comme le levier quand la RAM manque.

Et une confirmation de méthode : ils ont rencontré **le même défaut que nous** —
des noyaux multi-jetons qui arrondissent autrement que mono-jeton, donc une
réponse gloutonne qui change selon le brouillon (leur issue #152) — et l'ont
traité comme nous : un drapeau opt-in et la mesure publiée.
