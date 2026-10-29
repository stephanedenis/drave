# A8.0 — `porte-budget` épingle sa PPL : 111,9225

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **sixième porte
> épinglée** — la PPL du découpage sans budget est ancrée, et les budgets généreux ne la changent
> pas. A8.0 reste **partielle** : 6 portes sur 33.
>
> **Dispositif** : `tools/porte-budget.sh`, Qwen2.5-0.5B Q8_0, topologie à deux régions ;
> référence **111,9225**, tolérance **5e-4** ; données [`a80-porte-budget.json`](a80-porte-budget.json).

## Ce qui est mesuré

| cas | PPL | code |
|---|---:|---:|
| sans budget | **111,9225** | 0 |
| budget généreux | **111,9225** | 0 |
| budget de latence généreux | **111,9225** | 0 |
| budget insuffisant | aucune | 6 |
| latence insuffisante | aucune | 8 |
| paires insuffisantes | aucune | 9 |

La porte **exit 0** ; la PPL est épinglée et les budgets insuffisants **ne rendent aucun résultat
partiel** — c’est le contrôle de conception de C10.

## Le contrôle négatif

La condition est numérique : `abs(ppl - 111,9225) <= 5e-4 × 111,9225`. Un décalage de **10 %** est
refusé par la même expression. Le contrôle porte sur la valeur, pas sur l’égalité entre les runs.

## Ce qui pourrait le rendre faux

- **Un seul modèle et une topologie** : deux régions, Qwen2.5-0.5B Q8_0.
- **Les budgets insuffisants** ne mesurent pas une PPL : ils vérifient l’arrêt, pas la qualité.
- **La latence mesurée** dépend de la machine (19,5–21,9 ms à 1 ms de budget).
- **Une seule valeur** : les budgets généreux partagent la même référence ; une dérive locale
  pourrait passer si elle est identique partout.

## Ce que ça change

A8.0 passe de **5/33** à **6/33** portes épinglées. La prochaine est `porte-adaptateur-sortie`
(7,4242) ou `porte-gain` (29,0206). A8.3 reste **opt-in**.

## Fichiers

- `tools/porte-budget.sh` — PPL épinglée.
- `reports/a80-porte-budget.json` — les mesures.
- `reports/rapport-a80-porte-budget.md` — cette fiche.
