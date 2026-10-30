# N3.3c — le moteur compte les experts et les canaux actifs

> **Ligne de roadmap** : N3 · **Date** : 2026-10-29 · **Verdict** : ✅ **N3.3c tenu** — les
> compteurs réels du moteur donnent **3 appels ffn**, **6/6/3 experts** et **48/24/24 canaux**
> pour trois modèles de mêmes poids ; `top_k` agit sur les experts, `kwta` sur les canaux.
> N3.3b montrait la sensibilité de la sortie ; N3.3c lit le **comptage**.
>
> **Dispositif** : `tools/porte-n3-sparsite-compte.sh`, `--drvm-sparsite`, petit `drave-n0`
> synthétique (graine 7, 113 292 paramètres, 1 bloc, prompt `abc`) ; données
> [`n3.3c-sparsite-compte.json`](n3.3c-sparsite-compte.json).

## Ce qui est mesuré

| modèle | `top_k` | `kwta` | appels ffn | experts actifs | canaux actifs |
|---|---:|---:|---:|---:|---:|
| **A** | 2 | 0,5 | 3 | **6** | **48** |
| **B** | 2 | **0,25** | 3 | **6** | **24** |
| **C** | **1** | 0,5 | 3 | **3** | **24** |

- **A** : 3 octets × 1 bloc = 3 appels ; 2 experts × 3 = 6 ; 8 canaux par expert × 6 = 48.
- **B** : même `top_k`, `kwta` divisé par 2 → canaux **24** (4 par expert).
- **C** : `top_k=1` → experts **3** (moitié de A), canaux 24.
- A deux fois : **identique**.

## Le contrôle négatif

- **Compteurs exacts** : la porte exige `(3, 6, 48)`, `(3, 6, 24)`, `(3, 3, 24)` — pas une
  inégalité.
- **A deux fois** : identique — les compteurs ne dépendent pas du hasard.
- **`kwta` seul** : experts égaux, canaux divisés par deux.
- **`top_k` seul** : experts divisés par deux, canaux égaux à B.

## Ce qui pourrait le rendre faux

- **Modèle synthétique** ; prompt de 3 octets, 1 bloc.
- **Les égalités au seuil** sont comptées `>=` : un plateau peut ajouter des canaux.
- **Le compteur est global** : il ne dit pas quels experts, seulement combien.
- **Pas de mesure de qualité** : la sparsité n’est pas un gain.

## Ce que ça change

N3.3c est **fait** : le moteur expose la sparsité réelle. N3.3 (routage/k-WTA) est complet au
niveau comptage/config. N3 reste **partielle** : N3.2b (seuil de confiance) et la porte de
composition.

## Fichiers

- `drave-core/src/native.rs` — compteurs atomiques et `sparsite()`.
- `drave-core/src/main.rs` — `--drvm-sparsite`.
- `tools/porte-n3-sparsite-compte.sh` — la porte.
- `reports/n3.3c-sparsite-compte.json` — les mesures.
- `reports/rapport-n3.3c-sparsite-compte.md` — cette fiche.
