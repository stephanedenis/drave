# X3 — le tagger en lot : 1 000 items, 662 appels réseau, 0 $ en cache chaud

> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **X3** (J5, la part du
> pilote) · **Date** : 2026-11-15 · **HEAD mesuré** : `d2fd406a` + ce diff · **Verdict** :
> ✅ **le lot est mesuré de bout en bout** — **1 000 items** (665 textes distincts), **662
> appels réseau** à froid, **98 968 tokens**, **690,4 s**, **86,9 items/min**, **40,8 Mo** de
> pic RSS, **0,0216 $** pour le lot (**0,0325 $** extrapolé à 1 000 textes uniques hors pointe,
> **0,0651 $** en pointe). Le **cache chaud** rejoue les mêmes 1 000 items en **2,715 s**, avec
> **0 réseau, 0 token, 0 $** et **1 000/1 000 sorties identiques**. `--jsonl` rend **1 003
> lignes** (trois phrases du gold contiennent deux phrases) ; le second passage chaud est
> **0 réseau, 0 token**.

**En trois lignes.** (1) Le corpus réel disponible fait **668 lignes source** — 612 du gold
(hand 20 + reel 432 + synth 160) et **56 phrases** tirées des **50 textes libres** de l'audit
produit —, soit **665 textes distincts** (3 doublons du gold) et **662 prompts distincts**
(3 collisions de ponctuation). Le lot de **1 000 items** ajoute **332 répétitions déterministes**
(graine 20261115) : ce sont des phrases réelles, mais 335 items rejouent un texte déjà vu. (2)
À froid, **662 appels réseau**, **3 rejeux disque** (prompts identiques) et **335 rejeux mémoire**
— **33,8 %** des items ne sont pas facturés ; **98 968 tokens** (83 880 d'entrée + 15 088 de
sortie), **690,4 s**, **86,9 items/min**, pic **40,8 Mo**, cache disque **703 720 octets** en
**662 fichiers**. (3) À chaud, **0 réseau, 0 token, 0 $**, **2,715 s**, **22 099 items/min**,
pic **37,9 Mo** : le contrôle négatif est **exact**, et les **1 000 hashes** d'annotation sont
identiques.

**Ce que cette fiche est, et n'est pas.**

- **Est** : la mesure **réelle** du câblage du tagger (`drave._cascade_tagger`, `NeuronalLLMPOS`
  + `Heuristique`, client `tools/llm/deepseek.py`, température 0) sur un lot de 1 000 items,
  avec le **cache froid**, le **cache chaud**, le **débit**, la **mémoire**, le **coût** et le
  mode **`--jsonl`** du CLI. Chaque item est enregistré (appel transport, cache disque, cache
  mémoire, tokens, latence, hash) ; le JSON joint porte les agrégats et le détail des passes.
- **N'est pas** : une nouvelle mesure de **qualité** (W2 la porte : 402 **0,9643**, H50
  **0,8607**), une mesure d'un tagger **local** (règle 11 : aucun serveur local), ni un lot de
  **1 000 textes distincts** : les sources nommées n'en contiennent que **665**. Le chiffre à
  1 000 textes uniques est une **extrapolation** (×1,5038), et le lot à 1 000 items est la
  mesure **réelle**.
- **Public** : **R0.7/B13**, la décision **J5** du tagger, et toute machine qui doit chiffrer
  un lot avant de l'envoyer.

## 1. Le corpus et le lot

| source | lignes | textes distincts | mots (heuristique) | remarque |
|---|---:|---:|---:|---|
| `gold.json` (`hand`) | 20 | 20 | 105 | 14 fr + 6 en |
| `gold_reel.json` (`reel`) | 432 | 429 | 2 375 | 228 fr + 204 en ; 3 doublons |
| `gold_synthetique.json` (`synth`) | 160 | 160 | 699 | 160 fr, générés par le gold |
| **50 textes libres** (`pensee-produit-bloc-l.json`) | **56** | **56** | **819** | 50 textes de l'audit, segmentés en phrases |
| **total source** | **668** | **665** | **3 998** | 442 fr + 224 en + 2 `und` |

