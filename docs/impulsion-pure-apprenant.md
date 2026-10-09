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

**(d) Un connectome inné aléatoire coûte 1 %.** Masque de 25 % des connexions tiré à
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
