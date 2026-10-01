# Rapport — pourquoi le déport des projections change (ou non) la perplexité

**En une ligne** : sur un modèle **dense**, le déport des projections donne des
logits **identiques** au CPU (écart moyen 0,0000) ; sur un **MoE**, il les décale de
**0,038 nat** en moyenne — même top-1 partout, mais 1,2 % de perplexité à 511
jetons. L'hypothèse la plus simple, fortement étayée par ce contraste, est que de
minuscules écarts numériques **changent le routage des experts** (top-8 sur 128).

## Le doute, et d'où il vient

Au sprint 2, gpt-oss-120b MXFP4 à `--ctx 1024`, 511 jetons :

| chemin | perplexité | écart vs CPU |
|---|---|---|
| CPU | 18,5803 | — |
| GPU, miroir KV seul (`DRAVE_GPU_KV`) | 18,3074 | −1,47 % |
| GPU, projections seules (`DRAVE_GPU`) | 18,3538 | −1,22 % |

Le miroir KV ne pèse donc que 0,25 % : l'essentiel vient du déport des
**projections**. Or les noyaux GPU sont exacts (2e-7 sur la tête Q8_0, **0,00e0**
sur un expert MXFP4, mesurés un par un). Une erreur de 1e-7 ne devrait pas peser
1,2 % de perplexité — d'où le doute consigné.

## La mesure qui tranche

`--logits-bin` exporte les logits des deux chemins sur **les mêmes jetons**, et
`tools/compare_logits.py` les compare position par position.

**Qwen2.5-0.5B Q8_0 (dense), ctx 256, 255 jetons :**

| | CPU | GPU (projections) |
|---|---|---|
| perplexité | 17,4315 | 17,4315 |
| écart moyen \|ΔNLL\| | — | **0,0000** (max 0,0000) |

**gpt-oss-120b MXFP4 (MoE, 128 experts, top-8), ctx 1024, 511 jetons :**

| | CPU | GPU (projections) |
|---|---|---|
| perplexité | 18,5803 | 18,3538 |
| écart moyen \|ΔNLL\| | — | **0,0379** (médiane 0,0123, max 1,3708) |
| accord du top-1 | — | **511/511 positions** |
| corrélation des logits (position 0) | — | 1,000000 |

Le top-1 est le même PARTOUT, mais les probabilités diffèrent : la perplexité,
qui est une moyenne de −log p(jeton cible), intègre ces écarts.

## L'hypothèse, et pourquoi elle est la bonne piste

Sur un modèle dense, la même comparaison donne **exactement zéro** : les noyaux GPU
sont donc bien exacts, et la différence sur gpt-oss ne vient pas d'eux. Ce qui
diffère entre les deux modèles, c'est le **routage** : gpt-oss choisit 8 experts sur
128 par couche, et un tri top-8 est une opération DISCRÈTE — un écart de 1e-7 sur
un logit de routeur peut faire basculer le 8e expert, et l'ensemble des experts
actifs change alors la sortie bien plus que 1e-7.

C'est cohérent avec l'écart de 0,06 % mesuré à `--ctx 256` (deux fenêtres de 255
jetons, un autre calcul) et avec l'accord parfait du top-1 : les jetons changent de
probabilité, pas d'identité.

**Statut : hypothèse étayée, pas démontrée.** La démonstration demanderait de
comparer les routages eux-mêmes (quels experts, quels poids) entre les deux
chemins — c'est un chantier à part entière, noté au planning.

## Ce que ça change pour l'usage

* les chemins GPU sont **exacts** sur un modèle dense (à la précision de la
  machine) : aucun doute sur les noyaux ;
* sur un MoE, `DRAVE_GPU` déplace la perplexité de l'ordre du pour cent au-delà de
  ~500 jetons évalués, **sans changer les jetons choisis** en top-1 — c'est
  acceptable pour un usage courant, mais à savoir avant de comparer deux
  perplexités mesurées avec et sans GPU ;
* les portes du dépôt (15,1757 CPU / 15,1667 GPU à ctx 256) restent valides : elles
  sont mesurées dans les mêmes conditions que leurs valeurs de référence.

## Reproduire

```bash
# logits des deux chemins, mêmes jetons
./drave-core/target/release/drave <modele> --ppl /tmp/ids.txt --ctx 1024 --dense \
    --limit 512 --logits-bin /tmp/logits_cpu.bin
DRAVE_GPU=1 ./drave-core/target/release/drave <modele> --ppl /tmp/ids.txt --ctx 1024 \
    --dense --limit 512 --logits-bin /tmp/logits_gpu.bin
python3 tools/compare_logits.py /tmp/logits_cpu.bin /tmp/logits_gpu.bin /tmp/ids.txt
```
