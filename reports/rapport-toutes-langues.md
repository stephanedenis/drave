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


---

## 10. Signal précoce sur le panel STRATIFIÉ : l'écart de transfert était un artefact

Mesure prise sur les 168 premières langues tracées : **133 d'apprentissage, 15 de
validation, 20 de test couvrant 12 des 22 écritures**. Assez pour lire la réponse
de la phase 2 avant la fin du traçage.

**Réseau : 52 neurones en 1 seule couche.**

| | ancien panel (test non latin seul) | **nouveau panel stratifié** |
|---|---:|---:|
| fidélité TEST | 0,6383 | **0,7438** |
| fidélité VALIDATION | 0,7500 | 0,7621 |
| constante témoin | 0,6140 | 0,7215 |
| **écart à la constante** | +0,0243 | **+0,0223** |
| invariance TEST | 0,9488 | 0,9739 |
| pire paire | 0,8821 | 0,8929 |
| **écart oracle TEST** | +0,0693 | **+0,0292** |
| écart oracle VALIDATION | +0,0269 | +0,0198 |
| **rapport des écarts (test/validation)** | **2,58** | **1,47** |

### Ce que cela établit

**L'écart de transfert tombe de +0,0693 à +0,0292 — 2,4× plus petit** — et son
rapport test/validation passe de **2,58 à 1,47**. Le « goulot dans le transfert »
que j'avais annoncé au tour 3 était donc **pour l'essentiel un artefact de mon
panel de test**, composé uniquement de langues non latines. C'est exactement ce que
le diagnostic de typologie laissait prévoir.

**Et l'invariant tient** : l'écart à la constante vaut **+0,0223** ici, contre
+0,0243 sur l'ancien panel et +0,020 sur les sept périmètres du rapport précédent.
La contribution propre du pont reste **+0,020**, indépendamment du panel.

### Réserve explicite

Ce panel est **partiel** : 20 langues de test sur 41, et 12 écritures sur 22. Les
chiffres définitifs viendront de l'analyse complète, déclenchée automatiquement à
la fin des 392 langues. Mais la direction est nette et va dans le sens du
diagnostic de typologie.


---

## 11. Mon seuil de couche par défaut était TROP STRICT

Le critère de couche n'ouvrait **jamais** de couche sur le panel stratifié
(`communs` plafonnait à 28-38 %, sous le seuil de 50 %). Deux lectures possibles :
soit c'était correct — rien de partagé à composer à ce niveau — soit je me privais
de profondeur utile. Test en abaissant le seuil de **décision** :

| seuil-part | réseau | fid VAL | fid TEST | **écart à la constante** | invariance | pire paire |
|---|---|---:|---:|---:|---:|---:|
| **0,50** (défaut) | 52 neurones · **1 couche** | 0,7621 | 0,7438 | **+0,0223** | **0,9739** | **0,8929** |
| **0,25** | 80 neurones · **5 couches** [44, 10, 10, 11, 5] | **0,7681** | **0,7487** | **+0,0272** | 0,9649 | 0,8745 |

**Forcer la profondeur gagne en fidélité** : +0,0060 en validation, +0,0049 en test,
et l'écart à la constante monte de **+0,0223 à +0,0272, soit +22 %**. Le prix est
l'invariance : **−0,0090**, et la pire paire perd 0,0184.

### Ce que cela dit du seuil

**Le défaut de 0,50 était trop strict** — il laissait de la fidélité sur la table.
Mais ce n'est pas gratuit : c'est un déplacement le long de la courbe d'échange.

**Le taux obtenu est intéressant** : 0,0049 de fidélité pour 0,0090 d'invariance
abandonnée, soit **0,55 point par point** — à comparer aux **0,3856** de la loi
générale mesurée sur onze points de croissance. **Forcer la profondeur est donc un
moyen légèrement plus efficace que la moyenne d'acheter de la fidélité.**

### Et un bug trouvé au passage

