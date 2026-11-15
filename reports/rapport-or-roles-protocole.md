# J4 — L'or de rôles : sept champs, deux codeurs, 144 rôles S, un or permuté

> **Ligne de roadmap** : **B13 / R0.7** · **Tâche** : X2 (J4 matin, la part du pilote) ·
> **Date** : 2026-11-15 · **Verdict** : protocole livré, **gold S non modifié**
> (SHA-256 `4cebc6d7…f8879` avant et après). Les **61 phrases / 144 rôles** du gold S se
> projettent en **117 mentions des sept champs** et **27 hors_champ** ; avec les **46 textes**
> du gold v2, la base donne **222 mentions** dont **195** dans les sept champs. Les quatre
> rôles rares n'y sont pas mesurables : `temps` 9, `destinataire` 5, `possession` 1,
> `complement` 7. Le protocole prévoit un **supplément de 60 phrases / 90 mentions** qui
> porte chaque rôle à ≥ 20 ; le kappa simulé à 90 % d'accord passe de **0,857** à **0,878**,
> et l'or permuté existant s'effondre à **0/18** sur les cinq rôles de GP. Le protocole est
> prêt pour S ; le pilote n'écrit ni dans le gold S ni dans `tools/structures/`.

**La question.** Le gold v2 (46 textes) n'annote que **trois** rôles (`agent`, `predicat`,
`lieu`) et un **cadre principal** ; le gold S (61 phrases) annote **144 rôles** en **17
étiquettes**, mais seulement **117** dans les sept champs du produit et **0** étiquette
`complement` (7 seulement par projection des GP `theme`/`instrument`/`but`). Comment
construire un or qui mesure les **sept champs** (`agent`, `predicat`, `lieu`, `temps`,
`destinataire`, `possession`, `complement`), avec **deux codeurs**, un **kappa publiable**,
les seconds cadres et les rôles hors cadre — sans toucher au gold S, et avec un **or
permuté qui tue la mesure** ?

**La réponse.** Le protocole part du gold v2 comme **graine** (46 textes, 65 variantes,
78 rôles non vides dans la première variante), re-annote les **61 phrases S en aveugle**
(sans voir les étiquettes S), ajoute **60 phrases ciblées** pour les rôles rares, et double
chaque item. Le kappa est calculé **par mention de rôle**, avec un appariement par span
exact, un bootstrap par phrase et des contrôles négatifs. Le gold n'est publiable que si
**κ ≥ 0,80** et si l'or permuté tombe sous le plafond **1/7**.

## 1. Les sources et l'inventaire

### 1.1 Le gold S — 61 phrases, 144 rôles, 17 étiquettes

[`gold-analyseur.json`](../tools/structures/donnees/gold-analyseur.json) : **61 phrases**
(7 `dev`, 16 `test`, 38 `holdout`), **144 rôles**, **144 spans exacts** (100 %), **17
étiquettes**. Les rôles par phrase : 1 rôle (5 phrases), 2 (32), 3 (21), 4 (3). Les
prédicats par phrase : 1 (56), 2 (1), 0 (4).

| étiquette | n | étiquette | n | étiquette | n |
|---|---:|---|---:|---|---:|
| `predicat` | 58 | `agent` | 34 | `temps` | 9 |
| `qualite` | 7 | `contenu` | 5 | `destinataire` | 5 |
| `patient` | 5 | `cause` | 4 | `theme` | 4 |
| `but` | 3 | `lieu` | 3 | `hypothese` | 2 |
| `concession` | 1 | `consequence` | 1 | `instrument` | 1 |
| `maniere` | 1 | `possession` | 1 | | |

La projection sur les **sept champs** est une convention, pas une vérité :

- `agent` 34, `predicat` 58, `lieu` 3, `temps` 9, `destinataire` 5, `possession` 1 ;
- `complement` **7** : les GP `theme` (4), `but` (2) et `instrument` (1) sont des
  compléments prépositionnels et tombent dans le repli ;
- **hors_champ 27** : `patient` (5, GN), `qualite` (7, REL) et les subordonnées `but` (1),
  `cause` (4), `hypothese` (2), `concession` (1), `consequence` (1), `contenu` (5),
  `maniere` (1). Ils restent dans la couche étendue et ne sont pas comptés dans le score
  des sept champs.

**117/144 = 0,8125** des rôles S sont dans les sept champs. Les **quatre phrases sans
prédicat** sont `h043`, `h052`, `h053`, `h059` (GN nus : « Une belle maison. », « La
ferme. », « Le grand lit. », « La vieille porte. ») ; `h031` a **deux prédicats** (« Il
court mais il ne rit pas. »). Ce sont les cas limites du schéma : `cadres: []` et rôles
`hors_cadre` pour les premières, deux cadres dont un principal pour `h031`.

