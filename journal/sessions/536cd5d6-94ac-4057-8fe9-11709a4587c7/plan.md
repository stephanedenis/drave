# Plan de session — le hub, la reprise après reboot

> **Mandat vivant.** Ouvert le 2026-11-02 15 h 50 HNE depuis
> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md). Ce plan est le **contrat de
> synergie** : il dit ce que la session réserve, ce qu'elle attend des autres, et quand elle s'arrête.
> Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.

- **Session** : `536cd5d6-94ac-4057-8fe9-11709a4587c7`
- **Rôle** : **Hub** — intégration, état, roadmap, chantiers, journal, compteurs ; reprise après le
  reboot du 02/11 15 h 06 ; remise à zéro de la sédimentation ; runbook multi-terminaux.
- **Périmètre** : pilotage (en-cours, roadmap, chantiers, plan-travail, références), backlog, journal
  (hors `sessions/<id>/`), `reports/README.md`, `reports/INDEX.md`, outillage de pilotage.
- **Fichiers réservés** : `docs/pilotage/`, `journal/` (hors `sessions/<id>/`),
  `reports/README.md`, `reports/INDEX.md`, `AGENTS.md`, `tools/sessions.py`,
  `tools/porte-sessions.sh`, `tools/index_reports.py`, `tools/surveille_sessions.py`,
  `journal/sessions/536cd5d6-…/`.
- **Heartbeat** : 2026-11-02 16:37 EST
- **Prochaine action** : la **passe de portes** complète, **reportée** — mesuré à 16 h 32 :
  GPU 0 à **92 %** (N2, 1 650 MiB) et GPU 1 à **84 %** (`entrainer_rope.py`, 1 300 MiB), charge
  **24** ; le doc `portes.md` interdit la passe sous mesure GPU. La sous-passe documentaire (8
  portes) rend **7/8** : `porte-bloc-maths` rouge sur le seul critère de **coût** (×8,31 pour ×4),
  **vert seul** trois fois (×4,24 / ×2,84 / ×4,12) — bruit de charge, pas régression. Relancer la
  passe complète quand les deux runs N2 seront finis (200 k pas ≈ 3,3 h à 16,7 pas/s).
- **État** : actif
- **Plan** : 1) ~~audit des 111 sessions et du pilotage~~ ; 2) ~~plan de session~~ ; 3) **commits par
  flux** ; 4) **état cohérent** (140/140, gold 432, N2.ac, reboot) ; 5) **mandats** (N2, S, clôture
  GPU) ; 6) **porte sessions stricte** et registre des rouges ; 7) **INDEX.md** régénéré ; 8) ~~runbook~~ ; 9) **passe de portes**.
- **Ambition** : que l'état redevienne reprenable en deux minutes — zéro fichier non attribué, des
  mandats qui disent la vérité, et une porte qui échoue quand un mandat est mort.
- **Stratégie** : committer **par flux** avec `git add` explicite et l'index alterné ; ne jamais
  réécrire le travail d'une session ; nommer ce qui reste au lieu de le masquer ; vérifier les
  portes légères avant chaque commit.
- **Objectif final** : une sédimentation à zéro, un `en-cours` cohérent, quatre mandats explicites
  (N2, S, L/B13, D/R/A), et un runbook pour ouvrir ou reprendre chaque session dans son terminal.
