# Audit produit du bloc linguistique — 0 plantage sur 50 phrases, 34/50 avec une anomalie de contrat

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **HEAD vérifié en fin d'audit** : `c6904284`
> (le HEAD a bougé pendant l'audit ; module `bloc_linguistique.py` inchangé ; `evaluer_gold.py`
> modifié en `7f73c17f`) ·
> **Date** : 2026-11-06 ·
> **Verdict** : ⚠️ **la surface est utilisable en autonomie ; la structure ne l'est pas encore.**
> **Aucun fichier existant modifié par cet audit ; aucun commit.** Sorties : ce rapport et
> [`pensee-produit-bloc-l.json`](pensee-produit-bloc-l.json).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ; **50 phrases libres** écrites pour
> l'audit (textes dans le JSON) ; harnais local non committé dans `/tmp/audit_produit_bl`.
> **Porte** : `bash tools/porte-bloc-linguistique.sh` → **verte** (16 tests, autotest UDHR
> **0,9687**, profils permutés **0,0022**).

**En une phrase.** Sur 50 phrases libres, le bloc **ne plante pas**, **ne refuse pas**, **ne rend
jamais une sortie vide** et garde **tous les offsets** ; mais **34/50 textes** portent au moins une
anomalie, dont **31/50** avec des **syntagmes qui se chevauchent** (188/362 étiquettes), les
**frontières de phrase** cassent sur les décimaux, dates, URL et abréviations, et les
**compositions** perdent le refus et le contexte. La surface (graphème, mot, POS fermées, phrase,
document) est utilisable seule ; la structure (syntagmes, attachement, cascade) ne l'est pas encore.

| brique | état pour un utilisateur autonome | preuve |
|---|---|---|
| graphème, mot | ✅ | 0 crash, 0 span hors texte, `valeur = texte[debut:fin]` à **100 %**, couverture **49/50 à 100 %** (x46 : 95,14 %, newlines) |
| POS fermées | ✅ | gold **0,9004** ; 50/50 textes ont des POS |
| POS ouvertes | ⚠️ | gold **0,6234** ; sur 50 : **365 NOUN pour 32 VERB**, « arrose », « rentre », « prépare », « warm » → NOUN |
| phrase (type, négation, modalité) | ⚠️ | gold **0,9967 / 0,9771 / 0,9886**, mais frontières cassées (décimaux, URL, abréviations) |
| syntagme | ❌ | **132 paires** de chevauchement dans **31/50** textes, **188/362** étiquettes ; F1 gold **0,5849** |
| attachement | ⚠️ | **222/222** exact quand le span est bon, mais **17 spans** inatteignables, **16/265** cibles sont des mots fermés, pas d'offset de cible |
| document | ⚠️ | toujours présent, mais **42/53** valeurs tronquées à 60 caractères, **1/50** faux titre (x48) + 4 en cas limites |
| langue fr/en | ✅ | **50/50** sur ce banc (34 fr, 14 en, 2 `und`) ; **39/50** seulement avec les profils UDHR, et le format change `fr`/`fra` |
| compositions | ❌ | refus et contexte perdus, cascade **50/50** appels ; POS **0,7465 < 0,7581** (verdict `cascade_pos` vert par plancher 0,70 depuis `7f73c17f`, pas par correctif) |
| scripts non latins | ⚠️ | russe et chinois : graphème/mot/phrase/document, **0 syntagme**, **0 morphème** |

## 1. Dispositif

- **Banc libre** : 50 phrases écrites à la main pour cet audit — 29 françaises, 14 anglaises,
  7 de bruit ou de script (URL/email, SMS, markdown, sans ponctuation finale, cyrillique,
  sinogrammes, emoji). **819 mots**, **4 320 étiquettes**, **265 attachements**. Aucune phrase ne
  vient du gold. Les textes sont dans le JSON, section `banc_50.detail`.
- **Analyses** : `Heuristique().analyser(texte)` (défaut : générateur S + union + chunker), plus
  `MockNeuronal`, `Parallele`, `Cascade` pour les compositions. Les 50 phrases passent par
  plusieurs lectures (métriques, contrat, mode dégradé) ; le déterminisme est vérifié à part.
- **Vérifications** : spans dans le texte, `debut <= fin`, spans vides, `valeur` vs tranche,
  cible d'attachement présente et token, segment d'attachement, chevauchements `pos`/`syntagme`/
  `phrase`, doublons, unités sémantiques, fraction recalculée, confiance, source, niveau, type,
  clés JSON. **25 cas limites** textuels + 4 entrées non-str.
- **Performance** : 10/50/200 mots, 31/21/11 répétitions, machine Xeon E5-2687W v3, Python 3.13.16 ;
  mémoire par `tracemalloc` et `ru_maxrss` ; déterminisme sur 3 graines de hash.
- **Ce que ce banc ne mesure pas** : la justesse sémantique sur texte libre (pas de gold), la
  qualité du vrai modèle neuronal (pas de réseau/GPU ici), ni la robustesse à un corpus aléatoire.

## 2. État gold rejoué

