# L — le gold v0 : 20 phrases, POS 0,924, syntagmes 0,356, pragmatique 1,0/1,0/0,95/0,9

> **Ligne de roadmap** : **R0.7** (bloc linguistique) / **L** · **Date** : 2026-11-01 ·
> **Verdict** : ✅ **le gold v0 est mesuré** — 20 phrases, 105 tokens ; l'heuristique fait
> **0,924** en POS, **0,356** de F1 en syntagmes (P 0,471 / R 0,286), **1,0** sur l'acte,
> **1,0** sur la négation, **0,95** sur la modalité, **0,9** sur le double sens. ⚠️ **le gold
> fait 20 phrases, pas 100–200** ; le **vrai modèle neuronal est refusé** (le `llama-cli` local
> expire) ; la cascade est mesurée avec le **mock de contrat**, pas avec un modèle qualifié.
>
> **Dispositif** : [`gold.py`](../tools/tests/linguistique/gold.py) (20 phrases écrites à la main),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py), JSON
> [`pensee-gold-linguistique.json`](pensee-gold-linguistique.json).

## 1. Le gold

20 phrases (14 françaises, 6 anglaises), **écrites après le bloc**, pas tirées des 7 phrases du
banc S ni des exemples du générateur : 105 tokens annotés en POS, segments GN/GV/GP/REL/SUB et
pragmatique (acte, négation, modalité, double sens). Les spans sont **calculés par sous-chaîne**
et vérifiés à la construction.

## 2. Les résultats

| lecture | POS | POS fermé | POS ouvert | syntagmes F1 | acte | négation | modalité | double sens | fraction |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **heuristique** | **0,924** | **0,912** | **0,938** | **0,356** | **1,0** | **1,0** | **0,95** | **0,9** | **0,469** |
| mock neuronal seul | 0,486 | 0,105 | 0,938 | 0,244 | 1,0 | 0,9 | 0,9 | 0,9 | 0,525 |
| **parallèle** | **0,924** | **0,912** | **0,938** | **0,356** | **1,0** | **1,0** | **0,95** | **0,9** | **0,525** |
| **cascade** | **0,924** | **0,912** | **0,938** | **0,356** | **1,0** | **1,0** | **0,95** | **0,9** | **0,525** |

- L'heuristique porte les **classes fermées** (0,912) et les **classes ouvertes** (0,938) ;
  les deux erreurs POS visibles sont `que`/`that` lus PRON au lieu de CONJ.
- Le **syntagme** est le point faible : le générateur S segmente à sa manière, le gold à la
  sienne ; le F1 **0,356** est une mesure de **désaccord de segmentation**, pas une absence de
  structure.
- Le **mock neuronal seul** a une POS fermée de 0,105 : il ne propose que les classes ouvertes ;
  c'est un **double de contrat**, pas un modèle. La cascade récupère les classes fermées de
  l'heuristique et les ouvertes du mock, et **préserve** la négation/la modalité depuis que la
  fusion supprime les alternatives **par type** (le type de phrase ne mange plus la négation).
- La **cascade appelle le neuronal 20 fois sur 20** (les niveaux profonds sont sous 0,6) et
  couvre **52,5 %** du texte en unités sémantiques ; l'heuristique seule en couvre **46,9 %**.

## 3. Le vrai neuronal : refusé, pas simulé

`--reel` essaie `NeuronalLLM` avec `Qwen2.5-0.5B-Q4_0` et un délai de 10 s : **`RefusNeuronal`**
(le `llama-cli` local n'a pas rendu de JSON). Le mock est un **double de contrat** ; il ne
remplace pas une qualification neuronale. La cascade est donc mesurée **avec le mock** ; la
qualification du vrai modèle reste la prochaine campagne.

## 4. Ce que ce gold ne dit pas

- **20 phrases ne font pas 100–200** : c'est un **v0**, insuffisant pour une précision stable ;
  les intervalles de confiance seraient larges.
- **Le gold est écrit par le même auteur que le bloc** : un biais de conception reste possible ;
  les phrases sont nouvelles, mais les conventions (GN/GV/GP/REL/SUB) sont partagées.
- **Le syntagme F1 bas** mesure un désaccord de **segmentation**, pas seulement des erreurs ;
  une évaluation par **tête** (tête du GN, du GP) serait plus juste.
- **Le mock n'est pas un modèle** : la cascade mesure le **contrat**, pas un gain neuronal.
- **Le vrai modèle est refusé** : aucun chiffre de qualité neuronale n'est revendiqué.

## 5. Ce qui pourrait rendre cette fiche fausse

- un gold **trop proche** des règles de l'heuristique (les 20 phrases sont simples) ;
- une **convention de segmentation** qui favorise le générateur S sur certains cas ;
- une **classe POS** du gold mal annotée (les 2 erreurs `que`/`that` sont peut-être des
  conventions, pas des erreurs) ;
- un **modèle neuronal** qui, le jour où il répond, change la cascade (le mock ne la représente
  pas) ;
- un **échantillon** qui ne couvre pas les phrases longues, le bruit OCR ou le multiligne.

## 6. La suite

1. **Étendre le gold à 100–200 phrases** (difficiles : relatives, portée, double sens, anglais).
2. **Qualifier un vrai modèle neuronal** (ou un tagger) sur ce gold ; l'adaptateur est branché.
3. **Mesurer la cascade** avec ce modèle, pas avec le mock ; l'AUC/le regret de la cascade.
4. **Décomposer le syntagme par tête** pour distinguer segmentation et attachement.

## 7. Fichiers

- [`gold.py`](../tools/tests/linguistique/gold.py) · [`gold.json`](../tools/tests/linguistique/gold.json).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py).
- [`pensee-gold-linguistique.json`](pensee-gold-linguistique.json).
- [`bloc-linguistique.md`](../docs/implantation/bloc-linguistique.md) — le contrat.
