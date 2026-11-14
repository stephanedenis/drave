# A — coordination : A6.2 est libre, A8.3b2 est nommée mais hors du graphe

> **Ligne de roadmap** : A (le moteur) · **Tâche** : J4.4 · **Date** : 2026-11-13, 22 h 45 HNE
> · **Branche** : `s/v7` · **HEAD** : `dc78f223`
>
> **Verdict** : **A6.2 n'est pas bloquée.** Le MoE local de 18 Go existe et tourne — la porte
> de l'échange d'experts est **tenue** au HEAD, et `--ppl` redonne **37,2013**. Le seul blocage
> est la **résidence mono-GPU 16 Go** (17,28 GiB > 16 GiB), avec une précision : le cache VRAM
> d'experts n'est câblé que pour **MXFP4**, pas pour le **Q4_K** du modèle local. **A8.3b2 est
> nommée** par A8.3b (« instrumenter `forward_lot` »), mais elle est **absente du backlog, de la
> roadmap et du graphe** ; elle est libre. **Aucun fichier de A modifié** (ni `drave-core/`, ni
> `data/`, ni `work/`) : deux fichiers neufs, celui-ci et son JSON.

**En trois lignes.** (1) Le MoE `qwen3-30b-a3b-Q4_K_M` (18 556 686 752 o, 17,28 GiB,
`sha256 6c997b8a…`) est présent, chargé en **9,82 s**, et rend **37,2013** de perplexité à
`--limit 32` ; la porte `porte-echange-experts` rend **54,5202** à `N=16`, avec **768** décisions
de routage, l'invariant exact et le routage étranger à **36 074,9497**. (2) A8.3b2 est **nommée**
dans `rapport-a83b-decision.md`, mais **aucune** fiche de backlog, **aucune** ligne de roadmap,
**aucune** arête du graphe ne la porte. (3) Les décisions à prendre sont : requalifier A6.2 dans
les docs, définir la métrique du « ÷10 », choisir l'environnement de mesure (offload maintenant,
cache Q4_K plus tard), puis nommer A8.3b2, réparer son harnais (`LOT=1` est refusé par la porte
actuelle) et décider « une référence ou deux » avant de toucher au défaut.

## Ce que cette fiche est, et n'est pas

- **Est** : une coordination en **lecture seule**, avec des **rejeux** ciblés au HEAD. Elle donne
  l'état exact des deux lignes, les commandes qui le vérifient et les décisions à prendre.
- **N'est pas** : un patch, un commit, ni une modification de `drave-core/`, `data/`, `work/`,
  `docs/pilotage/backlog/` ou `docs/pilotage/roadmap.md`. La session A reste seule à écrire dans
  son territoire ; la session principale met l'état et la roadmap à jour.
- **Public** : la session A (prochaines actions : A6.2, A8.3b2) et le superviseur du chantier J4.

## 1. A6.2 — le MoE existe, la résidence est le blocage

### 1.1 Le fichier et la machine

| propriété | valeur mesurée |
|---|---|
| fichier | `/home/stephane/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf` |
| taille | **18 556 686 752 o** = **18,56 Go** = **17,28 GiB** |
| sha256 | `6c997b8af17debdfb01d890214400ccbab00db6acc0ba8da5de1cc906c4774d0` |
| architecture | **48 couches**, **128 experts**, **8 utilisés** par jeton (Qwen3-30B-A3B) |
| machine | **2 × Quadro RTX 5000, 16 384 MiB chacune** (32 GiB au total, NVLink) ; **125 GiB de RAM** |
| résidence | **17,28 GiB > 16 GiB** : ne tient pas dans **une** GPU ; le moteur l'exécute en mmap/offload CPU |
| défaut de la porte | `tools/porte-echange-experts.sh` prend ce chemin (`MODELE` par défaut) |
| `--ppl` au HEAD | **37,2013** sur 31 jetons notés (ctx 512, limit 32, 8 threads), chargement **9,82 s**, listes **0,91 Go** |

**Le chemin réel n'est pas `modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf`.** Cette
adresse, citée par `rapport-etat-a.md` § 4, **n'existe pas** dans l'arbre ; le fichier est sous
`$HOME/IA/modeles/`. C'est une correction de documentation, pas une mesure.

### 1.2 Les rejeux (ce que cette fiche a réellement exécuté)

| commande | résultat | ce qu'elle prouve |
|---|---|---|
| `bash tools/porte-echange-experts.sh` (défaut : `N=16`, `CTX=512`) | **exit 0** ; référence **54,5202** ; trace **768 décisions** ; routage propre **54,5202** (identique) ; routage étranger **36 074,9497** (différent) | le MoE **tourne**, le routage est **capturé** et **imposé**, l'invariant est exact et le mécanisme n'est pas mort |
| `DRAVE_TAMPONS=1 drave … --ppl <ids> --ctx 512 --limit 32 --threads 8` | **37,2013** sur **31** jetons notés ; **9,82 s** de chargement ; **0,91 Go** de listes | la perplexité publiée par C9 est **reproduite** au HEAD |
| `python3 tools/verifie_backlog.py` | exit 0 ; frontière **(3) : A2.6, N2, N4** | le graphe est cohérent **avec ses fiches** — et il ne voit ni A6.2 comme libre, ni A8.3b2 |

