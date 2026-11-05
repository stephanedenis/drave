# Coût des règles d'attachement du chunker — O(n²) réel, cache ×12 à 160 tokens

> **Date** : 2026-11-05 · **Instantané** : [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py)
> sha256 `6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65`, commit
> `9d5337ce` (branche `s/v7` ; le fichier mesuré y est committé ; il était encore modifié
> dans l'arbre au moment du banc) · **Verdict** : ✅ **le O(n²) est confirmé** ;
> le cache « un chunking + un verbe de GV par analyse » divise le temps par
> **11,6 à 160 tokens** et **16,9 à 320** sur le chemin chunker seul, par **2,0 / 2,4** sur le
> chemin par défaut ; **mais** il ne rend pas la complexité strictement linéaire (le tri des GV
> par segment reste) et il ne gagne presque rien sur le corpus court.
>
> **Dispositif** : banc hors dépôt (`/tmp/bench_final.py`, sha256 `6c823a1f…`), 612 phrases de
> [`evaluer_gold.charger()`](../tools/tests/linguistique/evaluer_gold.py), phrases synthétiques
> de 20 à 1 280 tokens, variantes V1/V2/OFF ; JSON
> [`pensee-cout-chunker.json`](pensee-cout-chunker.json). Contexte : la fiche
> [`rapport-bloc-linguistique.md`](rapport-bloc-linguistique.md) décrit le bloc, pas son coût.

## 1. Ce qui était mesuré

Dans `Heuristique.analyser`, la section 5 (lignes 853-941 de l'instantané) a deux chemins.

**Chemin chunker seul** (`segmenter_s=False`, ou repli quand le générateur S ne rend rien) :
la boucle sur les segments rappelle le chunker **à chaque tour** pour reconstruire la liste des
GV.

```python
# lignes 913-923 de l'instantané
for s in self._syntagmes_simple(texte, lg):                       # 914
    cible = self._cible_proche(
        texte, s,
        [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"], verbes)  # 916
    gvs_s = [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"]       # 919
```

Si `S` est le nombre de segments, l'analyse paie **1 + 2·S** chunkings du texte entier. Comme
`S` croît avec la longueur et que chaque chunking est linéaire, le coût est **O(n²)**.

**Chemin par défaut** (générateur S disponible) : `_syntagmes_simple` n'est appelé que **deux
fois** (ligne 861, puis 928 pour l'union). Le re-chunking dans la boucle est du **code mort**
sur ce chemin. Le coût quadratique vient d'ailleurs : `_cible_proche` et `_verbes_proches`
parcourent les GV **pour chaque segment**, et `_verbe_dans` re-scanne le même GV à chaque
appel (lignes 681, 685, 701). C'est la règle d'attachement qui est chère, pas le chunker.

Les deux chemins sont mesurés séparément, parce qu'ils ne disent pas la même chose :

- **V1** : `_syntagmes_simple` mémoïsé par `(texte, langue)` dans une sous-classe locale du
  banc — le « GV calculé une seule fois » minimal ;
- **V2** : V1 + le verbe de chaque GV calculé **une seule fois** par analyse (cache local
  `(debut, fin)`) — c'est le correctif de cache proposé ;
- **OFF** : la même sous-classe, caches désactivés — contrôle négatif.

## 2. Protocole

- **Instantané** : `tools/bloc_linguistique.py` sha256 `6e843018…`, commit `9d5337ce`, branche
  `s/v7`. Le fichier mesuré y est committé ; au moment du banc il était encore modifié dans
  l'arbre, au-dessus de `e1171032` (règles d'attachement récentes, dont `_tete_texte` et
  `_cible_s_par_genre`). Le hash a été **revérifié identique après le banc** et correspond au
  contenu de `HEAD`. Tous les numéros de ligne cités sont ceux de cet instantané.
- **Corpus** : `evaluer_gold.charger()` = 20 « hand » + 432 réelles + 160 synthétiques = **612
  phrases** (402 fr, 210 en), **3 179 mots gold**, **16 371 caractères**, **6,13 tokens
  `_mots`/phrase**, **1,10 segment simple** et **0,186 GV** par phrase en moyenne.
- **Phrases longues** : base de **10 tokens** `« Le chat de la voisine est sur le toit. »`
  répétée 2/4/8/16/32 fois, soit **20/40/80/160/320 tokens** exacts (77/155/311/623/1 247
  caractères). Segments simples : 6/12/24/48/96 ; GV simples : 2/4/8/16/32. Segments S :
  8/16/32/64/128. Deux points de continuité à **640 et 1 280 tokens** (3 passes).
- **Temps** : `time.process_time()` (CPU), 2 passes de chauffe puis médiane. Corpus : 11
  passes ciblées, complétées par 7 passes du banc complet. Longueurs 20-320 : 9 passes
  entrelacées (ordre des variantes tourné à chaque round) ; 640/1 280 : 3 passes.
- **Égalité** : chaque sortie est comparée champ à champ à l'original — niveau, type, valeur,
  span, source, confiance, candidats, langue, script, `meta`, unités sémantiques, fraction,
  trace. V1, V2 et OFF rendent **612/612** sur le corpus et **10/10** sur les textes longs.
- **Banc** : écrit en heredoc dans `/tmp/bench_final.py` (hors dépôt), exécuté par
  `python3 /tmp/bench_final.py` ; durée **82,9 s** ; sortie brute `/tmp/bench_final.json`.
  Aucun fichier existant n'a été modifié **par cette mission** ; les deux fichiers de cette
  fiche sont neufs et **non committés**.

## 3. Temps mesurés

### 3.1 Les 612 phrases du corpus

| variante | chunker seul (ms) | gain | µs/phrase | défaut S (ms) | gain | µs/phrase |
|---|---:|---:|---:|---:|---:|---:|
| original | 231,4 | ×1,000 | 378,1 | 394,4 | ×1,000 | 644,4 |
| V1 (chunking caché) | 193,3 | ×1,197 | 315,8 | 374,2 | ×1,054 | 611,4 |
| **V2 (chunking + verbes)** | **196,6** | **×1,177** | **321,2** | **367,6** | **×1,073** | **600,7** |
| OFF (caches off) | 228,8 | ×1,011 | 373,9 | 393,5 | ×1,002 | 643,0 |

Mesure ciblée 11 passes. Le banc complet (7 passes) donne 230,6 → 189,4 ms (×1,22) en chunker
et 385,1 → 396,0 ms (×0,97) en défaut : les deux passages encadrent le bruit de la machine.
**Le gain corpus est donc faible et variable** — ×1,18-1,22 en chunker, ×0,97-1,07 en
défaut. Les phrases du gold font 6,1 tokens : le terme quadratique n'a pas le temps de mordre.
Sur le corpus chunker, V1 (×1,20) fait même un peu mieux que V2 (×1,18) : le cache des verbes
de GV coûte plus qu'il ne rapporte quand il n'y a que 0,32 appel `_verbe_dans` par phrase.

### 3.2 Phrases longues — chemin chunker seul (`segmenter_s=False`)

| N | S | G | original (ms) | V1 (ms) | gain V1 | V2 (ms) | gain V2 | OFF (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 20 | 6 | 2 | 1,75 | 0,93 | ×1,873 | 0,73 | ×2,402 | 1,75 |
| 40 | 12 | 4 | 5,04 | 1,95 | ×2,583 | 1,31 | ×3,832 | 5,58 |
| 80 | 24 | 8 | 17,29 | 4,51 | ×3,829 | 2,57 | ×6,729 | 16,39 |
| 160 | 48 | 16 | 64,82 | 11,80 | ×5,494 | 5,58 | ×11,615 | 57,61 |
| 320 | 96 | 32 | 238,00 | 34,80 | ×6,840 | 14,10 | ×16,886 | 233,01 |

Les appels réels le confirment : `_syntagmes_simple` est appelé **13/25/49/97/193** fois, soit
exactement **1 + 2·S**. Le cache V2 n'en fait plus qu'**un** par analyse, et calcule
**2/4/8/16/32** verbes de GV au lieu de **20/64/192/640/2 304**. À 160 tokens, 640 appels de
`_verbe_dans` pour 16 GV distincts (×40 de redondance) ; à 320, 2 304 pour 32 (×72).

### 3.3 Phrases longues — chemin par défaut (générateur S)

| N | S_S | G_S | original (ms) | V1 (ms) | gain V1 | V2 (ms) | gain V2 | OFF (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 20 | 8 | 2 | 1,98 | 1,92 | ×1,033 | 1,58 | ×1,258 | 1,99 |
| 40 | 16 | 4 | 4,23 | 4,10 | ×1,032 | 2,99 | ×1,414 | 4,19 |
| 80 | 32 | 8 | 9,89 | 9,62 | ×1,027 | 6,08 | ×1,626 | 9,82 |
| 160 | 64 | 16 | 27,83 | 26,71 | ×1,042 | 13,94 | ×1,996 | 28,41 |
| 320 | 128 | 32 | 88,38 | 89,73 | ×0,985 | 36,88 | ×2,397 | 89,10 |

Ici V1 ne gagne rien (le chunking n'est appelé que 2 fois), et V2 gagne **×2,0 / ×2,4** : tout
le gain vient du cache des verbes de GV. `_verbe_dans` est appelé **66/196/648/2 320/8 736**
fois pour seulement **4/8/16/32/64** GV distincts (×72 à 160 tokens, ×136 à 320). C'est le
vrai terme quadratique du chemin par défaut.

## 4. Complexité empirique

Ajustement log-log `temps = a · N^p` sur les points mesurés (R² indiqué) :

| chemin | variante | pente 20-160 | R² | pente 20-320 | R² | pente 160-1 280 | R² |
|---|---|---:|---:|---:|---:|---:|---:|
| chunker | original | **1,742** | 0,9976 | **1,786** | 0,9982 | **1,943** | 0,9996 |
| chunker | V1 | 1,219 | 0,9965 | 1,304 | 0,9943 | — | — |
| chunker | V2 | 0,979 | 0,9963 | 1,064 | 0,9921 | **1,438** | 0,9983 |
| chunker | OFF | 1,667 | 0,9991 | 1,748 | 0,9975 | — | — |
| défaut | original | **1,266** | 0,9949 | **1,367** | 0,9923 | **1,861** | 0,9964 |
| défaut | V1 | 1,263 | 0,9955 | 1,380 | 0,9910 | — | — |
| défaut | V2 | 1,046 | 0,9966 | 1,131 | 0,9928 | **1,551** | 0,9965 |
| défaut | OFF | 1,273 | 0,9934 | 1,372 | 0,9919 | — | — |

Trois lectures :

1. **La pente 20-160 sous-estime le O(n²)**. Sur le chunker, elle vaut 1,74, mais à
   640-1 280 elle monte à **1,94**, et le doublement 160→320 coûte déjà **×3,67** (au lieu de
   ×2 pour un algorithme linéaire). Sur le défaut, la pente passe de 1,27 à **1,86**. Les
   termes linéaires (tokenisation, phrases, POS) diluent la pente aux petites tailles.
2. **Le cache V2 divise le coût, mais ne linéarise pas complètement**. Sur 20-160, sa pente
   tombe à 0,98 / 1,05 — proche de 1 —, mais sur **160-1 280 elle reste 1,44 / 1,55** : le
   `sorted(gvs, key=ecart)` par segment est encore là, en O(S·G log G). À 1 280 tokens, le
   doublement 640→1 280 coûte encore ×3,0 (chunker) et ×3,5 (défaut) pour V2.
3. **Le contrôle OFF suit l'original** (1,67 vs 1,74 en chunker ; 1,27 vs 1,27 en défaut) :
   la chute de pente observée avec V2 vient bien du cache, pas d'un changement de chemin de
   mesure.

### 4.1 Attribution du coût (cProfile, N=160)

Les temps cProfile sont gonflés par l'instrumentation ; on ne lit que les **partages**.

- **Chunker seul, original** : total 1,447 s, dont `_syntagmes_simple` **1,115 s (77 %)** en
  97 appels, `_verbe_dans` 0,239 s, `_cible_proche` 0,212 s. V2 : total **0,116 s**,
  `_syntagmes_simple` 0,023 s, `_verbe_dans` 0,006 s.
- **Défaut, original** : total 0,747 s, dont `_cible_proche` **0,492 s (66 %)**, `_verbe_dans`
  0,492 s, `_est_verbe` 0,414 s (les deux se recouvrent), `_syntagmes_s` 0,036 s,
  `_tete_texte` 0,024 s. V2 : total **0,264 s**, `_cible_proche` 0,056 s, `_verbe_dans` 0,013 s.
  Le résidu V2 est le tri/proximité par segment, plus `_tete_texte` et le générateur S.

## 5. Surcoût de l'original et gain du cache

| N | chunker original (ms) | chunker V2 (ms) | gain | surcoût original vs V2 | défaut original (ms) | défaut V2 (ms) | gain | surcoût |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 20 | 1,75 | 0,73 | ×2,40 | +140 % | 1,98 | 1,58 | ×1,26 | +26 % |
| 40 | 5,04 | 1,31 | ×3,83 | +283 % | 4,23 | 2,99 | ×1,41 | +41 % |
| 80 | 17,29 | 2,57 | ×6,73 | +573 % | 9,89 | 6,08 | ×1,63 | +63 % |
| 160 | 64,82 | 5,58 | **×11,62** | **+1 061 %** | 27,83 | 13,94 | **×2,00** | **+100 %** |
| 320 | 238,00 | 14,10 | **×16,89** | **+1 589 %** | 88,38 | 36,88 | **×2,40** | **+140 %** |
| 640 | 957,93 | 37,10 | ×25,82 | +2 482 % | 367,28 | 102,41 | ×3,59 | +259 % |
| 1 280 | 3 748,72 | 112,14 | ×33,43 | +3 244 % | 1 171,87 | 356,82 | ×3,28 | +228 % |

Les lignes 640 et 1 280 sont les points de continuité (3 passes, médianes plus bruitées) ; les autres sont à 9 passes.

Le facteur à retenir dépend du chemin :

- **chunker seul** : ×11,6 à 160 tokens, ×16,9 à 320, ×25,8 à 640, ×33,4 à 1 280. Le gain
  **croît** avec la longueur, parce que le cache supprime le terme 1+2·S qui domine.
- **défaut** : ×2,0 à 160, ×2,4 à 320, puis **plateau ×3,3-3,6** à 640-1 280. Le cache retire
  le terme `_verbe_dans`, mais le tri par segment reste et devient le goulot.
- **corpus** : ×1,18-1,22 (chunker), ×0,97-1,07 (défaut). Pas de gain spectaculaire sur des
  phrases de 6 tokens.

La décomposition V1 → V2 isole la part du cache des verbes : à 160 tokens, V1 est à 11,80 ms
et V2 à 5,58 ms (**×2,11**) ; à 320, 34,80 → 14,10 ms (**×2,47**). En défaut, V1 ≈ original
et V2 fait tout le gain.

### 5.1 Sensibilité à la base : un GV à verbe plein change le gain défaut

| base | N | chunker original → V2 (ms) | gain | défaut original → V2 (ms) | gain |
|---|---:|---:|---:|---:|---:|
| A : « … est sur le toit » (GV à auxiliaire) | 160 | 64,82 → 5,58 | ×11,62 | 27,83 → 13,94 | ×2,00 |
| A | 320 | 238,00 → 14,10 | ×16,89 | 88,38 → 36,88 | ×2,40 |
| B : « … a vu la souris » (GV à verbe plein) | 160 | 84,99 → 4,64 | ×18,32 | 13,32 → 12,47 | **×1,07** |
| B | 320 | 337,72 → 12,91 | ×26,16 | 28,62 → 25,23 | **×1,13** |

En base A, `_verbe_dans` rend `« est »`, un auxiliaire : `_cible_proche` le saute et scanne
**tous** les GV. En base B, le GV de S `« a vu »` donne `« vu »`, plein : la boucle s'arrête au
premier GV et le cache ne sert presque à rien (×1,07-1,13). Le gain défaut est donc
**fortement dépendant de la phrase** ; le gain chunker, lui, reste (le re-chunking est
indépendant des GV). C'est la limite principale du chiffre ×2,0.

## 6. Correctif proposé (non appliqué)

**Fichier** : [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) ·
**fonction** : `Heuristique.analyser` · **lignes** : 853-941 (section 5), helpers 642 et
661-704. Le correctif est un **cache local à l'analyse** : aucun état d'instance, aucun
changement de signature obligatoire, aucune modification de sortie.

### 6.1 Pseudo-code précis

```python
# Dans Heuristique.analyser, après la ligne 855 (calcul de `verbes`).
# (A) Un seul chunking par analyse.
simples = self._syntagmes_simple(texte, lg)
# (B) Une seule extraction des GV.
gvs_simple = [x for x in simples if x["type"] == "GV"]
# (C) Cache des verbes de GV, local à CET appel d'analyser.
cache_gv = {}

cands = self._syntagmes_s(texte)
cibles_s = self._cibles_s(texte) if cands else {}

if cands:
    # ligne 861 : SUPPRIMER `gvs_simple = [...]` (déjà calculé en (B)).
    for c in cands[:1]:
        gvs_s = [x for x in c.get("segments", []) if x.get("type") == "GV"]
        deja = {(x["debut"], x["fin"]) for x in gvs_s}
        gvs = gvs_s + [x for x in gvs_simple if (x["debut"], x["fin"]) not in deja]
        for s in c.get("segments", []):
            ...
            cible = self._cible_proche(
                texte, s, gvs, verbes=verbes, cache_gv=cache_gv)       # 887, 895
            ...
            candidats = list(noms) + self._verbes_proches(
                texte, s, gvs, verbes=verbes, cache_gv=cache_gv)       # 899
else:
    # ligne 914 : `for s in simples:` (plus d'appel au chunker dans la boucle).
    for s in simples:
        cible = self._cible_proche(
            texte, s, gvs_simple, verbes=verbes, cache_gv=cache_gv)    # 916
        ...
        # ligne 919 : SUPPRIMER `gvs_s = [...]` ; utiliser `gvs_simple`.
        candidats = [s["type"]] + self._verbes_proches(
            texte, s, gvs_simple, verbes=verbes, cache_gv=cache_gv)    # 922

if cands and self.union:
    # ligne 928 : SUPPRIMER `simples = self._syntagmes_simple(...)` (déjà calculé en (A)).
    # ligne 929-930 : `gvs_u = gvs_s + gvs_simple`
    for s in simples:
        ...
        cible = self._cible_proche(
            texte, s, gvs_u, verbes=verbes, cache_gv=cache_gv)         # 935
        candidats = [s["type"]] + self._verbes_proches(
            texte, s, gvs_u, verbes=verbes, cache_gv=cache_gv)         # 940


@staticmethod
def _verbe_gv(texte, g, verbes, cache_gv):
    """Le verbe d'un GV, calculé une fois par analyse. Clé valide dans un seul texte."""
    if cache_gv is None:                       # compatibilité avec les appels existants
        return Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
    cle = (g["debut"], g["fin"])
    if cle not in cache_gv:
        cache_gv[cle] = Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
    return cache_gv[cle]


# Dans _cible_proche (lignes 661-686), remplacer les appels des lignes 681 et 685 :
v = Heuristique._verbe_gv(texte, g, verbes, cache_gv)
# et ajouter `cache_gv=None` à la signature, après `verbes=None`.

# Dans _verbes_proches (lignes 688-704), remplacer l'appel de la ligne 701 :
v = Heuristique._verbe_gv(texte, g, verbes, cache_gv)
# et ajouter `cache_gv=None` à la signature, après `verbes=None`.
```

Points de vigilance :

- La clé `(debut, fin)` est valide **parce que `cache_gv` est créé dans `analyser`** : `texte`
  et `verbes` sont constants pendant l'appel. Ne pas promouvoir ce cache en attribut
  d'instance : `analyser` peut être appelé sur des textes différents, et un état partagé
  exposerait à des courses si un même `Heuristique` est utilisé par plusieurs threads.
- Le fallback `cache_gv is None` garde la compatibilité des appels hors `analyser`
  (`MockNeuronal`, tests, outils).
- Ne pas oublier l'union (lignes 925-941) : c'est le troisième site qui recompte les GV.
- La sortie doit rester **strictement identique** ; le contrôle 612/612 + 10/10 du banc est
  la condition d'acceptation.

### 6.2 Effet attendu

| compteur | avant | après | N=320 |
|---|---:|---:|---:|
| `_syntagmes_simple` (chunker) | 1 + 2·S | 1 | 193 → 1 |
| `_syntagmes_simple` (défaut) | 2 | 1 | 2 → 1 |
| `_verbe_dans` sur GV (chunker) | 640 (160 tokens) | 16 | 2 304 → 32 |
| `_verbe_dans` sur GV (défaut) | 2 320 (160 tokens) | 32 | 8 736 → 64 |

Le gain mesuré de V2 est une **borne basse** : V2 conserve les 1+2·S appels (mémoïsés) et les
listes de GV reconstruites par segment, alors que le patch hoisté supprime ces appels et ces
listes. Le gain réel du patch devrait donc être **au moins** ×11,6 (160) / ×16,9 (320) sur le
chemin chunker, et **au moins** ×2,0 / ×2,4 sur le défaut, à sortie identique.

### 6.3 Ce que ce correctif ne règle pas

Le `sorted(gvs, key=ecart)` de `_cible_proche` et `_verbes_proches` est refait **pour chaque
segment** : O(S·G log G). C'est ce qui maintient la pente V2 à 1,44 / 1,55 sur 160-1 280 et
le plateau ×3,3-3,6 du défaut. Pour aller plus loin, il faudrait un **index pré-trié** des GV
(gauche par `fin` décroissante, droite par `debut` croissante, `bisect` + fusion, repli exact
sur le tri quand un GV recouvre le segment). Deux prototypes locaux ont été testés sur l'instantané antérieur (`d9c9d5…`), non re-mesurés ici :

- **V3** (index + `bisect`) : plus lent que V2 en Python pur (la fusion/générateur coûte plus
  que le Timsort C sur ≤128 GV) et **1 divergence sur 612** (`r362`, anglais) ;
- **V4** (un seul tri par segment, partagé cible/candidats) : plus lent que V2 (surcoût du
  cache `id(gvs)` et des lambdas).

Ils ne sont **pas retenus en l'état**. Si la linéarité stricte devient l'objectif, c'est un
chantier séparé, avec un test d'égalité dédié aux cas de recouvrement et aux ex æquo.

## 7. Contrôle négatif

| contrôle | résultat |
|---|---|
| **égalité de sortie** | V1, V2 et OFF identiques à l'original : **612/612** phrases du corpus et **10/10** textes longs (5 longueurs × 2 chemins), champ à champ |
| **OFF vs original, temps** | ratios ×0,90 à ×1,13 selon le point, **médiane ×1,00** ; l'écart est le bruit du Xeon partagé, pas un effet de code |
| **OFF vs original, pente** | 1,667 vs 1,742 (chunker) ; 1,273 vs 1,266 (défaut) : la pente ne baisse que lorsque le cache est actif |
| **compteurs N=160** | chunker : `_syntagmes_simple` 97 appels → 1 chunking, `_verbe_dans` 640 → 16 ; défaut : 2 → 1, 2 320 appels → 32 GV distincts |
| **profil N=160** | chunker : 1,447 s → 0,116 s sous cProfile ; défaut : 0,747 s → 0,264 s ; la baisse est portée par les fonctions ciblées |

Le contrôle OFF est le plus important : c'est **le même code de sous-classe**, avec les mêmes
méthodes réécrites, mais sans les hits de cache. Il redonne les temps de l'original. Le gain
n'est donc ni un changement d'algorithme déguisé, ni un artefact de la mesure.

## 8. Limites — ce qui pourrait rendre ce résultat faux

- **Base A défavorable.** Le GV `« est sur le toit »` a pour tête l'auxiliaire `« est »` ;
  `_cible_proche` le saute et scanne tous les GV. C'est un cas réel (copules), mais il amplifie
  le coût. Avec la base B à verbe plein, le gain défaut tombe à **×1,07-1,13** (tableau 5.1).
  Ne pas lire ×2,0 comme universel.
- **Corpus court.** 6,13 tokens `_mots`/phrase, 1,10 segment, 0,19 GV. Le gain corpus est
  faible (×1,18-1,22 chunker ; ×0,97-1,07 défaut) ; le O(n²) ne mord pas sur le gold actuel.
  Le résultat est une mesure de **passage à l'échelle**, pas une optimisation du gold.
- **Chemin par défaut = code mort.** Le générateur S répond pour les 612 phrases ;
  `_syntagmes_simple` n'est appelé que 2 fois/phrase. Le re-chunking dans la boucle n'est
  chaud que si `segmenter_s=False` ou si S échoue. Sur le corpus, le chemin par défaut est
  pourtant le plus lent en absolu (394 ms contre 231 ms) à cause du générateur S et des
  règles d'attachement, pas du chunker.
- **Le cache seul ne linéarise pas.** Pente V2 1,44 / 1,55 sur 160-1 280 ; le tri par segment
  reste. Une vraie linéarité demande l'index pré-trié (non retenu en l'état) ou une autre
  réduction du nombre de candidats.
- **Bruit de mesure.** Xeon E5-2687W v3 partagé, 40 cœurs, temps CPU, 3 à 11 passes. L'OFF
  varie de ×0,90 à ×1,13 selon le point ; lire les facteurs à ±10 % près. Le point 320
  chunker (×18,9 dans une passe antérieure, ×16,9 ici) illustre cette enveloppe.
- **Instantané de travail.** Le fichier mesuré a changé pendant la préparation (`d9c9d5…` →
  `6e8430…`) puis a été committé dans `9d5337ce` ; les mesures portent sur `6e8430…`, qui est
  le contenu de `HEAD`. Une édition ultérieure invalide les numéros de ligne. Les règles
  récentes `_tete_texte` et `_cible_s_par_genre` sont incluses dans les temps du chemin défaut.
- **Prototype ≠ patch.** V2 est une sous-classe du banc, pas le patch réel. L'égalité
  612/612 + 10/10 est un contrôle fort, mais le patch hoisté doit être appliqué puis repassé
  par la porte du bloc et une nouvelle mesure.
- **Clé du cache.** `(debut, fin)` n'est valide que dans un appel d'`analyser` (texte et
  `verbes` constants). Un cache global par instance serait faux si `analyser` change de texte,
  et risqué si l'instance est partagée entre threads. Le pseudo-code crée le dict localement.
- **Mesure CPU seulement.** `time.process_time` exclut les I/O et le temps hors CPU ; l'analyse
  est CPU-bound, mais une machine chargée peut décaler les médianes. Pas de mesure GPU : le
  bloc heuristique est CPU.

## 9. Conclusion

- **Le O(n²) est réel, et il y en a deux.** Sur le chemin chunker seul, c'est bien le
  re-chunking par segment (1+2·S appels) qui domine : le cache le supprime et donne
  **×11,6 à 160 tokens, ×16,9 à 320, ×33 à 1 280**. Sur le chemin par défaut,
  le re-chunking est du code mort ; le coût est le **re-scan des GV par `_verbe_dans`**
  (2 320 appels pour 32 GV à 160), que le cache des verbes ramène aux GV distincts : **×2,0 à
  160, ×2,4 à 320**, plateau ×3,3-3,6 ensuite.
- **Le correctif de cache est sûr, local et exact** : hoister `simples`/`gvs_simple`, créer un
  `cache_gv` local, passer ce cache aux deux helpers. Il ne change aucune sortie (612/612 +
  10/10) et ne crée aucun état d'instance. C'est le premier pas à appliquer.
- **Ne pas promettre la linéarité ni un gain corpus.** Le tri `sorted(gvs)` par segment reste
  et maintient une pente 1,44-1,55 au-delà de 320 tokens ; le corpus court ne gagne que
  ×1,18-1,22 (chunker) et ×0,97-1,07 (défaut). Le chantier suivant, si la linéarité devient
  l'objectif, est l'index pré-trié des GV — avec un vrai contrôle d'égalité sur les
  recouvrements, car le prototype V3 a échoué 1 fois sur 612.
- **Aucun fichier existant n'a été modifié par cette mission ; aucun commit n'a été fait.**
  Les deux livrables sont cette fiche et [`pensee-cout-chunker.json`](pensee-cout-chunker.json).
