# Où mettre les bits du cache KV : la courbe complète

**En une ligne** : à taille ÉGALE, mettre les bits sur les **clés** plutôt que sur
les valeurs change l'erreur d'un facteur **130 à 840** — et les clés en f16
donnent 39 % de la taille f32 pour **+0,018 %**.

## Le tableau

Qwen2.5-0.5B-Q8_0, 8 191 jetons notés, contexte 8 192. « Octets par élément » =
octets par position et par dimension de tête, pour la paire clé + valeur (échelle
par bloc de 32 comprise).

| clés | valeurs | octets/élément | % du f32 | perplexité | écart |
|---|---|---|---|---|---|
| f32 | f32 | 8 | 100 % | **14,2339** | référence |
| **f32** | **int8** | 5,125 | 64 % | **14,2372** | **+0,023 %** |
| **int8** | **f32** | 5,125 | 64 % | 14,6622 | **+3,01 %** |
| f32 | int4 | 4,625 | 58 % | 14,2994 | +0,46 % |
| int4 | f32 | 4,625 | 58 % | 69,0464 | **+385 %** |
| int8 | int8 | 2,25 | 28 % | 14,6667 | +3,04 % |
| **f16** | **int8** | **3,125** | **39 %** | **14,2365** | **+0,018 %** |
| int4 | int4 | 1,25 | 16 % | 66,0369 | **+364 %** |
| f16 | int4 | 2,625 | 33 % | 14,3209 | +0,61 % |

## Ce que la courbe dit

**La frontière, du plus petit au plus gros** (8 191 jetons, ctx 8 192) :

```
16 %  int4/int4 ................ +364 %
28 %  int8/int8 ................ +3,04 %
33 %  clés f16 · valeurs int4 .. +0,61 %
39 %  clés f16 · valeurs int8 .. +0,018 %   ← le meilleur point
58 %  clés f32 · valeurs int4 .. +0,46 %
64 %  clés f32 · valeurs int8 .. +0,023 %
100 %  f32/f32 ................. référence
```

Le point utile est à **39 %** : on divise la taille du cache par 2,5 pour deux
centièmes de pour cent. Descendre plus bas coûte cher d'un coup — 33 % pour
+0,61 %, puis 28 % pour +3,04 % — parce qu'on attaque alors la précision des
VALEURS, qui n'est pas le maillon faible, ou qu'on rogne les clés sous le f16.

1. **Les deux moitiés n'ont pas le même rôle.** Une clé entre dans le SCORE
   d'attention, donc dans le softmax : son erreur déplace le poids relatif de
   toute une position. Une valeur ne fait que pondérer la sortie : son erreur se
   moyenne. À taille égale (5,125 octets), clés f32 + valeurs int8 coûte
   **+0,023 %** et clés int8 + valeurs f32 coûte **+3,01 %** — un facteur 130.
2. **Le pire cas est spectaculaire** : à 4,625 octets, clés f32 + valeurs int4
   coûte +0,46 %, clés int4 + valeurs f32 coûte **+385 %** (perplexité 69 au lieu
   de 14,2). Même taille, même modèle, facteur **840**.
   Et le 4 bits des DEUX côtés (1,25 octet, 16 % du f32) coûte **+364 %** : c'est
   le même ordre que les clés seules en 4 bits, ce qui confirme que ce sont bien
   les clés qui décident.
3. **La bonne politique est donc asymétrique** : garder les clés précises et
   rogner les valeurs. `DRAVE_KV_K_F32=1` (clés f32, valeurs int8) donne 64 % de
   la taille f32 pour +0,023 % — utilisable aujourd'hui.
