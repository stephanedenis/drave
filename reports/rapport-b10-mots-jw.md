# B10 — le décodeur mot sur JW : 26,7 contre un plancher de 17,1 (+9,5), mais le `z` ne porte que 1,9 point

> **Ligne de roadmap** : B10 (levier « objectif », corpus non formulaire) · **Date** : 2026-10-30 ·
> **Verdict** : ✅ **le décodeur mot bat le plancher** sur le corpus JW — **26,65** de chrF contre
> **17,1** pour la copie source→référence (**+9,5**), là où le décodeur octet restait à **7,6**
> (44 % du plancher). ❌ **le contrôle `z` ne perd que 1,9 point** (24,8 avec le `z` d'un autre
> article) : sur un corpus **non formulaire** aussi, le décodeur est surtout un **modèle de
> langue** ; le verrou est l'encodeur.
>
> **Dispositif** : encodeur **JW gelé** (`/tmp/jw-a-s1`, entraîné sur les 5 articles/12 langues),
> corpus JW (139 unités, 5 articles, 11 langues avec espaces, `jpn` exclu), découpage par
> article (101 train / 38 val) ; décodeur de **mots** (embedding de mots + langue, 2 couches
> d'attention croisée sur `z`, vocabulaire appris sur l'entraînement), 3000 pas, **3 graines** ;
> cibles chrF **ind, swh, vie** (source `eng`) ; JSON
> [`b10-mots-jw.json`](b10-mots-jw.json) ; code
> [`decodeur_mots.py`](../tools/semantique/decodeur_mots.py) (`--corpus jw`).

## La question

Le décodeur mot a levé le décodeur sur l'UDHR (**32,5**, plancher 33,7) — mais l'UDHR est
formulaire et le contrôle `z` n'y perdait que 2,6 points. Sur un corpus **non formulaire**
(paragraphes de la Tour de garde, 12 langues), le `z` porte-t-il davantage ? Et le décodeur
mot bat-il le plancher ?

## Ce qui est mesuré — 3 graines

| graine | chrF reconstruction | chrF traduction | plancher (4 cibles) | `z` mélangé | langue mélangée |
|---:|---:|---:|---:|---:|---:|
| 1 | 25,0 | **26,5** | 37,8 | 25,1 | 13,1 |
| 2 | 22,1 | **27,4** | 37,8 | 25,3 | 13,3 |
| 3 | 24,8 | **26,0** | 37,8 | 23,9 | 12,9 |
| **moyenne** | **24,0** | **26,7** | **37,8** | **24,8** | **13,1** |

**Le plancher à lire.** Le plancher du protocole inclut la **source** (eng → eng = 100) :
37,8 est la moyenne à **4 cibles**. Le plancher des **3 cibles de traduction** est
(37,8 × 4 − 100) / 3 = **17,1** — exactement le chiffre du run octet. C'est à celui-là que se
compare la traduction.

**Comparaison avec le décodeur octet** (même encodeur, même corpus, même split) : traduction
**7,6** (44 % du plancher 17,1) ; reconstruction **9,4**. Le décodeur mot fait **26,7** :
il **bat le plancher de 9,5 points** et **multiplie le chrF octet par 3,5**.

## Les contrôles — la limite est dans `z`

- **`z` mélangé** (chaque unité reçoit le `z` d'une autre unité) : **24,8** au lieu de 26,7.
  Le `z` ne porte que **1,9 point** — **moins encore** que sur l'UDHR (2,6). Sur un texte
  non formulaire, le décodeur ne lit pas davantage : il produit la langue et le registre.
- **langue mélangée** : **13,1** — la langue est portée par l'embedding de langue (le
  décodeur n'a pas appris à l'ignorer).
- **reconstruction** : **24,0** pour eng → eng (la copie vaut 100) : le décodeur ne restitue
  pas la langue source, même avec le bon `z`.

## Ce que ça décide

1. **L'objectif mot est confirmé sur un corpus non formulaire** : il bat le plancher (+9,5) là
   où l'octet restait à 44 % du plancher. C'est le levier **positif** de B10.
2. **Le verrou est l'encodeur, pas le décodeur** : 1,9 à 2,6 points de `z` sur 26 à 32 de chrF
   (~7 %), sur **deux corpus**. Un décodeur qui sait écrire ne lit pas `z` pour autant.
3. **B10.3 reste bloqué** : raisonner sur `z` suppose que `z` porte le contenu ; ce n'est pas
   le cas. Le prochain chantier n'est pas le décodeur : c'est l'**objectif de l'encodeur**
   (reconstruction à travers `z`, contraste plus dur, ou une tâche qui force le contenu).

## Ce qui pourrait le rendre faux

- **Le plancher 17,1 est bas** : `eng → ind/swh/vie` ne sont pas cognates, la copie ne peut pas
  aider ; un plancher bas rend le « +9,5 » plus facile à battre qu'un plancher de cognates.
- **38 unités de validation** (paragraphes courts) : le chrF moyen est bruité (±1 point).
- **Le `z` JW vient d'un encodeur entraîné sur 101 unités** : il peut être sous-entraîné —
  c'est une limite de l'encodeur, pas une preuve que `z` ne peut pas porter.
- **Vocabulaire appris sur l'entraînement seul** : les mots inconnus de validation sont
  `<unk>` ; la référence, elle, voit tous les mots.
- **`jpn` exclu** (pas d'espaces) et **`hin` non testé ici** (il l'était dans le run octet).

## Reproduire

```bash
gpu-env/bin/python3 tools/semantique/decodeur_mots.py --corpus jw --graine 1 --pas 3000 \
  --sortie /tmp/mots-jw-s1
gpu-env/bin/python3 tools/semantique/decodeur_mots.py --corpus jw \
  --mesure reports/b10-mots-jw.json --pas 3000 --graines 1,2,3
```