Le rejeu du 2026-11-06 redonne l'**état fourni** (vivant 612 ; module inchangé de `fa1b0c6e` à `c6904284`, dernier contrôle) ; la fiche
v12 publie, elle, les valeurs du **gelé 602** pour le F1 et la tête :

| mesure | valeur |
|---|---:|
| phrases / cibles / tokens | **612 / 239 / 3 179** |
| exact / labels | **222 / 222 = 1,0000** |
| couverture | **0,9289** |
| spans perdus | **17** (décomposition v12 : 8 REL, 5 SUB, 4 GP) |
| F1 syntagmes (vivant 612) | **0,5849** (P 0,6292 ; R 0,5464) |
| tête (vivant 612) | **0,7336** |
| F1 / tête gelé 602 | **0,5893** (P 0,6319 ; R 0,5522) / **0,7392** ; POS 0,7603 |
| POS | **0,7581** (fermé 0,9004 ; ouvert 0,6234) |
| pragmatique | acte 0,9967 ; négation 0,9771 ; modalité 0,9886 ; double sens 0,9444 |
| fraction sémantique | 0,5537 |

**Vivant 612 vs gelé 602.** L'exact (222/222) et la couverture (0,9289) sont **identiques** sur
les deux bases — les 10 phrases ajoutées après le gel n'ont aucune cible. Le F1 et la tête
diffèrent : **0,5849 / 0,7336** sur le vivant, **0,5893 / 0,7392** sur le gelé. La fiche v12
publie les valeurs **gelées** (le POS 0,7603 est notre mesure du gelé, pas une valeur de la
fiche) ; comme le note l'[audit v10](rapport-audit-v10.md), ne pas comparer un F1 vivant à un F1
gelé.

**dev/test** (`gold_split` : `crc32(id) % 3 == 0` → test) :

| split | phrases | cibles | exact | couverture | spans | POS | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| dev | 422 | 163 | **153/153** | 0,9387 | 10 | 0,7547 | 0,5820 |
| test | 190 | 76 | **69/69** | 0,9079 | 7 | 0,7656 | 0,5914 |
| total | **612** | **239** | **222/222** | **0,9289** | **17** | **0,7581** | **0,5849** |

**Les quatre modes** (vivant 612 ; valeurs identiques à `c6904284`). Le mock est le double de contrat,
pas un modèle :

| mode | POS | F1 | couverture | exact |
|---|---:|---:|---:|---:|
| heuristique | **0,7581** | 0,5849 | **0,9289** | **222/222** |
| mock neuronal | 0,3454 | 0,5763 | 0,8326 | 0/239 |
| parallèle | 0,7465 | **0,6141** | 0,8703 | 208/208 |
| cascade | 0,7465 | **0,6141** | 0,8703 | 208/208 |

- **`cascade_pos` : rouge à `fa1b0c6e`, vert au dernier contrôle (`c6904284`) par plancher.** À `fa1b0c6e`, le verdict
  comparait la cascade à l'heuristique : 0,7465 < 0,7581 → `ok=false`. Depuis `7f73c17f`,
  `evaluer_gold.py` remplace la comparaison par un **plancher 0,70** : 0,7465 ≥ 0,70 → `ok=true`.
  Les valeurs mesurées sont **identiques** ; le module n'a pas changé. La fusion par confiance
  mélange le POS du mock (0,3454) à celui de l'heuristique : elle gagne 0,0292 de F1 mais perd
  0,0116 de POS et 14 spans d'attachement (222 → 208). Le vert est une **décision de seuil**, pas
  un correctif.
- **`cascade` = `parallèle` au chiffre près** : le mock est déterministe et la cascade appelle le
  neuronal **1 676 fois pour 1 676 évaluations** (612 `all` + 452 `reel` + 20 `hand` + 432
  `reel_new` + 160 `synthétique`), soit **100 %**. Sur `all` : **612/612**.
- **`ok`** : **faux à `fa1b0c6e`** (à cause de `cascade_pos`) ; **vrai au dernier contrôle `c6904284`** (plancher 0,70),
  toutes les autres valeurs étant inchangées.

## 3. Robustesse hors gold : les 50 phrases libres

### 3.1 Aucun plantage, aucun refus, aucune sortie vide

| indicateur | valeur |
|---|---:|
| phrases | **50** (819 mots) |
| plantages | **0** |
| refus (`refus` non vide) | **0** |
| sorties vides (`etiquettes == 0`) | **0** |
| textes sans aucune anomalie | **16/50** |
| textes avec au moins une anomalie | **34/50** |
| anomalies détectées | **149** |
| étiquettes / attachements | **4 320 / 265** |

- **Niveaux** : graphème, mot, pos, phrase, pragmatique, discours et document sont présents dans
  **50/50** textes ; **morphème manque 9 fois** (mots sans affixe productif) ; **syntagme manque
  2 fois** (russe x47, chinois x48). Un client ne peut donc pas exiger les neuf niveaux.
- **Langue** : 34 fr (29 phrases fr + 5 bruit francophone), 14 en, 2 `und` ; scripts :
  48 `Latn`, 1 `Cyrl`, 1 `Hani`.
