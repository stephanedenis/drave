# U1 — les deux O(k²) sont bornés : 10 000 mots de **4,0 s à 0,82 s** (×4,9), α de **1,53 à 1,08**, sorties **identiques au bit près**

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **U1** (exploitable, suite de T4) ·
> **Date** : 2026-11-16 · **Verdict** : ✅ **le contrôle de linéarité passe** — α = **1,076**
> (objectif ≤ 1,15), le terme quadratique n'ajoute que **+0,00077 de R²** (contre +0,041
> avant), et **les sorties sont identiques** : 612 phrases du gold, 452 réelles, 10 000 mots,
> sept blocs contrôlés, **diff vide**. Le temps de la fonction sur 10 000 mots passe de
> **3,991 s à 0,816 s** (×4,9) ; la mémoire reste au même niveau (**127,4 Mio** contre
> **126,9 Mio**), le JSON est **octet pour octet** le même (14 795 890 octets).
>
> **Les deux points de T4.** `_groupes_partition` comparait **toutes les paires** de
> syntagmes (O(k²)) ; il balaie maintenant les intervalles triés par début (O(k log k)).
> `_cible_proche` filtrait puis **triait tous les GV** pour chaque segment ; un **index**
> rend les GV par distance croissante en O(log m + candidats examinés). Le profil a ensuite
> nommé trois autres boucles quadratiques, corrigées sans changer les résultats :
> `_sujet_hors_gv` (un `any()` sur tous les segments par GV), `_repli_cible_gp` /
> `_cible_rel_sujet` (parcours de tous les GN), et deux boucles du générateur S
> (`construire_arbre`, cibles de `_segmente`). Le `deepcopy` des candidats dans
> `_expliciter_partition` est remplacé par une copie superficielle.
>
> **Dispositif** : [`tools/banc_performance.py`](../tools/banc_performance.py),
> [`reports/performance-fix.json`](performance-fix.json),
> [`tools/verifier_performance_fix.py`](../tools/verifier_performance_fix.py) pour le
> contrôle négatif. Machine à 40 cœurs (Xeon E5-2687W v3, 125 Go), Python 3.13.16,
> `PYTHONHASHSEED=0`, mesures froides répétées 3 fois (médiane), mémoire par
> `/usr/bin/time -f %M`. Avant = commit **`83adaa2b`** (sous-module `389b99f`), après = commit
> **`d19f0fc7`** (sous-module `648adce`).

## 1. Le contrôle de linéarité avant/après

Même bloc contrôlé que T4 : **247 mots**, phrases entières, répété 1, 2, 4, 8, 16, 32 et 40
fois. La distribution du texte est constante ; seule la taille change. Les syntagmes
croissent exactement avec la taille (124, 248, 496, 992, 1 984, 3 968, 4 960).

| répétition | mots | syntagmes | temps avant (s) | temps après (s) | avant/après |
|---:|---:|---:|---:|---:|---:|
| ×1 | 247 | 124 | 0,050 | **0,032** | ×1,55 |
| ×2 | 494 | 248 | 0,113 | **0,078** | ×1,46 |
| ×4 | 988 | 496 | 0,300 | **0,144** | ×2,08 |
| ×8 | 1 976 | 992 | 0,828 | **0,308** | ×2,69 |
| ×16 | 3 952 | 1 984 | 2,461 | **0,618** | ×3,98 |
| ×32 | 7 904 | 3 968 | 8,863 | **1,478** | ×6,00 |
| ×40 | 9 880 | 4 960 | 13,691 | **1,777** | ×7,70 |

Les ajustements sur les sept points :

