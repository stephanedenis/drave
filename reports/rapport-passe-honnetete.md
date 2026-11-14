# Passe d'honnêteté — 19 fiches portent « instantané historique », les quatre chiffres dépassés ne se lisent plus comme l'état courant

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J9.1 · **Date** : 2026-11-14 ·
> **Verdict** : ✅
>
> **Ce que la passe fait.** Les fiches qui publient l'instantané **POS 85 / F1 0,7535 / 236/237 /
> 2 spans** portent désormais un encart **« instantané historique »** qui ne recopie **aucune
> valeur** : il renvoie à [`en-cours`](../docs/pilotage/en-cours.md) et à
> [`la roadmap`](../docs/pilotage/roadmap.md). Dix encarts qui copiaient un état devenu faux sont
> réécrits ; neuf sont ajoutés.
>
> **Le chiffre.** **19/19** fiches annotées, **19/19** encarts en ligne 3, **38/38** liens qui
> résolvent. Après la passe, **0 fiche de résultats** ne publie un des quatre marqueurs sans
> mention, hors **2 faux positifs nommés** (`2 spans` de phrase, autre unité) et les index.
>
> **État courant, mesuré à HEAD `229098ec`** (J8.1 ; le produit n'a pas bougé depuis `b6e474dc`,
> `s065`) : gold vivant **612** phrases, **POS 0,8625**, **F1 0,7902**, **attachement 238/238
> labels (238/239 cibles, 0,9958)**, **1 span sans label (`g017`)** ; gold gelé **602** : F1
> **0,7882**, attachement **234 labels sur 239 cibles**. La commande est en § 4.
>
> **Dispositif** : scan lexical des 723 fiches de `reports/`, annotation des 19, contrôle des
> liens et re-mesure du gold. JSON : [`passe-honnetete.json`](passe-honnetete.json).

## 1. Le problème, en une table

Le produit a avancé après les fiches de la semaine : `r035` (07/11), la convention des GV (07/11),
puis `s065` (14/11) ont déplacé l'attachement et la F1. Les fiches antérieures restent vraies
**pour leur commit**, mais leurs chiffres ne sont plus l'état courant.

| mesure | instantané publié (06/11) | **état courant (14/11, HEAD `229098ec`)** | écart |
|---|---:|---:|---:|
| POS (gold vivant 612) | **84,96 – 85,75 %** | **86,25 %** | **+0,50 à +1,29 pt** |
| F1 syntagmes (vivant 612) | **0,7535** | **0,7902** | **+0,0367** |
| F1 syntagmes (gelé 602) | — | **0,7882** | — |
| attachement exact / labels | **236/237** (0,9916) | **238/238** (238/239 cibles, 0,9958) | **+2 / +1** |
| spans sans label | **2** (`r035`, `g017`) | **1** (`g017`) | **−1** |

**Pourquoi ces chiffres ont bougé.** `r035` a réglé la relative zéro (236 → 237) ; la convention
des GV a fait monter la F1 de 0,7549 à 0,7902 ; `s065` a attaché la REL « qui commence » au sujet
du GV qui la suit (237/238 → 238/238). `g017` reste le seul span sans label : ce n'est pas une
cible fausse, c'est une convention d'adverbe à trancher.

## 2. La règle appliquée

**Est « concernée »** une fiche de `reports/` qui publie, dans son titre, son résumé ou une
mesure, un des quatre marqueurs de l'instantané **comme son état ou comme l'état du produit** :

- `POS 85` (84,96 / 85,00 / 85,34 / 85,75) ;
- `F1 0,7535` ;
- `236/237` (couverture 0,9916) ;
- `2 spans` restants.

**L'encart** est un bloc de trois lignes, placé en ligne 3, juste après le titre :

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

**Il ne copie plus les valeurs courantes.** L'ancien encart des dix fiches disait
« l'état courant est … (POS 86,25 %, F1 0,7535, 236/237, 2 spans) » : en recopiant l'état, il
**devenait faux à son tour** quand `s065` a bougé l'attachement. Le lien, lui, ne périme pas.
C'est la leçon de la passe : un instantané historique **pointe**, il ne réplique pas.

## 3. L'inventaire — 19 fiches

**A. La cohorte de l'instantané (14 fiches).** Dix portaient déjà un encart (avec les valeurs
recopiées) ; quatre n'en portaient pas.

