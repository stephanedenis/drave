# Note — entraîner le chemin court (N4), la seule voie qui reste pour C8

> Écrite le **2026-10-13 11 h 30 HAE** après la matinée de mesures
> ([`reports/rapport-c8-echelle.md`](../reports/rapport-c8-echelle.md)). Elle **propose** ; elle ne
> décide pas. Rien ici n'est mesuré : ce qui est mesuré est dans la fiche.

## 1. Ce que la matinée a établi (et qui ferme deux voies)

| ce qui a été essayé | résultat | conséquence |
|---|---|---|
| **plus de données** pour l'adaptateur (4 → 30 morceaux) | ÷5,75, mais ÷1,4 par doublement en fin de courbe | fermer l'écart de ×12,6 demanderait ~4 000 morceaux *(extrapolation)* |
| **plus de capacité** (896→512→896, GELU) | **376,01 contre 179,59** — 2,1× pire à données égales | **agrandir la tête est contre-productif** |
| **sortir plus tôt** (16 → 4 couches) | ×1,14 · ×1,30 · ×2,00 par 4 couches | la profondeur est bon marché ; l'état précoce est **lisible** |
| la tête **empruntée** (non entraînée) | 449 500 → 24,7 M selon la profondeur | un lecteur **gelé** ne sait pas lire un état précoce |

**Ce qui reste : le chemin court lui-même.** Un adaptateur sur 16 couches gelées plafonne parce que
l'information perdue n'est pas dans l'état **tel qu'il est calculé** — pas parce qu'il manque de
paramètres. Il faut donc que les couches **basses** produisent un état *plus lisible*, c'est-à-dire
qu'elles soient **entraînées pour ça**.

## 2. Trois dessins possibles (du moins cher au plus cher)

| # | dessin | ce qu'on entraîne | coût | ce que ça teste |
|---|---|---|---|---|
| **A** | **adaptateur d'entrée** | une matrice appliquée à l'embarquement + l'adaptateur de sortie existant | le moins cher (déjà outillé) | l'état précoce est-il mal *cadré* plutôt que pauvre ? |
| **B** | **adaptateurs par couche** (LoRA sur les 8 premières) | rang faible sur q/k/v/o | moyen (rétropropagation à travers 8 couches) | les couches basses peuvent-elles apprendre à rendre leur état lisible ? |
| **C** | **routeur de profondeur** (`--routee`, manque N4) | un routeur qui choisit la profondeur **par jeton** | le plus cher (le routeur doit s'entraîner *avec* la tête) | la profondeur peut-elle être **adaptative** au lieu d'être fixée ? |

L'ordre proposé est **A → B → C** : A coûte une heure et élimine (ou confirme) l'hypothèse du
cadrage ; B est le premier vrai test de « les couches basses peuvent apprendre » ; C est le dessin
du plan, et il n'a de sens que si B montre qu'un chemin court *entraîné* existe.

## 3. Les portes, écrites AVANT le code (règle du dépôt)

1. **invariant d'identité** : entraînement désactivé (adaptateur = identité) ⇒ le chemin tronqué
   rend **exactement** la perplexité de la tête empruntée (aucun octet ne change) ;
2. **le témoin « tête empruntée » reste dans la table** : toute mesure publie les trois lignes
   (empruntée, entraînée, modèle complet) — sinon un gain peut venir du texte ;
3. **test sur morceau jamais vu ET sur un second morceau** : la matinée a montré que le morceau de
   test pèse **×10** (17,35 contre 179,59) — une mesure sur un seul texte ne dit rien ;
4. **deux graines** au minimum (la graine pèse 0,7 % : en dessous de cet écart, un gain n'est pas un
   gain) ;
5. **la porte refuse de choisir l'époque sur le test** : validation séparée, comme ce matin.

## 4. Ce qu'il ne faut PAS conclure de la matinée

* que C8 est hors d'atteinte : la matinée dit que la **tête** ne suffit pas, pas que le **chemin**
  ne peut pas apprendre ;
* que la profondeur doit rester à 16 : la pénalité mesurée (×1,5 pour deux fois moins de couches)
  est faible **pour un lecteur entraîné** — c'est précisément ce qui rend le dessin C intéressant ;
* que les chiffres absolus se transposent : ils dépendent du texte (×10), et la fiche le dit.
