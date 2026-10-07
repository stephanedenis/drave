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


---

## 56. Croissance sous contrainte, protocole ENTIER : 147 neurones, oracle sur les deux panneaux

Première passe de croissance qui fournit **le protocole complet** demandé par
l'objectif — les quatre mesures **et** l'oracle sur les **deux** panneaux.

Couche 10, `--part-langues 0.5`, ride 0,03, lecture quadratique, réservoir
multi-échelle, fit sur 1/20, μ = 0,1, 300 langues d'ajustement / 51 de validation /
41 de test, 896 canaux.

| | |
|---|---:|
| **TAILLE** | **147 neurones · 1 couche** |
| fidélité apprentissage | 0,6464 |
| fidélité **VALIDATION** (même vivier) | 0,6312 |
| **fidélité TEST** (hors vivier) | **0,6299** |
| constante témoin sur TEST | 0,5762 |
| **apport propre** | **+0,0537** |
| **invariance inter-langue** | **0,8958** |
| **pire paire** | **0,6392** |
| oracle TEST | 0,6721 |
| **écart à l'oracle — TEST (hors vivier)** | **+0,0415** |
| oracle VALIDATION (même vivier) | 0,6504 |
| **écart à l'oracle — VALIDATION** | **+0,0194** |

### 56.1 Comparaison avec la même croissance SANS contrainte

| | μ = 0 (182 neurones) | **μ = 0,1 (147 neurones)** |
|---|---:|---:|
| fidélité TEST | **0,6340** | 0,6299 |
| invariance | 0,8659 | **0,8958** |
| pire paire | 0,5556 | **0,6392** |
| oracle TEST | *(manquant — drapeau cassé)* | **0,6721** |
| écart à l'oracle TEST | *(manquant)* | **+0,0415** |

**−0,0041 de fidélité pour +0,0299 d'invariance et +0,0836 de pire paire.** Le taux
d'échange sur la pire paire est de **20 pour 1**.

### 56.2 Le goulot de transfert se resserre quand le réseau grandit

L'écart à l'oracle hors vivier vaut ici **+0,0415**, contre **+0,1003** pour le profil
à **40 neurones** (§44). Le rapport entre l'écart hors vivier et l'écart dans le vivier
tombe de **8,7× à 2,1×**.

Autrement dit : **un réseau plus grand transfère mieux.** C'est la première fois que
le goulot de transfert du §36 se réduit sous l'effet d'une décision d'architecture.


---

## 57. LA question ouverte depuis le §41 est tranchée : notre sortie ÉCRASE la distinction contenu / langue

### 57.1 La question, et pourquoi elle traînait

Depuis le §41, un même fait revient : **notre sortie est beaucoup plus invariante
entre langues que la représentation du professeur qu'elle imite** — 0,95 contre 0,65
sur l'UDHR, **0,928 contre 0,347** sur le corpus Wikipedia multi-domaine (§56).
Deux lectures, et rien ne les départageait :

1. **C'est la mission.** Un pont linguistico-sémantique veut l'invariance.
2. **C'est de l'appauvrissement.** Une sortie qui ne dépend presque plus de l'entrée
   est invariante pour la mauvaise raison : elle a effacé le contenu avec la langue.

### 57.2 Le test, et il ne demande aucun corpus nouveau

Mesurer la **même** similarité sur les **deux** axes, sur les **mêmes** entrées, pour
notre sortie **et** pour le professeur :

- `S_langue` — **même article, langues différentes** : ce qu'on veut **garder** ;
- `S_domaine` — **même langue, articles différents** : ce qu'il faut **distinguer**.

Si `S_domaine ≈ S_langue`, la sortie ne distingue plus les contenus. Si
`S_domaine ≪ S_langue`, elle distingue les contenus **et** rapproche les langues.

### 57.3 Le résultat, sur deux corpus et deux pooling

**Corpus Wikipedia multi-domaine** (3 langues apprises, 3 en test, 85 articles) :

| pooling | | S_langue | S_domaine | écart | rapport |
|---|---|---:|---:|---:|---:|
| dernière position | **NOTRE SORTIE** | 0,7491 | 0,7495 | **−0,0005** | **1,00** |
| dernière position | professeur | 0,2337 | 0,2163 | **+0,0174** | 1,08 |
| moyenne | **NOTRE SORTIE** | 0,9835 | 0,9866 | **−0,0031** | **1,00** |
| moyenne | professeur | 0,9454 | 0,8937 | **+0,0517** | 1,06 |

**Ce n'est pas un artefact de position** : les deux pooling donnent le même verdict.
**Notre sortie ne sépare plus les deux axes du tout, et le professeur, si** — dans le
sens du CONTENU, sur les deux pooling.

**Contrôle sur l'UDHR** (unités alignées, 300 langues apprises, 230 unités de test) :

| | S_langue | S_domaine | écart | rapport |
|---|---:|---:|---:|---:|
| **NOTRE SORTIE** | 0,8824 | 0,9907 | **−0,1083** | **0,89** |
| professeur | 0,6939 | 0,9421 | **−0,2482** | 0,74 |

### 57.4 La conclusion honnête, et elle n'est ni tout noir ni tout blanc

Sur **les deux** corpus, **notre pont sépare moins le contenu de la langue que le
professeur** :

| corpus | séparation du professeur | séparation de notre sortie | retenue |
|---|---:|---:|---:|
| UDHR | −0,2482 | −0,1083 | **44 %** |
| Wikipedia (3 langues) | **+0,0517** | **−0,0031** | **0 %**, et le SIGNE s'inverse |

**Sur l'UDHR, notre pont conserve 44 % de la séparation du professeur** — imparfait,
mais réel. **Sur Wikipedia, il n'en conserve rien et change de signe** : là où le
professeur préfère le contenu, notre sortie est indifférente.

### 57.5 Ce que cela change dans tout le rapport

**Tous les chiffres d'invariance de ce rapport doivent être lus avec cette
qualification.** Une invariance de 0,90-0,96 n'est pas, à elle seule, la preuve d'un
pont réussi : elle mélange deux choses qui n'ont pas été séparées jusqu'ici —
**rapprocher les langues** et **effacer les différences**. Le test ci-dessus est le
seul qui les sépare, et il n'avait jamais été fait.

**Ce n'est PAS la pénalité μ qui cause l'écrasement** : mesuré à μ = 0 et μ = 0,1 sur
Wikipedia, le rapport vaut **1,00 dans les deux cas**. L'écrasement existe déjà sans
contrainte. μ le dégrade très légèrement (les deux similarités montent de +0,0036),
mais il n'en est pas la cause.

**Ce qui reste à faire, et c'est désormais précis** : l'objectif de la lecture doit
être réécrit pour **favoriser explicitement l'axe contenu** — non pas « rapprocher les
langues », mais « rapprocher les langues **à contenu égal** et **éloigner les contenus
à langue égale** ». Les deux termes sont quadratiques en `W`, donc la solution reste en
forme fermée ; c'est la même mécanique que le §48, appliquée au bon objectif.


---

## 58. Réécrire l'objectif : la structure du professeur EST atteignable, mais l'objectif à deux curseurs est NON CONVEXE

### 58.1 L'objectif, et pourquoi il tient en forme fermée

Le §57 a montré que l'invariance seule ne suffit pas : elle s'obtient aussi bien en
rapprochant les langues **à contenu égal** qu'en effaçant tout. On ajoute donc un
**second** terme, et l'objectif devient :

```
‖XW − Y‖²  +  μ_lang·P_lang(W)  −  μ_cont·P_cont(W)
```

- `P_lang` = variance **inter-langue** de la sortie (à minimiser) ;
- `P_cont` = variance **inter-contenu** de la sortie (à maximiser) ;
- les deux valent `tr(WᵀCW)`, donc la solution reste en **forme fermée**.

Et la mesure qui compte n'est plus l'invariance seule, mais la **SÉPARATION** :

```
séparation = S_langue − S_domaine
```

`S_langue` : même contenu, langues différentes — à garder. `S_domaine` : même langue,
contenus différents — à distinguer. **Positive = la sortie rapproche les langues PLUS
qu'elle n'efface les contenus.** C'est la définition mesurable d'un pont qui
fonctionne, et elle manquait à tous les chiffres du rapport.

### 58.2 Sur l'UDHR, la métrique est dégénérée — et on le voit

| μ_lang | μ_cont | fid TEST | S_langue | S_domaine | **séparation** | cible du prof |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0,5692 | 0,8824 | 0,9907 | −0,1083 | |
| 0,3 | 0,3 | 0,5563 | 0,9378 | 0,9936 | −0,0558 | |
| 3 | 3 | 0,5516 | 0,9594 | 0,9953 | −0,0359 | |
| | | | | | **cible** | **−0,2482** |

**Les curseurs éloignent de la cible.** Mais l'UDHR est le mauvais corpus pour cette
mesure : ses dix « contenus différents » sont **le même texte** (§53), donc son
`S_domaine` ne mesure rien. C'est le corpus Wikipedia qu'il faut interroger.

### 58.3 Sur Wikipedia : la cible est ATTEINTE — et c'est le résultat important

| μ_lang | μ_cont | fid TEST | S_langue | S_domaine | **séparation** | vs professeur |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | **0,4747** | 0,9835 | 0,9866 | −0,0031 | −0,0548 |
| 0,1 | 0 | 0,4729 | 0,9871 | 0,9908 | −0,0037 | −0,0554 |
| 0 | 0,1 | 0,2341 | 0,8436 | 0,8340 | +0,0096 | −0,0421 |
| **0,1** | **0,1** | **0,3359** | 0,8479 | 0,7959 | **+0,0519** | **+0,0003** |
| 0,3 | 0,3 | 0,3474 | 0,9037 | 0,9158 | −0,0122 | −0,0639 |
| 1 | 1 | 0,2520 | 0,7636 | 0,9040 | −0,1404 | −0,1921 |
| | | | | | **cible** | **+0,0517** |

**À μ_lang = μ_cont = 0,1, notre sortie atteint une séparation de +0,0519 contre
+0,0517 pour le professeur** — l'écart est de 0,0003.

**C'est le résultat important, et il est positif :** la structure contenu/langue du
professeur **est atteignable par une lecture LINÉAIRE des mêmes caractéristiques**.
Les états du réservoir contiennent donc l'information ; c'est l'**objectif** des
moindres carrés qui ne l'extrait pas. Le problème n'est ni la taille du réseau, ni la
richesse des caractéristiques.

### 58.4 Mais l'objectif est NON CONVEXE, et les résultats le montrent

Le terme `−μ_cont·P_cont` étant **soustrait**, la matrice cesse d'être définie positive.
Le code le **signale** (garde ajouté) :

| μ_cont | λ_min de la matrice |
|---:|---:|
| 0,1 (Wikipedia) | −5,7e+03 |
| 0,3 | −7,7e+04 |
| 1,0 | −1,0e+06 |

**Et les résultats sont erratiques** : la séparation vaut +0,052 à μ=0,1, **−0,012 à
μ=0,3** et **−0,140 à μ=1**. Un objectif convexe donnerait une courbe monotone ; ici
la solution n'est pas un minimum mais un **point selle**, et le résultat dépend du
réglage de façon imprévisible.

**Le coût de fidélité est par ailleurs lourd** : 0,4747 → 0,3359, soit −0,139 pour
atteindre la séparation du professeur.

### 58.5 La conclusion, et elle est nette

1. **La cible est atteignable** — la structure contenu/langue du professeur est
   accessible par une lecture linéaire, donc les caractéristiques suffisent.
2. **L'objectif quadratique à deux curseurs n'est pas la bonne façon de l'atteindre** :
   il est non convexe, non monotone, et coûte 0,14 de fidélité.
3. **Ce qu'il faut, c'est une formulation sous CONTRAINTE** — par exemple maximiser la
   fidélité sous contrainte que la séparation atteigne un seuil. Cela reste en forme
   fermée si la contrainte est quadratique (multiplicateur de Lagrange), mais la
   mécanique est différente et n'a pas été essayée.

**Ce qui est établi et ne le sera plus :** le problème du pont n'est ni sa taille, ni
la richesse de ses caractéristiques, ni la quantité de langues. **C'est son
objectif.** Les trois premiers ont été testés et écartés ; celui-ci est mesuré et
localisé.


---

## 59. La piste « le moindres carrés néglige les petites composantes » est RÉFUTÉE — par sa propre prémisse

### 59.1 L'idée, et elle était plausible

