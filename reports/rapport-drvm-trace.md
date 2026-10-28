# N0.5 — trace et rejeu DRVM : contenu, logits et rejeu exacts

> **Objet.** Vérifier qu'un DRVM relu est **exactement** celui qui a été écrit : manifeste, blocs,
> tenseurs. C'est le rejeu **du contenu**, pas encore le rejeu d'une **passe avant**.

## Résultats

| mesure | valeur |
|---|---:|
| tenseurs tracés | **291** |
| tenseurs identiques au rejeu | **291 / 291** |
| mauvais | **aucun** |
| manifeste identique | **oui** |
| listes de trace | **6 144** |
| listes manquantes au rejeu | **0** |
| SHA-256 des logits (DRVM / source) | **identique** `ebd93f71…` |

- DRVM : Qwen2.5-0.5B Q4_0 importé (290 tenseurs + `__gguf_kv`).
- Trace : `drvm_trace.py trace` ; rejeu : `drvm_trace.py replay`.
- Le test synthétique vérifie aussi qu'une trace **falsifiée** est détectée.

## Lecture

- Le **contenu** DRVM se rejoue **au bit près** : chaque tenseur et le manifeste sont couverts.
- Ce n'est **pas** un rejeu d'**activation** ni de **logits** : `drave-core` lit DRVM, mais
  n'exécute pas encore sa passe avant.
- C'est donc **N0.5 — contenu** : la porte **logits** reste ouverte.

## Verdict

**N0.5 est atteint** : contenu **291/291**, trace d'exécution **6 144 listes**, rejeu **0 manquante**,
logits **SHA identique** et PPL **28,7355** identique.

## Limites

- **Trace de calcul** : `--drvm-ppl --trace-flux` produit **6 144 listes** (16 Mo) ; rejouée sur le GGUF source et sur le DRVM, elle rend **0 liste manquante**.
- **Logits** : `--logits-bin` sur les deux chemins donne le **même SHA-256** (`ebd93f71…`), 74 Mo.
- **PPL** : **28,7355** sur les deux chemins.

## Fichiers

- Code : [`tools/drvm_trace.py`](../tools/drvm_trace.py).
- Test : [`tools/cerveau/tests/test_drvm_trace.py`](../tools/cerveau/tests/test_drvm_trace.py).
- JSON : [`drvm-trace.json`](drvm-trace.json).
