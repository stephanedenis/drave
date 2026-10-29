# R13.1 — la PPL BPE-native n’est pas mesurable sans un modèle BPE natif

> **Ligne de roadmap** : R13.1 · **Date** : 2026-10-29 · **Verdict** : ⛔ **condition nommée** —
> la longueur BPE est mesurée (R13.0), mais la **PPL BPE-native** ne peut pas l’être : le modèle
> natif est en **octets** (`vocab = 256`), et aucun checkpoint BPE natif n’existe. Comparer la PPL
> de Qwen BPE à celle de `drave-n0` comparerait **deux modèles**, pas deux tokenisations.
>
> **Dispositif** : lecture du code (`tools/native_model.py:26`, `:192`), R13.0, aucun nouveau run ;
> données [`r13.1-condition.json`](r13.1-condition.json).

## La condition

| élément | état |
|---|---|
| modèle natif | **octets**, `NativeConfig.vocab = 256` |
| tokenizer déclaré | `{"kind": "bytes", "vocab": 256}` |
| tokenizer BPE | Qwen2.5, **151 936** jetons, **autre modèle** |
| checkpoint BPE natif | **aucun** |

**R13.1 exige** un modèle de **même architecture** et de **même budget**, mais avec un vocabulaire
BPE et son tokenizer. Ce modèle n’existe pas ; le fabriquer est une **campagne** (embedding
151 936 × d_model, entraînement, tokenizer versionné), pas un patch de mesure.

## Ce que R13.0 a établi

Le BPE divise la séquence par **3,4–5,2** sur le latin, **2,8** sur l’arabe/cyrillique ; le
contrôle aléatoire tombe à **1,63** octet/jeton ; la réversibilité est exacte. C’est une mesure de
**longueur**, pas de **qualité**.

## Ce que ça décide

**R13 reste ouverte.** La prochaine étape n’est pas une PPL de Qwen : c’est
1. abstraire le tokenizer dans `NativeConfig` ;
2. entraîner un petit modèle **BPE natif** au même budget que `drave-n0` ;
3. comparer **bits/octet** et PPL à budget égal, avec le même corpus.

Tant que 2 n’existe pas, toute « PPL BPE » serait celle d’un autre modèle.

## Ce qui pourrait le rendre faux

- **Aucune nouvelle mesure** : c’est une condition, pas un résultat de qualité.
- **Le BPE change les données effectives** (mêmes octets, autres frontières) ; le budget doit être
  défini en octets ou en pas, pas en jetons seulement.
- **Le vocabulaire BPE est 593× plus grand** (151 936 / 256) : l’embedding et la tête changent le
  coût ; une comparaison de PPL seule serait incomplète.
- **Un autre modèle BPE** pourrait être utilisé, mais il ne serait pas `drave-n0`.

## Fichiers

- `reports/r13.1-condition.json` — la condition.
- `reports/rapport-r13.1-condition.md` — cette fiche.
