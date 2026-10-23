# Note — la règle contrastive : ce qu'il faut construire, et pourquoi c'est elle

> **Document daté.** Plan, note ou étude d'un chantier : il porte sa date et son état en tête. La
> **feuille de route courante** est [`roadmap.md`](roadmap.md) ; l'**état** est
> [`en-cours.md`](en-cours.md).

> 06/10. Suite directe des trois négatifs mesurés (`rapport-plateau-semantique.md`
> et `note-cancellation-evenementielle.md` §9). Ce document dit **quoi faire**, pas
> ce qui a été fait.

## 1. Le constat qui commande tout

| fait mesuré | conséquence |
|---|---|
| le plateau sémantique existe, à 35-42 % de la profondeur | il y a un endroit à viser |
| un modèle haut de gamme converge mieux (pire paire 0,471 contre 0,280) | il y a un écart à combler |
| **la lecture ne rattrape rien** (0,6027 au mieux, combiner dilue) | l'écart est **dans les poids** |
| **une règle locale non ciblée ne transfère pas** et dégrade les langues non vues | il faut une règle **ciblée** |

**Pourquoi la règle actuelle échoue, en une phrase** : `D += η·Δy⊗Δx` accumule les
statistiques de transition de **ce qu'elle voit**. Rien dans son écriture ne
distingue ce qui est **partagé** entre les cas de ce qui est **propre** à chacun.
Elle apprend donc le particulier, et sur un cas nouveau elle ajoute une composante
fausse.

## 1bis. LE FONDEMENT EST VALIDÉ — la langue est soustractible (06/10, 10h30)

Avant de construire la règle, une question plus simple : **le composant de langue
est-il seulement soustractible ?** Si oui, « rétroactivité négative » est la bonne
direction et la règle anti-hebbienne n'est que la façon de l'**apprendre**.