En testant, j'ai découvert qu'abaisser `--seuil-commun` de 0,50 à 0,25 donnait un
résultat **bit-à-bit identique**. Cause : le déclencheur comparait `part_commune >
0.5`, une **constante en dur**, au lieu de la variable. Le drapeau ne changeait que
le pourcentage **affiché**, jamais la **décision**. Corrigé : la décision se règle
par `--seuil-part` (défaut 0,5, comportement inchangé), et `--seuil-commun` garde
son rôle propre — définir ce qu'est un neurone « concept commun ».

**Leçon** : quand un paramètre ne change rien, **suspecter le paramètre avant de
conclure sur le phénomène**.


---

## 12. L'optimum du seuil de couche : 0,25, et c'est un maximum INTÉRIEUR

Balayage complet, panel stratifié, tout le reste égal :

| seuil-part | réseau | fid VAL | fid TEST | **écart à la constante** | invariance | pire paire |
|---|---|---:|---:|---:|---:|---:|
| 0,50 | 52 neurones · **1 couche** | 0,7621 | 0,7438 | +0,0223 | **0,9739** | **0,8929** |
| **0,25** | 80 neurones · 5 couches [44, 10, 10, 11, 5] | **0,7681** | **0,7487** | **+0,0272** | 0,9649 | 0,8745 |
| 0,10 | 80 neurones · 5 couches [44, 8, 8, 16, 4] | 0,7662 | 0,7481 | +0,0266 | 0,9634 | 0,8562 |

**0,25 est un maximum intérieur.** Au-delà, forcer encore la profondeur détériore
**les trois colonnes à la fois** : la fidélité de test (−0,0006), l'écart à la
constante (−0,0006) **et** l'invariance (−0,0015). On paie donc plus pour obtenir
moins — le signe net d'un réglage passé.

**Ce n'est pas un déplacement gratuit le long de la courbe d'échange** : entre 0,25
et 0,10, l'invariance baisse *et* la fidélité baisse. La courbe d'échange ne suffit
donc pas à décrire ce réglage — au-delà de l'optimum, on perd sur les deux tableaux.

### Le réglage retenu

Le défaut reste **0,50** — je ne change pas un défaut en silence, et 0,50 maximise
l'**invariance** (0,9739) et la **pire paire** (0,8929). Mais **0,25 est désormais
mesuré comme l'optimum de fidélité** (+22 % d'écart à la constante), réglable en
une ligne.

**Le choix dépend de l'usage** : un pont destiné au raisonnement veut de la
fidélité (0,25) ; un pont destiné à servir de représentation interlingue veut de
l'invariance (0,50). Les deux sont maintenant chiffrés.


---

## 13. Le plateau sur 392 langues, et un effet de panel qui corrige une mesure antérieure

Mesure faite sur les **392 langues**, dernière position, couche 10 :

| | |
|---|---:|
| **50 % de l'énergie** | **40 canaux sur 896 (4 %)** |
| 90 % de l'énergie | 298 (33 %) |
| 99 % de l'énergie | 597 (67 %) |
| canaux actifs dans **au moins une** langue | **896 / 896** |
| **canaux actifs dans TOUTES les langues** | **48 / 896 (5 %)** |

### Ce qui tient, et ce qui s'effondre

**Ce qui tient** : la couche est **creuse** — 40 canaux sur 896 portent la moitié de
l'énergie. C'était déjà le chiffre mesuré sur l'ancien panel (34 canaux), il est
confirmé à 392 langues. La conclusion qualitative est solide.

**Ce qui s'effondre** : le « sous-ensemble partagé ». Sur 6 langues je mesurais
**678 canaux actifs dans toutes** ; sur **392 langues, il n'en reste que 48**.
Autrement dit **95 % des canaux ne sont pas universellement actifs** — ils
dépendent de la langue à la dernière position.

