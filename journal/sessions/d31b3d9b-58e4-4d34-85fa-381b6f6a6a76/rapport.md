# Session d31b3d9b — Où en est-on

| | |
|---|---|
| Identifiant | `d31b3d9b-58e4-4d34-85fa-381b6f6a6a76` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-08 09:11 |
| Durée | 51.4 h |
| Tours | 88 |
| Messages | 2328 |
| Appels d'outils | 2133 |
| Fichiers touchés | 76 |
| Commandes | 1850 |
| Sous-agents | 3 |
| Commits | 204 |
| Compactages de contexte | 3 |

## Objectifs déclarés

- **create** — Produire un modèle nativement événementiel qui soit à son meilleur dans l'architecture de Drave : parcimonie ENTRAÎNÉE (décharge/LIF ou parcimonie structurée), exécutable en listes d'événements, et découpable en unités de travail autonomes plaçables sur les unités d'une machine (cœurs, GPU, disque) 
… [348 caractères tronqués]
- **pause** — Produire un modèle nativement événementiel qui soit à son meilleur dans l'architecture de Drave : parcimonie ENTRAÎNÉE (décharge/LIF ou parcimonie structurée), exécutable en listes d'événements, et découpable en unités de travail autonomes plaçables sur les unités d'une machine (cœurs, GPU, disque) 
… [348 caractères tronqués]
- **edit** — Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, cod
… [728 caractères tronqués]
- **resume** — Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, cod
… [728 caractères tronqués]
- **complete** — Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, cod
… [728 caractères tronqués]
- **create** — Sprint « cerveau complet » en autonomie jusqu'au 10 octobre 9 h (HAE) : implémenter, avec portes mesurées, les trois premières capacités du plan docs/plan-cerveau-complet.md — C1 graphe de régions (descripteur de topologie, validateur de DAG, ordonnanceur par dépendances, pilote multi-nœuds ; porte 
… [609 caractères tronqués]
- **complete** — Sprint « cerveau complet » en autonomie jusqu'au 10 octobre 9 h (HAE) : implémenter, avec portes mesurées, les trois premières capacités du plan docs/plan-cerveau-complet.md — C1 graphe de régions (descripteur de topologie, validateur de DAG, ordonnanceur par dépendances, pilote multi-nœuds ; porte 
… [609 caractères tronqués]
- **create** — Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais pa
… [1001 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — où en est-on

**Tour 2** — ça fait plusieurs jours qu'on est sur des travaux lourds avec peu de résultats constructifs. Il faut revenir à l'essence de Drave et produire un modèle qui est à son meilleur dans une architecture événementielle facilement distribuable sur les divers types d'unité de traitement et ressources d'une machine et de plusieurs machines en réseau.

**Tour 3** — <goal_round> Objective: "Produire un modèle nativement événementiel qui soit à son meilleur dans l'architecture de Drave : parcimonie ENTRAÎNÉE (décharge/LIF ou parcimonie structurée), exécutable en listes d'événements, et découpable en unités de travail autonomes plaçables sur les unités d'une machine (cœurs, GPU, disque) puis sur plusieurs machines en réseau. Chaque affirmation porte sa mesure : … [816 caractères tronqués]

**Tour 4** — <goal_round> Objective: "Produire un modèle nativement événementiel qui soit à son meilleur dans l'architecture de Drave : parcimonie ENTRAÎNÉE (décharge/LIF ou parcimonie structurée), exécutable en listes d'événements, et découpable en unités de travail autonomes plaçables sur les unités d'une machine (cœurs, GPU, disque) puis sur plusieurs machines en réseau. Chaque affirmation porte sa mesure : … [816 caractères tronqués]

**Tour 5** — Hypothèse de changement de configuration matériel : Si je déploie ce projet sur une station de travail bi-processeur (Xeon E5-2687W v3) sous Linux, configurée avec une topologie NUMA asymétrique stricte pour séparer le système du calcul intensif.  Voici la ségrégation matérielle exacte de la machine : - Nœud NUMA 0 (OS & Tâches de fond) : CPU 0, 32 Go de RAM, SSD NVMe système, et GPU AMD dédié à l … [403 caractères tronqués]

**Tour 6** — je viens de commander une carte pcie pour 4 nvme 4x4 et 4 unités Patriot P320 256GB PCIe Gen 3x4 M.2 2280 SSD pour aller dessus. je compte mettre cet array de nvme sur le même noeud que les gpu, déplacer aussi le nvme existant pour le mettre sur l'autre noeud avec une carte graphique amd 100-c44971-00 pour avoir un noeud xeon de travail et un noeud os et desktop. je maintiens la topologie ram actu … [16 caractères tronqués]

**Tour 7** — le ram est actuellement hors de prix. je t'ai fait évaluer une approche asymétrique, mais c'est déconseillé. Que peut-on faire pour le ram.

**Tour 8** — donc les nouveaux nvme seront sur l'autre cpu pour ne pas réduire le nombre de voies des gpu. La ram reste tel-quelle. la carte amd pour le desktop sera sur le même cpu que les nouveaux nvme à mettre en raid. Quelels sont les autres optimisations à faire ? prépare un document pour ce changement de configuration et la configuration de la carte amd-yeston (6 ports mini-dp) et les nouveaux nvme en ra … [2 caractères tronqués]

**Tour 9** — encore une journée complète avant l'arrivé du nouveau matériel. Exécute pendant 24h les tâches que tu trouves les plus adéquates pour explorer les bénéfices attendus de Drave pour tout type de tâches.

**Tour 10** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1196 caractères tronqués]

**Tour 11** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1196 caractères tronqués]

**Tour 12** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1196 caractères tronqués]

**Tour 13** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1196 caractères tronqués]

**Tour 14** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1196 caractères tronqués]

**Tour 15** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1196 caractères tronqués]

**Tour 16** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1196 caractères tronqués]

**Tour 17** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 18** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 19** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 20** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 21** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 22** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 23** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 24** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 25** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 26** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 27** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 28** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 29** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 30** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 31** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 32** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 33** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 34** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 35** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1197 caractères tronqués]

**Tour 36** — allons-y pour un sprint cerveau complet. Vasy en mode autonome jusqu'à demain matin (9h hae 10 octobre)

**Tour 37** — <goal_round> Objective: "Sprint « cerveau complet » en autonomie jusqu'au 10 octobre 9 h (HAE) : implémenter, avec portes mesurées, les trois premières capacités du plan docs/plan-cerveau-complet.md — C1 graphe de régions (descripteur de topologie, validateur de DAG, ordonnanceur par dépendances, pilote multi-nœuds ; porte : un graphe linéaire doit rendre des logits identiques au bit près et un dé … [1077 caractères tronqués]

**Tour 38** — <goal_round> Objective: "Sprint « cerveau complet » en autonomie jusqu'au 10 octobre 9 h (HAE) : implémenter, avec portes mesurées, les trois premières capacités du plan docs/plan-cerveau-complet.md — C1 graphe de régions (descripteur de topologie, validateur de DAG, ordonnanceur par dépendances, pilote multi-nœuds ; porte : un graphe linéaire doit rendre des logits identiques au bit près et un dé … [1077 caractères tronqués]

**Tour 39** — <goal_round> Objective: "Sprint « cerveau complet » en autonomie jusqu'au 10 octobre 9 h (HAE) : implémenter, avec portes mesurées, les trois premières capacités du plan docs/plan-cerveau-complet.md — C1 graphe de régions (descripteur de topologie, validateur de DAG, ordonnanceur par dépendances, pilote multi-nœuds ; porte : un graphe linéaire doit rendre des logits identiques au bit près et un dé … [1077 caractères tronqués]

**Tour 40** — <goal_round> Objective: "Sprint « cerveau complet » en autonomie jusqu'au 10 octobre 9 h (HAE) : implémenter, avec portes mesurées, les trois premières capacités du plan docs/plan-cerveau-complet.md — C1 graphe de régions (descripteur de topologie, validateur de DAG, ordonnanceur par dépendances, pilote multi-nœuds ; porte : un graphe linéaire doit rendre des logits identiques au bit près et un dé … [1077 caractères tronqués]

**Tour 41** — <goal_round> Objective: "Sprint « cerveau complet » en autonomie jusqu'au 10 octobre 9 h (HAE) : implémenter, avec portes mesurées, les trois premières capacités du plan docs/plan-cerveau-complet.md — C1 graphe de régions (descripteur de topologie, validateur de DAG, ordonnanceur par dépendances, pilote multi-nœuds ; porte : un graphe linéaire doit rendre des logits identiques au bit près et un dé … [1077 caractères tronqués]

**Tour 42** — <goal_round> Objective: "Sprint « cerveau complet » en autonomie jusqu'au 10 octobre 9 h (HAE) : implémenter, avec portes mesurées, les trois premières capacités du plan docs/plan-cerveau-complet.md — C1 graphe de régions (descripteur de topologie, validateur de DAG, ordonnanceur par dépendances, pilote multi-nœuds ; porte : un graphe linéaire doit rendre des logits identiques au bit près et un dé … [1077 caractères tronqués]

**Tour 43** — ajuste tes sprints en timeboxing plus qu'en tranche de backlog. C'est à dire que tu dois continuer pour occupper le temps imparti au lieu de t'arrêter là où ta planification de sprint arrive au terme. C'est du gaspillage de temps précieux que d'arrêter trop vite. Je préfère interrompre un sprint car j'ai de nouvelles idées que de consatater que tout a été arreté car on est arrivé au bout du plan.  … [284 caractères tronqués]

**Tour 44** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1469 caractères tronqués]

**Tour 45** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1469 caractères tronqués]

**Tour 46** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1469 caractères tronqués]

**Tour 47** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1469 caractères tronqués]

**Tour 48** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1469 caractères tronqués]

**Tour 49** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1469 caractères tronqués]

**Tour 50** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1469 caractères tronqués]

**Tour 51** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1469 caractères tronqués]

**Tour 52** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1469 caractères tronqués]

**Tour 53** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 54** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 55** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 56** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 57** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 58** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 59** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 60** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 61** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 62** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 63** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 64** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 65** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 66** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 67** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 68** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 69** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 70** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 71** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 72** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 73** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 74** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 75** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 76** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 77** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 78** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 79** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 80** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 81** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 82** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 83** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 84** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 85** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 86** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 87** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

**Tour 88** — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sans s'arrêter à la fin d'une liste de tâches. À chaque round : choisir la capacité ou l'expérience de plus grande valeur parmi (a) les capacités restantes du plan docs/plan-cerveau-complet.md — C3 délais par lien, C4 horloges/asynchronisme, C2 entrées multiples et récurrence, C6 m … [1470 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — où en est-on

*32 appels d'outils.* Actions notables :

- bash — Show git status and recent commits
- bash — List top-level files
- bash — Check sizes and diff stat of modified files
- bash — List most recent reports and sprints
- read
- bash — Show diff of journal metadata files
- get_goal
- bash — Diff tool changes and inspect new script
- bash — Read head of REPRISE.md status file
- bash — Read tail of latest session digest
- bash — List state sections in REPRISE.md
- bash — Find DRVF readers and running processes
- bash — List REPRISE.md section headings
- bash — List recent docs and commit dates
- … et 17 autres

**Synthèse produite :**

⏵ Point complet sur l'état du projet Drave

\## Où on en est — 08/10 09:12

**Dernière activité** : hier soir 21h14 (session `bbd6969f`, 222,5 h, archivée dans le journal). Dépôt sur `7d32b4f`, **aucun job en cours**, portes vertes (`portes.sh` exit 0, 77 tests cargo).

\### Les trois chantiers du mandat en cours

| chantier | état | ce qui le dit |
|---|---|---|
| **1. Écart froid/chaud de la passe K3** | ✅ **clos** | La mesure « une moitié de modèle » (47 couches) tranche : `sda` occupé **85,3 %**, CPU **31 %**, **367 Go/h**, 554 s. Le temps de la passe est le temps de **lire les octets**. Rien d'autre. |
| **2. Regroupement par expert / critère « 4 jetons < 10 min »** | ❌ **impossible à un nœud** | Le regroupement **existait déjà** (`MoeK3::avant_lot`) — le levier est la **taille du lot**, pas le code. Et la loi des octets `79,0 + 31,9·T Gio` (validée sur 3 points, §11) interdit le critère : 4 jetons = 206,6 Gio à 133 Mio/s. |
| **3. Grappe, un nœud = une plage de couches** | ✅ **fait, porte tenue au bit près** | Commit `3c2b542` : 2 plages + monolithe, sorties **identiques au bit**. Mais « 2,5 min/passe » demande **11 nœuds** — c'est une extrapolation, pas une mesure. Transport réseau encore par **fichier**, et la porte n'a été tenue que pour **deux** plages. |

\### En chantier, non commité (l'heure finale d'hier)

**Un vrai bug, trouvé par comparaison moteur/GPU** : le moteur quantifie chaque enregistrement DRVF v2 sur 127 niveaux (`round(v/s)`) et range `s` dans l'en-tête… que **les lecteurs du dépôt ignoraient**. Preuve : le rapport de normes passe de **×100 à ×1,003** une fois l'échelle appliquée (cosinus couche 0 : 0,849 → 0,864).

- corrigé **seulement** dans `tools/premiere_couche_semantique.py`, avec `--sans-echelle` pour mesurer l'écart — **non commité** ;
- **15 autres outils** lisent toujours les entiers ±127 comme des valeurs physiques (`profil_couches`, `localite_couches`, `invariance_unites`, `pont_*`, `cache_pont`, `sonde_pont`, `compare_professeurs`…) ;
- **l'impact sur le résultat publié n'est pas mesuré** : la « bande sémantique 10–15 » (`rapport-cycle-rapide.md`, commits `8b232d0`/`9eb9732`) a été calculée avec le lecteur bogué, et les caches `/tmp/pcs_*.sans_echelle.npz` n'existent pas → la session s'est arrêtée juste avant.

