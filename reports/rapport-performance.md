# T4 — la performance de `drave analyser` : 10 000 mots en 4,0 s, 126 Mio, 14,8 Mo de JSON ; le contrôle de linéarité **échoue** (α = 1,55)

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T4** (exploitable, 4/5) ·
> **Date** : 2026-11-15 · **Verdict** : ✅ **les 10 000 mots sont exploitables** (4,0 s de
> fonction, 2 493 mots/s, 126 Mio de pic RSS, 14,8 Mo de JSON) ; ❌ **le contrôle négatif de
> linéarité échoue** — le temps croît en **α = 1,55** sur un bloc contrôlé, et le terme
> quadratique explique **R² 0,99995** contre **0,957** pour le linéaire. Le coupable est
> nommé : `_groupes_partition` (toutes les paires de syntagmes, O(k²)) et `_cible_proche`
> (tri de tous les GV pour chaque segment), pas la tokenisation.
>
> **Les chiffres.** Sur le préfixe exact de **10 000 mots** de
> `data/corpus_fr_litterature.txt` (Alice, français), versionné dans
> [`reports/performance-corpus-10000.txt`](performance-corpus-10000.txt)
> (sha256 `0069b20e28975ca7b504755456aacf014b864b16705d40e6b381c45ae5e08871`,
> 57 588 caractères, 814 phrases) : **4,012 s** pour `Heuristique.analyser`, **4,965 s**
> pour le CLI `--json` (dont 0,672 s de sérialisation), **2 493 mots/s** (fonction) /
> **2 014 mots/s** (CLI), **128 972 Ko** de pic RSS (126 Mio ; 167,6 Mio pour le CLI),
> **14 795 890 octets** de JSON indenté, **54 522 étiquettes**, **2 726 syntagmes**.
> Sur **100 phrases courtes** (661 mots, médiane 6 mots) : **1,10 ms/appel** pour la
> fonction, **1,18 ms** de coût fixe, **191,6 ms/appel** pour le CLI (démarrage compris),
> et **0,369 s** pour les 100 en un seul `--jsonl` (×52,6 vs 100 CLI). Avec `--tagger` et
> un cache **froid** : **110,2 s** pour 92 appels, **14 677 tokens**, **1,17 s/phrase**,
> soit **×299** le lot heuristique ; l'extrapolation aux 10 000 mots donne **797 appels**,
> **236 215 tokens** et **~954 s** (~16 min).
>
> **Dispositif** : [`tools/banc_performance.py`](../tools/banc_performance.py),
> [`reports/performance.json`](performance.json),
> [`reports/performance-profil.json`](performance-profil.json), machine à 40 cœurs
> (Xeon E5-2687W v3, 125 Go), Python 3.13.16, `PYTHONHASHSEED=0`, mesures froides
> répétées 3 fois (médiane), mémoire par `/usr/bin/time -f %M`.

## 1. Ce que le banc mesure

Le banc est **hors ligne par défaut** et n'importe que la bibliothèque standard. Il mesure
trois choses distinctes, qu'il ne faut pas confondre :

1. **la fonction** `Heuristique.analyser` seule, dans un sous-processus neuf : le temps est
   pris autour de l'appel, après une analyse de chauffe qui compile les expressions
   régulières ; c'est le temps de l'analyse, sans le démarrage du CLI ;
2. **le CLI** `python3 tools/drave.py analyser --fichier … --json` : temps mural complet,
   démarrage de Python, import, analyse, sérialisation JSON et écriture sur le tube ;
3. **le tagger** `--tagger --jsonl`, avec `DEEPSEEK_CACHE` dans un répertoire temporaire
   **froid** : le coût réseau est lu dans la ligne `TAGGER API` (appels, requêtes, cache,
   tokens, latence), pas estimé.

