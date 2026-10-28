# UTILISER DRAVE — ce qui marche aujourd'hui, et ce qui manque

> Écrit le **16/10**, **revu le 2026-10-27**. en réponse à une question simple : « que manque-t-il pour que je puisse utiliser
> tout ça ? ». Ce document dit **ce qui s'utilise tout de suite** ✓, **la commande exacte** ✓, et
> **ce qui n'existe pas encore** ✗ — avec ce que chaque manque coûterait ✓.
> Règle de lecture : tout ce qui est ✅ a été **exécuté** le jour de l'écriture ✓ ; tout ce qui est ❌
> est un **manque constaté**, pas une supposition ✓.

## 1. ✅ Ce qui s'utilise tout de suite

### Parler au modèle — le chat

```bash
python3 tools/chat.py                       # REPL : Qwen2.5-0.5B, contexte 2048, 256 jetons/réponse
python3 tools/chat.py --modele models/Qwen2.5-0.5B-Q4_0.gguf --temp 0.9 --n 512
```

Commandes dans le REPL : `/aide`, `/reset`, `/system TEXTE`, `/temp X`, `/n X`, `/ctx X`, `/brut`,
`/quitter` ✓. **Ce que ce script corrige, et qui manquait** ✗ : `--chat` **seul ne fait rien** ✗ (le
gabarit n'est appliqué qu'avec `--prompt` ✓ — sans lui, le moteur lance un **banc de mesure** ✗✓) ; et
il n'existe **aucun mode silencieux** ✗ (la télémétrie suit la réponse ✓) → le REPL construit le
gabarit Qwen, tient l'historique, et **coupe l'instrumentation** ✓✓.

### La documentation, en ligne — **un seul serveur, `docwatch`**

