# T3 — le démarrage en 5 minutes : clone public, installation, trois commandes, JSON, tagger, erreurs

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T3** (exploitable, 3/5) ·
> **Date** : 2026-11-15 · **Verdict** : ✅ **quickstart livré et rejoué** ; ⚠️ le **clone
> public** n'a pas le sous-module `tools/structures`, donc la sortie d'un débutant est
> **dégradée** par rapport au dépôt de développement. Le document le dit, mesure l'écart et
> donne les deux sorties.
>
> **Le chiffre.** Sur un clone public neuf (commit **7f1519f**, Python **3.13.16**, pip
> **26.2.1**, sans clé) : **3/3 commandes** sortent **0**, le JSON fait **5 899 octets** en
> schéma **v2**, `--tagger` sans clé sort **4**, `--tagger auto` sort **0**, et les **3
> erreurs** rejouées sortent **3 / 4 / 1**. Clone + venv + installation : **13,64 s** de
> machine. Le contrôle négatif « un débutant sans le dépôt » passe pour les commandes, mais
> découvre l'écart du sous-module : `analyser` rend `rôle=objet` / `GV → —` au lieu de
> `agent` / `chat`, et `evaluer` **81,88 %** / **88,70 %** au lieu de **79,02 %** / **99,58 %**.
>
> **Dispositif** : [`docs/produit/demarrage.md`](../docs/produit/demarrage.md),
> [`reports/quickstart.json`](quickstart.json), clone public
> `https://github.com/stephanedenis/drave.git` dans `/tmp/qs-doc/drave`, `HOME=/tmp/qs-doc-home`,
> sans `DEEPSEEK_*`, sans sous-module, sans `data/`.

## 1. Ce qui est livré

Le **quickstart** [`docs/produit/demarrage.md`](../docs/produit/demarrage.md) contient :

1. le **clone** public et le `cd` ;
2. l'**installation T1** : `python3 -m venv .venv`, activation, `python3 -m pip install -e .`,
   `drave --version` ;
3. les **trois commandes** : `drave --version`, `drave analyser "Le chat dort."`,
   `drave evaluer`, avec leurs sorties **réelles** ;
4. le **JSON** : `--json > annotation.json`, l'extrait de 22 lignes, le consommateur Python et
   les huit champs obligatoires ;
5. le **tagger optionnel** : `--tagger` (code 4 sans clé, code 0 avec clé et 130 tokens),
   `--tagger auto` (code 0, repli) ;
6. les **trois erreurs courantes** et leur code, puis le **tableau des codes** 0–4 ;
7. les liens vers la notice, les exemples, le schéma et la fiche.

Les liens sont ajoutés dans [`docs/produit/README.md`](../docs/produit/README.md) (en tête et au
§ 9) et dans [`docs/README.md`](../docs/README.md) (table **Produit**). `.venv/` est ajouté au
[`.gitignore`](../.gitignore) : un débutant qui suit le parcours ne salit pas `git status`.

## 2. Le dispositif