4. **Les clés en f16 sont le meilleur réglage mesuré** : 3,125 octets par élément
   (39 % du f32) pour **+0,018 %** — contre 5,125 octets (64 %) pour les clés f32
   avec les mêmes valeurs int8 (+0,023 %). Les deux sont à +0,02 %, et l'écart
   entre eux n'est PAS significatif (8 191 jetons) : ce qui compte, c'est que la
   même qualité s'obtient avec **40 % d'octets en moins**, parce que le f16 est une
   précision RELATIVE là où l'int8 à échelle par bloc est une erreur ABSOLUE.
   Autrement dit : `DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1` donne un cache à **39 % de la
   taille f32** pour +0,018 %, là où l'int8 complet (28 %) coûte +3,04 %.

5. **La perspective llama.cpp** : son cache q8_0 coûte +0,8 % à la même longueur.
   Nos VALEURS sont donc meilleures que les siennes ; c'est le quantificateur de
   CLÉS qui est le maillon faible, et c'est là qu'il faut travailler — pas en
   ajoutant des bits partout.

## La suite : clés en f16

`DRAVE_KV_K_F16=1` stocke les clés en demi-précision (2 octets par valeur, aucune
échelle) : la précision est RELATIVE (2⁻¹¹ par valeur) au lieu d'être une erreur
ABSOLUE de bloc/254 — ce qui écrase les petits canaux d'une clé. Mesuré à
8 192 jetons : **+0,018 %** pour 3,125 octets par élément (**39 %** du f32), et à
4 096 : +0,011 % — dans les deux cas le meilleur point de la courbe.

## La frontière tient-elle à un AUTRE contexte ?

Les mesures de référence sont à 8 192. Refaites à **4 096** (mêmes 4 095 jetons
notés, mêmes commandes avec `--ctx 4096`) :

| réglage | 4 096 (PPL) | écart | 8 192 (rappel) | écart |
|---|---|---|---|---|
| f32 · f32 (référence) | **12,2175** | — | 14,2339 | — |
| clés f16 · valeurs int8 | **12,2188** | **+0,011 %** | 14,2365 | +0,018 % |
| int8 · int8 | 12,4921 | **+2,25 %** | 14,6667 | +3,04 % |
| clés f32 · valeurs int8 | 12,2223 | +0,039 % | 14,2372 | +0,023 % |

**Le classement tient** : à 4 096 comme à 8 192, les clés en f16 avec des valeurs
int8 restent collées à la référence (un à deux centièmes de pour cent) pendant que
l'int8 des deux côtés coûte plus de deux pour cent. La conclusion « les bits
doivent aller aux clés, et le f16 est le bon compromis » n'est donc pas un
artefact d'une longueur de contexte.

Un détail qui se répète : **les clés en f16 font aussi bien, et ici mieux, que les
clés en f32** avec les mêmes valeurs int8 (+0,011 % contre +0,039 % à 4 096 ;
+0,018 % contre +0,023 % à 8 192) — pour **moitié moins d'octets**. On ne prétend
pas que le f16 soit plus fidèle (l'écart est du même ordre que le bruit d'une
mesure de perplexité) : on constate qu'il ne coûte rien, et qu'il divise la taille
du cache par deux.

Détail rassurant au passage : la référence à 4 096 (**12,2175**) est exactement
celle que le dépôt avait mesurée pour le banc du KV déporté — les deux chemins
redisent le même chiffre à un an d'intervalle.

## Reproductible

```bash
D=./drave-core/target/release/drave ; M=models/Qwen2.5-0.5B-Q8_0.gguf
G="--ppl /tmp/ids_qwen_long.txt --ctx 8192 --limit 8192 --dense --threads 16 --lot 512"
DRAVE_KV_BITS=8 DRAVE_KV_K_F32=1 $D $M $G    # clés f32 · valeurs int8
DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1 $D $M $G    # clés f16 · valeurs int8
DRAVE_KV_BITS=4 DRAVE_KV_K_F32=1 $D $M $G    # clés f32 · valeurs int4
```

Chaque exécution prend 25 à 28 minutes à contexte 8 192 (trois passes de
8 191 jetons, dont une en f32 de référence).
