# Le bilan du 15/11 — la semaine 2 en un jour : le tagger décidé, le gold nommé, les rôles séparés

> **Ce que ce bilan est.** La synthèse de la **journée du 15/11** (08 h 15 → 16 h) : les six
> vagues de la semaine 2 (W1-W6) et les trois tâches du pilote (X1-X3), les chiffres, les
> négatifs, la décision du tagger. **Aucune mesure nouvelle** : chaque chiffre renvoie à sa fiche.

## 1. Les vagues mesurées

| vague | résultat | fiche |
|---|---|---|
| **W1** le gold réel 452 | 20 hand + 432 corpus, **242 fr / 210 en**, le split **402 / H50** figé, le sha256, **10 GP/SUB** listés (184 → 194 cibles) | [`rapport-gold-452.md`](rapport-gold-452.md) |
| **W2** le tagger sur 402/H50 | 402 **0,9198 → 0,9643** (**+4,45**) ; H50 **0,6842 → 0,8607** (**+17,65**) ; F1 et attachement du 402 **inchangés** | [`rapport-tagger-h50.md`](rapport-tagger-h50.md) |
| **W3** la matrice du défaut | défaut **hors ligne, code 0, 0 socket** ; `--tagger` opt-in ; clé invalide **4** ; réseau coupé **0** après 3 essais ; 1 000 phrases = **143 870 tokens** | [`rapport-tagger-defaut.md`](rapport-tagger-defaut.md) |
| **W4** Panini | le manifeste des **26 signatures** prêt ; le rejeu **27/60** (33 manquantes) — **pas un test**, aucune p-value | [`rapport-panini-manifeste.md`](rapport-panini-manifeste.md) |
| **W5** la restitution v3 | les 5 rôles de GP se **séparent** (S : **18/18**, **144/144**, permutation **0/18**) ; le cadre ne suit pas (v2 : **20/46**, F1 0,5406) | [`rapport-restitution-v3.md`](rapport-restitution-v3.md) |
| **W6** la clôture | 5 vagues, 3 positives, 1 bloquée, 1 mixte ; tag `semaine-2-2026-11-20` | [`rapport-semaine-2.md`](rapport-semaine-2.md) |
| **X1** la page `/` | **369/0** (l'ancien banc) contre **359/99** (la v7) ; la recette | [`rapport-page-s-mesure.md`](rapport-page-s-mesure.md) |
| **X2** l'or de rôles | le protocole pour S, le **schéma** (`schema-or-roles.json`), la base v1 | [`rapport-or-roles-protocole.md`](rapport-or-roles-protocole.md) |
| **X3** le tagger en lot | 1 000 items, 672 appels, **99 971 tokens**, **87,6 items/min**, **0,022 $** ; **0 $ en cache chaud** | [`rapport-tagger-lot.md`](rapport-tagger-lot.md) |

## 2. La décision du tagger (J5)

**La recommandation, appuyée par la mesure** : le **défaut reste hors ligne** (code 0, 0 socket,
déterministe) ; `--tagger` est **opt-in** ; un mode `auto` seulement si la clé existe et **sans
changer le code de sortie**. Les raisons : le gain est **+4,45 sur 402** mais le **fermé baisse
(−1,55)** ; le coût est **0,022 $/1 000** (négligeable) mais le réseau n'est pas toujours là ; et
le produit doit rester utilisable **sans clé**.

**Ce que la mesure ne tranche pas** : le mode `auto` (la clé présente → automatique) — il change
le comportement selon l'environnement, ce qui est une **décision d'humain**.

## 3. Les négatifs, dits

- **Panini** : le rejeu n'est **pas un test** (27/60 paires, aucune p-value) ; les **26
  signatures** manquent — le manifeste est prêt, la balle est chez eux.
- **La restitution v3** : les rôles se séparent mais la **fidélité du cadre** ne suit pas (20/46).
- **La page `/`** : S doit migrer (l'ancien banc sert toujours).

## 4. L'état

`master` = `s/v7`, **0 divergence** ; le tag **`semaine-2-2026-11-20`** ; **183/183** d'autotest ;
la porte produit **verte** ; les portes de doc vertes ; la file du chantier à **53 tâches**.

## 5. Ce qui reste (la suite)

1. **S** : les 10 GP/SUB du gold 452, la page `/` (la migration), l'or de rôles (le protocole X2).
2. **Panini** : envoyer le manifeste des 26 signatures, recevoir les signatures, rejouer les 60
   paires (le protocole B1).
3. **La décision du tagger `auto`** : un humain.
4. **La restitution v4** : le cadre (le goulot est nommé).