### 1.2 Le gold v2 — 46 textes, 65 variantes, 3 rôles

[`gold_restitution_v2.json`](../tools/tests/linguistique/gold_restitution_v2.json) :
**46 textes**, **65 variantes**, 35 `fr`, 5 `en`, 5 `und`, 1 `it`. La première variante a
**138 cellules**, **78 non vides** : `agent` 32, `predicat` 39, `lieu` 7. Toutes variantes :
**195 cellules**, **115 non vides** : `agent` 48, `predicat` 58, `lieu` 9. **7 cadres sont
vides** (`f18`, `f25`, `f37`, `f39`, `f40`, `f42`, `f48`).

C'est un or de **cadre principal**, pas une annotation complète : les seconds cadres, les
subordonnées et les quatre rôles `temps`, `destinataire`, `possession`, `complement` n'y
sont **pas** annotés. Il couvre **3/7** champs ; les 65 variantes restent des lectures
acceptées, la graine ne duplique que la première. C'est la **graine**, pas le gold final.

### 1.3 La base commune — 222 mentions, 195 dans les sept champs

| rôle | gold S | gold v2 (1re variante) | base | après supplément | cible |
|---|---:|---:|---:|---:|---|
| `agent` | 34 | 32 | **66** | 66 | — |
| `predicat` | 58 | 39 | **97** | 97 | — |
| `lieu` | 3 | 7 | **10** | **20** | +10 |
| `temps` | 9 | 0 | **9** | **29** | +20 |
| `destinataire` | 5 | 0 | **5** | **25** | +20 |
| `possession` | 1 | 0 | **1** | **21** | +20 |
| `complement` | 7 | 0 | **7** | **27** | +20 |
| **sept champs** | **117** | **78** | **195** | **285** | **+90** |
| `hors_champ` | 27 | 0 | **27** | **27** | — |
| **total** | **144** | **78** | **222** | **312** | **+90** |

*Lecture* : les colonnes S et v2 sont les projections sur les sept champs ; le gold S
garde **0** étiquette `complement`, les 7 viennent des GP `theme`/`but`/`instrument`.

**Le point dur est là** : sans supplément, `possession` a **1** mention, `destinataire` 5,
`complement` 7, `temps` 9, `lieu` 10. Aucun de ces rôles n'atteint le seuil de **10
mentions positives** par rôle, et `possession` est à 1. Un F1 par rôle sur 1 ou 5 items
n'est pas publiable. Le supplément de **60 phrases / 90 mentions** (20 `temps`, 20
`destinataire`, 20 `possession`, 20 `complement`, 10 `lieu`) porte les cinq rôles à
**20–29** et fait passer le total à **312 mentions** (285 dans les sept champs + 27
`hors_champ`).

## 2. Le protocole d'annotation

### 2.1 Les champs

Un item = **une phrase** et **zéro ou plusieurs cadres**. Un cadre = **un prédicat** et ses
rôles. Chaque rôle est une **liste de mentions** (0..n), chaque mention étant un span
exact `{texte, debut, fin}` en **caractères Unicode**. Un seul cadre est `principal`.

| champ | obligatoire | contenu |
|---|---|---|
| `phrase` | oui | `id`, `texte`, `langue`, `source`, `source_id`, `split` |
| `cadre` | oui (liste, 0..n) | `id`, `principal`, `roles` |
| `roles` | oui | `agent`, `predicat`, `lieu`, `temps`, `destinataire`, `possession`, `complement` |
| `hors_cadre` | non | `role`, `mention`, `raison` : subordonnée, relative, apposition, phrase sans prédicat |
| `meta` | oui | `codeur`, `date`, `statut`, `protocole`, `a_completer`, `sha256_source` |

Le schéma JSON est [`schema-or-roles.json`](schema-or-roles.json) (Draft 2020-12). Il est
validé par [`protocole_or_roles.py`](../tools/protocole_or_roles.py) sur les **46 items** de
la graine : **0 erreur**, spans exacts vérifiés. **Contrôle négatif du schéma** : quatre
mutations (sans agent, deux cadres principaux, span faux, sans prédicat) sont refusées
**4/4**.

### 2.2 Les définitions

