# Cache du chunker — validation indépendante : ×11,0 à 160 tokens, égalité 612/612

> **Date** : 2026-11-05 · **Instantané mesuré** : `git show HEAD:tools/bloc_linguistique.py`,
> sha256 `6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65` — celui de la fiche
> [`rapport-cout-chunker.md`](rapport-cout-chunker.md) · **Verdict** : ✅ **le cache est validé**.
> Le O(n²) du chemin chunker est confirmé (1+2·S appels : 97/193/769 à 160/320/1 280 tokens ;
> pente 1,71-2,00). La mémoïsation seule de `_syntagmes_simple` donne **×1,24 sur le corpus et
> ×5,1/×6,9 à 160/320** ; le cache complet de la fiche (chunking + verbes de GV) donne **×11,0 à
> 160** (re-mesure ×12,2 ; fiche ×11,6), **×18,1-19,5 à 320**, et **×2,06/×2,61** sur le défaut.
> Égalité stricte : **612/612** sur les deux chemins et **42/42** sur 7 longueurs × 2 chemins ;
> le comparateur est sensible (cache falsifié : 113/612 et 290/612). Le patch hoisté complet,
> appliqué à une copie, fait **1 seul chunking par analyse** et rend **612/612 + 14/14**.
> La fiche ×11,6 est confirmée à ±10 % près ; le cache ne linéarise pas (pente 1,42-1,52).
>
> **Dispositif** : banc hors dépôt (`/tmp/bench_cache_chunker.py`, sha256 `15c4506c…`), sous-classe
> locale `C1`/`C2`/`OFF`, 612 phrases de `evaluer_gold.charger()`, textes de 20 à 1 280 tokens,
> 9 à 15 passes ; JSON [`pensee-cache-chunker.json`](pensee-cache-chunker.json). **Aucun fichier
> existant n'a été modifié ; deux fichiers neufs, non committés.**

## 1. Ce qui est validé

| affirmation de la fiche | mesure indépendante | verdict |
|---|---|---|
| O(n²) chunker : 1+2·S appels | 97/193/769 = 1+2×48/96/384 ; pente 1,71-2,00 ; doublement 160→320 ×3,68 (re-mesure) | confirmé |
| cache ×11,6 à 160 | ×11,0 (9 passes) à ×12,2 (15 passes) ; C2 5,25-5,61 ms contre 5,58 dans la fiche | confirmé à ±10 % |
| cache ×16,9 à 320 | ×18,1-19,5 ; C2 12,0-13,9 ms contre 14,1 | confirmé |
| défaut ×2,0 / ×2,4 | ×1,91-2,06 / ×2,61-2,83 | confirmé |
| corpus ×1,18-1,22 / ×0,97-1,07 | ×1,25 / ×1,03 | confirmé |
| égalité 612/612 + 10/10 | 612/612 + 42/42 (et patch réel 612/612 + 14/14) | confirmé |
| le cache ne linéarise pas | pente C2 1,42 (chunker) / 1,52 (défaut) sur 160-1 280 | confirmé |

Une nuance de lecture, que la fiche dit dans son § 6 mais que son titre masque : **le ×11,6 n'est
pas le gain de la seule mémoïsation de `_syntagmes_simple`**. C1 (chunking seul) donne ×5,1 à
160 tokens ; il faut le cache des verbes de GV (C2) pour atteindre ×11. Les deux composantes sont
mesurées séparément ci-dessous : c'est la seule réserve de fond, et elle est conforme au
pseudo-code de la fiche (V1 → V2).

## 2. Protocole

### 2.1 Instantané et dérive de l'arbre

Le fichier mesuré est le snapshot `6e8430…`, figé par `git show HEAD:tools/bloc_linguistique.py`
au début de la session (HEAD était alors `de292c7d`), et non l'arbre de travail. Pendant la
session, un autre agent a patché `tools/bloc_linguistique.py` dans l'arbre (`6e8430…` →
`e568c9…`), puis l'a committé ; HEAD a successivement valu `2e08cbc7`, `de292c7d`, `a2def5ee`,
`a914c1e7`, `5640809e`, puis au-delà. Toutes les mesures et tous les numéros de ligne portent donc sur
`6e8430…`, l'instantané de la fiche. Le fichier mesuré n'a pas été modifié par cette mission ; il
a été copié dans `/tmp/bloc_linguistique_snapshot.py` (même sha256).

Ce point compte pour deux raisons : (a) les mesures sont reproductibles sur un contenu figé, pas
sur un arbre mouvant ; (b) le patch committé (`5640809e`) n'est **pas** le correctif complet de la
fiche — il en manque la hoist du chemin par défaut (voir § 8.3).

### 2.2 Corpus

`evaluer_gold.charger()` : **612 phrases** = 20 « hand » + 432 réelles + 160 synthétiques,
**402 fr / 210 en**, **3 179 mots gold**, **3 749 tokens `_mots`**, **16 371 caractères**,
**6,13 tokens `_mots`/phrase** (5,19 mots gold), **1,106 segment simple** et **0,186 GV** par
phrase en moyenne. Le générateur S répond pour **612/612** phrases : le chemin par défaut est
réellement exercé, pas un repli sur le chunker.

