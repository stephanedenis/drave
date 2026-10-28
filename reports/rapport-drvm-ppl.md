# N0.3b — PPL DRVM en mémoire : 28,7355 identique

> **Objet.** Comparer la perplexité du GGUF source et du GGUF **reconstruit depuis le DRVM**
> (N0.4), pour vérifier que le conteneur natif ne change pas le calcul.

## Résultat

| mesure | source | retour DRVM |
|---|---:|---:|
| perplexité | **28,7355** | **28,7355** |
| tokens notés | 127 | 127 |
| contexte | 128 | 128 |
| threads | 8 | 8 |

- Source : `models/Qwen2.5-0.5B-Q4_0.gguf`.
- Retour : `/tmp/qwen05-q4-retour.gguf`, SHA-256 **identique** à la source.
- Commande source : `drave <gguf> --ppl-texte data/corpus_fr.txt --ctx 128 --limit 128 --threads 8`.
- Commande native : `drave --drvm-ppl /tmp/qwen05-q4.drvm --ppl-texte data/corpus_fr.txt --ctx 128 --limit 128 --threads 8` — **aucun fichier GGUF temporaire**.

## Lecture

- La PPL est **identique** : le passage DRVM ne change pas le modèle.
- C'est une **parité de conversion** **et** une **exécution depuis DRVM en mémoire** : `Drvm::en_gguf`
  reconstruit les octets, `Gguf::depuis_octets` les lit sans fichier temporaire, puis le moteur calcule.
- Ce n'est **pas** encore une attention native sur les tenseurs DRVM : le moteur passe par un
  `Gguf` en mémoire. La différence est le **chemin de lecture**, pas le résultat.
- La porte **N0.3b — exécution DRVM** reste ouverte : il faut que `drave-core` lise les tenseurs
  DRVM et calcule la passe avant sans reconstruire un GGUF.

## Verdict

**N0.3b — conversion : atteint** ; **N0.3b — exécution native : à faire**. Le DRVM est un
conteneur **fidèle** ; il n'est pas encore un **format exécutable** par le moteur.

## Limites

- **127 tokens**, un seul corpus.
- Le retour est **le même fichier** (SHA identique) : la PPL ne pouvait pas différer.
- **Pas** de passe avant qui lirait les tenseurs DRVM sans passer par un `Gguf` en mémoire.

## Fichiers

- Code : [`tools/gguf_drvm.py`](../tools/gguf_drvm.py).
- Fiche N0.4 : [`rapport-gguf-drvm.md`](rapport-gguf-drvm.md).
- JSON : [`drvm-ppl.json`](drvm-ppl.json).
