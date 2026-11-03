# N2 — La distillation native : le professeur long dans un élève à fenêtre courte

> **Ligne de roadmap** : N2 (la distillation) · **Date** : 2026-11-03 · **Verdict** : le premier
> distillateur **natif → natif** du dépôt (professeur `drave-n0` RoPE à fenêtre 1 024, élève
> 11,47 M à fenêtre 512, init identique, mêmes 33 Mo) **paie — et le optimum est à forte douceur**.
> À **α = 0,9**, l'élève gagne **0,136** à 128 octets (3,5090 contre 3,6452), **0,166** à 512 et
> **0,177** à 1 024 ; le gain **croît avec la longueur**, alors que le professeur n'a que 1 024
> octets de fenêtre et l'élève 512. À α = 0,5 le gain s'effondre et s'inverse à 1 024 (+0,019) :
> **mélanger dur et doux dilue le professeur**. Le professeur coûte **+25 % par pas** (259 contre
> 208 ms) : à temps égal il reste ~0,15 de gain net — la distillation native est le premier levier
> qui **ajoute** à la fenêtre au lieu de la remplacer.

## La question

La note de passage N2 → R1 disait : « former un professeur **long** d'abord, **distiller**
ensuite ». La nuit a produit ce professeur — `rope1024-20k`, 34,3 M, fenêtre 1 024, **2,6256** à
1 000 octets sur `val_fr`. La question de cette fiche : **les cibles douces d'un professeur qui
voit loin apprennent-elles quelque chose à un élève qui ne voit pas si loin, à budget égal ?**

## Le dispositif

- **Professeur** : `work/n2ac/rope1024-20k.pt` (34,3 M, RoPE, fenêtre 1 024), gelé.
- **Élève** : `drave-n0` RoPE **11,47 M** (`224/288`), fenêtre **512**, **init aléatoire** —
  exactement celle du bras « dur » de référence (`cap-1147m-512`, graine 1). L'ordre
  d'initialisation est vérifié : l'élève est construit **avant** le professeur (sinon le chargement
  du professeur consomme le RNG) et la perte du pas 1 reproduit **5,8480**, la valeur du bras dur.
- **Perte** : `(1−α)·CE + α·T²·KL(professeur_T ‖ élève_T)`, T = 2, plus les **têtes précoces**
  supervisées comme dans l'entraîneur (parité de l'entraînement).
- **Budget** : 8 000 pas × 8 × 512 = **33 Mo**, corpus `data/wiki_fr/propre` et son canal, mêmes
  fenêtres Van der Corput (même ordre de données) que le bras dur.
- **Bras** : α = 0 (dur, référence), α = 0,5, α = 0,9.

## Ce qui est mesuré

Validation française, canal fourni :

| élève 11,47 M, fenêtre 512 (33 Mo) | 128 | 512 | 1 024 |
|---|---:|---:|---:|
| **dur** (α = 0, référence) | 3,6452 | 3,4493 | **3,3628** |
| distillé α = 0,5 | 3,5861 | 3,4330 | 3,3819 |
| écart | −0,059 | −0,016 | +0,019 |
| **distillé α = 0,9** | **3,5090** | **3,2835** | **3,1863** |
| écart | **−0,136** | **−0,166** | **−0,177** |

## Lecture

1. **La douceur paie, et il en faut beaucoup.** α = 0,5 donne un gain faible et même négatif à
   1 024 ; α = 0,9 donne −0,14 à −0,18 **partout**. Mélanger à parts égales le dur et le doux
   revient à entraîner sur une cible que **personne** ne vise : le professeur est presque toujours
   meilleur que les octets réels (il est plus gros et voit 1 024), donc suivre sa distribution est
   la bonne cible, pas un compromis.
2. **Le gain croît avec la longueur** (−0,136 à 128, −0,177 à 1 024) alors que l'élève ne voit que
   512 octets : les cibles douces **transportent** une partie de ce que le professeur a appris au
   long, même si l'élève ne peut pas le reconstruire. C'est le premier mécanisme de la nuit qui
   améliore l'élève **au-delà de sa fenêtre**.
3. **Le coût est modeste : +25 % par pas** (259 contre 208 ms), et non ×2 comme le laissait croire
   le premier run (mesuré sous contention). À budget de temps constant, l'élève distillé voit
   ~26,5 Mo au lieu de 33 (≈ −0,02 de PPL sur la pente mesurée) : le gain net reste **~+0,15**.
4. **La distillation ne remplace pas la fenêtre, elle s'y ajoute** : l'élève distillé (3,19 à
   1 024 octets) reste loin du professeur (2,63) et du même élève **entraîné à 1 024** (2,87 à
   1 024 octets, fiche [`n2-porte-propre`](rapport-n2-porte-propre.md)). C'est un **complément** :
   il faut d'abord un professeur long, et la fenêtre d'entraînement reste le levier premier.

## Ce qui pourrait le rendre faux

- **Un seul couple professeur/élève, une graine, deux α** (0,5 et 0,9) : le sens de la tendance est
  net, l'optimum exact n'est pas cherché (ni α = 0,7, ni T ≠ 2).
- **Le professeur est 3× plus gros que l'élève** (34,3 M contre 11,47 M) : on ne teste pas la
  compression au-delà ; un professeur plus gros ou plus long dirait peut-être plus.
- **La parité d'entraînement** est vérifiée sur la perte du pas 1 (5,8480) et sur les mêmes
  fenêtres, mais le script de distillation n'applique pas le curriculum de longueur des campagnes
  N2 ; il est à recette fixe.
- **Le coût du professeur** est mesuré sur cette machine avec les deux modèles sur le même GPU ;
  il dépend du lot et de la séquence, pas seulement du modèle.
- **La distillation HuggingFace** (`tools/distiller_budget.py`) reste le chemin pour les
  professeurs non natifs ; ce script-ci est **nouveau** et ne double pas les chiffres de N2.r.

## Fichiers

- Outil : `work/n2ac/distiller_natif.py` (copié dans
  `journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/`).
- Modèles : `work/n2ac/kd-1147m-512-a0.5.pt`, `work/n2ac/kd-1147m-512-a0.9.pt` ; référence
  `work/n2ac/cap-1147m-512.pt` ; professeur `work/n2ac/rope1024-20k.pt`.
- Mesures : `reports/n2-distillation-native.json` ; fiches amont
  [`n2-r12-2048`](rapport-n2-r12-2048.md), [`n2-fenetre`](rapport-n2-fenetre.md),
  [`n2-distillation`](rapport-n2-distillation.md).
