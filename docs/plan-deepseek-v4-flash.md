# Chantier — adapter les tests de contexte à DeepSeek-V4-Flash

> **État au 02/10 — écrit avant le téléchargement ; trois constats ont changé :**
> le **lecteur multi-shards est fait** (`Gguf::open_multi` :
> `reports/rapport-lecteur-multifichiers.md`) ; **V4.1-Flash a un GGUF Q2
> communautaire** (365,71 Go, mesuré — c'est lui la cible, V4-Flash reste le
> **banc** parce que llama.cpp le fait tourner) ; la **MLA à rang faible est
> faite** (validée à la position 0 — `reports/rapport-mla-experts.md`). Ce qui
> bloque encore V4-Flash, `--config` le nomme : **hyper-connexions** et **sortie
> à rang faible groupée**. La suite du chantier est dans
> `docs/plan-deepseek41-complet.md`.

**État au 01/10 09h40** : le modèle **est téléchargé** dans la bibliothèque du
disque mécanique (`/home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/`,
3 shards, 86,9 Go). Le NVMe, lui, a depuis accueilli la copie de travail de V4.1
(365,71 Go, `reports/rapport-execution-v41.md`). Le moteur **lit déjà ses métadonnées** : `--plan` affiche
« deepseek4, 43 couches, 256 experts (top-6) ». Mais il ne peut pas encore le
FAIRE TOURNER, pour deux raisons précises, et c'est ce document qui les cadre.

## Ce qui a été téléchargé, et pourquoi celui-là

| nom | nature | poids ouverts ? |
|---|---|---|
| **DeepSeek-V4.1-Flash** | modèle d'API ([api-docs](https://api-docs.deepseek.com/news/news260910/), [deepseek.com](https://www.deepseek.com/news/deepseek-v4-1-flash/)) | **oui** depuis le 02/10 — GGUF Q2 communautaire (365,71 Go), **incomplet** (`output_hc_fn/base/scale` absents alors que `hc_mult = 4` est déclaré) : `docs/plan-deepseek41-complet.md` §3.2 |
| **DeepSeek-V4-Flash** | poids ouverts (base de V4.1) : [unsloth/DeepSeek-V4-Flash-GGUF](https://huggingface.co/unsloth/DeepSeek-V4-Flash-GGUF), [huihui-ai](https://huggingface.co/huihui-ai/Huihui-DeepSeek-V4-Flash-0731-abliterated-GGUF) | oui |

C'est donc **DeepSeek-V4-Flash** (le seul des deux qui avait des poids ouverts à
cette date) qui a été récupéré, en quantification **UD-IQ1_M** : la plus petite publiée, 86,9 Go en trois
shards — les autres vont de ~120 Go (IQ2) à plusieurs centaines de Go, et le dépôt
complet pèse 1,67 To. Le choix est dicté par la place disque (586 Go libres) et par
le fait que le moteur lit le fichier EN PLACE : moins il y a d'octets, plus vite on
saura si l'architecture passe.

## Ce que le moteur sait déjà faire de ces fichiers (mesuré, 07h36)

| fichier | ce que le moteur en tire |
|---|---|
| shard 1 (5,3 Mo) | ✅ l'**architecture** (`--plan` : « deepseek4, 43 couches, 256 experts (top-6) ») et le **tokenizer** : 129 280 jetons, aller-retour texte→jetons→texte **identique** sur `data/wikitext2_test.txt` |
| shard 2 (49,97 Go) | ✅ **784 tenseurs** lisibles avec leurs noms, formes et quantifications (`Q4_K output.weight [129280, 4096]`, `F32 output_hc_base.weight [4]`…) — mais **sans métadonnées** : « 0 couches », architecture « ? » |
| shard 3 (36,92 Go) | ✅ téléchargé (mêmes propriétés que le shard 2) |

Autrement dit : le lecteur GGUF savait déjà tout lire, **séparément**, et il
manquait le lien entre les deux. **Ce lien est fait** : `Gguf::open_multi`
(`drave-core/src/gguf.rs`) ouvre les trois shards ensemble, résout les métadonnées
depuis le shard 1 et additionne les tailles — 1 328 tenseurs, 86,90 Go
(`reports/rapport-lecteur-multifichiers.md`).

