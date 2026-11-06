# Session 14114f3d — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `14114f3d-ae0d-416e-ad8e-4d4eaa04c36c` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 09:31 |
| Durée | 2.1 h |
| Tours | 1 |
| Messages | 124 |
| Appels d'outils | 140 |
| Fichiers touchés | 7 |
| Commandes | 116 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer la fiabilité « produit » du bloc linguistique** — qu'est-ce qu'un utilisateur peut utiliser en autonomie, et qu'est-ce qui est encore fragile ?  Contexte : `tools/bloc_linguistique.py` (`Heuristique`, `analyser`), `tools/tests/linguistique/evaluer_gold.py` (`charger`, `evaluer_bl … [1929 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer  … [2209 caractères tronqués]

*140 appels d'outils.* Actions notables :

- bash — Vérifier branche et état du dépôt
- bash — Lister outils, tests linguistiques, rapports
- bash — Compter lignes des fichiers cibles
- bash — Vérifier existence des fiches
- read
- bash — Lister classes et fonctions du module
- bash — Lire débuts des fiches audit et dev-test
- bash — Rejouer l'évaluation gold de référence
- bash — Vérifier commit et propreté des fichiers cibles
- bash — Lire les tests existants du bloc
- bash — Repérer les portes liées au bloc
- bash — Lire le contrat documenté du bloc
- bash — Lire la suite du contrat documenté
- bash — Vérifier le corpus UDHR et ses codes langue
- … et 111 autres

**Synthèse produite :**

Audit terminé. J'ai écrit **uniquement deux fichiers neufs**, sans modifier d'existant et sans commit :

- [`reports/rapport-produit-bloc-l.md`](reports/rapport-produit-bloc-l.md)
- [`reports/pensee-produit-bloc-l.json`](reports/pensee-produit-bloc-l.json) — contient les 50 textes, les 25 cas limites, les 18 correctifs et tous les chiffres.

\## Plantages

- **0 plantage sur les 50 phrases libres**, **0 refus**, **0 sortie vide**, **0 span hors texte**, **0 cible absente**.
- **34/50 textes** ont au moins une anomalie (**149** au total) :
  - **132 paires de syntagmes qui se chevauchent**, dans **31/50 textes**, soit **188/362 étiquettes (51,9 %)** ; le chunker seul n'en produit aucune, c'est le générateur S + l'union ;
  - 1 chevauchement de phrases (f10), dû à l'extension d'abréviation `M.` ;
  - 8 morphèmes normalisés (`tion` vs `TION`), 4 actes `exclamation` absents des candidats, 4 listes de candidats avec doublons.
- **Cas limites** : **1 plantage textuel** — un surrogate isolé, `UnicodeEncodeError` à `len(texte.encode())` (ligne 1246) — plus **3 entrées non-str** (`bytes`, `int`, `list` → `AttributeError`). `None` devient silencieusement `refus = "vide"`.
- Qualité libre : 365 `NOUN` pour 32 `VERB` ; « arrose », « rentre », « prépare », « warm » → `NOUN`. Les URL, décimaux et abréviations cassent les frontières de phrase ; les types `url` et `emoji` ne sortent **jamais** (0/963).

\## Temps par phrase

| mode | 10 mots | 50 mots | 200 mots |
|---|---:|---:|---:|
| heuristique | **1,08 ms** | **4,60 ms** | **19,43 ms** |
| parallèle | 1,51 ms | 6,18 ms | 27,22 ms |
| cascade | 1,51 ms | 6,25 ms | 29,64 ms |

- Débit : **923 / 218 / 51,5 phrases/s** ; **0,09–0,11 ms/mot**.
- Mémoire : pic **540,6 Kio** pour 200 mots ; RSS **30,7 Mio**, **delta 0** après 100 analyses ; démarrage à froid **99–113 ms**.
- Au-delà de 200 mots, coût superlinéaire : **0,394 ms/mot à 4 000 mots** (1,57 s, exposant ≈ 1,45), à cause de `_cible_proche` (199 302 appels à `_est_adverbe_seul`).
- Déterminisme : **mêmes JSON** sur même instance, instances fraîches et graines de hash **0/1/42** ; seule `duree_s` varie, et elle est exclue par défaut.

