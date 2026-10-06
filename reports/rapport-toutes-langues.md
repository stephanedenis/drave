# Extension à toutes les langues, puis aux grands corpus

Objectif : passer de **46 langues** à **toutes celles disponibles**, puis aux grands
corpus multilingues pour obtenir des professeurs plus riches.

Professeur unique : **Qwen2.5-0.5B, couche 10**. Boîte noire : on ne lit de lui que
la couche à émuler. Aucune rétropropagation : `A` et `B` aléatoires et gelés, seule
la lecture s'ajuste en forme fermée.

---

## 1. Le périmètre, inventorié

| corpus | contenu | parallèle ? |
|---|---|---|
| **UDHR** | **392 langues × 10 unités** | **oui**, aligné |
| Wikipedia | 81 Go, 6 langues, 65 589 fichiers de 150 articles | **non** |
| Gutenberg | 40 œuvres, 6,6 M mots | **3 paires** : Dostoïevski en/es, Dumas en/fr, Shakespeare en/fr |

**Wikipedia n'est pas parallèle, et c'est vérifié** : sur 400 articles par langue
dans six langues, **aucun titre commun** — les dumps sont triés par titre et chaque
langue commence ailleurs. L'alignement par titre ne donnerait qu'une poignée de
noms propres. D'où la division assumée :

- **richesse** (fidélité, transfert) → UDHR complet, Romeo, Wikipedia ;
- **invariance** (contenu apparié) → UDHR, Romeo.

---

## 2. La convention de traçage, unique et vérifiée

```
--ctx 4096 · --couches 0:11 · --lot 1 · --n 0 · --trace-couches 0,10
```

- `--n 0` : ni la tête du professeur, ni les jetons qu'il génère. Le défaut de drave
  est `n = 32`, ce qui mettait **32 jetons inventés dans la trace**.
- `--trace-couches 0,10` : on n'écrit que l'entrée et la cible. Vérifié
  **bit-identique** au traçage complet, et **11× plus petit**.
- `--ctx 4096` : **11 % des langues étaient tronquées** à `ctx 2048` (16 sur 143 :
  ame ben blt boa bod ccp chr cpu csw div dzo **ell** fuf guj **hin**). Vérifié
  avant d'agir : `--ctx` ne change **rien** au calcul quand le texte tient — deux
  traces du même texte à 2048 et 4096 sont **bit-à-bit identiques**. Seul le
  contexte d'allocation change, donc le surcoût est nul.

**Pourquoi la troncature est grave** : sur un texte coupé, la « dernière position »
n'est plus la fin du texte, donc l'invariance inter-langue compare des **contenus
différents**. C'est un biais **silencieux** qui frappe exactement la métrique
mesurée.

---

## 3. Le découpage : stratifié par écriture, déduit du texte

`tools/decoupe_langues.py` déduit l'écriture des **points de code** du texte
lui-même — pas un choix à la main, donc reproductible et vérifiable.

**22 écritures trouvées, toutes représentées dans le TEST.**

| | langues |
|---|---:|
| **TEST** | **41** (les 22 écritures) |
| VALIDATION | 50 |
| APPRENTISSAGE | **301** |

C'est la réponse directe au biais découvert précédemment : un test **uniquement non
latin** mesurait surtout la **distance typologique**. L'écart de transfert s'était
révélé **2,6× plus grand** sur le test que sur la validation, et cette différence
était entièrement attribuable à l'écriture et à la famille linguistique.

---

## 4. Les cinq phases, chaînées

| # | phase | contenu | état |
|---|---|---|---|
| 1 | **392 langues UDHR** | 10 unités chacune, convention ci-dessus | en cours |
| 2 | analyse 392 | caches, plateau, pont sur **301 langues** | attend 1 |
| 3 | **Romeo and Juliet** | 24 scènes alignées en/fr, corpus **parallèle** riche | attend 1 |
| 4 | **Wikipedia** | en/fr, 240 morceaux de ~3 000 car. | attend 3 |
| 5 | **traçage par unité** | 40 langues × 10 unités séparées | attend 4 |
| 6 | analyse finale | Romeo + Wikipedia + invariance par unité | attend 5 |

