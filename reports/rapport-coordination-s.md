# S — les 11 verdicts de `/paragraphes` ne sont pas dans git

> **Ligne de roadmap** : S · **Date** : 2026-11-13 · **HEAD parent mesuré** : `ced21933`
> · **Sous-module `tools/structures`** : `523d8c1` · **Verdict** : les 11 verdicts a004–a009
> sont **11 lignes non committées** de `donnees/paragraphes-validations.jsonl` (lignes **9–19**)
> : **6 `resolu`, 1 `compatible`, 4 `exclu`**, soit **7 acceptés et 4 exclus**. Le working tree
> voit **19 verdicts / 11 acceptés / 0 candidat sans verdict** ; un clone à `523d8c1` voit
> **8 verdicts / 4 acceptés / 11 candidats sans verdict**. **Aucun fichier de `tools/structures/`
> n'est modifié par cette fiche** : l'unique modification du sous-module est celle des 11
> verdicts, antérieure à la fiche.

**En trois lignes.** (1) Les 11 verdicts sont des verdicts de **candidat**, pas de paragraphe :
six paragraphes (`a004`–`a009`), onze candidats, ajoutés le **2026-11-04** entre **15:03:43** et
**15:10:08**. (2) Le fichier est **append-only** et le diff est **+11 / −0** ; rien n'est committé.
(3) La session S doit committer le fichier **dans le sous-module**, puis avancer le **pointeur**
`tools/structures` dans le parent : sans les deux, un clone du parent reste à 8 verdicts.

## Ce que cette fiche est, et n'est pas

- **Est** : une coordination en **lecture seule**. Elle liste les 11 lignes, donne la commande de
  commit de la session S et mesure ce qu'un clone à `523d8c1` voit réellement.
- **N'est pas** : un commit, un patch, ni une modification de `tools/structures/`. La session S
  reste seule à écrire dans son territoire.
- **Public** : la session S (prochaine action : committer les 11 verdicts) et le superviseur du
  chantier J4.
- **Ne tranche pas** la qualité des référents enregistrés : elle la signale (§ 1.1), parce que le
  commit les figera tels quels.

## 1. Les 11 verdicts, ligne à ligne

**Fichier unique** : `tools/structures/donnees/paragraphes-validations.jsonl`

| propriété | HEAD `523d8c1` | working tree |
|---|---|---|
| lignes | **8** | **19** |
| blob git | `2ada51b5e8f227e65b764f504aae1a6e8a1ef8b4` | `b34f8f548ed2d2e49c8e577e10fef96537522715` (calculé) |
| sha256 | `adf23efe0e8ebc77b397295521b1d1fccb4394c4c97e11bb859d0c1d2ada8862` | `a3c54c9cf2b81904ce43b43685be78f18ed675df2745e7b72ddcf0943d531123` |
| octets | 2 390 | 6 047 |

Le diff est **`+11 / −0`**, **non indexé** (`git diff`, pas `git diff --cached`) ; le hunk est
`@@ -6,3 +6,14 @@`, donc les lignes ajoutées sont **9 à 19** :

```text
tools/structures/donnees/paragraphes-validations.jsonl:9   a004-c1  resolu
tools/structures/donnees/paragraphes-validations.jsonl:10  a004-c2  exclu
tools/structures/donnees/paragraphes-validations.jsonl:11  a005-c1  resolu
tools/structures/donnees/paragraphes-validations.jsonl:12  a005-c2  exclu
tools/structures/donnees/paragraphes-validations.jsonl:13  a006-c1  resolu
tools/structures/donnees/paragraphes-validations.jsonl:14  a007-c1  resolu
tools/structures/donnees/paragraphes-validations.jsonl:15  a007-c2  exclu
tools/structures/donnees/paragraphes-validations.jsonl:16  a008-c1  compatible
tools/structures/donnees/paragraphes-validations.jsonl:17  a009-c1  resolu
tools/structures/donnees/paragraphes-validations.jsonl:18  a009-c2  exclu
tools/structures/donnees/paragraphes-validations.jsonl:19  a009-c3  resolu
```

