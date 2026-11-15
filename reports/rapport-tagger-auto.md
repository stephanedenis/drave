# Y1 — le prototype du mode `auto` du tagger : l'API si la clé existe, l'heuristique sinon, sans changer le code de sortie

> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **Y1** (J5, la décision
> du tagger) · **Date** : 2026-11-15 · **HEAD mesuré** : `f63ad709` + ce diff · **Verdict** :
> ✅ **le prototype est mesuré** — clé présente → API, **code 0**, **130 tokens** ; clé
> invalide → heuristique, **code 0** (pas 4), `refus` explicite ; clé absente → heuristique,
> **code 0**, **sortie identique au défaut octet pour octet** ; clé + réseau coupé →
> heuristique, **code 0** après **3 essais** ; refus de texte → **code 3**, **aucun appel API**.
> **30/30 tests**. **Recommandation** : garder le **défaut heuristique hors ligne** et
> `--tagger auto` comme **prototype opt-in**, jamais comme défaut. **La décision reste à
> l'humain** : ce diff ne change pas le défaut.

**En trois lignes.** (1) `analyser --tagger auto` choisit la voie : si `_cle_tagger()` trouve
une clé (fichier ou environnement), il construit la cascade API ; sinon il ne construit même
pas le client réseau et rend l'heuristique. (2) Le **code de sortie ne change pas** : **0**
dans les deux cas, **3** pour un refus de texte, jamais **4** — le 4 reste réservé à
`--tagger` **explicite**. (3) `stderr` dit **laquelle a servi** (`API (clé présente)` ou
`heuristique (clé absente)` ou `heuristique (repli : …)`), sans jamais nommer la clé ; la
ligne `TAGGER API` porte le coût quand l'API a été tentée.

**Ce que cette fiche est, et n'est pas.**

- **Est** : le **contrat** du prototype, la **matrice des quatre cas** de la tâche, les
  **sorties réelles** (CLI en sous-processus, clé jamais affichée), le **contrôle négatif**
  auto / explicite, et la **recommandation** à l'humain. Les mesures réelles utilisent la clé
  de `~/.config/drave/deepseek.key`, un cache neuf par cas et un endpoint fermé pour le réseau.
- **N'est pas** : un changement de **défaut** (il reste l'heuristique, CPU, hors ligne,
  déterministe), une nouvelle mesure de **qualité** (W2 la porte : 402 **0,9198 → 0,9643**,
  H50 **0,6842 → 0,8607**), ni un run de **1 000 phrases**. Le mode `auto` n'est pas livré
  comme défaut ; il est livré comme **porte explicite**.
- **Public** : **J5** (la décision du tagger), **R0.7/B13**, et toute machine qui hésite entre
  une clé disponible et un fonctionnement hors ligne.

## 1. Le contrat du prototype

```bash
python3 tools/drave.py analyser "Le chat dort." --tagger auto
python3 tools/drave.py analyser "Le chat dort." --tagger auto --json
python3 tools/drave.py analyser --fichier corpus.txt --jsonl --tagger auto
```

**La sélection.** `auto` appelle `_cle_tagger()`, qui lit dans cet ordre :
`DEEPSEEK_KEY_FILE`, `DSH_KEY_FILE`, `~/.config/drave/deepseek.key`, `DEEPSEEK_API_KEY`,
`DSH_API_KEY`. Si une clé est trouvée, la cascade API est construite ; sinon le module réseau
n'est **pas importé** et `Heuristique.analyser` est appelé directement. La clé n'est jamais
affichée, ni dans le message, ni dans le JSON, ni dans le cache ; `_sans_secret` retire la clé
d'un message de diagnostic si elle y apparaissait par accident.

**Le choix de la voie, dans la sortie.**

| voie | `source` | `stderr` | ligne `TAGGER API` |
|---|---|---|---|
| **API** (clé présente, cascade appelée) | `cascade` | `drave: tagger auto · API (clé présente)` | oui : `appels=1 · réseau=1 · tokens=130 …` |
| **API disponible mais non appelée** (tous les niveaux au-dessus du seuil 0,60) | `cascade` ou `heuristique` selon la cascade | `drave: tagger auto · API disponible (clé présente) ; non appelée (heuristique suffisante)` | oui, avec `appels=0` |
| **heuristique sans clé** | `heuristique` | `drave: tagger auto · heuristique (clé absente)` | non : aucun appel, aucun coût |
| **repli** (clé refusée, réseau, modèle) | `heuristique` | `drave: tagger auto · heuristique (repli : …)` | oui : l'appel a été tenté (`appels=1`, `tokens=0`) |
| **refus de texte** | `heuristique` | `drave: tagger auto · heuristique (clé présente ; refus du texte, aucun appel)` | non : aucun appel |