**La question à laquelle la phase 2 répond** : passer de 30 à **301 langues**
d'apprentissage change-t-il quelque chose ? Je n'avais pu mesurer l'effet que de
**20 à 36 langues, où il était nul**.

---

## 5. Mesure : l'invariance à dix points

Faiblesse corrigée en route : l'invariance ne tenait qu'à **un seul point de
contenu** par langue — la dernière position. Or l'UDHR a **dix unités alignées**.
En traçant chaque unité séparément, on obtient **dix points de mesure appariés**,
et la « pire paire » cesse d'être un agrégat pour porter sur une **unité précise et
un couple de langues nommable**.

Outils : `invariance_unites.py` (côté professeur), `pont_unites.py` (notre sortie
contre le professeur), `pont_parallele.py` (corpus apparié, segment par segment).

---

## 6. Deux erreurs de méthode, et ce qu'elles ont coûté

**Un « gain de 1,33× » qui n'existait pas.** J'avais lancé un second traçage en
parallèle et mesuré 28,6 s par langue au lieu de 38. En réalité ce second traçage
**n'avait jamais tourné** : `bash -n` vérifie la syntaxe, pas le droit d'exécution,
et `nohup` échouait sur `Permission denied` avec la sortie redirigée vers
`/dev/null`. Le rythme était simplement revenu à la normale après la fin d'une
contention. **Mesuré après correction** : deux traçages = **50 s par langue**, un
seul = **28 s**. La charge montait à 44 sur 40 threads — drave occupe déjà les cœurs
physiques. **Un traçage à la fois est l'optimum sur cette machine.**

**Un guetteur qui aurait attendu indéfiniment.** En modifiant les scripts d'attente
pour exiger la fin des deux traçages, puis en arrêtant le second, je les aurais
bloqués pour toujours. Réparé et vérifié.


---

## 7. Signal précoce : PLUS DE LANGUES AIDENT

Mesure prise sur les 133 premières langues tracées, **avant** la fin du traçage —
pour ne pas attendre deux heures si la réponse était déjà lisible. Même validation
(12 langues), même test (9 langues), **seul le nombre de langues d'apprentissage
change**.

| | **30 langues** | **112 langues** | gain |
|---|---:|---:|---:|
| fidélité TEST | 0,7029 | **0,7105** | **+0,0076** |
| fidélité VALIDATION | 0,7450 | **0,7478** | +0,0028 |
| invariance TEST | 0,9787 | **0,9809** | +0,0022 |
| pire paire | 0,9267 | **0,9309** | +0,0042 |
| écart oracle TEST | +0,0347 | **+0,0299** | −0,0048 |
| écart oracle VALIDATION | +0,0240 | +0,0231 | −0,0009 |
| constante témoin | 0,6907 | 0,6955 | +0,0048 |
| **écart à la constante** | **+0,0122** | **+0,0150** | **+23 %** |

**Cela contredit ma mesure antérieure.** Sur la plage 20 → 30 → 36 langues, l'effet
était **nul**, et j'en avais conclu que le nombre de langues ne comptait pas. À
112 langues, l'avantage sur la constante progresse de **23 %**.

**L'effet existe donc, mais il n'apparaît qu'à plus grande échelle** : entre 20 et
36 langues il est sous le bruit, à 112 il devient visible.

**Réserve à ne pas oublier** : le test ne compte que **9 langues** à ce stade (41
quand tout sera tracé). Le gain de +0,0076 porte donc sur un panel mince, et c'est
l'**écart à la constante** — qui corrige la difficulté du panel — qu'il faut
regarder : **+0,0122 → +0,0150**.

