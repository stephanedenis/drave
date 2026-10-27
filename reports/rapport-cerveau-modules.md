# Rapport — modules cerveau-langage M1–M9

> **Objet.** Mesurer les neuf modules du prototype Python, sur les corpus B5/B7 et des parties générées
> par les règles. Aucun résultat n'est extrapolé au moteur Rust ni à un cerveau biologique.

## 1. Dispositif

- **Bus** : événements typés, journal, rejeu.
- **M1** : codec + contexte, code RSN typé.
- **M2** : encodeur `route` gelé, deux têtes (jeu / de), **300 pas sur les surfaces synthétiques**, test sur les 146 surfaces réelles.
- **M3–M8** : structures déterministes, sans gradient.
- **Séquences** : 160 parties (échecs, dames, go, morpion), 12 pas, générées par les règles.
- **Corpus** : 528 coups B5/B7.
- **M9** : privations déclarées.

## 2. Résultats

| module | mesure | verdict |
|---|---|---:|
| **M1** | exact **1,000** ; sans contexte **0,708** ; canonique **1,000** ; invariance **1,000** ; 1 584 événements | ✅ |
| **M2** | `jeu` **1,000** ; `de` **0,9315** (n=146) ; lésion ventrale `jeu` **0,1781**, `de` **0,9315** ; lésion dorsale `jeu` **1,000**, `de` **0,0274** | ✅ double dissociation |
| **M3** | span **12/12** ; exact **1,000** ; n-back contrôle **1,000** ; n-back brut **0,0006 / 0,0042** (invalide) | ✅ tampon |
| **M4** | rappel **1,000** ; complétion **0,979** ; séparation **1,000** ; 29 codes uniques | ✅ |
| **M5** | exact **0,989** = majoritaire **0,989** ; surprise **0,0096** | ❌ |
| **M6** | exact **0,700** ; FP **1** ; FN **20** ; coût **−0,150** | ❌ |
| **M7** | **29** nouveaux / 528 ; rappel **1,000** | ❌ |
| **M8** | **0,9648** sur 106 épisodes non stockés ; baseline **0,0** (M4 n'a rien vu) | ✅ |
| **M9** | contexte **0,292** ; M2 ventrale **0,192** ; M2 dorsale **0,014** ; M3 **0** ; M4 **0** ; M5 **0,011** ; M6 **0,314** ; M8 **0** | ✅ table |

## 3. Contrôles

- **M1** : avec/sans contexte (100 / 70,8).
- **M2** : lésions croisées des têtes ; ventrale 100 → 17,8 %, dorsale 93,2 → 2,7 %.
- **M3** : capacité zéro → span 0.
- **M4** : stockage vide → rappel 0.
- **M5** : sans transitions → 1,1 %.
- **M6** : sans porte → 30 %.
- **M8** : les 106 épisodes de test sont hors mémoire → 0 % ; les prototypes consolidés → 96,48 %.

## 4. Ce que le résultat établit

1. **M1** est un **hub de lecture fiable** : 528/528 avec contexte, 100 % en canonique et en invariance.
   C'est le codec classique, pas un réseau neuronal.
2. **M4** est une **mémoire épisodique exacte** sur le corpus : rappel 1,0, complétion 97,9 %,
   séparation 1,0.
3. **M3** tient un **tampon de 12 codes** ; le n-back n'est pas un test valide ici.
4. **M5, M6, M7** sont **négatifs ou trop faibles** : le prédicteur
   ne bat pas la majorité ; la porte est à 70 % ; la neuromodulation ne change rien ; le sommeil dégrade.
5. **M8** généralise aux épisodes non stockés : **96,48 %** contre **0 %** ; la consolidation résume, elle ne
   remplace pas.
6. **M9** montre les dépendances, pas une causalité biologique.

## 5. Critique

- **M1 exact** ne veut pas dire **M1 neuronal** : c'est un bloc classique.
- **M2** est **valide** : la double dissociation est nette (`de` 93,2 %, lésion dorsale 2,7 %, lésion
  ventrale `jeu` 17,8 %) ; le point qui a débloqué est le **dernier état caché**, pas seulement la moyenne.
  Le `jeu` reste trivial.
- **M3** n-back est dominé par l'absence de répétitions ; le span est un tampon.
- **M4** est un plus proche voisin ; le rappel exact est une propriété du stockage, pas une généralisation.
- **M5–M7** sont des négatifs utiles : ils disent ce qu'un module **ne fait pas**. **M8** est positif sur
  un test tenu à l'écart.
- **M9** ne prouve pas la nécessité ; il chiffre la privation.

## 6. Suite

- **M2** : validé ; étendre à `vers`, `chemin`, `point` et à une ablation du contexte.
- **M3** : séquences avec répétitions et interférence ; le tampon est validé, pas la mémoire du réseau.
- **M5** : ordre 2, séquences stochastiques, comparaison à un modèle de langue.
- **M6** : conflit langue/tâche, coût en pas, inhibition.
- **M7** : mémoire à capacité limitée, contrôle sans modulation.
- **M8** : rejet + prototypes + épisodes, gain hors domaine.
- **M9** : lésions par module, batteries de déficits.

## 7. Fichiers

- [`tools/cerveau/`](../tools/cerveau/) : bus, hub, voies, mémoires, prédictif, gating, neuromodulation,
  sommeil, batterie, séquences.
- [`reports/cerveau-mesures.json`](cerveau-mesures.json).
- Note : [`docs/modules-cerveau-langage.md`](../docs/modules-cerveau-langage.md).
