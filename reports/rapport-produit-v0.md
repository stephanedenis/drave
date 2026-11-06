# B13 — le premier produit : `drave` v0, une CLI qui analyse, mesure et rejoue

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Ce que c'est** : un **point d'entrée unique** — `python3 tools/drave.py` — qui expose le bloc
> linguistique en autonomie, **hors ligne**, **CPU**, **déterministe** : `analyser` (POS, syntagmes
> avec rôle et **cible d'attachement**, pragmatique), `evaluer` (la mesure sur le gold), `rejouer`
> (le déterminisme par sha256), `--version`. Une **porte** le vérifie (`porte-produit.sh` : 5
> contrôles + le smoke test + l'autotest parallèle), et un **smoke test** de 6 cas tourne en 1,2 s.
>
> **Dispositif** : [`drave.py`](../tools/drave.py), [`test_produit.py`](../tools/tests/test_produit.py),
> [`porte-produit.sh`](../tools/porte-produit.sh) ; JSON [`pensee-produit-v0.json`](pensee-produit-v0.json).

## 1. Ce que la commande fait

| commande | sortie | mesure |
|---|---|---|
| `drave.py analyser "Le chat dort sur le toit."` | POS, syntagmes (GN/GV/GP, rôle, cible), pragmatique, couverture | 32 étiquettes, 3 segments |
| `drave.py analyser … --langue en --json` | le même en JSON complet | 8 704 o (fr court 5 561 o, fr long 16 100 o) |
| `drave.py evaluer` | POS 75,81 %, F1 syntagmes 58,49 %, tête 73,36 % | attachement exact 92,89 %, couverture 92,89 % |
| `drave.py rejouer "…"` | deux analyses, sha256 identique | `6b6def47…` deux fois |
| `drave.py --version` | `drave 0.1.0` | — |

## 2. La porte produit

`bash tools/porte-produit.sh` : **6 contrôles**, **~1 min 56** (dont l'autotest parallèle
183/183 en 1 min 54) :

1. `--version` répond `drave …` ;
2. `analyser` **fr** rend un JSON parsable avec POS et syntagmes ;
3. `analyser` **en** idem ;
4. `rejouer` rend le **même** sha256 deux fois (déterminisme) ;
5. le smoke test `test_produit.py` passe (6 tests, 1,2 s) ;
6. l'autotest parallèle tient **183/183**.

## 3. Ce que le produit ne fait pas encore

- **La restitution** (annotation → texte) et la **traduction** : elles demandent des poids/service.
- **Le neuronal** (`NeuronalLLM`) : hors ligne, il n'est pas exposé.
- **17 spans** du gold restent inatteignables (12 formes synthétiques, 4 GP du gold sans
  préposition, une tokenisation) — la couverture est 0,9289, pas 1,0.
- **`cascade_pos`** : la fusion avec le contrat passe sous l'heuristique (rouge documentée).

## 4. Ce que ce banc ne dit pas

- **La robustesse hors gold** : auditée à part (`rapport-produit-bloc-l.md`).
- **La charge** : le CLI est mono-phrase ; le traitement de masse passe par l'API Python.
- **La mémoire** : ~50 Mo pour le module.

## 5. Ce qui pourrait rendre cette fiche fausse

- **le JSON** est un **instantané** de l'API `Annotation` : un changement de champ casse les clients ;
- **le smoke test** ne couvre que 6 cas ;
- **l'autotest parallèle** dépend du `fork` (repli séquentiel ailleurs).

## 6. La suite

1. **La doc d'usage** (`docs/produit/`) et les exemples.
2. **La restitution** : le miroir entrée/sortie (règle 6).
3. **Les correctifs produit** de l'audit de fiabilité.

## 7. Fichiers

- [`drave.py`](../tools/drave.py) — la CLI.
- [`test_produit.py`](../tools/tests/test_produit.py) — le smoke test.
- [`porte-produit.sh`](../tools/porte-produit.sh) — la porte.
- [`pensee-produit-v0.json`](pensee-produit-v0.json) — les mesures.