Les **50 textes libres** sont les 50 phrases écrites pour l'audit produit
([`pensee-produit-bloc-l.json`](pensee-produit-bloc-l.json), `banc_50.detail`, 819 mots) ; le
segmenteur `Heuristique._phrases` en tire **56 phrases** (6 textes sont multi-phrases). Le lot
de 1 000 items est :

- les **668 lignes source**, dans l'ordre du corpus ;
- puis **332 répétitions** tirées au hasard déterministe (`random.Random(20261115)`), qui
  rejouent un texte déjà vu.

Il y a donc **665 textes distincts** et **335 items répétés** (3 doublons source + 332 ajoutés).
Le `sha256` des textes source est `94d47d017f1597881425b2650a7ddc33a28d768e293b2db8acf7fd888eff2bc3`.
La composition par source du lot (avec répétitions) est : `reel` 655, `synth` 234, `libre` 85,
`hand` 26 ; par langue : fr 656, en 341, `und` 3.

**Ce que « 1 000 phrases » veut dire ici.** Les sources nommées ne fournissent que **665 textes
distincts** ; il n'existe pas 1 000 phrases réelles dans le gold + les 50 textes. Le lot de
**1 000 items** est donc mesuré tel quel, et le coût des **1 000 textes uniques** est extrapolé
linéairement (×1,5038). Les 160 phrases `synth` du gold sont conservées parce que la consigne
part de la base **612** (`~0,04 $/612`) ; le sous-ensemble strictement réel (452 + 56 = 508
lignes, 505 textes distincts) est discuté dans les limites.

## 2. Le dispositif

- **Banc** : [`qualifier_tagger_lot.py`](../tools/tests/linguistique/qualifier_tagger_lot.py).
- **Câblage** : `drave._cascade_tagger` → `NeuronalLLMPOS("deepseek-chat")` + `Heuristique`,
  seuil 0,6, POS neuronal, syntagmes/rôles/pragmatique à l'heuristique. **Un appel par phrase**
  (le tagger de syntagmes a été retiré le 15/11).
- **Client** : `tools/llm/deepseek.py`, température 0, cache disque
  (`DEEPSEEK_CACHE`), clé lue par `drave._cle_tagger()` — **jamais affichée ni écrite**.
- **Modèle demandé / renvoyé** : `deepseek-chat` / **`deepseek-flash`** sur les **662** fichiers
  du cache.
- **Machine** : Linux, Python 3.13.16, 40 CPU, 125 GiB de RAM ; mesure **séquentielle**, une
  requête à la fois.
- **Trois passes** :
  1. **froid** : cache `/tmp/tagger-lot-cache` **vide**, 1 000 items, une cascade ;
  2. **chaud** : le **même** cache, 1 000 items, cascade neuve ;
  3. **`--jsonl`** : le CLI sur un fichier de 1 000 items (chaud), puis 20 items (froid, cache
     neuf).
- **Mémoire** : `VmHWM` de `/proc/self/status` et `ru_maxrss` (`resource`), en kio ; le pic est
  celui du processus Python, pas du serveur DeepSeek. Le cache disque est mesuré en fichiers et
  en octets.
- **Coût** : tarif public `deepseek-flash` au 2026-11-13 (entrée cache hit 0,003 / 0,006 $ par M,
  entrée cache miss 0,15 / 0,30 $, sortie 0,60 / 1,20 $, hors pointe / pointe), repris de
  [`rapport-coordination-r.md`](rapport-coordination-r.md) § 3.3. Le run a lieu le 2026-11-15 de
  **17 h 58 à 18 h 10 UTC**, dans la fenêtre hors pointe (16:30–00:30 UTC).

## 3. Les résultats

### 3.1 Le cache froid

