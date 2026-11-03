# Le contrat du bloc langue — un seul contrat, quatre modes

> **Rôle.** Ce document est le **premier livrable de L** : le contrat d'entrée/sortie que doivent
> respecter l'**heuristique** et le **neuronal** pour être **substituables** ou **parallèles**.
> Il ne remplace pas une mesure : il fixe l'interface, les niveaux, les modes, la trace, le coût
> et la porte. Les chiffres cités viennent des fiches ; le contrat, lui, ne dépend pas d'eux.
>
> **Ce qu'il n'est pas.** Un plaidoyer « le CPU remplace le réseau » ; ni un contrat de
> **sémantique** (la couche sémantique est un autre bloc, `CoucheSemantique`), ni un contrat de
> **document** (R). Le contrat de L est celui de l'**annotation linguistique**, du graphème au
> pragmatique.

## 1. L'interface

```python
class BlocLinguistique(Protocol):
    nom: str

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation: ...
```

- **Entrée** : `texte` (chaîne), `langue` (code BCP-47 ou `None` → `und`), `contexte` (optionnel,
  pour la pragmatique et la coréférence).
- **Sortie** : une **`Annotation`** unique, quel que soit le mode. C'est elle qui rend la
  substitution possible : le lecteur ne sait pas qui a étiqueté, il lit la même structure.

### 1.1 L'`Annotation`

| champ | sens |
|---|---|
| `texte` | le texte analysé, inchangé |
| `langue` | la langue retenue (`und` si inconnue) |
| `script` | le script dominant (`Latn`, `Cyrl`, `Arab`…, `Zyyy` si neutre) |
| `etiquettes` | la liste des `Etiquette` (tous niveaux confondus) |
| `refus` | **non vide** si le bloc refuse — il refuse, il n'invente pas |
| `trace` | la liste des étapes (qui a fait quoi, avec quel modèle) |
| `cout` | `octets`, `tokens`, `duree_s` (et ce que le mode ajoute) |
| `unites_semantiques` | les spans activables pour la couche sémantique |
| `fraction_semantique` | la part du texte couverte par ces spans |
| `source` | `heuristique`, `neuronal`, `humain`, `parallele`, `cascade` |
| `contexte` | le contexte transmis, s'il y en a |

### 1.2 L'`Etiquette`

