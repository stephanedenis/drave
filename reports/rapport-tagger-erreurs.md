# E2 — les cas d'erreur de `--tagger` : clé refusée = code 4, réseau et refus du modèle = repli heuristique

> **Ligne de roadmap** : **B13** (le produit) · **Tâche** : **E2** · **Date** : 2026-11-15 ·
> **Verdict** : ✅ **4/4 cas caractérisés**, **18/18 tests**, **0 socket**.
> **La clé invalide (HTTP 401/403) sort désormais 4** avec un message clair et **rien sur
> `stdout`** ; avant, elle était avalée par le tagger et le CLI rendait **0** avec un repli
> heuristique déguisé en cascade. Le **réseau coupé** (3 essais du client) et le **refus du
> modèle** restent des refus **par phrase** : repli heuristique, code **0**, cause dans `refus`.
> **Dispositif** : [`tools/drave.py`](../tools/drave.py) 0.1.0, client `DeepSeek` injecté,
> transport factice, cache temporaire vide, aucun socket. **Contrôle négatif** : un transport
> valide donne code 0 et des POS neuronaux ; la mutation qui retire le contrôle 401/403 fait
> échouer le test (`0 != 4`). **JSON** : [`rapport-tagger-erreurs.json`](rapport-tagger-erreurs.json).

## 1. Les quatre cas

Le tableau dit le comportement **du code courant**, pas l'intention. Chaque ligne a son test
dans [`test_tagger_api.py`](../tools/tests/test_tagger_api.py), avec un transport factice.

| cas | ce que fait le CLI | code | `stdout` | `stderr` / JSON | test |
|---|---|---:|---|---|---|
| **clé absente** | refuse de démarrer | **4** | vide (0 octet) | `drave: dépendance absente : clé DeepSeek absente …` | `TestCle.test_sans_cle_code_4` |
| **clé invalide** (HTTP 401/403) | refuse de démarrer, **sans repli** | **4** | vide (0 octet) | `drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.` | `TestErreursTagger.test_cle_invalide_code_4` |
| **réseau coupé** (après 3 essais) | **replie** sur l'heuristique | **0** | annotation heuristique | `drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek: réseau : …` ; `refus` non vide, POS `source=heuristique` | `TestErreursTagger.test_reseau_coupe_repli_heuristique` |
| **refus du modèle** (texte non JSON, JSON incomplet) | **replie** sur l'heuristique | **0** | annotation heuristique | `drave: tagger : refus partiel : neuronal-pos: ValueError: …` ; `refus` non vide, POS `source=heuristique` | `TestErreursTagger.test_refus_du_modele_repli_heuristique`, `test_modele_json_incomplet_repli_heuristique` |

**Deux familles.** Une **clé absente** ou **refusée** est une **dépendance manquante** : le run
ne peut pas commencer, il sort **4**, rien sur `stdout`, et il ne publie pas un repli déguisé en
cascade. Un **réseau coupé** ou un **refus du modèle** est un refus **par phrase** : la cascade
garde le POS de l'heuristique, porte la cause dans `refus`, et le JSON reste valide ; le code
reste **0** parce que l'analyse, elle, est rendue.

**Le champ `source`.** Dans le repli, l'annotation garde `source: "cascade"` (la cascade a bien
été appelée), mais **toutes les étiquettes POS portent `source: "heuristique"`** : c'est
`refus` qui dit que le tagger n'a rien rendu. Les deux champs se lisent ensemble ; `source` seul
mentirait.

## 2. Le dispositif

- **CLI en processus** : `drave.main([...])` avec `drave._client_tagger` remplacé par un client
  `DeepSeek` dont le **transport** est une fonction factice. Aucun DNS, TLS ou HTTP réel ; le
  test « clé absente » lance la commande dans un `HOME` vide.
- **Trois formes de panne** : `ErreurDeepSeek("HTTP 401 …", code=401)` pour la clé refusée ;
  `ErreurDeepSeek("réseau : …", reessayable=True)` pour le réseau (le client réessaie **3 fois**
  avec `sleep` neutralisé) ; un contenu `"Je ne peux pas répondre."` ou `{"pos": ["DET"]}` pour
  le refus du modèle.
