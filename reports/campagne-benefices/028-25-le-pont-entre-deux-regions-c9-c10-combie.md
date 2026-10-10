> Campagne : **campagne-benefices** · expérience **25**
> Titre : 25. Le pont entre deux régions (C9/C10) : combien de fibres, et à quel prix
> Date réelle : **2026-10-10 10:18 HAE** (source : commit `4a8cac9`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 25. Le pont entre deux régions (C9/C10) : combien de fibres, et à quel prix

Ajouté dans le sprint « cerveau ». La question est celle du **corps calleux** : deux
régions d'un modèle échangent un état à chaque pas ; combien faut-il en échanger pour
ne rien perdre ? `--pont-k K` ne garde que les K plus grandes amplitudes de l'état
échangé, **dans les deux sens** (le nœud reçoit le même réglage), et le moteur publie
les **octets réellement échangés**. Modèle 0,5 B, 896 canaux, 48 pas, région locale
= couches 0-11, distante = 12-23.

**D'abord un piège, mesuré : en dense f32, élaguer ne réduit AUCUN octet.** Le flux
envoie 896 valeurs, que 448 d'entre elles soient nulles ou non :

| encodage | fibres | perplexité | octets/flux (aller) | écart |
|---|---|---|---|---|
| dense f32 | 896 | 113,0068 | 3 664 | — |
| dense f32 | **448** | **121,8551** | **3 664** | **+7,83 % pour zéro octet gagné** |
| dense f32 | 224 | 248,5349 | 3 664 | +119,9 % |
| listes par blocs | 896 | **111,9225** | 1 951 | — |
| listes par blocs | 672 | 112,9891 | 1 543 | +0,95 % |
| listes par blocs | **448** | **115,0632** | **1 096** | **+2,81 %, ÷1,8 en octets** |
| listes par blocs | 224 | 233,8589 | 648 | +108,9 % |
| listes par blocs | 112 | 1 153,3098 | 424 | +930,5 % |

**C'est l'encodage qui convertit la parcimonie en octets**, pas le pont. La courbe
utile est donc celle en « listes par blocs » (2 octets par neurone actif, indices par
écarts), et elle dit trois choses :

1. **on peut couper le corps calleux en deux** : 448 fibres sur 896 coûtent **+2,81 %**
   de perplexité et **÷1,8** en octets par pas (1 951 → 1 096) ;
2. **on ne peut pas le couper en quatre** : entre 448 et 224 fibres, la perplexité
   passe de +2,81 % à **+108,9 %** — la falaise est nette, et elle est **entre** ces
   deux points ;
3. **la falaise est localisée, et c'est une MARCHE, pas une pente** : entre 448 et
   392 fibres, le coût passe de **+2,81 %** à **+25,35 %** — soit neuf fois plus de
   dégradation pour 11 % de fibres en moins :

   | fibres | perplexité | octets/flux | écart |
   |---|---|---|---|
   | 896 | 111,9225 | 1 951 | — |
   | 560 | 114,2250 | 1 319 | +2,06 % |
   | **448** | **115,0632** | **1 096** | **+2,81 %** |
   | **392** | **140,2979** | **984** | **+25,35 %** |
   | 336 | 150,1778 | 872 | +34,18 % |
   | 280 | 166,0824 | 760 | +48,39 % |
   | 224 | 233,8589 | 648 | +108,95 % |

   Une marche à cet endroit dit quelque chose de précis : l'état au point de coupe a
   de l'ordre de **450 canaux porteurs**, et en dessous on entame le signal, pas le
   bruit ;
4. **à budget d'octets égal, élaguer est bien moins efficace que quantifier** :
   le rendement (perplexité pour 1 000 octets) est de 57,4 pour l'encodage complet
   contre 105,0 pour le pont de 448 fibres — **83 % pire**. Autrement dit : garder
   tous les canaux et réduire leur précision vaut mieux que jeter la moitié des
   canaux, sur ce lien comme sur les poids.

**Ce que la porte verrouille** (`tools/porte-pont.sh`, 7 cas) : pont entier ≡ sans
pont **dans les deux encodages** (perplexité identique) · les deux sens **maigrissent**
quand on élargit le pont · la courbe est **monotone** en les fibres (5 points) ·
élaguer **coûte** (sinon le pont n'est branché nulle part) · et le piège du dense f32
est vérifié comme tel (mêmes octets, perplexité pire).

**Ce qu'il faut en retenir pour distribuer** : sur ce modèle et ce découpage,
**garder tous les canaux et les quantifier** (listes par blocs, 2 octets par neurone
actif) donne la meilleure qualité par octet ; si le lien est vraiment contraint,
**couper à 448 fibres sur 896** (la moitié) coûte +2,81 % et divise les octets par
1,8 ; **ne pas descendre sous 448** — la marche est juste en dessous. Et si le lien
est dense (f32), élaguer ne sert à rien : cela ne fait que perdre.

**Conditions** : un seul modèle (0,5 B, 24 couches, découpage 12/12), 48 pas,
`--limit 48`, liaison locale TCP. Le pont n'est pas testé sur un modèle plus grand —
où la largeur d'état est plus grande, donc où le même *nombre* de fibres représente
une fraction plus petite ; ni sur un découpage différent (le point de coupe change la
largeur utile de l'état).