| # | ligne | phrase | candidat | statut | accepté ? | horodatage |
|---:|---:|---|---|---|---|---|
| 1 | 9 | a004 | a004-c1 | `resolu` | oui | 2026-11-04T15:03:43 |
| 2 | 10 | a004 | a004-c2 | `exclu` | non | 2026-11-04T15:04:02 |
| 3 | 11 | a005 | a005-c1 | `resolu` | oui | 2026-11-04T15:06:12 |
| 4 | 12 | a005 | a005-c2 | `exclu` | non | 2026-11-04T15:06:26 |
| 5 | 13 | a006 | a006-c1 | `resolu` | oui | 2026-11-04T15:06:43 |
| 6 | 14 | a007 | a007-c1 | `resolu` | oui | 2026-11-04T15:07:00 |
| 7 | 15 | a007 | a007-c2 | `exclu` | non | 2026-11-04T15:07:05 |
| 8 | 16 | a008 | a008-c1 | `compatible` | oui | 2026-11-04T15:08:25 |
| 9 | 17 | a009 | a009-c1 | `resolu` | oui | 2026-11-04T15:09:45 |
| 10 | 18 | a009 | a009-c2 | `exclu` | non | 2026-11-04T15:10:02 |
| 11 | 19 | a009 | a009-c3 | `resolu` | oui | 2026-11-04T15:10:08 |

**Statuts** : `resolu` **6**, `compatible` **1**, `exclu` **4**, `double_sens` **0**. Au sens de la
page (résolu + compatible + double sens), **7 acceptés** et **4 exclus**. Les 11 lignes sont
`auteur: humain`, `niveau: 2`, **`note: ""`** : aucune note n'explique un choix.

### 1.1 Les référents enregistrés (inchangés par le commit)

Les 11 lignes portent **16 mappings uniques** (répétés d'un candidat à l'autre, 26 occurrences).
L'audit de `rapport-etat-s.md` § 2 les compare à la source anglaise :

| phrase | référents enregistrés | justes |
|---|---|---:|
| a004 | `sa → ALICE` | 1/1 |
| a005 | `elle → Alice`, `son → Alice`, `en → coup` | 2/3 (`en` faux ; attendu : la salle) |
| a006 | `cela → Comme`, `son → Alice`, `elle → Alice`, `y → table` | 3/4 (`cela` faux ; attendu : attendre à la petite porte) |
| a007 | aucun | 0/0 |
| a008 | `Je → le contenu`, `me → le contenu`, `on → Je me sens toute drôle`, `je → Je me sens toute drôle`, `en → Je me sens toute drôle` | 0/5 |
| a009 | `se → Un moment`, `elle → Alice`, `en → Un moment` | 1/3 (`se` et `en` faux ; attendu : Alice / préposition) |
| **total** | **16 mappings uniques** | **7/16** |

**Conséquence pour le commit** : les statuts de structure sont des décisions humaines, mais **9 des
16 référents sont faux ou restés aux défauts de la page** (`a008` en porte 5 à lui seul). Committer
le fichier tel quel **fige ces référents** avec `auteur: humain` et `note: ""`. Deux options, à
trancher par S :

- **A (recommandée)** : committer les 11 verdicts tels quels pour **ne pas perdre la seule trace**,
  puis ouvrir une correction de référents séparée (le fichier est append-only, la correction peut
  être un nouveau verdict sur le même candidat ; la page prend le dernier).
- **B** : corriger les 9 mappings dans le working tree **avant** le commit, avec une note qui dit
  pourquoi. Le diff n'est alors plus « +11 tel qu'enregistré » et il n'existe plus de trace de la
  valeur d'origine.

La fiche ne fait ni A ni B : elle donne la commande de A et signale B.

## 2. Ce que git voit, ce que le working tree voit

### 2.1 Les totaux

| mesure | HEAD `523d8c1` | working tree | delta |
|---|---:|---:|---:|
| verdicts (`lignes`) | **8** | **19** | **+11** |
| `resolu` | 4 | 10 | +6 |
| `compatible` | 0 | 1 | +1 |
| `exclu` | 4 | 8 | +4 |
| `double_sens` | 0 | 0 | 0 |
| **acceptés** (page) | **4** | **11** | **+7** |
| paragraphes jugés | 3/9 (a001–a003) | 9/9 (a001–a009) | +6 |
| candidats sans verdict | **11** | **0** | −11 |

