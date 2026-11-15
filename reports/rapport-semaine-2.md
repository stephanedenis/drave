# W6 — le rapport de la semaine 2 : le tagger gagne sur les deux bases, Panini reste bloqué, la restitution sépare sans fidélité

> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** (le produit) / **L** (le bloc langue) ·
> **Tâche** : **W6** (J5 après-midi, la clôture) · **Date** : 2026-11-15 (J5 · 20/11) ·
> **HEAD mesuré** : `93e046f7` (W4) puis `73edb3dd` (W5) · **Verdict** : **cinq vagues mesurées,
> trois positives, une bloquée, une mixte** ; le tag annoté `semaine-2-2026-11-20` est posé sur
> le dernier commit de code vert (`73edb3dd`, W5) ; **aucune passe complète n'a été relancée**
> pour la clôture — le relevé lit `work/portes/` et un ciblage de neuf portes.
>
> **JSON** : [`rapport-semaine-2.json`](rapport-semaine-2.json) · **Fiches** :
> [W1](rapport-gold-452.md), [W2](rapport-tagger-h50.md), [W3](rapport-tagger-defaut.md),
> [W4](rapport-panini-manifeste.md), [W5](rapport-restitution-v3.md) · **Portes** :
> `work/portes-1115-09h53/registre.txt`, `work/portes/w6-ciblage/`, `work/portes/w6-ciblage2/`.

**En trois lignes.** (1) **W1** nomme et compose le **gold réel 452** (20 hand + 432 corpus,
242 fr / 210 en), fige le split **402 / H50** et liste **10 GP/SUB** à annoter (184 → **194**
cibles), sans toucher au gold. (2) **W2** mesure le tagger POS sur les deux bases : **402
0,9198 → 0,9643** (**+4,45**), **H50 0,6842 → 0,8607** (**+17,65**), F1 et attachement du 402
inchangés ; **W3** fixe la matrice du défaut : **hors ligne, code 0, 0 socket**, `--tagger`
**opt-in**, clé invalide **code 4**, réseau coupé **code 0** après **3 essais**, **1 000 phrases
= 143 870 tokens / ~0,031 $**. (3) **W4** livre le manifeste Panini mais **ne teste pas** : **27/60**
paires, calibration **42/44**, **3** sources courtes, **5** groupes de doublons, contrôle **N5
vide** ; **W5** sépare les cinq rôles (**24/24**, gold S **144/144**, **18/18**, permutation
**0/18**) mais le produit ne suit pas (**20/46** contre 19/46, F1 **0,5406** contre 0,5270).

**Ce que ce rapport est, et n'est pas.**

- **Est** : la **synthèse de la semaine 2** — les chiffres avant/après de chaque vague, les
  **contrôles négatifs**, les **décisions**, le **relevé des portes** et l'état du **tag**. Chaque
  chiffre renvoie à sa fiche ; aucune mesure nouvelle n'est produite ici.
