# N2.h3 — Le verrou de longueur : les positions absolues, pas le contexte

> **Ligne de roadmap** : N2 / R1 · **Date** : 2026-11-01 · **Verdict** : à 128 octets le modèle
> vaut **3,0904** ; à 256, **14,11** — il **surapprend sa longueur**. En tirant les
> **positions au hasard** pendant l'entraînement, la PPL à 256 passe à **3,25** et celle à
> 512 à **5,93**, pour **3,2381** en domaine à 129.

## La question

N2 le répète depuis cinq mesures : 129 octets est le meilleur point, 130 est négatif, 256 est à
5,7. La leçon retenue était « allonger le contexte demande un autre schéma ». Mais le modèle
apprend des **positions absolues** (`nn.Embedding(2048)`) : entraîné à 128 octets, les positions
128–2047 ne sont **jamais** vues, et aucun décalage ne peut généraliser. L'hypothèse testée ici :
**le verrou est la position apprise, pas la longueur**.

## Le dispositif

Deux bras, même corpus propre, même professeur, même base, mêmes 20 000 pas, trois graines :

| bras | positions à l'entraînement |
|---|---|
| **A** | `0..127` — l'entraînement de N2 |
| **R** | `o..o+127`, avec **o ~ U(0, 384)** à chaque pas — les positions `0..511` sont toutes vues |

Le reste est identique (lot 16, lr 1e-4 puis 3e-5). L'évaluation balaie 129, 192, 256, 384 et
512 octets, fenêtres tirées **dans** les chunks de validation (jamais à cheval sur un collage).

## Ce qui est mesuré

| octets | 129 | 192 | 256 | 384 | 512 |
|---|---:|---:|---:|---:|---:|
| **A** (positions 0–127) | 3,13 | 8,56 | 14,11 | 23,90 | 32,41 |
| **R** (positions aléatoires) | 3,24 | 3,23 | 3,25 | 5,06 | 5,93 |

## Lecture

Le verrou **tombe jusqu'à 256 octets** : la PPL passe de **14,11** à **3,25** (÷ 4,3), et à 512 de **32,41** à **5,93** (÷ 5,5). Mais entre 256 et 512, R **remonte** (3,25 → 5,93) : au-delà de la fenêtre d'attention locale (256), le modèle ne voit plus le début de la séquence. Il y a donc **deux verrous** : la **position apprise** jusqu'à 256, la **fenêtre locale** au-delà. En domaine (129 octets), le coût est de **0,148** : la position randomisée n'est pas gratuite, mais elle achète la longueur.

## Le second verrou n'est pas le masque

À 512 octets, l'attention locale ne laisse voir que les 256 octets précédents. Le même modèle a
été évalué avec une fenêtre élargie **à l'inférence** :

| fenêtre | 256 octets | 512 octets |
|---|---:|---:|
| 256 (entraînement) | 3,26 | 6,13 |
| 512 | 3,26 | 6,37 |
| 1 024 | 3,26 | 6,37 |

Élargir le masque **ne récupère rien** — il dégrade même un peu. Le second verrou n'est donc
**pas** la fenêtre : c'est l'**entraînement** (le modèle n'a jamais vu plus de 128 octets de
contexte). Pour lire 1 000 octets, il faudra entraîner sur des contextes longs — les positions
aléatoires étant la condition pour que les positions suivent — et non élargir une fenêtre.

## Ce que ça change pour R1

Le verrou de longueur n'est pas un seul verrou, et aucun n'est l'architecture :

1. **jusqu'à 256 octets, c'est la position apprise** : quelques lignes de code (tirer l'offset des
   positions à chaque pas) suffisent à faire tomber la PPL de 256 octets de 14,11 à 3,25. Le
   curriculum n'est plus la seule voie ;
2. **au-delà, c'est la fenêtre d'attention locale (256)** : R remonte de 3,25 à 5,93 à 512. Ce
   n'est plus un problème d'exposition mais de **schéma** — exactement ce que R1 doit trancher.

La question de R1 (« 1 000 octets sans refaire les négatifs 130–256 ») se scinde donc en deux :
la position (résolue, trois graines) et la fenêtre (ouverte, et c'est un vrai choix
d'architecture).

## Ce qui pourrait le rendre faux

- **L'attention est locale (fenêtre 256)** : au-delà de 256 octets, le modèle ne peut pas regarder
  le début de la séquence ; le gain à 512 vient de la position, pas d'un contexte long.
- **Le tirage des positions n'est pas un curriculum** : les positions sont vues uniformément, pas
  dans l'ordre de difficulté.
- **Une seule architecture** (11,47 M, 6 blocs), une seule taille de tirage (384).
- **Le protocole de longueur** utilise 128 fenêtres par point (16 384 octets) ; l'écart entre deux
  tirages vaut ~0,03.

## Fichiers

- Code : [`tools/distiller_budget.py`](../tools/distiller_budget.py) (`--positions-aleatoires`) ·
  [`tools/native_model.py`](../tools/native_model.py) (`pos_debut`).
- Points de contrôle : `work/n2h/R-pos-g{1,2,3}.pt`, `A-propre-g{1,2,3}.pt`.
