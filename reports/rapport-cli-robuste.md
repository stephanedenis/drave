# T5 — la robustesse de la CLI : `--duree`, cinq codes de sortie, aide des quatre sous-commandes, `--fichier` sans trace

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T5** (exploitable, 5/5) ·
> **Date** : 2026-11-15 · **Verdict** : ✅ **20/20 cas mesurés**, **30 tests** de fumée
> verts (dont **6** ajoutés pour T5), aucune trace Python sur les chemins d'erreur.
>
> **Le chiffre.** `--duree` ajoute `cout.duree_s` au JSON de `analyser` — **4,7 à 5,6 ms**
> mesurés sur « Le chat dort. », **5,9 ms** sur la phrase longue — et **ne change rien
> d'autre** : texte, étiquettes et durée par défaut sont identiques. Les **cinq codes**
> sont désormais **0 succès / 3 refus / 4 clé ou dépendance / 5 usage / 1 autre erreur** ;
> les deux erreurs de `--fichier` sortent **4** (chemin inexistant) et **5** (répertoire),
> avec un message d'une ligne et **0 trace**. `--aide` et `--help` sortent **0** sur les
> **quatre** sous-commandes.
>
> **Dispositif** : [`tools/banc_cli_robuste.py`](../tools/banc_cli_robuste.py),
> [`reports/cli-robuste.json`](cli-robuste.json),
> [`tools/tests/test_produit.py`](../tools/tests/test_produit.py),
> [`tools/drave.py`](../tools/drave.py),
> [`docs/produit/README.md`](../docs/produit/README.md) § 3.5/6/7,
> [`docs/produit/demarrage.md`](../docs/produit/demarrage.md) § 5–6.
> Commit de base mesuré : `7e195ee6` ; le diff T5 est appliqué par-dessus (le hash du JSON
> est celui du `HEAD` au moment du banc).

## 1. `--duree` — le temps de l'analyse, dans le JSON seulement

```bash
python3 tools/drave.py analyser "Le chat dort." --json --duree
```

Le champ est `cout.duree_s`, un flottant en secondes, mesuré par le bloc autour de
`Heuristique.analyser` (pas le démarrage Python). Sans le drapeau, `duree_s` reste
**absent** : le JSON par défaut est inchangé, et le déterminisme octet pour octet de
`--json` / `rejouer` est conservé.

| mesure | sans `--duree` | avec `--duree` |
|---|---|---|
| `cout.duree_s` | absent | **0,0047 – 0,0056 s** (phrase courte) · **0,0059 s** (phrase longue) |
| `texte` | identique | identique |
| `etiquettes` | identique | identique |
| validité du schéma v2 | oui | oui (`cout` est ouvert) |

`--jsonl` applique le même contrat : **une durée par ligne**, celle de l'analyse de la
phrase. Le drapeau ne vaut que pour `analyser` ; `evaluer`, `rejouer` et `restituer`
gardent leur sortie actuelle. En mode lisible (sans `--json`), il n'ajoute rien.

**Ce que la durée n'est pas.** Ce n'est pas un engagement de performance : elle varie
avec la machine et la charge. Le banc ne teste donc **aucun seuil** de temps ; il vérifie
la présence, le type, le signe et le fait que la durée est le **seul** ajout.

## 2. Les codes de sortie — le contrat, dans `--aide` et dans la notice

| code | sens | cas mesurés |
|---:|---|---|
| **0** | succès | `analyser`, `evaluer`, `rejouer`, `restituer`, `--version`, aide |
| **3** | refus d'analyse (une **réponse**, pas une erreur) | `analyser "" --json` (JSON de refus sur `stdout`), `restituer ""`, `rejouer ""` |
| **4** | clé/dépendance absente | `--tagger` sans clé (environnement nettoyé), `--fichier` sur un chemin inexistant |
| **5** | usage invalide | aucune sous-commande, `--langue de`, option fantôme `--sortie`, `--fichier` sur un répertoire |
| **1** | autre erreur | divergence de rejeu, tagger qui refuse une phrase sans POS, exception inattendue |