| modèle | avant R² | avant RMSE | avant coefficient | après R² | après RMSE | après coefficient |
|---|---:|---:|---|---:|---:|---|
| `t = a + b·n` | 0,9586 | 1,015 s | b = 1,373·10⁻³ s/mot | **0,9966** | **0,0383 s** | b = 1,850·10⁻⁴ s/mot |
| `t = a + b·n + c·n²` | 0,99993 | 0,0406 s | c = 1,292·10⁻⁷ s/mot² | 0,99739 | **0,0337 s** | c = **2,3·10⁻⁹ s/mot²** |
| `log t = α·log n + β` | 0,9947 | 0,144 | **α = 1,530** | **0,9985** | **0,0538** | **α = 1,076** |

Le terme quadratique n'apporte plus que **+0,00077 de R²** (contre **+0,0414** avant) : il
n'est **pas significatif** au critère du banc (< 0,02), et α = **1,076** est sous le seuil
**1,15**. Le contrôle de l'instrument n'a pas bougé : la boucle volontairement linéaire
donne α = 0,9998, la boucle volontairement quadratique α = 2,0045.

## 2. Les 10 000 mots

Sur le préfixe exact de 10 000 mots de `data/corpus_fr_litterature.txt` (sha256
`0069b20e…e08871`), même texte, même JSON :

| mesure | avant | après | écart |
|---|---:|---:|---:|
| fonction `Heuristique.analyser` | **3,991 s** | **0,816 s** | **×4,89** |
| débit (fonction) | 2 506 mots/s | **12 259 mots/s** | ×4,89 |
| CLI `--json` | 5,011 s | **1,668 s** | ×3,00 |
| sérialisation JSON seule | 0,628 s | 0,628 s | ×1,00 |
| pic RSS (fonction) | 129 936 Ko (126,9 Mio) | 130 452 Ko (**127,4 Mio**) | +0,5 Mio |
| pic RSS (CLI) | 171 316 Ko (167,3 Mio) | 171 864 Ko (167,8 Mio) | +0,5 Mio |
| JSON indenté | 14 795 890 octets | **14 795 890 octets** | **identique** |
| étiquettes / syntagmes | 54 522 / 2 726 | 54 522 / 2 726 | identique |

Le CLI ne gagne « que » ×3 parce que les **0,63 s de `json.dumps`** et le démarrage ne
baissent pas ; c'est la fonction qui porte le gain. La mémoire ne baisse pas : les index
ajoutent environ **0,5 Mio** (trois listes triées + un arbre de segments par liste de GV),
soit **+0,4 %** — le prix du temps linéaire.

## 3. Le gold 612 / 452 — mêmes chiffres, au bit près

Les annotations canoniques (JSON trié, sans durée) des **612** phrases et des **452** réelles
sont **identiques** avant/après. Les métriques le confirment :

| lecture | POS | F1 syntagmes | tête F1 | attachement top-1 | attachement top-k | exact sur span |
|---|---:|---:|---:|---:|---:|---:|
| 612 — avant | 0,8625 | 0,7902 | 0,9029 | 0,9958 | 0,9874 | 1,0 |
| 612 — après | **0,8625** | **0,7902** | **0,9029** | **0,9958** | **0,9874** | **1,0** |
| 452 — avant | 0,8891 | 0,7906 | 0,8990 | 0,9946 | 0,9891 | 1,0 |
| 452 — après | **0,8891** | **0,7906** | **0,8990** | **0,9946** | **0,9891** | **1,0** |

Le JSON complet d'`evaluer_gold.py` est identique **hors date** (sha256 canonique
`5bca5f76…bdebd8` avant et après) ; `ok=true` et le verdict sont inchangés.

## 4. Le contrôle négatif — le diff est vide

Le protocole : produire les annotations **canoniques** (JSON trié, `ensure_ascii=False`,
sans `duree_s`) avec l'ancien code puis avec le nouveau, et comparer **octet pour octet**.

