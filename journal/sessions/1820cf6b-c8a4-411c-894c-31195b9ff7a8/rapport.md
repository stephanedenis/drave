# Session 1820cf6b — Tu es un vérificateur ADVERSARIAL

| | |
|---|---|
| Identifiant | `1820cf6b-c8a4-411c-894c-31195b9ff7a8` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-02 19:29 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 23 |
| Appels d'outils | 21 |
| Fichiers touchés | 4 |
| Commandes | 10 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es un vérificateur ADVERSARIAL en LECTURE SEULE. Dépôt : /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur LLM Rust). INTERDICTION de modifier un fichier du dépôt (pas d'édition, pas de git, pas d'écriture dedans). Tes scripts vont dans /tmp uniquement.  OBJECTIF : réfuter ou confirmer une affirmation précise.  Fichiers à lire : `drave-core/src/engram.rs` (fonction `Engram::adresses`, env … [3390 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es un vérificateur ADVERSARIAL en LECTURE SEULE. Dépôt : /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur LLM  … [3670 caractères tronqués]

*21 appels d'outils.* Actions notables :

- bash — List repository root and tools directory
- read
- write `/tmp/test_engram_fenetre.py`
- write `/tmp/test_engram_fenetre.py`
- bash — Run the engram window equivalence test
- edit `/tmp/test_engram_fenetre.py`
- edit `/tmp/test_engram_fenetre.py`
- bash — Fix comparison harness and rerun test
- write `/tmp/test_engram_fenetre2.py`
- write `/tmp/engram_lib.py`
- bash — Patch and run phase 2 adversarial tests
- bash — Fix stale PAD in harness and rerun phase 2
- write `/tmp/test_engram_fenetre3.py`
- bash — Run phase 3 edge case tests
- … et 4 autres

**Synthèse produite :**

⏵ Rédaction du verdict final

\## Verdict

**OK** pour l'affirmation telle qu'opérationnalisée (fenêtre = les `max_ngram` = **4** derniers jetons, on ne lit que l'adresse du **dernier** jeton) : **180 259 comparaisons, 0 désaccord**.

**FAUX** si on lit littéralement « fenêtre de `max_ngram − 1` = 3 jetons » : **11 412 / 45 640 désaccords (25 %)** — et l'oracle Python donne exactement les mêmes 11 412.
**TROU** : l'équivalence exige des positions **strictement croissantes** (doublons → 16 358 / 46 200 désaccords).

\## Preuves dans `engram.rs`

`debut = positions.first()` (**l.132**) ; boucle `for shift in 0..self.max_ngram` (**l.137**) ; `if recul >= debut` (**l.140**) ; `token.checked_sub(shift)` (**l.145**) ; `blocked = blocked || recul < 0 || source == MORT` (**l.157**) ; `valeur` (**l.158**) ; XOR `valeur * multipliers[layer*max_ngram + shift]` (**l.160**) ; colonnes/modulo (**l.163-166**). Miroir exact dans `engram_reference.py:132,136-141,147-148`.

\## Méthode et chiffres (~466 000 comparaisons)

Transcription ligne à ligne de `adresses`, **validée** : elle reproduit exactement le vecteur `ADRESSES` de `engram.rs:300-306`. Oracle = `tools/engram_reference.py` importé par `importlib` (garde `__main__`, aucun effet de bord). Scripts `/tmp/engram_lib.py`, `/tmp/test_engram_fenetre{,2,3}.py`. Dépôt intact, pas de cargo.

| Test | Comparaisons | Désaccords |
|---|---|---|
| Rust-transcription vs oracle Python | 97 732 | **0** |
| Fenêtre 4 vs préfixe (positions croissantes) | 180 259 | **0** |
| Fenêtre 3 vs préfixe | 45 640 | 11 412 |
| Fenêtre 4, positions avec doublons | 46 200 | 16 358 |

Les 180 259 cas « fenêtre 4 » incluent : masques de morts **exhaustifs** pour L ≤ 8 puis un trou à **chaque** position, trous collants à t−1/t−2/t−3 (84 360), bord de séquence t < 3 / position < max_ngram−1 (1 980), L jusqu'à 200, départs 0/1/3/5/100/1000, token_map permuté, multiplicateurs 31 bits.

**Exemple minimal (fenêtre 3)** : `ids=[5,6,7,8]`, `pos=[0,1,2,3]`, aucun mort, cible = dernier jeton → préfixe `bloc[16]=256002972`, fenêtre `[6,7,8]` → `256002941`. Colonnes divergentes = exactement **16–23** (couche 1) et **40–47** (couche 14) = groupe de recul `shift=3`. Prédicat confirmé 5 435/5 435 : divergence ⟺ t ≥ 3, aucun mort en t, t−1, t−2, et jeton vivant en t−3.

**Contre-exemple positions doublons** : `ids=[3,11,11,7,3]`, `pos=[0,1,2,3,3]`, cible 4 — cause l.140 : `debut` de la tranche vaut 1, le recul du shift 3 vaut 0 < 1 → pad, alors que le préfixe (`deb
… [1217 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/test_engram_fenetre.py` | 2 | 2 |
| `/tmp/test_engram_fenetre2.py` | 1 | 0 |
| `/tmp/engram_lib.py` | 1 | 0 |
| `/tmp/test_engram_fenetre3.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** List repository root and tools directory
- **T1** Run the engram window equivalence test
- **T1** Run the engram window equivalence test
- **T1** Fix comparison harness and rerun test
- **T1** Patch and run phase 2 adversarial tests
- **T1** Fix stale PAD in harness and rerun phase 2
- **T1** Run phase 3 edge case tests
- **T1** Patch library and rerun all three test phases
- **T1** Confirm counterexamples against Python oracle
- **T1** Compute clean minimal counterexample addresses