\## Contrat

**Stable** : 11 clés pour `Annotation`, 11 pour `Etiquette`, spans valides, aucun span vide, `confiance ∈ [0,1]` pour l'heuristique, unités triées/disjointes, fraction recalculable.

**Peut être vide/absent** : `etiquettes`, `unites_semantiques`, `fraction_semantique=0`, `refus`, `candidats`, `meta`, `contexte`, `langue="und"`
… [2027 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/audit_produit_bl/phrases.py` | 1 | 0 |
| `/tmp/audit_produit_bl/audit.py` | 1 | 0 |
| `/tmp/audit_produit_bl/performance.py` | 1 | 0 |
| `/tmp/audit_produit_bl/performance_final.py` | 1 | 0 |
| `/tmp/audit_produit_bl/extra.py` | 1 | 0 |
| `/tmp/audit_produit_bl/construire_json.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-produit-bloc-l.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Vérifier branche et état du dépôt
- **T1** Lister outils, tests linguistiques, rapports
- **T1** Compter lignes des fichiers cibles
- **T1** Vérifier existence des fiches
- **T1** Lister classes et fonctions du module
- **T1** Lire débuts des fiches audit et dev-test
- **T1** Rejouer l'évaluation gold de référence
- **T1** Vérifier commit et propreté des fichiers cibles
- **T1** Lire les tests existants du bloc
- **T1** Repérer les portes liées au bloc
- **T1** Lire le contrat documenté du bloc
- **T1** Lire la suite du contrat documenté
- **T1** Vérifier le corpus UDHR et ses codes langue
- **T1** Vérifier dépendance générateur et variable d'environnement
- **T1** Lire l'API du générateur S
- **T1** Rejouer l'évaluation et sauver le JSON de référence
- **T1** Extraire les chiffres de référence du JSON
- **T1** Exécuter le harnais de robustesse et contrat
- **T1** Corriger la collision de clé et relancer
- **T1** Inspecter les anomalies détectées
- **T1** Inspecter cas limites et déterminisme
- **T1** Mesurer temps, mémoire et déterminisme
- **T1** Inspecter la stabilité du contrat
- **T1** Inspecter le format des codes langue
- **T1** Inspecter qualitativement des sorties représentatives
- **T1** Calculer les statistiques agrégées de robustesse
- **T1** Quantifier attachements, titres, connecteurs, URL
- **T1** Compléter les mesures de contrat et compositions
- **T1** Mesurer la détection de langue avec et sans profils
- **T1** Tester cascade, fusion refus/contexte, décimales
- **T1** Vérifier les appels neuronal de la cascade sur le gold
- **T1** Mesurer le coût des modes composés
- **T1** Lire le style des JSON de fiches
- **T1** Lire le début de la fiche cohérence v8
- **T1** Exécuter les mesures finales et le démarrage à froid
- **T1** Corriger et relancer les mesures finales
- **T1** Vérifier la croissance du coût jusqu'à 4000 mots
- **T1** Profiler une analyse de 2000 mots
- **T1** Contrôles négatifs et simulation du correctif chevauchement
- **T1** Tester les mutations et simuler la déduplication sur le gold
- … et 76 autres

## 4. Mesures et résultats marquants

- **T1** `la cascade (mock de contrat) préserve ces chiffres et couvre **67,1 %** en unités sémantiques.`
- **T1** `(les réels passent de 40 % à 80 % en tête avec les deux lectures). Le **vrai** modèle neuronal est **refusé**`
- **T1** `- **L'attachement par tête couvre 100 %** ; le gold annote 29 cibles ambiguës en double lecture,`
- **T1** `MOTS '12,5 %' [(0, 2, '12', 'nombre'), (2, 3, ',', 'ponctuation'), (3, 4, '5', 'nombre'), (5, 6, '%', 'ponctuation')]`
- **T1** `"permutation": "1,997/220 (0,908 %) p=0",`
- **T1** `"candidat_aleatoire": "42,14 % top-1"`
- **T1** `99.2 ms 32`
- **T1** `109.0 ms 32`
- **T1** `113.3 ms 32`
- **T1** `200 median_s 0.019 ms/mot 0.096 labels 1061`
- **T1** `500 median_s 0.07 ms/mot 0.139 labels 2613`
- **T1** `1000 median_s 0.166 ms/mot 0.166 labels 5218`
- **T1** `2000 median_s 0.482 ms/mot 0.241 labels 10438`
- **T1** `4000 median_s 1.574 ms/mot 0.394 labels 20826`
- **T1** `f15 'Les prix ont augmenté de 12,5 % entre janvier et mars 2024, soit 3 poi' | nb 1`
- **T1** `e34 'The prices rose by 12.5% between January and March 2024, three points ' | nb 1`
- **T1** `### e34 'The prices rose by 12.5% between January and March 2024, three points more than expected.'`
- **T1** `[(0, 22, "'The prices rose by 12.'"), (22, 89, "'5% between January and March 2024, three points more than expected.'")]`
- **T1** `"valeur = texte[debut:fin] pour graphème/mot/pos/syntagme (100 %)"`
- **T1** `6ef2a3f5 (HEAD -> s/v7, origin/s/v7, origin/master, origin/HEAD, master) JOURNAL ET ROADMAP — LA VAGUE PRODUIT : DRAVE V0 DOCUMENTÉ, PORTE PRODUIT VERTE, AUTOTEST ×2,4, MASTER POUSSÉ (7f73c17f)`
- **T1** `| graphème, mot | ✅ | 0 crash, 0 span hors texte, `valeur = texte[debut:fin]` à **100 %**, couverture **49/50 à 100 %** (x46 : 95,14 %, newlines) |`
- **T1** ``reel_new` + 160 `synthétique`), soit **100 %**. Sur `all` : **612/612**.`
- **T1** `6ef2a3f5 (origin/s/v7, origin/master, origin/HEAD, master) JOURNAL ET ROADMAP — LA VAGUE PRODUIT : DRAVE V0 DOCUMENTÉ, PORTE PRODUIT VERTE, AUTOTEST ×2,4, MASTER POUSSÉ (7f73c17f)`

## 5. Erreurs rencontrées

6 sorties en erreur ou divergentes. Les premières :

- **T1** : MOTS 'https://example.com/a.pdf' [(0, 5, 'https', 'mot'), (5, 6, ':', 'ponctuation'), (6, 7, '/', 'ponctuation'), (7, 8, '/', 'ponctuation'), (8, 15, 'example', 'mot'), (15, 16, '.', 'ponctuation'), (
- **T1** : SIMULATION dedupe: paires 132 -> 0 | syntagmes 362 -> 292 | attachements 265 -> 215 | phrases 31 labels syntagme retirés 70 attachements retirés 50 [stderr] Traceback (most recent call last):   File "
- **T1** : ### mutations span_hors_texte detectee True | ['chevauchement_syntagme', 'span_hors_texte'] cible_absente detectee True | ['chevauchement_syntagme', 'cible_absente'] chevauchement_syntagme detectee Tr
- **T1** : clean [stderr] Traceback (most recent call last):   File "/tmp/audit_produit_bl/construire_json.py", line 41, in <module>     modes = {nom: mode(nom) for nom in ("heuristique", "mock_neuronal", "paral
- **T1** : gold 222 222 0.9289 0.5849 0.7581 17 0.5893 0.7392 banc {'labels': 60, 'textes_multi': 6, 'commencent_par_espace': 6, 'chevauchements': 1, 'exemples': [{'id': 'f10', 'a': [0, 104], 'b': [2, 104]}]} 81
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 42, in <module> AssertionError [exit code: 1]

