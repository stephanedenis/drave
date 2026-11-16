# U3 — `drave profils` : la détection de langue des 398 profils UDHR, exposée

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **U3** (suite de T5) ·
> **Date** : 2026-11-16 · **Verdict** : ✅ **la détection est exposée** ; **20/20** langues
> et **20/20** scripts sur l'échantillon UDHR de 20 langues (article 15 tenu à l'écart),
> **313/320 = 0,9781** sur les articles 15–30, **433/447 = 0,9687** sur l'autotest complet
> 398 langues. Le texte ambigu bilingue rend **`und`** (0,0836 < 0,12), un mot isolé rend
> **`und`**, et les profils permutés tombent à **0/20** (0,0022 sur 447).
>
> **Le chiffre.** `drave profils --texte "Le chat dort."` rend **`fra`**, le script **`Latn`**
> et la confiance **0,3333** (source `lexique`, prior des mots-outils) ; un article 15 de
> l'UDHR rend la langue et le script par les **398 profils** (`source: profils`). La roue U2
> embarque l'artefact : **802 110 octets**, sha256 `33aee69d…`, et `drave profils` fonctionne
> **hors du dépôt**, depuis `/tmp`.
>
> **Dispositif** : [`tools/profils_udhr.py`](../tools/profils_udhr.py) (chargement, détection,
> prior court), [`tools/construire_profils_udhr.py`](../tools/construire_profils_udhr.py)
> (artefact reproductible), [`tools/mesurer_profils.py`](../tools/mesurer_profils.py) (la
> mesure), [`tools/tests/test_profils.py`](../tools/tests/test_profils.py) (**20 tests**),
> [`reports/profils.json`](profils.json), [`tools/drave.py`](../tools/drave.py),
[`tools/porte-produit.sh`](../tools/porte-produit.sh),
> [`docs/produit/README.md`](../docs/produit/README.md) § 3,
> [`docs/produit/demarrage.md`](../docs/produit/demarrage.md) § 3,
> [`docs/implantation/bloc-linguistique.md`](../docs/implantation/bloc-linguistique.md) § 8.

## 1. La question

Le bloc linguistique mesure la langue sur **398 langues UDHR** depuis R0.7, mais le CLI ne
l'exposait pas : `analyser` ne rendait que la langue détectée par le repli à sept langues, et
la **confiance** n'était publiée nulle part. U3 demande une commande qui rend, pour un texte
donné, la **langue probable**, le **script** et la **confiance**, avec une mesure sur les
**20 langues de l'échantillon UDHR** et un **contrôle négatif** sur un texte ambigu.

## 2. Ce que la commande fait

```bash
python3 tools/drave.py profils --texte "Le chat dort."
python3 tools/drave.py profils --texte "Привет мир" --json
python3 tools/drave.py profils --fichier article.txt --json
python3 tools/drave.py analyser "Le chat dort." --profils
```

```text
drave 0.1.0 — profils de langue (UDHR, hors ligne)
langue=fra script=Latn confiance=0.3333 source=lexique
langue      : fra (French)
script      : Latn
confiance   : 0.3333 (marge 0.0000, seuil 0.12)
source      : lexique
prior       : fra (mots-outils 0.3333)
candidats   : hns 0.6364 · lld 0.5455 · deu 0.4545 · oci 0.4545 · pcd 0.4545
profils     : 398 langues UDHR (articles 0–14, top 200)
```

Le JSON porte `schema: "drave.profils"`, `version: 1`, `texte`, `langue` (**décision**),
`langue_probable` (**premier profil**, même sous le seuil), `nom`, `script`, `confiance`,
`marge`, `source`, `seuil`, `sous_seuil`, `refus`, `prior`, `candidats` et les métadonnées
`profils` (398 langues, source, empreinte). **Sous le seuil 0,12, `langue` est `und`** ;
`langue_probable` et `confiance` restent publiées, pour que l'abstention soit lisible et non
un effacement.

**Deux chemins, et `source` le dit.** Sur un texte **long** (> 80 caractères), les 398 profils
de trigrammes. Sur un texte **court**, les profils se recouvrent (398 langues, quelques
trigrammes) : le **prior des mots-outils** des sept langues du bloc peut trancher
(`source: lexique`, `prior: {langue, score}`), et les `candidats` restent les profils — le
désaccord est visible, pas masqué. Un texte de **moins de cinq mots** qui passe par les profils est pénalisé
(confiance × mots / 5) pour qu'un mot isolé ne devienne pas une langue.

**Codes de sortie.** `0` succès, `3` refus (texte vide ou sans lettre/chiffre), `4` artefact
de profils absent ou illisible, `5` usage (`TEXTE` et `--texte` ensemble, seuil hors `[0,1]`,
fichier répertoire). Sans l'artefact, `stdout` reste vide, le message nomme le fichier et les
deux issues (réinstaller la roue, ou lancer le constructeur).

## 3. La mesure — les 20 langues de l'échantillon UDHR

