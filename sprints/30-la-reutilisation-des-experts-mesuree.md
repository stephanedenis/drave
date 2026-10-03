# Sprint 30 — La réutilisation des experts, mesurée (et c'est le levier)

- **Début** : 11:40 · **Fin** : 12:40
- **Objectif** : le bloc 29 a montré qu'un jeton de Kimi-K3 lit **24,7 Go d'experts**
  et que **aucun placement** ne rend ça interactif. Restait LA question qui décide
  de tout : *les mêmes experts reviennent-ils ?* Ce bloc la mesure — sur un modèle
  qu'on peut faire tourner aujourd'hui, avec l'instrument du dépôt, en attendant
  que le téléchargement de Kimi-K3 se termine.
- **Engagement de fin** : dépôt vert, machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. L'instrument

`tools/analyse_reutilisation_experts.py` (neuf) lit une trace de routage
(`DRAVE_TRACE_EXPERTS`, une ligne par (couche, jeton)) et rend : la couverture,
la **réutilisation immédiate** (t−1 → t), la réutilisation **fenêtrée**, et la
**courbe d'un cache LRU** — donc ce qu'un cache rapporterait, sans en écrire un.

### 2. Les chiffres, sur trois relevés

Qwen3-30B-A3B (48 couches, **128 experts, 8 par jeton**), traces de 48 et 128
jetons de wikitext, et 128 jetons de code (le module de matvec du dépôt, tokenisé
par le tokenizer du modèle) :

| mesure | wikitext 48 | wikitext 128 | code 128 |
|---|---|---|---|
| **réutilisation immédiate** (t−1 → t) | 46,9 % | **47,9 %** | **48,8 %** |
| fenêtre de 4 jetons | 63,9 % | 68,5 % | 72,9 % |
| fenêtre de 16 jetons | 78,8 % | 84,5 % | 88,2 % |
| sur tout l'historique | 82,7 % | 93,1 % | 93,9 % |

**Près d'un expert sur deux est déjà là au jeton précédent**, et c'est vrai sur
les trois textes : la dépendance au texte est faible *sur cette mesure*.

### 3. Ce qu'un cache LRU rendrait — mesuré, pas espéré

| cache (experts/couche) | part des experts | wikitext 128 | **code 128** |
|---|---|---|---|
| 16 | 13 % | 62,0 % | 66,4 % |
| **32** | **25 %** | 80,3 % | **86,8 %** |
| 64 | 50 % | 92,0 % | 93,5 % |
| 128 | 100 % | 93,1 % | 93,9 % |

**Un quart des experts en cache sert 80 à 87 % des lectures.** C'est exactement la
forme qu'il faut pour un modèle qui ne tient pas : on ne garde pas tout, on garde
le quart le plus chaud.

### 4. Transposition à Kimi-K3 — chiffrée, avec ses réserves

Trafic d'experts de K3 : **24,7 Go/jeton**. Avec un cache qui capte 80 % :
**≈ 5 Go/jeton** ; à 2 Go/s (NVMe) cela fait 2,5 s au lieu de 12,4 s, et la partie
dense (62 Go, résidente, 20 Go/s) reste à 3,1 s : **≈ 5,6 s/jeton au lieu de
15 s**, sans autre changement qu'un cache.

**Réserves, nommées** : K3 a 896 experts (7× plus), 16 par jeton (2× plus) et un
routage **sigmoïde** (celui de Qwen3-30B est softmax) ; la courbe y sera
différente, et c'est le **jalon M6** que de la mesurer sur le modèle lui-même. La
conclusion de ce bloc est donc : *le levier existe et il est gros* — pas : *le
cache de K3 rapportera 80 %*.

### 5. Un contrôle croisé gratuit, et une limite

V4-Flash route par **table** (`tid2eid`, l'identifiant du jeton décide) : sa
réutilisation se lirait **sans rien calculer**. Mesuré : **3 couches sur 43**
portent cette table (0, 1, 2) — les 40 autres utilisent le routeur appris. Le
contrôle croisé est donc possible mais étroit ; il est noté, pas fait.

## Rétrospective — garder / changer / doute

**Garder.** Mesurer la réutilisation **avant** d'écrire un cache. L'historique du
dépôt aurait poussé à l'inverse : un cache RAM d'experts a déjà été construit et
mesuré **plus lent** (+4 % à 4 Go, +21 % à 32 Go) — sur un modèle où le noyau
servait déjà tout depuis le `buff/cache`. Ici, la question posée est la bonne :
*combien de lectures le cache éviterait-il ?* — et elle a une réponse chiffrée
avant la première ligne de code.

**Garder (2).** Le même instrument sur trois textes, sans effort supplémentaire :
c'est ce qui transforme « la réutilisation dépend du texte » (une réserve) en
« elle est stable à 47-49 % sur ces textes » (un fait). Les réserves se
*mesurent*, elles ne se récitent pas.

**Changer.** Le premier essai sur Qwen3-235B (un modèle de 86 Go sur disque dur) a
été tué après 13 minutes **sans avoir produit un seul jeton** — parce qu'un
téléchargement de 1,5 To écrivait sur le même disque. La leçon n'est pas « être
patient » : c'est **choisir le support avant de choisir le modèle** (le 30B est
resté dans le cache de pages et a mesuré en 6 minutes ce que le 235B n'aurait pas
donné en une heure).

**Doute.** Les trois relevés viennent du **même modèle** et de la même famille de
textes. Un MoE à routage sigmoïde (K2.7, GLM-5.3) et un modèle à 896 experts
pourraient donner une courbe sensiblement plus plate — auquel cas le cache
rapporterait moins. C'est précisément pourquoi la mesure de K3 (M6) est un
**préalable**, pas une confirmation.

**Doute (2).** Le taux de succès d'un cache LRU n'est pas le gain de temps : il
faut aussi payer la gestion, la mémoire, et la lecture des experts manquants en
parallèle du calcul. Le chiffre de 5,6 s/jeton est un **plancher de trafic**, pas
une mesure de débit.
