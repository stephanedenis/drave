# N2 — La distillation native : le professeur long dans un élève à fenêtre courte

> **Ligne de roadmap** : N2 (la distillation) · **Date** : 2026-11-03/04 · **Verdict — ERRATUM** :
> le gain annoncé le 03/11 (**0,14 à 0,18** à α = 0,9) était un **artefact de pondération**, pas de
> la distillation. Le code d'hier donnait à la tête principale le poids **1** au lieu de **1/4**
> (l'entraîneur de référence fait la **moyenne** des quatre têtes) : les runs « distillés » étaient
> donc aussi des runs **à tête principale surpondérée**. À **parité stricte** — même code, même
> harnais, même init, mêmes 33 Mo, seul α change — **α = 0,9 ne gagne rien** : 3,6774 / 3,5633 /
> 3,5208 contre **3,7072 / 3,5727 / 3,5251** pour α = 0, soit **−0,030 / −0,009 / −0,004**, dans le
> bruit. Le bruit de harnais lui-même est de **±0,06 à ±0,16** : c'est la leçon de la nuit.
>
> **Mais la distillation paie depuis une initialisation entraînée** : sur la **recette de
> production** (34,3 M, init `mix-60k`, mêmes 15 000 pas, mêmes 61,4 Mo), la paire propre donne
> **3,1119 / 2,8462 / 2,7388 / 2,6968** contre **3,1500 / 2,9069 / 2,8006 / 2,7618** — soit
> **−0,04 à −0,07** en domaine et **−0,19 / −0,34** hors domaine
> (fiche [`n2-production-fenetre`](rapport-n2-production-fenetre.md) § 4). Le résultat d'hier
> n'était donc pas *faux* : il était **gonflé** (2×) et attribué au mauvais mécanisme.

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

Le **contrôle de parité** d'abord : le code a été corrigé (`perte = moyenne(tête principale
distillée, têtes précoces)`, exactement la perte de `entrainer_rope.py`). Vérification : la perte
du **pas 1** vaut **5,8480** et celle du pas 50 **2,6713** — les valeurs du bras dur de référence
(5,8480 / 2,6714). La parité est exacte.

| élève 11,47 M, fenêtre 512, 33 Mo (même code, même harnais, même init) | 128 | 512 | 1 024 |
|---|---:|---:|---:|
| **α = 0** (contrôle : le professeur est évalué, pas imité) | **3,7072** | **3,5727** | **3,5251** |
| **α = 0,9** (distillation) | 3,6774 | 3,5633 | 3,5208 |
| **écart** | −0,030 | −0,009 | −0,004 |
| pour mémoire : bras dur de l'entraîneur (sans passe professeur) | 3,6452 | 3,4493 | 3,3628 |
| pour mémoire : l'ancien code α = 0,9 (tête principale surpondérée) | 3,5090 | 3,2835 | 3,1863 |

**Trois lectures, dans l'ordre de l'importance :**

1. **Depuis zéro, la distillation native ne gagne rien** à ce budget : −0,03 à −0,00, et le signe
   n'est même pas stable avec la longueur. **Depuis une initialisation entraînée**, elle gagne
   **−0,06** (fiche production § 4) : ce n'est pas le schéma qui est inutile, c'est **le point de
   départ** qui décide. Un élève sans bases n'a que faire d'une distribution fine ; un élève déjà
   entraîné, si.
2. **Le harnais déplace la PPL de +0,06 à +0,16** : les deux runs de la paire (α = 0 et α = 0,9)
   valent ~3,70/3,57/3,53 là où le même entraînement mené par `entrainer_rope.py` vaut
   3,6452/3,4493/3,3628. Même perte au pas 1, même init, même données : la seule différence est la
   **passe du professeur et la seconde passe de l'élève** (ordre des noyaux, non-déterminisme GPU
   amplifié sur 8 000 pas). **Aucune comparaison entre deux harnais différents n'est donc sûre** —
   c'est ce qui a produit le faux gain.
3. **L'erreur est instructive, et le levier qu'elle cachait est modeste.** Le gain apparent
   venait de la **pondération de la perte**, pas des cibles douces. Mesuré proprement dans
   l'entraîneur de référence (même init, mêmes 33 Mo), le poids principal **4×** vaut
   **3,6067 / 3,3984 / 3,3129** contre 3,6452 / 3,4493 / 3,3628 — soit **−0,039 / −0,051 /
   −0,050**. C'est un levier **gratuit** (un facteur dans la perte), réel mais cinq fois plus
   petit que le −0,14 à −0,18 annoncé ; le reste de l'écart d'hier venait de l'**échelle** de la
   perte du vieux code (4 à 7× plus grande, donc un pas effectif différent sous `clip_grad_norm`).
   Deux confusions pour le prix d'une : c'est exactement ce qu'un contrôle de parité attrape.

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