| fichier | octets | sha256 (avant = après) |
|---|---:|---|
| `corpus-10000.json` | 16 457 228 | `16488a95ca0d63f478e971d866a05d90796d24085497641e4677ae6c51ef3094` |
| `bloc-x1.json` | 449 558 | `137cb8097696e49b52cc49041f96b9cdeb24d121654e4c08a6b13a9d0b268789` |
| `bloc-x2.json` | 901 533 | `dbbb1699cf09922a2288c721d0f095bd1c99ade7dae04629caf614e8fbe2dd3d` |
| `bloc-x4.json` | 1 805 483 | `8eba512f8ad72f6c6bc0b706665d21e27242645c5adfe50daa3368cf9c6e634e` |
| `bloc-x8.json` | 3 618 708 | `fa3f9e7d637686031c4ac7eeadd37fe23dbbf6fbaad29fe5aaccccd6427d76ca` |
| `bloc-x16.json` | 7 263 340 | `c3c34bfb1cd3b4b5442a14e7a13607ada5bf851fc417dd66728c155212974094` |
| `bloc-x32.json` | 14 552 604 | `06675c023dc93768056bce30ccc641e61772e6eb1bee1d2aaae982326e0dcfed` |
| `bloc-x40.json` | 18 197 238 | `28a412b9ae7d6a785ddd40cace5f2a652d387289b6955854a7ee99cfe48afe56` |
| `gold-annotations-612.json` | 4 281 465 | `b61c1521328bde4261ee42c1a0259d4c61cd05a9f12ec922a9256008c176c3dc` |
| `gold-annotations-452.json` | 3 222 340 | `de329b530ddafbca9908622b1869edb024207180b468352905e1678f713d7c87` |

`python3 tools/verifier_performance_fix.py --comparer AVANT APRES` rend
**`10/10 identiques — diff vide`** (code 0). En plus, le générateur S (sous-module
`tools/structures`) a été comparé directement sur **620 textes** (les 10 000 mots, les sept
blocs et les 612 phrases) : JSON canonique identique. Les hashes complets sont dans
[`reports/performance-fix.json`](performance-fix.json).

## 5. Ce qui a été changé

| fichier | fonction | avant | après |
|---|---|---|---|
| [`bloc_linguistique.py:2710`](../tools/bloc_linguistique.py) | `_groupes_partition` | toutes les paires de syntagmes, O(k²) | balayage des intervalles triés par début, O(k log k) |
| [`bloc_linguistique.py:524`](../tools/bloc_linguistique.py) | `_IndexGV` + `_cible_proche` / `_verbes_proches` | filtre de tous les GV puis tri par distance, par segment | index gauche/droite/chevauchement + tas, O(log m + candidats) |
| [`bloc_linguistique.py:1127`](../tools/bloc_linguistique.py) | `_sujet_hors_gv` | `any()` sur tous les segments pour chaque GV | fins de GN triées + `bisect`, O(k log k) |
| [`bloc_linguistique.py:655`](../tools/bloc_linguistique.py) | `_IndexFins` / `_repli_cible_gp` / `_cible_rel_sujet` | parcours de tous les GN à chaque appel | index par fin, O(log k) |
| [`bloc_linguistique.py:2745`](../tools/bloc_linguistique.py) | `_expliciter_partition` | `deepcopy` des candidats par alternative | copie superficielle (aucune mutation ensuite) |
| [`generateur.py:319`](../tools/structures/generateur.py) | `construire_arbre` | `reversed(segs[:k])` + `segs.index(parent)`, O(k²) | dernier segment à gauche entretenu, O(k) |
| [`generateur.py:345`](../tools/structures/generateur.py) | `_segmente` (cibles) | `reversed(segs[:k])` par segment, O(k²) | dernier GN / GP / GV entretenu, O(k) |

