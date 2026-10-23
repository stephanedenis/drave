# Un pont par professeur — il n'y a pas de couche sémantique universelle

> **Document daté.** Plan, note ou étude d'un chantier : il porte sa date et son état en tête. La
> **feuille de route courante** est [`roadmap.md`](roadmap.md) ; l'**état** est
> [`en-cours.md`](en-cours.md).

Correction de cap, énoncée par Stéphane, et elle invalide une comparaison que
j'avais commise :

## 1. Chaque modèle a sa propre représentation sémantique interne

On travaille sur une **couche interne**. Cette couche n'a de sens que *dans* le
modèle qui la produit : elle est exprimée dans SA base, SA métrique, SA façon de
répartir l'information. **Il n'existe pas, à ce jour, de représentation
universelle d'une couche sémantique.**

Conséquences directes :

- La cible change avec le professeur. Ce n'est pas la même chose à approximer.
- Il faut donc **une version de notre modèle par professeur** — `pont_0.5B`,
  `pont_30B`, etc. Ce ne sont pas des variantes d'un même objet, ce sont des
  objets distincts, chacun ajusté contre SA cible.
- **Comparer les invariances de deux ponts ajustés sur deux professeurs
  différents n'a pas de sens** : les deux nombres appartiennent à deux espaces de
  représentation différents. Un pont plus « invariant » que le professeur d'un
  autre modèle ne veut rien dire.

## 2. La comparaison que j'avais commise, et pourquoi elle est nulle

Dans `reports/rapport-pont-generatif.md` §9, j'ai écrit que le pont génératif
(0,9425 d'invariance) « bat le professeur 30B » (0,9014). **C'est faux comme
classement.** Le 0,9014 est l'invariance de la couche 17 de Qwen3-30B-A3B, dans
la représentation propre de ce modèle ; le 0,9425 est celle de notre sortie
ajustée sur la couche 10 de Qwen2.5-0.5B. Deux espaces, deux cibles, deux objets.
Les nombres sont exacts, le classement est vide.

Ce qui reste valide : **la comparaison à l'intérieur d'un même professeur** —
notre pont contre la couche du professeur qu'il émule. C'est la seule qui dise
quelque chose.

## 3. Ne pas calculer l'« extérieur » du professeur

La tête de sortie (logits, vocabulaire) ne nous intéresse pas : ce n'est pas la
boîte noire linguistico-sémantique qu'on cherche à émuler. Or le défaut de drave
est `n: 32` — chaque traçage **générait 32 jetons** et calculait la tête.

Mesuré sur Qwen3-30B-A3B : `--n 1` **107,75 s** contre `--n 0` **108,96 s**. La
tête ne coûte donc **rien en temps** (un matvec sur un jeton, contre 350 jetons de
préfill sur 18 couches). Mais elle **change la trace** : la couche 17 de la
dernière position diffère d'un écart max de **118** entre les deux modes.

**Règle** : tout traçage de professeur se fait avec `--n 0`. Et deux jeux de
traces faits avec des `--n` différents ne sont **pas** comparables — il a fallu
reprendre les six langues de test du 30B pour cette raison.

### Et la contamination n'est pas théorique, elle est mesurée

Vérifié au jeton près, en traçant deux fois le même texte : `--n 32` donne
**542 positions**, `--n 0` en donne **510**. La différence est **exactement 32** —
les jetons générés sont bien **dans la trace**. Notre pont
s'entraînait donc pour partie sur ce que le professeur avait *inventé* après le
corpus — 6 % des positions en anglais, et bien davantage dans les langues dont le
texte donne moins de jetons. Ces positions n'ont aucun sens linguistique pour
notre usage : elles ne sont pas du corpus.

Toutes les traces ont été reprises en `--n 0`, pour les deux professeurs.

## 4. Ne pas journaliser les couches internes de NOTRE boîte noire

Notre modèle est une boîte noire linguistico-sémantique : ce qui compte est sa
**sortie** — la couche émulée. Les trajectoires internes de nos neurones ne sont
pas un livrable et n'ont pas à être écrites. `tools/pont_generatif.py` ne produit
aucun fichier de trace : il ne lit que les traces du professeur et n'écrit que ses
propres mesures.

## 5. Les universaux sémantiques : un sujet pour Panini, pas pour Drave

Une fois qu'on aura plusieurs ponts satisfaisants — un par professeur — on pourra
se demander s'il émerge des structures communes. **C'est un projet pour l'initiative
Panini (et Nipada), pas pour Drave.** Drave doit rester ce qu'il est : un moteur
qui construit, pour un professeur donné, le pont le plus fidèle possible vers sa
couche sémantique, à moindre coût et distribuable.


## 6. Second défaut, plus grave que la contamination : la TRONCATURE

En vérifiant la contamination, un motif a sauté aux yeux : des dizaines de traces
portaient **exactement 1016 positions**. Ce n'est pas une coïncidence, c'est un
plafond : `ctx 1024` moins la réserve `n + 8` = 40 laissait passer **984 jetons**
de texte, plus les 32 jetons générés.

Mesuré sur l'abkhaze, dont le texte de dix unités est le plus long :

| contexte | positions obtenues | temps |
|---|---:|---:|
| 1 024 | 1 016 (**tronqué**) | 131 s |
| 2 048 | **1 958** (complet) | 204 s |
| 4 096 | 1 958 (complet, même coût) | 183 s |

Le texte demande **1 958 jetons** : à `ctx 1024`, près de la moitié était perdue.
Sur un échantillon de dix langues d'entraînement, **5 sur 10 étaient tronquées**.

**Pourquoi c'est plus grave que la contamination.** Notre invariance se mesure sur
la **dernière position**. Si le texte est coupé, cette position n'est plus la fin
du texte : chaque langue s'arrête à son propre 984ᵉ jeton, c'est-à-dire à un
**contenu différent**. La mesure comparait donc des choses qui ne se comparent
pas — exactement le genre d'erreur qu'on traque depuis le début.

**Ce que cela fait aux résultats déjà publiés**, et il faut le dire nettement :

| jeu | contamination (32 jetons générés) | langues tronquées | solidité |
|---|---:|---:|---|
| 1 unité (article 1) | **25 à 60 %** des positions | oui | **faible** |
| 10 unités | 3 % | ~50 % | moyenne |
| **reprise `ctx 2048 --n 0`** | **0 %** | **0 %** | la seule propre |

Les résultats à **une unité** reposent donc sur des données dont **un quart à
60 %** étaient des jetons que le professeur avait *inventés* — et ils sont les
plus fragiles de tout ce travail. Les résultats à **dix unités** sont bien
meilleurs (3 % de contamination) mais souffrent encore de la troncature sur la
moitié des langues.

**Tout est repris** en `--ctx 2048 --n 0` pour les deux professeurs.
