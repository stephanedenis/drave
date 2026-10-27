# B23 — routeur M1→M2 : gagne sur les espaces, perd sur les typos

> **Objet.** M1 est exact sur les surfaces connues, M2 sauve les typos. Un routeur simple choisit
> M1 si la surface est connue (ou une phrase longue), M2 sinon. Mesure sur les **146 items `de`**,
> **3 graines**, 300 pas.

## Résultats (moyennes 3 graines)

| mode | M1 | M2 | **routeur** | part M2 |
|---|---:|---:|---:|---:|
| original | **100 %** | 93,15 % | **100 %** | 0 % |
| casse | **99,32 %** | 93,15 % | **99,32 %** | 0 % |
| espaces | 11,64 % | **41,78 %** | **41,78 %** | 100 % |
| typo | 47,72 % | **68,27 %** | **56,16 %** | 60 % |
| phrase | **92,47 %** | 0 % | **92,47 %** | 0 % |

## Lecture

- Le routeur **préserve** M1 sur original, casse et phrase.
- Il **bascule** sur M2 pour les espaces et gagne **+30,1 pts** (11,6 → 41,8).
- Sur les typos, il ne fait que **56,2 %** contre **68,3 %** pour M2 : **40 %** des typos
  normalisées tombent sur une **autre surface valide** du lexique, donc le routeur choisit M1 et
  se trompe. Le lexique ne distingue pas une typo d’une variante connue.
- Le routeur n’est donc **pas un oracle** : il améliore M1 mais reste sous M2 sur la niche typo.

## Verdict

**Routeur positif mais partiel** : il combine les forces sur les cas connus et les espaces, mais
la **collision de lexique** l’empêche de récupérer toute la niche typo. Il faudrait un score de
confiance M1, pas une simple appartenance au lexique.

## Limites

- **146 items `de`**, 3 graines ; pas d’intervalle de confiance.
- Le lexique est construit sur les **528** surfaces réelles ; une typo qui redonne une surface
  valide est indiscernable.
- M2 reste un **rameau** (B14) ; B23 ne le promeut pas.

## Fichiers

- Code : [`tools/cerveau/routeur_m1_m2.py`](../tools/cerveau/routeur_m1_m2.py).
- Test : [`tools/cerveau/tests/test_routeur_m1_m2.py`](../tools/cerveau/tests/test_routeur_m1_m2.py).
- JSON : [`routeur-m1-m2.json`](routeur-m1-m2.json).
