# Session da69b1fa — Tu travailles dans le dépôt

| | |
|---|---|
| Identifiant | `da69b1fa-91b0-4c69-bb2b-58bf00e92e28` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-30 15:07 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 37 |
| Appels d'outils | 45 |
| Fichiers touchés | 1 |
| Commandes | 20 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM en Rust, `std` seul, binaire `drave`). Tout est en FRANÇAIS : écris en français.  CONTEXTE : le moteur sait faire tourner un modèle découpé sur deux machines qui se passent des « listes d'activation » (le cœur du projet). Le protocole de flux est en **version 4** et a quatre modes … [3874 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM e … [4154 caractères tronqués]

*45 appels d'outils.* Actions notables :

- read
- bash — Liste les points d'ancrage dans main.rs
- bash — Repère les fonctions modèle utiles
- bash — Liste docs/reports et cherche le critère 3.5
- bash — Lit le début du rapport transport liste
- bash — Cherche les mentions du mode 4 et du critère
- bash — Lit la section blocs du rapport transport
- bash — Lit les tests flux existants
- bash — Repère les options et usages liés aux flux
- bash — Repère les options CLI et le compteur de trace
- bash — Vérifie flags de vérif, actifs(), options et flux_lot
- bash — Cherche l'aide CLI et la règle Colab
- bash — Cherche comment les ids sont fournis au banc
- bash — Vérifie le support de --ids-file
- … et 19 autres

**Synthèse produite :**

⏵ Spécification écrite et transmise ; vérification finale de l'état du dépôt.

La spécification est dans `docs/plan-mode4-lot-listes.md` (445 lignes) — seul fichier que j'ai touché. Aucune compilation, aucune exécution : le `drave` de la campagne (PID 656529) tourne toujours, je ne l'ai pas approché (`journal/README.md` était déjà modifié avant mon écriture, sa mtime le prouve).

**Résumé — décisions d'architecture et points ouverts**

1. Le mode 4 est le mode 2 répété par état dans un seul flux : `n` = nombre d'ÉTATS, en-tête 79 octets inchangé, échelle d'en-tête sans objet.
2. Chaque état est auto-délimité par un préfixe de 12 octets (`a_j · n_blocs_j · longueur_j`), puis les échelles f32 par bloc de 32, puis les paires d'`encoder_paires_blocs` — aucun encodage réinventé.
3. L'échelle vit dans l'état, pas dans une table du lot : indépendance des états, dynamique par jeton, 112 octets sur ~1 530 ne justifient pas un second codec.
4. Le protocole passe en version 5, sinon un pair v4 consommerait `4·t` octets avant de dire « mode inconnu » ; le refus des modes inconnus devient immédiat, après l'en-tête.
5. Le corps n'étant plus borné par l'en-tête, `a_j·2`, `n_blocs_j·4`, `longueur_j` et leur cumul passent par `verifier_taille` avant chaque allocation, après `t·hidden·4` validé en tête.
6. Le mode 4 s'arrête au transport : `ChargeFlux::Lot`, `emb_imposee_lot`, `forward_lot`, le cache KV et la norme finale ne changent pas d'une ligne.
7. La réponse est encodée comme la demande ; le pilote norme chaque état une fois, puis `logits_lot`.
8. Critère de vérification : `écart(mode 4) ≤ 1,5 × écart(mode 2 par jeton)` (≈ 2,7e-2 à 256 jetons, seuil 0,01), jamais 0,00e0 — le mode est avec perte par décision, et ÷2,3 attendu sur le fil.
9. Laissé à l'implémenteur : la forme exacte des helpers `encoder_etat_blocs` / `lire_etat_blocs` et le portage de `Flux.actifs`.
10. Laissé à l'implémenteur : le seuil de bascule mode 3 ↔ mode 4 et la borne structurelle facultative du corps ; le plan en 7 étapes (§8) donne fichier et critère de succès pour chacune.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mode4-lot-listes.md` | 1 | 10 |

### Commandes exécutées (échantillon)

- **T1** Liste les points d'ancrage dans main.rs
- **T1** Repère les fonctions modèle utiles
- **T1** Liste docs/reports et cherche le critère 3.5
- **T1** Lit le début du rapport transport liste
- **T1** Cherche les mentions du mode 4 et du critère
- **T1** Lit la section blocs du rapport transport
- **T1** Lit les tests flux existants
- **T1** Repère les options et usages liés aux flux
- **T1** Repère les options CLI et le compteur de trace
- **T1** Vérifie flags de vérif, actifs(), options et flux_lot
- **T1** Cherche l'aide CLI et la règle Colab
- **T1** Cherche comment les ids sont fournis au banc
- **T1** Vérifie le support de --ids-file
- **T1** Cherche les invocations réelles du banc réparti
- **T1** Lit l'invocation de référence du banc réparti
- **T1** Vérifie les noms exacts des options et la ligne du cache KV
- **T1** Vérifie la ligne de KvCache::assurer
- **T1** Localise les passages à corriger
- **T1** Vérifie l'état git et les processus drave
- **T1** Vérifie l'ancienneté de la modif de journal/README.md

## 4. Mesures et résultats marquants

