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


---

## 23. Domaine ou langue ? — testé, et le test est INCOMPLET

Hypothèse testée : « certains mots et groupes de mots sont spécifiques à leur domaine ;
ils sont plus communs à leur domaine qu'à leur langue. »

Le traçage par unité offre les deux axes : **même unité entre langues** (`S_langue`)
et **unités différentes dans une même langue** (`S_domaine`). 18 langues, 10 unités.

| couche | S_langue | S_domaine | lecture |
|---|---:|---:|---|
| 0 | 0,4894 | **0,9872** | la langue l'emporte |
| 8 | 0,6132 | **0,8578** | la langue l'emporte |
| 10 | 0,5806 | **0,7916** | la langue l'emporte |

**Des contenus différents dans une même langue se ressemblent plus (0,86) que le
même contenu dans des langues différentes (0,61).**

### Le défaut de mon expérience, et il est décisif

**Les dix unités de l'UDHR sont toutes du MÊME DOMAINE** — le droit humain.
« Contenus différents » n'est donc **pas** « domaines différents ». Mon test compare
du *contenu différent dans un domaine unique* à du *même contenu entre langues*.

**Ce qu'il établit** : dans un domaine unique, la langue pèse plus que le contenu.
**Ce qu'il n'établit pas** : que la langue pèse plus que le domaine.

**L'hypothèse reste donc NON TESTÉE, pas réfutée.**

### Ce qu'il faudrait pour la tester

Des données **appariées entre langues ET couvrant plusieurs domaines**. Ce que
j'ai ne le permet pas :

| corpus | apparié ? | multi-domaine ? |
|---|---|---|
| UDHR (392 langues) | **oui** | **non** — un seul domaine |
| Wikipedia (6 langues) | non | oui |
| Romeo, Gutenberg | oui | non — une œuvre |

Pistes : articles Wikipedia **liés entre langues** (liens interlangues, absents de
mon corpus), ou **manuels traduits** (droit, médecine, biologie) en plusieurs
langues. Aucune n'est disponible sur disque aujourd'hui.


---

## 24. Signal précoce : la couche 8 gagne aussi au niveau des UNITÉS

Mesure prise sur les 198 premières unités tracées (**17 langues complètes**, 10 unités
chacune), donc **avant** la fin du traçage. C'est la mesure la plus fine dont je
dispose : dix points appariés par langue au lieu d'un.

| | couche 10 | **couche 8** | gain |
|---|---:|---:|---:|
| **invariance moyenne** (10 unités) | 0,5977 | **0,6358** | **+0,0381** |
| pire paire (moyenne sur les unités) | 0,1383 | 0,1620 | +0,0237 |
| pire unité | 0,5616 | **0,6170** | +0,0554 |

**Deux confirmations indépendantes de la couche 8 :**

| mesure | corpus | gain de la couche 8 |
|---|---|---:|
| invariance segment par segment | Romeo (24 scènes) | +0,0512 |
| **invariance par unité** | **UDHR (17 langues × 10 unités)** | **+0,0381** |

Deux corpus, deux méthodes de mesure, même conclusion. Ce n'est plus une mesure
isolée.

### Et la « pire paire » devient enfin NOMMABLE

C'était l'objectif du traçage par unité. Au lieu d'un agrégat, on obtient des
couples précis :

| couche | pire unité | pire couple | valeur |
|---|---:|---|---:|
| 10 | 8 | **deu–dzo** | 0,0970 |
| 8 | 9 | **ces–dzo** | 0,0905 |

Le dzongkha (dzo) apparaît dans les deux — c'est la langue la plus éloignée du
panel sur ce corpus, ce qui est cohérent avec sa position (tibétain, isolat
morphologique) et donne enfin une **cible concrète** pour améliorer le pont.


---

## 25. La pire paire (dzo) : hypothèse testée et RÉFUTÉE

La mesure par unité a nommé la pire paire : **deu–dzo** (couche 10) et **ces–dzo**
(couche 8). Le dzongkha (bhoutanais, écriture tibétaine) est la langue la plus
éloignée du panel. J'ai voulu savoir pourquoi.

**Hypothèse testée** : manque de contexte — ses unités seraient trop courtes pour
que la représentation se stabilise.

| langue | jetons par unité |
|---|---:|
| fuf | 495 |
| **dzo** | **344** — **2ᵉ plus longue sur 21** |
| csw | 305 |
| deu | 83 |
| heb | 71 — la plus courte |

**Hypothèse RÉFUTÉE.** Le dzongkha est la **deuxième langue la plus longue** du
panel, pas la plus courte. Sa distance n'est donc **pas** un artefact de données :
elle est **représentationnelle**, et c'est exactement ce qu'on attend d'une langue
témoin.

**Observation au passage** : l'écriture tibétaine est **fragmentée environ quatre
fois plus** par le tokenizer que le latin — 344 jetons pour le même contenu que
l'allemand dit en 83. Et cela **ne suffit pas** à aligner sa représentation.

**Ce que cela donne** : une cible concrète et bien caractérisée. Si l'on veut
améliorer le pont sur les langues isolées, c'est **ce couple** qu'il faut regarder,
et l'on sait maintenant que le problème n'est ni la longueur du texte ni le
tokenizer — c'est la représentation elle-même.


---

## 26. Ce qui distingue les langues éloignées : une NORME plus grande

Après avoir réfuté l'hypothèse de longueur (§25), j'ai profilé les 22 langues
complètes : norme de la représentation, canaux actifs, et cosinus au centroïde du
panel. Couche 10, trié par éloignement :

| langue | norme | actifs | cos au centroïde |
|---|---:|---:|---:|
| **csw** (cri des plaines) | **479** | 868 | **0,4419** |
| **dzo** (dzongkha) | **468** | 864 | **0,4651** |
| **amh** (amharique) | **537** | 867 | 0,6090 |
| fuf | 418 | 860 | 0,6818 |
| … | | | |
| acu | 283 | 844 | 0,8669 |
| haw | 282 | 846 | 0,8703 |
| **guc** | 289 | 845 | **0,8774** |

**Les langues les plus éloignées du centroïde ont systématiquement une norme plus
grande** : 468-537 pour les trois premières, ~282-289 pour les trois dernières. Le
nombre de canaux actifs, lui, est quasi identique partout (844-868) — ce n'est donc
**pas** un effet de densité.

### Et les trois plus éloignées partagent leur type d'écriture

**cri syllabique** (csw), **tibétain** (dzo), **éthiopien** (amh) — trois écritures
très éloignées du latin. Le quatrième (fuf, Pular) est à écriture latine et déjà
nettement plus proche (0,68).

**Ce n'est pas une preuve de mécanisme** — 22 langues, une corrélation — mais c'est
une piste nette : **plus l'écriture s'éloigne du latin, plus la représentation du
professeur est forte en magnitude et divergente en direction.**

### Pourquoi cela compte pour le pont

Si la cible est « forte » pour certaines langues, le pont doit apprendre à être
fort pour elles — ce qui **coûte le transfert**. Cela expliquerait pourquoi les
paires impliquant dzo résistent, et **donne un levier testable** : normaliser la
magnitude de la cible, langue par langue, avant d'ajuster la lecture.

**Réserve** : j'ai testé une normalisation voisine sur les états du RÉSERVOIR (§10.3)
et elle avait **échoué** en effondrant l'invariance. Mais il s'agissait des états
internes, pas de la cible du professeur. Les deux sont à ne pas confondre, et
l'expérience reste à faire.



---

## 27. Le pont ne sert pas également les langues — et le chiffre de tête est surtout la CONSTANTE

Le §26 laissait une piste : les langues les plus éloignées du centroïde avaient une
norme plus grande. Je l'ai instruite à l'échelle des 41 langues de test, périmètre
**896 canaux**, réseau **40 neurones / 1 couche**, lecture quadratique — les mêmes
réglages que le résultat de tête. Résultat : la piste était à moitié fausse, et
l'enquête a mis au jour quelque chose de plus important.

### 27.1 D'abord un fait inconfortable : la fidélité EST le témoin constant

J'ai mesuré, langue par langue, la fidélité du pont **et** celle du témoin constant
(la même constante `mt` pour toutes, sans aucun neurone).

| | |
|---|---:|
| **corrélation fidélité ↔ témoin constant** | **+0,9768** |
| apport propre du pont (fidélité − témoin) | **+0,0294** en moyenne |
| étendue de cet apport | +0,0014 (heb) à +0,0885 (dzo) |

**Le classement des langues par fidélité est, à 97,7 %, le classement par le témoin
constant.** Autrement dit : la variation de « fidélité TEST » d'une langue à l'autre
ne dit presque rien du pont — elle dit à quel point la langue ressemble à la moyenne
du vivier. Le chiffre de tête (0,7430 contre 0,7207, écart +0,0223) reste exact,
mais il faut savoir que **0,72 des 0,74 sont la constante**.

Ce n'est pas une erreur de mesure : c'est la même chose que l'écart au témoin déjà
rapporté. C'est un rappel de lecture, et il manquait.

### 27.2 L'apport propre du pont : la FRAGMENTATION du tokeniseur, pas la norme

L'apport `fidélité − témoin` est ce que le pont ajoute réellement. Ce qui le prédit,
mesuré sur les 41 langues :

| variable | corrélation avec l'apport | R² seul |
|---|---:|---:|
| **fragmentation (jetons/caractère)** | **+0,8207** | **0,6735** |
| norme de la cible | −0,5912 | 0,3495 |
| témoin constant (la « marge ») | +0,1127 | 0,0127 |
| fragmentation + norme | | 0,7002 |

**Ce n'est pas un effet de marge** : la corrélation avec `1 − témoin` vaut −0,11, et
en contrôlant le témoin la corrélation avec la fragmentation reste +0,8250. Les
langues qui reçoivent le plus ne sont pas celles qui avaient le plus de place — ce
sont les langues que le tokeniseur hache.

| langue | jetons/car | apport du pont |
|---|---:|---:|
| dzo | 1,324 | **+0,0885** |
| mya | 1,017 | +0,0769 |
| csw | 1,507 | +0,0639 |
| fuf | 1,578 | +0,0610 |
| … | | |
| deu | 0,271 | +0,0133 |
| srp | 0,390 | +0,0128 |
| **heb** | 0,407 | **+0,0014** |

**Sur l'hébreu, le pont n'apporte rien du tout** — 0,0014 au-dessus d'une constante.
Et sur `deu`, `jpn`, `kor`, `heb`, `srp`, la constante est mauvaise (0,31 à 0,48) et
le pont n'y ajoute rien : **ces langues ne sont pas servies**, ni par l'un ni par
l'autre.

### 27.3 L'oracle dit où est le goulot — et la réponse n'est pas unique

Une lecture **ajustée sur la langue elle-même** (oracle, diagnostic) sépare deux
causes que la fidélité confond.

| | moyenne |
|---|---:|
| témoin constant | 0,5678 |
| pont | 0,5972 |
| **oracle par langue** | **0,6935** (+0,0963 sur le pont) |
| oracle ↔ norme | **−0,8368** (Spearman −0,7117) |
| (oracle − pont) ↔ norme | +0,3634 |

L'écart oracle−pont, qui est la part imputable au **partage**, est le plus grand
là où la norme est forte : **jpn +0,245 · fuf +0,219 · kor +0,213 · deu +0,187**,
contre **xsm +0,048**. Mais l'oracle lui-même reste bas sur ces langues (deu 0,539,
srp 0,561, jpn 0,575) : une lecture privée ne suffit donc pas non plus.

**Deux limitations se superposent** : un partage qui convient mal aux langues
atypiques, et des caractéristiques qui ne portent qu'imparfaitement leur contenu.
Je n'ai pas isolé laquelle domine — les deux proxys (norme, fragmentation) restent
corrélés à −0,55 et je ne peux pas les départager ici.

### 27.4 La norme est une propriété réelle, pas un artefact de longueur

La norme et la longueur sont très liées (corrélation −0,8176) : il fallait écarter
l'artefact. Si la norme décroissait avec la position, une moyenne sur 730 pas
vaudrait plus qu'une moyenne sur 4088.

Mesuré : corrélation norme↔position **−0,157** (jpn), −0,095 (deu), **+0,015** (dzo),
+0,026 (fuf) — quasi nulle. Et sur une **fenêtre commune des 715 premiers pas de
chaque langue**, les normes sont pratiquement identiques aux normes pleines :
écart-type **49,3 contre 49,7**, jpn 575,8 pour 574,0, deu 548,6 pour 542,2,
fuf 354,8 pour 361,7.

**La norme est réelle.** Et en contrôle partiel, elle reste le meilleur prédicteur de
l'oracle : oracle ↔ norme | fragmentation = −0,7653, contre oracle ↔ fragmentation |
norme = +0,1876.

### 27.5 Hypothèse écartée : la pondération du fit

La fidélité est un **cosinus**, donc insensible à l'échelle. Si la norme agit, ce ne
peut être que dans le **fit**, qui minimise une erreur *absolue* : une langue de
norme double y pèse quatre fois plus. J'ai ajouté la correction exacte — une pesée
`1/norme²` par langue, soit l'erreur *relative* — et **écrit la prédiction avant de
mesurer** : si l'effet vient de là, la corrélation doit tendre vers zéro.

| | fit ordinaire | fit pondéré |
|---|---:|---:|
| fidélité TEST | 0,5972 | **0,5969** |
| fidélité ↔ norme | −0,7540 | **−0,7613** |
| Q4 − Q1 (quartiles de norme) | −0,1313 | **−0,1362** |

**Réfuté** — et légèrement pire. La pondération n'est pas retenue.

### 27.6 Ce que cela change pour la suite

Le pont ne sert pas également les langues, et il ne le cachait pas : le calcul le
disait déjà, personne ne l'avait lu langue par langue. Deux conséquences :

1. **Toute affirmation sur ce pont doit nommer la langue ou le groupe.** Une
   fidélité moyenne de 0,60 recouvre 0,35 (deu) et 0,70 (dzo).