[**docwatch**](https://github.com/stephanedenis/docwatch) est le **seul** serveur de documentation du
dépôt ✓. Il affiche une **collection de documents Markdown** pendant que d'autres processus les écrivent :
**arbre** de contenu ✓, **rendu** HTML ✓, **rechargement** (le navigateur interroge `/stat` toutes les 3 s ✓,
comparaison par jetons de version en 64 bits ✓), **épingles** ✓ (`/pins`,
`~/.config/docwatch/pins.json` ✓ — `docs`, `reports` et `en-cours.md` y sont ✓), **changement de racine** ✓
(ne peut que **restreindre** la vue ✗), **filtrage** ✓, **images et annexes** ✓, **navigation par URL** ✓
(`/drave/docs/guide.md`, retour/avant, liens relatifs et ancres, sans rechargement de page), **montages
multiples** ✓ (`/drave/…`, `/docwatch/…`) et **diagrammes** ✓ (`.mmd`/`.puml` → `<source>.svg`).

| quoi | valeur |
|---|---|
| adresse | **http://127.0.0.1:8771/drave/** ✓ et **http://127.0.0.1:8771/docwatch/** ✓ |
| portée | **127.0.0.1 seulement** ✗ (garantie par construction ✓) |
| dépôt | [**stephanedenis/docwatch**](https://github.com/stephanedenis/docwatch) ✓ — licence MIT, CI Python 3.9–3.13 |
| service | `docwatch.service` ✓ (`systemd --user`, `Restart=always` ✓, journal `/tmp/docwatch.log` ✓, config `~/.config/docwatch/config.toml` ✓) |
| écritures | **aucune** sur les `.md` ✓ ; seules les **épingles** et les **SVG de diagrammes générés** s'écrivent ✓ |

**Le 27/10, l'outil a été isolé de Drave** ✓✓ : code, **87 tests**, CI Python 3.9–3.13, README et licence MIT
dans [**stephanedenis/docwatch**](https://github.com/stephanedenis/docwatch). Ancien nom : `mdserve`
(paquet `mdserve-local`) ; les commandes sont désormais `docwatch` et `docopen`.

Installation et mise à jour :

```bash
pipx install --force "git+https://github.com/stephanedenis/docwatch.git"
pipx reinstall docwatch        # après une évolution du dépôt
```

Le service lance le paquet avec `--config ~/.config/docwatch/config.toml --no-browser` ✓. Il n'y a **plus de
patch hors dépôt** ✓ : les sauvegardes `~/.local/share/docwatch-migration/mdserve.*` ne servent qu'au retour
arrière ✓.

### Montages et diagrammes

La configuration `~/.config/docwatch/config.toml` déclare les montages :

```toml
[[mounts]]
name = "drave"
path = "~/Data13TB/stephane/GitHub/Qtrinet"
label = "Drave"

[[mounts]]
name = "docwatch"
path = "~/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch"
label = "docwatch"
```

Une seule instance sert donc les deux dépôts : `/drave/docs/en-cours.md` et `/docwatch/README.md` ✓.
Les épingles et le filtre temporel suivent le montage courant ✓.

Les sources **Mermaid** (`.mmd`, `.mermaid`) et **PlantUML** (`.puml`, `.pu`, `.plantuml`) sont converties
automatiquement en SVG **à côté du source**, en conservant l'extension en affixe :
`pipeline.mmd` → `pipeline.mmd.svg`, `decision.puml` → `decision.puml.svg` ✓. C'est ce que
`docs/schemas/README.md` référence ✓. Les blocs Markdown `mermaid` / `puml` sont aussi rendus, via le cache
et la route `/diagram/<hash>.<affixe>.svg` ✓. Un outil absent laisse le bloc intact ✓.

Outils installés localement : `~/.local/bin/plantuml` (JAR) et `~/.local/bin/mmdc`
(`@mermaid-js/mermaid-cli`, Chrome système) ✓. Les chemins sont dans `[diagrams]` ✓.

**Le 27/10, l'ancien `serveur-doc.py` (port 8787, `drave-doc.service`) a été retiré** ✓ : il faisait double
emploi avec docwatch et n'était pas versionnable indépendamment. La page « où en est » se lit désormais
directement dans [`docs/en-cours.md`](en-cours.md) ✓ — c'est le document épinglé à ouvrir dans docwatch ✓.
Le code reste dans l'historique Git et une sauvegarde hors dépôt ✓.

**Ce qui change pour la suite** : toute évolution de la présentation (arbre, rendu, épingles, routes) va dans
le dépôt public — il est épinglé dans **`tools/docwatch/`** comme sous-module ✓. Drave ne garde **aucun**
serveur de documentation ✓.

### Le code est un sous-module de Drave

Après un clone :

```bash
git submodule update --init --recursive
```

Pour faire évoluer une fonctionnalité :

```bash
cd tools/docwatch
pytest && ruff check .
git add -A && git commit -m "…" && git push
cd ../..
git add tools/docwatch && git commit -m "DOCWATCH — …"   # pointeur du sous-module
```

Le service tourne sur une installation **éditable** du sous-module — `pipx install --editable tools/docwatch` —
donc après une modification Python : `systemctl --user restart docwatch.service` ✓.

### Mesurer un modèle

```bash
./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl TEXTE.txt --limit 1024 --ctx 1024 --threads 8
```
Donne la **perplexité** ✓, le détail des paires poids × activation, les postes de temps ✓. C'est
l'instrument de base de tout le dépôt ✓.

### Les portes (les 49 vérifications)

```bash
bash tools/porte-tableaux.sh        # 2 s : tableaux + liens + fraîcheur de la page vivante
bash tools/porte-vision.sh          # la tour de vision, en isolation et le projecteur
bash tools/toutes-les-portes.sh     # la passe complète, ~1 h 34, écrit son REGISTRE
```
⚠️ **Ne jamais lire une porte à travers un `tail`** ✗ : le code de sortie devient celui du tuyau ✓
(leçon payée le 16/10 ✓). La passe écrit désormais `registre.txt` avec chaque code de sortie ✓.

### La vision (le banc)

```bash
DRAVE_VISION_IMAGE=image.f32 DRAVE_VISION_NOYAU=noyau.f32 \
  ./drave-core/target/release/drave models/vision/mmproj-Qwen2-VL-2B-Instruct-Q8_0.gguf --banc-vision sortie.bin
```
Le chemin image est **vérifié** ✓ (embedding exact, 31 couches à 7,58e-06 en isolation, projecteur à
0,71 % ✓) — mais ce n'est **pas encore** une vision multimodale utilisable ✗ (§ 2).

### La synthèse théorique (à lire en premier, ou en dernier)

**`docs/synthese/`** ✓ — **huit chapitres** **vulgarisés** et **quatorze schémas SVG** : l'idée fondatrice, l'anatomie
interne (régions, liens, bus, horloges), les modes d'exécution et les portes, les douze facultés et les neuf
apports de biologie, la pensée sans verbaliser (le travail du 16/10), la méthode avec ses cinq pièges, les
modèles alternatifs de l'entrée-sortie, et les opérations (la négation, la composition, la grappe).
Entrée : **`docs/synthese/index.md`** ✓.

⚠️ **Où les schémas s'affichent** ✓ : sur **docwatch** (route `/asset` et réécriture des `src`) ; si une image
reste cassée, c'est un **cache** ✗ : rechargez avec `Ctrl+Maj+R` ✓ — ou ouvrez directement le fichier
`docs/synthese/schemas/vue-ensemble.svg` ✓ (les SVG sont autonomes ✓).

### Les outils de la nuit du 16/10 (langage abstrait, empreinte, pensée itérative)

Tous sont dans `tools/`, documentés dans la fiche `reports/rapport-modele-drave.md`, et leurs pièges
d'instrument y sont **écrits à côté des chiffres** ✗✓ :

| outil | ce qu'il fait | la commande |
|---|---|---|
| `chat.py` ✓ | **parler** au modèle (REPL, historique, coupe la télémétrie) | `python3 tools/chat.py` |
| `lora_recopie.py` ✓ | apprend au modèle à **recopier** (LoRA, 100,0 % avec contrôle à 0,0 % ✓) | `python3 tools/lora_recopie.py --hf <snapshot> --ids <corpus>` |
| `empreinte.py` ✓ | l'**empreinte** du texte dans l'état, **avec contre-épreuve** ✓ | `python3 tools/empreinte.py --hf <snapshot> --ids <corpus> --lora /tmp/lora-recopie.pt` |
| `pont_abstrait.py` ✓ | le **mapping** sortie prélinguistique → entrée postlinguistique (le pont actuel ; la **RSN** visée) (+ balayage par couche et horizon ✓) | `... --hf <snapshot> --ids <corpus> [--couches … --horizons …]` |
| `pensee_silencieuse.py` ✓ | penser **sans verbaliser** (itération d'état) vs verbaliser | `... --morceau <ids> --amorces … [--pont …]` |
| `pas_latent.py` ✓ | le **pas** `h_p → h_{p+1}` : contraction et contenu | `... --hf <snapshot> --ids <corpus>` |
| `boucle_directe.py` ✓ | la boucle **sans pont** (λ, contenu) | `... --hf <modèle> --ids <corpus>` |
| `operateur_pensee.py` ✓ | l'**opérateur post-hoc** (contractant, λ = 0,997 ✓) | `... --hf <modèle aligné> --ids <corpus>` |
| `iterer_bloc.py` ✓ | **itérer** un bloc répété : contenu et déplacement ✓ | `... --partage <modèle> --distinct <témoin> --ids <corpus>` |
| **`banc_lecteur.py`** ✓ | **le banc** : λ de ridge par **validation croisée** ✓ et **batterie de longueurs** ✓ — il transforme un chiffre en **mesure** ✓✓ | `python3 tools/banc_lecteur.py --modeles A,B --ids <corpus> --longueurs 32,64,128,256` |
| **`lecteur_non_lineaire.py`** ✓ | le lecteur **MLP** (et sa leçon : mal réglé, il **sur-apprend** ✗ — 119,9 % contre 85,2 % pour le ridge ✓) | `... --modeles A,B --ids <corpus>` |

⚠️ **Ce que les mesures de la nuit ont appris sur l'instrument** ✓✓ — à lire avant de refaire une mesure :
un ridge **sous-déterminé** (moins de positions que de coefficients ✓) **interpole** et rend 0,0 % ✓✗ ;
une cible qui contient **sa propre source** (même position ✓) rend aussi 0,0 % ✓✗ ; un plan de textes qui
sort du corpus rend « n = 149 » sur 24 demandés ✓✗ ; et un **λ fixé** rend les chiffres dépendants des
réglages (**104,3** à longueur 64, **87,0** à 128 ✓✗). Dans les quatre cas, la même règle sauve la mesure :
**écrire à côté du chiffre ce qui pourrait le rendre faux** ✓✓.

Et l'entraîneur a gagné **quatre** options pour ce programme ✓ : `--alignement λ` (unifier entrée et
sortie ✓), `--partage` (bloc répété ✓), `--recurrence-max T` (entraîner **sur** l'itération ✓), et
`--kwta`/`--signes` (les contraintes biologiques ✓).

### Les facultés du « cerveau » (la recherche)

Chaque faculté a **sa fiche** (`reports/`) et **sa porte** ✓ : consolidation et sommeil (C7 ✓),
homéostasie E9 ✓, cycle C2 ✓, mémoire épisodique C6 ✓, bus C5 ✓, budgets C10 ✓, topologie C1 ✓.
Point d'entrée : le chapitre 4 de la synthèse (`docs/synthese/04-les-facultes-et-la-biologie.md`) pour la
carte courante, l'ancienne carte archivée (`docs/archive/cerveau-facultes.md`) pour l'historique, et
`tools/boucle-cerveau.sh` pour la chaîne.

### Le journal et l'état

`docs/en-cours.md` (**la page vivante** ✓, servie par le serveur ✓) et `docs/roadmap.md` (le plan) ;
l'ancien état complet est archivé (`docs/archive/etat-cerveau.md`) ; `journal/AAAA-MM-JJ.md` est le récit
du jour ✓. **Une porte vérifie que la page vivante date du dernier commit** ✓✓ : un cycle qui commite sans
la mettre à jour **échoue** ✓.

## 2. ❌ Ce qui manque, par ordre de ce que ça coûte

| # | ce qui manque | ce que ça bloque | ce que ça coûte |
|---|---|---|---|
| 1 | **un modèle plus gros** (le seul texte disponible fait **0,5 B** ✓) | toute réponse de qualité ✗ : le 0,5 B hallucine (« créé par Anthropic » ✓) et radote ✓ | télécharger un 3-7 B quantifié ✓ + vérifier la mémoire (16 Go ✓) — **le plus rentable** ✓ |
| 2 | **la vision multimodale de bout en bout** ✗ | poser une question **sur une image** ✗ — le chemin image est vérifié ✓ mais le **mRoPE** du modèle de langue manque ✗ | **cadré en 4 pas, 3 faits** ✓ (`rapport-vision-qwen2vl.md` § 4) : valeurs d'or ✓ puis branchement (une édition ✓) puis vérification ✓ |
| 3 | **un serveur d'inférence** (HTTP) ✗ | appeler Drave depuis un autre programme ✗ | il n'existe **que** le serveur de documentation ✓ ; un `--serveur` d'inférence est un ajout ✓ |
| 4 | **`--aide` et un mode silencieux dans le moteur** ✗ | la commande exacte se **découvre dans la source** ✗ | un drapeau `--silence` ✓ + une aide ✓ — petit, mais **c'est le moteur** ✓ (reconstruction + passe ✓) |
| 5 | **la pensée sans verbaliser** ✗ | penser sans passer par les jetons ✗ | **recherche, mesurée** ✓ : le langage abstrait **existe** ✓ (il bat le jeton ✓), mais **la boucle est expansive** ✗ — il faut apprendre une **dynamique contractante** ✓ (`rapport-pensee-silencieuse.md` ✓) |
| 6 | **un seul cerveau, pas de « produit »** ✗ | un usage « clé en main » des facultés ✗ | les facultés sont des **outils et des portes** ✓, pas un service ✓ — c'est un choix de conception, pas un oubli ✓ |

## 3. Le chemin le plus court vers « je peux m'en servir »

1. **`tools/chat.py`** ✓ — c'est fait, et c'est utilisable **maintenant** ✓ (avec un 0,5 B ✓) ;
2. **un modèle 3-7 B** ✓ — c'est ce qui change le plus la valeur perçue ✓ (une commande à vérifier,
   pas un développement ✓) ;
3. **le mRoPE** ✓ — c'est ce qui ouvre la vision **utilisable** ✓ (3 pas sur 4 sont faits ✓) ;
4. **`--silence` + `--aide` dans le moteur** ✓ — pour que le moteur soit **lisible** par ses utilisateurs ✓.
