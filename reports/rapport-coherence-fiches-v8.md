# Cohérence des fiches B13 du 2026-11-05 — v2 → v8 (état `f908d7b0`)

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ❌
> **8 fiches auditées** (1 courante, 7 historiques), **42 écarts** dont **7 critiques** ;
> **8/8** ont au moins un écart ; **3 contrôles négatifs invalides** (v4, v5, v6) et **2 absents**
> (v8, gold-split) ; **7 mentions d'historique obsolètes** (v2→v7) et **1 imprécise** (v8) ;
> **5 lignes** de `reports/README.md` à corriger ; **1 lien cassé** au commit (`rapport-spans-v7.md`,
> cité par la v8, absent de `f908d7b0`) ; **2 tableaux dont la somme visible ne tombe pas**
> (corrections de la v2, règles de la v8).
>
> **État audité** : commit **`f908d7b0`** (2026-11-05 21:08, branche `s/v7`), le commit demandé
> (avant `d497324b`). Les huit fiches, leurs huit JSON et `reports/README.md` sont lus **à ce
> commit** (`git show f908d7b0:…`), pas dans l'arbre de travail.
>
> **HEAD a bougé (note de version)** : pendant l'audit, HEAD est passé de `f908d7b0` à
> **`d497324b`** (« la v8 réécrite honnêtement : +17 net, 7 régressions ; audits A17/A19
> intégrés »). Ce commit corrige déjà une partie de ce rapport : la v8 est réécrite (+17 net,
> 7 régressions, 17+7+3, contrôle, date/commit, couverture française), la v7 est passée en
> instantané (`0,7482`, « qui » 6, § 3), et les contrôles v4/v5/v6 sont remplacés par un renvoi
> au dispositif de la v7 (le faux `1,67/196` disparaît, mais il n'y a toujours pas de contrôle
> sur leur base). **Ce rapport décrit `f908d7b0`**, l'état demandé : les points V8-1/2/3/5/6 et
> V7-1/2, ainsi que l'essentiel de V7-6, y sont donc déjà traités à `d497324b`. Les points V2, V3, V4, V5, V6, gold-split, le
> JSON v7 `avant` et les lignes README restent à vérifier sur le nouveau HEAD. Une lecture rapide
> de la nouvelle table d'ablation de la v8 y montre une arithmétique à contrôler (R1 :
> 15+1+4 = 20 gains, 19 annoncés ; total 26 gains / 18 net, 24/17 annoncés ; `g017` compté comme
> perte R1c alors qu'il manquait déjà en v7) — audit séparé, non couvert ici. De même, le
> `top-k 211` de la nouvelle fiche est postérieur à `f908d7b0` (correctif `prec = s`), alors que
> son en-tête porte `Commit : f908d7b0` : à dater.
>
> **Concurrence (arbre de travail au moment de l'écriture)** : l'arbre contenait des corrections
> non committées de `rapport-pensee-couverture-v7.md` (en-tête POS `0,7475` → `0,7482`, « qui »
> `12` → `6`, § 3) et `rapport-spans-v7.md` (A17) non suivi. Ces corrections sont désormais
> committées dans `d497324b` ; le lien A17 est donc valide au nouveau HEAD.
>
> **Méthode** : lecture intégrale des 8 fiches et des 8 JSON au commit ; pour chaque fiche,
> chargement du `bloc_linguistique.py` **historique** depuis `git show <commit>:tools/bloc_linguistique.py`
> comme module (avec `RACINE` forcée à la racine), puis `evaluer_bloc` sur le **gold vivant 612**
> et le **gold gelé 602** ; les fichiers d'or sont **identiques** de `9d5337ce` à `f908d7b0`
> (`git diff --stat` vide). Les portes de mesure T110/T112/T113 ont été rejouées vertes ; les
> 183 portes n'ont pas été rejouées en entier.
> **Aucune fiche modifiée, aucun commit, aucune écriture hors des deux fichiers de sortie.**
> Détail structuré : [`pensee-coherence-fiches-v8.json`](pensee-coherence-fiches-v8.json).

## 1. Synthèse

| indicateur | valeur |
|---|---:|
| fiches vérifiées | **8** |
| fiches courantes / historiques | **1 / 7** |
| fiches sans écart | **0** |
| écarts | **42** |
| — critiques (chiffre de tête, statut, somme) | **7** |
| — majeurs (table, prose, base, JSON) | **23** |
| — mineurs (dénominateurs, arrondi, métadonnées) | **12** |
| fiches avec au moins un écart critique | **4** (v4, v5, v7, v8) |
| contrôles négatifs valides | **2** (v2 négatif documenté, v3) + **1 sous réserve** (v7) |
| contrôles négatifs invalides | **3** (v4, v5, v6) |
| contrôles négatifs absents | **2** (v8, gold-split) |
| fiches historiques avec mention obsolète | **7** (v2→v7) |
| fiches dont la base F1/tête/POS est fausse ou absente | **2** (v4, v5) + **2 partielles** (v7, v8) |
| lignes de `reports/README.md` à corriger | **5** (20, 21, 23, 24, 25) |
| liens cassés au commit `f908d7b0` | **1** (v8 → `rapport-spans-v7.md`) |
| tableaux dont la somme visible ne tombe pas | **2** (v2, v8) |

**Lecture.** Les chiffres de mesure des huit fiches se reproduisent presque tous : le problème
n'est pas le calcul, il est dans les **libellés, les bases, les contrôles et le récit**. Trois
couches d'erreurs se cumulent :

1. **La v8 est la fiche la plus grave** : son tableau de règles est emprunté au prototype A17
   (`+27` exacts, `0 perte`), alors que le code intégré fait **+23 labels gagnés et −7 perdus**
   (`+16` labels, `+17` exacts), dont **7 pertes françaises** ; les « 17 inatteignables » sont
   un compte juste par coïncidence, mais la composition publiée est fausse (6 des 12
   « synthétiques » sont des régressions, 3 SUB synthétiques sont omises). La fiche n'a **ni
   date ni contrôle négatif**, et son lien A17 n'est pas committé.
2. **Les v4, v5, v6 ont copié le contrôle de la v7** (`1,67/196` contre `195/196`) alors que
   leurs bases sont `160`, `187` et `187` labels : le contrôle ne mesure pas leur dispositif.
3. **La v7 est encore présentée comme « état courant »** alors que la v8 la remplace ; son JSON
   `avant` mélange trois bases (v6 612, v5, v4) et son en-tête POS utilise `0,7475`, la valeur
   de la **v4**, au lieu de `0,7482` (v6 mesurée).

## 2. Les huit fiches

| # | fiche | JSON | commit | statut | portes | B13 | date | verdict | écarts |
|---:|---|---|---|---|---:|---|---|---|---:|
| 1 | [`rapport-pensee-attachement-v2.md`](rapport-pensee-attachement-v2.md) | [`pensee-attachement-v2.json`](pensee-attachement-v2.json) | `9d5337ce` | historique | 180/180 | ✅ | 2026-11-05 | ✅ | 4 |
| 2 | [`rapport-pensee-attachement-v3.md`](rapport-pensee-attachement-v3.md) | [`pensee-attachement-v3.json`](pensee-attachement-v3.json) | `dcf7bc91` | historique | 181/181 | ✅ | 2026-11-05 | ✅ | 3 |
| 3 | [`rapport-pensee-segmentation-v4.md`](rapport-pensee-segmentation-v4.md) | [`pensee-segmentation-v4.json`](pensee-segmentation-v4.json) | `392f03aa` | historique | 183/183 | ✅ | 2026-11-05 | ✅ | 4 |
| 4 | [`rapport-pensee-couverture-v5.md`](rapport-pensee-couverture-v5.md) | [`pensee-couverture-v5.json`](pensee-couverture-v5.json) | `b975011b` | historique | 183/183 | ✅ | 2026-11-05 | ✅ | 5 |
| 5 | [`rapport-pensee-attachement-parfait.md`](rapport-pensee-attachement-parfait.md) | [`pensee-attachement-parfait.json`](pensee-attachement-parfait.json) | `0ec6c27d` | historique | 183/183 | ✅ | 2026-11-05 | ✅ | 3 |
| 6 | [`rapport-gold-split.md`](rapport-gold-split.md) | [`pensee-gold-split.json`](pensee-gold-split.json) | `85e4082b` | historique | — | ✅ | 2026-11-05 | ✅ | 4 |
| 7 | [`rapport-pensee-couverture-v7.md`](rapport-pensee-couverture-v7.md) | [`pensee-couverture-v7.json`](pensee-couverture-v7.json) | `69bd865e` | **historique** (dit « courante ») | 183/183 | ✅ | 2026-11-05 | ✅ | 7 |
| 8 | [`rapport-pensee-r1r3.md`](rapport-pensee-r1r3.md) | [`pensee-r1r3.json`](pensee-r1r3.json) | `f908d7b0` | **courante** | 183/183 | ✅ | **❌ absente** | ✅ | 8 |

Les huit fiches nomment **B13** et un **verdict**. La v8 est la seule à **ne pas nommer sa date**
(l'en-tête porte `Ligne de roadmap · État courant · Verdict`, sans `Date` ; le JSON porte
`"date": "2026-11-05"`). La v7 se dit « état courant » alors qu'elle est l'avant-dernière.
`gold-split` ne donne pas le compte de portes (le commit `85e4082b` est à 183/183) ; son JSON n'a
pas de champ `portes`.

## 3. Mesures reproduites

### 3.1 Attachement, couverture, spans (gold gelé 602, valeurs identiques sur 612)

| fiche | labels | exact | couverture | top-k | fr | en | spans |
|---|---:|---:|---:|---:|---|---|---|
| v2 | 145 | 137/145 (0,9448) | 0,6067 | 142/239 | 109/117 | 28/28 | 94 = 48 REL + 33 SUB + 13 GP |
| v3 | 145 | 141/145 (0,9724) | 0,6067 | 142/239 | 113/117 | 28/28 | 94 = 48 REL + 33 SUB + 13 GP |
| v4 | 160 | 157/160 (0,9812) | 0,6695 | 156/239 (0,6527) | 117/118 (0,9915) | 40/42 (0,9524) | 79 = 48 REL + 21 SUB + 10 GP |
| v5 | 187 | 186/187 (0,9947) | 0,7824 | 161/239 (0,6736) | 126/127 (0,9921) | 60/60 (1,0000) | 52 = 24 REL + 12 SUB + 16 GP |
| v6 | 187 | 187/187 (1,0000) | 0,7824 | 161/239 (0,6736) | 127/127 (1,0000) | 60/60 (1,0000) | 52 = 24 REL + 12 SUB + 16 GP |
| v7 | 196 | 195/196 (0,9949) | 0,8201 | 166/239 (0,6946) | 135/135 (1,0000) | 60/61 (0,9836) | 43 = 21 REL + 17 SUB + 5 GP |
| v8 | 212 | 212/212 (1,0000) | 0,8870 | 177/239 (0,7406) | 129/129 (1,0000) | 83/83 (1,0000) | 27 = 16 REL + 6 SUB + 5 GP |

Les dénominateurs de cibles par langue sont absents des fiches et des JSON : **fr 151 cibles,
en 88 cibles**. Les taux « fr 129/129 » et « en 83/83 » de la v8 sont des **exacts sur labels**,
pas des couvertures : la couverture française est **129/151 = 0,8543**, l'anglaise **83/88 =
0,9432**. Pour la v7 : fr **135/151 = 0,8940**, en **61/88 = 0,6932** — la couverture anglaise
est bien plus basse que le taux exact `60/61` ne le suggère.

### 3.2 F1, tête, POS : 612 vivant / 602 gelé

| fiche | F1 612 | F1 602 | tête 612 | tête 602 | POS 612 | POS 602 |
|---|---:|---:|---:|---:|---:|---:|
| v2 | 0,2862 | 0,2895 | 0,4989 | 0,5053 | 0,7455 | 0,7475 |
| v3 | 0,2862 | 0,2895 | 0,4989 | 0,5053 | 0,7455 | 0,7475 |
| v4 | 0,4509 | **0,4539** | 0,6385 | **0,6432** | 0,7455 | 0,7475 |
| v5 | 0,5130 | 0,5164 | 0,6785 | 0,6834 | 0,7461 | 0,7482 |
| v6 | **0,5130** | 0,5164 | 0,6785 | 0,6834 | 0,7461 | 0,7482 |
| v7 | 0,5555 | **0,5595** | 0,7152 | **0,7205** | 0,7581 | **0,7603** |
| v8 | 0,5720 | **0,5763** | 0,7262 | **0,7316** | 0,7581 | 0,7603 |
| gold-split | 0,4414 / 0,4719 (dev/test) | — | 0,6347 / 0,6470 | — | — | — |

En gras, la valeur publiée par la fiche. Vérifications :

- **v4** publie la F1 et la tête du **602** (`0,4539`, `0,6432`) mais son § 3 parle du « gold
  612 » ; sur 612, le code donne `0,4509`, `0,6385`. Surtout, sa colonne « avant »
  (`0,2862`, `0,4989`) est la **v3 sur 612**, pas la v3 sur 602 (`0,2895`, `0,5053`) : la ligne
  F1/tête compare **deux golds différents**.
- **v5** publie `0,5156` / `0,6826`, qui ne sont **ni** le 602 (`0,5164` / `0,6834`) **ni** le 612
  (`0,5130` / `0,6785`) : ce sont les constantes de la porte T112/T113 (état `7a9f0d6a`,
  tolérance `0,001`). La fiche ne nomme pas la base.
- **v6** publie `0,5130`, la valeur du **612**, et l'étiquette « (612) » : c'est la seule des
  quatre fiches de milieu de journée dont la F1 est sur le gold annoncé.
- **v7** publie les valeurs du **602** et les nomme ; les valeurs 612 sont données dans la ligne
  « Base » (`0,5555` / `0,7152` / `0,7581`). En revanche, l'en-tête dit `POS 0,7475 → 0,7603`
  et le JSON `avant.pos` vaut `0,7475` : c'est la POS de la **v4**, pas celle de la v6
  (`0,7482`). La table, elle, dit bien `0,7482`.
- **v8** publie `0,5763` / `0,7316`, valeurs du **602** ; la table le dit (« gelé 602 »), mais
  l'en-tête et le JSON ne portent aucune base. Sur 612 : `0,5720` / `0,7262`.
- **gold-split** est sur le **612** (le gold de la fiche), et le dit.

### 3.3 dev/test

| fiche | dev | test | F1 dev | F1 test | tête dev | tête test |
|---|---:|---:|---:|---:|---:|---:|
| gold-split | 104/106 (0,9811) | 53/54 (**0,9815**) | 0,4414 | 0,4719 | 0,6347 | 0,6470 |
| v5 | 126/126 (1,0000) | 60/61 (0,9836) | 0,5091 | 0,5217 | 0,6782 | 0,6792 |
| v6 | 126/126 (1,0000) | 61/61 (1,0000) | 0,5091 | 0,5217 | 0,6782 | 0,6792 |
| v7 | 133/134 (0,9925) | 62/62 (1,0000) | 0,5512 | 0,5651 | 0,7132 | 0,7196 |
| v8 | 148/148 (1,0000) | 64/64 (1,0000) | 0,5723 | 0,5714 | 0,7270 | 0,7241 |

Le split est stable (422 phrases / 163 cibles / 106 labels en dev ; 190 / 76 / 54 en test ;
total 612 / 239 / 160). **La v5 écrit `dev 126/126 (0,9921)`** : le numérateur est juste, le taux
est celui du français (`126/127`), pas du dev (`126/126 = 1,0000`). **gold-split écrit
`test 53/54 (0,9814)`** : `53/54 = 0,98148…`, arrondi à `0,9815` (le code rend `0,9815`). La
fiche et le JSON sont à `0,9814` (troncature).

## 4. Registre des écarts

Légende : **C** = critique, **M** = majeure, **m** = mineure. Les 42 lignes sont reprises dans
le JSON (`divergences`).

### 4.1 v2 — `9d5337ce` (4 écarts)

| id | gravité | où | constat | correction |
|---|---|---|---|---|
| V2-1 | M | § 1, tableau lignes 29-30 | Les lignes « cibles verbes (POS gold) » / « cibles noms (POS gold) » donnent, en « avant », `63 (0,9524)` et `82 (0,7683)`. Ces comptes et ces taux sont le **split lexical pré-v2** (`_est_verbe` : 60/63 et 63/82, vérifié sur `9d5337ce^`), pas le POS gold. L'« après » `111/116`, `26/29` est le POS gold. `+53 cibles` est `116 − 63`, un **reclassement**, pas un gain : les justes passent 60 → 111 (+51) et les noms 63 → 26 (−37). | Étiqueter l'avant « split lexical (`_est_verbe`) 60/63, 63/82 » et l'après « POS gold 111/116, 26/29 » ; remplacer `+53 cibles` par le reclassement et les justes. |
| V2-2 | M | § 2, ligne 48 | « **46** des 57 échecs étaient des candidats non réduits à leur tête. Réduits → **+45** » : 46 et +45 dans la même phrase. Le gain strict est 45 (`141 − 88 − 8 = 45`) ; 46 est `134 − 88` (top-k moins strict), pas le compte des têtes. | Lire **45**. |
| V2-3 | M | § 2, tableau des corrections | La colonne « gain » ne s'additionne pas : strict `88 + 45 = 133` pour un total de 141 ; top-k `134` pour 142 ; top1 `126 + 8 = 134` pour 140. Les +8 top-k/strict du lexique et le +6 top1 du segment ne sont pas crédités. | Créditer le lexique de **+8 top-k et +8 strict**, le segment de **+6 top1**, ou ajouter une ligne « total ». |
| V2-4 | m | JSON | Le JSON n'a que les taux : les comptes 60/63, 63/82, 111/116, 26/29, `22 = 11 + 11`, `46/57`, `139/145`, `r048/r068`, les 8 verbes anglais manquent. | Ajouter les compteurs et le détail des corrections, ou retirer ces chiffres du texte. |

### 4.2 v3 — `dcf7bc91` (3 écarts)

| id | gravité | où | constat | correction |
|---|---|---|---|---|
| V3-1 | M | JSON | La note A13 du Markdown (43/96 GP, `exact_any 143/145`, 143/239, McNemar p = 0,5, s108/s122) est **absente du JSON** : pas de champ `exact_any`, pas de bloc `A13`. Le JSON n'a pas suivi la réparation du tableau. | Ajouter `exact_any` (143/145, 143/239) et le bloc A13. |
| V3-2 | m | § 2, tableau des règles | R1 est donné « portée 2–3 » avec **trois** identifiants (`s108`, `s122`, `s041`) : le 2 et le 3 ne sont pas expliqués. | Écrire 3 (ou 2 + s041 expliqué). |
| V3-3 | m | JSON | Les comptes 111/116, 112/116, 26/29, 29/29 ne sont pas dans le JSON (taux seulement). | Ajouter les numérateurs/dénominateurs. |

### 4.3 v4 — `392f03aa` (4 écarts)

| id | gravité | où | constat | correction |
|---|---|---|---|---|
| V4-1 | **C** | titre et § 2, lignes 1 et 33-34 | La ligne F1/tête compare **deux golds** : `0,2862 / 0,4989` est la **v3 sur 612**, `0,4539 / 0,6432` est la **v4 sur 602**. Sur un gold constant : 602 `0,2895 / 0,5053 → 0,4539 / 0,6432` ; 612 `0,2862 / 0,4989 → 0,4509 / 0,6385`. Le `0,2862 → 0,4539` du titre est un delta mixte. | Choisir une base et l'écrire : 602 (`0,2895 → 0,4539`, `0,5053 → 0,6432`) ou 612 (`0,2862 → 0,4509`, `0,4989 → 0,6385`). |
| V4-2 | M | contrôle négatif | Le paragraphe copie le contrôle de la **v7** : `1,67/196` contre `195/196`. La v4 a **160** labels et **157** exacts ; `195/196` n'est pas son observation. | Mesurer sur 160 (même principe : `1,80/160` contre `157/160`, 100 tirages, graine 20261105) ou retirer le paragraphe. |
| V4-3 | M | § 3, ligne 61 | « Le gold 612 » alors que la F1 et la tête publiées sont mesurées sur le **602** ; la base n'est pas nommée dans le tableau. | Nommer le 602, ou publier les valeurs du 612 (`0,4509 / 0,6385`). |
| V4-4 | m | JSON | Les effets intermédiaires des sept corrections (145→159, 141→145, 0,2937→0,4033, 0,4194, 144→152, 30→38, 152→158, 0,5930, passif 3/3, 84 spans de A12, 38 assertions) ne sont pas dans le JSON. | Ajouter ces valeurs ou les retirer du texte. |

### 4.4 v5 — `b975011b` (5 écarts)

| id | gravité | où | constat | correction |
|---|---|---|---|---|
| V5-1 | **C** | § 2, ligne 51 | « dev **126/126 (0,9921)** » : `126/126 = 1,0000` ; `0,9921` est le taux français `126/127`. L'en-tête dit bien `dev 126/126 (1,000)`, et la v6 aussi. | Écrire **126/126 (1,0000)**. |
| V5-2 | M | contrôle négatif | Le paragraphe copie la **v7** : `1,67/196` contre `195/196`. La v5 a **187** labels et **186** exacts. | Mesurer sur 187 (même principe : `1,93/187` contre `186/187`) ou retirer. |
| V5-3 | M | en-tête, § 2, JSON, README ligne 23 | F1 `0,5156` et tête `0,6826` sont les **constantes de la porte T112/T113** (état `7a9f0d6a`), pas la mesure de `b975011b` : 602 `0,5164 / 0,6834`, 612 `0,5130 / 0,6785`. La base n'est pas nommée ; le README écrit « F1 0,5156 (602) », ce qui est faux au quatrième chiffre. | Publier `0,5164 / 0,6834` (602) ou écrire explicitement « constante de porte 0,5156/0,6826, tolérance 0,001 ». |
| V5-4 | M | § 3, § 5, JSON `limites` | « Les **27 échecs de cible** » contredit `apres.echecs_cible = 1` et le § 2 (« l'échec de cible unique et les 26 candidats manquants »). 27 = **1 échec de cible + 26 candidats manquants**. | Écrire « 1 échec de cible + 26 candidats manquants (27 écarts) » partout, y compris `limites`. |
| V5-5 | m | § 1 correction 7 vs v6 § 1 correction 1 | La même correction est décrite « **27 → 26 couvertures** » dans la v5 et « **26 → 26** » dans la v6. Le chiffre correct est « candidats manquants 27 → 26 » (JSON `candidats_manquants: 26`). | Harmoniser : « candidats manquants 27 → 26 ». |

### 4.5 v6 — `0ec6c27d` (3 écarts)

| id | gravité | où | constat | correction |
|---|---|---|---|---|
| V6-1 | M | contrôle négatif | Le paragraphe copie la **v7** : `1,67/196` contre `195/196`. La v6 a **187** labels et **187** exacts. | Mesurer sur 187 (même principe : `1,95/187` contre `187/187`) ou retirer. |
| V6-2 | M | § 1, correction 1 | « couverture des candidats **26 → 26**, top-k 161 » est un **no-op** : la correction des candidats du précédent est déjà dans la v5 (`b975011b`) ; le diff de code `b975011b..0ec6c27d` n'ajoute que la règle adverbe/repli (r309). La fiche présente donc comme « correction de ce round » une correction qui n'en est pas une. | Retirer la ligne 1 des « deux corrections de ce round », ou l'étiqueter « déjà en v5, sans effet ». |
| V6-3 | m | JSON | Le JSON n'a que l'état v6 : les valeurs v5 (`130/131`, `56/56`, `0,9947`, `0,9921`, `1` échec), les 26 candidats et le contrôle manquent. | Ajouter l'état v5 et les 26 candidats, ou retirer ces chiffres du texte. |

### 4.6 gold-split — `85e4082b` (4 écarts)

| id | gravité | où | constat | correction |
|---|---|---|---|---|
| GS-1 | M | fiche entière | **Aucun contrôle négatif** : pas de permutation du split, pas de mélange des identifiants, pas de test de fuite. Le split est l'objet de la fiche, pas son contrôle. | Ajouter un contrôle : mélanger les identifiants, ou permuter les labels dev/test, et montrer que l'écart observé disparaît. |
| GS-2 | m | titre, § 2, JSON | `test 53/54 (0,9814)` : `53/54 = 0,98148…`, arrondi **0,9815** (le code `round` rend 0,9815). | Écrire **0,9815** (ou `0,9814` en troncature, mais le dire). |
| GS-3 | M | JSON | Le JSON ne porte **pas** l'équilibre du split qui est l'objet de la fiche : sources (`15/302/105`, `5/130/55`, `20/432/160`), langues (`277/145`, `125/65`, `402/210`), 79 spans, `106/163`, `54/76`, `160/239`, les dénominateurs `79/79`, `38/39`, `25/27`, `15/15`, le point `1,9`. | Ajouter le tableau des sources et des langues, les spans et les dénominateurs au JSON. |
| GS-4 | m | fiche et JSON | Pas de compte de portes (le commit `85e4082b` est à 183/183) ; pas de champ `portes` dans le JSON. | Ajouter `183/183` et `portes` au JSON. |

### 4.7 v7 — `69bd865e` (7 écarts)

| id | gravité | où | constat | correction |
|---|---|---|---|---|
| V7-1 | **C** | en-tête, ligne 9 | « **État courant** : commit `69bd865e` » : faux à `f908d7b0`. La v7 est l'**avant-dernière** fiche ; la courante est la v8. | Écrire « **Instantané historique** : état au commit `69bd865e` ; ne décrit pas l'état courant `f908d7b0` — voir [r1r3](rapport-pensee-r1r3.md) ». |
| V7-2 | **C** | en-tête, ligne 7 vs § 2, ligne 36, et JSON | L'en-tête dit `POS 0,7475 → 0,7603`, la table dit `0,7482 → 0,7603`, le JSON `avant.pos` vaut `0,7475`. `0,7475` est la POS de la **v4** (`392f03aa`), `0,7482` est la v6 mesurée (`2350/3141 = 0,748169`). | Mettre `0,7482` dans l'en-tête et le JSON (la table est juste). |
| V7-3 | **C** | JSON, bloc `avant` | Le bloc mélange **trois bases** : `f1 0,5130` est la v6 **612**, `tete 0,6826` est la **v5** (constante de porte), `pos 0,7475` est la **v4** ; le tableau du Markdown est la v6 **602** : `0,5164 / 0,6834 / 0,7482`. | Ramener le bloc `avant` à une base unique (602) : `f1 0,5164`, `tete 0,6834`, `pos 0,7482`, `labels 187`, `exact 187`, `couverture 0,7824`, `spans 52`. |
| V7-4 | M | § 1, correction 1 | `POS +0,0118` et `+8 labels` sont l'**effet isolé** de la règle POS (A17 : `0,7603−0,7485 = 0,0118`, `196−188 = 8`), alors que le tableau v6→v7 totalise `0,7482 → 0,7603` (+0,0121) et `187 → 196` (+9). Les deux mesures sont vraies, mais la fiche ne dit pas laquelle est laquelle. | Étiqueter « effet isolé de la règle 1 » vs « total v6→v7 ». |
| V7-5 | M | contrôle négatif | `1,67/196` (max 4, 100 tirages, graine 20261105) n'est pas reproductible avec la description : nos 100 tirages avec la même graine donnent **1,59/196** (permutation des 239 cibles, max 8) ou **1,90/196** (permutation des 196 labels, max 5). Le protocole ne dit pas si l'on permute 196 ou 239 cibles. | Publier le code exact (ensemble permuté, remise, comparaison) ou re-mesurer. |
| V7-6 | m | § 2, § 3, § 5 | « 21 REL (« qui » **12**) » et « REL « qui » (12) » : le compte des REL françaises manquantes est **8**, dont **6** commencent par « qui » (s010, s035, s061, s065, s125, s141) ; les deux autres sont « dont » (r224) et « que » (r255). Et le § 3 dit « dev/test **n'ont pas été re-mesurés** depuis la v6 (à refaire) » alors que le § 2 dit « dev/test (**re-mesurés**) : dev 133/134, test 62/62 » ; le § 5 répète « à re-mesurer ». | Écrire 6 (« qui » français) et supprimer la contradiction § 3/§ 5. |
| V7-7 | m | JSON | Le JSON n'a pas dev/test (`133/134`, `62/62`, `62/76`, trois découpages), le contrôle (`1,67/196`, max 4, p), la répartition « 6 qui / 4 SUB françaises », ni les valeurs 612 (`0,5555 / 0,7152 / 0,7581`). | Ajouter ces blocs. |

### 4.8 v8 — `f908d7b0` (8 écarts)

| id | gravité | où | constat | correction |
|---|---|---|---|---|
| V8-1 | **C** | § 1, tableau des règles ; § 2 | Le tableau annonce `R1 +15 dev, +5 test, 0 perte`, `R2 +3`, `R3a +2`, `R3c +2` (somme `+27`). La mesure v7→v8 est : **+23 labels gagnés** (22 en + 1 fr) et **7 perdus** (6 REL synthétiques fr : s032, s037, s069, s072, s115, s135 ; + r273), soit **+16 labels / +17 exacts**. En exact : **24 gains, 7 pertes** ; dev 19 gains / 4 pertes (net +15), test 5 gains / 3 pertes (net **+2**, pas +5). « 0 perte » est faux ; la somme +27 est celle du prototype **A17** (222/222), pas du code intégré (212/212). | Publier le bilan intégré par règle (gains/pertes), nommer les 7 pertes, ou étiqueter le tableau « prototype A17, marginal, non additif ». |
| V8-2 | **C** | en-tête et § 2, lignes 10 et 44-46 | « 27 spans (16 REL, 6 SUB, 5 GP), dont **17 inatteignables** » : le compte 17 est celui d'A17, mais la composition publiée (12 synthétiques + 4 GP + 1 tokenisation) est fausse. Les 27 se décomposent en **17 inatteignables** (6 REL synthétiques : s010, s035, s061, s065, s125, s141 ; 3 SUB synthétiques : s044, s112, s114 ; 4 GP du gold : s027, s146, s148, s160 ; r255 « achetée » ; r035 relative zéro ; r264 tokenisation ; r288 adverbe final), **7 régressions** (les 6 REL synthétiques ci-dessus + r273) et **3 gains A17 non intégrés** (g017, r280, r153). | Remplacer par le tableau 17 + 7 + 3 ; corriger `inevitables` et lister les 7 pertes. |
| V8-3 | M | en-tête, lignes 3-4 | Pas de **date** (le JSON l'a) ; pas de commit exact : « État courant : commit à jour (après `4ebeb683`) » au lieu de `f908d7b0`. | Ajouter `Date : 2026-11-05` et `État courant : commit f908d7b0`. |
| V8-4 | M | fiche entière | **Aucun contrôle négatif** (ni permutation, ni hasard). Le § 4 ne propose qu'un audit. | Ajouter un contrôle (permutation des cibles : `2,10/212` contre `212/212`, 100 tirages, graine 20261105, même principe que la v7) ou un candidat aléatoire. |
| V8-5 | M | § 2, tableau et puces | Les labels français passent **135 → 129 (−6)** et les anglais **61 → 83 (+22)** : le net `+16` cache un **échange de langue**, et les 27 spans restants sont majoritairement français. « Les deux langues sont parfaites (1,0/1,0) » est vrai des **taux exacts**, pas des couvertures : fr **129/151 = 0,8543**, en **83/88 = 0,9432**. « 0 perte » est faux au niveau des labels. | Écrire la régression française et les couvertures par langue (`fr 129/151`, `en 83/88`). |
| V8-6 | M | § 2, lignes 44-46 | L'énumération `12 synthétiques + 4 GP + 1 tokenisation + 1 relative zéro + 1 adverbe final + 1 couverture verbale réelle` fait **20**, pas 17 ni 27 ; elle omet les **3 SUB synthétiques** et inclut **6 régressions** dans les « 12 synthétiques ». « Verbes hors lexique » est faux pour les 6 régressions (v7 les prédisait). | Remplacer par le tableau 17/7/3 et la liste des identifiants. |
| V8-7 | M | en-tête et JSON | `F1 0,5763` et `tête 0,7316` sont des valeurs du **602** ; l'en-tête et le JSON ne portent aucune base. Sur 612 : `0,5720` / `0,7262`. | Nommer le 602 (comme la table) ou publier les deux bases. |
| V8-8 | m | JSON | Le JSON n'a **pas** `cibles` (239), ni les gains par règle, ni les catégories de spans, ni dev/test, ni `commit`/`gold`/`verdict` ; `inevitables: 17` n'est pas défini. | Enrichir le JSON (cibles, bilan des règles, 17/7/3, base). |

### 4.9 Systémique (4 écarts)

| id | gravité | où | constat | correction |
|---|---|---|---|---|
| S-1 | M | v2, v3, v4, v5, v6, gold-split, ligne 3 | Les six fiches historiques disent « ne décrit pas l'état courant **`69bd865e`** — voir **`rapport-pensee-couverture-v7`** ». À `f908d7b0`, l'état courant est `f908d7b0` et la fiche courante est la **v8**. Le pointeur est décalé d'un commit et d'une fiche. | Remplacer `69bd865e` par `f908d7b0` et le lien v7 par `rapport-pensee-r1r3.md` ; la v7 devient elle-même un instantané (V7-1). |
| S-2 | M | les 8 JSON | Aucun ne porte `commit`, `gold` (612/602), `verdict` ou `historique` ; `gold-split` n'a pas `portes` ; la v8 n'a pas `cibles` ; la v5 n'a pas `echecs` détaillé. | Ajouter ces métadonnées et les compteurs manquants. |
| S-3 | M | `reports/README.md` | Lignes **20** (7 fiches v2→v7, 23 écarts), **21** (v7 encore « courante »), **23** (`F1 0,5156 (602)`), **24** (`test 0,9814`), **25** (`F1 0,4539` sans base). La ligne **18** (v8) est juste mais incomplète (`27 spans` sans `dont 17 inatteignables`, sans base 602). Le nouveau rapport v8 n'est pas référencé. | Corriger les lignes 20, 21, 23, 24, 25 ; enrichir la 18 ; ajouter ce rapport à la liste (ou déplacer les historiques). |
| S-4 | m | `tools/pensee/autotest.py`, docstring T112 | La docstring dit « segments F1 **0,5595** (S 0,4741) » alors que l'assertion et le message sont **0,5763** (S 0,4966). | Mettre la docstring à 0,5763 / 0,4966. |

## 5. Tableaux : sommes et dénombrements

### 5.1 v2 — le tableau des corrections ne s'additionne pas

| ligne | gain crédité | total de la fiche | manque |
|---|---:|---:|---:|
| top-k strict | 88 + 45 = **133** | **141** | +8 (lexique) |
| top-k (sous-chaîne) | 134 (aucun gain crédité) | **142** | +8 (lexique) |
| top1 | 126 + 8 = **134** | **140** | +6 (segment) |
| exact | 123 + 6 + 8 = **137** | **137** | 0 |

Les totaux de la fiche sont justes ; c'est la colonne « gain » qui est incomplète (V2-3).

### 5.2 v8 — le tableau des règles ne s'additionne pas

| ligne | effet annoncé | effet intégré mesuré (exacts) |
|---|---:|---:|
| R1 | +15 dev, +5 test, 0 perte | dev 19 gains / 4 pertes (net +15) ; test 5 gains / 3 pertes (net +2) |
| R2 | +3 | 3 cas intégrés (r215, r279, r294) |
| R3a | +2 | marginal A17 ; r280 (cas A17) reste manquant |
| R3c | +2 | marginal A17 ; r245 fixé |
| **somme** | **+27** | **+24 gains / 7 pertes = +17 exacts ; +16 labels** |

Les gains/pertes de la ligne R1 sont des **exacts** ; en **labels**, le bilan est **+23 / −7** (22 en + 1 fr gagnés, 6 REL synthétiques fr + r273 perdus). Le prototype A17 atteint `222/222` (154/154 dev, 68/68 test, 17 absents) ; la v8 intégrée atteint
`212/212` (148/148 dev, 64/64 test, 27 absents). L'écart de **10 labels** = **7 régressions**
(6 REL synthétiques + r273) + **3 gains A17 non intégrés** (g017, r280, r153). La fiche présente
les gains d'A17 comme ceux du code intégré : c'est l'erreur centrale de la v8.

### 5.3 v8 — les 27 spans, décomposition vérifiée

| catégorie | effectif | identifiants |
|---|---:|---|
| **17 inatteignables** (A17) | 17 | 6 REL synthétiques (s010, s035, s061, s065, s125, s141) ; 3 SUB synthétiques (s044, s112, s114) ; 4 GP du gold (s027, s146, s148, s160) ; r255 (REL réelle) ; r035 (relative zéro) ; r264 (tokenisation `qu'il`) ; r288 (adverbe final) |
| **7 régressions v7→v8** | 7 | 6 REL synthétiques (s032, s037, s069, s072, s115, s135) + r273 (REL, adverbe final) |
| **3 gains A17 non intégrés** | 3 | g017 (SUB), r280 (REL), r153 (GP) |
| **total** | **27** | 16 REL + 6 SUB + 5 GP |

Le texte de la v8 énumère 20 cas (`12 + 4 + 1 + 1 + 1 + 1`) et en déclare 17 inatteignables ;
il omet les 3 SUB synthétiques et compte 6 régressions parmi les « 12 synthétiques ». Le compte
17 est juste, la composition ne l'est pas.

### 5.4 Les autres tableaux

- **v3** : 112/116 + 29/29 = 141 exacts ; 94 = 48 + 33 + 13 ; R2/R3/R4 : +2+1+1 = +4 exacts,
  +3 top1, +1 strict. ✅
- **v4** : 117/118 + 40/42 = 157/160 ; 79 = 48 + 21 + 10 ; 3 échecs. ✅
- **v5** : 126/127 + 60/60 = 186/187 ; 52 = 24 + 12 + 16 ; 1 échec. ✅
- **v6** : 127/127 + 60/60 = 187 ; 131 + 56 = 187 ; 126 + 61 = 187 ; 52 = 24 + 12 + 16. ✅
- **v7** : 135 + 61 = 196 labels ; 135 + 60 = 195 exacts ; 43 = 21 + 17 + 5. ✅
- **v8** : 129 + 83 = 212 labels ; 16 + 6 + 5 = 27 ; mais 135 + 61 = 196 → 129 + 83 = 212
  (le total est juste, l'échange de langues est le problème, V8-5).
- **gold-split** : 422 + 190 = 612 ; 163 + 76 = 239 ; 106 + 54 = 160 ; sources 15+302+105 =
  422, 5+130+55 = 190, 20+432+160 = 612 ; langues 277+145 = 422, 125+65 = 190, 402+210 = 612.
  ✅ (seul le taux test est arrondi, GS-2).

## 6. JSON ↔ texte

| fiche | chiffres du JSON absents du texte | chiffres du texte absents du JSON |
|---|---|---|
| v2 | aucun (les taux sont repris) | 60/63, 63/82, 111/116, 26/29, `22 = 11 + 11`, `46/57`, `139/145`, `r048/r068`, les 8 verbes anglais |
| v3 | aucun | tout le bloc A13 (43/96, 143/145, 143/239, p = 0,5, s108/s122, `exact_any`), 111/116, 112/116, 26/29, 29/29, la portée 2–3 de R1 |
| v4 | aucun | les effets intermédiaires des 7 corrections, le contrôle, les 84 spans de A12, les 38 assertions, le passif 3/3 |
| v5 | `dev.f1` 0,5091, `dev.couverture` 0,773, `test.f1` 0,5217, `test.couverture` 0,8026 | `0,8610`, les 27 échecs, les dénominateurs 126/127, 60/60, 117/118, 40/42, le contrôle |
| v6 | aucun | 130/131, 56/56 (v5), 0,9947, 0,9921, 1 échec v5, les 26 candidats, le contrôle |
| gold-split | aucun | tout l'équilibre du split (sources, langues), 79 spans, 106/163, 54/76, 160/239, les dénominateurs, le point 1,9 |
| v7 | `avant` faux (0,5130 / 0,6826 / 0,7475) ; le reste est repris | dev/test 133/134, 62/62, 62/76 ; le contrôle 1,67/196 max 4 ; `6 qui / 4 SUB` ; les valeurs 612 0,5555/0,7152/0,7581 ; le « qui 12 » (faux) |
| v8 | `inevitables: 17` (non défini) ; les taux 129/129 et 83/83 | les cibles 239, les gains par règle, « 20 des 43 », les catégories de spans (17/7/3), les 76 cibles du test, les 24 assertions, A17 ; la date du JSON n'est pas dans la fiche |

**Le déséquilibre le plus net** : la v8 a un JSON de 45 lignes pour une fiche de 73 lignes qui
introduit un tableau de règles, une décomposition de 27 spans et un échange de langues ; le JSON
ne porte que les totaux. À l'inverse, la v5 est la seule fiche dont le JSON contient des mesures
absentes du texte (F1 et couverture dev/test). La v7 est la seule dont le JSON **contredit** le
tableau (`avant`).

## 7. Contrôles négatifs

| fiche | contrôle | statut | mesure |
|---|---|---|---|
| v2 | modèle appris rejeté : 142/145 contre 137, +5, McNemar 7/2, p = 0,18, IC [−0,7 ; +7,6] ; A8 ajoute permutations et candidat aléatoire (externe) | ✅ négatif documenté (pas un contrôle de permutation dans la fiche) | — |
| v3 | complétion naïve des GV 132 (−5) ; R5 sans ADV 131 (−6) ; R3(a) 2/4 | ✅ | — |
| v4 | `1,67/196` contre `195/196` | ❌ **contrôle de la v7**, pas de la v4 (160/157) | re-mesure proposée : `1,80/160` contre `157/160` |
| v5 | `1,67/196` contre `195/196` | ❌ **contrôle de la v7**, pas de la v5 (187/186) | re-mesure proposée : `1,93/187` contre `186/187` |
| v6 | `1,67/196` contre `195/196` | ❌ **contrôle de la v7**, pas de la v6 (187/187) | re-mesure proposée : `1,95/187` contre `187/187` |
| v7 | `1,67/196` (max 4) contre `195/196` | ⚠️ présent mais **protocole non reproductible** : nos 100 tirages graine 20261105 donnent `1,59/196` (239 cibles, max 8) ou `1,90/196` (196 labels, max 5) | publier le code exact ou re-mesurer |
| v8 | aucun | ❌ | re-mesure proposée : `2,10/212` contre `212/212` |
| gold-split | aucun | ❌ | mélanger les identifiants du split et montrer que l'écart disparaît |

**Méthode des re-mesures proposées** : pour chaque fiche, on prend les labels prédits (160, 187,
187, 212), on permute les cibles gold entre ces labels (100 tirages, graine 20261105) et on compte
les accords exacts ; la moyenne est le contrôle, l'observation est l'exact de la fiche. Ces
valeurs sont **indicatives** : le protocole exact de la v7 (196 ou 239 cibles) doit être fixé
avant de remplacer `1,67/196`.

## 8. Mentions d'historique et bases 612/602

### 8.1 Mentions

| fiche | mention | commit cité | pointeur « courant » | date | statut |
|---|---|---|---|---|---|
| v2 | Instantané historique | `9d5337ce` | `69bd865e` / v7 | ✅ | ❌ pointeur décalé (S-1) |
| v3 | Instantané historique | `dcf7bc91` | `69bd865e` / v7 | ✅ | ❌ pointeur décalé ; A13 ajouté plus tard (`e1903e2d`) |
| v4 | Instantané historique | `392f03aa` | `69bd865e` / v7 | ✅ | ❌ pointeur décalé ; contrôle ajouté plus tard |
| v5 | Instantané historique | `b975011b` | `69bd865e` / v7 | ✅ | ❌ pointeur décalé ; contrôle ajouté plus tard |
| v6 | Instantané historique | `0ec6c27d` | `69bd865e` / v7 | ✅ | ❌ pointeur décalé ; contrôle ajouté plus tard |
| gold-split | Instantané historique | `85e4082b` | `69bd865e` / v7 | ✅ | ❌ pointeur décalé ; phrase de couverture corrigée plus tard |
| v7 | **État courant** | `69bd865e` | se dit courante | ✅ | ❌ faux à `f908d7b0` (V7-1) |
| v8 | **État courant** | « après `4ebeb683` » | se dit courante | **❌** | ⚠️ commit imprécis, date absente (V8-3) |

**Aucune** des huit fiches n'est donc à jour de son statut : six pointent vers `69bd865e`/v7,
la v7 se dit courante, la v8 ne nomme ni sa date ni son commit. Le commit `69bd865e` est un
ancêtre de `f908d7b0` (six commits d'écart : `8d6c318d`, `35a67bc7`, `9bf94feb`, `4ebeb683`,
`638ac8e8`, `f908d7b0`).

### 8.2 Bases

| fiche | valeurs publiées | base réelle | 612 | 602 | statut |
|---|---|---|---|---|---|
| v2 | — | — | — | — | n.c. |
| v3 | — | — | — | — | n.c. |
| v4 | F1 0,4539 ; tête 0,6432 ; avant 0,2862/0,4989 | après 602 ; avant 612 | 0,4509 / 0,6385 | 0,4539 / 0,6432 | ❌ delta mixte + base non nommée |
| v5 | F1 0,5156 ; tête 0,6826 | constantes de porte (602) | 0,5130 / 0,6785 | 0,5164 / 0,6834 | ❌ ni 612 ni 602 |
| v6 | F1 0,5130 | 612 nommé | 0,5130 | 0,5164 | ✅ |
| v7 | F1 0,5595 ; tête 0,7205 ; POS 0,7603 | 602 nommé ; en-tête/JSON POS 0,7475 | 0,5555 / 0,7152 / 0,7581 | 0,5595 / 0,7205 / 0,7603 | ⚠️ table juste, en-tête/JSON faux |
| v8 | F1 0,5763 ; tête 0,7316 | 602 (table) ; en-tête/JSON sans base | 0,5720 / 0,7262 | 0,5763 / 0,7316 | ⚠️ base non nommée hors table |
| gold-split | F1 0,4414 / 0,4719 ; tête 0,6347/0,6470 | 612 (le gold de la fiche) | oui | — | ✅ |

**Conclusion base** : 2 fiches correctes (v6, gold-split), 2 partielles (v7, v8), 2 fausses ou
muettes (v4, v5), 2 sans objet (v2, v3).

## 9. `reports/README.md`

Les huit fiches sont référencées : v8 ligne **18**, v7 ligne **21**, v6 ligne **22**, v5 ligne
**23**, gold-split ligne **24**, v4 ligne **25**, v3 ligne **33**, v2 ligne **39**. En revanche :

| ligne | contenu | problème | correction |
|---:|---|---|---|
| 18 | v8 : « exact 212/212 (1,0000), couverture 0,887, F1 0,5763 ; 27 spans » | juste, mais incomplet : pas de « dont 17 inatteignables », pas de base 602 | ajouter « 27 spans dont 17 inatteignables ; F1/tête 602 » |
| 20 | cohérence v7 : « 7 fiches v2→v7 : 23 écarts, 4 critiques » | **périmée** : c'est l'audit de `69bd865e`, avant les corrections ; la fiche v8 est arrivée ; le nouveau bilan est 8 fiches / 42 écarts | marquer « audit historique du 2026-11-05 » et ajouter ce rapport |
| 21 | v7 : « la couverture 0,8201 : POS contextuel 0,7603, F1 0,5595, exact 195/196 » | **périmée** : v7 n'est plus courante ; base 602 non dite ; POS 0,7603 est après, l'avant 0,7482 n'est pas dit | déplacer vers les historiques, ajouter « base 602 » |
| 23 | v5 : « F1 0,5156 (602) » | **fausse** : le 602 mesure 0,5164 ; 0,5156 est la constante de porte | écrire 0,5164 ou « constante 0,5156, tolérance 0,001 » |
| 24 | gold-split : « test 0,9814 » | **fausse** : 53/54 = 0,9815 | écrire 0,9815 |
| 25 | v4 : « F1 0,4539 » | incomplète : 602, pas 612 ; la fiche elle-même ne le dit pas | ajouter « (602) » ou publier 0,4509 (612) |

La section « **Les fiches courantes** » contient encore v7, v6, v5, v4, v3, v2 et gold-split,
toutes historiques : le titre est devenu un fourre-tout. La ligne 20 renvoie à l'audit v7, pas à
ce rapport. Le nouveau rapport n'est pas référencé (il ne peut pas l'être par nos soins : nous
n'écrivons que les deux fichiers de sortie).

## 10. Corrections priorisées

### P1 — chiffres de tête et statut (à corriger avant toute citation)

1. **v8, tableau des règles** : remplacer `+15 dev, +5 test, 0 perte`, `+3`, `+2`, `+2` (somme
   +27) par le bilan intégré : **24 gains, 7 pertes, +17 exacts, +16 labels** ; nommer les 7
   pertes (s032, s037, s069, s072, s115, s135, r273) et le net test **+2**. Ou étiqueter le
   tableau « prototype A17, marginal, non additif ».
2. **v8, 17 inatteignables** : remplacer la composition par le tableau **17 + 7 + 3** de § 5.3 ;
   corriger `inevitables` et lister les 7 régressions.
3. **v8, en-tête** : ajouter `Date : 2026-11-05` et `État courant : commit f908d7b0`.
4. **v7, statut** : passer en « Instantané historique ... ne décrit pas `f908d7b0` — voir r1r3 ».
5. **v7, POS** : mettre `0,7482` dans l'en-tête et le JSON (la table est juste).
6. **v7, JSON `avant`** : ramener le bloc à la v6 602 : `f1 0,5164`, `tete 0,6834`,
   `pos 0,7482`.
7. **v4, F1/tête** : choisir une base ; sur 602, `0,2895/0,5053 → 0,4539/0,6432` ; sur 612,
   `0,2862/0,4989 → 0,4509/0,6385`. Ne pas laisser `0,2862 → 0,4539`.
8. **v5, dev** : `126/126 (0,9921)` → `126/126 (1,0000)`.
9. **v2, 46** : `46` → `45`.

### P2 — contrôles négatifs

10. **v4, v5, v6** : remplacer le contrôle copié de la v7 (`1,67/196` vs `195/196`) par un
    contrôle sur leur base : `1,80/160` (v4), `1,93/187` (v5), `1,95/187` (v6), ou retirer le
    paragraphe. Ne pas laisser « le dispositif est celui de la fiche courante ».
11. **v8** : ajouter un contrôle (permutation des cibles : `2,10/212` vs `212/212`, ou candidat
    aléatoire).
12. **gold-split** : ajouter un contrôle de split (mélange des identifiants, écart qui disparaît).
13. **v7** : publier le code exact du contrôle (196 ou 239 cibles, remise, comparaison) ou
    re-mesurer ; `1,67/196` n'est pas reproductible avec la description actuelle.

### P3 — bases 612/602

14. **v4** : nommer le 602 pour F1/tête, ou publier 612 (`0,4509/0,6385`) ; corriger le § 3 qui
    dit « gold 612 ».
15. **v5** : publier `0,5164/0,6834` (602) ou dire « constante de porte 0,5156/0,6826,
    tolérance 0,001 » ; corriger le README ligne 23.
16. **v8** : nommer le 602 dans l'en-tête et le JSON, ou publier 612 (`0,5720/0,7262`).
17. **v7** : l'en-tête et le JSON à `0,7482` (V7-2) ; le tableau est déjà bon.

### P4 — JSON ↔ texte

18. **v7** : corriger le bloc `avant` et ajouter dev/test, contrôle, `6 qui / 4 SUB`, valeurs 612.
19. **v3** : ajouter le bloc A13 (`exact_any 143/145`, 143/239, 43/96, p = 0,5, s108/s122) et
    les comptes 111/116, 112/116, 26/29, 29/29.
20. **v5** : ajouter les dénominateurs et `27 = 26 + 1` ; **v6** : ajouter les valeurs v5 et les
    26 candidats ; **v2** : ajouter 60/63, 63/82, 111/116, 26/29, 22 = 11 + 11, 46/57, 139/145,
    r048/r068, les 8 verbes.
21. **v8** : ajouter `cibles: 239`, le bilan des règles, les catégories 17/7/3, la base, le
    commit ; ajouter la date à la fiche.
22. **gold-split** : ajouter le tableau des sources et des langues, 79 spans, 106/163, 54/76,
    160/239, les dénominateurs, le point 1,9.

### P5 — README et historique

23. `reports/README.md` : corriger les lignes **20, 21, 23, 24, 25** ; enrichir la **18** ;
    ajouter ce rapport ; déplacer ou marquer les fiches historiques.
24. **Six fiches historiques** : remplacer `69bd865e` par `f908d7b0` et le lien v7 par
    `rapport-pensee-r1r3.md` (S-1).
25. **v8, lien A17** : `rapport-spans-v7.md` est absent de `f908d7b0` ; le committer avec la v8
    (ou retirer le lien). Le fichier est présent dans l'arbre de travail, non suivi.

### P6 — mineurs

26. **gold-split** : `0,9814` → `0,9815` (ou dire « troncature »).
27. **v7** : « qui 12 » → « qui 6 » ; supprimer la contradiction § 3/§ 5 sur dev/test.
28. **v2** : étiqueter le split lexical ; **v5** : harmoniser « candidats manquants 27 → 26 ».
29. **autotest.py, docstring T112** : 0,5595/0,4741 → 0,5763/0,4966.

## 11. Ce qui pourrait rendre ce rapport faux

- **Les corrections en cours dans l'arbre de travail** : `rapport-pensee-couverture-v7.md` y est
  déjà modifié (en-tête 0,7482, « qui 6 », § 3 re-mesuré) ; si ces corrections sont committées,
  V7-2 et V7-6 disparaissent partiellement. Le JSON de la v7, le statut et le contrôle restent.
- **Le fichier A17 non suivi** : s'il est committé, le lien de la v8 n'est plus cassé ; le
  tableau des règles reste faux (les gains A17 ne sont pas ceux du code intégré).
- **Le protocole du contrôle v7** : si l'auteur précise la permutation (196 ou 239 cibles), la
  valeur `1,67/196` peut redevenir reproductible ; notre re-mesure ne prétend pas la remplacer.
- **La convention de base** : si la convention du dépôt est « F1/tête/POS sur le 602, couverture
  sur le 612 », alors v7 et v8 sont acceptables **à condition de l'écrire** ; v4 et v5 restent
  faux ou muets.
- **Le classement des 17 inatteignables** suit la fiche A17 (`rapport-spans-v7.md`) ; si A17
  révise sa liste, le 17/7/3 change. Les 7 pertes v7→v8, elles, sont mesurées directement.
- **Le choix de compter 42 écarts** dépend des regroupements (les dénominateurs JSON et les
  arrondis sont groupés par fiche) ; le registre du JSON fait foi.
- **Le gold** : les fichiers d'or sont identiques de `9d5337ce` à `f908d7b0` (vérifié), mais un
  ajout de phrase postérieur changerait les 239 cibles et tous les taux.

## 12. Fichiers

- [`rapport-coherence-fiches-v8.md`](rapport-coherence-fiches-v8.md) — ce rapport.
- [`pensee-coherence-fiches-v8.json`](pensee-coherence-fiches-v8.json) — le registre structuré
  (8 fiches, 42 écarts, 8 contrôles, 8 mentions, 8 bases, 6 lignes README : 5 à corriger + 1 à enrichir).
- Sources : les 8 fiches et 8 JSON à `f908d7b0` ; `tools/bloc_linguistique.py` et
  `tools/pensee/autotest.py` aux commits `9d5337ce`, `dcf7bc91`, `392f03aa`, `b975011b`,
  `0ec6c27d`, `85e4082b`, `69bd865e`, `f908d7b0` ; `evaluer_gold.py`, `gold_split.py`,
  `gold.json`, `gold_reel.json`, `gold_synthetique.json`, `gold_gele.json` ;
  `rapport-spans-v7.md` (A17) et `rapport-audit-v7.md` ; l'audit précédent
  [`rapport-coherence-fiches-v7.md`](rapport-coherence-fiches-v7.md).
- **Aucune fiche modifiée, aucun commit.** Seuls les deux fichiers de sortie sont neufs.