### 2.3 Textes longs

Base de 10 tokens `« Le chat de la voisine est sur le toit. »` répétée 2/4/8/16/32/64/128 fois,
soit **20/40/80/160/320/640/1 280 tokens** exacts (76/152/304/608/1 216/2 432/4 864 caractères
avec cette base sans séparateur ; la fiche insère un espace entre chaque répétition, d'où rep−1
caractères de plus). Segments simples : 6/12/24/48/96/192/384 ; GV simples : 2/4/8/16/32/64/128 ;
segments S : 8/16/32/64/128/256/512. Les structures sont identiques à celles de la fiche ; seul
le caractère séparateur diffère, ce qui ne change ni les tokens ni les segments.

### 2.4 Les trois variantes

Toutes sont des **sous-classes locales** de `Heuristique`, dans le banc :

- **C1** : `_syntagmes_simple(texte, langue)` mémoïsé par couple `(texte, langue)`, dans un dict
  créé au début de `analyser` et jeté à la fin. C'est la mémoïsation demandée.
- **C2** : C1 + `_verbe_gv`, le verbe de chaque GV calculé une fois par analyse (clé
  `(debut, fin)`). `_cible_proche` et `_verbes_proches` sont recopiés à l'identique, seul l'appel
  au verbe passe par le cache. C'est le correctif complet de la fiche.
- **OFF** : la même sous-classe que C2, avec les deux caches désactivés (compteurs conservés) —
  le contrôle négatif.

Le cache de C1 conserve les **appels** (1+2·S) mais n'en calcule qu'un par analyse ; C2 fait de
même pour les verbes. C'est volontairement une **borne basse** du patch hoisté : elle mesure le
gain du cache sans supprimer les appels ni les listes reconstruites par segment. Le patch réel est
mesuré à part (§ 8.2).

### 2.5 Temps