**Les codes de sortie.** `auto` ne change pas le contrat du défaut : **0** si une annotation
est rendue (API ou heuristique), **3** si le texte est refusé (vide ou sans lettre/chiffre),
**2** pour une erreur d'usage. Il ne sort **jamais 4** : une clé refusée ou un réseau coupé
sont des **replis** visibles dans `refus` et `stderr`, pas un arrêt du run. Le code **4** reste
réservé à `--tagger` explicite, où l'utilisateur a demandé le tagger.

**Le périmètre.** Le prototype couvre `analyser` (y compris `--jsonl`). `evaluer --tagger auto`
n'est pas implémenté : la commande rend un **code 2** d'usage et le dit sur `stderr`.

## 2. La matrice des quatre cas

Les quatre lignes de la tâche sont mesurées en **sous-processus réels** ; les deux contrôles
sont la même mesure avec `--tagger` explicite. Le texte est `« Le chat dort. »` (3 tokens ;
l'heuristique donne DET/NOUN/VERB). Les durées sont murales, sur la machine de mesure.

| cas | commande | code | `stdout` | `stderr` / JSON | test |
|---|---|---:|---|---|---|
| **clé présente** | `analyser "Le chat dort." --tagger auto --json`, cache neuf | **0** | 6 117 octets, `source=cascade`, POS `neuronal` | `TAGGER API · appels=1 · réseau=1 · tokens=130 · latence=1.4 s` puis `tagger auto · API (clé présente)` | `TestTaggerAuto.test_auto_cle_presente_api` |
| **clé invalide** (HTTP 401) | même commande, `DEEPSEEK_KEY_FILE=<clé-invalide>`, cache neuf | **0** | 5 904 octets, `source=heuristique`, POS `heuristique` | `tagger : refus partiel : tagger auto : clé refusée (HTTP 401) ; heuristique` ; `TAGGER API · appels=1 · réseau=0 · tokens=0` ; `tagger auto · heuristique (repli : clé refusée (HTTP 401))` | `TestTaggerAuto.test_auto_cle_invalide_code_0_pas_4` |
| **clé absente** | même commande, `HOME` vide, aucun `DEEPSEEK*`/`DSH*` | **0** | **5 852 octets, identique au défaut octet pour octet** ; `source=heuristique`, `refus=""` | `tagger auto · heuristique (clé absente)` ; pas de ligne `TAGGER API` | `TestTaggerAuto.test_auto_sans_cle_identique_au_defaut` |
| **clé + réseau coupé** | même commande, `DEEPSEEK_BASE_URL=http://127.0.0.1:9`, cache neuf | **0** | 5 950 octets, `source=heuristique`, POS `heuristique` | `tagger : refus partiel : tagger auto : neuronal-pos: ErreurDeepSeek: réseau : [Errno 111] Connection refused ; heuristique` ; `TAGGER API · appels=1 · réseau=0 · tokens=0` ; `tagger auto · heuristique (repli : … réseau …)` | `TestTaggerAuto.test_auto_reseau_coupe_code_0` |
| **refus de texte** | `analyser "... !!! ???" --tagger auto --json`, clé présente | **3** | 342 octets, `refus="vide"` | `tagger auto · heuristique (clé présente ; refus du texte, aucun appel)` | `TestTaggerAuto.test_auto_refus_texte_code_3` |
| **contrôle : `--tagger` explicite, clé invalide** | même clé, `--tagger` | **4** | **0 octet** | `dépendance absente : clé DeepSeek refusée (HTTP 401) …` | `TestErreursTagger.test_cle_invalide_code_4` |
| **contrôle : `--tagger` explicite, réseau coupé** | même endpoint, `--tagger` | **0** | 6 253 octets, `source=cascade`, POS `heuristique` | `refus partiel : neuronal-pos: … réseau …` ; pas de message `auto` | `TestErreursTagger.test_reseau_coupe_repli_heuristique` |

**Deux familles, une frontière nette.** Une **clé absente** n'est pas une erreur en `auto` :
c'est le **défaut**, et la sortie le dit. Une **clé refusée** ou un **réseau coupé** sont des
**replis** : l'analyse est rendue par l'heuristique, `source=heuristique`, `refus` porte la
cause, et le code reste **0**. Le **4** n'apparaît que si l'utilisateur a écrit `--tagger`
**sans** `auto` : c'est la seule porte où la dépendance manquante arrête le run.

## 3. Les mesures

### 3.1 Clé présente : API, code 0, 130 tokens

```
$ python3 tools/drave.py analyser "Le chat dort." --tagger auto
drave 0.1.0 — analyse cascade POS (tagger auto : API DeepSeek, réseau)
langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.55 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
TAGGER API  modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=1.3 s

$ # stderr
drave: tagger auto · API (clé présente)
```

Le POS est **identique** à celui du défaut (`Le/DET chat/NOUN dort/VERB ./PONCT`) et à celui de
`--tagger` : `auto` ne change pas la **qualité** de la phrase, il choisit seulement la **voie**.
La ligne `TAGGER API` montre le coût : **1 appel**, **130 tokens** (116 d'entrée + 14 de
sortie), **1,3 s** de latence. Le modèle demandé est `deepseek-chat`, le modèle renvoyé
`deepseek-flash` (comme W2/W3).

### 3.2 Clé invalide : repli heuristique, code 0, pas 4

```
$ DEEPSEEK_KEY_FILE=<clé-invalide> python3 tools/drave.py analyser "Le chat dort." --tagger auto --json
code 0 · stdout 5 904 octets · 0,704 s
stderr : drave: tagger : refus partiel : tagger auto : clé refusée (HTTP 401) ; heuristique
         drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · cache=0 · tokens=0 · latence=0.0 s
         drave: tagger auto · heuristique (repli : clé refusée (HTTP 401))
JSON   : source=heuristique · refus="tagger auto : clé refusée (HTTP 401) ; heuristique"
         POS : Le/DET chat/NOUN dort/VERB ./PONCT · toutes les étiquettes POS ont source="heuristique"
```

C'est le **contrôle négatif principal** : la **même** clé invalide, avec `--tagger` explicite,
sort **4** et `stdout` reste vide. `auto` ne transforme donc pas un 4 en 0 par accident : il
choisit explicitement le repli parce que la clé n'est pas utilisable. La clé temporaire
`sentinelle` n'apparaît ni dans `stdout` ni dans `stderr` (test dédié).

### 3.3 Clé absente : le défaut, octet pour octet

```
$ env -i HOME=<vide> PATH=$PATH python3 tools/drave.py analyser "Le chat dort." --tagger auto --json
code 0 · stdout 5 852 octets · source=heuristique · refus="" · 0,228 s
stderr : drave: tagger auto · heuristique (clé absente)
```

Le JSON est **exactement** `Heuristique().analyser("Le chat dort.").json()`, et la sortie
lisible est **exactement** celle de `analyser` sans option (5 852 octets JSON, 593 octets
lisibles). La seule différence est le message `stderr`, exigé par la tâche. Le sous-processus
piège aussi `socket.socket` : `tools.llm.deepseek` n'est **pas importé**, aucune socket n'est
construite. C'est le sens de « comportement identique au défaut sans clé ».

### 3.4 Clé + réseau coupé : 3 essais, puis repli, code 0

```
$ DEEPSEEK_BASE_URL=http://127.0.0.1:9 python3 tools/drave.py analyser "Le chat dort." --tagger auto --json
code 0 · stdout 5 950 octets · 3,303 s (3 essais : 1 s + 2 s)
stderr : drave: tagger : refus partiel : tagger auto : neuronal-pos: ErreurDeepSeek:
         réseau : [Errno 111] Connection refused ; heuristique
         drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · cache=0 · tokens=0 · latence=0.0 s
         drave: tagger auto · heuristique (repli : neuronal-pos: … réseau …)
JSON   : source=heuristique · refus="tagger auto : neuronal-pos: … réseau … ; heuristique"
         POS : toutes les étiquettes POS ont source="heuristique"
```

Le client `DeepSeek` fait **3 essais** (1 s puis 2 s) avant de rendre l'erreur ; la cascade
replie, puis `auto` rend l'heuristique. Le code reste **0** parce que l'analyse est rendue.
La différence avec `--tagger` explicite est **lisible** : explicite garde `source=cascade` et
`refus=neuronal-pos: …` ; `auto` rend `source=heuristique` et `refus=tagger auto : …`, ce qui
permet à un script de distinguer le repli auto d'un succès du tagger.

### 3.5 Refus de texte : code 3, aucun appel

```
$ python3 tools/drave.py analyser "... !!! ???" --tagger auto --json
code 3 · stdout 342 octets · refus="vide"
stderr : drave: tagger auto · heuristique (clé présente ; refus du texte, aucun appel)
```

Même avec une clé présente, un texte sans lettre ni chiffre ne paie **aucun** appel : la
vérification `_mots` est faite avant la construction de la cascade. Le code **3** est celui du
refus d'analyse, pas un code 4 ni un code 0.

### 3.6 Le coût

| poste | valeur |
|---|---:|
| tokens (phrase de 3 tokens) | **130** = 116 entrée + 14 sortie |
| appels / réseau / cache | **1 / 1 / 0** |
| latence de l'appel | **1,3–1,4 s** |
| durée murale (JSON) | **1,673 s** |
| prix hors pointe (tarif W3, 2026-11-13) | **~0,000026 $** |
| prix en pointe | **~0,000052 $** |
| repli clé invalide | **1 appel, 0 réseau, 0 token**, 0,704 s |
| repli réseau coupé | **3 tentatives, 1 appel, 0 token**, 3,303 s |
| sans clé | **0 appel, 0 réseau, 0 token**, 0,228 s |

Le coût est dominé par le **prompt fixe** : 130 tokens pour 3 tokens de texte. Ce n'est pas une
moyenne ; c'est le plancher observé. Le chiffre de référence pour un lot reste l'extrapolation
W3 (**143 870 tokens pour 1 000 phrases** de même longueur moyenne), pas une nouvelle mesure.

## 4. Les contrôles négatifs

| contrôle | ce qui est mesuré | résultat |
|---|---|---|
| **paire auto / `--tagger` sur clé invalide** | même client, même clé, même texte | auto **0** + heuristique + `refus` ; explicite **4** + `stdout` vide : le 0 de auto n'est pas un 4 déguisé |
| **auto sans clé / défaut** | même `HOME` vide, JSON et lisible | **0 / 0**, `stdout` identique octet pour octet ; seule différence : le message `stderr` de auto |
| **socket piégée** | `socket.socket` remplacé par une classe qui lève, auto sans clé | processus **0**, aucune exception, `tools.llm.deepseek` **non importé** |
| **refus de texte / appel API** | texte sans lettre ni chiffre, clé présente | **3**, **0 appel**, `refus="vide"` |
| **réseau coupé auto / explicite** | même endpoint fermé | auto **0** + `source=heuristique` + refus préfixé ; explicite **0** + `source=cascade` + refus neuronal |
| **fuite de clé** | clé sentinelle dans le client, cas invalide et réseau | la sentinelle n'apparaît ni dans `stdout` ni dans `stderr` |

**Le contrôle principal** est la **paire auto / explicite** sur la même clé invalide : il montre
que le code 0 de `auto` est un **choix de repli**, pas une erreur avalée. Le second est la
**socket piégée** : `auto` sans clé ne doit pas importer le module réseau. Les deux passent.

## 5. Ce qui pourrait rendre ces résultats faux

- **Le coût 130 tokens** vaut pour une phrase de **3 tokens** ; il ne se généralise pas. Un lot
  de phrases longues coûte plus, un lot de phrases courtes moins.
- **Le mode auto ne force pas l'API** quand la cascade juge l'heuristique suffisante (seuil
  **0,60**) : sur un texte où tous les niveaux sont au-dessus, l'API est **disponible mais non
  appelée**, et le message le dit (`appels=0`). Ce n'est pas un bug : c'est la règle de la
  cascade, que `auto` ne change pas.
- **La clé invalide réelle** dépend du service : un proxy qui rendrait `400` avec « invalid
  key » suivrait le repli, pas le 4. Le choix est volontaire (le code HTTP est la seule
  autorité), mais il laisse ce cas dehors.
- **Le réseau coupé réel** est une **connexion refusée** (`127.0.0.1:9`), pas un timeout DNS ou
  TLS ; la latence et le nombre d'essais peuvent différer sur un vrai timeout.
- **Les tests n'ouvrent aucun socket** : le transport factice couvre le contrat (JSON, 401,
  réseau, longueur), pas la diversité des réponses réelles.
