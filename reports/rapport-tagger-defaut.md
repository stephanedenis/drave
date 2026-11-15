# W3 — la matrice du tagger : le défaut reste hors ligne (code 0), `--tagger` est la seule porte qui peut sortir 4

> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **W3** (semaine 2, J2
> après-midi) · **Date** : 2026-11-15 · **HEAD mesuré** : `3439cb0c` + ce diff (champ de coût
> additif) · **Verdict** : ✅ **la matrice est mesurée** — le **défaut sans clé** rend
> l'heuristique, **code 0**, **0 socket** ; avec clé, **code 0**, **130 tokens** et **1,16 s**
> pour une phrase ; **clé invalide**, **code 4**, `stdout` vide ; **réseau coupé**, **code 0**
> après **3 essais**, repli heuristique explicite. **Coût pour 1 000 phrases** : **143 870
> tokens**, **989 requêtes**, **981,9 s** de réseau, **~0,031 $ hors pointe / ~0,062 $ en
> pointe**. **Recommandation** : garder le **défaut hors ligne** et `--tagger` **opt-in** ; ne
> pas livrer `auto` maintenant, et si `auto` vient, **seulement si la clé existe** et **sans
> changer le code de sortie**. **21/21 tests**.

**En trois lignes.** (1) Le **défaut** ne touche ni la clé, ni le réseau, ni l'API : `analyser`
et `evaluer` sans `--tagger` sortent **0** dans un `HOME` vide, le JSON dit `source=heuristique`,
et un `socket.socket` piégé n'est **jamais** appelé. (2) `--tagger` est la **seule** porte qui
peut sortir **4** : clé absente ou refusée. Un **réseau coupé** ou un **refus du modèle** ne
sortent pas 4 : ils **replient** sur l'heuristique, code **0**, avec la cause dans `refus`.
(3) Le coût du même câblage pour **1 000 phrases** est une **extrapolation linéaire** de la
mesure W2 sur **452** phrases ; le chiffre est le **token** et la **seconde**, le dollar dépend
du tarif du jour.

**Ce que cette fiche est, et n'est pas.**

- **Est** : la **matrice de décision** du tagger (défaut, avec clé, clé invalide, réseau coupé,
  repli), le **coût pour 1 000 phrases**, la **recommandation** et les tests qui verrouillent
  chaque ligne. Les mesures réelles sont des **sous-processus du CLI** ; les tests utilisent un
  **transport factice**, donc **aucun socket**.
- **N'est pas** : une nouvelle mesure de qualité (W2 la porte : 402 **0,9198 → 0,9643**, H50
  **0,6842 → 0,8607**), ni un run **réel** de 1 000 phrases (le coût est extrapolé), ni la
  **décision J5** qui appliquera ou rejettera la recommandation.
- **Public** : **J5** (la décision), **R0.7/B13**, et toute machine qui n'a **pas** de clé.

## 1. La matrice, en une table

Les six premières lignes sont des **mesures réelles** (CLI en sous-processus, cache neuf,
clé jamais affichée). Les deux suivantes sont les **refus du modèle** couverts par les tests :
on ne peut pas les provoquer à volonté sur l'API réelle. La dernière est le **contrat de
calcul** du coût, testé sur un transport factice.

