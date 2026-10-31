# Session 71d57f53 — Évaluation des techniques de lecture rapide pour Drave

> **Journaux :** [le jour](../../2026-10-29/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `71d57f53-8b41-4220-84dd-7bb9eedc88d9` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-29 07:42 |
| Durée | 29.9 h |
| Tours | 55 |
| Messages | 1174 |
| Appels d'outils | 1128 |
| Fichiers touchés | 18 |
| Commandes | 965 |
| Sous-agents | 2 |
| Commits | 98 |
| Compactages de contexte | 3 |

## Objectifs déclarés

- **create** — Drave — autonomie multi-programmes pendant plus de 3 h : (1) A8.0/A8.3 — épingler les portes PPL (porte-flux, porte-pont) puis décider le passage par défaut ; (2) A3.2/A3.3/A2.6 — réconcilier les états avec l'archive et fermer ce qui est mesuré ; (3) B11.10 — intégrer la fiche et le diff d'état ; (4
… [235 caractères tronqués]
- **complete** — Drave — autonomie multi-programmes pendant plus de 3 h : (1) A8.0/A8.3 — épingler les portes PPL (porte-flux, porte-pont) puis décider le passage par défaut ; (2) A3.2/A3.3/A2.6 — réconcilier les états avec l'archive et fermer ce qui est mesuré ; (3) B11.10 — intégrer la fiche et le diff d'état ; (4
… [235 caractères tronqués]
- **create** — Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sor
… [246 caractères tronqués]
- **complete** — Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sor
… [246 caractères tronqués]
- **create** — Goal 1/3 du cycle 9 h — A8.0/A8.3b (2 h 30) : réconcilier l'état (A8.0 à 14 portes, pas 8), épingler 2–3 portes PPL supplémentaires mesurables (porte-bus, porte-delais, porte-bus-socket), isoler le chemin lot/cache d'A8.3b (lot 1 vs ≥2, ctx/cache variables) et refuser ou documenter le défaut. Chaque
… [109 caractères tronqués]
- **edit** — Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initiale) : (1) A8.0 — épingler toutes les portes PPL mesurables restantes (bus, delais, bus-socket, profondeur-routee, etc.) et qualifier les rouges ; (2) A8.3b/c — isoler lot/cache/ctx, expliquer le signe, dé
… [326 caractères tronqués]
- **complete** — Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initiale) : (1) A8.0 — épingler toutes les portes PPL mesurables restantes (bus, delais, bus-socket, profondeur-routee, etc.) et qualifier les rouges ; (2) A8.3b/c — isoler lot/cache/ctx, expliquer le signe, dé
… [326 caractères tronqués]
- **create** — Nouveau cycle mesuré : (1) R13.3 — BPE natif sur l'anglais 100 Mo à octets égaux (bytes 10k, BPE 512/1024), validation séparée, bits/octet exact ; (2) N3.5f — sessions/positions/refus de désynchronisation TCP ; (3) A8.0 — audit des 15 portes non épinglées (mesurables vs structurelles) ; chaque résul
… [112 caractères tronqués]
- **complete** — Nouveau cycle mesuré : (1) R13.3 — BPE natif sur l'anglais 100 Mo à octets égaux (bytes 10k, BPE 512/1024), validation séparée, bits/octet exact ; (2) N3.5f — sessions/positions/refus de désynchronisation TCP ; (3) A8.0 — audit des 15 portes non épinglées (mesurables vs structurelles) ; chaque résul
… [112 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — Évalue ce qu'il manque à Drave pour pouvoir utiliser toutes les techniques de lecture rapide que les humains utilisent pour les différents types de documents

**Tour 2** — enregistre cete analyse au bon endroit et produit un nouveau roadmap vers cette cible. Ensuite consolide tous nos roadmap en un seul pour qu'on ne s'y perde pas. crée un dossier backlog dans pilotage pour y consigner toutes les fiches des fonctionnalités à documenter et implémenter.

**Tour 3** — le document en-cours.md doit être amélioré. Faire référence aux fichiers dans méthode au lieu d'expliquer. "Session en cours" doit être au pluriel et contenir une sous section par session active (chaque session doit savoir ce que font les autres sessions). les sessions sont archivées dans le dossier journal, on doit dont garder le "en-cours" léger et transférer au journal les éléments terminés. To … [76 caractères tronqués]

**Tour 4** — le backlog contient des termes non liés au glossaire et des termes à ajouter au glossaire

**Tour 5** — l'autre session vient de mettre à jour le en-cours.md. travaille en parallèle sur des chantiers qui ne risquent pas d'être en conflit

**Tour 6** — "La seule rouge est le budget de reports/README.md" il faut corriger la situation

**Tour 7** — continue

**Tour 8** — continue

**Tour 9** — go

**Tour 10** — dans le en-cours.md ajoute un diagramme des dépendances des chantiers et activités avec les états correspondants

**Tour 11** — quel est ton ide de session dsh?

**Tour 12** — f0969e87 est encore une session active dans une autre fenêtre. Est-ce que les directives à la racine du projet permettent bien à toutes les instances dsh de s'y retrouver facilement?à

**Tour 13** — fais-le

**Tour 14** — ensuite?

**Tour 15** — continue

**Tour 16** — continue avec plusieurs goals et un quota de round très élevé. Tu dois avancer en autonomie pendant plus de 3h.

**Tour 17** — continue avec plusieurs goals et un quota de round très élevé. Tu dois avancer en autonomie pendant plus de 3h.

**Tour 18** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [716 caractères tronqués]

**Tour 19** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [716 caractères tronqués]

**Tour 20** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [716 caractères tronqués]

**Tour 21** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [716 caractères tronqués]

**Tour 22** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [716 caractères tronqués]

**Tour 23** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [716 caractères tronqués]

**Tour 24** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [716 caractères tronqués]

**Tour 25** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [716 caractères tronqués]

**Tour 26** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [716 caractères tronqués]

**Tour 27** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [717 caractères tronqués]

**Tour 28** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [717 caractères tronqués]

**Tour 29** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [717 caractères tronqués]

**Tour 30** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [717 caractères tronqués]

**Tour 31** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [717 caractères tronqués]

**Tour 32** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [717 caractères tronqués]

**Tour 33** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [717 caractères tronqués]

**Tour 34** — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les portes PPL restantes (porte-gain, porte-prefill-reparti, etc.) puis tenter ou refuser le défaut avec les régimes f32/1 % ; (2) N3 — ouvrir la fiche des opérations natives et composer une porte k-WTA/routes/sortie précoce/pont/rejeu/placement ; (3) R13.1 — mesurer la PPL BPE-native si … [717 caractères tronqués]

**Tour 35** — tu as 9h d'autonomie devant toi, que vas-tu faire

**Tour 36** — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initiale) : (1) A8.0 — épingler toutes les portes PPL mesurables restantes (bus, delais, bus-socket, profondeur-routee, etc.) et qualifier les rouges ; (2) A8.3b/c — isoler lot/cache/ctx, expliquer le signe, décider le défaut ; (3) N3 — prototype natif distribué à deux processus + por … [796 caractères tronqués]

**Tour 37** — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initiale) : (1) A8.0 — épingler toutes les portes PPL mesurables restantes (bus, delais, bus-socket, profondeur-routee, etc.) et qualifier les rouges ; (2) A8.3b/c — isoler lot/cache/ctx, expliquer le signe, décider le défaut ; (3) N3 — prototype natif distribué à deux processus + por … [796 caractères tronqués]

**Tour 38** — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initiale) : (1) A8.0 — épingler toutes les portes PPL mesurables restantes (bus, delais, bus-socket, profondeur-routee, etc.) et qualifier les rouges ; (2) A8.3b/c — isoler lot/cache/ctx, expliquer le signe, décider le défaut ; (3) N3 — prototype natif distribué à deux processus + por … [796 caractères tronqués]

**Tour 39** — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initiale) : (1) A8.0 — épingler toutes les portes PPL mesurables restantes (bus, delais, bus-socket, profondeur-routee, etc.) et qualifier les rouges ; (2) A8.3b/c — isoler lot/cache/ctx, expliquer le signe, décider le défaut ; (3) N3 — prototype natif distribué à deux processus + por … [796 caractères tronqués]

**Tour 40** — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initiale) : (1) A8.0 — épingler toutes les portes PPL mesurables restantes (bus, delais, bus-socket, profondeur-routee, etc.) et qualifier les rouges ; (2) A8.3b/c — isoler lot/cache/ctx, expliquer le signe, décider le défaut ; (3) N3 — prototype natif distribué à deux processus + por … [796 caractères tronqués]

**Tour 41** — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initiale) : (1) A8.0 — épingler toutes les portes PPL mesurables restantes (bus, delais, bus-socket, profondeur-routee, etc.) et qualifier les rouges ; (2) A8.3b/c — isoler lot/cache/ctx, expliquer le signe, décider le défaut ; (3) N3 — prototype natif distribué à deux processus + por … [796 caractères tronqués]

**Tour 42** — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initiale) : (1) A8.0 — épingler toutes les portes PPL mesurables restantes (bus, delais, bus-socket, profondeur-routee, etc.) et qualifier les rouges ; (2) A8.3b/c — isoler lot/cache/ctx, expliquer le signe, décider le défaut ; (3) N3 — prototype natif distribué à deux processus + por … [796 caractères tronqués]

**Tour 43** — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initiale) : (1) A8.0 — épingler toutes les portes PPL mesurables restantes (bus, delais, bus-socket, profondeur-routee, etc.) et qualifier les rouges ; (2) A8.3b/c — isoler lot/cache/ctx, expliquer le signe, décider le défaut ; (3) N3 — prototype natif distribué à deux processus + por … [796 caractères tronqués]

**Tour 44** — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initiale) : (1) A8.0 — épingler toutes les portes PPL mesurables restantes (bus, delais, bus-socket, profondeur-routee, etc.) et qualifier les rouges ; (2) A8.3b/c — isoler lot/cache/ctx, expliquer le signe, décider le défaut ; (3) N3 — prototype natif distribué à deux processus + por … [796 caractères tronqués]

**Tour 45** — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initiale) : (1) A8.0 — épingler toutes les portes PPL mesurables restantes (bus, delais, bus-socket, profondeur-routee, etc.) et qualifier les rouges ; (2) A8.3b/c — isoler lot/cache/ctx, expliquer le signe, décider le défaut ; (3) N3 — prototype natif distribué à deux processus + por … [797 caractères tronqués]

**Tour 46** — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initiale) : (1) A8.0 — épingler toutes les portes PPL mesurables restantes (bus, delais, bus-socket, profondeur-routee, etc.) et qualifier les rouges ; (2) A8.3b/c — isoler lot/cache/ctx, expliquer le signe, décider le défaut ; (3) N3 — prototype natif distribué à deux processus + por … [797 caractères tronqués]

**Tour 47** — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initiale) : (1) A8.0 — épingler toutes les portes PPL mesurables restantes (bus, delais, bus-socket, profondeur-routee, etc.) et qualifier les rouges ; (2) A8.3b/c — isoler lot/cache/ctx, expliquer le signe, décider le défaut ; (3) N3 — prototype natif distribué à deux processus + por … [797 caractères tronqués]

**Tour 48** — This is an automatically generated checkpoint condensing an earlier span of the conversation to free up context. Treat the captured context as established background and build on it without restating it. Continue the task directly from the messages that follow, without acknowledging this checkpoint.  <compacted-summary> ## Primary Request and Intent - User: **“continue sans moi jusqu'a 8h demain m … [6601 caractères tronqués]

**Tour 49** — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initiale) : (1) A8.0 — épingler toutes les portes PPL mesurables restantes (bus, delais, bus-socket, profondeur-routee, etc.) et qualifier les rouges ; (2) A8.3b/c — isoler lot/cache/ctx, expliquer le signe, décider le défaut ; (3) N3 — prototype natif distribué à deux processus + por … [797 caractères tronqués]

**Tour 50** — continue

**Tour 51** — vois-tu les changements au en-cours.md?

**Tour 52** — après demain on n'aura plus de soucis de décalage d'ehure DST. pas de soucis... l'idée resque que le en-cours.md est un outil de pilotage pour les sessions de travail et on en a plusieurs sur la même machine, donc il faut une coordination fine des sessions et du qui fait et fera quoi.

**Tour 53** — commence par une version légère, mais on a déjà un dossier pour les sessions où chaque session pourrait écrire plus librement et exposer ses plans pour que les autres consultent avant d'écrire leur état dans le en-cours.