| fiche | marqueur(s) publié(s) | action | preuve |
|---|---|---|---|
| [`rapport-autotest-parallele.md`](rapport-autotest-parallele.md) | encart : F1 0,7535, 236/237, 2 spans | encart réécrit | ligne 3 |
| [`rapport-composition-sans-perte.md`](rapport-composition-sans-perte.md) | encart : F1 0,7535, 236/237, 2 spans | encart réécrit | ligne 3 |
| [`rapport-frontieres-integrees.md`](rapport-frontieres-integrees.md) | encart : F1 0,7535, 236/237, 2 spans | encart réécrit | ligne 3 |
| [`rapport-morphologie-verbes.md`](rapport-morphologie-verbes.md) | encart : F1 0,7535, 236/237, 2 spans | encart réécrit | ligne 3 |
| [`rapport-partition-integree.md`](rapport-partition-integree.md) | POS 85,00 ; F1 0,7535 ; 236/237 ; 2 spans | encart réécrit | ligne 3 |
| [`rapport-pos-anglais-v2.md`](rapport-pos-anglais-v2.md) | encart : F1 0,7535, 236/237, 2 spans | encart réécrit | ligne 3 |
| [`rapport-pos-nombres.md`](rapport-pos-nombres.md) | POS 85,00 ; F1 0,7535 ; 236/237 ; 2 spans | encart réécrit | ligne 3 |
| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | POS 84,96 ; F1 0,7535 ; 236/237 ; 2 spans | encart réécrit | ligne 3 |
| [`rapport-produit-v0.md`](rapport-produit-v0.md) | encart : F1 0,7535, 236/237, 2 spans | encart réécrit | ligne 3 |
| [`rapport-schema-v1.md`](rapport-schema-v1.md) | encart : F1 0,7535, 236/237, 2 spans | encart réécrit | ligne 3 |
| [`rapport-gn-pronom-sujet.md`](rapport-gn-pronom-sujet.md) | F1 0,7535 ; 236/237 | encart ajouté | ligne 3 |
| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | POS 85,75 ; 235/236 | encart ajouté | ligne 3 |
| [`rapport-pos-r4.md`](rapport-pos-r4.md) | POS 85,00 ; POS 85,34 ; 222/222 | encart ajouté | ligne 3 |
| [`rapport-r264-elision.md`](rapport-r264-elision.md) | 236/237 ; 2 spans | encart ajouté | ligne 3 |

**B. Les héritiers immédiats (5 fiches).** Ils publient un état **postérieur** à l'instantané
(226/226, 237/238 ou 236/237 conditionnel), que `s065` a dépassé à son tour. L'encart évite une
seconde lecture périmée.

| fiche | marqueur(s) publié(s) | action | preuve |
|---|---|---|---|
| [`rapport-gold-gp-corrige.md`](rapport-gold-gp-corrige.md) | 226/226 ; 13 spans | encart ajouté | ligne 3 |
| [`rapport-convention-gv.md`](rapport-convention-gv.md) | 236/237 (avant) ; 237/238 (arrivée) | encart ajouté | ligne 3 |
| [`rapport-g017.md`](rapport-g017.md) | 236/237 (contrefactuel) ; 2 spans | encart ajouté | ligne 3 |
| [`rapport-r035.md`](rapport-r035.md) | 236/237 (avant) ; 237/238 (arrivée) | encart ajouté | ligne 3 |
| [`rapport-semaine.md`](rapport-semaine.md) | 236/237 (bilan) ; 2 spans (plan) | encart ajouté | ligne 3 |

## 4. Les contrôles

**Contrôle positif — les 19 encarts.** `19/19` fiches portent exactement le bloc en ligne 3 ;
`19/19` contiennent les deux liens ; `38/38` cibles résolvent (`../docs/pilotage/en-cours.md` et
`../docs/pilotage/roadmap.md` existent). Aucun encart ne contient encore
`F1 0,7535, attachement 236/237` : l'ancien texte a bien disparu.

**Contrôle négatif 1 — la fiche courante n'est pas annotée.** [`rapport-s065.md`](rapport-s065.md)
publie **238/238** et **0 POS changée** : elle ne porte pas l'encart et ne doit pas le porter.
C'est la frontière entre « historique » et « courant ».

