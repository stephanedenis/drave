# B13 — la restitution v1 : la forme canonique à 46/46, le miroir strict reste à 0,1087

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : J8.1 · **Date** : 2026-11-14 ·
> **Verdict** : ✅
>
> **La question.** Au-delà de la surface exacte (46/46), produire une **forme canonique**
> depuis l'annotation — **segments + rôles + cibles** — et la mesurer : le **miroir strict**
> (0,1087) doit-il monter ?
>
> **La réponse.** **Non — et il ne doit pas.** Le miroir strict compare une sortie à la
> **surface brute** ; la forme canonique replie la casse, retire la ponctuation et réduit
> les espaces. Contre la source canonisée, elle est exacte **46/46 = 1,0000** ; contre la
> source brute, elle tombe à **1/46 = 0,0217** (seul `f18`, `1234567890`, n'a ni casse ni
> ponctuation). Le **miroir strict reste 5/46 = 0,1087** : la v1 ne fabrique pas de
> surface, elle mesure autre chose. Le chiffre utile de la v1 est **1,0000 canonique**,
> pas 0,1087 strict.
>
> **Le chiffre.** 46 annotations, **46/46 formes canoniques exactes** contre la source
> canonisée ; **395 segments**, **395 rôles**, **315 cibles**, **315/315 cibles résolues**
> dans la source, **313/315** portées par un autre segment ; couverture moyenne
> **65,84 % des jetons** et **75,19 % des caractères** ; stabilité structurelle
> **18/46 = 0,3913** (le lexique, lui, est stable 46/46). Contrôles : mélange et
> troncature canoniques **0/46**, détection **46/46** ; rôles/cibles retirés, clé changée
> **43/43** textes éligibles.
>
> **Dispositif** : [`restitution.py`](../tools/restitution.py) (`forme_canonique`,
> `miroir_canonique`, `mesurer_banc_v1`), [`drave.py`](../tools/drave.py)
> (`restituer --canonique`), [`mesurer_restitution_v1.py`](../tools/mesurer_restitution_v1.py) ;
> JSON [`pensee-restitution-v1.json`](pensee-restitution-v1.json) ;
> banc [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json) ;
> fiche v0 [`rapport-restitution-v0.md`](rapport-restitution-v0.md).

## 1. La commande

```bash
python3 tools/drave.py restituer "Le chat dort." --canonique
```

```
restitution v1 (surface + forme canonique)
source         : 'Le chat dort.'
surface brute  : 'Le chat dort.'
miroir strict  : 0.0000 (non exact) — surface/mots/POS vs source brute
forme canonique: 1.0000 (exacte) — jetons canoniques vs source canonique
  caractères   : 1.0000
strict sur la forme canonique : 0.0000 (la forme n'est pas la surface : le strict ne doit pas monter)

forme canonique (segments + rôles + cibles)
surface canonique : 'le chat dort'
squelette :
  GN/agent: le chat -> dort
  GV/predicat: dort -> chat
segments 2 · rôles 2 · cibles 2 · résolues 2/2 · dans un segment 2/2

contrôle négatif canonique : mélange exacte 0.0000 · troncature exacte 0.0000 · détecté True
contrôle de structure : rôles retirés 2 · cibles retirées 2 · clé changée True
stabilité structurelle : oui (2 → 2 segments après re-analyse de la surface canonique)
```

La v0 reste la sortie par défaut : `restituer "Le chat dort."` affiche toujours la
surface et le miroir strict. `--canonique` ajoute la lecture structurelle ; `--banc ...
--canonique --json` produit le JSON de la fiche.

## 2. Ce que la forme canonique contient

La forme est construite **depuis les étiquettes**, sans lire `Annotation.texte` :

| pièce | source | rôle |
|---|---|---|
| `segments` | niveau `syntagme` | type, rôle, span, valeur, cible et `cible_segment` |
| `squelette` | vue **linéaire** | `TYPE/rôle : valeur canonique -> cible canonique` |
| `jetons` | `mot` > `pos` > `graphème` | plancher lexical : casse repliée, lettres/chiffres |
| `surface_canonique` | `jetons` | les jetons joints par une espace |
| `cle` | tout le corps | sha256 du JSON canonique (clés triées) |

La **linéarisation** choisit les segments par la clé publiée du dépôt : le chunker
(`union`) d'abord, puis le plus large, puis le plus sûr. Les autres segments restent dans
`segments` (`lineaire: false`) : c'est une vue de lecture, pas une suppression. Le
**rôle** et la **cible** viennent de `meta` (`role`, `attachement`) ; `cible_segment` est
le premier **autre** segment dont les jetons contiennent la cible.

La canonisation est volontairement pauvre : `[^\W_]+` sur la casse repliée. Deux
surfaces qui ne diffèrent que par la casse, la ponctuation ou les espaces ont la même
forme. C'est ce qui rend la mesure comparable à une **source canonisée**, et c'est aussi
pourquoi elle ne peut pas reproduire la source brute.

