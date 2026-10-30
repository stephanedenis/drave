# N3.2b0 — la profondeur de service est branchée, et le service lisait mal les requêtes

> **Ligne de roadmap** : N3 · **Date** : 2026-10-29 · **Verdict** : ✅ **N3.2b0 tenu** — le
> service natif accepte `DRAVE_NATIVE_PROFONDEUR=N`, la profondeur 1 et la profondeur pleine
> donnent des sorties **différentes**, chacune est **déterministe**, et `/sante` ne bouge pas.
> La porte a aussi trouvé un **défaut de lecture HTTP** : le service lisait la requête en un
> seul `read` et perdait parfois le corps. Corrigé.
>
> **Dispositif** : `tools/porte-n3-profondeur.sh`, petit `drave-n0` synthétique (graine 7,
> 2 blocs, 132 528 paramètres), service `--drvm-serve` ; données
> [`n3.2b0-profondeur.json`](n3.2b0-profondeur.json).

## Le défaut trouvé

Avant correctif, **la même requête** `/generer` donnait parfois **12 octets** (corps vide) et
parfois **15 octets** (prompt « abc » + 12 générés) : le service faisait un seul `read` et le
corps pouvait arriver dans un second segment TCP. Ce n’était pas un aléa du modèle, c’était une
**lecture incomplète**.

Correctif : lire jusqu’à `Content-Length` (et jusqu’à la fin des en-têtes), 64 Ko maximum.

## Ce qui est mesuré après correctif

| mesure | résultat |
|---|---|
| `/sante` | **132 528** paramètres |
| pleine profondeur × 2 | **15 octets**, identiques |
| profondeur 1 × 2 | **15 octets**, identiques |
| profondeur 1 contre pleine | **différentes** (dernier octet) |
| `/sante` à profondeur 1 | **132 528**, identique |

`DRAVE_NATIVE_PROFONDEUR=1` coupe après le premier bloc ; le défaut reste la profondeur pleine.

## Le contrôle négatif

- **Même profondeur deux fois** : identique — pas de tirage.
- **Profondeur différente** : sortie différente — le chemin est branché.
- **`/sante` stable** : la profondeur ne change pas le modèle chargé.
- **Avant correctif** : la même requête changeait de longueur — le contrôle qui a déclenché le
  correctif.

## Ce qui pourrait le rendre faux

- **Profondeur fixe, pas de seuil de confiance** : N3.2b (le seuil) reste ouvert.
- **Modèle synthétique 2 blocs** : la différence de sortie est mince (dernier octet).
- **Un prompt** ; la qualité n’est pas mesurée.
- **Pas de test de charge** : la lecture HTTP est corrigée, pas durcie.

## Ce que ça change

N3.2b0 est **fait** : le service a une profondeur réglable et lit ses requêtes en entier.
N3.2b (seuil de confiance), N3.3b (sparsité/top-k) et la porte de composition restent.

## Fichiers

- `drave-core/src/native.rs` — lecture HTTP complète + profondeur.
- `tools/porte-n3-profondeur.sh` — la porte.
- `reports/n3.2b0-profondeur.json` — les mesures.
- `reports/rapport-n3.2b0-profondeur.md` — cette fiche.
