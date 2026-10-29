# R0.3 durci — 19 puis 84 paraphrases : le lexique tombe, le modèle prend la tête (de moins en moins)

> **Ligne de roadmap** : R0.3 (banc durci) · **Date** : 2026-10-29 · **Verdict** : ✅ **le
> renversement tient, de moins en moins à mesure que le banc grandit** (84 questions : 0,375
> contre 0,269 ; 19 questions : 0,717 contre 0,30) — sur des questions qui ne partagent presque aucun mot avec le
> passage (recouvrement moyen **0,20**), le lecteur lexical tombe à **0,30** de réponses
> justes, le **modèle** en donne **0,717** ; et son contrôleur bat toujours la troncature
> (**0,133**) et le closed-book (**0,000**).
>
> **Dispositif** : 19 questions **paraphrases** (5 types), écrites à la main sur des golds du
> banc complet ; recouvrement question↔gold vérifié **< 0,5** (moyenne **0,20**, max **0,43**) ;
> lecteur extractif et lecteur modèle (Qwen2.5-0.5B, `llama-cli` CUDA) ; JSON bruts
> [`r03-banc-durci-extractif.json`](r03-banc-durci-extractif.json) et
> [`r03-banc-durci-modele.json`](r03-banc-durci-modele.json).

## La question

Le banc complet (249 questions) sature : le lecteur lexical y trouve le passage gold dans
**100 %** des cas à 30 % du budget. Un banc qui ne peut pas perdre ne peut pas départager —
et il ne peut pas mesurer une tête apprise (R0.4). On durcit donc : **la question ne partage
presque aucun mot avec le passage qui porte la réponse**. Un lecteur qui ne sait que recouvrer
échoue ; un lecteur qui comprend peut réussir.

## Le dispositif

- **19 paraphrases**, 5 types, écrites à la main sur des golds du banc complet (la valeur et le
  gold sont repris tels quels, seule la formulation change) ;
- **le recouvrement est vérifié** par le constructeur : fraction des mots de la question
  présents dans le gold. Au-dessus de 0,5, la question est refusée. Moyenne **0,20**, max
  **0,43** — c'est bien une paraphrase ;
- **le harnais est celui de R0.2** : budgets 10/30/50 %, contrôle aléatoire, troncature naïve,
  closed-book ; le même lecteur extractif, puis le modèle sur GPU.

## Ce qui est mesuré

**Réponses justes (la valeur attendue est dans la réponse) :**

| type | extractif à 30 % | modèle, contrôleur | modèle, début | closed-book |
|---|---:|---:|---:|---:|
| code | 0,25 | **1,00** | 0,00 | 0,00 |
| juridique | 0,00 | 0,33 | **0,67** | 0,00 |
| prose | 0,50 | **1,00** | 0,00 | 0,00 |
| tableau | 0,25 | **0,50** | 0,00 | 0,00 |
| technique | 0,50 | **0,75** | 0,00 | 0,00 |
| **agrégat** | **0,30** | **0,717** | **0,133** | **0,000** |

**Et la récupération du passage gold (extractif)** : 1,00 / 0,33 / 1,00 / 1,00 / 0,75 → **0,817**
contre **1,000** sur le banc complet. La chute est exactement le fait des paraphrases : sur le
juridique, où les questions ne partagent presque rien avec le passage, le lexical ne trouve plus
qu'un cas sur trois.

## Ce que ça dit, et c'est le résultat du cycle

**Il n'y a pas UN meilleur lecteur : il y a deux régimes.**

| régime | qui gagne | chiffre |
|---|---|---|
| **questions lexicales** (le banc complet) | le **lecteur extractif** | 0,72–1,00 contre 0,23 pour le modèle |
| **paraphrases** (ce banc) | le **modèle** | 0,717 contre 0,30 pour l'extractif |

Le pipeline de lecture doit donc **choisir** : rendre le passage quand la question partage ses
mots avec le document, générer quand elle ne les partage pas. Ce n'est pas une préférence, c'est
une mesure.

**Et le contrôleur reste utile dans les deux régimes** : sur les paraphrases, il donne 0,717
contre 0,133 pour la troncature naïve — **5,4×** — et 0,000 en closed-book.

