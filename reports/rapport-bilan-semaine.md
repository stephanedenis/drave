# Le bilan de la semaine (07 → 15/11) — le produit gagne 3,7 points, Panini est borné, le harnais tient

> **Ce que ce bilan est.** La **synthèse de la semaine** : le produit, Panini, la coordination, le
> méta-harnais. **Aucune mesure nouvelle** : chaque chiffre renvoie à sa fiche. Il est écrit pour
> être lu en 5 minutes, pas pour remplacer les fiches.

## 1. Le produit — les chiffres, avec leur base

| mesure | avant (07/11) | **après (15/11)** | base |
|---|---:|---:|---|
| **F1 syntagmes** | 0,7533 | **0,7902** (+3,69) | vivant 612 |
| F1 syntagmes (réel) | — | **0,7906** | réel 452 |
| **POS** | 0,8625 | 0,8625 | vivant 612 |
| POS (réel) | — | **0,8891** | réel 452 |
| POS avec `--tagger` | — | **0,9575** (612) · **0,9500** (réel) | API |
| **attachement exact** | 236/237 | **238/239** (0,9958) | vivant 612 |
| attachement (réel) | — | **99,46 %** | réel 452 |
| exact sur span | 1,0000 | **1,0000** | vivant 612 |
| spans perdus | 2 | **1** (`g017`, inatteignable) | vivant 612 |

**Les trois bases** : le **vivant 612** (20 main + 432 corpus + 160 synthétiques), le **gelé 602**
(la référence figée) et le **réel 452** (`--reel`, hand + reel, sans synthétique). Les chiffres
globaux et réels sont **publiés ensemble** depuis le 15/11.

## 2. Ce que le produit a gagné

- **Le tagger en option** (`--tagger`) : +8,49 pts sur 612, +6,1 sur le réel ; 1 appel/phrase,
  ~0,02 $, la ponctuation restituée ; le défaut reste hors ligne.
- **La base honnête** (`--reel`) : le chiffre réel à côté du global.
- **Le schéma v2** (`meta.partition`/`meta.alternative`), v1 toujours lue.
- **La restitution** : v0 (surface 46/46), v1 (canonique), v2 (**négatif** : les rôles ne se
  restituent pas — 19/46, F1 0,527).
- **Les 50 textes** libres (0 plantage, 50/50 v2), **les 5 exemples** rejoués, **la FAQ** (10/10
  vérifiées), **la mesure par langue** (fr 0,8159 / en 0,9451).
- **La clôture** : 84 portes, **82 vertes**, 2 rouges structurelles nommées (`indice`, `melange`),
  `porte-sessions` repassée verte ; **183/183** d'autotest.

## 3. Panini — mesuré, borné, et deux négatifs utiles

| intégration | résultat |
|---|---|
| **la table 14 atomes × 8 niveaux** | 14/14 lignes, 33 paires colinéaires |
| **le corpus commun UDHR** | 418/438 paires exactes |
| **le retrieval par famille** | sœurs **0,619** vs 0,0445 — **mais seulement dans la même écriture** |
| **la généalogie à deux faces** | 154/154 paires hors script ; la famille vit dans 2-3 paires |
| **le §334** | leur loi H0 **reproduite** (R² 0,909) ; leur β époque **+0,138 non reproduit** (−0,006) ; le plan est **colinéaire** |
| **les atomes comme prédicteurs** | ❌ **négatif** : POS R²CV −0,092, syntagmes −0,160 ; le contrôle de date tue tout |
| **le corpus d'or CIC** | **42/42**, les types de de Bruijn clos, le sha256 **sans `hashlib`**, 1 020/1 020 mutations rejetées |
| **le protocole à date contrôlée** | 60 paires en 3 strates ; le §334 ne fournit **qu'une** paire contemporaine |

**La leçon** : les atomes captent un **gradient de style/époque**, pas la syntaxe ; l'intégration
Panini est **bornée**, et le **négatif est un résultat**.

## 4. La coordination — les actions sont chez les sessions

- **N2** : la commande **validée** `--rope --canal-dir` (2,79) ; `--rope` seul = 40,07 ; le témoin
  **3,09**.
- **S** : les **11 verdicts** committés (`389b99f`) ; la page `/` **ne sert pas la v7**.
- **R** : le tagger **intégré** ; le « gold 200+ » **défini** (452), 50 ratées sélectionnées.
- **A** : A6.2 **repoussé** (décision 5A).

## 5. Le méta-harnais — 38 lancements, 3 leçons

**Les faits** : 38 lancements, ~12 h d'agent, **31 tâches livrées** (3 timeouts après commit,
requalifiés « fait » par la règle *acceptation d'abord*), 1 plan perdu puis restauré. **Les trois
corrections** apprises en production : la **clé** (`~/.config/drave/deepseek.key`), le **worktree
jamais propre** (dépôt multi-sessions), le **plan relu à chaque tour**.

## 6. Les décisions (1A → 6A) et leur état

| # | décision | état |
|---|---|---|
| **1A** | le tagger en option | ✅ livré (`--tagger`) |
| **2A** | `g017` inatteignable | ✅ inscrit |
| **3B** | les 11 verdicts committés | ✅ (`389b99f`) |
| **4A** | la note Panini | ✅ écrite (`note-panini-334.md`), **à envoyer** |
| **5A** | A6.2 repoussé | ✅ inscrit |
| **6A → C → B** | l'ordre | ✅ exécuté (produit → coordination → Panini) |

## 7. L'état et ce qui reste

**L'état** : `master` = `s/v7`, **0 divergence** ; les tags `chantier-2026-11-14` et
`semaine-2026-11-14` ; **183/183** d'autotest ; la porte produit verte (12 contrôles) ; la doc à
jour (les trois bases, la FAQ, les fiches indexées).

**Ce qui reste** :
1. **Envoyer la note à Panini** (l'humain).
2. **Le gold réel étendu** : les 50 phrases de C3, à annoter par la session S.
3. **La page `/`** : la session S doit la servir.
4. **Le corpus à date contrôlée** : de nouvelles données (le §334 ne suffit pas).
5. **La restitution v3** : les rôles ne suivent pas (le négatif de D2) — un vrai sujet de recherche.