**Attention aux deux chiffres de perplexité.** `37,2013` est mesuré à `--limit 32` ; la porte,
à `N=16`, rend `54,5202`. Ce n'est pas une contradiction : la perplexité dépend du nombre de
jetons notés et de la fenêtre. Toute fiche A6.2 doit **épingler son `N` et son `ctx`**.

### 1.3 Ce qui bloque vraiment — et ce qui ne bloque pas

- **Ce n'est pas l'absence de MoE.** Le fichier est là, il se charge, il calcule, la trace de
  routage fonctionne. La phrase « aucun MoE local ne tient dans 16 Go de VRAM » de la fiche
  `A6.2-moe-local.md` est **vraie au sens littéral** (17,28 GiB > 16 GiB) et **fausse comme
  motif de blocage** : le moteur n'a pas besoin que le modèle réside pour le mesurer.
- **Le blocage est la résidence mono-GPU.** Un modèle de 17,28 GiB ne tient pas dans une carte
  de 16 GiB ; il tourne en offload. C'est une **contrainte d'exploitation interactive**, pas une
  **absence de brique de mesure**.
- **Précision qui change la décision** : le cache VRAM d'experts (`DRAVE_GPU_EXPERTS`) n'est
  câblé que pour **MXFP4** (`model.rs:4956`, `CacheExperts::monter` appelle `charger_mxfp4` et
  compte 17 octets par bloc). Le **Q4_K** du Qwen3-30B n'entre pas dans ce cache, même avec
  32 Go de VRAM. Le noyau GPU Q4_K a pourtant été mesuré (0,171 ms/expert, 5,17 Go/s dans
  `rapport-vram-transfert.md`), mais il n'est **pas branché** dans la production. Donc :
  **« résidence mono-GPU » est le bon nom pour le plafond ; « cache Q4_K non câblé » est le
  nom du travail de code qui le lèverait.**
- **Le cache RAM n'est pas la solution** : `DRAVE_EXPERTS_RAM` est mesuré **perdant** (+4 % à
  4 Go, +21 % à 32 Go) — le noyau garde déjà les pages ; le cache ajoute un second exemplaire.
- **Le cache VRAM n'est pas la solution immédiate** : `rapport-cache-experts-vram.md` donne un
  plafond de **×1,09** (pour un cache qui capte 28,7 % des lectures), contre ×3,1 pour le dense.

### 1.4 Ce qui est déjà mesuré pour A6.2 (et ce qui manque)