- **Le cache disque peut masquer une panne** : les mesures utilisent un cache neuf par cas. En
  production, un cache chaud peut rendre une panne invisible.
- **La reproductibilité n'est pas acquise** : le même texte peut rendre un POS différent selon
  que la machine a une clé ou non. C'est précisément pourquoi `auto` n'est **pas** le défaut.
- **`auto` n'est pas testé sur `evaluer`** : le prototype est limité à `analyser`.

## 6. La recommandation — la décision reste à l'humain

**Ce que la mesure montre.** Le prototype tient le contrat : il **choisit** la voie, il **dit**
laquelle a servi, il **ne change pas** le code de sortie, il **ne fuit pas** la clé, et sans
clé il est **exactement** le défaut. Les quatre cas sont couverts, et le 4 reste réservé à
l'option explicite.

**Ce que la mesure ne tranche pas.** Le même texte peut changer de POS et de `source` selon la
machine (clé présente ou non), ce qui casse la **reproductibilité** au niveau du run ; le coût
réel (**130 tokens** au minimum par phrase) n'est pas nul ; et le gain de qualité est déjà
accessible par `--tagger` explicite. Ces trois points sont des **choix de produit**, pas des
mesures.

**Recommandation.** Garder le **défaut heuristique hors ligne** (aucun changement dans ce
diff) et traiter `--tagger auto` comme un **prototype opt-in**, documenté, qui ne devient
**jamais** le défaut tant que l'humain n'a pas tranché la reproductibilité et le coût. Si le
mode est retenu plus tard, il peut rester une **porte explicite** : c'est la seule forme qui
préserve le contrat « sans clé, rien ne change » tout en donnant l'API à qui a une clé.