**Le changement assumé.** L'ancien contrat utilisait **2** pour l'usage et **1** pour les
erreurs de fichier ; il devient **5** pour l'usage et **4/5** pour les deux erreurs de
`--fichier` (voir § 4). Un refus dans `rejouer`, qui sortait **1**, sort désormais **3** :
le refus est une réponse, pas une panne. Les usages qui sortaient 2 (`--langue de`,
sous-commande absente, options exclusives) sortent **5**.

Le tableau est écrit à deux endroits, et le banc vérifie les deux :

- `python3 tools/drave.py --aide` : lignes « Codes de sortie : 0 succès · 3 refus ·
  4 clé/dépendance · 5 usage · 1 autre erreur » ;
- [`docs/produit/README.md`](../docs/produit/README.md) § 6 : une ligne par code, plus
  le paragraphe des deux erreurs de `--fichier`.

Le contrôle négatif du tableau est une **option fantôme** : `--sortie` doit sortir **5**
(et non 0), ce qui prouve que le code d'usage est réellement appliqué.

## 3. `--aide` et `--help` sur les quatre sous-commandes

Les **huit** combinaisons (`analyser`, `evaluer`, `rejouer`, `restituer` × `--aide`,
`--help`) sortent **0**, affichent `usage:` et nomment la sous-commande. L'aide globale
(`--aide`) porte le tableau des codes ; chaque aide de sous-commande porte ses options,
dont `--duree` pour `analyser`.

| commande | `--aide` | `--help` |
|---|---:|---:|
| `analyser` | 0 | 0 |
| `evaluer` | 0 | 0 |
| `rejouer` | 0 | 0 |
| `restituer` | 0 | 0 |

## 4. `--fichier` : chemin inexistant et répertoire

Les deux cas ont désormais un **code distinct**, un **message d'une ligne** et **rien sur
`stdout`** :

| entrée | code | message (`stderr`) | trace |
|---|---:|---|---|
| chemin inexistant | **4** | `drave: dépendance absente : fichier introuvable : 'absent.txt'` | aucune |
| répertoire | **5** | `drave: erreur d'usage : un répertoire n'est pas un fichier : 'corpus/' (--fichier attend un fichier UTF-8)` | aucune |
| fichier présent, illisible | **4** | `drave: dépendance absente : fichier illisible : '…' (Permission denied)` | aucune |

**Pourquoi 4 pour l'un et 5 pour l'autre.** Un chemin **inexistant** est une
**dépendance** qui manque à l'exécution (fichier déplacé, montage absent) : code **4**,
comme une clé absente. Un **répertoire** est un **usage invalide** de `--fichier`, qui
attend un fichier UTF-8 : code **5**. Un fichier présent mais non lisible reste une
dépendance (4), pas un usage.

Le contrôle négatif est la **trace** : sur ces trois chemins, `stdout` et `stderr` ne
contiennent ni `Traceback` ni `FileNotFoundError` / `IsADirectoryError` bruts. La lecture
passe par `ErreurEntree`, attrapée dans `main()` avant le `except Exception` générique.

## 5. Le dispositif et les résultats

`tools/banc_cli_robuste.py` rejoue **20 cas** sans réseau et sans clé (sauf le cas
`--tagger`, joué dans un `HOME` temporaire et un environnement sans `DEEPSEEK*`/`DSH_*`) :

| groupe | cas | résultat |
|---|---|---|
| durée | `duree_json`, `duree_jsonl` | ✅ 2/2 |
| aide | `aide_globale`, 4 × 2 sous-commandes | ✅ 9/9 |
| entrées | `fichier_inexistant`, `fichier_repertoire` | ✅ 2/2 |
| codes | usage × 3, refus × 2, clé absente, tableau de la notice | ✅ 7/7 |

```bash
python3 tools/banc_cli_robuste.py            # CLI robuste — 20/20 cas tenus
python3 tools/banc_cli_robuste.py --json > reports/cli-robuste.json
python3 tools/tests/test_produit.py          # Ran 30 tests ... OK
```

