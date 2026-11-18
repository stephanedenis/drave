# R0.7 / B13 — le lot API du tagger sur le gold 612 : la commande prête pour 11 h 30, sans appel payant

> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : préparation du lot 612 ·
> **Date** : 2026-11-18 09:32 EST · **HEAD** : `df6b9495` · **Verdict** : ✅ **prêt à lancer à
> 11:30** — le gold 612 est identifié (trois fichiers, 612 items), la clé est présente (0600,
> jamais affichée), le défaut hors ligne est prouvé **sans socket**, et le coût du lot complet
> est **87 841 tokens** (batch + évaluation), soit **0,01875 $ remisé / 0,03751 $ plein**,
> ~10 min 20 s. **Aucun appel API payant n'a été fait.**

**En trois lignes.** (1) Le « gold 612 » n'est **pas** un fichier : c'est `gold.json` (20 `hand`)
\+ `gold_reel.json` (432 `reel`) + `gold_synthetique.json` (160 `synth`), soit **612 items /
3 179 tokens** ; le corpus aplati fait **612 blocs**, sha256
`4f5231c60db991426eeabd495538b82e1c9004a492efecd34af163bba6d99c2f`. (2) La commande du lot est
le CLI `analyser --fichier … --jsonl --tagger` ; à froid, elle fera **608 appels réseau**,
**87 550 tokens** et **0,01869 $ remisé / 0,03738 $ plein** (batch seul), avec **614 lignes
JSONL** (deux phrases du gold contiennent deux phrases). (3) Le dry-run hors ligne sur 5 items
rend **0**, **5/5 JSON valides**, **0 socket** et n'importe même pas `tools.llm.deepseek` ; sans
clé, `--tagger` rend **4**, `stdout` vide, **0 socket**.

**Ce que cette fiche est, et n'est pas.**

- **Est** : la préparation exécutable du lot API du tagger sur le gold 612 — le gold exact, la
  commande exacte, la clé et son code 4, le dry-run hors ligne, le coût mesuré par les prompts
  déjà en cache, les risques et le contrôle négatif. Toutes les mesures de cette fiche sont
  **locales** (fichiers, CLI, cache) ; **aucune** requête n'est partie vers l'API de modèle
  (`api.deepseek.com/chat/completions`) — la page publique de tarifs a seulement été lue en
  **GET**, comme la tâche l'autorise.
- **N'est pas** : le run payant (il est à lancer à 11:30), ni une nouvelle mesure de qualité du
  tagger (elle sera dans `evaluer --tagger --json` le jour du run), ni une modification du code,
  des golds, de `docs/pilotage/en-cours.md`, de `docs/pilotage/roadmap.md` ou d'`AGENTS.md`.
- **Public** : la personne qui lance le lot à 11:30, et la ligne **R0.7/B13**.

## 1. Le gold 612 : trois fichiers, pas un `gold_612.json`

Il n'existe **aucun** fichier `gold_612.json` dans le dépôt. Le 612 est la concaténation, dans
cet ordre, des trois golds du bloc linguistique :

| fichier | `source` | phrases | tokens (mots du gold) | rôle |
|---|---|---:|---:|---|
| [`tools/tests/linguistique/gold.json`](../tools/tests/linguistique/gold.json) | `hand` | **20** | 105 | les 20 phrases de référence |
| [`tools/tests/linguistique/gold_reel.json`](../tools/tests/linguistique/gold_reel.json) | `reel` | **432** | 2 375 | le gold réel (228 fr + 204 en) |
| [`tools/tests/linguistique/gold_synthetique.json`](../tools/tests/linguistique/gold_synthetique.json) | `synth` | **160** | 699 | les 160 phrases synthétiques |
| **total** | | **612** | **3 179** | le « gold vivant » de `evaluer` |

- **Le gold 452** est le sous-ensemble `hand + reel` (20 + 432) ; c'est la base de
  `evaluer --reel` et de [`rapport-gold-452.md`](rapport-gold-452.md). Le 612 **ajoute 160
  phrases synthétiques** : le 612 n'est pas « le réel », c'est le vivant. `gold_reel.json` fait
  **432** ; la base `--reel` (hand + reel) fait **452**.
- **Le fichier `reports/tagger-612.json`** est une **mesure** du 13/11 (612 phrases, six modes,
  1 218 appels, 358 962 tokens), **pas** le gold. Ne pas le confondre avec une source.
- **Le corpus aplati** (une phrase par bloc, une ligne vide entre deux blocs) fait **612 blocs**,
  **17 782 octets**, sha256 `4f5231c6…`. Il se reconstruit en 10 lignes de Python (§ 6).
- **609 textes distincts** : trois textes sont en double (`Le vent souffle fort.`,
  `La voiture roule vite.`, `Paul sees Marie; he speaks to her.`).
