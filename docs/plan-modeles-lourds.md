# Plan — les modèles lourds : les télécharger, les analyser, découper leurs MoE

**En une ligne** : la bibliothèque brute vit sur le disque mécanique (4,7 To
libres), le NVMe ne sert plus qu'aux fichiers que NOUS produisons ; une file de
**1,14 To** de modèles lourds est en téléchargement, et le même protocole de mesure
que celui du sprint précédent (trace de routage → découpage en clusters) doit
passer sur eux pour décider du format.

## Pourquoi eux

Notre mode d'opération — listes d'événements, experts allumés un par un, mémoire
paginée, déport GPU partiel — ne se juge pas sur un modèle de 0,5B. Les décisions
de format (disposition des experts, manifeste multi-shards, index de routage) n'ont
de sens que sur les modèles qui ont **beaucoup d'experts** et **1 M de contexte**.
« Pouvoir rouler du best of breed » veut dire : ouvrir ces fichiers tels qu'ils sont
publiés, sans les requantifier.

## Ce qui est disponible (relevé sur Hugging Face, 01/10)

| modèle | pourquoi lui | plus petit GGUF | contexte | état |
|---|---|---|---|---|
| **DeepSeek-V4.1-Flash** | le plus lourd des ouverts, MoE, agentique | **365,7 Go** (Q2) | — | **en cours** (26 % à 09h36) |
| **DeepSeek-V4** | la version complète | 3 761 Go | 1 M | hors budget disque |
| **Kimi-K2.7-Code** | le meilleur agent de code ouvert | **303,9 Go** (UD-IQ1_M) | 262 k | en file |
| **GLM-5.3** | 1 M de contexte, MoE | **216,7 Go** (UD-IQ1_S) | 1 M | en file |
| **GLM-5.3-Flash** | le même en plus léger | **93,1 Go** (UD-IQ1_S) | 1 M | en file |
| **MiniMax-H3** | famille différente (vision+langage) | 22,8 Go (2 × Q4_K) | — | en file |
| **Qwen3-235B-A22B** | la référence MoE de 2025 | **85,7 Go** (Q2_K) | 262 k | en file |
| **DeepSeek-V4-Flash** | déjà téléchargé (86,9 Go) | — | 1 M | ✅ sur le disque mécanique |
| gpt-oss-120b, Qwen3-30B-A3B, Muse-Glimmer-30B | déjà là, servent de témoins | — | 128 k–262 k | ✅ |

**Budget** : 1,14 To de téléchargement pour ~4,4 To libres sur le disque
mécanique. Le NVMe ne reçoit **que** les artefacts produits : la politique complète
et les mesures qui la motivent sont dans `/home/stephane/FastNVMe/artefacts/README.md`
(mécanique ~210 Mo/s en écriture soutenue, NVMe 2,1 Go/s en lecture — notre mode
d'opération lit les poids en flux à chaque jeton, donc c'est le chemin chaud qui
doit être rapide).

## La mécanique de téléchargement (écrite, mesurée, reprenable)

`tools/telecharger_modeles.py` + `tools/manifeste_modeles_lourds.json` :

* **tranches `Range` de 256 Mo sur 6 connexions** : mesuré nécessaire — le pont Xet
  de Hugging Face refuse un GET plein sur le fichier de 365,7 Go (**HTTP 400**) et
  sert très bien les requêtes par tranches (**206**). Débit obtenu : 56–81 Mo/s
  contre 5–62 Mo/s en une seule connexion, et instable ;
* **reprise par tranche** : l'avancement de chaque tranche est noté dans un sidecar
  JSON, donc un arrêt (ou une coupure) ne coûte que la tranche en cours ;
* **garde-fou de disque** : la file s'arrête sous 300 Go libres ;
* **état** : `python3 tools/telecharger_modeles.py --etat`.

```bash
python3 tools/telecharger_modeles.py                 # toute la file
python3 tools/telecharger_modeles.py --seulement GLM-5.3-UD-IQ1_S
```

## Ce qu'on leur fera (le protocole, déjà rodé)

1. **Trace de routage** — `DRAVE_TRACE_EXPERTS=<fichier>`, une ligne par (couche,
   jeton) : les experts retenus. Ajouté au moteur pour Qwen3-30B-A3B (voir
   `reports/rapport-decoupage-moe.md`) et **indépendant du modèle**.
2. **Découpage en clusters** — `tools/clusters_moe.py` : couverture, ventilation,
   deux témoins (hasard, fréquence). Le premier résultat est un résultat NÉGATIF
   utile : sur Qwen3-30B-A3B, trier les experts par fréquence donne exactement la
   même partition que la co-activation (accord 1,000). À vérifier sur 256 experts
   et plus — c'est là que la co-activation pourrait enfin apporter quelque chose.
3. **Décision de format** à partir des mesures :
   * **manifeste multi-shards** (`MANIFEST.json`) : indispensable de toute façon,
     les modèles lourds sont livrés en 3 à 8 shards et le moteur n'ouvre qu'un
     fichier ;
   * **index MoE** (`*.moe.json`) : par couche, l'ordre des experts (fréquence ou
     clusters) et leurs plages dans les shards ;
   * **disposition contiguë par cluster** : un nœud ne lit que sa tranche, en
     séquentiel (NVMe→RAM→VRAM), au lieu de sauter dans tout le fichier.
