# X3 — le tagger en lot : 1 000 items, 672 appels réseau, 0 $ en cache chaud

> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **X3** (J5, la part du
> pilote) · **Date** : 2026-11-15 · **HEAD mesuré** : `e1a28307` + ce diff · **Verdict** :
> ✅ **le lot est mesuré de bout en bout** — **1 000 items** (677 textes distincts), **672
> appels réseau** à froid, **99 971 tokens**, **685,2 s**, **87,6 items/min**, **40,8 Mo** de
> pic RSS, **0,02177 $** pour le lot (**0,032157 $** extrapolé à 1 000 textes uniques hors
> pointe, **0,064315 $** en pointe). Le **cache chaud** rejoue les mêmes 1 000 items en
> **2,635 s**, avec **0 réseau, 0 token, 0 $** et **1 000/1 000 sorties identiques**.
> `--jsonl` rend **1 003 lignes** (trois phrases du gold contiennent deux phrases) ; le second
> passage chaud est **0 réseau, 0 token**.

**En trois lignes.** (1) Le corpus réel disponible fait **681 lignes source** — 612 du gold
(hand 20 + reel 432 + synth 160) et **69 phrases** tirées des **50 textes libres** du banc de
robustesse (`pensee-fiabilite-produit.json`, 50 textes dont 2 vides et 2 refus) —, soit **677
textes distincts** (4 doublons) et **673 prompts distincts** (4 collisions de ponctuation). Le
lot de **1 000 items** ajoute **319 répétitions déterministes** (graine 20261115) : ce sont des
phrases réelles, mais **323 items rejouent un texte** déjà vu et **2 refusent sans appel** (texte
sans mot). (2) À froid, **672 appels réseau**, **3 rejeux disque** (prompts identiques) et **323
rejeux mémoire** — **326 items sur 1 000** ne sont pas facturés ; **99 971 tokens** (84 916
d'entrée + 15 055 de sortie), **685,2 s**, **87,6 items/min**, pic **40,8 Mo**, cache disque
**712 943 octets** en **672 fichiers**, **4 refus** sur 1 000. (3) À chaud, **0 réseau, 0 token,
0 $**, **2,635 s**, **22 770 items/min**, pic **38,2 Mo** : le contrôle négatif est **exact**,
et les **1 000 hashes** d'annotation sont identiques.

**Ce que cette fiche est, et n'est pas.**

- **Est** : la mesure **réelle** du câblage du tagger (`drave._cascade_tagger`, `NeuronalLLMPOS`
  + `Heuristique`, client `tools/llm/deepseek.py`, température 0) sur un lot de 1 000 items,
  avec le **cache froid**, le **cache chaud**, le **débit**, la **mémoire**, le **coût** et le
  mode **`--jsonl`** du CLI. Chaque item est enregistré (appel transport, cache disque, cache
  mémoire, refus sans appel, tokens, latence, hash) ; le JSON joint porte les agrégats et le
  détail des passes.
- **N'est pas** : une nouvelle mesure de **qualité** (W2 la porte : 402 **0,9643**, H50
  **0,8607**), une mesure d'un tagger **local** (règle 11 : aucun serveur local), ni un lot de
  **1 000 textes distincts** : les sources nommées n'en contiennent que **677**. Le chiffre à
  1 000 textes uniques est une **extrapolation** (×1,4771), et le lot à 1 000 items est la
  mesure **réelle**.
- **Public** : **R0.7/B13**, la décision **J5** du tagger, et toute machine qui doit chiffrer
  un lot avant de l'envoyer.

## 1. Le corpus et le lot

| source | lignes | textes distincts | mots (banc) | remarque |
|---|---:|---:|---:|---|
| `gold.json` (`hand`) | 20 | 20 | 105 | 14 fr + 6 en |
| `gold_reel.json` (`reel`) | 432 | 429 | 2 375 | 228 fr + 204 en ; 3 doublons |
| `gold_synthetique.json` (`synth`) | 160 | 160 | 699 | 160 fr, générés par le gold |
| **50 textes libres** (`pensee-fiabilite-produit.json`) | **69** | **69** | **1 068** | 50 textes (2 vides, 2 refus), segmentés en phrases |
| **total source** | **681** | **677** | **4 247** | 458 fr + 215 en + 7 `und` + 1 it |