| mesure | valeur |
|---|---:|
| items | **1 000** |
| textes distincts | **665** |
| prompts distincts | **662** |
| appels transport | **665** |
| **requêtes réseau** | **662** |
| rejeux disque (prompts identiques) | **3** |
| rejeux mémoire (texte déjà vu) | **335** |
| **cache total (disque + mémoire)** | **338 / 1 000 = 33,8 %** |
| tokens d'entrée | **83 880** |
| tokens de sortie | **15 088** |
| **tokens totaux** | **98 968** |
| tokens rejoués depuis le disque (non facturés) | 392 |
| tokens par requête réseau | **149,5** |
| tokens par texte distinct | **148,8** |
| tokens par item du lot | **99,0** |
| durée murale | **690,4 s** (11 min 30 s) |
| latence réseau moyenne / médiane / p95 / max | **1,036 / 1,017 / 1,325 / 3,677 s** |
| latence par item moyenne / médiane | 0,690 / 0,915 s |
| latence réseau cumulée | 685,7 s |
| **débit** | **86,9 items/min** · **57,5 requêtes/min** |
| pic RSS | **40 820 kio** (~39,9 Mio) |
| RSS avant / delta de pic | 33 868 kio / **+6 952 kio** |
| cache disque | **703 720 octets** · **662 fichiers** · ~1 058 octets/texte |
| refus | **5 / 1 000** (2 textes distincts) |

**Lecture.** Le cache **froid** n'est pas « 0 % » au sens strict : **3 items** sont servis par
le disque parce que trois couples de textes partagent le **même prompt** (la ponctuation n'est
pas envoyée au tagger) — « Tu viens demain ? » / « Tu viens demain. », « You come tomorrow? » /
« You come tomorrow. », « ce livre commence! » / « ce livre commence ». Ce ne sont pas des
réponses d'un cache chaud : les **662** fichiers ont été écrits pendant la passe. Les **335**
autres items sont des **rejeux mémoire** (le texte est déjà dans la cascade) : le lot contient
**335 répétitions**. Le coût repose donc sur **662 requêtes**, pas 1 000.

**Les refus.** Cinq items (sur 1 000) refusent le POS neuronal : `x48-00` (« longueur POS 6 / 2 »)
et `x50-00` (« longueur POS 88 / 87 »), chacun deux fois, plus un second `x50-00`. Ce sont
**2 textes distincts sur 665** (0,3 %), tous deux des textes libres longs (URL, e-mail,
ponctuation). La cascade **replie** sur le POS de l'heuristique, le lot continue, le code reste
**0** ; le JSONL porte le `refus` de ces lignes. W2 n'avait **0 refus** sur 452 phrases ; ce lot
plus long en trouve, ce qui est un résultat en soi.

### 3.2 Le cache chaud — le contrôle négatif

| mesure | froid | **chaud** |
|---|---:|---:|
| requêtes réseau | 662 | **0** |
| rejeux disque | 3 | **665** |
| rejeux mémoire | 335 | **335** |
| cache total | 33,8 % | **100 %** |
| tokens facturés | 98 968 | **0** |
| dollars hors pointe | 0,021635 $ | **0 $** |
| durée murale | 690,4 s | **2,715 s** |
| débit | 86,9 items/min | **22 099 items/min** |
| pic RSS | 40 820 kio | **37 932 kio** |
| refus | 5 | **5** |
| hashes d'annotation identiques | — | **1 000 / 1 000** |

**Lecture.** Le cache chaud **rejoue les 1 000 items** — 665 rejeux disque (dont les 3
collisions de prompt) et 335 rejeux mémoire — **sans un seul appel réseau, sans un token, sans
un dollar**. Les **1 000 hashes** canoniques des annotations sont **identiques** à ceux du froid
(les 5 refus aussi) : le cache ne change pas la sortie, il supprime le coût. C'est le contrôle
négatif exigé : *les mêmes phrases en cache chaud coûtent 0*.

### 3.3 Le taux de cache, en deux définitions

| cache | froid | chaud |
|---|---:|---:|
| **disque seul** (items servis par un fichier) | 3 / 1 000 = **0,3 %** | 665 / 1 000 = **66,5 %** |
| **mémoire seule** (texte déjà vu dans la cascade) | 335 / 1 000 = **33,5 %** | 335 / 1 000 = **33,5 %** |
| **total** (disque + mémoire) | 338 / 1 000 = **33,8 %** | 1 000 / 1 000 = **100 %** |
| **API prompt cache** (`prompt_cache_hit_tokens`) | **0 / 83 880 = 0 %** | 0 (aucun appel) |