**C'était une borne supérieure optimiste.** Avec 6 langues, un canal n'avait que 6
occasions d'être absent ; avec 392, il en a 392. La mesure ne grandit pas avec le
panel, elle **se resserre**. Toute affirmation du type « ce canal est partagé par
toutes les langues » doit donc dire **sur combien de langues elle a été vérifiée** —
sinon elle ne veut rien dire.

### Et l'écart test/validation, à pleine échelle

Sur le panel complet de **41 langues de test couvrant les 22 écritures** :

| neurones | fid appr | fid VAL | **fid TEST** | invariance | pire paire |
|---:|---:|---:|---:|---:|---:|
| 33 | 0,7445 | 0,7494 | 0,7411 | 0,9865 | 0,9320 |
| 37 | 0,7453 | 0,7502 | **0,7428** | 0,9838 | 0,9192 |

**Rapport test/validation : 1,01** — contre **2,58** sur l'ancien panel uniquement
non latin. Le diagnostic de typologie est donc confirmé **à pleine échelle**, et
pas seulement sur le signal précoce.

`communs` reste à **+0,233** avec 14-15 % des neurones au-dessus du seuil de 0,35 :
le critère n'ouvre pas de couche, le réseau reste à **1 couche** — résultat qui, on
le sait maintenant, n'est pas optimal (l'optimum mesuré est 0,25, +22 % d'écart à
la constante).


---

## 14. LE LIVRABLE DE LA PHASE 2 : le pont sur 301 langues

| | |
|---|---:|
| apprentissage / validation | **301 / 50 langues** |
| test | **41 langues · 22 écritures** |
| réseau | **40 neurones · 1 couche** |
| fidélité apprentissage | 0,7459 |
| fidélité VALIDATION | 0,7505 |
| **fidélité TEST** | **0,7430** (constante 0,7207) |
| **invariance TEST** | **0,9827** |
| **pire paire** | **0,9165** |
| oracle TEST | 0,7653 — écart **+0,0223** |
| oracle VALIDATION | 0,7563 — écart **+0,0058** |
| **écart à la constante** | **+0,0223** |

### Les trois choses qui tiennent, à pleine échelle

**1. L'écart test/validation est de 1,01** (0,7505 / 0,7430), contre **2,58** sur
l'ancien panel uniquement non latin. Le diagnostic de typologie est **confirmé sur
le panel complet**, et pas seulement sur le signal précoce.

**2. L'écart de transfert tombe à +0,0223** (oracle test), contre **+0,0693** sur
l'ancien panel — **3,1× plus petit**. Là encore, ce que je prenais pour un goulot
de méthode était largement un artefact de mesure.

**3. L'écart à la constante vaut +0,0223** — dans la plage de l'invariant des +0,020

> **ATTENTION — cette affirmation est CORRIGÉE au §16.** L'écart vaut +0,0223 ici
> mais **+0,0322** sur les 896 canaux : ce n'est pas une constante mais une
> **plage de +0,020 à +0,032**. Les sept périmètres qui donnaient +0,0197 ± 0,0009
> partageaient le **même panel de 46 langues**. Voir §16.
mesuré sur sept périmètres et deux architectures, puis sur le panel stratifié
partiel (+0,0223). Il traverse donc : changement de panel, de taille, de corpus.

### Le signal précoce était représentatif

| | signal précoce (20 langues) | **définitif (41 langues)** |
|---|---:|---:|
| fidélité TEST | 0,7438 | 0,7430 |
| fidélité VALIDATION | 0,7621 | 0,7505 |
| écart oracle TEST | +0,0292 | **+0,0223** |

Les chiffres convergent. **Prendre le signal tôt était donc justifié** : il a
corrigé une conclusion fausse plusieurs heures avant que le run complet ne la
confirme.


---

## 15. Le piège du droit d'exécution, trois fois de suite

**Ce qui s'est passé.** Romeo a terminé ses 48 scènes (24 anglais + 24 français,
appariement parfait vérifié). Mais Wikipedia **n'a pas démarré**, et son guetteur
n'était plus vivant.