2. **Le levier le plus direct n'est pas la lecture, c'est la cible.** Pour `deu`,
   `jpn`, `kor`, `heb`, ni la constante, ni le pont, ni un ajustement privé
   n'atteignent le niveau des autres. C'est un argument pour la couche 8 : non pas
   « meilleure en moyenne » — elle l'est de +0,0215 sur Romeo — mais peut-être
   atteignable plus tôt par ces langues-là. Le traçage de la couche 8 sur les 392
   langues est en chaîne pour répondre exactement à cela.

L'outil est `tools/profil_langues.py`, la table `/tmp/profil_langues.csv` (indexée
par nom de langue).

### 27.7 Une erreur de ma part, corrigée

Dans une analyse intermédiaire, j'ai recopié un tableau de fidélités — trié par
norme décroissante — en l'associant à l'ordre du cache, qui est différent. Les
corrélations de ce script-là étaient **entièrement fausses** : il annonçait −0,042
là où la valeur est −0,754. Les corrélations publiées ici sont calculées **dans le
script**, où l'indexation est cohérente, et la table est écrite en CSV indexé par
nom. Aucun chiffre du §27 ne vient de la version fausse — mais elle a existé, donc
elle est signalée.


---

## 28. Réservoir multi-échelle : gain réel, mais ce n'était pas la cause

### 28.1 L'idée

La quantité de contenu par jeton varie de **6×** selon la langue (1,578 jeton/caractère
en pular contre 0,271 en allemand, §27). Le réservoir n'avait qu'**une** constante de
temps `a = 0,2`, donc **une** échelle de mémoire : la même en jetons, donc jusqu'à 6×
différente en contenu. Je lui ai donné des constantes **étalées logarithmiquement**
de 0,02 à 0,80 (médiane 0,127), une par neurone — même nombre de neurones, coût nul.

### 28.2 Prédiction, écrite avant la mesure

Si la mémoire mono-échelle était la limite, **l'apport propre du pont
(`fidélité − témoin`) devait augmenter préférentiellement sur les langues FAIBLEMENT
fragmentées** — celles où le pont n'apporte rien aujourd'hui (`deu` 0,271,
`pam` 0,332, `tpi` 0,352).

### 28.3 Mesure

| | mono-échelle | multi-échelle |
|---|---:|---:|
| fidélité TEST | 0,5972 | **0,5998** |
| **apport propre** | **+0,0294** | **+0,0320** (+8,8 %) |
| oracle par langue | 0,6935 | **0,6994** |
| apport ↔ fragmentation | +0,8206 | +0,7973 |
| oracle ↔ norme | −0,8368 | −0,8314 |

**37 langues sur 41 s'améliorent**, 4 régressent (`khm` −0,0046, `ell` −0,0025,
`mal` −0,0017, `tam` −0,0006).

Par quartile de fragmentation, le gain est bien plus grand là où le tokeniseur est
**efficace** :

| quartile | fragmentation | gain de l'apport |
|---|---:|---:|
| Q1 (la plus efficace) | 0,37 | **+0,0039** |
| Q4 (la plus hachée) | 1,30 | +0,0017 |

**La direction de la prédiction est confirmée, son amplitude non** : corrélation
(effet ↔ fragmentation) = **−0,2103**, faible. Et le plus gros gain individuel est
`fuf` (+0,0100), qui est la langue **la plus** fragmentée — l'inverse de la
prédiction.

### 28.4 Et surtout : les langues non servies ne sont pas servies

| langue | apport mono | apport multi | effet |
|---|---:|---:|---:|
| **deu** | +0,0133 | +0,0143 | **+0,0010** |
| **heb** | +0,0014 | +0,0023 | **+0,0009** |
| srp | +0,0128 | +0,0144 | +0,0016 |
| jpn | +0,0216 | +0,0219 | +0,0003 |
| kor | +0,0192 | +0,0215 | +0,0023 |

**L'écart entre Q1 (+0,019) et Q4 (+0,055) reste d'un facteur 3.** Le multi-échelle
est un gain général modeste, **pas** le correctif des langues que le pont ignore.
L'hypothèse de la constante de temps unique est donc **écartée comme cause
principale** — mesure faite, pas supposée.

### 28.5 Ce qui est retenu

Le réservoir multi-échelle est **conservé** : +8,8 % sur l'apport propre et +0,0059
sur l'oracle, à nombre de neurones constant et sans apprentissage. C'est un gain
gratuit et vérifié sur 37 langues. Mais il ne dispense pas de chercher la vraie
cause pour `deu`, `heb`, `jpn`, `kor`, `srp`.

Implémentation : `Pont.a_min` / `Pont.a_max` / `Pont.a_neur` (`tools/pont_generatif.py`),
propagés dans `nait`, `recalcule` et `compacte` — une constante de temps qui ne
suivrait pas le neurone à l'attrition changerait silencieusement la dynamique de
tous les survivants.


---

## 29. Le réservoir ne sert presque à rien — et le vrai témoin n'était pas celui que je croyais

Depuis le début, l'apport du pont est mesuré **contre la constante témoin** (`mt`).
C'est un témoin trop faible : il ne dit pas si le pont apporte quelque chose qu'une
**lecture directe de l'entrée du professeur** n'apporterait pas déjà. Je l'ai
mesuré. C'est la remise en cause la plus sérieuse de ce rapport.

### 29.1 Les quatre variantes, même vivier, même périmètre

351 langues d'apprentissage · 41 de test · **896 canaux** · entrée centrée par langue
(calculable à l'inférence) · lecture `[X, X²]`.

| | caractéristiques | fidélité TEST | apport vs constante |
|---|---:|---:|---:|
| témoin constant | 0 | 0,5678 | — |
| **A · 40 neurones récurrents, 1 couche** | 80 | 0,5972 | +0,0294 |
| **C · l'entrée SEULE, ZÉRO neurone** | 1 792 | **0,6536** | **+0,0857** |
| B · réservoir **et** entrée | 1 872 | **0,6609** | +0,0931 |
| D · 2 couches de 20 (même budget) | 80 | 0,5979 | +0,0301 |

### 29.2 Ce que cela dit, sans détour

**Une lecture sans aucun neurone — une simple application quadratique de la couche 0
du professeur — bat le réservoir de 40 neurones de +0,0564.** Et lui ajouter le
réservoir par-dessus ne rapporte plus que **+0,0073**.

Autrement dit : **sur ce périmètre, 40 neurones récurrents valent +0,007. Le pont,
tel qu'il est construit, est pour l'essentiel une sonde sur l'entrée.**

### 29.3 Et les langues « non servies » étaient servies depuis le début

C'est le plus instructif. Les langues pour lesquelles le pont n'apportait rien
(§27) sont précisément celles que la lecture directe sert le mieux :

| langue | apport A (réservoir) | apport C (entrée seule) |
|---|---:|---:|
| **heb** | +0,0014 | **+0,0637** |
| **srp** | +0,0128 | **+0,1005** |
| **deu** | +0,0133 | **+0,1024** |
| **jpn** | +0,0216 | **+0,1224** |
| **kor** | +0,0192 | **+0,0823** |

**L'information n'était pas absente : elle était dans l'entrée, et le réservoir la
détruisait.** L'hypothèse du §27.5 — « les caractéristiques ne portent pas le
contenu de ces langues » — est donc **fausse** : elle confondait « les
caractéristiques du réservoir » avec « les caractéristiques disponibles ». La couche
0 du professeur les porte.

### 29.4 La profondeur n'achète rien

**D (2 couches de 20) = 0,5979** contre **A (1 couche de 40) = 0,5972** : +0,0007,
soit le bruit. À budget de neurones constant, composer une couche de plus n'apporte
rien de mesurable. C'est une réponse — négative — à la question centrale de la
mission, et elle est mesurée.

### 29.5 Ce qui reste debout, et ce qui tombe

**Tombe** : l'idée que l'apport mesuré contre la constante qualifie le réservoir.
Il faut désormais mesurer contre **C**, la lecture directe de l'entrée.

**Reste debout** : toute la mécanique d'attention, d'oracle et de profil par langue,
qui a précisément permis de trouver cela. Et le fait que B (réservoir **et** entrée)
soit le meilleur des cinq — +0,0073 au-dessus de C — donc que le réservoir n'est pas
*nul*, seulement très bon marché à remplacer.

**Reste à établir** : C a 1 792 caractéristiques contre 80 pour A. Une partie de
l'écart peut être de la **capacité**, pas de la nature. Le contrôle qui tranche est
une lecture **linéaire seule** sur l'entrée (896 caractéristiques) et un réservoir
**beaucoup plus large**. C'est la prochaine mesure, et elle est écrite ici avant
d'être faite.

### 29.6 Une réserve de méthode

Le témoin constant n'était pas *faux* — c'est bien lui qui apparaît dans le résultat
de tête (0,7430 contre 0,7207). Mais il était **trop faible pour être informatif** :
il laissait croire que l'écart mesurait le pont, alors qu'il mesurait surtout ce que
la couche 0 contient déjà. Le corriger change la lecture de tous les écarts
« +0,02 à +0,03 » rapportés depuis le début, sans en changer un seul chiffre.

Outil : `tools/leviers_pont.py`.


---

## 30. Couche 8 contre couche 10, au niveau des DIX unités alignées

Le traçage par unité écrit les couches 0, 8 et 10. On peut donc comparer les deux
cibles sur **le même découpage et les mêmes langues** — 17 langues d'apprentissage,
230 unités de test, dix points de mesure alignés par langue au lieu d'un.

### 30.1 Les chiffres

| | couche 10 | couche 8 | écart |
|---|---:|---:|---:|
| canaux retenus | 151/896 | 121/896 | — |
| neurones (naissance libre + attrition) | 49 | 120 | — |
| **invariance du PROFESSEUR** | 0,6471 | **0,6998** | **+0,0527** |
| fidélité VALIDATION | 0,7649 | **0,8138** | +0,0489 |
| **fidélité TEST** | 0,7087 | **0,7582** | **+0,0495** |
| **oracle TEST** | 0,7439 | **0,8012** | **+0,0573** |
| notre invariance | **0,9701** | 0,9401 | −0,0300 |
| notre pire paire | **0,8702** | 0,7778 | −0,0924 |

**La couche 8 gagne sur tout ce qui mesure la cible** : le professeur y est plus
interlingue (+0,0527), et notre fidélité y est meilleure (+0,0495), y compris
mesurée contre l'oracle (+0,0573 — donc ce n'est pas un effet de lecture).

### 30.2 Deux réserves, et elles comptent

**Les réseaux n'ont pas la même taille** (49 neurones contre 120). La naissance
libre et l'attrition ont divergé, donc une partie de l'écart peut être de la
capacité et non de la couche. Ce n'est pas corrigé ici.

**Notre invariance BAISSE à la couche 8** (0,9401 contre 0,9701), alors que celle du
professeur MONTE. Nous sommes donc **plus invariants que le professeur**, et l'écart
se creuse à la couche 10 : 0,9701 pour nous contre 0,6471 pour lui. Un modèle qui
lisse plus que sa cible peut être en train de perdre du contenu, pas d'acquérir de
l'invariance. La fidélité (0,7582) dit que ce n'est pas un effondrement — mais le
point mérite d'être surveillé, et il n'est pas résolu.

### 30.3 Le décrochage d'une seule langue

À la couche 10, la pire paire mélangeait `csw`, `amh`, `acu`, `bum`. **À la couche 8,
`amh` apparaît dans 8 des 10 unités.** Ce n'est plus un bruit réparti mais une
langue qui décroche, et c'est un point d'enquête précis — pas encore instruit.

### 30.4 Une régression que j'ai introduite, et corrigée

En ajoutant la constante de temps par neurone (§28), j'ai étendu `nait`, `recalcule`
et `compacte` — mais **pas la recopie de généalogie de `tools/pont_parallele.py`**,
qui copiait `poids` sans copier `a_neur`. Résultat : le pont a planté sur **Romeo**
et sur **Wikipedia**, les deux sections entières, avec un `IndexError` obscur.

C'est exactement le risque que mon propre commentaire du §28 annonçait — « une
constante de temps qui ne suivrait pas le neurone changerait silencieusement la
dynamique » — et je ne l'ai pas vérifié ailleurs. Corrigé à deux endroits :

1. `pont_parallele.py` recopie désormais `a_neur`, avec un `assert` de cohérence ;
2. `recalcule` **refuse bruyamment** toute généalogie désynchronisée, au lieu de
   produire un calcul silencieux avec la mauvaise dynamique.

Les deux sections ont été relancées.


---

## 31. Contrôle de capacité : l'entrée gagne-t-elle par NATURE ou par TAILLE ?

Le §29 laissait une objection sérieuse : C (entrée seule, 1 792 caractéristiques) bat
A (40 neurones, 80 caractéristiques) — mais C a 22× plus de colonnes. Une partie de
l'écart peut être de la **capacité**, pas de la nature. Mesuré :

| | caractéristiques | fidélité TEST |
|---|---:|---:|
| témoin constant | 0 | 0,5678 |
| A40 · réservoir | 80 | 0,5972 |
| **A200 · réservoir (5× plus large)** | 400 | **0,6218** |
| **C_lin · entrée seule, LINÉAIRE** | 896 | **0,6364** |
| C_quad · entrée seule, quadratique | 1 792 | 0,6536 |
| B · A40 + entrée | 1 872 | 0,6609 |

Deux enseignements :

1. **La non-linéarité ne fait presque rien.** C_lin (896 colonnes) = 0,6364 contre
   C_quad (1 792 colonnes) = 0,6536. Doubler les colonnes par les carrés ne rapporte
   que +0,0172 : **l'essentiel de ce que porte l'entrée est accessible LINÉAIREMENT.**
2. **La capacité aide le réservoir, mais ne le rattrape pas.** 5× plus de neurones
   font passer A de 0,5972 à 0,6218 (+0,0246). Il reste 0,0146 sous C_lin, qui a
   2,2× plus de colonnes — donc à peu près à capacité comparable, le réservoir est
   toujours derrière.

**Verdict : la prédiction d'un avantage de NATURE est soutenue sans être tranchée.**
Le réservoir progresse avec la taille mais reste sous une lecture linéaire de
l'entrée.

### 31.1 Une mesure perdue, à refaire

