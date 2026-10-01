# Rapport — pourquoi le déport des projections change (ou non) la perplexité

**En une ligne** : sur un modèle **dense**, le déport des projections donne des
logits **identiques** au CPU (écart moyen 0,0000, fichiers bit à bit égaux) ; sur un
**MoE**, il les décale de **0,038 nat** en moyenne — **497 jetons sur 511 gardent le
même top-1** (14 divergent), et cela suffit à déplacer la perplexité de 1,2 %. L'hypothèse la plus simple, fortement étayée par ce contraste, est que de
minuscules écarts numériques **changent le routage des experts** (top-8 sur 128).

## Le doute, et d'où il vient

Au sprint 2, gpt-oss-120b MXFP4 à `--ctx 1024`, 511 jetons :

| chemin | perplexité | écart vs CPU |
|---|---|---|
| CPU | 18,5803 | — |
| GPU, miroir KV seul (`DRAVE_GPU_KV`) | 18,3074 | −1,47 % |
| GPU, projections seules (`DRAVE_GPU`) | 18,3538 | −1,22 % |

Ajouter le miroir KV aux projections ne pèse que **0,25 % de plus** : l'essentiel
(1,22 %) vient du déport des **projections** lui-même. Or les noyaux GPU sont exacts
(2e-7 sur la tête Q8_0, **0,00e0** bit à bit sur un expert MXFP4 — `REPRISE.md` §6,
huit chantiers, noyaux GPU). Une erreur de 1e-7 ne devrait pas peser
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
| écart moyen \|ΔNLL\| | — | **0,0379** (médiane 0,0123, p90 0,0836, max 1,3708) — p90 imprimé par l'outil depuis ce sprint |
| accord du top-1 | — | **497/511** (14 positions divergentes) |
| corrélation des logits (position 0) | — | 1,000000 |

Le jeton choisi est le même sur 97 % des positions. Les 14 divergences portent un
écart de NLL **6× plus grand en moyenne** que les autres (0,198 contre 0,033), et le
maximum global (1,3708 nat, position 284) est l'une d'elles — mais seules 3 des 14
sont dans le top-14 des écarts : le lien est réel, pas exclusif. ⚠️ **Piège de
lecture payé** : `compare_logits.py` n'imprimait qu'un ÉCHANTILLON de positions
(`i < 24` ou `i % 32 == 0`), et « aucun NON dans l'échantillon » avait été lu comme
« accord partout » (511/511 annoncé, **497/511** mesuré). L'outil imprime
maintenant l'accord GLOBAL — un affichage partiel qui a l'air complet est un
affichage qui ment.

## L'hypothèse, et pourquoi elle est la bonne piste

Sur un modèle dense, la même comparaison donne **exactement zéro** : les noyaux GPU
sont donc bien exacts, et la différence sur gpt-oss ne vient pas d'eux. Ce qui
diffère entre les deux modèles, c'est le **routage** : gpt-oss choisit 8 experts sur
128 par couche, et un tri top-8 est une opération DISCRÈTE — un écart de 1e-7 sur
un logit de routeur peut faire basculer le 8e expert, et l'ensemble des experts
actifs change alors la sortie bien plus que 1e-7.

C'est cohérent avec l'écart de 0,06 % mesuré à `--ctx 256` (deux fenêtres de 255
jetons, un autre calcul) : 14 positions sur 511 changent de jeton, et ces quelques
basculements suffisent à déplacer une perplexité de 1 %. La perplexité GPU est
MEILLEURE (18,35 contre 18,58) — ce n'est pas une supériorité, c'est du bruit de
bascule sur un échantillon de 511 jetons.

**Statut : hypothèse étayée, pas démontrée.** La démonstration demanderait de
comparer les routages eux-mêmes (quels experts, quels poids) entre les deux
chemins — c'est un chantier à part entière, noté au planning.

## Ce que ça change pour l'usage

* les chemins GPU sont **exacts** sur un modèle dense (à la précision de la
  machine) : aucun doute sur les noyaux ;
* sur un MoE, `DRAVE_GPU` déplace la perplexité de l'ordre du pour cent au-delà de
  ~500 jetons évalués, en changeant le top-1 sur **3 % des positions** (14 sur 511) —
  acceptable pour un usage courant, mais à savoir avant de comparer deux perplexités
  mesurées avec et sans GPU ;
* les portes du dépôt (15,1757 CPU / 15,1667 GPU à ctx 256) restent valides : elles
  sont mesurées dans les mêmes conditions que leurs valeurs de référence.

## Reproduire

```bash
# logits des deux chemins, mêmes jetons
# (les mesures de ce rapport utilisent /tmp/ids_oss_512.txt, 512 identifiants)
./drave-core/target/release/drave <modele> --ppl /tmp/ids_oss_512.txt --ctx 1024 --dense \
    --limit 512 --logits-bin /tmp/logits_cpu.bin
DRAVE_GPU=1 ./drave-core/target/release/drave <modele> --ppl /tmp/ids_oss_512.txt --ctx 1024 \
    --dense --limit 512 --logits-bin /tmp/logits_gpu.bin
python3 tools/compare_logits.py /tmp/logits_cpu.bin /tmp/logits_gpu.bin /tmp/ids_oss_512.txt
```