- **606 prompts distincts** pour le tagger en mode direct (les 612 items) ; **614 segments** et
  **608 prompts distincts** pour le CLI `--jsonl`, parce que **deux phrases contiennent deux
  phrases** (`r308` « Marie lit. Elle aime les livres. » et `r318` « Marie reads. She loves
  books. »). Le CLI les coupe : c'est la source des 614 lignes, pas un bug.

**Ce que le CLI `evaluer` appelle le gold 612.** `python3 tools/drave.py evaluer --json` charge
les trois fichiers et publie `gold = {phrases: 612, tokens: 3179, nom: "vivant (hand + reel +
synthétique)"}`. C'est la définition à utiliser dans la fiche R0.7.

## 2. Le tagger et les commandes déjà utilisées

### 2.1 La chaîne réelle

| maillon | fichier | rôle |
|---|---|---|
| CLI | [`tools/drave.py`](../tools/drave.py) | `--tagger`, `_construire_tagger`, `_cascade_tagger`, `_transport_tagger`, `_cle_tagger` |
| tagger | [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) | `NeuronalLLMPOS` : l'invite POS, le contrat JSON, le cache mémoire `(texte, langue)` |
| client | [`tools/llm/deepseek.py`](../tools/llm/deepseek.py) | la requête, le cache disque `DEEPSEEK_CACHE`, la lecture de la clé |
| **pas le tagger** | [`tools/llm/enseignant.py`](../tools/llm/enseignant.py) | le corpus du **professeur** (prompts publics → JSONL, `--limite`, `--dry-run`) ; aucun `tagger` |

Le câblage est **un appel par phrase** depuis le 15/11 : `_cascade_tagger` ne construit que
`NeuronalLLMPOS` (le tagger de syntagmes a été retiré) ; le POS vient du neuronal, les syntagmes,
rôles, l'attachement et la pragmatique restent à l'heuristique. `evaluer --tagger` mesure la
cascade et publie le Δ et le coût.

### 2.2 Les commandes déjà utilisées sur le 612

| commande | quoi | chiffre | source |
|---|---|---|---|
| `DEEPSEEK_KEY_FILE=… DEEPSEEK_CACHE="$(mktemp -d …)" DEEPSEEK_MODEL=deepseek-chat PYTHONPATH=. python3 tools/tests/linguistique/qualifier_tagger_612.py --sortie /tmp/tagger-612.json` | le run 612 **à deux appels/phrase** (POS + syntagmes) | **1 218 appels**, **358 962 tokens**, **1 257,96 s**, refus 1 (`s015`) | [`rapport-coordination-r.md`](rapport-coordination-r.md) § 6.2 · [`tagger-612.json`](tagger-612.json) |
| `python3 tools/drave.py evaluer --tagger --json` | la qualité et le Δ sur le 612, **un appel/phrase** | 609 appels, 22 299 tokens, 155 s (cache partiel) ; POS **0,9575** contre 0,8625 | [`rapport-tagger-option.md`](rapport-tagger-option.md) § 1 bis |
| `python3 tools/drave.py analyser --fichier corpus-1000.txt --jsonl --tagger` | le lot X3 de 1 000 items | 672 requêtes, 99 971 tokens, 685,2 s, 0,02177 $ hors pointe | [`rapport-tagger-lot.md`](rapport-tagger-lot.md) § 6 |
| `python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode froid …` | le banc X3 (froid/chaud/fusion) | 1 000 items, 677 textes, 672 appels | [`rapport-tagger-lot.md`](rapport-tagger-lot.md) |

**Le piège à éviter.** `qualifier_tagger_612.py` est l'ancien chemin **à deux appels par
phrase** : il coûte **358 962 tokens** et ~21 min, soit **4,1×** le câblage actuel. Ce n'est
**pas** la commande du lot 11:30 ; c'est une référence historique. La commande du lot est le CLI
`analyser --fichier … --jsonl --tagger` (le même chemin que X3, un appel par phrase).

## 3. La clé, vérifiée sans appel

### 3.1 Où le client lit la clé

Le CLI appelle `drave._cle_tagger()`, dans cet ordre :

