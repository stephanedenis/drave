# N — dédoublonner 7,50 Go par blocs : 954 Mio de RSS, 0 bloc écarté, 5,2 % de shingles déjà vus

> **Ligne de roadmap** : N (le palier 1, « la donnée d'abord ») · **Date** : 2026-11-18 ·
> **Verdict** : [`tools/dedup_blocs.py`](../tools/dedup_blocs.py) passe les **7 504 078 589
> octets** de `data/corpus_wiki_fr_texte/train.txt` en **7 min 11 s**, avec **954,3 Mio de RSS
> max** pour un budget de **2 048 Mio** (marge 1 094 Mio), et écrit **7 504 078 589 octets** :
> **112 blocs sur 112 gardés, aucun écarté**. La duplication n'est pourtant pas nulle —
> **4,18 %** des shingles échantillonnés étaient déjà vus avant leur bloc, **5,17 %** en
> comptant les répétitions internes au bloc — mais elle est **courte et diffuse** : 54,0 % des
> lignes sont des répétitions exactes, pour **8,28 % des octets**, surtout des lignes vides et
> du boilerplate. Aucun bloc de 64 Mio n'atteint le seuil de 80 % (le plus chargé est à
> **48,9 %**). Le dédoublonnage **par blocs ne ferme donc pas l'écart du palier 1** : il le
> **chiffre**, et montre que la masse retirable est **par ligne**, pas par bloc.

Aucun fichier de `data/` n'a été modifié ; la sortie est dans `work/dedup/` (ignoré par git).
Aucun appel API, aucun commit.

## 1. Le dispositif

### 1.1 Pourquoi une passe par blocs

`tools/corpus_propre.py` garde **tous** les shingles en mémoire (≈ 80 Go par Go de texte,
mesuré dans [`rapport-n2-corpus-1go`](rapport-n2-corpus-1go.md)) : dédupliquer les 7,50 Go
demanderait ≈ 600 Go de RAM pour 125 Go installés — l'outil ne peut pas passer à l'échelle.
`tools/dedup_blocs.py` renverse le problème : il lit le fichier **en blocs**, décide **bloc par
bloc**, et ne garde en mémoire qu'un **échantillon** des shingles déjà vus, dimensionné par le
budget.

### 1.2 Le pipeline

1. **Découpe.** Blocs de `--bloc-mo` Mio (64), coupés au dernier saut de ligne — 0 coupe au
   milieu d'une ligne sur les 112 blocs de la passe (une ligne plus longue que la moitié du bloc
   forcerait une coupe) — plus une marge de contexte **après** le bloc (2 % du bloc, max 1 Mio)
   qui sert à terminer les fenêtres commencées dans les derniers octets du bloc. Le cœur est ce
   qui sera écrit.
2. **Normalisation.** Minuscules ASCII (`bytes.lower`) et suites d'espaces horizontaux réduites
   (`[ \t\r\f\v]{2,}` → un espace). Les **sauts de ligne sont conservés** : c'est ce qui rend
   l'ancrage possible. Le motif exige 2 espaces ou plus : `+` matcherait chaque espace simple et
   `re.sub` garderait une entrée par occurrence (33 Mio de pic pour 1 Mio de texte, mesuré).
3. **Shingles ancrés.** Fenêtres de `--shingle` octets (96), hachées **BLAKE2b** (64 bits par
   défaut, 32 en option). Les positions sont **définies par le contenu** : début de chaque ligne,
   puis tous les `--pas` octets à l'intérieur de la ligne. Une copie du texte, même insérée à un
   décalage quelconque, produit donc exactement les mêmes fenêtres.
