# Sprint 23 — La porte de correction, serrée, outillée, et poussée au contexte long

- **Début** : 04:30 · **Fin** : en cours (le bloc est dominé par une passe longue)
- **Objectif** : le bloc 22 a montré que la porte de correction était mesurée sur
  **quatre** positions — trop peu pour dire quoi que ce soit (25 % d'écart de
  perplexité, dont on soupçonnait qu'il venait de la longueur de la fenêtre). Ce
  bloc doit : (1) serrer la mesure, (2) écrire une **définition** utilisable à la
  place de « même perplexité », (3) en faire un **outil** qui rend un verdict, et
  (4) porter la comparaison au contexte long, comme le plan l'annonce depuis P6.
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. La porte serrée : 63 positions, et l'hypothèse confirmée

Mêmes identifiants, même contexte, protocoles alignés, 64 positions
(`--ctx 256 --limit 64 --dense --threads 16 --logits-bin`) contre
`tools/ref_logits` (llama.cpp) :

| mesure | llama.cpp | Drave | écart |
|---|---|---|---|
| perplexité (63 prédictions) | 16,2931 | **15,2520** | **6,4 % relatif** |
| NLL moyenne | 2,7907 | 2,7249 | 0,066 nat |

**Contre 25 % sur 4 jetons** : l'amplification chaotique décroît avec la longueur
de la fenêtre, comme annoncé. Sur les logits eux-mêmes : corrélation min **0,95500**,
moyenne **0,985210**, top-1 identique **56/63 (88,9 %)**, rang médian du vrai jeton
**0 des deux côtés**, corrélation de rang 0,98810.

### 2. Une définition écrite, à la place de « même perplexité »

Deux quantifications différentes ne peuvent pas donner la même perplexité : le
critère était inatteignable par construction. Les critères sont maintenant :

1. **corrélation des logits par position ≥ 0,95** au minimum, ≥ 0,98 en moyenne ;
2. **top-1 identique ≥ 85 %** ;
3. **perplexité à moins de 10 %**, et **seulement au-delà de 64 prédictions** —
   en dessous, la mesure ne dit rien : 25 % d'écart à 4 jetons, 6,4 % à 63.

### 3. La porte devient un OUTIL, exécuté à chaque passage

`tools/compare_logits.py --porte` rend un verdict et un code retour ; le tableau
par position est complété d'un **diagnostic par tranches** (une erreur de position
— RoPE, blocs compressés, fenêtre — fait croître l'écart ; une erreur de tête ou de
norme le laisse plat). `tools/portes.sh` (7quinquies) l'exécute sur Qwen2.5-0.5B,
71 prédictions, ~10 s en tout :

| mesure | valeur |
|---|---|
| corrélation par position | min **0,9959** · moyenne **0,9994** |
| top-1 identique | 67/71 (**94,4 %**) |
| perplexité | nous 20,7914 · référence 20,8790 (**0,42 %**) |

**Test adverse** (une porte qui ne sait pas échouer est une porte cassée) : le même
modèle à `--abits 8` fait tomber la corrélation **minimale** à 0,513 → refus, code 1.
C'est le critère du minimum qui l'attrape : la moyenne reste à 0,983 et la
perplexité à 1,5 %.

### 4. Le contexte long : ce que la mesure a coûté, et ce qu'elle a appris

Le plan annonce depuis P6 « à terme, la même comparaison sur une couche compressée
à contexte long ». Première tentative : **ctx 1 024, 1 023 prédictions**. Elle a été
**arrêtée après 25 minutes et 6 positions** : le moteur écrivait **une ligne de
logits par minute**, soit **≈ 60 s par jeton** — 17 heures pour la passe complète.

Ce que cette mesure a appris, et qui n'était écrit nulle part :

| contexte | coût par jeton | dont attention | dont proj+mlp |
|---|---|---|---|
| 32 | **3,2 s** | 1,19 s | 2,04 s |
| 1 024 | **≈ 60 s** | (croissance) | — |

- Le coût du jeton **croît avec le contexte** — l'attention à longue portée n'est
  pas gratuite dans notre moteur, alors que llama.cpp fait la même passe de 1 024
  jetons en ~4 minutes (**≈ 0,2 s/jeton**, soit ~300 fois moins).
- `--dense` est **inerte pour V4-Flash** : PPL identique au chiffre près (72 793,4696)
  et durées identiques avec et sans ; le compteur « dont en listes » reste à
  **0,0 M** — ce modèle passe par le chemin dense de toute façon. Un drapeau qui ne
  fait rien doit être dit, pas laissé croire.
- La cause structurelle est nommée dans le code : **l'indexeur des couches CSA
  n'est pas implémenté** (`attention.indexer.top_k` = 512 pour V4-Flash). Tant que
  le nombre de blocs reste sous ce seuil, garder tous les blocs est **exact** ;
  au-delà, le moteur refuse au lieu de choisir faux — mais en dessous du seuil, il
  paie l'attention sur tous les blocs. C'est le poste à instruire pour le contexte
  long, et il ne se voyait pas à ctx 32.

**La porte longue est donc portée à ctx 256** (255 prédictions, mêmes identifiants),
où les blocs compressés sont publiés (ratio 4 → ~64 blocs) et où le coût reste
tenable (~10 s/jeton mesuré). C'est un contexte **dix fois plus long** que la porte
habituelle, et le verdict est en fin de sprint.

## Rétrospective — garder / changer / doute

**Garder.** Serrer une mesure avant de la commenter. Le bloc 22 a publié « 25 %
d'écart » et « corrélations ≥ 0,9979 » sur quatre positions : les deux chiffres
étaient vrais et tous les deux trompeurs. Le même protocole sur 63 positions donne
6,4 % et une corrélation **minimale** de 0,955 — la conclusion change de nature.

**Garder (2).** Un critère qui échoue doit être un **code retour**, pas une phrase
dans un rapport. `--porte` transforme une intention en porte ; le test adverse
(`--abits 8`) prouve qu'elle mord.

**Changer.** J'ai lancé une passe de 1 024 jetons **sans avoir mesuré le coût par
jeton au contexte visé** : 25 minutes perdues, et la découverte d'un facteur 300
par accident plutôt que par plan. La règle du dépôt (« mesurer avant de conclure »)
doit s'étendre à « **mesurer avant de lancer** » : une passe de 4 jetons au contexte
visé coûte une minute et donne le budget. C'est écrit dans le plan (P6) et dans
`REPRISE.md`.

**Changer (2).** `--dense` : je l'ai utilisé pendant deux blocs en croyant qu'il
alignait la comparaison sur llama.cpp. Il ne change **rien** pour V4-Flash. Le
drapeau n'est pas faux, il est sans objet ici — et cela méritait une mesure, pas une
supposition. Un compteur (« dont en listes : 0,0 M ») l'a dit en une ligne.

**Doute.** Le seuil de 0,95 sur la corrélation **minimale** est un premier choix,
calé sur une seule mesure (0,955 à ctx 256, 0,9959 sur Qwen). Il est probablement
trop serré pour des contextes longs — où la divergence de position s'accumule — et
trop lâche pour un petit modèle. Le seuil devra être **révisé avec des mesures**,
pas ajusté pour faire passer la porte : c'est le genre de réglage qui transforme une
porte en décoration.

**Doute (2).** La comparaison à ctx 256 reste une fenêtre **froide au début** : les
premiers jetons sont notés sans contexte. Le diagnostic par tranches est là pour
montrer si l'écart croît avec la position — s'il croît, la porte longue ne dit pas
seulement « le moteur est fidèle », elle dit **où** il cesse de l'être.
