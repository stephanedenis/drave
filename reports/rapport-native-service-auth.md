# N4.4 — service durci : jeton, taille, n borné

> **Objet.** Avant tout alignement, empêcher le service local d'être un exécuteur ouvert : jeton
> optionnel, corps borné, nombre d'octets borné.

## Résultat

| essai | code |
|---|---:|
| `POST /generer` sans jeton | **401** |
| `POST /generer` avec `Authorization: Bearer secret` | **200** |
| corps max | **64 Ko** |
| `n` max | **256** octets |

- Le jeton est lu dans `DRAVE_TOKEN` ; sans variable, le service reste ouvert (usage local).
- Vérification par `curl`.

## Lecture

- Le service **refuse** une requête sans jeton quand `DRAVE_TOKEN` est posé.
- La taille du corps et `n` sont **bornés** : pas de génération infinie.
- **Ce n'est pas un alignement** : aucun SFT, aucun jeu instruction, aucun refus de contenu.
- Le modèle reste un **banc de mécanismes**.

## Verdict

**N4.4 — durcissement : atteint** ; **alignement minimal : non fait**. Il n'existe pas de corpus
instruction dans le dépôt, et un SFT de 11,47 M sans données ne serait pas un alignement.

## Limites

- **Jeton en clair** dans l'environnement, pas de TLS.
- **Un seul thread**.
- **Pas de rate limit**.
- **Aucun alignement** de contenu.

## Fichiers

- Code : [`drave-core/src/native.rs`](../drave-core/src/native.rs).
- JSON : [`native-service-auth.json`](native-service-auth.json).
