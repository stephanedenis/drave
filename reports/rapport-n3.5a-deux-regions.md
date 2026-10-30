# N3.5a — le modèle natif coupé en deux régions est bit-exact

> **Ligne de roadmap** : N3.5a · **Date** : 2026-10-29 · **Verdict** : ✅ **le découpage
> 0..k / k..n rend exactement le modèle plein**, pour K = 0, 1, 2, 3, 4 et deux prompts. Le
> test unitaire `split_amont_aval_egal_pas` est vert. N3.5b (deux processus, TCP) reste.
>
> **Dispositif** : `Native::pas_amont`/`pas_aval` (extraction de `entree`, `traverser`, `tete`),
> CLI `--drvm-generate-split`, modèle 4 blocs (graine 7, 428 504 paramètres) ;
> porte `tools/porte-n3-deux-regions.sh` ; données [`n3.5a-deux-regions.json`](n3.5a-deux-regions.json).

## Deux bugs latents corrigés

1. **Pont à `n_blocks=1`** : `n_blocks/2 - 1` sous-débordait en debug (`cargo test` était
   **rouge**) et valait `usize::MAX` en release. Garde `n_blocks >= 2` aux deux endroits.
2. **`max_pos` en dur** (`pos.min(2047)`) : la fixture a 32 positions ; `--drvm-native-ppl`
   paniquait. `Cfg::max_pos` est maintenant lu de `pos.weight`, et le `min` l’utilise.

`cargo test --bin drave native::` : **2 tests verts**, dont le split bit-exact.

## Ce qui est mesuré

| K | sortie |
|---:|---|
| 0 | identique au plein |
| 1 | identique (pont dans l’aval) |
| 2 | identique (pont dans l’amont) |
| 3 | identique |
| 4 | identique |

Deux prompts (`abc`, `zzz`) ; le balayage K=0..4 couvre les deux côtés du pont.

## Le contrôle négatif

- **K=0 et K=4** encadrent le pont ; **K=1/K=2** le placent de chaque côté.
- **Prompt différent** : la référence et les splits suivent.
- **Bit-exact** : `assert_eq!` sur les logits, pas une tolérance.
- **La porte peut échouer** : un `b - k` relatif, une tête appliquée deux fois ou un pont perdu
  déplace la sortie et la comparaison le voit.

## Ce qui pourrait le rendre faux

- **Un seul processus** : c’est le découpage, pas encore le fil.
- **Aucun cache K/V transféré** : chaque région garde le sien ; c’est le choix du MVP.
- **Poids chargés en entier** des deux côtés en N3.5b : partage de calcul, pas de mémoire.
- **Modèle synthétique** 4 blocs ; le pont est testé aux deux positions.

## Ce que ça change

N3.5a est **fait** : le découpage par couches est prouvé bit-exact. N3.5b (deux processus, TCP
localhost, refus d’empreinte/K/position) reste ; il réutilise `pas_amont`/`pas_aval`.

## Fichiers

- `drave-core/src/native.rs` — `entree`/`traverser`/`tete`, `pas_amont`/`pas_aval`, bugs P0, test.
- `drave-core/src/main.rs` — `--drvm-generate-split`, `--drvm-generate-hex`.
- `tools/porte-n3-deux-regions.sh` — la porte.
- `reports/n3.5a-deux-regions.json` — les mesures.
- `reports/rapport-n3.5a-deux-regions.md` — cette fiche.
