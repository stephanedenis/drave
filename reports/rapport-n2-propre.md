# N2.h1 — Le corpus propre : la validation n'était pas tenue à l'écart, et la porte honnête vaut 3,09

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : le corpus de N2 se recopiait
> (**32,8 %** des fenêtres de validation étaient verbatim dans l'entraînement) ; dédupliqué, il
> perd **22,2 %** de son texte et la contamination tombe à **zéro**. La chaîne refaite vaut
> **3,0904** en domaine — pas 2,85 — et **16,70** sur de la littérature jamais vue : la
> porte < 2,5 est **redéfinie**, et elle est à **0,59**.

## La question

N2.d a montré que la PPL de N2 se mesurait sur un jeu où un tiers des fenêtres étaient
mémorisables (2,5862 sur les fenêtres contaminées contre 2,9795 sur les propres). La question
n'est plus « quel levier fait baisser la PPL » mais « **quel chiffre dit la vérité** ». Ce travail
construit le mètre, refait la chaîne dessus, et mesure ce que le mètre change.

## Le corpus propre — la méthode

`tools/corpus_propre.py` retire les passages répétés par **shingles de 96 octets** (hachage
roulant de Rabin-Karp, première occurrence gardée, runs ≥ 64 octets joints par `\n`), puis découpe
le texte nettoyé en **chunks contigus de 8 192 octets** dont un sur 20 va en validation, le suivant
en test, le reste en entraînement.

| mesure | avant | après |
|---|---:|---:|
| octets | 4 633 889 | **3 605 306** (−22,2 %) |
| répétitions | 127 blocs contigus, jusqu'à 1 792 octets | — |
| validation verbatim dans l'entraînement | **32,8 %** (42 / 128 fenêtres) | **0 / 2 814** |
| test verbatim dans l'entraînement | — | **0 / 2 814** |
| fenêtres de validation partageant 64 octets avec l'entraînement | — | 2,3 % (résidu de formules) |

Le split : **3 244 858** octets d'entraînement, **180 224** de validation, **180 224** de test.
Manifeste : [`corpus-propre.json`](corpus-propre.json).

## La chaîne refaite

Tout est réentraîné — professeur, base, distillation — pour qu'aucune pièce n'ait vu la validation :

| pièce | valeur |
|---|---|
| professeur | 23,57 M, 20 000 pas, sélection sur un **dev** pris dans l'entraînement |
| base | `drave-n0` 11,47 M, 20 000 pas supervisés, PPL interne **3,7210** |
| distillation | 20 000 pas × 16 × 128 = 41 Mo vus, lr 1e-4 puis 3e-5, **3 graines** |
| curriculum | +10 000 pas à 129, lr 5e-6, **3 graines** |

## Ce qui est mesuré

| bras | graines | val | test | littérature | anglais | wikitext2 |
|---|---:|---:|---:|---:|---:|---:|
| base propre | 1 | **3,2402** | **3,2880** | **12,2861** | **32,9009** | **33,2883** |
| **A — dépôt seul** | 3 | **3,0904** ±0,0048 | **3,1960** ±0,0100 | **16,7034** ±0,2706 | **57,5773** ±2,2054 | **56,8821** ±2,0231 |
| **C — curriculum 129** | 3 | **3,0804** ±0,0103 | **3,1879** ±0,0042 | **16,8172** ±0,3141 | **58,0259** ±1,6809 | **57,7717** ±1,3480 |
| **D — dépôt + littérature** | 3 | **3,2625** ±0,0032 | **3,3221** ±0,0032 | **3,8546** ±0,0026 | **25,6755** ±0,4552 | **26,0589** ±0,3353 |
| ancien témoin 5 000 pas (corpus contaminé) | 1 | — | — | **17,0318** | **51,8854** | **50,7895** |

La **base** et l'ancien témoin de 5 000 pas figurent pour situer : la base n'a aucune distillation,
et l'ancien témoin a été entraîné sur le corpus **contaminé** — sa PPL sur la validation propre
n'est donc pas une mesure honnête, seules ses colonnes hors domaine le sont.

## La porte honnête

Sur le corpus propre, la porte < 2,5 est à **0,59** de l'élève distillé (**3,0904**), et à
**0,70** du test (**3,1960**). Ce n'est pas un échec de réglage : c'est le premier
chiffre de N2 qui ne contienne pas de mémoire. Le **curriculum 129** vaut 3,0804 sur le protocole 128, contre 3,0904 : il ne la
rapproche pas.

Pour situer l'écart avec l'histoire de N2 : la chaîne d'origine, mesurée sur les fenêtres de son
propre jeu qui n'étaient pas dans l'entraînement, valait **2,9795** ; la chaîne propre vaut
**3,0904**, avec **22 % de texte unique en moins** et une sélection plus stricte. Le 2,6998
historique, lui, vient d'une chaîne **huit fois plus longue** (plus de 100 000 pas) mesurée sur le
jeu contaminé : il n'est pas comparable, ni dans un sens ni dans l'autre.

## Hors domaine — un spécialiste du dépôt

Le même élève, sur des textes qu'il n'a jamais vus :

| texte | PPL |
|---|---:|
| validation propre (dépôt) | **3,0904** |
| littérature française (Verne, domaine public) | **16,70** |
| anglais (Wikipédia) | **57,58** |
| wikitext2 (test standard) | **56,88** |

C'est le vrai résultat de la nuit : le modèle de N2 n'est pas un modèle de français, c'est un
modèle **du dépôt**. La PPL en domaine flattait doublement — par la contamination, et par
l'identité de registre.

## La distillation spécialise

Le tableau ci-dessus contient une surprise : la **base supervisée** — qui n'a jamais vu le
professeur — vaut **3,2402** en domaine mais **12,29** sur la littérature et
**32,90** en anglais. La distillation lui fait gagner **−0,150** en domaine et lui
coûte **4,42** hors domaine. Distiller vers un professeur qui ne connaît que le dépôt,
c'est **spécialiser** l'élève : le professeur n'est pas seulement un enseignant, c'est un
**prisme**.

C'est la même leçon que la fiche [`n2-diversite`](rapport-n2-diversite.md), par l'autre bout : ce
n'est pas la distillation qui est en cause, c'est **ce qu'elle distille**.

## La décomposition — où va le calcul

Trois têtes précoces lisent l'état après 2, 4 et 6 blocs ; la tête principale le lit après la
boucle de pensée. Sur la même validation :

| tête | PPL |
|---|---:|
| après 2 blocs | 3,8245 |
| après 4 blocs | 3,2238 |
| après 6 blocs | 3,0462 |
| principale (après pensée) | 3,1162 |
| principale, sans boucle de pensée | 2,36 × 10^7 |

La tête du 6ᵉ bloc, qui lit l'état **avant** la boucle, fait mieux que la principale lue après :
la boucle de pensée transforme l'état mais n'ajoute pas d'information décodable — et sans elle, la
tête principale ne reconnaît plus rien (sa PPL est multipliée par 10⁷). Deux têtes entraînées
différemment (la principale est distillé, la précoce non) : c'est un **indice**, pas une preuve.

## Ce que ça change pour N2

1. **La porte < 2,5 est redéfinie** : elle se mesure sur le corpus propre, et l'élève honnête est à
   3,0904. Le chiffre de référence de N2 n'est plus 2,6998 mais **3,0904**.
2. **Le levier est le corpus, pas le budget** : la chaîne propre, à budget égal, vaut 3,09 ; le
   modèle ne connaît que le dépôt (16,70 sur de la littérature). La fiche
   [`n2-diversite`](rapport-n2-diversite.md) montre ce que la diversité répare, et à quel prix.
3. **Le verrou de longueur** est intact sur le texte propre (14,11 à 256 octets) : la fiche
   [`n2-longueur`](rapport-n2-longueur.md) en donne le mécanisme.
4. **La boucle de pensée** coûte plus qu'elle ne rapporte à la prédiction (indice ci-dessus) : à
   instruire avant de la garder dans les prochains modèles.

## Ce qui pourrait le rendre faux

- **Le résidu de formules** : 2,3 % des fenêtres de validation partagent 64 octets avec
  l'entraînement ; la déduplication est exacte, pas sémantique. La PPL honnête reste une borne.
- **Le corpus est plus petit de 22 %** : la chaîne propre voit moins de texte unique que la chaîne
  d'origine à budget égal — l'écart entre les deux n'est donc pas *seulement* la contamination.
- **Une graine pour la base et le professeur** : la dispersion n'est mesurée que sur la
  distillation (trois graines).
- **Le protocole** : 128 fenêtres de 128 octets (16 384 octets) ; l'écart entre deux tirages vaut
  ~0,02, et l'écart val/test (0,11) montre que le corpus n'est pas homogène.

## Fichiers

- Code : [`tools/corpus_propre.py`](../tools/corpus_propre.py) ·
  [`tools/eval_n2_propre.py`](../tools/eval_n2_propre.py) · agrégat
  [`n2-propre.json`](n2-propre.json).
- Corpus : `data/corpus_propre/` (hors dépôt, manifeste versionné).
- Points de contrôle : `work/n2h/` (14 `.pt`, 903 Mo) archivés sur deux disques —
  `/home/stephane/Data13TB/stephane/backups/n2h/2026-11-01/` et
  `/home/stephane/IA/artefacts/n2h/2026-11-01/`.
