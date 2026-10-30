# A8.0 — `porte-c4-retard` épingle la PPL du retard : 14,6496 → 9 277,9771

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **quatorzième porte
> épinglée** — le modèle entier, les retards 0/1/8 et l’état manquant sont ancrés. A8.0 reste
> **partielle** : 14 portes sur 33.
>
> **Dispositif** : `tools/porte-c4-retard.sh`, Qwen2.5-0.5B Q8_0, 128 jetons, couches 0:24 ;
> tolérance **5e-4** ; données [`a80-porte-c4-retard.json`](a80-porte-c4-retard.json).

## Ce qui est mesuré

| mesure | PPL |
|---|---:|
| modèle entier | **14,6496** |
| retard 0 | **14,6496** |
| retard 1 | **9 277,9771** (×633) |
| retard 8 | **151 517,0001** (×10 343) |
| état manquant (1 position) | **15,5295** (×1,06) |

La porte **exit 0** : un état n’est valide qu’à sa position ; manquer coûte **×1,06**,
réutiliser coûte **×633**.

## Le contrôle négatif

La condition est numérique : `abs(ppl - attendu) <= 5e-4 × attendu` sur les cinq références. Un
décalage de **10 %** est refusé par la même expression.

## Ce qui pourrait le rendre faux

- **Un seul modèle** ; 128 jetons.
- **Les très grandes PPL** sont des bornes, pas des qualités.
- **Le retard** est imposé par le banc, pas par un réseau réel.
- **5e-4** attrape 0,05 %, pas 0,01 %.

## Ce que ça change

A8.0 passe de **13/33** à **14/33**. N3.4c est une condition (placement natif = métadonnée) ;
la composition native complète reste ouverte.

## Fichiers

- `tools/porte-c4-retard.sh` — cinq PPL épinglées.
- `reports/a80-porte-c4-retard.json` — les mesures.
- `reports/rapport-a80-porte-c4-retard.md` — cette fiche.
