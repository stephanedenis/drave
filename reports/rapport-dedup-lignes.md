# N — dédoublonner 7,50 Go par ligne : 24,7 M lignes retirées, 603 Mo (8,04 %), 1 054 Mio de RSS

> **Ligne de roadmap** : N (le palier 1, « la donnée d'abord ») · **Date** : 2026-11-18 ·
> **Verdict** : [`tools/dedup_lignes.py`](../tools/dedup_lignes.py) passe les **7 504 078 589
> octets** de `data/corpus_wiki_fr_texte/train.txt` en **161,1 s de passe** (+ **21,3 s** de
> relecture de vérification, soit **3 min 02 s** au total), avec **1 053,8 Mio de VmRSS** et
> **1 053,4 Mio de `ru_maxrss`** pour un budget de **2 048 Mio** (marge **994 Mio**), et écrit
> **6 900 585 097 octets** (6,43 Gio), sha256
> `e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552`. Il écarte
> **24 676 233 lignes** (**28,005 %**) et **603 493 492 octets** (**8,042 %**), en préservant
> **toutes** les **23 037 969 lignes vides**. La table est **exacte** (pas de filtre de Bloom,
> pas d'éviction ; seules les collisions 64 bits du § 5 restent) : la deuxième passe sur la
> sortie n'écarte **aucune** ligne et rend le **même sha256**. Comparé aux **53,98 % / 8,28 %** du [rapport blocs](rapport-dedup-blocs.md),
> cela donne **54,150 % / 8,349 %** à politique de lignes vides égale (l'outil retire en plus
> les variantes d'espaces de fin), et **28,005 % / 8,042 %** en pratique, parce que les lignes
> vides — 0,307 point d'octets — sont conservées.

Aucun fichier de `data/` n'a été modifié (lecture seule, mtime d'entrée inchangé) ; la sortie
est dans `work/dedup/` (ignoré par git). Aucun appel API, aucun commit.

## 1. Le dispositif

### 1.1 Pourquoi la ligne

[`rapport-dedup-blocs.md`](rapport-dedup-blocs.md) a mesuré que le dédoublonnage **par blocs**
ne retire **rien** sur ce corpus : 112 blocs sur 112 gardés, 0 octet écarté. Le diagnostic
exact du même rapport donne la vraie maille : **53,98 % des lignes** sont des répétitions
exactes, pour **8,28 % des octets**, dont **23,04 M de lignes vides** (26,1 % des lignes,
0,31 % des octets) qui sont des **séparateurs de paragraphes à préserver**. La prochaine
action était donc un dédoublonnage **par ligne, en flux** ; c'est cet outil.

### 1.2 Le pipeline

1. **Lecture en flux.** Itération `for ligne in fichier` sur un lecteur binaire, tampon
   d'entrée de 4 Mio. Aucun fichier entier en RAM, aucune indexation d'offsets.
2. **Normalisation.** Par défaut, seuls les **espaces de fin** sont retirés
   (`ligne.rstrip()`, qui enlève aussi le `\n`, le `\r` d'un CRLF et les tabulations
   finales). `--normaliser` ajoute les **minuscules ASCII** et **compacte** les espaces
   (`b" ".join(ligne.split()).lower()`, qui rogne aussi les bords). La ligne **originale**
   n'est jamais modifiée : la sortie écrit la première occurrence **telle quelle**.
3. **Hachage 64 bits.** `BLAKE2b(digest_size=8)` sur la ligne normalisée. Pas de `hash()` de
   Python : il est **salé par processus**, donc non reproductible d'une passe à l'autre.
4. **Table exacte.** `array('Q')` de `2^n` cases de 8 octets, adressage ouvert linéaire,
   sentinelle 0 (le hachage 0 est remappé à 1). Une ligne dont le hachage est présent est
   **écartée** ; une ligne neuve est **gardée** (première occurrence) puis insérée. Il n'y a
   **pas de faux positifs** comme dans un filtre de Bloom ; seules les collisions 64 bits
   restent (§ 5).
5. **Lignes vides.** Une ligne est « vide » si elle est vide **après** le retrait des espaces
   de fin. Toutes les lignes vides sont **écrites** et **jamais insérées** dans la table :
   ce sont les séparateurs de paragraphes. Une ligne faite uniquement d'espaces est donc
   préservée et comptée dans `lignes_vides`.
6. **Sortie telle quelle.** Les octets de la ligne d'origine (espaces de fin compris,
   `\r\n` compris, dernier saut de ligne absent compris) sont écrits sans réécriture.
7. **Budget.** `--memoire-mo` est un plafond, pas une indication ; le modèle est au § 1.4.
8. **Contrôles.** `--verifier` relit la sortie par blocs de 4 Mio et compare octets, lignes
   et sha256 aux compteurs de la passe ; une divergence est `ERREUR verification_echouee`
   (code 4).

### 1.3 Pourquoi une table exacte, pas un Bloom

Le corpus a **40 400 230** lignes non vides distinctes (mesuré). À 8 octets par case, une
table ouverte à charge 0,30 tient dans **1 GiB** : c'est le choix fait à 2 048 Mio. « Exacte »
veut dire ici : **pas de faux positifs** de Bloom, **pas d'éviction** ; les collisions 64 bits
sont traitées au § 5. Un filtre de Bloom aurait ajouté des **faux positifs** (des lignes
neuves écartées) pour économiser une mémoire dont on n'a pas besoin ici. La table n'évince
rien : la première occurrence est réellement la première, et une troisième copie est bien
écartée même si la deuxième ne l'a pas été. Si la table atteint sa charge maximale (0,8),
l'outil **s'arrête** avec `capacite_depassee` (code 3) au lieu d'oublier des entrées ou de
dépasser le budget.

### 1.4 Le budget, explicitement

```
plancher      = 48 Mio   (interpréteur, 3 tampons de 4 Mio, journal, marge)
octets_table  = (budget − plancher), arrondi à la puissance de 2 inférieure
capacité      = octets_table / 8          (array('Q') : 8 octets par case)
entrées_max   = 0,8 × capacité            (charge maximale, sondage linéaire)
```

À 2 048 Mio : disponible 2 000 Mio, soit 250 M de cases ; la plus grande puissance de 2 est
**2^27 = 134 217 728 cases = 1 GiB** (2^28 ferait 2 GiB, au-delà du budget). La table est donc
à **30,1 %** de charge (40,4 M / 134,2 M) et le RSS mesuré est **1 053,8 Mio**, loin sous le
plafond : le budget est un **plafond**, pas une cible. À 64 Mio : disponible 16 Mio, table
**2^21 = 2 097 152 cases = 16 Mio**, 1 015 997 entrées (48,45 % de charge).

Le chien de garde relit le **VmRSS courant** après l'allocation puis toutes les **65 536
lignes** ; au-delà du plafond, il sort en `ERREUR memoire_depassee` (code 3). Le plafond est
le budget, ou `--test-plafond-mo` (hameçon masqué) pour prouver que le garde-fou sait
échouer. Un budget inférieur à **56 Mio** (plancher 48 + table minimale 8) est refusé au
départ : `ERREUR budget_memoire_impossible` (code 3).

`ru_maxrss` est reporté à part (`ru_maxrss_mio`) : sous Linux, il est **hérité** à travers
fork/exec, donc un enfant lancé depuis un parent gros (l'autotest) lit le pic du parent.
C'est pourquoi le chien de garde utilise le VmRSS ; pour les passes lancées depuis un shell,
les deux mesures coïncident à 0,4 Mio près (1 053,4 Mio ici, confirmé par
`/usr/bin/time -v`).

## 2. Les chiffres

| | preuve budget (200 Mo) | passe principale (7,50 Go) |
|---|---:|---:|
| entrée | `work/dedup/slice-200Mo.txt`, 200 000 000 o | `data/corpus_wiki_fr_texte/train.txt`, **7 504 078 589 o** |
| budget / table | **64 Mio** / 16 Mio (2^21 cases) | **2 048 Mio** / 1 GiB (2^27 cases) |
| **RSS max** (`ru_maxrss`) | **49,5 Mio** | **1 053,4 Mio** |
| RSS max (VmRSS) | 45,6 Mio | 1 053,8 Mio |
| marge sous le budget (`ru_maxrss`) | **14,5 Mio** | **994,6 Mio** |
| durée de la passe | 4,1 s | **161,1 s = 2 min 41 s** |
| vérification (`--verifier`) | 0,9 s | 21,3 s |
| durée totale | 5,0 s | **182,4 s = 3 min 02 s** |
| débit (passe) | 46,9 Mio/s | **44,4 Mio/s** |
| débit (total) | 38,4 Mio/s | 39,2 Mio/s |
| lignes lues | 1 741 349 | **88 114 432** |
| **lignes gardées / écartées** | 1 477 432 / **263 917** | 63 438 199 / **24 676 233** |
| % lignes écartées | 15,156 % | **28,005 %** (37,919 % des non-vides) |
| octets écartés | 7 053 497 (3,527 %) | **603 493 492 (8,042 %)** |
| lignes vides préservées | 461 435 | **23 037 969** |
| octets écrits | 192 946 503 | **6 900 585 097** |
| sha256 de la sortie | `1ec785b6…` | **`e3112a84…`** |
| entrées de table / charge | 1 015 997 / 48,45 % | **40 400 230 / 30,10 %** |

Le temps de la passe principale est **CPU** : 169,97 s d'utilisateur et 8,51 s de système
pour 182,49 s d'horloge (97,8 %) ; le hachage et le sondage dominent, pas les entrées-sorties.
La plus longue ligne du corpus fait **10 389 octets** (5 457 o sur la tranche de 200 Mo) :
le traitement par ligne ne crée donc aucun gros objet, et la mémoire est dominée par la table.
La relecture de vérification a relu **6 900 585 097 octets** et **63 438 199 lignes**, avec
le **même sha256** que l'écriture. `wc -l` et `stat` confirment ces deux valeurs de
l'extérieur, et `sha256sum` confirme le sha256.

Les 8,042 % se lisent : **8,279 %** du diagnostic **− 0,307 point** de lignes vides
préservées **+ 0,070 point** de variantes d'espaces de fin **= 8,042 %**. La sortie fait
**6 900 585 097 o = 91,958 %** de l'entrée ; les 23,04 M de lignes vides pèsent **0,307 %**
des octets.

**Preuve sur 200 Mo.** Budget **64 Mio** — plus serré que les 256 Mio du rapport blocs — pour
une entrée de 200 Mo : `ru_maxrss` **49,5 Mio**, soit **14,5 Mio sous le plafond**, avec une
table de 16 Mio et 1,016 M de lignes uniques. C'est la preuve demandée « sur 200 Mo au moins »,
et elle est plus contraignante que la passe principale (charge 48,45 % contre 30,10 %).

**Idempotence.** Une deuxième passe sur `work/dedup/train-lignes.txt` (6,90 Go) écrit vers
`/dev/null` : **63 438 199 lignes lues, 0 écartée**, **même sha256**
`e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552`, mêmes
6 900 585 097 octets, en 118,5 s, avec le même RSS (1 053,8 Mio de VmRSS, 1 053,4 Mio de
`ru_maxrss`). La sortie ne contient donc **aucune** ligne non vide dupliquée au sens de la
normalisation par défaut, et la passe est déterministe.

## 3. Les contrôles

### 3.1 L'autotest : 16 assertions, toutes vertes

`python3 tools/dedup_lignes.py --autotest` construit un contrôle de **12 lignes / 162 octets**
(dont **4 vides**) et vérifie **16 assertions** ([`autotest.json`](../work/dedup/autotest-lignes/autotest.json)).
Les six cas demandés :

| cas | contenu | attendu | observé |
|---|---|---|---|
| (a) | lignes uniques `alpha` et `beta` | gardées | 6 lignes non vides gardées, sortie exacte (121 o) ✅ |
| (b) | `alpha` puis la **même** ligne | 2ᵉ écartée | 1 écartée, sortie = 1ʳᵉ ligne ✅ |
| (c) | `alpha   ` puis `alpha` (espaces de fin) | 2ᵉ écartée **par défaut** | 1 écartée, sortie = 1ʳᵉ ligne **avec ses espaces** ✅ |
| (d) | `ligne differente beta` | gardée | présente dans la sortie ✅ |
| (e) | 3 `\n` + 1 ligne `   \n` | **4** lignes vides préservées | `vides_lues = 4`, les 4 dans la sortie ✅ |
| (f) | deux passes identiques | même sha256 | `3de1a6d9…` deux fois, sorties identiques ✅ |

Les assertions supplémentaires couvrent : `--normaliser` (4 copies écartées au lieu de 2 :
minuscules `bonjour`/`Bonjour` et espaces compactés, sortie attendue de 87 o, sha stable
`a8667c3c…`) ; `budget_memoire_impossible` (8 Mio → code 3) ; `capacite_depassee` (850 000
lignes uniques dans une table de 2^20 cases → code 3) ; `memoire_depassee` (plafond de test
de 1 Mio → code 3) ; `verification_sortie_ok` (sha relu identique) ; la première occurrence
écrite **telle quelle** ; et une ligne d'espaces préservée comme vide.

### 3.2 Ce que les contrôles prouvent

- **L'outil écarte une copie** exacte et une copie qui ne diffère que par les espaces de fin,
  **garde** une ligne différente, et **préserve** les vides : les six cas sont des contrôles
  positifs et négatifs, pas seulement un test de bout en bout.
- **La sortie est intègre** : relecture indépendante (sha256, octets, lignes), `sha256sum`,
  `wc -l` et `stat` externes. Le sha256 d'entrée est
  `27277e320d7781e0dc8957a449fff386a7d1fa712838bba42f8a1e728dd0924b` ; celui de sortie est
  `e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552`.
- **La sortie est dédupliquée** : la deuxième passe n'écarte rien et rend le même sha256.
- **Le budget est un plafond** : 49,5 Mio sur 64 Mio (200 Mo), 1 053,4 Mio sur 2 048 Mio
  (7,50 Go), et les trois chemins d'erreur mémoire sont exercés pour de vrai.

### 3.3 Budget : la preuve et les refus

- **Preuve 200 Mo** : `--memoire-mo 64` → `ru_maxrss` **49,5 Mio** (VmRSS 45,6), table de
  16 Mio, **14,5 Mio de marge** ; `/usr/bin/time -v` confirme `Maximum resident set size =
  50 688 Kio` = 49,5 Mio. JSON :
  [`prouve-200Mo-lignes.json`](../work/dedup/prouve-200Mo-lignes.json).
- **Passe principale** : `--memoire-mo 2048` → `ru_maxrss` **1 053,4 Mio**, VmRSS 1 053,8,
  **994,6 Mio de marge** ; `/usr/bin/time -v` confirme `1 078 684 Kio` = 1 053,4 Mio. La
  table de 1 GiB explique 1 024 Mio des 1 053 Mio ; le reste (≈ 29 Mio) est l'interpréteur,
  les tampons et la marge.
- **Budget impossible** : `--memoire-mo 8` → `ERREUR budget_memoire_impossible: budget 8 Mio
  < plancher 48 Mio + 8 Mio (table minimale de 1048576 cases à 8 o)`, **code 3**, aucun
  fichier de sortie créé ([`budget-impossible-8.json`](../work/dedup/budget-impossible-8.json)).
- **Capacité dépassée** : 850 000 lignes uniques dans 56 Mio → `ERREUR capacite_depassee`,
  **code 3** (autotest).
- **Chien de garde** : plafond de test de 1 Mio → `ERREUR memoire_depassee`, **code 3**
  (autotest). Un garde-fou qui ne sait pas échouer ne garde rien.

## 4. Comparaison aux 53,98 % / 8,28 % du rapport blocs

Le diagnostic exact du [rapport blocs](rapport-dedup-blocs.md) § 4.3 comptait **toutes** les
lignes, y compris les vides, et ne retirait **pas** les espaces de fin. Il hachait sur
**40 bits** (≈ 3 700 collisions attendues sur 88,1 M de lignes, négligeables devant
150 540) ; ici le hachage est sur 64 bits (≈ 4,4 × 10⁻⁵ collision attendue), donc l'écart
n'est **pas** un artefact de collisions. Voici les deux politiques côte à côte :

| mesure | lignes | % des lignes | octets | % du fichier |
|---|---:|---:|---:|---:|
| diagnostic exact, vides comprises | 47 563 661 | **53,98 %** | 621 277 675 | **8,28 %** |
| diagnostic exact, hors vides | 24 525 693 | 27,834 % | 598 239 707 | 7,972 % |
| **cet outil, effectif** (vides préservées) | **24 676 233** | **28,005 %** | **603 493 492** | **8,042 %** |
| **cet outil, équivalent** (vides dédoublonnées) | **47 714 201** | **54,150 %** | **626 531 460** | **8,349 %** |

La réconciliation est exacte, terme à terme :

| terme | lignes | octets |
|---|---:|---:|
| diagnostic exact (blocs) | 47 563 661 | 621 277 675 |
| − lignes vides préservées | −23 037 968 | −23 037 968 |
| + variantes d'espaces de fin | +150 540 | +5 253 785 |
| **= retiré par cet outil** | **24 676 233** | **603 493 492** |

Trois lectures :

1. **Les 23,04 M de lignes vides sont la différence principale.** Le diagnostic les comptait
   comme 100 % dupliquées (toutes sauf une) ; l'outil les **préserve** toutes. D'où le taux
   effectif de **28,005 %** des lignes au lieu de 53,98 %, et **8,042 %** des octets au lieu
   de 8,28 %. Ce n'est pas un désaccord de mesure : c'est une **politique** — les vides sont
   des séparateurs de paragraphes. Le chiffre de 8,28 % n'est donc pas « atteint » par la
   sortie ; ce qui est retiré, c'est **598,2 Mo de contenu non vide**, plus **5,25 Mo** de
   variantes d'espaces de fin.
2. **Les espaces de fin ajoutent 0,070 point d'octets.** Le diagnostic hachait la ligne brute ;
   l'outil la `rstrip()` d'abord. 150 540 lignes (5,25 Mo, longueur moyenne 34,9 o) ne
   diffèrent que par ces espaces : elles sont écartées en plus. C'est ce qui explique que
   l'équivalent soit à **54,150 % / 8,349 %**, légèrement **au-dessus** du 53,98 % / 8,28 %,
   et non en dessous. Une variante `--normaliser` (minuscules ASCII + espaces compactés)
   écarte encore **164 547 lignes** et **6 528 572 octets** de plus (8,129 % des octets,
   équivalent 54,337 % / 8,436 %), mais coûte **260,8 s** contre 161,1 s : c'est un choix
   éditorial, pas le défaut.
3. **Les lignes longues restent le gros de la prose retirée.** Le diagnostic ventile
   194 315 806 octets (2,59 % du fichier) dans les lignes de 80 o et +. L'outil ne refait pas
   cette ventilation ; les 5,25 Mo supplémentaires ont une longueur moyenne de 34,9 o, donc
   ils sont surtout courts. La masse de prose retirée reste de l'ordre de **2,6 %** du
   fichier, pas de 8 %.

La tranche de 200 Mo confirme aussi l'avertissement du rapport blocs : elle ne perd que
**3,527 %** de ses octets (c'est le début du fichier, avec moins de boilerplate), contre
**8,042 %** sur le fichier entier. Toute mesure sur une tranche **sous-estime**.

## 5. Ce qui pourrait rendre ce résultat faux

- **Collisions 64 bits.** La table ne stocke que 64 bits par ligne. Avec 40 400 230 lignes
  uniques, on attend **4,4 × 10⁻⁵ collision**, soit **0,0044 %** de chance qu'une ligne
  distincte soit confondue avec une autre et écartée à tort. C'est négligeable, mais ce n'est
  pas zéro ; une table à 128 bits doublerait la mémoire **à capacité égale** (2 GiB pour
  2^27 cases), donc diviserait par deux le nombre d'entrées à budget constant, et une
  collision n'est **pas détectable** avec cette structure.
- **Lignes quasi identiques non détectées.** Par défaut, seule la fin de ligne est
  normalisée. Une ligne qui change **un mot, une ponctuation, une casse, un accent ou un
  espace interne** est gardée. Les 150 540 variantes d'espaces de fin montrent que la
  normalisation compte : `--normaliser` en trouve 164 547 de plus, et il ne va toujours pas
  jusqu'aux accents (`É` ≠ `é`), aux variantes Unicode ni aux textes reflués. Une ligne
  répétée mais **coupée différemment** (phrase à cheval sur deux lignes) est invisible.
- **Normalisation.** Le défaut est **conservateur** : espaces de fin seulement, casse et
  espaces internes significatifs. `--normaliser` fait des **minuscules ASCII** (pas Unicode),
  compacte tous les espaces blancs ASCII et rogne les bords ; il peut fusionner des lignes
  que l'on voudrait distinguer. Le choix change le résultat de **0,087 point d'octets** sur
  ce corpus ; il doit être documenté dans toute comparaison.
- **Ordre et première occurrence.** L'outil garde la **première** occurrence dans l'ordre du
  fichier. Si la première est un résumé ou un boilerplate et la seconde une version meilleure,
  c'est la première qui reste. Retirer une ligne au milieu d'un paragraphe peut laisser un
  texte troué ; les vides préservés gardent les frontières de paragraphes, pas la grammaire.
  Ce n'est pas un nettoyage éditorial, c'est un filtre de répétition.
- **Lignes vides.** Les 23 037 969 vides sont **toutes** gardées, y compris les suites de
  plusieurs vides. Le taux de 28,005 % des lignes ne doit pas être comparé directement aux
  53,98 % (qui supprimaient les vides) ; c'est pourquoi les deux taux sont donnés. Une ligne
  faite uniquement d'espaces est classée vide et préservée : sur ce corpus, le compte est
  exactement celui du diagnostic (23 037 969), donc aucune ligne d'espaces seule en plus ici.
- **Budget et capacité.** La table est exacte **tant qu'elle n'est pas pleine** : à 2 048 Mio
  elle peut accueillir 107 374 182 entrées (40,4 M utilisées, **62,4 %** de marge). Avec un
  budget plus petit, l'outil **s'arrête** (`capacite_depassee`) au lieu d'oublier des lignes ;
  ce n'est pas un dédoublonnage « à mémoire constante » pour un corpus arbitrairement grand.
  Le plancher (48 Mio) est une marge au-dessus des ≈ 29–33 Mio mesurés hors table
  (interpréteur + tampons), sur cette machine (CPython 3.13, Linux) ; un autre interpréteur
  ou un autre OS pourrait dépasser, et le chien de garde le dirait **après coup**.
- **Le chien de garde échantillonne.** Il lit le VmRSS toutes les 65 536 lignes ; un pic
  transitoire entre deux mesures ne serait pas vu. Ici, toutes les grosses allocations sont
  faites au départ, et le `ru_maxrss` externe (1 053,4 Mio) confirme le VmRSS. Le champ
  `ru_maxrss` est reporté à part car il est hérité à travers fork/exec : l'autotest, lancé
  depuis un parent gros, le verrait gonflé ; le chien de garde, lui, utilise le VmRSS.
- **La vérification est une intégrité, pas une justesse.** `--verifier` prouve que les octets
  sur disque, les lignes et le sha256 sont ceux annoncés ; l'idempotence prouve qu'il ne
  reste pas de doublon **selon la même normalisation**. Ni l'un ni l'autre ne prouve que la
  définition de « répétition » est la bonne pour l'entraînement.
- **Le corpus n'est pas homogène.** 3,527 % d'octets retirés sur les 200 premiers Mo contre
  8,042 % sur le fichier : une tranche sous-estime. Inversement, un autre corpus (moins de
  boilerplate) pourrait être bien en dessous de 8 %.
- **Ce qui est retiré n'est pas également utile.** Une ligne de tableau, une catégorie, un
  en-tête répété peut avoir du sens à chaque occurrence. Le filtre par ligne ne le sait pas ;
  le retrait de 8 % des octets n'est pas une garantie de qualité. La suite doit mesurer la
  perte (perplexité, échantillon), pas seulement les octets.
- **La sortie n'est pas un texte canonique.** Les lignes gardées sont écrites **telles
  quelles** : les espaces de fin et les `\r\n` d'origine restent, la dernière ligne sans saut
  de ligne reste sans saut. Un consommateur qui compte les lignes ou tokenise doit en tenir
  compte.

## 6. Ce que ça change : le corpus v2 et la suite

**Le corpus v2 est prêt** : `work/dedup/train-lignes.txt`, produit par la passe par défaut
(sans `--normaliser`, 2 048 Mio) depuis l'entrée
`27277e320d7781e0dc8957a449fff386a7d1fa712838bba42f8a1e728dd0924b` (7 504 078 589 o).
Son **épingle** :

| | valeur |
|---|---|
| chemin | `work/dedup/train-lignes.txt` |
| taille | **6 900 585 097 octets** (6,427 Gio) |
| lignes | **63 438 199** |
| sha256 | **`e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552`** |
| entrée | 7 504 078 589 o, sha256 `27277e32…` |
| retiré | 603 493 492 o (8,042 %), 24 676 233 lignes (28,005 %) |
| conservé | 40 400 230 lignes non vides + 23 037 969 vides |

Il vit dans `work/` (ignoré par git), **pas** dans `data/`. Le promouvoir en corpus de
référence demande une copie explicite, la même épingle et un passage en lecture seule — une
décision qui touche `data/`, hors de cette tâche.

**La suite, par ordre de valeur :**

1. **Mesurer la sortie, pas seulement l'entrée.** Compter les jetons de v1 et v2, puis un
   petit entraînement ou une perplexité sur les deux : 8,04 % d'octets en moins ne valent que
   si la qualité ne baisse pas. C'est le miroir entrée/sortie de la méthode.
2. **Décider du filtre éditorial.** Le retrait de toutes les lignes dupliquées enlève aussi
   des lignes de tableau/catégorie. Un filtre « dupliquée **et** longueur ≥ N » est un choix
   différent, à mesurer ; le diagnostic donne 194 Mo (2,59 %) dans les lignes de 80 o et +,
   et 598 Mo (7,97 %) hors vides au total.
3. **Choisir la normalisation en connaissance de cause.** Le défaut est conservateur ;
   `--normaliser` retire 6,53 Mo de plus (0,087 point) mais coûte 1,6× le temps et fusionne
   des lignes que l'on peut vouloir distinguer. Pour un corpus v2 « propre », le défaut est
   le bon point de départ.
4. **Si le quasi-doublon compte, ajouter une passe.** Après cette déduplication exacte, une
   passe par shingles sur v2 dira ce qu'il reste de duplication **diffuse** (le rapport blocs
   mesurait 5,17 % de shingles déjà vus sur v1) ; elle sera plus petite, et c'est elle qui
   justifierait un nettoyage plus agressif.
5. **Ne pas oublier les vides.** Ils sont 26,1 % des lignes et 0,31 % des octets ; les retirer
   ferait gagner peu et casserait les paragraphes. La politique actuelle est de les garder.

À reporter dans `docs/pilotage/en-cours.md` et `docs/pilotage/roadmap.md` par la session
principale : cette tâche ne les touche pas.

## 7. Fichiers et reproduction

- l'outil : [`tools/dedup_lignes.py`](../tools/dedup_lignes.py) (CLI, autotest, erreurs
  nommées, `--verifier`) ;
- la passe : [`reports/dedup-lignes-7.5go.json`](dedup-lignes-7.5go.json) ; la sortie
  [`work/dedup/train-lignes.txt`](../work/dedup/train-lignes.txt) (6 900 585 097 o, sha256
  `e3112a84…`) ;
- la preuve de budget : [`work/dedup/prouve-200Mo-lignes.json`](../work/dedup/prouve-200Mo-lignes.json)
  (200 Mo, 64 Mio, `ru_maxrss` 49,5 Mio) ;
- l'autotest : [`work/dedup/autotest-lignes/autotest.json`](../work/dedup/autotest-lignes/autotest.json)
  (16 assertions) ;
- l'idempotence : [`work/dedup/idempotence-train-lignes.json`](../work/dedup/idempotence-train-lignes.json)
  (0 ligne écartée, même sha256) ;
- la variante normalisée : [`work/dedup/normalise-train-lignes.json`](../work/dedup/normalise-train-lignes.json)
  (sortie vers `/dev/null`) ;
- le refus de budget : [`work/dedup/budget-impossible-8.json`](../work/dedup/budget-impossible-8.json) ;
- le diagnostic exact de référence : [`work/dedup/diagnostic_lignes_exact.py`](../work/dedup/diagnostic_lignes_exact.py) ;
- reproduire :

```bash
python3 tools/dedup_lignes.py --autotest
python3 tools/dedup_lignes.py --entree work/dedup/slice-200Mo.txt \
    --sortie work/dedup/slice-200Mo-lignes.txt --memoire-mo 64 \
    --json work/dedup/prouve-200Mo-lignes.json --verifier
python3 tools/dedup_lignes.py --entree data/corpus_wiki_fr_texte/train.txt \
    --sortie work/dedup/train-lignes.txt --memoire-mo 2048 \
    --json reports/dedup-lignes-7.5go.json --verifier
python3 tools/dedup_lignes.py --entree work/dedup/train-lignes.txt \
    --sortie /dev/null --memoire-mo 2048 \
    --json work/dedup/idempotence-train-lignes.json
```
