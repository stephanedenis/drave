# Rapport — base d'universaux typés

> **Objet.** Tester la direction « base fixe d'universaux + paramètres fixes en sortie » sur les coups des
> jeux, et comparer deux blocs : le **parseur natif typé** et le **codec classique**.
> Code : [`tools/semantique/universaux.py`](../tools/semantique/universaux.py),
> [`typed_corpus.py`](../tools/semantique/typed_corpus.py),
> [`entrainer_type.py`](../tools/semantique/entrainer_type.py). Données : B5 (112 items) et B7 (449 surfaces),
> filtrés sur les **coups**.

## 1. Le corpus et le code

| élément | valeur |
|---|---:|
| coups B5 | 79 |
| coups B7 | 449 |
| items après dédoublonnage | 528 |
| train / validation | 377 / 151 |
| paires train / validation | 25 / 6 |
| champs typés | 15 |
| classes (vocabulaire fixe) | 502 |

Le code est un **one-hot concaténé** sur 15 champs : `jeu`, `action`, `de`, `vers`, `promotion`, `roque`,
`case`, `symbole`, `carte`, `taille`, `point`, `passe`, `chemin_0`, `chemin_1`, `chemin_2`. Le découpage est
**par paire** : aucune surface d'un même sens n'est des deux côtés.

## 2. Le parseur natif typé

`route` 31,63 M, pooling moyen, 15 têtes linéaires, 200 pas, lot 32, lr base 2e-4, lr têtes 1e-3. Le
découpage est par paire, sans fuite.

| mesure | valeur |
|---|---:|
| exactitude **train** (code complet) | **48,3 %** |
| exactitude **validation** (code complet) | **0,0 %** |
| base gelée, validation | **0,0 %** |
| majoritaire (validation) | **0,0 %** |
| déterminisme (même entrée) | **1,000** |
| invariance par paire (validation) | **0,000** |

**Lecture** : le modèle **surapprend** les surfaces d'entraînement et ne généralise pas à des coups nouveaux.
La base gelée ne fait pas mieux : ce n'est pas seulement un problème de capacité, c'est un problème de
**données/compositionnalité**. Le code typé est déterministe, mais le parseur ne le remplit pas.

## 3. Le codec classique

Le codec B5/B7 est le **bloc linguistique exact** déjà présent dans le dépôt.

| mesure | B5 | B7 |
|---|---:|---:|
| coups lus | 79 / 79 | 449 / 449 |
| RSN exacte après lecture | **100 %** | **100 %** |
| restitution exacte (formats canoniques) | **33 / 79** | non mesurée (`multilingue`) |

**Lecture** : la **lecture sémantique** est exacte sur tout le corpus ; la **restitution de surface** n'est
exacte que sur 33/79 formats canoniques — le format de sortie doit être choisi, ce n'est pas un décodeur
universel. La traduction **sémantique** (surface → RSN → RSN cible) est donc exacte par construction ; la
traduction **de surface** demande encore un rendu par langue.

## 4. Contrôles

- **Découpage par paire** : aucune paire de validation n'apparaît à l'entraînement.
- **Majoritaire** : 0 % de code complet exact ; le score n'est pas porté par une classe fréquente.
- **Base gelée** : 0 % ; le résultat négatif n'est pas dû à un entraînement trop fort de la base.
- **Train vs validation** : 48,3 % contre 0 % : le contrôle d'apprentissage est explicite, c'est un
  **surapprentissage**, pas une mesure de généralisation.
- **Déterminisme** : 1,000 ; le code est stable.
- **Codec** : lecture exacte 100 % sur les deux corpus.

## 5. Ce que le résultat établit

1. La **base typée** est un **contrat** clair : 15 champs, 502 classes, sortie déterministe.
2. Le **codec classique** est aujourd'hui le **meilleur bloc linguistique** pour ce corpus : lecture
   sémantique exacte à 100 %.
3. Le **parseur natif typé** n'est **pas** au niveau : il surapprend et ne généralise pas. Il faut soit
   **plus de données synthétiques/compositionnelles**, soit de la **régularisation**, soit **distiller le
   codec** dans le natif.
4. La **restitution** est partielle (33/79) ; le format cible doit être explicite.

## 6. Ce qui pourrait rendre ce résultat faux

- Un corpus de validation plus grand, ou un découpage par **langue** plutôt que par paire.
- Un parseur natif avec **données synthétiques** et **classes équilibrées**.
- Un codec avec un **format canonique** imposé : la restitution 33/79 peut monter.
- Une taxonomie plus fine (rôles, aspect) : le code actuel est un **sous-ensemble** jeu.

## 7. Fichiers

- Code : [`universaux.py`](../tools/semantique/universaux.py), [`typed_corpus.py`](../tools/semantique/typed_corpus.py),
  [`entrainer_type.py`](../tools/semantique/entrainer_type.py), tests.
- Mesures : [`universaux-mesures.json`](universaux-mesures.json).
- Note de fond : [`docs/semantique-universaux.md`](../docs/semantique-universaux.md).
