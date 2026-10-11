# Reprise — démarrer une session de travail

> **Check-list, pas un état.** L'état vit dans [`docs/etat.md`](docs/etat.md) (index des modules)
> et [`docs/etat-cerveau.md`](docs/etat-cerveau.md) (les douze capacités, avec le chiffre qui
> prouve chacune). Ce fichier ne dit que : quoi lire, quoi vérifier, quels pièges éviter, et où
> écrire. Le détail mesuré est dans [`reports/`](reports/) — **une fiche par expérience**.
> Version longue d'avant le 2026-10-10 : [`journal/2026-10-10-reprise-historique.md`](journal/2026-10-10-reprise-historique.md).

## 1. Les cinq premières minutes

```bash
date                                   # HAE (EDT, UTC−4) : on LIT l'horloge, on ne la suppose pas
git log --oneline -5                   # ce qui vient d'être fait
ls journal/ | tail -5                  # la journée en cours, par thème
```

Puis, dans l'ordre : `journal/<aujourd'hui>.md` (l'index du jour) → [`docs/etat.md`](docs/etat.md)
(état par module et **prochaine action**) → la fiche `reports/` du chantier en cours.

## 2. Ce qui doit être vert

| quoi | commande | attendu |
|---|---|---|
| tests | `cd drave-core && cargo test --release` | **122 verts** |
| le calcul (non-régression) | `tools/porte-flux.sh` | cinq modes verts, ~2 min |
| toutes les portes | `tools/toutes-les-portes.sh` | **toutes vertes**, ~1 h, **aucune sautée** — le compte et les repères du jour sont dans `docs/references-non-regression.md` |
| les repères chiffrés | [`docs/references-non-regression.md`](docs/references-non-regression.md) | les valeurs de la passe du 10/10 |

**Toute modification du chemin d'exécution se paie d'un `porte-flux.sh`** (cinq modes, deux
minutes) — sans quoi trois modes étaient restés cassés en silence.

## 3. Les pièges de l'environnement (chacun a coûté une erreur)

- **un nœud sert UNE connexion** : les bancs doivent le **relancer** entre deux essais (ne pas le
  faire a fait croire que tous les drapeaux étaient inertes) ;
- **`--flux` ne prend pas d'argument** (`--flux f32` reste dense, en silence) et **un drapeau
  inconnu est ignoré** : utiliser `--options-strict` pour qu'il refuse ;
- **`--limit` ne veut pas dire la même chose selon le chemin** : `--ppl` note les N **premiers**
  jetons, `--ppl-reparti` tronque aux N **derniers** — dans une porte, **compter** les jetons ;
- **une position ne se devine pas** : `--tokenize` et `--prompt` ne comptent pas les mêmes jetons
  (`--etat-fin` existe pour ça) ;
- **un nœud refuse une plage d'une seule couche** ;
- **`pkill -f "<nom>"` se tue lui-même** si le motif apparaît dans sa propre ligne de commande ;
- **ne pas éditer un script pendant qu'il tourne** : bash lit au fur et à mesure ;
- **pas d'accent dans un nom de variable bash** (les noms de fonction, oui) ;
- **sérialiser les gros lecteurs de disque** (deux lecteurs de 63 Go en parallèle : 8,6 Mo/s) ;
- **`sys.exit("message")` sort toujours en 1** — une porte « verte » rendait 1 ;
- **`..Default::default()` donne 0,0 à un f32** : un poids de greffe nul, en silence ;
- **un fichier `.ids` du dépôt ne dit pas avec quel tokenizer il a été fait** :
  `data/wikitext2_test.txt.ids` vient d'un **autre** tokenizer que Qwen2.5 — le modèle complet y
  rend **7 379** de perplexité au lieu de 16,6. Une mesure qui s'y appuie est absurde **sans que
  rien ne le signale** ⇒ tokeniser soi-même (`--tokenize --fichier TEXTE --sortie F`) ;
- **`--etat-sortie PREFIXE` écrit `PREFIXE.<position>`** : c'est un **préfixe de fichier**, pas un
  dossier. Donner un dossier fait écrire `dossier.4`, `dossier.5`… et la relecture répond « aucun
  état lu » — la capture, elle, a bien eu lieu ;
- **un contrôle tautologique ne contrôle rien** : sous reparamétrisation, `module.weight` **est**
  déjà `signes · clamp(θ).exp()`, donc comparer les deux rend toujours 0. C'est ce faux contrôle
  qui a laissé **M8** ouvert deux jours — le vrai contrôle se fait **après** le retrait ;
- **`tie_word_embeddings` partage un TENSEUR, pas une formule** : `lm_head.weight` **est**
  `model.embed_tokens.weight`. Toute reparamétrisation de l'un **casse le partage** en silence
  (l'autre reste figé à sa valeur initiale, et l'écriture suivante écrase le mauvais). Exclure les
  poids **partagés** — `named_parameters(remove_duplicate=False)` les révèle ;
- **une mesure à un seul moment ne dit pas *où* ça casse** : recalculer la **même** grandeur à
  chaque étape (avant/après restauration/écriture/relecture) est ce qui a trouvé M8 ;
- **écrire dans un poids reparamétré n'écrit RIEN** : `mod.weight` est une valeur *calculée*, donc
  `mod.weight.mul_(...)` et `.copy_(...)` remplissent un temporaire — en silence. Trois sites du
  harnais faisaient ça (élagage, masque, ratio de signes) ; tout passe maintenant par
  `ecrire_poids`, qui écrit dans le **paramètre** et **vérifie** que le poids a bougé ;
- **un poids log-normal ne peut pas être NUL** (`|w| = e^θ ≥ e^−12 = 6,1e-6`) : un élagage ne
  l'annule qu'à la **quantification** de l'export. Le harnais **compte** ces poids et les annonce
  au lieu de laisser croire que l'élagage a fait zéro.

## 4. Les règles de méthode (le dépôt les applique à lui-même)

1. **un chiffre ne se vérifie pas par sa cohérence**, mais par comparaison à une valeur connue ;
2. **deux nombres égaux ne prouvent pas qu'ils mesurent la même chose** (18,5520 = 18,5520 était
   deux réglages inertes ; `0 ≡ 4` puits était un zéro **avalé** par un `if > 0`) ;
3. **une mesure d'inertie faite là où l'inertie est attendue ne dit rien** ;
4. **une porte rouge s'instruit jusqu'à sa cause** — deux fois, la cause était la porte ;
5. **une erreur avalée coûte plus cher que l'erreur** (un `except Exception` masquait un `import`
   manquant : 296 étapes perdues en silence) ;
6. **on ne laisse jamais l'arbre cassé** : une tentative qui échoue se renverse, et s'écrit.

## 5. Où écrire

[`docs/organisation-du-depot.md`](docs/organisation-du-depot.md) — en résumé : **`docs/`** = fond,
principes, plans, **état** ; **`reports/`** = **une fiche par expérience** (question, protocole,
mesures, verdict, date réelle) ; **`journal/AAAA-MM-JJ_<thème>.md`** = les **événements datés**,
avec liens (générés par `tools/journal_auto.py`, l'index du jour est `journal/AAAA-MM-JJ.md`).
**Tout horodatage est en HAE**, et la source de vérité d'une date est **git**.

## 6. La carte du dépôt

| chemin | quoi |
|---|---|
| `drave-core/` | le moteur Rust (`std` seul) : `model.rs`, `gguf.rs`, `topologie.rs`, `episodique.rs`, `trace_globale.rs`, `bus.rs`, `main.rs` |
| `tools/` | portes (`porte-*.sh`), campagne, harnais Python, `journal_auto.py`, `carte-fenetre-puits.sh` |
| `models/` | les GGUF utilisés par les portes et les mesures |
| `docs/` | fond, plans, état, conventions, glossaire |
| `reports/` | les mesures, une fiche par expérience (+ `reports/archive/` des monolithes d'origine) |
| `journal/` | les événements datés, par jour et par thème (+ `journal/sessions/`) |

## 7. Le premier pas, si rien n'est en cours

`docs/etat.md` porte la **prochaine action par module**, et `docs/etat-cerveau.md` § 6 la liste
courte des chantiers ouverts, chacun avec sa **première commande**. S'il n'y a plus de liste : la
consigne du dépôt est de **choisir ce qui est mesurable maintenant**, de lui donner une porte, et
de l'écrire — un round qui **corrige** une mesure fausse vaut un round qui en ajoute une.