| cas | commande | code | `stdout` | `stderr` / JSON | test |
|---|---|---:|---|---|---|
| **défaut, sans clé** | `analyser "Le chat dort." --json` | **0** | 5 852 octets, `source=heuristique` | vide ; aucun `tagger` | `TestMatriceW3.test_defaut_sans_cle_code_0` |
| **défaut, sans clé** | `evaluer --json` | **0** | 3 165 octets, pas de clé `tagger` | vide | le même test |
| **défaut, zéro socket** | `drave.main(["analyser", …])` avec `socket.socket` piégé | **0** | heuristique | `tools.llm.deepseek` **non importé**, aucune socket construite | `TestMatriceW3.test_defaut_n_ouvre_aucune_socket` |
| **avec clé** | `analyser "Le chat dort." --tagger --json` | **0** | 6 117 octets, `source=cascade`, POS `neuronal` | `TAGGER API · appels=1 · réseau=1 · tokens=130 · latence=1,2 s` | `TestCliAvecTransportFactice.test_analyser_tagger_json` |
| **clé invalide** (401) | `analyser "Le chat dort." --tagger --json` | **4** | **0 octet** | `clé DeepSeek refusée (HTTP 401) …` ; **aucun repli** | `TestErreursTagger.test_cle_invalide_code_4` |
| **réseau coupé** | `analyser "Le chat dort." --tagger --json`, endpoint fermé | **0** | 6 253 octets, `source=cascade`, POS `heuristique` | `refus partiel : … réseau : [Errno 111] Connection refused` ; **3 essais** | `TestErreursTagger.test_reseau_coupe_repli_heuristique` |
| **refus du modèle** (non JSON) | client injecté, contenu `« Je ne peux pas répondre. »` | **0** | annotation heuristique | `refus = « … pas de JSON … »` | `TestErreursTagger.test_refus_du_modele_repli_heuristique` |
| **refus du modèle** (JSON incomplet) | client injecté, `{"pos": ["DET"]}` pour 3 tokens | **0** | annotation heuristique | `refus = « … longueur POS 1 / 3 »` | `TestErreursTagger.test_modele_json_incomplet_repli_heuristique` |
| **coût 1 000 phrases** | `evaluer --tagger --json` (2 phrases identiques, transport factice) | **0** | `cout_pour_1000_phrases` | extrapolation par phrase (×500) | `TestMatriceW3.test_cout_pour_1000_phrases` |

**Deux familles, une frontière nette.** Une **clé absente** ou **refusée** est une **dépendance
manquante** : le run ne commence pas, il sort **4**, `stdout` reste vide, et il ne publie pas un
repli déguisé en cascade. Un **réseau coupé** ou un **refus du modèle** est un refus **par
phrase** : la cascade garde le POS de l'heuristique, porte la cause dans `refus`, et le code
reste **0** parce que l'analyse est rendue. Le **défaut**, lui, ne peut pas sortir 4 : il ne
regarde même pas la clé.

## 2. Le dispositif

- **Mesures réelles** : `python3 tools/drave.py` en sous-processus, `cwd` à la racine, `HOME`
  vide pour le défaut et la clé invalide, `HOME` réel pour la clé valide et le réseau coupé.
  La clé est lue dans `~/.config/drave/deepseek.key` (ou `DEEPSEEK_KEY_FILE` pour la clé
  invalide) et **n'est jamais affichée** ; les messages ne nomment que les trois sources.
- **Caches neufs** : un répertoire `DEEPSEEK_CACHE` vide par cas. La clé valide a coûté **un**
  appel réseau ; le cache de W2 (`/tmp/tagger-h50-api-cache`, **447** fichiers) sert uniquement
  au calcul du coût, pas à la matrice.
- **Réseau coupé réel** : `DEEPSEEK_BASE_URL=http://127.0.0.1:9` avec la clé valide. Le client
  fait **3 essais** (espacés de 1 s puis 2 s), puis rend `ErreurDeepSeek("réseau : …")` ; la
  cascade replie. C'est une **connexion refusée** réelle, pas une simulation DNS.
- **Tests** : `tools/tests/test_tagger_api.py`, **transport factice** injecté, **0 socket**.
  Les cas `réseau`/`refus` passent par le client `DeepSeek` avec `sleep` neutralisé ; le défaut
  et la clé invalide passent par un **sous-processus** (`HOME` vide), donc sans état partagé.
