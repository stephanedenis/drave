# A7.5b — le flux sparse gagne même à latence nulle

> **Objet.** A7.5 mesurait le volume et la latence loopback. Ici on modélise le temps total :
> `encodage + octets×8/débit + latence + décodage`, et on cherche le seuil où le sparse bat le
> dense. Le modèle est **explicite**, pas un `sleep`.

## Résultats (4×448, 356 non-nuls, 1 000 Mbit/s)

| mesure | dense | sparse |
|---|---:|---:|
| octets | **7 416** | **1 672** (4,44×) |
| encodage | 0,688 ms | **0,254 ms** |
| décodage | 0,490 ms | **0,369 ms** |
| temps à 0 ms | 1,238 ms | **0,637 ms** (1,94×) |
| temps à 5 ms | 6,238 ms | **5,637 ms** (1,11×) |
| temps à 20 ms | 21,238 ms | **20,637 ms** (1,03×) |
| temps à 100 ms | 101,238 ms | **100,637 ms** (1,006×) |

**Seuil calculé : −0,60 ms** — le sparse est **toujours** devant, même à latence nulle.

## Lecture

- Le sparse gagne **deux fois** : moins d'octets **et** un encodage/décodage plus rapide (il ne
  parcourt que les non-nuls).
- Le gain **relatif** s'effondre quand la latence monte : à 100 ms, il ne reste que **0,6 %**.
- Le **seuil** est négatif : aucune latence positive ne renverse la conclusion dans ce modèle.
- C'est **A3.3** appliqué au **transport de grappe** : la latence domine, mais le sparse ne perd
  jamais.

## Ce que ça ne dit pas

- **Pas de calcul distant** : on modélise le transport, pas l'exécution d'une couche.
- **Loopback** pour A7.5 ; ici un modèle de lien **1 000 Mbit/s**.
- Le **décodage dense** mesuré est plus lent que le sparse sur cette machine ; sur un autre CPU,
  le seuil pourrait devenir positif.
- Le flux synthétique a **19,9 %** de non-nuls ; à 100 %, le sparse serait plus cher.

## Verdict

**Le sparse gagne sur ce lien, à toutes les latences testées.** Le gain est **1,94×** à 0 ms et
**1,006×** à 100 ms : le **volume** et le **CPU** sont gagnants, la **latence** est le facteur
dominant.

## Fichiers

- Code : [`tools/seuil_reseau.py`](../tools/seuil_reseau.py).
- Test : [`tools/cerveau/tests/test_seuil_reseau.py`](../tools/cerveau/tests/test_seuil_reseau.py).
- JSON : [`seuil-reseau.json`](seuil-reseau.json).
