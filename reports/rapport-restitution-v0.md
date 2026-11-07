# B13 — la restitution v0 : 46/46 surfaces exactes, le miroir strict à 0,1087

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : J1.4 · **Date** : 2026-11-07 ·
> **Verdict** : ✅
> **Ce que la commande fait** : `python3 tools/drave.py restituer TEXTE` analyse le texte,
> reconstruit la surface depuis le niveau **`graphème`** de l'annotation — **sans lire
> `Annotation.texte`** — et affiche la fidélité du **miroir** (surface, mots, POS), la fidélité
> de caractères et un **contrôle négatif**. `restituer --banc` rejoue le banc des 50 textes.
>
> **Le chiffre.** Sur les **50 textes libres** de l'audit A26 : **46 annotations** (4 refus),
> **46/46 surfaces exactes** (1,0000) ; le **miroir strict** — le minimum des fidélités
> surface/mots/POS — vaut **5/46 = 0,1087** ; le contrôle négatif casse **46/46**.
> Le miroir a trouvé un trou : `f50` perdait ses **10 sauts de ligne** (45/46, 0,9783) ;
> le correctif `C` les annote et la surface revient à 46/46.
>
> **Dispositif** : [`drave.py`](../tools/drave.py) (`restituer`, `--banc`, `--json`),
> [`restitution.py`](../tools/restitution.py) (reconstruction, Levenshtein, miroir, contrôle),
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (catégorie `C` → `contrôle`),
> [`mesurer_restitution_v0.py`](../tools/mesurer_restitution_v0.py) ;
> JSON [`pensee-restitution-v0.json`](pensee-restitution-v0.json) ;
> banc [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json).

## 1. La commande

```bash
python3 tools/drave.py restituer "Le chat dort."
```

```
restitution (annotation → surface)
source      : 'Le chat dort.'
surface     : 'Le chat dort.'
fidélité    : exacte 1.0000 · caractères 1.0000 · couverture 100.00%
mots        : exacte 0.0000 · caractères 0.9286 · couverture 84.62%
pos         : exacte 0.0000 · caractères 0.9286 · couverture 84.62%
miroir      : 0.0000 (non exact) — minimum des fidélités binaires de la surface (graphème),
              des mots et des POS ; une sortie n'est fidèle que si elle reproduit exactement
              la source
contrôle négatif : mélange exacte 0.0000 (caractères 0.3077) · troncature exacte 0.0000
                   (caractères 0.9231)
```

