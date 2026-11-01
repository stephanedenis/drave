# Le bloc linguistique — 398 langues au niveau langue, un contrat pour l'heuristique et le neuronal

> **Ligne de roadmap** : **R0.7** (proposition — la couche linguistique de surface) · **Date** :
> 2026-11-01 · **Verdict** : ✅ **le contrat tient** : neuf niveaux, deux implémentations
> substituables, un parallèle et une cascade, une activation sémantique à **51–76 %** ; la
> **langue** est mesurée à **0,9687** sur **398 langues** (script **1,0000**, profils permutés
> **0,0022**). ⚠️ **les niveaux profonds n'ont pas de gold** et le **modèle neuronal réel n'est
> pas qualifié** (le `llama-cli` local a expiré) : la couverture est **déclarée**, pas prouvée.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`porte-bloc-linguistique.sh`](../tools/porte-bloc-linguistique.sh),
> [`test_bloc_linguistique.py`](../tools/tests/linguistique/test_bloc_linguistique.py),
> JSON [`bloc-linguistique.json`](bloc-linguistique.json). Contrat :
> [`bloc-linguistique.md`](../docs/implantation/bloc-linguistique.md).

## 1. La question

Peut-on avoir **un seul bloc** qui étiquette du **graphème** à la **pragmatique**, avec une
version **heuristique CPU** et une version **neuronale**, **substituables** ou **parallèles**, et
dont l'heuristique peut activer la **couche sémantique** sur une **fraction** du coût — sans
changer le consommateur ?

La réponse est **oui pour le contrat**, **oui pour la langue/le script**, **partielle pour les
niveaux profonds**. C'est écrit ainsi, pas autrement.

## 2. Le dispositif

- **neuf niveaux** : graphème, morphème, mot, pos, syntagme, phrase, discours, pragmatique,
  document ; chaque étiquette porte `niveau`, `span`, `type`, `valeur`, `source`, `confiance`,
  `candidats`, `langue`, `script` ;
- **l'heuristique** : profils de trigrammes de caractères par langue, script Unicode, mots,
  classes fermées fr/en, affixes, chunker + **générateur de la coloration** (importé en lecture
  seule), phrases, connecteurs, actes de parole, régions ;
- **le neuronal de contrat** (`MockNeuronal`) : déterministe, sans GPU, il rend les niveaux
  profonds avec `source = neuronal` ; il prouve la substitution et le parallèle, pas la qualité ;
- **l'adaptateur réel** (`NeuronalLLM`) : prompt JSON, `llama-cli`, parsing, refus explicite ;
- **les compositions** : `Parallele` (fusion par niveau/span/source, syntagme heuristique
  prioritaire) et `Cascade` (neuronal seulement si un niveau reste sous le seuil) ;
- **la couche sémantique** : un stub qui ne reçoit que `unites_semantiques` et compte la
  fraction et le coût.

## 3. La langue et le script : 398 langues

Profils construits sur les articles **0–14** de l'UDHR, test sur l'article **15**, tenu à
l'écart. Les langues qui n'ont pas assez d'articles sont exclues.

| mesure | résultat |
|---|---:|
| langues avec profil | **398** |
| articles de test | **447** |
| **accuracy langue** | **0,9687** |
| **accuracy script** | **1,0000** |
| **profils permutés** (contrôle) | **0,0022** |
| construction + test | **4,0 s** |

**Ce que ça prouve** : un CPU, sans modèle, identifie la langue et le script de 398 langues UDHR
avec une précision élevée, et le contrôle permuté tombe au hasard. **Ce que ça ne prouve pas** :
la même précision sur du bruit, des codes mêlés ou des langues proches ; l'UDHR est **parallèle
et propre**, et un article par langue ne fait pas une campagne multi-domaines.

**Les erreurs nommées** : l'anglais et le scots sont proches ; l'échantillon anglais du banc est
classé **`sco`** (ou **`und`** sous le seuil) par l'heuristique, et le `MockNeuronal` — qui lit
les mêmes profils — ne le corrige pas. Le vrai correctif est un modèle neuronal qualifié, ou un
profil de langue plus fin. L'indice de langue est un **prior** (+0,02) : il ne force pas une
mauvaise langue ; le texte inconnu rend **`und`**.

## 4. Les neuf niveaux

| niveau | heuristique | neuronal (mock) | ce que ça donne |
|---|---:|---:|---|
| graphème | 0,99 | — | plages de lettres, chiffres, ponctuation, espaces |
| morphème | 0,32 | 0,80 | affixes candidats, racine |
| mot | 0,98 | 0,80 | frontières, nombres, URLs, emoji |
| pos | 0,92 fermé / 0,30 ouvert | 0,82 | DET/PREP/PRON/CONJ/AUX, classes ouvertes |
| syntagme | 0,40 | 0,78 | GN/GV/GP/REL/SUB, rôles, attachements candidats |
| phrase | 0,85 | 0,90 | type, négation, modalité |
| discours | 0,55 | 0,80 | paragraphes, connecteurs, relations |
| pragmatique | 0,45 / 0,25 | 0,80 | acte, double sens, contexte |
| document | 0,70 | 0,80 | régions, titres, provenance |

Les **neuf niveaux sont présents** sur les échantillons (`niveaux_manquants = []`). Les
confiances basses sont **assumées** : le morphème, le syntagme et la pragmatique sont des
**candidats**, pas des verdicts.

## 5. Substitution, parallèle, cascade

- **substitution** : `Heuristique` et `MockNeuronal` rendent le **même schéma** (mêmes clés,
  mêmes spans valides) ; seules la source et les valeurs changent. Le consommateur ne change pas
  de code.