Un « mot » est un token de type `mot` ou `nombre` selon `Heuristique._mots` ; le préfixe de
10 000 mots est **exactement** le texte qui s'arrête à la fin du 10 000e token, pas une
coupe au caractère. Le JSON mesuré est celui du CLI, **indenté** (`indent=1`) ; le JSONL du
tagger est **compact**, donc plus petit à contenu égal. Le JSONL heuristique, lui, change le
découpage (une phrase à la fois) et peut être **plus gros** que le JSON global : voir § 2.

## 2. Les 10 000 mots

| mesure | valeur |
|---|---:|
| temps de la fonction `analyser` | **4,012 s** (3,926–4,396 ; 3 répétitions) |
| temps mural du CLI `--json` | **4,965 s** (4,958–5,043) |
| sérialisation JSON seule | **0,672 s** |
| démarrage + écriture du CLI | **~0,28 s** |
| débit (fonction) | **2 493 mots/s** |
| débit (CLI) | **2 014 mots/s** |
| pic RSS (fonction) | **128 972 Ko = 125,9 Mio** |
| pic RSS (CLI) | **171 656 Ko = 167,6 Mio** |
| taille du JSON indenté | **14 795 890 octets = 14,8 Mo** (1 480 octets/mot) |
| étiquettes | **54 522** (5,45 par mot) |
| syntagmes | **2 726** |
| unités sémantiques | **4 701** |
| phrases | **814** |
| JSONL compact (même texte) | **17 693 596 octets**, 3,086 s |

Le CLI paie **0,95 s** de plus que la fonction : 0,67 s de `json.dumps(indent=1)`, ~0,15 s
de démarrage et d'import, le reste en écriture de 14,8 Mo. Le JSONL compact est **plus gros**
(17,7 Mo) que le JSON global (14,8 Mo) parce qu'il analyse chaque phrase séparément : le
générateur S ne voit plus le texte entier et produit davantage de syntagmes locaux. C'est
un effet de **découpage**, pas de format.

## 3. Les 100 phrases courtes — le coût fixe

Les 100 phrases sont réelles, tirées du même préfixe, de 3 à 12 mots, une seule phrase
chacune ; elles totalisent **661 mots** (médiane **6 mots**). Le lot `--jsonl` en segmente
**94** (le découpage fusionne six lignes), et le tagger fait **92 appels** (deux phrases
sont servies sans appel réseau).

| mesure | valeur |
|---|---:|
| 100 appels **fonction** séparés | **1,10 ms/appel** (médiane ; p95 2,14 ms ; 0,116 s pour 100) |
| coût fixe ajusté `t = a + b·mots` | **a = 1,18 ms** · b = 0,00 ms/mot |
| 100 appels **CLI** séparés | **191,6 ms/appel** (médiane ; p95 219,8 ms ; 19,43 s pour 100) |
| pic RSS d'un appel CLI | **31 938 Ko = 31,2 Mio** (médiane) |
| JSON par phrase (moyenne) | **14 244 octets** (médiane 12 613) |
| un seul `--jsonl` pour les 100 | **0,369 s**, soit **3,69 ms/phrase** |
| accélération du lot vs 100 CLI | **×52,6** |

Le **coût fixe de la fonction est ~1,1 ms** ; la pente par mot est négligeable sur cette
plage de 3–12 mots. Le **coût fixe du CLI est ~190 ms**, presque entièrement le démarrage
de Python et l'import du bloc : c'est pourquoi un lot `--jsonl` est **52 fois** plus rapide
que 100 invocations. Pour un corpus, le CLI par phrase est un mauvais choix ; le lot ou
l'appel de la fonction sont les bons.

## 4. `--tagger` — le coût réseau

Mesure sur le même lot de 100 phrases, **cache froid** (`DEEPSEEK_CACHE` temporaire) :

| mesure | valeur |
|---|---:|
| durée du CLI `--tagger --jsonl` | **110,204 s** |
| appels / requêtes réseau | **92 / 92** (cache 0) |
| tokens | **14 677** (159,5 tokens/appel) |
| latence réseau cumulée | **109,1 s** |
| temps par phrase | **1,17 s** |
| pic RSS | **34 308 Ko = 33,5 Mio** |
| JSONL | **1 116 929 octets** (94 lignes) |
| comparaison au lot heuristique | **×299** (110,204 s contre 0,369 s) |

