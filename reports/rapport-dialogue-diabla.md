# Le dialogue réel (DiaBLa) : +40,3 / +44,2 au 1,5 B — mais la référence est une **post-édition**, pas une traduction

> Mesures du 24/10/2026, Qwen2.5-**1.5B**-Instruct, 400 paires par sens, le protocole des six registres (chrF,
> plancher, marge, IC bootstrap). **DiaBLa** : 4 910 paires de dialogues spontanés FR/EN, référence = les
> **post-éditions humaines** des sorties de TA ; **OpenSubtitles** : les sous-titres, référence = les **traductions
> humaines** — mesuré au **même** modèle pour que la comparaison des registres soit possible.

## Les résultats

| corpus | sens | chrF | plancher | **marge** | IC 95 % |
|---|---|---:|---:|---:|---:|
| **DiaBLa** | EN→FR | 57,55 | 17,24 | **+40,3** | [38,0 ; 42,3] |
| **DiaBLa** | FR→EN | 62,58 | 18,38 | **+44,2** | [42,1 ; 46,2] |
| OpenSubtitles | EN→FR | 44,2 | 17,2 | +27,0 | [25,4 ; 28,7] |
| OpenSubtitles | FR→EN | 47,6 | 17,2 | +30,4 | [28,4 ; 32,2] |

À première vue, le **dialogue spontané serait plus facile que les sous-titres** (+40/+44 contre +27/+30, un écart de
**+13 à +14**).

## La réserve, avant la conclusion

**La référence de DiaBLa n'est pas une traduction indépendante** : c'est la **post-édition** des sorties d'un système
de TA — le texte humain *corrigé à partir de la machine*. Le modèle testé produit, lui aussi, de la TA : sa sortie
**ressemble** à celle que le post-éditeur a corrigée, donc la marge est **mécaniquement gonflée**. Ce n'est pas la
même mesure que les sous-titres, dont la référence est humaine et indépendante.

- **+40/+44 est une borne HAUTE** du dialogue réel, pas sa mesure ;
- **+27/+30** (OpenSubtitles) est une borne basse (les sous-titres sont du parlé écrit et contraint) ;
- la vraie valeur du dialogue spontané est **entre les deux**, et elle demande les **références indépendantes** que
  le corpus annonce (« reference translations produced a posteriori ») — elles sont dans le dépôt GitHub du corpus
  (`rbawden/DiaBLa-dataset`), pas dans la version HuggingFace utilisée ici.

## Ce que ça change pour la carte des registres

- Le corpus du **dialogue réel** existe (144 dialogues, 5 700+ phrases, l'informel écrit) : la ligne B1.6 n'est plus
  bloquée ;
- **on ne l'ajoute pas** à la carte des six registres tant que la référence n'est pas indépendante : la case
  « dialogue » reste tenue par les sous-titres (+32,3/+33,6 au 7 B), et DiaBLa est une **borne haute** documentée ;
- la prochaine étape est la récupération des références du GitHub, puis la mesure au **7 B** (le modèle des six
  registres).

**Mise à jour (même jour)** : les références indépendantes ont été récupérées (`raw-corpus/*.ref`, alignées par le
`eval-filter` : **4 981 paires**, vérifiées sur les premières lignes) et la mesure au même 1,5 B est **en cours** —
elle dira si l'écart de +13 à +14 avec les sous-titres était le registre ou le biais de la post-édition.

## Ce que ce résultat ne dit pas

- Un seul modèle (1,5 B), 400 paires par sens — les six registres sont mesurés au 7 B.
- La post-édition peut aussi **aider** le post-éditeur à produire une référence plus fluide que la traduction
  humaine : le biais n'est pas seulement « vers la machine », il est **inconnu** — c'est pourquoi le chiffre ne peut
  pas être comparé, pas seulement « corriger » d'un facteur.
- Les sous-titres et les dialogues n'ont pas les mêmes longueurs (45-51 caractères en moyenne pour DiaBLa) : la
  difficulté du registre et la difficulté de la phrase se confondent encore.
