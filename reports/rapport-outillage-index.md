# B13 — l'outillage repris : `index_reports` a une aide, et l'index passe de 625 à 677 fiches

> **Ligne de roadmap** : **B13** (moteur de pensée, outillage) · **Date** : 2026-11-06 ·
> **Verdict** : ✅ **Deux pièges fermés** : `python3 tools/index_reports.py --help` **réécrivait**
> `reports/INDEX.md` (aucun `argparse`) ; et l'index était **périmé de 52 fiches** (625 annoncées,
> 677 sur le disque). L'outil a maintenant `--aide`, `--verifier` (sort 1 si l'index est périmé)
> et une génération déterministe ; l'index régénéré est **à jour** (`--verifier` sort 0).
> Le `plan-travail` portait **deux § 9** (numérotation 9, 12, 9) : le second devient **§ 13**.
>
> **Dispositif** : [`index_reports.py`](../tools/index_reports.py) (`argparse`, `--verifier`,
> `--aide`), [`INDEX.md`](INDEX.md) régénéré, [`plan-travail.md`](../docs/pilotage/plan-travail.md) ;
> JSON [`pensee-outillage-index.json`](pensee-outillage-index.json).

## 1. Ce qui était cassé

| piège | effet | correctif |
|---|---|---|
| `index_reports.py --help` | **réécrivait** `reports/INDEX.md` (le script générait à l'import, sans `argparse`) | `argparse` : `--aide` n'écrit rien, `--verifier` compare sans écrire |
| index périmé | 625 fiches annoncées, **677** sur le disque (52 fiches invisibles) | régénération ; `--verifier` sort 1 si périmé, 0 sinon |
| deux § 9 | numérotation 9, 12, 9 dans `plan-travail.md` | le second devient **§ 13** |

## 2. L'état après

- `python3 tools/index_reports.py --aide` : affiche l'aide, **ne touche à rien**.
- `python3 tools/index_reports.py --verifier` : **exit 0** (index à jour).
- `python3 tools/index_reports.py` : régénère (677 fiches).
- `revue_documentation` et `porte-tableaux` passent.

## 3. Ce que ce banc ne dit pas

- **L'usage du hub** : `INDEX.md` est régénéré par l'outil, pas à la main — la prochaine fiche
  doit relancer l'outil (ou `--verifier` le signalera).
- **Les autres outils** : beaucoup n'ont pas d'`argparse` (le même piège est possible) — non
  audités ici.
- **Le compte** : 677 fiches ≠ 679 `.md` (les exclusions `README`, `INDEX`, `historique-*`).

## 4. Ce qui pourrait rendre cette fiche fausse

- **une fiche ajoutée** sans régénération : `--verifier` le dira ;
- **un outil qui écrit à l'import** : non détecté ici en général.

## 5. La suite

1. **Passer les outils en `argparse`** (audit rapide des `--help` destructeurs).
2. **`--verifier` dans la passe** : une porte légère qui échoue si l'index est périmé.

## 6. Fichiers

- [`index_reports.py`](../tools/index_reports.py) — l'outil.
- [`INDEX.md`](INDEX.md) — l'index à jour.
- [`plan-travail.md`](../docs/pilotage/plan-travail.md) — § 13.
- [`pensee-outillage-index.json`](pensee-outillage-index.json).
