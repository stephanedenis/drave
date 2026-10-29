# N0.3b — PPL DRVM ↔ GGUF : 28,7355, puis 59 / 1 076 octets ; close

> **Mise à jour 2026-10-29 — clôture N0.3b.** La conversion est mesurée sur **59** et **1 076**
> octets ; l'exécution native est mesurée sur `drave-n0` ; la limite « même modèle Qwen exécuté
> nativement » est nommée. La ligne est close pour ce qu'elle peut prouver.
>
> **Objet.** Comparer la perplexité du GGUF source et du GGUF **reconstruit depuis le DRVM**
> (N0.4), puis vérifier l'exécution **native** du DRVM sur `drave-n0`, pour distinguer les deux
> parités que le nom « DRVM ↔ GGUF » mélangeait.

## Résultat du 28/10 — conversion

| mesure | source | retour DRVM |
|---|---:|---:|
| perplexité | **28,7355** | **28,7355** |
| tokens notés | 127 | 127 |
| contexte | 128 | 128 |
| threads | 8 | 8 |

- Source : `models/Qwen2.5-0.5B-Q4_0.gguf`.
- Retour : `/tmp/qwen05-q4-retour.gguf`, SHA-256 **identique** à la source.
- Commande source : `drave <gguf> --ppl-texte data/corpus_fr.txt --ctx 128 --limit 128 --threads 8`.
- Commande DRVM : `drave --drvm-ppl /tmp/qwen05-q4.drvm --ppl-texte data/corpus_fr.txt --ctx 128 --limit 128 --threads 8` — **aucun fichier GGUF temporaire**.

## Lecture du 28/10

- La PPL est **identique** : le passage DRVM ne change pas le modèle.
- C'est une **parité de conversion** : `Drvm::en_gguf` reconstruit les octets, `Gguf::depuis_octets`
  les lit sans fichier temporaire, puis le moteur calcule.
- Ce n'est **pas** une attention native sur les tenseurs DRVM : le moteur passe par un `Gguf` en
  mémoire. La différence est le **chemin de lecture**, pas le résultat.
- La porte **N0.3b — exécution native** restait ouverte le 28/10 ; la section suivante la tranche
  pour le modèle natif, et nomme ce qui reste hors de portée pour Qwen.

## Clôture N0.3b — 59 et 1 076 octets

Deux moitiés, deux dispositifs. Elles ne mesurent pas le même modèle, et c'est écrit.

### Conversion — Qwen 0,5 B Q4_0, GGUF contre DRVM

| texte | tokens notés | PPL GGUF | PPL DRVM | écart |
|---|---:|---:|---:|---:|
| **59 octets** (`/tmp/n0-59.txt`) | 15 | **68,1917** | **68,1917** | **0,0000** |
| **1 076 octets** (`/tmp/n0-1076.txt`) | 304 | **92,1875** | **92,1875** | **0,0000** |

- Commandes : `drave <gguf> --ppl-texte <texte> --ctx 128 --limit 128|1024 --threads 8` et
  `drave --drvm-ppl /tmp/qwen05-q4.drvm ...` avec **les mêmes options**.
- Le DRVM est **reconstruit en GGUF en mémoire** : c'est une parité de **conteneur**, pas une passe
  avant native sur les tenseurs DRVM.
- Le fichier de 59 octets en pèse 60 sur disque : le premier octet sert de contexte, **59 sont
  notés**. Le fichier de 1 076 octets en pèse 1 077 : **1 076 sont notés**.

### Exécution native — `drave-n0`, DRVM contre Python

| texte | octets notés | PPL native | PPL Python | écart |
|---|---:|---:|---:|---:|
| **59 octets** | 59 | **4,6585** | **4,658519** | **< 0,0001** |
| **1 076 octets** | 1 076 | **18,6394** | **18,6395** | **0,0001** |

- DRVM : `/tmp/n0-native.drvm`, **11 469 192** paramètres.
- Commandes : `drave --drvm-native-ppl /tmp/n0-native.drvm @/tmp/n0-59.txt 60` et
  `... @/tmp/n0-1076.txt 1024`.
- Les valeurs Python sont celles des fiches **N0.12** et **N0.13** ; la reproduction native redonne
  les mêmes chiffres.

## Contrôles

- **Aller-retour** : `gguf2drvm` puis `drvm2gguf` redonne le **SHA-256 identique** au GGUF source
  (`c8cd5f37…`) ; le DRVM est **déterministe** (`52d2c1c0…` aux deux conversions).
- **Déterminisme** : deux passes Qwen 59 octets donnent **68,1917** ; deux passes natives 59 octets
  donnent **4,6585**.
- **Modèle modifié** : un DRVM tronqué à 1 Mo est **refusé** (`en-tête incohérent`, code de sortie
  **3**), pas silencieusement lu.
- **Même corpus, même longueur, mêmes options** : les deux bras d'une paire ne diffèrent que par le
  conteneur.

## Ce qui pourrait rendre cette clôture fausse

- La parité Qwen est une parité de **conversion** : `--drvm-ppl` appelle `en_gguf()` puis
  `Gguf::depuis_octets` ; elle ne prouve pas une exécution native des tenseurs DRVM.
- Les deux moitiés ne portent pas sur le même modèle : Qwen 0,5 B (conversion) et `drave-n0`
  11,47 M (natif). Aucune ne prouve « Qwen exécuté nativement depuis DRVM ».
- Les textes sont courts (15 et 304 jetons ; 59 et 1 076 octets) : ce n'est pas une PPL de corpus.
- Le DRVM natif est un fichier `/tmp`, non versionné : la fiche cite son SHA et les commandes, pas
  le fichier.

## Verdict (2026-10-29)

**N0.3b — conversion : atteint.** Qwen GGUF et DRVM reconstruit donnent **68,1917** (15 jetons) et
**92,1875** (304 jetons), écart **0**.

**N0.3b — exécution native `drave-n0` : atteint.** **4,6585** / **18,6394** contre Python
**4,658519** / **18,6395** (N0.12/N0.13).

**N0.3b — exécution native du même modèle Qwen : hors de portée en l'état.** Le DRVM Qwen est un
**conteneur d'import** ; la passe avant native n'existe que pour le modèle natif. La ligne est close
pour ce qu'elle peut prouver, avec cette limite nommée.

## Limites

- La parité Qwen est une parité de **conteneur**, pas d'exécution native.
- Les deux modèles sont différents ; la PPL native est celle de `drave-n0`.
- Textes courts ; pas de PPL de corpus.

## Fichiers

- Code : [`tools/gguf_drvm.py`](../tools/gguf_drvm.py), [`drave-core/src/native.rs`](../drave-core/src/native.rs).
- Fiches liées : [`rapport-gguf-drvm.md`](rapport-gguf-drvm.md),
  [`rapport-native-ppl.md`](rapport-native-ppl.md),
  [`rapport-native-ppl-corpus.md`](rapport-native-ppl-corpus.md).
- JSON : [`drvm-ppl.json`](drvm-ppl.json).
