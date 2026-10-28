# N2.5b — capacité à budget égal : 21,63 M bat 11,47 M de 4,1 %

> **Objet.** Lever le biais de N2.5 : le student 21,63 M partait de zéro et le 11,47 M d'un checkpoint.
> Ici, les deux partent d'une **initialisation aléatoire**, avec le **même budget** (5 000 pas, lot 8),
> le même professeur, le même corpus et le même échantillonnage VDC.

## Dispositif

| | 11,47 M | 21,63 M |
|---|---:|---:|
| paramètres | **11 469 192** | **21 634 536** |
| initialisation | aléatoire | aléatoire |
| pas | 5 000 | 5 000 |
| lot / séquence | 8 / 128 | 8 / 128 |
| professeur | `/tmp/route-teacher` (PPL **2,355**) | idem |
| échantillonnage | VDC | VDC |

## Résultats

| mesure | 11,47 M | 21,63 M |
|---|---:|---:|
| **PPL validation** | **4,476** | **4,294** |
| écart | — | **−4,1 %** |
| précision principale | **59,11 %** | **58,81 %** |
| tête précoce 3 | **57,13 %** | **57,81 %** |
| durée | 311 s | 327 s |

**Contrôle** : le même 11,47 M **parti d'un checkpoint** (`/tmp/drave-n0-pont.pt`) atteint **3,295**.
Le passage de 4,476 à 3,295 mesure donc le **budget antérieur**, pas la capacité.

## Lecture

- À **budget égal** et **initialisation égale**, le modèle plus gros est **meilleur de 4,1 %** :
  **4,294** contre **4,476**. La capacité **sert**, faiblement.
- Mais **l'historique d'entraînement pèse plus** : le même 11,47 M passe de **4,476** à **3,295** avec un
  checkpoint de départ. Le résultat N2.5 était donc bien **confondu**.
- Les précisions sont **proches** (59,1 % vs 58,8 %) : le gain de PPL ne se voit pas encore en top-1.

## Verdict

**N2.5b — capacité : positif faible** (+4,1 % de PPL à budget égal), **mais le prior d'entraînement
domine** (+26 % pour le 11,47 M entraîné). La porte N2 (**PPL < 2,5**) reste hors de portée à 5 000 pas.

## Limites

- **5 000 pas** ; les deux modèles sont loin de la convergence.
- **Un seul lot** de validation.
- **Pas de moyenne sur plusieurs graines** : l'initialisation aléatoire est une source de variance.
- **Professeur fr**, corpus fr.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-capacite-egal.json`](native-capacite-egal.json).