**Décision.** **Humaine, non appliquée ici.** Le code livré ne change pas le défaut : sans
`--tagger`, la commande reste l'heuristique, CPU, hors ligne, déterministe, **0 socket**.

**Note de lecture.** W3 (§4.2) avait posé les conditions d'un `auto` ; Y1 les **implémente** et
les **mesure**. La phrase « `auto` n'est pas testé : il n'existe pas » de W3 §6 est **datée** du
2026-11-15 matin ; le prototype et ses **30 tests** sont du 2026-11-15 après-midi. La
recommandation de W3 — **défaut hors ligne, tagger en opt-in** — reste celle de cette fiche.

## 7. Fichiers et reproduction

| fichier | rôle |
|---|---|
| [`tools/drave.py`](../tools/drave.py) | `_TaggerAuto`, `_cle_tagger_presente`, `_sans_secret`, `_normaliser_tagger`, `formater_annotation(titre=…)`, le mode `auto` de `cmd_analyser` |
| [`tools/tests/test_tagger_api.py`](../tools/tests/test_tagger_api.py) | **30 tests** ; la classe `TestTaggerAuto` couvre les quatre cas, le refus de texte, le texte après le drapeau et le rejet sur `evaluer` |
| [`reports/rapport-tagger-auto.json`](rapport-tagger-auto.json) | les chiffres bruts de cette fiche (matrice, comparaison sans clé, contrôles, coût) |
| [`reports/rapport-tagger-defaut.md`](rapport-tagger-defaut.md) | W3 : la matrice du tagger, la recommandation de statu quo et les conditions d'un `auto` |
| [`docs/produit/README.md`](../docs/produit/README.md) | § 3.7 : le tagger en option, désormais avec `--tagger auto` |

