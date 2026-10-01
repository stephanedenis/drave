# Chantier — adapter les tests de contexte à DeepSeek-V4-Flash

**État au 01/10 07h10** : le modèle est **en cours de téléchargement**
(`/home/stephane/FastNVMe/models/DeepSeek-V4-Flash-UD-IQ1_M/`, 3 shards, 86,9 Go,
~25 Mo/s → ~1 h). Le moteur **lit déjà ses métadonnées** : `--plan` affiche
« deepseek4, 43 couches, 256 experts (top-6) ». Mais il ne peut pas encore le
FAIRE TOURNER, pour deux raisons précises, et c'est ce document qui les cadre.

## Ce qui a été téléchargé, et pourquoi celui-là

| nom | nature | poids ouverts ? |
|---|---|---|
| **DeepSeek-V4.1-Flash** | modèle d'API ([api-docs](https://api-docs.deepseek.com/news/news260910/), [deepseek.com](https://www.deepseek.com/news/deepseek-v4-1-flash/)) | **non** — aucun GGUF publié |
| **DeepSeek-V4-Flash** | poids ouverts (base de V4.1) : [unsloth/DeepSeek-V4-Flash-GGUF](https://huggingface.co/unsloth/DeepSeek-V4-Flash-GGUF), [huihui-ai](https://huggingface.co/huihui-ai/Huihui-DeepSeek-V4-Flash-0731-abliterated-GGUF) | oui |

C'est donc **DeepSeek-V4-Flash** (le seul des deux qui se télécharge) qui est
récupéré, en quantification **UD-IQ1_M** : la plus petite publiée, 86,9 Go en trois
shards — les autres vont de ~120 Go (IQ2) à plusieurs centaines de Go, et le dépôt
complet pèse 1,67 To. Le choix est dicté par la place disque (586 Go libres) et par
le fait que le moteur lit le fichier EN PLACE : moins il y a d'octets, plus vite on
saura si l'architecture passe.

## Les deux obstacles, mesurés

1. **Le GGUF est découpé en shards.** Le moteur ouvre UN fichier
   (`Gguf::open(path)`) ; le shard 1 ne contient **aucun tenseur** (« 0 tenseurs »)
   — il porte les métadonnées, les autres portent les poids. Il faut donc un
   **lecteur multi-fichiers** : ouvrir les N shards, résoudre un nom de tenseur dans
   l'ensemble, et additionner les tailles pour le placement. C'est le premier
   chantier, et il est indépendant de l'architecture.
2. **L'architecture `deepseek4` n'est pas implémentée.** Le moteur en lit la
   configuration (43 couches, 256 experts, top-6) mais il n'a **aucun code** pour son
   attention ni pour son routage : `model.rs` ne contient le mot « deepseek » qu'une
   fois, dans un commentaire. Ce qu'il faut couvrir, dans l'ordre :
   * l'**attention** (V4 utilise une attention latente de type MLA — le moteur en a
     une implémentation validée sur un modèle synthétique, `--banc-mla`, écart
     5,2e-7 : c'est la brique la plus proche du but) ;
   * le **MoE 256 experts / top-6** (le moteur en gère 128/top-8 sur gpt-oss et
     Qwen3) ;
   * le **tokenizer** et le **gabarit de conversation** (jetons `｜User｜`,
     `｜Assistant｜`, `｜DSML｜` pour les outils — le moteur a son propre gabarit
     Qwen, il faut lire celui du GGUF) ;
   * le **contexte de 1 048 576 jetons** annoncé : c'est précisément ce que les
     tests de contexte doivent sonder, et c'est là que le KV paginé, le top-k
     déporté et le miroir VRAM de cette nuit deviennent intéressants.

## Le plan, une fois le téléchargement fini

| # | étape | critère de succès |
|---|---|---|
| 1 | lecteur GGUF **multi-shards** | les 3 shards ouverts, un tenseur résolu depuis le shard 2, le placement total affiché |
| 2 | **tokenizer + gabarit** de V4-Flash | un aller-retour texte→jetons→texte identique sur `data/wikitext2_test.txt`, et un tour de conversation bien formé |
| 3 | **forward** : attention (MLA ou GQA selon le GGUF) puis MoE | perplexité sur 512 jetons comparable à llama.cpp, ou l'écart expliqué |
| 4 | **tests de contexte** (`tools/aiguille.py`) : 4 k / 8 k / 16 k / 32 k, profondeur 0,1 / 0,5 / 0,9 | le même protocole que cette nuit, mais sur un modèle à 1 M de contexte — et la question qui compte : **le taux de récupération tient-il quand k/contexte décroît ?** |
| 5 | croisement avec l'attention creuse (`--attn-topk`) | le k nécessaire croît-il plus lentement que le contexte, comme les deux points de cette nuit le suggèrent ? |

## Reprendre le téléchargement

```bash
cd /home/stephane/FastNVMe/models/DeepSeek-V4-Flash-UD-IQ1_M
B=https://huggingface.co/unsloth/DeepSeek-V4-Flash-GGUF/resolve/main/UD-IQ1_M
for f in DeepSeek-V4-Flash-UD-IQ1_M-0000{1,2,3}-of-00003.gguf; do wget -c "$B/$f"; done
```

`wget -c` reprend où il s'est arrêté : le journal est `/tmp/dl_v4flash.log`.