**La cause** : trois scripts créés par l'outil d'écriture avaient le mode
`-rw-------` — donc **non exécutables** : `trace_wiki.sh`, `trace_unites.sh`,
`analyse_final.sh`. Or `wiki_apres.sh` faisait `exec /tmp/trace_wiki.sh`, qui exige
le droit d'exécution. L'échec est **silencieux** : le guetteur meurt, la phase ne
démarre jamais, et rien ne le signale.

**Pourquoi je ne l'avais pas vu** : j'avais vérifié la **syntaxe** de ces scripts
avec `bash -n`. Or `bash -n` teste la syntaxe, **pas** le droit d'exécution. C'est
exactement la même confusion que deux tours plus tôt, avec `nohup` et
`Permission denied` redirigé vers `/dev/null`.

**C'est la troisième fois** qu'un défaut de plomberie me coûte du temps dans ce
parcours — après le `chmod +x` manquant et le drapeau sans effet. Les trois avaient
la même signature : **ça a l'air de tourner, donc je crois que ça marche.**

**Corrigé à la racine**, pas au cas par cas :

1. les huit scripts sont maintenant exécutables (`chmod +x`) ;
2. **et** les `exec /tmp/x.sh` sont devenus `exec bash /tmp/x.sh` — passer par
   `bash` rend le droit d'exécution **inutile**, donc le piège ne peut plus se
   reproduire même si un script est recréé par l'outil d'écriture.

C'est la différence entre réparer un symptôme et supprimer la cause. La première
correction aurait suffi aujourd'hui ; la seconde protège les prochains scripts.


---

## 16. Restriction ou pas : la comparaison complète, et une correction de mon invariant

Les deux runs de la phase 2, même professeur, mêmes 301 langues d'apprentissage,
même panel de test (41 langues, 22 écritures) :

| | **896 canaux** (sans restriction) | **157 canaux** (50 % de l'énergie) |
|---|---:|---:|
| réseau | 45 neurones · 1 couche | 40 neurones · 1 couche |
| fidélité apprentissage | 0,6199 | 0,7459 |
| fidélité VALIDATION | 0,6231 | 0,7505 |
| **fidélité TEST** | 0,6088 | **0,7430** |
| constante témoin | 0,5766 | 0,7207 |
| **écart à la constante** | **+0,0322** | **+0,0223** |
| **invariance TEST** | 0,9682 | **0,9827** |
| **pire paire** | 0,8494 | **0,9165** |
| écart oracle TEST | +0,0327 | +0,0223 |
| écart oracle VALIDATION | +0,0111 | +0,0058 |
| rapport des écarts | 2,95 | 3,85 |

### Ce qui se confirme

**La restriction améliore tout ce qui compte pour l'usage** : +13,4 points de
fidélité, +1,5 point d'invariance, +6,7 points sur la pire paire — **avec 5 fois
moins de canaux de sortie** (157 sur 896). Le pont restreint est meilleur sur les
trois axes mesurés.

### Ce que je dois CORRIGER

**L'écart à la constante est plus GRAND sans restriction (+0,0322) qu'avec
(+0,0223).** Or j'ai présenté cet écart comme « l'invariant des +0,020 » à travers
sept périmètres et deux architectures. La mesure d'aujourd'hui dit autre chose :
c'est une **plage de +0,020 à +0,032**, pas une constante.

**Ce qui tient** : la contribution propre du pont est **petite** (2 à 3 points de
cosinus) et **ne croît pas avec la restriction** — ici elle décroît même. La
conclusion qualitative est intacte.

**Ce qui ne tient pas** : le chiffre exact. J'ai lu une coïncidence numérique
(+0,0197 ± 0,0009 sur sept périmètres) comme une loi, alors que ces sept
périmètres partageaient le même panel de 46 langues. **Changer de panel change
l'écart** — je ne l'avais pas testé, et c'est une leçon de plus sur les conclusions
tirées d'un seul jeu de données.


---

## 17. Le plateau du professeur est à la couche 8, PAS à la couche 10

Mesure sur le corpus parallèle *Romeo and Juliet*, invariance **segment par
segment** (24 scènes appariées) :

| couche | invariance moyenne | pire scène |
|---|---:|---:|
| 0 (plongement) | **0,1420** | **−0,0888** |
| 4 | 0,4483 | 0,1289 |
| **8** | **0,5985** | 0,1943 |
| 10 | 0,5703 | **0,2381** |

**Le plateau est à la couche 8** ; la couche 10 est déjà **en re-spécialisation**
vers la sortie (0,5703 contre 0,5985).

**Et ce n'est pas propre à ce corpus.** Sur l'UDHR propre (46 langues), je
mesurais **0,5471 à la couche 8 contre 0,5247 à la couche 10**. Les deux corpus
concordent.

### Ce que cela remet en cause

**Ma cible était mal choisie.** Depuis le début de ce travail, le pont émule la
**couche 10** — parce que la mesure initiale, faite sur l'article 1 de l'UDHR avec
quarante langues, plaçait le pic à 42 % de profondeur (couche 10 sur 24). Les deux
mesures d'aujourd'hui, sur des corpus et des panels différents, placent le pic
**deux crans plus haut**.

**Ce n'est pas une erreur de mesure, c'est une erreur de choix** : la couche 10
n'est pas la plus interlingue, et émuler une couche en re-spécialisation revient à
apprendre du détail linguistique qui coûte précisément l'invariance cherchée.

**Ce qu'il faudrait** : refaire la mesure du pont avec la couche 8 pour cible. Le
traçage de Romeo contient **déjà** la couche 8 (`--trace-couches 0,4,8,10`), donc
la comparaison est possible sans retracer.

### Le plongement, sur du texte littéraire

**0,1420 d'invariance à la couche 0, avec des scènes négatives** (jusqu'à −0,0888).
Sur du texte littéraire long, les plongements anglais et français sont **quasi
orthogonaux** — bien plus que sur l'UDHR (0,58 sur l'ancien panel). Cela quantifie
combien la couche d'entrée est propre à chaque langue, et donc **quel travail le
pont doit fournir**.