4. **Décision.** Un bloc dont **≥ `--seuil`** (0,8) de ses shingles échantillonnés sont déjà dans
   l'ensemble est **écarté** ; sinon il est **gardé** et ses shingles sont insérés. L'insertion a
   lieu **après** la décision : les répétitions internes à un bloc ne comptent pas comme « déjà
   vu » (un bloc n'est pas écarté à cause de sa propre répétition). Les shingles d'un bloc écarté
   sont quand même insérés, pour qu'une 3ᵉ copie soit écartée même si la 2ᵉ ne l'a pas été.
5. **Budget.** Le taux d'échantillonnage et la capacité du jeu sont calculés **avant** la
   lecture, à partir du budget, de la taille du fichier et du coût mesuré d'une entrée de `set`.

### 1.3 L'ancrage : le point qui a changé le résultat

La première version prenait les fenêtres sur une **grille à pas fixe** ancrée sur les offsets du
fichier — la méthode de l'inventaire. Le contrôle négatif l'a condamnée : une copie exacte
insérée à un décalage qui n'est pas un multiple du pas **ne partage aucune fenêtre** avec son
original (chance 1/pas). Mesuré sur 100 Mo du train
([`work/dedup/diagnostic_ancrage.py`](../work/dedup/diagnostic_ancrage.py)) :

| mode de prélèvement | shingles | déjà vus | taux |
|---|---:|---:|---:|
| grille fixe, pas 96 (méthode de l'inventaire) | 1 041 666 | 412 | **0,04 %** |
| grille fixe, pas 48 | 2 083 332 | 1 531 | 0,07 % |
| **ancres (cet outil)** | 2 436 451 | 10 971 | **0,45 %** |
| toutes les fenêtres, échantillonnées par hachage | 6 252 573 | 38 933 | **0,62 %** |

La grille fixe **sous-estime de 16×** sur cette tranche ; l'ancrage par le contenu est à 0,45 %
de la référence à 0,62 %. C'est pour cette raison que l'outil ancre sur les débuts de ligne et
que les shingles sont échantillonnés par `h & masque == 0` — une condition, elle aussi, définie
par le contenu : une copie est échantillonnée exactement comme son original.

### 1.4 Le budget mémoire, explicitement

Le coût d'une entrée de `set` a été **mesuré** : un `set` de 10 000 000 d'entiers 64 bits atteint
`ru_maxrss` = 757 Mio, soit **79,4 octets par entrée** (table 26,8 + entier 28 + pic du dernier
doublement de table + arènes). Le modèle, dans l'ordre :

```
plancher = 4 × (bloc + recouvrement) + 32 Mio + 48 Mio     # copies transitoires + interpréteur
capacité = (budget − plancher) / 80 octets
p        = plus grande puissance de 2 ≤ 0,5 × capacité / (1,5 × octets / pas)
```

La marge de 0,5 laisse le jeu à la moitié de ce que le budget permettrait : elle absorbe l'écart
entre le coût mesuré (80 o, pic de redimensionnement compris) et le coût réel d'un `set` qui
grandit. À chaque bloc,
le chien de garde relit `resource.getrusage(RUSAGE_SELF).ru_maxrss` et **sort en erreur nommée**
si le RSS dépasse le budget : `ERREUR memoire_depassee`, code 3. Un budget inférieur au plancher
est refusé au départ (`ERREUR budget_memoire_impossible`), et le dépassement de capacité du jeu
a son propre nom (`capacite_depassee`). Rien n'est « supposé » : les trois chemins d'erreur sont
exercés par l'autotest (§ 3.3).

## 2. Les chiffres

Passe principale : `--bloc-mo 64 --memoire-mo 2048 --json reports/dedup-blocs-7.5go.json`.

| | preuve budget (200 Mo) | passe principale (7,50 Go) |
|---|---:|---:|
| entrée | `work/dedup/slice-200Mo.txt`, 200 000 000 o | `data/corpus_wiki_fr_texte/train.txt`, **7 504 078 589 o** |
| bloc / budget | 8 Mio / **256 Mio** | 64 Mio / **2 048 Mio** |
| **RSS max** (`ru_maxrss`) | **120,8 Mio** | **954,3 Mio** |
| marge sous le budget | 135,2 Mio | **1 093,7 Mio** |
| durée | 11,3 s | **430,7 s = 7 min 11 s** |
| débit | 17,3 Mio/s | 16,6 Mio/s |
| blocs | 24 | **112** |
| **gardés / écartés** | 24 / 0 | **112 / 0** |
| octets écrits | 200 000 000 | **7 504 078 589** |
| échantillonnage | 1/8 | 1/32 |
| shingles calculés | 4 830 660 | **191 312 755** |
| shingles échantillonnés | 604 152 | **6 006 207** |
| vus **avant** le bloc | 1,962 % | **4,177 %** |
| vus **avec** répétitions internes | 2,351 % | **5,171 %** |

La sortie est `work/dedup/train.txt`, sha256
`27277e320d7781e0dc8957a449fff386a7d1fa712838bba42f8a1e728dd0924b`, 88 114 432 lignes. Comme
aucun bloc n'a été écarté, elle est **identique à l'octet près** à l'entrée (`cmp` : identique).
Le temps est **CPU** : 419,87 s d'utilisateur pour 430,7 s d'horloge (99 %), 10,91 s de système ;
le hachage domine, pas les entrées-sorties. Le pic RSS de la passe principale est confirmé de
l'extérieur par `/usr/bin/time -v` : `Maximum resident set size (kbytes): 977 200` = 954,3 Mio.

## 3. Les contrôles

### 3.1 Les quatre cas demandés — et deux de plus

`python3 tools/dedup_blocs.py --autotest` construit un fichier de 1 Mio (quatre textes de
262 144 o, paragraphes de 2 048 o) et vérifie **18 assertions**, toutes vertes :

| cas | contenu | attendu | fraction vue | décision |
|---|---|---|---:|---|
| (a) | texte A, 4 blocs | gardé | 0,0 % | ✅ |
| (b) | B = A, copie **exacte** | écarté | **100,0 %** | ✅ |
| (c) | C = A à **9,4 % modifié** (paragraphes entiers remplacés) | écarté à 0,8 | **90,04–90,21 %** | ✅ |
| (d) | D, texte **différent** | gardé | 0,0 % | ✅ |
| (b′) | B précédé de 21 o : copie **décalée** | écarté | 99,92–100 % | ✅ |
| (c′) | A avec **10 % des mots** remplacés, dispersés | **gardé** | 0,99–2,83 % | ✅ |

- **(c) départage le seuil**, comme demandé : à `--seuil 0,95`, C repasse et la sortie devient
  A + C + D (786 432 o au lieu de 524 288 o). La fraction de C dit pourquoi : **90 %** de ses
  shingles sont intacts, donc 0,8 < 0,90 < 0,95.
- **(c′) est le contrôle qui compte** : « 10 % modifié » ne veut pas dire « 90 % vu ». Si les
  10 % sont **dispersés** (mots remplacés dans tout le texte), presque chaque fenêtre de 96 o est
  touchée et la copie est **gardée** (1 à 3 % de shingles vus). La similarité par shingles dépend
  de la **localisation** des modifications, pas seulement de leur quantité.
- **(b′) vérifie l'insensibilité au décalage** : c'est précisément ce qu'une grille fixe rate.
- **Stabilité** : deux passes identiques donnent le même sha256
  (`1a5c01ef8c713c541c0a2ad6f50e2aa4ff4d7ce858a9e4d51e65033f4a402244`), les mêmes décisions et
  les mêmes 524 288 octets ; à `--hash-bits 32`, les 16 décisions sont identiques aussi.
- Le budget est respecté sur le contrôle : RSS 30,9 Mio pour 512 Mio demandés.

### 3.2 Ce que les contrôles ne prouvent pas

Ils prouvent que l'outil **écarte une copie** et **garde un texte neuf**, pas qu'il écarte *tout*
ce qui est dupliqué : une copie plus petite qu'un bloc ne fait jamais tomber le bloc sous 80 %
(c'est le sujet du § 4), et une copie dont les **retours à la ligne** ont changé (texte reflué)
n'est pas reconnue (l'ancrage est sur les débuts de ligne, § 5).

### 3.3 Budget : la preuve et les refus

- **Preuve sur 200 Mo** (≥ 200 Mo demandés) : `--bloc-mo 8 --memoire-mo 256` →
  **RSS max 120,8 Mio** (mesuré par `ru_maxrss` et confirmé par `/usr/bin/time` : 123 676 Kio),
  soit **135 Mio sous le budget**, pour 4,83 M de shingles et 604 152 échantillonnés.
- **Budget impossible**, refusé au départ :
  `--bloc-mo 64 --memoire-mo 64` → `ERREUR budget_memoire_impossible: budget 64 Mio < plancher
  340 Mio (4 × (bloc 64.0 + recouvrement 1.00) + 32 + 48 Mio) + 32 Mio pour le jeu de shingles`,
  code 3.
- **Chien de garde**, déclenché pour de vrai (hameçon de test `--test-plafond-mo 8`) :
  `ERREUR memoire_depassee: RSS max 31 Mio > plafond 8 Mio au bloc 1`, code 3, JSON d'erreur
  écrit. Un garde-fou qui ne sait pas échouer ne garde rien.

## 4. Pourquoi aucun bloc n'est écarté

### 4.1 La distribution par bloc

Les 112 blocs de 64 Mio ont ces fractions de shingles déjà vus (avant le bloc) :
1 bloc à 0 %, 1 dans [0–1 %[, **95 dans [1–5 %[**, 12 dans [5–20 %[, 3 dans [20–50 %[, **aucun
au-delà de 50 %** — le maximum est **48,9 %**. À 64 Mio, un bloc contient ≈ 18 000 articles : il
faudrait que 4 blocs sur 5 soient de la copie pour atteindre 80 %.

### 4.2 La taille de bloc décide de ce qui est retiré

Même tranche de 200 Mo, même outil, quatre tailles de bloc (`work/dedup/granularite/`) :

| bloc | blocs | écartés | octets écartés | part |
|---|---:|---:|---:|---:|
| 64 Mio | 3 | 0 | 0 | 0,000 % |
| 1 Mio | 191 | 0 | 0 | 0,000 % |
| 64 Kio | 2 993 | 0 | 0 | 0,000 % |
| **4 Kio** | 50 837 | **74** | **293 157** | **0,147 %** |

Même à 4 Kio — la taille d'un court article — le seuil de 80 % n'écarte que 0,15 % des octets.
La duplication n'est donc pas « en blocs » : elle est **en lignes**.

### 4.3 La duplication est dans les lignes, et elle est courte

Mesure **exacte** sur les 7,50 Go
([`work/dedup/diagnostic_lignes_exact.py`](../work/dedup/diagnostic_lignes_exact.py),
hachage de chaque ligne, tri de 88,1 M de valeurs, 672 Mio de tableau) :

| catégorie | lignes | déjà vues | % lignes | octets | octets dupliqués | % du fichier |
|---|---:|---:|---:|---:|---:|---:|
| vides | 23 037 969 | 23 037 968 | 100,0 % | 23 037 969 | 23 037 968 | **0,31 %** |
| 1–19 o | 20 689 727 | 16 900 629 | 81,7 % | 243 994 263 | 187 886 634 | **2,50 %** |
| 20–79 o | 23 410 695 | 6 825 264 | 29,2 % | 959 609 824 | 216 037 267 | **2,88 %** |
| 80 o et + | 20 976 041 | 799 800 | 3,8 % | 6 277 436 533 | 194 315 806 | **2,59 %** |
| **total** | **88 114 432** | **47 563 661** | **53,98 %** | **7 504 078 589** | **621 277 675** | **8,28 %** |

**54 % des lignes sont des répétitions exactes, mais 8,28 % des octets** : l'essentiel est fait de
lignes vides (26 % des lignes, 1 octet chacune, séparateurs de paragraphes) et de lignes courtes
de boilerplate. Les lignes de 80 o et + ne sont dupliquées qu'à **3,8 %** — et pèsent 2,59 % des
octets. C'est cette structure qui explique les 5,17 % de shingles vus : les ancres de début de
ligne tombent sur les lignes courtes répétées.

Conséquence directe : un dédoublonnage **par bloc** ne peut pas retirer cette masse (aucun bloc
n'est majoritairement de la copie), alors qu'un dédoublonnage **par ligne** la retirerait —
jusqu'à 621 Mo (8,28 %), dont 23 Mo de lignes vides à préserver comme séparateurs : **598 Mo
de contenu (7,97 %)**, dont 194 Mo de lignes longues (2,59 %), en gardant la première
occurrence. C'est la prochaine étape naturelle, et elle coûte **2 min 30 s** et 3,4 Gio de RSS
pour la version triée (celle du diagnostic ci-dessus) ou ≈ 2 min en flux avec un `set`
échantillonné comme l'outil.

## 5. Ce qui pourrait rendre ce résultat faux

- **Shingles 32 bits = collisions.** En 64 bits, les collisions sont négligeables (7 M d'entrées
  → 7e6²/2⁶⁵ ≈ 10⁻⁶). En 32 bits, avec ≈ 7 M d'entrées échantillonnées et 181 M de requêtes,
  on attend ≈ 181e6 × 7e6/2³² ≈ **295 000 faux « déjà vus »**, soit **+0,16 point** sur un taux
  de 5 % — l'option `--hash-bits 32` gonfle donc la mesure, elle ne la casse pas.
- **L'échantillonnage.** 6 006 207 shingles échantillonnés (1/32) : l'erreur-type sur 5,17 % est
  ≈ 0,009 point, négligeable. Mais les ancres ne sont **pas** un tirage uniforme des positions :
  sur 100 Mo, les ancres donnent 0,45 % là où toutes les fenêtres donnent 0,62 % (facteur 0,73),
  et sur 20 Mo elles donnaient l'inverse (0,32 % contre 0,24 %). Le 5,17 % est un **ordre de
  grandeur**, pas une mesure au dixième.
- **Le décalage des copies est traité, le refluage ne l'est pas.** Une copie dont les retours à
  la ligne diffèrent (texte reflué, lignes fusionnées) n'a plus les mêmes ancres : elle est
  invisible. Une copie qui commence au milieu d'une ligne perd sa première ligne, pas les
  suivantes. Et un bloc coupé au milieu d'une ligne (impossible ici, possible à 4 Kio) décale
  les ancres de cette ligne.
- **Un bloc qui coupe un doublon à cheval.** Les blocs sont coupés sur des `\n` : aucune ligne
  n'est coupée, et la marge de contexte (1 Mio) termine toutes les fenêtres. Mais la **décision**
  reste par bloc : un doublon réparti sur deux blocs ne pèse que sa part dans chacun. C'est le
  § 4, pas un bug.
- **La taille de bloc change le taux mesuré** : sur la même tranche de 200 Mo, 1,59 % de shingles
  vus à 64 Mio, 2,45 % à 4 Kio (les répétitions internes au bloc ne sont pas comptées comme
  « déjà vu » avant la décision). Comparer deux chiffres exige la même taille de bloc.
- **Normalisation.** Les minuscules ne sont qu'**ASCII** : `É` (UTF-8) n'est pas `é`, donc
  « Étoile » et « étoile » ne se rencontrent pas. Les espaces horizontaux sont réduits, les
  sauts de ligne conservés. Une normalisation Unicode complète augmenterait un peu le taux.
- **Le corpus n'est pas homogène.** La tranche de 200 Mo est le **début** du fichier (articles
  anciens, peu de boilerplate) : 3,74 % d'octets dupliqués par ligne ; une tranche au milieu
  (3,5 Go) en donne 5,08 %, et le fichier entier 8,28 %. Toute mesure sur une tranche
  **sous-estime**.
- **Le modèle de budget** repose sur 80 octets par entrée, mesurés ici (CPython 3.13, Linux). Un
  autre interpréteur pourrait dépasser : le chien de garde le dirait (`memoire_depassee`), mais
  après coup.
- **Une sortie identique n'est pas un nettoyage.** Les 7 504 078 589 octets écrits sont
  l'entrée à l'octet près : la passe ne perd rien, mais elle ne retire rien non plus.

## 6. Comparaison avec les 2,0 % de l'inventaire

L'inventaire ([`rapport-donnees-inventaire.md`](rapport-donnees-inventaire.md) § 1) a mesuré
**2,93 %** de shingles déjà vus sur les 7,50 Go (pas de 96 o, CRC32) puis corrigé les collisions
32 bits pour annoncer **≈ 2,0 %** de duplication réelle. Le tableau ci-dessous met les méthodes
côte à côte.

| mesure | portée | taux |
|---|---|---:|
| grille fixe pas 96 (méthode de l'inventaire) | 100 Mo | **0,04 %** |
| grille fixe pas 96 (inventaire, publié) | 7,50 Go | 2,93 % |
| ancres, avant le bloc (cet outil) | 7,50 Go | **4,18 %** |
| ancres, avec répétitions internes (cet outil) | 7,50 Go | **5,17 %** |
| lignes déjà vues (exact) | 7,50 Go | 53,98 % des lignes = **8,28 % des octets** |
| lignes de 80 o et + déjà vues (exact) | 7,50 Go | 3,8 % des lignes = **2,59 % des octets** |

Trois écarts, dans cet ordre d'importance :

1. **La grille fixe sous-estime.** Une copie décalée de d octets ne partage une fenêtre que si
   d ≡ 0 (mod pas) : 1 chance sur pas. Sur 100 Mo, la méthode de l'inventaire trouve 0,04 % là où
   la référence « toutes les fenêtres » trouve 0,62 % — **16×**. Le facteur n'est pas constant :
   à 7,50 Go, le foisonnement des répétitions fait coïncider des positions par hasard, et l'écart
   retombe à ≈ 1,8× (2,93 % contre 5,17 %). C'est pourquoi la correction de collisions de
   l'inventaire (711 000) est juste dans son cadre mais ne sauve pas le chiffre : le cadre est
   biaisé.
2. **La définition n'est pas la même.** L'inventaire compte des fenêtres de 96 o **non
   chevauchantes** ; l'outil compte des fenêtres **ancrées sur les lignes**, échantillonnées par
   hachage, avec normalisation. Les chiffres entre 2 et 5 % mesurent des choses voisines, pas
   identiques ; le seul chiffre **exact** de cette fiche est la mesure ligne à ligne (8,28 % des
   octets, 3,8 % des lignes longues).
3. **La masse retirable n'est pas celle annoncée.** L'inventaire en déduisait « il reste ≈ 7,2–7,35
   Go après déduplication ». Par **bloc**, il reste **7 504 078 589 octets** (rien) ; par
   **ligne**, on retirerait jusqu'à 621 Mo (8,28 %), dont 23 Mo de lignes vides (à garder) et
   194 Mo de lignes de 80 o et + (2,59 %).
   L'estimation de l'inventaire (≈ 2 %) est donc du bon ordre pour la **prose dupliquée**
   (2,59 %) mais elle rate la masse des lignes courtes et elle est obtenue par une méthode qui,
   sur une tranche, se trompe d'un facteur 16.

## 7. Ce que ça change

- **L'outil est le bon bâtiment, la mauvaise maille.** `tools/dedup_blocs.py` prouve qu'on peut
  traverser 7,50 Go en 2 Go de RAM, décider de façon déterministe et rendre des erreurs nommées.
  Mais la décision par bloc de 64 Mio est un **no-op** sur ce corpus : il ne faut pas construire
  le corpus v2 avec.
- **La duplication réelle est plus grande que 2 %, et plus courte.** 54 % des lignes, 8,28 % des
  octets ; pour les lignes de 80 o et +, 3,1 % de leurs octets (194 Mo, 2,59 % du fichier).
  La prochaine action est un dédoublonnage **par ligne** en flux, avec le même modèle de budget :
  hacher chaque ligne, garder la première occurrence (en préservant les séparateurs vides), et
  mesurer ce qui reste. Le diagnostic exact de cette fiche en donne le coût : 2 min 30 s et
  3,4 Gio de RSS pour la version triée, ou ≈ 2 min et un `set` échantillonné en flux.
- **Le chiffre de l'inventaire est à corriger** dans les documents de pilotage : 2,0 % est une
  sous-estimation (méthode à grille fixe) et la masse retirable par ligne est plutôt de 8 % des
  octets (598 Mo hors lignes vides), dont 2,6 % de prose. La conclusion de l'inventaire — « le
  volume est là, il faut l'outiller » — reste vraie ; c'est la nature du dédoublonnage qui change :
  par ligne, pas par bloc.
- **Ce qui n'est pas tranché** : retirer 8,28 % des octets en supprimant les lignes répétées
  enlève aussi des lignes de tableau et de catégorie qui ont un sens ; un filtre « lignes
  dupliquées + longueur ≥ N » est un choix éditorial, à mesurer sur une perte de qualité, pas
  seulement sur des octets.

## 8. Fichiers

- l'outil : [`tools/dedup_blocs.py`](../tools/dedup_blocs.py) (CLI, autotest, erreurs nommées) ;
- la passe : [`reports/dedup-blocs-7.5go.json`](dedup-blocs-7.5go.json) ; la sortie
  `work/dedup/train.txt` (7 504 078 589 o, sha256 `27277e32…`) ;
- la preuve de budget : `work/dedup/prouve-200Mo.json` (200 Mo, 256 Mio, RSS 120,8 Mio) ;
- le contrôle négatif : `work/dedup/controle/autotest.json` et `controle.txt` ;
- les diagnostics : `work/dedup/diagnostic_ancrage.py` (grille vs ancres),
  `work/dedup/diagnostic_lignes_exact.py` (duplication ligne à ligne, exacte),
  `work/dedup/granularite/bloc-*.json` (quatre tailles de bloc) ;
- reproduire : `python3 tools/dedup_blocs.py --autotest` puis
  `python3 tools/dedup_blocs.py --entree data/corpus_wiki_fr_texte/train.txt --sortie
  work/dedup/train.txt --bloc-mo 64 --memoire-mo 2048 --json reports/dedup-blocs-7.5go.json`.