| élément | valeur |
|---|---|
| clone | `https://github.com/stephanedenis/drave.git`, clone complet (sans `--depth`), **commit 7f1519f** |
| répertoire | `/tmp/qs-doc/drave` (hors du dépôt de développement) |
| `HOME` | `/tmp/qs-doc-home` (aucune clé, aucun cache DeepSeek) |
| Python / pip | **3.13.16** / **26.2.1** |
| git | **2.56.0** |
| sous-modules | **aucun** (`tools/docwatch`, `tools/structures` absents) |
| `data/` | **absent** (le corpus UDHR n'est pas versionné) |
| clé DeepSeek | **absente** pour le chemin principal ; une clé réelle a servi au test « avec clé » |

Le parcours a été exécuté **dans l'ordre du document**, avec `source .venv/bin/activate` et
les commandes telles qu'elles sont écrites. Les sorties ont été capturées séparément
(`stdout`, `stderr`, code).

### Les temps mesurés

| étape | commande | temps |
|---|---|---:|
| clone | `git clone https://github.com/stephanedenis/drave.git` | **6,71 s** |
| venv | `python3 -m venv .venv` | **3,58 s** |
| installation | `python3 -m pip install -e .` | **3,35 s** |
| **total machine** | | **13,64 s** |

Le « 5 minutes » est humain : lecture, activation, vérification. La machine fait le reste en
**13,64 s** ; le document est écrit pour tenir en cinq minutes de lecture et d'exécution.

## 3. Les sorties observées

### 3.1 `drave --version`

| commande | cwd | code | `stdout` |
|---|---|---:|---|
| `drave --version` | `/tmp/qs-doc/drave` | **0** | `drave 0.1.0` |

### 3.2 `drave analyser "Le chat dort."`

| commande | cwd | code | `stdout` (extrait) |
|---|---|---:|---|
| `drave analyser "Le chat dort."` | `/tmp/qs-doc/drave` | **0** | `langue=fr`, `GN [0:7] Le chat rôle=objet → dort`, `GV [8:12] dort rôle=predicat → —` |

La sortie complète est dans le document (§ 3.2). Les 20 étiquettes et la ligne `POS` sont
identiques au dépôt de développement ; **deux champs** changent (`role` du GN, `cible` du GV),
à cause du sous-module (§ 4).

### 3.3 `drave evaluer`

| commande | cwd | code | POS | F1 | attachement exact |
|---|---|---:|---:|---:|---:|
| `drave evaluer` | `/tmp/qs-doc/drave` | **0** | **86,25 %** | **81,88 %** | **88,70 %** |

La sortie complète (612 phrases, 239 cibles, base réelle 452, contrôle négatif **1,67 %**) est
dans le document (§ 3.3). Le contrôle négatif est **1,67 %** dans les deux configurations : il
ne dépend pas du sous-module.

### 3.4 Le JSON

```bash
drave analyser "Le chat dort." --json > annotation.json
sed -n '1,22p' annotation.json
```

| mesure | valeur |
|---|---:|
| code | **0** |
| octets | **5 899** |
| `schema` / `version` | `drave.annotation` / **2** |
| étiquettes | **20** |
| syntagmes | `GN Le chat` (`objet`), `GV dort` (`predicat`) |
| consommateur Python | `drave.annotation 2 fr 20 étiquettes` |

Le JSON est **v2** et **additif** : les huit champs obligatoires de la racine sont ceux de la
v1 ; la v1 reste lue. Le schéma est
[`tools/schemas/drave-annotation-v2.json`](../tools/schemas/drave-annotation-v2.json).

### 3.5 Le tagger optionnel

| cas | commande | code | `stdout` | `stderr` |
|---|---|---:|---|---|
| **sans clé, explicite** | `drave analyser "Le chat dort." --tagger` | **4** | vide | `drave: dépendance absente : clé DeepSeek absente …` |
| **sans clé, auto** | `drave analyser "Le chat dort." --tagger auto` | **0** | identique au § 3.2 | `drave: tagger auto · heuristique (clé absente)` |
| **avec clé, explicite** | `drave analyser "Le chat dort." --tagger` | **0** | `source=cascade`, `TAGGER API … réseau=1 · cache=0 · tokens=130 · latence=0.9 s` | vide |
| **avec clé, cache chaud** | le même, seconde fois | **0** | `réseau=0 · cache=1 · tokens=0 · latence=0.0 s` | vide |

La clé n'apparaît ni dans `stdout`, ni dans `stderr`, ni dans le JSON. Le mode `auto` ne change
jamais le code de sortie (0 dans les deux cas) ; le 4 reste réservé à `--tagger` explicite.

### 3.6 Les trois erreurs

| cas | commande | code | `stdout` | `stderr` (extrait) |
|---|---|---:|---|---|
| texte vide | `drave analyser ""` | **3** | vide | `drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)` |
| `--tagger` sans clé | `drave analyser "Le chat dort." --tagger` | **4** | vide | `drave: dépendance absente : clé DeepSeek absente …` |
| `--fichier` inexistant | `drave analyser --fichier absent.txt` | **1** | vide | `drave: erreur : FileNotFoundError : [Errno 2] No such file or directory: 'absent.txt'` |

Avec `--json`, le refus de texte sort un **JSON valide** sur `stdout` (`refus: "vide"`,
`etiquettes: []`) et le code reste **3**. Un répertoire à la place du fichier donne
`IsADirectoryError` et le code **1**. `--langue de` sort **2** (usage) : c'est la ligne 2 du
tableau des codes, pas une des trois erreurs.

## 4. Le contrôle négatif — un débutant sans le dépôt

**Le principe.** On ne part pas du dépôt de développement : on clone le dépôt **public** dans
`/tmp`, avec un `HOME` neuf, sans clé, sans `data/` et **sans les sous-modules**. On suit le
document à la lettre. C'est le débutant « sans le dépôt ».

**Ce qui passe.** Les **3/3 commandes** sortent **0** ; le JSON est produit et consommé ; le
tagger sans clé sort **4** et `auto` sort **0** ; les trois erreurs sortent **3 / 4 / 1**
comme documenté. Le parcours est suivi de bout en bout, sans fichier local.

**Ce que le contrôle découvre.** Le clone public **n'a pas** `tools/structures` : son URL dans
[`.gitmodules`](../.gitmodules) est un **chemin local**
(`/home/stephane/Data13TB/stephane/GitHub/drave-structures`), pas une URL publique. Dans le
clone, `git submodule update --init tools/structures` échoue :

```text
Submodule 'tools/structures' (/home/stephane/Data13TB/stephane/GitHub/drave-structures) registered for path 'tools/structures'
fatal: transport 'file' not allowed
Failed to clone 'tools/structures'. Retry scheduled
fatal: transport 'file' not allowed
Failed to clone 'tools/structures' a second time, aborting
```

Le CLI ne le dit pas : il **replie silencieusement** sur le chunker simple. Les sorties d'un
débutant diffèrent donc de la notice :

| mesure | clone public (sans S) | dépôt de développement (avec S) |
|---|---|---|
| `analyser` — rôle du GN | **objet** | **agent** |
| `analyser` — cible du GV | **—** | **chat** |
| `analyser` — confiance syntagme | **0,35** | **0,55** |
| `analyser` — JSON | **5 899** octets | **6 179** octets |
| `rejouer` — JSON | **4 217** octets | **4 390** octets |
| `evaluer` — POS | 86,25 % | 86,25 % |
| `evaluer` — F1 | **81,88 %** | **79,02 %** |
| `evaluer` — attachement exact | **88,70 %** | **99,58 %** |
| `evaluer` — base réelle F1 | **80,14 %** | **79,06 %** |
| `evaluer` — base réelle attachement | **91,85 %** | **99,46 %** |
| `evaluer` — top-k | **89,54 %** | **98,74 %** |

**Lecture.** Les deux colonnes ne mesurent **pas le même système** : le clone public segmente
avec le chunker de secours, le dépôt de développement avec le générateur S. Le F1 plus haut du
clone public (81,88 contre 79,02) **n'est pas un gain** : il s'accompagne de 10,88 points
d'attachement en moins et de deux champs sémantiques faux sur la phrase de démonstration. Ne pas
comparer les colonnes comme deux versions du même produit ; la phrase du README est celle de la
colonne de droite.

**Ce que le document fait.** Le quickstart affiche la **colonne de gauche** (ce que le débutant
voit réellement) et nomme la colonne de droite dans une note de mesure, avec le renvoi à cette
fiche. Il ne masque pas l'écart et ne présente pas la sortie du développeur comme celle d'un
clone public. C'est le compromis honnête : le parcours de 5 minutes **tient**, la qualité
canonique demande le sous-module.

**Ce qui reste à corriger (hors T3, docs).** Rendre `tools/structures` **public** (ou le
vendorer, ou remplacer l'URL locale par une URL publique) pour qu'un clone public rende la
sortie de la notice. Tant que ce n'est pas fait, le quickstart restera la seule description
vraie de ce que voit un débutant. La correction touche le packaging, pas la documentation :
elle est nommée, pas maquillée.

**Contrôle du contrôle.** Les mêmes commandes, lancées dans le dépôt de développement (avec le
sous-module), rendent `agent` / `chat` et **79,02 % / 99,58 %**. C'est ce contraste qui prouve
que l'écart vient du sous-module, pas du document ni de la phrase.

## 5. Ce qui pourrait rendre ce résultat faux

1. **Le commit a bougé.** Les sorties sont celles de **7f1519f** ; un clone plus récent peut
   changer les chiffres, le JSON ou les messages. Relancer `python3 tools/verifier_faq.py` et
   ce parcours si le code bouge.
2. **Le réseau.** `git clone` et `pip install -e .` (installation de `setuptools` en isolation)
   demandent le réseau ou un cache. Un poste hors ligne échoue **avant** le paquet.
3. **Le sous-module.** C'est le piège principal : sans `tools/structures`, la sortie est
   dégradée. Le document le dit, mais un lecteur qui saute la note croira à une régression.
4. **La clé et le cache.** Avec `--tagger`, le modèle, le prix et la latence dépendent du jour ;
   le cache peut servir une réponse ancienne. Sans clé, le code 4 est stable ; avec une clé
   refusée, le code est aussi 4.
5. **Python 3.10 non exécuté.** La mesure tourne en **3.13.16** ; `requires-python >= 3.10`
   est vérifié par la métadonnée, pas par une exécution réelle en 3.10. Windows n'a pas été
   testé (l'activation y est différente).
6. **Le `HOME` et le `PATH`.** Le contrôle négatif utilise un `HOME` neuf et pas de clé ; un
   `drave` déjà installé dans le `PATH`, ou une clé dans `~/.config/drave/`, changerait le
   résultat. C'est le sens du test « sans le dépôt ».
7. **`data/` absent.** Le corpus UDHR n'est pas versionné ; les commandes du quickstart n'en
   ont pas besoin, mais d'autres chemins (profils de langue, autotest UDHR) en dépendent.

## 6. Les fichiers

- [`docs/produit/demarrage.md`](../docs/produit/demarrage.md) — le quickstart.
- [`docs/produit/README.md`](../docs/produit/README.md) — lien en tête et au § 9.
- [`docs/README.md`](../docs/README.md) — ligne **Produit**.
- [`.gitignore`](../.gitignore) — `.venv/`.
- [`reports/quickstart.json`](quickstart.json) — le relevé machine.
- [`reports/rapport-empaquetage.md`](rapport-empaquetage.md) — T1, l'installation.
- [`reports/rapport-contrat-json.md`](rapport-contrat-json.md) — T2, le contrat du JSON.