- **Fraction sémantique** : **0,3529 – 0,5493 – 0,8750** (min/médiane/max). La plage documentée
  **0,51–0,76** ne tient pas sur ce banc : un SMS descend à 0,35, le chinois monte à 0,875.
- **Taille** : 14 à 417 étiquettes par texte (médiane 78).

### 3.2 Les incohérences mesurées

| anomalie | n | textes | exemple |
|---|---:|---:|---|
| **chevauchement de syntagmes** | **132 paires** | **31/50** | f02 : `GP 29-51` et `GP 29-60` ; `GV 80-96` et `GV 90-96` |
| **chevauchement de phrases** | 1 | f10 | `(0,104)` et `(2,104)` : l'extension d'abréviation (`M.`) ne fait pas avancer l'itérateur |
| **valeur hors span** | 8 | f11, f14, f16, x46 | morphème normalisé : `tion` vs `TION`, `pro` vs `PRO` |
| **acte hors candidats** | 4 | f07, f26, x44, x49 | `acte = exclamation`, candidats `["assertion","question","ordre"]` |
| **candidat dupliqué** | 4 | f09, f23, e35 | `["SUB","savent","savent","sonner"]` |
| **zéro** | 0 | — | span hors texte, span vide, cible absente, cible non-token, segment d'attachement, unité hors texte, unité qui se chevauche, fraction incohérente, confiance hors [0,1], source/niveau/type invalides, doublon |

**Le chevauchement de syntagmes est le problème n° 1.** 132 paires, **188 des 362 étiquettes
syntagme (51,9 %)** sont impliquées, dans **31/50 textes** ; 113 sont des **inclusions**, 19 des
chevauchements partiels ; 61 paires sont de même type, 71 de types différents. Ce n'est pas un
détail de bord : un client qui construit un arbre, un index par offset ou une partition de la
phrase casse sur près d'un texte sur deux. Et le chunker simple, seul, ne produit **aucun**
chevauchement (`Heuristique(segmenter_s=False, union=False)` : 0) : le problème vient du
générateur S et de l'union, pas de la tokénisation.

**Autres écarts de forme** : **60 étiquettes phrase** pour 50 textes (6 textes multi-phrases),
dont **6 spans commencent par un espace** ; **53 étiquettes document**, dont **42 valeurs
tronquées à 60 caractères** et **2 titres** (x46, vrai titre markdown ; x48, faux titre chinois) ;
**graphème** : 49/50 textes à 100 %, x46 à **95,14 %** (7 newlines, catégorie `Cc`, non couvertes).

### 3.3 Qualité observable (sans gold libre)

- **POS ouvertes** : 365 `NOUN` pour 32 `VERB` sur les 50 textes. f02 : « arrose », « rentre »,
  « prépare » → `NOUN` ; e29 : « warm » → `NOUN`. Le gold mesure 0,6234 sur l'ouvert ; les
  exemples libres sont cohérents avec cette faiblesse.
- **Nombres, dates, URL** : « 12.5 » coupe la phrase en **deux fragments** ; « 12.03.2024 » en
  **trois** ; « 12,5 » (virgule) ne coupe pas la phrase mais découpe le nombre en `12`, `,`, `5`.
  Une URL peut créer **3 à 4 phrases** (x43 : 4, avec URL + email) et les tokens `https`,
  `example`, `com` sont des mots ordinaires. **Les types `url` et `emoji` ne sortent jamais** (0/963) : l'alternative URL est
  après `\w+`, et `[^\w\s]` capture l'emoji avant l'alternative emoji. L'emoji est étiqueté
  `ponctuation`.
- **Abréviations** : « Le Dr. Martin est arrivé hier. Il repart demain. » rend **deux** étiquettes
  phrase qui se chevauchent (`0-30` et `6-30`) ; « M. Dupont » et « etc. Puis… » aussi.
- **Attachements** : **16/265** cibles sont des mots fermés — `au` 3, `was` 3, `lui` 2, `pas` 2,
  `have` 2, `entre` 2, `ne` 1, `Tu` 1 ; **3/265** cibles sont ambiguës (mot répété, `example` dans
  x43) ; **0 cible absente** du texte et **0 segment d'attachement** incohérent. Le champ
  `meta.attachement` ne porte **pas l'offset de la cible**, seulement sa chaîne.
- **Double sens** : **9/50** phrases déclenchent `double_sens` (candidat à 0,25) : `livre` 2,
  `temps` 2, `point` 2, `note` 1, ` ou ` 1, guillemets 1. C'est du rappel, pas de la précision.
- **Langue** : défaut **50/50** (34 fr, 14 en, 2 `und`). Avec les **profils UDHR** : **39/50**
  après conversion ISO3→ISO2 (30/34 fr, 7/14 en, 2/2 `und` ; `oci` compté comme fr,
  `hns`/`sco`/`pcm` non), et **2/50** en égalité stricte de chaîne (les deux `und`). Exemples : f01 fr→`hns`, e29/e35/e42 en→`sco`, e37 en→`pcm`, f03/f23/
  x44 fr→`und`, e32/e36/e40 en→`und`. L'indice de langue `"fr"` est **ignoré** quand les profils
  sont chargés (les clés sont en ISO3).
