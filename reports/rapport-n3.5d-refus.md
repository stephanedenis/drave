# N3.5d — l’empreinte du modèle refuse un aval divergent

> **Ligne de roadmap** : N3.5d · **Date** : 2026-10-29 · **Verdict** : ✅ **le protocole refuse**
> — deux modèles de mêmes formes mais de poids différents (pont nul) ont des empreintes
> différentes ; le client A contre l’aval B rend **REFUS, code 4, aucun logit**. Le même modèle
> reste **bit-exact**.
>
> **Dispositif** : `Native::empreinte` (FNV-1a 64 sur les poids triés), en-tête TCP ; porte
> `tools/porte-n3-refus.sh` ; données [`n3.5d-refus.json`](n3.5d-refus.json).

## Ce qui est mesuré

| paire | résultat |
|---|---|
| client A / aval B (pont nul) | **REFUS**, code **4**, aucun logit |
| client A / aval A | **succès bit-exact** |

Les deux modèles ont **428 504** paramètres et les mêmes formes ; seule l’empreinte les sépare.

## Le contrôle négatif

- **Mêmes formes, poids différents** : refus — l’empreinte ne compare pas que des dimensions.
- **Même modèle** : succès bit-exact — le refus n’est pas systématique.
- **Code 4** distinct de la panne (7) et du budget (6).
- **Aucun logit** dans le refus : pas de résultat partiel.

## Ce qui pourrait le rendre faux

- **Pas encore de session/position/génération** : l’empreinte protège le modèle, pas la
  désynchronisation de cache.
- **Localhost, sans auth/TLS** : ce n’est pas une frontière de sécurité.
- **Un seul forward** ; le coût de l’empreinte est linéaire aux poids (une fois au chargement).
- **Modèle synthétique**.

## Ce que ça change

N3.5a/b/c/d sont **faits** : découpage bit-exact, fichiers, TCP, refus d’empreinte.
N3.5e (sessions, positions, boucle de génération) reste.

## Fichiers

- `drave-core/src/native.rs` — `empreinte`.
- `drave-core/src/main.rs` — empreinte dans l’en-tête, refus code 4.
- `tools/porte-n3-refus.sh` — la porte.
- `reports/n3.5d-refus.json` — les mesures.
- `reports/rapport-n3.5d-refus.md` — cette fiche.