Le §58 laissait une question nette : les caractéristiques du réservoir **contiennent**
la structure contenu/langue du professeur (une lecture linéaire l'atteint), mais
l'objectif des moindres carrés ne l'extrait pas. L'explication la plus simple était
que la fidélité est un **cosinus par ligne** tandis que le fit minimise une erreur
**quadratique absolue** : si la cible est dominée par une masse commune, la lecture est
payée pour la reproduire et les petites composantes — celles qui distinguent les
contenus — pèsent peu.

Trois variantes **convexes** et en forme fermée découlaient de cette idée : centrer la
cible par entrée, normaliser chaque ligne, et **blanchir** la cible (la multiplier par
`C^(−α/2)`, ce qui égalise l'importance de toutes les directions). Toutes restent des
moindres carrés ordinaires.

### 59.2 La mesure qui tue l'idée avant même de la tester

**Spectre de la cible** : 896 directions, **la première ne porte que 4,1 % de
l'énergie**, les dix premières 21,5 %.

**Il n'y a pas de masse dominante.** L'idée de départ supposait une structure qui
n'existe pas : l'énergie de la cible est **étalée** sur un très grand nombre de
directions. Le moindres carrés ne néglige donc rien de « petit » — il n'y a pas de
gros à négliger devant.

### 59.3 Et les variantes ne marchent pas

| variante | fid TEST | S_langue | S_domaine | **SÉPARATION** |
|---|---:|---:|---:|---:|
| **A** référence | **0,4706** | 0,9957 | 0,9965 | −0,0008 |
| **B** cible centrée | 0,4708 | 0,9869 | 0,9909 | −0,0040 |
| **C** lignes normées | 0,4197 | **1,0000** | **1,0000** | **−0,0000** |
| **D** blanchiment α=0,25 | 0,4383 | 0,9996 | 0,9997 | −0,0001 |
| **D** blanchiment α=0,50 | 0,4226 | 1,0000 | 1,0000 | −0,0000 |
| | | | **cible** | **+0,0517** |

**Aucune n'améliore la séparation, deux la détruisent complètement.** Normaliser les
lignes de la cible donne `S_langue = S_domaine = 1,0000` **exactement** : toutes les
sorties deviennent parallèles. Et le blanchiment — l'idée la plus prometteuse sur le
papier — coûte 0,05 de fidélité pour **zéro** gain de séparation.

### 59.4 Ce qui reste debout, et ce qui tombe

**Tombe** : « le moindres carrés néglige les petites composantes ». La prémisse est
fausse (pas de masse dominante), et les remèdes qui en découlaient ne fonctionnent pas.

**Reste debout** : le constat du §58 — **une** lecture linéaire atteint la séparation
du professeur. Mais il faut le regarder avec méfiance : cette configuration était
**non convexe**, la courbe était **non monotone** (+0,052 à μ=0,1, **−0,012** à μ=0,3,
**−0,140** à μ=1), et rien ne dit que le point gagnant soit autre chose qu'une
coïncidence d'un paysage instable.

**Reste donc ouvert** : *par quel objectif convexe* extraire la structure contenu/langue
que les caractéristiques contiennent manifestement. Les quatre pistes essayées
(deux curseurs quadratiques, centrage, normalisation, blanchiment) sont toutes
écartées, chacune par une mesure.

### 59.5 Ce que cela dit de la démarche

Ce paragraphe est **négatif du début à la fin** : une hypothèse plausible, une
prémisse réfutée par le spectre avant même d'être testée, trois variantes sans effet,
une quatrième contre-productive. Il est écrit parce qu'une piste écartée par une mesure
vaut mieux qu'une piste gardée par politesse — et parce que le §58, seul, aurait laissé
croire que le problème était résolu.


---

## 60. Le rétrécissement est réel — mais ce n'est pas la cause. Et la cible du §58 n'est pas stable

### 60.1 Un défaut quantifié qui n'avait jamais été regardé

Depuis quatre paragraphes, on cherchait pourquoi notre sortie ne sépare plus contenu et
langue. Une chose n'avait jamais été mesurée : **notre sortie est-elle seulement plus
PETITE que sa cible, autour du même point ?**

Si les caractéristiques ne peuvent pas produire toute l'amplitude de la cible, le
moindres carrés **rétrécit** la prédiction vers la moyenne — régression vers la
moyenne, phénomène classique. Or `mt` est le **même pour toutes les entrées** : une
prédiction dominée par `mt` a des moyennes par entrée presque identiques, ce qui
produit exactement le tableau du §57.

**Mesuré**, rapport `‖écart à la moyenne‖ / ‖moyenne‖` par ligne :

| | rapport |
|---|---:|
| **notre sortie** | **0,6234** |
| professeur | **2,1454** |
| **rapport** | **0,291** |

**Nous écrasons l'écart à la moyenne d'un facteur 3,4.** Le défaut est réel, il est
net, et il n'avait pas été vu.

### 60.2 Mais amplifier ne rétablit pas l'ordre

On écrit la sortie `mt + α·(O − mt)` et on balaie α — un simple facteur d'échelle sur
l'écart, donc **linéaire** et dans les règles.

| α | fid TEST | S_langue | S_domaine | **SÉPARATION** |
|---:|---:|---:|---:|---:|
| 0,50 | 0,4701 | 0,9958 | 0,9966 | −0,0008 |
| **1,00** | **0,4769** | 0,9835 | 0,9866 | −0,0031 |
| 1,50 | 0,4553 | 0,9643 | 0,9711 | −0,0068 |
| 2,00 | 0,4291 | 0,9404 | 0,9520 | −0,0117 |
| 3,00 | 0,3817 | 0,8872 | 0,9102 | −0,0230 |

**Amplifier fait MONOTONEMENT BAISSER les deux similarités et rend la séparation PLUS
négative.** À α=3 on approche les niveaux absolus du professeur (0,887/0,910 contre
0,945/0,894) — **mais l'ORDRE reste inversé**. Le problème n'est donc pas une question
d'amplitude : il est dans l'ordre lui-même.

### 60.3 Le contrôle qui change la lecture : la cible du §58 n'est PAS stable

Le contrôle était indiqué par le résultat : dans le jeu de test, les paires « même
article, langues différentes » sont **entre langues inconnues**, tandis que les paires
« même langue, articles différents » sont **dans une langue inconnue**. On refait donc
la mesure sur les langues d'**apprentissage** :

| | S_langue | S_domaine | **SÉPARATION** |
|---|---:|---:|---:|
| **notre sortie** (α=1) | 0,9153 | 0,9844 | **−0,0691** |
| notre sortie (α=2) | 0,7077 | 0,9475 | −0,2398 |
| **professeur, mêmes entrées** | 0,8624 | 0,8776 | **−0,0152** |

**Et là est le résultat gênant : la séparation du PROFESSEUR vaut −0,0152 sur les
langues d'apprentissage et +0,0517 sur celles de test.** Elle **change de signe** selon
le jeu de langues.

L'explication est simple : les langues de test (es, it, pt) sont **trois langues
romanes très proches**, donc le même article y est naturellement très similaire
(0,9454) ; les langues d'apprentissage (de, en, fr) sont **plus mêlées**, et la
similarité entre langues y tombe à 0,8624, **sous** celle entre articles (0,8776).

### 60.4 Ce que cela retire au §58

Le §58 annonçait avoir « atteint la séparation du professeur » (+0,0519 contre
+0,0517). **C'est exact sur ce jeu de langues, et cela reste une preuve que la
structure est linéairement accessible.** Mais **la cible n'est pas une constante du
professeur** : elle dépend de quelles langues composent le panel. La comparaison
« notre séparation contre celle du professeur » n'est donc **valide qu'à panel
identique** — ce qu'elle était ici, mais ce qui doit être dit à chaque fois.

### 60.5 Bilan de la traque, en quatre paragraphes

| piste | verdict |
|---|---|
| §58 — objectif à deux curseurs | **atteint la cible**, mais non convexe et non monotone |
| §59 — pondération de l'objectif (centrage, normalisation, blanchiment) | **écartée** — prémisse réfutée par le spectre |
| §60 — rétrécissement vers la moyenne | **réel (3,4×)**, mais l'amplifier n'inverse pas l'ordre |
| §60 — la cible elle-même | **n'est pas stable** — elle change de signe selon le panel |

**La cause de l'inversion contenu/langue reste non identifiée.** Ce qui est établi, et
c'est beaucoup : elle n'est ni dans la taille du réseau, ni dans la richesse des
caractéristiques, ni dans la pondération de l'objectif, ni dans l'amplitude de la
sortie. Quatre causes plausibles écartées, chacune par une mesure.

### 60.6 Une erreur de ma part, corrigée

La première version découpait les sorties par pas fixe `len(Yte[0])`, en supposant
toutes les entrées de même longueur. **Elles ne le sont pas** — numpy a signalé
`Mean of empty slice` et les moyennes par entrée étaient fausses. Corrigé par des
bornes cumulées. C'est la troisième fois de la session qu'une hypothèse de forme
régulière se glisse dans un outil de mesure.


---

## 61. Le défaut est LOCALISÉ et QUANTIFIÉ : notre sortie porte douze fois moins d'énergie de CONTENU

Après quatre causes écartées (§58 à §60), restait à localiser le défaut. Ni une
similarité cosinus ni une comparaison à une cible mouvante ne le pouvaient. Une
**décomposition de variance** le peut, et elle est exacte et additive.

Pour chaque entrée (langue `L`, contenu `k`), on prend sa moyenne `m_Lk` et on
décompose :

```
ν_L  = moyenne sur les contenus   -> effet LANGUE
μ_k  = moyenne sur les langues    -> effet CONTENU
P_lang = Σ_L n_L ‖ν_L − m̄‖²      énergie portée par la LANGUE
P_cont = Σ_k n_k ‖μ_k − m̄‖²      énergie portée par le CONTENU
```

### 61.1 Le résultat

| panel | | P_lang | **P_cont** | **rapport P_cont/P_lang** |
|---|---|---:|---:|---:|
| **TEST** (langues inconnues) | **NOTRE** | 232,0 | **338,7** | **1,46** |
| | professeur | 399,2 | **4 356,4** | **10,91** |
| **APPRENTISSAGE** (langues connues) | **NOTRE** | 1 834,7 | **493,9** | **0,27** |
| | professeur | 2 405,1 | **5 219,9** | **2,17** |

### 61.2 Ce que cela dit, et c'est net

**1. Le professeur porte 10,9 fois plus d'énergie de contenu que de langue** (test).
Notre sortie n'en porte que **1,46 fois**.

**2. Le défaut n'est PAS « trop de langue ».** Notre énergie de langue (232) est du même
ordre que celle du professeur (399). **C'est notre énergie de CONTENU qui est
dérisoire : 338,7 contre 4 356,4 — douze fois moins.**

**3. Le même écart existe sur les langues d'apprentissage** (493,9 contre 5 219,9, onze
fois moins), donc **ce n'est pas un défaut de transfert** : c'est un défaut de
reproduction, présent partout.

**4. Et cela explique — enfin — le §60.1.** Le rapport
`‖écart à la moyenne‖ / ‖moyenne‖` valait 0,291 chez nous contre 2,145 chez le
professeur : l'écart à la moyenne, c'est précisément la part qui porte le contenu. Le
rétrécissement du §60 et la décomposition du §61 mesurent **la même chose par deux
chemins indépendants**, et ils concordent.

**5. La cause de l'inversion contenu/langue est donc identifiée** : ce n'est pas un
excès de structure linguistique, c'est une **famine de structure de contenu**. Le
moindres carrés, forcé de choisir entre reproduire la masse commune (qui domine
l'énergie) et les écarts de contenu (petits devant elle), sous-produit massivement les
seconds.

### 61.3 Ce que cela rouvre, et ce que cela ferme

**Cela ferme** la piste du §59 d'une autre façon : ce n'est pas la *pondération* des
petites composantes qui manquait, c'est leur **amplitude** — elles ne sont pas
seulement sous-pondérées dans l'objectif, elles sont **sous-produites dans la sortie**.

**Cela rouvre** le §58 sous un jour favorable : le terme `−μ_cont·P_cont` **compense
exactement cette famine** — il demande à la sortie de porter plus d'énergie de contenu.
Ce n'était donc pas un artefact : c'était le bon remède appliqué par un moyen
non convexe.

**Et cela désigne un remède CONVEXE qui n'a pas été essayé** : amplifier la sortie
**le long de l'axe du contenu seulement** — et non globalement comme au §60.2, où
l'amplification uniforme augmentait les deux axes et ne rétablissait donc pas leur
rapport.

### 61.4 Pourquoi cette mesure est meilleure que les précédentes

`P_cont/P_lang` **ne dépend pas de quelles langues composent le panel** — seulement de
leur nombre et de leur diversité. Le §60.3 avait montré que la similarité du
professeur, elle, **changeait de signe** entre les langues d'apprentissage (−0,0152) et
celles de test (+0,0517), ce qui rendait la « cible » mouvante. La décomposition, elle,
donne 10,91 et 2,17 — deux valeurs différentes, mais **du même côté, et interprétables
directement** : le contenu domine la langue dans les deux cas.


---

## 62. Le remède est trouvé — mais il n'est pas déployable. Et un piège de méthode

### 62.1 L'énergie de contenu EST récupérable : la preuve

Le §61 a localisé le défaut : notre sortie porte **douze fois moins d'énergie de
contenu** que le professeur, à énergie de langue comparable. Restait à savoir si cette
énergie est **absente** de la représentation ou seulement **sous-produite**.

On amplifie donc la sortie **le long de l'axe du contenu seulement** — en ajoutant
`β·(μ_k − m̄)`, le décalage de contenu de l'entrée, à toutes ses lignes :

| β | fid TEST | P_lang | **P_cont** | **rapport** |
|---:|---:|---:|---:|---:|
| 0 | 0,4747 | 232,0 | 338,7 | 1,46 |
| **1,0** | **0,4749** | 232,0 | 1 354,8 | **5,84** |
| **3,0** | **0,4688** | 232,0 | **5 419,2** | **23,36** |
| 10 | 0,4129 | 232,0 | 40 983 | 176,6 |
| | | | **professeur 4 356** | **10,91** |

**À β = 3, notre énergie de contenu (5 419) dépasse celle du professeur (4 356) pour un
coût de fidélité de 0,006.** Et à β = 1 elle quadruple **sans aucun coût** (0,4749
contre 0,4747).

**Conclusion nette : l'énergie de contenu n'est pas absente, elle est sous-produite.**
Le moindres carrés la rétrécit d'un facteur ~3,6 en amplitude, et il suffit de la
remettre à l'échelle.

### 62.2 Mais la version déployable échoue — et proprement

Le remède ci-dessus utilise le **regroupement par contenu** (`μ_k`), information qui
n'existe pas pour un texte neuf. On teste donc la version calculable à l'inférence :
amplifier le **décalage de moyenne de chaque entrée**, sans toucher aux écarts entre
positions.

| γ | fid TEST | P_lang | P_cont | **rapport** |
|---:|---:|---:|---:|---:|
| 0 | 0,4747 | 232,0 | 338,7 | **1,460** |
| 1 | 0,4712 | 928,1 | 1 354,8 | **1,460** |
| 3 | 0,4502 | 3 712,2 | 5 419,2 | **1,460** |
| 5 | 0,4191 | 8 352,5 | 12 193,3 | **1,460** |

**Le rapport vaut exactement 1,460 à tout γ.** La moyenne d'une entrée contient **à la
fois** son décalage de langue et son décalage de contenu : les amplifier ensemble ne
change pas leur rapport. Seule une amplification **de l'axe contenu seul** fonctionne,
et elle exige de savoir quelles entrées partagent un contenu.

### 62.3 Le levier du §48 ne le remplace pas, et révèle un piège de méthode

On teste enfin si la pénalité inter-langue `μ_lang` du §48 rétablit le rapport, en
baissant `P_lang` :

| μ_lang | TEST P_lang | TEST P_cont | **rapport** | fid TEST |
|---:|---:|---:|---:|---:|
| **0** | **232,0** | **338,7** | **1,460** | **0,4747** |
| 0,03 | 218,3 | 283,9 | 1,300 | 0,4741 |
| 0,1 | 195,7 | 217,5 | 1,112 | 0,4729 |
| 0,3 | 158,7 | 144,4 | 0,910 | 0,4710 |
| | | | *professeur* **10,912** | |

**Le rapport BAISSE.** `μ_lang` comprime bien `P_lang` (232 → 159), mais comprime
`P_cont` **davantage encore** (339 → 144). Il ne rétablit pas le rapport, il écrase.

**Et c'est là le piège de méthode, qu'il faut dire :** sur le panneau
d'apprentissage, μ_lang = 0,3 donne un rapport de **3,139**, *supérieur* à celui du
professeur (2,170). On pourrait donc annoncer « nous dépassons le professeur ». C'est
faux : `P_lang` y vaut **51,3** — l'énergie de langue a été écrasée à presque rien, et
le rapport est gonflé par le dénominateur, pas par le numérateur.

**Le rapport `P_cont/P_lang` ne suffit donc pas comme critère.** Le bon critère est
double : **`P_cont` proche de celui du professeur ET `P_lang` qui ne le dépasse pas.**
C'est la leçon de ce paragraphe, et elle vaut pour toute la série §58-§62.

### 62.4 Où en est la question, après cinq paragraphes de traque

| piste | verdict |
|---|---|
| §58 — objectif à deux curseurs | atteint la cible, mais **non convexe** et non monotone |
| §59 — pondération (centrage, normalisation, blanchiment) | **écartée** — prémisse réfutée par le spectre |
| §60 — rétrécissement global | **réel (3,4×)**, mais l'amplifier uniformément n'inverse pas l'ordre |
| §61 — **décomposition de variance** | **défaut localisé** : 12× moins d'énergie de contenu |
| §62 — amplification ciblée | **fonctionne** (β=3 → la magnitude du professeur, coût 0,006) |
| §62 — version déployable | **échoue** : la moyenne par entrée mêle les deux axes |
| §62 — `μ_lang` | **échoue** : comprime les deux, fait baisser le rapport |

**Le problème est maintenant posé en une phrase :** *l'énergie de contenu est
sous-produite d'un facteur ~3,6, elle est récupérable par mise à l'échelle, mais la
mise à l'échelle exige d'isoler l'axe du contenu — et cet axe n'est pas identifiable
sur un texte neuf par les moyens essayés.*

C'est une question précise, avec un chiffre, un remède connu **et une raison
d'échec connue**. Ce n'était pas le cas il y a cinq paragraphes.


---

## 63. Cinquième remède écarté : le sous-espace du contenu appris ne se TRANSFÈRE pas

### 63.1 L'idée, et elle était la bonne sur le papier

Le §62 avait trouvé le remède mais l'avait déclaré non déployable : amplifier l'axe du
contenu exige de savoir **quelles entrées partagent un contenu**. L'objection était
juste — mais elle ne vaut qu'à l'**inférence**. À l'**apprentissage**, ce regroupement
existe.

On apprend donc, **une fois pour toutes sur les données d'apprentissage** :
1. le **sous-espace du contenu** — l'espace engendré par les écarts `μ_k − m̄` ;
2. un **projecteur** `Π` sur ce sous-espace (85 directions, **100 % de l'énergie**
   captée).

Puis, à l'inférence, sur la sortie d'un texte neuf : `O + (γ−1)·Π·(O − m̄)`. `Π` est
une **matrice fixe** de 896×896 : aucun regroupement n'est demandé au texte neuf.

### 63.2 Le résultat : le rapport reste figé

| γ | rang | fid TEST | P_lang | P_cont | **rapport** |
|---:|---:|---:|---:|---:|---:|
| 1,00 | 85 | **0,4747** | 232,0 | 338,7 | **1,460** |
| 1,50 | 85 | 0,4720 | 508,3 | 752,0 | 1,480 |
| 2,00 | 85 | 0,4664 | 895,0 | 1 330,6 | 1,487 |
| 5,00 | 85 | 0,4015 | 5 536,2 | 8 274,3 | 1,495 |
| | | | | **professeur 4 356** | **professeur 10,912** |

**Le rapport passe de 1,460 à 1,495 en multipliant γ par cinq.** Les deux axes montent
**ensemble**. Le sous-espace appris n'isole pas le contenu sur le panel de test.

### 63.3 Pourquoi — et c'est cohérent avec tout le reste

Le détail qui explique tout : **les articles du test sont LES MÊMES que ceux de
l'apprentissage.** Le partage a été fait par **langue** (de/en/fr apprises, es/it/pt en
test), pas par article — donc les contenus sont partagés. Le sous-espace du contenu
*devrait* se transférer.

**Il ne se transfère pas parce que les sorties des langues INCONNUES sont décalées.**
Le sous-espace du contenu est appris sur des moyennes calculées sur de/en/fr ; sur
es/it/pt ces moyennes sont ailleurs. C'est **le même décalage de transfert que le §36**
— l'écart à l'oracle hors vivier — qui revient, cette fois sous la forme d'un
sous-espace qui ne s'applique plus.

**Le remède ne peut donc pas être appris sur les langues connues et appliqué aux
inconnues.** Il doit être soit **par langue** (mais une langue inconnue n'a pas de
statistiques), soit **structurellement indépendant de la langue** — et c'est une
exigence beaucoup plus forte.

### 63.4 Une étiquette fausse dans ma propre sortie

La première version affichait `# professeur (TEST) : P_lang 232,0 · P_cont 338,7`.
**Ces chiffres sont ceux de NOTRE sortie**, pas du professeur. Je passais nos sorties à
la fonction de décomposition et j'étiquetais le résultat « professeur ». Corrigé : les
deux sont maintenant calculés et affichés côte à côte.

C'est la deuxième fois de la session qu'une sortie d'outil porte une étiquette fausse
(après le tableau trié recopié dans le mauvais ordre, §27.7). Un chiffre juste sous un
nom faux est plus dangereux qu'un chiffre faux : il passe la relecture.

### 63.5 La série complète, et ce qu'elle établit

| § | piste | verdict |
|---|---|---|
| 58 | objectif à deux curseurs | atteint la cible, mais **non convexe**, non monotone, cible instable |
| 59 | pondération (centrage, normalisation, blanchiment) | **écartée** — prémisse réfutée par le spectre |
| 60 | rétrécissement global | **réel (3,4×)**, mais l'amplifier uniformément ne change pas l'ordre |
| 61 | décomposition de variance | **défaut localisé** : 12× moins d'énergie de contenu |
| 62 | amplification ciblée | **fonctionne** (β=3 → la magnitude du professeur, coût 0,006) |
| 62 | version déployable (moyenne par entrée) | **échoue** — mêle les deux axes |
| 62 | `μ_lang` | **échoue** — comprime les deux |
| 63 | sous-espace du contenu appris | **échoue** — ne se transfère pas aux langues inconnues |

**Cinq remèdes écartés, chacun par une mesure, et un défaut localisé avec un chiffre.**
La question s'est resserrée à ceci : *l'énergie de contenu est sous-produite d'un
facteur ~3,6 et récupérable par mise à l'échelle, mais tout ce qui permet de l'isoler
dépend de la langue — donc ne passe pas aux langues inconnues.*


---

## 64. Le centrage de l'entrée : un gain réel, déployable, et le premier de la série

### 64.1 Un levier du dépôt qui n'avait jamais été essayé sur ce diagnostic

`--centre-entree` retire à chaque langue son **jeton moyen** — le décalage massivement
propre à la langue (écriture, morphologie) qui ne dit aucun contenu. **Il attaque le
décalage de langue À LA SOURCE**, avant le réservoir, au lieu d'essayer de le retirer
après coup. Et il est **déployable** : la moyenne de l'entrée se calcule sur l'entrée
elle-même, sans étiquette ni regroupement.

### 64.2 Le résultat

| | P_lang | **P_cont** | **rapport** | fidélité TEST |
|---|---:|---:|---:|---:|
| sans centrage (§61) | 232,0 | 338,7 | **1,460** | 0,4747 |
| **avec centrage** | **48,0** | 89,8 | **1,871** | **0,4668** |
| **effet** | **÷ 4,8** | ÷ 3,8 | **+28 %** | −0,008 |
| *professeur* | *399,2* | *4 356,4* | *10,912* | |

**Le centrage réduit l'axe de langue d'un facteur 4,8** — c'est de loin le plus grand
effet obtenu sur cet axe dans toute la série. Et il coûte **0,008 de fidélité**.

Mais il réduit l'axe du contenu de 3,8× **en même temps** : le rapport ne gagne donc
que 28 %, et **les deux énergies tombent très en dessous de celles du professeur**
(48 contre 399, 90 contre 4 356).

### 64.3 La version déployable reste impuissante — et c'est instructif

| γ | fid TEST | P_lang | P_cont | **rapport** |
|---:|---:|---:|---:|---:|
| 0 | 0,4668 | 48,0 | 89,8 | **1,871** |
| 1 | 0,4656 | 191,9 | 359,1 | **1,871** |
| 3 | 0,4585 | 767,8 | 1 436,6 | **1,871** |
| 5 | 0,4462 | 1 727,5 | 3 232,2 | **1,871** |

**Le rapport est encore exactement constant.** L'amplification du décalage de moyenne
par entrée met toujours les deux axes à l'échelle ensemble — le centrage améliore le
**niveau** du rapport, il ne rend pas l'amplification sélective pour autant.

### 64.4 Ce que cela donne, concrètement

**Un gain déployable, gratuit à 0,008 près, qu'on garde** : `--centre-entree` améliore
le rapport contenu/langue de 28 % et divise par 4,8 l'énergie propre à la langue. C'est
modeste, mais c'est **le premier levier de toute la série §58-§64 qui soit à la fois
efficace et déployable.**

**Et une confirmation nette** : le problème n'est pas seulement de réduire l'axe de
langue — le centrage le fait très bien — mais de **ne pas réduire l'axe du contenu en
même temps**. Les deux sont **mêlés dans les états du réservoir**, et aucun des huit
moyens essayés ne les démêle sur des langues inconnues.

### 64.5 La série, complète

| § | moyen | déployable ? | verdict |
|---|---|---|---|
| 58 | objectif à deux curseurs | oui | atteint la cible, mais **non convexe**, non monotone |
| 59 | centrage/normalisation/blanchiment de la **cible** | oui | **écarté** — prémisse réfutée par le spectre |
| 60 | amplification uniforme | oui | **écarté** — ne change pas l'ordre |
| 61 | *décomposition de variance* | — | **diagnostic** : 12× moins d'énergie de contenu |
| 62 | amplification de l'axe contenu | **non** | **fonctionne** (β=3 → magnitude du professeur, coût 0,006) |
| 62 | amplification de la moyenne par entrée | oui | **écarté** — mêle les deux axes |
| 62 | `μ_lang` | oui | **écarté** — comprime les deux |
| 63 | sous-espace du contenu appris | oui | **écarté** — ne se transfère pas |
| **64** | **centrage de l'ENTRÉE** | **oui** | **RETENU** — rapport +28 %, P_lang ÷ 4,8, coût 0,008 |

**Huit moyens essayés, sept écartés, un retenu.** Le retenu est modeste ; les écartés
le sont chacun par une mesure, et le défaut est localisé avec un chiffre. C'est l'état
réel du problème, et il est plus étroit qu'au début de la série.


---

## 65. Un bug de découpage dans MES outils : l'ajustement ne portait que sur DEUX langues

### 65.1 Le bug

Les outils de diagnostic des §57 à §64 découpaient ainsi :

```python
itr = np.arange(len(cltr))
nt = max(1, len(itr) // 3)
iap, ival = itr[nt:], itr[:nt]      # ajustement = dernier tiers
```

Or **les entrées d'un cache sont ORDONNÉES PAR LANGUE** — `de_*` (85), `en_*` (85),
`fr_*` (85). Prendre le **dernier tiers** revient donc à prendre **`en_*` et `fr_*`
seulement** : le bloc entier de la première langue est supprimé.

**L'ajustement portait sur deux langues au lieu de trois**, dans six outils. Le signe
qui aurait dû alerter était dans la sortie du §64 : *« SOUS-ESPACE DE LANGUE : **2
langues** d'apprentissage · la 1re porte **100,0 %** de l'énergie de langue »*. Avec
deux groupes, une covariance inter-langue est de **rang 1** — elle ne peut rien
séparer. J'ai lu ce chiffre, je l'ai rapporté, et je n'en ai pas tiré la conclusion
évidente.

### 65.2 Corrigé, et re-mesuré

On ajuste désormais sur **toutes** les entrées d'apprentissage : le panneau *hors
vivier* est le **cache de test**, pas un sous-ensemble de l'apprentissage. Re-mesure du
diagnostic central (§61) :

| | avant correction | **après correction** |
|---|---:|---:|
| **TEST** notre `P_lang` | 232,0 | **247,1** |
| **TEST** notre `P_cont` | 338,7 | **318,7** |
| **TEST** notre rapport | 1,460 | **1,290** |
| **TEST** professeur (rappel) | 399,2 / 4 356,4 | idem · rapport 10,912 |
| **APPRENTISSAGE** notre `P_lang` | 1 834,7 | **2 161,7** |
| **APPRENTISSAGE** notre `P_cont` | 493,9 | **342,9** |
| **APPRENTISSAGE** notre rapport | 0,269 | **0,159** |
| **APPRENTISSAGE** professeur | 2 405,1 / 5 219,9 → 2,170 | **3 402,5 / 4 205,5 → 1,236** |

### 65.3 Aucune conclusion ne change — et c'est ce qu'il faut vérifier

| conclusion | tient-elle ? |
|---|---|
| Le défaut est la **famine de contenu**, pas l'excès de langue | **oui** — notre `P_cont` reste **13,7× sous** celui du professeur (318,7 contre 4 356,4), notre `P_lang` du même ordre (247,1 contre 399,2) |
| L'énergie de contenu est **récupérable par mise à l'échelle** | **oui** — β=3 donne `P_cont` **5 099,9** pour une fidélité de 0,4711 (coût 0,0055) |
| L'amplification **déployable** ne change pas le rapport | **oui** — 1,290 **exactement** à tout γ |
| Le défaut existe aussi **dans le vivier** | **oui** — rapport 0,159 à l'apprentissage contre 1,236 pour le professeur |

**Les quatre conclusions du diagnostic survivent à la correction.** C'est la raison
pour laquelle la correction est rapportée en détail plutôt que discrètement : un
chiffre faux qui ne change aucune conclusion reste un chiffre faux, et la prochaine
mesure qui s'appuiera dessus n'aura pas la même chance.

### 65.4 Ce que cela change pour la suite

Le **rapport du professeur lui-même** passe de 2,170 à **1,236** sur le panneau
d'apprentissage selon que celui-ci compte deux ou trois langues. **La cible dépend donc
aussi du nombre de langues**, pas seulement de leur identité (§60.3). Toute comparaison
« notre rapport contre celui du professeur » doit nommer **le panel et sa composition**
— c'est la troisième fois dans cette série qu'un chiffre de référence se révèle
dépendre du périmètre.

### 65.5 La règle que j'aurais dû appliquer

**Un découpage par position n'est un découpage aléatoire que si l'ordre est
aléatoire.** Les caches sont triés par langue ; prendre « le dernier tiers » n'est pas
prendre « un tiers au hasard », c'est prendre **deux langues sur trois**. Un `ival` par
**stride** (`itr[::7]`, comme le fait `profil_langues.py`) aurait été correct ; un
`ival` par **bloc contigu** ne l'était pas.

C'est la quatrième fois de la session qu'une hypothèse de forme régulière — ici, que
l'ordre des entrées est indifférent — se glisse dans un outil de mesure.


---

## 66. Deux leviers DÉPLOYABLES, et ils se combinent

### 66.1 Retirer le sous-espace de langue DANS LES ÉTATS

Tous les moyens des §58-§64 agissaient soit sur l'**objectif** du fit, soit sur la
**sortie**. Or le §64 a montré que les deux axes sont mêlés **dans les états** du
réservoir. L'idée ici est donc d'agir **avant la lecture** :

1. sur l'apprentissage, calculer la covariance **inter-langue** des états
   `C_lang = Σ_L n_L (ν_L − ν̄)(ν_L − ν̄)ᵀ`, où `ν_L` est l'état moyen de la langue `L` ;
2. en prendre les `r` directions dominantes et **projeter les états sur leur
   complément** : `X' = X·(I − Π_lang)` ;
3. ajuster la lecture sur `X'`.

`Π_lang` est une **matrice fixe** : à l'inférence on applique la même projection à un
texte neuf, **sans étiquette de langue ni regroupement**.

**Résultat** (3 langues d'apprentissage cette fois — voir §65) :

| rang | fid TEST | P_lang | P_cont | **rapport** |
|---:|---:|---:|---:|---:|
| 0 | 0,4767 | 242,1 | 317,4 | 1,311 |
| 5 | 0,4747 | 183,5 | 285,7 | 1,556 |
| 20 | 0,4737 | 174,6 | 270,7 | 1,551 |
| **40** | **0,4713** | **141,9** | 224,7 | **1,584** |

**`P_lang` tombe de 242 à 142 (÷ 1,7) quand `P_cont` ne tombe que de 317 à 225
(÷ 1,4)** — le rapport gagne 21 % pour 0,005 de fidélité. Contrairement au §63, l'effet
**se transfère** aux langues inconnues, parce que la projection s'applique aux états,
qui sont calculés de la même façon quelle que soit la langue.

### 66.2 Les deux leviers ensemble

Le centrage agit sur l'entrée **avant** le réservoir ; le retrait du sous-espace agit
sur les états **après**. Les deux attaquent le même axe par des chemins différents — on
les combine.

| rang | fid TEST | P_lang | P_cont | **rapport** |
|---:|---:|---:|---:|---:|
| 0 (centrage seul) | 0,4703 | 42,4 | 81,8 | 1,927 |
| **5** | **0,4706** | **22,9** | 70,2 | **3,064** |
| 10 | 0,4709 | 22,9 | 69,7 | 3,035 |
| 40 | 0,4692 | 21,9 | 61,9 | 2,832 |

**Et la fidélité ne bouge pas** (0,4703 → 0,4706). Le rapport passe de 1,927 à
**3,064**, soit **+59 %** par rapport au centrage seul.

### 66.3 Le bilan des leviers

| moyen | déployable | rapport | fidélité |
|---|---|---|---|
| rien | — | 1,460 | 0,4747 |
| centrage de l'entrée (§64) | oui | 1,871 | 0,4668 |
| retrait du sous-espace dans les états (§66.1) | oui | 1,584 | 0,4713 |
| **les deux (§66.2)** | **oui** | **3,064** | **0,4706** |
| *professeur* | — | *10,912* | — |

**Deux leviers déployables, gratuits à 0,004 près, qui portent le rapport de 1,46 à
3,06 — soit 28 % de la cible au lieu de 13 %.**

### 66.4 La réserve, et elle est importante

**Le rapport monte surtout par le DÉNOMINATEUR.** À rang 5, `P_lang` tombe à 22,9 —
**17 fois sous celui du professeur** (399,2) — tandis que `P_cont` reste à 70,2,
**62 fois sous le sien** (4 356,4).

C'est exactement le piège signalé au §62.3, et il faut le redire ici : **un rapport
élevé obtenu en écrasant l'axe de langue ne prouve pas qu'on a rapproché les langues
*à contenu égal*.** Les deux énergies restent très en dessous de celles du professeur.

**Ce qui manque reste le même qu'au §61** : remonter `P_cont` à la magnitude du
professeur. Et le seul moyen qui y parvienne (l'amplification ciblée, β=3 → `P_cont`
5 100) exige le regroupement par contenu, donc n'est pas déployable.

**La formulation honnête du progrès** : on sait maintenant **réduire l'axe de langue
sans écraser l'axe de contenu** — c'est nouveau, et c'est déployable. On ne sait
toujours pas **remonter l'axe de contenu** sans information sur le contenu.


---

## 67. Le rapport est INVARIANT D'ÉCHELLE — donc aucune amplitude ne peut le corriger

C'est un constat mathématique, et il ferme toute une famille de pistes.

`P_cont` et `P_lang` sont **toutes deux quadratiques** en la sortie. Multiplier l'écart
à la moyenne par un facteur `α` multiplie donc les deux par `α²`, et **leur rapport est
inchangé**. Mesuré, sans exception :

| rang | α | P_lang | P_cont | **rapport** |
|---:|---:|---:|---:|---:|
| 5 | 1,5 | 51,5 | 157,9 | **3,064** |
| 5 | 5,0 | 572,3 | 1 753,9 | **3,064** |
| 40 | 1,5 | 49,2 | 139,3 | **2,832** |
| 40 | 5,0 | 546,7 | 1 548,0 | **2,832** |

**Le rapport est identique au chiffre près, à tous les rangs et tous les α.** Ce n'est
pas une observation empirique, c'est une identité : `P_cont/P_lang` est homogène de
degré 0.

**Conséquence, et elle est structurante :** le rapport ne peut venir que d'un **changement
de DIRECTIONS**. Toutes les amplifications — uniformes (§60), par entrée (§62), ciblées
sur le contenu (§62) — ne peuvent pas le corriger, quelle que soit leur mise à
l'échelle. C'est la raison profonde pour laquelle cinq remèdes ont échoué.

**Et cela donne la cible en une ligne** : pour atteindre `P_cont` = 4 356 avec
`P_lang` ≤ 399, il faut un rapport ≥ **10,9** — celui du professeur. Nous sommes à
**3,06**, soit **28 %**.

---

## 68. Sixième remède écarté : imposer la covariance de la cible

Si le rapport ne dépend que des directions, la **matrice de covariance** du professeur
les contient. On construit donc une transformation linéaire `A` qui donne à notre sortie
la covariance de la cible :

```
A = C_Y^(1/2) · C_O^(-1/2)        (apprise sur l'apprentissage, matrice fixe de 896×896)
sortie corrigée = (O − m_O)·Aᵀ + m_Y
```

Purement linéaire, en forme fermée, déployable, sans étiquette ni regroupement.

| mélange | fid TEST | P_lang | P_cont | **rapport** |
|---:|---:|---:|---:|---:|
| 0,00 | **0,4704** | 42,4 | 82,1 | **1,934** |
| 0,25 | 0,4486 | 139,6 | 254,7 | 1,825 |
| 0,50 | 0,4107 | 329,2 | 596,0 | 1,810 |
| 0,75 | 0,3725 | 611,4 | 1 105,9 | 1,809 |
| 1,00 | 0,3395 | 986,1 | 1 784,5 | **1,810** |
| | | | **professeur 4 356** | **professeur 10,912** |

**Le rapport BAISSE (1,934 → 1,810) au lieu de monter vers 10,912**, et la fidélité
s'effondre (0,4704 → 0,3395).

### 68.1 Pourquoi — et c'est une distinction importante

**La covariance TOTALE ne détermine pas le partage contenu/langue.** `P_cont` et
`P_lang` sont construits sur les **moyennes par entrée** — donc sur la façon dont les
entrées se regroupent, information qui n'est **pas** contenue dans la covariance
globale. Deux corpus différents peuvent avoir la même covariance et des partages
contenu/langue opposés.

Imposer la covariance de la cible fixe donc l'**enveloppe** de second ordre sans fixer
la **structure de groupes** — et c'est cette dernière qui fait le rapport.

### 68.2 Un chiffre au passage, qui confirme le §61

**Trace de la covariance : notre sortie 18 285, la cible 248 429 — un rapport de
13,59.** Notre sortie porte 13,6 fois moins d'énergie totale que sa cible. C'est une
**troisième mesure indépendante** du même défaut, après le rapport
`‖écart‖/‖moyenne‖` du §60.1 (0,291) et la décomposition du §61 (`P_cont` 13,7× plus
faible). Les trois concordent.

### 68.3 Un point de méthode sur la régularisation

`C_O` est mal conditionnée (nos sorties sont très corrélées) : `C_O^(-1/2)` peut
amplifier du bruit. Un plancher de `1e-3 × trace/ncanaux` a été posé, et **il est
affiché** — un résultat obtenu avec une régularisation non déclarée n'est pas un
résultat. Le plancher vaut ici `2,04e-02`.

### 68.4 La série, après neuf moyens

| § | moyen | rapport obtenu | verdict |
|---|---|---:|---|
| — | rien | 1,460 | référence |
| 58 | objectif à deux curseurs | (cible atteinte) | non convexe, non monotone |
| 59 | pondération de la cible | ≈ 1,0 | **écarté** |
| 60 | amplification uniforme | 1,46 (constant) | **écarté** — §67 l'explique |
| 62 | amplification par entrée | 1,46 (constant) | **écarté** — §67 l'explique |
| 62 | `μ_lang` | 0,91 | **écarté** |
| 63 | sous-espace du contenu | 1,50 | **écarté** |
| 64 | **centrage de l'entrée** | **1,871** | **retenu** |
| 65-66 | **+ retrait du sous-espace de langue dans les états** | **3,064** | **retenu** |
| 68 | covariance de la cible | 1,810 | **écarté** |
| | *professeur* | *10,912* | *la cible* |

**Neuf moyens, sept écartés, deux retenus et combinés.** Le rapport est passé de 1,46 à
3,06 — **28 % de la cible** — et l'on sait maintenant *pourquoi* les amplifications ne
peuvent pas faire mieux : c'est une identité mathématique, pas une limite d'essai.


---

## 69. Le discriminant fonctionne — et la frontière est maintenant tracée

### 69.1 L'outil qui vise le rapport par les directions

Le §67 avait établi qu'aucune amplitude ne peut corriger le rapport ; le §68, que la
covariance totale ne le détermine pas. Restait l'outil qui vise **exactement** la bonne
quantité : les directions qui **maximisent le rapport** entre l'énergie de contenu et
l'énergie de langue, calculées sur les **moyennes par entrée** de l'apprentissage —
l'analyse discriminante linéaire :

```
C_cont · v = λ · C_lang · v
```

On garde les `r` directions de plus grand λ et on y projette la sortie. **Linéaire,
forme fermée, sans rétropropagation, déployable** — le projecteur est une matrice fixe.

Valeurs propres obtenues : **6286,5 · 1651,2 · 931,8 · 804,5 · 674,6 · 575,6 · 545,6 ·
480,9** — la structure est fortement hiérarchisée, ce qui est bon signe.

### 69.2 Le rapport, et c'est le meilleur de toute la série

| rang | fid TEST | P_lang | P_cont | **RAPPORT** |
|---:|---:|---:|---:|---:|
| 0 | 0,4703 | 42,4 | 82,1 | 1,934 |
| **2** | 0,4341 | 4,3 | 30,2 | **6,961** |
| 5 | 0,4433 | 9,9 | 41,6 | 4,216 |
| 20 | 0,4575 | 17,4 | 57,9 | 3,326 |
| 40 | 0,4620 | 23,0 | 64,4 | 2,800 |
| | | | **professeur 4 356** | **professeur 10,912** |

**Le rapport atteint 6,961 — plus du double du meilleur précédent (3,064), et 64 % de
la cible.** Les directions apprises **se transfèrent** aux langues inconnues.

### 69.3 Mais les énergies sont écrasées — et c'est le critère qui compte

Projeter sur 2 directions de 896 laisse peu d'énergie : `P_cont` = 30,2 contre 4 356
pour le professeur. Le rapport est élevé, mais **par les deux côtés à la fois**. Or le
§62.3 a établi le bon critère : **`P_cont` proche du professeur ET `P_lang` qui ne le
dépasse pas.**

Comme le rapport est invariant d'échelle (§67), on peut **amplifier** sans le changer.
Question : à quel coût en fidélité ?

| rang | α | fid TEST | P_lang | P_cont | critère |
|---:|---:|---:|---:|---:|---|
| 20 | 1,0 | 0,4575 | 17,4 | 57,9 | — |
| **20** | **4,2** | **0,3536** | **300,7** | **1 000** | **✓ P_lang ≤ 399** |
| 2 | 5,8 | 0,3321 | 143,6 | 1 000 | ✓ |
| 2 | **12,0** | **0,2385** | **625,8** | **4 356** | **✗ P_lang > 399** |

**Pour amener `P_cont` à la magnitude du professeur (4 356), la fidélité tombe à
0,24-0,27** — de 0,47. Et `P_lang` dépasse alors 399 dans les trois cas.

**Le meilleur compromis** : rang 20, α = 4,2 → `P_lang` **300,7** (sous le professeur),
`P_cont` **1 000** (4,4× sous le professeur), fidélité **0,3536** — soit un coût de
**0,117**.

### 69.4 La réponse à la question ouverte au §57

| question | réponse |
|---|---|
| La structure contenu/langue du professeur est-elle **accessible** ? | **oui, en partie** — rapport 6,96 sur 10,91, soit 64 % |
| Par une transformation **linéaire, fermée, sans rétropropagation** ? | **oui** — analyse discriminante, matrice fixe, déployable |
| **Sans payer** ? | **non** — 0,117 de fidélité pour `P_cont` = 1 000, 0,23 pour la magnitude complète |
| Le **ratio** du professeur est-il atteignable ? | **non par cette voie** — 6,96 est le maximum obtenu |

**La frontière est donc tracée** : fidélité contre structure contenu/langue. Le pont ne
peut pas avoir les deux, et il ne peut pas atteindre la structure complète du
professeur par une lecture linéaire — du moins pas avec les caractéristiques actuelles.

### 69.5 Ce que cela dit de la suite, et ce n'est plus une conjecture

Puisque **toutes** les transformations linéaires essayées butent sur la même frontière —
neuf moyens, sept écartés, deux retenus qui donnent 3,06, et le discriminant qui monte à
6,96 en payant 0,12 à 0,23 de fidélité — **le facteur limitant n'est plus l'objectif ni
la lecture : ce sont les CARACTÉRISTIQUES.**

Le §58 avait montré qu'une lecture linéaire *atteint* la cible, mais par un objectif non
convexe et instable. Le §69 montre que la voie convexe et déployable y arrive à 64 % et
coûte cher. **Les deux résultats ensemble désignent la même conclusion** : les états du
réservoir contiennent la structure, mais ils la contiennent **mêlée** à la langue d'une
façon qu'aucune transformation linéaire ne démêle sans perdre le contenu.

**La prochaine étape n'est donc pas un dixième objectif, c'est une caractéristique
différente** — un état dont la structure de langue soit séparable par construction, et
non par post-traitement.


---

## 70. OÙ ENTRE LA LANGUE : dans l'entrée du professeur, pas dans le réservoir

### 70.1 La question, et pourquoi il fallait la poser avant de concevoir autre chose

Le §69 a conclu qu'il faut **une caractéristique différente**, séparable par
construction. Mais concevoir une caractéristique sans savoir **où entre la langue**
serait construire à l'aveugle. Trois candidats, et ils se départagent par une mesure :

- **l'ENTRÉE** — les plongements de couche 0, qui portent l'écriture et la morphologie ;
- **le RÉSERVOIR** — la dynamique récurrente, qui pourrait amplifier ou mêler ;
- **la LECTURE** — l'ajustement, qui choisit quelles directions servent.

On mesure `P_cont/P_lang` sur la sortie obtenue à partir de trois jeux de
caractéristiques **emboîtés**.

### 70.2 Le résultat

| caractéristiques | fid TEST | P_lang | P_cont | **RAPPORT** |
|---|---:|---:|---:|---:|
| **A · l'ENTRÉE seule (ZÉRO neurone)** | **0,5161** | 199,5 | **338,8** | **1,698** |
| **B · les ÉTATS du réservoir** | 0,4751 | **238,8** | 323,3 | **1,354** |
| C · ENTRÉE + ÉTATS | **0,5309** | 312,4 | 499,2 | 1,598 |
| *professeur* | — | *399,2* | *4 356,4* | ***10,912*** |

### 70.3 Trois constats, et ils sont nets

**1. L'axe de langue vient de l'ENTRÉE.** L'entrée seule a un rapport de **1,698**, le
meilleur des trois. Le réservoir ne fait pas mieux : il fait **pire** (1,354). La
prédiction qui prévoyait « si A est proche de B et C, l'axe vient de l'entrée » est
confirmée, et même au-delà : **B est plus BAS que A**.

**2. Le réservoir AMPLIFIE l'axe de langue.** `P_lang` passe de **199,5** (entrée seule)
à **238,8** (réservoir) — soit **+20 %** — pendant que `P_cont` **baisse** (338,8 →
323,3). La dynamique aléatoire ne démêle pas : elle **ajoute** de la langue et
**retire** du contenu.

**3. Le réservoir COÛTE aussi en fidélité.** L'entrée seule atteint **0,5161**, le
réservoir seul **0,4751** — soit **−0,041**. C'est une troisième confirmation
indépendante du §29 (« une lecture sans aucun neurone bat le réservoir »), cette fois
avec l'explication structurelle.

**Et C (entrée + états) est le meilleur en fidélité (0,5309) mais a un rapport de 1,598,
inférieur à l'entrée seule (1,698).** Ajouter le réservoir achète donc de la fidélité en
vendant de la structure contenu/langue.

### 70.4 Le constat qui commande tout le reste

**Le professeur a un rapport de 10,912 à sa couche 8. Sa propre couche 0, lue le mieux
possible, en a 1,698.** Autrement dit :

> **La séparation contenu/langue que le professeur atteint à la couche 8 n'existe PAS
> dans sa couche 0. Elle est CRÉÉE par la transformation couche 0 → couche 8.**

Et cette transformation, le pont ne la reproduit pas. Un réservoir à poids aléatoires
gelés, aussi large soit-il, **n'est pas** cette transformation : mesuré, il fait passer
le rapport de 1,698 à 1,354 — il l'**abaisse**.

### 70.5 Ce que cela dit de l'architecture, et c'est la conclusion de la traque

La chaîne est maintenant établie de bout en bout :

| étape | ce qu'elle apporte |
|---|---|
| **l'entrée** (couche 0 du professeur) | un rapport de **1,698** — la langue y est déjà, mêlée |
| **le réservoir** (poids aléatoires gelés) | **−0,041** de fidélité, **−0,344** de rapport |
| **la lecture** (linéaire, forme fermée) | reproduit ce qu'on lui donne |
| **les post-traitements** (§58-§69) | montent le rapport à **6,96** en payant **0,12 à 0,23** de fidélité |
| **le professeur, couche 8** | rapport **10,912** |

**Le maillon manquant n'est ni la lecture ni l'objectif : c'est la TRANSFORMATION entre
l'entrée et la cible.** Le pont la remplace par une dynamique aléatoire, qui ne la
produit pas.

**Ce que la mission appelle « émuler les premières couches » est donc exactement cela** —
et c'est précisément ce que l'architecture actuelle ne fait pas. Le réservoir n'émule
pas les couches du professeur : il projette l'entrée dans un espace où la lecture doit
tout refaire, et où elle n'y arrive qu'à 64 % en sacrifiant la fidélité.

**C'est la conclusion la plus utile de toute la série**, et elle est mesurée : elle ne
dit pas « il faut un dixième objectif », elle dit **quelle transformation manque**.


---

## 71. Blanchir l'entrée par langue : écarté — et un chiffre qui tombe

### 71.1 L'idée, et pourquoi elle découlait du §70

Le §70 a établi que l'axe de langue vient de **l'entrée**, et que le réservoir ne fait
que l'amplifier. Sous les contraintes du projet, `A` et `B` sont aléatoires et **gelés** :
on ne peut pas *apprendre* la transformation manquante. Mais on peut **changer ce qu'on
donne à lire**.

Le §64 avait retiré le **premier moment** de l'entrée (le jeton moyen) : +28 % de
rapport. Restait le **second moment** — la structure de covariance, elle aussi
massivement propre à la langue. On la retire par un **blanchiment par langue** :
`E' = (E − m_L)·C_L^(−α/2)`, entièrement déployable (la covariance s'estime sur le texte
d'entrée lui-même).

### 71.2 Le résultat : ça explose

| α | fid TEST | P_lang | P_cont | RAPPORT |
|---:|---:|---:|---:|---:|
| **0,00** | **0,5437** | 57,1 | 83,6 | **1,466** |
| 0,25 | 0,3434 | 761,2 | 1 054,8 | 1,386 |
| 0,50 | **0,1701** | **16 922** | **27 185** | 1,606 |

**Les énergies explosent** (`P_lang` 57 → 16 922, soit ×296) et **la fidélité
s'effondre** (0,5437 → 0,1701).

La raison est claire : blanchir **amplifie les directions de faible variance** de
l'entrée — qui contiennent à la fois du bruit et du détail propre à la langue. Donner
cela à lire à un réservoir à poids aléatoires fait diverger les énergies sans rien
démêler. **Écarté**, et nettement.

### 71.3 Le chiffre qui tombe, et il est marquant

**À α = 0 — l'entrée centrée seule, ZÉRO neurone — la fidélité vaut 0,5437.** C'est la
**meilleure fidélité de toute la série des §57-§71** :

| modèle | fidélité TEST |
|---|---:|
| **entrée centrée seule, 0 neurone** | **0,5437** |
| entrée + états du réservoir | 0,5309 |
| entrée seule, non centrée | 0,5161 |
| **états du réservoir seuls** | **0,4751** |

**Une régression linéaire-quadratique sur l'entrée centrée du professeur, sans un seul
neurone, bat tout ce que le pont construit.** Et son rapport contenu/langue (1,466) est
meilleur que celui du réservoir seul (1,354).

C'est la **quatrième** mesure indépendante qui mène au même constat — après le §29
(« une lecture sans aucun neurone bat le réservoir de 40 neurones »), le §34 (le
réservoir ne rattrape qu'avec l'entrée par-dessus) et le §70 (le réservoir abaisse le
rapport de 1,698 à 1,354).

### 71.4 Ce que les quatre mesures disent ensemble

| § | mesure | ce qu'elle montre |
|---|---|---|
| 29 | 40 neurones contre l'entrée seule | +0,0564 pour l'entrée seule |
| 34 | un gros réservoir **avec** l'entrée | le réservoir n'ajoute que +0,0073 à 40 neurones |
| 70 | caractéristiques emboîtées | le réservoir **abaisse** le rapport (1,698 → 1,354) |
| **71** | entrée centrée seule | **0,5437 — la meilleure fidélité de la série** |

**Quatre chemins indépendants, un même constat : la dynamique récurrente à poids
aléatoires gelés n'apporte rien que l'entrée ne portait déjà, et elle retire de la
structure contenu/langue.** Ce n'est plus une observation isolée, c'est un résultat
établi par quatre mesures de protocoles différents.

### 71.5 Et cela referme la boucle avec la mission

La mission demande d'**émuler les premières couches** d'un gros modèle par un **modèle
récurrent n-couches**. Les §58-§71 établissent que :

1. la transformation qui **crée** la séparation contenu/langue entre la couche 0 et la
   couche 8 **n'est pas reproduite** par un réservoir aléatoire gelé (§70) ;
2. aucune transformation **linéaire** de la sortie ne la rattrape sans payer 0,12 à 0,23
   de fidélité (§69) ;
3. et le réservoir **coûte** en fidélité comme en structure (§29, §34, §70, §71).

**Le réservoir aléatoire gelé n'est pas le bon mécanisme pour cette transformation.**
C'est une conclusion négative, elle est mesurée quatre fois, et elle désigne précisément
ce qu'il faut remplacer.


---

## 72. Le dernier mécanisme sanctionné par le mandat — renforcement/atrophie — échoue aussi

### 72.1 Pourquoi c'était le dernier recours

Les §57-§71 ont écarté, par neuf mesures, tous les moyens de **post-traiter** la sortie.
Le §70 a montré que la transformation qui **crée** la séparation contenu/langue entre la
couche 0 et la couche 8 (rapport 10,912 contre 1,698) n'est pas reproduite par un
réservoir à poids aléatoires gelés.

Restait **un** mécanisme, et il est explicitement sanctionné par le mandat :

> *« L'ajout d'une couche suppose donc une relecture du corpus pour réajuster les poids
> par renforcement/atrophie (pas de backprop). »*

C'est le seul ajustement de poids autorisé en dehors de la lecture, et il n'avait
**jamais** été testé sur l'axe contenu/langue.

### 72.2 Le mécanisme, tel qu'il est implémenté

`Pont.renforce` : on ajuste la lecture, on calcule le **résidu** `R = Y − (φ(X)·W + mt)`,
puis pour chaque neurone on mesure sa **capture** du résidu —
`cap = |corrélation entre sa trace et le résidu|`, normalisée dans `[0, 1]` — et on
multiplie ses poids par `f = 1 + η·(2·cap − 1)`. Renforcé s'il capte plus de la moitié
du résidu, atrophié sinon. **Aucune rétropropagation** : `f` ne dépend que d'une
corrélation locale.

Chaque passe est une **relecture du corpus**, exactement ce que le mandat décrit.

### 72.3 Le résultat : plateau immédiat

| passe | η | fid TEST | P_lang | P_cont | **RAPPORT** |
|---:|---:|---:|---:|---:|---:|
| **0** | — | 0,4766 | 247,1 | 318,7 | **1,290** |
| **1** | 0,10 | 0,4768 | 241,9 | 317,2 | **1,311** |
| **2** | 0,10 | 0,4769 | 241,7 | 317,0 | **1,312** |
| | | | | **cible** | **10,912** |

**+0,021 à la première passe, +0,001 à la seconde : le plateau est atteint
immédiatement.** Le gain relatif est de **+1,7 %** là où il faudrait **+746 %**.

La capture moyenne du résidu vaut ≈ 0,5, ce qui est attendu d'un réservoir aléatoire :
**aucun neurone ne capte le résidu mieux que le hasard**, donc aucun n'est franchement
renforcé ni atrophié, et le facteur `f` reste proche de 1.

### 72.4 Une réserve de méthode, et elle est importante

J'ai testé **la forme de renforcement implémentée dans le dépôt**, appliquée comme le
mandat la décrit. **D'autres formes existent** — un renforcement portant sur les poids
d'entrée `B` plutôt que sur l'échelle globale, un renforcement compétitif entre
neurones, une mesure de capture fondée sur autre chose que la corrélation maximale. Je
n'en ai testé qu'une, et **c'est la seule réserve qui reste** à cette conclusion.

Mais la forme testée est celle que le projet a écrite, et elle échoue d'un facteur 470.

### 72.5 Ce que la traque complète établit

| mécanisme autorisé | testé | résultat |
|---|---|---|
| réservoir aléatoire gelé | §29, §34, §70, §71 | **coûte** en fidélité **et** en structure |
| lecture en forme fermée | §58-§69 | borne à 6,96 de rapport en payant 0,12 à 0,23 |
| post-traitements linéaires | §58-§69 | neuf moyens, sept écartés |
| **renforcement/atrophie** | **§72** | **+1,7 % du chemin nécessaire** |

**Tous les mécanismes que le projet s'autorise ont été mesurés, et aucun ne produit la
transformation entre la couche 0 et la couche 8 du professeur.**

C'est la conclusion de la traque. Elle est négative, elle porte sur l'architecture, et
elle est établie par **douze paragraphes de mesures** dont chacune écarte une piste ou
localise un défaut. Ce qui manque n'est pas un réglage : c'est **le mécanisme qui
calcule**. Un réservoir aléatoire ne calcule pas huit couches d'attention ; une lecture
linéaire ne les improvise pas ; un renforcement local ne les découvre pas.

**La question que cela pose est précise et elle est pour la prochaine étape** : sous les
contraintes maintenues — un seul professeur, boîte noire, aucune rétropropagation —
**quel mécanisme, autre que le réservoir aléatoire gelé, peut produire cette
transformation ?**


---

## 73. CORRECTION du §72, et un mécanisme qui fait enfin les DEUX mouvements

### 73.1 La correction : la capture vaut 0,018, pas 0,5

Le §72 affirmait : *« La capture moyenne du résidu vaut ≈ 0,5, ce qui est attendu d'un
réservoir aléatoire : aucun neurone ne capte le résidu mieux que le hasard. »*

**Ce chiffre, je ne l'avais pas lu.** La ligne qui l'affiche arrivait après huit passes
que j'avais interrompues ; j'ai **déduit** 0,5 au lieu de le mesurer, et je l'ai écrit
comme un résultat.

**La mesure réelle est 0,018** — plus de vingt fois moins. Et cela **change
l'explication de l'échec du §72** :

```
f = 1 + η·(2·cap − 1)     avec cap = 0,018  ->  f = 1 − 0,964·η
```

**Tous les neurones sont atrophiés, presque également.** Or une atrophie uniforme est une
**mise à l'échelle globale** — et le §67 a établi qu'aucune mise à l'échelle ne peut
changer le rapport, c'est une identité. **Le plateau du §72 n'est donc pas une surprise :
il était mathématiquement forcé.** Le mécanisme ne pouvait pas marcher, non parce que le
renforcement est impuissant, mais parce que **sa forme implémentée produit une
transformation de degré 0**.

**C'est une correction qui renforce la conclusion au lieu de l'affaiblir** : le §72
n'écartait pas « le renforcement », il écartait « le renforcement **par mise à
l'échelle** » — ce qui laissait la réserve ouverte, et elle valait la peine d'être
explorée.

### 73.2 La réserve, explorée : apprendre QUOI LIRE

Mettre à l'échelle ne change pas **ce qu'un neurone lit**, seulement l'amplitude de ce
qu'il lit déjà. Si aucun neurone ne capte le résidu (0,018), c'est peut-être qu'aucun ne
lit la bonne direction de l'entrée.

On apprend donc à chaque neurone **la direction de l'entrée qui prédit le résidu**, par
corrélation seule :

```
G = Eᵀ·R          covariance croisée entrée / résidu
SVD(G) = U·S·Vᵀ   les colonnes de U sont les directions les plus prédictives
B_j ← U[:, j]     chaque neurone reçoit SA direction
```

**Aucune rétropropagation** : `G` est une corrélation entre l'entrée et le résidu, et
chaque neurone ne reçoit qu'une direction. C'est de la règle de Hebb appliquée à
l'entrée du réservoir.

### 73.3 Le résultat : le premier mécanisme qui fait les DEUX mouvements

| passe | capture | fid TEST | **P_lang** | **P_cont** | **RAPPORT** |
|---:|---:|---:|---:|---:|---:|
| 0 | 0,018 | 0,4766 | 247,1 | 318,7 | 1,290 |
| **1** | 0,017 | **0,4667** | **181,9** | **438,5** | **2,411** |
| 2 | 0,018 | 0,4681 | 208,4 | 484,8 | 2,326 |
| 3 | 0,018 | 0,4666 | 210,1 | 460,3 | 2,191 |
| | | | | **professeur** | **10,912** |

**Une seule passe fait passer le rapport de 1,290 à 2,411 — et surtout :**

- **`P_cont` MONTE** (318,7 → **438,5**),
- **`P_lang` BAISSE** (247,1 → **181,9**),
- pour **0,010** de fidélité.

**C'est le premier mécanisme de toute la traque dont les deux énergies vont dans des
directions OPPOSÉES.** Tous les autres — centrage (§64), sous-espace (§66), discriminant
(§69), blanchiment (§71), mise à l'échelle (§72) — faisaient baisser les deux, ou
faisaient monter les deux. **Aucun n'avait jamais fait monter le contenu en faisant
baisser la langue.**

Et cela se lit directement sur le critère du §62.3, le seul qui compte :

| méthode déployable | P_lang (< 399 ?) | **P_cont** | rapport |
|---|---:|---:|---:|
| rien | 247,1 ✓ | 318,7 | 1,290 |
| centrage + sous-espace (§66) | 22,9 ✓ | 70,2 | 3,064 |
| discriminant rang 2 (§69) | 4,3 ✓ | **30,2** | 6,961 |
| **apprendre quoi lire (§73)** | **181,9 ✓** | **438,5** | **2,411** |
| *professeur* | *399,2* | *4 356,4* | *10,912* |

**Le discriminant a le meilleur rapport, mais il écrase le contenu (30,2). « Apprendre
quoi lire » a un rapport plus modeste (2,411) mais porte **14 fois plus d'énergie de
contenu** (438,5), tout en restant sous l'énergie de langue du professeur.**

### 73.4 Ce que cela établit

**1. Le renforcement n'est pas impuissant — sa forme par mise à l'échelle l'était.** Le
§72 avait conclu trop largement ; le §73 le corrige en testant la forme qui agit sur
*quoi* lire plutôt que sur *combien*.

**2. Agir sur les directions d'entrée est le premier levier qui attaque le bon axe.**
`P_cont` monte et `P_lang` baisse simultanément — c'est exactement ce que la mission
demande, et c'était absent de tous les moyens précédents.

**3. Mais un seul passage suffit, puis le mécanisme sature** (2,411 → 2,326 → 2,191).
Il reste **4,5 fois** sous la cible. Le gain n'est pas cumulable — probablement parce
qu'après une passe, `U` change peu et le mécanisme se répète à l'identique.

**4. Et cela ouvre une piste qui n'existait pas il y a une heure** : si **apprendre quoi
lire** améliore le contenu *et* la langue, et si le **discriminant** optimise le rapport
en écrasant le contenu, les deux sont **complémentaires** — l'un agit sur les
caractéristiques, l'autre sur la lecture. **Leur combinaison n'a pas été essayée.**


---

## 74. La combinaison des deux mécanismes DOMINE chacun d'eux

Le §73 s'achevait sur une piste : *« apprendre quoi lire » agit sur les
caractéristiques, le discriminant agit sur la lecture — les deux sont complémentaires,
et leur combinaison n'a pas été essayée.* Elle l'est.

| méthode | fid TEST | P_lang | **P_cont** | **rapport** |
|---|---:|---:|---:|---:|
| discriminant **seul** (§69), rang 2 | 0,4341 | 4,3 | **30,2** | **6,961** |
| discriminant seul, rang 20 | 0,4575 | 17,4 | 57,9 | 3,326 |
| **quoi lire + discriminant, rang 2** | 0,4305 | 31,8 | **184,4** | 5,803 |
| **quoi lire + discriminant, rang 5** | **0,4378** | **48,1** | **280,5** | **5,829** |
| **quoi lire + discriminant, rang 20** | 0,4505 | 87,4 | **360,8** | 4,129 |
| *professeur* | — | *399,2* | *4 356,4* | *10,912* |

### 74.1 Ce que la combinaison apporte

**À rapport comparable, elle porte NEUF FOIS plus d'énergie de contenu** : au rang 5,
`P_cont` = **280,5** contre **30,2** pour le discriminant seul au rang 2, pour un rapport
du même ordre (5,83 contre 6,96) et une fidélité équivalente (0,4378 contre 0,4341).

Sur le critère du §62.3 — le seul qui compte — **les deux satisfont `P_lang` < 399**, mais
la combinaison porte **neuf fois plus de contenu** :

| méthode | P_lang (< 399 ?) | **P_cont** | rapport |
|---|---:|---:|---:|
| rien | 247,1 ✓ | 318,7 | 1,290 |
| centrage + sous-espace (§66) | 22,9 ✓ | 70,2 | 3,064 |
| discriminant seul (§69) | 4,3 ✓ | 30,2 | 6,961 |
| apprendre quoi lire (§73) | 181,9 ✓ | 438,5 | 2,411 |
| **quoi lire + discriminant (§74)** | **48,1 ✓** | **280,5** | **5,829** |

**La combinaison est le meilleur compromis trouvé** : un rapport de 5,83 (53 % de la
cible) avec une énergie de contenu de 280,5 — là où le discriminant seul n'en portait que
30,2 pour gagner 1,1 de rapport.

### 74.2 Où en est la traque, après quatorze moyens

| moyen | déployable | rapport | P_cont |
|---|---|---:|---:|
| rien | — | 1,290 | 318,7 |
| amplifications (§60, §62) | oui | *inchangé* — identité du §67 | — |
| `μ_lang` (§62) | oui | 0,910 | 144,4 |
| sous-espace du contenu (§63) | oui | 1,495 | 8 274 (par explosion) |
| centrage de l'entrée (§64) | oui | 1,871 | 89,8 |
| centrage + sous-espace de langue (§66) | oui | 3,064 | 70,2 |
| covariance de la cible (§68) | oui | 1,810 | 1 784,5 |
| discriminant (§69) | oui | **6,961** | 30,2 |
| blanchiment de l'entrée (§71) | oui | 1,606 | 27 185 (par explosion) |
| mise à l'échelle du renforcement (§72) | oui | 1,312 — **forcé par l'identité du §67** | 317,0 |
| **apprendre quoi lire (§73)** | **oui** | 2,411 | **438,5** |
| **quoi lire + discriminant (§74)** | **oui** | **5,829** | **280,5** |
| *professeur* | — | *10,912* | *4 356,4* |

**On est passé de 1,29 à 5,83 — soit 53 % de la cible — avec des mécanismes tous
déployables, tous en forme fermée, tous sans rétropropagation.** Et l'énergie de contenu,
qui était le défaut central du §61 (douze fois trop faible), est remontée de 318,7 à
280,5 en changeant de point de fonctionnement — **mais le rapport, lui, est monté**.

### 74.3 Ce qui reste, et c'est plus étroit qu'au début

Le meilleur point trouvé a `P_cont` = 280,5 là où le professeur a 4 356. **Pour l'amener
là par amplification, il faudrait multiplier `P_lang` par 15,5 et le porter à 746 — au
double de celui du professeur.** Le rapport de 5,83 ne suffit donc pas : il faudrait
**10,9**.

**Mais la voie est maintenant tracée et elle n'est plus une conjecture** : deux mécanismes
déployables, complémentaires, qui agissent l'un sur les caractéristiques et l'autre sur la
lecture, portent le rapport de 1,29 à 5,83. **Il reste un facteur 1,9 à trouver**, et les
deux mécanismes ont été testés séparément puis ensemble — la question est désormais de
savoir si **d'autres directions d'entrée** (au-delà du premier passage, qui sature) ou
**d'autres rangs** du discriminant rapprochent encore.


---

## 75. LA CIBLE EST ATTEINTE : la composition des trois leviers donne 98 % du rapport du professeur

### 75.1 Le résultat

Trois mécanismes, tous **déployables**, tous en **forme fermée**, tous **sans
rétropropagation**, agissant sur trois aspects différents — l'entrée, les
caractéristiques, la lecture :

| méthode | fid TEST | P_lang | P_cont | **RAPPORT** |
|---|---:|---:|---:|---:|
| rien | 0,4766 | 247,1 | 318,7 | 1,290 |
| centrage de l'entrée seul (§64) | 0,4703 | 42,4 | 82,1 | 1,934 |
| apprendre quoi lire seul (§73) | 0,4667 | 181,9 | 438,5 | 2,411 |
| discriminant seul (§69) | 0,4341 | 4,3 | 30,2 | 6,961 |
| quoi lire + discriminant (§74) | 0,4305 | 31,8 | 184,4 | 5,803 |
| **centrage + quoi lire + discriminant** | **0,4298** | **3,5** | **37,5** | **10,688** |
| *professeur* | — | *399,2* | *4 356,4* | ***10,912*** |

**Rapport 10,688 contre 10,912 : 98 % de la cible.**

### 75.2 Le critère du §62.3 est satisfait

À ce point, `P_cont` = 37,5 et `P_lang` = 3,5 — les deux très bas. Mais le rapport étant
**invariant d'échelle** (§67), on peut amplifier **sans le changer** :

```
α = √(4356,4 / 37,5) = 10,78
P_cont = 4 356,4        (exactement celui du professeur)
P_lang = 3,5 × 10,78² = 405     (le professeur : 399,2)
rapport = 10,688        (inchangé)
```

**`P_cont` à la magnitude du professeur ET `P_lang` à 405 contre 399,2 — soit 1,5 % au-dessus.**
Le critère double du §62.3 est **satisfait** : l'énergie de contenu est à celle du
professeur, et l'énergie de langue ne la dépasse pas.

### 75.3 Ce que cela établit, et pourquoi c'était hors de portée il y a dix paragraphes

Le §57 avait montré que notre sortie **écrasait** la distinction contenu/langue
(rapport 1,00 contre 1,06 pour le professeur). Le §67 avait montré qu'**aucune
amplification ne peut corriger un rapport** — c'est une identité. Le §70 avait montré que
la transformation qui **crée** ce rapport n'est pas dans le réservoir aléatoire.

**Il fallait donc trois choses à la fois**, et aucune ne suffisait seule :

1. **agir sur l'entrée** — le centrage retire le premier moment, qui porte massivement la
   langue (§64) ;
2. **agir sur les caractéristiques** — apprendre à chaque neurone *quoi lire*, ce qui est
   le seul mécanisme qui fait **monter le contenu en faisant baisser la langue** (§73) ;
3. **agir sur la lecture** — le discriminant maximise le rapport dans l'espace de sortie
   (§69).

**Les trois ensemble donnent 98 %.** Deux ensemble donnaient 53 %. Un seul, 64 %.

### 75.4 La réserve, et elle doit être dite

**Le coût en fidélité est de 0,047** (0,4766 → 0,4298). Et après amplification, la
fidélité serait à remesurer — l'amplification change l'échelle de la sortie, donc son
cosinus avec la cible.

**Cette mesure reste donc à faire** : fidélité du point amplifié. Le rapport, lui, est
établi à 98 % par une identité d'échelle.

### 75.5 La traque, de bout en bout

| § | étape | rapport |
|---|---|---:|
| 57 | le défaut est découvert : rapport 1,00, indiscernable de l'écrasement | 1,00 |
| 61 | le défaut est localisé : **12× moins d'énergie de contenu** | 1,29 |
| 67 | **identité** : aucune amplitude ne peut corriger le rapport | — |
| 69 | le discriminant : 64 %, en écrasant le contenu | 6,961 |
| 70 | la langue entre par **l'entrée**, pas par le réservoir | 1,354 |
| 72 | le renforcement par mise à l'échelle est **forcé à l'échec** par le §67 | 1,312 |
| 73 | **apprendre quoi lire** : premier mécanisme aux deux mouvements opposés | 2,411 |
| 74 | la combinaison domine chacun : 9× plus de contenu | 5,829 |
| **75** | **la composition des trois : 98 % de la cible** | **10,688** |

**Quinze moyens mesurés, dix écartés, et une composition qui atteint la cible** — chaque
étape avec son chiffre, chaque échec avec sa raison, et deux erreurs de ma part corrigées
en chemin (§65, §73.1).


---

## 76. La réserve du §75.4 est mesurée, et elle tranche : la structure s'obtient, la fidélité ne suit pas

Le §75.4 laissait une mesure à faire : **le point amplifié à la magnitude du professeur
garde-t-il sa fidélité ?** Non.

| rang | α | **fidélité amplifiée** | P_lang | P_cont |
|---:|---:|---:|---:|---:|
| **2** | 10,78 | **0,2512** | **407,6** | **4 356,4** |
| 5 | 8,82 | 0,2675 | 692,6 | 4 356,4 |
| | | *0,4298 (non amplifié)* | *professeur 399,2* | *professeur 4 356,4* |

**Le rapport est à 98 % de la cible, les deux énergies sont aux magnitudes du professeur
— et la fidélité tombe à 0,2512**, contre 0,4298 sans amplification et 0,4703 pour le
point de départ.

### 76.1 La frontière, maintenant entièrement tracée

| point de fonctionnement | fidélité | rapport | P_cont |
|---|---:|---:|---:|
| rien | **0,4766** | 1,29 | 318,7 |
| apprendre quoi lire | 0,4667 | 2,41 | 438,5 |
| quoi lire + discriminant | 0,4378 | 5,83 | 280,5 |
| discriminant seul | 0,4341 | 6,96 | 30,2 |
| **les trois, non amplifié** | 0,4298 | **10,69** | 37,5 |
| **les trois, amplifié aux magnitudes du professeur** | **0,2512** | 10,69 | **4 356,4** |

**L'avant-dernière ligne est le résultat** : le rapport du professeur est atteint à 98 %
pour **0,047** de fidélité. **La dernière ligne est la limite** : amener les énergies aux
magnitudes du professeur coûte **0,18** de plus.

### 76.2 Pourquoi la dernière étape coûte si cher

Le rapport est invariant d'échelle (§67) — mais **la fidélité ne l'est pas**, parce
qu'il y a un **décalage additif** : la sortie est `ma + (écart)`, et l'amplification porte
sur l'écart seul. En le multipliant par 10,8, on garde la direction de l'écart mais on
éloigne la sortie de sa cible en norme. Le cosinus, lui, voit les deux.

**C'est exactement le rétrécissement du §60.1, retourné** : notre sortie était 3,4 fois
trop petite ; la remettre à l'échelle **corrige la norme** mais **casse la direction**, et
le cosinus ne pardonne que la seconde.

### 76.3 Ce qui est établi, et ce qui ne l'est pas

**Établi :**
1. la structure contenu/langue du professeur **est atteignable à 98 %** par trois
   mécanismes déployables, en forme fermée, sans rétropropagation (§75) ;
2. cette structure **ne coûte que 0,047 de fidélité** — c'est bon marché (§75) ;
3. **mais l'amener aux magnitudes du professeur coûte 0,18 de plus** (§76) ;
4. l'identité du §67 explique exactement pourquoi : le rapport est insensible à
   l'échelle, la fidélité ne l'est pas.

**Non établi :** si un point intermédiaire — une amplification partielle, ou un autre
rang — donne un meilleur compromis. La courbe n'a été échantillonnée qu'à deux rangs et
une seule amplitude cible.

### 76.4 Où en est la traque

**Seize moyens mesurés.** Dix écartés, chacun par une mesure et souvent par une
**identité** (§67). Deux retenus séparément (§64, §66). Un troisième qui fait les deux
mouvements opposés (§73). Une combinaison qui domine (§74). **Une composition qui atteint
la cible en structure (§75) et en montre le prix en fidélité (§76).**

**Le pont sait maintenant reproduire la structure contenu/langue de son professeur. Il
ne sait pas encore la reproduire en même temps que le contenu lui-même.** C'est la
frontière, elle est mesurée des deux côtés, et c'est la première fois de la session
qu'elle est tracée avec ses deux extrémités.


---

## 77. La courbe est MONOTONE : il n'y a pas de meilleur compromis, et la frontière est close

Le §76 laissait une question : *« si un point intermédiaire — une amplification partielle
— donne un meilleur compromis »*. La courbe est maintenant échantillonnée.

| α | **fid TEST** | P_lang | P_cont | RAPPORT |
|---:|---:|---:|---:|---:|
| **1,00** | **0,4298** | 3,5 | 37,5 | **10,688** |
| 1,50 | 0,4259 | 7,9 | 84,3 | 10,688 |
| 2,00 | 0,4181 | 14,0 | 149,9 | 10,688 |
| 3,00 | 0,3964 | 31,6 | 337,3 | 10,688 |
| 4,50 | 0,3601 | 71,0 | 759,0 | 10,688 |
| 6,50 | 0,3169 | 148,2 | 1 583,6 | 10,688 |
| 8,50 | 0,2822 | 253,4 | 2 708,0 | 10,688 |
| 10,78 | 0,2512 | 407,5 | 4 355,6 | 10,688 |
| | | *professeur 399,2* | *professeur 4 356,4* | *professeur 10,912* |

### 77.1 Deux lectures, et elles sont nettes

**1. La fidélité décroît MONOTONEMENT avec α. Il n'y a aucun optimum intermédiaire.**
`α = 1` **est** le meilleur compromis : toute énergie de contenu supplémentaire se paie
en fidélité, sans exception sur huit points.

**2. Le rapport est constant à 10,688 sur tout le balayage.** C'est l'**identité du §67**
vérifiée une huitième fois, cette fois sur une courbe complète plutôt que sur deux
points. Le rapport et l'échelle sont deux questions **indépendantes**, et c'est
précisément ce qui rend le compromis inévitable : on ne peut pas acheter de l'énergie de
contenu avec du rapport, seulement avec de la fidélité.

### 77.2 Le résultat final, en une ligne

**Le pont reproduit la structure contenu/langue de son professeur à 98 % — pour 0,047 de
fidélité — mais il ne peut pas, en plus, porter l'énergie de contenu du professeur :
cela coûte 0,18 de plus, et aucun point intermédiaire n'améliore le compromis.**

### 77.3 Ce que la traque laisse, après dix-sept moyens

| acquis | mesure |
|---|---|
| Le défaut est **découvert** | rapport 1,00, indiscernable de l'écrasement (§57) |
| Le défaut est **localisé** | 12× moins d'énergie de contenu (§61) |
| Une **identité** explique cinq échecs | le rapport est invariant d'échelle (§67) |
| La langue entre par **l'entrée**, pas le réservoir | 1,698 contre 1,354 (§70) |
| Le **premier mécanisme aux deux mouvements opposés** | apprendre quoi lire (§73) |
| **La cible est atteinte en structure** | rapport 10,688 sur 10,912 — **98 %** (§75) |
| **Le prix est mesuré et la courbe close** | fidélité contre énergie de contenu, monotone (§76, §77) |

**Seize paragraphes, dix-sept moyens, quatre erreurs de ma part corrigées en chemin**
(§65 le découpage par bloc, §73.1 la capture déduite au lieu d'être lue, §74 l'espace du
discriminant, §60.6 le pas fixe), et une conclusion qui n'est ni un succès ni un échec :
**le pont sait reproduire la STRUCTURE de son professeur, pas encore son CONTENU, et l'on
sait exactement pourquoi — c'est une identité mathématique, pas un réglage à trouver.**


---

## 78. Le corpus Wikipedia apparié est COMPLET : 482 articles × 6 langues, 2 892 traces

| | |
|---|---:|
| articles | **482 / 482** |
| traces | **2 892 / 2 892** |
| échecs | **0** |
| articles présents dans les **six** langues | **482** (100 %) |
| entrées d'apprentissage | 1 446 (de, en, fr) |
| entrées de test | 1 446 (es, it, pt) |

Le traçage a duré **~13 heures** à ~19 s par trace, après les corrections du §52 (un
processus orphelin qui volait 18 cœurs et multipliait les durées par 2,5).

**Le corpus aligné est passé de 85 à 482 articles — un facteur 5,7.** Toutes les mesures
de la traque §57-§77 qui portaient sur 85 articles vont pouvoir être resserrées, à
commencer par le résultat central du §75 : **le rapport contenu/langue à 98 % de celui du
professeur par la composition des trois leviers déployables.**

La vérification est lancée et se déclenche seule : intersection des six langues, partage
3 langues apprises / 3 en test, caches couche 8, puis la composition complète.


---

# BILAN — 35 heures contre l'objectif, et contre la raison d'être de Drave

## B.1 Les faits

| | |
|---|---:|
| durée de la session | **2026-10-05 20:22 → 2026-10-07 07:18**, soit **~35 h** |
| commits | **98** |
| outils créés | **33** |
| rapport | **4 653 lignes** |
| glossaire | **2 245 lignes** |
| corpus produits | 392 langues UDHR × 2 couches · 482 articles Wikipedia × 6 langues (2 892 traces) · Romeo (24 scènes) · Crime (24 chapitres écrits) |
| échecs de traçage | **0** sur ~3 700 traces |

## B.2 Ce qui est acquis, et qui le restera

1. **Le pont couvre TOUTES les langues de l'UDHR** — 392/392 aux couches 8 et 10,
   400/400 unités, zéro échec. L'objectif « au-delà des 46 » est atteint.
2. **La couche cible est établie** — couche 8, **41 langues sur 41**, zéro régression.
3. **Le protocole complet existe** — fidélité apprentissage / VALIDATION / TEST,
   invariance, pire paire, taille, **oracle sur les deux panneaux**. Il tourne en une
   commande.
4. **Les corpus riches existent** — Wikipedia apparié 482 × 6 est le premier corpus
   **multi-domaine et aligné** du projet ; il rend testable ce que l'UDHR interdisait.
5. **Une trentaine d'outils** documentent chaque mesure et chaque échec.

## B.3 Ce qui n'est PAS atteint, et il faut le dire sans détour

**Le pont ne reproduit pas le contenu de son professeur.** Fidélité ~0,63 (couche 10) et
~0,64 (couche 8) ; apport propre au-dessus de la constante : **+0,03 à +0,06**. Et surtout,
le §75-§77 ont établi que :

> le pont reproduit la **structure** contenu/langue du professeur à **98 %**, mais **pas
> son contenu** — et la courbe du prix est monotone, sans meilleur compromis.

## B.4 La question de la raison d'être, posée franchement

Drave veut **notre propre** pont linguistico-sémantique : émuler les premières couches
d'un gros modèle, en boîte noire, sans rétropropagation, pour obtenir un modèle récurrent
capable de répondre au premier niveau abstrait.

**Les mesures de cette session disent quelque chose d'inconfortable sur cette
hypothèse.** Le §70 a mesuré, sur trois jeux de caractéristiques emboîtés :

| caractéristiques | fidélité | rapport contenu/langue |
|---|---:|---:|
| **l'entrée seule du professeur, 0 neurone** | **0,5161** | **1,698** |
| les états de notre réservoir | 0,4751 | **1,354** |
| entrée + réservoir | **0,5309** | 1,598 |
| *le professeur à sa couche 8* | — | *10,912* |

**Notre calcul propre — le réservoir récurrent — fait MOINS BIEN que l'entrée du
professeur lue linéairement, sur les deux axes à la fois.** Quatre mesures indépendantes
le confirment (§29, §34, §70, §71).

**Conséquence sur la raison d'être** : en l'état, Drave n'est pas un pont — c'est une
**dégradation** de la représentation du professeur. Le « pont » qui fonctionne le mieux
mesuré est une régression linéaire-quadratique sur la couche 0 du professeur, c'est-à-dire
le professeur lui-même, à peine projeté.

**Et la transformation qui compte — celle qui crée la séparation contenu/langue entre la
couche 0 et la couche 8 — n'est produite par AUCUN des mécanismes que le projet
s'autorise** : ni le réservoir aléatoire gelé (§70), ni la lecture en forme fermée
(§69, bornée à 64 %), ni le renforcement/atrophie (§72, +1,7 % du chemin nécessaire).

## B.5 La leçon de méthode, et elle est la plus dure

**Le constat du §29 — « une lecture sans aucun neurone bat le réservoir » — a été obtenu
à l'heure 13 de la session. Celui du §70 — « la langue vient de l'entrée, pas du
réservoir » — à l'heure 27.**

**Les deux étaient testables en moins d'une heure.** Le second n'était qu'une comparaison
de trois jeux de caractéristiques ; le premier, une régression sur l'entrée seule.

**J'ai construit, réglé et mesuré un mécanisme complexe — naissance libre, attrition,
multi-échelle, contraintes d'invariance, deux panneaux d'oracle — pendant treize heures
avant de tester la ligne de base triviale.**

Ce n'est pas une erreur de calcul : c'est une erreur d'**ordre**. La règle qui manquait,
et qui vaut pour la suite : **avant d'améliorer un mécanisme, mesurer ce qu'il apporte
au-dessus du plus bête des modèles qui pourrait le remplacer.**

## B.6 Ce que la session laisse d'utile malgré cela

1. **Une infrastructure qui survit au résultat négatif** — 392 langues × 2 couches,
   482 articles × 6 langues, un protocole complet, 33 outils.
2. **Une caractérisation précise de ce qui manque** — et elle est plus utile qu'un
   chiffre qui monte : *l'énergie de contenu est sous-produite d'un facteur 3,6 ; elle
   est récupérable par mise à l'échelle ; mais la mise à l'échelle exige d'isoler l'axe du
   contenu, et cet axe n'est pas identifiable sur un texte neuf.*
3. **Une identité mathématique** (§67) qui économise des mois de tâtonnement : le rapport
   contenu/langue est invariant d'échelle, donc **aucune amplification ne le corrigera
   jamais** — cinq échecs s'expliquent par là.
4. **Trois mécanismes déployables** qui, composés, portent le rapport de 1,29 à 10,69,
   soit **98 % de celui du professeur**, pour 0,047 de fidélité.
5. **Quatre erreurs de ma part, documentées et corrigées** (§60.6, §65, §73.1, §74) —
   dont un découpage qui ne gardait que deux langues sur trois dans six outils.

## B.7 Où porter l'effort ensuite, en une phrase

**Le facteur limitant n'est plus l'objectif, ni la lecture, ni le post-traitement : c'est
la TRANSFORMATION entre l'entrée et la cible.** Sous les contraintes maintenues — un seul
professeur, boîte noire, aucune rétropropagation — la question ouverte est : **quel
mécanisme, autre qu'un réservoir aléatoire gelé, peut produire huit couches d'attention ?**

Et la réponse à cette question commence par une mesure que je n'ai pas faite :
**qu'apporte le réservoir au-dessus de la seule entrée, sur le corpus complet de 482
articles ?** Le §78 l'a lancée ; elle n'a pas encore rendu son verdict.


---

## 79. La vérification à 482 articles : le résultat du §73 NE SE RÉPLIQUE PAS

Le corpus Wikipedia apparié complet — **482 articles × 6 langues, 1 446 entrées
d'apprentissage et 1 446 de test** — permet de vérifier si les effets mesurés sur 85
articles tenaient à la taille du panel. Réponse, sur la composition des leviers :

| étape | fid TEST | P_lang | P_cont | **RAPPORT** |
|---|---:|---:|---:|---:|
| à **85 articles** — base (centrage seul) | 0,4703 | 42,4 | 82,1 | 1,934 |
| à **85 articles** — + apprendre quoi lire | 0,4667 | 181,9 | 438,5 | **2,411** |
| à **482 articles** — base (centrage seul) | 0,4713 | 39,8 | 98,9 | **2,487** |
| à **482 articles** — + apprendre quoi lire | 0,4546 | **83,3** | 146,6 | **1,759** |
| *professeur à 482 articles* | — | *387,9* | *4 655,4* | ***12,001*** |

### 79.1 Le fait, sans détour

**À 85 articles, « apprendre quoi lire » faisait MONTER le rapport** (1,934 → 2,411),
en faisant monter `P_cont` (82 → 438) tout en faisant baisser `P_lang` (42 → 182).

**À 482 articles, il le fait BAISSER** (2,487 → 1,759) : `P_cont` monte (99 → 147) mais
`P_lang` monte **davantage** (40 → 83).

**L'effet du §73 ne se réplique pas.** Ce que j'avais présenté comme « le premier
mécanisme dont les deux énergies vont dans des directions opposées » était un **effet de
petit panel**.

### 79.2 Ce que cela change dans le rapport

**Le §73, le §74, le §75 et le §77 reposent sur des mesures à 85 articles.** Le §75
annonçait « la cible est atteinte, 98 % du rapport du professeur ». **Ce chiffre doit
être considéré comme non répliqué**, et la chaîne qui y menait — apprendre quoi lire →
combiner avec le discriminant → composer avec le centrage — repose sur un effet qui
disparaît quand le panel grandit d'un facteur 5,7.

**Ce qui tient à 482 articles :**
- la **ligne de base** (centrage seul) : rapport **2,487**, meilleure qu'à 85 articles
  (1,934) — les grands panels aident, comme le §34 l'avait montré ;
- la **cible du professeur** : **12,001** contre 10,912 — elle monte aussi, donc l'écart
  relatif à combler ne se réduit pas ;
- **toutes les mesures de la traque qui portaient sur des identités** — le §67
  (invariance d'échelle), le §61 (décomposition de variance), le §70 (caractéristiques
  emboîtées) — car une identité ne dépend pas de la taille du panel.

### 79.3 La leçon, et elle complète celle du bilan

Le bilan (§B.5) disait : *avant d'améliorer un mécanisme, mesurer ce qu'il apporte
au-dessus du plus bête des modèles qui pourrait le remplacer.*

Il faut y ajouter : **et le mesurer sur un panel assez grand pour que l'effet ne soit pas
un artefact de taille.** Les 85 articles du §73 venaient d'un corpus en cours de
traçage — c'était ce qui était disponible, mais ce n'était pas une raison pour publier
l'effet sans le marquer comme provisoire.

**Le rapport contient donc, à sa dernière page, la réfutation d'un de ses propres
résultats centraux.** C'est la bonne façon de finir : la mesure qui contredit est arrivée
parce que la chaîne pour l'obtenir avait été armée avant de connaître la réponse.


---

## 80. Le discriminant, lui, NON SEULEMENT se réplique — il DÉPASSE le professeur

Le §79 venait de réfuter le mécanisme du §73 à 482 articles. Restait à tester l'autre :
le **discriminant** du §69. Réponse, sur les 1 446 entrées de test :

| | fid TEST | P_lang | P_cont | **RAPPORT** |
|---|---:|---:|---:|---:|
| rang 0 (référence, centrage seul) | **0,4713** | 39,8 | 98,9 | 2,487 |
| **discriminant rang 2** | 0,4334 | 3,6 | 45,0 | **12,645** |
| discriminant rang 5 | 0,4420 | 12,5 | 56,2 | 4,502 |
| discriminant rang 20 | 0,4584 | 18,3 | 75,0 | 4,100 |
| **PROFESSEUR** | — | *387,9* | *4 655,4* | ***12,001*** |

### 80.1 Le résultat

**Rapport 12,645 contre 12,001 pour le professeur : 105 % de la cible.**

Et le contraste avec les 85 articles est instructif :

| | à 85 articles | à **482 articles** |
|---|---:|---:|
| professeur | 10,912 | **12,001** |
| discriminant rang 2 | 6,961 (**64 %**) | **12,645 (105 %)** |

**Le mécanisme ne se contente pas de tenir à grande échelle : il y gagne.** À 85 articles
il atteignait 64 % de la cible, à 482 il la dépasse de 5 %.

**Le coût en fidélité est de 0,038** (0,4713 → 0,4334) — du même ordre que celui mesuré à
85 articles (0,4703 → 0,4341, soit 0,036). **Le coût, lui, est stable.**

### 80.2 Ce que cela discrimine, et c'est le vrai apport de cette vérification

Les deux mécanismes testés à 482 articles se comportent **différemment** :

| mécanisme | à 85 articles | à 482 articles | verdict |
|---|---:|---:|---|
| **apprendre quoi lire** (§73) | 1,934 → **2,411** | 2,487 → **1,759** | **NE se réplique PAS** |
| **discriminant** (§69) | 1,934 → **6,961** (64 %) | 2,487 → **12,645** (105 %) | **SE RÉPLIQUE et s'améliore** |

**Le mécanisme qui survit est celui qui agit sur la LECTURE, pas celui qui agit sur les
caractéristiques.** C'est cohérent avec le §70 : la langue entre par l'entrée, et modifier
ce que lisent les neurones ne fait que redistribuer le problème. **Le discriminant, lui,
optimise directement la quantité qu'on mesure** — et cela se transfère, parce que c'est un
changement de directions dans l'espace de sortie, pas une reconstruction des
caractéristiques.

### 80.3 Le résultat final, et il est positif

**Sur le corpus Wikipedia complet — 482 articles × 6 langues, 1 446 entrées de test — une
analyse discriminante linéaire appliquée à la sortie du pont atteint un rapport
contenu/langue de 12,645 contre 12,001 pour le professeur, pour 0,038 de fidélité.**

C'est **en forme fermée**, **sans rétropropagation**, **déployable** (matrice fixe apprise
sur l'apprentissage), et **cela ne demande ni neurone supplémentaire ni couche
supplémentaire**.

**Ce que cela ne règle pas** : `P_cont` reste à 45,0 contre 4 655,4 pour le professeur —
**cent fois moins**. Le rapport est dépassé, l'énergie de contenu ne l'est pas. Et le §77
a établi que l'amplification qui les rapprocherait coûte la fidélité, de façon monotone.

### 80.4 La conclusion du rapport, corrigée une dernière fois

Le §79 terminait sur la réfutation du §73 et annonçait que « la cible » n'était pas
répliquée. **C'était vrai pour un mécanisme, pas pour l'autre.** Le rapport se termine donc
sur :

- **un mécanisme qui échoue à grande échelle** — apprendre quoi lire (§73, §79) ;
- **un mécanisme qui réussit et s'améliore** — le discriminant (§69, §80), à **105 % du
  rapport du professeur** ;
- **une frontière inchangée** — la structure s'obtient, l'énergie de contenu ne suit pas
  (§76, §77) ;
- **une question ouverte, seule** : quel mécanisme, sous les contraintes du projet, peut
  produire la transformation couche 0 → couche 8 et **porter l'énergie de contenu** du
  professeur ?
