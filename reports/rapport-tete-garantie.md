# Rapport — restriction de tête GARANTIE : exacte, et sans gain

Chantier 2 de la session. La question posée était précise : peut-on ne pas
calculer tous les logits **sans jamais changer la sortie**, en chargeant
dynamiquement les logits manquants, avec une borne de Cauchy-Schwarz sur les
lignes hors liste et une extension par paliers quand la borne ne conclut pas ?

**Réponse : oui, c'est implémenté et exact — et non, ça ne fait rien gagner.**
La borne est 12,6 fois plus lâche que le logit maximal sur les poids réels, donc
toutes les lignes restent candidates et le moteur finit par tout calculer.

## 1. Ce qui est implémenté

`--tete-garantie <fichier>` (`logits_garanti`, `drave-core/src/model.rs`) :

1. une passe unique calcule `||w_i||` pour les 151 936 lignes de la tête et les
   trie par norme décroissante ;
2. à chaque jeton, les logits de la liste de candidats sont calculés ;
3. toute ligne non calculée est bornée par `||w_i|| · ||h||` (Cauchy-Schwarz dans
   la même unité que le produit scalaire : `qx` et `sx` de la quantification) ;
4. si la plus grande borne dépasse le meilleur logit connu, on étend par paliers
   — les lignes étant triées par norme, le premier non calculé porte la borne
   maximale ;
5. si la borne ne conclut jamais, la liste atteint le vocabulaire entier : c'est
   la réponse juste, pas une réponse rapide et fausse.

**Exactitude vérifiée** : mêmes jetons générés avec et sans l'option, sur
Qwen2.5-0.5B, prompt « Le ciel est bleu parce que », 8 jetons gloutons :

```
sans  : [512, 13309, 321, 1788, 12422, 84, 13, 356]
avec  : [512, 13309, 321, 1788, 12422, 84, 13, 356]
```

C'est le contrat : la sortie ne change **pas**.

## 2. Ce qui est mesuré, et qui condamne la méthode

Sur la vraie matrice de tête (Qwen2.5-0.5B, 151 936 × 896 en Q8_0, 2 048 lignes
échantillonnées, activation aléatoire de même dimension) :

| grandeur | valeur |
|---|---|
| logit maximal | **+1,4283** |
| borne globale `max ‖w_i‖·‖h‖` | 18,0381 — **×12,6** le logit max |
| borne par blocs de 32 `Σ_b ‖w_b‖·‖h_b‖` | 17,6646 — ×12,4 |
| lignes encore candidates (globale) | **2 048 / 2 048 = 100 %** |
| lignes encore candidates (par blocs) | **2 048 / 2 048 = 100 %** |

Le raffinement par blocs n'apporte rien : la perte dominante est l'**alignement**
entre `w` et `h`, pas la structure par blocs. Et à l'exécution, la boucle de
paliers a effectivement calculé **151 936 lignes sur 151 936** à chaque jeton.

C'est le même verdict que la session précédente (borne « 5 à 20× trop lâche »),
mais il est maintenant établi sur les poids réels, avec le mécanisme en place et
la preuve d'exactitude — et non par un raisonnement sur une borne.

## 3. Ce que ça laisse

Une restriction de tête ne peut payer que d'une façon : si la liste de candidats
est **connue** comme contenant la réponse. C'est le cas de la génération
contrainte (grammaire, choix fermé, liste de tokens d'une langue), et c'est
`--tete-restreinte` — qui **change la sortie**, donc refusé en perplexité et
annoncé comme tel.

Le compromis est donc net, et il est écrit dans le code :

| voie | gain | sortie |
|---|---|---|
| `--tete-restreinte` | ×7 sur la tête (13 % du vocabulaire suffit) | **changée** — génération contrainte |
| `--tete-garantie` | **nul** (12,6× trop lâche) | identique, prouvé |

Il n'existe pas, sur ces poids, de troisième voie : aucune borne utilisable ne
distingue les lignes hors liste avant de les avoir lues.

## 4. Méthode

Deux leçons de cette session s'appliquent ici aussi :

- la première version de la boucle bornait le **maximum** des lignes hors liste
  par la norme de la **première** ligne non calculée : c'est correct *parce que*
  les lignes sont triées par norme décroissante, et ça ne se voit pas — le tri
  est donc commenté comme faisant partie de la preuve, pas comme une commodité ;
- la borne doit être calculée dans la **même unité** que le produit scalaire
  (`q·s` après quantification de l'activation), sinon elle ne borne rien.

---

# Annexe — chargeur d'experts : lecteurs parallèles, mesurés sur fichier froid

Chantier 4. Le disque NVMe de cette machine a été mesuré à **5,37 Go/s avec un
lecteur et 31 Go/s avec seize** ; il y avait donc un facteur 5 à prendre si le
défaut de page sérialisait les lectures d'experts. Mesure appariée sur deux zones
distinctes (donc des octets différents), `posix_fadvise(DONTNEED)` pour forcer le
froid, 120 blocs de 4 Mo — l'ordre de grandeur d'un expert :

| support | 1 lecteur | 16 fils | rapport |
|---|---|---|---|
| disque mécanique (13 To) | 0,26 Go/s | 0,20 Go/s | **×0,78** |
| NVMe (FastNVMe) | 3,11 Go/s | 2,72 Go/s | **×0,88** |

**Les lecteurs parallèles n'apportent rien, et coûtent un peu.** Deux raisons,
qui sont deux mesures en soi : sur le mécanique, la tête se déplace et le
parallélisme ne fait que l'ajouter aux seeks ; sur le NVMe, l'avance de lecture
du noyau sature déjà le périphérique avec UN flux séquentiel — le facteur 5,8
mesuré entre un et seize lecteurs valait pour des lectures explicites, pas pour
des défauts de page qui bénéficient du readahead.

C'est la cinquième fois qu'un mécanisme de prélecture est mesuré ici, et la
cinquième fois qu'il ne donne rien. La différence, cette fois, est qu'on sait
pourquoi : ce n'est pas le cache de pages qui masque l'effet (le froid est forcé
et vérifié), c'est que le noyau fait déjà le travail.

Ajouté : `tools/mesurer_lecture_experts.py`, qui rejoue la mesure en une commande.
