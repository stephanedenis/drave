# N0.5 — trace et rejeu DRVM : 291/291, mais pas encore de logits

> **Objet.** Vérifier qu'un DRVM relu est **exactement** celui qui a été écrit : manifeste, blocs,
> tenseurs. C'est le rejeu **du contenu**, pas encore le rejeu d'une **passe avant**.

## Résultats

| mesure | valeur |
|---|---:|
| tenseurs tracés | **291** |
| tenseurs identiques au rejeu | **291 / 291** |
| mauvais | **aucun** |
| manifeste identique | **oui** |

- DRVM : Qwen2.5-0.5B Q4_0 importé (290 tenseurs + `__gguf_kv`).
- Trace : `drvm_trace.py trace` ; rejeu : `drvm_trace.py replay`.
- Le test synthétique vérifie aussi qu'une trace **falsifiée** est détectée.

## Lecture

- Le **contenu** DRVM se rejoue **au bit près** : chaque tenseur et le manifeste sont couverts.
- Ce n'est **pas** un rejeu d'**activation** ni de **logits** : `drave-core` lit DRVM, mais
  n'exécute pas encore sa passe avant.
- C'est donc **N0.5 — contenu** : la porte **logits** reste ouverte.

## Verdict

**N0.5 est partiel** : trace et rejeu **du contenu** sont faits (291/291), mais la trace
d'**exécution** et la comparaison de **logits** ne le sont pas.

## Limites

- **Pas d'activation**, pas de logits, pas de DRVF.
- **Qwen importé** : le graphe DRVM est un seul bloc `input`.
- La trace est **statique**, pas une trace de calcul.

## Fichiers

- Code : [`tools/drvm_trace.py`](../tools/drvm_trace.py).
- Test : [`tools/cerveau/tests/test_drvm_trace.py`](../tools/cerveau/tests/test_drvm_trace.py).
- JSON : [`drvm-trace.json`](drvm-trace.json).