| rôle | définition | exemples |
|---|---|---|
| `agent` | l'entité qui fait l'action ; sujet actif ou complément d'agent d'un passif (`par`) | `Le chat`, `par Marie` |
| `predicat` | le verbe ou le GV qui porte le cadre ; auxiliaires et copule inclus | `dort`, `a été écrit` |
| `lieu` | lieu, origine, destination ou trajet | `à Paris`, `dans la cour`, `vers la gare` |
| `temps` | moment, durée ou fréquence | `à 14 h`, `demain`, `depuis dix minutes` |
| `destinataire` | bénéficiaire ou récepteur d'un transfert ou d'une communication | `à Marie`, `pour Paul`, `lui` |
| `possession` | le possesseur, pas l'objet possédé | `de la voisine`, `à moi` |
| `complement` | le repli des compléments prépositionnels qui ne sont ni lieu, ni temps, ni destinataire, ni possession ; le rôle étendu (`theme`, `moyen`, `but`) reste dans `role_etendu` | `de son projet`, `avec le télescope` |

Les règles de décision sont publiées dans le JSON (`protocole.regles_de_decision`, 27
règles) : `à` + temps / lieu / personne / infinitif ; `de` + GN (possession) / GV
(complément) ; `avec` (complément, `moyen`) ; `par` + passif (agent) / moyen ; `pour` +
bénéficiaire (destinataire) / but (complément) ; `dans`, `sur`, `vers`, `chez` (lieu) ;
`pendant`, `depuis`, `vers 9 h` (temps) ; `en` + temps / lieu / véhicule / gérondif ;
copule + `à` + pronom (possession) ; passif ; coordination ; subordonnée ; phrase sans
prédicat ; impératif sans agent ; ambiguïté.

**La couche étendue.** Les 17 étiquettes du gold S ne sont pas jetées : `role_etendu` les
conserve (`theme`, `instrument`, `but`, `patient`, `qualite`…). La couche des sept champs est
celle du **score** ; la couche étendue est celle de la **compatibilité** et de la
description. Un `theme` est un `complement` dans la couche grossière, mais il reste `theme`
dans `role_etendu` ; un `patient` est `hors_champ`, pas `complement`. Les **27 rôles S**
hors des sept champs (`patient`, `qualite`, subordonnées) seront enregistrés dans
`hors_cadre` avec `role: "hors_champ"` et leur `role_etendu` ; ils ne sont pas comptés dans
le score des sept champs.

### 2.3 Les cadres et le hors-cadre

- **Un cadre par prédicat.** `h031` (« Il court mais il ne rit pas. ») a deux cadres ; le
  premier est principal.
- **Une subordonnée avec son propre prédicat** est un second cadre ; sans rôle propre, elle
  va dans `hors_cadre` avec son étiquette étendue (`cause`, `but`, `hypothese`…).
- **Une phrase sans prédicat** a `cadres: []` ; ses GN vont dans `hors_cadre` avec
  `role: agent` (ou `hors_champ` pour un `patient`).
- **Un impératif sans agent** a un cadre avec `agent: []`.
- **Une ambiguïté** : on annote le rôle syntaxique principal et on met l'alternative dans
  `meta.note` ; elle n'entre pas dans l'or.

### 2.4 L'échantillon

| bloc | items | mentions | rôle |
|---|---:|---:|---|
| gold v2 (graine) | 46 | 78 | 3 rôles déjà annotés ; 4 à compléter |
| gold S (référence) | 61 | 144 | re-annotation en aveugle, sans voir les étiquettes S |
| supplément | 60 | 90 | 20 `temps`, 20 `destinataire`, 20 `possession`, 20 `complement`, 10 `lieu` |
| **total** | **167** | **312** | **285** dans les sept champs + **27** `hors_champ` |

Les codeurs ne voient **pas** les étiquettes du gold S ; la graine v2 est montrée **à
l'identique** aux deux codeurs ; le gold S n'est ouvert qu'**après le gel**, pour la
comparaison. Le supplément est **ciblé**, pas aléatoire : il sert au rappel par rôle et au
kappa, pas à estimer la prévalence ni une F1 générale.

### 2.5 La double annotation

1. **Calibration** : 10 items hors du gold, annotés par A et B ; si κ < 0,80, le manuel est
   révisé avant l'annotation.
2. **Annotation indépendante** : A (pilote) et B (désigné par S) annotent les **167 items**
   dans des fichiers séparés, sans discussion ni accès au fichier de l'autre.
3. **Kappa** : calculé sur les mentions appariées par span exact ; les désaccords de
   frontière sont comptés à part.
4. **Adjudication** : C (S ou un tiers) tranche tous les désaccords ; les annotations A et B
   restent dans l'audit. Un item non tranché est exclu, avec sa raison.
5. **Gel** : SHA-256, manifeste, version. Toute modification crée une nouvelle version.