**Attention aux deux « 11 ».** Les **11 verdicts non committés** (a004–a009) ne sont pas les
**11 lectures acceptées** du working tree : les premiers comptent 7 acceptés + 4 exclus ; les
seconds sont la somme des acceptés sur les 19 verdicts (a001–a009). Un clone à `523d8c1` n'a que
**4 acceptés** et **8 verdicts**. Les deux chiffres « 11 » sont vrais, mais dans deux ensembles
différents ; les confondre est l'erreur que la fiche `rapport-etat-s.md` avait déjà relevée.

### 2.2 Par paragraphe

| phrase | candidats | verdicts HEAD | verdicts working | dont les 11 non committés |
|---|---:|---:|---:|---|
| a001 | 2 | 2 | 2 | — |
| a002 | 3 | 3 | 3 | — |
| a003 | 3 | 3 | 3 | — |
| a004 | 2 | **0** | 2 | c1 `resolu`, c2 `exclu` |
| a005 | 2 | **0** | 2 | c1 `resolu`, c2 `exclu` |
| a006 | 1 | **0** | 1 | c1 `resolu` |
| a007 | 2 | **0** | 2 | c1 `resolu`, c2 `exclu` |
| a008 | 1 | **0** | 1 | c1 `compatible` |
| a009 | 3 | **0** | 3 | c1 `resolu`, c2 `exclu`, c3 `resolu` |
| **total** | **19** | **8** | **19** | **11** |

Les 19 candidats sont **régénérés à la volée** par `generateur.analyser` (comptes 2, 3, 3, 2, 2, 1,
2, 1, 3) : ils ne sont pas stockés dans `paragraphes.json`. À `523d8c1`, les 11 candidats a004–a009
existent donc dans la page, mais **aucun n'a de verdict** : le clone affiche 9 paragraphes et
19 cartes, dont 11 sans badge.

### 2.3 Ce que le commit ne répare pas

- **0 note** sur les 11 verdicts ; le journal ne distingue pas un choix humain d'un défaut de page.
- Le seul `compatible` est **a008**, précisément le paragraphe à **0/5** référents : le statut dit
  « pas tranché », mais 5 référents faux sont enregistrés.
- Les verdicts valident la **structure** (quelle lecture est acceptée), pas la **référence**.

## 3. La commande de commit pour la session S

**Préconditions mesurées le 2026-11-13** : sous-module sur `master`, HEAD `523d8c1`, **un seul
fichier modifié** (`M donnees/paragraphes-validations.jsonl`), `+11 / −0`. Le parent est sur
`s/v7` et porte **d'autres modifications d'autres sessions** : `git add` explicite, **jamais**
`git commit -a`.

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures

# 1. vérifier l'état : un seul fichier, 11 ajouts, 0 suppression
git status --porcelain
# attendu : " M donnees/paragraphes-validations.jsonl" et rien d'autre
git diff --numstat
# attendu : 11	0	donnees/paragraphes-validations.jsonl

# 2. committer les 11 verdicts (add explicite)
git add donnees/paragraphes-validations.jsonl
git commit -m "S — VALIDATION HUMAINE : 11 VERDICTS SUR /PARAGRAPHES (a004–a009), 7 ACCEPTÉS (6 RÉSOLUS, 1 COMPATIBLE), 4 EXCLUS"

# 3. publier le sous-module AVANT le pointeur parent
git push origin master

# 4. avancer le pointeur dans le dépôt parent
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
git add tools/structures
git commit -m "S — POINTEUR : 11 VERDICTS /PARAGRAPHES (a004–a009) COMMITTÉS"
git push origin s/v7
```

**Vérification après le commit** :

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures
git show --stat --oneline HEAD
# attendu : 1 file changed, 11 insertions(+)
git show HEAD:donnees/paragraphes-validations.jsonl | wc -l
# attendu : 19

cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
git ls-tree HEAD tools/structures
# attendu : 160000 commit <nouveau_sha> tools/structures (et non plus 523d8c1)
```

