# A8.0 — `porte-bus-socket` épingle la référence et les trois régimes : 113,0068 / 148,7080 / 42,3176 / 148,9144

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **dix-septième porte
> épinglée** — la référence, le gain statique, la ligne par socket, le plein vol et le bus du
> pilote sont ancrés. A8.0 reste **partielle** : 17 portes sur 33.
>
> **Dispositif** : `tools/porte-bus-socket.sh`, Qwen2.5-0.5B Q8_0, topologie à deux régions ;
> tolérance **5e-4** ; données [`a80-porte-bus-socket.json`](a80-porte-bus-socket.json).

## Ce qui est mesuré

| mesure | PPL |
|---|---:|
| référence, aucun bus | **113,0068** |
| gain statique `gain=2.0` | **148,7080** |
| ligne socket avant connexion | **148,7080** |
| modulation en plein vol | **42,3176** |
| bus du pilote modulé | **148,9144** |
| bus neutre | **identique au bit** |

La porte **exit 0** : le bus neutre ne change rien, le socket branché agit, le plein vol n’est ni
la référence ni le pas 0, le bus du pilote agit.

## Le contrôle négatif

La condition est numérique : `abs(ppl - attendu) <= 5e-4 × attendu` sur les quatre références.
Un décalage de **10 %** est refusé. Le contrôle porte sur la valeur, pas sur la simple différence.

## Ce qui pourrait le rendre faux

- **Un seul modèle** et une topologie à deux régions.
- **42,3176** est une modulation « en plein vol » : liée à l’instant, pas une qualité.
- **La PPL dépend de la limite** ; 113,0068 / 148,7080 / 148,9144 sont liés au montage.
- **5e-4** attrape 0,05 %, pas 0,01 %.

## Ce que ça change

A8.0 passe de **16/33** à **17/33**. Les portes mesurables restantes sont
`porte-profondeur-routee` (longue) et les rouges à qualifier. A8.3b/c et N3 suivent.

## Fichiers

- `tools/porte-bus-socket.sh` — quatre PPL épinglées.
- `reports/a80-porte-bus-socket.json` — les mesures.
- `reports/rapport-a80-porte-bus-socket.md` — cette fiche.
