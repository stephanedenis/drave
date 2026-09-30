# Phase 1.4 — l'écart du cache KV int8 est ENTIÈREMENT dû aux clés

**En une ligne** : à 8 192 jetons, les **valeurs** en int8 ne coûtent rien
(1 % de l'écart) et les **clés** coûtent tout (99 %) — l'expérience était écrite
dans la feuille de route, la voici faite.

## Les quatre mesures

Qwen2.5-0.5B-Q8_0, 8 191 jetons notés, contexte 8 192, `--dense --lot 512` :

| configuration | perplexité | écart au f32 | part de l'écart |
|---|---|---|---|
| cache f32 (référence) | **14,2339** | — | — |
| cache int8 complet | 14,6667 | +3,04 % | 100 % |
| **clés f32** · valeurs int8 | **14,2372** | **+0,023 %** | **99,2 % expliqué** |
| clés int8 · **valeurs f32** | 14,6622 | +3,01 % | 1,0 % seulement |

Reproductible :

```bash
DRAVE_KV_BITS=8 DRAVE_KV_K_F32=1 ./drave models/Qwen2.5-0.5B-Q8_0.gguf \
    --ppl /tmp/ids_qwen_long.txt --ctx 8192 --limit 8192 --dense --threads 16 --lot 512
```

## Ce que ça veut dire

Les deux moitiés du cache n'ont pas du tout le même rôle : une clé entre dans le
**score** d'attention, donc dans le softmax — une erreur de clé déplace le poids
relatif de toute une position. Une valeur ne fait que pondérer la sortie — son
erreur se moyenne. Le résultat est net : **les bits doivent aller aux clés**.

Conséquence immédiate, utilisable aujourd'hui : `DRAVE_KV_BITS=8
DRAVE_KV_K_F32=1` donne un cache à **75 % de la taille f32** pour +0,02 % de
perplexité — alors que l'int8 complet (50 % de la taille) coûte +3,0 %. C'est le
premier réglage KV qui soit à la fois plus petit ET gratuit en qualité.

Perspective : llama.cpp paie +0,8 % pour son cache int8 à la même longueur. Notre
quantificateur de **valeurs** est donc bon ; c'est celui des **clés** qui est le
maillon faible, et c'est là qu'il faut travailler — pas en ajoutant des bits
partout.

## Les deux expériences que ça ouvre

1. **clés f32 · valeurs int4** : 62,5 % de la taille f32 (1 + 0,25 sur 2). Si les
   valeurs tolèrent 4 bits aussi bien que 8, ce réglage bat l'int8 complet en
   taille *et* en qualité.
2. **un meilleur quantificateur de clés** : échelle par tête plutôt que par bloc
   de 32, ou rotation orthogonale avant quantification (le remède standard contre
   les valeurs aberrantes des clés). Le critère est simple : ramener l'écart des
   clés int8 sous celui de llama.cpp (+0,8 %).

Aucune des deux n'est faite ici : ce rapport établit l'attribution, il ne
l'exploite pas.