- **Cache temporaire vide** par cas : aucune réponse d'un run précédent ne peut masquer la
  panne. La clé factice `cle-de-test-sentinelle` sert de sentinelle de fuite.
- **Texte** : `« Le chat dort. »` (3 tokens, POS heuristique DET/NOUN/VERB). Le gold n'est pas
  utilisé : on mesure des **codes de sortie** et des **contrats de sortie**, pas une qualité.
- **Coût** : **0 token**, **0 requête réseau**, **0 $**. Le coût affiché par le CLI
  (`appels=1 · réseau=0 · tokens=0`) compte les appels du tagger, pas les 3 tentatives internes
  du client réseau.

## 3. Les mesures

### 3.1 Clé absente et clé invalide — code 4, `stdout` vide

| commande | code | `stdout` | message |
|---|---:|---:|---|
| `analyser "Le chat dort." --tagger --json`, sans clé | **4** | 0 octet | `clé DeepSeek absente : exportez DEEPSEEK_KEY_FILE, déposez la clé dans ~/.config/drave/deepseek.key, ou exportez DEEPSEEK_API_KEY.` |
| `analyser "Le chat dort." --tagger --json`, clé 401 | **4** | 0 octet | `clé DeepSeek refusée (HTTP 401) : vérifiez DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY.` |
| `evaluer --tagger --json`, clé 401 | **4** | 0 octet | le même message ; aucune métrique n'est publiée |

**La clé invalide avant/après.** Avant, `NeuronalLLMPOS.analyser` attrapait l'`ErreurDeepSeek`
comme un refus de phrase : le CLI rendait **0**, publiait l'annotation heuristique avec
`source=cascade`, et `evaluer` rendait `refus: N`, `delta_pos: 0`. C'était un **repli muet** :
le code de sortie ne distinguait pas « le tagger a refusé cette phrase » de « la clé est
refusée ». Le contrôle 401/403 est maintenant retenu dans `stats["cle_refusee"]`,
`_CascadeTagger.analyser` lève `CleTaggerRefusee`, et `main` rend **4**.

### 3.2 Réseau coupé — 3 essais, puis repli

```
$ drave analyser "Le chat dort." --tagger --json        # transport réseau qui échoue
code 0
stderr: drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek: réseau : [Errno -2] Name or service not known
        drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · cache=0 · tokens=0 · latence=0.0 s
JSON  : source=cascade · refus="neuronal-pos: ErreurDeepSeek: réseau : [Errno -2] Name or service not known"
        POS : Le/DET chat/NOUN dort/VERB ./PONCT · toutes les étiquettes POS ont source="heuristique"
```

**Les 3 essais** sont ceux de `DeepSeek.demande` (`essais=3`, `reessayable=True`). Le transport
factice est appelé **3 fois** ; `stats["appels"]` reste à **1** (un appel du tagger, trois
tentatives HTTP). Le repli est **explicite** : `refus` est non vide, `stderr` le dit, et les POS
restent heuristiques.

### 3.3 Refus du modèle — deux formes, même repli

| sortie du modèle | `refus` | code | POS |
|---|---|---:|---|
| `"Je ne peux pas répondre."` | `neuronal-pos: ValueError: pas de JSON : 'Je ne peux pas répondre.'` | **0** | heuristique |
| `{"pos": ["DET"]}` (1 classe pour 3 tokens) | `neuronal-pos: ValueError: longueur POS 1 / 3` | **0** | heuristique |

Le contrat `NeuronalLLMPOS` refuse **sans exception** : le JSON reste valide, la cascade garde
l'heuristique, et `refus` nomme le défaut. C'est le même chemin que le réseau, par conception.

### 3.4 `evaluer --tagger`

- **Clé refusée** : code **4**, `stdout` vide, message identique à `analyser` ; aucune métrique
  n'est publiée.
- **Réseau ou refus du modèle** : code **0**, `tagger.refus = N`, `refus_detail` donne les
  identifiants, `delta_pos = 0`, et les métriques du tagger sont **égales à l'heuristique**
  (le repli). La sortie lisible ajoute la ligne `REFUS N phrase(s) (JSON partiel)`.