`tools/cancellation_langue.py`, sur les traces réelles de 10 langues : on prend le
« portrait de langue » `x̄_L` (moyenne sur l'article), on calcule le décalage
`δ_L = x̄_L − moyenne_des_langues`, on le **soustrait**, et on re-mesure.

**Avec son témoin obligatoire** : la même chose avec un `δ` tiré au hasard, de
**même norme**. Sans lui, on ne saurait pas si le gain vient de la langue ou du
seul fait de retirer de la norme.

| couche 10 | cos moyen | **pire paire** |
|---|---:|---:|
| brute | 0,6490 | 0,2790 |
| **δ de langue soustrait** | **0,6603** | **0,3779** |
| TÉMOIN : δ au hasard, même norme | 0,6240 | 0,2296 |

| couche | 4 | 8 | **10** | 12 |
|---|---:|---:|---:|---:|
| gain sur la moyenne | **+0,0251** | +0,0160 | +0,0113 | +0,0027 |
| gain sur la pire paire | +0,0519 | −0,0054 | **+0,0989** | +0,0887 |
| témoin (moyenne) | −0,0363 | −0,0271 | −0,0250 | −0,0365 |

**Trois choses établies :**

1. **Le gain est réel et il est de la langue** : le vrai δ monte, un δ aléatoire de
   même norme **baisse**. La soustraction ne retire donc pas de l'énergie, elle
   retire une **direction**.
2. **L'effet est maximal sur la PIRE PAIRE, au plateau** : +0,099 à la couche 10,
   soit 0,279 → 0,378 (**+35 %**). C'est exactement la cible — le grand modèle fait
   0,280 → 0,471.
3. **La direction existe donc, et elle est apprenable** : c'est un décalage, et un
   décalage est ce qu'une règle locale peut accumuler.

**Ce que ce n'est PAS** : `δ` est calculé **sur les langues de test**, donc c'est un
**oracle**. Le chiffre est une **borne supérieure** de ce qu'un apprentissage
atteindrait, pas une méthode déployable. Il dit que la direction existe — pas
qu'on sait la trouver sans les étiquettes.

## 2. La règle qu'il faut : anti-Hebbien sur le différentiel INTER-LANGUE

```text
  pour chaque paire de langues (A, B) et chaque position ALIGNÉE p :
      Δx = x_A(p) − x_B(p)        ce qui change quand la langue change
      Δy = y_A(p) − y_B(p)        ce que la sortie change en conséquence
      D -= η · Δy ⊗ Δx            on SUPPRIME la réponse au changement de langue
```

**Le signe moins est tout.** La règle de Hebb renforce ce qui varie ensemble ;
celle-ci **annule** ce qui varie avec la langue. Et c'est là qu'est le **terme de
partage qui manquait** : ne pénaliser que ce qui *change avec la langue*, c'est
préserver, par construction, tout ce qui ne change pas — donc le sens.

C'est exactement la « rétroactivité négative sur des grappes d'activation
récurrentes » et les « patterns qui émergent après cancellation ».

## 3. Les deux conditions, et comment les remplir

### Condition 1 — l'alignement au niveau du jeton

Le différentiel `x_A(p) − x_B(p)` n'a de sens que si `p` dit **la même chose**
dans les deux langues. L'UDHR donne l'alignement **par article** (les 30 articles
sont alignés dans les 456 langues, vérifié), mais pas au jeton — les longueurs
diffèrent (33 jetons en anglais, 174 en hindi).

**Trois voies, de la plus simple à la plus fidèle :**

1. **Par la position relative** — rééchantillonner chaque article à un nombre fixe
   de points (par exemple 32) par interpolation sur la longueur. Grossier mais
   immédiat, et suffisant pour une covariance de moyennes.
2. **Par les moyennes d'article** — utiliser `x̄_A − x̄_B` (la moyenne sur tout
   l'article) plutôt que position par position. **Aucun alignement requis**, et
   ça capture exactement l'offset de langue. C'est la voie à essayer d'abord.
3. **Par alignement forcé** — l'UDHR a des traductions **officielles et
   parallèles** ; un aligneur (ou les numéros d'article et de paragraphe) donne
   des paires de phrases sûres.

### Condition 2 — la dimension de l'adaptateur

`HebbDiff` s'applique à la **sortie d'une projection** : sa forme est
`n_out(sortie) × n_in(entrée)`. Or `--trace-flux` enregistre l'entrée de la couche
(base 0) et l'entrée de la FFN (base 1000), **toutes deux de largeur cachée** — il
ne contient pas la sortie de la porte (largeur FFN).

**Deux réponses :**

1. **Élargir la trace** : ajouter un `cb` sur la sortie de la porte (`gate`) dans
   `forward_lot` et `forward`, pour que la trace porte le `y` dont la règle a
   besoin. C'est le plus direct.
2. **Adapter le flux résiduel** au lieu de la porte : une matrice
   `caché × caché` appliquée à la sortie de la couche. La trace suffit alors,
   mais `HebbDiff` doit apprendre à viser un autre point du graphe.

## 4. Le protocole de vérification, écrit d'avance

**Le test tenu à l'écart est obligatoire, et il a déjà attrapé une fausse
réussite ce soir** (+11,7 % en apparence, −5 à −10 % en réalité) :

1. entraîner sur l'article 1 en **N langues**, en **excluant** M langues ;
2. mesurer le plateau sur les **M langues exclues** — et **entre elles**, pas
   seulement contre les langues d'entraînement ;
3. comparer à trois références : sans adaptateur, la règle de Hebb actuelle (pour
   montrer que le contraste est ce qui change), et le modèle haut de gamme.

**Critère de réussite, écrit comme un taux** : le cosinus moyen des paires tenues
à l'écart doit **monter** vers celui du grand modèle (0,6027 → au-delà de 0,69), et
**la pire paire** doit monter (0,28 → au-delà de 0,47). Un gain sur la moyenne
seule ne suffit pas : c'est sur la pire paire que se joue « répondre la même chose
dans toutes les langues ».

## 5. Ce qui existe déjà, et qui sert

- `HebbDiff` — l'adaptateur : forme, seuil d'événement, décroissance, **sauvegarde
  et rechargement** (`DRAVE_HEBB_SAUVER` / `DRAVE_HEBB_CHARGER`) ; il ne reste
  qu'à changer le **signe** et la **source du différentiel** ;
- `--trace-flux` / `--flux-forcer` — capture et rejeu exact, par couche ;
- `tools/plateau_multilingue.py`, `tools/lecture_plateau.py`,
  `tools/invariance_semantique.py` — la mesure, déjà écrite et éprouvée ;
- `tools/extrait_udhr.py` — les unités alignées, 456 langues ;
- le corpus Wikipedia en local (81 Go, 6 langues) pour l'étape « domaine ».

**Ce qui manque, en une ligne** : `D -= η·Δy⊗Δx` avec `Δ` pris **entre langues**,
et la trace élargie pour porter `y`.
