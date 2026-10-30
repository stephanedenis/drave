# N3.5c — deux processus, frontière TCP, logits identiques

> **Ligne de roadmap** : N3.5c · **Date** : 2026-10-29 · **Verdict** : ✅ **le découpage passe
> le réseau** — deux processus TCP localhost, K=0..4, deux prompts, logits **bit-à-bit
> identiques** au `pas` plein. Aucun cache K/V ne traverse. N3.5d (sessions/refus/boucle de
> génération) reste.
>
> **Dispositif** : `--drvm-serve-aval`, `--drvm-split-net`, `--drvm-pas-hex`, modèle 4 blocs
> (graine 7, 428 504 paramètres) ; porte `tools/porte-n3-reseau.sh` ; données
> [`n3.5c-reseau.json`](n3.5c-reseau.json).

## Le défaut trouvé

Le serveur utilisait **son** K de ligne de commande, pas celui du client : le premier test K=0
échouait. K est maintenant **dans l’en-tête** (`n, d, k`), le serveur le lit et le borne.

## Ce qui est mesuré

| K | logits |
|---:|---|
| 0 | identiques |
| 1 | identiques |
| 2 | identiques |
| 3 | identiques |
| 4 | identiques |

Prompts `abc` et `zzz` ; comparaison `{:08x}` des f32.

## Le contrôle négatif

- **K=0..4** : les deux côtés du pont.
- **Deux prompts** : le fil ne fige pas un texte.
- **Deux processus** : l’amont envoie, l’aval calcule ; un K désaccordé casse la comparaison
  (c’est le bug trouvé).
- **Aucun cache K/V sur le fil** : seuls `n, d, k` et les hiddens de frontière.

## Ce qui pourrait le rendre faux

- **Localhost seulement**, sans auth ni TLS : ce n’est pas une frontière de sécurité.
- **Un seul forward**, pas une boucle de génération avec sessions.
- **Les deux processus chargent tous les poids** : partage de calcul, pas de mémoire.
- **Modèle synthétique** 4 blocs.

## Ce que ça change

N3.5a (découpage bit-exact), N3.5b (deux processus fichier) et N3.5c (TCP) sont **faits**.
N3.5d devra ajouter session/refus/empreinte et la boucle de génération ; B11.10 reste.

## Fichiers

- `drave-core/src/main.rs` — `--drvm-serve-aval`, `--drvm-split-net`.
- `tools/porte-n3-reseau.sh` — la porte.
- `reports/n3.5c-reseau.json` — les mesures.
- `reports/rapport-n3.5c-reseau.md` — cette fiche.