- **N'est pas** : une nouvelle passe complète (elle n'a **pas** été relancée : le relevé lit les
  journaux existants et un ciblage), ni une annotation du gold (le gold est à **S**), ni un test
  Panini (les 27 paires disponibles ne sont pas l'échantillon), ni une généralisation du tagger
  (H50 est un stress test circulaire).
- **Public** : la clôture de la semaine, la reprise du 21–22/11, et toute session qui reprend
  `en-cours.md`.

## 1. Les cinq vagues, en une table

| vague | tâche | avant | **après** | delta | contrôle négatif | verdict | fiche |
|---|---|---|---|---|---|---|---|
| **W1** | le gold réel 452 et le split 402/H50 | libellé « gold 200+ » (**18** occurrences), pas de split, **184** cibles | **452** phrases (**20** hand + **432** corpus ; **242** fr / **210** en), split **402/H50**, **184 → 194** cibles, sha256 **identique** | **+10** cibles proposées, **0** phrase ajoutée | tirage `20261116` : POS **88,13 %** contre H50 **68,42 %** ; H50 ∩ 402 = **0**, union = **452** | ✅ nommé et figé | [W1](rapport-gold-452.md) |
| **W2** | le tagger POS sur 402 / H50 | 402 **0,9198** · H50 **0,6842** · total **0,8891** | 402 **0,9643** · H50 **0,8607** · total **0,9508** | **+4,45** · **+17,65** · **+6,17** | F1 et attachement 402 **inchangés** ; fermé 402 **−1,55** ; H50 **circulaire** | ✅ avec réserve | [W2](rapport-tagger-h50.md) |
| **W3** | la matrice du tagger et le défaut | 4 cas d'erreur E2 ; défaut non matricé | défaut **code 0 / 0 socket** ; `--tagger` **code 4** sans clé ou clé refusée ; réseau coupé **code 0** (3 essais) ; **143 870** tokens / **989** requêtes / **981,9 s** / **~0,031 $** pour 1 000 phrases | matrice **9** lignes, **21/21** tests | socket piégée ; mutation 401/403 ; cache chaud **0** token ; coût **extrapolé** | ✅ décision : statu quo | [W3](rapport-tagger-defaut.md) |
| **W4** | Panini : le manifeste des 26 signatures et le rejeu | **33/59** textes signés ; **60** paires ; pas de manifeste | **26** textes à signer (dont **1** des 655 paires), commande et format ; rejeu **27/60** ; calibration **42/44** ; **3** sources courtes ; **5** groupes de doublons | **27/60** paires décrites, **33** manquantes | **N2** dates permutées G2 p=**0,252** ; **N3** G3 p=**0,001** (tiré par une paire non calibrée) ; **N4** signatures permutées ; **N5** colonnes **vide** ; **N6** doublons | ❌ **bloqué** (incomplet, aucune p-value) | [W4](rapport-panini-manifeste.md) |
| **W5** | la restitution v3 : les rôles des GP | gold v2 **19/46** (16 non vides), F1 **0,5270**, `lieu` F1 **0,40** ; gold S **139/144** (17/18 cinq rôles) | gold v2 **20/46** (17 non vides), F1 **0,5406**, `lieu` F1 **0,60** ; gold S **144/144** (18/18 cinq rôles) ; séparation **24/24** | +1 cadre, +0,0136 F1, +0,20 `lieu`, +5 rôles | permutation cinq **0/18** ; tous **0,4028** ; rôle constant **3/18** (0,0208) | ✅ séparation / ❌ produit | [W5](rapport-restitution-v3.md) |

**Lecture.** Trois vagues changent un chiffre de production (W2, W3, W5) ; W1 change la **base**
et le **nom** ; W4 ne change **rien** chez Panini et le dit. Le mot de la semaine n'est pas
« gain » : c'est **base nommée, règle mesurée, test bloqué, séparation sans fidélité**.

## 2. Les chiffres, vague par vague

### 2.1 W1 — le gold réel 452, nommé, composé, tenu à l'écart

**La composition.** **452** = **20 hand** (`gold.json`) + **432 corpus** (`gold_reel.json`) ;
**242 fr + 210 en** ; **2 480 tokens**, **1 501 segments**, **184 cibles** (GP 72 + REL 58 +
SUB 54). Le corpus pèse **95,8 %** des tokens et **171** cibles ; le hand pèse **105** tokens et
**13** cibles. **10 segments GP/SUB** n'ont pas de cible (**9 GP + 1 SUB**) : **4 dans H50**,
**6 dans 402** ; le dénominateur passerait de **184 à 194** si S les annote.

**Le split.** **402 / H50** : H50 = **50** phrases (**2 hand + 48 corpus**, **25 fr + 25 en**,
**323 tokens**, **190 segments**, **22 cibles**), sélectionnées par le score d'erreur de
l'heuristique (`3 × attachement + 2 × POS + 1 × segment absent`), **sans aléa**. Le manifeste
sha256 des 50 ids est `1615c17a…b575d970`. La partition est vérifiée : H50 ∩ 402 = **0**,
union = **452**, aucun id dupliqué. La graine `20261116` ne sert **pas** à tirer H50 : elle fixe
le contrôle aléatoire et le manifeste ; ce tirage donne **88,13 %** de POS, contre **68,42 %**
pour H50 — la preuve que H50 est un **lot dur**, pas un échantillon.

**Le sha256.** `gold.json` = `3663be6c…e2e58a` ; `gold_reel.json` = `05d4f6df…1ff11` ;
concaténation ordonnée = `cff6b6d7…e90ac5`. Avant = après ; `git diff` des deux golds **vide**.
Le libellé « gold 200+ » passe de **18** occurrences à **0** dans `docs/`.

**Le négatif et la limite.** H50 est **circulaire par construction** : il ne mesure pas la
généralisation. Les 10 cibles sont des **propositions** ; S valide ou corrige. H50 ne devient un
**test** que quand S a validé les 50 phrases et les 4 cibles de H50.

### 2.2 W2 — le tagger POS sur 402 / H50 : il gagne sur les deux, le fermé paie

| base | POS heuristique | POS tagger | delta | F1 | attachement |
|---|---:|---:|---:|---:|---:|
| **402** | 0,9198 | **0,9643** | **+4,45** | 0,8190 → 0,8190 | 1,0000 → 1,0000 |
| **H50** | 0,6842 | **0,8607** | **+17,65** | 0,5836 → 0,5836 | 0,9545 → 0,9545 |
| **total 452** | 0,8891 | **0,9508** | **+6,17** | 0,7906 → 0,7906 | 0,9946 → 0,9946 |

**Le détail fermé / ouvert.** Sur 402, le gain est **ouvert** (+10,64 pts) et le **fermé baisse**
(**−1,55 pt** : 0,9580 → 0,9425). Sur H50, les deux montent (fermé +6,14, ouvert +31,95). Le
tagger ne remplace **que** le POS : F1 et attachement du 402 sont **inchangés**, ce qui est le
contrôle de non-régression.

**Le coût.** **447** requêtes, **65 029** tokens réseau, **443,813 s** de réseau pour **452**
phrases, soit **~144 tokens** et **~0,98 s** par phrase ; le cache chaud après API rejoue à
**0 réseau / 0 token**.

**La règle et le négatif.** La règle « une règle qui ne gagne que sur H50 est rejetée » ne
rejette pas le tagger : il gagne **+4,45** sur 402. Mais la **réserve du fermé** est nommée : une
règle qui exigerait la non-régression du fermé **rejetterait** le tagger tel quel. H50 reste
**circulaire** ; le gain sur H50 n'est pas une généralisation.

### 2.3 W3 — la matrice du tagger : le défaut reste hors ligne, `--tagger` est la seule porte à code 4

| cas | code | ce qui est mesuré |
|---|---:|---|
| défaut, sans clé, `analyser` / `evaluer` | **0** | heuristique, `source=heuristique`, aucun `tagger` |
| défaut, `socket.socket` piégé | **0** | aucune socket construite, `tools.llm.deepseek` non importé |
| avec clé | **0** | POS neuronal, **130** tokens, **1,156 s** pour une phrase |
| clé invalide (HTTP 401) | **4** | `stdout` vide ; `--tagger` est la seule porte qui sort 4 |
| réseau coupé (`127.0.0.1:9`) | **0** | **3** essais, repli heuristique explicite, cause dans `refus` |
| réponse du modèle non conforme | **0** | repli heuristique (test, transport factice) |

**Le coût pour 1 000 phrases.** **143 870** tokens (**122 947** entrée + **20 923** sortie),
**989** requêtes, **981,9 s** de réseau, **~0,031 $** hors pointe / **~0,062 $** en pointe, sur
le tarif `deepseek-flash` du 2026-11-13. C'est une **extrapolation linéaire** de la mesure W2 sur
452 phrases, pas un run réel de 1 000 phrases.

**La décision.** Garder le **défaut hors ligne**, `--tagger` **opt-in**, **pas de `auto`**
maintenant ; si `auto` vient, **seulement si la clé existe** et **sans changer le code de sortie**.
**21/21** tests. Le négatif : le coût est extrapolé, le dollar dépend du tarif du jour, et le
repli réseau **code 0** peut masquer une dégradation silencieuse.

### 2.4 W4 — Panini : le manifeste est prêt, le test n'est pas fait

**Le manifeste.** **59** textes, **60** paires ; **33** textes ont déjà une signature V14,
**26** n'en ont pas (dont **un seul** des 655 paires : `zadeh_1965`). La commande
[`tools/panini_signatures_26.py`](../tools/panini_signatures_26.py) calibre sur **44** œuvres et
signe les **26** ; le format attendu est **14 clés, somme 1**. Un seul vecteur est déjà disponible
(`qiwulun`) : **21** vecteurs distincts, **20** nouveaux. **3** sources font **< 300 mots**
(`epicurus_letters`, `sextus_pyrrho`, `zadeh_1965`) ; **5** groupes de doublons parmi les 26
(le JSON en liste **6**, dont une paire déjà signée).

**Le rejeu.** **27/60** paires calculées (**1 G1, 14 G2, 12 G3**) ; **33** manquantes. Aucune
**p-value de H0** n'est écrite. La calibration échoue sur **2/44** œuvres (`bengio_2003`,
`mengzi`) : `cos` 0,9678 et 0,9891, sous le seuil 0,99. Le contrôle **N2** (dates permutées G2)
donne p=**0,252** ; **N3** (dates permutées G3) p=**0,001**, mais il est **tiré par une paire
dont l'œuvre n'est pas calibrée** ; **N4** (signatures permutées) ne reproduit pas la pente de
date ; **N5** (colonnes permutées) est **vide par isométrie** ; **N6** (doublons exclus) laisse
les conclusions stables.

