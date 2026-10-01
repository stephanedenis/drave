# Sprint 09 — L'empreinte mémoire : ce qui réduit vraiment ce qu'il faut charger

- **Début** : 16:35 · **Fin prévue** : 18:35 (boxing de 120 min)
- **Objectif** : chiffrer ce qu'un MoE doit charger **avant d'opérer**, et écarter
  les pistes qui ne paient pas. Cible : DeepSeek-V4.1-Flash (365,7 Go) sur 125 Go.
- **Engagement de fin** : dépôt vert, mesures consignées, machine rendue.

## Le résultat

L'empreinte de V4.1 tombe de **365,7 Go à 50–80 Go** — et pas en découpant les
experts. En décomposant les poids par famille :

| famille | Go | % | à charger |
|---|---|---|---|
| **engram** | **203,4** | **55,6 %** | **0,4 Go** |
| experts | 152,9 | 41,8 % | 21–71 Go |
| attention, embeddings, tête | 10,0 | 2,7 % | 10 Go |

`blk.N.engram_embd.weight` : **101,4 Go par couche**, `[384 006 168, 264]` en I8.
Ce n'est **pas un tenseur de poids mais une table de hachage de n-grammes**
(jusqu'à 4 tokens, 48 nombres premiers de hâchage). Une session de 10 000 jetons
n'en touche que **17 276 entrées = 4,6 Mo** : **1 pour 22 000**.

C'est le cas d'usage exact du `mmap` — et la brique la plus simple de toutes,
puisqu'il n'y a même pas de LRU à écrire.

## Les pistes mesurées

| piste | verdict | chiffre |
|---|---|---|
| **engram mmappé** | **retenu** | 203 Go → 0,4 Go |
| **tête restreinte à la langue** | **retenu** | −30 % de trafic, top-1 à 99,2 % |
| **cache d'experts 25 %** | **retenu** | 80 % des appels en mémoire |
| découper sous l'expert | écarté | seuil 5 % → perplexité **×287** |
| grappes par langue | écarté | Jaccard 0,75–0,90 entre langues, réf. interne 0,805 |
| dictionnaire token → experts | écarté | Jaccard 0,06 aux couches médianes |
| pré-remplissage du cache | écarté | régime atteint en **32 jetons** |
| allocation du cache par couche | écarté | gain **+1,2 %** au mieux |
| localité temporelle | écarté | réutilisation 27–52 % (hasard 6,2 %), mais un LRU de 32 fait 78 % |
| ordre des experts dans le fichier | écarté | étendue 30–69 rangs ; lire par bloc coûterait 30–70 experts au lieu de 8 |
| préchargement | écarté | le calcul (0,6 ms) est **18× plus rapide** que la lecture (10,9 ms) |

## Deux structures trouvées en chemin

**Le miroir** : les couches extrêmes sont **4,6× plus liées au token** que les
médianes (Jaccard 0,259 contre 0,056). Mais les couches symétriques (0/47) ne
partagent rien (0,030) : le miroir est une propriété par couche, pas une
correspondance.

**Une périodicité de 12 couches** : Jaccard 0,323 à écart 12, 0,210 à écart 24,
**0,035 pour tout autre écart**. Quatre blocs de 12 couches réutilisent les mêmes
experts. Aucune économie de stockage directe — ce sont des tenseurs différents —
mais un index 1,56× plus petit si on regroupe par bloc.

## Les mesures d'infrastructure

| support | débit |
|---|---|
| VRAM (2 GPU) | ~750 Go/s |
| RAM | ~20 Go/s |
| NVMe, aléatoire, blocs 4 Mo | **5,5 Go/s** |
| NVMe, séquentiel | 2,1 Go/s |
| disque mécanique, séquentiel | 0,21 Go/s |
| **disque mécanique, aléatoire** | **0,06 Go/s** — 3,5× pire |

**Le disque mécanique est disqualifié pour le chargement à la demande.**

## Rétrospective

- **Garder** : mesurer avant de conclure. Huit pistes ont été testées, trois ont
  survécu. Sans les mesures, les cinq autres auraient été implémentées.
- **Garder** : conserver les traces. Les 21 Mo de traces de cette session sont
  sur le NVMe et rejouables par `tools/analyse_empreinte.py`.
- **Changer** : trois fois un chiffre absurde a sauvé la conclusion (disque à
  2 211 Go/s, allocation à 4,1 %, total à 4 231 Go). C'est l'invraisemblance qui
  a alerté, pas le test. Un contrôle de plausibilité devrait être systématique.
- **Doute** : tout est mesuré sur Qwen3-30B (128 experts, top-8). L'extrapolation
  à V4.1 (384 experts, top-6) suppose la même concentration **relative**. Le
  rapport top-k/n_experts y est plus petit (1,6 % contre 6,25 %), ce qui devrait
  **aider** — mais ce n'est pas mesuré.
- **Doute** : l'engram n'est pas exécuté (pas de `forward` deepseek4). Le nombre
  de n-grammes touchés est calculé sur le texte, pas sur l'accès réel au tenseur.

## Planning

| # | chantier | critère de succès |
|---|---|---|
| 1 | Accès mmappé à l'engram | la table de 101 Go s'ouvre sans la charger, l'accès par n-gramme rend les bonnes lignes |
| 2 | Cache d'experts adossé au disque | 25 % d'empreinte → 80 % des appels servis |
| 3 | Tête restreinte par langue | −30 % de trafic, perplexité inchangée sur le vocabulaire complet |
| 4 | `forward` deepseek4 | la perplexité de V4-Flash égale celle de la référence llama.cpp |


## Revue — ce qui est livré, mesuré

Rapport [`reports/rapport-empreinte-memoire.md`](reports/rapport-empreinte-memoire.md),
outil [`tools/analyse_empreinte.py`](../tools/analyse_empreinte.py), traces
conservées sur le NVMe (21 Mo, rejouables).

**Onze pistes mesurées, trois retenues.** Le résultat principal n'était pas
attendu : l'engram pèse 55,6 % du modèle et n'est pas un tenseur de poids mais
une table creuse — 203 Go qui tombent à 0,4 Go chargés.

Durée : 68 min (boxing 120 min). Commits : 2.

## Rétrospective — garder / changer

- **Garder** : avoir cherché la décomposition des poids AVANT d'optimiser le
  découpage. Six tours ont été passés sur les experts (42 % du modèle) alors que
  le gisement était ailleurs (56 %).
- **Garder** : les trois absurdités qui ont alerté — disque mécanique à
  2 211 Go/s, allocation de cache à 4,1 %, total à 4 231 Go. Aucune n'a été
  détectée par un test, toutes par invraisemblance.
- **Changer** : vérifier le retour des appels système. `pread` sans contrôle a
  produit un chiffre faux d'un facteur 37 000.
- **Doute** : l'extrapolation à V4.1 suppose la même concentration relative, et
  l'engram n'est pas exécuté (pas de `forward`). Les deux sont signalés dans le
  rapport plutôt que lissés.

## Planning

Voir le tableau du sprint. Le premier chantier — l'accès mmappé à l'engram — est
le seul qui divise l'empreinte par 5, et c'est aussi le plus simple : pas de LRU,
le noyau fait le travail.