- **Coût** : la base est la passe API de W2 (`reports/rapport-tagger-h50.json`) : **452**
  phrases, **2 480** tokens de gold, **449** appels, **447** requêtes, **65 029** tokens
  (55 572 d'entrée + 9 457 de sortie), **443,813 s** de réseau. On extrapole **linéairement**
  à 1 000 phrases ; on ne relance pas 1 000 phrases (ce serait **~16 min** et un nouvel appel
  facturé pour un chiffre déjà mesuré).

## 3. Les mesures

### 3.1 Le défaut sans clé : code 0, heuristique, zéro socket

| commande | code | `stdout` | `stderr` | clé `tagger` dans le JSON |
|---|---:|---:|---|---|
| `analyser "Le chat dort." --json` | **0** | 5 852 octets | **vide** | absente |
| `evaluer --json` | **0** | 3 165 octets | **vide** | absente |

Le JSON de `analyser` donne `source=heuristique`, `refus=""`, et **aucune** étape `neuronal`
dans la trace. Le test va plus loin : il lance un sous-processus qui **remplace
`socket.socket` par une classe qui lève**, puis exécute `drave.main([...])`. Le processus rend
**0** et `tools.llm.deepseek` n'est **pas** dans `sys.modules` : le défaut ne charge pas le
client réseau et ne construit aucune socket.

**Ce que « hors ligne » veut dire ici.** Ce n'est pas « le réseau est disponible mais on ne
l'utilise pas » : c'est **aucun import du module réseau**, aucune lecture de clé, aucun coût.
Une machine sans clé, sans DNS et sans `~/.config/drave/` peut lancer le défaut.

### 3.2 Avec la clé : code 0, POS neuronal, 130 tokens

| mesure | valeur |
|---|---:|
| code | **0** |
| durée murale | **1,326 s** |
| latence de l'appel | **1,156 s** |
| appels / réseau / cache | **1 / 1 / 0** |
| tokens | **130** = **116** entrée + **14** sortie |
| modèle demandé / renvoyé | `deepseek-chat` / **`deepseek-flash`** |
| POS | `Le/DET chat/NOUN dort/VERB ./PONCT` |
| sources POS | `DET/NOUN/VERB` = **neuronal**, `PONCT` = **heuristique** |

Le `PONCT` est restitué par l'heuristique : le tagger ne reçoit que les mots et les nombres.
La phrase est **courte** (3 tokens) : ses 130 tokens ne sont pas une moyenne, ils montrent
seulement que le chemin avec clé fonctionne et ce qu'il coûte **au minimum** (le prompt fixe).

### 3.3 Clé invalide : code 4, `stdout` vide, pas de repli

```
$ DEEPSEEK_KEY_FILE=/tmp/bad.key drave analyser "Le chat dort." --tagger --json
code 4 · stdout 0 octet · 0,672 s
stderr : drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez
         DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY.
         Sans --tagger, le défaut reste l'heuristique hors ligne.
```

Le contrôle 401/403 est **avant** le repli : une clé refusée n'est pas un refus de phrase. Le
test couvre `analyser` **et** `evaluer`, et vérifie que `stdout` reste **vide** : aucune
métrique n'est publiée, aucun repli heuristique n'est déguisé en cascade. Le message nomme les
trois sources de la clé, jamais sa valeur.

### 3.4 Réseau coupé : 3 essais, puis repli explicite, code 0

```
$ DEEPSEEK_BASE_URL=http://127.0.0.1:9 drave analyser "Le chat dort." --tagger --json
code 0 · stdout 6 253 octets · 3,258 s (3 essais : 1 s + 2 s d'attente)
stderr : drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek:
         réseau : [Errno 111] Connection refused
         drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · tokens=0
JSON   : source=cascade · refus="neuronal-pos: ErreurDeepSeek: réseau : [Errno 111] Connection refused"
         POS : Le/DET chat/NOUN dort/VERB ./PONCT · toutes les étiquettes POS ont source="heuristique"
```

Le **code 0** est celui du repli : l'analyse est rendue, mais le tagger n'a rien rendu. Le
`refus` et `stderr` le disent ; un script qui ne lit que le code de sortie **ne peut pas**
distinguer ce repli d'un succès du tagger. C'est le prix assumé d'un code 0 stable pour le
traitement de corpus, et la raison pour laquelle le **défaut** ne doit jamais dépendre du réseau.

### 3.5 Les refus du modèle : deux formes, même repli

| sortie du modèle | `refus` | code | POS |
|---|---|---:|---|
| `« Je ne peux pas répondre. »` | `neuronal-pos: ValueError: pas de JSON : …` | **0** | heuristique |
| `{"pos": ["DET"]}` (1 classe pour 3 tokens) | `neuronal-pos: ValueError: longueur POS 1 / 3` | **0** | heuristique |

Le contrat `NeuronalLLMPOS` refuse **sans exception** : le JSON reste valide, la cascade garde
l'heuristique, et `refus` nomme le défaut. C'est le même chemin que le réseau, par conception.

### 3.6 Le coût pour 1 000 phrases

La base est la passe API de W2. Le tableau donne le **mesuré** et l'**extrapolé** ; le facteur
est **1000 / 452 = 2,2124**.

| poste | 452 phrases (mesuré) | 1 000 phrases (extrapolé) |
|---|---:|---:|
| appels du tagger | 449 | **993** |
| requêtes réseau | 447 | **989** |
| lectures du cache local | 2 | **4** |
| tokens d'entrée (prompt) | 55 572 | **122 947** |
| tokens de sortie | 9 457 | **20 923** |
| **tokens total** | **65 029** | **143 870** |
| latence réseau | 443,813 s | **981,9 s** (~16 min 22 s) |
| latence par requête | 0,993 s | 0,993 s |
| **prix hors pointe** (entrée miss 0,15 $/M, sortie 0,60 $/M) | **0,0140 $** | **0,0310 $** |
| **prix en pointe** (0,30 $/M, 1,20 $/M) | **0,0280 $** | **0,0620 $** |

**Lecture.** Le coût est dominé par le **prompt** (122 947 tokens d'entrée contre 20 923 de
sortie) : le tagger reçoit la liste des tokens et une consigne, et ne rend qu'une classe par
token. Les **989 requêtes** font **981,9 s** de réseau en séquentiel ; c'est le temps, pas le
prix, qui domine l'usage. Le cache **local** (cache disque du client) rejoue les mêmes réponses
avec **0 réseau** et **0 token** : **~0,14 s** pour 1 000 phrases, **0 $**. C'est le seul mode
qui rend le tagger compatible avec un lot répété.

**Le tarif n'est pas figé.** Les prix ci-dessus sont ceux du **`deepseek-flash` au
2026-11-13** ([tarifs](https://api-docs.deepseek.com/quick_start/pricing)), repris de
[`rapport-coordination-r.md`](rapport-coordination-r.md) § 3.3 : entrée cache hit **0,003 /
0,006 $** par M, entrée cache miss **0,15 / 0,30 $**, sortie **0,60 / 1,20 $** (hors pointe /
pointe). Le run W2 n'a **aucun** cache hit côté API (`prompt_cache_hit_tokens = 0`) : tous les
tokens d'entrée sont facturés au tarif **miss**. Un changement de modèle, de routage ou de
tarif déplace le dollar, pas les **143 870 tokens**.

**Une phrase, pour l'échelle.** L'appel réel de § 3.2 a coûté **130 tokens** (116 entrée +
14 sortie), soit **~0,000026 $ hors pointe** (**~0,000052 $ en pointe**) et **1,156 s**. Ce
n'est pas un coût moyen : la phrase fait 3 tokens et le prompt fixe pèse l'essentiel.

**Ce que 1 000 phrases ne veut pas dire.** Le gold 452 fait **2 480 tokens** pour **452
phrases**, soit **5,49 tokens/phrase** ; c'est un gold de phrases **courtes**. Le coût par
phrase est proportionnel à la longueur du texte (le prompt la porte) : 1 000 phrases de 20
tokens coûteront plus que 143 870 tokens. Le chiffre est donc **143 870 tokens pour 1 000
phrases de même longueur moyenne que le gold 452**, pas une constante universelle.

## 4. La recommandation

### 4.1 Ce qui est recommandé

1. **Le défaut reste hors ligne.** Aucune clé, aucun réseau, **code 0**, heuristique,
   déterministe, **0 socket**. C'est le seul défaut qui marche sur une machine sans compte,
   sans DNS et sans `~/.config/drave/`.
2. **`--tagger` reste opt-in.** C'est la seule porte qui peut sortir **4** (clé absente ou
   refusée) et la seule qui coûte des tokens. L'utilisateur qui la pose accepte le réseau, le
   coût et le repli.
3. **Pas de `auto` maintenant.** Un mode `auto` rendrait le **même texte** différent selon la
   machine (clé présente ou non), donc la reproductibilité et le coût deviendraient
   dépendants de l'environnement. Le gain de qualité est déjà accessible par un drapeau
   explicite ; le coût et le repli sont mesurés ; rien ne presse.

### 4.2 Si `auto` vient un jour

Le mode `auto` ne doit pas être un second défaut déguisé. Les conditions, dans l'ordre :

- **clé présente** : `auto` ne s'active que si `_cle_tagger()` trouve une clé. Sans clé, il se
  comporte **exactement** comme le défaut : **code 0**, heuristique, **0 socket**, aucun
  message d'erreur.
- **sans changer le code de sortie** : une clé **invalide** ou un **réseau coupé** en `auto`
  ne doit **pas** sortir 4 ; il replie sur l'heuristique, code **0**, avec `refus` et un
  message sur `stderr`, comme le réseau coupé de § 3.4. Le code 4 reste réservé à
  `--tagger` **explicite**, où l'utilisateur a demandé le tagger.
- **pas de coût caché** : `auto` doit annoncer le coût sur `stderr` (la ligne `TAGGER API`
  existe déjà) et ne doit pas être le défaut global. Un utilisateur qui ne veut pas payer
  garde le défaut hors ligne.
- **un test par issue** : sans clé → 0 heuristique ; clé invalide → 0 heuristique + `refus` ;
  réseau coupé → 0 heuristique + `refus` ; clé valide → 0 cascade. Le test doit lancer la
  **même** commande dans les quatre environnements et vérifier le **code** à chaque fois.

**Décision W3** : **statu quo** — défaut hors ligne, `--tagger` opt-in, pas de `auto`. J5 peut
appliquer cette recommandation sans changer le code ; si la semaine 2 veut `auto`, il faudra
d'abord un run **réel** de 1 000 phrases et un besoin utilisateur nommé.

### 4.3 Pourquoi ne pas rendre le tagger par défaut

- **La qualité n'est pas uniforme.** W2 : le tagger gagne **+4,45 pts** sur 402 et **+17,65**
  sur H50, mais il **perd 1,55 pt sur le fermé du 402** (PREP −8,43, CONJ −10,15). Un défaut
  qui échange un peu de fermé contre de l'ouvert est un **choix**, pas une évidence ; l'opt-in
  laisse le choix à l'utilisateur et garde la réserve nommée.
- **Le prix et la latence.** **143 870 tokens** et **~16 min** pour 1 000 phrases : ce n'est
  pas un défaut acceptable pour un CLI qui doit rendre une phrase en quelques millisecondes.
- **La panne.** Le tagger peut être indisponible (clé, réseau, modèle) ; le défaut, non.
- **La reproductibilité.** Deux runs du même texte ne donnent pas exactement le même POS
  (l'API n'est pas déterministe à température 0) ; le cache fige une réponse, mais un cache
  neuf ne la rejoue pas. Le défaut heuristique est déterministe.

## 5. Les contrôles négatifs

| contrôle | ce qui est mesuré | résultat |
|---|---|---|
| **paire défaut / `--tagger`** | même `HOME` vide, même texte | défaut **0** ; `--tagger` **4** : le code 0 du défaut n'est pas un 4 déguisé |
| **avec clé / clé invalide** | même transport, même texte | valide **0** + POS `neuronal` ; invalide **4** + `stdout` vide : le 4 vient bien de la clé |
| **avec clé / réseau coupé** | même client, endpoint fermé | valide **0** + POS `neuronal` ; coupé **0** + POS `heuristique` + `refus` : le repli est visible |
| **socket piégée** | `socket.socket` remplacé par une classe qui lève, défaut lancé | processus **0**, aucune exception, `tools.llm.deepseek` **non importé** |
| **cache chaud / cache neuf** | même run W2, cache local | **0** réseau, **0** token, **0 $** en chaud contre **65 029** tokens en neuf : le coût est le réseau, pas le CPU |
| **mutation 401/403** | retirer `if code: raise CleTaggerRefusee(code)` dans `_CascadeTagger.analyser` | `test_cle_invalide_code_4` **échoue** (`0 != 4`) ; le test détecte le repli muet |
| **extrapolation par phrase** | 2 phrases **identiques** : 1 appel, 17 tokens | `cout_pour_1000_phrases` = **500 appels**, **8 500 tokens** : l'extrapolation suit les **phrases**, pas les appels (la différence 449 / 452 de W2) |

**Le contrôle négatif principal** est la **paire** défaut / `--tagger` : elle montre que le
code 0 du défaut n'est pas obtenu en avalant une erreur de clé. Le second est la **socket
piégée** : un `socket.socket` qui lève rendrait le défaut bruyant si un appel réseau était
caché. Les deux passent.

## 6. Ce qui pourrait rendre ces résultats faux

- **Le coût 1 000 est une extrapolation**, pas un run de 1 000 phrases. La base est 452
  phrases / 2 480 tokens de gold ; des phrases plus longues coûtent plus, des phrases plus
  courtes moins. Le chiffre vaut pour **la même longueur moyenne**.
- **Le tarif change.** Les dollars sont ceux du `deepseek-flash` au 2026-11-13 ; les tokens
  (143 870) sont stables, le prix ne l'est pas. Un cache hit côté API réduirait l'entrée ;
  W2 n'en a **aucun**.
- **Le modèle renvoyé n'est pas celui demandé.** `deepseek-chat` demandé, **`deepseek-flash`**
  renvoyé sur l'appel réel et sur les 447 appels de W2. Un changement de routage change le
  tarif et, à la marge, la qualité.
- **Le réseau coupé réel est une connexion refusée** (`127.0.0.1:9`), pas un timeout DNS ni un
  TLS qui échoue. Le client enveloppe les trois en `ErreurDeepSeek("réseau : …")`, mais la
  latence et le nombre d'essais peuvent différer sur un vrai timeout (120 s par essai).
- **Les tests ne touchent pas le réseau.** Le transport factice couvre le contrat (JSON, 401,
  réseau, longueur), pas la diversité des réponses réelles. La mesure réelle de § 3.2 couvre
  **une** phrase.
- **Le cache peut masquer une panne.** Un cache disque déjà rempli sert une réponse ancienne
  sans réseau ; les tests utilisent un cache vide par cas. En production, un cache chaud peut
  rendre une panne invisible : c'est le comportement documenté du cache, pas une erreur.
- **401/403 seulement.** Un proxy qui rend `400` avec « invalid key » suivrait le **repli**,
  pas le code 4. Le choix est volontaire (le code HTTP est la seule autorité), mais il laisse
  ce cas dehors.
- **Le code 0 du repli n'est pas un feu vert.** Il dit « l'analyse est rendue », pas « le
  tagger a fonctionné ». Un script qui ne lit que le code doit lire aussi `refus` (ou
  `stderr`).
- **`--jsonl`** : le code 4 peut arriver après des lignes déjà écrites ; les mesures portent
  sur `analyser` avec **un** texte.
- **`auto` n'est pas testé** : il n'existe pas. Les conditions du § 4.2 sont une
  recommandation, pas un contrat livré ; le jour où `auto` existe, il lui faudra ses quatre
  tests.

## 7. Fichiers et reproduction

| fichier | rôle |
|---|---|
| [`tools/drave.py`](../tools/drave.py) | le tagger opt-in, `_cout_pour_phrases`, le champ `cout_pour_1000_phrases` dans `evaluer --tagger --json` |
| [`tools/tests/test_tagger_api.py`](../tools/tests/test_tagger_api.py) | **21 tests** : matrice W3 (défaut 0, zéro socket, coût 1 000), cas d'erreur, cascade, clé |
| [`reports/rapport-tagger-defaut.json`](rapport-tagger-defaut.json) | les chiffres bruts de cette fiche (matrice, coût, contrôles) |
| [`reports/rapport-tagger-h50.md`](rapport-tagger-h50.md) | la mesure de qualité et le coût 452 qui sert de base |
| [`reports/rapport-tagger-erreurs.md`](rapport-tagger-erreurs.md) | les quatre cas d'erreur et la règle des deux familles |
| [`reports/rapport-tagger-option.md`](rapport-tagger-option.md) | l'option `--tagger`, sa clé et son cache |

**Reproduire les tests.** `python3 tools/tests/test_tagger_api.py` — **21 tests**, **0
socket**, ~5 s.

**Reproduire la matrice réelle.** Les commandes du § 3 ; pour le défaut, un `HOME` vide suffit :

```bash
tmp=$(mktemp -d)
env -i HOME="$tmp" PATH="$PATH" python3 tools/drave.py analyser "Le chat dort." --json
env -i HOME="$tmp" PATH="$PATH" python3 tools/drave.py evaluer --json
```

**Reproduire le coût.** `python3 tools/drave.py evaluer --tagger --json` publie
`tagger.cout_pour_1000_phrases` (extrapolation du run mesuré) ; le chiffre de référence de
cette fiche reste la passe W2 de 452 phrases, pas un nouveau run de 1 000.

**HEAD.** Les mesures réelles ont été prises sur `3439cb0c` + ce diff (le champ de coût est
additif et ne change aucun code de sortie). Le commit de clôture porte le chiffre.
