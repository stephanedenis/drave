# Session session- — Prototype tagger auto avec repli heuristique

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-ed9b8942-25a3-48ee-9f86-f6821e56df9d` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 14:13 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 111 |
| Appels d'outils | 123 |
| Fichiers touchés | 6 |
| Commandes | 67 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche Y1 (J5, la décision du tagger) : le **prototype** du mode `auto` — `analyser --tagger auto` : si la clé existe (le fichier ou l'environnement), utiliser l'API ; sinon l'heuristique ; **sans changer le code de sortie** (0 dans les deux cas, 3 pour un refus) ; un message sur stderr qui dit lequel a servi (sans la clé, sans le secret) ; le coût affiché dans la ligne TAGGER API. Mesure : les qua … [349 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche Y1 (J5, la décision du tagger) : le **prototype** du mode `auto` — `analyser --tagger auto` : si la clé existe (le … [629 caractères tronqués]

*123 appels d'outils.* Actions notables :

- bash — Lister la structure du dépôt
- bash — Voir l'historique git et le statut
- bash — Trouver les fichiers liés au tagger et à analyser
- bash — Trouver la commande analyser et le module LLM
- bash — Chercher analyser et tagger dans drave.py
- bash — Lire le test tagger api
- read
- bash — Chercher les mentions du tagger auto
- bash — Chercher la section 3.7 et le tagger dans la doc produit
- bash — Lire la fiche tagger défaut et son JSON
- bash — Vérifier la présence de la clé sans l'afficher
- bash — Lancer les tests existants du tagger
- bash — Chercher la tâche Y1 dans le pilotage
- bash — Voir la roadmap et le plan chantier
- … et 92 autres

**Synthèse produite :**

\## Y1 livré — le prototype `--tagger auto`

\### Ce qui a été fait

- **`tools/drave.py`** : `analyser --tagger auto` choisit la voie.
  - clé trouvée (`DEEPSEEK_KEY_FILE`, `DSH_KEY_FILE`, `~/.config/drave/deepseek.key`, `DEEPSEEK_API_KEY`, `DSH_API_KEY`) → cascade API ;
  - pas de clé → heuristique, **sans importer le module réseau** ;
  - clé invalide ou réseau coupé → **repli heuristique, code 0**, avec `refus` explicite ;
  - refus de texte → **code 3**, aucun appel API ;
  - `--tagger` explicite reste la seule porte qui peut sortir **4** ;
  - message `stderr` disant la voie servie, sans jamais afficher la clé ;
  - coût dans la ligne `TAGGER API` quand l’API a été tentée.
- **`tools/tests/test_tagger_api.py`** : classe `TestTaggerAuto`, **9 tests** ajoutés (30 au total).
- **`reports/rapport-tagger-auto.md`** + **`reports/rapport-tagger-auto.json`**.
- **`docs/produit/README.md`** § 3.7 : tableau des cas `auto`, codes, coût, contrôle négatif.
- **`docs/pilotage/en-cours.md`** : compteurs et état R0.7 mis à jour.

\### Les quatre cas mesurés

| cas | code | résultat |
|---|---:|---|
| **clé présente** | **0** | API, `source=cascade`, **130 tokens**, 1,673 s |
| **clé invalide** | **0** (pas 4) | heuristique, `refus="clé refusée (HTTP 401)"` |
| **clé absente** | **0** | heuristique, **stdout identique au défaut octet pour octet** (5 852 octets JSON), `tools.llm.deepseek` non importé |
| **clé + réseau coupé** | **0** | 3 essais, heuristique, `refus` réseau |
| **refus de texte** | **3** | `refus="vide"`, **0 appel API** |

**Contrôle négatif principal** : la même clé invalide sort **0** en `auto`, mais **4** avec `--tagger` explicite, `stdout` vide.

\### Validation

- `python3 tools/tests/test_tagger_api.py` → **30 tests, OK**
- `bash tools/porte-produit.sh` → **verte**
- `python3 tools/revue_documentation.py` → **tout passe**
- `bash tools/porte-tableaux.sh` → **verte**
- `python3 tools/verifie_en_cours.py` → **état reprenable**

\### Recommandation — décision humaine

La fiche recommande de **garder le défaut heuristique hors ligne** et de traiter `--tagger auto` comme un **prototype opt-in**, jamais comme défaut : le même texte peut changer de POS selon la machine, et le coût n’est pas nul. **Le code ne change pas le défaut** ; la décision reste à l’humain.

Commit : **`519b729f`** — *J5 — Y1 : LE MODE AUTO DU TAGGER (CLÉ 0/130 TOKENS, INVALIDE 0, SANS CLÉ 0 IDENTIQUE AU DÉFAUT, RÉSEAU 0 APRÈS 3 ESSAIS) ; 30/30 TESTS*.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py` | 0 | 18 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-auto.json` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-auto.md` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 4 |

