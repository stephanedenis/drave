# UTILISER DRAVE — ce qui marche aujourd'hui, et ce qui manque

> Écrit le **16/10** en réponse à une question simple : « que manque-t-il pour que je puisse utiliser
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

### La documentation, en ligne — **DEUX serveurs, et ils ne servent pas la même chose**

| | **mdserve** | **`serveur-doc.py`** |
|---|---|---|
| adresse | **http://127.0.0.1:8771/** ✓ | **http://localhost:8787/** (et **192.168.1.101:8787** ✓) |
| ce que c'est | **le navigateur de documents** ✓ : **arbre** de contenu ✓, **rechargement** (le navigateur interroge `/stat` toutes les 3 s ✓, comparaison par jetons de version en 64 bits ✓), **épingles** ✓ (`/pins`, `~/.config/mdserve/pins.json` ✓ — `docs`, `reports` et `etat-cerveau.md` y sont ✓), **changement de racine** ✓ (ne peut que **restreindre** la vue ✗), **filtrage** ✓ | **la page « où en est le travail »** ✓ : `docs/en-cours.md` en premier, puis les documents de tête, la dernière passe des portes, les fiches récentes, le journal du jour ✓ |
| portée | **127.0.0.1 seulement** ✗ (garantie par construction ✓) | **0.0.0.0** ✓ — donc accessible **depuis une autre machine** ✓ |
| service | `mdserve.service` ✓ (`systemd --user`, `Restart=always` ✓, journal `/tmp/mdserve.log` ✓) | `drave-doc.service` ✓ |
| écritures | **aucune** sur les documents ✓ (lecture seule ✗ : le source n'est **jamais** ouvert en écriture ✓) ; seules les **épingles** s'écrivent ✓ | aucune ✓ |

**Décision du 17/10 : mdserve est LE viewer** ✓✓ — il a l'arbre, le rechargement (3 s), les épingles, le
filtrage **et désormais les images** ✓ (voir ci-dessous). `drave-doc` (8787) ne garde qu'un rôle : l'accès
**depuis le réseau**, que mdserve refuse par construction (il n'écoute que sur 127.0.0.1 ✓).

### Ce qui a été ajouté à mdserve pour qu'il devienne le viewer unique (17/10)

mdserve ne servait que le **Markdown** ✗ : une image écrite en syntaxe Markdown était rendue en
`<img src="schemas/x.svg">` ✓, que le navigateur demandait à la **racine du serveur** (et non au dossier du
document ✓) → 404 ✗✓. Deux ajouts, faits **hors du dépôt** (`~/.local/bin/mdserve` ✗ — c'est un outil
externe, sauvegardé en `mdserve.avant-assets` ✓) :

* une route **`/asset?path=…`** qui sert un fichier de la racine **avec son type** ✓ (`image/svg+xml` pour un
  SVG ✓, validée par `safe_path` ✓ — pas de sortie de la racine ✓) ;
* une **réécriture des `src` relatifs** vers cette route, résolus contre le **dossier du document** ✓✓.

Vérifié : `/render` sur `docs/synthese/index.md` renvoie **6 images** aux `src` réécrits ✓, et
`/asset?path=…/vue-ensemble.svg` répond **200 `image/svg+xml`** ✓.

⚠️ **Ce patch n'est pas dans le dépôt** ✗✓ : si `mdserve` est réinstallé, il sera perdu ✗. La sauvegarde
`mdserve.avant-assets` permet de revenir en arrière ✓, et le patch est décrit ici pour être **refait** ✓.

**Lequel ouvrir ?** Pour **parcourir** le dépôt (l'arbre, les épingles, le filtrage, le suivi des
modifications ✓) : **mdserve, port 8771** ✓✓. Pour **savoir en une page où en est le travail** ✓ (et y
accéder depuis une autre machine ✓) : **8787** ✓.
*Les deux tournent en service, redémarrent seuls, et relisent le disque — aucun rechargement manuel ✓.*

### Mesurer un modèle

```bash
./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl TEXTE.txt --limit 1024 --ctx 1024 --threads 8
```
Donne la **perplexité** ✓, le détail des paires poids × activation, les postes de temps ✓. C'est
l'instrument de base de tout le dépôt ✓.

### Les portes (les 46 vérifications)

```bash
bash tools/porte-tableaux.sh        # 2 s : tableaux + liens + fraîcheur de la page vivante
bash tools/porte-vision.sh          # la tour de vision, en isolation et le projecteur
bash tools/toutes-les-portes.sh     # la passe complète, ~90 min, écrit son REGISTRE
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

**`docs/synthese/`** ✓ — six chapitres **vulgarisés** et **six schémas SVG** : l'idée fondatrice, l'anatomie
interne (régions, liens, bus, horloges), les modes d'exécution et les portes, les douze facultés et les neuf
apports de biologie, la pensée sans verbaliser (le travail du 16/10), et la méthode avec ses cinq pièges.
Entrée : **`docs/synthese/index.md`** ✓.

⚠️ **Où les schémas s'affichent** ✓✗ : sur le serveur **8787** (`drave-doc`) ✓ — il sert désormais les
`.svg` avec leur **type MIME** (`image/svg+xml` ✓) ; **pas sur mdserve** ✗, qui ne rend que le markdown et
ne sert aucune fichier annexe (ses API sont `/root`, `/tree`, `/changed` ✓). Si une image reste cassée,
c'est un **cache** ✗ : rechargez avec `Ctrl+Maj+R` ✓ — ou ouvrez directement le fichier
`docs/synthese/schemas/vue-ensemble.svg` ✓ (les SVG sont autonomes ✓).

### Les outils de la nuit du 16/10 (langage abstrait, empreinte, pensée itérative)

Tous sont dans `tools/`, documentés dans la fiche `reports/rapport-modele-drave.md`, et leurs pièges
d'instrument y sont **écrits à côté des chiffres** ✗✓ :

| outil | ce qu'il fait | la commande |
|---|---|---|
| `chat.py` ✓ | **parler** au modèle (REPL, historique, coupe la télémétrie) | `python3 tools/chat.py` |
| `lora_recopie.py` ✓ | apprend au modèle à **recopier** (LoRA, 100,0 % avec contrôle à 0,0 % ✓) | `python3 tools/lora_recopie.py --hf <snapshot> --ids <corpus>` |
| `empreinte.py` ✓ | l'**empreinte** du texte dans l'état, **avec contre-épreuve** ✓ | `python3 tools/empreinte.py --hf <snapshot> --ids <corpus> --lora /tmp/lora-recopie.pt` |
| `pont_abstrait.py` ✓ | le **mapping** sortie prélinguistique → entrée postlinguistique (+ balayage par couche et horizon ✓) | `... --hf <snapshot> --ids <corpus> [--couches … --horizons …]` |
| `pensee_silencieuse.py` ✓ | penser **sans verbaliser** (itération d'état) vs verbaliser | `... --morceau <ids> --amorces … [--pont …]` |
| `pas_latent.py` ✓ | le **pas** `h_p → h_{p+1}` : contraction et contenu | `... --hf <snapshot> --ids <corpus>` |
| `boucle_directe.py` ✓ | la boucle **sans pont** (λ, contenu) | `... --hf <modèle> --ids <corpus>` |
| `operateur_pensee.py` ✓ | l'**opérateur post-hoc** (contractant, λ = 0,997 ✓) | `... --hf <modèle aligné> --ids <corpus>` |
| `iterer_bloc.py` ✓ | **itérer** un bloc répété : contenu et déplacement ✓ | `... --partage <modèle> --distinct <témoin> --ids <corpus>` |
| **`banc_lecteur.py`** ✓ | **le banc** : λ de ridge par **validation croisée** ✓ et **batterie de longueurs** ✓ — il transforme un chiffre en **mesure** ✓✓ | `python3 tools/banc_lecteur.py --modeles A,B --ids <corpus> --longueurs 32,64,128,256` |
| **`lecteur_non_lineaire.py`** ✓ | le lecteur **MLP** (et sa leçon : mal réglé, il **sur-apprend** ✗ — 119,9 % contre 85,2 % pour le ridge ✓) | `... --modeles A,B --ids <corpus>` |
| `serveur-doc.py` ✓ / **mdserve** ✓ | les deux serveurs de documentation (voir plus haut ✓) | services `drave-doc` et `mdserve` |

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
Point d'entrée : `docs/cerveau-facultes.md` (la carte ✓), `tools/boucle-cerveau.sh` (la chaîne ✓).

### Le journal et l'état

`docs/en-cours.md` (**la page vivante** ✓, servie par le serveur ✓), `docs/etat-cerveau.md` (l'état
complet ✓), `journal/AAAA-MM-JJ.md` (le récit du jour ✓). **Une porte vérifie que la page vivante date
du dernier commit** ✓✓ : un cycle qui commite sans la mettre à jour **échoue** ✓.

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
