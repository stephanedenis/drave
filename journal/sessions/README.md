# Sessions — plans vivants et archives

Deux choses différentes vivent ici :

- **`<id>/plan.md`** — le **mandat vivant** d'une session active : périmètre, fichiers réservés,
  heartbeat, prochaine action, état. Il s'écrit **avant** de modifier `docs/pilotage/en-cours.md`
  et se consulte avec `python3 tools/sessions.py --status`.
- **`<id>/rapport.md`** et **`<id>/digest.md`** — l'**archive** d'une session terminée, générée
  par `tools/session_report.py` / `tools/archive_sessions.py` ; les deux outils lisent
  `session.jsonl.zstd` **et** `session.v4.jsonl.zstd` (les traces récentes).
- **`<id>/cloture.md`** — la **clôture écrite à la main** quand le rapport automatique ne dit pas
  ce qui est livré et ce qui reste (`c3d0f0bd`, `f0969e87`) ; `N2-GPU` n'a pas de trace DSH et son
  rapport est écrit à la main.

Un plan n'est pas un état : `en-cours` reste la seule source de l'état. Un plan périmé (heartbeat
> 45 min) est signalé ; une session qui reprend un périmètre périmé le rafraîchit d'abord.

Modèle : [`_modele/plan.md`](_modele/plan.md). Vérification : `python3 tools/sessions.py --check`.

Migration douce : `python3 tools/sessions.py --depuis-en-cours` crée, pour chaque session listée
dans `en-cours` et sans plan, un plan **à confirmer** (rôle, fichiers, heartbeat et prochaine action
recopiés de l'état). La session le complète ensuite ; `--strict` reste rouge tant qu'il y a des
« à confirmer ».