**La décision.** Statut **incomplet** : on ne teste **pas** les 27 paires choisies par
disponibilité. Le manifeste et la commande sont le livrable ; les 26 signatures restent à
recevoir. Aucune écriture dans Panini (statut git identique avant/après).

### 2.5 W5 — la restitution v3 : les cinq rôles se séparent, le cadre ne suit pas

**La règle.** `_role_gp` lit la préposition **et son contexte** : `à` + lieu / temps /
destinataire, `de` + possession ou thème, `avec` + moyen, `par` + agent passif ou moyen, `en` +
temps / lieu / moyen / manière. **24/24** cas de séparation.

| mesure | v2 | **v3** | delta |
|---|---:|---:|---:|
| gold v2, cadres exacts | 19/46 | **20/46** | **+1** |
| gold v2, cadres non vides exacts | 16/46 | **17/46** | **+1** |
| gold v2, F1 rôles | 0,5270 | **0,5406** | **+0,0136** |
| gold v2, `lieu` F1 | 0,40 | **0,60** | **+0,20** |
| gold v2, `agent` / `prédicat` F1 | 0,60 / 0,4872 | 0,60 / 0,4872 | **0** |
| gold S, rôles | 139/144 | **144/144** | **+5** |
| gold S, cinq rôles | 17/18 | **18/18** | **+1** |
| séparation | — | **24/24** | — |