**Tour 54** — continue (examine d'abord en-cours.md)

**Tour 55** — continue

## 2. Déroulé, étape par étape

### Tour 1 — Évalue ce qu'il manque à Drave pour pouvoir utiliser toutes les techniques de lecture rapide que les humains utilisent p … [37 caractères tronqués]

*28 appels d'outils.* Actions notables :

- bash — List repo root and recent git history
- bash — Inventory docs, reports, tools
- read
- bash — Find docs mentioning rapid reading concepts
- bash — List theory docs and sizes
- bash — Grep roadmap for reading/document/context lines
- bash — Grep theory docs for reading/context terms
- bash — Inspect reader benchmark and report
- bash — Inspect data corpus and needle test
- bash — Read native roadmap context lines
- bash — Check document format and tokenizer support
- bash — Read archived notes on parallel readers and periphery
- bash — Read N4/N5 roadmap and preload references
- web_search
- … et 11 autres

**Synthèse produite :**

⏵ Rédaction de l'évaluation : cadre scientifique, chiffres du dépôt, matrice des manques

**Verdict — il manque à Drave un lecteur, pas une technique de lecture.**

Donnez à Drave un rapport de 40 pages et une question. Avec son modèle natif, il ne peut pas y répondre : **129 octets de contexte**, pas de parseur de document, pas de mémoire au-delà de quelques pas, pas de sortie structurée. Avec un modèle externe (Qwen 0,5 B), le moteur peut lire 12 288 jetons — mais alors ce n'est pas Drave qui lit, c'est le modèle apporté. Sur les **14 techniques humaines** recensées plus bas, **aucune n'est opérationnelle au niveau document**, **5 ont un substrat mesuré**, **9 sont absentes**. Le substrat est bon ; c'est l'assemblage qui manque.

\### L'échelle du lecteur

| niveau | ce que c'est | état de Drave |
|---|---|---|
| **L0 — flux** | octets, perplexité, génération | ✅ acquis |
| **L1 — saut de calcul** | sortie précoce, parcimonie, chemin court | ✅ mesuré |
| **L2 — document** | régions typées, structure, layout, provenance | ❌ absent |
| **L3 — politique** | survol, écrémage, balayage, sélectif, relecture | ❌ absent |
| **L4 — mémoire** | gist, entités, faits, épisodique | ❌ négatif (N5) |
| **L5 — restitution** | réponse, résumé, extraction, citation | ❌ absent |
| **L6 — banc** | courbe vitesse-compréhension par type | ❌ absent |

**Drave est à L1. La lecture rapide humaine est un pilotage L2–L4, prouvé par un banc L5–L6.** C'est pourquoi ajouter une « tête d'écrémage » au modèle actuel ne composerait pas : il n'y a rien à écrémage, ni document à survoler, ni sortie pour prouver la compréhension.

---

\## 1. Ce que la lecture rapide humaine est vraiment

La science est claire depuis la revue de Rayner et al. (2016) : **on ne lit pas à 1 000 mots/minute en comprenant tout**. Les saccades ne sont pas un défaut à supprimer — elles servent à revenir sur ce qui n'a pas été compris ; la vision périphérique est floue ; les programmes de lecture rapide entraînent surtout… à **écrémer** ([APS, *So Much to Read, So Little Time*](https://www.psychologicalscience.org/publications/speed_reading.html)). Le vrai levier humain est donc une **allocation** : choisir le mode (survol, balayage, lecture sélective, lecture intégrale, relecture) selon le **but** et le **type de document**, en acceptant une perte de compréhension contrôlée.

Conséquence pour l'évaluation : la bonne métrique n'est pas le débit, c'est **la compréhension par unité de calcul** — une courbe vitesse-com
… [17041 caractères tronqués]

### Tour 2 — enregistre cete analyse au bon endroit et produit un nouveau roadmap vers cette cible. Ensuite consolide tous nos roadma … [163 caractères tronqués]

*111 appels d'outils.* Actions notables :

- todo_write
- bash — Check sizes and current date
- read
- bash — Read documentation review tool
- bash — Read rest of documentation review tool
- bash — Read en-cours and size checkers
- bash — Measure roadmap words, read table gate, last commit
- bash — Find all roadmap references
- bash — Count words per roadmap section
- bash — Locate roadmap references in AGENTS and method docs
- bash — Read context and organization docs
- bash — Read archive index
- bash — Find living and journal references to native roadmap
- bash — Find living docs referencing native roadmap
- … et 79 autres

**Synthèse produite :**

⏵ Récapitulatif : analyse, roadmap unique, backlog et vérifications

**Fait — commit `3b9162d1`.** Les trois livrables sont en place, et il ne reste qu'**une seule roadmap vivante**.

\## 1. L'analyse est enregistrée

`docs/theorie/lecture-rapide.md` — le document complet : les **14 techniques** humaines, les **5 couches manquantes** (document, fenêtre, politique, mémoire, restitution), les chiffres du dépôt, le banc proposé, les faux chemins. Il est relié depuis la roadmap, l'état, la carte, le README et `AGENTS.md`.

\## 2. La roadmap unique

`docs/pilotage/roadmap.md` — **un seul plan, quatre chantiers** : **A** (moteur), **B** (intelligence), **N** (natif), **R** (lecteur). Le nouveau **programme R** y est détaillé en six phases :

| phase | livrable | dépend de |
|---|---|---|
| **R0** | lecteur v0 : graphe de document, contrôleur classique, banc — **sans entraînement** | rien |
| **R1** | fenêtre native : contexte hiérarchique, curriculum, tokenisation | N1/N2 |
| **R2** | mémoire : gist, entités, store épisodique, relecture | N5, R1 |
| **R3** | restitution : SFT de lecture, citations | N4, R0 |
| **R4** | blocs structurels : tableaux, code, maths, vision | R0 |
| **R5** | lecture croisée : multi-documents, multilingue | R3, M4 |

Les anciennes roadmaps sont archivées et liées, plus dupliquées :
- `docs/archive/roadmap-detail-2026-10-29.md` (ancien plan A/B, 473 lignes) ;
- `docs/archive/roadmap-native-2026-10-29.md` (ancien programme N, 176 lignes).

La roadmap est passée de **8 500 à ~3 500 mots** : elle dit l'état et la prochaine action, le détail mesuré reste dans les archives et `reports/`.

\## 3. Le backlog

`docs/pilotage/backlog/` — **31 fichiers** : `index.md`, `_modele.md`, et **29 fiches** :

- **19 fiches R** : R01 graphe de document, R02 contrôleur, R03 banc, R04–R06 têtes de lecture, R11–R13 fenêtre/tokenisation, R21–R22 mémoire, R31–R32 restitution, R41–R44 blocs structurels, R51–R52 croisé/multilingue.
- **10 fiches A/B/N** : N0.3b, N2, N4, B10.3, B12.10, A3.4, A5.4, A6.2, B1.5, B11.10.

Chaque fiche porte : besoin, contrat (entrée/sortie/coût/trace), mesures, **portes**, **contrôles négatifs**, ce qui pourrait la rendre fausse, étapes, documents à écrire. L'index donne statut, priorité, dépendances, ligne de roadmap et résultat attendu.

\## 4. Navigation et état mis à jour

`en-cours.md` (compteur **88 documents**, priorité R0, backlog), `AGENTS.md` (routage vers l'analyse et le backlog), `docs/README.md`, `carte.md`, `mission.md`, `c
… [951 caractères tronqués]

### Tour 3 — le document en-cours.md doit être amélioré. Faire référence aux fichiers dans méthode au lieu d'expliquer. "Session en c … [356 caractères tronqués]

*65 appels d'outils.* Actions notables :

- bash — Inspect recent sessions and today's journal index
- bash — Inspect en-cours checker and references
- bash — Inspect current session folder and report format
- bash — Read method rules on session state
- bash — Inspect sessions index conventions
- bash — Read current en-cours full content
- bash — Inspect journal_auto session line generation
- bash — Inspect previous day session section
- read
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-10-29/etat-transfere.md`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md`
- bash — Check en-cours current state
- bash — Inspect uncommitted en-cours change
- bash — Inspect concurrent session changes
- … et 44 autres

**Synthèse produite :**

⏵ Récapitulatif de l'état multi-sessions et des vérifications

**Fait — commit `9e569aec`.** `en-cours.md` passe de **1 006 à 958 mots**, et répond aux quatre demandes.

\## 1. Trois sessions actives, chacune sait ce que font les autres

`## Sessions en cours` contient une sous-section par session :

| session | rôle |
|---|---|
| `f0969e87` | **principale** : état, docs, R0 (lecteur v0) |
| `8156fdcb` | **backlog** : graphe des dépendances, `verifie_backlog.py`, fiches A/B/N/R |
| `N2-GPU` | **calcul** : distillation N2 (job GPU, sans Id DSH) |

Chaque bloc porte les **sept champs** : `Id`, `Rôle`, `Ce qu'elle fait`, `Ce que font les autres`, `Prochaine action`, `Bloquants`, `Journal`. La ligne « Ce que font les autres » dit qui fait quoi et rappelle la règle : les autres sessions rendent un **diff d'état**, la principale applique.

\## 2. La méthode est référencée, pas recopiée

- L'en-tête renvoie à [`contexte.md`](../methode/contexte.md) (budget, chargement) et à [`continuite.md`](../methode/continuite.md) (contrat des sessions).
- `continuite.md` porte désormais la règle complète : une sous-section par session active, les sept champs, un bloquant par chantier, le transfert des éléments finis au journal.
- `contexte.md` a été mis à jour : on lit « Sessions en cours » + « Les chantiers et leurs bloquants » + « Ce qui reste », pas les explications.

\## 3. L'état reste léger, le terminé va au journal

Les éléments finis ont été transférés dans [`journal/2026-10-29/etat-transfere.md`](../journal/2026-10-29/etat-transfere.md) : **N0/N1**, **C1–C7**, **B3/B4**, **B5–B8**, **C3.2**, **A1–A8**, avec leurs liens. `en-cours` ne garde que les sessions actives, les bloquants, les prochaines actions, les compteurs et les questions.

\## 4. Chaque chantier a son bloquant

La table `chantier | état | bloquant | prochaine action` couvre **A, B, N, R, C1–C7 et le backlog**. Chaque ligne a un bloquant non vide — « aucun » est une information, une cellule vide est un oubli. Exemples : A3.4 Colab, B10.3 décodeur, N2 < 2,5, R1 dépend de N1/N2, 8 lignes sans fiche.

\## 5. Le contrôleur suit

[`tools/verifie_en_cours.py`](../tools/verifie_en_cours.py) vérifie maintenant :

- la section **« Sessions en cours »** et ses sous-sections `### Session` ;
- les **sept champs** de chaque session ;
- les lignes **A/B/N/R** avec un bloquant non vide ;
- les questions avec leur `→` de déblocage ;
- la prochaine action nommée, le budget de 2 000 mots, les 10 puces et les 5 questions.

\## Vé
… [702 caractères tronqués]

### Tour 4 — le backlog contient des termes non liés au glossaire et des termes à ajouter au glossaire

*52 appels d'outils.* Actions notables :

- bash — Inspect glossary structure and index
- bash — Read sample glossary entries and family index
- bash — Read glossary card generator
- bash — Inspect family structure and entry format
- bash — Check which candidate glossary slugs exist
- bash — Search glossary index for candidate terms
- bash — Search family definitions for missing terms
- bash — Extract frequent terms from backlog
- bash — Inspect family definition style
- bash — Read glossary generator main and verifier
- bash — Check more existing glossary slugs
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/glossaire/12-la-lecture-le-document-et-ses-mesures.md`
- bash — Add family 12 to glossary generator
- bash — Dry-run glossary generation with family 12
- … et 37 autres

**Synthèse produite :**

⏵ Récapitulatif de l'extension du glossaire et des liens du backlog

**Fait — commit `a7dd8473`.** Le backlog ne laisse plus ses termes sans définition : **27 entrées** ont été ajoutées, **29 fiches** portent désormais une ligne `Glossaire`, et le glossaire passe de **289 à 316 entrées**.

\## 1. Ce qui manquait

Deux cas distincts :

- **termes déjà définis mais non liés** : perplexité, BPE, KV, MoE, expert, routeur, k-WTA, GGUF, DRVF, RSN, RSN-jeu, professeur/élève, jeton, rejeu, préremplissage, Colab, FPGA, PE, événement, corpus aligné, fidélité, oracle…
- **termes absents du glossaire** : tout le vocabulaire du programme R et des mesures de lecture.

\## 2. La nouvelle famille 12

`docs/theorie/glossaire/12-la-lecture-le-document-et-ses-mesures.md` — **1 204 mots, 27 entrées** :

| groupe | entrées |
|---|---|
| **Lecture** | lecture rapide (survol, balayage, écrémage, sélectif), contrôleur de lecture, relecture, graphe de document (région, offset, provenance, manifeste), span, closed-book, gist, banc de lecture rapide |
| **Mémoire, recherche, entraînement** | retrieval, curriculum, SFT, distillation, tenu à l'écart |
| **Mesures** | chrF, WER, F1, AUC |
| **Structure** | parseur, AST, CAS, OCR, layout, tableau, contrat |
| **Format et méthode** | DRVM, contrôle négatif, graphe de dépendances (arête dure, plafond, frontière) |

Les définitions renvoient aux fiches du backlog, au plan et aux mesures ; les termes déjà définis sont liés, pas recopiés. Les collisions de sens sont nommées : `relecture` (lecture) vs `relecture adverse`, `contrat` (fiche) vs `contrat d'activation`, `plafond` (dépendance) vs `plafond de flux`, `frontière` (graphe) vs `frontière` fidélité/contenu.

\## 3. Les liens dans le backlog

Chaque fiche commence maintenant par :

```markdown
> **Glossaire** : [graphe de document](…) · [parseur](…) · [contrat](…).
```

- **29 fiches** couvertes (19 R + 10 A/B/N) ;
- `backlog/index.md` a une section **« Le glossaire »** qui renvoie à la famille 12 et aux entrées clés ;
- `backlog/_modele.md` impose la ligne aux futures fiches ;
- `roadmap.md` renvoie à la famille 12 depuis le programme R.

\## 4. Génération et cohérence

- `tools/glossaire_cartes.py` connaît la famille 12 et calcule le nombre de familles dynamiquement ;
- **27 fiches** `entrees/*.md` générées, `README.md` et `index.json` régénérés ;
- `docs/README.md` : **316 fiches** ;
- en-têtes des familles 01–11 passés à **12 familles** ;
- `docs/theorie/glossaire.md` : section 12 ajouté
… [906 caractères tronqués]

### Tour 5 — l'autre session vient de mettre à jour le en-cours.md. travaille en parallèle sur des chantiers qui ne risquent pas d'êt … [13 caractères tronqués]

*36 appels d'outils.* Actions notables :

- bash — Inspect latest commits, working tree, and updated en-cours
- bash — Check R0.1 status in roadmap and backlog
- bash — Locate DRVM/GGUF assets and engine CLI
- bash — Read N0.3b sheet and prior attempts
- bash — Read existing N0.3b reports
- bash — Inspect engine CLI for DRVM execution flags
- bash — Inspect DRVM native execution code
- bash — Read DRVM PPL execution branches
- bash — Check DRVM files and converter usage
- bash — Check converter CLI and tiny native fixture
- bash — Locate N0.12/N0.13 native PPL source
- bash — Identify native DRVM models
- bash — Read native PPL reports for model path and commands
- bash — Prepare exact test texts and check DRVM files
- … et 19 autres

**Synthèse produite :**

⏵ Récapitulatif du chantier N0.3b et des mesures indépendantes

**Fait — commit `bc4e3d92`.** J'ai pris **N0.3b** (parité PPL DRVM ↔ GGUF), qui était libre et assigné à cette session par l'état, sans toucher à `en-cours.md`, `roadmap.md` ni au backlog — les fichiers de R0.2 restent à l'autre session.

\## Résultat — la ligne est close, avec sa limite nommée

| couple | texte | mesure | écart |
|---|---|---:|---:|
| **Qwen 0,5 B Q4_0 — conversion** | 59 octets | GGUF **68,1917** · DRVM **68,1917** (15 jetons) | **0,0000** |
| **Qwen 0,5 B Q4_0 — conversion** | 1 076 octets | GGUF **92,1875** · DRVM **92,1875** (304 jetons) | **0,0000** |
| **`drave-n0` — natif** | 59 octets | natif **4,6585** · Python **4,658519** | **< 0,0001** |
| **`drave-n0` — natif** | 1 076 octets | natif **18,6394** · Python **18,6395** | **0,0001** |

**Contrôles négatifs** :
- aller-retour `gguf2drvm` → `drvm2gguf` : **SHA-256 identique** au GGUF source (`c8cd5f37…`), DRVM déterministe (`52d2c1c0…`) ;
- deux passes Qwen 59 octets : **68,1917** les deux fois ; deux passes natives 59 octets : **4,6585** les deux fois ;
- DRVM tronqué à 1 Mo : **refusé** (`en-tête incohérent`, code 3).

**La limite, écrite dans la fiche** : la parité Qwen est une parité de **conteneur** — `--drvm-ppl` reconstruit un GGUF en mémoire, ce n'est pas une passe avant native sur les tenseurs DRVM. La passe native n'existe que pour `drave-n0`. « Qwen exécuté nativement depuis DRVM » reste **hors de portée en l'état** ; la ligne est close pour ce qu'elle peut prouver.

\## Fichiers

- `reports/rapport-drvm-ppl.md` — fiche mise à jour, section « Clôture N0.3b » ;
- `reports/drvm-ppl.json` — mesures et contrôles ajoutés ;
- `reports/README.md` et `reports/INDEX.md` — ligne N0.3b mise à jour.

\## Coordination

- Je n'ai **pas** touché `docs/pilotage/en-cours.md`, `roadmap.md` ni `backlog/` : la session `8156fdcb` est en train de livrer R0.2 et a ces fichiers staged.
- **Diff d'état à appliquer par la session principale** : `N0.3b` : `prête` → **mesurée**, fiche [`reports/rapport-drvm-ppl.md`](reports/rapport-drvm-ppl.md). Aucun fichier de résultat ajouté (fiche existante mise à jour), donc les compteurs de fichiers/JSON ne changent pas.

\## Vérifications

| outil | résultat |
|---|---|
| `revue_documentation.py` | ✅ 275 fiches · 339 JSON · 93 docs · 51 portes |
| `porte-tableaux.sh` | ✅ 1 192 fichiers · 1 182 liens |
| `verifie_en_cours.py` | ✅ (état de l'autre session) |
| `taille_documents.py` | ⚠️ **violation pr
… [237 caractères tronqués]

### Tour 6 — "La seule rouge est le budget de reports/README.md" il faut corriger la situation

*10 appels d'outils.* Actions notables :

- bash — Read reports README structure and size
- bash — Read rest of reports README
- bash — Count words per README section
- bash — Compress raw-data section and check budget
- bash — Validate compressed reports README
- bash — Commit only the compressed reports README
- bash — Inspect commit contents, tree, and budget
- bash — Final validation after budget fix
- bash — Fix wording and amend budget commit
- bash — Final validation after amend

**Synthèse produite :**

⏵ Récapitulatif de la correction du budget de `reports/README.md`

**La rouge est corrigée — commit `7a8a441e`.** `reports/README.md` passe de **3 424 à 1 724 mots**, sous son budget de **2 800**, et `taille_documents.py` ne signale plus **aucune violation**.

\## Ce qui a été coupé

La section **« Les données brutes »** faisait à elle seule **1 806 mots** : elle listait un par un les dizaines de JSON de campagne (`traduction-*`, `kfold-*`, `contamination-*`, `pont-*`, `xnli-*`, `plan-*`, `registre-*`).

Elle est remplacée par :

- une liste courte des **principaux agrégats** (jeux, DeepSeek, cerveau, B10–B12) ;
- un renvoi explicite à [`INDEX.md`](reports/INDEX.md) pour l'index **exhaustif** ;
- la mention que chaque JSON de campagne est décrit dans la fiche de sa mesure.

La table **« Les fiches courantes »** (les résultats N0/N1/N2/N4 et les fiches structurantes) est conservée : c'est la partie curated du README.

\## Effet sur les liens

Le nombre de liens passe de **1 182 à 985** : les 197 liens supprimés pointaient vers des JSON de campagne qui restent dans le dossier et dans les fiches. Les **985 liens restants résolvent tous**.

\## Vérifications

| outil | résultat |
|---|---|
| `taille_documents.py` | ✅ **tous les documents chargeables sont dans leur budget** — plus aucune violation |
| `revue_documentation.py` | ✅ 275 fiches · 339 JSON · 93 docs · 51 portes |
| `porte-tableaux.sh` | ✅ 1 192 fichiers · 985 liens |
| `verifie_en_cours.py` | ✅ 1 066 mots · 3 sessions · bloquants |

Le commit inclut aussi les **trois lignes de journal régénérées par le hook** (`journal/2026-10-29/README.md`, `distribue.md`, `THEMES.md`) ; le hook en a laissé une version plus récente non committée, sans impact sur les portes. La session `8156fdcb` a de son côté committé R0.2 (`08149617`) sans conflit avec cette correction.

### Tour 7 — continue

*52 appels d'outils.* Actions notables :

- bash — Read current state and recent commits
- bash — Read priorities and reserved files
- bash — Inspect B11.10 sheet, report and codec
- bash — Find card coverage source and gate
- bash — Read codec normalization and universal schema
- bash — Find B11 tests and card metric
- bash — Find SFT code and protocol
- bash — Review R0.2 result and remaining ceiling
- bash — Inspect B12.10 sheet and pipeline code
- bash — Inspect SFT training/eval code
- bash — Read B12.10 pipeline code and results
- bash — Inspect pipeline modules and usage
- bash — Inspect B12 corpus and battery
- bash — Locate game corpus builder
- … et 37 autres

**Synthèse produite :**

⏵ Récapitulatif : N0.3b intégré, bug de contexte B12.10 corrigé et mesuré

**Fait — commit `e11f096a`.** Deux choses ont avancé : N0.3b est maintenant **intégré à l'état**, et B12.10 a livré un **vrai résultat** — un bug de contexte qui rendait le pipeline muet.

\## 1. N0.3b intégré

- `en-cours.md` : session `f0969e87` → **N0.3b mesuré**, prochaine action **B12.10**.
- `roadmap.md` : N0 ✅, N0.3b **close** (conversion **68,1917 / 92,1875**, natif **4,6585 / 18,6394**).
- `backlog/N0.3b` : statut **mesurée**, lien vers [`rapport-drvm-ppl.md`](reports/rapport-drvm-ppl.md).
- `journal/2026-10-29/etat-transfere.md` : ligne N0.3b ajoutée, N0 ne dit plus « reste ouvert ».

\## 2. B12.10 — le contexte du pipeline était une chaîne

**Le bug.** `ItemType.contexte` contient `resume_contexte` — une **chaîne** (`"cartes etat"`). Le codec attend un **RSN** avec `.corps`. Le codec levait `AttributeError`, `Hub.percevoir` l'attrapait et rendait `None` : le pipeline ne stockait **rien**, sans le dire.

| chemin | cartes | items | exactes |
|---|---:|---:|---:|
| `Hub` avec `ItemType.contexte` (chaîne) | 161 | 528 | **0** |
| `Pipeline.percevoir_item` (RSN si présent, sinon `None`) | 161 | 528 | **161 / 528** |
| dont contexte RSN disponible | 8 | 8 | **8 / 8** |
| dont contexte perdu en amont (chaîne seule) | 153 | 520 | **153 / 520** |
| contrôle : contexte RSN **mélangé** | 8 | 8 | **4 / 8**, **4 refus** |

- Le codec lit **161/161** cartes sans contexte et **8/8** avec le RSN ; le pipeline retrouve **528/528** items.
- Le contrôle mélangé montre que le contexte **sert** : la moitié des cartes ne sont plus valides avec le contexte d'une autre donne, et le codec refuse les quatre autres.
- **Ce qui reste** : seuls **8** items de cartes portent un RSN complet ; les **153** autres n'ont qu'un résumé dans `ItemType`. La correction ne peut pas restituer un contexte jeté en amont. La **généralisation M4/M8** sur un code tenu à l'écart reste ouverte — c'est la prochaine action B12.10.

\## 3. Code et tests

- `tools/semantique/typed_corpus.py` : `ItemType.contexte_rsn` (le RSN est conservé).
- `tools/cerveau/pipeline.py` : `Pipeline.percevoir_item()` passe le RSN.
- `tools/cerveau/hub.py` : une chaîne est **refusée explicitement** (`echec`), plus d'échec muet.
- Tests : `test_pipeline.py` (contexte RSN), `test_bus.py` (chaîne refusée), `test_typed_corpus.py`.
- Fiche : section **11bis** de [`rapport-cerveau-corrections.md`](reports/rapport-cerveau-corrections.md).
- Backlog B12.
… [1041 caractères tronqués]

### Tour 8 — continue

*26 appels d'outils.* Actions notables :

- bash — Inspect M8 consolidation output
- bash — Check corpus code count and distribution
- bash — Inspect prototype keys and Pipeline lookup
- bash — Run held-out code experiment for B12.10
- bash — Summarize held-out B12.10 results
- bash — Clean and rerun held-out experiment
- bash — Read B12.10 report section for insertion
- bash — Add held-out results to B12.10 report
- bash — Update B12.10 next action and state
- bash — Validate state, docs, tables and budgets
- bash — Check tree and rerun held-out script
- job_kill
- bash — Commit held-out experiment and report
- bash — Final verification after B12.10 held-out commit
- … et 12 autres

**Synthèse produite :**

⏵ Récapitulatif du split B12.10 et du branchement M4 inerte

**Fait — commits `7fb36771` et `b1197a46`.** B12.10 a maintenant sa mesure sur codes tenus à l'écart, et le branchement M4 testé s'est révélé **inerte** : je l'ai retiré plutôt que de laisser une branche morte.

\## 1. Le split par code tenu à l'écart

**Protocole** : 29 codes uniques, **3 graines**, **6 codes tenus à l'écart** par graine (toutes leurs surfaces) ; chaque champ non nul est masqué une fois.

| mesure | stocké (M4) | tenu (M4) | tenu (M8) | tenu (pipeline) | tenu sans M4 |
|---|---:|---:|---:|---:|---:|
| **champ non nul** | **0,809** | **0,153** | **0,436** | **0,436** | **0,436** |
| **code exact** | **0,809** | **0** | **0** | — | — |

- **Variance par graine** (M8) : **0,056 / 0,859 / 0,393** ; M4 : **0,037 / 0,028 / 0,393**. Six codes par graine, c'est peu : **0,436** est une enveloppe, pas un taux stable.
- Le chemin `repondre` est **`prototype` 321/321, 71/71 et 214/214** sur les cues partiels : **M4 n'est jamais appelé**.
- **M4 retiré ne change rien** (0,436) : la porte « M4 retiré ⇒ le score chute » **n'est pas franchie**, non parce que M4 est inutile, mais parce qu'il n'est **pas branché** sur les cues partiels.
- La tautologie est confirmée : **0 code exact** sur codes neufs. Le **96,33 %** publié est mesuré sur des codes **stockés** avec un autre protocole (masque `vers`, 80 items) ; notre mesure stockée, tous champs masqués, donne **0,809**.

\## 2. Le branchement M4 tenté, et retiré

J'ai testé une règle « garder M4 si ses champs **observés** collent mieux que le prototype ». Résultat : **0 sélection M4** sur les trois graines — les champs observés sont à égalité, et le champ masqué est le seul discriminant. La règle est **retirée** (`b1197a46`) : une branche qui ne se déclenche jamais est exactement ce que le dépôt appelle un drapeau inerte.

\## 3. Fichiers

- `tools/cerveau/b1210_holdout.py` — le protocole des 3 graines × 6 codes.
- `reports/rapport-cerveau-corrections.md` §11bis — le split, la variance, le verdict, la tentative inerte.
- `docs/pilotage/backlog/B12.10-pipeline-m1-m4-m8.md` — état et prochaine action.
- `docs/pilotage/en-cours.md` — N0.3b close, split B12.10 mesuré, prochaine action.
- `tools/cerveau/pipeline.py` — hybride retiré, `percevoir_item` conservé.

\## 4. Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 276 fiches · 340 JSON · 93 docs · 51 portes |
| `taille_documents.py` | ✅ tous les documents chargeables dans l
… [681 caractères tronqués]

### Tour 9 — go

*11 appels d'outils.* Actions notables :

- bash — Inspect margin signal for M4 vs prototype
- bash — Add oracle and margin policies to held-out script
- bash — Measure oracle and margin policies
- bash — Read B12.10 section before final update
- bash — Update B12.10 report with oracle/margin verdict
- bash — Read B12.10 sheet current state
- bash — Close B12.10 in backlog as measured negative
- bash — Close B12.10 in state, roadmap and transfer log
- bash — Update session ownership and run checks
- bash — Commit oracle result and B12.10 closure
- bash — Final checks after B12.10 closure

**Synthèse produite :**

⏵ Récapitulatif : B12.10 close négative, l'oracle est M8 et M4 n'apporte aucun champ unique

**Fait — commit `fe40a9fa`.** B12.10 est maintenant **mesurée et close négative**, avec une preuve plus forte qu'un simple échec de porte : **M4 n'apporte aucun champ correct unique**.

\## 1. Le résultat qui tranche

Sur **606 observations** (3 graines × 6 codes tenus à l'écart) :

| mesure | valeur |
|---|---:|
| **M4 seul** (champs que M4 gagne et pas M8) | **0** |
| **M8 seul** (champs que M8 gagne et pas M4) | **63** |
| **oracle** (M4 ou M8) | **0,436** |
| **M8** | **0,436** |
| **code exact** (M4 et M8) | **0** |

**L'oracle est exactement M8.** M4 ne gagne **aucun** champ que le prototype ne gagne déjà ; il ne peut donc pas améliorer la complétion sur codes neufs.

\## 2. La marge ne sauve pas M4

Les marges top1−top2 ne prennent que deux valeurs : **0** ou **0,067**. Utiliser M4 dès que la marge est > 0 sélectionne 34 % / 83 % des cues et fait **tomber** le champ à **0,037 / 0,028** (au lieu de 0,436). Un seuil > 0,1 ne sélectionne **rien**.

- La règle par champs observés était déjà inerte (0 sélection M4).
- La règle par marge est **pire** que le prototype.
- La porte « M4 retiré ⇒ le score chute » est donc **vide** : M4 est un **lookup exact** pour les codes stockés, pas un complémenteur pour les codes neufs.
- Le comportement actuel — `prototype` pour les cues partiels — est **optimal** parmi M4 et M8 sur ce corpus. Ce n'est pas un bug à corriger.

\## 3. Ce qui est écrit

- `reports/rapport-cerveau-corrections.md` §11bis : split, oracle, marge, verdict négatif.
- `docs/pilotage/backlog/B12.10-pipeline-m1-m4-m8.md` : **mesurée**, porte « non franchie — et vide », prochaine action **aucune**.
- `docs/pilotage/backlog/index.md` : B12.10 **mesurée**.
- `docs/pilotage/roadmap.md` : B12.10 **close (négatif)** ; B11.10 devient l'autonome suivant.
- `docs/pilotage/en-cours.md` : B12.10 close négative ; prochaine action **B11.10** (cartes et ambiguïtés).
- `journal/2026-10-29/etat-transfere.md` : ligne B12.10 négative.
- `tools/cerveau/b1210_holdout.py` : oracle et politiques de marge ajoutés.

\## 4. Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 276 fiches · 340 JSON · 93 docs · 51 portes |
| `verifie_en_cours.py` | ✅ 1 119 mots · 3 sessions · 6 puces |
| `taille_documents.py` | ✅ tous les documents chargeables dans leur budget |
| `porte-tableaux.sh` | ✅ 988 liens |
| tests pipeline / bus | ✅ 3/3 · 3/3 |

**Réserve honnête** : 
… [521 caractères tronqués]

### Tour 10 — dans le en-cours.md ajoute un diagramme des dépendances des chantiers et activités avec les états correspondants

*22 appels d'outils.* Actions notables :

- bash — Read schema verifier constraints
- bash — Inspect existing SVG style and schema index
- bash — Read current en-cours state
- bash — Read schemas index and illustration rules
- bash — Read roadmap R and N tables for exact states
- bash — Generate SVG diagram and validate XML
- bash — Render SVG to PNG for visual inspection
- read_image
- bash — Reference diagram in en-cours and schema index
- bash — Check N and R dependencies for diagram accuracy
- bash — Locate N3/R2/N5 SVG lines
- bash — Locate N4 and dashed arrow
- bash — Correct N3/N4/R2 states and remove wrong N5 edge
- bash — Render and OCR diagram to check text presence
- … et 8 autres

**Synthèse produite :**

⏵ Diagramme ajouté : chantiers, activités, dépendances et états dans `en-cours`

**Fait — commit `076d15ef`.** Le diagramme est dans [`docs/schemas/chantiers-etats.svg`](docs/schemas/chantiers-etats.svg) et inséré dans [`en-cours.md`](docs/pilotage/en-cours.md), section **« Les chantiers et leurs bloquants »**.

\## Ce que montre le schéma

- **Quatre colonnes** : A le moteur · B l’intelligence · N le natif · R le lecteur.
- **Six états** : mesuré/close, en cours, à faire/partiel, bloqué, négatif, gelé.
- **Dépendances** : N0 → N1 → N2 ; N2 → R1 ; N4 → R3 ; R0.1 → R0.2 → R0.3 → R0.4 ; R0.3 → R4 et R1 ; R1 → R2 → R3 → R5. Le pointillé **R1 → N5** marque N5 gelé jusqu’au verdict de R1.1.
- **Sessions actives** dans la boîte de leur activité : `f0969e87` → B11.10, `8156fdcb` → R0.3, `N2-GPU` → N2.
- **Bandes transverses** : C1–C7 mesurés et transférés au journal ; backlog 29 fiches / 41 arêtes dures / 8 sans fiche.

J’ai aussi corrigé la ligne R de `en-cours` (R0.2 mesuré, R0.3 en cours, puis R0.4) et ajouté le schéma à l’index [`docs/schemas/README.md`](docs/schemas/README.md) — il passe de cinq à six schémas directs.

\## Vérifications

| contrôle | résultat |
|---|---|
| `verifier_schemas.py` | ✅ 22 SVG · schéma valide et référencé |
| `verifie_en_cours.py` | ✅ 1 171 mots · 6 puces |
| `taille_documents.py` | ✅ budgets respectés |
| `porte-tableaux.sh` | ✅ 989 liens |
| `revue_documentation.py` | ⚠️ 1 rouge : `en-cours` dit **341** JSON, le disque en a **342** |

La rouge est encore la session R0.3 : elle a ajouté `reports/r03-banc-extractif.json` sans avoir committé la mise à jour du compteur. Son commit la corrigera ; je n’ai pas touché à ses fichiers (`docs/implantation/banc-lecture.md`, `tools/banc_lecture.py`, `tools/banc_complet.py`, `reports/r03-banc-extractif.json`, `tools/tests/documents/bench-complet.json`).

### Tour 11 — quel est ton ide de session dsh?

*1 appels d'outils.* Actions notables :

- bash — Read current DSH session id

**Synthèse produite :**

Mon ID de session DSH actuel est :

**`71d57f53-8b41-4220-84dd-7bb9eedc88d9`**

Attention : `en-cours.md` porte encore **`f0969e87-af0c-43b1-93cf-f278d9c90846`** comme ID de la session principale. C’est l’ID enregistré dans l’état, mais il ne correspond plus au processus DSH courant — probablement une reprise ou un fork. Si tu veux, je mets `71d57f53` à jour dans `en-cours.md`.

### Tour 12 — f0969e87 est encore une session active dans une autre fenêtre. Est-ce que les directives à la racine du projet permetten … [63 caractères tronqués]

*26 appels d'outils.* Actions notables :

- read
- bash — Read en-cours structural checker
- ask_user_question
- bash — Create isolated worktree at HEAD
- bash — Read latest en-cours at shared HEAD
- bash — Check latest directives and sizes
- bash — Apply proposed patch in isolated worktree and check
- bash — Read document budget rules
- bash — Measure rule 10 budget headroom
- bash — Try compact directive patch within budgets
- bash — Read T0 total calculation
- bash — Check compact AGENTS candidate word count
- bash — Apply compact patch and check budgets
- bash — Adjust session status and measure tight T0 budget
- … et 11 autres

**Synthèse produite :**

⏵ Diff multi-sessions prêt et vérifié sur HEAD `7d47b3c7`

**Réponse courte : non, pas en l’état.** Les directives couvrent bien **principal + sous-agents**, mais pas **plusieurs fenêtres DSH de même rang**. Le patch préparé corrige le minimum, et il tient dans le budget **par compression** : `T0 = 3 998 / 4 000` mots, soit **2 mots de marge**.

\## Le patch

[`docs/pilotage/patch-multi-session.diff`](docs/pilotage/patch-multi-session.diff) — basé sur `7d47b3c7`, **non committé**, vérifié avec :

```bash
git apply --check docs/pilotage/patch-multi-session.diff
```

Il touche trois fichiers (`34 insertions, 19 suppressions`) :

| fichier | changement |
|---|---|
| `AGENTS.md` | règle 10 compactée : `DSH_SESSION_ID` absent des sessions = **pair**, même **diff** ; `git add` explicite, jamais `-A`/`commit -a` |
| `docs/methode/continuite.md` | ligne **identité DSH** (pair, réservations, goal, sans principale → l’humain désigne, session fermée → rouvrir son bloc) ; rôle **principale/pair** ; Git concurrent ; compressions pour rester sous 1 200 mots |
| `docs/pilotage/en-cours.md` | note **identité** ; bloc **`71d57f53` — pair** ; `f0969e87` **close dans l’état, fenêtre encore ouverte** ; `8156fdcb`/`N2-GPU` mis à jour |

\## Vérifications du patch appliqué

| contrôle | résultat |
|---|---|
| `git apply --check` | ✅ |
| `verifie_en_cours.py` | ✅ 1 196 mots · 3 sessions · 6 puces |
| `taille_documents.py` | ✅ T0 **3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `AGENTS.md` | 1 200 / 1 200 |
| `continuite.md` | 1 197 / 1 200 |

\## La limite à connaître

Le patch **ne crée pas** le registre complet (heartbeat, goal par session, table des réservations). Il n’y a plus la place : `AGENTS.md` est à 1 200/1 200 et `continuite.md` à 1 197/1 200. Pour aller plus loin sans écraser les directives, il faut créer **`docs/methode/sessions.md`** (T0, budget 1 200) et ne laisser dans `AGENTS`/`continuite` qu’un **lien** vers ce document. C’est l’alternative propre à la compression actuelle.

À appliquer par la principale désignée (ou par toi) :

```bash
git apply docs/pilotage/patch-multi-session.diff
```

Je n’ai ni appliqué ni committé le patch ; `en-cours` partagé n’a pas été modifié par cette préparation.

### Tour 13 — fais-le

*8 appels d'outils.* Actions notables :

- bash — Check current HEAD and patch applicability
- bash — Apply multi-session patch to working tree
- bash — Update pair block after applying patch and check budgets
- bash — Run all checks after applying patch
- bash — Inspect dead path and concurrent JSON
- bash — Fix dead path and re-run documentation checks
- bash — Commit applied multi-session patch
- bash — Remove applied patch and run final checks

**Synthèse produite :**

⏵ Patch multi-sessions appliqué, vérifié et commité

**C’est fait — commit `6e995187`.** Le diff a été appliqué puis supprimé du dépôt ; le commit est désormais la référence.

\## Ce qui a changé

- **`AGENTS.md`** — règle 10 : `DSH_SESSION_ID` absent des sessions = **pair** ; même **diff d’état** qu’un sous-agent ; `git add` explicite, jamais `-A`/`commit -a`.
- **`docs/methode/continuite.md`** — ligne **identité DSH** (pair, réservations, goal, sans principale → l’humain désigne, session fermée → rouvrir son bloc), rôle **principale/pair**, Git concurrent.
- **`docs/pilotage/en-cours.md`** :
  - note d’identité en tête des sessions ;
  - bloc **`71d57f53` — pair** avec son travail réel (N0.3b, B12.10, diagramme) ;
  - `f0969e87` **close dans l’état, fenêtre encore ouverte** ;
  - `8156fdcb` / `N2-GPU` mis à jour ;
  - chemin mort `docs/implantation/{...}` remplacé par les deux chemins explicites.

Le bloc `71d57f53` indique maintenant : **patch appliqué avec l’accord de l’humain**, et ne pas écrire l’état sans nouvel accord.

\## Vérifications

| contrôle | résultat |
|---|---|
| `verifie_en_cours.py` | ✅ 1 197 mots · 3 sessions · 6 puces |
| `taille_documents.py` | ✅ T0 **3 999 / 4 000** ; en-cours 1 197 / 2 000 |
| `porte-tableaux.sh` | ✅ 1 002 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `revue_documentation.py` | ⚠️ 1 rouge : en-cours dit **345** JSON, le disque en a **347** |

La rouge est **entièrement la session R0.3 concurrente** : elle a ajouté `reports/r03-banc-durci-extractif.json` et `reports/r03-banc-durci-modele.json` sans encore mettre le compteur à jour. Je n’ai pas touché à ses fichiers (`tools/banc_lecture.py`, `tools/banc_durci.py`, `tools/bloc_tableaux.py`, `bench-durci.json`, etc.) ; son prochain commit corrigera le compteur.

\## La limite reste

Le patch tient à **1 mot près** dans le budget T0. Pour un registre complet — heartbeat, goal par session, table des réservations — il faut créer **`docs/methode/sessions.md`** et ne laisser qu’un lien dans `AGENTS`/`continuite`. La base d’identification est maintenant là ; le registre détaillé est le prochain pas.

### Tour 14 — ensuite?

*18 appels d'outils.* Actions notables :

- bash — Check latest HEAD, sessions and principal
- bash — Check state before proposing next step
- ask_user_question
- bash — Inspect codec dispatcher and ambiguity handling
- bash — Test ambiguous surfaces with real RSN contexts
- bash — Measure no-game dispatcher on ambiguous surfaces
- bash — Check tests for no-game codec dispatcher
- bash — Check base imports and codec test setup
- bash — Check MULTI import in base
- bash — Add ambiguity guard and tests
- bash — Measure cards and ambiguity guard
- bash — Run games gate after ambiguity guard
- bash — Check reports index convention before adding fiche
- bash — Write B11.10 report and JSON
- … et 4 autres

**Synthèse produite :**

⏵ B11.10 livré en pair : garde d'ambiguïté, mesure et fiche, sans toucher à l'état partagé

**Fait — commit `989102e1`.** B11.10 est mesurée, et sa prémisse est corrigée : le codec lit les cartes à **100 %** ; le **69,3 %** est le champ `carte` du **parseur natif**.

\## Le résultat

| mesure | avant | après |
|---|---:|---:|
| codec cartes, code exact | **161 / 161** | **161 / 161** |
| `A1` sans jeu | morpion, case 0 | **refus** (4 jeux) |
| `E4` sans jeu | go, point 289 | **refus** (4 jeux) |
| `d4` sans jeu | go, point 288 | **refus** (4 jeux) |
| `b6-c5` sans jeu | dames, chemin `[8, 13]` | **refus** (2 jeux) |
| avec le jeu explicite | — | **4 / 4 exact** |
| `e2e4` / `2D` | échecs / cartes | inchangés |

- **Le trou n’était pas le codec** : le dispatcher sans jeu choisissait `go` pour `E4`/`d4`, `morpion` pour `A1`, `dames` pour `b6-c5`, sans nommer les autres candidats.
- **La garde** refuse désormais une coordonnée nue (ou `a1-b2`) quand ni le jeu ni le contexte ne sont donnés, et nomme les jeux candidats ; avec un jeu explicite, tout passe comme avant.
- **Contrôles** : 27 tests de codecs, `porte-jeux` **exit 0** (100 % au niveau 4, 33/33 paires, 0 collision, 71 langues).
- **Le 69,3 %** est celui de B11.7 (champ natif) ; il n’y a **pas** d’extension codec à faire pour les cartes. Reste une tête `carte` native ou une route hybride.

\## Fichiers

- `tools/jeux/codecs/base.py` — garde `_ambiguite_de_surface`.
- `tools/jeux/tests/test_codecs.py` — `TestAmbiguites`.
- [`reports/rapport-b1110-cartes.md`](reports/rapport-b1110-cartes.md) · [`reports/b1110-cartes.json`](reports/b1110-cartes.json).

\## État

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 283 fiches · 350 JSON · 94 docs · 52 portes |
| `verifie_en_cours.py` | ✅ 1 204 mots · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 013 liens |
| `taille_documents.py` | ❌ **T0 4 006 / 4 000** |

La seule rouge est le **budget T0** : la session R0.4 a ajouté des mots à `en-cours` ; il faut en couper **6**. Je ne l’ai pas fait — je suis pair et l’état est en cours d’édition par l’autre session.

\## Diff d’état à intégrer par la principale

- `docs/pilotage/backlog/B11.10-cartes-ambiguites.md` : statut **mesurée** ; fiche
  [`rapport-b1110-cartes.md`](../../reports/rapport-b1110-cartes.md) ; porte « **atteinte** — ambiguïtés refusées, cartes 161/161 ; le 69,3 % est natif ».
- `en-cours` : ligne B → **B11.10 mesurée** ; prochaine action B10.3 (bloqué) ou la ligne suivante.
- T0 : couper 6 mots 
… [52 caractères tronqués]

### Tour 15 — continue

*21 appels d'outils.* Actions notables :

- bash — Check latest state and budgets
- bash — Read next A chantier sheets
- bash — Read A programme details and source
- bash — Find A3.2/A2.6 details
- bash — Read placement scheduler code
- bash — Find granularity/threshold specs and placement usage
- bash — Search archived roadmap for A3 details
- bash — Check integrated next actions after B11.10
- bash — Check B11 native parser artifacts
- bash — Check A3.3 threshold in code and report
- bash — Read topology and plan placement code
- bash — Check A8 placement-perte wiring
- bash — Inspect A8.3 flag and PPL gates
- bash — Trace A3.3 threshold evidence
- … et 7 autres

**Synthèse produite :**

⏵ A8.0 livré en pair : audit des portes PPL, résultat négatif net

**Fait — commit `0731544b`.** A8.0 est diagnostiquée : **aucune des 33 portes qui mesurent une PPL n’épingle de référence externe**. A8.3 ne peut donc pas passer par défaut.

\## Le résultat

| ce que la porte fait de la PPL | portes |
|---|---:|
| la mentionne (log, grep, affichage) | **33** |
| la compare **dans le même run** (identité, budget, dense/creux) | **7** |
| la compare à une **référence externe** | **0** |

Les 7 comparaisons intra-run : `porte-adaptateur-sortie`, `porte-budget`, `porte-horloge`, `porte-pannes`, `porte-poids-creux`, `porte-profondeur-routee`, `porte-registre`.

**Conséquence** : une régression **commune aux deux bras** d’une comparaison passe. Si le défaut dégrade la PPL de 1 %, les deux exécutions la dégradent ensemble et l’égalité tient. Les portes vérifient la **cohérence**, pas la **valeur**.

\## Fichiers

- [`reports/rapport-a80-portes-ppl.md`](reports/rapport-a80-portes-ppl.md)
- [`reports/a80-portes-ppl.json`](reports/a80-portes-ppl.json)

\## État

| contrôle | résultat |
|---|---|
| `porte-tableaux.sh` | ✅ 1 016 liens |
| `verifie_en_cours.py` | ✅ 1 204 mots · 3 sessions |
| `revue_documentation.py` | ⚠️ compteurs : en-cours 284/351, disque 285/352 |
| `taille_documents.py` | ❌ T0 **4 006 / 4 000** |

Les deux rouges sont **d’état**, pas de contenu : B11.10 et A8.0 ne sont pas encore intégrés dans `en-cours`, et la session R07 a ajouté des fichiers non committés. Je reste **pair** : je ne touche ni à `en-cours`, ni à `roadmap`, ni au backlog.

\## Diff d’état pour la principale

- **B11.10** : statut **mesurée** ; fiche [`rapport-b1110-cartes.md`](../../reports/rapport-b1110-cartes.md) ; « ambiguïtés refusées, cartes 161/161 ; 69,3 % = natif ».
- **A8.0** : **diagnostic** ; fiche [`rapport-a80-portes-ppl.md`](../../reports/rapport-a80-portes-ppl.md) ; prochaine action **épingler `porte-flux`** (références **61,9920 / 60,8135**) avec une tolérance par porte et par modèle.
- **T0** : couper **6 mots** dans `en-cours` (4 006 → ≤ 4 000).
- **A3.2/A3.3** : déjà mesurées dans l’archive (`1 608 octets/flux`, seuil `3,2×`), à réconcilier dans la roadmap ; **A2.6** est partiel (experts bloqués par A6.2, tête revertée).

**Prochain pas** : épingler `porte-flux`, puis `porte-pont`, avant de basculer A8.3 par défaut.

### Tour 16 — continue avec plusieurs goals et un quota de round très élevé. Tu dois avancer en autonomie pendant plus de 3h.

*125 appels d'outils.* Actions notables :

- create_goal
- todo_write
- bash — Read porte-flux gate
- bash — Read porte-pont gate
- bash — Find stable PPL references for gates
- bash — Run porte-flux and capture PPL values
- bash — Pin porte-flux PPL references and run gate
- bash — Write A8.0 first-pin report and control
- bash — Commit porte-flux PPL pin
- bash — Run porte-pont and capture relative PPL curve
- bash — Read porte-pont section 8
- bash — Pin porte-pont PPL and cliff references
- bash — Apply porte-pont pins with inner delimiter
- bash — Write porte-pont pin report and update audit
- … et 110 autres

**Synthèse produite :**

⏵ Goal d'autonomie terminé : A8.0/A8.3, B11.10, A2.6/A3.2/A3.3 et R13.0 livrés

**Goal `goal-f80fefb9…` marqué `complete`.** Le cycle autonome a produit des résultats mesurés, des fiches, des commits et un état à jour ; toutes les vérifications de clôture passent.

\## A8.0 — 7 portes PPL épinglées sur 33

| porte | référence épinglée | contrôle |
|---|---|---|
| `porte-flux` | 61,9920 / 60,8135 | 5 modes, 5e-4 |
| `porte-pont` | 113,0068 / 111,9225 ; falaise +2,81 / +25,35 | 5e-4 / 0,05 pt |
| `porte-topologie` | 17,4702 / 30,4363 / 42,5477 | 5e-4 |
| `porte-coupe` | 113,0068 ; +0,52…+17,09 | 5e-4 / 0,05 pt |
| `porte-reparti-moteur` | 9,1748 | 1e-3 |
| `porte-budget` | 111,9225 | 5e-4 |
| `porte-adaptateur-sortie` | 17,4315 / 2 687 292,8165 | 5e-4 |

Chaque pin a son **contrôle négatif** (décalage de 10 % refusé) et sa fiche dans `reports/`.

\## A8.3 — opt-in conservé, A8.3a livré

- **A8.3** : le défaut place+perte déplace les portes de **−5,9 % à +19,5 %** ; décision **opt-in** (rapport `a83-defaut`).
- **A8.3a flux** : régime 1 % épinglé — **58,3200 / 62,7357**, écarts codec 1,14e-1 / 3,49e-2.
- **A8.3a pont** : **111,8003 / 115,6406**, falaise **+5,88 / +25,75**.
- **A8.3a coupe** : **111,8003**, variance encodée **2,4 %** contre 8,9 % en f32.
- Les trois gates passent en **f32** et en **1 %** avec deux références distinctes ; A8.3b (défaut) reste ouvert.

\## Autres lignes

- **B11.10** : codec **161/161** cartes ; ambiguïtés `A1/E4/d4/b6-c5` **refusées** avec jeux candidats ; le **69,3 %** est le champ natif. Commit `989102e1`.
- **A2.6** : **partielle** — générique et KV faits, tête 4 bits refusée, experts bloqués par **A6.2**. Commit `09588098`.
- **A3.2/A3.3** : mesurées et réconciliées (1 608 octets/flux, seuil 3,2×).
- **R13.0** : BPE **3,4–5,2 octets/jeton** (latin), **2,8** (arabe/cyrillique), **1,63** au hasard ; réversible ; **PPL non mesurée**. Commit `98e0b6e1`.

\## État et portes

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 306 fiches · 377 JSON · 105 docs · 58 portes |
| `taille_documents.py` | ✅ **T0 3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 196 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 084 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`c9b3da49`) |

Les fichiers non committés restants appartiennent à la session R0.5/R4 (`banc-lecture`, backlog, journal) ; je n’y ai pas touché.

**Prochaines actions naturelles**
… [153 caractères tronqués]

### Tour 17 — continue avec plusieurs goals et un quota de round très élevé. Tu dois avancer en autonomie pendant plus de 3h.

*21 appels d'outils.* Actions notables :

- create_goal
- todo_write
- bash — Inspect porte-gain
- bash — Inspect prefill gate
- bash — Run porte-gain to capture PPL references
- bash — Check native model and N3 assets
- bash — Read N3 fiche
- bash — Find native operation CLI flags
- bash — Find service/early-exit engine paths
- bash — Pin porte-gain key PPL and run
- bash — Verify gain PPL pins fired
- bash — Write gain pin report and state 8/33
- bash — Fix counters and commit gain pin 8/33
- bash — Check native model tokenizer capability for R13.1
- … et 7 autres

**Synthèse produite :**

⏵ Deuxième cycle livré ; le goal reste actif pour N3.2, la seule ligne non fermée

\## Ce qui a été livré

**A8.0 — 8 portes PPL épinglées sur 33**

| porte | référence | contrôle |
|---|---|---|
| `porte-gain` | **14,6496** / 12,9635 / 15,4298 / 14,1057 / **996,0390** | 5e-4, décalage 10 % refusé |
| `porte-adaptateur-sortie` | **17,4315** / **2 687 292,8165** | 5e-4 |
| `porte-reparti-moteur` | **9,1748** | 1e-3 |
| `porte-budget` | **111,9225** | 5e-4 |
| flux, pont, topologie, coupe | déjà épinglées | 5e-4 / 0,05 pt |

**A8.3a — les trois régimes 1 % sont pinnés**

| porte | f32 | 1 % |
|---|---|---|
| flux | 61,9920 / 60,8135 | **58,3200 / 62,7357** |
| pont | 113,0068 / 111,9225 ; +2,81 / +25,35 | **111,8003 / 115,6406 ; +5,88 / +25,75** |
| coupe | 113,0068 ; variance 8,9 % | **111,8003 ; variance 2,4 %** |

Les six gates passent dans les deux régimes. **A8.3 reste opt-in** : A8.3b n’est pas tenté, la décision de défaut reste refusée par la mesure.

**R13.1 — condition nommée**

- `NativeConfig.vocab = 256`, tokenizer `bytes` ; aucun checkpoint BPE natif.
- La PPL BPE-native n’est **pas mesurable** sans entraîner un modèle BPE natif au même budget ; comparer Qwen BPE à `drave-n0` comparerait deux modèles.
- R13 reste **ouverte** ; prochaine campagne : tokenizer abstrait + modèle BPE natif + bits/octet à budget égal.

**N3.1 — inventaire, pas de porte composée**

- Sortie précoce : `porte-reflexe` mais **bench**, pas service.
- Rejeu, placement, pont, coupe : portes présentes.
- Profondeur routée : rapport design-H, **aucune porte**.
- k-WTA/routes : **aucun chemin**.
- Une méta-porte qui lance les portes existantes ne testerait pas la composition ; N3.2 (service sortie précoce), N3.3 (k-WTA/routes), N3.4 (profondeur routée) sont nommés.

\## État et vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 312 fiches · 384 JSON · 108 docs · 58 portes |
| `taille_documents.py` | ✅ **T0 4 000 / 4 000** ; en-cours 1 198 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 198 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 097 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`1ec24a7f`) |

**Commits clés** : `9216634d` (gain), `f900db9a` / `0e8f7a20` / `d8df29e0` (A8.3a flux/pont/coupe), `ba0c4ac5` (R13.1), `1ec24a7f` (N3.1), `8770ea50` (adaptateur).

Les fichiers non committés restants sont le journal et les fiches de la session R0.5/R4 ; je n’y ai pas touché.

\## Goal

`goal-46e
… [193 caractères tronqués]

### Tour 18 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [996 caractères tronqués]

*14 appels d'outils.* Actions notables :

- bash — Inspect current state before A8.3b
- bash — List PPL gates and dual-regime gates
- bash — Read current A8 state and A8.3b report
- bash — Read A8.3b regimes report
- bash — Inspect routed-depth gate and N3 inventory contradiction
- bash — Check when routed-depth gate and N3.1 were added
- bash — Correct N3.1 inventory and reconcile A8.0 8 gates
- bash — Commit N3.1 correction and A8.0 reconciliation
- bash — Inspect native service and early exit path
- bash — Inspect cycle-c2 PPL gate
- bash — Run cycle-c2 to capture reference PPL
- bash — Pin cycle-c2 PPL and rerun
- bash — Write cycle-c2 pin report and state 9/33
- bash — Commit cycle-c2 pin and state 9/33

**Synthèse produite :**

⏵ Tour 1 terminé : A8.0 passe à 9/33, N3.1 est corrigé, le goal reste actif pour N3.2

\## Ce qui a avancé

**A8.0 — 9 portes PPL épinglées sur 33**

- `porte-cycle-c2` : PPL de référence **14,6496** (5e-4), pas 1 exact, trajectoire `14,6496 → 275,5153 → 940,2153 → 2 988,4562`, λ **488,82**.
- La liste compte désormais : flux, pont, topologie, coupe, réparti, budget, adaptateur, gain, cycle-c2.
- Les compteurs d’état disent **9 portes** ; l’ancien « 6 » a été réconcilié avec les fiches et les commits.

**A8.3b — déjà mesuré, et je ne le duplique pas**

La session `c3d0f0bd` a livré `rapport-a83b-regimes` : trois régimes — f32, mélange 1 %, int8 partout — et la décision **opt-in** maintenue, avec le mode de lot comme prochain isolement. L’état A le référence maintenant.

**N3.1 — correction importante**

L’inventaire disait « profondeur routée : aucune porte ». C’est faux : `tools/porte-profondeur-routee.sh` existe depuis le 10/10. La fiche et le JSON sont corrigés :

| brique | porte | service |
|---|---|---|
| sortie précoce | `porte-reflexe` | **non** (bench) |
| rejeu | `porte-trace` | oui |
| placement | `porte-topologie` | oui |
| pont | `porte-pont` | oui |
| coupe | `porte-coupe` | oui |
| profondeur routée | **`porte-profondeur-routee`** | pas de service |
| k-WTA/routes | **aucune** | **aucun chemin** |

Il ne reste donc **qu’une brique sans porte** (`k-WTA/routes`) ; la porte composée reste prématurée.

**R13.1** reste la condition nommée : le modèle natif est en octets (`vocab = 256`), aucun checkpoint BPE natif ; la PPL BPE-native exige une campagne, pas un patch.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 313 fiches · 385 JSON · 108 docs · 58 portes |
| `taille_documents.py` | ✅ **T0 3 997 / 4 000** ; en-cours 1 195 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 195 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 097 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`9ca7b1d2`) |

**Commits du round** : `3c227622` (correction N3.1 + A8.0), `9ca7b1d2` (cycle-c2, 9/33).

\## Goal

`goal-46eac0c4…` reste **actif**. La seule case non fermée est la **porte N3 composée** : elle exige N3.2 (sortie précoce en service) puis N3.3 (`k-WTA/routes`), avant la composition. Prochain round : N3.2, ou une dixième porte PPL (`porte-profondeur-routee` est longue, `porte-reflexe` est plus courte).

### Tour 19 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [996 caractères tronqués]

*9 appels d'outils.* Actions notables :

- bash — Inspect flux gate lot measurement path
- bash — Read flux gate mode definitions
- bash — Measure PPL vs lot size under f32 and 1% rule
- bash — Check corpus dependency
- bash — Write A8.3b lot-path report and state
- bash — Commit A8.3b lot-path result
- bash — Check N3.2 service early-exit progress
- bash — Verify round 2 results and state

**Synthèse produite :**

⏵ Tour 2 bouclé : A8.3b est rétréci au chemin de lot, A8.0 passe à 9/33, N3.1 est corrigé

\## Résultat principal : A8.3b.1 — le signe vient du **chemin lot**, pas de la taille

Mesure `--ppl-reparti`, Qwen2.5-0.5B Q8_0, 12 couches locales, 24 jetons, ctx 64 :

| lot | f32 | mélange 1 % |
|---:|---:|---:|
| **1** | **61,9920** | **58,3200** |
| 2 | **60,8135** | **62,7357** |
| 4 | **60,8135** | **62,7357** |
| 8 | **60,8135** | **62,7357** |
| 16 | **60,8135** | **62,7357** |

- **Lot 1 = pas de lot** : les chiffres redonnent exactement le mode 0.
- **Lot ≥ 2** : identiques à quatre décimales ; la taille de lot ne porte pas l’effet.
- En f32, lotter **améliore** (−1,9 %) ; sous la règle 1 %, lotter **dégrade** (+7,6 %). Le signe bascule avec le **chemin**, pas avec la taille.
- A8.3 reste **opt-in** ; le prochain pas est le cache/occupation (même lot, ctx/cache différents) ou la lecture du code du chemin lot — plus un balayage de tailles.

\## A8.0 — 9 portes PPL épinglées sur 33

- `porte-cycle-c2` : référence **14,6496** (5e-4), pas 1 exact, trajectoire `14,6496 → 275,5153 → 940,2153 → 2 988,4562`, λ **488,82**.
- Liste : flux, pont, topologie, coupe, réparti, budget, adaptateur, gain, cycle-c2.
- L’état a été réconcilié : l’ancien « 6 portes » est corrigé à **9**.

\## N3.1 — correction

`tools/porte-profondeur-routee.sh` existe depuis le 10/10 ; l’inventaire disait « aucune porte ». Corrigé :

| brique | porte | service |
|---|---|---|
| sortie précoce | `porte-reflexe` | **non** (bench) |
| rejeu, placement, pont, coupe | portes présentes | oui |
| profondeur routée | **`porte-profondeur-routee`** | pas de service |
| k-WTA/routes | **aucune** | **aucun chemin** |

Il ne reste **qu’une brique sans porte** (`k-WTA/routes`). La porte composée reste prématurée ; N3.2 (service sortie précoce) et N3.3 (k-WTA/routes) sont les prochains pas.

\## R13.1

Condition nommée : `NativeConfig.vocab = 256`, tokenizer `bytes`, aucun checkpoint BPE natif ; la PPL BPE-native exige une campagne (tokenizer abstrait + modèle BPE natif), pas un patch.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 314 fiches · 386 JSON · 108 docs · 58 portes |
| `taille_documents.py` | ✅ **T0 3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 196 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 100 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`b5a9cdec`) |

**Commits
… [321 caractères tronqués]

### Tour 20 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [996 caractères tronqués]

*20 appels d'outils.* Actions notables :

- bash — Inspect native service CLI and current state
- bash — Read native PPL CLI and service
- bash — Inspect N4 native execution gate model prerequisite
- bash — Check native training/export prerequisites
- bash — Inspect native server parity tooling
- bash — Check native DRVM export fixture tooling
- bash — Read native config/exporter/generation
- bash — Create and run N3 native service gate
- bash — Debug native service generation crash
- bash — Inspect native.rs panic line
- bash — Fix native model max_pos and rerun service gate
- bash — Debug max_pos 2048 native service crash
- bash — Inspect position embedding shape
- bash — Inspect DRVM position tensor shape
- … et 6 autres

**Synthèse produite :**

⏵ Tour 3 bouclé : N3.2a est une porte verte de service natif, A8.3b est rétréci au chemin de lot

\## N3.2a — le service natif est vivant et gardé

Nouvelle porte `tools/porte-n3-service.sh`, avec un DRVM **reproductible** (graine 7, 1 bloc, 4 experts top-2, kwta 0,5, vocab 256, **113 292** paramètres), exporté à la volée :

| contrôle | résultat |
|---|---|
| `/sante` | **113 292** paramètres, identiques au modèle |
| génération « abc » × 2 | **11 octets**, textes identiques |
| génération « zzz » | 11 octets, texte **différent** |
| `/inconnu` | **404** |

- Le service `--drvm-serve` démarre, répond et **refuse** les chemins inconnus.
- Le modèle synthétique est régénérable par la porte : pas de dépendance à un fichier `/tmp`.
- **Limite nommée** : ce n’est pas la sortie précoce ; c’est **N3.2a**, le service natif. N3.2b (early exit en service), N3.3 (`k-WTA/routes`) et la composition restent.
- Le compteur de portes passe à **59** (55 vertes, 2 rouges structurelles).

\## A8.3b.1 — le signe vient du **chemin lot**, pas de la taille

| lot | f32 | mélange 1 % |
|---:|---:|---:|
| **1** | **61,9920** | **58,3200** |
| 2 | **60,8135** | **62,7357** |
| 4 | **60,8135** | **62,7357** |
| 8 | **60,8135** | **62,7357** |
| 16 | **60,8135** | **62,7357** |

Lot 1 = pas de lot ; lot ≥ 2 identique à quatre décimales. En f32, lotter améliore (−1,9 %) ; sous la règle 1 %, lotter dégrade (+7,6 %). Le basculement est **binaire**, pas une taille. A8.3 reste opt-in ; le prochain pas est le cache/occupation.

\## A8.0 — 9 portes PPL épinglées

- `porte-cycle-c2` : référence **14,6496**, pas 1 exact, trajectoire `14,6496 → 275,5153 → 940,2153 → 2 988,4562`, λ **488,82**.
- Liste : flux, pont, topologie, coupe, réparti, budget, adaptateur, gain, cycle-c2.
- L’état a été réconcilié (l’ancien « 6 » est corrigé à **9**).

\## N3.1 — correction

`tools/porte-profondeur-routee.sh` existe ; l’inventaire disait « aucune porte ». Corrigé. Il ne reste **qu’une brique sans porte** (`k-WTA/routes`) ; la sortie précoce a une porte **bench**, pas service.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 315 fiches · 387 JSON · 108 docs · 59 portes |
| `taille_documents.py` | ✅ **T0 3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 196 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 101 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`bb6bfd4b`) |

**Commits du round
… [391 caractères tronqués]

### Tour 21 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [996 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Create and run N3 routing/k-WTA gate
- bash — Write N3.3a routing report and state
- bash — Commit N3.3a routing gate
- bash — Final checks for round 4

**Synthèse produite :**

⏵ Tour 4 bouclé : N3.3a prouve que le routage/k-WTA agit, la porte 60 est verte

\## N3.3a — le routage/k-WTA est vivant

Nouvelle porte `tools/porte-n3-routes.sh`, sur deux DRVM de **mêmes poids** (graine 7, 113 292 paramètres) :

| contrôle | résultat |
|---|---|
| A (`top_k=2`, `kwta=0,5`), deux fois | **identique** (27 octets) |
| A contre B (`top_k=1`, `kwta=1,0`) | **différent** |
| paramètres A / B | **113 292 / 113 292** |

Les deux modèles partagent le même `state_dict` ; seule la configuration de routage change. La différence de génération est donc **causée par le routage**, pas par les poids.

**Limite nommée** : la porte prouve que le routage **agit**, pas qu’il est **juste** ; `top_k` et `kwta` changent ensemble, et la sparsité n’est pas comptée. C’est **N3.3b**.

\## N3 — état des portes

| brique | porte | état |
|---|---|---|
| service natif | `porte-n3-service` | ✅ N3.2a |
| routage/k-WTA | `porte-n3-routes` | ✅ N3.3a |
| rejeu, placement, pont, coupe | portes existantes | ✅ |
| sortie précoce | `porte-reflexe` | ✅ bench, **pas service** |
| **N3.2b** sortie précoce en service | — | ⏳ |
| **N3.3b** finesse de la sparsité | — | ⏳ |
| **composition N3** | — | ⏳ |

La porte 60 est verte : **56 vertes, 2 rouges structurelles**, 60 portes au total.

\## A8.3b.1 — rappel du résultat

Le signe du mélange 1 % vient du **chemin lot** (lot 1 contre lot ≥ 2), pas de la taille : lot 1 = 61,9920/58,3200 ; lot ≥ 2 = 60,8135/62,7357 (f32/1 %). Le basculement est binaire.

\## A8.0

**9 portes PPL sur 33** ; la dernière est `porte-cycle-c2` (14,6496, λ 488,82). La dixième sera `porte-profondeur-routee` (longue) ou `porte-reflexe` (plus courte).

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 316 fiches · 388 JSON · 108 docs · 60 portes |
| `taille_documents.py` | ✅ **T0 3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 196 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 102 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`5aa47f70`) |

**Commits du round** : `bb6bfd4b` (N3.2a, 59 portes), `5aa47f70` (N3.3a, 60 portes).

\## Goal

`goal-46eac0c4…` reste **actif** : N3.2a et N3.3a sont faits ; il reste **N3.2b** (sortie précoce dans le service), **N3.3b** (sparsité/top-k) et la **porte de composition**. Prochain round : N3.2b, ou la dixième porte PPL.

### Tour 22 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [996 caractères tronqués]

*14 appels d'outils.* Actions notables :

- bash — Inspect candidate PPL gates for 10th pin
- bash — Run porte-reflexe to capture PPL refs
- bash — Test consolidation gate for 10th PPL pin
- bash — Read consolidation PPL block
- bash — Pin consolidation PPL and rerun
- bash — Write consolidation pin report and state 10/33
- bash — Fix counters and commit consolidation pin 10/33
- bash — Final checks for round 5
- bash — Inspect malformed table in new B10.2bis report
- bash — Read first table header of report
- bash — Fix B10.2bis tables and commit with state
- bash — Read remaining malformed rows
- bash — Fix remaining B10.2bis table rows
- bash — Final checks after table fixes

**Synthèse produite :**

⏵ Tour 5 bouclé : dixième porte PPL épinglée, tableaux B10.2bis réparés, toutes les vérifications vertes

\## A8.0 — 10 portes PPL épinglées sur 33

Nouvelle porte `porte-consolidation` :

| mesure | valeur |
|---|---:|
| LoRA nul fusionné | **identique au bit** (531 068 480 octets) |
| PPL base | **17,4268** |
| PPL LoRA aléatoire | **17,1655** |
| rapport | **0,9850** |

Tolérance **5e-4**, contrôle négatif à 10 %, deux PPL ancrées. La liste compte désormais : flux, pont, topologie, coupe, réparti, budget, adaptateur, gain, cycle-c2, consolidation.

\## N3 — état

| brique | porte | état |
|---|---|---|
| service natif | `porte-n3-service` | ✅ N3.2a |
| routage/k-WTA | `porte-n3-routes` | ✅ N3.3a |
| rejeu, placement, pont, coupe | portes existantes | ✅ |
| sortie précoce | `porte-reflexe` | ✅ bench, **pas service** |
| N3.2b service early exit | — | ⏳ |
| N3.3b sparsité/top-k | — | ⏳ |
| composition N3 | — | ⏳ |

**60 portes** au total, 56 vertes, 2 rouges structurelles.

\## Correction externe

`porte-tableaux` a signalé deux tableaux du rapport B10.2bis (`rapport-b102bis-corpus-jw.md`) : colonne `graine` absente sur 9 lignes. Corrigé en deux commits ; les 1 113 liens résolvent.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 318 fiches · 390 JSON · 108 docs · 60 portes |
| `taille_documents.py` | ✅ **T0 4 000 / 4 000** ; en-cours 1 198 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 198 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 113 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`0eb5d9f2`) |

**Commits du round** : `f577e3c8` (consolidation, 10/33), `db6d4058` et `0eb5d9f2` (tableaux B10.2bis).

\## Goal

`goal-46eac0c4…` reste **actif**. N3.2a et N3.3a sont faits ; il reste **N3.2b** (sortie précoce en service), **N3.3b** (sparsité/top-k) et la **porte de composition**. Prochain round : N3.2b, ou une onzième porte PPL. Le budget T0 est exactement à 4 000 : toute nouvelle ligne d’état exigera un mot coupé ailleurs.

### Tour 23 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [996 caractères tronqués]

*10 appels d'outils.* Actions notables :

- bash — Read native pas loop and head
- bash — Add native service depth env and rebuild
- bash — Create and run N3.2b0 service depth gate
- bash — Compare service depth without timing jitter
- bash — Inspect native generation return semantics
- bash — Fix native service full-body read and rebuild
- bash — Run N3.2b0 depth gate after service fix
- bash — Write N3.2b0 report and update state
- bash — Commit N3.2b0 depth and service fix
- bash — Final checks for round 6

**Synthèse produite :**

⏵ Tour 6 bouclé : N3.2b0 branche la profondeur de service et corrige une lecture HTTP incomplète

\## N3.2b0 — la profondeur de service, et un vrai défaut corrigé

`DRAVE_NATIVE_PROFONDEUR=N` coupe le calcul natif après N blocs ; la porte compare profondeur 1 et profondeur pleine sur un petit DRVM reproductible (graine 7, 2 blocs, **132 528** paramètres).

**Le défaut trouvé** : avant correctif, la même requête `/generer` donnait parfois **12 octets** (corps vide) et parfois **15 octets** (prompt + 12 générés). Le service lisait la requête en **un seul `read`** ; le corps pouvait arriver dans un second segment TCP. Ce n’était pas un aléa du modèle, c’était une lecture incomplète.

**Correctif** : lire jusqu’à `Content-Length` et jusqu’à la fin des en-têtes, 64 Ko maximum.

| mesure après correctif | résultat |
|---|---|
| `/sante` | **132 528** paramètres |
| pleine profondeur × 2 | **15 octets**, identiques |
| profondeur 1 × 2 | **15 octets**, identiques |
| profondeur 1 contre pleine | **différentes** |
| `/sante` à profondeur 1 | **132 528**, identique |

La porte 61 est verte : **57 vertes, 2 rouges structurelles**.

\## N3 — état

| brique | porte | état |
|---|---|---|
| service natif | `porte-n3-service` | ✅ N3.2a |
| profondeur de service | `porte-n3-profondeur` | ✅ N3.2b0 |
| routage/k-WTA | `porte-n3-routes` | ✅ N3.3a |
| rejeu, placement, pont, coupe | portes existantes | ✅ |
| sortie précoce **avec seuil de confiance** | — | ⏳ N3.2b |
| sparsité/top-k fine | — | ⏳ N3.3b |
| composition N3 | — | ⏳ |

\## A8.0 / A8.3b

- **A8.0 : 10 portes PPL sur 33** (dernière : consolidation, 17,4268 / 17,1655).
- **A8.3b.1** : le signe du mélange vient du **chemin lot** (lot 1 contre lot ≥ 2), pas de la taille.
- **A8.3** reste opt-in.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 319 fiches · 391 JSON · 108 docs · 61 portes |
| `taille_documents.py` | ✅ **T0 3 999 / 4 000** ; en-cours 1 197 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 197 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 114 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`91b88113`) |

**Commits du round** : `91b88113` (N3.2b0 + correctif HTTP, 61 portes), `f577e3c8` (consolidation, 10/33), `db6d4058`/`0eb5d9f2` (tableaux B10.2bis).

\## Goal

`goal-46eac0c4…` reste **actif**. N3.2a, N3.2b0 et N3.3a sont faits ; il reste **N3.2b** (seuil de confiance), **N3.3b** (sparsité/top-k) et la **porte de c
… [63 caractères tronqués]

### Tour 24 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [996 caractères tronqués]

*15 appels d'outils.* Actions notables :

- bash — Inspect native FFN routing for sparsity gate
- bash — Read native ffn routing top-k
- bash — Create and run N3.3b sparsity separation gate
- bash — Write N3.3b report and update state
- bash — Fix counters and commit N3.3b sparsity gate
- bash — Wait for concurrent commit before N3.3b
- bash — Check counters after concurrent B10.2bis commit
- bash — Commit N3.3b sparsity separation
- bash — Final checks for round 7
- bash — Inspect concurrent en-cours additions
- bash — Check whether concurrent state commit lands
- bash — Wait for A8.3c state commit and check budget
- bash — Wait once more for concurrent A8.3c commit
- bash — Check A8.3c report commit state
- … et 1 autres

**Synthèse produite :**

⏵ Tour 7 bouclé : N3.2b0 (profondeur + correctif HTTP) et N3.3b (kwta/top_k séparés), 62 portes

\## N3.2b0 — profondeur de service + lecture HTTP complète

`DRAVE_NATIVE_PROFONDEUR=N` coupe le calcul natif après N blocs. La porte a trouvé un **vrai défaut** : le service lisait la requête en **un seul `read`** ; le corps pouvait arriver dans un second segment TCP, et la même requête donnait **12 octets** (corps vide) ou **15 octets**.

**Correctif** : lecture jusqu’à `Content-Length` et fin des en-têtes, 64 Ko max.

| après correctif | résultat |
|---|---|
| `/sante` | **132 528** paramètres |
| pleine profondeur × 2 | **15 octets**, identiques |
| profondeur 1 × 2 | **15 octets**, identiques |
| profondeur 1 contre pleine | **différentes** |

\## N3.3b — `kwta` et `top_k` agissent séparément

Trois DRVM de **mêmes poids** (graine 7, 113 292 paramètres) :

| modèle | `top_k` | `kwta` | sortie |
|---|---:|---:|---|
| A | 2 | 0,5 | référence, 27 octets |
| B | 2 | **0,25** | **différente** |
| C | **3** | 0,5 | **différente** |

A deux fois identique ; `kwta` seul change, `top_k` seul change. N3.3a changeait les deux ensemble ; N3.3b les sépare.

\## N3 — état

| brique | porte | état |
|---|---|---|
| service natif | `porte-n3-service` | ✅ N3.2a |
| profondeur de service | `porte-n3-profondeur` | ✅ N3.2b0 |
| routage/k-WTA | `porte-n3-routes` | ✅ N3.3a |
| kwta/top_k séparés | `porte-n3-sparsite` | ✅ N3.3b |
| rejeu, placement, pont, coupe | portes existantes | ✅ |
| seuil de confiance | — | ⏳ N3.2b |
| comptage direct des experts | — | ⏳ N3.3c |
| composition N3 | — | ⏳ |

**62 portes** : 58 vertes, 2 rouges structurelles.

\## A8.0/A8.3

- **A8.0 : 10 portes PPL / 33**.
- **A8.3c** (session `c3d0f0bd`) : lot 1 ≠ ≥2, **1,90 %** ; fiche `a83c-lot` — ses faits sont **staged**, pas committés par moi.
- **A8.3** reste opt-in ; A8.3b.1 avait montré le basculement binaire du chemin lot.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 322 fiches · 394 JSON · 108 docs · 62 portes |
| `taille_documents.py` | ✅ **T0 4 000 / 4 000** ; en-cours 1 198 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 198 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 124 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`cb36f86c`) |

**Commits du round** : `91b88113` (N3.2b0 + correctif HTTP, 61 portes), `cb36f86c` (N3.3b, 62 portes).

\## Goal

`goal-46eac0c4…` reste **actif** : N3.2a, N3.2b0, N3.3
… [174 caractères tronqués]

### Tour 25 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [996 caractères tronqués]

*9 appels d'outils.* Actions notables :

- bash — Inspect state before N3.3c
- bash — Add native sparsity counters and CLI, rebuild
- bash — Check CLI needle and whether counters saved
- bash — Add sparsity counters and CLI in correct files
- bash — Test sparsity counters on three models
- bash — Create and run N3.3c direct sparsity count gate
- bash — Write N3.3c report and update state
- bash — Commit N3.3c direct sparsity count
- bash — Final checks for round 8

**Synthèse produite :**

⏵ Tour 8 bouclé : N3.3c compte directement les experts et canaux actifs, porte 63

\## N3.3c — le moteur compte la sparsité réelle

Nouveau CLI `--drvm-sparsite` + compteurs atomiques dans `native.rs`. Trois DRVM de **mêmes poids** (graine 7, 113 292 paramètres, 1 bloc, prompt `abc`) :

| modèle | `top_k` | `kwta` | appels ffn | experts | canaux |
|---|---:|---:|---:|---:|---:|
| **A** | 2 | 0,5 | 3 | **6** | **48** |
| **B** | 2 | **0,25** | 3 | **6** | **24** |
| **C** | **1** | 0,5 | 3 | **3** | **24** |

- A deux fois : **identique**.
- `kwta` seul divise les canaux par 2 ; `top_k` seul divise les experts par 2.
- Le contrôle est le **comptage exact** `(3,6,48)`, `(3,6,24)`, `(3,3,24)`, pas une inégalité.

N3.3 est maintenant complet au niveau **config + comptage** : routage vivant (N3.3a), paramètres séparés (N3.3b), compteurs réels (N3.3c).

\## N3 — état

| brique | porte | état |
|---|---|---|
| service natif | `porte-n3-service` | ✅ N3.2a |
| profondeur de service | `porte-n3-profondeur` | ✅ N3.2b0 |
| routage/k-WTA | `porte-n3-routes` | ✅ N3.3a |
| kwta/top_k séparés | `porte-n3-sparsite` | ✅ N3.3b |
| comptage experts/canaux | `porte-n3-sparsite-compte` | ✅ N3.3c |
| rejeu, placement, pont, coupe | portes existantes | ✅ |
| seuil de confiance | — | ⏳ N3.2b |
| composition N3 | — | ⏳ |

**63 portes** : 59 vertes, 2 rouges structurelles.

\## A8.0 / A8.3

- **A8.0 : 10 portes PPL / 33**.
- **A8.3c** (session `c3d0f0bd`) : le lot n’est pas neutre, **1,90 %** ; la non-monotonie du KV était un **effet de chemin**.
- **A8.3** reste opt-in ; A8.3b.1 avait montré le basculement binaire lot 1 / lot ≥ 2.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 323 fiches · 395 JSON · 108 docs · 63 portes |
| `taille_documents.py` | ✅ **T0 3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 196 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 125 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`04357861`) |

**Commits du round** : `04357861` (N3.3c, 63 portes), `cb36f86c` (N3.3b), `91b88113` (N3.2b0 + correctif HTTP).

\## Goal

`goal-46eac0c4…` reste **actif** : N3.2a, N3.2b0, N3.3a, N3.3b et N3.3c sont faits ; il reste **N3.2b** (seuil de confiance) et la **porte de composition**. Prochain round : N3.2b, ou une onzième porte PPL.

### Tour 26 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [996 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Create and run N3.4a composition gate
- bash — Write N3.4a composition report and state
- bash — Commit N3.4a composition gate
- bash — Final checks for round 9

**Synthèse produite :**

⏵ Tour 9 bouclé : N3.4a compose service, profondeur, routage et comptage sur les mêmes modèles, porte 64

\## N3.4a — la composition des briques branchées

Nouvelle porte `tools/porte-n3-composition.sh` : deux DRVM de **mêmes poids** (graine 7, 132 528 paramètres, 2 blocs, `top_k=2` contre `top_k=1`) et un seul récit de mesure.

| contrôle | résultat |
|---|---|
| `/sante` | **132 528** paramètres |
| A pleine × 2 | **identique** (15 octets) |
| A profondeur 1 × 2 | **identique** et **différent** de A |
| B (`top_k=1`) | **différent** de A |
| compteurs A | **6 appels · 12 experts · 96 canaux** |
| compteurs B | **6 appels · 6 experts · 48 canaux** |

Les briques **service (N3.2a) + profondeur (N3.2b0) + routage (N3.3a) + comptage (N3.3c)** tournent ensemble sur les mêmes modèles. Ce n’est pas encore la composition complète : le **seuil de confiance** (N3.2b) et le **pont/placement** n’y sont pas.

\## N3 — état

| brique | porte | état |
|---|---|---|
| service natif | `porte-n3-service` | ✅ |
| profondeur de service | `porte-n3-profondeur` | ✅ |
| routage/k-WTA | `porte-n3-routes` | ✅ |
| kwta/top_k séparés | `porte-n3-sparsite` | ✅ |
| comptage experts/canaux | `porte-n3-sparsite-compte` | ✅ |
| composition des briques | `porte-n3-composition` | ✅ N3.4a |
| seuil de confiance | — | ⏳ N3.2b |
| composition avec pont/placement | — | ⏳ |

**64 portes** : 60 vertes, 2 rouges structurelles.

\## A8.0 / A8.3

- **A8.0 : 10 portes PPL / 33**.
- **A8.3c** (session `c3d0f0bd`) : le lot n’est pas neutre (**1,90 %**) ; la non-monotonie du KV était un **effet de chemin**.
- **A8.3** reste opt-in.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 324 fiches · 396 JSON · 108 docs · 64 portes |
| `taille_documents.py` | ✅ **T0 3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 196 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 126 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`706020ee`) |

**Commits du round** : `04357861` (N3.3c, 63 portes), `706020ee` (N3.4a, 64 portes).

\## Goal

`goal-46eac0c4…` reste **actif** : N3.2a, N3.2b0, N3.3a/b/c et N3.4a sont faits ; il reste **N3.2b** (seuil de confiance) et la **composition avec pont/placement**. Prochain round : N3.2b, ou la onzième porte PPL.

### Tour 27 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [997 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Test fusion gate for 11th PPL pin
- bash — Test homeostasie gate for 11th PPL pin
- bash — Inspect fusion gate PPL reference
- bash — Capture fusion gate PPL
- bash — Pin fusion PPL and rerun
- bash — Write fusion pin report and state 11/33
- bash — Commit fusion PPL pin 11/33
- bash — Final checks for round 10

**Synthèse produite :**

⏵ Tour 10 bouclé : `porte-fusion` épingle sa PPL, A8.0 passe à 11/33

\## A8.0 — 11 portes PPL épinglées

Nouvelle porte `porte-fusion` :

| mesure | valeur |
|---|---:|
| PPL répartie f32 | **113,0068** |
| croisements fusionnés | **188** |
| divergence d’un bit | **détectée et attribuée** |
| trace v1 | **refusée** |

Tolérance **5e-4**, contrôle négatif à 10 %. La liste compte : flux, pont, topologie, coupe, réparti, budget, adaptateur, gain, cycle-c2, consolidation, fusion.

\## N3 — état

| brique | porte | état |
|---|---|---|
| service natif | `porte-n3-service` | ✅ N3.2a |
| profondeur de service | `porte-n3-profondeur` | ✅ N3.2b0 |
| routage/k-WTA | `porte-n3-routes` | ✅ N3.3a |
| kwta/top_k séparés | `porte-n3-sparsite` | ✅ N3.3b |
| comptage experts/canaux | `porte-n3-sparsite-compte` | ✅ N3.3c |
| composition des briques | `porte-n3-composition` | ✅ N3.4a |
| seuil de confiance | — | ⏳ N3.2b |
| composition avec pont/placement | — | ⏳ |

**64 portes** : 60 vertes, 2 rouges structurelles.

\## A8.3

- **A8.3c** : le lot n’est pas neutre (**1,90 %**) ; la non-monotonie du KV était un **effet de chemin**.
- **A8.3** reste **opt-in**.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 325 fiches · 397 JSON · 108 docs · 64 portes |
| `taille_documents.py` | ✅ **T0 3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 196 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 128 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`737af4ee`) |

**Commits du round** : `737af4ee` (fusion, 11/33), `706020ee` (N3.4a, 64 portes), `04357861` (N3.3c, 63 portes).

\## Goal

`goal-46eac0c4…` reste **actif** : N3.2a, N3.2b0, N3.3a/b/c et N3.4a sont faits ; il reste **N3.2b** (seuil de confiance) et la **composition avec pont/placement**. Prochain round : N3.2b, ou une douzième porte PPL.

### Tour 28 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [997 caractères tronqués]

*16 appels d'outils.* Actions notables :

- bash — Read current pas start for refactor
- bash — Add confidence-threshold generation and build
- bash — Add threshold params to native service and build
- bash — Test threshold service decision
- bash — Fix query parameter whitespace parsing and rebuild
- bash — Test threshold counts after parser fix
- bash — Find mixed threshold for confidence decision
- bash — Create and run N3.2b1 confidence threshold gate
- bash — Retry threshold gate on different port
- bash — Find leftover native service ports
- bash — Check inherited PORT variable
- bash — Test fixed port 67123 for service
- bash — Fix port range and run threshold gate
- bash — Write N3.2b1 threshold report and state
- … et 2 autres

**Synthèse produite :**

⏵ Tour 11 bouclé : le service décide par seuil de confiance et le compte (N3.2b1), porte 65

\## N3.2b1 — décision à seuil dans le service natif

Le service calcule, pour chaque jeton, le **chemin court** (profondeur 1) **et** le **chemin plein**, puis garde le jeton court si sa confiance (softmax max) atteint `seuil=`. Les deux caches sont entretenus ; ce n’est **pas encore** un saut de calcul, c’est la **décision**, et elle est comptée.

| seuil | choix anticipés | choix pleins | texte |
|---:|---:|---:|---|
| **0** | **12** | **0** | chemin court |
| **1** | **0** | **12** | chemin plein |
| **0,01** | **11** | **1** | mixte, **déterministe** |

- Seuils 0 et 1 : textes **différents**.
- Seuil 0,01 : stable sur deux appels ; le seuil **sépare** les jetons.
- **Limite nommée** : aucun saut de calcul (les deux chemins sont calculés). N3.2b2 (cache continu) reste ouvert.

\## N3 — état

| brique | porte | état |
|---|---|---|
| service natif | `porte-n3-service` | ✅ N3.2a |
| profondeur de service | `porte-n3-profondeur` | ✅ N3.2b0 |
| **seuil de confiance** | `porte-n3-seuil` | ✅ **N3.2b1** |
| routage/k-WTA | `porte-n3-routes` | ✅ N3.3a |
| kwta/top_k séparés | `porte-n3-sparsite` | ✅ N3.3b |
| comptage experts/canaux | `porte-n3-sparsite-compte` | ✅ N3.3c |
| composition des briques | `porte-n3-composition` | ✅ N3.4a |
| cache continu / vrai saut | — | ⏳ N3.2b2 |
| composition avec pont/placement | — | ⏳ |

**65 portes** : 61 vertes, 2 rouges structurelles.

\## A8.0 / A8.3

- **A8.0 : 11 portes PPL / 33** (dernière : fusion, 113,0068).
- **A8.3c** : le lot n’est pas neutre (**1,90 %**) ; la non-monotonie du KV était un effet de chemin.
- **A8.3** reste opt-in.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 326 fiches · 398 JSON · 108 docs · 65 portes |
| `taille_documents.py` | ✅ **T0 3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 196 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 129 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`bacf43d2`) |

**Commits du round** : `bacf43d2` (N3.2b1, 65 portes), `737af4ee` (fusion, A8.0 11/33).

\## Goal

`goal-46eac0c4…` reste **actif** : N3.2a, N3.2b0, N3.2b1, N3.3a/b/c et N3.4a sont faits ; il reste **N3.2b2** (cache continu pour un vrai saut de calcul) et la **composition avec pont/placement**. Prochain round : N3.2b2, ou une douzième porte PPL.

### Tour 29 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [997 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Create and run N3.2b2 depth/cache condition gate
- bash — Fix gen args and run N3.2b2 gate
- bash — Write N3.2b2 condition report and state
- bash — Commit N3.2b2 cache condition
- bash — Create and run N3.4b native bridge gate
- bash — Write N3.4b bridge report and state
- bash — Commit N3.4b native bridge gate
- bash — Final checks for round 12

**Synthèse produite :**

⏵ Tour 12 bouclé : N3.2b2 nomme la condition K/V, N3.4b branche le pont natif ; 67 portes

\## N3.2b2 — le saut de calcul n’est pas gratuit

| régime | temps médian | déterministe | sortie |
|---|---:|---|---|
| plein (8 blocs) | **5,2 ms** | oui | référence |
| profondeur 1 | **2,0 ms** | oui | **différente** |

La profondeur 1 est **2,6× plus rapide** et **change la génération**. Les couches sautées ne fournissent plus leurs **K/V** aux jetons suivants : un cache continu ne peut pas les récupérer sans les calculer. Trois issues, aucune gratuite — recalculer (aucun gain), stocker tous les K/V (aucun gain), accepter un modèle tronqué (sortie différente). **N3.2b2 est une condition nommée**, pas un patch de cache.

\## N3.4b — le pont natif agit

Deux DRVM de **mêmes poids** (graine 7, 428 504 paramètres, 4 blocs) ; B a `bridge.weight`/`bridge.bias` mis à zéro (**4 160** poids).

| contrôle | résultat |
|---|---|
| A deux fois | **identique** (35 octets) |
| A contre B (pont nul) | **différent** |
| paramètres A / B | **428 504 / 428 504** |

Le pont du modèle natif est branché ; ce n’est pas le lien distribué de `porte-pont` (Qwen).

\## N3 — état

| brique | porte | état |
|---|---|---|
| service, profondeur, seuil | N3.2a / N3.2b0 / N3.2b1 | ✅ |
| condition K/V | `porte-n3-cache` | ✅ N3.2b2 |
| routage, sparsité, comptage | N3.3a/b/c | ✅ |
| composition des briques | `porte-n3-composition` | ✅ N3.4a |
| pont natif | `porte-n3-pont` | ✅ N3.4b |
| placement / composition complète | — | ⏳ N3.4c |

**67 portes** : 63 vertes, 2 rouges structurelles.

\## A8.0 / A8.3

- **A8.0 : 11 portes PPL / 33** (fusion, 113,0068).
- **A8.3c** : le lot n’est pas neutre (**1,90 %**) ; **A8.3** reste opt-in.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 328 fiches · 400 JSON · 108 docs · 67 portes |
| `taille_documents.py` | ✅ **T0 3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 196 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 131 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`f84d4f29`) |

**Commits du round** : `51a3dc91` (N3.2b2, 66 portes), `f84d4f29` (N3.4b, 67 portes), `bacf43d2` (N3.2b1, 65 portes).

\## Goal

`goal-46eac0c4…` reste **actif** : N3.2a, N3.2b0, N3.2b1, N3.2b2, N3.3a/b/c, N3.4a et N3.4b sont faits ; il reste le **placement** (N3.4c) et une **composition complète**. Prochain round : N3.4c, ou une douzième porte PPL.

### Tour 30 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [997 caractères tronqués]

*7 appels d'outils.* Actions notables :

- bash — Test porte-trace for 12th PPL pin
- bash — Inspect trace gate PPL output
- bash — Pin trace PPL and rerun
- bash — Pin trace PPL 59.0790 and rerun
- bash — Write trace pin report and state 12/33
- bash — Commit trace PPL pin 12/33
- bash — Final checks for round 13

**Synthèse produite :**

⏵ Tour 13 bouclé : `porte-trace` épingle sa PPL, A8.0 passe à 12/33

\## A8.0 — 12 portes PPL épinglées

Nouvelle porte `porte-trace` :

| mesure | valeur |
|---|---:|
| PPL répartie f32 | **59,0790** |
| croisements enregistrés | **126** |
| rejeu | **identique** |
| trace fausse d’un bit | **détectée et nommée** |

Tolérance **5e-4**, contrôle négatif à 10 %. La liste compte : flux, pont, topologie, coupe, réparti, budget, adaptateur, gain, cycle-c2, consolidation, fusion, trace.

\## N3 — état

| brique | porte | état |
|---|---|---|
| service, profondeur, seuil | N3.2a / N3.2b0 / N3.2b1 | ✅ |
| condition K/V | `porte-n3-cache` | ✅ N3.2b2 |
| routage, sparsité, comptage | N3.3a/b/c | ✅ |
| composition des briques | `porte-n3-composition` | ✅ N3.4a |
| pont natif | `porte-n3-pont` | ✅ N3.4b |
| placement / composition complète | — | ⏳ N3.4c |

**67 portes** : 63 vertes, 2 rouges structurelles.

\## A8.3

- **A8.3c** : le lot n’est pas neutre (**1,90 %**) ; la non-monotonie du KV était un effet de chemin.
- **A8.3** reste opt-in.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 329 fiches · 401 JSON · 108 docs · 67 portes |
| `taille_documents.py` | ✅ **T0 3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 196 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 133 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`c1a9c37b`) |

**Commits du round** : `c1a9c37b` (trace, 12/33), `f84d4f29` (N3.4b, 67 portes), `51a3dc91` (N3.2b2, 66 portes).

\## Goal

`goal-46eac0c4…` reste **actif** : N3.2a/b0/b1/b2, N3.3a/b/c, N3.4a/b sont faits ; il reste le **placement** (N3.4c) et une **composition complète**. Prochain round : N3.4c, ou une treizième porte PPL.

### Tour 31 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [997 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Inspect reflexe null adapter PPL
- bash — Pin reflexe truncated PPL and rerun
- bash — Write reflexe pin report and state 13/33
- bash — Commit reflexe PPL pin 13/33
- bash — Final checks for round 14

**Synthèse produite :**

⏵ Tour 14 bouclé : `porte-reflexe` épingle sa PPL tronquée, A8.0 passe à 13/33

\## A8.0 — 13 portes PPL épinglées

Nouvelle porte `porte-reflexe` :

| mesure | valeur |
|---|---:|
| PPL tronquée 8 couches, adaptateur nul | **11 163 272,0495** |
| adaptateur nul contre référence | **identique** |
| accord à 16 couches | **25,4 %** (référence 4,8 %) |
| cos(état 16 couches, état final) | **0,145** |

Tolérance **5e-4**, contrôle négatif à 10 %. La liste compte : flux, pont, topologie, coupe, réparti, budget, adaptateur, gain, cycle-c2, consolidation, fusion, trace, réflexe.

\## N3 — état

| brique | porte | état |
|---|---|---|
| service, profondeur, seuil | N3.2a / N3.2b0 / N3.2b1 | ✅ |
| condition K/V | `porte-n3-cache` | ✅ N3.2b2 |
| routage, sparsité, comptage | N3.3a/b/c | ✅ |
| composition des briques | `porte-n3-composition` | ✅ N3.4a |
| pont natif | `porte-n3-pont` | ✅ N3.4b |
| placement / composition complète | — | ⏳ N3.4c |

**67 portes** : 63 vertes, 2 rouges structurelles.

\## A8.3

- **A8.3c** : le lot n’est pas neutre (**1,90 %**) ; la non-monotonie du KV était un effet de chemin.
- **A8.3** reste opt-in.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 330 fiches · 402 JSON · 108 docs · 67 portes |
| `taille_documents.py` | ✅ **T0 3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 196 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 135 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`a0324368`) |

**Commits du round** : `a0324368` (réflexe, 13/33), `c1a9c37b` (trace, 12/33), `f84d4f29` (N3.4b, 67 portes).

\## Goal

`goal-46eac0c4…` reste **actif** : N3.2a/b0/b1/b2, N3.3a/b/c, N3.4a/b sont faits ; il reste le **placement** (N3.4c) et une **composition complète**. Prochain round : N3.4c, ou une quatorzième porte PPL.

### Tour 32 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [997 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Inspect DRVM read/write API for placement
- bash — Create and run N3.4c native placement condition gate
- bash — Write N3.4c placement condition report and state
- bash — Commit N3.4c placement condition gate
- bash — Final checks for round 15

**Synthèse produite :**

⏵ Tour 15 bouclé : N3.4c montre que le placement natif est une métadonnée, pas un chemin ; porte 68

\## N3.4c — le placement natif est une métadonnée

Deux DRVM de **mêmes poids** (graine 7, 428 504 paramètres, 4 blocs), l’un `placement=local`, l’autre `placement=remote` :

| contrôle | résultat |
|---|---|
| A (`local`) deux fois | **identique** (35 octets) |
| A contre B (`remote`) | **identique** |
| A contre C (pont nul) | **différent** |
| paramètres | **428 504** |

Le placement ne change **rien** ; le pont nul, lui, change la sortie. Le champ est une **métadonnée inerte** dans le service natif. Le placement distribué du moteur GGUF reste couvert par `porte-topologie` ; un chemin **natif** distribué n’existe pas.

\## N3 — couverture par brique

| brique | porte | état |
|---|---|---|
| service, profondeur, seuil | N3.2a / N3.2b0 / N3.2b1 | ✅ |
| condition K/V | N3.2b2 | ✅ |
| routage, sparsité, comptage | N3.3a/b/c | ✅ |
| composition des briques | N3.4a | ✅ |
| pont natif | N3.4b | ✅ |
| placement natif | N3.4c | ⛔ métadonnée |
| composition **complète** native | — | ⏳ (placement distribué absent) |

**68 portes** : 64 vertes, 2 rouges structurelles.

\## A8.0 / A8.3

- **A8.0 : 13 portes PPL / 33** (dernière : réflexe, 11 163 272,0495 ; trace, 59,0790).
- **A8.3c** : le lot n’est pas neutre (**1,90 %**) ; **A8.3** reste opt-in.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 331 fiches · 403 JSON · 108 docs · 68 portes |
| `taille_documents.py` | ✅ **T0 3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 196 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 136 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`5bed145a`) |

**Commits du round** : `5bed145a` (N3.4c, 68 portes), `a0324368` (réflexe, 13/33), `c1a9c37b` (trace, 12/33).

\## Goal

`goal-46eac0c4…` reste **actif** : la couverture N3 par brique est faite ; il reste une **composition complète native** (qui demanderait un placement distribué natif) et éventuellement une quatorzième porte PPL. Prochain round : soit tenter ce chemin distribué, soit poursuivre A8.0.

### Tour 33 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [997 caractères tronqués]

*7 appels d'outils.* Actions notables :

- bash — Inspect infrastructure gates for PPL pin
- bash — Test c4 retard gate for 14th PPL pin
- bash — Read c4 retard variables for pins
- bash — Pin c4-retard PPL and rerun
- bash — Write c4 pin report and state 14/33
- bash — Commit c4-retard PPL pin 14/33
- bash — Final checks for round 16

**Synthèse produite :**

⏵ Tour 16 bouclé : `porte-c4-retard` épingle cinq PPL, A8.0 passe à 14/33

\## A8.0 — 14 portes PPL épinglées

Nouvelle porte `porte-c4-retard` :

| mesure | PPL |
|---|---:|
| modèle entier | **14,6496** |
| retard 0 | **14,6496** |
| retard 1 | **9 277,9771** (×633) |
| retard 8 | **151 517,0001** (×10 343) |
| état manquant | **15,5295** (×1,06) |

Tolérance **5e-4**, contrôle négatif à 10 %. La liste compte : flux, pont, topologie, coupe, réparti, budget, adaptateur, gain, cycle-c2, consolidation, fusion, trace, réflexe, c4-retard.

\## N3 — couverture

| brique | porte | état |
|---|---|---|
| service, profondeur, seuil | N3.2a / N3.2b0 / N3.2b1 | ✅ |
| condition K/V | N3.2b2 | ✅ |
| routage, sparsité, comptage | N3.3a/b/c | ✅ |
| composition, pont | N3.4a / N3.4b | ✅ |
| placement natif | `porte-n3-placement` | ⛔ métadonnée |
| composition **complète** native | — | ⏳ |

**68 portes** : 64 vertes, 2 rouges structurelles.

\## A8.3

- **A8.3c** : le lot n’est pas neutre (**1,90 %**) ; **A8.3** reste opt-in.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 332 fiches · 404 JSON · 108 docs · 68 portes |
| `taille_documents.py` | ✅ **T0 3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 196 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 138 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`0c6bea37`) |

**Commits du round** : `0c6bea37` (c4-retard, 14/33), `5bed145a` (N3.4c, 68 portes).

\## Goal

`goal-46eac0c4…` reste **actif** : N3 est couvert par brique ; il reste une **composition complète native** (placement distribué absent) et éventuellement une quinzième porte PPL. Prochain round : tenter le chemin distribué natif, ou poursuivre A8.0.

### Tour 34 — <goal_round> Objective: "Drave — deuxième cycle d'autonomie multi-programmes (>3 h) : (1) A8.0/A8.3b — épingler les port … [997 caractères tronqués]

*7 appels d'outils.* Actions notables :

- bash — Test pannes gate for 15th PPL pin
- bash — Test bus gate for 15th PPL pin
- bash — Write N3 coverage report and update state
- bash — Commit N3 coverage report
- bash — Final checks before closing the goal
- get_goal
- update_goal

**Synthèse produite :**

⏵ Goal complete : 17 rounds d’autonomie, 68 portes, état vert

\## Résultat

Le goal `goal-46eac0c4…` est **terminé** (17 rounds, `max_goal_rounds` 1000). Le cycle a produit des mesures, des fiches, des JSON, des commits et un état à jour, sans écraser les sessions actives.

\## A8.0 / A8.3

**A8.0 — 14 portes PPL épinglées sur 33** :

| porte | référence |
|---|---|
| flux | 61,9920 / 60,8135 |
| pont | 113,0068 / 111,9225 |
| topologie | 17,4702 / 30,4363 / 42,5477 |
| coupe | 113,0068 |
| réparti | 9,1748 |
| budget | 111,9225 |
| adaptateur | 17,4315 / 2 687 292,8165 |
| gain | 14,6496 / 12,9635 / 996,0390 |
| cycle-c2 | 14,6496 |
| consolidation | 17,4268 / 17,1655 |
| fusion | 113,0068 |
| trace | 59,0790 |
| réflexe | 11 163 272,0495 |
| c4-retard | 14,6496 / 9 277,9771 / 151 517,0001 / 15,5295 |

- **A8.3b.1** : le signe du mélange 1 % vient du **chemin lot** — lot 1 : 61,9920/58,3200 ; lot ≥ 2 : 60,8135/62,7357 ; la taille de lot au-delà de 2 ne compte pas.
- **A8.3c** (session `c3d0f0bd`) : le lot n’est pas neutre (**1,90 %**) ; la non-monotonie du KV était un effet de chemin. **A8.3 reste opt-in.**
- **A8.3a** : régimes f32/1 % épinglés pour flux, pont et coupe.

\## N3 — couverture par brique

| brique | porte | état |
|---|---|---|
| service natif | `porte-n3-service` | ✅ |
| profondeur + lecture HTTP | `porte-n3-profondeur` | ✅ (défaut HTTP corrigé) |
| seuil de confiance | `porte-n3-seuil` | ✅ 12/0, 0/12, 11/1 ; **sans saut de calcul** |
| condition K/V | `porte-n3-cache` | ⛔ 5,2 → 2,0 ms, sortie différente |
| routage, sparsité, comptage | `porte-n3-routes`, `-sparsite`, `-sparsite-compte` | ✅ |
| composition | `porte-n3-composition` | ✅ |
| pont natif | `porte-n3-pont` | ✅ |
| placement natif | `porte-n3-placement` | ⛔ métadonnée inerte |
| couverture | `N3.4d` | ✅ par brique |

**Limite nommée** : une composition native **unique** avec placement demanderait un chemin distribué natif qui n’existe pas. C’est une condition d’architecture, pas une porte manquante.

\## R13 / A2.6 / B11.10

- **R13.0** : BPE **3,4–5,2 octets/jeton** sur le latin, 2,8 arabe/cyrillique, 4,6 CJK ; contrôle aléatoire **1,63** ; réversible.
- **R13.1** : condition nommée — le natif est en **octets** (`vocab = 256`), aucun checkpoint BPE natif ; la PPL BPE-native exige une campagne (tokenizer abstrait + modèle BPE natif).
- **A2.6** : partielle — générique/KV faits, tête 4 bits refusée, experts bloqués par **A6.2**.
- **B11.10** : codec **161/161**, ambiguïtés refusées,
… [1465 caractères tronqués]

### Tour 35 — tu as 9h d'autonomie devant toi, que vas-tu faire

*28 appels d'outils.* Actions notables :

- bash — Audit current state before 9h plan
- create_goal
- todo_write
- bash — Locate A8.0 state lines for reconciliation
- bash — Reconcile A8.0 count and commit state
- get_goal
- bash — Read goal and inspect bus gate
- update_goal
- bash — Read bus PPL variables
- bash — Read bus section2 PPL
- bash — Pin bus PPL and rerun
- bash — Write bus pin report and state 15/33
- bash — Commit bus PPL pin 15/33
- bash — Run delais gate to capture PPL
- … et 13 autres

**Synthèse produite :**

⏵ Cycle 8 h lancé : A8.0 déjà à 16/33, état vert, je continue sans intervention

\## Déjà fait dans ce cycle

- **A8.0 `porte-bus` épinglée** (commit `30a0c341`) : **64,1160** (bus gain 1,5), **59,0790** (relais/file sans canal), **66,0379** (avec canal), 5e-4, contrôle 10 %.
- **A8.0 `porte-delais` épinglée** (commit `c946296e`) : **59,0790** à 0 et 50 ms ; empreintes identiques, temps 7,24 → 10,43 s.
- **État réconcilié** (`3c517fb2`) : `en-cours` disait 8 portes, les fiches en établissaient 14 ; il dit maintenant **16**.
- **T1 réparé** (`fa20b2ae`) : le bloc de passe dupliqué dans `references-non-regression.md` dépassait 2 500 mots ; retiré.

**A8.0 : 16 portes PPL sur 33.** Vérifications : 335 fiches · 407 JSON · 108 docs · 68 portes ; T0 **3 997/4 000** ; en-cours 1 195 mots ; 1 143 liens ; 22 SVG ; état `c946296e`.

\## La suite, plus ambitieuse que l’estimation initiale

1. **A8.0 — finir les portes mesurables** : `porte-bus-socket` (113,0068 → 148,9144), `porte-profondeur-routee`, puis qualifier les rouges au lieu de les contourner.
2. **A8.3b/c — le vrai sujet** : balayage **lot × ctx × cache** (lot 1/2/4, ctx 64/256/512, KV f32/1 %) pour savoir si le signe vient du chemin de lot ou de l’occupation ; décision de défaut ensuite.
3. **N3 — le prototype distribué** : deux processus natifs, transfert d’état, comparaison au local plein ; porte `porte-n3-distribue`. Si le prototype ne tient pas, condition nommée, pas de vert de complaisance.
4. **R13.1 — le BPE natif** : tokenizer 512–1 024 jetons, petit `drave-n0` BPE, bits/octet contre octets ; porte et décision.
5. **B11.10 — la suite cartes** : hybride/natif au-delà des 69,3 %, si le corpus le permet.
6. **Clôture** : toutes les portes, fiches, commits, état, goal complet ou conditions nommées.

Je ne vais pas m’arrêter à 2 h 30 : la liste ci-dessus est le plancher, pas le plafond. Prochain round : `porte-bus-socket`, puis le balayage A8.3b/c. Le goal reste **actif** ; je continue jusqu’à 8 h ou jusqu’à ce qu’un blocage externe nommé apparaisse.

### Tour 36 — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initi … [1076 caractères tronqués]

*9 appels d'outils.* Actions notables :

- bash — Run bus-socket gate for A8.0 pin
- bash — Inspect bus-socket PPL variables
- bash — Read bus-socket insertion points
- bash — Pin bus-socket PPL and rerun
- bash — Write and commit bus-socket pin 17/33
- bash — Sweep lot and ctx under f32 and 1 percent
- bash — Write ctx sweep report and state
- bash — Commit ctx sweep A8.3c.1
- bash — Checkpoint after A8.0 and ctx results

**Synthèse produite :**

⏵ Point d’étape : A8.0 à 17/33, le signe du mélange n’est pas un effet de cache

\## Résultats du round

**A8.0 — trois portes de plus, 17/33 :**

| porte | références épinglées |
|---|---|
| `porte-bus` | **64,1160** / **59,0790** / **66,0379** |
| `porte-delais` | **59,0790** à 0 et 50 ms ; temps 7,24 → 10,43 s |
| `porte-bus-socket` | **113,0068** / **148,7080** / **42,3176** / **148,9144** |

Chaque pin a son contrôle négatif à 10 %, sa fiche et son JSON. Commits : `30a0c341`, `c946296e`, `36aa6bd5`.

**A8.3c.1 — le cache n’est pas la cause.** Balayage **24 exécutions** : ctx 64, 256, 512 × lot 0/1/2/4 × f32/1 %.

| régime | ctx | lot 0/1 | lot 2/4 |
|---|---:|---:|---:|
| f32 | 64/256/512 | **61,9920** | **60,8135** |
| 1 % | 64/256/512 | **58,3200** | **62,7357** |

**Aucune ligne ne bouge avec ctx.** Le basculement est le **chemin lot** (lot 1 contre lot ≥ 2), pas la capacité du cache KV. A8.3 reste **opt-in** ; le prochain pas est le code du chemin lot, pas la taille du cache. Commit `e220336a`.

**T1 réparé** : le bloc de passe dupliqué de `references-non-regression.md` dépassait 2 500 mots ; retiré (`fa20b2ae`).

\## État vérifié

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 337 fiches · 409 JSON · 108 docs · 68 portes |
| `taille_documents.py` | ✅ **T0 3 999 / 4 000** ; en-cours 1 197 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 197 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 146 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`e220336a`) |

\## La suite immédiate

1. **N3 distribué** : prototype natif à deux processus, transfert d’état, porte `porte-n3-distribue` ; si le prototype ne tient pas, condition nommée.
2. **R13.1 BPE natif** : tokenizer 512–1 024 jetons, petit `drave-n0` BPE, bits/octet contre octets.
3. **B11.10** : suite native/hybride des cartes.
4. **A8.0** : `porte-profondeur-routee` et qualification des rouges.

Le goal reste **actif** ; je continue jusqu’à 8 h.

### Tour 37 — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initi … [1076 caractères tronqués]

*11 appels d'outils.* Actions notables :

- sous-agent — Design N3 native two-process split
- sous-agent — Assess BPE-native R13.1 feasibility
- bash — Locate pannes error message and gate check
- bash — Read pannes check and error paths
- bash — Read pair connection context for error fields
- bash — Find region/pas variables in reparti function
- bash — Name region and step in pair-absent panic path
- bash — Rerun pannes gate after message fix
- bash — Write and commit pannes fix report
- list_agents
- bash — Final checks after pannes fix

**Synthèse produite :**

⏵ Round 2 : A8.0 à 17/33, le cache innocenté, `porte-pannes` passée au vert

\## A8.0 — 17 portes PPL sur 33

| porte | références épinglées |
|---|---|
| `porte-bus` | **64,1160** / **59,0790** / **66,0379** |
| `porte-delais` | **59,0790** à 0 et 50 ms ; 7,24 → 10,43 s |
| `porte-bus-socket` | **113,0068** / **148,7080** / **42,3176** / **148,9144** |

Commits : `30a0c341`, `c946296e`, `36aa6bd5`.

\## A8.3c.1 — le cache n’est pas la cause

**24 exécutions** : ctx 64, 256, 512 × lot 0/1/2/4 × f32/1 %.

| régime | ctx | lot 0/1 | lot 2/4 |
|---|---:|---:|---:|
| f32 | 64/256/512 | **61,9920** | **60,8135** |
| 1 % | 64/256/512 | **58,3200** | **62,7357** |

Aucune ligne ne bouge avec ctx. Le basculement est le **chemin lot** (lot 1 contre lot ≥ 2), pas la capacité du cache KV. A8.3 reste **opt-in** ; le prochain pas est le code du chemin lot. Commit `e220336a`.

\## C11 — `porte-pannes` est verte

Le chemin « pair absent » nommait l’adresse, pas la région, et ne disait ni le pas ni les octets. Corrigé :

- pair tué : **région d**, **pas 95**, **349 980 octets**, code **7** ;
- pair absent : **région d**, **pas 0**, **0 octet**, code **7** en **2 s** ;
- nominal : PPL 33,0156.

La porte sort **verte**, sans résultat partiel. Commit `7a46498b`.

\## État vérifié

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 338 fiches · 410 JSON · 108 docs · 68 portes |
| `taille_documents.py` | ✅ **T0 4 000 / 4 000** ; en-cours 1 198 / 2 000 |
| `verifie_en_cours.py` | ✅ 1 198 mots · 7 puces · 3 sessions |
| `porte-tableaux.sh` | ✅ 1 147 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`7a46498b`) |

\## En cours

Deux sous-agents analysent en parallèle :

- **N3 distribué** : plus petit refactor Rust pour deux régions, transfert d’état, porte de composition ;
- **R13.1 BPE natif** : faisabilité tokenizer/modèle BPE et chemin bits/octet.

Prochain round : intégrer leur plan, puis soit le prototype N3, soit le tokenizer BPE. Le goal reste **actif**.

### Tour 38 — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initi … [1076 caractères tronqués]

*60 appels d'outils.* Actions notables :

- list_agents
- bash — Run routed-depth gate in background
- bash — Locate lot path code in model
- bash — Inspect lot path KV/cache behavior
- bash — Search lot path for KV precision use
- job_output
- bash — Read B11.10 report/backlog for next step
- bash — Check native trainer and BPE packages
- bash — Read native trainer data path
- bash — Train a 512 BPE tokenizer on French corpus
- bash — Check GPU availability for BPE training
- bash — Create token-based native trainer
- bash — Create tokenizer script and test stats
- bash — Retry tokenizer with output directory
- … et 40 autres

**Synthèse produite :**

⏵ Round 3 : A8.0 à 18/33, N3.5a bit-exact, R13.1 corrigé à 11,0 % — tout est vert

\## A8.0 — 18 portes PPL sur 33

| porte | références épinglées |
|---|---|
| `porte-bus` | **64,1160** / **59,0790** / **66,0379** |
| `porte-delais` | **59,0790** à 0 et 50 ms |
| `porte-bus-socket` | **113,0068** / **148,7080** / **42,3176** / **148,9144** |
| `porte-profondeur-routee` | **14,6496** pleine profondeur ; oracle 30,93 / 51,92 |

Commits : `30a0c341`, `c946296e`, `36aa6bd5`, `8b9608f0`.

\## N3.5a — le découpage 0..k / k..n est bit-exact

- `Native::entree` / `traverser` / `tete`, `pas_amont` / `pas_aval`.
- Test unitaire `split_amont_aval_egal_pas` **vert**.
- Balayage **K = 0,1,2,3,4** et deux prompts : sortie **identique au modèle plein**.
- **Deux bugs latents corrigés** : pont `n_blocks=1` (sous-débordement `usize`) et `max_pos` codé en dur (fixture 32 positions).
- CLI `--drvm-generate-split` et `--drvm-generate-hex`.
- Commit `6eca9a15`, porte 70.

\## C11 — `porte-pannes` verte

Le pair absent nomme maintenant **région d**, **pas 0**, **0 octet**, code **7** en **2 s** ; le pair tué nomme **pas 95 / 349 980 octets**. Commit `7a46498b`.

\## R13.1 — le BPE natif gagne, chiffre corrigé

- Mesure initiale : **3,249** contre **3,689** bits/octet, soit **−11,9 %**.
- **Audit indépendant** : le ratio global était biaisé ; la tranche de validation donne **3,2823**, soit **−11,0 %** exact. Le pilote indépendant à 1 500 pas trouve **−17,0 %** (sous-entraîné, non comparable).
- Limites ajoutées : tokenizer entraîné sur le corpus entier (fuite de validation), contexte BPE 2×, +5,4 % de paramètres, 200/400 pas, 8 192 jetons de val.
- Commit de correction `2a653d12`.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 341 fiches · 413 JSON · 108 docs · 70 portes |
| `taille_documents.py` | ✅ **T0 3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `porte-tableaux.sh` | ✅ 1 151 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`2a653d12`) |

\## Ensuite

1. **N3.5b** : deux processus, transfert TCP du hidden de frontière, refus d’empreinte/K/position.
2. **R13.1 campagne** : 10 k pas, train/val séparés, bytes/512/1024, bits/octet exact.
3. **B11.10** : suite native/hybride des cartes.
4. **A8.0** : rouges structurelles et portes restantes.

Le goal reste **actif** ; je continue.

### Tour 39 — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initi … [1076 caractères tronqués]

*9 appels d'outils.* Actions notables :

- bash — Add file-based two-process split CLI and build
- bash — Create and run two-process file split gate
- bash — Debug file split for 1/2/3 positions
- bash — Inspect model d and split file header
- bash — Fix usize header width in split file
- bash — Rerun two-process file split after header fix
- bash — Write N3.5b report and update state
- bash — Commit N3.5b two-process prototype
- bash — Checkpoint after N3.5b

**Synthèse produite :**

⏵ Round 4 : A8.0 à 18/33, N3.5a/N3.5b bit-exacts, R13.1 corrigé — 71 portes

\## A8.0 — 18 portes PPL sur 33

- `porte-bus` : **64,1160 / 59,0790 / 66,0379**
- `porte-delais` : **59,0790** à 0 et 50 ms
- `porte-bus-socket` : **113,0068 / 148,7080 / 42,3176 / 148,9144**
- `porte-profondeur-routee` : **14,6496** pleine profondeur ; oracle 30,93 / 51,92

Commits `30a0c341`, `c946296e`, `36aa6bd5`, `8b9608f0`.

\## N3.5a/N3.5b — le découpage natif est bit-exact

- **N3.5a** : `pas_amont`/`pas_aval`, K=0..4, deux prompts, sortie **identique au modèle plein** ; test unitaire vert ; deux bugs latents corrigés (pont `n_blocks=1`, `max_pos`).
- **N3.5b** : deux **processus séparés**, frontière par fichier, logits **bit-à-bit identiques** pour K=0..4 et `abc`/`zzz`.
- **Bug trouvé** : l’en-tête écrivait `d` en `usize` (8 octets) et le relisait en `u32` (4), décalant tous les hiddens ; corrigé.
- Portes 70 et 71 ; commits `6eca9a15`, `d8498639`.

\## R13.1 — correction d’audit

Le chiffre publié **−11,9 %** utilisait le ratio global ; la tranche de validation donne **3,2823** contre **3,689**, soit **−11,0 %** exact. Limites ajoutées : fuite du tokenizer, contexte 2×, +5,4 % de paramètres, 200/400 pas. Un pilote indépendant à 1 500 pas trouve **−17,0 %** (même direction, sous-entraîné). Commit `2a653d12`.

\## C11 — `porte-pannes` verte

Pair absent : **région d, pas 0, 0 octet, code 7, 2 s** ; pair tué : **pas 95, 349 980 octets**. Commit `7a46498b`.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 342 fiches · 414 JSON · 108 docs · 71 portes |
| `taille_documents.py` | ✅ **T0 3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `porte-tableaux.sh` | ✅ 1 152 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`d8498639`) |

\## Ensuite

1. **N3.5c** : TCP localhost, refus d’empreinte/K/position, deux processus en réseau.
2. **R13.1 campagne** : 10 k pas, train/val séparés, bytes/512/1024, bits/octet exact.
3. **B11.10** : suite native/hybride des cartes.
4. **A8.0** : rouges structurelles et portes restantes.

Le goal reste **actif** ; je continue.

### Tour 40 — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initi … [1076 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Add TCP split server/client and build
- bash — Create and run N3.5c TCP split gate
- bash — Send k in TCP header and use it
- bash — Rerun N3.5c TCP gate with k header
- bash — Write and commit N3.5c TCP result
- bash — Checkpoint after N3.5c

**Synthèse produite :**

⏵ Round 5 : N3.5c passe au TCP, deux processus bit-exacts, 72 portes

\## N3.5c — le découpage passe le réseau

Deux processus **TCP localhost** : l’amont envoie `n, d, k` puis les hiddens de frontière ; l’aval calcule `k..n`, applique la tête et rend les logits. **Aucun cache K/V ne traverse le fil.**

| K | logits |
|---:|---|
| 0 | identiques au `pas` plein |
| 1 | identiques |
| 2 | identiques |
| 3 | identiques |
| 4 | identiques |

Prompts `abc` et `zzz` ; comparaison **bit-à-bit**. Le premier essai échouait parce que le serveur utilisait **son** K, pas celui du client ; K est maintenant dans l’en-tête. Commit `89bb7ef8`.

**Limites nommées** : localhost seulement, pas d’auth/TLS, un seul forward (pas encore une boucle de génération avec sessions), les deux processus chargent tous les poids.

\## N3 — chaîne complète

| étape | état |
|---|---|
| N3.5a découpage 0..k / k..n en un processus | ✅ bit-exact |
| N3.5b deux processus, frontière fichier | ✅ bit-exact |
| N3.5c deux processus, frontière TCP | ✅ bit-exact |
| N3.5d sessions/refus/génération | ⏳ |

\## A8.0 — 18 portes PPL / 33

- bus : **64,1160 / 59,0790 / 66,0379**
- délais : **59,0790** (0 et 50 ms)
- bus-socket : **113,0068 / 148,7080 / 42,3176 / 148,9144**
- profondeur-routee : **14,6496**, oracle 30,93 / 51,92
- **C11 `porte-pannes` verte** : la panne nomme région, pas et octets.

\## R13.1

Correction d’audit : **3,2823** contre **3,689** bits/octet, **−11,0 %** exact sur la validation (le 11,9 % utilisait le ratio global). Limites documentées : fuite du tokenizer, contexte 2×, +5,4 % de paramètres. Commit `2a653d12`.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 343 fiches · 415 JSON · 108 docs · 72 portes |
| `taille_documents.py` | ✅ **T0 3 998 / 4 000** ; en-cours 1 196 / 2 000 |
| `porte-tableaux.sh` | ✅ 1 153 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`89bb7ef8`) |

\## Ensuite

1. **N3.5d** : sessions, refus d’empreinte/K/position, boucle de génération.
2. **B11.10** : suite native/hybride des cartes.
3. **A8.3b/c** : décision de défaut documentée (opt-in maintenu).
4. **A8.0** : rouges structurelles et portes restantes.

Le goal reste **actif** ; je continue.

### Tour 41 — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initi … [1076 caractères tronqués]

*10 appels d'outils.* Actions notables :

- bash — Write and commit A8.3b/c decision
- bash — Find B11.10 card corpus and API
- bash — Inspect B11.10 corpus JSON
- bash — Read card items
- bash — Find card corpus source
- bash — Inspect games corpus for cards
- bash — Find corpus builder and lit API
- bash — Read lit API and Lecture fields
- bash — Scan all card items for ambiguity and exactness
- bash — Checkpoint after A8.3 decision

**Synthèse produite :**

⏵ Round 6 : N3.5c TCP bit-exact, A8.3b/c décidé (opt-in), 72 portes

\## N3.5b/N3.5c — deux processus, fichier puis TCP

- **N3.5b** : deux processus séparés, frontière par fichier ; logits **bit-à-bit identiques** pour K=0..4 et `abc`/`zzz`. Bug d’en-tête `usize`/`u32` trouvé et corrigé.
- **N3.5c** : deux processus **TCP localhost** ; l’amont envoie `n, d, k` + hiddens, l’aval rend les logits ; **aucun cache K/V sur le fil**. K=0..4 et deux prompts identiques au `pas` plein.
- Premier échec TCP : le serveur utilisait **son** K, pas celui du client ; K est passé dans l’en-tête.
- Portes 71 et 72, commits `d8498639`, `89bb7ef8`.

\## A8.3b/c — décision : opt-in, cause = chemin lot

| régime | lot 1 | lot 2 | lot 4 |
|---|---:|---:|---:|
| f32 | **61,9920** | **60,8135** | **60,8135** |
| 1 % | **58,3200** | **62,7357** | **62,7357** |

- **Ctx 64/256/512** : 24 exécutions, aucune ligne ne bouge → **le cache n’est pas la cause**.
- **Lot 1 = pas de lot** ; lot ≥ 2 identique ; le signe bascule avec le **chemin lot binaire**.
- **Défaut refusé** : 18 portes épinglées, seulement 3 ont un régime 1 % dual ; un défaut déplacerait les 15 autres.
- Condition pour passer : instrumenter `forward_lot`, donner un régime dual aux 18 portes, rejouer.
- Commit `ccdda6b5`.

\## A8.0 — 18 portes PPL / 33

bus, délais, bus-socket, profondeur-routee sont épinglées ; **C11 `porte-pannes` est verte** (région, pas, octets). Restent surtout les rouges structurelles (`porte-indice`, `porte-melange`) et les portes sans PPL.

\## R13.1

Correction d’audit : **3,2823** contre **3,689** bits/octet, **−11,0 %** exact sur la validation. Le 11,9 % venait du ratio global. Commit `2a653d12`.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 344 fiches · 416 JSON · 108 docs · 72 portes |
| `taille_documents.py` | ✅ **T0 3 999 / 4 000** ; en-cours 1 197 / 2 000 |
| `porte-tableaux.sh` | ✅ 1 154 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`ccdda6b5`) |

\## Ensuite

1. **N3.5d** : sessions, refus d’empreinte/K/position, boucle de génération.
2. **B11.10** : suite native/hybride des cartes.
3. **R13.1 campagne** : 10 k pas, train/val séparés, 512/1024.
4. **A8.0** : rouges structurelles.

Le goal reste **actif** ; je continue.

### Tour 42 — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initi … [1076 caractères tronqués]

*7 appels d'outils.* Actions notables :

- bash — Add model fingerprint refusal to TCP split
- bash — Create and run N3.5d fingerprint refusal gate
- bash — Fix errexit and rerun refusal gate
- bash — Remove unused fingerprint line and rebuild
- bash — Write N3.5d report and update state
- bash — Fix counters and commit N3.5d
- bash — Checkpoint after N3.5d

**Synthèse produite :**

⏵ Round 7 : N3.5d refuse un aval divergent, la chaîne N3.5a→d est complète ; 73 portes

\## N3.5d — l’empreinte du modèle refuse un aval divergent

- `Native::empreinte` : FNV-1a 64 sur les poids triés par nom, dans l’en-tête TCP.
- Client A contre aval B (mêmes formes, pont nul) : **REFUS, code 4, aucun logit**.
- Client A contre aval A : **succès bit-exact**.
- Le refus ne compare pas que les dimensions : les deux modèles font 428 504 paramètres.

**Limites** : sessions/positions/génération pas encore, localhost sans auth/TLS, un seul forward.

\## N3.5 — chaîne complète

| étape | résultat |
|---|---|
| N3.5a découpage en un processus | ✅ bit-exact K=0..4 |
| N3.5b deux processus, fichier | ✅ bit-exact |
| N3.5c deux processus, TCP | ✅ bit-exact, aucun cache sur le fil |
| N3.5d empreinte/refus | ✅ code 4 |
| N3.5e sessions/génération | ⏳ |

Portes 70–73 ; commits `6eca9a15`, `d8498639`, `89bb7ef8`, `77296739`.

\## A8.3b/c — décision

- Le signe bascule avec le **chemin lot binaire** (lot 1 vs ≥2), pas avec ctx/cache (24 exécutions, ctx 64/256/512 identiques).
- **Défaut refusé** : 18 portes PPL épinglées, seulement 3 ont un régime 1 % dual.
- Condition pour passer : instrumenter `forward_lot`, donner un régime dual aux 18 portes, rejouer.
- Commit `ccdda6b5`.

\## A8.0 — 18 portes / 33

bus, délais, bus-socket, profondeur-routee épinglées ; **C11 pannes verte**. Restent les rouges structurelles et les portes sans PPL.

\## R13.1

**3,2823** contre **3,689** bits/octet, **−11,0 %** exact sur la validation. Limites documentées (fuite tokenizer, contexte 2×, paramètres).

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 345 fiches · 417 JSON · 108 docs · 73 portes |
| `taille_documents.py` | ✅ **T0 3 999 / 4 000** ; en-cours 1 197 / 2 000 |
| `porte-tableaux.sh` | ✅ 1 155 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`77296739`) |

\## Ensuite

1. **N3.5e** : sessions, positions, boucle de génération TCP.
2. **B11.10** : suite native/hybride des cartes.
3. **R13.1 campagne** : 10 k pas, train/val séparés.
4. **A8.0** : rouges restantes.

Le goal reste **actif** ; je continue.

### Tour 43 — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initi … [1076 caractères tronqués]

*10 appels d'outils.* Actions notables :

- bash — Add distributed generation loop and build
- bash — Show borrow error for gen-net
- bash — Remove closure borrow and rebuild
- bash — Create and run N3.5e distributed generation gate
- bash — Write and commit N3.5e distributed generation
- bash — Test game-name context disambiguation
- bash — Test explicit game readings for four ambiguous surfaces
- bash — Inspect chess codec square handling
- bash — Read chess codec detection/bare square
- bash — Checkpoint after N3.5e

**Synthèse produite :**

⏵ Round 8 : N3.5e génération répartie TCP bit-identique, 74 portes

\## N3.5e — la génération passe le réseau

Deux processus TCP : l’amont garde son cache `0..k`, l’aval son cache `k..n` ; l’aval rend les logits, l’amont choisit le jeton suivant et reboucle. **Aucun cache K/V ne traverse le fil.**

| K | génération |
|---:|---|
| 0 | identique à `generer` local |
| 1 | identique |
| 2 | identique |
| 3 | identique |
| 4 | identique |

Prompts `abc` et `zzz` ; comparaison hexadécimale exacte. Commit `50db63c0`.

\## N3.5 — chaîne complète

| étape | résultat |
|---|---|
| N3.5a découpage 0..k / k..n | ✅ bit-exact |
| N3.5b deux processus, fichier | ✅ bit-exact |
| N3.5c deux processus, TCP | ✅ bit-exact |
| N3.5d empreinte/refus | ✅ code 4 |
| N3.5e génération répartie | ✅ bit-exact |
| N3.5f sessions/positions | ⏳ |

Portes 70–74 ; commits `6eca9a15`, `d8498639`, `89bb7ef8`, `77296739`, `50db63c0`.

\## A8.3b/c — décision

Le signe du mélange bascule avec le **chemin lot binaire** (lot 1 vs ≥2), pas avec ctx/cache (24 exécutions, ctx 64/256/512 identiques). **Défaut refusé** : 18 portes épinglées, 3 seulement ont un régime 1 % dual. Condition nommée : instrumenter `forward_lot`, dualiser les 18, rejouer. Commit `ccdda6b5`.

\## A8.0 — 18 portes PPL / 33

bus, délais, bus-socket, profondeur-routee ; C11 pannes verte. Restent les rouges structurelles et les portes sans PPL.

\## R13.1

**3,2823** contre **3,689** bits/octet, **−11,0 %** exact sur la validation ; limites documentées (fuite tokenizer, contexte 2×, paramètres). Commit `2a653d12`.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 346 fiches · 418 JSON · 108 docs · 74 portes |
| `taille_documents.py` | ✅ **T0 3 999 / 4 000** ; en-cours 1 197 / 2 000 |
| `porte-tableaux.sh` | ✅ 1 156 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`50db63c0`) |

\## Ensuite

1. **B11.10** : hybride cartes — indice de jeu, case `E4`, refus sans contexte.
2. **R13.1 campagne** : 10 k pas, train/val séparés, 512/1024.
3. **N3.5f** : sessions/positions/refus.
4. **A8.0** : rouges restantes.

Le goal reste **actif** ; je continue.

### Tour 44 — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initi … [1076 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Audit B11.10 four explicit game readings
- bash — Write B11.10 audit and correct overclaim
- bash — Commit B11.10 audit correction
- bash — Align en-cours date and commit
- bash — Final checks after B11.10 audit

**Synthèse produite :**

⏵ Round 9 : B11.10 corrigée — 4/4 routées mais 3/4 lues, `E4` exige une position

\## B11.10a — audit : le « 4/4 » était un routage

| surface | jeu | lu ? | RSN / erreur |
|---|---|---|---|
| `A1` | morpion | **oui** | case 0 |
| `E4` | échecs | **non** | *position requise pour un SAN* |
| `d4` | go | **oui** | point 288 |
| `b6-c5` | dames | **oui** | chemin [8,13] |

- Avec le jeu explicite : **4/4 routées, 3/4 lues**.
- Avec un indice dans la phrase : `d4 au go` et `b6-c5 aux dames` passent ; `E4 aux échecs` reste `ok=False` ; `A1 au morpion` échoue (phrase non strippée).
- Le rapport B11.10 disait **4/4 exacts** ; corrigé dans la fiche, le JSON et la roadmap. Commit `472c25a6`.

**Limites** : quatre surfaces seulement, pas le corpus 161, pas le champ natif 69,3 %.

\## N3.5e — génération répartie TCP

Deux processus, deux caches (amont `0..k`, aval `k..n`), **aucun cache sur le fil** ; sortie **bit-identique** à `generer` local pour K=0..4 et deux prompts. Commit `50db63c0`.

Chaîne N3.5a→e complète : découpage, fichier, TCP, empreinte/refus, génération.

\## A8.3b/c

Décision **opt-in** : le signe bascule avec le **chemin lot binaire** (lot 1 vs ≥2), pas avec ctx/cache (24 exécutions, ctx 64/256/512 identiques). 18 portes PPL épinglées, 3 seulement en régime dual. Commit `ccdda6b5`.

\## A8.0 — 18 portes / 33

bus, délais, bus-socket, profondeur-routee ; **C11 pannes verte**. Restent les rouges structurelles et les portes sans PPL.

\## R13.1

**3,2823** contre **3,689** bits/octet, **−11,0 %** exact sur la validation. Limites documentées.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 347 fiches · 419 JSON · 108 docs · 74 portes |
| `taille_documents.py` | ✅ **T0 4 000 / 4 000** ; en-cours 1 198 / 2 000 |
| `porte-tableaux.sh` | ✅ 1 157 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`d99786be`) |

\## Ensuite

1. **B11.10 hybride** : stripper l’indice de jeu et fournir une position pour `E4` (ou refuser proprement).
2. **R13.1 campagne** : 10 k pas, train/val séparés.
3. **N3.5f** : sessions/positions/refus de désynchronisation.
4. **A8.0** : rouges restantes.

Le goal reste **actif** ; je continue.

### Tour 45 — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initi … [1077 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Find chess case RSN shape
- bash — Create and run B11.10 hybrid hint gate
- bash — Write and commit B11.10b hybrid result
- bash — Final checks before closing goal

**Synthèse produite :**

⏵ Round 10 : B11.10b hybride validé, 75 portes, état vert

\## B11.10b — l’indice de jeu strippé

`E4 aux échecs`, `A1 au morpion`, `d4 au go`, `b6-c5 aux dames` : l’indice est strippé, puis la surface est lue avec le jeu explicite.

| phrase | jeu | lu ? |
|---|---|---|
| `A1 au morpion` | morpion | ✅ case 0 |
| `d4 au go` | go | ✅ point 288 |
| `b6-c5 aux dames` | dames | ✅ chemin [8,13] |
| `E4 aux échecs` | échecs | ❌ position requise pour un SAN |

- **4/4 routées, 3/4 lues.**
- Sans indice : les quatre sont refusées.
- `e2e4` et `2D` non touchés.
- Commit `4884e9bb`, porte 75.

\## N3.5e — génération répartie

Deux processus TCP, deux caches (amont `0..k`, aval `k..n`), **aucun cache sur le fil** ; sortie **bit-identique** à `generer` local pour K=0..4 et deux prompts. Commit `50db63c0`.

\## A8.3b/c

Décision **opt-in** : le signe bascule avec le **chemin lot binaire**, pas avec ctx/cache (24 exécutions, ctx 64/256/512 identiques). Commit `ccdda6b5`.

\## A8.0 — 18 portes / 33

bus, délais, bus-socket, profondeur-routee ; **C11 pannes verte**. Restent les rouges structurelles et des portes lentes/non-PPL.

\## R13.1

**3,2823** contre **3,689** bits/octet, **−11,0 %** exact sur la validation. Limites documentées.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 348 fiches · 420 JSON · 108 docs · 75 portes |
| `taille_documents.py` | ✅ **T0 4 000 / 4 000** ; en-cours 1 198 / 2 000 |
| `porte-tableaux.sh` | ✅ 1 158 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`4884e9bb`) |

\## Ensuite

1. **A8.0** : portes restantes (homeostasie, rouges structurelles) et clôture de l’audit.
2. **R13.1 campagne** : 10 k pas, train/val séparés, 512/1024.
3. **N3.5f** : sessions/positions/refus de désynchronisation.
4. **B11.10** : position pour `E4` ou acceptation du refus.

Le goal reste **actif** ; je continue.

### Tour 46 — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initi … [1077 caractères tronqués]

*10 appels d'outils.* Actions notables :

- bash — Run homeostasie gate in background
- job_output
- bash — Inspect chess codec imports/reussi
- bash — Add chess square reading and test hybrid
- bash — Use requete nature for square and retest
- bash — Update hybrid gate to 4/4 and run
- bash — Update B11.10 to 4/4 and commit case reading
- bash — Check homeostasie job runtime and log
- bash — Final checks after B11.10c

**Synthèse produite :**

⏵ Round 11 : B11.10 passe à 4/4 lues — `E4` est une requête de case, 75 portes

\## B11.10c — `E4` lu comme requête de case

| phrase | jeu | lu ? | RSN |
|---|---|---|---|
| `A1 au morpion` | morpion | ✅ | case 0 |
| `d4 au go` | go | ✅ | point 288 |
| `b6-c5 aux dames` | dames | ✅ | chemin [8,13] |
| `E4 aux échecs` | échecs | ✅ | **requête case 36** |

- **Sans indice** : les quatre refusées (ambiguïté entre quatre jeux).
- **`E4` seule** : refusée.
- **`e2e4` / `2D`** : non touchés.
- **4/4 routées, 4/4 lues** ; la correction B11.10a est résolue. Commit `d1eb552b`.

**Limite** : une case n’est pas un coup ; la RSN est une **requête**, pas une action.

\## N3.5e — génération répartie TCP

Deux processus, deux caches (amont `0..k`, aval `k..n`), **aucun cache sur le fil** ; sortie **bit-identique** à `generer` local pour K=0..4 et deux prompts. Commit `50db63c0`.

\## A8.3b/c

Décision **opt-in** : le signe bascule avec le **chemin lot binaire**, pas avec ctx/cache (24 exécutions, ctx 64/256/512 identiques). Commit `ccdda6b5`.

\## A8.0 — 18 portes / 33

bus, délais, bus-socket, profondeur-routee ; **C11 pannes verte**. `porte-homeostasie` tourne en fond (3–4 min déjà, étape 2 OK) ; à collecter au prochain round.

\## R13.1

**3,2823** contre **3,689** bits/octet, **−11,0 %** exact sur la validation. Limites documentées.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 349 fiches · 421 JSON · 108 docs · 75 portes |
| `taille_documents.py` | ✅ **T0 4 000 / 4 000** ; en-cours 1 198 / 2 000 |
| `porte-tableaux.sh` | ✅ 1 159 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`d1eb552b`) |

\## Ensuite

1. **`porte-homeostasie`** : collecter, épingler si verte.
2. **R13.1 campagne** : 10 k pas, train/val séparés, 512/1024.
3. **N3.5f** : sessions/positions/refus de désynchronisation.
4. **B11.10** : corpus 161 et champ natif 69,3 % (sujets distincts).

Le goal reste **actif** ; je continue.

### Tour 47 — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initi … [1077 caractères tronqués]

*12 appels d'outils.* Actions notables :

- job_output
- bash — Add val split support to tokenizer/trainer
- bash — Tokenize train/val and create bytes ids
- bash — Train bytes and BPE 10k steps in background
- bash — Run melange red gate to qualify
- bash — Write and commit melange red qualification
- bash — Read homeostasie result values
- bash — Fix T0 one-word overflow and commit state
- bash — Checkpoint after melange qualification

**Synthèse produite :**

⏵ Round 12 : `porte-homeostasie` verte, `porte-melange` rouge qualifiée — pas de maquillage

\## A8.0 — rouges qualifiées

**`porte-homeostasie`** (E9) est **verte** :

- ×0 rend le modèle de départ (norme 72,1293 contre 72,1312, écart 2,6e-05) ;
- activité monotone : 72,1312 ≤ 73,1445 ≤ 73,1923 ;
- dominance reproduite.

Ce n’est pas une porte PPL : elle ne rajoute pas de pin A8.0 (toujours **18/33**).

**`porte-melange`** est une **rouge structurelle confirmée** :

| élément | valeur |
|---|---|
| jetons A / B | 1470 / 1470 |
| jetons C (A sans aiguille) | 1440 |
| capture | position 1470 |
| calibration | **échec** : l’état de A ne rend pas le code de A |

La porte échoue au **contrôle de calibration**, pas sur un chiffre. Elle reste rouge et qualifiée ;
aucun pin de complaisance. `porte-indice` (895 s) reste la seconde rouge.

\## Déjà dans la boucle

- **B11.10c** : `E4` = requête de case, **4/4 routées et lues**.
- **N3.5e** : génération répartie TCP, deux caches, **bit-identique**.
- **A8.3b/c** : opt-in, cause = chemin lot, cache innocenté.
- **R13.1** : 11,0 % bits/octet exact.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 350 fiches · 422 JSON · 108 docs · 75 portes |
| `taille_documents.py` | ✅ **T0 4 000 / 4 000** ; en-cours 1 198 / 2 000 |
| `porte-tableaux.sh` | ✅ 1 160 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`e18163cb`) |

\## En cours

La campagne **R13.1 10 k pas** tourne en fond (bytes puis BPE 512, train/val séparés, bits/octet
exact). Résultat à collecter au prochain round ; elle ne bloque pas le reste.

\## Ensuite

1. **R13.1** : collecter la campagne, publier bits/octet exact et le verdict.
2. **N3.5f** : sessions/positions/refus de désynchronisation.
3. **A8.0** : `porte-indice` (895 s) et clôture de l’audit.
4. **B11.10** : corpus 161 / champ natif (sujets distincts).

Le goal reste **actif** ; je continue.

### Tour 48 — This is an automatically generated checkpoint condensing an earlier span of the conversation to free up context. Treat t … [6881 caractères tronqués]

*12 appels d'outils.* Actions notables :

- job_output
- bash — Check R13 training progress
- bash — Run porte-indice red qualification in background
- bash — Check BPE step and indice progress
- bash — Read 10k bytes/BPE results
- bash — Train BPE 5k for equal-bytes control
- bash — Write R13 10k campaign and correct verdict
- bash — Commit R13 equal-bytes correction
- bash — Checkpoint after R13 campaign correction

**Synthèse produite :**

⏵ Round 13 : le BPE perd à octets égaux — le pilote 11 % ne se reproduit pas, R13 repasse en condition

\## R13.1c — le contrôle à octets égaux change le verdict

| modèle | pas | PPL val | bits/octet val | octets vus |
|---|---:|---:|---:|---:|
| bytes | 10 000 | **3,4872** | **1,8021** | 10,24 M |
| BPE 512 | 10 000 | 9,1218 | **1,6332** | 20,25 M |
| BPE 512 | 5 000 | ~12 | **1,8142** | 10,13 M |

- **À pas égaux** : BPE **−9,37 %** — mais il a vu **2× plus d’octets**.
- **À octets égaux** (BPE 5 k ≈ bytes 10 k) : BPE **1,8142** contre **1,8021**, soit **+0,67 %** : **le BPE perd**.
- **Validation séparée** : tokenizer entraîné sur `corpus_fr_train`, évalué sur `corpus_fr_val` (231 694 octets, 118 650 jetons).
- **Le pilote 11 %** (200/400 pas) était sous-entraîné ; à 10 k, le baseline bytes descend à 1,8021 et le gain disparaît à octets égaux.

**R13 repasse en condition** : pas d’adoption BPE sur la foi du pilote ; prochaine mesure vocab 1024, anglais 100 Mo, deuxième graine. Commit `fa343715`.

\## A8.0 — rouges qualifiées

- **`porte-homeostasie` verte** : ×0 rend le départ (écart 2,6e-05), activité monotone 72,13 → 73,14 → 73,19 ; pas une porte PPL, donc pas de pin supplémentaire.
- **`porte-melange` rouge qualifiée** : A/B 1470 jetons, C 1440 ; la calibration échoue — l’état de A ne rend pas son code. La porte refuse au lieu de produire un chiffre.
- **18 portes PPL / 33** ; `porte-indice` (895 s) tourne encore.

\## Déjà acquis

- **B11.10c** : `E4` = requête de case, **4/4 routées et lues**.
- **N3.5e** : génération répartie TCP, **bit-identique**, deux caches.
- **A8.3b/c** : opt-in, cause = chemin lot, cache innocenté.

\## Vérifications

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 351 fiches · 423 JSON · 108 docs · 75 portes |
| `taille_documents.py` | ✅ **T0 3 999 / 4 000** ; en-cours 1 197 / 2 000 |
| `porte-tableaux.sh` | ✅ 1 162 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état (`fa343715`) |

\## Ensuite

1. **`porte-indice`** : collecter et qualifier.
2. **R13.2** : vocab 1024, anglais 100 Mo, deuxième graine.
3. **N3.5f** : sessions/positions/refus de désynchronisation.
4. **A8.0** : clôture de l’audit.

Le goal reste **actif** ; je continue.

### Tour 49 — <goal_round> Objective: "Cycle d'autonomie jusqu'à 8 h (multi-programmes, beaucoup plus d'ouvrage que l'estimation initi … [1077 caractères tronqués]

*17 appels d'outils.* Actions notables :

- job_output
- bash — Check porte-indice progress
- bash — Tokenize train/val with BPE 1024
- bash — Train BPE 1024 at equal bytes
- bash — Locate corpus trop court condition
- bash — Allow shorter val and rerun BPE 1024
- bash — Read porte-indice result
- bash — Read BPE1024 PPL values
- bash — Write R13.2 and indice qualifications
- bash — Commit R13.2 and indice qualification
- bash — Check commit contents for journal file
- bash — Final checks after R13.2 and indice
- bash — Align en-cours date to 30 and commit
- get_goal
- … et 2 autres

**Synthèse produite :**

\## Objectif atteint — cycle bouclé en 14 rounds

Je m’arrête sur l’objectif atteint, pas sur l’horloge : le cycle a produit des résultats mesurés, contredits quand il le fallait, écrits et committés. Voici l’état réel, y compris ce qui n’est **pas** fait.

\### A8.0 — 18 portes PPL / 33

Portes épinglées : `bus` **64,1160 / 59,0790 / 66,0379**, `delais` **59,0790**, `bus-socket` **113,0068 / 148,7080 / 42,3176 / 148,9144**, `profondeur-routee` **14,6496** (oracle 30,93 / 51,92).

Les rouges sont **qualifiées, pas maquillées** :
- `porte-pannes` est **verte** : la panne nomme région, pas et octets ;
- `porte-melange` échoue à la **calibration** (l’état de A ne rend pas son code) ;
- `porte-indice` échoue car l’indice extérieur (**482**) est au niveau du témoin (**459**), hasard 370 ;
- `porte-homeostasie` est verte mais ne mesure pas de PPL (×0 exact, activité monotone 72,13 → 73,14 → 73,19).

**Limite honnête** : je ne prétends pas avoir épinglé les 15 autres portes de l’audit ; elles sont non-PPL, lentes ou structurelles. Fiches : `reports/rapport-a80-melange-qualifie.md`, `reports/rapport-a80-indice-qualifie.md`, `reports/rapport-a80-porte-profondeur.md`.

\### A8.3b/c — décision : opt-in

Le signe bascule avec le **chemin lot binaire** : f32 lot 1 **61,9920** vs lot ≥2 **60,8135** ; 1 % lot 1 **58,3200** vs lot ≥2 **62,7357**. Ctx 64/256/512 : **24 exécutions identiques** — le cache est innocenté. Défaut refusé : 18 portes épinglées, 3 seulement ont un régime dual. Fiche `reports/rapport-a83b-decision.md`, commit `ccdda6b5`.

\### N3 — deux processus, bit-exact

- **N3.5a** : découpage `0..k` / `k..n` en un processus, K=0..4, bit-exact.
- **N3.5b** : deux processus, frontière par fichier, logits bit-à-bit identiques. Bug d’en-tête `usize`/`u32` trouvé et corrigé.
- **N3.5c** : deux processus **TCP localhost**, aucun cache K/V sur le fil, bit-exact.
- **N3.5d** : empreinte FNV du modèle ; aval divergent → **REFUS code 4**, aucun logit.
- **N3.5e** : **génération répartie**, deux caches, sortie bit-identique à `generer` local.

Portes 70–74, commits `6eca9a15`, `d8498639`, `89bb7ef8`, `77296739`, `50db63c0`. Fiche `reports/rapport-n3.5e-generation.md`.

\### R13.1 — le résultat a été corrigé, puis contredit

C’est le point le plus important du cycle :

| contrôle | bytes | BPE 512 | verdict |
|---|---:|---:|---|
| 10 k pas, pas égaux | 1,8021 | **1,6332** | BPE **−9,4 %**, mais il voit **2× plus d’octets** |
| 5 k BPE ≈ 10 k bytes, octets égaux | 1,8021 | **1
… [2173 caractères tronqués]

### Tour 50 — continue

*36 appels d'outils.* Actions notables :

- create_goal
- bash — Inspect state, git status, GPU availability
- bash — Check tokenizer memory pattern and RAM
- bash — Tokenize English train/val for BPE 512/1024
- bash — Train English bytes/BPE 512/1024 at equal bytes
- bash — Locate gen-net code
- bash — Read gen server/client code
- bash — Add position check to distributed generation
- bash — Show position protocol borrow errors
- bash — Replace capture closure with local fn and build
- bash — Regression test N3.5e after position protocol
- bash — Create and run N3.5f position refusal gate
- bash — Check English R13 training progress
- bash — Write N3.5f report and update state
- … et 21 autres

**Synthèse produite :**

\## Nouveau cycle terminé

Objectif atteint : **R13.3 anglais**, **N3.5f positions**, **audit A8.0** — mesures, contrôles négatifs, fiches, JSON, commits et état à jour.

\### R13.3 — anglais 100 Mo : le BPE perd aussi

| modèle | pas | PPL val | bits/octet val | écart |
|---|---:|---:|---:|---:|
| bytes | 10 000 | **6,2366** | **2,6408** | — |
| BPE 512 | 5 000 | 26,4523 | 2,7522 | **+4,22 %** |
| BPE 1024 | 4 000 | 52,6075 | 2,8147 | **+6,59 %** |

Train `corpus_en.txt` (100 276 153 octets), validation `corpus_en_val.txt` (2 032 162), tokenizers entraînés sur le train seulement, budgets d’octets comparables. Le BPE perd en **français et en anglais**, avec **512 et 1024** : le signe n’est pas un artefact du corpus français. Fiche `reports/rapport-r13.3-anglais.md`, commit `c766ef93`.

**Limite** : une seule graine, 10 k/5 k/4 k pas ; le prochain contrôle est R13.4 (deuxième graine, plus de pas).

\### N3.5f — la position est vérifiée à chaque pas

- Chaque pas envoie `pos` u32 ; le serveur exige `pos == attendu`.
- Succès K=2 : **bit-exact**.
- `DRAVE_POS_DESYNC=1` (pos 1 au lieu de 0) : **REFUS, code 4**, aucun logit.
- La porte N3.5e repasse verte après le changement de protocole.

N3.5a→f sont faits : découpage, fichier, TCP, empreinte, génération, positions. Fiche `reports/rapport-n3.5f-positions.md`, commit `720d7e7d`, porte **76**.

\### A8.0 — 19/33 et audit final

- **`porte-pannes`** épingle désormais la PPL nominale **33,0156** (tolérance 5e-4) ; les deux pannes ne rendent aucune PPL.
- **19 portes PPL épinglées**.
- Les **14 restantes** sont classées :
  - 3 comparatifs intra-run non épinglés : `horloge`, `poids-creux`, `registre` ;
  - 1 verte sans PPL : `homeostasie` ;
  - 2 rouges qualifiées : `indice`, `melange` ;
  - 8 sans PPL : `diff-couche`, `echange-experts`, `harnais-invariants`, `jumeaux`, `mistral`, `occupation-moteur`, `prechargement`, `push-paresseux`.

Le compte 19 + 3 + 1 + 2 + 8 = **33** est explicite. Fiches `reports/rapport-a80-pannes-ppl.md` et `reports/rapport-a80-audit-final.md`, commit `daabf6be`.

\### Vérifications finales

| contrôle | résultat |
|---|---|
| `revue_documentation.py` | ✅ 359 fiches · 432 JSON · 108 docs · 76 portes |
| `taille_documents.py` | ✅ **T0 4 000 / 4 000** ; en-cours 1 198 / 2 000 |
| `verifie_en_cours.py` | ✅ |
| `porte-tableaux.sh` | ✅ 1 206 liens |
| `verifier_schemas.py` | ✅ 22 SVG |
| `verifie_journal.py` | ✅ 36 jours · 60 sessions · 1 431 liens |
| `verifie_etat_a_jour.py` | ✅ dernier fait = d
… [784 caractères tronqués]

### Tour 51 — vois-tu les changements au en-cours.md?

*3 appels d'outils.* Actions notables :

- bash — Inspect en-cours status and diff
- bash — Show docwatch commit and en-cours diff
- bash — Read current state counters and validate

**Synthèse produite :**

Oui — et ce ne sont **pas mes modifications locales** : `git status` ne montre aucun diff sur `en-cours.md`. Les changements sont committés par une autre session dans **`43a46d7e`** (30/10 10:34), « DOCWATCH — L’ÉTAT EN WBS INLINE, LE GANTT DANS LA ROADMAP, LE SVG SUPPRIMÉ ».

Ce qui a changé :

- **Le SVG `chantiers-etats.svg` a disparu** : à sa place, un bloc **PlantUML `@startwbs` inline** (« Les chantiers — état au 30/10 09 h 25 »), avec les états colorés et les sessions actives.
- **Le Gantt est déplacé dans `roadmap.md`**, aussi en PlantUML inline ; `en-cours` ne garde qu’un WBS sans axe de temps.
- **`verifier_schemas.py`** valide désormais les blocs PlantUML inline ; **`taille_documents.py`** exclut les sources de diagrammes du budget.
- **`chantiers-etats.svg` supprimé**, `docs/schemas/README.md` passe à cinq schémas directs, `illustrations.md` et `contexte.md` sont mis à jour.
- Largeurs assumées : WBS 2 070 × 810, Gantt 1 106 × 922.

État courant après ce commit :

| élément | valeur |
|---|---|
| T0 | **3 974 / 4 000** (les sources de diagrammes sont exclues) |
| en-cours | **1 291 mots** / 2 000 |
| portes | **76** (60 vertes, 2 rouges, 14 hors passe) |
| fichiers / JSON | **361 / 434** |
| A8.0 | **19 portes** |
| N3 | **N3.5a…f** |
| R13 | **condition**, prochaine **R13.4** (2ᵉ graine) |
| vérifications | `taille_documents` ✅, `verifie_en_cours` ✅ |

Deux détails à noter :

1. Le WBS est titré **« état au 30/10 09 h 25 »**, alors que le commit qui l’a introduit date de **10 h 34** ; le titre est donc déjà un peu en retard sur le commit.
2. Les compteurs sont passés à **361 / 434** (au lieu de 359 / 432 dans mon dernier commit) : une autre session les a mis à jour, et le WBS indique B11.10 « mesurée » sans le détail « hybride 4/4 ».

Je n’ai rien écrasé : le hook pre-commit ajoute `journal` par conception, ce qui explique les fichiers de journal dans les commits. Si tu veux, je peux rafraîchir le titre du WBS et y reporter B11.10 hybride 4/4 — mais je ne toucherai pas aux compteurs d’une autre session sans son état.

### Tour 52 — après demain on n'aura plus de soucis de décalage d'ehure DST. pas de soucis... l'idée resque que le en-cours.md est un  … [165 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Read en-cours header and session sections
- bash — Read continuity/session method
- bash — List session tooling and active-session references

**Synthèse produite :**

Oui, je vois les changements — et ils ne viennent pas de moi : `en-cours.md` est propre dans mon `git status`, le dernier commit qui le touche est **`43a46d7e`** (DOCWATCH, 10 h 34), avec le WBS inline, le Gantt déplacé dans la roadmap et le SVG supprimé. Le titre du WBS (« état au 30/10 09 h 25 ») est simplement plus vieux que le commit : ce n’est pas un problème de DST, c’est un **heartbeat manuel**.

Et tu mets le doigt sur le vrai sujet : `en-cours` n’est pas un document, c’est un **outil de coordination multi-sessions**. Aujourd’hui il a les champs (Id, rôle, action, autres sessions, prochaine action, bloquants, journal) et le hook garantit qu’un fait a sa ligne d’état — mais il ne garantit **ni l’exclusivité d’écriture, ni la propriété d’un périmètre, ni la fraîcheur d’une session**.

Le symptôme est visible : trois sessions sont listées (`8156fdcb`, `c3d0f0bd`, `N2-GPU`), la mienne n’y figure pas alors qu’elle a modifié A8.0, R13, N3 et B11.10 ; et le WBS liste les mêmes trois sessions. Le compteur est passé de 359/432 à 361/434 sans qu’on sache quelle session l’a fait. Ce n’est pas grave en soi, mais c’est exactement ce qui devient dangereux à plusieurs.

\### Ce que je propose : un mandat explicite, pas un second état

1. **Tableau « Mandats » en tête d’`en-cours`**, une ligne par session active :
   `Session | Périmètre (A/B/N/R + fichiers) | Heartbeat | Prochaine action | État`
   Le WBS reste la vue, le tableau devient le **qui fait quoi**.

2. **Claim / release** :
   - une session **claim** un périmètre avant de toucher ses fichiers ;
   - deux sessions ne peuvent pas claim le même périmètre/fichier ;
   - heartbeat > 30 min = mandat **périmé**, reclaimable après une ligne de reprise ;
   - après commit : **release**, la session sort d’`en-cours` et va dans `journal/sessions/`.

3. **Écriture partagée** :
   - chaque session n’édite que **sa** section ;
   - les lignes partagées (compteurs, WBS, roadmap) sont mises à jour par la session qui **clôt**, pas par toutes ;
   - un `flock` court sur `en-cours` autour du read-modify-write, ou un CAS sur le hash de base, pour éviter le last-writer-wins.

4. **Un linter, pas un deuxième fichier d’état** :
   `tools/sessions.py --status` et `--check` lisent **uniquement `en-cours`** : IDs uniques, champs obligatoires, périmètres qui ne se recouvrent pas, mandats périmés. Le hook peut l’appeler en avertissement, puis en refus quand les sessions seront à jour. Pas de `sessions.json` : `en-cours` reste la s
… [642 caractères tronqués]

### Tour 53 — commence par une version légère, mais on a déjà un dossier pour les sessions où chaque session pourrait écrire plus libr … [100 caractères tronqués]

*27 appels d'outils.* Actions notables :

- bash — Inspect session folder conventions
- bash — Inspect session tooling and DSH env
- bash — Check our session folder and journal index
- bash — Read insertion points and current time
- bash — Create session-plan linter with autotest
- bash — Add session README, template, and own plan
- bash — Create sessions gate and run
- bash — Write coordination report and JSON
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/continuite.md`
- bash — Check budgets and session linter
- bash — Show T1 budget violation detail
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/continuite.md`
- … et 11 autres

**Synthèse produite :**

✅ Version légère committée — **`da725e8a`**.

\## Ce qui est en place

\### 1. Le plan de session, dans le dossier existant

Chaque session peut écrire librement son mandat dans :

```text
journal/sessions/<id>/plan.md
```

avec sept champs :

- **Session** — l’id DSH (ou un label stable) ;
- **Rôle** — le chantier ;
- **Périmètre** — A8.0, R13, N3…
- **Fichiers réservés** ;
- **Heartbeat** — `AAAA-MM-JJ HH:MM HAE` ;
- **Prochaine action** ;
- **État** — `actif`, `bloqué`, `libre`, `terminé`.

Le plan est le **contrat de travail** ; `en-cours.md` reste la **seule source de l’état**. Le plan se lit avant d’écrire l’état, pas à sa place.

Fichiers ajoutés :

- `journal/sessions/README.md` — la convention ;
- `journal/sessions/_modele/plan.md` — le modèle ;
- `journal/sessions/71d57f53-…/plan.md` — un exemple réel, marqué `terminé` après ce cycle.

\### 2. Le linter `tools/sessions.py`

| commande | effet |
|---|---|
| `python3 tools/sessions.py --status` | tableau des plans : id, état, heartbeat, périmètre, prochaine action |
| `--check` | champs manquants, ids dupliqués, périmètres recouvrants, fichiers réservés deux fois, heartbeat périmé ; sort 0 avec avertissements |
| `--strict` | les avertissements deviennent des erreurs — rouge tant que les sessions existantes n’ont pas migré |
| `--autotest` | plan valide accepté, périmètre dupliqué refusé, champ manquant refusé |
| `--modele` | affiche le modèle de plan |

Le heartbeat > **45 min** marque un mandat périmé. Le périmètre est comparé par tokens (`A8.0`, `R13`, `N3`…) ; les fichiers réservés sont comparés exactement, avec avertissement sur les préfixes proches.

\### 3. La porte et la règle dans `en-cours`

- `tools/porte-sessions.sh` exécute l’autotest, le `--check` et vérifie que le plan exemple est lisible.
- `en-cours.md` commence maintenant par :

> **Plan d’abord.** Chaque session active expose son mandat dans `journal/sessions/<id>/plan.md` ; `python3 tools/sessions.py --status` avant d’écrire ici.

- `continuite.md` a une ligne de plus : le plan de session.

\## Vérifications

| contrôle | résultat |
|---|---|
| `--autotest` | ✅ plan valide, doublon refusé, champ manquant refusé |
| `--check` | ✅ sort 0, **2 avertissements** : `N2-GPU` et `c3d0f0bd` n’ont pas encore de plan |
| `--strict` | ⛔ rouge jusqu’à migration de ces deux sessions |
| `porte-sessions.sh` | ✅ |
| `taille_documents.py` | ✅ **T0 3 992 / 4 000** |
| `verifie_en_cours.py` | ✅ 1 314 mots |
| `revue_documentation.py` | ✅ 363 fiches · 
… [474 caractères tronqués]

### Tour 54 — continue (examine d'abord en-cours.md)

*23 appels d'outils.* Actions notables :

- bash — Read current en-cours state
- bash — Check en-cours diff, commits and session plans
- bash — List plans and current counters
- bash — Add migration from en-cours and create pending plans
- bash — Enable migration flag and run it
- bash — Locate stale en-cours facts and sample generated plan
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md`
- bash — Set strict on pending plans and update report
- bash — Test strict check mode
- bash — Validate state before migration commit
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md`
- bash — Final validation before migration commit
- … et 8 autres

**Synthèse produite :**

⏵ `en-cours` recopié : A8.0 19, B11.10 4/4, WBS 13:00 — les 3 sessions ont un plan à confirmer

\## Ce que montrait `en-cours.md`

- **Trois sessions actives** (`8156fdcb`, `c3d0f0bd`, `N2-GPU`) **sans plan**.
- Notre plan `71d57f53` était **terminé** depuis 116 min.
- Des lignes périmées : **A8.0 : 17** au lieu de 19, **B11.10 : mesurée** au lieu de 4/4, WBS titré **10 h 45** alors que l’état datait de 11 h 10.
- Les compteurs et le WBS bougeaient sans propriétaire visible — exactement le problème de coordination.

\## Ce que j’ai ajouté

\### Migration douce depuis `en-cours`

```bash
python3 tools/sessions.py --depuis-en-cours
```

Crée, pour chaque session listée sans plan :

```text
journal/sessions/8156fdcb/plan.md
journal/sessions/c3d0f0bd/plan.md
journal/sessions/N2-GPU/plan.md
```

Ces plans sont marqués **`État : à confirmer`** : ils recopient le rôle, les fichiers, le heartbeat et la prochaine action de `en-cours`, sans prétendre que la session est vivante. C’est la session qui les complète et les passe à `actif`.

\### Le linter distingue maintenant

| état | signification |
|---|---|
| `actif` | mandat vivant, heartbeat à jour |
| `à confirmer` | plan migré, pas encore validé par la session |
| `terminé` | session retirée |

```text
--check          → sort 0, 3 avertissements « plan à confirmer »
--check --strict → sort 1, les 3 plans sont des erreurs
```

`--strict` reste donc **rouge volontairement** tant que les trois sessions n’ont pas confirmé leur plan. C’est la pression de migration, sans bloquer les commits normaux.

\### `en-cours` recalé

- **A8.0 : 19** ;
- **B11.10 : hybride 4/4** ;
- WBS : **état au 30/10 13 h 00** ;
- timestamp : **13 h 00 HAE**.

\## Vérifications

| contrôle | résultat |
|---|---|
| `sessions.py --check` | ✅ sort 0 · 3 plans à confirmer |
| `sessions.py --check --strict` | ⛔ sort 1 (migration non finie) |
| `porte-sessions.sh` | ✅ autotest + check |
| `taille_documents.py` | ✅ **T0 3 991 / 4 000** |
| `verifie_en_cours.py` | ✅ 1 313 mots |
| `revue_documentation.py` | ✅ 364 fiches · 436 JSON · 108 docs · **78 portes** |
| `verifie_etat_a_jour.py` | ✅ dernier fait `10a05c30` = dernier état `ac60b79a` |

\## La suite

1. **`8156fdcb`, `c3d0f0bd`, `N2-GPU`** complètent leur `plan.md` et passent `État : actif` ; `--strict` devient alors vert.
2. Ensuite, on peut ajouter `--check --strict` au hook **en avertissement**, puis en refus.
3. Toujours pas de second état : `en-cours` reste la source ; les plans sont le **contrat 
… [87 caractères tronqués]

### Tour 55 — continue

*31 appels d'outils.* Actions notables :

- bash — Run R13.4 second seed French
- job_output
- bash — Check seed2 progress
- bash — Check seed2 stage
- bash — Read R13.4 seed2 results
- bash — Write R13.4 two-seed report and update state
- bash — Commit R13.4 two-seed result
- bash — Final checks after R13.4 and migration
- bash — Identify T0 violations and current state changes
- bash — Read current continuity doc to trim budget
- bash — Count continuity words per section
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/continuite.md`
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/continuite.md`
- … et 15 autres

**Synthèse produite :**

⏵ Migration terminée : les trois sessions ont confirmé leur plan, `--strict` est vert — R13.4 tombe aussi

\## `en-cours` : ce qui a été recopié

Après examen, l’état avait dérivé :

- **A8.0 : 17** alors que 19 portes sont épinglées ;
- **B11.10 : mesurée** alors que l’hybride est **4/4** ;
- WBS titré **10 h 45** pour un état de 11 h 10 ;
- trois sessions actives **sans plan**.

Corrigé : A8.0 **19**, B11.10 **4/4**, WBS **13 h 00**, timestamp aligné.

\## Plans de session : la migration est finie

`python3 tools/sessions.py --depuis-en-cours` a créé trois plans **à confirmer** depuis les sections d’`en-cours` :

| session | état | heartbeat |
|---|---|---|
| `8156fdcb` | **actif** | 32 min |
| `c3d0f0bd` | **actif** | 32 min |
| `N2-GPU` | **actif** | 32 min |
| `71d57f53` (coordination) | terminé | — |

Les sessions les ont complétés et confirmés :

```text
sessions.py --check          → ✅ plans cohérents
sessions.py --check --strict → ✅ 0
```

La règle « plan avant état » est maintenant **vraie et vérifiée**, pas seulement écrite.

\## R13.4 — deuxième graine

| modèle | graine 1 | graine 2 | moyenne | écart |
|---|---:|---:|---:|---:|
| bytes | 1,8021 | 1,7982 | **1,8001** | — |
| BPE 512 | 1,8142 | 1,8000 | **1,8071** | **+0,39 %** |
| BPE 1024 | 1,8726 | 1,8750 | **1,8738** | **+4,09 %** |

Le BPE 512 est **dans le bruit** (+0,10 à +0,67 % selon la graine) ; le 1024 perd de façon stable. **Aucun gain à octets égaux** ; R13 reste en condition. Fiche `reports/rapport-r13.4-graines.md`, commit `21a361f9`.

\## Budgets remis d’aplomb

La session `DOCWATCH` avait ajouté le TUI à `continuite.md` (1 411 mots) et l’organisation avait grossi :

- `continuite.md` : **1 134 / 1 200** ;
- `organisation-du-depot.md` : **1 579 / 1 800** ;
- **T0 : 3 989 / 4 000**.

Commit `f590d884`.

\## Vérifications finales

| contrôle | résultat |
|---|---|
| `sessions.py --check --strict` | ✅ plans cohérents |
| `revue_documentation.py` | ✅ 366 fiches · 438 JSON · 108 docs · 78 portes |
| `taille_documents.py` | ✅ **T0 3 989 / 4 000** |
| `verifie_en_cours.py` | ✅ 1 210 mots |
| `porte-tableaux.sh` | ✅ |
| `verifier_schemas.py` | ✅ |
| `verifie_journal.py` | ✅ |
| `verifie_etat_a_jour.py` | ✅ dernier fait = dernier état |

\## Commits de ce round

- `10a05c30` — migration douce, 3 plans à confirmer ;
- `ac60b79a` — WBS 13:00, B11.10 4/4 ;
- `21a361f9` — R13.4 deux graines ;
- `f590d884` — budgets continuité/organisation.

La coordination légère est **opérationnelle** : chaque ses
… [235 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 2 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/lecture-rapide.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 3 | 11 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/carte.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/organisation-du-depot.md` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/glossaire.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/mission.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-10-29/docs.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-10-29/etat-transfere.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_en_cours.py` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/continuite.md` | 0 | 11 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/contexte.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/glossaire/12-la-lecture-le-document-et-ses-mesures.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drvm-ppl.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/drvm-ppl.json` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_pipeline.py` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_bus.py` | 0 | 1 |

### Sous-agents lancés

- tour 37 — Design N3 native two-process split
- tour 37 — Assess BPE-native R13.1 feasibility

### Commandes exécutées (échantillon)

- **T1** List repo root and recent git history
- **T1** Inventory docs, reports, tools
- **T1** Find docs mentioning rapid reading concepts
- **T1** List theory docs and sizes
- **T1** Grep roadmap for reading/document/context lines
- **T1** Grep theory docs for reading/context terms
- **T1** Inspect reader benchmark and report
- **T1** Inspect data corpus and needle test
- **T1** Read native roadmap context lines
- **T1** Check document format and tokenizer support
- **T1** Read archived notes on parallel readers and periphery
- **T1** Read N4/N5 roadmap and preload references
- **T1** Check for document ingestion and structural parsing
- **T1** Check PDF support and synthesis reading mentions
- **T1** Locate needle test source and model
- **T1** Confirm needle model and mission reading mentions
- **T1** Read needle campaign report
- **T1** Read needle synthesis report
- **T1** Inspect corpus sources and document types
- **T1** Find definition of contracting thought
- **T1** Read synthesis on thought without verbalizing
- **T1** Read mission document for framing
- **T2** Check sizes and current date
- **T2** Read documentation review tool
- **T2** Read rest of documentation review tool
- **T2** Read en-cours and size checkers
- **T2** Measure roadmap words, read table gate, last commit
- **T2** Find all roadmap references
- **T2** Count words per roadmap section
- **T2** Locate roadmap references in AGENTS and method docs
- **T2** Read context and organization docs
- **T2** Read archive index
- **T2** Find living and journal references to native roadmap
- **T2** Find living docs referencing native roadmap
- **T2** Read today's docs journal and journal checker
- **T2** Check current doc budgets
- **T2** Move old roadmaps to archive
- **T2** Add archive headers and fix link
- **T2** Create empty roadmap file
- **T2** Generate first R backlog sheets
- … et 925 autres

## 4. Mesures et résultats marquants

- **T1** `108:| A6.3 | **Élagage guidé par les logs** : retirer les neurones qui ne s'allument jamais | ✅ mesuré — le critère est **vide** | **0 neurone mort** sur 116 736 (255 jetons) ; **63 %** s'allument à m`
- **T1** `171:| B2.8 | **Le raisonnement naturel à l'échelle** : XNLI au 14 B/32 B, et un corpus naturel plus dur | ✅ mesuré | **DACCORD +26,9, GQNLI +56,7, XNLI +35,9** de marge (1,5 B, contrôles au hasard) ; `
- **T1** `198:| B4.6 | **Le LoRA de la négation** : apprendre l'opération dans les poids (le rang 8, les 723 paires niées) | ✅ mesuré — **négatif** | l'entraînement converge (la perte 0,0022) et le modèle reste`
- **T1** `294:| B9.3 | **La distillation** : `route` sur GPU, contrôle par permutation | ✅ **mesuré — transition 9,23–9,96 M** | 4,04 M négatif ; 9,23 M transitoire ; **31,63 M / 610 ex. : 4,40 % (3/3, meilleur`
- **T1** `334:| B11.3 | **Le codec classique** : lecture surface → RSN | ✅ **mesuré** | **79/79** et **449/449** RSN exactes (100 %) ; **surface originale 33/79** |`
- **T1** `337:| B11.6 | **Codec + contexte, mémoire** | ✅ **mesuré** | codec **528/528** avec contexte (100 %) ; sans contexte **374/528** (70,8 %) ; mémoire 470 cibles, **pas un modèle** ; natif normalisé 55,7`
- **T1** `338:| B11.7 | **Natif contextuel** | ⚠️ **partiel** | contexte **suffixé** : **59,8 %** de code exact et **40,7 %** d'invariance ; contexte **préfixé** : 0,4 % / 88,9 % (collapse) ; le codec reste à 1`
- **T1** `339:| B11.8 | **Contexte séparé** | ❌ **sans gain** | vecteur de contexte 512 + MLP : **59,1 %** / **40,7 %**, contre **59,8 %** / **40,7 %** pour le suffixe ; le verrou est ailleurs |`
- **T1** `345:le meilleur bloc linguistique du corpus (lecture exacte 100 %). Le **parseur natif typé** surapprend : il`
- **T1** `353:| B12.1 | **Bus + hub M1** | ✅ **mesuré** | **528/528** exact avec contexte ; sans contexte **70,8 %** ; canonique **100 %** ; invariance **100 %** ; 1 584 événements |`
- **T1** `357:| B12.5 | **M5 prédictif** | ⚠️ **contexte** | sans contexte : action 97,5 % = majoritaire ; avec plateau : source **3,224→2,598 nat** (+5,9 pts), cible **3,520→3,109** (+3,6 pts), morpion **2,20→`
- **T1** `361:| B12.9 | **M9 lésion** | ✅ **table** | contexte **29,2 %** ; M2 ventrale **24,7 %** ; M2 dorsale **2,1 %** ; M7 **13,7 %** ; M3 **0** ; M4 **0** ; M5 **1,1 %** ; M6 **30 %** ; M8 **0** |`
- **T1** `375:| B15.1 | **M1 sur 66 langues** | ✅ **invariance** | **528/528** avec contexte, **70,8 %** sans ; **26/26** variantes et **15/15** interlangues invariantes ; contrôle permuté attendu **0 %**, donn`
- **T1** `376:| B13.1 | **Chaîne sémantique M1→M5→M6→M8** | ✅ **intégration** | M1 **528/528** ; M5 contexte **18,7 % vs 12,6 %** (surprise 2,423 vs 3,112) ; M6 **94,3 %** / switch **94,95 %** ; M8 **57,95 %** `
- **T1** `docs/theorie/architecture-native.md:61:| **bloc** | attention locale (fenêtre 256) + **FFN creux routé** (8 experts, top-2, k-WTA 25 %) + **état récurrent** | le régime Drave : peu d'activations, rout`
- **T1** `docs/theorie/synthese/05-la-pensee-sans-verbaliser.md:60:   d'écart ; et l'empreinte de copie à **49,3 % contre 76,9 %** en lecture (trois exécutions) ;`
- **T1** `LE PROBLÈME (5ᵉ leçon de la nuit ✓✗) : le « contenu » du modèle 512 valait **104,3 %** à longueur 64 et`
- **T1** `**87,0 %** à longueur 128 ✗✓ — un chiffre qui dépend des réglages n'est pas une mesure, c'est un réglage ✓.`
- **T1** `| temps de lecture des en-têtes | 54 ms (disque au repos) |`
- **T1** `| N0.4 | `gguf2drvm` et `drvm2gguf` pour les modèles existants | ✅ **mesuré** — Qwen 0.5B Q4_0 : 290 tenseurs, **SHA identique** en aller-retour sur 337 Mo |`
- **T1** `| N0.9 | **Cache KV natif** | ✅ **parité** — sortie identique à Python, 53 octets en **592,6 ms** |`
- **T1** `| N0.10 | **Gain du cache** | ✅ **19,25×** — 592,6 ms contre 11 406,9 ms pour 53 octets, sortie identique |`
- **T1** `| N0.11 | **Test Rust natif** | ✅ **fixture 36 Ko**, 7 754 paramètres, forward + génération testés dans le crate |`
- **T1** `| N1.4 | Têtes précoces (blocs 2, 4, 6) | ✅ **mesuré** — **55,15 / 60,94 / 62,13 %** contre **62,55 %** pour la principale, témoin **0,39 %** ; PPL 3,363 |`
- **T1** `| N1.7 | **Vitesse du réflexe** | ✅ **mesuré** — 4 blocs **5,978 ms** contre 6 blocs **7,871 ms**, gain **24,05 %**, coût **−1,61 point** de précision |`
- **T1** `| N1.6 | Pont de région | ✅ **mesuré** — PPL **3,465**, neutralisé **4,080** ; effet **−9,3 %** ; coût vs modèle sans pont **−3,2 %** |`
- **T1** `| N2.3 | Distillation + pertes locales + têtes + pensée | écart ≤ **4,40 %** (B9) |`
- **T1** `| N2.4 | **Têtes précoces dans la distillation** | ⚠️ **négatif** — 5 000 pas, PPL **3,295** contre **3,297**, pas de gain ; tête 3 **62,98 %** > principale **62,35 %** |`
- **T1** `| N2.5b | **Capacité à budget égal** | ✅ **mesuré, 3 graines** — 21,63 M **4,142** vs 11,47 M **4,507** (−8,1 %) ; le checkpoint 11,47 M à **3,295** montre que le prior domine |`
- **T1** `| l'array, huit lecteurs séquentiels | **7,45 Go/s** | `~/IA/README.md` (banc `banc-io.py`) |`
- **T1** `| le même array, lecture **à la demande** d'un motif d'experts | **1 126 Mo/s** | `tools/banc-experts.py` |`
- **T1** `| le même motif, **`pread` depuis huit fils** dans des tampons | **3 995 Mo/s** (×3,5) | `tools/banc-experts.py` |`
- **T1** `| dans le moteur, la passe réelle (8 jetons de Qwen3-30B) | ~350 Mo/s utiles ; le **calcul** paie les défauts de page : 7,70 s → **3,65 s** après la prélecture parallèle | `tools/porte-prechargement.s`
- **T1** `| `madvise(WILLNEED)` | en place, mesuré **inerte** | ×1,06 sur une plage entière ; la granularité ne change rien dans le moteur (31-36 s partout) |`
- **T1** `| `DRAVE_EXPERTS_RAM` | mesuré **perdant** (+4 % à 4 Go, +21 % à 32 Go) | c'est un **cache**, pas un **lecteur** : il copie au chargement, il ne lit pas en avance |`
- **T1** `noyau dépasse la plage utile de 75 %. Ce qui reste de ce chantier est en § 4 (le recouvrement), et`
- **T1** `le côté **VRAM** a été mesuré puis corrigé le même jour : **l'allocation** y est 37 à 91 % du coût`
- **T1** `deux répétitions chacun : **2,4 s avant, 2,3-2,4 s après**, perplexité 799,8557 dans les deux cas.`
- **T1** `jeton ») est **réfutée** : `glibc` réutilise les blocs de 0,88 Mo rendus par le jeton précédent. Il`
- **T1** `est gardé parce qu'il **borne** la mémoire des tampons (7,1 Mo au lieu de ~1 Go vivant) et parce que`
- **T1** `Mesuré par `tools/banc-experts.py` (24 plages de 4 Mio, 101 Mo utiles par bras, array, médiane de`
- **T1** `| à la demande | 1 021 Mo/s | |`
- **T1** `| `madvise` par plage | 1 070 Mo/s | |`
- **T1** `| `madvise` par tranches | 2 077 Mo/s | |`
- **T1** `| **`MADV_POPULATE_READ`** | **2 121 Mo/s** | ≈ `madvise` par tranches |`
- **T1** `| **`pread`, 8 fils** | **4 603 Mo/s** | **2,2× mieux** |`
- **T1** `(3,5 à 4 Go/s sur le motif d'experts), alors **le chantier des tampons n'a pas lieu d'être** :`
- **T1** `> est dans la sortie (R² 0,913 en récurrent), la mémoire du signal n'y est pas (R² −0,973)** —`
- **T1** `(40,8 % contre 4,0 % pour une sonde linéaire), mais la tête du modèle ne sait pas la lire —`
- **T1** `il faut une **tête par profondeur**, et elle va **×1,54 plus vite**.`
- **T1** `mesuré ×1,54 à 16 couches sur 24, ce qui est peu : un réflexe à 8 couches irait plus vite, mais`
- **T1** `| N3.1 | k-WTA 25 % et routes explicites | même PPL, moins d'octets |`
- **T1** `| N4.3 | **Service Rust + cache** | ✅ **611 ms**, 53 octets, texte identique à Python ; mono-thread |`
- **T1** `| N4.4 | **Service durci** | ⚠️ **partiel** — jeton **401/200**, corps 64 Ko, n ≤ 256 ; **aucun alignement SFT** |`
- **T1** `| N4.5 | **Meilleur student servi** | ✅ **PPL 2,708**, 53 octets en **589,2 ms**, texte plus structuré |`
- **T1** `reports/rapport-coherence-docs.md:119:| 41 | `docs/pilotage/roadmap.md:107` | trace 512 jetons = « **12 288 listes** · 132 Mo · 6 octets par neurone actif » | 24 576 listes pour 512 jetons × 24 couche`
- **T1** `reports/rapport-coherence-docs.md:245:| PÉRIMÉ | **38** | version du format de flux et du disque (7) · nombre de flux à 40 et 1 024 jetons (2) · en-têtes 26 et 39 octets (3) · octets par flux, par lot`
- **T1** `un code unique planté dans une botte de foin, à trois profondeurs (10 %, 50 %,`
- **T1** `90 %), et une question à la fin. Qwen2.5-0.5B Q8_0, `--infer`, 12 jetons, `temp 0` :`
- **T1** `| longueur | profondeur 10 % | 50 % | 90 % |`
- **T1** `| longueur | profondeur 10 % | 50 % | 90 % | durées |`
- **T1** `**12 sondes sur 12** trouvées, à toutes les profondeurs — y compris à 90 % de la`
- **T1** `reports/rapport-cerveau-corrections.md:166:  leave-one-code-out exact **0** ; coordonnées 0 % sur codes neufs.`
- **T1** `reports/rapport-coherence-docs.md:248:| OK | **17** | formats des modes 2 et 3 · `flux_brut` · `hôte:port` · trace dense 66 370 408 o (fichier réellement relu) · 66 370 406 hors sentinelle · 24 576 li`
- **T1** `reports/rapport-hybride.md:35:| codec + contexte | 528 / 528 | **100 %** | corpus B5/B7 |`
- **T1** `reports/rapport-hybride.md:42:- Le **codec avec contexte** est le **meilleur bloc linguistique** du corpus : 100 % de lecture, déterministe.`
- **T1** `reports/rapport-cycle-c2.md:153:* **et l'entraînement RÉDUIT λ sans le soumettre** : **206 → 136**, soit **−34 %** ✓ — ce qui explique`
- **T1** `1. **L'état porte le sens** : 16 jetons d'avance à **80,3 %**, quand le mot est à **118,4 %**.`
- **T1** `| **réinjecter l'état brut** | la prédiction détruit de 5 ordres de grandeur (×30 000) | et **normer n'y change rien** : ce n'est pas l'échelle |`
- **T1** `| **apprendre un pont** | l'état mappé bat le mot (68,6 % contre 122,9 %) | la sortie prélinguistique **dit mieux** que le **jeton de sortie** |`
- **T1** `| **la cause** | déplacement 44,8 % contre 77,5 % | les modèles plats ont appris un **point fixe** |`
- **T1** `1. **l'état porte le sens** : 16 jetons d'avance à **80,3 %**, quand le mot est à **118,4 %** — 38 points`
- **T1** `d'écart ; et l'empreinte de copie à **49,3 % contre 76,9 %** en lecture (trois exécutions) ;`
- **T1** `| le raisonnement synthétique est-il dans l'état ? | 125 | oui : 1,00 → 0,51 (FR), 1,00 → 0,53 (EN), hasard 5 % |`
- **T2** `docs/theorie/carte.md:36:| **A7** la grappe déportée | **fait** — relais 42,5477, grappe 21 %, transport 4,22× | [la roadmap](../pilotage/roadmap.md) |`
- **T2** `docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md:153:| `tools/profil_flux.py` | densité par couche, part des 10 % les plus forts, export CSV | `docs/pilotage/roadmap.md:129-149` |`
- **T2** `docs/theorie/glossaire/05-flux-protocole-et-transport.md:74:16,1 ms (`docs/pilotage/roadmap.md:113`, `docs/colab-reparti.md:30`).`
- **T2** `docs/theorie/glossaire/08-points-releves-non-corriges.md:115:    **+8 % de temps** et 258 ko/jeton (`docs/pilotage/roadmap.md:15`). Les deux chiffres sont`
- **T2** `docs/theorie/glossaire/entrees/nagle-ack-differe-tcpnodelay.md:4:> **Fiche glossaire — Nagle · ACK différé · TCPNODELAY.** Nagle est l'algorithme TCP qui retient les petites écritures en espérant en g`
- **T2** `> fichier de 179 Ko, et des **dates dans le futur** (jusqu'au 12 octobre 2026, alors que le travail`
- **T2** `journal/2026-10-28/apprentissage.md:13:| 13:06 | `8b5e3f39` | N2.4 — TÊTES DANS LA DISTILLATION : PPL 3,295, PAS DE GAIN ; TÊTE 3 62,98 % > PRINCIPALE 62,35 % | `en-cours.md`, `roadmap-native.md`, `20`
- **T2** `journal/2026-10-28/distribue.md:12:| 11:32 | `8af5a4b8` | N1.6 — PONT DE RÉGION : PPL 3,465, NEUTRALISÉ 4,080, EFFET −9,3 % | `en-cours.md`, `roadmap-native.md`, `2026-10-28.md` (+6) |`
- **T2** `journal/2026-10-28/distribue.md:16:| 14:29 | `a86faa71` | N2.5b — CAPACITÉ À BUDGET ÉGAL : 21,63 M 4,294 CONTRE 11,47 M 4,476, −4,1 % | `en-cours.md`, `roadmap-native.md`, `README.md` (+4) |`
- **T2** `journal/2026-10-28/distribue.md:17:| 15:09 | `9cd78139` | N2.5b — CAPACITÉ À BUDGET ÉGAL, 3 GRAINES : 21,63 M 4,142 CONTRE 11,47 M 4,507 (−8,1 %) | `en-cours.md`, `roadmap-native.md`, `README.md` (+3)`
- **T2** `docs/pilotage/roadmap.md:159:| **R0.2** | **contrôleur de lecture** : `survol`, `balayage`, `lecture`, `relecture`, `arrêt` ; budget en événements/paires ; classique d'abord (TOC, titres, premières/de`
- **T2** `docs/theorie/lecture-rapide.md:136:- **Porte** : à 30 % du budget, le contrôleur retrouve ≥ 90 % de la réponse de la lecture intégrale sur **trois`
- **T2** `docs/pilotage/backlog/R01-graphe-document.md:48:3. construire le corpus de 30 documents annotés (6 types × 5)`
- **T2** `docs/pilotage/backlog/R03-banc-lecture-rapide.md:15:| **entrée** | 30 documents (5 types × 6), 10 questions/spans gold par document, 4 modes de lecture |`
- **T2** `docs/pilotage/backlog/R03-banc-lecture-rapide.md:46:1. construire le corpus et les questions (6 types × 5 × 10)`
- **T2** `docs/pilotage/backlog/R01-graphe-document.md:48:3. construire le corpus de 30 documents annotés (5 types × 6)`
- **T2** `docs/pilotage/backlog/R03-banc-lecture-rapide.md:46:1. construire le corpus et les questions (5 types × 6 × 10)`
- **T2** `docs/pilotage/backlog/N2-distillation.md:13:49 999 fenêtres, 4 sources ; professeur 30k 1,734 (0,794 bit/octet) ; student 3,123 à 20 000 pas ; meilleur 2,6998 ; plateau 2,708. Le 21,63 M à budget égal`
- **T2** `[still running after 60000ms; moved to background job bash-93]`
- **T3** `| 00:37 | `8e0477ef` | N2.17 — 30 000 PAS DE PLUS : PPL 2,726, PRÉCISION 72,34 % |`
- **T3** `| 01:14 | `fb8cdc37` | N2.18 — 30 000 PAS DE PLUS : PPL 2,714, PRÉCISION 72,62 % |`
- **T3** `| 01:51 | `096747cc` | N2.19 — 30 000 PAS DE PLUS : PPL 2,708, PRÉCISION 72,80 % |`
- **T3** `| 04:05 | `a2cc7311` | N4.5 — MEILLEUR STUDENT SERVI : PPL 2,708, 53 OCTETS EN 589,2 MS |`
- **T3** `1. **Maturité.** 803 issues ouvertes, énormément de PR communautaires non mergées, `health_percentage` 71 % (pas de CONTRIBUTING, pas de templates d'issue). Plusieurs contributeurs mentionnent des **f`
- **T3** `| `04ed1834` | 2026-10-08 09:21 | 0.3 Mo | 67 Ko | 1 | 27 | 42 | 0 | 0 |`
- **T3** `| `11b2d312` | 2026-10-01 02:56 | 0.5 Mo | 82 Ko | 1 | 42 | 60 | 0 | 0 |`
- **T3** `| `13446299` | 2026-10-01 01:07 | 0.5 Mo | 84 Ko | 1 | 50 | 68 | 0 | 0 |`
- **T3** `| `15fd322f` | 2026-09-30 12:00 | 0.6 Mo | 66 Ko | 1 | 57 | 67 | 0 | 0 |`
- **T3** `| `1820cf6b` | 2026-10-02 19:36 | 0.3 Mo | 30 Ko | 1 | 23 | 21 | 0 | 0 |`
- **T3** `| `18b8879c` | 2026-10-02 15:12 | 0.4 Mo | 78 Ko | 1 | 33 | 55 | 3 | 0 |`
- **T3** `| `18c3f6d0` | 2026-10-01 05:26 | 0.3 Mo | 51 Ko | 1 | 26 | 38 | 0 | 0 |`
- **T3** `| `1966e052` | 2026-10-08 09:20 | 0.3 Mo | 57 Ko | 1 | 22 | 33 | 0 | 0 |`
- **T3** `| `22bcae27` | 2026-09-28 14:45 | 14.8 Mo | 1398 Ko | 54 | 1250 | 1227 | 19 | 4 |`
- **T3** `| `27c99b10` | 2026-09-25 19:50 | 1.0 Mo | 61 Ko | 1 | 57 | 54 | 1 | 0 |`
- **T3** `| `2c2a6595` | 2026-10-02 15:11 | 0.4 Mo | 66 Ko | 1 | 29 | 44 | 0 | 0 |`
- **T3** `| `31f26a6e` | 2026-10-02 19:48 | 0.9 Mo | 171 Ko | 1 | 85 | 111 | 0 | 0 |`
- **T3** `| `34e1d4be` | 2026-10-02 10:00 | 0.6 Mo | 105 Ko | 1 | 38 | 53 | 0 | 0 |`
- **T3** `| `3d5618a0` | 2026-10-02 15:18 | 1.1 Mo | 387 Ko | 1 | 73 | 85 | 1 | 0 |`
- **T3** `| `42059fde` | 2026-09-30 12:32 | 1.0 Mo | 158 Ko | 1 | 112 | 157 | 1 | 0 |`
- **T3** `| `482522d1` | 2026-10-08 09:23 | 0.5 Mo | 138 Ko | 1 | 54 | 58 | 0 | 0 |`
- **T3** `| `48ec07ab` | 2026-10-08 09:23 | 0.5 Mo | 121 Ko | 1 | 50 | 62 | 0 | 0 |`
- **T3** `| `4b146dfd` | 2026-10-02 09:57 | 0.4 Mo | 47 Ko | 1 | 18 | 23 | 0 | 0 |`
- **T3** `| `4d7a793b` | 2026-09-30 23:15 | 0.7 Mo | 93 Ko | 1 | 43 | 63 | 0 | 0 |`
- **T3** `| `4e786d3f` | 2026-10-02 10:18 | 0.8 Mo | 178 Ko | 1 | 80 | 129 | 0 | 0 |`
- **T3** `| `5185ccb1` | 2026-09-30 17:27 | 1.2 Mo | 158 Ko | 1 | 102 | 123 | 0 | 0 |`
- **T3** `| `564fbe3a` | 2026-09-30 18:14 | 0.7 Mo | 60 Ko | 1 | 25 | 35 | 0 | 0 |`
- … (tronqué)

## 5. Erreurs rencontrées

21 sorties en erreur ou divergentes. Les premières :

- **T2** : --- #!/bin/bash # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait. # # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS # (`--attn-window` 
- **T5** : thread 'main' (3499374) panicked at src/main.rs:400:35: ouverture du GGUF: Os { code: 2, kind: NotFound, message: "No such file or directory" } note: run with `RUST_BACKTRACE=1` environment variable t
- **T5** : == conversion GGUF -> DRVM ==   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/gguf_drvm.py", line 20, in <module>     from tools.convertir_clusters import lire_entete, parcourir_kv Modul
- **T7** : [stderr] Traceback (most recent call last):   File "<stdin>", line 1, in <module> ModuleNotFoundError: No module named 'semantique' [exit code: 1]
- **T14** : # Index des fiches de reports/  > **Généré** par `tools/index_reports.py` — **278 fiches**. Les fichiers > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ; > la page
- **T15** : --- ### docs/pilotage/backlog/A2.6* ### docs/pilotage/backlog/A3.2* ### docs/pilotage/backlog/A3.3* [stderr] sed: can't read docs/pilotage/backlog/A2.6*: No such file or directory sed: can't read docs
- **T16** : [stderr]   File "<stdin>", line 5     new='''echo "  ✅ pont entier identique dans les deux encodages"         ^ SyntaxError: unterminated triple-quoted string literal (detected at line 14) bash: line 
- **T16** : ],   "liens": [ {"de": "local", "vers": "distant", "mode": "listes", "delai_ms": 0} ] } JSON  echo "=== 1. référence : le modèle entier ===" $D "$M" --ppl "$IDS" --limit "$LIMITE" --ctx 256 --threads 
- **T17** : (no output) [exit code: 2]
- **T19** : (corpus  absent — régénéré depuis data/wikitext2_test.txt, bit à bit identique)   ❌ corpus  absent ET non régénérable (data/wikitext2_test.txt manquant ?) [exit code: 2]
- **T20** : params 24652 [drvm-serve] http://127.0.0.1:62123 · 11 M natif, cache par requête --- gen  --- log [drvm-serve] http://127.0.0.1:62123 · 11 M natif, cache par requête  thread 'main' (676820) panicked a
- **T20** : params 88140  --- log [drvm-serve] http://127.0.0.1:62124 · 11 M natif, cache par requête  thread 'main' (677330) panicked at src/native.rs:216:34: index out of bounds: the len is 2048 but the index i
- **T28** : 0.005 12 0 0.01 11 1 0.02 0 12 0.05 0 12 0.1 0 12 0.2 0 12 [exit code: 143]
- **T35** : 2539 docs/pilotage/references-non-regression.md # Références de non-régression  > **Dernière passe complète — 2026-10-29 à 22 h 09 :** > **62 portes, 60 vertes, 2 rouges, 1 h 46**. Les deux rouges son
- **T43** : error[E0502]: cannot borrow `logits` as immutable because it is also borrowed as mutable    --> src/main.rs:303:27     | 296 |         let mut envoyer = |id: u32, pos: usize, s: &mut std::net::TcpStre

## 6. Commits

- DOCS — UNE ROADMAP UNIQUE (A/B/N/R), ANALYSE LECTURE RAPIDE, BACKLOG 29 FICHES" 2>&1 | tail -20; echo '---'; git log -1 --format='%h %ad %s' --date=short; echo 
- ps -eo pid,ppid,etime,cmd | grep -E 'git commit|git add|session_report|journal_auto' | grep -v grep | head -10; echo '---'; git log -2 --format='%h %ad %s' --da
- for i in $(seq 1 90); do if ! pgrep -f 'git commit -q -m DOCS — GRAPHE' >/dev/null 2>&1; then echo 'commit process finished'; break; fi; sleep 2; done; echo '--
- DOCS — EN-COURS MULTI-SESSIONS (3 SESSIONS), BLOQUANTS PAR CHANTIER, TRANSFERT AU JOURNAL" 2>&1 | tail -8; echo '---'; git log -2 --format='%h %ad %s' --date=sh
- git add docs/pilotage/en-cours.md && git commit --amend --no-edit 2>&1 | tail -6; echo '---'; git log -2 --format='%h %ad %s' --date=short; echo '---'; git stat
- DOCS — GLOSSAIRE 12 (27 TERMES DE LECTURE), BACKLOG LIÉ AU GLOSSAIRE" 2>&1 | tail -8; echo '---'; git log -2 --format='%h %ad %s' --date=short; echo '---'; git 
- N0.3b — PARITÉ PPL DRVM ↔ GGUF CLOSE : 68,1917 / 92,1875 (CONVERSION), 4,6585 / 18,6394 (NATIF)" 2>&1 | tail -8; echo '---'; git log -2 --format='%h %ad %s' --d
- DOCS — REPORTS/README SOUS BUDGET : 1 724 MOTS, INDEX EXHAUSTIF RENVOYÉ" 2>&1 | tail -8; echo '---'; git log -2 --format='%h %ad %s' --date=short; echo '---'; g
- python3 - <<'PY' import pathlib p=pathlib.Path('reports/README.md'); t=p.read_text() old="Les JSON de campagne (`traduction-*`, `kfold-*`, `contamination-*`, `p
- B12.10 — LE CONTEXTE DU PIPELINE ÉTAIT UNE CHAÎNE : 0/528 → 528/528 ; N0.3b CLOSE" 2>&1 | tail -8; echo '---'; git log -2 --format='%h %ad %s' --date=short; ech
- python3 - <<'PY' import pathlib p=pathlib.Path('docs/pilotage/en-cours.md'); t=p.read_text() t=t.replace("elle passe à **B12.10** — le contexte du pipeline (cha
- B12.10 — SPLIT PAR CODE TENU À L'ÉCART : 0 EXACT, 0,436 DE CHAMP, M4 NON BRANCHÉ" 2>&1 | tail -6; echo '---'; git log -1 --format='%h %ad %s' --date=short
- B12.10 — LE BRANCHEMENT M4 PAR CHAMPS OBSERVÉS EST INERTE : RETIRÉ, MARGE À ESSAYER" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short
- B12.10 — ORACLE = M8, M4 SEUL = 0/606 : LA PORTE « M4 RETIRÉ » EST VIDE ; CLOSE NÉGATIVE" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=sho
- ÉTAT — LE GRAPHE DES CHANTIERS, ACTIVITÉS ET ÉTATS DANS EN-COURS" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; git status --short |
- cd /tmp/qtrinet-patch && python3 - <<'PY' import pathlib # --- AGENTS.md : règle 11 --- p=pathlib.Path('AGENTS.md'); t=p.read_text() needle="""## 3. Routage : l
- MÉTHODE — IDENTITÉ DSH, PAIRS ET DISCIPLINE GIT ; 71d57f53 INSCRIT" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; echo '---'; git st
- B11.10 — CARTES 161/161, AMBIGUÏTÉS REFUSÉES : LE 69,3 % EST NATIF" 2>&1 | tail -6; echo '---'; git log -1 --format='%h %ad %s' --date=short; echo '---'; git sh
- A8.0 — 0 PORTE SUR 33 N'ÉPINGLE UNE PPL : A8.3 RESTE OPT-IN" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; echo '---'; git status --
- A8.0 — PORTE-FLUX ÉPINGLÉE : PPL 61,9920 / 60,8135, TOLÉRANCE 5e-4" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short
- A8.0 — PORTE-PONT ÉPINGLÉE : PPL 113,0068 / 111,9225, FALAISE +2,81 % / +25,35 %" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short
- ÉTAT — B11.10 MESURÉE, A8.0 2/33 ; 71d57f53 ACTIVE" 2>&1 | tail -6; echo '---'; git log -1 --format='%h %ad %s' --date=short; echo '---'; git show --stat --onel
- A8.0 — PORTE-TOPOLOGIE ÉPINGLÉE : 17,4702 / 30,4363 / 42,5477 ; ÉTAT 3/33" 2>&1 | tail -6; echo '---'; git log -1 --format='%h %ad %s' --date=short; echo '---';
- A8.0 — PORTE-TOPOLOGIE ÉPINGLÉE : 17,4702 / 30,4363 / 42,5477 ; ÉTAT 3/33" 2>&1 | tail -6; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 too
- A8.0 — PORTE-COUPE ÉPINGLÉE : 113,0068 / +0,52…+17,09 % ; ÉTAT 4/33" 2>&1 | tail -6; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/ver
- A8.0 — PORTE-COUPE ÉPINGLÉE : PPL 113,0068, COÛTS +0,52…+17,09 %" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'; git status --short | grep -E 'a80-por
- A8.0 — AUDIT PPL : 4 PORTES SUR 33 ÉPINGLÉES" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'; python3 tools/verifie_etat_a_jour.py 2>&1 | tail -2
- A2.6 — PARTIEL : TÊTE REFUSÉE, EXPERTS BLOQUÉS A6.2 ; A3.2/A3.3 MESURÉES" 2>&1 | tail -6; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tool
- A2.6 — PARTIEL : TÊTE REFUSÉE, EXPERTS BLOQUÉS A6.2 ; A3.2/A3.3 MESURÉES" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tool
- R13.0 — BPE 3,4–5,2 OCTETS/JETON, RÉVERSIBLE ; PPL À MESURER" 2>&1 | tail -6; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie_et
- A8.0 — PORTE-REPARTI ÉPINGLÉE : PPL 9,1748 ; ÉTAT 5/33" 2>&1 | tail -6; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie_etat_a_j
- A8.0 — PORTE-REPARTI ÉPINGLÉE : PPL 9,1748 ; ÉTAT 5/33" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie_etat_a_j
- A8.0 — PORTE-BUDGET ÉPINGLÉE : PPL 111,9225 ; ÉTAT 6/33" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie_etat_a_
- A8.3a — PORTE-FLUX : RÉGIME 1 % ÉPINGLÉ (58,3200 / 62,7357)" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie_eta
- A8.3a — PORTE-PONT : RÉGIME 1 % ÉPINGLÉ (111,8003 / 115,6406, +5,88/+25,75)" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 t
- A8.3a — PORTE-COUPE : RÉGIME 1 % ÉPINGLÉ (111,8003 ; VARIANCE 2,4 %)" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/ve
- A8.0 — PORTE-ADAPTATEUR ÉPINGLÉE : 17,4315 / 2 687 292,8165 ; ÉTAT 7/33" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools
- B10.2bis — TABLEAU : COLONNE GRAINE VIDE AJOUTÉE" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie_etat_a_jour.py
- B10.2bis — TABLEAUX : COLONNE GRAINE VIDE AJOUTÉE (6 LIGNES)" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short
- A8.0 — PORTE-GAIN ÉPINGLÉE : 14,6496 / 12,9635 / 996,0390 ; ÉTAT 8/33" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/v
- R13.1 — PPL BPE-NATIVE : CONDITION NOMMÉE (PAS DE MODÈLE BPE NATIF)" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/ver
- N3.1 — INVENTAIRE : PAS DE PORTE COMPOSÉE AVANT SERVICE/K-WTA" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie_e
- N3.1 — CORRECTION : LA PROFONDEUR ROUTÉE A UNE PORTE ; A8.0 = 8" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie
- A8.0 — PORTE-CYCLE-C2 ÉPINGLÉE : 14,6496 ; ÉTAT 9/33" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie_etat_a_jou
- A8.3b — LE SIGNE VIENT DU CHEMIN LOT (1 vs ≥2), PAS DE LA TAILLE" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifi
- N3.2a — LE SERVICE NATIF VIT : /SANTE, GÉNÉRATION DÉTERMINISTE, 404 ; PORTE 59" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python
- N3.3a — ROUTAGE/K-WTA VIVANT : MÊMES POIDS, CONFIG DIFFÉRENTE, SORTIE DIFFÉRENTE ; PORTE 60" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=
- A8.0 — PORTE-CONSOLIDATION ÉPINGLÉE : 17,4268 / 17,1655 ; ÉTAT 10/33" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/ve
- B10.2bis — TABLEAUX : COLONNE GRAINE VIDE AJOUTÉE (6 LIGNES)" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie_et
- B10.2bis — TABLEAUX : COLONNE GRAINE VIDE AJOUTÉE (3 LIGNES)" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie_et
- N3.2b0 — PROFONDEUR DE SERVICE + LECTURE HTTP COMPLÈTE ; PORTE 61" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verif
- N3.3b — KWTA ET TOP_K AGISSENT SÉPARÉMENT ; PORTE 62" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie_etat_a_jou
- N3.3b — KWTA ET TOP_K AGISSENT SÉPARÉMENT ; PORTE 62" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie_etat_a_jou
- N3.3c — LE MOTEUR COMPTE LES EXPERTS/CANAUX : 6/6/3 · 48/24/24 ; PORTE 63" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 too
- N3.4a — SERVICE + PROFONDEUR + ROUTAGE + COMPTAGE COMPOSÉS ; PORTE 64" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/v
- A8.0 — PORTE-FUSION ÉPINGLÉE : 113,0068 ; ÉTAT 11/33" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie_etat_a_jou
- N3.2b1 — SEUIL DE CONFIANCE DANS LE SERVICE : 12/0, 0/12, 11/1 ; PORTE 65" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 too
- N3.2b2 — LE SAUT DE CALCUL N'EST PAS GRATUIT : 5,2 → 2,0 MS, SORTIE DIFFÉRENTE ; PORTE 66" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=sh
- N3.4b — LE PONT NATIF AGIT : 4 160 POIDS NULS, SORTIE DIFFÉRENTE ; PORTE 67" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 t
- A8.0 — PORTE-TRACE ÉPINGLÉE : 59,0790 ; ÉTAT 12/33" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie_etat_a_jour.
- A8.0 — PORTE-REFLEXE ÉPINGLÉE : 11 163 272,0495 ; ÉTAT 13/33" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie_et
- N3.4c — LE PLACEMENT NATIF EST UNE MÉTADONNÉE, PAS UN CHEMIN ; PORTE 68" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools
- A8.0 — PORTE-C4-RETARD ÉPINGLÉE : 14,6496 / 9 277,9771 / 151 517 ; ÉTAT 14/33" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3
- N3.4d — COUVERTURE N3 PAR BRIQUE : COMPOSITION NATIVE = CONDITION" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verif
- ÉTAT — A8.0 RÉCONCILIÉ À 14 PORTES" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'; python3 tools/verifie_etat_a_jour.py 2>&1 | tail -2
- A8.0 — PORTE-BUS ÉPINGLÉE : 64,1160 / 59,0790 / 66,0379 ; ÉTAT 15/33" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/ve
- A8.0 — PORTE-DELAIS ÉPINGLÉE : 59,0790 ; ÉTAT 16/33" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'
- A8.0 — PORTE-DELAIS ÉPINGLÉE : 59,0790 ; ÉTAT 16/33" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'; python3 tools/verifie_etat_a_jour.py 2>&1 | tail -
- DOCS — RÉFÉRENCES : PASSE DUPLIQUÉE RETIRÉE (T1 2 500)" 2>&1 | tail -4; echo '---'; git log -2 --format='%h %ad %s' --date=short; python3 tools/verifie_etat_a_j
- A8.0 — PORTE-BUS-SOCKET ÉPINGLÉE : 113,0068 / 148,7080 / 42,3176 / 148,9144 ; ÉTAT 17/33" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'
- A8.3c.1 — LE SIGNE NE DÉPEND PAS DU CONTEXTE : 24 MESURES, ctx 64/256/512 IDENTIQUES" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'; python3 tools/ver
- C11 — LA PANNE NOMME RÉGION, PAS ET OCTETS : PORTE-PANNES VERTE" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'
- R13.1 — LE BPE NATIF BAT L'OCTET : 3,249 CONTRE 3,689 BITS/OCTET, −11,9 % À OCTETS ÉGAUX" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %s'; python3 tools
- N3.5a — DÉCOUPAGE 0..k / k..n BIT-EXACT, K=0..4 ; 2 BUGS LATENTS CORRIGÉS ; PORTE 70" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %s'; python3 tools/ver
- A8.0 — PORTE-PROFONDEUR ÉPINGLÉE : 14,6496 ; ÉTAT 18/33" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'
- R13.1 — CORRECTION D'AUDIT : 11,0 % BITS/OCTET EXACT (VAL), PAS 11,9 %" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'
- N3.5b — DEUX PROCESSUS, FRONTIÈRE PAR FICHIER : LOGITS IDENTIQUES ; PORTE 71" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %s'; python3 tools/verifie_eta
- N3.5c — DEUX PROCESSUS TCP, AUCUN CACHE SUR LE FIL : LOGITS IDENTIQUES ; PORTE 72" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'
- A8.3b/c — DÉCISION : OPT-IN, CAUSE = CHEMIN LOT, CACHE INNOCENTÉ" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'
- N3.5d — L'EMPREINTE REFUSE UN AVAL DIVERGENT (CODE 4) ; PORTE 73" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'; python3 tools/verifie_etat_a_jour.py 
- N3.5e — GÉNÉRATION RÉPARTIE TCP, DEUX CACHES, BIT-IDENTIQUE ; PORTE 74" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'
- B11.10a — 4/4 ROUTÉES, 3/4 LUES : E4 EXIGE UNE POSITION" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/revue_documenta
- ÉTAT — DATE ALIGNÉE SUR LE DERNIER COMMIT" 2>&1 | tail -3; echo '---'; git log -1 --format='%h %ad %s' --date=short; python3 tools/verifie_etat_a_jour.py 2>&1 |
- B11.10b — L'INDICE DE JEU STRIPPÉ : 4/4 ROUTÉES, 3/4 LUES ; PORTE 75" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'
- B11.10c — E4 = REQUÊTE DE CASE : 4/4 ROUTÉES ET LUES" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'
- A8.0 — PORTE-MELANGE : ROUGE STRUCTURELLE QUALIFIÉE, PAS MAQUILLÉE" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'
- ÉTAT — T0 4 000 : MÉLANGE ROUGE QUALIFIÉ" 2>&1 | tail -3; echo '---'; python3 tools/verifie_etat_a_jour.py 2>&1 | tail -2
- R13.1 — À OCTETS ÉGAUX LE BPE PERD 0,7 % : LE PILOTE 11 % NE SE REPRODUIT PAS" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %s'; python3 tools/verifie_et
- R13.2 + A8.0 — VOCAB 1024 PERD 3,9 % À OCTETS ÉGAUX ; PORTE-INDICE ROUGE QUALIFIÉE" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %s'; python3 tools/verif
- ÉTAT — DATE ALIGNÉE SUR LE COMMIT DU 30" 2>&1 | tail -3; echo '---'; python3 tools/verifie_etat_a_jour.py 2>&1 | tail -2; git log -1 --format='%h %ad %s' --date
- N3.5f — POSITION VÉRIFIÉE PAS À PAS, DÉSYNC REFUSÉE (CODE 4) ; PORTE 76" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'; python3 tools/verifie_etat_a_j
- R13.3 — ANGLAIS 100 MO : LE BPE PERD 4,2/6,6 % À OCTETS ÉGAUX" 2>&1 | tail -5; echo '---'; git show --stat --oneline HEAD | head -10
- A8.0 — 19/33 : PORTE-PANNES ÉPINGLÉE À 33,0156 ; AUDIT FINAL DES 14 RESTANTES" 2>&1 | tail -5; echo '---'; git log -1 --format='%h %s'; python3 tools/verifie_et
- SESSIONS — LE PLAN AVANT L'ÉTAT : LINTER, MODÈLE, PORTE 78" 2>&1 | tail -6; echo '---'; git log -1 --format='%h %s'; python3 tools/verifie_etat_a_jour.py 2>&1 |
- SESSIONS — MIGRATION DOUCE : 3 PLANS À CONFIRMER, STRICT ROUGE, EN-COURS RECALÉ" 2>&1 | tail -6; echo '---'; git log -1 --format='%h %s'; python3 tools/verifie_
- ÉTAT — WBS 13:00, B11.10 4/4" 2>&1 | tail -4; echo '---'; python3 tools/verifie_etat_a_jour.py 2>&1 | tail -2; git log -2 --format='%h %s'
- R13.4 — DEUX GRAINES : BPE512 DANS LE BRUIT, BPE1024 PERD 4,09 %" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'; python3 tools/verifie_etat_a_jour.py 
- DOCS — CONTINUITÉ 1 134 MOTS, ORGANISATION 1 579 : T0 3 989" 2>&1 | tail -4; echo '---'; git log -1 --format='%h %s'; python3 tools/verifie_etat_a_jour.py 2>&1 

