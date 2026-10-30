# B10.2bis — la capacité : 31,77 M contre 9,29 M, le décodeur ne bouge pas

> **Ligne de roadmap** : B10.2bis (levier « capacité ») · **Date** : 2026-10-29 · **Verdict** :
> ❌ **négatif** — avec une base **3,4× plus grosse** (31,77 M contre 9,29 M), le chrF de
> traduction gagne **0,5 à 0,7 point** (11,8 / 11,6 / 11,7 contre 11,1 / 11,2 / 11,0), pas les
> **27 points** qui manquent pour atteindre le plancher de 38,5. La capacité n'est pas le levier.
>
> **Dispositif** : corpus UDHR (30 articles, 10 langues, 24/6 par article), base
> `/tmp/natif-600-512-8-align-s1` (**31,77 M**), 600 pas, lot 8, seq 128, graine 1, trois bras
> (projection, attention croisée, segments) ; cibles chrF fra, spa, deu, cmn ; GPU ; JSON
> [`b102bis-capacite.json`](b102bis-capacite.json).

## La question

B10.2bis a éliminé l'attention croisée (11,2 contre 11,1) et les pas (1800 pas sans effet) ;
le corpus JW n'a rien changé non plus. Reste la **capacité** : un modèle 3,4× plus grand
apprend-il à restituer ?

## Ce qui est mesuré — 31,77 M, trois bras, graine 1

| bras | chrF reconstruction | chrF traduction | plancher | rappel | sonde |
|---|---:|---:|---:|---:|---:|
| projection (n_sem=1) | **16.9** | **11.8** | 38.5 | 0.335 | 0.2 |
| attention croisée | **16.5** | **11.6** | 38.5 | 0.335 | 0.25 |
| segments | **17.7** | **11.7** | 38.5 | 0.333 | 0.133 |

**Comparaison avec la base 9,29 M** (3 graines) : traduction **11.13 / 11.2 / 11.0**
(plancher 38.5) ; ici **11.8 / 11.6 / 11.7**
(plancher 38.5). La capacité multipliée par 3,4 déplace le décodeur de **0,5 à 0,7 point** : le plancher
n'est ni l'attention, ni le corpus, ni les pas, ni la taille — c'est le **protocole de
décodage** (byte-level) qui reste à changer.

## Les contrôles

| contrôle | ce qu'il devait faire | ce qu'il a fait |
|---|---|---|
| **même protocole** | seule la base change | ✅ mêmes données, mêmes pas, même graine |
| **plancher** | rester au-dessus | ✅ 38.5 contre ~11 |
| **sonde de langue** | chuter si `z` perd la langue | ✅ 0.2 en fin d'entraînement |

## Ce qui pourrait le rendre faux

- **Une seule graine** par bras (temps GPU) : l'écart de 0,1–0,3 point entre bras est du bruit.
- **Deux modèles, pas une échelle** : 9,29 M et 31,77 M restent petits ; la conclusion vaut
  pour cette plage, pas pour 100 M.
- **Le protocole est inchangé** : si le décodage byte-level est le plafond, un modèle plus
  grand ne peut que le confirmer — c'est le résultat.
- **La base 31,77 M a été entraînée sur le même corpus** : elle n'apporte pas de données
  nouvelles, seulement de la capacité.

## Ce que ça décide

**B10.2bis est close** : quatre leviers testés (attention, pas, corpus, capacité), quatre
négatifs. Le prochain chantier n'est pas un réglage du décodeur, c'est son **objectif** —
un décodage non byte-level (BPE/words) ou une échelle N5 (gelée). C'est nommé, pas supposé.

## Reproduire

```bash
gpu-env/bin/python3 tools/semantique/entrainer.py --corpus udhr \
  --checkpoint /tmp/natif-600-512-8-align-s1 --articles 30 --pas 600 --eval-tous 100 \
  --lot 8 --seq 128 --graine 1 --n-sem 4 --attention-sem --sortie /tmp/cap-b-s1
```