**Lecture.** Le cache **disque** chaud est à **66,5 %**, pas 100 % : les **335 répétitions** du
lot sont servies par la **mémoire** de la cascade avant d'atteindre le client. Le cache **total**
est à 100 % et le coût à 0. Le cache **côté API** (`prompt_cache_hit_tokens`) est **vide** sur
les 662 appels : tout le prompt est facturé au tarif **miss**. Le cache disque local, lui, est
**703 720 octets** pour 662 fichiers (~1 058 octets/texte) ; il ne bouge pas à chaud.

### 3.4 Le débit

| passe | items/min | requêtes/min | s/item | s/requête |
|---|---:|---:|---:|---:|
| **froid** | **86,9** | **57,5** | 0,690 | 1,043 |
| **chaud** | **22 099,4** | 0 | 0,0027 | 2,715 (total) |
| `--jsonl` chaud, 1er passage | 8 339,8 lignes/min | 33,3 | 0,0072 | — |
| `--jsonl` chaud, 2e passage | 19 577,1 lignes/min | 0 | 0,0031 | — |
| `--jsonl` froid, 20 items | 59,1 lignes/min | 59,1 | 1,016 | 1,016 |

**Lecture.** Le froid est **limité par la latence réseau** (1,036 s par requête, séquentiel) :
86,9 items/min. Le chaud est **limité par le CPU** (heuristique + copie d'annotations) :
22 099 items/min, **254×** le froid. Le `--jsonl` ajoute le coût de la sérialisation JSON
(8,65 Mo pour 1 003 lignes) : 8 340 lignes/min au premier passage (4 appels réseau), 19 577 au
second (0 appel). La concurrence API pourrait monter le froid, mais **pas** la latence par
requête ; le chiffre publié est **séquentiel**.

### 3.5 La mémoire

| processus | RSS avant | pic RSS | delta | cache disque |
|---|---:|---:|---:|---:|
| passe **froide** | 33 868 kio | **40 820 kio** | +6 952 kio | 703 720 o |
| passe **chaude** | 33 792 kio | **37 932 kio** | +4 140 kio | 703 720 o |
| `--jsonl` chaud, 1er | — | 39 108 kio | — | 703 720 o |
| `--jsonl` chaud, 2e | — | 35 772 kio | — | 703 720 o |
| `--jsonl` froid, 20 | — | 33 984 kio | — | 20 fichiers |

**Lecture.** Le pic est **40,8 Mio** à froid, **37,9 Mio** à chaud : la mémoire est dominée par
l'interpréteur et le **cache mémoire des 665 annotations**, pas par les 1 000 items (le banc ne
garde que les métriques et un hash par item). Le cache disque pèse **0,7 Mo**, soit ~1 058
octets par texte. Le `--jsonl` à 1 003 lignes pèse **8,65 Mo** sur `stdout` (le sous-processus
les capture), d'où un pic de 39,1 Mio ; le second passage, sans réseau, descend à 35,8 Mio.

### 3.6 Le coût

| poste | 1 000 items (mesuré) | 1 000 textes uniques (extrapolé ×1,5038) |
|---|---:|---:|
| appels transport | 665 | 1 000 |
| requêtes réseau | 662 | 995,5 |
| rejeux disque | 3 | 4,5 |
| rejeux mémoire | 335 | 0 |
| tokens d'entrée | 83 880 | 126 136 |
| tokens de sortie | 15 088 | 22 687 |
| **tokens totaux** | **98 968** | **148 823** |
| **prix hors pointe** | **0,021635 $** | **0,032534 $** |
| **prix en pointe** | **0,043270 $** | **0,065068 $** |
| prix par item / par texte | 0,0000216 $ | 0,0000325 $ |

