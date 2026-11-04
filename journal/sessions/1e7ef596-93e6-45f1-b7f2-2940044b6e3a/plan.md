# Plan de session — le hub de reprise du 04/11

> **Mandat vivant.** Ouvert le 2026-11-04 08 h 50 HNE après le reboot du 03/11 19 h 33.
> Ce plan est le contrat de la reprise : il dit ce que la session analyse, ce qu'elle commite,
> et ce qu'elle laisse aux sessions interrompues.

- **Session** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a`
- **Rôle** : **Hub de reprise** — analyse des quatre sessions interrompues (N2, S, Pensée/L, hub),
  tâches courtes, état, journal, intégration, compteurs.
- **Périmètre** : `docs/pilotage/` (en-cours, roadmap, chantiers, plan-travail, références),
  `journal/` (hors `sessions/<id>/`), `reports/README.md`, `reports/INDEX.md`, `tools/sessions.py`,
  `tools/ressources.py`, `tools/index_reports.py`, `tools/surveille_sessions.py`, l'index git.
- **Fichiers réservés** : `docs/pilotage/`, `journal/` (hors `sessions/<id>/`),
  `reports/README.md`, `reports/INDEX.md`, l'index git.
- **Heartbeat** : 2026-11-04 11:50 EST
- **Prochaine action** : **suivi docs** (N3 intégré, état au 04/11), puis la **passe** après les runs.
- **État** : actif
- **Plan** : 1) ~~analyse des quatre sessions~~ ; 2) ~~tâches courtes~~ ; 3) **état au 04/11** ;
  4) **revue + commit** ; 5) **passe de portes** ; 6) **runs longs N2** (plus tard, sur décision).
- **Ambition** : que la reprise ne perde rien — chaque session interrompue a une prochaine action
  courte et nommée, et le WIP est soit committé, soit explicitement écarté.
- **Stratégie** : `git add` explicite, index resynchronisé (`git read-tree HEAD`), pas de run long
  pendant les tâches courtes ; une fiche dit le chiffre, un commit le porte.
- **Objectif final** : un état reprenable au 04/11, quatre sessions avec une prochaine action, et
  les deux runs N2 prêts à repartir.