**Le découpage, et ce qu'il retire au 144/144.** Le gold S gagne **+4 rôles** et **+1
appariement** par le découpage : le **144/144 n'est pas un gain de rôles seul**. Les cinq rôles de
la tâche sont **18/18** (lieu 3, temps 9, destinataire 5, possession 1, complément 0).

**Les contrôles négatifs.** Permutation des cinq rôles : **0/18** (le global reste 126/144 parce
que les autres rôles ne bougent pas). Permutation de tous les rôles : **0,4028** global. Rôle
constant `lieu` : **3/18**, **0,0208** global. Le codec 46/46 est un **invariant**, pas une
fidélité.

**La décision.** `--roles-v3` est **opt-in** ; `--roles` reste la **v2** inchangée. Le gold v2
n'annote que `agent`, `prédicat` et `lieu` : la prochaine mesure est **J4 — l'or de rôles**
(seconds cadres, rôles hors cadre). Le goulot est la **segmentation et le choix du cadre**, pas
la préposition.

## 3. Les négatifs de la semaine

| # | négatif | ce qu'il tue | où il est écrit |
|---|---|---|---|
| **N1** | H50 est sélectionné sur les erreurs de l'heuristique | toute lecture de H50 comme **généralisation** ; le +17,65 n'est pas un gain réel | [W1](rapport-gold-452.md) § 2.5, [W2](rapport-tagger-h50.md) |
| **N2** | sur 402, le POS **fermé** baisse de **1,55 pt** | la lecture « le tagger gagne partout » ; une règle qui exige le fermé le rejette | [W2](rapport-tagger-h50.md) |
| **N3** | le coût de 1 000 phrases est **extrapolé** | le chiffre comme mesure d'un run réel ; le dollar comme constante | [W3](rapport-tagger-defaut.md) |
| **N4** | Panini : **27/60**, calibration **42/44**, **3** sources courtes, **5** doublons | le test H0 ; aucune p-value n'est écrite | [W4](rapport-panini-manifeste.md) |
| **N5** | le contrôle « colonnes permutées » est **vide par isométrie** | la preuve que le contrôle N5 protège quoi que ce soit | [W4](rapport-panini-manifeste.md) |
| **N6** | le gold v2 ne gagne **qu'un cadre** (20/46) | la lecture « la v3 comprend les rôles » ; la fidélité du cadre ne suit pas | [W5](rapport-restitution-v3.md) |
| **N7** | le 144/144 du gold S inclut **+4 rôles et +1 appariement** de découpage | la lecture « le 144/144 est un gain de rôles seul » | [W5](rapport-restitution-v3.md) |

