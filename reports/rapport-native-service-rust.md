# N4.3 — service Rust natif avec cache KV : 611 ms

> **Objet.** Servir `drave-n0` depuis le moteur Rust, avec cache KV par requête, sans passer par
> Python ni par un GGUF.

## Dispositif

- DRVM : `/tmp/n0-native.drvm`, **11 469 192** paramètres.
- Serveur : `drave --drvm-serve FILE 8766`, std seul (`TcpListener`).
- Routes : `GET /sante`, `POST /generer?n=32` (corps = prompt brut).
- Cache : `Cache::default()` par requête.

## Résultat

```text
GET /sante
{"ok":true,"parametres":11469192}

POST /generer?n=32  corps: La France est un pays
{"octets":53,"ms":611.0,"texte":"La France est un payse de contenu de la couche 8 et l"}
```

| mesure | valeur |
|---|---:|
| octets | **53** |
| latence | **611 ms** |
| texte | identique au service Python |

## Lecture

- Le service **Rust** répond, avec le **même texte** que le service Python (N4.2) et que la génération
  cache (N0.9).
- La latence **611 ms** est proche des **592,6 ms** du CLI : le coût HTTP est faible.
- Le serveur est **mono-thread** : une requête à la fois, pas de concurrence.

## Verdict

**N4.3 — service Rust natif : atteint** (HTTP, cache KV, texte identique, 611 ms).

## Limites

- **Mono-thread**, une connexion à la fois.
- **Pas d'auth**, pas de TLS, pas de quota.
- **Pas de cache persistant** entre requêtes : le cache est reconstruit par requête.
- **Pas de test automatisé** : vérification par `curl`.

## Fichiers

- Code : [`drave-core/src/native.rs`](../drave-core/src/native.rs).
- JSON : [`native-service-rust.json`](native-service-rust.json).
