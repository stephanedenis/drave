# Démarrage en 5 minutes

> **Ce que ce document est.** Le parcours le plus court pour installer **drave** et lancer
> les commandes. Il part d'un **clone public** et ne suppose aucun fichier du dépôt de
> développement. Chaque commande et chaque sortie ont été **rejouées le 2026-11-15** sur un
> clone neuf (commit **7f1519f**, Python **3.13.16**, pip **26.2.1**), sans clé DeepSeek.
> Le relevé complet, les temps et le contrôle négatif sont dans
> [`reports/rapport-quickstart.md`](../../reports/rapport-quickstart.md) et
> [`reports/quickstart.json`](../../reports/quickstart.json).

**Prérequis** : Python **3.10+**, `git`, un terminal. Aucun GPU, aucun modèle, aucune clé pour
le chemin par défaut : le produit est **CPU, hors ligne et déterministe**.

## 1. Cloner

```bash
git clone --recurse-submodules https://github.com/stephanedenis/drave.git
cd drave
```

> **Les sous-modules.** `tools/structures` (les données de S) et `tools/docwatch` sont des
> sous-modules ; sur cette machine leurs URLs sont **locales** (`/home/stephane/...`) et Git
> refuse le transport `file` par défaut : ajoutez `-c protocol.file.allow=always` à la commande
> (`git -c protocol.file.allow=always clone --recurse-submodules …`), ou lancez
> `git -c protocol.file.allow=always submodule update --init` après le clone. Le produit
> (`analyser`, `evaluer`, `restituer`) fonctionne **sans** eux ; seules les pages de S en ont
> besoin.

```text
Cloning into 'drave'...
```

Le clone ne télécharge **pas** les sous-modules : `tools/docwatch` et `tools/structures`
restent absents. Le CLI fonctionne sans eux ; l'écart que cela produit est dit au § 3.

## 2. Installer

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
drave --version
```

Sous Windows, la deuxième ligne est `.venv\Scripts\activate`. La sortie utile :

```text
Successfully installed drave-0.1.0
drave 0.1.0
```

L'installation est **éditable** (le paquet pointe vers le dépôt), sans dépendance d'exécution ;
`pip` a besoin du réseau ou d'un cache pour `setuptools` dans son isolation de build. Le chemin
historique `python3 tools/drave.py …` reste disponible.

## 3. Les commandes

> **Note de mesure — clone public.** Les sorties ci-dessous sont celles d'un clone **sans**
> `tools/structures` (son URL dans `.gitmodules` est un chemin local). C'est ce qu'un débutant
> obtient. Le dépôt de développement, avec ce sous-module, rend `rôle=agent`, `GV → chat`, et
> pour `evaluer` F1 **79,02 %** / attachement **99,58 %** (voir [`README.md`](README.md) § 3.1
> et § 3.3). L'écart est mesuré au § 4 de [`reports/rapport-quickstart.md`](../../reports/rapport-quickstart.md).

### 3.1 `drave --version`

```bash
drave --version
```

```text
drave 0.1.0
```

Si la commande n'existe pas, le venv n'est pas activé ou l'installation a échoué (code **127**).

### 3.2 `drave analyser "Le chat dort."`

```bash
drave analyser "Le chat dort."
```

```text
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=objet     → dort
  GV   [8:12]  dort     rôle=predicat  → —
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.35 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
```

Langue, POS, deux syntagmes avec rôle et cible, acte de parole. Les spans sont en points de
code Unicode, 0-based, fin exclue. `COUVERTURE` est la confiance **déclarée**, pas une précision.

### 3.3 `drave evaluer`

```bash
drave evaluer
```

```text
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement

POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)
SYNTAGMES   F1 81.88 %  (P 86.64 % / R 77.62 %)
  tête      F1 90.83 %  (P 96.11 % / R 86.10 %)
  vue linéaire (partition filtrer) F1 81.88 %  · attachement 93.72 % de couverture