Le réseau porte **109,1 s sur 110,2 s** : le tagger est un **coût de latence**, pas un coût
de calcul. Le nombre de tokens par appel est modeste (159,5), mais chaque phrase attend son
aller-retour. **Extrapolation** aux 10 000 mots (814 phrases, longueur moyenne 12,3 mots
contre 7,0 pour le lot, rapport **1,86**) :

| extrapolation 10 000 mots | valeur |
|---|---:|
| appels estimés | **797** |
| tokens estimés | **236 215** |
| durée estimée | **954 s ≈ 15,9 min** |
| réseau estimé | **945 s** |
| comparaison à la fonction heuristique (4,012 s) | **×238** |

C'est une **estimation**, pas une mesure : le champ `mesure: false` du JSON le dit. Elle
suppose la même distribution de phrases, corrigée du rapport de longueur ; un cache chaud
diviserait le temps et les tokens par presque le nombre d'appels. Au taux de W3
(0,031 $ pour 143 870 tokens), 236 215 tokens valent **~0,05 $** — le coût monétaire est
négligeable, le coût **temps** ne l'est pas.

## 5. Le contrôle négatif de linéarité — et pourquoi il échoue

### 5.1 Les préfixes réels sont confondus par le contenu

Les préfixes du même texte ne permettent **pas** de conclure : le nombre de syntagmes n'est
pas proportionnel aux mots, et le temps suit les syntagmes.

| mots | syntagmes | temps (s) | mots/s |
|---:|---:|---:|---:|
| 250 | 126 | 0,047 | 5 300 |
| 500 | 262 | 0,122 | 4 097 |
| 1 000 | 496 | 0,306 | 3 270 |
| 2 000 | 1 006 | 0,981 | 2 039 |
| 4 000 | 1 075 | **0,758** | 5 276 |
| 8 000 | 2 192 | 2,689 | 2 975 |
| 10 000 | 2 726 | 3,994 | 2 504 |

Le point **4 000 mots est plus rapide que le point 2 000** : il ne contient que **1 075**
syntagmes contre **1 006** — la segmentation globale du générateur S change avec le texte.
La pente log-log des préfixes vaut **α = 1,13**, mais elle mélange la taille et le contenu ;
ce n'est pas un test de complexité.

### 5.2 Le bloc contrôlé isole la taille

On prend un bloc de **247 mots** (phrases entières) et on le répète 1, 2, 4, 8, 16, 32 et
40 fois : la distribution du texte est **constante**, seule la taille change. Le nombre de
syntagmes croît alors **exactement** avec la taille (124, 248, 496, 992, 1 984, 3 968,
4 960).

| mots | syntagmes | temps (s) | rapport au précédent | attendu linéaire | attendu quadratique |
|---:|---:|---:|---:|---:|---:|
| 247 | 124 | 0,046 | — | — | — |
| 494 | 248 | 0,105 | **2,29** | 2 | 4 |
| 988 | 496 | 0,308 | **2,94** | 2 | 4 |
| 1 976 | 992 | 0,789 | **2,56** | 2 | 4 |
| 3 952 | 1 984 | 2,393 | **3,03** | 2 | 4 |
| 7 904 | 3 968 | 8,904 | **3,72** | 2 | 4 |
| 9 880 | 4 960 | 13,701 | 1,54 (×1,25 mot) | 1,25 | 1,56 |

Les rapports de doublement **s'éloignent de 2 et se rapprochent de 4** à mesure que la
taille augmente (2,29 → 2,94 → 2,56 → 3,03 → 3,72). Le dernier point n'est pas un
doublement (×1,25) : il vaut 1,54, soit presque le **1,56** attendu d'un quadratique.

Les ajustements sur les 7 points :