**Le négatif n'est pas un échec de la semaine.** W4 est **bloqué** et le dit ; W5 est **positif
sur la règle, négatif sur le produit** ; W2 porte sa **réserve fermée**. Les trois sont des
résultats au sens de la règle : chiffre, dispositif, contrôle, limite.

## 4. Les décisions

| # | décision | preuve | état |
|---|---|---|---|
| **D1** | le gold réel **452** est nommé ; le split **402/H50** est figé ; on n'ajoute **pas** de phrases, on annote **10 cibles** | W1 : 452 = 20 + 432 ; 184 → 194 ; sha256 identique | ✅ appliquée (W1) |
| **D2** | le tagger est **accepté** sur le 402, avec la **réserve du fermé** | W2 : 402 +4,45 ; F1/att inchangés ; fermé −1,55 | ✅ appliquée (W2) |
| **D3** | le **défaut reste hors ligne** ; `--tagger` est **opt-in** ; **pas de `auto`** maintenant | W3 : code 0 / 0 socket ; clé invalide 4 ; réseau coupé 0 | ✅ appliquée (W3) |
| **D4** | Panini reste **incomplet** : **aucune p-value**, on envoie le manifeste | W4 : 27/60 ; calibration 42/44 ; N5 vide | ✅ appliquée (W4) |
| **D5** | la restitution v3 est **opt-in** (`--roles-v3`) ; la v2 reste le défaut ; **J4 — l'or de rôles** suit | W5 : 20/46 ; gold S 144/144 ; permutation 0/18 | ✅ appliquée (W5) |
| **D6** | la clôture **ne relance pas** la passe complète ; le tag est posé sur le **dernier commit de code vert** (`73edb3dd`) | W6 : relevé `work/portes/` + ciblage 9/9 après heartbeat | ✅ appliquée (W6) |

