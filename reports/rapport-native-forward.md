# N0.7 — exécution native DRVM : le moteur calcule sans GGUF

> **Objet.** Faire lire les tenseurs DRVM **directement** par le moteur Rust, sans `Gguf` en mémoire :
> `--drvm-forward` charge le DRVM, reconstruit les poids f32 et calcule la passe avant de `drave-n0`.

## Dispositif

- DRVM : `/tmp/n0-native.drvm`, 44 Mo, **11 469 192** paramètres, architecture dans `model.architecture`.
- Prompt : `La France est un pays`, **21 octets**.
- Code : [`drave-core/src/native.rs`](../drave-core/src/native.rs), CLI `drave --drvm-forward FILE "prompt"`.

## Résultat

| | Rust natif | Python (référence) |
|---|---:|---:|
| octet argmax | **101 `e`** | **101 `e`** |
| logit du top-1 | **9,9429** | **10,8232** |
| top-2 | espace **6,8355** | espace **8,5745** |
| top-3 | `Ã` **6,1602** | `Ã` **7,5609** |
| top-4 | `a` **5,7669** | `a` **6,5002** |
| top-5 | `.` **4,7802** | `,` **5,6266** |

## Lecture

- Le **top-1 est le même** : le moteur natif sait exécuter le graphe.
- Les **logits ne sont pas identiques** : **9,94** contre **10,82**, soit **0,88** d'écart. Le top-5
  diverge au cinquième rang.
- L'exécution est **lente** et **sans cache KV** : une séquence complète refaite à chaque appel.
- Ce n'est donc **pas** encore une parité numérique : c'est une **preuve d'exécution**.

## Verdict

**N0.7 — exécution native : atteint techniquement** (top-1 identique, pas de GGUF). **Parité des logits :
non atteinte** (0,88). La cause reste à localiser : attention locale, LayerNorm, k-WTA ou ordre des
tenseurs.

## Limites

- **Un seul prompt**, un seul modèle.
- **f32**, pas de quantification.
- **Pas de cache KV**, pas de batch.
- **Pas de test unitaire** de la passe avant ; seul le CLI est vérifié.
- **Top-1 identique** ne prouve pas la parité : le top-5 diverge.

## Fichiers

- Code : [`drave-core/src/native.rs`](../drave-core/src/native.rs).
- DRVM : `/tmp/n0-native.drvm` (non versionné).