Le JSON `reports/cli-robuste.json` porte, pour chaque cas, la commande, le code attendu,
le code observé, le message, la présence de trace et le verdict ; il porte aussi le
commit, la version de Python et le **contrôle négatif** de la durée.

## 6. Contrôle négatif

1. **La durée n'est pas toujours là.** Sans `--duree`, `cout.duree_s` est **absent** ; le
   banc échoue si le champ apparaît, ce qui prouve que c'est bien le drapeau qui l'ajoute.
2. **Le code 5 n'est pas un code 0 déguisé.** `--sortie` (option fantôme) sort **5**, et
   une sous-commande absente sort **5**.
3. **Les erreurs de fichier ne sont pas des succès.** `stdout` est vide dans les deux cas,
   et le code est **4** ou **5**, jamais 0.
4. **Pas de trace.** Le banc cherche `Traceback` dans `stdout` et `stderr` des cas d'erreur.
5. **La clé absente reste un 4.** Le cas `--tagger` tourne sans clé et vérifie `stdout`
   vide + code 4 : le code 4 n'est pas réservé au fichier.

## 7. Ce qui pourrait rendre ce résultat faux

- **La durée est machine-dépendante** : les valeurs (4,7–5,9 ms) situent l'ordre de
  grandeur, pas une garantie. Le banc ne teste aucun seuil ; un test qui en fixerait un
  serait fragile.
- **`--duree` casse le déterminisme octet pour octet** : deux appels avec le drapeau
  diffèrent par `cout.duree_s`. C'est voulu ; `rejouer` et les tests de déterminisme
  n'utilisent pas `--duree`.
- **Les messages sont des chaînes** : les tests pinent des sous-chaînes
  (`fichier introuvable`, `répertoire`) et les codes, pas la phrase entière ; une
  reformulation qui garde le sens reste verte, une reformulation qui perd le mot échoue.
- **Le tableau de la notice peut dériver** : le banc lit les lignes `| **0** |`, `| **3** |`,
  `| **4** |`, `| **5** |` du README et les chaînes de `--aide` ; si l'un des deux change
  sans l'autre, le banc le dit.
- **Une clé DeepSeek dans l'environnement ferait échouer le cas 4** : le banc la retire
  explicitement (`DEEPSEEK*`, `DSH_*`) et utilise un `HOME` temporaire. C'est le comportement
  correct : avec une clé, `--tagger` ne doit pas sortir 4.
- **Le code 1 reste ouvert** aux erreurs inattendues ; une exception non prévue sort 1 avec
  un message, pas une trace. Le contrat ne prétend pas couvrir chaque exception possible.

## 8. Les fichiers touchés

| fichier | changement |
|---|---|
| `tools/drave.py` | `--duree` ; `ErreurEntree` (4/5) ; code d'usage **5** ; refus `rejouer` **3** ; épilogue des codes |
| `tools/tests/test_produit.py` | 6 tests T5 : durée JSON/JSONL, tableau, aide/help × 4, fichier inexistant, répertoire |
| `tools/tests/test_restitution*.py`, `test_tagger_api.py` | attentes d'usage passées de **2** à **5** (le contrat a changé) |
| `tools/banc_cli_robuste.py` | le banc des 20 cas et son JSON |
| `reports/cli-robuste.json` | la mesure reproductible |
| `docs/produit/README.md` | § 3.5, 6, 7 : codes, `--duree`, `--fichier` |
| `docs/produit/demarrage.md` | § 5–6 : erreurs de fichier et tableau des codes |
| `tools/verifier_faq.py`, `reports/faq.json`, `reports/rapport-faq.md` | `--langue de` et options fantômes en code **5** |

**Verdict.** La CLI est **robuste sur les quatre points demandés** : la durée est
disponible sans casser le défaut, les codes sont explicites et écrits aux deux endroits,
l'aide répond partout, et les deux erreurs de `--fichier` sont des réponses propres, sans
trace.