L'échantillon est celui de [`rapport-corpus-commun.md`](rapport-corpus-commun.md) § 3 : **20
langues stratifiées** (5 familles × 4, 10 écritures), choisies pour l'égalité exacte de
l'article 1 des deux côtés. On garde le **fichier** exact (`udhr_cmn_hant.xml`,
`udhr_mly_arab.xml`, …), pas seulement l'ISO3, pour que la variante d'écriture soit celle de
l'échantillon. Les profils sont construits sur les articles **0–14** ; l'article **15** est
tenu à l'écart.

| langue | famille | script | détecté | confiance | source | ok |
|---|---|---|---:|---:|---|---|
| `eng` | Indo-European | Latn | eng | 0,4213 | profils | ✓ |
| `hin` | Indo-European | Deva | hin | 0,4853 | profils | ✓ |
| `bel` | Indo-European | Cyrl | bel | 0,5897 | profils | ✓ |
| `ell` | Indo-European | Grek | ell | 1,0000 | profils | ✓ |
| `kin` | Atlantic-Congo | Latn | kin | 0,4035 | profils | ✓ |
| `ewe` | Atlantic-Congo | Latn | ewe | 0,6366 | profils | ✓ |
| `ibo` | Atlantic-Congo | Latn | ibo | 0,7487 | profils | ✓ |
| `fuf` | Atlantic-Congo | Adlm | fuf | 1,0000 | profils | ✓ |
| `ind` | Austronesian | Latn | ind | 0,3812 | profils | ✓ |
| `tgl` | Austronesian | Latn | tgl | 0,3825 | profils | ✓ |
| `zlm` | Austronesian | Arab | zlm | 0,7171 | profils | ✓ |
| `jav` | Austronesian | Latn | jav | 0,3187 | profils | ✓ |
| `mya` | Sino-Tibetan | Mymr | mya | 0,8845 | profils | ✓ |
| `cmn` | Sino-Tibetan | Hant | cmn | 0,3257 | profils | ✓ |
| `cnh` | Sino-Tibetan | Latn | cnh | 0,3623 | profils | ✓ |
| `ctd` | Sino-Tibetan | Latn | ctd | 0,4867 | profils | ✓ |
| `arb` | Afro-Asiatic | Arab | arb | 0,8069 | profils | ✓ |
| `amh` | Afro-Asiatic | Ethi | amh | 1,0000 | profils | ✓ |
| `heb` | Afro-Asiatic | Hebr | heb | 0,9412 | profils | ✓ |
| `hau` | Afro-Asiatic | Latn | hau | 0,6177 | profils | ✓ |

| mesure | résultat |
|---|---:|
| **langue, article 15** | **20/20 = 1,0000** |
| **décision (`und` sous le seuil)** | **20/20** |
| **script, article 15** | **20/20** (dont `Hani` accepté pour `Hant`) |
| confiance moyenne / min / max | **0,6255 / 0,3187 / 1,0000** |
| **langue, articles 15–30** | **313/320 = 0,9781** |
| **script, articles 15–30** | **320/320 = 1,0000** |

Le **20/20** de l'article 15 est une mesure sur un échantillon **stratifié**, pas aléatoire :
il prouve que la commande retrouve la langue et le script sur ces 20 textes tenus à l'écart, il
ne dit pas que les 398 langues font 100 %. L'autotest complet le dit :

| mesure (398 langues, article 15, 447 textes) | résultat |
|---|---:|
| profils bruts (l'autotest R0.7) | **433/447 = 0,9687** |
| chemin CLI (profils + prior court) | **431/447 = 0,9642** |
| script | **447/447 = 1,0000** |
| **profils permutés** | **1/447 = 0,0022** |

Le chemin CLI perd **2 textes** sur 447 par rapport aux profils bruts, et en gagne sur les
phrases courtes : c'est le prix du prior (`lexique` sur 2 textes de l'autotest). Le chiffre de
référence de la détection longue reste **0,9687** ; le CLI ne le maquille pas.

## 4. Les contrôles négatifs

1. **Le texte ambigu bilingue** — « All human beings are born free and equal in dignity and
   rights. Tous les êtres humains naissent libres et égaux en dignité et en droits. » — rend
   **`und`**, `langue_probable: eng`, confiance **0,0836 < 0,12**. C'est le contrôle demandé :
   deux langues à parts égales ne donnent pas un verdict ; le détecteur s'abstient.
2. **Le mot isolé** — `chat` — rend **`und`** (confiance 0,04, `langue_probable: agr`) : la
   pénalité des textes très courts empêche un trigramme de faire une langue.
3. **Le texte vide** — rend `und` + `refus: "vide"`, code **3** : c'est un refus, pas une
   annotation.
4. **Les profils permutés** — les étiquettes de langue sont décalées d'un cran : **0/20** sur
   l'échantillon, **1/447 = 0,0022** sur l'autotest. Le détecteur ne trouve pas la bonne
   langue par hasard.
5. **La roue sans l'artefact** — `DRAVE_PROFILS` pointe un fichier absent : code **4**,
   `stdout` vide, message qui nomme le fichier et les deux issues ; `analyser --profils` suit
   le même chemin. La roue **installée**, artefact retiré de `site-packages`, sort aussi **4**
   depuis `/tmp` (vérifié). C'est le contrôle négatif de l'empaquetage, comme la roue sans gold
   en U2.