**Pourquoi deux commits et deux push.** Le parent ne stocke qu'un **pointeur** (gitlink) vers le
sous-module. Committer le sous-module sans avancer le pointeur laisse un clone du parent à
`523d8c1` ; avancer le pointeur sans publier le sous-module laisse un clone incapable de récupérer
l'objet `<nouveau_sha>`. Les deux push sont donc nécessaires pour qu'un clone **neuf** voie les 11
verdicts.

**Contrôle de la commande.** Rejouée dans un clone **jetable** du sous-module (sans push), la
commande du sous-module donne `1 file changed, 11 insertions(+)` ; un clone de ce commit voit
**19 verdicts** (10 `resolu`, 1 `compatible`, 8 `exclu`) et **11 acceptés**. La commande est donc
mécaniquement valide ; le seul risque restant est celui du § 4.

## 4. Le risque d'un clone à `523d8c1`

### 4.1 Le contrôle négatif, mesuré

```bash
tmp=$(mktemp -d)
git clone -q tools/structures "$tmp/s"
cd "$tmp/s"
git rev-parse HEAD            # 523d8c1e8c6ca29ca415360a71bfab6c5b56102c
git status --porcelain        # 0 ligne : propre
wc -l < donnees/paragraphes-validations.jsonl   # 8
```

Résultat mesuré : **HEAD `523d8c1`**, working tree **propre**, **8 lignes**, **4 `resolu` + 4
`exclu`**, **4 acceptés**, phrases **a001–a003** uniquement, sha256
`adf23efe0e8ebc77b397295521b1d1fccb4394c4c97e11bb859d0c1d2ada8862`. Un clone à `523d8c1` **ne
voit aucun des 11 verdicts**.

### 4.2 Les risques, par gravité

1. **Perte sèche (haute).** Les 11 verdicts n'existent que dans le working tree local : ni commit,
   ni reflog, ni remote. Un `git reset --hard`, un `git checkout -- .`, un `git clean -fd`, un
   rebase interrompu ou une perte de machine les détruit **sans récupération possible**. C'est la
   seule copie de six paragraphes jugés **neuf jours plus tôt**, le 2026-11-04.
2. **Clone trompeur (haute).** Un clone à `523d8c1` affiche **9 paragraphes et 19 candidats** mais
   seulement **8 verdicts / 4 acceptés / 11 candidats sans verdict**. Toute affirmation « 9/9,
   19/19, 0 restant » est fausse dans ce clone : elle n'est vraie que dans le working tree.
3. **Re-jugement et écrasement (moyenne).** Un opérateur parti d'un clone re-jugera a004–a009. La
   page prend le **dernier** verdict par candidat (`dernier()` dans `static/paragraphes.js`) : les
   nouveaux verdicts écrasent à l'affichage les choix du 2026-11-04 (notamment `a004 sa → ALICE`
   en majuscules et `a008 compatible`), et le fichier append-only garde les deux sans dire lequel
   fait foi. Les 11 lignes d'origine deviennent invisibles dans l'UI.
4. **Référents figés (moyenne).** Le commit fige **9 mappings faux sur 16** (§ 1.1) avec
   `auteur: humain` et `note: ""`. Ce n'est pas une perte de données, mais cela transforme des
   défauts de page en « vérité » committée ; une correction ultérieure devra être explicite.
5. **Pointeur orphelin (moyenne).** Si S committe le pointeur parent sans publier le sous-module,
   le clone du parent échoue à récupérer le gitlink ou reste à l'ancien. Si S publie le sous-module
   sans le pointeur, le clone du parent reste à `523d8c1`. Les deux commits sont indissociables.
6. **Sous-module non portable (haute, pré-existante).** `.gitmodules` pointe
   `tools/structures` vers un **chemin local absolu**
   (`/home/stephane/Data13TB/stephane/GitHub/drave-structures`), et l'`origin` du sous-module est
   ce même chemin. Sur une **autre machine**, un clone du parent avec `--recurse-submodules` ne
   peut pas initialiser `tools/structures` ; sans l'option, le répertoire est vide. Le « clone voit
   8 verdicts » est donc un **majorant local** : hors de cette machine, il peut n'en voir **aucun**.
   Ce défaut est antérieur aux 11 verdicts et n'est pas réparé par leur commit.