`time.process_time()` (CPU), variantes **entrelacées** (l'ordre tourne à chaque passe), 2 passes de
chauffe puis **médiane**. Corpus : 9 passes (11 pour la re-mesure du contrôle OFF). Longueurs
20-320 : 9 passes ; 640-1 280 : 3 passes ; re-mesure ciblée 15 passes pour les points 160/320 et
défaut 80/160/320. La machine est un Xeon E5-2687W v3 partagé (40 threads, charge 13-14) ; les
ratios sont plus robustes que les temps absolus, et les temps des variantes cachées sont stables
à quelques pour cent.

### 2.6 Égalité

Chaque sortie est comparée via `Annotation.json()`, donc **tous les champs sérialisés** :
niveau, type, valeur, `debut`/`fin`, source, confiance, candidats, langue, script, `meta` (dont
`attachement`), unités sémantiques, fraction, trace, refus, contexte. Seul `cout.duree_s` est
écarté : il mesure le temps, pas l'analyse. La comparaison porte sur les 612 phrases × 2 chemins
(chunker seul et défaut), et sur les 7 longueurs × 2 chemins.

### 2.7 Contrôles négatifs

1. **OFF** : même code, caches coupés ; il doit suivre l'original, pas le cache.
2. **Cache falsifié** : une sous-classe retire le dernier segment du résultat mémoïsé ; le
   comparateur doit le voir (test de sensibilité du test).
3. **Portée** : deux analyses successives du même texte doivent recalculer une fois chacune
   (`simple_calc = 1` à chaque analyse), preuve qu'il n'y a pas d'état entre analyses.
4. **Disponibilité de S** : 612/612, pour que le chemin par défaut soit réel.

## 3. Temps mesurés

### 3.1 Les 612 phrases du corpus

| variante | chunker (ms) | gain | µs/phrase | défaut (ms) | gain | µs/phrase |
|---|---:|---:|---:|---:|---:|---:|
| original | 245,3 | ×1,000 | 400,8 | 395,2 | ×1,000 | 645,8 |
| C1 (chunking seul) | 198,0 | ×1,239 | 323,6 | 388,3 | ×1,018 | 634,5 |
| C2 (chunking + verbes) | 196,1 | ×1,251 | 320,4 | 385,1 | ×1,026 | 629,2 |
| OFF (caches off) | 275,6 | ×0,890 | 450,4 | 398,4 | ×0,992 | 650,9 |

Mesure principale, 9 passes (médianes). Le point OFF chunker (×0,89) est un **outlier de charge** :
la re-mesure à 11 passes donne OFF 236,5 ms contre original 229,7 ms, soit ×0,97 (voir § 7). Les
trois autres variantes sont stables : C2 196,1 ms contre 196,6 dans la fiche, C1 198,0 contre 193,3,
original 245,3 contre 231,4.

Sur le corpus, le gain est **×1,24-1,25 en chunker** et **×1,02-1,03 en défaut** : les phrases font
6,1 tokens, le terme quadratique n'a pas le temps de mordre. C'est conforme à la fiche
(×1,18-1,22 / ×0,97-1,07), avec un corpus chunker un peu au-dessus.

### 3.2 Phrases longues — chemin chunker seul (`segmenter_s=False`)

| N | S | G | original | C1 | C2 | OFF | gain C1 | gain C2 | gain OFF |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 20 | 6 | 2 | 1,64 | 0,88 | 0,71 | 1,67 | ×1,88 | ×2,32 | ×0,98 |
| 40 | 12 | 4 | 4,97 | 2,38 | 1,40 | 4,99 | ×2,09 | ×3,55 | ×1,00 |
| 80 | 24 | 8 | 16,19 | 4,26 | 2,50 | 16,44 | ×3,80 | ×6,46 | ×0,99 |
| 160 | 48 | 16 | 57,74 | 11,27 | 5,25 | 62,02 | ×5,12 | ×11,00 | ×0,93 |
| 320 | 96 | 32 | 233,47 | 33,80 | 12,00 | 241,33 | ×6,91 | ×19,46 | ×0,97 |
| 640 | 192 | 64 | 925,09 | 119,60 | 31,70 | 919,54 | ×7,74 | ×29,18 | ×1,01 |
| 1280 | 384 | 128 | 3740,44 | 426,46 | 100,93 | 3657,45 | ×8,77 | ×37,06 | ×1,02 |

### 3.3 Phrases longues — chemin par défaut (générateur S)

| N | S | G | original | C1 | C2 | OFF | gain C1 | gain C2 | gain OFF |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 20 | 6 | 2 | 2,02 | 1,95 | 1,60 | 2,03 | ×1,03 | ×1,26 | ×0,99 |
| 40 | 12 | 4 | 4,04 | 3,90 | 2,92 | 4,10 | ×1,04 | ×1,39 | ×0,99 |
| 80 | 24 | 8 | 14,88 | 12,54 | 6,03 | 14,09 | ×1,19 | ×2,47 | ×1,06 |
| 160 | 48 | 16 | 27,88 | 27,27 | 13,55 | 30,76 | ×1,02 | ×2,06 | ×0,91 |
| 320 | 96 | 32 | 91,33 | 89,07 | 35,04 | 90,22 | ×1,03 | ×2,61 | ×1,01 |
| 640 | 192 | 64 | 344,96 | 321,58 | 103,40 | 317,65 | ×1,07 | ×3,34 | ×1,09 |
| 1280 | 384 | 128 | 1161,80 | 1164,81 | 318,29 | 1188,64 | ×1,00 | ×3,65 | ×0,98 |

Le point défaut 80 de la série 9 passes (original 14,88 ms, gain ×2,47) est un outlier : la
re-mesure à 15 passes donne original 10,59 ms, C2 6,39 ms, gain **×1,66**, exactement la fiche
(×1,63). Les autres points sont cohérents.

### 3.4 Re-mesure ciblée (15 passes)

| point | original | C1 | C2 | OFF | gain C1 | gain C2 | gain OFF |
|---|---:|---:|---:|---:|---:|---:|---:|
| chunker 160 | 68,31 | 13,04 | 5,61 | 65,38 | ×5,24 | ×12,17 | ×1,04 |
| chunker 320 | 251,12 | 37,95 | 13,85 | 254,06 | ×6,62 | ×18,13 | ×0,99 |
| défaut 80 | 10,59 | 10,36 | 6,39 | 10,79 | ×1,02 | ×1,66 | ×0,98 |
| défaut 160 | 32,96 | 31,80 | 17,27 | 32,90 | ×1,04 | ×1,91 | ×1,00 |
| défaut 320 | 98,61 | 98,37 | 34,82 | 101,26 | ×1,00 | ×2,83 | ×0,97 |

La lecture est celle de la fiche : **le temps caché est stable, la ligne de base original varie**.
À 160 tokens chunker, C2 vaut 5,25 ms (9 p.) et 5,61 ms (15 p.) contre 5,58 dans la fiche ; mais
l'original vaut 57,7 ou 68,3 ms selon la passe, d'où un gain de ×11,0 à ×12,2. À 320, C2 vaut
12,0-13,9 ms contre 14,1 dans la fiche. Sur le défaut 160, C2 vaut 13,6-17,3 ms contre 13,9. La
conclusion ne doit donc pas être lue comme un facteur unique : **×11,6 est dans l'intervalle, pas
une constante**.

## 4. Complexité empirique

Ajustement log-log `temps = a · N^p` sur les points mesurés (R² indiqué) :

| chemin | variante | 20-160 | R² | 20-320 | R² | 160-1 280 | R² |
|---|---|---:|---:|---:|---:|---:|---:|
| chunker | original | 1,711 | 0,9991 | 1,784 | 0,9979 | 2,004 | 1,0000 |
| chunker | C1 | 1,190 | 0,9904 | 1,279 | 0,9911 | 1,755 | 0,9988 |
| chunker | C2 | 0,951 | 0,9981 | 1,007 | 0,9960 | 1,420 | 0,9943 |
| chunker | OFF | 1,736 | 0,9981 | 1,798 | 0,9979 | 1,958 | 1,0000 |
| défaut | original | 1,325 | 0,9806 | 1,379 | 0,9895 | 1,806 | 0,9996 |
| défaut | C1 | 1,309 | 0,9906 | 1,383 | 0,9930 | 1,810 | 0,9996 |
| défaut | C2 | 1,029 | 0,9957 | 1,112 | 0,9926 | 1,522 | 0,9986 |
| défaut | OFF | 1,353 | 0,9887 | 1,385 | 0,9941 | 1,763 | 0,9979 |

Trois lectures :

1. **Le O(n²) est confirmé.** Sur le chunker, la pente 20-160 vaut 1,71 et 20-320 1,78 ; sur
   160-1 280 elle monte à **2,00**. Le doublement 160→320 coûte ×4,04 dans la série 9 passes,
   **×3,68** dans la re-mesure 15 passes — la fiche donnait ×3,67. Les appels sont exactement
   1+2·S : 97 à 160 (S=48), 193 à 320 (S=96), 769 à 1 280 (S=384).
2. **Le cache divise, mais ne linéarise pas.** C1 fait tomber la pente 20-160 à 1,19 ; C2 à 0,95
   (20-160) puis **1,42 sur 160-1 280**. Le doublement 160→320 de C2 coûte ×2,29-2,47, pas ×2 :
   le `sorted(gvs, key=ecart)` par segment reste, en O(S·G log G), comme le dit la fiche. La pente
   C2 mesurée (1,42/1,52) est presque celle de la fiche (1,44/1,55).
3. **OFF suit l'original** (pente 1,74-1,80 en chunker, 1,35-1,76 en défaut) : la chute de pente
   observée avec C2 vient bien du cache, pas d'un changement de chemin de mesure.

## 5. Égalité des annotations

| comparaison | chunker seul | défaut S |
|---|---|---|
| C1 (chunking mémoïsé) | **612/612** | **612/612** |
| C2 (chunking + verbes) | **612/612** | **612/612** |
| OFF (caches off) | **612/612** | **612/612** |
| Cache falsifié (contrôle) | 113/612 | 290/612 |

- **Longueurs** : C1, C2 et OFF donnent **42/42** (7 longueurs × 2 chemins × 3 variantes).
- **Patch réel** : **612/612** sur les deux chemins et **14/14** sur les longueurs (§ 8.2).
- **Comparateur** : le cache falsifié (dernier segment retiré) n'est égal que 113 fois sur 612 en
  chunker et 290 fois en défaut ; les champs divergents sont `etiquettes`, `cout` et `trace`. Le
  test n'est donc pas vide : il détecte une altération de la sortie du chunker.
- **Portée** : deux analyses successives de `« Le chat dort. »` donnent chacune
  `simple_calc = 1`, `simple_hits = 2` — le cache est bien recréé à chaque `analyser`, aucun état
  d'instance ne survit.

La comparaison couvre les étiquettes, les spans, les cibles (`meta.attachement`), les candidats,
les unités sémantiques et la trace. Aucune divergence n'a été trouvée entre C1/C2/OFF et
l'original sur les 612 phrases, ni sur les textes longs.

## 6. Le chemin par défaut : le cache y change-t-il quelque chose ?

**Oui, mais pas celui qu'on croit.** Le générateur S répond pour 612/612 phrases. Sur ce chemin,
`_syntagmes_simple` est appelé **2 fois par phrase** (1224 appels corpus) : une fois pour les GV
qui complètent S, une fois pour l'union. Le re-chunking dans la boucle (1+2·S) est du **code
mort** ici : la boucle itère sur les segments de S, pas sur ceux du chunker.

- **Cache de chunking seul (C1)** : 1224 appels, 612 misses, 612 hits ; le temps passe de 395,2 à
  388,3 ms sur le corpus (×1,018) et gagne ×1,00-1,07 sur les longues (2 appels → 1). C'est
  réel mais marginal.
- **Cache complet (C2)** : ×1,026 sur le corpus, ×1,26-3,65 sur les longues ; **×2,06 à 160**,
  **×2,61 à 320**, plateau ×3,3-3,7. Tout le gain vient du cache des verbes de GV : à 160 tokens,
  2 289 appels à `_verbe_dans` pour 32 GV distincts (défaut), ramenés à 32 misses ; à 320,
  8 673 appels pour 64 GV, ramenés à 64.

Autrement dit : **le cache de chunking ne change presque rien au chemin par défaut** ; c'est le
cache des verbes de GV, seconde moitié du correctif de la fiche, qui le change. Si l'on n'applique
que la mémoïsation de `_syntagmes_simple`, le défaut reste à ×1,02-1,07.

Les compteurs le confirment (une analyse par point ; `misses` = calculs réels). La colonne
`_verbe_gv` compte les appels passés par le cache (les GV des listes) ; les appels **directs** à
`_verbe_dans` des lignes 883 et 891 (31/63/255 selon N sur le défaut) ne sont pas dans ce compteur.
C1 n'utilise pas `_verbe_gv` (il hérite des helpers d'origine) : ses appels sont ceux de
l'original, non comptés ici.