### Commandes exécutées (échantillon)

- **T1** Lister la structure du dépôt
- **T1** Voir l'historique git et le statut
- **T1** Trouver les fichiers liés au tagger et à analyser
- **T1** Trouver la commande analyser et le module LLM
- **T1** Chercher analyser et tagger dans drave.py
- **T1** Lire le test tagger api
- **T1** Chercher les mentions du tagger auto
- **T1** Chercher la section 3.7 et le tagger dans la doc produit
- **T1** Lire la fiche tagger défaut et son JSON
- **T1** Vérifier la présence de la clé sans l'afficher
- **T1** Lancer les tests existants du tagger
- **T1** Chercher la tâche Y1 dans le pilotage
- **T1** Voir la roadmap et le plan chantier
- **T1** Afficher la tâche Y1 du plan
- **T1** Lire les conventions de coût du tagger
- **T1** Repérer les classes et le champ refus
- **T1** Lire Annotation et Cascade
- **T1** Chercher les usages du parseur et de args.tagger
- **T1** Chercher les appels à formater_annotation
- **T1** Voir la date et le HEAD
- **T1** Compiler et afficher l'aide
- **T1** Lancer les tests existants après modification
- **T1** Lancer les tests du tagger avec le mode auto
- **T1** Mesurer le cas sans clé
- **T1** Mesurer le cas clé présente avec cache neuf
- **T1** Mesurer le cas clé invalide en auto
- **T1** Mesurer le cas clé + réseau coupé en auto
- **T1** Capturer la sortie lisible du mode auto avec clé
- **T1** Relancer les tests après ajout du refus modèle
- **T1** Mesurer les quatre cas et les contrôles
- **T1** Capturer la sortie lisible avec coût réel
- **T1** Afficher les mesures sélectionnées
- **T1** Vérifier les fichiers cibles
- **T1** Valider le JSON du rapport
- **T1** Trouver la ligne du code 4
- **T1** Tester la forme --tagger=auto et l'aide
- **T1** Lancer la revue de documentation
- **T1** Lancer la porte des tableaux
- **T1** Trouver les compteurs à mettre à jour
- **T1** Relancer la revue et capturer le vrai code
- … et 27 autres

## 4. Mesures et résultats marquants

- **T1** `self.assertEqual(donnees["tagger"]["cout"]["appels"], 2)  # 2 phrases × 1 tagger`
- **T1** `self.assertEqual(cout["appels"], 500)     # 1 appel pour 2 phrases, × 500`
- **T1** `self.assertEqual(cout["tokens"], 8500)    # 17 tokens pour 2 phrases, × 500`
- **T1** `145:POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)`
- **T1** `148:  vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture`
- **T1** `| **unités sémantiques** | les spans candidats à la RSN et la fraction du texte | **55,4 %** du texte en moyenne |`
- **T1** `1,67 %** (graine 0, 239 cibles). L'audit v10 publie un contrôle plus dur — un **candidat`
- **T1** `| **coût 1 000 phrases** | `evaluer --tagger --json` (2 phrases identiques, transport factice) | **0** | `cout_pour_1000_phrases` | extrapolation par phrase (×500) | `TestMatriceW3.test_cout_pour_1000`
- **T1** `.....................                                                    [100%]`
- **T1** `docs/pilotage/roadmap.md:35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 lan`
- **T1** `docs/pilotage/roadmap.md:363:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantiq`
- **T1** `tools/chantier/plan.json:581:   "mandat": "Tâche F1 : le plan de la **semaine 2** (16 → 22/11) — lis le bilan de la semaine (`reports/rapport-bilan-semaine.md`), `docs/pilotage/en-cours.md` et les fic`
- **T1** `33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**`
- **T1** `363:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `langue=fr script=Latn source=cascade · 43 étiquettes · unités sémantiques=3 (48.6% du texte)`
- **T1** `langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `"stdout": "drave 0.1.0 — analyse cascade POS (tagger auto : API DeepSeek, réseau)\nlangue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)\nPOS  Le/DET chat/NOUN d`
- **T1** `[still running after 60000ms; moved to background job bash-42]`
- **T1** `[still running after 60000ms; moved to background job bash-63]`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : tools/analyse_flux.py tools/trace_compacite.py tools/analyse_empreinte.py tools/aligneur_litteraire.py tools/docwatch/src/docwatch/diagrams.py tools/docwatch/src/docwatch/server.py tools/docwatch/.ven

## 6. Commits

- J5 — Y1 : LE MODE AUTO DU TAGGER (CLÉ 0/130 TOKENS, INVALIDE 0, SANS CLÉ 0 IDENTIQUE AU DÉFAUT, RÉSEAU 0 APRÈS 3 ESSAIS) ; 30/30 TESTS" 2>&1 | tail -20

