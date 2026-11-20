# Session d67a9bb1 — Intérêt pour le FPGA maintenant

> **Journaux :** [le jour](../../2026-11-17/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `d67a9bb1-090e-4f69-baf2-a831c00aa275` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-17 09:50 |
| Durée | 77.0 h |
| Tours | 86 |
| Messages | 1384 |
| Appels d'outils | 1201 |
| Fichiers touchés | 44 |
| Commandes | 1051 |
| Sous-agents | 7 |
| Commits | 99 |
| Compactages de contexte | 2 |

## Objectifs déclarés

- **create** — Ajouter au format DRVM les variantes d'implémentation par bloc (`impl` + `contrat {version, tolerance}`), les faire exécuter par les deux moteurs (Rust `native.rs` et numpy `tools/drvm_infere.py`), exposer la provenance dans l'inspecteur et la trace, et livrer une porte `porte-n3-variante` qui prouv
… [260 caractères tronqués]
- **complete** — Ajouter au format DRVM les variantes d'implémentation par bloc (`impl` + `contrat {version, tolerance}`), les faire exécuter par les deux moteurs (Rust `native.rs` et numpy `tools/drvm_infere.py`), exposer la provenance dans l'inspecteur et la trace, et livrer une porte `porte-n3-variante` qui prouv
… [260 caractères tronqués]
- **create** — Rendre `graph.routes` vivant dans le manifeste DRVM : schéma minimal déterministe (route conditionnelle par position vers un profil de bloc `local_mixer`), validation et refus dans les deux lecteurs, exécution par le moteur Rust (les deux moteurs refusent ce qu'ils n'exécutent pas), provenance dans 
… [306 caractères tronqués]
- **complete** — Rendre `graph.routes` vivant dans le manifeste DRVM : schéma minimal déterministe (route conditionnelle par position vers un profil de bloc `local_mixer`), validation et refus dans les deux lecteurs, exécution par le moteur Rust (les deux moteurs refusent ce qu'ils n'exécutent pas), provenance dans 
… [306 caractères tronqués]
- **create** — Livrer `porte-n3-moteurs` : prouver que les deux moteurs du même manifeste DRVM (Rust `native.rs` et numpy `drvm_infere.py`) rendent les mêmes logits dans la tolérance déclarée, pour les profils `defaut` et `bloque`, avec les contrôles négatifs qui rendent le comparateur non vide (une différence rée
… [164 caractères tronqués]
- **complete** — Livrer `porte-n3-moteurs` : prouver que les deux moteurs du même manifeste DRVM (Rust `native.rs` et numpy `drvm_infere.py`) rendent les mêmes logits dans la tolérance déclarée, pour les profils `defaut` et `bloque`, avec les contrôles négatifs qui rendent le comparateur non vide (une différence rée
… [164 caractères tronqués]
- **create** — Ajouter le profil d'implémentation `court` (fenêtre d'attention divisée par 4) au format DRVM et au moteur Rust, prouver qu'il n'est PAS substituable (logits différents) et qu'il PAIE en temps sur une charge dominée par l'attention, mesurer son coût de qualité (perplexité) sur un modèle entraîné, re
… [221 caractères tronqués]
- **complete** — Ajouter le profil d'implémentation `court` (fenêtre d'attention divisée par 4) au format DRVM et au moteur Rust, prouver qu'il n'est PAS substituable (logits différents) et qu'il PAIE en temps sur une charge dominée par l'attention, mesurer son coût de qualité (perplexité) sur un modèle entraîné, re
… [221 caractères tronqués]
- **create** — De 00 h 30 à 16 h le 18/11, en charge de TOUS les chantiers, machine dédiée : (1) épingler le corpus natif (sha256, manifeste, fiche) et lancer l'entraînement 100 M sur GPU avec bancs aux checkpoints ; (2) mesurer la grammaticalité du 100 M ; (3) instruire A2.6 (experts et tête) ; (4) exécuter les l
… [191 caractères tronqués]
- **complete** — De 00 h 30 à 16 h le 18/11, en charge de TOUS les chantiers, machine dédiée : (1) épingler le corpus natif (sha256, manifeste, fiche) et lancer l'entraînement 100 M sur GPU avec bancs aux checkpoints ; (2) mesurer la grammaticalité du 100 M ; (3) instruire A2.6 (experts et tête) ; (4) exécuter les l
… [191 caractères tronqués]
- **create** — De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits au strict minimum) et ressources locales à fond : (1) réparer le chargeur de corpus (mémoire bornée) et promouvoir le corpus v2 dédupliqué (6,90 Go) dans data/ avec son épingle ; (2) lancer le palier 1 — un
… [253 caractères tronqués]
- **complete** — De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits au strict minimum) et ressources locales à fond : (1) réparer le chargeur de corpus (mémoire bornée) et promouvoir le corpus v2 dédupliqué (6,90 Go) dans data/ avec son épingle ; (2) lancer le palier 1 — un
… [253 caractères tronqués]
- **create** — Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val tiers disjoint (wikitext2 français) pour trancher v1/v2 sans le biais de distribution ; (2) brancher la règle A2.6 dans model.rs en opt-in (coût experts, refus nommé, trace), avec les portes flux/pont/coupe
… [116 caractères tronqués]
- **complete** — Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val tiers disjoint (wikitext2 français) pour trancher v1/v2 sans le biais de distribution ; (2) brancher la règle A2.6 dans model.rs en opt-in (coût experts, refus nommé, trace), avec les portes flux/pont/coupe
… [116 caractères tronqués]
- **create** — D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec l
… [65 caractères tronqués]
- **complete** — D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec l
… [65 caractères tronqués]
- **create** — De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec é
… [217 caractères tronqués]
- **complete** — De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec é
… [217 caractères tronqués]
- **create** — De 08 h 30 à 16 h le 20/11, en autonomie : (1) avant 11 h 30 (plein tarif DeepSeek) les tâches locales et peu coûteuses en LLM — la validation de S sur `/paragraphes` (a004-a011), la porte propre (0,29) de N2, la préparation du corpus du palier 1 ; (2) de 11 h 30 à 16 h (fenêtre remisée) les tâches 
… [188 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — aurait-on un intérêt pour le FPGA maintenant?

**Tour 2** — j'ai 4 cartes FPGA Stratix V dans un mining rig. J'ai les cables pour les connecter en boucle de 40gbps. l'ensemble serait accessible via un cable ethernet dédié

**Tour 3** — considérant que certains modules on des équivalents heuristiques ou logique floue, peut-on ajouter les différentes options d'implémentation pour chaque module et avoir un routage flexible entre les modules

**Tour 4** — vas-y

**Tour 5** — go, continue tant qu'on est sur le tarif réduit de DeepSeek (jour ici, nuit en chine)

**Tour 6** — vas-y avec les prochains chantiers, continue tant qu'on est sur le tarif réduit de DeepSeek (jour ici, nuit en chine)

**Tour 7** — le rig n'est pas prêt (c'est un chantier en soit) continue sur d'autre chose

**Tour 8** — on est en soirée, donc tarif de jour en chine. fais des tâches qui demandent peu de réflexion et beaucoup de calcul local.

**Tour 9** — commit et push, puis sois autonome jusqu'à 16h. Tu est en charge de tous les chantiers. Coordonne-les et utilise beaucoup de subagents au besoin

**Tour 10** — continue en mode IA léger pendant la période plein tarif tout en exploitant au maximul les ressources locales. Sois autonome jusqu'à 8h demain

**Tour 11** — <goal_round> Objective: "De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits au strict minimum) et ressources locales à fond : (1) réparer le chargeur de corpus (mémoire bornée) et promouvoir le corpus v2 dédupliqué (6,90 Go) dans data/ avec son épingle ; (2) lancer le palier 1 — un modèle ~150 M sur le corpus v2 — sur les deux GPU, avec bancs aux checkpoi … [723 caractères tronqués]

**Tour 12** — <goal_round> Objective: "De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits au strict minimum) et ressources locales à fond : (1) réparer le chargeur de corpus (mémoire bornée) et promouvoir le corpus v2 dédupliqué (6,90 Go) dans data/ avec son épingle ; (2) lancer le palier 1 — un modèle ~150 M sur le corpus v2 — sur les deux GPU, avec bancs aux checkpoi … [723 caractères tronqués]

**Tour 13** — <goal_round> Objective: "De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits au strict minimum) et ressources locales à fond : (1) réparer le chargeur de corpus (mémoire bornée) et promouvoir le corpus v2 dédupliqué (6,90 Go) dans data/ avec son épingle ; (2) lancer le palier 1 — un modèle ~150 M sur le corpus v2 — sur les deux GPU, avec bancs aux checkpoi … [723 caractères tronqués]

**Tour 14** — <goal_round> Objective: "De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits au strict minimum) et ressources locales à fond : (1) réparer le chargeur de corpus (mémoire bornée) et promouvoir le corpus v2 dédupliqué (6,90 Go) dans data/ avec son épingle ; (2) lancer le palier 1 — un modèle ~150 M sur le corpus v2 — sur les deux GPU, avec bancs aux checkpoi … [723 caractères tronqués]

**Tour 15** — <goal_round> Objective: "De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits au strict minimum) et ressources locales à fond : (1) réparer le chargeur de corpus (mémoire bornée) et promouvoir le corpus v2 dédupliqué (6,90 Go) dans data/ avec son épingle ; (2) lancer le palier 1 — un modèle ~150 M sur le corpus v2 — sur les deux GPU, avec bancs aux checkpoi … [723 caractères tronqués]

**Tour 16** — <goal_round> Objective: "De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits au strict minimum) et ressources locales à fond : (1) réparer le chargeur de corpus (mémoire bornée) et promouvoir le corpus v2 dédupliqué (6,90 Go) dans data/ avec son épingle ; (2) lancer le palier 1 — un modèle ~150 M sur le corpus v2 — sur les deux GPU, avec bancs aux checkpoi … [723 caractères tronqués]

**Tour 17** — <goal_round> Objective: "De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits au strict minimum) et ressources locales à fond : (1) réparer le chargeur de corpus (mémoire bornée) et promouvoir le corpus v2 dédupliqué (6,90 Go) dans data/ avec son épingle ; (2) lancer le palier 1 — un modèle ~150 M sur le corpus v2 — sur les deux GPU, avec bancs aux checkpoi … [723 caractères tronqués]

**Tour 18** — <goal_round> Objective: "De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits au strict minimum) et ressources locales à fond : (1) réparer le chargeur de corpus (mémoire bornée) et promouvoir le corpus v2 dédupliqué (6,90 Go) dans data/ avec son épingle ; (2) lancer le palier 1 — un modèle ~150 M sur le corpus v2 — sur les deux GPU, avec bancs aux checkpoi … [723 caractères tronqués]

**Tour 19** — continue avec les prochaines actions

**Tour 20** — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val tiers disjoint (wikitext2 français) pour trancher v1/v2 sans le biais de distribution ; (2) brancher la règle A2.6 dans model.rs en opt-in (coût experts, refus nommé, trace), avec les portes flux/pont/coupe/echange-experts ; (3) ouvrir la diversité du corpus (livres FR) ; chaque r … [586 caractères tronqués]

**Tour 21** — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val tiers disjoint (wikitext2 français) pour trancher v1/v2 sans le biais de distribution ; (2) brancher la règle A2.6 dans model.rs en opt-in (coût experts, refus nommé, trace), avec les portes flux/pont/coupe/echange-experts ; (3) ouvrir la diversité du corpus (livres FR) ; chaque r … [586 caractères tronqués]

**Tour 22** — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val tiers disjoint (wikitext2 français) pour trancher v1/v2 sans le biais de distribution ; (2) brancher la règle A2.6 dans model.rs en opt-in (coût experts, refus nommé, trace), avec les portes flux/pont/coupe/echange-experts ; (3) ouvrir la diversité du corpus (livres FR) ; chaque r … [586 caractères tronqués]

**Tour 23** — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val tiers disjoint (wikitext2 français) pour trancher v1/v2 sans le biais de distribution ; (2) brancher la règle A2.6 dans model.rs en opt-in (coût experts, refus nommé, trace), avec les portes flux/pont/coupe/echange-experts ; (3) ouvrir la diversité du corpus (livres FR) ; chaque r … [586 caractères tronqués]

**Tour 24** — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val tiers disjoint (wikitext2 français) pour trancher v1/v2 sans le biais de distribution ; (2) brancher la règle A2.6 dans model.rs en opt-in (coût experts, refus nommé, trace), avec les portes flux/pont/coupe/echange-experts ; (3) ouvrir la diversité du corpus (livres FR) ; chaque r … [586 caractères tronqués]

**Tour 25** — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val tiers disjoint (wikitext2 français) pour trancher v1/v2 sans le biais de distribution ; (2) brancher la règle A2.6 dans model.rs en opt-in (coût experts, refus nommé, trace), avec les portes flux/pont/coupe/echange-experts ; (3) ouvrir la diversité du corpus (livres FR) ; chaque r … [586 caractères tronqués]

**Tour 26** — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val tiers disjoint (wikitext2 français) pour trancher v1/v2 sans le biais de distribution ; (2) brancher la règle A2.6 dans model.rs en opt-in (coût experts, refus nommé, trace), avec les portes flux/pont/coupe/echange-experts ; (3) ouvrir la diversité du corpus (livres FR) ; chaque r … [586 caractères tronqués]

**Tour 27** — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val tiers disjoint (wikitext2 français) pour trancher v1/v2 sans le biais de distribution ; (2) brancher la règle A2.6 dans model.rs en opt-in (coût experts, refus nommé, trace), avec les portes flux/pont/coupe/echange-experts ; (3) ouvrir la diversité du corpus (livres FR) ; chaque r … [586 caractères tronqués]

**Tour 28** — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val tiers disjoint (wikitext2 français) pour trancher v1/v2 sans le biais de distribution ; (2) brancher la règle A2.6 dans model.rs en opt-in (coût experts, refus nommé, trace), avec les portes flux/pont/coupe/echange-experts ; (3) ouvrir la diversité du corpus (livres FR) ; chaque r … [586 caractères tronqués]

**Tour 29** — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val tiers disjoint (wikitext2 français) pour trancher v1/v2 sans le biais de distribution ; (2) brancher la règle A2.6 dans model.rs en opt-in (coût experts, refus nommé, trace), avec les portes flux/pont/coupe/echange-experts ; (3) ouvrir la diversité du corpus (livres FR) ; chaque r … [587 caractères tronqués]

**Tour 30** — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val tiers disjoint (wikitext2 français) pour trancher v1/v2 sans le biais de distribution ; (2) brancher la règle A2.6 dans model.rs en opt-in (coût experts, refus nommé, trace), avec les portes flux/pont/coupe/echange-experts ; (3) ouvrir la diversité du corpus (livres FR) ; chaque r … [587 caractères tronqués]

**Tour 31** — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val tiers disjoint (wikitext2 français) pour trancher v1/v2 sans le biais de distribution ; (2) brancher la règle A2.6 dans model.rs en opt-in (coût experts, refus nommé, trace), avec les portes flux/pont/coupe/echange-experts ; (3) ouvrir la diversité du corpus (livres FR) ; chaque r … [587 caractères tronqués]

**Tour 32** — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val tiers disjoint (wikitext2 français) pour trancher v1/v2 sans le biais de distribution ; (2) brancher la règle A2.6 dans model.rs en opt-in (coût experts, refus nommé, trace), avec les portes flux/pont/coupe/echange-experts ; (3) ouvrir la diversité du corpus (livres FR) ; chaque r … [587 caractères tronqués]

**Tour 33** — continue avec les prochaines actions jusqu'à 17h

**Tour 34** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 1 … [535 caractères tronqués]

**Tour 35** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 2 … [535 caractères tronqués]

**Tour 36** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 3 … [535 caractères tronqués]

**Tour 37** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 4 … [535 caractères tronqués]

**Tour 38** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 5 … [535 caractères tronqués]

**Tour 39** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 6 … [535 caractères tronqués]

**Tour 40** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 7 … [535 caractères tronqués]

**Tour 41** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 8 … [535 caractères tronqués]

**Tour 42** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 9 … [535 caractères tronqués]

**Tour 43** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 1 … [536 caractères tronqués]

**Tour 44** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 1 … [536 caractères tronqués]

**Tour 45** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 1 … [536 caractères tronqués]

**Tour 46** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 1 … [536 caractères tronqués]

**Tour 47** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 1 … [536 caractères tronqués]

**Tour 48** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 1 … [536 caractères tronqués]

**Tour 49** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 1 … [536 caractères tronqués]

**Tour 50** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 1 … [536 caractères tronqués]

**Tour 51** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 1 … [536 caractères tronqués]

**Tour 52** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 1 … [536 caractères tronqués]

**Tour 53** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 2 … [536 caractères tronqués]

**Tour 54** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 2 … [536 caractères tronqués]

**Tour 55** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 2 … [536 caractères tronqués]

**Tour 56** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 2 … [536 caractères tronqués]

**Tour 57** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 2 … [536 caractères tronqués]

**Tour 58** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 2 … [536 caractères tronqués]

**Tour 59** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 2 … [536 caractères tronqués]

**Tour 60** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 2 … [536 caractères tronqués]

**Tour 61** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 2 … [536 caractères tronqués]

**Tour 62** — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les corpus wiki_big seul, wiki_fr seul et la référence v1, sur le val tiers wikitext2, en lançant les deux runs sur les GPU ; (2) finir A2.6 par la décision (le cache experts réglé par la règle, opt-in) avec les portes ; (3) fiche, état, commit et push pour chaque résultat." Round: 2 … [536 caractères tronqués]

**Tour 63** — que reste-t-il à faire?

**Tour 64** — d'abord rafraîchir la roadmap et l'état pour que la file redevienne exacte. puis enchaine avec la préparation des travaux de nuit (tarif DeepSeek plus élevé, donc moins de sollicitation LLM et des travaux plus longs localement. continue jusqu'à demain 8h en autonomie totale

**Tour 65** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [687 caractères tronqués]

**Tour 66** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [687 caractères tronqués]

**Tour 67** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [687 caractères tronqués]

**Tour 68** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [687 caractères tronqués]

**Tour 69** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [687 caractères tronqués]

**Tour 70** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [687 caractères tronqués]

**Tour 71** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [687 caractères tronqués]

**Tour 72** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [687 caractères tronqués]

**Tour 73** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [687 caractères tronqués]

**Tour 74** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [688 caractères tronqués]

**Tour 75** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [688 caractères tronqués]

**Tour 76** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [688 caractères tronqués]

**Tour 77** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [688 caractères tronqués]

**Tour 78** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [688 caractères tronqués]

**Tour 79** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [688 caractères tronqués]

**Tour 80** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [688 caractères tronqués]

**Tour 81** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [688 caractères tronqués]

**Tour 82** — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun sous-agent) : (1) construire un corpus « long-forme » (les lignes ≥ 200 o du plein texte) épinglé, et lancer deux runs longs sur les GPU — `wiki_big` seul et le long-forme, 11 tranches de 10 000 pas avec évaluation wikitext2 à chaque tranche ; (2) faire les deux pièces restantes  … [688 caractères tronqués]

**Tour 83** — "en-cours.md" montre 3 sessions en pause. Peux-tu les reprendre, ou tu as des choses a terminer avant?

**Tour 84** — prends tâches qui demandent plus de raisonnement pendant le jour et les tâches plus légères en LLM pendant le tarif élevé. go en mode autonome jusqu'à 16h

**Tour 85** — <goal_round> Objective: "De 08 h 30 à 16 h le 20/11, en autonomie : (1) avant 11 h 30 (plein tarif DeepSeek) les tâches locales et peu coûteuses en LLM — la validation de S sur `/paragraphes` (a004-a011), la porte propre (0,29) de N2, la préparation du corpus du palier 1 ; (2) de 11 h 30 à 16 h (fenêtre remisée) les tâches qui demandent du raisonnement par l'API — J4 (l'or de rôles), la rétro-trad … [658 caractères tronqués]

**Tour 86** — <goal_round> Objective: "De 08 h 30 à 16 h le 20/11, en autonomie : (1) avant 11 h 30 (plein tarif DeepSeek) les tâches locales et peu coûteuses en LLM — la validation de S sur `/paragraphes` (a004-a011), la porte propre (0,29) de N2, la préparation du corpus du palier 1 ; (2) de 11 h 30 à 16 h (fenêtre remisée) les tâches qui demandent du raisonnement par l'API — J4 (l'or de rôles), la rétro-trad … [658 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — aurait-on un intérêt pour le FPGA maintenant?

*15 appels d'outils.* Actions notables :

- grep
- bash — List repository root and pilotage docs
- read
- bash — Check FPGA card presence and recent commits
- bash — Check date and USB/PCI device list
- bash — Inspect sibling FPGA repo for DDR3 capacity and PCIe status
- bash — Check whether the Stratix V card is visible on PCIe
- bash — Read resource/method notes listing the FPGA
- bash — Check FPGA device nodes and November journal mentions
- bash — Read roadmap blocked-resource table
- bash — Date the FPGA verdict reports and read scaling argument

**Synthèse produite :**

⏵ Vérification du matériel et des chiffres FPGA avant réponse

**Réponse courte : non — et la seule chose qui a changé, c'est que la carte n'est plus là.**

Vérifié à l'instant sur la machine (17/11, 09 h 51) : **aucun device Altera sur PCIe ni sur USB**, pas de `/dev/ttyUSB*`. La Stratix V n'est branchée sur rien. A5.4 n'est donc pas « bloquée administrativement » ([roadmap](docs/pilotage/roadmap.md), [fiche](docs/pilotage/backlog/A5.4-fpga.md)) : elle est bloquée physiquement, en plus du reste.

**Pourquoi le verdict de septembre/octobre tient** — le mur est la mémoire, pas le calcul :

| même flux, 0,5 B Q8, 1 jeton = 352,8 M événements = 0,7 Go de listes | tok/s |
|---|---|
| FPGA, 1 carte, plafond **DDR3 9,66 Go/s** (72 ms/jeton, quoi que fasse la logique) | **13,7** *projeté* |
| CPU, mode push, **mesuré** | **15,6** |
| CPU, noyau dense int8, **mesuré** | **36,4** |
| GPU, listes / dense | **51 / ~770** |

