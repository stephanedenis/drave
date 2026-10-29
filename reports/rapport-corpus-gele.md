# Le corpus gelé — la dérive des bancs est close

> **Ligne de roadmap** : R0.3 (méthode) · **Date** : 2026-10-30 · **Verdict** : ✅ **le corpus
> des bancs est gelé et vérifié** — 30 documents, 1,4 Mo, manifeste sha256, **0 problème** ;
> les bancs régénérés sur les copies (**248** questions lexicales, **83** paraphrases) ; la
> réécriture d'un document ne change plus un banc.
>
> **Dispositif** : `tools/corpus_gele.py --fige` (copie + manifeste) ; les constructeurs
> lisent la copie (`corpus_gele.chemin_fige`) ; vérification par empreintes ; spec
> [`corpus-gele.md`](../docs/implantation/corpus-gele.md).

## Le problème

Le 29/10, une session voisine a réécrit `docs/methode/continuite.md` : le gold d'une question du
banc durci ne résolvait plus. Le banc a perdu **deux** questions (84 → 83) et sa vérification
est passée au rouge. Un banc adossé à des documents vivants mesure le dernier commit, pas une
progression.

## Ce qui est fait

| élément | résultat |
|---|---|
| documents figés | **30** (1,4 Mo) dans `tools/tests/documents/corpus/` |
| manifeste | `source`, `copie`, `type`, `octets`, **sha256** |
| vérification | `--verifie` : **0 problème** |
| banc lexical régénéré | **248** questions, **0 problème** |
| banc durci régénéré | **83** questions, recouvrement **0,16** (max 0,43), **0 problème** |
| constructeurs | lisent la copie ; le JSON du banc porte la copie **et** la source |

## Les mesures rejouées sur le corpus figé

| lecteur | lexical (248) | paraphrases (83) |
|---|---:|---:|
| extractif — récupération à 30 % | **1,000** | **0,609** |
| extractif — valeur à 30 % | **0,878** | **0,258** |
| modèle — contrôleur | 0,228 | 0,369 |
| modèle — début | 0,049 | 0,160 |
| modèle — closed-book | 0,000 | 0,000 |
| tête (états 8–11, négatifs durs) | — | 0,540 (BM25 0,720) |
| hasard (récupération) | 0,302 | 0,326 |

La récupération lexicale reste **1,000** : le gel ne change pas la conclusion de R0.2/R0.3. Le
modèle est à 0,228 sur le lexical (0,231 avant) et 0,369 sur les paraphrases (0,375 avant) ; la
tête à 0,540 contre BM25 0,720 (0,575/0,745 avant) — les conclusions des fiches tiennent, aux
arrondis près. Les paraphrases perdent un peu de récupération (0,653 → 0,609) avec la question
retirée et la copie gelée.

## Ce que ça change

1. **Un banc ne bouge plus dans le dos de ceux qui le lisent** : seule une re-gel explicite
   (`--fige`) le fait changer, et le manifeste dit lequel.
2. **La dérive est tracée** : les empreintes disent quelle version du corpus a produit quel
   chiffre.
3. **Ce qui n'est pas gelé** : l'extraction (le code de R0.1) et les résultats (`reports/`). Un
   changement de `graphe_document.py` changerait les régions du même fichier — un gel complet
   figerait aussi les manifestes de graphe. Nommé, pas fait.

## Fichiers

- `tools/corpus_gele.py` — le figeur et le vérificateur.
- `tools/tests/documents/corpus/` — les 30 copies et le manifeste.
- `tools/banc_complet.py`, `tools/banc_durci.py` — pointés sur la copie.
- `reports/r03-banc-extractif.json`, `reports/r03-banc-durci-extractif.json` — les mesures rejouées.
