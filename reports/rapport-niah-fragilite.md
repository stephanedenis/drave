# Le critère de `porte-indice` ne survit pas à une reconstruction de son entrée

> Campagne : **instruments** · expérience 01 — la fragilité d'un critère, mesurée
> Question : `porte-indice` (et `porte-melange`) exigent qu'un **indice extérieur** — l'état de la
> question dans une invite qui ne contient pas l'aiguille — tombe **plus près de l'aiguille que le
> hasard** dans la mémoire épisodique. Le 12/10, sur une botte de foin **régénérée**, ce critère
> échoue (482 jetons contre 370). Est-ce le moteur, ou l'entrée ?
> Verdict : **l'entrée.** le même moteur, la même porte, le même protocole, sur **cinq fenêtres de
> remplissage** du même corpus : **deux passent** (1,21× et 1,69× mieux que le hasard) et **trois
> échouent** (de 1,30× à 2,13× *pire* que le hasard). Le critère est **marginal et dépendant du
> texte** — ce que la porte écrit elle-même (« l'effet existe et il n'est PAS robuste »). La botte
> de foin de la campagne n'a **jamais été versionnée** : sa disparition a donc transformé un
> critère fragile en deux portes rouges, sans qu'aucun chiffre du moteur ait bougé.
> Date réelle : 2026-10-13, 00 h 20-01 h 03 HAE (heure lue sur la machine)
> Protocole : `SRC=/tmp/niah_f<f>.txt tools/porte-indice.sh` (botte générée par
> `tools/construire-niah.py --fenetre <f>`), cinq fenêtres : 0,00 · 0,15 · 1/3 · 0,50 · 0,75

## 1. Les mesures

| fenêtre de remplissage | distance à l'aiguille | hasard | verdict |
|---|---|---|---|
| 0,00 | 315 jetons | 381 | ✅ **1,21× mieux** (marge faible, la porte le dit) |
| 0,15 | 262 jetons | 444 | ✅ **1,69× mieux** |
| **1/3** (celle qui est versionnée) | 482 jetons | 370 | ❌ |
| 0,50 | 731 jetons | 334 | ❌ |
| 0,75 | 808 jetons | 380 | ❌ |

Ce que ça dit :

* **le critère n'est pas une propriété du moteur, c'est une propriété du couple (moteur, texte)** :
  deux fenêtres passent, trois échouent, avec des marges de part et d'autre du hasard. Une porte
  qui dépend d'un texte **non versionné** ne peut donc pas distinguer « le moteur a changé » de
  « l'entrée a changé » — c'est exactement ce qui s'est produit le 12/10 ;
* **les deux réussites sont marginales** (1,21× et 1,69×) et la porte **avertit** elle-même en
  dessous de 2× : « la marge est FAIBLE : un indice quasi identique donne 378 jetons au lieu de
  136. L'effet est réel mais NON ROBUSTE. » Le savoir était donc déjà dans la porte ; ce qui
  manquait était la **distribution** ;
* **ce n'est pas une régression du moteur** : la perplexité, les portes, les repères sont
  identiques, et la même porte passe sur d'autres fenêtres avec le **même** binaire.

## 2. Ce que je n'ai pas fait, et pourquoi

**Je n'ai pas choisi la fenêtre qui passe.** C'est possible (0,15 donne 1,69×) et cela rendrait les
deux portes vertes — mais une porte verte obtenue en choisissant l'entrée qui la fait passer ne
vérifie plus rien : elle dirait « le moteur va bien » alors qu'elle mesurerait « le texte est
favorable ». Le dépôt applique déjà cette règle sous une autre forme (« une mesure d'inertie faite
là où l'inertie est attendue ne dit rien »).

Ce qui a été fait à la place : **versionner l'entrée** (`tools/niah_4096_0.5.txt`, avec
`tools/construire-niah.py` et son option `--fenetre`), garder les deux portes **rouges** avec leur
cause écrite, et publier la distribution ci-dessus.

## 3. Ce que la porte devrait mesurer (recommandation, écrite avant tout code)

Le critère actuel compare une distance à **un hasard calculé sur le même texte**, et exige
seulement « mieux que le hasard ». Trois corrections possibles, par ordre de coût :

1. **un contrôle apparié** : la **même** invite, la **même** longueur, la même aiguille, mais une
   question dont on sait qu'elle ne désigne pas l'aiguille (l'écart des distances devient
   l'effet — le texte s'annule) ;
2. **une moyenne sur plusieurs fenêtres** (avec la distribution, pas seulement le verdict) : c'est
   ce que cette fiche fournit pour cinq d'entre elles ;
3. **un seuil tiré de la distribution**, pas du hasard : exiger, par exemple, que l'effet dépasse
   la dispersion mesurée sur 5 à 10 fenêtres.

Tant que l'une de ces corrections n'est pas faite, **les deux portes restent rouges par
construction** — et c'est écrit ici pour que personne ne les croie cassées.
