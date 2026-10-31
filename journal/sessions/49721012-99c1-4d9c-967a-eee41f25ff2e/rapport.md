# Session 49721012 — Dépôt /home/stephane/GitHub/Qtrinet, s

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `49721012-99c1-4d9c-967a-eee41f25ff2e` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 12:11 |
| Durée | 0.6 h |
| Tours | 1 |
| Messages | 57 |
| Appels d'outils | 67 |
| Fichiers touchés | 2 |
| Commandes | 48 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Dépôt /home/stephane/GitHub/Qtrinet, sprint autonome 24 h. Sous-agent A11 : revisiter M7 après le négatif A2, sans toucher aux autres modules.  État A2 : - `tools/cerveau/neuromodulation.py` : `MemoireLimitee` (capacité 16), politiques FIFO/LRU/LFU/gel/… ; 30 permutations appariées. - 3,64 % = plafond 16/439 ; LFU +23,1 pts de répétés (30/30), +4,25 pts suffixe surface ; nouveauté −19,6, incertitu … [1474 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Dépôt /home/stephane/GitHub/Qtrinet, sprint autonome 24 h. Sous-agent A11 : revisiter M7 après le négatif A2, sans touch … [1754 caractères tronqués]

*67 appels d'outils.* Actions notables :

- bash — List repo root and cerveau directory
- bash — Check sizes of key files
- read
- bash — Run baseline cerveau tests
- bash — Inspect corpus counts and fields
- bash — Look for prior A2 artifacts
- bash — Read prior A2 report summary
- bash — Inspect A2 JSON structure
- bash — Inspect corpus feature distributions
- bash — Check prepared flux sizes and signals
- bash — Reproduce A2 baselines and oracle
- bash — Check working tree and test tail
- bash — Confirm insertion point at module end
- edit `/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py`
- … et 52 autres

**Synthèse produite :**

⏵ M7-bis terminé : résultats et artefacts livrés

**M7-bis `MemoireFrequence` — verdict**

- **LFU vs FIFO** : +4,25 pts de suffixe surface (27/30), +23,13 pts de répétés surface (30/30), +8,73 pts de nouveaux utiles (29/30) ; mais −0,67 pt sur les nouveaux du suffixe (0/30, non significatif). LFU reste à 9,28 % de suffixe surface contre 24,28 % pour l’oracle.
- **LFU + récence ne bat pas LFU** : identique sur la clé surface (0,00 pt, 0/30) — 0 éviction sans item de fréquence 1 sur 11 163 évictions, donc le départage ne s’exerce jamais ; sur la clé code, −0,06 pt de suffixe code (0/30, p=0,5), très légèrement pire.
- **Aucun contexte ne bat LFU** : meilleur cas `LFU + longueur` −0,06 pt (14/30, p=0,54) ; `jeu` −1,89 pt (0/30) ; `type` −1,95 pt (0/30). Les contextes purs perdent 7,4 à 8,5 pts de suffixe surface.
- **Contrôle clé permutée** : le contexte réel est pire que sa permutation pour `jeu` (−2,26 pts, p<0,001) et `type` (−1,95 pt, p<0,001) ; `longueur` est à égalité. Le contexte est un prior de groupe qui dilue la fréquence d’item.
- **Contrôles** : Zipf synthétique LFU vs FIFO +13,52 pts de suffixe code (14/15) et +4,34 pts surface (11/15) ; plafond 16/439 = 3,6446 % atteint partout ; β=0 redonne exactement LFU+récence.
- **Tests** : suite cerveau **123 OK, 19 skip** au dernier contrôle ; les 12 tests du fichier M7 passent.

**Chemins**
- `/tmp/a11-m7-lfu.json` — JSON complet (33 configurations × 30 permutations)
- `/tmp/a11-m7-lfu.md` — fiche détaillée, contrôles, limites
- `tools/cerveau/neuromodulation.py` — `MemoireFrequence`, `experience_m7_bis`, `controle_zipf_frequence`
- `tools/cerveau/tests/test_neuromodulation.py` — `TestMemoireFrequence`

**Coordination** : un autre agent a commité pendant la session (`59ad77f3` puis `86259771`, `c122f430`) ; je n’ai fait aucune écriture git. Le `reports/m7-frequence.*` commité ne contient pas les deux ajouts finaux (`ret_nouveaux_suffixe`, diagnostic `evictions`) présents dans mon JSON `/tmp` ; les deux dernières assertions de test sont non commitées (2 lignes, tests verts).

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py` | 0 | 12 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_neuromodulation.py` | 0 | 4 |

### Commandes exécutées (échantillon)

- **T1** List repo root and cerveau directory
- **T1** Check sizes of key files
- **T1** Run baseline cerveau tests
- **T1** Inspect corpus counts and fields
- **T1** Look for prior A2 artifacts
- **T1** Read prior A2 report summary
- **T1** Inspect A2 JSON structure
- **T1** Inspect corpus feature distributions
- **T1** Check prepared flux sizes and signals
- **T1** Reproduce A2 baselines and oracle
- **T1** Check working tree and test tail
- **T1** Confirm insertion point at module end
- **T1** Smoke-test M7-bis with 3 permutations
- **T1** Verify LFU vs LFU+recency tie-break scenario
- **T1** Run full 30-permutation M7-bis
- **T1** Count repeated surfaces in prefix vs capacity
- **T1** Diff final LFU vs LFU+recency memories
- **T1** Find first divergence between LFU and LFU+recency
- **T1** Count evictions without freq-1 entries
- **T1** Full M7-bis results and context controls
- **T1** Extract recency, beta sweep, context verdicts
- **T1** Run neuromodulation tests
- **T1** Run full cerveau test suite
- **T1** Run final experiment and write JSON
- **T1** Generate markdown report from JSON
- **T1** Locate lines for metrics and eviction edits
- **T1** Read class init, eviction, and runner snippets
- **T1** Read MemoireFrequence init
- **T1** Read experiment loop and controls section
- **T1** Read controls and protocol descriptions
- **T1** Read verdict section
- **T1** Run M7-bis tests after metric additions
- **T1** Rerun 30 permutations with new metrics
- **T1** Inspect new-suffix metric denominators
- **T1** Save final JSON with new metrics
- **T1** Regenerate MD with new metrics and corrections
- **T1** Review MD middle sections
- **T1** Find MD wording to fix
- **T1** Fix MD wording and add nuance
- **T1** Final full test suite
- … et 8 autres

## 4. Mesures et résultats marquants

- **T1** `| **M7** | rétention bornée, 30 permutations appariées | plafond surface **3,6446 %** = 16/439 ; aucun signal ne bat FIFO ; LFU = +23,1 pts de répétés ; nouveauté surface = −19,6 pts ; incertitude = −`
- **T1** `| **M8** | prototypes vs codes neufs | 96,48 % champs reproduit ; exact **65,09 %** (pas 0 %) ; non nuls **85,96 %** ; codes uniques **24,14 %** ; codes neufs exact **0 %** ; baseline per-game 96,10 %`
- **T1** `- Plafonds : surface finale **3.6446 %** (16/439), code **55.17 %** (16/29).`
- **T1** `2. **La métrique 3,64 % est un plafond.** 16 places / 439 surfaces = 16/439 ; toute politique qui garde 16 surfaces distinctes obtient exactement ce score. Toutes les politiques l'atteignent (`plafond`
- **T1** `| **M7** | rétention bornée, 30 permutations appariées | plafond surface **3,6446 %** = 16/439 ; aucun signal ne bat FIFO ; LFU = +24,4 pts de répétés ; nouveauté surface = −18,5 pts ; incertitude = −`
- **T1** `> Durée de la mesure : 14.47 s (33 configurations × 30 permutations).`
- **T1** `| **LFU contre FIFO/LRU** | suffixe surface **+4.25 pts** (27/30) ; répétés surface **+23.13 pts** (30/30) ; nouveaux utiles **+8.73 pts** (30/30) | le LFU gagne, mais reste à **9.28 %** contre un ora`
- **T1** `| **contexte (jeu, longueur, type) contre LFU** | meilleur cas : longueur **−0.06 pt** (14/30, p=0.54, IC à 95 % incluant 0) ; jeu **−1.89 pt** (0/30) ; type **−1.95 pt** (0/30) | **aucun contexte ne `
- **T1** `- `ret_surface_finale` = **3.64 %** = capacité/vocabulaire = 16/439. **Toutes** les configurations l'atteignent (`True`) : ce n'est pas une mesure de politique.`
- **T1** `- `ret_surface_prefixe` = 16 / surfaces distinctes du préfixe (~357) ≈ 4.5 % : même plafond, à un dénominateur près.`
- **T1** `> Durée de la mesure : 15.14 s (33 configurations × 30 permutations).`
- **T1** `| **LFU contre FIFO/LRU** | suffixe surface **+4.25 pts** (27/30) ; répétés surface **+23.13 pts** (30/30) ; nouveaux utiles **+8.73 pts** (29/30) ; nouveaux du suffixe **−0.67 pt** (0/30, p=0.5, non `
- **T1** `Le LFU est défini pour garder les items qui reviennent : il **perd** sur les surfaces vues une seule fois au préfixe et redemandées dans le suffixe — **1.94 %** contre **2.62 %** pour FIFO et **2.62 %`
- **T1** `Le `lfu_code` atteint **95.00 %** de suffixe code (oracle **98.49 %**, FIFO code **87.39 %**) ; le `lfu` surface n'atteint que **9.28 %** (oracle **24.28 %**, FIFO **5.03 %**). La clé sémantique fait `
- **T1** `Diagnostic d'évictions, cumulé sur les 30 permutations (cf. `controles.evictions` du JSON) : sur la clé surface, **11163 évictions, dont 0 sans item de fréquence 1** ; le départage n'a donc jamais à c`
- **T1** `Conclusion demandée : **LFU + récence ne bat pas LFU**. Sur la clé surface, il ne peut pas en principe (le départage ne s'exerce jamais) ; sur la clé code, il perd un pouillème, non significatif. Le L`
- **T1** `- Les contextes **combinés** au LFU sont moins mauvais, mais aucun n'a d'IC à 95 % au-dessus de zéro. `longueur` est le seul à faire jeu égal (−0.06 pt, 14/30, p=0.54) ; `jeu` et `type` perdent ~1.9 p`
- **T1** `- Sur la clé code, les contextes sont encore plus perdants (suffixe code : 37.1 % pour `contexte_jeu`, 58.99 % pour `LFU + contexte jeu`, contre 95.00 % pour `lfu_code`) : le code contient déjà le jeu`
- **T1** `12:| **LFU contre FIFO/LRU** | suffixe surface **+4.25 pts** (27/30) ; répétés surface **+23.13 pts** (30/30) ; nouveaux utiles **+8.73 pts** (29/30) ; nouveaux du suffixe **−0.67 pt** (0/30, p=0.5, n`
- **T1** `| **LFU contre FIFO** (LRU au §2) | suffixe surface **+4.25 pts** (27/30) ; répétés surface **+23.13 pts** (30/30) ; nouveaux utiles **+8.73 pts** (29/30) ; nouveaux du suffixe **−0.67 pt** (0/30, p=0`
- **T1** `c122f430 B14 — CORRECTION M5 : LE 28,03 % EST UNE COUVERTURE DE 51,4 %, PAS UN GAIN ; M5 HONNÊTE 12,60 %`

