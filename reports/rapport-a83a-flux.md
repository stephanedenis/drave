# A8.3a — `porte-flux` : le régime 1 % a ses propres références

> **Ligne de roadmap** : A8.3a · **Date** : 2026-10-29 · **Verdict** : ✅ **le régime 1 % est
> épinglé pour `porte-flux`** — le même gate passe en f32 et avec `DRAVE_PERTE_MAX=1`, avec des
> références et des plafonds distincts. A8.3a reste **partielle** : pont et coupe à faire.
>
> **Dispositif** : `tools/porte-flux.sh`, Qwen2.5-0.5B Q8_0 ; deux régimes, cinq modes ;
> références f32 **61,9920 / 60,8135** et 1 % **58,3200 / 62,7357** ; données
> [`a83a-flux.json`](a83a-flux.json).

## Ce qui est mesuré

| mode | f32 réf / écart | 1 % réf / écart | 1 % plafond | état |
|---|---:|---:|---:|---|
| 0 — f32 dense | 61,9920 / 0 | **58,3200 / 0** | 0 | ✅ |
| 1 — listes quantifiées | 61,9920 / 0 | **58,3200 / 0** | 0 | ✅ |
| 2 — listes par blocs | 61,9920 / 3,65e-2 | **58,3200 / 1,14e-1** | 1,2e-1 | ✅ |
| 3 — lot dense f32 | 60,8135 / 0 | **62,7357 / 0** | 0 | ✅ |
| 4 — lot en listes | 60,8135 / 4,45e-3 | **62,7357 / 3,49e-2** | 4e-2 | ✅ |

- Les **références f32 sont inchangées** ; le gate f32 passe comme avant.
- Avec `DRAVE_PERTE_MAX=1`, les modes 2 et 4 ont un **écart de codec plus grand** (1,14e-1 au lieu
  de 3,65e-2 ; 3,49e-2 au lieu de 4,45e-3) : la règle change le cache KV, donc l’état échangé.
  Le plafond du régime 1 % est nommé, pas hérité du f32.
- Les deux gates **exit 0**.

## Le contrôle négatif

- **f32** : 61,9920 / 60,8135, plafonds f32 → ✅.
- **1 %** : 58,3200 / 62,7357, plafonds 1 % → ✅.
- **Sans le mode dual**, le gate 1 % échouait sur la référence (111,8003 dans A8.3) ; c’est le
  contrôle qui prouve que le régime a bien changé.
- **Budgets 0,001/10** : non épinglés ; le mode dual ne s’applique qu’à `DRAVE_PERTE_MAX=1`, pour
  ne pas mélanger les régimes.

## Ce qui pourrait le rendre faux

- **Un seul modèle et une seule machine** ; le signe peut changer.
- **Le mode dual est un contrat** : il ne dit pas que la règle est bonne, seulement que ses
  chiffres sont **connus**.
- **L’écart du codec augmente** sous la règle : 3,1× sur le mode 2, 7,8× sur le mode 4 ; c’est un
  coût à lire, pas un détail.
- **Les budgets 0,001/10** ne sont pas pinnés.

## Ce que ça change

A8.3a est fait **pour `porte-flux`**. Il reste `porte-pont` (dense 111,8003 sous la règle) et
`porte-coupe` (point de coupe et coûts). A8.3 **reste opt-in** : un régime pinné sur un gate ne
suffit pas pour un défaut ; il faut les trois.

## Fichiers

- `tools/porte-flux.sh` — mode dual f32 / 1 %.
- `reports/a83a-flux.json` — les deux régimes.
- `reports/rapport-a83a-flux.md` — cette fiche.
