# Partition des syntagmes — cartographie, deux options mesurées, recommandation

**P0-3 · ligne B13 · branche `s/v7` · 6 novembre 2026**

**Mesures épinglées au commit `fa1b0c6eb90b3d27ec78f946d677817ba08b419e`** (le dépôt a bougé
pendant la mesure ; voir § 1.1). Module épinglé :
`tools/bloc_linguistique.py`, sha256 `5954d0870bb957472662047ba40d027ea8f64e9434ecb24217faa9337437b08f`.
Harnais local non committé dans `/tmp/pin_audit` et `/tmp/partition_syntagmes`.

> **Verdict.** Les **239 paires** de chevauchement des deux bancs (107 + 132) sont **toutes** des
> paires **S × chunker** : aucune paire S×S, aucune paire chunker×chunker. **53,1 %** sont le cas
> canonique « le S contient le chunker », **33,5 %** l'inverse, **2,5 %** des mêmes bornes
> multi-label, **10,9 %** des croisements. L'alternative étiquetée **(A)** ne perd rien
> (F1 0,5849, exact **222/239**) ; le filtre union **partiel (B1)** coûte **5** attachements exacts
> (222→217) et laisse **91** paires ; la **partition stricte (B2)** coûte **17** (222→205) et
> supprime les 239 paires ; la déduplication silencieuse en coûte **14** (222→208). Recommandation :
> **A par défaut, B2 en option « partition », B1 documenté comme variante économique partielle.**

## 0. Résumé en une page

| question | réponse |
|---|---|
| Combien de paires, où ? | **239 paires** dans **54/96** textes des bancs (107/23 + 132/31) ; **59** paires dans 10/25 paragraphes libres |
| Quelles classes ? | **127** S ⊃ chunker, **80** chunker ⊃ S, **6** mêmes bornes, **26** croisements |
| Origine ? | **100 %** des paires opposent un S à un union ; chunker seul = **0** paire, S sans union = **0** paire |
| Option A (explicite) | F1 **0,5849**, exact **222/239**, POS **0,7581** ; **+10,4 %** de JSON ; 894 vues |
| Option B1 (filtre union) | F1 **0,6163**, exact **217/239**, reste **91 paires** ; **+7,2 %** de JSON |
| Option B2 (partition stricte) | F1 **0,6172**, exact **205/239**, **0 paire** ; **+2,0 %** de JSON |
| Référence déduplication | F1 **0,6141**, exact **208/239**, 0 paire, **silencieuse** |
| Contrôle négatif | 299 suppressions au hasard : F1 **0,5519** (max 0,5638), exact **193,15** (max 198) — le filtre est bien ciblé |
| Recommandation | **A par défaut** ; **B2** pour une vue strictement linéaire ; **B1** pour « moins de chevauchements » sans promesse de partition ; jamais la suppression silencieuse |

## 1. Dispositif

### 1.1 Pourquoi épingler

Les deux audits ont été mesurés à des commits différents, et le dépôt a continué de bouger pendant
cette étude (HEAD `ba39a7b1` au moment de la rédaction ; le gold a été corrigé après l'audit,
le commit `c5b80dd8` annonce 226/226 attachements exacts). Pour comparer les options **au même état** et
retrouver les chiffres publiés, tout est épinglé à `fa1b0c6e` :

| élément | valeur |
|---|---|
| module | `tools/bloc_linguistique.py` @ `fa1b0c6e`, sha256 `5954d087…37b08f` |
| générateur S | `tools/structures/generateur.py` @ sous-module `523d8c1e`, sha256 `291df65a…765202d5` |
| gold | `tools/tests/linguistique/gold{,_reel,_synthetique}.json` @ `fa1b0c6e`, 612 phrases, **239** cibles d'attachement |
| bancs | les 46 succès de `pensee-fiabilite-produit.json` + les 50 de `pensee-produit-bloc-l.json` |
| textes libres | 25 paragraphes de `data/corpus_fr_litterature.txt`, échantillon déterministe, hors gold |

Le patch proposé s'applique aussi au HEAD `ba39a7b1` (`patch -p1 --dry-run` : hunks à
+262/+312/+314/+321 lignes ; testé aussi à `d73e7d1f` et `5c5d3b52`). Les chiffres de ce rapport sont ceux du commit d'audit, pas ceux du HEAD.

### 1.2 Validation du harnais : les chiffres des audits sont reproduits

| grandeur | audit 1 (`fiabilite`) | reproduit | audit 2 (`bloc_l`) | reproduit |
|---|---:|---:|---:|---:|
| paires | 107 | **107** | 132 | **132** |
| textes à chevauchement | 23/46 | **23/46** | 31/50 | **31/50** |
| syntagmes | 360 | **360** | 362 | **362** |
| étiquettes `meta.union` | 85 | **85** | 98 | **98** |
| attachements | 284 | **284** | 265 | **265** |
| étiquettes syntagme impliquées | — | **170/360** | 188/362 | **188/362** |
| mêmes types / types différents | — | **70/37** | 61/71 | **61/71** |
| inclusions / partiels | — | **100/7** | 113/19 | **113/19** |

L'audit 2 compte **113 inclusions** = 67 (S ⊃ chunker) + 43 (chunker ⊃ S) + 3 (mêmes bornes), et
**19 croisements** : la taxonomie de ce rapport retrouve exactement ces chiffres. L'audit 1 ne
publiait pas le découpage inclusions/partiels ; il vaut **100/7** (60 + 37 + 3, puis 7).

### 1.3 Harnais et reproduction

Tout est local, hors dépôt :

