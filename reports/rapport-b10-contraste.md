# B10 — le terme contrastif ne fait pas lire `z` : 32,6 de chrF (inchangé), écart `z` 1,5 (contre 2,6)

> **Ligne de roadmap** : B10 (conditionnement du décodeur) · **Date** : 2026-10-30 · **Verdict** :
> ❌ **négatif** — un terme contrastif qui pousse le `z` correct au-dessus du `z` d'une autre
> unité (marge 1,0, λ 0,5) **ne fait pas lire `z`** : le chrF reste à **32,6** (référence 32,5)
> et l'écart au contrôle `z` mélangé **diminue** (**1,45** contre 2,57). Le décodeur est même
> un peu plus **robuste** au mauvais `z`. Le verrou n'est pas dans la perte du décodeur.
>
> **Dispositif** : même protocole que [`rapport-b10-decodeur-mots.md`](rapport-b10-decodeur-mots.md)
> (UDHR, encodeur gelé, 3000 pas, 3 graines, décodeur de mots, vocabulaire appris sur
> l'entraînement) ; la seule différence est le terme
> `λ · relu(marge − (CE_z_mélangé − CE_z_correct))` ajouté à la perte ; JSON
> [`b10-mots-contraste.json`](b10-mots-contraste.json).

## La question

Le décodeur mot fait **32,5** de chrF (plancher 33,7) mais ne perd que **2,6 points** avec le
`z` d'un autre article : il écrit la langue, pas l'article. Peut-on le **forcer** à lire `z`
par la perte — un terme contrastif qui rend le mauvais `z` coûteux ?

## Ce qui est mesuré — 3 graines

| graine | chrF reconstruction | chrF traduction | `z` mélangé | langue mélangée | écart `z` |
|---:|---:|---:|---:|---:|---:|
| 1 | 28,4 | **32,8** | 31,8 | 12,2 | 1,0 |
| 2 | 35,6 | **33,1** | 30,9 | 11,6 | 2,2 |
| 3 | 30,9 | **31,9** | 30,7 | 11,7 | 1,2 |
| **moyenne** | **31,6** | **32,6** | **31,1** | **11,8** | **1,45** |

**Référence sans terme contrastif** : traduction **32,5**, `z` mélangé **29,9**, écart **2,57**.

Le terme contrastif **ne change rien au niveau** (32,6 contre 32,5) et **réduit l'écart au
contrôle** (1,45 contre 2,57) : le décodeur ne s'appuie pas **plus** sur `z` ; il apprend à
produire un texte un peu plus **générique**, qui résiste mieux au mauvais `z`.

## Pourquoi le terme échoue — l'hypothèse

La perte contrastive pousse la vraisemblance du texte **sous le mauvais `z`** vers le bas.
Mais le décodeur peut satisfaire cette contrainte **sans lire `z`** : il lui suffit de rendre
sa distribution un peu plus **uniforme** (ou plus générique) sous le mauvais `z` — ce qui
coûte peu, puisque le texte est déjà prédit par la **langue** et le **registre**. À
l'évaluation, la génération reste dominée par le prior de langue : le `z` n'est pas consulté.

**La conséquence** : tant que la tâche est « générer du texte de cette langue sur ce corpus »,
le prior suffit ; aucune perte sur la **surface** ne forcera le contenu. Il faut retirer le
prior — c'est-à-dire tester une **langue tenue à l'écart** (le décodeur n'a jamais vu ses
cibles ; seule la structure de `z` peut l'aider) ou une tâche où le prior ne peut pas gagner.

## Ce qui pourrait le rendre faux

- **Un seul jeu d'hyperparamètres** (λ 0,5, marge 1,0) : un λ plus grand ou une marge plus
  dure peut changer le résultat — mais le terme pousse déjà le mauvais `z` ; le problème est
  la **facilité** de la contrainte, pas son poids.
- **3 graines, 6 articles de validation** : ±1 point de bruit ; l'écart de 1,1 point entre
  les deux écarts `z` est dans le bruit — mais il ne va **pas** dans le sens attendu.
- **Le terme ne modifie pas `z`** : il ne peut pas créer de contenu ; il ne peut que changer
  la façon dont le décodeur le consulte.

## Ce que ça décide

Le levier « forcer le décodeur par la perte » est **testé et négatif**. Le suivant est la
**langue tenue à l'écart** (retirer le prior) ou une tâche de **contenu** (retrouver un fait
précis de l'article, pas le style). B10.3 reste bloqué tant que `z` n'est pas consulté.

## Reproduire

```bash
gpu-env/bin/python3 tools/semantique/decodeur_mots.py --mesure reports/b10-mots-contraste.json \
  --pas 3000 --graines 1,2,3 --contraste 0.5 --marge 1.0
```