- **Scripts non latins** : russe et chinois rendent graphème/mot/phrase/document, **0 syntagme**,
  **0 morphème** ; le chinois est même classé **`document.titre`** parce que `upper() == lower()`
  sur les scripts sans casse.

### 3.4 Cas limites (25 textuels + 4 entrées non-str)

| cas | résultat |
|---|---|
| vide, espaces, ponctuation seule, emoji seul, espace invisible | `refus = "vide"`, **0 étiquette** (5 cas) |
| chiffres seuls (`1234567890`) | 6 étiquettes, pas de refus, **titre** faux |
| un mot (`Bonjour`), `Hello world` | 7 / 11 étiquettes, **langue `und`** |
| mot de 192 caractères | 9 étiquettes, pas de crash |
| NUL, tabs, contrôles | pas de crash ; **trous graphème** |
| arabe, hébreu, grec, japonais, coréen | pas de crash ; script correct ; **0 syntagme** ; titres faux (arabe, hébreu, japonais) |
| table markdown, code, JSON, URL seule | pas de crash ; URL seule : 67 étiquettes + chevauchement |
| **surrogate isolé** (`"\ud800abc"`) | **crash** `UnicodeEncodeError` à `len(texte.encode())` (ligne 1246) |
| `None` | `refus = "vide"` (silencieux) |
| `bytes`, `int`, `list` | **AttributeError** : `'int' object has no attribute 'isalpha'` (bytes) ; `'int' object has no attribute 'strip'` (int) ; `'list' object has no attribute 'strip'` (liste) |

**Bilan** : **1 plantage textuel** (surrogate, fabriqué) + **3 plantages d'entrée non-str** sur
25+4 cas ; **0/50** sur les phrases libres. Le bloc n'a pas de validation de type à l'entrée.

## 4. Performance

Mesures chaudes, 10/50/200 mots (médiane de 31/21/11 répétitions) :

| mode | 10 mots | 50 mots | 200 mots | ms/mot (200) |
|---|---:|---:|---:|---:|
| **heuristique** | **1,08 ms** | **4,60 ms** | **19,43 ms** | 0,097 |
| mock neuronal | 0,30 ms | 1,08 ms | 4,44 ms | 0,022 |
| parallèle | 1,51 ms | 6,18 ms | 27,22 ms | 0,136 |
| cascade | 1,51 ms | 6,25 ms | 29,64 ms | 0,148 |

- **Débit** : 923 phrases/s à 10 mots, 218/s à 50, 51,5/s à 200. Le mode par défaut est
  **largement assez rapide pour une phrase** ; sur un document de plusieurs milliers de mots, la
  composante superlinéaire commence à se voir.
- **Coût des compositions** : +37 % (parallèle) et +45 % (cascade) à 200 mots **avec le mock** ;
  avec le vrai modèle, le coût réseau/LLM domine et n'est pas mesuré ici.
- **Mémoire** : pic `tracemalloc` **540,6 Kio** pour 200 mots / 1 061 étiquettes ; RSS du processus
  **30,7 Mio**, **delta 0** après 100 analyses (pas de fuite observée). Démarrage à froid :
  **99–113 ms** (import + première analyse), **27,4 Mio**.
- **Passage à l'échelle** : 200 mots 19 ms (0,096 ms/mot), 500 mots 70 ms (0,139), 1 000 mots
  166 ms (0,166), 2 000 mots 482 ms (0,241), 4 000 mots **1 574 ms** (0,394). Le coût par mot
  est multiplié par **4,1** entre 200 et 4 000 mots (exposant ≈ 1,45). cProfile sur 2 000 mots :
  `_cible_proche` appelle `_est_adverbe_seul` **199 302 fois** et retrie les GV à chaque segment
  (lignes 800-853). Pour une phrase ou une page, c'est linéaire et confortable ; pour un document
  long, c'est le seul point de performance à corriger.
- **Déterminisme** : même instance, instances fraîches, graines de hash **0/1/42** → **mêmes
  digests** ; `json()` par défaut **exclut `duree_s`** ; `json(avec_duree=True)` ne diffère que par
  la durée. Deux textes différents ont des digests différents.

## 5. Stabilité du contrat

**Ce qui est stable.** `Annotation.json()` a **toujours les 11 mêmes clés** et `Etiquette.json()`
les **11 mêmes clés** sur les 50 textes et les quatre modes. Les spans sont dans le texte,
`debut <= fin`, **aucun span vide**, `niveau` dans les neuf, `type` non vide, `source` d'étiquette
dans `{heuristique, neuronal, humain}`, `confiance` dans [0,1] pour l'heuristique, unités triées
et disjointes, fraction recalculable, **0 cible absente**.

**Ce qui peut être vide ou absent.**

