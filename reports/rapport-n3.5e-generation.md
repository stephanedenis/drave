# N3.5e — la génération est répartie sur deux processus TCP

> **Ligne de roadmap** : N3.5e · **Date** : 2026-10-29 · **Verdict** : ✅ **la boucle de
> génération passe le réseau** — l’amont garde son cache 0..k, l’aval son cache k..n, et la
> sortie est **bit-identique** à `generer` local pour K=0..4 et deux prompts.
>
> **Dispositif** : `--drvm-serve-gen`, `--drvm-gen-net`, modèle 4 blocs (graine 7, 428 504
> paramètres) ; porte `tools/porte-n3-generation.sh` ; données
> [`n3.5e-generation.json`](n3.5e-generation.json).

## Ce qui est mesuré

| K | génération |
|---:|---|
| 0 | identique à `generer` local |
| 1 | identique |
| 2 | identique |
| 3 | identique |
| 4 | identique |

Prompts `abc` et `zzz` ; comparaison hexadécimale exacte, pas une tolérance.

## Le contrôle négatif

- **K=0..4** : les deux côtés du pont.
- **Deux prompts**.
- **Deux caches** distincts : l’amont ne connaît que 0..k, l’aval que k..n.
- **Aucun cache K/V sur le fil** : hidden + logits seulement.
- **Empreinte** vérifiée à l’ouverture.

## Ce qui pourrait le rendre faux

- **Localhost, sans auth/TLS** : pas une frontière de sécurité.
- **Une session par connexion**, total de positions fixé à l’avance.
- **Pas encore de refus de désynchronisation de position** (N3.5f).
- **Modèle synthétique** 4 blocs.

## Ce que ça change

N3.5a (découpage), N3.5b (fichier), N3.5c (TCP forward), N3.5d (empreinte), N3.5e (génération)
sont **faits**. N3.5f devra ajouter sessions/positions/refus de désynchronisation.

## Fichiers

- `drave-core/src/main.rs` — `--drvm-serve-gen`, `--drvm-gen-net`.
- `tools/porte-n3-generation.sh` — la porte.
- `reports/n3.5e-generation.json` — les mesures.
- `reports/rapport-n3.5e-generation.md` — cette fiche.
