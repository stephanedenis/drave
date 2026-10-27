# Rapport — cohérence de la documentation, troisième passage

> **Objet.** Auditer la cohérence **doc ↔ doc** de Drave, appliquer les corrections, et outiller la
> revue pour que les contradictions ne reviennent pas. Le premier passage (30/09) comparait les
> documents au **code** ; celui-ci compare les documents **entre eux** et aux fichiers du disque.
>
> **Verdict.** Les compteurs divergents sont ramenés à une **source unique** ; **39 chemins morts**,
> **3 libellés trompeurs** et **4 documents orphelins** sont corrigés ; **B10–B12** entrent dans les
> cartes ; les **portes documentaires sont vertes**. La **passe complète des 49 portes** reste à
> faire sur un arbre propre : le chantier B12 écrivait encore (5 commits entre 09:49 et 10:41,
> 1 401 lignes non commitées à 10:51).
>
> **Date réelle.** 2026-10-27 11:40 HAE. Commit de référence : `b271db7a`.
>
> **Ce qui pourrait le rendre faux.** Les compteurs de `reports/` bougent à chaque fiche B12 ; la
> revue vérifie des **invariants** (liens, chemins, compteurs), pas la **vérité sémantique** d'une
> affirmation ; le titre extrait par `tools/index_reports.py` n'est pas un verdict ; et la passe
> complète des portes n'a **pas** été relancée (voir § 6).

## 1. Le constat

L'audit du 27/10 a trouvé trois familles de défauts.

**a. Des compteurs divergents.** Le même invariant avait jusqu'à cinq valeurs selon le document :

| invariant | valeurs rencontrées | valeur vérifiée |
|---|---|---|
| portes | 27 / 34 / 46 / 47 / **49** | **49** (47 vertes, 2 structurelles) |
| chapitres de synthèse | 6 / 7 / **8** | **8** |
| fichiers `reports/` | 60 / 164 / 170 / 172 / **179** | **179** au 27/10 12:00 |
| JSON de résultats | 236 / 241 / **242** | **242** |
| documents `docs/` | 18 / **52** | **52** hors archive |
| durée d'une passe | 60 / 85 / 90 / 97 min / **1 h 34** | **1 h 34** |
| mesures B4 | 5 / **6** | **6** (le LoRA) |
| fiche `07` | 67 mesures / 150 Ko / **168 / 10 parties** | **168 mesures, 10 parties** |

**b. Des chemins et des libellés périmés.** **39 références en prose** ne résolvaient plus (dont 18
dans `docs/etat.md`), **3 liens** annonçaient `docs/...` en pointant `docs/archive/...`, et
**4 documents** n'avaient aucun lien entrant : `configuration-nvme-raid-amd.md`,
`contexte-long.md`, `convertisseur.md`, `numa-segregation.md`.

**c. Des points d'entrée qui mentaient.** `docs/etat.md` (10/10) et `REPRISE.md` (11/10) décrivaient
encore 34 portes et 122 tests ; `organisation-du-depot.md` citait la 38ᵉ porte et 413 fichiers ;
`utilisation.md` disait 46 portes et 6 chapitres ; `manques.md` disait 27/27 ; le glossaire annonçait
18 documents et 60 rapports. Les nouveaux chantiers **B10–B12** n'étaient ni dans `docs/README.md`,
ni dans `docs/carte.md`, ni dans `docs/synthese/index.md`.

## 2. La méthode

1. **Lire les entrées** (`AGENTS.md`, `README.md`, `docs/README.md`, `docs/carte.md`, `en-cours`,
   `roadmap`, `references`, `reports/README`) et les documents de tâche.
2. **Comparer** chaque invariant aux fichiers du disque (`reports/*.md`, `reports/*.json`,
   `tools/porte-*.sh`, `docs/synthese/0*.md`, `docs/**/*.md`).
3. **Étendre la revue** pour que les défauts soient détectés automatiquement, pas à la main.
4. **Corriger** les documents, puis relancer la revue et `porte-tableaux`.
5. **Ne pas toucher** aux fichiers que le chantier B12 écrivait (`modules-cerveau-langage.md`,
   `rapport-cerveau-modules.md`, journal du 26/10) : ils ont été relus et intégrés par liens.

## 3. Les corrections

### Une source unique

