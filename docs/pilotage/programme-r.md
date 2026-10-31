# Le programme R en une page — ce qui tient, ce qui ne tient pas

> **État au 2026-10-29** · les fiches de résultat sont dans `reports/`, les contrats dans
> `docs/implantation/`, les chiffres dans les JSON. Cette page ne remplace ni les unes ni les
> autres : elle dit ce qu'on peut **affirmer** et ce qu'on ne peut pas.

## 1. Ce qui tient — mesuré, contrôlé, rejouable

| brique | dispositif | chiffre | fiche |
|---|---|---|---|
| **le document** (R0.1) | 16 PDF + 8 MD + 3 HTML + 3 DOCX/EPUB | partition **1,0000**, fidélité **1,0000**, 51 pages | `rapport-r01` |
| **le contrôleur** (R0.2) | 20 questions main, 5 types | récupération **1,000** à 30 % du budget | `rapport-r02` |
| **le banc** (R0.3) | 248 questions lexicales + 83 paraphrases, **corpus gelé** | 0 problème de vérification | `rapport-corpus-gele` |
| **le pipeline** (R0.6) | pilote + 3 jeux | pilote **0,600**, lexical **0,976**, paraphrases **0,325** | `rapport-r06-pipeline` |
| **le balayage** (R05) | index de spans, offsets exacts | rappel@10 **0,984** (lexical), **0,1 ms** | `rapport-r05-balayage` |

## 2. Ce qui ne tient pas — et pourquoi, nommé

| tentative | chiffre | la raison |
|---|---|---|
| **têtes de lecture** (R0.4) | 0,601/0,836 puis 0,448/0,811 puis **0,540/0,720** | une sonde linéaire sur un 0,5 B, avec 500 paires, ne bat pas BM25 ; la donnée et l'encodeur manquent |
| **routeur** (R0.5) | signal AUC **0,839**, transfert 0,819/0,313 | un signe qui **prédit** n'est pas une règle qui **décide** : un seuil absolu ne transfère pas d'un corpus à l'autre |
| **relecture** (R06) | relire plus : **0/249** | le lecteur extractif répond avec le passage le mieux scoré, toujours lu ; la relecture doit changer de **modalité** |
| ~~déclencheur de la cascade~~ | **levé** (R06 v4/v5) : cascade à confiance **calibrée** = oracle (0,911 / 0,415) avec **~50 golds** | il fallait **calibrer par corpus**, pas transférer un seuil — **publié** (R06 v6 : fichier daté, `--calibration`) |

## 3. Les trois lois du programme

1. **Le corpus décide du lecteur, pas la question.** Le vrai gain de la voie auto est sur un
   corpus de valeurs (+0,109) ; sur un corpus mixte, elle **coûte** (−0,150). Un classifieur
   de forme ne sait pas ce que la réponse attend.
2. **Un signal qui prédit n'est pas une règle qui décide.** L'AUC du signal BM25 est 0,839,
   ses contrôles au hasard — et pourtant aucun seuil ne transfère. La différence se mesure par
   le **transfert**, pas par l'AUC.
3. **Pour une valeur, rendre le passage ou le span bat générer** à 0,5 B : le span 0,944 contre
   l'extractif 0,851 contre le modèle 0,381. Le génératif ne gagne que là où le lexical échoue
   (les paraphrases), et il faudra un plus grand modèle pour que ce soit net.

## 4. La prochaine action

**R0 est close** : R0.1–R0.3 et R0.6 mesurés, R0.4 et R0.5 clos en négatif, R0.6 livré. La
suite n'est plus dans R0 : c'est **R1** (la fenêtre native), qui attend le verdict de **N2**
sur la hiérarchie, puis **R2/R3** (le gist et la restitution). **R4.4** reste bloqué (OCR).

Le verrou restant du programme n'est pas un signal de plus : c'est un **encodeur qui porte** —
sans lui, la tête de survol reste sous BM25 et le `z` de B10.3 ne lit que ~7 % du sens.

## 5. Voir aussi

- [La roadmap](roadmap.md) — l'ordre des chantiers et la prochaine action.
- [Le banc](../implantation/banc-lecture.md) · [Le corpus gelé](../implantation/corpus-gele.md) ·
  [Le pipeline](../implantation/pipeline-lecture.md) · [Le balayage](../implantation/tete-balayage.md).