```bash
PIN=/tmp/pin_audit python3 /tmp/partition_syntagmes/inventaire.py   # cartographie
PIN=/tmp/pin_audit python3 /tmp/partition_syntagmes/options.py      # variantes mesurées
python3 /tmp/partition_syntagmes/patch_eval.py                      # patch + contrôles
python3 /tmp/partition_syntagmes/stats_finales.py                   # lisibilité, invariants
```

Les scripts lisent les JSON d'audit du dépôt et n'écrivent que dans `/tmp`. **Aucun fichier existant
n'est modifié par cette étude, aucun commit n'est fait.**

## 2. Cartographie des chevauchements

### 2.1 Effectifs

| banc | textes | succès | textes à chevauchement | paires | syntagmes | union | attachements | labels impliqués | mêmes types / différents |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| audit 1 `fiabilite` | 50 | 46 | **23** | **107** | 360 | 85 | 284 | **170** (47,2 %) | 70 / 37 |
| audit 2 `bloc_l` | 50 | 50 | **31** | **132** | 362 | 98 | 265 | **188** (51,9 %) | 61 / 71 |
| **total bancs** | **96** | **96** | **54** | **239** | **722** | **183** | **549** | **358** (49,6 %) | **131 / 108** |
| libres (25 paragraphes) | 25 | 25 | **10** | **59** | 233 | 47 | 179 | **93** (39,9 %) | 35 / 24 |

Les 239 paires ne sont pas 239 paires indépendantes : elles forment **119 composantes** de
2 à 7 segments sur les bancs (53 groupes de 2, 38 de 3, 9 de 4, 13 de 5, 5 de 6, 1 de 7). Le plus
gros texte est `f50` (50 paires, 171 syntagmes, 152 vues en mode A) ; `x50` suit (16 paires).

### 2.2 Les quatre classes

| classe | définition | audit 1 | audit 2 | total | part | libres | part libres |
|---|---|---:|---:|---:|---:|---:|---:|
| `union_contenu` | **le S contient le chunker** (union) ; le chunker est un fragment | 60 | 67 | **127** | **53,1 %** | 24 | 40,7 % |
| `inclusion_s_dans_union` | **le chunker est plus large que le S** ; le S est un fragment | 37 | 43 | **80** | **33,5 %** | 24 | 40,7 % |
| `meme_span_union` | mêmes bornes, types différents, dont un union (multi-label) | 3 | 3 | **6** | **2,5 %** | 3 | 5,1 % |
| `croisement` | ni inclusion ni mêmes bornes ; les spans se croisent | 7 | 19 | **26** | **10,9 %** | 8 | 13,6 % |
| **total** | | **107** | **132** | **239** | 100 % | **59** | 100 % |

Deux faits structurants :

