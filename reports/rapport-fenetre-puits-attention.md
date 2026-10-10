# Fenêtre d'attention × puits : jusqu'où la fenêtre est-elle gratuite ?

> Campagne : **cerveau complet** · expérience : fenêtre × puits
> Question : existe-t-il un couple (fenêtre, nombre de puits d'attention) qui **approche
> l'attention complète** en ne notant qu'une **fraction** des clés ? Les scores d'attention sont
> le poste dominant : la fenêtre les rend `O(W)` au lieu de `O(N)` — mais elle coûte en qualité,
> et la question est de savoir si le **drain** (les `n` premiers jetons, toujours notés) paie ce
> coût.
> Verdict : **oui à courte portée, non à longue** — à 512 jetons, **fenêtre 128 + 64 puits** rend
> **13,3968** contre **13,1368** pour l'attention complète (**+2,0 %**) en ne notant que
> **192 clés sur 512** (**÷2,67**) ; mais à **2 048 jetons**, la meilleure case mesurée
> (**fenêtre 512 + 128 puits**, 640 clés sur 2 048, **÷3,2**) coûte **+40,3 %**
> (14,5531 contre 10,3703). **Le drain ne compense plus quand la séquence grandit** : la fenêtre
> est un levier de parcimonie à courte portée, un vrai trade-off de qualité à longue.
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

## 4. La pente en N : le drain ne compense plus quand la séquence grandit

Les deux cartes ci-dessus sont à 128 et 512 jetons. La troisième, à **2 048 jetons** (`--ctx 2048`,
mêmes ids, même modèle), répond à la question qui décide de l'usage réel :

| fenêtre \ puits | 0 | 64 | 128 | clés / jeton | prix vs complet |
|---|---|---|---|---|---|
| **128** | 20,6093 | 17,6891 | 16,4784 | 256 | ÷8 |
| **256** | 18,4229 | 16,4944 | 15,5281 | 384 | ÷5,3 |
| **512** | 15,4711 | 15,0810 | **14,5531** | 640 | **÷3,2** |
| **aucune** | **10,3703** | — | — | 2 048 | — |

**La synthèse, à taux de clés comparable :**

| N | attention complète | meilleure case | clés | prix |
|---|---|---|---|---|
| 128 | 14,6496 | 64 + 24 puits | 88 (**69 %**) | **+2,1 %** |
| 512 | 13,1368 | 128 + 64 puits | 192 (**37,5 %**) | **+2,0 %** |
| 2 048 | 10,3703 | 512 + 128 puits | 640 (**31 %**) | **+40,3 %** |

**Le fait, et il est net : à 31 % des clés notées, on paie +2,0 % à 512 jetons et +40,3 % à
2 048.** Ce n'est donc pas le *nombre* de clés qui décide, c'est **ce qu'on ne voit plus** : à
2 048 jetons, une fenêtre de 512 laisse 1 536 jetons accessibles seulement par les 128 puits, et
les puits ne portent pas l'information — ils drainent l'attention, ils ne la remplacent pas.

**Conséquence pour le sprint** : la fenêtre glissante n'est **pas** un gain gratuit sur les
scores d'attention (le poste dominant du calcul), et il ne faut pas la présenter comme tel. Elle
reste utile là où elle est utile : mémoire de travail à courte portée, et surtout **bornage du
coût par jeton** quand N grandit — mais alors le prix se paie en perplexité, et il est mesuré.

## 5. Ce que ça ne dit pas (et qu'il faut mesurer)

- **la pente en N est mesurée jusqu'à 2 048** (§ 4) : elle est **contre** la fenêtre au-delà de
  512 jetons. Reste à savoir si un drain **proportionnellement plus grand** (256, 512 puits à
  fenêtre 512) rachète le prix — c'est la mesure en cours ;
- **le prix réel n'est pas dans le compteur de paires affiché** : à cette échelle il arrondit à
  `0,01 M`. Le prix est **analytique** (`fenêtre + puits` clés notées par jeton par couche),
  et c'est celui du tableau ;
- **l'attention n'est pas tout le calcul** : le poste dominant mesuré ailleurs est la FFN
  (`proj+mlp` ≈ 26 ms/token contre 3,95 ms pour l'attention) — la fenêtre attaque le **second**
  poste, et c'est écrit ici pour ne pas laisser croire qu'elle divise le temps total ;
- **un modèle à fenêtre déclarée** (`swa_pattern` > 1, comme gpt-oss : une couche sur deux en
  attention complète) n'a pas été mesuré dans cette carte.

## 6. Protocole, pour rejouer

```bash
FENETRES="64 128 256" PUITS="0 32 64" tools/carte-fenetre-puits.sh 512
tools/carte-fenetre-puits.sh 128          # la carte complète par défaut
```

Le script imprime la référence sans fenêtre, puis une ligne par fenêtre — chaque case est une
perplexité mesurée par le moteur, aucun chiffre interpolé.
