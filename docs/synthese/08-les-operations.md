# 8. Les opérations : ce que l'état porte, et ce qu'il ne calcule pas

> Chapitre de synthèse, 24/10/2026 — il relie deux choses mesurées le même jour : les **opérations** de l'étage 2
> (B4, six mesures) et la **grappe** du moteur (A7.3). Les fiches :
> [`rapport-operateur-negation.md`](../../reports/rapport-operateur-negation.md) et
> [`rapport-grappe-intra-couche.md`](../../reports/rapport-grappe-intra-couche.md). Index de la synthèse :
> [`index.md`](index.md).

## La question

L'étage 2 doit **penser sans verbaliser** : lire la réponse dans l'**état**, avant la génération. La carte du
raisonnement (chapitre 5) a montré que **l'état porte** le raisonnement (la sonde, 0,81 au pic du 1,5 B), qu'un
**pont linéaire l'aligne** (0,87) et que le **plan résiste**. La question de ce chapitre est celle des
**opérations** : que devient une opération — la négation — dans l'état ?

## Les six mesures de B4

| la question | la réponse | le chiffre |
|---|---|---|
| l'opérateur est-il une **direction** ? | **non** | 0,4148 (sous le hasard), la garde 0,5852 |
| est-il **apprenable** ? | **oui** | 0,7042 en réentraînant, mais **pas transférable** (0,3312) |
| deux opérations **ensemble** ? | **oui** | 0,7749 / 0,6977 — un **sous-espace** |
| la composition est-elle **algébrique** ? | **non** | 0,5691 (le double nié ne revient pas) |
| est-elle **apprenable** ? | **oui, faiblement** | 0,6174 |
| l'opération apprise dans les **poids** se transfère-t-elle ? | **non — elle s'inverse** | 0,2283 = `1 − 0,7717` |

**La phrase du chapitre** : *l'état porte les opérations, mais il ne les calcule pas.* Les opérations sont des
**géométries apprises**, locales, non compositionnelles gratuitement — la même leçon que le plan (mesure 119) et que
la composition (mesure 81).

## La grappe : le moteur peut ne calculer que 21 %

Le moteur sait ne calculer que les **k** neurones les plus actifs d'une projection (`--act-topk`) :

| k | part des 4 864 | PPL |
|---|---:|---:|
| 64 | 1,3 % | 446 (effondrement) |
| 256 | 5,3 % | 6 918 (effondrement) |
| **1 024** | **21 %** | **30,7286 — la même** |

**La grappe exacte existe à 21 %** : 79 % des neurones FFN ne changent rien sur ce corpus. C'est la **densité
naturelle** des activations (SwiGLU) que la grappe épouse, pas une approximation choisie.

## La sixième mesure : le LoRA, et l'inversion

Le LoRA de la négation (B4.6) entraîne le modèle sur les paires niées. Le résultat : le modèle reste intact
(`reference_orig` 0,8135), l'entraînement converge (la perte 0,0022), et le `flip_sonde` tombe à **0,2283** =
`1 − garde_sonde` (0,7717). Le contrôle (le LoRA entraîné sur les paires **originales**) donne 0,4662 : le LoRA nié a
donc bien appris **quelque chose de spécifique** — mais ce quelque chose est **l'inverse** de la lecture, pas
l'opération. *L'entraînement ne transfère pas l'opération : il retourne la réponse.*

## Ce que les deux disent ensemble

- **Deux sens du mot « structure »**, tous deux mesurables : pour l'étage 2, c'est un **sous-espace appris**
  (B4.3) ; pour le moteur, c'est une **grappe de neurones** (le top-1024). Les deux **coûtent** : la composition
  0,62, la grappe 21 %.
- **La huitième leçon s'applique aux deux** : le point de mesure décide — la sonde de l'original donne 0,41 sur le
  nié, la réentraînée 0,70 ; le top-64 effondre, le top-1024 est exact.
- **Et la thèse tient** : la structure (le sous-espace, la grappe) est ce qui compte, pas la taille — la sonde est
  plate dès le 1,5 B, et la grappe exacte est à 21 %.

## Comment sait-on que c'est vrai ?

- **Les contrôles négatifs** : les étiquettes mélangées (0,46-0,51 partout) ; la garde (le nié relu comme l'original).
- **La reproductibilité** : les scripts sont dans `tools/`, les JSON dans `reports/`.
- **Ce qui pourrait le rendre faux** : la négation de **surface** (« Il est faux que »), les **255 jetons**, la
  **couche 22** et le **0,5 B** uniques ; une PPL identique n'est pas une sortie identique jeton par jeton.