| champ | sens |
|---|---|
| `niveau` | l'un des **9** niveaux (voir § 2) |
| `type` | le type dans le niveau (`POS`, `GN`, `GV`, `acte`…) |
| `valeur` | la valeur (la classe, le segment, l'acte…) |
| `debut`, `fin` | les offsets dans `texte` |
| `source` | qui a produit **cette** étiquette |
| `confiance` | 0–1 ; c'est elle que la cascade lit |
| `candidats` | les valeurs plausibles, quand l'heuristique hésite |
| `langue`, `script` | l'héritage de l'annotation |
| `meta` | les détails du modèle (nom, version), sans contrat |

## 2. Les neuf niveaux

`NIVEAUX = ("graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours",
"pragmatique", "document")`.

- **graphème** : script, normalisation, direction, ponctuation.
- **morphème** : affixes, diacritiques, lemme candidat.
- **mot** : frontières, nombres, dates, URLs.
- **pos** : les classes (`DET`, `NOUN`, `VERB`, `ADJ`, `ADV`, `PREP`, `PRON`, `AUX`, `CONJ`, …).
- **syntagme** : `GN`, `GV`, `GP`, `REL`, `SUB`, rôles, attachements.
- **phrase** : frontières, type, négation, modalité.
- **discours** : coréférence, chaînes, liens entre phrases.
- **pragmatique** : acte, négation, modalité, double sens.
- **document** : structure, régions, provenance (le contrat de R s'y branche).

**Les sources** : `SOURCES = ("heuristique", "neuronal", "humain")`. Une étiquette porte sa
source ; une annotation peut mélanger les trois (c'est le cas de la cascade).

## 3. Les quatre modes

| mode | classe | ce qu'il fait | ce qu'il coûte |
|---|---|---|---|
| **heuristique** | `Heuristique` | étiquette la surface, énumère les candidats | O(octets), CPU |
| **neuronal** | `NeuronalLLMPOS`, `NeuronalLLMChunks`, `NeuronalLLMPragmatique`, `NeuronalLLMCompose` | tranche l'ambigu (POS, BIO, pragmatique) | un appel par phrase et par niveau |
| **parallèle** | `Parallele` | les deux, **fusion explicite** | les deux coûts |
| **cascade** | `Cascade` | l'heuristique d'abord ; le neuronal **seulement sur le résidu** | le coût de l'heuristique + les appels du résidu |

### 3.1 Le parallèle

`Parallele(blocs, priorite_syntagme)` : exactement **deux** blocs, même contrat, `_fusion`
explicite. La priorité (`heuristique` ou `neuronal`) décide qui gagne quand les deux étiquettent
le même span — elle est **nommée**, jamais implicite.

### 3.2 La cascade

`Cascade(heuristique, neuronal, seuil=0.6, niveaux=(...))` :

1. l'heuristique analyse ;
2. on lit sa **couverture** par niveau ;
3. si **tous** les niveaux surveillés sont au-dessus du seuil, on rend l'heuristique
   (`appel_neuronal: False`) ;
4. sinon, on appelle le neuronal et on **fusionne** (`appel_neuronal: True`, `residuel` dans la
   trace).

Le compteur `appels_neuronal` est la mesure du coût : c'est lui qui dira si la cascade paie.

## 4. Le refus

`RefusNeuronal` : le modèle n'a pas rendu une annotation exploitable. Le contrat **refuse**
(`refus` non vide, `trace` avec l'erreur) — il n'invente pas, il ne « comble » pas. C'est la
règle qui rend les mesures honnêtes : un refus est un fait, pas une étiquette à 0,5.

## 5. La trace et le coût

- **Trace** : une liste d'étapes `{etape, modele, erreur?, niveaux?, seuil?, residuel?}`. Chaque
  mode ajoute la sienne ; aucune étape n'est effacée par la fusion.
- **Coût** : `octets`, `tokens`, `duree_s` ; la cascade ajoute `appels_neuronal`. C'est le coût
  **par unité de calcul** qui tranche la frontière, pas le débit brut.

## 6. La porte

Le contrat est tenu quand, **pour chaque mode**, on peut mesurer sur les mêmes golds :

| mesure | gold | ce qu'elle vérifie |
|---|---|---|
| POS exactitude | gold 180 et gold réel 432 | le niveau `pos` |
| syntagmes F1, tête F1 | idem | le niveau `syntagme` |
| acte, négation, modalité | idem | le niveau `pragmatique` |
| refus | idem | le contrat de refus |
| coût (latence, appels) | idem | la frontière |

**Contrôle négatif obligatoire** : « une heuristique rapide mais fausse coûte plus qu'un appel
réseau ». On le mesure en comparant la **précision par unité de calcul** des modes, pas leur
débit. Une cascade qui appelle le neuronal sur 90 % des phrases n'est pas une cascade : c'est un
neuronal avec un préfixe.

## 7. Ce que le contrat ne dit pas

- **La sémantique** : `CoucheSemantique` est un autre bloc, avec son propre contrat.
- **Le document** : R a le sien (régions, TOC, provenance).
- **La détection de langue** : `detecter_langue` (trigrammes + indice) est un service du bloc, pas
  une obligation du contrat ; un bloc peut recevoir la langue et ne pas la détecter.
- **Les modèles** : aucun nom de modèle n'est dans le contrat ; `meta` porte le nom, le contrat
  porte la structure.

## 8. Les limites, nommées

- L'heuristique est **FR/EN-centrée** ; les 398 langues à 0,9687 mesurent le **script**, pas le POS.
- Le neuronal passe par l'**API DeepSeek** (`tools/llm/enseignant.py`) ou le **DRVM natif** ; les
  expériences 7B locales sont **interdites** (règle 11).
- La **pragmatique neuronale** ne qualifie pas (test 0,6375 pour 0,7556 majoritaire) : le contrat
  le dit, l'heuristique garde.
- Le contrat ne dit rien de la **qualité** : c'est la porte qui la mesure, mode par mode.

## 9. La suite de L

1. **La mesure 71 langues** (la frontière) : couverture × précision par unité de calcul, sur les
   71 langues du dépôt ; le contrôle « une heuristique fausse coûte plus cher ».
2. **La porte des quatre modes** sur le gold 432 : le même tableau, une ligne par mode.
3. **Le contrat de la pragmatique** (le niveau 4) — il reste ouvert.

## 10. Fichiers

- [`tools/bloc_linguistique.py`](../../tools/bloc_linguistique.py) — `BlocLinguistique`,
  `Annotation`, `Etiquette`, `Heuristique`, `NeuronalLLM*`, `Parallele`, `Cascade`.
- [`pre-traitement-linguistique.md`](pre-traitement-linguistique.md) — l'analyse des niveaux.
- [`reports/rapport-pensee-cascade-vrai-modele.md`](../../reports/rapport-pensee-cascade-vrai-modele.md)
  et [`reports/rapport-pensee-cascade-reel-432.md`](../../reports/rapport-pensee-cascade-reel-432.md) —
  les mesures de la cascade.
- [`docs/schemas/bloc-linguistique-substitution.svg`](../schemas/bloc-linguistique-substitution.svg) —
  le schéma de la substitution.
