# B10.2bis — le corpus : 139 unités parallèles, 12 langues, et le décodeur ne décolle pas

> **Ligne de roadmap** : B10.2bis (levier « corpus ») · **Date** : 2026-10-29 · **Verdict** :
> ❌ **négatif** — sur le corpus JW (139 unités, **12 langues**, 5 articles), les trois bras
> plafonnent à **7.6 / 6.33 / 8.0** de chrF de
> traduction (reconstruction 0.0 / 0.0 / 0.0), pour
> un plancher source→référence de **17.1**. Le corpus n'est pas le levier : il ne
> change ni le niveau ni l'ordre des bras.
>
> **Dispositif** : corpus **parallèle JW** (`data/jw/jw_2026.json` : 5 articles, 12 langues,
> **139 unités alignées** par `num`), découpage **par article** (101 train / 38 val), modèle
> natif **9,29 M**, 600 pas, lot 8, seq 128, **3 graines**, 3 bras ; cibles chrF **ind, swh,
> vie** (scripts latins, pour un plancher comparable) ; GPU (torch 2.11, cu130) ; JSON
> [`b102bis-corpus-jw.json`](b102bis-corpus-jw.json).

## La question

B10.2bis a montré que l'attention croisée ne franchit pas le plancher sur 30 articles UDHR.
Le levier suivant est le **corpus** : plus de texte et plus de scripts changent-ils le
décodeur ? Le corpus JW donne **4,6× plus d'unités** et 12 langues (dont 6 non latines).

## Ce qui est mesuré — 3 bras × 3 graines

| bras | graine | chrF traduction | rappel | sonde |
|---|---:|---:|---:|---:|
| 1 | 8.2 | 0.325 | 0.158 |
| 2 | 7.4 | 0.387 | 0.208 |
| 3 | 7.2 | 0.328 | 0.182 |
| **moyenne** | | **7.6** | | |

| bras | graine | chrF traduction | rappel | sonde |
|---|---:|---:|---:|---:|
| 1 | 6.8 | 0.244 | 0.103 |
| 2 | 7.4 | 0.198 | 0.147 |
| 3 | 4.8 | 0.276 | 0.156 |
| **moyenne** | | **6.33** | | |

| bras | graine | chrF traduction | rappel | sonde |
|---|---:|---:|---:|---:|
| 1 | 8.7 | 0.315 | 0.239 |
| 2 | 8.1 | 0.379 | 0.182 |
| 3 | 7.2 | 0.305 | 0.182 |
| **moyenne** | | **8.0** | | |

**Comparaison avec l'UDHR** (même modèle, même protocole) : traduction **11,1 / 11,2 / 11,0**
(plancher 38,5) sur 30 articles ; ici **7.6 / 6.33 / 8.0**
(plancher 17.1) sur 139 unités et 12 langues. Le corpus multiplié par 4,6 et les scripts
non latins **ne déplacent pas** le décodeur : ni le niveau, ni l'ordre des bras.

## La reconstruction — contrôle sur un bras

Les neuf runs principaux n'incluaient pas la langue source dans les cibles chrF (ind, swh,
vie) : la **reconstruction** n'y est donc pas mesurée. Un run de contrôle (bras projection,
graine 1, cibles **eng, ind, swh, vie**) la mesure :

| mesure | valeur |
|---|---:|
| chrF reconstruction (eng → eng) | **9,4** |
| chrF traduction (eng → ind/swh/vie) | **8,2** |
| plancher | **37,8** |

La reconstruction du **sens dans la langue source** est à **9,4** : le décodeur ne restitue
même pas la langue d'entrée. Ce n'est pas la traduction qui manque, c'est la **restitution**.

## Les contrôles

| contrôle | ce qu'il devait faire | ce qu'il a fait |
|---|---|---|
| **plancher** (eng → référence) | être au-dessus du décodeur | ✅ **17.1** contre ~10 |
| **sonde de langue** | chuter si `z` perd la langue | ✅ de 0,98 à **0.103** |
| **rappel mélangé** | rester au hasard | ✅ ~0.017 |
| **bras égalés** | mêmes données, même budget, même graine | ✅ seul le bras change |

## Ce qui pourrait le rendre faux

- **139 unités courtes** (paragraphes de ~70 octets) : le corpus est plus large mais les
  unités sont plus courtes que les articles UDHR — deux effets opposés.
- **Le plancher est bas** (eng → ind/swh/vie) : le chrF de référence dépend de la paire, et
  comparer les niveaux entre corpus n'a de sens qu'à travers le plancher.
- **Un seul modèle** (9,29 M) : un modèle plus grand peut exploiter ce corpus autrement —
  c'est le levier « capacité », testé séparément.
- **600 pas** : le protocole est le même que B10.2bis, mais le corpus est différent : plus de
  pas pourrait aider ici et pas là.

## Ce que ça décide

Le levier **corpus** est **testé et négatif**. Restent la **capacité** (base 31,77 M) et
l'**objectif** (décodage byte-level). La prochaine expérience est la capacité, à protocole
constant.

## Reproduire

```bash
gpu-env/bin/python3 tools/semantique/entrainer.py --corpus jw \
  --checkpoint /tmp/natif-224-6-align-s1 --pas 600 --eval-tous 100 --lot 8 --seq 128 \
  --eval-cibles ind,swh,vie --graine 1 --n-sem 4 --attention-sem --sortie /tmp/jw-b-s1
```
