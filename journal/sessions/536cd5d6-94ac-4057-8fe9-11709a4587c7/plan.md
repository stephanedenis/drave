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
- **Heartbeat** : 2026-11-02 21:43 EST
- **Prochaine action** : la passe est **finie** (76/5, intégrée), le README/INDEX sont à jour ;
  la **veille** des quatre sessions et le **bilan 08 h**.
- **Ressources** : `gpu1`, `cpu1` 8 fils, `ram` 8 Gio ; registre `work/ressources.json`.
- **Nuit** : consigne `plan-travail` § 10.7 ; quatre sessions productives ; bilan 08 h.
- **État** : actif
- **Plan** : 1) ~~audit des 111 sessions et du pilotage~~ ; 2) ~~plan de session~~ ; 3) **commits par
  flux** ; 4) **état cohérent** (140/140, gold 432, N2.ac, reboot) ; 5) **mandats** (N2, S, clôture
  GPU) ; 6) **porte sessions stricte** et registre des rouges ; 7) **INDEX.md** régénéré ; 8) ~~runbook~~ ; 9) **passe de portes** ; 10) **nuit** : registre, passe, intégration, bilan 08 h.
- **Ambition** : que l'état redevienne reprenable en deux minutes — zéro fichier non attribué, des
  mandats qui disent la vérité, et une porte qui échoue quand un mandat est mort.
- **Stratégie** : committer **par flux** avec `git add` explicite et l'index alterné ; ne jamais
  réécrire le travail d'une session ; nommer ce qui reste au lieu de le masquer ; vérifier les
  portes légères avant chaque commit.
- **Objectif final** : une sédimentation à zéro, un `en-cours` cohérent, quatre mandats explicites
  (N2, S, L/B13, D/R/A), et un runbook pour ouvrir ou reprendre chaque session dans son terminal.
