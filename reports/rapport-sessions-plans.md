# Sessions — le plan avant l'état

> **Objet.** Version légère de la coordination multi-sessions : chaque session active expose son
> mandat dans `journal/sessions/<id>/plan.md` **avant** d'écrire dans `en-cours`. Les autres
> consultent `python3 tools/sessions.py --status` avant de claim un périmètre.
>
> **Verdict** : ✅ **linter + plan + autotest** ; les sessions existantes sans plan sont
> **signalées**, pas bloquées, pour permettre la migration.

## Ce qui est mesuré

| élément | résultat |
|---|---|
| plan de la session de coordination | lisible, `71d57f53` |
| `--autotest` | plan valide accepté, périmètre dupliqué refusé, champ manquant refusé |
| `--check` | sort 0 ; 2 avertissements « session en-cours sans plan » (8156 a quitté la liste) |
| `--strict` | échouerait sur ces 3 sessions (migration non finie) |

## Le contrôle négatif

- **Périmètre dupliqué** : deux plans actifs sur `A8.0` → erreur.
- **Champ manquant** : plan sans périmètre/fichiers/heartbeat → erreur.
- **Session en-cours sans plan** : avertissement (erreur en `--strict`).
- **Plan actif non listé** : avertissement, pas une invention d'état.
- **La porte** `tools/porte-sessions.sh` exécute l'autotest et le check.

## Ce qui pourrait le rendre faux

- **Heartbeat manuel** : le linter ne peut pas prouver qu'une session est vivante.
- **Pas de claim automatique** : la règle est une convention ; le linter la rend visible.
- **Les trois sessions existantes** n'ont pas encore de plan ; `--strict` est rouge jusqu'à migration.
- **Le plan n'est pas l'état** : `en-cours` reste la seule source ; un plan périmé ne doit pas
  être lu comme un état.

## Ce que ça change

`journal/sessions/` devient le **brouillon libre** des mandats ; `en-cours` garde la synthèse.
La prochaine étape est que chaque session active crée son plan et rafraîchisse son heartbeat.

## Fichiers

- `tools/sessions.py` — linter `--status`, `--check`, `--strict`, `--autotest`.
- `tools/porte-sessions.sh` — la porte.
- `journal/sessions/README.md` — la convention.
- `journal/sessions/_modele/plan.md` — le modèle.
- `journal/sessions/71d57f53-8b41-4220-84dd-7bb9eedc88d9/plan.md` — l'exemple.