Les **50 textes libres** sont le **banc de robustesse** (`reports/pensee-fiabilite-produit.json`,
`banc_50.resultats`) : 50 textes, **46 succès, 4 refus**, **1 068 mots** ; `Heuristique._phrases`
en tire **69 phrases** (les textes vides ou réduits à une ponctuation n'en donnent pas). Le lot
de 1 000 items est :

- les **681 lignes source**, dans l'ordre du corpus ;
- puis **319 répétitions** tirées au hasard déterministe (`random.Random(20261115)`), qui
  rejouent un texte déjà vu.

Il y a donc **677 textes distincts**, **4 doublons** (`r186`, `r189`, `r358`, et `f01-00`
« Le chat dort. » déjà dans le gold) et **319 répétitions ajoutées** : **323 items rejouent un
texte**. Deux items (`f14-00` « 🚀 », `f17-00` « ... ») n'ont **aucun mot** et refusent **sans
appel**. Le `sha256` des textes source est
`6a515d4585ec8e20a7fb4656f3af266bdba1def942faf03ad2bf713d605498b0`.

**Ce que « 1 000 phrases » veut dire ici.** Les sources nommées ne fournissent que **677 textes
distincts** ; il n'existe pas 1 000 phrases réelles dans le gold + les 50 textes. Le lot de
**1 000 items** est donc mesuré tel quel, et le coût des **1 000 textes uniques** est extrapolé
linéairement (×1,4771). Les 160 phrases `synth` du gold sont conservées parce que la consigne
part de la base **612** (`~0,04 $/612`) ; le sous-ensemble strictement réel (452 + 69 = 521
lignes, 517 textes distincts) est discuté dans les limites.

## 2. Le dispositif

- **Banc** : [`qualifier_tagger_lot.py`](../tools/tests/linguistique/qualifier_tagger_lot.py).
- **Câblage** : `drave._cascade_tagger` → `NeuronalLLMPOS("deepseek-chat")` + `Heuristique`,
  seuil 0,6, POS neuronal, syntagmes/rôles/pragmatique à l'heuristique. **Un appel par phrase**
  (le tagger de syntagmes a été retiré le 15/11).
- **Client** : `tools/llm/deepseek.py`, température 0, cache disque
  (`DEEPSEEK_CACHE`), clé lue par `drave._cle_tagger()` — **jamais affichée ni écrite**.
- **Modèle demandé / renvoyé** : `deepseek-chat` / **`deepseek-flash`** sur les **672** fichiers
  du cache.
- **Machine** : Linux, Python 3.13.16, 40 CPU, 125 GiB de RAM ; mesure **séquentielle**, une
  requête à la fois.
- **Trois passes** :
  1. **froid** : cache `/tmp/tagger-lot-fiab-cache` **vide**, 1 000 items, une cascade ;
  2. **chaud** : le **même** cache, 1 000 items, cascade neuve ;
  3. **`--jsonl`** : le CLI sur un fichier de 1 000 items (chaud), puis 20 items (froid, cache
     neuf).
- **Mémoire** : `VmHWM` de `/proc/self/status` et `ru_maxrss` (`resource`), en kio ; le pic est
  celui du processus Python, pas du serveur DeepSeek. Le cache disque est mesuré en fichiers et
  en octets.
- **Coût** : tarif public `deepseek-flash` au 2026-11-13 (entrée cache hit 0,003 / 0,006 $ par M,
  entrée cache miss 0,15 / 0,30 $, sortie 0,60 / 1,20 $, hors pointe / pointe), repris de
  [`rapport-coordination-r.md`](rapport-coordination-r.md) § 3.3. Le run a lieu le 2026-11-15 de
  **18 h 21 à 18 h 33 UTC**, dans la fenêtre hors pointe (16:30–00:30 UTC).

## 3. Les résultats

### 3.1 Le cache froid

| mesure | valeur |
|---|---:|
| items | **1 000** |
| textes distincts | **677** |
| prompts distincts | **673** |
| appels transport | **675** |
| **requêtes réseau** | **672** |
| rejeux disque (prompts identiques) | **3** |
| rejeux mémoire (texte déjà vu) | **323** |
| refus sans appel (texte sans mot) | **2** |
| **cache total (disque + mémoire)** | **326 / 1 000 = 32,6 %** |
| tokens d'entrée | **84 916** |
| tokens de sortie | **15 055** |
| **tokens totaux** | **99 971** |
| tokens rejoués depuis le disque (non facturés) | 392 |
| tokens par requête réseau | **148,8** |
| tokens par texte distinct | **147,7** |
| tokens par item du lot | **100,0** |
| durée murale | **685,2 s** (11 min 25 s) |
| latence réseau moyenne / médiane / p95 / max | **1,011 / 0,998 / 1,308 / 1,706 s** |
| latence par item moyenne / médiane | 0,684 / 0,912 s |
| latence réseau cumulée | 679,7 s |
| **débit** | **87,6 items/min** · **58,8 requêtes/min** |
| pic RSS | **40 836 kio** (~39,9 Mio) |
| RSS avant / delta de pic | 34 124 kio / **+6 712 kio** |
| cache disque | **712 943 octets** · **672 fichiers** · ~1 053 octets/texte |
| refus | **4 / 1 000** (3 items distincts) |

**Lecture.** Le cache **froid** n'est pas « 0 % » au sens strict : **3 items** sont servis par
le disque parce que trois couples de textes partagent le **même prompt** (la ponctuation n'est
pas envoyée au tagger) — « Tu viens demain ? » / « Tu viens demain. », « You come tomorrow? » /
« You come tomorrow. », « ce livre commence! » / « ce livre commence ». Ce ne sont pas des
réponses d'un cache chaud : les **672** fichiers ont été écrits pendant la passe. La quatrième
collision de prompt est « Le chat dort. », déjà dans le gold : elle est servie par la **mémoire**
du tagger (même texte, même langue) avant d'atteindre le client. Les **323** rejeux mémoire sont
les **4 doublons** et les **319 répétitions** ; les **2** items sans mot (`f14`, `f17`) refusent
**sans appel** et ne sont ni réseau ni cache. Le coût repose donc sur **672 requêtes**, pas
1 000.

**Les refus.** Quatre items (sur 1 000) refusent le POS neuronal, pour **3 items distincts** :

| item | refus | appel |
|---|---|---:|
| `f14-00` « 🚀 » | `vide` | **non** (aucun mot) |
| `f17-00` « ... » | `vide` | **non** (aucun mot) |
| `f50-03` (texte long) | `neuronal-pos: ValueError: longueur POS 37 / 34` | **oui** (puis rejeu mémoire) |

La cascade **replie** sur le POS de l'heuristique, le lot continue, le code reste **0** ; le
JSONL porte le `refus` de ces lignes. W2 n'avait **0 refus** sur 452 phrases ; le banc de
robustesse en trouve **4** (2 vides, 1 long texte refusé deux fois), ce qui est un résultat en
soi.

### 3.2 Le cache chaud — le contrôle négatif

| mesure | froid | **chaud** |
|---|---:|---:|
| requêtes réseau | 672 | **0** |
| rejeux disque | 3 | **675** |
| rejeux mémoire | 323 | **323** |
| refus sans appel | 2 | **2** |
| cache total (disque + mémoire) | 32,6 % | **99,8 %** |
| tokens facturés | 99 971 | **0** |
| dollars hors pointe | 0,021770 $ | **0 $** |
| durée murale | 685,2 s | **2,635 s** |
| débit | 87,6 items/min | **22 770 items/min** |
| pic RSS | 40 836 kio | **38 172 kio** |
| refus | 4 | **4** |
| hashes d'annotation identiques | — | **1 000 / 1 000** |

**Lecture.** Le cache chaud **rejoue les 1 000 items** — 675 rejeux disque (dont les 3
collisions de prompt) et 323 rejeux mémoire — **sans un seul appel réseau, sans un token, sans
un dollar**. Les **1 000 hashes** canoniques des annotations sont **identiques** à ceux du froid
(les 4 refus aussi) : le cache ne change pas la sortie, il supprime le coût. Le cache total est
**99,8 %**, pas 100 % : les **2** refus sans appel ne sont ni réseau ni cache. C'est le contrôle
négatif exigé : *les mêmes phrases en cache chaud coûtent 0*.

### 3.3 Le taux de cache, en deux définitions

| cache | froid | chaud |
|---|---:|---:|
| **disque seul** (items servis par un fichier) | 3 / 1 000 = **0,3 %** | 675 / 1 000 = **67,5 %** |
| **mémoire seule** (texte déjà vu dans la cascade) | 323 / 1 000 = **32,3 %** | 323 / 1 000 = **32,3 %** |
| **total** (disque + mémoire) | 326 / 1 000 = **32,6 %** | 998 / 1 000 = **99,8 %** |
| **sans appel** (refus « vide ») | 2 / 1 000 = **0,2 %** | 2 / 1 000 = **0,2 %** |
| **API prompt cache** (`prompt_cache_hit_tokens`) | **0 / 84 916 = 0 %** | 0 (aucun appel) |

**Lecture.** Le cache **disque** chaud est à **67,5 %**, pas 100 % : les **323 répétitions et
doublons** du lot sont servis par la **mémoire** de la cascade avant d'atteindre le client. Le
cache **total** atteint **99,8 %** (les 2 refus sans appel restent hors cache) et le coût est
**0**. Le cache **côté API** (`prompt_cache_hit_tokens`) est **vide** sur les 672 appels : tout
le prompt est facturé au tarif **miss**. Le cache disque local, lui, est **712 943 octets** pour
672 fichiers (~1 053 octets/texte) ; il ne bouge pas à chaud.

### 3.4 Le débit

| passe | items/min | requêtes/min | s/item | s/requête |
|---|---:|---:|---:|---:|
| **froid** | **87,6** | **58,8** | 0,685 | 1,020 |
| **chaud** | **22 770,4** | 0 | 0,0026 | 2,635 (total) |
| `--jsonl` chaud, 1er passage | 8 592,2 lignes/min | 34,3 | 0,0070 | — |
| `--jsonl` chaud, 2e passage | 21 078,8 lignes/min | 0 | 0,0028 | — |
| `--jsonl` froid, 20 items | 63,5 lignes/min | 63,5 | 0,945 | 0,945 |

**Lecture.** Le froid est **limité par la latence réseau** (1,011 s par requête, séquentiel) :
87,6 items/min. Le chaud est **limité par le CPU** (heuristique + copie d'annotations) :
22 770 items/min, **260×** le froid. Le `--jsonl` ajoute le coût de la sérialisation JSON
(8,29 Mo pour 1 003 lignes) : 8 592 lignes/min au premier passage (4 appels réseau), 21 079 au
second (0 appel). La concurrence API pourrait monter le froid, mais **pas** la latence par
requête ; le chiffre publié est **séquentiel**.

### 3.5 La mémoire

| processus | RSS avant | pic RSS | delta | cache disque |
|---|---:|---:|---:|---:|
| passe **froide** | 34 124 kio | **40 836 kio** | +6 712 kio | 712 943 o |
| passe **chaude** | 34 264 kio | **38 172 kio** | +3 908 kio | 712 943 o |
| `--jsonl` chaud, 1er | — | 37 884 kio | — | 712 943 o |
| `--jsonl` chaud, 2e | — | 35 476 kio | — | 712 943 o |
| `--jsonl` froid, 20 | — | 33 984 kio | — | 20 fichiers |

**Lecture.** Le pic est **40,8 Mio** à froid, **38,2 Mio** à chaud : la mémoire est dominée par
l'interpréteur et le **cache mémoire des 677 annotations**, pas par les 1 000 items (le banc ne
garde que les métriques et un hash par item). Le cache disque pèse **0,7 Mo**, soit ~1 053
octets par texte. Le `--jsonl` à 1 003 lignes pèse **8,29 Mo** sur `stdout` (le sous-processus
les capture), d'où un pic de 37,9 Mio ; le second passage, sans réseau, descend à 35,5 Mio.

### 3.6 Le coût

| poste | 1 000 items (mesuré) | 1 000 textes uniques (extrapolé ×1,4771) |
|---|---:|---:|
| appels transport | 675 | 997,0 |
| requêtes réseau | 672 | 992,6 |
| rejeux disque | 3 | 4,4 |
| rejeux mémoire | 323 | 0 |
| refus sans appel | 2 | 3,0 |
| tokens d'entrée | 84 916 | 125 430 |
| tokens de sortie | 15 055 | 22 238 |
| **tokens totaux** | **99 971** | **147 668** |
| **prix hors pointe** | **0,021770 $** | **0,032157 $** |
| **prix en pointe** | **0,043541 $** | **0,064315 $** |
| prix par item / par texte | 0,00002177 $ | 0,000032157 $ |

**Le chiffre de la consigne.** `0,04 $ / 612 → 0,065359 $ / 1 000` (extrapolation linéaire).
Le **mesuré extrapolé hors pointe** vaut **0,032157 $**, soit **−0,033202 $** (moitié moins) ;
le **mesuré extrapolé en pointe** vaut **0,064315 $**, à **0,001044 $** de la référence. La
raison est connue : la référence `0,04 $/612` est la mesure à **deux appels par phrase** (POS +
syntagmes) ; le câblage actuel fait **un appel par phrase** (le tagger de syntagmes a été retiré
le 15/11). Le chiffre W3 (**143 870 tokens / 0,031 $ pour 1 000**) est donc **confirmé à +2,6 %**
(147 668 tokens / 0,0322 $) : l'écart vient du banc de robustesse, plus long que le gold 452, et
des 4 refus.

**Le détail des tokens.** 84 916 d'entrée + 15 055 de sortie = **99 971** pour 672 appels, soit
**148,8 tokens/appel** ; 392 tokens supplémentaires sont **rejoués depuis le disque** (3 appels
servis par un prompt identique) et ne sont **pas facturés** — le total des appels est 100 363.
Tous les tokens d'entrée sont des **miss** (`prompt_cache_hit_tokens = 0`) : le cache côté API
n'a rien absorbé.

### 3.7 Le mode `--jsonl`

Le CLI est lancé sur un fichier de 1 000 items, une phrase par ligne avec une ligne vide entre
deux phrases (pour forcer la frontière), puis sur 20 items avec un cache neuf :

| passage | lignes | JSON valides | `stdout` | durée | réseau | tokens | cache | pic RSS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **chaud, 1er** | **1 003** | 1 003 | 8 292 533 o | 7,004 s | **4** | **513** | 673 | 37 884 kio |
| **chaud, 2e** | **1 003** | 1 003 | 8 292 533 o | 2,855 s | **0** | **0** | 677 | 35 476 kio |
| **froid, 20** | **20** | 20 | 160 229 o | 18,907 s | **20** | 2 907 | 0 | 33 984 kio |

**Lecture.** Le mode `--jsonl` **fonctionne** : une ligne JSON par phrase, `source=cascade`,
`refus` présent, coût sur `stderr`, jamais dans le JSONL. Le fichier de 1 000 items rend
**1 003 lignes** : trois phrases du gold (`Marie lit. Elle aime les livres.` et ses variantes)
contiennent **deux phrases** et le segmenteur du CLI les sépare. Ces 3 items, une fois découpés,
créent **4 prompts** absents du cache (les autres morceaux étaient déjà connus), d'où **4
appels, 513 tokens, 0,0001 $** au premier passage. Le **second passage**, même fichier et même
cache, rend **0 réseau, 0 token, 677 rejeux disque** : le contrôle négatif du mode est exact. Le
passage **froid de 20 items** prouve le chemin réseau (20 requêtes, 2 907 tokens, 18,9 s,
33 984 kio).

## 4. Le contrôle négatif

- **Même lot, cache chaud** : **0 réseau**, **0 token**, **0 $**, **2,635 s**, **22 770
  items/min**, **1 000/1 000 hashes identiques** (les 4 refus sont identiques). C'est le
  contrôle demandé.
- **Froid vs chaud** : 672 vs 0 requêtes ; 99 971 vs 0 tokens ; 0,021770 vs 0 $ ; les **1 000**
  annotations sont les mêmes.
- **Les 3 rejeux disque du froid ne sont pas un cache chaud** : ce sont trois paires de textes
  qui partagent le même prompt (ponctuation ignorée) ; les 672 fichiers ont été écrits pendant
  la passe, et le cache était vide au départ.
- **Les 2 refus sans appel** (`f14`, `f17`) ne sont ni réseau ni cache : le cache total est
  **99,8 %**, pas 100 %, mais le coût est **0** et les 1 000 sorties sont identiques.
- **`--jsonl`** : deuxième passage à **0 réseau, 0 token** ; le premier passage paie **4 appels**
  parce que le segmenteur du CLI découpe 3 phrases du gold, pas parce que le cache est froid.
- **Le cache ne change pas la sortie** : les hashes canoniques (sans durée) sont identiques
  entre froid et chaud ; le cache ne fait que supprimer l'appel.

## 5. Ce qui pourrait rendre ce résultat faux

- **677 textes distincts, pas 1 000.** Le lot de 1 000 items contient 319 répétitions et 4
  doublons ; le coût à 1 000 textes uniques est extrapolé (×1,4771). Si les textes manquants
  sont plus longs ou plus courts que la moyenne, le coût et le débit changent.
- **Le gold 612 contient 160 phrases synthétiques.** Le sous-ensemble strictement réel
  (452 + 69 = 521 lignes, 517 textes distincts) n'est pas mesuré seul ; son coût par texte peut
  différer, et les phrases synthétiques sont plus courtes que les textes libres.
- **Le tarif n'est pas figé.** Le prix `deepseek-flash` du 2026-11-13 et la fenêtre hors pointe
  (16:30–00:30 UTC) sont des hypothèses ; un changement de modèle, de routage ou de prix déplace
  le dollar, pas les tokens. Le run est à 18 h 21–18 h 33 UTC, hors pointe.
- **Le token est celui de l'API**, pas le mot. Le prompt fixe (consigne + classes + tokens) pèse
  l'essentiel : 84 916 tokens d'entrée pour 15 055 de sortie. Un changement de prompt ou de
  modèle change les tokens, donc le dollar.
- **La latence est séquentielle.** Une requête à la fois, sur cette machine et ce réseau ;
  l'API accepte plus de concurrence (le débit peut monter, la latence par requête non).
- **La mémoire est le RSS du processus Python**, pas celle du serveur DeepSeek. Le pic de
  40,8 Mio inclut l'interpréteur, l'heuristique et le cache mémoire des 677 annotations ; le
  cache disque pèse 0,7 Mo.
- **Le cache disque est local et daté.** Un cache chaud d'une autre date peut rejouer un autre
  modèle ou une autre réponse ; la passe froide (cache vide) est la référence. Le cache est
  indexé par `modèle + messages + température + max_tokens`, jamais par la clé.
- **Quatre refus sur 1 000 (3 items distincts).** `f14` (« 🚀 ») et `f17` (« ... ») refusent
  sans appel ; `f50-03` (texte long) est refusé deux fois (un appel réseau + un rejeu). La
  cascade replie sur l'heuristique ; le coût de l'appel est payé pour `f50-03`, pas pour les
  deux vides.
- **Les 50 textes libres sont le banc de robustesse**, pas un échantillon aléatoire ; 7 phrases
  sont en `und` et 1 en italien, taggées par un prompt français.
- **`--jsonl` dépend du segmenteur.** Le fichier de 1 000 items rend 1 003 lignes ; un corpus
  avec plus d'abréviations, d'URL ou d'e-mails en rendrait davantage, et chaque frontière
  nouvelle peut créer un prompt non caché.
- **La température 0 n'est pas un déterminisme garanti de l'API** ; le cache fige les réponses.
  Les 1 000 hashes identiques à chaud prouvent le **rejeu**, pas la reproductibilité du modèle.

## 6. Les fichiers

- [`reports/rapport-tagger-lot.md`](rapport-tagger-lot.md) — cette fiche.
- [`reports/rapport-tagger-lot.json`](rapport-tagger-lot.json) — les agrégats, les passes, le
  coût, le `--jsonl`, le contrôle négatif et les limites.
- [`tools/tests/linguistique/qualifier_tagger_lot.py`](../tools/tests/linguistique/qualifier_tagger_lot.py)
  — le banc (trois modes : `froid`, `chaud`, `fusion` ; `--libres fiabilite|produit`).
- Les caches de mesure sont dans `/tmp/tagger-lot-fiab-cache` (672 fichiers, 712 943 octets) ;
  le corpus `--jsonl` est dans `work/tagger-lot/` (ignoré par git).

**Commandes exactes.**

```bash
python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode froid \
  --cache /tmp/tagger-lot-fiab-cache --sortie /tmp/tagger-lot-fiab-froid.json --reset
python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode chaud \
  --cache /tmp/tagger-lot-fiab-cache --sortie /tmp/tagger-lot-fiab-chaud.json
python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode fusion \
  --froid /tmp/tagger-lot-fiab-froid.json --chaud /tmp/tagger-lot-fiab-chaud.json \
  --sortie reports/rapport-tagger-lot.json
```
