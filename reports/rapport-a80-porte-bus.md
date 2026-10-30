# A8.0 — `porte-bus` épingle le bus et le relais : 64,1160 / 59,0790 / 66,0379

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **quinzième porte
> épinglée** — la PPL du bus non neutre, du relais et du canal par fichier sont ancrées.
> A8.0 reste **partielle** : 15 portes sur 33.
>
> **Dispositif** : `tools/porte-bus.sh`, Qwen2.5-0.5B Q8_0, topologie à trois régions ;
> références **64,1160** (bus gain 1,5), **59,0790** (relais/file sans canal), **66,0379**
> (relais/file avec canal), tolérance **5e-4** ; données [`a80-porte-bus.json`](a80-porte-bus.json).

## Ce qui est mesuré

| mesure | PPL |
|---|---:|
| bus neutre | identique au bit |
| bus gain 1,5 | **64,1160** |
| relais sans bus | **59,0790** |
| relais avec bus | **66,0379** |
| fichier sans canal | **59,0790** |
| fichier avec canal | **66,0379** |

La porte **exit 0** : le bus neutre ne change rien, le bus non neutre change la PPL et les
empreintes, le bus traverse les instances et le canal par fichier agit.

## Le contrôle négatif

La condition est numérique : `abs(ppl - attendu) <= 5e-4 × attendu` sur les cinq références. Un
décalage de **10 %** est refusé. Le contrôle porte sur la valeur, pas sur la simple différence.

## Ce qui pourrait le rendre faux

- **Un seul modèle** et une topologie à trois régions.
- **La PPL dépend de la limite** ; 64,1160 / 59,0790 / 66,0379 sont liés à ce montage.
- **Le bus est un gain scalaire** ; le test ne dit pas qu’un bus plus riche serait neutre.
- **5e-4** attrape 0,05 %, pas 0,01 %.

## Ce que ça change

A8.0 passe de **14/33** à **15/33**. La prochaine est `porte-delais` ou `porte-bus-socket` ;
A8.3b/c et N3 restent les chantiers suivants.

## Fichiers

- `tools/porte-bus.sh` — cinq PPL épinglées.
- `reports/a80-porte-bus.json` — les mesures.
- `reports/rapport-a80-porte-bus.md` — cette fiche.