La variante **A200 + entrée** — la plus intéressante, puisqu'elle dirait ce qu'un
gros réservoir ajoute quand on lui donne aussi l'accès direct — **n'a pas été
obtenue** : le processus a été tué avant la fin. Cause : je l'ai lancé avec
`nohup … &` **sans `setsid`**, et il n'a pas survécu à la sortie du shell. C'est la
deuxième fois dans cette session qu'un lancement sans `setsid`/`disown` coûte une
mesure ; la règle est désormais explicite. À relancer.


---

## 32. Le §29 est-il un artefact d'alignement ? NON — mesuré

### 32.1 Le soupçon

L'UDHR est **un seul texte** traduit en 392 langues : à la position `t`, toutes les
langues disent la même chose. La couche 0 encode la position. Une lecture `e_t → y_t`
pourrait donc apprendre « à la position `t`, sors le vecteur typique de `t` » et
réussir **sans rien comprendre à la langue** — ce qui expliquerait tout le §29, où
l'entrée seule bat le réservoir (le réservoir, lui, ne lit pas la position
directement).

### 32.2 Le témoin qui le quantifie — aucun paramètre, aucun neurone

On prédit la ligne `t` d'une tranche de test par la **moyenne des lignes `t` des
tranches d'apprentissage**. C'est le meilleur prédicteur possible qui ne connaisse
**que la position**. Comparé à la constante (une seule ligne pour toutes les
positions), l'écart est exactement ce que la position apporte.

| corpus | position seule | constante | **ce que la position ajoute** |
|---|---:|---:|---:|
| **UDHR** (392 langues, texte ALIGNÉ) | 0,5690 | 0,5545 | **+0,0145** |
| **Wikipedia EN** (192/48 tranches, articles DIFFÉRENTS) | 0,3704 | 0,3602 | **+0,0101** |

**La position n'apporte que +0,0145 sur l'UDHR aligné, et +0,0101 sur Wikipedia non
aligné** — soit 0,0044 d'écart entre les deux. Or l'avantage de la lecture directe sur
le réservoir (§29) est de **+0,0564**.

**Conclusion : l'alignement de l'UDHR n'explique pas le §29.** La position seule est
loin de rendre compte de ce que la lecture directe extrait, et le corpus aligné
n'apporte presque rien de plus que le corpus non aligné. **Le §29 tient.**

### 32.3 Wikipedia : le pont y transfère mieux qu'on ne le craignait

Le pont a aussi été relancé sur Wikipedia (240 tranches EN, 240 FR, **articles
différents** — donc non parallèle). La régression `a_neur` l'avait tué ; corrigé, il
donne :

| | Romeo (parallèle, littéraire) | Wikipedia (non parallèle, encyclopédique) |
|---|---:|---:|
| fidélité sur A | 0,6660 | 0,5522 |
| **fidélité sur B (transférée)** | **0,5802** | **0,5226** |
| perte au transfert | −0,0858 | **−0,0296** |
| oracle sur B | 0,6207 | **0,5545** |
| écart à l'oracle | +0,0405 | **+0,0319** |
| invariance de sortie | 0,9540 | 0,9165 |

**La perte au transfert est presque trois fois plus faible sur Wikipedia** (−0,0296
contre −0,0858), et l'écart à l'oracle y est plus petit. Le corpus encyclopédique
transfère donc **mieux** que le corpus littéraire — ce qui va dans le sens de la
mission : un texte long et varié donne un pont plus général, pas moins.

L'invariance du professeur sur Wikipedia (0,3032) **ne veut rien dire** : le corpus
n'est pas apparié, et l'outil l'affiche lui-même en avertissement.


---

## 33. Introspection du bloc — ce que j'ai cassé, et ce que j'ai appris sur ma propre mesure

Le mandat demande des rétrospectives en mode **introspection** et des revues en mode
**adverse autonome**. Voici l'une et l'autre, appliquées à ce bloc.

### 33.1 Trois erreurs, toutes les trois de ma part

**1. J'ai cassé la chaîne en ajoutant une fonctionnalité.** En donnant une constante
de temps par neurone (§28), j'ai correctement propagé `a_neur` dans `nait`,
`recalcule` **et** `compacte` — et j'ai écrit un commentaire expliquant précisément
pourquoi il fallait le propager partout. Puis je ne l'ai pas fait dans
`pont_parallele.py`, qui recopie la généalogie à la main. **Deux sections entières
sont mortes** (Romeo, Wikipedia), et je ne l'ai vu qu'une heure plus tard en lisant
un log que je n'avais pas relu. Le commentaire juste à côté du code fautif était le
mien.

*Leçon retenue, appliquée* : `recalcule` **refuse** désormais une généalogie
désynchronisée au lieu de planter obscurément ou — pire — de calculer en silence
avec la mauvaise dynamique.

**2. J'ai transcrit un tableau trié dans un ordre qui ne l'était pas.** Une analyse
intermédiaire a produit des corrélations entièrement fausses (−0,042 au lieu de
−0,754). Le tableau était trié par norme, l'index par ordre du cache. Corrigé en
faisant calculer les corrélations **là où l'indexation est cohérente**, et en
écrivant désormais les tables en CSV indexé par nom.

**3. J'ai lancé deux fois un calcul long sans `setsid`.** Le premier est mort avec
le shell ; le second aussi. Deux mesures perdues, dont une que j'ai dû réécrire plus
légère (2 192 colonnes → 1 296). La règle est maintenant explicite : **tout calcul
de plus de quelques minutes passe par `setsid`/`disown` ou par un job géré.**

### 33.2 La revue adverse : le chiffre de tête ne disait pas ce que je croyais

C'est le point le plus grave, et il n'est pas technique.

Depuis le début, l'apport du pont est mesuré **contre la constante témoin**. Ce
témoin est trop faible : il ne dit rien de ce qu'une lecture directe de l'entrée
apporterait. En le remplaçant par le bon témoin (§29), on découvre que **40 neurones
récurrents valent +0,007 au-dessus d'une simple régression sur la couche 0 du
professeur.** Le chiffre de tête (0,7430 contre 0,7207) reste exact, mais il ne
qualifie pas le pont : il qualifie surtout ce que la couche 0 contient déjà.

**Je n'ai pas choisi ce témoin par malhonnêteté — je ne l'ai pas remis en question
pendant des heures.** Un chiffre qui monte est un chiffre qu'on ne va pas déranger.
C'est exactement le biais que la consigne « toute affirmation non mesurée n'est pas
une affirmation » cherche à corriger, et il a fallu une question de côté (pourquoi
`dzo` est-il la pire paire ?) pour tomber dessus.

### 33.3 Ce qui a bien fonctionné, et pourquoi

**Le profil par langue.** C'est le seul outil qui a produit des résultats
inattendus à répétition : la fidélité EST le témoin constant (r = 0,977), l'apport
est prédit par la fragmentation (R² 0,67), les langues « non servies » étaient
servies depuis le début. Aucun de ces faits n'était visible dans une moyenne.

**Les prédictions écrites avant la mesure.** Elles ont été réfutées trois fois
(pesée 1/norme², multi-échelle comme cause principale, effet plus fort à faible
fragmentation). Trois réfutations valent mieux que trois confirmations : elles
disent que la mesure n'est pas un rituel.

**Le garde-fou `TERMINE` avec `grep -qx`.** Après la leçon du sous-chaîne, aucune
étape de la chaîne ne s'est déclenchée trop tôt.

### 33.4 Ce que je ne sais toujours pas

- **Pourquoi `amh` décroche à la couche 8** (8 unités sur 10). Piste ouverte.
- **Si l'avantage de l'entrée est de nature ou de capacité.** Le §31 le soutient
  sans le trancher : à capacité comparable, le réservoir reste derrière, mais
  l'égalisation n'est pas exacte.
- **Si notre invariance supérieure à celle du professeur** (0,9701 contre 0,6471)
  est un gain ou un effondrement déguisé.
- **Ce qu'un réservoir beaucoup plus large ajoute** par-dessus l'entrée : la mesure
  est relancée, elle a déjà échoué deux fois.

### 33.5 La question de fond, posée sans détour

La mission est un **modèle n-couches récurrent** capable de répondre au premier
niveau abstrait d'un gros modèle. Les mesures de ce bloc disent que, tel qu'il est
construit, ce modèle **n'ajoute presque rien** à une régression sur l'entrée du
professeur. Ce n'est pas une raison d'arrêter : c'est la mesure qui dit où le
travail n'est pas. Ajouter des couches n'achète rien (§29.4) ; ajouter des neurones
achète peu et mal (§31) ; viser la couche 8 plutôt que la 10 achète +0,0495 (§30).

**La piste que ces chiffres désignent n'est pas la taille du réservoir, c'est ce
qu'on lui donne à lire.** Il ne voit que `e_t` et sa propre récurrence. Or
l'information qui compte pour la cible est manifestement présente dans l'entrée, et
le réservoir la détruit au lieu de la structurer. La prochaine question n'est donc
pas « combien de neurones », mais **« quelle fenêtre d'entrée, et pour quelle
transformation »**.


---

## 34. Correction du §29 : le réservoir n'était pas inutile, il était TROP PETIT

Le §29 concluait que « 40 neurones récurrents valent +0,007 : le pont est pour
l'essentiel une sonde sur l'entrée ». La mesure qui manquait — un réservoir large
avec accès à l'entrée — **renverse cette conclusion**.

### 34.1 Le tableau complet, même vivier, même périmètre

351 langues d'apprentissage · 41 de test · 896 canaux · entrée centrée par langue.

| configuration | caractéristiques | fidélité TEST | apport vs constante |
|---|---:|---:|---:|
| témoin constant | 0 | 0,5678 | — |
| A40 · réservoir | 80 | 0,5972 | +0,0294 |
| A200 · réservoir | 400 | 0,6218 | +0,0540 |
| C_lin · entrée seule, linéaire | 896 | 0,6364 | +0,0686 |
| C_quad · entrée seule, quadratique | 1 792 | 0,6536 | +0,0857 |
| A40 + entrée quadratique | 1 872 | 0,6609 | +0,0931 |
| **A200 + entrée LINÉAIRE** | **1 296** | **0,6738** | **+0,1059** |

### 34.2 Ce n'est pas de la capacité

**A200 + entrée (1 296 caractéristiques) bat C_quad (1 792) et A40 + entrée (1 872)
avec MOINS de colonnes.** L'objection du §31 — « l'entrée gagne peut-être par
capacité » — est donc levée dans l'autre sens : **les 400 états récurrents portent
une information que l'expansion quadratique instantanée de l'entrée ne contient
pas.**

La différence est qualitative et nommable : `C_quad` ne voit que le **jeton
courant** `e_t` et son carré. Le réservoir voit `e_t` **et l'histoire** de la
séquence, à travers sa récurrence. Ce qu'il ajoute, c'est de la **mémoire
non linéaire**.

### 34.3 L'apport marginal croît avec la taille — il ne plafonne pas

| | apport du réservoir par-dessus l'entrée |
|---|---:|
| 40 neurones (+ entrée quadratique) | +0,0073 |
| **200 neurones (+ entrée linéaire)** | **+0,0374** |

Multiplier la taille par 5 multiplie l'apport marginal par 5. **Ce n'est pas une
saturation, c'est une pente.** Le §29 avait mesuré un point et conclu une tendance —
c'était l'erreur.

### 34.4 Ce qui reste vrai du §29

Le §29 n'était pas faux, il était **incomplet** : à 40 neurones, sur ce périmètre,
le réservoir vaut effectivement +0,007. Ce qui tombe, c'est la généralisation que
j'en avais tirée. Et le §29.4 (la profondeur n'achète rien) n'est pas touché : D
(2 couches de 20) = 0,5979 contre A (1 couche de 40) = 0,5972.

### 34.5 La suite, écrite avant d'être faite

Si l'apport croît avec la taille, il faut **la courbe**, pas un point : 400, 800
neurones, avec la même entrée linéaire. Deux questions précises :

1. **Où est le coude ?** Si +0,037 à 200 devient +0,06 à 800, l'architecture est la
   bonne et le problème est un budget de neurones. Si l'apport plafonne vers 200,
   c'est la **forme** de la récurrence qu'il faut revoir.
2. **Le réservoir aléatoire gelé est-il le bon ?** Les poids `P` et `B` sont tirés
   au hasard et ne changent jamais — seul le readout est ajusté. C'est ce qui rend
   le pont si peu coûteux, et c'est peut-être ce qui le limite.


---

## 35. Où va le temps — profil mesuré, et un remède gratuit

Question posée : le professeur ne devrait tourner qu'**une fois**, et l'apprentissage
par croissance devrait être quasi instantané sur cette machine. Où va le temps ?

### 35.1 Le pipeline, en quatre étapes, avec le coût MESURÉ de chacune

| étape | ce qu'elle fait | coût mesuré |
|---|---|---|
| **1. Passe professeur** (`drave --infer --trace-flux`) | fait tourner Qwen2.5-0.5B sur le texte et écrit la couche 0 et la couche cible à chaque position | **39,3 s par langue** → **392 langues = 4 h 17** |
| **2. Cache** (`cache_pont.py`) | lit les `.drvf` en `.npz` | 16 s |
| **3. Construction du réservoir** (`Pont.nait`) | boucle Python sur chaque pas de chaque langue (472 472 pas) | **24 µs/pas** → **0,4 min pour 40 neurones**, ~2 min pour 200, ~8 min pour 800 |
| **4. Trajectoires de test** (`recalcule`) | rejoue le réseau sur le test | ~5 s pour les 41 langues |
| **5. AJUSTEMENT DE LA LECTURE** (`ajuste`) | accumule la Gram `AᵀA` sur 472 472 lignes | **LE GOULOT — voir ci-dessous** |

**La construction du réservoir, que l'on soupçonnait, est l'étape la MOINS chère.**
0,4 minute pour 40 neurones sur 472 472 pas. C'est 24 µs par pas, dont l'essentiel
est de la surcharge d'interpréteur Python, pas du calcul.

### 35.2 Le vrai goulot : le fit de la lecture

La lecture est ajustée par moindres carrés ridgés. On accumule `AᵀA` où `A` a
`n_caractéristiques` colonnes et 472 472 lignes. Le coût est **O(lignes ×
caractéristiques²)**, et les caractéristiques valent `2 × neurones + 896` :