## Les deux obstacles, mesurés

1. ~~**Le GGUF est découpé en shards.**~~ **Fait** (`Gguf::open_multi`,
   `reports/rapport-lecteur-multifichiers.md`) : le moteur ouvrait UN fichier
   (`Gguf::open(path)`) alors que le shard 1 ne contient **aucun tenseur** — il
   porte les métadonnées, les autres portent les poids. Le lecteur multi-fichiers
   ouvre les N shards, résout un nom de tenseur dans l'ensemble et additionne les
   tailles pour le placement.
2. **L'architecture `deepseek4` n'est pas implémentée.** Le moteur en lit la
   configuration (43 couches, 256 experts, top-6) mais il n'a **aucun code** pour son
   attention ni pour son routage : `model.rs` ne contient le mot « deepseek » qu'une
   fois, dans un commentaire. Ce qu'il faut couvrir, dans l'ordre :
   * l'**attention** : la MLA à rang faible **est faite** et validée contre
     llama.cpp (GLM-5.3, corrélation **0,999024** à la position 0 —
     `reports/rapport-mla-experts.md`) ; restent les **hyper-connexions**, la
     **sortie à rang faible groupée** et la dé-rotation/puits, que `--config`
     nomme ;
   * le **MoE 256 experts / top-6** (le moteur en gère 128/**top-4** sur gpt-oss
     et 128/top-8 sur Qwen3) ;
   * le **tokenizer** et le **gabarit de conversation** (jetons `｜User｜`,
     `｜Assistant｜`, `｜DSML｜` pour les outils — le moteur a son propre gabarit
     Qwen, il faut lire celui du GGUF) ;
   * le **contexte de 1 048 576 jetons** annoncé : c'est précisément ce que les
     tests de contexte doivent sonder, et c'est là que le KV paginé, le top-k
     déporté et le miroir VRAM de cette nuit deviennent intéressants.

## Le plan (le téléchargement est fini)

| # | étape | critère de succès |
|---|---|---|
| 1 | ~~lecteur GGUF multi-shards~~ **fait** | 3 shards ouverts, 1 328 tenseurs, 86,90 Go (`reports/rapport-lecteur-multifichiers.md`) |
| 2 | **tokenizer + gabarit** de V4-Flash | un aller-retour texte→jetons→texte identique sur `data/wikitext2_test.txt`, et un tour de conversation bien formé |
| 3 | **forward** : attention (MLA ou GQA selon le GGUF) puis MoE | perplexité sur 512 jetons comparable à llama.cpp, ou l'écart expliqué |
| 4 | **tests de contexte** (`tools/aiguille.py`) : 4 k / 8 k / 16 k / 32 k, profondeur 0,1 / 0,5 / 0,9 | le même protocole que cette nuit, mais sur un modèle à 1 M de contexte — et la question qui compte : **le taux de récupération tient-il quand k/contexte décroît ?** |
| 5 | croisement avec l'attention creuse (`--attn-topk`) | le k nécessaire croît-il plus lentement que le contexte, comme les deux points de cette nuit le suggèrent ? |
| 6 | **grappes + `--ppl-reparti`** (deux processus, voire deux machines) | mêmes listes, même perplexité qu'un nœud unique — `docs/plan-deepseek41-complet.md` P6 |

## Téléchargement terminé (86,9 Go, trois shards)

```bash
# La file complète (tous les modèles lourds) est dans le manifeste :
python3 tools/telecharger_modeles.py --seulement DeepSeek-V4-Flash-UD-IQ1_M
python3 tools/telecharger_modeles.py --etat        # où en est chaque fichier
```

Le téléchargement passe par **tranches `Range` de 256 Mo sur 6 connexions** : le
pont Xet de Hugging Face refuse un GET plein sur les très gros fichiers (HTTP 400
mesuré sur celui de 365,7 Go) mais sert très bien une requête par tranches (206).
Le journal est `/tmp/telechargement_lourds.log`.
