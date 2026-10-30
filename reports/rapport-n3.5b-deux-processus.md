# N3.5b — deux processus, frontière par fichier, logits identiques

> **Ligne de roadmap** : N3.5b · **Date** : 2026-10-29 · **Verdict** : ✅ **deux processus**
> suffisent : l’amont écrit les hiddens de frontière, l’aval les relit et rend les **mêmes
> logits** que le `pas` plein, pour K=0..4 et deux prompts. N3.5c (TCP) reste.
>
> **Dispositif** : CLI `--drvm-split-amont` / `--drvm-split-aval` / `--drvm-pas-hex`, modèle
> 4 blocs (graine 7, 428 504 paramètres) ; porte `tools/porte-n3-deux-processus.sh` ;
> données [`n3.5b-deux-processus.json`](n3.5b-deux-processus.json).

## Le défaut trouvé

L’en-tête du fichier écrivait `d` en **`usize` (8 octets)** et le relisait en **`u32` (4)** :
tous les hiddens étaient décalés de 4 octets, et les logits ne ressemblaient à rien. Corrigé
(`d as u32`). C’est exactement le genre de bug que la comparaison bit-à-bit attrape.

## Ce qui est mesuré

| K | logits |
|---:|---|
| 0 | identiques au `pas` plein |
| 1 | identiques |
| 2 | identiques |
| 3 | identiques |
| 4 | identiques |

Prompt `abc` et `zzz` ; comparaison **bit-à-bit** (`{:08x}` des f32), pas une tolérance.

## Le contrôle négatif

- **K=0..4** couvre les deux côtés du pont.
- **Deux prompts** : le fichier ne fige pas un texte.
- **Deux processus séparés** : l’amont écrit, l’aval lit ; un décalage d’en-tête ou de position
  casse la comparaison.
- **Le bug d’en-tête** a été vu par cette porte avant d’être corrigé.

## Ce qui pourrait le rendre faux

- **Fichier, pas TCP** : ce n’est pas encore le réseau ; N3.5c.
- **Un seul forward**, pas une boucle de génération avec cache par pas.
- **Les deux processus chargent tous les poids** : partage de calcul, pas de mémoire.
- **Modèle synthétique** 4 blocs.

## Ce que ça change

N3.5b est **fait** : le découpage en deux processus est prouvé. N3.5c (TCP localhost, refus
d’empreinte/K/position) réutilise ces fonctions.

## Fichiers

- `drave-core/src/main.rs` — `--drvm-split-amont`, `--drvm-split-aval`, `--drvm-pas-hex`.
- `tools/porte-n3-deux-processus.sh` — la porte.
- `reports/n3.5b-deux-processus.json` — les mesures.
- `reports/rapport-n3.5b-deux-processus.md` — cette fiche.
