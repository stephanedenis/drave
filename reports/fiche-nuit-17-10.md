# La nuit du 17 au 18 octobre : la couche commune entrée-sortie, de 2 langues à 448

**État au 18/10, 2 h.** Le chapitre complet est dans
[`docs/synthese/07-modeles-alternatifs-entree-sortie.md`](../docs/synthese/07-modeles-alternatifs-entree-sortie.md) ;
le récit dans [`journal/2026-10-17.md`](../journal/2026-10-17.md) et [`journal/2026-10-18.md`](../journal/2026-10-18.md) ;
l'état courant sur la page d'accueil.

## La question

Une **couche commune entrée-sortie** qui abstrait la langue : l'état d'un modèle peut-il porter le **sens** sans
porter la **langue**, la langue redevenant un **paramètre** à la sortie ? Deux programmes : **deux langues** (le
corpus anglais/français du dépôt) puis **448 langues** (la Déclaration universelle des droits de l'homme).

## L'erratum majeur : le « noyau neutre » était un artefact

Le résultat fondateur du chapitre — « le noyau est neutre, un classifieur de langue y est au hasard (50,2 %),
cinq réplications » — **est retiré** ✗✗. La sonde (`langue_dans_etat.py` v1) concaténait les états anglais puis
français et découpait les **lignes** en deux : l'entraînement portait sur la **première moitié des fenêtres
anglaises** (une seule classe), le test sur un mélange. Sonde corrigée (découpage par fenêtre, standardisation,
contrôle intra-langue, contrôle négatif) :

| modèle | couche 1 | couche 2 | couche 4 | contrôle |
|---|---:|---:|---:|---:|
| mixte prose 256 | **80,4 %** | 82,9 % | 88,5 % | intra-langue 51,7 % |
| mixte prose 512 | **79,4 %** | 83,0 % | 97,5 % | 51,2 % |
| littérature 256 v1 | **84,3 %** | 87,0 % | 90,2 % | 51,0 % |
| littérature 256 v2 | **85,4 %** | 81,5 % | 97,5 % | 50,5 % |
| littérature 512 | **80,1 %** | 94,1 % | 97,6 % | 51,2 % |
| UDHR 448 langues | **98,9 %** | 99,1 % | 99,1 % | négatif 1,5-2,2 % |
| Qwen 0,5 B | **100 %** | 100 % | 100 % | — |

**La langue est lisible partout.** Il n'y a pas de noyau neutre — et les contrôles disent que la sonde corrigée est
juste (intra-langue 50-52 %, étiquettes mélangées 1,5-2,2 %). L'ancien outil est gardé sous
`tools/langue_dans_etat_v1_fautif.py`.

## Le corpus UDHR

`data/udhr/` — **456 fichiers XML**, **448 langues** gardées, **13 222 articles alignés**, **3,57 Mo**, **43
écritures**, **37 langues à plusieurs variantes** (occitan 7, romanche 7, houndé 3, roumain 3…). Alignement vérifié :
corrélation **0,978** de la forme des 30 articles entre langues. Importeurs : `tools/importer_udhr.py` et
`tools/preparer_udhr.py`.

## Les résultats, par régime

| le régime | la mesure | le résultat |
|---|---|---|
| **traduction** (Qwen, 12 paires choisies) | le même article se retrouve-t-il d'une langue à l'autre ? | **96,4 %** · hasard 3,3 % · longueur seule 3-30 % · articles mélangés 0 % ✓✓ |
| **traduction** (Qwen, grille de 40 langues stratifiées) | idem, 780 paires | **14,4 %** (médiane 10 %) · test groupé **6,50 %** contre 0,08 % (contrôle 0,00 %) ✓✗ |
| **traduction** (petit modèle octets, 448 langues, 19 M) | idem | **31 %** sur les paires choisies : il n'aligne que les langues **proches** (romanes 57-87 %), 0-10 % sur les lointaines ✗ |
| **restitution** (modèle spécialisé, 1 langue) | reproduit-il exactement le texte lu ? | **85,1 %** de fragments de 32 octets exacts (français), **99,4 %** d'octets ✓✓ |
| **restitution** (448 langues partagées) | idem | **0,6 %** de fragments exacts, 62,7 % d'octets ✗✗ |
| **courbe de restitution** | 1 → 10 → 50 → 448 langues | **30 % → 4,4 % → 0,4 % → 0,6 %** : la restitution exacte **meurt entre 1 et 10 langues** ✗✗ |
| **dialectes** (7 variantes d'occitan) | lire la variante ? retrouver le contenu ? | **100 %** · **52,2 %** (16× le hasard) ✓✓ |
| **styles** (Odyssée, Butler vs Pope, 25 chants) | lire le traducteur ? retrouver le chant ? | **100 %** · **24 %** (6× le hasard, rang médian 6/25) ✓✓ |

**Et la hiérarchie des surfaces** : langues **96 %** > dialectes **52 %** > styles **24 %**, toutes au-dessus du
hasard — et les trois sont **lues à 100 %** dans l'état. *La couche commune n'efface aucune surface ; elle en aligne
le sens.*

## Ce qui reste vrai du chapitre (et ce qui a changé)

- **la langue est lisible partout** (le noyau neutre est retiré) ;
- **le contenu est aligné malgré elle** : traduction 96 % sur les paires choisies, 14 % sur la grille, 6,5 % dans un
  vivier de 1 200 états (81× le hasard) ;
- **la langue est un petit paramètre de sortie** : 1,33 % des poids, 5 ms de bascule ✓✓ — et il **améliore d'autant
  plus que le noyau est faible** (−53 % sur un modèle faible, −4,7 % sur un bon jouet, −7,6 % sur Qwen ; et sur le
  bon jouet il **abîme** l'autre langue, +10,8 %) ;
- **la pensée itérée est sans langue** (50,6-56,2 % sur huit itérations) mais **ne tient qu'un pas**.

## Les pièges de la nuit (18 en tout, dont 6 nouveaux)

Le **code** qui ment (boucle accumulée) · le **signe** arbitraire d'un classifieur · l'**échantillon** au mauvais
endroit · l'**alignement** accusé à tort · le **corpus mal étiqueté** (`dracula_fr.txt`, `pg2000_en.txt`) · le
**CPU au lieu de la carte** · les **paramètres du LoRA** sur un autre dispositif · le taux de jouet qui **diverge** ·
le **numéro d'article** dans le texte (`itertext` ramassait « Article 2 ») · les articles énumérés hors `<para>` ·
le **seuil script-aveugle** (le chinois rejeté) · la **validation plus courte qu'un lot** (0,0000 et premier point
sauvegardé) · l'**article encodé sans contexte** (restitution impossible par construction) · la **même permutation
pour toutes les langues** (contrôle qui vaut la mesure) · la sonde **v1 fautive** (l'erratum majeur).

## La santé du dépôt

**Passage complet des 46 portes** : à refaire après ces changements (le précédent donnait 44 vertes et les 2 mêmes
rouges connues, `porte-indice` et `porte-melange`).

## Les outils de la série

`importer_udhr.py` · `preparer_udhr.py` · `sonder_udhr.py` (langues, écritures, variantes) ·
`retrieval_udhr.py` (paires, variantes, grille, témoin) · `restitution_udhr.py` (en flux) ·
`style_traducteur.py` (traducteurs) · `udhr_commun.py` · `langue_dans_etat.py` (v2, corrigé).