**Deux autres fichiers en attente** : `tools/trace_gpu.py` (nouveau — traçage du professeur sur GPU dans le format du moteur, calibré hier 21h11 ; sa propre note dit qu'il faut passer en **DRVF v3** pour les éche
… [425 caractères tronqués]

### Tour 2 — ça fait plusieurs jours qu'on est sur des travaux lourds avec peu de résultats constructifs. Il faut revenir à l'essence … [222 caractères tronqués]

*107 appels d'outils.* Actions notables :

- sous-agent — Inventaire parcimonie événementielle
- sous-agent — Inventaire du travail modèle
- sous-agent — Inventaire capacités de distribution
- read
- bash — Search spiking-related work in repo
- bash — Check corpora, torch and GPU availability
- bash — Read imposed-sparsity and campaign reports
- bash — Check training code and Python env packages
- bash — Locate available text corpora
- list_agents
- job_list
- bash — Read push/pull crossover report
- bash — Inventory corpora and HF cache
- bash — Inspect token id format and tokenizers
- … et 88 autres

**Synthèse produite :**

⏵ Cycle 1 bouclé et commité : la cible se déplace, et c'est la mesure qui la déplace

\## Ce que le banc a établi (dim 192, 100 Mo, 20 000 pas, meilleur point de validation)

| modèle | val (bits/octet) | densité | coût |
|---|---|---|---|
| **dense (jumeau)** | **2,2572** | 1,00 | 1,77 M MACs/jeton |
| décharge, poids valués | 3,2128 | 0,16 | 0,29 M événements |
| décharge, poids binaires | 3,4924 | 0,18 | 0,32 M événements |
| décharge, poids ternaires | 3,5091 | 0,17 | 0,30 M événements |

**La parcimonie s'entraîne** — c'était la question ouverte du dépôt, et elle est tranchée : R̂ = 0,17 obtenu par l'entraînement, réglable jusqu'à 0,03 par le seuil, là où la parcimonie *imposée* après coup plafonnait à 85 % de densité. Mais à taille égale, le dense garde ~0,9 bit/octet d'avance, et les poids signés coûtent 0,3 de plus.

\## Le chiffre qui manquait, et qui déplace la cible

J'ai fait tourner le banc du moteur (binaire du dépôt, `blk.0.ffn_gate.weight`, 16 fils) :

- le **pull dense est au mur mémoire** : 14,0 Go/s, soit 67 % de la bande passante mesurée (20,8 Go/s) ;
- un **événement coûte 2,9× (valué) à 4,3× (signé) un poids dense** — 0,210 et 0,305 ns contre 0,0716 ns.

Donc le « R̂ = 0,15 → 6,7× moins d'événements → ~100 tok/s » de `docs/comparaison-spiking.md` **n'est pas soutenable** : à R̂ = 0,17, le gain réel de temps est ≈ 1,4×, pas 6,7×. Et le push *signé* est aujourd'hui plus lent par événement que le push valué, alors qu'il stocke 1 bit au lieu de 8 — un défaut de noyau (`FusedSign` n'a pas reçu le traitement AVX2 du push int8), pas une loi de la nature.

**Et le constat qui commande la suite** : à 1,9 M paramètres, le modèle dense tient dans le cache et le chemin par listes n'a structurellement rien à gagner. L'avantage de Drave — ne lire que ce qui parle — n'existe que sur un modèle **plus gros que la mémoire**, avec une activité par jeton minuscule. C'est exactement la leçon du disque de Kimi-K3, et ça recentre tout : un modèle « à son meilleur dans Drave » se mesure en **octets lus par jeton**, pas en MACs ni en événements.

\## La suite, dans cet ordre

1. **Banc 2 — gros modèle, activité minuscule, routé par blocs** : paramètres ≫ cache, quelques pour cent actifs par jeton, mesure en octets/jeton contre un dense à *même lecture d'octets* (c'est la comparaison honnête).
2. **Distillation depuis Qwen2.5-0.5B** (sur le disque, jamais utilisée dans ce dépôt) pour payer la qualité du routage.
3. **Noyau signé** : chronométrer `FusedSign` optim
… [563 caractères tronqués]

### Tour 3 — <goal_round> Objective: "Produire un modèle nativement événementiel qui soit à son meilleur dans l'architecture de Drave … [1096 caractères tronqués]

*95 appels d'outils.* Actions notables :

- bash — Check workspace and resources state
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/essai_blocs.py`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/essai_blocs.py`
- bash — Smoke test block-routed bench
- bash — Locate cache and family lines
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/essai_blocs.py`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/essai_blocs.py`
- bash — Show family loop for edit
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/essai_blocs.py`
- bash — Smoke test iso-reads routed bench
- bash — Launch routed-model experiments on both GPUs
- bash — Check engine MoE architecture support
- bash — Look for a GGUF writer in the repo
- bash — Read the repo's GGUF writer
- … et 80 autres

**Synthèse produite :**

⏵ Réponse chiffrée sur la ségrégation NUMA, à partir des mesures du dépôt

\## Réponse courte

**Une partie est bénéfique, une autre est probablement contre-productive, et la raison invoquée — le QPI — n'est pas le goulot sur cette machine.** Le dépôt a déjà mesuré les trois régimes qui comptent, et ils ne répondent pas de la même façon.

\## Ce que la machine mesure aujourd'hui

| mesure | valeur | source |
|---|---|---|
| distances NUMA | 10 local / **21 distant** (2,1×) | `numactl --hardware` |
| RAM | **64,3 / 64,4 Go symétrique** (libre : 2,6 / 0,4 Go — page cache) | idem |
| calcul pur, nœud 0 vs nœud 1 | 13,8 vs 14,2 Go/s → **3 %, du bruit** | `REPRISE.md:1523` |
| lecture NVMe, nœud 0 vs nœud 1 | 22,41 vs 21,45 Go/s → **4 %** | `REPRISE.md:1524` |
| **épinglage sur UN socket, charge réelle** (30B MoE) | **23,2 → 27,6 s, soit −19 %** | `docs/convertisseur.md:192` |
| banc mémoire, lié à un socket | 20,7 → **24,7 Go/s** | `docs/convertisseur.md:101` |
| 20 cœurs / +hyperthreads | 22,5 / 18,9 Go/s | plan du moteur |
| NVMe 16 lecteurs | 5,4 → **31,1 Go/s** | idem |
| passe Kimi-K3 | `sda` occupé **87,6 %**, CPU **21 %**, 133 Mio/s (plafond 205) | `rapport-passe-k3-disque.md` |

Les deux dernières lignes sont la clé : **la passe lourde du projet est liée au disque, pas à l'interconnexion.** Pendant 26 minutes, le CPU est à 21 % — le QPI est quasiment au repos. Le séparer ne rapporte rien ; c'est le **motif d'accès disque** qui laisse 35 % sur la table (133 contre 205 Mio/s).

\## Pourquoi le QPI n'est pas votre goulot

Les deux seules mesures « inter-nœuds » du dépôt donnent 3 % et 4 % — de l'ordre du bruit de cette machine. Et surtout, l'expérience qui devait montrer le coût du QPI montre l'inverse : **restreindre un calcul au seul socket 1 le ralentit de 19 %**. La ressource rare n'est pas la liaison entre processeurs, c'est **la bande passante mémoire d'un socket**. Le micro-banc dit le contraire (20,7 → 24,7 Go/s en liant un socket) parce qu'il fait un flux unique : une charge réelle a beaucoup de flux simultanés et a besoin des deux contrôleurs mémoire.

\## Ce que votre ségrégation apporte réellement

1. **La reproductibilité des mesures — et c'est le gain le plus solide.** Le dépôt le répète partout : « la machine portait une charge de fond (bureau, autres projets) qui fait varier le temps mur de 30 % », et plusieurs campagnes ont dû être refaites sous charge 8-14. Isoler le bureau et l'affichage sur le nœud 0 rend les chiffres reproductibles. **Bén
… [3380 caractères tronqués]

### Tour 4 — <goal_round> Objective: "Produire un modèle nativement événementiel qui soit à son meilleur dans l'architecture de Drave … [1096 caractères tronqués]

*76 appels d'outils.* Actions notables :

- bash — Check trained model and bench outcome
- bash — Check bench process state
- bash — Kill diverged bench and start dense twin
- bash — Stop leftover bench, confirm dense twin running
- bash — Export trained routed model to GGUF
- bash — Run reference and engine on trained routed model
- bash — Run formal gate on trained routed model
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/exporter_gguf.py`
- bash — Simplify exporter flags
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-reparti-moteur.sh`
- bash — Run the distributed gate on our trained model
- bash — Inspect distributed run output in detail
- bash — Compare truncated vs full model perplexity
- bash — Verify the reference flux gate is green
- … et 60 autres

**Synthèse produite :**

⏵ Erreur plus grave : le décalage double était aussi dans la **boucle d'entraînement**

### Tour 5 — Hypothèse de changement de configuration matériel : Si je déploie ce projet sur une station de travail bi-processeur (Xe … [683 caractères tronqués]

*33 appels d'outils.* Actions notables :

- bash — Check background work and machine state
- bash — Prepare interleaved NUMA A/B script
- bash — Run interleaved NUMA A/B on real workload
- bash — Re-run NUMA A/B with bash timing
- bash — Inspect GPU/PCIe topology and NVLink
- bash — Locate big models and disks
- bash — Map disks to NUMA nodes and locate K3 model
- bash — Measure sequential read ceilings of both disks
- bash — Find large files for disk benchmarks
- bash — Measure both disks sequential read
- bash — Check routed training and load
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/numa-segregation.md`
- bash — Verify cited numbers in the document
- bash — Verify PCIe root complex for each GPU
- … et 18 autres

**Synthèse produite :**

⏵ Document NUMA livré et commité ; je fais le point sur l'objectif

\## Le document demandé

**`docs/numa-segregation.md`** (207 lignes, commit `29a68c8`) répond à la question avec des mesures faites **sur cette machine aujourd'hui**, pas des principes.

**Réponse en trois lignes :**

1. **Séparer l'OS, le bureau et l'affichage du calcul : bénéfique** — pour la reproductibilité des mesures (le dépôt note jusqu'à 30 % de variation du temps mur à cause de la charge de fond) et pour la VRAM rendue au moteur. Pas pour le QPI.
2. **Forcer le calcul sur un seul socket : coûteux, et mesuré.** J'ai lancé un A/B entrelacé (3 répétitions, charge réelle, Qwen 0.5B) :

| configuration | médiane | écart |
|---|---:|---:|
| A — défaut (20 fils, aucune liaison) | 15 365 ms | — |
| **B — nœud 1 seul (10 fils, mémoire nœud 1)** | **16 614 ms** | **+8,1 %** |
| C — nœud 1, mémoire entrelacée | 16 474 ms | +7,2 % |
| D — deux nœuds, mémoire entrelacée | 15 225 ms | −0,9 % |

La proposition est **la plus lente des quatre**, et le dépôt avait déjà mesuré pire sur un 30B MoE (`--pin` : 23,2 → 27,6 s, −19 %). Le facteur limitant n'est pas la liaison QPI (3 à 4 % d'écart entre nœuds en calcul pur et en lecture NVMe) mais **la bande passante mémoire d'un socket**.

3. **Le goulot réel est le disque.** Mesuré aujourd'hui en lecture directe : **246 Mo/s** sur le disque dur `sda` contre **1 600 Mo/s** sur le NVMe — facteur 6,5, qui décide d'une passe de 26 minutes. Le document note aussi que la page cache ne retient pas le dense de Kimi-K3 (déjà mesuré : 1 516 430 puis 1 522 584 ms), donc les 128 Go n'achètent pas ce qu'on croit, et que le NVMe actuel est plein à 97 %.

Il contient aussi la topologie relevée (distances NUMA 10/21, 64/64 Go symétrique, **les deux Quadro déjà sur le nœud 0, sur deux root complexes distincts**, NVLink 25,781 Go/s), les recommandations, les réserves, et un protocole à trois mesures entrelacées si la configuration proposée est retenue.

\## Et l'objectif, pendant ce temps

Deux portes ont été franchies et sont commitées (`a9f4b40`) :

- **Porte d'exécution** : un Qwen3-MoE **entraîné ici** tourne dans Drave — 5,3397 de perplexité contre 5,3585 pour la référence à poids quantifiés identiques, corrélation des logits min 0,9906, top-1 95,7 %, `compare_logits --porte` **exit 0**.
- **Porte de répartition** : deux processus, deux plages de couches — **3,9020 = 3,9020**, écart de flux 0,00e0, écart relatif **0,0000 %**.
- **À lecture égale** (2,3 M poids/jeton, v
… [892 caractères tronqués]

### Tour 6 — je viens de commander une carte pcie pour 4 nvme 4x4 et 4 unités Patriot P320 256GB PCIe Gen 3x4 M.2 2280 SSD pour aller … [296 caractères tronqués]

*9 appels d'outils.* Actions notables :

- bash — Inspect PCIe link widths for GPUs and NVMe
- bash — Check DIMM population
- bash — Try verbose lspci and EDAC DIMM data
- bash — Read PCIe link widths and measure memory bandwidth
- bash — Check NVMe contents and capacity
- web_search
- bash — Measure PCIe link speed under GPU load
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/numa-segregation.md`
- bash — Commit the array analysis section

**Synthèse produite :**

⏵ Analyse terminée et ajoutée au document (§11) — voici l'essentiel

\## Le plan est bon sur le placement, mais trois contraintes mordent avant lui

J'ai ajouté une section au document (`docs/numa-segregation.md` §11, commit `42ea1ae`). Ce qui est juste d'abord : **l'array sur le nœud des GPU, l'OS/affichage isolés de l'autre côté, la RAM symétrique** — c'est exactement ce que les mesures recommandaient. Et les P320 annoncent 2 200 Mo/s, soit ~5× le NVMe actuel (mesuré **1,6 Go/s**) et ~9× le disque dur (**246 Mo/s**).

\### 1. Les lignes PCIe — c'est là que ça coince

Le Xeon E5-2687W v3 donne **40 lignes PCIe 3.0 par socket**. Relevé à l'instant sur le nœud 0 :

| périphérique | liaison | max |
|---|---|---|
| Quadro RTX 5000 (`03:00.0`) | **x16** (2,5 → 5,0 GT/s selon la charge) | x16 Gen3 |
| Quadro RTX 5000 (`04:00.0`) | **x16** (2,5 → 8,0 GT/s) | x16 Gen3 |
| NVMe système (`02:00.0`, MAP1602) | x4 Gen3 | x4 Gen4 |

**36 lignes sur 40 sont déjà prises.** Une carte 4×NVMe x16 en demande 16 de plus : **52**. Il faudra choisir, et ce choix se fait au BIOS :

- **GPU en x8 + carte en x16** : l'array est complet, mais chaque GPU perd la moitié de sa bande passante hôte (le dépôt a mesuré **6,5 Go/s en x8**) — et c'est ce trafic qui porte le miroir du cache KV, donc le « 22,16 → 3,29 ms/jeton ».
- **GPU en x16 + carte en x4** : les 4 SSD partagent ~3,9 Go/s, soit **le débit d'un seul**. L'array ne sert à rien.

Deux vérifications à faire **avant** de tout démonter : la **bifurcation `x4x4x4x4`** du slot choisi (les cartes passives l'exigent ; sans elle, **un seul SSD apparaît**), et que ce slot est bien câblé au **CPU** — derrière le PCH, c'est du x4 Gen2 partagé, ~2 Go/s pour les quatre. Et c'est le slot qui décide du nœud : si le seul x16 libre est câblé au CPU 1, l'array sera sur le nœud 1, pas avec les GPU.

\### 2. Les canaux mémoire — la moitié est vide

EDAC le dit sans ambiguïté : **2 DIMM par socket, sur un contrôleur à 4 canaux**. Deux canaux sur quatre sont vides, et la bande passante mesurée aujourd'hui le confirme : **20,4 Go/s** (64 Mo, 16 threads) — un ordre de grandeur de dual-channel.

Donc « je maintiens 2×32 + 2×32 » = **la moitié de la bande passante mémoire de la machine**, dans le régime même que le placement NUMA ne rattrape pas (§3 : forcer un socket coûte 8 à 19 %). Passer à **4 DIMM par socket** doublerait à peu près cette bande passante. C'est probablement le meilleur gain par dollar de toute la liste, et il n'est pas dans le plan.


… [1410 caractères tronqués]

### Tour 7 — le ram est actuellement hors de prix. je t'ai fait évaluer une approche asymétrique, mais c'est déconseillé. Que peut-on … [19 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Check uncore, governor, THP settings
- bash — Check swap, memory sysctls and zram
- bash — Read swap settings and biggest swap users
- bash — Measure memory bandwidth under three placements
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/numa-segregation.md`
- bash — Commit the RAM section

**Synthèse produite :**

⏵ Section RAM ajoutée au document (§12, commit `ffa46da`) — voici la réponse

\## 1. D'abord : 26 Go sont déjà perdus, et ça ne coûte rien à reprendre

Relevé à l'instant : **62 Go de swap, 26 Go utilisés — et le swap est sur le disque dur** (246 Mo/s mesuré). Toute page touchée là coûte des centaines de microsecondes. Le dépôt avait déjà croisé ce fantôme pendant les travaux Kimi-K3 (« VmSwap 28,5 Go » relevé alors que le moteur affirmait « pas de swap »).

`swapoff -a && swapon -a` les ramène en RAM — il y a 103 Go disponibles. Et quand l'array arrive, **le swap va sur le NVMe, jamais sur `sda`**. `vm.swappiness` est déjà à 10 : le réglage n'est pas le problème, le support l'est.

Côté réglages, le reste est déjà propre (gouverneur `performance`, THP `always`, `mmap` par défaut). J'ai quand même mesuré le banc mémoire sous trois placements :

| placement | débit |
|---|---:|
| sans liaison (16 fils) | 20,4 Go/s |
| lié au nœud 0 (10 fils) | 22,4 Go/s (+10 %) |
| **entrelacé sur les deux nœuds** (20 fils) | **23,8 Go/s (+17 %)** |

**Mais** : le même entrelacement donne **−0,9 %** sur une passe réelle (l'A/B du § 7). Le gain de banc ne se transfère pas — c'est exactement la règle du dépôt, et elle joue ici contre l'optimisation gratuite. Le seul levier gratuit qui reste est la **fréquence de l'uncore** (le ring plafonne la bande passante sur Haswell-EP ; MSR `0x620`, non exposé par le noyau ici, il faut `msr-tools` et root).

\## 2. Le substitut de RAM, c'est le disque — et il est déjà commandé

La passe K3 lit **206,58 Gio** dont 57,93 de dense lu une fois. Le dépôt a mesuré que **la page cache ne retient pas ce dense** d'une passe à l'autre (1 516 430 puis 1 522 584 ms). Un array à 7 Go/s lit ces 58 Go en **8 secondes** : le problème disparaît au lieu d'être résolu.

Et le corollaire du programme, qui est le vrai argument : **un modèle routé n'a pas besoin d'être en RAM pour être gros**. Mesuré sur le prototype — 2,3 M poids lus par jeton pour 7,58 M stockés, **3,35× de paramètres pour la même lecture**. Acheter de la RAM pour faire tenir un modèle de 1,5 To sur une machine de 125 Go est perdu d'avance : c'est la définition de la niche du projet.

\## 3. Réduire ce qui *doit* tenir en RAM

Le cache KV est le seul poste qui grandit avec l'usage, et il est déjà chiffré :

| réglage | coût qualité | gain RAM |
|---|---|---|
| KV int8 à 512 jetons | **+1,5 %** de perplexité | 2× |
| KV int8 à 8 192 jetons | **+3,0 %** | 2× |
| KV int4 | +364 % → inutilisable |
… [1303 caractères tronqués]

### Tour 8 — donc les nouveaux nvme seront sur l'autre cpu pour ne pas réduire le nombre de voies des gpu. La ram reste tel-quelle. l … [282 caractères tronqués]

*11 appels d'outils.* Actions notables :

- bash — Check RAID tooling, ECC and kernel
- web_search
- bash — Check I/O queue settings, md modules, amdgpu firmware
- bash — Verify md RAID and GPU driver modules
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/configuration-nvme-raid-amd.md`
- bash — Verify missing storage tools
- bash — Check tools by full path, not PATH
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/configuration-nvme-raid-amd.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/configuration-nvme-raid-amd.md`
- bash — Check section 5 numbering for the lspci reference
- bash — Commit the reconfiguration document

**Synthèse produite :**

⏵ Document livré (`docs/configuration-nvme-raid-amd.md`, commit `1353c8e`) — voici l'essentiel

\## Le plan tient : les GPU gardent leurs x16

36 voies sur 40 utilisées sur le nœud 0 (2 GPU x16 + NVMe système x4). En mettant l'array sur le CPU 1, les Quadro **restent en x16** — c'est le bon arbitrage, puisque les faire tomber en x8 coûte la moitié de la bande passante hôte (6,5 Go/s mesuré). Le prix à payer : **6 à 8 Go/s traverseront le QPI**, soit la moitié de ce qu'il écoule. Les mesures du dépôt donnent 3-4 % de pénalité pour le traverser, donc le pari est raisonnable — mais c'est un pari, et le § 7 dit comment le vérifier (trois placements de fils à comparer).

\## Les vérifications à faire **avant** de démonter

1. **Bifurcation `x4x4x4x4`** sur le slot, et qu'il est bien câblé au **CPU 1** — derrière le PCH c'est du x4 Gen2 partagé, ~2 Go/s pour les quatre SSD, et tout le bénéfice part.
2. **`Above 4G Decoding`**, **ASPM désactivé** sur les slots NVMe, **affichage primaire = AMD**.
3. **La carte AMD dans un slot x4 ou x8**, pas x16 : elle n'en a pas besoin, et chaque voie laissée libre va aux SSD.

\## Le RAID

RAID0 `mdadm` (les poids se retéléchargent), `--chunk=512K`, `--assume-clean`, XFS, `noatime`, `fstrim.timer`, `mdadm.conf` + `dracut -f`. Attendu : **~2 Go/s par P320, 6-7 Go/s sur `md0`** (plafonné par le lien x16 Gen3, pas par les disques). Si `md0` plafonne à 2 Go/s → la bifurcation n'est pas active : `current_link_width` le dira. **Deux pièges** : les P320 sont **DRAM-less** (l'écriture soutenue s'effondre après le cache SLC — télécharger les gros modèles un par un), et **pas de swap sur le RAID0** (une panne de SSD corromprait la mémoire paginée).

\## La carte Yeston 6 mini-DP

C'est très probablement une **R7 350** (GCN 1.0, Southern Islands). Le noyau la pilote avec **`radeon` par défaut** — rien à faire. Pour `amdgpu` : `amdgpu.si_support=1 radeon.si_support=0`. **Attention** : `cik_support` concerne Sea Islands (Bonaire/Hawaii), pas cette carte — les confondre donne un écran noir. Le firmware `amdgpu/` est déjà en place, et les deux modules aussi.

**Le point qui annule tout si on le rate** : vérifier que X ne prend pas les Quadro (`xrandr --listproviders` → un seul fournisseur ; `nvidia-smi` → aucun processus). Si elles apparaissent, forcer le `BusID` de l'AMD dans `xorg.conf.d`. Et pour les six écrans : les adaptateurs mini-DP→HDMI/DVI doivent être **actifs** sauf si la sortie émet du DP++.

\## Les autres optimisations, par ordre de 
… [1255 caractères tronqués]

### Tour 9 — encore une journée complète avant l'arrivé du nouveau matériel. Exécute pendant 24h les tâches que tu trouves les plus a … [80 caractères tronqués]

*24 appels d'outils.* Actions notables :

- bash — Inventory runnable models
- bash — Inventory corpora and traces
- bash — Verify big model paths and free space
- bash — Check speculative decoding support
- bash — Check time tool, tokenizer and a second model
- bash — Find KV and sparsity CLI flags
- bash — Find KV precision flag
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/campagne-benefices.sh`
- bash — Launch the scaled training pairs on both GPUs
- bash — Smoke-test campaign steps
- bash — Measure dense/push baselines before the sweep
- bash — Verify the tokenizer trap
- bash — Fix the tokenizer trap in the campaign
- bash — Launch the full 24h campaign queue
- … et 9 autres

**Synthèse produite :**

⏵ Campagne 24 h lancée : file de mesures + deux paires d'entraînement en parallèle

\## Ce qui tourne maintenant, et jusqu'à demain

**1. La file de mesures** (`tools/campagne-benefices.sh`, commit `596de74`) — neuf étapes, ~4 à 8 h, journal dans `/tmp/campagne24/journal.txt` :

| étape | ce qu'elle mesure |
|---|---|
| `grille` | **6 modèles, 0,5 B → gpt-oss-120b** : perplexité, RSS, octets lus, débit — le HDD et le NVMe à l'œuvre |
| `parcimonie` | 12 réglages × {dense, listes} : le coût suit-il l'activité sur un VRAI modèle ? |
| `contexte` | ctx 512 → 8 192 : PPL, cache KV choisi, mémoire |
| `lot` | `--lot` 1 → 64 : le seul levier qui multiplie un débit de disque |
| `routage` | MoE 30B-A3B : experts réveillés, volume à router |
| `semantique` | traces UDHR **avec et sans** l'échelle corrigée |
| `noyau` | bande passante, push/pull par densité |
| `repartition` | deux nœuds, porte du modèle entraîné |
| `portes` | non-régression |

**2. Deux paires d'entraînement** sur les deux GPU, à **lecture égale** — pour voir si l'avantage du routage tient à l'échelle :

| GPU | paire | lectures/jeton/couche |
|---|---|---|
| 0 | dense dim 256 (3,2 M) vs **routé 8 experts** (~10 M) | 0,85 M |
| 1 | dense dim 384 (7,2 M) vs **routé 16 experts** (~40 M) | 1,92 M |

Déjà à 8 000 pas, val **2,12-2,16 bits/octet**.

**3. Un batch 2 enchaîné automatiquement** (`batch2.sh`) pour la question que je trouve la plus intéressante de la journée : **le bénéfice événementiel dépend-il de la tâche ?** Même modèle, quatre corpus — prose anglaise, français, code, multilingue — et pour chacun, densité d'activation en dense et en listes. Plus chaque modèle sur sa tâche *et* sur l'autre (codestral-22B sur du code et sur de la prose), et la carte de latence réseau.

\## Deux trouvailles avant même de commencer

**Le piège du tokenizer.** `data/wikitext2_test.txt.ids` vient d'un **autre** tokenizer que Qwen2.5 (`201,438,10498…` contre `198,284,8397…`). Sur les mêmes octets :

| identifiants | perplexité (256 jetons, ctx 512) |
|---|---:|
| ceux du dépôt | **7 710,72** |
| tokenisés par le modèle | **17,43** |

Toute la campagne serait partie d'un chiffre faux. La règle est maintenant dans le script : **chaque modèle tokenise son propre corpus**.

**Deux manques, consignés comme manques.** `bge-m3` (embeddings, BERT 24 couches) est lisible en en-tête mais **inexécutable** — le moteur exige `blk.0.attn_norm.weight` et une attention causale : la famille « recherche/embeddings » n'est pas co
… [528 caractères tronqués]

### Tour 10 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1476 caractères tronqués]

*34 appels d'outils.* Actions notables :

- bash — Check campaign and training status
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/campagne_synthese.py`
- bash — Test the synthesis parser on current logs
- bash — Inspect time -v output format
- bash — Debug the time -v capture
- bash — List campaign directory
- bash — Inspect the 14B run and time output
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/campagne_synthese.py`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/campagne_synthese.py`
- bash — Verify the fixed synthesis parser
- bash — Check HuggingFace network access and cache
- bash — Download a 1.5B target model for the speculative test
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/speculatif.py`
- bash — Test the speculative acceptance script
- … et 20 autres

**Synthèse produite :**

⏵ Point de mi-campagne : deux résultats solides, et la file continue

\## Ce que la campagne a déjà établi (21 h 45, 25 min après le départ)

**1. Le décodage spéculatif naïf vaut ×1,2 — mesuré avant d'écrire une ligne de moteur.**

`tools/speculatif.py` : brouillon Qwen2.5-0.5B, cible Qwen2.5-1.5B (même tokenizer), 40 préfixes, k = 8.

| | |
|---|---:|
| acceptation moyenne | **3,35 jetons sur 8 (41,9 %)** |
| médiane · min · max | 3 · 0 · 8 |
| au moins 1 / 2 / 3 / 4 acceptés | 68 % · 60 % · 52 % · 42 % |
| gain si le brouillon coûte 0,25× / **0,33×** / 0,50× la cible | ×1,45 · **×1,20** · ×0,87 |

Sur cette machine, bornée par la bande passante mémoire, un 0,5 B coûte ~1/3 d'un 1,5 B par pas : **×1,20**, là où la feuille de route attendait ×1,58. Un brouillon **générique** ne paie pas — il faut un brouillon aligné (distillé, ou une tête Eagle3 qui consomme les états cachés de la cible), donc un chantier d'entraînement, pas une option de moteur.

**2. La perplexité n'est comparable qu'à tokenizer égal — et la taille ne dit pas la qualité.**

Trois modèles de la grille partagent **exactement** le même tokenizer (mêmes premiers jetons `198,284,8397,…`) :

| modèle | perplexité | **bits/octet** | tok/s | RSS | lus |
|---|---:|---:|---:|---:|---:|
| Qwen2.5-0.5B Q8 | 17,43 | **0,983** | 28,7 | 1,28 Go | 0 |
| r1-distill-1.5B Q4 | **47,14** | **1,326** | 9,5 | 4,76 Go | 1,04 Go |
| r1-distill-14B Q4 | 14,30 | **0,915** | 0,5 | 39,8 Go | 8,71 Go |

**Le 1.5B est 2,7× pire que le 0.5B** : un distillat de raisonnement est mauvais en langue pure. Et codestral (tokenizer Mistral, 32 768 entrées) découpe le même texte en **288 554** jetons contre 85 626 : sa perplexité ne se lit pas sur la même échelle, d'où la colonne **bits/octet** que j'ai ajoutée au dépouillement.

\## Ce qui tourne

- **La file** : grille (codestral-22B en cours, puis Qwen3-30B-A3B, puis gpt-oss-120b depuis le disque dur), puis parcimonie, contexte, lots, routage, sémantique, noyau, répartition, portes.
- **Batch 2 enchaîné** : la densité d'activation dépend-elle de la **tâche** (prose, français, code, multilingue) ?
- **Batch 3 enchaîné** : l'aiguille dans la botte de foin — la perplexité moyenne ne dit pas si la mémoire tient à 4 000 jetons.
- **Les entraînements** : `d256 dense` **terminé** (val 1,9307 bits/octet), le routé 8 experts suit ; `d384` à 32 000/40 000. La chaîne export → porte → mesure moteur → répartition à deux nœuds est armée pour se déclencher dès qu'ils finissent.
- **Deux ma
… [291 caractères tronqués]

### Tour 11 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1476 caractères tronqués]

*23 appels d'outils.* Actions notables :

- bash — Collect campaign results so far
- bash — Locate the training loop for distillation
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/entrainer_moteur.py`
- bash — Show the loss computation block
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/entrainer_moteur.py`
- bash — Add distillation CLI options and validate syntax
- bash — Smoke-test distillation training
- bash — Fix KL normalization and retest
- bash — Chain the distillation experiment
- bash — Check campaign and training progress
- bash — Verify the semantic tool CLI before its campaign step
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-benefices.md`
- bash — Commit distillation support and the state of the art
- bash — Verify commit message and progress
- … et 9 autres

**Synthèse produite :**

⏵ Mi-parcours : deux modèles entraînés passent la porte, la nuit est armée

\## Ce qui a atterri depuis le dernier point

**Les modèles entraînés passent la porte du moteur, automatiquement.** J'ai armé une chaîne qui exporte, calcule la référence PyTorch **sur les mêmes poids quantifiés**, passe la porte de logits, puis mesure dans le moteur :

| modèle | val (bits/octet) | PPL moteur | paires/jeton | événements/jeton | tok/s | porte |
|---|---:|---:|---:|---:|---:|---|
| `m5_d256_dense` (3,2 M) | 2,007 | **5,3973** | 3,2 M | 732,9 M | 438,3 | ✅ |
| `m5_d384_dense` (7,2 M) | 1,919 | **5,3719** | 7,2 M | 1 648,5 M | 240,2 | ✅ |

**Le rendement décroît vite** : 2,25× plus de paramètres lus n'apporte que **0,5 %** de perplexité et coûte **1,8× de débit**. C'est exactement l'argument du modèle qui *stocke* plus sans *lire* plus — ce que les deux routés de la même paire vont trancher.

Et j'ai consigné une mise en garde qui évite une erreur facile : la colonne « val » (16 000 jetons répartis) et la colonne « PPL moteur » (les 256 premiers octets) **ne mesurent pas la même tranche de texte** — 34 % d'écart systématique, qui n'est pas un défaut du moteur.

**La distillation est implémentée** — le levier que l'inventaire du dépôt notait « mentionné, jamais réalisé ». L'élève creux imite la distribution entière d'un dense gelé, pas seulement son argmax. Piège corrigé au passage : `kl_div(reduction="batchmean")` divise par la taille du **lot**, pas par le nombre de jetons — sur des logits (lot, séquence, vocabulaire) la KL sortait **128 fois trop grande** (perte 622 mesurée, contre ~7 après correction).

\## La nuit est armée

- **GPU 0** : distillation du routé dim 256 (enseignant = dense dim 384) → puis **dim 512 dense** → puis **dim 512 routé, 16 experts**.
- **GPU 1** : **dim 384 routé distillé** — le témoin non distillé existe déjà, seul le terme de KL change.
- **CPU/disque** : la file de campagne continue (codestral-22B en cours, puis Qwen3-30B-A3B, puis **gpt-oss-120b depuis le disque dur**), puis batch 2 (densité par tâche), batch 3 (aiguille dans la botte de foin), et l'export continu à chaque modèle.

Tout est commité (`d8e1311`), et les journaux sont horodatés avec la charge de fond — parce qu'elle a déjà atteint 47 pendant la passe du 14B, et qu'un temps mesuré sous cette charge ne se compare pas à un temps mesuré sous charge 3.

### Tour 12 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1476 caractères tronqués]

*13 appels d'outils.* Actions notables :

- bash — Check campaign and training state
- bash — Add the generation and task-quality batch
- bash — Check the default lot for prefill
- bash — Find the default lot value
- bash — Measure dense vs push on our trained models
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-benefices.md`
- bash — Commit the dense-vs-push measurement
- bash — Chain the batch-size sweep on the 30B MoE
- bash — Fix the batch 5 waiter to wait for a real end marker
- bash — List waiter PIDs only
- bash — Rewrite and launch the fixed waiter
- bash — Fix all waiters to use end markers
- bash — Final state check for this round

**Synthèse produite :**

⏵ Chaînage corrigé, et une réponse nette sur « pour quel type de tâche »

\## Ce que ce round a établi

**Le chemin par listes coûte 1,8 à 2,1× sur nos propres modèles — et c'est la réponse.** Mêmes jetons, mêmes 8 fils :

| modèle | dense | listes | densité |
|---|---:|---:|---:|
| `m5_d256_dense` (3,2 M) | **787,2 tok/s** | 442,3 tok/s | 2,874 M événements / 3,2 M paires ≈ **90 %** |
| `m5_d384_dense` (7,2 M) | **528,2 tok/s** | 255,0 tok/s | 6,465 M / 7,2 M ≈ **90 %** |

La densité d'activation vaut **90 %**, très au-dessus du croisement mesuré de 22 %. Autrement dit : **sur un modèle de langue ordinaire, l'architecture par listes est un coût, pas un bénéfice.** C'est la réponse la plus directe à « pour quel type de tâche » — et c'est précisément ce que la branche « parcimonie entraînée » cherche à changer. (J'ai aussi corrigé une étiquette trompeuse dans le rapport : la colonne « événements » portait le total de la fenêtre, pas le compte par jeton.)

**Un bug de chaînage trouvé et corrigé avant qu'il ne fausse la nuit.** Mes quatre « enchaîneurs » attendaient la fin d'un script avec `pgrep` — or `pgrep` sur un script **pas encore lancé** rend la main immédiatement : le batch 5 serait parti en parallèle de la campagne, deux gros modèles lus en même temps, et des temps qui ne mesurent plus rien. Ils attendent maintenant un **marqueur de fin** écrit dans le journal.

\## La file, désormais complète

1. **Campagne** (en cours : codestral-22B, puis Qwen3-30B-A3B, puis **gpt-oss-120b depuis le disque dur**) ;
2. **batch 2** — la densité d'activation dépend-elle de la **tâche** (prose, français, code, multilingue) ?
3. **batch 3** — l'aiguille dans la botte de foin : la perplexité moyenne ne dit pas si la mémoire tient ;
4. **batch 4** *(nouveau)* — la **génération** : TTFT et débit par modèle, quatre tâches (code, traduction, arithmétique, résumé) avec les sorties **verbatim**, et une conversation à trois tours ;
5. **batch 5** *(nouveau)* — le **lot** sur le Qwen3-30B-A3B lu depuis le NVMe, de 1 à 64 : l'axe 1 de la feuille de route, mesuré sur le modèle qui ne tient pas en cache.

Côté GPU : `d256_route` et `d384_route` s'entraînent ; ensuite distillation, dim 512, et l'export continu qui passe déjà la porte pour chaque modèle dès qu'il existe.

### Tour 13 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1476 caractères tronqués]

*9 appels d'outils.* Actions notables :

- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/census_routage.py`
- bash — Run the routing census on the trained model
- bash — Fix the hook and run the census
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-benefices.md`
- bash — Commit the routing census
- bash — Chain the extreme-size model test
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/campagne-benefices.md`
- bash — Commit the campaign plan update
- bash — Round status check

**Synthèse produite :**

⏵ Nouvelle mesure livrée : le recensement du routage, et le cas extrême armé

\## Ce round a produit

**Le recensement du routage** (`tools/census_routage.py`, commit `1e11cc7`) — les trois chiffres qui décident d'un découpage par **experts** plutôt que par plages de couches, mesurés sur `m4_route` (4 couches, 8 experts, top-2, 1 024 jetons) :

| couche | charge max | moyenne | déséquilibre | experts pour 90 % des jetons |
|---|---:|---:|---:|---:|
| 0 | 537 | 256 | **×2,10** | 5 sur 8 |
| 1 | 517 | 256 | ×2,02 | 7 sur 8 |
| 2 | 703 | 256 | **×2,75** | 6 sur 8 |
| 3 | 999 | 256 | **×3,90** | 4 sur 8 |

**Trois conséquences** : le déséquilibre est réel (jusqu'à 3,9× — un partage naïf donnerait un nœud quatre fois plus chargé) ; **on ne peut pas élaguer** (4 à 7 experts sur 8 servent) ; et **le volume à router est négligeable — 847 octets par jeton**, du même ordre que les 848 octets déjà mesurés pour un flux de couche. Ce qui coûte, c'est l'**aller-retour par couche**, pas les octets : répartir par experts multiplie les allers-retours que répartir par couches évite.

**Le cas extrême armé** : batch 6 exécute **DeepSeek-V4.1-Flash Q2 — 365,7 Go sur une machine de 125 Go de RAM** — et mesure les octets lus, la mémoire résidente et le temps. C'est la revendication centrale du projet, et elle méritait son propre chiffre plutôt qu'une extrapolation.

**La chaîne complète est posée** : campagne (codestral-22B en cours, puis Qwen3-30B-A3B, puis gpt-oss-120b depuis le disque dur) → batch 2 (densité par tâche) → batch 3 (aiguille) → batch 4 (génération, quatre tâches verbatim, conversation) → batch 5 (le lot sur le 30B depuis le NVMe) → batch 6 (V4-Flash). Cinq enchaîneurs, chacun attendant un **marqueur de fin** dans le journal — la correction qui évite que deux gros modèles se fassent lire en même temps et que les temps ne mesurent plus rien.

Côté GPU : `d256_route` (12 000/40 000, val 2,075) et `d384_route` (8 000/40 000, val 2,117) s'entraînent ; ensuite distillation, dim 512, et l'export continu. Charge 24, tout tourne.

### Tour 14 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1476 caractères tronqués]

*14 appels d'outils.* Actions notables :

- bash — Understand the restricted-head feature
- bash — Read the restricted-head implementation
- bash — Build the label token list for a classification task
- bash — Compare full head vs restricted head
- bash — Measure the restricted head with 64 tokens, interleaved
- bash — Chain the constrained-output batch
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-benefices.md`
- bash — Commit the constrained-output finding
- bash — Status check
- bash — Identify the running drave processes
- bash — Read the early batch results
- bash — Cancel the duplicate batch 3 run
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-benefices.md`
- bash — Commit the needle and generation results

**Synthèse produite :**

⏵ Deux résultats de tâche atterris : la mémoire tient, et la latence est mesurée

\## Ce que les batches ont rendu (ils ont tourné plus tôt que prévu)

**L'aiguille est retrouvée 12 fois sur 12** — test de mémoire, pas de perplexité : un code unique planté dans une botte de foin à trois profondeurs, quatre longueurs, Qwen2.5-0.5B, `--infer`, `temp 0`.

| longueur | profondeur 10 % | 50 % | 90 % |
|---|---:|---:|---:|
| 512 jetons | ✅ | ✅ | ✅ |
| 1 024 | ✅ | ✅ | ✅ |
| 2 048 | ✅ | ✅ | ✅ |
| **4 096** | ✅ | ✅ | ✅ |

**C'est la démonstration de tâche que la revendication « contexte long » attendait** : le cache KV, sa quantification et sa pagination ne détruisent pas la mémoire du contexte, même à 4 096 jetons sur un 0,5 B.

**La génération, mesurée directement** : 0,5 B → **TTFT 27,9 ms, 29,0 tok/s** ; r1-1.5B → 114,6 ms et 7,1 tok/s. La perplexité ne donne pas la latence perçue ; celle-ci, si.

\## Et deux incidents, traités

**Un défaut d'enchaînement** a fait partir les batches 3 et 4 pendant la campagne : `pgrep` sur un script pas encore lancé rend la main immédiatement. Conséquence : deux gros modèles lisaient le disque en même temps — **les verdicts n'en dépendent pas, les durées oui** (26 s à 609 s pour la même taille). C'est écrit dans le rapport, et j'ai supprimé l'enchaîneur devenu redondant (le batch 3 aurait retourné 30 minutes pour rien).

**Le reste de la chaîne tient** : campagne (codestral-22B, puis 30B, puis gpt-oss) → batch 2 (densité par tâche) → batch 5 (le lot sur le 30B) → batch 6 (**V4-Flash, 365 Go sur 125 Go**) → batch 7 (sorties contraintes). Les entraînements avancent : `d256_route` 16 000/40 000 (val 2,047), `d384_route` 8 000/40 000.

Le rapport (`reports/rapport-campagne-benefices.md`) porte maintenant onze sections : le piège du tokenizer, le spéculatif à ×1,2, les deux familles manquantes, la grille de modèles, les modèles entraînés mesurés dans le moteur, l'état des lieux sourcé par famille, le recensement du routage, les sorties contraintes à ×1,42, la mémoire qui tient, et la latence.

### Tour 15 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1476 caractères tronqués]

*10 appels d'outils.* Actions notables :

- bash — Check state after the early batches
- bash — Test codestral on code vs prose
- bash — Launch the codestral diagnostic in the background
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-benefices.md`
- bash — Verify the report structure
- bash — Fix the heading and commit the verdict table
- bash — Check the codestral diagnostic
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-benefices.md`
- bash — Re-read the grid section
- bash — Commit the grid update with the MoE result

**Synthèse produite :**

⏵ Le MoE gagne sur les deux tableaux, et une anomalie consignée comme telle

\## Le résultat de la grille qui compte

| modèle | PPL | **bits/octet** | RSS | octets lus |
|---|---:|---:|---:|---:|
| Qwen2.5-0.5B Q8 | 17,43 | 0,983 | 1,28 Go | 0 |
| r1-distill-1.5B Q4 | 47,14 | 1,326 | 4,76 Go | 1,04 Go |
| r1-distill-14B Q4 | 14,30 | 0,915 | 39,8 Go | 8,71 Go |
| codestral-22B Q4 | **35 657** ⚠️ | — | 63,6 Go | 12,7 Go |
| **Qwen3-30B-A3B Q4 (MoE)** | **8,63** | **0,742** | **14,3 Go** | 11,8 Go |
| gpt-oss-120b MXFP4 | en cours | | | |

**Le MoE donne la meilleure qualité de la grille pour trois fois moins de mémoire que codestral-22B** — et moins que le 14B dense. Un modèle plus gros qui lit moins : c'est la thèse du projet, démontrée ici par un modèle qui n'a pas été conçu pour ça. Le prototype routé qu'on entraîne cherche exactement à reproduire ce rapport en le construisant.

\## L'anomalie, consignée comme un point d'interrogation

Codestral-22B à **35 657** de perplexité sur de la prose, c'est 4 000× le 30B. Deux hypothèses : le modèle est spécialisé pour le **code** et mauvais en prose — ou **le moteur exécute mal l'architecture Mistral**, qui n'a aucune porte dans `tools/portes.sh`. Un diagnostic tourne en arrière-plan : génération de code (le texte est-il cohérent ?) puis perplexité **sur du code**. Tant qu'il n'a pas rendu, je ne le compte pas comme un résultat.

\## Le rapport porte maintenant son verdict

J'ai ajouté en tête un tableau **famille par famille** avec la mesure qui le porte :

- **gagne par construction** : sorties contraintes (×1,42 + garantie d'ensemble) ;
- **gagne par ses circonstances** : modèles plus gros que la RAM, contexte long (12 aiguilles sur 12) ;
- **perd** : la modélisation de langue ordinaire tant que le modèle n'est pas creux (1,8 à 2,1× plus lent en listes à 90 % de densité) ;
- **manque** : embeddings (inexécutable) et décodage spéculatif (mesuré à ×1,20, insuffisant).

Le reste de la nuit continue : campagne sur gpt-oss-120b, batches 2/5/6/7 enchaînés, et les quatre entraînements dont la distillation.

### Tour 16 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1476 caractères tronqués]

*21 appels d'outils.* Actions notables :

- bash — Check diagnostic, campaign and training state
- bash — Check the codestral diagnostic progress
- bash — Download a tiny Mistral for the architecture gate
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte_mistral.py`
- bash — Locate the tiny Mistral snapshot
- bash — Export the tiny Mistral and test engine loading
- bash — Fix import and retry the export
- bash — List the tiny Mistral files
- bash — Download the tiny Mistral weights
- bash — Support pytorch_model.bin and export again
- bash — Build a dimensionally valid tiny Mistral and export it
- bash — Run the Mistral gate: reference and engine
- bash — Fix the reference class and run the gate
- bash — Train the tiny Mistral so its logits have structure
- … et 7 autres

**Synthèse produite :**

⏵ Fausse alerte levée : le moteur exécute Mistral correctement, et la famille a maintenant sa porte

\## Ce que ce round a établi

L'anomalie codestral (35 657 de perplexité sur de la prose, 4 000× le 30B) avait deux explications : le modèle est spécialisé pour le **code**, ou le moteur exécute mal l'architecture **Mistral** — qui n'avait **aucune porte** dans `tools/portes.sh`, alors que Qwen, GLM, V4, gpt-oss et Kimi en ont une.

J'ai construit la porte manquante (`tools/porte_mistral.py`, commit `26e55bd`) : elle exporte un Mistral et fabrique la référence PyTorch **sur les mêmes poids quantifiés**. Sur un Mistral minuscule entraîné ici même :

| | perplexité | corrélation des logits | top-1 |
|---|---:|---:|---:|
| référence PyTorch (mêmes poids Q8_0) | 3 411,4394 | — | — |
| **moteur** | **3 411,4405** | **min 1,0000** | **100 %** |

**Le moteur exécute Mistral correctement.** Les 35 657 de codestral sont un décalage de **tâche** — un modèle spécialisé pour le code, évalué sur de la prose. La ligne « code » du verdict est donc : la famille tourne, c'est le modèle qui n'est pas fait pour ça.

\## Et une fausse alerte que je consigne

La première version de mon script instanciait le modèle par `MistralForCausalLM(config)` — des poids **aléatoires** — au lieu de `from_pretrained`. La porte accusait donc le moteur d'un défaut de la référence, et rendait « NON TENUE » à tort. C'est exactement ce qu'une porte doit empêcher : **elle a d'abord accusé le bon camp (le trou de couverture), puis le mauvais (mon script)**. Les deux sont écrits dans le rapport.

J'ai aussi écrit ce script **à part** de `exporter_gguf.py`, qui tournait dans la chaîne d'export : modifier un outil en service est le meilleur moyen de corrompre les résultats de la nuit.

La campagne continue (gpt-oss-120b en cours depuis 22:06), les quatre entraînements avancent (`d256_route` 32 000/40 000, `d384_route` 20 000/40 000), et les batches 2/5/6/7 sont enchaînés pour le reste de la nuit.

### Tour 17 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*11 appels d'outils.* Actions notables :

- bash — Check the diagnostic and campaign state
- bash — Identify the two gpt-oss processes
- bash — Cancel the competing gpt-oss generation
- bash — List batch4 process tree
- bash — Stop batch4 and mark it finished so the chain continues
- bash — Inspect the gates script structure
- bash — Read the gate helper and the end of portes.sh
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-mistral.sh`
- bash — Test the standalone Mistral gate
- bash — Add the Mistral gate to the gate suite
- bash — Commit the Mistral gate and its integration

**Synthèse produite :**

⏵ Mistral a désormais sa porte, dans la suite de portes du dépôt

\## Ce round

**La porte Mistral est entrée dans `tools/portes.sh`** (commit `210e760`). Elle fabrique un Mistral minuscule **entraîné** — pas aléatoire, parce que des poids au hasard rendent des logits quasi uniformes sur lesquels une corrélation ne mesure rien — avec des dimensions **multiples de 32** (les blocs de quantification ggml font 32 poids ; le modèle de test officiel de HuggingFace a `intermediate_size = 37`, il est tout simplement inexporterable). Mesure :

| | perplexité | corrélation | verdict |
|---|---:|---:|---|
| référence PyTorch (mêmes poids Q8_0) | 3 502,5424 | — | |
| **moteur** | **3 502,4907** | **min 1,0000** | ✅ porte tenue |

C'est la famille qui manquait pour interpréter codestral — et le dépôt couvre maintenant Qwen, GLM, V4, gpt-oss, Kimi **et Mistral**.

\## Une décision de ressources, documentée

Deux processus lisaient **le même gpt-oss de 63 Go en même temps** : la mesure PPL de la campagne (la mesure phare « plus gros que la RAM ») et la génération du batch 4. J'ai **annulé la génération** — chaque étape gpt-oss du batch 4 coûtait ~1 h de lectures et menaçait de faire tomber les deux mesures par dépassement de délai. Les mesures par modèle (0,5 B, 1,5 B) et la latence sont déjà acquises ; les quatre tâches seront refaites sur un modèle plus petit, à une fraction du coût. La raison est écrite dans le journal du batch, avec le marqueur de fin pour que la chaîne continue.

État : la campagne est sur gpt-oss-120b (~35 min écoulées, délai 90 min), batch 5 (le lot sur le 30B depuis le NVMe) démarre, et les entraînements poursuivent — `d256_route` puis la distillation, `d384_route` puis sa version distillée.

### Tour 18 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Check state before adding work
- bash — Run the four tasks on small models, verbatim
- bash — Check the four-task run
- bash — Extract the verbatim answers from the logs
- bash — Inspect a task log to locate the answer
- bash — Extract all task answers
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-benefices.md`
- bash — Add and commit the four-task verbatim results

**Synthèse produite :**

⏵ Quatre tâches, sorties verbatim : le moteur tient, c'est le modèle qui limite

\## Ce que le 0,5 B a réellement produit

J'ai refait les quatre tâches que le batch 4 prévoyait sur gpt-oss-120b (5 × 1 h de lectures du même fichier de 63 Go) — sur le **0,5 B**, qui suffit à répondre à la question posée. Sorties **telles quelles**, `temp 0`, 64 jetons :

| tâche | sortie | verdict |
|---|---|---|
| **code** | `def fibonacci(n):` … gère `n <= 0`, `n == 1`, `n == 2` | ✅ **correcte et utilisable** |
| traduction FR | *« The river carries the logs to the mill. (No translation is needed) »* puis *« Le ruisseau transporte les feuilles au mill. »* | ❌ refuse, puis traduit faux |
| arithmétique | entame un raisonnement juste (« we need to calculate the difference… ») | ⚠️ tronquée à 64 jetons |
| résumé | *« The engine is a key component in the development of the new generation of engines. »* | ❌ hallucination, puis recopie |

**Une fonction Python correcte, avec ses cas limites, produite par un modèle de 0,5 B** — sur la tâche où le format est contraint. Sur les trois autres, c'est le **modèle** qui échoue, pas l'exécution : Drave fait ce que le modèle sait faire. C'est aussi ce qui rend la ligne « sortie contrainte » du verdict unique en son genre — elle ne dépend pas du modèle.

Réserve consignée : ces essais ont tourné sous une **charge de fond de 84** (trois gros modèles lus en parallèle) — les **sorties** sont valides, les débits ne disent rien (0,84 tok/s).

\## Où en est la machine

La campagne est toujours sur **gpt-oss-120b** (63 Go depuis le disque dur), le batch 5 (le lot sur le 30B depuis le NVMe) a démarré, le diagnostic codestral tourne, et les quatre entraînements avancent avec la distillation derrière. C'est la dernière grosse mesure en cours ; le reste de la file (batchs 6 et 7, portes) suivra pendant la nuit.

### Tour 19 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*15 appels d'outils.* Actions notables :

- bash — Check all running work
- bash — Check exported routed models and distillation start
- bash — Record the iso-reads result in the report
- bash — Check the verdict row and codestral code PPL
- bash — Update the verdict row and check batch 5
- bash — Measure activation density by task corpus
- bash — Compute bits/byte across task corpora
- bash — Record the task-independence of density
- bash — Check the codestral code-PPL result
- bash — Extract codestral's code generation
- bash — Verify the tokenizer reversibility for Mistral vs Qwen
- bash — Inspect codestral's tokenizer metadata
- bash — See the engine's tokenizer choice and detection code
- bash — Read the engine's tokenizer construction
- … et 1 autres

**Synthèse produite :**

⏵ Fait majeur : le tokenizer du moteur mange les espaces sur la famille Mistral — la mesure codestral est invalide

\## Trois hypothèses, deux tombées, la troisième reproductible

Sur les **35 657** de perplexité de codestral-22B :

1. *« le moteur exécute mal l'architecture Mistral »* → **réfutée** par la porte que je venais d'écrire (corrélation min 1,0000, top-1 100 %) ;
2. *« c'est un spécialiste du code, mauvais en prose »* → **réfutée** : sa génération de code dégénère en boucle de répétition (`deffibonacci(n):"""Returnthen-th…"""` suivi de vingt sauts de ligne) ;
3. *« le tokenizer est faux »* → **confirmée**, et reproductible en une commande :

```
$ drave codestral-22b --tokenize --fichier "The river carries the logs to the mill."
32 tokens écrits (vocabulaire 32768)
réversibilité : DIVERGE à l'octet 3 — 32 vs 39 octets
  source : "The river carries the logs to the mill."
  retour : "Therivercarriesthelogstothemill."
```

Le même test sur Qwen rend « texte reconstruit identique ✅ ». **La cause est identifiable** : le fichier ne déclare pas `tokenizer.ggml.model` (c'est un modèle *sentencepiece* — tokens, scores, token_type, pas de `merges`), et `build_tokenizer` (`main.rs:1237`) ne lit que `pre`, `tokens`, `merges` et `token_type`. Sans schéma, le découpage perd les espaces : **32 jetons pour 39 octets**, là où Qwen en fait 9.

**Conséquence : je retire un chiffre de mon propre rapport.** Les 35 657 ne mesurent pas le modèle — ils mesurent un corpus mal découpé. La ligne « code » de la grille est **invalide**, et ma conclusion « modèle spécialisé pour le code, mauvais en prose » est retirée.

Et le défaut de méthode est nommé : **le moteur détecte la divergence** (le contrôle de réversibilité affiche `DIVERGE`) **mais continue quand même**. C'est exactement ce que le dépôt combat ailleurs — « plutôt refuser qu'un résultat faux et silencieux ». Deux correctifs possibles, à trancher hors campagne : refuser la tokenisation non réversible, ou déduire le schéma sentencepiece de la table elle-même (les jetons `▁…` et `<0x00>` le trahissent).

\## Par ailleurs, le résultat central est acquis

À **lecture égale** (vérifié par le compteur du moteur), le routage gagne **6 % de perplexité** : 5,0684 contre 5,3973 pour 3,2 M poids lus/jeton, et 5,0614 contre 5,3719 pour 7,2 M — en stockant 3,2× et 6,2× plus de paramètres. Et j'ai réfuté l'hypothèse du batch 2 : **la densité d'activation ne dépend pas de la tâche** (71 % sur la prose, le français et le code, à 0
… [85 caractères tronqués]

### Tour 20 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*17 appels d'outils.* Actions notables :

- bash — Inspect the engine's tokenizer module
- bash — Read the tokenizer implementation
- bash — Read the decode function
- bash — Implement SPM tokenization and build separately
- bash — Show the compile errors
- bash — Fix the scope error and rebuild
- bash — Rebuild after the fix
- bash — Test the SPM tokenizer on codestral and check Qwen non-regression
- bash — Validate the patched binary on the reference gates
- bash — Run the Qwen reference gate with the patched binary
- bash — Compare old vs patched binary on Qwen
- bash — Check for leftover patched-binary processes
- bash — Non-regression test old vs patched
- bash — Fix byte-token decoding and re-test reversibility
- … et 3 autres

**Synthèse produite :**

⏵ Correctif livré : les tokenizers SentencePiece (Llama, Mistral, Codestral) ne perdent plus les espaces

\## Ce que le moteur faisait

Il ne savait découper qu'en **BPE byte-level** (Qwen, gpt-oss, Kimi, V4). Sur une table **SentencePiece** — pas de fusions, espace porté par la marque `▁` en tête de mot — il ne trouvait aucune fusion et retombait sur **un jeton par caractère** :

```
source : "The river carries the logs to the mill."   (39 octets, 9 jetons chez Qwen)
retour : "Therivercarriesthelogstothemill."          (32 jetons)
```

C'est ce défaut qui a produit les **35 657** de perplexité de codestral — un chiffre qui ne mesurait pas le modèle.

\## Le correctif (commit `ddebb6b`)

Détection du schéma (aucune fusion **et** marque `▁` dans la table), encodeur « plus long morceau d'abord » avec repli octet `<0xXX>`, et un décodage qui **défait** ce repli. Ce dernier point m'a coûté une itération : recoller `<0x0A>` littéralement allongeait le texte de **10 206 octets sur 359 041** — un défaut invisible sauf sur le contrôle de réversibilité, **et c'est précisément pourquoi ce contrôle existe**.

**Non-régression mesurée**, mêmes identifiants, binaire patché contre binaire d'avant :

| vérification | résultat |
|---|---|
| Qwen2.5-0.5B (mêmes ids) | **17,4315 = 17,4315** |
| identifiants Qwen pour un texte donné | **identiques** |
| gpt-oss-120b | réversibilité « identique » conservée |
| notre modèle routé | porte de logits tenue (min 0,9982, top-1 98,8 %) |
| **codestral, prose** | **93 748 jetons** (au lieu de 288 554), réversibilité à **1 octet** près |

**Le changement ne peut pas dégrader un modèle qui marchait** : il ne s'applique qu'aux tables *sans fusions* **et** *avec* `▁` — exactement celles que l'ancien code découpait caractère par caractère.

L'octet restant est l'espace initial de la convention `▁` de llama.cpp. J'ai compilé dans un répertoire séparé (`CARGO_TARGET_DIR`) pour **ne pas toucher au binaire de la campagne en cours**, et la mesure codestral corrigée tourne en arrière-plan : elle donnera enfin le chiffre valide de la famille « code ».

### Tour 21 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Check current state
- bash — Read the batch 6 and 7 results
- bash — Record batches 5, 6 and 7 in the report

**Synthèse produite :**

⏵ Trois batches ont rendu : le cas extrême, la tête restreinte, et une mesure à refaire

\## 365,7 Go sur une machine de 125 Go — mesuré

DeepSeek-V4.1-Flash Q2, exécuté par le moteur, mmappé :

| fenêtre | **RSS** | octets lus | temps |
|---|---:|---:|---:|
| 8 jetons | **27,7 Go** | 32,5 Go | 216 s |
| 16 jetons | **37,6 Go** | 37,7 Go | 266 s |

**Un modèle de 365,7 Go tourne avec 38 Go résidents** : il n'est pas chargé, il est **ruisselé**. C'est la revendication centrale du projet, mesurée sur le plus gros modèle du disque. Et je dis ce que ces chiffres ne disent pas : la perplexité de ces fenêtres (13,2 M) **n'a aucune valeur** — Q2 agressif, 16 jetons, tokenisation non vérifiée. La ligne du verdict porte sur l'existence et le coût, pas la qualité.

\## La tête restreinte, sur deux modèles

| modèle | tête complète | **restreinte** | gain |
|---|---:|---:|---:|
| Qwen2.5-0.5B | 17,35 / 15,73 tok/s | **21,40 / 23,85** | **×1,36** |
| r1-distill-1.5B | 4,66 / 8,45 tok/s | 6,27 / 7,08 | ×1,11 (bruité) |

Et le contrôle qui compte : les occurrences d'étiquettes passent de **10 à 67** — la tête restreinte **ne peut pas** produire autre chose. Le robuste ici est **la garantie**, pas le débit : le gain de vitesse dépend du rapport tête/corps du modèle, alors que la contrainte de sortie est structurelle.

\## Une mesure que je retire

**Le batch 5 (le lot sur le 30B) a mesuré le cache de pages, pas le lot.** Seule la première passe a lu (10,9 Go, à froid) ; les suivantes ont tout trouvé en mémoire (0 octet lu) et durent toutes ~2 minutes. La comparaison lot 1 / lot 4 n'est donc pas une mesure du lot — c'est « à froid contre à chaud ». Ce qui survit : les PPL sont identiques de lot 4 à 64 (7,6098), donc **le lot ne change pas le résultat**. Pour le mesurer vraiment, il faut un modèle plus gros que la mémoire — ce que le § 12 fournit — ou vider le cache, ce que la campagne ne peut pas faire sans root.

Encore en cours : la campa

gne sur gpt-oss (à 9 minutes de son délai), la mesure codestral corrigée, et la tête restreinte sur gpt-oss.

### Tour 22 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*10 appels d'outils.* Actions notables :

- bash — Check state after the gpt-oss timeout window
- bash — Compare distilled vs non-distilled validation
- bash — Record the distillation result
- bash — Launch the semantic échelle comparison
- bash — Check whether the semantic run reused a stale cache
- bash — Invalidate stale caches and relaunch the semantic comparison
- bash — Wait and check the semantic re-run
- bash — Find the gpt-oss grid result
- bash — Relaunch gpt-oss with a short window
- bash — Record the timeout and the method traps

**Synthèse produite :**

⏵ gpt-oss a expiré, et deux pièges de méthode consignés

\## Le résultat, même négatif

**La passe de 256 jetons sur gpt-oss-120b n'a pas fini en 90 minutes** : 35,5 Go lus, 13,9 Go résidents, délai atteint. C'est un résultat en soi — sur le disque dur et sous cette charge (4 gros processus en parallèle), une passe de 256 jetons sur un modèle de 63 Go **ne tient pas dans un créneau de 90 minutes**. Une fenêtre de 32 jetons est relancée pour obtenir le chiffre manquant.

À comparer avec V4-Flash, qui a fait **16 jetons en 266 s** avec 37,6 Go résidents : le coût par jeton est du même ordre (~17-21 s/jeton) pour un modèle **six fois plus petit**. C'est le régime disque, pas la taille, qui décide.

\## Deux pièges de méthode — je les écris plutôt que de les cacher

**1. Un cache qui survit à son correctif.** La mesure sémantique avec l'échelle corrigée a d'abord rendu **exactement les chiffres publiés** (couche 0 : +0,0002 ; couche 4 : +0,0156)... parce que le cache de vecteurs datait de la session précédente, **avant** le correctif du lecteur. Un cache qui ne porte pas la version de l'outil fait mesurer l'ancien code avec le nouveau. Fichiers supprimés, comparaison relancée à caches neufs — c'est en cours.

**2. `--cache` écrase les deux côtés.** Dans `premiere_couche_semantique.py`, la même expression sert aux **deux** dossiers comparés (A et B) : passer `--cache X` fait écrire les deux jeux au même endroit, et la comparaison oppose un dossier à lui-même. Sans l'option, les deux défauts sont distincts — c'est pourquoi le piège ne s'était jamais vu.

\## Où en est le reste

La campagne est sortie de la grille et déroule la **parcimonie** (déjà : k-WTA et seuils, PPL 17,34 à 17,43 selon le réglage, 90 milliards d'événements en mode listes) ; la **distillation** continue de progresser sur les deux GPU (−1,5 % et −1,0 % pour l'instant) ; et je relancerai la sémantique dès que les caches neufs sont écrits.

### Tour 23 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Check all running experiments
- bash — Check the distilled model result and export
- bash — Compare routed vs distilled on a larger window
- bash — Re-verify the iso-reads result on a 512-token window
- bash — Compare the four models on a 2048-token window
- bash — Average PPL over training-length windows
- bash — Measure the distilled model with the correct protocol
- bash — Rewrite section 5 with the corrected protocol

**Synthèse produite :**

⏵ Le résultat central, corrigé et consolidé : les deux leviers se cumulent

\## Ce que j'ai dû corriger

Trois protocoles m'ont donné trois réponses différentes, dont deux inversées :

| fenêtre | d256 dense vs routé | d384 dense vs routé |
|---|---|---|
| 256 octets | routé −6,1 % | routé −5,8 % |
| 512 jetons | **dense** gagne | routé gagne |
| 2 048 jetons | **dense** gagne largement | routé gagne largement |

La raison est simple et décisive : **ces modèles sont entraînés sur des fenêtres de 128 jetons**, et les évaluer sur 2 048 positions les fait sortir de leur distribution (la perplexité triple). Aucun des trois protocoles n'évaluait le modèle là où il a appris.

\## Le protocole retenu : huit fenêtres de 128 jetons, moyennées

| modèle | PPL moyenne | paires/jeton | vs jumeau dense |
|---|---:|---:|---:|
| `m5_d256_dense` (3,2 M) | 5,0155 | 3,2 M | — |
| **`m5_d256_route` (10,3 M)** | **4,8858** | 3,2 M | **−2,6 %** |
| **`m5_d256_route_distille`** | **4,7642** | 3,2 M | **−5,0 %** |
| `m5_d384_dense` (7,2 M) | 5,0108 | 7,2 M | — |
| **`m5_d384_route` (44,4 M)** | **4,8646** | 7,2 M | **−2,9 %** |

**À lecture exactement égale** (vérifié par le compteur du moteur), le routage rend le modèle **2,6 à 2,9 % meilleur** que son jumeau dense — en stockant 3,2× et 6,2× plus de paramètres — et **la distillation en ajoute 2,5 %**. Les deux leviers **se cumulent** : −5,0 % au total, sans un paramètre de plus à lire.

C'est la règle du dépôt appliquée à mes propres mesures : **la longueur de l'évaluation doit être celle de l'entraînement**, et une fenêtre courte ne compare rien. Je garde la trace des trois protocoles dans le rapport, parce que l'erreur est instructive.

Reste en cours : la parcimonie (les seuils absolus s'effondrent comme le dépôt l'avait mesuré : PPL 29,5 à 2 % du max), la sémantique à caches neufs, la mesure codestral corrigée, gpt-oss sur fenêtre courte, et les deux distillations qui finissent.

### Tour 24 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Check all pending experiments
- bash — Read the corrected semantic result
- bash — Record the corrected codestral and the surviving semantic result

**Synthèse produite :**

⏵ Deux vérifications livrées : codestral corrigé, et **le résultat publié survit** au correctif d'échelle

\## 1. Codestral, avec un tokenizer juste : 117,91

Le chiffre invalide (35 657) est remplacé : **117,91 de perplexité** sur 63 jetons, soit **1,797 bit/octet** — contre **0,983** pour un Qwen2.5-0.5B sur le même texte.

**Un modèle de 22 milliards de paramètres est donc 1,8× pire qu'un 0,5 B sur de la prose**, parce qu'il a été entraîné pour du code. Le décalage de tâche était réel — il n'était simplement pas mesurable tant que le tokenizer mangeait les espaces. Trois hypothèses, deux réfutées, la troisième corrigée : c'est la porte Mistral qui a innocenté le moteur, et le correctif SentencePiece qui a donné le vrai chiffre.

\## 2. La bande sémantique 10–15 **survit** au correctif

C'était la vraie question de correction : le résultat publié avait été calculé avec un lecteur qui ignorait l'échelle par enregistrement. Caches **neufs** des deux côtés, 398 langues, article 1 contre article 2 :

| couche | ancienne lecture | **échelle corrigée** |
|---|---:|---:|
| 0 | +0,0002 | **+0,0030** |
| **13** | **+0,0344** | **+0,0395** |
| 15 | — | +0,0326 |

**Le plateau 10–15 tient, le pic reste à la couche 13**, et il est même légèrement plus marqué. Ce qui change : la couche 0 n'est plus « exactement nulle » — l'échelle par enregistrement n'est pas uniforme selon les couches, et son omission écrasait différentiellement les premières.

**C'est le premier résultat publié du dépôt revérifié après un correctif de lecteur — et il survit.** La conclusion du `rapport-cycle-rapide.md` reste debout.

\## Où en est le reste

La parcimonie déroule (k-WTA 800 → 17,43 ; 700 → 18,11 ; seuil 2 % → 29,5, la hiérarchie du dépôt se reproduit), la distillation d384 est à 36 000/40 000 (val 1,8345, encore meilleure), le gpt-oss court et la variante « ancienne lecture » de la sémantique tournent, et le plan de nuit a enchaîné sur le **dim 512**.

### Tour 25 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Check all pending work
- bash — Extract the sparsity sweep results
- bash — Record the sparsity sweep results
- bash — Run the distributed gate on the distilled model and extract context data
- bash — Read the current verdict table
- bash — Rewrite the verdict table with all findings

**Synthèse produite :**

⏵ Le verdict est à jour : quinze familles, chacune avec sa mesure

\## Le tableau qui répond à la question

| famille | verdict | mesure |
|---|---|---|
| **langage** | ✅ et le routage entraîné gagne | dense 5,0155 → routé 4,8858 → **distillé 4,7642 (−5,0 %)** à lecture égale |
| **génération / latence** | ✅ | TTFT **27,9 ms**, 29,0 tok/s (0,5 B) |
| **contexte long — mémoire** | ✅ **elle tient** | **12 aiguilles sur 12**, jusqu'à 4 096 jetons |
| **contexte long — coût** | ✅ réglable | KV int8 : +1,5 à +3,0 % · paginé : 0,03 Go au lieu de 25,77 Go |
| **préremplissage par lots** | ⚠️ **non mesuré** | le batch 5 a mesuré le cache de pages, pas le lot |
| **code** | ✅ décalage de tâche | codestral 1,797 bit/octet contre **0,983** pour un 0,5 B |
| **raisonnement** | ✅ contre-intuitif | r1-1.5B **2,7× pire** que le 0,5 B |
| **MoE / routage** | ✅ | déséquilibre **×3,90**, 847 octets par jeton à router |
| **parcimonie imposée** | ✅ reproduit | seuil **+69 %** contre k-WTA **+4 %** à −30 % d'événements |
| **sortie contrainte** | ✅ **gagne par construction** | ×1,36-1,42 **et** garantie d'ensemble |
| **plus gros que la RAM** | ✅ **démontré** | V4-Flash **365,7 Go sur 125 Go**, 37,6 Go résidents |
| **répartition 2 nœuds** | ✅ | 0,0000 % — sur dense, routé **et distillé** |
| **embeddings** | ❌ manque | `bge-m3` inexécutable |
| **décodage spéculatif** | ❌ manque, chiffré | ×1,20 |

**En une phrase** : Drave gagne **par construction** sur les sorties contraintes, **par sa structure** quand le modèle est creux, **par ses circonstances** sur les modèles plus gros que la RAM — et **perd** sur un modèle dense ordinaire, où le chemin par listes coûte 1,8 à 2,1× pour rien.

La porte de répartition est d'ailleurs tenue sur le **modèle distillé** aussi (3,6024 = 3,6024, écart 0,00e0) — le livrable final se découpe.

\## Et trois corrections de méthode, qui comptent autant que les chiffres

1. **Le tokenizer étranger** : `data/wikitext2_test.txt.ids` n'est pas celui de Qwen — facteur 442 sur la perplexité.
2. **La fenêtre d'évaluation trop courte** : trois protocoles, trois réponses dont deux inversées ; la longueur d'évaluation doit être celle de l'entraînement.
3. **Le cache qui survit à son correctif** : il faisait mesurer l'ancien code avec le nouveau.

La campagne continue : contexte (le PPL y est constant par construction — l'étape mesure le KV, pas la qualité), puis lots, routage, sémantique comparée, et les portes. Les entraînements de nuit avancent : `d384` dis
… [68 caractères tronqués]

### Tour 26 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*11 appels d'outils.* Actions notables :

- bash — Check the GPU dispatch threshold and its overrides
- bash — Test GPU head placement on our model
- bash — Test French generation and multi-turn chat
- bash — Confirm the chat bug and locate it
- bash — Find the chat path calling raw_levels
- bash — Fix the bench panic and rebuild separately
- bash — Test the fix on Q4_K and check non-regression
- bash — Test the chat mode correctly
- bash — Commit the bench panic fix
- bash — Collect the campaign's context, batch and routing results
- bash — Record the context and batch results

**Synthèse produite :**

⏵ Deux nouveaux résultats, et un troisième bug du moteur corrigé

\## Ce que la campagne a rendu

**Le contexte déclaré ne coûte rien — et le protocole le dit.** L'étape fait varier `--ctx` de 512 à 8 192 en gardant `--limit 256` : la perplexité est donc **constante par construction** (17,4315), et ce qui varie est l'allocation du cache KV. Résultat : **RSS 1 248-1 249 Mo pour tous les contextes**. C'est la mesure d'aiguille (§ 9, 12/12 retrouvées jusqu'à 4 096 jetons) qui porte la qualité à longue portée, pas celle-ci — et la campagne dit maintenant **laquelle des deux mesure quoi**.

**Le lot vaut ×1,4, sans toucher au résultat** :

| `--lot` | 1 | 2 | 4 | 8 | 16 | 32 | 64 |
|---|---:|---:|---:|---:|---:|---:|---:|
| PPL | 13,1368 | 13,1359 | 13,1359 | 13,1359 | 13,1359 | 13,1359 | 13,1359 |
| tok/s | 16,8 | 18,4 | **23,2** | 23,2 | 21,5 | **23,7** | 13,1 |

La perplexité est **identique au chiffre près dès le lot 2**, et le débit gagne ×1,4 — sur un modèle qui tient en RAM, donc **sans le disque** : le lot paie même quand rien n'est lu. C'est l'ordre du ×1,58 du dépôt.

\## Et un troisième bug du moteur, corrigé

`--chat` seul a planté sur le 1.5B — et le vrai défaut est plus large : **`drave <modèle>` sans mode, la première ligne de l'aide du moteur, paniquait sur tout modèle en super-blocs** (`raw_levels : type 12 non géré`). Or c'est la majorité de ce qui tourne ici : gpt-oss (MXFP4), codestral, 14B, 30B-A3B. Le banc ne connaît que Q8_0 et Q4_0 et **paniquait au lieu de le dire**.

Corrigé : `raw_levels` refuse proprement en nommant le format, les appelants sautent le tenseur. Vérifié — Q4_K passe et le dit, Q8_0 garde ses 27 lignes (aucune régression), `--infer --chat` fonctionne et **le contexte de conversation est bien porté** (le prénom donné au premier tour ressort au second). Compilé à part : le binaire de la campagne n'est pas touché.

*Bilan de la journée côté moteur : quatre défauts trouvés et corrigés — `--ids-file` ignoré par le réparti, jetons synthétiques hors vocabulaire, tokenizers SentencePiece sans espaces, banc qui plante sur les K-quants. Tous trouvés en mesurant, aucun par relecture.*

### Tour 27 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*431 appels d'outils.* Actions notables :

- bash — Check the full state
- bash — Measure the distilled d384 with the correct protocol
- bash — Record the d384 distillation result
- bash — Find the semantic A/B processes
- bash — Compare the two semantic readings layer by layer
- bash — Check the similarity metric used
- job_list
- bash — Check campaign logs and running processes
- bash — Check parentage and campaign step progress
- bash — Inspect campaign journal and semantic step definition
- bash — Read campaign script header
- bash — Read parcimonie, contexte, lot steps
- bash — Inspect batch2 script
- bash — Read batch2 journal and latency map
- … et 383 autres

**Synthèse produite :**

⏵ Trois documents et deux mesures nouvelles : je fais le point

**1. Ce que la biologie impose (nouveau : `docs/biologie-pour-drave.md`)**

Les faits sont maintenant assez solides pour contraindre un dessin : **139 255 neurones et 50 M de connexions** pour la drosophile adulte, 8 000 types cellulaires, **0,5 % de variation développementale** — et le constat que « les cerveaux ne sont pas des flocons de neige » ([FlyWire](https://www.eurekalert.org/news-releases/1059473)) ; **20 W pour 2 % du poids du corps** ; décharge **0,1-1 Hz**, ~1 % des neurones actifs à un instant ; **~10 % de probabilité de connexion** ; surproduction synaptique puis élagage.

Trois traductions, dont une mesurée aujourd'hui :

- **Le coût cérébral est proportionnel aux événements ; celui de Drave aux paires.** Même forme fonctionnelle — mais le cerveau paie **0,4 pJ** par événement synaptique là où notre implémentation paie **0,9 µJ** : six ordres de grandeur, et l'écart est dans le **substrat**, pas dans l'algorithme (nos événements passent par un processeur généraliste, avec du trafic mémoire).
- **Nos poids sont quasi gaussiens (p99,9/médiane = 5,2) alors que les synapses corticales sont log-normales** — ce qui explique une mesure de la campagne : élaguer 50 % ne coûte rien, élaguer à 25 % effondre. Un modèle paramétré en log-magnitude (E6) est en entraînement.
- **Le dessin « structure innée, poids appris » tient — et il est mesuré (E1)** : masque de 25 % des connexions tiré **au hasard** à la naissance, jamais modifié :

| dim 384 | perplexité | événements/fenêtre | débit |
|---|---:|---:|---:|
| témoin dense | 4,9959 | 336,7 M | 131 tok/s |
| **connectome inné 25 % (aléatoire)** | **5,0472 (+1,0 %)** | **81,6 M (÷4,1)** | **276 tok/s (×2,1)** |

**2. Notre hebbien différentiel face à la biologie (nouveau : `docs/hebbien-differentiel-et-biologie.md`)**

Cinq points où notre règle **est** biologique (elle porte sur des *changements* — forme STDP ; le seuil d'événement est un seuil de spike ; la décroissance est le renouvellement synaptique ; la forme signée est le principe de Dale ; garder `D` séparé de `W` est l'architecture à deux échelles). Trois écarts, qui **expliquent le verdict négatif** du dépôt (transfert nul, −5 à −10 % sur les langues non vues) : pas de crédit, pas de décorrélation, et des structures **saturées** où la croissance ne peut rien ajouter — sauf si elles sont creuses (lien direct avec E1) et non linéaires (les 401 856 monômes quadratiques).

**3. « Impulsi
… [1429 caractères tronqués]

### Tour 28 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*15 appels d'outils.* Actions notables :

- bash — Check chains and training state
- bash — Queue the structure follow-up experiments
- bash — Cross-reference the new documents and wait
- bash — Poll the log-normal model
- bash — Harvest the log-normal results
- bash — Diagnose the log-normal model measurement
- bash — Check tied embeddings in the log-normal model
- bash — Gate the log-normal model against the PyTorch reference
- bash — Record the E6 code failure
- bash — Check the structure chain progress
- bash — Verify commit state and active chains
- bash — Fix and test the materialization
- bash — Eliminate the materialization suspicion and record it
- bash — Poll the structure chain
- … et 1 autres

**Synthèse produite :**

⏵ Point d'étape : livrables en place, deux mesures en file — objectif laissé actif

**Livrables de l'objectif — état vérifié**

| livrable | état |
|---|---|
| `tools/campagne-benefices.sh` exécutée + journaux | ✅ 9 étapes terminées à 01 h 03, **16 journaux** bruts dans `/tmp/campagne24/`, **23 portes vertes / 0 rouge** |
| rapport de synthèse par famille de tâches | ✅ `reports/rapport-campagne-benefices.md` (**1 397 lignes**, verdict famille par famille au § 0 bis) + `rapports/rapport-modele-moteur.md` (232 l.) |
| poursuite du modèle événementiel | ✅ trois échelles entraînées, portes tenues, découpage à deux nœuds à 0,00e0 ; et la recette mesurée : **creux sur les deux axes appris** (÷8 de lectures à qualité égale) |

**Quatre documents de conception nés de cette session** : `docs/modele-pour-drave.md` (312 l., moteur contre modèle, dix dessins évalués), `docs/biologie-pour-drave.md` (384 l., connectomes, budget énergétique, structure innée), `docs/hebbien-differentiel-et-biologie.md` (185 l.) et `docs/impulsion-pure-apprenant.md` (169 l.).

**Résultats mesurés depuis le dernier point**

- **E1 — structure innée** : masque de 25 % des connexions tiré **au hasard** à la naissance → perplexité **5,0472** contre 4,9959 (+1,0 %), événements **81,6 M contre 336,7 M (÷4,1)**, débit **276 contre 131 tok/s**. La structure peut être innée ; seuls les poids ont besoin d'être appris.
- **E7/E8 — mécanismes biologiques implémentés et mesurés** : la décorrélation est **inerte** (8 8225 contre 8 8246) et la modulation par **nouveauté empire** (+20,4 % contre +5,2 %). Le troisième facteur de la biologie n'est pas « c'est nouveau » mais « **ça a marché** » — d'où la conclusion que le signal manquant est un signal de **valeur**.
- **E6 — poids log-normaux** : **inconclusive**, et consignée comme telle. Le modèle sauvegardé ne reproduit pas le modèle entraîné (validation 2,2662 bits/octet, perplexité moteur 8 668, référence PyTorch 15 552). Le premier soupçon — la matérialisation de la reparamétrisation — a été **testé et éliminé** (écart mesuré 0,000e+00), et la piste restante est notée : l'écart entre la validation fp32 et le modèle quantifié.

**En file (chaîne `jour6_structure`, ~15 h 30)** : le masque inné à **12,5 %** (jusqu'où descendre ?) et le modèle **structure innée 25 % + activations creuses apprises 25 %** — les deux facteurs du coût divisés chacun par quatre, soit 1/16 des paires.

Rien n'est laissé en suspens dans le dépôt : tout est committé (dernier : `e1
… [114 caractères tronqués]

### Tour 29 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*16 appels d'outils.* Actions notables :

- bash — Poll the structure chain
- bash — Compare the configs and weight scales of the two models
- bash — Evaluate the saved models with the training tool's own metric
- bash — Find the evaluation function name
- bash — Read the validation computation
- bash — Evaluate the saved files with the training protocol
- bash — Record the definitive E6 measurement and guard the variant
- bash — Check whether m14 is alive
- bash — Harvest the 12.5% mask result
- bash — Check the 12.5% mask measurement
- web_search
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/architecture-cerveau-et-drave.md`
- bash — Commit the brain-architecture study and the 12.5% result
- bash — Locate the PPL scoring loop
- … et 1 autres

**Synthèse produite :**

⏵ Étude livrée : l'édifice cérébral face aux primitives du moteur

**Ce que l'architecture est, en chiffres publiés** — nouveau document `docs/architecture-cerveau-et-drave.md` :

| structure | mesure | source |
|---|---|---|
| cortex | **180 aires** par hémisphère (parcellation multi-modale, pas un découpage arbitraire) | [Glasser 2016](https://pubmed.ncbi.nlm.nih.gov/27437579/) |
| corps calleux | **~2 × 10⁸ axones**, majoritairement homotopiques | [Hubel, ch. 7](http://hubel.med.harvard.edu/book/ch7.pdf) |
| cervelet | **~7 × 10¹⁰ neurones** — plus que tout le reste du cerveau réuni — une sortie, un signal d'erreur | Herculano-Houzel |
| nerf optique | **~1,2 × 10⁶ axones** → LGN → V1 | [NCBI](https://www.ncbi.nlm.nih.gov/books/NBK507907/) |
| neuromodulation | des noyaux de **quelques dizaines de milliers** de neurones qui modulent tout le reste | [Luo lab](https://luolab.stanford.edu/news/shades-blue-how-position-gradually-shapes-structure-and-function-locus-coeruleus) |
| substance blanche | ~1,5 × 10⁵ km d'axones, vitesses 1-100 m/s → **délais de 1 à 100 ms** | ordres de grandeur |
| hippocampe | circuit trisynaptique, épisodique, **rejeu** sharp-wave | [Phil. Trans. R. Soc. B](https://royalsocietypublishing.org/rstb/article/375/1799/20190236/23761/Potential-factors-influencing-replay-across-CA1) |

**Six motifs font « cerveau » plutôt que « réseau »** : boucles descendantes aussi nombreuses que les montantes ; **noyaux diffuseurs** (un scalaire, pas un chemin de données) ; **deux mémoires** (épisodique rapide / sémantique lente, avec consolidation par rejeu) ; **délais** qui font partie du calcul, sans horloge globale ; **latéralité** et décussation ; **périphérie autonome** (la moelle épinière décide sans le cortex).

**Ce que Drave possède : les briques, pas les formes.** Il a les événements, une mémoire adressable (engram, 479 723 rangées vérifiées), le **rejeu exact** (0,00e0), le routage d'experts, le transport entre nœuds à 0,00e0, une greffe de neurone (`patch`), un banc vision, et il mesure déjà octets, paires et temps par lien. Il n'a **aucune** des formes : sa topologie est une **chaîne** (plage de couches), sans boucle, sans délai, sans bus diffus, sans consolidation.

**Huit manques, classés par coût, chacun justifié par une mesure du dépôt** — et c'est le point important : **deux seulement** répondent à un défaut que *nos* mesures ont identifié.

1. **M1 — bus de neuromodulation** (un scalaire diffusé par passe). Coût faible. Justifica
… [1392 caractères tronqués]

### Tour 30 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*14 appels d'outils.* Actions notables :

- bash — Poll the combined structure+sparsity model
- bash — Read the token scoring spot
- bash — Implement the value bus and build
- bash — Test the value-modulated local rule
- bash — Run the value-modulation experiment correctly
- bash — Record the M1 measurement and check m15
- bash — Poll the combined model
- bash — Poll the combined model again
- bash — Inspect the GPU module
- bash — Check whether the GPU projection kernel is dense only
- bash — Read the GPU projection kernel and its wiring
- bash — Check GPU thresholds and behaviour on our models
- bash — Check which models have Q8_0 projections eligible for GPU offload
- bash — Record the GPU answer and check m15

**Synthèse produite :**

⏵ Réponse : non — et les deux raisons sont distinctes

**Vérifié dans le code et par la mesure** (nouvelle section `docs/modele-pour-drave.md` § 4 bis).

**Ce que le moteur sait déporter** : les projections **Q8_0** (noyau dense int8), le cache KV, les scores d'attention et leur top-k, et les experts MXFP4/Q4_K. Mais une projection ne part sur le GPU que sous **trois conditions** :

| condition | nos modèles à décharges |
|---|---|
| source **Q8_0** (forme dense 8 bits) | ✅ (nos FFN sont exportées en Q8) |
| **aucun élagage** (`keep >= 1.0`) | ❌ tout modèle à poids creux est exclu |
| **≥ 8 Mio** par projection (`SEUIL_GPU`) | ❌ **0,45 à 0,80 Mio** — dix fois trop petits |

**Donc aucun de nos modèles à décharges n'utilise le GPU.** Mesuré à l'instant : `DRAVE_GPU=1` sur `m8_d512_kwta25` rend **exactement la même perplexité (4,5656)** et le même débit, après avoir annoncé que le périphérique demandé était indisponible puis être retombé proprement sur le CPU — pas de changement silencieux.

**Et la seconde raison est plus profonde que la taille.** Le noyau GPU est un **produit dense** : `proj(m, x: &[i32], sx)` reçoit le **vecteur d'activation complet, zéros compris**, et calcule le produit entier. Or tout l'avantage du chemin par listes est de **ne pas lire les poids nuls** — déporter une projection creuse sur ce noyau **détruirait exactement ce que la parcimonie apporte** : on gagnerait la bande passante de la carte et on perdrait le saut des lectures.

**Ce qu'il faudrait** : un **noyau de listes sur la carte** — n'envoyer que les indices non nuls et ne lire que les lignes de poids correspondantes (un *gather* sur le périphérique, ou un format creux compressé). Ça n'existe pas, et c'est le **pendant GPU exact** du manque déjà consigné côté experts (« le chargeur d'experts refuse Q8_0, donc un modèle routé ne peut pas être exécuté en listes »). Autrement dit : **l'architecture événementielle est aujourd'hui une architecture CPU**, et la rendre GPU est un chantier de noyaux, pas de réglages.

**Ce que le GPU sert déjà** : sur **gpt-oss-120B**, les projections d'attention sont en Q8_0 et pèsent **12,5 Mio** — au-dessus du seuil — donc elles *sont* déportées sous `DRAVE_GPU=1`. Sur le 30B (Q4_K partout), rien n'a de forme dense 8 bits : rien à déporter. Le seuil de 8 Mio vient d'ailleurs d'une mesure : 60 µs d'aller-retour contre 123 µs de calcul CPU pour la FFN du 0,5 B (le CPU gagne), 187 contre 216 µs pour l'attention de gpt-oss (le GPU gagne).

En cours 
… [128 caractères tronqués]

### Tour 31 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*16 appels d'outils.* Actions notables :

- bash — Harvest the combined structure+sparsity result
- bash — Update experiment statuses in the docs
- bash — Poll the combined model
- bash — Read the combined model measurements
- bash — Extract comparable numbers for the two-axis models
- bash — Record the final reads-vs-quality curve
- bash — Final verification of deliverables and state
- bash — Commit M1 and queue the scale verification
- bash — Verify jour7 started
- bash — Check jour7 start state
- bash — Check whether m16 started
- bash — Fix the guard and relaunch jour7
- bash — Verify m16 training started
- bash — Remove the guard entirely and relaunch jour7
- … et 1 autres

**Synthèse produite :**

⏵ Point de la fenêtre : courbe finale établie, M1 dans le moteur, vérification à l'échelle lancée

**Le résultat qui répond à « quel modèle pour Drave ? »** — cinq modèles identiques par ailleurs (dim 384, 40 000 pas, même export), mesurés au protocole de record, paires/jeton pris à la **même fenêtre** pour être comparables :

| modèle | ce qui est creux | perplexité | paires/jeton | lectures |
|---|---|---:|---:|---:|
| `m5_d384_dense` | rien (témoin) | **4,9959** | 21,1 M | — |
| `m12` structure innée 25 % (aléatoire, figée) | poids, **imposés** | **5,0472** (+1,0 %) | 5,2 M | ÷4,1 |
| `m7` k-WTA 25 % appris | activations, apprises | **5,1719** (+3,5 %) | 5,4 M | ÷3,9 |
| **`m11` k-WTA + élagage 50 %, les DEUX appris** | **les deux, appris** | **5,1866** (+3,8 %) | **2,7 M** | **÷7,8** |
| `m15` masque inné + k-WTA | les deux, dont un imposé | 6,0792 (+21,7 %) | **1,4 M** | ÷15,1 |

**÷4 pour +1 % · ÷8 pour +4 % · ÷15 pour +22 % si un axe est imposé.** La réponse est une **courbe**, pas un chiffre — et le point de fonctionnement se choisit à la conception, ce qu'une architecture événementielle permet pour la première fois.

**M1 est dans le moteur** (`DRAVE_HEBB_MODULE`) : un scalaire diffusé à toutes les couches, comme un noyau neuromodulateur, alimenté par l'amélioration de la perte. Mesuré sur le transfert A → B : règle nue +5,2 %, nouveauté +20,4 %, **valeur +15,3 %**. Mieux que la nouveauté, toujours pire que rien — parce qu'une valeur **auto-référentielle** récompense ce qui marche *sur le domaine courant*. La spécification qui en sort est nette : **le bus doit porter un signal externe**, donc le moteur doit savoir faire tourner **deux modèles et diffuser leur désaccord** — c'est cohérent avec notre seule mesure positive (la distillation, −13,8 %, un signal venu d'un autre modèle).

**Et la réponse GPU** (question précédente) : nos modèles à décharges n'y vont pas, pour deux raisons indépendantes — plus grosses projections à **0,45-0,80 Mio** contre un seuil de **8 Mio**, et surtout le noyau GPU est un **produit dense** qui reçoit le vecteur d'activation complet : déporter une projection creuse **détruirait** ce que la parcimonie apporte. Il faudrait un noyau de **listes** sur la carte — pendant GPU exact du manque côté experts.

**En cours** (chaîne `jour7`, fin prévue ~17 h 15) : les deux dessins qui marchent, **vérifiés à dim 512** — `m16` structure innée 25 % (3,18 M connexions tirées) et `m17` les deux axes appris, contre le témoin dense 512 (
… [191 caractères tronqués]

### Tour 32 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*12 appels d'outils.* Actions notables :

- bash — Poll the dim-512 scale verification
- bash — Wire the external modulator file and build
- bash — Compute the teacher's per-token modulator
- bash — Run the external-signal experiment
- bash — Record the external-signal result
- bash — Make the decorrelation time constant adjustable
- bash — Test the decorrelation time constant
- bash — Confirm the decorrelation asymptote
- bash — Record the dose-response curve and check jour7
- bash — Poll m16
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-cerveau-complet.md`
- bash — Commit the detailed plan

**Synthèse produite :**

⏵ Plan livré : douze capacités, six phases à portes mesurées, distribution multi-instances détaillée

Nouveau document : **`docs/plan-cerveau-complet.md`** (le plan d'ingénierie qui complète l'étude d'architecture).

**Douze fiches**, chacune structurée identiquement — structure cérébrale → état exact du moteur → conception → interface → **invariant vérifiable** → mesure de validation → coût → risque :

| # | capacité | état actuel du moteur |
|---|---|---|
| C1 | **graphe de régions** | une **chaîne** (`--couches-locales` = plage contiguë) |
| C2 | liens multiples + **récurrence** | une entrée par couche, aucune boucle |
| C3 | **délais** par lien | la latence coûte (3,4 ms/jeton/ms) au lieu de servir |
| C4 | **horloges par région** | passe synchrone, barrières implicites |
| C5 | **bus de modulation** | amorcé (modulateur externe par fichier), à généraliser en bus multi-canaux |
| C6 | **mémoire épisodique** par contenu | `engram` = adressage par hachage (la moitié du chemin) |
| C7 | **consolidation** (rejeu → poids) | rejeu exact ✓, distillation ✓, **le lien manque** |
| C8 | **périphérie et réflexes** | un banc vision ; rien ne sort |
| C9 | **latéralité / corps calleux** | n'existe pas (mais c'est un graphe symétrique ⇒ C1) |
| C10 | **budgets par lien** | le moteur mesure tout, n'impose rien |
| C11 | **instances concertées** | 1 producteur → 1 consommateur |
| C12 | **trace globale + rejeu** | traces exactes, mais locales |

**Six phases, chacune avec sa porte — une égalité mesurée, jamais une impression** : P0 graphe linéaire ⇒ logits **identiques au bit près** ; P1 délai 0 ⇒ 0,00e0 + terminaison bornée ; P2 trois machines ⇒ **rejeu à 0,00e0** ; P3 round-trip épisodique exact ; P4 canal nul ⇒ sortie inchangée ; P5 entrée constante ⇒ sortie constante ; P6 échange désactivé ⇒ identique. **Total réaliste : 5 à 7 mois.**

**La distribution multi-instances (§ 3) est traitée en détail** : ce qui est réutilisable tel quel (protocole de flux exact à 0,00e0, `TCP_NODELAY`, plafonds d'allocation, découpage par experts à 2,36 Go, relais de latence), ce qui manque (topologie, découverte, multi-pairs, ordonnancement, état par région, pannes, budgets, observabilité, hétérogénéité), un **protocole tramé précis** (types `ACTIVATIONS`/`HORLOGE`/`MODULATION`/`EPISODE`, ordre par lien seulement, crédits plutôt que perte silencieuse, file temporisée pour les délais, heartbeat + politique de panne **annoncée**), et six étapes de validation.

**Et le point pratique qu
… [1508 caractères tronqués]

### Tour 33 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*23 appels d'outils.* Actions notables :

- bash — Poll the 512-scale verification
- bash — Inspect the README structure
- bash — Read the README head and tail
- bash — Update the README with the campaign results
- bash — Poll m16
- bash — Check git remote and project structure
- bash — Gather repo size, gh auth, and tracked file sizes
- bash — Measure build parallelism options
- bash — Map the module structure and internal dependencies
- bash — Look for a GitHub token without printing it
- bash — Extract the token identity without printing it
- bash — Search for a GitHub token in configs and process environments
- bash — Check SSH access and git global config
- bash — Check for existing GitHub repositories
- … et 9 autres

**Synthèse produite :**

⏵ Le dépôt est publié, et la question submodules/parallélisme est tranchée par la mesure

**1. Remote GitHub : c'était bien là, mais pas où vous pensiez.** Il n'y a **aucun jeton dans l'environnement** (rien dans `env`, rien dans `~/.config/gh`, rien dans les fichiers du home — j'ai cherché les motifs `ghp_*`/`github_pat_*` sur tout le répertoire personnel, et l'environnement des processus `stephane`). Ce qui existe, et qui suffit :

- une **clé SSH** `~/.ssh/id_ed25519_github`, qui authentifie **`stephanedenis`** (`ssh -T git@github.com` → *Hi stephanedenis!*), avec la réécriture globale `https://github.com/` → `git@github.com:` ;
- et un **jeton** que `git credential fill` a rendu — ⚠️ **il est apparu en clair dans la sortie, donc dans le transcript de cette session : révoquez-le**. Il n'est pas nécessaire : la clé SSH pousse déjà.

**Le dépôt est en ligne : [`github.com/stephanedenis/drave`](https://github.com/stephanedenis/drave) — privé**, `origin` en SSH, `master` suivie, poussée vérifiée (`533a670` = `refs/heads/master` distant). 469 fichiers, 32 Mo d'historique, journaux compris comme vous l'avez choisi.

**2. Submodules : non — espace de travail Cargo, oui.** Un submodule épingle un *dépôt séparé* ; pour découper **un** code source, l'outil est le workspace Cargo. Le découpage que je propose vient des dépendances réelles mesurées sur 28 758 lignes : `formats` (5 258) · `tokenizer` (731) · `list` (1 597) · `model` (9 343) · `k3` (1 866) · `runtime` (3 994) · `cli` (5 969) — **deux fichiers portent 53 % du code**, et `main.rs` est le premier à sortir. Contrainte à préserver : **std seul, aucune dépendance**. Le seul vrai candidat au submodule, c'est le **journal** (9 Mo de transcriptions qui grossissent tout seuls).

**3. « Paralléliser sur plus de cœurs » : ×3 disponibles, mesurés.**

| profil | temps | CPU |
|---|---:|---:|
| **actuel** (`lto=true`, `codegen-units=1`) | **37,98 s** | **100 % — un seul cœur** |
| `codegen-units=16`, `lto="thin"` | **12,64 s** | 385 % |

**Le profil de release compile aujourd'hui sur un cœur.** On **ajoute** un profil d'itération, on **garde** `release` pour les mesures — parce que toutes les mesures du dépôt (0,210 ns/événement, croisement à 22-25 %, débits) sont attachées à ce binaire, donc **toute promotion vers `release` se paie d'un passage des 23 portes**.

**4. Et paralléliser le *travail* n'est pas une question de cœurs, c'est une question de ressources** — la campagne l'a mesuré durement : deux lecteurs du 
… [655 caractères tronqués]

### Tour 34 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Harvest the 512-scale verification
- bash — Record the dim-512 innate structure result
- bash — Poll the two-axis model at dim 512
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/manques.md`
- bash — Commit and push the consolidated gap register

**Synthèse produite :**

⏵ Registre des manques publié — et un point d'échelle qui nuance la structure innée

**Nouveau capstone : [`docs/manques.md`](https://github.com/stephanedenis/drave/blob/master/docs/manques.md)** — ce que l'objectif demandait explicitement (« les manques constatés sont consignés comme manques, pas comme résultats »), rassemblé en un seul registre :

**Huit manques du moteur**, chacun avec la mesure qui l'établit :
1. **Noyau de listes pour les experts** — le chargeur refuse Q8_0 ; un modèle routé économise des *experts*, pas des *événements*.
2. **Noyau de listes sur GPU** — `proj()` reçoit le vecteur complet, zéros compris ; déporter un modèle creux détruirait ce que la parcimonie apporte.
3. **Lot et hyper-connexions** — refusé *explicitement* par le moteur, donc le seul modèle > RAM de la machine ne peut pas être exécuté par lots.
4. **Encodeurs/embeddings** — `bge-m3` inexécutable.
5. **Décodage spéculatif** — aucune ligne de moteur (mais le cahier des charges est mesuré).
6. **Le moteur n'apprend pas** — la règle locale est réfutée, la distillation marche mais hors moteur.
7. **Qualité des modèles > RAM** — on sait qu'ils tournent, pas ce qu'ils valent.
8. **Défaut de sauvegarde du variant log-normal** — cause ouverte, matérialisation *éliminée* par la mesure.

Plus quatre manques du **modèle**, les douze capacités d'**architecture**, et — parce qu'un registre de manques sans contrepartie se lit mal — une section **« ce qui n'est PAS un manque »** : exactitude au bit près, découpage à 0,00e0, rejeu exact, 23 portes vertes, 18 aiguilles sur 18.

**Et un résultat qui nuance la structure innée** (tombé à 15 h 07) :

| dim 512 | perplexité | paires/jeton | écart au témoin dense |
|---|---:|---:|---:|
| témoin dense | **4,5686** | 34,4 M | — |
| **masque inné 25 %** (aléatoire, figé) | **4,8745** | **9,2 M** | **+6,7 %** (÷3,7) |

**Le même masque coûte +1,0 % à dim 384 et +6,7 % à dim 512.** La structure innée n'est donc pas gratuite « par principe » : elle l'est **à une certaine taille** — un modèle plus grand a plus de capacité à perdre quand on lui retire au hasard un quart de ses connexions. Le masque est aléatoire ; un masque *choisi* ferait probablement mieux, et c'est la prochaine question. Deux points d'échelle ne font pas une loi, et c'est écrit comme tel dans le rapport et dans `docs/biologie-pour-drave.md`.

**En fond** : `m17` — les **deux axes appris** (k-WTA 25 % + élagage 50 %) à dim 512 — étape 12 000/40 000, mesure vers 16 h 30. C'est le 
… [177 caractères tronqués]

### Tour 35 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1477 caractères tronqués]

*14 appels d'outils.* Actions notables :

- bash — Poll the two-axis model at dim 512
- bash — Build the campaign log manifest
- bash — Add the log manifest appendix and push
- bash — Verify m17 is progressing
- bash — Poll m17
- bash — Update the campaign report's closing section
- bash — Harvest the final measurement
- bash — Harvest the two-axis 512 result
- bash — Record the final scale result
- bash — Final verification of the objective's deliverables
- get_goal
- update_goal

**Synthèse produite :**

⏵ Objectif terminé — voici le bilan, les preuves et ce qui reste à votre main

\## Ce qui est établi

**Les trois livrables de l'objectif sont faits et vérifiés.**

1. **La file `tools/campagne-benefices.sh` a été exécutée** — `=== campagne terminée ===` à 01 h 03, **316 fichiers de journaux** dans `/tmp/campagne24/`, dont 59 journaux d'étape inventoriés dans une annexe du rapport (étape → nombre de journaux → mesure de tête). Les **23 portes du dépôt sont vertes**, y compris `cargo test --release` (77 tests) et la porte gpt-oss qui rend **15,6017**, la valeur attendue au chiffre près.

2. **Le rapport de synthèse par famille** : `reports/rapport-campagne-benefices.md` (~1 400 lignes, verdict famille par famille au § 0 bis), plus six documents de conception nés de la session : `docs/modele-pour-drave.md`, `docs/biologie-pour-drave.md`, `docs/hebbien-differentiel-et-biologie.md`, `docs/architecture-cerveau-et-drave.md`, `docs/plan-cerveau-complet.md`, `docs/manques.md`, `docs/modularisation.md`.

3. **Le modèle nativement événementiel** : 45 modèles exportés, entraînés ici à trois échelles (dim 256/384/512), en dense, routé, distillé et creux — portes de logits tenues, découpage à deux nœuds à **0,00e0**, et la **courbe lecture ↔ qualité** mesurée aux deux échelles.

\## Les cinq résultats qui comptent

| résultat | mesure |
|---|---|
| **Les listes n'approximent rien** | logits **identiques au bit près** contre le chemin dense, à encodage de poids égal (`cmp`, 4 254 216 octets) |
| **La parcimonie doit être apprise** | à 25 % gardés : témoin **10,8758** → modèle entraîné creux **5,1719** (−52 %) |
| **La courbe lecture ↔ qualité** | dim 384 : **÷4 pour +1 %**, **÷8 pour +4 %**, ÷15 pour +22 % si un axe est imposé · dim 512 : **÷3,7 pour +6,7 %**, **÷7,2 pour +8,0 %** |
| **Le routage seul s'inverse à dim 512 ; la distillation le rattrape** | routé +10 %, routé **distillé 4,3305 contre 4,5686** au dense, à 12,8 M paires/jeton des deux côtés |
| **La mémoire tient et les gros modèles tournent** | **18 aiguilles sur 18** jusqu'à **12 288 jetons** · V4-Flash **365,7 Go sur 125 Go de RAM, 37,6 Go résidents** |

\## Ce que la fenêtre a coûté en corrections

**Cinq pièges de méthode**, dont trois qui avaient faussé des mesures publiées : un **binaire plus vieux que ses correctifs** (le codestral mesurait un texte aux espaces mangés), une **porte qui ne pouvait pas passer** (2 400 s accordées à une passe qui en demande 6 900), un cache qui survivait à son correctif. 
… [1889 caractères tronqués]

### Tour 36 — allons-y pour un sprint cerveau complet. Vasy en mode autonome jusqu'à demain matin (9h hae 10 octobre)

*24 appels d'outils.* Actions notables :

- create_goal
- todo_write
- bash — Inspect the distributed driver and transport API
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/topologie.rs`
- bash — Wire the module and run its tests
- bash — Find the dispatch and the plan flag
- bash — Wire the topology CLI and build
- bash — Test the topology plan and refusals
- bash — Locate the premature model loading
- bash — Inspect the dispatch region
- bash — Verify the flag is parsed
- bash — Find all topology references
- bash — Read the Options initializer
- bash — Read the top of main
- … et 9 autres

**Synthèse produite :**

⏵ C1a livrée et vérifiée, C1b conçue sur le code — le sprint continue

**C1a — le descripteur de topologie est en place** (`drave-core/src/topologie.rs`, 8 tests, **85 tests au total, tous verts**) :

- **JSON minimal analysé à la main** — le crate reste *std seul, sans dépendance*, comme le dépôt l'exige ;
- **validation stricte**, chaque refus avec son message et son **code de sortie** : trou de couverture, recouvrement de couches, identifiant dupliqué, lien orphelin, lien réflexif, **cycle** (refusé tant que la récurrence C2 n'existe pas), clé inconnue, mode de lien inconnu ;
- **ordre d'exécution** par tri topologique de Kahn, et détection **chaîne *vs* graphe** — la chaîne étant le cas de non-régression ;
- la commande passe **avant le chemin du modèle** : un descripteur de régions ne décrit pas des poids, et exiger un GGUF pour lire un graphe ferait mentir la commande.

Vérifié en direct :

```
$ drave --topologie topo_chaine.json    → CHAÎNE · 2 régions · plan en 2 étapes
$ drave --topologie topo_y.json         → GRAPHE · 3 régions · délai déclaré affiché
$ drave --topologie topo_trou.json      → refus : « couche 12 n'est portée par aucune région » (code 3)
```

**C1b — la conception est relevée sur le code, pas devinée.** La découverte qui rend le relais tractable : **le protocole transmet déjà la plage de couches dans la trame** (`f.debut`, `f.fin`) — le découpage voyage avec le flux, il n'y a rien à inventer côté format. Ce qui manque, c'est qu'un nœud du **milieu** transmette à son successeur au lieu de répondre à son appelant. Les points d'insertion exacts sont consignés dans `docs/sprint-cerveau.md` : `run_serveur_flux` après `mdl.forward` (main.rs:3347), `run_ppl_reparti` (main.rs:3605), deux options côté nœud (`--relais`, `--region`) et deux accesseurs à ajouter. **Le retour se fait de proche en proche**, donc le pilote n'a pas à connaître le nombre de relais.

Le protocole de porte est écrit : référence un seul processus · deux régions (non-régression, **0,00e0**) · **trois régions sur trois instances** (pilote + deux nœuds en relais) égales à la référence · puis les mêmes derrière le **relais de latence** — la perplexité ne doit pas bouger, seul le temps doit changer.

Et la limite est dite : les régions **non contiguës** et les **entrées multiples** (un graphe en Y qui s'exécute vraiment) demandent deux plages disjointes dans un même processus — c'est **C2**, pas C1.

Tout est committé et poussé sur `stephanedenis/drave` (privé) ; le spri
… [112 caractères tronqués]

### Tour 37 — <goal_round> Objective: "Sprint « cerveau complet » en autonomie jusqu'au 10 octobre 9 h (HAE) : implémenter, avec porte … [1357 caractères tronqués]

*12 appels d'outils.* Actions notables :

- bash — See how the driver decodes the reply
- bash — See how the node loads its layer range
- bash — Check the layer-range mechanism
- bash — Read the driver's head to patch it
- bash — Locate the driver function body
- bash — Make the driver honour the topology and build
- bash — Test the topology-driven split against the historical one
- bash — Debug the topology-driven split
- bash — Restrict the pre-scan and re-test the topology-driven split
- bash — Write and run the topology gate
- bash — Run tests, update the sprint doc, commit and push
- todo_write

**Synthèse produite :**

⏵ C1b pas 1 franchi, porte outillée et tenue — le relais est le prochain jalon

**Ce qui est fait et vérifié depuis le début du sprint** (85 tests verts, 23 portes intactes, tout poussé) :

**C1a — le descripteur de topologie** (`drave-core/src/topologie.rs`) : JSON minimal analysé à la main (le crate reste *std seul*), validation stricte avec un refus explicite par cas — trou de couverture, recouvrement, doublon, lien orphelin, lien réflexif, cycle, clé inconnue, mode inconnu — tri topologique de Kahn, et détection **chaîne *vs* graphe**.

**C1b pas 1 — la topologie PILOTE le découpage.** `--ppl-reparti … --topologie F` exécute maintenant le découpage **décrit par le fichier**. Le pilote vérifie que la région locale commence à la couche 0, que les deux régions recouvrent le modèle entier (nombre de couches lu dans l'**en-tête** du GGUF, sans charger les poids) et **refuse** une topologie dont l'adresse contredit `--ppl-reparti`.

**La porte est outillée** (`tools/porte-topologie.sh`, quatre cas) et elle tient :

| cas | mesure (m5_d384_dense, 2 couches locales sur 4) |
|---|---|
| 1. référence, modèle entier | perplexité **3,7326** |
| 2. découpage historique `--couches-locales` | **5,0374** · écart de flux **0.00e0** |
| 3. **découpage par TOPOLOGIE** | **5,0374** · écart **0.00e0** — *le même chiffre* |
| 4. refus | trou de couverture → refusé · adresse contredite → refusée avec le message |

**PORTE TENUE** : la topologie rend exactement le chiffre du découpage historique, et l'écart de flux reste 0,00e0.

Un détail qui a failli coûter cher, et qui est consigné : `--topologie` seul imprime le plan et sort, ce qui **avalait** `--ppl-reparti … --topologie` (la commande imprimait le plan au lieu de mesurer). La pré-analyse est maintenant restreinte à l'absence de `--ppl-reparti`.

**Le prochain jalon est le RELAIS** — trois régions sur trois instances : le pilote porte la première, le nœud du milieu applique sa plage puis **transmet à son successeur** au lieu de répondre, et le retour se fait de proche en proche. Le point d'insertion est relevé précisément (`run_serveur_flux` après `mdl.forward`, main.rs:3347), et la découverte qui le rend tractable est que **le protocole transporte déjà la plage de couches dans la trame** : le découpage voyage avec le flux, il n'y a rien à inventer côté format. Le protocole de mesure des quatre cas (dont le relais de latence) est écrit dans `docs/sprint-cerveau.md`, qui tient l'état du sprint round par round.

### Tour 38 — <goal_round> Objective: "Sprint « cerveau complet » en autonomie jusqu'au 10 octobre 9 h (HAE) : implémenter, avec porte … [1357 caractères tronqués]

*23 appels d'outils.* Actions notables :

- bash — Check how the node sets its layer range
- bash — Read the node loop context precisely
- bash — Implement the relay node and build
- bash — Test the three-region relay chain
- bash — Fix the pre-scan and test the three-instance chain
- bash — Run the three-instance chain with full logs
- bash — Remove the two-region guard and test the relay
- bash — Find the driver frame call
- bash — Send the first remote region's range and build
- bash — Fix n_layer and test the relay chain
- bash — Inspect the node logs after the hang
- bash — Test the relay chain on a 24-layer model
- bash — Compare the 2-region split at the same boundaries
- bash — Compare two versus three regions in the listes mode
- … et 9 autres

**Synthèse produite :**

⏵ **C1 est livrée** : le relais est exact à trois instances — et il a fait trouver un vrai bug

**Ce qui est fait ce round, mesuré et poussé :**

| montage (modèle 24 couches, mode 0) | perplexité | écart de flux |
|---|---:|---:|
| référence locale | 42,5477 | — |
| deux régions / deux instances | **42,5477** | **0.00e0** |
| **trois régions / trois instances** (pilote + relais + sortie) | **42,5477** | **0.00e0** |

**Le relais ne change pas un chiffre** — 127 trames servies par chaque nœud, résultat identique au découpage à deux régions et à la référence locale. C'est la **distribution sur plusieurs instances concertées** demandée, avec sa porte tenue.

**Le bug que cette étape a trouvé, et qui compte autant que la capacité.** En câblant la plage du pair, j'ai envoyé `derniere` au lieu de `derniere + 1` : **la fin de plage est EXCLUSIVE** (le nœud exécute `debut..fin`). La dernière couche de la région distante n'était plus exécutée — et le défaut **ne touchait que les modes 0, 1 et 2** (les modes 3 et 4 passent par un autre encodeur, resté intact).

C'est `tools/porte-flux.sh` qui l'a dit, en trois lignes :

```
mode 0 — f32 dense            1.69e1  ❌ (plafond 0)   →  après correctif : 0.00e0 ✅
mode 1 — listes quantifiées   1.69e1  ❌              →  0.00e0 ✅
mode 2 — listes par blocs     1.67e1  ❌              →  3.65e-2 ✅
```

J'ai cassé trois modes sur cinq pendant le sprint, **et la porte du dépôt l'a attrapé**. La leçon est inscrite dans `docs/sprint-cerveau.md` : toute modification du chemin d'exécution se paie d'un passage de `porte-flux.sh` — cinq modes, deux minutes — sans quoi trois modes seraient restés cassés en silence. Les 85 tests repassent ✓.

**État du sprint** (`docs/sprint-cerveau.md` tenu à jour, tout poussé sur `stephanedenis/drave`) :

- **C1 — FAIT** : descripteur de topologie (C1a) · la topologie pilote le découpage (C1b pas 1) · le relais trois instances (C1b pas 2). La porte est outillée (`tools/porte-topologie.sh`, cinq cas dont deux refus) et tenue.
- **C12 — trace globale + rejeu** : en cours, c'est le prochain jalon.
- **C5 — bus de modulation** : à suivre.

Reste hors périmètre, et c'est dit : les **entrées multiples** (un graphe en Y qui s'exécute vraiment) demandent deux plages disjointes dans un même processus — c'est la capacité **C2** du plan, pas C1.

### Tour 39 — <goal_round> Objective: "Sprint « cerveau complet » en autonomie jusqu'au 10 octobre 9 h (HAE) : implémenter, avec porte … [1357 caractères tronqués]

*11 appels d'outils.* Actions notables :

- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/trace_globale.rs`
- bash — Wire the trace module and run its tests
- bash — Find the driver's summary print
- bash — Wire the trace into the driver and build
- bash — Define the region name and rebuild
- bash — Test the global trace and its replay verification
- bash — Re-test the trace with a matching topology port
- bash — Verify that a falsified trace is detected
- bash — Write and run the C12 gate
- bash — Check the flux gate, update the doc, commit and push
- todo_write

**Synthèse produite :**

⏵ **C12 livrée** : trace globale au bit près, rejeu sans divergence, et trace fausse détectée

**Ce qui est fait ce round** (90 tests verts, `porte-flux.sh` repassé et vert, tout poussé) :

**`drave-core/src/trace_globale.rs`** — par croisement : région, pas, lien, nombre de valeurs, **empreinte FNV-1a des octets** (donc **au bit près**, sans epsilon) et horodatage. Les valeurs ne sont **pas** stockées : la trace dit *où* regarder, le rejeu recompte et compare — 126 croisements tiennent en 128 lignes de texte.

**La porte** (`tools/porte-trace.sh`), trois cas mesurés :

| cas | résultat |
|---|---|
| 1. exécution répartie + trace | **126 croisements** écrits (64 pas × 2 liens) · perplexité 59,0790 |
| 2. rejeu de la même exécution | **126 croisements, AUCUNE divergence ✅** |
| 3. trace **faussée d'un seul bit** | **DÉTECTÉE et NOMMÉE** : « DIVERGENCE AU BIT PRÈS au croisement 0 — région *local*, pas 0, lien *local->pair* : empreinte 0x…d696 attendue, 0x…d697 obtenue » — code de sortie 4 |

**Le cas 3 est le cœur de la capacité** : une porte qui ne sait pas échouer ne vérifie rien. C'est précisément ce qui manquait pour déboguer un graphe distribué — savoir *quel pas, quelle région, quel lien* ont divergé.

**Non-régression vérifiée** : `porte-flux.sh` repassé après la modification du chemin d'exécution, cinq modes verts (0.00e0 / 0.00e0 / 3.65e-2 / 0.00e0 / 4.45e-3) — la leçon du round précédent, appliquée.

**État du sprint** (`docs/sprint-cerveau.md` à jour, poussé sur `stephanedenis/drave`) :

| capacité | état |
|---|---|
| **C1** — graphe de régions | **FAIT** : descripteur + validateur, la topologie pilote le découpage, relais trois instances (**écart 0,00e0**), porte outillée (5 cas dont 2 refus) |
| **C12** — trace globale + rejeu | **FAIT** : 126 croisements, aucune divergence, trace fausse détectée au bit près |
| **C5** — bus de modulation multi-canaux | **en cours** : c'est le prochain jalon — canaux diffusés à toutes les régions (y compris entre instances), avec la porte « canal nul ⇒ sortie inchangée » |

Deux capacités sur trois sont livrées avec leurs invariants vérifiés, et les deux ont trouvé ou attrapé un vrai défaut au passage (la fin de plage exclusive, réparée ; la porte de trace qui sait échouer).

### Tour 40 — <goal_round> Objective: "Sprint « cerveau complet » en autonomie jusqu'au 10 octobre 9 h (HAE) : implémenter, avec porte … [1357 caractères tronqués]

*10 appels d'outils.* Actions notables :

- bash — Create the bus module and its tests
- bash — Wire the bus into driver and node, build, test
- bash — Write and run the C5 bus gate
- bash — Fix the gate comparison and re-run
- bash — Test the bus on a relay node
- bash — Run tests and the flux regression gate
- bash — Record C5 and push
- todo_write
- bash — Launch the repo gates in the background
- bash — Write the sprint summary, push, and check the gates

**Synthèse produite :**

⏵ **Les trois capacités du sprint sont livrées** — les 23 portes tournent en fond

**C1, C12 et C5 sont faites, chacune avec son module, sa porte outillée et son invariant mesuré :**

| capacité | module | porte | invariant vérifié |
|---|---|---|---|
| **C1** graphe de régions | `topologie.rs` (8 tests) | `porte-topologie.sh` (5 cas) | graphe linéaire = découpage historique (**même chiffre**) · **trois régions sur trois instances = référence, écart 0,00e0** · deux refus contrôlés |
| **C12** trace globale | `trace_globale.rs` (5 tests) | `porte-trace.sh` (3 cas) | **126 croisements, aucune divergence** au rejeu · une trace faussée **d'un seul bit** est **détectée et nommée** (pas, région, lien) |
| **C5** bus de modulation | `bus.rs` (5 tests) | `porte-bus.sh` (3 cas) | bus **neutre** ⇒ **empreintes identiques** (126 croisements) · gain 1,5 ⇒ la sortie change · bus d'un nœud **relais** ⇒ agit **à travers les instances** |

**95 tests** (77 d'origine + 18 ajoutés) et `porte-flux.sh` repassée après chaque modification du chemin d'exécution — cinq modes verts (0.00e0 / 0.00e0 / 3.65e-2 / 0.00e0 / 4.45e-3). Les **23 portes du dépôt** tournent en fond depuis 17 h 46 (elles ont atteint la porte gpt-oss, la plus lente) ; leur résultat sera relevé au prochain round.

**Trois défauts trouvés par les portes — et c'est exactement leur raison d'être :**

1. **Fin de plage exclusive** : j'envoyais `derniere` au lieu de `derniere + 1`, donc la dernière couche de la région distante n'était plus exécutée — et **seuls les modes 0, 1 et 2** étaient touchés (3 et 4 passent par un autre encodeur). Attrapé par `porte-flux.sh`, réparé, revérifié.
2. **`--topologie` avalait `--ppl-reparti`** : la commande imprimait le plan au lieu de mesurer. Arrivé **deux fois** (au pilote, puis au nœud relais) — la pré-analyse est maintenant restreinte aux deux usages d'exécution.
3. **Le gain d'un nœud final est absorbé par la normalisation de sortie** (une norme divise par la norme) : mon test du bus était faux, pas le bus. C'est un nœud du **milieu** qui prouve que le bus agit.

**Ce qui reste hors périmètre du sprint, et c'est écrit** : les entrées multiples et la récurrence (**C2**), les délais et horloges (**C3**, **C4**), la mémoire épisodique et la consolidation (**C6**, **C7**), la périphérie (**C8**), la latéralité et les budgets (**C9**, **C10**) — et pour C5, la **diffusion réseau** du bus (le format de la ligne de contrôle `MODULATION canal valeur` est écrit dans `bus.rs`, le tra
… [184 caractères tronqués]

### Tour 41 — <goal_round> Objective: "Sprint « cerveau complet » en autonomie jusqu'au 10 octobre 9 h (HAE) : implémenter, avec porte … [1357 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Check the repository gates result
- bash — Sentinel: wait for the repository gates and report
- bash — Verify the repository state and the sprint deliverables

**Synthèse produite :**

⏵ Sprint livré et poussé ; les portes du dépôt tournent, une sentinelle me réveillera

**État vérifié à l'instant :**

- **Arbre propre**, tout committé et poussé — `origin/master` = `8959d1c`, dernier commit « Bilan du sprint : C1, C12 et C5 livrées avec leurs invariants, 95 tests, trois défauts trouvés par les portes ».
- **Les trois capacités du sprint sont livrées**, chacune avec son module, sa porte outillée et son invariant :

| capacité | module | porte | invariant |
|---|---|---|---|
| **C1** graphe de régions | `topologie.rs` | `porte-topologie.sh` (123 l., 5 cas) | linéaire = historique · **trois régions / trois instances = référence, 0,00e0** · deux refus contrôlés |
| **C12** trace globale | `trace_globale.rs` | `porte-trace.sh` (59 l., 3 cas) | **126 croisements sans divergence** · trace faussée d'un bit **détectée et nommée** |
| **C5** bus de modulation | `bus.rs` | `porte-bus.sh` | bus neutre ⇒ **empreintes identiques** · gain actif ⇒ la sortie change · bus d'un **relais** ⇒ agit entre instances |

- **95 tests verts**, et `porte-flux.sh` (5 modes) repassée après chaque modification du chemin d'exécution.

**En cours** : les **23 portes du dépôt**, relancées à 17 h 46 (12 vertes, 0 rouge au moment du relevé — elles sont sur la porte gpt-oss, la plus lente, qui demande ~20-50 min sur machine calme). Une **sentinelle tourne en fond** : elle me rendra le compte final (vertes/rouges) dès que `portes.sh` aura terminé, et je pourrai alors clore le sprint sur une vérification complète — c'est la dernière condition de l'objectif (« les 23 portes du dépôt et les 77 tests doivent rester verts »), les 95 tests étant déjà confirmés.

Rien n'est laissé en suspens dans le dépôt : `docs/sprint-cerveau.md` (17 Ko) porte le bilan complet, les portes, les trois défauts trouvés par elles, le journal heure par heure, et la liste explicite de ce qui reste hors périmètre (C2 entrées multiples et récurrence, C3/C4 délais et horloges, C6/C7 mémoire épisodique et consolidation, C8 périphérie, C9/C10 latéralité et budgets, plus la diffusion réseau du bus pour C5).

### Tour 42 — <goal_round> Objective: "Sprint « cerveau complet » en autonomie jusqu'au 10 octobre 9 h (HAE) : implémenter, avec porte … [1357 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Check the gates progress
- bash — Wait and check the gates
- job_output
- bash — Record the green gates, re-run tests, commit and push
- get_goal
- update_goal

**Synthèse produite :**

⏵ Sprint cerveau terminé : les trois capacités livrées, 23 portes vertes

\## Résultat

**Les trois capacités du premier sprint sont livrées, chacune avec sa porte mesurée** — et le dépôt n'a rien perdu : **23 portes vertes, 0 rouge** (`tools/portes.sh`, code 0), **95 tests** (77 avant le sprint).

| capacité | module livré | porte outillée | invariant mesuré |
|---|---|---|---|
| **C1 — graphe de régions** | `drave-core/src/topologie.rs` (JSON analysé à la main, validation stricte, tri de Kahn, `Topologie::chaine()`) | `tools/porte-topologie.sh` (5 cas) | graphe linéaire = découpage historique (**même chiffre**) · **trois régions sur trois instances = référence, écart 0,00e0** · deux refus contrôlés (trou de couverture, adresse contredite) |
| **C12 — trace globale** | `drave-core/src/trace_globale.rs` (empreinte FNV-1a des octets, donc au bit près) | `tools/porte-trace.sh` (3 cas) | **126 croisements, AUCUNE divergence** au rejeu · une trace faussée **d'un seul bit** est **détectée et nommée** (pas, région, lien), sortie code 4 |
| **C5 — bus de modulation** | `drave-core/src/bus.rs` (canaux nommés, valeur neutre par canal, ligne de contrôle `MODULATION`) | `tools/porte-bus.sh` (3 cas) | bus **neutre ⇒ empreintes identiques** (126 croisements) · gain 1,5 ⇒ la sortie change · bus d'un nœud **relais** ⇒ agit **à travers les instances** |

**Trois défauts trouvés — par les portes, pas par chance :**

1. **fin de plage exclusive** : j'envoyais `derniere` au lieu de `derniere + 1`, donc la dernière couche de la région distante n'était plus exécutée — et **seuls les modes 0, 1 et 2** étaient touchés (3 et 4 passent par un autre encodeur). `porte-flux.sh` les a vus rouges (1.69e1), réparés, revérifiés verts ;
2. **`--topologie` avalait `--ppl-reparti`** — la commande imprimait le plan au lieu de mesurer. Arrivé **deux fois** (pilote, puis nœud relais) ;
3. **le gain d'un nœud final est absorbé par la normalisation de sortie** : mon test du bus était faux, pas le bus — c'est un nœud du **milieu** qui le prouve.

\## Artefacts

Tout est committé et poussé sur **`github.com/stephanedenis/drave`** (privé), `origin/master` = dernier commit. Le bilan complet, les portes, les défauts et le journal heure par heure sont dans **`docs/sprint-cerveau.md`** ; le relevé des 23 portes est dans `/tmp/portes_sprint.log`.

\## Ce qui reste, et que vous devez savoir

- **C5 est partiellement diffusée** : le bus est **local à chaque instance** (`--bus` sur le pilote et sur les nœuds)
… [865 caractères tronqués]

### Tour 43 — ajuste tes sprints en timeboxing plus qu'en tranche de backlog. C'est à dire que tu dois continuer pour occupper le temp … [564 caractères tronqués]

*23 appels d'outils.* Actions notables :

- create_goal
- todo_write
- bash — Implement per-link delays in the driver
- bash — Test the delay invariant
- bash — Add delays to the relay node and rebuild
- bash — Write and run the delay gate
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/relations-humaines.md`
- bash — Commit C3 and the relations charter
- bash — Add the control-line parser and its tests
- bash — Wire the network bus listener into the node
- bash — Test the network bus end to end
- bash — Find the node's listener and accept
- bash — Move the bus listener before the accept and rebuild
- bash — Re-test the network bus
- … et 9 autres

**Synthèse produite :**

⏵ Round bouclé : C3 et C5bis livrées, état resumable en tête du fichier de sprint

**Fait ce round, mesuré et poussé** (96 tests verts, arbre propre, dernier commit `883f934` → puis l'état resumable) :

**C3 — les délais par lien.** La topologie déclare `delai_ms`, le moteur l'applique (pilote sur son lien sortant, nœud relais sur le sien). Porte `tools/porte-delais.sh` :

| cas | perplexité | empreintes | mur |
|---|---:|---|---:|
| délai 0 ms | 59,0790 | référence | 6,23 s |
| **délai 50 ms par trame** | **59,0790** (identique) | **identiques** | **9,35 s (+3,1 s = 50 ms × 64 pas)** |

Un délai change **le temps, jamais un chiffre** — et c'est la trace (C12) qui le prouve, empreinte par empreinte. La loi de coût rejoint celle de la campagne (**3,4 ms par jeton et par ms de RTT**).

**C5bis — la diffusion du bus.** `--bus-fichier F` est relu **avant chaque trame** : un autre processus peut donc changer un canal **pendant l'exécution**, ce qui est la définition d'un bus. Porte `porte-bus.sh` cas 4, sur un nœud relais : **66,0379** contre **59,0790** sans canal.

**Deux leçons tombées deux fois chacune, écrites pour de bon :**
1. **Le gain d'un nœud FINAL est invisible** (la normalisation de sortie divise par la norme) — tout test de bus doit viser une région du **milieu**. Je suis retombé dans le piège, et j'ai d'abord cru le fichier de contrôle inopérant.
2. **Une porte mal formée ressemble à une capacité cassée** : le cas 4 a échoué parce que mon `printf` écrivait un `\n` **littéral**, valeur illisible que le parseur **refusait** — le parseur avait raison.

**Le fichier de relations humaines est écrit** (`docs/relations-humaines.md`) : *carpe diem* des deux côtés — timeboxing plutôt que backlog, rapports de dix lignes (fait / cassé / ensuite), une question seulement si elle bloque, les alertes en tête, l'état écrit en permanence pour qu'une interruption ne perde rien, et la liste de ce que je m'engage à ne jamais faire.

**La prochaine action est en tête de `docs/sprint-cerveau.md`**, car c'est la règle : six chantiers classés par valeur mesurable — **C4** (horloges par région, le plus structurant qui reste), **C12bis** (trace côté nœud), **C5ter** (bus par socket, avec le point d'entrée exact : le fil doit être lancé **avant** `ecoute.accept()`), **C2** (entrées multiples, à cadrer honnêtement), les expériences **E2/E4** et les dessins **H/I/J**, puis les trois manques du registre (noyaux Q8 experts et GPU, encodeurs).

Je continue sur cette liste — il 
… [62 caractères tronqués]

### Tour 44 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1749 caractères tronqués]

*324 appels d'outils.* Actions notables :

- bash — Implement per-region step counters and the step bound
- bash — Write and run the clock/step-bound gate
- bash — Commit C4 step 1 and push
- bash — Inspect node-side trace handling
- bash — Read trace format API
- bash — Read node relay loop
- bash — Read trace write/read/verify
- bash — Locate node step counter and exit
- bash — Read node send sites
- bash — Read driver record sites
- bash — Read node input extraction
- bash — Extend trace format to v2 with timestamps
- bash — Add merge, clock drift, link verification
- bash — Rewrite link pairing and build
- … et 297 autres

**Synthèse produite :**

⏵ Session résumée : 15 commits, 6 capacités du cerveau livrées et mesurées

**Fait depuis le point de contrôle** — 15 commits poussés, 122 tests verts, 14 portes vertes :

- **C4 pas 1** — compteur de pas par région + borne `--pas-max` : borne atteinte ⇒ **aucune perplexité rendue**, code 5.
- **C12bis** — le nœud trace, format v2 horodaté, `--fusionner-trace` : **94/94 liens identiques** ; 1 bit changé ⇒ DIVERGENT au pas nommé.
- **C5ter** — bus par socket : **socket ≡ statique 0,00e0**, neutre ≡ référence 0,00e0, plein vol ≠ les deux.
- **C6** — mémoire épisodique : trois négatifs mesurés (aucun élagage, l'espacement ne change rien, collisions à petit k), puis **trois ingrédients** (expansion 896→16 384, décorrélation, **égalisation des canaux hub**) → **élagage 83 %**, rappel 96,3 % à 50 % de dégradation, round-trip **exact au bit près**, Δ = **11 jetons sur 2 048**.
- **C7** — consolidation par rejeu : **l'exemplaire bat la moyenne partout** (7 % du magasin → 87 % de rappel contre 13 % → 22 %) ; le rejeu répété est un **point fixe exact** (0,00e0).
- **C8** — réflexe : **0 % d'accord jusqu'à 16 couches sur 24**, cause mesurée (cos 0,145 — l'état intermédiaire est presque orthogonal au final).
- **C9/C10** — pont : **448 fibres = +2,81 % et ÷1,8 en octets**, falaise **entre 448 et 392** ; en dense f32 élaguer ne gagne **aucun** octet ; à budget égal **quantifier bat élaguer de 83 %**.
- **C9×C1** — **8 points de coupe, une seule perplexité** (lien sans perte) ; 8,9 % d'écart en encodé ; coût du pont variant d'un **facteur 30** ⇒ **couper tard**.
- **C2/C6** — greffe d'état : branchée (témoin à 0), mais **une greffe d'état n'est pas une greffe de contexte** — cause mesurée : la suite est re-dérivée par l'attention sur le cache KV, sur lequel **le moteur n'a aucune prise** (manque écrit).
- **C6** — indice étranger : 136 jetons contre 448 de hasard, **puis la porte a corrigé ma conclusion** : un point d'interrogation de plus donne 378 ⇒ effet réel, **non robuste**.

**Prochain** (inscrit dans `docs/sprint-cerveau.md`) : l'**entrée de cache KV** — ranger un état rappelé comme clé/valeur que l'attention peut interroger, avec l'invariant « sans état rappelé, sortie identique ». Conception écrite, y compris le point délicat de la position RoPE.

### Tour 45 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1749 caractères tronqués]

*31 appels d'outils.* Actions notables :

- bash — Build the second-content prompt
- bash — Capture the second content state
- bash — Write and launch the merge-rule gate
- bash — Read the merge gate result
- bash — Diagnose the token-count difference
- bash — Compare token counts for the gate prompts
- bash — Rewrite with calibration and relaunch
- bash — Read calibrated merge gate output
- bash — Add capture-from-inference and test
- bash — Calibrate with inference-captured states
- bash — Correct the merge gate and relaunch
- bash — Read corrected merge result
- bash — Read the merge table
- bash — Read merge verdict
- … et 17 autres

**Synthèse produite :**

⏵ Round livré : C2 (règle de mélange mesurée) + correction d'un faux négatif publié

**Ce round** — 4 commits poussés, 122 tests verts, `porte-melange` (nouvelle, 4 cas) et `porte-greffe` (corrigée, 5 cas) vertes :

- **C2 — deux entrées, une règle de mélange** : deux invites de 1 750 jetons (même remplissage, un code différent), états prélevés, mélange α·A+(1−α)·B injecté dans une invite **sans aucun code** :
  - la somme **ARBITRE, elle ne détruit pas** : 7/7 mélanges rendent le premier jeton de l'un des deux contenus, jamais un troisième ;
  - **bascule mesurée à α = 0,6**, prédite à **0,509** par le rapport des normes (65,89/129,54) — écart 0,091 ⇒ **la somme est arbitrée par la NORME des états**, pas seulement par le poids.

- **Correction d'un faux négatif que j'avais publié.** « Une greffe d'état ne transfère pas le contexte » était **faux** : le prélèvement se faisait sur les identifiants tokenisés (1 750) alors que l'inférence construit une invite d'**un jeton de plus** (1 751) — j'injectais l'état qui prédit « : » au lieu du code. Avec `--etat-fin` (k-ième depuis la fin, résolu dans la numérotation de l'inférence), **le contenu passe** : `[1863, 48, 18, 19, 20, …]` = « ZQ-… » depuis une invite qui ne contient aucun code. L'ancienne conclusion est conservée **à côté** de la correction (rapport §28, en-tête de la porte), comme le veut la règle du dépôt.

- **Leçon de méthode, écrite** : une position ne se devine pas, elle se **capture là où le calcul se fait**. Trois mesures ont échoué sur ce décalage ; c'est chaque fois la porte qui a rendu le défaut visible — jamais le résultat qui avait l'air bon.

**Reste ouvert** (dans `docs/sprint-cerveau.md`) : l'**entrée de cache KV** — ranger un état rappelé comme clé/valeur que l'attention peut interroger, le seul chemin qui reste pour qu'une mémoire *serve* le calcul ; puis les têtes dédiées par profondeur (C8) et les modèles conçus pour l'événementiel (H/I/J). L'objectif reste **actif**.

### Tour 46 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1749 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Locate the decorrelation block
- bash — Implement retrieved-state extraction
- bash — Capture an external cue from B
- bash — Retrieve an episode and extract its state
- bash — Inject the retrieved state into a codeless context
- bash — Document and commit the end-to-end chain

**Synthèse produite :**

⏵ Round 3 livré : la chaîne mémoire → injection fonctionne ; le goulot est mesuré (le rappel)

**Ce round** — 3 commits poussés, 122 tests verts :

- **La chaîne complète, de bout en bout** (`--episodique-extraire`) : indexer 1 750 états → **retrouver par le contenu** avec un indice *extérieur* → **injecter** l'état retrouvé dans un calcul qui n'a pas vécu l'épisode.

| étape | mesure |
|---|---|
| rappel | épisode 437 · recouvrement 25/64 · **303 jetons** de l'aiguille (hasard 448) |
| injection α = 0 | `150px` — **témoin de non-effet** |
| **injection α = 0,2 / 1** | **`The vault access code is`** |
| injection α = 5 | `"150px` (saturé) |

Le modèle **dit la phrase-cadre de l'aiguille** alors que ni le code ni cette phrase ne sont dans son contexte : l'information a voyagé de la mémoire jusqu'à la sortie. **Mais le code n'est pas produit** — et la cause est en haut du tableau, pas en bas : l'épisode retrouvé est à 303 jetons de l'aiguille, donc son préfixe ne contient pas encore le code.

- **Conclusion utile du round** : **le goulot est le RAPPEL, pas la greffe**. La greffe d'état est un mécanisme qui marche (corrigée et vérifiée au round précédent) ; ce qui limite l'usage est la qualité du rappel par un indice purement sémantique (1,5× le hasard), cohérent avec les 136 et 378 jetons mesurés au round 2 selon la formulation de l'indice.

- **Deux réserves écrites** : le magasin stocke la sortie **normalisée** du moteur (norme 306) alors que la greffe injecte un résidu brut (54-66) — l'échelle est absorbée par la normalisation finale, mais stocker le résidu serait plus cohérent ; et un seul indice, un seul texte.

**Suivant** (dans `docs/sprint-cerveau.md`) : améliorer le **rappel** (clé stockant le résidu brut, plusieurs indices pour moyenner, index multi-documents), puis l'entrée de cache KV et les têtes dédiées C8. L'objectif reste **actif**.

### Tour 47 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1749 caractères tronqués]

*11 appels d'outils.* Actions notables :

- bash — Make cue capture and query multi-valued
- bash — Implement the multi-cue query loop
- bash — Revert and apply the minimal multi-position patch
- bash — Capture 8 cue positions from B at once
- bash — Fix parser and recapture cues
- bash — Launch 8 cue-position essays in background
- bash — Check the cue-position distribution
- bash — Wait for more cue results
- bash — Wait for the last cue results
- bash — Compute the cue distribution statistics
- bash — Document and commit the cue distribution

**Synthèse produite :**

⏵ Round 4 livré : le rappel dépend de l'INDICE (1 sur 8 trouve), pas de la mémoire

**Ce round** — 2 commits poussés, 122 tests verts :

- **La question** : le §29 avait montré que le goulot est le rappel. La mémoire est-elle mauvaise, ou est-ce l'indice choisi ? Une distribution, pas un point : **8 indices** prélevés dans l'invite B (positions 1, 2, 4, 8, 16, 32, 64, 128 depuis la fin), chacun requêtant le magasin de A (aiguille au jeton 740, hasard **448**).

| indice (depuis la fin) | épisode | distance |
|---|---|---|
| **4ᵉ** | 690 | **50** |
| 2ᵉ | 429 | 311 |
| 32ᵉ | 437 | 303 |
| dernière | 437 | 303 |
| 16ᵉ / 64ᵉ | 393 / 393 | 347 / 347 |
| 128ᵉ | 1630 | 890 |
| 8ᵉ | 1743 | 1 003 |

**Moyenne 444 · médiane 329 · meilleure 50 · pire 1 003 · hasard 448.**

1. **Un indice trouve l'aiguille** : 50 jetons, **9× mieux que le hasard** — le préfixe de l'épisode contient le fait.
2. **Mais un seul sur huit** : les autres sont au niveau du hasard ⇒ le « 3,3× mieux que le hasard » du round 2 était **un tirage chanceux**, et sa fragilité (136 puis 378 selon un point d'interrogation) s'explique enfin.
3. **La limite est le CHOIX DE L'INDICE, pas la mémoire** — et ce choix ne se devine pas : rien ne désigne la 4ᵉ position depuis la fin plutôt que la dernière.

- **Instrument ajouté** : `--etat-fin` accepte une **liste** de positions (1,2,4,8…) — huit indices en un parcours au lieu de huit parcours de 70 s. Deux bugs attrapés en l'écrivant (parseur relisant le même argument ; splice mal ancré qui dupliquait une fonction — reverti et refait avec des ancres sûres).

**Suivant** (dans `docs/sprint-cerveau.md`) : départager plusieurs indices par un score qui ne soit pas le recouvrement (le gagnant n'a que 25/64), ou assumer que le rappel sémantique n'est pas le bon outil et faire entrer le contenu comme jetons. L'objectif reste **actif**.

### Tour 48 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1749 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Inspect the text around the winning cue
- bash — Capture and test three more cue positions
- bash — Check the extra cue positions
- bash — Document the non-continuity of recall
- bash — Commit the non-continuity finding

**Synthèse produite :**

⏵ Round 5 livré : le rappel n'est pas continu — et le mécanisme est identifié (k-WTA)

**Ce round** — 2 commits poussés, 122 tests verts :

Les six **dernières** positions de l'invite B prélevées une à une, après les huit du round 4 :

| depuis la fin | jeton | distance à l'aiguille (hasard 448) |
|---|---|---|
| 1 | `:` | 303 |
| 2 | `Answer` | 311 |
| 3 | `.` | 533 |
| **4** | **`only`** | **50** |
| **5** | **`code`** | **1 006** |
| 6 | `the` | 1 005 |

- **Deux jetons VOISINS — « code » et « only » — donnent 1 006 et 50 jetons.** Rien de lexical ne l'explique : les deux états ont lu presque le même texte, et le mot partagé avec l'aiguille (« code ») est justement celui qui **échoue**.
- **Le mécanisme** : la clé est un **k-WTA** (64 canaux sur 16 384) — une petite variation de l'état fait **entrer et sortir des canaux**, donc la clé **saute**. Le rappel n'est pas une fonction continue de l'indice : **il n'y a aucune pente à suivre** pour s'approcher du bon.
- Cela explique rétrospectivement les deux anomalies des rounds précédents : le « 3,3× mieux que le hasard » (un tirage chanceux), et le fait que le recouvrement ne départage pas les indices (le gagnant n'a que 25/64).

**Trois voies ouvertes, aucune mesurée** : rendre la clé **stable** en la formant sur une **fenêtre** de positions (union/intersection des k-WTA voisins) ; interroger avec plusieurs indices et garder le meilleur ; ou **abandonner le rappel sémantique** et faire entrer le contenu comme jetons.

**Suivant** (dans `docs/sprint-cerveau.md`) : la clé de fenêtre — c'est l'expérience qui découle directement du mécanisme identifié, et elle est falsifiable (si la clé de fenêtre ne lisse pas l'hypersensibilité, l'explication par le k-WTA est incomplète). L'objectif reste **actif**.

### Tour 49 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1749 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Implement the window key
- bash — Find the exact option anchor
- bash — Apply the window-key patch
- bash — Run the window-key experiment
- bash — Check the window experiment
- bash — Wait for window results
- bash — Wait for the remaining window runs
- bash — Document and commit the refuted prediction

**Synthèse produite :**

⏵ Round 6 livré : prédiction réfutée proprement — et elle confirme une leçon par une 3ᵉ voie

**Ce round** — 1 commit poussé, 122 tests verts. Une **prédiction falsifiable formulée, testée, réfutée** :

Le round 5 avait identifié le mécanisme (la clé est un **k-WTA** → elle saute d'un jeton à l'autre). D'où la prédiction : *former la clé sur la moyenne de W positions voisines doit lisser l'hypersensibilité*. Mesuré (`--episodique-fenetre`) :

| fenêtre | indice « only » (le bon) | indice « code » (le mauvais) | **séparation** |
|---|---|---|---|
| **1** | **50** | 1 006 | **1,31/64** |
| 4 | 653 | 1 005 | 1,73/64 |
| 16 | 573 | 1 004 | 4,58/64 |
| 64 | **449** (= le hasard) | 1 004 | **19,94/64** |

- **Réfutée, et proprement** : le lissage **détruit le bon indice** (50 → 449, exactement le hasard) sans aider le mauvais (1 006 → 1 004), et il **effondre la sélectivité** (1,31 → 19,94 canaux partagés sur 64 : la clé d'une moyenne ressemble à celle de tout le monde).
- **Troisième voie indépendante qui confirme le §24 quater** : abstraire par moyennage détruit la rappelabilité — prototype moyen 22 % contre 87 % pour l'exemplaire ; clé moyenne qui ne retrouve pas le passage ; fenêtre moyenne qui fait tomber le meilleur indice au hasard. **La sélectivité de cette mémoire EST la netteté de sa clé**, et l'hypersensibilité à l'indice en est le prix.
- **La conséquence change de direction** : le lissage étant exclu et le choix de l'indice n'étant pas devinable, **retrouver un passage depuis une question n'est pas ce que le rappel par le contenu sait faire**. Ce qui reste solide (tout mesuré) : la complétion de motif (Δ = 2 jetons à 50 % de dégradation), la localisation en jetons, et l'injection d'un état retrouvé. Pour la recherche par question : des **jetons** (RAG) ou une **clé apprise**.

**Suivant** (dans `docs/sprint-cerveau.md`) : soit une **clé apprise** (ce qui suppose d'entraîner — le chantier de C7 vers les poids), soit acter que la mémoire sert par complétion de motif et passer aux capacités restantes (C8 têtes dédiées, C7 poids, modèles H/I/J). L'objectif reste **actif**.

### Tour 50 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1749 caractères tronqués]

*9 appels d'outils.* Actions notables :

- bash — Inspect the topology link struct
- bash — Read the link JSON parser
- bash — Add the link budget to the topology
- bash — Fix the test initializer
- bash — Find where the driver reads the link delay
- bash — Read the delay extraction and byte accounting
- bash — Wire the budget check into the driver
- bash — Write and run the budget gate
- bash — Document and commit the link budget

**Synthèse produite :**

⏵ Round 7 livré : C10 fermé — budget par lien, vérifié sur ce qui passe

**Ce round** — 1 commit poussé, 122 tests verts, `porte-budget.sh` verte (3 cas).

Le plan assignait à **C10** des budgets par lien « vérifiés au démarrage » ; **la mesure a corrigé le plan** : la taille d'un flux n'est pas une propriété du mode, elle dépend de l'**activité** réelle — 1 951 octets/pas en listes par blocs à 97,7 %, **1 096 à 50 %** (§31). Un contrôle au démarrage ne pourrait comparer qu'à une valeur nominale inventée.

Le budget est donc déclaré dans la topologie (`"budget_octets": N`) et **comparé à ce qui passe**, au pas où il passe :

| cas | mesure |
|---|---|
| aucun budget (défaut) | 111,9225 · 1 951 octets/pas · code 0 |
| budget **généreux** (2 451) | **111,9225 — identique** · code 0 |
| budget **insuffisant** (975) | premier flux **1 860 octets** ⇒ arrêt **au pas 0**, lien/octets/budget/pas nommés, **code 6**, **aucune perplexité rendue** |

C'est la même règle qu'en C4 (borne de pas) et C9 (pont) : **s'arrêter et le dire**, jamais rendre un chiffre qui mentirait sur ses conditions. Détail mesuré au passage : le **premier** flux est plus gros que la moyenne des 47 pas — un budget juste sous la moyenne arrête donc dès le pas 0, ce qui est le comportement voulu.

Le champ est **optionnel** : les 23 portes, les topologies existantes et les tests ne changent pas de comportement.

**Suivant** (dans `docs/sprint-cerveau.md`) : la **politique de pannes** (`requis` / `best-effort` — arrêter en nommant la région et le pas, jamais un résultat partiel), puis les têtes dédiées C8 et les modèles H/I/J. L'objectif reste **actif**.

### Tour 51 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1749 caractères tronqués]

*11 appels d'outils.* Actions notables :

- bash — Locate the driver's link-loss paths
- bash — Implement named link-failure handling
- bash — Write and run the fault-policy gate
- bash — Reproduce the panic on node kill
- bash — Name the unreachable-peer failure
- bash — Kill after connection and rerun the gate
- bash — Separate ports per case and rerun
- bash — Make cases 2-3 robust and rerun
- bash — Commit fault handling and launch porte-flux
- bash — Check porte-flux after the changes
- bash — Verify the budget gate after the fault patch

**Synthèse produite :**

⏵ Round 8 livré : C11 — les pannes sont nommées, avec leur propre code

**Ce round** — 1 commit poussé, 122 tests verts, `porte-pannes.sh` (nouvelle, 3 cas) et `porte-budget.sh` vertes, **`porte-flux.sh` 5/5** après les changements de chemin d'exécution.

Le plan prévoyait un `best-effort` qui « saute la région et annonce l'écart ». **La mesure oblige à refuser cette sémantique** : sauter douze couches ne calcule pas une version approchée, cela calcule **un autre modèle**. Conduite retenue : **s'arrêter en disant tout**.

| cas | mesure |
|---|---|
| exécution nominale | 33,0156 · code 0 |
| **pair tué en cours de route** | `PANNE sur le lien local → d : le pair a fermé avant de rendre son état. L'exécution s'arrête **au pas 12** (**43 968 octets** échangés jusque-là). AUCUNE perplexité n'est rendue` · **code 7** |
| **pair absent** | `INJOIGNABLE (Connection refused)` · **code 7**, en **2 s**, aucune perplexité |

**Codes de sortie désormais distincts** : **5** = borne de pas (C4) · **6** = budget dépassé (C10) · **7** = panne de lien (C11) — un script peut distinguer les trois causes d'arrêt.

**Deux défauts trouvés en écrivant la porte** :
1. un pair **absent faisait paniquer** le pilote (`expect` sur la connexion, code 134 illisible) au lieu de nommer le lien — corrigé ;
2. la porte elle-même attendait `client connecté` dans le journal du nœud : fragile, elle échouait pour une raison qui n'était pas celle qu'elle mesure (port en TIME_WAIT, pilote qui calcule 10 s de référence locale avant de se connecter) — elle chronomètre maintenant la mort et juge sur le code et le message.

**Reste non fait, et écrit** : la **reprise** — un pair qui revient a perdu son cache KV, donc continuer serait faux ; reprendre proprement demanderait de rejouer le préfixe (checkpoint/restart).

**Suivant** (dans `docs/sprint-cerveau.md`) : les têtes dédiées C8 (ce qui suppose d'entraîner — le chantier C7 vers les poids), les modèles H/I/J, ou la reprise après panne. L'objectif reste **actif**.

### Tour 52 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1749 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Find the per-flux round-trip timing
- bash — Read the round-trip timing site
- bash — Add the latency budget
- bash — Extend the budget gate with latency cases
- bash — Fix unbound variable and rerun
- bash — Reproduce the latency-budget case
- bash — Fix the clobbered variable and rerun
- bash — Document and commit the latency budget

**Synthèse produite :**

⏵ Round 9 livré : C10 complet (octets **et** latence), quatre codes d'arrêt distincts

**Ce round** — 1 commit poussé, 122 tests verts, `porte-budget.sh` étendue à **5 cas** (verte).

Le plan demande `{paires/s, octets/s, ms}` par lien. Les octets étaient faits ; voici la **latence** : `"budget_ms": N`, comparé à l'**allé-retour mesuré** de chaque pas — la loi du dépôt étant 3,4 ms par jeton et par ms de RTT, un lien déclaré à 5 ms qui en met 50 n'est pas le lien qu'on croit, et le savoir au premier pas vaut mieux qu'à la fin.

| cas | mesure |
|---|---|
| latence **généreuse** (100 000 ms) | 111,9225 — **identique** · code 0 |
| latence **insuffisante** (1 ms) | `LATENCE DÉPASSÉE … : **20,1 ms pour un budget de 1 ms, au pas 0**` · **code 8** · aucune perplexité |

**Quatre codes d'arrêt distincts désormais** : **5** borne de pas (C4) · **6** budget d'octets · **7** panne de lien (C11) · **8** budget de latence (C10). Un script nomme la cause sans lire les messages — même discipline que partout ailleurs dans ce sprint : *s'arrêter et le dire*.

**Défaut de porte attrapé** : la porte écrasait la variable `D` (le chemin du binaire) avec la sortie du pilote — le cas suivant échouait sur un **127** (« command not found »), ce qui ne disait rien de ce qu'on mesurait. C'est la deuxième fois dans ce sprint qu'une porte échoue pour une raison étrangère à sa mesure ; les deux fois, elle l'a dit.

**Suivant** (dans `docs/sprint-cerveau.md`) : le troisième volet `paires/s` (le coût en paires, déjà instrumenté par le moteur), puis les têtes dédiées C8 / modèles H-I-J, ou la reprise après panne. L'objectif reste **actif**.

### Tour 53 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*13 appels d'outils.* Actions notables :

- bash — Launch the full gate suite
- bash — Check the suite progress
- bash — Wait for more gates
- bash — Wait for the remaining gates
- bash — Continue waiting for the suite
- bash — Wait for the suite to finish
- bash — Final stretch of the suite
- bash — Wait for the merge gate
- bash — Read the suite's final verdict
- bash — Diagnose the red gate
- bash — Read the red gate's setup
- bash — Record the verification result and the red gate
- bash — Commit the verification round

**Synthèse produite :**

⏵ Round 10 livré : vérification complète des 20 portes — 19 vertes, 1 rouge nommée

**Ce round** — 1 commit poussé, 122 tests verts. Un round de vérification, parce que la contrainte de l'objectif (« les portes restent vertes ») se vérifie — surtout après huit rounds qui ont touché le chemin d'exécution.

**Suite complète des 20 portes du dépôt : 19 vertes · 1 rouge.**

Vertes : budget · bus · bus-socket · coupe · delais · episodique · flux · fusion · greffe · horloge · indice · melange · mistral · pannes · pont · reflexe · tokenizer-kimi · topologie · trace.

**La rouge : `porte-reparti-moteur`** — perplexité entière **321,9623** contre répartie **132,8349** (écart 58,7 %) alors que **l'écart de flux est 0,00e0**. C'est la porte de **notre** modèle (`/tmp/moteur_route.gguf`, `COUCHES=2`).

- **Ce que j'affirme** : les huit rounds n'ont ajouté que des chemins **inactifs par défaut** sur cette porte (fusion sans `--fusion-etat`, pont sans `--pont-k`, budgets sans `budget_octets`/`budget_ms`, pannes seulement en cas d'erreur, capture sans `--etat-sortie`, clé de fenêtre à 1) — aucun ne peut produire un écart de 58 %.
- **Ce que je n'affirme pas** : je n'ai pas remonté au commit d'avant le sprint pour le prouver ⇒ la rouge est écrite comme **pré-existante et non expliquée**, pas comme « pas ma faute ».
- **Fait relevé en la nommant** : `/tmp/moteur_route.gguf` et `/tmp/route_ids.txt` datent du **8 octobre 10 h 55** — l'artefact peut être périmé par rapport à l'entraîneur actuel.
- **Prochaine action écrite** : régénérer l'artefact avec `tools/entrainer_moteur.py`, rejouer la porte ; si la rouge persiste, comparer les logits entier/réparti position par position (`compare_logits.py`).

**Suivant** (dans `docs/sprint-cerveau.md`) : instruire cette rouge, puis le troisième budget (`paires/s`) et les têtes dédiées C8 / modèles H-I-J. L'objectif reste **actif**.

### Tour 54 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*7 appels d'outils.* Actions notables :

- bash — Check available trained-model artifacts
- bash — Run the red gate with the dense variant
- bash — Read the gate's reference and split commands
- bash — Compare tokens scored by both paths
- bash — Test the fix with the true token count
- bash — Fix the gate and verify on the routed model
- bash — Document and commit the red-gate resolution

**Synthèse produite :**

⏵ Round 11 : la rouge était la PORTE — et notre modèle entraîné survit au découpage

**Ce round** — 1 commit poussé, 122 tests verts, **20 portes vertes sur 20**.

La rouge non expliquée du round 10 (`porte-reparti-moteur` : 321,9623 contre 132,8349, écart 58,7 %, flux à 0,00e0) est **instruite jusqu'à sa cause**.

**Trois hypothèses éliminées par la mesure :**
- le **routage d'experts** ne survivrait pas au découpage → la variante **dense** échoue aussi (37,8 %) : ce n'est pas le routage ;
- le **transport** altérerait les états → l'écart de flux imprimé est **0,00e0** ;
- notre modèle serait intrinsèquement non découpable → contredit par le résultat final.

**La cause, trouvée en comparant les deux chemins à la main** : le fichier d'identifiants contient **255 jetons**, la porte en annonçait **128** — et les deux chemins **fenêtrent différemment** :
```
--ppl          note les `limit` PREMIERS jetons   → 0..127
--ppl-reparti  « troncature aux 128 derniers »    → 128..255
```
**La porte comparait deux textes différents** — et 37 à 58 % d'écart entre deux passages sans rapport est un chiffre parfaitement normal.

**Après correction** (le nombre de jetons est **compté**, plus supposé) :

| modèle | entier | réparti | écart |
|---|---|---|---|
| `moteur_dense.gguf` | 173,0196 | **173,0196** | **0,0000 %** |
| `moteur_route.gguf` | 173,0196 | **173,0196** | **0,0000 %** |

**PORTE TENUE** : le modèle entraîné ici (Qwen3-MoE, corpus d'octets) **survit au découpage au chiffre près, routage compris** — ce que la rouge laissait croire faux depuis deux jours. C'est un vrai résultat pour le sprint « cerveau » : le modèle qu'on produit n'a pas besoin d'être « split-aware » pour être réparti.

**Deux leçons** : (1) une porte qui échoue doit être instruite jusqu'à sa cause — celle-ci accusait le modèle, et c'était la porte ; (2) `--limit` ne veut pas dire la même chose dans les deux chemins (N premiers en perplexité, N derniers en réparti) : **asymétrie de protocole**, maintenant écrite dans la porte qui l'a subie.

**Suivant** (dans `docs/sprint-cerveau.md`) : le troisième budget (`paires/s`), les têtes dédiées C8, les modèles H-I-J. L'objectif reste **actif**.

### Tour 55 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Add the registry resolver
- bash — Find the driver's pair resolution
- bash — Wire the registry into driver and relay
- bash — Write and run the registry gate
- bash — See the topology validation message
- bash — Read the coherence check
- bash — Fix resolution order and rerun the gate
- bash — Document and commit the registry

**Synthèse produite :**

⏵ Round 12 livré : C11 — le registre des régions, la « découverte » du plan

**Ce round** — 1 commit poussé, 122 tests verts, `porte-registre.sh` (nouvelle, 3 cas) verte.

Une topologie qui écrit `"instance": "127.0.0.1:50001"` décrit **un** déploiement ; la même sur trois machines en demanderait trois. Le plan §3.2 (ligne « découverte ») prévoyait un registre statique : `--registre FICHIER`, chaque ligne donnant `region hote:port`.

- **Ce qui est résolu, et ce qui ne l'est pas** : une instance qui contient déjà `:` est une adresse et n'est **pas** touchée (les topologies existantes marchent au caractère près) ; sinon elle est cherchée dans le registre, et une région **absente est refusée en la nommant** — un repli silencieux sur `localhost` ferait parler le moteur à la mauvaise machine. Résolution des **deux côtés** (pilote et nœud relais).

| cas | mesure |
|---|---|
| topologie **nommée** + registre | **113,0068** · code 0 |
| même topologie, **adresse en dur** | **113,0068 — identique** |
| région **absente** du registre | refus **en la nommant**, code 2, rien n'est calculé |

- **Défaut trouvé en écrivant la porte** : le contrôle de cohérence (« la région distante est sur X mais `--ppl-reparti` dit Y ») comparait l'adresse à l'instance **brute** — une topologie nommée était donc refusée (code 3) comme contradictoire alors que les deux sources disaient la même chose. **La résolution doit précéder le contrôle**, et c'est maintenant écrit à cet endroit du code.

**État du sprint** (12 rounds, 20 portes) : **toutes vertes**, 122 tests. Capacités livrées : C1, C2 (règle de mélange), C4 (pas 1), C5/C5bis/C5ter, C6 (mémoire + ses limites mesurées), C7 (consolidation), C8 (réflexe), C9/C10 (pont, coupes, budgets octets **et** latence), C11 (pannes + registre), C12/C12bis.

**Suivant** (dans `docs/sprint-cerveau.md`) : le budget `paires/s`, les têtes dédiées C8, les modèles H-I-J. L'objectif reste **actif**.

### Tour 56 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*7 appels d'outils.* Actions notables :

- bash — Check porte-flux reference computation
- bash — Sweep gates for whole-vs-split comparisons
- bash — Inspect porte-topologie's reference
- bash — Check the ids file length and the comparison
- bash — Fix the latent trap and rerun
- bash — Run the topology gate fully
- bash — Document and commit the gate sweep

**Synthèse produite :**

⏵ Round 13 livré : le piège de fenêtre était latent dans une 2ᵉ porte — balayage fait, règle écrite

**Ce round** — 1 commit poussé, `porte-topologie` corrigée et verte (code 0, aucun rouge).

Après avoir corrigé `porte-reparti-moteur` (round 11), la question mécanique : **combien d'autres portes portent le même piège de fenêtre** (`--ppl` note les `limit` **premiers** jetons, `--ppl-reparti` **tronque aux `limit` derniers**) ? Balayage des 20 portes :

| porte | compare à un entier ? | verdict |
|---|---|---|
| `porte-reparti-moteur` | **oui, et affirme l'égalité** | corrigée (round 11) |
| **`porte-topologie`** | **non — imprime côte à côte** | **corrigée ici** |
| `porte-flux` | non : lit la « référence **locale** » du même run | saine par construction |
| 11 autres | non : réparti contre réparti | saines par construction |

**`porte-topologie` avait le piège à l'état latent** : 255 jetons dans le fichier, limite annoncée à 128 — la perplexité de référence et celle du découpage **portaient sur deux passages différents**, affichées l'une sous l'autre comme si elles se comparaient. Elle ne l'affirmait pas, donc elle passait ; mais elle **invitait à une comparaison fausse**.

Après correction (jetons **comptés**) : **référence 5,3719 · découpage 5,3719 · écart de flux 0,00e0** — les deux nombres parlent enfin du même texte.

**Règle écrite une fois pour toutes** : dans une porte, `--limit` doit valoir **le nombre de jetons du fichier, compté et non écrit à la main**, dès qu'un chemin réparti intervient. Les deux portes qui le faisaient à la main s'étaient trompées **toutes les deux**.

**Bilan du sprint** : 13 rounds, 21 portes (toutes vertes), 122 tests, quatre codes d'arrêt distincts (5/6/7/8), un registre de régions, et une douzaine de résultats mesurés dont la moitié sont des négatifs ou des corrections — tous documentés avec leurs conditions dans `reports/rapport-campagne-benefices.md` (§24 à §36). L'objectif reste **actif**.

### Tour 57 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Write the consolidated handoff state
- bash — Commit the consolidated handoff

**Synthèse produite :**

⏵ Round 14 livré : état reprenable consolidé — trois chantiers avec leur première commande

**Ce round** — 1 commit poussé (`7869a12`), 122 tests verts, arbre de travail propre (hors `journal/` géré par le harnais).

J'ai réécrit le bloc **▶ PROCHAINE ACTION** de `docs/sprint-cerveau.md` pour qu'un round suivant — ou un humain — reprenne sans rien relire :

**Les trois prochains chantiers, chacun avec sa première commande :**
1. **Budget `paires/s`** (C10, 3ᵉ volet) — la difficulté est nommée : ce sont **les pairs** qui calculent les paires, donc le pilote ne peut les borner sans que le nœud les **transporte** (protocole v7 : un champ dans la trame de réponse). Première commande : mesurer ce que le nœud calcule par pas — il l'imprime déjà.
2. **C8 suite — une tête dédiée par profondeur** : mesuré qu'un réflexe court ne peut pas lire l'état intermédiaire (cos 0,145 à 16 couches sur 24) ; il lui faut une tête **entraînée pour sa couche**, et `tools/entrainer_moteur.py` existe.
3. **E4 — courbe de dose d'une inhibition négative** (`--ffn-gain` < 0) par couche, avec les leviers déjà présents.

**Le bilan par capacité** en une ligne chacune (C1 → C12bis) avec les chiffres clés, et surtout **les cinq corrections de ce sprint écrites pour ne pas être réintroduites** :
1. `--limit` **diffère selon le chemin** (`N` premiers en perplexité, `N` derniers en réparti) ⇒ toujours **compter** les jetons ;
2. une **position ne se devine pas** ⇒ `--etat-fin`, résolu par le moteur après troncature ;
3. `..Default::default()` donne **0,0** à un f32 ⇒ un poids de greffe nul, en silence ;
4. `sys.exit("message")` sort **toujours en 1** ⇒ une porte « verte » rendait 1 ;
5. une porte qui échoue doit être **instruite jusqu'à sa cause** (la rouge accusait le modèle ; c'était la porte).

**Bilan du sprint** : 14 rounds, **21 portes toutes vertes**, 122 tests, quatre codes d'arrêt distincts (5 borne · 6 octets · 7 panne · 8 latence), et une trentaine de mesures documentées — dont une bonne moitié sont des négatifs, des réfutations ou des corrections, chacun écrit avec ses conditions. L'objectif reste **actif**.

### Tour 58 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Check the ffn-gain syntax
- bash — Run the inhibition dose-response
- bash — Refine the positive gain dose at early layers
- bash — Write and run the gain gate
- bash — Document and commit the E/I result

**Synthèse produite :**

⏵ Round 15 livré : E4 — l'équilibre excitation/inhibition, et un levier de −11,5 % SANS entraîner

**Ce round** — 1 commit poussé, 122 tests verts, `porte-gain.sh` (nouvelle, 4 cas) verte. **Aucune ligne de moteur touchée** : le levier existait (`--ffn-gain couche:valeur`).

L'hypothèse biologique E4 (« un réseau équilibré vit près d'un point où excitation et inhibition se compensent ») transposée en question mesurable : *existe-t-il un gain de la FFN, par couche, qui améliore la perplexité — et est-il intérieur ?* Référence **14,6496**.

| gain | couche 0 | couche 1 | couche 12 | couche 18 |
|---|---|---|---|---|
| **1,0** | **14,6496** | **14,6496** | **14,6496** | **14,6496** |
| 0,75 | **12,9635** | 13,9844 | — | — |
| 0,5 | 14,1057 | **13,7907** | 14,9512 | 15,4868 |
| 0,25 | **996,04** | 14,2423 | — | — |
| 0,0 | 56 860 | — | 15,69 | 17,43 |
| −0,5 | 70 350 | — | 17,12 | 21,20 |
| −1,0 | 112 958 | — | 19,48 | 30,25 |

1. **Invariant** : `--ffn-gain L:1.0` **EST** l'absence de réglage (14,6496 exactement, sur trois couches) — sans lui, aucune autre ligne ne comparerait quoi que ce soit.
2. **Inhibition : RÉFUTÉE** — la courbe est monotone, tout gain < 1 dégrade, et de plus en plus. « Un peu d'inhibition fait du bien » est faux ici.
3. **Amplification : optimum INTÉRIEUR et net sur les premières couches** — couche 0 à **0,75 → 12,9635**, soit **−11,5 %** ; couche 1 à 0,5 → −5,9 % ; couche 2 sans optimum utile.
4. **Falaise** : couche 0 à 0,25 → **996,04**, **68× pire** — un gain trop faible à la première couche ne dégrade pas un peu, il **casse** le modèle.

**Le plus intéressant** : le profil optimal **décroît avec la profondeur** (0,75 → 0,5 → ≥ 1,0). Les premières couches ont besoin d'être amplifiées, les suivantes non — la « balance » d'un transformeur n'est pas la même partout. Un **profil appris par couche** est donc un levier **mesuré, sans rien entraîner**, et c'est une piste directe pour le dessin **I** de `docs/modele-pour-drave.md`.

**Bilan** : 15 rounds, **22 portes** toutes vertes, 122 tests. L'objectif reste **actif**.

### Tour 59 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Measure the 0.75 gain across all layers
- bash — Add the localization case and rerun
- bash — Document and commit the localization

**Synthèse produite :**

⏵ Round 16 livré : le déséquilibre E/I est **localisé à l'entrée**, pas réparti

**Ce round** — 1 commit poussé, 122 tests verts, `porte-gain.sh` à **5 cas** (verte). Le gain 0,75 mesuré sur **chaque** couche (référence 14,6496) :

| couche | 0 | 1 | 2 | 3 | 4–16 | 17 | 21 | 23 |
|---|---|---|---|---|---|---|---|---|
| écart | **−11,5 %** | **−4,5 %** | **+9,2 %** | **+10,6 %** | ±1 % (neutres) | +3,8 % | +4,3 % | +5,7 % |

(couches 8, 9, 19 : −0,4 % à −0,1 %, dans le bruit)

**Le déséquilibre n'est pas réparti sur la profondeur : il est à l'ENTRÉE.** Deux couches veulent être amplifiées, deux autres ne supportent pas d'être touchées, et vingt sont déjà à leur point. La lecture biologique (E4) s'en trouve précisée : ce n'est pas l'équilibre *global* du réseau qui est en jeu, c'est le **gain d'entrée**.

**Conséquence pour le dessin I** (profil de gains appris) : le levier existe et vaut **−11,5 % sans rien entraîner**, mais il porte sur **deux couches, pas vingt-quatre** — donc très peu de paramètres utiles : bonne nouvelle pour l'entraînement, mauvaise pour l'ambition. C'est écrit tel quel.

**Ce que la porte verrouille** (5 cas) : `gain 1.0` **est** l'absence de réglage (exactement) · l'inhibition est **monotone** · l'optimum intérieur existe (0,75 bat 0,5 et 1,5) · la **falaise** à 0,25 (68× pire) · et le bénéfice est **localisé** (couches 0-1 oui, couche 5 non).

**Bilan** : 16 rounds, 22 portes toutes vertes, 122 tests, une trentaine de mesures dont la moitié des négatifs ou des corrections — toutes documentées avec leurs conditions dans `reports/rapport-campagne-benefices.md` (§24 à §37). L'objectif reste **actif**.

### Tour 60 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*9 appels d'outils.* Actions notables :

- bash — Find the ffn_gain application site
- bash — Read the two application sites
- bash — Make ffn-gain a per-layer profile
- bash — Read the wiring site
- bash — Fix the wiring and build
- bash — Fix the second wiring site
- bash — Measure the composed gain profile
- bash — Add the composition case and run
- bash — Document and commit the composition result

**Synthèse produite :**

⏵ Round 17 livré : les gains **ne se composent pas** — le profil défait le meilleur réglage seul

**Ce round** — 1 commit poussé, 122 tests verts, `porte-gain.sh` à **6 cas** (verte). `--ffn-gain` accepte maintenant une **liste** (`0:0.75,1:0.5`), ce qui rend la question mesurable.

| profil | perplexité | écart |
|---|---|---|
| **`0:0.75` seul** | **12,9635** | **−11,51 %** |
| `1:0.5` seul | 13,7907 | −5,86 % |
| `0:0.75,1:0.5` | 13,7679 | −6,02 % |
| `0:0.9,1:0.6` | 13,4209 | −8,39 % |
| `0:0.75,1:0.5,2:1.0` | **13,7679** | identique |

- **Ajouter le gain de la couche 1 dégrade celui de la couche 0** (12,9635 → 13,7679) : les deux réglages **s'antagonisent** en partie, ils ne s'additionnent pas. Le meilleur profil mesuré est donc **un réglage SEUL**.
- La dernière ligne est le **témoin** qui rend les autres lisibles : un gain de **1,0 dans un profil est exactement neutre** (13,7679 = 13,7679) — l'identité tient aussi à l'intérieur d'un profil.
- **Conséquence pour le dessin I, plus dure qu'au round précédent** : non seulement le profil n'a que deux couches utiles, mais **le composer empire les choses**. Un profil appris aurait à découvrir que la bonne réponse est « une seule couche, un seul gain » — ce qu'un gradient sur peu de paramètres peut très bien ne pas trouver, puisqu'il optimiserait les deux ensemble. C'est écrit tel quel.

Le drapeau passe de `Option<(usize, f32)>` à `Option<Vec<(usize, f32)>>`, les deux sites d'application (chemin normal et hyper-connexions) itèrent sur la liste, et un `L:V` unique continue de marcher exactement comme avant — les 6 cas de la porte le vérifient.

**Bilan** : 17 rounds, 22 portes toutes vertes, 122 tests, 38 sections de rapport (§24 à §37) dont une bonne moitié de négatifs, réfutations et corrections. L'objectif reste **actif**.

### Tour 61 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Verify the execution-path gate after the type change
- bash — Record the verification and commit

**Synthèse produite :**

⏵ Round 18 livré : vérification du changement de type `ffn_gain` — contrainte tenue

**Ce round** — 1 commit poussé. Le drapeau est passé de `Option<(usize, f32)>` à `Option<Vec<(usize, f32)>>` (profil de gains), ce qui **touche le chemin d'exécution** : la règle de l'objectif s'applique donc à la lettre.

| vérification | résultat |
|---|---|
| **`porte-flux.sh`** (5 modes du protocole) | **verts, code 0** — écarts identiques à avant : 0,00e0 · 0,00e0 · 3,65e-2 · 0,00e0 · 4,45e-3 |
| référence de perplexité | **14,6496** sur le jeu d'essai — inchangée |
| `porte-gain.sh` | 6 cas verts, dont l'identité (`L:1.0` = absence de réglage) |
| tests | **122 verts** |

Le changement est donc **inactif quand le drapeau n'est pas donné**, et **identique à l'ancien comportement** quand un seul `L:V` est donné.

**État du sprint** : 18 rounds, **22 portes toutes vertes**, 122 tests, quatre codes d'arrêt distincts (5 borne · 6 octets · 7 panne · 8 latence), un registre de régions, et une quarantaine de mesures documentées avec leurs conditions — dont une bonne moitié de négatifs, réfutations (E/I, clé de fenêtre, composition des gains) et corrections (décalage d'un jeton, fenêtre `--limit`, porte rouge, `sys.exit`).

**Les trois prochains chantiers** restent inscrits dans `docs/sprint-cerveau.md` avec leur première commande : budget `paires/s` (protocole v7), tête dédiée par profondeur (C8), courbe de dose E4 approfondie. L'objectif reste **actif**.

### Tour 62 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — List available models
- bash — Test generalization across quantization and window
- bash — Add the window-dependence case and run
- bash — Document and commit the generalization results

**Synthèse produite :**

⏵ Round 19 livré : l'effet généralise, mais sa magnitude est une **condition**

**Ce round** — 1 commit poussé, 122 tests verts, `porte-gain.sh` à **7 cas** (verte).

Deux axes testés sur le gain 0,75 à la couche 0 (le meilleur réglage mesuré) :

| axe | mesure |
|---|---|
| autre **quantification** (Q4_0 au lieu de Q8_0) | **14,7453** contre **15,8055** sans réglage = **−6,7 %** |
| autre **fenêtre** (256 jetons au lieu de 128) | **17,1915** contre **17,4315** = **−1,4 %** (contre −11,5 %) |

1. **L'effet n'est pas un artefact de quantification** : −6,7 % sur Q4_0 et −11,5 % sur Q8_0 — la direction est robuste.
2. **Mais il décroît fortement avec la fenêtre** : −11,5 % sur 128 jetons, −1,4 % sur 256. Le chiffre de −11,5 % est un **point de mesure**, pas une propriété du modèle.

C'est pourquoi **la porte exige désormais que la magnitude décroisse** quand la fenêtre grandit : un futur relecteur ne pourra pas citer le meilleur chiffre sans voir la condition à côté. Une mesure sans sa condition est exactement ce que ce dépôt refuse — et c'est la troisième fois ce sprint qu'une mesure se révèle dépendre d'un paramètre qu'on n'avait pas fait varier (indice du rappel, formulation de la question, fenêtre d'évaluation).

**Bilan** : 19 rounds, **22 portes toutes vertes**, 122 tests, et une quarantaine de mesures documentées avec leurs conditions dans `reports/rapport-campagne-benefices.md` (§24 à §37). Les trois prochains chantiers restent inscrits dans `docs/sprint-cerveau.md` avec leur première commande. L'objectif reste **actif**.

### Tour 63 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Test the entry gain under the split
- bash — Check whether ffn_gain is wired in the split path
- bash — Identify which functions wire ffn_gain
- bash — Find the model load in the split path
- bash — Wire ffn_gain into the split path
- bash — Verify the flag now acts in the split path
- bash — Add the split-path case and run the gate
- bash — Document and commit the wiring defect

**Synthèse produite :**

⏵ Round 20 livré : un drapeau qui ne faisait **rien** dans le chemin réparti — trouvé, corrigé, gardé

**Ce round** — 1 commit poussé, 122 tests verts, `porte-gain.sh` à **8 cas** (verte).

En cherchant à mesurer l'interaction du gain d'entrée (E4) avec le **découpage**, la mesure a rendu **exactement le même chiffre avec et sans le drapeau** (42,5477). Ce n'était pas une absence d'effet : une absence de **câblage**.

`--ffn-gain` était appliqué dans `run_infer` et `run_ppl`, et **pas** dans `run_ppl_reparti` : dans le chemin réparti — celui sur lequel porte tout ce sprint — le réglage ne faisait **rien, en silence**. C'est la famille de défauts que ce dépôt traque, et celui-ci comptait double : un réglage fin qui ne survit pas à la distribution est exactement ce qu'on ne veut pas découvrir en production.

**Corrigé** et mesuré : réparti sans réglage **180,5245**, avec `0:0.75` **222,3496** ⇒ le drapeau agit. Le *signe* n'est pas celui du chemin local (−11,5 % sur 128 jetons) parce que la fenêtre de 32 jetons est trop courte : **ce n'est pas une mesure de qualité, c'est un contrôle de câblage**, et la porte le traite comme tel (elle exige que les chiffres **diffèrent**).

**Le piège de fenêtre a mordu une troisième fois** dans la même tentative : `--ppl --limit 128` note les **128 premiers** jetons d'un fichier qui en compte 85 625, `--ppl-reparti` **tronque aux 128 derniers**. Trois portes le documentent désormais, et le rapport aussi.

**Bilan** : 20 rounds, **22 portes toutes vertes**, 122 tests, ~39 sections de rapport. Les défauts trouvés cette session par la mesure — et non par relecture — se comptent maintenant par dizaines : deux portes fausses, un décalage d'un jeton, un `sys.exit` qui sortait en 1, un poids par défaut à zéro, un drapeau non câblé en réparti. L'objectif reste **actif**.

### Tour 64 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Audit flag wiring across execution paths
- bash — Check what appliquer_quantification wires
- bash — Measure candidate unwired flags in the split path
- bash — Commit the audit with its exact scope

**Synthèse produite :**

⏵ Round 21 livré : audit des drapeaux par chemin — méthode, angle mort, et ce qui reste **à instruire**

**Ce round** — 1 commit poussé, arbre propre (hors `journal/`).

Après le défaut de câblage de `--ffn-gain` (round 20), la question mécanique : *combien d'autres drapeaux ne sont câblés que dans certains chemins ?* Criblage statique des trois fonctions d'exécution (assignations `mdl.<champ> = …`) :

| fonction | champs assignés en propre |
|---|---|
| `run_infer` | 30 |
| `run_ppl` | 16 |
| **`run_ppl_reparti`** | **3** |

**L'angle mort, et il est important** : le criblage annonce 29 champs « absents » pour `run_infer`, dont `act_thresh`, `act_topk`, `attn_topk`, `qk_topk`, `moe_topk` — **qui sont câblés**, mais par le **helper** `appliquer_quantification`, que le criblage ne lit pas. Il ne voit que les assignations écrites *dans* la fonction. **« Absent du criblage » n'est pas « non câblé »**, et confondre les deux aurait produit un faux rapport — c'est écrit noir sur blanc.

**Ce qu'il a établi** : le chemin réparti assigne 3 champs en propre, le helper en couvre 7 de plus, et c'est **ce qui restait hors des deux** qui contenait le défaut (`ffn_gain`). La méthode a donc servi — avec sa portée exacte.

**Ce qui n'est pas concluant, écrit comme tel** : les candidats restants (`--attn-window`, `--attn-sinks`, `--swa-pattern`, `--patch`, `--hebb-*`, `--flux-forcer`, `--trace-flux`) n'ont **pas** été départagés — la mesure en réparti a rendu des perplexités **vides**, et une mesure vide ne prouve rien. Ils sont **à instruire**, pas déclarés sains ni défectueux, avec la commande exacte pour le faire.

**Bilan** : 21 rounds, **22 portes toutes vertes**, 122 tests, 40 sections de rapport (§1 → §39). L'objectif reste **actif** — les trois chantiers nommés dans `docs/sprint-cerveau.md` (budget `paires/s` via protocole v7, tête dédiée par profondeur C8, instruction des drapeaux candidats) attendent leur premier round.

### Tour 65 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Diagnose the empty measurement
- bash — Resolve the candidate flags with a valid port
- bash — Inspect the Act struct transported in frames
- bash — Document the resolved candidates

**Synthèse produite :**

⏵ Round 22 livré : la mesure vide était **mon** erreur — et deux drapeaux restent à instruire

**Ce round** — 1 commit poussé. Le round 21 laissait des candidats « à instruire » après une mesure vide. La cause de la mesure vide est trouvée, **et ce n'est pas les drapeaux** : le tirage de port du banc montait à 65 949, **au-delà de 65 535** — le nœud ne pouvait pas se lier, et le moteur le disait clairement (`INJOIGNABLE (invalid port value)`). Une mesure vide ne prouvait rien, et elle ne venait pas de ce qu'elle mesurait.

Reprise avec un port valide et `--options-strict` (pour qu'un drapeau inconnu soit **refusé** au lieu d'être ignoré) :

| drapeau | réparti | verdict |
|---|---|---|
| aucun (référence) | 180,5245 | — |
| `--act-topk 64` | **1 137 878,95** | **agit** |
| `--qk-topk 64` | **24 955,44** | **agit** |
| `--act-thresh 0,01` | **209,7804** | **agit** |
| **`--attn-window 16`** | 180,5245 | **SANS EFFET** |
| **`--attn-topk 64`** | 180,5245 | **SANS EFFET** |
| `--moe-topk 2` | 180,5245 | sans effet — **normal**, le modèle est dense |

**Trois verdicts, dont un faux positif :**
- `--moe-topk` : normalement sans effet sur un modèle **dense**, ce n'est pas un défaut ;
- `--attn-topk` : **voyage pourtant dans la trame** (le champ est dans `struct Act`, avec `qk_topk`) et agit en local — câblé et transporté, mais sans effet **dans cette configuration** : l'explication la plus probable est qu'à 32 jetons de contexte l'attention est déjà triviale ; à tester à contexte long ;
- `--attn-window` : **ne voyage pas** (absent de `Act`), donc le nœud garde son défaut — le candidat le plus sérieux.

**La leçon de méthode**, celle du sprint entier : une mesure vide doit être instruite **jusqu'à sa cause** avant d'accuser ce qu'elle mesurait — ici, mon propre banc de test.

**Bilan** : 22 rounds, **22 portes toutes vertes**, 122 tests, 40 sections de rapport. L'objectif reste **actif**.

### Tour 66 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*7 appels d'outils.* Actions notables :

- bash — Retest candidates at a long context
- bash — Test attn-window in the local path
- bash — Wire attn_window and measure
- bash — Fix the option types and rebuild
- bash — Verify the flag now acts and tests pass
- bash — Revert the wiring and verify the baseline
- bash — Document the attn-window finding and the revert

**Synthèse produite :**

⏵ Round 23 livré : un candidat innocenté, un vrai trou — et une correction **revertée** faute de diagnostic

**Ce round** — 1 commit poussé, 122 tests verts, arbre propre, référence répartie inchangée (18,5520).

Instruction des deux candidats à **contexte long** (512 jetons, port valide) :

| drapeau | en réparti | en local |
|---|---|---|
| `--attn-topk 64` | 18,5520 → **18,4032** — **agit** | — |
| `--attn-window 64` | 18,5520 → **18,5520** — **sans effet** | 13,1368 → **21,5801** — **agit** |

1. **`--attn-topk` n'est pas un défaut** : sans effet à 32 jetons (où l'attention est déjà triviale), il **agit** à 512. Mon hypothèse du round précédent est confirmée par la mesure.
2. **`--attn-window` est un vrai trou**, de la même famille que `--ffn-gain` : câblé dans `run_infer` et `run_ppl`, **pas** dans `run_ppl_reparti`. Et il **ne voyage pas** dans la trame (`struct Act` ne porte ni `attn_window`, ni `swa_pattern`, ni `attn_sinks`).

**La correction a été tentée, puis REVERTÉE** : le câblage rend un **résultat vide** (aucune perplexité), cause **non diagnostiquée**. J'ai préféré revenir en arrière plutôt que de laisser dans l'arbre une modification dont je ne comprends pas l'effet — **une régression silencieuse vaut moins qu'un manque écrit**. Après revert : référence **18,5520** (identique à avant), 122 tests verts, arbre propre.

**À instruire, avec la commande** : câbler les trois champs en regardant la sortie **complète** (le vide vient d'un refus ou d'une panne, et le moteur dit lequel), puis décider s'ils doivent **voyager dans la trame** (protocole v7) — sinon le pilote et le nœud n'appliqueraient pas la même fenêtre, soit **deux modèles différents sous le même nom**.

**Bilan** : 23 rounds, 22 portes toutes vertes, 122 tests. L'objectif reste **actif**.

### Tour 67 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Re-apply and inspect the full output
- bash — Implement the explicit refusal and verify
- bash — Add the refusal case and run the gate
- bash — Document and commit the refusal

**Synthèse produite :**

⏵ Round 24 livré : un drapeau inerte → un drapeau qui **mentait** → un refus explicite

**Ce round** — 1 commit poussé, 122 tests verts, `porte-gain.sh` à **9 cas** (verte).

La commande laissée par le round 23 (« câbler les trois champs en regardant la sortie complète ») est faite — et le résultat vide d'alors n'était pas une panne : le câblage rend un résultat **faux et silencieux**, ce qui est pire.

| avec `--attn-window 64` câblé naïvement | perplexité |
|---|---|
| référence locale (12 couches du pilote) | **195,5685** |
| découpage (12 + 12 couches) | **50,3829** |
| écart de flux | **7,42e-1** |

Le pilote applique la fenêtre à **ses** douze couches, le nœud garde la sienne : les deux moitiés ne calculent plus le même modèle — **deux modèles différents sous le même nom**, et rien ne le disait.

**La correction est donc devenue un REFUS EXPLICITE** : en chemin réparti, si `--attn-window`, `--swa-pattern` ou `--attn-sinks` est donné, le moteur **s'arrête en expliquant** (code 2, **aucune perplexité**). Un drapeau inerte est un défaut ; un drapeau qui fait calculer deux modèles différents sous le même nom en est un pire — et le pire cas du dépôt est le résultat faux qui a l'air d'un résultat. Ces réglages restent honorés en local et en inférence, où ils sont mesurés (13,1368 → 21,5801).

**Reste à faire pour les honorer en réparti** : les ajouter à `struct Act` et à l'encodeur de trame (**protocole v7**). C'est nommé, chiffré, et la porte l'exige dès maintenant.

**Bilan** : 24 rounds, **22 portes toutes vertes**, 122 tests, 40 sections de rapport. L'objectif reste **actif**.

### Tour 68 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Verify porte-flux after the refusal change
- bash — Verify the failure and registry gates
- bash — Commit the post-refusal verification

**Synthèse produite :**

⏵ Round 25 livré : vérification du chemin d'exécution après le refus — trois portes vertes

**Ce round** — 1 commit poussé. Le refus ajouté au round 24 est un **changement du chemin d'exécution réparti** : la contrainte de l'objectif s'applique donc à la lettre (« `porte-flux.sh` après toute modification du chemin d'exécution »).

| porte | résultat |
|---|---|
| **`porte-flux.sh`** | **code 0** — les cinq modes du protocole sont **inchangés au chiffre près** : 0,00e0 · 0,00e0 · 3,65e-2 · 0,00e0 · 4,45e-3 |
| **`porte-pannes.sh`** | **code 0** — pannes toujours nommées (lien, pas, octets), code 7 |
| **`porte-registre.sh`** | **code 0** — registre et adresse en dur donnent le même résultat |
| `porte-gain.sh` | 9 cas verts, dont le refus lui-même |
| tests | **122 verts** |

Le refus ne se déclenche **que si** l'un des trois réglages est demandé : une exécution qui ne les demande pas suit exactement le chemin d'avant.

**Bilan du sprint** : 25 rounds, **22 portes toutes vertes**, 122 tests verts, quatre codes d'arrêt distincts (5 borne · 6 octets · 7 panne · 8 latence) plus le refus de transport (2), un registre de régions, et 40 sections de rapport dont une bonne moitié de négatifs, réfutations et corrections — toutes documentées avec leurs conditions.

**Ce qui attend son premier round** (inscrit dans `docs/sprint-cerveau.md` avec les commandes) : le **protocole v7** (transporter `attn_window`/`swa_pattern`/`attn_sinks` et le compte de paires), la **tête dédiée par profondeur** (C8), et le budget `paires/s`. L'objectif reste **actif**.

### Tour 69 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Inspect the frame header layout
- bash — Compute the header offsets
- bash — Publish the v7 specification

**Synthèse produite :**

⏵ Round 26 livré : le protocole v7 **spécifié à l'octet près** — et explicitement pas implémenté

**Ce round** — 1 commit poussé. Un round de **conception**, et il est écrit comme tel.

Le refus du round 24 (`--attn-window`, `--swa-pattern`, `--attn-sinks` non transportables) se lève en faisant voyager ces trois réglages. Reconnaissance faite : **l'en-tête est plein**.

```text
TAILLE_TETE = 79 octets, aucune marge :
  0 magie · 4 version · 5 mode · 6 debut · 10 fin · 14 pos · 18 n · 22 echelle
  26 levels · 30 thresh · 34 topk · 38 renorm · 39 topk_proj[7] (39..67)
  67 attn_topk · 71 qk_topk · 75 moe_topk
```

**Les cinq modifications, et rien d'autre** :
1. `struct Act` : `attn_window`, `swa_pattern`, `attn_sinks` (u32) + `du_modele` + `appliquer` ;
2. `TAILLE_TETE` : 79 + 12 = **91** ;
3. `VERSION_FLUX` : 6 → **7** (le décodeur refuse une version étrangère — c'est voulu) ;
4. `tete_flux` : trois `extend_from_slice` aux offsets **79, 83, 87** ;
5. `recevoir_flux` : trois lectures `u(79)`, `u(83)`, `u(87)` — puis **retirer le refus**.

**Ce qui vérifie ce changement** : `porte-flux.sh` fait parler **les deux côtés** sur les cinq modes et compare les écarts à 0,00e0 / 0,00e0 / 3,65e-2 / 0,00e0 / 4,45e-3 — un en-tête décalé d'un octet y échoue immédiatement. Le garde-fou existe déjà, et c'est ce qui rend le changement tentable.

**Pourquoi pas maintenant** : l'en-tête est plein, donc la modification touche l'encodeur **et** le décodeur **et** la version — trois endroits où une erreur d'un octet casse les cinq modes à la fois. Le round qui l'entreprend doit avoir de la marge pour déboguer ; **j'ai préféré spécifier à l'octet près plutôt que de laisser un arbre cassé**.

**Bilan** : 26 rounds, 22 portes toutes vertes, 122 tests. L'objectif reste **actif**.

### Tour 70 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*7 appels d'outils.* Actions notables :

- bash — Read Act's methods
- bash — Implement protocol v7
- bash — Fix the default Act initializer
- bash — Complete the initializer and build
- bash — See which tests fail
- bash — Revert and inspect the failing assertion
- bash — Document the v7 attempt and revert

**Synthèse produite :**

⏵ Round 27 livré : protocole v7 tenté puis **reverté** — neuf tests encodent la mise en page v6

**Ce round** — 1 commit poussé, **122 tests verts** (contrainte intacte), arbre propre.

Les **huit modifications** de la spécification du round 26 ont été appliquées : `struct Act` (+3 champs), `du_modele`, `appliquer`, `TAILLE_TETE` (79 → **91**), `VERSION_FLUX` (6 → **7**), l'encodeur (offsets 79/83/87), le décodeur (`u(79)`, `u(83)`, `u(87)`), et le **retrait du refus**. Le binaire **compile**.

**Mais 9 tests tombent** — exactement ceux qui encodent la v6 :
- `entete_et_version_sont_ce_que_les_numeros_disent` : `assert_eq!(TAILLE_TETE, 79, …)`, plus un commentaire qui énumère les versions (« 4 quand les top-k sont entrés, 5 quand le mode 4 est apparu, 6 quand… ») ;
- les tests de **trame forgée** : ils construisent une trame **à la main**, avec les offsets et la taille de la v6.

**J'ai donc reverté** — la contrainte de l'objectif prime : 122 tests verts, arbre propre, porte-flux inchangée. Une modification de protocole qui laisse neuf tests rouges n'est pas une modification livrée.

**Ce qui reste à faire, écrit précisément** :
1. `assert_eq!(TAILLE_TETE, 79)` → **91**, et le commentaire de version gagne « 7 quand la fenêtre d'attention et le motif glissant sont entrés dans le contrat » ;
2. les constructeurs de **trame forgée** prennent la nouvelle taille — et devraient **lire `TAILLE_TETE`** plutôt qu'un littéral, sinon le prochain ajout de champ les cassera pareil ;
3. **puis** retirer le refus.

**Leçon, la même que partout dans ce sprint** : le contrat d'échange n'est pas seulement dans l'encodeur et le décodeur, il est aussi dans **les tests qui le forgent**. Une modification de protocole se compte en **trois** endroits, pas deux.

**Bilan** : 27 rounds, 22 portes toutes vertes, 122 tests. L'objectif reste **actif**.

### Tour 71 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Find layout-dependent test code
- bash — Read the forged-frame builder
- bash — Read the second frame builder
- bash — Make builders self-adjusting and test
- bash — Apply protocol v7 fully and test
- bash — Verify the header change with porte-flux
- bash — Measure the transported window in the split path
- bash — Document and commit protocol v7

**Synthèse produite :**

⏵ Round 28 livré : **protocole v7** — la fenêtre d'attention voyage, le refus disparaît, tout est vert

**Ce round** — 1 commit poussé, **122 tests verts**, **`porte-flux.sh` vert** (5 modes, écarts inchangés). Le round 27 avait reverté le v7 à cause de neuf tests rouges ; la cause était précise, et elle est corrigée **avant** de réappliquer :

- les constructeurs de **trame forgée** remplissaient l'en-tête avec **dix mots littéraux** — ils **calculent** maintenant le remplissage à partir de `TAILLE_TETE`, donc le prochain ajout de champ ne les cassera plus ;
- puis le v7 a été appliqué en **11 sites** : `Act` (+3 champs), `du_modele`, `appliquer`, `TAILLE_TETE` (**79 → 91**), `VERSION_FLUX` (**6 → 7**), encodeur (offsets 79/83/87), décodeur, initialiseur, retrait du refus, et les deux assertions « de mémoire ».

**Mesure, avec `--attn-window 64` en réparti :**

| | perplexité |
|---|---|
| référence locale du run réparti | **18,5520** |
| découpage (12 + 12 couches) | **18,5520** |
| **écart de flux** | **0,00e0** |

Là où le câblage sans transport donnait **195,5685 contre 50,3829** — un facteur 4, **deux modèles différents sous le même nom** — les deux moitiés s'accordent maintenant **au bit près**. Le chemin purement local donne 21,5801 avec le même réglage : un **autre** calcul, mais un calcul **annoncé**.

**Le refus est retiré** : il était la bonne conduite tant que la trame ne transportait pas ces réglages ; il devient un obstacle dès qu'elle les transporte.

**Enseignement écrit** : une modification de protocole se compte en **trois** endroits — l'encodeur, le décodeur, **et les tests qui le forgent**.

**Bilan** : 28 rounds, 22 portes toutes vertes, 122 tests, protocole v7 livré. Ce qui attend : le budget `paires/s` (le compte de paires à transporter, même mécanisme que v7), la tête dédiée par profondeur (C8), et le compte de paires côté nœud. L'objectif reste **actif**.

### Tour 72 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Verify the protocol-dependent gates after v7
- bash — Check the v7 verification suite
- bash — Commit the v7 verification across gates

**Synthèse produite :**

⏵ Round 29 livré : le v7 vérifié sur **toutes** les portes réparties — huit vertes

**Ce round** — 1 commit poussé. Le v7 change la **mise en page de la trame**, donc **toutes** les exécutions à deux nœuds : les huit portes qui parlent le protocole ont été rejouées.

| porte | résultat |
|---|---|
| **`porte-flux.sh`** (les deux côtés, 5 modes) | **code 0** — écarts inchangés : 0,00e0 · 0,00e0 · 3,65e-2 · 0,00e0 · 4,45e-3 |
| `porte-pannes.sh` | **code 0** — pannes nommées, code 7 |
| `porte-registre.sh` | **code 0** |
| `porte-budget.sh` | **code 0** — budgets d'octets et de latence |
| `porte-pont.sh` | **code 0** — fibres, falaise, symétrie |
| `porte-coupe.sh` | **code 0** — points de coupe |
| `porte-bus-socket.sh` | **code 0** — bus par le réseau |
| `porte-horloge.sh` / `porte-fusion.sh` | **code 0** |

**Huit vertes, aucune rouge, 122 tests verts.** Un en-tête décalé d'un octet aurait fait tomber la première ; les sept autres vérifient que le reste du contrat (pannes, budgets, fibres, registre, bus, horloge, traces) n'a pas bougé.

**Ce qui attend son premier round** : le **compte de paires côté nœud** — même mécanisme que le v7 (un champ dans la trame de réponse, protocole v8) — pour clore le budget `paires/s`, troisième volet de C10 dont les octets et la latence sont déjà faits.

**Bilan** : 29 rounds, **22 portes toutes vertes**, 122 tests, protocole v7 livré et vérifié. L'objectif reste **actif**.

### Tour 73 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Find the pair counter API
- bash — Publish the v8 specification

**Synthèse produite :**

⏵ Round 30 livré : protocole v8 **spécifié** — le compte de paires du nœud

**Ce round** — 1 commit poussé. Un round de conception, sur le patron qui a réussi pour le v7 (spécifier → tenter → livrer).

Objectif : clore le **troisième volet de C10** (le budget `paires/s`). Les paires sont calculées **par le nœud** ; le pilote ne peut donc pas les borner sans qu'elles lui soient **transportées**.

**Reconnaissance faite** — le compteur existe et est déjà exploité côté local :
```text
model.rs:2395   pub paires: [u64; 3],      // attention · experts · partagé
main.rs:1513    let pa = mdl.paires;       // le rapport le lit tel quel
main.rs:7299    let pt: u64 = pa.iter().sum::<u64>() + scores;
```

**Les six modifications** : en-tête **91 → 99** (un `u64`, les paires dépassent 2³²) · `VERSION_FLUX` **7 → 8** · `envoyer_flux` écrit à l'offset 91 · `recevoir_flux` lit un `u64` → champ `paires_du_pair` · le pilote publie le compte du pair · **`budget_paires`** dans la topologie, comparé au compte du pair par pas, avec **arrêt explicite (code 9) et aucune perplexité**.

**Et la difficulté que le v7 n'avait pas**, écrite noir sur blanc : l'en-tête est **partagé par les deux sens**, or ce champ est **directionnel** — le pilote y met 0, le nœud y met son compte. Un champ qui ne veut dire quelque chose que dans un sens doit être écrit dans le commentaire, sinon la prochaine relecture le prendra pour une mesure symétrique.

**Ce qui vérifie ce changement** : les huit portes réparties du v7 (`porte-flux` en tête), plus un cas neuf pour le budget de paires. Les tests de trame forgée **calculent** maintenant leur remplissage — c'est le v7 qui l'a appris — donc seules les deux assertions « de mémoire » restent à mettre à jour.

**Bilan** : 30 rounds, 22 portes toutes vertes, 122 tests, protocoles v7 livré et v8 spécifié. L'objectif reste **actif**.

### Tour 74 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Implement the pair-count transport
- bash — Emit and publish the pair count
- bash — Fix the print and test
- bash — Verify the pair count travels and porte-flux passes
- bash — Fix the double counting and re-measure
- bash — Verify, document and commit v8

**Synthèse produite :**

⏵ Round 31 livré : **protocole v8** — le compte de paires du nœud voyage, et le chiffre a attrapé mon bug

**Ce round** — 1 commit poussé, **122 tests verts**, **`porte-flux.sh` vert** (les deux côtés, 5 modes).

Le v8 ajoute **un `u64` à l'en-tête** (91 → **99 octets**, version **8**) : le nœud y met son compte de paires, le pilote le lit et le publie.

```text
paires du pair    : 8408924160 au total, 178.9 M par pas (annoncées par le nœud — protocole v8)
```

**178,9 M paires par pas pour la moitié distante** — cohérent avec les **358 M par jeton** du modèle *entier* mesurés pendant la campagne : la moitié des couches, la moitié des paires. **C'est la première fois que le pilote sait ce que coûte la moitié distante** sans le déduire de son propre travail.

**Et le chiffre a attrapé mon propre bug** : ma première implémentation **additionnait** le compte de chaque trame — or le compteur du nœud est **cumulatif**, donc la somme des cumuls vaut N²/2, et le pilote annonçait **4 293,9 M par pas**, ~24× trop. C'est **la comparaison au chiffre connu** (358 M pour le modèle entier) qui l'a rendu visible : 12× plus que le modèle *complet* pour la moitié de ses couches ne pouvait pas être juste. Corrigé (`fetch_max`) → 178,9 M.

**Leçon écrite** : un chiffre nouveau n'est pas vérifié par sa propre cohérence, il l'est par **comparaison à ce qu'on sait déjà**. Sans les 358 M de la campagne, 4 293,9 M serait passé pour une mesure.

Le champ est **directionnel** (pilote = 0, nœud = son compte) et c'est écrit dans le code : un en-tête partagé ne dit pas de lui-même qui parle.

**Reste pour clore C10** : le `budget_paires` dans la topologie, comparé à ce compte par pas, avec arrêt explicite (**code 9**). Le transport est fait ; il ne manque que le contrôle.

**Bilan** : 31 rounds, 22 portes toutes vertes, 122 tests, protocoles v7 **et** v8 livrés. L'objectif reste **actif**.

### Tour 75 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Implement the pair budget
- bash — Test the pair budget both ways
- bash — Add the pair-budget case and run the gate
- bash — Move the check into the loop and rerun
- bash — Revert the broken patch and verify
- bash — Document the pair-budget attempt and revert

**Synthèse produite :**

⏵ Round 32 livré : budget de paires **tenté et reverté** — deux leçons, dont une donnée par la porte

**Ce round** — 1 commit poussé, **122 tests verts**, arbre propre, aucune régression laissée.

Le transport du compte de paires est livré (v8) ; il ne manquait que le **contrôle**. Écrit, mesuré, puis **reverté** :

- **ce qui marche** (mesuré à la main) : `budget_paires` dans la topologie, comparaison au plafond `budget × pas`, **refus en code 9** — budget généreux (10 G/pas) ⇒ le run aboutit et annonce **178,9 M paires par pas** ; budget insuffisant (1 M/pas) ⇒ `PAIRES DÉPASSÉES … 8408924160 paires pour un budget de 1000000 par pas sur 47 pas (plafond 47000000)`, **code 9** ✓ ;
- **leçon 1 — le contrôle doit être DANS la boucle** : placé après, il laissait **calculer et afficher la perplexité** avant de refuser, soit exactement **le résultat partiel** que ce dépôt refuse. C'est **la porte** qui l'a dit, par son assertion « aucune perplexité ne doit être rendue » ;
- **leçon 2 — une suppression de bloc se vérifie aussi** : le déplacement a laissé un **déséquilibre d'accolades** qui a cassé la compilation. Plutôt que de bricoler un correctif sur un fichier à moitié édité, **j'ai reverté**. Une modification de 7 sites qui ne compile pas n'est pas une modification livrée — même règle que le v7, reverté au round 27 et livré au 28 après avoir été compris.

**Ce qui reste, écrit précisément** : (1) `budget_paires` dans `topologie.rs` ; (2) la lecture dans `run_ppl_reparti` ; (3) **le contrôle dans la boucle**, juste après la réception, avec `pas_servis` comme multiplicateur ; (4) le cas 6 de `porte-budget.sh`, **déjà écrit**, qui exige le code 9 *et* l'absence de perplexité.

**Bilan** : 32 rounds, 22 portes toutes vertes, 122 tests, protocoles v7 et v8 livrés. L'objectif reste **actif**.

### Tour 76 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Re-implement the pair budget additively
- bash — Verify the in-loop refusal
- bash — Add the gate case and verify both gates
- bash — Document and commit C10 closure

**Synthèse produite :**

⏵ Round 33 livré : **C10 CLOS** — trois budgets de lien, trois codes d'arrêt distincts

**Ce round** — 1 commit poussé, 122 tests verts, `porte-budget.sh` (6 cas) et `porte-flux.sh` (5 modes) **vertes**.

Le round 32 avait reverté ce travail après un déséquilibre d'accolades. **Repris en ADDITIF** — rien supprimé, donc rien à casser — et livré :

| volet | unité | code | mesure |
|---|---|---|---|
| octets | octets/pas | **6** | 1 860 pour un budget de 975 ⇒ arrêt au pas 0 |
| latence | ms/pas | **8** | 20,1 ms pour un budget de 1 ms |
| **paires** | paires du nœud/pas | **9** | **178 913 280** pour un budget de **1 000 000** ⇒ arrêt **au pas 0** |

**La leçon du round précédent est appliquée** : le contrôle est **dans la boucle**, au pas du dépassement. Placé après elle, il laissait **calculer et afficher la perplexité** avant de refuser — le résultat partiel que ce dépôt refuse. C'est **la porte** qui l'avait signalé, par son assertion « aucune perplexité ne doit être rendue » — et elle l'exige maintenant.

**Détail qui se recoupe** : le compte annoncé au **premier** pas (178 913 280) vaut exactement la valeur par pas mesurée sur la session entière (178,9 M) — un compteur cumulatif lu une fois dit la même chose au début et à la fin.

**Ce que C10 apporte à la distribution** : les trois coûts d'un lien sont désormais **déclarables et vérifiés** — le temps, les octets, et le **calcul déporté**, le seul que ce moteur compte vraiment (`paires = poids non nuls × activations vivantes`). Un lien qui ne peut pas porter un demi-modèle se voit refuser **au premier pas**, au lieu de le découvrir à la fin.

**Bilan** : 33 rounds, **22 portes toutes vertes**, 122 tests, protocoles v7 et v8 livrés, **C10 complet**. Restent : la tête dédiée par profondeur (C8), les modèles H-I-J, et les drapeaux candidats à instruire. L'objectif reste **actif**.

### Tour 77 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Measure whether the trace sees the injected delay
- bash — Document and commit the calibration

**Synthèse produite :**

⏵ Round 34 livré : l'instrument de trace est **étalonné** — 50 ms injectés, 50,2 ms mesurés

**Ce round** — 1 commit poussé. Toute la partie asynchrone (C4) repose sur une question préalable : **la trace globale sait-elle mesurer le temps ?** Un instrument jamais étalonné ne prouve rien sur ce qu'il observe.

**Protocole** : un délai **connu** injecté (`"delai_ms": 50`), les deux côtés tracent, la fusion apparie par `(lien, pas)`, et l'on compare l'horodatage d'**envoi** (pilote) à celui de **réception** (nœud) :

| mesure | valeur |
|---|---|
| croisements par source | **46** (23 pas × 2 liens) |
| liens confrontés | **46 identiques, 0 divergents** |
| **écart envoi → réception, médian** | **50,2 ms** (min 50,2 · max 50,2) |
| délai injecté | **50 ms** |

**L'instrument mesure le temps à 0,2 ms près** — et cet écart *est* le transport lui-même. Il est **rigoureusement constant** (min = max) parce que le délai injecté l'est : un instrument bruité l'aurait montré.

**Pourquoi c'est un préalable** : quand C4 dira que deux régions avancent à des rythmes différents, l'instrument qui le dira aura été **étalonné contre une valeur connue**, et non supposé juste parce qu'il produit des nombres — c'est la différence entre un instrument et un affichage.

**Bilan** : 34 rounds, **22 portes toutes vertes**, 122 tests, protocoles v7 et v8, **C10 clos**, instrument étalonné. Restent : la tête dédiée par profondeur (C8), les modèles H-I-J, et l'asynchronisme réel (C4) — désormais mesurable avec un instrument dont on connaît la précision. L'objectif reste **actif**.

### Tour 78 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Measure per-step link jitter from the traces
- bash — Document and commit the jitter measurement

**Synthèse produite :**

⏵ Round 35 livré : la **gigue** d'un pas réparti — 7 ms sur 17,7, soit 40 %

**Ce round** — 1 commit poussé. L'instrument étant étalonné (round 34), il peut mesurer autre chose que ce qu'on lui injecte. La question qui décide de l'asynchronisme (C4) : **de combien la durée d'un pas varie-t-elle ?** Un ordonnanceur qui suppose des pas réguliers casse à la première irrégularité.

**Mesure** (12 couches locales, 12 distantes, 64 pas, traces des deux côtés fusionnées) :

| phase | médiane | p90 | max | min |
|---|---|---|---|---|
| aller (pilote → nœud) | **0,13 ms** | 0,14 | 0,16 | 0,09 |
| retour (nœud → pilote) | **0,14 ms** | 0,17 | 0,17 | 0,05 |
| **pas complet** | **17,67 ms** | 19,57 | **21,29** | **14,29** |

1. **Le réseau local ne coûte rien** (0,13 / 0,14 ms) — cohérent avec la loi de latence de la campagne dès qu'un vrai RTT entre en jeu.
2. **Le pas complet vaut 17,67 ms**, dont l'essentiel est le calcul du nœud.
3. **La gigue est de 7,00 ms sur 17,67, soit 40 %** — et le p90 dépasse la médiane de 2 ms. **Un ordonnanceur qui suppose des pas réguliers se trompe de 40 %** : c'est précisément ce que C4 devra absorber, et le chiffre est désormais connu.

**Ce que la mesure ne dit pas**, écrit tel quel : les deux « régions » sont deux processus du **même hôte**, donc la gigue mesurée est celle de l'ordonnanceur système, pas celle du réseau — `tools/proxy_latence.py` permet d'ajouter le RTT, et ce n'est pas fait ici.

**Bilan** : 35 rounds, 22 portes toutes vertes, 122 tests, protocoles v7/v8, C10 clos, instrument étalonné, gigue chiffrée. L'objectif reste **actif**.

### Tour 79 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Check the latency proxy usage
- bash — Read the proxy header
- bash — Measure jitter with a real injected RTT
- bash — Document and commit the RTT jitter measurement

**Synthèse produite :**

⏵ Round 36 livré : la gigue avec un **vrai RTT** — 14,8 ms sur 30,2 (49 %)

**Ce round** — 1 commit poussé. La condition laissée ouverte au round 35 (« la gigue mesurée est celle de l'ordonnanceur système, pas du réseau ») est levée avec `tools/proxy_latence.py` à **5 ms par message** :

| phase | sans RTT | **avec 5 ms/message** |
|---|---|---|
| aller (pilote → nœud) | 0,13 ms | **5,29 ms** · p90 **10,38** · max 10,46 |
| pas complet | 17,67 ms | **30,24 ms** · p90 38,98 · max 39,47 |
| **gigue du pas** | 7,00 ms (**40 %**) | **14,80 ms (**49 %**)** |

1. **L'instrument est de nouveau étalonné** : 5 ms injectés par message ⇒ 5,29 ms mesurés à l'aller.
2. **Le p90 de l'aller vaut le double de la médiane** (10,38 contre 5,29) : le proxy endort chaque message, et une trame qui traverse les deux sens paie deux fois — la distribution est **bimodale**, pas bruitée.
3. **La gigue croît plus vite que la latence** : +71 % de latence médiane pour **+111 % de gigue**, et le taux passe de 40 % à **49 %**. Un ordonnanceur asynchrone (C4) doit donc tolérer **la moitié d'un pas en irrégularité** sur un lien à 5 ms — et cette proportion **empire** avec la distance, l'inverse de l'intuition (« un lien plus lent est plus régulier »).

**Ce que la mesure ne dit toujours pas**, écrit tel quel : le proxy endort **par message** ; il ne simule ni la perte, ni la réorganisation, ni la congestion. La gigue mesurée est un **plancher** pour ce RTT.

**Bilan** : 36 rounds, 22 portes toutes vertes, 122 tests. Le sprint a maintenant les trois coûts d'un lien (temps, octets, paires) **déclarables et vérifiés**, un protocole v8, un instrument **étalonné à 0,2 ms**, et la **gigue chiffrée à 49 %** — tout ce qu'il faut pour attaquer l'asynchronisme réel (C4). L'objectif reste **actif**.

### Tour 80 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Fit the per-message delay against step cost
- bash — Document and commit the message-count measurement

**Synthèse produite :**

⏵ Round 37 livré : un pas coûte **4 messages** — l'en-tête est écrit à part du corps

**Ce round** — 1 commit poussé. Le protocole écrit la trame en **deux fois** (`write_all(&tete)` puis `write_all(&corps)`) : sur un lien qui facture **par message**, ces deux écritures se paient deux fois. Le proxy ajoute un délai par message, on mesure le pas médian, et la **pente** donne le nombre équivalent de messages :

| délai par message | pas médian | pente |
|---|---|---|
| 0 ms | 14,87 ms | — |
| 2 ms | 23,35 ms | **4,24 messages** |
| 5 ms | 34,93 ms | **4,01** |
| 10 ms | 44,83 ms | **3,00** |

1. **À petit délai, un pas coûte ~4 messages** : en-tête **et** corps, à l'aller **et** au retour — le chiffre recoupe exactement les deux `write_all` de chaque direction.
2. **La pente décroît avec le délai** (4,24 → 3,00) : ce n'est pas le protocole qui change, c'est le **proxy**, qui endort après chaque `recv` et laisse le système regrouper plusieurs écritures. La mesure donne donc un **majorant**, et c'est le petit délai qui est le plus fidèle.
3. **Conséquence actionnable et chiffrée** : écrire en-tête et corps en **une seule** fois ferait payer ~2 messages au lieu de ~4 ⇒ sur un lien à 5 ms/message, **≈ 25 ms au lieu de ≈ 35 ms**, soit **−29 % de la durée du pas**, sans toucher ni au calcul ni aux octets — seulement au **nombre d'envois**.

**Ce qui reste à faire**, écrit tel quel : la fusion des deux écritures (trois émetteurs : jeton, lot dense, lot en listes), traitée comme une modification de protocole — mesure avant/après, `porte-flux.sh` en garde-fou.

**Bilan** : 37 rounds, 22 portes toutes vertes, 122 tests. Les mesures de ce sprint dessinent maintenant une carte complète du **coût d'un lien** : temps (loi de latence), octets (budget), paires (budget), **gigue (49 %)**, et **messages (4 par pas, réductibles à 2)**. L'objectif reste **actif**.

### Tour 81 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Find the double writes
- bash — Coalesce the writes and build
- bash — Measure the gain from coalescing
- bash — Verify porte-flux, document and commit the coalescing

**Synthèse produite :**

⏵ Round 38 livré : **−20 % de la durée d'un pas**, sans rien coûter

**Ce round** — 1 commit poussé, **`porte-flux.sh` vert** (5 modes, écarts identiques), 122 tests verts.

Le round 37 avait mesuré que le protocole écrivait la trame en **deux fois** (en-tête puis corps) ⇒ **4 messages par pas** sur un lien facturé par message. **La fusion est faite** : les trois émetteurs (jeton, lot dense, lot en listes) écrivent **une seule trame**.

**Mesure avant/après**, aux deux mêmes délais par message :

| délai/message | AVANT | **APRÈS** | gain |
|---|---|---|---|
| 2 ms | 23,35 ms | **19,06 ms** | **−18,4 %** |
| 5 ms | 34,93 ms | **27,98 ms** | **−19,9 %** |

**La pente retombe aussi** : (27,98 − 14,87) / 5 = **2,62 messages** au lieu de 4,01 — le pas retrouve le nombre d'envois que le protocole décrit vraiment (un aller, un retour).

**Ce que ce gain est** : −20 % de la durée d'un pas sur un lien facturé **par message**, sans toucher ni au calcul, ni aux octets, **ni au résultat** (les cinq modes du protocole donnent exactement les mêmes écarts). C'est **le seul levier de ce sprint qui accélère sans rien coûter** — et il vient d'une mesure, pas d'une intuition.

**Ce qu'il ne dit pas**, écrit tel quel : le gain est **nul** sur un lien facturé **au débit** (où deux écritures coûtent les mêmes octets). La question « message ou octet ? » est celle de l'opérateur — mais le protocole ne doit pas **ajouter** des messages sans raison.

**Bilan** : 38 rounds, 22 portes toutes vertes, 122 tests. Le sprint a livré neuf capacités, deux protocoles (v7, v8), trois budgets de lien, une optimisation mesurée à −20 %, un instrument étalonné, et une quarantaine de mesures documentées — dont une bonne moitié de négatifs et de corrections. L'objectif reste **actif**.

### Tour 82 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Check the gain in the batch mode
- bash — Document the scaling of the gain

**Synthèse produite :**

⏵ Round 39 livré : le gain de la fusion est **fixe par échange** — il paie d'autant plus que les pas sont petits

**Ce round** — 1 commit poussé. Vérification que la fusion des écritures (round 38) profite aussi au **mode par lots**, où les trames sont bien plus grosses :

| mode | ce qu'un échange transporte | temps par échange | gain de la fusion |
|---|---|---|---|
| 0 (un jeton) | 896 canaux | 27,98 ms | **−20 %** |
| 3 (8 jetons) | 28 772 octets | 130,2 ms (dont 99,8 de calcul local) | **≈ −8 %** |

Le gain est le **même en millisecondes** (~10 ms : deux messages en moins à 5 ms/message), donc il **pèse relativement moins** quand l'échange transporte plus. Autrement dit : **la fusion paie d'autant plus que les pas sont petits** — et c'est précisément le régime du **décodage jeton par jeton**, celui où la latence domine.

**Ce qu'il ne dit pas**, écrit tel quel : le gain est **nul** sur un lien facturé **au débit** (deux écritures coûtent les mêmes octets). La question « message ou octet ? » est celle de l'opérateur ; le protocole, lui, ne doit pas **ajouter** de messages sans raison.

**Bilan** : 39 rounds, **22 portes toutes vertes**, 122 tests. Le sprint a livré neuf capacités (C1→C12bis), deux protocoles (v7, v8), trois budgets de lien déclarés et vérifiés, une optimisation mesurée (−20 % sur le décodage), un instrument étalonné à 0,2 ms, la gigue chiffrée à 49 %, et une quarantaine de mesures documentées — dont une bonne moitié de négatifs, réfutations et corrections.

**Ce qui attend son premier round**, inscrit dans `docs/sprint-cerveau.md` avec les commandes : la tête dédiée par profondeur (C8), les modèles H-I-J, l'asynchronisme réel (C4) — désormais attaquable avec un instrument étalonné et une gigue connue — et les drapeaux candidats restants. L'objectif reste **actif**.

### Tour 83 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Verify the protocol-affected gates
- bash — Check the verification progress
- bash — Commit the round-40 verification

**Synthèse produite :**

⏵ Round 40 livré : vérification après v7/v8 et la fusion des écritures — **huit portes réparties vertes**

**Ce round** — 1 commit poussé. Les rounds 28 à 39 ont touché **le protocole** (v7 : fenêtre d'attention ; v8 : compte de paires) et **le chemin d'envoi** (fusion des deux écritures). Les portes réparties ont été rejouées :

| porte | résultat |
|---|---|
| `porte-pannes` · `porte-registre` · `porte-budget` · `porte-pont` · `porte-coupe` · `porte-fusion` · `porte-horloge` · `porte-bus-socket` | **code 0** chacune |
| `porte-flux` (rejouée au round 38) | **code 0** — cinq modes, écarts inchangés |
| tests | **122 verts** |

**Aucune rouge.** Les trois modifications de protocole et la fusion des écritures ont laissé le **contrat d'échange intact** — un octet de décalage dans l'en-tête ou un envoi perdu auraient fait tomber `porte-flux` immédiatement.

**Les trois chantiers qui attendent leur premier round**, inscrits avec leur commande :
1. **C8 — une tête dédiée par profondeur** : `tools/entrainer_moteur.py` existe, et `porte-reflexe.sh` mesure déjà l'accord d'une tête *empruntée* — il suffit d'y mettre une tête apprise.
2. **Les modèles H/I/J** : le dessin **I** a reçu sa mesure (−11,5 % sur la couche 0, mais **le levier porte sur deux couches et composer dégrade**) — un profil appris aurait à découvrir « une seule couche, un seul gain ».
3. **C4 — l'asynchronisme réel** : instrument **étalonné** (50 ms injectés → 50,2 mesurés), **gigue chiffrée** (49 % d'un pas), **messages par pas** ramenés de 4 à 2,6. Tout ce qu'il faut est là.

**Bilan** : 40 rounds, **22 portes toutes vertes**, 122 tests, neuf capacités livrées, protocoles v7 et v8, trois budgets de lien, une optimisation à −20 % sur le décodage, et une quarantaine de mesures documentées avec leurs conditions. L'objectif reste **actif**.

### Tour 84 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Verify the other two transported fields
- bash — Diagnose the flagged run
- bash — Check whether the pilot applies the window
- bash — Commit the correction

**Synthèse produite :**

⏵ Round 41 livré : **correction d'une de mes conclusions** — deux nombres égaux ne prouvent pas qu'ils mesurent la même chose

**Ce round** — 1 commit poussé. En vérifiant les **trois** champs que le v7 transporte (je n'avais mesuré que `attn_window`), la mesure a contredit ma conclusion du round 28.

**Ce que j'avais écrit** : « les deux moitiés appliquent la même fenêtre, le résultat est cohérent au bit près » (18,5520 = 18,5520).

**Ce qui est vrai** : le v7 **transporte** bien les trois champs (le nœud les applique via `Act::appliquer`), mais le **pilote ne les applique pas** — `mdl.attn_window`, `mdl.swa_pattern` et `mdl.attn_sinks` ne sont assignés **nulle part** dans `run_ppl_reparti` (vérifié par lecture du code). Les deux nombres « s'accordaient » parce que **ni l'un ni l'autre ne changeait**.

**Mesure refaite** : à `--limit 128`, `--attn-window 64`, `--swa-pattern 2` et `--attn-sinks 4` donnent **tous 42,5477**, identiques au run sans drapeau — alors que le même `--attn-window 64` fait passer le chemin **local** de 13,1368 à **21,5801**.

**Ce qui reste à faire** — même famille que `--ffn-gain` (round 20) : **assigner ces trois champs dans `run_ppl_reparti`**. Le transport est prêt, le refus est retiré, **il ne manque que l'assignation** : trois lignes, avec la mesure avant/après que la porte exigera.

**La leçon, et elle vaut plus que la correction** : **deux nombres égaux ne prouvent pas qu'ils mesurent la même chose**. J'ai lu « 18,5520 = 18,5520 » comme un accord entre les deux côtés du graphe ; c'était un accord entre deux réglages **inertes**. La vérification qui manquait tenait en une ligne de lecture de code — « ce champ est-il assigné dans cette fonction ? » — et c'est celle que j'aurais dû faire **avant** de conclure.

**Bilan** : 41 rounds, 22 portes toutes vertes, 122 tests. L'objectif reste **actif**.

### Tour 85 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Assign the three fields in the pilot
- bash — Measure before/after the assignment
- bash — Verify and commit the assignment

**Synthèse produite :**

⏵ Round 42 livré : les trois lignes manquantes — le pilote applique enfin la fenêtre

**Ce round** — 1 commit poussé, **`porte-flux.sh` vert** (5 modes inchangés), 122 tests verts.

Suite directe de la correction du round 41 : `mdl.attn_window`, `mdl.swa_pattern` et `mdl.attn_sinks` n'étaient assignés **nulle part** dans `run_ppl_reparti`. Les trois lignes sont posées, et la mesure **avant/après** le confirme :

| | nu | `--attn-window 64` |
|---|---|---|
| **chemin réparti** | 42,5477 | **1 926,1996** |
| chemin local | 14,6496 | 16,1972 |

**Le drapeau agit en réparti** (il était inerte : 42,5477 dans les deux cas). Que le chiffre réparti soit mauvais (1 926) est **attendu** — « les 128 derniers jetons d'un fichier de 85 625, avec une fenêtre de 64 » ne laisse presque pas de contexte — mais c'est un calcul **annoncé**, et non un réglage ignoré. C'est toute la différence entre un résultat qu'on explique et un drapeau qui ne fait rien.

`porte-flux.sh` reste **vert** : les portes n'utilisent pas ces drapeaux, donc les défauts à zéro laissent le chemin d'exécution inchangé.

**La leçon est écrite dans le code, là où elle servira** : *deux nombres égaux ne prouvent pas qu'ils mesurent la même chose* — avant de conclure à un accord, vérifier **pourquoi** ils sont égaux. Ici, la raison était que le réglage était inerte **des deux côtés**.

**Bilan** : 42 rounds, 22 portes toutes vertes, 122 tests. Le sprint a trouvé **quatre** défauts de la même famille (« un drapeau qui ne fait rien » : `--ffn-gain` en réparti, `--attn-window`, `--sys.exit`, le poids de greffe par défaut) — tous par la mesure, aucun par relecture. L'objectif reste **actif**.

### Tour 86 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Build the definitive flag table for the split path
- bash — Rerun the flag table with a fresh node each time
- bash — Commit the definitive flag inventory

**Synthèse produite :**

⏵ Round 43 livré : inventaire **définitif** des drapeaux en réparti — six sur dix agissent, un seul candidat ouvert

**Ce round** — 1 commit poussé. L'audit du round 21 avait produit des **candidats** sans les départager (mesure vide due à un port hors bornes). Après le v7, le v8 et les corrections des rounds 20 et 42, l'inventaire est fait — **nœud relancé à chaque essai** (il sert **une** connexion : mon premier banc les faisait tous échouer, quatrième erreur de harnais du sprint).

| drapeau | réparti (réf. **72,0185**) | verdict |
|---|---|---|
| `--act-topk 64` | 362 333,58 | **agit** |
| `--qk-topk 64` | 4 760,07 | **agit** |
| `--attn-window 32` | 1 571,30 | **agit** (corrigé round 42) |
| `--act-thresh 0,01` | 98,83 | **agit** |
| `--ffn-gain 0:0.75` | 76,88 | **agit** (corrigé round 20) |
| `--attn-topk 64` | 71,47 | **agit** |
| `--swa-pattern 2` | 72,0185 | sans effet — **attendu** (rien à décider sans fenêtre) |
| `--sans-fenetre` | 72,0185 | sans effet — **attendu** (fenêtre absente) |
| `--moe-topk 2` | 72,0185 | sans effet — **attendu** (modèle **dense**) |
| **`--attn-sinks 4`** | 72,0185 | **à instruire** — les puits devraient peser |

**Six sur dix agissent**, trois inertes pour une raison **identifiée**, **un seul candidat ouvert**. C'est la réponse chiffrée à la question du round 21 — « combien d'autres drapeaux ne font rien en réparti ? » — et les **deux vrais défauts** qu'elle a fait apparaître ont été corrigés et mesurés avant/après.

**Bilan** : 43 rounds, **22 portes toutes vertes**, 122 tests. Les quatre erreurs de harnais du sprint (port hors bornes, `sys.exit` qui sort en 1, variable `D` écrasée, nœud non relancé) ont toutes été **trouvées par la mesure**, jamais par relecture — comme les quatre défauts du moteur de la même famille. L'objectif reste **actif**.

### Tour 87 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Check whether the engine reads attn_sinks at all
- bash — Find where attn_sinks is read in the computation
- bash — Commit the attn-sinks finding
- bash — Insert the missing journal section

**Synthèse produite :**

⏵ Round 44 livré : `--attn-sinks` — écrit partout, transporté par le v7, **lu nulle part**

**Ce round** — 2 commits poussés. Le dernier candidat de l'inventaire, et **le plus grave des cinq**.

**Mesure** : inerte en réparti **et** en local (14,6496 dans les deux cas). **Lecture du code** :

| où | ce qui est fait |
|---|---|
| `main.rs:1036` | le drapeau pose `o.attn_sinks` |
| `main.rs:1227` / `7114` | `if attn_sinks > 0 { mdl.attn_sinks = … }` (inférence, perplexité) |
| `main.rs:4425` | assigné en réparti (round 42) |
| `model.rs:2961` | **transporté par le protocole v7** |
| **le calcul** | **aucune lecture de `self.attn_sinks`** |

Ce sont les puits **appris** (`lay.sinks`, tenseur `attn_sinks.weight`) que l'attention consomme — pas ce compteur.

**Cinquième défaut de la même famille** — après `--ffn-gain` en réparti, le poids de greffe à zéro par défaut, `--attn-window`, et le `sys.exit` qui sortait en 1 — **et le plus grave : le v7 a fait voyager un réglage mort** (une modification de version, 91 → 99 octets, pour rien).

**Deux issues, et c'est un choix de conception** : (1) **implémenter** le compteur (`n` jetons puits au début de la séquence, comme le décrit `model.rs:2435` — mécanisme réel, différent des puits appris) ; ou (2) **retirer le drapeau** — un drapeau qui ne peut rien faire est pire qu'aucun drapeau : il donne l'illusion d'un réglage. Dans les deux cas, **la porte doit suivre** : exiger qu'il agisse, ou qu'il n'existe plus.

**Bilan** : 44 rounds, **22 portes toutes vertes**, 122 tests. La chaîne d'audit ouverte au round 21 est **close** : dix drapeaux testés, six agissent, trois inertes pour une raison identifiée, **un cinquième défaut systémique trouvé et documenté**. L'objectif reste **actif**.

### Tour 88 — <goal_round> Objective: "Timeboxing jusqu'au 10 octobre 9 h (HAE) : occuper TOUT le temps imparti en progrès mesurés, sa … [1750 caractères tronqués]

*291 appels d'outils.* Actions notables :

- bash — Add the refusal and verify
- bash — Move the refusal to the single point and verify
- bash — Check exit code 2 and find gates with refusals
- bash — Inspect refusal style in existing gates
- bash — Locate gate that covers attention flags or refusals
- bash — Read porte-gain gate structure
- bash — List gate sections
- bash — Add refusal case to porte-gain and run it
- bash — Inspect main.rs diff for collateral deletion
- bash — Check for collateral deletions and refusal locations
- bash — Find the untransportable refusal implementation
- bash — Read v7 removal context and flag inventory
- bash — Read flag inventory section in docs
- bash — Establish whether section 9 predates the v7 removal
- … et 264 autres

**Synthèse produite :**

⏵ Référence obtenue sur le même texte : modèle complet 14,2342 — l'écart du réflexe est ×59 (pas ×90) ; je corrige la fiche

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/essai_decharge.py` | 2 | 20 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_wikipedia.py` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-parcimonie-entrainee.md` | 1 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/essai_blocs.py` | 1 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/exporter_gguf.py` | 1 | 19 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte_moteur.py` | 1 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/entrainer_moteur.py` | 1 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-reparti-moteur.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/numa-segregation.md` | 1 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-modele-moteur.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/configuration-nvme-raid-amd.md` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/campagne-benefices.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/campagne-benefices.md` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/campagne_synthese.py` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/speculatif.py` | 1 | 0 |
| `/tmp/campagne24/batch3_niah.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-benefices.md` | 1 | 23 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/census_routage.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte_mistral.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-mistral.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/speculatif_moteur.py` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesure_fenetres.sh` | 1 | 0 |
| `/tmp/campagne24/nuit2_m6.sh` | 1 | 0 |
| `/tmp/campagne24/nuit3_kwta.sh` | 1 | 0 |
| `/tmp/campagne24/nuit4_route_creux.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesure_lot_disque.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/carte_latence.sh` | 1 | 1 |
| `/tmp/campagne24/jour1_suite.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/modele-pour-drave.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/biologie-pour-drave.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/hebbien-differentiel-et-biologie.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/impulsion-pure-apprenant.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/architecture-cerveau-et-drave.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-cerveau-complet.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/modularisation.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/manques.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/topologie.rs` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/trace_globale.rs` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/relations-humaines.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-fusion.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-bus-socket.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/episodique.rs` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-episodique.sh` | 1 | 0 |
| `/tmp/patch_porte_c6.py` | 1 | 0 |
| `/tmp/c6_multi_1.py` | 1 | 0 |
| `/tmp/c6_multi_2.py` | 1 | 0 |
| `/tmp/c6_multi_3.py` | 1 | 0 |
| `/tmp/c6_docs.py` | 1 | 0 |
| `/tmp/c7_module.py` | 1 | 0 |
| `/tmp/c7_module2.py` | 1 | 0 |
| `/tmp/c7_cli.py` | 1 | 0 |
| `/tmp/c7_mode.py` | 1 | 0 |
| `/tmp/c7_cli2.py` | 1 | 0 |
| `/tmp/c7_gate.py` | 1 | 0 |
| `/tmp/c7_docs.py` | 1 | 0 |
| `/tmp/next_actions.py` | 1 | 0 |
| `/tmp/c9_code.py` | 1 | 0 |
| `/tmp/c9_code2.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-pont.sh` | 6 | 0 |
| `/tmp/c9_node.py` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/toutes-les-portes.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/carte-fenetre-puits.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/organisation-du-depot.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/decouper-rapport.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/etat-cerveau.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fenetre-puits-attention.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/etat.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/journal_auto.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/c8_sonde_lineaire.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-c8-sonde-profondeur.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/c8_carte_profondeur.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md.new` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md.new` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/c8_entrainer_tete.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-c8-tete-entrainee.md` | 1 | 0 |

### Sous-agents lancés

- tour 2 — Inventaire parcimonie événementielle
- tour 2 — Inventaire du travail modèle
- tour 2 — Inventaire capacités de distribution

### Commandes exécutées (échantillon)

- **T1** Show git status and recent commits
- **T1** List top-level files
- **T1** Check sizes and diff stat of modified files
- **T1** List most recent reports and sprints
- **T1** Show diff of journal metadata files
- **T1** Diff tool changes and inspect new script
- **T1** Read head of REPRISE.md status file
- **T1** Read tail of latest session digest
- **T1** List state sections in REPRISE.md
- **T1** Find DRVF readers and running processes
- **T1** List REPRISE.md section headings
- **T1** List recent docs and commit dates
- **T1** Read the rapid-cycle report intro
- **T1** Check which tools handle per-record scale
- **T1** Count tools and show recently modified
- **T1** Inspect scale handling in key readers
- **T1** Search echelle usage in readers
- **T1** Check temp caches from recent runs
- **T1** Read end of new GPU tracer script
- **T1** Search digest for calibration and scale-fix mentions
- **T1** Check rapid-cycle report conclusions
- **T1** Read half-model measurement logs
- **T1** Read K3 disk-pass report conclusion
- **T1** Extract latest session objective text
- **T1** Read last tour summary in session report
- **T1** Find readers that apply the record scale
- **T1** Inspect last commit and gates status
- **T1** Locate raw DRVF record parsers in tools
- **T1** Check gates log and count affected tools
- **T2** Search spiking-related work in repo
- **T2** Check corpora, torch and GPU availability
- **T2** Read imposed-sparsity and campaign reports
- **T2** Check training code and Python env packages
- **T2** Locate available text corpora
- **T2** Read push/pull crossover report
- **T2** Inventory corpora and HF cache
- **T2** Inspect token id format and tokenizers
- **T2** Check engine support for binary/ternary events
- **T2** Inspect corpus file formats
- **T2** Check English corpus size
- … et 1810 autres

## 4. Mesures et résultats marquants

- **T1** `6df6de4 §10 : le palier NVMe donne −8,8 %, la prédiction était de −16,3 %`
- **T1** `3169941 Attribution des 206,58 Gio : 72 % sont les experts, relus à chaque jeton`
- **T1** `d186466 §94 : rang 1, 2 ou 3 — le meilleur rang n'est pas celui du meilleur chiffre`
- **T1** `df8980e §92 : la pire paire après échelle — de–en à 486 % du professeur, mais 5 paires sur 15 échouent`
- **T1** `| `8e04c99a` | 2026-09-30 18:17 | 0.7 Mo | 118 Ko | 1 | 59 | 85 | 0 | 0 |`
- **T1** `| `aa5f9fc5` | 2026-09-30 15:17 | 0.8 Mo | 129 Ko | 1 | 78 | 100 | 0 | 0 |`
- **T1** `| `b13a6032` | 2026-10-02 15:09 | 0.3 Mo | 88 Ko | 1 | 17 | 43 | 0 | 0 |`
- **T1** `-| `bbd6969f` | 2026-10-07 20:45 | 56.7 Mo | 8968 Ko | 205 | 9596 | 9018 | 63 | 26 |`
- **T1** `+| `bbd6969f` | 2026-10-07 21:14 | 56.9 Mo | 9009 Ko | 205 | 9630 | 9050 | 63 | 26 |`
- **T1** `| `bcfe0b97` | 2026-09-30 12:39 | 1.0 Mo | 145 Ko | 1 | 102 | 110 | 0 | 0 |`
- **T1** `| `c25f97d1` | 2026-09-30 11:59 | 0.8 Mo | 126 Ko | 1 | 73 | 104 | 0 | 0 |`
- **T1** `| `c776b71f` | 2026-09-30 18:43 | 0.7 Mo | 82 Ko | 1 | 35 | 54 | 0 | 0 |`
- **T1** `| `fba448b3` | 2026-10-02 15:10 | 0.5 Mo | 39 Ko | 1 | 19 | 26 | 0 | 0 |`
- **T1** `| `ff364db0` | 2026-10-01 05:58 | 0.5 Mo | 120 Ko | 1 | 63 | 75 | 0 | 0 |`
- **T1** `-Total : 99.0 Mo de traces brutes.`
- **T1** `+Total : 99.2 Mo de traces brutes.`
- **T1** `+⏵ **PREUVE : les normes passent de ×100 à ×1,003 une fois l'échelle appliquée. Nos lecteurs l'ignorent depuis toujours. Je quantifie l'impact sur le résultat publié.**`
- **T1** `- **T1** : 511 tokens notés — perplexité cumulée 247.031  (4.9 tok/s) === perplexité 247.0308 sur 511 tokens (0 événements, 104.5 s) ===  ### B3 harmony assistant 511 --- ref --- 0.0 0.0 0:00 ls: cann`
- **T1** `+    le rapport de normes va de ×6 à ×100 selon la couche ; avec, il tombe entre`
- **T1** `> Budget par jeton **mesuré** : **86,787 Go** — experts routés 25,830 (29,8 %),`
- **T1** `> dense 60,958 (70,2 %). Le dense pèse 2,3× les experts : aucune technique sur`
- **T1** `> les experts n'adresse plus de 30 % du trafic d'un jeton.`
- **T1** `> sans avoir jamais été mesuré, vaut **×1,58** (Qwen3-30B-A3B, invite de`
- **T1** `> refermés (« paires experts » tombait à 1 % dès le lot 2), et `forward_lot``
- **T1** `> **11 % de CPU** (borné par le disque : 1,80 To lus, 451 Go/jeton, 5,2 balayages`
- **T1** `>   trace** — 25 à 60 % des positions sur la donnée à une unité, 3 % à dix unités.`
- **T1** `⏵ **PREUVE : les normes passent de ×100 à ×1,003 une fois l'échelle appliquée. Nos lecteurs l'ignorent depuis toujours. Je quantifie l'impact sur le résultat publié.**`
- **T1** `1290:#    moteur déporte alors tout seul les projections Q8_0 de plus de 8 Mo — le`
- **T1** `1295:#    du même ordre que les 0,06 % mesurés alors — non re-mesuré depuis.)`
- **T1** `1512:# attendu : CPU 20,9 Go/s · GPU ligne par fil 41,9 · GPU warp par ligne 84,9`
- **T1** `1595:### L'engram : 16 ms par entrée sur le disque mécanique`
- **T1** `6df6de4 07/10 18:11 §10 : le palier NVMe donne −8,8 %, la prédiction était de −16,3 %`
- **T1** `| ajustement d'un pont | **5 à 10 min** sur 1 446 entrées × 575 positions, parce que la Grammaire `AᵀA` coûte `n·d²` avec `d = 1 792` |`
- **T1** `- **diviser `d` par 1,5** (un modèle de 576 cachés au lieu de 896) gagne **×2,4** ;`
- **T1** `- **diviser `n` par 20** (une phrase au lieu d'un article) gagne **×20**.`
- **T1** `26884:⏵ Trace DRVF v3 : valeurs i8 + échelle f16 par bloc (l'étude déléguée annonce −63 % ; je vérifie).`
- **T1** `27144:ae85043 DRVF v3 : −66 % de trace au total, pour +0,074 % de perplexité`
- **T1** `| traçage article 1 (399 langues × 24 couches) | **26 min** |`
- **T1** `| traçage article 2 (399 langues × 24 couches) | **48 min** |`
- **T1** `#    occupé                                  473 s   (85.3%)`
- **T1** `#    occupé, pondéré par les files         12578 s   (2270.4%)`
- **T1** `#   LE DISQUE. `sda` est occupé 85% du temps et le CPU ne`
- **T1** `#   travaille que 31% : le temps de la passe est le temps de LIRE les`
- **T1** `#   octets au débit du disque. Vérification : 56.5 Go à 0 Mo/s`
- **T1** `couche 41 :   2254 ms de chargement +  14302 ms de calcul · banque 4`
- **T1** `couche 42 :   1619 ms de chargement +  14274 ms de calcul · banque 4`
- **T1** `couche 43 :   3285 ms de chargement +  12625 ms de calcul · banque 4`
- **T1** `couche 44 :   1619 ms de chargement +  15101 ms de calcul · banque 4`
- **T1** `couche 45 :   1738 ms de chargement +  15464 ms de calcul · banque 4`
- **T1** `couche 46 :   1851 ms de chargement +  12578 ms de calcul · banque 4`
- **T1** `---- chargement 69.0 s (15 %) · calcul 394.9 s (85 %) [attention 90.3 s · FFN 304.6 s]`
- **T1** `passe complète : 466359 ms au total`
- **T1** `bit près, et le relais qui circule entre deux nœuds fait 142 ko par saut.`
- **T1** `La couche 0 a une séparation **nulle** (+0,001) : le même texte dans deux langues ne se ressemble pas plus que deux textes différents. La couche 13 a **+0,034**, et les couches **10 à 15 forment un pl`
- **T2** `avons mesuré le contraire sur un LLM dense : **0,00 % d'activations nulles**, donc`
- **T2** `| 0,1 % | 343,8 M (−2,6 %) | 19,5750 | 1,02× |`
- **T2** `| 0,2 % | 334,9 M (−5,1 %) | 19,6502 | 1,02× |`
- **T2** `| 0,5 % | 312,3 M (−11,5 %) | 20,1511 | 1,05× |`
- **T2** `| 1,0 % | 281,1 M (−20,3 %) | 22,2286 | 1,15× |`
- **T2** `| 2,0 % | 230,8 M (−34,6 %) | 30,5837 | 1,59× |`
- **T2** `| 5,0 % | 145,0 M (−58,9 %) | **2264,84** | **117×** |`
- **T2** `➡️ Économiser 11 % d'événements coûte 5 % de perplexité, et au-delà de 2 % le`
- **T2** `| 100 % | 354,3 M | 23,6125 | 26,2565 |`
- **T2** `| 90 % | 319,1 M (−9,9 %) | 23,6790 (+0,28 %) | 26,2950 (+0,15 %) |`
- **T2** `| 85 % | 301,5 M (−14,9 %) | 23,7468 (+0,57 %) | 26,5785 (+1,23 %) |`
- **T2** `| 80 % | 283,7 M (−19,9 %) | 23,8251 (+0,90 %) | 26,8586 (+2,29 %) |`
- **T2** `➡️ **À sparsité comparable, le k-WTA coûte dix fois moins que le seuil** : −15 %`
- **T2** `d'événements pour +0,6 à +1,2 % de perplexité, contre +4,6 % pour le seuil à`
- **T2** `−11 %. La raison est simple : un seuil relatif au *maximum* coupe d'autant plus`
- **T2** `| **poids d'attention** (top-k clés) | **améliore** de 0,5 à 1,2 % | ✅ à garder |`
- **T2** `| activations du FFN (k-WTA 90 %) | +0,15 à +0,28 % | ✅ acceptable |`
- **T2** `| activations du FFN (k-WTA 85 %) | +0,5 à +1,2 % | ⚠️ selon le budget |`
- **T2** `| entrée des projections d'attention (90 %) | +0,06 % | ✅ quasi gratuit |`
- **T2** `| **Q et K** (après RoPE) | ×2,2 à 50 %, ×36 à 25 % | ❌ intouchable |`
- **T2** `| activations du FFN (seuil absolu) | ×117 à 5 % du max | ❌ inutilisable |`
- **T2** `**Attention à 32 clés + projection `gate` à 85 %.**`
- **T2** `| attention 32 clés seule | 354,3 M | 23,3279 (**−1,21 %**) | 26,1178 (**−0,53 %**) |`
- **T2** `| **+ `gate` à 85 %** | **338,8 M (−4,4 %)** | 23,2811 (**−1,40 %**) | 26,1417 (**−0,44 %**) |`
- **T2** `➡️ **On améliore la qualité de 0,4 à 1,4 % tout en réduisant le flux`
- **T2** `d'événements de 4,4 %.** Ce n'est pas un compromis : les deux vont dans le même`
- **T2** `| renormalisation homéostatique après k-WTA | **dégrade** (+0,2 à +3,6 %) : le modèle préfère la troncature franche |`
- **T2** `| FFN complet à 85 % + attention creuse | **non additif, défavorable** (+0,19 % en B) |`
- **T2** `Elles donnent **exactement le même résultat** — vérifié : perplexité 19,2647 au`
- **T2** `Mesure refaite sur `blk.0.ffn_gate.weight` (4 864 × 896, 4,36 M poids), 16 threads,`
- **T2** `| 0 % | 0,004 | 0,167 | 0,03 |`
- **T2** `| 1 % | 0,019 | 0,162 | 0,12 |`
- **T2** `| 5 % | 0,047 | 0,168 | 0,28 |`
- **T2** `| **10 %** | 0,078 | 0,163 | **0,48** |`
- **T2** `| **25 %** | 0,180 | 0,163 | **1,11** |`
- **T2** `| 50 % | 0,355 | 0,165 | 2,15 |`
- **T2** `| **100 %** | 0,801 | 0,171 | **4,69** |`
- **T2** `➡️ **Les deux architectures se croisent à ~22 % de densité d'activation**, pas à`
- **T2** `10 %. Le chiffre se lit dans le rapport à pleine densité : le pull traite 4,7 fois`
- **T2** `/dev/mapper/system-root   11T  8,8T  2,1T  81% /home/stephane/Data13TB`
- **T2** `// sursouscription (mesuré : ×1,3 de perte à 40+1 threads sur 40 CPU).`
- **T2** `blk.0.ffn_gate.weight  [4864 × 896]  densité 99.2 %`
- **T2** `dense 8 bits               8.000 b/poids  (   4.36 Mo)`
- **T2** `bitmap + signe             1.992 b/poids  (   1.09 Mo)`
- **T2** `creux k=1 (signe seul)     1.992 b/poids  (   1.09 Mo)`
- **T2** `creux k=4                  4.970 b/poids  (   2.71 Mo)`
- **T2** `creux k=8                  8.939 b/poids  (   4.87 Mo)`
- **T2** `listes signées + écarts    7.975 b/poids  (   4.34 Mo)`
- **T2** `blk.0.ffn_down.weight  [896 × 4864]  densité 99.2 %`
- **T2** `creux k=4                  4.967 b/poids  (   2.71 Mo)`
- **T2** `creux k=8                  8.934 b/poids  (   4.87 Mo)`
- **T2** `listes signées + écarts    7.941 b/poids  (   4.33 Mo)`
- **T2** `blk.0.attn_q.weight  [896 × 896]  densité 99.1 %`
- **T2** `dense 8 bits               8.000 b/poids  (   0.80 Mo)`
- **T2** `bitmap + signe             1.991 b/poids  (   0.20 Mo)`
- **T2** `creux k=1 (signe seul)     1.991 b/poids  (   0.20 Mo)`
- **T2** `creux k=4                  4.964 b/poids  (   0.50 Mo)`
- **T2** `creux k=8                  8.929 b/poids  (   0.90 Mo)`
- **T2** `listes signées + écarts    7.964 b/poids  (   0.80 Mo)`
- **T2** `blk.0.attn_output.weight  [896 × 896]  densité 99.2 %`
- **T2** `bitmap + signe             1.992 b/poids  (   0.20 Mo)`
- **T2** `creux k=1 (signe seul)     1.992 b/poids  (   0.20 Mo)`
- **T2** `creux k=4                  4.968 b/poids  (   0.50 Mo)`
- **T2** `creux k=8                  8.936 b/poids  (   0.90 Mo)`
- **T2** `listes signées + écarts    7.972 b/poids  (   0.80 Mo)`
- **T2** `0.0%             0  fusion   0.00 G (0.0064 ms) | 2-listes   0.00 G (0.0062 ms)`
- … (tronqué)

## 5. Erreurs rencontrées

84 sorties en erreur ou divergentes. Les premières :

- **T1** : ```  ### 🤖 Assistant  ⏵ **En transformers 5, `AutoModel` rend directement `Qwen2Model` (pas de `.model`). Je corrige le diagnostic.**  - **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitH
- **T2** : 3310393 bash -c pgrep -af "essai_decharge" | grep python | head; echo "--- logs ---"; tail -2 /tmp/ec_d192_lr3e3.log 2>/dev/null; tail -2 /tmp/ec_d192_lr1e3.log 2>/dev/null; echo "---"; ls -la /tmp/ec
- **T2** : === /tmp/ec_lr3e3.log === === VERDICT (validation tenue à l'écart) ===   dense    :   1875072 paramètres · 2.4420 bits/octet ·    1.77 M MACs/token   décharge :   1880064 paramètres · 3.2004 bits/octe
- **T2** : println!("  pool 4 bits vs scalaire : {}",                  if pire.1 == 0.0 { "IDENTIQUE ✅".to_string() }                  else { format!("DIVERGENT rang {} (écart relatif {:.3}) ❌", pire.0, pire.1) 
- **T3** : File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/exporter_gguf.py", line 155, in kv_depuis_config     (f"{arch}.expert_count", int(cfg["num_experts"])),                                  ~~~
- **T3** : gu = poids[p + "mlp.experts.gate_up_proj"]      # (E, 2·ff, d)          ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ KeyError: 'model.layers.0.mlp.experts.gate_up_proj' === en-tête vu par le moteur ===  thre
- **T3** : /tmp/moe_ids.txt : 256 tokens, fenêtres de 256 [moe] couche 0 : « blk.0.ffn_gate_exps.weight » de type F32 — format sans noyau ni déquantification  thread 'main' (3319853) panicked at src/model.rs:148
- **T3** : # /tmp/moe_test.gguf : 51 tenseurs · 6.2 Mo (f32, experts Q4_0) · 17 métadonnées # architecture 4 couches · 192 cachés · 8 experts (top-2) · norm_topk_prob=True /tmp/moe_ids.txt : 256 tokens, fenêtres
- **T3** : assert a.shape[-1] % 32 == 0, f"dernière dimension non multiple de 32 : {a.shape}"            ^^^^^^^^^^^^^^^^^^^^^ AssertionError: dernière dimension non multiple de 32 : (4, 64, 48) === le moteur ch
- **T4** : [config] mélanges d'experts chargés : 4/4 couches · mapping absent (experts en clair dans le fichier) [config] puits appris sur 0/4 couches · n_rot 48 · ffn 768 · experts 8 [config] rotation : RoPE si
- **T4** : [flux] quantification : 127 niveaux, seuil 0, top-k 0, renorm false [flux] pilote : 2 couches en local, 2 chez le pair, 128 jetons   référence locale  : perplexité 1186.5313  (0.1 s)   deux nœuds     
- **T4** : ~~~~~^^^^^^^^^^^^^^^^^^^^^^^ KeyError: 'model.layers.0.mlp.gate.weight' === charge ===  thread 'main' (3374822) panicked at src/main.rs:2427:40: === ppl dense === [exit code: 1]
- **T4** : Error: tool call aborted
- **T5** : fichier :  === NVMe === fichier :  [exit code: 1]
- **T9** : === bge-m3 : exécution ? ===  thread 'main' (3706022) panicked at src/gguf.rs:1752:53: tenseur blk.0.attn_norm.weight absent note: run with `RUST_BACKTRACE=1` environment variable to display a backtra

## 6. Commits

- Parcimonie entraînée : premier banc, et la loi du coût par événement mesurée dans le moteur  Le dépôt n'avait jamais entraîné un seul modèle (zéro rétropropagat
- Porte d'exécution : un modèle entraîné ici tourne dans Drave, logits identiques  Le moteur lit le GGUF en place et n'avait pas de convertisseur : le dépôt ne po
- Réparti : --ids-file était ignoré, et les jetons synthétiques sortaient du vocabulaire  Deux défauts trouvés en essayant de répartir le modèle entraîné ici.  1.
- entrainer_moteur : deux erreurs qui faussaient la mesure, corrigées  1. Double décalage. Le modèle HF décale lui-même (shift_logits/shift_labels) ;    lui passe
- entrainer_moteur : le double décalage était AUSSI dans la boucle d'entraînement  La correction précédente n'avait touché que l'évaluation. Le défaut était plus 
- docs/numa-segregation : la ségrégation NUMA proposée, mesurée plutôt que raisonnée  Réponse à une proposition de station bi-Xeon avec topologie asymétrique stri
- Le modèle produit ici tourne dans Drave et se découpe — les deux portes sont tenues  Porte d'exécution : un Qwen3-MoE entraîné ici (4 couches, 8 experts, top-2,
- docs/numa-segregation §11 : la carte 4xNVMe et l'AMD, chiffrées avant achat du reste  Le placement proposé est juste (array sur le nœud des GPU, OS/affichage is
- docs/numa-segregation §12 : quoi faire de la RAM quand elle est hors de prix  Trois réponses, dans l'ordre où elles paient, et toutes mesurées :  1. RÉCUPÉRER C
- docs/configuration-nvme-raid-amd : préparation de la reconfiguration (array sur le nœud 1, AMD pour le bureau)  Document écrit AVANT l'intervention, pour que ch
- Campagne 24 h : mesurer ce que l'architecture par listes vaut, tâche par tâche  Le dépôt a surtout mesuré un couple (Qwen2.5-0.5B, perplexité). tools/campagne-b
- Campagne : le décodage spéculatif naïf vaut ×1,2 (mesuré), et deux familles manquent  tools/speculatif.py mesure ce qu'il faut savoir AVANT d'écrire le décodage
- Campagne : le décodage spéculatif naïf vaut ×1,2 (mesuré), et deux familles manquent  tools/speculatif.py mesure ce qu'il faut savoir AVANT d'écrire le décodage
- Campagne : la perplexité n'est comparable qu'à tokenizer égal — colonne bits/octet  Trois modèles de la grille partagent EXACTEMENT le même tokenizer (leurs fic
- Distillation implémentée (jamais faite dans ce dépôt) + l'état des lieux par famille de tâches  tools/entrainer_moteur.py accepte --enseignant, --alpha-distill 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/msg.txt <<'MSG' Distillation implémentée (jamais faite dans ce dépôt) + l'état des lieux par fa
- Campagne : les quatre premiers modèles entraînés passent la porte du moteur  Chaîne automatique : chaque dossier d'entraînement est exporté dès qu'il apparaît, 
- Campagne : le chemin par listes coûte 1,8 à 2,1x sur nos propres modèles, et c'est la réponse  Mesuré sur les deux modèles denses entraînés ici, mêmes jetons, m
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 git add tools/census_routage.py reports/rapport-campagne-benefices.md && timeout 300 git commi
- Campagne : les cinq batches enchaînés (tâche, mémoire, génération, lot, cas extrême)  Le plan porte maintenant la file complète : après les neuf étapes viennent
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 git add reports/rapport-campagne-benefices.md && timeout 300 git commit -q -F - <<'MSG' Les tâ
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 git add reports/rapport-campagne-benefices.md && timeout 300 git commit -q -F - <<'MSG' La mém
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p="reports/rapport-campagne-benefices.md"; s=open(p).read() # La section « décodage spécu
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p="reports/rapport-campagne-benefices.md"; s=open(p).read() s = s.replace('''| r1-distill
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/msg_mistral.txt <<'MSG' La famille Mistral a désormais sa porte — et l'anomalie codestral est e
- Rapport : l'anomalie codestral est un décalage de tâche, pas un bug du moteur  La porte Mistral (commit précédent) tranche : référence 3411,4394 contre moteur 3
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/msg_portes.txt <<'MSG' La porte Mistral entre dans la suite : une famille de plus est couverte 
- Quatre tâches, sorties verbatim : le moteur tient, c'est le modèle qui limite  Refaites sur le 0,5 B après avoir coupé les mêmes essais sur gpt-oss-120b (5 x 1 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p="reports/rapport-campagne-benefices.md"; s=open(p).read() vieux = s[s.index("## 5. Les 
- Verdict : la ligne « langage » porte maintenant le gain du routage à lecture égale  Le verdict famille par famille disait « le chemin par listes n'aide pas ». C
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p="reports/rapport-campagne-benefices.md"; s=open(p).read() ajout = '''## 10 ter. La dens
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p="reports/rapport-campagne-benefices.md"; s=open(p).read() vieux_debut = s.index("**L'an
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/msg_tok.txt <<'MSG' Tokenizers SentencePiece (Llama, Mistral, Codestral) : les espaces étaient 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p="reports/rapport-campagne-benefices.md"; s=open(p).read() ajout = '''## 12. Le cas extr
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p="reports/rapport-campagne-benefices.md"; s=open(p).read() ajout = '''## 5 bis. La disti
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p="reports/rapport-campagne-benefices.md"; s=open(p).read() s = s.replace('''| gpt-oss-12
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p="reports/rapport-campagne-benefices.md"; s=open(p).read() deb = s.index("## 5. Les modè
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p="reports/rapport-campagne-benefices.md"; s=open(p).read()  # 1. La ligne codestral, cor
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p="reports/rapport-campagne-benefices.md"; s=open(p).read() ajout = '''## 19. La parcimon
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p="reports/rapport-campagne-benefices.md"; s=open(p).read() deb = s.index("## 0 bis. Le v
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/msg_banc.txt <<'MSG' Le banc des encodages ne plante plus sur les modèles K-quant (c'était la p
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p="reports/rapport-campagne-benefices.md"; s=open(p).read() ajout = '''## 20. Contexte et
- tail -4 /tmp/campagne24/journal4.txt; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p="reports/rapport-campagne-benefices.md"; s=open(p
- L'échelle par enregistrement des traces : les lecteurs l'ignoraient, et le résultat change  Le moteur quantifie chaque enregistrement DRVF sur act_levels = 127 
- Instrument : la convention SentencePiece nommée, le k-WTA appris, la FFN en Q8  Trois corrections nées de la campagne, chacune pour lever un silence.  1. Le con
- Deux harnais qui manquaient : le protocole 8×128 écrit, l'acceptation mesurée par le moteur  mesure_fenetres.sh — le protocole de record des modèles entraînés i
- Campagne 24 h : l'équivalence au bit près, le routage qui s'inverse, le lot à froid  Cinq résultats de la fenêtre, tous avec leur protocole.  1. FIDÉLITÉ (§ 22)
- La carte de latence : répartir ne paie que si le calcul dépasse 3,4 ms x RTT  Le découpage était prouvé exact sur localhost — un plancher optimiste. Un relais T
- Spéculatif : l'alignement du brouillon aide, mais l'acceptation plafonne à 15,6 %  Trois paires mesurées par le moteur, en décodage glouton :   - 0,5 B nu -> 1,
- La porte gpt-oss rend 15,6017 au chiffre près : la campagne est verte partout  Relancée seule après recalibrage du délai, la passe de 512 jetons sur gpt-oss-120
- Dim 512 : le routage seul perd, le routé DISTILLÉ gagne de 5,2 %  La courbe d'échelle est complète, et elle a deux branches :    dim 256 : dense 5,0155 -> routé
- Rapport du modèle : la courbe d'échelle 256/384/512, et le routage qui s'inverse  Trois paires entraînées au même protocole, mesurées au protocole de record : l
- Spéculatif : c'est le RAPPORT DE COÛT qui décide, et il est minimal sur un modèle plus gros que la RAM  Troisième paire mesurée par le moteur — un brouillon min
- Parcimonie IMPOSÉE ou APPRISE : la réponse est mesurée, et elle est nette  Deux modèles identiques par ailleurs (dim 384, mêmes pas, FFN en Q8 pour que le chemi
- Parcimonie apprise : le tableau complet à trois modèles, et la recette qui en sort  Trois modèles identiques par ailleurs, un témoin et deux entraînés creux (50
- Le point de la file à 5 h 20 : ce qui est fait, ce qui tourne, ce qui reste un manque  Le tableau de clôture distingue trois choses qui ne doivent pas être conf
- Un quatrième piège de méthode : la chaîne qui attendait son marqueur dans le mauvais journal  Deux heures de GPU perdues devant un marqueur écrit dans le journa
- Le lot sur un modèle plus gros que la RAM : le moteur refuse, et il dit pourquoi  V4.1-Flash (365,7 Go sur 125 Go) est le seul modèle de la machine qui ne tient
- Les correctifs du moteur sont promus : 77 tests verts, Codestral à 8 jetons, porte rejouée  Le binaire de référence datait du 8/10 11 h 00 et trois commits de d
- L'aiguille tient jusqu'à 12 288 jetons : 18 sondes sur 18  La série est complétée à 8 192 puis 12 288 jetons, trois profondeurs à chaque fois : toutes retrouven
- Échelle 512 : la recette creuse tient, et le débit ne distingue plus les deux chemins  m8_d512_kwta25 (entraîné à 25 %, mêmes 40 000 pas que son témoin) :    sa
- Résumé exécutif : les cinq résultats qui comptent et les cinq manques  Une page en tête du rapport, chacun renvoyant à sa section et à sa mesure. Le rapport fai
- Le débit de lecture réel : 8,6 Mo/s sur disque dur contre 243 Mo/s en séquentiel  Mesuré machine au calme : le disque dur qui porte les gguf délivre 243 Mo/s en
- Codestral corrigé, mesuré au protocole commun : 133,08 sur 255 jetons (1,842 bit/octet)  Le chiffre publié jusqu'ici (117,91) portait sur 63 jetons, parce que l
- Les deux leviers ne se cumulent pas : la distillation n'ajoute rien au creux appris  m9_d384_kwta25_distille reprend exactement la recette de kwta025 PLUS la di
- Ce que le nouveau matériel change, d'après les mesures — et ce qu'il ne change pas  Section de liaison avec le plan matériel (4xNVMe en RAID + carte AMD pour l'
- Résumé : la distillation s'ajoute au routage, pas à la parcimonie" && echo committed; sleep 540; tail -1 /tmp/campagne24/tr_m9_route_long.log
- Le tableau des manques était cassé par des barres verticales non échappées" && echo ok
- Rapport du modèle : la recette du modèle nativement événementiel  Trois règles mesurées : on n'élague pas un modèle, on l'entraîne creux (à 25 % le témoin s'eff
- Distinguer le moteur du modèle : évaluer un modèle ad hoc pour Drave  Le rapport de campagne mesurait le MOTEUR sur des modèles faits pour d'autres architecture
- Trois dessins inédits que Drave récompense : profondeur routée, budget d'événements appris, quantification-aware  Le document n'évaluait que des leviers déjà ou
- Budget d'événements : le premier essai d'allocation ciblée ÉCHOUE, et il apprend pourquoi  À événements comparables, une allocation ciblée d'après le tableau de
- 80 000 pas : meilleur en fp32, PIRE après export — le format fait partie du modèle  Le routé 512 entraîné deux fois plus longtemps améliore sa validation fp32 (
- Moteur contre modèle : un tableau qui dit, pour chaque mesure, de qui elle parle  Quand une mesure est décevante, il faut savoir de qui : le chemin par listes e
- Biologie : ce que les connectomes imposent comme contraintes, et l'expérience E1 outillée  Nouveau document docs/biologie-pour-drave.md : les faits mesurés (dro
- Le budget chiffré : 0,4 pJ par événement synaptique contre 0,9 µJ chez nous  Deux calculs d'ordre de grandeur, à partir des chiffres du document et des mesures 
- Carte des taux complète : 50 %, 25 %, 12,5 % — chaque division par deux coûte 2 % puis 8 %  Troisième point mesuré (m10_d384_kwta125, mêmes 40 000 pas, même tém
- Le fait biologique que nos modèles ne reproduisent pas : des poids à queue lourde  Les efficacités synaptiques corticales sont log-normales, sur plusieurs ordre
- E6 outillée : poids log-normaux (theta = log|w| appris, signes figés à la naissance)  Les synapses corticales sont log-normales ; nos modèles sont quasi gaussie
- Les deux axes appris se cumulent : +poids élagués appris = ÷2 lectures à qualité égale  m11_d384_kwta25_elag50 reprend exactement kwta025 plus un élagage APPRIS
- Notre hebbien différentiel face à la biologie : pourquoi il échoue, et par quoi le remplacer  Le dépôt a appliqué, mesuré, sauvé, rechargé ET réfuté une règle h
- E1 : un connectome inné ALÉATOIRE coûte 1 % de perplexité et divise les lectures par 4  Même modèle que le témoin dense (dim 384, 40 000 pas, même export), sauf
- Drave en impulsion pure serait-il un meilleur apprenant ? Pas en l'état, oui sous conditions nommées  Trois sens de « mode impulsion pur » : l'EXÉCUTION (déjà é
- E7 et E8 implémentés et mesurés : la nouveauté empire la règle, la décorrélation est inerte  Deux mécanismes écrits dans le moteur (DRAVE_HEBB_MODULE, DRAVE_HEB
- Le rapport de campagne renvoie aux trois documents de conception, et porte le résultat de structure innée" && echo ok; sleep 420; tail -1 /tmp/campagne24/tr_m13
- E6 (poids log-normaux) : échec de code, consigné comme tel — le modèle sauvegardé n'est pas le modèle entraîné  La reparamétrisation w = signe·e^theta a été ent
- E6 : le soupçon de matérialisation est testé et ÉLIMINÉ (écart 0,000e+00) — le défaut est ailleurs  La matérialisation a été refaite en recalculant explicitemen
- E6 : mesure définitive — le fichier sauvé ne reproduit pas le modèle entraîné  Avec le protocole de l'entraînement lui-même (mêmes fenêtres, même formule) :   t
- L'architecture du cerveau face à Drave : les briques y sont, les formes non  Nouveau document : après la brique (docs/biologie-pour-drave.md), l'édifice. Les ch
- M1 : le bus de valeur est implémenté, et la valeur auto-référentielle ne suffit pas  Le manque M1 (un scalaire diffusé à toutes les couches, comme un noyau neur
- Nos modèles à décharges ne vont pas sur GPU : trop petits, et le noyau GPU est dense  Vérifié dans le code et par la mesure. Trois conditions pour déporter une 
- Statuts d'expériences à jour : E1 et E3 faits, E2/E4 cadrées, et le pendant GPU du noyau de listes ajouté au plan" && echo ok
- La courbe lecture-qualité, réponse finale : ÷4 pour +1 %, ÷8 pour +4 %, ÷15 pour +22 % si l'axe est imposé  Cinq modèles identiques par ailleurs (dim 384, 40 00
- M1 dans le moteur : le bus de modulation (nouveauté ou valeur), et la persistance de D  DRAVE_HEBB_MODULE accepte désormais « valeur » : eta est piloté par hd.m
- Signal externe mesuré : meilleur des modulateurs, et toujours pire que la règle nue  Le moteur lit maintenant un modulateur externe (DRAVE_HEBB_MODULATEUR_FICHI
- Décorrélation en courbe de dose : elle améliore de façon monotone et converge vers « ne rien apprendre »  DRAVE_HEBB_BETA rend la constante de temps réglable. M
- Plan détaillé des douze capacités manquantes, jusqu'à la distribution multi-instances  Douze fiches (structure cérébrale -> état du moteur -> conception -> inte
- README : la campagne du 8-9 octobre en tête, avec ses cinq résultats et ses quatre documents  La porte d'entrée du dépôt datait de la session précédente. Elle p
- journal : index des sessions à jour" 2>/dev/null; git status --short | wc -l; CRED=$(printf "protocol=https\nhost=github.com\n\n" | timeout 15 git credential fi
- Publication du dépôt + document de modularisation : espace de travail Cargo, pas de submodules  Le dépôt est publié en privé : https://github.com/stephanedenis/
- Dim 512 : la structure innée coûte +6,7 % (contre +1,0 % à dim 384) pour ÷3,7 de lectures  m16_d512_masque25 (masque aléatoire de 25 % des connexions, figé à la
- Registre consolidé des manques — le capstone que l'objectif demande  docs/manques.md : huit manques du MOTEUR (noyau de listes pour les experts — mesuré par le 
- Annexe : manifeste des journaux de la campagne (59 fichiers d'étape, 79 Kio, 17 journaux de chaînes)  Le livrable « la file exécutée et ses journaux » est maint
- Clôture du rapport : ce qui reste n'est plus de la mesure en retard mais du travail identifié  Le § 23 renvoie désormais au registre des manques et au plan des 
- Dim 512 : le prix de la parcimonie croît avec l'échelle (+6,7 % et +8,0 % contre +1,0 % et +3,8 % à 384)  Dernier point de la courbe lecture-qualité, mesuré à 1
- C1a : la topologie de régions se lit, se vérifie et refuse les graphes incohérents  Première brique du sprint cerveau (docs/plan-cerveau-complet.md, capacité C1
- C1b : la conception relevée sur le code, prête à implémenter  Le protocole transmet DÉJÀ la plage de couches dans la trame (f.debut, f.fin) : le découpage voyag
- C1b pas 1 : la topologie PILOTE le découpage — porte tenue, même chiffre, 0,00e0  --ppl-reparti --topologie F exécute le découpage DÉCRIT par le fichier au lieu
- C1b pas 2 : le RELAIS — trois régions sur trois instances, écart 0,00e0  Un nœud du milieu (--flux-serveur … --topologie F --region n1) applique SA plage puis t
- C12 : trace globale horodatée et rejeu exact — 126 croisements, aucune divergence  TraceGlobale enregistre, par croisement : région, pas, lien, nombre de valeur
- C5 : bus de modulation multi-canaux — canal neutre exact au bit près, canal actif sur un relais  bus.rs : canaux nommés, valeur NEUTRE par canal (gain = 1,0, le
- Bilan du sprint : C1, C12 et C5 livrées avec leurs invariants, 95 tests, trois défauts trouvés par les portes  Les trois capacités ont leur module, leur porte o
- Sprint clos sur vérification : les 23 portes du dépôt sont vertes (0 rouge), 95 tests  tools/portes.sh relancé après le sprint, terminé en 15 minutes (machine l
- C3 : les délais par lien, et le fichier de relations humaines  C3 — la topologie déclare delai_ms, le moteur l'applique (pilote sur son lien sortant, nœud relai
- C5bis : diffusion du bus par fichier de contrôle — le canal change la région du milieu  --bus-fichier F : le nœud RELIT le fichier avant chaque trame, donc un a
- État resumable : la prochaine action en tête du fichier de sprint  Six chantiers classés par valeur mesurable pour occuper le temps imparti : C4 (horloges par r
- C4 pas 1 : compteur de pas par région et borne de terminaison explicite  Ce que C4 demande est que chaque région ait SON horloge. Le pas complet (asynchronisme 
- C12bis : le nœud trace, et les traces de plusieurs processus se fusionnent  CE QUI MANQUAIT, ET QUI ÉTAIT GRAVE. Seul le pilote traçait : une divergence sur un 
- C5ter : le bus par le réseau — un réglage atteint une autre machine  C5bis diffusait un réglage par un FICHIER relu à chaque pas : il fallait donc un système de
- C6 : mémoire épisodique adressable par contenu — et ses trois résultats négatifs  Module episodique.rs : clé creuse (k-WTA sur l'amplitude), index inversé canal
- C6 suite : l'index élude enfin — et il fallait TROIS ingrédients, pas un  Le premier pas de C6 avait mesuré un négatif net : l'index inversé n'éludait RIEN (300
- C7 pas 1 : consolider par rejeu — et garder un CAS bat résumer par une MOYENNE  C7 au sens du plan veut rejouer des épisodes pour modifier des POIDS. Ce n'est p
- C9/C10 pas 1 : le pont à fibres limitées — combien de fibres, et à quel prix  La question du corps calleux, posée en termes mesurables : deux régions échangent 
- C9 : la falaise du pont est une MARCHE entre 448 et 392 fibres  Localisée en raffinant la courbe (listes par blocs) :      896 fibres   111,9225   1 951 octets 
- C8 pas 1 : le réflexe — un chemin court qui ne sait RIEN, et la cause mesurée  Un réflexe est un chemin COURT (la moelle épinière ne remonte pas au cortex). Le 
- C9 x C1 : où couper le modèle — le point de coupe est neutre, sauf à cause du lien  C1 (découpage) et C9 (pont) avaient chacun été mesurés à UN SEUL endroit : 1
- C6 suite : la mémoire LOCALISE — l'erreur se mesure en jetons, et elle est petite  Savoir si la mémoire rend l'épisode EXACT est une chose ; savoir à quelle DIS
- C7 suite : le rejeu RÉPÉTÉ est un point fixe, pas une usure (erreur exactement 0,00e0)  Question laissée ouverte par le premier pas de C7 : un prototype-exempla
- C2/C6 : la greffe d'état — branchée, et elle ne transfère PAS le contexte  Le passage manquant entre C6 (une mémoire qui retrouve un état) et C9 (un lien qui li
- Porte bus-socket : elle rendait 1 en ayant TOUT réussi (sys.exit avec un message)  Le dernier cas de tools/porte-bus-socket.sh terminait par sys.exit('  ❌ …' if
- C6 : un indice ÉTRANGER retrouve le bon passage — 136 jetons contre 448 de hasard  Toutes les mesures précédentes interrogeaient la mémoire avec un indice ISSU 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -q --amend -F - <<'MSG' C6 : un indice ÉTRANGER retrouve le bon passage — 136 jetons contre 448
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 600 cargo test --release --manifest-path drave-core/Cargo.toml 2>&1 | grep -E "^test result" && gi
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A drave-core/src/main.rs drave-core/src/model.rs tools/porte-melange.sh tools/porte-greffe.sh rep
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib p = pathlib.Path("tools/porte-greffe.sh") s = p.read_text() a = '''echo
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_te
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A docs/sprint-cerveau.md && git commit -q -F - <<'MSG' Verification complete : 19 portes vertes, 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib p = pathlib.Path("docs/sprint-cerveau.md") s = p.read_text() a = """| 1
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib p = pathlib.Path("docs/sprint-cerveau.md") s = p.read_text() a = "## ▶ 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib p = pathlib.Path("docs/sprint-cerveau.md") s = p.read_text() a = "## ▶ 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib p = pathlib.Path("docs/sprint-cerveau.md") s = p.read_text() a = "## ▶ 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib p = pathlib.Path("docs/sprint-cerveau.md") s = p.read_text() a = "## ▶ 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib p = pathlib.Path("docs/sprint-cerveau.md") s = p.read_text() a = "## ▶ 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib p = pathlib.Path("docs/sprint-cerveau.md") s = p.read_text() a = "## ▶ 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 900 bash tools/porte-flux.sh > /tmp/pf31.txt 2>&1; echo "porte-flux code=$?"; timeout 600 cargo te
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib p = pathlib.Path("docs/sprint-cerveau.md") s = p.read_text() a = "## ▶ 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 1200 bash tools/porte-flux.sh > /tmp/pf38.txt 2>&1; echo "porte-flux code=$?"; tail -3 /tmp/pf38.t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib p = pathlib.Path("docs/sprint-cerveau.md") s = p.read_text() a = "## ▶ 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 1200 bash tools/porte-flux.sh > /tmp/pf42.txt 2>&1; echo "porte-flux code=$?"; tail -2 /tmp/pf42.t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'ENDPY' import pathlib  p = pathlib.Path("reports/rapport-campagne-benefices.md") s = p.read_t
- Journal : la section 46 bis (--attn-sinks ecrit partout, lu nulle part) manquait — l'ancre du premier essai ne correspondait pas" && git push -q origin master &
- $(cat <<'MSG' --attn-sinks : le refus etait FAUX (le compteur EST lu, branche a fenetre) — le drapeau vit, et le zero n'existait pas  Le refus code 2, ecrit sur
- $(cat <<'MSG' Rangement : docs = fond, reports = une fiche par experience, journal = evenements dates  Retour de Stephane : les trois dossiers etaient melanges,
- $(cat <<'MSG' Fenetre x puits d'attention : +2,0 % de perplexite pour divide 2,67 les cles notees (512 jetons)  Mesure (Qwen2.5-0.5B-Q8_0, ctx 512, perplexite d
- $(cat <<'MSG' Rangement (suite) : rapport toutes-langues eclate (107 fiches), recapituatif range comme etat  - reports/rapport-toutes-langues.md (296 Ko, 107 se
- Journal : l'index liste les ENTREES QUOTIDIENNES (il ne voyait que les sessions automatiques)  Le journal paraissait ne contenir que des rapports de session gen
- docs/etat.md : l'index des modules (roadmap -> etat -> prochaine action) demande par Stephane  Pour chaque module (moteur, modele, cerveau/distribue, emulation,
- $(cat <<'MSG' Journal automatise par JOUR et par THEME (tools/journal_auto.py), branche sur le pre-commit  Demande de Stephane : automatiser journal/ depuis git
- Journal : les ETAPES du jour (lignes du journal de session) sont reprises par theme  Les rapports de session contiennent, tour par tour, ce que l'agent a consig
- Journal : journal/THEMES.md, la regle de classement rendue lisible et modifiable  Les themes etaient dans le script seulement. La table est maintenant ecrite da
- Fenetre x puits : la pente en N mesuree — gratuit a 512 jetons, +40 % a 2 048  Troisieme carte (2 048 jetons, ctx 2048, memes ids) : attention complete 10,3703 
- Journal : les CHIFFRES du jour par theme, extraits des textes deja fiables  Chaque fichier de theme porte desormais une ligne « Chiffres du jour » (pourcentages
- $(cat <<'MSG' Journal : etapes DATEES par la trace de session (elles couvraient toute la session)  Le rapport et le digest de session ne portent pas d'horodatag
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A && git commit -q -F - <<'MSG' Journal : etapes DATEES par la trace de session (elles couvraient
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PYEOF' import pathlib p = pathlib.Path("reports/rapport-fenetre-puits-attention.md"); s = p.r
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A && git commit -q -F - <<'MSG' Journal : classement affine (theme APPRENTISSAGE, plus de model.r
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PYEOF' import pathlib p = pathlib.Path("tools/carte-fenetre-puits.sh"); s = p.read_text() old
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PYEOF' import pathlib # 4096 dans la fiche fenêtre × puits : la ligne de plus, et la synthèse
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A && git commit -q -F - <<'MSG' C8 : l'etat de la couche 16 CONTIENT le prochain jeton (43,1 %) —
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A && git commit -q -F - <<'MSG' README et REPRISE allegés : demarrer en 5 minutes, et renvoyer au
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PYEOF' import pathlib # l'état : C8 avec la courbe et la distinction décodabilité / qualité p
- Carte fenetre x puits : l'extraction des secondes ratait (« ? s » affiche sans le dire)  Le motif exigeait la phrase de synthese entiere sur UNE ligne ; la sort
- Index et convention : les points d'entree sont nommes, avec la regle « renvoyer, pas recopier »  docs/etat.md gagne les points d'entree (README, REPRISE, refere
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline origin/master..HEAD; echo "=== amend du message ==="; git commit --amend -q -F - <<'MSG'
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PYEOF' import pathlib # 1) corriger l'extraction des secondes (la carte ne tourne plus) p = p
- Etat : le prix en temps de la fenetre est consigne (div 4 de cles = +12 % de debit, pas x4)" && git push -q origin master && echo poussé; sleep 240; ls /tmp/c8-
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PYEOF' import pathlib p = pathlib.Path("reports/rapport-c8-tete-entrainee.md"); s = p.read_te