## 3. Les chiffres

### 3.1 Strict contre canonique

| mesure | v0 | v1 |
|---|---:|---:|
| annotations / refus | 46 / 4 | 46 / 4 |
| surface `graphème` exacte | **46/46 = 1,0000** | 46/46 (inchangée) |
| **miroir strict** (min surface/mots/POS) | **5/46 = 0,1087** | **5/46 = 0,1087** |
| **miroir canonique** (min mots/POS/forme vs source canonisée) | — | **46/46 = 1,0000** |
| fidélité de caractères canonique | — | **1,0000** |
| strict sur la forme canonique | — | **1/46 = 0,0217** |
| fidélité de caractères du strict sur la forme | — | 0,8566 |

Le miroir strict **ne monte pas** : il est identique à la v0, parce que la v1 ne remplace
pas la surface. La forme canonique, elle, est exacte **46/46** contre la source canonisée.

### 3.2 La structure

| mesure | valeur |
|---|---:|
| segments | **395** |
| segments avec rôle | **395/395 = 1,0000** |
| cibles (attachements) | **315** |
| cibles résolues dans la source | **315/315 = 1,0000** |
| cibles portées par un autre segment | **313/315 = 0,9937** |
| couverture des jetons par les segments (moyenne) | **0,6584** |
| couverture des caractères par les segments (moyenne) | **0,7519** |
| stabilité structurelle (forme → surface → forme) | **18/46 = 0,3913** |
| stabilité des jetons | **46/46 = 1,0000** |

**Lecture.** Les segments ne couvrent que **65,84 %** des jetons : le plancher lexical
remplit le reste (déterminants, prépositions, ponctuation, mots hors syntagme). Les
cibles sont **toutes** retrouvées dans la source, et **313/315** sont portées par un autre
segment — les deux autres sont des cibles hors segment, pas des cibles inventées.
Les rôles et les cibles sont donc **cohérents** ; ils ne sont pas **justes** : sans gold
de forme canonique, on ne peut pas dire que `agent` ou `dort` sont les bons choix.

**La stabilité est la limite.** Re-analyser la surface canonique (`le chat dort`) donne
le même squelette pour **18/46** seulement : sans ponctuation ni casse, le bloc heuristique
segmente autrement. Le lexique est stable 46/46 (mêmes jetons), la structure ne l'est pas.
La forme canonique n'est donc **pas un point fixe** du bloc ; c'est une lecture, pas un
normalisateur idempotent.

### 3.3 Les cas utiles

- **`f01`** (`Le chat dort.`) : GN/agent `le chat -> dort`, GV/prédicat `dort -> chat` ;
  strict 0, canonique 1.
- **`f18`** (`1234567890`) : aucun segment, un seul jeton ; strict 1 **et** canonique 1.
  C'est le seul texte où la forme canonique est identique à la source brute.
- **`f50`** (2 144 caractères, 4 paragraphes) : la surface reste exacte (correctif `C` de
  la v0) ; la forme canonique est exacte, mais la stabilité structurelle échoue (la
  ponctuation des paragraphes guidait la segmentation).

## 4. Pourquoi le miroir strict ne monte pas

Le miroir strict est le **minimum** des fidélités binaires `surface` / `mots` / `pos`
contre la source **brute**. La v0 est à 0,1087 parce que `rendre_mots` et `rendre_pos`
joignent les tokens par une espace : `dort.` devient `dort .`, `l'eau` devient `l' eau`.
La v1 ne change pas cette couche : elle ajoute des **segments**, des **rôles** et des
**cibles**. Ces objets disent **quels tokens vont ensemble** et **vers quoi ils pointent** ;
ils ne disent pas **où est l'espace** ni **si le point est collé**. Cette information est
dans le niveau `graphème` (et le correctif `C`), c'est-à-dire dans la v0.

D'où les deux mesures, qui ne se remplacent pas :

- **strict** = « la sortie est-elle la source, caractère pour caractère ? » → 0,1087,
  inchangé ; la forme canonique, elle, tombe à 1/46 ;
- **canonique** = « les jetons et leur ordre sont-ils ceux de la source, une fois la
  présentation normalisée ? » → 1,0000.

Si le strict montait avec les rôles et les cibles, c'est que la forme canonique aurait
recopié la surface : elle n'apporterait rien. Le fait qu'il **ne monte pas** est le
résultat attendu ; le fait qu'il **tombe** à 1/46 quand on lui donne la forme canonique
est le contrôle qui montre que la v1 n'est pas un codec de surface déguisé.

## 5. Les contrôles négatifs

**Canonique.** Même principe que la v0, sur les jetons : mélange déterministe (graine 0)
et troncature du dernier jeton.