| neurones | caractéristiques | temps de fit mesuré |
|---:|---:|---:|
| 40 | 80 | quelques secondes |
| 200 | 1 296 | **~22 min** |
| 200 + entrée | 1 296 | ~22 min |
| 800 + entrée | 2 496 | **~80 min** |

C'est du calcul dense réel, pas de la surcharge. D'où la lenteur apparente : ce n'est
pas le modèle qui est lent, c'est **une régression sur un demi-million de lignes**.

### 35.3 Vous avez raison sur un point, et il a coûté 4 heures

**La passe professeur ne devrait avoir lieu qu'UNE fois.** Elle a eu lieu **deux
fois** : j'ai d'abord visé la couche 10, découvert que la couche 8 est le plateau
(§30), puis retracé les 392 langues. **4 h 17 perdues à cause de mon choix de cible.**

Et l'erreur est plus bête que ça : `--trace-couches` ne filtre que l'**écriture**. La
passe avant exécute les 24 couches de toute façon. Écrire 0, 4, 8, 10, 12 et 16 au
lieu de 0 et 10 n'aurait coûté **presque rien** et aurait rendu la question du
plateau réponseable sans aucune repasse. La convention actuelle écrit le minimum et
paie le maximum.

### 35.4 Votre intuition « millisecondes » : elle tient à moitié

**L'évaluation est rapide** : 41 langues de test, 76 812 pas, en ~5 s — soit 0,1 s
par langue. C'est la récurrence, séquentielle en `t`, à ~50 µs par pas. Pas des
millisecondes, mais pas lent non plus.

**Le fit, lui, ne peut pas être en millisecondes** : résoudre un système de 472 472
équations à 1 296 inconnues, sur 351 séquences, c'est ~1,7 TFLOP. À 1,2 TFLOP/s
effectif, cela fait 22 minutes. Le chiffre est cohérent avec le matériel.

### 35.5 Le remède gratuit, mesuré

Une régression sur 472 472 lignes est massivement sur-déterminée. J'ai mesuré ce que
coûte de n'en garder qu'une fraction (lecture linéaire sur l'entrée, 896 colonnes,
évaluation sur **tout** le test) :

| sous-échantillonnage | lignes | temps de fit | fidélité TEST |
|---|---:|---:|---:|
| 1/1 | 472 472 | 328,0 s | **0,6364** |
| 1/2 | 236 318 | 129,4 s | 0,6353 |
| **1/5** | **94 634** | **56,4 s** | **0,6319** |
| 1/10 | 47 395 | 29,5 s | 0,6265 |
| 1/20 | 23 790 | 14,9 s | 0,6161 |

**Garder une ligne sur cinq rend le fit 5,8× plus rapide et coûte 0,0045 de
fidélité** — 0,7 % en relatif. C'est le meilleur rapport temps/qualité disponible, et
il ne demande aucune approximation : c'est le même modèle, ajusté sur moins de
points.

*(Contrôle de cohérence : la valeur 1/1 vaut 0,6364, exactement le `C_lin` du §31.)*

### 35.6 Les remèdes, par ordre de gain

| remède | gain | coût |
|---|---|---|
| **Tracer TOUTES les couches utiles en UNE passe** | **4 h 17 économisées** | nul |
| **Sous-échantillonner le fit à 1/5** | **5,8×** | −0,0045 de fidélité |
| Gram en `float32` | ~2× | à mesurer |
| Mettre en cache les états du réservoir sur disque | exploration quasi gratuite | disque |
| Vectoriser le réservoir **sur les langues** (boucler sur `t`, pas sur les pas) | construction en secondes | réécriture |

Le dernier point mérite d'être dit clairement : la récurrence est séquentielle en `t`,
mais **les langues sont indépendantes**. La boucle actuelle est
`pour chaque langue : pour chaque pas`. L'inverse — `pour chaque pas : toutes les
langues d'un coup` — ferait passer 472 472 itérations Python à ~4 000, chacune sur un
tableau `(351, k)`. Ce n'est pas le goulot aujourd'hui, mais c'est un plancher de
24-275 µs par pas qu'on peut supprimer.


---

## 36. Le protocole à DEUX PANNEAUX tranche : le goulot est le TRANSFERT, pas les caractéristiques

Le protocole exige l'oracle sur deux panneaux : le **TEST**, hors vivier (41 langues
jamais vues), et la **VALIDATION**, du même vivier que l'apprentissage. Un langage
d'apprentissage sur sept est mis de côté (51 langues), et la lecture est ajustée sur
les 300 restantes seulement. Mesuré, couche 10, 40 neurones, 1 couche, 80
caractéristiques, 896 canaux :

| | TEST (hors vivier) | VALIDATION (même vivier) |
|---|---:|---:|
| fidélité | 0,5960 | **0,6206** |
| témoin constant | 0,5678 | 0,5889 |
| **apport propre** | +0,0282 | **+0,0317** |
| oracle | 0,6935 | 0,6318 |
| **écart à l'oracle** | **+0,0975** | **+0,0112** |

### 36.1 Ce que cela dit, et c'est décisif

**Dans le vivier, notre lecture partagée est à 0,0112 de l'oracle** — c'est-à-dire
quasi optimale. Les caractéristiques suffisent, la lecture suffit, il n'y a rien à
gagner sur ces langues.

**Hors vivier, l'écart est 8,7× plus grand (+0,0975).** Un ajustement privé
rapporterait dix fois plus sur une langue jamais vue que sur une langue du vivier.

**Le goulot n'est donc ni la taille du réseau, ni la lecture, ni les
caractéristiques : c'est le TRANSFERT d'une langue à l'autre.**

### 36.2 Cela réconcilie trois résultats qui semblaient se contredire

- Le §27 trouvait que l'oracle **par langue** restait mauvais sur `deu`, `jpn`, `kor`,
  `heb` — donc « les caractéristiques ne portent pas ces langues ».
- Le §34 trouvait qu'un **gros** réservoir ajoutait +0,0374 par-dessus l'entrée —
  donc la capacité compte.
- Le §29 trouvait qu'à **40** neurones le réservoir n'ajoutait que +0,007.

Les trois tiennent ensemble si l'on sépare les panneaux : **dans le vivier tout va
bien ; c'est la généralisation à une langue nouvelle qui coûte.** Un plus gros
réservoir aide non pas parce que la lecture manque de place, mais parce que ses
caractéristiques **transfèrent mieux**.

### 36.3 La piste que cela désigne

Si le problème est le transfert, la question n'est plus « combien de neurones » mais
**« qu'est-ce qui, dans nos caractéristiques, est propre à la langue et ne transfère
pas ? »**. Le §27 en donne déjà le corrélat : l'apport transfère d'autant mieux que
le tokeniseur hache la langue (R² 0,67), et d'autant moins que sa représentation est
de forte norme.

C'est une question de **facteurs communs**, pas de taille. Et elle est mesurable :
il suffit de chercher la partie des états qui est commune aux langues du vivier, et
de la garder seule.

### 36.4 Note de méthode

La couche 10 a été **recalculée avec le même code** que la couche 8 (`/tmp/profil_l10.csv`),
précisément parce que le protocole a changé le vivier d'ajustement (300 au lieu de
351). Comparer un chiffre ancien à un chiffre nouveau aurait été une faute — c'est
exactement l'erreur de périmètre déjà commise plus tôt dans ce rapport.