**Reproduire les tests.** `python3 tools/tests/test_tagger_api.py` — **30 tests**, **0 socket**,
~7 s. L'acceptation de la tâche est `python3 tools/tests/test_tagger_api.py 2>&1 | tail -1`
→ `OK`.

**Reproduire les quatre cas.**

```bash
# 1. clé absente : HOME vide, aucune variable DEEPSEEK*/DSH*
tmp=$(mktemp -d)
env -i HOME="$tmp" PATH="$PATH" python3 tools/drave.py analyser "Le chat dort." --tagger auto --json

# 2. clé présente : cache neuf pour forcer un appel réel
DEEPSEEK_CACHE=$(mktemp -d) python3 tools/drave.py analyser "Le chat dort." --tagger auto --json

# 3. clé invalide : un fichier temporaire, jamais la vraie clé
bad=$(mktemp); printf 'cle-invalide\n' > "$bad"
DEEPSEEK_KEY_FILE="$bad" DEEPSEEK_CACHE=$(mktemp -d) \
  python3 tools/drave.py analyser "Le chat dort." --tagger auto --json

# 4. clé + réseau coupé : connexion refusée réelle
DEEPSEEK_BASE_URL=http://127.0.0.1:9 DEEPSEEK_CACHE=$(mktemp -d) \
  python3 tools/drave.py analyser "Le chat dort." --tagger auto --json
```

**HEAD.** Les mesures réelles ont été prises sur `f63ad709` + ce diff (le mode `auto` est
additif et ne change aucun code de sortie). Le commit de clôture porte le chiffre.