**Couverture** : 100 % des 167 items, deux codeurs, soit **334 annotations**. Le coût est
d'environ **0,5 h** de schéma, **1 h** de calibration, **2 × 3 h** d'annotation, **1 h** de
kappa, **2 h** d'adjudication et **1 h** de gel.

### 2.6 Le kappa

Le kappa est celui de **Cohen** :

```
κ = (p_o − p_e) / (1 − p_e)
```

où `p_o` est l'accord observé et `p_e` l'accord attendu sous les marges des deux codeurs.
L'unité est la **mention de rôle** (8 catégories : 7 champs + `hors_champ`), appariée par
`(debut, fin)` exacts. Les mesures secondaires sont le **kappa de présence** (phrase × rôle,
présent/absent), le **taux de spans exacts** et le **taux de cadres exacts**.

- **IC** : bootstrap par phrase (cluster), 2 000 rééchantillonnages, graine `20261115`.
- **Seuils** : κ ≥ 0,80 accepté ; 0,60–0,80 adjudication puis gold accepté avec limite
  nommée ; < 0,60 manuel révisé, aucun gold, aucun score.
- **Rôles rares** : moins de 10 mentions positives = pas de F1 publiable ; on rapporte
  l'accord brut et l'effectif. Le kappa global est la porte ; les kappas par rôle sont
  descriptifs.
- **Contrôle négatif** : permuter les étiquettes de B, ou tirer B indépendamment de A, doit
  donner κ ~ 0 ; si κ_permute > 0,20, le calcul est invalide.

**L'étalonnage sous la prévalence de l'or** (simulation, pas une double annotation) :

| accord brut visé | κ base (222) | κ après supplément (312) |
|---:|---:|---:|
| 0,80 | 0,713 [0,636 ; 0,787] | 0,756 [0,704 ; 0,808] |
| 0,85 | 0,786 [0,713 ; 0,848] | **0,818** [0,770 ; 0,864] |
| 0,90 | **0,857** [0,802 ; 0,915] | **0,878** [0,836 ; 0,914] |
| 0,95 | 0,928 [0,885 ; 0,968] | 0,939 [0,906 ; 0,965] |
| indépendant | −0,001 [−0,078 ; 0,071] | 0,002 [−0,049 ; 0,051] |
| permuté | 0,002 [−0,080 ; 0,087] | −0,001 [−0,048 ; 0,050] |

**Lecture** : avec la prévalence de la base (`p_e = 0,299`), il faut **~86 % d'accord brut**
pour atteindre κ = 0,80 ; à 85 %, la base est à 0,786, juste sous le seuil. Après
supplément (`p_e = 0,180`), 85 % suffit (0,818). La base seule donne une demi-largeur
IC95 de **0,056** ; le supplément la ramène à **0,041** ; pour 0,05 il faut ~282 mentions
avec la prévalence de la base et ~206 après supplément. Le supplément n'est donc pas
cosmétique : il rend le seuil atteignable et l'IC plus étroit.

## 3. Le contrôle négatif : l'or permuté doit s'effondrer

### 3.1 Ce que la v3 mesure déjà

Les contrôles W5 sont rejoués **en lecture seule** par `tools/protocole_or_roles.py` ; le
JSON les publie avec les SHA-256.

**Gold S (144 rôles)** :

| contrôle | global | cinq rôles de GP |
|---|---:|---:|
| v3 (référence) | **144/144** | **18/18** |
| permutation des cinq | 126/144 = 0,8750 | **0/18** |
| permutation de tous (rotation 17) | **58/144 = 0,4028** | **0/18** |
| rôle constant `lieu` | 3/144 = 0,0208 | 3/18, F1 0,037 |
| constant par type (plancher) | 104/144 = 0,7222 | — |

**Gold v2 (46 textes, 77 rôles attendus)** :

| contrôle | cadres exacts | rôles justes | F1 |
|---|---:|---:|---:|
| v3 | **20/46** | **40/77** | **0,5406** |
| vide | 7/46 | 0/77 | 0,0000 |
| constant par type | 6/46 | 39/77 | 0,4382 |
| rôles mélangés | 3/46 | 0/77 | 0,0000 |
| permutation des cinq | 17/46 | 37/77 | 0,5139 |
| dont `lieu` | — | **0/6** | **0,0000** |

**Le point de méthode.** La permutation des cinq rôles de GP tue bien la cible :
**0/18** sur le gold S, **0/6** `lieu` sur le gold v2. La rotation des 17 étiquettes donne
**0,4028**, mais ce n'est **pas** un contrôle propre : le mapping contient à la fois
`predicat` et `prédicat`, et **58 prédicats** survivent par l'alias. C'est une **borne
haute**, pas une preuve. Le contrôle propre du nouveau gold est la **permutation cyclique
des sept champs** :

