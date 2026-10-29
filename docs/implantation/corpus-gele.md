# Le corpus gelé des bancs (R0.3) — mesurer une progression, pas le dernier commit

> **Code** : `tools/corpus_gele.py` · **Manifeste** :
> `tools/tests/documents/corpus/manifeste.json` · **Dépend de** : R0.1 (le manifeste de document).

## 1. Le besoin

Les bancs de R0.3 sont adossés à des documents **vivants**. Le 29/10, une session voisine a
réécrit `docs/methode/continuite.md` : le gold d'une question du banc durci ne résolvait plus, la
vérification est passée au rouge, et le banc a perdu **deux** questions (84 → 83). Un banc qui
bouge avec la documentation ne mesure pas une progression — il mesure le dernier commit.

## 2. Le gel

| élément | contenu |
|---|---|
| **copie** | chaque document du corpus est copié dans `tools/tests/documents/corpus/<type>/` (30 documents, 1,4 Mo) |
| **manifeste** | `source`, `copie`, `type`, `octets`, `sha256` — le banc est le couple (copie, empreinte) |
| **constructeurs** | `banc_complet.py` et `banc_durci.py` lisent la copie (`corpus_gele.chemin_fige`) et écrivent la copie **et** la source dans le JSON du banc |
| **vérification** | `python3 tools/corpus_gele.py --verifie` recalcule les empreintes ; une copie modifiée est signalée |
| **re-gel** | volontaire : `--fige` recopie et réécrit le manifeste — un banc ne change donc jamais dans le dos de ceux qui le lisent |

## 3. Ce qui est mesuré

- **les deux bancs régénérés** sur le corpus gelé : 248 questions lexicales, 83 paraphrases,
  recouvrement moyen **0,16** (max 0,43), **0 problème** de vérification ;
- **les mesures rejouées** (voir `reports/rapport-corpus-gele.md`) : la récupération lexicale
  reste à **1,000** à 30 %, les paraphrases à **0,609**, la valeur lexicale à **0,878** ;
- **la dérive est close** : une réécriture de la documentation ne change plus le banc ; seule
  une re-gel explicite le fait.

## 4. Ce qui pourrait le rendre faux

- **le gel ne couvre que la source** : l'extraction (R0.1) est du code ; si `graphe_document.py`
  change, les régions du même fichier changent. Un gel complet devrait figer aussi les
  manifestes de graphe (prévu, pas fait) ;
- **une copie peut être modifiée à la main** : `--verifie` la démasque, mais rien ne l'empêche ;
- **le corpus est un instantané** : une correction de la documentation ne profite au banc qu'au
  prochain `--fige` — c'est voulu, et il faut le dire ;
- **le corpus reste latin** : les PDF russes et chinois ne produisent pas d'ancre (limite du
  tokeniseur, R5.2 en hérite).

## 5. Voir aussi

- [Le banc de lecture](banc-lecture.md) — ce que les bancs mesurent.
- [Le graphe de document](document-graph.md) — ce que le gel fige (la source), et ce qu'il ne
  fige pas (l'extraction).