| contrôle | exacts | caractères |
|---|---:|---:|
| mélange | **0/46** | 0,3865 |
| troncature | **0/46** | 0,7998 |
| détection | **46/46** | — |

**Structure.** On retire les rôles et les cibles de la forme, puis on recalcule la clé :

| contrôle | valeur |
|---|---:|
| textes éligibles (au moins un rôle ou une cible) | **43/46** |
| rôles retirés | **395** |
| cibles retirées | **315** |
| clé changée | **43/43** |

Les 3 textes non éligibles (`f18`, `f27`, `f37`) n'ont aucun segment : il n'y a rien à
retirer. Le contrôle ne dit pas que les rôles sont **justes** ; il dit que la mesure les
lit et que la clé en dépend.

## 6. Ce que la v1 ne dit pas

- **La fidélité sémantique** : 1,0000 canonique est un **invariant de codec**. Les jetons
  viennent des spans `mot`/`pos`, qui sont des sous-chaînes de la source ; la canonisation
  retire la présentation. Cela prouve que le contenu lexical et l'ordre sont conservés,
  pas que la phrase est comprise.
- **La justesse des rôles et des cibles** : 395 rôles et 315 cibles sont **cohérents**
  (tous résolus, presque tous dans un autre segment), mais il n'y a pas de gold de forme
  canonique. Un rôle faux reste un rôle cohérent.
- **La complétude de la structure** : les segments ne couvrent que 65,84 % des jetons.
  Le plancher lexical masque les mots hors syntagme ; il ne les structure pas.
- **La stabilité** : 18/46 seulement. La forme canonique n'est pas un point fixe ; une
  vraie forme canonique demanderait un analyseur insensible à la présentation, pas
  l'heuristique de surface.
- **Les 4 refus** : `f14` (emoji), `f15` (vide), `f16` (espaces), `f17` (`...`) n'ont pas
  d'annotation. Si on les compte comme des échecs, la forme canonique est **46/50 =
  0,9200**.
- **Le corpus** : 50 textes écrits à la main (audit A26), pas un échantillon aléatoire ;
  le temps de la mesure complète est ≈ 12 s.

## 7. Ce qui pourrait rendre cette fiche fausse

- **La définition de la canonisation** : `[^\W_]+` sur la casse repliée. Une autre
  normalisation (accents conservés/retirés, chiffres séparés, ponctuation conservée)
  changerait le 1,0000. Le JSON publie la règle et les jetons pour que le calcul soit
  refaisable.
- **La définition du miroir canonique** : c'est le **minimum** de mots/POS/forme, comme
  le strict. Une moyenne ou la forme seule donnerait le même 1,0000 ici, mais pas
  nécessairement sur un autre banc.
- **La linéarisation** : la clé `(union, largeur, confiance, début, fin, type)` est une
  convention mesurée sur le gold 612 (le chunker le plus large est le span du gold dans
  86,5 % des groupes ambigus). Une autre préférence changerait le squelette et la
  stabilité.
- **Le choix de la stabilité** : comparer le **squelette** est sévère (il inclut les
  cibles et l'ordre). Comparer les jetons donne 46/46 ; les deux chiffres sont publiés.
- **Le banc** : 46 annotations seulement, dont 3 sans segment ; les textes très longs ou
  bruités ne sont pas couverts.

## 8. La suite

1. **Un gold de forme canonique** : quelques phrases avec segments/rôles/cibles attendus,
  pour mesurer la **justesse**, pas seulement la cohérence.
2. **Un analyseur insensible à la présentation** : la stabilité 18/46 est le signal ; il
  faut segmenter sur les tokens, pas sur la ponctuation, pour que la forme soit un point
  fixe.
3. **Un usage produit** : exposer `--canonique` dans la doc produit et l'utiliser comme
  contrôle de régression (la clé change si un rôle ou une cible change).
4. **La v0.1 de la ponctuation** : replacer la ponctuation sur les spans `mot` ferait
  monter le **strict** sans lire la source ; c'est un autre chantier, et il ne doit pas
   être confondu avec la forme canonique.

## 9. Fichiers

- [`restitution.py`](../tools/restitution.py) — `forme_canonique`, `miroir_canonique`,
  `structure_canonique`, `stabilite_structurelle`, `mesurer_banc_v1`.
- [`drave.py`](../tools/drave.py) — `restituer --canonique` (texte et banc).
- [`mesurer_restitution_v1.py`](../tools/mesurer_restitution_v1.py) — produit le JSON.
- [`test_restitution.py`](../tools/tests/test_restitution.py) — **22 tests** (11 v0 + 11 v1).
- [`pensee-restitution-v1.json`](pensee-restitution-v1.json) — les 50 résultats, la
  synthèse, les contrôles et les limites.
- [`pensee-restitution-v0.json`](pensee-restitution-v0.json) — la référence de surface.
- [`rapport-restitution-v0.md`](rapport-restitution-v0.md) — la v0 et le miroir strict.