**Ce que la semaine ne décide pas.** Elle ne livre **pas** `auto` ; elle ne teste **pas** Panini ;
elle ne migre **pas** la page `/` de S ; elle ne fait **pas** J4 (l'or de rôles) ni la recette
`/` (J4 après-midi) — ces deux lignes restent **nommées** et passent à la réserve / à la semaine
suivante.

## 5. Le relevé des portes

**La règle.** Le verdict se lit au **code de sortie** (`awk '$2 != 0'`), jamais au marqueur.
**Aucune passe complète n'a été relancée** pour W6 : on lit les journaux durables et on cible
les portes du diff.

| passe | portes | vertes | rouges | lecture |
|---|---:|---:|---|---|
| **`work/portes/passe-1402-02h00`** (14/11 02 h 00) | 84 | **81** | `indice`, `melange`, `sessions` | dernière passe complète **avant** la semaine 2 ; `sessions` revérifiée verte le 14/11 06 h 55 |
| **`work/portes-1115-09h53`** (15/11 09 h 53 → 12 h 15) | **85** | **81** | `indice` (1149 s), `melange` (137 s), `sessions` (heartbeat), `prechargement` (258 s) | **dernière passe complète** ; `sessions` **réparée** (heartbeat rafraîchi, revérifiée verte) ; `prechargement` **environnementale** (deux passes en parallèle : le bras `fils` à 20,5 s contre 16,4 s, PPL identique 799,8557 ; verte le 14/11 à 181 s) |
| **`work/portes-w5`** (15/11 11 h 21, `DELAI=600`) | 29/85 au moment de la lecture | — | `greffe` **124** | passe **non concluante** : la borne 600 s coupe `greffe` (780 s verte le 14/11) ; **124 = délai, pas régression** ; elle tourne encore, elle n'est pas le verdict |
| **`work/portes/w6-ciblage`** (W6) | 9 | **8** | `sessions` | `sessions` rouge sur heartbeat **périmé** (162 min), pas sur le code |
| **`work/portes/w6-ciblage2`** (W6, après heartbeat) | 2 | **2** | — | `porte-etat` et `porte-sessions` **vertes** |
| **`work/portes/w6-final`** (W6, après commit) | 9 | **9** | — | ciblage final sur le commit de clôture : **9/9** |

**Les rouges nommées.** `indice` et `melange` restent **structurelles** (l'indice extérieur tombe
à 482 jetons contre 459 pour le témoin ; l'état de A ne rend pas son code) ; ce sont les deux
rouges **tolérées** de la référence. `sessions` est une **rouge de liveness** : le heartbeat de
`e181ce02` était à 09 h 30, il est rafraîchi à **12 h 20** et la porte repasse **verte**.
`prechargement` est **environnementale** : deux passes complètes tournaient en parallèle ; la
perplexité est identique dans les quatre bras et la porte était verte le 14/11.

**Le ciblage W6.** 9 portes : `etat`, `document`, `tableaux`, `bloc-linguistique`, `bloc-tableaux`,
`lecteur`, `lecture`, `registre`, `sessions` ; **8 vertes / 1 rouge** (`sessions`), puis **9/9**
après le heartbeat (`w6-ciblage2`, `porte-etat` + `porte-sessions`), et **9/9** sur le commit de
clôture (`w6-final`). `revue_documentation.py` passe :
**753** fiches, **846** JSON, **124** docs, **85** portes, **8** chapitres.

**Le tag.** `semaine-2-2026-11-20` est **annoté** et posé sur `73edb3dd` (W5), le **dernier
commit de code vert** ; le commit de clôture W6 vient après. C'est la convention du dépôt (le tag
`chantier-2026-11-14` est sur `0e75f101`, pas sur le commit de clôture) : un lecteur qui cherche
le rapport dans le tag ne le trouvera pas — la limite est **nommée**.

## 6. L'état, le tag et ce qui reste

**L'état.** `master` = `s/v7` ; les cinq vagues sont committées : W1 `4dbeff45`, W2 `1683c2b4`,
W3 `be3f41ad`, W4 `93e046f7`, W5 `73edb3dd`. Le tag annoté `semaine-2-2026-11-20` pointe sur
W5. Les compteurs de l'état sont à jour (753 fiches / 846 JSON / 124 docs / 85 portes).

**Ce que la semaine a produit, en une phrase.** Le **tagger** gagne **+4,45** sur 402 et
**+17,65** sur H50, avec le fermé 402 qui paie **−1,55** ; le **défaut** reste hors ligne et
`--tagger` est la seule porte à code 4 ; **Panini** est **bloqué** à **27/60** et **42/44**, sans
p-value ; la **restitution v3** sépare les cinq rôles (**24/24**, **18/18**) mais ne gagne qu'un
cadre (**20/46**) ; le **gold 452** est nommé et son split est figé.

**Ce qui reste, et qui prend la suite.**

1. **J4 — l'or de rôles** (seconds cadres, rôles hors cadre) : le gold v2 n'annote que trois
   rôles ; c'est la prochaine mesure de B13.
2. **La page `/` de S** : décision et recette (106 conservés / 41 à re-juger) ; S est en pause,
   la ligne reste **bloquée** et **nommée**.
3. **Panini** : les **26 signatures** V14 ; ensuite seulement le test à date contrôlée. Le
   manifeste et la commande sont prêts.
4. **Le tagger** : `auto` n'est **pas** livré ; le coût de 1 000 phrases est une **extrapolation** ;
   la réserve du fermé 402 reste ouverte.
5. **N2 / N4 / A6.2** : hors périmètre de la semaine ; aucun GPU réservé.

## 7. Limites et ce qui pourrait rendre ce rapport faux

- **Pas de passe complète le 15/11 après W5.** Le ciblage couvre le diff (état, document,
  tableaux, bloc linguistique, lecteur, lecture, registre, sessions) et les tests, pas les 85
  portes. Un changement de code ou de données après 12 h 20 ne serait pas couvert.
- **Le tag est sur W5, pas sur le commit de clôture.** Un lecteur qui cherche le rapport dans le
  tag ne le trouvera pas.
- **`prechargement` est rouge au moment de la passe** ; on l'attribue à la charge (deux passes en
  parallèle) parce que la PPL est identique et que la porte était verte le 14/11. Si elle reste
  rouge à la prochaine passe **seule**, c'est une régression, pas un artefact.
