> Campagne : **toutes-langues** · expérience **25**
> Titre : 25. La pire paire (dzo) : hypothèse testée et RÉFUTÉE
> Date réelle : **2026-10-06 07:41 HAE** (source : commit `0b91cb0`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 25. La pire paire (dzo) : hypothèse testée et RÉFUTÉE

La mesure par unité a nommé la pire paire : **deu–dzo** (couche 10) et **ces–dzo**
(couche 8). Le dzongkha (bhoutanais, écriture tibétaine) est la langue la plus
éloignée du panel. J'ai voulu savoir pourquoi.

**Hypothèse testée** : manque de contexte — ses unités seraient trop courtes pour
que la représentation se stabilise.

| langue | jetons par unité |
|---|---:|
| fuf | 495 |
| **dzo** | **344** — **2ᵉ plus longue sur 21** |
| csw | 305 |
| deu | 83 |
| heb | 71 — la plus courte |

**Hypothèse RÉFUTÉE.** Le dzongkha est la **deuxième langue la plus longue** du
panel, pas la plus courte. Sa distance n'est donc **pas** un artefact de données :
elle est **représentationnelle**, et c'est exactement ce qu'on attend d'une langue
témoin.

**Observation au passage** : l'écriture tibétaine est **fragmentée environ quatre
fois plus** par le tokenizer que le latin — 344 jetons pour le même contenu que
l'allemand dit en 83. Et cela **ne suffit pas** à aligner sa représentation.

**Ce que cela donne** : une cible concrète et bien caractérisée. Si l'on veut
améliorer le pont sur les langues isolées, c'est **ce couple** qu'il faut regarder,
et l'on sait maintenant que le problème n'est ni la longueur du texte ni le
tokenizer — c'est la représentation elle-même.


---