| élément | constat sur 50 textes |
|---|---|
| `etiquettes` | vide seulement sur refus (0/50 ici) |
| `unites_semantiques`, `fraction_semantique` | peuvent être vides / 0,0 (pas sur ce banc, mais sur du texte sans classe ouverte) |
| `refus` | vide en succès ; `"vide"` sur entrée vide/ponctuation ; **quatre sémantiques** selon l'implémentation (voir § 6) |
| `candidats` | vide pour **1 778/1 778** graphèmes, **963/963** mots, **384** POS fermées, 53 document, 76 phrase ; non vide pour syntagme, morphème, POS ouverte |
| `meta` | vide pour graphème, mot, phrase, pragmatique, discours, document, morphème ; non vide pour POS (`ouvert`, `contexte` 14 fois) et syntagme (`role`, `niveau`, `attachement` 265, `union` 98) |
| `contexte` | vide si non fourni ; **perdu** dans `Parallele`/`Cascade` (le label `pragmatique.contexte` reste) |
| `langue` | `"und"` possible ; **`fr`/`en` en défaut, `fra`/`eng` avec les profils**, format mixte avec `NeuronalLLM` |
| `script` | `"Zyyy"` possible |
| `niveaux` | sous-ensemble : **morphème 41/50**, **syntagme 48/50** ; les autres 7 toujours là |
| `type` | vocabulaire ouvert : 11 classes POS, 5 syntagmes, 3 phrase, 2 pragmatique, 2 discours, 2 document, 2 morphème, 5 graphème, 3 mot ; **`url` et `emoji` jamais émis** |
| `valeur` | **surface** pour graphème/mot/pos/syntagme (100 %) ; **normalisée** pour morphème (126/134) ; **tronquée à 60** pour document (42/53) ; **catégorielle** pour phrase/pragmatique/discours ; **contexte** pour `pragmatique.contexte` |
| `cout` | **clés variables** : `caracteres` seulement pour Heuristique ; `etiquettes` absent sur refus ; `octets` toujours |
| `trace` | schéma variable (`langue`, `niveaux`, `neuronal`, `fusion`, `cascade`, `refus`) : **ne pas parser** |
| `Annotation.source` | **quatre valeurs** : `heuristique`, `neuronal`, `parallele`, `cascade` — deux hors de l'enum documenté pour les étiquettes |
| attachement | **265** cibles, **16** mots fermés, **3** ambiguës ; **pas d'offset de cible** |
| `par_niveau()` / `couverture()` | ne rendent que les niveaux **présents** ; `couverture()` = **max de confiance**, pas un taux de couverture |