**Le chiffre de la consigne.** `0,04 $ / 612 → 0,065359 $ / 1 000` (extrapolation linéaire).
Le **mesuré extrapolé hors pointe** vaut **0,032534 $**, soit **−0,032825 $** (moitié moins) ;
le **mesuré extrapolé en pointe** vaut **0,065068 $**, à **0,000291 $** de la référence. La
raison est connue : la référence `0,04 $/612` est la mesure à **deux appels par phrase** (POS +
syntagmes) ; le câblage actuel fait **un appel par phrase** (le tagger de syntagmes a été retiré
le 15/11). Le chiffre W3 (**143 870 tokens / 0,031 $ pour 1 000**) est donc **confirmé à +3,4 %**
(148 823 tokens / 0,0325 $) : l'écart vient des textes libres plus longs et des 5 refus.

**Le détail des tokens.** 83 880 d'entrée + 15 088 de sortie = **98 968** pour 662 appels, soit
**149,5 tokens/appel** ; 392 tokens supplémentaires sont **rejoués depuis le disque** (3 appels
servis par un prompt identique) et ne sont **pas facturés** — le total des appels est 99 360.
Tous les tokens d'entrée sont des **miss** (`prompt_cache_hit_tokens = 0`) : le cache côté API
n'a rien absorbé.

### 3.7 Le mode `--jsonl`

Le CLI est lancé sur un fichier de 1 000 items, une phrase par ligne avec une ligne vide entre
deux phrases (pour forcer la frontière), puis sur 20 items avec un cache neuf :

| passage | lignes | JSON valides | `stdout` | durée | réseau | tokens | cache | pic RSS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **chaud, 1er** | **1 003** | 1 003 | 8 645 416 o | 7,216 s | **4** | **513** | 667 | 39 108 kio |
| **chaud, 2e** | **1 003** | 1 003 | 8 645 416 o | 3,074 s | **0** | **0** | 667 | 35 772 kio |
| **froid, 20** | **20** | 20 | 160 228 o | 20,32 s | **20** | 2 907 | 0 | 33 984 kio |

**Lecture.** Le mode `--jsonl` **fonctionne** : une ligne JSON par phrase, `source=cascade`,
`refus` présent, coût sur `stderr`, jamais dans le JSONL. Le fichier de 1 000 items rend
**1 003 lignes** : trois phrases du gold (`Marie lit. Elle aime les livres.` et ses variantes)
contiennent **deux phrases** et le segmenteur du CLI les sépare. Ces 3 items, une fois découpés, créent **4
prompts** absents du cache (les autres morceaux étaient déjà connus), d'où **4 appels, 513
tokens, 0,0001 $** au premier passage. Le **second passage**, même fichier
et même cache, rend **0 réseau, 0 token, 667 rejeux disque** : le contrôle négatif du mode est
exact. Le passage **froid de 20 items** prouve le chemin réseau (20 requêtes, 2 907 tokens,
20,32 s, 33 984 kio).

## 4. Le contrôle négatif

- **Même lot, cache chaud** : **0 réseau**, **0 token**, **0 $**, **2,715 s**, **22 099
  items/min**, **1 000/1 000 hashes identiques** (les 5 refus sont identiques). C'est le
  contrôle demandé.
- **Froid vs chaud** : 662 vs 0 requêtes ; 98 968 vs 0 tokens ; 0,021635 vs 0 $ ; les **1 000**
  annotations sont les mêmes.
- **Les 3 rejeux disque du froid ne sont pas un cache chaud** : ce sont trois paires de textes
  qui partagent le même prompt (ponctuation ignorée) ; les 662 fichiers ont été écrits pendant
  la passe, et le cache était vide au départ.
- **`--jsonl`** : deuxième passage à **0 réseau, 0 token** ; le premier passage paie **4 appels**
  parce que le segmenteur du CLI découpe 3 phrases du gold, pas parce que le cache est froid.
- **Le cache ne change pas la sortie** : les hashes canoniques (sans durée) sont identiques
  entre froid et chaud ; le cache ne fait que supprimer l'appel.

## 5. Ce qui pourrait rendre ce résultat faux