| point | variante | `_syntagmes_simple` | misses | `_verbe_gv` | misses |
|---|---|---:|---:|---:|---:|
| chunker 160 | original | 97 | 97 | 640 | 640 |
| chunker 160 | C1 | 97 | 1 | — | — |
| chunker 160 | C2 | 97 | 1 | 640 | 16 |
| chunker 160 | OFF | 97 | 97 | 640 | 640 |
| défaut 160 | original | 2 | 2 | 2289 | 2289 |
| défaut 160 | C1 | 2 | 1 | — | — |
| défaut 160 | C2 | 2 | 1 | 2289 | 32 |
| défaut 160 | OFF | 2 | 2 | 2289 | 2289 |
| chunker 320 | original | 193 | 193 | 2304 | 2304 |
| chunker 320 | C1 | 193 | 1 | — | — |
| chunker 320 | C2 | 193 | 1 | 2304 | 32 |
| chunker 320 | OFF | 193 | 193 | 2304 | 2304 |
| défaut 320 | original | 2 | 2 | 8673 | 8673 |
| défaut 320 | C1 | 2 | 1 | — | — |
| défaut 320 | C2 | 2 | 1 | 8673 | 64 |
| défaut 320 | OFF | 2 | 2 | 8673 | 8673 |
| chunker 1280 | original | 769 | 769 | 33792 | 33792 |
| chunker 1280 | C1 | 769 | 1 | — | — |
| chunker 1280 | C2 | 769 | 1 | 33792 | 128 |
| chunker 1280 | OFF | 769 | 769 | 33792 | 33792 |
| défaut 1280 | original | 2 | 2 | 132993 | 132993 |
| défaut 1280 | C1 | 2 | 1 | — | — |
| défaut 1280 | C2 | 2 | 1 | 132993 | 256 |
| défaut 1280 | OFF | 2 | 2 | 132993 | 132993 |