| modèle | R² | RMSE | coefficient |
|---|---:|---:|---:|
| `t = a + b·n` | 0,957 | 1,032 s | b = 1,377·10⁻³ s/mot |
| `t = a + b·n + c·n²` | **0,99995** | **0,036 s** | **c = 1,313·10⁻⁷ s/mot²** |
| `log t = α·log n + β` | 0,995 | 0,140 | **α = 1,552** |

Le terme quadratique ajoute **+0,043 de R²** et divise le RMSE par **29** : le linéaire est
rejeté, le quadratique est retenu. **Le contrôle négatif demandé échoue.**

### 5.3 Le contrôle de l'instrument

Le banc vérifie que la pente log-log **sait** distinguer 1 de 2 : une boucle Python
volontairement linéaire (`n × 200` additions) et une boucle volontairement quadratique
(`n²` additions) sont mesurées sur les mêmes tailles.

| charge | α mesuré | R² | attendu |
|---|---:|---:|---:|
| boucle linéaire | **0,9998** | 0,970 | 1 |
| boucle quadratique | **2,0045** | 0,99986 | 2 |

L'instrument retrouve **1,00** et **2,00** : l'échec du § 5.2 n'est pas un artefact de
l'ajustement. C'est bien `analyser` qui est superlinéaire.

## 6. Le coupable — le profil du bloc ×16

`cProfile` sur le bloc ×16 (3 952 mots, 1 984 syntagmes) donne **48,6 s profilées** pour
**2,393 s** réelles (le profileur multiplie les appels Python par ~20 ; les **parts
relatives** sont le signal, pas les secondes) :

| fonction | appels | temps cumulé profilé | part |
|---|---:|---:|---:|
| `analyser` | 1 | 48,588 s | 100 % |
| `_cible_proche` | 1 040 | **14,474 s** | 30 % |
| `_expliciter_partition` | 1 | **14,330 s** | 29 % |
| `_est_adverbe_seul` | **768 048** | **11,606 s** | 24 % |
| `_groupes_partition` | 1 | **11,162 s** | 23 % |
| `_sujet_hors_gv` | 1 | 5,964 s | 12 % |
| `_verbes_proches` | 1 984 | 3,170 s | 7 % |
| `deepcopy` | 171 610 | 3,019 s | 6 % |

Deux boucles expliquent la croissance :

1. **`_groupes_partition`** ([`bloc_linguistique.py:2518`](../tools/bloc_linguistique.py))
   compare **toutes les paires** de syntagmes pour trouver les composantes connexes de
   chevauchement : O(k²) en nombre de syntagmes k. À k = 1 984, cela fait ~2 M de paires ;
   à k = 4 960 (bloc ×40), ~12,3 M. C'est la part qui double le plus vite.
2. **`_cible_proche`** ([`bloc_linguistique.py:1273`](../tools/bloc_linguistique.py))
   filtre **tous** les GV pour chaque segment (`_est_adverbe_seul`, 768 048 appels) puis
   les **trie** par distance (`sorted`) : O(k·m log m) par analyse. `_verbes_proches` fait
   le même tri pour les candidats.

Le nombre de **syntagmes**, pas le nombre de mots, est la variable qui pilote le temps.
C'est pourquoi le texte réel de 10 000 mots (2 726 syntagmes) prend 4,0 s, tandis que le
bloc répété de 9 880 mots (4 960 syntagmes) en prend 13,7 s.

## 7. Ce qui est exploitable, et ce qui ne l'est pas

**Exploitable aujourd'hui.**

- **10 000 mots en 4,0 s** (fonction) / **5,0 s** (CLI), **2 493 / 2 014 mots/s**, **126 Mio**
  de pic RSS, **14,8 Mo** de JSON : c'est un traitement par lots confortable sur une
  machine à 40 cœurs, sans GPU.
- **100 phrases courtes en 1,1 ms** par appel de fonction ; le lot `--jsonl` fait **0,37 s**
  pour 100, soit **52 fois** moins que 100 CLI séparés. Pour un corpus, utiliser le lot.
- **`--tagger`** : **1,2 s** et **160 tokens** par phrase, **~16 min** pour 10 000 mots.
  Le réseau porte **99 %** du temps ; le coût monétaire est ~0,05 $. À réserver au
  traitement par lots avec cache, pas à l'interactif.