1. **Toutes les paires opposent exactement un S et exactement un segment union.** Il n'y a ni paire S×S, ni
   paire union×union, ni paire d'inclusions à deux sources non-union. Le défaut est donc **la
   composition** (l'union S + chunker), pas le générateur S ni le chunker : `segmenter_s=False,
   union=False` donne **0 paire** (611 syntagmes) et `union=False` donne **0 paire** (725 segments).
2. **Le cas canonique « le S contient le chunker » n'est que la moitié** (53,1 %) ; **un tiers** est
   l'inverse (le chunker est plus large) et **10,9 %** sont des croisements. Un filtre qui ne traite
   que le cas canonique laisse donc mécaniquement des paires (voir B1).

### 2.3 Exemples, un par classe

| classe | texte | segment S | segment union | lecture |
|---|---|---|---|---|
| `union_contenu` | audit 1 `f06` | `GV 43-60` « nous verrons bien » | `GV 48-60` « verrons bien » | le chunker est un **fragment** du GV S |
| `inclusion_s_dans_union` | audit 1 `f02` | `REL 22-42` « qui dort sur le toit » | `REL 22-54` « qui dort sur le toit se réveille » | le chunker **ajoute** « se réveille » à la relative |
| `meme_span_union` | audit 2 `f02` | `GP 68-78` « au travail » | `GV 68-78` « au travail » | même span, deux **lectures** (lieu / GV) |
| `croisement` | audit 1 `f06` | `GV 0-15` « Je ne pense pas » | `GV 3-36` « ne pense pas qu'il viendra demain » | le chunker absorbe la complétive et rogne le sujet |

Le cas `meme_span_union` n'est pas une erreur de span : c'est un **multi-label assumé** (un GP et un
GV sur le même texte), que le client doit pouvoir distinguer. Les 6 paires de ce type sont toutes
`union` contre S ; il n'y a aucune paire de mêmes bornes entre deux S.

### 2.4 Ce que la cartographie impose au produit

- Un client qui construit un **arbre** ou un **index par offset** ne peut pas ignorer les 239 paires :
  elles ne sont pas des doublons exacts (sauf 6), ni des erreurs de span ; ce sont des **vues
  concurrentes** du même texte.
- Un filtre qui ne traite que le cas canonique laisse **91 paires** (B1), dont 80 inclusions
  inverses, 6 mêmes bornes et 5 croisements. Ce n'est pas une partition.
- Une **partition stricte** doit trancher les 4 classes ; elle coûte des attachements (voir § 3.3),
  et ce coût est concentré dans les cas où le chunker est **plus large** que le S.
- Le rang de préférence ne peut pas être un simple « plus court » : le chunker est le span du gold
  dans **179/207** groupes ambigus qui en portent un (86,5 %), le S le plus large dans **25/244**
  (10,2 %). La préférence naturelle est donc **le chunker le plus large**, pas le S.

## 3. Deux options mesurées

### 3.1 Définitions

- **A — alternative explicite.** Les deux segments restent dans `etiquettes` ; chaque segment du
  groupe reçoit `meta.partition` et `meta.alternative` (les autres segments, leur relation vue du
  porteur, leur rang, leur attachement et leur rôle). **Aucune suppression.** Rang 1 = chunker le
  plus large (à défaut, le plus court).
- **B1 — filtre union partiel.** Quand un segment **S contient un segment union**, le S est retiré
  et conservé dans `meta.alternative` du segment gardé, avec `retire: true`. Les autres classes
  (union plus large, mêmes bornes, croisement) restent documentées. C'est le « filtre union » du
  P0-3 ; **ce n'est pas une partition stricte**.
- **B2 — partition stricte.** **Tous** les segments union sont conservés ; tous les S qui les
  chevauchent sont retirés et conservés dans `meta.alternative` avec `retire: true`. La vue de
  premier niveau ne contient plus aucune paire. Une passe de sécurité tranche les union-union
  résiduels par rang (aucun sur les 121 textes mesurés).
- **Référence — déduplication silencieuse.** `_supprimer_chevauchements` (politique actuelle de la
  fusion) : 0 paire, mais aucune trace des segments retirés.

Une variante de sensibilité est mesurée : **glouton attachement** (par groupe, garder le segment qui
porte un attachement, puis le chunker, puis le plus long) — partition stricte orientée attachement.

### 3.2 Qualité sur le gold (612 phrases, 239 cibles)

| variante | F1 | P | R | tête F1 | POS | fraction | exact / 239 | taux exact | top-k |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| base (S + union, brut) | 0,5849 | 0,6292 | 0,5464 | 0,7336 | 0,7581 | 0,5537 | **222** | **0,9289** | 221 |
| **A — alternative** | 0,5849 | 0,6292 | 0,5464 | 0,7336 | 0,7581 | 0,5537 | **222** | **0,9289** | 221 |
| **B1 — filtrer_union** | **0,6163** | 0,7122 | 0,5432 | 0,7545 | 0,7581 | 0,5537 | **217** | 0,9079 | 216 |
| **B2 — filtrer** | **0,6172** | **0,7445** | 0,5271 | **0,7605** | 0,7581 | 0,5537 | **205** | 0,8577 | 204 |
| déduplication | 0,6141 | 0,7283 | 0,5309 | 0,7432 | 0,7581 | 0,5537 | 208 | 0,8703 | 207 |
| glouton attachement | 0,5892 | 0,7048 | 0,5062 | 0,7260 | 0,7581 | 0,5537 | **213** | 0,8912 | 212 |
| partition mix_E (sensibilité) | 0,6179 | 0,7453 | 0,5276 | 0,7612 | 0,7581 | 0,5537 | 206 | 0,8619 | 205 |

`mix_E` est une variante de sensibilité par classe (mêmes bornes → garder le S) : elle
dépasse B2 de 0,0007 de F1 pour un attachement de plus, ce qui ne justifie pas un cas particulier
dans le patch. La POS et la fraction sont **identiques dans toutes les variantes** (0,7581 ; 0,5537) : les options
ne touchent que des étiquettes `syntagme`, jamais les POS, et les syntagmes ne sont pas dans
`unites_semantiques`. Le hash des POS est le même (`cb4757217465da39`) dans les quatre modes.

### 3.3 Le coût en attachement, et pourquoi il n'est pas là où on l'attend

| variante | exact | perte vs 222 | paires supprimées | perte par paire | gain F1 | gain F1 par attache perdu |
|---|---:|---:|---:|---:|---:|---:|
| base | 222 | — | — | — | — | — |
| A | 222 | **0** | 0 | 0 | 0 | — |
| B1 | 217 | **5** | 148 | **0,034** | +0,0314 | **0,0063** |
| B2 | 205 | **17** | 239 | 0,071 | +0,0323 | 0,0019 |
| déduplication | 208 | **14** | 239 | 0,059 | +0,0292 | 0,0021 |
| glouton attachement | 213 | **9** | 239 | 0,038 | +0,0043 | 0,0005 |

Le résultat central : **le filtre union partiel est bien moins cher que la déduplication**
(222→**217**, soit −5, contre 222→**208**, soit −14), et il gagne presque tout le F1 (+0,0314 sur
+0,0323). Mais il **laisse 91 paires** (33/96 textes) : il ne répond pas au client qui veut un
arbre/index strict. La partition stricte coûte **17** attachements, soit 3 de plus que la
déduplication, parce qu'elle retire aussi les S dans les cas où le chunker est **plus large** —
précisément les cas où le S porte souvent l'attachement (B2 ne garde que 397 attachements de
premier niveau, contre 444 pour la déduplication).

Si le client a besoin d'une partition **et** tient à l'attachement, le glouton attachement est le
meilleur compromis strict mesuré : **213** exacts (seulement 9 perdus), 0 paire, F1 0,5892. Il perd
du F1 (0,5892 contre 0,6172), mais il préserve 8 attachements de plus que B2.

### 3.4 Sortie : paires, textes, segments, JSON

| variante | paires | textes avec chevauchement | segments | attachements de premier niveau | JSON 96 textes | Δ JSON | vues `alternative` |
|---|---:|---:|---:|---:|---:|---:|---:|
| base | 239 | 54 | 722 | 549 | 1 928 458 | — | 0 |
| A | 239 | 54 | 722 | 549 | 2 129 150 | **+10,4 %** | 894 |
| B1 | 91 | 33 | 636 | 481 | 2 066 365 | **+7,2 %** | 714 |
| B2 | 0 | 0 | 545 | 397 | 1 967 190 | **+2,0 %** | 466 |
| déduplication | 0 | 0 | 584 | 444 | n. m. | — | 0 |

Sur les 25 paragraphes libres : 59 paires / 10 textes en base, 29 / 7 en B1, 0 / 0 en B2. Le JSON
libre passe de 928 683 à 974 128 (+4,9 %) en A, 959 786 (+3,3 %) en B1, 929 427 (+0,1 %) en B2.
Le **pire cas** est `f50` : 152 vues en A, 77 en B2, 171 segments ; le coût est réel mais borné.

Aucun mode ne crée de texte sans syntagme : les **6** textes sans syntagme le restent —
`fiabilite/f13`, `f18`, `f27`, `f37` et `bloc_l/x47`, `x48`. Les 4 refus de l'audit 1 (entrées
vides ou non textuelles) ne sont pas dans le banc des 96 et ne sont pas affectés : la sortie a
lieu avant le niveau syntagme.

### 3.5 Lisibilité

Le formateur `drave.py` actuel **ignore** `meta.alternative` : la sortie humaine reste donc de la
longueur de la base (max 132 caractères, médiane 38), mais elle **cache** les alternatives. Si on
voulait les afficher en ligne, la sortie deviendrait illisible :

| rendu | max | médiane | p95 | lignes > 100 |
|---|---:|---:|---:|---:|
| base, inline | 132 | 38 | 67 | 7 |
| A, inline | **251** | 60 | 171 | **288** |
| B1, inline | 237 | 47 | 173 | 245 |
| B2, inline | 237 | 42 | 178 | 152 |
| base, compact | 138 | 44 | 74 | 9 |
| A, compact | 157 | 55 | 88 | 19 |
| B2, compact | 143 | 48 | 96 | 28 |

La bonne forme est donc un **suffixe compact** `[g0 r1/4 · alt=3 · 2 retiré(s)]` (voir le patch
`drave.py` § 4.4), pas l'inline des vues. Le détail complet reste dans `--json`.

### 3.6 La préférence : le chunker le plus large

| règle de rang 1 | rang 1 = span du gold | /207 groupes avec gold | /244 groupes |
|---|---:|---:|---:|
| **chunker le plus large** (retenu) | **179** | **86,5 %** | 73,4 % |
| chunker le plus court | 177 | 85,5 % | 72,5 % |
| chunker avec attachement | 178 | 86,0 % | 73,0 % |
| plus court, toutes sources | 169 | 81,6 % | 69,3 % |
| S le plus large | 25 | 12,1 % | 10,2 % |
| plus large, toutes sources | 19 | 9,2 % | 7,8 % |

Le filtre strict garde **au moins un span du gold dans 181/207 groupes** (87,4 %) ; il en perd
**26**, ce qui explique l'essentiel de la perte 222→205. Le rang 1 est une **préférence**, pas une
partition : en B2, plusieurs segments union peuvent être conservés dans un même groupe (le chunker
n'est pas un segment par groupe) ; c'est **`retire`** qui fait foi.

### 3.7 Contrôles négatifs

| contrôle | paires | F1 | exact | lecture |
|---|---:|---:|---:|---|
| chunker seul (`segmenter_s=False, union=False`) | **0** | — | — | le chunker ne chevauche jamais |
| S sans union (`union=False`) | **0** | — | — | le S seul ne chevauche jamais |
| supprimer **tous** les union | **0** | 0,4957 | 199 | 0 conflit, mais −23 attachements et −0,0892 de F1 : le filtre évident est le pire |
| filtre inverse (retirer le chunker contenu) | 112 | 0,5006 | 208 | la **direction** du filtre est décisive |
| `union_any` (retirer l'union de toute inclusion) | 3 | 0,4959 | 199 | trop agressif |
| `widest` (retirer le plus étroit de toute inclusion) | 32 | 0,4967 | 200 | trop agressif |
| 299 suppressions **au hasard** (20 graines) | — | **0,5519** (0,5431–0,5638) | **193,15** (184–198) | le gain du filtre n'est pas un effet « moins de segments » |
| **B1** | 91 | 0,6163 | 217 | meilleur coût d'attachement, mais partiel |
| **B2** | **0** | 0,6172 | 205 | partition stricte, coût 17 |

Le contrôle au hasard retire **le même nombre** de syntagmes que B2 (299 sur le gold) : même à sa
meilleure graine, il ne dépasse pas F1 0,5638 et 198 exacts, très en dessous de B2 (0,6172 / 205).
Le gain vient donc du **choix des segments**, pas de la diminution du nombre. Le filtre inverse et la
suppression de tous les union montrent que le sens et la cible du filtre comptent.

## 4. Recommandation

### 4.1 Choix

1. **Défaut : A — `partition="alternative"`.** Les deux segments restent ; `meta.partition` et
   `meta.alternative` documentent le groupe, la relation et la vue préférée (chunker le plus large).
   F1 0,5849 et exact 222/239 sont **inchangés** ; le client choisit. Coût : **+10,4 %** de JSON.
2. **Option « vue partition » : B2 — `partition="filtrer"`.** 0 paire, F1 0,6172, exact 205/239,
   **+2,0 %** de JSON. Les S retirés restent dans `meta.alternative` (`retire: true`) : la vue est
   linéaire, la donnée n'est **pas** perdue. C'est la vue à servir aux clients arbre/index.
3. **Option économique : B1 — `partition="filtrer_union"`.** Le filtre union du P0-3 : F1 0,6163,
   exact **217/239**, **+7,2 %** de JSON, mais **91 paires** restantes (33/96 textes). À ne vendre
   que comme « moins de chevauchements », **jamais** comme « partition ».
4. **Ne pas retenir** : la suppression de tous les union (F1 0,4957, exact 199), les filtres
   agressifs (`union_any`, `widest` : ~0,496 / 199–200), et la déduplication silencieuse
   (0,6141 / 208) qui perd 14 attachements sans trace.
5. **Compositions** : `Parallele` et `Cascade` avec `priorite_par_niveau=None` appellent encore
   `_supprimer_chevauchements` en silence. Le patch couvre `Heuristique.analyser` (le défaut de la
   CLI) ; propager la politique dans `_fusion` est le suivi **P0-3b**.

### 4.2 Selon le besoin du client

| besoin | mode | F1 | exact | paires | Δ JSON |
|---|---|---:|---:|---:|---:|
| je veux tout, je choisis | `alternative` (défaut) | 0,5849 | 222/239 | 239 | +10,4 % |
| moins de chevauchements, coût minimal | `filtrer_union` | 0,6163 | 217/239 | 91 | +7,2 % |
| partition stricte, F1 d'abord | `filtrer` | 0,6172 | 205/239 | 0 | +2,0 % |
| partition stricte, attachement d'abord | `glouton_att_union` (sensibilité) | 0,5892 | 213/239 | 0 | n. m. |
| compatibilité / mesure d'avant | `brut` | 0,5849 | 222/239 | 239 | 0 |

### 4.3 Patch exact — `tools/bloc_linguistique.py`

Le patch ajoute un paramètre `partition` (`brut`, `alternative` par défaut, `filtrer_union`,
`filtrer`), quatre fonctions (`_relation_partition`, `_cle_preferee`, `_groupes_partition`,
`_expliciter_partition`), l'appel en fin de `Heuristique.analyser` (après le tri, avant le
`trace`) et un **strip** dans `_fusion` (voir § 4.6). Il s'applique à `fa1b0c6e` et, avec offsets (+262/+312/+314/+321), au HEAD `ba39a7b1`. La copie
patchée est `/tmp/pin_audit/tools/bloc_partition.py` (sha256 `e9444daf…2e0e39d`).

```diff
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -529,12 +529,20 @@
 
     def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
                  seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
-                 union: bool = True):
+                 union: bool = True, partition: str = "alternative"):
         self.profils = profils
         self.segmenter_s = segmenter_s
         self.seuil_ouvert = seuil_ouvert
         self.seuil_langue = seuil_langue
         self.union = union
