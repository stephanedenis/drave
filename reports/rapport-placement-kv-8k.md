# Le placement du KV à 8 k : ×1,93 sur le préremplissage, ×5,8 sur l'attention

> Mesure du 24/10/2026, Qwen2.5-0.5B Q8_0, contexte 8192, **5 337 jetons** de prompt, 8 jetons générés,
> 20 fils, binaire du dépôt. Deux exécutions, même prompt, même contexte : seul le **placement du cache KV** change
> (RAM par défaut, VRAM avec `DRAVE_GPU_KV=1`).

## La question

L'axe 2 de la vision tient en une règle : **on place un opérateur là où son flux coûte le moins cher**. Le cache KV
est le cas type : sa **lecture par jeton** croît linéairement avec le contexte (5 337 jetons × 24 couches × 2 têtes
KV × 64 dim × 4 octets ≈ **65,6 Mo par jeton**), et la bande passante de la RAM (~22,5 Go/s mesurés) contre celle
de la VRAM (~84,9 Go/s mesurés) décide du coût. À quel point la règle se voit-elle sur un contexte long ?

## La mesure

| | KV en RAM (défaut) | KV en VRAM | gain |
|---|---:|---:|---:|
| **préremplissage** (5 337 jetons) | 297,0 s (18,0 tok/s) | **153,7 s (34,7 tok/s)** | **×1,93** |
| **attention** (par jeton) | 32,3 ms | **5,6 ms** | **×5,8** |
| décodage (8 jetons) | 0,696 s (11,5 tok/s) | **0,278 s (28,7 tok/s)** | ×2,5 |
| total mesuré (par jeton) | 59,0 ms | **32,2 ms** | ×1,84 |
| TTFT | 55,7 ms | **28,8 ms** | ×1,93 |

Les deux exécutions donnent le **même** résultat (même prompt, même température 0 ; le KV est un miroir exact) : la
comparaison des temps est licite.

## Ce que ça dit

- **La règle est confirmée et mesurée** : le cache KV, dont la lecture par jeton dépasse le cache du processeur dès
  quelques milliers de jetons, va dans la **mémoire la plus rapide où il tient** — et cela vaut **×1,93** sur le
  préremplissage, **×5,8** sur l'attention.
- **Le gain n'est pas la bande passante seule** : le calcul CPU (le matvec, le MLP) domine à 23 ms/jeton et ne bouge
  pas ; c'est la part « attention » (32,3 → 5,6 ms) qui est **bornée par la mémoire**.
- **Le placement est donc un levier de premier ordre**, du même rang que la quantification : il ne change pas le
  résultat, seulement le temps.

## Le modèle de coût (la règle écrite)

Un opérateur `O` dont la lecture par jeton vaut `B` octets va sur le support qui **minimise** `B / bande + coût du
transfert` :

| support | bande mesurée | ce qu'on y met |
|---|---:|---|
| VRAM | **84,9 Go/s** | le KV au-delà de ~2-4 k jetons, l'attention, la tête |
| RAM | **22,5 Go/s** | les poids (mmap, non copiés), le KV des contextes courts |
| NVMe | **3,5 Go/s** | les poids qui ne tiennent pas en RAM (streaming) |
| réseau | 0,25 Mbit/s | les activations seules (jamais les poids) |

*C'est la table que l'ordonnanceur (A2.6) doit appliquer au lieu des `if` codés en dur — le chiffre du jour lui
donne sa première ligne validée.*

## Ce que ce résultat ne dit pas

- **Un seul modèle** (0,5 B) et **un seul prompt** ; le 3 B et le 14 B ont des poids et des têtes plus gros, et le
  seuil où le KV « tient » en VRAM est plus bas.
- 5 337 jetons, pas 8 192 : le prompt est en deçà du contexte, et le gain **croîtrait** encore avec la longueur.
- Le décodage ne porte que sur 8 jetons ; le préremplissage est le gros du temps et c'est lui qui fait foi.
- Le coût du transfert initial (le KV vers la VRAM) n'est pas isolé : il est noyé dans le préremplissage.
