# Le banc de génération du natif — le modèle a appris les mots, pas la phrase

> **Ligne de roadmap** : **N4** (l'usage du natif) · **Date** : 2026-11-16 · **Modèle mesuré** :
> `work/n2ac/mix1024-60k.pt` (**34,3 M** paramètres, RoPE, seq 1 024, PPL **2,40**, corpus
> `wiki_mix/propre`) · **Verdict** : ❌ **le natif n'est pas un générateur de texte** — il a
> appris le **vocabulaire** (87 % de mots réels), pas la **composition** (un trigramme répété
> **15 fois** en greedy, des pseudo-mots en échantillonnage).
>
> **Le chiffre, en une ligne.** Sur **20 prompts** fixes et **128 octets** par prompt, trois
> réglages : **greedy** 0,870 de mots valides mais une **répétition de 15** ; **top-40/0,8**
> 0,490 de mots valides et une diversité de 1,000 ; **top-20/0,5** 0,735 et 0,981. Le
> **contrôle aléatoire** (même architecture, poids au hasard) : **0,336** de mots valides et
> **1** de répétition — le banc discrimine le modèle du bruit.

## 1. Le dispositif

[`tools/banc_generation.py`](../tools/banc_generation.py) : 20 prompts français
(« La France est un pays », « Dans les années 1950 », « Il était une fois »…), trois réglages
(greedy ; top-40 + 0,8 ; top-20 + 0,5), 128 octets par génération. Mesures par réglage : les
**mots valides** (la fraction des mots générés présents dans les 50 000 formes les plus fréquentes
du corpus), la **diversité** (distinct-2), la **répétition** (le plus grand nombre d'occurrences
d'un trigramme), l'**écho** (la fraction des mots générés recopiés du prompt), le **débit**.

**Contrôle négatif** : `--aleatoire` (la même architecture, les poids au hasard, la graine 1234).

## 2. Les résultats

| réglage | mots valides | distinct-2 | répétition | écho | octets/s |
|---|---:|---:|---:|---:|---:|
| **greedy** | **0,870** | 0,726 | **15** | 0,01 | 36,4 |
| top-40 / 0,8 | 0,490 | 1,000 | 1 | 0,01 | 36,4 |
| top-20 / 0,5 | 0,735 | 0,981 | 1 | 0,01 | 36,6 |
| **aléatoire (contrôle)** | **0,336** | 1,000 | 1 | 0,00 | 41,7 |

**Lecture.** (1) Le modèle **connaît les mots** : 0,870 contre 0,336 au hasard (+0,53). (2) Il
**ne compose pas** : en greedy, il tombe dans une boucle (un trigramme 15 fois) ; en
échantillonnage, il invente des pseudo-mots (0,49–0,74). (3) Le **débit** est de ~36 octets/s
(byte-level, 34 M sur CPU).

## 3. Les échantillons (la preuve, pas l'impression)

```
greedy  : « La France est un pays don d d da d 20 n dese de 1 20 20 aba dele 1 la 1 20 20 201 1 »
top-20  : « La France est un pays 2010 sene don d ousi le e 20 ste 2019 de 20 1 se confolemenatéce »
greedy  : « Dans les années 1950 le por le de la da la le e e de de e ena 20 1 esa la en ena da da »
```

La **cohérence s'arrête au prompt + ~3 mots** ; ensuite viennent les **nombres du corpus** (20,
201, 2019, 2020 — les dates) et les **formes inventées**. C'est le « 12 octets puis dérive » de
l'archive, mesuré.

## 4. Ce que le banc ne dit pas

- **La validité lexicale n'est pas la grammaticalité** : « 20 » est dans le vocabulaire du corpus.
- **20 prompts** et **128 octets** : un échantillon, pas une distribution.
- **Le byte-level** pénalise le débit ; un BPE changerait les chiffres, pas le diagnostic.

## 5. Ce qu'il faudrait (le chemin, chiffré)

1. **Le tokenizer BPE** (4 000–8 000) : ~8× moins de pas pour un même texte, et la qualité par
   paramètre remonte. **Le levier le plus rentable.**
2. **L'échelle** : 34 M est petit ; le corpus (1 Go) nourrirait un 150–300 M — mais l'entraînement
   passe de 3,7 h à des jours, et le GPU est réservé.
3. **L'alignement** (SFT) : le N4.6 mémorisait (24/24 vus, 0/4 tenus) ; un vrai SFT demande des
   données d'instruction, pas le corpus brut.
4. **L'évaluation** : ce banc est le début ; il faut une mesure de **grammaticalité** (un
   analyseur, le nôtre !) sur les générations.

## 6. La conclusion honnête

Le natif est un **prototype de recherche** : il sait **modéliser** (PPL 2,40, les mots appris) mais
pas **produire**. Ce n'est pas un défaut de plomberie (l'entraînement, la génération, le service,
le DRVM existent) : c'est un défaut de **qualité**, et il se paie en semaines de calcul, pas en
jours. Le produit `drave` exploitable reste le **bloc linguistique** (183/183, 0 dépendance) ; le
natif est le **chantier suivant**, pas une livraison.