**Contrôle négatif 2 — les faux positifs du scan.** Le motif `2 spans` attrape deux fiches qui
parlent d'une **autre unité** : [`rapport-frontieres-phrase.md`](rapport-frontieres-phrase.md)
(« 2 spans **de phrase** du gold corrigés ») et
[`rapport-gold-anglais.md`](rapport-gold-anglais.md) (« 2 spans exacts » du gold anglais). Elles
ne sont **pas** annotées : leur `2 spans` n'est pas l'attachement. Les index
(`reports/README.md`, `reports/INDEX.md`) sont exclus par construction.

**Contrôle négatif 3 — le scan après la passe.** Sur les **723** fiches de `reports/`, il reste
**0 fiche de résultats** qui publie un des quatre marqueurs sans encart, hors les **2 faux
positifs** ci-dessus et les **2 index**. Le compte est reproductible par le scan du § 6.

**La re-mesure de l'état courant.** La fiche ne recopie pas l'état : elle le mesure. Commande :

```bash
python3 tools/drave.py evaluer --json        # gold vivant 612
python3 tools/drave.py evaluer --gold --json # gold gelé 602
```

Résultat au HEAD `229098ec` :

| gold | phrases | POS | F1 | tête | labels / cibles | exact | span exact |
|---|---:|---:|---:|---:|---:|---:|---:|
| **vivant** | 612 | **0,8625** | **0,7902** | 0,9029 | **238 / 239** | 0,9958 | 1,0 |
| **gelé** | 602 | **0,8625** | **0,7882** | 0,9025 | **234 / 239** | 0,9791 | 1,0 |

Le `span exact = 1,0` ne dit pas qu'il ne manque rien : il dit que **les 238 labels sont sur le
bon span**. Le 239e span, `g017`, n'a pas de label — c'est le **1 span** de l'état courant.

## 5. Ce qui pourrait rendre ce rapport faux

- **Le scan est lexical.** Il attrape les quatre chaînes et leurs variantes de POS, pas une
  formulation qui publierait `0,85` sans « POS » ni `85 %`. Une fiche peut donc rester périmée
  sans être prise. La passe générique — « tout chiffre d'arrivée antérieur à HEAD » — reste à
  faire ; `rapport-pensee-v11.md` (221/221, 18 spans) en est un exemple hors des quatre marqueurs.
- **L'état courant est daté.** Il vaut pour `229098ec`. Si un commit suivant change le bloc, les
  valeurs de ce rapport deviennent historiques à leur tour ; c'est précisément pourquoi les
  encarts **pointent** vers `en-cours` au lieu de recopier. Le lien reste vrai, le chiffre non.
- **La base.** La F1 et l'attachement diffèrent entre le **vivant 612** et le **gelé 602**
  (0,7902 / 0,7882 ; 238/239 / 234/239). Une fiche qui ne nomme pas sa base peut tromper même
  avec des chiffres exacts. Les deux sont donnés ici.
- **L'encart ne corrige pas le corps.** Il empêche une lecture périmée, il ne réécrit pas la
  fiche. Les chiffres du corps restent ceux du commit ; c'est le contrat de l'instantané.
- **Le lien dépend de `en-cours`.** Si `en-cours` est en retard, l'encart pointe vers un état en
  retard. Le contrôle de fraîcheur de `tools/revue_documentation.py` et la re-mesure ci-dessus
  sont la parade ; ils ne remplacent pas une mise à jour humaine.

## 6. La trace

- **Scan** : `python3 - <<'PY'` sur `reports/*.md`, quatre motifs
  (`POS 85`, `0,7535`, `236/237`, `2 spans`) ; `19` fiches annotées, `2` faux positifs, `2` index.
- **Fiche** : ce document. **JSON** : [`passe-honnetete.json`](passe-honnetete.json).
- **Commit** : `J9.1 — PASSE D'HONNÊTETÉ : 19 FICHES « INSTANTANÉ HISTORIQUE », 4 CHIFFRES
  DÉPASSÉS NE SE LISENT PLUS COMME L'ÉTAT COURANT`.
- **Prochaine action** : la passe **générique** (tout chiffre d'arrivée antérieur à HEAD), en
  commençant par les fiches B13 sans encart (`rapport-pensee-v11.md`, `rapport-pensee-v9.md`,
  `rapport-pensee-v10.md` a déjà le sien).