## 4. Les contrôles négatifs

| contrôle | ce qui est mesuré | résultat |
|---|---|---|
| **tagger valide** | un transport qui rend `{"pos":["DET","NOUN","VERB"]}` | code **0**, `refus=""`, POS `source=neuronal` (sauf PONCT, heuristique) : les cas d'erreur ne sont pas un « tout échoue » |
| **mutation du contrôle 401/403** | retirer `if code: raise CleTaggerRefusee(code)` dans `_CascadeTagger.analyser` | `test_cle_invalide_code_4` **échoue** : `0 != 4` ; le test détecte bien le repli muet |
| **fuite de clé** | `cle-de-test-sentinelle` dans `stdout` + `stderr` | **absente** des deux ; le message nomme les variables, jamais la valeur |
| **défaut inchangé** | `analyser --json` sans `--tagger` | JSON **identique** à l'heuristique (`TestDefaultInchange.test_analyser_json_sans_tagger`) |

**Le contrôle négatif principal** est la mutation : sans elle, un test qui vérifie seulement
« code 4 » pourrait passer pour la mauvaise raison (par exemple une clé absente). Ici, la
mutation rétablit exactement l'ancien comportement et le test échoue.

## 5. Ce qui pourrait rendre ces résultats faux

- **Le transport factice ne teste pas le réseau réel** : DNS, TLS, proxy et coupure de socket
  peuvent produire d'autres exceptions (`TimeoutError`, `ConnectionResetError`) que
  `DeepSeek._http` enveloppe en `ErreurDeepSeek("réseau : …", reessayable=True)`. Le repli
  couvre ces cas, mais le **nombre d'essais** et la latence réels ne sont pas mesurés ici.
- **401/403 seulement** : un proxy qui rend `400` avec « invalid key » dans le corps suivrait
  le **repli**, pas le code 4. Le choix est volontaire (le code HTTP est la seule autorité),
  mais il laisse ce cas dehors.
- **Le refus du modèle est simulé** : un vrai modèle peut refuser autrement (contenu vide,
  contenu tronqué, classe hors jeu, JSON valide mais sémantiquement faux). Les deux formes
  testées couvrent le contrat, pas la diversité des refus.
- **Le cache peut masquer une panne** : avec un cache disque déjà rempli, une réponse ancienne
  est servie sans réseau ; le test utilise un cache vide par cas. En production, le cache peut
  donc rendre une panne invisible — c'est le comportement documenté du cache, pas une erreur.
- **Le code 0 du repli n'est pas un feu vert** : il dit « l'analyse est rendue », pas « le
  tagger a fonctionné ». Un script qui ne lit que le code de sortie doit lire aussi `refus`
  (ou `stderr`) pour distinguer les deux.
- **`--jsonl`** : le code 4 peut arriver après des lignes déjà écrites (le premier texte sans
  appel neuronal ne déclenche pas le 401) ; les mesures ci-dessus portent sur `analyser` avec
  **un** texte.

## 6. Fichiers

| fichier | rôle |
|---|---|
| [`tools/drave.py`](../tools/drave.py) | `CleTaggerRefusee`, drapeau `cle_refusee`, contrôle 401/403, code 4 dans `main` |
| [`tools/tests/test_tagger_api.py`](../tools/tests/test_tagger_api.py) | 18 tests, dont les 4 cas d'erreur et le JSON incomplet |
| [`docs/produit/README.md`](../docs/produit/README.md) § 3.7 | le tableau des cas, la règle des deux familles, le code 4 élargi |
| [`reports/rapport-tagger-erreurs.json`](rapport-tagger-erreurs.json) | les mesures brutes (codes, `stdout`, `refus`, contrôles) |

**Reproduire.** `python3 tools/tests/test_tagger_api.py` — 18 tests, aucun socket. Les mesures
du JSON ont été prises sur le **HEAD `7d4e3bc5`** plus ce diff, avec `drave 0.1.0` et le schéma
d'annotation **v2**.
