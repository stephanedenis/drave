# Plan de session — N3, les opérations natives : la clôture par l'inventaire

> **Mandat ouvert** le 2026-11-04 11 h 30 HNE, sur la frontière du graphe
> (`A2.6, N2, N3, N4` — les trois autres sont pris : N2 aux runs GPU, A2.6 et N4
> attendent les mêmes GPU jusqu'à ~15 h). La session prend la seule ligne **CPU**
> de la frontière et la mène jusqu'à son verdict.

- **Session** : `aeafe951-9c3d-4bb5-8af7-0246a4f3d51d`
- **Rôle** : **N3 — les opérations natives** : vérifier que chaque brique mesurée a bien
  une porte dans le moteur, que l'inventaire de N3.1 ne ment plus, et clore la ligne sur
  ses deux négatifs nommés (placement = métadonnée, saut de calcul conditionnel).
- **Périmètre** : N3 (N3.1–N3.6), `tools/porte-n3-*.sh`, `reports/rapport-n3.*`,
  `reports/n3.*`.
- **Fichiers réservés** : `tools/porte-n3-*.sh`, `tools/n3_inventaire.py`,
  `reports/rapport-n3-*`, `reports/n3-*`, `work/n3*`,
  `journal/sessions/aeafe951-9c3d-4bb5-8af7-0246a4f3d51d/`.
- **Heartbeat** : 2026-11-04 11:38 EST
- **Prochaine action** : **close** — N3 est intégré (fiche, JSON, porte, ligne d'état) ; il reste au hub
  à marquer la ligne N3 dans la roadmap et le statut du backlog (proposition exacte dans la fiche).
- **Fait** : passe **17/17** à **11 h 32** (92 s, 0 rouge) ; inventaire exécutable
  (`--autotest` 5/5) ; **18 portes, 20 fiches, 20 JSON, 0 orpheline** ; fiche
  [`rapport-n3-inventaire`](../../../reports/rapport-n3-inventaire.md).
- **État** : terminé
- **Plan** : 1) plan + claim cpu1 ; 2) passe `PORTES=n3` (17 portes + l'inventaire) ; 3) inventaire
  exécutable (`tools/n3_inventaire.py` + autotest) ; 4) fiche + JSON de clôture ;
  5) ligne d'état proposée au hub ; 6) commit explicite.
- **Ambition** : qu'une brique mesurée ne puisse plus perdre sa porte sans qu'une
  porte le dise — l'inventaire statique a menti en quatre endroits en six jours.
- **Stratégie** : le registre de la passe fait foi (code de sortie, jamais le marqueur) ;
  chaque affirmation de la fiche N3 est confrontée à une porte ou à un rapport ; le
  contrôle négatif de l'inventaire est un autotest qui **doit** échouer sur une brique
  sans porte.
- **Objectif final** : N3 clos sur ses deux négatifs nommés, avec un inventaire qui
  tourne, et la fiche/roadmap à mettre à jour par le hub.
