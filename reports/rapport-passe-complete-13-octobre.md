# Deux passes complètes dans la même nuit — et ce qu'elles ont attrapé

> Campagne : **outillage** · expérience : la passe complète des portes (`tools/toutes-les-portes.sh`)
> Question : après une nuit de changements du moteur (prélecture parallèle, lecture séquentielle
> dans nos tampons, chargement paresseux, pool VRAM), **les portes tiennent-elles toutes** ?
> Verdict : **oui pour le moteur** — aucun chiffre de référence n'a bougé, `porte-flux.sh` rend
> exactement 61,9920 / 60,8135 après chaque changement. Mais les deux passes ont attrapé **quatre
> portes qui ne mesuraient plus rien** (elles dépendaient d'un fichier `/tmp` disparu) et **une
> porte fragile que je venais d'écrire** (elle lisait `chargées en …s` alors que le moteur imprime
> `…ms` sous la seconde). État final : **35 vertes sur 37**, les deux rouges étant ceux de la
> botte de foin, instruits et non moteur.
> Date réelle : **2026-10-12 23 h 00 → 2026-10-13 02 h 25 HAE** (heure lue sur la machine)
> Protocole : `tools/toutes-les-portes.sh` (chaque porte bornée à 1 800 s, journal gardé dans
> `/tmp/portes-1012-23h00` puis `/tmp/portes-1013-01h13`)

## 1. Les deux passes

| passe | portes | verdict | durée | rouges |
|---|---:|---|---:|---|
| 2026-10-12 23 h 00 | 36 | **34 vertes, 2 rouges** | ~74 min | `porte-indice`, `porte-melange` (botte de foin) |
| 2026-10-13 01 h 13 | 37 | **34 vertes, 3 rouges** → **35/37 après correction** | ~68 min | les deux mêmes, plus `porte-push-paresseux` (**défaut de la porte**, corrigé à 02 h 25) |

Entre les deux, le moteur avait changé **une fois de plus** (le pool de tampons VRAM), et la porte
de la paresse était née. Aucune porte n'exerce le chemin VRAM : le pool est couvert par son propre
A/B (`reports/rapport-vram-transfert.md` § 5), pas par la passe — c'est écrit ici pour que personne
ne croie le contraire.

## 2. Ce que la première passe a attrapé : quatre portes qui ne mesuraient plus rien

`porte-greffe`, `porte-indice`, `porte-melange` et `porte-topologie` sortaient **« code 2 »** —
c'est-à-dire « je ne peux pas mesurer », ce qui n'est ni vert ni rouge et passait inaperçu. Cause
unique : leurs prérequis vivaient dans `/tmp`, que chaque redémarrage emporte. **Réparé par les
défauts, pas par des variables** :

* les trois portes à aiguille lisent une botte de foin **versionnée** dans le dépôt
  (`tools/niah_4096_0.5.txt`) ;
* `porte-topologie` **régénère** son corpus et ses identifiants (`~/IA/scratch/prerequis/`), et sa
  limite est bornée comme celle de l'artefact de campagne.

## 3. Ce que la seconde a attrapé : ma propre porte, fragile à l'unité d'un nombre

`porte-push-paresseux.sh` (écrite à 23 h 05) comparaît les temps de chargement en lisant
`chargées en [0-9.]+s`. Le moteur imprime une durée `{:?}` : **`601.034622ms`** quand le chargement
passe sous la seconde, **`7.36s`** sinon. La porte **passait sur une machine lente** (1,42 s au
premier essai) et rendait une chaîne **vide** sur une machine rapide (0,68 s) — d'où un `float("")`
en pleine passe. Corrigée (l'unité est lue, et la porte refuse de mesurer sur du vide — elle imprime
la sortie brute du moteur). **C'est la passe qui l'a vue, pas une relecture** : une porte qui n'a
tourné que dans les conditions de son auteur n'a pas tourné.

## 4. Ce que les deux passes n'ont PAS dit

* **rien du chemin VRAM** : aucune porte ne l'exerce (`DRAVE_GPU_EXPERTS` n'apparaît dans aucun
  `tools/porte-*.sh`) ;
* **rien de la botte de foin** : les deux rouges restants disent seulement que le critère
  « mieux que le hasard » est marginal (mesuré : 2 fenêtres sur 5 passent,
  `reports/rapport-niah-fragilite.md`) ;
* **rien des temps** : plusieurs portes mesurent des latences, et la machine portait aussi un banc
  GPU et une carte de sorties pendant la seconde passe. Les chiffres de perplexité, eux, ne
  dépendent pas de la charge.

## 5. Ce qu'il faudrait ajouter (recommandations)

1. **une porte qui exerce le chemin VRAM** — sinon le pool et les noyaux GPU vivent hors du filet
   (la moins chère : `--gpu-banc` sur un tenseur d'experts, avec le débit publié et un plancher) ;
2. **`code 2` ne doit pas ressembler à un succès** : la passe affiche la marque, mais un `code 2`
   répété sur plusieurs portes devrait **arrêter la passe** — quatre portes muettes ont survécu à
   une nuit entière ;
3. **le critère d'indice extérieur** doit être refait (contrôle apparié, ou moyenne sur plusieurs
   fenêtres) : voir `reports/rapport-niah-fragilite.md` § 3.
