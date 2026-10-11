# Drave en mode impulsion pur serait-il un meilleur apprenant ?

> 9 octobre 2026. Question posée telle quelle. Réponse en trois temps : ce que
> « impulsion pure » peut vouloir dire chez nous, ce que nos propres mesures disent
> déjà, et les mécanismes supplémentaires qu'il faudrait — avec le protocole qui
> trancherait.

---

## 1. Trois sens de « mode impulsion pur », et ils n'ont pas le même avenir

| sens | état dans Drave | verdict |
|---|---|---|
| **exécution** par événements (aucun produit dense) | **fait** : le chemin par listes, les paires (poids × activation), le flux réparti | le coût suit déjà l'activité |
| **apprentissage** par événements (ne mettre à jour que les poids touchés) | **non** : l'entraînement est hors moteur, et chaque pas met à jour **tous** les paramètres | c'est là que la question se joue |
| **représentation** impulsionnelle (le temps porte l'information) | **non** : un jeton est un vecteur dense, pas une salve | le plus spéculatif, et le plus intéressant |

**Le point dur est le deuxième**, et il se chiffre : notre exécution la plus économe
touche **25 % des activations × 50 % des poids = 12,5 %** des poids par jeton
(campagne, § 5 ter), alors qu'un pas d'entraînement par gradient en touche **100 %**.
Autrement dit : **notre apprenant coûte huit fois plus cher que notre exécutant, en
unités de poids touchés.** C'est exactement l'écart qu'un mode impulsion pur
supprimerait — s'il apprenait aussi bien.

---

## 2. Ce que nos mesures disent déjà, et c'est presque tout

Quatre résultats du dépôt, obtenus sur ce moteur, encadrent la réponse.

**(a) La corrélation locale seule n'apprend pas.** `--hebb-diff` (Δx, Δy, seuil
d'événement, décroissance, forme signée) : gains en échantillon −0,73 % au mieux,
**transfert nul** sur un autre texte, et **dégradation de 5 à 10 % sur des langues
non vues**. Cause écrite au verdict : rien ne distingue le partagé du spécifique
(`docs/hebbien-differentiel-et-biologie.md`).

**(b) Un signal global, lui, apprend.** La distillation (−13,8 % sur un modèle routé
à dim 512 ; −0,3 % sur un dense creux) est notre seul mécanisme de crédit, et il
fonctionne. C'est la version « hors moteur » de ce que la biologie appelle un
neuromodulateur.

**(c) Les contraintes dures apprises marchent.** k-WTA à 25 % : le modèle creux fait
*mieux* que dense, là où le témoin s'effondre (+118 %). Élagage appris à 50 % :
÷2 lectures, qualité inchangée (+0,3 %). **Le substrat accepte d'apprendre sous
contrainte** — c'est la condition d'un apprenant événementiel.

**(d) Un connectome inné aléatoire coûte 1 % — ATTENTION : sur l'attention seulement, rétracté le 11/10 (+9,4 % pour le modèle entier).** Masque de 25 % des connexions tiré à
la naissance, jamais modifié : perplexité 5,0472 contre 4,9959, événements **÷4,1**,
débit **×2,1** (§ 4 bis de `biologie-pour-drave.md`). **La structure peut être
innée ; seuls les poids ont besoin d'être appris** — et c'est précisément ce qui rend
un apprenant local *borné* : il n'a que 25 % des poids à considérer.

**Ce que ces quatre points disent ensemble** : un apprenant par impulsion n'est pas
condamné par (a) — (a) réfute une règle *sans crédit ni décorrélation*, pas le
principe. (b) dit ce qui manque. (c) et (d) disent que le substrat est prêt.

---

## 3. Les mécanismes supplémentaires, et ce que chacun achète

| mécanisme | ce qu'il remplace | ce qu'il coûte | état chez nous |
|---|---|---|---|
| **traces d'éligibilité + troisième facteur** (pré × post × modulateur global) | le crédit global de la rétropropagation | un scalaire diffus, pas un gradient par poids | `--hebb-diff` a la trace et le seuil ; **le modulateur manque** (E7) |
| **anti-Hebbien / décorrélation** (soustraire la moyenne ou la direction dominante) | la normalisation implicite des couches | une soustraction par pas | **manque** (E8) — et c'est la correction que notre verdict réclame |
| **rétroaction de crédit** (alignement par rétroaction, propagation d'équilibre, codage prédictif) | la rétropropagation exacte | une passe de plus, non différentiable | la voie « prédire une couche pour ne transporter que l'imprévu » est consignée (`c4ffbc8`), pas implémentée |
| **code temporel** (latence, rang) | le vecteur dense par pas | un ordonnancement, une horloge | **rien** — c'est le sens 3 du § 1 |
| **plasticité structurelle** (naissance/élagage) | l'architecture figée | un mécanisme de croissance | l'élagage existe ; la **naissance** non (E9 : seules les caractéristiques *non linéaires* ajoutent de la capacité) |
| **homéostasie** | la stabilité | un contrôle de taux | notre décroissance/écrêtement en est la version fruste : **sans elle, η = 1e-3 diverge** (+33 %) |

---

## 4. « Meilleur » selon quel critère ? Les trois métriques, et une seule est favorable

1. **Qualité par échantillon vu.** Rien dans nos mesures ni dans la littérature ne
   suggère qu'une règle locale batte la rétropropagation ici : notre meilleure règle
   locale ne transfère pas du tout. **Défavorable.**
2. **Qualité par unité de calcul — la métrique de Drave.** L'exécution est déjà
   proportionnelle aux paires ; un apprenant événementiel rendrait les **mises à jour**
   proportionnelles aux événements aussi (÷8 dans notre configuration creuse). Si la
   qualité tient, c'est un gain structurel. **Favorable en principe, non mesuré.**
3. **Généralisation hors échantillon.** Notre règle locale *dégrade* les langues
   non vues ; la distillation, elle, améliore. **Défavorable aujourd'hui.**

**Et un argument que nos mesures portent, et qui n'est pas dans la littérature** :
nous avons mesuré que **le format d'exécution fait partie du modèle** — le même
modèle entraîné deux fois plus longtemps est meilleur en fp32 (1,8237) et pire après
export Q4_0 (5,3845), la pénalité de quantification passant de +0,445 à +0,605
bit/octet, soit **+36 %**. Autrement dit : **« apprendre ailleurs, puis exporter » a
un coût caché qui croît avec l'entraînement.** Apprendre *dans le substrat* où l'on
exécute supprime ce coût par construction. C'est le meilleur argument qu'on ait pour
un apprenant embarqué — et il vient d'une mesure, pas d'une intuition.

---

## 5. Le protocole qui trancherait

Trois apprenants, un seul modèle, une seule tâche (byte-level, dim 384, le corpus de
la campagne), et **une seule métrique : la qualité en fonction du coût cumulé** —
paires lues et **poids mis à jour**, plus le temps et les octets.

| apprenant | ce qu'il fait | état |
|---|---|---|
| **L1** gradient hors moteur | la recette actuelle : entraîner en fp32, exporter, exécuter | **fait** (témoin : 4,9959) |
| **L2** gradient + contraintes apprises | k-WTA 25 % + élagage 50 % appris (la recette du § 5 ter) | **fait** (5,1866 à 42,2 M d'événements) |
| **L3** apprenant embarqué | mises à jour **seulement sur les poids touchés**, modulées par un signal global (perte ou nouveauté), avec décorrélation anti-Hebbienne, sur un **connectome inné** (25 %) | **à construire** — les briques existent (`--hebb-diff` sait accumuler, seuiliser, décroître, signer, **sauver et recharger**) |

### 5 bis. E7 et E8 IMPLÉMENTÉS ET MESURÉS — et le résultat est négatif

Les deux mécanismes ont été écrits dans le moteur le 9 octobre (`DRAVE_HEBB_MODULE`,
`DRAVE_HEBB_DECORRELE`, plus la persistance de `D` — `DRAVE_HEBB_D_SAUVE` et
`DRAVE_HEBB_D_CHARGE` — sans laquelle le test hors échantillon n'existe pas). Le
protocole : adapter `D` sur **A** (WikiText anglais, 256 jetons, couche 12, η = 4e-4,
seuil + décroissance + forme signée), **puis évaluer sur B** (français, 128 jetons)
sans autre apprentissage que celui qui continue en ligne.

| configuration | perplexité sur B | écart à la référence |
|---|---:|---:|
| **référence, sans adaptateur** | **8,3869** | — |
| règle actuelle (seuil + décroissance + signes) | 8,8246 | **+5,2 %** |
| **+ décorrélation (E8)** | 8,8225 | +5,2 % — *inerte* |
| **+ modulation par nouveauté (E7)** | **10,1034** | **+20,4 %** |
| + les deux | 10,0974 | +20,4 % |

**Trois enseignements, et aucun n'est celui qu'on espérait.**

1. **Le transfert A → B dégrade** (+5,2 %) : le verdict précédent est reproduit dans
   un protocole compact — une matrice apprise sur une langue nuit à une autre.
2. **La décorrélation est inerte** à cette échelle : soustraire une moyenne courante
   (β = 0,01 sur 256 pas) ne change rien au chiffre. Elle n'est pas réfutée, elle est
   **trop lente** pour ce protocole, et c'est écrit comme tel.
3. **Moduler par la NOUVEAUTÉ est le contraire de ce qu'il faut** (+20 % au lieu de
   +5 %). L'explication est simple une fois le chiffre connu : la nouveauté est
   maximale **exactement sur l'entrée hors distribution**, donc la modulation
   amplifie l'apprentissage de ce qui est spécifique à la nouvelle langue — le défaut
   qu'on voulait corriger.

**Ce que cela corrige dans ce document** : le troisième facteur de la biologie n'est
pas « la nouveauté », c'est **l'utilité** — ce que la dopamine code n'est pas
« c'est nouveau » mais « ça a marché ». Or notre seul mécanisme d'utilité mesuré
comme efficace est la **distillation** (−13,8 % sur un modèle routé) : un signal
global venu d'une cible, pas une statistique locale. La conclusion du § 6 s'en trouve
resserrée : ce qui manque à un apprenant par impulsions n'est pas un signal de
surprise, c'est un **signal de valeur**.

### 5 ter. M1 — le bus de valeur est IMPLÉMENTÉ, et la valeur auto-référentielle ne suffit pas

Le manque M1 de `docs/architecture-cerveau-et-drave.md` (un scalaire diffusé à
toutes les couches, comme un noyau neuromodulateur) est maintenant dans le moteur :
`DRAVE_HEBB_MODULE=valeur` fait piloter `η` par `hd.modulateur`, alimenté à chaque
jeton par **l'amélioration de la perte** — « ce jeton s'est-il mieux passé que la
moyenne courante ? » — avec un retard d'un jeton, comme la modulation biologique.

Même protocole que ci-dessus (adapter sur l'anglais, évaluer sur le français) :

| modulation de `η` | perplexité sur B | écart à la référence |
|---|---:|---:|
| aucune (référence) | **8,3869** | — |
| règle nue | 8,8246 | +5,2 % |
| par la nouveauté | 10,1034 | +20,4 % |
| **par la VALEUR (amélioration de la perte)** | **9,6674** | **+15,3 %** |

**La valeur est meilleure que la nouveauté — et toujours pire que rien.** Le signal
est meilleur, il ne suffit pas, et la raison est nette : une valeur **auto-référentielle**
(« ma perte baisse ») récompense exactement ce qui marche **sur le domaine courant**.
Hors distribution, cela veut dire : apprends plus vite les spécificités de la langue
nouvelle. C'est le même piège, en plus doux.

**Ce que cela spécifie pour M1** : le bus doit porter un signal **externe** — une
cible, une récompense, un environnement — et non une statistique dérivée du modèle
lui-même. C'est cohérent avec nos seules mesures positives : la **distillation**
(−13,8 % sur un modèle routé) est un signal venu d'**un autre modèle**.

### 5 quater. Le signal EXTERNE, mesuré — meilleur que les autres, et toujours insuffisant

Le moteur sait maintenant lire un modulateur **externe**
(`DRAVE_HEBB_MODULATEUR_FICHIER` : un flottant par pas). Le signal utilisé ici est
**l'avantage d'un enseignant** (R1-distill-1,5 B, même tokenizer) sur le jeton
observé, calculé à partir de ses logits exportés et rapporté à sa propre moyenne :
quand l'enseignant trouve le jeton bien plus probable que l'élève, `η` monte.

| modulation de `η` | perplexité sur B | écart à la référence |
|---|---:|---:|
| aucune (référence) | **8,3869** | — |
| **règle nue** | **8,8246** | **+5,2 % — le meilleur résultat** |
| signal **externe** (enseignant) | 9,1511 | +9,1 % |
| valeur propre (amélioration de la perte) | 9,6674 | +15,3 % |
| nouveauté | 10,1034 | +20,4 % |

**Le signal externe est le meilleur des trois modulateurs — et il ne sauve pas la
règle.** Toutes les modulations sont *pires* que ne pas moduler. C'est un résultat
plus tranchant que le précédent, parce qu'il élimine l'explication facile : le
problème **n'est pas la force ni le crédit de la mise à jour**, c'est **ce qui est
appris**. Moduler le *taux* d'une règle qui accumule les statistiques de transition
du domaine courant ne change pas la *nature* de ce qu'elle accumule.

### 5 quinquies. La décorrélation, en courbe de dose : elle améliore, et converge vers « ne rien apprendre »

La décorrélation était **inerte** à β = 0,01 (une moyenne courante trop lente sur
256 pas). β est maintenant réglable (`DRAVE_HEBB_BETA`), et voici la courbe complète
— même protocole, adapté sur l'anglais, évalué sur le français :

| β (constante de temps) | perplexité sur B | ‖D‖ |
|---:|---:|---:|
| pas de décorrélation | 8,8246 | — |
| 0,01 | 8,8244 | — |
| 0,1 | 8,7942 | — |
| 0,3 | 8,7112 | 8,70 |
| 0,5 | 8,6316 | — |
| **0,8** | **8,5381** | **8,42** |
| **1,0 (limite)** | **8,3869** = la référence **sans aucun adaptateur** | 0 |

**La décorrélation améliore de façon monotone — et la limite de la courbe est la
référence elle-même.** À β = 1, la moyenne courante *est* le différentiel courant :
le différentiel centré est nul, `D` ne bouge plus, et le moteur rend exactement le
chiffre du modèle intact. Autrement dit : **le mieux que la règle locale sache faire
hors de son domaine, c'est ne rien faire.**

*(Et ce n'est pas un simple amortissement : ‖D‖ **augmente** avec β — 8,42 contre
8,70 — donc la décorrélation change bien *ce qui* est stocké, pas seulement *combien*.)*

**Ce qu'il faudrait, et c'est maintenant précisément spécifié** : une règle
**contrastive** — soustraire explicitement ce qui est propre au domaine, au lieu de
moduler. Le verdict du dépôt le disait déjà (« `D -= η·(différentiel INTER-langue)` »),
et notre décorrélation par moyenne courante était **trop lente** pour le tester
(β = 0,01 sur 256 pas : inerte au chiffre près). C'est la prochaine expérience, et
elle est peu coûteuse : un β réglable, puis une vraie paire de contextes.

**Ce qui manque pour L3, en une phrase** : `D` est aujourd'hui un *ajout* appris en
ligne ; il faut (i) le moduler (E7), (ii) le décorréler (E8), (iii) l'appliquer à un
graphe creux inné (E1, fait), et (iv) accepter qu'il porte l'apprentissage **en plus**
des poids de base plutôt qu'à leur place — ce que le moteur sait déjà faire, sauver et
recharger.

**La prédiction à réfuter** : à budget de **poids mis à jour** égal, L3 doit
s'approcher de L2 à moins de 10 % de perplexité. Si L3 en est loin, la réponse à la
question posée est **non**, et elle sera mesurée, pas argumentée.

---

## 6. Réponse courte

**Pas en l'état, oui sous conditions, et les conditions sont nommées.** Un mode
impulsion pur est déjà notre **exécutant** ; il n'est pas notre **apprenant**. Ce qui
manque n'est pas la forme du signal (l'événement), c'est le **crédit** et la
**décorrélation** — deux mécanismes que la biologie possède, que nos mesures
réclament explicitement, et qui tiennent chacun en quelques lignes dans un moteur qui
sait déjà accumuler, sauver et recharger une matrice apprise en ligne.

Le seul avantage *structurel* démontré d'un apprenant embarqué, à ce jour, est celui
que nous avons mesuré sans le chercher : **le format d'exécution fait partie du
modèle**, et sa pénalité croît avec l'entraînement. Apprendre là où l'on exécute
n'est donc pas une élégance, c'est une économie mesurable.