Un détail structurel au passage : la naissance libre trouve ici **40 neurones en
1 SEULE couche** dans les deux cas, là où le panel à 46 langues donnait
[30, 8, 8, 8, 8, 8, 8, 2]. La hiérarchie dépend donc bien des données.


---

## 8. La courbe de dose complète : elle NE sature PAS

Troisième point ajouté (60 langues, sous-ensemble strict de la dose 112 — même
graine). Même validation, même test, seul le nombre de langues d'apprentissage
change.

| langues | fid TEST | constante | **écart à la constante** | écart oracle TEST | écart oracle VAL |
|---:|---:|---:|---:|---:|---:|
| 30 | 0,7029 | 0,6907 | **+0,0122** | +0,0347 | +0,0240 |
| 60 | 0,7058 | 0,6928 | **+0,0130** | +0,0343 | +0,0237 |
| 112 | 0,7105 | 0,6955 | **+0,0150** | +0,0299 | +0,0231 |

### Ce que la courbe dit

**Le gain marginal par langue AUGMENTE au lieu de diminuer** :
2,7·10⁻⁵ par langue de 30 à 60, puis **3,8·10⁻⁵** de 60 à 112. Une courbe qui
sature ferait l'inverse. **Pousser jusqu'à 392 langues devrait donc continuer de
payer** — ce qui justifie la phase en cours.

**Et l'écart de transfert se réduit régulièrement** : oracle TEST +0,0347 → +0,0343
→ **+0,0299**, oracle VALIDATION +0,0240 → +0,0237 → +0,0231. Plus de langues
réduisent donc aussi la distance entre ce que nos caractéristiques contiennent et
ce que la lecture en extrait.

**Ce que cela corrige** : j'avais conclu, sur la plage 20-30-36 langues, que le
nombre de langues **ne comptait pas**. C'était vrai *dans cette plage* — l'effet y
est sous le bruit — et faux au-delà. Une conclusion tirée d'une plage trop étroite
ne vaut que pour cette plage.

### Réserve, toujours la même

Le test ne compte que **9 langues** à ce stade (41 quand les 392 seront tracées).
C'est pourquoi l'**écart à la constante** est le chiffre à regarder : il corrige la
difficulté du panel, qui varie d'une dose à l'autre (la constante passe de 0,6907
à 0,6955 sans que le modèle change).


---

## 9. Dimensionnement de l'analyse finale, mesuré

Avant de laisser tourner, j'ai chiffré ce que coûtera l'analyse sur les **351
langues** d'apprentissage (301 + 50), au lieu de le découvrir à 3 h du matin.

| | |
|---|---:|
| cache attendu | **~437 000 positions** · ~919 Mo |
| mémoire du readout quadratique (120 neurones → 240 colonnes) | 419 Mo |
| disque libre / RAM disponible | 2,1 To / 108 Go |

**Le coût dominant est la régression**, mesuré sur des matrices à l'échelle :

| taille de X | `XᵀX + XᵀY` |
|---|---:|
| 154 307 × 120 | 4,5 s |
| 436 788 × 120 | 11,4 s |
| **436 788 × 240** (readout quadratique) | **22,0 s** |

Soit **~22 s par neurone** — et 35 min à 1,7 h par run selon que la naissance
s'arrête à 40 ou à 120 neurones. L'analyse en fait deux.

**Décision : on n'optimise pas.** Il serait facile de rendre cette étape 20× plus
rapide en maintenant la Gram `XᵀX` de façon incrémentale — ajouter UN neurone ne
change qu'une ligne et une colonne. Mais la chaîne est **validée de bout en bout**,
et le temps n'est pas le facteur limitant : la phase 1 ne finit pas avant 02h30 de
toute façon. Toucher à un pipeline vérifié pour gagner une heure qu'on n'attend pas
serait un mauvais échange. Le chiffre est consigné pour que la décision soit
réexaminable si le volume change.