+        # "brut" : la sortie d'avant (chevauchements non documentés) ; "alternative" :
+        # les deux segments restent, `meta.alternative` dit lequel est préféré ;
+        # "filtrer_union" : on retire le S qui **contient** un segment chunker (le filtre
+        # union du P0-3) ; "filtrer" : partition stricte, le chunker est la partition.
+        # Dans les deux filtres, le segment retiré reste dans `meta.alternative` (`retire`).
+        if partition not in ("brut", "alternative", "filtrer_union", "filtrer"):
+            raise ValueError("partition attend 'brut', 'alternative', 'filtrer_union' ou 'filtrer'")
+        self.partition = partition
 
     # -- langues / script ---------------------------------------------------
     def _langue(self, texte: str, indice: str | None) -> tuple[str, float, str]:
@@ -1237,6 +1245,10 @@
         longueur = sum(u.fin - u.debut for u in unites)
         fraction = longueur / max(1, len(texte))
         etiquettes.sort(key=lambda e: (e.debut, e.fin, e.niveau))
+        if self.partition != "brut":
+            _expliciter_partition(etiquettes, filtrer=(
+                "" if self.partition == "alternative"
+                else "union" if self.partition == "filtrer_union" else "strict"))
         trace.append({"etape": "niveaux", "etiquettes": len(etiquettes),
                       "niveaux": sorted({e.niveau for e in etiquettes}),
                       "unites_semantiques": len(unites), "fraction": round(fraction, 4)})
