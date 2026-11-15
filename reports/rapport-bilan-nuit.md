# Le bilan de la nuit du 14 au 15/11 — le tagger, la base honnête, la phase C/B

> **Ce que ce bilan est.** La synthèse de la nuit (23 h 30 → 04 h 45) : les décisions exécutées
> (1A → 6A), les mesures, les négatifs, et l'état du dépôt. **Aucune mesure nouvelle** n'est
> revendiquée : chaque chiffre renvoie à sa fiche.

## 1. Le produit (6A)

| chantier | résultat | fiche |
|---|---|---|
| **le tagger en option** (`--tagger`) | POS **95,75 %** sur 612 (+9,5), **95,00 %** sur le réel 452 (+6,1) ; **1 appel**/phrase ; `PONCT` restitué ; ~0,02 $ | [`rapport-tagger-option.md`](rapport-tagger-option.md) |
| **la base honnête** (`--reel`) | 452 phrases : POS **88,91 %**, F1 **79,06 %**, attachement **99,46 %** ; publiée à côté du global | [`rapport-base-reelle.md`](rapport-base-reelle.md) |
| **les tests** | 14 tests tagger (0 réseau) + 20 tests produit ; porte produit **verte** | — |

## 2. La coordination (C)

| tâche | résultat | fiche |
|---|---|---|
| **N2** | la commande **validée** : `--rope --canal-dir` (2,79) ; `--rope` seul = 40,07 ; le témoin **3,09** | [`rapport-coordination-n2-v2.md`](rapport-coordination-n2-v2.md) |
| **S** | la page `/` **ne sert pas la v7** ; les **11 verdicts** committés (`389b99f`) | [`rapport-coordination-s-v2.md`](rapport-coordination-s-v2.md) |
| **R** | le « gold 200+ » **défini** : 452 phrases ; **50 ratées** sélectionnées | [`rapport-gold-reel-50.md`](rapport-gold-reel-50.md) |

## 3. Panini (B)

| tâche | résultat | fiche |
|---|---|---|
| **le protocole à date contrôlée** | 60 paires en 3 strates ; le §334 ne fournit **qu'une** paire contemporaine mesurée | [`rapport-protocole-date.md`](rapport-protocole-date.md) |
| **les atomes ↔ niveaux** | ❌ **négatif net** : POS R²CV **−0,092**, syntagmes **−0,160**, attachement **−0,092** ; le contrôle de date tue le seul signal | [`rapport-atomes-prediction.md`](rapport-atomes-prediction.md) |
| **le CIC v2** | **42/42** verdicts, les types de de Bruijn **clos**, le sha256 **sans `hashlib`**, **1 020/1 020** mutations rejetées | [`rapport-cic-v2.md`](rapport-cic-v2.md) |

## 4. Les négatifs, dits

- **Les atomes ne prédisent pas les niveaux** : c'est un **résultat**, pas un échec — l'intégration
  Panini est **bornée** au style/époque.
- **Le protocole à date contrôlée** ne peut pas être rempli par le §334 (une seule paire) : il faut
  **de nouvelles données**.
- **La page `/` de S** ne sert pas la v7 : c'est une action pour la session S.

## 5. L'état

`HEAD c24253ee` + les commits de la nuit ; **tous poussés** (`master` = `s/v7`, 0 divergence) ;
**183/183** d'autotest ; la porte produit **verte** (12 contrôles) ; la doc à jour (les trois
bases, le tagger, les fiches C/B indexées) ; les décisions **1A-6A** inscrites.

**Ce qui reste pour la suite** : le **gold réel étendu** (les 50 phrases de C3, à annoter par S),
la **page `/`** (S), le **corpus à date contrôlée** (Panini, de nouvelles données), et la
**restitution v2**.