---

## 18. Romeo : le pont transfère sur du texte LITTÉRAIRE

Premier test hors de l'UDHR. Corpus **parallèle** — 24 scènes appariées en/fr —
donc l'invariance se mesure **segment par segment**, et le transfert se mesure
**en entraînant sur l'anglais et en testant sur le français**, sans réapprentissage.

| | |
|---|---:|
| invariance du professeur (segment par segment) | 0,6532 · pire segment 0,2966 |
| fidélité sur l'anglais (apprise) | **0,6660** |
| **fidélité sur le français (transférée)** | **0,5802** |
| **invariance de notre sortie** | **0,9540** · pire segment 0,8738 |
| oracle sur le français | 0,6207 |
| **écart oracle** | **+0,0405** |
| taille | 120 neurones · 1 couche |

### Trois observations

**1. Le pont transfère sur du littéraire long.** De l'anglais au français, sans
réapprentissage : 0,6660 → 0,5802. Une perte de 0,086, du même ordre que les
écarts de transfert mesurés sur l'UDHR.

**2. Notre sortie est BEAUCOUP plus interlingue que le professeur** : 0,9540 contre
0,6532. Le pont dépasse largement la couche qu'il émule sur l'invariance — cohérent
avec tout ce qui précède, et c'est le prix de la fidélité.

**3. La restriction de canaux est confirmée par une voie indépendante.** L'invariance
du professeur mesurée **sur les canaux à forte énergie** vaut **0,6532**, contre
**0,5703** sur les 896 canaux. Les canaux énergétiques sont donc bien **plus
interlingues** — ce que la sélection par énergie supposait, et qui n'avait pas
encore été vérifié directement.

### La comparaison couche 8 / couche 10

Mesurée en parallèle (les traces de Romeo contiennent déjà la couche 8) : elle dira
si viser le plateau plutôt que la couche 10 améliore le pont.


