# W2 — le tagger POS sur le split 402 / H50 : +4,45 pts sur 402, +17,65 sur H50 ; il gagne sur les deux, donc la règle ne le rejette pas

> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **W2** (semaine 2, J2 matin) ·
> **Date** : 2026-11-15 (mesure) · **Cible** : J2 · 17/11 · **HEAD mesuré** : `6b2208ee` ·
> **Verdict** : ✅ **le tagger n'est pas H50-only** — il gagne **+4,45 pts** sur **402** et
> **+17,65 pts** sur **H50** ; le F1 et l'attachement du 402 sont **inchangés**. **Réserve nommée** :
> sur 402, le gain est **ouvert** (+10,64 pts) et le **fermé baisse** (−1,55 pt) ; une règle qui
> exigerait la non-régression du fermé rejetterait le tagger tel quel.

**En trois lignes.** (1) Sur les **402** phrases de l'entraînement, le POS passe de **0,9198** à
**0,9643** (**+4,45 pts**, **96 tokens** réparés sur 2 157) ; sur les **50** de **H50**, de
**0,6842** à **0,8607** (**+17,65 pts**, **57 tokens** sur 323). (2) Le **F1** et l'**attachement**
ne bougent pas (le tagger ne remplace que le POS) ; le total 452 donne **0,9508** contre **0,8891**
(**+6,17 pts**), à **0,0008** du 0,9500 déjà publié. (3) La passe **API** paie **447 requêtes** et
**65 029 tokens réseau** pour **452** phrases, soit **~144 tokens** et **~0,98 s** par phrase ; le
**cache chaud après API** rejoue les mêmes réponses avec **0 réseau** et **0 token**. **La règle** :
le tagger gagne sur le 402, donc il n'est pas rejeté comme règle H50-only ; **la réserve du fermé**
est explicitement portée.

**Ce que cette fiche est, et n'est pas.**

- **Est** : la mesure du tagger POS de l'API sur le split **402 / H50** figé par W1, le POS de
  l'heuristique et du tagger sur chaque base, le **delta**, le détail **fermé / ouvert** et **par
  langue**, le **coût** et la **latence** par phrase, les passes **cache chaud → API → cache chaud
  après API**, et l'application de la règle « une règle qui ne gagne que sur H50 est rejetée ».
