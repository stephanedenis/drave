# Session 00221850 — Outillage de présentation de documentation

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `00221850-90de-4287-90ee-324a35e504cd` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 11:34 |
| Durée | 4.9 h |
| Tours | 6 |
| Messages | 469 |
| Appels d'outils | 529 |
| Fichiers touchés | 38 |
| Commandes | 389 |
| Sous-agents | 0 |
| Commits | 25 |
| Compactages de contexte | 0 |

## Objectifs déclarés

- **create** — Isoler l'outil de présentation de la documentation (mdserve, éventuellement mdopen) dans un dépôt public GitHub autonome, généralisé, testé et documenté, puis mettre à jour les références de Drave-Qtrinet vers ce dépôt.
- **complete** — Isoler l'outil de présentation de la documentation (mdserve, éventuellement mdopen) dans un dépôt public GitHub autonome, généralisé, testé et documenté, puis mettre à jour les références de Drave-Qtrinet vers ce dépôt.

## 1. Ce qui a été demandé

**Tour 1** — cette session de travail se concentre exclusivement sur l'outillage de présentation de la documentation. le but est d'isoler cet outil pour le mettre dans un repos public sur GitHub et le faire évoluer indépendamment du projet Drave-Qtrinet.

**Tour 2** — arrête le processus PyPI mdserve pour qu'on puisse utiliser le nom. quand tu as terminé la migration de l'appli, supprime l'appli du repo qtrinet pour qu'on n'ait qu'une seule instance du code à gérer.

**Tour 3** — mets ça en submodule de Qtrinet car on va faire évoluer les fonctionnalités avec sa doc

**Tour 4** — aurait-on intérêt à utiliser rust au lieu de python?

**Tour 5** — ok, on continue en python. Maintenant, corrigeons la robustesse des liens relatifs. car je crois que cliquer sur un lien change l'url. Si on est dans un spa, on devrait correller l'url avec le fichier courant et supporter la navigation par url.

