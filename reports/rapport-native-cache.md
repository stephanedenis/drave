# N0.9 — cache KV natif : même sortie, 0,59 s

> **Objet.** Ajouter un cache KV au moteur Rust natif pour ne pas recalculer les
> clés/valeurs des positions précédentes à chaque octet généré.

## Dispositif

- DRVM : `/tmp/n0-native.drvm`, **11 469 192** paramètres.
- Prompt : `La France est un pays`, **32** octets générés.
- Cache : par bloc, par tête, clés et valeurs des positions déjà vues.
- CLI : `drave --drvm-generate FILE "prompt" 32`.

## Résultat

| mesure | valeur |
|---|---:|
| octets produits | **53** |
| durée | **592,6 ms** |
| sortie Rust | `La France est un payse de contenu de la couche 8 et l` |
| sortie Python (même modèle) | **identique** |

- Le modèle Python de référence est `/tmp/drave-n0-pont.pt`, le même que le DRVM.
- La sortie est **greedy** et **déterministe**.

## Lecture

- Le cache **ne change pas** la sortie : Rust et Python donnent le même texte.
- Le cache évite de recalculer **toutes** les positions précédentes ; la génération reste
  **lente** car le forward Rust est scalaire, mais la complexité par octet est réduite.
- **Pas de baseline full-Rust** mesurée : le gain de temps n'est pas chiffré dans cette fiche.

## Verdict

**N0.9 — cache KV : atteint** (parité de sortie, cache par bloc/tête). Le **gain** de temps reste à
mesurer contre un forward complet Rust.

## Limites

- **Un seul prompt**.
- **Pas de comparaison** avec un forward complet Rust.
- **Greedy** seulement.
- **Pas de test unitaire** du cache.

## Fichiers

- Code : [`drave-core/src/native.rs`](../drave-core/src/native.rs).
- JSON : [`native-cache.json`](native-cache.json).