- **N'est pas** : une nouvelle annotation du gold (le gold est à S), une mesure d'un tagger local
  (règle 11 : pas de serveur local), une décision sur le **défaut** du produit (c'est W3), ni une
  mesure de la **généralisation** : H50 est sélectionné sur les erreurs de l'heuristique, il est
  circulaire par construction.
- **Public** : **R/B13** (R0.7), **W3** (la décision du défaut), **S** (les 4 cibles de H50).

## 1. Le split et le dispositif

### 1.1 Le split

Le split est celui de W1 ([`rapport-gold-452.md`](rapport-gold-452.md)) : **402** phrases pour
l'entraînement, **50** pour la tenue à l'écart (**H50**), **25 fr + 25 en**, **323 tokens**,
**190 segments**, **22 cibles** d'attachement. H50 = les **50 phrases dures** de C3, sélectionnées
par score d'erreur de l'heuristique (`3 × attachement + 2 × POS + 1 × segment absent`), sans aléa.
Le manifeste `sha256` des 50 ids triés est
`1615c17a97bb998451de66585dadcea0643ba1d7f8d962ccbdf28a13b575d970` ; la partition est vérifiée
(H50 ∩ 402 = 0, union = 452). Le tirage aléatoire de la graine `20261116`, **H50 retiré**, donne un
**contrôle de composition** de **45** phrases (il n'est pas un échantillon neuf : les phrases sont
dans le gold).

### 1.2 La mesure

La mesure est celle de `drave evaluer --tagger` : `evaluer_bloc` de
[`tools/tests/linguistique/evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py), la
**cascade** de [`tools/drave.py`](../tools/drave.py) (`_cascade_tagger`, seuil **0,6**), la fusion
`POS → neuronal ; syntagmes, rôles, attachement, pragmatique → heuristique`. Le tagger est
`NeuronalLLMPOS` (API DeepSeek, température 0), le client est
[`tools/llm/deepseek.py`](../tools/llm/deepseek.py). **Un appel par phrase** (le tagger de
syntagmes a été retiré le 15/11), **0 refus** sur les 452.

Le banc est [`tools/tests/linguistique/qualifier_tagger_h50.py`](../tools/tests/linguistique/qualifier_tagger_h50.py).
Il mesure quatre bases : **402**, **H50**, **total 452** et **tirage 45**. Chaque base a sa propre
cascade (cache mémoire neuf) ; le cache disque est partagé dans une passe.

### 1.3 Les trois passes

| passe | cache | ce qu'elle mesure |
|---|---|---|
| **cache chaud** | `data/deepseek/cache` existant (3 759 fichiers, 2026-10-26 → 2026-11-15 01:38) | les réponses déjà reçues ; **399 + 50 appels, tous en cache**, 0 réseau, 0 token |
| **API** | cache **neuf** `/tmp/tagger-h50-api-cache` (vide au départ) | **toutes** les phrases passent par l'API ; c'est la mesure de référence |
| **cache chaud après API** | le cache neuf de la passe API (447 fichiers, 2026-11-15 09:11 → 09:18) | le même run, **0 réseau, 0 token** ; contrôle de déterminisme du cache |

L'ordre demandé est **cache chaud puis API** ; le troisième passage vérifie que le cache neuf rejoue
exactement les mêmes réponses. Le modèle **demandé** est `deepseek-chat` ; le modèle **renvoyé** est
`deepseek-flash` sur les 449 appels de la passe API (comme le 612 du 13/11).

## 2. Les résultats

### 2.1 Les scores sur 402 et H50

| base | phrases | tokens | POS heuristique | POS tagger | **Δ POS** | fermé H → T | ouvert H → T | F1 H → T | attachement H → T |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **402** | 402 | 2 157 | 0,9198 (1 984) | **0,9643** (2 080) | **+4,45 pts** | 0,9580 → 0,9425 (**−1,55**) | 0,8804 → 0,9868 (**+10,64**) | 0,8190 → 0,8190 | 1,0000 → 1,0000 |
| **H50** | 50 | 323 | 0,6842 (221) | **0,8607** (278) | **+17,65 pts** | 0,7542 → 0,8156 (**+6,14**) | 0,5972 → 0,9167 (**+31,95**) | 0,5836 → 0,5836 | 0,9545 → 0,9545 |
| **total 452** | 452 | 2 480 | 0,8891 (2 205) | **0,9508** (2 358) | **+6,17 pts** | 0,9294 → 0,9246 (**−0,48**) | 0,8466 → 0,9784 (**+13,18**) | 0,7906 → 0,7906 | 0,9946 → 0,9946 |

**Lecture.** Le tagger gagne **sur les deux bases**. Le gain est **plus grand sur H50** (+17,65) que
sur 402 (+4,45) : c'est attendu, H50 est le lot dur, et c'est précisément pourquoi le gain H50 **ne
suffit pas** comme preuve. Le contrôle est le **402** : il ne baisse pas, il gagne. Le **total 452**
donne **0,9508** contre **0,8891** ; la fiche D1 publiait **0,9500**, l'écart est de **0,0008**
(2 tokens), dans le bruit de l'API.

**Le fermé n'est pas uniforme.** Sur 402, le tagger **perd 1,55 pt** sur les classes fermées
(DET, PREP, CONJ, PRON, AUX) et **gagne 10,64 pts** sur les ouvertes (VERB, NOUN, ADJ) ; le gain net
est **+4,45**. Sur H50, il gagne **aussi** le fermé (+6,14). La réserve est donc **propre au 402** :
le tagger n'est pas « meilleur partout », il est meilleur **en agrégé** sur 402 et **partout** sur
H50. Le détail par classe est au § 2.3.

### 2.2 Par langue

| base | langue | phrases | tokens | POS heuristique | POS tagger | Δ |
|---|---|---:|---:|---:|---:|---:|
| **402** | fr | 217 | 1 164 | 0,8754 | **0,9570** | **+8,16 pts** |
| **402** | en | 185 | 993 | 0,9718 | **0,9728** | **+0,10 pt** |
| **H50** | fr | 25 | 168 | 0,6012 | **0,7917** | **+19,05 pts** |
| **H50** | en | 25 | 155 | 0,7742 | **0,9355** | **+16,13 pts** |
| **total** | fr | 242 | 1 332 | 0,8408 | **0,9362** | **+9,54 pts** |
| **total** | en | 210 | 1 148 | 0,9451 | **0,9678** | **+2,27 pts** |

**Lecture.** Le gain est surtout **français** : +8,16 sur le 402 fr, **+0,10** sur le 402 en (un seul
token sur 993). Sur H50, les deux langues gagnent (+19,05 fr, +16,13 en). Le prompt du tagger est
**français** ; l'anglais du gold est étiqueté par le même prompt, et le 402 anglais est déjà à
**0,9718** pour l'heuristique : il n'y a presque rien à gagner. Ce n'est pas une mesure de tagger
anglais.

### 2.3 Le détail fermé / ouvert sur 402

| classe | gold | heuristique | tagger | Δ rappel |
|---|---:|---:|---:|---:|
| DET | 399 | 0,9950 | 0,9875 | **−0,75** |
| PREP | 83 | 1,0000 | 0,9157 | **−8,43** |
| CONJ | 69 | 0,8261 | 0,7246 | **−10,15** |
| PRON | 361 | 0,9418 | 0,9418 | 0,00 |
| ADV | 78 | 0,9103 | 0,9487 | +3,84 |
| AUX | 103 | 0,9612 | 0,9320 | **−2,92** |
| NOUN | 462 | 0,9913 | 0,9957 | +0,44 |
| VERB | 512 | 0,7852 | **0,9766** | **+19,14** |
| ADJ | 67 | 0,8060 | **1,0000** | **+19,40** |

**Lecture.** Le gain du 402 est **un gain de classes ouvertes** : **VERB +19,14** et **ADJ +19,40** gagnent ces points de rappel **dans leur
classe** ; le fermé perd **−1,55 pt** au total, surtout
**PREP −8,43** et **CONJ −10,15**, avec **AUX −2,92** et **DET −0,75**. Le tagger répare les verbes
et les adjectifs, et il **casse un peu de fermé**. Sur H50, le même tagger gagne **aussi** le fermé
(VERB 0,3857 → 0,8286, PRON 0,6479 → 0,7746, AUX 0,7727 → 0,9091, NOUN 0,7719 → 1,0000) : le lot
dur est dur **aussi** pour le fermé de l'heuristique, et le tagger y est meilleur. La réserve du 402
ne se reproduit pas sur H50.

### 2.4 Le total 452 et le tirage de composition

| base | phrases | POS heuristique | POS tagger | Δ |
|---|---:|---:|---:|---:|
| **total 452** | 452 | 0,8891 | **0,9508** | **+6,17 pts** |
| **tirage 20261116 hors H50** | 45 | 0,9073 | **0,9556** | **+4,83 pts** |

**Lecture.** Le tirage aléatoire **hors H50** gagne **+4,83 pts**, du même ordre que le 402
(+4,45) et **loin** du H50 (+17,65) : le gain « normal » est autour de **+4,5 à +5**, et H50 est
bien un **stress test**, pas un échantillon. Le tirage n'est pas un échantillon neuf : c'est un
contrôle de composition, il ne remplace pas une généralisation hors gold.

## 3. Le coût et la latence

### 3.1 La passe API

| base | phrases | appels | requêtes | cache | tokens réseau | tokens lus du cache | tokens / phrase | latence / requête | latence / phrase | durée |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **402** | 402 | 399 | **397** | 2 | **57 544** | 261 | **143,14** (réseau) · 143,79 (total) | **0,993 s** (méd. 1,000 ; p95 1,292 ; max 1,589) | **0,981 s** | 397,7 s |
| **H50** | 50 | 50 | **50** | 0 | **7 485** | 0 | **149,70** | **0,989 s** (méd. 0,968 ; p95 1,324 ; max 1,573) | **0,989 s** | 49,9 s |
| **total 452 (402 + H50)** | 452 | 449 | **447** | 2 | **65 029** | 261 | **143,87** (réseau) · 144,45 (total) | **0,993 s** (moyenne pondérée) | **0,982 s** | 452,0 s (passe) |
| **total, rejoué (base `total`)** | 452 | 449 | 0 | 449 | 0 | 65 290 | 0 (réseau) · 144,45 (lu) | — | — | 0,1 s |

**Lecture.** La passe API paie **447 requêtes réseau** pour **452** phrases : **397** pour le 402
et **50** pour H50. Les **2 lectures de cache** du 402 viennent de deux phrases qui partagent la
**même liste de tokens** qu'une phrase déjà appelée : `r423` (« Tu viens demain. ») a le prompt de
`r010` (« Tu viens demain ? »), et `r427` (« You come tomorrow. ») celui de `r030` (« You come
tomorrow? »). Le tagger ne reçoit que mots et nombres : la ponctuation ne change pas le prompt, donc
le cache disque sert ces deux phrases (261 tokens) sans appel. Les **trois textes dupliqués**
(`r019`/`r186`, `r051`/`r189`, `r336`/`r358`) sont, eux, servis par le **cache mémoire** du tagger
(même texte, même langue) : 399 appels pour 402 phrases, pas 402.

Le coût est de **65 029 tokens réseau** pour 452 phrases, soit **143,87 tokens/phrase** en réseau
(**144,45** en comptant les 261 tokens lus du cache) ; la latence est de **443,8 s** de réseau au
total, **0,982 s/phrase**, **0,993 s/requête** en moyenne. Le total rejoué depuis le cache neuf
(449 hits) ne refait **aucun appel réseau** et **aucun token** : c'est le contrôle de cache.

### 3.2 Le cache chaud

| passe | base | appels | réseau | cache | tokens réseau | tokens lus du cache | latence murale | score POS tagger |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **cache chaud (avant API)** | 402 | 399 | **0** | 399 | **0** | 57 805 | 0,058 s | 0,9629 |
| **cache chaud (avant API)** | H50 | 50 | **0** | 50 | **0** | 7 485 | 0,007 s | 0,8638 |
| **cache chaud (avant API)** | total | 449 | **0** | 449 | **0** | 65 290 | 0,066 s | 0,9500 |
| **cache chaud (avant API)** | tirage | 45 | **0** | 45 | **0** | 6 514 | 0,007 s | 0,9597 |
| **cache chaud (après API)** | 402 | 399 | **0** | 399 | **0** | 57 805 | 0,057 s | **0,9643** |
| **cache chaud (après API)** | H50 | 50 | **0** | 50 | **0** | 7 485 | 0,007 s | **0,8607** |
| **cache chaud (après API)** | total | 449 | **0** | 449 | **0** | 65 290 | 0,063 s | **0,9508** |
| **cache chaud (après API)** | tirage | 45 | **0** | 45 | **0** | 6 514 | 0,007 s | **0,9556** |

**Lecture.** Le cache chaud **avant** l'API rejoue des réponses **antérieures** (3 759 fichiers,
jusqu'au 2026-11-15 01:38) : il donne **0,9629 / 0,8638 / 0,9500 / 0,9597**, légèrement différent
de l'API (**0,9643 / 0,8607 / 0,9508 / 0,9556**). Ce n'est pas un bug : le cache fige des réponses
d'un **autre moment** du même modèle `deepseek-flash`, et l'API n'est pas déterministe à
température 0. Le cache chaud **après** l'API rejoue le **run du jour** et redonne **exactement**
les scores de l'API. Un cache chaud ne prouve donc pas le modèle du jour : seule la passe API le
fait ; le cache chaud est un **contrôle de coût** (0 réseau, 0 token) et de **rejeu** (après API).

### 3.3 Le coût par phrase, en une ligne

- **API** : **0,989 requête/phrase** (447 / 452), **143,87 tokens réseau/phrase**,
  **0,982 s/phrase** (moyenne des requêtes réseau ; médiane 402 **1,000 s**, H50 **0,968 s** ; p95
  **1,292–1,324 s** ; max **1,589 s**).
- **Cache chaud** : **0 réseau, 0 token**, **~0,0001 s/phrase** de lecture (0,06 s pour 402).
- **Prix** : la fiche donne les **tokens** et la **latence**, pas un dollar : le tarif de l'API
  change, et le coût est dominé par le prompt (le tagger reçoit la liste des tokens). La passe API
  consomme **65 029 tokens réseau pour 452 phrases** ; c'est le chiffre à multiplier par le tarif
  du jour, pas un prix figé.

## 4. La règle de décision

### 4.1 L'énoncé

**Une règle qui ne gagne que sur H50 est rejetée.** Le contrôle est la **non-régression du 402**,
pas le gain sur H50. H50 est sélectionné sur les erreurs de l'heuristique : il est **circulaire**,
et un gain plus grand sur H50 est **attendu** sans être une preuve. La règle exige :

1. **delta POS 402 ≥ 0** (le 402 ne baisse pas) ;
2. **F1 402 ≥ 0** et **attachement 402 ≥ 0** (le tagger ne doit pas casser les autres niveaux) ;
3. **delta POS H50 ≥ 0** (la tenue à l'écart ne baisse pas) ;
4. **rejet** si le seul gain est H50 (`delta 402 ≤ 0` et `delta H50 > 0`).

### 4.2 L'application au tagger

| critère | valeur | verdict |
|---|---:|---|
| delta POS 402 | **+4,45 pts** | ✅ |
| delta F1 402 | **0,00** | ✅ |
| delta attachement 402 | **0,00** | ✅ |
| delta POS H50 | **+17,65 pts** | ✅ |
| le seul gain est H50 ? | **non** (402 gagne) | ✅ |

**Verdict : ✅ accepté par la règle.** Le tagger **gagne sur le 402** (+4,45) et **sur H50**
(+17,65) ; il n'est pas un candidat H50-only. Le gain H50 (+17,65) est **plus grand** que le gain
402 (+4,45) : c'est normal, H50 est le lot dur. **Ne pas publier +17,65 seul** : le chiffre qui
décide est le **+4,45 du 402**, et le +6,17 du total 452.

### 4.3 La réserve : le fermé du 402 baisse

La règle ci-dessus est **agrégée**. Si on la durcit en **« aucune classe ne baisse sur 402 »**, le
tagger est **rejeté** : le fermé perd **−1,55 pt** (PREP −8,43, CONJ −10,15, AUX −2,92, DET −0,75,
PRON 0,00) et le **net** du fermé est négatif : PREP, CONJ, AUX et DET perdent, l'ADV gagne +3,84 mais
ne compense pas, et le gain net vient de l'ouvert (VERB +19,14, ADJ +19,40). Cette réserve ne
change pas le verdict de la règle **telle qu'elle est écrite**, mais elle change la **décision du
défaut** (W3) :

- **garder `--tagger` opt-in** : le défaut hors ligne reste l'heuristique ; l'option gagne en
  agrégé sur le 402 et sur H50 ;
- **ou tester un hybride** « fermé → heuristique, ouvert → tagger » : il devrait récupérer le fermé
  du 402 sans perdre l'ouvert, mais il perdrait une partie du fermé de H50 (le tagger y est
  meilleur) ; c'est une mesure de W3, pas de W2.

**La règle H50-only, elle, est tranchée** : le tagger n'est pas dans ce cas. Un candidat qui
n'aurait que le gain H50 (delta 402 = 0) serait rejeté, même avec +17,65 sur H50.

## 5. Contrôles négatifs

| contrôle | attente | résultat |
|---|---|---|
| **hasard, 402** | le tagger doit être très au-dessus | classe majoritaire **0,2374** (VERB), uniforme **0,0955** ; tagger **0,9643** |
| **hasard, H50** | idem | majoritaire **0,2198** (PRON), uniforme **0,0867** ; tagger **0,8607** |
| **hasard, tirage** | idem | majoritaire **0,2298** (VERB), uniforme **0,0847** ; tagger **0,9556** |
| **F1 402** | identique (le tagger ne change que le POS) | **0,8190 → 0,8190** (Δ 0,0000) |
| **attachement 402** | identique | **1,0000 → 1,0000** (Δ 0,0000) |
| **total 452** | retrouver le chiffre publié | **0,9508** contre **0,8891** (D1 : 0,9500 ; écart **0,0008**) |
| **cache après API** | mêmes scores, 0 réseau, 0 token | **oui** (449 hits, 0 token, scores identiques à l'API) |
| **cache avant API** | 0 réseau, 0 token, mais **pas** la mesure du jour | **oui** (399 + 50 hits, scores légèrement différents : 0,9629 / 0,8638) |
| **refus** | aucun refus caché | **0 / 452** |
| **règle** | rejeter un H50-only | le tagger **n'est pas** H50-only (delta 402 +4,45) ; le cas H50-only reste **rejeté** par le code du banc |

**Le contrôle qui compte** est la **non-régression du 402**, pas le gain H50. Le F1 et
l'attachement du 402 sont **inchangés** : le tagger ne fuit pas sur les autres niveaux. Le total
452 **retrouve** le 0,9500 de D1 à **0,0008** près, ce qui recoupe la mesure. La réserve du fermé
est le **signal négatif** de la fiche : elle n'est pas cachée, elle est dans le tableau § 2.1, le
§ 2.3 et le § 4.3.

## 6. Ce qui pourrait rendre ce résultat faux

- **H50 est circulaire** : sélectionné sur les erreurs de l'heuristique, il **surévalue** le gain du
  tagger. Le +17,65 n'est pas une généralisation ; le +4,45 du 402 et le +4,83 du tirage sont les
  chiffres « normaux ».
- **Les 4 cibles GP/SUB de H50 ne sont pas annotées** : l'attachement de H50 porte sur **22**
  cibles, pas 26. Une annotation après cette mesure **contaminerait** le test.
- **Le 402 est l'entraînement de l'heuristique**, pas du tagger : le tagger est un modèle externe,
  jamais entraîné sur ce gold. Le 402 est un contrôle de non-régression, pas un test du tagger.
- **Pas d'échantillon neuf annoté** : le tirage 20261116 est un contrôle de composition, pas une
  généralisation hors gold. Une généralisation demanderait 50 phrases **neuves**, annotées après
  le gel du split.
- **Le modèle renvoyé** est `deepseek-flash` alors que `deepseek-chat` est demandé ; un changement
  de routage ou de modèle change les scores. Le cache chaud **avant** l'API rejoue un autre moment
  du modèle (0,9629 / 0,8638) : seule la passe API est la mesure du jour.
- **La température 0** n'est pas un déterminisme garanti ; le cache disque fige chaque réponse et
  le rejeu est exact, mais un appel non caché peut différer (c'est visible entre le cache avant et
  la passe API).
- **Le prompt est français** : l'anglais du 402 (185 phrases) est étiqueté par un prompt français ;
  le +0,10 pt du 402 anglais est **1 token**, pas une mesure de tagger anglais.
- **Trois textes dupliqués** dans le 402 (`r019`/`r186`, `r051`/`r189`, `r336`/`r358`) : le tagger
  les sert une fois par cache mémoire ; le coût par phrase est **399 appels / 402 phrases**, pas
  402 appels ; et **2 phrases** (`r423`, `r427`) partagent un prompt, d'où **2 lectures de cache**
  dans la passe API (447 requêtes, pas 449).
- **Le fermé du 402 baisse** : si la règle exige la non-régression **par classe**, le tagger est
  rejeté. C'est la réserve de W3, pas un détail.

## 7. Fichiers et reproduction

- **Cette fiche** : [`reports/rapport-tagger-h50.md`](rapport-tagger-h50.md).
- **JSON** : [`reports/rapport-tagger-h50.json`](rapport-tagger-h50.json) — les trois passes, les
  quatre bases, le détail fermé/ouvert, le coût, la règle, les contrôles.
- **Banc** : [`tools/tests/linguistique/qualifier_tagger_h50.py`](../tools/tests/linguistique/qualifier_tagger_h50.py).
- **Lus, non modifiés** : `tools/tests/linguistique/gold.json`,
  `tools/tests/linguistique/gold_reel.json`, `reports/rapport-gold-452.json`,
  `tools/bloc_linguistique.py`, `tools/drave.py`.
- **Split** : [`reports/rapport-gold-452.md`](rapport-gold-452.md) (W1) ; le split est figé par
  `h50_ids` / `reste_402_ids` dans `reports/rapport-gold-452.json`.

**Reproduire** :

```bash
python3 tools/tests/linguistique/qualifier_tagger_h50.py \
  --mode tous --cache-api /tmp/tagger-h50-api-cache \
  --sortie reports/rapport-tagger-h50.json
```

Le banc lit la clé par l'ordre du CLI (`DEEPSEEK_KEY_FILE`, `~/.config/drave/deepseek.key`,
`DEEPSEEK_API_KEY`) ; il ne l'affiche jamais. Le cache API est **neuf** (le banc le vide en mode
`tous`) ; sans cache neuf, on rejoue un ancien modèle et on ne mesure pas le jour.

## 8. La décision et la suite

1. **La règle est satisfaite** : le tagger gagne sur **402** (+4,45) et sur **H50** (+17,65), le F1
   et l'attachement du 402 sont inchangés. Il **n'est pas H50-only** ; il n'est pas rejeté.
2. **La réserve du fermé** est portée à W3 : le défaut **reste hors ligne** tant que la décision
   n'est pas prise ; `--tagger` reste **opt-in**. W3 teste la matrice défaut / clé absente / clé
   invalide / réseau coupé, le coût pour 1 000 phrases et, si le temps le permet, l'hybride
   fermé/ouvert.
3. **S** doit annoter les **4 cibles GP/SUB de H50** (`r324`, `r328`, `r349`, `r363`) avant que H50
   ne devienne un **test** ; le dénominateur passerait de **22 à 26** cibles et le total de **184 à
   194**. La mesure W2 est **avant** cette annotation, et le dit.
4. **Ne pas publier +17,65 seul** : le chiffre de la tenue à l'écart est un **stress test** ; le
   chiffre de la décision est le **402** (+4,45) et le **total 452** (+6,17).