La carte est **sous le CPU déjà mesuré**, dans son propre mode de prédilection. Elle lit 1/3 de la RAM et 1/40 de la VRAM ; ses 4 Go de DDR3 sont la mémoire la plus petite et la plus lente de la machine. Et la mesure de [architecture-mémoire §14](reports/rapport-architecture-memoire.md) n'a pas bougé : lire une couche coûte 18× son calcul — un accélérateur de calcul sur un chemin où le calcul pèse 5 % ne peut rien gagner.

**Ce qui a changé depuis, et qui empire le cas** : les modèles ont grossi (engram 365 Go mmap, MoE 18,56 Go, cache KV), et tous les murs actuels sont de la **bande passante**. Le seul chantier *compute-bound* de la maison est l'entraînement — or le PE est justement « 176 ALM, **0 DSP**, aucun multiplieur » : l'exact inverse de ce qu'il faut pour du dense fp16. L'AMP GPU à 2,4× le CPU ne se transpose pas.

**Les trois seuls intérêts qui restent, et leur prix :**

1. **Énergie** : 8,3 nJ/événement *projeté* contre 57 nJ CPU *mesuré* (7×). Aucun budget joules dans la roadmap ; et il faudrait PCIe + contrôleur DDR3 pour seulement le mesurer.
2. **Ring 2–4 cartes** : 92,8 tok/s projetés à 4 cartes ([rapport-cpu-aer](reports/rapport-cpu-aer.md)) — le seul argument d'échelle. Prix : 4 cartes, contrôleur DDR3, séquenceur, chemin retour, QSFP+ (rien de tout ça n'existe), pour un modèle 0,5 B que le GPU fait déjà 8× plus vite.
3. **Preuve de portabilité bit-exacte** du format sur un hôte sans multiplieur (l'argument CDC) : à moitié faite (PE + lecteur vérifiés et synthétisés, 309 020 événements), mais la moitié qui reste exige la carte.


… [717 caractères tronqués]

### Tour 2 — j'ai 4 cartes FPGA Stratix V dans un mining rig. J'ai les cables pour les connecter en boucle de 40gbps. l'ensemble sera … [41 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Read Stratix V card specs (QSFP+, PCIe, power)
- bash — Read host diagnostic script and multicard plan
- bash — Read the CPU/AER report assumptions
- bash — Check SSH hosts and known machines
- bash — Look for an existing GPU scatter benchmark
- bash — Check card power and GPU scatter notes

**Synthèse produite :**

⏵ Réponse : ce que 4 cartes + ring changent, et la seule porte qui décide

**Oui — mais pas pour le débit. Pour la seule chose que rien d'autre dans la maison ne fait.**

Ce que tu décris remplit exactement les deux conditions que le dépôt s'était lui-même fixées : « le FPGA n'a de sens qu'à partir de **2–4 cartes** » ([rapport-cpu-aer](reports/rapport-cpu-aer.md), verdict 4) et « le ring 40G n'a de sens que pour des **cartes déportées** » ([multicartes](docs/../FPGA-Stratix-V/docs/multicartes.md) §3). Un mining rig à 4 cartes, relié en boucle QSFP+ et accessible par Ethernet, c'est la topologie que la doc décrivait sans l'avoir.

**Ce que 4 cartes donnent (chiffres du dépôt)**

| | 4 cartes | comparaison |
|---|---|---|
| mémoire | **16 Go** (4 × 4 Go DDR3) | = 1 GPU ; 32 Go en tout sur la machine |
| bande passante agrégée | **38,6 Go/s** | CPU 28,7 · GPU 380 |
| débit d'événements | **19,3 G év/s** *projeté* (4 × 4,83) | CPU 5,3 mesuré · 1 GPU 18,1 mesuré (dispersion) |
| ring | **4,8 Go/s par lien** | sous la DDR3 d'une carte (9,66) → **les poids ne doivent jamais traverser le ring** |
| énergie | ~8,3 nJ/év *projeté* → ~160 W | GPU 12,7 nJ → seulement **1,5×**, pas 7× (les 7× sont contre le CPU) |

Deux conséquences structurelles : (1) seules les **activations** traversent le ring — 3,5 Mo par jeton, 0,7 ms par saut, négligeable devant 18 ms de lecture ; (2) l'**Ethernet dédié ne gêne pas** l'inférence : si les poids restent sur les cartes, seuls les jetons passent (quelques Ko). Et pour un modèle ≤ 4 Go (le 0,5 B Q8), **pas besoin du ring du tout** : 4 cartes en data-parallel = 4 × 13,7 ≈ **55 tok/s**.

**Le hic, et il est décisif.** Le seul avantage de vitesse du FPGA sur le GPU (le 7B à 5 % de densité : 92,8 tok/s projetés à 4 cartes contre ~52 en mode listes) est mesuré contre la **dispersion GPU non optimisée** (`np.add.at`-class, 18,1 G év/s), alors que la VRAM peut lire 380 Go/s. Un noyau scatter à accumulateurs par banc (sans atomiques) est une journée de travail — et s'il dépasse 19,3 G év/s, l'argument de débit du ring meurt et il ne reste que la démonstration. **C'est la porte à franchir avant d'écrire une ligne de RTL.**

**Le prix, sans fard** : les 4 pièces RTL manquantes ([bilan §4](reports/bilan-multi-materiel.md)) restent à faire — contrôleur DDR3 (le ref design UniPHY existe), séquenceur sur 168 matrices, chemin retour accumulateur → liste, opérations non matricielles — plus la chaîne 40G, dont **aucun exemple n'est publié** sur cett
… [1487 caractères tronqués]

### Tour 3 — considérant que certains modules on des équivalents heuristiques ou logique floue, peut-on ajouter les différentes optio … [85 caractères tronqués]

*12 appels d'outils.* Actions notables :

- bash — List source tree and Rust core
- bash — Search vision docs for module substitution and routing
- bash — Read block/contract model in native model doc
- bash — Inspect Rust traits and enums for dispatch
- bash — Check whether manifest routes are implemented
- bash — Read vision on substitutability and roadmap N0
- bash — List CLI flags and check variant provenance in trace
- bash — Check roadmap/backlog routing items and R0.5
- bash — Read DRVM manifest parsing for graph/routes
- bash — Read N3.3a routes report
- bash — Check DRVM writers and unread manifest fields
- job_kill

**Synthèse produite :**

⏵ Réponse : variantes par bloc et routage, ce que le dépôt permet déjà et ce qui manque

**Oui — l'idée est déjà la théorie du dépôt ; ce qui manque, c'est le contrat *exécutable*.**

Trois choses existent déjà : la [vision](docs/theorie/vision.md) (propriété 2 : deux implémentations du même contrat se remplacent sans toucher au bus), le [théorème d'indifférence](docs/theorie/modele-natif.md) (« le mode d'opération est privé », le bus ne voit que des types, un coût et une trace), et le manifeste DRVM qui porte déjà `graph.routes`, `regions`, `heads`, `thought` avec un `kind` en liste fermée et refus des inconnus. `placement.rs` porte même la règle de coût.

**Mais il y a un défaut à corriger avant d'ajouter quoi que ce soit** : le lecteur Rust parse `blocks` et `tensors`, refuse une version ou un `kind` inconnus — puis **ignore silencieusement** `routes`, `regions`, `heads`, `thought`. Un modèle qui déclare ses routes et s'exécute comme si elles n'existaient pas, c'est exactement ce que le doc interdit (« un modèle à moitié compris qui s'exécute quand même est un modèle qui ment »).

**Ce qu'il faut ajouter — trois champs, pas plus** :

```json
{"id":"b0","kind":"local_mixer","impl":"dense","contrat":{"version":1,"tolerance":0.0}}
```
plus, dans la trace : `impl`, `params`, `seed`. Et le coût mesuré par variante (octets, ms, énergie) : c'est tout ce que le consommateur a le droit de voir. Trois couches — **contrat** (public : signature, tolérance, champs de trace), **variantes** (privées : dense, heuristique, floue, API, distante — la techno ne sort jamais du bloc), **route** (sélection, statique par défaut).

**L'avertissement empirique, et c'est le point le plus important** : le routage flexible a **déjà** été essayé ici, quatre fois, et quatre négatifs — R0.5 (routeur extractif/génératif : AUC 0,839, mais transfert **0,819/0,313** contre **0,871/0,373** pour le choix fixe, [rapport](reports/rapport-r07-routeur.md)), puis R06 v1, la cascade v2, le déclencheur, le pipeline. Même diagnostic partout : **un seuil absolu ne transfère pas ; le choix dépend du document**. Donc : les variantes coûtent peu ; le *routeur* coûte cher et a déjà perdu une fois. Il ne s'ajoute pas comme un interrupteur, il se conquiert comme un résultat — avec le choix fixe pour contrôle négatif.

**Les trois pièges à nommer** : (1) **explosion combinatoire** — n blocs × k variantes, donc variantes seulement là où deux implémentations sont *déjà mesurées* ; (2) **non-déterminisme** — 
… [1439 caractères tronqués]

### Tour 4 — vas-y

*68 appels d'outils.* Actions notables :

- bash — Check git state and DRVM-related gates
- bash — Find the routes schema in the docs
- bash — Read the refusal and routes gates
- bash — Find DRVM manifest writers
- read
- bash — Read the DRVM exporter
- bash — Inspect real DRVM manifests
- bash — Check git hooks before committing
- glob
- bash — Compare manifest keys across real DRVM files
- bash — Read GGUF to DRVM manifest construction
- bash — Survey all DRVM manifests for exact key sets
- bash — Check Python test layout and inspect command
- bash — Find existing Python tests and DRVM gates
- … et 43 autres

**Synthèse produite :**

⏵ Récapitulatif du correctif livré et de la suite

**Fait, mesuré, committé — `97579a55`.**

Le défaut était réel : le format DRVM **déclarait** `routes`, `regions`, `heads`, `thought`, `bridge`, et le lecteur Rust n'en lisait **aucun**. Un manifeste avec une route s'exécutait comme si la route n'existait pas — le « modèle qui ment » que `modele-natif.md` interdit. Corrigé dans **les deux lecteurs** (Rust et `tools/drvm.py`), mêmes messages :

```
DRVM invalide : routes non exécutées : 1 route(s) — le lecteur refuse ce qu'il ne sait pas exécuter
```
(exit 3 côté Rust, `DRVMError` côté Python, sur le même fichier)

**Ce qui est verrouillé maintenant** : clés **fermées** aux cinq niveaux (racine, `graph`, bloc, `execution`, `thought`, région) ; région / tête / pont qui nomme un bloc absent → refus nommé ; `thought.steps` négatif ou fractionnaire → refus ; `routes` vide accepté, route déclarée **refusée** ; et `write_drvm` refuse aussi — **un manifeste ne peut plus naître menteur**.

**Le dispositif** (`porte-n3-refus` §4) : 10 cas mutés, les deux lecteurs, mêmes messages ; contrôles négatifs = le DRVM valide passe, l'écriture avec route est refusée, et **les 62 DRVM du disque restent lisibles**.

**Portes** : n3 ×18 **vertes** (11 h 16), `produit`/`document`/`etat`/`poids-creux` **vertes** (11 h 18). Tests Rust **136/137** — la rouge (`tests_vars::DRAVE_POS_DESYNC`) est **préexistante à HEAD**, hors de ce diff. Python : 189 tests, 1 erreur d'import préexistante (`test_bus`, `PYTHONPATH`).

Deux notes de transparence : le hook a balayé le journal de la session active dans le commit (15 fichiers ; c'est son comportement), et `tools/chantier/plan.json` reste non committé (session Pensée).

**Ce que ça débloque pour ta question** — le manifeste est maintenant un contrat vérifié, donc la suite est exactement ton idée, dans cet ordre :

1. `impl` + `contrat {version, tolerance}` par bloc, avec **refus d'une `impl` inconnue** (même mécanique que `kind`) ;
2. **provenance** dans la trace (`impl`, `params`, `seed`) — sans elle, deux variantes sont indistinguables au rejeu ;
3. **table de routes statique** dans `graph.routes` (le champ existe et est déjà contrôlé) — pas de routeur appris avant ;
4. **test d'indifférence** + contrôle négatif : deux implémentations du même contrat → même sortie à la tolérance près ; une impl hors contrat doit **échouer**, sinon le test ne teste rien ;
5. **coût mesuré par variante** (le `placement.rs` a déjà la règle).

Et le garde-fou 
… [290 caractères tronqués]

### Tour 5 — go, continue tant qu'on est sur le tarif réduit de DeepSeek (jour ici, nuit en chine)

*104 appels d'outils.* Actions notables :

- get_goal
- bash — Survey the native engine functions
- create_goal
- read
- bash — Read the drvm-pas-hex command
- bash — Check how the gate count is verified
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drvm.py`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drvm.py`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/native_model.py`
- bash — Add impl constants and Bloc fields
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/drvm.rs`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/drvm.rs`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/drvm.rs`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drvm.py`
- … et 67 autres

**Synthèse produite :**

⏵ Récapitulatif des cinq commits et de l'état du chantier

**Cinq commits, tous verts, tous mesurés.** Le chantier « variantes + routage » est passé d'une idée à un contrat exécuté.

| commit | ce qui est établi | le chiffre |
|---|---|---|
| `97579a55` | le lecteur refuse ce qu'il n'exécute pas (clés fermées, deux lecteurs) | **13 refus nommés**, 62 DRVM relus |
| `20648db7` | substitution = contrat : `impl` + `contrat` par bloc, indifférence mesurée | **4,768e-07** ≤ 1e-4 |
| `337715d1` | le moteur numpy exécute `bloque` et refuse `flou` | **2,831e-07** |
| `49904862` | **les routes sont exécutées** (seuil 0 / 10⁹ / mixte) | **bit-exact / bit-exact / 5,779e-03** |
| `b480a439` | les deux moteurs rendent le même corps, gardé à chaque passe | **3,576e-07 / 2,384e-07** |

**Ce que ça change dans le manifeste** — deux mécanismes, deux usages, désormais séparés :

```json
{"id":"b0","kind":"local_mixer","impl":"bloque","contrat":{"version":0,"tolerance":1e-4}}
{"id":"r0","bloc":"b1","si":{"kind":"position","seuil":512},"alors":"flou","sinon":"defaut"}
```
`impl` = **substitution** (même fonction, autre algorithme → indifférence dans la tolérance). `routes` = **routage** (autre fonction, même signature → la substitution est interdite, et le test doit le dire). Le nom du profil est public (manifeste → hash → trace), l'algorithme est privé, et **chaque moteur refuse ce qu'il n'exécute pas**.

**Trois portes nouvelles** (89 au total) : `porte-n3-variante`, `porte-n3-route`, `porte-n3-moteurs`. Toutes ont un contrôle négatif qui **doit échouer** : `flou` échoue l'indifférence (5,790e-03), le comparateur ne doit pas être aveugle, numpy refuse les routes. La porte des routes a d'ailleurs **trouvé un vrai bug** : l'indice de bloc venait de la position dans `graph.blocks` au lieu du `i` de `b{i}` — la route ne s'appliquait jamais. C'est le bit-exact qui l'a révélé.

**Les limites, écrites dans les fiches** : un modèle, une graine, un pas ; `bloque` n'est **pas plus rapide** ici (0,98–0,99×) ; le coût du routage n'est pas chronométré ; et surtout, **la politique de routage reste une question ouverte** — R0.5 et R06 ont montré quatre fois qu'un seuil global ne transfère pas. La porte prouve le mécanisme, pas qu'il faut router.

**Ce que je ferais ensuite, et pourquoi ce n'est plus du même chantier** : la suite n'est pas un mécanisme de plus, c'est une **politique** qui batte le choix fixe sur un banc (la condition nommée par R0.5 : calibration apprise par document, plus
… [802 caractères tronqués]

### Tour 6 — vas-y avec les prochains chantiers, continue tant qu'on est sur le tarif réduit de DeepSeek (jour ici, nuit en chine)

*36 appels d'outils.* Actions notables :

- create_goal
- bash — Check the native perplexity command
- bash — Add the court profile to the format and engine
- bash — Measure court vs defaut on a synthetic window-dominated model
- bash — Check the court window boundary behaviour
- bash — Inspect the trained model config
- bash — Measure perplexity defaut vs court on the trained model
- bash — Clean timing and a second text for perplexity
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-n3-court.sh`
- bash — Run the court gate
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n3-court.md`
- bash — Update counters and state for the court profile
- bash — Run N3 suite and key gates with court
- bash — Look for an in-distribution corpus
- … et 22 autres

**Synthèse produite :**

⏵ Bilan des trois chantiers de ce tour et de ce qu'ils tranchent

**Trois chantiers de plus, trois commits, et une décision tranchée.**

| commit | chantier | le chiffre |
|---|---|---|
| `de967b7b` | **N3.10 — `court`** : fenêtre divisée par 4, premier profil qui paie | **0,694×** le temps ; PPL **23,7480 → 23,5824** sur 2 048 o ; bit-exact < 64 o, **3,633e-02** au-delà |
| `24cb295e` | **A5.4 — le matériel existe** : 4 cartes + ring 40G + Ethernet | 16 Go, 38,6 Go/s agrégés, 19,3 G év/s projetés |
| `a0d7fa3b` | **P1 — le GPU scatter** : la porte qui décide du FPGA | **29,37 G év/s** sur **une** carte vs **19,3 G** pour **4** |

**Le résultat qui compte : P1 ferme l'argument de débit du FPGA.** Sur la même Quadro, la dispersion avec accumulateurs par bancs fait **29,37 G év/s** (268 M événements, int32 exact) — **1,52× la projection des 4 cartes**. Et le chiffre de référence du bilan (18,1 G) était mou : la même carte fait **25,65 G** avec la simple primitive à atomiques. Deux effets secondaires mesurés : la banque achète de la **contention** (3,2× à O=1024) et **pas** de la bande passante — à O=65 536 elle s'effondre (1,16 G), ce qui est le contrôle négatif du mécanisme. Toutes les méthodes rendent le **même** accumulateur, et le harnais est vérifié contre `np.bincount` (écart 0).

**Ce qu'il reste au FPGA, nommé et plus faible** : l'énergie (**1,5×** projeté sur le GPU, pas 7× — les 7× sont contre le CPU), le déterminisme bit-exact, la capacité (16 Go, égale à un GPU) et la **démonstration du réparti**. La décision de rouvrir A5.4 ne se prend plus sur le débit : elle se prend sur **P2** (le ring tient-il 4,8 Go/s ?) — et P2 demande le rig.

**Sur le routage** : `court` est le premier profil qui donne un arbitrage coût/qualité — mais sur ce modèle entraîné, la fenêtre de 1 024 n'est **pas utilisée** au-delà de 256 (PPL inchangée, ~5 % de temps). Il n'y a donc rien à router *ici* ; la politique demanderait un modèle et un corpus où la fenêtre longue sert, ce que la maison n'a pas encore.

**Où en est le dépôt** : 8 commits sur la journée, **90 portes** (dont 22 N3), **786 fiches**, **877 JSON**, état **1 735 mots**, revue de documentation verte, graphe backlog cohérent. Tests Rust **138/139** — la rouge (`tests_vars`) est préexistante à HEAD. La session N2 a du travail en cours dans l'arbre (`tools/banc_generation.py`, `reports/banc-generation-100m.json`) : je n'y ai pas touché, c'est à elle de le committer.

**Les deux prochaines actions, et leur condit
… [263 caractères tronqués]

### Tour 7 — le rig n'est pas prêt (c'est un chantier en soit) continue sur d'autre chose

*31 appels d'outils.* Actions notables :

- bash — Read the env-var completeness test
- bash — Read VARS_LUES and the source() helper
- bash — Compute the env-var list delta
- bash — Locate the two variables and any documentation table
- bash — Read the end of VARS_LUES
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs`
- bash — Run the Rust tests after the vars fix
- bash — Fix the comment reference and re-run tests
- bash — Commit the env-var test fix
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/bench/drvm_profils.py`
- bash — Simplify the profile bench loop
- bash — Run the profile bench on the trained model
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-profils-modele.md`
- … et 17 autres

**Synthèse produite :**

⏵ Bilan des quatre derniers commits et de la matrice de capacités

**Quatre commits de plus, et la ligne N3 est maintenant close proprement.**

| commit | chantier | le chiffre |
|---|---|---|
| `6d720eaa` | **tests** : `NATIVE_PROFONDEUR` et `POS_DESYNC` déclarées | suite Rust **139/139** |
| `0e5da7bd` | **profils sur le 34 M entraîné** | `bloque` **+0,04 %**, `flou` **+2,09 %**, `court` **−0,70 %** de PPL |
| `7c219067` | **numpy exécute `court`** | parité Rust ↔ numpy **2,980e-07** sur 128 octets |
| `a85da6f3` | **backlog N3** : cinq fiches, étape 5 | **22 portes** (17 au 04/11) |

**La nuance qui compte, et elle est écrite dans la fiche** : le contrat d'indifférence porte sur les **logits** (5e-7, sous 1e-4), **pas sur la perplexité**. `bloque` déplace la PPL de **+0,04 %** — la PPL est une fonction non linéaire de tous les logits, où le décalage s'accumule. Promettre l'invariance de la PPL aurait été un mensonge de plus. À l'inverse, `flou` coûte **+2,09 %** (une dégradation réelle), et `court` **−0,70 %** (la fenêtre de 1 024 n'est pas utilisée au-delà de 256 sur ce modèle). Les temps de cette passe ne sont **pas** interprétables (machine partagée : `bloque`, à coût identique, varie de −17 % à +4 %) — le chiffre de temps valide reste le banc contrôlé (0,694×).

**La matrice de capacités des deux moteurs, désormais explicite** :

| | Rust | numpy |
|---|---|---|
| `defaut`, `bloque`, `court` | ✅ | ✅ (parité 2,98–3,58e-07) |
| `flou` | ✅ | **refusé** (nommé) |
| routes | ✅ (seuil 0/10⁹ bit-exacts) | **refusées** (nommées) |

Chaque moteur déclare ce qu'il exécute et refuse le reste — c'est la règle du format appliquée aux moteurs eux-mêmes.

**Les temps valides, sans bruit** : `court` **0,694×** sur une charge dominée par l'attention (11 passes alternées, CV 3–6 %) ; **29,37 G év/s** pour la dispersion GPU (P1, sur 268 M d'événements, bit-exact contre `np.bincount`).

**Ce que je ne fais pas, et pourquoi** : la politique de routage demanderait un modèle et un corpus où la fenêtre longue **sert** (celui-ci ne l'utilise pas au-delà de 256) ; P2 demanderait le rig (chantier à part entière, comme tu l'as dit) ; `flou` dans numpy serait de la complétude sans usage (il coûte 2 % de PPL et ne gagne rien). Les lignes A2.6 et N2 appartiennent à d'autres sessions.

**État du dépôt** : 12 commits sur la journée, **90 portes**, **787 fiches**, **878 JSON**, état **1 750 mots**, revue de documentation verte, graphe backlog cohérent, tests Rust **139/139**. Le tra
… [340 caractères tronqués]

### Tour 8 — on est en soirée, donc tarif de jour en chine. fais des tâches qui demandent peu de réflexion et beaucoup de calcul loca … [2 caractères tronqués]

*48 appels d'outils.* Actions notables :

- bash — List trained models and their configs
- bash — Batch profile benchmarks on five trained models
- bash — Run the GPU scatter grid across accumulator sizes
- bash — Assemble the GPU scatter grid table
- bash — List and parse the grid JSONs correctly
- bash — Merge the scatter grid into one JSON
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gpu-scatter-grille.md`
- bash — Commit the scatter grid fiche
- bash — Check the profile batch progress
- bash — Check card-to-card variance on both GPUs
- bash — Add the two-GPU control and check batch progress
- bash — Measure Rust vs numpy parity on the real 34M model
- bash — Wait and check batch progress
- bash — Wait for the batch to finish
- … et 32 autres

**Synthèse produite :**

⏵ Bilan des trois gros calculs locaux (grille, cinq modèles, passe complète)

**Trois calculs longs, trois commits, zéro nouvelle rouge.**

**1. La grille du scatter GPU** (`d6e08d6a`) — 5 tailles d'accumulateur × 4 bancs :

| O \ B | atomiques | B=16 | B=64 |
|---:|---:|---:|---:|
| 512 | 4,76 | 28,16 | **28,52** |
| 1 024 | 8,42 | 27,14 | **27,53** |
| 4 096 | 25,18 | 26,51 | **26,57** |
| 16 384 | **26,58** | 26,64 | 2,73 |
| 65 536 | **26,98** | 2,70 | 1,16 |

La banque est un **remède à la contention**, pas un accélérateur : **6,0×** à 512 sorties, 1,06× à 4 096, et elle **se retourne** à 65 536 (le tableau de bancs ne tient plus dans le cache). Les deux cartes donnent le même plateau (25,20 / 25,23 en atomiques). Même le pire cas (25,2 G) reste au-dessus des 19,3 G projetés pour 4 cartes.

**2. Les profils sur cinq modèles entraînés** (`18d49ce7`) — 34,3 M chacun, même texte de 2 055 octets :

| modèle | fenêtre | `bloque` Δ | `flou` Δ | `court` Δ |
|---|---:|---:|---:|---:|
| base-en-34m | 256 | +0,00 % | +1,94 % | +1,46 % |
| base-multi-34m | 256 | +0,00 % | +1,07 % | +3,09 % |
| mix1024-60k | 1 024 | +0,04 % | +2,09 % | −0,70 % |
| propre512-8k | 512 | −0,04 % | +6,99 % | **−12,13 %** |
| rope2048-20k | 2 048 | +0,00 % | +3,09 % | **+4,57 %** |

`bloque` ne biaise pas (±0,04 %, des deux signes) ; `flou` est **toujours** une perte (5/5) ; `court` **change de signe** selon le modèle — le « gratuit » de mix1024 était une exception. Contrôle : sur le vrai modèle, Rust ↔ numpy à **1,526e-05** (≤ 1e-4).

**3. La passe complète** (`e6fa9c0d`) — 90 portes, **87 vertes, 3 rouges**, 116 min de calcul, cumul 6 981 s :
- `indice` (862 s) et `melange` (106 s) : **structurelles**, connues ;
- `sessions` (0 s) : **circonstance** — le mandat `e181ce02` est périmé de 1 896 min, c'est à sa session de rafraîchir son heartbeat ;
- **aucune rouge nouvelle** : les 22 portes N3 (dont les quatre du jour) sont vertes.

J'ai vu au passage le commit `02cc66d4` d'une autre session (`plans-tarif.md`) : il place les tâches API en remisée (11 h 30 → 19 h 30 EST) et le local en pleine — ce lot est exactement dans sa file « locale ».

État : **90 portes**, 789 fiches, 880 JSON, état 1 635 mots, tests Rust **139/139**. La session N2 garde son travail non committé (`tools/banc_generation.py`, `reports/banc-generation-100m.json`) : je n'y touche pas.

### Tour 9 — commit et push, puis sois autonome jusqu'à 16h. Tu est en charge de tous les chantiers. Coordonne-les et utilise beaucou … [24 caractères tronqués]

*218 appels d'outils.* Actions notables :

- bash — Inspect pending work, remote and branch
- bash — Inspect the N2 bench JSON and plan diff
- bash — Read the generation bench fiche
- bash — Read the 100M bench numbers and the random control
- bash — Read the generation bench arguments
- bash — Run matched 34M and random generation benches on GPU
- bash — Save the matched bench JSONs to reports
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-banc-generation-100m.md`
- bash — Locate the N2 bullet and counters
- bash — Integrate the 100M result into the state
- bash — Fix the date and JSON counter
- bash — Read the current state header
- bash — Apply the header and counter fixes
- bash — Read the exact current state lines
- … et 198 autres

**Synthèse produite :**

⏵ Bilan final de la période autonome

\# Le 18/11, de 00 h 30 à 16 h — bilan

**22 commits, tous poussés sur `s/v7` (HEAD `1fe0444d`), arbre propre, passe à 88/2.** Cinq chantiers avancés en parallèle, sept sous-agents, et deux résultats négatifs documentés — c'est le lot le plus dense de la semaine.

\## 1. N — le natif : le corpus épinglé, la courbe 3k → 53k, le décodage

| résultat | chiffre |
|---|---|
| **Corpus épinglé** | train `0876b608…` (1 017 487 092 o), val `fbddef91…`, manifeste `fae5bb73…`, `--verifie` 6,5 s |
| **La validation change tout** | mêmes poids, mêmes 65 536 jetons : **4,0139** (fin du train) contre **4,6792** (val épinglé) — **+16,57 %** |
| **Courbe 5 tranches** | PPL **4,6792 → 3,4130 → 3,2321 → 3,1317 → 3,0628 → 3,0098** (−36 %) |
| **Génération** | top-40 **0,551 → 0,895**, top-20 **0,932** ; greedy toujours cassé (répétition 10-13) |
| **Décodage** | **top-40 / T=0,5** bat le greedy sur tous les axes : 0,907 vs 0,902, rép **1,7 vs 5,7**, écho 0,075 vs 0,149 |

Le critère du palier 1 (« répétition ≤ 3 ») est **tenu en échantillonnage**, jamais en greedy : il doit nommer son décodage. Le plateau 33k-43k s'est rouvert au 5e tour.

\## 2. R0.7 — le tagger API gagne : 0,9572 contre 0,8625 (+9,47)

Lot lancé à **11 h 30:10**, fenêtre remisée : **608 appels réseau, 87 550 tokens, 0,01869 $, 612,6 s**. POS **0,9572** contre 0,8625 pour l'heuristique — le gain est dans les **classes ouvertes** (0,978 contre 0,7918, +18,6), les fermées à parité ; **0 refus**. Le coût prédit par le cache était exact à l'unité.

\## 3. A2.6 — la bande des experts mesurée, la tête Q8_0 dans la règle

- **7,0 Go/s à 8 fils** (16 fils : 165,40 ms, aucun gain), cache RAM 314 ms et tampons 231 ms (plus lents), **PPL 37,2013 invariante** — la règle doit porter ~7 Go/s et **un** lecteur, et refuser nommément.
- `placement.rs` : **+117 lignes** (tête Q8_0/Q6_K, perte 0, hors `PRECISIONS`), **9/9** tests placement, **140/140** crate, contrôle de retrait vérifié (8/9 sans l'entrée).

\## 4. D — 135,5 Go inventoriés, la dédup tranchée

- **7,5 Go** de français exploitable (écart de volume fermable sans collecte) ; **la diversité (~0,1 Go hors Wikipédia) ne l'est pas**.
- Dédup **par blocs : 0 %** (la duplication est courte et diffuse) → dédup **par ligne : 8,042 % des octets** (28,005 % des lignes) en **161 s**, idempotente, corpus v2 **6,90 Go** (`e3112a84…`).
- Test v2 en entraînement : **+2,1 %** de PPL à pas égal, **mais confondu** (v1 n'a que 0,038 % de duplication
… [1169 caractères tronqués]

### Tour 10 — continue en mode IA léger pendant la période plein tarif tout en exploitant au maximul les ressources locales. Sois auto … [22 caractères tronqués]

*23 appels d'outils.* Actions notables :

- create_goal
- bash — Check resources and read the A2.6 code plan
- bash — Read the A2.6 report structure
- bash — Read the A2.6 code plan and risk
- bash — Fix the corpus loader to use a uint8 tensor
- bash — Control the new loader against the known r4 PPL
- bash — Promote the deduped corpus and pin it
- bash — Count the parameters at scale
- bash — Time a 100-step 150M run on the v2 corpus
- bash — Launch the two overnight chains (150M on v2 and v1)
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-v2.md`
- bash — Commit the v2 corpus promotion
- bash — Read the placement module
- bash — Read the placement tests layout
- … et 9 autres

**Synthèse produite :**

⏵ Les deux chaînes 150 M tournent (GPU 0/1 à 99 %), la passe du soir est en cours — j'attends le premier point de contrôle

Les deux chaînes d'entraînement sont lancées depuis 16 h 39 (150 M, `d=896`, corpus v2 et v1, tranches de 10 000 pas avec banc après chacune), la passe complète des 90 portes tourne depuis 16 h 51, et le corpus v2 (6,90 Go) est promu et épinglé (`9861fb39…`). Le chargeur de corpus a été réparé au passage (`torch.frombuffer`), avec un contrôle bit-identique : la PPL du checkpoint r4 sur le val épinglé rend **3,0628**, exactement la valeur enregistrée.

Prochain point de contrôle dans ~90 minutes : fin de la première tranche (les deux runs), progression de la passe, et premier regard sur la courbe 150 M.

### Tour 11 — <goal_round> Objective: "De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits a … [1003 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Check the night's progress
- bash — Locate the experts placement site
- bash — Add the experts trace and test
- bash — Identify the failing test
- bash — Remove the unwired env name and re-test
- bash — Commit the experts trace

**Synthèse produite :**

⏵ A2.6 : la trace des experts est testée et poussée (`a039fe51`) — j'attends la fin de la première tranche (≈ 17 h 45) et la passe du soir

État de la nuit à 17 h 05 :

- **Chaînes 150 M** : tranche 1/12 en cours sur les deux GPU (≈ 0,4 s/pas, 10 000 pas), PPL de validation autour de 12,2 en début de course — les deux runs sont partis du même init (graine 1, `d=896`, 142 M paramètres) pour que la comparaison v2/v1 soit appariée. Banc complet après chaque tranche.
- **Passe des 90 portes** : lancée à 16 h 51, en cours (`work/portes/roue-1118-1712`).
- **A2.6** : la règle sait désormais **chiffrer** les experts (7,0 Go/s par lecteur, saturation à 8), **refuser** nommément (avec le coût NVMe qu'elle refuse) et **tracer** ses chiffres — 5 nouveaux tests, `placement` 14/14, crate **145/145**. Reste le branchement dans `model.rs`, que je ne toucherai pas tant que la passe tourne (elle recompile le binaire).

Prochain point de contrôle automatique dans ~75 minutes.

### Tour 12 — <goal_round> Objective: "De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits a … [1003 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Write the chain-curve analysis tool
- bash — Check progress of the chains and the pass

**Synthèse produite :**

⏵ Outil de courbe écrit (`tools/courbe_chaine.py`) : la nuit se lira en une table — j'attends la première tranche (≈ 17 h 45)

Les deux chaînes sont à ~2 500 pas de leur première tranche (PPL de validation ~12,3 en début de course, ce qui est le régime d'un modèle neuf), la passe du soir est à sa 9ᵉ porte, et l'outil `tools/courbe_chaine.py` produira la table des 12 tranches × 2 corpus (PPL, précision, trois régimes du banc) dès les premiers JSON. Prochain point complet à la fin de la tranche 1 et au fil de la passe.

### Tour 13 — <goal_round> Objective: "De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits a … [1003 caractères tronqués]

*12 appels d'outils.* Actions notables :

- bash — Sleep ten minutes and check the night
- bash — Read the loss trajectory of the 150M runs
- bash — Stop the diverging chains
- bash — Check whether the chains are stopped
- bash — Kill the orphaned trainers
- bash — Probe two learning rates on the 150M
- bash — Check the probe processes
- bash — Check the LR probes
- bash — Find the 73M scratch run log
- bash — Add the AMP scale to the training log
- bash — Check the probes' final numbers
- bash — Relaunch the chains at lr 1e-4

**Synthèse produite :**

⏵ Relance des chaînes 150 M à lr 1e-4 après la découverte d'un palier — la sonde montre la percée à 2 000 pas

**Ce que la sonde a appris.** La première版本 (lr 3e-4) plafonnait à une perte de ~2,5 et sa PPL de validation *montait* (12,0 → 13,1) : instabilité. Deux sondes de 2 000 pas à **lr 1e-4** et 2e-4 montrent un **palier puis une percée** : PPL 11,9 (1 000 pas) → 11,6 (1 500) → **7,6** (2 000) à 1e-4 (7,98 à 2e-4). La recette retenue est **lr 1e-4**, et les chaînes sont relancées depuis 17 h 24 (11 tranches de 10 000 pas, banc après chacune, échelle AMP journalisée).

Les deux GPU tournent à 99 %, la passe du soir est à sa ~25ᵉ porte. Prochain point complet à la fin de la tranche 1 (≈ 18 h 35).

### Tour 14 — <goal_round> Objective: "De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits a … [1003 caractères tronqués]

*12 appels d'outils.* Actions notables :

- bash — Record the learning-rate probe data
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-150m-lr.md`
- bash — Update the state for the LR finding
- bash — Trim the state under the T0 budget
- bash — Read the exact N4 bullet text
- bash — Apply the word cuts
- bash — Commit the LR finding and the curve tool
- bash — Ten minutes later: check the chains and the pass
- bash — Ten minutes later: check
- bash — Wait 25 minutes, then read the first tranche results

**Synthèse produite :**

⏵ Tranche 1 en approche : PPL 3,91 (v2) et 3,98 (v1) à ~6 400 pas — le relevé complet est programmé

Les deux 142 M sont sortis du palier (PPL ~3,9 à 6 400 pas, contre 12,0 au palier) et l'échelle AMP croît sainement (65 536 → 524 288). La passe du soir est à 66 portes, toujours 2 rouges (les structurelles). Le relevé de la première tranche (avec banc complet) se fera automatiquement vers 18 h 33.

### Tour 15 — <goal_round> Objective: "De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits a … [1003 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Verify the v2 corpus pin

**Synthèse produite :**

⏵ L'épingle du corpus v2 est vérifiée (6,90 Go, 21 s) — j'attends la fin de la tranche 1 (le relevé est programmé)

La vérification de l'épingle v2 vient de repasser : `train.txt` → **`e3112a842ed6d97a…`**, 6 900 585 097 octets, en 21 s. C'est le contrôle de l'objectif (1) : le corpus promu est bien celui qui a été dédupliqué et épinglé.

Les deux chaînes sont à ~6 900 pas (PPL ~3,9), la passe du soir à 66 portes (2 rouges structurelles), et le relevé de la tranche 1 (banc complet) se déclenchera automatiquement vers 18 h 33.

### Tour 16 — <goal_round> Objective: "De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits a … [1003 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Check the A2.6-related gates in the running pass

**Synthèse produite :**

⏵ Les portes A2.6 du soir sont vertes (flux, coupe, échange-experts) — la règle non branchée ne perturbe pas le régime 1 %

Vérifié dans le registre de la passe en cours : `porte-flux` (26 s), `porte-coupe` (140 s) et `porte-echange-experts` (55 s) sont **vertes** — l'invariant du routage des experts n'a pas bougé, ce qui est le contrôle attendu d'un ajout non branché. 67 portes passées, 2 rouges structurelles, la passe se termine vers 18 h 45.

La tranche 1 des deux 142 M se termine vers 18 h 33 (PPL ~3,9 en cours de route) ; le relevé complet suivra automatiquement.

### Tour 17 — <goal_round> Objective: "De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits a … [1003 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Inspect the material module's band tables
- bash — Wait ten minutes and check the three runs

**Synthèse produite :**

⏵ Les deux 142 M sont à ~8 000 pas (PPL 3,78), passe à 72 portes — tranche 1 dans quelques minutes

Aucune anomalie : la PPL descend régulièrement (3,78), l'échelle AMP est passée à 1 048 576 (saine), et la passe n'a toujours que les deux rouges structurelles. Le relevé de la première tranche (banc complet sur les deux corpus) est programmé ; c'est lui qui donnera le premier point de comparaison v1/v2.

### Tour 18 — <goal_round> Objective: "De 15 h 30 le 18/11 à 8 h le 19/11, en IA légère (aucun appel API payant, sous-agents réduits a … [1003 caractères tronqués]

*119 appels d'outils.* Actions notables :

- bash — Wait ten minutes, then check the first tranche outputs
- bash — Check the first tranche completion and benches
- job_output
- bash — Check the v2 tranche 1 and the pass
- bash — Wait for the evening pass to finish
- bash — Record the evening pass 88/2
- bash — Commit the evening pass record and the tranche 1 benches
- bash — Add the missing A2.6 experts gate
- bash — Inspect the test names in the release run
- bash — Fix the gate's test-name pattern
- bash — Update the gate count and the fiche
- bash — Commit the new A2.6 gate
- bash — Wait ten minutes and check the chains
- bash — Read the experts placement site in model.rs
- … et 75 autres

**Synthèse produite :**

⏵ Bilan de la nuit — objectif clos à 06 h 50, tout est poussé

\# La nuit du 18 au 19/11 — ce qui a été fait, ce qui est vérifié

**9 commits, tous poussés sur `s/v7` (HEAD `efb3d45b`), arbre propre, revue verte, passe à 89/2 sur 91 portes.** Aucun appel API payant, deux sous-agents (loisirs : aucun), les deux GPU occupés ~13 h.

\## Les quatre points de l'objectif

**1. Le chargeur réparé et le corpus v2 promu — ✅ vérifié.**
`torch.frombuffer` (uint8) remplace `torch.tensor(list(b))` : le corpus de 6,9 Go tient en ~7 Go de RAM au lieu de ~200. Le contrôle est bit-identique : la PPL du checkpoint r4 sur le val épinglé rend **3,0628**, exactement la valeur enregistrée dans `r4.pt.json`. `data/wiki_mix_v2/train.txt` (6 900 585 097 o, sha `e3112a84…`) est promu et épinglé (manifeste `9861fb39…`), et son `--verifie` repasse en 21 s. Fiche `reports/rapport-corpus-v2.md`.

**2. Le palier 1 sur les deux GPU — ✅ mesuré.**
Deux chaînes de **11 tranches de 10 000 pas** (142 M paramètres, `d=896`, lr 1e-4, AMP, val épinglé, banc complet après chaque tranche) :
- **v1** (1,017 Go) : PPL **3,5088 → 2,8440** (−19 %), précision 0,6878 ;
- **v2** (6,90 Go dédupliqué) : PPL **3,5568 → 3,0381** (−15 %), précision 0,6768.

Les deux courbes **plafonnent après ~60 000 pas**. v1 gagne la PPL de **6,4 %**, mais le val est **v1-centré** (les résumés `wiki_fr` sont dans son train) ; v2 gagne le top-20 final (**0,948 contre 0,900**) et 7 tranches sur 9. Le greedy reste instable (9-14, une pointe à 36). Fiche `reports/rapport-150m-nuit.md`, données `reports/courbe-150m.json` + 44 JSON de banc.

**3. La règle A2.6 — ✅ pour la règle, ⏳ pour le branchement (assumé et documenté).**
La bande des experts est mesurée (**7,0 Go/s par lecteur**, saturation à 8, 16 fils ne gagne pas), et `placement.rs` porte désormais `bande_experts`, `cout_experts`, `choisir_experts` (**refus nommé** avec le coût NVMe refusé) et `trace_experts` — **5 tests** (le coût reproduit 156,9 ms pour 1,097 Go/jeton), **placement 14/14**, **crate 145/145**, et la **porte qui manquait** : `porte-a2.6-experts` (91ᵉ porte). **Le branchement dans `model.rs` n'a pas été fait** : c'est la tâche désignée suivante (backlog `A2.6-ordonnanceur.md`, étape 5), et je n'ai pas voulu toucher le chemin de chargement du moteur à 7 h du matin sans une session fraîche.

**4. Les portes et les commits — ✅.**
Passe de la nuit : **91 portes, 89 vertes, 2 rouges** (`indice` 870 s, `melange` 108 s, les deux structurelles connues), la nouvelle p
… [1159 caractères tronqués]

### Tour 19 — continue avec les prochaines actions

*46 appels d'outils.* Actions notables :

- create_goal
- bash — Check the wikitext2 val and the eval tool
- bash — Find the PPL evaluation tools
- bash — Write and test the checkpoint PPL tool on wikitext2
- bash — Evaluate the v2 and 73M checkpoints on wikitext2
- bash — Compare the texture of the v1 and v2 corpora
- bash — Quantify the wiki markup density in both corpora
- bash — Save the wikitext2 results
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-val-tiers.md`
- bash — Update the state for the third-party val
- bash — Commit the third-party val result
- bash — Inspect the cleaning tool and prepare the 30k reference
- bash — Compute the v2 checkpoint at 30k on wikitext2
- bash — Write the corpus cleaner and run its autotest
- … et 29 autres

**Synthèse produite :**

⏵ Deux runs de contrôle en cours (nettoyé GPU 0, recollé GPU 1) — point complet à 30 minutes

À 10 000 pas, sur le val de v1 : v2 brut **3,5568**, nettoyé **3,5913**, recollé **3,5763** — le nettoyage et le recollement ne payent pas encore, et c'est exactement ce que le test doit trancher : la comparaison décisive se fait à **30 000 pas sur wikitext2** (le val tiers), où le brut est à 7,4277. Les deux chaînes tournent (GPU 0/1), la clôture de l'expérience est prévue vers 12 h.

### Tour 20 — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val t … [866 caractères tronqués]

*15 appels d'outils.* Actions notables :

- bash — Test whether the machine can download from Gutenberg
- bash — Diagnose the network access
- bash — Test the Wikisource API for French novels
- bash — Write and test the Wikisource collector
- bash — Extend to chapters and test on 6 books
- bash — Check the novels result and test the tales category
- bash — Inspect a Wikisource tale's raw wikitext
- bash — Diagnose the cleaning on real pages
- bash — Retry the Wikisource API with a delay and inspect a page
- bash — Diagnose the batch yield on 40 tales
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-diversite-sources.md`
- bash — Commit the diversity blocker
- bash — Fix the budget after the diversity commit
- bash — Read the t1 benches and wait for t2
- … et 1 autres

**Synthèse produite :**

⏵ Diversité documentée comme bloquée ; les deux variantes du corpus courent — à 10 000 pas, le corpus **nettoyé** a le meilleur top-40 (0,918 contre 0,888 au brut)

**Le point.** La diversité (livres FR) est **bloquée par les sources** : Gutenberg répond 503, Wikisource renvoie des portails à transclusions (40 pages de contes = 1 241 octets bruts). C'est documenté (`reports/rapport-diversite-sources.md`), le moissonneur est committé comme point de départ, et aucun texte n'a été ajouté au corpus. La réserve hors Wikipédia reste ≈ 0,1 Go.

**Le test en cours.** Les deux variantes du corpus v2 tournent (GPU 0 = nettoyé, GPU 1 = nettoyé + recollé, 3 tranches de 10 000 pas chacune). À 10 000 pas, les signaux sont déjà intéressants : le corpus **nettoyé** a le meilleur **top-40** (0,918 contre 0,888 pour le brut et 0,883 pour le recollé), alors que sa PPL sur le val de v1 est légèrement moins bonne (3,591 contre 3,557). La comparaison décisive reste **wikitext2 à 30 000 pas** (brut : 7,4277), prévue vers 11 h 45.

### Tour 21 — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val t … [866 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Read the Moe struct for the expert sizes
- bash — Find how the expert tensor sizes are accessible
- bash — Inspect the tensor and config structures
- bash — Read the gguf tensor accessor
- bash — Read the TensorInfo structure
- bash — Find the ggml type size helper
- bash — Write the A2.6 branch instructions in the backlog
- bash — Commit the A2.6 branch instructions

**Synthèse produite :**

⏵ Le branchement A2.6 a son mode d'emploi dans le backlog (sites, entrées, test, portes) — j'attends la tranche 2 des deux runs

**Fait depuis le dernier point** : les instructions précises du branchement A2.6 (le helper `octets_experts_par_jeton` à écrire, `gguf::octets_tensor` et `g.tensor("blk.N.ffn_*_exps.weight")` comme entrées, le test qui doit rendre 1,097 Go sur le 30B, l'opt-in `DRAVE_PERTE_MAX`, les portes à relancer) sont dans `docs/pilotage/backlog/A2.6-ordonnanceur.md`. Le branchement lui-même reste à faire — c'est le seul point de l'objectif qui n'est pas clos.

**En cours** : les deux variantes du corpus v2 (nettoyé GPU 0, recollé GPU 1) finissent leur deuxième tranche vers 10 h 35-50 ; la comparaison décisive (wikitext2 à 30 000 pas, contre 7,4277) tombe vers 11 h 45.

### Tour 22 — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val t … [866 caractères tronqués]

*15 appels d'outils.* Actions notables :

- bash — Read the construction site's context
- bash — Check the octets_tensor context and the type of g
- bash — Find the enclosing function of the site
- bash — Check n_layer_total and the Cfg fields
- bash — Add the experts-bytes arithmetic and its test
- bash — Add the helper and the trace to the engine
- bash — Fix the call qualification and rebuild
- bash — Test the experts trace on the real 30B model
- bash — Control the default path and run the A2.6 gates
- bash — Run the three remaining A2.6 gates
- job_output
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-branchement.md`
- bash — Update the state for the A2.6 branch
- bash — Commit the A2.6 branch
- … et 1 autres

**Synthèse produite :**

⏵ A2.6 est **branchée** : la règle parle sur le vrai 30B (`1,10 Go/jeton · 6,99 Go/s · 156,9 ms → VRAM`), le défaut ne bouge pas, les cinq portes sont vertes

**Ce qui vient d'être fait.** Le branchement A2.6 est committé (`b67af8de`) : `model::octets_experts_par_jeton` scanne les tenseurs `ffn_*_exps` du fichier, `placement::octets_experts` ramène au nombre d'experts allumés, et sous `DRAVE_PERTE_MAX` la construction imprime la trace — **1,10 Go/jeton, 156,9 ms → VRAM**, exactement la mesure. Sans l'opt-in : aucune trace, aucun changement de défaut. **146 tests**, `porte-a2.6-experts`, `porte-flux`, `porte-pont`, `porte-coupe`, `porte-echange-experts` **vertes**. Ce qui reste d'A2.6 est dit : la **décision** (le cache experts réglé par la règle) et les clusters.

**En cours** : les deux variantes du corpus v2 finissent leur deuxième tranche (nettoyé GPU 0, recollé GPU 1) ; la comparaison décisive sur wikitext2 à 30 000 pas est attendue vers 11 h 45.

### Tour 23 — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val t … [866 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Check the second tranche and the tree
- bash — Read the clean t2 result and the tree status

**Synthèse produite :**

⏵ Tranche 2 du corpus nettoyé : PPL 3,3201 (brut : 3,2989) — le nettoyage ne paye toujours pas sur la PPL, le top-40 reste son argument

**Le point à 20 000 pas** : le corpus nettoyé donne **3,3201** (précision 0,6485) contre **3,2989** pour le brut — l'écart se resserre mais reste en faveur du brut sur le val de v1. Le recollement (GPU 1) finit sa deuxième tranche. Les trois runs seront jugés à **30 000 pas sur wikitext2** (brut : 7,4277), où le nettoyage avait montré son meilleur top-40 à 10 000 pas (0,918 contre 0,888).

Les JSON de banc des tranches 1-2 (6 fichiers) attendent la clôture pour être committés avec la fiche. A2.6 est clos au niveau du branchement (trace), la diversité est documentée bloquée ; il ne reste que ce test à lire.

### Tour 24 — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val t … [866 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Commit the variant benches and fix the counter

**Synthèse produite :**

⏵ Les bancs des variantes sont committés (cl1, cl2, rf1 — compteurs à 959), l'arbre est propre

**Hygiène faite** : les six JSON de banc des deux variantes (nettoyé, recollé) sont entrés dans `reports/`, le compteur est passé à **959** et la revue est verte. Le message du commit dit « 963 » alors que le disque en avait 959 — coquille dans le message, l'état est juste.

**En cours** : le corpus recollé finit sa deuxième tranche (≈ 10 h 50), puis les troisièmes tranches ; la comparaison décisive sur wikitext2 (brut : 7,4277) est attendue vers 11 h 50. A2.6 est branchée (trace) et la diversité est documentée bloquée.

### Tour 25 — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val t … [866 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Read the variant benches

**Synthèse produite :**

⏵ Bancs des variantes relevés (top-40 : cl1 0,918 → cl2 0,871 ; rf1 0,883) — les troisièmes tranches décideront

**Ce que disent les bancs** : le corpus nettoyé garde le meilleur top-40 à la première tranche (0,918) mais redescend à 0,871 à la deuxième ; le recollé est à 0,883. La PPL, elle, reste en faveur du brut (3,299 contre 3,320 pour le nettoyé à 20 000 pas). Les troisièmes tranches (fin ≈ 11 h 30 pour le nettoyé, 11 h 50 pour le recollé) puis les trois PPL sur wikitext2 trancheront — le point complet et la fiche suivront.

### Tour 26 — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val t … [866 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Record the intermediate points of the three-way test
- bash — Restore the budget

**Synthèse produite :**

⏵ Les points intermédiaires du test à trois sont dans la fiche (20 000 pas : brut 3,2989 · nettoyé 3,3201) — j'attends les troisièmes tranches

**Fait** : la fiche du nettoyage porte désormais le tableau des points intermédiaires (PPL et top-40) et la lecture honnête — à 20 000 pas, le corpus nettoyé est à **+0,6 %** de PPL du brut et son avantage de top-40 (0,918 à 10 000 pas) est retombé à 0,871, donc pas stable. Le juge reste **wikitext2** aux 30 000 pas.

**En cours** : le recollé finit sa deuxième tranche (≈ 10 h 50), puis les troisièmes (≈ 11 h 30-50). À ce moment-là : les trois PPL sur wikitext2, la fiche finale et le commit de clôture.

### Tour 27 — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val t … [866 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Check the chains' tranche and step
- bash — Wait 50 minutes, then check the final tranches

**Synthèse produite :**

⏵ Les deux variantes sont dans leur **dernière tranche** (nettoyé à 1 500 pas, recollé à 150) — la clôture de l'expérience est programmée

Les deux runs terminent leur 3/3 (≈ 11 h 25 pour le nettoyé, ≈ 11 h 40 pour le recollé), avec le banc complet après chacun. Ensuite : les trois PPL sur **wikitext2** (brut 7,4277, nettoyé et recollé à calculer), la fiche finale et le commit de clôture. Tout le reste de l'objectif est fait ou nommé : le val tiers est mesuré (v1 6,867 / v2 7,093 / 73 M 7,351), A2.6 est branchée en trace sous opt-in, et la diversité est documentée bloquée par les sources.

### Tour 28 — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val t … [866 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Review the session's commits for the handoff

**Synthèse produite :**

⏵ 17 commits depuis minuit, l'arbre est propre et poussé — il ne reste que la lecture des deux dernières tranches (clôture ≈ 11 h 25-40)

**État du chantier à 10 h 30** : le val tiers est mesuré (v1 **6,867** / v2 **7,093** / 73 M **7,351**), la règle A2.6 est branchée en trace sous opt-in sur le vrai 30B, la diversité est documentée bloquée (Gutenberg 503, Wikisource à transclusions), et le test à trois (brut / nettoyé / recollé) termine ses dernières tranches. Les points intermédiaires sont dans la fiche : à 20 000 pas, le nettoyé est à +0,6 % de PPL du brut, son avantage de top-40 n'est pas stable.

La suite est automatique : les troisièmes tranches se terminent vers 11 h 25-40, puis je calcule les trois PPL sur wikitext2, je clos la fiche et je fais le point complet.

### Tour 29 — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val t … [867 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Compare the three 20k checkpoints on wikitext2
- bash — Record the 20k wikitext2 comparison
- bash — Find the exact fiche anchor
- bash — Apply the 20k comparison edits correctly
- bash — Commit the 20k wikitext2 comparison
- bash — Trim the state to the budget

**Synthèse produite :**

⏵ Wikitext2 à 20 000 pas : le brut gagne encore (7,8688 contre 7,9091 nettoyé et 8,0378 recollé) — la forme n'est pas la cause

**Le point clé** : sur le val tiers, à 20 000 pas, le corpus **brut** reste le meilleur, le nettoyé est à +0,5 %, le recollé à +2,1 %. Le nettoyage et le recollement **n'aident pas** : la seule différence qui tient entre v1 et v2 est la **sélection du contenu** (résumés + « big » de v1 contre le plein texte de `wiki_fr_texte`), pas la forme. C'est consigné dans la fiche et le JSON (`ppl-wikitext2.json`).

Les dernières tranches (30 000 pas) se terminent vers 11 h 25-40 ; je calculerai alors les trois PPL finaux et je clorai la fiche. Tout le reste de l'objectif est fait ou nommé : val tiers mesuré, A2.6 branchée, diversité documentée bloquée.

### Tour 30 — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val t … [867 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Check the last tranche progress
- bash — Verify the clean and reflow corpus pins

**Synthèse produite :**

⏵ Les deux corpus dérivés sont vérifiés (nettoyé `860aeb6a…`, recollé `9a5ca658…`) — les runs lisent bien les fichiers épinglés

**Vérification faite** : les épingles des deux corpus dérivés repassent — `work/clean/train.txt` (6 894 225 744 o, sha `860aeb6a…`) et `work/reflow/train.txt` (6 893 866 028 o, sha `9a5ca658…`) sont intacts, donc les runs en cours lisent bien les fichiers mesurés et pinnés.

Les troisièmes tranches avancent (nettoyé à 2 650 pas, recollé à 1 550 ; PPL ~3,37-3,39). Clôture attendue vers 11 h 30-40, puis les trois PPL sur wikitext2 et la fiche finale.

### Tour 31 — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val t … [867 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Read the roadmap's N row
- bash — Read the N row's next-action cell
- bash — Check the roadmap's budget headroom
- bash — Closing checks before the final integration

**Synthèse produite :**

⏵ Tous les contrôles de clôture sont verts (revue, état, budget, arbre synchronisé) — il ne reste que la lecture des dernières tranches

**Vérifié à 10 h 40** : revue de documentation ✅ (812 fiches, 961 JSON, 128 docs, 91 portes), état court ✅, budget T0 à 3 998/4 000 ✅, arbre propre et synchronisé avec `origin/s/v7`. La roadmap est à 8 999/9 000 mots — je ne l'ai pas touchée pour ne pas la faire déborder.

**Le seul point ouvert** : les troisièmes tranches (30 000 pas) du test à trois, qui se terminent vers 11 h 30-40, puis les trois PPL finaux sur wikitext2 et la fiche de clôture. Le reste de l'objectif est fait (val tiers mesuré, A2.6 branchée) ou nommé (diversité bloquée par les sources, décision A2.6 et sélection du contenu comme suites).

### Tour 32 — <goal_round> Objective: "Enchaîner les prochaines actions désignées : (1) mesurer les deux 150 M et le 73 M sur un val t … [867 caractères tronqués]

*14 appels d'outils.* Actions notables :

- bash — Ten-minute pause and progress
- bash — Ten-minute pause
- bash — Wait for the last tranche of the cleaned run
- bash — Check the cleaned run's final tranche
- bash — Compute the clean 30k wikitext2 PPL
- bash — Check the reflow run's final tranche
- bash — Compute the reflow 30k wikitext2 PPL
- bash — Record the final three-way results
- bash — Commit the three-way verdict
- bash — Fix the budget and push the verdict
- bash — Final verification before the handoff
- get_goal
- update_goal

**Synthèse produite :**

⏵ Bilan — les trois prochaines actions sont traitées : deux mesurées, une bloquée par les sources

\# Les prochaines actions — ce qui est fait, ce qui est bloqué

**Depuis minuit : 21 commits, tous poussés (HEAD `e4cd1953`), arbre propre, revue verte, budget T0 à 3 997/4 000.** Aucun sous-agent, aucun appel API payant.

\## 1. Le val tiers — ✅ mesuré, et il tranche

Les trois checkpoints passés sur **wikitext2 français** (tout le val, 352 256 jetons) :

| modèle | PPL wikitext2 |
|---|---:|
| 142 M corpus **v1** (1,017 Go propre) | **6,8674** |
| 142 M corpus **v2** (6,90 Go dédupliqué) | 7,0930 |
| 73 M (référence d'échelle) | 7,3508 |

**v1 gagne aussi hors du val v1-centré** (−3,2 %) : l'avantage n'est pas un artefact de distribution. Fiche `reports/rapport-val-tiers.md`, données `reports/ppl-wikitext2.json`.

**La suite désignée** — nettoyer et recoller le corpus (l'hypothèse « forme ») — a été **testée et écartée**. Trois runs de 30 000 pas, même recette :

| corpus | PPL val v1 | PPL wikitext2 |
|---|---:|---:|
| v2 brut | 3,1922 | **7,4277** |
| v2 nettoyé (`860aeb6a…`) | 3,2029 | 7,6189 (+2,6 %) |
| v2 recollé (`9a5ca658…`) | **3,1811** | 7,7476 (+4,3 %) |

Les deux juges **se contredisent** : le recollé est le meilleur sur le val de v1 et le plus mauvais sur wikitext2. **La forme n'est pas la cause** du déficit de v2 ; la **sélection du contenu** (résumés + « big » de v1 contre le plein texte de `wiki_fr_texte`) est la seule différence qui tienne. Fiche `reports/rapport-nettoyage-corpus.md`, outils `tools/nettoyer_corpus.py` et `tools/reflow_corpus.py` (autotests 7/7 et ok).

\## 2. A2.6 — ✅ branchée (trace sous opt-in), décision restante

Sous `DRAVE_PERTE_MAX`, la construction du moteur appelle la règle et imprime sur le **vrai 30B** :

```
experts : 1.10 Go/jeton · 8 lecteurs · bande 6.99 Go/s · 156.9 ms/jeton → VRAM
(VRAM libre 14.57 Go, RAM libre 68.72 Go, budget 1000.0 ms)
```

Ce sont les chiffres de la mesure (1,097 Go ; 156,95 ms). **Sans l'opt-in : aucune trace, aucun changement de défaut.** 146 tests, `porte-a2.6-experts`, `porte-flux`, `porte-pont`, `porte-coupe`, `porte-echange-experts` **vertes**. Ce qui reste — la **décision** (le cache experts réglé par la règle) et les clusters — est dit dans le backlog et la fiche `rapport-a2.6-branchement.md`.

\## 3. La diversité — ⚠️ bloquée par les sources

Gutenberg répond **503** ; Wikisource est joignable mais ses pages sont des **portails à transclusions** (40 pages de contes = 1 241 octets b
… [1306 caractères tronqués]

### Tour 33 — continue avec les prochaines actions jusqu'à 17h

*14 appels d'outils.* Actions notables :

- create_goal
- bash — Check the source corpora and compute the v1 reference at 30k
- bash — Launch the wiki_big and wiki_fr runs
- bash — Check the Materiel fields for the free RAM
- bash — Wire the placement decision for the experts cache
- bash — Test the decision branch on the real 30B
- bash — Remove the duplicate trace and verify a single one
- bash — Verify the single trace and the test suite
- bash — Run the tests and the five A2.6 gates
- bash — Confirm the test suite count
- bash — Commit the A2.6 decision branch
- bash — Restore the budget after the A2.6 decision commit
- bash — Final budget trim
- bash — Wait 50 minutes, then check the first tranche of the source runs

**Synthèse produite :**

⏵ A2.6 est **close** : la décision passe par la règle (le cache experts n'est créé que si elle le place en VRAM, refus nommé sinon) — 146 tests, cinq portes vertes

**Ce qui vient d'être fait** : le second pas d'A2.6 est committé (`7b234e98`). Sous `DRAVE_PERTE_MAX`, la création du cache VRAM des experts est soumise à `choisir_experts` : sur cette machine la règle rend VRAM (156,9 ms < 1 s) et le cache est créé comme avant ; un refus ne créerait pas le cache et le dirait. Sans l'opt-in, rien ne change. Testé sur le 30B (`DRAVE_GPU_EXPERTS=1 DRAVE_GPU_EXPERTS_GO=2 DRAVE_PERTE_MAX=1`) : une trace `experts : 1.10 Go/jeton · … → VRAM` puis `cache d'experts : budget 2.0 Go`. Il ne reste d'A2.6 que les **clusters** et la consolidation des tables de bandes — nommés au backlog.

**En cours** : la décomposition de la sélection du contenu — `wiki_big` seul (GPU 0, 831 Mo) et `wiki_fr` seul (GPU 1, 186 Mo), 3 tranches de 10 000 pas chacun, jugés sur wikitext2 contre la référence v1 (**7,3987** à 30 000 pas) et v2 (**7,4277**). Premières tranches vers 13 h 05, verdicts vers 15 h 30, fiche avant 17 h.

### Tour 34 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [815 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Characterize the two source corpora

**Synthèse produite :**

⏵ Les deux sources de v1 sont caractérisées : `wiki_big` 831 Mo / 407,5 o par ligne, `wiki_fr` 186 Mo / 422,3 — contre 108,8 pour le plein texte de v2

**Ce que la décomposition va dire** : v1 = `wiki_big` (2,04 M lignes, 407,5 o/ligne) + `wiki_fr` (440 709 lignes, 422,3 o/ligne), deux corpus « propres » à lignes longues ; v2 = le plein texte (63,4 M lignes, 108,8 o/ligne). Les deux runs en cours (wiki_big seul GPU 0, wiki_fr seul GPU 1) diront si l'avantage de v1 vient d'une **source** ou de leur **mélange**.

Références à 30 000 pas sur wikitext2 : **v1 7,3987**, **v2 7,4277** (et le nettoyé/recollé écartés). Les premières tranches tombent vers 13 h 05, les verdicts vers 15 h 30 ; la fiche et le commit suivront avant 17 h. A2.6 est clos (décision branchée, 146 tests, cinq portes vertes).

### Tour 35 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [815 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Check the source runs' pace

**Synthèse produite :**

⏵ Les deux runs de sources tiennent le rythme (0,44 s/pas, ~2 800 pas ; pertes 1,71 et 1,51) — première tranche vers 13 h 05

**Le point** : `wiki_big` (831 Mo) et `wiki_fr` (186 Mo) s'entraînent à pas égal depuis 11 h 56, à 0,44 s/pas, et apprennent normalement (perte 1,71 et 1,51 à ~2 800 pas). Les premières tranches (10 000 pas) tombent vers 13 h 05 ; les verdicts à 30 000 pas vers 15 h 30, puis les trois PPL sur wikitext2 et la fiche.

**Rappel des références** : à 30 000 pas sur wikitext2, v1 (le mélange) = **7,3987**, v2 (le plein texte) = **7,4277** ; le nettoyé (7,6189) et le recollé (7,7476) sont écartés. A2.6 est clos côté dépôt (décision branchée, 146 tests, cinq portes vertes).

### Tour 36 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [815 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Draft the content-selection fiche

**Synthèse produite :**

⏵ La fiche de la décomposition est écrite (sources caractérisées, références posées, lignes `wiki_big`/`wiki_fr` en attente)

**Fait** : `reports/rapport-selection-contenu.md` est rédigée — les deux sources de v1 sont caractérisées (`wiki_big` 831 Mo / 407,5 o par ligne, `wiki_fr` 186 Mo / 422,3 o par ligne), les références à 30 000 pas sont posées (v1 **7,3987**, v2 **7,4277**) et la question est cadrée : l'avantage de v1 vient-il d'une source ou de leur mélange ? Il ne manque que les deux lignes `wiki_big` et `wiki_fr`, à remplir quand les runs terminent (~15 h 30) — puis le verdict, l'état et le commit.

A2.6 est clos côté dépôt, les runs tiennent le rythme (0,44 s/pas), et rien d'autre n'est ouvert.

### Tour 37 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [815 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Pin the two source corpora
- bash — Add the source pins to the fiche

**Synthèse produite :**

⏵ Les deux sources de v1 sont épinglées (`wiki_big` `11aa9b74…`, `wiki_fr` `d2804870…`) : la fiche de la décomposition est complète, il ne manque que les mesures

**Fait** : les corpus `wiki_big` (831 Mo + val 46 Mo) et `wiki_fr` (186 Mo + val) sont épinglés et cités dans `reports/rapport-selection-contenu.md` — la fiche est prête, seules les deux lignes de résultats manquent. Notons au passage que `wiki_big` a un val de 46 Mo (un cinquième val possible pour plus tard).

**En cours** : les deux runs à 0,44 s/pas ; première tranche vers 13 h 05, verdicts vers 15 h 30. Ensuite : les trois PPL (v1 7,3987 et v2 7,4277 déjà connus, wiki_big et wiki_fr à calculer), le verdict, l'état et le commit — avant 17 h.

### Tour 38 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [815 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Ten-minute pause with a thermal check

**Synthèse produite :**

⏵ Les deux runs sont à ~4 500 pas (pertes 1,37-1,39), GPU à 87 °C et 75 °C — tout est nominal

**Le point** : `wiki_big` (GPU 0) et `wiki_fr` (GPU 1) tiennent 0,44 s/pas, les pertes descendent (1,37-1,39), et les GPU sont à 87 °C et 75 °C — chaud mais stable, comme pendant la nuit. Première tranche (10 000 pas) vers 13 h 05, puis les deux suivantes ; verdicts à 30 000 pas vers 15 h 30, fiche et commit avant 17 h.

Rien d'autre n'est ouvert : A2.6 est branchée et décidée (146 tests, cinq portes vertes), la fiche de la décomposition attend ses deux mesures, et les pins des sources sont en place.

### Tour 39 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [815 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Verify the two source pins

**Synthèse produite :**

⏵ Les épingles des deux sources vérifient (5 et 7 fichiers ✅) — les runs liront des fichiers intacts

**Vérification faite** : `wiki_big` (5 fichiers) et `wiki_fr` (7 fichiers) correspondent exactement à leurs manifestes (`11aa9b74…`, `d2804870…`). Les runs en cours lisent donc des corpus dont l'identité est prouvée, et la fiche les cite correctement.

**Prochain point** : la première tranche des deux runs (10 000 pas) vers 13 h 05 ; ensuite les deux dernières tranches et les trois PPL sur wikitext2. A2.6 est clos, les fiches attendent leurs mesures, et le commit de clôture est prévu avant 17 h.

### Tour 40 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [815 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Check the runs' progress and elapsed time

**Synthèse produite :**

⏵ Les runs sont à 4 500 et 4 750 pas de leur première tranche — rien à signaler

**Le point** : `wiki_big` (4 500 pas) et `wiki_fr` (4 750 pas) avancent normalement ; la première tranche tombe vers 13 h 05. Les épingles des sources vérifient, la fiche de la décomposition attend ses deux mesures, et le commit de clôture est prévu avant 17 h. Aucun autre chantier n'est ouvert.

### Tour 41 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [815 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Check the pending tree before the final commit

**Synthèse produite :**

⏵ L'arbre porte les deux épingles des sources et le journal auto-généré — tout entrera avec le commit de clôture

**Le point** : les seuls fichiers en attente sont les deux JSON d'épingle des sources (`corpus-epingle-wikibig.json`, `-wikifr.json`), la fiche de la décomposition (non committée) et les mises à jour du journal que le hook régénère. Rien d'anormal : le commit de clôture, après les mesures de 15 h 30, les emportera tous.

Les runs sont à ~4 500-4 750 pas de la première tranche ; la suite est automatique (tranches 2 et 3, puis les trois PPL sur wikitext2).

### Tour 42 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [815 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Ten-minute pause and progress

**Synthèse produite :**

⏵ Mi-tranche : `wiki_fr` mène sur la PPL (3,77 contre 4,01) — mais le val est celui de v1, qui contient `wiki_fr` à 18 %

**Le point** : à ~6 000 pas, `wiki_fr` (le petit corpus de résumés, 186 Mo) a une PPL de 3,77 contre 4,01 pour `wiki_big` (831 Mo) — cohérent avec le fait que le val de v1 contient `wiki_fr` à ~18 %, donc plus proche de lui. La comparaison décisive reste **wikitext2 à 30 000 pas**, où les deux sources seront jugées hors de leur propre distribution.

Première tranche vers 13 h 05 ; les deux dernières et les PPL vers 15 h 30-45 ; commit de clôture avant 17 h.

### Tour 43 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Ten-minute pause and check the first tranche

**Synthèse produite :**

⏵ Les runs sont à 7 500 et 7 900 pas ; la première tranche tombe vers 13 h 00-05

**Le point** : `wiki_big` (7 500 pas) et `wiki_fr` (7 900) finissent leur première tranche ; les JSON de résultat (PPL et banc) arrivent dans quelques minutes. Ensuite les deux dernières tranches, puis les trois PPL sur wikitext2 (v1 7,3987, v2 7,4277 déjà connus) et la fiche.

Rien d'autre n'est ouvert : A2.6 est close (décision branchée, 146 tests, cinq portes vertes), les épingles des sources vérifient, et le commit de clôture est prévu avant 17 h.

### Tour 44 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Ten-minute pause and read the first tranche
- bash — Read the first tranche results

**Synthèse produite :**

⏵ Première tranche : `wiki_fr` rend 3,3255 (précision 0,6447) — `wiki_big` la suit de quelques minutes

**Le point** : `wiki_fr` (186 Mo) finit sa première tranche à **PPL 3,3255** sur le val de v1 ; son banc est écrit (`banc-generation-wf1.json`). `wiki_big` (831 Mo), parti un peu plus tard, termine dans quelques minutes. Les deux runs enchaînent ensuite les tranches 2 et 3 (30 000 pas) ; les PPL sur wikitext2 suivront vers 15 h 30-45, puis la fiche et le commit de clôture.

### Tour 45 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Check the wiki_big first tranche

**Synthèse produite :**

⏵ Les deux premières tranches sont là : `wiki_fr` 3,3255, `wiki_big` 3,5054 — le petit corpus mène sur le val de v1

**Le point** : à 10 000 pas, `wiki_fr` (186 Mo) mène sur le val de v1 (**3,3255** contre **3,5054** pour `wiki_big`) — attendu, puisque ce val contient `wiki_fr` à ~18 % et que le petit corpus y est vu plus souvent. La mesure décisive reste **wikitext2 à 30 000 pas**, hors distribution des deux sources.

Les tranches 2 et 3 se terminent vers 14 h 15 et 15 h 30 ; ensuite les deux PPL sur wikitext2, la fiche et le commit de clôture.

### Tour 46 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Control the default PPL after the decision branch

**Synthèse produite :**

⏵ Le chemin par défaut rend bien une PPL sans trace (branchement sous opt-in seulement) — rien n'a bougé par défaut

**Contrôle fait** : sans `DRAVE_PERTE_MAX`, le binaire rend une perplexité normale et **aucune trace** d'experts — la décision ne s'active que sous l'opt-in, et les cinq portes A2.6 (dont `porte-flux` et `porte-echange-experts`, qui tournent en mode par défaut) restent vertes. C'est la garantie que le branchement n'a pas déplacé le défaut.

**En cours** : les tranches 2 des deux runs de sources (fin ≈ 14 h 15), puis les troisièmes (≈ 15 h 30) et les deux PPL sur wikitext2. Fiche et commit de clôture avant 17 h.

### Tour 47 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Wait 40 minutes, then check the second tranche

**Synthèse produite :**

⏵ Point de contrôle programmé à 13 h 55 (tranche 2 en cours) — les runs tournent, rien à faire d'ici là

**Le point** : `wiki_big` et `wiki_fr` sont dans leur deuxième tranche (fin ≈ 14 h 15), puis la troisième (≈ 15 h 30). Les PPL sur wikitext2 suivront, puis la fiche, l'état, le commit et le bilan à 17 h. A2.6 est close et son défaut est contrôlé ; les épingles des sources vérifient ; aucun autre chantier n'est ouvert.

### Tour 48 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Launch a fresh full gate pass during the runs

**Synthèse produite :**

⏵ Passe complète des 91 portes relancée à 13 h 12 sur l'arbre final (A2.6 décision incluse) — elle finira vers 15 h 15, avec les runs

**Pourquoi maintenant** : la dernière passe date de la nuit (88/2, avant le branchement et la décision A2.6). Une passe fraîche sur l'arbre actuel — 91 portes, machine chargée par les deux runs de sources — donnera le verdict de clôture en même temps que les résultats du test. C'est aussi la vérification que la décision A2.6 n'a déplacé aucun défaut.

**En cours** : les tranches 2 des runs (fin ≈ 14 h 15), puis les troisièmes (≈ 15 h 30) et les deux PPL sur wikitext2. La passe, les PPL, la fiche, l'état et le commit s'enchaîneront entre 15 h 15 et 17 h.

### Tour 49 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Ten-minute pause and pass progress

**Synthèse produite :**

⏵ Passe à 16 portes (aucune rouge), runs en tranche 2 — tout est nominal

**Le point** : la passe des 91 portes avance (16 portes, 0 rouge), `wiki_big` et `wiki_fr` sont en tranche 2, et la machine tient (GPU ~87/75 °C). Les prochains jalons : fin de la tranche 2 (≈ 14 h 15), de la passe (≈ 15 h 15), des troisièmes tranches (≈ 15 h 30), puis les deux PPL sur wikitext2 et la clôture (fiche, état, commit, bilan) avant 17 h.

### Tour 50 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Ten-minute pause and checks

**Synthèse produite :**

⏵ Passe à 26 portes (aucune rouge), tranche 2 à 4 150 pas — tout avance

**Le point** : la passe des 91 portes est à 26 (0 rouge), `wiki_fr` à 4 150 pas de sa tranche 2. Les jalons restent : tranche 2 (≈ 14 h 15), passe (≈ 15 h 15), tranche 3 (≈ 15 h 30), puis les deux PPL sur wikitext2 et la clôture avant 17 h.

### Tour 51 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Ten-minute pause and checks

**Synthèse produite :**

⏵ Passe à 29 portes, tranche 2 à 4 700 pas — rien à signaler

**Le point** : la passe des 91 portes est à 29 (0 rouge), `wiki_big` à 4 700 pas de sa tranche 2. Prochains jalons : tranche 2 (≈ 14 h 15), passe (≈ 15 h 15), tranche 3 (≈ 15 h 30), puis les PPL sur wikitext2 et la clôture.

### Tour 52 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Ten-minute pause and checks

**Synthèse produite :**

⏵ Passe à 31 portes (0 rouge), `wiki_fr` à 7 200 pas de sa tranche 2 — les deuxièmes résultats arrivent vers 14 h 15

**Le point** : la passe avance sans rouge (31 portes), les runs finissent leur deuxième tranche vers 14 h 10-20. Prochains jalons : les deuxièmes résultats (PPL), la passe (≈ 15 h 15), les troisièmes résultats (≈ 15 h 30), puis les PPL sur wikitext2, la fiche et le commit de clôture.

### Tour 53 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Ten-minute pause and check the second tranche

**Synthèse produite :**

⏵ Passe à 33 portes, deuxièmes tranches en cours — résultats vers 14 h 15

**Le point** : la passe est à 33 portes (0 rouge) ; `wiki_big` et `wiki_fr` terminent leur deuxième tranche d'ici 14 h 10-20. Ensuite : passe (≈ 15 h 15), troisièmes tranches (≈ 15 h 30), PPL sur wikitext2, fiche et commit avant 17 h.

### Tour 54 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Read the second tranche results

**Synthèse produite :**

⏵ Deuxième tranche : `wiki_fr` à **3,0220** (précision 0,6705) — le petit corpus domine le val de v1, comme attendu puisque c'en est la source

**Le point** : à 20 000 pas, `wiki_fr` (186 Mo) rend **3,0220** sur le val de v1 — meilleur que v2 (3,2989) et que v1 (3,2186) à pas égal. C'est le signe que ce val est *sa* distribution (il en vient), pas une preuve de qualité. `wiki_big` termine sa tranche dans quelques minutes, et le juge décisif reste **wikitext2 à 30 000 pas** (v1 7,3987, v2 7,4277). La passe est à 34 portes, sans rouge.

### Tour 55 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Read the wiki_big second tranche

**Synthèse produite :**

⏵ Passe à 65 portes (0 rouge), `wiki_big` finit sa tranche 2 dans quelques minutes

**Le point** : la passe a franchi les portes lourdes (65 portes, 0 rouge) et finira vers 15 h. `wiki_fr` est à 3,0220 à 20 000 pas ; `wiki_big` termine sa tranche 2 (≈ 14 h 25). Les troisièmes tranches (30 000 pas) terminent vers 15 h 30, puis les deux PPL sur wikitext2 et la clôture.

### Tour 56 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Read the wiki_big second tranche and the pass

**Synthèse produite :**

⏵ Tranche 2 : `wiki_big` 3,2209, `wiki_fr` 3,0220 — le mélange v1 (3,2186) se comporte comme `wiki_big` seul ; la passe est à 67 portes, 2 rouges (les structurelles)

**Le point** : à 20 000 pas sur le val de v1, `wiki_big` seul (3,2209) est au niveau du mélange v1 (3,2186), et `wiki_fr` seul est bien meilleur (3,0220) — ce val étant les résumés `wiki_fr`, c'est attendu. La question que tranchera **wikitext2 à 30 000 pas** : laquelle des deux sources généralise le mieux ? La passe est à 67 portes avec les **deux rouges structurelles** (`indice` 859 s, `melange` 106 s) et aucune autre.

### Tour 57 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Ten-minute pause and checks

**Synthèse produite :**

⏵ Passe à 72 portes (2 rouges structurelles), tranche 3 à 1 950 et 3 500 pas — les deux finissent vers 15 h 10-30

**Le point** : la passe franchit les dernières portes lourdes (72/91), les runs sont dans leur tranche finale. Vers 15 h 10 : le verdict de la passe ; vers 15 h 30 : les deuxièmes PPL sur wikitext2 ; ensuite la fiche, l'état, le commit et le bilan de 17 h.

### Tour 58 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Ten-minute pause and check the pass

**Synthèse produite :**

⏵ Passe à 75 portes (produit, préchargement vertes), tranche 3 à 5 000 pas — la fin approche

**Le point** : la passe est à 75 portes, toujours avec les deux rouges structurelles ; `wiki_fr` est à 5 000 pas de sa dernière tranche. Vers 15 h 10 : le verdict de la passe ; vers 15 h 25-30 : les PPL finaux sur wikitext2 ; ensuite la fiche, l'état, le commit et le bilan.

### Tour 59 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Ten-minute pause and checks

**Synthèse produite :**

⏵ Passe à 83 portes (ressources verte), tranche 3 à 4 700 pas — la passe finit dans ~10 minutes

**Le point** : il reste une poignée de portes (dont `vision`, la plus longue) ; les runs sont à mi-tranche finale. Vers 15 h 10 : le verdict de la passe ; vers 15 h 25-30 : les PPL finaux ; puis la fiche, l'état, le commit et le bilan.

### Tour 60 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Wait for the pass verdict
- bash — Check the pass verdict and the final tranche
- bash — Read the pass summary

**Synthèse produite :**

⏵ Passe de clôture : **91 portes, 89 vertes, 2 rouges** (les deux structurelles `indice` 859 s et `melange` 106 s) — aucune autre

**Le verdict de la passe** : 91 portes, **89 vertes, 2 rouges** — `indice` (859 s) et `melange` (106 s), les deux structurelles connues, et **aucune autre**. L'arbre actuel (branchement et décision A2.6 inclus) ne déplace donc aucun défaut, machine chargée par les deux runs.

**Ensuite** : les troisièmes tranches de `wiki_big` et `wiki_fr` finissent vers 15 h 25, puis leurs deux PPL sur wikitext2 — le verdict de la décomposition, la fiche, l'état et le commit avant 17 h.

### Tour 61 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Read the final tranche of the source runs
- bash — Compute the wiki_fr wikitext2 PPL

**Synthèse produite :**

⏵ `wiki_fr` seul sur wikitext2 : **8,0876** — le meilleur sur le val de v1 (2,8973) et le pire sur le val tiers ; `wiki_big` finit dans ~5 minutes

**Le premier verdict** : `wiki_fr` (186 Mo de résumés) est le meilleur sur le val de v1 (2,8973) mais le **pire** sur wikitext2 (8,0876, contre 7,3987 pour le mélange v1 et 7,4277 pour le plein texte) — il sur-apprend sa propre distribution. La question qui reste : `wiki_big` (831 Mo d'articles longs) fait-il aussi bien que le mélange ? Sa tranche finale se termine vers 15 h 30 ; je calcule sa PPL juste après, puis la fiche et le commit.

### Tour 62 — <goal_round> Objective: "D'ici 17 h le 19/11 : (1) décomposer la sélection du contenu — mesurer à pas égal (30 000) les  … [816 caractères tronqués]

*12 appels d'outils.* Actions notables :

- bash — Check the wiki_big final tranche
- bash — Read the wiki_big final result
- bash — Compute the wiki_big wikitext2 PPL
- bash — Fill the selection fiche with the final results
- bash — Update the state with the selection verdict and the pass
- bash — Apply the state updates
- bash — Record the fresh pass in the references
- bash — Commit the content-selection verdict and the pass
- bash — Final closing checks
- bash — Retry the diversity sources
- get_goal
- update_goal

**Synthèse produite :**

⏵ Bilan de la session jusqu'à 17 h — la sélection du contenu est identifiée, A2.6 est close, la passe est verte

\# Décomposition de la sélection du contenu — le résultat

Trois sources mesurées **seules** à 30 000 pas (même recette), jugées sur **wikitext2** (352 256 jetons, tout le val) :

| corpus | PPL wikitext2 | PPL val de v1 |
|---|---:|---:|
| **`wiki_big` seul** (831 Mo d'articles longs) | **7,2237** | 3,1144 |
| v1 (le mélange `wiki_big` + `wiki_fr`) | 7,3987 | 3,0763 |
| v2 (le plein texte, 6,9 Go) | 7,4277 | 3,1922 |
| `wiki_fr` seul (186 Mo de résumés) | 8,0876 | **2,8973** |

**La lecture** : c'est bien la **sélection du contenu** qui décide, pas la forme (le nettoyage et le recollement du plein texte avaient déjà été écartés : 7,62 et 7,75). `wiki_big` seul **bat le mélange de 2,4 %** et le plein texte de 2,8 %. `wiki_fr` (les résumés) sur-apprend : premier sur son propre val, dernier sur le val tiers — à pas égal il est vu 1,6 époque contre 0,35 pour `wiki_big`, donc c'est aussi une question d'**époques**. Conséquence pour le palier 1 : sélection **explicite** (articles longs), époques équilibrées.

Fiche `reports/rapport-selection-contenu.md`, données `reports/ppl-wikitext2.json`, sources épinglées (`11aa9b74…`, `d2804870…`).

\# A2.6 — close (branchement et décision)

Sous `DRAVE_PERTE_MAX`, la construction du moteur **appelle la règle** et imprime sur le vrai 30B : `experts : 1.10 Go/jeton · 8 lecteurs · 6.99 Go/s · 156.9 ms → VRAM`, puis le **cache VRAM des experts n'est créé que si la règle le place en VRAM** (un refus ne crée rien et le dit). Sans l'opt-in : aucune trace, aucun changement. **146 tests**, `porte-a2.6-experts`, `porte-flux`, `porte-pont`, `porte-coupe`, `porte-echange-experts` **vertes**. Restent, nommés au backlog : les **clusters** (le scan du seul fichier principal rend 0) et la consolidation des bandes de `materiel.rs`. Fiche `reports/rapport-a2.6-branchement.md`.

\# Passe de clôture et état

**91 portes, 89 vertes, 2 rouges** (`indice` 859 s, `melange` 106 s — les deux structurelles), machine chargée par les deux runs. Arbre **propre**, 25 commits depuis minuit, tout poussé (HEAD `10a3e49c`), revue verte (813 fiches, 979 JSON), budget T0 à 3 993/4 000, journal et schémas verts.

\# Ce que vous devriez regarder / décider

1. **`reports/rapport-selection-contenu.md`** — le résultat qui oriente le palier 1 : partir de `wiki_big` et équilibrer les époques, pas empiler du volume.
2. **La suite concrète** : construire le co
… [434 caractères tronqués]

### Tour 63 — que reste-t-il à faire?

*3 appels d'outils.* Actions notables :

- bash — Read the state's remaining-work section
- bash — Read the roadmap's next actions per chantier
- bash — Read the N, B, R, C next actions fully

**Synthèse produite :**

⏵ Inventaire de ce qui reste, chantier par chantier

\# Ce qui reste à faire

Le dépôt est **propre et vert** (91 portes, 89/2, arbre poussé), mais il reste du travail dans chaque programme. Voici l'inventaire, classé par valeur.

\## 1. N — le natif (la priorité, la plus proche d'un résultat)

- **La prochaine expérience est mesurée et désignée** : construire le corpus du palier 1 à partir de **`wiki_big`** (la source qui gagne : 7,2237 sur wikitext2) et de textes longs, avec des **époques équilibrées**, puis entraîner à époque égale (pas à pas égal). C'est la suite directe de `rapport-selection-contenu.md`.
- La **« porte propre (0,29) »** de la ligne N2 (l'ancien critère) n'est toujours pas franchie.
- **N4** reste partiel (le 73 M, la courbe, le décodage — mais pas la composition).

\## 2. A — le moteur

- **A2.6** : il ne reste que deux pièces, nommées au backlog — les **clusters** (le scan des experts du seul fichier principal rend 0) et la **consolidation des trois tables de bandes** de `materiel.rs`.
- **A3.4** bloqué (le compte Colab), **A5.4** : le FPGA (P2 : le ring tient-il 4,8 Go/s ? puis le RTL), **A6.2** : le MoE local 18 Go.
- Le **lot ≥ 2** assumé (le lot ne divise pas les lectures denses).

\## 3. R — le lecteur

- **R0.7** : la **décision de routage** (le tagger API gagne de +9,47 sur les classes ouvertes, mesuré ; le `--tagger auto` est un prototype opt-in) — c'est une décision humaine.
- **J4 — l'or de rôles** (les seconds cadres).
- **R2/R3** attendent N4/N5 ; **R1.1/R1.2** sont mesurés.

\## 4. S, B, Pensée, Panini, L, D

- **S** : migrer la page `/` vers la **v7** (106 paires sauvées, 41 à re-juger), corriger les référents (12/28 faux), la rétro-traduction API.
- **B** : **B13** le gold neuronal (POS 0,9415 ; cascade 0,6130/0,7574 ; le gold réel 432 est à 0,9065/0,4598/0,5633) ; **B10.3** attend un encodeur qui porte.
- **Pensée** : `g017`, T132/T133, le gold de pensée.
- **Panini** : les **26 signatures V14**, la calibration 42/44, le rejeu 27/60.
- **L** : la pragmatique neuronale, le refus r353, la signature V14 des 21 langues.
- **D — la diversité** : **bloqué par les sources** (Gutenberg 503, Wikisource à transclusions — re-testé à 15 h 42). Le moissonneur dédié (dump + résolveur) est le seul chemin, non commencé.

\## 5. Les dettes de pilotage (petites, réelles)

- **La roadmap a deux lignes périmées** : la ligne A dit encore « câbler la règle » (fait aujourd'hui : trace + décision) et la ligne N parle encore de r1/r2 et du top-40/0
… [832 caractères tronqués]

### Tour 64 — d'abord rafraîchir la roadmap et l'état pour que la file redevienne exacte. puis enchaine avec la préparation des travau … [154 caractères tronqués]

*26 appels d'outils.* Actions notables :

- bash — Refresh the roadmap's A and N rows
- bash — Trim the roadmap back under budget
- bash — Read the exact roadmap substrings
- bash — Apply the roadmap trims
- bash — Finish the roadmap trims
- bash — Read the exact fragments to trim
- bash — Refresh the state's remaining-work section
- bash — Compact the remaining-work section
- bash — Commit the pilotage refresh
- create_goal
- bash — Create the night goal and the long-lines extractor
- bash — Extract the long-form corpus in the background
- bash — Write the night chain script and check the extraction
- bash — Check the long-form extraction result
- … et 11 autres

**Synthèse produite :**

⏵ La file est exacte (roadmap + état), A2.6 est close (bandes et garde des clusters), et la nuit tourne : deux chaînes de 11 tranches sur les GPU

**Le rafraîchissement est fait** (`62719c32`) : la ligne A de la roadmap ne dit plus « câbler la règle » mais « les clusters et les bandes », la ligne N porte le 150 M et la sélection, et l'état a un « Ce qui reste » réécrit au 19/11 au lieu de la liste du 16/11. Budget respecté : roadmap 8 999/9 000, état 3 997/4 000.

**A2.6 est close** (`c932aa35`), les deux dernières pièces sont faites : `materiel::cout_par_jeton` lit une seule table de bandes (celle de la règle) et la bande **mesurée** des experts — 7,0 Go/s, pas les 31 du pread à 16 lecteurs ; le coût estimé du 30B passe de ~160 à **231 ms**, plus honnête. Et un modèle en clusters ne rend plus une trace fausse à 0 Go/jeton : la règle ne tranche pas, le message le dit. 146 tests, portes A2.6 vertes.

**La nuit** : le corpus « long-forme » (les lignes ≥ 200 o du plein texte, sans rien recoller) fait **4,79 Go à 464 o/ligne** et il est épinglé (`a50f6045…`, manifeste `12e4620d…`). Deux chaînes tournent depuis 16 h 36, 11 tranches de 10 000 pas chacune — `wiki_big` seul (GPU 0) et le long-forme (GPU 1) — avec, après **chaque** tranche, le banc de génération, la grammaticalité et la **PPL sur wikitext2** (`bench/chaine_nuit.sh`). Fin prévue vers 5 h 30-6 h ; la fiche de la nuit et le bilan à 8 h.

### Tour 65 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [967 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Inspect the clusters module
- bash — Read the cluster Mapping structure

**Synthèse produite :**

⏵ Les clusters ne sont pas scannables sans ouvrir leurs fichiers (le `Mapping` ne porte que les indices) — le garde est la bonne réponse pour l'instant ; les runs tournent

**Précision sur les clusters** : le `Mapping` des clusters ne contient que les indices (cluster, ligne), pas les chemins des fichiers — lire réellement leurs experts demanderait d'ouvrir les 8 GGUF de clusters au démarrage pour en sommer les tenseurs. C'est un chargement de métadonnées dédié, pas une ligne. Le **garde** commité est donc la bonne réponse : la règle ne tranche pas sur un 0 faux, et le message le dit. La fiche le précise déjà.

**La nuit** : les deux chaînes (`wiki_big` GPU 0, long-forme GPU 1) sont en première tranche, avec banc + grammaticalité + **PPL wikitext2** après chacune. Premier relevé programmé vers 17 h 55, bilan à 8 h.

### Tour 66 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [967 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Ten-minute pause and check the night runs

**Synthèse produite :**

⏵ Les deux chaînes sont à ~3 000 pas (pertes 1,57 et 1,32) — premières tranches vers 17 h 45

**Le point** : `wiki_big` (GPU 0) et le long-forme (GPU 1) sont sortis du palier et apprennent (pertes 1,57 et 1,32 à ~3 000 pas). Le premier relevé complet — PPL sur le val de v1, banc, grammaticalité et **PPL wikitext2** — arrive vers 17 h 55, programmé automatiquement. Ensuite les tranches s'enchaînent jusqu'à 5 h 30-6 h.

### Tour 67 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [967 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Wait 100 minutes, then read the first tranches
- bash — Ten-minute pause and check

**Synthèse produite :**

⏵ Tranche 1 à 4 450 et 4 700 pas — rien à signaler, premier relevé vers 17 h 55

**Le point** : les deux runs sont à mi-première tranche ; le relevé automatique (PPL val, banc, grammaticalité, wikitext2) tombe vers 17 h 55.

### Tour 68 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [967 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Add the wikitext2 column to the curve tool

**Synthèse produite :**

⏵ L'outil de courbe sait lire la PPL wikitext2 de chaque tranche — la nuit se lira en une table (val, wikitext2, banc)

**Fait** : `tools/courbe_chaine.py` lit désormais `reports/ppl-wikitext2-<prefixe><tranche>.json` et ajoute la colonne **wikitext2** à la table — c'est elle qui jugera les deux corpus de la nuit. Modifié mais pas encore committé (il partira avec la fiche de la nuit).

**Le point** : les runs sont en fin de première tranche ; le relevé (les deux PPL, les deux wikitext2, les bancs) arrive vers 17 h 55.

### Tour 69 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [967 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Ten-minute pause and check

**Synthèse produite :**

⏵ Tranche 1 à 5 950 pas — les checkpoints tombent vers 17 h 45

**Le point** : les deux runs approchent de la fin de leur première tranche ; le relevé (PPL val, wikitext2, banc) arrive vers 17 h 45-55.

### Tour 70 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [967 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Ten-minute pause and check
- bash — Read the first night tranche
- bash — Check the first tranche again
- bash — Check the wikitext2 of the first tranche

**Synthèse produite :**

⏵ Première tranche de la nuit : `wiki_big` **8,86** sur wikitext2 (PPL v1 3,53) contre **9,94** pour le long-forme (3,67) — le long-forme est derrière

**Le point** : à 10 000 pas, `wiki_big` mène sur les deux juges (wikitext2 **8,86** contre **9,94** ; val de v1 3,53 contre 3,67). C'est cohérent avec la décomposition de cet après-midi (le long-forme, 464 o/ligne, n'est pas `wiki_big`). Les tranches 2 sont lancées (800 et 1 400 pas) ; le point décisif sera **30 000 pas** (≈ 19 h 45), comparé aux références : `wiki_big` seul 7,2237 et v1 7,3987.

### Tour 71 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [967 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Ten-minute pause and check

**Synthèse produite :**

⏵ Tranche 2 à 2 300 et 2 950 pas — le point à 30 000 pas (les références) tombe vers 20 h 20

**Le point** : les deux runs sont dans leur deuxième tranche ; les checkpoints à 30 000 pas — comparables aux références de l'après-midi (`wiki_big` 7,2237, v1 7,3987) — arriveront vers 20 h 20. Les tranches 4 à 11 s'enchaînent ensuite jusqu'à ~5 h 30.

### Tour 72 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [967 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Commit the first night tranche's data
- bash — Commit the first night tranche with the corrected counter
- bash — Ten-minute pause
- bash — Ten-minute pause and check
- bash — Check the second night tranche
- bash — Read the second night tranche's wikitext2

**Synthèse produite :**

⏵ Deuxième tranche : `wiki_big` **7,83** sur wikitext2 (PPL v1 3,23) contre **8,50** pour le long-forme (3,41) — l'écart tient

**Le point** : à 20 000 pas, `wiki_big` mène sur les deux juges (wikitext2 7,83 contre 8,50 ; val de v1 3,23 contre 3,41). Le point à 30 000 pas (≈ 20 h 15) sera doublement intéressant : il doit **reproduire** le 7,2237 de la référence `wiki_big` seul de cet après-midi (même recette, même graine — un contrôle de reproductibilité), et il donnera le premier vrai chiffre du corpus long-forme.

### Tour 73 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [967 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Ten-minute pause
- bash — Ten-minute pause and check
- bash — Check the third tranche (the 30k point)
- bash — Read the 30k point

**Synthèse produite :**

⏵ Le long-forme à 30 000 pas : **8,19** sur wikitext2 (PPL v1 3,30) — le pire des corpus ; `wiki_big` (la réplication) arrive dans ~10 minutes

**Le point** : le corpus « long-forme » (les lignes ≥ 200 o du plein texte) rend **8,1943** à 30 000 pas sur wikitext2, contre 7,2237 pour `wiki_big` seul, 7,3987 pour le mélange v1 et 7,4277 pour le plein texte. Filtrer les lignes longues du plein texte ne retrouve donc pas la qualité de `wiki_big` : la sélection ne se réduit pas à la longueur des lignes. Le run `wiki_big` (même recette que la référence de l'après-midi) doit rendre ~7,22 — c'est le contrôle de reproductibilité de la nuit.

### Tour 74 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [968 caractères tronqués]

*26 appels d'outils.* Actions notables :

- bash — Read the wiki_big 30k point
- bash — Compare the initial states of the replayed runs
- bash — Add the replication and the variance caveat to the selection fiche
- bash — Read the fiche's current verdict
- bash — Apply the replication caveat correctly
- bash — Update the state with the replication caveat
- bash — Read the exact state strings
- bash — Apply the state edits with the exact anchors
- bash — Trim the N bullet under 80 words
- bash — Commit the 30k milestone and the replication finding
- bash — Ten-minute pause
- bash — Ten-minute pause and check
- bash — Read the fourth night tranche
- bash — Read the wiki_big fourth tranche
- … et 3 autres

**Synthèse produite :**

⏵ `wiki_big` passe sous 7 : **6,9299** à 50 000 pas (PPL v1 2,9942) — il bat déjà les 150 M de la nuit dernière (v1 6,867 à 110 000 pas est à sa portée)

**Le point** : la courbe `wiki_big` de la nuit est nette — 8,86 (10k) → 7,83 → 7,35 → 7,11 → **6,93 (50k)** sur wikitext2. Le long-forme suit de loin (7,93 à 40k). Si la tendance tient, `wiki_big` seul dépassera à 110 000 pas les deux 150 M de la nuit dernière (v1 6,867, v2 7,093) — la sélection du contenu serait confirmée au-delà du bruit. Prochain point : la tranche 6 (60k) vers 23 h 50.

### Tour 75 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [968 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Ten-minute pause and progress
- bash — Read the chain tails
- bash — Read the long-form fifth tranche

**Synthèse produite :**

⏵ 50 000 pas : `wiki_big` **6,93** contre **7,80** pour le long-forme (PPL val 2,99 contre 3,17) — l'écart se creuse

**Le point** : le long-forme ne rattrape pas (7,80 contre 6,93 à 50 000 pas) ; la sélection par la longueur des lignes est donc bien insuffisante face à `wiki_big`. Les deux runs sont dans leur sixième tranche (60 000 pas), qui s'achève vers 23 h 30-50 — point de commit suivant.

### Tour 76 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [968 caractères tronqués]

*15 appels d'outils.* Actions notables :

- bash — Ten-minute pause and progress check
- bash — Ten-minute pause and progress
- bash — Read the sixth tranche (60k)
- bash — Read the wiki_big sixth tranche
- bash — Read the 60k milestone
- bash — Read the wiki_big 60k wikitext2
- bash — Commit the 60k milestone
- bash — Ten-minute pause
- bash — Read the seventh tranche (70k)
- bash — Read the wiki_big seventh tranche

**Synthèse produite :**

⏵ `wiki_big` à 70 000 pas : **6,8566** sur wikitext2 — il bat déjà le 150 M v1 de la nuit dernière (6,867) avec 40 000 pas de moins

**Le point** : la courbe `wiki_big` est 8,86 → 7,83 → 7,35 → 7,11 → 6,93 → 6,89 → **6,86** (10k → 70k), et le long-forme plafonne à 7,63. La sélection du contenu est donc confirmée **hors du bruit** : `wiki_big` seul, à 70 000 pas, dépasse le mélange v1 entraîné 110 000 pas. Prochaine étape : 110 000 pas vers 5 h 30, puis la fiche de la nuit et le bilan de 8 h.

### Tour 77 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [968 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Ten-minute pause
- bash — Ten-minute pause and progress
- bash — Read the long-form eighth tranche
- bash — Read the wiki_big eighth tranche
- bash — Read the 80k milestone

**Synthèse produite :**

⏵ 80 000 pas : `wiki_big` **6,8590** (PPL v1 2,9327) — la courbe plafonne ; le long-forme **7,6053** (3,1428)

**Le point** : `wiki_big` a convergé autour de **6,86** sur wikitext2 (6,8566 à 70k, 6,8590 à 80k — le bruit) ; le long-forme plafonne à 7,60. À 110 000 pas (vers 5 h 30), `wiki_big` aura donc tenu, seul et avec 1 Go, le niveau du mélange v1 (6,867) entraîné 110 000 pas — c'est le résultat de la nuit. Ensuite la fiche et le bilan de 8 h.

### Tour 78 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [968 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Commit the 80k milestone
- bash — Ten-minute pause
- bash — Ten-minute pause and progress
- bash — Ten-minute pause and health check
- bash — Read the ninth tranche (90k)
- bash — Read the 90k milestone
- bash — Read the wiki_big ninth tranche

**Synthèse produite :**

⏵ 90 000 pas : `wiki_big` **6,8072** (PPL v1 2,9203) — nouveau meilleur ; le long-forme redescend à 7,6991

**Le point** : `wiki_big` continue de gagner un peu (6,86 → 6,81) ; le long-forme stagne (7,60-7,70). À 90 000 pas, `wiki_big` seul fait déjà **mieux que le 150 M v1 à 110 000 pas** (6,867) avec 20 000 pas de moins. Il reste deux tranches (100k et 110k, vers 5 h 50), puis la fiche de la nuit et le bilan de 8 h.

### Tour 79 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [968 caractères tronqués]

*1 appels d'outils.* Actions notables :

- bash — Draft the night's fiche

**Synthèse produite :**

⏵ La fiche de la nuit est rédigée (courbes jusqu'à 90 000 pas, variance, limites) — il reste à remplir les deux dernières tranches vers 5 h 50

**Fait** : `reports/rapport-nuit-wikibig.md` est écrit — les deux courbes (10k → 90k), la lecture (`wiki_big` 6,807 à 90k bat le v1 6,867 à 110k, avec 1 Go et 20k pas de moins ; le long-forme à 7,70), la variance du run-à-run (±1,8 %, le pas 1 bit-identique) et les limites. Non committée : les tranches 100k et 110k doivent y entrer, vers 5 h 50.

**En cours** : `wiki_big` et le long-forme dans leurs deux dernières tranches ; GPU à 87/76 °C, tout est nominal.

### Tour 80 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [968 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Ten-minute pause and progress
- bash — Ten-minute pause
- bash — Ten-minute pause and tranche count
- bash — Read the long-form 100k tranche

**Synthèse produite :**

⏵ 100 000 pas du long-forme : **7,7758** (PPL v1 3,1476) — il se dégrade légèrement sur ses dernières tranches ; `wiki_big` (100k) arrive vers 4 h 40

**Le point** : le long-forme ne progresse plus (7,60 → 7,70 → 7,78 aux tranches 80k-100k) alors que `wiki_big` continuait de gagner (6,81 à 90k). La sélection par `wiki_big` est donc nette. Il reste la tranche 100k de `wiki_big` (≈ 4 h 40), sa tranche 110k et celle du long-forme (≈ 5 h 50), puis la fiche et le bilan de 8 h.

### Tour 81 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [968 caractères tronqués]

*9 appels d'outils.* Actions notables :

- bash — Ten-minute pause
- bash — Ten-minute pause and progress
- bash — Read the 100k milestone
- bash — Read the wiki_big 100k tranche
- bash — Commit the 100k milestone
- bash — Fix the fiche counter
- bash — Update the state header to the 20/11
- bash — Read the long-form final tranche

**Synthèse produite :**

⏵ Le long-forme est fini : **7,7479** à 110 000 pas (PPL v1 3,1525) — sa meilleure tranche était 80 000 (7,61) ; `wiki_big` termine vers 5 h 50

**Le point** : la chaîne long-forme est close (05 h 10) à **7,7479** sur wikitext2, avec un pic à 7,6053 (80 000 pas) puis une dégradation — filtrer les lignes longues du plein texte ne tient pas sur la durée. `wiki_big` termine sa onzième tranche vers 5 h 50 ; ensuite la fiche de la nuit (les deux courbes complètes) et le bilan de 8 h.

### Tour 82 — <goal_round> Objective: "De 16 h 30 le 19/11 à 8 h le 20/11, en autonomie totale et IA minimale (aucun appel API, aucun  … [968 caractères tronqués]

*25 appels d'outils.* Actions notables :

- bash — Fill the long-form's final rows in the fiche
- bash — Ten-minute pause and progress
- bash — Check the wiki_big final tranche
- bash — Read the wiki_big final tranche
- bash — Read the wiki_big final results
- bash — Finalize the night's fiche
- bash — Update the state with the night's final results
- bash — Commit the night's final results
- bash — Launch the closing gate pass
- bash — Ten-minute pause and pass progress
- bash — Ten-minute pause
- bash — Ten-minute pause and pass tail
- bash — Ten-minute pause and pass end
- bash — Read the closing pass verdict
- … et 4 autres

**Synthèse produite :**

⏵ Bilan de 8 h — la nuit `wiki_big` a tranché la sélection du contenu, A2.6 est close, la passe de clôture est verte

\# La nuit du 19-20/11 — ce qui est fait et vérifié

**11 commits poussés (HEAD `8c581925`), arbre propre, revue verte, passe de clôture à 91 portes, 89 vertes et 2 rouges (les deux structurelles).**

\## 1. La sélection du contenu — ✅ tranchée

Deux chaînes de 11 tranches de 10 000 pas, avec le banc, la grammaticalité et la **PPL sur wikitext2 après chaque tranche** :

| pas | `wiki_big` seul (831 Mo) | long-forme (4,79 Go) |
|---:|---|---|
| 10 000 | 8,86 / 3,53 | 9,94 / 3,67 |
| 50 000 | 6,93 / 2,99 | 7,80 / 3,17 |
| 90 000 | **6,81** / 2,92 | 7,70 / 3,15 |
| 110 000 | **6,8349** / 2,9102 | **7,7479** / 3,1525 |

*(wikitext2 / PPL du val de v1)*

**`wiki_big` seul fait 6,8349 à 110 000 pas** — au niveau du mélange v1 (6,867) et devant le plein texte v2 (7,093), avec **1 Go de données et 1/7 de celle de v2**. Le **long-forme** (les lignes ≥ 200 o du plein texte, extrait et épinglé `a50f6045…`) finit à 7,7479 : **filtrer les lignes longues ne remplace pas la préparation de `wiki_big`**.

**Le contrôle qui compte** : le rejeu de `wiki_big` donne 7,3531 à 30 000 pas contre 7,2237 l'après-midi, alors que le **pas 1 est bit-identique** (5,6191 / 185,706) — la **variance du run-à-run est de ±1,8 %** et vient de l'entraînement (non-déterminisme GPU), pas de l'initialisation. L'écart `wiki_big`/v1 (−0,5 %) est donc **dans le bruit** : match nul avec v1, victoire sur v2. La fiche de sélection de l'après-midi a été **corrigée** en conséquence. Fiche : `reports/rapport-nuit-wikibig.md`.

\## 2. A2.6 — ✅ close (deux pièces)

- **Les bandes** : `materiel::cout_par_jeton` lit désormais une seule table (celle de `placement.rs`) et la bande **mesurée** des experts (7,0 Go/s), au lieu de ses trois constantes (dont un NVMe à 31 Go/s qui n'est pas le chemin par défaut) ; le coût estimé du 30B passe de ~160 à **231 ms**.
- **Les clusters** : un scan vide ne tranche plus (le message le dit, les drapeaux restent maîtres) ; **lire** réellement les clusters demanderait d'ouvrir leurs GGUF au démarrage — c'est dit au backlog, pas fait.
- **146 tests**, `porte-a2.6-experts`, `porte-ressources`, `porte-flux`, `porte-pont`, `porte-coupe`, `porte-echange-experts` vertes.

\## 3. La passe de clôture — ✅

**91 portes, 89 vertes, 2 rouges** (`indice` 836 s, `melange` 105 s, les deux structurelles connues), machine au repos. Record dans `references-non-regression.md` et dans
… [747 caractères tronqués]

### Tour 83 — "en-cours.md" montre 3 sessions en pause. Peux-tu les reprendre, ou tu as des choses a terminer avant?

*15 appels d'outils.* Actions notables :

- bash — Read the paused sessions in the state
- bash — Check the session statuses and S's plan
- bash — Find the /paragraphes validation cases
- bash — Resume session S and read its validation fiche
- bash — Inspect the paragraphs data for the S validation
- bash — Check the N2 and Pensée plans and the paragraphs file
- bash — Reconcile the session blocks in the state
- bash — List the session headings in the state
- bash — Remove the terminated session blocks
- bash — Read the state verifier's next-action rule
- bash — Read the exact next-action regex
- bash — Read the current remaining-work section
- bash — Restore the state from HEAD
- bash — Redo the session reconciliation safely
- … et 1 autres

**Synthèse produite :**

⏵ Rien à terminer d'abord — S est reprise, N2 était terminé, Pensée attend sa fenêtre

**Non, je n'ai rien à terminer avant** : le goal de la nuit est clos (les 11 commits, la passe de clôture 91 portes / 89-2, l'arbre propre, le bilan livré à 8 h). Les sessions n'attendaient donc que la reprise.

**Ce que j'ai fait à l'instant** (`e0fd67e7`, poussé) :

- **S (`29ad180d`) — reprise, actif.** Son heartbeat est rafraîchi (20/11 08 h 10) et son plan est passé à « actif ». Sa prochaine action est concrète : **la validation sur `/paragraphes`** — a001-a003 faits (14/14 référents confirmés par l'anglais), **8 restants** (a004-a011) — puis la rétro-traduction et les 71 langues.
- **N2 (`0733c5bb`) — terminé**, pas en pause : son `plan.md` dit « terminé » depuis le 05/11, alors que l'état le listait encore. Son bloc sort de `en-cours`, et sa pièce restante — la **porte propre (0,29)** — est une action de la ligne **N**, pas d'une session : je la porte avec le palier 1.
- **Le hub du 04/11 (`1e7ef596`)** sort aussi : il est superseded par le pilotage courant.
- **Pensée (`e181ce02`) — reste en pause, mais pour une bonne raison** : l'entraînement long qu'elle attendait est **fait** (les 150 M du 19-20/11). Ce qui lui reste, c'est **J4** (l'or de rôles) — qui passe par l'API et donc par la **fenêtre remisée de 11 h 30**. Je la reprendrai à ce moment-là ; d'ici là je peux faire ses parties locales (T132/T133).

**État** : 2 sessions (S actif, Pensée en pause), revue verte, budget respecté (T0 3 9xx/4 000).

**La suite** : je continue la validation de S (`/paragraphes`, a004-a011) — c'est sa prochaine action, et elle est purement locale. Dites-moi si vous préférez que je prenne d'abord la porte propre (0,29) de N2 ou le corpus du palier 1.

### Tour 84 — prends tâches qui demandent plus de raisonnement pendant le jour et les tâches plus légères en LLM pendant le tarif élev … [34 caractères tronqués]

*77 appels d'outils.* Actions notables :

- create_goal
- bash — Create the goal and find the paragraphs data
- bash — Read the paragraphs data structure
- bash — Read the paragraphs list
- bash — Read the paragraph IDs and the S state fiche
- bash — Launch the two variance runs (seeds 2 and 3)
- bash — Inspect the structures tooling for the / page migration
- bash — Inspect the tree measure and the stored phrases
- bash — Read the tree measure and the server's root route
- bash — Read the root page handler
- bash — Read the data state builder of the root page
- bash — Read the data loader and the analyzer output
- bash — Inspect the stored bank's shape
- bash — Compare the stored and fresh analyzer outputs
- … et 63 autres

**Synthèse produite :**

⏵ Les graines 2 et 3 à 10 000 pas : **8,78** et **9,50** sur wikitext2 (graine 1 : 8,86) — l'écart entre graines est déjà visible

**Le point** : à 10 000 pas, les trois graines de `wiki_big` donnent **8,78** (g2), **8,86** (g1) et **9,50** (g3) sur wikitext2 — un écart de 8 % qui inclut l'initialisation (les PPL du pas 1 diffèrent : 185,5 / 185,7). C'est exactement ce que la nuit avait pointé : **le run-à-run est le bruit qui limite les comparaisons fines**. Les tranches 20k (≈ 11 h 30) et 30k (≈ 12 h 50) diront si l'écart se resserre en convergeant — c'est la mesure qui manque pour juger la sélection du contenu.

À 11 h 30, la fenêtre remisée s'ouvre : je lance la **rétro-traduction v2** (anaphores numérotées) et son analyse contre le gold des a001-a003, comme prévu.

### Tour 85 — <goal_round> Objective: "De 08 h 30 à 16 h le 20/11, en autonomie : (1) avant 11 h 30 (plein tarif DeepSeek) les tâches  … [938 caractères tronqués]

*29 appels d'outils.* Actions notables :

- bash — Read the N2 clean-gate context
- bash — Run the retro-translation v2
- bash — Inspect the v2 pairs against the gold paragraphs
- bash — Update the retro-translation fiche with the v2 analysis
- bash — Commit the retro-translation v2 analysis
- bash — Check the concurrent commits and the state lines
- bash — Retry the retro-translation commit
- bash — Wait and check the variance second tranche
- bash — Ten-minute pause and progress
- bash — Check the second tranche of the variance runs
- bash — Read the variance second tranche
- bash — Check the variance runs' progress
- bash — Read the seed-2 second tranche
- bash — Read the tagger fiche's summary
- … et 11 autres

**Synthèse produite :**

⏵ Graine 3 à 30 000 pas : **7,5607** sur wikitext2 — l'écart entre graines (7,22 / 7,35 / 7,56) est plus grand que l'écart wiki_big/v2

**Le point** : la graine 3 finit à **7,5607**, contre 7,2237 et 7,3531 pour les deux exécutions de la graine 1. L'écart entre graines (jusqu'à **4,6 %**) dépasse donc les écarts que la sélection du contenu prétendait mesurer (wiki_big 6,83 vs v1 6,87 : −0,5 % ; vs v2 7,09 : −3,6 %). C'est un résultat important — et sobre — pour la fiche de variance : **à 30 000 pas, une seule graine ne tranche pas**. La graine 2 arrive vers 12 h 50 ; ensuite le run du palier 1 (3,69 Go) part sur le GPU et la fiche de variance sera écrite.

### Tour 86 — <goal_round> Objective: "De 08 h 30 à 16 h le 20/11, en autonomie : (1) avant 11 h 30 (plein tarif DeepSeek) les tâches  … [938 caractères tronqués]

*32 appels d'outils.* Actions notables :

- bash — Read the seed-2 final tranche
- bash — Read the seed-2 final results
- bash — Launch the palier-1 runs (two seeds)
- bash — Finalize the variance fiche and the state
- bash — Commit the variance result
- bash — Add the gold comparison to the retro-translation script
- bash — List the gold disagreements
- bash — Fix the non-referent handling and re-run the comparison
- bash — Commit the gold comparison
- bash — Search for the J4 roles gold definition
- bash — Locate the roles gold data
- bash — Inspect the roles gold
- bash — Read the roles gold's structure fully
- bash — Read the roles gold's frame format
- … et 12 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drvm.py` | 0 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_drvm_trace.py` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/drvm.rs` | 0 | 8 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-n3-refus.sh` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/modele-natif.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/native_model.py` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drvm_infere.py` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drvm_trace.py` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-n3-variante.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n3-variante.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-n3-route.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n3-route.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-n3-moteurs.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n3-moteurs.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-n3-court.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n3-court.md` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/A5.4-fpga.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/bench/gpu_scatter.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gpu-scatter.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/bench/drvm_profils.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-profils-modele.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gpu-scatter-grille.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-profils-5-modeles.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-banc-generation-100m.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/epingle_corpus.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-epingle.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-natif-val-deux-decoupages.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-bande-experts.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r1-13000-pas.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/bench/balayage_decodage.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-decodage-r1.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-612.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-courbe-r1-r3.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-v2-slice.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-v2.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-150m-lr.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-150m-nuit.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-val-tiers.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-nettoyage-corpus.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-diversite-sources.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-branchement.md` | 1 | 0 |

### Sous-agents lancés

- tour 9 — Reconnaissance A2.6 experts
- tour 9 — Grammaticalité du 100 M
- tour 9 — Préparation lot tagger 612
- tour 9 — Inventaire des données D
- tour 9 — Dédoublonnage par blocs
- tour 9 — Précision de tête Q8_0
- tour 9 — Dédoublonnage par ligne

### Commandes exécutées (échantillon)

- **T1** List repository root and pilotage docs
- **T1** Check FPGA card presence and recent commits
- **T1** Check date and USB/PCI device list
- **T1** Inspect sibling FPGA repo for DDR3 capacity and PCIe status
- **T1** Check whether the Stratix V card is visible on PCIe
- **T1** Read resource/method notes listing the FPGA
- **T1** Check FPGA device nodes and November journal mentions
- **T1** Read roadmap blocked-resource table
- **T1** Date the FPGA verdict reports and read scaling argument
- **T2** Read Stratix V card specs (QSFP+, PCIe, power)
- **T2** Read host diagnostic script and multicard plan
- **T2** Read the CPU/AER report assumptions
- **T2** Check SSH hosts and known machines
- **T2** Look for an existing GPU scatter benchmark
- **T2** Check card power and GPU scatter notes
- **T3** List source tree and Rust core
- **T3** Search vision docs for module substitution and routing
- **T3** Read block/contract model in native model doc
- **T3** Inspect Rust traits and enums for dispatch
- **T3** Check whether manifest routes are implemented
- **T3** Read vision on substitutability and roadmap N0
- **T3** List CLI flags and check variant provenance in trace
- **T3** Check roadmap/backlog routing items and R0.5
- **T3** Read DRVM manifest parsing for graph/routes
- **T3** Read N3.3a routes report
- **T3** Check DRVM writers and unread manifest fields
- **T4** Check git state and DRVM-related gates
- **T4** Find the routes schema in the docs
- **T4** Read the refusal and routes gates
- **T4** Find DRVM manifest writers
- **T4** Read the DRVM exporter
- **T4** Inspect real DRVM manifests
- **T4** Check git hooks before committing
- **T4** Compare manifest keys across real DRVM files
- **T4** Read GGUF to DRVM manifest construction
- **T4** Survey all DRVM manifests for exact key sets
- **T4** Check Python test layout and inspect command
- **T4** Find existing Python tests and DRVM gates
- **T4** Read the gate qualifier for DRVM
- **T4** Find hand-built manifests in tools and gates
- … et 1011 autres

## 4. Mesures et résultats marquants

- **T1** `7f23e55b NATIF — LE CACHE KV MESURÉ (×1,9, PARITÉ 3/3) : LE JETON COÛTE 11 MS PARCE QUE LE CPU LIT 136 MO DE POIDS (MEMORY-BOUND), PAS PARCE QU'IL RECALCULE ; LE GPU EST AU LANCEMENT (11 MS À VIDE)`
- **T1** `14ef014d ÉTUDE — LES 2 GPU NVLink VS CPU : L'ENTRAÎNEMENT ×12-39 (×77 EN TANDEM), LE PRÉFILL ×12, LE NVLink 23 Go/s, MAIS LE 34 M EST SOUS-UTILISÉ ET LA GÉNÉRATION EST BLOQUÉE PAR LE CACHE KV (×20-50 `
- **T1** `v14_l2_distance.sv        Kernel 1 — Distance L2 V14 (Q0.16, 14 DSP, 2 cycles)`
- **T1** `nipada_k1.sdc             Contraintes timing 200 MHz`
- **T1** `nipada_k2.sdc             Contraintes timing 200 MHz`
- **T1** `./docs/carte-storey-peak.md:46:| DDR3 | **4 Go**, DIMM 240 broches, **72 bits avec ECC**, 1600 MT/s | **9 662 Mo/s lecture / 7 816 Mo/s écriture** (mesuré, [blog part 6](https://j-marjanovic.io/strati`
- **T1** `./docs/carte-storey-peak.md:47:| PCIe | Connecteur x16, **2 Hard IP PCIe Gen3 x8 distincts** (pièce custom) | **6,5 Go/s par interface**, **11–12 Go/s** avec les deux ([blog part 8](https://j-marjanov`
- **T1** `./docs/carte-storey-peak.md:58:| `CLK_PCIE1` | `PIN_AF6/AF5` | 100 MHz (période 10 ns) | refclk Hard IP PCIe n°1 |`
- **T1** `./docs/carte-storey-peak.md:59:| `CLK_PCIE2` | `PIN_AF34/AF35` | 100 MHz | refclk Hard IP PCIe n°2 |`
- **T1** `./docs/carte-storey-peak.md:138:| [chisel-stuff / pcie-endpoint](https://github.com/j-marjanovic/chisel-stuff/tree/master/example-14-pcie-endpoint) | Endpoint PCIe + DMA écrit en Chisel (6,5 Go/s par `
- **T1** `| S — la banque validée | **`/paragraphes` fini** : 9/9 paragraphes, 19/19 candidats, 11 acceptés, 8 exclus, **11 verdicts committés (`389b99f`)** ; **banque 150 verdicts / 74 des 207 phrases** (35,7 `
- **T1** `- **R0** : un contrôleur **classique** + un modèle externe atteint-il **90 %** de la compréhension à **30 %** du`
- **T1** `60e19582 2026-10-01 22:26:07 -0400 mmap : 365,7 Go adresses en 0,08 s et 47 Mo de RSS`
- **T1** `| CPU, borné bande passante (28,7 Go/s) | 14.51 | 68.9 |`
- **T1** `| CPU, borné noyau (7,79 G év/s) | 44.93 | 22.3 |`
- **T1** `cache : 183999808.9 G événements/s mesurés contre 0.35 G nécessaires par token.`
- **T1** `3. **Une carte FPGA ≈ ce CPU** (23 contre 22 tok/s) : le CPU a`
- **T1** `3× la bande passante (28,7 contre 9,66 Go/s) mais il est limité par sa`
- **T2** `| DSP 18×18 | **[à vérifier]** (ordre de 1 000+) | non utilisé par les kernels « zéro DSP » |`
- **T2** `> ⚠️ **Correction d'une erreur fréquente** : les chiffres « ~622 000 ALM / 2 567 M20K / 66`
- **T2** `> `device/5SGSKF40I3LNAC.md`) ne correspondent **pas** au D5. Le D5 = 172 600 ALM, 1 963 M20K.`
- **T2** `**Conséquence directe** : 4,9 Mo de RAM embarquée = ~19,6 M poids en 2 bits. Tout modèle ou`
- **T2** `| DDR3 | **4 Go**, DIMM 240 broches, **72 bits avec ECC**, 1600 MT/s | **9 662 Mo/s lecture / 7 816 Mo/s écriture** (mesuré, [blog part 6](https://j-marjanovic.io/stratix-v-accelerator-card-from-ebay-`
- **T2** `| PCIe | Connecteur x16, **2 Hard IP PCIe Gen3 x8 distincts** (pièce custom) | **6,5 Go/s par interface**, **11–12 Go/s** avec les deux ([blog part 8](https://j-marjanovic.io/stratix-v-accelerator-car`
- **T2** `| Réseau | **2 × QSFP+ 40GbE** (SFF-8436) | 40GBASE-CR4/SR4 = **4 voies × 10,3125 Gbps** par port, ≈ 5 Go/s brut, ≈ 4,8 Go/s utiles |`
- **T2** `| `CLK_125M` | `PIN_M23` | 125 MHz | horloge générale |`
- **T2** `| `CLK_PCIE1` | `PIN_AF6/AF5` | 100 MHz (période 10 ns) | refclk Hard IP PCIe n°1 |`
- **T2** `| `CLK_PCIE2` | `PIN_AF34/AF35` | 100 MHz | refclk Hard IP PCIe n°2 |`
- **T2** `| `CLK_QSFP_OSC` | `PIN_T7/T6` | **644,53125 MHz** (période 1,551 ns) | **refclk des transceivers 40G** |`
- **T2** `> Le 644,53125 MHz est la refclk standard du 10,3125 Gbps : la chaîne QSFP+ dispose donc`
- **T2** `docs/carte-storey-peak.md-15-| Die de référence | `5SGSMD5` (D5), boîtier F40 (1517-FBGA, 40×40 mm), température industrielle |`
- **T2** `docs/carte-storey-peak.md-17-| Format | 111 mm × 168 mm, hauteur pleine, demi-longueur, **refroidissement actif obligatoire** |`
- **T2** `docs/carte-storey-peak.md-46-| DDR3 | **4 Go**, DIMM 240 broches, **72 bits avec ECC**, 1600 MT/s | **9 662 Mo/s lecture / 7 816 Mo/s écriture** (mesuré, [blog part 6](https://j-marjanovic.io/stratix-`
- **T2** `docs/carte-storey-peak.md-47-| PCIe | Connecteur x16, **2 Hard IP PCIe Gen3 x8 distincts** (pièce custom) | **6,5 Go/s par interface**, **11–12 Go/s** avec les deux ([blog part 8](https://j-marjanovic`
- **T2** `docs/carte-storey-peak.md:48:| Réseau | **2 × QSFP+ 40GbE** (SFF-8436) | 40GBASE-CR4/SR4 = **4 voies × 10,3125 Gbps** par port, ≈ 5 Go/s brut, ≈ 4,8 Go/s utiles |`
- **T2** `docs/carte-storey-peak.md-57-| `CLK_125M` | `PIN_M23` | 125 MHz | horloge générale |`
- **T2** `docs/carte-storey-peak.md-58-| `CLK_PCIE1` | `PIN_AF6/AF5` | 100 MHz (période 10 ns) | refclk Hard IP PCIe n°1 |`
- **T2** `docs/carte-storey-peak.md-59-| `CLK_PCIE2` | `PIN_AF34/AF35` | 100 MHz | refclk Hard IP PCIe n°2 |`
- **T2** `docs/carte-storey-peak.md:60:| `CLK_QSFP_OSC` | `PIN_T7/T6` | **644,53125 MHz** (période 1,551 ns) | **refclk des transceivers 40G** |`
- **T2** `docs/carte-storey-peak.md:62:> Le 644,53125 MHz est la refclk standard du 10,3125 Gbps : la chaîne QSFP+ dispose donc`
- **T2** `docs/carte-storey-peak.md-104-| BAR | Region 0 = **256 Mo**, Region 2 = 1 Ko |`
- **T2** `docs/multicartes.md-55-| NVLink (GPU0↔GPU1) | **25,781 Go/s par lien**, 1 lien par GPU | **mesuré** (`nvidia-smi nvlink -s`) |`
- **T2** `docs/multicartes.md-56-| PCIe Gen3 ×16 | ≈ 12–13 Go/s utiles | |`
- **T2** `docs/multicartes.md-57-| PCIe Gen3 ×8 (carte FPGA) | **6,5 Go/s** | mesuré par Jan Marjanovic |`
- **T2** `docs/multicartes.md:58:| QSFP+ 40GbE | ≈ 4,8 Go/s utiles | |`
- **T2** `docs/multicartes.md:60:**Hiérarchie réelle : NVLink > PCIe ×16 > QSFP+ 40G ≈ PCIe ×8.**`
- **T2** `docs/multicartes.md-62-débit (4,8 < 6,5 Go/s) — il n'a de sens que **pour des cartes déportées**, ou comme banc`
- **T2** `docs/multicartes.md-78-  (13 Go/s agrégés) plutôt que le 40G.`
- **T2** `docs/multicartes.md:86:- Refclk disponible : `CLK_QSFP_OSC` = **644,53125 MHz** (période 1,551 ns, `PIN_T7/T6`).`
- **T2** `- **CPU2** (bus `9f`–`ff`, NUMA node 1) : les 2 slots ×16 pour les cartes FPGA.`
- **T2** `- Les GPU sont sur le node 0 → tout échange GPU↔FPGA traverse le QPI (≈ 2×16 GT/s).`
- **T2** `- La carte consomme **x8** (un Hard IP) — le port amont du slot est ×16.`
- **T2** `- Sans bifurcation : **1 endpoint x8 par carte = 6,5 Go/s par carte** (mesuré).`
- **T2** `| 1 carte | Slot1_CPU2 | 6,5 Go/s | état actuel |`
- **T2** `| **2 cartes** | Slot1_CPU2 + Slot2_CPU2 | **13 Go/s** | recommandé, aucun compromis |`
- **T2** `| 3 cartes | + Slot3 (x4 Gen2) | 13 + 2 Go/s | la 3ᵉ carte est bridée à ×4 |`
- **T2** `| 4 cartes | riser PLX PEX8747 | 13 + partagé | l'upstream ×16 du riser (≈ 15,75 Go/s) devient le goulot |`
- **T2** `> slot ×16. Vérifier que ses slots aval sont **câblés ×16** (beaucoup ne le sont qu'en ×8),`
- **T2** `| NVLink (GPU0↔GPU1) | **25,781 Go/s par lien**, 1 lien par GPU | **mesuré** (`nvidia-smi nvlink -s`) |`
- **T2** `| PCIe Gen3 ×16 | ≈ 12–13 Go/s utiles | |`
- **T2** `| PCIe Gen3 ×8 (carte FPGA) | **6,5 Go/s** | mesuré par Jan Marjanovic |`
- **T2** `| QSFP+ 40GbE | ≈ 4,8 Go/s utiles | |`
- **T2** `**Hiérarchie réelle : NVLink > PCIe ×16 > QSFP+ 40G ≈ PCIe ×8.**`
- **T2** `débit (4,8 < 6,5 Go/s) — il n'a de sens que **pour des cartes déportées**, ou comme banc`
- **T2** `(13 Go/s agrégés) plutôt que le 40G.`
- **T2** `(accumulateur, 4096 × 24 bits = **12 Kio**, tient dans les M20K) ;`
- **T2** `- bande passante lecture séquentielle : **11.5 Go/s**`
- **T2** `- dispersion (`np.bincount`) : **183999808.87 G événements/s**`
- **T2** `- dispersion (`np.add.at`) : 364797216.41 G événements/s`
- **T2** `| Lecture séquentielle | 4,1 Go/s | 23,4 | **28,7** | 28,2 |`
- **T2** `| Dispersion pure | 0,96 G év/s | 3,46 | 3,20 | 3,22 |`
- **T2** `## Projection 7B (densité 5 %, 0,476 b/poids)`
- **T2** `Le débit varie de **0,011 ms à 0,95 ms sur la même matrice** (rapport 86) selon ce`
- **T2** `## Montée en charge (meilleur de 3 passes, densité 100 %)`
- **T2** `➡️ **~0,15–0,18 G év/s par thread**, optimum vers 28–32 threads, soit ~0,8–1,3`
- **T2** `événement par cycle CPU. Une carte à 124 MHz × 32 PEs = 4 G év/s vise donc`
- **T2** `> Mesures prises avec le bureau actif (load ~1,5–5) : ±20 % d'une passe à l'autre,`
- **T2** `La première campagne annonçait « fusion DIVERGENTE au rang 0 : 3838 vs 3513 » et un`
- **T2** `chemin 2-listes à 7,53 G év/s. **Les deux chiffres étaient faux.** Le chemin`
- **T3** `attention locale (fenêtre 256), un **FFN creux routé** (8 experts, top-2, k-WTA 25 %), **3 têtes précoces**`
- **T3** `//! | VRAM (noyau warp) | 84,9 Go/s |`
- **T3** `//! | RAM, 20 cœurs physiques | 22,5 Go/s |`
- **T3** `//! | RAM, 10 cœurs + leurs hyperthreads | 18,7 Go/s (+27 % sur 10 cœurs secs) |`
- **T3** `//! | RAM, 20 cœurs + hyperthreads | 18,9 Go/s — **rien de plus** |`
- **T3** `//! | NVMe, 1 lecteur | 5,4 Go/s |`
- **T3** `//! | **NVMe, 16 lecteurs** | **31,1 Go/s** |`
- **T3** `/// deux fils d'une même paire partagent L1 et L2, ce qui vaut +27 % quand`
- **T3** `/// Liens NVLink actifs : 25,8 Go/s sur cette machine, soit 2× le PCIe.`
- **T3** `//! | VRAM | 84,9 Go/s | le KV au-delà de ~2-4 k jetons, l'attention, la tête |`
- **T3** `//! | RAM | 22,5 Go/s | les poids (mmap, non copiés), le KV court |`
- **T3** `//! | NVMe | 3,5 Go/s | les poids qui ne tiennent pas en RAM (streaming) |`
- **T3** `//! mesure du 24/10 valide la première ligne : le KV en VRAM donne ×1,93 sur le`
- **T3** `//! préremplissage à 8 k et ×5,8 sur l'attention.`
- **T3** `198:   30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T3** `250:[N0/N1] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T3** `docs/pilotage/roadmap.md:198:   30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.m`
- **T3** `[still running after 60000ms; moved to background job bash-26]`
- **T5** `defaut  médiane   87.0 ms  (CV 1 %)`
- **T5** `bloque  médiane   86.4 ms  (CV 14 %)`
- **T5** `[s/v7 20648db7] N3.7 — LES VARIANTES SONT UN CONTRAT : SUBSTITUTION 4,768e-07 ≤ 1e-4 · CONTRÔLE NÉGATIF 5,790e-03 > 1e-4 · COÛT 87,0/86,4 ms (0,99×)`
- **T5** `20648db7 N3.7 — LES VARIANTES SONT UN CONTRAT : SUBSTITUTION 4,768e-07 ≤ 1e-4 · CONTRÔLE NÉGATIF 5,790e-03 > 1e-4 · COÛT 87,0/86,4 ms (0,99×)`
- **T5** `./reports/rapport-natif-numpy.md:7:> **Le chiffre.** `tools/drvm_infere.py` charge les **127 tenseurs** du DRVM (130,9 Mo) en`
- **T5** `defaut  médiane   85.9 ms  (CV 2 %)`
- **T5** `bloque  médiane   84.1 ms  (CV 5 %)`
- **T5** `defaut  médiane   85.1 ms  (CV 2 %)`
- **T5** `bloque  médiane   84.5 ms  (CV 11 %)`
- **T6** `defaut  médiane   83.6 ms  (CV 4 %)`
- **T6** `court   médiane   55.9 ms  (CV 4 %)`
- **T6** `defaut  médiane   83.9 ms  min   78.0  CV 3 %`
- **T6** `court   médiane   56.1 ms  min   51.3  CV 3 %`
- **T6** `defaut  médiane   80.8 ms  (CV 3 %)`
- **T6** `court   médiane   56.0 ms  (CV 6 %)`
- **T6** `[s/v7 de967b7b] N3.10 — `COURT` : LE PREMIER PROFIL QUI PAIE — BIT-EXACT < 64 o · 3,633e-02 AU-DELÀ · 0,694× LE TEMPS · SUR LE 34 M PPL 23,7480 → 23,5824 ET ~5 %`
- **T6** `de967b7b N3.10 — `COURT` : LE PREMIER PROFIL QUI PAIE — BIT-EXACT < 64 o · 3,633e-02 AU-DELÀ · 0,694× LE TEMPS · SUR LE 34 M PPL 23,7480 → 23,5824 ET ~5 %`
- **T6** `0, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T6** `1, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T6** `index_add         2.66 ms  →  25.22 G év/s`
- **T6** `bancs_b1          2.69 ms  →  24.91 G év/s`
- **T6** `bancs_b4          2.54 ms  →  26.40 G év/s`
- **T6** `bancs_b16         2.47 ms  →  27.15 G év/s`
- … (tronqué)

## 5. Erreurs rencontrées

26 sorties en erreur ou divergentes. Les premières :

- **T4** : pre-commit === hook contenu === --- .git/hooks/pre-commit #!/bin/sh # pre-commit — l'état accompagne le fait, le journal accompagne le code. # # Versionné dans tools/hooks/ et installé par tools/insta
- **T4** : |            ^^^^^^^^  warning: the `ids:` in this pattern is redundant     --> src/main.rs:1751:9      | 1751 |         ids: mut ids, ids_file, prompt, n: n_new, temp, top_p, topk, rep_pen, hist,    
- **T4** : -rwxr-xr-x. 2 stephane stephane 3218824 17 nov 11:14 drave-core/target/release/drave DRVM v0 · 6 blocs · 30 tenseurs · payload 31488 o   bloc input        input   bloc b0           local_mixer [stderr
- **T5** : ... 110 |     pub fn est_vide(&self) -> bool { self.lignes.is_empty() } 400 | pub fn existe(chemin: &str) -> bool { Path::new(chemin).is_file() } 187 | impl Episodique { ... 193 |     pub fn est_vide(
- **T5** : ok ---- tests_vars::les_vars_lues_sont_completes stdout ----  thread 'tests_vars::les_vars_lues_sont_completes' (3595551) panicked at src/main.rs:9068:13: DRAVE_NATIVE_PROFONDEUR est lu dans le source
- **T8** : [stderr] Traceback (most recent call last):   File "<stdin>", line 3, in <module>   File "<stdin>", line 3, in <lambda> ValueError: invalid literal for int() with base 10: 'n' [exit code: 1]
- **T9** : work/n2ac/mix1024-100m.drvm work/n2ac/mix1024-100m.pt work/n2ac/mix1024-100m.pt.json === json du pt === {  "modele": "drave-n0",  "parametres": 73366568,  "corpus": "data/wiki_mix/propre/train.txt",  
- **T9** : pas 3900 · perte 1.1655 · PPL val 3.510 · 1087 s pas 3950 · perte 1.2692 · PPL val 3.505 · 1101 s [exit code: 2]
- **T9** : mer 18 nov 2026 12:21:56 EST pas 5700 · perte 1.0961 · PPL val 3.286 · 1687 s passe: 71 vertes, 2 rouges   porte-prechargement    ✅                         163 s    PORTE TENUE [exit code: 2]
- **T9** : mer 18 nov 2026 12:41:28 EST [stderr] Traceback (most recent call last):   File "<string>", line 3, in <module>     d=json.load(open('work/n3/r4.pt.json')); print('r4 FINI ppl_val', round(d['ppl_val']
- **T10** : --> src/placement.rs:52:12    --> src/placement.rs:117:11    --> src/placement.rs:119:11    --> src/placement.rs:122:11    --> src/placement.rs:124:11    --> src/placement.rs:127:11 --- src/main.rs:83
- **T11** : tests_vars::les_vars_lues_sont_completes --- FAILED ....... failures:  ---- tests_vars::les_vars_lues_sont_completes stdout ----  thread 'tests_vars::les_vars_lues_sont_completes' (1181902) panicked a
- **T18** : mer 18 nov 2026 18:29:18 EST pas 9200 · perte 1.2103 · PPL val 3.676 · 3904 s · échelle 1048576 pas 9250 · perte 1.2407 · PPL val 3.680 · 3925 s · échelle 1048576 === bancs === [exit code: 2]
- **T18** : mer 18 nov 2026 22:56:58 EST pas 9200 · perte 1.0393 · PPL val 3.169 [exit code: 2]
- **T18** : mer 18 nov 2026 23:24:22 EST [exit code: 1]

## 6. Commits

- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -F - <<'MSG' 2>&1 | tail -15 DRVM — LE LECTEUR REFUSE CE QU'IL N'EXÉCUTE PAS : routes/régions/t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -F - <<'MSG' 2>&1 | tail -8 N3.7 — LES VARIANTES SONT UN CONTRAT : SUBSTITUTION 4,768e-07 ≤ 1e-
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/drvm.py tools/drvm_infere.py tools/drave.py tools/porte-n3-variante.sh reports/rapport-n3-va
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/drvm.py drave-core/src/drvm.rs drave-core/src/native.rs drave-core/src/main.rs tools/drvm_in
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/porte-n3-moteurs.sh reports/rapport-n3-moteurs.md docs/pilotage/en-cours.md docs/pilotage/ro
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/drvm.py drave-core/src/drvm.rs drave-core/src/native.rs tools/porte-n3-court.sh reports/rapp
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/backlog/A5.4-fpga.md docs/pilotage/roadmap.md docs/pilotage/en-cours.md && git commi
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add bench/gpu_scatter.py reports/rapport-gpu-scatter.md reports/gpu-scatter.json docs/pilotage/backlog
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('drave-core/src/main.rs'); s = p.read_text() old = "    /
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add bench/drvm_profils.py reports/rapport-profils-modele.md reports/profils-34m.json docs/pilotage/en-
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/drvm.py tools/drvm_infere.py tools/porte-n3-moteurs.sh tools/porte-n3-court.sh reports/rappo
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/backlog/N3-operations-natives.md docs/pilotage/en-cours.md && git commit -F - <<'MSG
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add bench/gpu_scatter.py reports/rapport-gpu-scatter-grille.md reports/rapport-profils-5-modeles.md re
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/references-non-regression.md docs/pilotage/en-cours.md && git commit -F - <<'MSG' 2>
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/banc_generation.py tools/chantier/plan.json reports/banc-generation-100m.json reports/banc-g
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/epingle_corpus.py reports/corpus-epingle.json reports/rapport-corpus-epingle.md docs/pilotag
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() old = '| 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() old = '| 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add reports/rapport-tagger-lot-612-prep.md reports/tagger-612-dryrun-5.json reports/rapport-donnees-in
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- ÉTAT — LA PUCE N4 SOUS 80 MOTS (LE DÉTAIL EST DANS LES QUATRE FICHES)" && git log -1 --format='%h %s' | cat
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/roadmap.md docs/pilotage/en-cours.md && git commit -q -F - <<'MSG' && git log -1 --f
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/dedup_blocs.py reports/rapport-dedup-blocs.md reports/dedup-blocs-7.5go.json docs/pilotage/e
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add reports/rapport-tagger-612.md reports/tagger-612-api.json reports/rapport-courbe-r1-r3.md reports/
- README — CE QUI EST FAIT PASSE AU 18/11 : LE CONTRAT DRVM, LE TAGGER 0,9572, LE CORPUS ÉPINGLÉ, LA COURBE DU 73 M, A2.6 ET P1 ; LE FPGA RESTE P2 + RTL" && git l
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- ÉTAT — LA PUCE N4 SOUS 80 MOTS (LE DÉTAIL EST DANS LES QUATRE FICHES)" && echo ok; date; python3 -c " import json try:     d=json.load(open('work/n3/r4.pt.json'
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() debut = s
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/references-non-regression.md docs/pilotage/en-cours.md && git commit -q -F - <<'MSG'
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add reports/rapport-courbe-r1-r3.md reports/rapport-v2-slice.md reports/banc-generation-r5a.json repor
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add AGENTS.md README.md docs/README.md reports/README.md docs/pilotage/roadmap.md docs/pilotage/refere
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() old = "| 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() old = "[c
- ÉTAT — LA PUCE N REPASSE SOUS LE BUDGET T0 (4 000 MOTS EXACTEMENT)" && git push origin s/v7 2>&1 | tail -1
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('reports/rapport-a2.6-bande-experts.md'); s = p.read_text
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('reports/rapport-a2.6-bande-experts.md'); s = p.read_text
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/courbe_chaine.py reports/rapport-150m-lr.md reports/sonde-lr-150m.json docs/pilotage/en-cour
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/references-non-regression.md'); s = p.read
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/porte-a2.6-experts.sh reports/rapport-a2.6-bande-experts.md docs/pilotage/en-cours.md && git
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/backlog/A2.6-ordonnanceur.md docs/pilotage/en-cours.md && git commit -q -F - <<'MSG'
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -q -F - <<'MSG' && git push origin s/v7 2>&1 | tail -1 && git log -1 --format='%h %s' | cat N —
- ÉTAT — LA PAGE VIVANTE PASSE AU 19/11 : LA NUIT DU PALIER 1 (v1 2,844 · v2 3,038 · 91 PORTES, 89/2 · CORPUS V2 ÉPINGLÉ)" && git push origin s/v7 2>&1 | tail -1;
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() old = "le
- ÉTAT — LA PUCE N REPASSE SOUS LE BUDGET T0" && git push origin s/v7 2>&1 | tail -1
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- ÉTAT — LA PUCE N REPASSE SOUS LE BUDGET T0" && git push origin s/v7 2>&1 | tail -1
- ÉTAT — T0 À 4 000 (LA PUCE N SE RESSERRE)" && git push origin s/v7 2>&1 | tail -1; date
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('reports/rapport-nettoyage-corpus.md'); s = p.read_text()
- ÉTAT — T0 REPASSE SOUS 4 000 (PUCE N RESSERRÉE)" && git push origin s/v7 2>&1 | tail -1
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('reports/rapport-diversite-sources.md'); s = p.read_text(
- ÉTAT — DIVERSITÉ BLOQUÉE, T0 REPASSÉ (COMPTEURS JSON À LA CLÔTURE DES RUNS)" && git push origin s/v7 2>&1 | tail -1; date
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- N — LES BANCS DES VARIANTES ENTRENT (cl1, cl2, rf1) : COMPTEURS À 963 JSON" && git push origin s/v7 2>&1 | tail -1
- N — LE TEST À TROIS A SES POINTS INTERMÉDIAIRES : À 20 000 PAS, LE NETTOYÉ EST À +0,6 % DE PPL DU BRUT" && git push origin s/v7 2>&1 | tail -1
- ÉTAT — T0 REPASSÉ" && git push origin s/v7 2>&1 | tail -1
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | grep "T0 max"; python3 - <<'PY' import pathlib p = pathlib.Path('
- ÉTAT — T0 REPASSÉ (PUCE N RESSERRÉE)" && git push origin s/v7 2>&1 | tail -1; date
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- ÉTAT — T0 REPASSÉ APRÈS LE VERDICT DU TEST À TROIS" && git push origin s/v7 2>&1 | tail -1; date
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('reports/rapport-a2.6-branchement.md'); s = p.read_text()
- ÉTAT — T0 REPASSÉ (A2.6 : LA DÉCISION EST BRANCHÉE)" && git push origin s/v7 2>&1 | tail -1; date
- ÉTAT — T0 À 3 997" && git push origin s/v7 2>&1 | tail -1
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add reports/rapport-selection-contenu.md reports/ppl-wikitext2.json reports/corpus-epingle-wikibig.jso
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -1; python3 tools/revue_documentation.py 2>&1 | tail -1; git
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cp work/n4/nuit.sh bench/chaine_nuit.sh && git add drave-core/src/model.rs drave-core/src/materiel.rs tool
- N — LA NUIT, TRANCHE 1 : wiki_big 8,86 SUR WIKITEXT2 (PPL v1 3,53) CONTRE 9,94 POUR LE LONG-FORME (3,67) ; LA COURBE SAIT LIRE WIKITEXT2" && git push origin s/v
- N — LA NUIT, TRANCHE 1 : wiki_big 8,86 SUR WIKITEXT2 (PPL v1 3,53) CONTRE 9,94 POUR LE LONG-FORME (3,67) ; LA COURBE SAIT LIRE WIKITEXT2" && git push origin s/v
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add reports/rapport-selection-contenu.md reports/banc-generation-nb2.json reports/banc-generation-nl2.
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && n=$(ls reports/*.json | wc -l); echo "JSON: $n"; python3 - "$n" <<'PY' import pathlib, sys n = sys.argv[1]
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && n=$(ls reports/*.json | wc -l); python3 - "$n" <<'PY' import pathlib, sys n = sys.argv[1] p = pathlib.Path
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && n=$(ls reports/*.json | wc -l); python3 - "$n" <<'PY' import pathlib, sys n = sys.argv[1] p = pathlib.Path
- ÉTAT — LA FICHE DE LA NUIT COMPTE (814 FICHES)" && git push origin s/v7 2>&1 | tail -1; date
- ÉTAT — LA PAGE VIVANTE PASSE AU 20/11 (LA NUIT wiki_big)" && git push origin s/v7 2>&1 | tail -1; date
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add reports/rapport-nuit-wikibig.md reports/banc-generation-nb11.json reports/banc-grammaticalite-nb11
- PASSE DE CLÔTURE — 91 PORTES, 89 VERTES, 2 ROUGES (LES DEUX STRUCTURELLES), MACHINE AU REPOS" && git push origin s/v7 2>&1 | tail -1; date
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/en-cours.md journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md && git com
- S — LA PROFONDEUR ENTRE DANS LA BANQUE : 324/369 CANDIDATS APPARIÉS, 95 À PROFONDEUR ≥ 3 (MIGRATION NON DESTRUCTIVE, LES 150 VERDICTS INTACTS)" && git push orig
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && n=$(ls reports/*.json | wc -l); python3 - "$n" <<'PY' import pathlib, sys n = sys.argv[1] p = pathlib.Path
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > reports/rapport-corpus-palier1.md <<'MD' # Le corpus du palier 1 : les résumés Wikipédia, 3,69 Go à 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > reports/rapport-s-retro-traduction.md <<'MD' # S — La rétro-traduction existe : 9/9 paragraphes trad
- S — LA RÉTRO-TRADUCTION : LE SCRIPT (9 PARAGRAPHES, 39 PAIRES, 18 ACCORDS DE CLASSE) ET SON TÉMOIN SANS API" && git push origin master 2>&1 | tail -1; cd ../.. 
- S — LA LIGNE DE ROADMAP DIT CE QUI EST FAIT : LA MIGRATION / v7 (324/369) ET LA RÉTRO-TRADUCTION (9/9, ALIGNEMENT À RAFFINER)" && git push origin s/v7 2>&1 | ta
- S — LA LIGNE DE ROADMAP DIT CE QUI EST FAIT : LA MIGRATION / v7 (324/369) ET LA RÉTRO-TRADUCTION (9/9, ALIGNEMENT À RAFFINER) ; L'ÉTAT PASSE AU 20/11 09 H 58" &
- S — LA LIGNE DE ROADMAP DIT CE QUI EST FAIT (MIGRATION / v7 324/369, RÉTRO-TRADUCTION 9/9) ; L'ÉTAT AJOUTE CES FAITS À SON EN-TÊTE" && git push origin s/v7 2>&1
- S — RÉTRO-TRADUCTION v2 : LES ANAPHORES NUMÉROTÉES PAR L'ANALYSEUR (LE MODÈLE LES REND DANS L'ORDRE)" && git push origin master 2>&1 | tail -1
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() old = '| 
- S — LE GOLD MESURÉ PAR LE SCRIPT : 14/14 (12 RÉFÉRENTS + 2 NON-RÉFÉRENTS), L'APPARIEMENT PAR FORME ET OCCURRENCE" && git push origin master 2>&1 | tail -1; cd .
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() def rep(o