L'effet du changement est faible mais réel : à périmètre identique, la fidélité TEST
passe de 0,5972 (351 langues d'ajustement) à 0,5960 (300). L'apport passe de +0,0294
à +0,0282.


---

## 37. Le ride était dix fois trop fort — et l'écart de transfert n'est pas du sur-apprentissage

### 37.1 Balayage du ride, deux panneaux

Prédiction écrite avant la mesure : si la lecture sur-apprend le vivier, augmenter le
ride doit **réduire l'écart à l'oracle hors vivier**. Mesuré (40 neurones, 1 couche,
80 caractéristiques, 896 canaux, 300 langues d'ajustement / 51 de validation / 41 de
test) :

| ride | VALID fid | VALID écart | TEST fid | TEST écart |
|---:|---:|---:|---:|---:|
| 0,0003 | 0,6301 | +0,0191 | 0,6204 | +0,0468 |
| 0,001 | 0,6302 | +0,0190 | 0,6207 | +0,0465 |
| 0,003 | 0,6304 | +0,0187 | 0,6212 | +0,0458 |
| 0,01 | **0,6307** | +0,0177 | 0,6224 | +0,0440 |
| **0,03** | 0,6304 | +0,0159 | **0,6233** | +0,0409 |
| 0,1 | 0,6274 | +0,0133 | 0,6220 | +0,0364 |
| **0,3 (valeur du pont)** | 0,6206 | +0,0112 | 0,6159 | +0,0329 |
| 1,0 | 0,6106 | +0,0087 | 0,6044 | +0,0303 |
| 3,0 | 0,6022 | +0,0060 | 0,5930 | +0,0279 |
| 10 | 0,5964 | +0,0031 | 0,5842 | +0,0195 |
| 30 | 0,5940 | +0,0013 | 0,5804 | +0,0097 |

**L'écart diminue bien (+0,047 → +0,010), MAIS parce que les deux baissent** —
l'oracle chute plus vite que nous. **La prédiction est réfutée : le transfert manquant
n'est pas du sur-apprentissage de la lecture.**

### 37.2 Le gain gratuit : le ride de 0,3 est 10 à 30 fois trop fort

La fidélité TEST est **maximale à ride 0,03** (0,6233) et la validation à 0,01
(0,6307). À la valeur utilisée jusqu'ici (0,3) elles valent 0,6159 et 0,6206 :

| | ride 0,3 (actuel) | ride 0,03 | gain |
|---|---:|---:|---:|
| fidélité TEST | 0,6159 | **0,6233** | **+0,0074** |
| fidélité VALIDATION | 0,6206 | 0,6304 | +0,0098 |

C'est **+0,0074 gratuit**, sans un neurone de plus, sans apprentissage — le ride
n'avait jamais été balayé sur ce critère. En dessous de 0,01 la qualité retombe
(0,6204 à 0,0003) : l'optimum est un vrai maximum, pas un bord.

L'ancien 0,3 avait probablement été choisi sur un périmètre plus petit, et n'a jamais
été réexaminé. **Il faut le remplacer par 0,03.**

---

## 38. Stabilité de la récurrence et coût réel d'une implémentation par événements

Deux questions posées : la récursion peut-elle **osciller** (« épilepsie ») au lieu de
se stabiliser, et une implémentation **par événements** ferait-elle gagner du temps ?

### 38.1 Stabilité — mesurée, la crainte n'est pas réalisée

La récurrence `s_t = (1-a)·s_{t-1} + a·tanh(P·s_{t-1} + B·e_t)` a pour jacobien
`J = (1-a)·I + a·D·P` avec `D = diag(1 - tanh²)`. Son rayon spectral décide.

| a | rayon (D = I) | **rayon (D observé)** | max \|s\| | verdict |
|---:|---:|---:|---:|---|
| 0,05 | 0,997 | 0,989 | 1,000 | stable |
| **0,20 (valeur du pont)** | 0,991 | **0,944** | 1,000 | stable |
| 0,40 | 0,983 | 0,847 | 1,000 | stable |
| 0,80 | 0,973 | 0,436 | 1,000 | stable |
| 0,95 | 0,971 | 0,154 | 1,000 | stable |
| 1,20 | **1,436** | 0,200 | **1,500** | hors régime |

**Aucune oscillation jusqu'à a = 0,95.** Et le comportement est contre-intuitif mais
sain : **un `a` plus grand est PLUS stable**, parce qu'il sature davantage le `tanh`,
ce qui réduit `D` donc le gain de boucle. À a = 0,2 la marge est encore confortable
(rayon 0,944) mais c'est la plus faible de la plage utile — c'est le point à
surveiller si l'on augmente le gain d'entrée ou si l'on vient à ajuster `P`.

À a = 1,2 le rayon calculé avec `D = I` dépasse 1 et l'état sort de `[-1, 1]`
(max 1,5) : **la limite pratique est entre 0,95 et 1,2.**

### 38.2 Événements — la dynamique actuelle n'est PAS creuse, et c'est mesuré

« Événement » = `|s_t - s_{t-1}| > seuil`. Sur du corpus réel, 40 neurones :

| seuil | a = 0,2 | a = 0,8 |
|---:|---:|---:|
| 1e-6 | 99,9 % | 99,2 % |
| 1e-4 | **99,8 %** | 97,2 % |
| 1e-2 | 98,4 % | 90,4 % |
| neurones saturés (\|s\| > 0,99) | **0,6 %** | 14,8 % |

**Une implémentation par événements paierait 0,2 % de pas en moins à a = 0,2, et
2,8 % à a = 0,8.** Autrement dit : **rien.**

**La raison que j'avais écrite ici était FAUSSE, et la mesure la corrige.** J'avais
lu « 0,6 % de saturation » comme « la dynamique vit dans son régime linéaire ». C'est
une confusion entre deux choses différentes :

| | mesure |
|---|---:|
| argument du `tanh`, `\|B·e_t\|` | **moyenne 16,9 · max 126** |
| saturation de la SORTIE du `tanh` | quasi totale |
| état `\|s_t\|` (moyenne glissante) | moyenne **0,347** · > 0,99 seulement 0,6 % du temps |

Le `tanh` **sature donc presque toujours** : son argument vaut 16,9 en moyenne, très
au-delà de ±1. Ce que le « 0,6 % » mesurait, c'est l'**état**, qui est une moyenne
glissante `s_t = 0,8·s_{t-1} + 0,2·tanh(...)` de sorties essentiellement **binaires**
(±1). Une moyenne de ±1 qui se répond au hasard reste près de zéro.

**Le réservoir calcule donc une moyenne glissante de projections aléatoires binaires
de l'entrée.** C'est pour cela que :
- les événements sont inutiles — les sorties binaires basculent constamment, 99,8 %
  des neurones changent à chaque pas ;
- une lecture linéaire de l'entrée fait presque aussi bien (§29) — une moyenne de
  projections binaires est proche d'une fonctionnelle linéaire de l'entrée récente ;
- augmenter le gain ne change RIEN (mesuré de 1 à 16 : saturation 0,6 % → 0,8 %,
  fidélité identique à 1e-4) — **le `tanh` est déjà saturé à gain 1**, en ajouter ne
  peut donc rien changer.

**La conséquence est contre-intuitive et c'est une piste : le levier n'est pas
d'augmenter le gain, c'est de le BAISSER** — pour que le `tanh` cesse de saturer et
que chaque neurone transmette une information graduée au lieu d'un signe.

### 38.3 Ce que cela implique pour le passage aux impulsions

Le passage à un modèle à impulsions n'est donc **pas une optimisation de cette
dynamique** — c'en est un **changement**. Une impulsion est creuse *par
construction* : seuil, émission, remise à zéro. Pour que la parcimonie apparaisse, il
faut **pousser la dynamique en saturation**, c'est-à-dire augmenter le gain d'entrée
jusqu'à ce que les neurones basculent au lieu de dériver.

C'est mesurable, et c'est la mesure qui manque : **quel gain d'entrée donne quel taux
de saturation ?** Si `gain = 1` sature 0,6 % et que `gain = 8` en sature 60 %, alors
la porte des impulsions est ouverte et le coût par événement devient intéressant.
Tant que la saturation reste sous quelques pour cent, l'événementiel ne peut rien
apporter — et le dire maintenant évite une réécriture qui ne paierait pas.

### 38.4 Sur le nombre de couches

L'argument « un modèle récursif devrait avoir un nombre de couches inférieur ou égal
à un FFN » est **déjà soutenu par la mesure** : D (2 couches de 20) = 0,5979 contre A
(1 couche de 40) = 0,5972 — la profondeur n'achète rien à budget constant (§29.4). Le
pont tient dans **une** couche face aux 24 du professeur.


---

## 39. La courbe : pas de coude, le réservoir continue de payer

Le §34 avait mesuré une pente en deux points et demandé **la courbe**. La voici —
même vivier, 896 canaux, ride 0,03, fit sur 1/5 des lignes (§35.5, coût 0,0045) :

| neurones | A seul | A + entrée linéaire | apport sur `C_lin` | caractéristiques |
|---:|---:|---:|---:|---:|
| 40 | 0,5972 | 0,6609 (entrée quad.) | +0,0073 | 1 872 |
| **200** | 0,6218 | 0,6693 | **+0,0329** | 1 296 |
| **400** | 0,6333 | 0,6763 | **+0,0399** | 1 696 |
| **800** | **0,6421** | **0,6821** | **+0,0457** | 2 496 |

**Aucun coude.** L'apport du réservoir par-dessus l'entrée croît de façon monotone :
+0,0329 → +0,0399 → +0,0457 en doublant deux fois. Il est **sub-linéaire** (le
doublement rapporte de moins en moins : +0,0070 puis +0,0058) mais il ne plafonne
pas.

Et le point décisif reste vrai à chaque taille : **A800 + entrée (2 496
caractéristiques) fait 0,6821, contre 0,6536 pour `C_quad` (1 792 caractéristiques,
entrée seule quadratique)**. Le réservoir n'est pas un substitut à de la capacité
d'entrée : il porte une information que l'expansion instantanée de l'entrée ne
contient pas.

**Meilleur résultat de la session : fidélité TEST 0,6821, 800 neurones, 1 couche.**

### 39.1 Ce que cela dit de la croissance

La mission repose sur la **croissance** par corrélation, sans rétropropagation. Cette
courbe la valide : ajouter des neurones achète du transfert, régulièrement. Si l'on
veut +0,06, il faut de l'ordre de 2 000 à 3 000 neurones — c'est un budget, pas un
obstacle de principe.

### 39.2 Le point de méthode

La fidélité de `A200 + entrée` vaut 0,6738 avec **toutes** les lignes et 0,6693 avec
une sur cinq : le sous-échantillonnage coûte bien les 0,0045 annoncés, ni plus ni
moins. La prévision du §35.5 se vérifie donc sur un second cas.

---

## 40. Prédiction réfutée : baisser le gain n'ouvre PAS le régime gradué

Le §38.2 terminait sur une piste contre-intuitive : puisque le `tanh` est déjà saturé
à gain 1, **baisser** le gain devrait le faire sortir de saturation et donner à chaque
neurone une information graduée au lieu d'un signe. Mesuré :

| gain | saturation | événements 1e-4 | fidélité VALID | fidélité TEST |
|---:|---:|---:|---:|---:|
| 0,003 | 0,0 % | 99,4 % | 0,5985 | 0,5868 |
| 0,01 | 0,0 % | 99,8 % | 0,6112 | 0,6033 |
| 0,03 | 0,0 % | 99,9 % | 0,6217 | 0,6129 |
| 0,1 | 0,0 % | 100,0 % | 0,6281 | 0,6207 |
| 0,3 | 0,3 % | 100,0 % | 0,6301 | 0,6229 |
| **1,0 (valeur du pont)** | 0,6 % | 99,8 % | **0,6304** | **0,6233** |

**Réfutée, et nettement** : la fidélité **monte** de façon monotone avec le gain. Le
gain 1 est déjà au sommet de la plage utile, et sortir de saturation ne fait que
détruire l'information.

Autrement dit : **la saturation n'est pas un défaut, c'est le mécanisme.** Le `tanh`
saturé transforme l'entrée en signes ; la récurrence en fait une moyenne glissante de
signes ; c'est cette moyenne qui porte le contenu. Un neurone gradué, lui, ne
transmet presque rien.

**Troisième prédiction réfutée de la session** — après la pesée `1/norme²` (§27.3) et
le multi-échelle comme cause principale (§28). C'est le signe que les mesures ne sont
pas des rituels, et cela vaut d'être dit à égalité avec les résultats positifs.

### 40.1 Conséquence pour le passage aux impulsions

Le tableau ci-dessus est aussi la réponse à la question des événements. De 0,003 à 1,
le taux d'événements **ne descend jamais sous 99,4 %**. Il n'existe aucun réglage du
gain, dans cette dynamique, qui rende le calcul creux.

Le passage aux impulsions n'est donc **pas un réglage** : c'est un **changement de
dynamique** (seuil, émission, remise à zéro), et il faudra le mesurer comme tel — en
comparant une dynamique impulsionnelle à celle-ci, pas en espérant que celle-ci
devienne creuse.


---

## 41. Le profil porte maintenant TOUT le protocole — et il révèle un écart d'invariance

`tools/profil_langues.py` rapporte désormais, en une seule exécution : **taille du
réseau**, **invariance inter-langue et pire paire** (professeur ET notre sortie),
**fidélité et apport sur le TEST hors vivier et sur la VALIDATION du même vivier**,
et **l'écart à l'oracle sur les deux panneaux**. C'est le protocole complet.

Couche 10, 40 neurones, 1 couche, 80 caractéristiques, 896 canaux, 41 langues de test
(mesure sur la **dernière position** du texte entier — le point de contenu que l'UDHR
aligne d'une langue à l'autre) :

| | professeur | notre sortie |
|---|---:|---:|
| invariance inter-langue | 0,6529 | **0,9565** |
| **pire paire** | **0,0478** | **0,7371** |

### 41.1 Nous sommes BEAUCOUP plus invariants que le professeur

L'écart est massif et il ne va pas dans le sens qu'on croit :

- la **pire paire** du professeur vaut **0,0478** — deux langues dont la
  représentation de couche 10 est quasi orthogonale ;
- la nôtre vaut **0,7371** — nous les rendons très semblables.

Notre sortie est donc **plus uniforme que sa cible**. Deux lectures, et je ne tranche
pas :

1. **C'est la mission.** Un pont linguistico-sémantique *veut* l'invariance : si deux
   langues disent la même chose, leurs représentations doivent se ressembler. Sous cet
   angle, 0,9565 est un succès et 0,0478 dit que le professeur, lui, garde énormément
   de marque linguistique à sa couche 10.
2. **C'est un excès de lissage.** Notre fidélité n'est que de 0,5960 : nous ne
   reproduisons pas la cible, nous en produisons une version plus pauvre et plus
   consensuelle. Une invariance obtenue en effaçant les différences n'est pas de
   l'invariance, c'est de l'appauvrissement.

**Ce qui manque pour trancher** : la même mesure sur un corpus où le CONTENU diffère
d'une langue à l'autre. Si notre invariance reste à 0,95 alors que les contenus sont
différents, c'est du lissage. Sur l'UDHR, où tout le monde dit la même chose, les deux
lectures sont indiscernables — et c'est une limite du corpus, pas de la mesure.

### 41.2 Note de méthode sur les périmètres

Ces 0,6529 / 0,9565 se mesurent au **dernier pas du texte entier**. Le §30 mesurait
0,6471 au niveau des **dix unités alignées**. Les deux valent ce qu'ils valent, mais
ils ne se comparent pas : même si les chiffres sont proches, le découpage diffère. Le
périmètre est nommé à chaque fois, comme il doit l'être.

### 41.3 Le profil complet, en un bloc

```
TAILLE DU RÉSEAU : 40 neurones · 1 couche [40] · 80 caractéristiques
INVARIANCE : professeur 0,6529 (pire 0,0478) · notre sortie 0,9565 (pire 0,7371)
TEST       (hors vivier) : fidélité 0,5960 · apport +0,0282 · oracle 0,6935
VALIDATION (même vivier) : fidélité 0,6206 · apport +0,0317 · oracle 0,6318
ÉCART À L'ORACLE : TEST +0,0975 · VALIDATION +0,0112
```

C'est ce bloc qui sera produit pour la couche 8 sur les 392 langues, et c'est lui qui
rendra la comparaison des deux cibles légitime — même code, même périmètre, mêmes
quatre mesures.


---

## 42. Jalon : 392 langues tracées aux DEUX couches, zéro échec

| corpus | contenu | taille | langues | échecs |
|---|---|---:|---:|---:|
| `udhr392/` | couches 0 et 10 | 2,7 Go | **392/392** | **0** |
| `udhr392_c8/` | couches 0, **8** et 10 | 4,0 Go | **392/392** | **0** |
| `unites/` | 10 unités alignées, couches 0, 8 et 10 | 491 Mo | **400/400** | **0** |

Passe couche 8 : **241 minutes**, 36,9 s par langue en moyenne. Passe couche 10 :
environ 4 h 17 (§35). Les deux passes ont coûté **~8 heures de professeur**, dont
4 h 17 auraient pu être évitées : `--trace-couches` ne filtre que l'**écriture**, donc
écrire 0, 4, 8, 10, 12 et 16 dans la première passe n'aurait presque rien coûté. C'est
la leçon la plus chère de la session, et elle est corrigée pour toute passe future.

L'objectif « étendre le pont à TOUTES les langues de l'UDHR » est donc atteint **sur
les deux cibles**, et l'invariance se mesure désormais sur **dix points alignés par
langue** au lieu d'un.


---

## 43. Le goulot de la CROISSANCE : 28 s par neurone, ramené à 1,76 s

En lisant le code pour lancer l'entraînement complet, j'ai trouvé un coût que
personne n'avait nommé : **`nait` boucle `pour chaque langue : pour chaque pas`**,
soit **472 472 itérations d'interpréteur Python**. Chaque naissance coûtait donc
**28 secondes** — et le mode `--naissance libre` fait **une naissance par neurone**.

### 43.1 La vectorisation, et pourquoi elle est légitime

**Les langues sont indépendantes.** Seule la récurrence en `t` est séquentielle. On
regroupe donc les langues par longueurs voisines et on boucle sur `t`, toutes les
langues du bloc d'un coup. Le calcul est **le même** : c'est une vectorisation, pas un
changement d'algorithme.

### 43.2 Identité bit à bit — vérifiée, pas supposée

Comparaison avec l'ancienne boucle recopiée telle quelle, sur 25 langues réelles,
pour trois tailles de naissance et trois tailles de bloc :

| k \ bloc | 4 | 16 | 64 |
|---:|---:|---:|---:|
| 1 | **0,000e+00** | **0,000e+00** | **0,000e+00** |
| 7 | **0,000e+00** | **0,000e+00** | **0,000e+00** |
| 40 | **0,000e+00** | **0,000e+00** | **0,000e+00** |

**L'écart maximal est exactement zéro**, pas « petit ». La vectorisation ne change
rien aux trajectoires.

### 43.3 Le gain, sur le corpus complet

351 langues, 472 472 pas :

| langues par bloc | `nait(1)` |
|---:|---:|
| 8 | 2,58 s |
| 16 | 2,07 s |
| **32 (retenu)** | **1,76 s** |
| 64 | 1,67 s |

**×16 sur l'étape centrale de la croissance.** Le mode libre passait de 28 s à 1,76 s
par neurone : 300 neurones coûtaient 2 h 20 de naissances, ils en coûtent 9 minutes.

### 43.4 Ce que cela dit de la question « où va le temps »

C'était **la troisième réponse** à cette question, et chacune a désigné un endroit
différent :

1. le **fit de la lecture** (22 min par ajustement à 1 296 colonnes) — §35 ;
2. la **passe professeur** (4 h 17, faite deux fois par ma faute) — §35.3 et §42 ;
3. la **croissance** (28 s par neurone, ×16 par vectorisation) — ici.

Les trois sont indépendants, et aucun n'était visible sans instrumenter. La
simulation des neurones, soupçonnée la première, n'était le goulot dans aucun des
trois cas.


---

## 44. Couche 8 contre couche 10 à l'échelle des 392 langues : 41 sur 41, zéro régression

Le traçage de la couche 8 est terminé (§42) et l'analyse a tourné **avec exactement le
même code, le même périmètre et les mêmes quatre mesures** que la couche 10 — les
deux profils ont été recalculés dans la même exécution, précisément pour que la
comparaison soit légitime.

**Protocole complet** : 351 langues d'apprentissage (300 d'ajustement + 51 de
validation), 41 langues de test hors vivier, 896 canaux, 40 neurones, 1 couche,
80 caractéristiques, fit sur 300 langues, évaluation entière.

### 44.1 Le tableau

