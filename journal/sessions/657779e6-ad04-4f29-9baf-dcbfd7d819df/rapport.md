# Session 657779e6 — Dépôt /home/stephane/GitHub/Qtrinet, f

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `657779e6-ad04-4f29-9baf-dcbfd7d819df` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 18:48 |
| Durée | 0.8 h |
| Tours | 1 |
| Messages | 55 |
| Appels d'outils | 61 |
| Fichiers touchés | 2 |
| Commandes | 47 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Dépôt /home/stephane/GitHub/Qtrinet, fenêtre jusqu'à 2026-10-28 08:00 HAE. Sous-agent A18 : exécuter **une couche de modèle à distance** et vérifier la fidélité, sans modifier les modules existants.  Contexte : - A7.5 `tools/grappe_reseau.py` : transport TCP du flux sparse, 4,44× moins d'octets, fidélité 100 %, 0,125 ms loopback. - A7.4 : grappe top-1024 exacte à 21 %. - Modèle disponible : Qwen2. … [1669 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Dépôt /home/stephane/GitHub/Qtrinet, fenêtre jusqu'à 2026-10-28 08:00 HAE. Sous-agent A18 : exécuter **une couche de mod … [1949 caractères tronqués]

*61 appels d'outils.* Actions notables :

- bash — List tools directory and tests
- bash — Check GPU env and torch/transformers
- bash — Sizes of relevant files
- bash — Locate Qwen model in HF cache
- read
- bash — Introspect Qwen2 API signatures
- bash — Inspect Qwen cache snapshot and config
- bash — Print source of key Qwen2 methods
- bash — Check system python deps
- bash — Probe model forward kwargs and determinism
- bash — Prototype layer isolation exactness
- bash — Test sdpa/eager isolated layer exactness
- bash — Validate APIs and measure layer cost
- send_message
- … et 45 autres

**Synthèse produite :**

⏵ Clôture A18 : résultats, tests et chemins

\## A18 — Une couche de Qwen 0.5B exécutée à distance

**Livrables**
- `tools/couche_distante.py` — client + serveur TCP loopback ; la couche 12 est retirée du client et chargée seule côté serveur depuis `model.safetensors` (14,9 M params). Le client garde embeddings, 23 couches, norme et `lm_head`.
- `tools/cerveau/tests/test_couche_distante.py` — 24 tests (protocole, codecs dense/sparse, métriques), sans GPU.
- `/tmp/a18-couche-distante.json` et `/tmp/a18-couche-distante.md` — rapports du run final (3 invites de 18/60/28 jetons, 5 répétitions, GPU 0 fp32/sdpa).

**Fidélité**
- Logits **identiques au bit près** sur les 3 invites : écart max `0,0`, argmax/top-5/top-1024 = `1`, KL = `0`.
- PPL locale = distante = `7,1620667`, Δ = `0` ; 5/5 répétitions identiques ; hash des poids client/serveur identique.

**Transport et flux**
- Ping médian `0,178 ms` (A7.5 : `0,125 ms`) ; RTT de la couche `4,195 ms` dont `2,666 ms` de calcul serveur ; forward complet `57,5 ms` → la couche distante pèse `7,3 %`.
- `4105,1 o/jeton` (3584 hidden + 512 cos/sin + 8 position_ids + 38 en-tête), `1649,6 jetons/s`, `6,46 Mio/s`.
- Dense vs sparse : `1,027×` (sparse plus gros, `0 %` de zéros) ; le `4,44×` d'A7.5 concernait des activations creuses, pas l'état caché résiduel dense.
- Mémoire client : `−56,89 Mio` après libération de la couche.

**Contrôles négatifs**
- Positions RoPE zéro : écart `5,08`, ΔPPL `0,351`.
- CPU fp32/sdpa : `5,6e-5`, ΔPPL `−3e-6`.
- bfloat16 : `0,456`, ΔPPL `−0,002`.
- eager sans masque causal : `3,59`, ΔPPL `0,124`.
- Cache : non transféré (`use_cache=False`, prefill) ; KV estimé à `1 024 o/jeton/couche`, non mesuré.

**Tests** : suite complète `158 OK, 23 skipped` (24 nouveaux tests ; 134 hors notre fichier — la consigne en annonçait 132, 2 tests ont été ajoutés dans l'espace partagé).

**Contraintes** : seuls les deux fichiers ont été créés ; aucun module existant, doc, report, journal, `batterie.py` ni git modifié. Note de transparence : le fichier a reçu après mon premier run un contrôle `quant` int8 ajouté dans l'espace partagé ; j'ai relancé la version courante et les chiffres ci-dessus sont ceux du run final. Le JSON contient ce contrôle int8 (ratio `0,345×` mais écart logits `~26`, argmax `0` → non fidèle) ; le MD couvre dense/sparse et les négatifs demandés.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/couche_distante.py` | 1 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_couche_distante.py` | 1 | 1 |

### Commandes exécutées (échantillon)

- **T1** List tools directory and tests
- **T1** Check GPU env and torch/transformers
- **T1** Sizes of relevant files
- **T1** Locate Qwen model in HF cache
- **T1** Introspect Qwen2 API signatures
- **T1** Inspect Qwen cache snapshot and config
- **T1** Print source of key Qwen2 methods
- **T1** Check system python deps
- **T1** Probe model forward kwargs and determinism
- **T1** Prototype layer isolation exactness
- **T1** Test sdpa/eager isolated layer exactness
- **T1** Validate APIs and measure layer cost
- **T1** Compile and check header sizes
- **T1** Run main experiment end-to-end
- **T1** Rerun main experiment after batch fix
- **T1** Rerun main experiment after sparse fix
- **T1** Show partial markdown report
- **T1** Inspect partial JSON aggregates
- **T1** Run full experiment with negatives
- **T1** Show full markdown report
- **T1** Inspect negatives and server shutdown
- **T1** Run new tests alone
- **T1** Rerun new tests
- **T1** Run full unittest suite
- **T1** Count suite without new file
- **T1** Check report section and compile
- **T1** Regenerate final reports
- **T1** Check regenerated report sections
- **T1** Verify final JSON aggregates
- **T1** Final full suite and compile
- **T1** Extract final key figures
- **T1** Read network report section
- **T1** Compile and inspect edited section
- **T1** Final report regeneration
- **T1** Check final decomposition and verdict
- **T1** Final full suite
- **T1** Final key figures
- **T1** Check file structure for duplicates
- **T1** Check mtimes and quant additions
- **T1** Read current docstring and quant codec
- … et 7 autres

## 4. Mesures et résultats marquants

- **T1** `| 33%   30C    P8             20W /  230W |       1MiB /  16384MiB |      0%      Default |`
- **T1** `| 33%   28C    P8             16W /  230W |       1MiB /  16384MiB |      0%      Default |`
- **T1** `Loading weights:   0%|          | 0/290 [00:00<?, ?it/s]`
- **T1** `Loading weights:  58%|█████▊    | 167/290 [00:00<00:00, 1656.74it/s]`
- **T1** `Loading weights: 100%|██████████| 290/290 [00:00<00:00, 1736.64it/s]`
- **T1** `Loading weights:  59%|█████▉    | 172/290 [00:00<00:00, 1711.53it/s]`
- **T1** `Loading weights: 100%|██████████| 290/290 [00:00<00:00, 1754.85it/s]`
- **T1** `Loading weights:  59%|█████▉    | 171/290 [00:00<00:00, 1703.48it/s]`
- **T1** `Loading weights: 100%|██████████| 290/290 [00:00<00:00, 1693.34it/s]`
- **T1** `Loading weights:  57%|█████▋    | 166/290 [00:00<00:00, 1658.68it/s]`
- **T1** `Loading weights: 100%|██████████| 290/290 [00:00<00:00, 1687.49it/s]`
- **T1** `Loading weights:  59%|█████▉    | 171/290 [00:00<00:00, 1709.79it/s]`
- **T1** `Loading weights: 100%|██████████| 290/290 [00:00<00:00, 1669.79it/s]`
- **T1** `"conclusion": "Couche 12 exécutée dans un second processus : logits identiques au bit près sur les 3 invites ; ΔPPL corpus = +0. RTT couche médian 4.896 ms, 4105 o/jeton, 3629.7 jetons/s. Sparse/dense`
- **T1** `Agrégat : 435138 octets requête au total, 4105.08 o/jeton, RTT couche médian 4.896 ms, débit 3629.67 jetons/s (14.21 Mio/s), ping médian 0.1476 ms.`
- **T1** `Le flux résiduel est dense : taux de zéros moyen 0 %, ratio sparse/dense 1.027× (hidden seul 1.031×). Le masque de 1 bit par valeur coûte 1/32 des valeurs ; il ne paie que si les zéros dépassent ~3,1 `
- **T1** `Couche 12 exécutée dans un second processus : logits identiques au bit près sur les 3 invites ; ΔPPL corpus = +0. RTT couche médian 4.896 ms, 4105 o/jeton, 3629.7 jetons/s. Sparse/dense = 1.027×.`
- **T1** `Loading weights:  59%|█████▊    | 170/290 [00:00<00:00, 1699.66it/s]`
- **T1** `Loading weights: 100%|██████████| 290/290 [00:00<00:00, 1730.75it/s]`
- **T1** `"conclusion": "Couche 12 exécutée dans un second processus : logits identiques au bit près sur les 3 invites ; ΔPPL corpus = +0. RTT couche médian 3.613 ms, 4105 o/jeton, 1854.9 jetons/s. Sparse/dense`
- **T1** `Agrégat : 435138 octets requête au total, 4105.08 o/jeton, RTT couche médian 3.613 ms, débit 1854.91 jetons/s (7.262 Mio/s), ping médian 0.113 ms.`
- **T1** `Couche 12 exécutée dans un second processus : logits identiques au bit près sur les 3 invites ; ΔPPL corpus = +0. RTT couche médian 3.613 ms, 4105 o/jeton, 1854.9 jetons/s. Sparse/dense = 1.027×.`
- **T1** `Loading weights:  59%|█████▉    | 171/290 [00:00<00:00, 1700.31it/s]`
- **T1** `Loading weights: 100%|██████████| 290/290 [00:00<00:00, 1677.18it/s]`
- **T1** `"conclusion": "Couche 12 exécutée dans un second processus : logits identiques au bit près sur les 3 invites ; ΔPPL corpus = +0. RTT couche médian 5.524 ms, 4105 o/jeton, 1382.6 jetons/s. Sparse/dense`
- **T1** `Le top-1024 est ici l'intersection des 1024 plus grands logits par position. Ce n'est **pas** le taux d'exactitude de la grappe top-1024 d'A7.4 (21 %), qui portait sur une approximation de grappe : le`
- **T1** `f"ordre que le 0,125 ms d'A7.5 ; le RTT de la couche est dominé par le "`
- **T1** `Loading weights:  55%|█████▍    | 159/290 [00:00<00:00, 1581.26it/s]`
- **T1** `Loading weights: 100%|██████████| 290/290 [00:00<00:00, 1587.65it/s]`
- **T1** `"conclusion": "Couche 12 exécutée dans un second processus : logits identiques au bit près sur les 3 invites ; ΔPPL corpus = +0. RTT couche médian 5.185 ms, 4105 o/jeton, 1432.1 jetons/s. Sparse/dense`
- **T1** `34:Décomposition : le ping (transport seul) est 0.1097 ms, du même ordre que le 0,125 ms d'A7.5 ; le RTT de la couche est dominé par le calcul serveur (3.796 ms), pas par le réseau. La couche distante`
- **T1** `Couche 12 exécutée dans un second processus : logits identiques au bit près sur les 3 invites ; ΔPPL corpus = +0. RTT couche médian 5.185 ms, 4105 o/jeton, 1432.1 jetons/s. Sparse/dense = 1.027×.`
- **T1** `serait un coût supplémentaire (2 × 2 têtes KV × 64 × 4 o = 1 024 o/jeton/`
- **T1** `[still running after 60000ms; moved to background job bash-2799]`
- **T1** `34:Décomposition : le ping (transport seul) est 0.1779 ms, du même ordre que le 0,125 ms d'A7.5 ; le RTT de la couche est dominé par le calcul serveur (2.666 ms), pas par le réseau. La couche distante`