1. `DEEPSEEK_KEY_FILE` (un **chemin** de fichier, pas la clé) ;
2. `DSH_KEY_FILE` ;
3. `~/.config/drave/deepseek.key` ;
4. `DEEPSEEK_API_KEY` (la clé en variable d'environnement) ;
5. `DSH_API_KEY`.

Le module `tools/llm/deepseek.py` a, **quand on l'utilise seul**, un ordre différent
(`DEEPSEEK_API_KEY` d'abord, puis `DEEPSEEK_KEY_FILE`). Le CLI **passe la clé explicitement** à
`DeepSeek(cle=…)` : c'est donc l'ordre de `drave.py` qui fait foi pour le tagger. Pour éviter
toute ambiguïté, le run n'exporte **que** `DEEPSEEK_KEY_FILE`.

**État réel de la machine (vérifié sans afficher la clé) :**

| source | état |
|---|---|
| `DEEPSEEK_KEY_FILE`, `DSH_KEY_FILE`, `DEEPSEEK_API_KEY`, `DSH_API_KEY` | **non définies** |
| `~/.config/drave/deepseek.key` | **présent**, lisible, **0600**, 36 octets |
| `_cle_tagger()` | **clé trouvée** (35 caractères, jamais affichée) |
| `DEEPSEEK_CACHE` | non définie → défaut `data/deepseek/cache` (**3 759 fichiers**) |
| `DEEPSEEK_MODEL` | non définie → défaut `deepseek-chat` |
| base | `https://api.deepseek.com` |

### 3.2 La matrice sans clé (le code 4)

Les commandes suivantes tournent dans un `HOME` **vide** et un environnement **sans aucune
variable DeepSeek** ; elles ne peuvent donc pas trouver la clé réelle :

```bash
tmp=$(mktemp -d)
env -i HOME="$tmp" PATH="$PATH" python3 tools/drave.py analyser --tagger "Le chat dort." --json
echo "code=$?"          # attendu 4, stdout vide
env -i HOME="$tmp" PATH="$PATH" python3 tools/drave.py evaluer --tagger --json
echo "code=$?"          # attendu 4, stdout vide
env -i HOME="$tmp" PATH="$PATH" python3 tools/drave.py analyser "Le chat dort." --json
echo "code=$?"          # attendu 0, source=heuristique
```

| cas | code | `stdout` | `stderr` | socket |
|---|---:|---:|---|---:|
| défaut, 5 items, `--jsonl` | **0** | 51 207 o, 5 JSON | vide | **0** |
| défaut, une phrase, `--json` | **0** | 6 179 o, `source=heuristique` | vide | **0** |
| `--tagger` sans clé | **4** | **0 o** | « clé DeepSeek absente : exportez DEEPSEEK_KEY_FILE… » | **0** |
| `evaluer --tagger` sans clé | **4** | **0 o** | le même message | **0** |

Le `--tagger` sans clé **importe** `tools.llm.deepseek` (l'import est local dans
`_client_tagger`) mais **ne construit aucune socket** : la clé est refusée avant le transport.
Le **défaut** (sans `--tagger`) n'importe même pas le module réseau. C'est la frontière W3 :
**une dépendance absente = code 4** ; un réseau coupé ou un refus du modèle = repli, code 0,
avec la cause dans `refus`.

## 4. Le dry-run hors ligne

### 4.1 La commande exacte, sans `--tagger`

Le corpus de 5 items est le début du corpus 612 (les 5 premiers `hand`) :

```bash
python3 - <<'PY'
import pathlib
corpus = pathlib.Path("/tmp/tagger-612/corpus-gold-612.txt").read_text(encoding="utf-8")
blocs = [b for b in corpus.split("\n\n") if b.strip()]
assert len(blocs) == 612, len(blocs)
pathlib.Path("/tmp/tagger-612/corpus-gold-5.txt").write_text(
    "\n\n".join(blocs[:5]) + "\n", encoding="utf-8")
print("5 items :", blocs[:5])
PY
env -i HOME="$(mktemp -d)" PATH="$PATH" \
  python3 tools/drave.py analyser --fichier /tmp/tagger-612/corpus-gold-5.txt --jsonl
```

C'est **la commande du lot privée de `--tagger`** : même `--fichier`, même `--jsonl`, même
segmenteur, même sortie JSON, mais le défaut heuristique. Aucun appel réseau n'est possible.

### 4.2 Le résultat observé (2026-11-18 09:24 EST)

| mesure | valeur |
|---|---:|
| code | **0** |
| lignes JSONL | **5** |
| JSON valides | **5 / 5** |
| `stdout` | 51 207 octets |
| `stderr` | **vide** |
| sockets construites | **0** (piège `socket.socket`, `create_connection`, `socketpair`) |
| `tools.llm.deepseek` importé | **non** |
| sha256 de la sortie | `2c4b723e3b0976112114daf5049c1af0ee5a5ba49f82c59d0eefe91f039646ba` |

Les 5 annotations sont bien celles de l'heuristique, par exemple :

| texte | POS (extrait) |
|---|---|
| `Le chat dort.` | `Le/DET chat/NOUN dort/VERB ./PONCT` |
| `La femme a vu l'homme dans le parc.` | `La/DET femme/NOUN a/PREP vu/VERB l'/DET homme/NOUN dans/PREP le/DET parc/NOUN ./PONCT` |

Le JSON complet (les 5 annotations, les quatre cas, le piège à sockets) est dans
[`reports/tagger-612-dryrun-5.json`](tagger-612-dryrun-5.json). Le script de mesure est dans
`/tmp/tagger-612/dryrun_612.py` (hors dépôt).

### 4.3 La passe complète 612 hors ligne (contrôle de forme)

Pour vérifier le **pipeline complet**, la même commande a été lancée sur les 612 items, toujours
sans clé :

| mesure | valeur |
|---|---:|
| code | **0** |
| lignes JSONL | **614** (612 items + `r308` et `r318` coupés en deux) |
| JSON valides | **614 / 614** |
| durée | **0,85 s** |
| pic RSS | 33 612 kio |
| `stdout` | 4 747 475 octets |
| sha256 | `de4b0a22a6b02262205eba5b4575649443ceb924e3bd002db922cfe563a8da6e` |

C'est le **format attendu** du lot payant : 614 lignes, pas 612. La passe payante fera les mêmes
614 lignes, avec `source=cascade` et le POS neuronal.

### 4.4 Les tests du tagger (transport factice)

`python3 tools/tests/test_tagger_api.py` : **30 tests**, **30 OK**, **6,569 s**, **0 réseau**
(le transport est factice ; le test W3 `test_defaut_n_ouvre_aucune_socket` piège la socket).
Les tests couvrent le défaut, le code 4, la clé invalide 401/403, le réseau coupé, le refus du
modèle, le cache, `evaluer --tagger` et le mode `auto`.

## 5. Le coût du lot complet

### 5.1 La base mesurée

Le lot CLI fait **614 segments** ; ils donnent **608 prompts distincts** (6 collisions : 3 textes
en double + 3 variantes de ponctuation). Les 608 prompts sont **tous présents dans le cache X3**
`/tmp/tagger-lot-fiab-cache` (676 fichiers : 672 du froid + 4 du `--jsonl`), avec leur `usage`
exact. La somme est donc **mesurée**, pas extrapolée :

| jeu de prompts | prompts | appels réseau à froid | entrée | sortie | **tokens** | remisé | plein | latence réseau |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **batch CLI** (614 segments) | 608 | 608 | 75 200 | 12 350 | **87 550** | **0,018690 $** | **0,037380 $** | 610,8 s |
| **évaluation** (612 items) | 606 | 606 | 74 988 | 12 340 | **87 328** | 0,018652 $ | 0,037304 $ | 608,8 s |
| **union** (batch + éval, cache partagé) | **610** | **610** | **75 448** | **12 393** | **87 841** | **0,018753 $** | **0,037506 $** | 612,9 s |

**Le chiffre à retenir** : le lot complet (batch **et** évaluation, un seul cache neuf) coûte
**87 841 tokens**, **610 appels réseau**, **0,01875 $ remisé / 0,03751 $ plein**, pour
**~10 min 20 s** de réseau (610 × 1,019 s/appel + ~5 s de surcoût local). Le batch seul coûte
**0,01869 $ remisé / 0,03738 $ plein**. Le run démarre à 11:30, finit vers 11:41.

**Par item** : 143,53 tokens, **0,0000306 $ remisé / 0,0000613 $ plein** (batch + éval).
**Par appel réseau** : 144,0 tokens. **Extrapolé à 1 000 items** : 143 531 tokens,
**0,03064 $ remisé / 0,06129 $ plein** — à comparer au **0,032157 $ / 0,064315 $** de X3 pour
1 000 textes uniques : le gold est un peu plus court (−4,7 %), c'est cohérent.

### 5.2 Pourquoi la règle de trois « 612 / 1 000 » est un piège

Le rapport X3 donne **672 appels / 99 971 tokens / 0,02177 $** pour **1 000 items**. Une règle de
trois par **item** donnerait **61 182 tokens / 0,01332 $** : c'est un **plancher faux**, parce que
le lot X3 de 1 000 items contient **319 répétitions et 4 doublons** (32,6 % de cache) alors que
le gold 612 n'a que **6 collisions** (1 %). La bonne échelle est l'**appel réseau**, pas l'item :

| méthode | tokens | appels | remisé | plein | lecture |
|---|---:|---:|---:|---:|---|
| X3 mesuré, 1 000 items | 99 971 | 672 | 0,021770 $ | 0,043541 $ | la référence |
| règle de trois **par item** (612/1000) | 61 182 | 411 | 0,01332 $ | 0,02665 $ | **faux** : suppose 32,6 % de cache |
| règle de trois **par appel** (608/672) | 90 450 | 608 | 0,01970 $ | 0,03939 $ | proche, +3 % (prompts plus courts) |
| **somme exacte des 610 prompts** | **87 841** | **610** | **0,01875 $** | **0,03751 $** | **le chiffre du run** |

### 5.3 Le tarif, à la page du 2026-11-18

La page officielle [Models & Pricing](https://api-docs.deepseek.com/quick_start/pricing) a été
consultée le 2026-11-18 (lecture seule, aucun appel API). Elle donne, pour `deepseek-flash` :

| poste | hors pointe (remisé) | pointe (plein) |
|---|---:|---:|
| entrée, cache miss | **0,15 $ / M** | **0,30 $ / M** |
| entrée, cache hit | 0,003 $ / M | 0,006 $ / M |
| sortie | **0,60 $ / M** | **1,20 $ / M** |

Ce sont **exactement** les prix du 2026-11-13 repris par X3. La page précise que les heures de
pointe sont **01:00–04:00 et 06:00–10:00 UTC, du lundi au vendredi** (les autres heures, dont
les week-ends, sont hors pointe) ; **11:30 EST = 16:30 UTC** est donc hors pointe. La règle 12 du
dépôt (`docs/pilotage/plans-tarif.md`) donne une fenêtre plus étroite (**11:30 → 19:30 EST**) :
elle est **incluse** dans l'hors-pointe de la page, donc le run de 11:30 est remisé dans les deux
lectures. Le modèle demandé est `deepseek-chat` ; la page confirme que l'alias est servi par
**DeepSeek-V4.1-Flash-1017** et facturé au prix Flash — c'est le `deepseek-flash` des 608
fichiers de cache.

### 5.4 Le cache : neuf, ou le run est un rejeu

| cache | prompts du batch présents | ce que ferait le run |
|---|---:|---|
| **neuf** (`mktemp -d`) | 0 / 608 | **608 appels**, **87 550 tokens**, **0,01869 $** — la mesure |
| défaut `data/deepseek/cache` | 604 / 608 | 4 appels, **~513 tokens**, ~0 $ — rejeu partiel des réponses du 03–15/11 |
| X3 `/tmp/tagger-lot-fiab-cache` | **608 / 608** | **0 appel, 0 token, 0 $** — rejeu exact du 15/11 |

**Le cache par défaut n'est pas « gratuit » pour ce lot** : 4 des 608 prompts manquent (les
quatre moitiés de `r308`/`r318`). Le cache X3, lui, est complet, mais il **rejoue** les réponses
du 15/11 : c'est un **contrôle négatif** (mêmes entrées, 0 réseau), pas une nouvelle mesure. Le
run de 11:30 doit donc utiliser un **cache neuf** pour mesurer le modèle du jour.

## 6. La commande exacte à lancer à 11 h 30

Le bloc ci-dessous est **copiable** ; il vérifie l'heure, la clé, le corpus, lance le batch,
valide le JSONL, lance l'évaluation et audite le coût. Il n'affiche **jamais** la clé.

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet

# 0. La fenêtre et la clé (aucun appel API ici)
now=$(date +%H%M)
if (( 10#$now < 1130 )); then echo "AVANT 11:30 : ne pas lancer"; exit 1; fi
if (( 10#$now >= 1930 )); then echo "APRÈS 19:30 : tarif plein"; exit 1; fi
test -r "$HOME/.config/drave/deepseek.key" && echo "CLE-OK (fichier lisible)"
test "$(stat -c '%a' "$HOME/.config/drave/deepseek.key")" = "600" && echo "CLE-0600"

# 1. Le corpus 612 (hors ligne, reproductible)
mkdir -p /tmp/tagger-612
python3 - <<'PY'
import hashlib, json, pathlib
racine = pathlib.Path("tools/tests/linguistique")
items = []
for nom, source in (("gold.json", "hand"), ("gold_reel.json", "reel"),
                    ("gold_synthetique.json", "synth")):
    for p in json.loads((racine / nom).read_text(encoding="utf-8"))["phrases"]:
        items.append({"id": p["id"], "source": source,
                      "langue": p.get("langue") or "fr",
                      "texte": " ".join(p["texte"].split())})
assert len(items) == 612, len(items)
assert [sum(1 for i in items if i["source"] == s) for s in ("hand", "reel", "synth")] == [20, 432, 160]
corpus = "\n\n".join(i["texte"] for i in items) + "\n"
pathlib.Path("/tmp/tagger-612/corpus-gold-612.txt").write_text(corpus, encoding="utf-8")
pathlib.Path("/tmp/tagger-612/attendu-612.json").write_text(
    json.dumps(items, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("items", len(items), "sha256", hashlib.sha256(corpus.encode()).hexdigest())
PY
# attendu : items 612 sha256 4f5231c60db991426eeabd495538b82e1c9004a492efecd34af163bba6d99c2f
test "$(sha256sum /tmp/tagger-612/corpus-gold-612.txt | cut -d' ' -f1)" = \
  "4f5231c60db991426eeabd495538b82e1c9004a492efecd34af163bba6d99c2f" \
  || { echo "CORPUS INATTENDU : arrêt"; exit 1; }

# 2. Le batch payant : 614 segments, 608 appels réseau à froid
export DEEPSEEK_KEY_FILE="$HOME/.config/drave/deepseek.key"
export DEEPSEEK_MODEL=deepseek-chat
export DEEPSEEK_CACHE="$(mktemp -d /tmp/tagger-612-cache.XXXXXX)"
echo "cache=$DEEPSEEK_CACHE"
/usr/bin/time -v python3 tools/drave.py analyser \
  --fichier /tmp/tagger-612/corpus-gold-612.txt \
  --jsonl --tagger \
  > /tmp/tagger-612/lot.jsonl 2> /tmp/tagger-612/lot.err
code=$?
echo "code=$code"
grep -E "TAGGER API|Elapsed|Maximum resident" /tmp/tagger-612/lot.err || true
# attendu : code=0 · TAGGER API · modèle=deepseek-chat · appels=611 · réseau=608 ·
#           cache=3 · tokens=87550 · latence=610.8 s · Elapsed ~10:20
# SI réseau=0 ou tokens=0 : le cache était chaud, ce n'est pas une mesure neuve → relancer.
# SI code=4 : la clé est refusée → ne rien publier, vérifier le fichier.
# SI tokens < 50000 ou refus > 20 : le tagger a replié → lire lot.err, relancer.

# 3. Le JSONL : 614 lignes, 614 JSON valides
python3 - <<'PY'
import collections, json, pathlib
p = pathlib.Path("/tmp/tagger-612/lot.jsonl")
lignes = [l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
assert len(lignes) == 614, f"lignes {len(lignes)} != 614"
annotations = [json.loads(l) for l in lignes]
assert all(a.get("schema") == "drave.annotation" for a in annotations)
refus = [a for a in annotations if a.get("refus")]
pos_n = sum(1 for a in annotations for e in a["etiquettes"]
            if e["niveau"] == "pos" and e["source"] == "neuronal")
pos_t = sum(1 for a in annotations for e in a["etiquettes"] if e["niveau"] == "pos")
print("614/614 JSON valides ·", p.stat().st_size, "octets")
print("sources", collections.Counter(a.get("source") for a in annotations))
print("refus", len(refus), [a.get("texte") for a in refus][:5])
print("POS neuronal", pos_n, "/", pos_t)
PY

# 4. L'évaluation R0.7 : qualité et Δ, avec le MÊME cache (2 appels neufs seulement)
python3 tools/drave.py evaluer --tagger --json \
  > /tmp/tagger-612/eval.json 2> /tmp/tagger-612/eval.err
echo "code=$?"
grep "TAGGER API" /tmp/tagger-612/eval.err || true
python3 - <<'PY'
import json
d = json.load(open("/tmp/tagger-612/eval.json"))
print("POS heuristique", d["heuristique"]["pos"]["exactitude"])
print("POS tagger", d["tagger"]["pos"]["exactitude"], "Δ", d["tagger"]["delta_pos"])
print("tagger.refus", d["tagger"]["refus"], d["tagger"]["refus_detail"])
print("tagger.cout", d["tagger"]["cout"])
print("ATTENTION : cout_pour_1000_phrases est chaud (291 tokens mesurés, extrapolé à ~475)")
PY

# 5. L'audit du coût : la somme des usage dans le cache neuf
python3 - <<'PY'
import json, os, pathlib
cache = pathlib.Path(os.environ["DEEPSEEK_CACHE"])
pin = pout = 0
for f in cache.glob("*.json"):
    u = json.loads(f.read_text(encoding="utf-8")).get("usage", {})
    pin += int(u.get("prompt_tokens", 0) or 0)
    pout += int(u.get("completion_tokens", 0) or 0)
print(f"fichiers={len(list(cache.glob('*.json')))} entrée={pin} sortie={pout} total={pin + pout}")
print(f"remisé={(pin*0.15 + pout*0.60)/1e6:.6f} $ · plein={(pin*0.30 + pout*1.20)/1e6:.6f} $")
PY
# attendu : fichiers=610 entrée=75448 sortie=12393 total=87841
#           remisé=0.018753 $ · plein=0.037506 $

# 6. Les résultats (à copier dans reports/ seulement après les contrôles)
cp /tmp/tagger-612/lot.jsonl reports/tagger-612-lot.jsonl
cp /tmp/tagger-612/lot.err  reports/tagger-612-lot.err.txt
cp /tmp/tagger-612/eval.json reports/tagger-612-eval.json
cp /tmp/tagger-612/eval.err  reports/tagger-612-eval.err.txt
```

**Si l'on ne veut que la qualité R0.7**, l'étape 4 seule avec un cache neuf suffit (exporter
`DEEPSEEK_KEY_FILE` et un `DEEPSEEK_CACHE` vide) : `evaluer --tagger --json` fait **606 appels**,
**87 328 tokens**, **0,01865 $ remisé / 0,03730 $ plein**, ~10 min. Mais elle ne produit pas le
JSONL du corpus. Le bloc complet (batch puis éval) est la recommandation : le batch produit le
corpus, l'éval publie la qualité, et le cache partagé fait payer l'éval **2 appels** (les deux
phrases entières `r308`/`r318`).

**Ce qu'on attend dans `eval.json`.** L'heuristique à HEAD vaut **0,8625** (mesuré le 18/11,
`evaluer --json` hors ligne : fermé 0,9373, ouvert 0,7918, 3 179 tokens). Le tagger est attendu
autour de **0,95** (0,9475 le 13/11 à deux appels, 0,9575 le 15/11 avec cache partiel) ; le Δ
attendu est **+8,5 à +9,5 points**. Le chiffre **0,8500** de `rapport-etat-r.md` n'est plus celui
du HEAD : `evaluer --json` mesure 0,8625. La fiche R0.7 doit publier le chiffre du jour, pas
0,8500.

## 7. Les risques, et ce qu'on fait

| risque | ce qu'on verrait | action |
|---|---|---|
| **clé absente** | code 4, `stdout` vide, « clé DeepSeek absente… » | ne pas lancer ; vérifier `test -r` et le mode 0600 ; le défaut reste hors ligne |
| **clé refusée (401/403)** | code 4, `stdout` **partiel** (les lignes déjà écrites), message « clé refusée (HTTP 401) » | ne rien publier ; vérifier la clé ; le code 4 n'est pas un repli |
| **quota / 429** | code **0**, `refus` élevé, `tokens` bas, `réseau` bas | le client fait 3 essais (1 s + 2 s) puis replie sur l'heuristique ; si `tokens < 50 000` ou `refus > 20`, relancer plus tard |
| **format** | 614 lignes, pas 612 ; `r308`/`r318` coupés | attendu ; ne pas « corriger » le corpus ; le JSONL n'a pas d'`id`, l'éval a les `id` |
| **refus partiel** | 1 refus attendu (`s015` sur l'ancien 612) ; `refus` dans la ligne | la cascade replie sur l'heuristique, le code reste 0 ; compter les refus |
| **cache chaud** | `réseau=0`, `tokens=0`, `cache` élevé | ce n'est pas une mesure neuve ; relancer avec un `DEEPSEEK_CACHE` neuf |
| **`cout_pour_1000_phrases`** | l'éval affiche ~475 tokens (291 × 1000/612) | c'est le coût **chaud** de l'éval ; le coût du lot est dans `lot.err` et l'audit du cache |
| **modèle / prix** | `deepseek-chat` demandé, `deepseek-flash` renvoyé ; la page peut changer | le dollar bouge, pas les tokens ; vérifier la page avant un gros lot |
| **fenêtre** | avant 11:30 = plein tarif ; après 19:30 = plein tarif | le bloc vérifie l'heure ; le run dure ~10 min |
| **clé dans un fichier** | une clé dans `lot.err`, `eval.json` ou un cache | jamais : le client ne l'écrit pas, les messages la masquent ; ne pas `cat` le fichier |
| **`/tmp` vidé** | corpus absent ou sha256 différent | relancer l'étape 1 ; le sha256 est le garde-fou |
| **vieux harnais** | `qualifier_tagger_612.py` : 1 218 appels, 358 962 tokens, ~21 min | ne pas l'utiliser ; c'est l'ancien chemin à deux appels |
| **`--tagger auto`** | `evaluer --tagger auto` rend 5 (usage) | utiliser `--tagger` explicite ; `auto` est un prototype d'`analyser` |

**Le risque le plus sournois est le quota.** Un 429 n'est pas un 401 : le client le classe
`reessayable`, fait trois essais, puis lève `ErreurDeepSeek` ; la cascade **replie** sur
l'heuristique et le CLI rend **0**. Un lot qui « réussit » avec `tokens=0` et beaucoup de
`refus` n'est pas un lot taggé. Les contrôles des étapes 2 et 3 sont là pour l'attraper.

## 8. Le contrôle négatif : le défaut ne doit rien appeler

| contrôle | commande | code | `stdout` | socket | `deepseek` importé |
|---|---|---:|---:|---:|---|
| **défaut, 5 items** | `analyser --fichier corpus-gold-5.txt --jsonl` (HOME vide) | **0** | 5 JSON valides | **0** | **non** |
| **défaut, 1 phrase** | `analyser "Le chat dort." --json` (HOME vide) | **0** | `source=heuristique` | **0** | **non** |
| **`--tagger` sans clé** | `analyser "Le chat dort." --tagger --json` (HOME vide) | **4** | **0 o** | **0** | oui (import local, aucun socket) |
| **`evaluer --tagger` sans clé** | `evaluer --tagger --json` (HOME vide) | **4** | **0 o** | **0** | oui (import local, aucun socket) |
| **passe 612 hors ligne** | `analyser --fichier corpus-gold-612.txt --jsonl` (HOME vide) | **0** | **614 / 614** JSON | **0** | **non** |

Le piège est un `socket.socket` / `socket.create_connection` / `socket.socketpair` qui **lève** :
le dry-run complet (5 items, une phrase, `--tagger` sans clé, `evaluer --tagger` sans clé) a
rendu **0 tentative**. Les **30 tests** du tagger, à transport factice, ont rendu **30/30**,
**0 réseau**. C'est le contrôle exigé : **le défaut hors ligne ne peut pas appeler**, et le code
4 du `--tagger` sans clé est une **dépendance absente**, pas un appel déguisé.

## 9. Ce qui pourrait rendre l'estimation fausse

- **La base X3 est du 15/11.** Les 608 prompts sont dans le cache X3 avec leur `usage` exact ;
  un changement de prompt, de tokenisation ou de modèle déplace les tokens. Le câblage est
  inchangé depuis X3 (`git diff e1a28307..HEAD` ne touche ni `NeuronalLLMPOS`, ni `_mots`, ni
  `CLASSES_POS`), mais le **modèle du 18/11** peut rendre des sorties un peu différentes.
- **Les tokens de sortie ne sont pas déterministes.** L'entrée (le prompt) est stable ; la
  sortie peut varier de quelques pour cent. L'estimation à **87 841 tokens** est une mesure du
  15/11, pas une garantie du 18/11 ; l'audit du cache donne le chiffre réel.
- **Le lot 612 n'est pas le réel 452.** 160 phrases sont synthétiques, plus courtes et plus
  faciles ; le coût par item du réel seul peut différer. Le chiffre vaut pour le gold 612.
- **Les deux phrases coupées.** `r308` et `r318` sont **coupées en deux** par le CLI `--jsonl` ;
  c'est pourquoi le lot fait 614 lignes et 608 prompts, pas 612/606. L'évaluation, elle, garde
  les 612 items et les 606 prompts.
- **Le tarif n'est pas figé.** La page du 18/11 confirme les prix du 13/11 ; un changement de
  routage, de modèle ou de tarif déplace le dollar, pas les tokens.
- **Le cache est daté.** Le cache X3 rejoue le modèle du 15/11 ; un cache neuf mesure celui du
  18/11. Les deux ont le même `deepseek-flash` aujourd'hui, mais ce n'est pas garanti.
- **La latence est séquentielle.** 610 appels × ~1,02 s = ~10 min 20 s ; une API plus lente ou
  un réseau chargé allonge, pas le prix.
- **Un refus.** L'ancien 612 avait **1 refus** (`s015`) ; le lot peut en avoir 0 à 2. La cascade
  replie et le code reste 0 ; le chiffre de qualité doit être lu avec `tagger.refus`.

## 10. Les fichiers

| fichier | rôle |
|---|---|
| [`reports/rapport-tagger-lot-612-prep.md`](rapport-tagger-lot-612-prep.md) | cette fiche |
| [`reports/tagger-612-dryrun-5.json`](tagger-612-dryrun-5.json) | le JSON du dry-run (5 annotations, 0 socket, les 4 cas) |
| `/tmp/tagger-612/corpus-gold-612.txt` | le corpus 612 (612 blocs, sha256 `4f5231c6…`) |
| `/tmp/tagger-612/corpus-gold-5.txt` | le sous-corpus 5 items (sha256 `9bce3e13…`) |
| `/tmp/tagger-612/attendu-612.json` | le manifeste `id / source / langue / texte` des 612 |
| `/tmp/tagger-612/offline-612.jsonl` | la passe heuristique 612 (614 lignes, 0 réseau) |
| `/tmp/tagger-lot-fiab-cache/` | le cache X3 (676 fichiers) qui donne les tokens des 608 prompts |
| `data/deepseek/cache/` | le cache par défaut (3 759 fichiers, 604/608 prompts du batch) |

**Les fiches de référence** : [`rapport-tagger-lot.md`](rapport-tagger-lot.md) (X3, le lot de
1 000 items et le coût), [`rapport-tagger-defaut.md`](rapport-tagger-defaut.md) (W3, la matrice
du défaut et le code 4), [`rapport-tagger-option.md`](rapport-tagger-option.md) (1A, le gold
612 et le CLI), [`rapport-coordination-r.md`](rapport-coordination-r.md) (la commande 612
historique et le coût à deux appels), [`tagger-612.json`](tagger-612.json) (la mesure du 13/11).

## 11. Le go, en une checklist

- [ ] il est **11:30 ou plus** (le bloc le vérifie) ;
- [ ] `~/.config/drave/deepseek.key` est **lisible** et **0600** ;
- [ ] le corpus 612 fait **612 blocs** et le sha256 **`4f5231c6…`** ;
- [ ] le batch rend **code 0**, **614 lignes**, `réseau=608`, `tokens=87550` ;
- [ ] le JSONL est **614/614** valide, `refus` faible, POS neuronal majoritaire ;
- [ ] l'éval rend **code 0**, POS tagger **~0,95**, Δ **~+0,09** vs 0,8625 ;
- [ ] l'audit du cache donne **~87 841 tokens**, **~0,01875 $ remisé** ;
- [ ] aucun fichier publié ne contient la clé ;
- [ ] les résultats sont copiés dans `reports/` et la fiche R0.7 porte le chiffre du jour.

**Verdict.** Le lot est **prêt** : le gold est exact, la commande est copiable, le dry-run est
passé sans socket, le coût est mesuré par les prompts, et le seul risque non simulable — le
quota — a son contrôle (`tokens`, `refus`). **On peut lancer à 11:30.**