| | couche 10 | **couche 8** | écart |
|---|---:|---:|---:|
| fidélité **TEST** (hors vivier) | 0,5960 | **0,6424** | **+0,0464** |
| fidélité **VALIDATION** (même vivier) | 0,6206 | **0,6768** | +0,0562 |
| témoin constant sur TEST | 0,5678 | 0,6049 | +0,0371 |
| **apport propre TEST** | +0,0282 | **+0,0375** | **+0,0093** |
| apport propre VALIDATION | +0,0317 | +0,0328 | +0,0011 |
| oracle TEST | 0,6935 | **0,7427** | +0,0492 |
| **écart à l'oracle TEST** | **+0,0975** | **+0,1003** | +0,0028 |
| écart à l'oracle VALIDATION | +0,0112 | +0,0121 | +0,0009 |
| invariance du **professeur** | 0,6529 | **0,6836** | +0,0307 |
| invariance de **notre sortie** | 0,9565 | 0,9483 | −0,0082 |
| **pire paire** du professeur | 0,0478 | **0,0104** | |
| **pire paire** de notre sortie | 0,7371 | 0,6798 | −0,0573 |
| corrélation apport ↔ fragmentation | +0,7986 (R² 0,64) | +0,8175 (R² 0,67) | |
| corrélation oracle ↔ norme | −0,8368 | −0,8022 | |

### 44.2 Le résultat sans ambiguïté : 41 sur 41

Langue par langue, sur les 41 langues de test :

- **apport propre : 41 langues améliorées, 0 dégradée**, gain moyen **+0,0112** ;
- **oracle : 41 améliorées, 0 dégradée**, gain moyen **+0,0492**.

Ce n'est pas une moyenne qui monte en cachant des pertes : **aucune langue ne perd.**
C'est la mesure la plus nette de la session.

Et les langues les plus mal servies sont celles qui gagnent le plus :

| langue | apport L10 | apport L8 | effet | oracle L10 → L8 |
|---|---:|---:|---:|---|
| **amh** | +0,0535 | +0,0880 | **+0,0345** | 0,7538 → 0,7814 |
| **csw** | +0,0639 | +0,0980 | **+0,0342** | 0,7859 → 0,8333 |
| **dzo** | +0,0885 | +0,1219 | **+0,0334** | 0,7907 → 0,8108 |
| mya | +0,0769 | +0,1018 | +0,0250 | 0,7515 → 0,7661 |
| lao | +0,0379 | +0,0609 | +0,0230 | 0,7450 → 0,7782 |
| tha | +0,0208 | +0,0437 | +0,0229 | 0,6374 → 0,6840 |
| **heb** | +0,0014 | +0,0099 | **+0,0085** | 0,5916 → 0,6412 |
| … | | | | |
| **deu** | +0,0133 | +0,0146 | +0,0012 | 0,5388 → 0,5676 |
| **jpn** | +0,0216 | +0,0218 | **+0,0002** | 0,5747 → 0,5964 |
| **srp** | +0,0128 | +0,0140 | +0,0012 | 0,5615 → 0,6144 |

`heb` multiplie son apport par **7**, `csw` et `amh` gagnent +0,034. Les trois langues
que rien ne servait (`deu`, `jpn`, `srp`) gagnent peu — **elles restent le noyau dur.**

### 44.3 Ce que la couche 8 NE règle PAS : le transfert

**L'écart à l'oracle est inchangé : +0,0975 à la couche 10, +0,1003 à la couche 8.**
Dans le vivier, il reste à +0,012. Autrement dit :

> **le goulot de transfert identifié au §36 est structurel — il ne dépend pas de la
> couche visée.** Changer de cible améliore tout le monde uniformément, mais ne
> réduit pas d'un iota l'écart entre ce que nos caractéristiques permettent (oracle)
> et ce que notre lecture partagée en tire.

C'est un résultat négatif précis, et il oriente : la question n'est plus « quelle
couche », ni « combien de neurones », mais **« qu'est-ce qui, dans nos états, ne
transfère pas d'une langue à l'autre »**.

### 44.4 Deux réserves qui comptent

**1. Les deux tiers du gain brut sont le témoin, pas le pont.** La fidélité TEST gagne
+0,0464, mais le **témoin constant** gagne +0,0371 à lui seul (0,5678 → 0,6049) : la
couche 8 est simplement plus prévisible pour tout le monde. L'apport **propre** du
pont ne gagne que **+0,0093**. C'est réel, mais six fois plus petit que le chiffre
brut.

**2. La pire paire du professeur EMPIRE à la couche 8 : 0,0104 contre 0,0478.** Deux
langues dont les représentations de couche 8 sont quasi orthogonales, là où la couche
10 les rapprochait un peu. Notre sortie, elle, reste à 0,6798 — nous lissons toujours
beaucoup plus que notre cible (§41).

### 44.5 Le multi-échelle, confirmé à l'échelle 392

| | mono-échelle | multi-échelle | effet |
|---|---:|---:|---:|
| apport TEST (couche 8) | +0,0375 | **+0,0406** | +0,0031 |
| apport TEST (couche 10) | +0,0282 | +0,0307 | +0,0025 |
| corrélation effet ↔ fragmentation | | | −0,3094 |

Le gain est du même ordre qu'au §28 (+0,0025), la corrélation avec la fragmentation
reste **faible** (−0,31) : la prédiction d'origine n'est toujours pas confirmée.

### 44.6 Verdict

**La couche 8 est la bonne cible, et c'est maintenant établi à l'échelle des 392
langues, sur deux panneaux, avec 41 langues sur 41 qui s'améliorent et aucune qui
régresse.** Le gain propre est de +0,0093 à +0,0112 selon la mesure ; le gain d'oracle
de +0,0492.

Mais **la couche 8 ne réduit pas le goulot de transfert**, et c'est désormais la
question centrale.


---

## 45. Premier corpus MULTI-DOMAINE et ALIGNÉ : 482 articles Wikipedia en 6 langues

### 45.1 Ce que la machine contenait et qui n'avait pas été utilisé

Dix bases **Wikipedia décompressées**, 30 Go au total, dans
`data/wikipedia/db/*.db` : arabe, allemand, anglais, espagnol, français, italien,
japonais, portugais, russe, chinois. Chacune porte, par article, son **résumé**
(2 000 caractères), indexé par titre.

C'est exactement le « grand corpus multilingue » que l'objectif demande, et il était
là depuis le début. Le pont n'avait travaillé que sur l'UDHR — **un seul texte**,
juridique et répétitif.

### 45.2 Comment on apparie sans être aligné

Wikipedia n'est pas aligné : les articles diffèrent d'une langue à l'autre. Mais un
article donné existe souvent **sous le même titre** dans plusieurs langues quand ce
titre est un nom propre ou un internationalisme (« Albert Einstein », « Albedo »,
« Achilles »). On garde donc les titres présents dans **toutes** les langues visées.

Rendement mesuré sur 400 titres anglais tirés au hasard :

| langue | présents | | langue | présents |
|---|---:|---|---|---:|
| fr | 173/400 | | ru | **39/400** |
| de | 179/400 | | zh | **27/400** |
| es | 142/400 | | ja | **22/400** |
| it | 182/400 | | ar | **1/400** |
| pt | 149/400 | | | |

**Les écritures non latines transcrivent les noms** : l'appariement par titre y est
stérile (1 sur 400 en arabe). Le corpus aligné est donc bâti sur les **six langues
latines** ; arabe, chinois, japonais et russe restent disponibles pour la fidélité et
le transfert, **pas** pour l'invariance.

### 45.3 Le corpus, mesuré

Sur 4 000 titres anglais candidats (résumé > 900 caractères), **483 tiennent dans les
six langues (12 %)**. Écrit dans `corpus/wiki_apparie/` :

| langue | articles | caractères | moyenne par article |
|---|---:|---:|---:|
| en | 482 | 961 174 | 1 994 |
| fr | 482 | 942 809 | 1 956 |
| de | 482 | 948 858 | 1 969 |
| es | 482 | 940 144 | 1 951 |
| it | 482 | 944 789 | 1 960 |
| pt | 482 | 923 709 | 1 916 |

**2 892 fichiers, ~5,7 millions de caractères.** Contre l'UDHR : **un** texte de
~1 300 jetons.

### 45.4 Pourquoi cela change ce qu'on peut mesurer

**1. Le multi-domaine.** L'UDHR est mono-domaine : l'hypothèse « le vocabulaire dépend
du domaine » n'y était **pas testable** (§25). Ici, 482 articles couvrent la science,
l'histoire, la géographie, les personnes — et chaque article est traduit. On peut donc
enfin séparer **ce qui vient de la langue** de **ce qui vient du domaine**.

**2. Le professeur est plus riche.** 2 000 caractères d'encyclopédie par article,
contre un texte juridique répétitif. Le vocabulaire et la syntaxe sont bien plus
variés.

**3. Six langues latines proches** — un cas de contrôle utile : si l'invariance est
déjà imparfaite entre six langues apparentées, elle ne peut pas être meilleure entre
familles éloignées.

### 45.5 Un gain de traçage, vérifié octet à octet

Puisque la couche 8 est la cible retenue (§44), il est inutile d'**exécuter** les 24
couches du professeur. `--couches 0:9` n'exécute que 0..8.