`docs/en-cours.md` porte désormais un bloc **« Les chiffres de l'état »** : 49 portes, 8 chapitres,
179 fichiers / 246 JSON, 53 documents, 1 h 34. Les autres pages y renvoient ; `tools/revue_documentation.py`
compare ces valeurs au disque.

### Les points d'entrée

- `docs/etat.md` : l'ancien index est archivé dans `docs/archive/etat-modules-2026-10-10.md` ; la page
  est une **redirection** vers `en-cours.md` et `roadmap.md`.
- `REPRISE.md` : 138 tests, 49 portes, 1 h 34, dernière passe du 26/10, pointe vers l'état et le plan.
- `docs/organisation-du-depot.md` : entrées actuelles, nommage des plans datés renvoyé à
  `docs/archive/`, compteur `49 portes / 583 fichiers`, date de revue.
- `docs/utilisation.md` : 49 portes, 8 chapitres, 7 schémas, contradiction mdserve corrigée.
- `docs/manques.md` : 49 portes (47/2), feuille de route `roadmap.md`, plan d'origine archivé.
- `docs/glossaire.md` : 53 documents / 179 fichiers, parcours de lecture actuel, 2 276 lignes.
- `docs/references-non-regression.md` : la dernière passe est en tête ; l'historique (10/10 → 26/10
  09 h 40) est dans `reports/historique-passes-portes.md`.

### Les chemins et les orphelins

Les 39 chemins morts sont corrigés vers `docs/archive/...` ; les 3 libellés (`README.md`,
`REPRISE.md`, `docs/roadmap.md`) annoncent la cible réelle ; les 4 orphelins sont liés depuis
`docs/README.md` et `docs/carte.md`. Les documents datés portent
`Dernière vérification : 2026-10-27` et la revue signale ceux de plus de 90 jours.

### B10–B12 et le vocabulaire

- B10, B11 et B12 sont dans `docs/README.md`, `docs/carte.md` et `docs/synthese/index.md`.
- B11 est reformulé partout : **restitution du code (aller-retour RSN) 100 %**,
  **surface originale 33/79** — dans `en-cours`, `carte`, `roadmap`, `reports/README`, `bilan-b11`
  et `rapport-restitution`.
- B10 porte ses deux conditions : **12,7 / 5,3 contre 39,6** (référence complète) et
  **14,0 / 5,4 contre 38,8** (référence tronquée).
- La roadmap est réordonnée **B10 → B11 → B12** ; le bilan B9 est remonté auprès de B9 ; le bas de
  page (ordre du jour, file, décisions, A6.2) est à jour.

### L'index des fiches

`tools/index_reports.py` génère `reports/INDEX.md` : une ligne par fiche, triée par nom, avec son
titre. Il exclut `README.md`, `INDEX.md` et `historique-*` ; la page d'état, elle, compte tous les
`.md`. Au 27/10 10:52 : **176 fiches** dans l'index, **179 fichiers** dans `reports/`.

### La synthèse comme introduction

Les **huit chapitres** de `docs/synthese/` s'ouvrent désormais sur une **fiche concept** (9 fiches au
total), avec un lien vers le glossaire et une illustration ; l'index est une **introduction** (13
concepts, carte des 11 familles, **14 schémas**). Les **170 liens internes** de la synthèse sont
**relatifs** et résolvent ; la revue vérifie la fiche, le lien glossaire, l'image, la date de l'index
et l'usage de chaque schéma.

### Le glossaire par entrée

Le glossaire passe de **11 familles** à **11 familles + 289 fiches** : une **carte courte** par
entrée dans [`docs/glossaire/entrees/`](../docs/glossaire/entrees/), un **index groupé** par famille
dans [`docs/glossaire/README.md`](../docs/glossaire/README.md), et un **manifeste**
[`docs/glossaire/index.json`](../docs/glossaire/index.json) pour mdserve. Le générateur est
`tools/glossaire_cartes.py` ; les fiches sont **exclues du compteur de documents** (comme les
README) et la revue vérifie que chaque fiche est listée dans l'index. Le lien direct évite
l'ancrage dans une famille de 500 lignes.

## 4. L'outillage

`tools/revue_documentation.py` vérifie maintenant :

