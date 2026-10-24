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

### Le 3 B, même corpus, mêmes références

| modèle | EN→FR | FR→EN |
|---|---:|---:|
| 1,5 B | +35,0 [32,9 ; 37,1] | +39,3 [37,2 ; 41,5] |
| **3 B** | **+38,1** [36,1 ; 40,0] | **+41,3** [39,3 ; 43,2] |

Le 3 B gagne **+2 à +3 points** sur le dialogue — la **traduction profite de la taille**. C'est l'inverse de la
**lisibilité de l'état** (B2.8 : le 3 B y perd 0,10) : deux axes différents, et c'est cohérent avec la carte — la
sonde et le pont mesurent l'**accès** à l'état, pas la **qualité** de la sortie. Un modèle peut mieux traduire en
étant moins lisible.

## Ce que ça change pour la carte des registres

- Le corpus du **dialogue réel** existe (144 dialogues, 5 700+ phrases, l'informel écrit) : la ligne B1.6 n'est plus
  bloquée ;
- avec les **références indépendantes**, la mesure est propre : le **dialogue spontané** est plus facile que les
  sous-titres (+5 à +9 au même modèle), et la case « dialogue » gagne deux niveaux — les sous-titres (écrit et
  contraint) et le spontané (DiaBLa) ;
- la prochaine étape est la récupération des références du GitHub, puis la mesure au **7 B** (le modèle des six
  registres).

**Mise à jour (même jour) — les références indépendantes.** Les `.ref` du GitHub (4 981 paires alignées par le
`eval-filter`) donnent, au même 1,5 B :

| référence de DiaBLa | EN→FR | FR→EN |
|---|---:|---:|
| **indépendantes** (les `.ref`) | **+35,0** [32,9 ; 37,1] | **+39,3** [37,2 ; 41,5] |
| post-édition (la version HF) | +40,3 | +44,2 |
| (rappel) OpenSubtitles | +27,0 | +30,4 |

- **Le biais de la post-édition est réel mais petit** : **+5,3** et **+4,9** points — pas les +13 que la comparaison
  aux sous-titres laissait craindre.
- **Le dialogue spontané reste plus facile que les sous-titres** : +35/+39 contre +27/+30 **au même modèle** — la
  distinction tient ; le dialogue réel a son propre niveau, entre la post-édition et les sous-titres.
- **La carte peut gagner sa ligne « dialogue spontané »** (+35,0/+39,3 au 1,5 B), à côté du « dialogue écrit et
  contraint » des sous-titres ; la réserve restante est le **modèle** (1,5 B ici, 7 B pour la carte des six
  registres).

## Ce que ce résultat ne dit pas

- Un seul modèle (1,5 B), 400 paires par sens — les six registres sont mesurés au 7 B. **Le 7 B n'a pas pu être
  mesuré** ici : 15,2 Go de poids sur 15,55 Go de carte, la marge des activations manque (OOM mesuré, même avec
  l'allocateur extensible) — c'est une limite de la machine, pas du corpus.
- La post-édition peut aussi **aider** le post-éditeur à produire une référence plus fluide que la traduction
  humaine : le biais n'est pas seulement « vers la machine », il est **inconnu** — c'est pourquoi le chiffre ne peut
  pas être comparé, pas seulement « corriger » d'un facteur.
- Les sous-titres et les dialogues n'ont pas les mêmes longueurs (45-51 caractères en moyenne pour DiaBLa) : la
  difficulté du registre et la difficulté de la phrase se confondent encore.