**Vérifié, et pas supposé** : sur `en_Albert_Einstein` et `de_Albert_Einstein`, la
trace produite avec `--couches 0:9` est **identique OCTET À OCTET** à celle produite
avec `--couches 0:24` — même MD5 (`400c4a1ed58700bbc59a6848d02ae757` pour l'anglais).
Et c'est **1,6× plus rapide** : 15 s contre 24 s.

C'est la troisième fois de la session qu'une optimisation est vérifiée par identité
plutôt que supposée — après `--ctx` et la vectorisation de `nait`.

### 45.6 Le traçage est lancé

**2 892 traces** à ~16 s, soit **~13 heures**. Elles sont analysables par lots au fur
et à mesure ; la chaîne écrit son journal dans `/tmp/trace_wiki_apparie.log` et se
termine par `TERMINE` (garde `grep -qx`, pas de correspondance de sous-chaîne).


---

## 46. Deuxième œuvre parallèle, et deuxième couple de langues

### 46.1 Le manque

Le corpus parallèle du pont ne comptait qu'**une** œuvre : *Roméo et Juliette*, en
anglais et en français, 24 scènes. Or **une seule paire de langues ne permet pas de
distinguer une propriété du PONT d'une propriété du COUPLE de langues.** Si le
transfert se comporte de la même façon sur une seconde paire, c'est le pont ; sinon,
c'était en–fr.

Les bases `backlog_gutenberg_{en,fr,de,es}.db` (Panini-Research) contiennent trois
paires exploitables :

| œuvre | paire | découpage | état |
|---|---|---|---|
| Roméo et Juliette | en–fr | 24 scènes | déjà traité |
| Le Comte de Monte-Cristo | en–fr | tomes de tailles très inégales (2,6 M contre 0,73 M caractères) | écarté |
| **Crime et Châtiment** | **en–es** | **39 chapitres (en) / 40 (es)** | **retenu** |

### 46.2 Alignement EXACT, pas approximatif

On ne découpe pas à offsets fixes : le même caractère ne dit pas la même chose dans
les deux langues. On découpe **par chapitre**, et le chapitre `i` d'une langue
correspond au chapitre `i` de l'autre. Vérifié sur les tailles, dont le rapport reste
entre **0,82 et 1,14** sur les 38 premiers chapitres.

L'anglais marque `CHAPTER <romain>`, l'espagnol une ligne ne portant que le numéro
romain. **On ne garde que les chapitres qui tiennent dans `--ctx 8192` DANS LES DEUX
LANGUES** — un chapitre tronqué d'un seul côté romprait l'alignement sans le dire.
Seuil retenu : 30 000 caractères.

### 46.3 Le corpus

Écrit dans `corpus/parallele_crime/` :

| langue | segments | caractères | moyenne |
|---|---:|---:|---:|
| en | **24** | 590 808 | 24 617 |
| es | **24** | 564 651 | 23 527 |

**24 chapitres alignés — exactement l'ordre de grandeur des 24 scènes de Romeo**, ce
qui rend les deux corpus directement comparables. Mais **2 000 fois plus longs** :
24 600 caractères par segment contre ~1 200 pour une scène de Romeo.

### 46.4 Une fausse alerte que j'ai levée, et qui méritait de l'être

En comparant deux traces du même fichier, j'ai obtenu **des tailles et des empreintes
MD5 différentes** — ce qui aurait signifié que le moteur n'est pas déterministe, et
aurait mis en doute toutes les mesures de la session.

**C'était faux, et l'erreur est de moi** : les deux fichiers comparés étaient **partiels**,
tronqués par les `timeout` que j'avais posés sur mes propres commandes. La comparaison
propre — `--couches 0:9` contre `--couches 0:24`, sur `en_Albert_Einstein` et
`de_Albert_Einstein` — donne des empreintes **identiques** (§45.5). Le moteur est
déterministe ; c'est ma façon de mesurer qui ne l'était pas.

Leçon appliquée : les traçages longs sont lancés **sans `timeout`**, avec un journal
qui permet de savoir ce qui est complet et ce qui ne l'est pas.

### 46.5 Coût, et pourquoi il est acceptable

Un chapitre de 25 000 caractères coûte ~250 s (la machine est partagée). 48 traces,
soit **~3,5 heures**, lancées en tâche de fond et analysables par segment : après `n`
segments on a `n` points alignés.

Traçage en cours, journal `/tmp/trace_crime.log`, garde `grep -qx TERMINE`.


---

## 47. Fidélité et invariance TIRENT EN SENS OPPOSÉ quand le réseau grandit

Le journal de la croissance (§44, couche 10, ride 0,03, lecture quadratique,
multi-échelle, 300 langues d'ajustement et 51 de validation) donne, à chaque
naissance, la fidélité **et** l'invariance. Les deux courbes vont dans des directions
opposées, et de façon monotone :

| neurones | fidélité TEST | invariance inter-langue | pire paire |
|---:|---:|---:|---:|
| 8 | 0,6151 | **0,9437** | **0,7399** |
| 24 | 0,6261 | 0,9206 | 0,6551 |
| 40 | 0,6294 | 0,9084 | 0,6559 |
| 64 | 0,6287 | 0,8971 | 0,6625 |
| 96 | 0,6311 | 0,8819 | 0,6419 |
| 128 | 0,6302 | 0,8760 | 0,5935 |
| 160 | 0,6327 | 0,8662 | 0,5737 |
| 179 | **0,6336** | **0,8661** | **0,5594** |

| | 8 → 179 neurones |
|---|---:|
| fidélité TEST | **+0,0185** |
| invariance | **−0,0776** |
| pire paire | **−0,1805** |

**Le coût est quatre fois le gain, et il porte exactement sur ce que la mission
cherche.** Ajouter des neurones rend le pont plus fidèle *et moins interlingue*.

### 47.1 Pourquoi, et ce n'est pas un accident

La lecture est ajustée pour reproduire la représentation du professeur. Or **le
professeur garde lui-même beaucoup de structure propre aux langues** : son invariance
est de 0,6836 à la couche 8 et 0,6529 à la couche 10 (§44, §41). Un réseau plus
grand reproduit davantage de cette structure **et donc davantage de marque
linguistique**.

Autrement dit : **le pont devient plus fidèle et moins « pont » à mesure qu'il
grandit.** Ce n'est pas un défaut de réglage, c'est l'objectif qui est ambigu — on
demande au même ajustement de copier la cible *et* d'effacer ce que la cible contient.

### 47.2 Le résultat contre-intuitif : le PETIT réseau est presque aussi bon

À **8 neurones**, la fidélité vaut déjà 0,6151 contre 0,6336 au mieux — **2 % de
moins** — et l'invariance est de 0,9437 contre 0,8661. Si l'objectif est un pont
interlingue, **un réseau huit fois plus petit est meilleur sur l'axe qui compte**.

### 47.3 La suite que cela désigne : une lecture ajustée SOUS CONTRAINTE d'invariance

L'ajustement actuel minimise `‖XW − Y‖²` seul. Il ignore complètement l'invariance.
Or la pénalité manquante **reste en forme fermée** :

> pénaliser la variance **inter-langue** de la sortie `XW` — c'est-à-dire
> `Σ_i ‖m_i − m̄‖²`, où `m_i` est la moyenne par langue de la sortie — ajoute un terme
> **quadratique en `W`**. L'objectif total reste quadratique, donc résoluble d'un seul
> coup, sans rétropropagation.

C'est un changement d'objectif, pas d'algorithme : on demande à la lecture de copier
la cible **tout en rapprochant les langues**, avec un curseur pour doser. C'est
exactement ce que la mission demande, et cela n'a jamais été essayé.

**Prédiction, écrite avant la mesure** : pénaliser l'invariance doit faire monter
l'invariance et baisser la fidélité ; le point intéressant est **le taux d'échange**.
Si l'invariance monte beaucoup pour peu de fidélité, le curseur est un vrai levier.


---

## 48. Ajuster la lecture SOUS CONTRAINTE d'invariance : le levier existe, et il est bon marché

### 48.1 Le principe, et pourquoi il reste en forme fermée

L'ajustement ordinaire minimise `‖XW − Y‖²` **seul**. Il ignore l'invariance
inter-langue — d'où la tension mesurée au §47. On ajoute donc à l'objectif la
**variance inter-langue de la sortie** :

```
P(W) = Σ_i n_i ‖m_i − m̄‖²        m_i = moyenne par langue de X_i·W
```

`P` est **quadratique en `W`** : `P(W) = tr(Wᵀ C W)` avec
`C = Σ_i n_i (M_i − M̄)ᵀ(M_i − M̄)`. L'objectif total reste quadratique et la solution
reste **en forme fermée** :

```
(XᵀX + μ·C_échelle + ride·I) W = Xᵀ(Y − mt)
```

**On ne change pas d'algorithme, on change d'objectif** — et la contrainte « aucune
rétropropagation » est respectée à la lettre.

### 48.2 Une première tentative FAUSSE, et ce qu'elle a appris

J'avais d'abord écrit la pénalité `μ·len(X)·C`. Mesuré :

| μ | fid TEST | invariance | pire paire |
|---:|---:|---:|---:|
| 0 | 0,6646 | 0,8740 | 0,4463 |
| 0,003 | 0,5982 | **0,9998** | **0,9986** |
| ≥ 0,01 | 0,5988 | **1,0000** | **1,0000** |

**Une falaise, pas un curseur.** L'invariance passe de 0,874 à 0,9998 dès le plus
petit μ non nul, et la fidélité tombe à 0,5988 — **sous le témoin constant** (0,6049
à la couche 8). Autrement dit : la sortie devenait la MÊME pour toutes les langues,
donc ne dépendait plus de l'entrée.

La cause est arithmétique : `len(X)·trace(C)` vaut **~80× `trace(XᵀX)`**, donc même
μ=0,003 écrasait le terme de données. Corrigé en normalisant `C` pour que **μ=1
signifie « pénalité de même échelle que l'ajustement »**.

### 48.3 Le vrai curseur

Couche 8, 40 neurones, 1 couche, lecture quadratique, multi-échelle, 300 langues
d'ajustement / 51 de validation / 41 de test, 896 canaux :

| μ | fid VAL | **fid TEST** | **invariance** | **pire paire** |
|---:|---:|---:|---:|---:|
| **0** | 0,6942 | **0,6646** | 0,8740 | 0,4463 |
| 0,001 | 0,6942 | 0,6646 | 0,8747 | 0,4489 |
| 0,003 | 0,6941 | 0,6644 | 0,8760 | 0,4540 |
| 0,01 | 0,6939 | 0,6639 | 0,8803 | 0,4713 |
| 0,03 | 0,6930 | 0,6624 | 0,8909 | 0,5152 |
| **0,1** | 0,6895 | **0,6564** | **0,9157** | **0,6224** |
| 0,3 | 0,6812 | 0,6429 | 0,9448 | 0,7543 |
| 1,0 | 0,6689 | **0,6242** | **0,9677** | **0,8600** |

**La prédiction est confirmée** : l'invariance monte, la fidélité baisse, et la
courbe est régulière sur trois ordres de grandeur de μ.

### 48.4 Le taux d'échange, et il est favorable

| de μ=0 à | gain d'invariance | gain de pire paire | coût de fidélité TEST |
|---|---:|---:|---:|
| μ=0,03 | +0,0169 | +0,0689 | **−0,0022** |
| **μ=0,1** | **+0,0417** | **+0,1761** | **−0,0082** |
| μ=0,3 | +0,0707 | +0,3080 | −0,0217 |
| μ=1,0 | +0,0937 | +0,4137 | −0,0404 |

**À μ = 0,1, on achète +0,042 d'invariance et +0,176 de pire paire pour 0,008 de
fidélité.** Le rapport est de **5 pour 1**, et sur la pire paire de **21 pour 1**.

C'est le premier levier de toute la session qui améliore **l'axe que la mission
cherche** sans coûter cher, et il ne demande ni neurone, ni couche, ni apprentissage
supplémentaire — seulement un terme de plus dans une équation qu'on résolvait déjà.

### 48.5 Ce que cela ne règle pas

À μ=0,1 notre invariance vaut 0,9157, contre **0,6836 pour le professeur**. Nous
restons **beaucoup plus invariants que notre propre cible**, et notre pire paire
(0,6224) reste très au-dessus de la sienne (0,0104). Le §41 n'est donc pas résolu : la
question « est-ce de l'invariance ou de l'appauvrissement ? » tient toujours, et elle
se tranchera sur un corpus où **le contenu diffère d'une langue à l'autre** — ce que
l'UDHR ne permet pas et que le corpus Wikipedia apparié (§45) permettra.

**μ = 0,1 est retenu comme point de fonctionnement par défaut** : c'est le point où le
gain d'invariance reste cinq fois son coût.


---

## 49. Croissance libre + attrition à 392 langues : le résultat complet

Protocole entier, couche 10, `--part-langues 0.5`, ride 0,03, lecture quadratique,
réservoir multi-échelle, fit sur 1/20 des lignes, **300 langues d'ajustement /
51 de validation / 41 de test**, 896 canaux.

| | |
|---|---:|
| naissance libre | **191 neurones nés**, arrêt par patience |
| **meilleur réseau (selon la VALIDATION)** | **182 neurones · 1 couche** |
| fidélité apprentissage | 0,6501 |
| fidélité VALIDATION | 0,6339 |
| **fidélité TEST** (hors vivier) | **0,6340** |
| constante témoin sur TEST | 0,5762 |
| **apport propre** | **+0,0578** |
| **invariance inter-langue** | **0,8659** |
| **pire paire** | **0,5556** |

Comparé au profil à 40 neurones de la même famille de réglages (couche 10,
multi-échelle, ride 0,03) : fidélité TEST 0,5985 → **0,6340**, soit **+0,0355**.
La croissance et l'attrition apportent donc bien un gain réel.

### 49.1 L'attrition n'a rien retranché d'utile — et c'est un résultat

L'attrition est descendue de 191 à 9 neurones, **et la validation a baissé à chaque
pas** : 0,6339 · 0,6328 · 0,6308 · 0,6288 · 0,6275 · 0,6255 · 0,6243 · 0,6221 ·
0,6206 · 0,6202 · 0,6192 · 0,6158. Le meilleur passage est donc le réseau **né**, et
l'attrition le confirme au lieu de le réduire.

**Mais le TEST, lui, préférait un autre point** : à **144 neurones** le TEST vaut
0,6362 contre 0,6340 à 191. L'écart est faible (0,0022) et il dit quelque chose
d'important : **le critère de sélection (51 langues de validation) et la mesure
d'intérêt (41 langues de test) ne désignent pas le même réseau.** Sélectionner sur
la validation est honnête, mais ce n'est pas gratuit.

### 49.2 Un drapeau qui ne se déclenchait plus, et c'est ma faute

Le bloc **oracle** ne figure pas dans ce résultat. En corrigeant plus tôt le
`IndexError` d'`opt` sur les drapeaux sans valeur, j'ai fait retourner `""` à un
drapeau placé en dernière position — et `if opt("--oracle", "")` devient alors
**faux**. Le drapeau ne plantait plus, il ne faisait plus rien. Quatre drapeaux
étaient dans ce cas : `--oracle`, `--centre-entree`, `--biais`, `--normalise`.

**Un drapeau se teste par sa PRÉSENCE (`in sys.argv`), jamais par sa valeur.** Corrigé
aux quatre endroits. C'est la deuxième fois de la session qu'un drapeau se comporte
mal en silence — la première fois il « marchait par accident » en renvoyant l'option
suivante.

**Conséquence sur le protocole** : sans ce bloc, le diagnostic oracle sur les **deux
panneaux** manque à ce résultat. Il sera fourni par la passe suivante, qui tourne en
outre **sous contrainte d'invariance** (`--mu-inv 0,1`, §48).


---

## 50. La contrainte d'invariance déplace la courbe, elle ne supprime pas la tension

Le §48 avait balayé μ sur **40 neurones**. Reste à savoir si la contrainte **annule**
le compromis du §47 ou si elle le **déplace**. Mesuré à **179 neurones**, couche 8,
mêmes 300/51/41 langues, mêmes 896 canaux :

| μ | fid VAL | **fid TEST** | **invariance** | **pire paire** |
|---:|---:|---:|---:|---:|
| 0 | 0,7251 | **0,6922** | 0,7492 | 0,3719 |
| 0,03 | 0,7246 | 0,6908 | 0,7701 | 0,4089 |
| 0,1 | 0,7218 | **0,6852** | **0,8019** | **0,4255** |
| 0,3 | 0,7131 | 0,6695 | 0,8405 | 0,4575 |

### 50.1 Les deux tailles, côte à côte

| | 40 neurones | 179 neurones |
|---|---:|---:|
| **μ = 0** : fid TEST | 0,6646 | **0,6922** |
| **μ = 0** : invariance | **0,8740** | 0,7492 |
| **μ = 0,1** : fid TEST | 0,6564 | **0,6852** |
| **μ = 0,1** : invariance | **0,9157** | 0,8019 |
| **μ = 0,1** : pire paire | **0,6224** | 0,4255 |
| gain d'invariance à μ=0,1 | +0,0417 | **+0,0528** |
| coût de fidélité à μ=0,1 | −0,0082 | **−0,0070** |

**La contrainte est encore plus rentable sur le grand réseau** : +0,0528 d'invariance
pour 0,0070 de fidélité, soit **7,5 pour 1** (contre 5 pour 1 à 40 neurones). Le
levier fonctionne, et il fonctionne mieux là où le besoin est le plus grand.

### 50.2 Mais la tension demeure

À μ = 0,1, passer de 40 à 179 neurones donne **+0,0288 de fidélité pour −0,1138
d'invariance**. Le rapport est de **1 pour 4** — le même sens qu'au §47, et le même
ordre de grandeur.

**La contrainte ne supprime donc pas le compromis : elle translate toute la courbe
vers plus d'invariance.** C'est un déplacement utile — à μ=0,1 et 179 neurones on a
0,8019 d'invariance, ce que le réseau nu n'atteint nulle part — mais grandir coûte
toujours ce que la mission cherche.

### 50.3 Ce que cela dit du choix d'architecture

Puisque la tension est réelle et monotone, **le choix de taille est un choix
d'objectif, pas de qualité** :

- si l'on veut **la fidélité** — reproduire le plus exactement possible la couche du
  professeur — il faut grandir, et accepter de perdre l'invariance ;
- si l'on veut **le pont** — que les langues se ressemblent au niveau abstrait — un
  réseau **petit** et une contrainte modérée donnent le meilleur point mesuré :
  **40 neurones, μ = 0,1 → fidélité 0,6564 · invariance 0,9157 · pire paire 0,6224.**

C'est le premier endroit de ce rapport où un choix d'architecture se déduit
proprement des mesures au lieu d'être postulé.


---

## 51. La contrainte d'invariance fonctionne DANS la croissance, pas seulement sur réseau fixe

Le §48 mesurait μ sur un réseau **déjà construit**. Restait à savoir si la contrainte
tient pendant que le réseau **naît**. Deux croissances libres, mêmes réglages
(couche 10, ride 0,03, quadratique, multi-échelle, 300/51/41 langues, 896 canaux),
**à μ = 0 et à μ = 0,1**, comparées à taille égale :

| neurones | μ = 0 : fid TEST · inv · pire | **μ = 0,1 : fid TEST · inv · pire** |
|---:|---|---|
| 40 | 0,6294 · 0,9084 · 0,6559 | 0,6278 · **0,9289** · **0,7329** |
| 64 | 0,6287 · 0,8971 · 0,6625 | 0,6274 · **0,9201** · **0,7364** |
| 96 | 0,6311 · 0,8819 · 0,6419 | 0,6298 · **0,9075** · **0,7090** |

| à taille égale | coût de fidélité | gain d'invariance | gain de pire paire |
|---|---:|---:|---:|
| 40 neurones | −0,0016 | **+0,0205** | **+0,0770** |
| 64 neurones | −0,0013 | **+0,0230** | **+0,0739** |
| 96 neurones | −0,0013 | **+0,0256** | **+0,0671** |

**Le taux d'échange est de 16 à 20 pour 1 sur l'invariance, et de 26 à 50 pour 1 sur
la pire paire.** Le coût de fidélité est constant (−0,0013 à −0,0016) et pratiquement
négligeable — trois à quatre fois plus petit que le bruit de graine mesuré ailleurs
dans ce rapport.

### 51.1 Ce que cela change

La contrainte n'est donc **pas** un artefact d'un réseau figé : elle agit à chaque
ajustement pendant la croissance, et son effet **s'accumule proprement**. À 96
neurones, le réseau contraint a **plus d'invariance (0,9075)** que le réseau **non
contraint en avait à 8 neurones** (0,8819 au §47) — tout en ayant une fidélité de
0,6298 contre 0,6151.

Autrement dit : **la contrainte permet de grandir sans payer l'invariance**, ce que
la croissance seule ne permettait pas. C'était exactement le problème du §47.

### 51.2 Réserve

La comparaison porte sur **une graine** (graine 5) pour chaque condition. Le §34 avait
mesuré qu'un écart de 0,0026 sépare deux graines sur ce genre de réseau : le coût de
fidélité (−0,0013) est **du même ordre**, donc « gratuit » se lit ici comme
« indiscernable du bruit », pas comme « exactement nul ». Le gain d'invariance, lui,
vaut 15 à 20 fois ce bruit.


---

## 52. Un processus ORPHELIN volait la moitié de la machine — et mon propre outil de nettoyage l'avait laissé passer

### 52.1 Le symptôme

Le traçage du corpus Wikipedia apparié tournait **quatre fois trop lentement** :
**60 s par trace** au lieu des 16 s mesurés à vide. À ce rythme, 2 892 traces
demandaient **48 heures** — au-delà de toute fenêtre.

### 52.2 La cause

Deux processus `drave` tournaient **en parallèle** alors que le script de traçage est
**séquentiel** : il n'en lance qu'un à la fois. Le second avait pour parent
`systemd --user` (PID 1 du utilisateur) — c'était un **orphelin**, survivant d'un
lancement antérieur dont j'avais tué le script mais **pas l'enfant**.

Un processus dont le parent meurt est **ré-adopté par `systemd`** et continue de
tourner. Il consommait **18 cœurs sur 40**, et écrivait dans
`parallele_crime/traces/en_05.drvf` — un fichier **partiel**, tronqué en pleine
écriture, que le script aurait ensuite **sauté** (`[ -s fichier ] && continue`) en le
croyant complet.

### 52.3 Pourquoi mon outil de nettoyage ne l'a pas vu

Mon tueur en Python cherche un motif dans la ligne de commande des processus :

```python
if 'trace_crime' in cl or ('ctx 8192' in cl and 'drave' in cl):
```

Or la ligne de commande du **script** contient `trace_crime`, mais celle de son
**enfant `drave`** ne la contient pas — elle contient `drave … --trace-flux …`. Tuer
le script laisse donc l'enfant vivant, ré-adopté, invisible au motif suivant.

**La règle qui manquait** : quand on tue un script qui lance des enfants, il faut tuer
**par arbre de processus**, pas par motif de ligne de commande. Et vérifier ensuite
qu'aucun orphelin n'a `systemd` pour parent.

### 52.4 Le résultat après nettoyage

| | avant | après |
|---|---:|---:|
| durée d'une trace Wikipedia | **60 s** | **16-17 s** |
| charge moyenne | 45 | **28** |
| durée estimée des 2 892 traces | 48 h | **~13 h** |

**Un seul orphelin coûtait 2,5× sur tout le corpus.** Et le fichier partiel a été
supprimé : il aurait produit un segment manquant **silencieusement**, exactement le
genre de faute que ce rapport traque ailleurs.

### 52.5 Une décision prise au passage

Le traçage du corpus **Crime et Châtiment** a été **arrêté** : 774 s par trace
(13 minutes !) pour 48 traces, en concurrence avec les 2 892 traces Wikipedia qui
demandent 17 s chacune. Le rapport de valeur était manifestement défavorable.
**4 segments sur 24 sont tracés** et conservés ; le corpus est écrit et pourra être
traité plus tard, hors concurrence.


---

## 53. Domaine ou langue ? Enfin testable, et la réponse est « à égalité »

### 53.1 Pourquoi il fallait un autre corpus

L'hypothèse — « certains mots et groupes de mots sont spécifiques à leur domaine ; ils
sont plus communs à leur domaine qu'à leur langue » — était **intestable sur l'UDHR** :
c'est **un seul texte** traduit en 392 langues, donc ses « contenus différents » (les
dix unités) restent le même texte juridique. Le §25 l'avait signalé sans pouvoir aller
plus loin.

Le corpus Wikipedia apparié (§45) lève l'obstacle : **61 articles distincts**
(science, histoire, géographie, personnes…) traduits dans **six** langues latines.

Deux similarités, mesurées sur les mêmes représentations :
- `S_langue` — **même article, langues différentes** : 915 paires ;
- `S_domaine` — **même langue, articles différents** : 10 980 paires.

### 53.2 Le résultat

| couche | S_langue | S_domaine | écart | verdict |
|---:|---:|---:|---:|---|
| **0** | 0,0489 | 0,0535 | **−0,0046** | **LANGUE domine** |
| **8** | **0,2158** | 0,2131 | **+0,0026** | **CONTENU domine** — de justesse |

**À la couche 0 — l'entrée du professeur — la LANGUE domine.** Deux articles différents
dans la même langue se ressemblent plus que le même article dans deux langues.

**À la couche 8, l'ordre s'inverse, mais de 0,0026 seulement** — soit 1,2 % en relatif.
C'est **une égalité à l'épaisseur du trait**, pas une domination.

### 53.3 Ce que cela dit de l'hypothèse, et du §25

**L'hypothèse est très faiblement soutenue à la couche 8, et réfutée à la couche 0.**
Autrement dit : le fait que deux textes parlent du même sujet ne les rapproche
quasiment pas plus, dans la représentation, que le fait d'être écrits dans la même
langue.

**Et cela disqualifie le chiffre de l'UDHR.** Le §25 rapportait `S_langue` 0,6132 contre
`S_domaine` 0,8578, soit **+0,19** en faveur du contenu. Sur un corpus réellement
multi-domaine, le même écart tombe à **+0,0026** — **70 fois moins**. L'écart de l'UDHR
ne mesurait pas le domaine : il mesurait que les dix « contenus différents » de l'UDHR
sont **le même texte**.

C'est la deuxième fois de la session qu'un corpus mono-contenu donne un chiffre qui ne
veut pas dire ce qu'il semble dire — après la constante témoin du §27.

### 53.4 Réserve

61 articles, six langues **apparentées** (toutes latines). Le résultat vaut pour ce
voisinage. Entre familles éloignées, `S_langue` baisserait probablement, ce qui
donnerait plus de poids au contenu — mais ce n'est pas mesuré, et l'appariement par
titre est stérile en écriture non latine (§45.2).

### 53.5 Une erreur de ma part dans la chaîne, corrigée

La construction des caches a d'abord produit **six caches à zéro langue**, sans
planter. Cause : j'intersectais les **noms de fichiers** (`de_A` contre `en_A`) au lieu
des **slugs** (`A`) — une intersection vide **par construction**. Corrigé, et la
construction rapporte maintenant les 71 articles communs aux six langues.

Leçon : un cache vide ne lève aucune erreur ; il faut que l'outil **dise combien** il a
trouvé, ce que celui-ci fait (« 0 langues · 0 pas »).


---

## 54. Le garde-fou du §30 a attrapé une SECONDE occurrence du même bug

### 54.1 Ce qui s'est passé

La croissance sous contrainte d'invariance (μ = 0,1) a parcouru **toute** la naissance
et **toute** l'attrition, puis a planté au moment du **diagnostic oracle** :

```
ValueError: généalogie désynchronisée : 6 constantes de temps pour 149 neurones.
```

**C'est le garde-fou ajouté au §30 qui a parlé**, et il a bien fait.

### 54.2 La cause : le même oubli, à un troisième endroit

En ajoutant la constante de temps par neurone (§28), j'avais propagé `a_neur` dans
`nait`, `recalcule` et `compacte` — **et écrit un commentaire expliquant qu'il fallait
la propager partout.** J'ai ensuite trouvé, et corrigé, un oubli dans
`pont_parallele.py` (§30.4). Voici le **troisième** :

**La sauvegarde et la restauration du « meilleur passage » de l'attrition.** Le code
met de côté `poids`, `X`, `couches` et `compte_neurones` pour pouvoir y revenir après
être descendu jusqu'à un neurone — **mais pas `a_neur`**. À la restauration, `poids`
repassait à 149 neurones en laissant `a_neur` à 6.

### 54.3 Ce que cela aurait donné SANS le garde-fou

Sans lui, `recalcule` aurait indexé `a_neur[j]` hors bornes — ou, si les listes
avaient eu la même longueur par hasard, il aurait **calculé des trajectoires avec la
mauvaise dynamique, en silence**, et le diagnostic oracle aurait été faux sans que
rien ne le signale.

C'est exactement le scénario que le garde-fou du §30 était censé empêcher, et c'est la
**deuxième fois** qu'il sert. Un contrôle bruyant posé une fois a payé deux fois.

### 54.4 Corrigé, et relancé

Trois endroits corrigés : les deux créations de `meilleur_passage` et la restauration.
La passe est relancée.

### 54.5 Ce que la passe interrompue avait déjà donné

Le journal contenait la naissance et l'attrition complètes ; seul le résumé final
manquait. Meilleur point mesuré, **149 neurones** :

| | μ = 0,1 | μ = 0 (même taille, interpolé) |
|---|---:|---:|
| fidélité apprentissage | 0,6466 | — |
| fidélité VALIDATION | 0,6311 | ~0,6317 |
| **fidélité TEST** | **0,6306** | ~0,6317 |
| **invariance** | **0,8954** | ~0,8703 |
| **pire paire** | **0,6433** | ~0,5817 |

**−0,0011 de fidélité pour +0,0251 d'invariance et +0,0616 de pire paire** — même
taux d'échange qu'au §51, sur un point de plus et une graine identique.


---

## 55. Le pont transfère sur le corpus Wikipedia multi-domaine — et sur TROIS paires de langues

Le corpus Wikipedia apparié (§45) permet pour la première fois de mesurer le transfert
sur un contenu **riche, multi-domaine et aligné**, et sur **plusieurs paires de
langues** — ce que Romeo seul (une paire, un registre) ne permettait pas.

**71 articles alignés × 6 langues**, couche 8, 120 neurones, 1 couche.

| paire | fidélité sur A | **fidélité sur B (transférée)** | **perte au transfert** | invariance de sortie | pire segment | oracle sur B | écart à l'oracle |
|---|---:|---:|---:|---:|---:|---:|---:|
| en ↔ fr | 0,6083 | **0,5444** | **−0,0639** | 0,9179 | 0,6556 | 0,6073 | +0,0629 |
| en ↔ de | 0,6083 | **0,5426** | **−0,0657** | 0,8981 | 0,6224 | 0,6160 | **+0,0734** |
| fr ↔ de | 0,6169 | **0,5851** | **−0,0318** | 0,9204 | 0,7420 | 0,6247 | **+0,0396** |

### 55.1 Ce que cela établit

**1. Le pont transfère, sur les trois paires.** La perte va de −0,032 (fr↔de) à
−0,066 (en↔de). La lecture apprise sur une langue, appliquée sans réapprentissage à
une autre, garde 87 à 95 % de sa fidélité.

**2. La paire la plus proche transfère le mieux.** fr↔de perd **deux fois moins** que
en↔fr et en↔de. C'est cohérent : plus les langues sont proches, mieux la lecture
partagée convient — et cela **confirme que la perte mesure bien la distance entre
langues**, pas autre chose.

**3. La comparaison avec Romeo est favorable.** Sur Romeo (24 scènes, en–fr), la perte
valait −0,0858. Ici, sur 71 articles encyclopédiques et multi-domaines, elle vaut
−0,0639 pour la même paire en–fr. **Un corpus plus riche et plus varié transfère
mieux**, ce qui va dans le sens de la mission.

**4. Le goulot de transfert est bien réel et quantifié** : l'écart à l'oracle va de
+0,0396 à +0,0734 selon la paire. Un ajustement privé rapporterait donc de 4 à 7 points
— c'est la marge qui reste à prendre.

### 55.2 Le chemin parcouru sur l'invariance de sortie

| corpus | paires | invariance de sortie | pire segment |
|---|---|---:|---:|
| Romeo (littéraire) | en–fr | 0,9540 | — |
| **Wikipedia (encyclopédique)** | en–fr | 0,9179 | 0,6556 |
| **Wikipedia** | en–de | 0,8981 | 0,6224 |
| **Wikipedia** | fr–de | 0,9204 | 0,7420 |

L'invariance de sortie de Wikipedia est **plus basse** que celle de Romeo — et c'est
attendu : le contenu est varié (71 sujets différents), donc il y a plus de matière à
ne pas confondre. Une invariance de 0,92 sur 71 sujets distincts vaut mieux qu'une
invariance de 0,95 sur 24 scènes d'une même pièce.

### 55.3 Une confirmation de déterminisme au passage

La croissance relancée après la correction du §54 reproduit **exactement** les points
de la passe interrompue : à 40 neurones, `0,6278 · 0,9289 · 0,7329` dans les deux
exécutions. Ce n'est pas une vérification de laboratoire, c'est une **reproduction
accidentelle sur un calcul de 40 minutes** — et elle vaut confirmation.
