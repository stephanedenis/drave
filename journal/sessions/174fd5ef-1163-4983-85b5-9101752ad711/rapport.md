# Session 174fd5ef — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-18/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `174fd5ef-1163-4983-85b5-9101752ad711` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-18 09:15 |
| Durée | 0.4 h |
| Tours | 1 |
| Messages | 68 |
| Appels d'outils | 84 |
| Fichiers touchés | 2 |
| Commandes | 61 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave, en français). La machine est dédiée. Il est ~09 h 15 ; la fenêtre tarifaire REMISÉE de l'API DeepSeek s'ouvre à 11 h 30 (heure de l'Est) — donc AUCUN appel API payant avant 11 h 30.  TÂCHE : préparer le lot API du TAGGER sur le gold 612 (ligne R, R0.7), pour qu'il puisse être lancé à 11 h 30 sans hésitation. … [2396 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave, en français). La machine est  … [2676 caractères tronqués]

*84 appels d'outils.* Actions notables :

- bash — Show working directory, date and top-level files
- glob
- bash — List tools directory and tools/llm
- grep
- read
- bash — Find files matching 612 and gold
- bash — List linguistic harness files and inspect gold JSON structure
- bash — Search tariff plan for 612 and check git state
- bash — Find documents mentioning gold 612
- bash — Read tariff plan
- bash — Read drave.py key and tagger cascade code
- bash — Read drave.py analyser path
- bash — Read evaluer command implementation
- bash — List CLI arguments and limite options
- … et 62 autres

**Synthèse produite :**

⏵ Bilan final : commande, coût, dry-run et risques

**Verdict** : le lot est prêt pour 11:30. **Aucun appel au modèle n'a été fait** ; la page publique de tarifs a seulement été lue en GET (autorisé par la tâche). Rapport complet : `reports/rapport-tagger-lot-612-prep.md` ; dry-run : `reports/tagger-612-dryrun-5.json`. Rien n'a été commité.

\### Le gold 612
Pas de `gold_612.json`. Le 612 est la concaténation de :
- `tools/tests/linguistique/gold.json` — 20 `hand` ;
- `gold_reel.json` — 432 `reel` ;
- `gold_synthetique.json` — 160 `synth` ;
soit **612 items / 3 179 tokens**. Le corpus aplati est `/tmp/tagger-612/corpus-gold-612.txt` (612 blocs, sha256 `4f5231c6…`). Le « gold 452 » = `hand + reel` ; le `reel` = 432 ; `reports/tagger-612.json` est une **mesure** du 13/11, pas le gold.

\### La commande exacte (à 11:30, cache neuf)
```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
export DEEPSEEK_KEY_FILE="$HOME/.config/drave/deepseek.key"
export DEEPSEEK_MODEL=deepseek-chat
export DEEPSEEK_CACHE="$(mktemp -d /tmp/tagger-612-cache.XXXXXX)"
/usr/bin/time -v python3 tools/drave.py analyser \
  --fichier /tmp/tagger-612/corpus-gold-612.txt --jsonl --tagger \
  > /tmp/tagger-612/lot.jsonl 2> /tmp/tagger-612/lot.err
python3 tools/drave.py evaluer --tagger --json \
  > /tmp/tagger-612/eval.json 2> /tmp/tagger-612/eval.err
```
Le builder du corpus, les contrôles (614 lignes, `réseau=608`, `tokens=87550`, refus) et l'audit du coût sont dans la fiche § 6.

\### Le coût estimé
Prix page DeepSeek du 18/11, identiques à X3 : **0,15/0,60 $/M hors pointe**, **0,30/1,20 $/M en pointe**.

| | appels réseau | tokens | remisé | plein | durée |
|---|---:|---:|---:|---:|---:|
| **batch seul** | 608 | 87 550 | **0,01869 $** | **0,03738 $** | ~10 min 10 s |
| **batch + éval** (cache partagé) | 610 | 87 841 | **0,01875 $** | **0,03751 $** | ~10 min 20 s |

La règle de trois 612/1000 donnerait 0,01332 $, mais elle est **fausse** : le lot X3 de 1 000 items a 32,6 % de cache, le 612 n'a que 6 collisions. Le chiffre exact vient de la somme des `usage` des 608 prompts déjà dans le cache X3. 11:30 EST = 16:30 UTC = hors pointe.

\### Le dry-run
- **5 items, défaut hors ligne** : code 0, **5/5 JSON valides**, 51 207 o, stderr vide, **0 socket**, `tools.llm.deepseek` non importé.
- **Sans clé** : `--tagger` → **4**, stdout vide, 0 socket ; `evaluer --tagger` → **4**.
- **Passe 612 hors ligne** : **614/614 JSON valides**, 0,85 s (r308 et r318 coupés en deux).
- **30/30 tests** du tagge
… [1127 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/tagger-612/dryrun_612.py` | 1 | 0 |
| `reports/rapport-tagger-lot-612-prep.md` | 1 | 8 |

### Commandes exécutées (échantillon)

- **T1** Show working directory, date and top-level files
- **T1** List tools directory and tools/llm
- **T1** Find files matching 612 and gold
- **T1** List linguistic harness files and inspect gold JSON structure
- **T1** Search tariff plan for 612 and check git state
- **T1** Find documents mentioning gold 612
- **T1** Read tariff plan
- **T1** Read drave.py key and tagger cascade code
- **T1** Read drave.py analyser path
- **T1** Read evaluer command implementation
- **T1** List CLI arguments and limite options
- **T1** Read X3 JSON per-source token aggregates
- **T1** Read reference 612 JSON and check caches
- **T1** Read evaluer tagger report construction
- **T1** Inspect existing X3 corpus files
- **T1** Inspect gold structure and counts
- **T1** Locate JSONL and tagger helper functions
- **T1** Read JSONL analysis and main
- **T1** Read cascade wiring and DeepSeek key lookup
- **T1** Read DeepSeek client key and cache logic
- **T1** Check tagger code changes since X3
- **T1** Verify corpus first 612 items match gold
- **T1** Read enseignant.py header and tagger references
- **T1** Find previous 612 commands in docs and reports
- **T1** Read previous 612 commands and cost
- **T1** Check POS prompt changes since X3
- **T1** Read transport and POS tagger implementation
- **T1** Compute prompt collisions and duplicates for 612
- **T1** Check for X3 cache artifacts
- **T1** Compute exact 612 gold tokens from X3 pass
- **T1** Check tokenization and POS classes diff
- **T1** Count cached prompts for 612 in both caches
- **T1** Build 612 and 5-item gold corpora in /tmp
- **T1** Run offline dry-run with trapped sockets
- **T1** Patch socket trap after import and rerun
- **T1** Fix JSON parsing for non-JSONL and rerun
- **T1** Run real CLI offline dry-run on 5 items
- **T1** Run full 612 offline heuristic pass and count lines
- **T1** Analyze CLI segmentation and estimate segment tokens
- **T1** Compute exact cost for 608 segment prompts
- … et 21 autres

## 4. Mesures et résultats marquants

- **T1** `df6b9495 N — LA VALIDATION CHANGE TOUT : 4,0139 OU 4,6792 SELON LE DÉCOUPAGE, MÊMES POIDS (+16,57 %)`
- **T1** `18d49ce7 PROFILS SUR CINQ MODÈLES : BLOQUE ±0,04 % (LE CONTRAT NE BIAISE PAS) · FLOU +1,1 À +7,0 % (TOUJOURS UNE PERTE) · COURT −12,1 À +4,6 % (LE SENS DÉPEND DU MODÈLE)`
- **T1** `| **remisée** | **11:30 → 19:30** | 00:30 → 08:30 | **−50 %** (chat) / **−75 %** (raisonneur) | **tout ce qui appelle l'API** : le tagger, la distillation, les sorties de modèle |`
- **T1** `f"· unités sémantiques={len(a.unites_semantiques)} ({a.fraction_semantique:.1%} du texte)"`
- **T1** `d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO`
- **T1** `9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS`
- **T1** `reports/rapport-tagger-defaut.md:51:| **coût 1 000 phrases** | `evaluer --tagger --json` (2 phrases identiques, transport factice) | **0** | `cout_pour_1000_phrases` | extrapolation par phrase (×500) `
- **T1** `- `--sortie` : le JSON de mesure (47 Ko), avec les six modes, les quatre ventilations, les`
- **T1** `N — LA VALIDATION CHANGE TOUT : 4,0139 OU 4,6792 SELON LE DÉCOUPAGE, MÊMES POIDS (+16,57 %)`