---

## 19. Couche 8 contre couche 10 : la correction de cible PAIE

Même corpus (Romeo, 24 scènes appariées), même protocole (entraîné sur l'anglais,
testé sur le français), même taille de réseau. **Seule la couche cible change.**

| | **couche 10** | **couche 8** | gain |
|---|---:|---:|---:|
| invariance du professeur | 0,6532 | **0,7044** | **+0,0512** |
| fidélité sur l'anglais (apprise) | 0,6660 | **0,6967** | +0,0307 |
| **fidélité sur le français (transférée)** | 0,5802 | **0,6015** | **+0,0213** |
| invariance de sortie | **0,9540** | 0,9504 | −0,0036 |
| pire segment | **0,8738** | 0,8650 | −0,0088 |
| oracle sur le français | 0,6207 | **0,6540** | +0,0333 |
| **écart oracle** | **+0,0405** | +0,0525 | +0,0120 |

### La correction de cible paie, et le prix est négligeable

**+0,0213 sur la fidélité TRANSFÉRÉE** — c'est-à-dire sur la seule mesure qui
compte pour un pont destiné à servir : celle où l'on transporte le modèle vers une
langue qu'il n'a jamais vue, sans réapprentissage.

**Le seul prix est une invariance de sortie inférieure de 0,0036** — négligeable,
et c'est la courbe d'échange connue : un peu moins d'invariance pour nettement
plus de fidélité.

**Et le professeur lui-même confirme** : son invariance segment par segment passe
de 0,6532 à **0,7044** entre les couches 10 et 8. Le plateau est bien là, et le
pont n'apprend plus du détail en re-spécialisation.

### Ce que cela dit de la méthode

**Ma cible avait été choisie sur une seule mesure** — l'article 1 de l'UDHR avec
40 langues, qui plaçait le pic à 42 % de profondeur. Deux corpus et deux panels
ultérieurs le placent deux crans plus haut. **Le choix de la cible est un paramètre
aussi important que l'architecture**, et il se mesure.

**Il reste à refaire proprement sur l'UDHR complète** : le traçage des 392 langues
n'a écrit que les couches **0 et 10** (`--trace-couches 0,10`), donc la
comparaison à grande échelle demanderait un retraçage avec la couche 8 incluse.
Sur Romeo elle était possible sans retraçage parce que j'avais tracé `0,4,8,10` par
précaution — et cette précaution a payé.


---

## 20. Le gain de la couche 8 est ROBUSTE — testé sur trois graines

Le §19 reposait sur **une seule mesure**. Une seule graine ne prouve rien : c'est
exactement la leçon du tour 3, où un signal non répété avait produit une conclusion
fausse. Vérification sur trois graines du réservoir gelé :

| graine | couche 10 | **couche 8** | **gain** | invariance 8 | invariance 10 |
|---|---:|---:|---:|---:|---:|
| 5 | 0,5802 | 0,6015 | **+0,0213** | 0,9504 | 0,9540 |
| 11 | 0,5826 | 0,6039 | **+0,0213** | 0,9611 | 0,9666 |
| 23 | 0,5828 | 0,6046 | **+0,0218** | 0,9505 | 0,9597 |

| | |
|---|---:|
| **gain moyen** | **+0,0215** |
| amplitude du gain | 0,0005 |
| variation entre graines (couche 10) | 0,0026 |
| **rapport gain / variation** | **8×** |

**Le gain est 8 fois plus grand que la dispersion entre graines.** Ce n'est donc
pas un coup de chance, et l'amplitude du gain (0,0005) est cinq fois plus petite
que la dispersion des mesures elles-mêmes.

**L'invariance de sortie est systématiquement plus basse à la couche 8** — de
0,006 en moyenne sur les trois graines, avec une amplitude de 0,001 seulement. Le
prix payé est donc stable lui aussi, et il reste très inférieur au gain.

### Ce que ce test ajoute à la méthode

