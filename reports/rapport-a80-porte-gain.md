# A8.0 — `porte-gain` épingle la courbe du gain FFN

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **huitième porte
> épinglée** — la référence, l’optimum intérieur et la falaise sont ancrés. A8.0 reste
> **partielle** : 8 portes sur 33.
>
> **Dispositif** : `tools/porte-gain.sh`, Qwen2.5-0.5B Q8_0, 128 jetons (256 pour le point
> §7) ; références **14,6496** (sans réglage), **12,9635** (gain 0,75), **15,4298** (1,5),
> **14,1057** (0,5), **996,0390** (0,25) ; tolérance **5e-4** ; données
> [`a80-porte-gain.json`](a80-porte-gain.json).

## Ce qui est mesuré

| point | PPL |
|---|---:|
| sans réglage | **14,6496** |
| gain 0,5 couche 0 | **14,1057** |
| **gain 0,75 couche 0** | **12,9635** |
| gain 1,5 couche 0 | **15,4298** |
| **falaise 0,25 couche 0** | **996,0390** |

La porte **exit 0** : identité du gain 1,0, inhibition monotone, optimum intérieur, falaise,
profil non composable, réparti, puits conditionnels.

## Le contrôle négatif

La condition est numérique : `abs(ppl - attendu) <= 5e-4 × attendu` sur les cinq références.
Un décalage de **10 %** est refusé par la même expression. Le contrôle porte sur la valeur, pas
sur les inégalités internes.

## Ce qui pourrait le rendre faux

- **Un seul modèle** et un seul corpus ; 128 jetons (256 pour §7).
- **996,0390** est une falaise, pas une qualité : elle est épinglée comme borne.
- **La magnitude décroît avec la fenêtre** (11,5 % à 128, 1,4 % à 256) : la valeur est liée à
  la longueur.
- **5e-4** attrape 0,05 %, pas 0,01 %.

## Ce que ça change

A8.0 passe de **7/33** à **8/33**. La prochaine est `porte-prefill-reparti` (si elle existe) ou
`porte-c2` ; A8.3 reste **opt-in** ; A8.3a est fait pour flux, pont et coupe.

## Fichiers

- `tools/porte-gain.sh` — cinq PPL épinglées.
- `reports/a80-porte-gain.json` — les mesures.
- `reports/rapport-a80-porte-gain.md` — cette fiche.