**La limite.** Le temps croît **superlinéairement** avec le nombre de syntagmes. Le
contrôle de linéarité **échoue** : à densité constante, α = **1,55** et le modèle
quadratique est le bon. Pour un document de **100 000 mots**, l'extrapolation va de **~40 s**
(linéaire) à **~7 min** (quadratique observée) ; le chiffre exact dépend de la densité de
syntagmes. Au-delà de ~10 000 mots, découper le document (`--jsonl` par phrase, ou appels
de la fonction par paragraphe) est la parade immédiate.

**La prochaine action.** Remplacer `_groupes_partition` par un **balayage** des intervalles
triés par début (O(k log k), même découpage) et précalculer les GV utiles une fois pour
`_cible_proche` (index spatial ou balayage, au lieu du tri de tous les GV par segment).
Puis re-mesurer le même bloc et le même texte. Le profil est dans
[`performance-profil.json`](performance-profil.json).

## 8. Ce qui pourrait rendre ces chiffres faux

- **Un seul texte** : le préfixe est un texte littéraire français (Alice) ; un texte
  technique, juridique ou multilingue peut changer la densité de syntagmes, donc le temps.
- **Le bloc répété n'est pas le texte réel** : il mesure la croissance à densité constante.
  Le texte réel de 10 000 mots a une densité plus faible (2 726 syntagmes, 0,27/mot) que
  le bloc (0,50/mot) ; c'est pourquoi il est plus rapide. Le contrôle teste la **complexité
  de l'algorithme**, pas la vitesse du texte réel.
- **Le profil** : `cProfile` gonfle les appels Python (~20×) ; les parts sont fiables, les
  secondes ne sont pas des temps muraux.
- **Le tagger** : 92 appels, une seule mesure, un cache froid, une latence réseau variable ;
  l'extrapolation à 10 000 mots n'est **pas** mesurée. Le cache chaud change tout.
- **La machine** : 40 cœurs partagés, pas d'épinglage CPU ; les médianes de 3 répétitions
  donnent la dispersion (min–max dans le JSON), pas une garantie temps réel.
- **Le JSON** : la taille est celle du JSON **indenté** ; le JSONL compact du tagger n'est
  pas comparable octet pour octet. Le JSONL heuristique de 10 000 mots est même plus gros
  (17,7 Mo) parce qu'il découpe par phrase.
- **Les 100 phrases** : elles viennent du début du texte (surtout des phrases courtes) ;
  une autre sélection changerait le coût fixe de quelques dixièmes de ms.

## 9. Reproduire

```bash
# le passage publié ici : hors ligne, puis réseau sur 100 phrases
python3 tools/banc_performance.py --repetitions 3 \
  --source reports/performance-corpus-10000.txt --mots 10000 \
  --sortie reports/performance.json
python3 tools/banc_performance.py --tagger-seulement --avec-tagger \
  --sortie reports/performance.json

# le passage complet, réseau compris (le tagger des 10 000 mots est long, ~16 min)
python3 tools/banc_performance.py --avec-tagger --tagger-complet

# le passage rapide, hors ligne (3 tailles, 1 répétition, sans tagger)
python3 tools/banc_performance.py --rapide

# le profil du bloc ×16 (le banc écrit ce fichier dans work/banc-performance/)
python3 tools/banc_performance.py --profil work/banc-performance/bloc-x16.txt \
  --sortie reports/performance-profil.json
```

Le banc écrit [`reports/performance.json`](performance.json) (mesures brutes, ajustements,
verdict) et, avec `--rapport`, une fiche markdown. Le profil est
[`reports/performance-profil.json`](performance-profil.json).

**Les fichiers du résultat** : [`tools/banc_performance.py`](../tools/banc_performance.py) ·
[`reports/performance.json`](performance.json) ·
[`reports/performance-profil.json`](performance-profil.json) ·
[`reports/rapport-performance.md`](rapport-performance.md).