| mesure | résultat | source |
|---|---|---|
| regroupement par expert, **lot 192** | **74 496 → 4 804** lectures d'experts, **÷15,51** ; borne à l'infini **÷12,1** | `rapport-prefill-par-experts.md` § 2 |
| regroupement, **lot 64** | **÷7,08** | idem |
| regroupement, **lot 8** | **÷2,27** | idem |
| temps de préremplissage, **lot 192** | **×1,58** (le calcul dense et l'ordonnancement deviennent le mur) | idem § 1 |
| découpage en **8 clusters** | ventilation **3,08** nœuds contre **5,32** au hasard (**÷1,73**) ; couverture **0,607** | `rapport-decoupage-moe.md` |
| cache LRU, **25 %** des experts (32/128) | **74,8 à 87 %** des lectures servies | `rapport-reutilisation-experts.md` § 2 |
| cache LRU, **50 %** (64/128) | **92 à 93 %** | idem |
| cache VRAM, plafond prédit | **×1,09** (28,7 % de succès), plafond absolu ×1,41 | `rapport-cache-experts-vram.md` |
| cache RAM | **+4 %** à 4 Go, **+21 %** à 32 Go (plus lent) | `rapport-chargement-paresseux.md` / docstring `model.rs:1583` |

**Lecture, et c'est la décision D2.** Le contrat « coût de routage ÷10 » est **atteint en
octets lus** par le regroupement par expert **au lot 192** (÷15,51), mais **pas au lot 64**
(÷7,08) ; le point de passage entre 64 et 192 (128 par exemple) reste à mesurer. Il n'est **pas
atteint en temps** (×1,58 à 192) ni en **décodage interactif** (le cache LRU divise le trafic
par ~4, la VRAM ne donne que ×1,09). Il faut donc **nommer la métrique** avant de dire « A6.2
est faite » : « octets d'experts lus par jeton en préremplissage, lot 192 » est mesurable et
tenu ; « latence ÷10 » ne l'est pas.

**Ce qui manque encore, et c'est le cœur de A6.2 :**

- **le routage appris** n'est pas mesuré : le moteur utilise le routeur du modèle ; C9 est une
  expérience d'**échange** de routages, pas un routeur entraîné sur les logs ;
- **aucune** fiche `reports/rapport-a62-moe.md` (le livrable attendu par la fiche de backlog)
  n'existe ;
- **aucun** code d'entraînement de routeur **MoE** appris n'existe dans `tools/` (les outils de
  routage sont `clusters_moe.py`, `analyse_union_experts.py`, `analyse_reutilisation_experts.py`,
  `census_routage.py` — de la mesure, pas de l'apprentissage) ;
- **aucune** comparaison « qualité égale ±0,1 » entre un routeur appris et le routeur d'origine ;
- **aucune** définition écrite du « ÷10 » dans `A6.2-moe-local.md`.

### 1.5 Les commandes exactes pour la session A

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
M="$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf"
IDS="$HOME/IA/scratch/prerequis/ids_qwen3_30b_wt2.txt"

# 1. identité du fichier (ne pas se fier au chemin de rapport-etat-a.md)
stat -c '%n %s' "$M"
sha256sum "$M"

# 2. la porte de l'échange d'experts (référence 54,5202 à N=16)
MODELE="$M" N=16 CTX=512 bash tools/porte-echange-experts.sh

# 3. la perplexité C9 (37,2013 à limit 32)
DRAVE_TAMPONS=1 ./drave-core/target/release/drave "$M" \
  --ppl "$IDS" --ctx 512 --limit 32 --threads 8

# 4. capturer puis imposer le routage (invariant exact)
DRAVE_TRACE_EXPERTS=/tmp/rout.txt DRAVE_TRACE_EXPERTS_ORDRE=1 \
  ./drave-core/target/release/drave "$M" --ppl "$IDS" --ctx 512 --limit 32 --threads 8
DRAVE_ROUTAGE_FORCER=/tmp/rout.txt \
  ./drave-core/target/release/drave "$M" --ppl "$IDS" --ctx 512 --limit 32 --threads 8

# 5. le coût de routage : trace longue, puis comptage d'octets
DRAVE_TRACE_EXPERTS=/tmp/routage.txt ./drave-core/target/release/drave "$M" \
  --ppl /tmp/ids_qwen_long.txt --ctx 2048 --limit 2048 --lot 64 --threads 16
python3 tools/analyse_union_experts.py /tmp/routage.txt --experts-par-jeton 8
python3 tools/analyse_reutilisation_experts.py /tmp/routage.txt
python3 tools/clusters_moe.py /tmp/routage.txt --clusters 8 --json /tmp/clusters.json

# 6. le temps de préremplissage, par lot
bash tools/mesure-prefill-lot.sh "$M" /tmp/ids_qwen_long.txt 1 2 4 8 16 32 64 192

# 7. la frontière du graphe
python3 tools/verifie_backlog.py
```

### 1.6 Les décisions à prendre pour A6.2

**D1 — requalifier A6.2 dans les docs (aucun code A).** Passer `A6.2-moe-local.md` de
`bloquée` à `libre` (P2 ou P3, à trancher), remplacer « aucun MoE local dans 16 Go » par
« MoE local 18 Go ; blocage = résidence mono-GPU 16 Go ; cache VRAM Q4_K non câblé ». Mettre
à jour `backlog/index.md`, `en-cours.md`, `chantiers.md`, `plan-travail.md`, `roadmap.md`
(l. 84, 152, 343, 355), `dependances.md` § 5 et `rapport-a26-bilan.md`/JSON. **Acceptation** :
`grep -R "aucun MoE local" docs/pilotage/backlog/A6.2-moe-local.md docs/pilotage/roadmap.md`
→ **0** ; `python3 tools/verifie_backlog.py` → exit 0 ; A6.2 hors de la liste des bloqués.
**Ce qui l'invaliderait** : si le fichier de 18 Go disparaît ou si la porte échoue, A6.2
redevient bloquée pour la mesure.

**D2 — définir la métrique du « ÷10 ».** Écrire dans la fiche A6.2 : métrique **M1** = octets
d'experts lus par jeton en préremplissage (cible **÷10**, mesurée à **lot 192**), métrique
**M2** = qualité égale, **|ΔPPL| ≤ 0,1** ; métrique **M3** = tok/s, **secondaire**, pas le
contrat. Les chiffres existants donnent M1 ÷15,51 à 192 mais ÷7,08 à 64, M3 ×1,58 à 192 :
**M1 est tenue à 192, pas à 64 ; M3 non**. **Acceptation** : la fiche `rapport-a62-moe.md`
publie M1, M2, M3 séparément, donne le lot où M1 passe ÷10 et ne dit jamais « ÷10 » sans sa
métrique. **Ce qui l'invaliderait** : un run qui ne reproduit pas le ÷7,08 à 64 ou le ÷15,51 à
192 sur la même trace.

**D3 — choisir l'environnement de mesure.** **Option A (recommandée)** : mesurer sur le MoE
Q4_K existant en **offload CPU** (mmap, 125 GiB de RAM), et **nommer** la borne de résidence.
**Option B** : câbler le **Q4_K** dans `CacheExperts` (le noyau GPU Q4_K est déjà mesuré à
0,171 ms/expert, 5,17 Go/s) ou utiliser un MoE **MXFP4** ; alors seulement on pourra dire
« résidence GPU ». **Option C** : une carte de 24–48 Go — hors budget immédiat. **Décision
recommandée** : A maintenant, B comme ligne de code séparée **seulement si** la mesure M1/M3
l'exige. **Contrôle** : la qualité du routage ne dépend pas du lieu d'exécution (le routeur est
CPU f32) ; vérifier que la PPL du gate est la même en offload et avec le cache.

**D4 — produire le résultat A6.2.** La session A écrit `reports/rapport-a62-moe.md` + JSON :
porte (invariant exact, routage étranger), M1/M2/M3, balayage de lots, contrôles négatifs
(routage aléatoire, routage dense, trace vide), verdict vs D2, et **borne nommée** si échec.
**Acceptation** : `test -f reports/rapport-a62-moe.md` ; `bash tools/porte-echange-experts.sh`
exit 0 ; JSON valide. **Ce qui l'invaliderait** : un résultat qui ne mesure que C9 (échange de
routages) et pas un routeur **appris**.

## 2. A8.3b2 — nommée, libre, mais hors du graphe

### 2.1 Où elle est nommée, où elle ne l'est pas

| document | A8.3b2 ? | ce qu'il dit |
|---|---|---|
| `reports/rapport-a83b-decision.md:52` | **oui** | « Prochain : A8.3b2 (instrumentation `forward_lot`) ou B11.10. » |
| `reports/a83b-decision.json:42` | **oui** | `"A8.3b2 instrumentation forward_lot"` |
| `reports/rapport-etat-a.md` § 3 et action 3 | **oui** | « à faire — libre », « nommé par la fiche A8.3b, absent du graphe » |
| `docs/pilotage/semaine-autonome.md:37` | **oui (plan)** | « A6.2 routage, A8.3b2 » dans la ligne de coordination A |
| `docs/pilotage/backlog/index.md` | **non** | aucune ligne A8.3b2 |
| `docs/pilotage/backlog/dependances.md` | **non** | aucune arête, aucun plafond |
| `docs/pilotage/roadmap.md` | **non** | A8.3b/c/d expliqués, A8.3b2 absent |
| `docs/pilotage/en-cours.md` | **non** | aucune mention |
| `docs/pilotage/backlog/A8.3-defaut.md` | **non** | « prochain : réduire la non-équivalence du lot », sans nommer A8.3b2 |

**Conclusion** : A8.3b2 est **nommée par une fiche de résultat et par le plan de semaine**,
pas par le **graphe**. Le graphe ne peut donc pas la proposer comme frontière — c'est le défaut
que `rapport-etat-a.md` avait déjà relevé. Elle est **libre** : aucune ressource externe,
seulement du code et une mesure.

### 2.2 Les chiffres qui la définissent

| régime | lot 1 | lot ≥ 2 | effet du lot |
|---|---:|---:|---:|
| **f32** | **61,9920** | **60,8135** | **−1,90 %** |
| **mélange 1 %** | **58,3200** | **62,7357** | **+7,57 %** |
| threads 1 | 61,9920 | 60,8135 | −1,90 % |
| threads 8 | 61,9920 | 60,8135 | −1,90 % |

- **A8.3c** : le lot déplace la PPL de **1,90 %** à lui seul (f32) ; l'effet du KV est
  **cohérent par chemin** : **−5,9 %** sur le chemin jeton, **+3,2 %** sur le chemin lot.
- **A8.3d** : l'écart de 1,90 % est **le même à 1 et à 8 threads** — ce n'est pas le pool,
  c'est le **noyau par lots** (sommes réordonnées).
- **A8.0** : **18 portes** (a83b-decision) ou **19** (audit A8.0) PPL épinglées, **3** avec un
  régime 1 % dual (`porte-flux`, `porte-pont`, `porte-coupe`). Le compte 18/19 est lui-même
  à trancher (voir § 3).
- **A8.3b2** doit expliquer le **1,90 % f32** (lot 1 vs lot 4) puis le **+7,57 %** du régime
  1 %. Le second n'est pas une « non-monotonie » : le régime 1 % est une règle de **précision
  KV** (`DRAVE_PERTE_MAX` choisit la précision KV par couche, `model.rs:4711`), pas une
  quantification d'activation ; l'interaction avec le chemin lot reste à expliquer.

### 2.3 La commande `LOT=1 bash tools/porte-flux.sh` ne marche pas — et c'est normal

Rejeu au HEAD :

| commande | résultat |
|---|---|
| `LOT=4 bash tools/porte-flux.sh` | **exit 0** ; mode 3 **60,8135** ; mode 4 **60,5427** (deux nœuds) |
| `DRAVE_PERTE_MAX=1 LOT=4 bash tools/porte-flux.sh` | **exit 0** ; mode 3 **62,7357** ; mode 4 **64,9228** (deux nœuds) |
| `LOT=1 bash tools/porte-flux.sh` | **exit 1** ; modes 3/4 mesurent **61,9920** là où la porte attend **60,8135** |

**Ce n'est pas une régression** : les modes 3/4 de `porte-flux.sh` (l. 149–150) portent les
références du **chemin lot ≥ 2** (60,8135 / 62,7357). `LOT=1` redonne exactement le mode 0
(61,9920 / 58,3200), donc la porte **échoue par construction**. La commande
`LOT=1/4 bash tools/porte-flux.sh` citée par `rapport-etat-a.md` § 6 est donc **invalide pour
LOT=1** : elle ne peut pas servir d'A/B.

**Le bon harnais** est un A/B direct, avec **deux nœuds** et **deux références par chemin** :

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
M=models/Qwen2.5-0.5B-Q8_0.gguf
PORT=49322

# lot 1 : référence 61,9920 / deux nœuds 61,9920
./drave-core/target/release/drave "$M" --flux-serveur $PORT --ctx 64 --threads 8 &
SRV=$!
# attendre « nœud moteur sur » dans le log du nœud
./drave-core/target/release/drave "$M" --ppl-reparti 127.0.0.1:$PORT \
  --couches-locales 12 --limit 24 --ctx 64 --threads 8 --flux --lot 1
kill $SRV 2>/dev/null; wait $SRV 2>/dev/null

# lot 4 : référence 60,8135 / deux nœuds 60,8135 (le nœud sert UNE connexion)
./drave-core/target/release/drave "$M" --flux-serveur $PORT --ctx 64 --threads 8 &
SRV=$!
# attendre « nœud moteur sur » dans le log du nœud
./drave-core/target/release/drave "$M" --ppl-reparti 127.0.0.1:$PORT \
  --couches-locales 12 --limit 24 --ctx 64 --threads 8 --flux --lot 4
kill $SRV 2>/dev/null; wait $SRV 2>/dev/null
```

Rejeu : **lot 1 = 61,9920 / 61,9920**, **lot 4 = 60,8135 / 60,8135** ; les deux références
coïncident avec le découpage, et la porte imprime **0,00e0** pour ses modes exacts. C'est la
base de l'instrumentation.

**Deux instruments existants ne sont pas branchés sur `--ppl-reparti`** : `--logits-bin` et
`--trace-flux` y sont **ignorés** (le pilote réparti ne les lit pas ; aucun avertissement).
Pour un premier passage **sans code**, on peut :
- soit utiliser `--ppl` **local** avec un fichier de 24 jetons et `--trace-flux`, puis
  `python3 tools/diff_flux.py trace_lot1 trace_lot4` (l'outil donne la première couche et le
  premier jeton qui divergent) ;
- soit brancher `--trace-flux`/`--logits-bin` dans `ppl_reparti` (petit patch A, à faire par la
  session A).

### 2.4 Les points d'instrumentation, au HEAD `dc78f223`

| point | fichier:ligne | rôle |
|---|---|---|
| `forward_lot` | `drave-core/src/model.rs:5967` | le chemin par lots (entrée) |
| `quantifier` (lot) | `model.rs:6085–6105` | quantification **dense i32** du lot, une échelle par jeton |
| quantification d'entrée | `model.rs:6110` | `hn` → `xi`, `sx` |
| `quant_scratch` (jeton) | `model.rs:5092` | quantification **creuse i8** du chemin jeton |
| `gemm_dense_i8` | `drave-core/src/engine.rs:708` | produit matrice-matrice du lot |
| `gemm_dense_q4` | `engine.rs:726` | produit Q4 du lot (MoE ; le gate 0,5 B ne l'utilise pas) |
| quantification après attention | `model.rs:6328` | `att` → `ai`, `sa` |
| quantification FFN | `model.rs:6352`, `6523` | `hn`/`gate` → `xi`/`gi` |
| règle 1 % | `model.rs:4711` | **précision KV par couche** (`kv_precision`) — pas l'activation |
| `--lot` | `drave-core/src/main.rs:1597` | option CLI |
| porte | `tools/porte-flux.sh:149–150` | pins des modes 3/4 |

**Protocole proposé (à écrire par la session A, pas par cette fiche) :**

1. **Reproduire** : `LOT=4 bash tools/porte-flux.sh` (exit 0) et l'A/B manuel § 2.3.
2. **Première divergence sans code** : `--ppl` local, `--trace-flux` lot 1/4, puis
   `tools/diff_flux.py` ; noter `(couche, jeton, écart relatif)`. Si la première divergence est
   à la couche 0, c'est la **quantification d'entrée** ; après q/k/v, le **GEMM** ; après
   l'attention, le **KV** ; après le FFN, le **FFN**.
3. **Isoler le KV** : rejouer avec `DRAVE_KV_BITS=32` (KV f32) contre `DRAVE_PERTE_MAX=1` (KV
   int8 sur les 12 premières couches). Si l'écart de **+7,57 %** (régime 1 %) disparaît en KV
   f32, le seuil int8 est l'amplificateur. Le **1,90 % f32**, lui, est déjà sans KV int8 : il
   relève de l'ordre de somme du noyau.
4. **Contrôles négatifs** : `THREADS=1` (déjà : même écart) ; inverser les deux références
   (la porte doit échouer) ; trace vide (la porte doit refuser) ; `LOT=2` (doit être identique
   à `LOT=4`, A8.3b).
5. **Cible** : soit un **écart relatif de PPL < 0,05 %** (la tolérance des pins est 5e-4
   relative) et une **seule** référence ; soit une **cause nommée** et **deux références par
   chemin**, ce que A8.3c pratique déjà. La cible « < 0,1 % » de `rapport-etat-a.md` est **plus
   lâche que les pins** : il faut choisir.

### 2.5 Les décisions à prendre pour A8.3b2

**D5 — nommer A8.3b2 dans le graphe.** Créer `docs/pilotage/backlog/A8.3b2-instrumentation-lot.md`
(ou une section dans `A8.3-defaut.md`) + une ligne dans `backlog/index.md` + une mention dans
`roadmap.md` (A8) ; statut **libre**, P2 (ou P3), dépend de **A8.3b** ; livrable
`reports/rapport-a83b2-lot.md` + JSON. **Acceptation** : `grep -R "A8.3b2" docs/pilotage/backlog
docs/pilotage/roadmap.md` → au moins 1 ; `python3 tools/verifie_backlog.py` → exit 0.
**Ce qui l'invaliderait** : une ligne sans porte ni contrôle négatif (ce serait un doublon de
A8.3b).

**D6 — réparer le harnais.** Ajouter à `porte-flux.sh` un **mode `LOT=1`** avec ses propres
références (61,9920 / 58,3200), ou un `tools/porte-lot.sh` qui fait l'A/B **lot 1 vs lot 4**
avec deux pins. **Ne pas** utiliser `LOT=1/4` dans la même invocation. **Acceptation** :
`LOT=1 bash tools/porte-flux.sh` → exit 0 avec 61,9920/58,3200 ; `LOT=4` → exit 0 avec
60,8135/62,7357 ; `DRAVE_PERTE_MAX=1` idem. **Contrôle négatif** : échanger les deux références
doit faire échouer la porte (sinon elle ne vérifie rien).

**D7 — trancher « une référence ou deux ».** Si la cause est **inhérente** (ordre de sommation
du noyau par lots), garder **deux références par chemin** et le documenter ; si la cause est
**évitable** (seuil KV int8, quantification d'activation), corriger et **unifier**. La cible
n'est donc pas forcément « < 0,1 % » : c'est **« cause nommée + référence assumée »**.
**Acceptation** : la fiche A8.3b2 donne la cause, le premier point de divergence et la décision ;
le JSON contient les deux références ou la référence unique. **Ce qui l'invaliderait** : une
correction qui déplace les 18 ou 19 pins sans les re-épingler.

**D8 — le défaut reste opt-in.** A8.3 ne passe pas par défaut tant que : (a) les **18 ou 19**
pins n'ont pas un régime 1 % **dual** (3 aujourd'hui : flux, pont, coupe) ; (b) A8.3b2 n'a pas
donné sa cause ; (c) la passe complète sous défaut n'a pas été rejouée sans régression.
**Acceptation** : `bash tools/toutes-les-portes.sh` sous défaut, et `references-non-regression.md`
à jour. **Ce qui l'invaliderait** : un défaut qui déplace une porte non nommée.

## 3. Les contradictions de documentation, à corriger par la session principale

### 3.1 A6.2 — « libre » et « bloquée » dans le même dépôt

| document | ce qu'il dit | ce qu'il devrait dire |
|---|---|---|
| `docs/pilotage/backlog/A6.2-moe-local.md` | statut **bloquée** ; « aucun MoE local ne tient dans 16 Go » | **libre** ; « MoE 18 Go ; blocage = résidence mono-GPU 16 Go ; cache Q4_K non câblé » |
| `docs/pilotage/backlog/index.md:86` | **bloquée** | **libre** |
| `docs/pilotage/backlog/dependances.md:68` | **libre** | ✅ (déjà juste) |
| `docs/pilotage/backlog/dependances.md:167` | A6.2 dans « bloqués par une ressource » | **retirer** |
| `docs/pilotage/backlog/dependances.md:208` | A6.2 **libre** | ✅ (déjà juste) |
| `docs/pilotage/roadmap.md:30` | A6.2 **libre** | ✅ (déjà juste) |
| `docs/pilotage/roadmap.md:84`, `:152`, `:343`, `:355` | A6.2 **bloqué** | **libre** |
| `docs/pilotage/en-cours.md:113` | A6.2 dans « bloqués » | **libre** |
| `docs/pilotage/chantiers.md:83`, `:202` | A6.2 **bloqué** | **libre** |
| `docs/pilotage/plan-travail.md:150` | A6.2 dans la file des bloqués | **libre** |
| `reports/rapport-a26-bilan.md` / `a26-bilan.json` | experts « bloqués par A6.2, pas de MoE local » | « experts mesurables sur le MoE local ; placement à faire » |

### 3.2 A8.3b2 — nommée mais pas dans le graphe

- `docs/pilotage/backlog/index.md` : **aucune** ligne.
- `docs/pilotage/backlog/dependances.md` : **aucune** arête.
- `docs/pilotage/roadmap.md` : **aucune** mention ; A8.3b/c/d seulement.
- `docs/pilotage/backlog/A8.3-defaut.md` : « prochain : réduire la non-équivalence », sans
  nommer A8.3b2.
- `docs/pilotage/en-cours.md` : **aucune** mention.

### 3.3 Deux corrections dans `rapport-etat-a.md`

- **Chemin du MoE** : `modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf` n'existe pas ;
  le fichier est `$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf`.
- **Commande A8.3b2** : `LOT=1/4 bash tools/porte-flux.sh` est invalide pour `LOT=1` (la porte
  échoue par construction, § 2.3). Utiliser l'A/B manuel ou un mode `LOT=1` dédié.

### 3.4 Le compte des pins A8

Trois comptes coexistent : **6** (roadmap A8), **18** (`a83b-decision.json`), **19** (audit
A8.0 et `rapport-etat-a.md`). Le compte à retenir est celui de l'audit A8.0, **19**, avec
**3** duales ; il faut corriger `a83b-decision.json` ou expliquer l'écart (une porte sans PPL
n'est pas un pin).

## 4. Les décisions, en une table

| # | décision | qui | acceptation | ce qui l'invaliderait |
|---|---|---|---|---|
| **D1** | A6.2 : `bloquée` → `libre` ; blocage = résidence mono-GPU | session principale (docs) + A (fiche) | `grep "aucun MoE local"` → 0 ; `verifie_backlog.py` exit 0 | fichier 18 Go absent, porte rouge |
| **D2** | métrique du ÷10 = **octets lus** en préremplissage, mesurée à **lot 192** (pas à 64) ; qualité ±0,1 ; tok/s secondaire | A | `rapport-a62-moe.md` publie M1/M2/M3 séparément | run qui ne reproduit pas ÷7,08 à 64 ou ÷15,51 à 192 |
| **D3** | mesurer en **offload CPU** maintenant ; cache **Q4_K** seulement si nécessaire | A | M1/M2/M3 sur le MoE local ; borne de résidence nommée | qualité qui dépend du lieu d'exécution |
| **D4** | écrire `reports/rapport-a62-moe.md` + JSON | A | `test -f` ; gate exit 0 ; JSON valide | résultat qui n'est que C9 (échange) |
| **D5** | nommer A8.3b2 dans backlog + roadmap + graphe | session principale + A | `grep A8.3b2 docs/pilotage` ≥ 1 ; `verifie_backlog.py` exit 0 | ligne sans porte |
| **D6** | réparer le harnais : `LOT=1` a ses références, ou A/B dédié | A | `LOT=1` exit 0 (61,9920) ; `LOT=4` exit 0 (60,8135) | références échangeables sans échec |
| **D7** | trancher **une référence** (écart < 5e-4) ou **deux par chemin** (cause nommée) | A | fiche A8.3b2 : cause + premier point de divergence + décision | correction qui déplace les pins sans re-épinglage |
| **D8** | A8.3 reste **opt-in** jusqu'à 18/19 (compte à trancher) dual + cause + passe complète | session principale + A | `toutes-les-portes.sh` sous défaut, rouges nommées | défaut qui déplace une porte non nommée |

## 5. Contrôles négatifs, et ce qui pourrait rendre cette fiche fausse

- **Ce qui est rejoué, pas lu** : la porte de l'échange d'experts (**exit 0**, 54,5202, 768
  décisions, invariant exact), le `--ppl` **37,2013**, `LOT=4` (**exit 0**, 60,8135/60,5427),
  `DRAVE_PERTE_MAX=1 LOT=4` (**exit 0**, 62,7357/64,9228), `LOT=1` (**exit 1**, 61,9920 contre
  60,8135), et l'A/B manuel lot 1/4 (61,9920 / 60,8135, découpage neutre).
- **Ce qui n'est pas rejoué** : la passe complète (`bash tools/toutes-les-portes.sh`, ~2 h) ;
  les runs A6.2 de routage **appris** (ils n'existent pas) ; l'instrumentation A8.3b2 (elle
  reste à écrire).
- **Le binaire** : `drave-core/target/release/drave` date du **2026-10-30 08:39** ; `model.rs`
  a son dernier commit au **2026-10-28**, `main.rs` au **2026-10-30 08:41**. Le binaire peut
  être antérieur de deux minutes au dernier commit de `main.rs` ; les rejeux sont cohérents
  avec les pins publiés, mais **une reconstruction avant de figer un nouveau chiffre** est
  recommandée.
- **Le MoE** : 18 Go sur disque, `sha256` donné ; nous ne l'avons **pas** copié ni modifié.
  La résidence mono-GPU est une **constatation de taille** (17,28 GiB > 16 GiB), pas une mesure
  de performance interactive.
- **La documentation bouge** : les contradictions du § 3 peuvent être corrigées par une autre
  session après cette fiche ; le JSON porte la date et le HEAD pour que la comparaison reste
  possible.
- **Ce qui invaliderait la conclusion A6.2** : si le MoE ne tournait **pas** sur cette machine.
  Ce n'est pas le cas : la porte et le `--ppl` sont des rejeux, pas des lectures.

## 6. Fichiers, commandes et limites

- **Fichiers neufs** : `reports/rapport-coordination-a.md` (ce rapport) et
  `reports/rapport-coordination-a.json` (la version machine). **Aucun existant modifié, aucun
  commit** ; les deux fichiers sont découvrables par leur nom, comme les coordinations N2/S/R.
- **Aucune modification de A** : `drave-core/`, `data/`, `work/` et `docs/pilotage/backlog/`
  sont intacts. Les rejeux n'écrivent pas dans A ; leurs sorties vont dans `/tmp`
  (`/tmp/porte-echange-a.log`, `/tmp/porte-flux-lot*.log`, `/tmp/tr*.drvf`, etc.).
- **Fichiers lus (non modifiés)** : `AGENTS.md` ; `docs/pilotage/roadmap.md`, `en-cours.md`,
  `chantiers.md`, `plan-travail.md`, `semaine-autonome.md` ; `docs/pilotage/backlog/index.md`,
  `dependances.md`, `A6.2-moe-local.md`, `A8.3-defaut.md` ; `reports/rapport-etat-a.md`,
  `pensee-etat-a.json`, `rapport-c9-echange-experts.md`, `rapport-prefill-par-experts.md`,
  `rapport-decoupage-moe.md`, `rapport-reutilisation-experts.md`,
  `rapport-cache-experts-vram.md`, `rapport-chargement-paresseux.md`,
  `rapport-vram-transfert.md`, `rapport-gpu-tandem-nvlink.md`, `rapport-a83b-lot.md`,
  `rapport-a83b-decision.md`, `rapport-a83c-lot.md`, `rapport-a83d-lot-threads.md`,
  `rapport-a26-bilan.md` ; `a83b-lot.json`, `a83b-decision.json`, `a26-bilan.json` ;
  `drave-core/src/model.rs`, `engine.rs`, `main.rs`, `list.rs`, `materiel.rs` ;
  `tools/porte-echange-experts.sh`, `porte-flux.sh`, `mesure-prefill-lot.sh`,
  `analyse_union_experts.py`, `analyse_reutilisation_experts.py`, `clusters_moe.py`,
  `diff_flux.py`, `verifie_backlog.py`.
- **Limite de méthode** : cette fiche **lit** les résultats A6.2 existants et **rejoue** les
  commandes de la porte et de la perplexité ; elle ne remplace ni la passe complète, ni le
  résultat A6.2 (à écrire), ni l'instrumentation A8.3b2 (à écrire).

## 7. Voir aussi

- [`rapport-etat-a.md`](rapport-etat-a.md) — l'état A du 06/11 (dont cette fiche corrige deux
  points : le chemin du MoE et la commande `LOT=1/4`).
- [`rapport-a83b-decision.md`](rapport-a83b-decision.md) · [`a83b-decision.json`](a83b-decision.json)
- [`rapport-a83b-lot.md`](rapport-a83b-lot.md) · [`rapport-a83c-lot.md`](rapport-a83c-lot.md) ·
  [`rapport-a83d-lot-threads.md`](rapport-a83d-lot-threads.md)
- [`rapport-c9-echange-experts.md`](rapport-c9-echange-experts.md) ·
  [`rapport-prefill-par-experts.md`](rapport-prefill-par-experts.md) ·
  [`rapport-decoupage-moe.md`](rapport-decoupage-moe.md) ·
  [`rapport-reutilisation-experts.md`](rapport-reutilisation-experts.md) ·
  [`rapport-cache-experts-vram.md`](rapport-cache-experts-vram.md) ·
  [`rapport-chargement-paresseux.md`](rapport-chargement-paresseux.md) ·
  [`rapport-vram-transfert.md`](rapport-vram-transfert.md)
- [`A6.2`](../docs/pilotage/backlog/A6.2-moe-local.md) ·
  [`A8.3`](../docs/pilotage/backlog/A8.3-defaut.md) ·
  [`roadmap`](../docs/pilotage/roadmap.md) ·
  [`dependances`](../docs/pilotage/backlog/dependances.md)
