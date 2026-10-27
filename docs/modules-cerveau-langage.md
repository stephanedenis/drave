# Modules cerveau-langage M1–M9 : ce qui est branché, ce qui tient

> **Périmètre.** Prototype **Python** de la couche linguistico-sémantique inspirée du cerveau, posé
> **à côté** du moteur Rust. Le bus est réel (événements, journal, rejeu) ; les modules sont des blocs
> mesurés, pas des aires corticales. Fiche : [`rapport-cerveau-modules.md`](../reports/rapport-cerveau-modules.md).

## 1. L'architecture

```text
surface ──► M1 hub ──► code RSN typé ──► bus ──► M2 voies
                                      ├─► M3 mémoire de travail
                                      ├─► M4 mémoire épisodique ──► M8 sommeil
                                      ├─► M5 prédictif
                                      ├─► M6 gating
                                      └─► M7 neuromodulation
```

- **Bus** : événements typés, horodatés, journalisés, rejouables. Aucun module ne parle directement à un
  autre : ils publient et lisent.
- **M1** : le hub typé (codec + contexte) ; il publie `sens` et `surface`.
- **M2–M9** : blocs indépendants, mesurés par la batterie `tools/cerveau/batterie.py`.

## 2. Les neuf modules

| module | rôle | mesure | verdict |
|---|---|---|---:|
| **M1 hub** | surface → code RSN, retour canonique | **528/528** exact ; sans contexte **70,8 %** ; canonique **100 %** ; invariance **100 %** | ✅ **tient** |
| **M2 voies** | ventrale (`jeu`) / dorsale (`de`) | `jeu` **100 %** ; `de` **93,2 %** (n=146) ; lésion ventrale `jeu` **17,8 %**, `de` **93,2 %** ; lésion dorsale `jeu` **100 %**, `de` **2,7 %** | ✅ **double dissociation** |
| **M3 mémoire de travail** | tampon de codes, span, n-back | span **12/12**, exact **1,0** ; n-back contrôle (5 codes répétés) **1,0** ; n-back brut **0,06 %** (test invalide) | ✅ **tampon** |
| **M4 épisodique** | rappel par contenu, complétion, séparation | rappel **1,0** ; complétion **97,9 %** ; séparation **1,0** | ✅ **tient** |
| **M5 prédictif** | action suivante, surprise | exact **98,9 %** = majoritaire **98,9 %** | ❌ **aucun gain** |
| **M6 gating** | langue cible, inhibition, commutation | exact **70,0 %** ; FP **1**, FN **20** ; coût **−0,15** | ❌ **faible** |
| **M7 neuromodulation** | nouveauté/incertitude sur l'écriture | **29** nouveaux / 528 ; rappel **1,0** | ❌ **aucun effet mesuré** |
| **M8 sommeil** | prototypes par (jeu, action), test **non stocké** | **96,48 %** sur 106 épisodes non stockés ; baseline épisodique **0 %** | ✅ **généralise** |
| **M9 lésion** | privations déclarées | contexte **29,2 %** ; mémoire **0** ; prédictif **1,1 %** | ✅ **table de dépendances** |

## 3. Contrôles négatifs

- **M1 sans contexte** : 70,8 % → le contexte est nécessaire.
- **M2 lésion ventrale** : `jeu` 100 → 17,8 % ; `de` reste 93,2 %.
- **M2 lésion dorsale** : `de` 93,2 → 2,7 % ; `jeu` reste 100 %.
- **M3 capacité zéro** : span 0.
- **M4 sans stockage** : rappel 0.
- **M5 sans transitions** : 1,1 %.
- **M6 sans porte** : 30 %.
- **M8 sans sommeil** : les 106 épisodes de test ne sont pas dans la mémoire → **0 %** ; les prototypes
  consolidés donnent **96,48 %**.

## 4. Critique honnête

1. **M1 n'est pas un hub neuronal** : c'est le codec classique avec un bus. Il est exact, mais il ne
   généralise pas ; le natif normalisé reste à **59,8 %**.
2. **M2 réalise la double dissociation** : la voie ventrale porte `jeu`, la voie dorsale porte `de` ; les
   lésions croisées sont nettes. Le point qui a débloqué : **le dernier état caché** (coordonnée finale),
   pas seulement la moyenne.
3. **M3 mesure un tampon**, pas la mémoire du réseau. Le n-back brut est dominé par l'absence de
   répétitions ; le **n-back contrôle** (5 codes répétés) est à 1,0, mais il mesure le tampon, pas le réseau.
4. **M4 est un plus proche voisin exact** : le rappel 1,0 est attendu ; la complétion 97,9 % est réelle,
   mais ce n'est pas une généralisation.
5. **M5 n'apprend rien** : l'action suivante est déjà majoritaire à 98,9 % ; le prédicteur ne fait pas mieux.
6. **M6 est une détection de langue**, pas un contrôle exécutif ; 70 % est faible.
7. **M7 n'a pas de contrôle** : le rappel est déjà 1,0 sans modulation ; aucun effet n'est démontré.
8. **M8 généralise** : sur les 106 épisodes **non stockés**, les prototypes donnent **96,48 %** contre
   **0 %** pour la mémoire épisodique seule ; la consolidation ne remplace pas les épisodes, elle les résume.
9. **M9 est une table de privations**, pas une lésion biologique ; elle montre la dépendance, pas la
   nécessité causale.

## 5. Ce qui reste à faire

- **M2** : validé ; étendre à `vers`, `chemin`, `point` et à une ablation du **contexte**.
- **M3** : construire des séquences avec répétitions contrôlées ; tester l'interférence.
- **M5** : séquences stochastiques, ordre 2, comparaison à un modèle de langue.
- **M6** : conflit langue/tâche, coût de commutation mesuré en pas, inhibition.
- **M7** : modulation sur une mémoire à capacité limitée, avec contrôle sans modulation.
- **M8** : rejeu + prototypes + épisodes ; mesurer le gain hors domaine.
- **M9** : lésions par module, batterie de déficits, double dissociation réelle.

## 6. Fichiers

- [`tools/cerveau/`](../tools/cerveau/) : bus, hub, voies, mémoires, prédictif, gating, neuromodulation,
  sommeil, batterie, séquences.
- [`reports/rapport-cerveau-modules.md`](../reports/rapport-cerveau-modules.md) ;
  [`reports/cerveau-mesures.json`](../reports/cerveau-mesures.json).
- Tests : `tools/cerveau/tests/`.