```
agent → predicat → lieu → temps → destinataire → possession → complement → agent
```

### 3.2 Les plafonds du nouveau gold

| contrôle | plafond | ce qui doit arriver |
|---|---:|---|
| or permuté 7 | **1/7 = 0,1429** | le score exact des sept champs tombe sous 0,1429 |
| or permuté 5 | **0,20** | 0/18 sur le gold S (déjà observé) |
| or vide | 0 | F1 = 0 (déjà observé sur le gold v2 : 0/77) |
| rôle constant | 0,05 | F1 ≤ 0,05 (déjà observé : 0,037) |
| kappa permuté | **0,20** | κ ~ 0 (simulation : −0,001 à 0,002) |

Si l'or permuté dépasse le plafond, la mesure **fuit** : elle ne dépend pas de
l'affectation des rôles. Dans ce cas, on publie l'échec, on ne baisse pas le plafond.

## 4. Ce qui pourrait rendre cette fiche fausse

- **Le gold S n'est pas une validation humaine indépendante** : 61 phrases, 144 rôles,
  écrites par la même famille de règles, avant la v3 ; un or aveugle donnerait moins.
- **Le gold v2 est un or de cadre principal** : 46 textes, 65 variantes, 3 rôles ; les
  seconds cadres et les rôles hors cadre n'y sont pas annotés.
- **La projection des 17 étiquettes S sur les 7 champs est une convention** : `theme`,
  `instrument` et `but` prépositionnels tombent dans `complement` ; `patient`, `qualite`
  et les subordonnées restent `hors_champ`. Une autre convention changerait les effectifs.
- **Le supplément est ciblé, pas aléatoire** : il sert au rappel par rôle et au kappa, pas
  à estimer la prévalence ni une F1 générale.
- **Les deux codeurs partagent le même manuel et la même formation** : le kappa mesure la
  cohérence, pas la vérité.
- **Les rôles rares gardent un kappa instable** : `possession` 21 mentions, `complement`
  27 après supplément ; le kappa global est la porte, les kappas par rôle sont descriptifs.
- **La base de 107 items est petite** : 222 mentions avant supplément, 312 après ; les IC
  par rôle restent larges.
- **La rotation des 17 étiquettes n'est pas un contrôle propre** : l'alias
  `predicat`/`prédicat` laisse 58 prédicats fixes ; le contrôle propre est la permutation
  des cinq rôles de GP (0/18) et la permutation cyclique des sept champs.
- **Le schéma ne vérifie pas l'égalité span/texte** : c'est le script et le validateur qui
  le font ; un span faux est refusé, pas corrigé.
- **Le pilote ne modifie pas le gold S** : si S change ses étiquettes, la comparaison et
  les 144 rôles doivent être rejoués, et le SHA-256 publié.

## 5. La décision et la suite

**Pour S.** Valider le schéma, désigner B, calibrer, annoter les **167 items**, adjudiquer,
geler avec un SHA-256, calculer le kappa et publier le contrôle permuté. **Le pilote ne
touche ni au gold S ni à `tools/structures/`.**

**Ce que ce n'est pas.** Pas un gold : la graine de 46 textes est `provisoire`, les quatre
rôles absents de la v2 sont vides, les 61 phrases S ne sont pas re-annotées ici. C'est un
**contrat** (champs, définitions, échantillon, double annotation, kappa, plafonds).

**La prochaine action.** S reprend ; le pilote peut étendre la graine aux quatre rôles
manquants sur les 46 textes (hors gold) et préparer les 60 phrases du supplément.

## 6. Fichiers

[`schema-or-roles.json`](schema-or-roles.json) (Draft 2020-12, 46 items validés) ·
[`or-roles-base-v1.json`](or-roles-base-v1.json) (graine provisoire, 46 textes) ·
[`rapport-or-roles-protocole.json`](rapport-or-roles-protocole.json) (inventaire,
protocole, simulations, contrôles, SHA-256) · [`protocole_or_roles.py`](../tools/protocole_or_roles.py)
(script reproductible, lecture seule du gold S) · [`gold-analyseur.json`](../tools/structures/donnees/gold-analyseur.json)
(gold S, lecture seule) · [`gold_restitution_v2.json`](../tools/tests/linguistique/gold_restitution_v2.json)
(gold v2, base de départ) · [`rapport-restitution-v3.md`](rapport-restitution-v3.md) (W5).