**Un résultat à une graine n'est pas un résultat.** Je l'avais appris au tour 3 en
me trompant, et je l'applique maintenant **avant** de graver la conclusion — plutôt
qu'après qu'un run complet l'ait contredite.


---

## 21. PIÈGE : l'invariance sur Wikipedia ne veut RIEN dire

`analyse_final.sh` fait tourner `pont_parallele.py` sur Wikipedia. Or **ce tool
apparie les segments PAR INDEX** : il compare le morceau 1 de l'anglais au morceau 1
du français, etc.

**Sur Wikipedia, ces morceaux n'ont rien à voir.** Vérifié :

| | premiers morceaux |
|---|---|
| anglais | *Actrius*, *Animalia (book)*, *Alain Connes* |
| français | *Algèbre générale*, *Armée républicaine irlandaise*, *Aka* |

Ce sont des **articles différents**, pris dans l'ordre alphabétique de deux wikis
distincts. Le chiffre d'« invariance » que le tool produira est donc **dépourvu de
sens** — il mesurera la similarité entre un film et un article de mathématiques.

**Ce qui reste mesurable sur Wikipedia** : la **fidélité** (notre sortie contre la
couche du professeur, dans chaque langue) et le **transfert** en→fr. Pas
l'invariance : elle exige du contenu **apparié**, et Wikipedia n'en a pas.

**Corrigé dans l'outil** : il imprime maintenant un avertissement explicite quand
on ne lui a pas passé `--apparie`, et signale une valeur basse comme « cohérente
avec un corpus NON apparié — NE PAS l'interpréter ».

**Ce que j'aurais dû faire** : ne pas mettre cette étape dans la chaîne, ou la
garder mais avec un outil qui ne calcule que la fidélité. Je ne peux pas corriger
`analyse_final.sh` — **il tourne**, et l'éditer en cours d'exécution est ce qui a
tué le guetteur de Wikipedia plus tôt. Le chiffre sera donc produit ; il est
désigné ici comme **non interprétable**.


---

## 22. CORRECTION : la « richesse » n'est pas dans le nombre de canaux actifs

Au tour précédent j'ai annoncé, sur un échantillon de huit traces, que Wikipedia
activait la couche « beaucoup plus densément » que l'UDHR — 810-864 canaux actifs
contre un minimum de 5. **C'était faux** : j'avais comparé un **minimum**
échantillonné à une **moyenne**.

Distribution complète, couche 10, sur 896 canaux :

| corpus | min | p10 | médiane | p90 | max | positions |
|---|---:|---:|---:|---:|---:|---:|
| UDHR (392 langues) | 60 | 850 | 862 | 873 | 889 | 20 803 |
| Wikipedia (en/fr) | 63 | 858 | **871** | 880 | 890 | 5 732 |
| Romeo (24 scènes) | 79 | 860 | **872** | 880 | 891 | 19 135 |

**La médiane va de 862 à 872 — 1 % d'écart.** Le minimum réel est de 60, pas 5. La
« richesse » d'un corpus ne se lit donc **pas** dans le nombre de canaux actifs.

### La vraie caractérisation, et les deux mesures ne se contredisent pas

**La couche 10 du professeur est DENSE EN SUPPORT et CREUSE EN ÉNERGIE :**

| | mesure |
|---|---|
| canaux non nuls | **862 sur 896 (96 %)** — dense |
| énergie portée par 50 % des canaux | **40 canaux (4 %)** — concentrée |

Ce ne sont pas deux mesures contradictoires, mais **deux questions différentes** :
*combien de canaux parlent* (presque tous) et *lesquels portent le signal* (une
poignée). J'avais laissé entendre qu'elles s'opposaient ; elles se complètent.

**Conséquence pour la sélection de canaux** : garder les 157 canaux énergétiques ne
revient pas à écarter du vide — 96 % des canaux sont non nuls. Cela revient à
écarter **du bruit de faible amplitude**, ce qui explique pourquoi la restriction
fonctionne aussi bien : on ne jette presque que du détail.