- **T1** `docs/plan-prefill-reparti.md:32:| la version change ? | **oui, 2 → 3** | un nœud v2 lirait `n×4` octets d'un corps qui en fait `n×hidden×4` avant de répondre « mode inconnu » : erreur exacte mais tard`
- **T1** `3 623** à seuil 5 %, et **1 568** avec des indices par écarts — mais jeter des`
- **T1** `canaux coûte cher (**×1,8 de perplexité** à ce seuil), et la courbe est là pour`
- **T1** `| dense f32 | 100 % | 3 623 | 3 623 | 144,8289 | **144,8289** | **0,00e0** |`
- **T1** `| listes 0,00 | 100,0 % (896) | 3 623 | 3 623 | 144,8289 | 141,0539 | 2,6e-2 |`
- **T1** `| listes 0,02 | 60,4 % (541) | 2 203 | 2 677 | 203,8033 | 213,7739 | 4,9e-2 |`
- **T1** `| listes 0,05 | 24,0 % (215) | 897 | 993 | 493,0344 | 893,1350 | 8,1e-1 |`
- **T1** `| listes 0,10 | 36,5 % (327) | 1 347 | 216 | 35 483,0643 | 66 813,6606 | 8,8e-1 |`
- **T1** `d'octets, pour une perte de 2,6 %. La valeur occupant 16 bits sur le fil, le`
- **T1** `3. **Jeter coûte cher, et pas linéairement.** À 0,02 (60 % d'activité) on a déjà`
- **T1** `perdu la fidélité (4,9e-2) ; à 0,05 (24 %) l'écart est ×1,8 ; à 0,10 la`
- **T1** `(19,3885), mais ici 16 bits coûtent 2,6 % : la différence n'est pas la précision,`
- **T1** `où le transport est exact, l'écart passe de 0,00e0 à 5,61e0** (perplexité 119`
- **T1** `docs/format-flux.md:117:f32 dense (3,5 ko par jeton) ; le lot en listes est le mode 4, pas encore écrit.`
- **T1** `reports/rapport-transport-liste.md:133:| blocs | 0,01 | 78,6 % | 2 268 | 2,7e-2 |`
- **T1** `| 2.2 | **Streaming des poids depuis le NVMe** (3,5 Go/s) pour ce qui ne tient pas en RAM — c'est la même idée : ne lire que ce qui parle | ⏳ | un modèle > RAM exécuté, débit mesuré |`
- **T1** `| 2.3 | **Cache d'experts rentable** : +6 % aujourd'hui ; grouper les trois projections par expert et supprimer les copies | ⏳ | ≥ +30 %, sinon abandonné (et écrit) |`
- **T1** `| 3.2 | **Granularité** : par couche, par bloc de canaux, par expert | 🔬 | livrés et mesurés : listes i16, **échelles par bloc de 32 canaux (valeurs i8)** et **indices par écarts** — `--flux-blocs --a`
- **T1** `| 3.3 | **Seuil de rentabilité** : à partir de quel débit réseau le découpage gagne | 🔬 | mesuré jusqu'à 20 ms de latence par message (`tools/proxy_latence.py`) : **attente ≈ calcul distant + 3,2 × la`
- **T1** `| 3.4 | **Démonstration Colab** : préremplissage réparti (le décodage reste séquentiel — c'est écrit dans la vision) | 🔬 | **le préremplissage par lots sur le fil est FAIT et fidèle** (mode 3 : 256 je`
- **T1** `| 0,00 | 98,1 % | 2 793 | 7,1e-2 | 3 622 octets · 2,6e-2 |`
- **T1** `| 0,02 | 60,4 % | **1 778** | **2,2e-3** | 2 203 octets · 4,9e-2 |`
- **T1** `| 0,05 | 24,0 % | 799 | 1,1e0 | 897 octets · 8,1e-1 |`
- **T1** `**÷2,3 sur le fil pour 2,7 %** de perplexité.`
- **T1** `| dense f32 | — | 100 % | 3 623 | **0,00e0** |`
- **T1** `| blocs | 0,01 | 78,6 % | 2 268 | 2,7e-2 |`
- **T1** `| blocs | 0,02 | 59,2 % | 1 745 | 1,4e-1 |`
- **T1** `| listes i16 | 0,02 | 59,2 % | 2 159 | 1,6e-1 |`
- **T1** `toujours les listes à sparsité égale (1 745 contre 2 159 octets, et 14 % contre`
- **T1** `16 % d'écart) ; et l'écart dépend du **corpus** bien plus que du seuil — 0,2 % sur`
- **T1** `identifiants synthétiques à 40 jetons, 2,7 % sur du vrai texte à 256.`
- **T1** `| 64 | 1,37e-1 | 2 249 | 77,9 % |`
- **T1** `| 128 | 6,37e-2 | 2 257 | 78,2 % |`
- **T1** `| 256 | 2,74e-2 | 2 268 | 78,6 % |`
- **T1** `| **1 024** | **1,32e-2** | **1 589** | 79,8 % |`
- **T1** `ci-dessous — **÷2,3 sur le fil pour 1,3 % d'écart à 1 024 jetons** (2,7 % à 256,`
- **T1** `13,7 % à 64) (et 13,7 % d'écart à 64 jetons : sur une séquence courte,`
- **T1** `l'erreur est chère). Ni le « ÷2 pour 0,2 % » que j'avais tiré du banc`
- **T1** `// `n_blocs × 4` octets + un Vec<f32> (mesuré : 16 Gio sur une trame de`
- **T1** `// Défauts du mode PERPLEXITÉ : 256 jetons, trois quarts des cœurs, 16 bits`
- **T1** `/// rejouait la mauvaise — mesuré : perplexité 356 694 au lieu de 17,43.`
- **T1** `22:| quel encodage dans le lot ? | **listes à échelle par bloc de 32, valeurs i8 — le mode 2, tel quel** | c'est le mode qui gagne en régime creux (mesuré : ÷2,3 et 20× plus fidèle que l'i16 à 60 % d'`
- **T1** `308:  référence locale  : perplexité 18,0xxx          <- identique au run mode 3 à mêmes ids et --lot`

