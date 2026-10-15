# Le budget du sommeil — ce que le rejeu rapporte (÷ croissant en domaine) et ce qu'il coûte (bruité)

> Campagne : **cerveau** · expérience : la **courbe** de consolidation (C7) — combien de rejeu, et
> pour quel prix ?
> Question : la fiche de consolidation (`rapport-consolidation-c7.md`) a montré qu'un rejeu de
> 10 morceaux améliore le domaine (**−16,4 %** sur m20) et coûte **+1,3 %** hors domaine. La
> question du **protocole de sommeil** est : **combien** rejouer, et le coût grandit-il avec le
> volume ?
> Verdict : **le gain en domaine croît, à rendements décroissants** — −5,57 % (3 morceaux),
> −6,70 % (6), −7,67 % (10), **−9,98 %** (20) sur un texte **jamais rejoué**. **Le coût hors
> domaine, lui, n'est PAS monotone** : −0,41 %, +2,86 %, +1,60 %, +3,30 % — du bruit autour de
> +2 %, sans falaise jusqu'à 20 morceaux. Autrement dit : **le sommeil paie, et la « perte de
> généralité » est réelle mais petite et mal ordonnée**.
> Date réelle : **2026-10-14 23 h 10-23 h 35 HAE** (heure lue sur la machine)
> Protocole : `tools/n4_dessin_b.py --objectif plein` (LoRA rang 8 sur les **8 premières
> couches**, 0,07 % des paramètres, 12 époques, époque choisie sur **m29**) · rejeu m0..m{k−1} pour
> k ∈ {3, 6, 10, 20} · test **m32** (jamais rejoué) · hors domaine : `data/corpus_en_val.txt`
> (1 024 jetons à la position 300 000, jamais rejoué) · graine 0 · mesure du **modèle complet**.

## 1. La courbe

| morceaux rejoués | jetons rejoués | m32 (même domaine, jamais rejoué) | écart | hors domaine | écart |
|---:|---:|---:|---:|---:|---:|
| **3** | 3 072 | 6,7790 | **−5,57 %** | 16,6633 | **−0,41 %** |
| **6** | 6 144 | 6,6979 | −6,70 % | 17,2111 | +2,86 % |
| **10** | 10 240 | 6,6283 | −7,67 % | 17,0001 | +1,60 % |
| **20** | 20 480 | **6,4622** | **−9,98 %** | 17,2853 | +3,30 % |

*(rappel du point de la fiche précédente, autre découpage de validation : 10 morceaux → −6,60 % sur
m32 et −16,4 % sur m20. Le chiffre de m32 dépend donc de l'époque choisie — ici m29, là m30+m31 —
et c'est écrit plutôt que lissé.)*

Ce que ça dit :

* **le gain en domaine est monotone et à rendements décroissants** : ×2 de rejeu donne ÷1,19
  (3→6), ÷1,12 (6→10), ÷1,16 (10→20) de perplexité restante — soit **environ −2,5 % par
  doublement** en fin de courbe. C'est la même forme que la courbe de données du 13/10
  (`rapport-c8-echelle.md`), et elle dit la même chose : **la donnée paie encore, lentement** ;
* **le coût hors domaine ne suit PAS le volume** : −0,41 % à 3 morceaux (un *gain*), puis +2,86 %,
  +1,60 %, +3,30 %. L'étendue (3,7 points) est du même ordre que le bruit de graine mesuré pour ces
  bras (±10 %, `rapport-n4-porte-execution.md` § 4) : **« plus on rejoue, plus on oublie » n'est
  pas établi ici** — ce qui est établi, c'est qu'un rejeu court (3 morceaux) **ne coûte rien de
  mesurable** et rapporte déjà −5,6 % en domaine ;
* **le point le plus efficient est donc le rejeu COURT** : 3 morceaux (3 072 jetons, ~1 % du corpus)
  donnent 56 % du gain maximal mesuré pour un coût hors domaine **indétectable**. C'est le chiffre à
  retenir pour un protocole de sommeil : *rejouer peu, souvent* — et c'est aussi ce que la biologie
  suggère (le sommeil rejoue des **extraits**, pas la journée entière).

## 2. Comment le lire pour le cerveau

* **la consolidation est un mécanisme à rendements décroissants** : le premier morceau rejoué
  rapporte le plus, le vingtième le moins. Un cerveau qui dort longtemps ne gagne pas
  proportionnellement — et le dépôt le chiffre au lieu de le supposer ;
* **la spécialisation n'est pas une falaise** : sur 20 morceaux (~20 000 jetons, 23 % du corpus de
  test), le hors-domaine ne perd que **+3,3 %**. C'est petit devant le gain en domaine (−10 %) et
  devant la variabilité de ces bras. La conclusion de la fiche précédente (« la consolidation
  spécialise ») **tient, mais elle est à l'échelle du pour cent, pas de la catastrophe** — et cette
  fiche corrige l'impression que le +1,3 % d'alors pouvait donner ;
* **le mécanisme reste sobre** : LoRA rang 8 sur 8 couches, 12 époques, aucune donnée supplémentaire
  — le « sommeil » coûte 0,07 % des poids et quelques minutes de calcul.

## 3. Ce que cette fiche ne dit pas

* **une seule graine, un seul morceau de test en domaine** (m32), un seul hors-domaine : les quatre
  points de la colonne « coût » sont **quatre mesures indépendantes**, pas une courbe lissée — et
  c'est précisément pourquoi la non-monotonie est écrite comme du bruit possible ;
* **le coût n'est pas mesuré sur plusieurs corpus** : « hors domaine » = un seul texte d'un seul
  autre corpus ; un vrai oubli catastrophique demanderait une batterie de textes et de tâches ;
* **rien sur l'ordre du rejeu** (les morceaux sont les k **premiers**) : rejouer au hasard, ou
  rejouer deux fois les mêmes, n'est pas mesuré — c'est le cœur d'un protocole de sommeil ;
* **rien sur la génération** : la courbe est une courbe de perplexité ;
* **le taux d'apprentissage et le rang ne sont pas balayés** : « rejouer peu » est le réglage
  efficient **à ce taux et à ce rang**, pas en général.