4. **Le banc de bout en bout** : perplexité sur 512 jetons, comparable à
   llama.cpp, ou l'écart expliqué — c'est la définition de « capable de rouler du
   best of breed ».

## Les architectures à implémenter (l'état des lieux)

| modèle | architecture GGUF | ce que le moteur a | ce qui manque |
|---|---|---|---|
| DeepSeek-V4 / V4-Flash / V4.1-Flash | `deepseek4` (43 couches, 256 experts top-6, 1 M ctx) | lecture des métadonnées et du tokenizer ✅ (129 280 jetons, aller-retour identique) ; MoE 128/top-8 (gpt-oss, Qwen3) ; attention MLA validée sur modèle synthétique (5,2e-7) | le forward `deepseek4`, et le **lecteur multi-shards** |
| Kimi-K2.7 | `kimi_k25` | — | tout le forward |
| GLM-5.3 | à relever | — | tout le forward |
| Qwen3-235B-A22B | `qwen3moe` | MoE Qwen3 ✅ (128/top-8) | le passage de 128 à 256 experts, le contexte 262 k |
| MiniMax-H3 | vision+langage | vision Qwen2.5-VL ✅ | à relever |

Le premier chantier est donc **commun à tous** : lire un GGUF en plusieurs
fichiers. C'est de la plomberie, pas de la recherche, et ça débloque tout le reste
(y compris DeepSeek-V4-Flash, déjà sur le disque).

## Ordre de travail proposé

| # | étape | critère de succès |
|---|---|---|
| 1 | **lecteur multi-shards** | les 3 shards de DeepSeek-V4-Flash ouverts ensemble, un tenseur du shard 2 résolu avec les métadonnées du shard 1 |
| 2 | **tokenizer + gabarit** de DeepSeek-V4.1 | aller-retour identique sur Wikitext-2, un tour de conversation bien formé (jetons `｜User｜`/`｜Assistant｜`/`｜DSML｜`) |
| 3 | **forward deepseek4** (attention latente + MoE 256/top-6) | perplexité sur 512 jetons comparable à llama.cpp, ou l'écart expliqué |
| 4 | **trace + découpage** sur les trois gros MoE | la question « fréquence ou co-activation ? » tranchée à 256 experts et plus |
| 5 | **format** : manifeste + index + disposition contiguë | ✅ **écrit et mesuré sur Qwen3-30B-A3B** : `commun.gguf` + 8 `cluster-XX.gguf`, un nœud charge **3,20 Go au lieu de 18,56** et 625 ms au lieu de 3,9 s, 1 587 tenseurs vérifiés par empreinte — [`docs/format-clusters.md`](format-clusters.md) |
| 6 | **lecteur multi-fichiers** (le même que pour les shards) | le moteur ouvre `commun.gguf` + un cluster et tourne |

## Reprendre le téléchargement

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
python3 tools/telecharger_modeles.py --etat
tail -5 /tmp/telechargement_lourds.log
```

## État au 01/10 à midi — l'inventaire est fait, et il recoupe

`tools/inventaire_modeles_lourds.sh` lit les **en-têtes seuls** (le plus gros
fichier fait 366 Go) et confronte les poids annoncés par les descripteurs GGUF
aux tailles annoncées par HuggingFace :

| modèle | architecture | fichiers | tenseurs | poids lus | annoncé HF |
|---|---|---|---|---|---|
| DeepSeek-V4.1-Flash-Q2 | `deepseek41` | 1 | 1 046 | **365,70 Go** | 365,7 Go |
| GLM-5.3-UD-IQ1_S | `glm-dsa` | 6 | 1 809 | **216,71 Go** | 216,7 Go |
| Kimi-K2.7-Code-UD-IQ1_M | `deepseek2` | 8 | 1 096 | **303,90 Go** | 303,9 Go |
| DeepSeek-V4-Flash-UD-IQ1_M | `deepseek4` | 3 | 1 328 | **86,90 Go** | 86,9 Go (3 shards) |
| MiniMax-H3 | `?` | 1 | 532 | **11,42 Go** | 11,4 Go |
| Qwen3-235B-A22B-Q2_K | — | — | — | en cours | 85,7 Go |

**La concordance porte sur 984 Go** : c'est la vérification croisée la plus large
dont on dispose pour la table des types ggml. Une seule entrée fausse produirait
un écart visible sur des centaines de gigaoctets — le type `iq1_m` manquant, lui,
avait fait annoncer 8,56 Go pour 86,9.

Trois observations :

* **Les architectures lourdes sont lues** : `deepseek41`, `deepseek2`, `deepseek4`,
  `glm-dsa`. Aucune n'a de `forward` dans le moteur — c'est le chantier suivant.
* **MiniMax-H3 n'est pas un modèle de texte** (`audio_patch_proj`, `adaln_tbl`) :
  son architecture est inconnue, et c'est normal.
* **Le nombre de fichiers n'est pas un obstacle** : Kimi en a huit, GLM six, et le
  lecteur les rassemble à partir d'un seul chemin.

### Ce que le téléchargement a coûté

1 137,9 Go annoncés pour 24 fichiers ; à midi, tout est arrivé sauf
Qwen3-235B-A22B (85,7 Go) et GLM-5.3-Flash (93,1 Go). Débit soutenu ~75–110 Mo/s
sur le disque mécanique, qui sert aussi de bibliothèque brute — le NVMe ne porte
que nos artefacts.

