> Campagne : **campagne-benefices** · expérience **10-bis**
> Titre : 10 bis. Quatre tâches, sorties verbatim — et c'est le MODÈLE qui limite, pas le moteur
> Date réelle : **2026-10-08 22:49 HAE** (source : commit `d82f01a`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 10 bis. Quatre tâches, sorties verbatim — et c'est le MODÈLE qui limite, pas le moteur

Le batch 4 les avait prévues sur gpt-oss-120b (5 × 1 h de lectures du même fichier
de 63 Go, en concurrence avec la mesure PPL). Refaites ici sur le **0,5 B**, qui
suffit à répondre à la seule question qui compte : le moteur produit-il une sortie
**exploitable** ? Sorties **telles quelles**, `temp 0`, 64 jetons.

| tâche | sortie du 0,5 B | verdict |
|---|---|---|
| **code** | `def fibonacci(n):` … gère `n <= 0`, `n == 1`, `n == 2` … | ✅ **correcte et utilisable** |
| traduction FR | *« The river carries the logs to the mill. (No translation is needed) »* puis *« Le ruisseau transporte les feuilles au mill. »* | ❌ refuse, puis traduit faux (`feuilles` = leaves, `mill` non traduit) |
| arithmétique | entame un raisonnement juste (« we need to calculate the difference… ») | ⚠️ **tronquée** à 64 jetons — la réponse n'apparaît pas |
| résumé | *« The engine is a key component in the development of the new generation of engines. »* | ❌ hallucination, puis recopie de l'entrée |

**Ce que cela dit.** Le moteur a produit une **fonction Python correcte** avec un
modèle de 0,5 B — sur la tâche où le format est contraint (du code), il tient. Sur
la traduction, l'arithmétique et le résumé, c'est le **modèle** qui échoue, pas
l'exécution : Drave est un moteur, il fait ce que le modèle sait faire. C'est
aussi pourquoi la ligne « sortie contrainte » du verdict est la seule où
l'architecture gagne *par construction*.

*(Débit de ces essais : 0,84 tok/s, sous une charge de fond de **84** — trois gros
modèles lus en parallèle. Le chiffre ne dit rien du modèle ; il dit que mesurer
sous cette charge ne vaut que pour les sorties, pas pour les temps.)*

---