**Une perte nommée** : sur le **juridique**, la troncature (0,67) bat le contrôleur (0,33). Les
réponses sont dans les 1 200 premiers caractères du PDF (en-tête, objet, date), et le contrôleur
préfère d'autres passages. C'est la limite de la fenêtre quand le document met sa réponse
devant : le contrôleur doit pouvoir dire « le début suffit ».

## Le banc élargi (84 paraphrases) — le modèle gagne encore, mais de moins

Le pilote de 19 questions a été **quadruplé** : 84 paraphrases sur 29 documents, recouvrement
moyen **0,17** (max 0,43), toujours vérifié par le constructeur. Les deux lecteurs sont rejoués.

| type | extractif, valeur à 30 % | modèle, contrôleur | modèle, début | closed-book |
|---|---:|---:|---:|---:|
| code | 0,211 | **0,474** | 0,053 | 0,000 |
| juridique | 0,214 | 0,357 | **0,500** | 0,000 |
| prose | 0,333 | **0,556** | 0,056 | 0,000 |
| tableau | 0,200 | **0,267** | 0,133 | 0,000 |
| technique | **0,389** | 0,222 | 0,056 | 0,000 |
| **agrégat** | **0,269** | **0,375** | **0,160** | **0,000** |

**Ce qui change avec l'échelle** :

- le modèle garde l'avantage (**0,375** contre **0,269**, +11 points) mais il était de +42 points
  sur 19 questions : le banc élargi est **plus dur pour lui aussi** (0,717 → 0,375) ;
- il ne gagne plus que **4 types sur 5** : sur la **technique**, l'extractif reprend la main
  (0,389 contre 0,222) — les paraphrases techniques gardent assez de vocabulaire pour BM25 ;
- le **juridique** confirme le motif : le **début** (0,500) bat le contrôleur (0,357) — les
  réponses sont dans les premières lignes du PDF, et le contrôleur préfère d'autres passages ;
- la **récupération** de l'extractif tombe à **0,653** en moyenne à 30 % (contre 0,817 sur 19),
  et le contrôle aléatoire monte à 0,526 sur le code : sur les documents courts, tirer au sort
  couvre presque tout — le contrôle aléatoire y perd son sens.

**Conclusion** : le régime paraphrase tient (le modèle devant), mais l'écart se resserre quand
le banc grandit et se diversifie. Le modèle de 0,5 B n'est pas un lecteur de paraphrases
robuste ; il est *moins mauvais* que le lexical.

## Ce qui pourrait le rendre faux

- **19 questions** : un cas vaut 0,05 à 0,25 selon le type ; c'est un pilote de difficulté.
- **Paraphrases écrites par l'auteur du banc** : elles peuvent être plus faciles (ou plus
  dures) qu'une paraphrase naturelle. Le recouvrement est vérifié, l'équité ne l'est pas.
- **Les valeurs courtes** (« 22 », « 1,5 ») rendent le contrôle permissif : après normalisation
  des séparateurs, « 22 » se retrouve dans beaucoup de réponses.
- **Modèle de 0,5 B** : 0,717 n'est pas un plafond, c'est ce modèle-là.
- **Le hasard sur le code** (0,75 en récupération) : les documents courts font que des passages
  tirés au sort couvrent presque tout — le contrôle aléatoire y perd son sens.
- **La même limite de tokeniseur** : le corpus est latin.

## Ce que ça change

1. **R0.4 est mesurable** : le scoreur classique ne sature plus sur ce banc, une tête apprise
   peut donc être départagée. C'est la prochaine action.
2. **Le routeur extractif/génératif** devient un chantier nommé : la question décide du lecteur,
   et la décision se mesure (recouvrement question↔document).
3. **La fenêtre doit être gouvernée** : le cas juridique montre qu'un contrôleur qui ignore le
   début du document peut perdre contre la troncature.

## Fichiers

- `tools/banc_durci.py` — les 19 paraphrases et la vérification du recouvrement.
- `tools/tests/documents/bench-durci.json` — le banc.
- `reports/r03-banc-durci-extractif.json`, `reports/r03-banc-durci-modele.json` — mesures brutes.
- `tools/banc_lecture.py --depuis` — relit un JSON sans rejouer la porte.
