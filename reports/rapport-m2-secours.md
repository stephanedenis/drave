# B19 — M2 comme secours hors codec : les typos, pas les phrases

> **Objet.** M2 n'a aucune niche mesurée sur le corpus réel (M1 lit 528/528). On perturbe les
> surfaces **sans changer le code attendu** et on demande : M2 sauve-t-il ce que M1 rate ?

## Résultats (300 pas, **3 graines**, 528 surfaces)

| mode | M1 exact | M2 `de` | M2 `vers` | lecture |
|---|---:|---:|---:|---|
| original | **100 %** | 92,88 % | 93,47 % | M1 gagne |
| casse (`E2E4`) | **98,67 %** | 92,88 % | 93,47 % | M1 gagne |
| espaces (`  e2e4  `) | 34,85 % | **52,74 %** | **48,63 %** | M2 gagne, mais reste faible |
| typo (un caractère ôté) | 36,78 % | **71,92 %** | **75,11 %** | **M2 sauve** |
| phrase (`le coup e2e4 est joue`) | **86,55 %** | **0,00 %** | 0,23 % | M1 gagne |

## Lecture

- **M1** est robuste à la **casse** (98,7 %) et assez robuste à une **phrase** (86,6 %) ; il
  s'effondre sur les **espaces** (34,8 %) et les **typos** (36,6 %).
- **M2** est **invariant** à la casse et aux espaces (il normalise) ; il **sauve les typos**
  (71,2 / 76,7 contre 36,6) et **dépasse M1** sur les espaces (41,8 / 45,2 contre 34,8).
- **M2 échoue complètement sur les phrases** (0 / 0,7) : il ne lit pas une phrase libre, il lit
  une **forme de notation**. Ce n'est pas un secours général.

## Verdict

**M2 a une niche réelle : les typos et les espaces dans la notation.** Il ne remplace pas M1 :
sur l'original, M1 est à 100 % et M2 à 93–94 % ; sur la phrase, M1 est à 86,6 % et M2 à 0.
Un **routeur** (M1 d'abord, M2 si M1 échoue) sauverait donc les typos, pas les phrases.

## Limites

- **3 graines**, 300 pas ; les espaces varient beaucoup (37–63 %), les typos restent fortes (68,5–76,7).
- Les perturbations sont **synthétiques** ; les typos réelles sont plus variées.
- Le code attendu est **inchangé** : on mesure la lecture de la forme, pas la compréhension.
- M2 reste un **rameau** (B14) ; ce résultat ne le promeut pas en étage.

## Fichiers

- Code : [`tools/cerveau/m2_secours.py`](../tools/cerveau/m2_secours.py).
- Test : [`tools/cerveau/tests/test_m2_secours.py`](../tools/cerveau/tests/test_m2_secours.py).
- JSON : [`m2-secours.json`](m2-secours.json).