## 7. Contrôles négatifs

- **OFF vs original, corpus chunker** : 275,6 ms contre 245,3 ms dans la série 9 passes (×0,89),
  mais **236,5 ms contre 229,7 ms** dans la re-mesure 11 passes (×0,97) ; l'écart de la première
  série est un épisode de charge. Le résidu +3-5 % est le surcoût des frames Python de la
  sous-classe (deux `analyser` imbriqués, appels à `_verbe_gv`), pas un effet de cache.
- **OFF vs original, longueurs** : ratios ×0,91 à ×1,09 (chunker et défaut), médiane proche de
  1,00. OFF ne montre **jamais** le gain de C2 (×2,3 à ×37 selon le point).
- **OFF, égalité** : 612/612 sur les deux chemins ; C1OFF et C2OFF revérifiés 612/612.
- **Cache falsifié** : 113/612 et 290/612 ; le comparateur voit l'altération.
- **Portée** : un miss par analyse, deux analyses du même texte = deux misses.
- **S disponible** : 612/612 ; le chemin par défaut n'est pas un repli.

Le contrôle OFF est le plus important : c'est le **même code de sous-classe**, avec les mêmes
méthodes réécrites, mais sans hits de cache. Il redonne les temps de l'original à ±10 % et ne
reproduit jamais le gain. Le gain n'est donc ni un changement d'algorithme déguisé, ni un artefact
de la mesure.

## 8. Correctif exact à appliquer

### 8.1 Les éditions, sur l'instantané `6e8430…`

**Fichier** : [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) · **fonction** :
`Heuristique.analyser` · **lignes** : 853-941 (section 5), helpers 642-658, 661-685, 688-704.
Aucun état d'instance, aucun changement de signature obligatoire, aucune modification de sortie.

| ligne | édition |
|---|---|
| 855 (après) | insérer `simples = self._syntagmes_simple(texte, lg)`, `gvs_simple = [...]`, `cache_gv: dict = {}` |
| 861 | supprimer `gvs_simple = [x for x in self._syntagmes_simple(...) ...]` (déjà hoisté) |
| 887, 895 | `_cible_proche(texte, s, gvs, verbes)` → ajouter `cache_gv=cache_gv` |
| 899 | `_verbes_proches(texte, s, gvs, verbes=verbes)` → ajouter `cache_gv=cache_gv` |
| 914 | `for s in self._syntagmes_simple(texte, lg):` → `for s in simples:` |
| 916 | liste de GV recalculée → `gvs_simple`, et ajouter `cache_gv=cache_gv` |
| 919 | supprimer `gvs_s = [x for x in self._syntagmes_simple(...) ...]` ; utiliser `gvs_simple` |
| 922 | `gvs_s` → `gvs_simple`, et ajouter `cache_gv=cache_gv` |
| 928 | supprimer `simples = self._syntagmes_simple(texte, lg)` (déjà hoisté) |
| 929-930 | `gvs_u = gvs_s + gvs_simple` (même concaténation, sans re-filtrer `simples`) |
| 935, 940 | ajouter `cache_gv=cache_gv` |
| 658 (après) | insérer le helper `_verbe_gv` ci-dessous |
| 662, 689 | ajouter un paramètre `cache_gv` (défaut `None`) à la signature de `_cible_proche` / `_verbes_proches` |
| 681, 685, 701 | `Heuristique._verbe_dans(...)` → `Heuristique._verbe_gv(texte, g, verbes, cache_gv)` |

Le helper, copié de la fiche :