1. **classement** : pas de résultat dans `docs/` ;
2. **structure** : les sept chantiers C1–C7 ;
3. **annotation** : les liens résolvent **et leur libellé ne ment pas** sur la cible ;
4. **fraîcheur** : la date de `en-cours.md` est celle du **dernier commit** (comparaison réelle) ;
5. **compteurs** : la page d'état dit le disque (portes, chapitres, fichiers, JSON, documents) ;
6. **cohérence** : la synthèse liste les 8 chapitres, les chapitres 7–8 et B10–B12 ;
7. **navigation** : aucun document vivant orphelin, aucun chemin en code inline mort ;
8. **dates** : les documents datés ont une `Dernière vérification` de moins de 90 jours ;
9. **vocabulaire** : « jeton » ne désigne jamais la RSN.

`porte-tableaux` complète : cellules des tableaux, liens, fraîcheur de la page vivante.

## 5. Les résultats

Portes documentaires, au 27/10 après corrections :

```text
revue de documentation · 179 fiche(s) · 246 JSON · 53 doc(s) · 49 porte(s) · 8 chapitre(s)
✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence,
   vocabulaire, navigation

porte-tableaux : ✅ 589 fichiers · 1160 liens relatifs résolvent
                 ✅ la page vivante date du dernier commit (2026-10-27)
```

Les deux passes de révision sont committées : `ca31ba8f` (bandeaux) et `a81c5bd9` (corrections),
puis `831ecdb1` (régénération du journal).

## 6. Ce qui n'a pas été fait, et pourquoi

**La passe complète des 49 portes n'a pas été relancée.** Le chantier B12 écrivait encore :
5 commits entre 09:49 et 10:41, et **1 401 lignes non commitées** dans `tools/cerveau/` à 10:51.
Une passe de 1 h 34 lancée sur cet arbre mesurerait un état qui change sous elle — les rouges
éventuelles ne seraient pas interprétables. La passe de clôture doit être lancée **quand l'arbre
est propre** ; c'est la première action de la file.

**Le journal est en retard d'un commit de housekeeping.** Il est généré par le `pre-commit`, donc
il ne peut pas voir le commit qui l'ajoute. Le commit de passe 2 (`a81c5bd9`) est bien dans
`journal/2026-10-27.md` ; seul le commit de régénération (`831ecdb1`) manque. C'est structurel.

## 7. Ce qui pourrait rendre ce rapport faux

- **Les compteurs bougent** : chaque fiche ou JSON ajouté par B12 change `179 / 246` ; la revue
  échouera volontairement jusqu'à la mise à jour de `en-cours.md`. C'est le but, pas un bug.
- **La revue est syntaxique** : elle vérifie qu'un lien résout et qu'un compteur correspond, pas
  qu'une phrase est vraie. Les contradictions sémantiques profondes (par exemple deux interprétations
  d'une même mesure) restent du ressort de la lecture.
- **Le titre de l'index** est le premier `# ` de la fiche, pas son verdict ; une fiche mal titrée
  entre mal dans l'index.
- **La passe complète manque** : les portes documentaires sont vertes, mais les 49 portes ne sont
  pas toutes rejouées. Le rapport ne dit rien des régressions du moteur.
- **Le corpus B12 a changé pendant l'audit** : les chiffres B12 cités sont ceux des commits
  `8cf29faf` / `091203d1` / `28c09f51` ; les commits `b271db7a` et suivants peuvent les déplacer.

## 8. Reproduire

```bash
python3 tools/revue_documentation.py
bash tools/porte-tableaux.sh
python3 tools/index_reports.py          # régénère reports/INDEX.md
PORTES="tableaux registre" DELAI=600 bash tools/toutes-les-portes.sh
```

## 9. Commits

```text
831ecdb1 JOURNAL — RÉGÉNÉRATION APRÈS LE COMMIT DE COHÉRENCE (9 COMMITS DU 27/10, PASSE 2 VISIBLE)
a81c5bd9 DOCS — PASSE 2/2 : COHÉRENCE APPLIQUÉE (49 PORTES, 8 CHAPITRES, 172/241, 52 DOCS) ; 39 CHEMINS, 4 ORPHELINS, B10–B12, REVUE ÉTENDUE
ca31ba8f DOCS — PASSE 1/2 : BANDEAUX DE RÉVISION SUR LES ENTRÉES (49 PORTES, 8 CHAPITRES, 170/241, 52 DOCS)
```
