# La tokenisation native — octets, par décision mesurée

> **Ce que ce document est.** La spécification de **R13 / R1.3** : ce que le natif tokenise,
> comment la décision a été mesurée, et dans quelles conditions elle serait rouverte. Le code
> est `tools/native_model.py` (`NativeConfig.vocab = 256`) ; les mesures sont dans
> [`rapport-r13-decision.md`](../../reports/rapport-r13-decision.md).
>
> **Chargement** : § 2 pour le contrat, § 4 pour la décision. § 5 pour les limites.
>
> **Ce que ce document n'est pas** : une implémentation de BPE de production. Le BPE est un
> **dispositif de mesure** (`tools/tokenizer_bpe.py`), pas une dépendance du moteur.

## 1. Le besoin

Un modèle en octets lit **1 jeton par octet**, avec un vocabulaire de 256. C'est simple,
réversible et sans tokenizer externe ; le prix est une séquence **3 à 5 fois plus longue** que
le BPE sur le latin (R13.0), donc un empan utile plus court à contexte en jetons égal. Le BPE
promet de rendre cette longueur — la question est de savoir si, **à budget égal**, il rend
aussi une meilleure qualité par octet.

## 2. Le contrat

| élément | contenu |
|---|---|
| **entrée** | octets UTF-8 ; chaque octet est un jeton `0…255` |
| **sortie** | un jeton par octet, réversible exactement (le décodage redonne le texte) |
| **déclaration** | `{"kind": "bytes", "vocab": 256}` dans le manifeste DRVM |
| **contexte** | mesuré en **octets** (130 au meilleur point de N2) — pas en jetons |
| **coût** | embedding et tête `256 × d_model`, sans vocabulaire externe |
| **comparaison** | **bits/octet**, jamais la PPL par jeton entre deux tokenisations |

La règle de comparaison est la seule qui compte : un BPE a une PPL par jeton plus élevée et des
jetons plus gros ; comparer les PPL par jeton compare deux découpages, pas deux qualités. Le
bits/octet ramène tout au même axe.

## 3. Le dispositif de mesure

- `tools/tokenizer_bpe.py` — entraîne un BPE byte-level (512, 1024) et produit les identifiants
  des deux tokenisations, plus la réversibilité et les octets/jeton ;
- `tools/entrainer_native_tokens.py` — entraîne le **même** `drave-n0` avec un vocabulaire
  variable (octets 256, BPE 512/1024), même graine, même architecture ;
- `tools/r13_anglais.py` — le dispositif anglais (R13.3/R13.4) ;
- corpus : français (`data/corpus_fr_train.txt`, val `corpus_fr_val.txt`, 4,4 Mo) et anglais
  (`corpus_en.txt` 100 Mo, val 2 Mo) ;
- **budget** : à **octets vus égaux** (10,2 M pour les trois), pas à pas égaux ; le ratio de
  **validation** donne le bits/octet exact ;
- **contrôles** : deux graines, deux langues, deux vocabulaires, réversibilité, contrôle
  aléatoire de la longueur (R13.0).

## 4. Ce qui est mesuré, et la décision

Bits/octet de validation, plus bas = mieux (source : [`rapport-r13-decision.md`](../../reports/rapport-r13-decision.md)).

| dispositif | bytes | BPE 512 | BPE 1024 |
|---|---:|---:|---:|
| français, 10 k / 5 k pas | **1,8021** | 1,8142 | — |
| français, 4 k pas | **1,8021** | — | 1,8726 |
| anglais 100 Mo | **2,6408** | 2,7522 | 2,8147 |
| français, deux graines | **1,8001** | 1,8071 | 1,8738 |

**Décision : le natif reste en octets.** Le BPE ne bat jamais les octets à budget égal ; le
512 est dans le bruit (+0,39 % sur deux graines), le 1024 perd de 3,9 à 6,6 % selon la langue.
Le « gain de 11 % » du pilote était un artefact de budget : à pas égaux, le BPE voit deux fois
plus d'octets, et le baseline octets était sous-entraîné.

Le coût du BPE est réel : vocabulaire 512 → **12,45 M** paramètres contre **11,81 M** pour les
octets (+5,4 %), et un tokenizer de plus à versionner. La décision ne l'achète pas.

## 5. La condition de réouverture

La décision est **mesurée, pas doctrinale**. Elle serait rouverte si :

1. un modèle **assez grand** (50–100 M, N5) rend la longueur de séquence dominante — ce n'est
   pas mesuré ;
2. une comparaison **à contexte égal en octets** montrait un avantage BPE — le dispositif actuel
   compare à budget d'octets, pas à empan égal ;
3. un tokenizer entraîné sur un **grand corpus de domaine** annulait la perte — non testé.

Tant que ces trois conditions ne sont pas mesurées, la charge de la preuve est du côté du BPE.

## 6. Ce qui pourrait rendre la décision fausse

- **Petits modèles, peu de pas** : 11,8 M de paramètres, 10 k pas ; l'effet peut changer à
  l'échelle.
- **Deux langues** : l'arabe, le cyrillique et le CJK ne sont pas mesurés en bits/octet ; leur
  gain de longueur est plus faible (2,8–4,6×), ce qui ne plaide pas pour le BPE.
- **Un seul type de BPE** : byte-level appris sur le train ; un tokenizer plus gros ou mieux
  adapté réduirait la perte sans nécessairement l'annuler.
- **Le contexte** : à 128 jetons, le BPE voit ~2× plus d'octets ; la comparaison à contexte
  égal reste à faire, et c'est la seule objection qui pourrait renverser la décision.

## 7. Voir aussi

- [L'architecture native](../theorie/architecture-native.md) — le manifeste, le vocabulaire, la
  décision de v0.
- [R13 — la décision](../../reports/rapport-r13-decision.md) — les chiffres et les contrôles.
- [R13.0 — la longueur](../../reports/rapport-r13-tokenisation.md) — 3,4–5,2 octets/jeton,
  réversibilité.
