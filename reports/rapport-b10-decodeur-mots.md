# B10 — le décodeur au niveau du mot : 32,5 de chrF (plancher 33,7), mais le `z` ne porte que 2,6 points

> **Ligne de roadmap** : B10 (levier « objectif de décodage ») · **Date** : 2026-10-30 ·
> **Verdict** : ✅ **l'objectif octet était un goulot réel** — le même `z` gelé, décodé en
> **mots** au lieu d'octets, passe de **11,1** à **32,5** de chrF, à **96 %** du plancher
> (33,67). ❌ **mais le contrôle dit la limite** : avec le `z` d'un **autre** article, le chrF
> ne tombe qu'à **29,9** — le décodeur est surtout un **modèle de langue** ; la restitution
> *depuis `z`* reste faible.
>
> **Dispositif** : encodeur **gelé** de B10.2bis (9,29 M, état `/tmp/b102bis-a-s1`), corpus
> UDHR (30 articles, 9 langues avec espaces, `cmn` exclu), découpage 24/6, décodeur de
> **mots** (embedding de mots + langue, 2 couches d'attention croisée sur `z`, softmax sur un
> vocabulaire appris sur l'**entraînement seul**), 3000 pas, **3 graines** ; cibles chrF
> spa/deu/ita/por/rus/swh (source fra) ; JSON [`b10-decodeur-mots.json`](b10-decodeur-mots.json) ;
> code [`decodeur_mots.py`](../tools/semantique/decodeur_mots.py).

## La question

B10.2bis a testé quatre leviers et quatre négatifs : attention croisée, durée, corpus (JW),
capacité (31,77 M). Le décodeur du protocole génère des **octets** (vocabulaire de 256) : la
question qui reste est l'**objectif**. Le même `z` décodé en **mots** fait-il mieux ?

## Ce qui est mesuré — 3 graines

| graine | chrF reconstruction | chrF traduction | plancher | z mélangé | langue mélangée |
|---:|---:|---:|---:|---:|---:|
| 1 | 34,3 | **33,3** | 33,7 | 30,8 | 11,5 |
| 2 | 32,1 | **31,4** | 33,7 | 29,4 | 12,2 |
| 3 | 32,0 | **32,7** | 33,7 | 29,5 | 11,7 |
| **moyenne** | **32,8** | **32,5** | **33,7** | **29,9** | **11,8** |

**Comparaison avec le décodeur octet** (même `z`, même corpus, même split) : traduction
**11,1** (29 % du plancher) ; reconstruction **17,4**. Le décodeur mot atteint **96 % du
plancher**. L'objectif octet était donc un **goulot réel** : le même sens, décodé en mots,
passe de 11 à 32,5.

## Les contrôles — et ils changent la lecture

- **`z` mélangé** (chaque article reçoit le `z` d'un autre article) : **29,9** au lieu de 32,5.
  Le `z` ne porte que **2,6 points** de chrF : le décodeur produit du texte de la bonne langue
  et du bon registre **sans lire l'article**. C'est un modèle de langue, pas encore un lecteur.
- **langue mélangée** (cible générée avec la langue d'une autre cible) : **11,8** — la langue,
  elle, est bien portée par le décodeur (elle est dans l'embedding de langue, pas dans `z`).
- **plancher** : 33,7 (fra → spa/deu/ita/por/rus/swh) ; le décodeur mot est à 1,2 point.

## Ce que ça décide

1. **L'objectif était bien un levier** : le décodeur octet n'était pas seulement faible, il
   était mal outillé. C'est le premier levier **positif** de B10.2bis (après quatre négatifs).
2. **La restitution depuis `z` reste le verrou** : 2,6 points de `z` sur 32,5 de chrF, c'est
   ~8 %. **B10.3 (« raisonner sur `z` ») n'est donc pas débloqué** : on ne peut pas raisonner
   sur un sens que le décodeur lit à 8 %.
3. Le prochain test est **le même décodeur mot sur le corpus JW** (moins formulaire) et un
   **contrôle `z` plus dur** (même article, autre langue source ; autre article ; autre
   registre). Si le `z` porte plus sur un corpus non formulaire, le levier est le corpus +
   l'objectif ; sinon, c'est l'encodeur.

## Ce qui pourrait le rendre faux

- **Le corpus UDHR est formulaire** : 30 articles courts, structures répétitives — un modèle
  de langue y brille sans lire ; c'est exactement ce que le contrôle `z` révèle.
- **6 articles de validation** : le chrF moyen est bruité (±1 point entre graines).
- **Comparaison de systèmes, pas de calculs** : le décodeur mot a une autre architecture et
  une autre unité (mots) ; le gain mesure « byte contre mot », pas « même modèle, autre
  objectif ».
- **Le vocabulaire est appris sur l'entraînement seul** (pas de fuite), mais les mots inconnus
  de validation deviennent `<unk>` — le chrF de référence, lui, voit tous les mots.
- **`cmn` est exclu** (pas d'espaces) : la comparaison ne couvre pas les langues sans
  séparateur.

## Reproduire

```bash
gpu-env/bin/python3 tools/semantique/decodeur_mots.py --graine 1 --pas 3000 --sortie /tmp/mots-s1
gpu-env/bin/python3 tools/semantique/decodeur_mots.py --mesure reports/b10-decodeur-mots.json \
  --pas 3000 --graines 1,2,3
```