@@ -1811,6 +1823,135 @@
 # --------------------------------------------------------------------------- compositions
 
 
+def _relation_partition(x: Etiquette, y: Etiquette) -> str:
+    """La relation de `y` vue **depuis** `x` : `inclut` = x contient y."""
+    if x.debut == y.debut and x.fin == y.fin:
+        return "meme_span"
+    if x.debut <= y.debut and x.fin >= y.fin:
+        return "inclut"
+    if y.debut <= x.debut and y.fin >= x.fin:
+        return "inclus"
+    return "croise"
+
+
+def _cle_preferee(e: Etiquette) -> tuple:
+    """La vue préférée : le segment du chunker (union), le plus large, puis le plus sûr.
+
+    Mesuré sur le gold 612 : dans 179/207 groupes ambigus qui portent un span du gold, le
+    chunker le plus large **est** ce span (86,5 %) ; le S le plus large ne l'est que 25 fois sur 244.
+    La préférence ne supprime rien par défaut : elle **classe**.
+    """
+    return (0 if (e.meta or {}).get("union") else 1, -(e.fin - e.debut), -e.confiance,
+            e.debut, e.fin, e.type)
+
+
+def _groupes_partition(segs: list[Etiquette]) -> list[list[Etiquette]]:
+    """Les composantes connexes du graphe de chevauchement, ordonnées par position."""
+    parent = list(range(len(segs)))
+
+    def trouver(i: int) -> int:
+        while parent[i] != i:
+            parent[i] = parent[parent[i]]
+            i = parent[i]
+        return i
+
+    for i in range(len(segs)):
+        for j in range(i + 1, len(segs)):
+            if max(segs[i].debut, segs[j].debut) < min(segs[i].fin, segs[j].fin):
+                ri, rj = trouver(i), trouver(j)
+                if ri != rj:
+                    parent[rj] = ri
+    groupes: dict[int, list[Etiquette]] = {}
+    for i, e in enumerate(segs):
+        groupes.setdefault(trouver(i), []).append(e)
+    return sorted((g for g in groupes.values() if len(g) > 1),
+                  key=lambda g: (min(e.debut for e in g), min(e.fin for e in g),
+                                 min(e.type for e in g)))
+
+
+def _expliciter_partition(etiquettes: list[Etiquette], filtrer: str = "") -> None:
+    """Documente (et, si `filtrer`, linéarise) les chevauchements de syntagmes.
+
+    `meta.partition` porte le groupe, le rang et la vue ; `meta.alternative` porte les
+    autres segments du groupe, leur relation vue du porteur et, en mode `filtrer`, le
+    drapeau `retire`. Aucun segment n'est supprimé en mode `alternative`.
+
+    `filtrer="union"` : on retire le S qui **contient** un segment chunker (le filtre
+    union du P0-3) ; les autres chevauchements restent documentés. `filtrer="strict"` :
+    le chunker est la partition — **tous** les segments `union` sont conservés, et tous
+    les S qui les chevauchent sont retirés. Dans les deux cas, le retiré reste lisible
+    dans `meta.alternative` du segment conservé, avec `retire: true`.
+    """
+    segs = [e for e in etiquettes if e.niveau == "syntagme"]
+    groupes = _groupes_partition(segs)
+    rangs: dict[int, tuple[int, int]] = {}
+    for gid, groupe in enumerate(groupes):
+        for i, e in enumerate(sorted(groupe, key=_cle_preferee)):
+            rangs[id(e)] = (gid, i + 1)
+    retirees: set[int] = set()
+    if filtrer == "union":
+        for groupe in groupes:
+            unions = [e for e in groupe if (e.meta or {}).get("union")]
+            for e in groupe:
+                if not (e.meta or {}).get("union") and any(
+                        u.debut >= e.debut and u.fin <= e.fin
+                        and (u.fin - u.debut) < (e.fin - e.debut) for u in unions):
+                    retirees.add(id(e))
+    elif filtrer == "strict":
+        for groupe in groupes:
+            unions = [e for e in groupe if (e.meta or {}).get("union")]
+            for e in groupe:
+                if not (e.meta or {}).get("union") and any(
+                        max(e.debut, u.debut) < min(e.fin, u.fin) for u in unions):
+                    retirees.add(id(e))
+        while True:  # sécurité : union-union, ou tout chevauchement résiduel
+            gardes = [e for e in etiquettes
+                      if e.niveau == "syntagme" and id(e) not in retirees]
+            paires = [(x, y) for i, x in enumerate(gardes) for y in gardes[i + 1:]
+                      if max(x.debut, y.debut) < min(x.fin, y.fin)]
+            if not paires:
+                break
+            for x, y in paires:
+                rx = rangs.get(id(x), (0, 99))[1]
+                ry = rangs.get(id(y), (0, 99))[1]
+                retirees.add(id(x if rx >= ry else y))
+    for gid, groupe in enumerate(groupes):
+        for e in groupe:
+            if filtrer and id(e) in retirees:
+                continue
+            meta = dict(e.meta or {})
+            meta["partition"] = {"groupe": gid, "rang": rangs[id(e)][1],
+                                 "membres": len(groupe),
+                                 "vue": ("alternative" if not filtrer
+                                         else "filtrer_union" if filtrer == "union"
+                                         else "filtrer")}
+            vues = []
+            for autre in groupe:
+                if autre is e:
+                    continue
+                vue = {"type": autre.type, "debut": autre.debut, "fin": autre.fin,
+                       "source": autre.source,
+                       "union": bool((autre.meta or {}).get("union")),
+                       "relation": _relation_partition(e, autre),
+                       "rang": rangs[id(autre)][1]}
+                if filtrer:
+                    vue["retire"] = id(autre) in retirees
+                att = (autre.meta or {}).get("attachement")
+                if att:
+                    vue["attachement"] = {"segment": att.get("segment", ""),
+                                          "cible": att.get("cible", "")}
+                role = (autre.meta or {}).get("role")
+                if role:
+                    vue["role"] = role
+                vues.append(vue)
+            vues.sort(key=lambda v: (v["rang"], v["debut"], v["fin"], v["type"]))
+            meta["alternative"] = vues
+            e.meta = meta
+    if retirees:
+        etiquettes[:] = [e for e in etiquettes
+                         if not (e.niveau == "syntagme" and id(e) in retirees)]
+
+
 def _supprimer_chevauchements(etiquettes: list[Etiquette],
                               priorite_syntagme: str = "heuristique") -> list[Etiquette]:
     """Les alternatives se suppriment **par type** quand les types sont complémentaires.
@@ -1905,6 +2046,13 @@
                 etiquettes.append(e)
         # La source est choisie par niveau : plus d'arbitrage de chevauchement à faire.
     else:
+        # la déduplication de la fusion retire des segments : les `meta.alternative` de
+        # l'heuristique pointeraient vers des absents. On les retire de la copie fusionnée
+        # plutôt que de laisser des références mortes ; la vue explicite des compositions
+        # est le suivi P0-3b.
+        for e in meilleures.values():
+            e.meta = {k: v for k, v in e.meta.items()
+                      if k not in ("partition", "alternative")}
         etiquettes = _supprimer_chevauchements(list(meilleures.values()), priorite_syntagme)
     if a.langue != "und" and (b.langue == "und" or a.langue == b.langue):
         lg, script = a.langue, a.script
```

### 4.4 Patch exact — `tools/drave.py`

`drave.py` n'existe pas à `fa1b0c6e` ; ce diff s'applique au HEAD `ba39a7b1` (sha256 de la copie
patchée `8cf61772…18fe622`).

```diff
--- a/tools/drave.py
+++ b/tools/drave.py
@@ -114,9 +114,17 @@
         lr = max(len(r) for r in roles)
         lignes.append("SYNTAGMES")
         for e, valeur, role, cible, span in zip(syntagmes, valeurs, roles, cibles, spans):
+            part = (e.meta or {}).get("partition")
+            suffixe = ""
+            if part:
+                alts = (e.meta or {}).get("alternative") or []
+                retires = sum(1 for v in alts if v.get("retire"))
+                suffixe = (f"  [g{part['groupe']} r{part['rang']}/{part['membres']}"
+                           f" · alt={len(alts)}"
+                           + (f" · {retires} retiré(s)" if retires else "") + "]")
             lignes.append(
                 f"  {e.type:<{lt}}  {span:<{lsp}}  {valeur:<{lv}}  "
-                f"rôle={role:<{lr}}  → {cible}"
+                f"rôle={role:<{lr}}  → {cible}{suffixe}"
             )
     else:
         lignes.append("SYNTAGMES —")
@@ -157,7 +165,7 @@
 
 
 def cmd_analyser(args: argparse.Namespace) -> int:
-    annotation = bl.Heuristique().analyser(args.texte, args.langue)
+    annotation = bl.Heuristique(partition=args.partition).analyser(args.texte, args.langue)
     if annotation.refus:
         # un refus est une **réponse** : le JSON la porte, le code 3 la distingue d'une erreur
         if args.json:
@@ -345,6 +353,11 @@
     analyser.add_argument("texte", metavar="TEXTE", help="texte à analyser (entre guillemets)")
     analyser.add_argument("--langue", choices=("fr", "en"), default=None,
                           help="indice de langue (fr/en) ; sans lui, le bloc détecte")
+    analyser.add_argument("--partition",
+                          choices=("alternative", "filtrer_union", "filtrer", "brut"),
+                          default="alternative",
+                          help="vue des syntagmes : alternative (défaut), "
+                               "filtrer_union (filtre union), filtrer (partition stricte), brut")
     analyser.add_argument("--json", action="store_true",
                           help="sortie JSON complète (annotation, sans durée)")
     analyser.set_defaults(fonction=cmd_analyser)
```

Exemple de sortie compacte :

```text
SYNTAGMES
  GP   [29:60]  du jardin chaque matin avant de  rôle=theme     → fleurs   [g0 r1/4 · alt=3 · 2 retiré(s)]
  GV   [61:67]  partir                           rôle=prédicat  → —        [g0 r2/4 · alt=3 · 2 retiré(s)]
```

### 4.5 Schéma de `meta.alternative`

`meta.partition` et `meta.alternative` ne sont présents que sur un syntagme qui appartient à un
groupe de chevauchement (au moins deux segments). Le schéma est **additif** : les clients qui ne
lisent pas `meta` continuent de lire l'annotation comme avant.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "meta.partition et meta.alternative d'une étiquette syntagme",
  "type": "object",
  "properties": {
    "partition": {
      "type": "object",
      "required": ["groupe", "rang", "membres", "vue"],
      "properties": {
        "groupe": {"type": "integer", "minimum": 0},
        "rang": {"type": "integer", "minimum": 1},
        "membres": {"type": "integer", "minimum": 2},
        "vue": {"enum": ["alternative", "filtrer_union", "filtrer"]}
      },
      "additionalProperties": true
    },
    "alternative": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["type", "debut", "fin", "source", "union", "relation", "rang"],
        "properties": {
          "type": {"enum": ["GN", "GV", "GP", "REL", "SUB"]},
          "debut": {"type": "integer", "minimum": 0},
          "fin": {"type": "integer", "minimum": 1},
          "source": {"enum": ["heuristique", "neuronal", "humain"]},
          "union": {"type": "boolean"},
          "relation": {"enum": ["inclut", "inclus", "meme_span", "croise"]},
          "rang": {"type": "integer", "minimum": 1},
          "retire": {"type": "boolean"},
          "attachement": {
            "type": "object",
            "required": ["segment", "cible"],
            "properties": {"segment": {"type": "string"}, "cible": {"type": "string"}},
            "additionalProperties": false
          },
          "role": {"type": "string"}
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": true
}
```

**Invariants** (vérifiés sur 125 textes, 153 groupes, 1084 vues en A et 560 en B2, **0 violation**) :

- les spans sont valides (`0 ≤ debut < fin ≤ len(texte)`), `valeur = texte[debut:fin]` ;
- `groupe` est unique par annotation ; deux groupes ne partagent aucun segment ;
- `rang` est une permutation de `1..membres` dans le groupe ;
- `relation` est réciproque : `inclut` ↔ `inclus`, `meme_span` ↔ `meme_span`, `croise` ↔ `croise` ;
- `alternative` ne contient ni le porteur ni deux fois le même `(type, debut, fin)` ;
- `retire` n'est présent qu'en `filtrer_union` / `filtrer` ;
- en vue `filtrer`, `retire: true` ⇒ segment absent des étiquettes de premier niveau ; `retire: false`
  ⇒ présent ;
- `membres` = porteur + alternatives, sans doublon ;
- **le rang 1 est la vue préférée, pas la partition** : en B2, tous les union sont conservés et
  `retire` fait foi.

Exemple A (porteur `GP 29-60`, groupe de 4, rang 1, trois alternatives) :

```json
{
  "type": "GP", "debut": 29, "fin": 60, "valeur": "du jardin chaque matin avant de",
  "meta": {
    "partition": {"groupe": 0, "rang": 1, "membres": 4, "vue": "alternative"},
    "alternative": [
      {"type": "GV", "debut": 61, "fin": 67, "source": "heuristique", "union": true,
       "relation": "croise", "rang": 2, "role": "prédicat"},
      {"type": "GP", "debut": 29, "fin": 51, "source": "heuristique", "union": false,
       "relation": "inclut", "rang": 3,
       "attachement": {"segment": "du jardin chaque matin", "cible": "partir"},
       "role": "possession"},
      {"type": "GP", "debut": 58, "fin": 67, "source": "heuristique", "union": false,
       "relation": "croise", "rang": 4,
       "attachement": {"segment": "de partir", "cible": "au"},
       "role": "possession"}
    ]
  }
}
```

Même porteur en B2 (`vue: "filtrer"`) : le `GV 61-67` reste (`retire: false`), les deux autres `GP`
sont retirés (`retire: true`) mais restent lisibles avec leur attachement et leur rôle. **Aucune
information n'est perdue** : un client peut reconstruire la vue A depuis la vue B2.

### 4.6 CLI, compatibilité, tests

- `drave analyser "…"` : défaut `alternative`, la sortie humaine gagne un suffixe compact ; `--json`
  porte le détail complet.
- `--partition brut` : reproduit la sortie d'avant le patch (aucune méta), pour les clients qui
  comparent des octets.
- Pas de bump de `VERSION_ANNOTATION` : les champs sont **additifs** dans `meta` ; le schéma
  `docs/produit/schema-v1.json` doit les déclarer optionnels (suivi, non modifié ici).
- `Parallele`/`Cascade` : le patch ne couvre pas leur déduplication ; quand
  `priorite_par_niveau=None`, `_fusion` appelle toujours `_supprimer_chevauchements` en silence.
  Il **retire d'abord** `partition`/`alternative` des étiquettes fusionnées : sans ce strip, 280
  vues pointeraient vers des segments absents (220 étiquettes) ; avec, **0 référence morte**.
  Métriques de composition inchangées (cascade/parallèle : F1 0,6141, exact 208, POS 0,7465).
  Suivi **P0-3b** : appeler `_expliciter_partition` après la fusion, ou propager la politique.
- Tests à ajouter : 0 paire après `filtrer` sur 96 + 25 textes ; réciprocité des relations ;
  permutation des rangs ; `retire` cohérent ; F1/attachement inchangés en `alternative` ; mesurer
  les nouveaux chiffres en `filtrer`.

## 5. Limites — ce qui pourrait rendre ce rapport faux

- **Commit épinglé** : les chiffres sont ceux de `fa1b0c6e` ; le HEAD a bougé (gold corrigé après l'audit,
  le commit `c5b80dd8` annonce 226/226 attachements exacts). Les chiffres du HEAD seront différents.
- **Gold in-sample** : 612 phrases, 239 cibles ; le F1 et l'attachement sont des mesures de gold, pas
  une exactitude sur texte libre. Les 25 paragraphes libres n'ont pas de gold : ils servent à la
  cartographie et à la lisibilité, pas à l'exactitude.
- **L'attachement exact** ne compte que les spans du gold ; un segment alternatif peut porter la
  bonne cible sans être compté, et un S retiré peut porter un attachement correct.
- **Le client arbre/index n'est pas testé** : « 0 paire » est une propriété structurelle, pas une
  preuve d'usage ; il reste à valider un consommateur réel.
- **Le rang 1** est une préférence de groupe (179/207 avec gold), pas une vérité sémantique ; le
  filtre strict garde **tous** les union, pas un par groupe.
- **Le payload** est mesuré sur 96 + 25 textes ; `f50` (152 vues) est le pire cas observé, pas une
  borne.
- **Les compositions** restent silencieuses quand `priorite_par_niveau=None` ; le patch est
  volontairement limité à `Heuristique.analyser`.
- **Pas de GPU / neuronal réel** : ce banc est CPU, heuristique, déterministe ; le vrai tagger et
  ses erreurs ne sont pas mesurés ici.
- Le filtre B2 retire des S qui peuvent être **sémantiquement** la bonne coupe (le chunker est plus
  large) ; le gold le dit minoritaire (12,1 % des groupes), pas impossible.

## 6. Reproductibilité

```bash
# copie épinglée (non committée)
#   /tmp/pin_audit/tools/bloc_linguistique.py  sha256 5954d087…37b08f
#   /tmp/pin_audit/tools/structures/generateur.py
#   /tmp/pin_audit/tools/tests/linguistique/gold*.json

PIN=/tmp/pin_audit python3 /tmp/partition_syntagmes/inventaire.py
PIN=/tmp/pin_audit python3 /tmp/partition_syntagmes/options.py
python3 /tmp/partition_syntagmes/patch_eval.py
python3 /tmp/partition_syntagmes/stats_finales.py
patch -p1 --dry-run < /tmp/partition_syntagmes/patch_final.diff   # depuis une copie du dépôt
patch -p1 --dry-run < /tmp/partition_syntagmes/drave.diff
```

Fichiers produits par cette étude : **ce rapport** et
[`pensee-partition-syntagmes.json`](pensee-partition-syntagmes.json). **Aucun fichier existant
n'a été modifié par cette étude, aucun commit n'a été fait.** Les scripts et la copie épinglée vivent dans `/tmp`.

## 7. Ligne de roadmap et suite

- **P0-3** : ce rapport + le patch `alternative` / `filtrer_union` / `filtrer` ; la décision
  produit est **A par défaut, B2 en option**.
- **P0-3b** (suite immédiate, 1 h) : propager `_expliciter_partition` dans `_fusion` quand
  `priorite_par_niveau=None`, et remplacer la déduplication silencieuse de `Parallele`/`Cascade`.
- **P0-3c** (2 h) : test de non-régression « 0 paire après `filtrer` » + validation d'un client
  arbre/index sur les 96 textes ; mesurer le coût de `f50` sur un vrai parseur.
- **P0-1** (frontières de phrase) et **P0-2** (types `url`/`emoji` morts) restent indépendants ;
  ils ne changent pas la partition des syntagmes.