- **parallèle** : les deux sources sont présentes dans l'annotation ; la fusion garde les
  alternatives par `(niveau, span, type, source)` ; à niveau égal, la plus confiante gagne,
  **sauf le syntagme**, où la segmentation heuristique (le générateur de la coloration) est
  prioritaire — un gros span du mock n'écrase pas un découpage plus fin.
- **cascade** : l'heuristique d'abord ; si `morphème`, `pos`, `syntagme`, `discours` ou
  `pragmatique` restent sous **0,6**, le neuronal est appelé sur le texte et la fusion garde la
  trace du **résidu** (`appel_neuronal = true`).

Sur « Le chat de la voisine qui dort sur le toit se réveille. », l'heuristique rend les
syntagmes du générateur S (GN « Le chat », GP « de la voisine », REL « qui dort sur le toit »,
GV « se réveille ») ; le parallèle garde ces segments et ajoute les classes ouvertes et l'acte
de parole du mock.

## 6. L'activation sémantique

`unites_semantiques` = les **mots de classe ouverte** (noms, verbes, adjectifs, adverbes), pas
les classes fermées, pas la ponctuation. La couche sémantique ne reçoit que ces unités.

| échantillon | fraction sémantique |
|---|---:|
| français | **0,513** |
| anglais | **0,737** |
| allemand | **0,756** |
| espagnol | **0,611** |
| italien | **0,706** |

Le consommateur peut activer la couche sémantique **avant** le neuronal, sur cette fraction :
c'est le chemin qui paie. Le coût se lit `C = c_h · B + c_s · U_h + c_n · U_n` ; le gain vient
de `U_h < B` et de `c_n >> c_s`. Une heuristique **fausse** coûterait plus qu'un appel réseau :
la confiance et la porte sont le garde-fou.

## 7. La version neuronale : ce qui est livré, ce qui ne l'est pas

- **`MockNeuronal`** : livré, testé, utilisé par la porte ; c'est un **double de contrat**, pas
  un modèle. Il ne prouve pas la qualité.
- **`NeuronalLLM`** : livré (prompt JSON, appel `llama-cli`, parsing, refus), **testé avec un
  faux `llama-cli`** qui rend le JSON attendu : le chemin réel est vérifié.
- **Le vrai modèle local** (`Qwen2.5-0.5B-Q4_0`) : **non qualifié** — `llama-cli` n'a pas fini
  dans le délai (110 s, puis 35 s en CPU pur, `-no-conversation`). Ce n'est pas une mesure de
  qualité ; c'est un **refus d'environnement**. La prochaine campagne doit qualifier un tagger
  ou un LLM sur un gold.

## 8. Les contrôles

| contrôle | résultat |
|---|---|
| profils de langue **permutés** | **0,0022** (proche du hasard) |
| texte **vide** | `refus = vide` |
| **ponctuation seule** | `refus = vide` |
| **langue inconnue** (`qqqqq zzzzz`) | **`und`** |
| **indice faux** (anglais, indice `fr`) | **`und`** (le prior ne force pas) |
| **rejeu** | identique (hors durée) |
| **faux `llama-cli`** | annotation `neuronal` parsée (phrase + pragmatique) |

## 9. Ce qui pourrait rendre cette fiche fausse

- **le corpus UDHR est parallèle et propre** : 0,9687 en langue ne se transporte pas sur du
  bruit, des codes mêlés ou des langues proches ;
- **un article par langue** : la mesure est tenue à l'écart, mais elle n'est pas multi-domaines ;
- **les profils sont construits sur le même corpus** : c'est un profil de langue, pas une
  connaissance linguistique générale ;
- **les niveaux profonds n'ont pas de gold** : les confiances 0,32–0,78 sont **déclarées**, pas
  mesurées ;
- **le neuronal est un mock** : la substitution est prouvée, la qualité neuronale ne l'est pas ;
- **la couche sémantique est un stub** : elle compte les unités, elle ne produit pas de RSN ;
- **le générateur S est français et petit** : 7 phrases, 11 tests ; la coloration est un germe ;
- **la langue et le script ne sont pas la traduction** : 398 langues identifiées ne veulent pas
  dire 398 langues analysées.

## 10. La suite

1. **Un gold** de POS/syntagme/pragmatique sur 100–200 phrases pour transformer les confiances en
   précisions.
2. **Un modèle neuronal qualifié** (tagger ou LLM) sur ce gold ; l'adaptateur est branché.
3. **Les paquets de langue** (classes fermées, affixes) pour les 71 langues du dépôt.
4. **Le profil de langue versionné** et son empreinte.
5. **L'intégration RSN/DRVM** : l'annotation `langue`, `script`, `source`, `confiance` à côté du
   corps ; le bloc comme port du bus.
6. **Le split `bloc-langue` / `bloc-coloration`** si le bloc grossit.

## 11. Fichiers

- Code : [`bloc_linguistique.py`](../tools/bloc_linguistique.py).
- Tests : [`test_bloc_linguistique.py`](../tools/tests/linguistique/test_bloc_linguistique.py).
- Porte : [`porte-bloc-linguistique.sh`](../tools/porte-bloc-linguistique.sh).
- Contrat : [`bloc-linguistique.md`](../docs/implantation/bloc-linguistique.md).
- JSON : [`bloc-linguistique.json`](bloc-linguistique.json).
- Schémas : [`bloc-linguistique-niveaux.svg`](../docs/schemas/bloc-linguistique-niveaux.svg),
  [`bloc-linguistique-substitution.svg`](../docs/schemas/bloc-linguistique-substitution.svg).
- Théorie : [`pre-traitement-linguistique.md`](../docs/theorie/pre-traitement-linguistique.md).