**Ce qu'un client peut parser sans casser** : l'enveloppe (les 11 + 11 clés), les offsets, le
`niveau`, le `type` comme chaîne, `confiance` (pour l'heuristique), la `source` d'étiquette, et
`valeur` pour graphème/mot/pos/syntagme. **Ce qu'il ne peut pas supposer** : que les syntagmes
sont disjoints, que les neuf niveaux sont là, que `valeur` est la surface, que `meta`/`cout`/`trace`
ont un schéma fixe, que `langue` est ISO2 ou ISO3, que `Annotation.source` est dans l'enum,
que `refus` est un enum, ou que l'attachement porte l'offset de sa cible.

## 6. Compositions

- **Refus perdu** : `"... !!! ???"` → Heuristique refuse, **0 étiquette** ; `Parallele` et
  `Cascade` rendent **4 étiquettes** (le mock invente des phrases) et `refus = ""`. Texte vide →
  `refus = ""` aussi. `MockNeuronal` n'a pas la garde vide/ponctuation de `Heuristique`.
- **Contexte perdu** : `Parallele`/`Cascade` rendent `Annotation.contexte = ""` alors que le label
  `pragmatique.contexte` (source `humain`) est bien présent.
- **`RefusNeuronal` non rattrapé** : avec un modèle absent, `Cascade(Heuristique(), NeuronalLLM(...))`
  et `Parallele` **lèvent** au lieu de rendre l'annotation heuristique déjà calculée. Le contrat
  refuse est **double** : `NeuronalLLM` lève, `NeuronalLLMPOS/Chunks/Pragmatique` rendent une
  `Annotation(refus=..., etiquettes=[])`.
- **Cascade non sélective** : **50/50** appels sur le banc, **1 676/1 676** sur le gold. Le résidu
  contient **morphème 50/50, syntagme 50/50, discours 50/50, pragmatique 50/50, pos 2/50**. Le
  seuil **0,6** est au-dessus des confiances déclarées (syntagme 0,55, pragmatique 0,45, discours
  0,55, morphème 0,32) : la cascade appelle donc **toujours**. Et `couverture()` = max cache les
  POS ouvertes à 0,3 (d'où `pos` résiduel seulement 2/50).
- **Environnement** : `DEEPSEEK_KEY_FILE` change la politique de `Parallele`/`Cascade` — même
  texte, même code : **55 → 49 étiquettes** et la source des syntagmes passe d'heuristique à
  neuronal. Le rejeu dépend donc d'une variable d'environnement non déclarée dans l'entrée.
- **Priorité par défaut** : `priorite_syntagme="heuristique"` garde le découpage heuristique ; le
  tagger réel documenté exige `"confiance"`. Un utilisateur qui compose sans lire la doc obtient
  le **mauvais** découpage avec le vrai modèle.
- **NeuronalLLM** : `float(e.get("confiance", 0.5))` n'est **pas borné** (ligne 1377) ; une réponse
  1,7 ou -0,2 viole le contrat [0,1]. `type`/`valeur` ne sont pas validés.

## 7. Correctifs produit

Sauf mention, les lignes sont celles de [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py).

### Bloquants

| # | correctif | preuve chiffrée | lignes | coût | risque |
|---|---|---|---|---|---|
| **P0-1** | **Expliciter les alternatives de syntagmes** (ou offrir une partition mesurée) | **132 paires / 31 textes**, 188/362 étiquettes ; f02 : GP 29-51 & 29-60, GV 80-96 & 90-96 | 1151-1156, 1170-1176, 1197-1203, 1239 ; `_supprimer_chevauchements` 1814-1843, appel 1908 | **0,5–1 j** | moyen : la déduplication donne F1 0,5849→0,6141 mais l'attachement exact 222→208 (couverture 0,9289→0,8703) ; préférer `meta.alternative` + option de partition à une déduplication silencieuse |
| **P0-2** | **Réparer les frontières de phrase et la tokénisation numérique** (décimaux, dates, URL, emails, abréviations, espace initial) | « 12.5 » coupe une phrase en 2 fragments ; « 12.03.2024 » en 3 ; URL → 3–4 ; `M./Dr./etc.` duplique la phrase (f10 : 0-104 & 2-104) ; 6/60 spans commencent par un espace ; `url`/`emoji` : 0/963 | 550, 553-563, 568-587 (surtout 570, 579) | **0,5–1 j** | faible-moyen : change le nombre de phrases et les actes par phrase ; tests dédiés obligatoires |
| **P0-3** | **Propager refus et contexte, rattraper `RefusNeuronal`, garder `MockNeuronal`** | `"... !!! ???"` → 4 étiquettes inventées, refus perdu ; contexte perdu ; modèle absent → exception ; mock sans garde | 1875-1922 (retour 1915-1922), 1276-1315, 1942-1947, 1970-1985, 1348-1349 | **0,5 j** | faible : gardes + propagation ; tests de composition à compléter |
| **P0-4** | **Rendre la cascade réellement sélective** (seuil par niveau, résidu sur absence/fraction, pas sur le max) | **50/50** appels ; 1 676/1 676 gold ; résidu morphème/syntagme/discours/pragmatique 50/50 ; `pos` 2/50 | 111-114, 1956, 1970-1985 | **0,5–1 j** | moyen : change les chiffres de la cascade et les portes ; ajouter un test « au moins une phrase sans appel » |
| **P0-5** | **Unifier le code langue et ne pas activer les 398 profils sur du texte court** | défaut **50/50** ; profils **39/50** mappés (30/34 fr, 7/14 en, 2/2 und), **2/50** strict ; `fr`→`hns`, `en`→`sco`, `es`→`und` ; indice `fr` ignoré avec profils | 199-224, 540-545, 273-296, 158-189, 1366-1368 | **0,5–1 j** | moyen : format touchant tests/gold/clients ; code canonique + accesseur de compatibilité |

### Importants

| # | correctif | preuve chiffrée | lignes | coût | risque |
|---|---|---|---|---|---|
| **P1-6** | **Compléter POS pour nombres et ponctuation** | **157/963** tokens sans POS (137 ponctuation, 20 nombres) ; **25** tokens PONCT du gold comptés `?` ; POS 0,7581 | 1037-1041, 601-623 | **2 h** | faible : +25 tokens couverts au mieux sur 3 179 (≈ +0,008 POS), mais alignement token/POS complet |
| **P1-7** | **Geler l'enveloppe** : `cout`, `Annotation.source`, `refus`, `contexte` | `caracteres` seulement pour Heuristique ; `etiquettes` absent sur refus ; `Annotation.source` = parallele/cascade ; quatre sémantiques de refus ; contexte perdu | 116-127, 1011, 1246-1247, 1314, 1920-1922, 1976 | **2–3 h** | faible : toujours émettre les mêmes clés + documenter l'enum |
| **P1-8** | **Corriger le titre document et la valeur tronquée** | **42/53** valeurs font 60 caractères ; x48 + arabe/hébreu/japonais/chiffres → titre faux (`upper() == lower()` sur scripts sans casse) | 1224-1230 | **2 h** | faible : exiger une casse réelle + exposer le texte complet |
| **P1-9** | **Rendre le repli S visible** | sans générateur S : **34/50** sorties changent, **132 syntagmes** et **119 attachements** perdus, sans trace | 641-650, 652-667 | **2 h** | faible : trace `repli_s` + champ de mode, ou échec explicite |
| **P1-10** | **Supprimer la dépendance à `DEEPSEEK_KEY_FILE`** | même texte, même code : **55 → 49** étiquettes ; source des syntagmes heuristique→neuronal | 1849-1855, 1938-1940, 1965-1967 | **2 h** | faible : paramètre explicite + trace de politique |
| **P1-11** | **Petites incohérences de valeurs et de candidats** | **8/134** morphèmes normalisés ; **4/50** actes `exclamation` hors candidats ; **4/50** listes avec doublons | 626-638, 1045-1048, 1078, 1142-1150, 1172-1176, 1199-1203 | **2 h** | faible : casse d'origine, ajouter `exclamation`, dédupliquer |
| **P1-12** | **Valider l'entrée et les encodages** | `bytes`/`int`/`list` → AttributeError ; surrogate → `UnicodeEncodeError` à 1246 ; `None` → refus `vide` silencieux | 1003-1011, 1246 | **1–2 h** | faible : TypeError explicite + encodage tolérant/refus propre |
| **P1-13** | **Valider la sortie du modèle neuronal** | `float(e.get("confiance", 0.5))` non borné ; `type`/`valeur` non validés | 1371-1378 | **1 h** | faible : min/max + rejet des types inconnus |
| **P1-14** | **Qualité POS des classes ouvertes** (lexique ou tagger qualifié) | POS **0,7581** (ouvert 0,6234) ; sur 50 : **365 NOUN / 32 VERB** ; « arrose », « rentre », « prépare », « consultez », « débloque », « écrivez », « warm » → NOUN | 319-349, 390-443, 601-623 | **1–3 j** (données + validation) | moyen : un lexique plus large peut déplacer le gold ; le tagger réel documenté (0,9440) est la voie de production |
| **P1-15** | **Réduire le coût superlinéaire au-delà de 200 mots** | 0,096 ms/mot à 200, **0,394** à 4 000 (4,1×), 1,57 s à 4 000 ; `_cible_proche` : **199 302** appels à `_est_adverbe_seul` | 800-853, 461-464 | **2–3 h** | faible : préfiltrer les GV une fois, mémoïser les adverbes, indexer par position |

### Confort

| # | correctif | preuve chiffrée | lignes | coût |
|---|---|---|---|---|
| **P2-16** | Couvrir les caractères de contrôle dans graphème | x46 : **7 newlines** non couverts, 95,14 % ; 49/50 à 100 % | 1020-1031 | **15 min** |
| **P2-17** | Aligner la doc sur les plages réelles | fraction **0,3529–0,8750** (doc 0,51–0,76) ; `couverture()` = max, pas un taux | 111-114, 1237-1238 | **1 h** (doc) |
| **P2-18** | Nettoyages sans effet produit | `_verbe_dans` : boucle dupliquée 777-782 ; `trace` à schéma variable ; `priorite_syntagme="heuristique"` par défaut = mauvais choix pour le tagger réel | 777-782, 116-127, 1931, 1957 | **1 h** |

## 8. Contrôles négatifs

- **Les 6 mutations sont détectées (6/6)** : span hors texte, cible absente, chevauchement,
  confiance 1,7, valeur hors span, fraction incohérente. Le détecteur d'anomalies n'est pas
  complaisant ; noter que l'annotation de base porte déjà un chevauchement, donc le test de
  mutation ajoute une anomalie à un état déjà imparfait.
- **Le chunker seul ne chevauche pas** : 0 paire avec `segmenter_s=False, union=False`, contre 132
  avec le générateur S + union. Le défaut vient bien de la composition des segments, pas du
  détecteur.
- **La déduplication simulée** (`_supprimer_chevauchements`, politique actuelle de la fusion) :

| base | paires | syntagmes | attachements | F1 | P | R | tête | exact | couverture |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 50 phrases, avant | 132 | 362 | 265 | — | — | — | — | — | — |
| 50 phrases, après | **0** | 292 | 215 | — | — | — | — | — | — |
| gold 612, avant | — | — | — | **0,5849** | 0,6292 | 0,5464 | 0,7336 | **222** | **0,9289** |
| gold 612, après | — | — | — | **0,6141** | 0,7283 | 0,5309 | 0,7432 | **208** | **0,8703** |

La déduplication **gagne 0,0292 de F1 et 0,0096 de tête**, mais **perd 14 spans d'attachement
exacts** (222 → 208) et 50 attachements sur le banc (265 → 215). C'est exactement ce que font
déjà `Parallele` et `Cascade` (F1 0,6141, 208/208, couverture 0,8703) : la fusion déduplique, et
c'est pour cela qu'elle perd ces 14 spans. Le rouge `cascade_pos` est un **autre** effet (le
mélange du POS du mock), pas la déduplication. La bonne réponse produit n'est donc **pas** de
dédupliquer en silence : c'est d'exposer les alternatives et d'offrir une vue « partition » dont
le coût est mesuré.
- **Contrôle de langue négatif** : 8 textes à caractères mélangés ; au niveau du bloc (seuil 0,12),
  **6/8 reçoivent quand même une langue** (fr, en, de, it), avec une confiance jusqu'à **0,5**.
  Le détecteur par mots-outils n'est pas un rejeteur de bruit : `und` n'est pas garanti sur du
  charabia. C'est un point à documenter ou à corriger par un seuil/longueur minimale.
- **Déterminisme** : même instance, instances fraîches, graines 0/1/42 → identiques ; deux textes
  différents → digests différents. Dans un environnement fixé, la seule nondétermination est
  `duree_s`, exclue par défaut (mais `DEEPSEEK_KEY_FILE` peut changer la politique, § 6).

## 9. Ce que ce banc ne dit pas — et ce qui pourrait le rendre faux

- Les **50 phrases sont écrites à la main**, pas un tirage aléatoire : le **0 plantage** et le
  **50/50 langue** ne sont pas des garanties de production.
- L'audit vérifie des **invariants structurels**, pas la **justesse sémantique**. La qualité POS
  sur texte libre n'a pas de gold ; on cite le gold 0,7581 et des exemples, pas une exactitude
  libre.
- Le gold est **in-sample** : les règles y ont été dessinées ; dev/test limitent sans exclure.
- Une seule machine, un seul interpréteur ; la performance du **vrai** neuronal (réseau, LLM) et
  son coût ne sont pas mesurés.
- Le comparatif de langue avec les profils porte sur **50 phrases favorables fr/en + 2 non-latin**,
  pas sur un échantillon multilingue ; il ne dit pas que les profils sont mauvais en général, il
  dit qu'ils **dégradent le court fr/en** et changent le format.
- La simulation de déduplication dépend de la politique : `_supprimer_chevauchements` est la
  politique **actuelle** de la fusion, pas la seule possible. Une autre politique pourrait
  conserver les 14 spans.
- Le plantage **surrogate** est un cas d'encodage fabriqué ; il ne prouve pas un plantage sur du
  texte UTF-8 valide, mais il montre que l'encodage n'est pas validé.
- Les chiffres `222/222`, `0,9289`, `0,5849`, `0,7581`, `17` sont ceux du **vivant 612** au
  commit `fa1b0c6e` ; la fiche v12 publie le F1/tête du **gelé 602** (0,5893/0,7392, POS 0,7603).
  Un commit ultérieur peut les déplacer.
- **Le verdict `cascade_pos` a changé dans `7f73c17f`** (plancher 0,70 au lieu de la
  comparaison à l'heuristique) : `ok` passe de faux à vrai **sans** changement du module ni des
  valeurs. Le rouge de l'état fourni est donc éteint par le harnais ; la baisse de POS de la
  composition reste mesurée (0,7465 contre 0,7581).

## 10. Fichiers et reproductibilité

- [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) — le module audité.
- [`tools/tests/linguistique/evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) —
  `charger`, `evaluer_bloc` ; [`gold_split.py`](../tools/tests/linguistique/gold_split.py) — dev/test.
- [`pensee-produit-bloc-l.json`](pensee-produit-bloc-l.json) — **les 50 textes**, les 25 cas
  limites, les 18 correctifs, tous les chiffres et les contrôles.
- Harnais local **non committé** : `/tmp/audit_produit_bl/` (`phrases.py`, `audit.py`,
  `performance_final.py`, `extra.py`, `construire_json.py`).
- Rejeu : `PYTHONPATH=. python3 tools/tests/linguistique/evaluer_gold.py` ;
  `bash tools/porte-bloc-linguistique.sh` (verte).
- **Aucun fichier existant modifié par cet audit, aucun commit, `reports/README.md` non modifié**
  (consigne).

## 11. Les 5 correctifs prioritaires

1. **P0-1 — Expliciter les alternatives de syntagmes** : 132 paires dans 31/50 textes, 188/362
   étiquettes ; ne pas dédupliquer en silence — `meta.alternative` + vue « partition » mesurée
   (F1 +0,0292, mais 222 → 208 attachements exacts).
2. **P0-2 — Réparer les frontières de phrase** (décimaux, dates, URL/emails, abréviations, espace
   initial) et les types `url`/`emoji` morts : une URL crée 3–4 phrases, `12.5` coupe une phrase
   en deux fragments (`12.03.2024` en trois), `M./Dr./etc.` duplique la phrase.
3. **P0-3 — Compositions** : propager `refus` et `contexte`, rattraper `RefusNeuronal`, garder
   `MockNeuronal` sur vide/ponctuation ; aujourd'hui `"... !!! ???"` rend 4 étiquettes inventées.
4. **P0-4 — Cascade sélective** : 50/50 appels, 1 676/1 676 sur le gold ; le seuil 0,6 est
   au-dessus des confiances déclarées et `couverture()` = max masque les POS ouvertes. Le verdict
   `cascade_pos` est vert par plancher (harnais `7f73c17f`), pas par correction du comportement.
5. **P0-5 — Langue** : format `fr`/`fra` selon le mode, indice `fr` ignoré avec les profils,
   **39/50** seulement avec les profils contre **50/50** en défaut.

Juste derrière : **P1-6** (POS des nombres/ponctuation, 157/963 tokens) et **P1-14** (POS ouvertes
0,6234 ; 365 NOUN pour 32 VERB ; le tagger réel documenté à 0,9440 est la voie de production).
