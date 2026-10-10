# Note — la périphérie de C8 : entrées, sorties, réflexes

> **2026-10-10 13:48 HAE**, **mise à jour à 14:19 : la conception est IMPLÉMENTÉE** et mesurée —
> `--entree signal:F`, `--entree-canal`, `--entree-gain`, `--entree-jeton`, `--delai`,
> `--recurent`, `--sortie F`, avec la porte `tools/porte-peripherie.sh` (déterminisme, entrée
> constante, délai exact, quatre refus, paires par décision). Le résultat est dans
> [`reports/rapport-c8-peripherie.md`](../reports/rapport-c8-peripherie.md) : **le signal courant
> est dans la sortie (R² 0,913 en récurrent), la mémoire du signal n'y est pas (R² −0,973)** —
> la poursuite demande un entraînement, pas du câblage. Ce qui suit reste la conception
> d'origine, conservée telle quelle ; les écarts avec ce qui a été livré sont notés au § 2.

## 1. Ce que le plan demande (et ce qui est déjà fait)

`docs/plan-cerveau-complet.md` § C8 — « Périphérie (capteurs, effecteurs, réflexes) » :

- **régions frontière** : une **entrée** (flux continu, horloge propre) et une **sortie**
  (effecteur, avec délai) ;
- **réflexes** : des liens qui **court-circuitent** le centre — une région répond à une entrée
  sans passer par le graphe profond ;
- **interface** : `--entree <type:chemin>`, `--sortie <type:fichier>`, `--reflexe <de:vers>` ;
- **invariant** : une entrée constante produit une sortie constante (déterminisme) ;
- **validation** : une tâche fermée (contrôle d'un signal simple), mesurée en **événements par
  décision** — la métrique du projet.

**Déjà mesuré (la moitié « réflexe »)** : un chemin court qui lit un état intermédiaire, sa tête
entraînée, sa généralisation et sa vitesse — `reports/rapport-c8-sonde-profondeur.md`,
`rapport-c8-tete-entrainee.md`, `rapport-c8-generalisation.md`, `rapport-c8-transfert-corpus.md`.
Le résultat qui compte pour la conception : **l'état de 16 couches contient l'information**
(40,8 % contre 4,0 % pour une sonde linéaire), mais la tête du modèle ne sait pas la lire —
il faut une **tête par profondeur**, et elle va **×1,54 plus vite**.

**Reste à faire** : les régions frontière elles-mêmes (l'entrée et la sortie), et la tâche fermée.

## 2. La conception minimale, celle qu'on peut mesurer

Plutôt qu'un banc vision (le plan en parle, mais il n'y a pas d'image dans ce dépôt), la
périphérie la plus **mesurable immédiatement** est **un signal** : une entrée scalaire par pas, une
sortie scalaire par pas, et une tâche fermée de **poursuite de consigne**.

| élément | proposition | pourquoi celle-là |
|---|---|---|
| **entrée** | `--entree signal:<fichier>` : une valeur par pas, lue en flux | un fichier se relit, se rejoue, et se compare — c'est le format que le dépôt utilise partout |
| **encodage** | la valeur module **un canal du bus** (`--bus`) ou une **activation injectée** sur la première couche | les deux mécanismes existent déjà (C5 pour le bus, C2/C6 pour l'injection d'état) : rien à inventer |
| **sortie** | `--sortie <fichier>` : la valeur prédite par le moteur à chaque pas (argmax ramené sur le signal, ou la norme de l'état de sortie) | l'effecteur du plan : « rien ne sort » aujourd'hui, c'est le manque à combler |
| **délai** | `--delai N` : la sortie est écrite N pas après l'entrée | le plan le demande explicitement, et un délai est déjà un paramètre de lien (C3) |
| **réflexe** | `--reflexe de:vers` : la sortie est produite par une **plage courte** (le chemin mesuré) au lieu du graphe complet | **livré autrement** : `--couches a:b --tete-partielle` dans la boucle de périphérie (mesuré : 119,3 M de paires par décision à 8 couches contre 357,8 M en complet). Un drapeau `--reflexe` séparé n'a pas été ajouté : il ferait doublon avec une option qui existe et qui est vérifiée |
| **récurrence** | *(non prévu dans la conception)* `--recurent` : positions croissantes, historique dans le cache KV | sans lui, chaque pas est une **décision indépendante** et « poursuivre » n'a pas de sens — ajouté en cours de route, et c'est lui qui rend la mémoire du signal mesurable |

## 3. La porte à tenir (écrite AVANT le code)

1. **entrée constante ⇒ sortie constante** : deux exécutions avec le même signal d'entrée, la même
   graine et les mêmes options doivent rendre des sorties **identiques au bit près** (le
   déterminisme est l'invariant du plan, et le moteur l'a déjà pour le reste) ;
2. **le délai est réel et mesuré** : `--delai N` décale la sortie de **exactement N pas** —
   vérifiable en corrélant l'entrée et la sortie sur un signal connu (une marche) ;
3. **le réflexe est plus rapide ET moins bon** : sur la même tâche, la plage courte doit produire
   la sortie en **moins de temps** et avec une **erreur plus grande** que le graphe complet ; les
   deux chiffres sont publiés ensemble — un réflexe qui ne paie pas sa vitesse ne sert à rien ;
4. **la métrique du plan est calculée** : **événements (paires) par décision**, pour le chemin
   complet et pour le réflexe. C'est la seule unité qui se compare entre architectures, et elle
   est déjà instrumentée (`paires (poids × activation) par token`).

## 4. Ce qui pourrait invalider la conception

- **le signal comme seule périphérie** : si la tâche fermée se résout avec une table de
  correspondance (entrée → sortie), la mesure ne dit rien du **cerveau** — d'où la tâche de
  **poursuite** (la sortie dépend de l'état, pas seulement de l'entrée du pas) ;
- **un effecteur qui lit la bonne réponse** : si la sortie est un argmax sur le vocabulaire, la
  comparaison au signal est indirecte et la mesure peut être un artefact de tokenisation. La
  sortie doit être **une valeur**, pas un jeton ;
- **la latence du réflexe** ne se mesure bien que si le chemin court est réellement plus court —
  mesuré ×1,54 à 16 couches sur 24, ce qui est peu : un réflexe à 8 couches irait plus vite, mais
  la fiche de profondeur dit ce que la tête y lit.

## 5. Ordre de travail proposé

1. `--entree signal:F` + `--sortie F` + `--delai N`, avec la porte § 3.1 et § 3.2 (déterminisme et
   délai) — c'est le socle, et il ne dépend d'aucune tête entraînée ;
2. la tâche fermée (poursuite d'une consigne), avec la porte § 3.4 (événements par décision) ;
3. `--reflexe de:vers` branché sur une plage courte **avec tête entraînée**, et la porte § 3.3
   (plus rapide, moins bon) ;
4. alors seulement, si la tâche le demande : une **vision** (patchs) comme type d'entrée
   supplémentaire.