## 5. Ce que ça prouve, ce que ça ne prouve pas

**Prouvé.** La détection de langue du bloc est **exposable** : 398 profils versionnés, une
commande, un JSON stable, un script, une confiance, une abstention `und` lisible, un prior
court explicite, et une mesure reproductible sur 20 langues puis sur 398. L'artefact est
**identique** aux profils reconstruits depuis le corpus (0 différence sur 398, empreinte de
source `e31851d5…`), il voyage dans la roue (802 110 octets, sha256 `33aee69d…`), et la
commande installée fonctionne depuis `/tmp`.

**Non prouvé.** Le **20/20 n'est pas une précision de déploiement** : l'UDHR est parallèle et
propre, l'échantillon est stratifié et choisi pour la diversité des écritures, et les textes
sont des articles de 1948. Sur les articles 15–30, la même échantillon tombe à **0,9781** ;
sur les 398 langues, **0,9642** (CLI) / **0,9687** (brut). La confiance n'est **pas calibrée** :
c'est une marge entre profils, pas une probabilité. Les langues proches restent le point
faible (chinois mandarin et jinyu, anglais et scots) ; le texte court hors des sept langues à
mots-outils peut rester `und`.

## 6. Ce qui pourrait rendre ce résultat faux

- **L'échantillon est stratifié, pas aléatoire** : 5 familles sur 51, 10 écritures, 20 textes ;
  un autre tirage donnerait un autre chiffre. Le 20/20 ne se transporte pas.
- **L'article 15 est un seul article par langue** (20 textes) : c'est peu. Les articles 15–30
  (320 textes) sont là pour montrer l'écart (0,9781) ; ils ne remplacent pas une campagne
  multi-domaines.
- **Le prior court est un arbitrage** : il corrige « Le chat dort. » et les phrases d'exemple,
  mais il coûte 2 textes sur 447 à l'autotest et ne couvre que sept langues. Le champ
  `source` le rend visible ; il ne faudrait pas le lire comme un modèle.
- **La confiance n'est pas calibrée** : deux textes de même confiance ne sont pas deux
  probabilités égales. La calibration est un travail séparé.
- **Les profils sont des données du corpus** : si `data/udhr/articles.jsonl` change, l'artefact
  doit être reconstruit. `construire_profils_udhr.py --verifier` le dit (code 1 si dérive).
- **La roue n'est pas minimale** : l'artefact ajoute ~0,33 Mo compressés à la roue U2
  (2 055 192 octets contre 1 727 201). C'est assumé : la détection doit marcher hors dépôt.
- **`--profils` est une option** : elle charge l'artefact (~800 Ko) et score 398 profils par
  phrase ; le défaut sans l'option garde le repli à sept langues, plus léger.

## 7. Les fichiers

| fichier | changement |
|---|---|
| `tools/profils_udhr.py` | chargement de l'artefact, `detecter`, prior court, `formater`, `ProfilsAbsents` |
| `tools/construire_profils_udhr.py` | construction déterministe des 398 profils + `--verifier` |
| `tools/mesurer_profils.py` | la mesure (20 langues, 398, permuté, contrôles, CLI) |
| `tools/tests/test_profils.py` | 20 tests : CLI, JSON, sortie compacte, ambigu, mot isolé, mot-outil isolé, vide, absent, 20 langues, permuté |
| `tools/tests/test_produit.py` | l'aide et les cinq sous-commandes incluent `profils` |
| `tools/tests/test_empaquetage.py` | `profils_udhr.json` dans les `package-data` |
| `tools/drave.py` | `profils --texte` ; `analyser --profils` ; `_HeuristiqueProfils` ; code 4 |
| `tools/porte-bloc-linguistique.sh` | tests `profils` + vérification de l'artefact |
| `tools/porte-produit.sh` | le cas `profils` (langue, script, confiance, 398 profils) dans la porte produit |
| `pyproject.toml` | `profils_udhr.json` dans la roue |
| `tools/tests/linguistique/profils_udhr.json` | l'artefact (398 langues, 802 110 octets) |
| `reports/profils.json` | la mesure reproductible |
| `docs/produit/README.md` § 3 | la commande, le JSON, les codes, la mesure |
| `docs/produit/demarrage.md` § 3 | `drave profils` dans les commandes |
| `docs/implantation/bloc-linguistique.md` § 8 | le renvoi vers la commande et la fiche |

**Verdict.** U3 est **livré** : la détection de langue des 398 profils UDHR est dans le CLI,
avec la langue probable, le script, la confiance et une abstention `und` explicite ; la mesure
sur les 20 langues de l'échantillon est **20/20** (article 15) et **0,9781** (articles 15–30),
le contrôle ambigu rend **`und`**, et les profils permutés tombent à **0/20**. La roue embarque
l'artefact et la commande fonctionne hors du dépôt. Les limites sont nommées : échantillon
stratifié, confiance non calibrée, prior court à sept langues, et **0,9642** sur les 398
textes du chemin CLI.