- **665 textes distincts, pas 1 000.** Le lot de 1 000 items contient 335 répétitions ; le coût
  à 1 000 textes uniques est extrapolé (×1,5038). Si les 335 textes manquants sont plus longs
  ou plus courts que la moyenne, le coût et le débit changent.
- **Le gold 612 contient 160 phrases synthétiques.** Le sous-ensemble strictement réel
  (452 + 56 = 508 lignes, 505 textes distincts) n'est pas mesuré seul ; son coût par texte peut différer, et les
  phrases synthétiques sont plus courtes que les textes libres.
- **Le tarif n'est pas figé.** Le prix `deepseek-flash` du 2026-11-13 et la fenêtre hors pointe
  (16:30–00:30 UTC) sont des hypothèses ; un changement de modèle, de routage ou de prix déplace
  le dollar, pas les tokens. Le run est à 17 h 58–18 h 10 UTC, hors pointe.
- **Le token est celui de l'API**, pas le mot. Le prompt fixe (consigne + classes + tokens) pèse
  l'essentiel : 83 880 tokens d'entrée pour 15 088 de sortie. Un changement de prompt ou de
  modèle change les tokens, donc le dollar.
- **La latence est séquentielle.** Une requête à la fois, sur cette machine et ce réseau ;
  l'API accepte plus de concurrence (le débit peut monter, la latence par requête non).
- **La mémoire est le RSS du processus Python**, pas celle du serveur DeepSeek. Le pic de
  40,8 Mio inclut l'interpréteur, l'heuristique et le cache mémoire des 665 annotations ; le
  cache disque pèse 0,7 Mo.
- **Le cache disque est local et daté.** Un cache chaud d'une autre date peut rejouer un autre
  modèle ou une autre réponse ; la passe froide (cache vide) est la référence. Le cache est
  indexé par `modèle + messages + température + max_tokens`, jamais par la clé.
- **Cinq refus sur 1 000.** `x48-00` et `x50-00` (2 textes distincts) font replier le POS sur
  l'heuristique ; le coût de l'appel est payé, la sortie n'est pas neuronale pour ces lignes.
  Un autre modèle ou un autre prompt peut changer le taux de refus.
- **`--jsonl` dépend du segmenteur.** Le fichier de 1 000 items rend 1 003 lignes ; un corpus
  avec plus d'abréviations, d'URL ou d'e-mails en rendrait davantage, et chaque frontière
  nouvelle peut créer un prompt non caché.
- **La température 0 n'est pas un déterminisme garanti de l'API** ; le cache fige les réponses.
  Les 1 000 hashes identiques à chaud prouvent le **rejeu**, pas la reproductibilité du modèle.
- **Les 50 textes libres sont écrits pour l'audit**, pas un échantillon aléatoire ; 14 sont en
  anglais et 2 en `und`, taggés par un prompt français. Le lot n'est pas une mesure de qualité
  multilingue.

## 6. Les fichiers

- [`reports/rapport-tagger-lot.md`](rapport-tagger-lot.md) — cette fiche.
- [`reports/rapport-tagger-lot.json`](rapport-tagger-lot.json) — les agrégats, les passes, le
  coût, le `--jsonl`, le contrôle négatif et les limites.
- [`tools/tests/linguistique/qualifier_tagger_lot.py`](../tools/tests/linguistique/qualifier_tagger_lot.py)
  — le banc (trois modes : `froid`, `chaud`, `fusion`).
- Les caches de mesure sont dans `/tmp/tagger-lot-cache` (662 fichiers, 703 720 octets) ; le
  corpus `--jsonl` est dans `work/tagger-lot/` (ignoré par git).

**Commandes exactes.**

```bash
python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode froid \
  --cache /tmp/tagger-lot-cache --sortie /tmp/tagger-lot-froid.json --reset
python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode chaud \
  --cache /tmp/tagger-lot-cache --sortie /tmp/tagger-lot-chaud.json
python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode fusion \
  --froid /tmp/tagger-lot-froid.json --chaud /tmp/tagger-lot-chaud.json \
  --sortie reports/rapport-tagger-lot.json
```