7. **Arbre parent sale (basse).** `git status` du parent affiche ` M tools/structures` et d'autres
   modifications d'autres sessions. Les outils qui exigent un arbre propre (ou un `git archive`)
   ignorent les 11 lignes ; un `git commit -a` les emporterait avec des changements étrangers.

### 4.3 Ce que le commit change, et ce qu'il ne change pas

- **Change** : un clone à `523d8c1` reste à 8 ; un clone au **nouveau** commit du sous-module voit
  19 verdicts, 11 acceptés, 0 candidat sans verdict — **à condition** que le parent pointe vers ce
  commit et que le sous-module soit publié.
- **Ne change pas** : les 9 référents faux, l'absence de note, le `compatible` de a008, et le
  chemin local du `.gitmodules`. Ces points demandent une décision de S, pas un simple commit.

## 5. Ce qui pourrait rendre cette fiche fausse

- **S committe avant la lecture** : le diff, les numéros de ligne et le blob `b34f8f5` changent ;
  les hashes et les IDs de candidats restent la clé stable.
- **Une ligne est insérée avant la ligne 9** : les numéros 9–19 se décalent ; se référer aux
  `candidat_id` et aux hashes, pas aux numéros seuls.
- **`generateur.analyser` change** : les comptes 2, 2, 1, 2, 1, 3 et les IDs `cNN` dépendent du
  générateur à `523d8c1`. La fiche mesure ce commit, pas un autre.
- **Le HEAD du sous-module ou le pointeur parent bouge** : le contrôle négatif et les totaux
  décrivent l'état `523d8c1` / `ced21933` du 2026-11-13.
- **L'audit des référents est cité, pas re-mesuré ici** : les 16 mappings et le 7/16 viennent de
  `rapport-etat-s.md` § 2, relu pour cette fiche ; la source anglaise n'a pas été ré-alignée ligne
  à ligne. Le point qui compte pour le commit (9 faux) est stable, mais un audit indépendant
  pourrait compter autrement les formes répétées.
- **Le contrôle négatif est local** : il clone le dépôt local `tools/structures`. Sur une autre
  machine, le `.gitmodules` en chemin absolu peut rendre le clone impossible (§ 4.2, risque 6).
- **La commande de commit suppose `master` et `s/v7`** : si S change de branche ou si le remote
  `origin` du sous-module n'est plus le dépôt local, adapter `git push origin master` et
  `git push origin s/v7` ; les commits, eux, ne changent pas.

## 6. Fichiers lus, non modifiés

- `tools/structures/donnees/paragraphes-validations.jsonl` (working tree et `HEAD`)
- `tools/structures/donnees/paragraphes.json` (9 paragraphes, `HEAD`)
- `tools/structures/serveur.py`, `tools/structures/generateur.py`, `tools/structures/static/paragraphes.js`
- `tools/structures/.git` (HEAD, status, diff, blob, remote), parent `.gitmodules`
- `reports/rapport-etat-s.md` (audit des référents, § 2)
- `reports/rapport-s-paragraphes.md` (fiche des 9 paragraphes)
- `docs/pilotage/en-cours.md`, `docs/pilotage/roadmap.md` (état S)

Aucune écriture dans `tools/structures/` ; le `git status` du sous-module est resté
`M donnees/paragraphes-validations.jsonl`, sans fichier ajouté (pas de `__pycache__`).

## 7. Références

- [rapport-etat-s.md](rapport-etat-s.md) — l'audit 19/19 et les 12 référents faux.
- [rapport-s-paragraphes.md](rapport-s-paragraphes.md) — les six paires a004–a009 et la page.
- [pensee-etat-s.json](pensee-etat-s.json) — l'instantané JSON de l'état S.
- [roadmap.md](../docs/pilotage/roadmap.md) — ligne S, § « la banque validée ».
- [en-cours.md](../docs/pilotage/en-cours.md) — l'état S courant.
