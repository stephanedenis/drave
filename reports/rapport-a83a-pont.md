# A8.3a — `porte-pont` : le régime 1 % change la falaise

> **Ligne de roadmap** : A8.3a · **Date** : 2026-10-29 · **Verdict** : ✅ **le régime 1 % est
> épinglé pour `porte-pont`** — le gate passe en f32 et avec `DRAVE_PERTE_MAX=1`, avec deux
> références et deux falaises distinctes. A8.3a reste **partielle** : coupe à faire.
>
> **Dispositif** : `tools/porte-pont.sh`, Qwen2.5-0.5B Q8_0 ; deux régimes ; données
> [`a83a-pont.json`](a83a-pont.json).

## Ce qui est mesuré

| mesure | f32 | 1 % | écart |
|---|---:|---:|---:|
| PPL dense | **113,0068** | **111,8003** | −1,1 % |
| PPL blocs | **111,9225** | **115,6406** | +3,3 % |
| falaise 448 fibres | **+2,81 %** | **+5,88 %** | ×2,1 |
| falaise 392 fibres | **+25,35 %** | **+25,75 %** | +0,4 pt |

Les deux gates **exit 0**. Le mode dual choisit les références selon `DRAVE_PERTE_MAX=1` ; sans
lui, le gate 1 % échouait sur la PPL dense (111,8003 au lieu de 113,0068) et sur 448 fibres
(5,88 % > 5 %).

## Le contrôle négatif

- **f32** : 113,0068 / 111,9225, falaise 2,81 / 25,35 → ✅.
- **1 %** : 111,8003 / 115,6406, falaise 5,88 / 25,75 → ✅.
- **Sans mode dual** : le même gate échoue ; c’est la preuve que le régime a changé.
- **Le seuil 448** passe de 5 % à 7 % sous la règle : il est nommé, pas hérité.

## Ce qui pourrait le rendre faux

- **Un seul modèle et une seule machine**.
- **Le mode dual est un contrat** : il dit que les chiffres sont connus, pas que la règle est
  bonne.
- **La falaise 448 double** : c’est un coût de la règle, pas un détail.
- **Les budgets 0,001/10** ne sont pas épinglés.

## Ce que ça change

A8.3a est fait pour **flux et pont**. Il reste `porte-coupe` (point de coupe et coûts). A8.3
**reste opt-in** : deux gates sur trois ne suffisent pas.

## Fichiers

- `tools/porte-pont.sh` — mode dual f32 / 1 %.
- `reports/a83a-pont.json` — les deux régimes.
- `reports/rapport-a83a-pont.md` — cette fiche.