```python
@staticmethod
def _verbe_gv(texte: str, g: dict, verbes, cache_gv: dict | None = None):
    """Le verbe d'un GV, calculé **une fois par analyse** (clé valide dans un seul texte)."""
    if cache_gv is None:
        return Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
    cle = (g["debut"], g["fin"])
    if cle not in cache_gv:
        cache_gv[cle] = Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
    return cache_gv[cle]
```

Le fallback `cache_gv is None` garde la compatibilité des appels hors `analyser` (`MockNeuronal`,
tests, outils). La clé `(debut, fin)` n'est valide que dans un appel d'`analyser` (texte et
`verbes` constants) : créer le dict localement, ne pas le promouvoir en attribut d'instance.

### 8.2 Diff complet et validation du patch réel

Le correctif a été appliqué à une **copie /tmp** (`/tmp/bloc_linguistique_patche.py`, sha256
`5639a376…`), jamais au dépôt. Le diff source (sha256 `01c27afd…`) est reproduit ci-dessous avec
les en-têtes `a/`/`b/` ; il contient exactement les éditions du tableau et rien d'autre.

```diff
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -658,8 +658,19 @@
         return None if strict else (mots[-1][1] if mots else None)
 
     @staticmethod
+    def _verbe_gv(texte: str, g: dict, verbes, cache_gv: dict | None = None):
+        """Le verbe d'un GV, calculé **une fois par analyse** (clé valide dans un seul texte)."""
+        if cache_gv is None:
+            return Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
+        cle = (g["debut"], g["fin"])
+        if cle not in cache_gv:
+            cache_gv[cle] = Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
+        return cache_gv[cle]
+
+    @staticmethod
     def _cible_proche(texte: str, segment: dict, gvs: list[dict],
-                      verbes: list[tuple[int, int, str]] | None = None) -> str | None:
+                      verbes: list[tuple[int, int, str]] | None = None,
+                      cache_gv: dict | None = None) -> str | None:
         """La cible d'un segment : le **verbe du GV le plus proche** (règle de proximité).
 
         Rend `None` si le segment est lui-même un GV ou s'il n'y a pas de GV. Le verbe est le
@@ -678,15 +689,16 @@
         # un GV réduit à l'auxiliaire (« a », « est ») ne donne pas la cible : on prend le
         # premier GV proche dont le verbe est **plein** (mesuré : « a » au lieu de « vu »).
         for g in sorted(gvs, key=ecart):
-            v = Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
+            v = Heuristique._verbe_gv(texte, g, verbes, cache_gv)
             if v and _normaliser(v) not in AUXILIAIRES:
                 return v
         g = min(gvs, key=ecart)
-        return Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
+        return Heuristique._verbe_gv(texte, g, verbes, cache_gv)
 
     @staticmethod
     def _verbes_proches(texte: str, segment: dict, gvs: list[dict],
-                        k: int = 3, verbes: list[tuple[int, int, str]] | None = None) -> list[str]:
+                        k: int = 3, verbes: list[tuple[int, int, str]] | None = None,
+                        cache_gv: dict | None = None) -> list[str]:
         """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
         if segment.get("type") == "GV" or not gvs:
             return []
@@ -698,7 +710,7 @@
             return 0
         proches: list[str] = []
         for g in sorted(gvs, key=ecart)[:k]:
-            v = Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
+            v = Heuristique._verbe_gv(texte, g, verbes, cache_gv)
             if v and v not in proches:
                 proches.append(v)
         return proches
@@ -853,12 +865,16 @@
         # 5. syntagmes : le générateur S (candidats) ou un chunker simple
         verbes = [(e.debut, e.fin, e.valeur) for e in etiquettes
                   if e.niveau == "pos" and e.type == "VERB"]
+        # (A) un seul chunking par analyse, (B) une seule extraction des GV,
+        # (C) cache local des verbes de GV — durée de CET appel d'analyser.
+        simples = self._syntagmes_simple(texte, lg)
+        gvs_simple = [x for x in simples if x["type"] == "GV"]
+        cache_gv: dict = {}
         cands = self._syntagmes_s(texte)
         cibles_s = self._cibles_s(texte) if cands else {}
         if cands:
             # les GV du chunker complètent ceux du générateur S : sans eux, un GP n'a aucun
             # candidat d'attachement (diagnostic des 33 échecs de T162).
-            gvs_simple = [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"]
             for c in cands[:1]:
                 noms = [x.get("nom", "") for x in cands]
                 gvs_s = [x for x in c.get("segments", []) if x.get("type") == "GV"]
@@ -884,7 +900,7 @@
                             elif g.get("type") == "GN":
                                 cible = self._tete_nom(texte, g["debut"], g["fin"])
                     if not cible and s.get("type") == "GP":
-                        cible = self._cible_proche(texte, s, gvs, verbes)
+                        cible = self._cible_proche(texte, s, gvs, verbes, cache_gv)
                     if not cible and brute:
                         i = texte.find(brute)
                         if i >= 0:
@@ -892,11 +908,12 @@
                     if cible and _normaliser(cible) in AUXILIAIRES:
                         cible = None  # « a » / « est » ne sont pas des cibles
                     if not cible:
-                        cible = self._cible_proche(texte, s, gvs, verbes)
+                        cible = self._cible_proche(texte, s, gvs, verbes, cache_gv)
                     meta = {"role": s.get("role", ""), "niveau": s.get("niveau", 0)}
                     if cible:
                         meta["attachement"] = {"segment": s.get("texte", ""), "cible": cible}
-                    candidats = list(noms) + self._verbes_proches(texte, s, gvs, verbes=verbes)
+                    candidats = list(noms) + self._verbes_proches(texte, s, gvs, verbes=verbes,
+                                                          cache_gv=cache_gv)
                     # la **tête** de chaque candidat S (« « … » → Le livre » → livre ; « … → Les
                     # fleurs poussent » → poussent) : mesuré +45 segments au top-k strict.
                     for nom in noms:
@@ -911,33 +928,32 @@
                                                 candidats=candidats, langue=lg, script=script,
                                                 meta=meta))
         else:
-            for s in self._syntagmes_simple(texte, lg):
+            for s in simples:
                 meta = {"role": s["role"], "niveau": s["niveau"]}
-                cible = self._cible_proche(texte, s, [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"], verbes)
+                cible = self._cible_proche(texte, s, gvs_simple, verbes, cache_gv)
                 if cible:
                     meta["attachement"] = {"segment": s["texte"], "cible": cible}
-                gvs_s = [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"]
                 etiquettes.append(Etiquette("syntagme", s["type"], s["texte"], s["debut"],
                                             s["fin"], self.nom, 0.35,
-                                            candidats=[s["type"]] + self._verbes_proches(texte, s, gvs_s, verbes=verbes),
+                                            candidats=[s["type"]] + self._verbes_proches(texte, s, gvs_simple,
+                                                                verbes=verbes, cache_gv=cache_gv),
                                             langue=lg, script=script, meta=meta))
         # 5 bis. union : les segments du chunker que le générateur S ne fournit pas
         if cands and self.union:
             deja = {(s.get("type"), s.get("debut"), s.get("fin"))
                     for s in cands[0].get("segments", [])}
-            simples = self._syntagmes_simple(texte, lg)
-            gvs_u = ([x for x in cands[0].get("segments", []) if x.get("type") == "GV"]
-                     + [x for x in simples if x["type"] == "GV"])
+            gvs_u = gvs_s + gvs_simple
             for s in simples:
                 if (s["type"], s["debut"], s["fin"]) in deja:
                     continue
                 meta = {"role": s["role"], "niveau": s["niveau"], "union": True}
-                cible = self._cible_proche(texte, s, gvs_u, verbes)
+                cible = self._cible_proche(texte, s, gvs_u, verbes, cache_gv)
                 if cible:
                     meta["attachement"] = {"segment": s["texte"], "cible": cible}
                 etiquettes.append(Etiquette("syntagme", s["type"], s["texte"], s["debut"],
                                             s["fin"], self.nom, 0.30,
-                                            candidats=[s["type"]] + self._verbes_proches(texte, s, gvs_u, verbes=verbes),
+                                            candidats=[s["type"]] + self._verbes_proches(texte, s, gvs_u,
+                                                                verbes=verbes, cache_gv=cache_gv),
                                             langue=lg, script=script, meta=meta))
     
         # 6. discours / document
```

