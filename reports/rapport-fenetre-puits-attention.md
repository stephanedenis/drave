# Fenêtre d'attention × puits : jusqu'où la fenêtre est-elle gratuite ?

> Campagne : **cerveau complet** · expérience : fenêtre × puits
> Question : existe-t-il un couple (fenêtre, nombre de puits d'attention) qui **approche
> l'attention complète** en ne notant qu'une **fraction** des clés ? Les scores d'attention sont
> le poste dominant : la fenêtre les rend `O(W)` au lieu de `O(N)` — mais elle coûte en qualité,
> et la question est de savoir si le **drain** (les `n` premiers jetons, toujours notés) paie ce
> coût.
> Verdict : **oui** — à 512 jetons, **fenêtre 128 + 64 puits** rend **13,3968** contre **13,1368**
> pour l'attention complète (**+2,0 %**) en ne notant que **192 clés sur 512** (**÷2,67**).
> Date réelle : **2026-10-10 10:18 HAE** (les journaux et commits de ce round ; `date` sur la
> machine, pas une horloge supposée).
> Protocole : `tools/carte-fenetre-puits.sh <limit>` — Qwen2.5-0.5B-Q8_0,
> `ids` = `/tmp/campagne24/ids_0.5B-Q8.txt`, `--ctx 512`, `--threads 8`, perplexité déterministe.

## 1. Pourquoi ce n'est pas une question de réglage, mais de mécanisme

`--attn-sinks N` **n'était pas un drapeau mort** (voir la fiche 50 de la campagne) : sous une
fenêtre, les `n` premiers jetons restent **notés** (`model.rs:7472`), et **zéro puits casse le
modèle** — 0 puits à fenêtre 32 : **1297,5437** contre **29,0206** à 4 puits (×45). Une attention
à fenêtre **sans drain** ne perd pas un peu de qualité : elle s'effondre. C'est ce qui rend la
question ci-dessus légitime — le drain est **porteur**, pas décoratif.

## 2. La carte, à 128 jetons (fenêtre 32 = un quart de la séquence)

| fenêtre \ puits | 0 | 8 | 16 | 24 | 32 |
|---|---|---|---|---|---|
| **16** | 23,8917 | 23,1946 | 20,7664 | 16,3487 | **16,2566** |
| **32** | 18,1141 | 16,9511 | 16,3812 | **15,4339** | 15,4499 |
| **64** | 16,1972 | 15,5128 | 15,3427 | 14,9614 | **14,8530** |

Référence **sans fenêtre : 14,6496**. Déjà visible : **un gros drain compense une petite
fenêtre** (16 de fenêtre + 32 puits = 16,2566 ≈ 64 de fenêtre + 0 puits = 16,1972).

## 3. La carte qui décide, à 512 jetons (le régime qui compte)

| fenêtre \ puits | 0 | 32 | 64 | clés notées / jeton | prix vs complet |
|---|---|---|---|---|---|
| **64** | 21,5801 | 16,2652 | 14,4247 | 128 | ÷4 |
| **128** | 17,2481 | 14,7484 | **13,3968** | 192 | **÷2,67** |
| **256** | 16,6749 | 14,6262 | 13,4778 | 320 | ÷1,6 |
| **aucune** | **13,1368** | — | — | 512 | — |

**Le résultat cherché est dans la case 128 × 64 : +2,0 % de perplexité pour ÷2,67 de clés
notées.** Et la fenêtre n'est pas seulement « moins chère » : avec le même drain de 64, la
fenêtre **128 bat la 256** (13,3968 contre 13,4778) — une non-monotonie de 0,6 % qu'il faut
**confirmer** (elle peut être du bruit de corpus sur 512 jetons ; elle est dans le bon sens).

## 4. Ce que ça ne dit pas (et qu'il faut mesurer)

- **une seule longueur** (512 jetons, un seul corpus, un seul modèle) : la pente en N n'est pas
  mesurée. La question ouverte est **à 2 048 et 4 096 jetons** : le couple (128, 64) tient-il,
  ou faut-il faire croître le drain avec la fenêtre ?
- **le prix réel n'est pas dans le compteur de paires affiché** : à cette échelle il arrondit à
  `0,01 M`. Le prix est **analytique** (`fenêtre + puits` clés notées par jeton par couche),
  et c'est celui du tableau ;
- **l'attention n'est pas tout le calcul** : le poste dominant mesuré ailleurs est la FFN
  (`proj+mlp` ≈ 26 ms/token contre 3,95 ms pour l'attention) — la fenêtre attaque le **second**
  poste, et c'est écrit ici pour ne pas laisser croire qu'elle divise le temps total ;
- **un modèle à fenêtre déclarée** (`swa_pattern` > 1, comme gpt-oss : une couche sur deux en
  attention complète) n'a pas été mesuré dans cette carte.

## 5. Protocole, pour rejouer

```bash
FENETRES="64 128 256" PUITS="0 32 64" tools/carte-fenetre-puits.sh 512
tools/carte-fenetre-puits.sh 128          # la carte complète par défaut
```

Le script imprime la référence sans fenêtre, puis une ligne par fenêtre — chaque case est une
perplexité mesurée par le moteur, aucun chiffre interpolé.