- **W4 n'est pas un test** : les 27 paires sont choisies par disponibilité ; la calibration
  échoue sur 2/44 ; 3 sources sont courtes ; 5 groupes sont des doublons. Aucune p-value ne doit
  être lue dans ce rapport.
- **W5 ne mesure que 46 textes** pour le gold v2 (trois rôles) et 61 phrases / 144 rôles pour le
  gold S ; le 144/144 inclut un gain de découpage. Un autre or, annoté autrement, peut changer
  les chiffres.
- **W2/W3 : H50 est circulaire** ; le tagger est un run API unique, non déterministe au bit près ;
  le coût de 1 000 phrases est une extrapolation linéaire.
- **Les dates.** Les cinq vagues ont été exécutées le **15/11**, pas aux dates du plan (16 → 20/11) ;
  le tag porte la date **cible** `2026-11-20`. J4 et J5 matin (or de rôles, recette `/`, décision
  du tagger) n'ont **pas** été ouverts comme vagues ; D3 applique la recommandation W3, J4 reste
  à faire.

## 8. Les fichiers

| quoi | chemin |
|---|---|
| ce rapport | `reports/rapport-semaine-2.md` |
| son JSON | `reports/rapport-semaine-2.json` |
| W1 | `reports/rapport-gold-452.md` · `reports/rapport-gold-452.json` |
| W2 | `reports/rapport-tagger-h50.md` · `reports/rapport-tagger-h50.json` |
| W3 | `reports/rapport-tagger-defaut.md` · `reports/rapport-tagger-defaut.json` |
| W4 | `reports/rapport-panini-manifeste.md` · `reports/panini-manifeste.json` |
| W5 | `reports/rapport-restitution-v3.md` · `reports/pensee-restitution-v3.json` |
| portes | `work/portes-1115-09h53/registre.txt` · `work/portes/w6-ciblage/` · `work/portes/w6-ciblage2/` |
| état | `docs/pilotage/en-cours.md` · `docs/pilotage/semaine-2.md` · `docs/pilotage/references-non-regression.md` |