Les deux premiers points sont ceux de T4 ; les cinq suivants ont été nommés par le profil
**après** correction des deux premiers. Le profil final du bloc ×32 (24,5 s profilées) ne
montre plus aucune boucle quadratique : `_groupes_partition` **0,08 s**, `_cible_proche`
**0,5 s**, `_sujet_hors_gv` **0,9 s**, `_expliciter_partition` **0,3 s** ; le `deepcopy` des
candidats a disparu. Pour situer, T4 profilait `_groupes_partition` à **11,2 s**,
`_cible_proche` à **14,5 s** et `_est_adverbe_seul` à **11,6 s** sur le bloc ×16 : ces trois
postes ne sont plus dans le haut du profil. Le temps propre restant est dominé par
`_est_verbe` (4,6 s) et `_morphemes` (2,5 s), linéaires en mots.

## 6. Tests et portes

| commande | résultat |
|---|---|
| `python3 -m unittest tools.tests.linguistique.test_bloc_linguistique` | **25 tests OK** (dont 5 tests différentiels ancien/nouveau) |
| `PYTHONPATH=. python3 tests/test_generateur.py` (dans `tools/structures`) | **27 tests OK** (dont `TestArbreLineaire`) |
| `python3 -m unittest tools.tests.test_verifier_performance_fix` | **3 tests OK** (identique, un octet différent, fichier manquant) |
| `python3 tools/tests/linguistique/evaluer_gold.py --json …` | `ok=true`, verdict identique |
| `python3 tools/banc_performance.py --sortie … --repetitions 3` | α = 1,076, `controle_lineaire=true` |
| `python3 tools/verifier_performance_fix.py --comparer …` | `10/10 identiques — diff vide` |

Les portes sont lancées à la clôture ; les rouges tolérées sont celles de
[`docs/pilotage/references-non-regression.md`](../docs/pilotage/references-non-regression.md).

## 7. Ce qui pourrait rendre ces chiffres faux

- **Un seul texte** : le préfixe est un texte littéraire français (Alice). Un texte
  technique, juridique ou multilingue peut changer la densité de syntagmes, donc le temps.
- **Le bloc répété n'est pas le texte réel** : il isole la taille, pas le contenu ; il teste
  la complexité de l'algorithme, pas la vitesse d'un document quelconque.
- **La machine** : 40 cœurs partagés, sans épinglage CPU. Les médianes de 3 répétitions
  donnent la dispersion, pas une garantie temps réel ; les parts du profil sont le signal,
  pas les secondes.
- **La copie superficielle** de `_expliciter_partition` suppose qu'aucun code ne mute les
  candidats après la partition. C'est vrai aujourd'hui (vérifié sur 620 textes et le
  10 000 mots) ; une future mutation casserait l'invariant.
- **L'index des GV** départage les distances égales par l'ordre d'origine, comme le tri
  stable de Python. Les tests différentiels couvrent 500 tirages ; un changement de l'ordre
  de construction des listes de GV changerait les égalités, pas la partition.
- **Le sous-module** : `tools/structures` est un sous-module ; un clone public sans lui
  retombe sur le chunker simple (T3), et les sorties de cette fiche ne sont pas rejouables.

## 8. Reproduire

```bash
PYTHONHASHSEED=0 python3 tools/banc_performance.py \
  --sortie /tmp/performance-apres.json --repetitions 3

PYTHONHASHSEED=0 python3 tools/tests/linguistique/evaluer_gold.py \
  --json /tmp/gold-apres.json

PYTHONHASHSEED=0 python3 tools/verifier_performance_fix.py --sortie /tmp/u1-apres
python3 tools/verifier_performance_fix.py --comparer /tmp/u1-avant /tmp/u1-apres
```

Pour l'« avant », se placer sur `83adaa2b` avec le sous-module `389b99f` ; pour l'« après »,
sur `d19f0fc7` (sous-module `648adce`). Le JSON brut de la fiche est
[`reports/performance-fix.json`](performance-fix.json).

**Prochaine action** : **U2 — la roue** ; **U3 — `--profils`**. Le point quadratique est
fermé : le prochain document de 100 000 mots se teste maintenant sans la parade du
découpage, et la mémoire est le seul coût qui augmente (+0,5 Mio).
