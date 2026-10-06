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
