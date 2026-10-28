# N0.10 — cache KV : 19,25× plus rapide que le forward complet

> **Objet.** Mesurer le gain réel du cache N0.9 contre le même moteur qui refait
> toute la passe avant à chaque octet.

## Résultat

| mesure | cache | complet | gain |
|---|---:|---:|---:|
| 53 octets | **592,6 ms** | **11 406,9 ms** | **19,25×** |
| sortie | identique | identique | — |

- Même DRVM (`/tmp/n0-native.drvm`), même prompt, 32 octets générés.
- CLI : `--drvm-generate` (cache) et `--drvm-generate-full` (témoin).
- Sortie : `La France est un payse de contenu de la couche 8 et l` dans les deux cas.

## Lecture

- Le cache **divise le temps par 19,25** sur 53 octets.
- Les deux chemins donnent **exactement la même sortie** : le cache ne change pas le calcul.
- Le forward complet est **O(s²)** par octet ; le cache est **O(s)**.

## Verdict

**N0.10 — gain du cache : mesuré**, **19,25×**. Le cache est justifié et validé par la sortie.

## Limites

- **Un seul prompt**, **32 octets**.
- **CPU**, f32, scalaire : les temps absolus ne sont pas ceux d’un moteur optimisé.
- **Pas de test unitaire** du cache.

## Fichiers

- Code : [`drave-core/src/native.rs`](../drave-core/src/native.rs).
- JSON : [`native-cache-gain.json`](native-cache-gain.json).