BASE RÉELLE (hand + reel, 452 phrases)  POS 88.91 % · F1 80.14 % · attachement 91.85 %
ATTACHEMENT exact 88.70 % · couverture 93.72 % · exact sur span 94.64 % · top-k 89.54 %
  tête      couverture 100.00 % · top-k 95.54 %
PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %
FRACTION SÉMANTIQUE 54.76 %
CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)
```

`CONTRÔLE NÉGATIF` est le garde-fou : une cible au hasard trouve **1,67 %**, l'attachement
**88,70 %**. `--gold` mesure le gold gelé 602, `--reel` la base réelle 452, `--par-langue` le
détail fr/en. La commande sort **0** : elle ne teste pas la cascade.

### 3.4 Le JSON — la même analyse, en machine

```bash
drave analyser "Le chat dort." --json > annotation.json
sed -n '1,22p' annotation.json
```

```json
{
 "schema": "drave.annotation",
 "version": 2,
 "texte": "Le chat dort.",
 "langue": "fr",
 "script": "Latn",
 "source": "heuristique",
 "refus": "",
 "etiquettes": [
  {
   "niveau": "graphème",
   "type": "lettres",
   "valeur": "Le",
   "debut": 0,
   "fin": 2,
   "source": "heuristique",
   "confiance": 0.99,
   "candidats": [],
   "langue": "fr",
   "script": "Latn",
   "meta": {}
  },
```

Le JSON complet fait **5 899 octets**. Pour le consommer sans dépendance :

```bash
python3 -c 'import json; a=json.load(open("annotation.json")); print(a["schema"], a["version"], a["langue"], len(a["etiquettes"]), "étiquettes"); print([(e["type"], e["valeur"], e["meta"].get("role")) for e in a["etiquettes"] if e["niveau"]=="syntagme"])'
```

```text
drave.annotation 2 fr 20 étiquettes
[('GN', 'Le chat', 'objet'), ('GV', 'dort', 'predicat')]
```

Le contrat est **versionné** et additif : `schema`, `version`, `texte`, `langue`, `script`,
`refus`, `etiquettes`, `unites_semantiques` sont les huit champs obligatoires de la racine ; la
version 1 reste lue. Schéma : [`tools/schemas/drave-annotation-v2.json`](../../tools/schemas/drave-annotation-v2.json).

### 3.5 `drave profils` — la langue probable, le script et la confiance

```bash
drave profils --texte "Le chat dort."
drave profils --texte "Привет мир" --json
drave profils --fichier article.txt --json
drave analyser "Le chat dort." --profils
```

```text
drave 0.1.0 — profils de langue (UDHR, hors ligne)
langue=fra script=Latn confiance=0.3333 source=lexique
langue      : fra (French)
script      : Latn
confiance   : 0.3333 (marge 0.0000, seuil 0.12)
source      : lexique
prior       : fra (mots-outils 0.3333)
candidats   : hns 0.6364 · lld 0.5455 · deu 0.4545 · oci 0.4545 · pcd 0.4545
profils     : 398 langues UDHR (articles 0–14, top 200)
```

La commande charge les **398 profils UDHR** embarqués dans la roue et rend la langue probable,
le script et la confiance. Le JSON porte `langue` (décision), `langue_probable`, `script`,
`confiance`, `sous_seuil`, `source`, `prior` et `candidats`. Sous le seuil **0,12**, `langue`
est **`und`** ; la langue probable reste publiée. Un texte **long** passe par les profils ; un
texte **court** peut passer par le prior des mots-outils des sept langues du bloc (`source:
lexique`). Codes : `0` succès · `3` refus (vide) · `4` profils absents · `5` usage.

Mesure sur les **20 langues** de l'échantillon UDHR (article 15 tenu à l'écart) : **20/20**
langues et **20/20** scripts ; articles 15–30 : **313/320 = 0,9781**. Le texte ambigu bilingue
rend **`und`** (0,0836). Détail, JSON et limites :
[`rapport-profils.md`](../../reports/rapport-profils.md) ·
[`profils.json`](../../reports/profils.json).

## 4. Le tagger, en option

Le défaut est l'heuristique hors ligne, **sans réseau ni clé**. `--tagger` remplace le **POS**
par l'API DeepSeek ; sans clé, la commande refuse de démarrer :

```bash
drave analyser "Le chat dort." --tagger
```

```text
drave: dépendance absente : clé DeepSeek absente : exportez DEEPSEEK_KEY_FILE, déposez la clé dans ~/.config/drave/deepseek.key, ou exportez DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.
```

Code **4**, `stdout` vide. Avec une clé (fichier `DEEPSEEK_KEY_FILE`, puis
`~/.config/drave/deepseek.key`, puis `DEEPSEEK_API_KEY`), le même appel sort **0** et ajoute la
ligne de coût ; le reste est celui du § 3.2 :

```text
drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
...
TAGGER API  modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=0.9 s
```

Un second appel identique est servi par le cache : `réseau=0 · cache=1 · tokens=0 · latence=0.0 s`.
La clé n'apparaît **jamais**.

Le mode **`auto`** est le choix sûr : l'API si une clé existe, l'heuristique sinon, **code 0**
dans les deux cas :

```bash
drave analyser "Le chat dort." --tagger auto
```

Sans clé, `stdout` est identique au § 3.2 et `stderr` affiche
`drave: tagger auto · heuristique (clé absente)`.

## 5. Les trois erreurs courantes

**Texte vide → code 3.**

```bash
drave analyser ""
```

```text
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
```

Un refus est une **réponse** : avec `--json`, le JSON de refus part sur `stdout`
(`refus: "vide"`, `etiquettes: []`) et le code reste **3**. Même refus pour `"..."`.

**`--tagger` sans clé → code 4.** `stdout` vide, message `drave: dépendance absente : clé
DeepSeek absente …` (voir § 4). Retirer `--tagger`, ou utiliser `--tagger auto` qui replie sur
l'heuristique avec le code **0**.

**`--fichier` inexistant → code 4.**

```bash
drave analyser --fichier absent.txt
```

```text
drave: dépendance absente : fichier introuvable : 'absent.txt'
```

Pas de trace Python. Un **répertoire** à la place du fichier est un **usage invalide**
(code **5**) : `drave: erreur d'usage : un répertoire n'est pas un fichier : 'corpus/'
(--fichier attend un fichier UTF-8)`.

## 6. Les codes de sortie

| code | sens | exemple |
|---:|---|---|
| **0** | succès | `drave analyser "Le chat dort."` |
| **3** | refus d'analyse (le JSON reste valide) | texte vide ou sans lettre/chiffre |
| **4** | clé/dépendance absente | `--tagger` sans clé, clé refusée (HTTP 401/403), `--fichier absent.txt` |
| **5** | usage invalide | `--langue de`, `--fichier` sur un répertoire |
| **1** | autre erreur d'exécution | divergence de rejeu, exception inattendue |

Un réseau coupé ou un refus du modèle **ne sort pas 4** : la cascade replie sur l'heuristique,
le code reste **0**, et la cause est dans `refus`. Le **4** couvre les deux dépendances
absentes : la clé d'un `--tagger` **explicite** et un `--fichier` introuvable. `--tagger auto`
ne sort jamais 4 : il replie sur l'heuristique avec le code 0.

## 7. Et après

| si vous voulez… | allez à |
|---|---|
| la notice complète (neuf niveaux, cinq exemples, FAQ) | [`README.md`](README.md) |
| cinq JSON commentés et un cas d'échec connu | [`exemples.md`](exemples.md) |
| la fiche de ce parcours (temps, sorties, contrôle négatif) | [`reports/rapport-quickstart.md`](../../reports/rapport-quickstart.md) |