**Validation du patch réel** (même protocole, module patché importé à côté du snapshot) :

- **Égalité** : 612/612 sur les deux chemins et 14/14 sur les 7 longueurs × 2 chemins.
- **Compteurs** : `_syntagmes_simple` = **1** par analyse partout (chunker 160/320/1 280, défaut
  160/320/1 280) ; `_verbe_dans` sur GV = **16/32/128** (chunker) et **63/127/511** (défaut, dont
  les appels directs des lignes 883 et 891 : 32+31, 64+63, 256+255).
- **Temps cachés** : 5,15 ms à 160 chunker (C2 : 5,25 ; fiche : 5,58), 13,18 ms à 320 (C2 : 12,00 ;
  fiche : 14,10), 13,45 ms à 160 défaut (C2 : 13,55 ; fiche : 13,94). Les ratios du patch
  (×12,86 et ×20,19) sont gonflés par une ligne de base original plus lente dans cette passe
  (66,2 ms à 160, 266,2 ms à 320) ; lire les temps, pas les ratios.
- **Conclusion** : le patch hoisté est **au niveau de C2** (5,15 contre 5,25 ms à 160 ; 13,18 contre
  12,00 à 320 — l'écart est dans le bruit) et supprime le terme 1+2·S. C2 reste une borne basse
  **en nombre d'opérations**, pas une garantie de temps à chaque passe.

### 8.3 Note sur le patch déjà committé (`5640809e`)

Au moment de la rédaction, HEAD contient un patch **partiel** : `_verbe_gv` et le cache des verbes
sont là, la branche chunker est hoistée, mais le chemin par défaut garde **deux** chunkings —
`gvs_simple` est calculé dans la branche `cands` (ligne 875 de HEAD) et `simples` dans l'union
(ligne 947). Le correctif complet ci-dessus les ramène à **un**. Le gain défaut reste acquis (le
cache des verbes en porte l'essentiel), mais le 2→1 manque : environ 2-4 % sur le défaut, pas de
quoi changer le ×2. À appliquer sur `6e8430…` ou à fusionner avec ce patch partiel.

## 9. Limites — ce qui pourrait rendre ce résultat faux

- **Base A défavorable.** Le GV `« est sur le toit »` a pour tête l'auxiliaire `« est »` ;
  `_cible_proche` le saute et scanne tous les GV. C'est un cas réel (copules), mais il amplifie le
  coût et le gain défaut. Avec la base B à verbe plein, la fiche mesure ×1,07-1,13 : ne pas lire
  ×2,0 comme universel.
- **Corpus court.** 6,13 tokens `_mots`/phrase, 1,11 segment, 0,19 GV : le O(n²) ne mord pas. Le
  gain corpus est ×1,24-1,25 (chunker) et ×1,03 (défaut), pas le gain long.
- **Bruit de mesure.** Xeon partagé, charge 13-14, temps CPU, 9-15 passes. La ligne de base
  original varie de 58 à 68 ms à 160 tokens, d'où un ratio de ×11,0 à ×12,2 alors que le temps
  caché reste 5,2-5,6 ms. Lire les facteurs à ±10-15 % près. Le point OFF corpus de la première
  série (×0,89) et le point défaut 80 (×2,47) sont des outliers explicitement re-mesurés.
- **Le cache seul ne linéarise pas.** Pente C2 1,42 (chunker) / 1,52 (défaut) sur 160-1 280 ; le
  tri `sorted(gvs, key=ecart)` par segment reste. Une vraie linéarité demande l'index pré-trié,
  non retenu par la fiche (V3 : 1 divergence sur 612 ; V4 : plus lent).
- **C2 est une borne basse.** La sous-classe conserve les 1+2·S appels (mémoïsés) et les listes
  reconstruites par segment ; le patch hoisté réel fait 1 appel et 5,15 ms à 160. L'égalité
  612/612 + 14/14 est un contrôle fort, mais le patch doit encore passer les portes du bloc et une
  mesure après commit.
- **Instantané mouvant.** L'arbre a changé pendant la session (`6e8430…` → `e568c9…`) et HEAD a
  bougé (`2e08cbc7` → `de292c7d` → `a2def5ee` → `a914c1e7` → `5640809e`, puis au-delà). Les numéros de ligne du
  correctif sont ceux de `6e8430…` ; une édition ultérieure les invalide. Le patch committé
  `5640809e` n'est pas le correctif complet (§ 8.3).
- **Mesure CPU seulement.** `time.process_time` exclut les I/O et le temps hors CPU ; l'analyse
  est CPU-bound, mais une machine chargée décale les médianes. Pas de mesure GPU.
- **Clé du cache.** `(debut, fin)` n'est valide que dans un appel d'`analyser` ; un cache global
  par instance serait faux si le texte change et risqué si l'instance est partagée entre threads.

## 10. Conclusion

- **Le O(n²) est réel** : 1+2·S appels à `_syntagmes_simple`, 97/193/769 à 160/320/1 280, pente
  1,71-2,00 et doublement 160→320 ×3,68 sur le chemin chunker.
- **Le cache est exact et sûr** : C1, C2 et OFF rendent **612/612** sur les deux chemins,
  **42/42** sur les longueurs, le cache falsifié est détecté, et le cache est recréé à chaque
  analyse (aucun état d'instance). Le patch hoisté complet rend **612/612 + 14/14** et fait
  **1 seul chunking par analyse**.
- **Le facteur ×11,6 de la fiche est confirmé à ±10 %** : ×11,0 (9 passes) à ×12,2 (15 passes) à
  160 tokens, ×18,1-19,5 à 320 ; le temps caché (5,2-5,6 ms à 160) est stable, c'est la ligne de
  base qui varie. En défaut : ×1,91-2,06 à 160, ×2,61-2,83 à 320. Sur le corpus : ×1,25 (chunker)
  et ×1,03 (défaut), pas de gain spectaculaire sur 6 tokens.
- **La mémoïsation seule ne suffit pas** : C1 donne ×5,1 à 160 ; c'est le cache des verbes de GV
  (C2) qui apporte le second facteur ×2. Le correctif de la fiche est bien l'ensemble des deux.
- **Le cache ne linéarise pas** : pente 1,42-1,52 sur 160-1 280, le tri par segment reste. Le
  chantier suivant, si la linéarité devient l'objectif, est l'index pré-trié des GV — avec un
  contrôle d'égalité sur les recouvrements, comme le note la fiche.

**Correctif à appliquer** : hoister `simples`/`gvs_simple` après le calcul de `verbes` (ligne
855), créer `cache_gv` localement, passer `cache_gv` à `_cible_proche`/`_verbes_proches`, ajouter
`_verbe_gv` et remplacer les trois appels directs (681, 685, 701), puis remplacer les sites
861/914/916/919/922/928/929-930/935/940. Le diff complet est au § 8.2 ; la validation 612/612 +
14/14 sur copie est au § 8.2. **Rien n'a été committé.**