**Lecture.** La **surface est exacte** (c'est la restitution demandée). Le **miroir strict**
tombe à 0 parce que `mots` et `pos` séparent le point du mot (`dort .`) : la ponctuation est
un token, pas un suffixe. Ce n'est pas une erreur de reconstruction, c'est la définition du
miroir : une sortie n'est fidèle que si elle reproduit la source **exactement**. La fidélité
de caractères (0,9286) dit, elle, que 93 % des caractères sont au bon endroit.

## 2. Les chiffres sur les 50 textes libres

| mesure | valeur |
|---|---:|
| textes du banc | 50 |
| annotations (textes linguistiques) | **46** |
| refus d'analyse | **4** (`f14` emoji, `f15` vide, `f16` espaces, `f17` `...`) |
| surface `graphème` exacte | **46/46 = 1,0000** |
| surface sans le correctif `C` | **45/46 = 0,9783** (0,9999 en caractères) |
| fidélité de caractères de la surface | **1,0000** |
| mots exacts | **5/46 = 0,1087** |
| fidélité de caractères des mots | **0,9506** |
| POS exacts | **5/46 = 0,1087** |
| fidélité de caractères des POS | **0,9506** |
| **miroir strict** (min surface/mots/POS) | **5/46 = 0,1087** |
| contrôle négatif — mélange | **0/46 exact**, 0,2630 en caractères |
| contrôle négatif — troncature | **0/46 exact**, 0,9506 en caractères |

Les 5 textes où mots et POS sont exacts sont `f03`, `f05`, `f18`, `f40`, `f44` : leur
ponctuation est déjà séparée par une espace (`Bonjour !`), ou le texte n'a qu'un token
(`1234567890`), ou les caractères sont isolés (`@ # $ %`). Les 41 autres échouent sur le
même motif : `dort.` devient `dort .`, `l'eau` devient `l' eau`, une URL se coupe. C'est
pourquoi la fidélité de caractères reste à 0,9506 alors que l'exactitude tombe à 0,1087 :
la perte est locale (ponctuation, apostrophes), pas massive.

## 3. Ce que le miroir a trouvé : les sauts de ligne

Le niveau `graphème` était construit sur les catégories Unicode `L`, `N`, `P`, `Z`, `S`, `M`.
La catégorie **`C` (contrôle)** — sauts de ligne, tabulations, marques de format — n'était pas
annotée. Sur `f50` (2 144 caractères, 4 paragraphes), la restitution perdait donc ses
**10 sauts de ligne** (7 spans `\n` ou `\n\n`) : **45/46** surfaces exactes, 0,9999 en
caractères. Le correctif ajoute `"C": "contrôle"` au dictionnaire des classes ; la surface
revient à **46/46**, sans toucher aux POS, aux syntagmes ni aux mesures du gold
(`evaluer` : POS 86,25 %, F1 79,02 %, attachement 237/238).

C'est le résultat utile de la v0 : **le miroir n'a pas seulement recopié, il a trouvé un
trou dans la couche de surface.** Le JSON garde la mesure `surface_sans_controle` pour que
le « avant » reste vérifiable.

## 4. Le miroir strict, et ce qu'il mesure

Le miroir est celui de [`miroir.py`](../tools/tests/linguistique/miroir.py) :

- `fidelite` est **binaire** : 1,0 si la sortie est exactement la source, 0,0 sinon ;
- `miroir` est le **minimum** des fidélités `surface` (graphème), `mots` et `pos`.

Sur les 50 textes, la surface est à 1,0 mais mots et POS à 0,1087 ; le miroir vaut donc
0,1087. Le chiffre est **plus bas** que le miroir du gold (0,2276) parce que le corpus est
différent : les textes libres contiennent plus de ponctuation collée, d'URL, de courriels et
d'apostrophes que les phrases du gold. **Les deux chiffres ne se comparent pas** : ils ne
portent pas sur le même banc.

La restitution v0 est un **codec de surface**, pas un décodeur : elle prouve que
l'annotation conserve la surface, pas qu'elle conserve le sens. C'est la même limite que la
restitution canonique B18 (528/528, sans décodeur neuronal). La fidélité de caractères de
la surface est 1,0000 ; celle des mots/POS est 0,9506, avec un minimum à **0,7667** sur
`f38` (deux URL et un fragment `?d=e#f`).

## 5. Le contrôle négatif

Deux altérations déterministes de la surface, graine 0 :

- **mélange** : les graphèmes sont permutés ; s'il n'y en a qu'un (`f18`, `1234567890`), ils
  sont retournés, puis substitués si le retournement est un no-op (`a`, `aa`) — sinon le
  contrôle serait un no-op. Résultat : **0/46 exact**, 0,2630 en caractères.
- **troncature** : le dernier graphème est retiré. Résultat : **0/46 exact**, 0,9506 en
  caractères. La fidélité de caractères reste haute (un caractère manque), mais le miroir
  binaire la rejette : c'est précisément sa sévérité qui compte.

`detectes = 46/46` : aucune des 46 annotations ne passe le contrôle. Le contrôle ne dit rien
du sens ; il dit que la mesure n'est pas complaisante.

## 6. Ce que ce banc ne dit pas

- **La fidélité sémantique** : la surface exacte ne prouve pas que l'annotation a compris la
  phrase. Aucun gold de restitution n'est utilisé ; c'est un invariant de codec.
- **Les 4 refus** : `f14`, `f15`, `f16`, `f17` n'ont pas d'annotation (le bloc refuse les
  entrées sans lettre ni chiffre). Ils ne sont pas des échecs de restitution, mais ils ne
  sont pas mesurables. Si on les compte comme des échecs, la surface est **46/50 = 0,9200**.
- **La langue** : le banc laisse le bloc détecter (`langue=None`), comme le CLI sans
  `--langue`. Une mesure avec `--langue fr` sur les textes anglais donnerait autre chose.
- **Le corpus** : les 50 textes sont écrits à la main pour l'audit A26 ; ils ne sont pas un
  échantillon aléatoire.
- **Le temps** : la mesure complète du banc prend ≈ 9 s (Levenshtein sur les 46 textes) ;
  la surface seule est immédiate.

## 7. Ce qui pourrait rendre cette fiche fausse

- **La définition du miroir** : `min(surface, mots, pos)` est la définition de
  `miroir.mesurer` ; une autre définition (moyenne, surface seule) donnerait 1,0. Le JSON
  publie la définition pour que le lecteur puisse refaire le calcul.
- **La normalisation des POS** : `rendre_pos` joint les tokens par une espace ; la
  ponctuation séparée fait chuter l'exactitude. Ce n'est pas une mesure de la qualité
  linguistique des POS.
- **Le correctif `C`** : il ajoute des étiquettes `graphème` de type `contrôle` ; un client
  qui compte les étiquettes ou qui compare des octets de rejeu verra la différence de
  `f50`. Les POS, syntagmes et mesures du gold sont inchangés.
- **Le banc** : 46 annotations seulement ; les 4 refus et le caractère manuel limitent la
  portée. Un texte réel très long ou binaire n'est pas couvert.

## 8. La suite

1. **La restitution depuis les niveaux pauvres** : un `rendre_pos` qui replace la
   ponctuation sur les spans (sans lire la source) ferait monter le miroir ; c'est une v0.1,
   pas la v0.
2. **Le gold de restitution** : un jeu de phrases avec une sortie attendue, pour mesurer
   autre chose que l'invariant de surface.
3. **`g017`** : le dernier span du gold, puis T132/T133 et le gold 200+.

## 9. Fichiers

- [`drave.py`](../tools/drave.py) — la commande `restituer` (texte, `--banc`, `--json`).
- [`restitution.py`](../tools/restitution.py) — reconstruction, fidélités, contrôle, banc.
- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `C` → `contrôle` dans `graphème`.
- [`mesurer_restitution_v0.py`](../tools/mesurer_restitution_v0.py) — produit le JSON.
- [`test_restitution.py`](../tools/tests/test_restitution.py) — 11 tests.
- [`pensee-restitution-v0.json`](pensee-restitution-v0.json) — les 50 résultats, la synthèse,
  le contrôle et les limites.
- [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json) — le banc des 50 textes.
- [`porte-produit.sh`](../tools/porte-produit.sh) — deux contrôles de plus (commande + tests).
