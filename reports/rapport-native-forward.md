# N0.7 — exécution native DRVM : logits identiques, sans GGUF

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
| logit du top-1 | **10,8232** | **10,8232** |
| top-2 | espace **8,5744** | espace **8,5745** |
| top-3 | `Ã` **7,5609** | `Ã` **7,5609** |
| top-4 | `a` **6,5002** | `a` **6,5002** |
| top-5 | `,` **5,6266** | `,` **5,6266** |

## Lecture

- Les **logits sont identiques** à **0,0001** près, et le top-5 est le même dans le même ordre.
- La **cause** de l'écart initial de **0,88** était le **routeur** : le modèle Python calcule les poids
  du top-k mais **ne les applique pas** à `h`. Le Rust les multipliait ; retirer cette multiplication
  a suffi.
- Le moteur exécute donc le **même graphe** que l'entraîneur, sans `Gguf`, sans fichier temporaire.

## Verdict

**N0.7 est atteint** : **logits identiques** à 0,0001 près, **top-5 identique**, **sans GGUF**. Le
routeur non appliqué était la seule cause de l'écart.

## Limites

- **Un seul prompt**, un seul modèle.
- **f32**, pas de quantification.
- **Pas de cache KV**, pas de batch.
- **Pas de test unitaire** de la passe avant ; seul le CLI est vérifié.
- **Pas de cache KV** : la passe avant est O(s²) et lente.
- **Un seul prompt** ; la parité demande plusieurs prompts et un test automatique.

## Fichiers

- Code : [`drave-core/src/native.rs`](../drave-core/src/native.rs).
- DRVM : `/tmp/n0-native.drvm` (non versionné).