**Tour 6** — on devrait avoir un fichier de config dans home (ou dossier approprié) afin de pouvoir n'avoir qu'une seule instance du service pour tous les dossiers à surveiller et servir. il faudra probavblement des dossiers virtuels dans l'url pour couvrir les différents repos sur un même port. de plus tant qu'a surveiller les dossiers, installe plantuml et mermaid pour générer automatiquement les fichiers sv … [31 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — cette session de travail se concentre exclusivement sur l'outillage de présentation de la documentation. le but est d'is … [121 caractères tronqués]

*203 appels d'outils.* Actions notables :

- bash — List repository root contents
- bash — Check git status and recent history
- bash — List tools directory
- bash — List docs directory
- bash — Find documentation-related tool files
- bash — Find tools producing HTML or serving pages
- bash — Inspect sizes and head of doc tools
- bash — Check doc tool details and gitignore
- read
- bash — Find all references to the doc server
- bash — Git history of documentation tools
- bash — Inspect mdserve installation
- bash — Check documentation services status
- bash — Inspect mdserve head and size
- … et 170 autres

**Synthèse produite :**

⏵ Dépôt public créé, CI verte, service basculé — bilan de la session

\## Ce qui a été isolé

L'outil de présentation était **`mdserve`** (le navigateur de documents : arbre, rendu, rechargement, épingles, filtre temporel), avec son lanceur **`mdopen`**. Il vivait hors du dépôt, dans `~/.local/bin/mdserve`, avec le patch `/asset` appliqué à la main — exactement le problème que cette session devait résoudre.

`tools/serveur-doc.py` n'a **pas** été extrait : c'est la page « où en est le travail », intimement liée à `docs/en-cours.md`, `reports/` et `journal/` de Drave. Il ne peut pas évoluer indépendamment.

\## Le dépôt public

**https://github.com/stephanedenis/mdserve** — public, licence MIT, release [v0.1.0](https://github.com/stephanedenis/mdserve/releases/tag/v0.1.0), CI verte sur **Python 3.9 à 3.13**.

- paquet installable `mdserve-local`, commandes `mdserve` et `mdopen` ;
- `src/mdserve/` : configuration, chemins, épingles, rendu, arbre, serveur, interface, CLI ;
- CSS et JavaScript extraits en fichiers statiques (`static/style.css`, `static/tree.js`) ;
- **64 tests** : rendu, cache, réécriture des liens/assets, épingles, traversée de chemins, routes HTTP, garde-fous ;
- `README`, `CHANGELOG`, `CONTRIBUTING`, `SECURITY`, `Makefile`, workflow GitHub Actions.

**Parité vérifiée** : la page HTML servie par la nouvelle version est **octet pour octet identique** à celle de l'ancien script. Le rendu, les images SVG et les liens `.md` ont aussi été testés dans Chrome headless.

\## Ce qui a changé dans l'outil

- plus aucun chemin propre à Drave : racine par défaut = répertoire courant ;
- les liens vers un `.md` ouvrent le document dans le lecteur (`/?f=…`) au lieu de renvoyer un 404 ;
- `/asset` ne sert plus qu'une liste fermée de types (images, polices, CSS/JS, PDF, textes) : un `.env` n'est plus téléchargeable ;
- vérification des en-têtes `Host` et `Origin` (rebinding DNS), chemins résolus avec les liens symboliques ;
- épingles écrites en `0600` ;
- `--no-browser`, `--config-dir`, `--cache-dir`, `--version`, port `0` ;
- `mdopen` déduit la racine du dossier commun des fichiers.

\## Côté Drave

- `docs/utilisation.md` pointe vers le dépôt public, documente l'installation (`pipx install --force "git+https://…"`), la mise à jour (`pipx reinstall mdserve-local`) et le `--no-browser` du service ;
- `docs/en-cours.md` mentionne l'outil comme dépôt autonome ;
- `python3 tools/revue_documentation.py` et `bash tools/porte-tableaux.sh` passent ; `python3 tools/ta
… [902 caractères tronqués]

### Tour 2 — arrête le processus PyPI mdserve pour qu'on puisse utiliser le nom. quand tu as terminé la migration de l'appli, supprim … [81 caractères tronqués]

*77 appels d'outils.* Actions notables :

- bash — Look for PyPI upload processes and credentials
- bash — Inventory Qtrinet documentation server and services
- bash — Inspect PyPI mdserve ownership and release history
- bash — Check if mdserve code ever existed in Qtrinet
- ask_user_question
- bash — Check PyPI availability of candidate names
- bash — Check GitHub repo availability under account
- bash — Check global name conflicts
- bash — Inventory old name occurrences in public repo
- bash — Rename package directory and bulk-replace identifiers
- bash — Inspect renamed metadata and entry points
- bash — Find version and old-name residues
- bash — Bump version and server identifier
- bash — Read README sections to update
- … et 59 autres

**Synthèse produite :**

⏵ Bilan : `docwatch` publié, `serveur-doc.py` retiré, un seul serveur actif

\## PyPI : il n'y avait aucun processus à arrêter

Le nom **`mdserve` sur PyPI** appartient à un projet tiers (`openjw` / `kingreatwill`, dernière release **1.4.4 du 5 novembre 2021**). Un nom PyPI ne se libère pas en arrêtant un processus local : il faudrait une reprise **PEP 541** auprès de PyPI, avec un délai et aucune garantie.

J'ai donc suivi ta consigne « trouve un nom plus adéquat » :

\## Le nouveau nom : `docwatch`

**https://github.com/stephanedenis/docwatch** — public, MIT, release [v0.2.0](https://github.com/stephanedenis/docwatch/releases/tag/v0.2.0).

Le nom dit ce que fait l'outil : il **regarde** une collection de documents pendant que d'autres processus les éditent, et en affiche l'état courant sans toucher aux sources.

- distribution, module et commandes renommés : **`docwatch`** et **`docopen`** ;
- version **0.2.0**, 64 tests, CI verte Python 3.9 à 3.13 ;
- répertoires `~/.config/docwatch` et `~/.cache/docwatch` ;
- wheel construit et testé dans un venv vierge, interface vérifiée dans Chrome headless ;
- procédure de publication PyPI ajoutée au README.

**`docwatch` est libre sur PyPI** (vérifié : 404), mais **pas encore réservé** : un nom PyPI n'est acquis qu'à la première publication. Il faut ton jeton PyPI pour lancer :

```bash
cd ~/Data13TB/stephane/GitHub/docwatch
.venv/bin/python -m build
.venv/bin/python -m twine upload dist/*
```

Sans `~/.pypirc` ni `TWINE_PASSWORD`, je ne peux pas publier à ta place. Tant que ce n'est pas fait, le nom reste disponible pour un tiers.

\## Qtrinet : une seule instance

- **`tools/serveur-doc.py` supprimé** (commit `441cb959`), après sauvegarde dans `~/.local/share/docwatch-migration/`.
- **`drave-doc.service` arrêté, désactivé et retiré** : le port **8787 est fermé**.
- **`mdserve-local` désinstallé de pipx** ; `mdserve` n'est plus dans le `PATH`. Seuls `docwatch` et `docopen` restent.
- **`docwatch.service`** actif sur **127.0.0.1:8771**, avec les épingles migrées : `docs`, `reports` et `en-cours.md`.
- Anciens scripts, configuration, cache et unités regroupés dans `~/.local/share/docwatch-migration/` (retour arrière possible).
- Documentation mise à jour :
  - `docs/utilisation.md` décrit **un seul serveur**, `docwatch` ;
  - `docs/references-non-regression.md` ne liste plus l'ancien serveur ;
  - `docs/en-cours.md` (C6) pointe vers `docwatch` ;
  - `revue_documentation.py` et `porte-tableaux.sh` passent.

\## Vérifica
… [756 caractères tronqués]

### Tour 3 — mets ça en submodule de Qtrinet car on va faire évoluer les fonctionnalités avec sa doc

*48 appels d'outils.* Actions notables :

- bash — Inspect Qtrinet clone instructions and git state
- bash — Verify standalone docwatch repo before submodule
- bash — Add docwatch git submodule
- bash — Install docwatch editable from submodule
- bash — Clean reinstall editable from submodule
- bash — Find Qtrinet docs sections for submodule note
- bash — Find clone docs and repository layout
- bash — Inspect README structure for submodule note
- bash — Read repository contents section
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md`
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md`
- … et 27 autres

**Synthèse produite :**

⏵ Sous-module `tools/docwatch` ajouté, service basculé en éditable, clone autonome archivé

\## Le sous-module

`docwatch` est maintenant un **sous-module Git** de Qtrinet :

- chemin : **`tools/docwatch/`** ;
- pointeur : **`d5b49ed`** (`v0.2.0-2`, `main` propre) ;
- `.gitmodules` : URL HTTPS publique `https://github.com/stephanedenis/docwatch.git` ;
- `git ls-tree` confirme un gitlink `160000` ;
- après un clone de Qtrinet : `git submodule update --init --recursive`.

\## Développement désormais dans le sous-module

Le service tourne sur une installation **éditable** du sous-module :

```text
docwatch.__file__ = .../Qtrinet/tools/docwatch/src/docwatch/__init__.py
```

Workflow documenté dans `README.md` et `docs/utilisation.md` :

```bash
cd tools/docwatch
pytest && ruff check .
git add -A && git commit -m "…" && git push
cd ../..
git add tools/docwatch && git commit -m "DOCWATCH — …"   # pointeur
systemctl --user restart docwatch.service                 # après un changement Python
```

La documentation de Qtrinet suit : `README.md`, `docs/utilisation.md`, `docs/en-cours.md`, `docs/modularisation.md` (le sous-module y est décrit comme une **dépendance externe**, pas un découpage interne), et le glossaire/les outils ne parlent plus de `mdserve`.

\## Une seule copie de travail

L'ancien clone autonome `~/GitHub/docwatch` a été **archivé**, pas supprimé sans trace :

- bundle complet : `~/.local/share/docwatch-migration/docwatch-standalone.bundle` (61 Ko) ;
- copie : `~/.local/share/docwatch-migration/standalone-clone-20261027/`.

La seule copie active est maintenant `~/GitHub/Qtrinet/tools/docwatch/`. L'ancien `mdserve` reste absent du `PATH`, et le port **8787 est fermé**.

\## Vérifications

- Qtrinet : arbre de travail **propre**, sous-module propre et à jour ;
- `docwatch.service` **actif** sur `127.0.0.1:8771`, épingles `docs`, `reports`, `en-cours.md` conservées ;
- `revue_documentation.py`, `porte-tableaux.sh` et `taille_documents.py` : **verts** ;
- dépôt public `docwatch` : 64 tests, CI 3.9–3.13 verte, release `v0.2.0`.

\## PyPI

`docwatch` est toujours **libre** sur PyPI (404). La publication est prête mais nécessite ton jeton : sans `~/.pypirc` ni `TWINE_PASSWORD`, je ne peux pas réserver le nom. Les commandes sont dans le README (`python -m build`, `twine upload`).

\## Note sécurité

Ta configuration git globale contient une règle `insteadOf` avec un **jeton Azure en clair** (`dev.azure.com`). Je n'y ai pas touché, mais ce jeton est lisible dans 
… [61 caractères tronqués]

### Tour 4 — aurait-on intérêt à utiliser rust au lieu de python?

*18 appels d'outils.* Actions notables :

- bash — Find largest docs and service memory
- bash — Measure HTTP latency of main routes
- bash — Measure cold and warm render latency
- bash — Benchmark Python Markdown rendering directly
- bash — Measure mistune rendering time directly
- bash — Build and run Rust Markdown benchmark
- bash — Measure Python startup time and memory
- bash — Benchmark Rust recursive Markdown scan
- bash — Check PyPI for fast Markdown bindings
- bash — Inspect fast Markdown packages
- bash — Benchmark Python, Rust and C Markdown engines
- bash — Locate markdown-it-pyrs module name
- bash — Inspect markdown-it-pyrs API
- bash — Inspect MarkdownIt constructor
- … et 4 autres

**Synthèse produite :**

⏵ Réponse étayée par des mesures : le goulet est le rendu Markdown, pas le serveur Python

\## Réponse courte

**Non pour une réécriture complète en Rust maintenant. Oui pour un moteur de rendu Rust.**

Le serveur Python n'est pas le goulet d'étranglement : l'arbre répond en 1–2 ms, le scan récent en 15 ms, une page à chaud en 5–8 ms, pour 27,6 Mo de RSS. Le seul poste coûteux est le **rendu Markdown à froid**, et un moteur Rust le divise par 16 à 25 — sans toucher au serveur, à l'API ni au frontend.

\## Ce que j'ai mesuré

Fichiers réels de Qtrinet, 5 passes après échauffement, lecture disque hors chrono. Python 3.13, mistune 3.4.0 (pur Python), Rust 1.97, pulldown-cmark 0.13.

| poste | Python actuel | Rust mesuré |
|---|---:|---:|
| rendu 49 Ko (`docs/roadmap.md`) | **51 ms** | **2,9 ms** (`markdown-it-pyrs`) · 0,6 ms (pulldown-cmark natif) |
| rendu 179 Ko | **174 ms** | **9,9 ms** · 2,1 ms |
| rendu 303 Ko | **310 ms** | **19,5 ms** · 3,7 ms |
| scan récursif 1 068 `.md` | 15 ms (`/recent`) | 3,3 ms (`walkdir`) |
| arbre, un niveau | 1–2 ms | ~0,1 ms (estimation) |
| démarrage jusqu'à `/status` | 130 ms | ~1–5 ms (estimation) |
| mémoire résidente | 27,6 Mo | ~5–10 Mo (estimation) |

À retenir : à chaud, le cache ramène déjà le rendu HTTP à **5–8 ms**. Le coût n'apparaît qu'à la **première vue** ou après chaque **modification** d'un document — précisément le cas d'usage de docwatch, qui suit des documents en cours d'édition.

\## Pourquoi pas une réécriture complète

- **Le gain principal est dans le parseur**, pas dans HTTP, les épingles, l'arbre ou le JSON. Ces routes sont déjà sous 20 ms.
- **Le frontend reste en JavaScript** dans tous les scénarios : 1 300 lignes, c'est lui qui porte l'expérience.
- **Le coût de réécriture** : ~1 100 lignes de Python, 64 tests, la sécurité des chemins, les épingles, le cache, le filtre temporel. En Rust, il faut ajouter axum/tokio, serde, notify, pulldown-cmark, et maintenir des binaires par plateforme.
- **Le gain restant** (démarrage, mémoire, binaire unique) ne change pas l'usage quotidien d'un service local qui tourne en permanence.

\## Les trois options

| option | coût | rendu à froid | démarrage / mémoire | distribution |
|---|---|---|---:|---|
| **Python actuel** | 0 | 51–310 ms | 130 ms / 28 Mo | pipx, Python 3.9+ |
| **Python + moteur Rust** | quelques jours | **3–20 ms** | inchangés | pipx + dépendance compilée |
| **Backend Rust complet** | plusieurs semaines | 1–5 ms | ~5 ms / ~10 Mo | binaire unique |

… [1842 caractères tronqués]

### Tour 5 — ok, on continue en python. Maintenant, corrigeons la robustesse des liens relatifs. car je crois que cliquer sur un lien … [124 caractères tronqués]

*73 appels d'outils.* Actions notables :

- bash — Find URL and openFile handling in client JS
- bash — Locate openFile definition
- read
- bash — Inspect client state variables
- bash — List all openFile call sites
- bash — Check currentFile usage
- bash — Rewrite Markdown links to clean URLs
- bash — Locate render call and 404 route
- bash — Add clean-URL SPA route and initial root
- bash — Add SPA history and link interception to client
- bash — Support clean path initial load in UI
- bash — Run tests to identify expected changes
- bash — Create dev venv and run tests
- bash — Update tests and add clean URL coverage
- … et 50 autres

**Synthèse produite :**

⏵ Navigation SPA corrigée : URL propre par document, clic sans rechargement, retour/avant

\## Ce qui n’allait pas

Un lien `.md` était réécrit en `/?f=/chemin/absolu`. Le clic provoquait donc une **navigation complète** : rechargement de la page, perte de l’état SPA (arbre déplié, épingles, position), et URL qui ne correspondait plus au chemin naturel du document.

\## Ce qui est en place

**1. Une URL propre par document**

```text
http://127.0.0.1:8771/docs/guide.md
http://127.0.0.1:8771/docs/synthese/05-la-pensee-sans-verbaliser.md#section
```

Le serveur sert la SPA sur `/<chemin>.md` : un rechargement, un favori ou un lien partagé fonctionne. La cible est validée sous la racine de départ.

**2. Clic sans rechargement**

Le client intercepte les liens `.md` de `#main` (même origine, clic gauche, sans modificateur, sans `target=_blank`/`download`), ouvre le document via `openFile`, puis met l’URL à jour avec `history.pushState`. L’arbre, les épingles et l’état restent en place.

**3. Retour / avant**

`popstate` relit l’URL et rouvre le bon document. Le retour vers `/` restaure la page d’accueil. Les liens en nouvel onglet ou avec `Ctrl`/`Cmd` continuent d’ouvrir l’URL propre dans un onglet, et le serveur la sert correctement.

**4. Liens relatifs robustes**

- `sub/b.md`, `../a.md`, `./x.md` : résolus contre le **dossier du document courant** ;
- `/docs/x.md` : résolu contre la **racine de départ** ;
- espaces et `%20`, accents, `?query`, `#fragment` : gérés ;
- ancre : conservée dans l’URL et défilement après le rendu ;
- lien externe, `mailto:`, image, PDF : laissés au navigateur.

**5. Anciennes URL conservées**

`/?f=/chemin/absolu` reste accepté et est **normalisé** vers `/docs/...` au premier rendu. `docopen` ouvre désormais directement l’URL propre.

\## Vérifications

- **69 tests** dont un test navigateur Chrome DevTools : clic sur un lien, URL `/sub/b.md`, **marqueur JS conservé** (donc pas de rechargement), retour/avant, `../`, espace `%20`, ancre, normalisation de `?f=`.
- Test réel sur Qtrinet : `/docs/en-cours.md` → clic `/docs/roadmap.md` → contenu changé, URL propre, retour correct.
- CI `docwatch` verte sur Python 3.9 à 3.13.
- `revue_documentation.py`, `porte-tableaux.sh`, `taille_documents.py`, `verifier_schemas.py` : verts.

\## Déploiement

- release **`docwatch v0.3.0`** : https://github.com/stephanedenis/docwatch/releases/tag/v0.3.0
- commit `docwatch` : `3c64d40` ;
- pointeur du sous-module dans Qtrinet : `95108777` ;
- service `do
… [514 caractères tronqués]

### Tour 6 — on devrait avoir un fichier de config dans home (ou dossier approprié) afin de pouvoir n'avoir qu'une seule instance du  … [311 caractères tronqués]

*110 appels d'outils.* Actions notables :

- bash — Check diagram tools and config state
- bash — Check submodule state and structure
- bash — Locate root switching and pins/recent calls
- read
- bash — Inventory Settings and State usage
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch/src/docwatch/config.py`
- bash — Refactor server routes for mounts
- bash — Check helper usage and UI template head
- bash — Find page_html callers and script tail
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch/src/docwatch/ui.py`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch/src/docwatch/ui.py`
- bash — Style the mount links
- bash — Adapt root/pins/recent to mounts
- bash — Locate URL functions after edits
- … et 86 autres

**Synthèse produite :**

⏵ Multi-racines et diagrammes en service : 0.4.1, deux dépôts sur un port, SVG PlantUML/Mermaid générés

\## Une seule instance, plusieurs dépôts

La configuration est dans **`~/.config/docwatch/config.toml`** :

```toml
[server]
port = 8771

[[mounts]]
name = "drave"
path = "~/Data13TB/stephane/GitHub/Qtrinet"
label = "Drave"

[[mounts]]
name = "docwatch"
path = "~/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch"
label = "docwatch"
```

Une seule instance sert donc :

- **http://127.0.0.1:8771/drave/** — tout Qtrinet ;
- **http://127.0.0.1:8771/docwatch/** — le dépôt de l’outil ;
- `/drave/docs/en-cours.md`, `/docwatch/README.md`, etc.

Le panneau de gauche affiche les deux montages. Les épingles et le filtre temporel sont désormais **par montage** (`/pins?root=…`, `/recent?root=…`). `docwatch --init-config` écrit un modèle ; `--config` choisit un autre fichier ; une racine passée en argument conserve le mode mono-racine.

Le service `docwatch.service` a été basculé sur cette configuration et tourne en **0.4.1**.

\## Diagrammes PlantUML et Mermaid

Les outils sont installés localement :

- **PlantUML 1.2026.9** : `~/.local/share/docwatch/tools/plantuml.jar`, wrapper `~/.local/bin/plantuml` ;
- **Mermaid CLI 12.0.0** : `~/.local/share/docwatch/tools/mermaid/`, wrapper `~/.local/bin/mmdc`, Chrome système via `~/.config/docwatch/puppeteer.json`.

\### Fichiers sources : l’extension reste en affixe

| source | SVG généré |
|---|---|
| `diagram.puml` | `diagram.puml.svg` |
| `diagram.pu` | `diagram.pu.svg` |
| `diagram.plantuml` | `diagram.plantuml.svg` |
| `diagram.mmd` | `diagram.mmd.svg` |
| `diagram.mermaid` | `diagram.mermaid.svg` |

Vérifié sur les deux sources réelles de Drave :

- `docs/schemas/pipeline.mmd` → **`pipeline.mmd.svg`** ;
- `docs/schemas/decision.puml` → **`decision.puml.svg`**.

Les images de `docs/schemas/README.md` s’affichent dans le navigateur (`naturalWidth` 300 et 462). Les SVG générés reçoivent `viewBox`, `<title>` et `<desc>` à la racine ; la porte `verifier_schemas.py` passe.

\### Blocs Markdown

Les blocs `puml`, `plantuml`, `mmd`, `mermaid` sont convertis en SVG et servis par `/diagram/<hash>.<affixe>.svg` — l’affixe est conservé là aussi (`<hash>.puml.svg`, `<hash>.mmd.svg`). Un outil absent ou une syntaxe invalide laisse le bloc de code intact.

\### Surveillance

Un watcher parcourt les montages toutes les 5 secondes et régénère un SVG quand sa source est plus récente. Un SVG manquant est aussi produit à la demande par `/asset`
… [955 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/src/mdserve/__init__.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/src/mdserve/config.py` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/src/mdserve/paths.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/src/mdserve/pins.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/src/mdserve/render.py` | 1 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/src/mdserve/tree.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/src/mdserve/ui.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/src/mdserve/server.py` | 1 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/src/mdserve/cli.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/src/mdserve/__main__.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/src/mdserve/mdopen.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/pyproject.toml` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/LICENSE` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/README.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/CHANGELOG.md` | 2 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/.gitignore` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/.github/workflows/ci.yml` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/Makefile` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/tests/conftest.py` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/tests/test_render.py` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/tests/test_paths.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/tests/test_pins.py` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/tests/test_server.py` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/tests/test_cli.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/CONTRIBUTING.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/SECURITY.md` | 1 | 0 |
| `/home/stephane/.config/systemd/user/mdserve.service` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/utilisation.md` | 0 | 14 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/en-cours.md` | 0 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/mdserve/tests/test_config.py` | 1 | 0 |
| `/home/stephane/.config/systemd/user/docwatch.service` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/references-non-regression.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/modularisation.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch/README.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch/src/docwatch/config.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch/src/docwatch/ui.py` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch/src/docwatch/diagrams.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** List repository root contents
- **T1** Check git status and recent history
- **T1** List tools directory
- **T1** List docs directory
- **T1** Find documentation-related tool files
- **T1** Find tools producing HTML or serving pages
- **T1** Inspect sizes and head of doc tools
- **T1** Check doc tool details and gitignore
- **T1** Find all references to the doc server
- **T1** Git history of documentation tools
- **T1** Inspect mdserve installation
- **T1** Check documentation services status
- **T1** Inspect mdserve head and size
- **T1** Diff mdserve versions
- **T1** Read services and pins config
- **T1** Search existing mdserve repo and GitHub auth
- **T1** All mdserve mentions in docs/journal
- **T1** Journal mentions of mdserve
- **T1** List imports and top-level definitions
- **T1** Read mdopen companion tool
- **T1** Check repo visibility and name availability
- **T1** Check Drave coupling and Python environment
- **T1** Locate CSS and JS constants
- **T1** AST-inspect top-level assignments
- **T1** Check license and PyPI name availability
- **T1** Check pipx and git identity
- **T1** Inspect PyPI mdserve package ownership
- **T1** Check alternative PyPI names
- **T1** Check CSS/JS block boundaries
- **T1** Build test fixture tree
- **T1** Capture baseline responses from current server
- **T1** Inspect baseline render and tree output
- **T1** Search client-side markdown link handling
- **T1** Find click interception in client JS
- **T1** Read global click handler
- **T1** List sibling GitHub repositories
- **T1** Create repo skeleton and extract CSS/JS
- **T1** Read end of prune function
- **T1** Replace path helper wrappers
- **T1** Compile modules and inspect imports
- … et 349 autres

## 4. Mesures et résultats marquants

- **T1** `07badd16 B12 — M2 AUG-FORMES : DE 95,2 % INÉDIT 13/20 ; CHEMIN 88,1 % 6/14 ; POINT SOUS LA MAJORITÉ`
- **T1** `9a3f753d B12 — M5 CONTEXTE : SOURCE +0,626 NAT, CIBLE +0,411 ; M6 SÉLECTEUR 94,95 % MAIS CONFLIT 0`
- **T1** `table { border-collapse:collapse; width:100%; margin:.6rem 0 1rem; font-size:.92rem; }`
- **T1** `82e9a9bf SYNTHESE — LE CHAPITRE 08 : LES OPERATIONS ET LA GRAPPE. Il relie les cinq mesures de B4 (l'etat porte les operations, mais il ne les calcule pas : pas une direction, apprenable, un sous-espa`
- **T1** `3. Rendu par ton navigateur (Blink) : ~0,9 s pour 362 Ko, ~3,3 s pour 8,3 Mo.`
- **T1** `defilement. html/body sont en height:100% + overflow:hidden et #wrap en`
- **T1** `height:100% : sans cela les panneaux s'etirent a la hauteur de leur contenu et`
- **T1** `html, body { height:100%; }`
- **T1** `#wrap { display:flex; height:100%; min-height:0; }`
- **T1** `........................................................F..              [100%]`
- **T1** `...........................................................              [100%]`
- **T1** `CPU: 140ms`
- **T1** `| 09:02 | `db87e70f` | B12 — M2 SYNTHÉTIQUE : DE 6,2 % (146), M3 N-BACK CONTRÔLE 1,0 ; PAS DE DOUBLE DISSOCIATION |`
- **T1** `| 09:06 | `e6985d94` | B12 — M2 DOUBLE DISSOCIATION : DE 93,2 %, LÉSIONS 19,2 / 1,4 ; LE DERNIER ÉTAT DÉBLOQUE |`
- **T1** `| 09:10 | `c92ccf83` | B12 — M8 SOMMEIL GÉNÉRALISE : 96,48 % SUR ÉPISODES NON STOCKÉS (BASELINE 0) ; M2 LÉSIONS 17,8 / 2,7 |`
- **T1** `| 09:12 | `28c09f51` | B12 — M7 NEUTRE (13,9 % VS 13,7 %), M8 96,48 % HORS STOCK ; M2/M3/M4 TIENNENT, M5/M6 NÉGATIFS |`
- **T1** `| 09:16 | `091203d1` | B12 — M2 ACTION 98,6 % / DE 93,2 % (LÉSIONS 19,2 / 3,4) ; M7 NUL À CAPACITÉ 16 |`
- **T1** `| 09:19 | `8cf29faf` | B12 — M5 ORDRE 2 SANS GAIN, M7 NOUVEAUTÉ PAR SURFACE SANS EFFET ; M6 72,9 % |`
- **T1** `| 09:49 | `b563a155` | B12 — PIPELINE M1→M4→M8 : 528/528, COMPLÉTION 96,3 %, PROTOYPES 7 |`
- **T1** `| 09:54 | `d28ad551` | B12 — PIPELINE M1→M4→M8 : 528/528, COMPLÉTION 96,3 %, 7 PROTOTYPES (DOCS) |`
- **T1** `| 11:05 | `9a3f753d` | B12 — M5 CONTEXTE : SOURCE +0,626 NAT, CIBLE +0,411 ; M6 SÉLECTEUR 94,95 % MAIS CONFLIT 0 |`
- **T1** `| 11:24 | `07badd16` | B12 — M2 AUG-FORMES : DE 95,2 % INÉDIT 13/20 ; CHEMIN 88,1 % 6/14 ; POINT SOUS LA MAJORITÉ |`
- **T1** `| **`lecteur_non_lineaire.py`** ✓ | le lecteur **MLP** (et sa leçon : mal réglé, il **sur-apprend** ✗ — 119,9 % contre 85,2 % pour le ridge ✓) | `... --modeles A,B --ids <corpus>` |`
- **T1** `un ridge **sous-déterminé** (moins de positions que de coefficients ✓) **interpole** et rend 0,0 % ✓✗ ;`
- **T1** `[still running after 60000ms; moved to background job bash-90]`
- **T1** `fcb20469 B12 — MESURES CORRIGÉES A1–A7 (1,4 MO) ; M8 SOMMEIL DOCSTRING`
- **T1** `74c1fd86 B12 — M2 AUG-POS : VERS 95,4 % INÉDIT 13,3/20 ; DE 92,2 % ; POINT = MAJORITÉ ; AUCUNE VARIANTE NE DOMINE`
- **T1** `............................................................             [100%]`
- **T1** `................................................................         [100%]`
- **T2** `[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)`
- **T2** `25830d86 B14 — M2 DANS LA CHAÎNE : 100 % VS 93,4/93,6 %, AUCUN ÉTAGE NE LE CONSOMME ; RAMEAU`
- **T2** `| `lora_recopie.py` ✓ | apprend au modèle à **recopier** (LoRA, 100,0 % avec contrôle à 0,0 % ✓) | `python3 tools/lora_recopie.py --hf <snapshot> --ids <corpus>` |`
- **T2** `une cible qui contient **sa propre source** (même position ✓) rend aussi 0,0 % ✓✗ ; un plan de textes qui`
- **T2** `- **B14 M2 dans la chaîne** — **n'ajoute rien** : M1 **100 %** (`de`/`vers`), M2 **93,4 / 93,6 %**, aucun étage ne consomme M2 ; M5 plateau **18,70 % vs 12,60 %** ; M6 **94,32 / 94,95 %**. M2 est un r`
- **T2** `- **B15 multilingue** — M1 sur **66 langues** : **528/528** avec contexte, **70,8 %** sans ; **26/26** variantes et **15/15** interlangues invariantes ; contrôle permuté **0 %** attendu / **90 %** don`
- **T3** `> fichier de 179 Ko, et des **dates dans le futur** (jusqu'au 12 octobre 2026, alors que le travail`
- **T3** `*Ce que la mesure impose de dire tout de suite* : la sparsité ne gagne pas toujours. En dessous d'environ **22 % de`
- **T3** `même perplexité à **+0,074 %** près.`
- **T3** `Les mesures ont déjà appris des choses invisibles autrement : le **top 10 %** des neurones portent **33,1 %** de la`
- **T3** `magnitude, et seuls **0,08 %** sont « chauds » plus de 90 % du temps — donc un préchargement statique ne paie pas,`
- **T3** `469 fichiers, 32 Mo d'historique, journaux de session compris.`
- **T3** `(9 Mo de transcriptions, 3 fichiers de 1 à 9 Mo, qui grossissent tout seuls et`
- **T4** `docs/roadmap.md                                            48983 o      59.4 ms/rendu`
- **T4** `reports/archive/rapport-campagne-benefices.md             179130 o     171.6 ms/rendu`
- **T4** `reports/archive/rapport-toutes-langues.md                 302658 o     304.4 ms/rendu`
- **T4** `docs/roadmap.md                                            48983 o       0.6 ms/rendu (html 65791 o)`
- **T4** `reports/archive/rapport-campagne-benefices.md             179130 o       2.1 ms/rendu (html 241754 o)`
- **T4** `reports/archive/rapport-toutes-langues.md                 302658 o       5.4 ms/rendu (html 472469 o)`
- **T4** `démarrage 1: 132 ms`
- **T4** `démarrage 2: 131 ms`
- **T4** `démarrage 3: 127 ms`
- **T4** `docwatch --version: 0.13 s, 26596 Ko`
- **T4** `python -c import docwatch: 0.02 s, 27272 Ko`
- **T4** `reports/archive/rapport-toutes-langues.md                 302658 o       3.7 ms/rendu (html 472469 o)`
- **T4** `balayage .md: 1068 fichiers en 3.3 ms`
- **T4** `mistune (Python)                50.71 ms  (65687 o html)`
- **T4** `markdown-it-pyrs (Rust)          2.86 ms  (64551 o html)`
- **T4** `cmarkgfm (C, GFM)                2.16 ms  (64583 o html)`
- **T4** `mistune (Python)               173.55 ms  (238673 o html)`
- **T4** `markdown-it-pyrs (Rust)          9.87 ms  (235614 o html)`
- **T4** `cmarkgfm (C, GFM)                6.80 ms  (229474 o html)`
- **T4** `mistune (Python)               309.72 ms  (470048 o html)`
- **T4** `markdown-it-pyrs (Rust)         19.46 ms  (461504 o html)`
- **T4** `cmarkgfm (C, GFM)               12.50 ms  (428632 o html)`
- **T5** `..............................................F.....................     [100%]`
- **T5** `....................................................................     [100%]`
- **T5** `.....................................................................    [100%]`
- **T5** `4816b7b6 B17 — M7-BIS DANS LA CHAÎNE : LFU 9,28 % SUFFIXE VS 5,03 %, M8 COUVERTURE 70,75 %, GÉNÉRALISATION 0`
- **T6** `........................................................................ [ 96%]`
- **T6** `...                                                                      [100%]`
- **T6** `........................................................................ [ 88%]`
- **T6** `.........                                                                [100%]`
- **T6** `<svg id="my-svg" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="flowchart" style="max-width: 168px; background-color: white;" viewBox="4 4 168 146" r`
- **T6** `........................................................................ [ 82%]`
- **T6** `...............                                                          [100%]`
- **T6** `<svg id="my-svg" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="flowchart" style="max-width: 168px; background-color: whi`
- **T6** `......                                                                   [100%]`
- **T6** `root tag: <svg id="my-svg" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="flowchart" style="max-width: 168px; backgroun`
- **T6** `root: <svg id="my-svg" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="flowchart" style="max-width: 1259.11px; backg`
- **T6** `7ebd74ca B23 — ROUTEUR M1→M2 : ESPACES 41,8 % VS 11,6 %, TYPO 56,2 % < M2 68,3 % ; COLLISION DE LEXIQUE, PAS UN ORACLE`

## 5. Erreurs rencontrées

10 sorties en erreur ou divergentes. Les premières :

- **T1** : obj = import_module(mod_path)   File "/usr/lib64/python3.13/importlib/__init__.py", line 88, in import_module     return _bootstrap._gcd_import(name[level:], package, level)            ~~~~~~~~~~~~~~~
- **T1** : docs/utilisation.md | 2 +-  1 file changed, 1 insertion(+), 1 deletion(-) diff --git a/docs/utilisation.md b/docs/utilisation.md index 7ff6ec17..54fd049c 100644 --- a/docs/utilisation.md +++ b/docs/ut
- **T4** : [stderr]  [notice] A new release of pip is available: 26.2.1 -> 26.2.2 [notice] To update, run: /tmp/md-bench-venv/bin/python3 -m pip install --upgrade pip Traceback (most recent call last):   File "<
- **T5** : [stderr]  [notice] A new release of pip is available: 26.2.1 -> 26.2.2 [notice] To update, run: /tmp/cdp-venv/bin/python3 -m pip install --upgrade pip Traceback (most recent call last):   File "<stdin
- **T5** : initial: {'path': '/a.md', 'search': '', 'hash': '', 'h1': 'A'} [stderr] Traceback (most recent call last):   File "<stdin>", line 33, in <module>   File "<stdin>", line 26, in attendre   File "<stdin
- **T5** : [stderr] Author identity unknown  *** Please tell me who you are.  Run    git config --global user.email "you@example.com"   git config --global user.name "Your Name"  to set your account's default id
- **T5** : 95108777 DOCWATCH — v0.3.0 : NAVIGATION SPA, URL PROPRES, 69 TESTS 75bc27af ILLUSTRATIONS — SVG OBLIGATOIRE, 4 DIAGRAMMES ASCII CONVERTIS, 18 SCHÉMAS ACCESSIBLES ET VÉRIFIÉS (54 DOCS) 71e6035d BILAN —
- **T6** : URL: https://github.com/plantuml/plantuml/releases/download/v1.2026.9/plantuml-1.2026.9-javadoc.jar Error: Could not find or load main class net.sourceforge.plantuml.Run Caused by: java.lang.ClassNotF
- **T6** : F401 [*] `os` imported but unused  --> tests/test_diagrams.py:6:8   | 5 | import json 6 | import os   |        ^^ 7 | import re 8 | import stat   | help: Remove unused import: `os`   | 5 | import json
- **T6** : [stderr] Traceback (most recent call last):   File "<stdin>", line 29, in <module>   File "<stdin>", line 28, in attendre AssertionError: {"path": "/drave/docs/schemas/README.md", "h1": "Les sch\u00e9

## 6. Commits

- cd ~/Data13TB/stephane/GitHub/Qtrinet && ls -la .git/hooks | grep -v sample; echo "---"; ps -ef --forest | grep -A8 -B2 "git commit" | head -40
- cd ~/Data13TB/stephane/GitHub/mdserve && git config user.name "Stéphane Denis" && git config user.email "stephane@sdenis.com" && git commit --amend --reset-auth
- TESTS — LIEN ABSOLU RÉSOLU CONTRE LA RACINE ; CHANGELOG DES FICHIERS CACHÉS" && git push origin main 2>&1 | tail -3 && git log --oneline -2
- DOCS — MDSERVE : 60 TESTS (ET NON 59)" -- docs/utilisation.md && git log --oneline -1 && git show --stat --oneline HEAD | head -8 && git status --short | grep "
- CONFIG — --config-dir ET --cache-dir SONT LES RÉPERTOIRES FINAUX ; 64 TESTS" && git push origin main 2>&1 | tail -3 && git log --oneline -1
- DOCS — MDSERVE : 64 TESTS" -- docs/utilisation.md && git log --oneline -1
- DOCS — MDSERVE : 64 TESTS" -- docs/utilisation.md && git log --oneline -1 && git status --short docs/utilisation.md
- RENOMMAGE — DOCWATCH : SERVICE D'AFFICHAGE VIVANT DE COLLECTIONS DOCUMENTAIRES ; 64 TESTS  - distribution, module et commandes renommés (docwatch, docopen) - ve
- DOCWATCH — SEUL SERVEUR DE DOCUMENTATION ; SERVEUR-DOC.PY ET DRAVE-DOC RETIRÉS" -- tools/serveur-doc.py docs/utilisation.md docs/references-non-regression.md &&
- DOCS — DOCWATCH DANS EN-COURS ; B16 ET COMPTEURS 179/246" -- docs/en-cours.md && git log --oneline -1 && git show --stat --oneline HEAD | head -8; echo "--- sta
- DOCS — DOCWATCH : SAUVEGARDES DE MIGRATION" -- docs/utilisation.md && git log --oneline -1
- README — DOCWATCH EST LIBRE SUR PYPI, INSTALLATION GITHUB EN ATTENDANT" && git push origin main 2>&1 | tail -3 && git log --oneline -1
- PUBLICATION — PROCÉDURE PYPI POUR DOCWATCH ; TWINE DANS LES DÉPENDANCES DE DÉV" && git push origin main 2>&1 | tail -3 && git log --oneline -1
- DOCWATCH — SOUS-MODULE tools/docwatch ; DÉVELOPPEMENT ÉDITABLE ; CLONE ET POINTEUR DOCUMENTÉS" git log --oneline -1 git status --short .gitmodules tools/docwatc
- DOCS — DOCWATCH ÉPINGLÉ EN SOUS-MODULE DANS L'ÉTAT COURANT" -- docs/en-cours.md && git log --oneline -1
- DOCS — DOCWATCH EST LE PREMIER SOUS-MODULE, DÉPENDANCE EXTERNE ÉPINGLÉE" -- docs/modularisation.md && git log --oneline -1
- DOCS — DOCWATCH DANS LE GLOSSAIRE ET LES OUTILS ; PLUS DE RÉFÉRENCE MDSERVE" -- docs/README.md docs/glossaire.md docs/glossaire/README.md tools/glossaire_cartes
- SPA — URL PROPRE PAR DOCUMENT, CLIC SANS RECHARGEMENT, RETOUR/AVANT ; 69 TESTS  - /docs/guide.md comme URL du document courant, ?f= accepté et normalisé - inter
- SPA — URL PROPRE PAR DOCUMENT, CLIC SANS RECHARGEMENT, RETOUR/AVANT ; 69 TESTS  - /docs/guide.md comme URL du document courant, ?f= accepté et normalisé - inter
- DOCWATCH — v0.3.0 : NAVIGATION SPA, URL PROPRES, 69 TESTS" -- tools/docwatch && git log --oneline -1 && git submodule status
- MULTI-RACINES ET DIAGRAMMES — CONFIG.TOML, URLS /<MONTAGE>/, PLANTUML/MERMAID → <SOURCE>.SVG ; 87 TESTS  - [[mounts]] name/path/label, routes /mounts, URLs virt
- DOCWATCH — v0.4.0 : MULTI-RACINES ET DIAGRAMMES PLANTUML/MERMAID" -- tools/docwatch && git log --oneline -1 && git submodule status
- URLS — REDIRECTION DES DOSSIERS SANS SLASH (/second → /second/)" && git push origin main 2>&1 | tail -3 && git log --oneline -1
- VERSION 0.4.1 — CORRECTIF DE REDIRECTION DES DOSSIERS" && git push origin main 2>&1 | tail -3 && git log --oneline -1
- docwatch 0.4.1 — redirection des URLs de dossier" git push origin v0.4.1 2>&1 | tail -3 gh release create -R stephanedenis/docwatch v0.4.1 --title "docwatch v0.

